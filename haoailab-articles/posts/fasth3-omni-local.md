---
title: "FastH3 Omni Goes Local: DGX Spark, RTX and Apple Silicon"
date: 2026-10-21
source: https://haoailab.com/blogs/fasth3-omni-local/
crawled: 2026-11-16
---

# FastH3 Omni Goes Local: DGX Spark, RTX and Apple Silicon

> 原文：[FastH3 Omni Goes Local: DGX Spark, RTX and Apple Silicon](https://haoailab.com/blogs/fasth3-omni-local/) · Hao AI Lab @ UCSD

# FastH3 Omni Goes Local: DGX Spark, RTX and Apple Silicon

The same FastH3 Omni request, with matched prompts, references and seeds, run end to end on DGX Spark, RTX GPUs and an Apple M5 Max.

October 21, 2026 · 17 min · Aryan Kumar, Will Lin, Hao Zhang

[![](https://img.shields.io/github/stars/hao-ai-lab/FastVideo?style=social)](https://github.com/hao-ai-lab/FastVideo)[![](https://img.shields.io/badge/🤗%20huggingface--green.svg?style=social)](https://huggingface.co/collections/FastVideo/fasth3-omni)[![Slack](https://img.shields.io/badge/Slack--4A154B?style=social&logo=slack&logoColor=blue)](https://join.slack.com/t/fastvideo/shared_invite/zt-3f4lao1uq-u~Ipx6Lt4J27AlD2y~IdLQ)

Yesterday we released [**FastH3 Omni**](/blogs/fastvideo-omniref-update/): give it a prompt plus images, video clips and a voice, and it returns a finished video with synchronized sound. On eight GB200s, a 5-second 768p clip from one reference photo takes **5.7 seconds**.

Today it comes to your desk. We ran the **exact same requests**, with identical prompts, references and seeds, end to end on one and two **NVIDIA DGX Sparks**, an **RTX 5090**, an **RTX 3090** and an **Apple M5 Max** (64 GB).

[![
Your browser does not support MP4 video with audio.](media/hero/spark-montage-poster.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--hero--spark-montage-768p.mp4)

Every clip in this video was generated on DGX Spark, one or two Sparks as labeled, from photos, video clips and voices. Turn the audio on.

## TL;DR[#](#tldr)

* **DGX Spark runs every reference mix.** A 5-second 480p clip from a photo takes **about 3 minutes on one Spark and about 2 minutes on two**, and the 128 GB of unified memory handles everything we tested, from one photo to three images or a long reference video, at 480p and 768p.
* **Across local hardware.** The same 1-photo request takes **62 s on an RTX 5090**, about **17 minutes on an RTX 3090** (plus model loading), and **19.5 minutes on an Apple M5 Max** (single run) with FastVideo’s new MLX runtime.
* **4.6× faster in seven weeks.** Text-to-video on the Spark went from 243 s at our first local release to 52.6 s today. FastH3 Omni runs on the same stack, so those gains carry over.
* **References are the real cost.** A reference photo makes a request 3.3–4.4× slower than text-to-video on the same machine. We show why, and how to trade some of it back.

## Same request, every machine[#](#same-request-every-machine)

Choose a reference mix and press **Play together**. Every panel uses the same prompt, references and seed; outputs differ across hardware, so compare quality rather than pixels.

References
1 imageImage + voice3 images1 short clip1 long clip
5 seconds
Next example →
832×480 · 5 s · seed 0

Play together
Pause all
Listen to
DGX Spark · 36L decoderDGX Spark · 8L decoderApple M5 Max · 36L decoderMute all

Playback starts when you press play. Choose one soundtrack with Listen to.

### 1 image · 5 s request

124 frames · 24 FPS · stereo audio · same prompt, references and seed on every device

**DGX Spark · 36L decoder**
192 s end to end · three-seed mean

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-36l-image-480p.mp4).
](media/posters/spark1x-36l-image-480p.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-36l-image-480p.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-36l-image-480p.mp4)

**DGX Spark · 8L decoder**
184 s end to end · three-seed mean

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-8l-image-480p.mp4).
](media/posters/spark1x-8l-image-480p.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-8l-image-480p.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-8l-image-480p.mp4)

