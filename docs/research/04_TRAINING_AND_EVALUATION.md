# Training and evaluation

**Purpose.** This note is the experimental design for Votelle protocol v0.1: what a learned scorer would be asked to beat, how labels and families are kept apart, and which gates would have to pass before a result could be called an improvement. It formalizes the 9 October 2026 training plan. It does not implement that plan.

**Protocol:** v0.1. **Evidence date:** 10 October 2026. Package version remains `0.1.0`. Schema version remains `0.1`.

The live names are Votelle, package `votelle_music`, CLI `votelle-music`, and exception `VotelleError`. Decisions 0001–0003 still write the historical commands `music-pref` and the historical package `music_pref`. Decision 0004 records that split and does not change dataset semantics, grouping, rights, or label meaning. Where this note names a command from those decisions, the historical form is labeled and the current CLI is `votelle-music`.

Model training, calibrated inference, and human preference validation remain unimplemented. The core tree has no CLAP adapter, no trained ranker, and no listening result. A green fixture test is not preference prediction. P-01 is not a training set. Do not run `votelle-music split` on P-01. Decision 0003 states the same prohibition under the historical name `music-pref split`.

## Executive summary

Two hypotheses stay separate. **H1** asks whether a regularized scorer on frozen representations predicts human brief-adherence choices better than the strongest fixed semantic or acoustic baseline on unseen brief and source families. **H2** asks whether a small regularized listener-specific residual improves that listener's later preferences, at 25–200 adaptation judgments, beyond a population or fixed baseline, without folding adherence into an undisclosed combined objective. A clip can match a brief without being preferred, and a preferred clip can miss the brief. Either hypothesis can fail. A negative result is a valid outcome.

The proposed comparison is R0 through R7: a fair-coin reference, frozen cosine, acoustic checks, a low-dimensional mixture, a 1,537-coefficient linear ranker, a 131,201-parameter MLP challenger per target, an eligible external scorer where the governance note permits it, and an optional larger evaluator only if unresolved errors justify the cost. Feature maps and the 10 October 2026 single-clip CPU probe are defined in [03_ENCODER_AND_MODEL.md](03_ENCODER_AND_MODEL.md). This note does not copy those tables. Training settings that the plan adds — regularization grids, the pairwise loss, split rules, metrics, and promotion thresholds — are stated here as proposed methods.

No accuracy, calibration, listening-time saving, or generation saving has been measured for this project. Sample sizes and the five-point promotion bar are proposed research choices. They are not results.

## 1. How to read this note

| Label | Use here |
|---|---|
| Verified implementation | Behavior in `votelle_music` source, configs, tests, or an accepted decision that the code follows |
| Measured | A figure recorded from a named software check or the status record. A fixture split is a software check |
| Estimate | An illustrative calculation under stated assumptions. It is not an observed sample size or an observed gain |
| Proposed method | A procedure, grid, threshold, or model in the training plan or a note it cites. The core tree does not run it |
| Unresolved | A disagreement or a missing specification. This note quotes it and does not choose a winner |

Authority, as recorded in [docs/research/README.md](README.md): source, tests, configs, and `uv.lock` say what runs; [docs/decisions/](../decisions/0001-foundation-choices.md) are accepted choices; the [training plan](../archive/research-preconsolidation-2026-10/05_Training_and_Evaluation_Research_Plan.md) holds scientific requirements the code has not implemented. Wave A consolidations do not override that plan or a decision. `docs/archive/` does not override a later decision. [Project direction](../PROJECT_DIRECTION.md) states long-term intent and yields to an active research document on method.

Rights, consent, and which corpora may enter a lane are in [01_DATA_GOVERNANCE.md](01_DATA_GOVERNANCE.md). Session procedure, question wording, and musical acceptance are in [02_P0_LISTENING_PROTOCOL.md](02_P0_LISTENING_PROTOCOL.md). This note cites those gates. It does not restate their sections.

The research index points here for hypotheses and gates. The predecessor plan is archived and is not current navigation.

## 2. Hypotheses

**Proposed method.** The pre-registered statements are the training plan's. Project direction's shorter gloss is quoted in section 16. Direction says that if it and an active research document disagree about method, the research document wins.

**H1 — Learning adds value.** A regularized scorer on frozen representations predicts human brief-adherence choices better than the strongest fixed semantic/acoustic baseline on unseen brief and source families.

**H2 — Personal adaptation adds value.** A small regularized user-specific residual improves that listener's future preferences beyond a population or fixed baseline, at 25–200 adaptation judgments, without degrading brief adherence through an undisclosed combined objective.

The neural model is a challenger within H1, not an assumption. A useful result may be that the linear method is sufficient, the representation omits the relevant distinction, or the listener's target needs better definition.

