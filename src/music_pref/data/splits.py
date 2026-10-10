"""Seeded whole-component splits. Connected records are never divided."""

from __future__ import annotations

import os
import random
from pathlib import Path

from music_pref.data.identity import Component, connected_components
from music_pref.data.manifest import Dataset, dataset_root, load_dataset, validate
from music_pref.schemas import FoundationConfig, MusicPrefError, SplitFractions, canonical_bytes, sha256_hex

SPLIT_ORDER = ("train", "validation", "calibration", "test")
GROUPING_POLICY = "component_v1"


class SplitError(MusicPrefError):
    pass


def assign_components(components: list[Component], fractions: SplitFractions, seed: int) -> dict[str, list[Component]]:
    named = {name: getattr(fractions, name) for name in SPLIT_ORDER}
    positive = [name for name in SPLIT_ORDER if named[name] > 0]
    if not positive:
        raise SplitError("insufficient_groups", "At least one split fraction must be positive.")
    total = sum(component.weight for component in components)
    max_fraction = max(named[name] for name in positive)
    if any((component.weight - max_fraction * total) > 1e-6 for component in components):
        raise SplitError(
            "unsplittable_component",
            "A connected component is larger than the largest split. Do not split it.",
        )
    if len(components) < len(positive):
        raise SplitError(
            "insufficient_groups",
            "Not enough independent components for the requested splits.",
        )
    ordered = sorted(components, key=lambda component: component.component_id)
    random.Random(seed).shuffle(ordered)
    buckets: dict[str, list[Component]] = {name: [] for name in positive}
    weight = {name: 0 for name in positive}
    targets = {name: named[name] * total for name in positive}
    for component in ordered:
        choice = min(
            positive,
            key=lambda name: (-(targets[name] - weight[name]), -named[name], SPLIT_ORDER.index(name)),
        )
        buckets[choice].append(component)
        weight[choice] += component.weight
    if any(len(buckets[name]) == 0 for name in positive):
        raise SplitError(
            "insufficient_groups",
            "Assignment left a split empty. Refusing to break a component to fill it.",
        )
    return buckets


def build_split(dataset: Dataset, config: FoundationConfig) -> dict:
    components = connected_components(dataset.assets, dataset.briefs, dataset.clips, dataset.judgments)
    buckets = assign_components(components, config.split_fractions, config.seed)
    body = {
        "components": [
            {
                "asset_ids": list(component.asset_ids),
                "brief_ids": list(component.brief_ids),
                "component_id": component.component_id,
                "judgment_ids": list(component.judgment_ids),
                "song_family_ids": list(component.song_family_ids),
                "weight": component.weight,
            }
            for component in sorted(components, key=lambda component: component.component_id)
        ],
        "excluded": [],
        "grouping_policy": GROUPING_POLICY,
        "manifest_sha256": dict(sorted(dataset.manifest_sha256.items())),
        "schema_version": "0.1",
        "seed": config.seed,
        "split_version": GROUPING_POLICY,
        "splits": {name: sorted(component.component_id for component in buckets[name]) for name in buckets},
    }
    body["split_sha256"] = sha256_hex(canonical_bytes(body))
    return body


def write_split(config: FoundationConfig, output: Path) -> dict:
    report = validate(config)
    if report.has_errors():
        raise SplitError("validation_failed", "Fix validation errors before splitting.")
    dataset, issues = load_dataset(dataset_root(config))
    if issues:
        raise SplitError("validation_failed", "Fix validation errors before splitting.")
    artifact = build_split(dataset, config)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + ".tmp")
    temporary.write_bytes(canonical_bytes(artifact))
    os.replace(temporary, output)
    return artifact
