# P0 listening protocol

Votelle research protocol v0.1. Evidence date: 10 October 2026.

**Purpose.** This is the written procedure for the preliminary four-group acquisition study and the P0 listening study. A person runs it with audio files, a locked written trial order, a local player, and a listener. It separates what the software does, what the research notes propose, and what is still unresolved. No P0 session is recorded as complete.

This consolidation does not change protocol version, excerpt length, grouping, rights, or label meaning. Those changes require a new protocol version. Package version remains `0.1.0`. Schema version remains `0.1`.

## 1. How to read this protocol

| Label | Meaning in this document |
|---|---|
| Verified | Behavior in source, tests, configs, or an accepted decision, as read for this consolidation |
| Measured | A number recorded from a run in `docs/STATUS.md`. A measurement of software or of one encoder excerpt is not a listening result |
| Estimate | A planning figure the research notes already give as approximate or assumed |
| Proposed | A method in the research notes. It has not been run, and it is not by itself an accepted decision |
| Unresolved | A procedure the sources do not specify, or a disagreement they do not settle |

Authority, as stated in `docs/research/README.md`: source, tests, configs, and `uv.lock` say what the software does; `docs/decisions/` are the accepted choices; the research notes govern scientific requirements the code has not implemented. `docs/PROJECT_DIRECTION.md` states long-term intent and does not expand protocol v0.1. Passing tests are not listening results.

The live names are Votelle, package `votelle_music`, CLI `votelle-music`, and exception `VotelleError`. Decisions 0001–0003 still write the historical commands `music-pref` and the historical package `music_pref`. Decision 0004 records that split and does not change dataset semantics. Where this protocol names a command, the historical form is labeled and the current CLI is `votelle-music`.

Rights details live in [`01_DATA_GOVERNANCE.md`](01_DATA_GOVERNANCE.md). The 10 October audit is archived at [`01_Data_Feasibility_and_Rights_Audit.md`](../archive/research-preconsolidation-2026-10/01_Data_Feasibility_and_Rights_Audit.md). Hypotheses H1 and H2 live in [`04_TRAINING_AND_EVALUATION.md`](04_TRAINING_AND_EVALUATION.md). They are not restated here. Historical command names in decisions 0001–0003 are explained in [decision 0004](../decisions/0004-votelle-naming.md).

## 2. Executive summary

The preliminary study is four groups, twelve candidate recordings, twelve within-group comparisons, and two delayed repeats: **14 trials**. It does not replace P0.

P0 is **20** independent brief families, **3** candidates each, **60** unique within-family pairs, plus **10** delayed repeats. With a practice trial held outside the dataset, the scored session is 70 trials in three blocks of 20, then the 10 repeats 24–72 hours later.

Each listened excerpt is a person-selected span within 1 ms of 10 seconds. Preparation resamples that span to exactly 480,000 mono samples at 48 kHz and, for listening, applies profile `gain_lufs_v1`: one constant gain toward **-20 LUFS**, limited by a **-1 dBTP** ceiling. Acceptance is **±0.1 LU**. Profile `none_fixture_only` resamples only.

Each trial records two separate comparative answers, brief adherence and personal preference for this use, plus an acceptability judgment for each clip. A clip can match a brief without being preferred, and a preferred clip can miss the brief. The two scores stay separate.

Status on 10 October 2026: no finalized creator brief, no musically accepted 10-second crops, no human judgments. A technically prepared probe excerpt is not musical acceptance and not a listening result. The study is N-of-1. One creator does not establish a population taste.

## 3. Current evidence and implementation status

Status is taken from [`docs/STATUS.md`](../STATUS.md) as read on 10 October 2026. Private audio was not inspected. Git does not contain the P-01 audio.

| Item | State | Label |
|---|---|---|
| Protocol v0.1 listening study | Not run. `docs/research/README.md` indexes the predecessor note as "Listening protocol. Not run" | Verified as a status statement |
| Finalized creator brief | None. Decision 0003: `briefs.jsonl` stays empty until the operator writes one | Verified |
| Musically accepted 10-second crops | None in the recorded status. Fixture tones can pass preparation. A synthetic tone is a fixture | Verified |
| Human judgments | None recorded. `judgments.jsonl` may be empty. Fixture graph edges use `label_source` `synthetic_rule` | Verified |
| `gain_lufs_v1` | Implemented. Checked on fixture tones. Decision 0002 is the procedure | Verified |
| `none_fixture_only` | Resample only. `level_matched` is false. It is the fixture profile | Verified |
| P-01 ingest and prepare | Local intake for three catalog recordings. A passing ingest test is not a rights grant and not a listening result | Verified |
| Earlier P-01 snapshot in status | Receipts for Disquiet, Mesmerize, and Colorless Aura were `reviewed_with_evidence` and `in_manifest: true`. `research_training` was `allowed`. Commercial training, audio release, embedding release, and checkpoint release were `unknown`. `release_clearance` was `not_assessed`. Brief, clip, and judgment manifests were empty. That maintenance pass did not re-validate the intake | Recorded status; not re-checked here |
| Disquiet 30–40 s probe | Status records one technical excerpt, mono float32, 48 kHz, 480,000 samples, used in an isolated CPU encoder run. Musical acceptance, preference, and the 20-clip benchmark remain open | Measured encoder run; not a listening result |
| Core adapter, training, UI, generator | Not implemented | Verified |
| Foundation check named in status | `votelle-music validate` reported 0 issues on `configs/foundation.json`. `votelle-music split` on that fixture config, seed 17, assigned 12 train, 2 validation, 2 calibration, and 4 test components | Measured software check on fixtures; not a listening split |

