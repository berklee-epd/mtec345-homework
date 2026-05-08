from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import torch
from torch.utils.data import Dataset


@dataclass(slots=True)
class DatasetConfig:
    cache_dir: Path
    seq_len: int = 256
    stride: int = 128


class MaestroChunkDataset(Dataset[dict[str, torch.Tensor]]):
    def __init__(self, cache_path: Path, seq_len: int, stride: int) -> None:
        payload = torch.load(cache_path, map_location="cpu")
        self.subdivisions = int(payload["subdivisions"])
        self.velocity_bin = int(payload["velocity_bin"])
        self.pieces = payload["pieces"]
        self.index: list[tuple[int, int, int]] = []

        for piece_index, piece in enumerate(self.pieces):
            note_count = int(piece["note_count"])
            if note_count < 4:
                continue
            if note_count <= seq_len:
                self.index.append((piece_index, 0, note_count))
                continue
            for start in range(0, note_count - 3, stride):
                end = min(start + seq_len, note_count)
                if end - start >= 4:
                    self.index.append((piece_index, start, end))
                if end == note_count:
                    break

    def __len__(self) -> int:
        return len(self.index)

    def __getitem__(self, idx: int) -> dict[str, torch.Tensor]:
        piece_index, start, end = self.index[idx]
        piece = self.pieces[piece_index]
        return {
            "pitches": piece["pitches"][start:end].long(),
            "features": piece["features"][start:end].float(),
            "targets": piece["targets"][start:end].float(),
            "length": torch.tensor(end - start, dtype=torch.long),
        }


def collate_batches(batch: list[dict[str, torch.Tensor]]) -> dict[str, torch.Tensor]:
    lengths = torch.tensor([item["length"].item() for item in batch], dtype=torch.long)
    max_len = int(lengths.max().item())
    batch_size = len(batch)
    feature_dim = batch[0]["features"].shape[1]
    target_dim = batch[0]["targets"].shape[1]

    pitches = torch.zeros(batch_size, max_len, dtype=torch.long)
    features = torch.zeros(batch_size, max_len, feature_dim, dtype=torch.float32)
    targets = torch.zeros(batch_size, max_len, target_dim, dtype=torch.float32)
    mask = torch.zeros(batch_size, max_len, dtype=torch.bool)

    for batch_index, item in enumerate(batch):
        length = int(item["length"].item())
        pitches[batch_index, :length] = item["pitches"]
        features[batch_index, :length] = item["features"]
        targets[batch_index, :length] = item["targets"]
        mask[batch_index, :length] = True

    return {
        "pitches": pitches,
        "features": features,
        "targets": targets,
        "lengths": lengths,
        "mask": mask,
    }
