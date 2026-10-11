# Active research

Protocol v0.1 notes that still govern method, rights, and promotion gates. Passing tests do not retire a requirement that the code has not implemented.

[Project direction](../PROJECT_DIRECTION.md) describes long-term project intent. It does not change these notes, the decisions, or what the software does.

The five consolidated notes are the current scientific text. Each one labels verified evidence, measurements, estimates, proposed methods, and unresolved questions in its own sections. A predecessor in the archive can still say "proposal" or "verified" in the words of its own date.

| Document | Governs | Does not claim |
|---|---|---|
| [01_DATA_GOVERNANCE.md](01_DATA_GOVERNANCE.md) | Acquisition suitability, permission policy, P-01 status, consent | That unknown permissions are allowed, or that P-01 is cleared for release |
| [02_P0_LISTENING_PROTOCOL.md](02_P0_LISTENING_PROTOCOL.md) | Preliminary study and the P0 listening procedure | That P0 has been run |
| [03_ENCODER_AND_MODEL.md](03_ENCODER_AND_MODEL.md) | Frozen CLAP contract, the 10 October 2026 single-clip CPU result, and the proposed rankers | A core adapter, MPS parity, the 20-clip benchmark, or a trained preference model |
| [04_TRAINING_AND_EVALUATION.md](04_TRAINING_AND_EVALUATION.md) | H1, H2, comparisons R0–R7, and promotion gates | That estimated sample sizes or expected gains are results |
| [05_MVP_SPECIFICATION.md](05_MVP_SPECIFICATION.md) | What the package runs, and which contracts remain proposed | That `train`, `evaluate`, `compare`, or `rank` exist |
| [REFERENCES.md](REFERENCES.md) | Source IDs S01–S83 and unresolved citation conflicts | Independent reproduction of author-reported results |

Accepted engineering choices are in [`docs/decisions/`](../decisions/). Current implementation status is in [`docs/STATUS.md`](../STATUS.md). Live commands are `votelle-music`. Historical `music-pref` / `music_pref` spellings in decisions 0001–0003 and in the archive are explained by [decision 0004](../decisions/0004-votelle-naming.md).

## Authority

1. Source, tests, `configs/`, and `uv.lock` establish what the software does.
2. `docs/decisions/` establish accepted engineering choices.
3. This directory establishes scientific requirements and experimental gates the code does not yet meet.
4. `docs/PROJECT_DIRECTION.md` states long-term project intent. It does not override items 1–3, change protocol v0.1, or turn a hypothesis into an implemented capability.
5. `docs/archive/` is evidence and earlier rationale. It does not override a later decision or the code.
6. `graphify-out/` is an optional local map. It is not in a fresh checkout and it is not a source of authority. An inferred edge is not a project fact. Follow `source_file` and check the file.

## Migration map

On 10 October 2026 the seven active notes moved to [`docs/archive/research-preconsolidation-2026-10/`](../archive/research-preconsolidation-2026-10/README.md). Their scientific requirements were carried into the consolidated notes. Requirements that the code has not implemented were not deleted. Content that remains only in the archive is historical wording, a pre-attempt contract, or a citation the consolidated note points at instead of copying.

| Superseded note | Current authority | Retained only as historical evidence |
|---|---|---|
| [01_Data_Feasibility_and_Rights_Audit.md](../archive/research-preconsolidation-2026-10/01_Data_Feasibility_and_Rights_Audit.md) | [Data governance](01_DATA_GOVERNANCE.md) | The audit's evidence-date header and any catalog count it states in its own words. Unknown permissions stay unknown |
| [02_P0_Dataset_and_Listening_Protocol.md](../archive/research-preconsolidation-2026-10/02_P0_Dataset_and_Listening_Protocol.md) | [P0 listening protocol](02_P0_LISTENING_PROTOCOL.md) | The 9 October session wording. P0 is still not run |
| [03_Audio_Encoder_and_Architecture_Analysis.md](../archive/research-preconsolidation-2026-10/03_Audio_Encoder_and_Architecture_Analysis.md) | [Encoder and model](03_ENCODER_AND_MODEL.md) | The architecture note's algebra and shortlist, which the encoder note cites rather than replacing with a new model |
| [03_CLAP_Encoder_Feasibility_and_Benchmark_Handoff.md](../archive/research-preconsolidation-2026-10/03_CLAP_Encoder_Feasibility_and_Benchmark_Handoff.md) | [Encoder and model](03_ENCODER_AND_MODEL.md) for the contract; [status](../STATUS.md) for the later single-clip CPU result | The handoff's statement that no encoder had run. That sentence is the pre-attempt record, not the 10 October result |
| [04_Dataset_and_Human_Feedback_Strategy.md](../archive/research-preconsolidation-2026-10/04_Dataset_and_Human_Feedback_Strategy.md) | [Data governance](01_DATA_GOVERNANCE.md) for rights and consent; [P0 protocol](02_P0_LISTENING_PROTOCOL.md) for collection; [training](04_TRAINING_AND_EVALUATION.md) for label-count planning | Corpus-by-corpus dispositions and the unresolved repeat-rate wording |
| [05_Training_and_Evaluation_Research_Plan.md](../archive/research-preconsolidation-2026-10/05_Training_and_Evaluation_Research_Plan.md) | [Training and evaluation](04_TRAINING_AND_EVALUATION.md) | The 9 October pre-registration sentences. H1, H2, and R0–R7 are preserved there, not retired |
| [06_MVP_Technical_Specification.md](../archive/research-preconsolidation-2026-10/06_MVP_Technical_Specification.md) | [MVP specification](05_MVP_SPECIFICATION.md) | Placeholder `music-pref` command lists and proposed interfaces the source does not implement. Those interfaces stay proposed |

No requirement was dropped because it was unimplemented. Where a predecessor and a decision disagree, the consolidated note quotes both and does not invent a winner. Those open items include near-duplicate identity, loudness-mismatch storage, the H2 baseline phrase, the cache layer field, the development repeat rate, and Incompetech commercial training.

## Graphify

Graphify is an optional local navigation aid. Contributing does not require it, and a fresh Git checkout does not contain a generated graph. Files under `graphify-out/` are local artifacts, not sources of project authority. Regenerate them with `graphify update .` when a map would help. Inferred edges are hints: open `source_file` and check it.

`.graphifyignore` keeps `docs/archive/` and `graphify-out/` out of a routine scan. Active source, decisions, and this directory stay in the scan. `graphify docs/archive` is the deliberate archive scan. A completed archive scan writes `docs/archive/graphify-out/`. That directory is gitignored, as is `/graphify-out/`. Do not install Torch or Transformers to refresh the graph.
