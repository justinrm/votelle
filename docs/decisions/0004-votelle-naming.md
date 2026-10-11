# 0004 — Votelle naming

The live identifiers are the project name Votelle, distribution `votelle-music`, import package `votelle_music`, CLI executable `votelle-music`, and primary exception `VotelleError`. Protocol stays `0.1`. Package version stays `0.1.0`.

This records the remaining rename after the package and CLI already used those identifiers. It does not change excerpt length, grouping, rights, label meaning, error codes, return values, schemas, serialization, hashes, or dataset semantics.

## Replacements

| Historical | Canonical |
|---|---|
| Human-readable project name in the first handoff | Votelle |
| Distribution and CLI `music-pref` | `votelle-music` |
| Import package `music_pref` | `votelle_music` |
| Exception `MusicPrefError` | `VotelleError` |

`FeatureError` and `SplitError` still subclass the primary exception. The constructor is unchanged: `code`, `remediation`, `record_id`, and `field`.

## Compatibility

No permanent alias. `MusicPrefError` is not part of a supported external contract.

Evidence in this tree:

- `votelle_music` does not re-export the exception. Callers import it from `votelle_music.schemas`.
- The CLI prints `code` and `remediation`. It does not print the class name.
- Manifests, configs, and hashes do not store the class name.
- The README installs from the checkout and does not assume a published PyPI distribution.
- This tree has no `music_pref` package. This decision does not add one.

## Scope

Renamed in live source and tests. Current-status sentences that still said the exception was `MusicPrefError` were corrected in `README.md`, `AGENTS.md`, and `docs/STATUS.md`.

Accepted decisions 0001–0003 and `docs/archive/` were not rewritten. They still contain `music-pref` and `music_pref` as historical text. The 10 October 2026 documentation integration moved the notes that used those spellings as contract language into `docs/archive/research-preconsolidation-2026-10/`. The English phrase “music-preference” in the dataset note is not an identifier.

## Retained historical names

- `docs/decisions/0002-audition-normalization.md` and `docs/decisions/0003-p01-ingestion.md` still name the earlier `music-pref` commands.
- `docs/archive/research-v0.1/08_Cursor_Agent_Implementation_Handoff.md` and `docs/archive/README.md` still describe `src/music_pref/`.
- `docs/archive/research-preconsolidation-2026-10/06_MVP_Technical_Specification.md` still uses `music_pref` and `music-pref` as its original placeholder contract. The live specification is `docs/research/05_MVP_SPECIFICATION.md`.

## Verification

From the repository root, with no model download, audio acquisition, training, or external API call:

- `uv sync --locked --group dev`
- `uv run python tests/fixtures/build.py --dest tests/fixtures/pilot --families 20`
- `uv run votelle-music validate --config configs/foundation.json`
- `uv run votelle-music split --config configs/foundation.json --output runs/split.json`
- `uv run pytest -q`
- `git diff --check`

Imports and the console script use `votelle_music` and `votelle-music`. A search of `src/` and `tests/` shows no `MusicPrefError`.
