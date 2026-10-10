# 06 — MVP Technical Specification

Research v0.1 · October 9, 2026 · Authority for MVP scope and contracts

## Problem and user

A musician has several short candidate regions and a defined creative brief. The system should learn whether one candidate better matches that brief and, separately, whether a particular listener prefers it. The purpose is to reduce auditioning effort while preserving creative acceptance by the human.

Primary user: Justin as a creator and ML researcher. Secondary user: a developer reproducing the experiments or contributing authorized audio and labels. Population-level music judgment is not presumed from a single-user study.

**Release scope:** a Python library, CLI, manifest format, cached-feature training/evaluation pipeline, model card, and an optional small checkpoint when the rights and evidence gates permit. Working package name `music_pref` is a neutral implementation placeholder, not a branding decision.

## Inputs, outputs and non-goals

Inputs: two to eight candidate excerpts, each explicitly bounded to ten seconds; one original English creative brief about properties audible within the excerpt; optional pseudonymous listener/model profile; explicit target (`adherence` or `personal_preference`). Store generation provenance without using generator identity as a predictive feature.

Outputs: candidate scalar scores and ordering, pairwise margins, optional validated probabilities, abstention and reason codes, exact model/feature versions, evaluation scope, and separately computed audio diagnostics. Any recommendation remains provisional until human acceptance.

Non-goals: full-song structural judgment; lyric transcription/fidelity; voice identity matching; generation; editing; DAW; prompt-rewriting agent; reinforcement learning of a generator; hosted accounts; subscriptions/payments; vector database; distributed training; production SaaS; universal taste prediction; a long-form explaining language model.

Architecture and objective are authoritative in 03. Dataset/rights policy is authoritative in 04; training/evaluation and promotion gates in 05. This specification does not override those decisions.

## Functional pipeline

1. Validate manifest, rights scope, media references and target-label definitions.
2. Resolve source/family identities and assign leakage-safe splits.
3. Prepare versioned excerpts and diagnostics; preserve original media.
4. Extract and cache frozen representations with a content-based key.
5. Fit fixed-feature baselines, then linear model, then the neural challenger if data supports it.
6. Evaluate the predeclared experiments without test-driven tuning.
7. Fit optional calibration and threshold artifacts in their dedicated data scope.
8. Load a self-contained model bundle for inference; reject incompatible feature versions.
9. Record human feedback as a new immutable event. Retraining is an explicit later operation.

## Storage contracts

Use UTF-8 JSONL for manifests and feedback; NPZ/NPY for small cached numeric arrays (`allow_pickle=False`); JSON for configuration and reports; Safetensors for neural weights. Keep large media and caches out of Git. No database is necessary initially.

### `assets.jsonl`

| Field | Type / invariant |
|---|---|
| `schema_version`, `asset_id` | Version string and unique stable ID |
| `relative_path`, `sha256_original`, `sha256_pcm` | Local path below dataset root; byte and canonical-audio hashes |
| `source_recording_id`, `song_family_id` | Required ancestry identifiers; do not invent distinct families for crops |
| `artist_id`, `contributor_id` | Optional pseudonymous IDs; unknown explicitly represented |
| `origin_type` | `original`, `contribution`, `generated`, `public_dataset`, `test_fixture` |
| `source_uri`, `acquired_at`, `source_revision` | Provenance; source URI need not be publicly published |
| `generator` | Optional object: model ID, revision, seed, settings hash, component-license evidence |
| `sample_rate`, `channels`, `duration_seconds` | Measured source properties |
| `rights_record_id`, `parent_asset_ids` | Rights linkage and full derivative ancestry |

### `rights.jsonl`

Record `rights_record_id`, rightsholder/contributor, evidence path/URL and hash, date, license identifier, applicable components (recording/composition/lyrics/prompt/labels), attribution text and exceptions. Permissions are separate `allowed|denied|unknown` fields for research training, commercial training, audio release, embeddings release and checkpoint release. Add `review_status` and review rationale.

