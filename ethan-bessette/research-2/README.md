# Machine Learning Research Project 2
AI Tools Review
Ethan Bessette

## The Process

### Setup
1. In the root directory:
```
curl -Lf https://github.com/Stability-AI/stable-audio-tools/archive/refs/heads/main.zip | tar -xz
```

2.
```
uv python pin 3.10
uv init
uv add pip hf
uv sync
source .venv/bin/activate
```

3.
```
cd stable-audio-tools-main
uv pip install .
```

The stable audio tools will install all the dependencies you need. If you accidentally enter `uv sync` again, you'll have to reinstall the dependencies. To avoid this, feel free to update `pyproject.toml` with all current packages.


4. Log in to Hugging Face to download the pre-trained weights. If you haven't already, make an account [here](huggingface.co). Then, navigate to the settings page, access tokens, and create a token. Then in the root directory:
`hf auth login`

5. Modify the conditioning section in `main.py`, adjusting the text prompt, start time, and total time.
6. In the same terminal, in the root directory: `python3 main.py`
    - You can check if the correct python3 is active with `which python3`


### Testing

```python
"prompt": "100bpm disco dance track with 8 bar sections. song form with intro, verse, chorus, bridge, chorus chorus, outro",
"negative_prompt": "",
"seconds_start": 0,
"seconds_total": 48
#Output: dance.wav

"prompt": "160 bpm breakbeat distorted bass with 8th note pulse. Chords: I, bVII, IV, bII, I",
"negative_prompt": "",
"seconds_start": 0,
"seconds_total": 30
#Output: bass.wav

"prompt": "160 bpm breakbeat with metal pipe fall on cement, loud distorted clang with low pitch resonance, salt shaker hihat",
"negative_prompt": "low quality",
"seconds_start": 0,
"seconds_total": 30
#Output: breakbeat.wav
```      


