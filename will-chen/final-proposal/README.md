# MTEC-345 Final Project Proposal

## What I Want to Build

I’m planning to build a neural network controlled synthesizer in SuperCollider. The system will map a 2D XY control interface to different synthesis parameters, making complex sound design to be controlled through a simple interface.

![SuperCollider](SuperCollider.jpg)

---

## Why This Project Matters

I want to do this project because I want to discover a new way of doing sound design. By adding machine learning to synthesis, it might generate results that are uncommon compared to my usual workflow. If it works well, I can use this system as a prototype and modify it in the future to control different synthesis parameters and create new sound textures that I can use in my own music production.

---

## Machine Learning, Data, Tools, and Workflow

This project will use a multilayer perceptron (MLP) to map a simple control input to complex synthesis parameters

#### Data Structure

- Input: XY position (2 values)  
- Output: synthesis parameters  

#### Approach

I will create a dataset of input-output pairs by designing sounds and assigning each one to a position in the XY space. These pairs will be stored and used to train the model. During training, the neural network will learn to predict synthesis parameters from XY inputs by minimizing error between its predictions and the target values. Once it’s trained, I can move around the XY controller, and the model will generate new parameter values in real time which will then control the synth.

#### Tools

- SuperCollider for synthesis and interaction  
- FluCoMa (MLPRegressor) for the neural network  
- Buffers/datasets to store data  
- JSON files to save and reload everything  

---

## Development Plan

- Build the synth and XY interface  
- Collect training data (sound and position pairs)  
- Train the neural network and check how it performs  
- Connect it to real-time sound control  
- Test and refine  

---

## Questions and Concerns

- Since this project involves things beyond what I’ve used before, I will need to spend time doing additional research to fully understand how everything works.  
- I’m also unsure about the final result, whether the generated sounds will actually be useful musically or not.

---