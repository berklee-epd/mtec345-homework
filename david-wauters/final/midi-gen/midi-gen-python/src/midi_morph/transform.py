from __future__ import annotations

from pathlib import Path

import miditoolkit

from midi_morph.music import NoteEvent, chord_pitches, melodic_pattern_for_chord, pitch_classes, rank_chords


def _load_notes(midi: miditoolkit.MidiFile) -> list[NoteEvent]:
    notes: list[NoteEvent] = []
    for instrument in midi.instruments:
        if instrument.is_drum:
            continue
        for note in instrument.notes:
            if note.end > note.start:
                notes.append(NoteEvent(note.pitch, note.start, note.end, note.velocity))
    return sorted(notes, key=lambda note: (note.start, note.pitch, note.end))


def _notes_in_window(notes: list[NoteEvent], start: int, end: int) -> list[NoteEvent]:
    return [note for note in notes if note.start < end and note.end > start]


def _copy_meta(source: miditoolkit.MidiFile) -> miditoolkit.MidiFile:
    output = miditoolkit.MidiFile(ticks_per_beat=source.ticks_per_beat)
    output.tempo_changes = list(source.tempo_changes)
    output.time_signature_changes = list(source.time_signature_changes)
    output.key_signature_changes = list(source.key_signature_changes)
    return output


def chords_to_melody(
    input_path: Path,
    output_path: Path,
    *,
    density: int = 2,
    octave: int = 5,
    velocity: int = 86,
) -> None:
    midi = miditoolkit.MidiFile(str(input_path))
    notes = _load_notes(midi)
    if not notes:
        raise ValueError(f"No non-drum notes found in {input_path}")

    output = _copy_meta(midi)
    melody = miditoolkit.Instrument(program=0, is_drum=False, name="Generated Melody")
    step = max(1, midi.ticks_per_beat // max(1, density))
    song_end = max(note.end for note in notes)
    previous_pitch: int | None = None

    for start in range(0, song_end, step):
        end = min(song_end, start + step)
        window = _notes_in_window(notes, start, end)
        pcs = pitch_classes(window)
        pattern = melodic_pattern_for_chord(pcs, previous_pitch, octave=octave)
        if not pattern:
            continue

        pitch = pattern[(start // step) % len(pattern)]
        previous_pitch = pitch
        melody.notes.append(miditoolkit.Note(velocity=velocity, pitch=pitch, start=start, end=end))

    output.instruments.append(melody)
    output.dump(str(output_path))


def melody_to_chords(
    input_path: Path,
    output_path: Path,
    *,
    bars_per_chord: float = 1.0,
    octave: int = 3,
    velocity: int = 72,
) -> None:
    midi = miditoolkit.MidiFile(str(input_path))
    notes = _load_notes(midi)
    if not notes:
        raise ValueError(f"No non-drum notes found in {input_path}")

    output = _copy_meta(midi)
    chord_track = miditoolkit.Instrument(program=0, is_drum=False, name="Generated Chords")
    beats_per_bar = 4
    if midi.time_signature_changes:
        beats_per_bar = midi.time_signature_changes[0].numerator
    window_ticks = max(1, int(midi.ticks_per_beat * beats_per_bar * bars_per_chord))
    song_end = max(note.end for note in notes)

    for start in range(0, song_end, window_ticks):
        end = min(song_end, start + window_ticks)
        window = _notes_in_window(notes, start, end)
        choices = rank_chords(window)
        if not choices:
            continue
        for pitch in chord_pitches(choices[0], octave=octave):
            chord_track.notes.append(miditoolkit.Note(velocity=velocity, pitch=pitch, start=start, end=end))

    output.instruments.extend(midi.instruments)
    output.instruments.append(chord_track)
    output.dump(str(output_path))


def midi_summary(input_path: Path) -> str:
    midi = miditoolkit.MidiFile(str(input_path))
    notes = _load_notes(midi)
    duration_ticks = max((note.end for note in notes), default=0)
    instruments = [instrument.name or str(instrument.program) for instrument in midi.instruments if not instrument.is_drum]
    return (
        f"ticks_per_beat={midi.ticks_per_beat}\n"
        f"tracks={len(midi.instruments)}\n"
        f"non_drum_tracks={len(instruments)}\n"
        f"notes={len(notes)}\n"
        f"duration_ticks={duration_ticks}\n"
        f"instruments={', '.join(instruments) if instruments else '(none)'}"
    )
