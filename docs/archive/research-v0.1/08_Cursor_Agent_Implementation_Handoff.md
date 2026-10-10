# 08 — Cursor Agent Implementation Handoff

Research v0.1 · October 9, 2026 · Review 01, 03–06 before implementation

## Engineering brief

Build a small reproducible music-ranking research library. The first session builds its **offline data foundation only**. Do not implement a music generator, agent system, web app or paid training workflow. Do not infer that a neural model has been proven necessary.

Authoritative decisions: architecture in 03, rights/annotation in 04, experiments in 05, contracts in 06, resources in 07. If a repository already exists, inspect its instructions and changes first and integrate safely. Record any necessary departure in a decision note; do not silently change the target or convert unknown permissions to allowed.

## Proposed repository boundaries

| Path | Responsibility |
|---|---|
| `pyproject.toml`, `uv.lock`, `.python-version` | Core dependencies, optional extras, exact reproducible environment |
| `src/music_pref/schemas.py` | Versioned Pydantic manifest, config and inference types |
| `src/music_pref/data/manifest.py` | JSONL parsing, referential integrity, deterministic serialization |
| `src/music_pref/data/rights.py` | Explicit policy profiles and auditable decisions |
| `src/music_pref/data/identity.py` | Ancestry, hashes, duplicate/group graph |
| `src/music_pref/data/splits.py` | Seeded component allocation and leakage audit |
| `src/music_pref/audio/prepare.py` | Decode, explicit crop, resampling and audition transforms |
| `src/music_pref/audio/measure.py` | Independent diagnostics with units/method IDs |
| `src/music_pref/features/base.py`, `dummy.py`, `clap.py` | Encoder protocol, offline fixture, real optional adapter |
| `src/music_pref/features/cache.py` | Content-keyed immutable feature cache |
| `src/music_pref/models/linear.py`, `mlp.py` | Candidate scorers only; no media I/O |
| `src/music_pref/training.py` | Train-only transforms, objectives, stopping and checkpointing |
| `src/music_pref/evaluation/` | Grouped metrics, paired intervals, slices and calibration |
| `src/music_pref/inference.py` | Bundle loading, compare/rank policy and typed abstention |
| `src/music_pref/cli.py` | Thin argparse commands |
| `configs/` | Small validated JSON configs; no hidden defaults |
| `tests/fixtures/` | Self-generated signals, manifests and deliberately invalid examples |
| `tests/` | Contract, identity, split, math and round-trip tests |
| `docs/`, `MODEL_CARD.md`, `DATA_CARD.md` | Decisions, protocol, limitations and provenance |
| `data/`, `cache/`, `runs/`, `checkpoints/` | Git-ignored user data and derived outputs |

Prefer one module per real responsibility, not one file per trivial class. Create directories only as the implementation reaches them.

## Stack selection

- **Python 3.11** for the initial compatibility baseline; 3.12 is a later supported target after the encoder environment passes. Do not depend on the user's global Python 3.14 installation.
- `uv` for a local virtual environment and dependency lock if already available; otherwise use an ordinary venv and a resolved lock process. Do not globally replace Python.
- Core: Pydantic, NumPy, soundfile, SciPy for a pinned resampling path; standard-library argparse, json, pathlib, hashlib and logging. Pytest for tests.
- Optional `clap`/`train` extras: PyTorch, Transformers, Hugging Face Hub, scikit-learn, Safetensors. Pin tested compatible versions at implementation time. This package does not assert an untested exact version matrix.
- FFmpeg for independently versioned audio/loudness operations when needed; invoke with argument arrays and controlled local paths. Keep it out of import-time requirements.
- Librosa is optional for musical feature experiments; torchaudio is optional rather than mandatory decoder infrastructure.
- Use JSON configuration validated by Pydantic. Hydra is unnecessary for this experiment count. Local metrics/config logs suffice; MLflow and a server are deferred. TensorBoard may be optional.
- No Rust, FastAPI, Docker requirement, cloud service, database or distributed scheduler initially.

If the real encoder requires different pins, isolate an encoder environment or optional extra while keeping core validation installable. Do not solve a dependency conflict by installing an unrelated large framework or silently swapping model IDs.

## Interface implementation notes

Use the exact data fields and semantics in 06. All IDs and paths are data; validate paths under the dataset root and do not execute manifest strings. Absolute external input paths may be explicitly imported into the dataset, but a downloaded manifest cannot escape its assigned root.

`validate` should return a structured report containing severity, record ID, field, error code and remediation. `split` takes a seed and grouping policy, emits a complete split artifact with hashes, and rejects insufficient independent groups. Do not try to hit exact ratios by splitting a connected component.

Real `embed_audio` and `embed_text` return 512-dimensional finite arrays plus an immutable feature specification. Normalization is explicit and handles zero norms as errors. The dummy encoder is clearly identified, deterministic and unusable for production model claims.

The linear scorer's feature interactions and intercept rule in 03 are locked. Unit-test conditionality, reversal symmetry and identical-input behavior. Training/evaluation consume persisted splits; they do not invent their own random splits. Calibration is a separately fitted artifact bound to a checkpoint and scope.

## Configuration example

Illustrative foundation config; the actual schema is validated and versioned:

