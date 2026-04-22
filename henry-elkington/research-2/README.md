# Research Work Phase 2: Prompt Engineering with Google Lyria

[assets](https://drive.google.com/drive/folders/1PqfC0Tr_md5m2Q3lYYk6QpZIalLq3Tcd?usp=sharing)

## Chosen Tool

I chose Google Lyria 3 and Suno because I have heard a lot about them,
and I wanted to see the quality output of these tools, so I wanted to try
to make something using mostly Suno and Lyria.

## Tool Experimentation

### Lyria 3

I first tried to use Lyria 3 because it was free and I haven’t ever used a music model before. It was limited to 30 seconds and I could only use it through the chat interface, so there was a chat button in between me and whatever was being made. I found that the music it made was not actually that preferable to me. It seemed like they had focused heavily on the lyrics for this model, and I was not attempting to make anything with lyrics. However, I don’t think I could understand this model very well because it was locked behind a chat interface, so after messing around with it for a bit, I ended up not using any of the results.

Prompts to try and get a workable sound bite

1. lyria/1.mp3 (no prompt)
2. make a string quartet part of a song with modern chords
3. can you make it less classical and more modern strings
4. add a string section to this
5. can you make a drum track, boom bap, deep kick, stem
6. can you make an instrumental track, 90s hip hop horn track, with modern chords
7. can you make an instrumental track, 90s hip hop horn track, with modern chords with no drums
8. can you make a hopeful 8 bit song
9. can you make a hopeful 8 bit song no vocals

### ComfyUI Workflows

I did some experimentation with ComfyUI workflows because it was free and I could download models to use on my computer.

However, I didn’t realize how hard this platform was to use, so I ended up just using some default workflows to experiment with some of the models.

This is something I’m going to have to look into more if I want to use it effectively. I didn’t realize how in depth this tool would allow you to customize the workflows. I definitely should use this tool to understand the models better before I even try to train them in Python or something.

### Suno

This is the first time I’ve ever used Suno, so I’m definitely not the greatest at getting good results out of it. What I first tried is just making a bunch of random stuff to see what it’s capable of generally. It was pretty interesting and I also was just learning how to use it generally.

I think that the output of this was significantly better; however, it’s a paid model that has a lot more work put in to make it a marketable product. Because of that, it’s a lot easier to get up and running and get good results out of it. My theory is that if I were to put a lot more work into the open source models, I would get similarly good results. However, I’m not in the space enough to know how to do that yet.

I made a few genres and songs just to figure it out, and I left the bad stuff that I didn’t like out of this project. And once I kind of started to understand how to use this

1. suno_default/1.mp3 Instrumental, ambient strings and piano, experimental
2. Instrumental experimental ambient texture, minor, modal, sound design
3. electronic, ambient texture, piano texture, house
4. Jazz fusion, modern HIFI, horns, strings, auxiliary percussion,

I discovered the make your own model feature. So what I did is, I put like 10 of my songs into it and tried to make a model that sounded similar to what I make. 

## How they work

these models starts with a language model that interprets your prompt to generate lyrics, structure and extract style stuff like genre, tempo, and instrumentation. Those are put into an audio token transformer, which predicts sequences of compressed audio codes, simmaler to next word prediction. The compression uses residual vector quantization, where stacked codebook layers capture progressively finer detail from coarse subtle. Then a neural audio codec decoder reconstructs those tokens back into an mp3.

## Reflections

I’m surprised how good Suno is, and I’m curious to see if I can make better quality stuff with open source weights and other things rather than using a closed source off-the-shelf model. I’m also more interested in sound-to-sound models and trying to understand how some of that works and maybe how to use it. I feel like it’s fun to mess around with, but I wouldn’t want to post any of the music that Suno made under my account. However, I think a lot of people would disagree with me on that. It’s fun to mess around with and understand how the technology has progressed.
