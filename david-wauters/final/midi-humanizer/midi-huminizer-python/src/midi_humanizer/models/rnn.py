from __future__ import annotations

import torch
from torch import nn
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence


class RNNHumanizer(nn.Module):
    def __init__(
        self,
        feature_dim: int,
        pitch_vocab_size: int = 128,
        pitch_embedding_dim: int = 32,
        hidden_dim: int = 192,
        num_layers: int = 2,
        dropout: float = 0.2,
    ) -> None:
        super().__init__()
        self.pitch_embedding = nn.Embedding(pitch_vocab_size, pitch_embedding_dim)
        self.input_projection = nn.Linear(pitch_embedding_dim + feature_dim, hidden_dim)
        self.encoder = nn.LSTM(
            input_size=hidden_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0.0,
            bidirectional=True,
        )
        self.output = nn.Sequential(
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, 3),
        )

    def forward(
        self,
        pitches: torch.Tensor,
        features: torch.Tensor,
        lengths: torch.Tensor,
    ) -> torch.Tensor:
        pitch_embed = self.pitch_embedding(pitches)
        x = torch.cat([pitch_embed, features], dim=-1)
        x = self.input_projection(x)

        packed = pack_padded_sequence(
            x,
            lengths.cpu(),
            batch_first=True,
            enforce_sorted=False,
        )
        encoded, _ = self.encoder(packed)
        encoded, _ = pad_packed_sequence(encoded, batch_first=True)
        return self.output(encoded)
