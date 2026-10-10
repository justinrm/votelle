"""Original-signal diagnostics. These are measurements, not preference scores."""

from __future__ import annotations

import numpy as np

SILENCE_PEAK = 1e-8
CLIP_PEAK = 0.999


def is_digital_silence(excerpt: np.ndarray) -> bool:
    if excerpt.size == 0:
        return True
    return float(np.max(np.abs(excerpt))) < SILENCE_PEAK


def measure_crop(excerpt: np.ndarray, sample_rate: int) -> list[dict]:
    peak = float(np.max(np.abs(excerpt))) if excerpt.size else 0.0
    rms = float(np.sqrt(np.mean(np.square(excerpt)))) if excerpt.size else 0.0
    duration = (excerpt.shape[0] / sample_rate) if sample_rate else 0.0
    rows = (
        ("duration", duration, "s", "duration_samples_over_rate_v1"),
        ("sample_rate", sample_rate, "Hz", "container_sample_rate_v1"),
        ("peak_amplitude", peak, "1", "peak_abs_v1"),
        ("clipping", peak >= CLIP_PEAK, "bool", "peak_threshold_0.999_v1"),
        ("rms", rms, "1", "rms_v1"),
        ("digital_silence", peak < SILENCE_PEAK, "bool", "peak_below_1e-8_v1"),
    )
    return [
        {"metric": metric, "value": value, "unit": unit, "method_id": method_id, "kind": "measured"}
        for metric, value, unit, method_id in rows
    ]
