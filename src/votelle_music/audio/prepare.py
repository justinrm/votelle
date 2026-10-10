"""Decode WAV/FLAC and build a 10-second mono excerpt.

`none_fixture_only` resamples and does not change gain. `gain_lufs_v1` is the
audition profile: one constant gain toward -20 LUFS, limited by -1 dBTP.
Neither profile compresses, limits, pads, or picks a crop.
"""

from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy.signal import resample

from votelle_music.audio.loudness import (
    LOUDNESS_METHOD,
    TRUE_PEAK_METHOD,
    measure_loudness,
    true_peak_linear,
)
from votelle_music.audio.measure import is_digital_silence, measure_crop
from votelle_music.schemas import MusicPrefError, canonical_bytes, sha256_hex

TARGET_RATE = 48000
TARGET_SAMPLES = 480_000
EXCERPT_SECONDS = 10.0
DURATION_TOLERANCE = 0.001
RESAMPLE_METHOD = "scipy.signal.resample/fft/v1"
FIXTURE_PROFILE = "none_fixture_only"
GAIN_PROFILE = "gain_lufs_v1"
TARGET_LUFS = -20.0
CEILING_DBTP = -1.0
INTEGRATED_TOLERANCE_LU = 0.1  # EBU Tech 3341 minimum tolerance for integrated loudness
# ponytail: equal-mean fold-down. Use ITU surround weights if a 5.1 lane appears.
DOWNMIX_METHOD = "equal_mean/phase_ratio_0.01/v1"
PHASE_RATIO_MIN = 0.01
PROFILE_REJECTION = "level_matched requires gain_lufs_v1. none_fixture_only applies no loudness match."


@dataclass
class PreparedExcerpt:
    samples: np.ndarray
    sample_rate: int
    method_id: str
    preprocessing_id: str
    preprocessing_sha256: str
    diagnostics: list[dict]
    gain_db: float = 0.0
    integrated_lufs: float | None = None
    true_peak_dbtp: float | None = None
    gain_limited_by: str = "not_applicable"
    loudness_mismatch: bool = False


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pcm_hash(samples: np.ndarray) -> str:
    array = np.ascontiguousarray(samples, dtype=np.float32)
    return hashlib.sha256(array.tobytes()).hexdigest()


def preprocessing_document(profile: str) -> dict:
    payload = {
        "channels": 1,
        "excerpt_seconds": EXCERPT_SECONDS,
        "method_id": RESAMPLE_METHOD,
        "normalization_profile": profile,
        "sample_rate": TARGET_RATE,
    }
    if profile == GAIN_PROFILE:
        payload.update(
            {
                "absolute_gate_fallback": "ungated_block_power_v1",
                "downmix_method": DOWNMIX_METHOD,
                "integrated_tolerance_lu": INTEGRATED_TOLERANCE_LU,
                "loudness_method": LOUDNESS_METHOD,
                "target_lufs": TARGET_LUFS,
                "true_peak_ceiling_dbtp": CEILING_DBTP,
                "true_peak_method": TRUE_PEAK_METHOD,
            }
        )
    elif profile != FIXTURE_PROFILE:
        raise MusicPrefError("normalization_profile_rejected", PROFILE_REJECTION, field="normalization_profile")
    return payload


def read_audio(path: Path) -> tuple[np.ndarray, int]:
    if path.suffix.lower() not in {".wav", ".flac"}:
        raise MusicPrefError("unsupported_format", "Use WAV or FLAC.", field="relative_path")
    try:
        data, sample_rate = sf.read(path, always_2d=True, dtype="float64")
    except Exception as exc:
        raise MusicPrefError(
            "unsupported_format",
            f"Could not decode audio: {exc}",
            field="relative_path",
        ) from exc
    if not np.isfinite(data).all():
        raise MusicPrefError("nonfinite_audio", "Audio contains NaN or Inf.", field="relative_path")
    return data, int(sample_rate)


