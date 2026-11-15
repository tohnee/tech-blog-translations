---
title: "FastVideo FastH3 Omni: Open Source Real-Time Minimax FastH3 Ref2VA on NVIDIA Blackwell, RTX Spark, and RTX GPUs."
date: 2026-10-20
source: https://haoailab.com/blogs/fastvideo-omniref-update/
crawled: 2026-11-16
---

# FastVideo FastH3 Omni: Open Source Real-Time Minimax FastH3 Ref2VA on NVIDIA Blackwell, RTX Spark, and RTX GPUs.

> 原文：[FastVideo FastH3 Omni: Open Source Real-Time Minimax FastH3 Ref2VA on NVIDIA Blackwell, RTX Spark, and RTX GPUs.](https://haoailab.com/blogs/fastvideo-omniref-update/) · Hao AI Lab @ UCSD

# FastVideo FastH3 Omni: Open Source Real-Time Minimax FastH3 Ref2VA on NVIDIA Blackwell, RTX Spark, and RTX GPUs.

MiniMax H3 video and audio with up to approximately 12× lower end-to-end latency on eight GB200 GPUs, plus optimized NVFP4 QAD checkpoints for local AI.

October 20, 2026 · FastVideo Team

[![](https://img.shields.io/github/stars/hao-ai-lab/FastVideo?style=social)](https://github.com/hao-ai-lab/FastVideo)[![](https://img.shields.io/badge/🤗%20huggingface--green.svg?style=social)](https://huggingface.co/collections/FastVideo/fasth3-omni)[![Slack](https://img.shields.io/badge/Slack--4A154B?style=social&logo=slack&logoColor=blue)](https://join.slack.com/t/fastvideo/shared_invite/zt-3f4lao1uq-u~Ipx6Lt4J27AlD2y~IdLQ)

FastVideo is open-sourcing **FastH3 Omni**, a distilled MiniMax H3 model for reference-guided video and audio. Give it a prompt plus images, video clips and a voice reference to generate a finished video with synchronized sound.

[Model weights](https://huggingface.co/collections/FastVideo/fasth3-omni) · [UniServe deployment](#deploy-fasth3-omni-with-uniserve) · [Local AI with FastVideo](#local-ai-with-fastvideo)

ComfyUI support is available. Our local AI blog post and release are planned for tomorrow, **October 21**.

[
Your browser does not support MP4 video with audio.](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--hero--trilingual-bgm-1080p.mp4)

This entire video was generated with FastH3 Omni on FastVideo.

## TL;DR[#](#tldr)

* **Eight transformer evaluations**, down from Base’s 50, with image, video and audio references.
* **5.6–11.9× lower end-to-end latency** across 27 matched workloads on eight GB200 GPUs. This compares full serving recipes, using Base’s `lossless` numerical policy; [methodology](#benchmark-methodology).
* **Real-time Generation on FastVideo UniServe**: On particular FastH3 Omni tasks, FastVideo UniServe achieves real time generation speeds for 768p videos for 5s, 10s, and 15s clips.
* **Local AI.** Run on [DGX Spark or RTX 5090 with FastVideo](#local-ai-with-fastvideo), using the NVFP4 QAD weights and device recipes.
* **See and hear the outputs below.** Change the references or clip length, then play the matched examples together. Reference inputs are expanded; open the full prompt when you need it.
* **Partners.** Thanks to [Nuva Lab](https://nuvalab.ai/), [Reactor](https://www.reactor.inc/), NVIDIA FastGen Team, and NVIDIA Enterprise products for their collaboration and support.

## Matched reference inputs and outputs[#](#matched-reference-inputs-and-outputs)

Choose a reference mix and clip length to compare **Base, FastH3 Omni and FastH3 Omni with the 36-layer VAE**. All examples use seed 0 and matched inputs; these are qualitative comparisons, not evidence of output parity.

References
1 imageImage + voice3 images9 images1 short clip1 long clip3 clipsImage + video + voice9 images + 3 clips
Requested length
5 seconds10 seconds15 seconds
Next example →
8×GB200 · seed 0

Play together
Pause all
Listen to
BaseFastH3 OmniFastH3 Omni · 36L VAEMute all

Playback starts when you press play. Choose one soundtrack with Listen to.

### 1 image · 5 s request

124 frames · 24 FPS · stereo audio · matching prompt, references, seed and GPU count

**Base**
35.44 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-image-5s-seed0.mp4).
](media/posters/base-image-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-image-5s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-image-5s-seed0.mp4)

**FastH3 Omni**
5.67 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-image-5s-seed0.mp4).
](media/posters/fast-image-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-image-5s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-image-5s-seed0.mp4)

**FastH3 Omni · 36L VAE**
Quality comparison

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-image-5s-seed0.mp4).
](media/posters/decoder36-image-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-image-5s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-image-5s-seed0.mp4)

**6.25× lower latency** for this workload. 35.44 s → 5.67 s end to end (three-seed means).

Source references (1)

[![Picture 1 supplied to all three variants](media/inputs/hf_character_action_reference.png)](media/inputs/hf_character_action_reference.png)

Picture 1 · [original input](media/inputs/hf_character_action_reference.png)

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

### 1 image · 10 s request

243 frames · 24 FPS · stereo audio · matching prompt, references, seed and GPU count

**Base**
78.53 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-image-10s-seed0.mp4).
](media/posters/base-image-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-image-10s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-image-10s-seed0.mp4)

**FastH3 Omni**
9.37 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-image-10s-seed0.mp4).
](media/posters/fast-image-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-image-10s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-image-10s-seed0.mp4)

**FastH3 Omni · 36L VAE**
Quality comparison

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-image-10s-seed0.mp4).
](media/posters/decoder36-image-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-image-10s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-image-10s-seed0.mp4)

**8.38× lower latency** for this workload. 78.53 s → 9.37 s end to end (three-seed means).

Source references (1)

[![Picture 1 supplied to all three variants](media/inputs/hf_character_action_reference.png)](media/inputs/hf_character_action_reference.png)

Picture 1 · [original input](media/inputs/hf_character_action_reference.png)

Full promptCopy full prompt

```
subject_definitions:
<Subject 1> is the young man with dark curly hair wearing a white T-shirt in <Picture 1>.

summary:
[reference generation] <Subject 1> makes breakfast in a sunlit kitchen and speaks warmly to the camera.

retention_analysis:
<Subject 1> (appears in [Shot 1], [Shot 2]): fully_preserved - the young man's face, dark curly hair and white T-shirt are retained.

detailed_description:
The target video is in a realistic live-action style with warm morning light.
[Shot 1] A medium close-up with a slow push-in. In a sunlit kitchen, <Subject 1> (S1) sets a bowl of oranges on the wooden counter, wipes his hands on a striped towel, looks into the camera and says with a relaxed smile, <d>[English] Breakfast is on me today, so take your time.</d> Morning light falls across his shoulders and the steam of a kettle drifts behind him.
[Shot 2] At 00:05.000, the shot cuts to a close shot over the counter. <Subject 1> (S1) slices an orange in half on a wooden board, squeezes it into a glass and slides the glass toward the camera, saying, <d>[English] Fresh juice first.</d> A drop runs down the glass in the sunlight.

overall_soundscape:
Bright kitchen room tone, a kettle beginning to whistle, and birdsong drifting through an open window.

non_diegetic_music:
N/A
```

### 1 image · 15 s request

362 frames · 24 FPS · stereo audio · matching prompt, references, seed and GPU count

**Base**
139.69 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-image-15s-seed0.mp4).
](media/posters/base-image-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-image-15s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-image-15s-seed0.mp4)

**FastH3 Omni**
14.14 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-image-15s-seed0.mp4).
](media/posters/fast-image-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-image-15s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-image-15s-seed0.mp4)

**FastH3 Omni · 36L VAE**
Quality comparison

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-image-15s-seed0.mp4).
](media/posters/decoder36-image-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-image-15s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-image-15s-seed0.mp4)

**9.88× lower latency** for this workload. 139.69 s → 14.14 s end to end (three-seed means).

Source references (1)

[![Picture 1 supplied to all three variants](media/inputs/hf_character_action_reference.png)](media/inputs/hf_character_action_reference.png)

Picture 1 · [original input](media/inputs/hf_character_action_reference.png)

Full promptCopy full prompt

```
subject_definitions:
<Subject 1> is the young man with dark curly hair wearing a white T-shirt in <Picture 1>.

summary:
[reference generation] <Subject 1> makes breakfast in a sunlit kitchen and speaks warmly to the camera.

retention_analysis:
<Subject 1> (appears in [Shot 1], [Shot 2], [Shot 3]): fully_preserved - the young man's face, dark curly hair and white T-shirt are retained.

detailed_description:
The target video is in a realistic live-action style with warm morning light.
[Shot 1] A medium close-up with a slow push-in. In a sunlit kitchen, <Subject 1> (S1) sets a bowl of oranges on the wooden counter, wipes his hands on a striped towel, looks into the camera and says with a relaxed smile, <d>[English] Breakfast is on me today, so take your time.</d> Morning light falls across his shoulders and the steam of a kettle drifts behind him.
[Shot 2] At 00:05.000, the shot cuts to a close shot over the counter. <Subject 1> (S1) slices an orange in half on a wooden board, squeezes it into a glass and slides the glass toward the camera, saying, <d>[English] Fresh juice first.</d> A drop runs down the glass in the sunlight.
[Shot 3] At 00:10.000, the shot cuts to a medium wide shot of the whole kitchen. <Subject 1> lifts the whistling kettle off the stove, pours hot water into a teapot and turns back to the camera with a grin as the steam rises past the open window.

overall_soundscape:
Bright kitchen room tone, a kettle beginning to whistle, and birdsong drifting through an open window.

non_diegetic_music:
N/A
```

### Image + voice · 5 s request

124 frames · 24 FPS · stereo audio · matching prompt, references, seed and GPU count

**Base**
35.92 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-image-voice-5s-seed0.mp4).
](media/posters/base-image-voice-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-image-voice-5s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-image-voice-5s-seed0.mp4)

**FastH3 Omni**
5.84 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-image-voice-5s-seed0.mp4).
](media/posters/fast-image-voice-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-image-voice-5s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-image-voice-5s-seed0.mp4)

**FastH3 Omni · 36L VAE**
Quality comparison

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-image-voice-5s-seed0.mp4).
](media/posters/decoder36-image-voice-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-image-voice-5s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-image-voice-5s-seed0.mp4)

**6.15× lower latency** for this workload. 35.92 s → 5.84 s end to end (three-seed means).

Source references (2)

[![Picture 1 supplied to all three variants](media/inputs/hf_character_action_reference.png)](media/inputs/hf_character_action_reference.png)

Picture 1 · [original input](media/inputs/hf_character_action_reference.png)

[Download audio reference](media/inputs/official_ref2va_1_audio.mp3)

Audio 1 · [original input](media/inputs/official_ref2va_1_audio.mp3)

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

### Image + voice · 10 s request

243 frames · 24 FPS · stereo audio · matching prompt, references, seed and GPU count

**Base**
79.92 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-image-voice-10s-seed0.mp4).
](media/posters/base-image-voice-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-image-voice-10s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-image-voice-10s-seed0.mp4)

**FastH3 Omni**
9.71 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-image-voice-10s-seed0.mp4).
](media/posters/fast-image-voice-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-image-voice-10s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-image-voice-10s-seed0.mp4)

**FastH3 Omni · 36L VAE**
Quality comparison

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-image-voice-10s-seed0.mp4).
](media/posters/decoder36-image-voice-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-image-voice-10s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-image-voice-10s-seed0.mp4)

**8.23× lower latency** for this workload. 79.92 s → 9.71 s end to end (three-seed means).

Source references (2)

[![Picture 1 supplied to all three variants](media/inputs/hf_character_action_reference.png)](media/inputs/hf_character_action_reference.png)

Picture 1 · [original input](media/inputs/hf_character_action_reference.png)

[Download audio reference](media/inputs/official_ref2va_1_audio.mp3)

Audio 1 · [original input](media/inputs/official_ref2va_1_audio.mp3)

Full promptCopy full prompt

```
subject_definitions:
<Subject 1> is the young man with dark curly hair wearing a white T-shirt in <Picture 1>.
<Audio 1> is the voice-timbre reference for <Subject 1> (S1).

summary:
[reference generation + audio reference] <Subject 1> finishes cooking dinner in a kitchen and speaks to the camera in the voice timbre of <Audio 1>.

retention_analysis:
<Subject 1> (appears in [Shot 1], [Shot 2]): fully_preserved - the young man's face, dark curly hair and white T-shirt are retained.
<Audio 1>: reference - its vocal timbre guides the dialogue delivery of <Subject 1> without copying the original signal.

detailed_description:
The target video is in a realistic live-action style with soft evening light.
[Shot 1] A medium close-up with a slow push-in. In a warm kitchen, <Subject 1> (S1) dries his hands on a towel, looks into the camera and says, using the voice timbre referenced from <Audio 1>, <d>[English] Dinner is almost ready, come sit down.</d>
[Shot 2] At 00:05.000, the shot cuts to a close shot of the stove. <Subject 1> (S1) lifts the lid of a pot, tastes the sauce from a wooden spoon, nods and says in the same voice, <d>[English] A little more salt, and it is perfect.</d> Steam curls up past his face.

overall_soundscape:
Quiet kitchen room tone with a faint refrigerator hum, a simmering pot and the clink of plates.

non_diegetic_music:
N/A
```

### Image + voice · 15 s request

362 frames · 24 FPS · stereo audio · matching prompt, references, seed and GPU count

**Base**
140.91 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-image-voice-15s-seed0.mp4).
](media/posters/base-image-voice-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-image-voice-15s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-image-voice-15s-seed0.mp4)

**FastH3 Omni**
14.44 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-image-voice-15s-seed0.mp4).
](media/posters/fast-image-voice-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-image-voice-15s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-image-voice-15s-seed0.mp4)

**FastH3 Omni · 36L VAE**
Quality comparison

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-image-voice-15s-seed0.mp4).
](media/posters/decoder36-image-voice-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-image-voice-15s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-image-voice-15s-seed0.mp4)

**9.76× lower latency** for this workload. 140.91 s → 14.44 s end to end (three-seed means).

Source references (2)

[![Picture 1 supplied to all three variants](media/inputs/hf_character_action_reference.png)](media/inputs/hf_character_action_reference.png)

Picture 1 · [original input](media/inputs/hf_character_action_reference.png)

[Download audio reference](media/inputs/official_ref2va_1_audio.mp3)

Audio 1 · [original input](media/inputs/official_ref2va_1_audio.mp3)

