# 03 — Encoder and model

Research protocol **v0.1**. Evidence date **10 October 2026**.

Human-readable name: Votelle. Package: `votelle_music`. CLI: `votelle-music`. Exception: `VotelleError`. Decisions 0001–0003 still spell the earlier `music-pref` / `music_pref` commands. Those historical sentences stay in the decision files. This note uses the live names.

## Purpose

This note is the current representation and scoring position for protocol v0.1. It consolidates the architecture analysis, the dated CLAP handoff, the accepted audition and foundation decisions, the encoder and cache source, and the status record.

The architecture note remains the design authority for representation and model form. The dated handoff remains a pre-attempt contract and was not rewritten after the probe. `docs/STATUS.md` is the result record. `docs/PROJECT_DIRECTION.md` states long-term order and yields to the architecture note on method. Source, tests, and configs establish what the core tree runs.

## Executive summary

The v0.1 representation is frozen music CLAP. The primary checkpoint is `laion/larger_clap_music` at revision `a0b4534a14f58e20944452dff00a22a06ce629d1`, 776,444,665 bytes, SHA-256 `5c289311f4a030d768af7ffbfdecd01b008aa64824211899a4e59f4f9d154fd1`. The resource fallback is frozen `laion/clap-htsat-unfused`. Both expose 512-dimensional audio and text vectors. The core tree does not load either checkpoint.

`votelle_music` implements a 512-dimensional dummy encoder, `dummy` / `fixture-v1`, and a content-addressed feature cache. `votelle-music validate` refuses every other encoder. There is no core CLAP adapter. PyTorch and Transformers are not dependencies of the core environment.

On 10 October 2026 an isolated CPU probe embedded one technical excerpt and four texts. Cold peak resident set size was 1,103,282,176 bytes. In-process and fresh-process embeddings were bit-identical. The four cosines are encoder similarities for that excerpt. The planned scorers, in order, are cosine similarity, a 1,537-coefficient linear pairwise ranker, and a 131,201-parameter MLP challenger, with adherence and preference kept as separate targets. The 20-clip benchmark has not been run, MPS parity is unverified, the three-clip runner has not been executed, and no preference model has been trained.

## 1. Claim labels

| Label | Use in this note |
|---|---|
| Verified implementation | Behavior present in `votelle_music` source, configs, or the foundation tests |
| Measured probe result | A figure recorded from the 10 October 2026 isolated probe in `docs/STATUS.md` |
| Proposed method | A specified later method. The core tree does not run it |
| Unresolved question | Still open after the sources listed in section 16 |

A green foundation test is a software check. It is not evidence of preference prediction.

## 2. Representation order

**Proposed method.** `docs/PROJECT_DIRECTION.md` records this order and does not expand protocol v0.1:

1. Frozen CLAP audio and text representations.
2. Fixed cosine similarity and other simple baselines.
3. Regularized linear pairwise ranking.
4. A small neural challenger only when the data and the baselines justify it.
5. Leakage-safe evaluation, uncertainty analysis, and human validation.

The unit of analysis is an explicitly selected ten-second excerpt. The architecture note is the authority for the feature maps and parameter counts in sections 9 and 10. The direction note and the architecture note agree on this order.

Text-only Jev is not this encoder. The v0.1 representation is frozen music CLAP.

## 3. Primary encoder, fallback, and shortlist

**Proposed method** for the selection. **Measured probe result** for the one primary checkpoint that was loaded on CPU (section 13).

| Role | Hugging Face ID | What v0.1 uses it for |
|---|---|---|
| Primary | `laion/larger_clap_music` | Frozen semantic baseline and frozen feature source |
| Resource fallback | `laion/clap-htsat-unfused` | Same 512-d interface after a primary resource failure. New cache namespace. Vectors are not mixed |

Start with one encoder and one 10-second mono excerpt at a time. Pin the repository revision, processor files, library environment, and weight hash. The primary card declares Apache-2.0. The native LAION repository uses CC0 and distributes different `.pt` checkpoints, including `music_audioset_epoch_15_esc_90.14.pt`. Preserve the license and identity of the artifact actually loaded.

The published primary file tree is about 776 MB of weights. That file size is storage, not peak process memory. The CLAP parameter figures below are storage-derived approximations, not verified `numel()` counts.

