# ML Midterm Project Documentation
Ethan Bessette

## Proposal

### Vision
Create a model that estimates synthesizer parameters to create patches that match target sounds.

### PseudoCode

![Architecture example](./Images/Figure2.png)

From https://ieeexplore.ieee.org/document/10017350

#### Differentiable synthesizer
In Csound, I will design an FM synthesizer with 2 audio oscillators, 1 control oscillator, and one noise generator. They will all be able to modulate each other and themselves, like in FM8. Each will have an amplitude envelope.

![FM8](./Images/Figure1.png)

Even with few numbers of oscillators, a large number of sounds can be created. 

https://drive.google.com/file/d/1FBpwcrP1YOWGa7a5kgqJJ4nyOe9Wz6hr/view?usp=sharing

#### In-domain dataset
All the differentiable parameters will be randomized and coupled with the synth's resulting audio output.
This process will be automated in the terminal by generating random values to fill a csv for each differentiable synth parameter, reading the values into csound and saving the resulting audio along with the csv of parameters.

#### Out of Domain dataset
Additionally, audio that doesn't have coupled synth parameters will be used.

#### Structure / Architecture
This is an area that I have some questions and concerns about. One option is to follow the structure from the paper diagram I included above. On the other hand, I don't know enough about the various structures and optimization / training types.
Because of this, I might use similar structure to what we've seen in class.

I think if I decide on what structure to use conceptually, I would just need a generic example so I can change it to fit my needs.

Ideas could include:
Convolutional
Multi head attention layers within transformer to find changes across time.

##### Data comparisons
I still have to learn how to use the calculated loss to optimize. I will review the nn_2 and 3 to see what optimization functions are used. For example, the loss of each individual synth parameter might be summed or averaged somehow into overall loss.

For **audio spectral loss**, use MelSpectrogram. The number of bands can be adjusted, the window size, and hop length.

![MelSpectrogram](./Images/Figure3.png)

For **synth parameter loss**, each synth parameter will be normalized from 0 to 1 and the difference taken for each.


#### Training
The datasets will be divided 80-10-10 training validation testing.
For in domain data, the loss between estimated synth parameters and real will be calculated and used to optimize.
For all data, the audio spectral loss will be calculated by taking the difference of the MelSpectrogram of original and predicted audio and used to optimize.




## Notepad
Window of 4 chords, what is most likely next chord?
Training:
- 4 chords of song, give next chord

So for audio, give a window of seconds and therefor x samples. Predict next y samples, add to output, move window

Diffusion model
Encoding: add noise to data over course of time steps until full noise.
Train it to recognize where it is in timestep, therefore how much noise to remove to get back one tilmestep, repeat until back to original image
It trains it to predict noise to remove per timestep until it gets an image that resembles the training images


DDSP
Train a model to control digital signal processing parameters to create a complex synthesizers given note pitch, velocity, and length
- label training data with note pitch, velocity, and length
- window of x notes of input (range of input length from 1 to maybe 4)

Get output sound, match to original synthesizer, adjust sytnhezsizer parameters to reduce difference
- gradient descent


Calculating the loss change in output and input to gradient descent 
- could be used for deep ANC

https://realpython.com/gradient-descent-algorithm-python/
This explains gradient descent. For a 2d vector (x,y) it finds a 1d vector, the minimum, by getting the gradient (the derivative of the 2d vector) and 


The next chord predictor is probabilistic. It gets optimized 



I could get samples of an instrument or my voice. Then
DDSP
Create structure of synthesizers and parameters. Randomize parameters, calculate loss, move parameters to minimize loss.
I could calculate gradient descent of move input towards trained function
For each audio sample, calculate difference of output to original


One hot encoding aligns output with true correct answer in one hot encoding to determine loss.
So for my model, it should have one output for each changeable synth parameter.


## The Process

### Dataset creation

#### Csound
I created a csound file that outputs 32 floating point wave files at each of 12 notes through the same synthesizer, naming them the index of the synth along with the note number. Outputting results in a dataset being generated that contains sets of 12 notes for each set of random synth parameters along with text files holding the synth parameters. As of now, I haven't found a way to output only the synth parameters, so the text file contains a header that will need to be discarded when cleaning data for machine learning training.

There is an encode.csd file that generates parameters and creates audio for them, as well as a decode.csd that reads parameters and generates data. I tested them and it works. I also tested them on my own new parameters that I changed by hand.

