from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pretty_midi


@dataclass(slots=True)
class PreparedPiece:
    piece_id: str
    split: str
    pitches: np.ndarray
    features: np.ndarray
    targets: np.ndarray
    quantized_start_beats: np.ndarray
    quantized_duration_beats: np.ndarray
    input_velocities: np.ndarray
    note_count: int


def load_pretty_midi(midi_path: Path) -> pretty_midi.PrettyMIDI:
    return pretty_midi.PrettyMIDI(str(midi_path))


def select_primary_instrument(midi_obj: pretty_midi.PrettyMIDI) -> pretty_midi.Instrument:
    instruments = [instrument for instrument in midi_obj.instruments if not instrument.is_drum]
    if not instruments:
        raise ValueError("No non-drum instrument found in MIDI file.")
    return max(instruments, key=lambda instrument: len(instrument.notes))


def sorted_notes(instrument: pretty_midi.Instrument) -> list[pretty_midi.Note]:
    return sorted(instrument.notes, key=lambda note: (note.start, note.pitch, note.end))


def quantize_velocities(velocities: np.ndarray, velocity_bin: int) -> np.ndarray:
    quantized = np.round(velocities / velocity_bin) * velocity_bin
    return np.clip(quantized, 1, 127).astype(np.float32)


def _segment_indices(values: np.ndarray, anchors: np.ndarray) -> np.ndarray:
    if anchors.size < 2:
        raise ValueError("At least two beat anchors are required.")
    indices = np.searchsorted(anchors, values, side="right") - 1
    return np.clip(indices, 0, anchors.size - 2)


def seconds_to_beats(times: np.ndarray, beat_times: np.ndarray) -> np.ndarray:
    indices = _segment_indices(times, beat_times)
    left = beat_times[indices]
    right = beat_times[indices + 1]
    segment = np.maximum(right - left, 1e-6)
    fraction = (times - left) / segment
    return indices.astype(np.float32) + fraction.astype(np.float32)


def beats_to_seconds(beat_positions: np.ndarray, beat_times: np.ndarray) -> np.ndarray:
    if beat_times.size < 2:
        raise ValueError("At least two beat anchors are required.")
    beat_positions = np.maximum(beat_positions, 0.0)
    indices = np.floor(beat_positions).astype(np.int64)
    indices = np.clip(indices, 0, beat_times.size - 2)
    left = beat_times[indices]
    right = beat_times[indices + 1]
    fraction = beat_positions - indices
    return left + (right - left) * fraction


def _same_onset_counts(quantized_start_beats: np.ndarray) -> np.ndarray:
    rounded = np.round(quantized_start_beats, 4)
    counts = np.zeros_like(rounded, dtype=np.float32)
    unique, inverse = np.unique(rounded, return_inverse=True)
    unique_counts = np.bincount(inverse)
    for onset_index, onset_count in enumerate(unique_counts):
        counts[inverse == onset_index] = onset_count
    return counts


def build_note_features(
    pitches: np.ndarray,
    quantized_start_beats: np.ndarray,
    quantized_duration_beats: np.ndarray,
    input_velocities: np.ndarray,
) -> np.ndarray:
    beat_phase = np.mod(quantized_start_beats, 1.0)
    bar_phase = np.mod(quantized_start_beats, 4.0) / 4.0

    previous = np.roll(quantized_start_beats, 1)
    previous[0] = quantized_start_beats[0]
    ioi_beats = quantized_start_beats - previous
    same_onset_count = _same_onset_counts(quantized_start_beats)

    features = np.stack(
        [
            input_velocities / 127.0,
            np.clip(quantized_duration_beats, 0.0, 8.0) / 8.0,
            np.clip(ioi_beats, 0.0, 4.0) / 4.0,
            np.sin(2.0 * np.pi * beat_phase),
            np.cos(2.0 * np.pi * beat_phase),
            np.sin(2.0 * np.pi * bar_phase),
            np.cos(2.0 * np.pi * bar_phase),
            np.clip(same_onset_count, 1.0, 8.0) / 8.0,
            (pitches >= 60).astype(np.float32),
        ],
        axis=1,
    )
    return features.astype(np.float32)


def prepare_piece(
    midi_path: Path,
    split: str,
    piece_id: str,
    subdivisions: int = 4,
    velocity_bin: int = 8,
) -> PreparedPiece:
    midi_obj = load_pretty_midi(midi_path)
    beat_times = np.asarray(midi_obj.get_beats(), dtype=np.float32)
    if beat_times.size < 2:
        raise ValueError(f"{midi_path} does not contain enough beat anchors.")

    instrument = select_primary_instrument(midi_obj)
    notes = sorted_notes(instrument)
    if not notes:
        raise ValueError(f"{midi_path} does not contain note events.")

    pitches = np.asarray([note.pitch for note in notes], dtype=np.int64)
    velocities = np.asarray([note.velocity for note in notes], dtype=np.float32)
    start_seconds = np.asarray([note.start for note in notes], dtype=np.float32)
    end_seconds = np.asarray([note.end for note in notes], dtype=np.float32)

    start_beats = seconds_to_beats(start_seconds, beat_times)
    end_beats = seconds_to_beats(end_seconds, beat_times)

    step = 1.0 / subdivisions
    quantized_start_beats = np.round(start_beats / step) * step
    quantized_end_beats = np.round(end_beats / step) * step
    quantized_end_beats = np.maximum(quantized_end_beats, quantized_start_beats + step)
    quantized_duration_beats = quantized_end_beats - quantized_start_beats

    input_velocities = quantize_velocities(velocities, velocity_bin)
    features = build_note_features(
        pitches=pitches,
        quantized_start_beats=quantized_start_beats,
        quantized_duration_beats=quantized_duration_beats,
        input_velocities=input_velocities,
    )

    targets = np.stack(
        [
            start_beats - quantized_start_beats,
            (end_beats - start_beats) - quantized_duration_beats,
            (velocities - input_velocities) / 127.0,
        ],
        axis=1,
    ).astype(np.float32)

    return PreparedPiece(
        piece_id=piece_id,
        split=split,
        pitches=pitches,
        features=features,
        targets=targets,
        quantized_start_beats=quantized_start_beats.astype(np.float32),
        quantized_duration_beats=quantized_duration_beats.astype(np.float32),
        input_velocities=input_velocities.astype(np.float32),
        note_count=len(notes),
    )


