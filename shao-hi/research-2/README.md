# Research Work Phase 2 — AI Tool Review

## Project Goal

Use both commercial and open-source AI tools to create something not commercial and push against the aesthetic defaults baked into these models.

## Tools Used

| Tool | Role |
|---|---|
| **Magenta Studio** (Google) | Generate random melodies, MIDI notes, and drum patterns |
| **RAVE** (custom-trained model, in Max/MSP) | Real-time audio generation / style transfer using my own dataset |
| **vschaos2** (in Max/MSP) | Neural audio synthesis and sample exploration |
| **Suno** | Commercial AI music generation — fed raw exports + text prompts |

## Process

### 1. MIDI & Pattern Generation (Magenta Studio)

Used Magenta Studio's plugins to generate randomized MIDI melodies and drum patterns. These served as the raw compositional skeleton — no manual note editing, just generation and selection.

### 2. Audio Generation (RAVE + vschaos2 in Max/MSP)

Ran my **custom-trained RAVE model** (trained on my own dataset) alongside **vschaos2** (pretrained folder https://www.dropbox.com/scl/fo/6th53cqxmpf106jj84usk/AFd9AYaZ3fuYBsGHtzPgWAg?rlkey=auvetbzxc89kv1uzvl7u3kc4n&e=1&dl=0)inside Max/MSP. Explored  for a while until I found  samples and textures. Applied additional processing to shape the results.

### 3. Assembly (Ableton Live)

Brought everything together in Ableton:
- Magenta-generated MIDI notes driving virtual instruments
- RAVE / vschaos2 audio samples layered on top

At this stage the material was still very **raw and unpolished** — intentionally.

### 4. Suno (Commercial AI Generation)

Exported the raw Ableton session and fed it into **Suno** along with text prompts. The goal was to see how a commercial model would interpret and reshape experimental source material.

## Key Finding: Fighting the Default Aesthetic

**The core challenge:** No matter what I fed Suno, the output kept gravitating toward **Synthwave**. The commercial model has strong stylistic biases — it wants to make things sound polished and genre-conforming.

I iterated through many different prompts, trying to push the output toward more **extreme, experimental** territory. Each round I adjusted the language to be more specific and aggressive about avoiding conventional song structure and production aesthetics.

This back-and-forth — trying to make a commercial tool produce non-commercial results — became the central experiment of the project.

## Reflections

- **Magenta Studio** — Good for generating raw MIDI material quickly. Strengths: randomness, speed. Weaknesses: output is musically "safe," needs heavy curation.
- **RAVE** — Most creatively interesting tool in the chain. Custom-trained models give unique results that don't sound like anything else. Steep learning curve.
- **vschaos2 in Max** — Useful for exploration and happy accidents. Works best as a sample-finding tool rather than a compositional one.
- **Suno** — Powerful but opinionated. It excels at producing commercial-sounding music, which is exactly what I was trying to avoid. Interesting as a study in model bias — the training data strongly shapes what it "wants" to make.
- **Overall insight:** Commercial AI music tools optimize for broad appeal. Using them for experimental work requires actively fighting their defaults, which is itself a creative process worth documenting.

## Underlying AI/ML Technology

- Magenta Studio
- RAVE 
- vschaos2
- Suno

## Song link
https://drive.google.com/file/d/1GOiq5Jimjw3a_HS0lVw6Wx9Kwm-1Mb4z/view?usp=sharing