The next step will be figuring out how to get the .csd to run in the correct order in training. Also, training will take a long time unless I figure out how to make generating audio much faster for the amount of data I have.

While the data is generating, I'm checking my activity monitor and it looks like processing is kept to 1 processor. I wonder if I could figure out multi threading to make it faster as well as forcing csound to make new instances instead of reusing them.

##### Problems
1. One problem was figuring out how to keep the pitch relatively constant during self modulation. When an oscillator self modulates its frequency, the pitch is perceived as lowering as the sidebands to the positive and negative are created. I researched ways to keep this constant and first kind Bessel functions were what came up. I tried to ask ChatGPT to help write functions to keep the pitch normal by calculating the spectral center as a function of f0 and self modulation index, but when I tried to implement it in Csound, it was too computationally expensive and sound froze every time. I spent a while finding a workaround and I ended up using a realtime polynomial function to approximate the amount of frequency offset within the range of parameters that I was using. It stops working at a certain point, but that doesn't matter since the way I programmed the synth it will never generate parameters outside that range. I also realized that a small amount of modulation by the original frequency helped to stabilize the pitch. I slightly modulate the frequency of the oscillator with a separate oscillator at its original frequency as a function of self-modulation index. While it adds some harmonics not present in true self-modulation, it doesn't matter.

2. Another problem was figuring out how to keep the parameters constant while generating 12 different pitches of the same parameters. I ended up using two different scheduler instruments to do this. One scheduler spawns instances of the other scheduler so that synth sets can be generated in parallel. The other scheduler spawns 12 parallel instances of one set of parameters at different pitches. The instances themselves output the audio data, while the second scheduler holds the generated parameters and outputs them when done.

3. Originally, the synth parameters were generated in each instance of a note. This obviously didn't work because what was supposed to be different pitches with the same parameters actually all had different parameters. To fix this, I generated each parameter from 0 to 1 in the 2nd scheduler instrument and set up the note instrument so that the scheduler could pass in the parameters when called. The note instrument can further process these normalized values. This allows the eventual machine learning algorithm to be able to output normalized values for the parameters which can be used to generate audio.

4. It turns out Csound re-uses instances of instruments to save storage in memory. This was causing a problem where two clips were combined in one in the output audio. To solve this, I made sure to offset the parent scheduler so that it never created secondary schedulers at the same time. Note to self, I bet if I use more primary schedulers than the note length, I might have to change this so that it instantiates notes with a new identity instead of simply offsetting.
    - Update, yes, this is the case. If I were to keep the note 5 seconds, that means I can only uses 5 instruments at a time. To generate 1000 sets of synth parameters, it would take 200 seconds to generate the dataset. Honestly that's reasonable, I'll keep it how it is for now. Nevermind 200 seconds only generates 200 examples. Def something I need to fix.

5. The biggest problem is that I didn't understand that for ddsp to work, the synth has to be implemented in PyTorch.

#### PyTorch
I referenced the ddsp core.py library.

I created a linear interpolation wavetable lookup function that takes in an index and returns an amplitude value based on the wavetable.

I created an adsr generator that generates envelopes based on attack time, decay time, sustain time, sustain level, and release time. The time based parameters are loaded into a tensor, and softmax is applied so that the total time sums to one. Each value is then multiplied by the total number of samples to get the total time.

I created an FM bank generator. Currently, it inits 2 audio tensors with zeros the length of total samples. It sets the phase of both to zero. Then, it works sample by sample:
- calculate frequency from base frequency, ratios, previous audio tensor amplitude values, indexes
- make the current audio sample equal the table lookup for the current phase
- update the phase by adding its acceleration (it will always increase and wrap around 1. A higher frequency means the phase gets to 1 quicker / in larger steps. A lower frequency means it gets there in shorter steps)
- output the audio with the values of out 1 and 2 scaled to sum to 1 to avoid clipping.
It currently implements only modulating the other audio wave, no self modulation.

Next step: generate dataset

