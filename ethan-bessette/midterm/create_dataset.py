from os import cpu_count

import torch
import io
import base64
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
from IPython import display
from scipy.io import wavfile
import pandas as pd
from pathlib import Path
import math
import os
import random
from concurrent.futures import ProcessPoolExecutor, as_completed

#%% Config and constants
SR = 48000
seconds = 4
NUM_SAMPLES = int(SR*seconds)
wavetable_samples = 2**13
start_note = 21
num_of_notes = 12
note_increment = 7
generate = True
simpleSynth = True
total_parameter_vectors = 250
simultaneous_generators = 10


PARAMS = ["i1ratio","i1index1","i1index2","i2index2","i2index1","i1out","i2out","iattack1","idecay1","isustaintime1","isustain1","irelease1","iattack2","idecay2","isustaintime2","isustain2","irelease2"]
stoi = {param: i for i, param in enumerate(PARAMS)}
itos = {i: name for i, name in enumerate(PARAMS)}

MELS = 128
FFT = 1024
HOP_LENGTH = FFT // 4

NUM_SAMPLES_TENSOR = torch.tensor([NUM_SAMPLES], dtype=torch.float32)
STFT_WINDOW = torch.hann_window(FFT)

wavetable = torch.sin(torch.linspace(0, 2*np.pi, wavetable_samples))
wavetable = torch.cat([wavetable, wavetable[:1]], dim=0)



#%% NOTE_FREQS
midi_to_freq = {
    midi: 440.0 * (2 ** ((midi - 69) / 12))
    for midi in range(128)
}

def get_note_frequencies(start_midi: int, note_count: int, note_increment: int) -> list[float]:
    return [
        float(midi_to_freq[start_midi + i * note_increment])
        for i in range(note_count)
    ]


NOTE_FREQS = get_note_frequencies(start_midi=start_note, note_count=num_of_notes, note_increment=note_increment)


#%% MEL_FILTER
def hz_to_mel(hz: torch.Tensor) -> torch.Tensor:
    return 2595.0 * torch.log10(1.0 + hz / 700.0)

def mel_to_hz(mel: torch.Tensor) -> torch.Tensor:
    return 700.0 * (10.0 ** (mel / 2595.0) - 1.0)