Full promptCopy full prompt

```
subject_definitions:
<Subject 1> is the young man with dark curly hair wearing a white T-shirt in <Picture 1>.
<Audio 1> is the voice-timbre reference for <Subject 1> (S1).

summary:
[reference generation + audio reference] <Subject 1> finishes cooking dinner in a kitchen and speaks to the camera in the voice timbre of <Audio 1>.

retention_analysis:
<Subject 1> (appears in [Shot 1], [Shot 2], [Shot 3]): fully_preserved - the young man's face, dark curly hair and white T-shirt are retained.
<Audio 1>: reference - its vocal timbre guides the dialogue delivery of <Subject 1> without copying the original signal.

detailed_description:
The target video is in a realistic live-action style with soft evening light.
[Shot 1] A medium close-up with a slow push-in. In a warm kitchen, <Subject 1> (S1) dries his hands on a towel, looks into the camera and says, using the voice timbre referenced from <Audio 1>, <d>[English] Dinner is almost ready, come sit down.</d>
[Shot 2] At 00:05.000, the shot cuts to a close shot of the stove. <Subject 1> (S1) lifts the lid of a pot, tastes the sauce from a wooden spoon, nods and says in the same voice, <d>[English] A little more salt, and it is perfect.</d> Steam curls up past his face.
[Shot 3] At 00:10.000, the shot cuts to a medium wide shot. <Subject 1> (S1) carries two plates to a small table by the window, sets them down, looks back at the camera and says, <d>[English] Come on, before it gets cold.</d>

overall_soundscape:
Quiet kitchen room tone with a faint refrigerator hum, a simmering pot and the clink of plates.

non_diegetic_music:
N/A
```

### 3 images · 5 s request

124 frames · 24 FPS · stereo audio · matching prompt, references, seed and GPU count

**Base**
73.09 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-images3-5s-seed0.mp4).
](media/posters/base-images3-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-images3-5s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-images3-5s-seed0.mp4)

**FastH3 Omni**
12.42 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-images3-5s-seed0.mp4).
](media/posters/fast-images3-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-images3-5s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-images3-5s-seed0.mp4)

**FastH3 Omni · 36L VAE**
Quality comparison

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-images3-5s-seed0.mp4).
](media/posters/decoder36-images3-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-images3-5s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-images3-5s-seed0.mp4)

**5.88× lower latency** for this workload. 73.09 s → 12.42 s end to end (three-seed means).

Source references (3)

[![Picture 1 supplied to all three variants](media/inputs/hf_character_action_reference.png)](media/inputs/hf_character_action_reference.png)

Picture 1 · [original input](media/inputs/hf_character_action_reference.png)

[![Picture 2 supplied to all three variants](media/inputs/hf_fashion_glasses_reference_3.png)](media/inputs/hf_fashion_glasses_reference_3.png)

Picture 2 · [original input](media/inputs/hf_fashion_glasses_reference_3.png)

[![Picture 3 supplied to all three variants](media/inputs/official_fl2va_0_image.png)](media/inputs/official_fl2va_0_image.png)

Picture 3 · [original input](media/inputs/official_fl2va_0_image.png)

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

### 3 images · 10 s request

243 frames · 24 FPS · stereo audio · matching prompt, references, seed and GPU count

**Base**
131.25 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-images3-10s-seed0.mp4).
](media/posters/base-images3-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-images3-10s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-images3-10s-seed0.mp4)

**FastH3 Omni**
19.15 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-images3-10s-seed0.mp4).
](media/posters/fast-images3-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-images3-10s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-images3-10s-seed0.mp4)

**FastH3 Omni · 36L VAE**
Quality comparison

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-images3-10s-seed0.mp4).
](media/posters/decoder36-images3-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-images3-10s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-images3-10s-seed0.mp4)

**6.85× lower latency** for this workload. 131.25 s → 19.15 s end to end (three-seed means).

Source references (3)

[![Picture 1 supplied to all three variants](media/inputs/hf_character_action_reference.png)](media/inputs/hf_character_action_reference.png)

Picture 1 · [original input](media/inputs/hf_character_action_reference.png)

[![Picture 2 supplied to all three variants](media/inputs/hf_fashion_glasses_reference_3.png)](media/inputs/hf_fashion_glasses_reference_3.png)

Picture 2 · [original input](media/inputs/hf_fashion_glasses_reference_3.png)

[![Picture 3 supplied to all three variants](media/inputs/official_fl2va_0_image.png)](media/inputs/official_fl2va_0_image.png)

Picture 3 · [original input](media/inputs/official_fl2va_0_image.png)

Full promptCopy full prompt

```
subject_definitions:
<Subject 1> is the young man with dark curly hair wearing a white T-shirt in <Picture 1>.
<Subject 2> is the pair of silver wraparound sunglasses shown from three angles in <Picture 2>.
<Subject 3> is the environment in <Picture 3>: a warmly lit traditional Japanese dining room with a family gathered around a low table.

summary:
[reference generation] <Subject 1>, wearing <Subject 2>, joins the family dinner in <Subject 3> and shares the meal.

retention_analysis:
<Subject 1> (appears in [Shot 1], [Shot 2]): fully_preserved - the young man's face, dark curly hair and white T-shirt are retained.
<Subject 2> (appears in [Shot 1], [Shot 2]): fully_preserved - the silver wraparound frame and dark lenses of the sunglasses are retained.
<Subject 3> (appears in [Shot 1], [Shot 2]): fully_preserved - the paper doors, low wooden table, warm lantern light and the family are retained.

detailed_description:
The target video is in a realistic live-action style with warm lantern light.
[Shot 1] A medium wide shot with a gentle handheld drift. <Subject 1> (S1) slides open the paper door of <Subject 3>, with <Subject 2> pushed up on his forehead. He smiles, lowers the sunglasses, bows slightly and says, <d>[English] Sorry I'm late, the train was packed.</d> The family laughs and makes room for him at the low table while steam rises from the bowls of ramen.
[Shot 2] At 00:05.000, the shot cuts to a medium shot across the table. <Subject 1> kneels at the low table, takes off <Subject 2> and sets them beside his bowl. The child across from him picks up the sunglasses, tries them on, and the whole family laughs.

overall_soundscape:
Soft family chatter, clinking ceramic bowls, the slide of a paper door and the hiss of a simmering pot.

non_diegetic_music:
N/A
```

### 3 images · 15 s request

362 frames · 24 FPS · stereo audio · matching prompt, references, seed and GPU count

**Base**
206.88 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-images3-15s-seed0.mp4).
](media/posters/base-images3-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-images3-15s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-images3-15s-seed0.mp4)

**FastH3 Omni**
26.53 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-images3-15s-seed0.mp4).
](media/posters/fast-images3-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-images3-15s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-images3-15s-seed0.mp4)

**FastH3 Omni · 36L VAE**
Quality comparison

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-images3-15s-seed0.mp4).
](media/posters/decoder36-images3-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-images3-15s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-images3-15s-seed0.mp4)

**7.80× lower latency** for this workload. 206.88 s → 26.53 s end to end (three-seed means).

Source references (3)

[![Picture 1 supplied to all three variants](media/inputs/hf_character_action_reference.png)](media/inputs/hf_character_action_reference.png)

Picture 1 · [original input](media/inputs/hf_character_action_reference.png)

[![Picture 2 supplied to all three variants](media/inputs/hf_fashion_glasses_reference_3.png)](media/inputs/hf_fashion_glasses_reference_3.png)

Picture 2 · [original input](media/inputs/hf_fashion_glasses_reference_3.png)

[![Picture 3 supplied to all three variants](media/inputs/official_fl2va_0_image.png)](media/inputs/official_fl2va_0_image.png)

Picture 3 · [original input](media/inputs/official_fl2va_0_image.png)

Full promptCopy full prompt

```
subject_definitions:
<Subject 1> is the young man with dark curly hair wearing a white T-shirt in <Picture 1>.
<Subject 2> is the pair of silver wraparound sunglasses shown from three angles in <Picture 2>.
<Subject 3> is the environment in <Picture 3>: a warmly lit traditional Japanese dining room with a family gathered around a low table.

summary:
[reference generation] <Subject 1>, wearing <Subject 2>, joins the family dinner in <Subject 3> and shares the meal.

retention_analysis:
<Subject 1> (appears in [Shot 1], [Shot 2], [Shot 3]): fully_preserved - the young man's face, dark curly hair and white T-shirt are retained.
<Subject 2> (appears in [Shot 1], [Shot 2]): fully_preserved - the silver wraparound frame and dark lenses of the sunglasses are retained.
<Subject 3> (appears in [Shot 1], [Shot 2], [Shot 3]): fully_preserved - the paper doors, low wooden table, warm lantern light and the family are retained.

detailed_description:
The target video is in a realistic live-action style with warm lantern light.
[Shot 1] A medium wide shot with a gentle handheld drift. <Subject 1> (S1) slides open the paper door of <Subject 3>, with <Subject 2> pushed up on his forehead. He smiles, lowers the sunglasses, bows slightly and says, <d>[English] Sorry I'm late, the train was packed.</d> The family laughs and makes room for him at the low table while steam rises from the bowls of ramen.
[Shot 2] At 00:05.000, the shot cuts to a medium shot across the table. <Subject 1> kneels at the low table, takes off <Subject 2> and sets them beside his bowl. The child across from him picks up the sunglasses, tries them on, and the whole family laughs.
[Shot 3] At 00:10.000, the shot cuts to a close-up of a steaming bowl of ramen. <Subject 1> (S1) lifts noodles with his chopsticks, takes a bite and says, <d>[English] This is worth the trip.</d> The lantern light glows on the lacquered table.

overall_soundscape:
Soft family chatter, clinking ceramic bowls, the slide of a paper door and the hiss of a simmering pot.

non_diegetic_music:
N/A
```

### 9 images · 5 s request

124 frames · 24 FPS · stereo audio · matching prompt, references, seed and GPU count

**Base**
121.61 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-images9-5s-seed0.mp4).
](media/posters/base-images9-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-images9-5s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-images9-5s-seed0.mp4)

**FastH3 Omni**
21.59 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-images9-5s-seed0.mp4).
](media/posters/fast-images9-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-images9-5s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-images9-5s-seed0.mp4)

**FastH3 Omni · 36L VAE**
Quality comparison

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-images9-5s-seed0.mp4).
](media/posters/decoder36-images9-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-images9-5s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-images9-5s-seed0.mp4)

**5.63× lower latency** for this workload. 121.61 s → 21.59 s end to end (three-seed means).

Source references (9)

[![Picture 1 supplied to all three variants](media/inputs/square_character_action_reference.png)](media/inputs/square_character_action_reference.png)

Picture 1 · [original input](media/inputs/square_character_action_reference.png)

[![Picture 2 supplied to all three variants](media/inputs/square_official_fl2va_0_image.png)](media/inputs/square_official_fl2va_0_image.png)

Picture 2 · [original input](media/inputs/square_official_fl2va_0_image.png)

[![Picture 3 supplied to all three variants](media/inputs/square_fashion_glasses_reference_1.png)](media/inputs/square_fashion_glasses_reference_1.png)

Picture 3 · [original input](media/inputs/square_fashion_glasses_reference_1.png)

[![Picture 4 supplied to all three variants](media/inputs/square_fashion_glasses_reference_2.png)](media/inputs/square_fashion_glasses_reference_2.png)

Picture 4 · [original input](media/inputs/square_fashion_glasses_reference_2.png)

[![Picture 5 supplied to all three variants](media/inputs/square_fashion_glasses_reference_3.png)](media/inputs/square_fashion_glasses_reference_3.png)

Picture 5 · [original input](media/inputs/square_fashion_glasses_reference_3.png)

[![Picture 6 supplied to all three variants](media/inputs/square_fl2va_clay_fox_reference.png)](media/inputs/square_fl2va_clay_fox_reference.png)

Picture 6 · [original input](media/inputs/square_fl2va_clay_fox_reference.png)

[![Picture 7 supplied to all three variants](media/inputs/square_h3_cinematic_shot_3s.png)](media/inputs/square_h3_cinematic_shot_3s.png)

Picture 7 · [original input](media/inputs/square_h3_cinematic_shot_3s.png)

[![Picture 8 supplied to all three variants](media/inputs/square_h3_suspense_title_2s.png)](media/inputs/square_h3_suspense_title_2s.png)

Picture 8 · [original input](media/inputs/square_h3_suspense_title_2s.png)

[![Picture 9 supplied to all three variants](media/inputs/square_robot_arm_red_cube_1s.png)](media/inputs/square_robot_arm_red_cube_1s.png)

Picture 9 · [original input](media/inputs/square_robot_arm_red_cube_1s.png)

Full promptCopy full prompt

```
subject_definitions:
<Subject 1> is the young man with dark curly hair wearing a white T-shirt in <Picture 1>.
<Subject 2> is the model in the black sleeveless dress in <Picture 3> and <Picture 4>.
<Subject 3> is the clay fox in <Picture 6>.
<Subject 4> is the pair of silver wraparound sunglasses in <Picture 5>.
<Subject 5> is the white robotic arm in <Picture 9>.
<Subject 6> is the family dining room in <Picture 2>.
<Subject 7> is the starship observation deck in <Picture 7>.
<Subject 8> is the noir title-card style of <Picture 8>.

summary:
[reference generation] A five-shot sunglasses commercial cuts between a family dinner, a fashion studio, a clay forest, a robot lab and a starship deck, and ends on a noir title card.

retention_analysis:
<Subject 1> (appears in [Shot 1]): fully_preserved - the young man's face, dark curly hair and white T-shirt are retained.
<Subject 2> (appears in [Shot 2]): fully_preserved - the model's braided hair and black sleeveless dress are retained.
<Subject 3> (appears in [Shot 3]): fully_preserved - the clay fox's shape and stop-motion texture are retained.
<Subject 4> (appears in [Shot 1], [Shot 2], [Shot 3], [Shot 4], [Shot 5]): fully_preserved - the silver wraparound frame and dark lenses are retained.
<Subject 5> (appears in [Shot 4]): fully_preserved - the white robotic arm and its black gripper are retained.
<Subject 6> (appears in [Shot 1]): fully_preserved - the low table and warm light of the dining room are retained.
<Subject 7> (appears in [Shot 5]): fully_preserved - the great window and the starfield of the observation deck are retained.
<Subject 8> (appears in [Shot 5]): weak_reference - the closing card follows its flat noir palette and lettering.

detailed_description:
The target video is a fast-cut commercial that changes visual style with each shot.
[Shot 1] A live-action medium shot. <Subject 1> sits down at the table of <Subject 6> and puts on <Subject 4>.
[Shot 2] At 00:01.000, the shot cuts to a white-cyclorama fashion studio, where <Subject 2> turns toward the camera wearing <Subject 4>.
[Shot 3] At 00:02.000, the shot cuts to stop-motion clay animation: <Subject 3> finds <Subject 4> on a mossy stump and tries them on.
[Shot 4] At 00:03.000, the shot cuts to a white table, where <Subject 5> lifts <Subject 4> and holds them up to the light.
[Shot 5] At 00:04.000, the shot cuts to <Subject 7>: a silhouetted captain slips on <Subject 4>, and the frame cuts to a title card in the style of <Subject 8>.

overall_soundscape:
Quick cuts carry a dinner murmur, a camera shutter, rustling leaves, a servo whir and a low starship hum.

non_diegetic_music:
A cool jazz bass line with brushed drums at a steady medium tempo.
```

