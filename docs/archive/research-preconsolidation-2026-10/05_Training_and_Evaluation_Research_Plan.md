# 05 — Training and Evaluation Research Plan

Research v0.1 · October 9, 2026 · Authority for experimental design and promotion gates

## Questions and pre-registered hypotheses

**H1 — Learning adds value:** a regularized scorer on frozen representations predicts human brief-adherence choices better than the strongest fixed semantic/acoustic baseline on unseen brief and source families.

**H2 — Personal adaptation adds value:** a small regularized user-specific residual improves that listener's future preferences beyond a population or fixed baseline, at 25–200 adaptation judgments, without degrading brief adherence through an undisclosed combined objective.

The neural model is a challenger within H1, not an assumption. A useful result may be that the linear method is sufficient, the representation omits the relevant distinction, or the listener's target needs better definition.

Pre-register the target, exclusions, split hashes, baseline implementations, hyperparameter grid, primary metric, comparison, practical improvement threshold and maximum experiment budget before unlocking test labels.

## Baselines and experiment matrix

| ID | Baseline / model | Why it is necessary |
|---|---|---|
| R0 | Fair random choice / probability 0.5 | Reference accuracy and log loss; expected loss ln(2) |
| R1 | CLAP cosine on the exact brief | Strongest immediate zero-training semantic baseline |
| R2 | Acoustic-only heuristics | Tests whether gross silence/clipping dominates the dataset |
| R3 | Fixed and learned low-dimensional mixtures of cosine and diagnostics | Tests whether a simple engineered combination explains any gains |
| R4 | Linear conditional interaction scorer from 03 | Main small trainable model |
| R5 | 131,201-parameter MLP per target | Tests value of nonlinear interactions |
| R6 | Existing eligible reward scorer; TuneJury variant / Audiobox / CMI-RM as permitted | Avoids comparing only to weak baselines; isolate restricted resources |
| R7 | Optional larger audio-language evaluator | Higher-resource ceiling, only if unresolved errors justify cost |

R2 and R3 must never treat “louder” as inherently better. Define hard invalidity checks and measured deviations from explicit constraints. If weights are fitted, label the method learned, not deterministic. Run R1, R3, R4 and R5 on the same locked examples and feature extraction. For a semantic target, comparing only with a quality-only model is inadequate.

Existing released scorers may have trained on public benchmarks. Use leave-dataset-out variants where documented, or a fresh original test set. Unknown training overlap is a limitation, not evidence of independence. A restricted comparison result does not make those weights redistributable.

### Required ablations

- Audio only versus text–audio interaction features; real versus shuffled briefs.
- Cosine versus linear versus MLP, using identical eligible labels.
- With versus without acoustic features in R3.
- Fixed raw-audio analysis versus the level-matched audition condition.
- Same-generator and cross-generator pairs, with generator metadata excluded from input features.
- At least three fixed training seeds for the neural model; expand to five only for a borderline promotion decision.

If shuffled briefs perform just as well, do not claim instruction-conditioned preference learning. If performance collapses within a single generator, investigate learning generator identity rather than useful musical distinctions.

## Preprocessing and feature caching

The canonical v0.1 item is a **declared 10-second excerpt**. Record start/end time and source identity; never silently use the first ten seconds of a whole song. Do not transfer a whole-song human judgment to an arbitrary crop. Public labels collected on different durations belong in separate benchmark protocols or require new excerpt-specific annotation.

Preserve original media. Decode a canonical float waveform, verify finite samples, channel count, nonzero length and adequate duration, and calculate original-signal diagnostics. Create the separately versioned audition derivative with a fixed gain-only loudness-matching procedure, target -20 LUFS and true-peak ceiling -1 dBTP. If both cannot be met through gain alone, reduce gain to meet the ceiling, flag the mismatch, and exclude from the primary level-matched analysis or analyze separately. Do not use compression/limiting to disguise a degraded candidate. Digital silence is invalid; intentional quiet music is not automatically bad.

Use the same declared audition condition for feature extraction and human labels. Convert to mono and 48 kHz for CLAP with a pinned resampler; log potential phase cancellation as a diagnostic. Exactly ten seconds avoids the processor's default random cropping, which must not affect inference. Store the brief token count and reject over-limit text rather than truncating meaningful constraints. [S50](https://huggingface.co/laion/larger_clap_music/blob/main/preprocessor_config.json)

Cache normalized audio/text embeddings separately by `(source PCM hash, excerpt bounds, preprocessing hash, encoder ID, revision, processor hash, layer/pooling, dtype)`. Audio needs one extraction per unique excerpt, regardless of how many pairs contain it. Disk cache is immutable and atomic. If a key changes, recompute into a new namespace.

