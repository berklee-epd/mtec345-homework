def main():
    import torch
    import wave
    from einops import rearrange
    from stable_audio_tools import get_pretrained_model
    from stable_audio_tools.inference.generation import generate_diffusion_cond

    device = "mps" if torch.mps.is_available() else "cpu"

    # Download model
    model, model_config = get_pretrained_model("stabilityai/stable-audio-open-1.0")
    sample_rate = model_config["sample_rate"]
    sample_size = model_config["sample_size"]

    model = model.to(device)

    # Set up text and timing conditioning
    conditioning = [{
        "prompt": "160 bpm breakbeat with metal pipe fall on cement, loud distorted clang with low pitch resonance, salt shaker hihat",
        "negative_prompt": "low quality",
        "seconds_start": 0,
        "seconds_total": 30
    }]

    # Generate stereo audio
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

    # Rearrange audio batch to a single sequence
    output = rearrange(output, "b d n -> d (b n)")

    # Peak normalize, clip, convert to int16, and save to file
    output = output.to(torch.float32).div(torch.max(torch.abs(output))).clamp(-1, 1).mul(32767).to(torch.int16).cpu()
    with wave.open("output.wav", "wb") as f:
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(sample_rate)
        f.writeframes(output.numpy().tobytes())


if __name__ == "__main__":
    main()
