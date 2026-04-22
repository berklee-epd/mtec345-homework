import numpy as np
from PIL import Image
from symusic import Note, Score, Tempo, Track

MAJOR_PENTATONIC = [0, 2, 4, 7, 9]
MINOR_PENTATONIC = [0, 3, 5, 7, 10]
NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

VOICES = [
    ("Soprano", 5, 6),
    ("Alto",    4, 5),
    ("Tenor",   3, 4),
    ("Bass",    2, 3),
]


def build_scale(root, intervals, oct_min, oct_max):
    notes = []
    for octave in range(oct_min, oct_max + 1):
        for iv in intervals:
            pitch = 12 * octave + (root % 12) + iv
            if 0 <= pitch <= 127:
                notes.append(pitch)
    return sorted(set(notes))


def generate_key_schedule(num_pixels, pixels_per_bar, bars_per_key, seed=42):
    rng = np.random.default_rng(seed)
    schedule = []
    num_bars = num_pixels // pixels_per_bar
    for bar in range(0, num_bars, bars_per_key):
        root = int(rng.integers(0, 12))
        intervals = list(rng.choice([MAJOR_PENTATONIC, MINOR_PENTATONIC]))
        schedule.append((bar * pixels_per_bar, root, intervals))
    return schedule


def get_scale_at(pixel_idx, key_schedule, oct_min, oct_max):
    root, intervals = key_schedule[0][1], key_schedule[0][2]
    for start, r, iv in key_schedule:
        if start <= pixel_idx:
            root, intervals = r, iv
        else:
            break
    return build_scale(root, intervals, oct_min, oct_max)


def generate_voice(row, key_schedule, oct_min, oct_max, ticks_per_note=4):
    notes = []
    tick = 0
    i = 0

    while i < len(row):
        scale = get_scale_at(i, key_schedule, oct_min, oct_max)
        pitch = scale[round(int(row[i]) / 255 * (len(scale) - 1))]

        # Merge adjacent pixels with same pitch and key
        duration = ticks_per_note
        j = i + 1
        while j < len(row):
            next_scale = get_scale_at(j, key_schedule, oct_min, oct_max)
            next_pitch = next_scale[round(int(row[j]) / 255 * (len(next_scale) - 1))]
            if next_scale != scale or next_pitch != pitch:
                break
            duration += ticks_per_note
            j += 1

        notes.append(Note(tick * 0.25, duration * 0.25, pitch, 70, ttype="quarter"))
        tick += duration
        i = j

    return notes

## code

image = Image.open("mysun.jpg").convert("L").resize((128, 128), Image.Resampling.LANCZOS)
image = np.array(image)

Image.fromarray(image).save("chorale_processed.png")

# the rows of the melodys
row_indices = np.linspace(10, image.shape[0] - 11, len(VOICES), dtype=int) # [30, 39, 99, 39]

# key changes every 3 bars (4 pixels a bar)
key_schedule = generate_key_schedule(image.shape[1], pixels_per_bar=4, bars_per_key=6)

for start, root, intervals in key_schedule:
    name = "major" if intervals == MAJOR_PENTATONIC else "minor"

score = Score(ttype="quarter")
score.tempos.append(Tempo(0, 200, ttype="quarter"))

for (name, oct_min, oct_max), row_idx in zip(VOICES, row_indices):
    notes = generate_voice(image[row_idx], key_schedule, oct_min, oct_max)
    track = Track(ttype="quarter")
    track.name = name
    for n in notes:
        track.notes.append(n)
    score.tracks.append(track)

score.dump_midi("chorale.mid")

