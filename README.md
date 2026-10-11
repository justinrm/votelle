# Votelle

Votelle is a Python research project investigating compact, specialized models for music evaluation and decision support. The long-term question is whether those models can help larger music-generation systems, recommendation methods, and related applications make more informed decisions. This repository implements the offline data foundation for that research. It is not a trained music evaluator, and the broader applications remain hypotheses. [Project direction](docs/PROJECT_DIRECTION.md) separates that long-term intent from the current experiment.

## Why Votelle?

Music-generation systems can produce many plausible candidates. Checking a creative brief, learning what one person prefers, and choosing among candidates are different problems. General audio quality, acoustic measurements, and text–audio similarity can help, and none of them is an individual creator’s preference. A candidate can follow a brief without being preferred, or be preferred while missing part of the brief.

Protocol v0.1 asks whether a relatively small amount of comparative human feedback can teach a compact ranking model those two distinctions for one creator, using frozen audio and text representations. The intended role, if that experiment supports it, is an evaluation companion alongside larger music systems. The creator retains the final choice. Reduced listening effort and candidate selection would still have to be measured. Reward signals and recommendation support remain longer-term hypotheses in the direction note. A well-controlled negative result is a useful outcome.

The experiment evaluates an **explicitly selected ten-second excerpt**, not a whole song. Personal preference, brief adherence, and human acceptability are distinct judgments. Votelle is not a music generator, streaming application, general-purpose recommender, digital audio workstation, deployed reward-model service, hosted service, or validated universal music-quality predictor.

## Current status

The following describes the working tree reviewed on **October 10, 2026**. “Implemented” means present in source; it does not establish experimental effectiveness. See [current status and immediate gates](docs/STATUS.md) for the resumption record.

| Component | Current state |
| --- | --- |
| Dataset contracts | Implemented: typed JSONL manifests, schema and reference validation |
| Rights and provenance | Implemented: explicit permission policies, evidence checks, media hashes, acquisition receipts |
| Audio preparation | Implemented: declared ten-second crops, mono/48 kHz output, versioned gain-only audition normalization |
| Identity-safe splitting | Implemented: whole connected components from declared source/song/brief relationships and exact hashes |
| Encoder interface and feature cache | Implemented library primitives; deterministic 512-dimensional `dummy` / `fixture-v1` encoder only |
| P-01 real-audio intake | Implemented for three catalog recordings; musical suitability and listening outcomes remain unvalidated |
| Real CLAP extraction | No core adapter. Pinned primary checkpoint: single-clip CPU feasibility succeeded. The 20-clip benchmark has not been run |
| Human feedback collection | Schema and research protocol exist; no completed listening pilot or collection UI |
| Linear ranking and personalization | Planned; no trained models or adaptation results |
| Neural challenger | Conditional research comparison, not implemented |
| Calibration, abstention, inference bundles | Planned; no validated probabilities or release-ready inference artifacts |

The earlier Git-ignored P-01 intake snapshot recorded Disquiet, Mesmerize, and Colorless Aura: three assets with research training declared `allowed`, other permissions `unknown`, and release clearance `not_assessed`, with empty brief, clip, and judgment manifests. A later technical excerpt was prepared for an isolated CLAP attempt. That preparation is not a completed listening dataset or musical acceptance. [Current status](docs/STATUS.md) records the checked single-clip CPU result. The three-asset intake was not re-audited here. These local records are absent from a fresh clone, and permission declarations are not independent legal clearance.

**Fixture success is not evidence of preference prediction.** Generated tones and synthetic graph edges exercise software contracts; they are neither musical evaluation results nor human preference labels. No improvement over a baseline, calibrated probability, full-song understanding, or lyric-fidelity capability is claimed.

## Install from source

