# %% [markdown]
# # Next Chord Prediction with a Neural Network
#
# In this notebook, we'll train a neural network to predict the **next chord**
# in a progression.
#
# Given a sequence like `["I", "IV", "V", "I"]`, the model will learn to predict
# what chord typically comes next in popular music.
#
# We'll use the one-hot encoding techniques from the previous notebook
# (`assignment.py`).

# %% Setup
import torch
import torch.nn as nn
import pandas as pd
from collections import Counter

# Set random seed for reproducibility
torch.manual_seed(42)

# Configuration
INPUT_SEQUENCE_LENGTH = 4

# %% [markdown]
# ---
# ## Step 1: Load and Prepare the Dataset

# %% Load the data
df = pd.read_csv("./billboard_numerals_simple.csv")
df["chords"] = df["chords"].str.split("|")
print(f"Loaded {len(df)} songs")
df.head()

# %% Build the vocabulary
all_chords = []
for chord_list in df["chords"]:
    if chord_list:
        all_chords.extend(chord_list)

CHORDS = sorted(set(all_chords))
VOCABULARY_SIZE = len(CHORDS)
stoi = {chord: i for i, chord in enumerate(CHORDS)}

print(f"Vocabulary ({VOCABULARY_SIZE} chords): {CHORDS}")

# %% [markdown]
# ---
# ## Step 2: Define Encoding Functions
#
# These are the same functions from `assignment.py`.


# %%
def encode(chord):
    """One-hot encode a chord symbol."""
    index = stoi[chord]
    vector = torch.zeros(VOCABULARY_SIZE)
    vector[index] = 1.0
    return vector


def decode(vector):
    """Decode a one-hot vector (or logits) back to a chord symbol."""
    index = torch.argmax(vector).item()
    return CHORDS[index]


def encode_sequence(chords):
    """Encode a list of chords as a flat tensor."""
    encoded = [encode(c) for c in chords]
    return torch.stack(encoded).flatten()


# Test
print(f"encode('I') = {encode('I')}")
print(f"encode_sequence(['I', 'IV', 'V', 'I']).shape = {encode_sequence(['I', 'IV', 'V', 'I']).shape}")

# %% [markdown]
# ---
# ## Step 3: Create Training Pairs
#
# For each song, we'll create multiple training examples using a **sliding window**:
#
# - Input: chords at positions [i, i+1, i+2, i+3]
# - Target: chord at position [i+4]
#
# This way, one song with 100 chords gives us ~96 training examples!

# %% Create training pairs
def create_training_pairs(chord_list, window_size=INPUT_SEQUENCE_LENGTH):
    """
    Create (input, target) pairs from a chord progression.

    Input: window_size consecutive chords
    Target: the next chord after the window
    """
    pairs = []
    for i in range(len(chord_list) - window_size):
        input_chords = chord_list[i : i + window_size]
        target_chord = chord_list[i + window_size]
        pairs.append((input_chords, target_chord))
    return pairs


# Test on one song
sample_chords = df.iloc[0]["chords"]
sample_pairs = create_training_pairs(sample_chords)
print(f"Song has {len(sample_chords)} chords → {len(sample_pairs)} training pairs")
print(f"\nFirst 3 pairs:")
for inp, tgt in sample_pairs[:3]:
    print(f"  {inp} → {tgt}")

# %% Create all training pairs
all_pairs = []
for _, row in df.iterrows():
    if row["chords"] and len(row["chords"]) > INPUT_SEQUENCE_LENGTH:
        pairs = create_training_pairs(row["chords"])
        all_pairs.extend(pairs)

print(f"Total training pairs: {len(all_pairs)}")

# %% Look at target distribution
target_counts = Counter(tgt for _, tgt in all_pairs)
print("\nTarget chord distribution:")
for chord, count in target_counts.most_common():
    pct = count / len(all_pairs) * 100
    print(f"  {chord:5s}: {count:5d} ({pct:5.1f}%)")

# %% [markdown]
# ---
# ## Step 4: Prepare Tensors
#
# Convert our pairs into tensors for training.

# %% Encode all pairs
X_list = []
y_list = []

for input_chords, target_chord in all_pairs:
    x = encode_sequence(input_chords)
    y = stoi[target_chord]  # Just the index for CrossEntropyLoss
    X_list.append(x)
    y_list.append(y)

X = torch.stack(X_list)
y = torch.tensor(y_list)

print(f"X shape: {X.shape}")  # (num_pairs, INPUT_SEQUENCE_LENGTH * VOCABULARY_SIZE)
print(f"y shape: {y.shape}")  # (num_pairs,)

# %% Split into train and test sets (80/20)
n_train = int(0.8 * len(X))
indices = torch.randperm(len(X))

train_idx = indices[:n_train]
test_idx = indices[n_train:]

X_train, y_train = X[train_idx], y[train_idx]
X_test, y_test = X[test_idx], y[test_idx]

print(f"Training samples: {len(X_train)}")
print(f"Test samples: {len(X_test)}")

# %% [markdown]
# ---
# ## Step 5: Define the Model
#
# A simple MLP (multi-layer perceptron) with one hidden layer.
#
# ```
# Input (40) → Hidden (16) → Output (10)
# ```

# %%
INPUT_DIM = INPUT_SEQUENCE_LENGTH * VOCABULARY_SIZE  # 4 * 10 = 40
HIDDEN_DIM = 16


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


model = NextChordPredictor()
print(model)

