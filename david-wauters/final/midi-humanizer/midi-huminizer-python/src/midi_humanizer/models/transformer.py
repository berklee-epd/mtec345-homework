from __future__ import annotations

import torch
from torch import nn


class TransformerHumanizer(nn.Module):
    def __init__(
        self,
        feature_dim: int,
        pitch_vocab_size: int = 128,
        pitch_embedding_dim: int = 32,
        model_dim: int = 192,
        num_layers: int = 4,
        num_heads: int = 6,
        dropout: float = 0.2,
        max_positions: int = 4096,
    ) -> None:
        super().__init__()
        self.pitch_embedding = nn.Embedding(pitch_vocab_size, pitch_embedding_dim)
        self.position_embedding = nn.Embedding(max_positions, model_dim)
        self.input_projection = nn.Linear(pitch_embedding_dim + feature_dim, model_dim)
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=model_dim,
            nhead=num_heads,
            dim_feedforward=model_dim * 4,
            dropout=dropout,
            batch_first=True,
            activation="gelu",
        )
        self.encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.output = nn.Sequential(
            nn.Linear(model_dim, model_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(model_dim, 3),
        )

    def forward(
        self,
        pitches: torch.Tensor,
        features: torch.Tensor,
        mask: torch.Tensor,
    ) -> torch.Tensor:
        batch_size, seq_len = pitches.shape
        if seq_len > self.position_embedding.num_embeddings:
            raise ValueError(
                f"Sequence length {seq_len} exceeds maximum {self.position_embedding.num_embeddings}."
            )

        pitch_embed = self.pitch_embedding(pitches)
        x = torch.cat([pitch_embed, features], dim=-1)
        x = self.input_projection(x)

        positions = torch.arange(seq_len, device=pitches.device).unsqueeze(0).expand(
            batch_size,
            seq_len,
        )
        x = x + self.position_embedding(positions)
        encoded = self.encoder(x, src_key_padding_mask=~mask)
        return self.output(encoded)
