# 07 — Development Roadmap and Budget

Research v0.1 · October 9, 2026 · Authority for resource planning

## Hardware verdict

Apple's published specifications confirm an A18 Pro MacBook Neo configuration with 8 GB unified memory. This is enough for an inexpensive cached-feature experiment. It is not a sensible platform for training a music foundation model. PyTorch documents MPS acceleration on supported macOS/Metal devices; actual model/operator support must be checked at runtime. The presence of an Apple Neural Engine does not mean ordinary PyTorch code uses it. [S51](https://www.apple.com/macbook-neo/specs/), [S52](https://www.apple.com/newsroom/2026/03/say-hello-to-macbook-neo/), [S53](https://docs.pytorch.org/docs/stable/notes/mps.html)

Use CPU first, one encoder per process, batch 1, FP32 and short clips. Test MPS against CPU for finite outputs and ranking consistency. Close memory-heavy applications during extraction. Small heads do not need GPU rental. Quantization, MLX conversion and Core ML export are optional later optimizations with their own parity checks.

## Planning envelopes—not machine benchmarks

Peak memory depends on dependency versions, model-loading duplication, attention buffers and the OS. These broad **estimates** are intended for deciding what to measure first.

| Task | Estimated process memory | Device / main bottleneck | Runtime approach |
|---|---|---|---|
| Decode, resample, diagnostics for one excerpt | ~0.1–0.8 GB including libraries | CPU; decoding and file I/O | Time 20 files; processing should be a small fraction of the project |
| CLAP music extraction, 10 seconds, batch 1 | ~1.5–4 GB; temporary loading may exceed steady state | CPU or tested MPS; encoder dominates | Measure cold load plus warm p50/p95; no A18 Pro timing verified |
| Smaller CLAP extraction | ~1–3 GB | CPU/MPS, one worker | Resource fallback, requiring new feature namespace |
| Linear training on cached 1,000–10,000 pairs | ~0.2–1 GB | CPU; solver/feature arrays | Usually a small job; record actual solver time and convergence |
| Tiny MLP training on cached features | ~0.5–1.5 GB total process | CPU generally sufficient; framework overhead dominates head storage | Measure epochs/sec; stop at predeclared budget |
| Head-only pair inference | Negligible head tensors relative to interpreter | CPU | Separate from uncached audio-to-decision latency |
| MuQ-MuLan, MERT2, multiple encoders | Several GB each plus buffers | 8 GB headroom becomes unreliable | Sequential extraction or rented GPU only if justified |
| Encoder adapters / larger audio LLM | Not committed to local feasibility | Backprop/attention memory | GPU experiment only after diagnostic evidence |
| Generator-based dataset production | Separate environment and budget | Generator memory/runtime | Not required for the first owned-audio pilot |

Adopt a provisional extraction stop threshold of 4.5 GB process RSS or sustained swap growth/memory pressure on the actual Mac. This is a project guardrail, not a documented hardware limit. Record peak unified/device allocations as well as process RSS where possible; neither alone represents total system pressure.

### Storage arithmetic

- 10 seconds × 48,000 samples/sec × 1 channel × 4 bytes ≈ **1.92 MB** per float32 mono excerpt. 640 clips ≈ **1.23 GB**, before retained originals and audition derivatives.
- 640 × 512 × 4 bytes ≈ **1.31 MB** for one pooled audio-embedding matrix. 160 brief vectors add ~0.33 MB. Pair tables should reference vectors instead of duplicating audio.
- A 131,201-parameter FP32 head contains ~0.525 MB of weights. Optimizer state, gradients and the Python process add overhead but remain tiny beside the encoder.
- Reserve **10–20 GB free disk** for a scoped pilot: environment, one encoder, audio/derivatives, cache and results. Avoid downloading whole multi-dataset archives.

All sizes are decimal-derived estimates. The published HF CLAP file size is documented in 03; downloads and raw tensor memory are not necessarily equal.

### Runtime and cost formulas

