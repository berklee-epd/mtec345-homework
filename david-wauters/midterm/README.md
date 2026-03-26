# Documentation - Tokenization and Musical Application

## What I did
My initial goal was to build a neural network that would generate melodies based on a dataset of melodies represented as MIDI files. This goal ended up being above my achieveable level of scope, and the amount of work involved in it was gradually growing in a direction which did not align with what I was most interested in for the project. Because of this, I had to adjust my end product significantly. In lowering the scope, I made my new goal to understand the concept of tokenization as it relates to encoding for music.

My first step was reading the tokenization section from Chapter 7 of [*Deep and Shallow, Machine Learning in Music and Audio*](https://www.taylorfrancis.com/books/mono/10.1201/9781003240198/deep-shallow-shlomo-dubnov-ross-greer) by Shlomo Dubnov and Ross Greer. This not only gave me a solid foundation in understanding tokenization, but it also led me to look into the documentation [MidiTok](https://miditok.readthedocs.io/en/latest/index.html), a Python package for tokenizing MIDI files. The textbook, as well as MidiTok's documentation, helped me gain a better understanding of tokenizations application specifically to music and MIDI encoding.

With this research, I then was able to put together a presentation where I could share my understanding of tokenization with my peers as it is not a concept we have touched upon in class yet. I additionally wanted to have a more concrete deliverable to help convey the concept, so using MidiTok I tokenized MIDI files of my own using the four different tokenization schemes that the chapter touched upon. This resulted in a final deliverable of two markdown files (one with the presentation and one with the tokens) as well as a small python file that serves as my tokenizer. With this deliverable I now feel I have a strong understanding of tokenization, which is a great first step in furthering my research on melody generation.

## How machine learning is involved
While no neural networks were used directly for this project, the concept of tokenization is a crucial step in the training of certain neural networks. In this project I chose to put my focus on the encoding process and how to do it the most efficiently for music and MIDI. By honing my knowledge on this aspect, I better understand how to create and encode a strong dataset that would work well for training a model in the most efficient way possible in terms of time, energy, and processing power.

## What I learned
Before doing thorough research for this project I was anticipating that I could just use one-hot encoding like we did in class to produce melodies. But by diving deeper into these topics, I was able to expand my knowledge on the different ways we can encode information. More importantly, I have a better grasp on what kind of encoding to use based on the project being developed. 

I now feel that I have a strong grasp of tokenization, how it differs from one-hot encoding (the only other form of encoding I knew before starting this project), and how it can be applied specifically to music, MIDI data, and melody generation. With this knowledge, I am now closer to being able to develop my own neural network that generates melodies for the final project if I want to continue in that direction.

## Reflection
A more concrete problem I faced was getting MidiTok to run properly, as one of the tokenization schemes was not running properly at first. It was an issue that I could not understand, and I likely would not have figured it out if I didn't run it by an AI assistant and learn that I had to downgrade a certain package for it to be compatible with MidiTok.

If it was not obvious enough, the biggest challenge was beginning with a scope that was too large. It would have made more sense to determine what my minimum viable product was, aim for that, and then see how much more ambitious I could get after that. Once I narrowed the scope and settled on something smaller, it was much easier to move forward with the project as I could actually see and formulate the next steps. Given that this project was mostly research based, it's harder to have expectations that could or could not have been met. However, I was fairly surprised to learn how much data actually lies within MIDI and how much could be parsed from it.


## Presentation notes
 Additionally for reference, here are the presentation notes that I made for myself. They elaborate on the bullet points in the tokenization-presentation.md file:
- tokenization is the process of converting musical information into smaller units called tokens
    - similar to one-hot encoding but not identical, essentially converting data we can understand into a format that a NN can understand
- chatgpt uses tokenization
    - letter tokenization: “charles holbrow is cool” = {c,h,a,r,l,e,s,o,b,w,i}
    - word tokenization: “charles holbrow is cool” = {charles, holbrow, is, cool}
    - take 10,000 tokens before it, what is the most likely token to come next

- way we tokenize musical data directly impacts what model can learn from data and what it can produce, certain kinds of music are easier to read in certain ways and will be less intense on GPU
- music sequences contain information beyond temporal dimension, also contains vertical relationship of notes, gets more complicated with bigger multi-track compositions
- music has more complex structure that gets even more complicated with expressiveness, absence of long-term structure in generated samples (ex. repetition & motivic content)
    - essentially the human/creative aspect of music, same reason LLMs can’t write amazing poetry
- inputting straight MIDI doesn’t work because network would have to learn MIDI formatting which has nothing to do with musical information, instead use MIDI to tokenize musical information

- four parameters to tokenize:
    1. pitch range: min + max pitch values (integers in MIDI)
    2. number of velocities: velocity levels 0 to 127 to quantize to
    3. beat resolution: sample rate per beat, ranges for which sample rate should be applied (ex. high resolution for short beats can improve precision)
    4. additional tokens: such as chord, rest (explicit time-shift event, more helpful over placing next note at later timestep), tempo

- MidiTok: Python pacakge, implements MIDI tokenization schemes:
    1. MIDI-Like: 413 tokens total, 128 note-on and note-off events (one per pitch), 125 time-shift events (8ms-1sec), 32 velocity events
    2. Revamped MIDI-Derived Events (REMI): uses note-on and note velocities, uses Note Duration instead of Note-off,  note represented by 3 tokens, arguably better for modeling rhythm, note duration is clearer than having to infer it by note-on and note-off tokens and recognize they appear in pairs
    3. Structured: tokens provided in order of pitch, velocity, duration, time shift. cannot accommodate rests or chords, so only useful in very specific cases.- not good for pieces with long rests because time shift has a certain maximum value
    4. Compound Word: an issue is events intended to be simultaneous but have to be provided as a sequence (ex. note-on instruction and note velocity are two sequential instructions, but they describe the same event). this is corrected here through super-tokens, tokens are independently embedded, after embedding they merge into a single super token (family, bar/position, pitch, velocity, duration, optional: program, chord, rest, tempo, time signature), better suited for larger models