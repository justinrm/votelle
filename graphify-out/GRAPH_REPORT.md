# Graph Report - Model  (2026-10-10)

## Corpus Check
- 48 files · ~30,182 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 6 file(s) not represented in the graph (top: (none) 5, .lock 1)

## Summary
- 419 nodes · 1320 edges · 26 communities (17 shown, 9 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 103 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f3d91128`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- manifest.py
- build_dataset
- 06 — MVP Technical Specification
- test_audition.py
- base.py
- ingest
- MusicPrefError
- Status
- 03 — Audio Encoder and Architecture Analysis
- 05 — Training and Evaluation Research Plan
- 04 — Dataset and Human Feedback Strategy
- 03 — CLAP Encoder Feasibility & Benchmark Handoff
- research/README.md
- 01 — Data Feasibility & Rights Audit
- 02 — P0 Dataset & Listening Protocol
- _UnionFind
- 0003 — P-01 real-audio ingestion
- Votelle
- FIRST_PARTY_DECLARATION.md
- votelle-music

## God Nodes (most connected - your core abstractions)
1. `MusicPrefError` - 52 edges
2. `build_dataset()` - 45 edges
3. `ingest()` - 42 edges
4. `write_config()` - 30 edges
5. `prepare_excerpt()` - 29 edges
6. `validate()` - 29 edges
7. `load_dataset()` - 25 edges
8. `canonical_bytes()` - 24 edges
9. `load_config()` - 23 edges
10. `prepare_clip()` - 21 edges

## Surprising Connections (you probably didn't know these)
- `Preparation` --references--> `prepare_excerpt()`  [INFERRED]
  docs/decisions/0003-p01-ingestion.md → src/votelle_music/audio/prepare.py
- `Files` --references--> `ingest()`  [INFERRED]
  docs/decisions/0003-p01-ingestion.md → src/votelle_music/data/ingest.py
- `CLAP handoff` --references--> `waveform_for_encoder()`  [INFERRED]
  docs/decisions/0002-audition-normalization.md → src/votelle_music/audio/prepare.py
- `0001 — Foundation choices` --references--> `dataset_root()`  [INFERRED]
  docs/decisions/0001-foundation-choices.md → src/votelle_music/data/manifest.py
- `Commands` --references--> `validate()`  [INFERRED]
  README.md → src/votelle_music/data/manifest.py

## Import Cycles
- None detected.

## Communities (26 total, 9 thin omitted)

### Community 0 - "manifest.py"
Cohesion: 0.07
Nodes (42): 0001 — Foundation choices, cli(), main(), Component, connected_components(), _union_key(), IngestRequest, brief_content_hash() (+34 more)

### Community 1 - "build_dataset"
Cohesion: 0.12
Nodes (43): load_config(), validate(), build_dataset(), dump_jsonl(), foundation_config(), _hex(), main(), make_asset() (+35 more)

### Community 2 - "06 — MVP Technical Specification"
Cohesion: 0.12
Nodes (16): 06 — MVP Technical Specification, Acceptance criteria and tests, `assets.jsonl`, `briefs.jsonl` and `clips.jsonl`, CLI surface, Error and uncertainty behavior, Functional pipeline, Future generator integration contract (+8 more)

### Community 3 - "test_audition.py"
Cohesion: 0.32
Nodes (13): _prepare(), _replace_asset(), _sine(), test_bs1770_meter_matches_the_stereo_reference_tone(), test_gain_path_rejects_silent_nonfinite_invalid_and_out_of_bounds(), test_gain_preparation_is_deterministic_and_leaves_the_source_file(), test_hot_sine_is_attenuated_by_gain_alone(), test_inverted_stereo_is_phase_cancellation_not_a_level_match() (+5 more)

### Community 4 - "base.py"
Cohesion: 0.13
Nodes (16): 0002 — Audition normalization, CLAP handoff, Gain, Order, PreparedExcerpt, AudioTextEncoder, FeatureBatch, FeatureError (+8 more)

### Community 5 - "ingest"
Cohesion: 0.20
Nodes (30): file_sha256(), ingest(), _config(), _mp3(), _pair(), _request(), _rights(), _sha() (+22 more)

### Community 6 - "MusicPrefError"
Cohesion: 0.08
Nodes (49): Identity, _as_channels(), _biquads(), _block_power(), integrated_loudness(), _k_weight(), _lufs(), measure_loudness() (+41 more)

### Community 7 - "Status"
Cohesion: 0.11
Nodes (17): CLAP, Implemented, Implemented, not experimentally validated, Next, Not implemented, Open, P-01, Status (+9 more)

### Community 8 - "03 — Audio Encoder and Architecture Analysis"
Cohesion: 0.18
Nodes (11): 03 — Audio Encoder and Architecture Analysis, Architecture B: smallest credible conditional ranker, Architecture C: exact neural challenger, Independent, pairwise, and listwise ranking, License and adaptation matrix, Other 2025–2026 options, Personalization and encoder adaptation, Ranked encoder shortlist (+3 more)

### Community 9 - "05 — Training and Evaluation Research Plan"
Cohesion: 0.18
Nodes (11): 05 — Training and Evaluation Research Plan, Baselines and experiment matrix, Blind listening validation and generation efficiency, Calibration and abstention policy, Evaluation metrics and uncertainty, Leakage-safe partitioning, Minimum evidence and promotion rules, Preprocessing and feature caching (+3 more)

### Community 10 - "04 — Dataset and Human Feedback Strategy"
Cohesion: 0.20
Nodes (10): 04 — Dataset and Human Feedback Strategy, Annotation design, Auditable acquisition procedure, Collection stages and burden, Dataset inventory: content, labels and fitness, Dataset rights audit and decision, Efficient feedback and synthetic data, Generated audio and Suno (+2 more)

### Community 11 - "03 — CLAP Encoder Feasibility & Benchmark Handoff"
Cohesion: 0.22
Nodes (8): 03 — CLAP Encoder Feasibility & Benchmark Handoff, Bounded benchmark specification, Environment and known integration risks, Exact processing and return contract, Local setup and acquisition — after Session 1, Memory, storage and fallbacks, Pinned artifacts, prepared_waveform and exact_brief come from the validated manifests.

### Community 12 - "research/README.md"
Cohesion: 0.25
Nodes (3): Active research, Authority, Graphify

### Community 15 - "01 — Data Feasibility & Rights Audit"
Cohesion: 0.29
Nodes (6): 01 — Data Feasibility & Rights Audit, Acquisition manifest and review procedure, Exact acquisition shortlist, Material exclusions and component questions, Source inventory and acquisition decision, Source-level permissions matrix

### Community 16 - "02 — P0 Dataset & Listening Protocol"
Cohesion: 0.29
Nodes (6): 02 — P0 Dataset & Listening Protocol, How to construct the full P0, One-musician collection method, Repeatability and readiness, Small preliminary acquisition test, Ten-second candidate preparation

### Community 21 - "0003 — P-01 real-audio ingestion"
Cohesion: 0.33
Nodes (5): 0003 — P-01 real-audio ingestion, Catalog and identity, Files, Preparation, Three different gates

### Community 23 - "Votelle"
Cohesion: 0.50
Nodes (3): Authority, Votelle, What to open

## Knowledge Gaps
- **1 isolated node(s):** `votelle-music`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 131 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `MusicPrefError` connect `MusicPrefError` to `manifest.py`, `test_audition.py`, `base.py`, `ingest`, `Status`?**
  _High betweenness centrality (0.262) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `MusicPrefError` (e.g. with `Status` and `main()`) actually correct?**
  _`MusicPrefError` has 15 INFERRED edges - model-reasoned connections that need verification._
- **What connects `votelle-music` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `manifest.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07400194741966894 - nodes in this community are weakly interconnected._
- **Why does `Status` connect `Status` to `MusicPrefError`?**
  _High betweenness centrality (0.213) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `build_dataset()` (e.g. with `Asset` and `Brief`) actually correct?**
  _`build_dataset()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Should `build_dataset` be split into smaller, more focused modules?**
  _Cohesion score 0.11530398322851153 - nodes in this community are weakly interconnected._