# midi-morph

`midi-morph` is a small command-line MIDI transformation tool:

- chords -> melody: extracts harmonic pitch classes and creates a monophonic melodic line.
- melody -> chords: harmonizes a monophonic line with block chords.

It uses `miditoolkit` for MIDI IO, `torch` for candidate scoring tensors and future model checkpoints, and `miditok` for tokenizer scaffolding when you move from rules to training.

## Install

```bash
uv sync
```

## Use

```bash
uv run midi-morph chords-to-melody input_chords.mid output_melody.mid
uv run midi-morph melody-to-chords input_melody.mid output_chords.mid
```

Useful options:

```bash
uv run midi-morph chords-to-melody chords.mid melody.mid --density 2 --octave 5
uv run midi-morph melody-to-chords melody.mid chords.mid --bars-per-chord 0.5 --octave 3
uv run midi-morph inspect song.mid
```

## Tokenizers

The learned version should use `miditok` token IDs rather than a custom MIDI vocabulary. `REMI` is the default because it preserves bar and position tokens, which are useful for chord timing and melody phrasing.

Supported tokenizer choices:

- `remi`
- `tsd`
- `midi-like`
- `structured`
- `cp-word`
- `octuple`
- `mmm`

Examples:

```bash
uv run midi-morph encode song.mid tokens.json --tokenizer remi
uv run midi-morph decode tokens.json reconstructed.mid --tokenizer remi
uv run midi-morph train-tokenizer ./midi_data tokenizer.json --tokenizer remi --vocab-size 2048
```

For this project, start with `remi`. Try `tsd` if you want a simpler stream with explicit time shifts, and `midi-like` if you want a representation closer to raw MIDI events.

## Training

Train a causal Transformer on a directory of MIDI files:

```bash
uv run midi-morph train-model ./midi_data checkpoints/remi.pt --tokenizer remi --epochs 20 --seq-len 512 --batch-size 8
```

Generate from the checkpoint:

```bash
uv run midi-morph generate checkpoints/remi.pt generated.mid --max-new-tokens 512
```

Continue from a prompt MIDI:

```bash
uv run midi-morph generate checkpoints/remi.pt continued.mid --prompt-midi seed.mid --max-new-tokens 512
```

For quick CPU testing, use a smaller model:

```bash
uv run midi-morph train-model ./midi_data checkpoints/debug.pt --seq-len 128 --batch-size 2 --d-model 128 --nhead 4 --num-layers 2 --max-steps 10 --device cpu
```

## Dataset notes

The `shiehn/chord-melody-dataset` repo is directly relevant to chord-melody pairing, but it is small and tied to a specific representation. For a learned version, a stronger path is to combine:

- paired symbolic melody/chord datasets such as AutoHarmonizer resources;
- broader MIDI corpora with chord metadata, such as ComMU;
- your own MIDI pairs exported from DAW projects, normalized into a common token format with `miditok`.

The current tool is intentionally deterministic so it works before training data is collected.

## Development

```bash
uv run pytest
```
