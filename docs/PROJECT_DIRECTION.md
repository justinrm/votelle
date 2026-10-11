# Project direction

October 10, 2026. Authoritative for long-term project intent. Research protocol v0.1 is unchanged. This note does not override source behavior, accepted decisions, or the active research documents.

## 1. Project purpose

Music systems can generate, retrieve, and rank many candidates. Deciding which candidate fits a creative intent, or which one a particular person would rather hear, is a different problem from producing the audio.

Votelle investigates whether compact, specialized models can make those music-aware decisions well enough to help larger music-generation systems, recommendation methods, and related applications. The specialized model is meant to complement those systems. Replacing a music generator is outside the project.

The long-term ambition is to develop compact, adaptable music-intelligence and decision models that support more informed, reliable, and efficient decisions where a larger system would otherwise rely on a generic score, another full listen, or an unsupported guess. Whether any of that is achievable remains a research question.

## 2. Foundational research philosophy

The architectural inspiration is compact, task-specialized decision-making, in the spirit of systems such as Jev: a small model asked to make a bounded decision and to expose uncertainty. Jev's documented interface is text and structured content. No validated music-waveform evaluator was established for it, and Votelle does not reproduce its internals. The v0.1 representation is frozen music CLAP. Text-only Jev is not that encoder. The distinction is recorded in the [literature note](archive/research-v0.1/02_Literature_and_Competitive_Landscape.md) and the [encoder note](research/03_ENCODER_AND_MODEL.md).

The project does not commit to a proprietary model, an integration partner, or an untested architecture.

These quantities are different, and a claim about compactness has to name which one was measured:

| Concern | Meaning in this project |
| --- | --- |
| Trainable model size | Parameters updated from Votelle's own labels. The v0.1 plan starts with a regularized linear head. A small neural scorer is a later challenger. |
| Inference and representation cost | The cost of producing a decision, including any frozen encoder. A small head on a large encoder can still be expensive to run. |
| Decision quality | Whether the score matches the declared human judgment on held-out material. |
| Adaptability | Whether a modest amount of new feedback changes predictions for that listener or creator. |
| Reliability and uncertainty | Whether the system can abstain when the excerpt, the labels, or the domain do not support a decision. |

A small scoring head backed by a large frozen encoder is the v0.1 research design. That design is not, by itself, an independently lightweight end-to-end model.

## 3. Long-term research directions

The following are possible later directions. Each one needs its own evidence. None is an approved build, a performance target, or a demonstrated application.

- **Creative-intent and adherence evaluation.** Ask whether a candidate matches a stated brief, using labels collected for that question.
- **Personal preference learning.** Ask whether limited comparative feedback predicts what a particular listener or creator prefers later.
- **Generator-independent candidate selection.** Compare candidates without binding the evaluator to one generator's training loop.
- **Specialized reward or evaluation components.** Offer a score or a ranking that a larger model might consume, after that score has been validated for that use.
- **Recommendation and personalization support.** Inform ranking or personalization methods. A recommender is a separate system.
- **Efficient inference, feature reuse, and possible distillation.** Reuse cached representations. Consider distillation only after a measured cost problem remains and the decision itself has evidence.
- **Reliable abstention and scope-aware decisions.** Decline a judgment when the input, the training support, or the excerpt scope does not justify one.

## 4. Current research focus — v0.1

The accepted experiment asks whether a compact learned scoring model, on frozen audio and text representations, improves prediction of two separate targets:

1. Creative-brief adherence.
2. Individual listener or creator preference.

A clip can match a brief without being preferred, and a preferred clip can miss the brief. The two scores stay separate.

Creator-specific pairwise preference is the first falsifiable preference hypothesis because the protocol records comparative judgments from a named person, on declared excerpts, against fixed baselines. One creator does not establish a population taste. The direct test is whether a regularized listener-specific adjustment predicts that person's later choices on unseen families better than the fixed baseline, without folding adherence into the same objective. Adherence is the paired hypothesis, tested on its own labels. Either hypothesis can fail. A negative result is a valid outcome. The pre-registered statements are H1 and H2 in the [training and evaluation note](research/04_TRAINING_AND_EVALUATION.md).