**Apple M5 Max · 36L decoder**
19.5 min end to end · single run

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--m5max-36l-image-480p.mp4).
](media/posters/m5max-36l-image-480p.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--m5max-36l-image-480p.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--m5max-36l-image-480p.mp4)

Source references (1)

[![Picture 1 supplied on every device](/blogs/fastvideo-omniref-update/media/inputs/hf_character_action_reference.png)](/blogs/fastvideo-omniref-update/media/inputs/hf_character_action_reference.png)

Picture 1

Full promptCopy full prompt

```
subject_definitions:
<Subject 1> is the young man with dark curly hair wearing a white T-shirt in <Picture 1>.

summary:
[reference generation] <Subject 1> makes breakfast in a sunlit kitchen and speaks warmly to the camera.

retention_analysis:
<Subject 1> (appears in [Shot 1]): fully_preserved - the young man's face, dark curly hair and white T-shirt are retained.

detailed_description:
The target video is in a realistic live-action style with warm morning light.
[Shot 1] A medium close-up with a slow push-in. In a sunlit kitchen, <Subject 1> (S1) sets a bowl of oranges on the wooden counter, wipes his hands on a striped towel, looks into the camera and says with a relaxed smile, <d>[English] Breakfast is on me today, so take your time.</d> Morning light falls across his shoulders and the steam of a kettle drifts behind him.

overall_soundscape:
Bright kitchen room tone, a kettle beginning to whistle, and birdsong drifting through an open window.

non_diegetic_music:
N/A
```

### Image + voice · 5 s request

124 frames · 24 FPS · stereo audio · same prompt, references and seed on every device

**DGX Spark · 36L decoder**
198 s end to end · three-seed mean

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-36l-image-voice-480p.mp4).
](media/posters/spark1x-36l-image-voice-480p.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-36l-image-voice-480p.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-36l-image-voice-480p.mp4)

**DGX Spark · 8L decoder**
191 s end to end · three-seed mean

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-8l-image-voice-480p.mp4).
](media/posters/spark1x-8l-image-voice-480p.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-8l-image-voice-480p.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-8l-image-voice-480p.mp4)

**Apple M5 Max · 36L decoder**
20.1 min end to end · single run

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--m5max-36l-image-voice-480p.mp4).
](media/posters/m5max-36l-image-voice-480p.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--m5max-36l-image-voice-480p.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--m5max-36l-image-voice-480p.mp4)

Source references (2)

[![Picture 1 supplied on every device](/blogs/fastvideo-omniref-update/media/inputs/hf_character_action_reference.png)](/blogs/fastvideo-omniref-update/media/inputs/hf_character_action_reference.png)

Picture 1

[Download audio reference](/blogs/fastvideo-omniref-update/media/inputs/official_ref2va_1_audio.mp3)

Audio 1

Full promptCopy full prompt

```
subject_definitions:
<Subject 1> is the young man with dark curly hair wearing a white T-shirt in <Picture 1>.
<Audio 1> is the voice-timbre reference for <Subject 1> (S1).

summary:
[reference generation + audio reference] <Subject 1> finishes cooking dinner in a kitchen and speaks to the camera in the voice timbre of <Audio 1>.

retention_analysis:
<Subject 1> (appears in [Shot 1]): fully_preserved - the young man's face, dark curly hair and white T-shirt are retained.
<Audio 1>: reference - its vocal timbre guides the dialogue delivery of <Subject 1> without copying the original signal.

detailed_description:
The target video is in a realistic live-action style with soft evening light.
[Shot 1] A medium close-up with a slow push-in. In a warm kitchen, <Subject 1> (S1) dries his hands on a towel, looks into the camera and says, using the voice timbre referenced from <Audio 1>, <d>[English] Dinner is almost ready, come sit down.</d>

overall_soundscape:
Quiet kitchen room tone with a faint refrigerator hum, a simmering pot and the clink of plates.

non_diegetic_music:
N/A
```

### 3 images · 5 s request

124 frames · 24 FPS · stereo audio · same prompt, references and seed on every device