### 9 images · 10 s request

243 frames · 24 FPS · stereo audio · matching prompt, references, seed and GPU count

**Base**
193.95 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-images9-10s-seed0.mp4).
](media/posters/base-images9-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-images9-10s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-images9-10s-seed0.mp4)

**FastH3 Omni**
30.80 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-images9-10s-seed0.mp4).
](media/posters/fast-images9-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-images9-10s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-images9-10s-seed0.mp4)

**FastH3 Omni · 36L VAE**
Quality comparison

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-images9-10s-seed0.mp4).
](media/posters/decoder36-images9-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-images9-10s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-images9-10s-seed0.mp4)

**6.30× lower latency** for this workload. 193.95 s → 30.80 s end to end (three-seed means).

Source references (9)

[![Picture 1 supplied to all three variants](media/inputs/square_character_action_reference.png)](media/inputs/square_character_action_reference.png)

Picture 1 · [original input](media/inputs/square_character_action_reference.png)

[![Picture 2 supplied to all three variants](media/inputs/square_official_fl2va_0_image.png)](media/inputs/square_official_fl2va_0_image.png)

Picture 2 · [original input](media/inputs/square_official_fl2va_0_image.png)

[![Picture 3 supplied to all three variants](media/inputs/square_fashion_glasses_reference_1.png)](media/inputs/square_fashion_glasses_reference_1.png)

Picture 3 · [original input](media/inputs/square_fashion_glasses_reference_1.png)

[![Picture 4 supplied to all three variants](media/inputs/square_fashion_glasses_reference_2.png)](media/inputs/square_fashion_glasses_reference_2.png)

Picture 4 · [original input](media/inputs/square_fashion_glasses_reference_2.png)

[![Picture 5 supplied to all three variants](media/inputs/square_fashion_glasses_reference_3.png)](media/inputs/square_fashion_glasses_reference_3.png)

Picture 5 · [original input](media/inputs/square_fashion_glasses_reference_3.png)

[![Picture 6 supplied to all three variants](media/inputs/square_fl2va_clay_fox_reference.png)](media/inputs/square_fl2va_clay_fox_reference.png)

Picture 6 · [original input](media/inputs/square_fl2va_clay_fox_reference.png)

[![Picture 7 supplied to all three variants](media/inputs/square_h3_cinematic_shot_3s.png)](media/inputs/square_h3_cinematic_shot_3s.png)

Picture 7 · [original input](media/inputs/square_h3_cinematic_shot_3s.png)

[![Picture 8 supplied to all three variants](media/inputs/square_h3_suspense_title_2s.png)](media/inputs/square_h3_suspense_title_2s.png)

Picture 8 · [original input](media/inputs/square_h3_suspense_title_2s.png)

[![Picture 9 supplied to all three variants](media/inputs/square_robot_arm_red_cube_1s.png)](media/inputs/square_robot_arm_red_cube_1s.png)

Picture 9 · [original input](media/inputs/square_robot_arm_red_cube_1s.png)

Full promptCopy full prompt

```
subject_definitions:
<Subject 1> is the young man with dark curly hair wearing a white T-shirt in <Picture 1>.
<Subject 2> is the model in the black sleeveless dress in <Picture 3> and <Picture 4>.
<Subject 3> is the clay fox in <Picture 6>.
<Subject 4> is the pair of silver wraparound sunglasses in <Picture 5>.
<Subject 5> is the white robotic arm in <Picture 9>.
<Subject 6> is the family dining room in <Picture 2>.
<Subject 7> is the starship observation deck in <Picture 7>.
<Subject 8> is the noir title-card style of <Picture 8>.

summary:
[reference generation] A five-shot sunglasses commercial cuts between a family dinner, a fashion studio, a clay forest, a robot lab and a starship deck, and ends on a noir title card.

retention_analysis:
<Subject 1> (appears in [Shot 1]): fully_preserved - the young man's face, dark curly hair and white T-shirt are retained.
<Subject 2> (appears in [Shot 2]): fully_preserved - the model's braided hair and black sleeveless dress are retained.
<Subject 3> (appears in [Shot 3]): fully_preserved - the clay fox's shape and stop-motion texture are retained.
<Subject 4> (appears in [Shot 1], [Shot 2], [Shot 3], [Shot 4], [Shot 5]): fully_preserved - the silver wraparound frame and dark lenses are retained.
<Subject 5> (appears in [Shot 4]): fully_preserved - the white robotic arm and its black gripper are retained.
<Subject 6> (appears in [Shot 1]): fully_preserved - the low table and warm light of the dining room are retained.
<Subject 7> (appears in [Shot 5]): fully_preserved - the great window and the starfield of the observation deck are retained.
<Subject 8> (appears in [Shot 5]): weak_reference - the closing card follows its flat noir palette and lettering.

detailed_description:
The target video is a fast-cut commercial that changes visual style with each shot.
[Shot 1] A live-action medium shot. <Subject 1> sits down at the table of <Subject 6> and puts on <Subject 4>.
[Shot 2] At 00:02.000, the shot cuts to a white-cyclorama fashion studio, where <Subject 2> turns toward the camera wearing <Subject 4>.
[Shot 3] At 00:04.000, the shot cuts to stop-motion clay animation: <Subject 3> finds <Subject 4> on a mossy stump and tries them on.
[Shot 4] At 00:06.000, the shot cuts to a white table, where <Subject 5> lifts <Subject 4> and holds them up to the light.
[Shot 5] At 00:08.000, the shot cuts to <Subject 7>: a silhouetted captain slips on <Subject 4>, and the frame cuts to a title card in the style of <Subject 8>.

overall_soundscape:
Quick cuts carry a dinner murmur, a camera shutter, rustling leaves, a servo whir and a low starship hum.

non_diegetic_music:
A cool jazz bass line with brushed drums at a steady medium tempo.
```

### 9 images · 15 s request

362 frames · 24 FPS · stereo audio · matching prompt, references, seed and GPU count

**Base**
282.81 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-images9-15s-seed0.mp4).
](media/posters/base-images9-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-images9-15s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-images9-15s-seed0.mp4)

**FastH3 Omni**
41.57 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-images9-15s-seed0.mp4).
](media/posters/fast-images9-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-images9-15s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-images9-15s-seed0.mp4)

**FastH3 Omni · 36L VAE**
Quality comparison

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-images9-15s-seed0.mp4).
](media/posters/decoder36-images9-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-images9-15s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-images9-15s-seed0.mp4)

**6.80× lower latency** for this workload. 282.81 s → 41.57 s end to end (three-seed means).

Source references (9)

[![Picture 1 supplied to all three variants](media/inputs/square_character_action_reference.png)](media/inputs/square_character_action_reference.png)

Picture 1 · [original input](media/inputs/square_character_action_reference.png)

[![Picture 2 supplied to all three variants](media/inputs/square_official_fl2va_0_image.png)](media/inputs/square_official_fl2va_0_image.png)

Picture 2 · [original input](media/inputs/square_official_fl2va_0_image.png)

[![Picture 3 supplied to all three variants](media/inputs/square_fashion_glasses_reference_1.png)](media/inputs/square_fashion_glasses_reference_1.png)

Picture 3 · [original input](media/inputs/square_fashion_glasses_reference_1.png)

[![Picture 4 supplied to all three variants](media/inputs/square_fashion_glasses_reference_2.png)](media/inputs/square_fashion_glasses_reference_2.png)

Picture 4 · [original input](media/inputs/square_fashion_glasses_reference_2.png)

[![Picture 5 supplied to all three variants](media/inputs/square_fashion_glasses_reference_3.png)](media/inputs/square_fashion_glasses_reference_3.png)

Picture 5 · [original input](media/inputs/square_fashion_glasses_reference_3.png)

[![Picture 6 supplied to all three variants](media/inputs/square_fl2va_clay_fox_reference.png)](media/inputs/square_fl2va_clay_fox_reference.png)

Picture 6 · [original input](media/inputs/square_fl2va_clay_fox_reference.png)

[![Picture 7 supplied to all three variants](media/inputs/square_h3_cinematic_shot_3s.png)](media/inputs/square_h3_cinematic_shot_3s.png)

Picture 7 · [original input](media/inputs/square_h3_cinematic_shot_3s.png)

[![Picture 8 supplied to all three variants](media/inputs/square_h3_suspense_title_2s.png)](media/inputs/square_h3_suspense_title_2s.png)

Picture 8 · [original input](media/inputs/square_h3_suspense_title_2s.png)

[![Picture 9 supplied to all three variants](media/inputs/square_robot_arm_red_cube_1s.png)](media/inputs/square_robot_arm_red_cube_1s.png)

Picture 9 · [original input](media/inputs/square_robot_arm_red_cube_1s.png)

Full promptCopy full prompt

```
subject_definitions:
<Subject 1> is the young man with dark curly hair wearing a white T-shirt in <Picture 1>.
<Subject 2> is the model in the black sleeveless dress in <Picture 3> and <Picture 4>.
<Subject 3> is the clay fox in <Picture 6>.
<Subject 4> is the pair of silver wraparound sunglasses in <Picture 5>.
<Subject 5> is the white robotic arm in <Picture 9>.
<Subject 6> is the family dining room in <Picture 2>.
<Subject 7> is the starship observation deck in <Picture 7>.
<Subject 8> is the noir title-card style of <Picture 8>.

summary:
[reference generation] A five-shot sunglasses commercial cuts between a family dinner, a fashion studio, a clay forest, a robot lab and a starship deck, and ends on a noir title card.

retention_analysis:
<Subject 1> (appears in [Shot 1]): fully_preserved - the young man's face, dark curly hair and white T-shirt are retained.
<Subject 2> (appears in [Shot 2]): fully_preserved - the model's braided hair and black sleeveless dress are retained.
<Subject 3> (appears in [Shot 3]): fully_preserved - the clay fox's shape and stop-motion texture are retained.
<Subject 4> (appears in [Shot 1], [Shot 2], [Shot 3], [Shot 4], [Shot 5]): fully_preserved - the silver wraparound frame and dark lenses are retained.
<Subject 5> (appears in [Shot 4]): fully_preserved - the white robotic arm and its black gripper are retained.
<Subject 6> (appears in [Shot 1]): fully_preserved - the low table and warm light of the dining room are retained.
<Subject 7> (appears in [Shot 5]): fully_preserved - the great window and the starfield of the observation deck are retained.
<Subject 8> (appears in [Shot 5]): weak_reference - the closing card follows its flat noir palette and lettering.

detailed_description:
The target video is a fast-cut commercial that changes visual style with each shot.
[Shot 1] A live-action medium shot. <Subject 1> sits down at the table of <Subject 6> and puts on <Subject 4>.
[Shot 2] At 00:03.000, the shot cuts to a white-cyclorama fashion studio, where <Subject 2> turns toward the camera wearing <Subject 4>.
[Shot 3] At 00:06.000, the shot cuts to stop-motion clay animation: <Subject 3> finds <Subject 4> on a mossy stump and tries them on.
[Shot 4] At 00:09.000, the shot cuts to a white table, where <Subject 5> lifts <Subject 4> and holds them up to the light.
[Shot 5] At 00:12.000, the shot cuts to <Subject 7>: a silhouetted captain slips on <Subject 4>, and the frame cuts to a title card in the style of <Subject 8>.

overall_soundscape:
Quick cuts carry a dinner murmur, a camera shutter, rustling leaves, a servo whir and a low starship hum.

non_diegetic_music:
A cool jazz bass line with brushed drums at a steady medium tempo.
```

### 1 short clip · 5 s request

124 frames · 24 FPS · stereo audio · matching prompt, references, seed and GPU count

**Base**
36.06 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-clip-5s-seed0.mp4).
](media/posters/base-clip-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-clip-5s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-clip-5s-seed0.mp4)

**FastH3 Omni**
5.17 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-clip-5s-seed0.mp4).
](media/posters/fast-clip-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-clip-5s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-clip-5s-seed0.mp4)

**FastH3 Omni · 36L VAE**
Quality comparison

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-clip-5s-seed0.mp4).
](media/posters/decoder36-clip-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-clip-5s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-clip-5s-seed0.mp4)

**6.98× lower latency** for this workload. 36.06 s → 5.17 s end to end (three-seed means).

Source references (1)

[
[Download video reference](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)

Video 1 · with original audio · [original input](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)

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

### 1 short clip · 10 s request

243 frames · 24 FPS · stereo audio · matching prompt, references, seed and GPU count

**Base**
79.73 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-clip-10s-seed0.mp4).
](media/posters/base-clip-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-clip-10s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-clip-10s-seed0.mp4)

**FastH3 Omni**
8.06 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-clip-10s-seed0.mp4).
](media/posters/fast-clip-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-clip-10s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-clip-10s-seed0.mp4)

**FastH3 Omni · 36L VAE**
Quality comparison

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-clip-10s-seed0.mp4).
](media/posters/decoder36-clip-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-clip-10s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-clip-10s-seed0.mp4)

**9.89× lower latency** for this workload. 79.73 s → 8.06 s end to end (three-seed means).

Source references (1)