Commands run from the repository root. A relative `dataset_root` resolves from the current working directory. Paths must stay under the dataset root.

Current commands used by this procedure:

- `votelle-music validate --config <config>`
- `votelle-music ingest` with the flags in section 9, for the three P-01 URIs only
- `votelle-music prepare --config <config> --asset-id <id> --clip-id <id> --start <seconds> --end <seconds>`

Decisions 0002 and 0003 name validate and the P-01 split prohibition with the historical command `music-pref`. Decision 0003 names the intake and excerpt steps as `ingest` and `prepare`. The current executable prefixes those steps with `votelle-music`. Do not run `votelle-music split` on the P-01 dataset. Decision 0003 states the same prohibition under the historical name `music-pref split`. The split fractions in `configs/p01_piano.json` exist because the config schema requires them. P-01 is an acquisition and listening pilot, not a training set.

## 4. Study phases

Project direction keeps full-song evaluation, reinforcement learning, encoder fine-tuning, generator integration, and recommender development outside protocol v0.1. The unit of analysis remains an explicitly selected ten-second excerpt.

| Phase | Design stated in the notes | What it is for | Relationship to the others |
|---|---|---|---|
| Preliminary acquisition | 4 groups, 12 recordings, 12 unordered comparisons, 2 delayed repeats: 14 trials | Permissions, crop QC, question wording, playback, and whether a group actually offers alternatives | Proposed. Does not replace P0. Judgments stay in a separate dataset or version |
| P0 | 20 families × 3 candidates = 60 unique pairs, plus 10 delayed repeats | Instructions, rights workflow, stability, and playback. An N-of-1 usability and repeatability study | Proposed. No train/test success claim. Data used to refine the protocol stay out of a later untouched confirmation set |
| P1 | 160 families × 4 candidates = 640 clips / 960 within-family pairs. Family allocation 96 / 16 / 16 / 32, giving pair slots 576 / 96 / 96 / 192 | Train, validate, calibrate, and test without shared-family leakage | Proposed in the feedback note. Preserve this group split and the evaluation gates. Software assigns whole connected components; it does not by itself apply this family allocation |
| Later confirmation | Fresh test set with at least 100 independent brief families. Four candidates each gives up to 600 correlated pairs | Precision and a blind recommendation study, with selection separated from judgment when feasible | Proposed. P0 and preliminary judgments are not that fresh holdout |

Listener-time figures in the notes are estimates, using 45–75 seconds per trial:

| Phase | Stated time | Label |
|---|---|---|
| Preliminary | About 11–18 minutes of active listening and labeling, plus setup | Estimate |
| P0 | 70 × 45–75 seconds = 53–88 minutes of active work. Allow 2–4 hours for orientation, replays, breaks, and record handling | Estimate |
| P1 | 12–20 hours at 45–75 seconds per pair. Repeats and QA bring the plan to about 15–25 hours | Estimate |
| Confirmation | 7.5–12.5 hours per listener before repeats. The design can sample fewer pairs per family | Estimate |

Completed P0 fields, if every trial is filled, are 140 ranking responses and 140 candidate-acceptability responses. The notes say these are not 280 independent comparisons.

The initial self-labeling study is N-of-1. The feedback note limits any claim to Justin on this distribution. It does not support a universal music-preference model. Project direction states the same boundary: one creator does not establish a population taste. A proposed external panel of five people, two hours each, at $15–25 per hour, is given as $150–250 before fees. That is an annotation planning assumption, not a market quote or an approved expense. Population claims need multiple consenting listeners and held-out listeners. Recruitment and payment are not part of running P0.

What the feedback note says a pair count can support, once families, listeners, and reliability are real:

| Human pairs | Reasonable use stated in the note | Not yet defensible, as stated in the note |
|---|---|---|
| 50 | Schema mistakes, gross artifacts, unclear targets | Neural superiority, robust calibration, broad personalization |
| 100 | Repeatability, compact features, preliminary per-user signal | Trustworthy subgroup claims or five-point improvements |
| 500 | Regularized baseline learning curves; exploratory comparison | Strong conclusions from only a few songs or briefs |
| 1,000 | More credible scoped evaluation and adaptation curves | Universal vocal, genre, language, or generator generalization |
| 10,000+ | Richer multi-user modeling and stronger subgroup studies | Immunity to bias, leakage, weak rights, or distribution shift |

Independent brief and song families, listener diversity, and label reliability matter more than the raw pair count. P0's 60 pairs plus 10 repeats sit in the coarse diagnostic range. Ten repeats are coarse diagnostic evidence only.

## 5. Preliminary four-group study

Proposed. Fourteen trials. Collect all three unordered comparisons in each group, then repeat two comparisons after 24–72 hours. Which two comparisons are repeated is unresolved.

The briefs below are the note's draft briefs. Status says there is no finalized creator brief. Do not treat the table text as a locked brief. All examples require human audition. No suitability or preference was measured when the note was written.