**DGX Spark · 36L decoder**
10.7 min end to end · three-seed mean

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-36l-images3-480p.mp4).
](media/posters/spark1x-36l-images3-480p.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-36l-images3-480p.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-36l-images3-480p.mp4)

**DGX Spark · 8L decoder**
10.6 min end to end · three-seed mean

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-8l-images3-480p.mp4).
](media/posters/spark1x-8l-images3-480p.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-8l-images3-480p.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-8l-images3-480p.mp4)

**Apple M5 Max · 36L decoder**
59.1 min end to end · single run

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--m5max-36l-images3-480p.mp4).
](media/posters/m5max-36l-images3-480p.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--m5max-36l-images3-480p.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--m5max-36l-images3-480p.mp4)

Source references (3)

[![Picture 1 supplied on every device](/blogs/fastvideo-omniref-update/media/inputs/hf_character_action_reference.png)](/blogs/fastvideo-omniref-update/media/inputs/hf_character_action_reference.png)

Picture 1

[![Picture 2 supplied on every device](/blogs/fastvideo-omniref-update/media/inputs/hf_fashion_glasses_reference_3.png)](/blogs/fastvideo-omniref-update/media/inputs/hf_fashion_glasses_reference_3.png)

Picture 2

[![Picture 3 supplied on every device](/blogs/fastvideo-omniref-update/media/inputs/official_fl2va_0_image.png)](/blogs/fastvideo-omniref-update/media/inputs/official_fl2va_0_image.png)

Picture 3

Full promptCopy full prompt

```
subject_definitions:
<Subject 1> is the young man with dark curly hair wearing a white T-shirt in <Picture 1>.
<Subject 2> is the pair of silver wraparound sunglasses shown from three angles in <Picture 2>.
<Subject 3> is the environment in <Picture 3>: a warmly lit traditional Japanese dining room with a family gathered around a low table.

summary:
[reference generation] <Subject 1>, wearing <Subject 2>, joins the family dinner in <Subject 3> and shares the meal.

retention_analysis:
<Subject 1> (appears in [Shot 1]): fully_preserved - the young man's face, dark curly hair and white T-shirt are retained.
<Subject 2> (appears in [Shot 1]): fully_preserved - the silver wraparound frame and dark lenses of the sunglasses are retained.
<Subject 3> (appears in [Shot 1]): fully_preserved - the paper doors, low wooden table, warm lantern light and the family are retained.

detailed_description:
The target video is in a realistic live-action style with warm lantern light.
[Shot 1] A medium wide shot with a gentle handheld drift. <Subject 1> (S1) slides open the paper door of <Subject 3>, with <Subject 2> pushed up on his forehead. He smiles, lowers the sunglasses, bows slightly and says, <d>[English] Sorry I'm late, the train was packed.</d> The family laughs and makes room for him at the low table while steam rises from the bowls of ramen.

overall_soundscape:
Soft family chatter, clinking ceramic bowls, the slide of a paper door and the hiss of a simmering pot.

non_diegetic_music:
N/A
```

### 1 short clip · 5 s request

124 frames · 24 FPS · stereo audio · same prompt, references and seed on every device

**DGX Spark · 36L decoder**
195 s end to end · three-seed mean

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-36l-clip-480p.mp4).
](media/posters/spark1x-36l-clip-480p.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-36l-clip-480p.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-36l-clip-480p.mp4)

**DGX Spark · 8L decoder**
199 s end to end · three-seed mean

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-8l-clip-480p.mp4).
](media/posters/spark1x-8l-clip-480p.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-8l-clip-480p.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-8l-clip-480p.mp4)

**Apple M5 Max · 36L decoder**
14.4 min end to end · single run

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--m5max-36l-clip-480p.mp4).
](media/posters/m5max-36l-clip-480p.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--m5max-36l-clip-480p.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--m5max-36l-clip-480p.mp4)

Source references (1)

