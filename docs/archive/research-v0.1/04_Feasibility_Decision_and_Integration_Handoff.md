# 04 — Feasibility Decision & Integration Handoff

Music Preference Model v0.1 · October 9, 2026 Pacific / October 10 UTC

**Advance to the smallest real-data test, conditionally. Do not begin training.** A concrete audio source and reproducible encoder specification now exist; the actual listening set and Mac execution remain unverified.

## Ten decision answers

| Question | Answer and gate |
|---|---|
| 1. Can we assemble P0 with sufficiently cleared audio? | **Plausibly yes, not yet demonstrated.** Incompetech offers substantial capacity and an explicit training invitation. Twenty meaningful, independent families and 60 reviewed excerpts still need curation; there are currently zero acquired/validated recordings in this session. |
| 2. Immediately usable sources? | The selected Incompetech route is available under published CC BY terms plus the creator’s AI-training offer, subject to per-track review/attribution. Fully owned originals can qualify when supplied and declared. Contributions, MusicNet/Musopen, Music Arena and ACE-Step outputs remain conditional. Jamendo, mixed AIME and Suno are excluded from the default commercial-ready lane as audited in 01. |
| 3. Manual annotation burden? | Preliminary test: 12 comparisons +2 repeats, roughly 11–18 active minutes. P0: 60+10 comparisons, 53–88 active minutes; plan 2–4 hours with orientation/breaks. Separately estimate 3–6 hours to source/prepare P0. No crowdworker cost if Justin is the sole musician/listener. |
| 4. Most likely dataset bottleneck? | Finding three musically plausible alternatives per brief while preserving provenance and independent source/brief groups. Raw song count is no longer the primary obstacle. |
| 5. Is music CLAP plausible on this Mac? | **Yes as an engineering hypothesis.** Published weights are 776 MB; batch-one FP32 CPU execution is supported in principle. The 8 GB hardware spec does not prove sufficient peak headroom. |
| 6. What must be measured? | Loading peak, system pressure/swap, 20-unique-clip throughput, audio/text shapes and normalization, repeatability, actual dependency installation, and optionally synchronized CPU/MPS parity. Retain the 4.5 GB RSS stop. |
| 7. Cheapest fallback? | Smaller CLAP locally first, at $0 incremental service spend. If that fails, one-time free Colab extraction with availability and upload-permission gates. Paid GPU rental is only a separately authorized contingency. |
| 8. What can begin while Cursor works? | Review the exact 12-file shortlist, inventory genuinely owned originals, write/finalize four brief texts, and prepare per-asset rights evidence. No repository access, encoder download, training, contact with artists or remote upload is needed. |
| 9. What goes to Cursor after Session 1? | These four files; Session 1 report/commit and test status; cleared source/clip/brief manifests; fixed audition preprocessing; pinned model revisions/hashes; the proposed torch/Transformers versions; the resource supervisor and benchmark requirements in 03. |
| 10. Advance to real embeddings? | **Yes, after one real excerpt has cleared rights and audition preparation and Session 1 passes.** Run one clip/brief first, then 20 clips under the guardrail. Do not wait to acquire/label all P0 material before testing encoder fit. |

