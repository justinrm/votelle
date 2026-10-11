# 05 — MVP specification

Research protocol **v0.1**. Package version **0.1.0**. Schema version **0.1**. Evidence date **10 October 2026**.

Human-readable name: Votelle. Distribution and CLI: `votelle-music`. Import package: `votelle_music`. Exception: `VotelleError`. Decisions 0001–0003 still spell the historical commands `music-pref` and the historical package `music_pref`. Decision 0004 records that split. This note uses the live names and labels the historical ones.

## Purpose

This note is the implementation-aware technical specification for protocol v0.1. It states what `votelle_music` runs, which of that behavior has been exercised only on fixtures or on an unreleased intake path, and which contracts in the 9 October MVP note remain requirements the core tree does not implement.

Source, tests, configs, and `uv.lock` establish implemented behavior. `docs/decisions/` are the accepted choices. The 9 October note, [`docs/archive/research-preconsolidation-2026-10/06_MVP_Technical_Specification.md`](../archive/research-preconsolidation-2026-10/06_MVP_Technical_Specification.md), remains the broader product contract. It is not a list of implemented modules. Where that note and the source disagree about behavior the code already has, this file follows the source and quotes the disagreement in section 15. A requirement the code has not implemented stays in force. It is labeled proposed or deferred. It is not deleted.

Rights policy detail stays in [`01_DATA_GOVERNANCE.md`](01_DATA_GOVERNANCE.md). Listening procedure stays in [`02_P0_LISTENING_PROTOCOL.md`](02_P0_LISTENING_PROTOCOL.md). Encoder algebra, probe measurements, and the proposed ranker stay in [`03_ENCODER_AND_MODEL.md`](03_ENCODER_AND_MODEL.md). Training hypotheses and metrics stay in [`04_TRAINING_AND_EVALUATION.md`](04_TRAINING_AND_EVALUATION.md). The 9 October plan is archived at [`05_Training_and_Evaluation_Research_Plan.md`](../archive/research-preconsolidation-2026-10/05_Training_and_Evaluation_Research_Plan.md). This note points at those documents. It does not copy their sections, and it does not invent a trained metric.

`docs/PROJECT_DIRECTION.md` is used here only for non-goals and protocol boundaries. It does not expand protocol v0.1.

A green fixture run is a software check. It is not preference prediction.

## Executive summary

The core tree is an offline data foundation. It validates JSONL manifests, blocks unknown or denied rights for the selected policy, prepares a caller-selected 10-second excerpt, groups records by exact identity, writes a deterministic whole-component split, and can embed that excerpt with a 512-dimensional dummy encoder. The CLI commands that exist are `validate`, `split`, `ingest`, and `prepare`. PyTorch and Transformers are not dependencies.

`gain_lufs_v1` and the P-01 intake path are implemented and covered by tests. No musically accepted excerpt is in Git, and a passing ingest test is not a rights grant. Git does not contain the P-01 audio. Release permissions for that pilot are unknown, so `commercial_ready` is unavailable for it. This pass did not re-validate the earlier local intake.

There is no core CLAP adapter. Single-clip CPU CLAP feasibility succeeded on 10 October 2026 in a separate environment. That result is not the 20-clip benchmark. MPS parity is unverified. `production_claim_allowed` stays false. No preference model has been trained. Training, calibration, inference bundles, `compare`, `rank`, and a generator remain proposed or deferred.

## 1. Claim labels and status

| Label | Meaning in this note |
|---|---|
| Implemented | Behavior in current `votelle_music` source, tests, or configs |
| Implemented, experimentally unvalidated | The code path exists and the fixture or intake tests lock it. No musically accepted excerpt, listening result, or preference model is claimed |
| Proposed | A requirement in the 9 October specification, a decision handoff, or a research note. The core tree does not run it |
| Deferred | A later capability the protocol keeps outside the current build |
| Explicit non-goal | Out of protocol v0.1, or rejected as a product claim |
| Measured probe result | A figure whose evidence is the 10 October 2026 status record. This note does not recompute it |

| Capability | Status |
|---|---|
| JSONL manifests, schema `0.1`, path confinement, canonical file-byte and PCM hashes | Implemented |
| `research_only` and `commercial_ready` permission gates | Implemented |
| Ten-second crop, 480,000 mono samples at 48 kHz, `none_fixture_only` | Implemented |
| `gain_lufs_v1` (−20 LUFS, −1 dBTP, ±0.1 LU) on fixture tones | Implemented, experimentally unvalidated |
| P-01 local ingest and prepare for three official URIs | Implemented, experimentally unvalidated |
| Exact-id identity graph and seeded whole-component splits | Implemented |
| Dummy encoder `dummy` / `fixture-v1`, dimension 512, cache | Implemented as software. Not a musical embedding |
| Foundation refusal of every encoder other than `dummy` / `fixture-v1` | Implemented |
| Core CLAP adapter, `brief_too_long`, training, calibration, bundles, `compare`, `rank` | Proposed |
| 20-clip benchmark, MPS parity, three-clip cosine matrix | Deferred measurement. The single-clip CPU probe is a measured result in a separate environment |
| Generator, UI, full-song judgment, hosted service, universal taste | Explicit non-goal for this protocol |

**Explicit non-goals**, from the project direction and the 9 October scope. Protocol v0.1 does not build them, and a fixture pass does not imply them:

- a music generator, editor, digital audio workstation, or prompt-rewriting agent
- reinforcement learning of a generator, or a requirement that ACE-Step, YuE2, or HeartMuLa be installed
- a streaming application, hosted accounts, subscriptions, payments, or production SaaS
- a general-purpose recommender, a vector database, or distributed training
- a deployed reward-model service or a validated universal music-quality predictor
- full-song structural judgment, lyric transcription or fidelity, or voice-identity matching
- a long-form explaining language model
- a user interface

A change to excerpt length, grouping, rights, or label meaning needs a new protocol version.

## 2. Package and runtime

**Implemented.**

The distribution name is `votelle-music`, version `0.1.0`. `requires-python` is `>=3.11,<3.12`. The console script is `votelle-music = "votelle_music.cli:cli"`. `votelle_music.__version__` is `0.1.0`. The package docstring states that fixture success is not evidence of preference prediction. `votelle_music` does not re-export `VotelleError`. Callers import it from `votelle_music.schemas`.

Runtime dependencies declared in `pyproject.toml` and pinned in `uv.lock` are NumPy, Pydantic, SciPy, and SoundFile. The lockfile records NumPy 2.4.6, Pydantic 2.14.0, SciPy 1.17.1, and SoundFile 0.14.0, plus their transitive packages. The development group is pytest (lockfile 9.1.1). Hatchling builds the package. The license field is `Apache-2.0`, and the license file is included in distributions.

**Explicit non-goal for the core environment.** PyTorch and Transformers are not dependencies. Safetensors, scikit-learn, and a training framework are not dependencies. Adding them to make a test pass is outside this specification. An authorized encoder probe may use a separate environment. That environment is not the core tree.

Apache-2.0 covers original source code and project documentation. It does not clear recordings, compositions, annotations, embeddings, checkpoints, or third-party weights. A permission declaration is not legal clearance.

The status record’s verification environment on 10 October 2026 was uv 0.12.21 and CPython 3.11.16. This writing pass did not re-run that check.

## 3. Command-line interface

**Implemented** commands are the four subparsers in `src/votelle_music/cli.py`. The program name is `votelle-music`. An unrecognized subcommand is rejected by the argument parser before a dataset is opened. There is no dry-run flag.

