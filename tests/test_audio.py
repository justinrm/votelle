import numpy as np
import pytest

from votelle_music.audio.measure import measure_crop
from votelle_music.audio.prepare import prepare_excerpt, read_audio
from votelle_music.data.manifest import load_config, validate
from votelle_music.schemas import VotelleError
from tests.fixtures.build import build_dataset, write_config


def _tone(count: int = 480_000) -> np.ndarray:
    time = np.arange(count) / 48000
    return (0.2 * np.sin(2 * np.pi * 440 * time)).reshape(-1, 1)


def test_diagnostics_have_units_and_method_ids():
    excerpt = np.array([[0.5], [-0.25]])
    rows = {row["metric"]: row for row in measure_crop(excerpt, 2)}
    assert rows["peak_amplitude"]["value"] == 0.5
    assert rows["peak_amplitude"]["unit"] == "1"
    assert rows["peak_amplitude"]["kind"] == "measured"
    assert rows["peak_amplitude"]["method_id"]
    assert rows["clipping"]["value"] is False
    assert rows["duration"]["unit"] == "s"
    assert rows["sample_rate"]["unit"] == "Hz"


def test_nonfinite_silence_bounds_and_rejected_profiles():
    tone = _tone()
    with pytest.raises(VotelleError) as nonfinite:
        dirty = tone.copy()
        dirty[0, 0] = np.nan
        prepare_excerpt(dirty, 48000, 0, 10, "none_fixture_only", False)
    assert nonfinite.value.code == "nonfinite_audio"
    with pytest.raises(VotelleError) as infinite:
        dirty = tone.copy()
        dirty[0, 0] = np.inf
        prepare_excerpt(dirty, 48000, 0, 10, "none_fixture_only", False)
    assert infinite.value.code == "nonfinite_audio"
    with pytest.raises(VotelleError) as silent:
        prepare_excerpt(np.zeros_like(tone), 48000, 0, 10, "none_fixture_only", False)
    assert silent.value.code == "digital_silence"
    with pytest.raises(VotelleError) as short:
        prepare_excerpt(tone, 48000, 0, 9, "none_fixture_only", False)
    assert short.value.code == "duration_not_ten_seconds"
    with pytest.raises(VotelleError) as loudness:
        prepare_excerpt(tone, 48000, 0, 10, "gain_lufs_v1", False)
    assert loudness.value.code == "normalization_profile_rejected"
    with pytest.raises(VotelleError) as claimed:
        prepare_excerpt(tone, 48000, 0, 10, "none_fixture_only", True)
    assert claimed.value.code == "normalization_profile_rejected"


def test_prepare_is_deterministic_and_fixture_profile_has_no_gain(tmp_path):
    root = build_dataset(tmp_path / "data", families=1, stereo=True)
    data, sample_rate = read_audio(root / "audio" / "asset-0.wav")
    first = prepare_excerpt(data, sample_rate, 0, 10, "none_fixture_only", False)
    second = prepare_excerpt(data, sample_rate, 0, 10, "none_fixture_only", False)
    np.testing.assert_array_equal(first.samples, second.samples)
    assert first.samples.shape == (480_000,)
    assert first.method_id == "scipy.signal.resample/fft/v1"
    assert first.preprocessing_id == "none_fixture_only"
    peak = next(row["value"] for row in first.diagnostics if row["metric"] == "peak_amplitude")
    assert peak < 0.999


def test_silent_wav_and_level_matched_claim_fail_validation(tmp_path):
    silent = build_dataset(tmp_path / "silent", families=1, silent=True)
    report = validate(load_config(write_config(tmp_path / "silent.json", silent)))
    assert "digital_silence" in {issue.code for issue in report.issues}

    tonal = build_dataset(tmp_path / "claim", families=1)
    claimed = validate(load_config(write_config(tmp_path / "claim.json", tonal, level_matched=True)))
    assert "normalization_profile_rejected" in {issue.code for issue in claimed.issues}


def test_flac_round_trip(tmp_path):
    root = build_dataset(tmp_path / "flac", families=1, audio_format="flac")
    report = validate(load_config(write_config(tmp_path / "flac.json", root)))
    assert report.issues == []
