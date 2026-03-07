# Lab 4: Neural Networks in PyTorch

## 1. Study Process Overview

### Questions I Asked

I went through each cell and asked Gemini what the cell is overall doing in this script, and it did a great job helping me understand the big picture of each cell.

I asked what lines 61–62 are doing, and it said they apply `argmax` along the vocabulary dimension (`dim=-1`) to get the indices for each prediction in the batch, then map each index to its chord name. I still don’t quite understand why we need to return this value in the encoding cell.

I asked why we need `y = torch.tensor([stoi[tgt] for _, tgt in all_pairs])`, and it told me that without it, we would only have the encoded inputs (`X`) but no numerical labels (`y`) to compute the loss against. It also said that this line builds the target vector that the network is trying to predict. I still don’t understand how this single line does all of that.

I asked what lines 93–97 are doing, and it told me that `perm[:n_train]` gives the first 80% of the randomized indices, which selects that many examples for the training set, while `perm[n_train:]` gives the remaining 20%, which becomes the test set. I still don’t understand how this works just from these lines.

---

## 2. Understanding Inventory

### Imports and Config

It imports the libraries of `torch` and `pandas`.

It also configures several variables, including `WINDOW_SIZE` (how many chords are used as inputs), `HIDDEN_DIM` (the size of the hidden layer), `BATCH_SIZE` (how many training examples are processed at once during each training step), `EPOCHS` (how many times the model runs through the training dataset), and `LR` (the learning rate, which controls how much the model’s weights are adjusted during each update).

---

### Step 1: Load Data and Build Vocabulary

`df = pd.read_csv("./billboard_numerals_simple.csv")` loads the chord data into a pandas DataFrame.

`df["chords"] = df["chords"].str.split("|")` converts the chord strings into lists of individual chords.

Lines 32–36 flatten all the chord lists into one long list and skip any empty entries.

`CHORDS = sorted(set(all_chords))` creates a sorted list of unique chord names and removes duplicates.

`VOCAB_SIZE = len(CHORDS)` counts how many unique chords there are and stores this number as the vocabulary size.

`stoi = {chord: i for i, chord in enumerate(CHORDS)}` creates a mapping from each chord name to its index position in the `CHORDS` list.

`print(f"Loaded {len(df)} songs | Vocabulary ({VOCAB_SIZE}): {CHORDS}")` displays how many songs were loaded, the vocabulary size, and the list of chords.

---

### Step 2: Encoding

Lines 49–52 create a one-hot encoded vector for a single chord.

Lines 54–55 convert a list of chords into a flattened 1D one-hot tensor.

For lines 57–62, I understand that it finds the highest value using `torch.argmax` and then looks up the chord name in the `CHORDS` list. However, I don’t fully understand what the rest of the code is doing. I’m also not sure why this step is needed in the encoding process.

---

### Step 3: Build Training Pairs (Sliding Window)

`for chords in df["chords"] if chords` loops through each song’s chord list and skips any empty ones.

`for i in range(len(chords) - WINDOW_SIZE)` means that for each song, it creates sliding windows starting at positions 0, 1, 2, … as long as there is still a next chord available.

`(chords[i : i + WINDOW_SIZE], chords[i + WINDOW_SIZE])` means that for each position `i`, it takes a slice of `WINDOW_SIZE` chords as the input and the next chord as the target.

Lines 79–80 print the total number of training pairs and show the first example.

---

### Step 4: Encode and Split

I understand that `X = torch.stack([encode_sequence(inp) for inp, _ in all_pairs])` means that for each training pair, it takes the input chord sequence, creates a flattened one-hot vector, and stacks all the encoded inputs into a 2D tensor. However, I don’t understand why we need to flatten again, because I thought we had already done the one-hot encoding before.

I kind of understand that `y = torch.tensor([stoi[tgt] for _, tgt in all_pairs])` converts each target chord into its vocabulary index using `stoi` and creates a 1D tensor. But I don’t understand why we are doing that. Is this line defining what we are trying to predict?

Lines 90–91 mean that we are using 80% of the data for training and randomly shuffling the indices with `torch.randperm`.

I don’t understand what lines 93–97 are doing. I know that they are keeping the inputs and targets matched.

`TensorDataset(X_train, y_train)` pairs the inputs and labels together so they stay synchronized.  

`DataLoader(..., batch_size=BATCH_SIZE, shuffle=True)` produces an iterator that yields mini-batches of size 64 and shuffles the samples each epoch.