| Group | Draft brief in the listening note | Proposed candidates | Role stated in the note |
|---|---|---|---|
| P-01 | Restrained solo piano for a reflective nighttime scene; gentle motion, subdued emotion, no dramatic attack | Disquiet / Mesmerize / Colorless Aura | Compare plausible alternatives within instrumentation and mood |
| P-02 | Relaxed small-ensemble jazz for a quiet lounge; a light groove with an unobtrusive lead and moderate energy | Night in Venice / Lobby Time / Airport Lounge | Differences in lead instrument are allowed; none is declared a loser |
| P-03 | A bass-led funk passage with steady groove and restrained grit; rhythmic drive without harshness | RetroFuture Clean / Dirty / Nasty | Published related variants; one source or song component, not three independent songs. Confirm the chosen regions actually differ musically |
| P-04 | An orchestral waltz passage with graceful motion and moderate urgency, avoiding either a dragging or rushed feel | Grand Dark Waltz Allegro / Allegretto / Moderato | One related-composition component. Align musical position, not arbitrary equal timestamps |

P-03 and P-04 are there to diagnose subtle variant comparisons. The note says they are not sufficient evidence of broad artistic preference: tempo or texture may make them easy, and some corresponding ten-second regions may be effectively identical. If that happens, retain the finding or replace the whole group under a logged pre-label rule. Do not manufacture distortion or choose candidates to force disagreement. The log format for that pre-label rule is unresolved.

**Proposed preliminary exit**, called operational thresholds in the note, not statistical claims. Every asset has a documented applicable permission. All 12 crops pass technical QC. At least three groups offer meaningful alternatives. Question meanings are understood. No accidental source disclosure. Repeat trials work. If a group fails, resolve or replace it before scheduling P0.

Only group P-01 has an ingest catalog. Verified in decision 0003 and `votelle_music.data.ingest`: the command accepts only these official URIs, copies the MP3 unchanged, and does not download.

| Recording | ISRC | Official URI |
|---|---|---|
| Disquiet | USUAN1500036 | `https://incompetech.com/music/royalty-free/mp3-royaltyfree/Disquiet.mp3` |
| Mesmerize | USUAN1500005 | `https://incompetech.com/music/royalty-free/mp3-royaltyfree/Mesmerize.mp3` |
| Colorless Aura | USUAN1400008 | `https://incompetech.com/music/royalty-free/mp3-royaltyfree/Colorless%20Aura.mp3` |

`source_recording_id` is one stable id per official URI. `song_family_id` is distinct per URI unless a review file merges them. The stored artist id `kevin-macleod` does not merge families. A family merges only when a review file has `review_status` `reviewed`, a rationale, and a group of at least two catalog URIs. A later ingest that passes that file does not rewrite rows already written. Groups need two distinct catalog recordings. A URI in more than one group is an error. A URI outside this catalog is rejected.

P-02, P-03, and P-04 names are proposed candidates in the listening note. They are not an ingest catalog. How their files enter a manifest is unresolved. See section 13.

P-01 has four gates in decision 0003. They are different states. Ingest does not edit permissions.

| Gate | What it means |
|---|---|
| Provisional review | No rights id, a `review_status` other than `reviewed`, or a missing or hash-mismatched local evidence file. Receipt: `rights_gate: provisional_review`, `in_manifest: false`. Nothing is appended to `assets.jsonl` |
| Manifest candidate | An existing rights row is `reviewed` and its local evidence file matches `evidence_sha256`. Ingest appends an asset and does not edit `rights.jsonl`. Permissions stay as written, including `unknown`. Receipt `release_clearance` is `not_assessed` |
| Dataset eligibility | `votelle-music validate --config configs/p01_piano.json`. Policy `research_only` requires `research_training` `allowed`. Unknown fails. Historical command name: `music-pref validate` |
| Release clearance | `commercial_ready` requires `allowed` on research training, commercial training, audio release, embedding release, and checkpoint release. Ingest never sets those fields |

`in_manifest: true` means the rights row was reviewed and evidenced. It does not mean validate passed, and it does not mean the clip is cleared to publish. The permission audit itself is in the governance consolidation, not here.

## 6. P0 families, ancestry, and leakage

Proposed construction, from the listening note. Write the 20 briefs before final candidate selection. Use audible instrumentation, texture, rhythmic motion, and mood. Use five sourcing pools with four materially different briefs each: reflective piano/chamber, relaxed jazz, groove-based instrumentals, atmospheric electronics, and dramatic/acoustic scene music. These are sourcing pools. They are not, by themselves, 20 independent groups.

Restrict the first briefs to locally audible texture, instrumentation, and broad mood. The feedback note's example is "quiet piano-led nocturnal instrumental with a restrained dynamic feel." Chorus progression and lyric fidelity in a longer brief cannot be validated from an arbitrary ten-second excerpt. A vocal exploratory subset may be labeled separately. Claims about lyrics or complete arrangement stay excluded. Brief constraints must be audible in the crop that is actually heard.

For each brief, find four plausible tracks or variants using the artist's metadata, audition them, and retain three by eligibility and useful variation. All three must address the same use case. Do not compare unrelated genres, silence against music, or obviously broken audio as the primary task. Do not use CLAP scores to pick winners or to curate difficulty. The status cosine figures are encoder similarities for one technical excerpt. They are not listener preferences and they are not a selection score.

For retrieved catalog music, call the three items **brief-matched retrieval candidates**. They are not three outputs generated from the same prompt. This design can test labeling and selection. Generator-specific claims require fresh generated or contributed alternatives later. Keep the source catalog consistent within each trio. A single-artist pilot cannot demonstrate artist generalization.

