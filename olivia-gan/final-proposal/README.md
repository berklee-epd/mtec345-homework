## Final Project Prposal

![](mediapipe.png)

### What I Would Like to Do?

For my final project, I want to build a real-time performance in which my hand gestures control processing of my live vocal inside Ableton Live. I am very inspired by last week's lesson and I plan to use MediaPipe to track my hands through a webcam and then using TouchDesigner to turn that gesture data into control information. My goal is to design expressive vocal effects, such as vocoding, tremolo, reverb, delay, and auto-shifting, where my physical movement dynamically alter these parameters. I want the final result to feel like a complete intergrated performance instrument and that my body becomes the visible automation engine of the process of sound design.

### Why It Matters?

As someone who works closely with vocals and performance technology, I like the idea of making vocal processing feel more physical and visible. I am drawn to the idea that singing can be extended by gesture, so that performance becomes a combination of voice and motion. Technically, this project matters to me because I saw in our last class how computer vision and gesture tracking can be turned into control signals, and I really want to try that process on my own. This is unknown territory for me, and I want to explore what can be done with these control signals while learning how to integrate them into Ableton Live.

### How machine learning will be involved?

Machine learning will be involved through MediaPipe’s hand-tracking model. It takes visual input and translates it into information about finger positions, hand shape, and movement, which can then be used inside TouchDesigner to change audio parameters. I am excited to experiment with mapping a range of expressive hand gestures to plugin parameters in Ableton Live. For example, vertical movement could control pitch shifting, horizontal movement could affect panning or delay time, hand openness could shape filter cutoff or reverb depth, and rotational or twisting motions could control modulation effects such as tremolo or vibrato.

### Resources

The main tools I plan to use are MediaPipe, TouchDesigner, Ableton Live, my laptop cam, and a microphone with an audio interface. Because I am new to this area, I plan to build my understanding by reading/watching through a range of online materials, including practical tutorials and more in-depth documentation on MediaPipe that explain both its implementation and underlying concepts.

Links:

* [video 1](https://www.youtube.com/watch?v=cFHLWsniNIs)
* [video 2](https://www.youtube.com/watch?v=e2FtkufeErY)
* [MediaPipe Solutions](https://ai.google.dev/edge/mediapipe/solutions/guide?hl=zh-cn)
* [GitHub Page](https://github.com/google-ai-edge/mediapipe)


### Plan for Getting Started

I plan to develop the project by first getting a basic technical pipeline working. My first step will be setting up MediaPipe hand tracking and making sure I can reliably capture hand landmark data from a webcam. Secondly, I want to bring that data into TouchDesigner and test simple mappings between gesture and sound, such as using hand height to control filter cutoff or the distance between fingers to control the amount of reverb. Once I can successfully connect one gesture to one vocal effect, I want to start to build a more expressive system with multiple mappings between movement and sound. After that, I plan to practice performing with this system with live vocal input in Ableton Live and refine it based on how responsive, stable, and musically useful it feels in performance.

### Questions and Concerns

My biggest concern is MediaPipe, mainly because I am completely new to it and have not actually used it before. I think a large part of this project will simply be learning the basics well enough to build a working pipeline. Because of that, one challenege is that I may need much more time than expected just to understand the setup, workflow, and limitations of the tool. 

I am also not yet sure how well MediaPipe will track two hands at the same time in a performance situation, especially if both hands are moving quickly or making different gestures. Another question I have is how reliably it can recognize each hand as separate, so that the system does not confuse my left and right hands when they are doing different things. Beyond that, I am concerned about tracking accuracy, latency, and whether the gesture data will be stable enough to use for real-time musical control. 

For now, I plan to rely on MediaPipe’s pretrained hand-tracking model to extract gesture data and build my system around that. If time and technical progress allow, one of my stretch goals is to go further and train my own gesture mappings using a tool like Wekinator, so that the system can recognize more complex or personalized gestures. 