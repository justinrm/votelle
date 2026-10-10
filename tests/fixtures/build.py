"""Build generated-tone fixtures. These files are not music or preference labels."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import soundfile as sf

from music_pref.audio.prepare import file_sha256, pcm_hash, read_audio
from music_pref.data.manifest import brief_content_hash, canonical_pair_id
from music_pref.schemas import SCHEMA_VERSION, Asset, Brief, Clip, Judgment, RightsRecord

DECLARATION = Path(__file__).with_name("FIRST_PARTY_DECLARATION.md")


def _hex(value: int) -> str:
    return f"{value:064x}"


def make_rights(rights_id: str, evidence_sha256: str, mode: str = "allowed", components: list[str] | None = None) -> RightsRecord:
    def permission(field: str) -> str:
        if mode == "unknown_research" and field == "research_training":
            return "unknown"
        if mode == "unknown_audio" and field == "audio_release":
            return "unknown"
        if mode == "denied_audio" and field == "audio_release":
            return "denied"
        if mode == "denied_research" and field == "research_training":
            return "denied"
        return "allowed"

    return RightsRecord.model_validate(
        {
            "schema_version": SCHEMA_VERSION,
            "rights_record_id": rights_id,
            "rightsholder": "first-party-test",
            "evidence_path": "FIRST_PARTY_DECLARATION.md",
            "evidence_url": None,
            "evidence_sha256": evidence_sha256,
            "recorded_at": "2026-10-09T00:00:00Z",
            "license_identifier": "CC-BY-4.0" if mode == "unknown_research" else "first-party-declaration",
            "components": components or ["recording"],
            "attribution": None,
            "exceptions": None,
            "research_training": permission("research_training"),
            "commercial_training": permission("commercial_training"),
            "audio_release": permission("audio_release"),
            "embedding_release": permission("embedding_release"),
            "checkpoint_release": permission("checkpoint_release"),
            "review_status": "recorded",
            "review_rationale": "Generated test signal. Not music and not a human preference label.",
        }
    )


def make_asset(index: int = 1, **overrides) -> Asset:
    raw = {
        "schema_version": SCHEMA_VERSION,
        "asset_id": f"asset-{index}",
        "relative_path": f"audio/asset-{index}.wav",
        "sha256_original": _hex(index + 1),
        "sha256_pcm": _hex(index + 100_000),
        "source_recording_id": f"recording-{index}",
        "song_family_id": f"family-{index}",
        "artist_id": None,
        "contributor_id": None,
        "origin_type": "test_fixture",
        "source_uri": None,
        "acquired_at": "2026-10-09T00:00:00Z",
        "source_revision": None,
        "generator": None,
        "sample_rate": 48000,
        "channels": 1,
        "duration_seconds": 10.0,
        "rights_record_id": f"rights-{index}",
        "parent_asset_ids": [],
    }
    raw.update(overrides)
    return Asset.model_validate(raw)


def make_brief(index: int = 1, **overrides) -> Brief:
    text = overrides.pop("text", f"quiet test tone {index}")
    raw = {
        "schema_version": SCHEMA_VERSION,
        "brief_id": f"brief-{index}",
        "brief_family_id": f"brief-family-{index}",
        "text": text,
        "language": "en",
        "audible_clauses": [],
        "intended_scope": "10s_excerpt",
        "rights_record_id": "rights-brief",
        "content_sha256": brief_content_hash(text),
    }
    raw.update(overrides)
    return Brief.model_validate(raw)


def make_clip(index: int = 1, **overrides) -> Clip:
    raw = {
        "schema_version": SCHEMA_VERSION,
        "clip_id": f"clip-{index}",
        "asset_id": f"asset-{index}",
        "start_seconds": 0.0,
        "end_seconds": 10.0,
        "audition_condition": "none_fixture_only",
    }
    raw.update(overrides)
    return Clip.model_validate(raw)


def make_judgment(index: int = 1, **overrides) -> Judgment:
    clip_a = overrides.get("clip_a_id", f"clip-{index}")
    clip_b = overrides.get("clip_b_id", f"clip-{index + 1}")
    raw = {
        "schema_version": SCHEMA_VERSION,
        "judgment_id": f"judgment-{index}",
        "pair_id": canonical_pair_id(clip_a, clip_b),
        "session_id": "fixture-session",
        "brief_id": f"brief-{index}",
        "clip_a_id": clip_a,
        "clip_b_id": clip_b,
        "listener_id": "fixture-listener",
        "timestamp": "2026-10-09T00:00:00Z",
        "presentation_order": "AB",
        "adherence_choice": "A",
        "preference_choice": "B",
        "acceptable_a": "yes",
        "acceptable_b": "no",
        "confidence": None,
        "reason_codes": [],
        "notes": None,
        "listened_seconds_a": None,
        "listened_seconds_b": None,
        "is_repeat_of": None,
        "label_source": "synthetic_rule",
        "label_rights_record_id": "rights-label",
    }
    raw.update(overrides)
    raw["pair_id"] = overrides.get("pair_id", canonical_pair_id(raw["clip_a_id"], raw["clip_b_id"]))
    return Judgment.model_validate(raw)


def dump_jsonl(path: Path, records: list) -> None:
    lines = [json.dumps(record.model_dump(mode="json"), sort_keys=True) for record in records]
    path.write_text(("\n".join(lines) + "\n") if lines else "", encoding="utf-8")


def foundation_config(dataset_root: Path, **overrides) -> dict:
    config = {
        "schema_version": "0.1",
        "dataset_root": str(dataset_root),
        "rights_policy": "commercial_ready",
        "target": "adherence",
        "seed": 17,
        "split_fractions": {"train": 0.6, "validation": 0.1, "calibration": 0.1, "test": 0.2},
        "audio": {
            "excerpt_seconds": 10,
            "sample_rate": 48000,
            "channels": 1,
            "normalization_profile": "none_fixture_only",
        },
        "encoder": {"name": "dummy", "revision": "fixture-v1"},
        "network_access": False,
        "level_matched": False,
    }
    config.update(overrides)
    return config


def write_config(path: Path, dataset_root: Path, **overrides) -> Path:
    path.write_text(json.dumps(foundation_config(dataset_root, **overrides), indent=2) + "\n", encoding="utf-8")
    return path


def _tone(rate: int, seconds: float, frequency: float, silent: bool) -> np.ndarray:
    count = int(round(seconds * rate))
    if silent:
        return np.zeros(count, dtype=np.float64)
    time = np.arange(count) / rate
    return (0.2 * np.sin(2 * np.pi * frequency * time)).astype(np.float64)


def build_dataset(
    dest: Path,
    *,
    families: int = 20,
    link: str = "none",
    rights_mode: str = "allowed",
    rate: int = 48000,
    silent: bool = False,
    stereo: bool = False,
    audio_format: str = "wav",
) -> Path:
    dest.mkdir(parents=True, exist_ok=True)
    declaration = dest / "FIRST_PARTY_DECLARATION.md"
    declaration.write_text(DECLARATION.read_text(encoding="utf-8"), encoding="utf-8")
    evidence_hash = file_sha256(declaration)
    count = 2 if link == "pair" else families
    audio_dir = dest / "audio"
    audio_dir.mkdir(exist_ok=True)
    assets: list[Asset] = []
    clips: list[Clip] = []
    shared_family = "shared-family" if link in {"shared_family", "pair"} else None
    extension = "flac" if audio_format == "flac" else "wav"
    subtype = "PCM_16"
    written: list[Path] = []
    for index in range(count):
        samples = _tone(rate, 10.0, 110 + (index + 1) * 25, silent)
        if stereo:
            samples = np.column_stack([samples, samples * 0.5])
        path = audio_dir / f"asset-{index}.{extension}"
        sf.write(path, samples, rate, subtype=subtype)
        written.append(path)
    if link == "duplicate_pcm" and len(written) > 1:
        written[1].write_bytes(written[0].read_bytes())
    for index, path in enumerate(written):
        decoded, sample_rate = read_audio(path)
        parent_ids = ["asset-0"] if link == "parent_link" and index == 1 else []
        assets.append(
            make_asset(
                index,
                relative_path=f"audio/{path.name}",
                sha256_original=file_sha256(path),
                sha256_pcm=pcm_hash(decoded),
                sample_rate=sample_rate,
                channels=int(decoded.shape[1]),
                duration_seconds=decoded.shape[0] / sample_rate,
                song_family_id=shared_family or f"family-{index}",
                parent_asset_ids=parent_ids,
                rights_record_id=f"rights-{index}",
            )
        )
        clips.append(make_clip(index, asset_id=f"asset-{index}"))
    rights = [] if rights_mode == "omit" else [make_rights(f"rights-{index}", evidence_hash, rights_mode) for index in range(count)]
    briefs: list[Brief] = []
    judgments: list[Judgment] = []
    if link in {"pair", "chain", "compare_pair"}:
        rights.append(make_rights("rights-brief", evidence_hash, rights_mode, ["prompt"]))
        rights.append(make_rights("rights-label", evidence_hash, rights_mode, ["labels"]))
    if link == "pair":
        briefs.append(make_brief(0))
        judgments.append(make_judgment(0, clip_a_id="clip-0", clip_b_id="clip-1", brief_id="brief-0"))
    elif link == "compare_pair":
        briefs.append(make_brief(0))
        judgments.append(make_judgment(0, clip_a_id="clip-0", clip_b_id="clip-1", brief_id="brief-0"))
    elif link == "chain":
        for index in range(count - 1):
            briefs.append(make_brief(index))
            judgments.append(
                make_judgment(index, clip_a_id=f"clip-{index}", clip_b_id=f"clip-{index + 1}", brief_id=f"brief-{index}")
            )
    dump_jsonl(dest / "assets.jsonl", assets)
    dump_jsonl(dest / "rights.jsonl", rights)
    dump_jsonl(dest / "briefs.jsonl", briefs)
    dump_jsonl(dest / "clips.jsonl", clips)
    dump_jsonl(dest / "judgments.jsonl", judgments)
    return dest


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Write a generated-tone fixture dataset.")
    parser.add_argument("--dest", type=Path, required=True)
    parser.add_argument("--families", type=int, default=20)
    args = parser.parse_args()
    build_dataset(args.dest, families=args.families)
    print(args.dest)


if __name__ == "__main__":
    main()
