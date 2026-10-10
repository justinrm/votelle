"""Deterministic fixture encoder. Not a musical embedding and not a production model."""

from __future__ import annotations

import hashlib

import numpy as np

from music_pref.audio.prepare import PreparedExcerpt
from music_pref.features.base import FeatureBatch, l2_normalize
from music_pref.schemas import Brief, EncoderSpec

DIMENSION = 512


def vector_from_digest(digest: bytes) -> np.ndarray:
    generator = np.random.Generator(np.random.PCG64(np.random.SeedSequence(list(digest))))
    return l2_normalize(generator.standard_normal(DIMENSION))


class DummyEncoder:
    def describe(self) -> EncoderSpec:
        return EncoderSpec(
            name="dummy",
            revision="fixture-v1",
            dimension=DIMENSION,
            production_claim_allowed=False,
            processor_hash="none",
            pooling="clip",
            dtype="float32",
        )

    def embed_audio(self, clips: list[PreparedExcerpt]) -> FeatureBatch:
        rows = [
            vector_from_digest(hashlib.sha256(np.ascontiguousarray(clip.samples, dtype=np.float32).tobytes()).digest())
            for clip in clips
        ]
        vectors = np.stack(rows) if rows else np.zeros((0, DIMENSION), dtype=np.float32)
        return FeatureBatch(vectors=vectors, spec=self.describe())

    def embed_text(self, briefs: list[Brief]) -> FeatureBatch:
        rows = [vector_from_digest(hashlib.sha256(brief.text.encode("utf-8")).digest()) for brief in briefs]
        vectors = np.stack(rows) if rows else np.zeros((0, DIMENSION), dtype=np.float32)
        return FeatureBatch(vectors=vectors, spec=self.describe())
