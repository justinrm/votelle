"""Local P-01 intake. Tones and fake MP3 bytes are not music or preference evidence."""

import hashlib
import json
from pathlib import Path

import numpy as np
import pytest
import soundfile as sf

from votelle_music.audio.loudness import integrated_loudness
from votelle_music.audio.prepare import file_sha256, pcm_hash, preprocessing_document, read_audio
from votelle_music.cli import main
from votelle_music.data.ingest import IngestRequest, ingest, prepare_clip
from votelle_music.data.manifest import load_config, load_dataset, validate
from votelle_music.schemas import SCHEMA_VERSION, MusicPrefError, RightsRecord, canonical_bytes, sha256_hex
from tests.fixtures.build import dump_jsonl, write_config

DISQUIET = "https://incompetech.com/music/royalty-free/mp3-royaltyfree/Disquiet.mp3"
MESMERIZE = "https://incompetech.com/music/royalty-free/mp3-royaltyfree/Mesmerize.mp3"
AURA = "https://incompetech.com/music/royalty-free/mp3-royaltyfree/Colorless%20Aura.mp3"
ACQUIRED = "2026-10-09T18:00:00Z"
COMMAND = "ffmpeg -i Disquiet.mp3 -c:a pcm_f32le Disquiet.wav"


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _mp3(path: Path, payload: bytes) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"ID3" + payload)
    return path


