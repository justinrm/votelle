# 04 — Dataset and Human Feedback Strategy

Research v0.1 · October 9, 2026 · Authority for data acquisition and rights policy

## Recommended data route

Use **original or explicitly contributed recordings, original briefs, and first-party human judgments** as the main releasable experiment. Optionally add generated candidates from an audited permissive local model. Treat public research datasets as separate resources with separate approval scopes. A file being downloadable, a service assigning output rights, and a dataset permitting commercial training are three different questions.

The license findings below describe published terms; they do not certify every upstream right or decide whether a particular learned checkpoint is a derivative work. Where an effect on trained weights is not explicit, mark it unresolved and withhold a commercial-release claim. Unknown permission is a blocked state in the acquisition manifest, not a guessed “yes.”

## Dataset inventory: content, labels and fitness

Sizes refer to the cited release or publication; actual eligible unique pairs will be smaller after missing-audio, scope, deduplication and rights filters.

| Dataset | Size / duration | Audio and labels | What it can supervise |
|---|---|---|---|
| Music Arena | Monthly card totals July 2025–July 2026 sum to **8,117 battles**; duration not established | Released audio plus some null entries; prompt, A/B/tie/both-bad, pseudonymous user, listening metadata | Overall contextual preference; not automatically separate adherence |
| CMI-Pref | **4,027 votes**, 3,527 train / 500 test; card reports **133.80 hours** | Generated and reference MP3 assets; musicality, alignment and confidence; multiple votes may concern one pair | Best public task match for multimodal adherence research; user histories may be sparse |
| CMI-Pref-Pseudo | Card describes ~56k generations and ~165k candidate comparisons; ~115k pseudo labels | Audio archives; teacher musicality/alignment scores; round-robin includes unvoted rows | Teacher distillation, not independent human preference |
| MusicPrefs | **5,040 audio rows**; paper collects **2,520 pairs**; duration varies, aggregate not verified | Audio with prompt/system metadata; separate fidelity/musicality judgments, prompts hidden during judgment | General musicality/fidelity; unsuitable as adherence ground truth |
| AIME / AIME-survey | **6,000 generated tracks + 500 Jamendo tracks**; **15,600 comparisons**; judged regions 10 seconds | Audio and tag prompts; separate music-quality/text-alignment questions | Useful alignment/quality benchmark, not established personalization data |
| SongEval | Study/card: **2,399 songs, ~140 hours**; inspected HF viewer shows **1,000 rows** | Full-song audio, five aesthetic dimensions, expert ratings | Whole-song aesthetics including vocal phrasing; release coverage must be reconciled |
| MTG-Jamendo | **55,609** processed autotagging tracks; full duration not verified | Audio, genre/instrument/mood tags | Representation probes and attribute supervision; no comparative preference labels |
| MusicCaps | **5,521 ten-second examples**; 15.34 hours of referenced excerpts, derived | YouTube IDs/time ranges and musician-written captions; no blanket original-audio grant | Description/alignment research, not personal preference |
| MusicBench | Approximately **52.8k training rows** in current viewer; unique original-audio hours not verified | Caption/tempo/key/chord metadata and augmentation paths; external audio acquisition needed | Attribute controls; augmentations are not independent songs or preferences |
| LFM-2b | Historically >2 billion listening events; **currently withdrawn** | Listening metadata, not a generated-audio comparison corpus | No acquisition route recommended; curator cites licensing issues |