[
[Download video reference](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)

Video 1 · with original audio · [original input](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)

Full promptCopy full prompt

```
subject_definitions:
<Subject 1> is the young man with short wavy blonde hair, wearing a bright pink suit jacket, matching pink trousers, an unbuttoned white shirt and silver rings, holding a small black lamb in his arms in <Video 1>.
<Subject 2> is the environment in <Video 1>: a grassy hill at golden hour with white lambs grazing.
<Audio 1> is the synchronized audio track of <Video 1>, a soft background music.

summary:
[reference generation + audio reference] <Subject 1> spends a quiet moment with the black lamb in <Subject 2>, over music in the manner of <Audio 1>.

retention_analysis:
<Subject 1> (appears in [Shot 1], [Shot 2]): fully_preserved - the man's blonde hair, pink suit, white shirt, rings and the black lamb are retained.
<Subject 2> (appears in [Shot 1], [Shot 2]): fully_preserved - the grassy hill, golden light and grazing lambs are retained.
<Audio 1>: reference - the soft background music is referenced throughout.

detailed_description:
The target video is in a realistic photographic style with golden-hour light.
[Shot 1] A steady medium shot. <Subject 1> cradles the black lamb in the warm, low sunlight of <Subject 2>. The lamb lifts its head and nuzzles his chin; he laughs softly, tilts his head toward the camera and grins while the white lambs keep grazing on the hill.
[Shot 2] At 00:05.000, the shot cuts to a wide shot from down the hill. <Subject 1> walks slowly through the flock with the black lamb in his arms, the white lambs parting around his legs and the long grass bending in the breeze.

overall_soundscape:
A light breeze over the grass and distant bleating, beneath gentle music in the manner of <Audio 1>.

non_diegetic_music:
N/A
```

### 1 short clip · 15 s request

362 frames · 24 FPS · stereo audio · matching prompt, references, seed and GPU count

**Base**
140.29 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-clip-15s-seed0.mp4).
](media/posters/base-clip-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-clip-15s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-clip-15s-seed0.mp4)

**FastH3 Omni**
11.76 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-clip-15s-seed0.mp4).
](media/posters/fast-clip-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-clip-15s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-clip-15s-seed0.mp4)

**FastH3 Omni · 36L VAE**
Quality comparison

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-clip-15s-seed0.mp4).
](media/posters/decoder36-clip-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-clip-15s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-clip-15s-seed0.mp4)

**11.93× lower latency** for this workload. 140.29 s → 11.76 s end to end (three-seed means).

Source references (1)

[
[Download video reference](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)

Video 1 · with original audio · [original input](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)

Full promptCopy full prompt

```
subject_definitions:
<Subject 1> is the young man with short wavy blonde hair, wearing a bright pink suit jacket, matching pink trousers, an unbuttoned white shirt and silver rings, holding a small black lamb in his arms in <Video 1>.
<Subject 2> is the environment in <Video 1>: a grassy hill at golden hour with white lambs grazing.
<Audio 1> is the synchronized audio track of <Video 1>, a soft background music.

summary:
[reference generation + audio reference] <Subject 1> spends a quiet moment with the black lamb in <Subject 2>, over music in the manner of <Audio 1>.

retention_analysis:
<Subject 1> (appears in [Shot 1], [Shot 2], [Shot 3]): fully_preserved - the man's blonde hair, pink suit, white shirt, rings and the black lamb are retained.
<Subject 2> (appears in [Shot 1], [Shot 2], [Shot 3]): fully_preserved - the grassy hill, golden light and grazing lambs are retained.
<Audio 1>: reference - the soft background music is referenced throughout.

detailed_description:
The target video is in a realistic photographic style with golden-hour light.
[Shot 1] A steady medium shot. <Subject 1> cradles the black lamb in the warm, low sunlight of <Subject 2>. The lamb lifts its head and nuzzles his chin; he laughs softly, tilts his head toward the camera and grins while the white lambs keep grazing on the hill.
[Shot 2] At 00:05.000, the shot cuts to a wide shot from down the hill. <Subject 1> walks slowly through the flock with the black lamb in his arms, the white lambs parting around his legs and the long grass bending in the breeze.
[Shot 3] At 00:10.000, the shot cuts to a close shot near the ground. <Subject 1> kneels and sets the black lamb down among the white lambs; it shakes its ears and trots off, and he watches it go with a smile, his rings catching the light.

overall_soundscape:
A light breeze over the grass and distant bleating, beneath gentle music in the manner of <Audio 1>.

non_diegetic_music:
N/A
```

### 1 long clip · 5 s request

124 frames · 24 FPS · stereo audio · matching prompt, references, seed and GPU count

**Base**
69.93 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-video-5s-seed0.mp4).
](media/posters/base-video-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-video-5s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-video-5s-seed0.mp4)

**FastH3 Omni**
8.34 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-video-5s-seed0.mp4).
](media/posters/fast-video-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-video-5s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-video-5s-seed0.mp4)

**FastH3 Omni · 36L VAE**
Quality comparison

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-video-5s-seed0.mp4).
](media/posters/decoder36-video-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-video-5s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-video-5s-seed0.mp4)

**8.39× lower latency** for this workload. 69.93 s → 8.34 s end to end (three-seed means).

Source references (1)

[
[Download video reference](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--official_ref2va_0_video.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--official_ref2va_0_video.mp4)

Video 1 · with original audio · [original input](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--official_ref2va_0_video.mp4)

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

### 1 long clip · 10 s request

243 frames · 24 FPS · stereo audio · matching prompt, references, seed and GPU count

**Base**
139.27 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-video-10s-seed0.mp4).
](media/posters/base-video-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-video-10s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-video-10s-seed0.mp4)

**FastH3 Omni**
13.51 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-video-10s-seed0.mp4).
](media/posters/fast-video-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-video-10s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-video-10s-seed0.mp4)

**FastH3 Omni · 36L VAE**
Quality comparison

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-video-10s-seed0.mp4).
](media/posters/decoder36-video-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-video-10s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-video-10s-seed0.mp4)

**10.31× lower latency** for this workload. 139.27 s → 13.51 s end to end (three-seed means).

Source references (1)

[
[Download video reference](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--official_ref2va_0_video.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--official_ref2va_0_video.mp4)

Video 1 · with original audio · [original input](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--official_ref2va_0_video.mp4)

Full promptCopy full prompt

```
subject_definitions:
<Subject 1> is the young man with short wavy blonde hair, wearing a bright pink suit jacket, matching pink trousers, an unbuttoned white shirt and silver rings, holding a small black lamb in his arms in <Video 1>.
<Subject 2> is the environment in <Video 1>: a grassy hill at golden hour with white lambs grazing.
<Audio 1> is the synchronized audio track of <Video 1>, a soft background music.

summary:
[reference generation + audio reference] <Subject 1> spends a quiet moment with the black lamb in <Subject 2>, over music in the manner of <Audio 1>.

retention_analysis:
<Subject 1> (appears in [Shot 1], [Shot 2]): fully_preserved - the man's blonde hair, pink suit, white shirt, rings and the black lamb are retained.
<Subject 2> (appears in [Shot 1], [Shot 2]): fully_preserved - the grassy hill, golden light and grazing lambs are retained.
<Audio 1>: reference - the soft background music is referenced throughout.

detailed_description:
The target video is in a realistic photographic style with golden-hour light.
[Shot 1] A steady medium shot. <Subject 1> cradles the black lamb in the warm, low sunlight of <Subject 2>. The lamb lifts its head and nuzzles his chin; he laughs softly, tilts his head toward the camera and grins while the white lambs keep grazing on the hill.
[Shot 2] At 00:05.000, the shot cuts to a wide shot from down the hill. <Subject 1> walks slowly through the flock with the black lamb in his arms, the white lambs parting around his legs and the long grass bending in the breeze.

overall_soundscape:
A light breeze over the grass and distant bleating, beneath gentle music in the manner of <Audio 1>.

non_diegetic_music:
N/A
```

### 1 long clip · 15 s request

362 frames · 24 FPS · stereo audio · matching prompt, references, seed and GPU count

**Base**
215.75 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-video-15s-seed0.mp4).
](media/posters/base-video-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-video-15s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-video-15s-seed0.mp4)

**FastH3 Omni**
18.41 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-video-15s-seed0.mp4).
](media/posters/fast-video-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-video-15s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-video-15s-seed0.mp4)

**FastH3 Omni · 36L VAE**
Quality comparison

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-video-15s-seed0.mp4).
](media/posters/decoder36-video-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-video-15s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-video-15s-seed0.mp4)

**11.72× lower latency** for this workload. 215.75 s → 18.41 s end to end (three-seed means).

Source references (1)

[
[Download video reference](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--official_ref2va_0_video.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--official_ref2va_0_video.mp4)

Video 1 · with original audio · [original input](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--official_ref2va_0_video.mp4)

Full promptCopy full prompt

```
subject_definitions:
<Subject 1> is the young man with short wavy blonde hair, wearing a bright pink suit jacket, matching pink trousers, an unbuttoned white shirt and silver rings, holding a small black lamb in his arms in <Video 1>.
<Subject 2> is the environment in <Video 1>: a grassy hill at golden hour with white lambs grazing.
<Audio 1> is the synchronized audio track of <Video 1>, a soft background music.

summary:
[reference generation + audio reference] <Subject 1> spends a quiet moment with the black lamb in <Subject 2>, over music in the manner of <Audio 1>.

retention_analysis:
<Subject 1> (appears in [Shot 1], [Shot 2], [Shot 3]): fully_preserved - the man's blonde hair, pink suit, white shirt, rings and the black lamb are retained.
<Subject 2> (appears in [Shot 1], [Shot 2], [Shot 3]): fully_preserved - the grassy hill, golden light and grazing lambs are retained.
<Audio 1>: reference - the soft background music is referenced throughout.

detailed_description:
The target video is in a realistic photographic style with golden-hour light.
[Shot 1] A steady medium shot. <Subject 1> cradles the black lamb in the warm, low sunlight of <Subject 2>. The lamb lifts its head and nuzzles his chin; he laughs softly, tilts his head toward the camera and grins while the white lambs keep grazing on the hill.
[Shot 2] At 00:05.000, the shot cuts to a wide shot from down the hill. <Subject 1> walks slowly through the flock with the black lamb in his arms, the white lambs parting around his legs and the long grass bending in the breeze.
[Shot 3] At 00:10.000, the shot cuts to a close shot near the ground. <Subject 1> kneels and sets the black lamb down among the white lambs; it shakes its ears and trots off, and he watches it go with a smile, his rings catching the light.

overall_soundscape:
A light breeze over the grass and distant bleating, beneath gentle music in the manner of <Audio 1>.

non_diegetic_music:
N/A
```

### 3 clips · 5 s request

124 frames · 24 FPS · stereo audio · matching prompt, references, seed and GPU count

**Base**
74.35 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-clips3-5s-seed0.mp4).
](media/posters/base-clips3-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-clips3-5s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-clips3-5s-seed0.mp4)

**FastH3 Omni**
9.45 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-clips3-5s-seed0.mp4).
](media/posters/fast-clips3-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-clips3-5s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-clips3-5s-seed0.mp4)

**FastH3 Omni · 36L VAE**
Quality comparison

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-clips3-5s-seed0.mp4).
](media/posters/decoder36-clips3-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-clips3-5s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-clips3-5s-seed0.mp4)

**7.87× lower latency** for this workload. 74.35 s → 9.45 s end to end (three-seed means).

Source references (3)

[
[Download video reference](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)

Video 1 · with original audio · [original input](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)

[
[Download video reference](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_robot_arm_red_cube_2s.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_robot_arm_red_cube_2s.mp4)

Video 2 · with original audio · [original input](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_robot_arm_red_cube_2s.mp4)

[
[Download video reference](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_h3_cinematic_shot_2s.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_h3_cinematic_shot_2s.mp4)

Video 3 · with original audio · [original input](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_h3_cinematic_shot_2s.mp4)

Full promptCopy full prompt

```
subject_definitions:
<Subject 1> is the young man with short wavy blonde hair, wearing a bright pink suit jacket, matching pink trousers, an unbuttoned white shirt and silver rings, holding a small black lamb in his arms in <Video 1>.
<Subject 2> is the white robotic arm with a black gripper in <Video 2>.
<Subject 3> is the dark starship observation deck in <Video 3>.
<Audio 1>, <Audio 2> and <Audio 3> are the synchronized audio tracks of <Video 1>, <Video 2> and <Video 3>.

summary:
[reference generation + audio reference] A three-shot sequence shows <Subject 1> in a golden pasture, <Subject 2> at work on a white table and the great window of <Subject 3>, with sound in the manner of <Audio 1>, <Audio 2> and <Audio 3>.

retention_analysis:
<Subject 1> (appears in [Shot 1]): fully_preserved - the man's blonde hair, pink suit and the black lamb are retained.
<Subject 2> (appears in [Shot 2]): fully_preserved - the white robotic arm and its black gripper are retained.
<Subject 3> (appears in [Shot 3]): fully_preserved - the dark deck, its great window and the starfield are retained.
<Audio 1>: reference - the pasture's soft music is referenced in the first shot.
<Audio 2>: reference - the servo whir is referenced in the second shot.
<Audio 3>: reference - the low starship hum is referenced in the third shot.

detailed_description:
The target video is in a realistic photographic style.
[Shot 1] <Subject 1> holds the black lamb in a golden pasture and looks up at the sky while soft music in the manner of <Audio 1> plays.
[Shot 2] At 00:01.667, the shot cuts to a white table, where <Subject 2> grips a red cube and drops it into a glass jar with a servo whir like <Audio 2>.
[Shot 3] At 00:03.333, the shot cuts to <Subject 3>: the camera pushes in toward the great window, where a fleet of ships drifts past the stars over a low hum like <Audio 3>.

overall_soundscape:
The pasture's soft music gives way to a servo whir and then a low starship hum.

non_diegetic_music:
N/A
```

### 3 clips · 10 s request

243 frames · 24 FPS · stereo audio · matching prompt, references, seed and GPU count

**Base**
132.62 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-clips3-10s-seed0.mp4).
](media/posters/base-clips3-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-clips3-10s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-clips3-10s-seed0.mp4)

**FastH3 Omni**
13.55 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-clips3-10s-seed0.mp4).
](media/posters/fast-clips3-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-clips3-10s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-clips3-10s-seed0.mp4)

**FastH3 Omni · 36L VAE**
Quality comparison

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-clips3-10s-seed0.mp4).
](media/posters/decoder36-clips3-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-clips3-10s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-clips3-10s-seed0.mp4)

**9.79× lower latency** for this workload. 132.62 s → 13.55 s end to end (three-seed means).

Source references (3)

