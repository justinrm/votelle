# Status

Votelle asks whether a compact model can learn one creator's musical preferences, and separately whether a clip follows that creator's brief, from comparative listening judgments. A negative result is a valid outcome. The listener keeps the final choice.

Research protocol **v0.1**. This file is the resumption note. Authority order is in `docs/research/README.md`.

The human-readable name is Votelle. This tree's package is `votelle_music` and the CLI is `votelle-music`. Decision records and the archived handoff still say `music-pref` / `music_pref`. `MusicPrefError` is still the exception class. That rename is a separate task.

## Licensing

On October 10, 2026, the maintainer selected Apache-2.0 for Votelle’s original source code and project documentation, unless a file explicitly states otherwise. The root [LICENSE](../LICENSE) contains the standard terms; `pyproject.toml` declares `Apache-2.0` and includes the license file in distributions. This does not change third-party library/model licenses or grant recording, composition, annotation, training, or artifact-release permissions. P-01 permission declarations remain unchanged.

## Implemented

Checked against source, configs, and tests. Fixture success is not preference prediction.

- JSONL manifests, explicit rights profiles, and unknown-permission blocking (`research_only`, `commercial_ready`).
- Leakage-safe splits by source and brief ancestry. Connected components are not broken.
- Ten-second excerpts. `none_fixture_only` resamples and does not loudness-match. `gain_lufs_v1` applies one gain toward -20 LUFS, capped at -1 dBTP, with a ±0.1 LU match flag.
- Content-addressed cache and a dummy encoder, `dummy` / `fixture-v1`. Any other encoder is refused.
- P-01 ingest and prepare. Provisional review, dataset eligibility, and release clearance stay distinct. Ingest does not edit permissions.

## Implemented, not experimentally validated

- `gain_lufs_v1` on fixture tones. No musically accepted excerpt is in Git.
- The P-01 intake path. A passing ingest test is not a rights grant and not a listening result.

## Not implemented

CLAP, training, the linear scorer, the neural challenger, calibration, inference bundles, a generator, and a UI. Torch and Transformers are not dependencies of this environment.

## P-01

Git does not contain the audio. `data/` is gitignored, so a clone has the workflow and not the files.

On this machine, outside Git, `data/p01_piano` has Disquiet, Mesmerize, and Colorless Aura ingested. Each receipt is `reviewed_with_evidence` and `in_manifest: true`. `research_training` is `allowed`. Commercial training, audio release, embedding release, and checkpoint release are `unknown`. `release_clearance` is `not_assessed`. Briefs, clips, and judgments are empty. Nothing has been prepared. That local state was not re-validated by this documentation pass.

## CLAP

No adapter, no weights, no Mac benchmark. The probe contract is `docs/research/03_CLAP_Encoder_Feasibility_and_Benchmark_Handoff.md`. Decision 0002 says the foundation config cannot name CLAP yet.

## Open

These remain unresolved. Archiving the risk note did not close them.

- The eight source conflicts in `docs/archive/research-v0.1/09_Research_Risks_and_Open_Questions.md`: TuneJury's license, CMI counts, SongEval coverage, MusicPrefs' permission, Music Arena eligibility, HeartCLAP weights, MusicFM provenance, and unmeasured local encoder deployment.
- No creator brief, no accepted 10-second crops, no human judgments.
- Release permissions for P-01 are `unknown`, so `commercial_ready` is not available.
- Whether frozen CLAP can carry the preference signal is untested.
- Package naming is inconsistent, as noted above.

`docs/decisions/0002-audition-normalization.md` is the loudness procedure. The archived feasibility handoff still describes that procedure as a proposal. Do not merge those texts.

## Next

Write one creator brief and choose one 10-second span for each ingested P-01 recording. Run `votelle-music prepare`. Stop before CLAP until those excerpts are accepted as musically suitable.

## Where to look

- Decisions: `docs/decisions/0001-foundation-choices.md`, `0002-audition-normalization.md`, `0003-p01-ingestion.md`
- Active research: `docs/research/README.md`
- Open risks and citations: `docs/archive/README.md`
