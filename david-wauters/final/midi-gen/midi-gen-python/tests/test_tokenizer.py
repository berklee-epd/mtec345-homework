import miditoolkit

from midi_morph.tokenizer import MidiTokTokenizer, build_tokenizer, decode_tokens, encode_midi


def _write_simple_midi(path):
    midi = miditoolkit.MidiFile(ticks_per_beat=480)
    piano = miditoolkit.Instrument(program=0, is_drum=False, name="Piano")
    piano.notes.append(miditoolkit.Note(velocity=80, pitch=60, start=0, end=480))
    piano.notes.append(miditoolkit.Note(velocity=80, pitch=64, start=0, end=480))
    piano.notes.append(miditoolkit.Note(velocity=80, pitch=67, start=0, end=480))
    midi.instruments.append(piano)
    midi.dump(str(path))


def test_build_tokenizer_supports_remi_and_tsd():
    assert type(build_tokenizer(MidiTokTokenizer.remi)).__name__ == "REMI"
    assert type(build_tokenizer(MidiTokTokenizer.tsd)).__name__ == "TSD"


def test_miditok_encode_decode_round_trip(tmp_path):
    midi_path = tmp_path / "input.mid"
    tokens_path = tmp_path / "tokens.json"
    output_path = tmp_path / "output.mid"
    _write_simple_midi(midi_path)

    encode_midi(midi_path, tokens_path, tokenizer_name=MidiTokTokenizer.remi)
    decode_tokens(tokens_path, output_path, tokenizer_name=MidiTokTokenizer.remi)

    assert tokens_path.exists()
    assert output_path.exists()