| Rank / model | Architecture and representation | Input / context | Size and resource implications | Decision |
|---|---|---|---|---|
| 1. CLAP music | HTSAT/Swin audio tower + RoBERTa text tower; 512-d aligned embeddings; approximately 194M parameters from checkpoint size | 48 kHz; 10-second processor window | ~0.78 GB weights; one CPU/MPS worker, batch 1 | Primary semantic baseline and frozen feature source |
| 2. CLAP unfused | Smaller general-audio HTSAT + text tower; 512-d joint space; ~154M inferred from storage | 48 kHz; 10-second windows | ~615 MB weights | Resource and dependency fallback; less music-specific |
| 3. MusicFM FMA | BEST-RQ-style masked prediction with Conformer; approximately 330M; frame features, commonly 1,024-d | 24 kHz; published examples use 30 seconds | ~1.32 GB tensor storage; non-Flash CPU path preferred for a probe | Optional complementary audio-only encoder after baseline results |
| 4. MERT-v1-95M / 330M | Masked audio Transformer; 768 / 1,024-d frame features | 24 kHz; 5-second pretraining context; longer extraction needs memory testing | ~0.38 / 1.32 GB tensor storage | Restricted research probes; no native brief alignment |
| 5. MuQ / MuQ-MuLan | Music SSL (~300M) / music–text contrastive (~700M); 1,024-d audio / 512-d aligned output | Strict 24 kHz; MuLan config uses 10 seconds | ~1.2 / 2.8 GB before overhead; authors recommend FP32 | Noncommercial comparison; too costly and restricted as the default |
| 6. MERT2-30s / FullSong | 632M bidirectional encoder; 24 layers, 1,024-d, 25 Hz | 24 kHz; 30-second or 30–360-second intended context | ~2.53 GB tensor storage; long-context activations can dominate | 2026 research comparator; not the 8 GB MVP default |
| 7. OpenL3 music | Audio CNN from audiovisual correspondence; 512 or 6,144-d embeddings | About one-second analysis windows, configurable hop | Loaded parameter count and peak RAM were not established in the review | Permissive audio-only fallback; extra Keras/TensorFlow stack; no text alignment |
| 8. music2vec-v1 | 95M BYOL/data2vec-family audio representation; 768-d | 16 kHz; 30-second pretraining context | ~0.38 GB tensor storage | Older audio-only control; no practical advantage for this first experiment |

Weight memory in that table is derived FP32 tensor storage, not peak process memory. Runtime on A18 Pro was not measured in the architecture review. Section 13 records a later macOS arm64 measurement and does not name the chip.

Publisher metadata for the two CLAP snapshots, as pinned in the handoff:

| Property | Primary | Resource fallback |
|---|---|---|
| Hugging Face ID | `laion/larger_clap_music` | `laion/clap-htsat-unfused` |
| Immutable revision | `a0b4534a14f58e20944452dff00a22a06ce629d1` | `8fa0f1c6d0433df6e97c127f64b2a1d6c0dcda8a` |
| Weight filename | `pytorch_model.bin` | `pytorch_model.bin` |
| Published file bytes | 776,444,665 | 614,525,833 |
| Published LFS SHA-256 | `5c289311f4a030d768af7ffbfdecd01b008aa64824211899a4e59f4f9d154fd1` | `1cd3c601bc4afe0fa87be3de4c13dd2cfadd249fac1e29acf74a9b296c3219bb` |
| Audio tower | HTSAT/Swin, depths 2/2/12/2; final width 1024; patch width 128 | HTSAT/Swin, depths 2/2/6/2; final width 768; patch width 96 |
| Shared projection | 512 audio / 512 text | 512 audio / 512 text |
| Text tower | RoBERTa-style, hidden width 768 | Same hidden width |
| Published weight license | Apache-2.0 model-card declaration | Apache-2.0 model-card declaration |

The smaller file is 161,918,832 bytes smaller (about 20.9%). The handoff treats that saving as insufficient, by itself, to assume it would rescue an activation or loading failure. The fallback was not the checkpoint loaded in the recorded probe. Its hash remains publisher-reported.

Neither `main` nor a short hash is the reproducibility record. Both snapshots list README, config, preprocessor config, tokenizer files, `.gitattributes`, and one `.bin` weight file. No safetensors weight was listed at review. The handoff requires restricted weight loading, with remote code left off.

Music Flamingo is an optional rented-compute evaluator because of its noncommercial license and language-model stack. It is not the local MVP representation. HeartCLAP is described in a paper; a separately deployable checkpoint and inference contract were not verified. An announced architecture is not an available dependency. General audio LLMs are not on the shortlist without a task-specific advantage.

