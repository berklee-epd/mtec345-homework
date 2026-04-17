# %% Imports and setup
import torch
import io
import base64
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
from IPython import display
from scipy.io import wavfile
from scipy import signal as scipy_signal
#import synth
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import pandas as pd
from pathlib import Path
import math

#if not torch.backends.mps.is_available():
#    if not torch.backends.mps.is_built():
#        print("MPS not available because the current PyTorch install was not "
#              "built with MPS enabled.")
#    else:
#        print("MPS not available because the current macOS version is not 14.0+ "
#              "and/or you do not have an MPS-enabled device on this machine.")
#
#else:
#    mps_device = torch.device("mps")
#    torch.set_default_device(mps_device)

#%% Config
SR = 48000
seconds = 4
NUM_SAMPLES = int(SR*seconds)
wavetable_samples = 2**13
start_note = 21
num_of_notes = 12
note_increment = 7
simultaneous_generators = 1
total_parameter_vectors = 200
generate = True
simpleSynth = True


PARAMS = ["i1ratio","i1index1","i1index2","i2index2","i2index1","i1out","i2out","iattack1","idecay1","isustaintime1","isustain1","irelease1","iattack2","idecay2","isustaintime2","isustain2","irelease2"]
stoi = {param: i for i, param in enumerate(PARAMS)}
itos = {i: name for i, name in enumerate(PARAMS)}

wavetable = torch.sin(torch.linspace(0, 2*np.pi, wavetable_samples))
wavetable = torch.cat([wavetable, wavetable[:1]], dim=0)

#%% Preprocssing (only run if needed)
MELS = 128
FFT = 1024
HOP_LENGTH = FFT // 4



#%% Helper Functions
def show_waveform(tensor1, tensor2=None, title="Waveform"):
    """Display one or two waveforms. Second waveform shown in orange."""
    plt.figure(figsize=(10, 3))
    plt.plot(tensor1, color='tab:blue')
    if tensor2 is not None:
        plt.plot(tensor2, color='tab:orange')
    plt.title(title)
    plt.xlabel("Sample")
    plt.ylabel("Amplitude")
    plt.grid(True, alpha=0.3)
    plt.show()

def play_torch(audio):
    """Play audio in a notebook using HTML5 audio widget."""
    if isinstance(audio, torch.Tensor):
        audio = audio.detach().cpu()

        if audio.ndim == 2:
            audio = audio[0]

        audio = audio.clamp(-1.0, 1.0)
        audio_np = audio.numpy()
    else:
        audio_np = np.asarray(audio)
        if audio_np.ndim == 2:
            audio_np = audio_np[0]

    normalizer = float(np.iinfo(np.int16).max)
    audio_int16 = (audio_np * normalizer).astype(np.int16)

    memfile = io.BytesIO()
    wavfile.write(memfile, SR, audio_int16)

    html = """<audio controls>
                <source src="data:audio/wav;base64,{base64_wavfile}" type="audio/wav" />
                Your browser does not support the audio element.
              </audio>"""

    html = html.format(
        base64_wavfile=base64.b64encode(memfile.getvalue()).decode("ascii")
    )
    memfile.close()
    display.display(display.HTML(html))

def play_audio(audio):
    if isinstance(audio, torch.Tensor):
        audio = audio.detach().cpu().float().numpy()
    else:
        audio = np.asarray(audio, dtype=np.float32)

    if audio.ndim == 2:
        audio = audio[0]

    audio = np.clip(audio, -1.0, 1.0)
    sd.play(audio, SR)
    sd.wait()

def specplot(audio, vmin=-5, vmax=1, rotate=True, size=768):
    """Plot the log-magnitude spectrogram of audio using torch.stft and matplotlib.pyplot."""
    if not isinstance(audio, torch.Tensor):
        audio = torch.tensor(audio, dtype=torch.float32)
    else:
        audio = audio.detach().cpu().float()

    if audio.ndim == 2:
        audio = audio[0]

    hop_length = size // 4
    window = torch.hann_window(size)

    stft = torch.stft(
        audio,
        n_fft=size,
        hop_length=hop_length,
        win_length=size,
        window=window,
        center=True,
        return_complex=True,
    )

    logmag = torch.log10(torch.abs(stft) + 1e-7)

    if rotate:
        logmag = torch.flip(logmag, dims=[0])

    logmag = logmag.numpy()

    plt.figure(figsize=(10, 4))
    plt.imshow(
        logmag,
        vmin=vmin,
        vmax=vmax,
        cmap="magma",
        aspect="auto",
        origin="upper" if rotate else "lower",
    )
    plt.xlabel("Time")
    plt.ylabel("Frequency")
    plt.xticks([])
    plt.yticks([])
    plt.tight_layout()
    plt.show()

