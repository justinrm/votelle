"""Auditable rights profiles. A license string never grants permission."""

from __future__ import annotations

from pathlib import Path

from music_pref.audio.prepare import file_sha256
from music_pref.data.paths import resolve_under_root
from music_pref.schemas import (
    Asset,
    Brief,
    Judgment,
    MusicPrefError,
    Permission,
    RightsRecord,
    ValidationIssue,
    error,
)

USES = (
    "research_training",
    "commercial_training",
    "audio_release",
    "embedding_release",
    "checkpoint_release",
)


def check_rights(
    root: Path,
    rights: list[RightsRecord],
    assets: list[Asset],
    briefs: list[Brief],
    judgments: list[Judgment],
    policy: str,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    known = {record.rights_record_id for record in rights}
    referenced: set[str] = set()
    for asset in assets:
        referenced.add(asset.rights_record_id)
    for brief in briefs:
        referenced.add(brief.rights_record_id)
    for judgment in judgments:
        referenced.add(judgment.label_rights_record_id)
    for rights_id in sorted(referenced - known):
        issues.append(
            error(
                rights_id,
                "rights_record_id",
                "missing_rights",
                "Add a rights record with explicit permissions. Unknown is not a grant.",
            )
        )
    for record in rights:
        issues.extend(_check_record(root, record, policy))
    return issues


def _check_record(root: Path, record: RightsRecord, policy: str) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if not record.components:
        issues.append(
            error(
                record.rights_record_id,
                "components",
                "missing_component_scope",
                "List the components this record covers, such as recording or labels.",
            )
        )
    if record.evidence_path:
        try:
            path = resolve_under_root(root, record.evidence_path)
        except MusicPrefError as exc:
            issues.append(error(record.rights_record_id, "evidence_path", exc.code, exc.remediation))
        else:
            if not path.is_file():
                issues.append(
                    error(
                        record.rights_record_id,
                        "evidence_path",
                        "missing_evidence",
                        "The evidence file is missing. Do not infer permission from a license name.",
                    )
                )
            elif file_sha256(path) != record.evidence_sha256:
                issues.append(
                    error(
                        record.rights_record_id,
                        "evidence_sha256",
                        "hash_mismatch",
                        "The evidence file does not match the recorded hash.",
                    )
                )
    fields = USES if policy == "commercial_ready" else ("research_training",)
    for field in fields:
        permission: Permission = getattr(record, field)
        if permission == "allowed":
            continue
        code = "permission_unknown" if permission == "unknown" else "permission_denied"
        issues.append(
            error(
                record.rights_record_id,
                field,
                code,
                f"{field} is {permission}. That blocks this use. A license name does not grant it.",
            )
        )
    return issues
