# 0002 — Audition normalization

Session 2A of research v0.1. This implements `gain_lufs_v1`. It does not change excerpt length, grouping, rights, or label meaning. Schema version stays `0.1`.

`none_fixture_only` is unchanged: resample only, no loudness gain, and `level_matched` must be false. `gain_lufs_v1` requires `level_matched: true`. A synthetic tone that passes these tests is a fixture, not evidence of musical suitability or preference.

## Order

1. Decode WAV or FLAC to float64. Reject other suffixes, including MP3.
2. Require a caller-selected span of 10 seconds ± 1 ms. Do not pad, trim, or choose the crop.
3. Reject non-finite samples and digital silence (peak absolute amplitude below `1e-8`) on the multi-channel crop.
4. Downmix with an equal mean. Reject the crop when the mono result is digital silence while a channel is not, or when mono mean-square is below 1% of the channel mean-square (`equal_mean/phase_ratio_0.01/v1`). This is not an ITU surround fold-down.
5. Resample with `scipy.signal.resample` to exactly 480,000 mono samples at 48 kHz (`scipy.signal.resample/fft/v1`).
6. For `gain_lufs_v1` only, measure that derivative, apply one constant gain, and remeasure. The original file is not opened for writing.

## Gain

Target integrated loudness is **-20 LUFS**. True-peak ceiling is **-1 dBTP**. The applied linear gain is the smaller of the loudness gain and the ceiling gain. There is no compressor, limiter, fade, or sample-by-sample nonlinearity. A second constant scale runs only when float error puts the remeasured true peak over the ceiling.

Loudness is ITU-R BS.1770-4 K-weighting at 48 kHz (`itu-r-bs.1770-4/k-weight/48kHz/v1`): 400 ms blocks, 75% overlap, absolute gate -70 LUFS, relative gate -10 LU, channel weight 1.0 for mono and for each of stereo left/right. The shelf and high-pass constants are the De Man form of the BS.1770-4 biquads. Filters start at rest on the excerpt; there is no pre-roll.

If every block is below the absolute gate, the gain uses ungated block power (`ungated_block_power_v1`). The value stored after gain is the gated remeasurement. Gated and ungated results are not both stored as the audition loudness.

True peak is 4× `scipy.signal.resample_poly` with the default Kaiser-5 window and `padtype="line"` (`scipy.signal.resample_poly/4x/kaiser5/line-pad/v1`). This is not the BS.1770 Annex 2 FIR table.

Acceptance for a level match is **±0.1 LU**, the EBU Tech 3341 minimum requirement for integrated loudness. This tree is not an EBU-certified meter. `loudness_mismatch` is set when the remeasured gated loudness is non-finite or farther than 0.1 LU from -20. `gain_limited_by` is `true_peak` when the ceiling, rather than the loudness target, selected the gain. `music-pref validate` records that as a warning and does not fail the dataset. The clip row is not rewritten. Exclude the clip from the primary level-matched analysis, or keep it in a separately identified condition.

One gain is applied. If absolute-gate membership changes after that gain, a dynamic excerpt can miss ±0.1 LU and is flagged. There is no iteration.

## Identity

`preprocessing_sha256` is the SHA-256 of canonical JSON for `preprocessing_document(profile)`. The fixture document is still channels, excerpt length, resample method, profile name, and sample rate. The gain document adds the downmix method, loudness method, true-peak method, target LUFS, ceiling, tolerance, and the ungated-gate fallback. Changing any of those changes the feature-cache key. The prepared waveform hash in diagnostics is `pcm_hash`: SHA-256 of contiguous little-endian float32.

Listening samples and the future encoder buffer are the same excerpt. `waveform_for_encoder` returns a contiguous float32 copy of those samples, shape `(480000,)`.

## CLAP handoff

No `AudioTextEncoder` signature change. `embed_audio` already takes `PreparedExcerpt`. Session 2B still must not put PyTorch or Transformers in this environment.

The adapter, when it is written, has to:

- call `waveform_for_encoder` and pass `sampling_rate=48000`
- reject any buffer that is not exactly 480,000 finite samples before the feature extractor
- pass `truncation="rand_trunc"` and `padding="repeatpad"` only after that assert; those processor defaults are not allowed to repair length
- read `pooler_output` from the model-output object into the existing `FeatureBatch` ndarray
- reject a brief over 512 tokens, including special tokens, with truncation left off; add that failure inside the adapter (`brief_too_long`). The protocol method list does not grow
- set `EncoderSpec.pooling` to `pooler_output`, `dtype` to `float32`, and `production_claim_allowed` to false until the probe gates pass

`music-pref validate` still refuses every encoder except `dummy` / `fixture-v1`. That matches the handoff's separate probe environment. A foundation config cannot name CLAP until a later session opens the gate.

Not incompatible, and not done here: the handoff's `nb_max_frames` note (expect 1001, do not force 1000), `weights_only` loading, or the 20-clip CPU probe. No weights were downloaded and no encoder ran.
