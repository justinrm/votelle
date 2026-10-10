# Votelle

This file binds every coding agent on a clone of this repository, including Cursor, Claude Code, Codex, and GitHub Copilot. Research protocol v0.1. The tree is the offline data foundation for preference research, not a trained music evaluator.

Read `README.md` and `docs/STATUS.md` before changing the tree. Then read the source and tests for the behavior you are changing, and the decision record that covers it. Load only the research note the task needs.

## Environment

Use uv and CPython 3.11. From the repository root:

```bash
uv sync --locked --group dev
```

PyTorch and Transformers are not dependencies of this environment. Do not add them to make a test pass. The package is `votelle_music`. The CLI is `votelle-music`.

## Check

A change is checked from the repository root:

```bash
uv run python tests/fixtures/build.py --dest tests/fixtures/pilot --families 20
uv run votelle-music validate --config configs/foundation.json
uv run votelle-music split --config configs/foundation.json --output runs/split.json
uv run pytest -q
```

`test_repeat_ingest_is_deterministic` can fail when two generated WAV headers differ by timestamp even though the PCM matches. A green run is a software check. Fixture success is not evidence of preference prediction.

## Do not

- Do not download model weights, train, add a generator, or add a UI.
- Do not treat fixture tests as evidence of preference prediction.
- A change to excerpt length, grouping, rights, or label meaning needs a new protocol version. Do not make that change as an incidental refactor.
- Decision records still say `music-pref` / `music_pref`. The exception class remains `MusicPrefError`. Do not rename them in a documentation pass.
- `docs/research/06_MVP_Technical_Specification.md` is a broader contract, not a list of implemented modules.
- Ingest records a decode command. It does not run that command and it does not download audio.
- Do not run `split` on the P-01 acquisition pilot.

## Git and data

Git does not contain the P-01 audio. Do not commit `data/`, `runs/`, `tests/fixtures/pilot/`, audio, embeddings, or weights.

Apache-2.0 covers original source code and project documentation. It does not clear recordings, annotations, embeddings, or model artifacts. A permission declaration is not legal clearance.

## Authority

The order is in `docs/research/README.md`. Short form: code, tests, configs, and `uv.lock` say what runs; `docs/decisions/` are the accepted choices; `docs/research/` holds scientific requirements the tests do not retire; `docs/archive/` is earlier rationale; `graphify-out/` is a map. An inferred graph edge is a hint. Open the `source_file` and check it.

Consult `docs/archive/` only for provenance, a citation, or a contradiction. Do not load the whole research package by default.

## What to open

| Task | Open |
|---|---|
| Audio preparation and normalization | `docs/decisions/0002-audition-normalization.md`, then `src/votelle_music/audio/` |
| Rights and dataset acquisition | `docs/decisions/0001-foundation-choices.md`, `docs/decisions/0003-p01-ingestion.md`, `docs/research/01_Data_Feasibility_and_Rights_Audit.md` |
| CLAP encoder integration | `docs/decisions/0002-audition-normalization.md`, `docs/research/03_CLAP_Encoder_Feasibility_and_Benchmark_Handoff.md` |
| Human listening experiments | `docs/research/02_P0_Dataset_and_Listening_Protocol.md`, `docs/research/04_Dataset_and_Human_Feedback_Strategy.md` |
| Training and evaluation | `docs/research/05_Training_and_Evaluation_Research_Plan.md`, `docs/decisions/0001-foundation-choices.md` |
| Scientific methodology and prior art | `docs/research/03_Audio_Encoder_and_Architecture_Analysis.md`. For a citation or a prior-art dispute, also `docs/archive/research-v0.1/02_Literature_and_Competitive_Landscape.md` and `10_Source_Register.md` |
| Schemas and manifests | `src/votelle_music/schemas.py`, then `src/votelle_music/data/` |
| CLI | `src/votelle_music/cli.py` |
| Identity and splitting | `src/votelle_music/data/identity.py`, `src/votelle_music/data/splits.py` |
| Tests and fixtures | `tests/`, and `tests/fixtures/build.py` for generated tones |

Open risks that are not decisions: `docs/archive/research-v0.1/09_Research_Risks_and_Open_Questions.md`, summarized in `docs/STATUS.md`.

## Graphify

Graphify is optional. Contributing does not require it. When the CLI is installed and cross-file tracing would help, use one focused command: `graphify query "<question>"`, `graphify path "<A>" "<B>"`, or `graphify explain "<concept>"`. Verify every relationship in the source file. Do not load `graphify-out/graph.json` or `graphify-out/GRAPH_REPORT.md` in full. After a structural code change, refresh with `graphify update .`. Do not install Torch or Transformers to refresh the graph.

## Finish

Update `docs/STATUS.md` when implementation progress actually changes. Do not rewrite research notes to match the code.
