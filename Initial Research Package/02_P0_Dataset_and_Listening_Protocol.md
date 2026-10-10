# 02 — P0 Dataset & Listening Protocol

Music Preference Model v0.1 · Proposed protocol clarification · October 9, 2026 Pacific

**Preserve P0: 20 independent creative-brief families × 3 candidates = 60 clips and 60 unique within-family comparisons, plus 10 delayed repeats.** Ten-second excerpts and separate label meanings remain unchanged. This is an N-of-1 usability/repeatability study, not evidence of neural superiority or calibrated probabilities.

The acquisition route is newly proposed; it does not modify the established evaluation policy. All examples below require human audition. No suitability or preference was measured in this session.

## Small preliminary acquisition test

Use four groups from document 01, totaling 12 candidate recordings. Collect all three unordered comparisons per group, then repeat two comparisons after 24–72 hours: **14 trials**, approximately 11–18 minutes of active listening/labeling, plus setup. This preliminary test does not replace the 20-family P0.

| Group | Draft original creative brief | Proposed candidates and purpose |
|---|---|---|
| P-01 | Restrained solo piano for a reflective nighttime scene; gentle motion, subdued emotion, no dramatic attack. | Disquiet / Mesmerize / Colorless Aura. Compare plausible alternatives within instrumentation and mood. |
| P-02 | Relaxed small-ensemble jazz for a quiet lounge; a light groove with an unobtrusive lead and moderate energy. | Night in Venice / Lobby Time / Airport Lounge. Differences in lead instrument are allowed; none is declared a loser. |
| P-03 | A bass-led funk passage with steady groove and restrained grit; rhythmic drive without harshness. | RetroFuture Clean / Dirty / Nasty. Published related variants; one source/song component, not three independent songs. Confirm the chosen regions actually differ musically. |
| P-04 | An orchestral waltz passage with graceful motion and moderate urgency, avoiding either a dragging or rushed feel. | Grand Dark Waltz Allegro / Allegretto / Moderato. One related-composition component. Align musical position, not arbitrary equal timestamps. |

The last two groups intentionally diagnose subtle variant comparisons. They are not sufficient evidence of broad artistic preference: tempo/texture may make them easy, and some corresponding ten-second regions may be effectively identical. Retain that finding or replace the whole group under a logged pre-label rule; do not manufacture distortion or choose candidates to force disagreement.

**Preliminary exit:** every asset has a documented applicable permission; all 12 crops pass technical QC; at least three groups offer meaningful alternatives; question meanings are understood; no accidental source disclosure; repeat trials work. If a group fails, resolve or replace it before scheduling P0. These are proposed operational thresholds, not statistical claims.

## How to construct the full P0

1. Write 20 distinct briefs before final candidate selection, using audible instrumentation, texture, rhythmic motion and mood. Use five broad pools with four materially different briefs each: reflective piano/chamber, relaxed jazz, groove-based instrumentals, atmospheric electronics, and dramatic/acoustic scene music. These are sourcing pools, not assertions of 20 independent groups.
2. Find 4 plausible tracks/variants per brief using the artist’s metadata; audition and retain 3 by eligibility and useful variation. All must address the same use case. Do not compare unrelated genres, silence against music, or obviously broken audio as the primary task. Do not use CLAP scores to pick winners or curate test difficulty.
3. For retrieved catalog music, call these **brief-matched retrieval candidates**, not three outputs generated from the same prompt. This can validate labeling and selection; generator-specific claims require fresh generated/contributed alternatives later.
4. Keep the source catalog consistent within each trio. Hide titles, filenames, artist identity, release date, source, and automated scores. Within-source matching reduces source-quality shortcuts. A single-artist pilot cannot demonstrate artist generalization.
5. Do not reuse a recording, composition, alternate render, cover or paraphrased brief across supposedly independent groups. Inspect the identity graph after selection. Merge linked groups and add genuinely new families until there are 20 components. A collection tag alone is not proof of shared composition; shared melody/arrangement is a reason to link.
6. Curator exposure must be logged when the sole listener also selects clips. Use coded files, a delay, randomized presentation, and keep this data developmental. That is partial blinding, not a claim that the curator cannot recognize the music. A later confirmation study should separate selection from judgment when feasible.

The preliminary four groups may inform P0 preparation, but keep their judgments in a separate dataset/version. Prefer 20 fresh P0 groups; if reusing any, declare prior exposure and do not count them as a fresh holdout. P0 data used to refine the protocol stays out of a later untouched confirmation set.

