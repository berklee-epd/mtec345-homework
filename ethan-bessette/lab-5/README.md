# Lab 5: Symbolic Music Algorithm Documentation
Ethan Bessette

## The Process

### Description
This algorithm will convert dice-based algorithmic composition into musicxml files that can be interpreted by score prep software such as MuseScore. It will use a dice-based system that I designed a few years ago. I will convert this system into something that can be generated in Python.

### Pseudocode
1. Look up python libraries for generating musicxml files
2. Using ChatGPT, ask questions to understand the library
3. Write code to set up score: tempo, key signature, time signature)
4. Write an add note function that ties planned algorithm to the library methods
5. Write code to concatenate notes and apply formatting before exporting to musicxml
6. Open in MuseScore, convert to audio.

The algorithm:

![Figure 1](Figure1.png)


#### Translation of algorithm
Duration:
- d4, then
- d12. If 1-5, nothing. If 6-12, d4 * 0.25

Rest:
- d6, if 1, rest

Pitch:
- pitch of middle line +-:
- 50/50 whether add or subtract exploding d8
- d8. if d8, do another d8 (exploding)

Articulation:
- d20. Based on result, add a different articulation or ornament


### LLM Prompts and My Summaries of Responses
1. Are there any python libraries for generating musicxml files
    - music21
2. Using music21, show an example of how to set up a score (tempo, key signature, time signature). How do I add articulations? Can I define custom articulations using strings? Then, make an example of adding notes with different rhythms, including notes tied across barlines.

```python
from music21 import stream, tempo, meter, key, note, articulations, duration

# Create a Score and a Part
score = stream.Score()
part = stream.Part()

# Set tempo (e.g., 120 quarter notes per minute)
tempo_mark = tempo.MetronomeMark(number=120)
part.append(tempo_mark)

# Set key signature (e.g., G major)
key_sig = key.KeySignature(1)  # 1 sharp = G major / E minor
part.append(key_sig)

# Set time signature (e.g., 4/4)
time_sig = meter.TimeSignature('4/4')
part.append(time_sig)

# Create a note
n1 = note.Note("C4", quarterLength=1)

# Add an articulation (e.g., staccato)
n1.articulations.append(articulations.Staccato())
```
3. can music21 automatically tie notes across barlines if their length exceeds the current length of the bar?

    "This is done by using the makeMeasures() method on a stream (like a Part or Score) that contains notes with durations longer than a single measure."
    
    - this is wrong:

```python

# Create a Part and set time signature
part = stream.Part()
part.append(meter.TimeSignature('4/4'))

# Add a note longer than one measure (e.g., a whole note + a quarter note = 5 quarter lengths)
long_note = note.Note("C4", quarterLength=5)
part.append(long_note)

# Before making measures, the note is one long note
print("Before makeMeasures:")
for n in part.notes:
    print(n, n.quarterLength, n.tie)


# Automatically split into measures with ties
measured_part = part.makeMeasures()
```
4. What python version is best for music21?
- Im going to try python 3.8


### Programming

File: main.ipynb

#### Environment Setup
```zsh
uv python pin 3.8
uv init
uv add music21
uv sync
source .venv/bin/activate
```

#### Score setup
LLM questions:
5. how to set clef from string
6. how to get pitch of middle line of current part based on clef
   - it was wrong. did it myself by manually mapping clefs to midi numbers and storing them as an attribute in each part


After this, I followed the pseudocode translation of the algorithm.


#### Issues
- the glissandos don't work
- I had trouble with creating parts based on how many parts requested and values of dictionaries, but I figured it out
- the easiest way I found of passing in the correct middle note number for each part was to save it as an attribute in each part to pass in to the makenote()
- re-downloading musescore sounds was a pain, but annoyingly Dorico doesnt play back mordents and turns, so I "had" to


### Outcome
I'm happy with this. I feel like I translated my original dice algorithm decently well, and although there are a few things that didn't map, it still is satisfying. I didn't modify the generated score or audio. The score has some notes out of range of the instruments, although it doesn't matter as they simply weren't played in the wave file.

The wave file can be found [here](https://drive.google.com/file/d/1N9sTQENGNsfmfghs5cX6Zt5s--XaZn-e/view?usp=sharing).
