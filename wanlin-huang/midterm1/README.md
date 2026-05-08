# Midterm Project: Voice Cloning with RVC and ElevenLabs

## What I Did

For this project, I wanted to see how far I could push voice cloning using my own voice.

I worked with two tools:
- RVC (open-source, train-it-yourself)
- ElevenLabs (commercial voice cloning)

I recorded around 10 minutes of my own voice, including both speaking and some singing, and tried to train an RVC v2 model on a Windows machine (RTX 4070 Ti).

The process was much more complicated than I expected. I had to:
- record and clean my own dataset
- slice the audio into 61 segments
- run feature extraction (RMVPE)
- attempt training (~300 epochs)

At the same time, I used ElevenLabs as a comparison point to understand what a “working” voice clone sounds like.

---

## How Machine Learning Is Involved

RVC is a machine learning system that learns the characteristics of a voice and tries to map other voices into it.

From what I understood during the process, it uses models like HuBERT to extract speech features, and then trains something like a VITS-based model to match the tone and identity of the target voice.

In contrast, ElevenLabs feels like a black box. You upload data, and it just works. I don’t know the exact architecture, but the results show that it is highly optimized for usability and clean output.

Comparing these two approaches helped me understand the difference between:
- open-source systems (more control, but difficult setup)
- commercial systems (easy to use, but less transparent)

---

## What I Learned

This project pushed me far outside my comfort zone technically. I had never set up a machine learning training pipeline before.

Some key things I learned:

- Dependency management is extremely important — numpy, numba, and PyTorch conflicts caused repeated failures
- Audio preprocessing matters — slicing, normalization, and feature extraction all affect the training process
- The difference between training and inference became very clear
- Commercial tools like ElevenLabs prioritize usability, while open-source tools require much more setup but offer deeper control

---

## Reflection

The biggest challenge was the environment setup. Dependency conflicts between numpy, numba, and PyTorch caused repeated failures across two machines.

I started on a Mac (M2 Pro, 32GB), but eventually switched to a Windows machine with an RTX 4070 Ti to deal with CUDA requirements.

I spent an entire day trying to get RVC fully running. Every fix introduced a new problem — fixing PyTorch broke numpy, fixing numpy broke numba, and so on. The model never successfully completed training in a usable way.

Even though this was frustrating, it was also one of the most important parts of the project. I realized that setting up ML systems is not just a small step — it is a major part of the work.

The contrast with ElevenLabs was very clear. It worked immediately, but the output revealed something interesting.

I am not a native English speaker, and my accent is part of my voice. However, ElevenLabs noticeably smoothed my accent toward a more “standard” American English sound.

Also, something felt missing emotionally. In my recordings, I spoke with real enthusiasm — especially when talking about things I care about (like dogs). But in the generated voice, that emotional quality was gone.

This made me think that voice cloning models capture surface features (timbre, pronunciation), but not the lived experience or emotional intent behind a voice.

This gap between technical accuracy and human expression became the most important takeaway from this project.

---

## Results

- ElevenLabs voice clone: successfully generated audio and used for comparison
- RVC v2:
  - Dataset prepared (61 segments)
  - Feature extraction completed
  - Training attempted but not successfully completed due to dependency conflicts

🎧 ElevenLabs Audio Output:  
[Paste your Google Drive link here]

---

## Notes on AI Usage

I used AI tools (including ChatGPT,cursor and claude) to help troubleshoot errors, understand model architecture, and debug environment issues.

All implementation decisions, debugging, and reflections were based on my own process and experience.