# Count parameters
total_params = sum(p.numel() for p in model.parameters())
print(f"\nTotal parameters: {total_params}")
print(f"  Hidden layer: {INPUT_DIM} × {HIDDEN_DIM} + {HIDDEN_DIM} = {INPUT_DIM * HIDDEN_DIM + HIDDEN_DIM}")
print(f"  Output layer: {HIDDEN_DIM} × {VOCABULARY_SIZE} + {VOCABULARY_SIZE} = {HIDDEN_DIM * VOCABULARY_SIZE + VOCABULARY_SIZE}")

# %% Interactive prediction function
def predict_next_chord(input_chords):
    """Predict the next chord given a sequence."""
    model.eval()
    with torch.no_grad():
        x = encode_sequence(input_chords).unsqueeze(0)
        logits = model(x)
        probs = torch.softmax(logits, dim=1)

        # Get top 3 predictions
        top_probs, top_indices = torch.topk(probs[0], k=4)

        return [(CHORDS[idx], prob.item()) for idx, prob in zip(top_indices, top_probs)]


# Test some progressions
test_progressions = [
    ["I", "IV", "V", "I"],
    ["I", "V", "vi", "IV"],
    ["i", "VI", "VII", "i"],
    ["I", "I", "I", "I"],
    ["V", 'bVII', 'i', 'ii']
]

print("Sample predictions:\n")
for prog in test_progressions:
    predictions = predict_next_chord(prog)
    print(f"Input:{','.join([f"{c:>5s}" for c in prog])}     ➡️    {predictions[0][0]}")
    print(f"Output: ", end="")
    for chord, prob in predictions:
        print(f"{chord} ({prob:.0%})", end="  ")
    print("\n")

# %% [markdown]
# ---
# ## Step 6: Train the Model

# %% Setup training
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# %% Training loop
num_epochs = 50
batch_size = 64

for epoch in range(num_epochs):
    model.train()

    # Shuffle training data
    perm = torch.randperm(len(X_train))
    total_loss = 0.0
    num_batches = 0

    # Mini-batch training. Count from 0 -> 12023 in steps of 64 (batch size)
    for i in range(0, len(X_train), batch_size):
        batch_idx = perm[i : i + batch_size]
        X_batch = X_train[batch_idx]
        y_batch = y_train[batch_idx]

        # Forward pass
        logits = model(X_batch)
        loss = loss_fn(logits, y_batch)

        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        num_batches += 1

    # Print progress every 10 epochs
    if (epoch + 1) % 10 == 0:
        avg_loss = total_loss / num_batches

        # Evaluate on train and test
        model.eval()
        with torch.no_grad():
            train_pred = torch.argmax(model(X_train), dim=1)
            train_acc = (train_pred == y_train).float().mean().item()

            test_pred = torch.argmax(model(X_test), dim=1)
            test_acc = (test_pred == y_test).float().mean().item()

        print(f"Epoch {epoch + 1:3d} | Loss: {avg_loss:.4f} | Train: {train_acc:.1%} | Test: {test_acc:.1%}")

# %% [markdown]
# ---
# ## Step 7: Evaluate the Model

# %% Final accuracy
model.eval()
with torch.no_grad():
    logits = model(X_test)
    predictions = torch.argmax(logits, dim=1)
    correct = (predictions == y_test).sum().item()
    accuracy = correct / len(y_test)

print(f"Test accuracy: {accuracy:.1%}")
print(f"Correct: {correct} / {len(y_test)}")

# %% Accuracy by target chord
print("\nAccuracy by target chord:")
for i, chord in enumerate(CHORDS):
    mask = y_test == i
    if mask.sum() > 0:
        chord_correct = (predictions[mask] == y_test[mask]).sum().item()
        chord_total = mask.sum().item()
        chord_acc = chord_correct / chord_total
        print(f"  {chord:5s}: {chord_acc:5.1%} ({chord_correct}/{chord_total})")

# %% [markdown]
# ---
# ## Step 8: Make Predictions
#
# Let's see the model in action!

# %% Interactive prediction function
print("Sample predictions:\n")
for prog in test_progressions:
    predictions = predict_next_chord(prog)
    print(f"Input: {prog}")
    print(f"  Predictions: ", end="")
    for chord, prob in predictions:
        print(f"{chord} ({prob:.0%})", end="  ")
    print("\n")

# %% Show some test examples
print("Sample test predictions:\n")
for i in range(min(15, len(X_test))):
    # Get original pair
    original_idx = test_idx[i].item()
    input_chords, actual = all_pairs[original_idx]

    # Make prediction
    with torch.no_grad():
        logits = model(X_test[i].unsqueeze(0))
        probs = torch.softmax(logits, dim=1)
        pred_idx = torch.argmax(logits, dim=1).item()
        confidence = probs[0, pred_idx].item()

    predicted = CHORDS[pred_idx]
    status = "✓" if predicted == actual else "✗"

    print(f"{status} {input_chords} → Predicted: {predicted} ({confidence:.0%}), Actual: {actual}")

# %% [markdown]
# %% [markdown]
# ---
# ## Summary
#
# This file contains a machine learning pipeline:
#
# 1. **Load data**: Read CSV, parse chord lists
# 2. **Create pairs**: Sliding window over each song
# 3. **Encode**: One-hot encode inputs, integer indices for targets
# 4. **Split**: 80/20 train/test
# 5. **Model**: Simple MLP (40 → 16 → 10)
# 6. **Train**: CrossEntropyLoss + Adam optimizer
# 7. **Evaluate**: Test accuracy, per-chord breakdown
# 8. **Predict**: Apply to new chord progressions
#
# This is the core workflow for most sequence prediction tasks in deep learning!
