"""JSONL loading, referential integrity, and judgment orientation."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from pydantic import BaseModel, ValidationError

from music_pref.audio.measure import is_digital_silence
from music_pref.audio.prepare import crop_samples, file_sha256, pcm_hash, prepare_excerpt, read_audio
from music_pref.data.paths import resolve_under_root
from music_pref.data.rights import check_rights
from music_pref.schemas import (
    SCHEMA_VERSION,
    Asset,
    Brief,
    Clip,
    FoundationConfig,
    Judgment,
    MusicPrefError,
    ValidationIssue,
    ValidationReport,
    canonical_bytes,
    error,
    sha256_hex,
)

ID_FIELDS = ("asset_id", "rights_record_id", "brief_id", "clip_id", "judgment_id")


@dataclass
class OrientedJudgment:
    clip_a_id: str
    clip_b_id: str
    adherence_choice: str | None
    preference_choice: str | None
    acceptable_a: str | None
    acceptable_b: str | None
    presentation_order: str


@dataclass
class Dataset:
    root: Path
    assets: list[Asset]
    rights: list
    briefs: list[Brief]
    clips: list[Clip]
    judgments: list[Judgment]
    manifest_sha256: dict[str, str]


def canonical_pair_id(clip_a_id: str, clip_b_id: str) -> str:
    left, right = sorted((clip_a_id, clip_b_id))
    return f"{left}::{right}"


def brief_content_hash(text: str) -> str:
    return sha256_hex(text.encode("utf-8"))


def _flip_choice(value: str | None) -> str | None:
    return {"A": "B", "B": "A"}.get(value, value)


def orient_judgment(judgment: Judgment) -> OrientedJudgment:
    left, right = sorted((judgment.clip_a_id, judgment.clip_b_id))
    flipped = judgment.clip_a_id != left
    if flipped:
        adherence = _flip_choice(judgment.adherence_choice)
        preference = _flip_choice(judgment.preference_choice)
        acceptable_a = judgment.acceptable_b
        acceptable_b = judgment.acceptable_a
    else:
        adherence = judgment.adherence_choice
        preference = judgment.preference_choice
        acceptable_a = judgment.acceptable_a
        acceptable_b = judgment.acceptable_b
    return OrientedJudgment(
        clip_a_id=left,
        clip_b_id=right,
        adherence_choice=adherence,
        preference_choice=preference,
        acceptable_a=acceptable_a,
        acceptable_b=acceptable_b,
        presentation_order=judgment.presentation_order,
    )


def load_config(path: Path) -> FoundationConfig:
    return FoundationConfig.model_validate(json.loads(path.read_text(encoding="utf-8")))


def dataset_root(config: FoundationConfig) -> Path:
    root = Path(config.dataset_root)
    if not root.is_absolute():
        root = Path.cwd() / root
    return root.resolve()


def _issue_from_validation(record_id: str | None, exc: ValidationError) -> ValidationIssue:
    detail = exc.errors()[0] if exc.errors() else {}
    loc = detail.get("loc", ())
    field = ".".join(str(part) for part in loc)
    message = str(detail.get("msg", exc))
    code = "schema_invalid"
    if "schema_version" in field:
        code = "schema_version"
    elif "components" in field:
        code = "missing_component_scope"
    elif "evidence" in field:
        code = "missing_evidence"
    return error(record_id, field or "record", code, message)


def load_jsonl(path: Path, model: type[BaseModel]) -> tuple[list, list[ValidationIssue]]:
    records: list = []
    issues: list[ValidationIssue] = []
    if not path.is_file():
        issues.append(error(None, path.name, "missing_reference", f"Create {path.name} under the dataset root."))
        return records, issues
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            raw = json.loads(line)
        except json.JSONDecodeError:
            issues.append(error(f"line:{line_no}", path.name, "schema_invalid", "The line is not valid JSON."))
            continue
        if not isinstance(raw, dict):
            issues.append(error(f"line:{line_no}", path.name, "schema_invalid", "Each JSONL line must be an object."))
            continue
        record_id = next((str(raw[key]) for key in ID_FIELDS if raw.get(key)), f"line:{line_no}")
        try:
            records.append(model.model_validate(raw))
        except ValidationError as exc:
            issues.append(_issue_from_validation(record_id, exc))
    return records, issues


def _duplicate_issues(records: list, id_fn, field: str) -> list[ValidationIssue]:
    seen: set[str] = set()
    issues: list[ValidationIssue] = []
    for record in records:
        ident = id_fn(record)
        if ident in seen:
            issues.append(error(ident, field, "duplicate_id", "IDs must be unique inside each manifest."))
        seen.add(ident)
    return issues


def load_dataset(root: Path) -> tuple[Dataset, list[ValidationIssue]]:
    from music_pref.schemas import RightsRecord

    issues: list[ValidationIssue] = []
    loaded: dict[str, list] = {}
    hashes: dict[str, str] = {}
    models = {
        "assets": Asset,
        "rights": RightsRecord,
        "briefs": Brief,
        "clips": Clip,
        "judgments": Judgment,
    }
    for name, model in models.items():
        path = root / f"{name}.jsonl"
        records, record_issues = load_jsonl(path, model)
        issues.extend(record_issues)
        loaded[name] = records
        if path.is_file():
            hashes[name] = sha256_hex(path.read_bytes())
    issues.extend(_duplicate_issues(loaded["assets"], lambda row: row.asset_id, "asset_id"))
    issues.extend(_duplicate_issues(loaded["rights"], lambda row: row.rights_record_id, "rights_record_id"))
    issues.extend(_duplicate_issues(loaded["briefs"], lambda row: row.brief_id, "brief_id"))
    issues.extend(_duplicate_issues(loaded["clips"], lambda row: row.clip_id, "clip_id"))
    issues.extend(_duplicate_issues(loaded["judgments"], lambda row: row.judgment_id, "judgment_id"))
    dataset = Dataset(
        root=root,
        assets=loaded["assets"],
        rights=loaded["rights"],
        briefs=loaded["briefs"],
        clips=loaded["clips"],
        judgments=loaded["judgments"],
        manifest_sha256=hashes,
    )
    return dataset, issues


def check_references(dataset: Dataset, config: FoundationConfig) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    assets = {asset.asset_id: asset for asset in dataset.assets}
    briefs = {brief.brief_id: brief for brief in dataset.briefs}
    clips = {clip.clip_id: clip for clip in dataset.clips}
    judgments = {judgment.judgment_id for judgment in dataset.judgments}
    for asset in dataset.assets:
        for parent_id in asset.parent_asset_ids:
            if parent_id not in assets:
                issues.append(
                    error(asset.asset_id, "parent_asset_ids", "missing_reference", "Parent asset is not in assets.jsonl.")
                )
    for brief in dataset.briefs:
        if brief.content_sha256 != brief_content_hash(brief.text):
            issues.append(
                error(brief.brief_id, "content_sha256", "hash_mismatch", "Brief content hash does not match the text.")
            )
    for clip in dataset.clips:
        asset = assets.get(clip.asset_id)
        if asset is None:
            issues.append(error(clip.clip_id, "asset_id", "missing_reference", "Clip asset_id is not in assets.jsonl."))
            continue
        if clip.audition_condition != config.audio.normalization_profile:
            issues.append(
                error(
                    clip.clip_id,
                    "audition_condition",
                    "normalization_profile_rejected",
                    "Clip audition_condition must match the config normalization profile.",
                )
            )
        if clip.end_seconds <= clip.start_seconds:
            issues.append(error(clip.clip_id, "end_seconds", "bad_bounds", "end_seconds must be greater than start_seconds."))
        elif abs((clip.end_seconds - clip.start_seconds) - 10.0) > 0.001:
            issues.append(
                error(
                    clip.clip_id,
                    "end_seconds",
                    "duration_not_ten_seconds",
                    "v0.1 clips must be 10 seconds within 1 ms. Do not pad or trim.",
                )
            )
    for judgment in dataset.judgments:
        if judgment.clip_a_id == judgment.clip_b_id:
            issues.append(error(judgment.judgment_id, "clip_b_id", "invalid_pair", "A comparison needs two distinct clips."))
        if judgment.clip_a_id not in clips or judgment.clip_b_id not in clips:
            issues.append(error(judgment.judgment_id, "clip_a_id", "missing_reference", "Judgment clips must exist."))
        if judgment.brief_id not in briefs:
            issues.append(error(judgment.judgment_id, "brief_id", "missing_reference", "Judgment brief_id must exist."))
        if judgment.pair_id != canonical_pair_id(judgment.clip_a_id, judgment.clip_b_id):
            issues.append(
                error(
                    judgment.judgment_id,
                    "pair_id",
                    "invalid_pair",
                    "pair_id must be the unordered pair of clip ids, lower then higher, joined by '::'.",
                )
            )
        if judgment.is_repeat_of and judgment.is_repeat_of not in judgments:
            issues.append(
                error(judgment.judgment_id, "is_repeat_of", "missing_reference", "Repeat judgments must point at an existing judgment.")
            )
    return issues


def check_media(dataset: Dataset, config: FoundationConfig) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    decoded: dict[str, tuple | None] = {}
    for asset in dataset.assets:
        try:
            path = resolve_under_root(dataset.root, asset.relative_path)
        except MusicPrefError as exc:
            issues.append(error(asset.asset_id, exc.field, exc.code, exc.remediation))
            decoded[asset.asset_id] = None
            continue
        if not path.is_file():
            issues.append(error(asset.asset_id, "relative_path", "missing_reference", "Asset audio file is missing."))
            decoded[asset.asset_id] = None
            continue
        try:
            data, sample_rate = read_audio(path)
        except MusicPrefError as exc:
            issues.append(error(asset.asset_id, exc.field, exc.code, exc.remediation))
            decoded[asset.asset_id] = None
            continue
        decoded[asset.asset_id] = (data, sample_rate)
        if file_sha256(path) != asset.sha256_original or pcm_hash(data) != asset.sha256_pcm:
            issues.append(
                error(asset.asset_id, "sha256_original", "hash_mismatch", "File bytes or canonical PCM hash do not match.")
            )
        duration = data.shape[0] / sample_rate
        if sample_rate != asset.sample_rate or data.shape[1] != asset.channels or abs(duration - asset.duration_seconds) > 0.001:
            issues.append(
                error(
                    asset.asset_id,
                    "duration_seconds",
                    "source_mismatch",
                    "Declared sample rate, channels, or duration do not match the decoded file.",
                )
            )
    assets = {asset.asset_id: asset for asset in dataset.assets}
    for clip in dataset.clips:
        loaded = decoded.get(clip.asset_id)
        if not loaded:
            continue
        data, sample_rate = loaded
        try:
            excerpt = crop_samples(data, sample_rate, clip.start_seconds, clip.end_seconds)
        except MusicPrefError as exc:
            issues.append(error(clip.clip_id, exc.field, exc.code, exc.remediation))
            continue
        silent = is_digital_silence(excerpt)
        if silent:
            issues.append(
                error(
                    clip.clip_id,
                    "relative_path",
                    "digital_silence",
                    "Digital silence is invalid. This check does not score quiet music.",
                )
            )
        asset = assets[clip.asset_id]
        if clip.end_seconds > asset.duration_seconds + 0.001:
            issues.append(error(clip.clip_id, "end_seconds", "bad_bounds", "Clip extends past the declared asset duration."))
        if config.audio.normalization_profile == "gain_lufs_v1" and config.level_matched and not silent:
            try:
                prepared = prepare_excerpt(
                    data,
                    sample_rate,
                    clip.start_seconds,
                    clip.end_seconds,
                    config.audio.normalization_profile,
                    True,
                )
            except MusicPrefError as exc:
                issues.append(error(clip.clip_id, exc.field, exc.code, exc.remediation))
            else:
                if prepared.loudness_mismatch:
                    if prepared.gain_limited_by == "true_peak":
                        remediation = (
                            "True-peak ceiling prevented -20 LUFS. Exclude this clip from the primary "
                            "level-matched analysis or keep it in a separately identified condition."
                        )
                    else:
                        remediation = (
                            "Integrated loudness is outside 0.1 LU of -20 after one constant gain. "
                            "Exclude this clip from the primary level-matched analysis."
                        )
                    issues.append(
                        ValidationIssue(
                            severity="warning",
                            record_id=clip.clip_id,
                            field="audition_condition",
                            code="loudness_mismatch",
                            remediation=remediation,
                        )
                    )
    return issues


def validate(config: FoundationConfig) -> ValidationReport:
    issues: list[ValidationIssue] = []
    if config.schema_version != SCHEMA_VERSION:
        issues.append(error(None, "schema_version", "schema_version", "This foundation reads schema 0.1."))
    if config.network_access:
        issues.append(
            error(None, "network_access", "network_access_refused", "This foundation is offline. Set network_access to false.")
        )
    if config.encoder.name != "dummy" or config.encoder.revision != "fixture-v1":
        issues.append(
            error(
                None,
                "encoder",
                "encoder_unavailable",
                "This session only implements the dummy fixture encoder. It cannot support a production claim.",
            )
        )
    if config.level_matched != (config.audio.normalization_profile == "gain_lufs_v1"):
        issues.append(
            error(
                None,
                "normalization_profile",
                "normalization_profile_rejected",
                "level_matched requires gain_lufs_v1. none_fixture_only applies no loudness match.",
            )
        )
    root = dataset_root(config)
    if not root.is_dir():
        issues.append(error(None, "dataset_root", "missing_reference", "dataset_root does not exist."))
        return ValidationReport(policy=config.rights_policy, provenance=config.rights_policy, issues=issues)
    dataset, load_issues = load_dataset(root)
    issues.extend(load_issues)
    issues.extend(check_references(dataset, config))
    issues.extend(check_rights(root, dataset.rights, dataset.assets, dataset.briefs, dataset.judgments, config.rights_policy))
    issues.extend(check_media(dataset, config))
    return ValidationReport(policy=config.rights_policy, provenance=config.rights_policy, issues=issues)


def report_bytes(report: ValidationReport) -> bytes:
    return canonical_bytes(report.model_dump(mode="json"))
