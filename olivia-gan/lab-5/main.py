import random

NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

MIN_MIDI = 12  # C0
MAX_MIDI = 96  # C7

def midi_to_note_name(midi_number):
    note = NOTE_NAMES[midi_number % 12]
    octave = (midi_number // 12) - 1
    return f"{note}{octave}"

def generate_random_notes(length=24, min_midi=MIN_MIDI, max_midi=MAX_MIDI):
    pattern = []
    for _ in range(length):
        midi_note = random.randint(min_midi, max_midi)
        note_name = midi_to_note_name(midi_note)
        pattern.append(note_name)
    return pattern

pattern = generate_random_notes()

print("Generated 24-note pattern:")
print(" ".join(pattern))

NOTE_TO_SEMITONE = {
    "C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5,
    "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11
}

def note_name_to_voltage(note):
    if len(note) == 2:
        pitch = note[0]
        octave = int(note[1])
    else:
        pitch = note[:2]
        octave = int(note[2])

    midi = (octave + 1) * 12 + NOTE_TO_SEMITONE[pitch]
    voltage = (midi - 60) / 12   # C4 = 0V
    return round(voltage, 3)

voltages = [note_name_to_voltage(note) for note in pattern]
print(voltages)