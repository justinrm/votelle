# 03 — CLAP Encoder Feasibility & Benchmark Handoff

Music Preference Model v0.1 · Verified October 10, 2026 UTC / October 9 Pacific

**ENCODER: GO to a bounded CPU probe; NO-GO to claiming confirmed Mac feasibility.** Specifications and source contracts are verified; no weights were downloaded, no encoder ran, and no Mac benchmark was performed. All execution commands below are an **untested local handoff**, to run only after Cursor’s offline Session 1 passes.

## Pinned artifacts

| Property | Primary | Resource fallback |
|---|---|---|
| Hugging Face ID | laion/larger_clap_music | laion/clap-htsat-unfused |
| Immutable revision | a0b4534a14f58e20944452dff00a22a06ce629d1 | 8fa0f1c6d0433df6e97c127f64b2a1d6c0dcda8a |
| Weight filename | pytorch_model.bin | pytorch_model.bin |
| Exact published file bytes | 776,444,665 | 614,525,833 |
| Published LFS SHA-256 | 5c289311f4a030d768af7ffbfdecd01b008aa64824211899a4e59f4f9d154fd1 | 1cd3c601bc4afe0fa87be3de4c13dd2cfadd249fac1e29acf74a9b296c3219bb |
| Audio tower | HTSAT/Swin, depths 2/2/12/2; final width 1024; patch width 128 | HTSAT/Swin, depths 2/2/6/2; final width 768; patch width 96 |
| Shared projection | 512 audio / 512 text | 512 audio / 512 text |
| Text tower | RoBERTa-style, hidden width 768 | Same hidden width |
| Published weight license | Apache-2.0 model-card declaration | Apache-2.0 model-card declaration |

