from __future__ import annotations

import argparse
from pathlib import Path

from midi_humanizer.data.midi import export_quantized_midi
from midi_humanizer.data.maestro import preprocess_maestro_dataset
from midi_humanizer.infer import InferenceConfig, humanize_file
from midi_humanizer.train import TrainConfig, train


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="midi-humanizer",
        description="Train and run a MAESTRO-based MIDI humanizer.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare_parser = subparsers.add_parser(
        "prepare-maestro",
        help="Preprocess MAESTRO into cached PyTorch tensors.",
    )
    prepare_parser.add_argument("--dataset-root", type=Path, required=True)
    prepare_parser.add_argument("--cache-dir", type=Path, default=Path("artifacts/cache"))
    prepare_parser.add_argument("--subdivisions", type=int, default=4)
    prepare_parser.add_argument("--velocity-bin", type=int, default=8)

    train_parser = subparsers.add_parser("train", help="Train a humanization model.")
    train_parser.add_argument("--dataset-root", type=Path, required=True)
    train_parser.add_argument("--cache-dir", type=Path, default=Path("artifacts/cache"))
    train_parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("artifacts/checkpoints"),
    )
    train_parser.add_argument(
        "--model-type",
        choices=["rnn", "transformer"],
        default="rnn",
    )
    train_parser.add_argument("--epochs", type=int, default=20)
    train_parser.add_argument("--batch-size", type=int, default=12)
    train_parser.add_argument("--learning-rate", type=float, default=3e-4)
    train_parser.add_argument("--weight-decay", type=float, default=1e-4)
    train_parser.add_argument("--seq-len", type=int, default=256)
    train_parser.add_argument("--stride", type=int, default=128)
    train_parser.add_argument("--subdivisions", type=int, default=4)
    train_parser.add_argument("--velocity-bin", type=int, default=8)
    train_parser.add_argument("--num-workers", type=int, default=0)
    train_parser.add_argument("--seed", type=int, default=7)

    humanize_parser = subparsers.add_parser(
        "humanize",
        help="Humanize a rigid MIDI clip with a trained model.",
    )
    humanize_parser.add_argument("--checkpoint", type=Path, required=True)
    humanize_parser.add_argument("--input-midi", type=Path, required=True)
    humanize_parser.add_argument("--output-midi", type=Path, required=True)
    humanize_parser.add_argument("--strength", type=float, default=1.0)

    quantized_parser = subparsers.add_parser(
        "export-quantized",
        help="Write the quantized version of a MIDI file to disk.",
    )
    quantized_parser.add_argument("--input-midi", type=Path, required=True)
    quantized_parser.add_argument("--output-midi", type=Path, required=True)
    quantized_parser.add_argument("--subdivisions", type=int, default=4)
    quantized_parser.add_argument("--velocity-bin", type=int, default=8)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "prepare-maestro":
        counts = preprocess_maestro_dataset(
            dataset_root=args.dataset_root,
            output_dir=args.cache_dir,
            subdivisions=args.subdivisions,
            velocity_bin=args.velocity_bin,
        )
        print(f"prepared_splits={counts}")
        return

    if args.command == "train":
        checkpoint_path = train(
            TrainConfig(
                dataset_root=args.dataset_root,
                cache_dir=args.cache_dir,
                output_dir=args.output_dir,
                model_type=args.model_type,
                epochs=args.epochs,
                batch_size=args.batch_size,
                learning_rate=args.learning_rate,
                weight_decay=args.weight_decay,
                seq_len=args.seq_len,
                stride=args.stride,
                subdivisions=args.subdivisions,
                velocity_bin=args.velocity_bin,
                num_workers=args.num_workers,
                seed=args.seed,
            )
        )
        print(f"best_checkpoint={checkpoint_path}")
        return

    if args.command == "humanize":
        humanize_file(
            InferenceConfig(
                checkpoint_path=args.checkpoint,
                midi_path=args.input_midi,
                output_path=args.output_midi,
                strength=args.strength,
            )
        )
        print(f"wrote_output={args.output_midi}")
        return

    if args.command == "export-quantized":
        export_quantized_midi(
            midi_path=args.input_midi,
            output_path=args.output_midi,
            subdivisions=args.subdivisions,
            velocity_bin=args.velocity_bin,
        )
        print(f"wrote_output={args.output_midi}")
        return

    raise ValueError(f"Unsupported command: {args.command}")
