"""Versioned manifest, config, and report types for protocol 0.1."""

from __future__ import annotations

import hashlib
import json
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

SCHEMA_VERSION = "0.1"
Permission = Literal["allowed", "denied", "unknown"]
ComponentKind = Literal["recording", "composition", "lyrics", "prompt", "labels"]
Choice = Literal["A", "B", "tie", "cannot_judge"]
Acceptability = Literal["yes", "no", "unsure"]


def canonical_bytes(payload: object) -> bytes:
    text = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return (text + "\n").encode("utf-8")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class MusicPrefError(Exception):
    def __init__(self, code: str, remediation: str, *, record_id: str | None = None, field: str = ""):
        super().__init__(f"{code}: {remediation}")
        self.code = code
        self.remediation = remediation
        self.record_id = record_id
        self.field = field


class ValidationIssue(BaseModel):
    model_config = ConfigDict(extra="forbid")

    severity: Literal["error", "warning"]
    record_id: str | None
    field: str
    code: str
    remediation: str


class ValidationReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["0.1"] = SCHEMA_VERSION
    policy: str
    provenance: str
    issues: list[ValidationIssue]

    def has_errors(self) -> bool:
        return any(item.severity == "error" for item in self.issues)


def error(record_id: str | None, field: str, code: str, remediation: str) -> ValidationIssue:
    return ValidationIssue(
        severity="error",
        record_id=record_id,
        field=field,
        code=code,
        remediation=remediation,
    )


class GeneratorInfo(BaseModel):
    model_config = ConfigDict(extra="forbid")

    model_id: str
    revision: str
    seed: int | None = None
    settings_hash: str | None = None
    component_license_evidence: str | None = None


class RightsRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["0.1"]
    rights_record_id: str = Field(min_length=1)
    rightsholder: str = Field(min_length=1)
    evidence_path: str | None = None
    evidence_url: str | None = None
    evidence_sha256: str = Field(min_length=64, max_length=64)
    recorded_at: str = Field(min_length=1)
    license_identifier: str | None = None
    components: list[ComponentKind] = Field(min_length=1)
    attribution: str | None = None
    exceptions: str | None = None
    research_training: Permission
    commercial_training: Permission
    audio_release: Permission
    embedding_release: Permission
    checkpoint_release: Permission
    review_status: str = Field(min_length=1)
    review_rationale: str = Field(min_length=1)

    @model_validator(mode="after")
    def evidence_present(self) -> RightsRecord:
        if not self.evidence_path and not self.evidence_url:
            raise ValueError("evidence_path or evidence_url is required")
        return self


class Asset(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["0.1"]
    asset_id: str = Field(min_length=1)
    relative_path: str = Field(min_length=1)
    sha256_original: str = Field(min_length=64, max_length=64)
    sha256_pcm: str = Field(min_length=64, max_length=64)
    source_recording_id: str = Field(min_length=1)
    song_family_id: str = Field(min_length=1)
    artist_id: str | None = None
    contributor_id: str | None = None
    origin_type: Literal["original", "contribution", "generated", "public_dataset", "test_fixture"]
    source_uri: str | None = None
    acquired_at: str = Field(min_length=1)
    source_revision: str | None = None
    generator: GeneratorInfo | None = None
    sample_rate: int = Field(gt=0)
    channels: int = Field(gt=0)
    duration_seconds: float = Field(gt=0)
    rights_record_id: str = Field(min_length=1)
    parent_asset_ids: list[str] = Field(default_factory=list)


class Brief(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["0.1"]
    brief_id: str = Field(min_length=1)
    brief_family_id: str = Field(min_length=1)
    text: str = Field(min_length=1)
    language: str = Field(min_length=1)
    audible_clauses: list[str] = Field(default_factory=list)
    intended_scope: str = Field(min_length=1)
    rights_record_id: str = Field(min_length=1)
    content_sha256: str = Field(min_length=64, max_length=64)


class Clip(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["0.1"]
    clip_id: str = Field(min_length=1)
    asset_id: str = Field(min_length=1)
    start_seconds: float = Field(ge=0)
    end_seconds: float = Field(gt=0)
    audition_condition: str = Field(min_length=1)


class Judgment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["0.1"]
    judgment_id: str = Field(min_length=1)
    pair_id: str = Field(min_length=1)
    session_id: str = Field(min_length=1)
    brief_id: str = Field(min_length=1)
    clip_a_id: str = Field(min_length=1)
    clip_b_id: str = Field(min_length=1)
    listener_id: str = Field(min_length=1)
    timestamp: str = Field(min_length=1)
    presentation_order: Literal["AB", "BA"]
    adherence_choice: Choice | None = None
    preference_choice: Choice | None = None
    acceptable_a: Acceptability | None = None
    acceptable_b: Acceptability | None = None
    confidence: float | None = None
    reason_codes: list[str] = Field(default_factory=list)
    notes: str | None = None
    listened_seconds_a: float | None = None
    listened_seconds_b: float | None = None
    is_repeat_of: str | None = None
    label_source: Literal["human", "teacher", "synthetic_rule"]
    label_rights_record_id: str = Field(min_length=1)


class SplitFractions(BaseModel):
    model_config = ConfigDict(extra="forbid")

    train: float
    validation: float
    calibration: float
    test: float

    @model_validator(mode="after")
    def sums_to_one(self) -> SplitFractions:
        values = (self.train, self.validation, self.calibration, self.test)
        if any(value < 0 for value in values):
            raise ValueError("split fractions must be non-negative")
        if abs(sum(values) - 1.0) > 1e-6:
            raise ValueError("split fractions must sum to 1")
        return self


class AudioConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    excerpt_seconds: float
    sample_rate: int
    channels: int
    normalization_profile: Literal["none_fixture_only", "gain_lufs_v1"]

    @model_validator(mode="after")
    def locked_excerpt(self) -> AudioConfig:
        if self.excerpt_seconds != 10 or self.sample_rate != 48000 or self.channels != 1:
            raise ValueError("v0.1 audio config is 10 seconds, 48000 Hz, mono output")
        return self


class EncoderConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1)
    revision: str = Field(min_length=1)


class FoundationConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["0.1"]
    dataset_root: str = Field(min_length=1)
    rights_policy: Literal["commercial_ready", "research_only"]
    target: Literal["adherence", "personal_preference"]
    seed: int
    split_fractions: SplitFractions
    audio: AudioConfig
    encoder: EncoderConfig
    network_access: bool
    level_matched: bool


class EncoderSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    revision: str
    dimension: int
    production_claim_allowed: bool
    processor_hash: str
    pooling: str
    dtype: str
