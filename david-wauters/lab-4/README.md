# Lab 4: Neural Networks in PyTorch

## 1. Study Process Overview

I downloaded the Gemini extension and used my personal email to connect it to VSCode and elaborate on the code of nn_3.py. I began by asking it to explain every line of each step in the neural network. If there was something I did not understand, I'd home in on that line and ask it to elaborate further, but that didn't occur often. Eventually I would come across a term which I remember learning about but can't remember, so I would ask Gemini to remind me what the term means. Once I understood the term, I would then ask for it to further explain it within the context of the code it appears in. Some specific terms that I used this for are logits and argmax.

## 2. Understanding Inventory

### What I Understand

Step 2 is used solely so that the neural network can communicate with human understanding. If our brains worked the exact same as the neural network, this step would not be necessary. The one_hot function is used to convert what we understand as a chord into 0s and 1s, and the encode_sequence function does a similar process but for sequences of chords instead. Then once the neural network processes the information and has a prediction it can use the decode function to return it in a way which we'll understand.

Step 5 is the actual model itself, and is simply the neural network image we studied in class translated into python. Within the nn.Sequential function we see the skeleton of the neural network, with each line consisting of a layer using the hyper parameters defined in step 1. So line 117 uses the WINDOW_SIZE and VOCAB_SIZE to determine the inputs, and HIDDEN_DIM to determine the number of layers they'll get passed through. Then line 118 runs those processed inputs through the ReLU function, and then the 119 does the same process as 117. Then the forward function spits out the encoded logits to be decoded.

### What I Don't Understand

While I understand that the purpose of step 6 is to test predictions of the model before any training is done, there are specific aspects of it that do not make as much sense to me. The topk function is elusive to me, I understand it's part of returning probabilities but this new variable of K is unfamiliar to me. I'm unsure how relevant it is that the variable is referred to as K, and if it has some significance in other mathematics concepts.

I can comprehend what step 4 is doing, but I cannot parse that from just looking at the code. I'm able to see that it's dividing the data into two groups, specifically in an 80/20 split. In the earlier lines of that I'm able to somewhat get that from looking at the code, but only cause I remember us talking about it in class. by the time we get to the train_loader variable using the DataLoader I don't really understand what is being done, especially with the shuffle parameter.

## 3. Model Limitations

The way the model is currently built does not account for harmonic rhythm, both in terms of the length of chords and their placement in a phrase. Because of the sliding window of four chords, the actual phrase is not really considered as some sets of 4 chords will be awkwardly between two phrases and the neural network will produce a chord that makes sense in a vacuum but not in the greater context. And with the way the dataset is presented and interpreted, it only accounts for the location of a chord in the song and not its length, which can again produce a chord that may not make sense in the harmonic phrase because of placement.

The model uses one-hot encoding for the chords, which ends up ignoring any potential harmonic relationships between chords. Because the chords are just stored as numerical data, it doesn't account for things like cadential patterns or chord function. So the model does not understand that I & vi are both tonic chords or that ii and IV are both subdominant. Because of this, it is likely to give chord progressions which are technically logical but do not flow very well.

## 4. Improvement or Experiment

I tinkered with the HIDDEN_DIM and EPOCHS hyperparameters, as well as some different test progressions. What I found by reducing the two hyperparameters to 1 was exactly what I expected, they would produce just 1 chord (sometimes 2). After that I would drastically increase the hyperparameters until there were 1000 hidden dimensions and 100 epochs, but the results were not much more impressive. In the case of the original sample progression ['iv', 'IV', 'V', 'I'] no change in the hyperparameters produced any chords other than I, IV, and V, which I guess would be expected. I eventually tried another common progression of ['I', 'vi', 'ii', 'V'], and no matter what I made the hyperparameters it would only produce the exact same progression. The last thing I tried was putting in nonsensical progressions such as ['VI', 'bVII', 'V', 'ii'], which all produced the same two chords back in forth (in the case of this progression it only gave me V and ii). 

## 5. Creative Possibilities

It would be interesting to figure out how to include inversions in this model. The base model would have to have a bit more polish as it seems to struggle a bit with predicting root position chords as it is, but once that is achieved it would be interesting to see how the model would handle predicting if a chord should be inverted or not. There are certain genres that I think would benefit from this as inversions make up the context of their identity much more (namely classical and Brazilian music, surely others as well but those are genres I've studied).
