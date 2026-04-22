from PIL import Image
import csv
import os
import random
from symusic import Note, Score, Synthesizer, Tempo, Track, dump_wav

img = Image.open("pixelated_photo.png").convert("RGB")
width, height = img.size
# the cell size (there are 300 in total)
rows = 15
cols = 20
cell_width = width // cols
cell_height = height // rows

cells = []

for r in range(rows):
    for c in range(cols):
        x0 = c * cell_width
        y0 = r * cell_height
        x1 = width if c == cols - 1 else (c + 1) * cell_width
        y1 = height if r == rows - 1 else (r + 1) * cell_height

        cell = img.crop((x0, y0, x1, y1))
        colors = cell.getcolors(maxcolors=cell.size[0] * cell.size[1]) or []
        if colors:
            dominant = max(colors, key=lambda t: t[0])[1] # lambda is simply what is changing (so that is the input cell being analyzed)
        else:
            dominant = cell.getpixel((cell.size[0] // 2, cell.size[1] // 2))

        rr, gg, bb = dominant
        hex_color = f"#{rr:02x}{gg:02x}{bb:02x}" # we actually don't need to use use hex color since we only using rgb values to evaluate the main color

        cells.append({
            "row": r,
            "col": c,
            "r": rr,
            "g": gg,
            "b": bb,
        })


# Make dictionary for the notes I want to use 
note_map = {
    "red": 60,      # C4
    "orange": 62,    # D4
    "green": 64,     # E4
    "yellow": 66,   # F#4
    "black": 67,    # G4
    "brown": 69,      # A4
    "white": 71,      # B4
    "gray": 72,      # C5
    "blue": 78      # F#5

}


# categorize the cells by matching them to my reference colors as shown in the palette dictionary 
def color_distance(c1, c2):
    return ((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2 + (c1[2] - c2[2])**2)**0.5

def get_color_name(cell_r, cell_g, cell_b):
    cell = (cell_r, cell_g, cell_b)
    # Make a dictionary using the colors in my image for the reference colors
    palette = {
        "red": (169, 42, 25),
        "orange": (255, 165, 98),
        "green": (65, 79, 64),
        "yellow": (198, 147, 82),
        "black": (16, 11, 5),
        "brown": (96, 65, 37), 
        "white": (202, 191, 169),
        "gray": (70, 59, 55),
        "blue": (105, 108, 127)
    }
    closest = min(palette, key=lambda name: color_distance(cell, palette[name]))
    return closest

# Now let's involve more symusic to provide the audio and MIDI files 


# create score
score = Score(960, ttype="quarter")
tempo = Tempo(0, 90, ttype="quarter")
score.tempos.append(tempo)

track = Track(ttype="quarter")

# Process image cells with random duration/velocity
beat = 0 # Note start time in quarter notes..took from example code
for cell in cells:
    r, g, b = int(cell["r"]), int(cell["g"]), int(cell["b"]) # get the rgb values in the cell we're analyzing 
    color_name = get_color_name(r, g, b) # what color is that cell?
    pitch = note_map[color_name]  # match the color to the pitch it should be based on our dictionary 
    
    # RANDOM duration and velocity...took from example code
    duration = random.randint(1, 8) * 0.25
    velocity = random.randint(10, 100)

# I do not need these lines from the example code because I'm using the image for pitches
# scale_degrees = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
# length = len(scale_degrees)
# notes = [60 + degree for degree in scale_degrees]

    print(f"Cell color {color_name} at pitch {pitch}, velocity:{velocity}, duration:{duration}") # changed this from example code for color 
    #took from example code 
    note = Note(beat, duration, pitch, velocity, "quarter") 
    track.notes.append(note)
    beat += duration
# I want to export...
score.tracks.append(track)
score.dump_midi("image_melody.mid") # changed name to image melody 

audio = Synthesizer().render(score)
dump_wav("image_melody.wav", audio, 44100) # changed name to image melody
