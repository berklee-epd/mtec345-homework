from __future__ import annotations

from torch import nn

from midi_humanizer.models.rnn import RNNHumanizer
from midi_humanizer.models.transformer import TransformerHumanizer


def build_model(model_type: str, feature_dim: int) -> nn.Module:
    if model_type == "rnn":
        return RNNHumanizer(feature_dim=feature_dim)
    if model_type == "transformer":
        return TransformerHumanizer(feature_dim=feature_dim)
    raise ValueError(f"Unsupported model type: {model_type}")