Project direction, section 4, is the boundary around those sentences: adherence and preference are separate scores; creator-specific pairwise preference is the first falsifiable preference hypothesis because the protocol records comparative judgments from a named person; one creator does not establish a population taste. The listening protocol owns the N-of-1 session. Population generalization additionally holds out listeners, and it needs the consent rules in the governance note.

The residual form `w_user = w_population + delta_user`, with the size of `delta_user` penalized, is the architecture note's proposed shrinkage, summarized in the encoder note, section 11. If no eligible population model exists, that note says to shrink toward the specified fixed baseline. Cold start uses the generic baseline and makes no claim about the individual. The architecture note's proposed adaptation curve is 0, 25, 50, 100, and 200 judgments, scored on future held-out clips. Those counts are planning points inside H2's 25–200 range plus a zero-shot point. They are not a measured learning curve. A user id is not a feature.

## 3. Pre-registration and locked evaluation

**Proposed method.** Before test labels are unlocked, pre-register:

- the target (adherence or preference; one model per target)
- exclusions
- split hashes
- baseline implementations
- the hyperparameter grid in section 8
- the primary metric in section 10
- the comparison (strongest eligible practical baseline, paired by group)
- the practical improvement threshold in section 13
- a maximum experiment budget

The training plan requires that budget and does not state a number. This note does not import a figure from the archive. The budget stays unresolved until it is written down before the test split is opened.

Labels and evaluation statistics stay hidden from training and from model selection. Fixed pretrained embeddings may be extracted for every split. That extraction is not permission to tune on those labels. The listening protocol allows cache extraction before judgments and forbids showing a model score to the listener.

Active selection, from the dataset strategy: after a random seed set, uncertainty or disagreement sampling stays inside training data; at least 30% of new training queries stay uniformly sampled; selection probabilities are logged; the locked test set is never actively selected. The listening protocol assigns that rule to later training work. It is not a license to reshape a listening session after seeing votes.

Copying encoder rankings into labels and then scoring the encoder on those labels is circular. `label_source` `teacher` is weighted separately and judged on untouched human labels. `synthetic_rule` is a fixture graph edge, not a human preference. Governance owns the distinction and the prohibition on distilling restricted labels into a permissive lane.

## 4. Comparison matrix

**Proposed method.** No row has been trained or scored on human labels.

| ID | Baseline or model | Role in the plan | Label |
|---|---|---|---|
| R0 | Fair random choice, probability 0.5 | Reference accuracy and log loss. A probability-0.5 predictor has expected log loss ln(2) | Proposed method. The ln(2) figure is the mathematical expectation of that reference, not a measured loss |
| R1 | CLAP cosine on the exact brief | Strongest immediate zero-training semantic baseline | Proposed method. Cosine on one technical excerpt is recorded in the encoder note. That cosine is not this baseline on a listening set |
| R2 | Acoustic-only heuristics | Tests whether gross silence or clipping dominates the dataset | Proposed method |
| R3 | Fixed and learned low-dimensional mixtures of cosine and diagnostics | Tests whether a simple engineered combination explains any gains | Proposed method. Separately, the architecture note specifies a four-similarity control for 50–100 pairs and calls it a pilot, not a substitute for the main experiment. This note does not treat that control as the same method as R3 |
| R4 | Linear conditional interaction scorer | Main small trainable model. Feature map in the encoder note, section 9 | Proposed method. Not implemented |
| R5 | 131,201-parameter MLP per target | Tests nonlinear interactions. Count in the encoder note, section 10 | Proposed method. Not implemented |
| R6 | An existing eligible reward scorer. The plan names a TuneJury variant, Audiobox, and CMI-RM as permitted | Avoids comparing only against weak baselines. Restricted resources stay isolated | Proposed method. Eligibility is the governance note's disposition, not a default allowlist |
| R7 | Optional larger audio-language evaluator | Higher-resource ceiling, only if unresolved errors justify the cost | Proposed method |

R2 and R3 must not treat “louder” as inherently better. Hard invalidity checks and measured deviations from explicit constraints are the acoustic evidence. If weights are fitted, the method is learned. It is not labeled deterministic. R1, R3, R4, and R5 run on the same locked examples and the same feature extraction. For a semantic target, a comparison that uses only a quality model is inadequate.

Released scorers may have trained on public benchmarks. Use a documented leave-dataset-out variant, or a fresh original test set. Unknown training overlap is a limitation. It is not evidence of independence. A restricted comparison does not make those weights redistributable. CMI-Pref remains an isolated research lane in the governance note. TuneJury's license is an open archive conflict and is not closed here.

## 5. Ablations and cross-generator tests

**Proposed method.** Required ablations:

