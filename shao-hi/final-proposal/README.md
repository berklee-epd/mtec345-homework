**ML Final Project Proposal**

## Why I'm building this

Whooshes, risers, and morphing sounds are everywhere in a lot of film and games — every fight scene, every camera move, UI transition etc. When I do sound design, a single whoosh usually require digging through sample libraries, layering and hand-automating filters to shape the energy over time. Most people would just find whooshes or impact on sfx library but still requires a lot of time serching for the right sound and most of the time still ends up layering different sfx.

Thats why I want to build a tool that works the way sound designers actually work: **open a labeled material pad, pick a spot between the tags, draw the energy shape, and iterate until it's right.**

## What it is (one sentence)

A **β-VAE** with a structured three-part latent bottleneck, trained on top of frozen EnCodec representations, with a 2D material pad pre-populated at training time by a fixed vocabulary of descriptive tags. I chose the VAE deliberately because it requires a navigable, interpretable latent space, and I think VAE would fits beat in this condition.

## The controls

Three layers, each a different part of the latent:

**1. A 2D material pad with built-in labels.** The pad comes pre-defined tags ("water," "metallic," "rough," "airy," etc.) placed at positions the model learned during training. Clicking near a label generates in that style; clicking between labels gives a blend weighted by proximity. Like mixing colors on a palette, except the palette comes with named pigments.

**2. Timbral sliders.** Around eight sliders for qualities the model discovers on its own (unsupervised disentanglement). Will name them post-hoc by running PCA on the learned dimensions and listening to what each controls and name them.

**3. Drawable curves over time.** The user draws two curves — overall energy and brightness — and the model follows them. Trained by regressing against RMS and spectral centroid envelopes extracted from each sample.

After generating, the user nudges any control and regenerates.


## Pipeline

Four stages. Each has defined inputs, defined outputs, and runs at a different time — so the project can be built, debugged, and resumed incrementally.

### Stage 1 — Preprocess (one-time, offline)

```
Raw audio  →  [resample 32 kHz mono, normalize to −23 LUFS, crop to 2s]
           →  [EnCodec encoder, frozen]  →  cached latents  (shape: 128 × 100)
           →  [librosa RMS + spectral centroid]  →  cached envelopes  (shape: 2 × 100)
           →  manifest.csv  (filename → latent_path, envelope_path, multi_hot_tags)
```

All caches written to Google Drive. After this stage, training never touches raw audio.

### Stage 2 — Train (iterative, on Colab)

```
Cached latents + envelopes + multi-hot tag vectors
       ↓
   [My VAE encoder]
       ↓ produces three latents:
   ├── z_material ∈ ℝ²     — supervised by multi-label tag vector (BCE)
   ├── z_timbre ∈ ℝ⁸       — β-VAE KL pressure for disentanglement
   └── z_time ∈ ℝ^(C×T)    — softly regressed against envelope ground truth (MSE)
       ↓
   [My VAE decoder]  →  reconstructed EnCodec latents
       ↓
   Loss = MSE reconstruction + β·KL terms + λ_mat·BCE + λ_env·envelope MSE
```

Two training phases:
- **Phase 2a — Material pretraining.** Train on a broad Foley corpus (including static, non-whoosh samples) so `z_material` organizes cleanly by the full tag vocabulary, uncontaminated by whoosh dynamics.
- **Phase 2b — Whoosh fine-tuning.** Fine-tune on the transitional subset (whooshes + risers) with `z_material` partially frozen, so the model learns time-varying shape while keeping the material structure.

Two augmentations during training:
- **Interpolation augmentation** — randomly blend `z_material` from pairs of samples so the decoder handles in-between points on the pad.
- **Envelope augmentation** — time-stretch and amplitude-modulate samples, recompute envelopes, train the model to match.

### Stage 3 — Analyze (one-time after training)

```
Trained checkpoint
       ↓
   For each tag: compute centroid of z_material across all training samples carrying that tag
       ↓  →  tag_positions.json  (tag name → 2D coordinate)
       ↓
   [PCA on pooled z_timbre across dataset]  →  principal axes of timbral variation
       ↓
   Synthesize traversals along each axis, listen  →  named sliders
       ↓  →  axes.json  (slider name → latent direction vector)
       ↓
   [Linear probe on z_material]  →  tag-level classification accuracy
```



