## Final Project

### What I made?

Initially, I had adapted WaveGAN to work on my MacBook to generate entirely new audio. Unfortunately, due to the unpredictable limit usage of Colab I was unable to fully train the model and generate the final audio using machine learning.

Instead I pivoted the project and put together an algorithmic composition using the sliced audio files and a custom "Xenakis" script. While this final output does not utilize any machine learning, it uses data manipulation and statistical probability to generate a 3-minute ambient piece.

https://drive.google.com/file/d/15UZxk9HQ_y0oF9ey_Sa7hsqF2_iy44hd/view?usp=sharing

### How machine learning is involved/how it works

For the initial task, I utilized a Generative Adversial Network. However, because of hardware constraints and colab being difficult to work with, this became an algorithmic compositon instead.

The composition of this piece utilized two scripts:

- A slicing script
- The "Xenakis" script

#### Slicing script

The slicing script formats a folder of audio I collected (4 hours of ambient music) into a dataset that was originally built for the data-preparation pipeline for WaveGAN, but ended up acting as the audio pool for this piece I put together. It turns these 44khz audio files into 16khz and mono, and then cuts them into exactly 1.024 second segments.

#### Xenakis script

With the cut audio files, I then ran them through the Xenakis script. This utilizes a stochastic proccess. It scatters the audio segments across the timeline using probability instead of a rigid music grid, creating an erratic 3 minute composition. 

The code alters the volume of these snippets in decibels by a random amount, and also pans the audio randomly left and right. More importantly, it places the sounds randomly by utilizing the poisson proccess. This proccess is typically used to count the occurences of certain events that appear to happen at a certain rate, but are actually completely at random (like rain hitting a roof or the number of cars passing by a certain street). By applying this exponential distrbution to the wait time between audio clips, there is an unpredictable clustering of sounds rather than a mechanical beat.


### How I implemented the project

1. I first curated the dataset of ambient audio. With the intention of using WaveGAN, I had collected around 4 and a half hours worth of ambient music. 

2. I then created a 3-minute audio canvas with the Xenakis script that would randomly select a segment from the dataset, apply the random volume and panning adjustments and then paste it onto the canvas.

3. This proccess also required some tweaking of the average_density_ms, because if it was too short the audio became muddy and if it was too long it felt empty. I came to a sweet spot of around 400ms. 


### What I learned?

During our last class and this project I learnt how resource-intensive GANs, as well as other forms of machine learning are. Neural networks are also incredibly strict with their input data. Most of this proccess was tedious data formatting, and realizing how if a file isn't exactly a certain amount of samples the whole thing will crash.

I became familiar with different libraries, such as librosa which is often used for tasks requiring analysis and format convention, or pydub which is used for mixing and panning.

Another question I had coming out of this project was if I even need to use AI for something like this? Simply using the right math for things like timing and volume I was able to mimic the chaotic piece I imagined using WaveGAN to be. 

### Reflection: Challenges, unfinished work, and what I would change
Colab is very annoying to run. There are time constraints and having to keep that tab open constantly is difficult with Google frequently disconnecting you. Furthermore, there is a hidden GPU limit usage that has no way of being tracked, and a cooldown period of 3-5 day can randomly be imposed onto you. With WaveGAN being a computationally draining task, this is impossible to run on the free tier.

If I were to do this again it would be with a much stronger computer. That being said I am still satisfied with the backup plan I executed as I ended up getting to experiment further with math creating organic sounds.