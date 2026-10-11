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


def _require_cached_vector(vector: np.ndarray) -> None:
    dtype = getattr(vector, "dtype", None)
    if not isinstance(vector, np.ndarray) or dtype is None or getattr(dtype, "hasobject", False):
        raise FeatureError("schema_invalid", "Feature cache refused a pickled array.")
    if dtype != np.float32:
        raise FeatureError(
            "schema_invalid",
            "Cache entries must be float32. Delete the entry and recompute the embedding.",
        )
    if vector.shape != (512,):
        raise FeatureError("encoder_dimension", "Cache entries must be vectors of length 512.")
    if not np.isfinite(vector).all():
        raise FeatureError("nonfinite_embedding", "Cache entries must be finite.")


def store_feature(cache_dir: Path, key: str, vector: np.ndarray) -> Path:
    if len(key) != 64 or any(character not in "0123456789abcdef" for character in key):
        raise FeatureError("schema_invalid", "Feature cache keys must be 64 lowercase hex characters.")
    stored = np.ascontiguousarray(vector, dtype=np.float32)
    _require_cached_vector(stored)
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
    try:
        vector = np.load(path, allow_pickle=False)
    except (OSError, EOFError, ValueError) as exc:
        text = str(exc).lower()
        if "pickle" in text or "object" in text:
            raise FeatureError("schema_invalid", "Feature cache refused a pickled array.") from exc
        raise FeatureError(
            "schema_invalid",
            "Feature cache file is unreadable. Delete it and recompute the embedding.",
        ) from exc
    _require_cached_vector(vector)
    return vector
