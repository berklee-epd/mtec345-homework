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
#General output settings example:
output = generate_diffusion_cond(
    model,
    steps=100,
    cfg_scale=7,
    conditioning=conditioning,
    sample_size=sample_size,
    sigma_min=0.3,
    sigma_max=500,
    sampler_type="dpmpp-3m-sde",
    device=device
)

# Prompts and settings in order of testing:

#Output: MX_dance.wav
"prompt": "100bpm disco dance track with 8 bar sections. song form with intro, verse, chorus, bridge, chorus chorus, outro",
"negative_prompt": "",
"seconds_start": 0,
"seconds_total": 48
steps=100,
cfg_scale=7,
sigma_min=0.3,
sigma_max=500,

#Output: MX_bass.wav
#Thoughts: does not follow any chords. May confuse breakbeat and bass, sounded like combo of them.
"prompt": "160 bpm breakbeat distorted bass with 8th note pulse. Chords: I, bVII, IV, bII, I",
"negative_prompt": "",
"seconds_start": 0,
"seconds_total": 30
steps=100,
cfg_scale=7,
sigma_min=0.3,
sigma_max=500,
#Output: MX_bass2.wav; try adding movement to progression by adjusting prompt and negative prompt. less control over progression. added more steps.
#Thoughts: still no chord movement. more variation, one half step higher.
"prompt": "160 bpm breakbeat distorted bass with 8th note pulse and moving evolving texture",
"negative_prompt": "static",
"seconds_start": 0,
"seconds_total": 30,
steps=200,
cfg_scale=7,
sigma_min=0.3,
sigma_max=500,

#Output: MX_breakbeat.wav
"prompt": "160 bpm breakbeat with metal pipe fall on cement, loud distorted clang with low pitch resonance, salt shaker hihat",
"negative_prompt": "low quality",
"seconds_start": 0,
"seconds_total": 30
steps=100,
cfg_scale=7,
sigma_min=0.3,
sigma_max=500,


#Output: AMB_rain.wav
"prompt": "in the countryside, rain is falling outside and hitting a tin roof and then splashing into puddles; there is some rolling thunder and gusts of wind",
"negative_prompt": "music",
"seconds_start": 0,
"seconds_total": 48,
steps=200,
cfg_scale=7,
sigma_min=0.1,
sigma_max=500,

#Output: SFX_metalPipe_100Steps.wav
#thoughts: too high pitched, not enough clang. 2 sfx within timespan
"prompt": "sound effect. industrial metal pipe fall on hard floor. foley recording.",
"negative_prompt": "music",
"seconds_start": 0,
"seconds_total": 10,
steps=100,
cfg_scale=7,
sigma_min=0.3,
sigma_max=500,
#Output: SFX_metalPipe_200Steps.wav; 200 steps, remove negative prompt, add low pitch to prompt
#thoughts: a bit lower in pitch and a bit more clang. 3 sfx in timespan. sounds better quality but still not following the prompt. still too high pitched and clattery.
"prompt": "sound effect. industrial metal pipe fall on hard floor. foley recording. low pitch clang impact",
"negative_prompt": "",
"seconds_start": 0,
"seconds_total": 10,
steps=200,
cfg_scale=7,
sigma_min=0.3,
sigma_max=500,

#Output: AMB_industrial.wav
"prompt": "field recording. industrial factory background machinery, background voices. foreground conveyor belt.",
"negative_prompt": "music",
"seconds_start": 0,
"seconds_total": 47,
steps=100,
cfg_scale=7,
sigma_min=0.3,
sigma_max=500,
#Output: AMB_industrial2.wav; 200 steps
#Notes: higher pitched, more variation
"negative_prompt": "music",
"seconds_start": 0,
"seconds_total": 47,
steps=200,
cfg_scale=7,
sigma_min=0.3,
sigma_max=500,
#Output: AMB_industrial3.wav; removed negative prompt
#Notes: lower pitched, less variation
"prompt": "field recording. industrial factory background machinery, background voices. foreground conveyor belt.",
"negative_prompt": "",
"seconds_start": 0,
"seconds_total": 47,
steps=100,
cfg_scale=7,
sigma_min=0.3,
sigma_max=500,
#Output: AMB_industrial4.wav; 150 steps and no negative prompt. perhaps the variation and pitch will balance out?
#Notes: lower pitched ambience, more variation. prediction was correct. but, more high pitched artifacts
"prompt": "field recording. industrial factory background machinery, background voices. foreground conveyor belt.",
"negative_prompt": "",
"seconds_start": 0,
"seconds_total": 47,
steps=150,
cfg_scale=7,
sigma_min=0.3,
sigma_max=500,

