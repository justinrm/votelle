# Data governance

This note consolidates Votelle's dataset landscape, acquisition suitability, permission model, and release gates for research protocol v0.1. It states what the software records and blocks, what the rights audit verified, and which permissions remain unresolved.

Listening procedure, trial structure, and musical acceptance criteria stay in [02_P0_LISTENING_PROTOCOL.md](02_P0_LISTENING_PROTOCOL.md). The 9 October procedure remains in the [archived protocol](../archive/research-preconsolidation-2026-10/02_P0_Dataset_and_Listening_Protocol.md) as historical evidence. This note covers the rights, privacy, and consent constraints around those judgments. It does not restate the listening method. Live commands use `votelle-music`; historical `music-pref` spellings in decisions 0001–0003 are recorded in [decision 0004](../decisions/0004-votelle-naming.md).

**Protocol:** v0.1. **Evidence date:** 10 October 2026.

Claim labels used below:

- **Verified evidence** — a primary page, an accepted decision, or the current source, tests, or config.
- **Derived** — arithmetic on an inspected snapshot, not remeasured for this note.
- **Measurement** — a named observation recorded elsewhere. This note does not recompute it.
- **Estimate** — a planning figure.
- **Proposed method** — a procedure or target that has not been executed as a cleared dataset.
- **Unresolved** — an open gate. An unknown permission stays unknown.

License conclusions in the source audit are scoped readings of published grants. They are not warranties about every underlying right, and they are not legal clearance. A permission declaration is not legal clearance.

## Executive summary

Votelle can store an explicit rights profile and reject a use when a required permission is `unknown` or `denied`. A license string does not grant a permission. The tree does not clear a recording, a composition, a sample, a lyric, a human label, an embedding, or a checkpoint.

The [feasibility audit](../archive/research-preconsolidation-2026-10/01_Data_Feasibility_and_Rights_Audit.md) is a **conditional** acquisition case for a small pilot. Its strongest published source-level evidence is Kevin MacLeod's Incompetech catalog: an explicit offer of the catalog for AI training, CC BY 4.0 terms, and individual file URLs. That is source-level evidence. It is not an asset-level `allowed` value, and it does not authorize public release of embeddings or checkpoints.

P-01 is an acquisition and listening pilot, not a training set. The ingest catalog accepts three official recordings only: Disquiet (ISRC USUAN1500036), Mesmerize (USUAN1500005), and Colorless Aura (USUAN1400008). Git does not contain the audio. The earlier local intake snapshot recorded each receipt as `reviewed_with_evidence` and `in_manifest: true`, with `research_training` `allowed` and commercial training, audio release, embedding release, and checkpoint release `unknown`. `release_clearance` was `not_assessed`. Brief, clip, and judgment manifests were empty. **Unresolved:** `commercial_ready` is unavailable while those release permissions are unknown. This consolidation did not inspect private audio or re-validate that intake.

First-party recordings and direct contributor grants remain the preferred route for a releasable experiment. Both inventories are empty. Public corpora, Jamendo-derived collections, and generator outputs stay on separate, narrower terms. Suno-origin audio is excluded from training and from a releasable benchmark unless written permission covers that use.

## Current evidence and implementation status

Authority, as recorded in the [research index](README.md): source, tests, configs, and `uv.lock` say what runs; [accepted decisions](../decisions/0001-foundation-choices.md) are the engineering choices; this directory holds scientific requirements the tests do not retire; the [archive](../archive/README.md) is earlier rationale; [project direction](../PROJECT_DIRECTION.md) does not expand protocol v0.1.

| Layer | Status on 10 October 2026 | Label |
|---|---|---|
| Rights profile and policy gate | Implemented in `votelle_music`. Policies are `research_only` and `commercial_ready`. | Verified evidence |
| P-01 local intake | Implemented. Copies operator-supplied files. Records a decode command and does not run it. Does not download audio. Does not edit `rights.jsonl`. | Verified evidence |
| P-01 private audio and receipts | Git-ignored under `data/`. Absent from a clone. The intake snapshot is the account in [status](../STATUS.md). | Recorded status; not re-validated here |
| Human listening study | Not run. No finalized creator brief and no musically accepted 10-second crops. | Unresolved |
| Training, embeddings as a product, checkpoint release | Not implemented. The core environment has no training loop and no released weights. | Verified evidence |
| Apache-2.0 | Selected 10 October 2026 for original source code and project documentation. Root [LICENSE](../../LICENSE); `pyproject.toml` declares `Apache-2.0`. | Verified evidence |

Apache-2.0 does not change third-party library or model licenses and does not grant recording, composition, annotation, training, or artifact-release permissions. P-01 permission declarations are unchanged by that license selection.

Decision [0004](../decisions/0004-votelle-naming.md) sets the live names: project Votelle, package `votelle_music`, CLI `votelle-music`, exception `VotelleError`. Protocol stays v0.1. Decisions 0001–0003, the archive, and the active research notes still say `music-pref` / `music_pref`. Those files were left in place. Where this note cites a historical command, it names the current CLI beside it.

The package under test uses schema `0.1`. Fixture tones described in [tests/fixtures/FIRST_PARTY_DECLARATION.md](../../tests/fixtures/FIRST_PARTY_DECLARATION.md) are generated signals for software tests. `configs/foundation.json` sets `rights_policy` to `commercial_ready` on that fixture root. A passing fixture validate checks the gate. It is not a music clearance and not evidence of preference prediction.

## 1. Dataset landscape and acquisition suitability

Two inventories overlap and answer different questions. The [feasibility audit](../archive/research-preconsolidation-2026-10/01_Data_Feasibility_and_Rights_Audit.md) asks where a small pilot can acquire audio. The [dataset strategy](../archive/research-preconsolidation-2026-10/04_Dataset_and_Human_Feedback_Strategy.md) asks which public corpora could supervise adherence or preference, and on what terms. A downloadable file, a service that assigns output rights, and a dataset that permits commercial training are three different questions.

Sizes below are the cited release or the audited snapshot. Eligible pairs will be smaller after missing audio, scope, deduplication, and rights filters. No figure in this section is a count of cleared Votelle assets.

### Acquisition candidates

