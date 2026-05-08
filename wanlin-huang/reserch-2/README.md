# Research 2: Google Lyria Realtime — Wanlin

## Tool Overview

**Google Lyria Realtime** is a generative AI music model developed by Google DeepMind. It produces continuous, real-time audio output from text prompts, designed for interactive and live music generation.

The underlying technology is a **diffusion-based audio model** trained on a large dataset of music. Lyria generates audio directly in the waveform domain, meaning it does not produce MIDI or notation — it outputs rendered audio. The "Realtime" variant is optimized for low-latency, continuous generation, making it distinct from batch-style generators like Suno or Stable Audio Open.

---

## Why I Chose This Tool

I was interested in tools that generate audio directly from text, especially for **ambient and experimental** music where texture, space, and atmosphere matter more than melody or rhythm. Rather than using an existing interface, I built my own web app using the **Gemini API with Lyria Realtime** as the backend. This gave me direct access to the model's parameters:

- **BPM** — tempo control
- **Density** — how busy or sparse the generated texture is
- **Brightness** — tonal color from dark to bright
- **Temperature** — how random/unpredictable the model's output is
- **Key** — tonal center (or Auto key)
- **Multi-track** — run multiple Lyria sessions simultaneously, with Tempo and Key sync between tracks

The interface also supports real-time recording and download. Having control over **Temperature** was especially important for experimental music — higher values made the output less predictable, but also harder to steer. This tension between control and unpredictability became a central theme of my research.

---

## Research Process & Experimentation

### Approach

My prompt strategy was inspired by **granular synthesis** and **drone music** — two techniques central to experimental ambient work. Instead of describing music in genre terms (e.g., "ambient electronic"), I wrote prompts as **sonic images**: describing texture, register, movement, and emotional quality in physical or visual terms.

I organized my prompts into four categories:

### Category 1: Granular Textures
Prompts focused on fragmented, frozen, or dissolved sound objects.

| Prompt | Notes |
|--------|-------|
| `granular ice crystals suspended mid-air, slowly rotating, no attack, ethereal` | Good results — airy, no transients, worked well |
| `granular breath clouds, inhale frozen in time, diffuse, weightless, haunting` | Output felt slightly too "musical" — subtle melodic drift appeared |
| `shattered string harmonics, granular freeze, upper register, cold shimmer` | Strong shimmer quality, somewhat consistent |
| `piano keys dissolved into dust, granular haze, no rhythm, surreal` | Rhythm still crept in; "no rhythm" instruction partially ignored |
| `granular water droplets stretched to infinity, morphing, aquatic, meditative` | Meditative quality achieved; morphing transitions were smooth |
| `fractured voice grains, unrecognizable, slowly drifting, uncanny, abstract` | Uncanny effect good but brief — model tended to stabilize quickly |

### Category 2: Dissolving Tones
Prompts focused on decay, filtering, and slow transformation.

| Prompt | Notes |
|--------|-------|
| `slowly dissolving bell tones, long decay trail, mid shimmer, no pulse` | Closest to target — long tail, no obvious beat |
| `texture melting from bright to dark, filter falling, cinematic, slow` | Cinematic quality present; slightly generic |
| `warm pad dissolving at edges, unstable harmonics, fading in and out` | Unstable harmonics not very pronounced; came out smoother than expected |
| `metallic shimmer morphing into fog, high to low, evolving, dreamlike` | Dreamlike quality good; high-to-low movement was subtle |
| `organ tone slowly losing pitch, dissolving into noise, haunting, slow` | One of the stronger results — disintegration texture felt intentional |

### Category 3: Drone & Detuning
Prompts targeting harmonic beating, tuning instability, and sustained tones.

