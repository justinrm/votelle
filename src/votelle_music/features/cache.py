"""Content-keyed feature cache.

ponytail: atomic replace for one process. Add a lock if extractors share a cache.
"""

from __future__ import annotations

import os
from pathlib import Path

import numpy as np

from votelle_music.features.base import FeatureError
from votelle_music.schemas import canonical_bytes, sha256_hex


def feature_cache_key(
    *,
    source_pcm_sha256: str,
    start_seconds: float,
    end_seconds: float,
    preprocessing_sha256: str,
    encoder_id: str,
    encoder_revision: str,
    processor_hash: str = "none",
    pooling: str = "clip",
    dtype: str = "float32",
) -> str:
    payload = {
        "dtype": dtype,
        "encoder_id": encoder_id,
        "encoder_revision": encoder_revision,
        "end_seconds": float(end_seconds),
        "pooling": pooling,
        "preprocessing_sha256": preprocessing_sha256,
        "processor_hash": processor_hash,
        "source_pcm_sha256": source_pcm_sha256,
        "start_seconds": float(start_seconds),
    }
    return sha256_hex(canonical_bytes(payload))


def store_feature(cache_dir: Path, key: str, vector: np.ndarray) -> Path:
    if len(key) != 64 or any(character not in "0123456789abcdef" for character in key):
        raise FeatureError("schema_invalid", "Feature cache keys must be 64 lowercase hex characters.")
    stored = np.ascontiguousarray(vector, dtype=np.float32)
    if stored.shape != (512,):
        raise FeatureError("encoder_dimension", "Cache entries must be vectors of length 512.")
    if not np.isfinite(stored).all():
        raise FeatureError("nonfinite_embedding", "Cache entries must be finite.")
    cache_dir.mkdir(parents=True, exist_ok=True)
    path = cache_dir / f"{key}.npy"
    if path.exists():
        return path
    temporary = cache_dir / f".{key}.tmp.npy"
    with temporary.open("wb") as handle:
        np.save(handle, stored, allow_pickle=False)
    os.replace(temporary, path)
    return path


def load_feature(path: Path) -> np.ndarray:
    vector = np.load(path, allow_pickle=False)
    if getattr(vector, "dtype", None) == object:
        raise FeatureError("schema_invalid", "Feature cache refused a pickled array.")
    return vector
