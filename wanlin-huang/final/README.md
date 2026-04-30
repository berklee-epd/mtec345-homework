# SynthPlay
Final Project Proposal · Machine Learning for Music

## What I want to make

I want to make a browser-based music game that you control with a PS5 DualSense controller. Different buttons, sticks, and triggers will control different parts of a live synth sound. The main idea is to bring together all the AI tools I have been using this semester and see what happens when each one is doing the thing it is actually good at, instead of just using them separately like I have been doing.

## Why this project matters to me

This semester I used a lot of different tools but always kind of separately — Suno for music, writing code with Cursor. I never really tried to combine them into one thing that actually works together. I am curious what a project looks like when you treat each tool as having its own strength instead of just asking everything to do everything.

I also think it is interesting to make music that feels personal. Most music games just ask you to follow something. I want to make something that listens to how you play and responds to you specifically.

## The controller — PS5 DualSense

The PS5 DualSense connects to the laptop over USB or Bluetooth and the browser picks it up automatically through the Web Gamepad API — no drivers needed. Here is how I am planning to map the inputs to sound:

| Input | Sound parameter |
|---|---|
| Left stick | pitch / melody |
| Right stick | filter / texture |
| L2 / R2 (analog) | reverb / volume |
| × ○ □ △ | trigger synth hits |
| L1 / R1 | switch sound layer |
| D-pad | switch scale / key |

L2 and R2 are especially useful because they have analog pressure — so instead of just on/off, you get a continuous value from 0.0 to 1.0 which maps well to audio parameters.

## How machine learning is involved

I will use Wekinator as the ML part. It takes the gamepad input — stick positions, which buttons are pressed, how hard the triggers are held — and classifies them into different playing styles in real time. I train it by showing it examples myself: playing aggressively, playing slowly, playing rhythmically, just exploring randomly. This is basically how Wekinator is supposed to work — you teach it by demonstrating, not by writing a model from scratch.

Once it is trained, the style label it outputs controls the rest of the system: which Suno loop is playing, what the synth sounds like, and what ElevenLabs says. So the music changes based on how I play, not based on a fixed script.

## Tools and what each one is good at

- **Wekinator** — real-time interactive ML. Takes live gamepad data and classifies it into style groups based on my own demonstrations, no need to write the model by hand
- **Suno** — generating music from text. I will write prompts to generate four loops that sound clearly different from each other, one for each style the ML detects
- **ElevenLabs** — ElevenLabs — sound design. A friend recommended it for generating custom sound effects and audio textures. I plan to explore what it can do and use it for some part of the sound design, not totally sure yet exactly how.
- **Tone.js + Gamepad API** — low-latency browser audio. Handles the real-time synth control in the browser driven by whatever Wekinator outputs
- **Cursor** — writing and editing code fast. I will use it to write the browser game code and the Node.js bridge script
- **Claude** — thinking through problems. Helps me figure out the system design, debug things when they break, and write documentation

## First steps I will take

1. Connect the PS5 controller to the browser and log all the axes and button values on screen to make sure everything is reading correctly
2. Write a small Node.js script that receives gamepad data over WebSocket and forwards it to Wekinator as OSC
3. Demonstrate four different playing styles in Wekinator and train the classifier
4. Generate four synth loops in Suno with prompts that try to make the styles sound as different as possible
5. Connect Wekinator's output to Tone.js and the loop switching logic in the browser
6. Record a few ElevenLabs voice lines and trigger them when the style changes
7. Design a simple visual interface and test the whole thing from start to finish

## Questions, risks, and stretch goals

**Risks:**
- The Node.js WebSocket to OSC bridge is the most uncertain part — I have not done this before and not sure how long it will take to get working
- How many examples does Wekinator need to actually classify well? Will four styles be too many or is that fine?

**Stretch goals:**
- Compare the ML classifier against a simple rule-based version to see if training it actually makes a difference