## 4. License considerations

**Proposed method** for which artifacts may be loaded. A model card is not a warranty of training-data rights, and a published encoder license does not prove absence of overlap with any particular recording catalog.

| Family | Source-code terms | Weight terms observed | Commercial-use position | Training / adaptation |
|---|---|---|---|---|
| Selected HF CLAP | Transformers Apache-2.0; native LAION code CC0 | Selected cards Apache-2.0 | Permissive published artifact terms; underlying provenance is not a legal warranty | Frozen extraction first; differentiable fine-tuning is technically possible |
| MuQ / MuQ-MuLan | MIT | CC-BY-NC-4.0 | Noncommercial research lane | Adapters cannot remove weight restrictions |
| MERT v1 | Repository root Apache-2.0; retain inherited component notices, including MIT headers | CC-BY-NC-4.0 | Noncommercial research lane | Pin and inspect before remote-code loading |
| MERT2 | YuE2 repository Apache-2.0 plus component notices | Encoder cards CC-BY-NC-4.0 | Treat encoders as noncommercial | Research adaptation later |
| MusicFM | MIT except an identified Flash-Conformer component under Apache-2.0 | Official HF metadata MIT; card body empty | Promising permissive alternative; retain checkpoint provenance | Frozen or fine-tuned; omit the Flash path on Mac |
| OpenL3 | MIT | CC-BY-4.0 | Attribution required | Keras-based |
| music2vec-v1 | Audit the underlying implementation if adopted | CC-BY-NC-4.0 | Noncommercial research lane | Superseded as the practical first choice by aligned CLAP |

Open weights and open-source software are different descriptions. NC weight terms do not meet an unrestricted commercial-use goal. Votelle’s own Apache-2.0 grant covers original source and project documentation. It does not clear third-party weights, recordings, or embeddings.

## 5. Pinned primary checkpoint

| Fact | Value | Label |
|---|---|---|
| Repository | `laion/larger_clap_music` | Proposed method, then loaded in the probe |
| Revision | `a0b4534a14f58e20944452dff00a22a06ce629d1` | Measured probe result |
| SHA-256 | `5c289311f4a030d768af7ffbfdecd01b008aa64824211899a4e59f4f9d154fd1` | Measured probe result |
| Bytes | 776,444,665 | Measured probe result |

The handoff recorded that hash and byte length as publisher-reported, and it said they had not been recomputed locally. That sentence is the pre-attempt contract. On 10 October 2026 the status record recomputed the SHA-256 and the byte length from the local `pytorch_model.bin`. Both matched the publisher figures, the pre-run `shasum`, and the worker. `snapshot-hashes.json` records `weight_ok: true`. A later cleanup the same day recomputed the checkpoint hash and length again, without reloading the model, and they still matched.

The fallback revision and hash in section 3 were not part of that recomputation.

## 6. Waveform, text, and pooling contract

**Verified implementation** for the excerpt buffer. **Proposed method** for the Transformers call. **Measured probe result** for the mel shape actually observed.

Protocol v0.1 audio is 10 seconds, 48 kHz, mono. `src/votelle_music/audio/prepare.py` sets `TARGET_RATE = 48000` and `TARGET_SAMPLES = 480_000`. Resampling uses `scipy.signal.resample` (`scipy.signal.resample/fft/v1`). The loader does not pad, trim, or choose the crop.

`waveform_for_encoder` returns a contiguous float32 copy of the prepared excerpt, shape `(480000,)`. The listening samples and the encoder buffer are the same excerpt. A buffer that is not exactly 480,000 finite float32 samples raises `VotelleError` with code `invalid_audio`.

Decision 0002 fixes the adapter contract for a later session. The `AudioTextEncoder` signature does not change. `embed_audio` already takes `PreparedExcerpt`. The adapter, when it is written, has to:

- call `waveform_for_encoder` and pass `sampling_rate=48000`
- reject any buffer that is not exactly 480,000 finite samples before the feature extractor
- pass `truncation="rand_trunc"` and `padding="repeatpad"` only after that assert
- read `pooler_output` from the model-output object into the existing `FeatureBatch` ndarray
- reject a brief over 512 tokens, including special tokens, with truncation left off, using the adapter-local failure `brief_too_long`
- set `EncoderSpec.pooling` to `pooler_output`, `dtype` to `float32`, and `production_claim_allowed` to false until the probe gates pass

