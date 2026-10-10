import numpy as np
import pytest

from music_pref.audio.prepare import prepare_excerpt, read_audio
from music_pref.data.manifest import load_config, validate
from music_pref.features.base import FeatureError, l2_normalize
from music_pref.features.cache import feature_cache_key, load_feature, store_feature
from music_pref.features.dummy import DummyEncoder
from music_pref.schemas import MusicPrefError
from tests.fixtures.build import build_dataset, make_brief, write_config


def _key(**overrides):
    payload = {
        "source_pcm_sha256": "a" * 64,
        "start_seconds": 0.0,
        "end_seconds": 10.0,
        "preprocessing_sha256": "b" * 64,
        "encoder_id": "dummy",
        "encoder_revision": "fixture-v1",
    }
    payload.update(overrides)
    return feature_cache_key(**payload)


def test_dummy_encoder_is_finite_repeatable_and_not_a_production_model(tmp_path):
    root = build_dataset(tmp_path / "data", families=1)
    data, sample_rate = read_audio(root / "audio" / "asset-0.wav")
    prepared = prepare_excerpt(data, sample_rate, 0, 10, "none_fixture_only", False)
    encoder = DummyEncoder()
    first = encoder.embed_audio([prepared])
    second = encoder.embed_audio([prepared])
    np.testing.assert_array_equal(first.vectors, second.vectors)
    assert first.vectors.shape == (1, 512)
    assert first.vectors.dtype == np.float32
    assert np.isfinite(first.vectors).all()
    assert abs(float(np.linalg.norm(first.vectors[0])) - 1.0) < 1e-5
    assert encoder.describe().production_claim_allowed is False
    text = encoder.embed_text([make_brief(1), make_brief(1)])
    np.testing.assert_array_equal(text.vectors[0], text.vectors[1])
    assert not np.array_equal(text.vectors[0], first.vectors[0])


def test_normalization_rejects_zero_and_wrong_dimension():
    with pytest.raises(FeatureError) as zero:
        l2_normalize(np.zeros(512))
    assert zero.value.code == "zero_norm"
    with pytest.raises(FeatureError) as dimension:
        l2_normalize(np.ones(511))
    assert dimension.value.code == "encoder_dimension"
    with pytest.raises(MusicPrefError) as nonfinite:
        l2_normalize(np.full(512, np.nan))
    assert nonfinite.value.code == "nonfinite_embedding"


def test_cache_key_changes_with_inputs_and_store_is_immutable(tmp_path):
    original = _key()
    assert _key() == original
    assert _key(source_pcm_sha256="c" * 64) != original
    assert _key(end_seconds=10.001) != original
    assert _key(preprocessing_sha256="d" * 64) != original
    assert _key(encoder_revision="fixture-v2") != original
    vector = l2_normalize(np.arange(512))
    path = store_feature(tmp_path, original, vector)
    store_feature(tmp_path, original, l2_normalize(np.ones(512)))
    np.testing.assert_array_equal(load_feature(path), vector)


def test_changed_audio_changes_the_cache_key(tmp_path):
    from music_pref.audio.prepare import pcm_hash

    root = build_dataset(tmp_path / "one", families=1)
    data, sample_rate = read_audio(root / "audio" / "asset-0.wav")
    prepared = prepare_excerpt(data, sample_rate, 0, 10, "none_fixture_only", False)
    original = _key(source_pcm_sha256=pcm_hash(data), preprocessing_sha256=prepared.preprocessing_sha256)
    changed = data.copy()
    changed[0, 0] += 0.05
    assert _key(source_pcm_sha256=pcm_hash(changed), preprocessing_sha256=prepared.preprocessing_sha256) != original
    repeated = prepare_excerpt(data, sample_rate, 0, 10, "none_fixture_only", False)
    assert _key(source_pcm_sha256=pcm_hash(data), preprocessing_sha256=repeated.preprocessing_sha256) == original
    report = validate(load_config(write_config(tmp_path / "config.json", root)))
    assert report.issues == []
