# Analysis

## Song Selection
- Song Title: Genre Cannon
- Artist / Team: Dadabots
- Year: 2024

**Brief Summary**  
Genre Cannon presents a narrative-driven audiovisual exploration of genre creation and fusion, using generative audio models capable of producing thousands of musical styles and unprecedented genre hybrids. The project treats genre itself as a compositional material, framing music generation as a journey through evolving stylistic worlds rather than a single fixed aesthetic.

Dadabots founders CJ Carr and Zack Zukowski studied at Berklee College of Music, where they developed interests in music production and audio technology. This educational background informs the group’s emphasis on experimental sound design and technology-driven composition.  
(Dadabots, 2024; Stability AI, 2024)

## Technical Analysis
Dadabots employ neural audio synthesis models that generate raw waveform audio rather than symbolic representations such as MIDI. These models learn timbral, spectral, and temporal patterns directly from large-scale audio datasets, prioritizing the capture of genre-level sound characteristics over note-level precision.

Genre Cannon primarily uses the open-source model Stable Audio Open for large-scale text-conditioned audio generation. In addition, Dadabots’ earlier work and aesthetic approach were strongly influenced by SampleRNN-based raw-audio systems, which established their practice of treating timbre and texture as primary compositional materials.

Raw-audio synthesis was chosen because traditional symbolic models struggle to represent distortion, noise, and complex hybrid textures that define many of the genres explored by Dadabots. This approach enables rapid iteration, large-scale stylistic experimentation, and a focus on timbre and texture as central compositional elements.  
(Dieleman et al., 2016; Stability AI, 2024; Dadabots, 2024)

## Input / Output Formats
- Input: Text prompts or conditioning data
- Output: Raw audio waveforms (WAV)
- Internal Representation: Continuous audio samples and learned latent embeddings

## Tool Ecosystem (Focused)
- Audio Models: Stable Audio Open (primary), SampleRNN (historical influence)
- DAW: Ableton Live  
  Ableton Live functions as the central production hub, integrating generated audio via sampling and arrangement.

## Custom Code vs. Off-the-Shelf
Dadabots combine custom-trained models with open-source frameworks. Stable Audio Open is publicly available, while additional internal models are customized for specific stylistic behaviors.  
(Dadabots, 2024)

## Data Pipeline
Source data consists primarily of large collections of audio recordings spanning a wide range of musical genres, which are used to train raw-audio neural networks. Dadabots’ training data emphasizes timbral diversity and extreme sound textures rather than symbolic representations such as MIDI.

Preprocessing includes normalization, segmentation, and format standardization. Detailed feature design is learned implicitly by the models through exposure to the audio corpus rather than manual feature extraction. Model training is performed offline, while inference operates in near-real-time for generation.

## Workflow & Process
**Core Steps**
- Concept development (animation narrative)
- Model training and testing
- Audio generation
- Sampling and arrangement in Ableton
- Visual world-building
- Final synchronization

Project concepts are first defined in terms of an audiovisual or narrative goal. Dadabots then train or select raw-audio generative models and generate large batches of audio outputs. Human creators curate, sample, and arrange selected material within Ableton Live, shaping the musical form and pacing. In parallel, visual environments are developed to match the evolving sonic worlds, followed by final synchronization of audio and visuals. Human intervention remains central at the stages of concept design, model selection, curation, and final arrangement.

## Workflow Diagram Descriptions
- **Short:** Human Concept → Dataset → Model Training → Audio Generation → Sampling in Ableton → Arrangement → Visual Sync → Final Output
- **Revised:** Concept / Narrative Idea → Audio Dataset → Model Training or Selection → Audio Generation → Human Curation & Sampling (Ableton Live) → Musical Arrangement → Visual World-Building → Audiovisual Synchronization → Final Output

## References (APA)
- Agostinelli, A., et al. (2023). MusicLM: Generating Music From Text. https://arxiv.org/abs/2301.11325
- Dadabots. (2024). About Dadabots. https://dadabots.com/about
- Dieleman, S., et al. (2016). WaveNet: A Generative Model for Raw Audio. https://arxiv.org/abs/1609.03499