Relative `dataset_root` is resolved from the current working directory. Commands are expected to run from the repository root. `network_access: true` is refused by `validate`, not by a network call. The implemented commands do not download audio or weights.

| Command | Arguments | Writes | Refuses |
|---|---|---|---|
| `validate` | `--config` (required) | Canonical JSON `ValidationReport` on stdout | Unreadable or schema-invalid config (`schema_invalid` on stderr, exit 1). Exit 1 when the report has any error-severity issue. A warning alone exits 0 |
| `split` | `--config`, `--output` (both required) | Canonical split JSON on stdout and at `--output`, via a temporary file and `os.replace` | Validation errors: the report goes to stderr, exit 1, and no output file is written. `SplitError` likewise. No partial split file |
| `ingest` | `--config`, `--source-uri`, `--raw`, `--decoded`, `--acquired-at`, `--decode-tool`, `--decode-version`, `--decode-command`; optional `--rights-record-id`, `--family-review` | `AcquisitionReceipt` as canonical JSON on stdout. Files under the dataset root as in section 7 | `VotelleError` JSON on stderr, exit 1. The decode command is stored and not executed. Missing local files are not fetched |
| `prepare` | `--config`, `--asset-id`, `--clip-id`, `--start`, `--end` | `QCSidecar` as canonical JSON. A prepared WAV. A `clips.jsonl` row only for `primary_level_matched` | Same error JSON. Requires `gain_lufs_v1` with `level_matched` true. Staged assets, bad bounds, and overwrites fail. Brief text is not invented |

On ingest, prepare, and split failures, stderr is a JSON object with `code` and `remediation`. The exception also carries `record_id` and `field`. The CLI does not print those two fields and does not print the class name. Config parse failures use `code` `schema_invalid` and put the parser message in `remediation`.

`validate` is the gate that refuses `network_access: true` (`network_access_refused`), any encoder other than `dummy` / `fixture-v1` (`encoder_unavailable`), and a `level_matched` flag that disagrees with the normalization profile (`normalization_profile_rejected`). `split` calls that same validation before it writes. `ingest` does not call `validate`. `prepare` enforces the gain profile itself and does not invent a rights decision.

`configs/foundation.json` is the fixture config: `commercial_ready`, seed 17, fractions 0.6 / 0.1 / 0.1 / 0.2, `none_fixture_only`, `level_matched` false, encoder `dummy` / `fixture-v1`, `network_access` false, target `adherence`. `configs/p01_piano.json` uses the same fractions, seed, encoder, and offline flag, with `dataset_root` `data/p01_piano`, `research_only`, `gain_lufs_v1`, and `level_matched` true. The P-01 fractions exist because `FoundationConfig` requires them. Decision 0003 forbids running split on that dataset. The split command has no P-01 special case in source. This note does not run it.

**Proposed, not implemented.** The 9 October CLI list names `extract`, `train`, `evaluate`, `compare`, `rank`, and `audit-release`, plus a dry-run that prints planned files and resource requirements. Those subcommands are absent. `ingest` is implemented and was not in that list. Section 15 quotes the old sentence.

## 4. Errors

**Implemented.** `VotelleError` is defined in `votelle_music.schemas`. `FeatureError` and `SplitError` subclass it. There is no `MusicPrefError` alias. The constructor fields are `code`, `remediation`, `record_id`, and `field`. `record_id` defaults to `None`. `field` defaults to `""`. The exception message is `"{code}: {remediation}"`.

Validation issues are a separate channel. A `ValidationIssue` has `severity` (`error` or `warning`), `record_id`, `field`, `code`, and `remediation`. `ValidationReport.has_errors` is true when any issue has severity `error`. `loudness_mismatch` is a warning. It does not by itself fail `validate`, and it does not rewrite the clip row.

Codes verified in source:

| Code | Where it is raised or reported | What it means |
|---|---|---|
| `schema_invalid` | CLI config parse; JSONL; family review; receipt JSON; feature cache | The payload does not match the schema, or a cache file is unreadable, pickled, or the wrong dtype |
| `schema_version` | `validate` | Config schema is not `0.1` |
| `network_access_refused` | `validate` | `network_access` is true. The foundation is offline |
| `encoder_unavailable` | `validate` | Encoder name is not `dummy` or revision is not `fixture-v1` |
| `normalization_profile_rejected` | `validate`, `prepare_excerpt`, `prepare_clip` | `level_matched` and the profile disagree, or P-01 prepare is not `gain_lufs_v1` with `level_matched` true |
| `path_escape` | `resolve_under_root` | Absolute path, empty path, `..`, or a resolved path outside the dataset root |
| `missing_reference` | load and reference checks | Missing JSONL, missing audio, missing parent, clip, brief, or repeat target |
| `duplicate_id` | manifest uniqueness; ingest; family review | Repeated manifest id, or a second ingest of the same URI, recording id, raw hash, or decoded PCM |
| `missing_rights` | rights check | An asset, brief, or judgment cites a rights id that is not in `rights.jsonl` |
| `missing_component_scope` | rights schema or check | `components` is empty |
| `missing_evidence` | rights check | Evidence path is missing. A license name is not a substitute |
| `permission_unknown` | rights check | A permission the policy requires is `unknown` |
| `permission_denied` | rights check | A permission the policy requires is `denied` |
| `hash_mismatch` | media check; ingest copy; prepared WAV | File bytes, PCM, evidence, or prepared WAV do not match the recorded hash |
| `unsupported_format` | `read_audio` | Suffix is not `.wav` or `.flac`, or SoundFile cannot decode the file |
| `nonfinite_audio` | decode, crop, resample, gain, loudness, true peak | NaN or Inf in samples or in a derived buffer |
| `invalid_audio` | shape, sample rate, loudness channel count, encoder waveform | Wrong rank, non-positive rate, loudness channels other than mono or stereo, or an encoder buffer that is not 480,000 finite float32 samples |
| `bad_bounds` | crop and reference checks | End is not after start, or the span falls outside the decoded asset |
| `duration_not_ten_seconds` | crop and reference checks | Span is farther than 1 ms from 10 seconds. The loader does not pad or trim |
| `digital_silence` | prepare and `validate` | Peak absolute amplitude below `1e-8` on the crop, or a gain path with no usable peak. Quieter musical material above that threshold is not rejected as silence |
| `phase_cancellation` | downmix | Equal-mean mono is silent while a channel is not, or mono mean-square is below 1% of the channel mean-square |
| `loudness_window_too_short` | loudness meter | Fewer than 400 ms at 48 kHz. A valid 10-second excerpt is longer than this guard |
| `loudness_mismatch` | `validate` warning | Gated loudness after one gain is non-finite or farther than 0.1 LU from −20. The dataset is not failed |
| `source_mismatch` | media check; ingest | Declared rate, channels, duration, or SoundFile info do not match the decode |
| `invalid_pair` | judgment check | The two clip ids are equal, or `pair_id` is not the sorted ids joined by `::` |
| `invalid_repeat` | judgment check | Self-repeat, different unordered pair, different brief, different listener, or a cycle |
| `invalid_source` | ingest | URI outside the three official strings, missing local file, raw and decoded paths identical, non-MP3 raw, decoded suffix not WAV or FLAC, bad family group, or empty `clip_id` |
| `lossy_source_mislabelled` | ingest | Decoded path looks like an MP3. The MP3 is not accepted as a manifest asset |
| `missing_provenance` | ingest | `acquired_at`, `decode_tool`, `decode_version`, or `decode_command` is blank. The command is recorded and is not executed |
| `already_exists` | ingest write; prepare | Refusing to overwrite a raw file, receipt, prepared WAV, QC sidecar, or clip id |
| `ineligible` | `prepare_clip` | Asset is not in `assets.jsonl`. Staged audio cannot enter the primary condition |
| `ingest_failed` | ingest rollback wrapper | An unexpected failure. Files that attempt created are removed |
| `insufficient_groups` | `SplitError` | No positive fraction, fewer components than positive splits, or an empty positive split after assignment |
| `unsplittable_component` | `SplitError` | A component’s weight exceeds the largest positive fraction of total weight |
| `validation_failed` | `SplitError` | `write_split` found validation errors |
| `encoder_dimension` | `FeatureError` | `l2_normalize` or a cache vector is not shape `(512,)` |
| `nonfinite_embedding` | `FeatureError` | Embedding or cache vector contains NaN or Inf, or normalization produced one |
| `zero_norm` | `FeatureError` | Refusing to L2-normalize a zero vector |

