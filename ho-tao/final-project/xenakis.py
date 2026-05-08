import os
import random
import numpy as np
from pydub import AudioSegment

dataset_dir = "/content/ambient_slices"
output_file = "/content/stochastic_ambient_composition.wav"

composition_length_ms = 180000 

average_density_ms = 400 

print("Loading audio slices into memory...")
slices = [os.path.join(dataset_dir, f) for f in os.listdir(dataset_dir) if f.endswith('.wav')]

if not slices:
    print("Error: No .wav files found in the directory.")
else:
    canvas = AudioSegment.silent(duration=composition_length_ms)
    
    current_time = 0
    slice_count = 0
    
    print(f"Generating stochastic timeline ({composition_length_ms / 1000} seconds)...")
    
    while current_time < composition_length_ms:
        slice_path = random.choice(slices)
        audio_slice = AudioSegment.from_wav(slice_path)
        
        vol_adjustment = np.random.normal(0, 4)
        audio_slice = audio_slice + vol_adjustment
        
        pan_val = np.random.uniform(-1.0, 1.0)
        audio_slice = audio_slice.pan(pan_val)
        
        canvas = canvas.overlay(audio_slice, position=current_time)
        slice_count += 1
        
        time_step = np.random.exponential(scale=average_density_ms)
        current_time += int(time_step)
    
    print(f"Applying final fade out and exporting {slice_count} overlapping slices...")
    
    canvas = canvas.fade_out(5000)
    
    canvas.export(output_file, format="wav")
    
    print(f"Success! Composition saved to: {output_file}")      