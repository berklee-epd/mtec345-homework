from miditok import MIDILike, REMI, Structured, CPWord
from symusic import Score

midi1 = Score("assets/MIDI/maracangalha.mid")
midi2 = Score("assets/MIDI/samba_sem_terra.mid")
midi3 = Score("assets/MIDI/song_of_the_moon.mid")
midi4 = Score("assets/MIDI/windmill_isle.mid")

midilike_tokens = MIDILike()(midi1)
remi_tokens = REMI()(midi2)
structured_tokens = Structured()(midi3)
cpword_tokens = CPWord()(midi4)

print("# Maracangalha (Tokenized with MIDI-Like)")
for i, track in enumerate(midilike_tokens):
    print(f"## === Track {i} ===")
    print(track.tokens[:100])
    print(f"## Total tokens: {len(track.tokens)}\n")

print("# samba sem terra (Tokenized with REMI)")
for i, track in enumerate(remi_tokens):
    print(f"## === Track {i} ===")
    print(track.tokens[:100])
    print(f"## Total tokens: {len(track.tokens)}\n")

print("# Song of the Moon (Tokenized with Structured)")
for i, track in enumerate(structured_tokens):
    print(f"## === Track {i} ===")
    print(track.tokens[:100])
    print(f"## Total tokens: {len(track.tokens)}\n")

print("# Windmill Isle (Tokenized with Compound Word)")
for i, track in enumerate(cpword_tokens):
    print(f"## === Track {i} ===")
    print(track.tokens[:100])
    print(f"## Total tokens: {len(track.tokens)}\n")