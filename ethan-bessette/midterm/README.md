# ML Midterm Project Documentation
Ethan Bessette

## Proposal

Produce an artifact such as a piece of music, composition, trained neural network, or interactive musical experience.
Develop a significant new skill or understanding that you unlocked and communicate it to the class in your documentation and presentations.

What you would like to do
How you will do it
Questions, concerns, and stretch goals

### Vision
Create a model that estimates synthesizer parameters to create patches that match target sounds.

### PseudoCode
#### Differentiable synthesizer
In Csound, I will design an FM synthesizer with 2 audio oscillators, 1 control oscillator, and one noise generator. They will all be able to modulate each other and themselves, like in FM8. Each will have an amplitude envelope.
![FM8](./Images/Figure1.png)
Even with few numbers of oscillators, a large number of sounds can be created. 
![FM Scream in MAX](https://drive.google.com/file/d/1FBpwcrP1YOWGa7a5kgqJJ4nyOe9Wz6hr/view?usp=sharing)

#### In-domain dataset
All the differentiable parameters will be randomized and coupled with the synth's resulting audio output.

#### Out of Domain dataset
Additionally, audio that doesn't have coupled synth parameters will be used.

#### Structure

#### Training
The datasets will be divided 80-10-10 training validation testing.
For in domain data, the loss between estimated synth parameters and real will be calculated.
For all data, the audio spectral loss will be calculated ( 


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