**Proposed.** `brief_too_long` is not raised anywhere in the core tree. Decision 0002 assigns it to a future CLAP adapter: a brief over 512 tokens, including special tokens, with truncation left off. The `AudioTextEncoder` method list does not grow to carry that failure. Until that adapter exists, the code has no token counter.

**Proposed error policy from the 9 October note, not implemented as a scorer.** Invalid input is a typed error and a nonzero CLI exit, which the foundation already does for the cases above. Valid but unsupported domain, an untrained personal target, an out-of-scope brief, an unresolved tie, or an insufficient margin are specified to abstain or return an unsupported status. They must not be compressed into a zero score. No scorer exists to do either. An out-of-memory failure must not silently shorten a clip, switch encoders, change precision, or change preprocessing. That rule is a requirement on a future extractor. The core tree has no batch extractor and no MPS path.

## 5. Manifests and storage

**Implemented.** Schema version is the string `0.1` on config and on each record model. Unknown fields are rejected (`extra="forbid"`). Manifest files are UTF-8 JSONL under the dataset root: `assets.jsonl`, `rights.jsonl`, `briefs.jsonl`, `clips.jsonl`, `judgments.jsonl`. A missing file is `missing_reference`. Blank lines are skipped. Each non-blank line must be a JSON object.

Source JSONL is append-only in the ingest and prepare writers. They do not rewrite an existing row. Ingest appends an asset line with `json.dumps(..., sort_keys=True)` and a trailing newline. Receipts, QC sidecars, validation reports, and split artifacts use canonical bytes: UTF-8 JSON, sorted keys, separators `(",", ":")`, `ensure_ascii` false, and a trailing newline. Manifest hashes stored on a split are SHA-256 of each existing JSONL file’s raw bytes.

Paths in manifests are relative to the dataset root. `resolve_under_root` rejects absolute paths, empty paths, `..`, and any resolved path that is not the root or a descendant. Commands do not follow a manifest path outside that root.

Canonical PCM, per decision 0001, is little-endian float32 at the file’s original sample rate and channel count, before crop or resample. `sha256_original` is the SHA-256 of the file bytes. `sha256_pcm` is `pcm_hash`: SHA-256 of contiguous `np.float32` bytes. On the little-endian hosts recorded for this project, those bytes are little-endian. The function does not pass an explicit `<f4` dtype. Section 16 notes that limit.

### Assets

**Implemented** `Asset` fields: `schema_version`, `asset_id`, `relative_path`, `sha256_original`, `sha256_pcm`, `source_recording_id`, `song_family_id`, optional `artist_id` and `contributor_id`, `origin_type` (`original`, `contribution`, `generated`, `public_dataset`, `test_fixture`), optional `source_uri` and `source_revision`, `acquired_at`, optional `generator` (`model_id`, `revision`, optional `seed`, `settings_hash`, `component_license_evidence`), `sample_rate`, `channels`, `duration_seconds`, `rights_record_id`, `parent_asset_ids`.

`validate` checks that the file bytes and the canonical PCM hash match, and that rate, channels, and duration (within 1 ms) match the decode. Parent ids must exist in `assets.jsonl`. P-01 ingest writes `origin_type` `public_dataset`, `artist_id` `kevin-macleod`, and `source_revision` set to the catalog ISRC. The same artist id does not merge song families.

### Rights records

**Implemented** `RightsRecord` fields: `schema_version`, `rights_record_id`, `rightsholder`, `evidence_path` or `evidence_url` (at least one), `evidence_sha256` (length 64), `recorded_at`, optional `license_identifier`, `attribution`, and `exceptions`, `components` (one or more of `recording`, `composition`, `lyrics`, `prompt`, `labels`), and permissions `research_training`, `commercial_training`, `audio_release`, `embedding_release`, `checkpoint_release`, each `allowed`, `denied`, or `unknown`. `review_status` and `review_rationale` are required strings. The permission check is in section 6. What a license string means for a particular catalog stays in the governance note.

### Briefs

**Implemented** `Brief` fields: `schema_version`, `brief_id`, `brief_family_id`, `text`, `language`, `audible_clauses`, `intended_scope`, `rights_record_id`, `content_sha256`. The content hash must equal SHA-256 of the UTF-8 text. Briefs that share `brief_family_id` are one identity component.

**Proposed, not implemented.** The 9 October note says a brief that requires an entire chorus arc fails the v0.1 scope check or needs explicit human revision. `intended_scope` is stored and is not interpreted. No chorus-arc validator exists. That requirement stands. Listening procedure for what a brief may ask stays in the protocol note.

### Clips

**Implemented** `Clip` fields: `schema_version`, `clip_id`, `asset_id`, `start_seconds`, `end_seconds`, `audition_condition`. `audition_condition` must equal the config normalization profile. Duration must be within 1 ms of 10 seconds. The loader does not pad or trim, and it does not choose the crop.

**Proposed fields the clip row does not carry.** The 9 October clip contract also names preprocessing id and hash, a prepared-audio hash, a diagnostics reference, and a split-group id. Current source keeps preprocessing id, preprocessing hash, prepared PCM hash, gain, loudness, true peak, and eligibility on the P-01 `QCSidecar`, and keeps diagnostics on `PreparedExcerpt`. Split membership lives in the split artifact, not on the clip. Those facts do not retire the richer clip contract. Section 15 quotes it. A future writer must not drop the requirement by treating the short row as the whole contract.

### Judgments

**Implemented** `Judgment` fields match the 9 October table: `judgment_id`, `pair_id`, `session_id`, `brief_id`, `clip_a_id`, `clip_b_id`, `listener_id`, `timestamp`, `presentation_order` (`AB` or `BA`), `adherence_choice` and `preference_choice` (each `A`, `B`, `tie`, `cannot_judge`, or null), `acceptable_a` and `acceptable_b` (each `yes`, `no`, `unsure`, or null), optional `confidence`, `reason_codes`, `notes`, `listened_seconds_a`, `listened_seconds_b`, `is_repeat_of`, `label_source` (`human`, `teacher`, `synthetic_rule`), and `label_rights_record_id`.

`pair_id` must be the two clip ids sorted, joined by `::`. The clips must differ and must exist. The brief must exist. `orient_judgment` keeps the stored row and, when `clip_a_id` is not the sorted left id, flips both choices and swaps the two acceptability fields together. `presentation_order` is left as stored. Repeats must point at another judgment with the same unordered pair, the same brief, and the same listener. A repeat may use another session and may disagree with the original. Chains are allowed. Cycles are `invalid_repeat`. The JSONL row is not rewritten.

Decision 0001: fixture judgments used to build graphs are `synthetic_rule` edges, not human preference labels.

