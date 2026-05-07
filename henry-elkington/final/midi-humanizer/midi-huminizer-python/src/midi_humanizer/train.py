from __future__ import annotations

import json
import random
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader
from tqdm import tqdm

from midi_humanizer.data.dataset import MaestroChunkDataset, collate_batches
from midi_humanizer.data.maestro import preprocess_maestro_dataset
from midi_humanizer.models.factory import build_model


@dataclass(slots=True)
class TrainConfig:
    dataset_root: Path
    cache_dir: Path
    output_dir: Path
    model_type: str = "rnn"
    epochs: int = 20
    batch_size: int = 12
    learning_rate: float = 3e-4
    weight_decay: float = 1e-4
    seq_len: int = 256
    stride: int = 128
    subdivisions: int = 4
    velocity_bin: int = 8
    num_workers: int = 0
    seed: int = 7


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def masked_huber_loss(
    prediction: torch.Tensor,
    target: torch.Tensor,
    mask: torch.Tensor,
    delta: float = 0.1,
) -> torch.Tensor:
    loss = nn.functional.huber_loss(prediction, target, reduction="none", delta=delta)
    expanded_mask = mask.unsqueeze(-1).float()
    loss = loss * expanded_mask
    denom = expanded_mask.sum().clamp_min(1.0)
    return loss.sum() / denom


def ensure_preprocessed_data(config: TrainConfig) -> None:
    expected_files = [
        config.cache_dir / "train.pt",
        config.cache_dir / "validation.pt",
        config.cache_dir / "test.pt",
    ]
    if all(path.exists() for path in expected_files):
        return
    preprocess_maestro_dataset(
        dataset_root=config.dataset_root,
        output_dir=config.cache_dir,
        subdivisions=config.subdivisions,
        velocity_bin=config.velocity_bin,
    )


def make_dataloaders(config: TrainConfig) -> tuple[DataLoader, DataLoader]:
    train_dataset = MaestroChunkDataset(
        cache_path=config.cache_dir / "train.pt",
        seq_len=config.seq_len,
        stride=config.stride,
    )
    val_dataset = MaestroChunkDataset(
        cache_path=config.cache_dir / "validation.pt",
        seq_len=config.seq_len,
        stride=config.seq_len,
    )

    train_loader = DataLoader(
        train_dataset,
        batch_size=config.batch_size,
        shuffle=True,
        num_workers=config.num_workers,
        collate_fn=collate_batches,
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=config.batch_size,
        shuffle=False,
        num_workers=config.num_workers,
        collate_fn=collate_batches,
    )
    return train_loader, val_loader


def run_epoch(
    model: nn.Module,
    loader: DataLoader,
    optimizer: torch.optim.Optimizer | None,
    device: torch.device,
    model_type: str,
) -> float:
    train_mode = optimizer is not None
    model.train(train_mode)
    total_loss = 0.0
    total_batches = 0

    for batch in tqdm(loader, leave=False):
        pitches = batch["pitches"].to(device)
        features = batch["features"].to(device)
        targets = batch["targets"].to(device)
        mask = batch["mask"].to(device)
        lengths = batch["lengths"].to(device)

        if model_type == "transformer":
            predictions = model(pitches=pitches, features=features, mask=mask)
        else:
            predictions = model(pitches=pitches, features=features, lengths=lengths)

        loss = masked_huber_loss(predictions, targets, mask)

        if optimizer is not None:
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()

        total_loss += loss.item()
        total_batches += 1

    return total_loss / max(total_batches, 1)


def save_checkpoint(
    path: Path,
    model: nn.Module,
    config: TrainConfig,
    feature_dim: int,
    best_val_loss: float,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "model_state_dict": model.state_dict(),
            "model_type": config.model_type,
            "feature_dim": feature_dim,
            "subdivisions": config.subdivisions,
            "velocity_bin": config.velocity_bin,
            "best_val_loss": best_val_loss,
            "train_config": {
                key: str(value) if isinstance(value, Path) else value
                for key, value in asdict(config).items()
            },
        },
        path,
    )


def train(config: TrainConfig) -> Path:
    set_seed(config.seed)
    ensure_preprocessed_data(config)
    train_loader, val_loader = make_dataloaders(config)
    sample_batch = next(iter(train_loader))
    feature_dim = int(sample_batch["features"].shape[-1])

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = build_model(config.model_type, feature_dim=feature_dim).to(device)
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=config.learning_rate,
        weight_decay=config.weight_decay,
    )

    best_val_loss = float("inf")
    best_checkpoint_path = config.output_dir / f"{config.model_type}_best.pt"

    history: list[dict[str, float]] = []
    for epoch in range(1, config.epochs + 1):
        train_loss = run_epoch(
            model=model,
            loader=train_loader,
            optimizer=optimizer,
            device=device,
            model_type=config.model_type,
        )
        with torch.no_grad():
            val_loss = run_epoch(
                model=model,
                loader=val_loader,
                optimizer=None,
                device=device,
                model_type=config.model_type,
            )

        history.append(
            {
                "epoch": epoch,
                "train_loss": train_loss,
                "val_loss": val_loss,
            }
        )
        print(
            f"epoch={epoch} train_loss={train_loss:.5f} val_loss={val_loss:.5f}"
        )

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            save_checkpoint(
                path=best_checkpoint_path,
                model=model,
                config=config,
                feature_dim=feature_dim,
                best_val_loss=best_val_loss,
            )

    history_path = config.output_dir / "train_history.json"
    history_path.parent.mkdir(parents=True, exist_ok=True)
    history_path.write_text(json.dumps(history, indent=2), encoding="utf-8")
    return best_checkpoint_path