midi_to_freq = {
    midi: 440.0 * (2 ** ((midi - 69) / 12))
    for midi in range(128)
}

def encode_random():
    """randomize the parameters"""
    out = torch.rand(len(PARAMS), dtype=torch.float32)
    if simpleSynth:
        out[1] = 0.0
        out[3] = 0.0
    return out

def encode_from_file(file_number: int):
    path = Path(f"Generated/{file_number:04d}.txt")

    with path.open("r") as f:
        lines = f.readlines()

    header_end =  "---------END OF HEADER--------------\n"
    start_line = lines.index(header_end) + 1
    values = []
    for line in lines[start_line : start_line + 17]:
        values.append(float(line.strip("\n")))

    if simpleSynth:
        values[1] = 0.0
        values[3] = 0.0
    return values

def decode(values):
    return dict(zip(PARAMS, values))

def save_audio(audio, file_number: int):
    path = Path(f"Generated/{file_number:04d}.wav")
    if isinstance(audio, torch.Tensor):
        audio = audio.detach().cpu().float().numpy()
    else:
        audio = np.asarray(audio, dtype=np.float32)

    if audio.ndim == 2:
        audio = audio[0]

    wavfile.write(path, SR, audio)

def adsr(adstsr_numSamples: torch.Tensor):
    a,d,s_time,s_level,r,num_samples = adstsr_numSamples
    adstr = torch.tensor([a,d,s_time,r])
    adstr = torch.softmax(adstr, dim=0)
    attack = torch.linspace(0.0,1.0, int(num_samples*adstr[0].item()))
    decay = torch.linspace(1.0, s_level.item(), int(num_samples*adstr[1].item()))
    sustain = torch.linspace(s_level.item(), s_level.item(), int(num_samples*adstr[2].item()))
    envelope = torch.concat([attack, decay, sustain], dim=0)
    release = torch.linspace(s_level.item(), 0.0, int(num_samples-len(envelope)))
    envelope = torch.concat([envelope, release], dim=0)
    return envelope

def linear_lookup(phase: float, wavetable: torch.Tensor):
    phase = phase % 1.0
    table_size = wavetable.shape[0] - 1
    index = phase * table_size
    i0 = int(math.floor(index))
    i1 = i0 + 1
    frac = index - i0
    return wavetable[i0] * (1.0 - frac) + wavetable[i1] * frac

def synthesize(parameters: torch.Tensor, f0: float):
    adsr1 = adsr(torch.cat([parameters[7:12], torch.tensor([NUM_SAMPLES])], dim=0))
    adsr2 = adsr(torch.cat([parameters[12:17], torch.tensor([NUM_SAMPLES])], dim=0))
    ratio1 = parameters[0] * 16
    ratio2 = 1
    i1index2 = parameters[2] * 14.5
    i2index1 = parameters[4] * 14.5
    iout1 = parameters[5]
    iout2 = parameters[6]

    a1 = torch.zeros(NUM_SAMPLES)
    a2 = torch.zeros(NUM_SAMPLES)
    phase1 = 0.0
    phase2 = 0.0

    for sample in range(NUM_SAMPLES):
        if sample == 0:
            freq1 = f0 * ratio1
            freq2 = f0 * ratio2
        else:
            freq1 = (f0 * ratio1)*(1 + float(a2[sample-1]) * i2index1)
            freq2 = (f0 * ratio2)*(1 + float(a1[sample-1]) * i1index2)

        #if sample % 1000 == 0:
        #    print(freq1, freq2)

        a1[sample] = linear_lookup(phase1, wavetable)
        a1[sample] = a1[sample] * adsr1[sample]

        a2[sample] = linear_lookup(phase2, wavetable)
        a2[sample] = a2[sample] * adsr2[sample]

        phase1 = (phase1 + freq1 / float(SR)) % 1.0
        phase2 = (phase2 + freq2 / float(SR)) % 1.0

    return a1 * (iout1 / (iout1 + iout2)) + a2 * (iout2 / (iout1 + iout2))

#%% Parameters

if generate:
    params = encode_random()
if not generate:
    params = encode_from_file(1)


params = torch.cat([torch.tensor(params, dtype=torch.float32), torch.tensor([NUM_SAMPLES]), torch.tensor([SR]), torch.tensor([57])], dim=0).flatten()

print(decode(params))

#%% Synthesis
audio = synthesize(params)
show_waveform(audio)
specplot(audio)
save_audio(audio, SR, 1)