def build_mel_filterbank(
    sample_rate: int,
    n_fft: int,
    n_mels: int,
    f_min: float = 0.0,
    f_max: float | None = None,
) -> torch.Tensor:
    if f_max is None:
        f_max = sample_rate / 2.0

    fft_freqs = torch.linspace(0.0, sample_rate / 2.0, n_fft // 2 + 1)
    mel_points = torch.linspace(
        hz_to_mel(torch.tensor(f_min)),
        hz_to_mel(torch.tensor(f_max)),
        n_mels + 2,
    )
    hz_points = mel_to_hz(mel_points)

    filters = torch.zeros(n_mels, n_fft // 2 + 1, dtype=torch.float32)

    for m in range(n_mels):
        left = hz_points[m]
        center = hz_points[m + 1]
        right = hz_points[m + 2]

        up_slope = (fft_freqs - left) / (center - left + 1e-8)
        down_slope = (right - fft_freqs) / (right - center + 1e-8)
        filters[m] = torch.clamp(torch.minimum(up_slope, down_slope), min=0.0)

    return filters


MEL_FILTER = build_mel_filterbank(SR, FFT, MELS)

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

def play_audio(audio, sample_rate=48000):
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


def encode_random():
    """randomize the parameters"""
    out = torch.rand(len(PARAMS), dtype=torch.float32)
    if simpleSynth:
        out[1] = 0.0
        out[3] = 0.0
    return out

def decode(values):
    return dict(zip(PARAMS, values))

def audio_to_log_mel(
    audio: torch.Tensor
) -> torch.Tensor:
    audio = audio.float()

    if audio.ndim == 1:
        audio = audio.unsqueeze(0)

    stft = torch.stft(
        audio,
        n_fft=FFT,
        hop_length=HOP_LENGTH,
        win_length=FFT,
        window=STFT_WINDOW,
        center=True,
        return_complex=True,
    )
    power = torch.abs(stft) ** 2
    mel = torch.matmul(MEL_FILTER.unsqueeze(0), power)
    mel = torch.log(mel + 1e-5)
    return mel.to(torch.float32)

#%% Synthesis
def adsr(adstsr: torch.Tensor):
    a, d, s_time, s_level, r = adstsr
    adstr = torch.tensor([a, d, s_time, r], dtype=torch.float32)
    adstr = torch.softmax(adstr, dim=0)

    attack = torch.linspace(0.0, 1.0, int(NUM_SAMPLES * adstr[0].item()))
    decay = torch.linspace(1.0, s_level.item(), int(NUM_SAMPLES * adstr[1].item()))
    sustain = torch.linspace(s_level.item(), s_level.item(), int(NUM_SAMPLES * adstr[2].item()))
    envelope = torch.concat([attack, decay, sustain], dim=0)
    release = torch.linspace(s_level.item(), 0.0, int(NUM_SAMPLES - len(envelope)))
    envelope = torch.concat([envelope, release], dim=0)
    return envelope

def linear_lookup(phases: torch.Tensor, wavetable: torch.Tensor):
    phases = phases % 1.0
    table_size = wavetable.shape[0] - 1
    index = phases * table_size
    i0 = torch.floor(index).long()
    i1 = i0 + 1
    frac = index - i0.to(index.dtype)
    return wavetable[i0] * (1.0 - frac) + wavetable[i1] * frac

def synthesize_k(parameters: torch.Tensor):
    k1 = adsr(parameters[7:12])
    k2 = adsr(parameters[12:17])
    return k1, k2
def synthesize_a(parameters: torch.Tensor, adsr1: torch.Tensor, adsr2: torch.Tensor, f0s: torch.Tensor):
    batch_size = f0s.shape[0]

    ratio1 = parameters[0] * 16
    iout1 = parameters[5]
    iout2 = parameters[6]
    denom = (iout1 + iout2).clamp_min(1e-8)

    a1 = torch.zeros((batch_size, NUM_SAMPLES), dtype=torch.float32)
    a2 = torch.zeros((batch_size, NUM_SAMPLES), dtype=torch.float32)
    phase1 = torch.zeros(batch_size, dtype=torch.float32)
    phase2 = torch.zeros(batch_size, dtype=torch.float32)

    adsrs1 = adsr1.unsqueeze(0).expand(batch_size, -1)
    adsrs2 = adsr2.unsqueeze(0).expand(batch_size, -1)

    base_freq1 = f0s * ratio1

    for sample in range(NUM_SAMPLES):
        if sample == 0:
            freq1 = base_freq1
            freq2 = f0s
        else:
            freq1 = base_freq1 * (1 + (a2[:, sample - 1]) * (parameters[4] * 14.5))
            freq2 = f0s * (1 + (a1[:, sample - 1]) * (parameters[2] * 14.5))

        a1[:, sample] = linear_lookup(phase1, wavetable) * adsrs1[:, sample]
        a2[:, sample] = linear_lookup(phase2, wavetable) * adsrs2[:, sample]

        phase1 = (phase1 + freq1 / float(SR)) % 1.0
        phase2 = (phase2 + freq2 / float(SR)) % 1.0

    return a1 * (iout1 / denom) + a2 * (iout2 / denom)

#%% Dataset Creation
def split_generation_counts(total_parameter_vectors: int, simultaneous_generators: int) -> list[int]:
    simultaneous_generators = max(1, simultaneous_generators)
    base = total_parameter_vectors // simultaneous_generators
    remainder = total_parameter_vectors % simultaneous_generators
    return [
        base + (1 if worker_index < remainder else 0)
        for worker_index in range(simultaneous_generators)
    ]

def assign_train_test_splits(param_ids: list[int], train_ratio: float = 0.8, seed: int = 1234) -> dict[int, str]:
    rng = random.Random(seed)
    param_ids = list(param_ids)
    rng.shuffle(param_ids)
    split_index = int(len(param_ids) * train_ratio)
    train_ids = set(param_ids[:split_index])
    return {
        param_id: ("train" if param_id in train_ids else "test")
        for param_id in param_ids
    }

def _worker_generate_examples(
    start_param_id: int,
    count: int,
    start_note: int,
    num_of_notes: int,
    note_increment: int,
    dataset_dir: str,
):
    dataset_root = Path(dataset_dir)
    examples_dir = dataset_root / "examples"
    examples_dir.mkdir(parents=True, exist_ok=True)

    params_by_id = {}
    records = []

    f0_batch = torch.tensor(NOTE_FREQS, dtype=torch.float32)

    for local_index in range(count):
        param_id = start_param_id + local_index
        params = encode_random().clone().to(torch.float32)
        params_by_id[param_id] = params

        k1, k2 = synthesize_k(params)
        audio_batch = synthesize_a(params, k1, k2, f0_batch)
        mel_batch = audio_to_log_mel(audio_batch)

        for note_offset, f0 in enumerate(NOTE_FREQS):
            midi_note = start_note + note_offset * note_increment
            mel = mel_batch[note_offset].contiguous().clone()

            example_rel_path = Path("examples") / f"{param_id:07d}_{midi_note:03d}.pt"
            example_abs_path = dataset_root / example_rel_path

            torch.save(
                {
                    "x": mel,
                    "y": param_id,
                    "f0": float(f0),
                },
                example_abs_path,
            )

            records.append(
                {
                    "example_path": str(example_rel_path),
                    "param_id": param_id,
                    "midi_note": midi_note,
                    "f0": float(f0),
                }
            )

    return params_by_id, records

def compute_train_stats(dataset_dir: Path, metadata: pd.DataFrame):
    train_rows = metadata[metadata["split"] == "train"]

    mel_sum = None
    mel_sq_sum = None
    frame_count = 0

    for _, row in train_rows.iterrows():
        item = torch.load(dataset_dir / row["example_path"], map_location="cpu")
        mel = item["x"].to(torch.float32)

        if mel_sum is None:
            mel_sum = torch.zeros(mel.shape[0], dtype=torch.float64)
            mel_sq_sum = torch.zeros(mel.shape[0], dtype=torch.float64)

        mel_sum += mel.sum(dim=1, dtype=torch.float64)
        mel_sq_sum += (mel ** 2).sum(dim=1, dtype=torch.float64)
        frame_count += mel.shape[1]

    mean = (mel_sum / frame_count).to(torch.float32)
    var = (mel_sq_sum / frame_count) - (mean.to(torch.float64) ** 2)
    std = torch.sqrt(var.clamp_min(1e-8)).to(torch.float32)

    stats = {
        "mean": mean,
        "std": std,
        "mels": MELS,
        "fft": FFT,
        "hop_length": HOP_LENGTH,
        "sample_rate": SR,
    }
    torch.save(stats, dataset_dir / "stats.pt")
    return stats

def generate_dataset(
    total_parameter_vectors: int,
    simultaneous_generators: int,
    note_increment: int = 7,
    dataset_dir: str = "Dataset/processed",
    train_ratio: float = 0.8,
    seed: int = 1234,
):
    dataset_root = Path(dataset_dir)
    dataset_root.mkdir(parents=True, exist_ok=True)
    (dataset_root / "examples").mkdir(parents=True, exist_ok=True)

    counts = split_generation_counts(total_parameter_vectors, simultaneous_generators)

    start_ids = []
    running = 0
    for count in counts:
        start_ids.append(running)
        running += count

    merged_params = {}
    all_records = []

    with ProcessPoolExecutor(max_workers=simultaneous_generators) as executor:
        futures = []
        for start_param_id, count in zip(start_ids, counts):
            if count == 0:
                continue
            futures.append(
                executor.submit(
                    _worker_generate_examples,
                    start_param_id,
                    count,
                    start_note,
                    num_of_notes,
                    note_increment,
                    str(dataset_root),
                )
            )

        for future in as_completed(futures):
            params_chunk, records_chunk = future.result()
            merged_params.update(params_chunk)
            all_records.extend(records_chunk)

    split_map = assign_train_test_splits(
        param_ids=sorted(merged_params.keys()),
        train_ratio=train_ratio,
        seed=seed,
    )

    for row in all_records:
        row["split"] = split_map[row["param_id"]]

    metadata = pd.DataFrame(all_records).sort_values(["param_id", "midi_note"]).reset_index(drop=True)

    torch.save(merged_params, dataset_root / "params.pt")
    metadata.to_csv(dataset_root / "metadata.csv", index=False)
    compute_train_stats(dataset_root, metadata)

    print(f"saved dataset to {dataset_root}")
    print(f"unique parameter vectors: {len(merged_params)}")
    print(f"total examples: {len(metadata)}")
    print(f"workers used: {simultaneous_generators}")

#%%
if __name__ == "__main__":
    generate_dataset(
        total_parameter_vectors=total_parameter_vectors,
        simultaneous_generators=simultaneous_generators,
        note_increment=note_increment,
        dataset_dir="Dataset/processed",
    )