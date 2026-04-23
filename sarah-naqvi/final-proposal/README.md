# Final Proposal 

## What you want to make, study, or build

I want to make an interactive performance system that recognizes gestures I make whilst playing the flute. Certain gestures I make for different flute fingerings will add specific effects to the audio and play background samples to accompany the flute playing. 

## Why this project matters to you artistically, technically, or conceptually
This project is artistically significant because I really want to incorporate the flute in this project since it is my principle instrument, and I think that it is unique to have processed flute sounds within an interactive composition. I also want to continue to use Wekinator and explore more of its capabilities for the final project. I'm also curious and excited about the way MediaPipe will work with identifying the fingering gestures. 

## How machine learning will be involved
I plan to use machine learning by using MediaPipe and Wekinator in order to recognize flute fingering gestures to then trigger certain effects processing and samples. 

## What data, source material, tools, models, platforms, or workflows you plan to use
In terms of data and source material, I'll be starting with the [example media pipe code](https://github.com/berklee-epd/mtec345/tree/main/extras/media-pipe-example) and running it locally. This will utilize my laptop's webcame and be able to capture my gestures. I will also use Wekinator for its ability to take input from Media Pipe and output that as OSC to MaxMSP. In Max, I'll be able to trigger samples and do the live audio processing and get audio output. I also plan to use AbletonLive to record my performance by setting the input to Ableton as the Max audio output. 


## How you plan to develop the project, including your first concrete steps
- Step 1: Start with the media pipe example code that recognizes the hands and face and make sure I can get it running on my laptop
- Step 2: Media pipe sends OSC to Wekinator to be able to recognize my gestures as classes
- Step 3: I'll train wekinator with the "All Classifiers" type to recognize the distinct flute fingerings
- Step 4:  Wekinator sends OSC to Max that has the udp send and recieve objects that I can use to trigger samples to play, and allow for effects processing to be turned on and off.
- Step 5: I can take audio output from max and record my performances with Ableton Live 

Some effects I plan to explore include reverb, bitcrusher, and delay. Additionally, some background sounds I have in mind are ambient crackly sounds and pads.   

## Questions, concerns, risks
I'm not sure how clear my flute fingering gestures will be for Media Pipe and Wekinator to identify. Perhaps I will need to get creative with the gestures I provide whilst playing the flute in order to make them more obvious. Instead of keeping my fingers close to the keys, I will probably need to lift them more or move my eyebrows for gestures. I'm also concerned that perhaps the effects processing on the flute audio will be difficult to implement since I haven't tried that with Max before, but I think a good backup plan would be to use gestures to trigger samples while I'm playing, so there is still some interactivity even without effects processing. 
###  Stretch Goal
I think a good stretch goal would be to have sort of visual component so perhaps I could experiment with having audio reactive visuals using [Jitter](https://docs.cycling74.com/learn/articles/jitterchapter00a_whatisamatrix/). I'm not exactly sure what visuals to implement but even a simple change of colors could make the experience feel more engaging and add some design and more interactivity to the Max patch. 