| Prompt | Notes |
|--------|-------|
| `two sine waves slightly detuned, slow beating frequency, hypnotic, vast` | Beating effect present but subtle; model smoothed the detuning |
| `analog oscillator drift, root E, warm, slightly unstable, meditative` | Warm and slow — worked as expected |
| `chorus of detuned strings, no melody, dense, slowly breathing, heavy` | Melody appeared anyway; "no melody" instruction was inconsistently followed |
| `bowed glass drone, microtonal clusters, eerie, no rhythm, spectral` | Eerie and spectral — one of the best results |
| `three layered drones, each slightly off pitch, beating together, trance-like` | Trance-like quality achieved; actual beating was indistinct |
| `cello harmonics drone, root D, raw, no vibrato, stark, monolithic` | Raw quality mostly achieved; no vibrato held |

### Category 4: Noise & Degraded Signal
Prompts targeting texture from noise, artifacts, and degraded media.

| Prompt | Notes |
|--------|-------|
| `vinyl crackle over silence, warm noise floor, intimate, nostalgic` | Warm and intimate — felt familiar/safe |
| `degraded cassette hum, warped, lo-fi warmth, slightly distorted, aged` | Lo-fi texture present; warping effect mild |
| `shortwave radio static, faint signal beneath noise, distant, lonely` | Lonely quality came through well |
| `old television white noise, high frequency hiss, analog warmth, fading` | High-frequency hiss accurate; "analog warmth" contradicted it slightly |
| `telephone line hum, 60hz buzz, industrial, dry, claustrophobic` | Claustrophobic feel — good result, very dry |
| `corrupted digital signal, bit-crushed artifacts, cold, glitching slowly` | Cold and glitchy — one of the stronger results in this category |

---

## Key Observations

### Strengths
- Lyria handles **broad atmospheric qualities** well: "ethereal," "haunting," "dreamlike," "meditative" came through consistently
- **Decay and shimmer textures** were generally accurate
- Prompts involving **specific physical imagery** (ice, fog, glass) produced more interesting results than abstract genre labels
- **Noise and degraded signal** category worked well — these are simpler tonal targets

### Weaknesses
- **Specificity is difficult**: Prompts like "root E," "60hz buzz," or "microtonal clusters" were interpreted loosely. The model averages toward a generalized version of the style
- **"No rhythm" / "no melody" instructions were inconsistently followed** — the model has a bias toward musical coherence
- **Detuning and beating effects were subtle** — the model seemed to smooth out dissonance
- **Styles converge toward the mean**: This was the most important finding. Even with detailed, specific prompts, outputs often sounded like a generic "ambient" track rather than something distinctly experimental. The model produces what ambient music is *expected* to sound like, not the edge cases I was describing

---

## Reflection

The central tension I encountered is that **AI music models are trained on what exists, so they reproduce what is typical**. Experimental music — by definition — resists typicality. When I asked for "fractured voice grains, unrecognizable, slowly drifting," the model produced something recognizable, listenable, and safe.

This is not necessarily a failure of Lyria specifically. It reflects a structural challenge: the training distribution shapes the output space, and highly specific or marginal aesthetics are underrepresented in that distribution.

What I found useful was treating the model as a **starting point or texture source** rather than a compositional agent. The outputs became more interesting when I stopped trying to get the model to produce a finished idea and instead used what it generated as raw material to react to.

**If I were to continue this project**, I would use Lyria's outputs as source audio and process them further — granular synthesis, spectral freezing, heavy filtering — to push toward the textures the prompts were describing but the model couldn't fully reach on its own.

---

## Final Composition

The composition uses four Lyria-generated audio segments selected from the experiments above, chosen for textural contrast:
- Segment 1: `organ tone slowly losing pitch, dissolving into noise` (Category 2)
- Segment 2: `bowed glass drone, microtonal clusters, eerie, no rhythm, spectral` (Category 3)
- Segment 3: `corrupted digital signal, bit-crushed artifacts, cold, glitching slowly` (Category 4)
- Segment 4: `slowly dissolving bell tones, long decay trail, mid shimmer, no pulse` (Category 2)

  > 🎵 Audio file: [Lyria.mp3](./Lyria.mp3) (final composition mix)

---

## Sources

- Google DeepMind, Lyria: https://deepmind.google/discover/blog/transforming-the-future-of-music-creation/
- YuE (original research context): https://github.com/multimodal-art-projection/YuE
- AI Song Contest reference: https://www.aisongcontest.com/