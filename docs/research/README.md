# Active research

Protocol v0.1 notes that still govern method, rights, and promotion gates. Passing tests do not retire a requirement that the code has not implemented.

[Project direction](../PROJECT_DIRECTION.md) describes long-term project intent. It does not change these notes, the decisions, or what the software does.

Labels below are an index. The documents themselves were not rewritten, so a section inside a file may still say "proposal" or "verified" in its own words.

| File | Index |
|---|---|
| [03_Audio_Encoder_and_Architecture_Analysis.md](03_Audio_Encoder_and_Architecture_Analysis.md) | Proposed model. Frozen CLAP, then a regularized linear pairwise scorer, then a neural challenger. Not implemented |
| [04_Dataset_and_Human_Feedback_Strategy.md](04_Dataset_and_Human_Feedback_Strategy.md) | Rights and labeling requirements. The rights profile is implemented. The listening study is not |
| [05_Training_and_Evaluation_Research_Plan.md](05_Training_and_Evaluation_Research_Plan.md) | Experiment plan and success gates. Not implemented |
| [06_MVP_Technical_Specification.md](06_MVP_Technical_Specification.md) | Product and data contract. Manifests, excerpts, and the dummy encoder exist. Training, calibration, and inference do not |
| [01_Data_Feasibility_and_Rights_Audit.md](01_Data_Feasibility_and_Rights_Audit.md) | Source audit and the P-01 shortlist. Ingest does not turn this audit into a grant |
| [02_P0_Dataset_and_Listening_Protocol.md](02_P0_Dataset_and_Listening_Protocol.md) | Listening protocol. Not run |
| [03_CLAP_Encoder_Feasibility_and_Benchmark_Handoff.md](03_CLAP_Encoder_Feasibility_and_Benchmark_Handoff.md) | Unrun CPU probe. No weights downloaded and no benchmark recorded |

Accepted engineering choices that narrowed these notes are in `docs/decisions/`. Current implementation status is in `docs/STATUS.md`.

## Authority

1. Source, tests, `configs/`, and `uv.lock` establish what the software does.
2. `docs/decisions/` establish accepted engineering choices.
3. This directory establishes scientific requirements and experimental gates the code does not yet meet.
4. `docs/PROJECT_DIRECTION.md` states long-term project intent. It does not override items 1–3, change protocol v0.1, or turn a hypothesis into an implemented capability.
5. `docs/archive/` is evidence and earlier rationale. It does not override a later decision or the code.
6. `graphify-out/` is a navigation map. An inferred edge is not a project fact. Follow `source_file` and check the file.

## Graphify

`.graphifyignore` keeps `docs/archive/` and `graphify-out/` out of a routine scan. Active source, decisions, and this directory stay in the scan.

`graphify update .` on 2026-10-10 refreshed `graphify-out/`: 419 nodes, 1320 edges, no LLM tokens. That graph includes Python symbols and headings from this directory, the decisions, `README.md`, and `AGENTS.md`. It does not include `docs/archive/`. Inferred edges are hints.

`graphify .` is the full rebuild. This session did not run it. `graphify docs/archive` is the deliberate archive scan. That command stopped here because no semantic-extraction key was set, after creating nothing but an empty cache, which was deleted. A completed archive scan writes `docs/archive/graphify-out/`, and that directory is gitignored. Do not install Torch or Transformers to refresh the graph.
