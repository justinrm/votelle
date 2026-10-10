# 0001 — Foundation choices

Session 1 of research v0.1. These are the reversible choices the research notes left open. They are not permission to change excerpt length, label meaning, or grouping.

- Policy `commercial_ready` requires `allowed` on research training, commercial training, audio release, embedding release, and checkpoint release. `research_only` requires `allowed` research training and labels artifacts with that provenance. Unknown or denied research training still fails. A license string never grants a permission.
- Source JSONL is immutable. Prepared audio, diagnostics, and split membership are written as new artifacts.
- A clip must be within 1 ms of 10 seconds. The loader does not pad or trim. Paths must stay under the dataset root. Commands run from the repository root; relative `dataset_root` is resolved from the current working directory.
- Canonical PCM is little-endian float32 at the file's original rate and channel count, before crop or resample. `sha256_original` is the file bytes.
- Digital silence is a peak absolute amplitude below `1e-8`. Quieter musical material above that threshold is not rejected here.
- Preparation always uses `scipy.signal.resample` to 480,000 mono samples. Method id: `scipy.signal.resample/fft/v1`. Profile `none_fixture_only` applies no loudness gain. Session 1 recognized `gain_lufs_v1` and refused it. Session 2A implements it in `docs/decisions/0002-audition-normalization.md`.
- Identity edges are exact ids and hashes only. Near-duplicate audio is not detected. Generator identity is not a main-split edge. Component weight is the number of distinct song families in the component.
- Splits shuffle components with `random.Random(seed)` and assign whole components by weight deficit. A component heavier than the largest split fraction, fewer components than positive splits, or an empty positive split is an error. No partial file is written.
- The dummy encoder is `dummy` / `fixture-v1`. It cannot support a production claim. Cache keys use canonical JSON of the source PCM hash, excerpt bounds, preprocessing hash, encoder identity, processor hash, pooling, and dtype.
- Fixture judgments used to build graphs are `synthetic_rule` edges, not human preference labels.
