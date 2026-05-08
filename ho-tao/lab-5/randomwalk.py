import random
from midiutil import MIDIFile


scale_midi = [60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82]

def generate_stochastic_midi(num_notes=32, filename="brownian_walk.mid"):
    midi = MIDIFile(1)
    
    track = 0
    channel = 0
    time = 0.0      
    tempo = 110    
    volume = 100  
    
    midi.addTrackName(track, time, "Whole-Tone Walk")
    midi.addTempo(track, time, tempo)
    
    current_index = 6 

    for _ in range(num_notes):
        pitch_roll = random.randint(1, 6)
        
        if pitch_roll in [1, 2]:
            current_index = max(0, current_index - 1)
        elif pitch_roll in [5, 6]:
            current_index = min(len(scale_midi) - 1, current_index + 1)
        
        current_pitch = scale_midi[current_index]

        duration_roll = random.randint(1, 6)
        
        if duration_roll in [1, 2, 3]:
            duration = 0.5  
        elif duration_roll in [4, 5]:
            duration = 1.0  
        else:
            duration = 2.0


        midi.addNote(track, channel, current_pitch, time, duration, volume)
        
        time += duration

    with open(filename, "wb") as output_file:
        midi.writeFile(output_file)
        
    print(f"Successfully generated {num_notes} notes and saved to '{filename}'")

# Run the generator
if __name__ == '__main__':
    generate_stochastic_midi(32, "xenakis_algorithm.mid")