The proposed progression is:

1. Frozen CLAP audio and text representations.
2. Fixed cosine similarity and other simple baselines.
3. Regularized linear pairwise ranking.
4. A small neural challenger only when the data and the baselines justify it.
5. Leakage-safe evaluation, uncertainty analysis, and human validation.

The unit of analysis remains an explicitly selected ten-second excerpt. Full-song evaluation, reinforcement learning, encoder fine-tuning, generator integration, and recommender development are outside this protocol.

| Topic | Document |
| --- | --- |
| Representation and model order | [Encoder and model](research/03_ENCODER_AND_MODEL.md) |
| Hypotheses and evaluation gates | [Training and evaluation](research/04_TRAINING_AND_EVALUATION.md) |
| MVP contracts | [MVP specification](research/05_MVP_SPECIFICATION.md) |
| Listening protocol | [P0 listening protocol](research/02_P0_LISTENING_PROTOCOL.md) |
| Rights and labels | [Data governance](research/01_DATA_GOVERNANCE.md) |
| What this tree implements | [Status](STATUS.md) |

The [MVP specification](research/05_MVP_SPECIFICATION.md) remains the contract for protocol scope, data, and proposed modules. This note does not replace it.

## 5. Evidence and expansion gates

| Layer | What it is allowed to mean | Where it lives |
| --- | --- | --- |
| Current implementation | Manifests, rights checks, ten-second preparation, identity-safe splits, a dummy encoder, and local P-01 intake. An isolated single-clip CPU CLAP feasibility run is recorded. There is no core adapter, trained ranker, or listening result. | [Status](STATUS.md), source, tests, and configs |
| Proposed experimental methods | Frozen CLAP features, cosine and simple baselines, regularized linear pairwise ranking, then a conditional neural challenger, with grouped splits, calibration, and abstention analysis. | [Encoder and model](research/03_ENCODER_AND_MODEL.md), [training and evaluation](research/04_TRAINING_AND_EVALUATION.md), [MVP specification](research/05_MVP_SPECIFICATION.md) |
| Hypotheses requiring validation | Learning beats the fixed baselines on brief adherence (H1). A small listener-specific adjustment improves later preference predictions (H2). | [Training and evaluation](research/04_TRAINING_AND_EVALUATION.md) |
| Potential future applications | Intent checks used by other systems, candidate selection, reward signals, recommendation support, distillation, and abstention beyond the v0.1 excerpt. | Section 3 |

A broader capability needs a suitable new experiment. A change to label meaning, grouping, rights, or excerpt length needs a new protocol version. Whole-song scope and a different model interface are in that category. They are not extensions that v0.1 can absorb in place.

## 6. Project boundaries

Votelle is not currently:

- a music generator
- a music streaming application
- a general-purpose music recommendation system
- a digital audio workstation
- a deployed reward-model service
- a validated universal music-quality predictor

The repository is an offline research foundation. Fixture tests check software contracts. They are not preference-prediction results.

## 7. Relationship to other project documents

This note states strategic direction. It yields when another document governs the same question:

| Document | Governs |
| --- | --- |
| Source, tests, `configs/`, and `uv.lock` | What the software does |
| [`docs/decisions/`](decisions/) | Accepted engineering choices |
| [`docs/research/`](research/README.md) | Scientific method, rights, and experimental requirements |
| [`docs/STATUS.md`](STATUS.md) | Implementation and research status |
| [`AGENTS.md`](../AGENTS.md) | How coding agents change the tree |
| [`docs/archive/`](archive/README.md) | Earlier rationale and citations |

If this note and an active research document disagree about method, the research document wins. If either disagrees with the code about behavior, the code wins.
