# Archive

Historical research for protocol v0.1. These files explain earlier rationale, citations, and handoffs. They do not override `docs/decisions/`, the source tree, or the active notes in `docs/research/`.

Two historical layers live here. Neither overrides `docs/decisions/`, the source tree, or the active notes in `docs/research/`.

`research-v0.1/` is the original October 9, 2026 package that was archived before consolidation: the executive assessment, literature review, feasibility decision, roadmap, agent handoff, risk note, and dated source register. Body text is unchanged except the four reading-order links in `00_READ_ME.md`. Those links now open the pre-consolidation copies, because the files they named are no longer in `docs/research/`.

`research-preconsolidation-2026-10/` holds the seven notes that stayed active until 10 October 2026, including the later rights audit and the CLAP handoff. Their findings were not rewritten. The [preface](research-preconsolidation-2026-10/README.md) states how they relate to the October 9 package and to the current research notes. The lookup copy of the source register is [`docs/research/REFERENCES.md`](../research/REFERENCES.md). `10_Source_Register.md` remains the dated original.


| File | Why it is here |
|---|---|
| `00_READ_ME.md` | Original reading order and decision register D01–D09 |
| `01_Executive_Feasibility_Assessment.md` | Conditional-go verdict before implementation |
| `02_Literature_and_Competitive_Landscape.md` | Prior-art review |
| `04_Feasibility_Decision_and_Integration_Handoff.md` | Data and encoder go/no-go after the rights audit. Its loudness wording was a proposal. `docs/decisions/0002-audition-normalization.md` is the accepted procedure |
| `07_Development_Roadmap_and_Budget.md` | Schedule and cost estimates |
| `08_Cursor_Agent_Implementation_Handoff.md` | First-session handoff. It still says `src/music_pref/` |
| `09_Research_Risks_and_Open_Questions.md` | Open risks. These are not closed decisions |
| `10_Source_Register.md` | Dated citation register, October 9, 2026 Pacific. Active lookup copy: [`docs/research/REFERENCES.md`](../research/REFERENCES.md) |

The original delivery ZIP matched these eleven package files byte for byte (SHA-256 `c1c48dc41f3a5676ae1db2de6c9c45a5f9a602457be0e2a6afc9aab534f643c5`). It was removed from the working tree. Git history still has the blob.

Graphify does not index this directory. Read a file here on purpose, or run `graphify` on `docs/archive/` when a historical question needs a graph.
