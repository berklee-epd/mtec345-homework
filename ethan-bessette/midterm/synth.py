#%%
import torch
import math

#%%
def adsr(a: float, d: float, s_time: float, r: float, sustain_level: float, num_samples: int, sample_rate: int):
    adstr = torch.tensor([a,d,s_time,r])
    adstr = torch.softmax(adstr, dim=0)
    attack = torch.linspace(0.0,1.0, int(num_samples*adstr[0]))
    decay = torch.linspace(1.0, sustain_level, int(num_samples*adstr[1]))
    sustain = torch.linspace(sustain_level, sustain_level, int(num_samples*adstr[2]))

    parameters = [attack, decay, sustain]
    envelope = torch.concat(parameters, dim=0)
    release = torch.linspace(sustain_level, 0.0, num_samples-len(envelope))
    envelope = torch.concat([envelope, release], dim=0)

    return envelope

#%%
def linear_lookup(phase: float, wavetable: torch.Tensor):
    phase = float(phase) % 1.0

    extended = torch.cat([wavetable, wavetable[:1]], dim=0)
    table_size = wavetable.shape[0]

    index = phase * table_size
    i0 = int(math.floor(index))
    i1 = i0 + 1
    frac = index - i0

    return extended[i0] * (1.0 - frac) + extended[i1] * frac


#%%
def fm_bank(base_freq: int, ratio1: float, ratio2: float, i1index2: float, i2index1: float, iout1: float, iout2: float, adsr1: torch.Tensor, adsr2: torch.Tensor, wavetable: torch.Tensor, num_samples: int, sample_rate: int):
    a1 = torch.zeros((num_samples))
    a2 = torch.zeros((num_samples))
    phase1 = 0
    phase2 = 0

    for sample in range(num_samples):
        if sample == 0:
            freq1 = base_freq * ratio1
            freq2 = base_freq * ratio2
        else:
            freq1 = (base_freq * ratio1)*(1 + float(a2[sample-1]) * i2index1)
            freq2 = (base_freq * ratio2)*(1 + float(a1[sample-1]) * i1index2)

        if sample % 1000 == 0:
            print(freq1, freq2)

        a1[sample] = linear_lookup(phase1, wavetable)
        a1[sample] = a1[sample] * adsr1[sample]

        a2[sample] = linear_lookup(phase2, wavetable)
        a2[sample] = a2[sample] * adsr2[sample]

        phase1 = (phase1 + freq1 / float(sample_rate)) % 1.0
        phase2 = (phase2 + freq2 / float(sample_rate)) % 1.0

    aout = a1 * (iout1 / (iout1 + iout2)) + a2 * (iout2 / (iout1 + iout2))
    return aout