[
[Download video reference](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)

Video 1 · with original audio

Full promptCopy full prompt

```
subject_definitions:
<Subject 1> is the young man with short wavy blonde hair, wearing a bright pink suit jacket, matching pink trousers, an unbuttoned white shirt and silver rings, holding a small black lamb in his arms in <Video 1>.
<Subject 2> is the environment in <Video 1>: a grassy hill at golden hour with white lambs grazing.
<Audio 1> is the synchronized audio track of <Video 1>, a soft background music.

summary:
[reference generation + audio reference] <Subject 1> spends a quiet moment with the black lamb in <Subject 2>, over music in the manner of <Audio 1>.

retention_analysis:
<Subject 1> (appears in [Shot 1]): fully_preserved - the man's blonde hair, pink suit, white shirt, rings and the black lamb are retained.
<Subject 2> (appears in [Shot 1]): fully_preserved - the grassy hill, golden light and grazing lambs are retained.
<Audio 1>: reference - the soft background music is referenced throughout.

detailed_description:
The target video is in a realistic photographic style with golden-hour light.
[Shot 1] A steady medium shot. <Subject 1> cradles the black lamb in the warm, low sunlight of <Subject 2>. The lamb lifts its head and nuzzles his chin; he laughs softly, tilts his head toward the camera and grins while the white lambs keep grazing on the hill.

overall_soundscape:
A light breeze over the grass and distant bleating, beneath gentle music in the manner of <Audio 1>.

non_diegetic_music:
N/A
```

### 1 long clip · 5 s request

124 frames · 24 FPS · stereo audio · same prompt, references and seed on every device

**DGX Spark · 36L decoder**
505 s end to end · three-seed mean

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-36l-video-480p.mp4).
](media/posters/spark1x-36l-video-480p.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-36l-video-480p.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-36l-video-480p.mp4)

**DGX Spark · 8L decoder**
499 s end to end · three-seed mean

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-8l-video-480p.mp4).
](media/posters/spark1x-8l-video-480p.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-8l-video-480p.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-8l-video-480p.mp4)

**Apple M5 Max · 36L decoder**
44.3 min end to end · single run

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--m5max-36l-video-480p.mp4).
](media/posters/m5max-36l-video-480p.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--m5max-36l-video-480p.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--m5max-36l-video-480p.mp4)

Source references (1)