I used ChatGPT for:
- create functions for making Mel spectrograms for pre-processing
- helper functions for converting between midi, frequency, and Mels
- manage multiple cpus to speed up dataset creation
- suggesting how to edit the synthesize function for batch processing
- suggesting how to save a single .pt with all the parameter sets (since 12 notes all share parameters)
- for each example, save .pt files containing the Mels, id of the parameters from the above file, and the fundamental frequency (in case I end up separating. For now I don't need this)
- assign parameter sets to train or test sets
- compute stats about training data for normalizing test data and save to a file
- save a csv containing the file path of each example, its parameter id, midi note, f0, and whether its train or test data (all notes sharing parameters were assigned to the same split to avoid data leaks)

Summary of AI use: I knew I wanted to process the data before saving to disk to decrease file size (instead of saving wave files and then processing them). I didn't know which functions to use for Mel processing, but I knew the arguments I wanted to use for them and I understand what they do. I didn't know how to assign tasks to different CPUs, but I knew I wanted each CPU to work on all the notes for a parameter set at once. I didn't know how to adjsut my synthesis code to allow for the additional tensor dimension. However, after receiving help I understand why the changes to synthesize() were made.

#### DDSP
Includes tensor operations that create audio synthesis as part of the machine learning function. This makes the parameters end to end differentiable.

##### Original DDSP Library
1. Preprocess raw audio
    - detect fundamental frequency and loudness over time for 5 second clips of audio, store in a TFRecord file
2. Save dataset stats so that future inputs can be processed to match training data
    - pitch (f0), power, loudness, quantile transform.

Training:
1. expects Nn to output amplitude over time, harmonics over time, and fundamental f over times
2. Uses those in additive to create pitched part of input
3. Uses noise and filter to create unpitched
4. The output of the model = input of synth closely reflects the spectral and envelope data of the original audio


##### My Implementation


1. Break training audio into Mel spectrogram at time points, save paired with parameters. Break into training and test data.
2. Save dateset stats for normalizing test data.
Training:
3. estimate synth parameters for given Mels
4. process audio tensor from those parameters, convert to Mel spectrogram
5. Find loss between output and training Mel spectrogram
6. Find loss between estimated and real synth parameters
7. autograd
8. Repeat

### Training

Understanding conv2d layers:
https://colab.research.google.com/github/d2l-ai/d2l-en-colab/blob/master/chapter_convolutional-neural-networks/padding-and-strides.ipynb

- kernel size is the size of the filer that moves up/down left/right over the 'image'
    - if the input is not square, consider using a rectangular kernel as well
    - so in my case, I have input that's (128, T) where T is 750
    - consider a kernel that is (7, 41)
        - this is based on the ration 7 / 128 used here: https://ieeexplore.ieee.org/document/10017350
        - maybe start with something larger to make sure it works. (47, 281)
- padding is the number of rows and columns added to the input so that the kernel captures the data in the corners and edges better
- stride is like window size, how many units the window moves up and sideways
    - to preserve size, use P = ((S-1)*W-S+F)/2, with F = filter size, S = stride, W = input size
    - if using a stride of (2, 12), a kernel of (48,282), input is (128, 750), padding = (87, 4260)

#### Pseudocode
Handle loading data using DataLoader and set the batch size with BATCH_SIZE and shuffle=true

Suggest a batch size? 64

1. mel frames in to nn.conv2
    - input channels is 1 because mono audio
    - height is num Mels, 128
    - width is timesteps = 750
    - so input is (128,750)
    - stride=(2,12) kernel=(48,282) padding=(87,4260)
2. Batch normalization
3. Repeat 1 and 2 three times
4. Send to GRU
    - batch_first=true
    - input will be (batch#, 750, 128)
        - batch, sequence, features
    - input_size=features=128
    - hidden_size=256
        - maybe 512 if needed
5. Send to linear layer
6. Use output to synthesize audio
7. Calculate mel
8. Get loss between Mels and L1 loss between parameters
    - first 0.125 epochs, only use L1 loss
    - for the next 0.375 epochs, mix loss linearly between parameter and spectral loss
    - for the last 0.5 opochs, use an even mix of parameter and spectral loss
    - multiply the L1 loss so it equal the spectral loss
9. Adam optimizer
    - start learning rate at 0.005, decrease exponentially by 0.99
        - learning_rate = 0.005 * (0.99)^epoch

#### Issues
/Users/ethan/.local/bin/uv run /Users/ethan/Int Working Media Drive/Berklee/Semester 8/MTEC345 Machine Learning/mtec345-homework/ethan-bessette/midterm/.venv/bin/python /Users/ethan/Int Working Media Drive/Berklee/Semester 8/MTEC345 Machine Learning/mtec345-homework/ethan-bessette/midterm/train.py 
/Users/ethan/Int Working Media Drive/Berklee/Semester 8/MTEC345 Machine Learning/mtec345-homework/ethan-bessette/midterm/.venv/lib/python3.13/site-packages/torch/autograd/graph.py:829: UserWarning: Error detected in MulBackward0. Traceback of forward call that caused the error:
  File "/Users/ethan/Int Working Media Drive/Berklee/Semester 8/MTEC345 Machine Learning/mtec345-homework/ethan-bessette/midterm/train.py", line 309, in <module>
    train()
  File "/Users/ethan/Int Working Media Drive/Berklee/Semester 8/MTEC345 Machine Learning/mtec345-homework/ethan-bessette/midterm/train.py", line 264, in train
    pred_mels = render_predicted_mels(pred_params, f0s).to(DEVICE)
  File "/Users/ethan/Int Working Media Drive/Berklee/Semester 8/MTEC345 Machine Learning/mtec345-homework/ethan-bessette/midterm/train.py", line 192, in render_predicted_mels
    audio = synth.synthesize_a_batch(pred_params, adsr1, adsr2, f0s)
  File "/Users/ethan/Int Working Media Drive/Berklee/Semester 8/MTEC345 Machine Learning/mtec345-homework/ethan-bessette/midterm/synth.py", line 220, in synthesize_a_batch
    freq2 = f0s * (1 + a1[:, sample - 1] * i1index2)
 (Triggered internally at /Users/runner/work/pytorch/pytorch/pytorch/torch/csrc/autograd/python_anomaly_mode.cpp:127.)
  return Variable._execution_engine.run_backward(  # Calls into the C++ engine to run the backward pass
Traceback (most recent call last):
  File "/Users/ethan/Int Working Media Drive/Berklee/Semester 8/MTEC345 Machine Learning/mtec345-homework/ethan-bessette/midterm/train.py", line 309, in <module>
    train()
    ~~~~~^^
  File "/Users/ethan/Int Working Media Drive/Berklee/Semester 8/MTEC345 Machine Learning/mtec345-homework/ethan-bessette/midterm/train.py", line 275, in train
    total_loss.backward()
    ~~~~~~~~~~~~~~~~~~~^^
  File "/Users/ethan/Int Working Media Drive/Berklee/Semester 8/MTEC345 Machine Learning/mtec345-homework/ethan-bessette/midterm/.venv/lib/python3.13/site-packages/torch/_tensor.py", line 647, in backward
    torch.autograd.backward(
    ~~~~~~~~~~~~~~~~~~~~~~~^
        self, gradient, retain_graph, create_graph, inputs=inputs
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/Users/ethan/Int Working Media Drive/Berklee/Semester 8/MTEC345 Machine Learning/mtec345-homework/ethan-bessette/midterm/.venv/lib/python3.13/site-packages/torch/autograd/__init__.py", line 354, in backward
    _engine_run_backward(
    ~~~~~~~~~~~~~~~~~~~~^
        tensors,
        ^^^^^^^^
    ...<5 lines>...
        accumulate_grad=True,
        ^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/Users/ethan/Int Working Media Drive/Berklee/Semester 8/MTEC345 Machine Learning/mtec345-homework/ethan-bessette/midterm/.venv/lib/python3.13/site-packages/torch/autograd/graph.py", line 829, in _engine_run_backward
    return Variable._execution_engine.run_backward(  # Calls into the C++ engine to run the backward pass
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        t_outputs, *args, **kwargs
        ^^^^^^^^^^^^^^^^^^^^^^^^^^
    )  # Calls into the C++ engine to run the backward pass
    ^
RuntimeError: one of the variables needed for gradient computation has been modified by an inplace operation: [torch.FloatTensor [64]], which is output 0 of AsStridedBackward0, is at version 191998; expected version 191996 instead. Hint: the backtrace further above shows the operation that failed to compute its gradient. The variable in question was changed in there or anywhere later. Good luck!

Process finished with exit code 1

## Midterm Reflection

What you did (the artifact you produced and/or what you built)
- programmed a FM synth
- re-programmed the synth using Pytorch
    - more details above
- created training outline and model, but ran into issue with synth not being fully differentiable due to sample by sample calculations from cross modulation.

How machine learning is involved (e.g. model, data, tools, or concepts you used)
- The end goal is a machine learning model that will predict the synth parameters needed to m

What you learned or what new skill or understanding you developed
- I learned about autogrid functions
- I became more familiar with PyTorch by programming the synth in it

Reflection: challenges, what you would do differently, and how the results compare to your expectations (or to a non-ML approach, if relevant)
- I got the model to work and output untrained data, but the synth was not fully differentiable due to sample by sample calculations from cross modulation.
- In the future I want to figure out how to get this part to be differentiable so I can train the model