def export_quantized_midi(
    midi_path: Path,
    output_path: Path,
    subdivisions: int,
    velocity_bin: int,
) -> None:
    midi_obj = load_pretty_midi(midi_path)
    beat_times = np.asarray(midi_obj.get_beats(), dtype=np.float32)
    if beat_times.size < 2:
        raise ValueError(f"{midi_path} does not contain enough beat anchors.")

    instrument = select_primary_instrument(midi_obj)
    notes = sorted_notes(instrument)
    if not notes:
        raise ValueError(f"{midi_path} does not contain note events.")

    start_seconds = np.asarray([note.start for note in notes], dtype=np.float32)
    end_seconds = np.asarray([note.end for note in notes], dtype=np.float32)
    velocities = np.asarray([note.velocity for note in notes], dtype=np.float32)

    start_beats = seconds_to_beats(start_seconds, beat_times)
    end_beats = seconds_to_beats(end_seconds, beat_times)

    step = 1.0 / subdivisions
    quantized_start_beats = np.round(start_beats / step) * step
    quantized_end_beats = np.round(end_beats / step) * step
    quantized_end_beats = np.maximum(quantized_end_beats, quantized_start_beats + step)
    quantized_velocities = quantize_velocities(velocities, velocity_bin)

    new_start_seconds = beats_to_seconds(quantized_start_beats, beat_times)
    new_end_seconds = beats_to_seconds(quantized_end_beats, beat_times)

    for note, start_time, end_time, velocity in zip(
        notes,
        new_start_seconds,
        new_end_seconds,
        quantized_velocities,
        strict=True,
    ):
        note.start = float(start_time)
        note.end = float(max(end_time, start_time + 1e-4))
        note.velocity = int(velocity)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    midi_obj.write(str(output_path))


def humanize_midi_notes(
    midi_path: Path,
    predicted_deltas: np.ndarray,
    subdivisions: int,
    velocity_bin: int,
    strength: float,
    output_path: Path,
) -> None:
    midi_obj = load_pretty_midi(midi_path)
    beat_times = np.asarray(midi_obj.get_beats(), dtype=np.float32)
    if beat_times.size < 2:
        raise ValueError(f"{midi_path} does not contain enough beat anchors.")

    instrument = select_primary_instrument(midi_obj)
    notes = sorted_notes(instrument)
    if len(notes) != predicted_deltas.shape[0]:
        raise ValueError("Prediction length does not match note count.")

    start_seconds = np.asarray([note.start for note in notes], dtype=np.float32)
    end_seconds = np.asarray([note.end for note in notes], dtype=np.float32)
    velocities = np.asarray([note.velocity for note in notes], dtype=np.float32)

    start_beats = seconds_to_beats(start_seconds, beat_times)
    end_beats = seconds_to_beats(end_seconds, beat_times)

    step = 1.0 / subdivisions
    quantized_start_beats = np.round(start_beats / step) * step
    quantized_end_beats = np.round(end_beats / step) * step
    quantized_end_beats = np.maximum(quantized_end_beats, quantized_start_beats + step)
    quantized_duration_beats = quantized_end_beats - quantized_start_beats
    input_velocities = quantize_velocities(velocities, velocity_bin)

    new_start_beats = np.maximum(
        quantized_start_beats + strength * predicted_deltas[:, 0],
        0.0,
    )
    new_duration_beats = np.maximum(
        quantized_duration_beats + strength * predicted_deltas[:, 1],
        step * 0.5,
    )
    new_end_beats = new_start_beats + new_duration_beats
    new_velocities = np.clip(
        np.round(input_velocities + strength * (predicted_deltas[:, 2] * 127.0)),
        1,
        127,
    )

    new_start_seconds = beats_to_seconds(new_start_beats, beat_times)
    new_end_seconds = beats_to_seconds(new_end_beats, beat_times)

    for note, start_time, end_time, velocity in zip(
        notes,
        new_start_seconds,
        new_end_seconds,
        new_velocities,
        strict=True,
    ):
        note.start = float(start_time)
        note.end = float(max(end_time, start_time + 1e-4))
        note.velocity = int(velocity)

    midi_obj.write(str(output_path))
