# Research Work Phase 1: AI Song Contest Analysis

## Song Selection
| Title | Artist | Year |
| --- | --- | --- |
| MF U UP | DADABOTS | 2025 |

DADABOTS are a duo of musicians and AI researchers who met at Berklee College of Music in 2012. They co-founded Harmonai, the music research team at StabilityAI, and there created Stable Audio [1].

This submission is a genre bending piece with lots of energy that repeats the phrase MF U UP. DADABOTS primarily used their own Stable Audio that they continually re-trained to achieve the sound they were aiming for [2].

## Technical Analysis

### ML Architecture

    Models used (architecture, parameters, training data)
    Why these models were chosen
    Input/output formats and data representations
    Training vs. inference pipeline
    
| Model | Architecture | Parameters | Training Data | Input Format | Output Format |
| --- | --- | --- | --- | --- | --- |
| Custom Stable Audio 2.5 [5] | Diffusion-transformer | Variable: 0.34B - 1.06B [5] | Variable: Audio with CC0, CC-BY, or CC-Sampling+ licenses; Free Music Archive Music; custom audio [2,5] | Audio and Text | Audio |
| Gemma3-27b [6] | Transformer | 27B | Source unknown; 14T tokens encompassing image, text, mono and multilingual text | Text | Text |
| I AM CHOIR [4] | Unknown | Unknown | Audio recordings of gospel choir, children's choir, and gang vocals | Audio | Audio |


The team primarily used Stable Audio, the model they continue to improve through their research at Stability AI [1,2], which was likely their reason for choosing the model. It is capable of audio-to-audio; in their recent paper, they informally experimented with its style and timbre transfer abilities [5]. It is also capable of text-to-audio [3].

The team likely used Gemma because it is relatively lightweight and is open sourced.
    
### Tool Ecosystem

    Software and hardware used
    Version numbers and configurations (if available)
    Integration between tools
    Custom code vs. off-the-shelf solutions

There is no information on which machines and operating systems the team used. However, they used the off-the-shelf solution I AM CHOIR [2], which only runs on macOS with Apple Silicon (M1 and later) [4], making it likely they used macOS with a Silicon chip.

All the models they used ran on their local machines [2].

As noted, they used their own diffusion-transformer model Stable Audio. They likely started with the latest version, 2.5, released in May of 2025. This is likely because this version was release prior to the AI Song Contest deadline of August 2025.

They also used a customized off-the-shelf solution, I AM CHOIR to shape the vocals [2]. The model was trained on a gospel choir, children's choir, and gang vocals [4].

They used an open sourced LLM (Gemma3-27b).

The tools were kept separate; human interaction piped data across models, as explained in the Workflow section.

### Data Pipeline

    Source data types and formats
    Preprocessing and transformations
    Feature engineering decisions
    Real-time vs. offline processing
    
    
| Model | Architecture | Parameters | Purpose | Input Format | Output Format |
| --- | --- | --- | --- | --- | --- |
| Customized Stable Audio | Autoencoder | 156M | "compresses waveforms into a manageable sequence length", creating a latent space in which the diffusion-transformer works. It then decodes and upsamples the audio at the end of the process. [3] | Audio | Audio |
|| T5-based text embedding | 109M | provides text conditioning to the diffuser-transformer so that text prompts can effect the audio output. [3] | Text | Unknown |
|| Diffusion-transformer | Variable: 0.34B - 1.06B [3,5]| using training data and text input, generate audio | Unknown | Audio |

The two papers cited explain the process much more in depth. They also have experimental setup and procedures for reproducing.
    
    
### Workflow & Process

    Project phases (conceptualization, experimentation, refinement, production)
    Key decision points and alternatives considered
    Where and why humans intervened
    Include a workflow diagram showing data flow, transformations, and human decision points (use draw.io, Lucidchart, or similar)
    
They recorded vocals, then used stable audio to generate short samples of the backing track around them. They handpicked ones they liked and used stable audio to refine the assembled piece. They used I AM CHOIR to process the vocals. They used a locally run LLM (Gemma3-27b) to extend the lyrics and for help with prompting Stable Audio. They used inpainting with Stable Audio to change certain sections of the song without changing the whole song [2]. Finally, they used a human producer, Encanti, to master the track [2]. This project was a combination of coding, training, prompting, adjusting, and finally human taste through using a producer to shape the final sound.

![Flowchart](Figure.png)

The workflow was a creative process shared between human and AI. There are a number of processes that were ongoing over the course of the project, as shown in the Figure.
- A1 <=> A2: DADABOTS picked the main lyrical theme and motif, then used Gemma to extend lyrics [2].
- A1 -> D1: DADABOTS recorded the lyrics into the DAW.
- B1 <=> B2: DADABOTS also used Gemma to improve the prompts they used for generating audio with Stable Audio across iterations [2].
- B1 | B2 -> B3: text prompts are used to generate audio in Stable Audio.
- B3 - B1: the audio generated in Stable Audio is considered, handpicked, and sparks the generation of new prompts to improve the audio. Chosen audio is arranged into the track.
- C1 <=> C2: DADABOTS used a LoRa (low-rank adaptation) of Stable Audio to train the model on two genres: one of DADABOTS' member's teenage mathcore, and trap. This enabled the model to learn these styles without significant processing and retraining of the entire model. Additionally, DADABOTS applied timbre transfer effects by using custom audio for the initial noisy sample xτi during ping-pong sampling [2,5]. They may also have refined the beat of the song by initializing xτi with a recording having a strong beat [5].
- D1 <=> D2: DADABOTS used a model called I AM CHOIR to apply timbre transfer effects to their vocals.


## Musical Analysis

