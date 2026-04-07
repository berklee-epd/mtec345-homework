# MTEC-345 Midterm Project

## What I Did

I produced a cinematic electronic track using Generative AI and music production tools with AI features. I also discovered a workflow that I think is effective for modern producers to improve their music making process using these tools.

[Listen](https://drive.google.com/file/d/1SswU-XPkhDzluWhlsDY3PCNEQAIrijOp/view?usp=sharing)

---

## How Machine Learning is Involved

The main machine learning tools used in this project were Suno and Splice for generating ideas and samples. I used text prompts in Suno to outline the basic mood and structure of the song. In Splice, I used AI-powered features like “Create” mode and “Stacks” to match musical elements to the main idea. The combined demo was then fed back into Suno for further refinement.

I also tested several stem separation tools, including Logic, Moises, and iZotope RX. After comparing them, I chose iZotope RX because it provided the best quality for extracting instrumental tracks like drums and bass. These loops were trimmed and edited into one-shots in Pro Tools, then mapped into samplers such as Serum and Logic Sampler to create playable MIDI instruments. Other sound effects were kept as audio and processed into mix-ready samples. All stems were later mixed in Pro Tools.

For mastering, I tested Logic Master Assistant, Moises, Ozone 12, and Emastered. I ultimately chose Ozone 12 since you can directly control the individual plugins in the mastering chain.

---

### Stem Separation Tool Comparison

| Category | Logic | Moises | RX |
|----------|------|--------|----|
| **Speed and Ease of Use** | Very easy. Import -> Functions -> Stem Splitter -> Choose what do you want to split. Around 10 seconds | Easy to use but requires more steps. Add -> Files Select (Navigating in your computer) -> Open -> Choose what do you want to split. Around 2 minutes | Very easy. Import -> Music Rebalance -> Choose what do you want to split. Around 1 to 2 minutes depending on the quality you chose to split the stems |
| **Accuracy of the Split** | Some pumping effects due to effects applied on the instruments. Some tone changes when the arrangement gets bigger. Random high frequency noises would appear | Pumping effects due to effects applied on the instruments. Constant tone changes when the arrangement changes. Constant white/pink noises | Cleanest. Just a bit of pumping effects due to effects applied on the instruments. Sometimes would include random noises |
| **Handling of Effects** | Effects stay with the stem. Some pumping and abrupt cuts | Effects stay with the stem very well | Effects stay with the stem. Effects tone may change sometimes |
| **Splitting Options** | Vocals, Drums, Bass, Other | Vocals (1 track with vocals, 2 tracks with lead and background vocals), Guitar (1 track with guitars, 2 tracks with acoustic and electric guitar, 2 tracks with lead and rhythm guitar), Bass, Drums (1 track with drums, 6 tracks with kick, snare, toms, hi-hat, cymbals, and other drums), Piano, Keys, Wind, Strings, Dialogue, Soundtrack, Effects | Vocal, Bass, Drums, Other |
| **Other Observations** | Fast and easy to use. Balance performance on all the stems | Cannot just drag the file into the app. Only mute, no solos. Shows lyrics, bpm, key, bars, rests, and chords. You can transpose the keys. Cleanest on effects but the stem splitting is not really clean | You can choose the quality of the stem splitter. The cleanest on instruments especially bass |

---

### Mastering Tool Comparison

| Category | Moises | Logic Master Assistant | Ozone 12 | Emastered |
|----------|--------|----------------------|----------|-----------|
| **Speed** | 1 minute 30 seconds | 10 seconds | 15 seconds | 1 minute |
| **Degree of Control** | In the Auto Mode, you can select different Target Loudness for all kinds of streaming platforms (very useful). In the Advanced Mode, you can tweak the Target Loudness, Ceiling, Mastering Intensity, Low Cut Frequency, and High Cut Frequency (not very useful because it’s too broad and gives too less control). Reference Track (nice feature to have) | Character (Clean, Valve, Punch, Transparent). Auto EQ with mix percentage. Custom EQ (pretty useful, it would be better to include dynamic EQ). Dynamic section with LUFS meter, TP meter, and LU Range (very useful to check the dynamic range). Stereo spread section with Correlation (pretty useful). Loudness compensation (nice feature to check the changes made by the plugin) | All kinds of targets to choose (Very useful because you can analyze other songs and save them as your custom target). In the One Click Mode, you can control the Dynamic, Width, Clarity, and Stabilizer amount (pretty useful to do a fast master). When you change to Custom Mode, you get access to all of the Ozone plugins (very useful and detailed tweaking) | Mastering Intensity (not useful because it will affect all of the changes). Compressor Intensity (pretty useful but only 5 levels). Equalization Intensity (pretty useful but only 5 levels). Stereo Width (it would be better to have more detailed controls because now it only has 3 levels). Volume (it would be better to have more detailed controls because now it only has 4 levels). Equalization (seperate EQ module besides the previous one, not that useful because the control is way too broad) |
| **Aesthetic** | I think the mastered quality is not very good. It brings the noise up more and makes the track sound muddy and lacks punch. | I think the problem with this one is that the track gets over compressed. I don’t think the mastered quality is good enough. | I think the mastered quality is pretty good if you turn the Maximizer off. It’s better to start with the AI master and tweak the individual settings yourself. | I think the mastered quality is the best among the 4 different AI mastering tools. It improves the mix’s clarity and punchiness without messing up the mix. |

---

## What I Learned

Through this project, I developed a workflow that I think works best when combining different AI tools. Suno was the most impactful tool, as it helped define the overall mood and structure of the track. The AI features in Splice were useful but took more time to match properly. I found it more efficient to select samples from Splice and then use them in Suno for generation.

Among the stem separation tools, iZotope RX produced the highest quality results, especially for instrumental elements, and also allowed for further cleanup. However, Logic is still a good option for quick stem extraction. For mastering, Ozone 12 gave the best results when the maximizer was turned off, allowing for more controlled processing.

![Workflow Chart](Workflow%20Chart.png)

---

## Reflection

The biggest challenge in this project was improving the quality of the AI-generated samples. I tried to reduce the high-frequency noise commonly found in generative AI outputs, but some artifacts like pops were still there in certain parts of the track. Converting samples into one-shots and mapping them into MIDI instruments helped improve quality, but it was very time-consuming.

If I were to approach this project differently, I would spend more time selecting higher-quality samples from Splice to replace problematic AI-generated sounds. Regarding Ozone 12, while it analyzes tracks and matches them to references from popular songs, I found the results to be too generalized. Adjusting the EQ and other processing manually often took more time than mastering the track on your own.