Fit any feature standardizer, PCA, imputer or learned pooling on training data only. Fixed pretrained embeddings may be extracted for all splits, but labels and evaluation statistics must remain hidden from training/model selection. For numerical stability, keep linear fitting and cached features in float32/float64 as appropriate; no mixed precision is necessary for the head.

## Leakage-safe partitioning

1. Build an explicit identity graph linking exact/near duplicates, source recordings, crops, augmentations, alternate renders, covers, stems and known song families. Link duplicate and paraphrased brief families. Each comparison's two assets and its brief belong to one admissible split group.
2. Assign entire connected components before pair construction; use the 60/10/10/20 train/validation/calibration/test family targets from 04. Repeated votes and mirrored pairs inherit the original group's split.
3. Keep known artist identity disjoint for an **artist-generalization experiment**. If a single creator supplies all audio, say that artist-generalization is untested. Do not merge every same-generator track into one main split group; generator holdout is a distinct protocol.
4. For generator generalization, freeze a separate challenge set containing an unseen generator/version and unseen brief/source families. A same-prompt cross-generator comparison after training on that prompt measures a different, easier condition and must be labeled accordingly.
5. For personalization, train/adapt only on earlier allowed judgments and evaluate on later unseen families. For population generalization, additionally hold out listeners.
6. Fail explicitly when group constraints leave too few groups or create a giant connected component. Recollect/restructure data; do not fall back to random pair splitting.

Run duplicate scans across external training data and tests, including source URLs and canonical PCM fingerprints. A different file name or codec is not independence. Record unknown identities and near-duplicate detection limitations. Never use file paths, generator names, dataset source IDs, annotator order, or split IDs as predictive features.

## Training configuration

| Component | Initial configuration / rationale |
|---|---|
| Linear model | `fit_intercept=False`; L2 pairwise logistic; scikit-learn non-tie baseline with C ∈ {0.01, 0.1, 1, 10}; solver convergence checked |
| Pair construction | Δphi = phi(A,brief) − phi(B,brief); y=1 for A, 0 for B |
| MLP | Design C in 03, one target per model, input dimension 2,048 |
| Neural optimizer | AdamW, LR {1e-4, 3e-4, 1e-3}, weight decay {1e-3, 1e-2}; tune a small predeclared grid, not unlimited search |
| Batch / epochs | 32 or 64 cached pairs; maximum 100 epochs, patience 10 on grouped validation log loss |
| Regularization | Dropout 0.1, L2/weight decay; no normalization layers or giant user embeddings initially |
| Seeds | 17, 29, 43; record Python, NumPy, Torch and sampler states |
| Device | CPU for fitting heads; benchmark MPS only if it measurably helps |
| Checkpoints | Save best-validation state and final run metadata; never pick best test seed |
| Tracking | Local JSON config/metrics/predictions, CSV summary, code commit and environment lock |

Score each candidate through the same weights. The loss on strict A/B decisions is `-y*logsigmoid(d) - (1-y)*logsigmoid(-d)`, with d=sA−sB. Candidate score offsets are not identifiable; report margins, not an absolute “quality percentage.”

Primary training and accuracy use non-tie judgments. Preserve ties and cannot-judge in the source manifest and report their frequencies. A secondary tie-aware experiment can use Davidson-style tie modeling or a soft 0.5 target, explicitly acknowledging that human indifference is not the same as a 50% chance of preferring A in a forced choice. “Both bad” informs a separate future acceptability head, not a fabricated ranking label.

For multiple votes on one pair, retain individual records. Either fit a soft empirical non-tie win fraction with capped pair weight using a custom BCE objective, or sample votes while equalizing pair/family influence. The initial scikit-learn reproduction uses strict vote rows with weights, not unsupported fractional class labels. Keep disagreement visible and do not majority-vote it away without an ablation.

Balance A/B presentation through randomized order. If training uses mirrored augmentation, each mirrored item receives half the original weight and remains in the same group; the independent sample count does not double. Do not artificially balance held-out outcomes. Do not sample a random other song as a known preference loser. Hard-negative selection must use genuine labeled pairs or create new questions for a human.

## Evaluation metrics and uncertainty