The validator does not infer permission from a familiar license string alone; it checks the audited record against the selected policy profile. Unknown permission blocks that use. Original self-authored fixtures can carry an explicit first-party declaration.

### `briefs.jsonl` and `clips.jsonl`

Brief: `brief_id`, `brief_family_id`, exact `text`, language, optional human-authored audible clauses, intended scope, rights reference and content hash. A paraphrase shares a family with the original request. Briefs that require an entire chorus arc fail the v0.1 scope check or require explicit human revision.

Clip: `clip_id`, `asset_id`, `start_seconds`, `end_seconds`, `audition_condition`, preprocessing ID/hash, prepared-audio hash, diagnostics reference and split-group ID. Require valid bounds and a ten-second duration within a small numerical tolerance; do not silently pad short music or trim long input.

### `judgments.jsonl`

| Field | Type / rule |
|---|---|
| `judgment_id`, `pair_id`, `session_id` | Unique event, unordered canonical comparison, session |
| `brief_id`, `clip_a_id`, `clip_b_id` | Same brief; distinct candidate IDs |
| `listener_id`, `timestamp`, `presentation_order` | Anonymous listener, timing and randomized display order |
| `adherence_choice`, `preference_choice` | Each independently `A`, `B`, `tie`, `cannot_judge`, or null |
| `acceptable_a`, `acceptable_b` | `yes`, `no`, `unsure`, or null |
| `confidence`, `reason_codes`, `notes` | Optional; notes private by default |
| `listened_seconds_a/b`, `is_repeat_of` | Playback evidence and repeat provenance |
| `label_source` | `human`, `teacher`, `synthetic_rule`; never mix silently |
| `label_rights_record_id` | Permission to use/release feedback |

Store original display orientation, and canonicalize targets during loading. Flipping candidates must flip A/B targets and acceptability fields together. Append corrections as superseding events rather than silently rewriting history.

### `splits.json` and feature metadata

Persist `split_version`, seed, grouping policy, asset/brief/judgment manifest hashes, exact component membership, per-split IDs, excluded IDs and reasons. Persist the same split hash inside every trained artifact. Feature records contain encoder ID/revision, processor and preprocessing hashes, dimension, dtype, pooling, input hashes, hardware and extraction software versions.

## Interfaces

These are proposed interfaces, not installed functions.

```python
class AudioTextEncoder(Protocol):
    def describe(self) -> EncoderSpec: ...
    def embed_audio(self, clips: list[PreparedClip]) -> FeatureBatch: ...
    def embed_text(self, briefs: list[Brief]) -> FeatureBatch: ...

class CandidateScorer(Protocol):
    def score(self, audio_features, text_features) -> np.ndarray: ...
    def describe(self) -> ModelSpec: ...

def train(config: TrainConfig, dataset: DatasetIndex) -> RunManifest: ...
def evaluate(bundle: ModelBundle, split: LockedSplit) -> EvaluationReport: ...
def compare(request: CompareRequest, bundle: ModelBundle) -> CompareResult: ...
def rank(request: RankRequest, bundle: ModelBundle) -> RankResult: ...
```

`CandidateScorer` consumes features, not paths or generator sessions. `compare` validates target, scope, listener support and cache compatibility before invoking it. `rank` scores candidates independently under one shared brief/model/target; it does not average adherence and preference. Missing personal training means that target is unsupported, rather than silently substituting generic quality.

Example response **for an exact-tie test fixture**, not a model result:

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

Probability, when enabled, always means **P(A beats B)**, irrespective of which candidate wins. A separate field may expose the probability of the selected winner, but it must be named differently. A raw sigmoid may be logged privately for research; it is not placed in the validated-probability field.

Measured evidence entries include metric, value, unit, source audio hash, method/version, and `kind="measured"`; inferred estimates use `kind="estimated"`. No lyrical, emotional or instrumental explanation is generated unless it comes from a separate validated measurement/estimator or is clearly labeled human feedback.

