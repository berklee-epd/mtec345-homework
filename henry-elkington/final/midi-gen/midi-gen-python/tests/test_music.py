from midi_morph.music import NoteEvent, chord_pitches, melodic_pattern_for_chord, rank_chords


def test_rank_chords_prefers_c_major_for_c_e_g():
    choices = rank_chords(
        [
            NoteEvent(60, 0, 120),
            NoteEvent(64, 0, 120),
            NoteEvent(67, 0, 120),
        ]
    )

    assert choices[0].root == 0
    assert choices[0].quality == "maj"


def test_chord_pitches_are_in_requested_octave():
    choice = rank_chords([NoteEvent(69, 0, 120), NoteEvent(72, 0, 120), NoteEvent(76, 0, 120)])[0]

    assert chord_pitches(choice, octave=3) == [57, 60, 64]


def test_melodic_pattern_uses_chord_tones():
    pattern = melodic_pattern_for_chord({0, 4, 7}, previous_pitch=None, octave=5)

    assert pattern
    assert {pitch % 12 for pitch in pattern}.issubset({0, 4, 7})
