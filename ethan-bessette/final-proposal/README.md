# ML Final Project Proposal 
Ethan Bessette

## Description
For my EPD capstone this summer, I plan to use MediaPipe along with Unity to create an interactive experience. I looked into MediaPipe packages for Unity, but they seemed to complicated, so I will likely run the MediaPipe Models and Gesture recognition models in external processes handled by the .app bundle and stream data into Unity to generate visuals and audio.

This project matters to me because it will jumpstart my project for the summer. In terms of why the capstone project matters: 

 > This project is a multimodal interactive experience, or installation, that aims to
connect the kinetic with the visual and auditory modes using the gestures and positions
of humans to drive a procedurally generated visual system. The experience will involve
the exploration of potential gesture combinations, such as in online particle generators
where combining particles creates new types of particles. It will also involve the
exploration of a virtual space as the participants progress through a short story. The
final outcome will be a binary executable and production documentation, and the
presentation format will be an installation work that runs the executable using a
computer, a projector or screen, and audio amplifiers. It will also be recorded as a video
to be more accessible as part of a digital portfolio. This project is important to me
because it combines my education in interactive audio system creation with my interests
in sound design and programming. I also personally love finding new sounds and
textures, and this experience will be a structured way to share that joy of exploration
with participants by allowing them to use their bodies to create new combinations." 
 > 
> — from my capstone proposal.



## Use of Machine Learning and Other Platforms

MediaPipe models will be used to track the position of particpants bodies based on visual data from a camera.
Wekinator will be used to detect gestures based on the landmark data from the MediaPipe models.

For this short term project, I will use a basic web setup. I will stream MediaPipe data to Wekinator as well as directly to Max and Processing to generate audio and visuals based on raw position data and gesture recongtion.


## Development Plan
1. I already added pose recongition to the example from the Machine Learning Repository.
2. I added multiple pose recognition so that mutliple people can be tracked.
   - these changes can be found [here](https://github.com/berklee-epd/mtec345-homework/tree/ethan-bessette-final/ethan-bessette/final); follow the setup instruction in the Readme. Note that the remainder of the readme is not accurate as of the submission of this proposal.
2. Next, I will add OSC hooks into Max and Processing.
   - I have some examples from previous classes to pull from. If I can't get Processing to work, I'll make the visuals in Max.
3. Create very basic reactive audio and visuals (my goal is to keep scope very small).

## Questions, concerns, risks, and stretch goals
- Stretch goals: this will almost certainly not happen, but it would be nice to get even more of a headstart on my summer project by getting the visuals and audio to run in Unity/Wwise instead of Processing/Max.
- I have no questions; I have a pretty clear idea of what my next steps will be.
- One concern is having enough time to get any progress for next week. Many of my finals are due next week.