## CLI surface

Proposed commands: `music-pref validate`, `split`, `prepare`, `extract`, `train`, `evaluate`, `compare`, `rank`, `audit-release`. Each accepts a configuration file and explicit dataset/model paths. Dry-run prints planned files and resource requirements without downloading or invoking paid services. Evaluation writes predictions, exclusions and group counts as well as aggregate scores.

Default behavior is local and offline once required artifacts exist. No hidden API calls, silent model downloads during simple validation, auto-uploaded music, or retraining triggered by an inference request. Model acquisition is a distinct explicit command/step.

## Model bundle and provenance

A bundle contains `weights.safetensors` (MLP) or a numeric coefficient array (linear), `model.json`, `feature_spec.json`, `preprocessing.json`, `normalization.npz`, optional `calibration.json`, `training_manifest.json`, `metrics.json`, `MODEL_CARD.md`, license notices and SHA-256 checksums. It does not embed third-party encoders or source audio unless their redistribution is separately allowed.

Model metadata records target semantics, scope, listener/population, architecture, trained/frozen parameter counts, seeds, code commit, dependency lock hash, training/validation/calibration/test split hashes, data-rights summary, training-data origins, and known unsupported inputs. A personal profile defaults to private. A release cannot claim an Apache-licensed end-to-end model merely because the newly written code is Apache.

Loaders verify hashes and shape/version compatibility. Prefer safe tensor formats; if an upstream official checkpoint uses pickle serialization, pin it and use supported restricted weight loading. Do not auto-enable arbitrary remote code or execute files from an unreviewed repository.

## Error and uncertainty behavior

Invalid file/path, unsupported format, nonfinite waveform, bad bounds, missing rights, incompatible feature dimension and wrong checkpoint hashes produce typed errors and nonzero CLI exits. Valid but unsupported domain, untrained personal target, out-of-scope brief, unresolved tie or insufficient margin produce explicit abstention/unsupported status. Different cases must not be compressed into a zero score.

If MPS fails, an explicitly configured CPU fallback may proceed and is logged. An out-of-memory failure never silently shortens a clip, switches encoders, changes precision, or changes preprocessing. Retry with a smaller batch or a documented separately versioned fallback.

## Acceptance criteria and tests

- Core validation and fixture tests run offline without Torch/model downloads.
- Rights records block prohibited/unknown uses; artifact ancestry is preserved.
- Repeated records, alternate encodings, crops and shared brief families cannot cross prohibited partitions.
- Candidate-order reversal negates margins; equal features yield zero margin; changes to briefs can affect the conditional scorer.
- Cache keys change when audio, excerpt, preprocessing, encoder or processor changes.
- Real extraction passes finite-value, shape and repeatability checks on a small authorized sample.
- Train-only normalization and calibration-only fitting are enforced by interfaces/tests.
- Checkpoint save/load gives equivalent scores within documented numerical tolerance.
- All evaluation outputs include exclusions, ties, group counts, target definitions and uncertainty.
- Unsupported inputs never produce a confident fabricated recommendation.
- A clean environment can reproduce a recorded run within stated platform tolerance.

Model-quality promotion is governed by 05, not by passing software tests. Hardware/cost gates are in 07. A complete research MVP may finish with a negative predictive result and no recommended learned checkpoint.

## Future generator integration contract

A generator adapter returns immutable candidate IDs, local audio paths, excerpt bounds, original brief, optional original lyrics, seed, model revision, and rights/provenance records. It can additionally provide internal scores as **generator-specific estimated evidence**, separate from ranker outputs. Generator packages stay in their own environments and communicate through files/manifests.

The orchestrator requests scoring, inspects abstention, presents candidates to the creator, and stores acceptance/rejection as new feedback. It never treats score improvement as creative approval or changes prompts automatically. Best-of-N selection, revision and generator optimization remain later experiments; this model's API does not require ACE-Step, YuE2 or HeartMuLa to be installed.