Use [uv](https://docs.astral.sh/uv/) and **CPython 3.11**. Both `.python-version` and the project’s `>=3.11,<3.12` requirement select that series; other Python versions are outside the current package contract.

```bash
git clone https://github.com/justinrm/votelle.git
cd votelle
uv python install 3.11
uv sync --locked --group dev
```

`uv sync` creates the project’s isolated `.venv`, installs the project, and includes pytest through the development group. The core dependencies are NumPy, Pydantic, SciPy, and SoundFile; [pyproject.toml](pyproject.toml) declares requirements and [uv.lock](uv.lock) records resolved versions. SoundFile needs libsndfile, normally bundled with its supported wheels. Environment setup may download Python and dependencies; the fixture workflow itself needs no network, model weights, private audio, credentials, or paid service.

The working-tree distribution and CLI are **`votelle-music`**; the import package is **`votelle_music`**; the exception class is **`VotelleError`**. Accepted historical records still use `music-pref` / `music_pref`. Those names describe earlier artifacts; use the current identifiers for commands and imports. These instructions install from the checkout and do not assume a published PyPI distribution. PyTorch and Transformers are not dependencies of this foundation environment; explicitly authorized CLAP feasibility tasks use a separate environment.

## Offline quick start

Run from the repository root:

```bash
uv run python tests/fixtures/build.py --dest tests/fixtures/pilot --families 20
uv run votelle-music validate --config configs/foundation.json
uv run votelle-music split --config configs/foundation.json --output runs/split.json
uv run pytest -q
```

The builder creates twenty independent generated-tone assets, declared clips, rights fixtures, and the five manifests under the ignored `tests/fixtures/pilot/` directory. It copies the [first-party fixture declaration](tests/fixtures/FIRST_PARTY_DECLARATION.md) as evidence. The default fixture has no briefs or judgments; tests construct additional synthetic cases. It is not the twenty-family musical P0 study.

`validate` emits a JSON report and returns a nonzero exit status for errors. `split` writes component membership, seed, manifest hashes, and provenance. The configuration requests 60/10/10/20 train/validation/calibration/test fractions with seed 17: allocation targets, not implemented training or calibration. Generated audio and `runs/` stay out of Git.

[`.github/workflows/ci.yml`](.github/workflows/ci.yml) runs this sequence on Ubuntu with CPython 3.11 and `uv sync --locked`. It does not download models, acquire audio, or use paid compute. A green run is a software check.

The ingestion regression checks semantic identity and matching PCM across deliberately different WAV metadata, while validating each container hash against its own file. Container bytes remain provenance, not an audio-determinism requirement.

## Implemented foundation

### Data contracts and provenance

[Versioned Pydantic schemas](src/votelle_music/schemas.py) describe assets, rights records, briefs, clips, judgments, configuration, and validation reports. A dataset has `assets.jsonl`, `rights.jsonl`, `briefs.jsonl`, `clips.jsonl`, and `judgments.jsonl`; empty manifests are permitted where appropriate. Validation checks schema shape, duplicate identifiers, cross-record references, file and canonical PCM hashes, declared audio properties, brief-text hashes, and excerpt bounds.

Judgments keep adherence and preference choices separate, including `tie` and `cannot_judge`, with independent candidate acceptability fields. Listener, session, presentation order, repeat linkage, and label source are recorded. Synthetic, teacher, and human labels are distinguishable; the schema does not turn a synthetic label into human evidence.

### Reproducible excerpt preparation

Preparation accepts WAV or FLAC and requires operator-selected bounds spanning ten seconds within 1 ms. It rejects invalid samples, digital silence, and substantial phase cancellation on equal-mean downmix, then resamples to exactly 480,000 mono samples at 48 kHz. It neither chooses a crop nor repairs an invalid duration through padding or trimming. Originals are not modified.

| Profile | Behavior |
| --- | --- |
| `none_fixture_only` | Downmix/resample without loudness gain; not a level-matched listening condition |
| `gain_lufs_v1` | One constant gain toward −20 LUFS, capped by a −1 dBTP estimated true-peak ceiling; ±0.1 LU match tolerance |

The audition path uses no compressor, limiter, or fade. A peak-limited or gate-changing excerpt can miss the loudness target. General validation reports a mismatch as a warning; the P-01 preparation path writes WAV/QC outputs but does not append mismatched excerpts to `clips.jsonl`. Technical acceptance is not musical acceptance. Loudness and peak estimation, method identifiers, and preprocessing hashes are specified in [decision 0002](docs/decisions/0002-audition-normalization.md); this is not an EBU-certified meter.

### Grouping and features

Identity components join source-recording IDs, song families, exact file/PCM matches, parent assets, brief families, comparisons, and repeats. Splitting preserves entire components and refuses infeasible allocations rather than falling back to random pairs. A connected comparison graph can make a split impossible. Exact relationships are only as complete as the supplied metadata: near-duplicate detection, artist/listener holdouts, and generator-generalization protocols are not provided by the main splitter.

The `AudioTextEncoder` protocol separates future representation extraction from data preparation. The dummy encoder returns deterministic normalized vectors without musical meaning. Audio feature-cache keys include source PCM hash, excerpt bounds, preprocessing identity, encoder/revision, processor identity, pooling, and dtype. Cache writes use atomic replacement and reuse existing keys; these single-process primitives are not a complete experiment runner or an independent cache-integrity audit.

## Architecture and CLI

The implemented boundaries are deliberately small:

| Module | Responsibility |
| --- | --- |
| [`schemas.py`](src/votelle_music/schemas.py) | Versioned data/configuration contracts and reports |
| [`data/`](src/votelle_music/data/) | Manifest validation, rights checks, identity graphs, splitting, P-01 intake and preparation orchestration |
| [`audio/`](src/votelle_music/audio/) | Decode checks, diagnostics, declared crops, normalization and preprocessing identity |
| [`features/`](src/votelle_music/features/) | Encoder protocol, fixture encoder, cache keys and storage |
| [`cli.py`](src/votelle_music/cli.py) | Four local commands; no training or ranking interface |

Manually supplied source files and rights evidence feed intake; explicit crop bounds feed preparation. Validation and splitting are separate operations. Encoder/cache functionality is a library boundary, not an extraction CLI. The proposed extension is frozen audio/text features → separate adherence/preference scorers → held-out evaluation, calibration, and human selection validation. These downstream stages do not exist yet; no deployed infrastructure is implied.

| Command | Required arguments | Purpose |
| --- | --- | --- |
| `validate` | `--config` | JSON validation report; errors cause failure, warnings alone do not |
| `split` | `--config`, `--output` | Validate and write whole-component membership |
| `ingest` | `--config`, `--source-uri`, `--raw`, `--decoded`, `--acquired-at`, `--decode-tool`, `--decode-version`, `--decode-command` | P-01 local acquisition receipt and conditional asset admission |
| `prepare` | `--config`, `--asset-id`, `--clip-id`, `--start`, `--end` | P-01 crop preparation, WAV/QC outputs, conditional clip admission |

Use `uv run votelle-music --help` or, for example, `uv run votelle-music ingest --help` for parser details. Ingestion additionally accepts `--rights-record-id` and `--family-review`. Relative `dataset_root` paths resolve from the current working directory, so run repository examples from the root.

### P-01 real-audio workflow

[configs/p01_piano.json](configs/p01_piano.json) uses `research_only` and `gain_lufs_v1`. Intake is restricted to the three exact official catalog URIs in [decision 0003](docs/decisions/0003-p01-ingestion.md); it is not a general audio downloader. Supply the raw MP3 and an already decoded WAV/FLAC locally. Decode tool/version/command are recorded, not executed; a lossless container does not make the MP3 source a lossless master.

A reviewed rights row with a matching local evidence file admits an asset to the manifest without changing permissions. Otherwise, intake stages the source with a provisional receipt. Manifest admission, permission-policy validation, and release clearance are separate gates. `prepare` requires an admitted asset but is not a substitute for dataset rights validation. Choose and audition crops, write the creator brief, and explicitly assess musical suitability before any future encoder probe. Do not run `split` on this acquisition pilot. The decision record covers file layout, duplicate rejection, and reviewed family links; its older CLI spelling should be read alongside the current help above.

## Research method and roadmap

The initial representation is proposed frozen music CLAP audio/text embeddings, with exact-brief cosine similarity as a zero-training semantic baseline. Regularized linear pairwise scoring comes first, using audio–text interaction features that do not disappear when candidate scores are subtracted. A small shared neural scorer is a controlled challenger only if eligible data and baseline evidence justify it. Separate target models preserve the distinction between adherence and personal preference.

Low-data personalization would fit a regularized listener-specific adjustment and measure learning curves on later, unseen families. Planned evaluations use source/brief grouping, training-only feature fitting, independent calibration data, locked test sets, and group-aware uncertainty. Ranking margins and training sigmoids are not publicly interpretable preference probabilities without calibration evidence. Abstention and blind human selection/acceptability studies must establish scope and utility; neither a single-listener pilot nor fixture success establishes general musical understanding. Generation savings would require a separate sequential-policy study, not merely ranking an already generated batch.

The evidence-based sequence is:

| Milestone | Gate before advancing |
| --- | --- |
| P-01 audition | Finalize a creator brief; select, prepare, and musically accept ten-second excerpts |
| Bounded CLAP probe | Single-clip CPU feasibility succeeded on October 10 under the existing memory safeguards. The 20-clip benchmark and MPS comparison have not been run. Further expansion needs explicit authorization |
| P0 listening pilot | Twenty independent brief families, three candidates each, sixty unique comparisons plus ten delayed repeats; verify question meaning and repeatability |
| Fixed-feature ranking | Establish semantic/compact controls and regularized linear baselines on eligible, grouped data |
| Conditional neural comparison | Compare on the same locked examples; diagnose labels and representation limits before escalating complexity |
| Personalization and utility | Test limited-feedback adaptation on future holdouts and selection usefulness in blind listening |
| Reproducible research release | Confirm artifact-specific permissions; publish permitted artifacts and reproducible methods, including inconclusive or negative results |

No deadlines or positive results are implied. Detailed requirements live in the [encoder and model note](docs/research/03_ENCODER_AND_MODEL.md), [training and evaluation note](docs/research/04_TRAINING_AND_EVALUATION.md), and [P0 listening protocol](docs/research/02_P0_LISTENING_PROTOCOL.md). The dated CLAP handoff is archived and still states its pre-attempt contract. [Current status](docs/STATUS.md) records the later single-clip CPU result.

## Reproducibility and data governance

Permissions are explicitly `allowed`, `denied`, or `unknown`; a license name never grants training permission. `research_only` requires allowed research training. `commercial_ready` requires allowed research training, commercial training, audio release, embedding release, and checkpoint release. Unknown permissions block the applicable policy. These declarations support human review, not legal-evidence interpretation or independent clearance of recordings, compositions, lyrics, briefs, and annotations.

Preserve source media and source manifests; intake appends new records, while prepared derivatives, QC, and split artifacts record distinct processing steps. Hashes, declared identities, seeds, preprocessing profiles, and locked environments make transformations traceable. Missing relationship metadata and unrecognized duplicates remain limitations. Frozen-feature extraction is not permission to use held-out labels for fitting or model selection.

The workflow is local-first. Real audio, embeddings, weights, and generated run outputs are Git-ignored; a fresh checkout contains software and fixture generation, not a licensed musical dataset. Audio redistribution, embedding release, checkpoint release, and commercial use each need their own applicable permission. An encoder’s license does not authorize third-party audio redistribution or clear every potential dataset or generated output. See [data governance](docs/research/01_DATA_GOVERNANCE.md) and the [foundation decisions](docs/decisions/0001-foundation-choices.md). Historical `music-pref` names in decisions 0001–0003 are explained in [decision 0004](docs/decisions/0004-votelle-naming.md).

## Contributing and documentation

Start with the source installation and offline quick start above. Read [AGENTS.md](AGENTS.md), [docs/STATUS.md](docs/STATUS.md), and the decision relevant to the proposed change, then inspect the affected source and tests. Useful contributions include stronger contract tests, reproducibility checks, and bounded work on the current development gates. Discuss changes to excerpt length, grouping, rights policy, or label meaning before implementation: these require protocol versioning, not an incidental refactor. Do not add heavyweight encoder dependencies or treat scientific requirements as satisfied by passing tests.

[The research index](docs/research/README.md) explains authority and selective navigation. Source, tests, configuration, and the lock establish executable behavior; decisions establish accepted choices; active research establishes still-unmet scientific requirements. [Project direction](docs/PROJECT_DIRECTION.md) states long-term intent and does not override those sources. The [MVP specification](docs/research/05_MVP_SPECIFICATION.md) distinguishes implemented behavior from proposed modules. The [documentation map](docs/README.md) is the entry point for the research notes. [Archived material](docs/archive/README.md) preserves rationale and citations. `graphify-out/` is an optional local navigation aid, not a specification and not part of a fresh checkout. Generated graph files are gitignored. Archive material is excluded from routine indexing. Consult original sources rather than treating inferred graph edges as facts. Developers can regenerate a local graph with `graphify update .` when the CLI is installed.

## Licensing and acknowledgments

Votelle’s original source code and project documentation are licensed under the [Apache License, Version 2.0](LICENSE), unless a file explicitly states otherwise. The package metadata declares the SPDX identifier `Apache-2.0`, and source and wheel distributions include the license text.

Original project code, third-party libraries, pretrained weights, recordings/compositions, human annotations, and derived artifacts have separate licensing and consent considerations. Planned CLAP use must retain the terms and identity of the specific library and checkpoint selected; those terms do not license this repository or its audio. No trained checkpoint or musical dataset is released here.

The research builds on [LAION CLAP](https://github.com/LAION-AI/CLAP), established pairwise-ranking and calibration methods, and the upstream Python scientific stack. P-01 investigates recordings from Kevin MacLeod’s Incompetech catalog under separately recorded rights evidence. These acknowledgments imply neither affiliation nor endorsement.
