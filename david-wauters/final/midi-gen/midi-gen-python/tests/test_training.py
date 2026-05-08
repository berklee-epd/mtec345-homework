import miditoolkit
import pytest

from midi_morph.training import load_checkpoint, train_model


def _write_midi(path, root):
    midi = miditoolkit.MidiFile(ticks_per_beat=480)
    piano = miditoolkit.Instrument(program=0, is_drum=False, name="Piano")
    for offset, pitch in enumerate([root, root + 4, root + 7, root + 12]):
        start = offset * 240
        piano.notes.append(miditoolkit.Note(velocity=80, pitch=pitch, start=start, end=start + 240))
    midi.instruments.append(piano)
    midi.dump(str(path))


def test_train_model_writes_loadable_checkpoint(tmp_path):
    midi_dir = tmp_path / "midi"
    midi_dir.mkdir()
    _write_midi(midi_dir / "one.mid", 60)
    _write_midi(midi_dir / "two.mid", 62)
    checkpoint = tmp_path / "model.pt"

    stats = train_model(
        midi_dir,
        checkpoint,
        seq_len=32,
        batch_size=1,
        epochs=1,
        d_model=64,
        nhead=4,
        num_layers=1,
        device="cpu",
        max_steps=1,
    )
    model, tokenizer_name, device = load_checkpoint(checkpoint, device="cpu")

    assert checkpoint.exists()
    assert stats["steps"] == 1
    assert model.config.vocab_size > 0
    assert tokenizer_name.value == "remi"
    assert str(device) == "cpu"


def test_train_model_skips_invalid_midi_by_default(tmp_path):
    midi_dir = tmp_path / "midi"
    midi_dir.mkdir()
    _write_midi(midi_dir / "valid.mid", 60)
    (midi_dir / "bad.mid").write_text("not a midi file")
    checkpoint = tmp_path / "model.pt"

    stats = train_model(
        midi_dir,
        checkpoint,
        seq_len=32,
        batch_size=1,
        epochs=1,
        d_model=64,
        nhead=4,
        num_layers=1,
        device="cpu",
        max_steps=1,
    )

    assert stats["skipped_files"] == 1
    assert stats["first_skipped"].endswith("bad.mid")


def test_train_model_strict_midi_reports_bad_path(tmp_path):
    midi_dir = tmp_path / "midi"
    midi_dir.mkdir()
    (midi_dir / "bad.mid").write_text("not a midi file")

    with pytest.raises(ValueError, match="bad.mid"):
        train_model(
            midi_dir,
            tmp_path / "model.pt",
            seq_len=32,
            batch_size=1,
            epochs=1,
            d_model=64,
            nhead=4,
            num_layers=1,
            device="cpu",
            max_steps=1,
            skip_bad_midi=False,
        )
