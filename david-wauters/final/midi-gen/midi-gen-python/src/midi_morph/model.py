from __future__ import annotations

from dataclasses import asdict, dataclass

import torch
import torch.nn.functional as F
from torch import nn


@dataclass(frozen=True)
class TransformerConfig:
    vocab_size: int
    max_seq_len: int = 512
    d_model: int = 384
    nhead: int = 6
    num_layers: int = 6
    dropout: float = 0.1


class TokenTransformer(nn.Module):
    """Causal Transformer language model for miditok token streams."""

    def __init__(
        self,
        vocab_size: int,
        max_seq_len: int = 512,
        d_model: int = 384,
        nhead: int = 6,
        num_layers: int = 6,
        dropout: float = 0.1,
    ):
        super().__init__()
        self.config = TransformerConfig(
            vocab_size=vocab_size,
            max_seq_len=max_seq_len,
            d_model=d_model,
            nhead=nhead,
            num_layers=num_layers,
            dropout=dropout,
        )
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.position = nn.Embedding(max_seq_len, d_model)
        self.dropout = nn.Dropout(dropout)
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=d_model * 4,
            dropout=dropout,
            batch_first=True,
            norm_first=True,
            activation="gelu",
        )
        self.encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.norm = nn.LayerNorm(d_model)
        self.output = nn.Linear(d_model, vocab_size)
        self.output.weight = self.embedding.weight

    def forward(self, tokens: torch.Tensor, targets: torch.Tensor | None = None) -> tuple[torch.Tensor, torch.Tensor | None]:
        if tokens.shape[1] > self.config.max_seq_len:
            raise ValueError(f"Sequence length {tokens.shape[1]} exceeds max_seq_len={self.config.max_seq_len}")
        positions = torch.arange(tokens.shape[1], device=tokens.device).unsqueeze(0)
        hidden = self.dropout(self.embedding(tokens) + self.position(positions))
        length = tokens.shape[1]
        mask = torch.triu(torch.ones(length, length, device=tokens.device), diagonal=1).bool()
        encoded = self.encoder(hidden, mask=mask)
        logits = self.output(self.norm(encoded))
        loss = None
        if targets is not None:
            loss = F.cross_entropy(logits.reshape(-1, logits.shape[-1]), targets.reshape(-1))
        return logits, loss

    @classmethod
    def from_config(cls, config: TransformerConfig) -> "TokenTransformer":
        return cls(**asdict(config))