**Proposed, not implemented as an access control.** The 9 October note says notes are private by default, and that corrections are appended as superseding events. The field `notes` is stored. No privacy filter enforces it. Repeats are the implemented provenance link. There is no distinct superseding-correction type. Privacy and consent stay in the governance note. The listening procedure stays in the protocol note.

### Split artifact and feature metadata

**Implemented** split JSON, from `build_split`: `schema_version` `0.1`, `seed`, `grouping_policy` and `split_version` both `component_v1`, `manifest_sha256`, `components` (ids, song families, weight), `splits` (component ids per positive split), `excluded` (always an empty list in this writer), and `split_sha256` over the canonical body before that field is added. The same seed and the same manifests yield the same bytes. Changing a manifest byte changes `split_sha256` even when membership does not.

**Implemented** cache-key payload, which is the feature identity the tree actually hashes: `source_pcm_sha256`, `start_seconds`, `end_seconds`, `preprocessing_sha256`, `encoder_id`, `encoder_revision`, `processor_hash`, `pooling`, `dtype`. Defaults on the dummy path are `processor_hash` `"none"`, `pooling` `"clip"`, `dtype` `"float32"`.

**Proposed, not stored.** The 9 October feature record also names hardware and extraction software versions. They are not cache-key fields. Excluded ids with reasons, and a copy of `split_sha256` inside every trained artifact, wait on a writer the tree does not have. Section 15 quotes both sentences.

Storage that is implemented for small arrays: NumPy `.npy` with `allow_pickle=False`. **Proposed:** Safetensors for neural weights. No database is required for the foundation, and none is implemented.

## 6. Rights validation

**Implemented.** A license string never grants a permission. `check_rights` reads the audited fields. It does not map `license_identifier` onto `allowed`.

| Policy | What must be `allowed` | What still fails |
|---|---|---|
| `research_only` | `research_training` | `unknown` or `denied` research training, even when the license string is familiar. Other permissions may stay `unknown` |
| `commercial_ready` | `research_training`, `commercial_training`, `audio_release`, `embedding_release`, and `checkpoint_release` | `unknown` or `denied` on any of those five |

Missing rights rows, missing component scope, a missing evidence file, and an evidence hash mismatch are errors. When `evidence_path` is set, the file must stay under the dataset root and match `evidence_sha256`. The report’s `policy` and `provenance` fields are both set to the config’s `rights_policy` string. That `provenance` value is the policy name, not a separate provenance document.

`configs/foundation.json` uses `commercial_ready` on the generated fixture root. A passing fixture validate checks the gate. It is not a music clearance.

Dataset eligibility for P-01 is `votelle-music validate --config configs/p01_piano.json` under `research_only`. Ingest does not edit `rights.jsonl` and does not run that check. Release clearance is the `commercial_ready` rule. Ingest never sets those permission fields.

Which catalogs, contributor grants, and component rights can ever satisfy those fields is the subject of [`01_DATA_GOVERNANCE.md`](01_DATA_GOVERNANCE.md), especially its commercial-ready and research-only section. This note does not restate that audit.

**Status constraint.** P-01 release permissions are unknown, so `commercial_ready` is not available for that pilot. The earlier local intake snapshot, as recorded in `docs/STATUS.md`, had `research_training` `allowed` and commercial training, audio release, embedding release, and checkpoint release `unknown`, with `release_clearance` `not_assessed`. This pass did not inspect that audio or re-validate that snapshot.

## 7. P-01 ingestion

**Implemented, experimentally unvalidated.** Decision 0003 and `src/votelle_music/data/ingest.py`. P-01 is an acquisition and listening pilot, not a training set. No audio is downloaded. No license is read from a filename, an ID3 tag, or a catalog row. A passing ingest test is not a rights grant and not a listening result.

Only these official URI strings are accepted. A space in place of `%20` is `invalid_source`.

| Recording | ISRC | URI | Slug |
|---|---|---|---|
| Disquiet | USUAN1500036 | `https://incompetech.com/music/royalty-free/mp3-royaltyfree/Disquiet.mp3` | `disquiet` |
| Mesmerize | USUAN1500005 | `https://incompetech.com/music/royalty-free/mp3-royaltyfree/Mesmerize.mp3` | `mesmerize` |
| Colorless Aura | USUAN1400008 | `https://incompetech.com/music/royalty-free/mp3-royaltyfree/Colorless%20Aura.mp3` | `colorless-aura` |

`source_recording_id` is one stable id per official URI. `song_family_id` is distinct per URI until a family-review file has `review_status` `reviewed`, a rationale, and a group of at least two catalog URIs. Passing that file on a later ingest does not rewrite rows already written. A second ingest of the same URI, the same raw hash, or the same decoded PCM is `duplicate_id`. Existing bytes stay. A failed ingest deletes only the files that attempt created.

The MP3 from the official URI is the raw original. It is copied and never modified. It is not an `assets.jsonl` row. The locked validator accepts WAV and FLAC only. `lossless_master` on the receipt is false. The operator-decoded WAV or FLAC is the manifest asset. `sha256_original` on that asset is the decoded file’s bytes. `sha256_pcm` is the canonical float32 PCM of that decode, before crop or resample. The receipt stores the MP3 path and hash, plus `decode_tool`, `decode_version`, and `decode_command`. Tests lock that the command string is stored and that a command such as `touch` is not executed.

| Path under the dataset root | Role |
|---|---|
| `raw/<slug>.mp3` | Unmodified copy of the local MP3 |
| `decoded/<slug>.wav` or `.flac` | Operator-decoded derivative and, when eligible, the manifest asset |
| `receipts/<asset_id>.json` | Acquisition receipt |
| `evidence/` | Local rights snapshot supplied by the operator |
| `assets.jsonl`, `rights.jsonl`, `briefs.jsonl`, `clips.jsonl`, `judgments.jsonl` | Manifests. The first successful ingest creates any that are missing. `judgments.jsonl` may be empty. `briefs.jsonl` stays empty until the operator writes one |
| `prepared/<clip_id>.wav` | Float32 WAV, 48 kHz, mono, 480,000 samples |
| `qc/<clip_id>.json` | QC sidecar |

Git does not contain this audio. `data/` is gitignored. A clone has the workflow and not the files.

### Three gates

Provisional review, dataset eligibility, and release clearance stay distinct.

| Gate | Rule | What it does not mean |
|---|---|---|
| Provisional review | No rights id, `review_status` other than `reviewed`, or a missing or hash-mismatched local evidence file. A URL without a local evidence file stays here | Receipt `rights_gate` is `provisional_review` and `in_manifest` is false. Nothing is appended to `assets.jsonl` |
| Manifest candidate | An existing rights row is `reviewed` and its local evidence file matches `evidence_sha256` | Receipt `rights_gate` is `reviewed_with_evidence` and `in_manifest` is true. Ingest appends an asset and does not edit permissions. `release_clearance` is `not_assessed` |
| Dataset eligibility | `validate` under `research_only` | `research_training` must be `allowed`. Unknown still fails. `in_manifest: true` does not mean this check passed |
| Release clearance | `commercial_ready` requires `allowed` on all five permission fields | Ingest never grants release |

### Prepare

**Implemented, experimentally unvalidated.** `prepare` takes operator-supplied start and end times and calls `prepare_excerpt` with `gain_lufs_v1`. It writes the float32 WAV and a QC sidecar. `excluded_loudness_mismatch` is not appended to `clips.jsonl`. `primary_level_matched` (within 0.1 LU of −20, and at or under −1 dBTP) is the only result that becomes a clip row. Staged assets are `ineligible`. Musical suitability is not decided here.

