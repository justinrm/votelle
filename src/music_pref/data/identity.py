"""Connected components for leakage-safe splits.

ponytail: exact id and hash edges only. Near-duplicate audio needs a
separate detector before any real training split.
"""

from __future__ import annotations

from dataclasses import dataclass

from music_pref.schemas import Asset, Brief, Clip, Judgment, canonical_bytes, sha256_hex


@dataclass(frozen=True)
class Component:
    component_id: str
    asset_ids: tuple[str, ...]
    brief_ids: tuple[str, ...]
    judgment_ids: tuple[str, ...]
    song_family_ids: tuple[str, ...]
    weight: int


class _UnionFind:
    def __init__(self) -> None:
        self.parent: dict[str, str] = {}

    def add(self, node: str) -> None:
        self.parent.setdefault(node, node)

    def find(self, node: str) -> str:
        self.add(node)
        while self.parent[node] != node:
            self.parent[node] = self.parent[self.parent[node]]
            node = self.parent[node]
        return node

    def union(self, left: str, right: str) -> None:
        root_left, root_right = self.find(left), self.find(right)
        if root_left != root_right:
            self.parent[root_right] = root_left


def _union_key(groups: _UnionFind, nodes: list[tuple[str, str]]) -> None:
    buckets: dict[str, list[str]] = {}
    for key, node in nodes:
        buckets.setdefault(key, []).append(node)
    for members in buckets.values():
        first = members[0]
        for other in members[1:]:
            groups.union(first, other)


def connected_components(
    assets: list[Asset],
    briefs: list[Brief],
    clips: list[Clip],
    judgments: list[Judgment],
) -> list[Component]:
    groups = _UnionFind()
    asset_nodes = [(asset.asset_id, f"asset:{asset.asset_id}") for asset in assets]
    for asset_id, node in asset_nodes:
        groups.add(node)
    for brief in briefs:
        groups.add(f"brief:{brief.brief_id}")
    for judgment in judgments:
        groups.add(f"judgment:{judgment.judgment_id}")

    _union_key(groups, [(asset.source_recording_id, f"asset:{asset.asset_id}") for asset in assets])
    _union_key(groups, [(asset.song_family_id, f"asset:{asset.asset_id}") for asset in assets])
    _union_key(groups, [(asset.sha256_original, f"asset:{asset.asset_id}") for asset in assets])
    _union_key(groups, [(asset.sha256_pcm, f"asset:{asset.asset_id}") for asset in assets])
    _union_key(groups, [(brief.brief_family_id, f"brief:{brief.brief_id}") for brief in briefs])

    known_assets = {asset.asset_id for asset in assets}
    for asset in assets:
        for parent_id in asset.parent_asset_ids:
            if parent_id in known_assets:
                groups.union(f"asset:{asset.asset_id}", f"asset:{parent_id}")

    clip_asset = {clip.clip_id: clip.asset_id for clip in clips}
    for judgment in judgments:
        node = f"judgment:{judgment.judgment_id}"
        for clip_id in (judgment.clip_a_id, judgment.clip_b_id):
            asset_id = clip_asset.get(clip_id)
            if asset_id in known_assets:
                groups.union(node, f"asset:{asset_id}")
        groups.union(node, f"brief:{judgment.brief_id}")
        if judgment.is_repeat_of:
            groups.union(node, f"judgment:{judgment.is_repeat_of}")

    members: dict[str, list[str]] = {}
    for node in groups.parent:
        members.setdefault(groups.find(node), []).append(node)

    assets_by_id = {asset.asset_id: asset for asset in assets}
    components: list[Component] = []
    for nodes in members.values():
        asset_ids = tuple(sorted(node.removeprefix("asset:") for node in nodes if node.startswith("asset:")))
        brief_ids = tuple(sorted(node.removeprefix("brief:") for node in nodes if node.startswith("brief:")))
        judgment_ids = tuple(sorted(node.removeprefix("judgment:") for node in nodes if node.startswith("judgment:")))
        families = tuple(sorted({assets_by_id[asset_id].song_family_id for asset_id in asset_ids}))
        payload = {"assets": list(asset_ids), "briefs": list(brief_ids), "judgments": list(judgment_ids)}
        components.append(
            Component(
                component_id=sha256_hex(canonical_bytes(payload)),
                asset_ids=asset_ids,
                brief_ids=brief_ids,
                judgment_ids=judgment_ids,
                song_family_ids=families,
                weight=len(families),
            )
        )
    return sorted(components, key=lambda component: component.component_id)