`print(f"X shape: {X.shape}  |  Train: {len(X_train)}  |  Test: {len(X_test)}")` prints the tensor shapes and dataset sizes.

---

### Step 5: Define the Model

`class NextChordPredictor(nn.Module):` inherits from PyTorch’s base module class.

`__init__` initializes the network layers inside a sequential container.

`super().__init__()` calls the parent class’s `__init__` method.

`self.net = nn.Sequential(...)` creates a sequential container that chains the layers together in order.

`nn.Linear(WINDOW_SIZE * VOCAB_SIZE, HIDDEN_DIM)` defines the first fully connected layer.

`nn.ReLU()` applies the ReLU function element-wise to the hidden layer output so the network can learn complex and non-linear relationships between chord sequences and predictions.

`nn.Linear(HIDDEN_DIM, VOCAB_SIZE)` defines the output layer that maps the hidden layers to `VOCAB_SIZE` logits.

Lines 122–123 define the `forward` method, which specifies how input data flows through the network.

Lines 125–127 create the model instance, print its structure, and count the number of trainable parameters.

---

### Step 6: Train

`def predict_next(chords, top_k=4):` defines a function that takes a chord sequence and an optional number of top predictions to return.

`model.eval()` switches the model to evaluation mode and disables training-specific behaviors like dropout or batch normalization updates.

`with torch.no_grad():` creates a context where gradients are not computed. This saves memory and speeds up inference.

`encode_sequence(chords)` converts the chord list into a flattened numerical vector.

`.unsqueeze(0)` adds a batch dimension, so the shape becomes `[1, input_size]`.

`model(...)` runs the input through the neural network and produces raw logits of shape `[1, VOCAB_SIZE]`.

`probs = torch.softmax(logits, dim=1)[0]` applies softmax along the vocabulary dimension to convert logits into probabilities that sum to 1.

`top_probs, top_idx = torch.topk(probs, k=top_k)` finds the highest probabilities and their corresponding indices in the vocabulary.

`zip(top_idx, top_probs)` pairs each top index with its corresponding probability.

`CHORDS[i]` looks up the chord name using the index `i`.

`p.item()` converts the PyTorch tensor `p` into a regular Python float.

Lines 147–152 is a set of test inputs.

Lines 154–157 is a for loop that runs each of the progressions through the model and prints the result.

Lines 160–161 set up the loss function and optimizer.

I don’t quite understand how lines 163–166 specifically work. I know they are related to measuring or improving accuracy, but I’m not sure how they operate.

Lines 168–176 show that for each epoch, the loop switches the model into training mode and goes through every mini-batch in `train_loader`.

Lines 179–181 print the average batch loss and the current training/testing accuracy.

---

### Step 7: Evaluate

Lines 188–190 make a forward pass over all test examples and select the highest-scoring chord index for each prediction.

`print(f"\nOverall test accuracy: {(preds == y_test).float().mean().item():.1%}\n")` prints the overall test accuracy.

Lines 194–198 loop through each chord in the vocabulary, filter the test examples that belong to that chord class, and print that chord’s prediction accuracy along with the number of samples for that class.

---

### Step 8: Predict

Lines 206–211 is a set of test inputs.

Lines 214–217 is a for loop that runs each of the progressions through the model and prints the result.

Lines 221–228 initialize a 4-chord starting sequence and then generate 12 more chords by repeatedly predicting the most likely next chord based on the current 4-chord window. After each prediction, the window slides forward by one chord, while all chords are collected into a final progression.

I understand that lines 230–232 print the final progression, but I don’t fully understand how those lines of code actually create the output format.

---

## 3. Model Limitations

1. The model only analyzes the chords and ignores rhythm, even though rhythm is very important in music. It affects where the chords are placed in the measure and whether they land on strong beats or weak beats. These factors matter and should influence the model’s chord predictions.

2. The model only uses a fixed window, but songs have larger structures and phrases. It should also be able to understand the overall form of the song so it can make better predictions depending on which part of the song it is in.

---

## 4. Improvement or Experiment

I changed the `WINDOW_SIZE` to 3 because it is more common to have 4 chords in a progression, so the first 3 chords can be used to predict the last one. I also removed the last chord in `test_progressions` and replaced the 4s in lines 230–232 with 3. The final result still looks fine to me.

---

## 5. Creative Possibilities

How to make the model learn that in music we have structures such as intro, verse, chorus, etc. It would be nice to include that information in the model so it is not just predicting chords freely, but also taking measures and song sections into consideration.

---