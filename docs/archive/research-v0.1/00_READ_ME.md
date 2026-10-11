# Music Preference Model — Research Package

Prepared for Justin Merwin · Research v0.1 · October 9, 2026 (Pacific)

**Decision: CONDITIONAL GO for a small, baseline-first research project.** A generic music reward network already has close public precedents. The useful next experiment is whether a modest, rights-cleared, creator-specific dataset improves short-clip decisions beyond frozen text–music similarity and existing reward models.

This package contains research and specifications, not an implemented or validated model. No training runs, paid jobs, model downloads, or listening experiments were performed. Hardware figures are planning estimates unless explicitly identified as a published specification. Public availability was checked through official repositories, model cards, and papers; successful local execution remains a gate.

## Reading order

1. Read **01** for the verdict and answers to the ten final questions.
2. Read **04** before acquiring audio; rights and labeling are the critical dependencies.
3. Read **03** and **05** to understand what is being trained and what would count as success.
4. Review **06**, then give **08** to Cursor with the package available in its workspace.
5. Use **02**, **07**, **09**, and **10** as research, planning, risk, and source references.

| Document | Role / authoritative subject |
|---|---|
| [01_Executive_Feasibility_Assessment.md](01_Executive_Feasibility_Assessment.md) | Recommendation, project positioning, final decision answers |
| [02_Literature_and_Competitive_Landscape.md](02_Literature_and_Competitive_Landscape.md) | Prior art, conflicting findings, build versus contribute |
| [03_Audio_Encoder_and_Architecture_Analysis.md](../research-preconsolidation-2026-10/03_Audio_Encoder_and_Architecture_Analysis.md) | Encoder selection, mathematical architecture, model sizes |
| [04_Dataset_and_Human_Feedback_Strategy.md](../research-preconsolidation-2026-10/04_Dataset_and_Human_Feedback_Strategy.md) | Data rights policy, acquisition, annotation and dataset sizes |
| [05_Training_and_Evaluation_Research_Plan.md](../research-preconsolidation-2026-10/05_Training_and_Evaluation_Research_Plan.md) | Splits, experiments, calibration, statistical claims and success gates |
| [06_MVP_Technical_Specification.md](../research-preconsolidation-2026-10/06_MVP_Technical_Specification.md) | Product scope, data and inference contracts, operational requirements |
| [07_Development_Roadmap_and_Budget.md](07_Development_Roadmap_and_Budget.md) | Schedule assumptions, hardware estimates, spending scenarios |
| [08_Cursor_Agent_Implementation_Handoff.md](08_Cursor_Agent_Implementation_Handoff.md) | Repository boundaries, implementation sequence and first-session prompt |
| [09_Research_Risks_and_Open_Questions.md](09_Research_Risks_and_Open_Questions.md) | Uncertainties, limitations and reasons to pivot |
| [10_Source_Register.md](10_Source_Register.md) | Primary-source links and evidence status |

## Decision register

These are recommendations for this research MVP, not previously approved project canon.

| ID | Decision | Authority |
|---|---|---|
| D01 | Start with explicitly selected 10-second excerpts; do not infer whole-song quality | 06 |
| D02 | Use frozen music CLAP; use the smaller unfused CLAP as the resource fallback | 03 |
| D03 | Train a regularized linear pairwise scorer before the 131,201-parameter neural alternative | 03 |
| D04 | Keep measured audio properties, brief adherence, and personal preference distinct | 06 |
| D05 | Use a rights-cleared data lane; isolate restricted research resources | 04 |
| D06 | Split related recordings and brief families together; lock evaluation before training | 05 |
| D07 | Return raw margins initially; expose probabilities only after scoped calibration validation | 05 / 06 |
| D08 | No generator, DAW, SaaS, or agent system in v0.1 | 06 |
| D09 | A null result is a valid research deliverable; neural complexity must earn promotion | 05 |

## Evidence conventions

- **Verified:** the cited primary source directly states the fact; this does not imply independent replication.
- **Derived:** arithmetic from published specifications or from this proposed design.
- **Estimate:** a planning range, requiring measurement on the actual machine.
- **Proposal / hypothesis:** a design choice or experiment, not an established result.
- **Unresolved:** information was missing, contradictory, inaccessible, or insufficiently specific.

Source review was completed October 10, 2026 UTC, corresponding to October 9 Pacific. Live repository pages can change. The implementation must pin immutable revisions and retain license snapshots before using artifacts. Source identifiers in the documents map to 10_Source_Register.md.
