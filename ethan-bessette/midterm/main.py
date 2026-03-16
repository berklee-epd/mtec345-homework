# %%

#import torchaudio
import torch
import io
import base64
import sounddevice as sd
import numpy as np
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
adstr = torch.tensor([1.234,0.456,0.789, 0.285])
sustain_level = 0.7

adstr2 = torch.tensor([0.3, 1.452, 0.842, 0.239])
sustain_level2 = 0.5

#%%
k1 = synth.adsr(adstr[0], adstr[1], adstr[2], adstr[3], sustain_level, num_samples, sample_rate)
k2 = synth.adsr(adstr2[0], adstr2[1], adstr2[2], adstr2[3], sustain_level2, num_samples, sample_rate)
show_waveform(k1, k2)

#%%
wavetable = torch.sin(torch.linspace(0, 2*np.pi, wavetable_samples))
show_waveform(wavetable)
#%%
frequency_envelope = torch.linspace(440, 440, num_samples)
phase_velocity = frequency_envelope / float(sample_rate)  # cycles / sample
phase = torch.cumsum(phase_velocity, dim=0, dtype=torch.float32) % 1.0
show_waveform(phase[:1000])

#%%
audio = synth.fm_bank(220,1.0,1.0,10.471,12,0,1,k1,k2,wavetable,num_samples,sample_rate)
show_waveform(audio)
specplot(audio)
play_audio(audio, sample_rate)
