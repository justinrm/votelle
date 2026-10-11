# 03 — Audio Encoder and Architecture Analysis

Research v0.1 · October 9, 2026 · Authority for representation and model design

## Recommended representation

**Primary: frozen `laion/larger_clap_music`, using the Hugging Face Transformers implementation. Fallback: frozen `laion/clap-htsat-unfused`.** Both audio and brief vectors have 512 coordinates in a shared space. Start with one encoder, one 10-second mono excerpt at a time. Pin the repository revision, processor files, library environment, and weight hash.

The primary checkpoint's card declares Apache-2.0, and its published file tree lists about 776 MB of weights. The native LAION repository uses CC0 and distributes differently packaged checkpoints. Preserve the license and identity of the artifact actually loaded; do not mix those descriptions. [S08](https://huggingface.co/laion/larger_clap_music), [S09](https://huggingface.co/laion/larger_clap_music/tree/main), [S11](https://github.com/LAION-AI/CLAP/blob/main/LICENSE)

This choice minimizes dependency complexity, offers instruction conditioning without a separate language model, and retains a plausible commercial route. It does not establish CLAP as the best representation for emotional or structural judgments.

## Ranked encoder shortlist

Parameter counts describe complete released encoders unless marked otherwise. Weight memory is **derived FP32 tensor storage**, not peak process memory. Exact parameter counts for approximate entries must be recorded after loading the pinned artifact. Runtime on A18 Pro has not been measured.

| Rank / model | Architecture and representation | Input / context | Size and resource implications | Decision |
|---|---|---|---|---|
| 1. CLAP music | HTSAT/Swin audio tower + RoBERTa text tower; 512-d aligned embeddings; approximately 194M parameters from checkpoint size | 48 kHz; 10-second processor window | ~0.78 GB weights; one CPU/MPS worker, batch 1 | Primary semantic baseline and frozen feature source |
| 2. CLAP unfused | Smaller general-audio HTSAT + text tower; 512-d joint space; ~154M inferred from storage | 48 kHz; 10-second windows | ~615 MB weights | Resource and dependency fallback; less music-specific |
| 3. MusicFM FMA | BEST-RQ-style masked prediction with Conformer; approximately 330M; frame features, commonly 1,024-d | 24 kHz; published examples use 30 seconds | ~1.32 GB tensor storage; non-Flash CPU path preferred for a probe | Optional complementary audio-only encoder after baseline results |
| 4. MERT-v1-95M / 330M | Masked audio Transformer; 768 / 1,024-d frame features | 24 kHz; 5-second pretraining context, longer extraction needs memory testing | ~0.38 / 1.32 GB tensor storage | Useful restricted research probes; no native brief alignment |
| 5. MuQ / MuQ-MuLan | Music SSL (~300M) / music–text contrastive (~700M); 1,024-d audio / 512-d aligned output | Strict 24 kHz; MuLan config uses 10 seconds | ~1.2 / 2.8 GB before overhead; authors recommend FP32 | Strong noncommercial comparison, too costly/restricted as default |
| 6. MERT2-30s / FullSong | 632M bidirectional encoder; 24 layers, 1,024-d, 25 Hz | 24 kHz; 30-second or 30–360-second intended context | ~2.53 GB tensor storage; long-context activations can dominate | New 2026 research comparator; not the 8 GB MVP default |
| 7. OpenL3 music | Audio CNN learned with audiovisual correspondence; 512 or 6,144-d embeddings | Approximately one-second analysis windows, configurable hop | Exact loaded parameters/peak RAM not established in this review | Permissive fallback for audio-only features, but extra Keras/TensorFlow stack and no text alignment |
| 8. music2vec-v1 | 95M BYOL/data2vec-family audio representation; 768-d | 16 kHz; 30-second pretraining context | ~0.38 GB tensor storage | Older audio-only research control; no clear practical advantage here |

