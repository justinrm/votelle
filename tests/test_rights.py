import json

from music_pref.data.manifest import load_config, validate
from tests.fixtures.build import build_dataset, write_config


def codes(report):
    return {issue.code for issue in report.issues}


def test_unknown_research_blocks_even_with_a_familiar_license(tmp_path):
    root = build_dataset(tmp_path / "data", families=1, rights_mode="unknown_research")
    report = validate(load_config(write_config(tmp_path / "config.json", root, rights_policy="research_only")))
    assert "permission_unknown" in codes(report)
    assert report.provenance == "research_only"


def test_unknown_audio_blocks_commercial_ready_only(tmp_path):
    root = build_dataset(tmp_path / "data", families=1, rights_mode="unknown_audio")
    commercial = validate(load_config(write_config(tmp_path / "commercial.json", root)))
    research = validate(
        load_config(write_config(tmp_path / "research.json", root, rights_policy="research_only"))
    )
    assert "permission_unknown" in codes(commercial)
    assert research.issues == []
    assert research.provenance == "research_only"


def test_denied_audio_blocks_commercial_release(tmp_path):
    root = build_dataset(tmp_path / "data", families=1, rights_mode="denied_audio")
    report = validate(load_config(write_config(tmp_path / "config.json", root)))
    assert "permission_denied" in codes(report)


def test_missing_rights_record(tmp_path):
    root = build_dataset(tmp_path / "data", families=1, rights_mode="omit")
    report = validate(load_config(write_config(tmp_path / "config.json", root)))
    assert "missing_rights" in codes(report)


def test_missing_component_scope_and_evidence(tmp_path):
    scoped = build_dataset(tmp_path / "scope", families=1)
    rows = [json.loads(line) for line in (scoped / "rights.jsonl").read_text().splitlines() if line.strip()]
    rows[0]["components"] = []
    (scoped / "rights.jsonl").write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
    report = validate(load_config(write_config(tmp_path / "scope.json", scoped)))
    assert "missing_component_scope" in codes(report)

    missing = build_dataset(tmp_path / "evidence", families=1)
    (missing / "FIRST_PARTY_DECLARATION.md").unlink()
    report = validate(load_config(write_config(tmp_path / "evidence.json", missing)))
    assert "missing_evidence" in codes(report)
