# Final

This is the final project that David and I did. It's two MIDI tools that you can use on MIDI. The integration with Ableton was stopped pretty quick after I found an issue with the Ableton Max for Live integration. Another issue was the synchronization part of the code.

## What you made or built

We made 2 MIDI transformers that would take MIDI and edit the MIDI in some way, hopefully synergizing with each other to help with the workflow of creating and editing MIDI when it comes to composition and songwriting. It's less of a complete product and more of a proof of concept that would need to be researched further. The idea is to figure out how to make MIDI transformers that are at least adequate at their job, and then we can start adding more transformers and improving the quality of the first ones. After this, we would integrate them into Ableton Live so you could directly call them from Live rather than having to use an external tool.

What we ended up making was two examples at opposite ends of the spectrum of types of transformers we would want to make. The first one is a simple humanizer that would literally not change notes, but just starting positions, ending positions, and velocity. This would do very minimal editing of the MIDI, but would still use machine learning to make it similar to other pianists and how they play, rather than just using randomization as you usually do in Ableton.

The second example we made was a MIDI generation tool. You could either generate from nothing or you could pass in starting data to generate from. It only generates new data after the initial data, so it doesn't add MIDI to the original MIDI. It will only make new MIDI after the provided MIDI. This is the opposite spectrum, where the machine is doing most of the generation.

The hope is to make a set of tools that span these two extremes. An example could be a tool that takes a drum groove and changes the time feel of it, or another tool that generates potential chords for a melody. Because of how Ableton's API could work, you could even have individual chord generation attempts per bar. So rather than trying to generate a bunch of chords in one go, it just suggests chords for a specific bar and you can choose your favorite.

## How machine learning is involved

Machine learning was involved everywhere. The idea for this project is to do the hard part of this future idea rather than any of the integration between tools and such. So the hard part would be making good models, and all we did was make two models (machine learning) to see if we could make the core of the idea.

The first model uses an RNN machine learning model to learn and then predict human performance from quantized MIDI. The second model is a transformer model that uses MidiTok and PyTorch to generate new MIDI tokens and then transform them into MIDI files.

## How you implemented the project

Both tools live in their own folders as standalone Python projects managed with uv. Each one has a CLI and a small package of code under src/.

### MIDI Generation

The MIDI generator is a command line tool built with Typer that basically wraps a causal transformer model we trained on tokenized MIDI. The code lives at midi-gen/midi-gen-python/src/midi_morph/.

For tokenization we used MidiTok over in tokenizer.py, which is what turns MIDI files into discrete tokens that the model can actually read. The CLI lets you pick between REMI, TSD, MIDI-Like, Structured, CP-Word, Octuple, or MMM, and we left REMI as the default because it keeps bar and position tokens, which felt important for keeping the timing of things like chords lined up. There are also train-tokenizer, encode, and decode commands so you can train your own vocab on a folder of MIDI and round-trip individual files through it.

The model itself is in model.py and it's a pretty standard causal transformer in PyTorch. By default it's 6 layers, 6 heads, d_model of 384, GELU activations, with a triangular causal mask, learned token and position embeddings, and the input and output embedding weights tied together.

Training is in training.py. MidiTokenDataset just walks a directory of MIDI, encodes each file with whichever tokenizer you picked, slaps BOS and EOS tokens on, and chops everything into fixed-length chunks padded with PAD. Training uses AdamW with weight decay, gradient clipping, and cross-entropy loss with PAD masked out so it doesn't try to learn the padding. The checkpoint saves the model weights, the config, the tokenizer name, and the sequence length, so when you go to generate it can rebuild everything from one file. It picks CUDA, MPS, or CPU automatically, and there's a max-steps flag if you just want to do a quick test run.

Generation is also in training.py. It loads a checkpoint, optionally tokenizes a prompt MIDI if you want to seed it, and then samples tokens one at a time with temperature and top-k. Once it's done it runs everything back through MidiTok to write out a MIDI file.

Before we had the learned model working, we also wrote two simple rule-based transforms in transform.py and music.py so the tool was at least usable without any training. chords-to-melody slides a window over the MIDI, grabs whatever pitch classes are in that window, and picks notes from the chord pattern that are closest to the previous melody note. melody-to-chords does the reverse — for each window of melody notes it scores all 12 roots times {maj, min, dim, sus4} chord templates against the pitch-class histogram and picks whichever one fits best. There's also an inspect command which is just a quick way to see the ticks-per-beat, instruments, and note count of a file.

