# Status

Votelle asks whether a compact model can learn one creator's musical preferences, and separately whether a clip follows that creator's brief, from comparative listening judgments. A negative result is a valid outcome. The listener keeps the final choice.

That question is the current experiment. [Project direction](PROJECT_DIRECTION.md) records the longer-term research intent. This file records implementation and research status. It does not mark a hypothesis as a result.

Research protocol **v0.1**. This file is the resumption note. Authority order is in `docs/research/README.md`.

The human-readable name is Votelle. This tree's package is `votelle_music` and the CLI is `votelle-music`. Decision records and the archived handoff still say `music-pref` / `music_pref`. `MusicPrefError` is still the exception class. That rename is a separate task.

## Licensing

On October 10, 2026, the maintainer selected Apache-2.0 for Votelle’s original source code and project documentation, unless a file explicitly states otherwise. The root [LICENSE](../LICENSE) contains the standard terms; `pyproject.toml` declares `Apache-2.0` and includes the license file in distributions. This does not change third-party library/model licenses or grant recording, composition, annotation, training, or artifact-release permissions. P-01 permission declarations remain unchanged.

## Implemented

Checked against source, configs, and tests. Fixture success is not preference prediction.

- JSONL manifests, explicit rights profiles, and unknown-permission blocking (`research_only`, `commercial_ready`).
- Leakage-safe splits by source and brief ancestry. Connected components are not broken.
- Ten-second excerpts. `none_fixture_only` resamples and does not loudness-match. `gain_lufs_v1` applies one gain toward -20 LUFS, capped at -1 dBTP, with a ±0.1 LU match flag.
- Content-addressed cache and a dummy encoder, `dummy` / `fixture-v1`. Any other encoder is refused.
- P-01 ingest and prepare. Provisional review, dataset eligibility, and release clearance stay distinct. Ingest does not edit permissions.

## Implemented, not experimentally validated

- `gain_lufs_v1` on fixture tones. No musically accepted excerpt is in Git.
- The P-01 intake path. A passing ingest test is not a rights grant and not a listening result.

## Not implemented

A core CLAP adapter, training, the linear scorer, the neural challenger, calibration, inference bundles, a generator, and a UI. Torch and Transformers are not dependencies of the core environment. Isolated single-clip CPU inference succeeded in a separate probe environment. That result is one technical excerpt, not an adapter and not the 20-clip benchmark.

## P-01

Git does not contain the audio. `data/` is gitignored, so a clone has the workflow and not the files.

The earlier local intake snapshot recorded Disquiet, Mesmerize, and Colorless Aura under Git-ignored `data/p01_piano`. Each receipt was `reviewed_with_evidence` and `in_manifest: true`; `research_training` was `allowed`, while commercial training, audio release, embedding release, and checkpoint release were `unknown`. `release_clearance` was `not_assessed`; brief, clip, and judgment manifests were empty. This maintenance pass did not inspect private audio or re-validate that intake. A later technical excerpt was reported prepared for the isolated probe below; technical preparation does not establish musical acceptance or a completed listening dataset.

## CLAP

**Single-clip CPU feasibility succeeded on October 10, 2026.** The feasibility run checked the saved reports in `runs/clap-cpu-probe/retries/20261010-144504/` and recomputed the checkpoint and waveform hashes. Those retry outputs match the copies at `runs/clap-cpu-probe/`. Host: macOS arm64, 8,589,934,592 bytes physical memory. Scope of this result: one technical excerpt on CPU. Musical acceptance, preference prediction, and the 20-clip benchmark remain open.

| Check | Evidence |
|---|---|
| Primary checkpoint | `laion/larger_clap_music`, revision `a0b4534a14f58e20944452dff00a22a06ce629d1`. `snapshot-hashes.json` records `weight_ok: true` and 776,444,665 bytes. Recomputed SHA-256 `5c289311f4a030d768af7ffbfdecd01b008aa64824211899a4e59f4f9d154fd1`, matching the pre-run `shasum` and the worker. |
| Embeddings | Three in-process passes and one fresh process. Audio and text shape `[1, 512]`, finite on every pass. L2 norms `0.9999999873370299` (audio) and `0.9999999792360142` (text). |
| Repeatability | In-process and fresh-process audio and text are bit-identical. Max absolute error `0`. Fresh cosine `1.0`. |
| Peak RSS | Cold `/usr/bin/time -l` maximum resident set size equals the polled peak: 1,103,282,176 bytes. Fresh-process time maximum: 1,096,663,040 bytes (`ru_maxrss` 1,096,646,656). About 1.10 GB, under the 4,500,000,000-byte guardrail. The fresh poll (755,826,688) sampled a 2.89-second process too coarsely to catch that maximum. |
| Host pressure | Pre-run watch: 60 samples, last at 60.879 seconds, pressure 1 throughout, swap used constant at 557,192,314 bytes. Supervisor preflight and both run traces stayed at pressure 1. |
| Resource stop | `stop` is null. Cold and fresh worker return codes are 0. |

The technical input is the Disquiet 30–40 second excerpt: mono float32, 48 kHz, 480,000 samples. Recomputed PCM SHA-256 `f78adc9e79b8bc0a115df25ae981d7daccef63d1c08924cf3b07c1b116fd4507`. Observed mel shape `[1, 1, 1001, 64]`. The separate environment is Python 3.11.16, PyTorch 2.14.1, and Transformers 5.19.0. MPS was built and available; the run stayed on CPU.

