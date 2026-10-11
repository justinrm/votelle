# Votelle

This file binds every coding agent on a clone of this repository, including Cursor, Claude Code, Codex, and GitHub Copilot. Research protocol v0.1. The tree is the offline data foundation for preference research, not a trained music evaluator.

Before changing the tree, read the source and tests for the behavior you are changing, and the decision record that covers it. Load only the research note the task needs. Read `README.md` when the change affects the public contract or the quick start. Read `docs/STATUS.md` when the change affects recorded implementation status.

## Environment

Use uv and CPython 3.11. From the repository root:

```bash
uv sync --locked --group dev
```

PyTorch and Transformers are not dependencies of this environment. Do not add them to make a test pass. The package is `votelle_music`. The CLI is `votelle-music`.

## Check

A change to source, tests, configs, or schemas is checked from the repository root. Skip this sequence for a documentation-only or Cursor-configuration edit.

```bash
uv run python tests/fixtures/build.py --dest tests/fixtures/pilot --families 20
uv run votelle-music validate --config configs/foundation.json
uv run votelle-music split --config configs/foundation.json --output runs/split.json
uv run pytest -q
```

`test_repeat_ingest_is_deterministic` compares semantic identity and PCM across different WAV metadata, checks each file's provenance hash, and rejects duplicate overwrites. A green run is a software check. Fixture success is not evidence of preference prediction.

The same sequence is [`.github/workflows/ci.yml`](.github/workflows/ci.yml).

## Model downloads and execution

Do not download model weights during normal development. Do not install PyTorch or Transformers into the core Votelle environment. Do not begin training, model integration, or GPU benchmarking without task-specific authorization.

An explicitly authorized encoder feasibility task may use a separate environment and download only the named, pinned, approved model files. Verify checkpoint hashes before loading, follow documented security and resource safeguards, keep weights, environments, logs, and derived artifacts out of Git, and stop at the specific scope of the approved task.

This exception is not blanket permission for future downloads, model execution, paid compute, remote uploads, or expanded experiments; each requires explicit task-specific authorization. A documentation or maintenance task does not itself authorize downloads or model execution.

## Do not

- Do not add a generator or UI.
- Do not treat fixture tests as evidence of preference prediction.
- A change to excerpt length, grouping, rights, or label meaning needs a new protocol version. Do not make that change as an incidental refactor.
- Accepted decisions 0001–0003 and the archive still say `music-pref` / `music_pref`. The exception class is `VotelleError`. Do not rename those historical records in a documentation pass. Decision 0004 records the naming migration.
- `docs/research/05_MVP_SPECIFICATION.md` is the implementation-aware contract. The 9 October specification in `docs/archive/research-preconsolidation-2026-10/` is not a list of implemented modules.
- Ingest records a decode command. It does not run that command and it does not download audio.
- Do not run `split` on the P-01 acquisition pilot.

## Git and data

Git does not contain the P-01 audio. Do not commit `data/`, `runs/`, `tests/fixtures/pilot/`, audio, embeddings, or weights.

Apache-2.0 covers original source code and project documentation. It does not clear recordings, annotations, embeddings, or model artifacts. A permission declaration is not legal clearance.

## Authority

The order is in `docs/research/README.md`. Short form: code, tests, configs, and `uv.lock` say what runs; `docs/decisions/` are the accepted choices; `docs/research/` holds scientific requirements the tests do not retire; `docs/archive/` is earlier rationale; `graphify-out/` is an optional local map and is absent from a fresh checkout. An inferred graph edge is a hint. Open the `source_file` and check it.

`docs/PROJECT_DIRECTION.md` states long-term intent. It does not expand protocol v0.1 or override the order above.

Consult `docs/archive/` only for provenance, a citation, or a contradiction. Do not load the whole research package by default.

## What to open

| Task | Open |
|---|---|
| Audio preparation and normalization | `docs/decisions/0002-audition-normalization.md`, then `src/votelle_music/audio/` |
| Rights and dataset acquisition | `docs/decisions/0001-foundation-choices.md`, `docs/decisions/0003-p01-ingestion.md`, `docs/research/01_DATA_GOVERNANCE.md` |
| CLAP encoder integration | `docs/decisions/0002-audition-normalization.md`, `docs/research/03_ENCODER_AND_MODEL.md` |
| Human listening experiments | `docs/research/02_P0_LISTENING_PROTOCOL.md` |
| Training and evaluation | `docs/research/04_TRAINING_AND_EVALUATION.md`, `docs/decisions/0001-foundation-choices.md` |
| Scientific methodology and prior art | `docs/research/03_ENCODER_AND_MODEL.md` and `docs/research/REFERENCES.md`. For a citation or a prior-art dispute, also `docs/archive/research-v0.1/02_Literature_and_Competitive_Landscape.md` and `docs/archive/research-v0.1/10_Source_Register.md` |
| Implementation contract | `docs/research/05_MVP_SPECIFICATION.md`, then the source it names |
| Schemas and manifests | `src/votelle_music/schemas.py`, then `src/votelle_music/data/` |
| CLI | `src/votelle_music/cli.py` |
| Identity and splitting | `src/votelle_music/data/identity.py`, `src/votelle_music/data/splits.py` |
| Tests and fixtures | `tests/`, and `tests/fixtures/build.py` for generated tones |

Open risks that are not decisions: `docs/archive/research-v0.1/09_Research_Risks_and_Open_Questions.md`, summarized in `docs/STATUS.md`.

## Graphify

Graphify is optional. Contributing does not require it. When the CLI is installed and cross-file tracing would help, use one focused command: `graphify query "<question>"`, `graphify path "<A>" "<B>"`, or `graphify explain "<concept>"`. Do not run Graphify before every file read. Verify every relationship in the source file. Do not load `graphify-out/graph.json` or `graphify-out/GRAPH_REPORT.md` in full. After a structural code change, refresh with `graphify update .`. Do not install Torch or Transformers to refresh the graph.

## Finish

Update `docs/STATUS.md` when implementation progress actually changes. Do not rewrite research notes to match the code.
