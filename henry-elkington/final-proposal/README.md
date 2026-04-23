# Final Project Proposal

## Project Overview

For our final project, we want to make a machine learning MIDI effect that can take a simple musical input as MIDI and expand it into fuller musical ideas. The core idea is to use MIDI tokenization to represent notes, rhythms in a form that a model can learn from, then use that model to generate related MIDI material.

The system would be designed as a Python script that could be run on any MIDI file, and also as a Max for Live device. It would be built with Python, PyTorch, MIDITok, and Max/MSP. The product we're aiming for is a MIDI effect that can sit inside a music production workflow and transform or continue MIDI in useful ways. For the final project, we will focus on a smaller prototype that proves the basic idea, sending MIDI into a model, generating new MIDI, and putting the generated notes into the the MIDI clip.

Possible musical tasks include:

- Adding a chord progression to a bassline
- Adding supporting chords to a melody
- Using chords and generating a melody or bassline
- Expanding a short MIDI phrase in a similar style
- Creating variations of an existing MIDI clip
- Enriching basic chord voicings
- Quantizing MIDI to sound more "human"

The final version that we present to the class may not include all of these modes. The minimum goal is to make one mode work clearly, such as melody to chords or bassline to chords.

## Why This Project Matters

Something interesting about this project is extending MIDI rather than making it from scratch, the collaborative process with the computer is a bit more interesting as a tool rather than maybe a method of outsourcing creative work. When using AI in creative endeavors, people either fall into avoiding it or overusing it. But if it can work in Ableton, the iteration cycle can be very fast and therefore actually useful in a composition workflow that isn't either of the extremes.

Some interesting topics that we want to learn:

- How to use MIDITok and how it represents symbolic music
- What models to use to train models that can do this
- How to train a model that generates useful musical structure
- How to connect a Python machine-learning workflow to Max/MSP and Ableton Live

The goal is to create a tool that isn't only used to make finished music, but is used as part of an interactive workflow where the user can edit and rerun the model on the same selection of MIDI.

## How Machine Learning Will Be Involved

The machine learning part of the project will focus on symbolic MIDI generation. MIDI data will be converted into tokens with MIDITok, similar to how text is tokenized for a language model. Then we will train and fine-tune a PyTorch model to predict or generate new musical tokens. After generation, the tokens will be converted back into MIDI.

The model does not need to be particularly large for this project. A smaller proof of concept model might be better for our timeline. We will need to look into transformers, LSTMs (and RNNs), and potentially also processes involving Markov chains. The most important part is whether the model can learn a musically useful relationship between one MIDI part and another, not whether it can generate an entire song from scratch.

## Data, Tools, and Workflow

### Data and Source Material

We plan to use MIDI files as the main source material. The dataset may include:

- Public MIDI datasets, such as pop, jazz, classical, or electronic MIDI collections
- Small hand-curated MIDI datasets

We will need to choose the data based on the first generation task. For example, if the goal is melody to chords, We need MIDI files where melody and harmony can be separated or inferred. If the goal is bassline to chords, We need examples where bass motion and chord progressions are both available.

Because the timeline is short, We will probably start with a small curated dataset and a narrow musical task. A smaller dataset that is clean and consistent may be more useful than a large dataset that is hard to parse.

### Tools and Platforms

Planned tools:

- Python
- PyTorch
- MIDITok or a similar MIDI tokenization library
- pretty_midi
- Max/MSP
- Ableton Live and Reaper

The main workflow will be:

1. Collect or create MIDI examples.
2. Clean the MIDI so the relevant parts are separated.
3. Save the MIDI dataset to be used.
4. Extract the features of the MIDI or make a pipeline to do so.
5. Get the piping in for a model.
6. Tune the model and mess with the hyper parameters until we find a good configuration.
7. Save the checkpoint.
8. Develop a Python script to run on midi files.
9. Make a Max device using the checkpoint to run on Ableton midi clips.
10. Attempt to use the tools to make a song to test them.

## Collaboration Plan

We will divide the project into two connected parts: the Python/model side and the Max/MSP/Ableton side. We will both add to the python model and the machine-learning pipeline, including MIDI cleaning, tokenization, training, and inference. The Ableton part is more of an aside that will not need to be focused on.

## Development Plan

### First Concrete Steps

Our first steps will be:

1. Choose one main generation task for the final prototype.
2. Make a small MIDI test set.
   - Create or collect 10-30 short MIDI clips.
   - Make sure each clip has the musical parts needed for the task.
   - Export or organize them into a consistent folder structure.
3. Test MIDI tokenization in Python.
   - Load a MIDI file.
   - Tokenize it.
   - Decode it back into MIDI.
   - Confirm that the reconstructed MIDI still sounds correct.
4. Build a simple generation bassline.
   - Before training a neural model, create a simple rule based version or statistical bassline.
   - This gives us something to compare the model against and makes sure the MIDI pipeline works.
5. Train a small PyTorch model.
   - Start with a small model that can overfit a tiny dataset.
   - Confirm that training, saving, loading, and generation all work.
   - Then test whether the model can generalize to new input clips.
6. Connect the model output to Max/MSP.
   - Start by loading generated MIDI files into Max or Ableton.
   - Then test a more interactive connection, such as Max sending MIDI data to a Python script and receiving generated MIDI back.

## Goals

The expected final deliverable is a prototype MIDI co-composition system. At minimum, it will include:

- Python code for MIDI tokenization and generation
- A trained PyTorch model
- Example input and output MIDI clips
- Documentation explaining the process, problems, and results

The project will be successful if we can show that a short MIDI idea can be transformed into related musical material through a machine-learning workflow, even if the final interface is still experimental.

## Stretch Goals

If the basic system works, possible stretch goals include:

- Multiple generation modes, such as melody to chords and chords to bassline
- A Max/MSP interface with controls for temperature, variation, phrase length, and regenerate
- Real time or near real time generation from incoming MIDI
- Style controls, such as simple, dense, dark, bright, rhythmic, or sparse
- A short finished musical piece made using the tool

## Questions, Concerns, and Risks

### Technical Questions

- What MIDI tokenization format is best with which model?
- How should the system represent chords vs melody vs basslines?
- Should the model generate one bar at a time, a full phrase, or a fixed number of tokens?
- How much data is enough for a meaningful prototype without overfit?
- What is the most practical way to connect a PyTorch model to Max/MSP?
- Should inference happen inside Max, through Python, through Node for Max, or through an exported model format?

### Risks

- Training a model from scratch may take too long or require more data than expected.
- MIDI datasets may be messy, with inconsistent tracks, tempos, and instrument labels.
- Generated MIDI may be technically valid but musically uninteresting.
- A full Ableton MIDI effect may be too ambitious for the final deadline.
