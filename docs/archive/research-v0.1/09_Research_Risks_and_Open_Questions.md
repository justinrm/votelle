# 09 — Research Risks and Open Questions

Research v0.1 · October 9, 2026

## Risk register

| Risk | Evidence status | Why it matters | Mitigation / stop trigger |
|---|---|---|---|
| Recreating an existing model | Verified close prior art; novelty of the exact proposed study remains unresolved | A small frozen-encoder MLP is not an original contribution by itself | Reproduce/compare existing work; emphasize personal data and rigorous low-resource evaluation |
| Unclear audio or checkpoint rights | Verified restrictions and incomplete source records | Could prevent the intended open/commercial release | Auditable permissions, isolated research lane, no released weights until ancestry clears |
| Too few independent examples | Expected statistical risk | Many correlated pairs can create false precision | Group-based sampling and intervals; collect more families, not more crops of one song |
| Brief term cancels in linear scoring | Mathematical fact | A nominally conditional model could ignore instructions | Interaction features and explicit shuffled-brief/conditionality tests |
| Personal preference differs from adherence | Task-definition fact; magnitude unknown | Combining labels hides the useful disagreement | Separate questions, scorers and evaluation targets |
| Frozen embedding misses subtle emotion | Unresolved | No head can reconstruct information the representation discarded | Controlled counterexamples, layer/encoder probe, narrow claims before fine-tuning |
| Generator fingerprint shortcut | Plausible, testable | Apparent success may fail on new generators | Exclude identity features; within-generator tests and version holdouts |
| Loudness and production polish bias | Plausible, testable | Aesthetic judgments may reward volume or mastering rather than intent | Consistent audition condition; explicit raw-audio sensitivity audit |
| Genre, language and cultural bias | Supported by representation literature; task impact unmeasured | A niche preference model may fail outside its domain | Report slices and unknowns; do not claim universal music judgment |
| Vocal/instrumental confounding | Plausible; prior datasets have different scopes | Model may learn presence of voice rather than quality or fidelity | Start narrow; label vocals separately; no lyric-fidelity claims |
| Inconsistent listener choices | Expected possibility, not proof that the user is unreliable | Limits predictable signal and changes over time | Delayed repeats, contextual metadata, preserve ties, temporal holdout |
| Invalid public probabilities | Established general ML risk | “0.9” can mislead despite typed output | Null probability until scoped validation; temperature testing and abstention |
| Reward hacking | Expected under optimization pressure | A generator can exploit proxy signals or collapse diversity | Human evaluation independent of reward; no gradient optimization in MVP |
| Short clips treated as whole songs | Scope error | Cannot assess global arc, payoff or repeated lyrics | Explicit excerpt scope; full-song study requires a new protocol |
| Encoder exhausts 8 GB | Estimated resource risk | Slow swap or failures can make collection impractical | Batch 1, CPU, smaller fallback, measured rental decision |
| Repeated test-driven iteration | Procedural risk | Inflates claimed performance | Pre-register, lock test access, refresh confirmation set after exploratory tuning |
| Privacy of taste/history | Data-governance risk | Personal recordings and notes can reveal sensitive context | Pseudonymous labels, private profiles, explicit contribution/release consent |
| Annotation effort dominates | Budget estimate | Free compute does not mean a free study | P0 usability gate, small random seed set, carefully measured active learning |

## Verified observations

The current field includes public music reward models, comparison datasets and instruction-focused benchmarks. Several strong weights are noncommercial. Some dataset metadata and underlying audio carry different terms. These are constraints on project design, not reasons to avoid all research. Detailed sources and component-specific conclusions are in 02–04.

The selected Mac specification is real and adequate for a small cached-feature experiment in principle; runtime and memory remain unmeasured. The mathematical design and parameter counts are derived, not trained-model evidence. No measured accuracy, calibration, user-time saving or generation saving exists for this project yet.

## Unresolved evidence and source conflicts

1. **TuneJury license mismatch:** the advertised permissive CLAP-only head does not clearly relicense the root repository's noncommercial code. Resolve the exact files and grants before using that path commercially.
2. **CMI pseudo-data counts:** the paper's ~110k pseudo samples and current card's larger round-robin count describe different units/releases. Not every row contains a valid label. Count actual label-bearing records after pinning.
3. **SongEval coverage:** the paper/card's full corpus and the visible released row count differ. Do not budget or claim full-dataset reproduction without inspecting the actual pinned release.
4. **MusicPrefs permission:** an explicit dataset license was not located in the inspected card. Do not infer it from a paper, repository, or other project's reuse.
5. **Music Arena eligibility:** the card's monthly totals do not establish how many pairs have both audio files, fit the ten-second scope and satisfy the intended release policy.
6. **HeartCLAP:** paper description was verified, but separate deployable weights and a usable contract were not sufficiently verified for dependency selection.
7. **MusicFM:** permissive model metadata is promising, but the empty card body leaves provenance detail to capture from the repository and specific artifact.
8. **Local deployment:** exact Python/package pins, processor behavior, MPS parity, peak unified memory and extraction latency must be measured.

These issues are identified limitations of the research, not tasks silently assumed complete. Pinning and acquisition gates are the appropriate next steps.

## What would falsify the project thesis?

- The listener's intended target cannot be defined well enough for repeat judgments to be useful, even after improving the brief and audition protocol.
- Strong simple baselines already perform as well as learning within a predeclared meaningful margin, leaving no demonstrated advantage to the specialized model.
- Learning gains disappear under source/prompt grouping or within-generator evaluation.
- Gains occur only on easy degradations, not actual candidate alternatives.
- The necessary data cannot be obtained under acceptable rights at a manageable cost.
- A useful gain requires an encoder or evaluator too large or restricted for the intended deployment.

Falsification should lead to a narrower tool, an upstream contribution, or a documented negative study. It need not make the portfolio work unsuccessful.

## Two worthwhile next research questions

**Few-shot creator adaptation with honest abstention:** Can a compact residual learn repeatable user-specific deviations from a generic ranking method, while abstaining on new styles/generators? Compare against unadapted, nearest-neighbor and regularized linear baselines on future unseen families.

**Adherence–preference disagreement benchmark:** Can a small, rights-cleared dataset reliably distinguish a candidate that follows a brief from one the creator likes more? Evaluate whether separate training targets help and whether existing models systematically collapse the distinction. A carefully documented dataset may be the strongest contribution.

Neither hypothesis assumes a Transformer or a new loss function. Novel method claims require a broader focused literature review after pilot results identify a specific gap.

## Final decision

**CONDITIONAL GO for the research MVP.** Proceed with the offline Cursor foundation and the small labeling pilot. Delay model complexity, full-song evaluation and compute spending until the evidence calls for them. Do not pursue a broad “new music reward model” novelty claim or commercial-ready checkpoint without resolving the specific data and license gates.
