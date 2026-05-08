# MTEC-345 Final Project

## What I Built

For my final project, I built a neural network controlled synthesizer called **CrazySynth** in SuperCollider. This project combines a chaotic feedback synth with a machine learning system using FluCoMa’s `FluidMLPRegressor`.

The synth has:
- 10 sliders that control different sound parameters
- an XY pad for machine learning control
- buttons for collecting data, training the model, and saving/loading everything

The sounds range from more stable tones to noisy and unpredictable textures. The main idea of the project was to make a synth that could be controlled in a more simple and expressive way using machine learning instead of manually adjusting 10 sliders all the time.

[Here's a track made with the synth!](https://drive.google.com/file/d/1mRnrpRNJTGGfdU9jo4Oy5GzgJsmT1GIW/view?usp=sharing)

---

## How Machine Learning Is Involved

Machine learning is used to connect the XY pad to the synth parameters.

Basically, I first created the sounds using the sliders and assigned those sounds to the positions on the XY pad. Every time I click **Add Points**, the system stores:
- the XY position
- the current slider values

After collecting enough examples, I trained the neural network using `FluidMLPRegressor`.

Once the model is trained, moving the XY pad will make the neural network predict new synth parameter values in real time. Instead of controlling 10 parameters directly, I can create the soundscape just by moving through the XY pad.

The interesting part is that the neural network can also interpolate between training points. So, moving between two sounds can create in-between sounds that were never manually programmed.

---

## How I Implemented the Project

The project was built in SuperCollider using FluCoMa.

I used:
- `MultiSliderView` for the 10 synth controls
- `Slider2D` for the XY controller
- `FluidDataSet` for storing training data
- `FluidMLPRegressor` for the machine learning model
- buffers to pass data between the GUI and the synth

The synth itself uses:
- 2 sine oscillators
- feedback loops with `LocalIn` and `LocalOut`
- `MoogFF` filters
- `FluidLoudness` analysis to make the oscillators affect each other dynamically

The sound is intentionally chaotic. The oscillators are feeding back into themselves, and the loudness of one oscillator will affect the filter behavior of the other one. This can create an unstable and evolving textures.

I also added buttons for:
- adding training points
- saving/loading datasets as JSON files
- training the model
- saving/loading the trained MLP
- toggling prediction mode on and off

---

## What the 10 Parameters Control

```supercollider
val[0] → Feedback modulation amount (osc1 pitch chaos)
val[1] → Base pitch offset (osc1 tuning)
val[2] → Amplitude / loudness (osc1)
val[3] → Filter modulation depth (osc2 loudness → osc1 filter)
val[4] → Filter resonance (osc1)

val[5] → Feedback modulation amount (osc2 pitch chaos)
val[6] → Base pitch offset (osc2 tuning)
val[7] → Amplitude / loudness (osc2)
val[8] → Filter modulation depth (osc1 loudness → osc2 filter)
val[9] → Filter resonance (osc2)
```

---

## What I Learned

One big thing I learned is that machine learning in music is less about “accuracy” and more about whether the system feels expressive or interesting to play.

At first I thought the goal was just to get the lowest loss value possible, but while testing the synth I realized that sometimes a slightly less accurate model actually sounded more musical or created more interesting transitions.

I also learned a lot about how SuperCollider handles communication between the language side and the audio server side. Using buffers, datasets, and real-time prediction helped me better understand how FluCoMa works internally.

Another thing I learned is how sensitive feedback systems are. Small parameter changes can completely change the behavior of the synth, which made the training data really important.

---

## Reflection: Challenges, Unfinished Work, and What I Would Change

One of the biggest challenges was debugging everything related to saving/loading datasets and the MLP model. I had several issues caused by variable naming and accidentally saving multiple things to the same JSON file.

Another challenge was understanding how to organize the training data. Since the XY positions and synth parameters need matching IDs, I had to carefully manage how points were added to the datasets.

The synth itself is also difficult to control because it is intentionally chaotic. Some slider combinations sound great, while others completely explode into noise. That unpredictability is part of the project, but it also makes training more difficult.

Right now the project works, but there are still things I would improve:
- cleaner GUI design
- labels for all sliders
- better organization of parameter groups
- more curated training examples
- smoother sound transitions

If I had more time, I would also like to connect the system to a physical controller or use motion tracking instead of just the XY pad. I think the project could become a much more performable instrument with a more expressive interface.