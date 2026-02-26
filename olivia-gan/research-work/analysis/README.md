## Part 1: Song Selection

Title: SOLARIUM <br>
Artist TEAM: KicKRaTT & KaOzBrD <br>

[Link To Website](https://www.aisongcontest.com/participants-2025/kickratt-and-kaozbrd)

Brief Summary:<br> 

SOLARIUM is a composition of midi score predictions made by LLMs trained on in-house developed synthetic datasets. SOLARIUM is composed of three predicted MIDI score celebrating genre music from the progressive rock of Canada, the acid house of USA, to the kosmische of Germany, and performed in the four-minute frame. 



## Part 2: Technical Analysis

### ML Architecture

They used GPT (Generative Pre-trained Transformer) and LSTM (Long Short-Term Memory) models. GPT is good at learning long patterns, and LSTM is good at remembering sequences like melodies. <br>

Instead of downloading data from the internet, they made their own MIDI files using: 
<br> 1. Algorithmic generators 
<br> 2. A hardware instrument called XOXBOX (a Roland TB-303 clone)
<br> 3. A Moog 960 sequencer<br>

The models were trained with their custom MIDI data, and the outputs were also in MIDI format. 

### Tool Ecosystem

They used a mix of hardware tools (like MIDI sequencers) and oftware tools (like Pure Data and a DAW). Though version numbers aren’t listed, they mentioned using Pure Data (Pd) for algorithmic music generation; a custom-built learning workstation for training models; and a DAW to arrange and polish the song.

### Data Pipeline

They only worked with MIDI data and no audio or soundwave data. They focused on predicting musical patterns like melody, chord & drum MIDI variations. From the many MIDI measures predicted by the LLMs only fifty measures were ultimately used and recursively arranged in the DAW to produce a tryptic of grooves targeting genre specific music. Using a fixed octave keyboard zone configuration, vocals were assigned to specific notes. Which corralled the singer into the predicted outcomes for a more complete song idea.

### Workflow & Process

- Decided the song would be 100% made from AI-predicted MIDI files
- Made their own MIDI sequences/data using tools like Pure Data, XOXBOX, and Moog 960
- Trained GPT and LSTM models with their data
- AI created many short musical parts
- Selected 50 best parts
- Arranged everything into a DAW
- Mix and mastered the final song


## Part 3: Musical Analysis

### Structure

Overall, this song does not follow a traditional song structure like verse–pre-chorus–chorus. Instead, it’s organized into three movements: the first and third are in A major, while the second shifts briefly to G major. Although the team provided lyrics on the contest website, they aren’t especially useful. The vocals are very sparse, not central to the arrangement, and the words appear to be repeated samples rather than fully written lyrics.

### Musical Elements

The first section centers on bass, electric guitar, and light cymbal accents, and garage-style drums, with minimal melodic changes. The second section adds variation and more space, featuring vocoder processing and layered vocal harmonies that create a more rich texture. The final section relies on repetitive guitar and vocal patterns, supported by lush pads and concluding with strings, giving the piece a more atmospheric and resolved ending.

### AI Signatures

The AI influence in is most obvious in its repetition, rigid phrase structure, and harmonically static traits. Some transitions between sections feel abrupt or overly mechanical. There is no feeling of performance in this song, e.g. velocity changes. The drum pattern is odd especially the hihats. 

## Part 4: Music Critic

### Comparative Analysis

Compared to other AI Song Contest entries that often rely on pre-trained models or vocal synthesis tools, SOLARIUM stands out for its use of fully custom-generated MIDI training data and that they purposely avoided publicly available datasets. This gives the creators more control over the music but makes the process slower and harder to scale. But this allowed the creators to tightly control both the training input and model outputs.

### Ethics and Aesthetics

SOLARIUM avoids copyright issues by using entirely self-generated MIDI data. Since the models were trained on original content and the final arrangement was human-curated, creative ownership clearly remains with the develop team and the artist. The environmental impact is likely minimal compared to large-scale AI projects, as training was done locally on a small workstation with relatively lightweight models.

(highly experimental and falls outside my area of musical expertise. While I can appreciate the creative intent, the repetition makes it difficult to stay engaged. It lacks the melodic or emotional elements I typically connect with, making it less appealing to me personally.)

### Innovation Assessment

The song introduces an approach by training AI models on fully synthetic, self-generated MIDI data and not on common reliance on public datasets. To work around limitations in AI musicality, the team manually selected and arranged only the most compelling outputs. This hybrid method of custom data and human curation maybe pushing AI music aesthetics beyond generic generation. 
