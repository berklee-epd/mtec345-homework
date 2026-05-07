from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

import torch
from miditok import TokSequence
from torch.utils.data import DataLoader, Dataset

from midi_morph.model import TokenTransformer, TransformerConfig
from midi_morph.tokenizer import MidiTokTokenizer, build_tokenizer


class MidiTokenDataset(Dataset[tuple[torch.Tensor, torch.Tensor]]):
    def __init__(
        self,
        midi_dir: Path,
        tokenizer_name: MidiTokTokenizer = MidiTokTokenizer.remi,
        seq_len: int = 512,
        stride: int | None = None,
        skip_bad_midi: bool = True,
    ):
        self.tokenizer = build_tokenizer(tokenizer_name)
        self.seq_len = seq_len
        self.examples: list[torch.Tensor] = []
        self.skipped_files: list[tuple[Path, str]] = []
        stride = stride or seq_len
        midi_paths = sorted(midi_dir.rglob("*.mid")) + sorted(midi_dir.rglob("*.midi"))
        if not midi_paths:
            raise ValueError(f"No MIDI files found under {midi_dir}")

        bos_id = self.tokenizer["BOS_None"]
        eos_id = self.tokenizer["EOS_None"]
        pad_id = self.tokenizer["PAD_None"]

        for midi_path in midi_paths:
            try:
                encoded = self.tokenizer.encode(midi_path)
            except Exception as exc:
                if not skip_bad_midi:
                    raise ValueError(f"Could not tokenize MIDI file {midi_path}: {exc}") from exc
                self.skipped_files.append((midi_path, str(exc)))
                continue
            sequences = encoded if isinstance(encoded, list) else [encoded]
            for sequence in sequences:
                ids = [bos_id, *sequence.ids, eos_id]
                if len(ids) < 2:
                    continue
                for start in range(0, max(1, len(ids) - 1), stride):
                    chunk = ids[start : start + seq_len + 1]
                    if len(chunk) < 2:
                        continue
                    if len(chunk) < seq_len + 1:
                        chunk = [*chunk, *([pad_id] * (seq_len + 1 - len(chunk)))]
                    self.examples.append(torch.tensor(chunk, dtype=torch.long))

        if not self.examples:
            if self.skipped_files:
                first_path, first_error = self.skipped_files[0]
                raise ValueError(
                    f"No token examples could be built from {midi_dir}. "
                    f"Skipped {len(self.skipped_files)} invalid MIDI files. "
                    f"First bad file: {first_path} ({first_error})"
                )
            raise ValueError(f"No token examples could be built from {midi_dir}")

    def __len__(self) -> int:
        return len(self.examples)

    def __getitem__(self, index: int) -> tuple[torch.Tensor, torch.Tensor]:
        chunk = self.examples[index]
        return chunk[:-1], chunk[1:]


def resolve_device(device: str) -> torch.device:
    if device != "auto":
        return torch.device(device)
    if torch.cuda.is_available():
        return torch.device("cuda")
    if torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