```      
Overall Observations:
- some prompt engineering is required; it's difficult to know exactly how the model wil respond to prompts. It reminds me of visual AI in 2020 when it took more prompt engineering to get high quality results.
- more time steps seems to make things higher pitched but better sound quality
- generation takes a long time, around 5 minutes
- there is a built in interface that can be used; I chose not to
- Getting it set up to run locally is a bit of a pain, though I created the documentation to hopefully make it easier for the next person.
- It works best in 44.1kHz, whereas I tend to use 48kHz for slightly more room to adjust pitch while retaining upper frequencies using granular synthesis. Oh well.
- seems to be better at ambience and field recrodings than one shot sfx and music
   - this is consistent with the training data used, which heavily featured field and foley recordings
- this model fits the workflow of creating short clips of audio and combining them in sample instruments and adding effects to create a piece

   - This is the workflow that DADABOTS used with this same model for the AI Song Contest.
   - This workflow fits experimental music better as compared with commercial products such as Suno, which from some observations can create very similar sounding music that fits mainstream genres better.
   - For this workflow, I should prioritize greater steps since it increases perceived quality. I can change the pitch content using granular synthesis.
   - I should use prompts that feature field recordings and use them to create sample instruments to create a piece of music


### Production

Shared setttings:
```python
"seconds_start": 0,
"seconds_total": 47,
steps=200,
cfg_scale=7,
conditioning=conditioning,
sample_size=sample_size,
sigma_min=0.3,
sigma_max=500,
sampler_type="dpmpp-3m-sde",
device=device

# SFX_SignalDrop.wav
"prompt": "static. phone. noise. signal sweep. sweep from high to low. falling pitch. TV. Field recording. Electronic.",

# SFX_SignalDrop2.wav
"seconds_total": 5,
steps=15,

# SFX_SignalDrop3.wav
"prompt": "static. noise. signal sweep. sweep from high to low. falling pitch. TV. Field recording. Electronic. low.",
"negative_prompt": "high pitch",
"seconds_start": 0,
"seconds_total": 10,
steps=25,

# AMB_Night.wav
"prompt": "night ambience. country. frogs, peepers, light wind, drops of water fall off leaves. field recording",
"negative_prompt": "high pitch",

# MX_ambientSynth.wav
"prompt": "ambient synth. evolving. sound design. middle c.",
"negative_prompt": "high pitch",

# AMB_stream.wav
"prompt": "gurgling stream with stones. field recording. birds. wind filters through leaves and trees.",

# MX_pluck.wav
"prompt": "mandolin pluck ambient jazz texture",

```


I chose some of these clips and used them to create an ambient piece. I didn't have much time to create the piece, so it's mixed terribly. I used Ozone to "master" the track. It evidently doesn't work well on a badly mixed track, one of its limitations. It would be interesting to test it on some of my well mixed tracks in the future.

To create the piece, I first used one of the signal drop files in a granular synthesizer. I adjusted pitch and speed to create various glitchy sounds. I added reverb and delay.
Next, I used the ambient synth file in a granulator. Using automation, I adjusted the values while playing along with the glitch sounds.

I then used my Max 4 live amplitude modulation plugin to multiply the ambient synth with the glitch texture. I used automation to adjust the amount of amplitude modulation over time.

Finally, I mixed in the "stream" pad and used an auto filter to turn it into wind, since it sounded more like wind than a stream. I also mixed in the night ambience sound and removed some of the high and low end.

I adjusted some automation and tried my best to mix some things quickly, then used Ozone to "master" the track.



Link to assets: [google drive](https://drive.google.com/drive/folders/1KlYOBlIUVHPDTamFagIMJ9nHqfbBUdxR?usp=sharing)