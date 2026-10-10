# Graph Report - Model  (2026-10-10)

## Corpus Check
- 54 files · ~38,270 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 436 nodes · 1533 edges · 17 communities (9 shown, 8 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 154 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Feasibility and Literature
- Audio Loudness Meter
- Rights and Identity Splits
- Intake and Audition Gain
- Encoder Policy and Agent Rules
- Fixture Dataset Builder
- Encoder Protocol and Features
- Ingestion Tests
- Scorer and Calibration Policy
- Project Overview
- Package Metadata

## God Nodes (most connected - your core abstractions)
1. `MusicPrefError` - 51 edges
2. `build_dataset()` - 45 edges
3. `ingest()` - 42 edges
4. `write_config()` - 30 edges
5. `prepare_excerpt()` - 30 edges
6. `validate()` - 28 edges
7. `load_dataset()` - 25 edges
8. `canonical_bytes()` - 24 edges
9. `load_config()` - 23 edges
10. `prepare_clip()` - 22 edges

## Surprising Connections (you probably didn't know these)
- `Dummy Encoder (fixture-v1)` --implements--> `AudioTextEncoder`  [INFERRED]
  docs/decisions/0001-foundation-choices.md → src/music_pref/features/base.py
- `Dummy Encoder` --semantically_similar_to--> `Dummy Encoder (fixture-v1)`  [INFERRED] [semantically similar]
  AGENTS.md → docs/decisions/0001-foundation-choices.md
- `Ten-Second Excerpt Preparation` --semantically_similar_to--> `10-Second Excerpt Protocol`  [INFERRED] [semantically similar]
  Initial Research Package/02_P0_Dataset_and_Listening_Protocol.md → docs/decisions/0001-foundation-choices.md
- `CLAP Encoder` --references--> `AudioTextEncoder`  [EXTRACTED]
  docs/research/03_Audio_Encoder_and_Architecture_Analysis.md → src/music_pref/features/base.py
- `Dummy Encoder (fixture-v1)` --implements--> `DummyEncoder`  [EXTRACTED]
  docs/decisions/0001-foundation-choices.md → src/music_pref/features/dummy.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Data Pipeline Foundation** — rights_policy, identity_splits, ten_second_excerpt, gain_lufs_v1, p01_intake [INFERRED 0.85]
- **Encoder Selection Decisions** — clap_encoder, fused_clap, unfused_clap, dummy_encoder [INFERRED 0.85]
- **Evaluation Framework** — preference_vs_adherence, pairwise_comparisons, calibration_gates, initial_research_package_02_p0_dataset_and_listening_protocol_p0_listening_protocol, initial_research_package_02_p0_dataset_and_listening_protocol_brief_matched_retrieval [INFERRED 0.85]
- **Scorer Architecture Choices** — linear_pairwise_scorer, neural_mlp_alternative, null_result_valid [INFERRED 0.85]
- **Separate brief adherence from personal preference** — docs_research_04_dataset_and_human_feedback_strategy_dual_criterion_annotation, docs_research_06_mvp_technical_specification_dual_target_scoring, docs_research_09_research_risks_and_open_questions_adherence_preference_disagreement_benchmark, docs_research_02_literature_and_competitive_landscape_aime [INFERRED 0.85]
- **Offline data foundation first session** — docs_research_01_executive_feasibility_assessment_offline_first_session, docs_research_06_mvp_technical_specification_jsonl_manifest_schemas, docs_research_08_cursor_agent_implementation_handoff_offline_foundation_scope, docs_research_08_cursor_agent_implementation_handoff_leakage_safe_component_splits, docs_research_08_cursor_agent_implementation_handoff_dummy_encoder_and_feature_cache, docs_research_08_cursor_agent_implementation_handoff_rights_policy_profiles [EXTRACTED 1.00]
- **Unknown permission blocks release and training** — docs_research_04_dataset_and_human_feedback_strategy_rights_lane_policy, docs_research_04_dataset_and_human_feedback_strategy_acquisition_procedure, docs_research_04_dataset_and_human_feedback_strategy_suno_output_exclusion, docs_research_08_cursor_agent_implementation_handoff_rights_policy_profiles, docs_research_06_mvp_technical_specification_jsonl_manifest_schemas [INFERRED 0.95]
- **P0 Pilot of 20 Families and 60 Clips** — initial_research_package_02_p0_dataset_and_listening_protocol_p0_listening_protocol, initial_research_package_02_p0_dataset_and_listening_protocol_brief_matched_retrieval, initial_research_package_02_p0_dataset_and_listening_protocol_ten_second_excerpt_preparation, initial_research_package_02_p0_dataset_and_listening_protocol_label_schema, initial_research_package_02_p0_dataset_and_listening_protocol_identity_independence, initial_research_package_02_p0_dataset_and_listening_protocol_repeatability_pause_trigger, initial_research_package_02_p0_dataset_and_listening_protocol_one_musician_collection [EXTRACTED 1.00]
- **Default-Lane Source Rights Disposition** — initial_research_package_01_data_feasibility_and_rights_audit_conditional_data_go, initial_research_package_01_data_feasibility_and_rights_audit_incompetech_catalog, initial_research_package_01_data_feasibility_and_rights_audit_permissions_matrix, initial_research_package_01_data_feasibility_and_rights_audit_material_exclusions, initial_research_package_01_data_feasibility_and_rights_audit_conditional_sources, initial_research_package_01_data_feasibility_and_rights_audit_acquisition_shortlist [EXTRACTED 1.00]
- **Bounded CLAP Feasibility Probe** — initial_research_package_03_clap_encoder_feasibility_and_benchmark_handoff_larger_clap_music, initial_research_package_03_clap_encoder_feasibility_and_benchmark_handoff_clap_htsat_unfused, initial_research_package_03_clap_encoder_feasibility_and_benchmark_handoff_processing_contract, initial_research_package_03_clap_encoder_feasibility_and_benchmark_handoff_environment_pins, initial_research_package_03_clap_encoder_feasibility_and_benchmark_handoff_bounded_cpu_benchmark, initial_research_package_03_clap_encoder_feasibility_and_benchmark_handoff_rss_guardrail, initial_research_package_03_clap_encoder_feasibility_and_benchmark_handoff_encoder_fallbacks [EXTRACTED 1.00]

## Communities (17 total, 8 thin omitted)

### Community 0 - "Feasibility and Literature"
Cohesion: 0.08
Nodes (34): Bradley-Terry linear scorer, Frozen LAION larger CLAP music, Music Preference Model v0.1, AIME, Bayesian Personalized Ranking, CMI-RewardBench, MusicPrefs and MAD, TuneJury (+26 more)

### Community 1 - "Audio Loudness Meter"
Cohesion: 0.09
Nodes (41): _as_channels(), _biquads(), _block_power(), integrated_loudness(), _k_weight(), _lufs(), measure_loudness(), _require_rate() (+33 more)

### Community 2 - "Rights and Identity Splits"
Cohesion: 0.09
Nodes (34): Identity Splits (component-based), Rights Policy (commercial_ready, research_only), Component, connected_components(), _union_key(), _UnionFind, brief_content_hash(), canonical_pair_id() (+26 more)

### Community 3 - "Intake and Audition Gain"
Cohesion: 0.10
Nodes (34): gain_lufs_v1 Audition Normalization, P-01 Intake Path, file_sha256(), cli(), main(), AcquisitionReceipt, _append_model(), _ensure_manifest() (+26 more)

### Community 4 - "Encoder Policy and Agent Rules"
Cohesion: 0.10
Nodes (20): Dummy Encoder, Foundation Choices, CLAP Encoder, Fused CLAP (Primary), Incompetech Acquisition Shortlist, Conditional Audio Sources, Incompetech Catalog, Adherence Preference and Acceptability Labels (+12 more)

### Community 5 - "Fixture Dataset Builder"
Cohesion: 0.12
Nodes (40): load_config(), validate(), build_dataset(), dump_jsonl(), foundation_config(), _hex(), main(), make_asset() (+32 more)

### Community 6 - "Encoder Protocol and Features"
Cohesion: 0.12
Nodes (15): PreparedExcerpt, AudioTextEncoder, FeatureBatch, FeatureError, l2_normalize(), feature_cache_key(), load_feature(), store_feature() (+7 more)

### Community 7 - "Ingestion Tests"
Cohesion: 0.20
Nodes (29): load_dataset(), _config(), _mp3(), _pair(), _request(), _rights(), _sha(), test_cli_ingest_and_prepare() (+21 more)

### Community 8 - "Scorer and Calibration Policy"
Cohesion: 0.29
Nodes (8): Calibration Gates, Dummy Encoder (fixture-v1), Linear Pairwise Scorer, MVP Scope (No Generator/DAW/SaaS), Neural MLP Alternative (131,201 params), Null Result is Valid Deliverable, Pairwise Comparisons, Preference vs Adherence Separation

## Ambiguous Edges - Review These
- `Frozen LAION larger CLAP music` → `CMI-RewardBench`  [AMBIGUOUS]
  docs/research/02_Literature_and_Competitive_Landscape.md · relation: conceptually_related_to
- `Five-point gain gate` → `Locked protocol changes`  [AMBIGUOUS]
  docs/research/08_Cursor_Agent_Implementation_Handoff.md · relation: references
- `Preliminary Four-Group Acquisition Test` → `Independent Family Identity Rule`  [AMBIGUOUS]
  Initial Research Package/02_P0_Dataset_and_Listening_Protocol.md · relation: conceptually_related_to

## Knowledge Gaps
- **5 isolated node(s):** `music-pref`, `Conditional GO Decision`, `Research v0.1`, `Music Preference Model`, `Votelle`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 53 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `10-Second Excerpt Protocol` connect `Rights and Identity Splits` to `Scorer and Calibration Policy`, `Audio Loudness Meter`, `Encoder Policy and Agent Rules`?**
  _High betweenness centrality (0.127) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `MusicPrefError` (e.g. with `main()` and `_rights_gate()`) actually correct?**
  _`MusicPrefError` has 14 INFERRED edges - model-reasoned connections that need verification._
- **What connects `music-pref`, `Conditional GO Decision`, `Research v0.1` to the rest of the system?**
  _5 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Feasibility and Literature` be split into smaller, more focused modules?**
  _Cohesion score 0.08382936507936507 - nodes in this community are weakly interconnected._
- **Why does `prepare_excerpt()` connect `Audio Loudness Meter` to `Rights and Identity Splits`, `Intake and Audition Gain`, `Fixture Dataset Builder`, `Encoder Protocol and Features`?**
  _High betweenness centrality (0.123) - this node is a cross-community bridge._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Frozen LAION larger CLAP music` and `CMI-RewardBench`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Five-point gain gate` and `Locked protocol changes`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._