The processor defaults are not allowed to repair length. At exactly 480,000 samples the handoff’s cited Transformers 5.19.0 extractor takes the no-random-crop path. Longer inputs can select a random crop. Shorter inputs can repeat or pad. Both pinned models use unfused extraction. The saved configuration’s `nb_max_frames` is 1000. The expected unfused mel shape is `(1, 1, 1001, 64)`. Record the observed shape. Do not force 1000 frames.

The primary and fallback preprocessor configs specify 48,000 Hz, 480,000 samples, 10 seconds, 64 mel bands, FFT 1024, hop 480, 50–14,000 Hz, `repeatpad`, and `rand_trunc`. The extractor validates `sampling_rate` and does not resample.

Text uses the snapshot’s RoBERTa tokenizer. The brief limit is 512 tokens, including special tokens. Tokenize with truncation off, inspect length, and reject a longer brief. Tokenizer metadata and `max_position_embeddings` are different fields. 514 is not the brief limit. Briefs stay plain original text, without an automatic prefix or rewrite.

With `return_dict=True`, `get_audio_features` and `get_text_features` return a model-output object. `pooler_output` is the projected, L2-normalized vector. `last_hidden_state` is not the cached embedding. The return value is not assumed to be a bare tensor. Full-model logits include a learned scale and are not preference probabilities. Zero and non-finite vectors are rejected. Re-normalizing is optional and, if done, must be versioned.

`EncoderSpec` in `src/votelle_music/schemas.py` stores `name`, `revision`, `dimension`, `production_claim_allowed`, `processor_hash`, `pooling`, and `dtype`. `FeatureBatch` is a dataclass in `src/votelle_music/features/base.py`: an ndarray `vectors` plus that spec. `l2_normalize` requires one finite vector of length 512 and rejects a zero norm. `FeatureError` subclasses `VotelleError`.

## 7. What the core tree implements

**Verified implementation.**

The dummy encoder is `dummy` / `fixture-v1`. It cannot support a production claim. `describe()` sets `dimension` 512, `production_claim_allowed` false, `processor_hash` `"none"`, `pooling` `"clip"`, and `dtype` `"float32"`. Audio vectors are a deterministic unit-length draw from the SHA-256 of the contiguous float32 PCM. Text vectors are the same kind of draw from the UTF-8 brief. The module states that this is not a musical embedding and not a production model.

`validate` in `src/votelle_music/data/manifest.py` appends `encoder_unavailable` when `encoder.name` is not `dummy` or `encoder.revision` is not `fixture-v1`. The foundation config cannot name CLAP. Decision 0002 still prohibits that, including after the isolated probe. The historical decision text says `music-pref validate`. The live command is `votelle-music validate`.

Cache keys are the SHA-256 of canonical JSON. Canonical bytes are UTF-8 JSON with sorted keys, separators `(",", ":")`, `ensure_ascii` false, and a trailing newline. The payload fields are:

| Field | Role |
|---|---|
| `source_pcm_sha256` | Source PCM hash |
| `start_seconds`, `end_seconds` | Excerpt bounds |
| `preprocessing_sha256` | Preprocessing document hash |
| `encoder_id`, `encoder_revision` | Encoder identity |
| `processor_hash` | Processor identity. Default `"none"` |
| `pooling` | Default `"clip"` on the dummy path. The CLAP adapter’s spec value is `pooler_output` |
| `dtype` | Default `"float32"` |

Stored entries are contiguous float32 vectors of shape `(512,)`, finite, written with `allow_pickle=False`. Keys are 64 lowercase hex characters. An existing key is reused. Replacement is atomic for one process. A changed encoder, processor, pooling mode, or preprocessing document is a new key. Dummy vectors and CLAP vectors do not share a feature space.

`preprocessing_sha256` is the SHA-256 of the canonical preprocessing document. The gain profile adds downmix, loudness, true-peak, target LUFS, ceiling, tolerance, and the ungated-gate fallback. Changing any of those changes the feature-cache key.

**Proposed method, absent from the core tree.** A CLAP adapter, training, the linear scorer, the neural challenger, calibration, and inference bundles are not implemented. Torch and Transformers stay out of the core environment. An authorized probe uses a separate environment.

## 8. Semantic cosine baseline

Let `a = normalize(E_audio(excerpt))` and `t = normalize(E_text(brief))`, each in R^512.