Evidence: official [primary tree](https://huggingface.co/laion/larger_clap_music/tree/a0b4534a14f58e20944452dff00a22a06ce629d1), [fallback tree](https://huggingface.co/laion/clap-htsat-unfused/tree/8fa0f1c6d0433df6e97c127f64b2a1d6c0dcda8a), and direct model metadata APIs [primary](https://huggingface.co/api/models/laion/larger_clap_music?blobs=true) / [fallback](https://huggingface.co/api/models/laion/clap-htsat-unfused?blobs=true). Hashes are publisher-reported, not locally recomputed weight hashes. Both repositories expose main, five commits and no tags at review. Pin the complete revisions above; neither main nor a short hash is the reproducibility record.

Both snapshots contain README.md, config.json, preprocessor_config.json, tokenizer_config.json, tokenizer.json, vocab.json, merges.txt, special_tokens_map.json, .gitattributes and the single .bin weight file. No safetensors weight was listed. Save card/license evidence with the snapshot. Use restricted weight loading; do not enable remote code, untrusted pickle execution, or silently source an unofficial conversion.

Transformers implementation is Apache-2.0. The separate [native LAION repository license](https://github.com/LAION-AI/CLAP/blob/main/LICENSE) is CC0. Its [music checkpoint family](https://github.com/LAION-AI/CLAP) includes music_audioset_epoch_15_esc_90.14.pt; those .pt files and the laion_clap package are a different packaging/integration route. Do not silently substitute them. Published encoder licenses do not warrant all training-data rights or prove absence of overlap with Incompetech.

## Exact processing and return contract

Use the selected revision’s processor assets and a pinned Transformers implementation. Both [primary](https://huggingface.co/laion/larger_clap_music/blob/a0b4534a14f58e20944452dff00a22a06ce629d1/preprocessor_config.json) and [fallback](https://huggingface.co/laion/clap-htsat-unfused/blob/8fa0f1c6d0433df6e97c127f64b2a1d6c0dcda8a/preprocessor_config.json) specify 48,000 Hz, 480,000 samples, 10 seconds, 64 mel bands, FFT 1024, hop 480, 50–14,000 Hz, repeatpad and rand_trunc. These processor defaults do not authorize padding or cropping research items automatically.

Our adapter must accept a finite float32 mono waveform of exactly 480,000 samples, already prepared under document 02. Pass sampling_rate=48000 explicitly; the extractor validates it and does not resample for you. Reject wrong duration/rate before calling it. At exactly this length the [v5.19.0 implementation](https://github.com/huggingface/transformers/blob/v5.19.0/src/transformers/models/clap/feature_extraction_clap.py) takes the no-random-crop path; longer inputs can select a random crop and shorter inputs can repeat/pad. Both models use unfused extraction. Expect the unfused mel tensor to have shape (1, 1, 1001, 64), despite the saved configuration’s nb_max_frames=1000; record the observed shape locally rather than forcing 1000 frames.

Text uses the snapshot’s RoBERTa tokenizer. The [primary tokenizer](https://huggingface.co/laion/larger_clap_music/blob/a0b4534a14f58e20944452dff00a22a06ce629d1/tokenizer_config.json) declares 512 tokens, including special-token accounting. Use plain original English briefs, no automatic prefix/rewrite; tokenize with truncation=False, inspect length, and reject >512. Record token IDs/mask hash. Tokenizer metadata and model max_position_embeddings are different concepts; do not use 514 as the brief limit.

**Version-sensitive correction:** [Transformers 5.19.0 source](https://github.com/huggingface/transformers/blob/v5.19.0/src/transformers/models/clap/modeling_clap.py) returns a model-output object from get_audio_features/get_text_features. With return_dict=True, use its **pooler_output**, which is the projected, L2-normalized vector. Do not cache last_hidden_state or assume the return is a tensor. Explicitly validate norms and reject zero/nonfinite vectors; re-normalizing is optional but must be versioned. Full-model logits include learned scaling and are not preference probabilities.

## Environment and known integration risks

**Candidate pins, metadata/source-verified but not installation-tested:** Python 3.11, torch==2.14.1, transformers==5.19.0. PyPI documents Python ≥3.10 for both and publishes torch-2.14.1-cp311-cp311-macosx_14_0_arm64.whl. [Torch](https://pypi.org/project/torch/2.14.1/); [Transformers](https://pypi.org/project/transformers/5.19.0/). Resolve and lock all transitive packages on the actual Mac, including NumPy, tokenizers, huggingface-hub, safetensors and psutil. Reuse the tested core soundfile/SciPy pins where compatible; otherwise isolate this probe environment. Do not change the Session 1 core environment to fix an optional encoder conflict.

No torchaudio, torchvision, datasets, laion_clap, CUDA, Accelerate/device_map or general audio extra is required for this narrow array-input route. The CLAP mel extractor uses CPU NumPy DSP. A clean minimal environment also avoids unrelated optional audio/vision import conflicts. Any missing backend must be diagnosed rather than addressed by installing an entire framework stack.

Apple verifies [A18 Pro / 8 GB unified memory](https://www.apple.com/macbook-neo/specs/). [PyTorch MPS documentation](https://docs.pytorch.org/docs/2.14/notes/mps.html) requires checking is_built/is_available; this does not prove CLAP’s convolution, bicubic interpolation, attention and normalization paths work on this specific device. No reproducible A18 Pro CLAP failure or success was established here. CPU remains the reference; MPS is optional. Standard PyTorch does not automatically use the Neural Engine.

Risks to test: old card examples omit resampling and use audios=; current generic processor uses audio-oriented dispatch. Use the feature_extractor and tokenizer directly below. Native examples use CUDA device 0, which is not a Mac instruction. Pickle-only snapshots require the supported weights_only loader. Returned output objects can retain intermediate tensors: detach/copy only the 512-vector and discard each output before the next clip. Disable gradients and dropout with inference_mode and eval. Do not use FP16, quantization or fusion as an unreported workaround.

## Local setup and acquisition — after Session 1

Run in a separate local benchmark directory, outside the active repository. These commands neither exist nor execute in Cursor automatically. Confirm native arm64 and use a Python 3.11 binary already installed; if absent, install it separately without replacing global Python 3.14.

~~~bash
uname -m
sw_vers
sysctl -n hw.memsize
python3.11 -m venv .venv-clap-probe
source .venv-clap-probe/bin/activate
python -m pip install 'torch==2.14.1' 'transformers==5.19.0' psutil soundfile scipy
python -m pip check
python -m pip freeze > environment.lock.txt
python -c 'import torch,transformers; print(torch.__version__,transformers.__version__); print(torch.backends.mps.is_built(),torch.backends.mps.is_available())'
~~~

The first resolution’s supporting dependencies are unpinned; environment.lock.txt becomes the run’s complete exact-version record. Recreate a second clean environment from that lock for reproduction. Store Python patch version, wheel hashes or a hash-locked requirements file, platform, macOS build and pip resolver report before calling the environment reproducible.

Acquire **one** official snapshot, separately from load timing:

~~~python
from huggingface_hub import snapshot_download
snapshot = snapshot_download(
    repo_id="laion/larger_clap_music",
    revision="a0b4534a14f58e20944452dff00a22a06ce629d1",
    local_dir="models/larger_clap_music",
    allow_patterns=["README.md", "config.json", "preprocessor_config.json",
                    "tokenizer_config.json", "tokenizer.json", "vocab.json",
                    "merges.txt", "special_tokens_map.json", "pytorch_model.bin"],
)
print(snapshot)
~~~

~~~bash
shasum -a 256 models/larger_clap_music/pytorch_model.bin
du -sk models/larger_clap_music
~~~

Compare with the expected hash before loading. Record hashes for every processor/config/tokenizer file. All subsequent benchmark loading uses the local directory with HF_HUB_OFFLINE=1; no timed run downloads anything.

**Minimal API contract for Cursor to incorporate, not a complete benchmark:**

~~~python
import numpy as np
import torch
from transformers import ClapModel, ClapProcessor

path = "models/larger_clap_music"
processor = ClapProcessor.from_pretrained(path, local_files_only=True)
model = ClapModel.from_pretrained(
    path, local_files_only=True, trust_remote_code=False,
    use_safetensors=False, weights_only=True, dtype=torch.float32,
).eval()
model.requires_grad_(False)
# prepared_waveform and exact_brief come from the validated manifests.
wave = np.asarray(prepared_waveform, dtype=np.float32)
assert wave.shape == (480000,) and np.isfinite(wave).all()
audio_inputs = processor.feature_extractor(
    wave, sampling_rate=48000, return_tensors="pt",
    truncation="rand_trunc", padding="repeatpad",
)
text_inputs = processor.tokenizer(
    [exact_brief], truncation=False, padding=True, return_tensors="pt",
)
assert text_inputs["input_ids"].shape[1] <= 512
with torch.inference_mode():
    a = model.get_audio_features(**audio_inputs, return_dict=True).pooler_output
    t = model.get_text_features(**text_inputs, return_dict=True).pooler_output
assert a.shape == t.shape == (1, 512)
assert torch.isfinite(a).all() and torch.isfinite(t).all()
assert torch.allclose(a.norm(dim=-1), torch.ones(1), atol=1e-5)
assert torch.allclose(t.norm(dim=-1), torch.ones(1), atol=1e-5)
audio_vector = a.detach().cpu().numpy().astype(np.float32, copy=True)
text_vector = t.detach().cpu().numpy().astype(np.float32, copy=True)
~~~

For MPS, launch a fresh process, move model and feature/token tensors to mps, and synchronize before/after each timed operation. Keep preprocessing on CPU. Do not set automatic CPU fallback for the first MPS test; a missing operator must be visible. A later explicitly labeled mixed-device trial is optional, not pure-MPS evidence.

## Bounded benchmark specification

Cursor should implement a standalone supervised runner in its next bounded session; no runner was created or executed here. Start with **one cleared clip + one brief**, then continue to 20 unique clips only if safe. The document 01 shortlist provides 12 candidates + 8 reserve tracks; repeated processing of one file does not satisfy the 20-clip requirement.

| Measurement | Required procedure and retained output |
|---|---|
| System baseline | Save idle vm_stat and sysctl vm.swapusage, Activity Monitor memory-pressure state, available disk, open heavy applications, power mode and thermal context. Save Cursor’s work before scheduling a controlled run. |
| Cold load | Fresh child process, locally cached weights, stopwatch around processor/model load; report imports separately and total startup too. Include load peaks. This is process-cold, not an OS page-cache-cold claim; do not purge caches. |
| Peak memory | Supervisor starts before Torch imports and samples child/descendant RSS every 100 ms. Record macOS resource.getrusage peak and /usr/bin/time -l as independent maxima. State bytes versus KiB explicitly. |
| Preparation | For each clip time disk read, validated preparation/cache lookup, mel extraction, model forward and return-to-CPU separately; report true uncached end-to-end latency as well. |
| Audio + text | Batch 1, FP32, eval/inference mode; 2 CPU threads initially, 1 interop thread, no data-loader workers. Save exact loaded parameter count, dtype, feature shapes, finite/norm checks and all software identities. |
| Repeatability | Three extractions of the same fixed waveform/text in-process, plus one fresh-process repeat, with seeds and thread count held fixed. Save max absolute error, cosine agreement and whether bit-identical. Never promise cross-platform bit identity. |
| 20-clip throughput | One warm-up outside the measured list; disable embedding-cache reads; process 20 distinct prepared hashes once, one at a time. Report successful count, failures, total wall time, clips/minute and per-stage median/p95. Label p95 from n=20 descriptive. |
| Cache | Save 20 audio vectors and deduplicated brief vectors, no pickled object arrays; record actual bytes, hit latency, keys and checksums. |
| MPS | Only after CPU pass, use the same 20 inputs in a new process with fallback disabled. Record is_built/is_available, operator errors, synchronized times, and current_allocated_memory / driver_allocated_memory where supported. Device and process memory overlap on unified memory; do not sum them as independent RAM. |
| CPU/MPS parity | Compare normalized audio/text vectors and their cosine scores. Record max coordinate error and maximum cosine-score error δ; inspect any winner change. All comparisons with CPU margin >2δ + 1e-5 should retain sign. Tiny-margin changes are numerically fragile, not a new listener preference. |

**Proposed numerical gates:** finite (1,512) outputs and norms within 1e-5; repeated same-device output allclose(rtol=1e-5, atol=1e-6); MPS versus CPU allclose(rtol=1e-3, atol=1e-4) and vector cosine ≥0.9999. These are project tolerances, not measured results or upstream guarantees. A CPU repeatability failure blocks feature caching until explained. MPS-only failure does not block CPU use.

**Resource stop:** retain the existing 4.5 GB RSS guardrail, operationalized as **4,500,000,000 bytes**, including loading. Stop immediately on exceeding it or red system pressure. Pause/stop on yellow pressure sustained for 10 seconds or swap growth across three 5-second samples totaling ≥128 MiB. These duration/swap thresholds clarify “sustained,” and are proposed conservative operational settings. Log initial swap; existing swap alone is not a new failure. A supervisor must terminate a stuck/over-budget worker rather than relying only on a final /usr/bin/time report. Do not disable allocator safety limits.

Bound one probe to 30 minutes total; mark timeout as inconclusive. A suggested usability target is 20 clips in ≤10 minutes after load, but slower safe CPU extraction can still be viable for an offline pilot. Record actual throughput before deciding; the time target is not an original scientific success criterion.

Useful macOS observation commands (read-only):

~~~bash
vm_stat
sysctl vm.swapusage
/usr/bin/time -l env HF_HUB_OFFLINE=1 PYTORCH_ENABLE_MPS_FALLBACK=0 python benchmark_clap.py --device cpu --manifest probe20.jsonl
~~~

The final command is a **proposed interface for the runner Cursor must create**, not a currently installed project CLI. Run the memory supervisor around that worker; /usr/bin/time alone does not enforce the stop. Use Activity Monitor’s Memory tab for system pressure if the local memory_pressure command/interface is unavailable. Repeat with --device mps only after the CPU gate passes. Do not run both models/devices concurrently.

## Memory, storage and fallbacks

The original 1.5–4 GB RSS estimate remains an unverified planning envelope. Weight-file size is not peak RAM. The smaller file saves **161,918,832 bytes (~20.9%)**, so it may not rescue a large activation/loading problem. Measure it independently under the same guardrail; switch encoder cache namespace and repeat all validation.

Derived storage: float32 mono PCM is 1.92 MB/clip; 20 clips =38.4 MB, P0’s 60=115.2 MB, excluding originals/duplicates. Each 512-vector is 2,048 bytes; P0 audio+20 briefs =163,840 numeric bytes, plus metadata/container overhead. Primary snapshot is ~0.780 GB; both snapshots ~1.399 GB. Retain the original 10–20 GB free-disk allowance for environments, sources, caches and logs.

| Fallback | Incremental expense / implication | Recommendation |
|---|---|---|
| Smaller CLAP on CPU | $0 service spend; ~0.618 GB snapshot; same 512-d interface, different feature space | First fallback after primary resource failure; new cache and comparison, no mixing vectors |
| One-time free Colab extraction | $0 if resources available; transfer 38–115 MB prepared clips for this probe/P0, return <1 MB vectors + manifests | Cheapest remote route; keep identical checkpoint/software/preparation and actively run notebook; [free resources are not guaranteed](https://research.google.com/colaboratory/intl/en-GB/faq.html) |
| One-time rented extraction | Current [Runpod listing](https://www.runpod.io/pricing): A5000 $0.27/hour; container/running volume $0.10/GB/month | Estimate only, not authorized: 1–2 hours = $0.27–$0.54 compute; 10 GB stored a full month ~$1, idle volume ~$2. Actual setup, billing minimums, availability and transfer must be checked. No paid action under this session’s constraints. |
| Lightweight audio-only model | Additional audit, dependency stack and no equivalent text alignment | Not justified yet. Fixed acoustic diagnostics can test plumbing but do not replace the chosen semantic representation. Prefer remote extraction over redesign. |

Remote upload requires permission for that processing location/service and any contributor privacy terms. Use one batch, verify cache checksums/dimensions, save locally and shut down/delete remote runtime artifacts. No permanent GPU hosting or hardware purchase is recommended.

**Cursor return packet:** Session 1 status/commit and test result; lock and platform record; model/processor hashes; cleared 20-clip and brief manifests; preparation version; numerical checks; full timings; RSS/device/swap/pressure traces; failures and stop reasons; cache manifest; CPU/MPS decision. The next step after a pass is P0 extraction/listening, not model training or architectural expansion.
