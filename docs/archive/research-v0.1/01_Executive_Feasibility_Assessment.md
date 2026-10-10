# 01 — Executive Feasibility Assessment

Research v0.1 · October 9, 2026 · Justin Merwin

## Verdict

**CONDITIONAL GO.** Build a reproducible experiment that can establish whether learning from a creator's judgments improves candidate selection. Do not begin by promising a new general music evaluator or a path to outperforming Suno. The central architecture is feasible, but it is already represented in public research. Your contribution must come from the question, data, evaluation, or demonstrated deployment advantage.

Recommended working definition: **Music Preference Model v0.1 is a Python research library that learns separate brief-adherence and listener-preference rankings over 10-second music excerpts, using frozen representations and the smallest scorer supported by evidence.** The initial release can legitimately contain a linear model and a negative neural-network result.

The strongest reason to do this is the combination of a useful personal music tool and a substantive ML engineering project: auditable datasets, leakage prevention, ranking objectives, uncertainty, experiments, and deployment. It is not currently a defensible claim of novel foundation-model research.

## What changed after reviewing the literature

- A close implementation already exists in TuneJury; use it as prior art and, where permitted, an external benchmark. Its published scope and license variants matter. See 02 and 04. [S01](https://github.com/yonghyunk1m/TuneJury)
- CMI-RewardBench directly investigates compositional music instructions. The broad problem is active research, not an empty field. [S04](https://proceedings.mlr.press/v306/ma26am.html)
- Several attractive encoders impose noncommercial weight terms. The proposed default instead uses a published Apache-2.0 CLAP checkpoint; this is a practical selection, not a claim that CLAP is universally best. [S08](https://huggingface.co/laion/larger_clap_music)
- A small trainable head does not make the entire system tiny. The frozen encoder dominates download size, memory, and uncached inference. Precomputing embeddings is the key economy.

## Viability assessment

| Dimension | Assessment | Condition |
|---|---|---|
| Technical | Strong for cached-feature ranking; uncertain for nuanced musical intent | Prove representations distinguish the particular judgments you care about |
| Financial | Local first experiment can have $0 incremental compute expense | Existing rights-cleared audio, self-labeling, and adequate local runtime |
| Scientific | Good falsifiable project; generic novelty is low | Compare strong baselines on genuinely held-out material |
| Open source | Viable for new code and carefully scoped artifacts | Audit code, weights, source audio, text, labels, and redistribution separately |
| Personal usefulness | Plausible for reducing listening workload | Measure accepted candidates and time, not just agreement scores |
| Foundation-model ambitions | Indirect preparation only | A better selector does not create missing generator capabilities |

## Answers to the ten decision questions

1. **Is a small preference model justified?** As an experiment, yes. As a predetermined neural solution, no. Begin with cosine similarity and regularized pairwise logistic regression. Only promote the neural variant if held-out results justify it.

2. **Best representation for the first experiment?** Frozen `laion/larger_clap_music` audio and text embeddings, with exact revision pinning. The operational fallback is `laion/clap-htsat-unfused`. Add an audio-only encoder only after a measured error analysis shows a representation gap. Encoder details and license distinctions live in 03.

3. **Simplest credible trainable architecture?** A shared candidate scorer using 1,537 fixed interaction features and L2-regularized Bradley–Terry-style logistic loss. Interaction terms are essential: concatenating audio and brief embeddings in a purely linear scorer makes the brief-only term cancel during pairwise comparison. With only 50–100 labels, prefer an even lower-dimensional baseline and treat results as exploratory.

4. **Where does legally usable data come from?** The most controllable route is original recordings or documented creator contributions, plus original prompts and human labels. Locally generated audio from an audited permissive model is another route. A filtered Music Arena subset is promising but requires per-source review; there is no verified, frictionless commercial dataset that fully matches this personal creative-intent task. Dataset metadata licenses do not settle every audio right.

5. **Can the MacBook Neo support a meaningful proof of concept?** Yes for preprocessing, cached features, linear training, small-head training and evaluation. Single-clip encoder extraction is plausible on CPU and worth testing on MPS. No throughput or memory benchmark on your machine has been run. An 8 GB system must load one encoder at a time and avoid simultaneously running generators.

6. **Realistic minimum cost?** $0 incremental cash for a local pilot with owned audio and your own judgments; roughly 2–4 hours of annotation/setup for the first small listening pilot, plus engineering time. An adequately powered publication-style study is not realistically a zero-effort exercise. Budget and runtime formulas are in 07.

7. **What would demonstrate value?** Pre-register a practical target of at least a five-percentage-point gain over the strongest eligible baseline, with a positive lower bound on a paired, group-resampled 95% confidence interval, on new brief/song families. Treat this as a proposed gate, not a prediction. Also require a blind listening study showing useful recommendations; a 50-pair pilot cannot substantiate a broad superiority claim.

8. **Strongest original contribution?** A legally releasable benchmark that separates “matches my brief” from “I personally prefer it,” includes repeated creator judgments, and tests low-data adaptation plus abstention on unfamiliar generators. A reproducible negative result about frozen embeddings would also be valuable. Novelty remains provisional until the exact study is compared with the full current literature.

9. **Independent model, contribution, or established method?** Build a narrow independent experiment harness and small scorer from established methods, and design an adapter for existing evaluation projects. Contribute reusable evaluation fixes upstream when appropriate. Avoid a broad fork of a noncommercial codebase if a permissive release is your goal. Stop at the established linear method if it performs as well.

10. **First action in Cursor?** Give Cursor document 08 and the rest of this package. Ask it to implement only typed manifests, rights-policy validation, group-safe splitting, deterministic audio preparation, a dummy encoder, and an offline contract test. The first session ends before real model downloads or training.

## Recommended decision gates

The cheap falsification sequence is: validate rights and label meaning → test whether judgments are sufficiently stable → benchmark one encoder locally → train simple models → evaluate on locked data → decide whether another model is worth building.

Do not escalate if you cannot secure appropriate audio, your preferred target is not repeatable enough to learn, or the linear scorer fails to beat cosine after a reasonable data expansion. Redirect toward a transparent similarity-and-measurement tool if that is what the evidence supports. The first meaningful deliverable is an honest experimental result, not a feature-rich application.
