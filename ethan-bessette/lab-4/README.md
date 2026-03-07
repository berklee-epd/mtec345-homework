# Lab 4 Documentation

## Study Process
I commented up the code for what I understood, and used AI chat agent to explain code I didn't quite understand. Lines I asked about are listed in this section, and the explanation in my words is in the Understanding Inventory section.

CHORDS = sorted(set(all_chords))
- set: creates a set of the data (removes duplicates)
- sorted: creates a new ordered list (eg ascending by number or alphabetical)

stoi = {chord: i for i, chord in enumerate(CHORDS)}
- dictionary comprehension


Running a model like model() requires the input to be (batch_size, input) which is why

> x = encode_sequence(input_chords).**unsqueeze(0)**

Is needed.

## Understanding Inventory

**Load the data**: store the csv in a pandas dataframe, re-save the chords column into lists split around the | character

**Build the vocabulary:**
- create a new list all_chords, if a song contains a list of chords, concatenate them into the new list so that it is a list of all the chords in the dataset from all the songs back to back
- create a new list CHORDS of all unique chords in ascending order
- create a new int VOCABULARY_SIZE the number of unique chords
- create a dictionary stoi
    - chord: i is the actual mapping
    - for i, chord is like (i, chord)
    - enumerate returns pairs of index and the chord at that index
    - so it returns the chord and its index for the mapping
    - in other words, maps each chord to its index

**Define Encoding Functions:**
- encode
    - get index of each chord from dictionary
    - make a vector full of zeros the size of all unique chords
    - replace the vector position of the chord index with 1.0
    - length should be window size * vocab size

- decode
    - get the indices of the max value of the vector (this will be the index of the chord in the list of unique chords)
    - returns the chord at that index

- encode_sequence
    - concatenates each one hot encoding into a new tensor and flattens it so it becomes 1 dimension

**Create Training Pairs:**
- for ONE song:
    - input window size
    - for total CHORDS in SONG - window size
        - save a tuple of (4 chords, next chord)
        - move the window 1 chord down
- for chords in df["chords"] if chords, create pair, extend all pairs.

more pythonic way:
```python
all_pairs = [
    (chords[i : i + WINDOW_SIZE], chords[i + WINDOW_SIZE])
    for chords in df["chords"] if chords
    for i in range(len(chords) - WINDOW_SIZE)
]
```

**Encode Input and Target, split into train and test sets:**
- into a list, encode each chord in the list of input chords in all the pairs (list of tensors), stack the list into a new tensor (dim=0) so it becomes a tensor of lists rather than a tensor of tensors (shape should be (len(all_pairs), window_size*vocab_size)
```python
X = torch.stack([encode_sequence(input_chords) for input_chords, _ in all_pairs])
```

- into a list, add the index of the target chord for each pair in all the pairs, make the list a tensor
```python
y = torch.tensor([stoi[tgt] for _, tgt in all_pairs])
```

**Shuffle and Split data into train and test sets**
- create a new integer equal to 80% of length of X, training cutoff
- create a new tensor of random numbers in range and length of X
    - torch.randperm()
    - each value in this tensor is therefor an index in X
- when a 1d tensor is passed to another tensor like X[tensor], the input tensor acts as a list of indexes and it outputs a tensor of a list of values returned for each index
- X_train is defined as X[random_indices[:train_cutoff]] and same with y
- X_test is defined as X[random_indices[train_cutoff:]] and same with y

**Defining the model**
```python
class NextChordPredictor(nn.Module):
    def __init__(self):
        super().__init__()
        self.hidden = nn.Linear(INPUT_DIM, HIDDEN_DIM)
        self.output = nn.Linear(HIDDEN_DIM, VOCABULARY_SIZE)

    def forward(self, x):
        x = self.hidden(x)
        x = torch.relu(x)
        x = self.output(x)  # Raw logits
        return x
        
class NextChordPredictor(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(WINDOW_SIZE * VOCAB_SIZE, HIDDEN_DIM),
            nn.ReLU(),
            nn.Linear(HIDDEN_DIM, VOCAB_SIZE),
        )

    def forward(self, x):
        return self.net(x)  # raw logits
```

The sequential version automatically chains inputs to outputs like in the first version of the forward function. This allows sequences of modules to be considered its own module


Creates model with 1 hidden layer of HIDDEN_DIM neurons with window_size*vocab_size input size, HIDDEN_DIM output size), and an output layer of HIDDEN_DIM input size and vocab_size output size

**Predict next chord (inference mode)**
- Put model in evaluation mode.
- Perform one batch with one set of input chords in no gradient descent mode
- get the probability of logits by using softmax
    - dim=1 is needed because unsqueezed is used before to specify one batch
- get top predictions by using tuple torch.topk(probabilities_of_batch_0, top_k_predictions: returns top_probabilites and their corresponding one-hot indices
- return type is a list of tuples (index converted into chords symbol, probability)


**Setup training**
- set up loss function and optimizer function using built in torch

**Training loop**
- create int number of epochs and batch size
- for each epoch
    - put model in train mode
    - shuffle training data by using similar method as when splitting all data
        - tensor of randomized indices of X_train
    - counter for index of batches
    - float for total loss
    - for i in range(0, len(X_train), batch_size) increments by batch size through total training data
        - creates a batch index tensor that splits the random indices tensor into windows of batch size
        - defines X_batch and y_batch as training data at each batch index
        - loss function can take in (raw_logits, target_as_vocab_index)
        - reset gradients of all parameters
        - perform a backwards pass with loss function (compute gradient of current model)
        - perform one optimization based on gradient
        - increment loss for this batch to total loss
        - increment batch
    - every 10 epochs
        - set to evaluation mode
        - average loss: total_loss / num_batches
        - with no gradient descent:
            - convert tensor of logits to tensor of index of largest (so basically the index of most likely chord
            - convert that tensor into a list of true or false compared with the index of the correct chord, then convert true and false to floats, get the mean of the entire tensor, and return as a float.

**Evaluate the model**
- set to evaluate mode
- with no gradient descent
- get logits
- get argmax (index of highest value per index)
- same as above, compare predicted chord with test chord, but this time sum all the correct ones and convert to number, divide by length of test values and that determines overall percent correct


## Model Limitations
1. It often gets stuck in loops when using the most likely chord, although that kinda makes sense because music is about breaking expectations to create interest
2. The dataset is weighted heavier towards certain chords, like I IV and V, which might skew representation. Even if those chords are used less often in pop music, when training a model to predict the next chord when encountering it, it should still be trained evenly on what to do.

## Improvement and Experimentation
1. For generating a song, it improved the output by getting the randint(1,3) most likely next chord.
2. Increased epocs and used smaller batch size. The smaller batch size runs the loss and optimizer more and I feel like it marginally improved the model.
3. I experimented with a different learning rate. It made the model much worse.

## Creative Possibilities
It could be neat to combine a sound generation model to follow the chord progression created with this model.