**Proposed method.** Architecture A is mandatory and has zero trained parameters: cosine similarity, invalid-audio checks, and optional fixed acoustic constraints. It learns nothing from preferences. It is broad semantic matching. Cosine similarity is the zero-training semantic baseline. With only 50–100 pairs, a compact pilot control may use four similarities — the full brief and up to three human-authored audible clauses — with explicit missing-clause masks. Coefficients and preprocessing for that control are fit on training data only. The control is not a substitute for the 1,537-coefficient model in section 9.

**Measured probe result.** On 10 October 2026 a CPU four-text check reused one audio `pooler_output` from the same Disquiet excerpt. Local output: `runs/clap-cpu-probe/semantic/20261010-150249/`. The audio vector’s float32 SHA-256 is `657881b15f2ee5dd2632939f0d698bc74b6f0a6da736c71cf2546e6f78fa4b77`, matching the feasibility run. Audio L2 norm `0.9999999873370299`. Mel shape `[1, 1, 1001, 64]`, `is_longer` false. No cutoff was applied. Python warnings: none. Worker return code 0. `stop` is null.

Descending cosine order:

| Text | Tokens | Cosine |
|---|---:|---:|
| Reflective, gentle piano music. | 10 | -0.0002889722135070734 |
| Solo piano instrumental music. | 8 | -0.0006666518625852746 |
| Loud distorted electric guitar music. | 9 | -0.0007077695082539841 |
| A person speaking during an interview. | 9 | -0.0012963386684998245 |

These are encoder similarities for one technical excerpt. They are not listener preferences. A cleanup later the same day recomputed these four values from `result.json` and they matched. The model was not reloaded.

`/usr/bin/time -l` maximum resident set size for this check was 1,039,990,784 bytes. The 100 ms poll peaked at 641,187,840 bytes. The final supervisor sample read pressure 2 after the worker had finished (5.32 seconds real), so the 10-second yellow stop did not fire.

## 9. Conditional linear pairwise ranker

**Proposed method.** Architecture B is the first trainable model. It is not implemented.

```text
phi(a,t) = concat(a, a*t, abs(a-t), dot(a,t))
512 + 512 + 512 + 1 = 1,537
s = w · phi(a,t)
```

`s` has 1,537 coefficients and no bias. Elementwise multiplication and absolute difference make the score depend jointly on the candidate and the brief. The candidate intercept is omitted because it cancels in every comparison.

For candidates A and B under one brief:

```text
d = s(A,t) - s(B,t)
p_train(A) = sigmoid(d)
```

Training minimizes binary cross-entropy on human non-tie choices plus L2 regularization. `p_train` is a training probability. It is not a validated public probability. Strong L2 is part of the design. The planning heuristic is several hundred labels. The model can represent weighted audio tendencies and fixed text–audio interactions. Nonlinear interactions beyond this map are outside B.

Naive linear text terms cancel. If the score is an audio term plus a text term,

```text
s(a,t) = w_a · a + w_t · t
```

then one shared brief gives

```text
s(A,t) - s(B,t) = w_a · (A - B)
```

`w_t · t` is the same for A and B, so the subtraction removes it. A model can carry a brief in its input schema and still ignore the brief in every pairwise decision. The interaction features in `phi` are there so the brief survives that subtraction. `a*t`, `abs(a-t)`, and `dot(a,t)` each change when the candidate changes.

Shared candidate scoring is the recommended decision rule: score each of N candidates once, sort, and use differences for pairwise decisions. That yields one scalar order under a fixed brief and listener. Human judgments may still contain cycles. Report that mismatch. A direct pairwise model that is not a difference of utilities has to enforce reversal symmetry, for example `d(A,B) = (h(A,B) - h(B,A)) / 2`. Symmetry does not remove cycles. Naive all-pairs ranking costs O(N²) comparisons. Listwise Plackett–Luce losses need reliable multi-item orderings. Six pairs derived from four ranked candidates are not six independent observations.

Coefficient inspection and controlled ablations are the interpretability available in B. Individual embedding coordinates are not musical concepts.

## 10. Neural challenger and deferred architectures

**Proposed method.** All head counts exclude the frozen encoder. The data amounts in the architecture note are planning heuristics, not measured learning curves.