## Technical Summary

**Architecture.** Frozen EnCodec 32 kHz mono for waveform ↔ latent conversion. A small 1D-convolutional VAE operates on EnCodec's continuous (pre-quantization) latents at ~50 Hz. Total trainable parameters ~5–15M.

**Loss:**
```
L = L_recon(MSE on EnCodec latents)
  + β · KL(z_material) + β · KL(z_timbre)
  + λ_mat · BCE(tag_heads(z_material), multi_hot_tags)
  + λ_env · MSE(envelope_heads(z_time), extracted_envelopes)
```
Starting hyperparameters: β = 1.0 (raised to 4.0 if disentanglement is poor), λ_mat = 0.5, λ_env = 0.1.

Multi-label BCE is used instead of cross-entropy because samples can carry multiple tags simultaneously (e.g., `metal + rough + bright`), and this richer supervision gives the 2D pad more meaningful structure than hard mutually-exclusive classes would.

**Post-hoc analysis.** Tag positions on the pad are computed as `z_material` centroids per tag. PCA over pooled `z_timbre` surfaces principal timbral axes, named by listening. Linear regression from `z_timbre` to acoustic features (spectral flatness, roughness) provides secondary attribute directions.

## References and reused components

I'm not building from scratch. I will reference following models to build the model.

**Used frozen (no training):**
- **EnCodec** — Défossez et al. 2022 ([`facebookresearch/encodec`](https://github.com/facebookresearch/encodec), via [`facebookresearch/audiocraft`](https://github.com/facebookresearch/audiocraft)). Waveform ↔ latent.
- **librosa / torchaudio** — envelope extraction, audio loading, resampling.
- **frechet-audio-distance** ([`gudgud96/frechet-audio-distance`](https://github.com/gudgud96/frechet-audio-distance)) — FAD evaluation.
- **sklearn** — PCA and linear-probe classifier.

- **RAVE** — Caillon & Esling 2021 ([`acids-ircam/RAVE`](https://github.com/acids-ircam/RAVE)). Closest conceptual relative: a VAE trained on audio with post-hoc latent analysis. I reference RAVE's encoder/decoder patterns and latent-analysis utilities, but write a smaller version suited to EnCodec latents.
- **Stable Audio Tools?** ([`Stability-AI/stable-audio-tools`](https://github.com/Stability-AI/stable-audio-tools), refactored [`yukara-ikemiya/friendly-stable-audio-tools`](https://github.com/yukara-ikemiya/friendly-stable-audio-tools)). Studied for config-driven training patterns and PyTorch Lightning training-loop structure.
- **β-VAE** — Higgins et al. 2017. Reference implementation: [`1Konny/Beta-VAE`](https://github.com/1Konny/Beta-VAE).



## Dataset

~5–10 hours of whooshes, risers, and Foley recordings from Freesound (Creative Commons) and the BBC Sound Effects Library (educational use). Each sample gets a multi-hot vector across the 18-tag vocabulary.

Tagging protocol: will utilize the tagging protocol in sfx library to speed up workflow.
## Evaluation

**Objective metrics:**
- Reconstruction quality (multi-scale spectral loss) on held-out samples.
- Envelope-following error (MSE + correlation between drawn and generated envelopes).
- Per-tag AP (average precision) from the tag classification heads — validates that the 2D pad actually organizes by label.
- Fréchet Audio Distance (FAD) against held-out whooshes.

**Subjective evaluation:**
- Axis interpretability study — 8–12 sound design / film students describe what changes when traversing each discovered `z_timbre` axis; measure inter-rater agreement.
- Pad navigability study — given a target description ("wet, airy whoosh"), can participants find it on the pad faster than in a sample library?

## Scope

**In scope:** dataset with tagging, two-stage VAE training, the three-part bottleneck, both augmentations, post-hoc analysis (tag centroids + PCA on timbre).

**Out of scope:**
- **User-uploaded reference samples on the pad.** The pad vocabulary is fixed at training time. Maybe future feature?
- **DAW plugin (Ableton, Max for Live).** Straightforward follow-up work.
- **Impacts.** Different temporal structure; separate project.


