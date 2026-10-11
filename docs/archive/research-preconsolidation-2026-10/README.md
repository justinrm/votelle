# Pre-consolidation research, 10 October 2026

These seven notes were the active research directory until the consolidation on 10 October 2026. Their text is the historical evidence. This move did not rewrite their findings, counts, or dated status sentences.

They are not current implementation authority. Source, tests, configs, and `uv.lock` say what runs. Accepted choices are in `docs/decisions/`. Current scientific requirements are the five notes in `docs/research/`. [`docs/STATUS.md`](../../STATUS.md) records what has been implemented and measured.

## How these files relate to the other research layers

| Layer | Where | What it is |
|---|---|---|
| Original 9 October 2026 package | [`../research-v0.1/`](../research-v0.1/00_READ_ME.md) | Executive assessment, literature, feasibility decision, roadmap, agent handoff, risks, and the dated source register. Several package files were kept active at the time and are the notes in this directory |
| Later feasibility research | This directory: the rights audit and the CLAP handoff | Evidence checked 10 October 2026 UTC / 9 October Pacific. The handoff is a pre-attempt contract. It still says no encoder had run |
| Pre-consolidation active notes | This directory, all seven files | The notes that governed method until the consolidated documents replaced them as the active text |
| Current protocol documentation | [`docs/research/`](../../research/README.md) | Governance, P0 listening, encoder and model, training and evaluation, MVP specification, and the reference index |

| Archived note | Current destination | What stays only here |
|---|---|---|
| `01_Data_Feasibility_and_Rights_Audit.md` | [`01_DATA_GOVERNANCE.md`](../../research/01_DATA_GOVERNANCE.md) | The audit's own evidence labels and the wider shortlist beyond P-01 |
| `02_P0_Dataset_and_Listening_Protocol.md` | [`02_P0_LISTENING_PROTOCOL.md`](../../research/02_P0_LISTENING_PROTOCOL.md) | The 9 October procedure wording |
| `03_Audio_Encoder_and_Architecture_Analysis.md` | [`03_ENCODER_AND_MODEL.md`](../../research/03_ENCODER_AND_MODEL.md) | The architecture note's own formulation of the shortlist and the algebra |
| `03_CLAP_Encoder_Feasibility_and_Benchmark_Handoff.md` | [`03_ENCODER_AND_MODEL.md`](../../research/03_ENCODER_AND_MODEL.md) and [`docs/STATUS.md`](../../STATUS.md) | The pre-attempt contract, including the sentence that no encoder had run |
| `04_Dataset_and_Human_Feedback_Strategy.md` | [`01_DATA_GOVERNANCE.md`](../../research/01_DATA_GOVERNANCE.md) and [`02_P0_LISTENING_PROTOCOL.md`](../../research/02_P0_LISTENING_PROTOCOL.md) | Corpus dispositions and label-count planning that the consolidated notes cite rather than replace |
| `05_Training_and_Evaluation_Research_Plan.md` | [`04_TRAINING_AND_EVALUATION.md`](../../research/04_TRAINING_AND_EVALUATION.md) | The 9 October pre-registration text |
| `06_MVP_Technical_Specification.md` | [`05_MVP_SPECIFICATION.md`](../../research/05_MVP_SPECIFICATION.md) | Placeholder `music_pref` / `music-pref` contract language. [Decision 0004](../../decisions/0004-votelle-naming.md) explains those names |

The full source-to-destination map is in the [research index](../../research/README.md).