def train_model(
    midi_dir: Path,
    output_checkpoint: Path,
    *,
    tokenizer_name: MidiTokTokenizer = MidiTokTokenizer.remi,
    seq_len: int = 512,
    batch_size: int = 8,
    epochs: int = 5,
    learning_rate: float = 3e-4,
    d_model: int = 384,
    nhead: int = 6,
    num_layers: int = 6,
    dropout: float = 0.1,
    device: str = "auto",
    max_steps: int | None = None,
    skip_bad_midi: bool = True,
) -> dict[str, float | int | str]:
    if d_model % nhead != 0:
        raise ValueError(f"d_model={d_model} must be divisible by nhead={nhead}")
    dataset = MidiTokenDataset(
        midi_dir,
        tokenizer_name=tokenizer_name,
        seq_len=seq_len,
        skip_bad_midi=skip_bad_midi,
    )
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=True, drop_last=False)
    tokenizer = dataset.tokenizer
    pad_id = tokenizer["PAD_None"]
    torch_device = resolve_device(device)
    config = TransformerConfig(
        vocab_size=len(tokenizer),
        max_seq_len=seq_len,
        d_model=d_model,
        nhead=nhead,
        num_layers=num_layers,
        dropout=dropout,
    )
    model = TokenTransformer.from_config(config).to(torch_device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate, betas=(0.9, 0.95), weight_decay=0.1)

    model.train()
    step = 0
    last_loss = 0.0
    for _epoch in range(epochs):
        for inputs, targets in loader:
            inputs = inputs.to(torch_device)
            targets = targets.to(torch_device)
            targets = targets.masked_fill(targets == pad_id, -100)
            optimizer.zero_grad(set_to_none=True)
            _, loss = model(inputs, targets)
            if loss is None:
                raise RuntimeError("Training loss was not computed")
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            step += 1
            last_loss = float(loss.detach().cpu())
            if max_steps is not None and step >= max_steps:
                break
        if max_steps is not None and step >= max_steps:
            break

    output_checkpoint.parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "model_state": model.state_dict(),
            "model_config": asdict(config),
            "tokenizer": tokenizer_name.value,
            "seq_len": seq_len,
            "loss": last_loss,
            "steps": step,
        },
        output_checkpoint,
    )
    return {
        "loss": last_loss,
        "steps": step,
        "examples": len(dataset),
        "device": str(torch_device),
        "skipped_files": len(dataset.skipped_files),
        "first_skipped": str(dataset.skipped_files[0][0]) if dataset.skipped_files else "",
    }


def load_checkpoint(checkpoint_path: Path, device: str = "auto") -> tuple[TokenTransformer, MidiTokTokenizer, torch.device]:
    torch_device = resolve_device(device)
    checkpoint = torch.load(checkpoint_path, map_location=torch_device)
    config = TransformerConfig(**checkpoint["model_config"])
    model = TokenTransformer.from_config(config)
    model.load_state_dict(checkpoint["model_state"])
    model.to(torch_device)
    model.eval()
    return model, MidiTokTokenizer(checkpoint["tokenizer"]), torch_device


@torch.no_grad()
def generate_midi(
    checkpoint_path: Path,
    output_midi: Path,
    *,
    prompt_midi: Path | None = None,
    max_new_tokens: int = 256,
    temperature: float = 1.0,
    top_k: int = 40,
    device: str = "auto",
) -> None:
    model, tokenizer_name, torch_device = load_checkpoint(checkpoint_path, device=device)
    tokenizer = build_tokenizer(tokenizer_name)
    bos_id = tokenizer["BOS_None"]
    eos_id = tokenizer["EOS_None"]

    if prompt_midi is None:
        ids = [bos_id]
    else:
        prompt = tokenizer.encode(prompt_midi)
        prompt_sequence = prompt[0] if isinstance(prompt, list) else prompt
        ids = [bos_id, *prompt_sequence.ids]

    for _ in range(max_new_tokens):
        context = ids[-model.config.max_seq_len :]
        tokens = torch.tensor([context], dtype=torch.long, device=torch_device)
        logits, _ = model(tokens)
        next_logits = logits[0, -1] / max(temperature, 1e-5)
        if top_k > 0:
            values, _ = torch.topk(next_logits, min(top_k, next_logits.shape[-1]))
            next_logits[next_logits < values[-1]] = -float("inf")
        probs = torch.softmax(next_logits, dim=-1)
        next_id = int(torch.multinomial(probs, num_samples=1).item())
        ids.append(next_id)
        if next_id == eos_id:
            break

    generated = [token_id for token_id in ids if token_id not in {bos_id, eos_id}]
    score = tokenizer.decode(TokSequence(ids=generated))
    output_midi.parent.mkdir(parents=True, exist_ok=True)
    score.dump_midi(output_midi)
