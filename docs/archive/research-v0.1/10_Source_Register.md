# 10 — Primary Source Register

Research cutoff: October 9, 2026 Pacific. Sources accessed October 10, 2026 UTC.

This is a literature/documentation review. Published results are author-reported and were not independently reproduced. License statements refer to the artifact or page named; they do not certify underlying rights. Current repository/model pages must be revision-pinned before implementation. The package avoids relying on third-party comparison blogs for technical conclusions.

| ID | Primary source | Evidence used |
|---|---|---|
| S01 | [TuneJury repository](https://github.com/yonghyunk1m/TuneJury) | Closest prior art, architecture and reported benchmark |
| S02 | [TuneJury model card](https://huggingface.co/TuneJury/tunejury) | Checkpoint variants, scope and declared licenses |
| S03 | [TuneJury LICENSE](https://github.com/yonghyunk1m/TuneJury/blob/main/LICENSE) | Noncommercial coverage of code and main release; conflict flag |
| S04 | [CMI-RewardBench, ICML 2026 proceedings](https://proceedings.mlr.press/v306/ma26am.html) | Peer-reviewed task and method summary |
| S05 | [CMI-RewardBench repository](https://github.com/Haiwen-Xia/CMI-RewardBench) | Public benchmark interface, code license and reported comparisons |
| S06 | [CMI-Pref dataset](https://huggingface.co/datasets/HaiwenXia/cmi-pref) | Human vote counts, duration, labels and NC-SA terms |
| S07 | [CMI-Pref-Pseudo dataset](https://huggingface.co/datasets/HaiwenXia/cmi-pref-pseudo) | Pseudo labels, valid-vote distinction, revision-sensitive counts |
| S08 | [LAION larger CLAP music card](https://huggingface.co/laion/larger_clap_music) | Selected aligned encoder and artifact license |
| S09 | [LAION larger CLAP music files](https://huggingface.co/laion/larger_clap_music/tree/main) | Download size and availability |
| S10 | [LAION unfused CLAP files](https://huggingface.co/laion/clap-htsat-unfused/tree/main) | Fallback size and artifact license |
| S11 | [Native LAION CLAP license](https://github.com/LAION-AI/CLAP/blob/main/LICENSE) | CC0 code/repository terms; distinct from selected HF packaging |
| S12 | [MERT-v1-95M card](https://huggingface.co/m-a-p/MERT-v1-95M) | Family dimensions, sizes, sample rates and weight license |
| S13 | [MuQ repository](https://github.com/tencent-ailab/MuQ) | MuQ/MuLan types, sizes, FP32 advice and licensing |
| S14 | [MusicFM repository](https://github.com/minzwon/musicfm) | Conformer/BEST-RQ approach, checkpoints and adaptation guidance |
| S15 | [MERT-v2-30s card](https://huggingface.co/m-a-p/MERT-v2-30s) | Verified 2026 short-context representation release |
| S16 | [MERT-v2-FullSong card](https://huggingface.co/m-a-p/MERT-v2-FullSong) | Full-song context, dimensions and NC weights |
| S17 | [Music Flamingo model card](https://huggingface.co/nvidia/music-flamingo-hf) | Audio-language evaluation candidate, scope and NC terms |
| S18 | [OpenL3 repository](https://github.com/marl/openl3) | Representation options and separate code/weight licenses |
| S19 | [MusicPrefs / MAD paper](https://arxiv.org/html/2503.16669v1) | Metric validity, preference collection and label semantics |
| S20 | [Music Arena dataset README](https://huggingface.co/datasets/music-arena/music-arena-dataset/blob/main/README.md) | Monthly counts, missing audio, labels and license |
| S21 | [AIME-survey card](https://huggingface.co/datasets/disco-eth/AIME-survey) | Comparison counts, ten-second judgments and target axes |
| S22 | [AIME audio card](https://huggingface.co/datasets/disco-eth/AIME) | Audio counts and mixed audio/tag permissions |
| S23 | [SongEval dataset card](https://huggingface.co/datasets/ASLP-lab/SongEval) | Study size, release mismatch, perceptual axes and duration |
| S24 | [SongEval repository README](https://github.com/ASLP-lab/SongEval/blob/main/README.md) | Evaluation toolkit and NC-SA license |
| S25 | [Audiobox Aesthetics repository](https://github.com/facebookresearch/audiobox-aesthetics) | Four-axis quality evaluator and published terms |
| S26 | [PAM repository](https://github.com/soham97/pam) | Prompt-based no-reference quality baseline |
| S27 | [MTG-Jamendo repository](https://github.com/MTG/mtg-jamendo-dataset) | Data counts, annotations and explicit commercial authorization requirement |
| S28 | [Google MusicCaps card](https://huggingface.co/datasets/google/MusicCaps/blob/main/README.md) | Referenced excerpt count, annotation type and license |
| S29 | [MusicBench card](https://huggingface.co/datasets/amaai-lab/MusicBench) | Augmented metadata, current row scale and license |
| S30 | [ACE-Step 1.5 tutorial](https://github.com/ace-step/ACE-Step-1.5/blob/main/docs/en/Tutorial.md) | Existing batch screening and human final selection |
| S31 | [ACE-Step lyric-score implementation](https://github.com/ace-step/ACE-Step-1.5/blob/main/acestep/core/generation/handler/lyric_score.py) | Attention-derived LM/DiT scoring interface |
| S32 | [HeartMuLa official repository](https://github.com/HeartMuLa/heartlib) | Released components and generation integration context |
| S33 | [YuE2 official repository](https://github.com/multimodal-art-projection/YuE) | Current releases, creator/company license distinction |
| S34 | [BPR original research](https://arxiv.org/abs/1205.2618) | Established personalized pairwise ranking background |
| S35 | [LFM-2b curator page](https://www.cp.jku.at/datasets/LFM-2b/) | Withdrawal over licensing issues; rejected acquisition source |
| S36 | [TypeSafe API documentation](https://api.typesafe.ai/redoc) | Jev typed state/question/decision interface |
| S37 | [TypeSafe Jev introduction](https://typesafe.ai/blog/introducing-system-one-models-and-jev) | Primary vendor description; not an audio benchmark |
| S38 | [Laya official model card](https://huggingface.co/convaiinnovations/laya) | Text architecture, checkpoint sizes and calibration caveats |
| S39 | [Suno Terms of Service](https://www.suno.com/terms) | Output competition restriction and qualified paid-tier rights |
| S40 | [ACE-Step 1.5 model repository](https://huggingface.co/ACE-Step/Ace-Step1.5) | MIT weights, component packaging and output-use statement |
| S41 | [HeartMuLa released checkpoint card](https://huggingface.co/HeartMuLa/HeartMuLa-oss-3B-happy-new-year) | Availability and Apache-2.0 weight declaration |
| S42 | [Guo et al., calibration paper](https://arxiv.org/abs/1706.04599) | Temperature scaling and empirical calibration background |
| S43 | [Universal Music Representations?, 2025](https://arxiv.org/abs/2506.17055) | Cross-cultural representation limits and adaptation findings |
| S44 | [HeartMuLa technical paper](https://arxiv.org/abs/2601.10547) | HeartCLAP and music-model family description |
| S45 | [music2vec-v1 card](https://huggingface.co/m-a-p/music2vec-v1) | Older audio representation and NC terms |
| S46 | [MuQ-MuLan configuration](https://huggingface.co/OpenMuQ/MuQ-MuLan-large/blob/main/config.json) | 512-d latent space and ten-second configuration |
| S47 | [MusicFM model repository](https://huggingface.co/minzwon/MusicFM) | MIT metadata and sparse model-card documentation |
| S48 | [MusicFM code license](https://github.com/minzwon/musicfm/blob/master/LICENSE) | MIT/Apache component distinction |
| S49 | [MusicPrefs dataset card](https://huggingface.co/datasets/i-need-sleep/musicprefs) | Audio availability/row count and missing explicit license |
| S50 | [CLAP processor configuration](https://huggingface.co/laion/larger_clap_music/blob/main/preprocessor_config.json) | 48 kHz, ten-second window and random-truncation default |
| S51 | [Apple MacBook Neo specifications](https://www.apple.com/macbook-neo/specs/) | 8 GB unified-memory configuration |
| S52 | [Apple MacBook Neo announcement](https://www.apple.com/newsroom/2026/03/say-hello-to-macbook-neo/) | A18 Pro configuration |
| S53 | [PyTorch MPS documentation](https://docs.pytorch.org/docs/stable/notes/mps.html) | Backend capability and runtime support checks |
| S54 | [Runpod pricing](https://www.runpod.io/pricing) | Illustrative current pod rates; volatile, not an approved expense |

## Additional directly inspected references

- [CMI-RM model card](https://huggingface.co/HaiwenXia/CMI-RM): published NC license and approximately 0.7B total parameters; body largely undocumented.
- [CLAP model configuration](https://huggingface.co/laion/larger_clap_music/blob/main/config.json): 512-dimensional projection and audio-tower structure.
- [Native LAION CLAP repository](https://github.com/LAION-AI/CLAP): music-specific checkpoint names and training/inference instructions.
- [OpenL3 tutorial](https://github.com/marl/openl3/blob/main/docs/tutorial.rst): 512/6,144-dimensional embeddings and configurable extraction.
- [MERT code license](https://github.com/yizhilll/MERT/blob/main/LICENSE): Apache-2.0 root license, distinct from NC weights and inherited component notices.

## Scope of verification

Repository pages and model file listings establish public artifact availability, not successful execution or independent benchmark reproduction. Some specifications remain explicitly unverified in 03 and 09. No third-party rights clearance, model weight download, private service access or paid compute purchase occurred. Decisions, proposed thresholds, derived parameter counts and budget envelopes are this project's research design rather than claims made by the cited authors.