- Audio only versus text–audio interaction features, and real briefs versus shuffled briefs.
- Cosine versus linear versus MLP, on identical eligible labels.
- R3 with acoustic features and R3 without them.
- Fixed raw-audio analysis versus the level-matched audition condition. The two conditions stay labeled. They are not pooled as one analysis.
- Same-generator pairs and cross-generator pairs. Generator metadata is excluded from input features.
- At least three fixed training seeds for the neural model. Expand to five only for a borderline promotion decision. The plan names seeds 17, 29, and 43. It does not name the fourth and fifth.

If shuffled briefs perform as well as real briefs, the result does not support a claim of instruction-conditioned preference learning. If performance collapses inside a single generator, the next question is whether the fit learned generator identity. Generator holdout is a separate protocol from the main split: do not merge every same-generator track into one main component. A same-prompt cross-generator comparison after training on that prompt is an easier condition and has to be labeled as such. The frozen challenge set for generator generalization contains an unseen generator or version and unseen brief and source families.

## 6. Leakage-safe splitting

Eligible human labels depend on the governance note. Under `research_only`, `research_training` must be `allowed`. Unknown or denied research training fails `votelle-music validate`. `commercial_ready` requires `allowed` on research training, commercial training, audio release, embedding release, and checkpoint release. A license string does not grant a permission. P-01's recorded snapshot had `research_training` `allowed` and the four release fields `unknown`, with empty brief, clip, and judgment manifests. That permission field does not make P-01 a training set. Decision 0003: P-01 is an acquisition and listening pilot. The split fractions in `configs/p01_piano.json` exist because the config schema requires them.

### What the software does

**Verified implementation.** Decision 0001 and `votelle_music.data.identity`. Identity edges are exact ids and hashes: `source_recording_id`, `song_family_id`, `sha256_original`, `sha256_pcm`, `parent_asset_ids` when the parent is in the manifest, `brief_family_id`, a judgment with its brief and with the assets of `clip_a_id` and `clip_b_id`, and `is_repeat_of`. Connected components are not broken. Component weight is the number of distinct song families in the component. Splits shuffle components with `random.Random(seed)` and assign whole components by weight deficit. A component heavier than the largest split fraction, fewer components than positive splits, or an empty positive split is an error. No partial split file is written. Generator identity is not a main-split edge. The same artist id does not merge families.

`configs/foundation.json` requests fractions 0.6 / 0.1 / 0.1 / 0.2 for train / validation / calibration / test, seed 17. **Measured**, from the 10 October 2026 status record: `votelle-music split` on that fixture config assigned 12 train, 2 validation, 2 calibration, and 4 test components. Those components are fixture families. Fixture judgments used to build graphs are `synthetic_rule` edges. The check does not read P-01 audio. It is not a training split and not a preference result.

Near-duplicate audio is not detected. `identity.py` states that a near-duplicate detector would be required before any real training split. Artist holdout, listener holdout, and generator-generalization protocols are not provided by the main splitter.

### What the plan requires before a real training split

**Proposed method.** The training plan:

1. Build an explicit identity graph linking exact and near duplicates, source recordings, crops, augmentations, alternate renders, covers, stems, and known song families. Link duplicate and paraphrased brief families. Each comparison's two assets and its brief belong to one admissible split group.
2. Assign entire connected components before pair construction. Use the 60/10/10/20 train/validation/calibration/test family targets from the dataset strategy. Repeated votes and mirrored pairs inherit the original group's split.
3. For an artist-generalization experiment, keep known artist identity disjoint. If a single creator supplies all audio, artist-generalization is untested.
4. For personalization, adapt only on earlier allowed judgments and evaluate on later unseen families. For population generalization, also hold out listeners.
5. Fail when group constraints leave too few groups or create a giant component. Recollect or restructure. Do not fall back to random pair splitting.
6. Scan duplicates across external training data and tests, including source URLs and canonical PCM fingerprints. A different file name or codec is not independence. Record unknown identities and the limits of near-duplicate detection.
7. Never use file paths, generator names, dataset source IDs, annotator order, or split IDs as predictive features.

The 60/10/10/20 ratio is the same ratio as the foundation config. The dataset strategy's P1 headcount is a proposed allocation of that ratio: 96 / 16 / 16 / 32 families, and pair slots 576 / 96 / 96 / 192, assuming linked families do not force further grouping. If they do, report the realized counts. The software's weight-deficit assignment does not by itself apply the 96 / 16 / 16 / 32 headcount. P0 is a listening study. The listening protocol says P0 adds no train/test success claim. P0 and preliminary judgments are not the fresh confirmation set.

The plan's near-duplicate link and the implemented exact-edge graph are quoted against each other in section 16. This note does not treat the operator's manual ids as a completed near-duplicate detector.

## 7. Audition condition and train-only transforms

The canonical v0.1 item is a declared 10-second excerpt. Record start, end, and source identity. Do not silently use the first ten seconds of a whole song. Do not transfer a whole-song human judgment to an arbitrary crop. Public labels collected on other durations belong in a separate benchmark protocol, or they need new excerpt-specific annotation. Decision 0001: a clip must be within 1 ms of 10 seconds. The loader does not pad or trim.