The status record’s earlier local intake had receipts for Disquiet, Mesmerize, and Colorless Aura under gitignored `data/p01_piano`, each `reviewed_with_evidence` and `in_manifest: true`, with empty brief, clip, and judgment manifests. This maintenance pass did not inspect that private audio or re-validate that intake. A later technical excerpt prepared for the isolated probe is not musical acceptance and not a completed listening dataset. Listening acceptance stays in [`02_P0_LISTENING_PROTOCOL.md`](02_P0_LISTENING_PROTOCOL.md).

## 8. Audio preparation

**Implemented** for the fixture profile. **Implemented, experimentally unvalidated** for `gain_lufs_v1`. Decision 0002 is the loudness procedure. This note cites it and does not rederive the meter. A synthetic tone that passes these tests is a fixture, not evidence of musical suitability or preference. The tree is not an EBU-certified meter.

`FoundationConfig` audio is locked to 10 seconds, 48,000 Hz, and one output channel. Any other excerpt length, rate, or channel count fails config validation.

Order in `prepare_excerpt`:

1. Decode WAV or FLAC to float64. Other suffixes, including MP3, are `unsupported_format`.
2. Require a caller-selected span of 10 seconds ± 1 ms (`DURATION_TOLERANCE = 0.001`). Do not pad, trim, or choose the crop.
3. Reject non-finite samples and digital silence (peak absolute amplitude below `1e-8`) on the multi-channel crop.
4. Downmix with an equal mean (`equal_mean/phase_ratio_0.01/v1`). This is not an ITU surround fold-down. Phase cancellation is an error.
5. Resample with `scipy.signal.resample` to exactly 480,000 mono samples at 48 kHz. Method id: `scipy.signal.resample/fft/v1`.
6. For `gain_lufs_v1` only, measure that derivative, apply one constant gain, and remeasure. The original file is not opened for writing.

| Profile | `level_matched` | What it does |
|---|---|---|
| `none_fixture_only` | false | Resample only. No loudness gain. `level_matched` on the excerpt stays false |
| `gain_lufs_v1` | true | One constant gain toward **−20 LUFS**, capped so true peak stays at or under **−1 dBTP**. No compressor, limiter, fade, or sample-by-sample nonlinearity |

The applied linear gain is the smaller of the loudness gain and the ceiling gain. A further constant scale runs when float error leaves the remeasured true peak over the ceiling. There is no loudness iteration. If absolute-gate membership changes after that gain, a dynamic excerpt can miss ±0.1 LU and is flagged.

Acceptance for a level match is **±0.1 LU**. `loudness_mismatch` is set when the remeasured gated loudness is non-finite or farther than 0.1 LU from −20. `gain_limited_by` is `true_peak` when the ceiling, rather than the loudness target, selected the gain. `validate` records that as a warning and does not fail the dataset. Exclude the clip from the primary level-matched analysis, or keep it in a separately identified condition. P-01 prepare uses the exclusion path: a mismatch does not become a clip row.

Loudness method id: `itu-r-bs.1770-4/k-weight/48kHz/v1`. True-peak method id: `scipy.signal.resample_poly/4x/kaiser5/line-pad/v1`. If every block is below the absolute gate, the gain uses ungated block power (`ungated_block_power_v1`). The value stored after gain is the gated remeasurement. Channel weight in the decision is 1.0 for mono and for each of stereo left and right. Filters start at rest on the excerpt. The true-peak oversampling is not the BS.1770 Annex 2 FIR table.

`preprocessing_sha256` is the SHA-256 of canonical JSON for `preprocessing_document(profile)`. The fixture document is channels, excerpt length, resample method, profile name, and sample rate. The gain document adds the downmix method, loudness method, true-peak method, target LUFS, ceiling, tolerance, and the ungated-gate fallback. Changing any of those changes the feature-cache key. The prepared waveform hash is `pcm_hash` of contiguous float32.

`waveform_for_encoder` returns a contiguous float32 copy of the samples a listener would hear, shape `(480000,)`. Listening samples and the future encoder buffer are the same excerpt. A buffer that is not exactly 480,000 finite samples raises `invalid_audio`.

Original-crop diagnostics from `measure_crop` are measurements, not preference scores: duration, sample rate, peak amplitude, clipping (peak at or above 0.999), RMS, and digital silence, each with a unit, a method id, and `kind="measured"`.

## 9. Identity and splitting

**Implemented.** Decision 0001. Identity edges are exact ids and hashes only. Near-duplicate audio is not detected. Generator identity is not a split edge. Tests lock that two assets with the same generator object remain two components.

`connected_components` unions assets that share `source_recording_id`, `song_family_id`, `sha256_original`, or `sha256_pcm`; assets linked by `parent_asset_ids` when the parent is in the manifest; briefs that share `brief_family_id`; and a judgment with its brief, with the assets of its two clips, and with `is_repeat_of` when that id is present. Component id is the SHA-256 of canonical JSON of the sorted asset, brief, and judgment ids. Component weight is the number of distinct song families in the component. A component with no assets has weight 0.

Splits shuffle components with `random.Random(seed)` after sorting by component id, then assign whole components by weight deficit. Positive splits are those whose fraction is greater than zero, in the order train, validation, calibration, test. A component heavier than the largest positive fraction of total weight, fewer components than positive splits, an empty positive split after assignment, or no positive fraction is `SplitError`. The assignment does not break a component to fill a bucket. Fractions must be non-negative and sum to 1 within `1e-6`.

The foundation check’s 20 equal-weight components at seed 17 assign 12 train, 2 validation, 2 calibration, and 4 test. That count is a software property of those fixture components. It is not a P-01 split, and it is not a preference result.

`write_split` validates first. On failure it writes nothing. The successful writer replaces the destination atomically. `excluded` in the artifact is an empty list. Reasons for exclusion are not recorded.

**Proposed, not implemented.** The training plan’s identity graph includes near-duplicate audio, covers, and stems. Decision 0001 and the source refuse that detector until it exists as a separate component. This note does not describe near-duplicate linking as current behavior, and it does not drop the requirement. It remains proposed for a later protocol-compatible detector. Running `split` on `configs/p01_piano.json` remains forbidden. Those fractions are schema fields, not an instruction to split the pilot.

## 10. Dummy encoder and feature cache

**Implemented** as software. The module states that the dummy encoder is not a musical embedding and not a production model. Fixture tests lock shape, finiteness, repeatability, and the production flag. They do not lock preference prediction.

`DummyEncoder.describe()` returns `EncoderSpec` with `name` `"dummy"`, `revision` `"fixture-v1"`, `dimension` 512, `production_claim_allowed` false, `processor_hash` `"none"`, `pooling` `"clip"`, and `dtype` `"float32"`. Audio vectors are a deterministic unit-length draw from the SHA-256 of the contiguous float32 PCM, using NumPy `PCG64` seeded from that digest. Text vectors are the same kind of draw from the UTF-8 brief. An empty input returns shape `(0, 512)`. `l2_normalize` requires one finite vector of length 512 and rejects a zero norm.

`AudioTextEncoder` in `src/votelle_music/features/base.py` is a `Protocol` with `describe`, `embed_audio(clips: list[PreparedExcerpt])`, and `embed_text(briefs: list[Brief])`. `FeatureBatch` holds `vectors` and `spec`. This protocol is installed. It is not a CLAP adapter. `validate` does not call it. It refuses every config encoder other than `dummy` / `fixture-v1` with `encoder_unavailable`, including after the isolated probe. Decision 0002 still prohibits naming CLAP in the foundation config. The historical decision text says `music-pref validate`. The live command is `votelle-music validate`.

