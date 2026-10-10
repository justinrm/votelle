import json

import pytest
from pydantic import ValidationError

from votelle_music.data.manifest import load_config, orient_judgment, validate
from votelle_music.schemas import FoundationConfig
from tests.fixtures.build import build_dataset, make_judgment, write_config


def codes(report):
    return {issue.code for issue in report.issues}


def rewrite_first(path, **changes):
    rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    rows[0].update(changes)
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def test_foundation_config_requires_level_match_flag():
    config = load_config(__import__("pathlib").Path("configs/foundation.json"))
    assert config.level_matched is False
    assert config.network_access is False
    assert config.audio.normalization_profile == "none_fixture_only"
    with pytest.raises(ValidationError):
        FoundationConfig.model_validate({"schema_version": "0.1"})


def test_permitted_fixture_validates(tmp_path):
    root = build_dataset(tmp_path / "data", families=1)
    report = validate(load_config(write_config(tmp_path / "config.json", root)))
    assert report.issues == []
    assert report.provenance == "commercial_ready"


def test_missing_reference_path_escape_duplicate_and_bounds(tmp_path):
    root = build_dataset(tmp_path / "missing", families=1)
    rewrite_first(root / "clips.jsonl", asset_id="missing-asset")
    report = validate(load_config(write_config(tmp_path / "missing.json", root)))
    assert "missing_reference" in codes(report)

    root = build_dataset(tmp_path / "escape", families=1)
    rewrite_first(root / "assets.jsonl", relative_path="../outside.wav")
    report = validate(load_config(write_config(tmp_path / "escape.json", root)))
    assert "path_escape" in codes(report)

    root = build_dataset(tmp_path / "dup", families=1)
    line = (root / "assets.jsonl").read_text(encoding="utf-8")
    (root / "assets.jsonl").write_text(line + line, encoding="utf-8")
    report = validate(load_config(write_config(tmp_path / "dup.json", root)))
    assert "duplicate_id" in codes(report)

    root = build_dataset(tmp_path / "bounds", families=1)
    rewrite_first(root / "clips.jsonl", end_seconds=9)
    report = validate(load_config(write_config(tmp_path / "bounds.json", root)))
    assert "duration_not_ten_seconds" in codes(report)


def test_flipping_candidates_flips_labels_together():
    forward = make_judgment(
        clip_a_id="a",
        clip_b_id="b",
        adherence_choice="A",
        preference_choice="B",
        acceptable_a="yes",
        acceptable_b="no",
        presentation_order="AB",
    )
    backward = make_judgment(
        judgment_id="judgment-flip",
        clip_a_id="b",
        clip_b_id="a",
        adherence_choice="B",
        preference_choice="A",
        acceptable_a="no",
        acceptable_b="yes",
        presentation_order="AB",
    )
    assert orient_judgment(forward) == orient_judgment(backward)
    assert orient_judgment(backward).presentation_order == "AB"