Sources: [S20](https://huggingface.co/datasets/music-arena/music-arena-dataset/blob/main/README.md), [S06](https://huggingface.co/datasets/HaiwenXia/cmi-pref), [S07](https://huggingface.co/datasets/HaiwenXia/cmi-pref-pseudo), [S19](https://arxiv.org/html/2503.16669v1), [S49](https://huggingface.co/datasets/i-need-sleep/musicprefs), [S21](https://huggingface.co/datasets/disco-eth/AIME-survey), [S22](https://huggingface.co/datasets/disco-eth/AIME), [S23](https://huggingface.co/datasets/ASLP-lab/SongEval), [S27](https://github.com/MTG/mtg-jamendo-dataset), [S28](https://huggingface.co/datasets/google/MusicCaps/blob/main/README.md), [S29](https://huggingface.co/datasets/amaai-lab/MusicBench), [S35](https://www.cp.jku.at/datasets/LFM-2b/).

## Dataset rights audit and decision

| Resource | Declared terms and important distinction | Commercial training / trained weights | Project disposition |
|---|---|---|---|
| Original recordings / contributions | Written scope must cover recording, composition, performers, lyrics and any samples; separate label consent | Allowed only within documented grant; specify release of embeddings and learned weights | Preferred route; grant permission fields are mandatory |
| Music Arena | Card CC-BY-4.0; some model audio omitted under release agreements | Dataset license is promising, but filter by underlying source permissions; no special trained-weight restriction established | Conditional eligible subset, never automatically the entire corpus |
| CMI-Pref / Pseudo | CC-BY-NC-SA-4.0 | Noncommercial only; implications for derivative artifacts require review | Isolated research lane, excluded from default permissive training |
| MusicPrefs | Inspected HF card does not state an explicit dataset license | Not established; paper availability is not dataset permission | Metadata research only until explicit grant is located or obtained |
| AIME | Generated audio declared CC-BY-4.0; Jamendo tracks per-track; prompt tags CC-BY-NC-SA-4.0 | Text-conditioned commercial training is not cleared by the audio license alone; service-origin outputs require review | Restricted research comparator, not default releasable data |
| SongEval | Repository declares CC-BY-NC-SA-4.0 | Do not treat dataset, toolkit or derived weights as commercially cleared | Research comparator; reconcile release counts and component coverage |
| MTG-Jamendo | Code Apache; metadata CC-BY-NC-SA; per-track CC audio; repository expressly limits dataset use to noncommercial research without authorization | Dataset-level permission is required; cherry-picking permissive audio does not automatically resolve acquisition/metadata terms | Exclude from commercial-ready lane without written permission |
| MusicCaps | Annotation dataset CC-BY-SA-4.0; source music linked through YouTube | Annotation license does not license linked recordings; trained-weight consequences not specified | No wholesale audio acquisition for this MVP |
| MusicBench | Card CC-BY-SA-3.0; derives from MusicCaps-related material | Provenance and source-audio rights unresolved; share-alike applicability needs review | No default commercial-ready training |
| LFM-2b | Curator removed availability over license issues | No permission inferred from old mirrors | Reject as an acquisition source |

Dataset sources above; SongEval repository license: [S24](https://github.com/ASLP-lab/SongEval/blob/main/README.md). The policy deliberately avoids laundering uncertain rights through cached embeddings or pseudo-labels.

## Generated audio and Suno

Suno's current terms, revised August 10 and effective September 3, 2026, prohibit using outputs or voice models to compete with Suno, including a competing music-generation product/service. Paid-tier assignments remain subject to the terms. Because the stated long-term aim includes a competing platform, **exclude Suno output from this training and releasable benchmark unless written permission resolves that use**. This is a conservative project policy, not a claim that every private act of ranking music is prohibited. [S39](https://www.suno.com/terms)

ACE-Step 1.5's official code and selected model repository declare MIT; its card expressly discusses commercial outputs. Generate from original text/lyrics without copyrighted reference audio or identity imitation, retain the exact components and licenses, and screen candidates for obvious borrowed material. An open model license cannot guarantee no third-party rights are implicated. [S40](https://huggingface.co/ACE-Step/Ace-Step1.5)

HeartMuLa's published 3B-family checkpoint card declares Apache-2.0; it is another future source, subject to component audit and compute needs. YuE2 is not the default commercial-ready source because its weight permissions distinguish creators from companies. [S41](https://huggingface.co/HeartMuLa/HeartMuLa-oss-3B-happy-new-year), [S33](https://github.com/multimodal-art-projection/YuE)

Do not scrape public demos or acquire subscription outputs in this session. Audio generation is optional future work, separately costed; existing owned recordings are sufficient to start.

## Auditable acquisition procedure

1. Create an immutable asset record before preprocessing: origin URL/file, date, author/contributor, generator revision if applicable, recording/composition/sample provenance, source hash and license evidence location.
2. Record separate permissions for research training, commercial training, audio redistribution, embedding redistribution, and learned-weight release. Use `allowed`, `denied`, or `unknown`, with a rationale and evidence hash. Record prompt/lyrics and label rights separately.
3. Download metadata first for public corpora. Count released audio and unique recording/brief families before acquiring large archives. Never reconstruct withheld audio from other sources.
4. Use a permissive-only default allowlist. Keep restricted evaluation artifacts in a separate experiment profile and output directory. No automatic mixing or distillation from restricted models.
5. Hash original bytes and canonical PCM. Track all descendants of each source, including crops, augmentations, codec variants, covers and alternate renders.
6. Preserve license snapshots and source revision IDs. A release audit walks the full dependency graph of each checkpoint and output dataset.

For contributions, specify whether consent permits public audio, anonymous votes, and trained weights. Do not publish listener names, emails, detailed listening history or free-text explanations by default. Make the limits of withdrawal after public redistribution clear before collection.

## Annotation design

Give the listener a brief and two anonymous, equal-duration excerpts at matched audition loudness. Randomize A/B presentation and question order, log playback completion, and hide generator names and automated scores.

Collect these independent fields:

- **Brief adherence:** A / B / tie / cannot judge.
- **Personal preference for this use:** A / B / tie / cannot judge.
- **Acceptability:** A acceptable? B acceptable? yes / no / unsure.
- Optional confidence and short reason codes: instrumentation, mood, delivery, artifacts, other. Do not require an essay.

“Both unacceptable” is not a preference tie. One candidate can win while both fail. “Cannot judge” is not an uncertain vote for A or B. Preserve conflicting answers across listeners and sessions; do not overwrite them with a supposed objective truth.

Restrict the first briefs to locally audible texture, instrumentation and broad mood. For example, “quiet piano-led nocturnal instrumental with a restrained dynamic feel.” The longer original brief's chorus progression and lyric fidelity cannot be validated from an arbitrary ten-second excerpt. A vocal exploratory subset may be labeled separately, but claims about lyrics or complete arrangement remain excluded.

### Collection stages and burden

| Stage | Proposed size | Purpose | Listener time estimate |
|---|---|---|---|
| P0 usability | 20 brief families × 3 candidates = 60 unique pairs; add 10 blind repeats | Test instructions, rights workflow, stability and playback | 70 × 45–75 sec = 53–88 min, plus preparation/breaks; plan 2–4 hr total |
| P1 main feasibility | 160 families × 4 candidates = 640 clips / 960 within-family pairs | Train, validate, calibrate and test without shared-family leakage | 12–20 hr at 45–75 sec/pair; repeats/QA bring plan to ~15–25 hr |
| P2 confirmation | Fresh test set with ≥100 independent brief families; 4 candidates each gives up to 600 correlated pairs | Better precision and blind recommendation study | 7.5–12.5 hr per listener before repeats; can sample fewer pairs per family |

For P1, allocate **96 / 16 / 16 / 32 families** to train/validation/calibration/test before generating pairs: **576 / 96 / 96 / 192 pair slots**. Actual strict choices will be fewer because of ties, missing labels and exclusions. These totals assume no linked source/artist families force additional grouping. If they do, use the leakage policy in 05 and report the realized counts.

The initial self-labeling study is N-of-1. It can support a claim about Justin on this distribution, not a universal music-preference model. For population claims, recruit multiple consenting listeners and reserve held-out listeners. A proposed modest external panel of five people × two hours × $15–25/hour would cost $150–250 before fees; this is an annotation planning assumption, not a market quote or approved expense.

## What different label counts can establish

| Human pairs | Reasonable use | Not defensible yet |
|---|---|---|
| 50 | Find schema mistakes, gross artifacts and unclear target definitions | Neural superiority, robust calibration, broad personalization |
| 100 | Check repeatability, compact features, preliminary per-user signal | Trustworthy subgroup claims or five-point improvements |
| 500 | Useful regularized baseline learning curves; exploratory MLP comparison | Strong conclusions if comparisons come from only a few songs/briefs |
| 1,000 | More credible scoped evaluation and adaptation curves | Universal vocal, genre, language or generator generalization |
| 10,000+ | Richer multi-user modeling and stronger subgroup studies | Immunity to bias, leakage, weak rights or distribution shift |

Independent brief/song families, listener diversity and label reliability matter more than the raw pair count. A thousand comparisons built from a handful of songs do not equal a thousand independent experiments.

## Efficient feedback and synthetic data

Binary comparisons are easier than absolute scales; multi-criteria ratings are richer but slower and often conflate concepts. Rankings of three or four candidates can reduce repeated listening, but introduce order effects and correlated pairs. Accept/reject decisions measure usefulness, but depend on each creator's changing threshold. Reasons help error analysis; they are not automatically reliable labels for instruments or emotion.

After a random seed set, use uncertainty/disagreement sampling only within training data. Keep at least 30% of new training queries uniformly sampled and log selection probabilities. Never actively select the locked test set. Compare active learning against random sampling on a separate fixed evaluation set.

Synthetic degraded/original pairs are suitable for testing clipping or artifact sensitivity, not proving artistic preference. Teacher scores can cheaply initialize a proxy, but should be recorded as `teacher`, weighted separately, and evaluated on untouched human judgments. Copying CLAP rankings into labels and then “beating” CLAP on those labels is circular. Neither pseudo-labels nor encoder outputs erase original license restrictions.

Disagreements should be analyzed by listener, brief and time. Repeat 10–15% of development comparisons in a later session; report exact and tie-aware consistency. Preserve taste differences rather than filtering out listeners for disagreeing with a majority. Scope narrowing or collecting better context is preferable to forcing consistency through a larger model.