| Architecture | Definition / count | MVP position |
|---|---|---|
| A. Deterministic baseline | Cosine; invalid-audio checks; optional fixed acoustic constraints. Zero trained parameters | Mandatory |
| B. Linear pairwise model | `s = w · phi(a,t)`; 1,537 coefficients; no bias | First trainable model |
| C. Small shared scorer | `[a, t, a*t, abs(a-t)] → 64 → 1`, GELU, dropout 0.1; **131,201 parameters** per target | Controlled challenger |
| D. Direct pair comparator | Antisymmetric MLP over both candidates and the brief; design budget ~0.25–1M | Defer unless C fails for a diagnosed reason |
| E. Compact decision Transformer | 2 layers, width 128, projected brief/audio/window tokens; proposed ~0.5–1M | No initial justification |
| F. Adapted audio encoder | Frozen backbone plus LoRA/adapters; proposed ~0.1–5M trainable, depending on target layers | Only after a representation diagnosis |

Architecture C’s input dimension is 2,048, which is `512 * 4`. That map includes the text vector itself. It does not append the scalar `dot(a,t)` that B uses as feature 1,537. One hidden layer has 64 units, GELU, dropout 0.1, and a scalar output. Dropout adds no parameters. The count is:

```text
2048*64 + 64 + 64*1 + 1 = 131,201
```

The `+ 64` term is the hidden bias. The `64*1` term is the hidden-to-output weight. The final `+ 1` is the output bias. Train two independent instances only when both target labels exist: 262,402 parameters in total. Separate models keep a missing label from being filled in by the other target, and they keep a large unrelated set from dominating the personal target. A shared multi-head trunk is a later ablation.

C is a challenger after eligible data and a baseline result. It is not the default first fit. Cached CPU training is the intended setting. Overfitting on a tiny set is the main risk. C through F offer less direct coefficient interpretation than B. None of them should emit a free-form musical explanation from a scalar score.

D is deferred because it needs more labeled comparisons, order tests, and an account of preference cycles. E is deferred because the sample demand is higher, interpretability is weaker, and attention does not supply calibration. F is deferred because adapter training still stores backbone activations, is likely to need rented GPU time, and leaves encoder and data rights in force. Alternate frozen layers or encoders come before adapters. Full encoder fine-tuning is out of scope for v0.1. It would mix representation learning, label noise, compute, and preference learning in the same small experiment.

## 11. Separate adherence and preference targets

**Proposed method.** Three output families stay distinct:

1. **Measurements.** Duration, sample rate, peak, clipping, RMS or loudness, and silence diagnostics. These come from signal processing and carry method identifiers. `gain_lufs_v1` is the accepted audition procedure in decision 0002.
2. **Adherence.** A learned ranking score for the listener’s explicit “better matches this brief” judgment.
3. **Preference.** A separately learned ranking score for a named listener or defined population, with its own labels and calibration.

A clip can match a brief without being preferred, and a preferred clip can miss the brief. The two scores are not averaged. Missing personal training means the preference target is unsupported. It is not filled with a generic quality score. Instrument labels, tempo estimates, ASR, emotion labels, and lyric correctness are not treated as facts inferred from CLAP similarity.

The direction note’s first falsifiable preference hypothesis is creator-specific pairwise preference against a fixed baseline, without folding adherence into the same objective. Adherence is the paired hypothesis on its own labels. Either hypothesis can fail. A negative result is a valid outcome. Those statements are H1 and H2 in the training plan. This note does not restate their gates.

Cold start uses the generic baseline and makes no claim about the individual. A later listener adjustment of the form `w_user = w_population + delta_user` is a proposed shrinkage, not an implemented model.

## 12. Resource safeguards

**Proposed method** in the dated handoff, and the standing rule in the status record. The 10 October probe ran under these limits.

| Rule | Threshold |
|---|---|
| RSS guardrail | 4,500,000,000 bytes, including loading |
| Red system pressure | Stop immediately |
| Yellow system pressure | Stop when yellow pressure is sustained for 10 seconds |
| Swap growth | Stop on 128 MiB of swap growth over 15 seconds |

The handoff operationalizes the swap window as growth across three 5-second samples totaling at least 128 MiB. That is the same 15-second window. Existing swap is logged and is not, by itself, a failure. The handoff also says to stop immediately when RSS exceeds 4,500,000,000 bytes. A supervisor has to be able to terminate the worker. `/usr/bin/time -l` reports a maximum; it does not enforce the stop.

The handoff’s pre-attempt wording for yellow pressure is “pause/stop.” The status record states a stop. The earlier same-day attempt ended in worker status `-9`.

One probe is bounded to 30 minutes in the handoff, and a timeout is inconclusive. A suggested usability target of 20 clips in 10 minutes or less after load is not a scientific success criterion.

