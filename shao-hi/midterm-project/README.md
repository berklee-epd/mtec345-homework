# RAVE Custom Model — Project Documentation



---

## What I Built

For this project I trained a custom neural audio synthesis model on my own collection of one-shots — claps, snares, hi-hats, rims, kicks, and other percussive sounds I've collected. The goal was to turn that personal sound library into a generative instrument, something that could produce new drum sounds that carry the timbral DNA of my own samples, but aren't any specific one of them.

Then a trained RAVE model exported as a TorchScript file, loaded into Max/MSP via the `nn~`. In Max, the model runs in real time — triggered by a metro object, also I uses the encode/decode pipeline with sliders to manipulate individual latent dimensions, which allows real-time timbral morphing between sounds in the dataset.

---

## The Dataset

### Collecting and Sorting the Samples

The dataset started much larger and messy than what ended up being used for training. My initial collection included mix of one-shots, loops, FX sounds, and longer sustaining samples pulled from all sources I've built up as a producer over the years.

The first major problem was timbral imbalance. A large portion of my collection was loops — not one-shots — and many of them shared a similar timbre. Having too much of one sound character in the dataset would bias the model toward that timbre and make the latent space less interesting to explore. I had to go through the collection manually and filter those out.

The second problem was sample type. RAVE is designed for short percussive audio. Samples with long sustains — FX hits, reverb tails, textural sounds — don't work well because RAVE's chunk-based preprocessing slices audio into fixed-length segments. A long sustaining sound creates chunks that are mostly decay or silence rather than transient content, which gives the model nothing useful to learn from. I filtered all of these out and kept only true one-shots with clear transients.

After filtering, I also had a solid foundation from the Roland TR-808 drum machine. These made up a significant portion of my final dataset because they are clean, well-characterized one-shots with consistent recording quality. Combining them with my personal sounds gave the model both a reliable sonic foundation and the personal character I wanted.

Most of the time I spent on this project was in this sorting phase — listening through samples, categorizing them, and making judgment calls about what fit the dataset's identity. This is unglamorous work but it directly determines what the model learns. A poorly curated dataset produces a poorly characterized model regardless of how long you train it.

### Converting the Audio

Once the dataset was sorted, every file needed to be standardized to mono, 44.1kHz, and -23 LUFS. I initially built a cell in Google Colab to handle this using FFmpeg:

```bash
ffmpeg -i input.wav -ac 1 -ar 44100 -af loudnorm=I=-23:TP=-1:LRA=11 output.wav
```

The problem was that every time I reconnected a Colab session, the cell would rerun the entire conversion process from scratch — re-downloading every file from Google Drive, processing it, and re-uploading it. Google Drive's bandwidth within Colab is limited, and with a large collection of files this became extremely slow and impractical.

I switched to processing the audio locally instead. Running FFmpeg locally was significantly faster since there was no network overhead, and I only had to do the conversion once before uploading the final processed files to Drive. This saved a significant amount of time and was the right decision.

---

## How Machine Learning Is Involved

**Colab session**
https://colab.research.google.com/drive/10skxqjZcSClpmxpv1XTcMoN4_ZhOLhQp?usp=sharing

### RAVE — The Model Architecture

RAVE (Realtime Audio Variational autoEncoder) is a deep learning architecture developed at IRCAM by Antoine Caillon and Philippe Esling. It is a variational autoencoder, meaning it has two main components:

- **Encoder** — compresses raw audio into a compact latent representation
- **Decoder** — reconstructs audio from that latent representation

The encoder and decoder are trained together with a discriminator — a separate neural network that judges whether the output sounds realistic. This setup pushes the decoder to produce convincing audio rather than just a blurry average of the training data.

### What "Variational" Means

The variational part means the model doesn't just learn a single compressed representation of each sound — it learns a probability distribution over possible representations. This is what makes generation possible. During inference you can sample a random point from this learned distribution and the decoder will produce a sound that belongs to the same timbral space as the training data, without copying any specific sample.

Think of it like this: the model learns the shape of what a drum sound is in your specific collection, and then you can ask it to generate anything within that shape.


### Training Infrastructure

Training was done on Google Colab Pro using an A100 GPU. The training pipeline was:

1. **Preprocess** — chunk audio into fixed-length segments and store in LMDB format
2. **Train** — run the adversarial training loop for thousands of epochs
3. **Export** — serialize the trained model as a TorchScript `.ts` file with streaming mode enabled
4. **Deploy** — load into Max/MSP using the `nn~` external

The training ran for approximately 9,000+ epochs with batch size 32 and validation every 200 epochs. Each checkpoint was saved to Google Drive so training could be resumed across multiple Colab sessions.

### nn~ — The Bridge to Max

`nn~` is a Max/MSP external developed at IRCAM that acts as a bridge between Max patches and PyTorch models. It loads a TorchScript file and exposes the model's methods — `forward`, `encode`, `decode` — as Max objects. The `--streaming` flag during export is critical — it reconfigures the model's convolutions to operate causally in real time, which is required for low-latency audio generation in Max.

---

## What I Learned

### Neural Audio Synthesis vs. Sample Playback

Before this project, my approach to drum sounds was entirely sample-based — you pick a sound, you place it. What RAVE introduces is something fundamentally different: a model that has internalized the latent structure of a sound collection and can generate new instances that sit within that learned space. This changes the creative relationship with sound from selection to exploration.

### The Latent Space

I learned what a latent space more in practice, not just in theory. The encoder maps audio into a 16-dimensional space. Each dimension captures some aspect of the timbral variation in the dataset. When you scale one dimension using a `*~` object in Max and route it through the decoder, we can directly manipulating one axis of that learned space — effectively morphing the sound along a direction the model discovered on its own from the data.