### MIDI Humanizer

The humanizer is basically a supervised regression problem. The input is a quantized version of a piano performance, and the target is how much each note actually deviates from that quantized version in the original recording (in timing, duration, and velocity). The code lives at midi-humanizer/midi-huminizer-python/src/midi_humanizer/.

For dataset prep we used MAESTRO, with the loading and feature code in data/midi.py and data/maestro.py. For each piece, prepare_piece loads the MIDI with pretty_midi, converts the onsets and ends from seconds to beats using the tempo map, snaps them to a grid (default 1/16-note), and bins the velocities into coarse buckets (default bin width 8). The per-note features include velocity, duration, inter-onset interval, beat-phase and bar-phase as sin/cos pairs, how many other notes share the same onset (basically a chord-size feature), and a flag for whether the note is in the upper register. The targets are basically just the difference between the original and the quantized version: start minus quantized start, duration minus quantized duration, and velocity delta divided by 127. The splits come from the MAESTRO CSV and the prepared tensors get cached as train.pt, validation.pt, and test.pt.

We made two interchangeable model backends with the same input and output shape, in rnn.py and transformer.py. The RNN one is a bidirectional 2-layer LSTM with a pitch embedding glued onto the rest of the features. The transformer one is a 4-layer encoder with learned position embeddings and a padding mask. Both finish with a small MLP that spits out 3 numbers per note (onset shift, duration shift, velocity delta).

Training is in train.py. MaestroChunkDataset cuts each prepared piece into overlapping chunks (default seq_len 256 with stride 128), and collate_batches pads them into batches with a length mask. Training uses AdamW, a masked Huber loss so padding doesn't mess up the gradients, gradient clipping, and a full validation pass after each epoch. We only save the best checkpoint based on validation loss (either rnn_best.pt or transformer_best.pt), and the loss curve goes into train_history.json.

At inference time, in infer.py and data/midi.py, the input MIDI gets run through the exact same quantization and feature pipeline as training, the model predicts the three deltas per note, and humanize_midi_notes adds those deltas back onto the quantized values, scaled by a strength knob (0.0 means no change, 1.0 means full model output, anything above 1.0 is exaggerated). It keeps the same note count and pitches, so the model only edits timing, duration, and velocity. There's also an export-quantized command that just writes out the model's input view as a MIDI file, so you can A/B the original, the quantized, and the humanized versions in Ableton.

The CLI is in cli.py and uses argparse, with the subcommands prepare-maestro, train, humanize, and export-quantized.

## What you learned

I learned a lot more about machine learning, especially transformer models, and a bit more about RNNs. I think I'm getting my head around them, and even though I don't understand exactly everything, I understand the two architectures a lot better. I first learned a bit when I did the Andrej Karpathy tutorial at the beginning of the semester, but whenever I didn't understand something, I would implement it and move on understanding it about 20%. When I did this project, especially with the transformer part, I think I moved my understanding from 20 to maybe 70 or 80%. I'm actually super interested in transformers and I really need to understand the attention system better. One thing I would love to ask more about is resources for learning this stuff — I want to find books that are good for this, blog posts, YouTube videos, and other things that are good.

Another thing I also learned was how hard it is to tune. I had a lot of issues tuning these with David — we kept trying stuff and it would just give us kind of garbage back. We eventually found a set of hyperparameters that returned good enough data, but I would really want to look into how to tune models better, now that I understand a little bit the process of how tuning models works in the first place.

While David was doing a bit of research for the tokenization and to find good datasets, I dug into the Live API, and I learned a lot about it. It's super interesting, and you could essentially turn Ableton into your own DAW if you made enough tools for it.

I learned a lot more about tokenization, especially when it comes to MidiTok, because I didn't know almost anything about it, but luckily David knew enough to teach me.

## Reflection: challenges, unfinished work, and what you would change

One thing about machine learning is that I'm super interested in it, similar to how I'm interested in things like old programming languages and history. Those topics don't usually come to light in normal everyday scenarios, and usually not for long periods of time. However, just in this class, I've learned enough about machine learning to make a few small models at my work that predict customer intent. They're not super great, but they're good enough that they're somewhat useful, so it's coming in handy already.

Another thing that I was thinking about is that I actually really like classical AI and early machine learning. Generative is super interesting to me too, however, I just think the people in the space are a little bit zealous despite the really interesting technology. So I'm definitely gonna keep learning about AI, but not because of the AI boom and money or whatever. I really am just interested in the technology enough to want to know it.

