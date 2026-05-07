# RAVE-inspired Variational Autoencoder

I designed a downsized implementation of a RAVE-inspired variational autoencoder.
The test.ipynb demonstrates the core components in a simplified form. It will be expanded in the future!!!



##Structure
1. Setup fro python environment and synthetic audio input.
2. PQMF analysis/synthesis filterbank
3. Dilated residual and downsample/upsample blocks
4. Encoder and decoder definitions
5. End-to-end waveform reconstruction test
6. Loss function definition for VAE training and a number to define how effective of the lossfunction (beta).

## What is missing compared to full RAVE
- No discriminator or adversarial loss
- No GAN-style training or feature matching
- No waveform-domain refinement after PQMF synthesis
- No dataset loader, training loop, or audio checkpointing
- No pitch/style conditioning or codebook quantization

## Lessons learned from RAVE
- Sub-band modeling with PQMF is effective for audio compression and generation.
- Dilated residual blocks expand receptive field while keeping the network compact.
- Spectral losses are often better than raw waveform losses for audio reconstruction.
- A simplified VAE can capture the high-level structure of RAVE's architecture.
- I didn't include it in the model but a noise synthsis is a brilliant idea to incorporate in the future.

## Challenges
- Understanding the PQMF filter design and how sub-band decomposition works.
- Understand the preprocessing framework and develope a general idea of how to improve the pipeline in the future.
- Understanding the dilated residual block structure and why residual connections help audio modeling.
- Understanding the STFT-based spectral loss and how it compares to waveform loss.

## Unfinished work
- Train the model on real audio data.
- Build a full data pipeline with loading, batching, and checkpointing.
- Add evaluation metrics for reconstructed audio quality.

## Future expansion
- add a real audio dataset loader and training loop
- implement adversarial training for better perceptual audio quality
- add waveform-domain refinement after PQMF synthesis
- evaluate reconstruction quality with real audio data
- explore pitch conditioning, style control, or codebook quantization for more expressive audio synthesis