Primary specifications: [S10](https://huggingface.co/laion/clap-htsat-unfused/tree/main), [S12](https://huggingface.co/m-a-p/MERT-v1-95M), [S13](https://github.com/tencent-ailab/MuQ), [S14](https://github.com/minzwon/musicfm), [S15](https://huggingface.co/m-a-p/MERT-v2-30s), [S16](https://huggingface.co/m-a-p/MERT-v2-FullSong), [S18](https://github.com/marl/openl3), [S45](https://huggingface.co/m-a-p/music2vec-v1), [S46](https://huggingface.co/OpenMuQ/MuQ-MuLan-large/blob/main/config.json).

The CLAP parameter approximations above are storage-derived, not verified `numel()` counts. Checkpoint buffers and serialization overhead make them approximate. The release registry must replace them with measured counts, not perpetuate the estimate.

## License and adaptation matrix

| Family | Source-code terms | Weight terms observed | Commercial-use position | Training / adaptation |
|---|---|---|---|---|
| Selected HF CLAP | Transformers Apache-2.0; native LAION code CC0 | Selected cards Apache-2.0 | Permissive published artifact terms; underlying provenance is not a legal warranty | Frozen extraction first; differentiable fine-tuning technically possible |
| MuQ / MuQ-MuLan | MIT | CC-BY-NC-4.0 | Noncommercial research lane | Training recipes available; adapters cannot remove weight restrictions |
| MERT v1 | Official repository root Apache-2.0; retain inherited component notices, including MIT headers | CC-BY-NC-4.0 | Noncommercial research lane | Public model/custom code; pin and inspect before remote-code loading |
| MERT2 | YuE2 repository Apache-2.0 plus component notices | Encoder cards CC-BY-NC-4.0 | Treat encoders as noncommercial; do not import YuE2 creator exceptions without explicit coverage | Research adaptation later; more recent dependency surface |
| MusicFM | MIT except identified Flash-Conformer component under Apache-2.0 | Official HF metadata MIT; card body empty | Promising permissive alternative, retain checkpoint provenance and license snapshot | Frozen or fine-tuned; omit Flash path on Mac |
| OpenL3 | MIT | CC-BY-4.0 | Attribution required; attractive for standalone audio probes | Keras-based; fine-tuning adds another framework |
| music2vec-v1 | Audit underlying implementation if adopted | CC-BY-NC-4.0 | Noncommercial research lane | Superseded as practical first choice by aligned CLAP or newer audio SSL models |

Sources: encoder links above, [S47](https://huggingface.co/minzwon/MusicFM), [S48](https://github.com/minzwon/musicfm/blob/master/LICENSE), and the [MERT code license](https://github.com/yizhilll/MERT/blob/main/LICENSE). “Open weights” and “open-source software” are different descriptions; NC models do not satisfy unrestricted commercial-use goals.

## Other 2025–2026 options

Music Flamingo supports music-focused audio–language interaction, with 30-second windows and a published ten-minute input cap. Its noncommercial license and large language-model stack make it an optional rented-compute evaluator, not the local MVP representation. Exact current-checkpoint parameter count, quantization quality, and Mac memory were not established; do not silently substitute a newer checkpoint for the one cited. [S17](https://huggingface.co/nvidia/music-flamingo-hf)

MERT2 is a verified new release worth revisiting for full-song structure. Its reported MIR results are not a reward-model benchmark. HeartCLAP is described in the HeartMuLa paper, but a separately deployable checkpoint and inference contract were not verified. An announced architecture is not an available dependency. General audio LLMs and text-only Jev/Laya are not shortlisted without a task-specific advantage; see 02.

## Representations and target separation

Let `a = normalize(E_audio(excerpt))` and `t = normalize(E_text(brief))`, each in R^512. Preserve the exact free-text brief; require a brief that describes properties audible within the selected region. Store optional explicit attributes as metadata rather than using an LLM to invent structured labels.

Maintain three output families:

1. **Measurements:** original duration, sample rate, sample peak, clipping indicator, RMS/loudness measurements and silence diagnostics. They come from signal processing, with method identifiers.
2. **Adherence:** a learned ranking score for the listener's explicit “better matches this brief” judgment.
3. **Preference:** a separately learned ranking score for a named listener or defined population, with its own labels and calibration.

Do not assume instrument detection, estimated tempo, ASR accuracy, or emotional labels are objective facts. If introduced later, they are model estimates with their own validation. Do not infer lyric correctness from CLAP similarity.

## Six architectures

All head counts exclude the frozen encoder. Data amounts below are research planning heuristics, not guaranteed learning curves.

| Architecture | Definition / count | What it can learn | Requirements and risks | MVP position |
|---|---|---|---|---|
| A. Deterministic baseline | Cosine similarity; invalid-audio checks; optional fixed acoustic constraints. Zero trained parameters | Nothing from preferences; broad semantic matching only | Very cheap after extraction; brittle proxies, poor personalization | Mandatory |
| B. Linear pairwise model | `s=w·phi(a,t)`; 1,537 coefficients, no bias | Weighted audio tendencies and fixed text–audio interactions | Strong L2, preferably several hundred labels; limited nonlinear interactions | First trainable model |
| C. Small shared scorer | `[a,t,a*t,abs(a-t)] → 64 → 1`, GELU, dropout; **131,201 parameters** per target | Nonlinear intent–audio interactions | Cached CPU training; high overfitting risk on tiny data | Controlled challenger |
| D. Direct pair comparator | Antisymmetric MLP over both candidates and brief; design budget ~0.25–1M | Relative interactions not separable into candidate utilities | More labeled comparisons, order tests, possible preference cycles | Defer unless C fails for a diagnosed reason |
| E. Compact decision Transformer | 2 layers, width 128, projected brief/audio/window tokens; proposed ~0.5–1M | Attention over structured evidence and temporal windows | Greater sample demand, weaker interpretability, no automatic calibration | No initial justification |
| F. Adapted audio encoder | Frozen backbone plus LoRA/adapters, proposed ~0.1–5M trainable depending on target layers | Can change representation where fixed features discard information | Backprop activations still large; likely rented GPU; encoder/data rights remain | Only after representation diagnosis |

Interpretability in B means coefficient inspection and controlled feature ablations, not that individual embedding coordinates are musical concepts. C–F generally offer less direct interpretation. None should emit free-form musical explanations from a scalar score.

### Architecture B: smallest credible conditional ranker

Use:

`phi(a,t) = concat(a, a*t, abs(a-t), dot(a,t))`.

Dimension: `512 + 512 + 512 + 1 = 1,537`. Elementwise multiplication and absolute difference make the score depend jointly on candidate and intent. Remove the candidate intercept because it cancels in every comparison.

For A versus B under one brief, `d = s(A,t) - s(B,t)` and `p_train(A)=sigmoid(d)`. Minimize binary cross-entropy on human non-tie choices plus L2 regularization. This is a training probability, not yet a validated public probability.

**Important implementation trap:** `s(a,t)=w_a·a + w_t·t` yields `s(A,t)-s(B,t)=w_a·(A-B)`. The text term disappears. A model can appear prompt-conditioned in its input schema while actually ignoring the brief.

With only 50–100 pairs, use cosine and a compact feature model before the 1,537-coefficient version: four similarities (full brief and up to three human-authored audible clauses) with explicit missing-clause masks. Coefficients and preprocessing are fit on training data only. This compact model is a pilot control, not a substitute for the specified main experiment.

### Architecture C: exact neural challenger

Input dimension 2,048. One hidden layer with 64 units, GELU, dropout 0.1, scalar output. Count: `2048*64 + 64 + 64*1 + 1 = 131,201`. Train two independent instances only when both target labels exist: 262,402 total parameters. Separate models simplify missing-label handling and prevent a large unrelated dataset from silently dominating the personal target. A shared multi-head trunk is a later ablation.

### Independent, pairwise, and listwise ranking

Shared candidate scoring is recommended: score each of N candidates once, sort, and use differences for pairwise decisions. It provides a consistent scalar ordering under a fixed brief/listener. The real human preferences may still contain cycles; report that mismatch rather than pretending the model captures every judgment.

A direct pairwise model must enforce reversal symmetry, for example `d(A,B)=(h(A,B)-h(B,A))/2`. This prevents order bias but does not prevent cycles. Naive all-pairs ranking costs O(N²) comparisons. Listwise Plackett–Luce or ranking losses require reliable multi-item orderings, and deriving all six pairs from four ranked candidates does not produce six independent observations.

## Personalization and encoder adaptation

Cold start uses the generic baseline with no claim about the individual. Later fit `w_user = w_population + delta_user`, penalizing the size of `delta_user`; if no eligible population model exists, shrink toward the specified fixed baseline instead. Do not add a user ID as a magic source of information. Estimate learning curves using 0, 25, 50, 100 and 200 adaptation judgments and future held-out clips.

Frozen embeddings are the default because they isolate the value of learning a preference rule and make repeated experiments cheap. Try alternate frozen layers/encoders before adapters. Full encoder fine-tuning is out of scope; it would confound representation learning, labeling noise, compute, and preference learning in the same small experiment.