## Ten-second candidate preparation

- Preserve the original. Decode and measure source properties; reject corrupt, nonfinite, empty or silent input. MP3 is acceptable for this pilot, but record bitrate/sample rate and do not claim lossless provenance.
- Select a stable, musically representative ten-second region with an explicit source start time. Avoid intros/fade-outs unless all alternatives and the brief call for them. For variants, use comparable musical position; do not time-stretch to align them. Log reasons for each crop.
- Fix channel handling and resampling before audition normalization: for this probe use the same 48 kHz mono derivative for listening and CLAP, with exactly 480,000 samples. Check phase cancellation on downmix and reject/log failures. This specifies the order left implicit in the original package; stereo preference remains outside this pilot’s scope.
- Apply the established **gain-only -20 LUFS target, -1 dBTP ceiling**. Measure both on the prepared derivative, apply the smaller safe gain, then remeasure. If the ceiling prevents level matching, flag and exclude from the primary matched analysis or keep in a separately identified condition. Never silently use FFmpeg’s dynamic loudness normalization, compression, limiting, fades, silence padding or automatic crop selection.
- Embed exactly what was heard. Record crop bounds, measured source diagnostics, channel/resampler versions, gain, final LUFS/true peak, waveform hash and preprocessing hash. Brief constraints must be audible in this crop; omit whole-song structure and lyric-correctness claims.

This follows original research documents 04–06. The encoder’s [published processor](https://huggingface.co/laion/larger_clap_music/blob/a0b4534a14f58e20944452dff00a22a06ce629d1/preprocessor_config.json) establishes the 48 kHz/10-second contract; the exact audition procedure is our protocol, not a requirement imposed by CLAP.

## One-musician collection method

Use a local audio player and a plain response table initially; no new app is necessary. A small offline trial presenter may follow once Cursor’s foundation works, but is not a prerequisite. Keep the mapping key private and give each trial independently randomized A/B aliases. Randomize question order by trial, preserving the same order on its repeat. Do not expose prior votes.

1. Use the same headphones, comfortable fixed playback volume, quiet setting, and no EQ/spatial-audio enhancements. Record equipment/settings once per session.
2. Read the brief, listen to all of A and B at least once, replay if needed, then record:

| Question | Allowed answers |
|---|---|
| Which candidate better adheres to this brief? | A / B / tie / cannot_judge |
| Which candidate do you personally prefer **for this use**? | A / B / tie / cannot_judge |
| Is A acceptable for this brief/use? | yes / no / unsure |
| Is B acceptable for this brief/use? | yes / no / unsure |

3. Optionally add confidence and one reason code. Both-unacceptable is not a tie; preference can conflict with adherence. Cannot-judge is not a weak vote. Missing is not cannot-judge.
4. Break after 15–20 trials. Schedule P0 as three 20-trial blocks, then 10 repeats 24–72 hours after their originals, with a practice trial outside the dataset.
5. Store judgment, pair, brief, clip, listener and session IDs; timestamp; display mapping; choices; acceptability; listening evidence; repeat link; human label source and label consent. Manual playback confirmation is self-report, not instrumented listening duration—leave unmeasured seconds null.

For 70 P0 trials, the package’s 45–75 seconds/trial estimate gives **53–88 minutes active work**; allow 2–4 hours for orientation, replays, breaks and record handling. There are 140 ranking responses and 140 candidate acceptability responses if all fields are completed; these are not 280 independent comparisons. Audio sourcing/preparation is additional.

## Repeatability and readiness

Sample repeats before examining votes, covering 10 distinct P0 families; reverse A/B in five and preserve it in five. Canonicalize to clip identity before comparison. Report adherence and preference separately: exact agreement including ties, strict-choice reversals, tie↔strict changes, cannot-judge rates and denominators. Report acceptability consistency separately. Ten repeats give coarse diagnostic evidence only.

**Proposed pause trigger:** ≥3 strict reversals among evaluable repeat pairs on either target, or >20% cannot-judge on that target, prompts a review of instructions, crops and fatigue before scaling. Never delete disagreements to pass. Retest revised instructions with a new protocol version; do not claim reliability from this heuristic alone.

P0 readiness requires 60 valid crops, 20 independent components, cleared brief/audio/label permissions, locked trial order and repeats, working playback, and no model scores shown to the listener. Preserve the original P1 group split and evaluation/calibration gates; P0 has no new train/test success claim. Cache extraction may precede judgments, but feature availability is not permission to tune against those judgments.