Let N be unique clips, t the measured extraction seconds/clip, L the cold-load time, and B the effective batch throughput factor. Estimate `total_seconds = L + N*t/B`; include retries and data transfer separately. For illustration only, at t=5 seconds, 640 clips take ~53 minutes plus load; at t=30 seconds, ~5.3 hours. These examples are not claims about your Mac.

Local cloud/API cost per evaluation is $0, excluding electricity, hardware and time. Rented extraction cost per clip is `hourly_rate * elapsed_hours / successful_unique_clips`, including idle and retry overhead. Head-only timing must not be advertised as end-to-end latency.

## Three compute budgets

These are spending ceilings and planning allocations, not authorized jobs. Annotation, taxes and opportunity cost are separate.

| Tier | Proposed allocation | Evidence gate | Expected role |
|---|---|---|---|
| 1: essentially free | **$0 incremental cloud/API spend**; own audio and self-labels | Rights-cleared pilot; local extractor fits | Complete core pipeline, linear model, small MLP, scoped result |
| 2: up to $50 | Target $10–20 one-off extraction/comparison, ≤$10 storage/transfer, remainder contingency | Measured local bottleneck or a necessary external comparator | Rent one 16–24 GB GPU briefly; shut it down when cache is complete |
| 3: up to $250 | Up to $60 extraction/comparator runs, $60 bounded representation/adaptation experiments, $30 storage/transfer, $100 reserve | Evidence of useful signal and a specific unresolved research question | More generators/encoders or modest adapter ablation, not foundation pretraining |

A current provider example is Runpod's published pod listing of RTX A5000 24 GB at $0.27/hour and RTX 4090 24 GB at $0.89/hour. Availability and SKU pricing vary; serverless is a different billing product. At those displayed pod rates, 10 GPU-hours is $2.70 or $8.90 **before storage, startup, idle time and other charges**. This is arithmetic, not a job cost forecast. Recheck the live quote before any rental; no account action was taken. [S54](https://www.runpod.io/pricing)

The easiest way to waste the $50 budget is leaving a machine running or repeatedly extracting identical audio, not fitting a small head. Prefer a fixed batch, cache verification and immediate shutdown over an always-on endpoint.

## Roadmap with evidence gates

Effort estimates assume one developer, familiar Python tooling and available audio. At 6–10 focused hours/week, the core feasibility project is more plausibly **4–8 weeks** than a weekend. Data collection can extend it. These are estimates, not deadlines.

| Phase | Work / effort estimate | Completion gate | Stop or redirect if… |
|---|---|---|---|
| 0. Research validation | Review this package, choose target and rights lane; 2–4 hr | Decisions recorded; 20 pilot families feasible; encoder license evidence captured | No suitable audio or target too broad |
| 1a. Offline foundation | Manifests, validators, split graph, fixtures, deterministic preparation; 4–8 hr | Document 08 first-session acceptance passes | Data identity/rights cannot be represented honestly |
| 1b. Local probe and labels | 20-clip extraction probe, P0 labeling, cache; 4–8 hr plus listening | Fits resource budget; stable labels; deterministic features | Sustained swap, broken preprocessing, unclear brief question |
| 2. First trained experiment | Expand to P1; fit baselines/linear/MLP; 6–12 hr engineering plus 15–25 hr labeling | Locked held-out report with group intervals and baselines | No improvement, excessive instability or leakage |
| 3. Research iteration | One or two selected ablations, optional adaptation; 4–10 hr each | Specific hypothesis resolved; fresh confirmation justified | Repeated architecture changes chase test noise |
| 4. Research release | Documentation, model/data cards, rights audit and clean reproduction; 4–8 hr | Reproducible artifact with honest scope; weights only if permitted | Unresolved rights or unsupported claims |

Do not repeatedly enlarge the study to rescue a preferred architecture. Allocate one initial experiment and at most two predeclared expansions before reconsidering the target. Publish the useful engineering and learning result even if the best model remains cosine or linear ranking.

## Least expensive valid path

Complete the offline first session, label P0 using original material, measure one CLAP extraction run, and fit a compact/linear baseline. This isolates the two biggest unknowns—label signal and local representation cost—without buying hardware or generating thousands of songs. GPU rental is an optimization after measurement, not a prerequisite.
