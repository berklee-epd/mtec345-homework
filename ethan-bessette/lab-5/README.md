# Lab 5: Symbolic Music Algorithm Documentation
Ethan Bessette

## The Process

### Description
This algorith will convert dice-based algorithmic composition into musicxml files that can be interprested by score prep software such as MuseScore. It will use a dice-based system that I designed a few years ago. I will convert this system into something that can be generated in Python.

### Pseudocode
1. Look up python libraries for generating musicxml files
2. Using ChatGPT, ask questions to understand the library
3. Write code to set up score: tempo, key signature, time signature)
4. Write an add note function that ties planned algorithm (see Figure 1) to the library methods
5. Write code to concatenate notes and apply formatting before exporting to musicxml
6. Open in MuseScore, convert to audio.

![Figure 1](Figure1.png)

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
#### Environment Setup
