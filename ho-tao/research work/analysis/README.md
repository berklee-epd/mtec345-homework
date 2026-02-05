# Noise to Water - Aiphex Twins (2022)

Aiphex Twins is an AI electronic music project lead by Philipp Stolberg and Edgar Eggert. Philipp is an electronic music producer from Zurich and Edgar uses deeplearning in computational cosmology to find out more about distant galaxies. Both passionate about electronic and ambient music, they met at the Dekmantel music festival and has kept in contact since. 

## Techncial Analysis 

### ML Architecture
GAN is when two neural networks train to compete against each other to generate more authentic data from a training dataset. One network generates new data by taking an input data sample and modifying it as much as possible, while the other network tries to predict whether the data belongs in the original dataset. This proccess keeps repeating until the predicting network can no longer distinguish fake from the original. They used their own GAN model, as well as an adapted version of Chris Donahue's WaveGAN model in the Tensorflow version trained in Colab. These models were used to take raw audio snippets of roughly a second and treat them with a bunch of effects and then modulate them over time so that they spanned throughout the track. They were fed 7 hours of Aphex Twin, 9 hours of Steve Reich and 8 hours of Boards of Canada as well as thousands of kick drums from Truncate and Chris Liebing. They were also trained between 6000-25000 epochs (an epoch is one full cycle where the algorithm processes every training example in the dataset once)


Lyrics were based on a vanilla LSTM implementation written in PyTorch, the standard version of a RNN (recurrent neural network) architecture designed to solve the problem of "forgetting" information over long sequences. RNN runs a cell state that goes through the entire sequence, where then the network decides whether to add new info, keep what's there or discard it away. There is the input gate which decides what's worth keeping and adding, the forget gate which decides what should be disgarded and the output gate which decides what the hidden state (output of the step) should be based on the filtered version of the current memory. Lyric generation was deprioritized, and the training data being fed was the Music O-Net billboard chart library that included metadata such as lyrics and descriptors. 

### Tool Ecosystem

The primary ML framework consisted of an adapted WaveGan implementation, using a modified open-source code developed by Chris Donahue. Initially they used GPT-2 and Google Magenta (off-the-shelf solution), but realized they were incapable of creating what they wanted. Edgar would be in charge of training and batch-inference (generating predictions on a large set of observations all at once), and would pass it to Philip to arrange the snippets into a track through a DAW. WaveGAN is optimized for consumer laptops because it uses convolutions to generate an entire audio clip at once. Unlike other AI models that build sounds piece-by-piece, WaveGAN creates a complete raw waveform instantly, which is much easier for consumer-grade GPUs.

### Data Pipeline

As mentioned, input into the models were thousands of kick drums, as well as 7 hours of Aphex Twin, 9 hours of Steve Reich and 8 hours of Boards of Canada. 

### Workflow and Proccess 

 For the melody, a snippet of Chopin's Nocturne was entered into the MuseNet Model, which can generate up to 4 minutes of musical compositions with 10 instruments. A MIDI file of a piano line was created and put into Google's ToneTransfer, which generated a sax line which was layered with excerpts of the generated piano melody. With their own model they generated WAV files of the drum patterns, but turned to Donahue's WaveNet Demo to export sounds for hihats because their own model was not able to do as well.


## Musical Analysis

### Structure
The song does not follow a traditional structure that uses a verse, chorus, bridge, etc.
### Musical Elements
For the hi-hats, they entered part of a programmed rhythm line into a concatenative synthesis tool called Mosaic, that basically tries to reconstruct the audio with a predefined sample corpus. They then selected the generation that they liked best and used it as a Hihat element.
### AI Signatures

## Music Critic
### Comparative Analysis
In comparison to other contestant entries, this project focused on frankensteining a collection of generated WAV files as opposed to focusing on MIDI generation. Since the focus was on aesthetic rather than focused melodic content, there were a lot of glitchy textures and unexpected sounds created unexpectedly. This was controlled through limiting most of the generated audio to one-second snippets, which Philipp had to manually listen to and arrange. This also helped in terms of scaling as the team lacked the hardware to train elaborate models. The architecture of the AI Models themselves are reproducable, however to reproduce what Aiphex Twins themselves did would be impossible. 

### Ethics and Aesthetics
Using copyrighted music for training is often labeled as fair use or transformative because the model isn't copying the song, but learning so that it can generate new waveforms. 

