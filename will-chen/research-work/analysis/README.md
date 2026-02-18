# Part 1: Song Selection

Song Title: 경, 敬, ɡjʌŋ  
Team: Rubato LAB  
Team Members: Junseop So, Jihyeon Park, Jongho Lee, Yonghee Kim, Hyunseo Seo, Changjun Yu  
Year: 2023  

Summary: This project shows how people today live in a state where rest and work are mixed together. Rubato LAB combined Eastern philosophy with Western ideas through music and visuals. They blended traditional Korean music with future bass, and produced a video using images of Korean culture. The project was created using both AI and human creativity, showing how AI can support and improve music and video production.

---

# Part 2: Technical Analysis

## ML Architecture

This project used a HITL ML architecture, where AI tools generated raw creative materials and humans made the main creative decisions and refinements. The main tools used were MusicGen for generating audio, music source separation for isolating instruments, and Stable Diffusion and RunwayML for creating images and videos. All of these models were pre-trained and were only used to generate content, without changing any settings or data. The inputs were text prompts and reference images, and the outputs were audio files, images, and video clips that were later edited by humans. These tools were chosen because of their accessibility, flexibility, and ability to support sampling based workflows instead of fully AI generated songs.

## Tool Ecosystem

This project used a mix of AI tools and professional media softwares, including MusicGen, AudioCraft Plus, Stable Diffusion, RunwayML, Midjourney, Adobe Premiere Pro, and After Effects. These tools were run on regular computers with GPU support, mostly using their default settings. Creative control mainly came from writing prompts and editing the results. The tools were connected through a file-based workflow, so the output from one tool was used as the input for another. Overall, the project relied on off-the-shelf solutions rather than custom coding.

## Data Pipeline

The data pipeline used AI generated audio, images, and videos, mainly in WAV and standard visual formats. Audio created by MusicGen was trimmed, edited, and processed to extract useful sounds using source separation. Visual content was refined through image-to-image tools and further edited in professional editing software. Instead of using technical feature controls, the team mainly adjusted the results through prompt writing. All of the work was done offline, which allowed time to carefully review and improve the results.

## Workflow & Process

The workflow followed four main phases: conceptualization, experimentation, refinement, and production. During experimentation, different AI tools and prompts were tested. In the refining stage, the best results were chosen and edited. The team decided to use AI generated audio as samples instead of full songs, and they avoided fully AI made videos because of quality issues. Humans were involved at every major step, including creating prompts, choosing samples, arranging the music, and making the final decisions.

### Workflow Diagram

![Workflow Diagram](Workflow_Diagram.png)

---

# Part 3: Musical Analysis

## Structure

This song follows a clear EDM style structure: Intro, Verse 1, Build-up 1, Drop 1, Breakdown, Drop 2, Verse 2, Build-up 2, Drop 3, and Outro. The intro sets the atmosphere with traditional Korean plucked instruments with syncopated percussive elements. Moving into Verse 1, the vocal comes in with long sustain melody lines. Each build-up increases tension with build-up drums and rising effects, leading into drops that feel rhythmically intense and emotionally charged. The breakdown creates contrast by pulling back the energy and including a different melodic vocal line before going into another drop. Throughout the entire track, the percussion and drums uses a lot of syncopation. Because AI was used primarily for sampling, the structural organization remained human directed. It’s the producers who arranged the fragment pieces of the music into a coherent structure.

## Musical Elements

Harmonically, this song blends pentatonic scales with wide and rythmic future bass chords. The AI generated samples and loops gave the team raw tonal material, and the team later layered and reshaped everything inside the DAW. Rhythmically, some patterns were likely started from AI generated loops, but they were chooped up and processed to match the future bass aesthetics, especially with the sycopated rhythm and heavy sidechain compression. Melodically, you can hear some moments where the phrases resolved in unexpected ways, which hints that AI was involved in the process. The mix of traditional instrumental timbres with thick synthesized future bass textures creates a unique blend between traditional Korean music and EDM music.

## AI Signatures

You can tell that AI played a role in the song in a few subtle ways. Some of the generated sounds feel slightly artificial that doesn’t match live recorded instruments. It’s because that the audio was generated at 32kHz, which can slightly reduce the clarity compared to professional studio recordings. A few melodic phrases also feel a bit unpredictable, which reflects how AI models sometimes struggle with long-term musical direction. But those small imperfections actually became part of the song’s identity. The AI made it possible to quickly generate musical ideas that would normally take much more time to record or design. But it still relied on human decisions to select and edit those ideas into a final polished track.

---

# Part 4: Music Critic

## Comparative Analysis

Compared to many other AI Song Contest entries, this project didn’t rely on fully automated song generation. Instead of letting AI compose the entire track from start to finish, the team used AI more like a sample generator and creative assistant. Some contest entries experiment with AI written lyrics, AI vocals, or end-to-end composition systems. But this project keeps humans fully in control of arrangement and final production decisions. The trade-off was definetly more manual work by the team, but it also allows for stronger artistic direction. In terms of scalability, this workflow is highly repeatable. The producers can generate all kinds of samples with prompts, but the final quality still depends heavily on the human taste, and that means it’s reproducible in the process but not identical in the outcome.

## Ethics and Aesthetics

The team used pre-trained models rather than building their own datasets. Since no additional dataset was collected specifically for this project, the ethical responsibility mainly depends on the transparency of the generative AI model training. In terms of ownership, the team said that because they select, edited, and rearranged AI outputs, they should hold creative authorship over the final product. But AI assisted art blurs the traditional ideas of authorship since the model still contributes to the materials even if it lacks intention. Lastly, generating high quality audio and video through AI models requires significant computational power which has a real energy cost that the artists and researchers should consider moving forward.

## Innovation Assessment

The most innovative aspect of this project is the way it reframes AI as a sampling engine for musicians and producers. By treating MusicGen outputs like MPC-style samples, the team turned technical limitations like the 32kHz audio quality into creative opportunities. Instead worrying about imperfect outputs, they used source separation, slicing, and layering to reshape the AI material into something new. This workaround shows a practical and realistic way of AI fitting into professional workflows without fully taking it over. Overall, this project contributes to the field by demonstrating a balanced workflow between human and AI. The AI expands the sonic possibilities and the humans maintain the artistic control.

---

# Bibliography

Rubato Lab. AI Song Contest 2023 – Participants: Rubato LAB. AI Song Contest, 2023, https://www.aisongcontest.com/participants-2023/rubato-lab. Accessed 13 Feb. 2026.

AI Song Contest Selection Spreadsheet. Google Sheets, https://docs.google.com/spreadsheets/d/1ZzV0MdhRn0Apb0k03j52OlbP8nxwo2t4IRmOd8nSa-o/edit?gid=227254321#gid=227254321. Accessed 13 Feb. 2026.