### Data Quality Matters More Than Data Quantity

I was thinking I needed thousands of samples first to get a good model. What I found is that data quality and consistency matter more at this scale. A small, well-curated dataset of sounds that share a stylistic identity gives the model a clearer target than a large diverse dataset would. The model isn't trying to generalize to all drums — it's trying to learn the specific timbral language of my collection. The sorting and filtering work was not just preparation — it was arguably the most important part of the entire project.

### Local vs. Cloud Processing

I learned that not everything should be done in the cloud. For tasks that are heavy on file I/O — like batch audio conversion — local processing is faster and more reliable than doing it inside Colab where Google Drive bandwidth is a bottleneck. The general principle is: use the cloud for GPU-heavy computation like training, and use local resources for everything that involves moving a lot of files around.

### Version Control for Training State

ML training pipelines need some extra care. Because RAVE's preprocessing creates a persistent database, and because Google Drive caches aggressively, I repeatedly ran into situations where I thought I was training on fresh data but was actually loading a corrupted partial dataset from a previous interrupted run. The fix was simple — always verify the training example count before letting training run — but it took several failed sessions to understand the root cause.

---

## Reflection

### Challenges

**Dataset curation** was the most time-consuming part of the project. Filtering loops, removing FX and long-sustain samples, balancing timbral variety, and identifying which sounds actually belonged in the dataset took more time than any technical step. This was unexpected — I assumed the coding and training setup would be the hard part.

**The audio conversion pipeline** was an early mistake. Running batch FFmpeg conversion inside Colab was too slow. Switching to local processing solved it immediately, but I lost time before making that decision.

**The preprocessing corruption loop** was the biggest recurring technical problem. Google Colab disconnects frequently, and each disconnect risked corrupting the preprocessed LMDB database. I ended up in multiple cycles of thinking training was running correctly, only to discover the dataset was using stale partial data. The solution was to always delete the preprocessed folder from Google Drive's UI and verify the example count before starting training.

**Dependency version conflicts** — a `pkg_resources` error caused by incompatible versions of `setuptools`, `pytorch-lightning`, and `acids-rave` — broke the training pipeline repeatedly across sessions. The fix was pinning `setuptools==65.5.0`, but finding it required systematic debugging.

**The runs folder nesting issue** — RAVE was saving checkpoints to a double-nested `runs/runs/` path instead of `runs/`, which made it appear that no checkpoints were being saved. This was caused by the training command being launched from inside the `runs/` directory due to a `%cd` command in the notebook.

### What I Would Do Differently

- **Process audio locally from the start.** Don't try to do batch file conversion inside Colab. Set up the local FFmpeg pipeline first, convert everything once, then upload the clean dataset.

- **Spend more time on dataset curation upfront.** I would be even more selective about sample type and timbral variety. The quality of the model is a direct reflection of the quality of the dataset.

- **Add more audio by concatenating one-shots.** 474 training examples is on the low end. I would concatenate all one-shots into longer files with short silences between them to increase dataset length, which would give the model more context to learn from.

- **Use a clean, version-controlled notebook from the start.** The notebook evolved chaotically through many debugging sessions. Starting with a well-structured notebook with explicit variable checks and a clear cell order would have saved significant time.

- **Monitor TensorBoard during training.** I didn't use TensorBoard during most of the training, which meant I had no visibility into whether losses were converging correctly. Monitoring spectral distance and discriminator losses would have given me early signal about model health.

- **Export at multiple checkpoints.** Rather than waiting, I would export at epoch 500, 2000, 5000, and 10000 to hear how the sound quality evolves over training. This would also make for a more interesting demonstration of the learning process.

### Results vs. Expectations

I expected the model to sound more like my original samples than it does. In reality, the output at around 9,000 epochs on a small dataset sounds like a blurry, noisy version of drums — recognizably percussive but not clean. This is consistent with what the RAVE documentation describes: the model requires significantly more training steps and larger datasets to produce high-quality reconstructions.

What surprised me is how musically interesting the imperfect output is. The noise and blurring create textures that don't exist in the original dataset — lo-fi, degraded, haunted-sounding drum hits that have a character I wouldn't have designed intentionally. In some ways the limited training produced a more interesting instrument than a fully converged model would have.

Compared to a non-ML approach — just playing samples directly — this system trades sonic precision for generative unpredictability. Every bang produces something slightly different. The latent space sliders introduce timbral control that has no equivalent in traditional sample playback. That tradeoff feels musically valuable, especially as a performance instrument.

---

## Technical Summary

| Component | Detail |
|---|---|
| Model | RAVE v2 + Wasserstein regularization |
| Dataset | Personal drum one-shots + TR-808 samples |
| Training examples | 474 chunks (~24 min audio) |
| Training duration | ~9,000+ epochs |
| GPU | A100 (Google Colab Pro) |
| Batch size | 32 |
| Val every | 200 epochs |
| Export format | TorchScript `.ts` (streaming mode) |
| Deployment | Max/MSP via nn~ external |
| Latent dimensions | 16 |
| Sample rate | 44.1kHz mono |
| Normalization | -23 LUFS |

---

## References

- Caillon, A. & Esling, P. (2021). RAVE: A variational autoencoder for fast and high-quality neural audio synthesis. *arXiv preprint arXiv:2111.05011*
- acids-ircam/RAVE — https://github.com/acids-ircam/RAVE
- acids-ircam/nn_tilde — https://github.com/acids-ircam/nn_tilde
- IRCAM Forum Tutorial: Neural Synthesis in Max 8 with RAVE — https://forum.ircam.fr/article/detail/tutorial-neural-synthesis-in-max-8-with-rave/
