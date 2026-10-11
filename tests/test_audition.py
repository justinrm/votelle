"""Gain-only audition normalization. Tones are fixtures, not musical-suitability evidence."""

import json

import numpy as np
import pytest
import soundfile as sf

from votelle_music.audio.loudness import integrated_loudness
from votelle_music.audio.prepare import (
    INTEGRATED_TOLERANCE_LU,
    file_sha256,
    pcm_hash,
    prepare_excerpt,
    preprocessing_document,
    read_audio,
    waveform_for_encoder,
)
from votelle_music.data.manifest import load_config, validate
from votelle_music.features.cache import feature_cache_key
from votelle_music.features.dummy import DummyEncoder
from votelle_music.schemas import VotelleError, canonical_bytes, sha256_hex
from tests.fixtures.build import build_dataset, foundation_config, write_config

RATE = 48000
N = 480_000


def _sine(amplitude: float, frequency: float = 1000.0, phase: float = 0.0, count: int = N) -> np.ndarray:
    time = np.arange(count) / RATE
    return (amplitude * np.sin(2 * np.pi * frequency * time + phase)).reshape(-1, 1)


def _prepare(samples: np.ndarray, profile: str = "gain_lufs_v1", level_matched: bool = True, rate: int = RATE):
    return prepare_excerpt(samples, rate, 0.0, 10.0, profile, level_matched)


def test_bs1770_meter_matches_the_stereo_reference_tone():
    amplitude = 10 ** (-23 / 20)
    tone = _sine(amplitude)[:, 0]
    stereo = np.column_stack([tone, tone])
    assert integrated_loudness(stereo, RATE) == pytest.approx(-23.0, abs=0.1)
    assert integrated_loudness(tone, RATE) == pytest.approx(-23.0 - 10 * np.log10(2), abs=0.1)


def test_steady_tone_hits_target_loudness_without_crossing_the_ceiling():
    assert INTEGRATED_TOLERANCE_LU == 0.1
    prepared = _prepare(_sine(0.2, frequency=440.0))
    assert prepared.samples.shape == (N,)
    assert prepared.sample_rate == RATE
    assert prepared.loudness_mismatch is False
    assert prepared.gain_limited_by == "loudness"
    assert prepared.integrated_lufs == pytest.approx(-20.0, abs=INTEGRATED_TOLERANCE_LU)
    assert prepared.true_peak_dbtp <= -1.0
    base = _prepare(_sine(0.2, frequency=440.0), profile="none_fixture_only", level_matched=False)
    scale = 10 ** (prepared.gain_db / 20)
    np.testing.assert_allclose(prepared.samples, base.samples * scale, rtol=0, atol=1e-12)


def test_hot_sine_is_attenuated_by_gain_alone():
    hot = _sine(2.0)
    prepared = _prepare(hot)
    base = _prepare(hot, profile="none_fixture_only", level_matched=False)
    scale = 10 ** (prepared.gain_db / 20)
    np.testing.assert_allclose(prepared.samples, base.samples * scale, rtol=0, atol=1e-12)
    assert prepared.loudness_mismatch is False
    assert prepared.integrated_lufs == pytest.approx(-20.0, abs=INTEGRATED_TOLERANCE_LU)
    assert prepared.true_peak_dbtp <= -1.0
    assert np.max(np.abs(prepared.samples)) < 1.0