## 13. Reconciliation of the 10 October 2026 probe

The dated handoff is a pre-attempt contract. Its header says specifications were verified, no weights had been downloaded, no encoder had run, and no Mac benchmark had been performed. It says go to a bounded CPU probe and no-go to claiming confirmed Mac feasibility. Hashes in that file are labeled publisher-reported. Decision 0002’s closing sentence, “no weights were downloaded and no encoder ran,” describes that foundation session (“not done here”). It does not describe the later isolated probe. Decision 0002 still bars CLAP in the foundation config.

**Measured probe result.** Single-clip CPU extraction succeeded on 10 October 2026. The status check covered `runs/clap-cpu-probe/retries/20261010-144504/` and the copies at `runs/clap-cpu-probe/`. Scope: one technical excerpt on CPU. Host: macOS arm64, 8,589,934,592 bytes physical memory. The status record does not name the SoC.

| Check | Evidence |
|---|---|
| Checkpoint | Primary revision, byte length, and SHA-256 in section 5. `weight_ok: true` |
| Embeddings | Three in-process passes and one fresh process. Audio and text shape `[1, 512]`, finite on every pass. L2 norms `0.9999999873370299` (audio) and `0.9999999792360142` (text) |
| Repeatability | In-process and fresh-process audio and text are bit-identical. Max absolute error `0`. Fresh cosine `1.0` |
| Cold peak RSS | 1,103,282,176 bytes (about 1.10 GB), from `/usr/bin/time -l`, equal to the polled peak. Under the 4,500,000,000-byte guardrail |
| Fresh-process RSS | `/usr/bin/time -l` maximum 1,096,663,040 bytes (`ru_maxrss` 1,096,646,656). The 100 ms poll peaked at 755,826,688 bytes and missed that maximum on a 2.89-second process |
| Host pressure | Pre-run watch: 60 samples, last at 60.879 seconds, pressure 1, swap used constant at 557,192,314 bytes. Supervisor preflight and both run traces stayed at pressure 1 |
| Stop | `stop` is null. Cold and fresh worker return codes are 0 |

The technical excerpt is Disquiet, 30–40 seconds: mono float32, 48 kHz, 480,000 samples. Recomputed PCM SHA-256 `f78adc9e79b8bc0a115df25ae981d7daccef63d1c08924cf3b07c1b116fd4507`. Observed mel shape `[1, 1, 1001, 64]`. The separate environment was Python 3.11.16, PyTorch 2.14.1, and Transformers 5.19.0. MPS was built and available. The run stayed on CPU. MPS parity is unverified.

An earlier attempt the same day stopped on yellow pressure sustained for 10 seconds, worker status `-9`, polled peak 151,371,776 bytes. The retained prior directory has no completed `cold.json`. Those logs remain in `retries/20261010-144504/prior/`. That attempt is not the successful run.

The handoff’s original 1.5–4 GB RSS envelope was an unverified planning range. The measured cold peak for this one clip, about 1.10 GB, sits under the guardrail and under that envelope. One excerpt does not measure 20-clip peak RSS. Weight-file size and peak RSS are different quantities: the file is 776,444,665 bytes and the cold peak was 1,103,282,176 bytes.

**The 20-clip throughput benchmark has not been run.** Distinct-clip throughput, the embedding cache under CLAP vectors, and CPU/MPS parity are unmeasured.

**The three-clip runner has not been executed.** `runs/clap-cpu-probe/semantic_three.py` reuses the single-clip supervisor limits, the pinned `larger_clap_music` checkpoint, and the `pooler_output` call. A no-model check confirmed the three `data/probes/clap-tech-3` excerpts and the checkpoint hash. No three-clip cosine matrix is recorded.

No preference model has been trained. `production_claim_allowed` stays false. The single-clip run does not open the foundation encoder gate.

The handoff’s proposed numerical gates — finite `(1, 512)` outputs, norms within `1e-5`, same-device `allclose(rtol=1e-5, atol=1e-6)`, and MPS-versus-CPU `allclose(rtol=1e-3, atol=1e-4)` with vector cosine at least `0.9999` — are project tolerances. They are not upstream guarantees. The CPU repeat on this excerpt met bit identity, which is inside the same-device tolerance. The MPS gate was not applied.

## 14. Limitations