| Question | Metric / interpretation |
|---|---|
| Does the model choose the human's preferred side? | Accuracy on strict choices, macro-averaged by brief family; micro accuracy additionally reported |
| Is probability prediction useful? | Log loss and Brier score on all eligible strict votes; distinguish majority labels from random-listener probabilities |
| Is confidence trustworthy? | Reliability plot, calibration slope/intercept and coarse-bin ECE with intervals; ECE alone is not proof |
| Does abstention help? | Accuracy/risk versus coverage curve; report excluded count and all abstention reasons |
| Are multi-candidate orderings right? | Kendall tau-b / Spearman only on actual comparable human rankings; not arbitrary comparisons of unconnected items |
| Does personalization help? | Within-listener paired improvement versus cold-start/population baseline on identical future held-out families |
| Does it generalize? | Per-genre, vocal/instrumental, language, generator/version, source and prompt-family slices with denominators |
| Is it deployable? | Cold/warm latency, p50/p95, peak RSS and device allocation, extraction/training time, download/cache size |
| Is it useful? | Human acceptability of selected candidate, listening time, and generation budget under a fixed policy |

Exact model score ties receive half credit in forced-choice accuracy and are reported; abstention is a separate metric. Inference need not break ties arbitrarily.

Use paired resampling of **brief/source connected components**, not individual overlapping comparisons, for the primary accuracy difference. For a multi-user study, account for crossed listener and family variation with multiway resampling or an appropriate hierarchical analysis. Report the resampling scheme, 95% interval and number of independent groups. A simple McNemar test is only appropriate when comparisons satisfy its independence assumptions; it is not a substitute for grouping.

Single-annotator labels measure agreement with that annotator. Repeated judgments estimate target stability. Population disagreement is not merely annotation error, and majority agreement is not an objective music truth. Report both per-listener and pooled performance when applicable.

## Calibration and abstention policy

Temperature scaling is a sensible simple calibration candidate, fitted only on the calibration split after model selection; it preserves score ordering. Standard calibration research supports testing it, not assuming it works on this task. [S42](https://arxiv.org/abs/1706.04599)

For small pilots, return `probability=null`, `calibration_status="unvalidated"`, and an experimental ordering/margin. A chosen training sigmoid is not a validated public probability. Calibrated output may be enabled only after a predeclared held-out study covering at least 200 strict comparisons across at least 50 independent families, with calibration plots and uncertainty, no material log-loss/Brier deterioration, and a documented applicable population and audio scope. These are minimum project gates, not guarantees of universal calibration.

Choose abstention thresholds on validation/calibration data, not test outcomes. Initially abstain for unsupported scope, missing features, invalid audio, exact score ties, and validation-defined small margins. Out-of-distribution warnings based on feature distance are heuristics; evaluate them and do not present them as certified novelty detection. Disable calibrated probabilities on an unvalidated generator/domain even if a numerical score can be produced.

## Minimum evidence and promotion rules

**Operational success:** manifests, extraction, training, provenance, honest results and inference work reproducibly. This can pass even if learning adds no predictive benefit.

**Exploratory signal:** a positive point estimate on P1 with group-aware intervals, repeatability checks and no known leakage. If the interval includes zero, the result is inconclusive. With only 32 held-out brief families, expect weak precision.

**Claim of useful improvement:** on a fresh locked set, target ≥5 percentage points over the strongest eligible practical baseline, with the paired group-bootstrap lower 95% bound above zero, corroborated by no material probabilistic-score degradation and a blind usefulness test. To claim a neural contribution, compare R5 against R4 as well as other baselines. To claim parity with lower cost, predefine a non-inferiority margin and evaluate resource savings; failure to detect a difference is not proof of parity.

Illustrative power calculation: for independent pairs and approximately 20% disagreement between two systems, detecting a five-point accuracy gain with 80% power at a two-sided 5% level needs roughly `(1.96+0.84)^2*0.20/0.05^2 ≈ 627` comparisons. Correlated pairs inflate requirements. Use pilot-estimated variance and group-based simulation to budget confirmation; 600 comparisons from 100 families are still not 600 independent observations.

If two predeclared data expansions and reasonable regularization fail to improve over the baseline, stop architectural escalation. Diagnose label stability and representation limitations, then use the existing method or narrow the task.

## Blind listening validation and generation efficiency

For at least 30–50 entirely new briefs in a pilot, assemble the same fixed candidate pool for every selector. Randomly anonymize the trained model's top choice and the strongest baseline's top choice. Ask the listener to compare and mark each acceptable; record time. If both selectors choose the same item, record agreement rather than silently dropping the brief. Balance presentation order and include delayed repeat trials. Do not show model confidence before the vote.

This tests **selection at fixed N**, not fewer generations. To test generation savings later, replay or prospectively evaluate a pre-registered sequential policy with the same generator/seed stream, maximum candidate budget and blinded acceptability labels. Compare generations-to-first-acceptable and total cost, including failures censored at the budget. A ranker cannot reduce the cost of an already generated batch; it can reduce listening effort, and may improve stopping decisions only if acceptability is separately modeled and validated.

No experimental results are asserted in this package. All thresholds, configurations and sizes here are proposed research choices.