**Verified implementation** of the signal path is decision 0002. This note does not redefine it. Preserve the original media. Decode a canonical float waveform. Reject non-finite samples, a bad channel count, zero length, and inadequate duration. Digital silence is a peak absolute amplitude below `1e-8`. Quieter musical material above that threshold is not rejected on that test. Intentional quiet music is not automatically bad. The listening protocol decides which crops are musically usable.

`none_fixture_only` resamples and does not loudness-match. `level_matched` is false. `gain_lufs_v1` is the human audition profile: one constant gain toward **-20 LUFS**, limited by a **-1 dBTP** ceiling, with no compressor or limiter. Acceptance is **±0.1 LU**. If the ceiling selects the gain, `gain_limited_by` is `true_peak`. `loudness_mismatch` is set when the remeasured gated loudness is non-finite or farther than 0.1 LU from -20. Historical command name in that decision: `music-pref validate` records the mismatch as a warning and does not fail the dataset. The current command is `votelle-music validate`. Primary level-matched training and primary level-matched listening use the same declared condition. Where a mismatched clip is stored is unresolved (section 16). A mismatched clip is not silently placed in the primary analysis.

Feature extraction for CLAP, when an adapter exists, uses that same excerpt. Decision 0002 requires `waveform_for_encoder` at 48 kHz, exactly 480,000 finite samples, `pooler_output`, and `dtype` `float32`. The core tree still refuses every encoder except `dummy` / `fixture-v1`. There is no core CLAP adapter. The encoder note owns the 10 October 2026 probe. That probe is one technical excerpt. It is not a trained ranker.

**Proposed method**, and an accepted adapter rule that is not implemented: store the brief token count and reject over-limit text. Do not truncate meaningful constraints. Decision 0002 sets the adapter failure at more than 512 tokens, including special tokens, with truncation left off (`brief_too_long`). The training plan cites the preprocessor config for the limit and does not restate 512 in its own paragraph. The integer used here is the decision's.

### Cache key

**Verified implementation.** `feature_cache_key` hashes canonical JSON of `source_pcm_sha256`, `start_seconds`, `end_seconds`, `preprocessing_sha256`, `encoder_id`, `encoder_revision`, `processor_hash`, `pooling`, and `dtype`. Cached vectors are float32. The training plan asks for separate audio and text entries keyed by source PCM hash, excerpt bounds, preprocessing hash, encoder ID, revision, processor hash, layer/pooling, and dtype, immutable and atomic, recomputed into a new namespace when a key changes. One audio extraction covers every pair that contains that excerpt. The implemented payload has `pooling` and does not have a separate layer field (section 16).

### Transforms fit on training data only

**Proposed method.** Any feature standardizer, PCA, imputer, or learned pooling is fit on training data only. Linear fitting and cached features stay in float32 or float64 as appropriate. Mixed precision is not required for the head. Train-only normalization is not implemented. The dummy encoder and its cache do not fit these transforms.

## 8. Linear model and neural challenger

**Proposed method.** Definitions of the feature map, the text-term cancellation, and the parameter count stay in the encoder note. Settings below are what the training plan adds.

The linear model is architecture B: `phi` has 1,537 coefficients and no bias, as specified in the encoder note, section 9. Naive concatenation of an audio term and a text term cancels the text term under a shared brief. That algebra is cited there and is not recopied. The training configuration is `fit_intercept=False`, L2 pairwise logistic regression, and a scikit-learn non-tie baseline with `C` in {0.01, 0.1, 1, 10}. Solver convergence is checked. The initial scikit-learn reproduction uses strict vote rows with sample weights. It does not use fractional class labels.

Pair construction: `Δphi = phi(A, brief) − phi(B, brief)`, with `y = 1` when the eligible non-tie judgment prefers A and `y = 0` when it prefers B. Both candidates are scored with the same weights. On a strict A/B decision the loss is `-y * logsigmoid(d) - (1 - y) * logsigmoid(-d)`, where `d = s(A) - s(B)`. An additive score offset is not identifiable. Report margins. Do not report an absolute quality percentage. The encoder note's `p_train = sigmoid(d)` is a training probability. It is not a validated public probability.

The MLP is architecture C in the encoder note, section 10: input dimension 2,048, one hidden layer of 64 units, GELU, dropout 0.1, scalar output, **131,201 parameters per target**. Dropout adds no parameters. Two independent models, one per target, are 262,402 parameters when both label sets exist. A shared multi-head trunk is a later ablation. Missing personal labels stay missing. They are not filled from the adherence model or from a generic quality score.