def crop_samples(data: np.ndarray, sample_rate: int, start_seconds: float, end_seconds: float) -> np.ndarray:
    if end_seconds <= start_seconds:
        raise MusicPrefError("bad_bounds", "end_seconds must be greater than start_seconds.", field="end_seconds")
    if abs((end_seconds - start_seconds) - EXCERPT_SECONDS) > DURATION_TOLERANCE:
        raise MusicPrefError(
            "duration_not_ten_seconds",
            "v0.1 clips must be 10 seconds within 1 ms. Do not pad or trim.",
            field="end_seconds",
        )
    start = int(round(start_seconds * sample_rate))
    end = int(round(end_seconds * sample_rate))
    if start < 0 or end > data.shape[0] or end <= start:
        raise MusicPrefError("bad_bounds", "Clip bounds fall outside the decoded asset.", field="start_seconds")
    return data[start:end]


def _reject_profile(profile: str, level_matched: bool) -> None:
    if profile == FIXTURE_PROFILE and not level_matched:
        return
    if profile == GAIN_PROFILE and level_matched:
        return
    raise MusicPrefError("normalization_profile_rejected", PROFILE_REJECTION, field="normalization_profile")


def _downmix(excerpt: np.ndarray) -> tuple[np.ndarray, float]:
    if excerpt.ndim != 2 or excerpt.shape[1] < 1:
        raise MusicPrefError("invalid_audio", "Expected audio shaped (samples, channels).", field="relative_path")
    if excerpt.shape[1] == 1:
        return np.ascontiguousarray(excerpt[:, 0], dtype=np.float64), 1.0
    mono = np.ascontiguousarray(excerpt.mean(axis=1), dtype=np.float64)
    channel_power = float(np.mean(np.square(excerpt)))
    mono_power = float(np.mean(np.square(mono)))
    ratio = 1.0 if channel_power == 0.0 else mono_power / channel_power
    cancelled = is_digital_silence(mono) and not is_digital_silence(excerpt)
    if cancelled or (ratio < PHASE_RATIO_MIN and not is_digital_silence(excerpt)):
        raise MusicPrefError(
            "phase_cancellation",
            "Downmix cancelled the channels. Check polarity. Stereo preference is outside this pilot.",
            field="relative_path",
        )
    return mono, ratio


def _metric(metric: str, value, unit: str, method_id: str, kind: str = "measured") -> dict:
    return {"metric": metric, "value": value, "unit": unit, "method_id": method_id, "kind": kind}


def _apply_gain(mono: np.ndarray) -> tuple[np.ndarray, float, float, float, str, bool]:
    # ponytail: one pre-gain measurement. Iterate only if gate membership moves real program outside 0.1 LU.
    integrated, ungated = measure_loudness(mono, TARGET_RATE)
    reference = integrated if math.isfinite(integrated) else ungated
    peak = true_peak_linear(mono)
    if peak <= 0.0 or not math.isfinite(reference):
        raise MusicPrefError(
            "digital_silence",
            "Digital silence is invalid. This check does not score quiet music.",
            field="relative_path",
        )
    ceiling = 10.0 ** (CEILING_DBTP / 20.0)
    gain_for_loudness = 10.0 ** ((TARGET_LUFS - reference) / 20.0)
    gain_for_peak = ceiling / peak
    limited_by = "true_peak" if gain_for_peak < gain_for_loudness else "loudness"
    gain = min(gain_for_loudness, gain_for_peak)
    gained = mono * gain
    measured_peak = true_peak_linear(gained)
    if measured_peak > ceiling:
        gain *= ceiling / measured_peak
        gained = mono * gain
        limited_by = "true_peak"
    after_lufs, _after_ungated = measure_loudness(gained, TARGET_RATE)
    after_peak = true_peak_linear(gained)
    if after_peak > ceiling:
        gain *= ceiling / after_peak
        gained = mono * gain
        limited_by = "true_peak"
        after_lufs, _after_ungated = measure_loudness(gained, TARGET_RATE)
        after_peak = true_peak_linear(gained)
    true_peak_dbtp = float("-inf") if after_peak <= 0.0 else 20.0 * math.log10(after_peak)
    mismatch = (not math.isfinite(after_lufs)) or abs(after_lufs - TARGET_LUFS) > INTEGRATED_TOLERANCE_LU
    return gained, gain, after_lufs, true_peak_dbtp, limited_by, mismatch