def _tone(seconds: float, rate: int, amplitude: float = 0.2, spike: bool = False) -> np.ndarray:
    count = int(round(seconds * rate))
    time = np.arange(count) / rate
    samples = (amplitude * np.sin(2 * np.pi * 440.0 * time)).astype(np.float64)
    if spike:
        samples[:] = 0.001
        samples[count // 2] = 0.8
    return samples


def _wav(path: Path, samples: np.ndarray, rate: int, flac: bool = False) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(path, samples, rate, format="FLAC" if flac else "WAV", subtype="PCM_16" if flac else "FLOAT")
    return path


def _config(path: Path, root: Path, **overrides):
    fields = {
        "rights_policy": "research_only",
        "level_matched": True,
        "audio": {
            "excerpt_seconds": 10,
            "sample_rate": 48000,
            "channels": 1,
            "normalization_profile": "gain_lufs_v1",
        },
    }
    fields.update(overrides)
    return load_config(write_config(path, root, **fields))


def _rights(root: Path, *, status: str = "reviewed", research: str = "allowed", file_exists: bool = True) -> str:
    evidence = root / "evidence" / "terms.txt"
    evidence.parent.mkdir(parents=True, exist_ok=True)
    evidence.write_text("local snapshot of the training offer\n", encoding="utf-8")
    digest = file_sha256(evidence)
    relative = "evidence/terms.txt"
    if not file_exists:
        relative = "evidence/missing.txt"
        digest = _sha(b"missing")
    record = RightsRecord.model_validate(
        {
            "schema_version": SCHEMA_VERSION,
            "rights_record_id": "rights-p01",
            "rightsholder": "Kevin MacLeod",
            "evidence_path": relative,
            "evidence_url": None,
            "evidence_sha256": digest,
            "recorded_at": ACQUIRED,
            "license_identifier": "CC-BY-4.0",
            "components": ["recording", "composition"],
            "attribution": None,
            "exceptions": None,
            "research_training": research,
            "commercial_training": "unknown",
            "audio_release": "unknown",
            "embedding_release": "unknown",
            "checkpoint_release": "unknown",
            "review_status": status,
            "review_rationale": "Human reviewed the saved terms snapshot.",
        }
    )
    dump_jsonl(root / "rights.jsonl", [record])
    return "rights-p01"


def _request(root: Path, uri: str, raw: Path, decoded: Path, **overrides) -> IngestRequest:
    fields = {
        "source_uri": uri,
        "raw_path": raw,
        "decoded_path": decoded,
        "acquired_at": ACQUIRED,
        "decode_tool": "ffmpeg",
        "decode_version": "7.1",
        "decode_command": COMMAND,
        "rights_record_id": None,
        "family_review_path": None,
    }
    fields.update(overrides)
    return IngestRequest(**fields)


def _pair(directory: Path, name: str, *, rate: int = 44100, seconds: float = 12.0, flac: bool = False, spike: bool = False):
    raw = _mp3(directory / f"{name}.mp3", name.encode() + b"-raw")
    decoded = _wav(
        directory / f"{name}.flac" if flac else directory / f"{name}.wav",
        _tone(seconds, rate, spike=spike),
        rate,
        flac=flac,
    )
    return raw, decoded


def test_receipt_links_uri_raw_hash_decode_command_and_measured_wav(tmp_path):
    root = tmp_path / "data"
    incoming = tmp_path / "in"
    raw, decoded = _pair(incoming, "disquiet", rate=44100, seconds=12)
    raw_before = raw.read_bytes()
    config = _config(tmp_path / "p01.json", root)
    _rights(root)
    receipt = ingest(config, _request(root, DISQUIET, raw, decoded, rights_record_id="rights-p01"))

    info = sf.info(decoded)
    decoded_audio, decoded_rate = read_audio(root / receipt.decoded_relative_path)
    assert receipt.source_uri == DISQUIET
    assert receipt.raw_sha256 == _sha(raw_before)
    assert receipt.raw_sha256 != receipt.decoded_sha256
    assert receipt.decoded_sha256 == _sha((root / receipt.decoded_relative_path).read_bytes())
    assert receipt.acquired_at == ACQUIRED
    assert receipt.decode_tool == "ffmpeg"
    assert receipt.decode_version == "7.1"
    assert receipt.decode_command == COMMAND
    assert receipt.sample_rate == info.samplerate == decoded_rate == 44100
    assert receipt.channels == info.channels == 1
    assert receipt.frames == info.frames
    assert receipt.duration_seconds == pytest.approx(info.frames / info.samplerate)
    assert receipt.format_name == "WAV"
    assert receipt.lossless_master is False
    assert receipt.asset_id
    assert raw.read_bytes() == raw_before
    assert (root / receipt.raw_relative_path).read_bytes() == raw_before
    assert (root / receipt.decoded_relative_path).suffix == ".wav"
    assert (root / receipt.decoded_relative_path).read_bytes()[:4] == b"RIFF"
    assert not (root / receipt.decoded_relative_path).read_bytes().startswith(b"ID3")

    dataset, issues = load_dataset(root)
    assert issues == []
    asset = dataset.assets[0]
    assert asset.asset_id == receipt.asset_id
    assert asset.sha256_original == receipt.decoded_sha256
    assert asset.sha256_pcm == pcm_hash(decoded_audio)
    assert asset.source_uri == DISQUIET
    assert asset.source_revision == "USUAN1500036"
    assert asset.origin_type == "public_dataset"
    assert asset.sample_rate == 44100
    assert asset.rights_record_id == "rights-p01"
    assert asset.parent_asset_ids == []
    assert dataset.judgments == []
    assert (root / "judgments.jsonl").is_file()


def test_decode_command_is_not_executed(tmp_path):
    root = tmp_path / "data"
    incoming = tmp_path / "in"
    raw, decoded = _pair(incoming, "disquiet")
    marker = tmp_path / "executed.txt"
    config = _config(tmp_path / "p01.json", root)
    _rights(root)
    command = f"touch {marker}"
    receipt = ingest(
        config,
        _request(root, DISQUIET, raw, decoded, rights_record_id="rights-p01", decode_command=command),
    )
    assert receipt.decode_command == command
    assert not marker.exists()


def test_missing_local_file_is_not_fetched(tmp_path):
    root = tmp_path / "data"
    config = _config(tmp_path / "p01.json", root)
    missing = tmp_path / "nope.mp3"
    decoded = tmp_path / "nope.wav"
    with pytest.raises(MusicPrefError) as caught:
        ingest(config, _request(root, DISQUIET, missing, decoded))
    assert caught.value.code == "invalid_source"
    assert not missing.exists()
    assert not root.exists() or not any(root.rglob("*.mp3"))


def test_invalid_source_writes_nothing(tmp_path):
    root = tmp_path / "data"
    incoming = tmp_path / "in"
    raw, decoded = _pair(incoming, "disquiet")
    renamed = incoming / "renamed.wav"
    renamed.write_bytes(raw.read_bytes())
    config = _config(tmp_path / "p01.json", root)
    cases = [
        _request(root, "https://example.invalid/Disquiet.mp3", raw, decoded),
        _request(root, AURA.replace("%20", " "), raw, decoded),
        _request(root, DISQUIET, raw, renamed),
        _request(root, DISQUIET, decoded, decoded),
        _request(root, DISQUIET, raw, decoded, decode_command="  "),
    ]
    for request in cases:
        with pytest.raises(MusicPrefError) as caught:
            ingest(config, request)
        assert caught.value.code in {"invalid_source", "lossy_source_mislabelled", "missing_provenance"}
    assert not (root / "assets.jsonl").exists() or (root / "assets.jsonl").read_text(encoding="utf-8") == ""
    assert list(root.rglob("*.wav")) == [] if root.exists() else True
    assert list(root.rglob("*.mp3")) == [] if root.exists() else True


def test_tracks_stay_distinct_until_a_reviewed_relationship(tmp_path):
    root = tmp_path / "data"
    incoming = tmp_path / "in"
    config = _config(tmp_path / "p01.json", root)
    _rights(root)
    first_raw, first_decoded = _pair(incoming, "disquiet", rate=44100)
    second_raw, second_decoded = _pair(incoming, "mesmerize", rate=48000, seconds=11)
    third_raw, third_decoded = _pair(incoming, "aura", rate=22050, seconds=15, flac=True)
    receipts = [
        ingest(config, _request(root, DISQUIET, first_raw, first_decoded, rights_record_id="rights-p01")),
        ingest(config, _request(root, MESMERIZE, second_raw, second_decoded, rights_record_id="rights-p01")),
        ingest(config, _request(root, AURA, third_raw, third_decoded, rights_record_id="rights-p01")),
    ]
    families = {item.song_family_id for item in receipts}
    recordings = {item.source_recording_id for item in receipts}
    assert len(families) == 3
    assert len(recordings) == 3
    assert len({item.asset_id for item in receipts}) == 3
    assert receipts[2].decoded_relative_path.endswith(".flac")
    dataset, _issues = load_dataset(root)
    assert len({asset.artist_id for asset in dataset.assets}) == 1
    assert {asset.song_family_id for asset in dataset.assets} == families
    assert {asset.source_revision for asset in dataset.assets} == {"USUAN1500036", "USUAN1500005", "USUAN1400008"}


def test_only_a_reviewed_relationship_shares_a_song_family(tmp_path):
    def review(status: str) -> Path:
        path = tmp_path / f"review-{status}.json"
        path.write_text(
            json.dumps(
                {
                    "schema_version": "0.1",
                    "review_status": status,
                    "rationale": "Listener confirmed a shared melody.",
                    "same_song_family": [[DISQUIET, MESMERIZE]],
                }
            ),
            encoding="utf-8",
        )
        return path

    def families(status: str) -> set[str]:
        root = tmp_path / status
        incoming = tmp_path / f"in-{status}"
        config = _config(tmp_path / f"{status}.json", root)
        _rights(root)
        left_raw, left_decoded = _pair(incoming, "disquiet")
        right_raw, right_decoded = _pair(incoming, "mesmerize", seconds=11)
        path = review(status)
        left = ingest(
            config,
            _request(root, DISQUIET, left_raw, left_decoded, rights_record_id="rights-p01", family_review_path=path),
        )
        right = ingest(
            config,
            _request(root, MESMERIZE, right_raw, right_decoded, rights_record_id="rights-p01", family_review_path=path),
        )
        assert left.source_recording_id != right.source_recording_id
        return {left.song_family_id, right.song_family_id}

    assert len(families("reviewed")) == 1
    assert len(families("provisional")) == 2


def test_duplicate_source_or_pcm_is_rejected(tmp_path):
    root = tmp_path / "data"
    incoming = tmp_path / "in"
    config = _config(tmp_path / "p01.json", root)
    _rights(root)
    raw, decoded = _pair(incoming, "disquiet")
    request = _request(root, DISQUIET, raw, decoded, rights_record_id="rights-p01")
    first = ingest(config, request)
    receipt_before = (root / "receipts" / f"{first.asset_id}.json").read_bytes()
    copied_before = (root / first.raw_relative_path).read_bytes()
    with pytest.raises(MusicPrefError) as caught:
        ingest(config, request)
    assert caught.value.code == "duplicate_id"
    assert (root / "receipts" / f"{first.asset_id}.json").read_bytes() == receipt_before
    assert (root / first.raw_relative_path).read_bytes() == copied_before

    other_raw = _mp3(incoming / "other.mp3", b"other-raw")
    with pytest.raises(MusicPrefError) as caught:
        ingest(config, _request(root, MESMERIZE, other_raw, decoded, rights_record_id="rights-p01"))
    assert caught.value.code == "duplicate_id"
    assert [path.name for path in (root / "receipts").iterdir()] == [f"{first.asset_id}.json"]


def test_missing_or_provisional_rights_stay_staged(tmp_path):
    root = tmp_path / "data"
    incoming = tmp_path / "in"
    raw, decoded = _pair(incoming, "disquiet")
    config = _config(tmp_path / "p01.json", root)
    staged = ingest(config, _request(root, DISQUIET, raw, decoded))
    assert staged.rights_gate == "provisional_review"
    assert staged.in_manifest is False
    assert staged.release_clearance == "not_assessed"
    assert load_dataset(root)[0].assets == []

    provisional = tmp_path / "provisional"
    incoming_b = tmp_path / "in-b"
    raw_b, decoded_b = _pair(incoming_b, "mesmerize")
    config_b = _config(tmp_path / "b.json", provisional)
    _rights(provisional, status="provisional")
    before = (provisional / "rights.jsonl").read_bytes()
    receipt = ingest(config_b, _request(provisional, MESMERIZE, raw_b, decoded_b, rights_record_id="rights-p01"))
    assert receipt.rights_gate == "provisional_review"
    assert receipt.in_manifest is False
    assert (provisional / "rights.jsonl").read_bytes() == before
    assert load_dataset(provisional)[0].assets == []

    missing = tmp_path / "missing"
    incoming_c = tmp_path / "in-c"
    raw_c, decoded_c = _pair(incoming_c, "aura", flac=True)
    config_c = _config(tmp_path / "c.json", missing)
    _rights(missing, file_exists=False)
    receipt = ingest(config_c, _request(missing, AURA, raw_c, decoded_c, rights_record_id="rights-p01"))
    assert receipt.rights_gate == "provisional_review"
    assert receipt.in_manifest is False
    assert load_dataset(missing)[0].assets == []


def test_reviewed_evidence_does_not_grant_permissions_or_release(tmp_path):
    root = tmp_path / "data"
    incoming = tmp_path / "in"
    raw, decoded = _pair(incoming, "disquiet")
    config = _config(tmp_path / "p01.json", root)
    _rights(root, research="unknown")
    before = (root / "rights.jsonl").read_bytes()
    receipt = ingest(config, _request(root, DISQUIET, raw, decoded, rights_record_id="rights-p01"))
    assert receipt.rights_gate == "reviewed_with_evidence"
    assert receipt.in_manifest is True
    assert receipt.release_clearance == "not_assessed"
    assert (root / "rights.jsonl").read_bytes() == before
    research = validate(config)
    assert "permission_unknown" in {issue.code for issue in research.issues}
    commercial = validate(_config(tmp_path / "release.json", root, rights_policy="commercial_ready"))
    assert commercial.has_errors()
    assert "permission_unknown" in {issue.code for issue in commercial.issues}


def test_repeat_ingest_is_deterministic(tmp_path):
    def once(name: str) -> bytes:
        root = tmp_path / name
        incoming = tmp_path / f"in-{name}"
        raw, decoded = _pair(incoming, "disquiet", rate=44100, seconds=12)
        config = _config(tmp_path / f"{name}.json", root)
        _rights(root)
        receipt = ingest(config, _request(root, DISQUIET, raw, decoded, rights_record_id="rights-p01"))
        stored = json.loads((root / "receipts" / f"{receipt.asset_id}.json").read_text(encoding="utf-8"))
        return canonical_bytes(stored)

    assert once("a") == once("b")


def test_failed_ingest_removes_partial_files(tmp_path):
    root = tmp_path / "data"
    root.mkdir()
    incoming = tmp_path / "in"
    raw, decoded = _pair(incoming, "disquiet")
    raw_before = raw.read_bytes()
    config = _config(tmp_path / "p01.json", root)
    _rights(root)
    assets = root / "assets.jsonl"
    assets.write_text("", encoding="utf-8")
    assets.chmod(0o444)
    with pytest.raises(MusicPrefError):
        ingest(config, _request(root, DISQUIET, raw, decoded, rights_record_id="rights-p01"))
    assert raw.read_bytes() == raw_before
    assert list(root.rglob("*.mp3")) == []
    assert list(root.rglob("*.wav")) == []
    assert list(root.glob("receipts/*")) == []
    assert assets.read_text(encoding="utf-8") == ""


def test_prepare_records_qc_and_admits_only_a_level_match(tmp_path):
    root = tmp_path / "data"
    incoming = tmp_path / "in"
    raw, decoded = _pair(incoming, "disquiet", rate=48000, seconds=12, spike=False)
    config = _config(tmp_path / "p01.json", root)
    _rights(root, research="allowed")
    receipt = ingest(config, _request(root, DISQUIET, raw, decoded, rights_record_id="rights-p01"))
    qc = prepare_clip(config, receipt.asset_id, "clip-disquiet", 1.0, 11.0)
    prepared = root / qc.prepared_relative_path
    audio, rate = sf.read(prepared, always_2d=False, dtype="float32")
    assert rate == 48000
    assert audio.shape == (480_000,)
    assert audio.dtype == np.float32
    assert sf.info(prepared).subtype == "FLOAT"
    assert qc.asset_id == receipt.asset_id
    assert qc.clip_id == "clip-disquiet"
    assert qc.start_seconds == 1.0
    assert qc.end_seconds == 11.0
    assert qc.preprocessing_id == "gain_lufs_v1"
    assert qc.preprocessing_sha256 == sha256_hex(canonical_bytes(preprocessing_document("gain_lufs_v1")))
    assert qc.prepared_pcm_sha256 == pcm_hash(audio)
    assert qc.loudness_mismatch is False
    assert qc.eligibility == "primary_level_matched"
    assert qc.eligibility_reason
    assert integrated_loudness(np.asarray(audio, dtype=np.float64), rate) == pytest.approx(-20.0, abs=0.1)
    assert qc.true_peak_dbtp <= -1.0
    dataset, issues = load_dataset(root)
    assert issues == []
    assert [clip.clip_id for clip in dataset.clips] == ["clip-disquiet"]
    assert dataset.clips[0].audition_condition == "gain_lufs_v1"
    assert dataset.clips[0].start_seconds == 1.0
    assert validate(config).issues == []

    other = tmp_path / "other"
    other_in = tmp_path / "other-in"
    other_raw, other_decoded = _pair(other_in, "disquiet", rate=48000, seconds=12)
    other_config = _config(tmp_path / "other.json", other)
    _rights(other, research="allowed")
    other_receipt = ingest(other_config, _request(other, DISQUIET, other_raw, other_decoded, rights_record_id="rights-p01"))
    other_qc = prepare_clip(other_config, other_receipt.asset_id, "clip-disquiet", 1.0, 11.0)
    assert canonical_bytes(json.loads((root / "qc" / "clip-disquiet.json").read_text(encoding="utf-8"))) == canonical_bytes(
        json.loads((other / "qc" / "clip-disquiet.json").read_text(encoding="utf-8"))
    )
    other_prepared = other / other_qc.prepared_relative_path
    left, left_rate = sf.read(prepared, always_2d=True, dtype="float32")
    right, right_rate = sf.read(other_prepared, always_2d=True, dtype="float32")
    left_info, right_info = sf.info(prepared), sf.info(other_prepared)
    assert np.array_equal(left, right)
    assert left_info.frames == right_info.frames == left.shape[0] == 480_000
    assert left_info.samplerate == right_info.samplerate == left_rate == right_rate == 48000
    assert left_info.channels == right_info.channels == left.shape[1] == 1
    assert left_info.subtype == right_info.subtype == "FLOAT"
    assert qc.prepared_pcm_sha256 == other_qc.prepared_pcm_sha256 == pcm_hash(left[:, 0])
    assert qc.preprocessing_id == other_qc.preprocessing_id == "gain_lufs_v1"
    assert qc.preprocessing_sha256 == other_qc.preprocessing_sha256
    # libsndfile stamps the WAV PEAK chunk, so container bytes are provenance only.
    assert file_sha256(prepared) != qc.prepared_pcm_sha256
    assert file_sha256(other_prepared) != other_qc.prepared_pcm_sha256


def test_loudness_mismatch_stays_out_of_the_primary_condition(tmp_path):
    root = tmp_path / "data"
    incoming = tmp_path / "in"
    raw, decoded = _pair(incoming, "disquiet", rate=48000, seconds=10, spike=True)
    config = _config(tmp_path / "p01.json", root)
    _rights(root, research="allowed")
    receipt = ingest(config, _request(root, DISQUIET, raw, decoded, rights_record_id="rights-p01"))
    qc = prepare_clip(config, receipt.asset_id, "clip-spike", 0.0, 10.0)
    audio, rate = sf.read(root / qc.prepared_relative_path, always_2d=False, dtype="float32")
    assert qc.loudness_mismatch is True
    assert qc.eligibility == "excluded_loudness_mismatch"
    assert abs(integrated_loudness(np.asarray(audio, dtype=np.float64), rate) - (-20.0)) > 0.1
    assert load_dataset(root)[0].clips == []
    report = validate(config)
    assert "loudness_mismatch" not in {issue.code for issue in report.issues}


def test_prepare_rejects_staged_assets_bad_bounds_and_overwrite(tmp_path):
    root = tmp_path / "data"
    incoming = tmp_path / "in"
    raw, decoded = _pair(incoming, "disquiet", rate=48000, seconds=12)
    config = _config(tmp_path / "p01.json", root)
    staged = ingest(config, _request(root, DISQUIET, raw, decoded))
    with pytest.raises(MusicPrefError) as caught:
        prepare_clip(config, staged.asset_id, "clip-nope", 0.0, 10.0)
    assert caught.value.code == "ineligible"
    assert list(root.rglob("prepared/*")) == []

    _rights(root, research="allowed")
    eligible_root = tmp_path / "eligible"
    eligible_in = tmp_path / "eligible-in"
    eligible_raw, eligible_decoded = _pair(eligible_in, "disquiet", rate=48000, seconds=12)
    eligible_config = _config(tmp_path / "eligible.json", eligible_root)
    _rights(eligible_root, research="allowed")
    receipt = ingest(
        eligible_config,
        _request(eligible_root, DISQUIET, eligible_raw, eligible_decoded, rights_record_id="rights-p01"),
    )
    with pytest.raises(MusicPrefError) as caught:
        prepare_clip(eligible_config, receipt.asset_id, "clip-short", 0.0, 9.0)
    assert caught.value.code == "duration_not_ten_seconds"
    assert list(eligible_root.glob("prepared/*")) == []

    qc = prepare_clip(eligible_config, receipt.asset_id, "clip-ok", 0.0, 10.0)
    before = (eligible_root / "qc" / "clip-ok.json").read_bytes()
    with pytest.raises(MusicPrefError) as caught:
        prepare_clip(eligible_config, receipt.asset_id, "clip-ok", 0.0, 10.0)
    assert caught.value.code == "already_exists"
    assert (eligible_root / "qc" / "clip-ok.json").read_bytes() == before
    assert load_dataset(eligible_root)[0].clips[0].clip_id == qc.clip_id


def test_failed_prepare_removes_partial_audio(tmp_path):
    root = tmp_path / "data"
    incoming = tmp_path / "in"
    raw, decoded = _pair(incoming, "disquiet", rate=48000, seconds=12)
    config = _config(tmp_path / "p01.json", root)
    _rights(root, research="allowed")
    receipt = ingest(config, _request(root, DISQUIET, raw, decoded, rights_record_id="rights-p01"))
    (root / "qc").write_text("blocker", encoding="utf-8")
    with pytest.raises(MusicPrefError):
        prepare_clip(config, receipt.asset_id, "clip-ok", 0.0, 10.0)
    assert list(root.glob("prepared/*")) == []
    assert (root / "qc").read_text(encoding="utf-8") == "blocker"
    assert load_dataset(root)[0].clips == []


def test_p01_config_is_separate_from_the_fixture_profile():
    foundation = load_config(Path("configs/foundation.json"))
    piano = load_config(Path("configs/p01_piano.json"))
    assert foundation.audio.normalization_profile == "none_fixture_only"
    assert foundation.level_matched is False
    assert piano.dataset_root == "data/p01_piano"
    assert piano.rights_policy == "research_only"
    assert piano.audio.normalization_profile == "gain_lufs_v1"
    assert piano.level_matched is True
    assert piano.network_access is False
    assert piano.encoder.name == "dummy"
    assert piano.encoder.revision == "fixture-v1"
    assert piano.audio.excerpt_seconds == 10


def test_cli_ingest_and_prepare(tmp_path, capsys):
    root = tmp_path / "data"
    incoming = tmp_path / "in"
    raw, decoded = _pair(incoming, "disquiet", rate=48000, seconds=12)
    config_path = write_config(
        tmp_path / "p01.json",
        root,
        rights_policy="research_only",
        level_matched=True,
        audio={
            "excerpt_seconds": 10,
            "sample_rate": 48000,
            "channels": 1,
            "normalization_profile": "gain_lufs_v1",
        },
    )
    _rights(root, research="allowed")
    code = main(
        [
            "ingest",
            "--config",
            str(config_path),
            "--source-uri",
            DISQUIET,
            "--raw",
            str(raw),
            "--decoded",
            str(decoded),
            "--acquired-at",
            ACQUIRED,
            "--decode-tool",
            "ffmpeg",
            "--decode-version",
            "7.1",
            "--decode-command",
            COMMAND,
            "--rights-record-id",
            "rights-p01",
        ]
    )
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["in_manifest"] is True
    assert payload["release_clearance"] == "not_assessed"
    prepare_code = main(
        [
            "prepare",
            "--config",
            str(config_path),
            "--asset-id",
            payload["asset_id"],
            "--clip-id",
            "clip-cli",
            "--start",
            "0",
            "--end",
            "10",
        ]
    )
    assert prepare_code == 0
    qc = json.loads(capsys.readouterr().out)
    assert qc["eligibility"] == "primary_level_matched"
    assert not (tmp_path / "split.json").exists()