[
[Download video reference](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--official_ref2va_0_video.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--official_ref2va_0_video.mp4)

Video 1 · with original audio

Full promptCopy full prompt

```
subject_definitions:
<Subject 1> is the young man with short wavy blonde hair, wearing a bright pink suit jacket, matching pink trousers, an unbuttoned white shirt and silver rings, holding a small black lamb in his arms in <Video 1>.
<Subject 2> is the environment in <Video 1>: a grassy hill at golden hour with white lambs grazing.
<Audio 1> is the synchronized audio track of <Video 1>, a soft background music.

summary:
[reference generation + audio reference] <Subject 1> spends a quiet moment with the black lamb in <Subject 2>, over music in the manner of <Audio 1>.

retention_analysis:
<Subject 1> (appears in [Shot 1]): fully_preserved - the man's blonde hair, pink suit, white shirt, rings and the black lamb are retained.
<Subject 2> (appears in [Shot 1]): fully_preserved - the grassy hill, golden light and grazing lambs are retained.
<Audio 1>: reference - the soft background music is referenced throughout.

detailed_description:
The target video is in a realistic photographic style with golden-hour light.
[Shot 1] A steady medium shot. <Subject 1> cradles the black lamb in the warm, low sunlight of <Subject 2>. The lamb lifts its head and nuzzles his chin; he laughs softly, tilts his head toward the camera and grins while the white lambs keep grazing on the hill.

overall_soundscape:
A light breeze over the grass and distant bleating, beneath gentle music in the manner of <Audio 1>.

non_diegetic_music:
N/A
```

JavaScript is disabled: all examples are displayed.

832×480 · 24 FPS · stereo audio · seed 0. Spark times are three-seed means; the Mac time is a single run.

## End-to-end latency[#](#end-to-end-latency)

Every bar is the full request, from prompt and references to a finished MP4 with audio.

References
1 imageImage + voice3 images1 short clip1 long clip
Resolution
480p · 832×480768p · 1344×768
Decoder
36-layer (quality)8-layer (fast)

DGX SparkOther machines

End-to-end seconds from request to finished MP4 with audio, 5 s clip (124 frames, 24 FPS), seed 0 prompt and references from the [FastH3 Omni release](/blogs/fastvideo-omniref-update/). Shorter is better.

**DGX Spark, every reference mix** (three-seed means, 36-layer decoder, 5-second clips):

| References | 2× Spark 480p | 1× Spark 480p | 2× Spark 768p | 1× Spark 768p |
| --- | --- | --- | --- | --- |
| 1 image | **130.1 s** | 192.0 s | **217.8 s** | 361.3 s |
| Image + voice | **128.6 s** | 198.3 s | **220.9 s** | 378.5 s |
| 3 images | **390.5 s** | 640.3 s | **594.8 s** | 957.9 s |
| 1 short clip | **116.2 s** | 194.8 s | **200.6 s** | 332.6 s |
| 1 long clip | **261.4 s** | 504.6 s | **366.5 s** | 656.9 s |

The two-Spark runs used the earlier FastH3 Omni QAD checkpoint, so read the 1× vs 2× ratio as indicative.

**Across local hardware** (480p, 36-layer decoder):

| References | 1× DGX Spark | RTX 5090 | RTX 3090 | Apple M5 Max |
| --- | --- | --- | --- | --- |
| 1 image | 192.0 s | 61.9 s | 16.9 min | 19.5 min |
| Image + voice | 198.3 s | 63.6 s | 18.0 min | 20.1 min |
| 1 short clip | 194.8 s | 57.2 s | 14.5 min | 14.4 min |

The M5 Max numbers are single runs; the RTX 3090 numbers exclude its ~7-minute model load per request.

* **Spark runs every mix in minutes**, at both resolutions and with either decoder. The 3-image and long-clip requests hit the memory limits of today’s 24–32 GB GPU profiles; the M5 Max runs them, but in 44–59 minutes.
* **Two Sparks are 1.5–1.9× faster than one**, and the long-clip request scales best (1.9× at 480p).
* **The decoder no longer matters much.** The 8-layer decoder saves only a few percent on Spark, because the [NVFP4 decoders](/blogs/fasth3-v21/#nvfp4-vae-decoders) take seconds and the transformer dominates.
* **Every class of local machine works.** The RTX 5090 is the quickest single GPU at about a minute, and the RTX 3090 and the Apple M5 Max land within 15–20 minutes.

## From text-to-video to references[#](#from-text-to-video-to-references)

Text-to-video on local hardware has become fast. On the Spark, where FastH3 first went local, the same 5-second 480p clip is **4.6× faster on one Spark and 6.8× faster on two** than seven weeks ago (8-layer decoder; the first release was measured cold), on top of the [8.4× we measured over the public vLLM-Omni recipe](/blogs/fasth3-local/) at launch:

1× DGX Spark2× DGX Spark

[Sep 2](/blogs/fasth3-local/)FastH3 V1 · 4 steps · full VAE

243 s

209 s

[Oct 6](/blogs/fasth3-rtx/)FastH3 V2 · 8 steps · NVFP4

141.4 s

87.2 s

[Oct 19](/blogs/fasth3-v21/)FastH3-QAD-v2 · 36-layer decoder

58.1 s

33.6 s

[Oct 19](/blogs/fasth3-v21/)FastH3-QAD-v2 · 8-layer decoder

52.6 s

30.7 s

Text-to-video on DGX Spark, end-to-end seconds for a 5 s, 832×480 clip with audio, as published in each post (Sep 2: cold starts; Oct 6 and Oct 19: warm medians).

The gains came from eight-step distillation in [NVFP4](/blogs/fasth3-rtx/), NVIDIA’s 4-bit floating-point format, then [quantization-aware distillation with 4-bit attention and NVFP4 decoders](/blogs/fasth3-v21/), which cut decoding from 43 s to under 2 s.

Adding a reference photo to the same request takes **3.3–4.4× more time** on the same machine:

Text-to-video (FastH3-QAD-v2)FastH3 Omni, 1 image reference

**2× DGX Spark**3.9× more time with a reference

33.6 s

130.1 s

**1× DGX Spark**3.3× more time with a reference

58.1 s

192 s

RTX 50904.4× more time with a reference

14.07 s

61.9 s

End-to-end seconds, 5 s clip at 832×480 with audio, 36-layer decoder. Text-to-video from the [FastH3-QAD-v2 post](/blogs/fasth3-v21/) (warm medians); FastH3 Omni from this post (three-seed means).

The reason is tokens. A 5-second 480p clip is about **14,400 video tokens**. FastH3 Omni reads each reference image on the **2048-pixel canvas** it was trained with, which adds about **7,100 VAE tokens** and another **7,100 vision tokens** in the prompt. One photo doubles the sequence to about 29,000 tokens, and three photos roughly quadruple it to nearly 60,000. This is why the 3-image request is the slowest everywhere.

The reference canvas is therefore the biggest lever you control. `--reference-max-pixels match` shrinks each reference to the clip’s own size: on the M5 Max, the 1-photo request drops from **19.5 to 4.7 minutes (4.2×)**. It is opt-in because it departs from training and changes framing and action:

**Trained reference canvas**M5 Max · 19.5 min

[![](media/posters/m5max-36l-image-480p.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--m5max-36l-image-480p.mp4)

**`--reference-max-pixels match`**M5 Max · 4.7 min

[![](media/posters/m5max-36l-image-480p-match.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--m5max-36l-image-480p-match.mp4)

## How it runs on each machine[#](#how-it-runs-on-each-machine)

FastH3 Omni pairs a ~35B-parameter transformer with a ~32B-parameter Qwen3-VL text encoder, well over 100 GB in BF16. Each machine fits it differently.

### DGX Spark[#](#dgx-spark)

Everything stays resident in the Spark’s 128 GB of unified memory: the 4-bit NVFP4 transformer, text encoder and decoder, with no offloading between stages. Attention uses the 4-bit sparse attention on 128-token tiles the model was trained with, while the text, reference and audio rows run densely at 8-bit so the conditioning stays out of FP4 rounding.

Two directly connected Sparks split the token sequence: each holds the full model and processes half the tokens. Conditioning does not split as cleanly as denoising, one reason the speedup stays below 2×.

Get started with the [Spark guide](https://haoailab.com/FastVideo/getting_started/installation/spark/) or the [Spark pair guide](https://haoailab.com/FastVideo/getting_started/installation/spark_pair/).

### RTX GPUs[#](#rtx-gpus)

The **RTX 5090** keeps the NVFP4 transformer on its 32 GB. A precomputed 155 MB table replaces 26 GB of timestep-projection weights, shrinking the transformer from 44.5 GB to 18.5 GB, and the text encoder loads only while the prompt is encoded.

The **RTX 3090** has no FP4 or FP8 hardware, so it runs FP8 weights with BF16 math through the [24 GB profile](https://github.com/hao-ai-lab/FastVideo/blob/main/examples/inference/basic/basic_fasth3_omniref_rtx4090.yaml), streaming the transformer a few blocks at a time.

### Apple Silicon[#](#apple-silicon)

FastH3 Omni runs natively on Macs through FastVideo’s [MLX runtime](https://github.com/hao-ai-lab/FastVideo/pull/2000):

* **INT6 transformer (17 GB).** Timestep projections are precomputed, as on the RTX 5090, and INT6 fits the rest in memory; Apple GPUs have no FP4 units.
* **No base VAE needed.** The [LightVAE](https://huggingface.co/lightx2v/LightVAE) Lite encoder (406 MB) reads the references, and the same NVFP4 decoders as on Blackwell write the frames.
* **The NVFP4 text encoder runs unchanged**, including its vision tower.
* **Trained sparsity on Metal**, through a new Metal kernel for the model’s 128-token sparse-attention tiles.

Peak memory on the M5 Max stays between 27 and 31 GB across all five workloads.

## Quantization-aware distillation[#](#quantization-aware-distillation)

Rounding a distilled eight-step model to 4 bits after training costs quality. **Quantization-aware distillation (QAD)** instead trains the NVFP4 student against the full-precision teacher with FP4 numerics active from the first step, so the weights learn to absorb the rounding. The sparse-attention gates and norms stay frozen, because retraining them changes which tiles are selected.

FastH3 Omni’s local weights, [`FastVideo/FastH3-Omni-NVFP4-QAD`](https://huggingface.co/FastVideo/FastH3-Omni-NVFP4-QAD), extend the [FastH3-QAD-v2 recipe](/blogs/fasth3-v21/) to 4-bit attention. The shared training recipe is available in [FastVideo #1989](https://github.com/hao-ai-lab/FastVideo/pull/1989).

## Try it[#](#try-it)

| Machine | Weights and recipe |
| --- | --- |
| DGX Spark | [NVFP4 QAD weights](https://huggingface.co/FastVideo/FastH3-Omni-NVFP4-QAD) · [`spark` recipe](https://github.com/hao-ai-lab/FastVideo/blob/main/examples/inference/basic/basic_fasth3_omniref_spark.yaml) |
| 2× DGX Spark | [NVFP4 QAD weights](https://huggingface.co/FastVideo/FastH3-Omni-NVFP4-QAD) · [`spark-pair` recipe](https://github.com/hao-ai-lab/FastVideo/blob/main/examples/inference/basic/basic_fasth3_omniref_spark_pair.yaml) |
| RTX 5090 | [NVFP4 QAD weights](https://huggingface.co/FastVideo/FastH3-Omni-NVFP4-QAD) · [`rtx-5090` recipe](https://github.com/hao-ai-lab/FastVideo/blob/main/examples/inference/basic/basic_fasth3_omniref_rtx5090.yaml) |
| 24 GB RTX GPUs | [FP8 weights](https://huggingface.co/FastVideo/FastH3-Omni-FP8-Comfy) · [`rtx-4090` recipe](https://github.com/hao-ai-lab/FastVideo/blob/main/examples/inference/basic/basic_fasth3_omniref_rtx4090.yaml) |
| Apple Silicon | [BF16 release](https://huggingface.co/FastVideo/FastVideo-FastH3-Omni-8-Step-V1), converted locally · [Apple Silicon recipe](https://haoailab.com/FastVideo/cookbook/minimax-h3/models/fasth3-omniref-mlx/) |

Start with the [FastVideo cookbook](https://haoailab.com/FastVideo/cookbook/) and the [FastH3 Omni recipe builder](https://haoailab.com/FastVideo/cookbook/minimax-h3/fasth3-omniref/).

Prefer a visual workflow? The local community has been making [great things](#from-the-community) with our [ComfyUI release](https://huggingface.co/FastVideo/FastH3-Omni-Comfy), available in [NVFP4 QAD](https://huggingface.co/FastVideo/FastH3-Omni-NVFP4-QAD-Comfy) and [FP8](https://huggingface.co/FastVideo/FastH3-Omni-FP8-Comfy).

## From the community[#](#from-the-community)

Within a day of release, people were running FastH3 Omni on their own GPUs:

**RTX 3090 · 24 GB**15 s clip in ~12 min

> FastH3-OmniRef（INT8版）をRTX 3090でローカル生成してみました。参照画像5枚から、5人が順番に登場してあいさつする15秒の動画です。
>
> — AIひよこ (@AibeginnerR8) [October 21, 2026](https://x.com/AibeginnerR8/status/2112831271185388002)

**RTX 4070 · 12 GB**416 s, from 1312 s dense

> FastH3 OmniRefをComfyUIで実測！（RTX 4070 12GB／縦1024×1792・5秒）
>
> — Kamimoto (@sep\_is\_heim) [October 21, 2026](https://x.com/sep_is_heim/status/2112748834464170432)

**16 GB GPU**5 s clip in ~3 min

> FastH3 OmniRef、試してみました。アニメのダンス動画と曲を渡すと、実写の子がその振り付けのまま曲に合わせて踊ってくれます
>
> — NookWright (@nookwright) [October 21, 2026](https://x.com/nookwright/status/2112740667956871372)

**RTX 4090 · 24 GB**15 s clip in 4 min

> FastH3 Omni 8Stepsのテスト。4090で15秒が生成4分。
>
> — Alone1M (@Alone1Moon) [October 21, 2026](https://x.com/Alone1Moon/status/2112930098013946059)

**RTX 4090 · 24 GB**15 s 480p in 1:24

> Been testing FastH3 Omni in @comfyui since the weights were released yesterday on my 4090 RTX.
>
> — OrctonAI (@OrctonAI) [October 21, 2026](https://x.com/OrctonAI/status/2112955932216791381)

**RTX 5090 · 32 GB**115 s, from 555 s base

> MiniMax-H3の8step蒸留モデル「FastH3-Omni」をComfyUIで検証✨ RTX 5090 / R2V / 768×1344 / 5秒
>
> — DeepForest (@DeepForest\_Inc) [October 21, 2026](https://x.com/DeepForest_Inc/status/2112770785970413929)

**RTX 5090 · 32 GB**313 s, from 742 s base

> MiniMax-H3の8step蒸留モデル「FastH3-Omni」をComfyUIで比較 RTX 5090 / R2V / 1024×576 / 約15秒
>
> — まぷて (@mapte\_fireball) [October 21, 2026](https://x.com/mapte_fireball/status/2112807768633831534)

**RTX 5090 · 32 GB**4:39 with NVFP4 QAD

> 14,4s Video, same prompt, same references (image, voice), same seed. On a 5090
>
> — Mathias\_M (@matze2001) [October 21, 2026](https://x.com/matze2001/status/2112878541327028466)

**ComfyUI**“Insanely fast, accurate”

> FastH3 Omni is insanely fast, accurate, and overall a very good model! i highly recommend!
>
> — Rebel AI (@realrebelai) [October 21, 2026](https://x.com/realrebelai/status/2112679911614030179)

Community-reported, each on its own setup and settings. Scroll for more; click a post to open it.

## What’s next[#](#whats-next)

We will keep pushing what FastH3 Omni can do on Apple Silicon, keep improving quality and speed across every machine, and release smaller models that fit a wider range of consumer hardware.

## Limitations[#](#limitations)

* NVFP4, FP8 and INT6 are different numerical variants, so outputs differ from the BF16 release and from each other for the same seed.
* The M5 Max numbers are single runs, the RTX 3090 numbers exclude model loading, and the two-Spark runs used the earlier QAD checkpoint.
* `--reference-max-pixels match` trades reference detail for speed.

## Acknowledgements[#](#acknowledgements)

FastH3 builds on [MiniMax H3](https://huggingface.co/MiniMaxAI/MiniMax-H3). We thank the MiniMax team for releasing its weights and code.

We thank the NVIDIA Enterprise Products team (Pengcheng Li and Cliff Woolley) for the Video Sparse Attention kernel used by FastH3. We thank the [NVIDIA FastGen](https://github.com/NVlabs/FastGen) team (Julius Berner, Chao Liu and Arash Vahdat) for the DMD2 framework and H3 reference work, and for introducing [Parallel Decoding Distillation](https://research.nvidia.com/labs/genair/pdd/).

We thank [Nuva Lab](https://nuvalab.ai/) for bringing production-grounded creative video workflows to FastH3, and the upstream serving, kernel and open-source communities whose implementations make these experiments possible. We also acknowledge [Reactor](https://www.reactor.inc/) for supporting FastH3 Omni, and the [vLLM project](https://vllm.ai/), [NVIDIA](https://www.nvidia.com/en-us/) and [MBZUAI](https://mbzuai.ac.ae/) for their support of FastVideo.

Finally, thanks to community member [@posi\_posi8](https://x.com/posi_posi8), who volunteered an Apple M5 Max to benchmark FastH3 Omni for this post.

## FastVideo team[#](#fastvideo-team)

**Contributor:** [Aryan Kumar](https://github.com/aryan5v)

  
**Tech lead:** [Will Lin](https://github.com/SolitaryThinker)

  
**Advisor:** [Hao Zhang](https://github.com/zhisbug)
