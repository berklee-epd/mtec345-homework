from pathlib import Path
import math

import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader

import synth


# %% Config
DATASET_DIR = Path("Dataset/processed")
BATCH_SIZE = 64
EPOCHS = 100
INITIAL_LR = 0.005
LR_GAMMA = 0.99
GRU_HIDDEN_SIZE = 256
NUM_PARAMS = len(synth.PARAMS)
TARGET_MELS = synth.MELS
TARGET_FRAMES = 750


# %% Device
def get_device() -> torch.device:
    #if torch.backends.mps.is_available():
    #    return torch.device("mps")
    return torch.device("cpu")


DEVICE = get_device()


# %% Dataset
class SynthDataset(Dataset):
    def __init__(self, dataset_dir: Path, split: str):
        self.dataset_dir = Path(dataset_dir)
        self.metadata = pd.read_csv(self.dataset_dir / "metadata.csv")
        self.metadata = self.metadata[self.metadata["split"] == split].reset_index(drop=True)

        self.params_by_id: dict[int, torch.Tensor] = torch.load(
            self.dataset_dir / "params.pt",
            map_location="cpu",
        )
        self.stats = torch.load(self.dataset_dir / "stats.pt", map_location="cpu")
        self.mean = self.stats["mean"].to(torch.float32)
        self.std = self.stats["std"].to(torch.float32)

    def __len__(self) -> int:
        return len(self.metadata)

    def __getitem__(self, index: int) -> dict[str, torch.Tensor | float | int]:
        row = self.metadata.iloc[index]
        item = torch.load(self.dataset_dir / row["example_path"], map_location="cpu")

        mel = item["x"].to(torch.float32)
        mel = (mel - self.mean[:, None]) / self.std[:, None]

        param_id = int(item["y"])
        params = self.params_by_id[param_id].to(torch.float32)
        f0 = float(item["f0"])

        return {
            "mel": mel,
            "params": params,
            "f0": f0,
            "param_id": param_id,
        }


def pad_or_crop_mel(mel: torch.Tensor, target_frames: int) -> torch.Tensor:
    frames = mel.shape[1]

    if frames == target_frames:
        return mel

    if frames > target_frames:
        return mel[:, :target_frames]

    pad_amount = target_frames - frames
    return F.pad(mel, (0, pad_amount))


def collate_batch(batch: list[dict]) -> dict[str, torch.Tensor]:
    mels = [pad_or_crop_mel(sample["mel"], TARGET_FRAMES) for sample in batch]
    params = [sample["params"] for sample in batch]
    f0s = [sample["f0"] for sample in batch]
    param_ids = [sample["param_id"] for sample in batch]

    mel_tensor = torch.stack(mels, dim=0)          # [B, 128, 750]
    mel_tensor = mel_tensor.unsqueeze(1)           # [B, 1, 128, 750]

    params_tensor = torch.stack(params, dim=0)     # [B, 17]
    f0_tensor = torch.tensor(f0s, dtype=torch.float32)      # [B]
    param_id_tensor = torch.tensor(param_ids, dtype=torch.long)

    return {
        "mel": mel_tensor,
        "params": params_tensor,
        "f0": f0_tensor,
        "param_id": param_id_tensor,
    }


def build_dataloader(dataset_dir: Path, split: str) -> DataLoader:
    dataset = SynthDataset(dataset_dir=dataset_dir, split=split)
    return DataLoader(
        dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=0,
        collate_fn=collate_batch,
    )


# %% Model
class ConvGruRegressor(nn.Module):
    def __init__(self, gru_hidden_size: int = 256):
        super().__init__()

        conv_kwargs = dict(
            kernel_size=(48, 282),
            stride=(7, 41),
            padding=(87, 200),
        )

        self.conv1 = nn.Conv2d(in_channels=1, out_channels=8, **conv_kwargs)
        self.bn1 = nn.BatchNorm2d(8)

        self.conv2 = nn.Conv2d(in_channels=8, out_channels=8, **conv_kwargs)
        self.bn2 = nn.BatchNorm2d(8)

        self.conv3 = nn.Conv2d(in_channels=8, out_channels=1, **conv_kwargs)
        self.bn3 = nn.BatchNorm2d(1)

        self.gru = nn.GRU(
            input_size=22,
            hidden_size=gru_hidden_size,
            batch_first=True,
        )

        self.linear = nn.Linear(gru_hidden_size, NUM_PARAMS)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: [B, 1, 128, 750]
        x = F.relu(self.bn1(self.conv1(x)))
        x = F.relu(self.bn2(self.conv2(x)))
        x = F.relu(self.bn3(self.conv3(x)))

        # [B, 1, 128, 750] -> [B, 750, 128]
        x = x.squeeze(1).transpose(1, 2)

        gru_out, _ = self.gru(x)
        last_timestep = gru_out[:, -1, :]
        params = self.linear(last_timestep)
        params = torch.sigmoid(params)

        # [B, 17]
        return params


