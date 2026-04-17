# Drone piece


I create a ambient piece using `symusic`. The piece layers three voices — a slow-shifting drone, staggered pads, and a wandering flute melody — all drawn from the E Dorian mode over an 80-bar span at 60 BPM.

## Concept

I wanted to make something that felt like weather rather than like a song. No real downbeats, no arrival, no hook — just a slowly changing harmonic field with a melody drifting across the top. The algorithm is built to produce pieces in that aesthetic: every generative choice pulls toward stasis, proximity, and overlap rather than toward contrast or development.

## Algorithm

The score is assembled from three independent layers that share only the key and the total length. They don't listen to each other — any alignment between them is coincidental, which I think is part of why the texture stays interesting across 80 bars.

### 1. Drone

The drone picks a pitch from `{E2, B2, E3}` (root, fifth below, root), holds it for a random 8–16 bars, then picks again. With 40% probability it layers a perfect fifth on top at slightly lower velocity, which creates those moments where the harmonic foundation thickens without any rhythmic event marking the change. Velocities are randomized per note in the 40–65 range so the drone breathes rather than sitting at a fixed volume.

### 2. Chords

The chord generator is a simple Markov chain over five chords in E Dorian: `i (Em7)`, `ii (F#m7)`, `IV (A7)`, `v (Bm7)`, and `VII (Dmaj7)`(usually used to embody the dorian sound). Each chord has a weighted transition table to every other chord — for example, from `i` the next chord is `IV` 35% of the time, `VII` 30%, `v` 25%, `ii` 10%. The weights were tuned by ear to favor motion that sounds modal rather than functional (lots of `i ↔ VII` and `IV ↔ v`, very little `ii → V → I` cadential pull).

Each chord lasts 4–8 bars. Within a chord. each pitch enters up to half a beat after the previous one. This is the single most important detail in the whole piece: it turns block chords into something that sounds like a pad slowly crystallizing, and it means two adjacent chords blur into each other at their boundary instead of changing cleanly.

### 3. Melody

The melody uses a **proximity-weighted random walk** over the E Dorian scale across two octaves. Given the previous pitch, the next pitch is chosen with weights proportional to `1 / (1 + |candidate − previous|)`, so small intervals are far more likely than large ones but leaps remain possible. This produces lines that feel sung rather than random — they move mostly by step, occasionally skip, and rarely jump.

### 4. Production 
Finally I export the stems and bring it into ableton and add a reverb on it and some finish touches on the piece.