Evidence: [Incompetech training offer](https://incompetech.com/wordpress/2022/11/music-catalog-available-for-any-ai-training-project/), [catalog and rights documentation](https://incompetech.com/agent-section/), [primary checkpoint files](https://huggingface.co/laion/larger_clap_music/tree/a0b4534a14f58e20944452dff00a22a06ce629d1), [Apple specifications](https://www.apple.com/macbook-neo/specs/). All checked this session; local results are absent.

## Reconciliation with existing research

Reviewed current 00, 01, 03, 04, 05, 06, 07, 08 and 10 from the existing Music Preference Model research package. They remain the baseline; no source files or repository were changed.

| Finding | Effect on the handoff |
|---|---|
| Original recordings had been suggested but no owned inventory established | Replace the implicit availability assumption with 0 verified owned items and a concrete Incompetech acquisition shortlist. |
| Catalog music is retrieved, not generated from our prompt | Declare a brief-matched retrieval pilot. It supports workflow/within-catalog preference evidence, not generator optimization or generator generalization. |
| Current CLAP getters return an output object | In Transformers 5.19.0, use normalized projected pooler_output. Pin the API; older tensor-return examples are not interchangeable. |
| Checkpoints are .bin only in inspected official snapshots | Verify published hash and use supported restricted weight loading; do not require nonexistent upstream safetensors or bypass safe loading. |
| Fallback is only ~21% smaller by weight file | Treat memory rescue as an empirical question; do not promise the original planning envelope. |
| Loudness/channel operation order was implicit | Proposed probe clarification: canonical mono/48 kHz → gain-only audition matching → same waveform for listening and embedding. Version this and compare against Cursor’s implementation before adopting. |
| No specific numerical, swap-duration or preliminary-test thresholds were locked | Document 02/03 adds proposed operational thresholds, explicitly distinct from scientific success gates. |

Unchanged: 10-second scope; separate adherence/preference/acceptability; ties and cannot-judge; unknown rights block corresponding uses; grouping by connected brief/source ancestry; P0’s 20×3 design; P1 split/evaluation and calibration gates; frozen encoder and baseline-first learning. Do not weaken a rights policy just to make the new source pass. If Cursor’s commercial_ready profile requires release permissions too, finish that review before using it rather than silently changing its semantics.

## Priority gates and expected expense

1. **Data gate:** capture exact track/license evidence, review composition/master/third-party scope, obtain a usable crop, and set only substantiated permission fields. The catalog’s default composer claim does not clear arrangements or samples automatically.
2. **Foundation gate:** receive Cursor’s actual Session 1 passing report; success is not presumed from ongoing work.
3. **Encoder gate:** resolve and lock the proposed environment, verify one checkpoint, run the supervised one-clip probe, then the 20-clip CPU test. MPS failure alone permits continued CPU use.
4. **Listening gate:** test four candidate groups, fix only documented protocol issues, then curate the full P0 before any learning claim.

Expected service spend: **$0** for metadata review, CC-licensed individual acquisition, local extraction and self-labeling. Electricity/time are excluded. P0 prepared PCM is about 115 MB; numeric audio/text cache about 0.164 MB; primary snapshot about 0.780 GB. Preserve 10–20 GB free-disk headroom for environment, originals and results. No generation subscription, hardware purchase or paid compute is necessary for the recommended next step.

## One recommended next bounded action

**Complete a three-file acquisition dry run for P-01: Disquiet, Mesmerize and Colorless Aura.** Use document 01’s exact official links, snapshot the permissions, review provenance, and select one ten-second region per file under document 02. Finalize one common original brief and three crop records. Produce three accepted asset/rights/clip records or explicit rejection reasons. Stop there; this action tests whether the source actually yields a usable preference family while Cursor finishes Session 1.

After that succeeds and Session 1 passes, hand Cursor document 03 for one-clip →20-clip benchmarking. Keep this sequence bounded; do not turn the next session into generation, model training or a new annotation app.

**DATA GO/NO-GO: CONDITIONAL GO for the three-file acquisition test and subsequent P0 curation. NO-GO for declaring the full P0 ready or publishing data/derived artifacts before asset-level review.** Evidence is the creator’s explicit training offer, CC BY terms, inspected catalog and 20 live endpoints; missing evidence is actual audio/QC, complete rights records and 20 independent usable families.

**ENCODER GO/NO-GO: GO for a supervised local CPU feasibility probe after Session 1 and cleared input; NO-GO for claiming confirmed Mac deployment today.** Official artifacts, revisions, processor contracts, current implementation behavior and an arm64 Python 3.11 wheel are verified. Peak memory, numerical stability, throughput and A18 Pro MPS support remain empirical gates.
