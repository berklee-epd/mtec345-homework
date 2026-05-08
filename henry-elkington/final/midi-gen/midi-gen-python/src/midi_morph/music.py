from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
import torch


NOTE_NAMES = ("C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B")


@dataclass(frozen=True)
class NoteEvent:
    pitch: int
    start: int
    end: int
    velocity: int = 80

    @property
    def duration(self) -> int:
        return max(0, self.end - self.start)


@dataclass(frozen=True)
class ChordChoice:
    root: int
    quality: str
    score: float

    @property
    def name(self) -> str:
        return f"{NOTE_NAMES[self.root]}{'' if self.quality == 'maj' else self.quality}"


CHORD_TEMPLATES: dict[str, tuple[int, ...]] = {
    "maj": (0, 4, 7),
    "min": (0, 3, 7),
    "dim": (0, 3, 6),
    "sus4": (0, 5, 7),
}


def pitch_classes(notes: Iterable[NoteEvent]) -> set[int]:
    return {note.pitch % 12 for note in notes}


def fit_pitch_to_octave(pitch_class: int, octave: int, low: int | None = None, high: int | None = None) -> int:
    pitch = (octave + 1) * 12 + pitch_class
    if low is not None:
        while pitch < low:
            pitch += 12
    if high is not None:
        while pitch > high:
            pitch -= 12
    return int(np.clip(pitch, low if low is not None else 0, high if high is not None else 127))


def rank_chords(notes: Iterable[NoteEvent]) -> list[ChordChoice]:
    pcs = pitch_classes(notes)
    if not pcs:
        return []

    hist = torch.zeros(12, dtype=torch.float32)
    for pc in pcs:
        hist[pc] += 1.0

    choices: list[ChordChoice] = []
    for root in range(12):
        for quality, intervals in CHORD_TEMPLATES.items():
            chord_pcs = {(root + interval) % 12 for interval in intervals}
            mask = torch.tensor([1.0 if i in chord_pcs else 0.0 for i in range(12)])
            coverage = torch.dot(hist, mask).item()
            misses = len(pcs - chord_pcs)
            root_bonus = 0.25 if root in pcs else 0.0
            quality_penalty = 0.05 if quality in {"dim", "sus4"} else 0.0
            choices.append(ChordChoice(root, quality, coverage - 0.35 * misses + root_bonus - quality_penalty))

    return sorted(choices, key=lambda item: item.score, reverse=True)


def chord_pitches(choice: ChordChoice, octave: int = 3) -> list[int]:
    intervals = CHORD_TEMPLATES[choice.quality]
    root_pitch = fit_pitch_to_octave(choice.root, octave, 24, 84)
    return [int(np.clip(root_pitch + interval, 0, 127)) for interval in intervals]


def melodic_pattern_for_chord(pcs: set[int], previous_pitch: int | None, octave: int = 5) -> list[int]:
    if not pcs:
        return []

    candidates = [fit_pitch_to_octave(pc, octave, 48, 84) for pc in sorted(pcs)]
    if previous_pitch is None:
        start = min(candidates, key=lambda pitch: abs(pitch - ((octave + 1) * 12)))
    else:
        start = min(candidates, key=lambda pitch: abs(pitch - previous_pitch))

    ordered = [start]
    remaining = [pitch for pitch in candidates if pitch != start]
    remaining.sort(key=lambda pitch: (abs(pitch - start), pitch))
    ordered.extend(remaining)

    if len(ordered) == 1:
        ordered.append(ordered[0] + 2 if ordered[0] <= 82 else ordered[0] - 2)
    return [int(np.clip(pitch, 0, 127)) for pitch in ordered]
