"""Keep manifest paths inside the dataset root."""

from __future__ import annotations

from pathlib import Path

from votelle_music.schemas import VotelleError


def resolve_under_root(root: Path, relative: str) -> Path:
    path = Path(relative)
    if not relative or path.is_absolute() or ".." in path.parts:
        raise VotelleError(
            "path_escape",
            "Paths must be relative to the dataset root. A manifest cannot leave that root.",
            field="relative_path",
        )
    root_resolved = root.resolve()
    candidate = (root_resolved / path).resolve()
    if candidate != root_resolved and root_resolved not in candidate.parents:
        raise VotelleError(
            "path_escape",
            "Paths must be relative to the dataset root. A manifest cannot leave that root.",
            field="relative_path",
        )
    return candidate
