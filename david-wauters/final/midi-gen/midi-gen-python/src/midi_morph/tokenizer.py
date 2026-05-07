from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import TypeAlias

from miditok import MIDILike, REMI, TSD, MMM, CPWord, Octuple, Structured, TokenizerConfig
from miditok.midi_tokenizer import MusicTokenizer

TokenizerName: TypeAlias = str


class MidiTokTokenizer(str, Enum):
    remi = "remi"
    tsd = "tsd"
    midi_like = "midi-like"
    structured = "structured"
    cp_word = "cp-word"
    octuple = "octuple"
    mmm = "mmm"


TOKENIZER_CLASSES = {
    MidiTokTokenizer.remi: REMI,
    MidiTokTokenizer.tsd: TSD,
    MidiTokTokenizer.midi_like: MIDILike,
    MidiTokTokenizer.structured: Structured,
    MidiTokTokenizer.cp_word: CPWord,
    MidiTokTokenizer.octuple: Octuple,
    MidiTokTokenizer.mmm: MMM,
}


def build_tokenizer(tokenizer_name: MidiTokTokenizer = MidiTokTokenizer.remi) -> MusicTokenizer:
    config = TokenizerConfig(
        num_velocities=32,
        use_chords=True,
        use_programs=True,
        use_tempos=True,
        beat_res={(0, 4): 8},
    )
    return TOKENIZER_CLASSES[tokenizer_name](config)


def train_tokenizer(
    midi_dir: Path,
    output_path: Path,
    vocab_size: int = 2048,
    tokenizer_name: MidiTokTokenizer = MidiTokTokenizer.remi,
) -> None:
    midi_paths = list(midi_dir.rglob("*.mid")) + list(midi_dir.rglob("*.midi"))
    if not midi_paths:
        raise ValueError(f"No MIDI files found under {midi_dir}")
    tokenizer = build_tokenizer(tokenizer_name)
    tokenizer.train(vocab_size=vocab_size, files_paths=midi_paths)
    if output_path.suffix == ".json":
        output_path.parent.mkdir(parents=True, exist_ok=True)
        tokenizer.save(output_path.parent, filename=output_path.name)
    else:
        output_path.mkdir(parents=True, exist_ok=True)
        tokenizer.save(output_path)


def encode_midi(
    input_midi: Path,
    output_json: Path,
    tokenizer_name: MidiTokTokenizer = MidiTokTokenizer.remi,
) -> None:
    tokenizer = build_tokenizer(tokenizer_name)
    tokens = tokenizer.encode(input_midi)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    tokenizer.save_tokens(tokens, output_json)


def decode_tokens(
    input_json: Path,
    output_midi: Path,
    tokenizer_name: MidiTokTokenizer = MidiTokTokenizer.remi,
) -> None:
    tokenizer = build_tokenizer(tokenizer_name)
    tokens = tokenizer.load_tokens(input_json)
    score = tokenizer.decode(tokens)
    score.dump_midi(output_midi)
