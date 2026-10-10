# music_pref

Offline data foundation for a music-preference research library. Protocol v0.1.

**Fixture success is not evidence of preference prediction.** The tones under `tests/fixtures/` are generated test signals, not music and not human judgments. A passing test only means the manifests, rights checks, splits, and dummy encoder behave as specified.

## What this package is

It validates JSONL manifests, applies an explicit rights profile, builds leakage-safe identity components, prepares a declared 10-second excerpt, and caches a dummy 512-d embedding. The dummy encoder is named `dummy` / `fixture-v1` and cannot support a production claim. Profile `none_fixture_only` does not loudness-match anything. Profile `gain_lufs_v1` is the audition path: one constant gain toward -20 LUFS, stopped at -1 dBTP. A passing tone test is not evidence of musical suitability. The rules are in `docs/decisions/0002-audition-normalization.md`.

Not in this tree: CLAP, training, an MLP, calibration, inference bundles, a generator, or a UI. Those are later sessions. Architecture notes live in `docs/research/`. Locked implementation choices are in `docs/decisions/0001-foundation-choices.md` and `docs/decisions/0002-audition-normalization.md`. P-01 intake rules are in `docs/decisions/0003-p01-ingestion.md`.

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

## P-01 Reflective Piano

`configs/p01_piano.json` points at `data/p01_piano` and uses `gain_lufs_v1`. It does not download audio. The operator decodes each official MP3 to a WAV or FLAC first and writes a reviewed rights row before ingest. Ingest copies both files, writes a receipt, and appends an asset only when that rights row is `reviewed` and its local evidence file matches the recorded hash. It does not edit permissions. `prepare` writes a float32 48 kHz mono WAV from the operator's crop. A loudness mismatch stays out of `clips.jsonl`. Do not run `split` on this config. Layout and the three gates (provisional review, dataset eligibility, release clearance) are in `docs/decisions/0003-p01-ingestion.md`.

```bash
uv run music-pref ingest --config configs/p01_piano.json \
  --source-uri "https://incompetech.com/music/royalty-free/mp3-royaltyfree/Disquiet.mp3" \
  --raw /path/to/Disquiet.mp3 \
  --decoded /path/to/Disquiet.wav \
  --acquired-at 2026-10-09T18:00:00Z \
  --decode-tool ffmpeg \
  --decode-version 7.1 \
  --decode-command "ffmpeg -i Disquiet.mp3 -c:a pcm_f32le Disquiet.wav" \
  --rights-record-id RIGHTS_ID

uv run music-pref prepare --config configs/p01_piano.json \
  --asset-id ASSET_ID \
  --clip-id clip-disquiet-1 \
  --start 30 --end 40
```

A reviewed song-family link is an optional `--family-review` JSON file. Without it, Disquiet, Mesmerize, and Colorless Aura stay three recording ids and three song families. Passing the file does not rewrite an ingest that already happened.

## Last check

`uv run pytest -q` on CPython 3.11.16: 56 passed in 4.21s. The run did not download models, weights, or audio. Installed core packages are pinned in `uv.lock` (numpy 2.4.6, pydantic 2.14.0, scipy 1.17.1, soundfile 0.14.0, pytest 9.1.1). Torch and Transformers are not installed.

## Next session

Session 2B is the CLAP probe, in a separate environment. Do not add Torch or Transformers to this environment. Do not run extraction until a human has downloaded the MP3s, reviewed permissions, chosen crops, and accepted the excerpts as musically suitable. Fixture tones and a passing ingest test are not that acceptance. The encoder protocol needs no signature change. See `docs/decisions/0002-audition-normalization.md`. Re-check this tree with:

```bash
uv run pytest
```
