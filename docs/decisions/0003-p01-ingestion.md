# 0003 — P-01 real-audio ingestion

Session 2A.1 of research v0.1. This adds local intake for the Reflective Piano pilot. It does not change excerpt length, grouping rules, rights policy, or label meaning. Manifest schema stays `0.1`. `configs/foundation.json` and the fixture profile `none_fixture_only` are unchanged.

No audio is downloaded. No license is read from a filename, ID3 tag, or catalog row. No split is written. P-01 is an acquisition and listening pilot, not a training set. The split fractions in `configs/p01_piano.json` exist because the config schema requires them. Do not run `music-pref split` on this dataset.

## Files

The MP3 from the official URI is the raw original. It is copied and never modified. It is not an `assets.jsonl` row: the locked validator accepts WAV and FLAC only, and a decoded derivative is not a lossless master. `lossless_master` on the receipt is false.

The WAV or FLAC the operator decoded is the manifest asset. `sha256_original` is that file's bytes. `sha256_pcm` is the canonical float32 PCM of that decode, before crop or resample. The receipt stores the MP3 path and hash separately, plus the decode tool, version, and command. The command is recorded and is not executed.

| Path under `data/p01_piano/` | Role |
|---|---|
| `raw/<slug>.mp3` | Unmodified copy of the official MP3 |
| `decoded/<slug>.wav` or `.flac` | Operator-decoded derivative and manifest asset |
| `receipts/<asset_id>.json` | Acquisition receipt |
| `evidence/` | Local rights snapshot supplied by the operator |
| `assets.jsonl`, `rights.jsonl`, `briefs.jsonl`, `clips.jsonl` | Existing manifest models |
| `judgments.jsonl` | Required. May be empty |
| `prepared/<clip_id>.wav` | Float32, 48 kHz, mono, 480,000 samples |
| `qc/<clip_id>.json` | QC sidecar |

`data/` is gitignored. The first successful `ingest` creates the manifest files it needs.

## Catalog and identity

Only these official URIs are accepted:

| Recording | ISRC | URI |
|---|---|---|
| Disquiet | USUAN1500036 | `https://incompetech.com/music/royalty-free/mp3-royaltyfree/Disquiet.mp3` |
| Mesmerize | USUAN1500005 | `https://incompetech.com/music/royalty-free/mp3-royaltyfree/Mesmerize.mp3` |
| Colorless Aura | USUAN1400008 | `https://incompetech.com/music/royalty-free/mp3-royaltyfree/Colorless%20Aura.mp3` |

`source_recording_id` is one stable id per official URI. `song_family_id` is distinct per URI. The same artist id does not merge families. A family merges only when a review file has `review_status` `reviewed`, a rationale, and a group of at least two catalog URIs. Passing that file on a later ingest does not rewrite rows already written.

A second ingest of the same URI, the same raw hash, or the same decoded PCM is `duplicate_id`. Existing bytes are left as they are. A failed ingest deletes only the files that attempt created.

## Three different gates

Provisional rights review, dataset eligibility, and release clearance are not the same state.

- **Provisional review.** No rights id, `review_status` other than `reviewed`, or a missing or hash-mismatched local evidence file. The receipt says `rights_gate: provisional_review` and `in_manifest: false`. Nothing is appended to `assets.jsonl`. A URL without a local evidence file stays here.
- **Manifest candidate.** An existing rights row is `reviewed` and its local evidence file matches `evidence_sha256`. Ingest appends an asset and does not edit `rights.jsonl`. Permissions stay whatever the operator wrote, including `unknown`. `release_clearance` on the receipt is `not_assessed`.
- **Dataset eligibility.** `music-pref validate --config configs/p01_piano.json`. The policy is `research_only`, so `research_training` must be `allowed`. Unknown still fails. This is the existing rights check, not a new one.
- **Release clearance.** `commercial_ready` requires `allowed` on research training, commercial training, audio release, embedding release, and checkpoint release. Ingest never sets those fields and never grants release.

`in_manifest: true` means the rights row was reviewed and evidenced. It does not mean validate passed, and it does not mean the clip is cleared to publish.

## Preparation

`prepare` takes operator-supplied start and end times and calls `prepare_excerpt` with `gain_lufs_v1`. It writes the float32 WAV and a QC sidecar. A loudness mismatch is `excluded_loudness_mismatch` and is not appended to `clips.jsonl`. A match within 0.1 LU of -20, at or under -1 dBTP, is `primary_level_matched` and is the only result that becomes a clip row. Staged assets are refused. Musical suitability is not decided here.

Brief text is not invented. `briefs.jsonl` stays empty until the operator writes one.