| Setting | Plan value | Label |
|---|---|---|
| Linear penalty | L2, `C` ∈ {0.01, 0.1, 1, 10}, `fit_intercept=False` | Proposed method |
| Neural optimizer | AdamW, learning rate {1e-4, 3e-4, 1e-3}, weight decay {1e-3, 1e-2} | Proposed method. A small predeclared grid, not an open search |
| Batch and epochs | 32 or 64 cached pairs; at most 100 epochs; patience 10 on grouped validation log loss | Proposed method |
| Regularization | Dropout 0.1 and weight decay. No normalization layers and no giant user embeddings in the first neural fit | Proposed method |
| Seeds | 17, 29, 43. Record Python, NumPy, Torch, and sampler states | Proposed method. Seed 17 in `configs/foundation.json` is the fixture split seed. It is not a license to try extra training seeds |
| Device | CPU for fitting heads. Benchmark MPS only if it measurably helps | Proposed method. Encoder MPS parity is unverified in the encoder note |
| Checkpoint rule | Save the best-validation state and the final run metadata. Never pick the best test seed | Proposed method |

PyTorch and Transformers are not dependencies of the core environment. The neural rows above are not a reason to add them to that environment. An authorized training run would be a separate environment under a task-specific authorization. No such run exists.

Architectures D, E, and F in the encoder note stay deferred. Full encoder fine-tuning is outside protocol v0.1.

## 9. Ties, disagreement, repeats, and correlated examples

The listening protocol owns how a session records answers. Stored tokens include `adherence_choice` and `preference_choice` with `A`, `B`, `tie`, and `cannot_judge`, plus per-clip acceptability `yes` / `no` / `unsure`. `cannot_judge` is not a weak vote. A missing answer is not `cannot_judge`. Both unacceptable is not a preference tie. Adherence can disagree with preference. Conflicting answers across sessions stay stored.

**Proposed method** for training, from the plan:

- Primary training and primary accuracy use non-tie judgments.
- Ties and `cannot_judge` stay in the source manifest. Report their frequencies.
- A secondary tie-aware experiment may use Davidson-style tie modeling or a soft 0.5 target. Human indifference is not the same thing as a 50% chance of preferring A in a forced choice. The secondary experiment has to say which of those it is doing.
- “Both bad” informs a separate future acceptability head. It is not turned into a fabricated ranking label. Acceptability labels from the listening protocol are the collection form. The head is not implemented.
- Several votes on one pair stay as individual records. Either fit a soft empirical non-tie win fraction with a capped pair weight under a custom binary cross-entropy, or sample votes while equalizing pair and family influence. Disagreement stays visible. Do not majority-vote it away without an ablation that reports the effect of doing so.
- Presentation order is randomized. The listening protocol's alias-to-clip mapping is unresolved there. Training does not infer it.
- If training mirrors a pair, each mirror receives half the original weight and stays in the same split group. The independent sample count does not double.
- Do not artificially balance held-out outcomes.
- Do not sample a random other song as a known loser. A hard negative is a genuine labeled pair, or a new question asked of a human.
- Six pairs derived from four ranked candidates are not six independent observations. The encoder note states that listwise point. Kendall tau-b and Spearman are computed only on actual comparable human rankings.

Single-annotator labels measure agreement with that annotator. Repeated judgments estimate target stability. Population disagreement is not merely annotation error, and a majority is not an objective music truth. Report per-listener and pooled performance when both exist. Listeners are not removed for disagreeing with a majority. The dataset strategy's repeat rule for later development comparisons, 10–15% in a later session, and P0's locked 10 repeats of 60 pairs, are quoted in section 16. The split rule does not depend on which count is chosen: a repeat inherits the original group's split.

## 10. Metrics, intervals, and power

**Proposed method.** Nothing in this table has been computed on human judgments.

| Question | Metric |
|---|---|
| Does the model choose the human's preferred side? | Accuracy on strict choices, macro-averaged by brief family. Micro accuracy is also reported. Primary metric for the pre-registration |
| Is the probability useful? | Log loss and Brier score on eligible strict votes. Majority labels and random-listener probabilities are different targets |
| Is confidence trustworthy? | Reliability plot, calibration slope and intercept, and coarse-bin expected calibration error with intervals. Expected calibration error alone is not proof |
| Does abstention help? | Accuracy or risk against coverage. Report the excluded count and every abstention reason |
| Are multi-candidate orderings right? | Kendall tau-b or Spearman, only on comparable human rankings |
| Does personalization help? | Within-listener paired improvement against the cold-start or population baseline, on the same future held-out families |
| Does it generalize? | Slices by genre, vocal or instrumental, language, generator and version, source, and prompt family, each with a denominator |
| Is it deployable? | Cold and warm latency, p50 and p95, peak resident set size, device, extraction time, training time, download size, and cache size |
| Is it useful to a listener? | The blind test in section 12 |

An exact tie of model scores receives half credit in forced-choice accuracy and is reported. Abstention is a separate metric. Inference does not have to break ties by an arbitrary rule.