Structure, Musical Elements, AI Signature

    Form and sections (verse, chorus, bridge, etc.)
    Temporal organization and phrasing
    How structure relates to the AI generation method
    Harmonic progressions and AI's role in them
    Rhythmic patterns and how they were generated
    Melodic contours and pitch selection
    Timbral characteristics
    Elements that reveal AI involvement
    Uncanny valley effects (if any)
    Strengths unique to the AI approach
    Limitations compared to traditional production
    
### Form
Intro - chorus - verse - chorus - verse - buildup - climax - chorus - outro

When transitioning between sections, the piece often features sound design and ear candy elements that were likely generated using Stable Audio and arranged and fit into place by the human artists and producer Encanti.
    
#### Intro
Soft intro featuring lead vocals on the main lyrical motif, backed by synth piano textures and a building glitch/pulse on quarter notes.

The intro transitions into the next section with a processed vocal/synth run and an angry scream before the beat drops into a new tonal center.

#### Chorus
Hard-style with pulsing, heavily distorted/noisy bass, with the lyrical motif repeating on top in a robotic grating tone.

- the tone was achieved by processing the vocals using I AM CHOIR
- The noisy signal is likely due to generation using 

#### Verse
The verse features a call and response between the vocals mentioning various objects and concepts, and distorted drums and bass. 

#### Buildup / Bridge
Features the same building glitch/pulse on quarter notes as the intro. It also includes a synth-like melody the changes between two notes. At the end of the section, it features a very simple, high blatty synth melody that arpeggiates a chord that is not the tonal center, before a female-sounding voice says dance and the piece drops into the climax.
- the simple synth melodic elements that don't nexearily match the key of the song show AI involvement
- however, this does fit the style/genre of the song

#### Climax
A melodic bass line changes between solfège notes re, ti, and do along with a heavy beat with snare on 3. It also has a siren-like sound in the background.

#### Outro
Features a new genre that DADBOTS named "twinkle trap". As mentioned above, they used a LoRa (low-rank adaptation) of Stable Audio to train the model on two genres: one of DADABOTS' member's teenage mathcore, and trap. This enabled the model to learn these styles without significant processing and retraining of the entire model. It is very melodic and features pleasant harmonies, in contrast with the rest of the piece.

### AI Signature
Overall, the main AI signature is the somewhat noisy sound, though it fits the style as it sounds like distortion in the context of the piece. Additionally, the piece is heavily form focused: each section is separated by feel and beat change-up. This is an element of the main style of the piece, but it also speaks to AI's limited memory and ability to generate full songs with contrasting sections without human intervention.

## Music Critic

### Comparative Analysis

    How does this approach differ from other AI Song Contest entries?
    Trade-offs between automation and control
    Scalability and reproducibility
    
Without going into too much detail, this entry differs from many of the other entries because its creators are on the engineering team of the main tool they used. They had access to past research, models, training data, etc, at their company.

It uses human taste and a final human producer to shape the overall sound of the piece. Some entries used machine learning mastering tools. This is an example of the trade-off between automation and control. Other examples include using handpicked snippets of the audio generated by Stable Audio.

Overall, I think this method of production is a great balance between creative coding and composition/production. The team was able to take an original lyrical motif and shape the generation of audio around their vocals in a way that sounds good while still contributing to the field of machine learning.


### Ethics and Aesthetics

    Training data sources and copyright considerations
    Attribution and creative ownership
    Environmental impact of computation
    
For Stable Audio, the team only used audio with Creative Commons and open sourced licenses, as well as their own audio. 

For the I AM CHOIR model, the choirs are credited and images are available for viewing on the website [4].

For the LLM, Gemma3, I could not find the source of the training data in the technical report [6].

In terms of environmental impact, the models were trained and run locally, with the exception possibly of Gemma3. The team only used the model and did no training of the LLM. It is possible that there was a more significant environmental impact of the trading of that model.

### Innovation Assessment

    Novel techniques or applications
    Workarounds for limitations
    Contribution to the field
    
    
None of the techniques were novel; however, the experimentation of creating this piece aligns with the time Stability AI released a new version of Stable Audio, along with a research paper [5]. They were able to reduce the number of parameters in the diffusion-transform portion of the model to improve inference-time efficiency while maintaining genre variance and sound quality [5]. According to the paper, this represents a significant innovation over other audio generation models [5].

One of the limitations of the Stable Audio model is that it wasn't originally created as a timbre-transfer model. The team was able to program a creative workaround, as mentioned above, by using custom audio custom audio for the initial noisy sample xτi during ping-pong sampling [5].

## Bibliography

[1]
“DADABOTS,” AI for Good, Jun. 05, 2025. https://aiforgood.itu.int/speaker/dadabots/ (accessed Feb. 05, 2026).

[2]
DADABOTS, “AI Song Contest,” AI Song Contest, 2025. https://www.aisongcontest.com/participants-2025/dadabots (accessed Feb. 05, 2026).

[3]
Z. Evans, J. D. Parker, C. Carr, Z. Zukowski, J. Taylor, and J. Pons, “Stable Audio Open,” arXiv.org, 2024. https://arxiv.org/abs/2407.14358 (accessed Feb. 05, 2026).

[4]
“I AM AUDIO,” Amiaudio.io, 2026. https://amiaudio.io/ (accessed Feb. 05, 2026).

[5]
Z. Novack et al., “Fast Text-to-Audio Generation with Adversarial Post-Training,” arXiv.org, 2025. https://arxiv.org/abs/2505.08175 (accessed Feb. 05, 2026).

[6]
G. Team and G. Deepmind, “Gemma 3 Technical Report,” Mar. 2025. Available: https://storage.googleapis.com/deepmind-media/gemma/Gemma3Report.pdf
