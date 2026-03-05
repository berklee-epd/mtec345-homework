# Lab 4: Neural Networks in PyTorch

## 1. Study Process Overview

I used my Claude account and signed into the Claude plugin on VS Code, you can do the same thing in the Claude plugin that you can do in Cursor. I also used the Claude Code app to explain things to me as I scroll through it. I asked it to explain the training process a little bit more. I don't yet completely understand it, however, I do understand it quite a bit better. I still don't know much about the magic functions like nn.CrossEntropyLoss() and torch.optim.Adam(model.parameters(), lr=LR). But Claude showed me some places that I could go to learn more. I asked about one big chunk and dug down on parts until I understood it all.

## 2. Understanding Inventory

### What I Understand

I understand the data parsing pretty well. I was not very fluent in pandas, but the walkthrough helped. The encoding and decoding I get and I also get how we put all the chords in a sequence and line them up for the inputs.

I also understand classes very well. The dunder methods make sense to me and also the `def forward(self, x):` makes sense as a callback. Also inheritance makes sense to me and I understand what it's doing and how the whole object oriented stuff works.

I understand how the progressions are getting split up into test data and training data. I also understand the windowing thing where the first four chords are the input and the correct output is the fifth chord. I also understand the thing where the next window and output is only one chord over.

### What I Don't Understand

I don't quite get the training process, and how exactly it changes the weights. I also don't understand how when training, running through the same dataset 10 times helps the training process. I also don't yet get how the training data gets stored, or how the weights and biases get stored in memory and how to save it to disk.

I also don't understand everything in the nn.Module. I have no idea what it brings, and I also don't know exactly how PyTorch stores all the processes for back prop. In the same vein, I don't know the different "modes" of a nn.Module, like I know there's model.eval() and model.train(), and I don't know what torch.no_grad is.

I don't know the math or theory behind some basic AI stuff. Like I don't know the nn.CrossEntropyLoss(), but it sounds like from Claude that it is some sort of standard loss function, but I would want to dig in and figure out what it is and how it works. I also want to know what the Adam optimizer is from torch.optim.Adam(model.parameters(), lr=LR).

## 3. Model Limitations

The data treats all songs equally. If I'm honest, there are probably songs in there that I don't want to train my model on, or at least you could weigh different genres differently. Or maybe more succinctly, it does not account for genre at all and treats all chord progressions as the same type of progression.

The hidden layer is super small. It is probably limited by the fact that there is only one and it's super small. This could be easily fixed by putting some more layers in and or increasing the size of them. I will probably try to do that for my improvement to see if I can.

One more limitation is that it has no other information about the chord and can't ever make 7 or modal interchange chords. It will not be able to do that because it's not in the training data or in the encoding at all, but if you added it to the training data and you also added it to the encoding and decoding functions, it would be able to.

## 4. Improvement or Experiment

In the final output, one of them for this seed is V I V I. So I tried to add more layers to see what would happen. It didn't do much, so I tried to increase the EPOCHS, and that made it way worse so I decreased it and then tried to run it with the second most common chord, and it was a little better but not tons. So then I experimented with the window size. It worked but it did not fix the problem.

## 5. Creative Possibilities

I need to figure out how the training process works a little bit better and then I would love to experiment with the training process. I would like to see if I could get the other data sets working and see what kind of chords it would make. I also would like to try and make an inference function that takes the most common and the second and third most common randomly. It would be interesting to see if I could encode song position with the chords so the model might get some sense of song structure with the chords.
