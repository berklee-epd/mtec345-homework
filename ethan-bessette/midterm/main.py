# %%

#import torchaudio
import torch
import io
import base64
import sounddevice as sd
import numpy as np
from numpy.random import random as rnd
import matplotlib.pyplot as plt
from IPython import display
from scipy.io import wavfile
from scipy import signal as scipy_signal
import synth


#%%
sample_rate = 48000
seconds = 5.0
num_samples = int(sample_rate*seconds)
wavetable_samples = 2**13

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

def play_torch(audio, sample_rate=48000):
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
    wavfile.write(memfile, sample_rate, audio_int16)

    html = """<audio controls>
                <source src="data:audio/wav;base64,{base64_wavfile}" type="audio/wav" />
                Your browser does not support the audio element.
              </audio>"""

    html = html.format(
        base64_wavfile=base64.b64encode(memfile.getvalue()).decode("ascii")
    )
    memfile.close()
    display.display(display.HTML(html))

def play_audio(audio, sample_rate):
    if isinstance(audio, torch.Tensor):
        audio = audio.detach().cpu().float().numpy()
    else:
        audio = np.asarray(audio, dtype=np.float32)

    if audio.ndim == 2:
        audio = audio[0]

    audio = np.clip(audio, -1.0, 1.0)
    sd.play(audio, sample_rate)
    sd.wait()


def specplot(audio, sample_rate=48000, vmin=-5, vmax=1, rotate=True, size=768):
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


 #%%
i1ratio = rnd(1)
i1index1 = rnd(1)
i1index2 = rnd(1)
i2index2 = rnd(1)
i2index1  = rnd(1)
i1out = rnd(1)
i2out = rnd(1)
iattack1 = rnd(1)
idecay1 = rnd(1)
isustaintime1 = rnd(1)
isustain1 = rnd(1)
irelease1 = rnd(1)
iattack2 = rnd(1)
idecay2 = rnd(1)
isustaintime2 = rnd(1)
isustain2 = rnd(1)
irelease2 = rnd(1)

#%%
k1 = synth.adsr(iattack1[0], idecay1[0], isustaintime1[0], irelease1[0], isustain1[0], num_samples, sample_rate)
k2 = synth.adsr(iattack2[0], idecay2[0], isustaintime2[0], irelease2[0], isustain2[0], num_samples, sample_rate)
show_waveform(k1, k2)

#%%
wavetable = torch.sin(torch.linspace(0, 2*np.pi, wavetable_samples))
show_waveform(wavetable)

#%%
audio = synth.fm_bank(220,i1ratio[0],1.0,i1index2[0],i2index1[0],i1out[0],i2out[0],k1,k2,wavetable,num_samples,sample_rate)
show_waveform(audio)
specplot(audio)
play_audio(audio, sample_rate)