Hide titles, filenames, artist identity, release date, source, and automated scores from the listener during the trial.

Do not reuse a recording, composition, alternate render, cover, or paraphrased brief across supposedly independent groups. A collection tag alone is not proof of shared composition. Shared melody or arrangement is a reason to link. Inspect the identity graph after selection. Merge linked groups and add genuinely new families until there are 20 components.

The preliminary groups may inform preparation. Keep their judgments in a separate dataset or version. Prefer 20 fresh P0 groups. If any preliminary group is reused, declare the prior exposure and do not count it as a fresh holdout.

### What the software treats as the same component

Verified in decision 0001 and `votelle_music.data.identity`. Identity edges are exact ids and hashes. Connected components are not broken. Splits shuffle components with `random.Random(seed)` and assign whole components by weight deficit. Component weight is the number of distinct song families in the component. A component heavier than the largest split fraction, fewer components than positive splits, or an empty positive split is an error. No partial split file is written.

| Edge that unions records | Verified |
|---|---|
| `source_recording_id` | Yes |
| `song_family_id` | Yes |
| `sha256_original` (file bytes) | Yes |
| `sha256_pcm` (canonical little-endian float32 at the file's original rate and channel count, before crop or resample) | Yes |
| `parent_asset_ids`, when the parent is in the manifest | Yes |
| `brief_family_id` | Yes |
| A judgment with its brief and with the assets of `clip_a_id` and `clip_b_id` | Yes |
| `is_repeat_of` between judgments | Yes |
| `artist_id` | No. The same artist id does not merge P-01 families, and the component builder does not union on artist id |
| Generator identity | No. Not a main-split edge |
| Near-duplicate audio, shared melody, cover, or paraphrased brief | Not detected. Decision 0001 limits edges to exact ids and hashes |

A human decision to link melody, arrangement, cover, or paraphrased brief changes the graph only when the operator writes one of the edges above. For P-01 song families, the review-file rule in section 5 is the implemented merge. Assigning the same artist id does not do it.

Canonical PCM and `sha256_original` are defined in decision 0001. `sha256_original` is the file bytes.

## 7. Ten-second excerpts and audition level

Two different acts are required. The operator selects the musical region. The loader checks the span and prepares it. The loader does not pad, trim, or choose the crop.

### Selection

Proposed, and required before prepare. Select a stable, musically representative ten-second region. Record an explicit source start time and the reason for the crop. Avoid intros and fade-outs unless all alternatives and the brief call for them. For variants, use comparable musical position. Do not time-stretch to align them. The musical reason is not a field on `Clip` or on the P-01 QC sidecar. Where that prose is stored is unresolved. Until that is settled, keep a written crop log beside the dataset and cite it from the session record.

Preserve the original. Reject corrupt, non-finite, empty, or silent input. Quieter musical material whose peak absolute amplitude is at or above `1e-8` is not rejected as digital silence.

### Preparation order

Verified. Decision 0002 is the normalization procedure. This section is the listening-facing summary. The preprocessing document, feature-cache key, and encoder-adapter constraints stay in that decision. Historical validate wording in the decision says `music-pref validate`. The current command is `votelle-music validate`.

1. Decode WAV or FLAC to float64. Other suffixes, including MP3, are rejected as the manifest asset.
2. Require a caller-selected span of 10 seconds ± 1 ms (`DURATION_TOLERANCE` 0.001). Error code `duration_not_ten_seconds`. Do not pad or trim.
3. Reject non-finite samples and digital silence on the multi-channel crop. Digital silence is peak absolute amplitude below `1e-8`.
4. Downmix with an equal mean (`equal_mean/phase_ratio_0.01/v1`). Reject the crop when the mono result is digital silence while a channel is not, or when mono mean-square is below 1% of the channel mean-square. This is not an ITU surround fold-down. Stereo preference is outside this pilot.
5. Resample with `scipy.signal.resample` to exactly 480,000 mono samples at 48 kHz (`scipy.signal.resample/fft/v1`).
6. For `gain_lufs_v1` only, measure that derivative, apply one constant gain, and remeasure. The original file is not opened for writing.

Listening samples and the future encoder buffer are the same excerpt. `waveform_for_encoder` returns a contiguous float32 copy of shape `(480000,)`.

### Loudness profile

Verified in decision 0002. Listening uses `gain_lufs_v1` with `level_matched: true`. `none_fixture_only` applies no loudness gain and requires `level_matched: false`. A config that breaks that pairing fails validation (`normalization_profile_rejected`).

| Rule | Value |
|---|---|
| Target integrated loudness | -20 LUFS |
| True-peak ceiling | -1 dBTP |
| Applied gain | One constant linear gain: the smaller of the loudness gain and the ceiling gain |
| Processing that is not used | Compressor, limiter, fade, sample-by-sample nonlinearity |
| Extra scale | A second constant scale only when float error puts the remeasured true peak over the ceiling |
| Iteration | None. If absolute-gate membership changes after the gain, a dynamic excerpt can miss ±0.1 LU and is flagged |
| Acceptance | ±0.1 LU, the EBU Tech 3341 minimum requirement for integrated loudness, as cited by decision 0002 |
| Meter status | This tree is not an EBU-certified meter |
| Loudness method | ITU-R BS.1770-4 K-weighting at 48 kHz (`itu-r-bs.1770-4/k-weight/48kHz/v1`): 400 ms blocks, 75% overlap, absolute gate -70 LUFS, relative gate -10 LU, channel weight 1.0 for mono and for each of stereo left and right. Shelf and high-pass constants are the De Man form of the BS.1770-4 biquads. Filters start at rest on the excerpt. There is no pre-roll |
| Absolute-gate fallback | If every block is below the absolute gate, the gain uses ungated block power (`ungated_block_power_v1`). The value stored after gain is the gated remeasurement. Gated and ungated results are not both stored as the audition loudness |
| True peak | 4× `scipy.signal.resample_poly`, default Kaiser-5 window, `padtype="line"` (`scipy.signal.resample_poly/4x/kaiser5/line-pad/v1`). This is not the BS.1770 Annex 2 FIR table |
| `loudness_mismatch` | Set when the remeasured gated loudness is non-finite or farther than 0.1 LU from -20 |
| `gain_limited_by` | `true_peak` when the ceiling, rather than the loudness target, selected the gain. The implementation also records `loudness` when the loudness target selected the gain, and `not_applicable` when no gain profile ran |

The listening note forbids silently using FFmpeg dynamic loudness normalization, compression, limiting, fades, silence padding, or automatic crop selection. `gain_lufs_v1` is the constant-gain procedure above. The operator's decode tool is whatever command is recorded at ingest. Ingest stores that command and does not run it.

`loudness_mismatch` excludes the clip from the primary level-matched analysis. Decision 0002 also allows keeping it in a separately identified condition. The two implemented commands do not do the same thing. The quotes are in section 13. For a listening session, a primary level-matched trial uses a clip that matched. A mismatched clip is not silently substituted into that analysis.

P-01 `prepare` calls `prepare_excerpt` with `gain_lufs_v1`. It writes a float32 WAV at `prepared/<clip_id>.wav` and a QC sidecar at `qc/<clip_id>.json`. Musical suitability is not decided there. Staged assets are refused.

| QC eligibility | When | Clip row |
|---|---|---|
| `primary_level_matched` | Within 0.1 LU of -20 and at or under -1 dBTP | Appended to `clips.jsonl`. `audition_condition` is the profile name |
| `excluded_loudness_mismatch` | Outside 0.1 LU of -20 after one constant gain | WAV and sidecar are written. The row is not appended to `clips.jsonl` |

The sidecar stores asset id, clip id, start, end, preprocessing id and SHA-256, prepared PCM SHA-256, `gain_db`, integrated LUFS, true peak, the mismatch flag, eligibility, eligibility reason, and the prepared path. It does not store `gain_limited_by` or the downmix ratio. Those exist on the in-memory diagnostics during prepare.

On `votelle-music validate`, a clip row that is already present and then mismatches produces a warning. The warning does not fail the dataset. The clip row is not rewritten. The warning text for `gain_limited_by` `true_peak` says to exclude the clip from the primary level-matched analysis or keep it in a separately identified condition. The other mismatch warning says to exclude it from the primary level-matched analysis. How a separately identified condition is stored, beyond that warning, is unresolved.

### Source format

The listening note says MP3 is acceptable for this pilot, with bitrate and sample rate recorded, and without a lossless-provenance claim. Decision 0002 rejects MP3 as a decode input. Decision 0003 and ingest keep the official MP3 as the unmodified raw original and require a separate WAV or FLAC as the manifest asset. `lossless_master` on the P-01 receipt is false. The quotes are in section 13. The executable rule from source and decision 0003: leave the MP3 unchanged, decode it to a new WAV or FLAC, record the decode tool, version, and command, and do not claim lossless provenance. Bitrate of the raw MP3 is not a field named in the receipt model. Recording it is a note requirement whose field is unresolved.

## 8. What the listener judges

Proposed question wording from the listening note. Stored tokens below are the schema literals in `votelle_music.schemas`. The feedback note writes "cannot judge" as two words. The stored token is `cannot_judge`.

Brief adherence and personal preference are separate. Acceptability is separate again. One candidate can win a comparison while both fail acceptability. "Both unacceptable" is not a preference tie. `cannot_judge` is not a weak vote for A or B. A missing answer is not `cannot_judge`. Conflicting answers across sessions stay as recorded. They are not overwritten with a supposed objective truth.

| Question asked | Allowed answers | Schema field |
|---|---|---|
| Which candidate better adheres to this brief? | `A` / `B` / `tie` / `cannot_judge` | `adherence_choice` |
| Which candidate do you personally prefer for this use? | `A` / `B` / `tie` / `cannot_judge` | `preference_choice` |
| Is A acceptable for this brief and use? | `yes` / `no` / `unsure` | `acceptable_a` |
| Is B acceptable for this brief and use? | `yes` / `no` / `unsure` | `acceptable_b` |

Optional, as stated in the notes: confidence, and a reason code. The listening note says one reason code. The feedback note lists short reason codes: instrumentation, mood, delivery, artifacts, other. It also says not to require an essay. Reasons help error analysis. They are not automatically reliable labels for instruments or emotion. The schema fields are `confidence` (`float` or null) and `reason_codes` (a list of strings), with no scale and no closed vocabulary. `notes` may hold a string. The confidence scale, whether one code or several are allowed, and whether those five words are closed, are unresolved.

The listener's "A" is the alias on the trial sheet. The schema stores `clip_a_id`, `clip_b_id`, and `presentation_order` of `AB` or `BA`. `orient_judgment` flips adherence, preference, and acceptability when `clip_a_id` is not the lexicographically first of the two clip ids. It does not consult `presentation_order` when it flips. The notes say to canonicalize to clip identity before comparing a repeat with its original. They do not say whether an answer of `A` means `clip_a_id` or the alias shown first. That mapping is unresolved and has to be fixed in writing before the first real trial. Do not infer it from the function name.

`label_source` for this study is `human`. `teacher` and `synthetic_rule` are different sources. Fixture judgments are `synthetic_rule`. Copying CLAP rankings into labels, and then scoring CLAP against those labels, is circular. Teacher scores, if used later, stay `teacher` and are weighted separately. They are not this listening record. Synthetic degraded pairs can test clipping or artifact sensitivity. They do not establish artistic preference.

## 9. Session procedure

No listening application is specified. The listening note allows a later offline trial presenter and says it is not a prerequisite. This protocol does not define one. The session is a local audio player, coded files, a written order, and a listener.

### Before the first trial

1. Finish brief text, candidate selection, and the ancestry check in sections 5 and 6. Hide titles, filenames, artist, release date, source, and scores on every listener-facing sheet.
2. For P-01 only, files must already be on disk. Ingest does not download. Decode the official MP3 to a different WAV or FLAC. Then run `votelle-music ingest --config configs/p01_piano.json --source-uri <official URI> --raw <mp3> --decoded <wav-or-flac> --acquired-at <timestamp> --decode-tool <name> --decode-version <version> --decode-command <command>`. Add `--rights-record-id` and `--family-review` only when those records already exist. The decode command is stored and is not executed.
3. Choose start and end by ear. The span must be within 1 ms of 10 seconds. Write the crop reason in the crop log.
4. Run `votelle-music prepare` with `--config`, `--asset-id`, `--clip-id`, `--start`, and `--end`. Read the QC sidecar. Use `primary_level_matched` clips in the primary analysis.
5. Run `votelle-music validate` on the dataset config. Errors block eligibility. A `loudness_mismatch` warning does not, and it still keeps that clip out of the primary level-matched analysis.
6. Do not run `votelle-music split` on P-01.
7. Draw the trial order, the A/B alias for each trial, and the question order for each trial before anyone looks at votes. Lock that written order. The random-draw algorithm and seed are unresolved. The fixture split seed is not a listening-order seed.
8. Keep the alias-to-clip-id key in a file the listener does not open during the trial. The file format is unresolved. Coded playback files are the files the listener opens.
9. If the person who selected the clips is also the listener, log that exposure. Use coded files, a delay, and the randomized presentation. This is partial blinding. It is not a claim that the curator cannot recognize the music. The length of the delay before the first judgment, as distinct from the 24–72 hour repeat delay, is unresolved.
10. Run one practice trial outside the dataset. Its content is unresolved beyond that exclusion. Do not enter it in `judgments.jsonl`.
11. Record equipment and settings once per session: the same headphones, a comfortable fixed playback volume, a quiet setting, and no EQ or spatial-audio enhancement. The archive field for that note is unresolved.

Cache extraction may precede judgments. Feature availability is not permission to tune against those judgments. No model score is shown to the listener.

### During a block

Read the brief. Listen to all of A and all of B at least once. Replay if needed. Then record the four answers. Do not show prior votes.

P0 is three blocks of 20 trials, then the 10 repeats. Break after 15–20 trials. Whether the three blocks are one sitting or separate calendar days is unresolved beyond that break rule and the later repeat window.

Each trial gets its own randomized A/B aliases. Question order is randomized per trial and kept the same on that trial's repeat.

### Repeats

Sample the repeat list before examining votes. Cover 10 distinct P0 families. Reverse the A/B display on five and preserve it on five. Run them 24–72 hours after their originals. Which of the three pairs inside a family is the repeated pair is unresolved. Canonicalize displayed answers to clip identity before comparing a repeat with its original, using the mapping fixed in section 8.

The preliminary study repeats two comparisons on the same 24–72 hour window. Which two is unresolved.

### Transcription

After the session, transcribe listener answers into `judgments.jsonl`. Schema version `0.1`. Required fields include `judgment_id`, `pair_id`, `session_id`, `brief_id`, `clip_a_id`, `clip_b_id`, `listener_id`, `timestamp`, `presentation_order`, `label_source` (`human`), and `label_rights_record_id`. Choice and acceptability fields may be null in the schema. A null choice is a missing answer. Do not convert it to `cannot_judge`.

`pair_id` in the software's `canonical_pair_id` is the two clip ids sorted and joined with `::`. Use that form when transcribing so a repeat refers to the same pair. `is_repeat_of` stores the original `judgment_id`.

`listened_seconds_a` and `listened_seconds_b` stay null when duration was not measured. Manual playback confirmation is self-report. There is no instrumented player in this tree.

The listening note's storage list is judgment, pair, brief, clip, listener, and session ids; timestamp; display mapping; choices; acceptability; listening evidence; repeat link; human label source; and label consent. The schema covers that list except the private display-key file, the question order, the equipment note, and the crop-reason log. Those four stay on the written sheets until a field exists for them.

Do not publish listener names, emails, detailed listening history, or free-text explanations by default. Consent, withdrawal, and the five permission flags are specified in the governance consolidation and in decision 0001.

## 10. Repeatability, pause, and exclusion

Report adherence and preference separately. For each target report exact agreement including ties, strict-choice reversals, tie-to-strict changes, `cannot_judge` rates, and the denominators. Report acceptability consistency separately. Ten repeats give coarse diagnostic evidence only.

**Proposed pause trigger.** Three or more strict reversals among evaluable repeat pairs on either target, or a `cannot_judge` rate above 20% on that target, prompts a review of instructions, crops, and fatigue before scaling. Do not delete disagreements to pass. Retest revised instructions under a new protocol version. Do not claim reliability from this heuristic alone. Which repeat pairs count as evaluable is unresolved. The `cannot_judge` rate is stated separately from the reversal count.

The feedback note also says to repeat 10–15% of development comparisons in a later session. P0's locked count, in both that note's stage table and the listening note, is 10 repeats of 60 unique pairs. Those two sentences are not reconciled in section 13. This protocol keeps 10 repeats.

| Outcome | Primary level-matched listening use |
|---|---|
| Span within 1 ms of 10 seconds, finite, not digital silence, downmix accepted, `gain_lufs_v1` within ±0.1 LU and at or under -1 dBTP | Eligible for the primary analysis once rights and brief gates pass |
| `loudness_mismatch`, including a ceiling that prevents the loudness target | Out of the primary level-matched analysis. P-01 prepare does not append it to `clips.jsonl` |
| Digital silence, non-finite samples, bad duration, failed downmix, MP3 used as the manifest asset | Rejected by prepare or by the loader |
| Unrelated genres, silence against music, or obviously broken audio used as the primary task | Excluded by the protocol. Do not use them as the P0 comparison |
| Variant regions that are effectively identical | Retain the finding or replace the whole group under the logged pre-label rule. Do not invent a difference |
| Missing answer | Missing. It is not `cannot_judge` |
| `cannot_judge`, `tie`, both unacceptable, adherence disagreeing with preference | Valid recorded outcomes. They are not cleaned into a forced winner |
| `label_source` `synthetic_rule` or `teacher` | Not a human listening judgment |
| Model score shown to the listener, or CLAP used to pick the winners | The trial does not meet the blinding rule. P0 readiness fails for that exposure |
| Unknown or denied `research_training` under `research_only` | Validate fails. The asset is not dataset-eligible |
| Provisional-review audio | Not in `assets.jsonl`. Prepare refuses staged assets |

Disagreements are kept and later described by listener, brief, and time. The notes prefer narrowing scope or collecting better context over forcing consistency. Listeners are not removed for disagreeing with a majority. That rule has no multi-listener P0 sample yet. It is the rule if more listeners are added.

## 11. Reporting

A session report is a file written by the operator. There is no report schema in the listening notes. The minimum that makes the session reconstructable:

| Report item | Source of the requirement |
|---|---|
| Protocol version 0.1 and the evidence date of the procedure used | This document |
| Dataset root, config path, and the validate output for that session | Decision 0001 and the CLI |
| Listener id, session ids, block boundaries, and the equipment note | Listening note |
| Locked trial order, including practice-trial exclusion, repeat links, which five displays were reversed, and question order | Listening note. Draw method unresolved |
| Alias key, stored apart from the listener-facing sheets | Listening note. Format unresolved |
| Crop log: source start, end, and musical reason | Listening note. Schema field unresolved |
| Curator-exposure log when selector and listener are the same person | Listening note. Format unresolved |
| Counts, with denominators, for adherence agreement, preference agreement, acceptability consistency, strict reversals, tie-to-strict changes, and `cannot_judge` | Listening note |
| Clips excluded for `loudness_mismatch`, failed QC, or rights | Decisions 0002 and 0003 |
| Statement that no model score was shown | P0 readiness in the listening note |
| Statement of what the result is allowed to mean: N-of-1 repeatability on this material | Feedback note and project direction |

Do not describe fixture validation, ingest tests, or the single-clip encoder run as preference evidence. Do not describe a `primary_level_matched` sidecar as musical acceptance.

P0 readiness, from the listening note, before the first scored trial: 60 valid crops, 20 independent components, cleared brief, audio, and label permissions, a locked trial order and repeat list, working playback, and no model scores shown to the listener. The preliminary exit in section 5 comes before P0 is scheduled. P0 adds no train/test success claim.

Active selection of queries, including uncertainty sampling, belongs to later training work. The feedback note says never to actively select the locked test set. That rule is not a license to reshape P0 after seeing votes. Training gates stay in the training plan.

## 12. Limits of this protocol

- The study has not been run. Draft briefs are not a finalized creator brief. A prepared probe WAV is not a musically accepted crop.
- N-of-1 judgments speak to the named listener on the clips that were heard. They do not establish a population taste, a generator comparison, or a full-song preference.
- Ten repeats are a coarse check. The pause rule is a proposed heuristic.
- The loudness implementation is not an EBU-certified meter. True peak uses the Kaiser resample stated in decision 0002, not the BS.1770 Annex 2 FIR table. A clip can miss ±0.1 LU after one gain when the absolute gate changes, and it is then flagged rather than iterated.
- Near-duplicate audio is not detected. Shared melody is a human link, and it enters the graph only through an exact id or hash edge.
- The same artist id does not merge families.
- Partial blinding does not make the music unrecognizable to the person who chose it.
- P-01 prepare will not create a "separately identified condition" row inside `clips.jsonl` for a mismatch. Validate will not delete a mismatched row that is already there.
- Ingest covers three URIs. The rest of the preliminary list and the 20 P0 families have no catalog command.
- This tree implements no listening user interface, no generator, and no trained ranker.
- Apache-2.0 on the source tree does not clear recordings, annotations, embeddings, or model artifacts. A permission declaration is not legal clearance. Release permissions recorded for the earlier P-01 snapshot were `unknown`, so `commercial_ready` was not available.

## 13. Unresolved items

These are left open. They are not filled in by this consolidation.

**MP3.** The listening note says: "MP3 is acceptable for this pilot, but record bitrate/sample rate and do not claim lossless provenance." Decision 0002 says: "Decode WAV or FLAC to float64. Reject other suffixes, including MP3." Decision 0003 says the MP3 is the raw original, is not an `assets.jsonl` row, and `lossless_master` is false. Ingest says: "The raw original for this pilot is the MP3 from the official URI" and "Refusing to treat an MP3 as WAV or FLAC." Section 7 follows source and decision 0003 for what the command accepts. The note's lossless-provenance prohibition still applies. Where raw bitrate is stored is unresolved.

**Loudness mismatch.** Decision 0002 says: "`music-pref validate` records that as a warning and does not fail the dataset. The clip row is not rewritten. Exclude the clip from the primary level-matched analysis, or keep it in a separately identified condition." Decision 0003 says: "A loudness mismatch is `excluded_loudness_mismatch` and is not appended to `clips.jsonl`. A match within 0.1 LU of -20, at or under -1 dBTP, is `primary_level_matched` and is the only result that becomes a clip row." Validate's true-peak warning repeats the exclude-or-separate sentence. Its other mismatch warning says only to exclude the clip from the primary analysis. The sidecar's mismatch reason does not record whether the ceiling selected the gain. A storage form for the separately identified condition is unresolved.

**Playback.** The feedback note says "log playback completion." The listening note says: "Manual playback confirmation is self-report, not instrumented listening duration—leave unmeasured seconds null." The schema has nullable `listened_seconds_a` and `listened_seconds_b` and no completion flag. Leave seconds null unless the listener self-reports a duration. An instrumented completion procedure is unresolved.

**Repeat rate.** The P0 design in the listening note and in the feedback note's stage table is 10 repeats of 60 unique pairs. The feedback note also says: "Repeat 10–15% of development comparisons in a later session." Ten of 60 is above 15%. This protocol does not change the count of 10. Which sentence governs later development stages is unresolved.

**Answer token versus display alias.** `orient_judgment` flips choices from sorted clip ids. `presentation_order` is stored and is not an input to that flip. The notes require randomized aliases and canonicalization to clip identity. They do not define which stored clip is display A. Unresolved until written down before the first trial.

**Other missing procedures.** Confidence scale. One reason code versus the five-word list versus `reason_codes` as an open list. Question-order field. Equipment-note field. Crop-reason field. Curator-exposure log format. Private alias-key format. Listening-order random seed. Which two preliminary comparisons are repeated. Which pair inside a three-candidate family is the P0 repeat. Which repeat pairs are "evaluable." Length of the curator delay before the first judgment. Whether the three blocks of 20 are separate days. Practice-trial content. Pre-label replacement log format. Manifest intake for any recording outside the three P-01 URIs. Bitrate field for the raw MP3.

## 14. Sources

| Source | What this protocol took from it |
|---|---|
| `docs/archive/research-preconsolidation-2026-10/02_P0_Dataset_and_Listening_Protocol.md` | Preliminary 14-trial design, P0 20×3 design, crop and session procedure, question table, repeat and pause rules, readiness. Dated 9 October 2026 in that file. Left in place |
| `docs/archive/research-preconsolidation-2026-10/04_Dataset_and_Human_Feedback_Strategy.md` | Label meanings, acceptability, stage sizes, N-of-1 claim limit, pair-count table, reason-code list. Rights inventory in that file is not copied |
| `docs/decisions/0001-foundation-choices.md` | Excerpt tolerance, loader behavior, identity edges, split rule, `synthetic_rule` |
| `docs/decisions/0002-audition-normalization.md` | `gain_lufs_v1`, -20 LUFS, -1 dBTP, ±0.1 LU, loudness and true-peak methods |
| `docs/decisions/0003-p01-ingestion.md` | P-01 catalog, gates, prepare eligibility, split prohibition |
| `docs/decisions/0004-votelle-naming.md` | Votelle, `votelle_music`, `votelle-music`, `VotelleError`; historical `music-pref` left in place |
| `docs/STATUS.md` | Not-run status, probe-versus-acceptance boundary, fixture check. Main checkout text of 10 October 2026 |
| `docs/PROJECT_DIRECTION.md` | Separate adherence and preference scores; N-of-1 boundary; phase boundary with H1/H2. Study scope only |
| `docs/archive/research-preconsolidation-2026-10/05_Training_and_Evaluation_Research_Plan.md` | Named as the home of H1/H2. Not summarized here |
| `docs/research/01_DATA_GOVERNANCE.md` | Assigned home for the rights audit. Not written here |
| `src/votelle_music/schemas.py`, `data/identity.py`, `data/ingest.py`, `data/manifest.py`, `audio/prepare.py`, `cli.py` | Field names, edges, catalog limit, QC eligibility, CLI flags |

Navigation still points at the predecessor filenames. This file does not edit `docs/research/README.md`, `docs/PROJECT_DIRECTION.md`, `docs/STATUS.md`, or the predecessor notes.