The primary accuracy difference uses paired resampling of brief/source connected components, not of overlapping comparisons. A multi-listener study accounts for crossed listener and family variation with multiway resampling or a hierarchical analysis. Report the scheme, the 95% interval, and the number of independent groups. A McNemar test is appropriate only when its independence assumptions hold. It does not replace grouping.

**Estimate.** The plan's illustrative power calculation assumes independent pairs, about 20% disagreement between two systems, a five-point accuracy gain, 80% power, and a two-sided 5% level: `(1.96 + 0.84)^2 * 0.20 / 0.05^2 ≈ 627` comparisons. The 20% disagreement is an assumption inside that illustration. It is not a measured disagreement rate. Correlated pairs inflate the requirement. Budget a confirmation study from pilot-estimated variance and a group-based simulation. Six hundred comparisons from 100 families are still not 600 independent observations. The plan also says that with only 32 held-out brief families, precision should be expected to be weak. That 32 is the proposed P1 test allocation, not an observed standard error.

The dataset strategy's pair-count table is the same kind of planning range. It is not a result and not a substitute for the promotion gate in section 13.

| Human pairs | Reasonable use named in that note | Not yet defensible, in that note's words |
|---|---|---|
| 50 | Schema mistakes, gross artifacts, unclear targets | Neural superiority, robust calibration, broad personalization |
| 100 | Repeatability, compact features, a preliminary per-user signal | Trustworthy subgroup claims or five-point improvements |
| 500 | Regularized baseline learning curves; an exploratory MLP comparison | Strong conclusions from only a few songs or briefs |
| 1,000 | A more credible scoped evaluation and adaptation curves | Universal vocal, genre, language, or generator generalization |
| 10,000+ | Richer multi-user modeling and stronger subgroup studies | Immunity to bias, leakage, weak rights, or distribution shift |

Independent brief and song families, listener diversity, and label reliability matter more than the raw pair count. A thousand comparisons from a handful of songs are not a thousand independent experiments.

## 11. Calibration and abstention

