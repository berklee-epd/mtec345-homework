# Lab 4: Neural Networks in PyTorch

## 1. Study Process Overview

[Describe how you used AI to study `nn_2.py`. What questions did you ask? What did it help you understand?]
It really help me understand and memorize eazh variable because I often need to run back and check each value's definition, and i ask a lot about model.eval since it is confusing at first, but turns out it ia a similar idea in RAVE just freeze the neurons while predicticing so it does not come up with a total different result.
## 2. Understanding Inventory

### What I Understand

[For each part, write 2–3 sentences explaining it in your own words.]
Step1: loading the chord prog and split each chord with "|".Going through the dataset to find all different kind of chords and build a vocabularay for them(i from 0-10). and the if statment skips the empty list, and sorted excludes the duplicates.

Step2:encode part turns a single chord into a tensor of zeros with a single 1.0 at the index matching that chord. encode_sequence does this for multiple chords and joins them all into one long flattened tensor. 

Step3:create_training_pairs slides a window of 4 chords across a song, creating one (input, target) pair per position where the input is 4 consecutive chords and the target is the single chord that follows them(so it becomes [4,1]). And the loop for on every song in the dataset, skipping any songs shorter than 4 chords, and collects all pairs into one all_pairs list. After that, Counter counts how often each chord appears as a target, and the target distribution printout helps us spot this and decide whether we need to handle the imbalance during training.

Step4:
The code encodes every sequence into a flat tensor using one-hot encoding,and stores each target chord as a plain integer index rather than one-hot, torch.stack then combines all inputs into one big matrix X and torch.tensor wraps all targets into a single vector y. Finally, torch.randperm generates a random shuffling of indices which is used to split X and y into 75% training and 25% test sets.

Step5:
This part model takes the tensor X as input and passes it through two hidden layers with ReLU and Dropout,outputting 10 raw logits,one for each chord. predict_next_chord then runs a sequence through the trained model, converts the logits to probabilities with softmax, and returns the top 4 most likely next chords with their confidence scores.

Step6:The model is trained for 100 epochs using mini-batches of 64(process 64 tensors at atime and epoch means a full runthrough of the dataset), where each batch computes a forward pass, calculates CrossEntropyLoss, then backpropagates gradients to update the weights via Adam optimizer.

Step7:After training, the model is tested on the held-out test set by comparing its predicted chord (the argmax of the logits) against the actual target in eval mode(where we previos split the dataset into train and test), giving an overall accuracy plus a breakdown per chord.

Step8:
The trained model is applied to new chord progressions to generate real predictions, showing both the top predicted next chord and the confidence percentages for the top 4 candidates.


### What I Don't Understand
CrossEntropyLoss the input and output(datatype)and why? 
adam optimizer 
why do we need torch.no_grad() in predict_next_chord
with torch.no_grad(): in line 351

## 3. Model Limitations
Although it analyze each seq by 4 chords i think often time the imbalance happens because of the cadence of each section, i think that often bring difficulty to the predictions and although a lot of modern pop songs use 4 chord loop in chorus but The model always looks at exactly 4 previous chords, which may be too short to capture longer repeating patterns like an 8-bar verse structure.


## 4. Improvement or Experiment
Adding an extra hidden layer and adjusting the train/test split were straightforward modifications — the architecture is easy to extend since each layer just needs matching input and output dimensions. However the 1% accuracy drop likely happened because the added layer introduced more parameters that the model struggled to train effectively with the same number of epochs and learning rate. This is a common tradeoff: deeper models have more capacity but also need more careful tuning of hyperparameters like learning rate, dropout rate, and training duration to actually improve.


## 5. Creative Possibilities

One direction I'd like to explore is extending the model to identify structural sections of a song like verse, chorus, and bridge. Use that information as an additional input feature during chord prediction. The intuition is that chord choices are heavily tied to song position; a chorus tends to use more emotionally resolved chords like I and IV, while a bridge often introduces unexpected harmonic shifts to create tension. If the dataset included section labels, you could one-hot encode the current section alongside the chord sequence, giving the model richer context beyond just the last 4 chords. This could meaningfully improve accuracy because the model would no longer treat a verse I to V and a chorus I to V identically and maybe it would learn that the same progression resolves differently depending on where it sits in the song's structure.
