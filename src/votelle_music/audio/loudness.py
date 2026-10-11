"""ITU-R BS.1770-4 integrated loudness and a 4x true-peak estimate.

Both are measurements of the prepared excerpt. They are not preference scores
and not evidence that a tone is musically suitable.
"""

from __future__ import annotations

import math

import numpy as np
from scipy.signal import lfilter, resample_poly

from votelle_music.schemas import VotelleError

RATE = 48000
BLOCK = 19200  # 400 ms
HOP = 4800  # 100 ms, 75% overlap
ABSOLUTE_GATE_LUFS = -70.0
# ponytail: 4x Kaiser resample_poly, not the BS.1770 annex FIR. Replace that FIR if a compliance item fails.
TRUE_PEAK_METHOD = "scipy.signal.resample_poly/4x/kaiser5/line-pad/v1"
LOUDNESS_METHOD = "itu-r-bs.1770-4/k-weight/48kHz/v1"


def _biquads() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """BS.1770-4 K-weighting at 48 kHz, in the form published by De Man."""
    frequency = 1681.9744509555319
    gain = 3.99984385397
    quality = 0.7071752369554193
    k = math.tan(math.pi * frequency / RATE)
    high = 10.0 ** (gain / 20.0)
    bridge = high ** 0.499666774155
    denominator = 1.0 + k / quality + k * k
    shelf_b = np.array(
        [
            (high + bridge * k / quality + k * k) / denominator,
            2.0 * (k * k - high) / denominator,
            (high - bridge * k / quality + k * k) / denominator,
        ]
    )
    shelf_a = np.array([1.0, 2.0 * (k * k - 1.0) / denominator, (1.0 - k / quality + k * k) / denominator])
    frequency = 38.13547087613982
    quality = 0.5003270373253953
    k = math.tan(math.pi * frequency / RATE)
    denominator = 1.0 + k / quality + k * k
    highpass_b = np.array([1.0, -2.0, 1.0])
    highpass_a = np.array(
        [1.0, 2.0 * (k * k - 1.0) / denominator, (1.0 - k / quality + k * k) / denominator]
    )
    return shelf_b, shelf_a, highpass_b, highpass_a


_SHELF_B, _SHELF_A, _HP_B, _HP_A = _biquads()


def _require_rate(sample_rate: int) -> None:
    if int(sample_rate) != RATE:
        raise VotelleError(
            "invalid_audio",
            "The BS.1770-4 coefficients are pinned at 48000 Hz.",
            field="sample_rate",
        )


def _as_channels(samples: np.ndarray) -> np.ndarray:
    audio = np.asarray(samples, dtype=np.float64)
    if audio.ndim == 1:
        audio = audio[:, None]
    if audio.ndim != 2 or audio.shape[1] not in {1, 2}:
        raise VotelleError("invalid_audio", "Loudness measurement accepts mono or stereo.", field="relative_path")
    if not np.isfinite(audio).all():
        raise VotelleError("nonfinite_audio", "Audio contains NaN or Inf.", field="relative_path")
    return np.ascontiguousarray(audio)


def _k_weight(channel: np.ndarray) -> np.ndarray:
    return lfilter(_HP_B, _HP_A, lfilter(_SHELF_B, _SHELF_A, channel))


def _block_power(audio: np.ndarray) -> np.ndarray:
    if audio.shape[0] < BLOCK:
        raise VotelleError(
            "loudness_window_too_short",
            "Integrated loudness needs at least 400 ms at 48000 Hz.",
            field="relative_path",
        )
    count = 1 + (audio.shape[0] - BLOCK) // HOP
    weighted = np.zeros(count, dtype=np.float64)
    for index in range(audio.shape[1]):
        filtered = _k_weight(audio[:, index])
        for block in range(count):
            start = block * HOP
            segment = filtered[start : start + BLOCK]
            weighted[block] += float(np.dot(segment, segment) / BLOCK)
    return weighted


def _lufs(power: float) -> float:
    if power <= 0.0 or not math.isfinite(power):
        return float("-inf")
    return -0.691 + 10.0 * math.log10(power)


def measure_loudness(samples: np.ndarray, sample_rate: int) -> tuple[float, float]:
    """Return gated integrated LUFS and ungated block-power LUFS.

    Ungated power is only a gain fallback when every block is below the
    absolute gate. The stored audition measurement is the gated value.
    """
    _require_rate(sample_rate)
    powers = _block_power(_as_channels(samples))
    ungated = _lufs(float(np.mean(powers)))
    block_lufs = np.array([_lufs(float(power)) for power in powers])
    above_absolute = block_lufs > ABSOLUTE_GATE_LUFS
    if not np.any(above_absolute):
        return float("-inf"), ungated
    absolute_power = float(np.mean(powers[above_absolute]))
    relative_gate = _lufs(absolute_power) - 10.0
    selected = above_absolute & (block_lufs > relative_gate)
    if not np.any(selected):
        return float("-inf"), ungated
    return _lufs(float(np.mean(powers[selected]))), ungated


def integrated_loudness(samples: np.ndarray, sample_rate: int) -> float:
    integrated, _ungated = measure_loudness(samples, sample_rate)
    return integrated


def true_peak_linear(samples: np.ndarray) -> float:
    audio = np.asarray(samples, dtype=np.float64).reshape(-1)
    if audio.size == 0:
        return 0.0
    if not np.isfinite(audio).all():
        raise VotelleError("nonfinite_audio", "Audio contains NaN or Inf.", field="relative_path")
    oversampled = resample_poly(audio, 4, 1, padtype="line")
    return float(np.max(np.abs(oversampled)))


def true_peak_dbtp(samples: np.ndarray) -> float:
    linear = true_peak_linear(samples)
    if linear <= 0.0:
        return float("-inf")
    return 20.0 * math.log10(linear)