Cache keys are SHA-256 of the canonical JSON payload in section 5. Stored entries are contiguous float32 vectors of shape `(512,)`, finite, written with `allow_pickle=False`. Keys must be 64 lowercase hexadecimal characters. An existing key is left in place. Replacement of a new key is atomic for one process. A path-like key is `schema_invalid` and does not create a file outside the cache directory. A changed encoder, processor, pooling mode, excerpt, preprocessing document, or source PCM hash is a new key.

`production_claim_allowed` stays false. Dummy vectors and any future CLAP vectors do not share a feature space, because encoder id, revision, processor hash, and pooling are part of the key. The CLAP adapter’s pooling value, when it is written, is `pooler_output`, not `clip`.

## 11. Proposed CLAP adapter

**Proposed. Not implemented.** There is no core adapter. Foundation validation still accepts only `dummy` / `fixture-v1`.

Decision 0002 and [`03_ENCODER_AND_MODEL.md`](03_ENCODER_AND_MODEL.md) hold the adapter contract. This note does not restate the feature algebra or the probe tables. The adapter, when it is written, has to follow decision 0002:

- call `waveform_for_encoder` and pass `sampling_rate=48000`
- reject any buffer that is not exactly 480,000 finite samples before the feature extractor
- pass `truncation="rand_trunc"` and `padding="repeatpad"` only after that assert; those processor defaults are not allowed to repair length
- read `pooler_output` into the existing `FeatureBatch` ndarray
- reject a brief over 512 tokens, including special tokens, with truncation left off, using the adapter-local failure `brief_too_long`
- set `EncoderSpec.pooling` to `pooler_output`, `dtype` to `float32`, and `production_claim_allowed` to false until the probe gates pass

The `AudioTextEncoder` signature does not change. Session 2B still must not put PyTorch or Transformers in this environment.

**Measured probe result, separate environment.** Single-clip CPU feasibility succeeded on 10 October 2026. The status record is the evidence. Scope: one technical excerpt on CPU. That run is not a core adapter, not a trained ranker, and not the 20-clip benchmark. MPS was available and was not used. MPS parity is unverified. The three-clip diagnostic runner is recorded as written and not executed. No three-clip cosine matrix is recorded. The four-text cosine check is an encoder similarity for one excerpt. It is not a listener preference. Checkpoint pins, shapes, hashes, and memory figures stay in the status record and in the encoder note.

`production_claim_allowed` stays false after that probe. Decision 0002’s sentence that no weights were downloaded and no encoder ran describes that foundation session. It does not erase the later isolated probe, and it does not open the foundation encoder gate.

## 12. Proposed training, evaluation, and inference

**Proposed. Not implemented.** No preference model has been trained. This note names the modules and does not invent a metric, a coefficient, or a result.

The training plan’s pre-registered hypotheses are H1 (brief adherence against a fixed baseline) and H2 (a listener-specific residual on later preference). Their metrics, grids, ablations, calibration gates, and promotion rules stay in [`04_TRAINING_AND_EVALUATION.md`](04_TRAINING_AND_EVALUATION.md). The predecessor plan is archived beside the other 9 October notes. The encoder note is the authority for the feature map and the parameter counts of the proposed ranker. A negative result is a valid outcome. Fixture success is not that result.

| Module | Status | Where the contract lives |
|---|---|---|
| Fixed cosine and other zero-training baselines | Proposed | Encoder note and training plan. Not a core function |
| Regularized linear pairwise ranker | Proposed | Encoder note. Not implemented |
| Neural challenger, only if the data and the baselines justify it | Proposed | Encoder note. Not implemented |
| Calibration and abstention | Proposed | Training plan. Not implemented |
| `train`, `evaluate` | Proposed CLI and library functions | 9 October note. No such functions in `votelle_music` |
| `compare`, `rank` | Proposed | 9 October note. They must not average adherence and preference |
| Personal-preference target with no personal training | Proposed to be unsupported, not filled with a generic quality score | 9 October note and encoder note |

The 9 October note labels the following as proposed interfaces, not installed functions. `AudioTextEncoder` has since been installed with `PreparedExcerpt` rather than `PreparedClip` (section 10 and section 15). The scorer and the four functions below are still unimplemented. They are preserved here so the requirement is not dropped:

```python
class CandidateScorer(Protocol):
    def score(self, audio_features, text_features) -> np.ndarray: ...
    def describe(self) -> ModelSpec: ...

def train(config: TrainConfig, dataset: DatasetIndex) -> RunManifest: ...
def evaluate(bundle: ModelBundle, split: LockedSplit) -> EvaluationReport: ...
def compare(request: CompareRequest, bundle: ModelBundle) -> CompareResult: ...
def rank(request: RankRequest, bundle: ModelBundle) -> RankResult: ...
```

`CandidateScorer` consumes features, not paths or generator sessions. `compare` is specified to validate target, scope, listener support, and cache compatibility before scoring. `rank` is specified to score candidates independently under one shared brief, model, and target. Missing personal training means that target is unsupported.

The following JSON is the 9 October example response **for an exact-tie test fixture**, not a model result, and not an output any current command emits:

```json
{
  "schema_version": "0.1",
  "candidate_ids": ["A", "B"],
  "target": "adherence",
  "preferred_candidate": null,
  "score_margin_a_minus_b": 0.0,
  "predicted_preference_probability": null,
  "probability_event": "A_beats_B_given_brief_and_population",
  "calibration_status": "unvalidated",
  "calibration_id": null,
  "abstain": true,
  "reason_codes": ["score_tie", "calibration_unvalidated"],
  "model_version": "fixture-only",
  "evaluation_scope": "10s_excerpt_brief_adherence",
  "human_acceptance": "pending",
  "evidence": []
}
```

**Proposed probability rule, unimplemented.** When a probability is enabled, it means P(A beats B), irrespective of which candidate wins. A probability for the selected winner needs a different field name. A raw sigmoid may be logged for research. It is not the validated-probability field. Measured evidence uses `kind="measured"`. Inferred estimates use `kind="estimated"`. The crop diagnostics in section 8 already use `kind="measured"`. No lyrical, emotional, or instrumental explanation is generated from a score.

### Model bundle

**Unimplemented.** The 9 October bundle contract stands as a future artifact. A bundle is specified to contain `weights.safetensors` (MLP) or a numeric coefficient array (linear), `model.json`, `feature_spec.json`, `preprocessing.json`, `normalization.npz`, optional `calibration.json`, `training_manifest.json`, `metrics.json`, `MODEL_CARD.md`, license notices, and SHA-256 checksums. It does not embed third-party encoders or source audio unless their redistribution is separately allowed. Loaders are specified to verify hashes and shape or version compatibility. Prefer safe tensor formats. If an upstream checkpoint uses pickle, pin it and use restricted weight loading. Do not auto-enable arbitrary remote code. A release cannot claim an Apache-licensed end-to-end model because the newly written code is Apache-2.0. A personal profile defaults to private. None of these files are written by the core tree.

Metadata the bundle is specified to record, and does not yet record: target semantics, scope, listener or population, architecture, trained and frozen parameter counts, seeds, code commit, dependency lock hash, split hashes for train, validation, calibration, and test, a data-rights summary, training-data origins, and known unsupported inputs.

### Generator boundary

**Deferred. Explicit non-goal for protocol v0.1’s build.** The 9 October generator contract is a file interface for a later experiment: immutable candidate ids, local audio paths, excerpt bounds, the original brief, optional lyrics, seed, model revision, and rights records. Internal generator scores are generator-specific estimated evidence, separate from ranker outputs. The orchestrator stores acceptance as new feedback. It does not treat a score increase as creative approval, and it does not rewrite prompts. Best-of-N selection and generator optimization remain later experiments. The current API does not require a generator to be installed. Project direction places generator integration outside this protocol.

