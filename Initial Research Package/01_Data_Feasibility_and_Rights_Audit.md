# 01 — Data Feasibility & Rights Audit

Music Preference Model v0.1 · Evidence checked October 10, 2026 UTC / October 9 Pacific

**DATA: conditional GO for a small acquisition test; P0 is not yet assembled or cleared asset by asset.** The strongest newly verified source is Kevin MacLeod’s Incompetech catalog. Its rightsholder explicitly offers music for AI training, publishes CC BY 4.0 terms, and provides individual download references. This is stronger evidence than a dataset’s license badge alone. No audio was downloaded or auditioned in this session.

Evidence labels: **Verified** means primary-source documentation or metadata inspected; **Derived** means arithmetic; **Recommendation** is our proposed action; **Unresolved** is a remaining gate. License conclusions below are scoped interpretations of published grants, not warranties about every underlying right.

## Source inventory and acquisition decision

| Source / official acquisition reference | Quantity, duration, media and metadata | Rights evidence and disposition |
|---|---|---|
| Original recordings supplied by Justin | Inventory unknown; **0 supplied/verified**. Request 3 genuinely different takes or arrangements per brief, WAV/FLAC preferred, each with a usable 10-second region. | Best control when Justin owns composition, recording and performance and clears samples. Personal authorship of lyrics or payment for a generation service is insufficient. **Conditional**, pending first-party provenance declaration. |
| Direct independent-artist contribution | No contributor contacted; **0 committed**. A scoped request for 4 briefs × 3 takes would yield 12 clips; this is a target, not available inventory. | Obtain an explicit grant for commercial ML use, derivatives, embeddings and checkpoints; separately agree audio publication and label consent. **Conditional** until granted. |
| [Incompetech catalog](https://incompetech.com/music/royalty-free/pieces.json) and [official access/rights documentation](https://incompetech.com/agent-section/) | Live JSON: **1,443 distinct filenames, 87.14 hours** from listed durations; 1,439 list ≥10 seconds. MP3 acquisition; sample rate, channels and bitrate need file inspection. Titles, ISRCs, dates, instruments, moods, BPM and descriptions supplied. No UUID field in the actual JSON despite documentation mentioning one. | [Explicit AI-training offer](https://incompetech.com/wordpress/2022/11/music-catalog-available-for-any-ai-training-project/), plus [CC BY 4.0/attribution guidance](https://www.incompetech.com/music/royalty-free/faq.html). **Permitted source-level route**, with attribution and individual provenance review. The older offer describes ~1,800 files / four days; it is not the current public JSON count. |
| [MusicNet, original release](https://zenodo.org/records/5120004) | 330 classical recordings; approximately 34 hours [reported by UW](https://news.cs.washington.edu/2016/11/30/uw-researchers-hit-the-right-note-with-new-machine-learning-tool-for-music/). PCM WAV plus note CSVs; 43.8 kB recording provenance CSV; official audio archive 11.1 GB. Exact file quality not inspected. | Zenodo API declares CC BY 4.0, but description identifies mixed CC/public-domain source performances. Recording-level provenance needs reconciliation. **Conditional classical control**, not blanket clearance and not a convenient selective acquisition route. Do not fetch the archive. |
| [Music Arena](https://huggingface.co/datasets/music-arena/music-arena-dataset/blob/main/README.md) | July 2026 release lists 1,959 included audio files. JSON has prompts, system names, duration, sample rate, paths and votes. Encoding varies/unverified; no total duration calculated. | CC BY 4.0 card; specific systems’ audio withheld. Provider permissions and user lyrics/prompts remain to be reviewed per source. Same-prompt pairs do not ensure three candidates per family. **Conditional; 0 eligible triplets verified**. No inherited votes used as our labels. |
| [ACE-Step 1.5, self-generated outputs](https://huggingface.co/ACE-Step/Ace-Step1.5) | **0 outputs available here**. Could prospectively produce 60 candidates from 20 briefs; duration/format controlled by a separately audited generation workflow. | MIT metadata and express commercial-output statement are promising. **Conditional**, subject to full component audit below, provenance and output screening. Generation is not needed for this first pilot. |
| [Musopen](https://musopen.org/music/) | Large catalog; individual durations/formats vary, no cleared subset counted. | [Its FAQ](https://musopen.org/faq/) explicitly distinguishes recording and composition rights and disclaims verifying user uploads. **Conditional**, not automatic clearance from a public-domain icon. |

## Source-level permissions matrix

“Review” means unknown for the specific assets; it must not be serialized as allowed. “BY” requires retained credits, license/source links and change notices. “Blocked” is this project’s applicable-use decision, not a claim about all possible legal exceptions.

| Source | Research ML | Commercial ML | Audio release | Embedding release | Trained-head release |
|---|---|---|---|---|---|
| Fully owned original, documented declaration | Allowed | Allowed | Per declaration | Per declaration | Per declaration |
| Artist contribution not yet granted | Review | Review | Review | Review | Review |
| Selected Incompetech original tracks | Permitted under published offer + BY grant, after review | Permitted under BY grant + training offer, after review | BY, within licensor’s rights | BY/provenance review | BY/provenance review; do not imply all source material becomes Apache-licensed |
| MusicNet / Musopen | Review underlying recording | Review | Review | Review | Review |
| Music Arena | Review provider/content chain | Review | Review | Review | Review |
| Audited ACE-Step outputs | Conditional | Conditional | Conditional | Conditional | Conditional |
| Jamendo acquisition / MTG-Jamendo without authorization | Restricted; authorization requested | Blocked | Per-track, not established here | No automatic clearance | No automatic clearance |
| AIME as a combined audio+prompt corpus | Restricted research review | Blocked for default combined corpus | Mixed | Mixed | Mixed |
| Suno-origin material | Excluded from this project absent permission | Excluded | Not evaluated | Excluded | Excluded |

The Incompetech interpretation relies on the creator’s training offer **and** the commercial reproduction/adaptation grant, rather than inferring ML rights from free access. Public embedding/head release is not expressly addressed by the offer. CC BY contains no special checkpoint prohibition, but exact attribution and component coverage must be recorded before release. Keeping an embedding private does not cure unauthorized acquisition. [CC legal code](https://creativecommons.org/licenses/by/4.0/legalcode.en); [CC’s AI-training guidance](https://creativecommons.org/using-cc-licensed-works-for-ai-training-2/).

## Material exclusions and component questions

- **Jamendo:** [terms updated April 17, 2025](https://licensing.jamendo.com/en/legal/termsofuse) prohibit unauthorized commercial text/data mining, explicitly including AI. [MTG-Jamendo](https://github.com/MTG/mtg-jamendo-dataset) also has dataset-level restrictions. A permissive track tag does not by itself resolve the acquisition terms.
- **AIME:** [card](https://huggingface.co/datasets/disco-eth/AIME) distinguishes 6,000 generated tracks, 500 per-track-licensed Jamendo recordings, and NC-SA prompt tags. Rewriting tags does not establish clean provenance. Exclude from the default lane.
- **Suno:** [current terms](https://www.suno.com/terms) restrict using outputs to compete with Suno. Existing project exclusion remains. This includes Suno audio found inside another collection.
- **FreePD:** [original site is closed](https://www.freepd.com/). Do not recommend a mirror as equivalent clearance. The artist’s [2025 account](https://billy.incompetech.com/wordpress/2025/07/the-ai-elephant-in-the-room/) also reports posting some Suno music there; search-index text was available, but the page fetch was intermittent. This reinforces caution, not proof about any particular file.
- **ACE-Step:** inspected [official file tree](https://huggingface.co/ACE-Step/Ace-Step1.5/tree/main) contains DiT turbo (~4.79 GB), VAE (~0.34 GB), Qwen3-Embedding-0.6B (~1.19 GB), and adapted 1.7B LM (~3.71 GB). The generator [code license](https://github.com/ace-step/ACE-Step-1.5/blob/main/LICENSE) is MIT; [upstream Qwen embedding](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B) declares Apache 2.0. The package card’s MIT declaration is not a component-by-component warranty. Pin all actual components, retain inherited notices, inspect any auxiliary model/download, and verify adapted LM/VAE coverage. No root LICENSE was found at the tested HF path. The default packaged tensors total ~10.0 GB; “under 4 GB VRAM” does not establish 8 GB unified-memory feasibility. Prefer a contributor’s documented outputs later, not local generation now.

## Acquisition manifest and review procedure

The shortlist below is **metadata-verified, not audition-approved**. Each direct audio URL returned HTTP 200 to a HEAD request; no audio body was fetched. MIME was generic application/octet-stream, so successful decoding and MP3 properties remain unverified. Preliminary 12 files target four groups; eight additional files support the separate 20-unique-clip resource probe. Do not treat the reserve as new listening families without assembling matched alternatives.

For each selected file, create the existing package’s asset/rights/clip records, including: source URL and ISRC; rightsholder; origin type; recording/composition/sample scope; exact permission evidence and retrieval date/hash; separate research/commercial/audio/embedding/checkpoint permissions; original and PCM hashes after acquisition; measured duration/rate/channels; explicit excerpt bounds; family ancestry; attribution and modifications. Use unknown for unfinished fields. Snapshot the track page and rights pages before ingestion. Exclude covers, third-party collaborators, unusual samples or generative-service provenance until clarified. The site’s common composer metadata is not proof that its classical arrangements are original compositions.

Catalog snapshot SHA-256: 54802ad340562624b9d1c9c97aa9f005e2b9bf79001f8a1a07ed857e68b2164a. Counts describe this snapshot, not guaranteed future availability.

**Expected yield, not a measured result:** start with 12 downloads and aim for 12 valid excerpts; replace failures only within the same brief family after review. For P0, shortlist up to 80 tracks to obtain 60 valid candidates across 20 independent brief/source groups. Catalog capacity is ample; meaningful matching and provenance checks are the bottleneck. Budget approximately 3–6 hours for P0 sourcing/preparation, in addition to listening. No existing collection of Justin-owned music is assumed.

For contributions, request scope covering the named compositions, masters, performers, lyrics and samples; reproduction/cropping/resampling; commercial training/evaluation; distribution of embeddings and learned weights; audio redistribution as a separate choice; attribution; and label consent. A rights request may be drafted later, but no one was contacted in this session.

## Exact acquisition shortlist

All entries below: Kevin MacLeod / Incompetech; proposed rights record INC-BY-AI-2026-10-09, pending per-asset review. Listed duration comes from the catalog. Start/end times remain unset until audition; never substitute a guessed crop.

| Group / role | Recording and official individual acquisition URL | ISRC | Listed duration |
|---|---|---|---|
| P-01 | [Disquiet](https://incompetech.com/music/royalty-free/mp3-royaltyfree/Disquiet.mp3) | USUAN1500036 | 00:03:05 |
| P-01 | [Mesmerize](https://incompetech.com/music/royalty-free/mp3-royaltyfree/Mesmerize.mp3) | USUAN1500005 | 00:07:04 |
| P-01 | [Colorless Aura](https://incompetech.com/music/royalty-free/mp3-royaltyfree/Colorless%20Aura.mp3) | USUAN1400008 | 00:02:38 |
| P-02 | [Night in Venice](https://incompetech.com/music/royalty-free/mp3-royaltyfree/Night%20in%20Venice.mp3) | USUAN1900056 | 00:03:38 |
| P-02 | [Lobby Time](https://incompetech.com/music/royalty-free/mp3-royaltyfree/Lobby%20Time.mp3) | USUAN1600054 | 00:03:13 |
| P-02 | [Airport Lounge](https://incompetech.com/music/royalty-free/mp3-royaltyfree/Airport%20Lounge.mp3) | USUAN1100806 | 00:05:08 |
| P-03 | [RetroFuture Clean](https://incompetech.com/music/royalty-free/mp3-royaltyfree/RetroFuture%20Clean.mp3) | USUAN1200040 | 00:03:26 |
| P-03 | [RetroFuture Dirty](https://incompetech.com/music/royalty-free/mp3-royaltyfree/RetroFuture%20Dirty.mp3) | USUAN1200041 | 00:03:26 |
| P-03 | [RetroFuture Nasty](https://incompetech.com/music/royalty-free/mp3-royaltyfree/RetroFuture%20Nasty.mp3) | USUAN1200042 | 00:03:26 |
| P-04 | [Grand Dark Waltz Allegro](https://incompetech.com/music/royalty-free/mp3-royaltyfree/Grand%20Dark%20Waltz%20Allegro.mp3) | USUAN2100020 | 00:06:25 |
| P-04 | [Grand Dark Waltz Allegretto](https://incompetech.com/music/royalty-free/mp3-royaltyfree/Grand%20Dark%20Waltz%20Allegretto.mp3) | USUAN2100019 | 00:07:30 |
| P-04 | [Grand Dark Waltz Moderato](https://incompetech.com/music/royalty-free/mp3-royaltyfree/Grand%20Dark%20Waltz%20Moderato.mp3) | USUAN2100018 | 00:08:28 |
| B-reserve | [The Complex](https://incompetech.com/music/royalty-free/mp3-royaltyfree/The%20Complex.mp3) | USUAN1300025 | 00:04:28 |
| B-reserve | [Odyssey](https://incompetech.com/music/royalty-free/mp3-royaltyfree/Odyssey.mp3) | USUAN1500012 | 00:05:06 |
| B-reserve | [New Direction](https://incompetech.com/music/royalty-free/mp3-royaltyfree/New%20Direction.mp3) | USUAN1100677 | 00:11:20 |
| B-reserve | [Clear Air](https://incompetech.com/music/royalty-free/mp3-royaltyfree/Clear%20Air.mp3) | USUAN1100626 | 00:03:04 |
| B-reserve | [When The Wind Blows](https://incompetech.com/music/royalty-free/mp3-royaltyfree/When%20The%20Wind%20Blows.mp3) | USUAN1100717 | 00:04:26 |
| B-reserve | [Funky Chunk](https://incompetech.com/music/royalty-free/mp3-royaltyfree/Funky%20Chunk.mp3) | USUAN1500054 | 00:03:59 |
| B-reserve | [Spy Glass](https://incompetech.com/music/royalty-free/mp3-royaltyfree/Spy%20Glass.mp3) | USUAN1500058 | 00:03:47 |
| B-reserve | [Darkling](https://incompetech.com/music/royalty-free/mp3-royaltyfree/Darkling.mp3) | USUAN1700050 | 00:02:50 |

Source-level permission evidence applies as discussed above; every row still needs decoded-file inspection and an asset-specific review record. These URLs are an acquisition plan, not a redistributed audio collection.