[
[Download video reference](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)

Video 1 · with original audio · [original input](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)

[
[Download video reference](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_robot_arm_red_cube_2s.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_robot_arm_red_cube_2s.mp4)

Video 2 · with original audio · [original input](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_robot_arm_red_cube_2s.mp4)

[
[Download video reference](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_h3_cinematic_shot_2s.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_h3_cinematic_shot_2s.mp4)

Video 3 · with original audio · [original input](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_h3_cinematic_shot_2s.mp4)

Full promptCopy full prompt

```
subject_definitions:
<Subject 1> is the young man with short wavy blonde hair, wearing a bright pink suit jacket, matching pink trousers, an unbuttoned white shirt and silver rings, holding a small black lamb in his arms in <Video 1>.
<Subject 2> is the white robotic arm with a black gripper in <Video 2>.
<Subject 3> is the dark starship observation deck in <Video 3>.
<Audio 1>, <Audio 2> and <Audio 3> are the synchronized audio tracks of <Video 1>, <Video 2> and <Video 3>.

summary:
[reference generation + audio reference] A three-shot sequence shows <Subject 1> in a golden pasture, <Subject 2> at work on a white table and the great window of <Subject 3>, with sound in the manner of <Audio 1>, <Audio 2> and <Audio 3>.

retention_analysis:
<Subject 1> (appears in [Shot 1]): fully_preserved - the man's blonde hair, pink suit and the black lamb are retained.
<Subject 2> (appears in [Shot 2]): fully_preserved - the white robotic arm and its black gripper are retained.
<Subject 3> (appears in [Shot 3]): fully_preserved - the dark deck, its great window and the starfield are retained.
<Audio 1>: reference - the pasture's soft music is referenced in the first shot.
<Audio 2>: reference - the servo whir is referenced in the second shot.
<Audio 3>: reference - the low starship hum is referenced in the third shot.

detailed_description:
The target video is in a realistic photographic style.
[Shot 1] <Subject 1> holds the black lamb in a golden pasture and looks up at the sky while soft music in the manner of <Audio 1> plays.
[Shot 2] At 00:03.333, the shot cuts to a white table, where <Subject 2> grips a red cube and drops it into a glass jar with a servo whir like <Audio 2>.
[Shot 3] At 00:06.667, the shot cuts to <Subject 3>: the camera pushes in toward the great window, where a fleet of ships drifts past the stars over a low hum like <Audio 3>.

overall_soundscape:
The pasture's soft music gives way to a servo whir and then a low starship hum.

non_diegetic_music:
N/A
```

### 3 clips · 15 s request

362 frames · 24 FPS · stereo audio · matching prompt, references, seed and GPU count

**Base**
206.44 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-clips3-15s-seed0.mp4).
](media/posters/base-clips3-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-clips3-15s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-clips3-15s-seed0.mp4)

**FastH3 Omni**
18.38 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-clips3-15s-seed0.mp4).
](media/posters/fast-clips3-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-clips3-15s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-clips3-15s-seed0.mp4)

**FastH3 Omni · 36L VAE**
Quality comparison

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-clips3-15s-seed0.mp4).
](media/posters/decoder36-clips3-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-clips3-15s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-clips3-15s-seed0.mp4)

**11.23× lower latency** for this workload. 206.44 s → 18.38 s end to end (three-seed means).

Source references (3)

[
[Download video reference](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)

Video 1 · with original audio · [original input](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)

[
[Download video reference](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_robot_arm_red_cube_2s.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_robot_arm_red_cube_2s.mp4)

Video 2 · with original audio · [original input](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_robot_arm_red_cube_2s.mp4)

[
[Download video reference](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_h3_cinematic_shot_2s.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_h3_cinematic_shot_2s.mp4)

Video 3 · with original audio · [original input](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_h3_cinematic_shot_2s.mp4)

Full promptCopy full prompt

```
subject_definitions:
<Subject 1> is the young man with short wavy blonde hair, wearing a bright pink suit jacket, matching pink trousers, an unbuttoned white shirt and silver rings, holding a small black lamb in his arms in <Video 1>.
<Subject 2> is the white robotic arm with a black gripper in <Video 2>.
<Subject 3> is the dark starship observation deck in <Video 3>.
<Audio 1>, <Audio 2> and <Audio 3> are the synchronized audio tracks of <Video 1>, <Video 2> and <Video 3>.

summary:
[reference generation + audio reference] A three-shot sequence shows <Subject 1> in a golden pasture, <Subject 2> at work on a white table and the great window of <Subject 3>, with sound in the manner of <Audio 1>, <Audio 2> and <Audio 3>.

retention_analysis:
<Subject 1> (appears in [Shot 1]): fully_preserved - the man's blonde hair, pink suit and the black lamb are retained.
<Subject 2> (appears in [Shot 2]): fully_preserved - the white robotic arm and its black gripper are retained.
<Subject 3> (appears in [Shot 3]): fully_preserved - the dark deck, its great window and the starfield are retained.
<Audio 1>: reference - the pasture's soft music is referenced in the first shot.
<Audio 2>: reference - the servo whir is referenced in the second shot.
<Audio 3>: reference - the low starship hum is referenced in the third shot.

detailed_description:
The target video is in a realistic photographic style.
[Shot 1] <Subject 1> holds the black lamb in a golden pasture and looks up at the sky while soft music in the manner of <Audio 1> plays.
[Shot 2] At 00:05.000, the shot cuts to a white table, where <Subject 2> grips a red cube and drops it into a glass jar with a servo whir like <Audio 2>.
[Shot 3] At 00:10.000, the shot cuts to <Subject 3>: the camera pushes in toward the great window, where a fleet of ships drifts past the stars over a low hum like <Audio 3>.

overall_soundscape:
The pasture's soft music gives way to a servo whir and then a low starship hum.

non_diegetic_music:
N/A
```

### Image + video + voice · 5 s request

124 frames · 24 FPS · stereo audio · matching prompt, references, seed and GPU count

**Base**
94.14 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-mixed-5s-seed0.mp4).
](media/posters/base-mixed-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-mixed-5s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-mixed-5s-seed0.mp4)

**FastH3 Omni**
13.06 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-mixed-5s-seed0.mp4).
](media/posters/fast-mixed-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-mixed-5s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-mixed-5s-seed0.mp4)

**FastH3 Omni · 36L VAE**
Quality comparison

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-mixed-5s-seed0.mp4).
](media/posters/decoder36-mixed-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-mixed-5s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-mixed-5s-seed0.mp4)

**7.21× lower latency** for this workload. 94.14 s → 13.06 s end to end (three-seed means).

Source references (3)

[![Picture 1 supplied to all three variants](media/inputs/hf_character_action_reference.png)](media/inputs/hf_character_action_reference.png)

Picture 1 · [original input](media/inputs/hf_character_action_reference.png)

[
[Download video reference](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--official_ref2va_0_video.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--official_ref2va_0_video.mp4)

Video 1 · with original audio · [original input](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--official_ref2va_0_video.mp4)

[Download audio reference](media/inputs/official_ref2va_1_audio.mp3)

Audio 1 · [original input](media/inputs/official_ref2va_1_audio.mp3)

Full promptCopy full prompt

```
subject_definitions:
<Subject 1> is the young man with dark curly hair wearing a white T-shirt in <Picture 1>.
<Subject 2> is the young man with short wavy blonde hair, wearing a bright pink suit jacket, matching pink trousers, an unbuttoned white shirt and silver rings, holding a small black lamb in his arms in <Video 1>.
<Subject 3> is the environment in <Video 1>: a grassy hill at golden hour with white lambs grazing.
<Audio 1> is the synchronized audio track of <Video 1>, a soft background music.
<Audio 2> is the voice-timbre reference for <Subject 1> (S1).

summary:
[reference generation + audio reference] <Subject 1> walks into <Subject 3> and greets <Subject 2>, speaking in the voice timbre of <Audio 2> over music in the manner of <Audio 1>.

retention_analysis:
<Subject 1> (appears in [Shot 1]): fully_preserved - the young man's face, dark curly hair and white T-shirt are retained.
<Subject 2> (appears in [Shot 1]): fully_preserved - the man's blonde hair, pink suit and the black lamb are retained.
<Subject 3> (appears in [Shot 1]): fully_preserved - the grassy hill, golden light and grazing lambs are retained.
<Audio 1>: reference - the soft background music is referenced beneath the dialogue.
<Audio 2>: reference - its vocal timbre guides the dialogue delivery of <Subject 1> without copying the original signal.

detailed_description:
The target video is in a realistic photographic style with golden-hour light.
[Shot 1] A steady medium shot of <Subject 3>. <Subject 2> cradles the black lamb in the warm sunlight as <Subject 1> (S1) steps into frame from the left, waves and says, using the voice timbre referenced from <Audio 2>, <d>[English] There you are, the whole farm is looking for that lamb.</d> <Subject 2> laughs and lifts the lamb a little higher.

overall_soundscape:
A light breeze over the grass, distant bleating and soft footsteps, beneath gentle music in the manner of <Audio 1>.

non_diegetic_music:
N/A
```

### Image + video + voice · 10 s request

243 frames · 24 FPS · stereo audio · matching prompt, references, seed and GPU count

**Base**
172.37 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-mixed-10s-seed0.mp4).
](media/posters/base-mixed-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-mixed-10s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-mixed-10s-seed0.mp4)

**FastH3 Omni**
19.75 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-mixed-10s-seed0.mp4).
](media/posters/fast-mixed-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-mixed-10s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-mixed-10s-seed0.mp4)

**FastH3 Omni · 36L VAE**
Quality comparison

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-mixed-10s-seed0.mp4).
](media/posters/decoder36-mixed-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-mixed-10s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-mixed-10s-seed0.mp4)

**8.73× lower latency** for this workload. 172.37 s → 19.75 s end to end (three-seed means).

Source references (3)

[![Picture 1 supplied to all three variants](media/inputs/hf_character_action_reference.png)](media/inputs/hf_character_action_reference.png)

Picture 1 · [original input](media/inputs/hf_character_action_reference.png)

[
[Download video reference](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--official_ref2va_0_video.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--official_ref2va_0_video.mp4)

Video 1 · with original audio · [original input](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--official_ref2va_0_video.mp4)

[Download audio reference](media/inputs/official_ref2va_1_audio.mp3)

Audio 1 · [original input](media/inputs/official_ref2va_1_audio.mp3)

Full promptCopy full prompt

```
subject_definitions:
<Subject 1> is the young man with dark curly hair wearing a white T-shirt in <Picture 1>.
<Subject 2> is the young man with short wavy blonde hair, wearing a bright pink suit jacket, matching pink trousers, an unbuttoned white shirt and silver rings, holding a small black lamb in his arms in <Video 1>.
<Subject 3> is the environment in <Video 1>: a grassy hill at golden hour with white lambs grazing.
<Audio 1> is the synchronized audio track of <Video 1>, a soft background music.
<Audio 2> is the voice-timbre reference for <Subject 1> (S1).

summary:
[reference generation + audio reference] <Subject 1> walks into <Subject 3> and greets <Subject 2>, speaking in the voice timbre of <Audio 2> over music in the manner of <Audio 1>.

retention_analysis:
<Subject 1> (appears in [Shot 1], [Shot 2]): fully_preserved - the young man's face, dark curly hair and white T-shirt are retained.
<Subject 2> (appears in [Shot 1], [Shot 2]): fully_preserved - the man's blonde hair, pink suit and the black lamb are retained.
<Subject 3> (appears in [Shot 1], [Shot 2]): fully_preserved - the grassy hill, golden light and grazing lambs are retained.
<Audio 1>: reference - the soft background music is referenced beneath the dialogue.
<Audio 2>: reference - its vocal timbre guides the dialogue delivery of <Subject 1> without copying the original signal.

detailed_description:
The target video is in a realistic photographic style with golden-hour light.
[Shot 1] A steady medium shot of <Subject 3>. <Subject 2> cradles the black lamb in the warm sunlight as <Subject 1> (S1) steps into frame from the left, waves and says, using the voice timbre referenced from <Audio 2>, <d>[English] There you are, the whole farm is looking for that lamb.</d> <Subject 2> laughs and lifts the lamb a little higher.
[Shot 2] At 00:05.000, the shot cuts to a two-shot from the side. <Subject 1> (S1) reaches out and scratches the lamb behind its ears and says in the same voice, <d>[English] He looks far too comfortable to come home.</d> <Subject 2> grins and shakes his head while the white lambs graze behind them.

overall_soundscape:
A light breeze over the grass, distant bleating and soft footsteps, beneath gentle music in the manner of <Audio 1>.

non_diegetic_music:
N/A
```

### Image + video + voice · 15 s request

362 frames · 24 FPS · stereo audio · matching prompt, references, seed and GPU count

**Base**
257.71 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-mixed-15s-seed0.mp4).
](media/posters/base-mixed-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-mixed-15s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-mixed-15s-seed0.mp4)

**FastH3 Omni**
26.71 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-mixed-15s-seed0.mp4).
](media/posters/fast-mixed-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-mixed-15s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-mixed-15s-seed0.mp4)

**FastH3 Omni · 36L VAE**
Quality comparison

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-mixed-15s-seed0.mp4).
](media/posters/decoder36-mixed-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-mixed-15s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-mixed-15s-seed0.mp4)

**9.65× lower latency** for this workload. 257.71 s → 26.71 s end to end (three-seed means).

Source references (3)

[![Picture 1 supplied to all three variants](media/inputs/hf_character_action_reference.png)](media/inputs/hf_character_action_reference.png)

Picture 1 · [original input](media/inputs/hf_character_action_reference.png)

