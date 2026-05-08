from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import torch

from midi_humanizer.data.midi import humanize_midi_notes, prepare_piece
from midi_humanizer.models.factory import build_model


@dataclass(slots=True)
class InferenceConfig:
    checkpoint_path: Path
    midi_path: Path
    output_path: Path
    strength: float = 1.0


def predict_deltas(
    checkpoint_path: Path,
    midi_path: Path,
) -> tuple[np.ndarray, int, int]:
    checkpoint = torch.load(checkpoint_path, map_location="cpu")
    model_type = checkpoint["model_type"]
    feature_dim = int(checkpoint["feature_dim"])
    subdivisions = int(checkpoint["subdivisions"])
    velocity_bin = int(checkpoint["velocity_bin"])

    model = build_model(model_type, feature_dim=feature_dim)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()

    piece = prepare_piece(
        midi_path=midi_path,
        split="inference",
        piece_id=midi_path.stem,
        subdivisions=subdivisions,
        velocity_bin=velocity_bin,
    )

    pitches = torch.from_numpy(piece.pitches).long().unsqueeze(0)
    features = torch.from_numpy(piece.features).float().unsqueeze(0)
    lengths = torch.tensor([piece.note_count], dtype=torch.long)
    mask = torch.ones(1, piece.note_count, dtype=torch.bool)

    with torch.no_grad():
        if model_type == "transformer":
            outputs = model(pitches=pitches, features=features, mask=mask)
        else:
            outputs = model(pitches=pitches, features=features, lengths=lengths)

    predicted = outputs.squeeze(0).cpu().numpy().astype(np.float32)
    return predicted, subdivisions, velocity_bin


def humanize_file(config: InferenceConfig) -> None:
    predicted_deltas, subdivisions, velocity_bin = predict_deltas(
        checkpoint_path=config.checkpoint_path,
        midi_path=config.midi_path,
    )
    config.output_path.parent.mkdir(parents=True, exist_ok=True)
    humanize_midi_notes(
        midi_path=config.midi_path,
        predicted_deltas=predicted_deltas,
        subdivisions=subdivisions,
        velocity_bin=velocity_bin,
        strength=config.strength,
        output_path=config.output_path,
    )
