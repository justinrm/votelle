"""Local intake for the three P-01 Incompetech recordings.

Copies files the operator already has. Does not download, decode, assign
permissions, pick a crop, or judge musical suitability.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import soundfile as sf
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from votelle_music.audio.prepare import (
    GAIN_PROFILE,
    file_sha256,
    pcm_hash,
    prepare_excerpt,
    read_audio,
    waveform_for_encoder,
)
from votelle_music.data.manifest import dataset_root, load_dataset, load_jsonl
from votelle_music.data.paths import resolve_under_root
from votelle_music.schemas import (
    SCHEMA_VERSION,
    Asset,
    Clip,
    MusicPrefError,
    canonical_bytes,
    sha256_hex,
)

# Official individual files from the rights audit. Exact strings, not filenames.
P01_CATALOG = {
    "https://incompetech.com/music/royalty-free/mp3-royaltyfree/Disquiet.mp3": {
        "isrc": "USUAN1500036",
        "slug": "disquiet",
    },
    "https://incompetech.com/music/royalty-free/mp3-royaltyfree/Mesmerize.mp3": {
        "isrc": "USUAN1500005",
        "slug": "mesmerize",
    },
    "https://incompetech.com/music/royalty-free/mp3-royaltyfree/Colorless%20Aura.mp3": {
        "isrc": "USUAN1400008",
        "slug": "colorless-aura",
    },
}
ARTIST_ID = "kevin-macleod"
MANIFESTS = ("assets.jsonl", "rights.jsonl", "briefs.jsonl", "clips.jsonl", "judgments.jsonl")


class AcquisitionReceipt(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["0.1"] = SCHEMA_VERSION
    asset_id: str
    source_uri: str
    source_recording_id: str
    song_family_id: str
    raw_relative_path: str
    raw_sha256: str
    acquired_at: str
    decode_tool: str
    decode_version: str
    decode_command: str
    decoded_relative_path: str
    decoded_sha256: str
    format_name: str
    subtype: str
    sample_rate: int
    channels: int
    frames: int
    duration_seconds: float
    lossless_master: Literal[False] = False
    rights_record_id: str | None = None
    rights_gate: Literal["provisional_review", "reviewed_with_evidence"]
    in_manifest: bool
    release_clearance: Literal["not_assessed"] = "not_assessed"
    status_reason: str


class QCSidecar(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["0.1"] = SCHEMA_VERSION
    asset_id: str
    clip_id: str
    start_seconds: float
    end_seconds: float
    preprocessing_id: str
    preprocessing_sha256: str
    prepared_pcm_sha256: str
    gain_db: float
    integrated_lufs: float | None
    true_peak_dbtp: float | None
    loudness_mismatch: bool
    eligibility: Literal["primary_level_matched", "excluded_loudness_mismatch"]
    eligibility_reason: str
    prepared_relative_path: str


class FamilyReview(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["0.1"]
    review_status: str = Field(min_length=1)
    rationale: str = Field(min_length=1)
    same_song_family: list[list[str]] = Field(min_length=1)


@dataclass(frozen=True)
class IngestRequest:
    source_uri: str
    raw_path: Path
    decoded_path: Path
    acquired_at: str
    decode_tool: str
    decode_version: str
    decode_command: str
    rights_record_id: str | None = None
    family_review_path: Path | None = None


def _stable_id(prefix: str, payload: object) -> str:
    return f"{prefix}-{sha256_hex(canonical_bytes(payload))[:20]}"


def _looks_like_mp3(header: bytes) -> bool:
    # ponytail: ID3 or frame-sync sniff. Parse frames if a non-MP3 container ever uses this header.
    if header.startswith(b"ID3"):
        return True
    return len(header) >= 2 and header[0] == 0xFF and (header[1] & 0xE0) == 0xE0


def _require_text(value: str, field: str) -> str:
    if not value or not value.strip():
        raise MusicPrefError(
            "missing_provenance",
            f"{field} is required. It is recorded and is not executed.",
            field=field,
        )
    return value


def _rollback(created: list[Path], restores: list[tuple[Path, bytes]]) -> None:
    for path, previous in reversed(restores):
        path.write_bytes(previous)
    for path in reversed(created):
        if path.is_file():
            path.unlink()


def _run(work):
    created: list[Path] = []
    restores: list[tuple[Path, bytes]] = []
    try:
        return work(created, restores)
    except Exception as exc:
        _rollback(created, restores)
        if isinstance(exc, MusicPrefError):
            raise
        raise MusicPrefError(
            "ingest_failed",
            "Removed partial files. Fix the dataset path and retry.",
        ) from exc


def _write_new(path: Path, data: bytes, created: list[Path]) -> None:
    if path.exists():
        raise MusicPrefError(
            "already_exists",
            f"{path.name} already exists. Refusing to overwrite.",
            field="relative_path",
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    created.append(path)
    path.write_bytes(data)


def _ensure_manifest(root: Path, name: str, created: list[Path]) -> None:
    path = root / name
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    created.append(path)
    path.write_text("", encoding="utf-8")


def _append_model(path: Path, record: BaseModel, restores: list[tuple[Path, bytes]]) -> None:
    before = path.read_bytes()
    line = json.dumps(record.model_dump(mode="json"), sort_keys=True) + "\n"
    with path.open("a", encoding="utf-8") as handle:
        handle.write(line)
    restores.append((path, before))


def _load_receipts(root: Path) -> list[dict]:
    directory = root / "receipts"
    if not directory.is_dir():
        return []
    loaded: list[dict] = []
    for path in sorted(directory.glob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise MusicPrefError(
                "schema_invalid",
                f"{path.name} is not valid JSON. Fix or remove that receipt before ingesting.",
                field="receipts",
            ) from exc
        if not isinstance(payload, dict):
            raise MusicPrefError(
                "schema_invalid",
                f"{path.name} must be a JSON object. Fix or remove that receipt before ingesting.",
                field="receipts",
            )
        loaded.append(payload)
    return loaded


def _family_review(path: Path | None) -> FamilyReview | None:
    if path is None:
        return None
    if not path.is_file():
        raise MusicPrefError("invalid_source", "Family review file is missing.", field="song_family_id")
    try:
        return FamilyReview.model_validate(json.loads(path.read_text(encoding="utf-8")))
    except (json.JSONDecodeError, ValidationError) as exc:
        raise MusicPrefError("schema_invalid", "Family review file is invalid.", field="song_family_id") from exc


def _song_family_id(uri: str, review: FamilyReview | None) -> str:
    if review is None or review.review_status != "reviewed":
        return _stable_id("song", [uri])
    groups = [group for group in review.same_song_family if uri in group]
    if not groups:
        return _stable_id("song", [uri])
    if len(groups) > 1:
        raise MusicPrefError(
            "duplicate_id",
            "Source URI is in more than one song-family group.",
            field="song_family_id",
        )
    group = groups[0]
    if len(group) < 2 or len(set(group)) != len(group):
        raise MusicPrefError(
            "invalid_source",
            "A song-family group needs two distinct catalog recordings.",
            field="song_family_id",
        )
    if any(item not in P01_CATALOG for item in group):
        raise MusicPrefError(
            "invalid_source",
            "Song-family review contains a URI outside the P-01 catalog.",
            field="source_uri",
        )
    return _stable_id("song", sorted(group))


def _rights_gate(root: Path, rights_id: str | None) -> tuple[str, str]:
    if not rights_id:
        return "provisional_review", "No rights record supplied. Staged and ineligible."
    path = root / "rights.jsonl"
    if not path.is_file():
        return "provisional_review", "rights.jsonl has no reviewed record. Staged and ineligible."
    from votelle_music.schemas import RightsRecord

    records, issues = load_jsonl(path, RightsRecord)
    if issues:
        return "provisional_review", "Rights file is not a valid record. Staged and ineligible."
    match = next((row for row in records if row.rights_record_id == rights_id), None)
    if match is None:
        return "provisional_review", "Rights record id is absent. Staged and ineligible."
    if match.review_status != "reviewed":
        return "provisional_review", "review_status is not reviewed. Provisional review is not eligibility."
    if not match.evidence_path:
        return "provisional_review", "A local evidence file is required. A URL alone is not eligibility."
    try:
        evidence = resolve_under_root(root, match.evidence_path)
    except MusicPrefError:
        return "provisional_review", "Evidence path escapes the dataset root. Staged and ineligible."
    if not evidence.is_file() or file_sha256(evidence) != match.evidence_sha256:
        return "provisional_review", "Evidence file is missing or its hash does not match. Staged and ineligible."
    return (
        "reviewed_with_evidence",
        "Reviewed rights record with evidence. Ingestion did not assign permissions or release clearance.",
    )


def _reject_duplicates(asset_id, uri, recording_id, raw_sha, decoded_sha, pcm_sha, assets, receipts) -> None:
    for asset in assets:
        same_identity = asset.asset_id == asset_id or asset.source_uri == uri or asset.source_recording_id == recording_id
        same_bytes = asset.sha256_original == decoded_sha or asset.sha256_pcm == pcm_sha
        if same_identity or same_bytes:
            raise MusicPrefError(
                "duplicate_id",
                "That source, recording identity, or decoded PCM is already ingested.",
                record_id=asset.asset_id,
                field="asset_id",
            )
    for receipt in receipts:
        same_identity = (
            receipt.get("asset_id") == asset_id
            or receipt.get("source_uri") == uri
            or receipt.get("source_recording_id") == recording_id
        )
        same_bytes = receipt.get("raw_sha256") == raw_sha or receipt.get("decoded_sha256") == decoded_sha
        if same_identity or same_bytes:
            raise MusicPrefError(
                "duplicate_id",
                "That source, recording identity, or file hash is already in a receipt.",
                record_id=str(receipt.get("asset_id") or ""),
                field="asset_id",
            )


def ingest(config, request: IngestRequest) -> AcquisitionReceipt:
    entry = P01_CATALOG.get(request.source_uri)
    if entry is None:
        raise MusicPrefError(
            "invalid_source",
            "P-01 accepts only the three official Incompetech URIs. Nothing was downloaded.",
            field="source_uri",
        )
    raw = request.raw_path
    decoded = request.decoded_path
    if not raw.is_file() or not decoded.is_file():
        raise MusicPrefError(
            "invalid_source",
            "Raw and decoded files must already exist locally. This command does not download audio.",
            field="relative_path",
        )
    if raw.resolve() == decoded.resolve():
        raise MusicPrefError(
            "invalid_source",
            "Keep the MP3 and write the WAV or FLAC to a different file.",
            field="relative_path",
        )
    acquired_at = _require_text(request.acquired_at, "acquired_at")
    decode_tool = _require_text(request.decode_tool, "decode_tool")
    decode_version = _require_text(request.decode_version, "decode_version")
    decode_command = _require_text(request.decode_command, "decode_command")

    raw_bytes = raw.read_bytes()
    decoded_bytes = decoded.read_bytes()
    if not _looks_like_mp3(raw_bytes[:4]):
        raise MusicPrefError(
            "invalid_source",
            "The raw original for this pilot is the MP3 from the official URI.",
            field="relative_path",
        )
    suffix = decoded.suffix.lower()
    if _looks_like_mp3(decoded_bytes[:4]) or suffix == ".mp3":
        raise MusicPrefError(
            "lossy_source_mislabelled",
            "Refusing to treat an MP3 as WAV or FLAC. Decode to a new file and leave the MP3 unchanged.",
            field="relative_path",
        )
    if suffix not in {".wav", ".flac"}:
        raise MusicPrefError("invalid_source", "Decoded derivative must be WAV or FLAC.", field="relative_path")
    info = sf.info(decoded)
    audio, sample_rate = read_audio(decoded)
    if info.format not in {"WAV", "FLAC"} or info.frames != audio.shape[0] or info.samplerate != sample_rate:
        raise MusicPrefError(
            "source_mismatch",
            "Decoded format properties do not match the file soundfile read.",
            field="relative_path",
        )
    if info.channels != audio.shape[1]:
        raise MusicPrefError("source_mismatch", "Decoded channel count does not match.", field="relative_path")

    review = _family_review(request.family_review_path)
    asset_id = _stable_id("asset", {"source_uri": request.source_uri})
    recording_id = _stable_id("recording", request.source_uri)
    family_id = _song_family_id(request.source_uri, review)
    raw_sha = sha256_hex(raw_bytes)
    decoded_sha = sha256_hex(decoded_bytes)
    pcm_sha = pcm_hash(audio)
    root = dataset_root(config)
    gate, reason = _rights_gate(root, request.rights_record_id)
    existing_assets = []
    assets_path = root / "assets.jsonl"
    if assets_path.is_file():
        existing_assets, asset_issues = load_jsonl(assets_path, Asset)
        if asset_issues:
            raise MusicPrefError("schema_invalid", "assets.jsonl is invalid. Fix it before ingesting.", field="assets.jsonl")
    _reject_duplicates(
        asset_id,
        request.source_uri,
        recording_id,
        raw_sha,
        decoded_sha,
        pcm_sha,
        existing_assets,
        _load_receipts(root),
    )

    raw_rel = f"raw/{entry['slug']}.mp3"
    decoded_rel = f"decoded/{entry['slug']}{suffix}"
    receipt = AcquisitionReceipt(
        asset_id=asset_id,
        source_uri=request.source_uri,
        source_recording_id=recording_id,
        song_family_id=family_id,
        raw_relative_path=raw_rel,
        raw_sha256=raw_sha,
        acquired_at=acquired_at,
        decode_tool=decode_tool,
        decode_version=decode_version,
        decode_command=decode_command,
        decoded_relative_path=decoded_rel,
        decoded_sha256=decoded_sha,
        format_name=info.format,
        subtype=info.subtype,
        sample_rate=int(sample_rate),
        channels=int(audio.shape[1]),
        frames=int(audio.shape[0]),
        duration_seconds=audio.shape[0] / float(sample_rate),
        rights_record_id=request.rights_record_id,
        rights_gate=gate,
        in_manifest=gate == "reviewed_with_evidence",
        status_reason=reason,
    )

    def write(created: list[Path], restores: list[tuple[Path, bytes]]) -> AcquisitionReceipt:
        root.mkdir(parents=True, exist_ok=True)
        for name in MANIFESTS:
            _ensure_manifest(root, name, created)
        _write_new(resolve_under_root(root, raw_rel), raw_bytes, created)
        _write_new(resolve_under_root(root, decoded_rel), decoded_bytes, created)
        if file_sha256(raw) != raw_sha:
            raise MusicPrefError("hash_mismatch", "The raw MP3 changed while it was being copied.", field="relative_path")
        receipt_path = root / "receipts" / f"{asset_id}.json"
        _write_new(receipt_path, canonical_bytes(receipt.model_dump(mode="json")), created)
        if receipt.in_manifest:
            asset = Asset.model_validate(
                {
                    "schema_version": SCHEMA_VERSION,
                    "asset_id": asset_id,
                    "relative_path": decoded_rel,
                    "sha256_original": decoded_sha,
                    "sha256_pcm": pcm_sha,
                    "source_recording_id": recording_id,
                    "song_family_id": family_id,
                    "artist_id": ARTIST_ID,
                    "contributor_id": None,
                    "origin_type": "public_dataset",
                    "source_uri": request.source_uri,
                    "acquired_at": acquired_at,
                    "source_revision": entry["isrc"],
                    "generator": None,
                    "sample_rate": int(sample_rate),
                    "channels": int(audio.shape[1]),
                    "duration_seconds": audio.shape[0] / float(sample_rate),
                    "rights_record_id": request.rights_record_id,
                    "parent_asset_ids": [],
                }
            )
            _append_model(root / "assets.jsonl", asset, restores)
        return receipt

    return _run(write)


def prepare_clip(config, asset_id: str, clip_id: str, start_seconds: float, end_seconds: float) -> QCSidecar:
    if config.audio.normalization_profile != GAIN_PROFILE or not config.level_matched:
        raise MusicPrefError(
            "normalization_profile_rejected",
            "P-01 preparation uses gain_lufs_v1 with level_matched true.",
            field="normalization_profile",
        )
    if not clip_id.strip():
        raise MusicPrefError("invalid_source", "clip_id is required.", field="clip_id")
    root = dataset_root(config)
    dataset, issues = load_dataset(root)
    manifest_error = next(
        (
            issue
            for issue in issues
            if issue.severity == "error"
            and (
                issue.field in {"assets.jsonl", "clip_id"}
                or (issue.field == "clips.jsonl" and issue.code != "missing_reference")
            )
        ),
        None,
    )
    if manifest_error is not None:
        raise MusicPrefError(
            "schema_invalid",
            "Fix assets.jsonl and clips.jsonl before preparing a clip.",
            field=manifest_error.field,
        )
    asset = next((row for row in dataset.assets if row.asset_id == asset_id), None)
    if asset is None:
        raise MusicPrefError(
            "ineligible",
            "Asset is not in the manifest. Staged audio cannot enter the primary condition.",
            record_id=asset_id,
            field="asset_id",
        )
    prepared_rel = f"prepared/{clip_id}.wav"
    qc_rel = f"qc/{clip_id}.json"
    wav_path = resolve_under_root(root, prepared_rel)
    qc_path = resolve_under_root(root, qc_rel)
    if any(clip.clip_id == clip_id for clip in dataset.clips) or wav_path.exists() or qc_path.exists():
        raise MusicPrefError(
            "already_exists",
            "That clip id already has a prepared file, QC sidecar, or clips.jsonl row. Refusing to overwrite.",
            record_id=clip_id,
            field="clip_id",
        )
    audio, sample_rate = read_audio(resolve_under_root(root, asset.relative_path))
    excerpt = prepare_excerpt(
        audio,
        sample_rate,
        start_seconds,
        end_seconds,
        config.audio.normalization_profile,
        config.level_matched,
    )
    wave = waveform_for_encoder(excerpt)
    if excerpt.loudness_mismatch:
        eligibility = "excluded_loudness_mismatch"
        reason = "Loudness is outside 0.1 LU of -20 after one constant gain. Excluded from the primary level-matched condition."
    else:
        eligibility = "primary_level_matched"
        reason = "Within 0.1 LU of -20 LUFS and at or under -1 dBTP. Accepted for the primary level-matched condition."
    qc = QCSidecar(
        asset_id=asset_id,
        clip_id=clip_id,
        start_seconds=start_seconds,
        end_seconds=end_seconds,
        preprocessing_id=excerpt.preprocessing_id,
        preprocessing_sha256=excerpt.preprocessing_sha256,
        prepared_pcm_sha256=pcm_hash(wave),
        gain_db=float(excerpt.gain_db),
        integrated_lufs=None if excerpt.integrated_lufs is None else float(excerpt.integrated_lufs),
        true_peak_dbtp=None if excerpt.true_peak_dbtp is None else float(excerpt.true_peak_dbtp),
        loudness_mismatch=excerpt.loudness_mismatch,
        eligibility=eligibility,
        eligibility_reason=reason,
        prepared_relative_path=prepared_rel,
    )

    def write(created: list[Path], restores: list[tuple[Path, bytes]]) -> QCSidecar:
        _ensure_manifest(root, "clips.jsonl", created)
        if wav_path.exists() or qc_path.exists():
            raise MusicPrefError("already_exists", "Refusing to overwrite a prepared clip.", record_id=clip_id)
        wav_path.parent.mkdir(parents=True, exist_ok=True)
        created.append(wav_path)
        sf.write(wav_path, wave, 48000, format="WAV", subtype="FLOAT")
        written, written_rate = sf.read(wav_path, always_2d=False, dtype="float32")
        if written_rate != 48000 or pcm_hash(written) != qc.prepared_pcm_sha256:
            raise MusicPrefError("hash_mismatch", "Prepared WAV does not match the excerpt.", field="relative_path")
        _write_new(qc_path, canonical_bytes(qc.model_dump(mode="json")), created)
        if eligibility == "primary_level_matched":
            clip = Clip.model_validate(
                {
                    "schema_version": SCHEMA_VERSION,
                    "clip_id": clip_id,
                    "asset_id": asset_id,
                    "start_seconds": start_seconds,
                    "end_seconds": end_seconds,
                    "audition_condition": config.audio.normalization_profile,
                }
            )
            _append_model(root / "clips.jsonl", clip, restores)
        return qc

    return _run(write)