def test_peak_ceiling_blocks_the_loudness_target_and_is_flagged():
    tone = _sine(0.001)[:, 0]
    tone[N // 2] = 0.8
    prepared = _prepare(tone.reshape(-1, 1))
    assert prepared.loudness_mismatch is True
    assert prepared.gain_limited_by == "true_peak"
    assert prepared.true_peak_dbtp == pytest.approx(-1.0, abs=0.05)
    assert prepared.true_peak_dbtp <= -1.0 + 1e-6
    assert abs(prepared.integrated_lufs - (-20.0)) > INTEGRATED_TOLERANCE_LU
    base = _prepare(tone.reshape(-1, 1), profile="none_fixture_only", level_matched=False)
    scale = 10 ** (prepared.gain_db / 20)
    np.testing.assert_allclose(prepared.samples, base.samples * scale, rtol=0, atol=1e-10)


def test_quiet_tone_above_digital_silence_can_still_be_matched():
    prepared = _prepare(_sine(1e-6))
    assert prepared.loudness_mismatch is False
    assert prepared.integrated_lufs == pytest.approx(-20.0, abs=INTEGRATED_TOLERANCE_LU)
    assert prepared.true_peak_dbtp <= -1.0


def test_gain_path_rejects_silent_nonfinite_invalid_and_out_of_bounds(tmp_path):
    tone = _sine(0.2)
    with pytest.raises(VotelleError) as silent:
        _prepare(np.zeros_like(tone))
    assert silent.value.code == "digital_silence"
    with pytest.raises(VotelleError) as nonfinite:
        dirty = tone.copy()
        dirty[10, 0] = np.nan
        _prepare(dirty)
    assert nonfinite.value.code == "nonfinite_audio"
    with pytest.raises(VotelleError) as flat:
        _prepare(tone[:, 0])
    assert flat.value.code == "invalid_audio"
    with pytest.raises(VotelleError) as bounds:
        prepare_excerpt(tone, RATE, 5.0, 15.0, "gain_lufs_v1", True)
    assert bounds.value.code == "bad_bounds"
    with pytest.raises(VotelleError) as short:
        prepare_excerpt(tone, RATE, 0.0, 9.0, "gain_lufs_v1", True)
    assert short.value.code == "duration_not_ten_seconds"
    bogus = tmp_path / "clip.mp3"
    bogus.write_bytes(b"not audio")
    with pytest.raises(VotelleError) as invalid:
        read_audio(bogus)
    assert invalid.value.code == "unsupported_format"


def test_inverted_stereo_is_phase_cancellation_not_a_level_match():
    tone = _sine(0.2)[:, 0]
    stereo = np.column_stack([tone, -tone])
    with pytest.raises(VotelleError) as cancelled:
        _prepare(stereo)
    assert cancelled.value.code == "phase_cancellation"


def test_gain_preparation_is_deterministic_and_leaves_the_source_file(tmp_path):
    root = build_dataset(tmp_path / "data", families=1)
    path = root / "audio" / "asset-0.wav"
    original = path.read_bytes()
    data, sample_rate = read_audio(path)
    first = prepare_excerpt(data, sample_rate, 0.0, 10.0, "gain_lufs_v1", True)
    second = prepare_excerpt(data, sample_rate, 0.0, 10.0, "gain_lufs_v1", True)
    np.testing.assert_array_equal(first.samples, second.samples)
    assert first.preprocessing_sha256 == second.preprocessing_sha256
    assert path.read_bytes() == original
    assert first.integrated_lufs == pytest.approx(-20.0, abs=INTEGRATED_TOLERANCE_LU)


def test_preprocessing_hash_changes_when_the_gain_profile_changes():
    tone = _sine(0.2)
    fixture = _prepare(tone, profile="none_fixture_only", level_matched=False)
    gained = _prepare(tone)
    assert fixture.preprocessing_id == "none_fixture_only"
    assert gained.preprocessing_id == "gain_lufs_v1"
    assert fixture.preprocessing_sha256 != gained.preprocessing_sha256
    document = preprocessing_document("gain_lufs_v1")
    assert document["target_lufs"] == -20.0
    assert document["true_peak_ceiling_dbtp"] == -1.0
    assert sha256_hex(canonical_bytes(document)) == gained.preprocessing_sha256
    changed = dict(document)
    changed["target_lufs"] = -23.0
    assert sha256_hex(canonical_bytes(changed)) != gained.preprocessing_sha256
    source = "a" * 64
    assert feature_cache_key(
        source_pcm_sha256=source,
        start_seconds=0.0,
        end_seconds=10.0,
        preprocessing_sha256=fixture.preprocessing_sha256,
        encoder_id="dummy",
        encoder_revision="fixture-v1",
    ) != feature_cache_key(
        source_pcm_sha256=source,
        start_seconds=0.0,
        end_seconds=10.0,
        preprocessing_sha256=gained.preprocessing_sha256,
        encoder_id="dummy",
        encoder_revision="fixture-v1",
    )


def test_listening_samples_and_encoder_waveform_are_the_same_excerpt():
    prepared = _prepare(_sine(0.2, frequency=440.0))
    wave = waveform_for_encoder(prepared)
    assert wave.shape == (N,)
    assert wave.dtype == np.float32
    assert np.isfinite(wave).all()
    np.testing.assert_allclose(prepared.samples, wave, rtol=0, atol=np.finfo(np.float32).eps * 4)
    encoder = DummyEncoder()
    first = encoder.embed_audio([prepared])
    second = encoder.embed_audio([prepared])
    np.testing.assert_array_equal(first.vectors, second.vectors)
    fixture = _prepare(_sine(0.2, frequency=440.0), profile="none_fixture_only", level_matched=False)
    assert not np.array_equal(encoder.embed_audio([fixture]).vectors, first.vectors)


def _gain_config(path, root):
    audio = foundation_config(root)["audio"]
    audio["normalization_profile"] = "gain_lufs_v1"
    return write_config(path, root, level_matched=True, audio=audio)


def _replace_asset(root, samples: np.ndarray):
    path = root / "audio" / "asset-0.wav"
    sf.write(path, samples, RATE, subtype="PCM_16")
    decoded, sample_rate = read_audio(path)
    record = json.loads((root / "assets.jsonl").read_text(encoding="utf-8").splitlines()[0])
    record["sha256_original"] = file_sha256(path)
    record["sha256_pcm"] = pcm_hash(decoded)
    record["sample_rate"] = sample_rate
    record["channels"] = int(decoded.shape[1])
    record["duration_seconds"] = decoded.shape[0] / sample_rate
    (root / "assets.jsonl").write_text(json.dumps(record) + "\n", encoding="utf-8")
    clip = json.loads((root / "clips.jsonl").read_text(encoding="utf-8").splitlines()[0])
    clip["audition_condition"] = "gain_lufs_v1"
    (root / "clips.jsonl").write_text(json.dumps(clip) + "\n", encoding="utf-8")


def test_validation_accepts_gain_profile_and_warns_when_the_ceiling_binds(tmp_path):
    matched = build_dataset(tmp_path / "matched", families=1)
    _replace_asset(matched, _sine(0.2, frequency=440.0)[:, 0])
    report = validate(load_config(_gain_config(tmp_path / "matched.json", matched)))
    assert report.issues == []

    conflict = build_dataset(tmp_path / "conflict", families=1)
    spike = _sine(0.001)[:, 0]
    spike[N // 2] = 0.8
    _replace_asset(conflict, spike)
    flagged = validate(load_config(_gain_config(tmp_path / "conflict.json", conflict)))
    warnings = [issue for issue in flagged.issues if issue.code == "loudness_mismatch"]
    assert len(warnings) == 1
    assert warnings[0].severity == "warning"
    assert flagged.has_errors() is False
