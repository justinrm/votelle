# 02 — Literature and Competitive Landscape

Research v0.1 · October 9, 2026

## The problem is partly solved, and partly still open

Three different tasks are often called “music preference”: predicting listening behavior, evaluating generated music, and choosing among alternatives for a creator's specific brief. They share ranking mathematics, but their labels and deployment contexts differ. Repeated listening can reflect familiarity or availability. It is not a label for whether a new chorus feels emotionally restrained.

BPR established pairwise learning from implicit user–item feedback long before current music generators. It provides useful optimization ideas, but its unobserved-item assumptions should not turn unheard music into negative artistic feedback. [S34](https://arxiv.org/abs/1205.2618)

The unresolved opportunity is not “use a small network to rank music.” It is whether a tightly scoped, reproducible learning procedure improves decisions for a creator, under low-data and hardware constraints, without confusing preference, adherence, and sound quality.

## Closest prior art

| Work | Verified contribution | Consequence for this project |
|---|---|---|
| TuneJury, 2026 | Released instance-level ranker with a 2.8M-parameter MLP over frozen CLAP/MERT features; authors report 70.86% agreement on 2,035 held-out non-tie comparisons | Near-direct prior art; generic architecture is not novel. The number is not a performance target transferable to our clips |
| CMI-RewardBench / CMI-RM, 2026 | Joint framework for musicality and instruction alignment, with text, lyrics and reference audio | Multimodal instruction evaluation is already being studied; use its interface and taxonomy |
| MusicPrefs / MAD, 2025 | Human comparisons and analysis of distribution-level audio metrics | Strong warning that a convenient automatic metric may not reflect human judgments |
| AIME | Separate quality and text-alignment comparison questions | Useful precedent for keeping labels distinct |
| SongEval | Whole-song aesthetic ratings and a released evaluator | Important later comparator; short-window ratings do not establish song-structure competence |
| Audiobox Aesthetics | Four learned audio-aesthetic axes across speech, music and sound | Stronger quality baseline than loudness or clipping alone, but not a personal brief judge |
| PAM | No-reference audio quality scoring through contrasting language prompts | Cheap semantic quality baseline; audit sensitivity to wording |

Sources: [S01](https://github.com/yonghyunk1m/TuneJury), [S04](https://proceedings.mlr.press/v306/ma26am.html), [S19](https://arxiv.org/abs/2503.16669), [S21](https://huggingface.co/datasets/disco-eth/AIME-survey), [S23](https://huggingface.co/datasets/ASLP-lab/SongEval), [S25](https://github.com/facebookresearch/audiobox-aesthetics), [S26](https://github.com/soham97/pam).

## What the evidence supports—and does not

**Similarity is an alignment proxy.** Contrastive audio-language training makes embeddings useful for retrieval and broad attributes. It does not by itself establish sensitivity to subtle restraint, emotional authenticity, lyric correctness, or personal taste. An audio-only encoder supplies no native representation of an instruction. Adding text requires a learned interaction or a compatible aligned representation.

**Distribution metrics answer a different question.** FAD and MAD compare collections to reference distributions. Applying a system-level ranking result to one candidate is a category error. The MusicPrefs study reports substantially better correlation for MAD than its standard FAD setting, but those reported correlations are not per-pair accuracy. Its human comparisons withheld the prompt, so those labels should not be relabeled as adherence judgments. [S19](https://arxiv.org/html/2503.16669v1)

**More complex does not always win.** In CMI-RewardBench's published text-only alignment slice, CLAP-music scores 67.20% and CMI-RM 67.60%; that table supplies no basis to assume the small difference is significant. Its richer compositional tasks tell a different story. The implication is to evaluate the intended input regime rather than copy an overall leaderboard winner. [S05](https://github.com/Haiwen-Xia/CMI-RewardBench)

**Music understanding benchmarks are not preference benchmarks.** Genre, instrument, emotion, key, and beat tasks are useful representation probes. Success there does not guarantee good creative selection. Work evaluating multiple musical traditions also finds uneven cross-cultural generalization and no universal benefit from adaptation. [S43](https://arxiv.org/abs/2506.17055)

**A model's own reward is not independent validation.** Improvements from best-of-N filtering or reward optimization can reflect selection for the evaluator's biases. Use new blind human judgments to establish usefulness. A higher score from the same evaluator used to select candidates is expected, not decisive.

## Existing generator evaluation and screening

ACE-Step 1.5 already documents batch generation, automatic screening, and DiT lyric-alignment scoring. Its implementation derives lyric scores from decoder attention and returns LM/DiT score fields. These are model-specific signals, not measured lyric transcripts or listener preferences. The generator's internal score is a relevant baseline for ACE-generated samples. [S30](https://github.com/ace-step/ACE-Step-1.5/blob/main/docs/en/Tutorial.md), [S31](https://github.com/ace-step/ACE-Step-1.5/blob/main/acestep/core/generation/handler/lyric_score.py)

HeartMuLa publicly describes alignment and transcription components as well as reinforcement-learning improvements. Its released generation resources are verifiable; the existence of a paper component does not establish a separately downloadable encoder. HeartCLAP availability was not sufficiently established to make it an MVP dependency. [S32](https://github.com/HeartMuLa/heartlib), [S44](https://arxiv.org/abs/2601.10547)

YuE2 and MERT2 have published repositories and model cards. YuE2's creator permissions and company commercial use terms differ; it is not interchangeable with the license of an earlier YuE release. MERT2 is a candidate future audio representation, not a reason to expand this MVP into full-song generation. [S33](https://github.com/multimodal-art-projection/YuE)

No primary source reviewed here establishes the detailed internal reward-model architecture or training labels of Suno. Public quality claims should not be used to reverse-engineer an assumed architecture.

## Jev, Laya, and language-model evaluators

Jev's useful idea is a focused typed decision API with uncertainty-aware downstream policy. Its documented state interface is text/structured content; no validated music-waveform evaluator was established. Borrow the interface discipline, not an assumed audio capability. [S36](https://api.typesafe.ai/redoc), [S37](https://typesafe.ai/blog/introducing-system-one-models-and-jev)

Laya's official card describes text decision checkpoints around 322–421M parameters. It also reports overconfidence requiring recalibration, despite stronger calibration language elsewhere in the card. Proper scoring rules encourage honest probabilities under assumptions; they do not prove calibration under distribution shift. Laya cannot recover audio nuances absent from a supplied caption, and interpreting a string of embedding coordinates is not a validated audio interface. [S38](https://huggingface.co/convaiinnovations/laya)

An audio-language model can supply a costly comparator or an annotation aid. Its eloquent explanation is not ground truth. Do not use its labels for both training and the final test. Music Flamingo is a relevant contemporary comparator, with noncommercial terms and a much larger deployment footprint than the proposed head. [S17](https://huggingface.co/nvidia/music-flamingo-hf)

## Build versus contribute

| Path | Advantages | Problems | Recommendation |
|---|---|---|---|
| Contribute to CMI-RewardBench | Existing task formats and external comparability | Dataset and model terms still need separate handling | Good destination for a small-model adapter or better resource reporting |
| Independent focused library | Clear scope, permissive original code, controlled personal-data experiments | Must avoid reinventing benchmark machinery | Recommended research vehicle |
| Fork TuneJury | Closest starting architecture and reproduction path | License inconsistencies between advertised variants and root code license; larger dependency stack | Research comparison only until exact licensing is resolved |
| Use an existing scorer only | Fastest path to personal candidate screening | Less original model training; still requires task validation | Appropriate if it already meets the need |
| Use a classical method | Cheap, explainable and easy to reproduce | May miss nonlinear interactions | Preferred outcome if neural models do not improve results |

The root TuneJury LICENSE covers training/evaluation code under CC-BY-NC, while the card advertises an Apache CLAP-only checkpoint. Do not assume the latter licenses all repository code. This inconsistency is an explicit adoption gate. [S02](https://huggingface.co/TuneJury/tunejury), [S03](https://github.com/yonghyunk1m/TuneJury/blob/main/LICENSE)

## What could be original

**Engineering contribution:** clean manifests, local extraction, cached training, calibrated typed outputs, generator-independent adapters, and a faithful reproduction. Valuable portfolio work, but not a novel ranking algorithm.

**Research contribution:** evidence that a defined low-data adaptation method improves a creator's future choices on held-out brief families and unfamiliar generators; or a released dataset separating adherence from personal preference with repeated judgments. Both need comparisons to existing adaptation methods.

**Product contribution:** fewer minutes spent auditioning unsuitable candidates, with transparent uncertainty and easy human override. This can be useful even if the final model is linear.

The two priority hypotheses and their falsification tests are specified in 05. They are proposed investigations, not claims of novelty already established by this review.
