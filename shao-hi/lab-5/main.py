import random
from symusic import Note, Score, Synthesizer, Tempo, Track, dump_wav



BPM           = 60
ROOT          = 52        
TOTAL_BARS    = 80
BEATS_PER_BAR = 4
TOTAL_BEATS   = TOTAL_BARS * BEATS_PER_BAR
SCALE_PITCHES = [64, 66, 67, 69, 71, 73, 74, 76, 78, 79, 81, 83]
CHORDS = {
    "i":   [0, 3, 7, 10],    
    "ii":  [2, 5, 9, 12],    
    "IV":  [5, 9, 12, 15],   
    "v":   [7, 10, 14, 17],  
    "VII": [10, 14, 17, 21], 
}
TRANSITIONS = {
    "i":   {"IV": 35, "VII": 30, "v": 25, "ii": 10},
    "ii":  {"v": 35,  "IV": 30,  "i": 25, "VII": 10},
    "IV":  {"i": 35,  "v": 30,   "VII": 25, "ii": 10},
    "v":   {"i": 40,  "IV": 30,  "VII": 20, "ii": 10},
    "VII": {"i": 35,  "IV": 30,  "v": 25,   "ii": 10},
}


def pick_next_chord(current):
    options = TRANSITIONS[current]
    return random.choices(list(options.keys()), list(options.values()))[0]

def pick_nearby(prev, candidates):
    weights = [1.0 / (1 + abs(p - prev)) for p in candidates]
    return random.choices(candidates, weights)[0]


# Drone

def make_drone():
    track = Track(ttype="quarter")
    track.name = "Drone"
    track.program = 89  

    options = [ROOT - 12, ROOT - 5, ROOT]  
    beat = 0.0

    while beat < TOTAL_BEATS:
        pitch    = random.choice(options)
        bars     = random.randint(8, 16)
        duration = min(bars * BEATS_PER_BAR, TOTAL_BEATS - beat)
        velocity = random.randint(40, 65)

        track.notes.append(Note(beat, duration, pitch, velocity, "quarter"))

        if random.random() < 0.4:
            track.notes.append(Note(beat, duration, pitch + 7, velocity - 10, "quarter"))

        beat += duration

    return track


# Pads

def make_chords():
    track = Track(ttype="quarter")
    track.name = "Chords"
    track.program = 92  

    chord = "i"
    beat = 0.0

    while beat < TOTAL_BEATS:
        bars     = random.randint(4, 8)
        duration = min(bars * BEATS_PER_BAR, TOTAL_BEATS - beat)
        velocity = random.randint(45, 70)
        pitches  = [ROOT + i for i in CHORDS[chord]]

        for i, p in enumerate(pitches):
            offset = i * random.uniform(0, 0.5)
            v = max(30, min(100, velocity + random.randint(-10, 10)))
            track.notes.append(Note(beat + offset, duration - offset, p, v, "quarter"))

        beat += duration
        chord = pick_next_chord(chord)

    return track


# Melody

def make_melody():
    track = Track(ttype="quarter")
    track.name = "Melody"
    track.program = 73  # flute

    beat = 8.0
    prev = None

    while beat < TOTAL_BEATS - 8:
        pitch    = pick_nearby(prev, SCALE_PITCHES) if prev else random.choice(SCALE_PITCHES)
        duration = random.choice([2, 3, 4, 6, 8])
        velocity = random.randint(55, 90)

        track.notes.append(Note(beat, duration, pitch, velocity, "quarter"))
        prev  = pitch
        beat += duration

        if random.random() < 0.5:
            beat += random.choice([2, 4, 6, 8])

    return track


# Stems

def render_stem(track):
    s = Score(960, ttype="quarter")
    s.tempos.append(Tempo(0, BPM, ttype="quarter"))
    s.tracks.append(track)
    return Synthesizer().render(s.to("tick"))


stems = {
    "stem_drone.wav":  make_drone,
    "stem_pads.wav":   make_chords,
    "stem_melody.wav": make_melody,
}

score = Score(960, ttype="quarter")
score.tempos.append(Tempo(0, BPM, ttype="quarter"))

for filename, fn in stems.items():
    track = fn()
    score.tracks.append(track)
    dump_wav(filename, render_stem(track), 44100)

score.dump_midi("drone.mid")