[
[Download video reference](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--official_ref2va_0_video.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--official_ref2va_0_video.mp4)

Video 1 · with original audio · [original input](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--official_ref2va_0_video.mp4)

[Download audio reference](media/inputs/official_ref2va_1_audio.mp3)

Audio 1 · [original input](media/inputs/official_ref2va_1_audio.mp3)

Full promptCopy full prompt

```
subject_definitions:
<Subject 1> is the young man with dark curly hair wearing a white T-shirt in <Picture 1>.
<Subject 2> is the young man with short wavy blonde hair, wearing a bright pink suit jacket, matching pink trousers, an unbuttoned white shirt and silver rings, holding a small black lamb in his arms in <Video 1>.
<Subject 3> is the environment in <Video 1>: a grassy hill at golden hour with white lambs grazing.
<Audio 1> is the synchronized audio track of <Video 1>, a soft background music.
<Audio 2> is the voice-timbre reference for <Subject 1> (S1).

summary:
[reference generation + audio reference] <Subject 1> walks into <Subject 3> and greets <Subject 2>, speaking in the voice timbre of <Audio 2> over music in the manner of <Audio 1>.

retention_analysis:
<Subject 1> (appears in [Shot 1], [Shot 2], [Shot 3]): fully_preserved - the young man's face, dark curly hair and white T-shirt are retained.
<Subject 2> (appears in [Shot 1], [Shot 2], [Shot 3]): fully_preserved - the man's blonde hair, pink suit and the black lamb are retained.
<Subject 3> (appears in [Shot 1], [Shot 2], [Shot 3]): fully_preserved - the grassy hill, golden light and grazing lambs are retained.
<Audio 1>: reference - the soft background music is referenced beneath the dialogue.
<Audio 2>: reference - its vocal timbre guides the dialogue delivery of <Subject 1> without copying the original signal.

detailed_description:
The target video is in a realistic photographic style with golden-hour light.
[Shot 1] A steady medium shot of <Subject 3>. <Subject 2> cradles the black lamb in the warm sunlight as <Subject 1> (S1) steps into frame from the left, waves and says, using the voice timbre referenced from <Audio 2>, <d>[English] There you are, the whole farm is looking for that lamb.</d> <Subject 2> laughs and lifts the lamb a little higher.
[Shot 2] At 00:05.000, the shot cuts to a two-shot from the side. <Subject 1> (S1) reaches out and scratches the lamb behind its ears and says in the same voice, <d>[English] He looks far too comfortable to come home.</d> <Subject 2> grins and shakes his head while the white lambs graze behind them.
[Shot 3] At 00:10.000, the shot cuts to a wide shot from down the hill. <Subject 1> and <Subject 2> walk side by side toward the camera through the flock, the black lamb still in <Subject 2>'s arms, their long shadows stretching across the grass.

overall_soundscape:
A light breeze over the grass, distant bleating and soft footsteps, beneath gentle music in the manner of <Audio 1>.

non_diegetic_music:
N/A
```

### 9 images + 3 clips · 5 s request

124 frames · 24 FPS · stereo audio · matching prompt, references, seed and GPU count

**Base**
219.90 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-full-5s-seed0.mp4).
](media/posters/base-full-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-full-5s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-full-5s-seed0.mp4)

**FastH3 Omni**
37.38 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-full-5s-seed0.mp4).
](media/posters/fast-full-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-full-5s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-full-5s-seed0.mp4)

**FastH3 Omni · 36L VAE**
Quality comparison

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-full-5s-seed0.mp4).
](media/posters/decoder36-full-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-full-5s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-full-5s-seed0.mp4)

**5.88× lower latency** for this workload. 219.90 s → 37.38 s end to end (three-seed means).

Source references (12)

[![Picture 1 supplied to all three variants](media/inputs/square_character_action_reference.png)](media/inputs/square_character_action_reference.png)

Picture 1 · [original input](media/inputs/square_character_action_reference.png)

[![Picture 2 supplied to all three variants](media/inputs/square_official_fl2va_0_image.png)](media/inputs/square_official_fl2va_0_image.png)

Picture 2 · [original input](media/inputs/square_official_fl2va_0_image.png)

[![Picture 3 supplied to all three variants](media/inputs/square_fashion_glasses_reference_1.png)](media/inputs/square_fashion_glasses_reference_1.png)

Picture 3 · [original input](media/inputs/square_fashion_glasses_reference_1.png)

[![Picture 4 supplied to all three variants](media/inputs/square_fashion_glasses_reference_2.png)](media/inputs/square_fashion_glasses_reference_2.png)

Picture 4 · [original input](media/inputs/square_fashion_glasses_reference_2.png)

[![Picture 5 supplied to all three variants](media/inputs/square_fashion_glasses_reference_3.png)](media/inputs/square_fashion_glasses_reference_3.png)

Picture 5 · [original input](media/inputs/square_fashion_glasses_reference_3.png)

[![Picture 6 supplied to all three variants](media/inputs/square_fl2va_clay_fox_reference.png)](media/inputs/square_fl2va_clay_fox_reference.png)

Picture 6 · [original input](media/inputs/square_fl2va_clay_fox_reference.png)

[![Picture 7 supplied to all three variants](media/inputs/square_h3_cinematic_shot_3s.png)](media/inputs/square_h3_cinematic_shot_3s.png)

Picture 7 · [original input](media/inputs/square_h3_cinematic_shot_3s.png)

[![Picture 8 supplied to all three variants](media/inputs/square_h3_suspense_title_2s.png)](media/inputs/square_h3_suspense_title_2s.png)

Picture 8 · [original input](media/inputs/square_h3_suspense_title_2s.png)

[![Picture 9 supplied to all three variants](media/inputs/square_robot_arm_red_cube_1s.png)](media/inputs/square_robot_arm_red_cube_1s.png)

Picture 9 · [original input](media/inputs/square_robot_arm_red_cube_1s.png)

[
[Download video reference](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)

Video 1 · with original audio · [original input](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)

[
[Download video reference](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_robot_arm_red_cube_2s.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_robot_arm_red_cube_2s.mp4)

Video 2 · with original audio · [original input](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_robot_arm_red_cube_2s.mp4)

[
[Download video reference](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_h3_cinematic_shot_2s.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_h3_cinematic_shot_2s.mp4)

Video 3 · with original audio · [original input](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_h3_cinematic_shot_2s.mp4)

Full promptCopy full prompt

```
subject_definitions:
<Subject 1> is the young man with dark curly hair wearing a white T-shirt in <Picture 1>.
<Subject 2> is the model in the black sleeveless dress in <Picture 3> and <Picture 4>.
<Subject 3> is the clay fox in <Picture 6>.
<Subject 4> is the pair of silver wraparound sunglasses in <Picture 5>.
<Subject 5> is the white robotic arm in <Picture 9> and <Video 2>.
<Subject 6> is the family dining room in <Picture 2>.
<Subject 7> is the starship observation deck in <Picture 7> and <Video 3>.
<Subject 8> is the noir title-card style of <Picture 8>.
<Subject 9> is the young man with short wavy blonde hair, wearing a bright pink suit jacket, matching pink trousers, an unbuttoned white shirt and silver rings, holding a small black lamb in his arms in <Video 1>.
<Audio 1>, <Audio 2> and <Audio 3> are the synchronized audio tracks of <Video 1>, <Video 2> and <Video 3>.

summary:
[reference generation + audio reference] A six-shot sunglasses commercial cuts between a family dinner, a fashion studio, a clay forest, a golden pasture, a robot lab and a starship deck, and ends on a noir title card.

retention_analysis:
<Subject 1> (appears in [Shot 1]): fully_preserved - the young man's face, dark curly hair and white T-shirt are retained.
<Subject 2> (appears in [Shot 2]): fully_preserved - the model's braided hair and black sleeveless dress are retained.
<Subject 3> (appears in [Shot 3]): fully_preserved - the clay fox's shape and stop-motion texture are retained.
<Subject 4> (appears in [Shot 1], [Shot 2], [Shot 3], [Shot 4], [Shot 5], [Shot 6]): fully_preserved - the silver wraparound frame and dark lenses are retained.
<Subject 5> (appears in [Shot 5]): fully_preserved - the white robotic arm and its motion are retained.
<Subject 6> (appears in [Shot 1]): fully_preserved - the low table and warm light of the dining room are retained.
<Subject 7> (appears in [Shot 6]): fully_preserved - the great window and the drifting fleet are retained.
<Subject 8> (appears in [Shot 6]): weak_reference - the closing card follows its flat noir palette and lettering.
<Subject 9> (appears in [Shot 4]): fully_preserved - the man's blonde hair, pink suit and the black lamb are retained.
<Audio 1>: reference - the pasture's soft music is referenced in the fourth shot.
<Audio 2>: reference - the servo whir is referenced in the fifth shot.
<Audio 3>: reference - the low starship hum is referenced in the sixth shot.

detailed_description:
The target video is a fast-cut commercial that changes visual style with each shot.
[Shot 1] A live-action medium shot. <Subject 1> sits down at the table of <Subject 6> and puts on <Subject 4>.
[Shot 2] At 00:00.833, the shot cuts to a white-cyclorama fashion studio, where <Subject 2> turns toward the camera wearing <Subject 4>.
[Shot 3] At 00:01.667, the shot cuts to stop-motion clay animation: <Subject 3> finds <Subject 4> on a mossy stump and tries them on.
[Shot 4] At 00:02.500, the shot cuts to a golden pasture, where <Subject 9> slides <Subject 4> onto his nose with one hand while holding the black lamb, over soft music in the manner of <Audio 1>.
[Shot 5] At 00:03.333, the shot cuts to a white table, where <Subject 5> lifts <Subject 4> and holds them up to the light with a servo whir like <Audio 2>.
[Shot 6] At 00:04.167, the shot cuts to <Subject 7>: a silhouetted captain slips on <Subject 4> before the great window over a low hum like <Audio 3>, and the frame cuts to a title card in the style of <Subject 8>.

overall_soundscape:
Quick cuts carry a dinner murmur, a camera shutter, rustling leaves, a breeze over grass, a servo whir and a low starship hum.

non_diegetic_music:
A cool jazz bass line with brushed drums at a steady medium tempo.
```

### 9 images + 3 clips · 10 s request

243 frames · 24 FPS · stereo audio · matching prompt, references, seed and GPU count

**Base**
314.16 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-full-10s-seed0.mp4).
](media/posters/base-full-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-full-10s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-full-10s-seed0.mp4)

**FastH3 Omni**
48.38 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-full-10s-seed0.mp4).
](media/posters/fast-full-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-full-10s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-full-10s-seed0.mp4)

**FastH3 Omni · 36L VAE**
Quality comparison

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-full-10s-seed0.mp4).
](media/posters/decoder36-full-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-full-10s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-full-10s-seed0.mp4)

**6.49× lower latency** for this workload. 314.16 s → 48.38 s end to end (three-seed means).

Source references (12)

[![Picture 1 supplied to all three variants](media/inputs/square_character_action_reference.png)](media/inputs/square_character_action_reference.png)

Picture 1 · [original input](media/inputs/square_character_action_reference.png)

[![Picture 2 supplied to all three variants](media/inputs/square_official_fl2va_0_image.png)](media/inputs/square_official_fl2va_0_image.png)

Picture 2 · [original input](media/inputs/square_official_fl2va_0_image.png)

[![Picture 3 supplied to all three variants](media/inputs/square_fashion_glasses_reference_1.png)](media/inputs/square_fashion_glasses_reference_1.png)

Picture 3 · [original input](media/inputs/square_fashion_glasses_reference_1.png)

[![Picture 4 supplied to all three variants](media/inputs/square_fashion_glasses_reference_2.png)](media/inputs/square_fashion_glasses_reference_2.png)

Picture 4 · [original input](media/inputs/square_fashion_glasses_reference_2.png)

[![Picture 5 supplied to all three variants](media/inputs/square_fashion_glasses_reference_3.png)](media/inputs/square_fashion_glasses_reference_3.png)

Picture 5 · [original input](media/inputs/square_fashion_glasses_reference_3.png)

[![Picture 6 supplied to all three variants](media/inputs/square_fl2va_clay_fox_reference.png)](media/inputs/square_fl2va_clay_fox_reference.png)

Picture 6 · [original input](media/inputs/square_fl2va_clay_fox_reference.png)

[![Picture 7 supplied to all three variants](media/inputs/square_h3_cinematic_shot_3s.png)](media/inputs/square_h3_cinematic_shot_3s.png)

Picture 7 · [original input](media/inputs/square_h3_cinematic_shot_3s.png)

[![Picture 8 supplied to all three variants](media/inputs/square_h3_suspense_title_2s.png)](media/inputs/square_h3_suspense_title_2s.png)

Picture 8 · [original input](media/inputs/square_h3_suspense_title_2s.png)

[![Picture 9 supplied to all three variants](media/inputs/square_robot_arm_red_cube_1s.png)](media/inputs/square_robot_arm_red_cube_1s.png)

Picture 9 · [original input](media/inputs/square_robot_arm_red_cube_1s.png)

[
[Download video reference](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)

Video 1 · with original audio · [original input](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)

[
[Download video reference](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_robot_arm_red_cube_2s.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_robot_arm_red_cube_2s.mp4)

Video 2 · with original audio · [original input](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_robot_arm_red_cube_2s.mp4)

[
[Download video reference](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_h3_cinematic_shot_2s.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_h3_cinematic_shot_2s.mp4)

Video 3 · with original audio · [original input](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_h3_cinematic_shot_2s.mp4)

Full promptCopy full prompt

```
subject_definitions:
<Subject 1> is the young man with dark curly hair wearing a white T-shirt in <Picture 1>.
<Subject 2> is the model in the black sleeveless dress in <Picture 3> and <Picture 4>.
<Subject 3> is the clay fox in <Picture 6>.
<Subject 4> is the pair of silver wraparound sunglasses in <Picture 5>.
<Subject 5> is the white robotic arm in <Picture 9> and <Video 2>.
<Subject 6> is the family dining room in <Picture 2>.
<Subject 7> is the starship observation deck in <Picture 7> and <Video 3>.
<Subject 8> is the noir title-card style of <Picture 8>.
<Subject 9> is the young man with short wavy blonde hair, wearing a bright pink suit jacket, matching pink trousers, an unbuttoned white shirt and silver rings, holding a small black lamb in his arms in <Video 1>.
<Audio 1>, <Audio 2> and <Audio 3> are the synchronized audio tracks of <Video 1>, <Video 2> and <Video 3>.

summary:
[reference generation + audio reference] A six-shot sunglasses commercial cuts between a family dinner, a fashion studio, a clay forest, a golden pasture, a robot lab and a starship deck, and ends on a noir title card.

retention_analysis:
<Subject 1> (appears in [Shot 1]): fully_preserved - the young man's face, dark curly hair and white T-shirt are retained.
<Subject 2> (appears in [Shot 2]): fully_preserved - the model's braided hair and black sleeveless dress are retained.
<Subject 3> (appears in [Shot 3]): fully_preserved - the clay fox's shape and stop-motion texture are retained.
<Subject 4> (appears in [Shot 1], [Shot 2], [Shot 3], [Shot 4], [Shot 5], [Shot 6]): fully_preserved - the silver wraparound frame and dark lenses are retained.
<Subject 5> (appears in [Shot 5]): fully_preserved - the white robotic arm and its motion are retained.
<Subject 6> (appears in [Shot 1]): fully_preserved - the low table and warm light of the dining room are retained.
<Subject 7> (appears in [Shot 6]): fully_preserved - the great window and the drifting fleet are retained.
<Subject 8> (appears in [Shot 6]): weak_reference - the closing card follows its flat noir palette and lettering.
<Subject 9> (appears in [Shot 4]): fully_preserved - the man's blonde hair, pink suit and the black lamb are retained.
<Audio 1>: reference - the pasture's soft music is referenced in the fourth shot.
<Audio 2>: reference - the servo whir is referenced in the fifth shot.
<Audio 3>: reference - the low starship hum is referenced in the sixth shot.

detailed_description:
The target video is a fast-cut commercial that changes visual style with each shot.
[Shot 1] A live-action medium shot. <Subject 1> sits down at the table of <Subject 6> and puts on <Subject 4>.
[Shot 2] At 00:01.667, the shot cuts to a white-cyclorama fashion studio, where <Subject 2> turns toward the camera wearing <Subject 4>.
[Shot 3] At 00:03.333, the shot cuts to stop-motion clay animation: <Subject 3> finds <Subject 4> on a mossy stump and tries them on.
[Shot 4] At 00:05.000, the shot cuts to a golden pasture, where <Subject 9> slides <Subject 4> onto his nose with one hand while holding the black lamb, over soft music in the manner of <Audio 1>.
[Shot 5] At 00:06.667, the shot cuts to a white table, where <Subject 5> lifts <Subject 4> and holds them up to the light with a servo whir like <Audio 2>.
[Shot 6] At 00:08.333, the shot cuts to <Subject 7>: a silhouetted captain slips on <Subject 4> before the great window over a low hum like <Audio 3>, and the frame cuts to a title card in the style of <Subject 8>.

overall_soundscape:
Quick cuts carry a dinner murmur, a camera shutter, rustling leaves, a breeze over grass, a servo whir and a low starship hum.

non_diegetic_music:
A cool jazz bass line with brushed drums at a steady medium tempo.
```

### 9 images + 3 clips · 15 s request

362 frames · 24 FPS · stereo audio · matching prompt, references, seed and GPU count

**Base**
422.20 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-full-15s-seed0.mp4).
](media/posters/base-full-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-full-15s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-full-15s-seed0.mp4)

**FastH3 Omni**
59.77 s mean latency

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-full-15s-seed0.mp4).
](media/posters/fast-full-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-full-15s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-full-15s-seed0.mp4)

