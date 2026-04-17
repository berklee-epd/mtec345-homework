import torch

#%% Config and constants
SR = 48000
seconds = 4
NUM_SAMPLES = int(SR*seconds)
wavetable_samples = 2**13
start_note = 21
num_of_notes = 12
note_increment = 7

PARAMS = ["i1ratio","i1index1","i1index2","i2index2","i2index1","i1out","i2out","iattack1","idecay1","isustaintime1","isustain1","irelease1","iattack2","idecay2","isustaintime2","isustain2","irelease2"]
stoi = {param: i for i, param in enumerate(PARAMS)}
itos = {i: name for i, name in enumerate(PARAMS)}

MELS = 128
FFT = 1024
HOP_LENGTH = FFT // 4

NUM_SAMPLES_TENSOR = torch.tensor([NUM_SAMPLES], dtype=torch.float32)
STFT_WINDOW = torch.hann_window(FFT)

wavetable = torch.sin(torch.linspace(0, 2*torch.pi, wavetable_samples))
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
def audio_to_log_mel_batch(
    audio: torch.Tensor
) -> torch.Tensor:
    audio = audio.float()

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
def adsr_envelope_batch(adstsr: torch.Tensor, num_samples: int=NUM_SAMPLES):
    """
    Compute ADSR envelopes for a batch of parameters.

    Args:
        adstsr: Tensor of shape [Batch, 5] where columns are [a, d, s_time, s_level, r]
        num_samples: Total number of samples in the envelope

    Returns:
        envelope: Tensor of shape [Batch, num_samples]
    """
    batch_size = adstsr.size(0)
    a, d, s_time, s_level, r = adstsr[:, 0], adstsr[:, 1], adstsr[:, 2], adstsr[:, 3], adstsr[:, 4]

    # Normalize ADSR segments to sum to 1 (softmax over time proportions)
    # We'll treat s_time as a fraction of sustain phase
    total = a + d + s_time + r
    a_frac = a / total
    d_frac = d / total
    s_frac = s_time / total
    r_frac = r / total


    # Fixed time grid
    t = torch.linspace(0, 1, num_samples, device=adstsr.device).unsqueeze(0)  # [1, num_samples]

    # Compute phase boundaries per batch
    attack_end = a_frac.unsqueeze(1)  # [Batch, 1]
    decay_end = attack_end + d_frac.unsqueeze(1)
    sustain_end = decay_end + s_frac.unsqueeze(1)

    # Attack: 0 -> 1 over attack_end
    attack = torch.where(
        t <= attack_end,
        t / attack_end.clamp(min=1e-5),  # avoid division by zero
        torch.zeros_like(t)
    )

    # Decay: 1 -> s_level over d_frac
    decay = torch.where(
        (t > attack_end) & (t <= decay_end),
        1.0 - (1.0 - s_level.unsqueeze(1)) * ((t - attack_end) / (d_frac.unsqueeze(1) + 1e-5)),
        torch.zeros_like(t)
    )

    # Sustain: s_level for s_frac
    sustain = torch.where(
        (t > decay_end) & (t <= sustain_end),
        s_level.unsqueeze(1),
        torch.zeros_like(t)
    )

    # Release: s_level -> 0 over r_frac
    release = torch.where(
        t > sustain_end,
        s_level.unsqueeze(1) * (1.0 - (t - sustain_end) / (r_frac.unsqueeze(1) + 1e-5)),
        torch.zeros_like(t)
    )

    # Combine all phases
    envelope = attack + decay + sustain + release

    return envelope  # [Batch, num_samples]

# Input: tensor of shape [B, 1]
# Output: tensor of shape [B, 1]
def linear_lookup(phases: torch.Tensor, wavetable: torch.Tensor = wavetable):
    wavetable = wavetable.to(device=phases.device)
    table_size = wavetable.shape[0] - 2
    index = phases * table_size
    i0 = torch.floor(index).long()
    i1 = i0 + 1
    frac = index - i0.to(index.dtype)
    return wavetable[i0] * (1.0 - frac) + wavetable[i1] * frac

def synthesize_k(parameters: torch.Tensor):
    k1 = adsr(parameters[:, 7:12])
    k2 = adsr(parameters[:, 12:17])
    return k1, k2
def synthesize_a_batch(
        parameters: torch.Tensor,   # [B, 17]
        adsr1: torch.Tensor,        # [B, num_samples]
        adsr2: torch.Tensor,        # [B, num_samples]
        f0s: torch.Tensor,
        sr: int = SR,
        num_samples: int = NUM_SAMPLES,
):
    batch_size = f0s.shape[0]

    ratio1 = parameters[:, 0] * 16
    base_freq1 = f0s * ratio1

    i2index1 = parameters[:, 4] * 14.5
    i1index2 = parameters[:, 2] * 14.5

    iout1 = parameters[:, 5].unsqueeze(1)
    iout2 = parameters[:, 6].unsqueeze(1)
    denom = (iout1 + iout2).clamp_min(1e-8)

    a1 = torch.zeros((batch_size, num_samples), dtype=torch.float32, device=parameters.device)
    a2 = torch.zeros_like(a1)
    phase1 = torch.zeros(batch_size, dtype=torch.float32, device=parameters.device)
    phase2 = torch.zeros_like(phase1)


    for sample in range(num_samples):
        if sample == 0:
            freq1 = base_freq1
            freq2 = f0s
        else:
            freq1 = base_freq1 * (1 + a2[:, sample - 1] * i2index1)
            freq2 = f0s * (1 + a1[:, sample - 1] * i1index2)

        a1[:, sample] = linear_lookup(phase1, wavetable) * adsr1[:, sample]
        a2[:, sample] = linear_lookup(phase2, wavetable) * adsr2[:, sample]

        phase1 = (phase1 + freq1 / float(sr)) % 1.0
        phase2 = (phase2 + freq2 / float(sr)) % 1.0

    return a1 * (iout1 / denom) + a2 * (iout2 / denom)