| Source | Scale | Rights evidence | Disposition |
|---|---|---|---|
| Original recordings supplied by Justin | Inventory unknown. **0 supplied or verified.** | Control is real when composition, recording, and performance are owned and samples are cleared. Authorship of lyrics, or payment to a generation service, is insufficient. | **Conditional.** Pending a first-party provenance declaration. Proposed method: 3 different takes or arrangements per brief, WAV or FLAC preferred, each with a usable 10-second region. |
| Direct independent-artist contribution | No contributor contacted. **0 committed.** | Needs an explicit grant for commercial ML use, derivatives, embeddings, and checkpoints, plus separate audio publication and label consent. | **Conditional** until granted. 4 briefs × 3 takes = 12 clips is a target, not inventory. |
| [Incompetech catalog](https://incompetech.com/music/royalty-free/pieces.json) | Live JSON at audit: **1,443 distinct filenames**, **87.14 hours** from listed durations; **1,439** list at least 10 seconds. Derived from snapshot SHA-256 `54802ad340562624b9d1c9c97aa9f005e2b9bf79001f8a1a07ed857e68b2164a`. MP3. Sample rate, channels, and bitrate need file inspection. No UUID field in the JSON, despite documentation that mentions one. | [Training offer](https://incompetech.com/wordpress/2022/11/music-catalog-available-for-any-ai-training-project/) and [CC BY 4.0 / attribution FAQ](https://www.incompetech.com/music/royalty-free/faq.html). The older offer's ~1,800 files / four days is not this JSON count. | **Permitted source-level route**, with attribution and per-asset review. See §3 and §5. The phrase is the audit's disposition. It is not the schema value `allowed`. |
| [MusicNet](https://zenodo.org/records/5120004) | 330 classical recordings; about 34 hours [as reported by UW](https://news.cs.washington.edu/2016/11/30/uw-researchers-hit-the-right-note-with-new-machine-learning-tool-for-music/). PCM WAV plus note CSVs. Official audio archive 11.1 GB. Exact file quality not inspected. | Zenodo API declares CC BY 4.0. The description identifies mixed CC and public-domain performances. | **Conditional** classical control. Recording-level provenance is unresolved. Not a convenient selective route. Do not fetch the archive for this pilot. |
| [Music Arena](https://huggingface.co/datasets/music-arena/music-arena-dataset/blob/main/README.md) | July 2026 release lists **1,959** included audio files (audit). Monthly card totals July 2025–July 2026 sum to **8,117 battles** (dataset strategy). Duration not established. Those are different units. | Card CC BY 4.0. Some systems' audio is withheld. Provider permissions and user lyrics or prompts still need review. | **Conditional. 0 eligible triplets verified.** Inherited votes are not Votelle labels. Eligibility is unresolved (§13). |
| [ACE-Step 1.5](https://huggingface.co/ACE-Step/Ace-Step1.5) outputs | **0 outputs** in this tree. A later workflow could propose 60 candidates from 20 briefs. | MIT metadata and a commercial-output statement on the card are promising. Component coverage is unresolved (§11). | **Conditional.** Generation is not required for the first pilot. |
| [Musopen](https://musopen.org/music/) | Large catalog. No cleared subset counted. | [FAQ](https://musopen.org/faq/) separates recording and composition rights and disclaims verification of user uploads. | **Conditional.** A public-domain icon is not clearance. |

Catalog capacity on Incompetech is ample. **Proposed method, not a measured yield:** the audit's P0 plan starts from 12 downloads aimed at 12 valid excerpts, and a wider shortlist of up to 80 tracks aimed at 60 candidates across 20 brief/source groups. Matching and provenance are the bottleneck. **Estimate:** about 3–6 hours for P0 sourcing and preparation, plus listening. No collection of Justin-owned music is assumed. The software ingest catalog is narrower than that plan: only the three P-01 URIs in §4.

### Public corpora as supervision

These rows are from the dataset strategy. They are not approved training sets.

| Dataset | Scale and labels | What it can supervise | Disposition |
|---|---|---|---|
| Music Arena | Battles and included files as above. Prompt, A/B/tie/both-bad, pseudonymous user, listening metadata. Some null audio. | Overall contextual preference. Not automatically separate adherence. | Conditional subset. Never the entire corpus by default. [S20](../archive/research-v0.1/10_Source_Register.md). |
| CMI-Pref | **4,027 votes** (3,527 train / 500 test). Card reports **133.80 hours**. Generated and reference MP3. Musicality, alignment, confidence. | Closest public task match for multimodal adherence. User histories may be sparse. | CC BY-NC-SA 4.0. Isolated research lane. Excluded from default permissive training. [S06](../archive/research-v0.1/10_Source_Register.md). |
| CMI-Pref-Pseudo | Card: ~56k generations and ~165k candidate comparisons; ~115k pseudo labels. | Teacher distillation, not independent human preference. | Same NC-SA lane. Counts conflict with the paper (§13). [S07](../archive/research-v0.1/10_Source_Register.md). |
| MusicPrefs | **5,040 audio rows.** Paper collects **2,520 pairs.** Duration aggregate not verified. Fidelity and musicality; prompts hidden during judgment. | General musicality or fidelity. Unsuitable as adherence ground truth. | **Unresolved.** Inspected card states no explicit dataset license. Metadata research only. [S49](../archive/research-v0.1/10_Source_Register.md), [S19](../archive/research-v0.1/10_Source_Register.md). |
| AIME / AIME-survey | **6,000** generated tracks + **500** Jamendo tracks. **15,600** comparisons. Judged regions 10 seconds. | Alignment and quality benchmark. Not established personalization data. | Restricted research comparator. Not default releasable data. [S22](../archive/research-v0.1/10_Source_Register.md), [S21](../archive/research-v0.1/10_Source_Register.md). |
| SongEval | Study/card: **2,399 songs, ~140 hours.** Inspected HF viewer: **1,000 rows.** | Whole-song aesthetics, including vocal phrasing. Outside the v0.1 ten-second protocol if used as full songs. | CC BY-NC-SA 4.0. Research comparator. Coverage unresolved. [S23](../archive/research-v0.1/10_Source_Register.md), [S24](../archive/research-v0.1/10_Source_Register.md). |
| MTG-Jamendo | **55,609** processed autotagging tracks. Full duration not verified. Genre, instrument, and mood tags. | Representation probes and attribute supervision. No comparative preference labels. | Exclude from the commercial-ready lane without written dataset permission. [S27](../archive/research-v0.1/10_Source_Register.md). |
| MusicCaps | **5,521** ten-second examples; **15.34 hours** of referenced excerpts. YouTube IDs, time ranges, musician-written captions. | Description or alignment research. Not personal preference. | Annotation license does not license the linked recordings. No wholesale audio acquisition. [S28](../archive/research-v0.1/10_Source_Register.md). |
| MusicBench | About **52.8k** training rows in the viewer used by the strategy. Unique original-audio hours not verified. | Attribute controls. Augmentations are not independent songs or preferences. | Provenance unresolved. No default commercial-ready training. [S29](../archive/research-v0.1/10_Source_Register.md). |
| LFM-2b | Historically more than 2 billion listening events. **Withdrawn.** | Listening metadata, not a generated-audio comparison corpus. | Rejected as an acquisition source. [S35](../archive/research-v0.1/10_Source_Register.md). |

## 2. First-party and contributor audio

**Verified evidence:** neither route has a committed inventory. The dataset strategy recommends original or explicitly contributed recordings, original briefs, and first-party human judgments as the main releasable experiment. Public research datasets stay separate, with separate approval scopes.

A first-party declaration has to cover the composition, the recording, and the performance, and it has to clear samples. Personal authorship of lyrics does not clear a recording. Paying a generation service does not clear that service's outputs for this project. The fixture declaration covers test tones only.

**Proposed method** for a contributor grant, not a form that has been sent:

- Named compositions, masters, performers, lyrics, and samples.
- Reproduction, cropping, and resampling.
- Research training and commercial training and evaluation, as separate answers.
- Distribution of embeddings and of learned weights, as separate answers.
- Audio redistribution as its own choice.
- Attribution text.
- Consent for labels, including whether public audio, anonymous votes, and trained weights are in scope.

No contributor was contacted in the audit session. A request may be drafted later. Until a reviewed rights row stores `allowed` on the uses the active policy requires, the contribution stays at review and must not be serialized as allowed.

## 3. Incompetech source and training-permission evidence

**Verified evidence** inspected by the audit, without downloading audio:

| Item | Record |
|---|---|
| Catalog | [pieces.json](https://incompetech.com/music/royalty-free/pieces.json). Snapshot SHA-256 `54802ad340562624b9d1c9c97aa9f005e2b9bf79001f8a1a07ed857e68b2164a`. Counts in §1 describe that snapshot, not later availability. |
| Access and rights documentation | [incompetech.com/agent-section/](https://incompetech.com/agent-section/) |
| Training offer | [Music catalog available for any AI training project](https://incompetech.com/wordpress/2022/11/music-catalog-available-for-any-ai-training-project/) (November 2022). Explicit offer of the catalog for AI training. |
| Attribution and CC BY 4.0 guidance | [Royalty-free FAQ](https://www.incompetech.com/music/royalty-free/faq.html) |
| CC legal code | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/legalcode.en) |
| CC note on AI training | [Using CC-licensed works for AI training](https://creativecommons.org/using-cc-licensed-works-for-ai-training-2/) |

The audit's reading uses the creator's training offer together with the CC BY commercial reproduction and adaptation grant. It does not infer ML rights from free access alone. **Unresolved:** public embedding release and trained-head release are not expressly addressed by the offer. CC BY contains no special checkpoint prohibition. Attribution and component coverage still have to be recorded before any release. Keeping an embedding private does not repair an unauthorized acquisition.

The audit's matrix cell for selected original Incompetech tracks says commercial ML is permitted under the BY grant plus the training offer, after review, and that audio release is "BY, within licensor's rights." That cell is a source-level interpretation. Section 5 records why it is not copied into `commercial_training` or the release fields.

Common composer metadata on the site is not proof that a classical arrangement is an original composition. Covers, third-party collaborators, unusual samples, and generative-service provenance stay out until clarified.

**Unresolved caution, not a file-level finding:** the original [FreePD](https://www.freepd.com/) site is closed. A mirror is not equivalent clearance. The artist's [July 2025 account](https://billy.incompetech.com/wordpress/2025/07/the-ai-elephant-in-the-room/) reports posting some Suno music on FreePD. Search-index text was available; the page fetch was intermittent. That reinforces caution. It is not proof about any particular Incompetech catalog file. Suno-origin material follows §11.

The proposed rights-record id in the audit is `INC-BY-AI-2026-10-09`, pending per-asset review. This note does not treat that id as present, reviewed, or hashed in `data/`.

## 4. P-01 recording shortlist and acquisition status

**Verified evidence — accepted catalog.** Decision [0003](../decisions/0003-p01-ingestion.md) and `P01_CATALOG` in `src/votelle_music/data/ingest.py` accept only these official URIs. `configs/p01_piano.json` sets `dataset_root` to `data/p01_piano`, `rights_policy` to `research_only`, `target` to `adherence`, `network_access` to false, and `level_matched` to true. The split fractions exist because the config schema requires them.

| Role | Recording | ISRC | Official URI | Catalog duration |
|---|---|---|---|---|
| P-01 ingest | Disquiet | USUAN1500036 | `https://incompetech.com/music/royalty-free/mp3-royaltyfree/Disquiet.mp3` | 00:03:05 |
| P-01 ingest | Mesmerize | USUAN1500005 | `https://incompetech.com/music/royalty-free/mp3-royaltyfree/Mesmerize.mp3` | 00:07:04 |
| P-01 ingest | Colorless Aura | USUAN1400008 | `https://incompetech.com/music/royalty-free/mp3-royaltyfree/Colorless%20Aura.mp3` | 00:02:38 |

Catalog durations are listed durations from the audit snapshot. They are not measurements of the Git-ignored files. Start and end times stay unset until audition. A guessed crop is not a substitute.

**Verified evidence — how intake behaves.** The official MP3 is the raw original. Ingest copies it and does not modify it. The MP3 is not an `assets.jsonl` row: the validator accepts WAV and FLAC only, and a decoded derivative is not a lossless master. The receipt field `lossless_master` is false. The operator-decoded WAV or FLAC is the manifest asset when the rights gate passes. `sha256_original` is that decoded file's bytes. `sha256_pcm` is the canonical little-endian float32 PCM of that decode, at the file's original rate and channel count, before crop or resample. The receipt stores the MP3 path and hash, plus decode tool, version, and command. The command is recorded and is not executed. Ingest does not download.

Paths under `data/p01_piano/`: `raw/<slug>.mp3`, `decoded/<slug>.wav` or `.flac`, `receipts/<asset_id>.json`, operator-supplied `evidence/`, and the JSONL manifests. `data/` is gitignored.

**Recorded intake snapshot, not re-validated here.** [Status](../STATUS.md) states that Disquiet, Mesmerize, and Colorless Aura were recorded under Git-ignored `data/p01_piano`. Each receipt was `reviewed_with_evidence` and `in_manifest: true`. `research_training` was `allowed`. Commercial training, audio release, embedding release, and checkpoint release were `unknown`. `release_clearance` was `not_assessed`. Brief, clip, and judgment manifests were empty. This consolidation did not open those files, recompute their hashes, or run validate.

`in_manifest: true` means the rights row was `reviewed` and the local evidence file matched `evidence_sha256`. It does not mean `votelle-music validate` passed. It does not mean the clip is cleared to publish. The receipt type allows only `release_clearance: not_assessed`. Ingest never writes another clearance value and never edits permission fields.

**Do not run split on P-01.** Decision 0003 states this with the historical command `music-pref split`. The current command is `votelle-music split`. The config's fractions do not make P-01 a training split. P-01 is an acquisition and listening pilot.

**Measurement recorded in status, not opened here.** A later technical excerpt was reported for an isolated probe: `data/probes/disquiet_0030_0040/waveform.wav`, Disquiet seconds 30–40, PCM SHA-256 `f78adc9e79b8bc0a115df25ae981d7daccef63d1c08924cf3b07c1b116fd4507`. That preparation does not establish musical acceptance, a completed listening dataset, or any change to the unknown release permissions.

### Wider shortlist, not in the ingest catalog

The audit's remaining rows are an acquisition plan. Each direct audio URL returned HTTP 200 to a HEAD request. No audio body was fetched. MIME was generic `application/octet-stream`, so decoding and MP3 properties were unverified. All rows are Kevin MacLeod / Incompetech, under the same pending record `INC-BY-AI-2026-10-09`. They are not accepted by `P01_CATALOG`.

| Group | Recording | ISRC | Listed duration | Official URI |
|---|---|---|---|---|
| P-02 | Night in Venice | USUAN1900056 | 00:03:38 | `https://incompetech.com/music/royalty-free/mp3-royaltyfree/Night%20in%20Venice.mp3` |
| P-02 | Lobby Time | USUAN1600054 | 00:03:13 | `https://incompetech.com/music/royalty-free/mp3-royaltyfree/Lobby%20Time.mp3` |
| P-02 | Airport Lounge | USUAN1100806 | 00:05:08 | `https://incompetech.com/music/royalty-free/mp3-royaltyfree/Airport%20Lounge.mp3` |
| P-03 | RetroFuture Clean | USUAN1200040 | 00:03:26 | `https://incompetech.com/music/royalty-free/mp3-royaltyfree/RetroFuture%20Clean.mp3` |
| P-03 | RetroFuture Dirty | USUAN1200041 | 00:03:26 | `https://incompetech.com/music/royalty-free/mp3-royaltyfree/RetroFuture%20Dirty.mp3` |
| P-03 | RetroFuture Nasty | USUAN1200042 | 00:03:26 | `https://incompetech.com/music/royalty-free/mp3-royaltyfree/RetroFuture%20Nasty.mp3` |
| P-04 | Grand Dark Waltz Allegro | USUAN2100020 | 00:06:25 | `https://incompetech.com/music/royalty-free/mp3-royaltyfree/Grand%20Dark%20Waltz%20Allegro.mp3` |
| P-04 | Grand Dark Waltz Allegretto | USUAN2100019 | 00:07:30 | `https://incompetech.com/music/royalty-free/mp3-royaltyfree/Grand%20Dark%20Waltz%20Allegretto.mp3` |
| P-04 | Grand Dark Waltz Moderato | USUAN2100018 | 00:08:28 | `https://incompetech.com/music/royalty-free/mp3-royaltyfree/Grand%20Dark%20Waltz%20Moderato.mp3` |
| B-reserve | The Complex | USUAN1300025 | 00:04:28 | `https://incompetech.com/music/royalty-free/mp3-royaltyfree/The%20Complex.mp3` |
| B-reserve | Odyssey | USUAN1500012 | 00:05:06 | `https://incompetech.com/music/royalty-free/mp3-royaltyfree/Odyssey.mp3` |
| B-reserve | New Direction | USUAN1100677 | 00:11:20 | `https://incompetech.com/music/royalty-free/mp3-royaltyfree/New%20Direction.mp3` |
| B-reserve | Clear Air | USUAN1100626 | 00:03:04 | `https://incompetech.com/music/royalty-free/mp3-royaltyfree/Clear%20Air.mp3` |
| B-reserve | When The Wind Blows | USUAN1100717 | 00:04:26 | `https://incompetech.com/music/royalty-free/mp3-royaltyfree/When%20The%20Wind%20Blows.mp3` |
| B-reserve | Funky Chunk | USUAN1500054 | 00:03:59 | `https://incompetech.com/music/royalty-free/mp3-royaltyfree/Funky%20Chunk.mp3` |
| B-reserve | Spy Glass | USUAN1500058 | 00:03:47 | `https://incompetech.com/music/royalty-free/mp3-royaltyfree/Spy%20Glass.mp3` |
| B-reserve | Darkling | USUAN1700050 | 00:02:50 | `https://incompetech.com/music/royalty-free/mp3-royaltyfree/Darkling.mp3` |

The twelve-file plan is P-01 through P-04, three recordings each. This table is the nine of those outside the ingest catalog, plus eight B-reserve files for a separate 20-unique-clip resource probe. The reserve is not a new listening family until matched alternatives are assembled and each file has its own reviewed evidence. Source-level evidence still requires decoded-file inspection and an asset-specific review. These URLs are not a redistributed audio collection.

## 5. Source-level and asset-level permissions

Source-level work answers whether a published grant is a reason to consider a catalog. Asset-level work is the JSONL row the validator reads. The audit's word "Review" means unknown for the specific assets and must not be serialized as `allowed`.

Schema permissions are only `allowed`, `denied`, and `unknown` (`votelle_music.schemas.Permission`). Audit words such as Permitted, Conditional, Blocked, Restricted, and Review are dispositions in prose. They are not legal values in `rights.jsonl`.

| Question | Source-level | Asset-level |
|---|---|---|
| Incompetech training offer and CC BY 4.0 | Published pages inspected. Audit disposition: permitted route after review, with attribution. | A rights row may cite those pages in `evidence_url`, `evidence_path`, `evidence_sha256`, `license_identifier`, and `review_rationale`. `license_identifier` alone grants nothing. |
| P-01 research training | The offer is the evidence the audit relies on. | Snapshot recorded `research_training: allowed` on the three receipts. Not re-opened here. Not a legal clearance. |
| P-01 commercial training and all three release fields | Audit matrix says commercial ML is permitted after review. Embedding and checkpoint release are not expressly addressed. | Snapshot recorded `unknown` for `commercial_training`, `audio_release`, `embedding_release`, and `checkpoint_release`. Left unknown. |
| Public dataset card | A card license describes that dataset artifact. | Each asset still needs component scope. Withheld audio is not reconstructed from another source. |
| `in_manifest: true` | Not a catalog-wide grant. | Reviewed local evidence matched the stored hash. Validate and release clearance are later gates. |

`check_rights` in `src/votelle_music/data/rights.py` implements the block: for each field the active policy requires, `unknown` is a `permission_unknown` validation error and `denied` is `permission_denied`. The remediation states that a license name does not grant the use. Missing evidence or a hash mismatch is `missing_evidence` or `hash_mismatch`. A missing component list is `missing_component_scope`.

## 6. Recording, composition, sample, lyrics, label, and derived-artifact rights

**Verified evidence — stored component kinds.** `ComponentKind` is `recording`, `composition`, `lyrics`, `prompt`, or `labels`. A rights row must list at least one. Briefs carry `rights_record_id`. Judgments carry `label_rights_record_id`. Assets carry `rights_record_id`. Prompt rights and label rights are separate records from the recording when the operator writes them that way.

**Scientific requirement, narrower than the enum.** The dataset strategy requires the written scope to cover recording, composition, performers, lyrics, and any samples. Performers and samples are not their own `ComponentKind` values. `exceptions` and `review_rationale` are free-text fields a review can use. Text in those fields is not a grant. This note does not add an enum value. An empty sample story is not a cleared sample.

| Layer | What has to be true before a releasable use | What v0.1 software does |
|---|---|---|
| Recording | The master or the decoded derivative in hand is the work the grant covers. | P-01 stores the MP3 hash on the receipt and the decoded file as the asset. `lossless_master` is false. |
| Composition | The composition right is identified. Site composer credit is not that identification for classical arrangements. | `composition` may be listed on the rights row. Ingest does not infer it. |
| Sample | Third-party samples are named and cleared, or the review says none are present and points at evidence. | No separate sample id. Unresolved if the rationale is silent. |
| Lyrics | Lyric rights are separate from the recording. A ten-second excerpt cannot validate lyric fidelity; that limit is a listening-scope rule in the protocol notes. | `lyrics` is a component kind. Absence of a lyric line is not a grant. |
| Labels | Annotator consent covers storage and any later publication of votes. Names, email, detailed history, and free text stay private by default (§10). | `labels` component and `label_rights_record_id`. `label_source` is `human`, `teacher`, or `synthetic_rule`. |
| Derived audio | Crops, resamples, codec variants, covers, and alternate renders stay tied to the parent. | `parent_asset_ids` unions known parents into the same split component. P-01 ingest writes an empty parent list on the decoded asset. The raw MP3 is not an asset row. |
| Embeddings | Redistribution is `embedding_release`. A private cache is still unauthorized if acquisition was unauthorized. | No released embedding product. Dummy encoder `dummy` / `fixture-v1` only. Any other encoder name fails validate. |
| Checkpoints | Redistribution is `checkpoint_release`. The audit's column "Trained-head release" is this field. Where an effect on trained weights is not explicit, the dataset strategy marks it unresolved and withholds a commercial-release claim. | No trained checkpoint exists. Apache-2.0 on Votelle source does not relicense training audio or a future head. |

`origin_type` is `original`, `contribution`, `generated`, `public_dataset`, or `test_fixture`. P-01 ingest writes `public_dataset` and `artist_id` `kevin-macleod`, with `source_revision` set to the ISRC. That origin label classifies the intake. It does not accept the rest of any public corpus.

## 7. Commercial-ready and research-only policies

**Verified evidence.** Decision [0001](../decisions/0001-foundation-choices.md) and `check_rights`.

| Policy | Fields that must be `allowed` | Other behavior |
|---|---|---|
| `commercial_ready` | `research_training`, `commercial_training`, `audio_release`, `embedding_release`, `checkpoint_release` | Unknown or denied on any of the five fails validate. |
| `research_only` | `research_training` | Unknown or denied research training fails. The other four fields are not required to be `allowed`. They are also not converted to `allowed`. |

A `research_only` validation report sets `provenance` to the policy name `research_only`. That is the implemented provenance label on the validation report. It is not a stamp on an embedding or a checkpoint, because this tree does not emit those artifacts. Decision 0001 says `research_only` labels artifacts with that provenance. The label this tree writes is the validation report's `provenance` field. The report string does not clear an embedding or a checkpoint, and this tree does not emit those files.

`configs/p01_piano.json` is `research_only`. The recorded P-01 snapshot has `research_training: allowed` and the release fields `unknown`. Those unknown fields are why `commercial_ready` is not available. They do not, by themselves, prove that validate would pass: this note did not run it, and `in_manifest` is not that result.

Fixture `commercial_ready` applies to generated test signals under `tests/fixtures/pilot`. It is not a template for P-01 and not a finding that Incompetech release fields are allowed.

## 8. Attribution, provenance, and the rights audit workflow

CC BY attribution, where it applies, keeps credits, license and source links, and change notices. The rights row has an `attribution` string for that text. Incompetech's FAQ is the catalog-specific guidance cited in §3. Do not describe source audio, embeddings, or a trained head as Apache-2.0 because the Votelle repository is Apache-2.0.

**Proposed method** from the dataset strategy, aligned with what ingest actually refuses to invent:

1. Write the rights row before claiming eligibility. Include rightsholder, component list, the five permissions, `review_status`, `review_rationale`, and `evidence_sha256`. Evidence is a local file, a URL, or both. The model requires at least one of path or URL.
2. For P-01 manifest eligibility, ingest ignores a URL-only row. `review_status` must be the exact string `reviewed`, and the local evidence file under the dataset root must match `evidence_sha256`. Otherwise the receipt is `provisional_review`, `in_manifest` is false, and nothing is appended to `assets.jsonl`.
3. Snapshot the track page and the rights pages the row relies on. Store the retrieval hash. Permissions stay at `unknown` until that review is finished.
4. Hash original bytes and canonical PCM. Track descendants. Preserve license snapshots and source revision ids.
5. Run `votelle-music validate --config <config>` for dataset eligibility under the chosen policy. Historical decision 0003 names this `music-pref validate`.
6. Leave `release_clearance` at `not_assessed` unless a future, explicit review writes a different decision outside the current receipt type. Today's receipt schema cannot store another value.
7. A release audit of any future checkpoint walks the full dependency graph of that checkpoint and of the output dataset. Restricted evaluation artifacts stay in a separate profile and output directory. There is no automatic mix or distillation from a restricted model into the permissive lane.

Three gates stay distinct:

| Gate | Meaning | P-01 state this note can stand behind |
|---|---|---|
| Provisional review | No usable reviewed local evidence. Asset row not appended. | The snapshot had moved past this gate for the three recordings. Not re-checked on disk. |
| Technical ingestion | Files copied, decode command stored, receipt written. Permissions unchanged. | Implemented. Audio not in Git. |
| Dataset eligibility | `votelle-music validate` under `research_only` or `commercial_ready`. | Not re-run on P-01 here. `in_manifest` is not this gate. |
| Public release authorization | All five permissions `allowed`, plus attribution and component coverage. | **Unresolved.** Receipt clearance `not_assessed`. Release fields `unknown`. |

`prepare` is a fourth, non-rights gate. It writes a float32 48 kHz mono excerpt of 480,000 samples under `gain_lufs_v1` only when level match is required. A loudness mismatch is `excluded_loudness_mismatch` and is not appended to `clips.jsonl`. A match within 0.1 LU of −20 LUFS, at or under −1 dBTP, is `primary_level_matched` and is the only prepare result that becomes a clip row. Musical suitability is not decided there. The loudness procedure is decision [0002](../decisions/0002-audition-normalization.md). An empty `briefs.jsonl` stays empty until an operator writes a brief. Brief text is not invented.

## 9. Manifests and immutable identity

**Verified evidence.** Source JSONL is append-only. Ingest creates empty manifest files if needed, then appends an asset line. It does not rewrite existing rows and does not edit `rights.jsonl`. A second ingest of the same URI, the same raw hash, or the same decoded PCM is `duplicate_id`. Existing bytes stay. A failed ingest deletes only files that attempt created. Prepared audio, diagnostics, and split membership are new artifacts.

Manifest files: `assets.jsonl`, `rights.jsonl`, `briefs.jsonl`, `clips.jsonl`, `judgments.jsonl`. Schema version `0.1`. Extra fields are rejected.

Identity edges are exact ids and hashes only. Near-duplicate audio is not detected. Generator identity is not a split edge. The same `artist_id` does not merge song families. A family merges only when a review file has `review_status` `reviewed`, a rationale, and a group of at least two catalog URIs. A later ingest that passes such a file does not rewrite rows already written. Component weight is the number of distinct song families in the component.

Edges implemented in `src/votelle_music/data/identity.py`:

| Key | Nodes joined |
|---|---|
| `source_recording_id` | Assets |
| `song_family_id` | Assets |
| `sha256_original` | Assets |
| `sha256_pcm` | Assets |
| `parent_asset_ids` | Asset and parent, when the parent is in the manifest |
| `brief_family_id` | Briefs |
| Clip's `asset_id` | Judgment and asset |
| `brief_id` | Judgment and brief |
| `is_repeat_of` | Judgment and the earlier judgment |

`source_recording_id` for P-01 is one stable id per official URI. `song_family_id` is distinct per URI unless that reviewed group exists. Connected components are not broken. Splits shuffle components with `random.Random(seed)` and assign whole components. `grouping_policy` is `component_v1`. A component heavier than the largest split fraction, fewer components than positive splits, or an empty positive split is an error. No partial split file is written. `votelle-music split` refuses to write when validate reports errors.

Canonical PCM, from decision 0001: little-endian float32 at the file's original rate and channel count, before crop or resample. A clip must be within 1 ms of 10 seconds. The loader does not pad or trim. Paths stay under the dataset root. Digital silence is a peak absolute amplitude below `1e-8`. Quieter musical material above that threshold is not rejected on that test. Fixture judgments used to build graphs are `synthetic_rule` edges, not human preference labels.

## 10. Human feedback governance, privacy, and consent

Collection order, randomization, playback logs, and musical acceptance criteria are specified in [02_P0_Dataset_and_Listening_Protocol.md](../archive/research-preconsolidation-2026-10/02_P0_Dataset_and_Listening_Protocol.md) and [02_P0_LISTENING_PROTOCOL.md](02_P0_LISTENING_PROTOCOL.md). The dataset strategy's stage sizes (P0, P1, P2) and listener-time figures are **proposed methods** and **estimates** for that study. They are not counts of judgments in this tree. The initial self-labeling design is N-of-1: it can support a claim about Justin on the declared distribution. It cannot support a population taste.

Governance constraints that bind any of those judgments:

- Each judgment stores `label_rights_record_id`. Label rights are not implied by the audio rights row.
- `label_source` distinguishes `human`, `teacher`, and `synthetic_rule`. Teacher scores and synthetic degraded pairs do not become human preference. Copying encoder rankings into labels and then scoring the encoder on those labels is circular. Neither pseudo-labels nor encoder outputs erase the source license.
- Consent, before collection, states whether public audio, anonymous votes, and trained weights are allowed, and states the limits of withdrawal after any public redistribution.
- Default publication excludes listener names, email addresses, detailed listening history, and free-text explanations. The schema can store `listener_id` and `notes`. Those fields are not a decision to publish them.
- Conflicting answers across listeners and sessions stay stored. A later aggregate does not overwrite the row.
- Restricted labels and restricted audio do not enter the permissive training lane by distillation.

No human judgments are in the recorded P-01 snapshot. An empty `judgments.jsonl` is not consent.

## 11. Restricted datasets and generator-output restrictions

**Verified as project policy in the research notes**, not as a second software allowlist. The code blocks unknown and denied permissions on rows that are actually loaded. It does not download these corpora, and it does not contain their audio.

| Resource | Terms that drive the disposition | Project rule |
|---|---|---|
| CMI-Pref and CMI-Pref-Pseudo | CC BY-NC-SA 4.0. Derivative-artifact consequences need review. | Isolated research lane. Out of default permissive training. |
| MusicPrefs | No explicit dataset license on the inspected card. | Metadata research only. A paper or another project's reuse is not permission. |
| AIME | Generated audio declared CC BY 4.0; Jamendo tracks per track; prompt tags CC BY-NC-SA 4.0. | Restricted research comparator. Text-conditioned commercial training is not cleared by the audio license alone. Rewriting tags does not create provenance. Exclude the combined corpus from the default lane. |
| SongEval | Repository CC BY-NC-SA 4.0. | Research comparator. Dataset, toolkit, and derived weights are not commercially cleared. Reconcile 2,399 songs against the 1,000-row viewer before any reproduction claim. |
| Jamendo / MTG-Jamendo | [Jamendo terms updated 17 April 2025](https://licensing.jamendo.com/en/legal/termsofuse) prohibit unauthorized commercial text and data mining, explicitly including AI. MTG-Jamendo limits dataset use to noncommercial research without authorization. Code is Apache; metadata is CC BY-NC-SA; audio is per track. | A permissive track tag does not resolve acquisition terms. Commercial use stays blocked here. Audio release is per track and is not established. No automatic embedding or checkpoint clearance. |
| MusicCaps | Annotations CC BY-SA 4.0. Music is linked through YouTube. | No wholesale audio acquisition. Trained-weight consequences unspecified. |
| MusicBench | Card CC BY-SA 3.0, derived from MusicCaps-related material. | No default commercial-ready training. Share-alike applicability unresolved. |
| LFM-2b | Withdrawn over licensing. | No permission from old mirrors. |
| Suno-origin audio | [Terms](https://www.suno.com/terms), revised 10 August 2026 and effective 3 September 2026, restrict using outputs or voice models to compete with Suno, including a competing music-generation product or service. Paid-tier assignments remain subject to the terms. [S39](../archive/research-v0.1/10_Source_Register.md). | **Excluded** from training and from a releasable benchmark unless written permission covers that use. This includes Suno audio inside another collection. The exclusion is a conservative project policy. It is not a claim that every private act of ranking music is prohibited. |
| ACE-Step 1.5 | Code [LICENSE](https://github.com/ace-step/ACE-Step-1.5/blob/main/LICENSE) is MIT. Card discusses commercial outputs. Inspected tree: DiT turbo ~4.79 GB, VAE ~0.34 GB, Qwen3-Embedding-0.6B ~1.19 GB, adapted 1.7B LM ~3.71 GB. Default packaged tensors ~10.0 GB. Upstream Qwen embedding declares Apache-2.0. No root LICENSE at the tested Hugging Face path. The card's MIT line is not a component warranty. | **Conditional. 0 local outputs.** Pin every component, keep inherited notices, and screen candidates. Generate only from original text or lyrics, without copyrighted reference audio or identity imitation. An open model license does not guarantee that no third-party right is implicated. "Under 4 GB VRAM" does not establish 8 GB unified-memory feasibility. Prefer documented contributor outputs later over local generation now. |
| HeartMuLa named checkpoint | Card cited as Apache-2.0. [S41](../archive/research-v0.1/10_Source_Register.md). | Future source only, after a component audit. HeartCLAP deployable weights are a separate unresolved item (§13). |
| YuE2 | Weight permissions distinguish creators from companies. [S33](../archive/research-v0.1/10_Source_Register.md). | Not the default commercial-ready source. |

Do not scrape public demos or acquire subscription outputs as a substitute for the grants above.

## 12. Technical limitations and remaining gates

- Ingest, validate, and release authorization are different gates. Passing one leaves the others where they were.
- The receipt cannot represent a release clearance other than `not_assessed`.
- `research_only` does not read the four release fields. A dataset can be eligible for that policy while remaining uncleared for audio, embedding, or checkpoint release.
- Sample and performer scope have no first-class fields.
- Near-duplicate audio is not linked. Two files with different hashes and different ids can split apart.
- Generator id, revision, and seed are stored on `GeneratorInfo` when present and are not identity edges.
- The core CLI refuses every encoder except `dummy` / `fixture-v1`. An isolated encoder probe does not change rights and is not a core adapter. Encoder results belong to [status](../STATUS.md) and the encoder notes, not to a clearance decision.
- `network_access: true` fails validate. The foundation does not fetch missing audio.
- P-01 `prepare` requires `gain_lufs_v1` and `level_matched` true. Loudness eligibility is not musical acceptance and not a rights grant.
- Schema `0.1`, excerpt length, grouping, rights fields, and label meaning change only with a new protocol version.
- Fixture success is a software check.

## 13. Outstanding permissions and release blockers

| Blocker | Label | Why it still blocks a release |
|---|---|---|
| P-01 `commercial_training`, `audio_release`, `embedding_release`, `checkpoint_release` | Unresolved (`unknown` on the recorded snapshot) | `commercial_ready` requires `allowed` on all five fields. |
| P-01 `release_clearance` | `not_assessed` | Ingest does not grant release. |
| P-01 validate, briefs, crops, judgments | Not established for the private tree | Empty manifests in the snapshot. No musically accepted excerpt in Git. Split must not be run. |
| Incompetech embedding and checkpoint release | Unresolved | The training offer does not expressly address them. Attribution and component coverage are still required before any release. |
| Remainder of the audit shortlist (P-02, P-03, P-04, B-reserve) | Proposed method | Not in `P01_CATALOG`. HEAD-only checks. No per-asset evidence row is claimed here. |
| First-party and contributor audio | Unresolved | 0 verified recordings, 0 contacted contributors. |
| Music Arena eligible subset | Unresolved | 1,959 included files and 8,117 battles do not state how many pairs have both audio files, fit ten seconds, and meet the release policy. |
| MusicPrefs license | Unresolved | No explicit dataset license on the inspected card. |
| SongEval coverage | Unresolved | 2,399 songs / ~140 hours versus 1,000 visible rows. |
| CMI pseudo counts | Unresolved | Card figures and the paper's ~110k pseudo samples describe different units or releases. Not every row is a valid label. |
| MusicNet / Musopen recording provenance | Unresolved | Mixed or user-upload rights. Conditional only. |
| Jamendo, MTG-Jamendo, AIME combined corpus | Restricted or blocked for the default commercial lane | Dataset-level or mixed terms. |
| Suno-origin material | Excluded absent written permission | Competition restriction in the current terms, including audio found inside another collection. |
| ACE-Step components and outputs | Unresolved; 0 outputs | MIT card is not a component warranty. |
| Apache-2.0 on this repository | Verified for source and project documentation | Does not clear recordings, annotations, embeddings, or model artifacts. |

### Unresolved contradictions

These statements are both in the tree. This note does not pick a winner and does not rewrite either source.

**Incompetech commercial training, source-level wording versus serialized fields.** The feasibility audit's matrix says, for selected Incompetech original tracks, in column order research ML, commercial ML, audio release, embedding release, and trained-head release:

> Permitted under published offer + BY grant, after review
>
> Permitted under BY grant + training offer, after review
>
> BY, within licensor’s rights
>
> BY/provenance review
>
> BY/provenance review

The same audit says: “Review” means unknown for the specific assets; it must not be serialized as allowed. And: “Public embedding/head release is not expressly addressed by the offer.”

The status note says the three P-01 receipts recorded `research_training` as `allowed`, "while commercial training, audio release, embedding release, and checkpoint release were `unknown`."

Decision 0001 says: "A license string never grants a permission."

The commercial-training cell and the instruction not to serialize "Review" as `allowed` are in tension. The asset snapshot left commercial training and the release fields unknown. Those fields stay unknown here.

**CMI pseudo-label scale.** The dataset strategy says the CMI-Pref-Pseudo card "describes ~56k generations and ~165k candidate comparisons; ~115k pseudo labels." The risk note says "the paper's ~110k pseudo samples and current card's larger round-robin count describe different units/releases. Not every row contains a valid label." Both stand. No pinned label-bearing count is adopted.

**Music Arena scale.** The audit reports 1,959 included audio files in the July 2026 release. The dataset strategy sums monthly card totals from July 2025 through July 2026 to 8,117 battles. The risk note says those monthly totals do not establish how many pairs have both audio files, fit the ten-second scope, and satisfy the release policy. The two counts are different units. Eligibility stays unresolved.

**SongEval coverage.** The dataset strategy reports the study/card figure of 2,399 songs and about 140 hours, and an inspected viewer count of 1,000 rows. The risk note states the same conflict. No reconciled pin is claimed.

### Other open license conflicts

The [risk note](../archive/research-v0.1/09_Research_Risks_and_Open_Questions.md) also leaves these unresolved. They are not dataset grants, and this note does not close them:

- TuneJury: the advertised permissive CLAP-only head does not clearly relicense the root repository's noncommercial code.
- HeartCLAP: the paper description was verified; separate deployable weights and a usable contract were not.
- MusicFM: permissive metadata is promising; the empty card body leaves provenance to the repository and the specific artifact.
- Local encoder deployment measurements remain an encoder-note question, not a rights grant.

## Sources

Primary register, cutoff 9 October 2026 Pacific, pages accessed 10 October 2026 UTC: [10 — Primary Source Register](../archive/research-v0.1/10_Source_Register.md). License statements there refer to the named artifact or page. They do not certify underlying rights. Current repository and model pages need a revision pin before implementation.

| Document | Role for this note |
|---|---|
| [01 — Data Feasibility and Rights Audit](../archive/research-preconsolidation-2026-10/01_Data_Feasibility_and_Rights_Audit.md) | Source inventory, Incompetech evidence, P-01 and wider shortlist. Evidence checked 10 October 2026 UTC / 9 October Pacific. |
| [04 — Dataset and Human Feedback Strategy](../archive/research-preconsolidation-2026-10/04_Dataset_and_Human_Feedback_Strategy.md) | Corpus dispositions, acquisition procedure, label-rights and privacy requirements. 9 October 2026. Collection method stays in the protocol notes. |
| [02 — P0 Dataset and Listening Protocol](../archive/research-preconsolidation-2026-10/02_P0_Dataset_and_Listening_Protocol.md) | Existing listening protocol. Not run. |
| [02 — P0 Listening Protocol (consolidated)](02_P0_LISTENING_PROTOCOL.md) | Consolidated procedure. Rights stay in this file. |
| [Decision 0001](../decisions/0001-foundation-choices.md) | `commercial_ready`, `research_only`, immutable JSONL, exact identity edges. |
| [Decision 0003](../decisions/0003-p01-ingestion.md) | P-01 catalog, three gates, historical `music-pref` commands. |
| [Decision 0004](../decisions/0004-votelle-naming.md) | Live names. No change to rights or protocol. |
| [Decision 0002](../decisions/0002-audition-normalization.md) | Loudness procedure. Not a rights grant. |
| [Status](../STATUS.md) | Implementation status and the P-01 intake snapshot. 10 October 2026. |
| [Project direction](../PROJECT_DIRECTION.md) | Long-term intent. Does not expand v0.1. |
| `src/votelle_music/data/rights.py`, `ingest.py`, `identity.py`, `schemas.py` | What validate, ingest, and identity actually do. |
| `configs/p01_piano.json`, `configs/foundation.json` | `research_only` pilot versus `commercial_ready` fixtures. |
