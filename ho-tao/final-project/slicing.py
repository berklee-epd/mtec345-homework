import os
import librosa
import soundfile as sf

SOURCE_DIR = '/content/drive/MyDrive/wavegan_data/source_audio'
OUTPUT_DIR = '/content/drive/MyDrive/wavegan_data/train'

TARGET_SR = 16000
CHUNK_SIZE = 16384 # Exactly 1.024 seconds at 16kHz

os.makedirs(OUTPUT_DIR, exist_ok=True)

files = [f for f in os.listdir(SOURCE_DIR) if f.endswith(('.wav', '.mp3', '.flac'))]
total_slices_created = 0

print(f"Found {len(files)} source files. Starting the chopping process...\n")

for filename in files:
    file_path = os.path.join(SOURCE_DIR, filename)
    print(f"Processing: {filename}")
    
    try:
        audio, _ = librosa.load(file_path, sr=TARGET_SR, mono=True)
    except Exception as e:
        print(f"  -> Skipping {filename}: Could not read file. ({e})")
        continue

    num_chunks = len(audio) // CHUNK_SIZE
    
    for i in range(num_chunks):
        start_sample = i * CHUNK_SIZE
        end_sample = start_sample + CHUNK_SIZE
        
        chunk = audio[start_sample:end_sample]
        
        base_name = os.path.splitext(filename)[0]
        output_filename = f"{base_name}_slice_{i:04d}.wav"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        sf.write(output_path, chunk, TARGET_SR)
        total_slices_created += 1

print(f"\nDone! Successfully created {total_slices_created} perfectly sized WaveGAN slices.")