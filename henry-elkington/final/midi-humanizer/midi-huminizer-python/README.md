# MIDI Humanizer

Train a PyTorch model on the MAESTRO piano-performance dataset and use it to humanize rigid MIDI clips.

This project treats humanization as a supervised regression problem:

- input: a quantized, less expressive version of a performance
- target: the original expressive timing, duration, and velocity deviations

The current implementation supports two model backends:

- `rnn`: bidirectional LSTM baseline
- `transformer`: transformer encoder baseline

## What The Model Learns

For each note in a MIDI sequence, the model predicts:

- onset shift in beats
- duration shift in beats
- velocity delta

Training pairs are created automatically from MAESTRO by:

1. loading the expressive performance MIDI
2. quantizing note starts and ends to a fixed rhythmic grid
3. quantizing note velocities into coarse bins
4. training the model to recover the original expressive deviations

## Setup

PyTorch support on Python `3.13` is still inconsistent across environments, so this repo targets Python `3.12`.

```bash
uv python install 3.12
uv sync
```

If you want to force `uv` to use the project-pinned Python version locally:

```bash
uv venv --python 3.12
uv sync
```

## MAESTRO Layout

In this repo, the dataset root is:

```text
./maestro-v3.0.0
```

It should contain the metadata CSV and year folders, for example:

```text
./maestro-v3.0.0/
  maestro-v3.0.0.csv
  2004/
  2006/
  2008/
  ...
```

## Preprocess The Dataset

```bash
uv run midi-humanizer prepare-maestro \
  --dataset-root ./maestro-v3.0.0 \
  --cache-dir artifacts/cache \
  --subdivisions 4 \
  --velocity-bin 8
```

This creates:

- `artifacts/cache/train.pt`
- `artifacts/cache/validation.pt`
- `artifacts/cache/test.pt`

## Train

RNN baseline:

```bash
uv run midi-humanizer train \
  --dataset-root ./maestro-v3.0.0 \
  --cache-dir artifacts/cache \
  --output-dir artifacts/checkpoints \
  --model-type rnn \
  --epochs 20 \
  --batch-size 12 \
  --seq-len 256 \
  --stride 128
```

Transformer baseline:

```bash
uv run midi-humanizer train \
  --dataset-root ./maestro-v3.0.0 \
  --cache-dir artifacts/cache \
  --output-dir artifacts/checkpoints \
  --model-type transformer
```

The best checkpoint is written to:

```text
artifacts/checkpoints/rnn_best.pt
```

or:

```text
artifacts/checkpoints/transformer_best.pt
```

## Humanize A MIDI Clip

Use a rigid or mostly quantized piano MIDI file as input.

```bash
uv run midi-humanizer humanize \
  --checkpoint artifacts/checkpoints/rnn_best.pt \
  --input-midi path/to/input.mid \
  --output-midi artifacts/humanized.mid \
  --strength 1.0
```

`strength` scales the predicted deviations:

- `0.0`: no change
- `1.0`: full model output
- `>1.0`: exaggerated humanization

## Export The Quantized MIDI

If you want to hear or inspect the exact quantized version used as the model input, write it back out as a MIDI file:

```bash
uv run midi-humanizer export-quantized \
  --input-midi ./bosa.mid \
  --output-midi artifacts/bosa_quantized.mid \
  --subdivisions 4 \
  --velocity-bin 8
```

That output file can be dragged directly into Ableton for A/B comparison against:

- the original MIDI
- the quantized MIDI
- the humanized MIDI

## Notes On Scope

This is an MVP intended for solo-piano humanization with MAESTRO.

Current constraints:

- it preserves the original note identities and note count
- it does not add or remove notes
- it assumes the input clip has a usable beat grid and tempo map
- it is best suited to piano MIDI, not arbitrary multi-instrument arrangements

## Recommended Next Steps

- add evaluation metrics on the validation split
- add pedal/control-change modeling
- add richer velocity-conditioning so user dynamics are preserved more explicitly
- add style conditioning by composer or era