- The probe result is one technical excerpt. Technical preparation does not establish musical acceptance or a completed listening dataset.
- The four cosines are encoder similarities. They supply no listener judgment and no test of whether frozen CLAP carries a preference signal.
- There is no core CLAP adapter. Foundation validation still accepts only `dummy` / `fixture-v1`.
- MPS was available and was not used. CPU/MPS parity is unverified.
- The 20-clip benchmark has not been run. The three-clip runner has not been executed.
- No linear scorer and no neural challenger have been trained. No calibrated probability is claimed.
- The ~194M and ~154M CLAP counts are storage-derived. The release registry still needs measured `numel()` counts.
- The architecture note’s A18 Pro runtime statement was not updated by a host line that does not name the chip.
- The fallback checkpoint hash has not been recomputed in the status record.
- The handoff file still says that no encoder ran and that hashes were not recomputed locally. Those sentences are historical. Section 13 is the result.
- Decision 0002 does not enumerate numeric probe gates. The numeric tolerances live in the handoff and are labeled there as proposed.
- Fixture success, cache tests, and dummy embeddings are software contracts.
- Published Apache-2.0 weight terms do not clear training data or P-01 release. P-01 release permissions remain `unknown` in the status record.
- The fresh-process RSS poll undersampled a short process. The `/usr/bin/time -l` maximum is the fresh-process peak cited above.
- A pressure reading of 2 on the four-text check arrived after the worker had exited. It is not the earlier yellow-pressure stop.

## 15. Unresolved questions

- Whether frozen CLAP embeddings can carry this creator’s preference signal, or the adherence signal, on held-out families.
- CPU/MPS parity, including max coordinate error, cosine-score error, and any winner change under the handoff’s `2δ + 1e-5` sign rule.
- Distinct-clip throughput, per-stage latency, and CLAP cache behavior on 20 prepared hashes.
- The result of the three-clip runner. The script is recorded as ready and unexecuted.
- Exact loaded parameter counts for the pinned primary and fallback artifacts.
- Whether the successful worker’s loader flags included `weights_only=True`. The status narrative records hashes, shapes, norms, and RSS. It does not restate the loader flags.
- Which numeric tolerances decision 0002’s phrase “until the probe gates pass” incorporates, beyond the handoff’s proposed gates.
- The chip identity of the probe host, relative to the architecture note’s unmeasured A18 Pro runtime.
- The eight archive conflicts still listed as open in `docs/STATUS.md`, including HeartCLAP weights and MusicFM provenance. Local deployment (archive item 8) now has one CPU excerpt’s pins, mel shape, and peak RSS. MPS parity and extraction throughput remain unmeasured, so that item is not closed.
- A finalized creator brief, musically accepted 10-second crops, and human judgments. The Disquiet 30–40 second waveform does not close those gates.
- The fallback snapshot’s locally recomputed weight hash.

## 16. Sources

Repo-relative paths. The status figures in this note follow the 10 October 2026 record.

| Path | Used for |
|---|---|
| `docs/archive/research-preconsolidation-2026-10/03_Audio_Encoder_and_Architecture_Analysis.md` | Shortlist, licenses, feature algebra, architectures, separate targets |
| `docs/archive/research-preconsolidation-2026-10/03_CLAP_Encoder_Feasibility_and_Benchmark_Handoff.md` | Pre-attempt pin table, processor contract, safeguards, proposed gates |
| `docs/STATUS.md` | Measured probe, four cosines, what is implemented, what remains unrun |
| `docs/decisions/0002-audition-normalization.md` | `waveform_for_encoder`, 480,000-sample contract, `pooler_output` adapter rules |
| `docs/decisions/0001-foundation-choices.md` | Dummy encoder identity and cache-key fields |
| `docs/decisions/0004-votelle-naming.md` | Canonical names and retained historical spellings |
| `docs/PROJECT_DIRECTION.md` | Representation order only |
| `src/votelle_music/features/base.py` | `AudioTextEncoder`, `FeatureBatch`, `l2_normalize`, `FeatureError` |
| `src/votelle_music/features/cache.py` | Canonical cache-key payload |
| `src/votelle_music/features/dummy.py` | `dummy` / `fixture-v1` |
| `src/votelle_music/audio/prepare.py` | `TARGET_SAMPLES`, `waveform_for_encoder` |
| `src/votelle_music/schemas.py` | `EncoderSpec`, `canonical_bytes`, `VotelleError` |
| `src/votelle_music/data/manifest.py` | Foundation refusal of every encoder other than `dummy` / `fixture-v1` |
