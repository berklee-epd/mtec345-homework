from __future__ import annotations

from pathlib import Path

import typer

from midi_morph.tokenizer import MidiTokTokenizer, decode_tokens, encode_midi, train_tokenizer
from midi_morph.training import generate_midi, train_model
from midi_morph.transform import chords_to_melody, melody_to_chords, midi_summary

app = typer.Typer(help="Transform MIDI chords into melodies, or melodies into chord accompaniments.")


@app.command("chords-to-melody")
def chords_to_melody_cmd(
    input_midi: Path = typer.Argument(..., exists=True, readable=True),
    output_midi: Path = typer.Argument(...),
    density: int = typer.Option(2, min=1, max=8, help="Generated melody notes per beat."),
    octave: int = typer.Option(5, min=1, max=8, help="Target melody octave."),
    velocity: int = typer.Option(86, min=1, max=127),
) -> None:
    chords_to_melody(input_midi, output_midi, density=density, octave=octave, velocity=velocity)
    typer.echo(f"Wrote {output_midi}")


@app.command("melody-to-chords")
def melody_to_chords_cmd(
    input_midi: Path = typer.Argument(..., exists=True, readable=True),
    output_midi: Path = typer.Argument(...),
    bars_per_chord: float = typer.Option(1.0, min=0.25, max=4.0, help="Harmonic rhythm."),
    octave: int = typer.Option(3, min=1, max=6, help="Target chord octave."),
    velocity: int = typer.Option(72, min=1, max=127),
) -> None:
    melody_to_chords(input_midi, output_midi, bars_per_chord=bars_per_chord, octave=octave, velocity=velocity)
    typer.echo(f"Wrote {output_midi}")


@app.command("train-tokenizer")
def train_tokenizer_cmd(
    midi_dir: Path = typer.Argument(..., exists=True, file_okay=False, readable=True),
    output_json: Path = typer.Argument(...),
    vocab_size: int = typer.Option(2048, min=256),
    tokenizer: MidiTokTokenizer = typer.Option(MidiTokTokenizer.remi, help="miditok tokenizer family."),
) -> None:
    train_tokenizer(midi_dir, output_json, vocab_size=vocab_size, tokenizer_name=tokenizer)
    typer.echo(f"Wrote {output_json}")


@app.command("encode")
def encode_cmd(
    input_midi: Path = typer.Argument(..., exists=True, readable=True),
    output_json: Path = typer.Argument(...),
    tokenizer: MidiTokTokenizer = typer.Option(MidiTokTokenizer.remi, help="miditok tokenizer family."),
) -> None:
    encode_midi(input_midi, output_json, tokenizer_name=tokenizer)
    typer.echo(f"Wrote {output_json}")


@app.command("decode")
def decode_cmd(
    input_json: Path = typer.Argument(..., exists=True, readable=True),
    output_midi: Path = typer.Argument(...),
    tokenizer: MidiTokTokenizer = typer.Option(MidiTokTokenizer.remi, help="miditok tokenizer family."),
) -> None:
    decode_tokens(input_json, output_midi, tokenizer_name=tokenizer)
    typer.echo(f"Wrote {output_midi}")


@app.command("train-model")
def train_model_cmd(
    midi_dir: Path = typer.Argument(..., exists=True, file_okay=False, readable=True),
    checkpoint: Path = typer.Argument(...),
    tokenizer: MidiTokTokenizer = typer.Option(MidiTokTokenizer.remi, help="miditok tokenizer family."),
    seq_len: int = typer.Option(512, min=32, max=4096),
    batch_size: int = typer.Option(8, min=1),
    epochs: int = typer.Option(5, min=1),
    learning_rate: float = typer.Option(3e-4, min=1e-6, max=1e-2),
    d_model: int = typer.Option(384, min=64),
    nhead: int = typer.Option(6, min=1),
    num_layers: int = typer.Option(6, min=1),
    dropout: float = typer.Option(0.1, min=0.0, max=0.5),
    device: str = typer.Option("auto", help="auto, cpu, cuda, or mps."),
    max_steps: int | None = typer.Option(None, min=1, help="Optional debug limit."),
    strict_midi: bool = typer.Option(False, help="Fail immediately instead of skipping invalid MIDI files."),
) -> None:
    stats = train_model(
        midi_dir,
        checkpoint,
        tokenizer_name=tokenizer,
        seq_len=seq_len,
        batch_size=batch_size,
        epochs=epochs,
        learning_rate=learning_rate,
        d_model=d_model,
        nhead=nhead,
        num_layers=num_layers,
        dropout=dropout,
        device=device,
        max_steps=max_steps,
        skip_bad_midi=not strict_midi,
    )
    typer.echo(
        f"Wrote {checkpoint} | loss={stats['loss']:.4f} "
        f"steps={stats['steps']} examples={stats['examples']} "
        f"skipped_files={stats['skipped_files']} device={stats['device']}"
    )
    if stats["first_skipped"]:
        typer.echo(f"First skipped file: {stats['first_skipped']}")


@app.command("generate")
def generate_cmd(
    checkpoint: Path = typer.Argument(..., exists=True, readable=True),
    output_midi: Path = typer.Argument(...),
    prompt_midi: Path | None = typer.Option(None, exists=True, readable=True),
    max_new_tokens: int = typer.Option(256, min=1, max=4096),
    temperature: float = typer.Option(1.0, min=0.05, max=2.0),
    top_k: int = typer.Option(40, min=0),
    device: str = typer.Option("auto", help="auto, cpu, cuda, or mps."),
) -> None:
    generate_midi(
        checkpoint,
        output_midi,
        prompt_midi=prompt_midi,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        top_k=top_k,
        device=device,
    )
    typer.echo(f"Wrote {output_midi}")


@app.command("inspect")
def inspect_cmd(input_midi: Path = typer.Argument(..., exists=True, readable=True)) -> None:
    typer.echo(midi_summary(input_midi))


if __name__ == "__main__":
    app()