```json
{
  "schema_version": "0.1",
  "dataset_root": "tests/fixtures/pilot",
  "rights_policy": "commercial_ready",
  "target": "adherence",
  "seed": 17,
  "split_fractions": {
    "train": 0.6,
    "validation": 0.1,
    "calibration": 0.1,
    "test": 0.2
  },
  "audio": {
    "excerpt_seconds": 10,
    "sample_rate": 48000,
    "channels": 1,
    "normalization_profile": "none_fixture_only"
  },
  "encoder": {"name": "dummy", "revision": "fixture-v1"},
  "network_access": false
}
```

The fixture-only normalization profile must be rejected for a claimed real level-matched experiment. The real training profile comes from 05. A `research_only` profile is explicit and labels output provenance; it is not a way to bypass permission that remains unknown for research itself.

## First bounded coding-session prompt

Copy the following into Cursor Agent after placing this research package in the repository's `docs/research/` folder:

```text
You are implementing only the offline foundation of Music Preference Model v0.1.

Read AGENTS.md and inspect git status and the repository before editing. Then read
docs/research/00_READ_ME.md and documents 03, 04, 05, 06 and 08. Treat these as a
connected specification. Summarize the scope and any concrete inconsistency, then
proceed with the bounded work below using reasonable reversible choices.

This is a research library, not a music generator or app. The architecture has not
been empirically validated. Do not claim that fixture success proves preference
prediction. Do not initiate paid work, download model weights, access external
datasets, collect other people's audio, or train a real model in this session.

Implement:
1. A Python 3.11 src-layout package called music_pref, with a minimal isolated
   environment and reproducible dependency configuration. Keep Torch, Transformers
   and model downloads outside the core import path.
2. Versioned Pydantic schemas for assets, rights, briefs, clips, judgments and
   splits from document 06. Add referential-integrity validation and clear errors.
3. Rights-policy validation with separate research training, commercial training,
   audio release, embedding release and checkpoint release permissions. Unknown
   must block the corresponding use. Preserve evidence and component scope.
4. Identity grouping covering parent recordings, song families, canonical hashes,
   both assets in comparisons, brief families and repeated judgments. Create
   deterministic component-level splits. Reject impossible splits; never fall
   back to random pair splitting.
5. WAV/FLAC loading, explicit ten-second crop validation, finite-sample checks,
   deterministic mono/resampling preparation and original basic diagnostics.
   Use a clearly named unnormalized fixture profile. Do not imply the real
   loudness-matched listening pipeline is complete.
6. An AudioTextEncoder protocol, a deterministic dummy encoder and a feature-cache
   key specification that includes content, excerpt, preprocessing and encoder
   identity. No real CLAP adapter yet.
7. CLI commands validate and split, plus a small offline fixture pipeline that
   exercises prepare and dummy feature extraction. Keep CLI logic thin.
8. Tests with generated tones/noise and licensed first-party fixture declarations.
   Cover duplicate/descendant leakage, connected comparison graphs, missing rights,
   bad bounds, NaN/Inf, silent signals, deterministic splits, A/B label orientation,
   hash invalidation and encoder dimension validation. Use at least 20 independent
   fixture families for split tests, plus a deliberately impossible connected set.
9. A README with reproducible commands, architecture boundaries, fixture-only
   warning and the next bounded task. Record dependencies, commands and results.

Before ending, run the relevant tests in the isolated environment and inspect the
diff for unrelated changes. Report what works, what is intentionally not built,
any unresolved issue and the exact next command/session. Stop after the offline
foundation passes; do not continue into model downloads, training or a UI.
```

## First-session acceptance checklist

1. A clean checkout installs the core package and runs tests with no model downloads or credentials.
2. A permitted fixture dataset validates; missing rights, missing references and invalid audio fail with actionable error codes.
3. Same-seed runs produce byte-stable split membership; all connected records remain together.
4. The intentionally unsplittable graph fails. No “helpful” fallback leaks identities across splits.
5. Identical input/configuration yields identical prepared audio and dummy features; changing an input changes the cache key.
6. The README and final report distinguish generated test signals from actual music/preference evidence.

These tests verify the experiment's foundations, not merely implementation details. A leakage bug could invalidate months of modeling work, so identity tests are worth doing early.

## Subsequent sessions, in order

**Session 2:** Add real audition normalization and its invariance/peak checks; audit and pin one official CLAP checkpoint; run a 20-clip CPU probe, optional MPS parity comparison, and measure memory/latency. Obtain original audio and label P0 under the same processing condition.

**Session 3:** Implement R0–R4, persisted train-only transforms, grouped metrics and paired confidence intervals. Produce the first honest exploratory report. No neural promotion from fixture labels.

**Session 4:** If enough real judgments exist, implement the exact small MLP and predeclared sweep; compare on the same splits. Add calibration only with its minimum evidence and separate fitting scope.

**Session 5:** Decide whether fresh confirmation, a personalization experiment, or an existing method is the best outcome. Package an inference bundle and model card only after the rights and research gates.

## Decisions not to change casually

Do not change excerpt duration, label semantics, encoder/preprocessing identity, grouping rules, evaluation data, probability meaning, rights policy, or primary success metric mid-experiment. A justified change creates a new protocol/version and invalidates incompatible caches or comparisons. Do not silently use the test set as validation. Human creative acceptance remains outside the model.
