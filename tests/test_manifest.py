import json

import pytest
from pydantic import ValidationError

from votelle_music.data.manifest import canonical_pair_id, load_config, orient_judgment, validate
from votelle_music.schemas import FoundationConfig
from tests.fixtures.build import build_dataset, make_judgment, write_config


def codes(report):
    return {issue.code for issue in report.issues}


def rewrite_first(path, **changes):
    rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    rows[0].update(changes)
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def append_judgment(root, **overrides):
    path = root / "judgments.jsonl"
    rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    raw = dict(rows[0])
    raw.pop("judgment_id")
    raw.update(overrides)
    raw.setdefault("judgment_id", "judgment-repeat")
    raw["pair_id"] = canonical_pair_id(raw["clip_a_id"], raw["clip_b_id"])
    rows.append(raw)
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def checked(tmp_path, name, root):
    return validate(load_config(write_config(tmp_path / f"{name}.json", root)))


def repeat_rows(report):
    return [(issue.record_id, issue.code, issue.remediation) for issue in report.issues]


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


def test_delayed_repeat_may_use_another_session(tmp_path):
    root = build_dataset(tmp_path / "delayed", link="pair")
    append_judgment(
        root,
        session_id="session-later",
        timestamp="2026-10-12T00:00:00Z",
        confidence=0.8,
        is_repeat_of="judgment-0",
    )
    assert checked(tmp_path, "delayed", root).issues == []


def test_reversed_candidate_presentation_is_a_valid_repeat(tmp_path):
    root = build_dataset(tmp_path / "reversed", link="pair")
    append_judgment(
        root,
        clip_a_id="clip-1",
        clip_b_id="clip-0",
        presentation_order="BA",
        adherence_choice="B",
        preference_choice="A",
        acceptable_a="no",
        acceptable_b="yes",
        session_id="session-later",
        timestamp="2026-10-11T00:00:00Z",
        is_repeat_of="judgment-0",
    )
    assert checked(tmp_path, "reversed", root).issues == []


def test_repeat_of_missing_judgment_is_rejected(tmp_path):
    root = build_dataset(tmp_path / "missing-repeat", link="pair")
    rewrite_first(root / "judgments.jsonl", is_repeat_of="missing-judgment")
    assert repeat_rows(checked(tmp_path, "missing-repeat", root)) == [
        ("judgment-0", "missing_reference", "Repeat judgments must point at an existing judgment."),
    ]


def test_judgment_cannot_repeat_itself(tmp_path):
    root = build_dataset(tmp_path / "self-repeat", link="pair")
    rewrite_first(root / "judgments.jsonl", is_repeat_of="judgment-0")
    assert repeat_rows(checked(tmp_path, "self-repeat", root)) == [
        ("judgment-0", "invalid_repeat", "A judgment cannot repeat itself."),
    ]


def test_repeat_requires_the_same_unordered_clip_pair(tmp_path):
    root = build_dataset(tmp_path / "other-pair", families=3, link="chain")
    append_judgment(root, clip_b_id="clip-2", is_repeat_of="judgment-0")
    assert repeat_rows(checked(tmp_path, "other-pair", root)) == [
        ("judgment-repeat", "invalid_repeat", "A repeat must use the same unordered clip pair."),
    ]


def test_repeat_requires_the_same_brief(tmp_path):
    root = build_dataset(tmp_path / "other-brief", families=3, link="chain")
    append_judgment(root, brief_id="brief-1", is_repeat_of="judgment-0")
    assert repeat_rows(checked(tmp_path, "other-brief", root)) == [
        ("judgment-repeat", "invalid_repeat", "A repeat must use the same creative brief."),
    ]


def test_repeat_requires_the_same_listener(tmp_path):
    root = build_dataset(tmp_path / "other-listener", link="pair")
    append_judgment(root, listener_id="other-listener", is_repeat_of="judgment-0")
    assert repeat_rows(checked(tmp_path, "other-listener", root)) == [
        ("judgment-repeat", "invalid_repeat", "A repeat must use the same listener."),
    ]


def test_repeat_may_disagree_with_the_original(tmp_path):
    root = build_dataset(tmp_path / "disagree", link="pair")
    append_judgment(
        root,
        adherence_choice="B",
        preference_choice="tie",
        acceptable_a="no",
        acceptable_b="unsure",
        confidence=0.1,
        session_id="session-later",
        timestamp="2026-10-11T00:00:00Z",
        is_repeat_of="judgment-0",
    )
    assert checked(tmp_path, "disagree", root).issues == []


def test_repeat_chain_is_allowed(tmp_path):
    root = build_dataset(tmp_path / "repeat-chain", link="pair")
    append_judgment(
        root,
        judgment_id="judgment-r1",
        session_id="session-2",
        timestamp="2026-10-11T00:00:00Z",
        is_repeat_of="judgment-0",
    )
    append_judgment(
        root,
        judgment_id="judgment-r2",
        session_id="session-3",
        timestamp="2026-10-12T00:00:00Z",
        is_repeat_of="judgment-r1",
    )
    assert checked(tmp_path, "repeat-chain", root).issues == []


def test_repeat_cycle_is_rejected(tmp_path):
    root = build_dataset(tmp_path / "cycle", link="pair")
    rewrite_first(root / "judgments.jsonl", is_repeat_of="judgment-repeat")
    append_judgment(
        root,
        judgment_id="judgment-repeat",
        session_id="session-later",
        timestamp="2026-10-11T00:00:00Z",
        is_repeat_of="judgment-0",
    )
    assert repeat_rows(checked(tmp_path, "cycle", root)) == [
        ("judgment-0", "invalid_repeat", "Repeat links must not form a cycle."),
        ("judgment-repeat", "invalid_repeat", "Repeat links must not form a cycle."),
    ]