An earlier attempt the same day stopped on yellow pressure sustained for 10 seconds, worker status `-9`, polled peak 151,371,776 bytes. The retained prior directory has no completed `cold.json`. Those logs remain in `retries/20261010-144504/prior/`. The dated [probe handoff](research/03_CLAP_Encoder_Feasibility_and_Benchmark_Handoff.md) is unchanged and still states its pre-attempt contract. Decision 0002 still prohibits naming CLAP in the foundation config. There is no core adapter.

**20-clip benchmark: not run.** Distinct-clip throughput, the embedding cache, and CPU/MPS parity are unmeasured.

**Four-text cosine check, same excerpt, CPU.** A fresh 60-second baseline passed before load: 59 samples, last at 60.041 seconds, pressure 1, swap used constant at 876,808,765 bytes. Limits stayed 4,500,000,000 bytes RSS, 128 MiB swap growth, and the 10-second yellow rule. Local output: `runs/clap-cpu-probe/semantic/20261010-150249/`. Python warnings: none. The final supervisor sample read pressure 2; the worker had already finished (5.32 seconds real), so the 10-second yellow stop did not fire. `stop` is null and the worker return code is 0. `/usr/bin/time -l` maximum resident set size was 1,039,990,784 bytes. The 100 ms poll peaked at 641,187,840 bytes.

One audio `pooler_output` was reused. Its float32 SHA-256 matches the feasibility run: `657881b15f2ee5dd2632939f0d698bc74b6f0a6da736c71cf2546e6f78fa4b77`. Audio L2 `0.9999999873370299`. Mel shape `[1, 1, 1001, 64]`, `is_longer` false. No cutoff was applied. Observed descending cosine order:

| Text | Tokens | Cosine |
|---|---:|---:|
| Reflective, gentle piano music. | 10 | -0.0002889722135070734 |
| Solo piano instrumental music. | 8 | -0.0006666518625852746 |
| Loud distorted electric guitar music. | 9 | -0.0007077695082539841 |
| A person speaking during an interview. | 9 | -0.0012963386684998245 |

These are encoder similarities for one technical excerpt. They are not listener preferences. Token IDs, masks, and extractor settings are in that directory's `result.json`.

A cleanup pass later on October 10, 2026 recomputed the checkpoint SHA-256 and byte length from the local `pytorch_model.bin`, and the PCM hash of `data/probes/disquiet_0030_0040/waveform.wav`. Both matched this record, as did the four cosine values in `semantic/20261010-150249/result.json`. The model was not reloaded.

## Open

These remain unresolved. Archiving the risk note did not close them.

- The eight source conflicts in `docs/archive/research-v0.1/09_Research_Risks_and_Open_Questions.md`: TuneJury's license, CMI counts, SongEval coverage, MusicPrefs' permission, Music Arena eligibility, HeartCLAP weights, MusicFM provenance, and unmeasured local encoder deployment.
- No finalized creator brief, no musically accepted 10-second crops, no human judgments; a technically prepared probe input does not close these gates.
- Release permissions for P-01 are `unknown`, so `commercial_ready` is not available.
- Whether frozen CLAP can carry the preference signal is untested. The four-text cosine check records encoder similarities for one technical excerpt and supplies no listener judgment.
- Package naming is inconsistent, as noted above.

`docs/decisions/0002-audition-normalization.md` is the loudness procedure. The archived feasibility handoff still describes that procedure as a proposal. Do not merge those texts.

## Next

Finalize the creator brief and musical acceptance of P-01 excerpts. Single-clip CPU feasibility and the four-text cosine check are recorded above. The 20-clip benchmark, MPS, training, and a core adapter wait for a separate explicit authorization. The safeguards remain 4,500,000,000 bytes RSS, an immediate stop on red pressure, a stop on yellow pressure sustained for 10 seconds, and a stop on 128 MiB swap growth over 15 seconds.

## Verification

Checked from this checkout on October 10, 2026 with uv 0.12.21 and CPython 3.11.16. Fixture success is not preference prediction. The test suite does not read P-01 audio or the probe waveform.

- Locked sync, a 20-family fixture build, `votelle-music validate` (0 issues), and `votelle-music split` (seed 17; 12 train, 2 validation, 2 calibration, and 4 test components).
- `pytest -q` three times for the foundation suite: 59 passed, 0 failed, no warnings.
- Repeat ingest compares semantic fields and PCM across different WAV containers. Each container hash is checked against its own file.
- Wheel and sdist `votelle_music-0.1.0`: package `votelle_music`, console script `votelle-music`, `License-Expression: Apache-2.0`, and the license file. The packages contain no audio or weights. Runtime dependencies remain NumPy, Pydantic, SciPy, and SoundFile.
- `.github/workflows/ci.yml` runs that sequence for pushes and pull requests to `main`, on Ubuntu, with CPython 3.11 and the lockfile. The workflow was checked locally. Hosted GitHub Actions has not run it.
- The recorded CLAP checkpoint SHA-256 and byte length, the probe PCM hash, and the four cosine values matched the local files. The model was not reloaded.

## Where to look

- Decisions: `docs/decisions/0001-foundation-choices.md`, `0002-audition-normalization.md`, `0003-p01-ingestion.md`
- Active research: `docs/research/README.md`
- Open risks and citations: `docs/archive/README.md`
