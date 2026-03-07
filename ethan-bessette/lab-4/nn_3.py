# %% [markdown]
# # Next Chord Prediction with a Neural Network
#
# Given a sequence like `["I", "IV", "V", "I"]`, the model learns to predict
# what chord typically comes next in popular music.
#
# This is more concise than nn_2.py. It uses higher-level abstractions and
# hides more of the implementation.

# %% Imports and config
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
import pandas as pd

torch.manual_seed(42)

WINDOW_SIZE = 4
HIDDEN_DIM = 32
BATCH_SIZE = 128
EPOCHS = 100
LR = 0.01

# %% [markdown]
# ---
# ## Step 1: Load Data and Build Vocabulary

# %%
df = pd.read_csv("./billboard_numerals_simple.csv")
df["chords"] = df["chords"].str.split("|")

all_chords = []
for row in df["chords"]:
    # Do not add empty lists
    if row:
        all_chords.extend(row)

CHORDS = sorted(set(all_chords))
VOCAB_SIZE = len(CHORDS)
stoi = {chord: i for i, chord in enumerate(CHORDS)}

print(f"Loaded {len(df)} songs | Vocabulary ({VOCAB_SIZE}): {CHORDS}")

# %% [markdown]
# ---
# ## Step 2: Encoding

# %%
def one_hot(chord):
    v = torch.zeros(VOCAB_SIZE)
    v[stoi[chord]] = 1.0
    return v

def encode_sequence(chords):
    return torch.stack([one_hot(c) for c in chords]).flatten()

def decode(logits_or_onehot):
    """Decode prediction(s): 1D → single chord name; 2D [batch, vocab] → list of chord names."""
    if logits_or_onehot.dim() == 1:
        return CHORDS[torch.argmax(logits_or_onehot).item()]
    idx = torch.argmax(logits_or_onehot, dim=-1)
    return [CHORDS[i.item()] for i in idx]

# %% [markdown]
# ---
# ## Step 3: Build Training Pairs (Sliding Window)
#
# Input: `WINDOW_SIZE` consecutive chords → Target: the next chord
#
# One song with 100 chords yields ~96 training examples.

# %%
all_pairs = [
    (chords[i : i + WINDOW_SIZE], chords[i + WINDOW_SIZE])
    for chords in df["chords"] if chords
    for i in range(len(chords) - WINDOW_SIZE)
]

print(f"Total training pairs: {len(all_pairs)}")
print(f"Example: {all_pairs[0][0]} → '{all_pairs[0][1]}'")

# %% [markdown]
# ---
# ## Step 4: Encode and Split

# %%
X = torch.stack([encode_sequence(inp) for inp, _ in all_pairs])
y = torch.tensor([stoi[tgt] for _, tgt in all_pairs])

n_train = int(0.8 * len(X))
perm = torch.randperm(len(X))

X_train = X[perm[:n_train]]
y_train = y[perm[:n_train]]

X_test = X[perm[n_train:]]
y_test = y[perm[n_train:]]

train_loader = DataLoader(TensorDataset(X_train, y_train), batch_size=BATCH_SIZE, shuffle=True)

print(f"X shape: {X.shape}  |  Train: {len(X_train)}  |  Test: {len(X_test)}")

# %% [markdown]
# ---
# ## Step 5: Define the Model
#
# A two-layer MLP:
# ```
# Input (WINDOW_SIZE × VOCAB_SIZE) → Hidden (16, ReLU) → Output (VOCAB_SIZE)
# ```

# %%
class NextChordPredictor(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(WINDOW_SIZE * VOCAB_SIZE, HIDDEN_DIM),
            nn.ReLU(),
            nn.Linear(HIDDEN_DIM, HIDDEN_DIM),
            nn.ReLU(),
            nn.Linear(HIDDEN_DIM, VOCAB_SIZE),
        )

    def forward(self, x):
        return self.net(x)  # raw logits

model = NextChordPredictor()
print(model)
print(f"Parameters: {sum(p.numel() for p in model.parameters())}")

# %% [markdown]
# ---
# ## Step 6: Train
#
# First, let's see what the untrained model predicts — these should look essentially random.

# %%
print("Predictions BEFORE training:\n")

def predict_next(chords, top_k=4):
    """Return top-k (chord, probability) predictions for a chord sequence."""
    model.eval()
    with torch.no_grad():
        logits = model(encode_sequence(chords).unsqueeze(0))
        probs  = torch.softmax(logits, dim=1)[0]
    top_probs, top_idx = torch.topk(probs, k=top_k)
    return [(CHORDS[i], p.item()) for i, p in zip(top_idx, top_probs)]

test_progressions = [
    ["I",  "IV",  "V",   "I"],
    ["I",  "V",   "vi",  "IV"],
    ["i",  "VI",  "VII", "i"],
    ["V",  "bVII","i",   "ii"],
]

for prog in test_progressions:
    results = predict_next(prog, top_k = 10)
    result_str = "  ".join(f"{c} ({p:.0%})" for c, p in results)
    print(f"  {prog} →  {result_str}")

# %%
loss_fn  = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=LR)

def accuracy(X, y):
    model.eval()
    with torch.no_grad():
        return (torch.argmax(model(X), dim=1) == y).float().mean().item()

for epoch in range(1, EPOCHS + 1):
    model.train()
    total_loss = 0.0
    for X_batch, y_batch in train_loader:
        optimizer.zero_grad()
        loss = loss_fn(model(X_batch), y_batch)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()


    print(f"Epoch {epoch:3d} | Loss: {total_loss / len(train_loader):.4f} "
            f"| Train: {accuracy(X_train, y_train):.1%} "
            f"| Test:  {accuracy(X_test, y_test):.1%}")

# %% [markdown]
# ---
# ## Step 7: Evaluate

# %%
model.eval()
with torch.no_grad():
    preds = torch.argmax(model(X_test), dim=1)

print(f"\nOverall test accuracy: {(preds == y_test).float().mean().item():.1%}\n")
print("Per-chord accuracy:")
for i, chord in enumerate(CHORDS):
    mask = y_test == i
    if mask.sum() > 0:
        acc = (preds[mask] == y_test[mask]).float().mean().item()
        print(f"  {chord:5s}: {acc:5.1%}  ({mask.sum().item()} samples)")

# %% [markdown]
# ---
# ## Step 8: Predict

# %%

test_progressions = [
    ["I",  "IV",  "V",   "I"],
    ["I",  "V",   "vi",  "IV"],
    ["i",  "VI",  "VII", "i"],
    ["V",  "bVII","i",   "ii"],
]

print("Predictions after training:\n")
for prog in test_progressions:
    results = predict_next(prog)
    result_str = "  ".join(f"{c} ({p:.0%})" for c, p in results)
    print(f"  {prog} →  {result_str}")


# %% Generate a song
test_progression = ["iv", "IV", "V", "I"]
final_progression = test_progression
for i in range(12):
    results = predict_next(test_progression)
    chosen_chord = results[0]
    chord, probability = chosen_chord
    test_progression  = test_progression[1:] + [chord]
    final_progression = final_progression + [chord]

print(f"Final progression")
for i in range(0, len(final_progression), 4):
    print(f"  {final_progression[i:i+4]}")

# %%
