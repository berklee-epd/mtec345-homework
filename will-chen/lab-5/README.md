# MTEC-345 Lab 5: Symbolic Music Generation

## Overview
This project is about algorithmic music generation using Csound. I built a system of modular `.csd` instruments that generate sound through procedural synthesis, parameter modulation, and randomness. Each element in the track was created as an individual `.csd` file and rendered separately. These generated sounds were later arranged and processed in Logic to create a complete piece of music.

---

## Sound Design (Synthesis & Signal Flow)

The first part of the project is sound design. Each `.csd` file defines an individual instrument using oscillators, filters, and envelopes to shape the timbre over time.

#### Example 1: Envelope + Oscillator (Kick / Bass)

```csound
aenv  expseg 1, 0.01, 0.3, 0.2, 0.001
afreq expseg 100, 0.02, 40

asig oscili aenv, afreq, 1
out  asig
```

#### Example 2: Filtered Oscillator (Pad / Synth)

```csound
asig  oscili 0.3, 220, 1
afilt moogladder asig, 2000, 0.7

out afilt
```

---

## Algorithmic Variation (Randomness & Modulation)

The algorithmic aspect of the project comes from adding controlled randomness and time-based modulation, which prevents repetition and creates evolving textures.

#### Example 1: Noise Generation (Hi-Hat / Snare)

```csound
anoise rand 1
aenv   linseg 1, 0.05, 0

out anoise * aenv
```

#### Example 2: Random Parameter Selection

```csound
irandFreq random 200, 400
asig oscili 0.2, irandFreq, 1

out asig
```

---

## Score Control (Structured Musical Input)

Although much of the project is generative, some elements such as the bass lines and structured sections are controlled using the **Csound Score section**.

#### Example 1: Basic Note Event

```csound
i1 0.00 1.00 1.00 06.00
```

#### Example 2: Repeated Events with Variation

```csound
i1 0.00 0.50 1.00 06.00
i1 +    .    .    06.02
i1 +    .    .    06.04
```
---

## Csound Files

- [`Kick.csd`](CsoundFiles/Kick.csd) – synthesized kick drum using pitch envelope  
- [`Snare.csd`](CsoundFiles/Snare.csd) – noise-based snare with filtering and envelope shaping  
- [`Hi-Hat.csd`](CsoundFiles/Hi-Hat.csd) – high-frequency noise percussion  
- [`Boom.csd`](CsoundFiles/Boom.csd) – low-end impact  
- [`SubBass.csd`](CsoundFiles/SubBass.csd) – sub-frequency bass layer  
- [`IntroBass.csd`](CsoundFiles/IntroBass.csd) – distorted bass 
- [`LeadBass&BassRiser.csd`](CsoundFiles/LeadBass&BassRiser.csd) – bass with modulation and riser effect  
- [`PadLow.csd`](CsoundFiles/PadLow.csd) – melodic pad
- [`PadHigh.csd`](CsoundFiles/PadHigh.csd) – melodic pad with modulation 
- [`PingPongSynth.csd`](CsoundFiles/PingPongSynth.csd) – stereo synth element  
- [`Riser.csd`](CsoundFiles/Riser.csd) – evolving transition effect  

---

## Editing and Post-Processing

After generating the audio files in Csound, I edited and processed them in Logic to create a more cohesive composition.

This included:
- rendering each `.csd` file into separate `.wav` files  
- selecting the most musically effective generated parts  
- trimming and arranging audio clips into a structured timeline  
- layering different elements, process, mix, and master 

Because many sounds were generated using randomness and modulation, each render could produce a slightly different result. The editing process was here to help transform the raw generated material into a more intentional and structured piece while preserving the algorithmic characteristics.

---

## Final Composition

[Listen](https://drive.google.com/file/d/1DSwun3UkWMhu4lwbIF6UpgmM0wKLZ2Vw/view?usp=sharing)

---