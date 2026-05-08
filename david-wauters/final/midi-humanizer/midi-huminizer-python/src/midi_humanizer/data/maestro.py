from __future__ import annotations

import csv
from pathlib import Path

import torch
from tqdm import tqdm

from midi_humanizer.data.midi import PreparedPiece, prepare_piece


def find_maestro_metadata(dataset_root: Path) -> Path:
    matches = sorted(dataset_root.glob("maestro-v*.csv"))
    if not matches:
        raise FileNotFoundError(
            f"Could not find MAESTRO metadata CSV under {dataset_root}."
        )
    return matches[0]


def load_maestro_rows(dataset_root: Path) -> list[dict[str, str]]:
    metadata_path = find_maestro_metadata(dataset_root)
    with metadata_path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader)


def preprocess_maestro_dataset(
    dataset_root: Path,
    output_dir: Path,
    subdivisions: int,
    velocity_bin: int,
) -> dict[str, int]:
    rows = load_maestro_rows(dataset_root)
    output_dir.mkdir(parents=True, exist_ok=True)

    split_payloads: dict[str, list[PreparedPiece]] = {
        "train": [],
        "validation": [],
        "test": [],
    }

    for row in tqdm(rows, desc="Preparing MAESTRO"):
        midi_rel_path = row["midi_filename"]
        midi_path = dataset_root / midi_rel_path
        split = row["split"]
        if split not in split_payloads:
            continue

        try:
            prepared = prepare_piece(
                midi_path=midi_path,
                split=split,
                piece_id=row["canonical_composer"] + "::" + row["canonical_title"],
                subdivisions=subdivisions,
                velocity_bin=velocity_bin,
            )
        except Exception as exc:
            print(f"Skipping {midi_rel_path}: {exc}")
            continue

        split_payloads[split].append(prepared)

    counts: dict[str, int] = {}
    for split, pieces in split_payloads.items():
        payload = {
            "split": split,
            "subdivisions": subdivisions,
            "velocity_bin": velocity_bin,
            "pieces": [
                {
                    "piece_id": piece.piece_id,
                    "split": piece.split,
                    "pitches": torch.from_numpy(piece.pitches),
                    "features": torch.from_numpy(piece.features),
                    "targets": torch.from_numpy(piece.targets),
                    "quantized_start_beats": torch.from_numpy(piece.quantized_start_beats),
                    "quantized_duration_beats": torch.from_numpy(
                        piece.quantized_duration_beats
                    ),
                    "input_velocities": torch.from_numpy(piece.input_velocities),
                    "note_count": piece.note_count,
                }
                for piece in pieces
            ],
        }
        torch.save(payload, output_dir / f"{split}.pt")
        counts[split] = len(pieces)

    return counts