**Proposed method.** Temperature scaling is the simple calibration candidate. Fit it only on the calibration split, after model selection. It preserves score order. The plan cites Guo et al., 2017, as support for testing temperature scaling, not for assuming it works on this task ([arXiv:1706.04599](https://arxiv.org/abs/1706.04599)).

For a small pilot, return `probability=null`, `calibration_status="unvalidated"`, and an experimental ordering or margin. A training sigmoid is not a validated public probability.

Calibrated output may be enabled only after a predeclared held-out study with all of the following: at least 200 strict comparisons, at least 50 independent families, calibration plots and uncertainty, no material log-loss or Brier deterioration, and a documented population and audio scope. These are minimum project gates. They are not a guarantee of universal calibration. The study has not been run.

Choose abstention thresholds on validation and calibration data, not on test outcomes. Initial abstention covers unsupported scope, missing features, invalid audio, exact score ties, and small margins defined on validation. A warning from feature distance is a heuristic. Evaluate it. Do not present it as certified novelty detection. On an unvalidated generator or domain, calibrated probabilities stay off even if a numerical score can be produced. The MVP specification says these unsupported cases must not be compressed into a zero score. That specification is a proposed contract. The inference path is not implemented.

## 12. Blind human usefulness

**Proposed method.** Session mechanics for ordinary P0 trials stay in the listening protocol. This section is the later selection test in the training plan.

For at least 30–50 entirely new briefs in a pilot, build one fixed candidate pool per brief and give that same pool to every selector. Randomly anonymize the trained model's top choice and the strongest baseline's top choice. The listener compares them and marks each acceptable. Record time. If both selectors choose the same item, record agreement. Do not drop the brief. Balance presentation order. Include delayed repeat trials. Do not show model confidence before the vote.

This tests selection at a fixed candidate count. It does not test fewer generations. A later generation-saving test replays or prospectively runs a pre-registered sequential policy with the same generator and seed stream, the same maximum candidate budget, and blinded acceptability labels. Compare generations until the first acceptable item, and total cost, with failures censored at the budget. A ranker does not reduce the cost of a batch that has already been generated. It can reduce listening effort. It can change a stopping decision only if acceptability is modeled and validated separately.

No such blinded comparison has been run.

## 13. Success, negative results, stop, and promotion

**Proposed method.** Thresholds below are not observed gains.

| Gate | What the plan requires | What it does not mean |
|---|---|---|
| Operational success | Manifests, extraction, training, provenance, honest results, and inference run reproducibly | Learning has added predictive value. This gate can pass when the learned model does not beat the baseline |
| Exploratory signal | A positive point estimate on the proposed P1 set, with group-aware intervals, repeatability checks, and no known leakage | A confirmed improvement. If the interval includes zero, the result is inconclusive |
| Useful improvement | On a fresh locked set, at least 5 percentage points over the strongest eligible practical baseline; the paired group-bootstrap lower 95% bound above zero; no material degradation of the probabilistic scores; a blind usefulness test | A result already in hand. The five-point bar is a promotion threshold |
| Neural contribution | R5 compared with R4 and with the other eligible baselines | A claim that any model beat R0 |
| Parity at lower cost | A predeclared non-inferiority margin, plus measured resource savings | Failure to detect a difference. That failure is not proof of parity |
| Stop architectural escalation | Two predeclared data expansions and reasonable regularization fail to improve on the baseline | A mandate to train a larger network. Diagnose label stability and representation limits, then keep the existing method or narrow the task |

A negative result is a valid outcome. The listener keeps the final choice. Fixture success, a passing ingest, and the single-clip encoder probe do not satisfy any predictive gate in this table.

## 14. Reproducible run artifacts

**Verified implementation** today is the foundation CLI: `votelle-music validate` writes a JSON report, and `votelle-music split` writes component membership, seed, manifest hashes, and provenance. There is no `train` or `evaluate` command. The MVP specification still names those steps with the historical prefix `music-pref`. Decision 0004 left that wording in place.

**Proposed method.** The training plan's minimum record for a future run is local JSON for config, metrics, and predictions; a CSV summary; the code commit; and the environment lock. Also record split hashes, the pre-registered grid, seeds, exclusions, tie counts, abstention reasons, group counts, and the resampling scheme. Save the best-validation checkpoint and do not select it on the test set.

The MVP specification proposes a larger bundle: weights or a coefficient array, `model.json`, `feature_spec.json`, `preprocessing.json`, `normalization.npz`, optional `calibration.json`, `training_manifest.json`, `metrics.json`, a model card, license notices, and SHA-256 checksums. Metadata would record target, scope, listener or population, architecture, trained and frozen parameter counts, seeds, commit, lock hash, split hashes, rights summary, training-data origins, and unsupported inputs. A personal profile defaults to private. Apache-2.0 on Votelle source does not license the training audio, the embeddings, or a trained head. That bundle is not implemented. Governance owns release clearance. `checkpoint_release` on the recorded P-01 snapshot is `unknown`.

## 15. Limitations

- No model has been trained. No calibrated probability has been validated. No human preference result exists.
- The core tree has no CLAP adapter. `votelle-music validate` accepts `dummy` / `fixture-v1` only. The 10 October 2026 CPU probe in the encoder note is one technical excerpt.
- A green foundation test is a software check. The measured 12 / 2 / 2 / 4 fixture split is that kind of check.
- P-01 is not a training set. Do not run `split` on it. Empty judgment manifests are not labels. `research_training: allowed` on a receipt is not a training run.
- Near-duplicate audio, covers, and paraphrased briefs are not detected. Artist, listener, and generator holdouts are not main-split modes.
- H2 on one listener does not establish a population taste.
- Estimated comparison counts, the illustrative 627, the 32-family precision warning, and the five-point bar are not results.
- R6 overlap with public training sets is unknown unless a leave-out or a fresh test is documented.
- Temperature scaling is untested here. Feature-distance warnings are not novelty detectors.
- The maximum experiment budget has no number in the training plan.
- The fourth and fifth neural seeds are unnamed.
- This note does not resolve the quoted disagreements in section 16.

## 16. Quoted disagreements

These statements are both in the tree. This note does not pick a winner and does not rewrite either source.

**Near-duplicate identity.** The training plan says: “Build an explicit identity graph linking exact/near duplicates, source recordings, crops, augmentations, alternate renders, covers, stems and known song families. Link duplicate and paraphrased brief families.” The same plan says: “Record unknown identities and near-duplicate detection limitations.” Decision 0001 says: “Identity edges are exact ids and hashes only. Near-duplicate audio is not detected. Generator identity is not a main-split edge.”

**Loudness-mismatch storage.** The training plan says: “If both cannot be met through gain alone, reduce gain to meet the ceiling, flag the mismatch, and exclude from the primary level-matched analysis or analyze separately.” Decision 0002 says: “`music-pref validate` records that as a warning and does not fail the dataset. The clip row is not rewritten. Exclude the clip from the primary level-matched analysis, or keep it in a separately identified condition.” Decision 0003 says: “A loudness mismatch is `excluded_loudness_mismatch` and is not appended to `clips.jsonl`. A match within 0.1 LU of -20, at or under -1 dBTP, is `primary_level_matched` and is the only result that becomes a clip row.” A storage form for the separately identified condition is unresolved. Primary analysis still excludes the mismatch.

**Phase cancellation.** The training plan says: “Convert to mono and 48 kHz for CLAP with a pinned resampler; log potential phase cancellation as a diagnostic.” Decision 0002 says: “Reject the crop when the mono result is digital silence while a channel is not, or when mono mean-square is below 1% of the channel mean-square (`equal_mean/phase_ratio_0.01/v1`).” The decision is the accepted preparation rule. The plan's “log” sentence is not rewritten here into that reject rule, and the reject rule is not relaxed into a log line.

**H2's baseline phrase.** The training plan says a residual improves future preferences “beyond a population or fixed baseline.” Project direction's section 5 gloss says: “A small listener-specific adjustment improves later preference predictions (H2).” Its section 4 says the direct test is prediction “better than the fixed baseline, without folding adherence into the same objective.” Direction also says: “If this note and an active research document disagree about method, the research document wins.” The pre-registered H2 sentence used in section 2 is the training plan's. The gloss is left on the record.

**Cache key and layer.** The training plan keys embeddings by “`(source PCM hash, excerpt bounds, preprocessing hash, encoder ID, revision, processor hash, layer/pooling, dtype)`.” The implemented `feature_cache_key` payload fields are `source_pcm_sha256`, `start_seconds`, `end_seconds`, `preprocessing_sha256`, `encoder_id`, `encoder_revision`, `processor_hash`, `pooling`, and `dtype`. There is no separate layer field.

**Development repeat rate.** The dataset strategy's stage table, with the listening note, sets P0 at 10 repeats of 60 unique pairs. The same strategy says: “Repeat 10–15% of development comparisons in a later session.” Ten of 60 is above 15%. The listening protocol, section 13, leaves which sentence governs later development stages unresolved. This note does not choose a rate.

**Incompetech commercial training, as it bounds a future lane.** The governance note quotes the feasibility audit's commercial-ML cell, “Permitted under BY grant + training offer, after review,” against the same audit's instruction that “Review” must not be serialized as `allowed`, and against the status snapshot in which commercial training and the release fields were `unknown`. Decision 0001 says a license string never grants a permission. The governance note leaves those fields unknown. This training note does not treat the catalog offer as `commercial_training: allowed`.

## 17. Sources

Evidence date 10 October 2026. Predecessor files below are the archived sources of the requirements in this note. They are not current navigation.

| Path | What this note took from it |
|---|---|
| `docs/archive/research-preconsolidation-2026-10/05_Training_and_Evaluation_Research_Plan.md` | H1, H2, R0–R7, ablations, leakage rules, loss, grids, metrics, calibration, promotion, blind test, run records. 9 October 2026. Left in place |
| `docs/research/03_ENCODER_AND_MODEL.md` | 1,537-feature map, text-term cancellation, 2,048-d MLP, 131,201-parameter count, separate targets, 10 October 2026 probe citation. Tables not copied |
| `docs/archive/research-preconsolidation-2026-10/03_Audio_Encoder_and_Architecture_Analysis.md` | Design authority the encoder note names for architecture B and C, the shrinkage formula, and the 0 / 25 / 50 / 100 / 200 curve |
| `docs/archive/research-preconsolidation-2026-10/04_Dataset_and_Human_Feedback_Strategy.md` | 60/10/10/20 as 96 / 16 / 16 / 32 families, active-sampling rule, label-count heuristics, 10–15% development repeats |
| `docs/research/01_DATA_GOVERNANCE.md` | Eligible permissions, P-01 is not a training set, restricted lanes, consent. Not restated |
| `docs/research/02_P0_LISTENING_PROTOCOL.md` | Session procedure, stored choice tokens, P0 has no train/test claim. Not restated |
| `docs/archive/research-preconsolidation-2026-10/06_MVP_Technical_Specification.md` | Proposed bundle and historical `music-pref` command names. Broader contract. Training commands are not implemented |
| `docs/decisions/0001-foundation-choices.md` | Exact identity edges, split failure rule, silence threshold, cache-key fields, `synthetic_rule` |
| `docs/decisions/0002-audition-normalization.md` | `gain_lufs_v1`, -20 LUFS, -1 dBTP, ±0.1 LU, phase-ratio reject, 512-token adapter rule |
| `docs/decisions/0003-p01-ingestion.md` | P-01 is not a training set. Historical `music-pref split` prohibition. Mismatch not appended to `clips.jsonl` |
| `docs/decisions/0004-votelle-naming.md` | Votelle, `votelle_music`, `votelle-music`, `VotelleError`. Historical names retained |
| `docs/STATUS.md` | Unimplemented training, fixture split counts, probe boundary. Main-checkout text of 10 October 2026 |
| `docs/PROJECT_DIRECTION.md` | H1/H2 boundary only. Yields on method |
| `src/votelle_music/data/identity.py` | Exact edges and the near-duplicate comment |
| `src/votelle_music/features/cache.py` | Implemented cache-key payload |
| `configs/foundation.json` | Split fractions 0.6 / 0.1 / 0.1 / 0.2 and seed 17 on fixtures |

Current navigation points at this note. The predecessor remains archived and unchanged.
