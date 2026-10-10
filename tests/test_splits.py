import json

import pytest

from votelle_music.data.identity import Component, connected_components
from votelle_music.data.manifest import load_config, load_dataset
from votelle_music.data.splits import SplitError, assign_components, write_split
from votelle_music.schemas import SplitFractions
from tests.fixtures.build import build_dataset, make_asset, make_brief, make_clip, make_judgment, write_config

FRACTIONS = SplitFractions.model_validate(
    {"train": 0.6, "validation": 0.1, "calibration": 0.1, "test": 0.2}
)


def _component(index: int, weight: int = 1) -> Component:
    return Component(
        component_id=f"{index:064x}",
        asset_ids=(f"asset-{index}",),
        brief_ids=(),
        judgment_ids=(),
        song_family_ids=tuple(f"family-{index}-{offset}" for offset in range(weight)),
        weight=weight,
    )


def test_identity_edges_keep_related_records_together():
    parent = make_asset(1)
    child = make_asset(2, parent_asset_ids=[parent.asset_id], song_family_id="other-family")
    assert len(connected_components([parent, child], [], [], [])) == 1

    same_pcm = make_asset(3, sha256_pcm=parent.sha256_pcm)
    assert len(connected_components([parent, same_pcm], [], [], [])) == 1
    same_file = make_asset(4, sha256_original=parent.sha256_original)
    assert len(connected_components([parent, same_file], [], [], [])) == 1

    shared_briefs = connected_components([], [make_brief(1, brief_family_id="same"), make_brief(2, brief_family_id="same")], [], [])
    assert len(shared_briefs) == 1

    left, right = make_asset(5), make_asset(6)
    clips = [make_clip(5, asset_id=left.asset_id), make_clip(6, asset_id=right.asset_id)]
    brief = make_brief(5)
    judgment = make_judgment(5, clip_a_id="clip-5", clip_b_id="clip-6", brief_id="brief-5")
    compared = connected_components([left, right], [brief], clips, [judgment])
    assert len(compared) == 1
    assert set(compared[0].asset_ids) == {left.asset_id, right.asset_id}
    assert brief.brief_id in compared[0].brief_ids

    extra_left, extra_right = make_asset(7), make_asset(8)
    extra_clips = [make_clip(7, asset_id=extra_left.asset_id), make_clip(8, asset_id=extra_right.asset_id)]
    repeat = make_judgment(
        6,
        clip_a_id="clip-7",
        clip_b_id="clip-8",
        brief_id="brief-5",
        is_repeat_of="judgment-5",
    )
    repeated = connected_components(
        [left, right, extra_left, extra_right],
        [brief],
        clips + extra_clips,
        [judgment, repeat],
    )
    assert len(repeated) == 1


def test_generator_identity_is_not_a_split_edge():
    generator = {
        "model_id": "fixture-generator",
        "revision": "v0",
        "seed": 1,
        "settings_hash": None,
        "component_license_evidence": None,
    }
    first = make_asset(1, generator=generator)
    second = make_asset(2, generator=generator)
    assert len(connected_components([first, second], [], [], [])) == 2


def test_twenty_equal_components_fill_every_split():
    components = [_component(index) for index in range(20)]
    assigned = assign_components(components, FRACTIONS, 17)
    assert {name: len(items) for name, items in assigned.items()} == {
        "train": 12,
        "validation": 2,
        "calibration": 2,
        "test": 4,
    }


def test_giant_component_and_too_few_groups_fail():
    with pytest.raises(SplitError) as giant:
        assign_components([_component(1, weight=13), *[_component(index) for index in range(2, 9)]], FRACTIONS, 17)
    assert giant.value.code == "unsplittable_component"
    with pytest.raises(SplitError) as few:
        assign_components([_component(index) for index in range(3)], FRACTIONS, 17)
    assert few.value.code == "insufficient_groups"


def test_file_split_is_byte_stable_and_keeps_descendants_together(tmp_path):
    root = build_dataset(tmp_path / "independent", families=20)
    config = load_config(write_config(tmp_path / "independent.json", root))
    first = tmp_path / "split-a.json"
    second = tmp_path / "split-b.json"
    write_split(config, first)
    write_split(config, second)
    assert first.read_bytes() == second.read_bytes()
    artifact = json.loads(first.read_text(encoding="utf-8"))
    assert {name: len(ids) for name, ids in artifact["splits"].items()} == {
        "train": 12,
        "validation": 2,
        "calibration": 2,
        "test": 4,
    }
    other = load_config(write_config(tmp_path / "other-seed.json", root, seed=18))
    other_artifact = write_split(other, tmp_path / "split-c.json")
    assert other_artifact["splits"] != artifact["splits"]

    linked = build_dataset(tmp_path / "linked", families=20, link="parent_link")
    linked_artifact = write_split(load_config(write_config(tmp_path / "linked.json", linked)), tmp_path / "linked.json")
    component = next(
        item
        for item in linked_artifact["components"]
        if "asset-0" in item["asset_ids"] and "asset-1" in item["asset_ids"]
    )
    homes = [name for name, ids in linked_artifact["splits"].items() if component["component_id"] in ids]
    assert len(homes) == 1


def test_connected_comparison_graph_writes_nothing(tmp_path):
    root = build_dataset(tmp_path / "chain", families=20, link="chain")
    output = tmp_path / "should-not-exist.json"
    with pytest.raises(SplitError) as exc:
        write_split(load_config(write_config(tmp_path / "chain.json", root)), output)
    assert exc.value.code == "unsplittable_component"
    assert not output.exists()


def test_duplicate_pcm_and_manifest_hash_invalidation(tmp_path):
    root = build_dataset(tmp_path / "dup", families=2, link="duplicate_pcm")
    dataset, issues = load_dataset(root)
    assert issues == []
    components = connected_components(dataset.assets, dataset.briefs, dataset.clips, dataset.judgments)
    assert len(components) == 1
    assert set(components[0].asset_ids) == {"asset-0", "asset-1"}

    independent = build_dataset(tmp_path / "hash", families=20)
    config = load_config(write_config(tmp_path / "hash.json", independent))
    before = write_split(config, tmp_path / "before.json")
    rows = [json.loads(line) for line in (independent / "assets.jsonl").read_text().splitlines() if line.strip()]
    rows[0]["acquired_at"] = "2026-10-10T00:00:00Z"
    (independent / "assets.jsonl").write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )
    after = write_split(config, tmp_path / "after.json")
    assert before["splits"] == after["splits"]
    assert before["split_sha256"] != after["split_sha256"]