def prepare_excerpt(
    data: np.ndarray,
    sample_rate: int,
    start_seconds: float,
    end_seconds: float,
    profile: str,
    level_matched: bool,
) -> PreparedExcerpt:
    _reject_profile(profile, level_matched)
    if not isinstance(sample_rate, (int, np.integer)) or int(sample_rate) <= 0:
        raise MusicPrefError("invalid_audio", "Sample rate must be a positive integer.", field="sample_rate")
    audio = np.asarray(data)
    if audio.ndim != 2 or audio.shape[1] < 1:
        raise MusicPrefError("invalid_audio", "Expected audio shaped (samples, channels).", field="relative_path")
    if not np.isfinite(audio).all():
        raise MusicPrefError("nonfinite_audio", "Audio contains NaN or Inf.", field="relative_path")
    excerpt = crop_samples(audio, int(sample_rate), start_seconds, end_seconds)
    if is_digital_silence(excerpt):
        raise MusicPrefError(
            "digital_silence",
            "Digital silence is invalid. This check does not score quiet music.",
            field="relative_path",
        )
    diagnostics = measure_crop(excerpt, int(sample_rate))
    mono, ratio = _downmix(excerpt)
    diagnostics.append(_metric("downmix_energy_ratio", ratio, "1", DOWNMIX_METHOD))
    prepared = np.asarray(resample(mono, TARGET_SAMPLES), dtype=np.float64).reshape(-1)
    if prepared.shape != (TARGET_SAMPLES,) or not np.isfinite(prepared).all():
        raise MusicPrefError("nonfinite_audio", "Resampling produced a non-finite sample.", field="relative_path")
    gain_db = 0.0
    integrated_lufs = None
    true_peak_dbtp = None
    limited_by = "not_applicable"
    mismatch = False
    if profile == GAIN_PROFILE:
        prepared, gain, integrated_lufs, true_peak_dbtp, limited_by, mismatch = _apply_gain(prepared)
        if prepared.shape != (TARGET_SAMPLES,) or not np.isfinite(prepared).all():
            raise MusicPrefError("nonfinite_audio", "Gain produced a non-finite sample.", field="relative_path")
        gain_db = 20.0 * math.log10(gain)
        if not math.isfinite(integrated_lufs):
            integrated_lufs = None
        if true_peak_dbtp is None or not math.isfinite(true_peak_dbtp):
            true_peak_dbtp = None
        diagnostics.extend(
            [
                _metric("integrated_lufs", integrated_lufs, "LUFS", LOUDNESS_METHOD),
                _metric("true_peak_dbtp", true_peak_dbtp, "dBTP", TRUE_PEAK_METHOD),
                _metric("gain_db", gain_db, "dB", "constant_gain_v1", "decision"),
                _metric("gain_limited_by", limited_by, "enum", "min_loudness_and_true_peak_v1", "decision"),
                _metric("loudness_mismatch", mismatch, "bool", f"abs_lu_gt_{INTEGRATED_TOLERANCE_LU}_v1", "decision"),
                _metric("prepared_pcm_sha256", pcm_hash(prepared), "sha256", "float32_le_v1"),
            ]
        )
    document = preprocessing_document(profile)
    return PreparedExcerpt(
        samples=np.ascontiguousarray(prepared, dtype=np.float64),
        sample_rate=TARGET_RATE,
        method_id=RESAMPLE_METHOD,
        preprocessing_id=profile,
        preprocessing_sha256=sha256_hex(canonical_bytes(document)),
        diagnostics=diagnostics,
        gain_db=gain_db,
        integrated_lufs=integrated_lufs,
        true_peak_dbtp=true_peak_dbtp,
        gain_limited_by=limited_by,
        loudness_mismatch=mismatch,
    )


def waveform_for_encoder(excerpt: PreparedExcerpt) -> np.ndarray:
    """Float32 copy of the samples a listener hears. One buffer for a future CLAP call."""
    wave = np.ascontiguousarray(excerpt.samples, dtype=np.float32)
    if wave.shape != (TARGET_SAMPLES,) or not np.isfinite(wave).all():
        raise MusicPrefError(
            "invalid_audio",
            "Encoder waveform must be 480000 finite float32 samples.",
            field="relative_path",
        )
    return wave