# %% Loss schedule
def get_loss_weights(epoch_index: int, total_epochs: int) -> tuple[float, float]:
    progress = epoch_index / max(1, total_epochs - 1)

    if progress < 0.125:
        return 1.0, 0.0

    if progress < 0.5:
        mix_progress = (progress - 0.125) / 0.375
        param_weight = 1.0 - 0.5 * mix_progress
        spectral_weight = 0.5 * mix_progress
        return param_weight, spectral_weight

    return 0.5, 0.5


# %% Differentiable render path
def render_predicted_mels(pred_params: torch.Tensor, f0s: torch.Tensor) -> torch.Tensor:
    """
    This is the key function for spectral-loss training.

    It should return:
        [B, 128, T]

    # params [B, 17] and f0s [B]
    # along the batch dimension, convert the parameters into mel spectrograms
    """
    adsr1 = synth.adsr_envelope_batch(pred_params[:, 7:12])
    adsr2 = synth.adsr_envelope_batch(pred_params[:, 12:17])
    audio = synth.synthesize_a_batch(pred_params, adsr1, adsr2, f0s)
    pred_mels = synth.audio_to_log_mel_batch(audio)

    return pred_mels


# %% Training / validation
@torch.no_grad()
def evaluate(model: nn.Module, loader: DataLoader) -> dict[str, float]:
    model.eval()

    param_loss_sum = 0.0
    spectral_loss_sum = 0.0
    total_items = 0

    for batch in loader:
        mel = batch["mel"].to(DEVICE)
        mel = mel[:, :TARGET_FRAMES]
        target_params = batch["params"].to(DEVICE)
        f0s = batch["f0"].to(DEVICE)

        pred_params = model(mel)

        param_l1 = F.l1_loss(pred_params, target_params)

        pred_mels = render_predicted_mels(pred_params, f0s).to(DEVICE)
        pred_mels = pred_mels[:, :TARGET_FRAMES]
        target_mels = mel.squeeze(1)
        spectral_l1 = F.l1_loss(pred_mels, target_mels)

        batch_size = mel.shape[0]
        param_loss_sum += float(param_l1.item()) * batch_size
        spectral_loss_sum += float(spectral_l1.item()) * batch_size
        total_items += batch_size

    return {
        "param_l1": param_loss_sum / max(1, total_items),
        "spectral_l1": spectral_loss_sum / max(1, total_items),
    }


def train() -> None:
    train_loader = build_dataloader(DATASET_DIR, split="train")
    test_loader = build_dataloader(DATASET_DIR, split="test")

    model = ConvGruRegressor(gru_hidden_size=GRU_HIDDEN_SIZE).to(DEVICE)
    optimizer = torch.optim.Adam(model.parameters(), lr=INITIAL_LR)
    scheduler = torch.optim.lr_scheduler.ExponentialLR(optimizer, gamma=LR_GAMMA)

    torch.autograd.set_detect_anomaly(True)

    for epoch in range(EPOCHS):
        model.train()

        epoch_param_loss = 0.0
        epoch_spectral_loss = 0.0
        epoch_total_loss = 0.0
        total_items = 0

        param_weight, spectral_weight = get_loss_weights(epoch, EPOCHS)

        for batch in train_loader:
            mel = batch["mel"].to(DEVICE)                    # [B, 1, 128, 750
            target_params = batch["params"].to(DEVICE)      # [B, 17]
            f0s = batch["f0"].to(DEVICE)                    # [B]

            optimizer.zero_grad()

            pred_params = model(mel)

            param_l1 = F.l1_loss(pred_params, target_params)

            pred_mels = render_predicted_mels(pred_params, f0s).to(DEVICE)
            pred_mels = pred_mels[:, :, :TARGET_FRAMES]
            target_mels = mel.squeeze(1)                    # [B, 128, 750]
            spectral_l1 = F.l1_loss(pred_mels, target_mels)

            with torch.no_grad():
                param_scale = spectral_l1.detach() / (param_l1.detach() + 1e-8)

            scaled_param_l1 = param_l1 * param_scale
            total_loss = (param_weight * scaled_param_l1) + (spectral_weight * spectral_l1)

            total_loss.backward()
            optimizer.step()

            batch_size = mel.shape[0]
            epoch_param_loss += float(param_l1.item()) * batch_size
            epoch_spectral_loss += float(spectral_l1.item()) * batch_size
            epoch_total_loss += float(total_loss.item()) * batch_size
            total_items += batch_size

        scheduler.step()

        train_metrics = {
            "param_l1": epoch_param_loss / max(1, total_items),
            "spectral_l1": epoch_spectral_loss / max(1, total_items),
            "total": epoch_total_loss / max(1, total_items),
        }
        test_metrics = evaluate(model, test_loader)

        current_lr = scheduler.get_last_lr()[0]

        print(
            f"epoch {epoch + 1:03d}/{EPOCHS} | "
            f"lr={current_lr:.6f} | "
            f"weights(param={param_weight:.3f}, spectral={spectral_weight:.3f}) | "
            f"train_total={train_metrics['total']:.6f} | "
            f"train_param={train_metrics['param_l1']:.6f} | "
            f"train_spec={train_metrics['spectral_l1']:.6f} | "
            f"test_param={test_metrics['param_l1']:.6f} | "
            f"test_spec={test_metrics['spectral_l1']:.6f}"
        )

#%%

if __name__ == "__main__":
    train()