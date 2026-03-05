# Midterm Proposal

## What you would like to do
I would like to build a neural network similar to the one we did in class to predict chord symbols, but instead of chord symbols it would produce notes for a melody. From that, I will produce a set of melodies to be used in a set of short music composition. These compositions will have differing levels of human involvement. Some will not have the melody altered at all while for some I will alter the melody it produces. I may also write a piece that is inspired by the produced melodies but does not directly use them.

## How you will do it
I will likely begin with the Python neural networks we used in class to predict chords, adjusting them as necessary to instead work for predicting melodies. For an initial dataset, I plan to use the [Billboard Melodic Music Dataset](https://github.com/madelinehamilton/BiMMuDa) (BiMMuDa). This dataset consists of MIDI files, and so I will make use of a Python library (potentially [Mido](https://mido.readthedocs.io/en/stable/) or [pretty-midi](https://pypi.org/project/pretty-midi/#description)) to convert the MIDI into text data that can then be encoded into the neural network. From there I will tweak the neural network until it produces promising results which I can then use for the human composition part of the project.

## Questions, concerns, and stretch goals
- Similar to the chord progression neural network, there is a worry that it will produce melodies that are "correct" but don't make any actual musical sense. If I really cannot make decent sounding melodies after extensive tweaking then that's okay too cause I can just blame the quality of the compositions on the neural network.

- The BiMMuDa consists of the top 5 songs every year from 1950-2024, so there are 370 songs. A concern I have is that this is not a big enough dataset, but I will have to test and see if that is the case. If it does prove to be a problem, I will see if I can find another dataset to add to the model's training. The only issue there is I will have to make sure there's no repeating songs between the datasets.

- A stretch goal I have would be to take a less popular artist/band that I am fond of and transcribe a collection of their melodies and feed it to the neural network to see if it can produce a melody that sounds like that artist. This is a stretch goal because it's not likely that I'll have time to complete it, as I would have to manually transcribe as many melodies in a short amount of time. Converting them to MIDI will not be an issue as music notation software allows you to export the file as MIDI.

- If the model can produce successful and logical melodies then I may even try to train the model on specific years and see how the melodies might differ, but I can also see an issue occurring here where the datasets become smaller when you focus on specific years.