## 13. Security, provenance, and release

**Implemented** controls:

- The foundation is offline. `network_access` must be false or `validate` fails. No command downloads audio or weights. Model acquisition is not a hidden step of validation.
- Manifest paths cannot leave the dataset root. Cache keys cannot be used as relative paths.
- Feature files are loaded with `allow_pickle=False`. Object arrays and pickle errors become `schema_invalid`.
- Ingest copies bytes the operator already has. It records a decode command and does not run it. It does not assign permissions.
- Duplicate ingest and prepare refuse to overwrite. A failed ingest or prepare removes only the files that attempt created.
- File bytes, PCM, evidence, and prepared WAV hashes are checked on the paths that claim them.
- Git ignores `data/`, `runs/`, `cache/`, `checkpoints/`, generated fixture audio, and audio, embedding, and weight suffixes. The status record’s wheel check found no audio or weights inside the `votelle_music` 0.1.0 packages.
- The CLI prints an error code and a remediation. It does not print a traceback as its contract, and it does not print the exception class name.

**Proposed** controls, from the 9 October note and the encoder handoff, for code that does not exist yet: hash checks on bundle load, rejection of incompatible feature versions, no auto-uploaded music, no retraining triggered by inference, restricted weight loading, and remote code left off. Resource stops for a future probe (RSS, memory pressure, swap growth) stay in the status record and the encoder note. They are not enforced by `votelle-music validate`.

**Release.** Apache-2.0 does not make a recording, a label, an embedding, or a checkpoint releasable. `commercial_ready` is unavailable while any of the five release-related permissions is unknown or denied. P-01 is in that state. `research_only` labels a research use. It is not a publication clearance. `in_manifest: true` is not a release.

## 14. Acceptance tests and pending milestones

### Tests that exist

**Implemented** software checks. The foundation sequence, from the repository root, is:

```bash
uv sync --locked --group dev
uv run python tests/fixtures/build.py --dest tests/fixtures/pilot --families 20
uv run votelle-music validate --config configs/foundation.json
uv run votelle-music split --config configs/foundation.json --output runs/split.json
uv run pytest -q
```

Do not point that split at `configs/p01_piano.json`. The same sequence is `.github/workflows/ci.yml`. The status record says the workflow was checked locally and that hosted GitHub Actions has not run it.

The status record, checked 10 October 2026, reports a later naming-migration run of the tracked suite as 77 passed, and an earlier foundation run the same day as 59 passed. This writing pass did not re-run pytest, validate, or split. The counts below describe what the tests lock, not a new execution.

| Test module | What it locks |
|---|---|
| `tests/test_cli.py` | `validate` exit 0 on a permitted fixture and exit 1 when rights are omitted. `split` exit 1 writes no file when the graph cannot be split. A 20-family split writes a file |
| `tests/test_rights.py` | Unknown research training fails under `research_only` even with a familiar license. Unknown or denied audio release fails `commercial_ready` and does not fail `research_only` when research training is allowed. Missing rights, empty components, and missing evidence fail |
| `tests/test_manifest.py` | Level-match flag pairing. Reference, path, duplicate, and bound errors. Orientation flips choices and acceptability together. Repeat session, order, pair, brief, listener, disagreement, chain, and cycle rules |
| `tests/test_splits.py` | Exact hash, parent, brief-family, comparison, and repeat edges. Generator identity is not an edge. Seed 17 yields 12 / 2 / 2 / 4 on twenty equal components. Giant components and too few groups raise `SplitError` and write nothing. Manifest-byte changes change `split_sha256` |
| `tests/test_audio.py` | Diagnostic units and `kind="measured"`. Non-finite, silence, short span, and rejected profiles. Deterministic `none_fixture_only` output of shape `(480000,)` and method `scipy.signal.resample/fft/v1`. FLAC round trip |
| `tests/test_audition.py` | Gain profile on tones: target loudness, true-peak ceiling, deterministic prepare, preprocessing-hash change, shared encoder waveform, and a validate warning when the ceiling binds. Not musical acceptance |
| `tests/test_features.py` | Dummy encoder finite, repeatable, shape `(1, 512)` float32, unit norm, `production_claim_allowed` false. `zero_norm`, `encoder_dimension`, `nonfinite_embedding`. Cache key changes with PCM, bounds, preprocessing, and revision. Store does not overwrite. Rejects path-like keys, truncated files, wrong shape, non-finite values, wrong dtype, and object arrays |
| `tests/test_ingest.py` | Three-URI catalog, receipt fields, decode command not executed, missing file not fetched, no partial state on failure, duplicate rejection, provisional versus reviewed gates, permissions not edited, `release_clearance` `not_assessed`, repeat ingest semantic and PCM identity, prepare QC, loudness exclusion, staged-asset refusal, and the P-01 config’s separation from `none_fixture_only` |
| `tests/test_readme.py` | The README does not treat fixtures as preference evidence |

`test_repeat_ingest_is_deterministic` compares semantic identity and PCM across different WAV metadata, checks each file’s provenance hash, and rejects duplicate overwrites.

### Pending milestones

| Milestone | Status on 10 October 2026 |
|---|---|
| Listening study, finalized creator brief, musically accepted 10-second crops, human judgments | Not run. Procedure: [`02_P0_LISTENING_PROTOCOL.md`](02_P0_LISTENING_PROTOCOL.md) |
| Core CLAP adapter in this environment | Not implemented. Foundation encoder gate stays on `dummy` / `fixture-v1` |
| 20-clip benchmark and MPS parity | Not run. Single-clip CPU feasibility is recorded and does not substitute |
| Three-clip cosine matrix | Runner recorded as ready and not executed |
| Training, linear scorer, neural challenger, calibration, inference bundle | Not implemented. No preference model has been trained |
| `commercial_ready` for P-01 | Unavailable while release permissions are unknown |

Model-quality promotion is governed by the training plan, not by passing these software tests. A complete research MVP may finish with a negative predictive result and no recommended checkpoint.

## 15. Contradictions with the 9 October specification

The 9 October note is [`docs/archive/research-preconsolidation-2026-10/06_MVP_Technical_Specification.md`](../archive/research-preconsolidation-2026-10/06_MVP_Technical_Specification.md). It was not rewritten. Source wins for the behavior below. The older sentences remain requirements only where section 12 or section 5 marks them proposed. They are not the names or the field lists the code implements.

**Package name.** The 9 October note says: “Working package name `music_pref` is a neutral implementation placeholder, not a branding decision.” The live distribution is `votelle-music`, the import package is `votelle_music`, and decision 0004 records that migration. Decisions 0001–0003 still say `music-pref`. That historical spelling is intentional.

**CLI surface.** The 9 October note says: “Proposed commands: `music-pref validate`, `split`, `prepare`, `extract`, `train`, `evaluate`, `compare`, `rank`, `audit-release`.” The implemented program is `votelle-music` with `validate`, `split`, `ingest`, and `prepare`. `ingest` is implemented and is absent from that sentence. `extract`, `train`, `evaluate`, `compare`, `rank`, and `audit-release` are not implemented. The same note says: “Dry-run prints planned files and resource requirements without downloading or invoking paid services.” No dry-run argument exists. The offline and no-download behavior does exist for the four implemented commands.

