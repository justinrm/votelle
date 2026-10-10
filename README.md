# music_pref

Offline data foundation for a music-preference research library. Protocol v0.1.

**Fixture success is not evidence of preference prediction.** The tones under `tests/fixtures/` are generated test signals, not music and not human judgments. A passing test only means the manifests, rights checks, splits, and dummy encoder behave as specified.

## What this package is

It validates JSONL manifests, applies an explicit rights profile, builds leakage-safe identity components, prepares a declared 10-second excerpt, and caches a dummy 512-d embedding. The dummy encoder is named `dummy` / `fixture-v1` and cannot support a production claim. Profile `none_fixture_only` does not loudness-match anything. Profile `gain_lufs_v1` is the audition path: one constant gain toward -20 LUFS, stopped at -1 dBTP. A passing tone test is not evidence of musical suitability. The rules are in `docs/decisions/0002-audition-normalization.md`.

Not in this tree: CLAP, training, an MLP, calibration, inference bundles, a generator, or a UI. Those are later sessions. Architecture notes live in `docs/research/`. Locked implementation choices are in `docs/decisions/0001-foundation-choices.md`.

## Setup

Use the pinned Python 3.11 environment. Do not use the system Python 3.14 interpreter for this package.

```bash
uv python install 3.11
uv sync --group dev
```

Core dependencies are pydantic, numpy, soundfile, and scipy. Exact pins are in `uv.lock`. Torch and Transformers are not installed.

## Commands

From the repository root:

```bash
uv run python tests/fixtures/build.py --dest tests/fixtures/pilot --families 20
uv run music-pref validate --config configs/foundation.json
uv run music-pref split --config configs/foundation.json --output runs/split.json
uv run pytest
```

`validate` prints a JSON report and exits nonzero when any issue has severity `error`. `split` writes a canonical JSON artifact and refuses to break a connected component. A fully connected comparison graph produces no split file.

The pilot builder writes generated tones and copies `tests/fixtures/FIRST_PARTY_DECLARATION.md` into the dataset. Generated audio is gitignored.

## Last check

`uv run pytest -q` on CPython 3.11.16: 39 passed in 3.72s. The run did not download models or open a network connection. Installed core packages are pinned in `uv.lock` (numpy 2.4.6, pydantic 2.14.0, scipy 1.17.1, soundfile 0.14.0, pytest 9.1.1). Torch and Transformers are not installed.

## Next session

Session 2B is the CLAP probe, not more normalization work. Use a separate environment for torch and Transformers. Do not add them to this core environment. Do not run extraction until one rights-cleared excerpt exists; the tones in this tree are fixtures. The encoder protocol needs no signature change. See `docs/decisions/0002-audition-normalization.md`. Re-check this tree with:

```bash
uv run pytest
```
