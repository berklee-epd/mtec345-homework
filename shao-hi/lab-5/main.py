import random
from symusic import Note, Score, Synthesizer, Tempo, Track, dump_wav

score = Score(960, ttype="quarter")
tempo = Tempo(0, 90, ttype="quarter")
score.tempos.append(tempo)

track = Track(ttype="quarter")

scale_degrees = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
length = len(scale_degrees)
notes = [60 + degree for degree in scale_degrees]
durations = [random.randint(1, 8) * 0.25 for _ in range(length)]
velocities = [random.randint(10, 100) for _ in range(length)]

beat = 0 # Note start time in quarter notes
for duration, pitch, velocity in zip(durations, notes, velocities):
    print(f"Adding note at beat {beat} for {duration} beats with pitch {pitch} and velocity {velocity}")
    note = Note(beat, duration, pitch, velocity, "quarter")
    track.notes.append(note)
    beat += duration

score.tracks.append(track)
score.dump_midi("melody.mid")

audio = Synthesizer().render(score)
dump_wav("melody.wav", audio, 44100)