**Installed encoder protocol.** The 9 October note says: “These are proposed interfaces, not installed functions.” It then shows `embed_audio(self, clips: list[PreparedClip])`. `AudioTextEncoder` is installed in `features/base.py`, and `embed_audio` takes `list[PreparedExcerpt]`. `CandidateScorer`, `train`, `evaluate`, `compare`, and `rank` are still absent. Decision 0002 says: “`embed_audio` already takes `PreparedExcerpt`.”

**Clip row.** The 9 October note says: “Clip: `clip_id`, `asset_id`, `start_seconds`, `end_seconds`, `audition_condition`, preprocessing ID/hash, prepared-audio hash, diagnostics reference and split-group ID.” The `Clip` model is `schema_version`, `clip_id`, `asset_id`, `start_seconds`, `end_seconds`, and `audition_condition`. Preprocessing and prepared-PCM hashes are on the QC sidecar and on `PreparedExcerpt`. Split membership is on the split artifact. The extra fields remain proposed requirements sitting on those neighboring objects, or, for a split-group id on the clip itself, unimplemented.

**Duration tolerance.** The 9 October note says clips need “a ten-second duration within a small numerical tolerance.” Decision 0001 and the source lock that tolerance at 1 ms: “v0.1 clips must be 10 seconds within 1 ms. Do not pad or trim.”

**Feature records.** The 9 October note says: “Feature records contain encoder ID/revision, processor and preprocessing hashes, dimension, dtype, pooling, input hashes, hardware and extraction software versions.” The cache payload has the identity, bounds, preprocessing hash, processor hash, pooling, and dtype. It does not include hardware or extraction software versions. `EncoderSpec` holds dimension, pooling, and dtype beside the cache key, not inside it.

**Split exclusions and trained artifacts.** The 9 October note says: “Persist `split_version`, seed, grouping policy, asset/brief/judgment manifest hashes, exact component membership, per-split IDs, excluded IDs and reasons. Persist the same split hash inside every trained artifact.” The writer persists the version, seed, policy, manifest hashes, component membership, and per-split ids. `excluded` is always `[]`, with no reason objects. No trained artifact exists to store `split_sha256`.

**Chorus-arc briefs.** The 9 October note says: “Briefs that require an entire chorus arc fail the v0.1 scope check or require explicit human revision.” No such check exists. The requirement is unmet, not withdrawn.

**Superseding corrections and private notes.** The 9 October note says: “Append corrections as superseding events rather than silently rewriting history.” History is not rewritten. The implemented link is `is_repeat_of`, not a superseding-correction type. The same note says notes are “private by default.” The field is stored. No privacy enforcement is implemented.

**MPS fallback.** The 9 October note says: “If MPS fails, an explicitly configured CPU fallback may proceed and is logged.” The core tree has no MPS path and no such fallback. The isolated probe stayed on CPU. MPS parity is unverified.

**Historical command names in decisions 0002 and 0003.** Those decisions still say `music-pref validate` and `music-pref split`. Decision 0004 retains that text on purpose. The source commands are `votelle-music validate` and `votelle-music split`.

## 16. Limitations

- This note was written from the main checkout’s source, tests, configs, decisions, status, and the uncommitted encoder note, plus the Wave A governance and listening companions. It did not re-run the foundation sequence, did not run split on the P-01 config, and did not inspect private audio.
- `pcm_hash` hashes native `np.float32` bytes. Decision 0001 requires little-endian float32. The recorded hosts are little-endian. The function does not encode an explicit little-endian dtype.
- The loudness implementation is the decision 0002 procedure. It is not an EBU-certified meter, and a fixture tone is not a musical acceptance test.
- The dummy encoder’s unit vectors are a keyed random draw. They are not CLAP embeddings. `production_claim_allowed` is false.
- `validate` refuses non-dummy encoders. `ingest` does not repeat that check. A mis-pointed ingest config can copy files without proving the encoder gate.
- The split command will accept any config that validates, including `configs/p01_piano.json`. The prohibition on splitting P-01 is a decision and an operator rule, not a special case in `cli.py`.
- Near-duplicate audio is invisible to the identity graph. Exact hashes and ids are the implemented edges.
- The single-clip CPU probe, the four-text cosines, and the unrun three-clip runner are status facts. They are not core-tree behavior, and this note does not treat them as preference evidence.
- Rights conclusions in the governance note are not restated here. A reader who needs a catalog disposition has to open that note.
- Training metrics are not restated here. No number in the training plan is a measured Votelle score.
- Companion notes are [`01_DATA_GOVERNANCE.md`](01_DATA_GOVERNANCE.md), [`02_P0_LISTENING_PROTOCOL.md`](02_P0_LISTENING_PROTOCOL.md), [`03_ENCODER_AND_MODEL.md`](03_ENCODER_AND_MODEL.md), and [`04_TRAINING_AND_EVALUATION.md`](04_TRAINING_AND_EVALUATION.md).

## 17. Sources

| Path | Used for |
|---|---|
| `src/votelle_music/cli.py` | The four commands, arguments, exit codes, and stderr shape |
| `src/votelle_music/schemas.py` | Schema `0.1`, `VotelleError`, manifest models, config locks |
| `src/votelle_music/data/manifest.py` | Load, references, media checks, `validate` refusals, orientation |
| `src/votelle_music/data/rights.py` | Policy gates and the license-string rule |
| `src/votelle_music/data/ingest.py` | P-01 catalog, receipt, prepare, rollback |
| `src/votelle_music/data/paths.py` | `path_escape` |
| `src/votelle_music/data/identity.py` | Exact-id components and weight |
| `src/votelle_music/data/splits.py` | `random.Random(seed)`, atomic write, `SplitError` |
| `src/votelle_music/audio/prepare.py` | 480,000 samples, profiles, `waveform_for_encoder` |
| `src/votelle_music/audio/loudness.py` | Method ids cited from decision 0002. The meter was not rederived |
| `src/votelle_music/audio/measure.py` | Silence threshold and crop diagnostics |
| `src/votelle_music/features/base.py`, `dummy.py`, `cache.py` | Protocol, dummy encoder, cache key |
| `pyproject.toml`, `uv.lock` | Name, script, license, dependencies |
| `configs/foundation.json`, `configs/p01_piano.json` | Live configs. Split was not run on the P-01 file |
| `tests/test_cli.py`, `test_rights.py`, `test_manifest.py`, `test_splits.py`, `test_audio.py`, `test_audition.py`, `test_features.py`, `test_ingest.py` | Contracts those tests lock |
| `docs/decisions/0001-foundation-choices.md` | Rights, PCM, identity, dummy encoder, cache fields |
| `docs/decisions/0002-audition-normalization.md` | Loudness procedure and the future adapter rules, including `brief_too_long` |
| `docs/decisions/0003-p01-ingestion.md` | Catalog, gates, and the split prohibition |
| `docs/decisions/0004-votelle-naming.md` | Live names and retained historical spelling |
| `docs/STATUS.md` | Implementation status, P-01 snapshot, CLAP probe scope, recorded test counts |
| `docs/archive/research-preconsolidation-2026-10/06_MVP_Technical_Specification.md` | Broader 9 October contract and the quoted contradictions |
| `docs/research/03_ENCODER_AND_MODEL.md` | Encoder algebra, probe measurements, and the proposed ranker. Not copied |
| `docs/research/04_TRAINING_AND_EVALUATION.md` | Hypotheses and metrics. The 9 October plan is the archived predecessor |
| `docs/research/01_DATA_GOVERNANCE.md` | Rights policy detail. Not copied |
| `docs/research/02_P0_LISTENING_PROTOCOL.md` | Listening procedure. Not copied |
| `docs/PROJECT_DIRECTION.md` | Non-goals and the protocol boundary only |

Companion notes are the consolidated research documents named above. This specification does not restate them.
