"""Encoder protocol. Scorers consume features, not media paths."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import numpy as np

from votelle_music.audio.prepare import PreparedExcerpt
from votelle_music.schemas import Brief, EncoderSpec, VotelleError


class FeatureError(VotelleError):
    pass


@dataclass
class FeatureBatch:
    vectors: np.ndarray
    spec: EncoderSpec


def l2_normalize(vector: np.ndarray) -> np.ndarray:
    array = np.asarray(vector, dtype=np.float64)
    if array.shape != (512,):
        raise FeatureError("encoder_dimension", "Embeddings must be one finite vector of length 512.")
    if not np.isfinite(array).all():
        raise FeatureError("nonfinite_embedding", "Embedding contains NaN or Inf.")
    norm = float(np.linalg.norm(array))
    if norm == 0.0 or not np.isfinite(norm):
        raise FeatureError("zero_norm", "Refusing to normalize a zero vector.")
    normalized = (array / norm).astype(np.float32)
    if not np.isfinite(normalized).all():
        raise FeatureError("nonfinite_embedding", "Normalization produced a non-finite value.")
    return normalized


class AudioTextEncoder(Protocol):
    def describe(self) -> EncoderSpec: ...

    def embed_audio(self, clips: list[PreparedExcerpt]) -> FeatureBatch: ...

    def embed_text(self, briefs: list[Brief]) -> FeatureBatch: ...
