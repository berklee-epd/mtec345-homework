# Lab 4: Next Chord Prediction with a Neural Network

## 1. Study Process

I used Claude (AI assistant) to study `nn_2.py` line by line, starting from the very basics. I asked questions about every part of the code I didn't understand, and often had to ask follow-up questions like "I still don't understand" or "explain everything" before getting a clear answer.

**Questions I asked:**
- Why is the random seed 42? (It's a programmer joke from *The Hitchhiker's Guide to the Galaxy* — any number works the same way)
- What does `df.head()` do? (Shows the first 5 rows of the dataset as a sanity check)
- What is `enumerate()` and why do we use it? (It automatically adds index numbers to a list, like a roll call)
- How does the sliding window work, and why does a 100-chord song give 96 training pairs? (Because 100 - 4 = 96; the last window needs a target chord to predict)
- Why does the neural network only accept a flat vector, not a table? (The input layer is a single row of neurons, so data must be flattened first)
- How does `loss` know it made a mistake? (The correct answer `y` is always provided during training — this is supervised learning)
- What is a tensor? (A multi-dimensional number container; a matrix is just a 2D tensor)

**Where the AI was less helpful:**
- Sometimes explanations moved too fast and I had to ask the same question multiple times
- Occasionally gave too much information at once instead of one concept at a time

---

## 2. Understanding Inventory

### What I Understand

**Sliding Window (`create_training_pairs`)**
The function uses a window of 4 chords and slides it one step at a time across each song. A song with 100 chords produces 96 training pairs (100 - 4 = 96), because each window needs one chord after it to use as the target. This is an efficient way to extract many training examples from a small dataset.

**One-Hot Encoding (`encode`, `decode`, `encode_sequence`)**
Each chord is represented as a vector of 10 numbers, where only one position is 1 and the rest are 0. Four chords encoded and flattened together produce a 40-number input vector (4 × 10). The `decode` function reverses this by finding the position of the largest value using `argmax`.

**Training Loop (Step 6)**
Each epoch passes all training data through the model once. The loop uses mini-batches of 64 samples at a time (a power of 2, which is efficient for computer memory). For each batch: the model makes a prediction, `loss_fn` measures how wrong it was, `loss.backward()` computes the gradient, and `optimizer.step()` updates the parameters.

**Supervised Learning**
The model needs correct answers (`y`) during training to know how wrong its predictions are. This is why we prepare both `X` (inputs) and `y` (targets). Once training is done, we only need `X` to make new predictions.

**Neural Network as a Black Box**
The model has thousands of parameters that adjust during training. Nobody knows exactly what each number represents — what matters is whether the final predictions are accurate. This is why neural networks are often called "black boxes."

### What I Don't Understand

**`super().__init__()` internals**
I understand this line is required and initializes the `nn.Module` base class. However, I don't know what PyTorch is actually doing behind the scenes — what data structures are being set up, and why skipping this line would break the model.

**Gradient math**
I understand gradients conceptually as "slope" or "direction to improve," but I don't understand the actual math behind `loss.backward()`. How does PyTorch calculate the gradient for every parameter automatically?

**Why CrossEntropyLoss for this problem**
I know `CrossEntropyLoss` is used for classification problems, but I don't understand why it works better than other loss functions here, or what the mathematical difference is.

---

## 3. Model Limitations

**Limitation 1: Fixed vocabulary of 10 chords**
The model can only work with the 10 chord types it saw during training. If a new chord (e.g., a jazz chord like `IVmaj7`) appears in the input, the model cannot handle it. This means the model is tied to its specific dataset and cannot generalize to more complex or diverse music styles.

**Limitation 2: No long-range musical structure**
The model only looks at 4 chords at a time, so it has no awareness of larger musical structures like verses, choruses, or 8-bar phrases. Two identical 4-chord windows could appear in very different parts of a song, but the model treats them identically. Real music has structure at multiple levels that a fixed 4-chord window cannot capture.

**Limitation 3: No rhythm or timing information**
The model only sees chord names, not how long each chord lasts. A chord held for 4 beats feels very different from one held for half a beat, but both look the same to this model. This limits the model's musical usefulness, since rhythm is a fundamental part of how chord progressions feel.

---

## 4. Improvements and Experiments

I ran two experiments and compared them against the original model (`HIDDEN_DIM=16`, `lr=0.01`, `epochs=50`).

### Experiment 1: Larger Hidden Layer (`HIDDEN_DIM = 64`)

Changed the hidden layer from 16 to 64 neurons, increasing the model's capacity.

| | Original (16) | Experiment 1 (64) |
|---|---|---|
| Train accuracy | 75.4% | 76.9% |
| Test accuracy | 74.4% | 75.9% |
| Train-Test gap | 1.0% | 1.0% |
| Final loss | 0.6902 | 0.6265 |

The larger hidden layer improved test accuracy by 1.5% with no sign of overfitting (Train-Test gap stayed at 1%). This suggests the problem is simple enough that even 64 neurons don't cause the model to memorize the training data.

### Experiment 2: Smaller Learning Rate + More Epochs (`lr=0.001`, `num_epochs=100`)

Changed the learning rate from 0.01 to 0.001 and doubled the number of epochs to compensate.

| | Original | Experiment 2 |
|---|---|---|
| Train accuracy | 75.4% | 76.7% |
| Test accuracy | 74.4% | 75.5% |
| Train-Test gap | 1.0% | 1.2% |
| Final loss | 0.6902 | 0.6325 |

An interesting finding: at Epoch 10, this model had lower accuracy (71.6%) than the original (73.3%), because smaller steps mean slower early learning. By Epoch 100, results were similar to Experiment 1. This showed me that a smaller learning rate with more epochs can reach a similar destination — just more slowly and carefully.

---

## 5. Creative Possibilities

**Style-specific chord predictors (Fine-tuning)**

I would want to train separate models on specific musical styles — one trained only on pop songs, one on minor-key progressions, one on blues. Each model would learn the harmonic patterns specific to its genre. When composing, you could choose which "style model" to consult depending on the mood you want. This concept is called fine-tuning and is widely used in AI — for example, ChatGPT is first trained on general internet text and then fine-tuned specifically for conversation.

This idea directly addresses Limitation 1 (fixed vocabulary) and Limitation 2 (no style awareness): a genre-specific model trained on richer data could learn more nuanced patterns and serve as a genuine composition tool rather than just a statistical average of all popular music.