**FastH3 Omni · 36L VAE**
Quality comparison

[![
[Download MP4 with audio](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-full-15s-seed0.mp4).
](media/posters/decoder36-full-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-full-15s-seed0.mp4)
[Download MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-full-15s-seed0.mp4)

**7.06× lower latency** for this workload. 422.20 s → 59.77 s end to end (three-seed means).

Source references (12)

[![Picture 1 supplied to all three variants](media/inputs/square_character_action_reference.png)](media/inputs/square_character_action_reference.png)

Picture 1 · [original input](media/inputs/square_character_action_reference.png)

[![Picture 2 supplied to all three variants](media/inputs/square_official_fl2va_0_image.png)](media/inputs/square_official_fl2va_0_image.png)

Picture 2 · [original input](media/inputs/square_official_fl2va_0_image.png)

[![Picture 3 supplied to all three variants](media/inputs/square_fashion_glasses_reference_1.png)](media/inputs/square_fashion_glasses_reference_1.png)

Picture 3 · [original input](media/inputs/square_fashion_glasses_reference_1.png)

[![Picture 4 supplied to all three variants](media/inputs/square_fashion_glasses_reference_2.png)](media/inputs/square_fashion_glasses_reference_2.png)

Picture 4 · [original input](media/inputs/square_fashion_glasses_reference_2.png)

[![Picture 5 supplied to all three variants](media/inputs/square_fashion_glasses_reference_3.png)](media/inputs/square_fashion_glasses_reference_3.png)

Picture 5 · [original input](media/inputs/square_fashion_glasses_reference_3.png)

[![Picture 6 supplied to all three variants](media/inputs/square_fl2va_clay_fox_reference.png)](media/inputs/square_fl2va_clay_fox_reference.png)

Picture 6 · [original input](media/inputs/square_fl2va_clay_fox_reference.png)

[![Picture 7 supplied to all three variants](media/inputs/square_h3_cinematic_shot_3s.png)](media/inputs/square_h3_cinematic_shot_3s.png)

Picture 7 · [original input](media/inputs/square_h3_cinematic_shot_3s.png)

[![Picture 8 supplied to all three variants](media/inputs/square_h3_suspense_title_2s.png)](media/inputs/square_h3_suspense_title_2s.png)

Picture 8 · [original input](media/inputs/square_h3_suspense_title_2s.png)

[![Picture 9 supplied to all three variants](media/inputs/square_robot_arm_red_cube_1s.png)](media/inputs/square_robot_arm_red_cube_1s.png)

Picture 9 · [original input](media/inputs/square_robot_arm_red_cube_1s.png)

[
[Download video reference](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)

Video 1 · with original audio · [original input](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)

[
[Download video reference](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_robot_arm_red_cube_2s.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_robot_arm_red_cube_2s.mp4)

Video 2 · with original audio · [original input](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_robot_arm_red_cube_2s.mp4)

[
[Download video reference](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_h3_cinematic_shot_2s.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_h3_cinematic_shot_2s.mp4)

Video 3 · with original audio · [original input](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_h3_cinematic_shot_2s.mp4)

Full promptCopy full prompt

```
subject_definitions:
<Subject 1> is the young man with dark curly hair wearing a white T-shirt in <Picture 1>.
<Subject 2> is the model in the black sleeveless dress in <Picture 3> and <Picture 4>.
<Subject 3> is the clay fox in <Picture 6>.
<Subject 4> is the pair of silver wraparound sunglasses in <Picture 5>.
<Subject 5> is the white robotic arm in <Picture 9> and <Video 2>.
<Subject 6> is the family dining room in <Picture 2>.
<Subject 7> is the starship observation deck in <Picture 7> and <Video 3>.
<Subject 8> is the noir title-card style of <Picture 8>.
<Subject 9> is the young man with short wavy blonde hair, wearing a bright pink suit jacket, matching pink trousers, an unbuttoned white shirt and silver rings, holding a small black lamb in his arms in <Video 1>.
<Audio 1>, <Audio 2> and <Audio 3> are the synchronized audio tracks of <Video 1>, <Video 2> and <Video 3>.

summary:
[reference generation + audio reference] A six-shot sunglasses commercial cuts between a family dinner, a fashion studio, a clay forest, a golden pasture, a robot lab and a starship deck, and ends on a noir title card.

retention_analysis:
<Subject 1> (appears in [Shot 1]): fully_preserved - the young man's face, dark curly hair and white T-shirt are retained.
<Subject 2> (appears in [Shot 2]): fully_preserved - the model's braided hair and black sleeveless dress are retained.
<Subject 3> (appears in [Shot 3]): fully_preserved - the clay fox's shape and stop-motion texture are retained.
<Subject 4> (appears in [Shot 1], [Shot 2], [Shot 3], [Shot 4], [Shot 5], [Shot 6]): fully_preserved - the silver wraparound frame and dark lenses are retained.
<Subject 5> (appears in [Shot 5]): fully_preserved - the white robotic arm and its motion are retained.
<Subject 6> (appears in [Shot 1]): fully_preserved - the low table and warm light of the dining room are retained.
<Subject 7> (appears in [Shot 6]): fully_preserved - the great window and the drifting fleet are retained.
<Subject 8> (appears in [Shot 6]): weak_reference - the closing card follows its flat noir palette and lettering.
<Subject 9> (appears in [Shot 4]): fully_preserved - the man's blonde hair, pink suit and the black lamb are retained.
<Audio 1>: reference - the pasture's soft music is referenced in the fourth shot.
<Audio 2>: reference - the servo whir is referenced in the fifth shot.
<Audio 3>: reference - the low starship hum is referenced in the sixth shot.

detailed_description:
The target video is a fast-cut commercial that changes visual style with each shot.
[Shot 1] A live-action medium shot. <Subject 1> sits down at the table of <Subject 6> and puts on <Subject 4>.
[Shot 2] At 00:02.500, the shot cuts to a white-cyclorama fashion studio, where <Subject 2> turns toward the camera wearing <Subject 4>.
[Shot 3] At 00:05.000, the shot cuts to stop-motion clay animation: <Subject 3> finds <Subject 4> on a mossy stump and tries them on.
[Shot 4] At 00:07.500, the shot cuts to a golden pasture, where <Subject 9> slides <Subject 4> onto his nose with one hand while holding the black lamb, over soft music in the manner of <Audio 1>.
[Shot 5] At 00:10.000, the shot cuts to a white table, where <Subject 5> lifts <Subject 4> and holds them up to the light with a servo whir like <Audio 2>.
[Shot 6] At 00:12.500, the shot cuts to <Subject 7>: a silhouetted captain slips on <Subject 4> before the great window over a low hum like <Audio 3>, and the frame cuts to a title card in the style of <Subject 8>.

overall_soundscape:
Quick cuts carry a dinner murmur, a camera shutter, rustling leaves, a breeze over grass, a servo whir and a low starship hum.

non_diegetic_music:
A cool jazz bass line with brushed drums at a steady medium tempo.
```

JavaScript is disabled: all 27 matched profiles are displayed.

1344×768 · 24 FPS · stereo audio. Downloads preserve the generated MP4s. Latencies are three-seed means; the displayed videos use seed 0.

The [36-layer VAE](/blogs/fasth3-v21/#nvfp4-vae-decoders) is shown for quality comparison; its latency is not included in the timing data.

## Results at a glance[#](#results-at-a-glance)

Across 27 matched workloads, FastH3 Omni delivers **5.6–11.9× lower end-to-end latency** than Base on eight GB200 GPUs. Timings include reference encoding, generation, decoding and the finished MP4, at a 1344×768 target canvas.

Both lanes use the original video VAE. Base uses SGLang’s `quality="lossless"` policy, not its stricter `exact` policy. This compares complete model and serving recipes; see the [benchmark methodology](#benchmark-methodology).

Requested clip length
5 seconds10 seconds15 seconds

Select a row to watch its matched outputs.

Base · 50 evaluations FastH3 Omni · 8 evaluations

[1 image
35.44 s
5.67 s
**6.25× ↗**](#omniref-example-image-5s)[Image + voice
35.92 s
5.84 s
**6.15× ↗**](#omniref-example-image-voice-5s)[3 images
73.09 s
12.42 s
**5.88× ↗**](#omniref-example-images3-5s)[9 images
121.61 s
21.59 s
**5.63× ↗**](#omniref-example-images9-5s)[1 short clip
36.06 s
5.17 s
**6.98× ↗**](#omniref-example-clip-5s)[1 long clip
69.93 s
8.34 s
**8.39× ↗**](#omniref-example-video-5s)[3 clips
74.35 s
9.45 s
**7.87× ↗**](#omniref-example-clips3-5s)[Image + video + voice
94.14 s
13.06 s
**7.21× ↗**](#omniref-example-mixed-5s)[9 images + 3 clips
219.90 s
37.38 s
**5.88× ↗**](#omniref-example-full-5s)

[1 image
78.53 s
9.37 s
**8.38× ↗**](#omniref-example-image-10s)[Image + voice
79.92 s
9.71 s
**8.23× ↗**](#omniref-example-image-voice-10s)[3 images
131.25 s
19.15 s
**6.85× ↗**](#omniref-example-images3-10s)[9 images
193.95 s
30.80 s
**6.30× ↗**](#omniref-example-images9-10s)[1 short clip
79.73 s
8.06 s
**9.89× ↗**](#omniref-example-clip-10s)[1 long clip
139.27 s
13.51 s
**10.31× ↗**](#omniref-example-video-10s)[3 clips
132.62 s
13.55 s
**9.79× ↗**](#omniref-example-clips3-10s)[Image + video + voice
172.37 s
19.75 s
**8.73× ↗**](#omniref-example-mixed-10s)[9 images + 3 clips
314.16 s
48.38 s
**6.49× ↗**](#omniref-example-full-10s)

[1 image
139.69 s
14.14 s
**9.88× ↗**](#omniref-example-image-15s)[Image + voice
140.91 s
14.44 s
**9.76× ↗**](#omniref-example-image-voice-15s)[3 images
206.88 s
26.53 s
**7.80× ↗**](#omniref-example-images3-15s)[9 images
282.81 s
41.57 s
**6.80× ↗**](#omniref-example-images9-15s)[1 short clip
140.29 s
11.76 s
**11.93× ↗**](#omniref-example-clip-15s)[1 long clip
215.75 s
18.41 s
**11.72× ↗**](#omniref-example-video-15s)[3 clips
206.44 s
18.38 s
**11.23× ↗**](#omniref-example-clips3-15s)[Image + video + voice
257.71 s
26.71 s
**9.65× ↗**](#omniref-example-mixed-15s)[9 images + 3 clips
422.20 s
59.77 s
**7.06× ↗**](#omniref-example-full-15s)

Mean latency, including audio and MP4 delivery. Both lanes use the original VAE.

Explore all 27 timings and their examples

1344×768, 24 FPS, eight GB200 GPUs. Generation time in seconds, mean ± sample standard deviation; lower is better. Target is the requested output length.

| References | Target | Base | FastH3 Omni | Base / FastH3 | Prompt, inputs & outputs |
| --- | --- | --- | --- | --- | --- |
| 1 image | 5 s | [35.44 ± 0.06](#omniref-example-image-5s) | [5.67 ± 0.02](#omniref-example-image-5s) | 6.25× | [View example ↓](#omniref-example-image-5s) |
| 1 image | 10 s | [78.53 ± 0.01](#omniref-example-image-10s) | [9.37 ± 0.01](#omniref-example-image-10s) | 8.38× | [View example ↓](#omniref-example-image-10s) |
| 1 image | 15 s | [139.69 ± 0.12](#omniref-example-image-15s) | [14.14 ± 0.01](#omniref-example-image-15s) | 9.88× | [View example ↓](#omniref-example-image-15s) |
| Image + voice | 5 s | [35.92 ± 0.07](#omniref-example-image-voice-5s) | [5.84 ± 0.01](#omniref-example-image-voice-5s) | 6.15× | [View example ↓](#omniref-example-image-voice-5s) |
| Image + voice | 10 s | [79.92 ± 0.06](#omniref-example-image-voice-10s) | [9.71 ± 0.15](#omniref-example-image-voice-10s) | 8.23× | [View example ↓](#omniref-example-image-voice-10s) |
| Image + voice | 15 s | [140.91 ± 0.06](#omniref-example-image-voice-15s) | [14.44 ± 0.00](#omniref-example-image-voice-15s) | 9.76× | [View example ↓](#omniref-example-image-voice-15s) |
| 3 images | 5 s | [73.09 ± 0.98](#omniref-example-images3-5s) | [12.42 ± 0.01](#omniref-example-images3-5s) | 5.88× | [View example ↓](#omniref-example-images3-5s) |
| 3 images | 10 s | [131.25 ± 0.02](#omniref-example-images3-10s) | [19.15 ± 0.06](#omniref-example-images3-10s) | 6.85× | [View example ↓](#omniref-example-images3-10s) |
| 3 images | 15 s | [206.88 ± 0.14](#omniref-example-images3-15s) | [26.53 ± 0.01](#omniref-example-images3-15s) | 7.80× | [View example ↓](#omniref-example-images3-15s) |
| 9 images | 5 s | [121.61 ± 0.05](#omniref-example-images9-5s) | [21.59 ± 0.01](#omniref-example-images9-5s) | 5.63× | [View example ↓](#omniref-example-images9-5s) |
| 9 images | 10 s | [193.95 ± 0.05](#omniref-example-images9-10s) | [30.80 ± 0.01](#omniref-example-images9-10s) | 6.30× | [View example ↓](#omniref-example-images9-10s) |
| 9 images | 15 s | [282.81 ± 0.05](#omniref-example-images9-15s) | [41.57 ± 0.01](#omniref-example-images9-15s) | 6.80× | [View example ↓](#omniref-example-images9-15s) |
| 1 short clip | 5 s | [36.06 ± 0.13](#omniref-example-clip-5s) | [5.17 ± 0.01](#omniref-example-clip-5s) | 6.98× | [View example ↓](#omniref-example-clip-5s) |
| 1 short clip | 10 s | [79.73 ± 0.02](#omniref-example-clip-10s) | [8.06 ± 0.01](#omniref-example-clip-10s) | 9.89× | [View example ↓](#omniref-example-clip-10s) |
| 1 short clip | 15 s | [140.29 ± 0.17](#omniref-example-clip-15s) | [11.76 ± 0.01](#omniref-example-clip-15s) | 11.93× | [View example ↓](#omniref-example-clip-15s) |
| 1 long clip | 5 s | [69.93 ± 0.00](#omniref-example-video-5s) | [8.34 ± 0.00](#omniref-example-video-5s) | 8.39× | [View example ↓](#omniref-example-video-5s) |
| 1 long clip | 10 s | [139.27 ± 0.02](#omniref-example-video-10s) | [13.51 ± 0.03](#omniref-example-video-10s) | 10.31× | [View example ↓](#omniref-example-video-10s) |
| 1 long clip | 15 s | [215.75 ± 0.17](#omniref-example-video-15s) | [18.41 ± 0.04](#omniref-example-video-15s) | 11.72× | [View example ↓](#omniref-example-video-15s) |
| 3 clips | 5 s | [74.35 ± 0.09](#omniref-example-clips3-5s) | [9.45 ± 0.01](#omniref-example-clips3-5s) | 7.87× | [View example ↓](#omniref-example-clips3-5s) |
| 3 clips | 10 s | [132.62 ± 0.06](#omniref-example-clips3-10s) | [13.55 ± 0.04](#omniref-example-clips3-10s) | 9.79× | [View example ↓](#omniref-example-clips3-10s) |
| 3 clips | 15 s | [206.44 ± 0.21](#omniref-example-clips3-15s) | [18.38 ± 0.01](#omniref-example-clips3-15s) | 11.23× | [View example ↓](#omniref-example-clips3-15s) |
| Image + video + voice | 5 s | [94.14 ± 0.07](#omniref-example-mixed-5s) | [13.06 ± 0.00](#omniref-example-mixed-5s) | 7.21× | [View example ↓](#omniref-example-mixed-5s) |
| Image + video + voice | 10 s | [172.37 ± 0.10](#omniref-example-mixed-10s) | [19.75 ± 0.00](#omniref-example-mixed-10s) | 8.73× | [View example ↓](#omniref-example-mixed-10s) |
| Image + video + voice | 15 s | [257.71 ± 0.06](#omniref-example-mixed-15s) | [26.71 ± 0.01](#omniref-example-mixed-15s) | 9.65× | [View example ↓](#omniref-example-mixed-15s) |
| 9 images + 3 clips | 5 s | [219.90 ± 0.14](#omniref-example-full-5s) | [37.38 ± 0.03](#omniref-example-full-5s) | 5.88× | [View example ↓](#omniref-example-full-5s) |
| 9 images + 3 clips | 10 s | [314.16 ± 0.13](#omniref-example-full-10s) | [48.38 ± 0.04](#omniref-example-full-10s) | 6.49× | [View example ↓](#omniref-example-full-10s) |
| 9 images + 3 clips | 15 s | [422.20 ± 0.22](#omniref-example-full-15s) | [59.77 ± 0.05](#omniref-example-full-15s) | 7.06× | [View example ↓](#omniref-example-full-15s) |

Download the [timing CSV](/blogs/fastvideo-omniref-update/data/latency.csv) or [full benchmark JSON](/blogs/fastvideo-omniref-update/data/benchmark.json).

## PDD + DMD[#](#pdd--dmd)

FastH3 Omni combines **Parallel Decoding Distillation (PDD)** with **Distribution Matching Distillation (DMD)**. PDD predicts several denoising updates per transformer evaluation; DMD helps train the completed video and audio output. Reference conditioning is retained throughout generation. For the method and its illustrations, see the [PDD paper](https://arxiv.org/abs/2607.26004).

* **PDD: many updates per forward.** The student’s output heads are widened from one velocity prediction to a 32-interval fine time grid. At inference those heads run as eight fused blocks of four, so one transformer evaluation advances four intervals and the full trajectory takes eight evaluations instead of Base’s 50. A teacher-supervised head loss keeps every head’s update consistent with the frozen Base model.
* **DMD: match the finished output.** On top of PDD, a trainable critic models the distribution of the student’s samples while the frozen Base teacher supplies the target; the student is updated to close the gap between them on the completed video and audio, not just on each individual step. Critic and student updates alternate, with several critic updates per student update.
* **References stay clean conditioning.** Reference images, videos and audio are never noised: they condition the student, teacher and critic in every forward, and only the target video and audio enter the noising and the losses.
* **Sparse throughout.** The student trains and samples with Video Sparse Attention on 128-row tiles, so the sparsity used for serving is the sparsity it was trained with.

Huge thanks to the [NVIDIA FastGen](https://github.com/NVlabs/FastGen) team (Julius Berner, Chao Liu and Arash Vahdat), who introduced PDD and whose DMD2 framework and H3 reference work this model builds on. FastVideo’s PDD and DMPDD trainers adapt the PDD objectives from the [FastGen repository](https://github.com/NVlabs/FastGen) to FastVideo’s MiniMax H3 model, sequence-parallel and checkpoint interfaces.

| Training | Amount |
| --- | --- |
| GPUs | 64 NVIDIA B300 |
| Training steps | 3,500 |
| Estimated compute | Approximately 7,800 GPU-hours |

The training code is in FastVideo: see the [FastH3 Omni DMPDD training guide](https://github.com/hao-ai-lab/FastVideo/blob/main/docs/training/omniref_dmpdd.md).

## Local AI with FastVideo[#](#local-ai-with-fastvideo)

FastH3 Omni also runs locally on **NVIDIA DGX Spark and RTX 5090 through FastVideo**. Start with the [FastVideo cookbook](https://haoailab.com/FastVideo/cookbook/) and [FastH3 Omni recipe builder](https://haoailab.com/FastVideo/cookbook/minimax-h3/fasth3-omniref/), then follow the [local inference guide](https://github.com/hao-ai-lab/FastVideo/blob/main/docs/inference/fasth3_omniref.md) for model setup and reference inputs.

| Device | Weights and inference recipe |
| --- | --- |
| DGX Spark (GB10, 128 GB unified memory) | [NVFP4 QAD weights](https://huggingface.co/FastVideo/FastH3-Omni-NVFP4-QAD) · [`spark` recipe](https://github.com/hao-ai-lab/FastVideo/blob/main/examples/inference/basic/basic_fasth3_omniref_spark.yaml) |
| RTX 5090 (32 GB) | [NVFP4 QAD weights](https://huggingface.co/FastVideo/FastH3-Omni-NVFP4-QAD) · [`rtx-5090` recipe](https://github.com/hao-ai-lab/FastVideo/blob/main/examples/inference/basic/basic_fasth3_omniref_rtx5090.yaml) |

**QAD means quantization-aware distillation:** these weights are trained for NVFP4 execution on Blackwell. Install FastVideo with the [DGX Spark setup guide](https://haoailab.com/FastVideo/getting_started/installation/spark/) or [NVIDIA GPU setup guide](https://haoailab.com/FastVideo/getting_started/installation/gpu/). Both device profiles default to 480p; Spark keeps the model components resident, while the RTX 5090 profile offloads the text encoder and requires a precomputed AdaLN table. The local inference guide covers preparing that table, composing the model directory and selecting the decoder. Keep the recipe’s attention and precision settings.

For **FP8 in ComfyUI**, use the [FastH3 Omni FP8 ComfyUI checkpoint](https://huggingface.co/FastVideo/FastH3-Omni-FP8-Comfy). Native FastVideo inference requires a compatible dense or FP8 export; follow the guide’s [FP8 device profile](https://github.com/hao-ai-lab/FastVideo/blob/main/docs/inference/fasth3_omniref.md#device-profiles) and [RTX 4090 recipe](https://github.com/hao-ai-lab/FastVideo/blob/main/examples/inference/basic/basic_fasth3_omniref_rtx4090.yaml) for layerwise offload. The text encoder must also match the hardware: the bundled NVFP4 encoder needs Blackwell, so other GPUs need compatible BF16 encoder components. NVFP4 QAD and FP8 are separate numerical variants; their outputs can differ from the BF16 release.

Optional [NVFP4 VAE decoders](https://huggingface.co/FastVideo/FastH3-NVFP4-VAE-Decoder) provide a **36-layer quality** tier and an **8-layer fast** tier. Follow the guide’s `--decoder` setup; these local configurations have their own resolution, memory and precision choices, so the eight-GB200 timings above do not describe their speed.

## Deploy FastH3 Omni with UniServe[#](#deploy-fasth3-omni-with-uniserve)

Install [UniServe](https://github.com/hao-ai-lab/uniserve) on every node:

```
git clone https://github.com/hao-ai-lab/uniserve.git && cd uniserve
apt-get update && apt-get install -y build-essential python3.12-dev pkg-config cmake \
  git curl ca-certificates nasm zlib1g-dev xz-utils
scripts/install-ffmpeg.sh
curl -LsSf https://astral.sh/uv/install.sh | sh
curl -sSf https://sh.rustup.rs | sh -s -- -y --profile minimal --default-toolchain stable
export CUDA_HOME=/usr/local/cuda MAX_JOBS=2
export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$CUDA_HOME/bin:$PATH"
uv sync --locked --python 3.12 --extra gpu
source .venv/bin/activate
```

Then pick your GPUs and run the steps from the UniServe checkout:

Model

GPU

GPUs

Optimize for

Checkpoint

Precision

Longest clip

Longest prompt

Reference sizing

Deployment file 

Shipped with UniServe; pass it to `--workers`.CopyDownload

The [UniServe serving guide](https://github.com/hao-ai-lab/uniserve/blob/main/docs/minimax_h3/minimax_h3.md) covers every option and request field.

## Benchmark methodology[#](#benchmark-methodology)

Nine reference compositions × three clip lengths (5, 10 and 15 seconds), measured on eight GB200 GPUs. Each profile uses one warmup and three measured seeds; the gallery consistently shows seed 0.

Read measurement settings and numerical policy

* **Hardware and scope.** Eight NVIDIA GB200 GPUs across two four-GPU trays. GB200 is our proxy for B200; B200 was not separately measured. These results describe the eight-GPU cohort.
* **Matched inputs.** Nine reference compositions × three requested lengths, all at 1344×768 and 24 FPS. The aligned outputs contain 124, 243 or 362 frames. Images use the released enlarged-reference mode with a 2048-pixel short edge. Reference clips retain their real soundtracks and standalone audio remains a real input.
* **Measurement.** One request at a time, one warmup with seed 42 for each profile, then measured seeds 0, 1 and 2. The tables report arithmetic mean client end-to-end time until the complete MP4 is available; the downloadable data also includes sample standard deviations. Model loading and server startup are excluded. No latency is inferred from missing cells or memory failures, and no timing is normalized to another workload.
* **Model and runtime.** Base is MiniMax H3 Ref2VA with 50 denoising evaluations; FastH3 Omni uses the 32-interval PDD student with eight fused evaluations and VSA. The Base lane uses Ulysses 4 × Ring 2 with the native FlashAttention transformer backend; the student uses eight-way Ulysses. Conditioning caches are disabled. Model weights, attention patterns and serving implementations differ, so this compares complete model/runtime recipes, not an isolated distillation or kernel ablation.
* **Base numerical policy.** These Base measurements use SGLang’s `quality="lossless"` policy with original unquantized weights, dense attention and the model’s mixed-precision rules. Its DiT normalization/modulation and VAE fusions can change intermediate rounding. They are not measurements of SGLang’s stricter `quality="exact"` policy, and reference-exact or perceptual equivalence has not been established. The original model is not uniformly BF16: it retains FP32-sensitive DiT operations and the released VAE’s mixed-precision execution. The displayed latencies have not been converted to an exact-policy estimate.
* **Reading the examples.** The timing statistics use three seeds; the gallery consistently uses seed 0. A shared seed does not imply numerical or perceptual output parity across different models or runtimes. The examples support direct inspection and are not a quantitative quality evaluation.

## Get started[#](#get-started)

Download the model weights from the [FastH3 Omni collection](https://huggingface.co/collections/FastVideo/fasth3-omni), then follow the [UniServe setup](#deploy-fasth3-omni-with-uniserve) to generate video and audio from your own references.

## Acknowledgements[#](#acknowledgements)

FastH3 builds on [MiniMax H3](https://huggingface.co/MiniMaxAI/MiniMax-H3). We thank the MiniMax team for releasing its weights and code.

We thank the NVIDIA Enterprise Products team (Pengcheng Li and Cliff Woolley) for the Video Sparse Attention kernel used by FastH3. We thank the [NVIDIA FastGen](https://github.com/NVlabs/FastGen) team (Julius Berner, Chao Liu and Arash Vahdat) for the DMD2 framework and H3 reference work, and for introducing [Parallel Decoding Distillation](https://research.nvidia.com/labs/genair/pdd/).

We thank [Nuva Lab](https://nuvalab.ai/) for bringing production-grounded creative video workflows to FastH3, and the upstream serving, kernel and open-source communities whose implementations make these experiments possible. We also acknowledge [Reactor](https://www.reactor.inc/) for supporting FastH3 Omni, and the [vLLM project](https://vllm.ai/), [NVIDIA](https://www.nvidia.com/en-us/) and [MBZUAI](https://mbzuai.ac.ae/) for their support of FastVideo.
