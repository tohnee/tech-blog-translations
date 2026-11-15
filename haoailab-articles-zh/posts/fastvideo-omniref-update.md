---
title: "FastVideo FastH3 Omni：在 NVIDIA Blackwell、RTX Spark 与 RTX GPU 上开源实时的 MiniMax FastH3 Ref2VA"
title_en: "FastVideo FastH3 Omni: Open Source Real-Time Minimax FastH3 Ref2VA on NVIDIA Blackwell, RTX Spark, and RTX GPUs."
date: 2026-10-20
source: https://haoailab.com/blogs/fastvideo-omniref-update/
crawled: 2026-11-16
translated: 2026-11-16
---

# FastVideo FastH3 Omni：在 NVIDIA Blackwell、RTX Spark 与 RTX GPU 上开源实时的 MiniMax FastH3 Ref2VA

> 原文：[FastVideo FastH3 Omni: Open Source Real-Time Minimax FastH3 Ref2VA on NVIDIA Blackwell, RTX Spark, and RTX GPUs.](https://haoailab.com/blogs/fastvideo-omniref-update/) · Hao AI Lab @ UCSD

# FastVideo FastH3 Omni：在 NVIDIA Blackwell、RTX Spark 与 RTX GPU 上开源实时的 MiniMax FastH3 Ref2VA

在八张 GB200 GPU 上把 MiniMax H3 视频与音频的端到端延迟降低最多约 12 倍，并为本地 AI 提供优化过的 NVFP4 QAD 检查点。

2026 年 10 月 20 日 · FastVideo Team

[![](https://img.shields.io/github/stars/hao-ai-lab/FastVideo?style=social)](https://github.com/hao-ai-lab/FastVideo)[![](https://img.shields.io/badge/🤗%20huggingface--green.svg?style=social)](https://huggingface.co/collections/FastVideo/fasth3-omni)[![Slack](https://img.shields.io/badge/Slack--4A154B?style=social&logo=slack&logoColor=blue)](https://join.slack.com/t/fastvideo/shared_invite/zt-3f4lao1uq-u~Ipx6Lt4J27AlD2y~IdLQ)

FastVideo 开源 **FastH3 Omni**：一个面向参考引导视频与音频的蒸馏版 MiniMax H3 模型。给它一段提示词，加上图片、视频片段与一段声音参考，它会生成一段音画同步的成品视频。

[模型权重](https://huggingface.co/collections/FastVideo/fasth3-omni) · [UniServe 部署](#deploy-fasth3-omni-with-uniserve) · [用 FastVideo 的本地 AI](#local-ai-with-fastvideo)

已支持 ComfyUI。我们的本地 AI 博客与发布计划在明天，**10 月 21 日**。

[
你的浏览器不支持带音频的 MP4 视频。](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--hero--trilingual-bgm-1080p.mp4)

整段视频都是用 FastH3 Omni 在 FastVideo 上生成的。

## TL;DR[#](#tldr)

* **八次 transformer 评估**，而 Base 是 50 次，并支持图片、视频与音频参考。
* 在八张 GB200 GPU 的 27 个配对工作负载上，**端到端延迟降低 5.6–11.9 倍**。这里比较的是完整的服务配方，Base 使用其 `lossless` 数值策略；见[方法](#benchmark-methodology)。
* **FastVideo UniServe 上的实时生成**：在特定的 FastH3 Omni 任务上，FastVideo UniServe 对 768p 的 5 秒、10 秒与 15 秒片段达到实时生成速度。
* **本地 AI。** 在 [DGX Spark 或 RTX 5090 上用 FastVideo 运行](#local-ai-with-fastvideo)，使用 NVFP4 QAD 权重与设备配方。
* **在下面看和听输出。** 改变参考素材或片段长度，然后把配对示例一起播放。参考输入已展开；需要时打开完整提示词。
* **合作伙伴。** 感谢 [Nuva Lab](https://nuvalab.ai/)、[Reactor](https://www.reactor.inc/)、NVIDIA FastGen 团队与 NVIDIA Enterprise products 的协作与支持。

## 配对的参考输入与输出[#](#matched-reference-inputs-and-outputs)

选择一种参考素材组合与片段长度，以比较 **Base、FastH3 Omni 与使用 36 层 VAE 的 FastH3 Omni**。所有示例都使用 seed 0 与匹配的输入；这些是定性比较，不构成输出一致性的证据。

参考素材
1 张图片图片 + 声音3 张图片9 张图片1 段短片段1 段长片段3 段片段图片 + 视频 + 声音9 张图片 + 3 段片段
请求长度
5 秒10 秒15 秒
下一个示例 →
8×GB200 · seed 0

一起播放
全部暂停
听
BaseFastH3 OmniFastH3 Omni · 36L VAE全部静音

按下播放后才会开始。用「听」选择一条音轨。

### 1 张图片 · 5 秒请求

124 帧 · 24 FPS · 立体声 · 匹配的提示词、参考素材、seed 与 GPU 数量

**Base**
平均延迟 35.44 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-image-5s-seed0.mp4).
](media/posters/base-image-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-image-5s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-image-5s-seed0.mp4)

**FastH3 Omni**
平均延迟 5.67 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-image-5s-seed0.mp4).
](media/posters/fast-image-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-image-5s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-image-5s-seed0.mp4)

**FastH3 Omni · 36L VAE**
质量对比

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-image-5s-seed0.mp4).
](media/posters/decoder36-image-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-image-5s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-image-5s-seed0.mp4)

**该工作负载延迟降低 6.25 倍**。端到端 35.44 秒 → 5.67 秒（三个 seed 的均值）。

源参考素材（1）

[![提供给三个版本的图片 1](media/inputs/hf_character_action_reference.png)](media/inputs/hf_character_action_reference.png)

图片 1 · [原始输入](media/inputs/hf_character_action_reference.png)

完整提示词复制完整提示词

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

### 1 张图片 · 10 秒请求

243 帧 · 24 FPS · 立体声 · 匹配的提示词、参考素材、seed 与 GPU 数量

**Base**
平均延迟 78.53 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-image-10s-seed0.mp4).
](media/posters/base-image-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-image-10s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-image-10s-seed0.mp4)

**FastH3 Omni**
平均延迟 9.37 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-image-10s-seed0.mp4).
](media/posters/fast-image-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-image-10s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-image-10s-seed0.mp4)

**FastH3 Omni · 36L VAE**
质量对比

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-image-10s-seed0.mp4).
](media/posters/decoder36-image-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-image-10s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-image-10s-seed0.mp4)

**该工作负载延迟降低 8.38 倍**。端到端 78.53 秒 → 9.37 秒（三个 seed 的均值）。

源参考素材（1）

[![提供给三个版本的图片 1](media/inputs/hf_character_action_reference.png)](media/inputs/hf_character_action_reference.png)

图片 1 · [原始输入](media/inputs/hf_character_action_reference.png)

完整提示词复制完整提示词

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

### 1 张图片 · 15 秒请求

362 帧 · 24 FPS · 立体声 · 匹配的提示词、参考素材、seed 与 GPU 数量

**Base**
平均延迟 139.69 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-image-15s-seed0.mp4).
](media/posters/base-image-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-image-15s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-image-15s-seed0.mp4)

**FastH3 Omni**
平均延迟 14.14 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-image-15s-seed0.mp4).
](media/posters/fast-image-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-image-15s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-image-15s-seed0.mp4)

**FastH3 Omni · 36L VAE**
质量对比

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-image-15s-seed0.mp4).
](media/posters/decoder36-image-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-image-15s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-image-15s-seed0.mp4)

**该工作负载延迟降低 9.88 倍**。端到端 139.69 秒 → 14.14 秒（三个 seed 的均值）。

源参考素材（1）

[![提供给三个版本的图片 1](media/inputs/hf_character_action_reference.png)](media/inputs/hf_character_action_reference.png)

图片 1 · [原始输入](media/inputs/hf_character_action_reference.png)

完整提示词复制完整提示词

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

### 图片 + 声音 · 5 秒请求

124 帧 · 24 FPS · 立体声 · 匹配的提示词、参考素材、seed 与 GPU 数量

**Base**
平均延迟 35.92 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-image-voice-5s-seed0.mp4).
](media/posters/base-image-voice-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-image-voice-5s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-image-voice-5s-seed0.mp4)

**FastH3 Omni**
平均延迟 5.84 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-image-voice-5s-seed0.mp4).
](media/posters/fast-image-voice-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-image-voice-5s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-image-voice-5s-seed0.mp4)

**FastH3 Omni · 36L VAE**
质量对比

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-image-voice-5s-seed0.mp4).
](media/posters/decoder36-image-voice-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-image-voice-5s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-image-voice-5s-seed0.mp4)

**该工作负载延迟降低 6.15 倍**。端到端 35.92 秒 → 5.84 秒（三个 seed 的均值）。

源参考素材（2）

[![提供给三个版本的图片 1](media/inputs/hf_character_action_reference.png)](media/inputs/hf_character_action_reference.png)

图片 1 · [原始输入](media/inputs/hf_character_action_reference.png)

[下载音频参考](media/inputs/official_ref2va_1_audio.mp3)

音频 1 · [原始输入](media/inputs/official_ref2va_1_audio.mp3)

完整提示词复制完整提示词

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

### 图片 + 声音 · 10 秒请求

243 帧 · 24 FPS · 立体声 · 匹配的提示词、参考素材、seed 与 GPU 数量

**Base**
平均延迟 79.92 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-image-voice-10s-seed0.mp4).
](media/posters/base-image-voice-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-image-voice-10s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-image-voice-10s-seed0.mp4)

**FastH3 Omni**
平均延迟 9.71 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-image-voice-10s-seed0.mp4).
](media/posters/fast-image-voice-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-image-voice-10s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-image-voice-10s-seed0.mp4)

**FastH3 Omni · 36L VAE**
质量对比

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-image-voice-10s-seed0.mp4).
](media/posters/decoder36-image-voice-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-image-voice-10s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-image-voice-10s-seed0.mp4)

**该工作负载延迟降低 8.23 倍**。端到端 79.92 秒 → 9.71 秒（三个 seed 的均值）。

源参考素材（2）

[![提供给三个版本的图片 1](media/inputs/hf_character_action_reference.png)](media/inputs/hf_character_action_reference.png)

图片 1 · [原始输入](media/inputs/hf_character_action_reference.png)

[下载音频参考](media/inputs/official_ref2va_1_audio.mp3)

音频 1 · [原始输入](media/inputs/official_ref2va_1_audio.mp3)

完整提示词复制完整提示词

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

### 图片 + 声音 · 15 秒请求

362 帧 · 24 FPS · 立体声 · 匹配的提示词、参考素材、seed 与 GPU 数量

**Base**
平均延迟 140.91 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-image-voice-15s-seed0.mp4).
](media/posters/base-image-voice-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-image-voice-15s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-image-voice-15s-seed0.mp4)

**FastH3 Omni**
平均延迟 14.44 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-image-voice-15s-seed0.mp4).
](media/posters/fast-image-voice-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-image-voice-15s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-image-voice-15s-seed0.mp4)

**FastH3 Omni · 36L VAE**
质量对比

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-image-voice-15s-seed0.mp4).
](media/posters/decoder36-image-voice-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-image-voice-15s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-image-voice-15s-seed0.mp4)

**该工作负载延迟降低 9.76 倍**。端到端 140.91 秒 → 14.44 秒（三个 seed 的均值）。

源参考素材（2）

[![提供给三个版本的图片 1](media/inputs/hf_character_action_reference.png)](media/inputs/hf_character_action_reference.png)

图片 1 · [原始输入](media/inputs/hf_character_action_reference.png)

[下载音频参考](media/inputs/official_ref2va_1_audio.mp3)

音频 1 · [原始输入](media/inputs/official_ref2va_1_audio.mp3)

完整提示词复制完整提示词

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

### 3 张图片 · 5 秒请求

124 帧 · 24 FPS · 立体声 · 匹配的提示词、参考素材、seed 与 GPU 数量

**Base**
平均延迟 73.09 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-images3-5s-seed0.mp4).
](media/posters/base-images3-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-images3-5s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-images3-5s-seed0.mp4)

**FastH3 Omni**
平均延迟 12.42 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-images3-5s-seed0.mp4).
](media/posters/fast-images3-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-images3-5s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-images3-5s-seed0.mp4)

**FastH3 Omni · 36L VAE**
质量对比

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-images3-5s-seed0.mp4).
](media/posters/decoder36-images3-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-images3-5s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-images3-5s-seed0.mp4)

**该工作负载延迟降低 5.88 倍**。端到端 73.09 秒 → 12.42 秒（三个 seed 的均值）。

源参考素材（3）

[![提供给三个版本的图片 1](media/inputs/hf_character_action_reference.png)](media/inputs/hf_character_action_reference.png)

图片 1 · [原始输入](media/inputs/hf_character_action_reference.png)

[![提供给三个版本的图片 2](media/inputs/hf_fashion_glasses_reference_3.png)](media/inputs/hf_fashion_glasses_reference_3.png)

图片 2 · [原始输入](media/inputs/hf_fashion_glasses_reference_3.png)

[![提供给三个版本的图片 3](media/inputs/official_fl2va_0_image.png)](media/inputs/official_fl2va_0_image.png)

图片 3 · [原始输入](media/inputs/official_fl2va_0_image.png)

完整提示词复制完整提示词

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

### 3 张图片 · 10 秒请求

243 帧 · 24 FPS · 立体声 · 匹配的提示词、参考素材、seed 与 GPU 数量

**Base**
平均延迟 131.25 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-images3-10s-seed0.mp4).
](media/posters/base-images3-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-images3-10s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-images3-10s-seed0.mp4)

**FastH3 Omni**
平均延迟 19.15 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-images3-10s-seed0.mp4).
](media/posters/fast-images3-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-images3-10s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-images3-10s-seed0.mp4)

**FastH3 Omni · 36L VAE**
质量对比

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-images3-10s-seed0.mp4).
](media/posters/decoder36-images3-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-images3-10s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-images3-10s-seed0.mp4)

**该工作负载延迟降低 6.85 倍**。端到端 131.25 秒 → 19.15 秒（三个 seed 的均值）。

源参考素材（3）

[![提供给三个版本的图片 1](media/inputs/hf_character_action_reference.png)](media/inputs/hf_character_action_reference.png)

图片 1 · [原始输入](media/inputs/hf_character_action_reference.png)

[![提供给三个版本的图片 2](media/inputs/hf_fashion_glasses_reference_3.png)](media/inputs/hf_fashion_glasses_reference_3.png)

图片 2 · [原始输入](media/inputs/hf_fashion_glasses_reference_3.png)

[![提供给三个版本的图片 3](media/inputs/official_fl2va_0_image.png)](media/inputs/official_fl2va_0_image.png)

图片 3 · [原始输入](media/inputs/official_fl2va_0_image.png)

完整提示词复制完整提示词

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

### 3 张图片 · 15 秒请求

362 帧 · 24 FPS · 立体声 · 匹配的提示词、参考素材、seed 与 GPU 数量

**Base**
平均延迟 206.88 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-images3-15s-seed0.mp4).
](media/posters/base-images3-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-images3-15s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-images3-15s-seed0.mp4)

**FastH3 Omni**
平均延迟 26.53 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-images3-15s-seed0.mp4).
](media/posters/fast-images3-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-images3-15s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-images3-15s-seed0.mp4)

**FastH3 Omni · 36L VAE**
质量对比

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-images3-15s-seed0.mp4).
](media/posters/decoder36-images3-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-images3-15s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-images3-15s-seed0.mp4)

**该工作负载延迟降低 7.80 倍**。端到端 206.88 秒 → 26.53 秒（三个 seed 的均值）。

源参考素材（3）

[![提供给三个版本的图片 1](media/inputs/hf_character_action_reference.png)](media/inputs/hf_character_action_reference.png)

图片 1 · [原始输入](media/inputs/hf_character_action_reference.png)

[![提供给三个版本的图片 2](media/inputs/hf_fashion_glasses_reference_3.png)](media/inputs/hf_fashion_glasses_reference_3.png)

图片 2 · [原始输入](media/inputs/hf_fashion_glasses_reference_3.png)

[![提供给三个版本的图片 3](media/inputs/official_fl2va_0_image.png)](media/inputs/official_fl2va_0_image.png)

图片 3 · [原始输入](media/inputs/official_fl2va_0_image.png)

完整提示词复制完整提示词

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

### 9 张图片 · 5 秒请求

124 帧 · 24 FPS · 立体声 · 匹配的提示词、参考素材、seed 与 GPU 数量

**Base**
平均延迟 121.61 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-images9-5s-seed0.mp4).
](media/posters/base-images9-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-images9-5s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-images9-5s-seed0.mp4)

**FastH3 Omni**
平均延迟 21.59 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-images9-5s-seed0.mp4).
](media/posters/fast-images9-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-images9-5s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-images9-5s-seed0.mp4)

**FastH3 Omni · 36L VAE**
质量对比

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-images9-5s-seed0.mp4).
](media/posters/decoder36-images9-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-images9-5s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-images9-5s-seed0.mp4)

**该工作负载延迟降低 5.63 倍**。端到端 121.61 秒 → 21.59 秒（三个 seed 的均值）。

源参考素材（9）

[![提供给三个版本的图片 1](media/inputs/square_character_action_reference.png)](media/inputs/square_character_action_reference.png)

图片 1 · [原始输入](media/inputs/square_character_action_reference.png)

[![提供给三个版本的图片 2](media/inputs/square_official_fl2va_0_image.png)](media/inputs/square_official_fl2va_0_image.png)

图片 2 · [原始输入](media/inputs/square_official_fl2va_0_image.png)

[![提供给三个版本的图片 3](media/inputs/square_fashion_glasses_reference_1.png)](media/inputs/square_fashion_glasses_reference_1.png)

图片 3 · [原始输入](media/inputs/square_fashion_glasses_reference_1.png)

[![提供给三个版本的图片 4](media/inputs/square_fashion_glasses_reference_2.png)](media/inputs/square_fashion_glasses_reference_2.png)

图片 4 · [原始输入](media/inputs/square_fashion_glasses_reference_2.png)

[![提供给三个版本的图片 5](media/inputs/square_fashion_glasses_reference_3.png)](media/inputs/square_fashion_glasses_reference_3.png)

图片 5 · [原始输入](media/inputs/square_fashion_glasses_reference_3.png)

[![提供给三个版本的图片 6](media/inputs/square_fl2va_clay_fox_reference.png)](media/inputs/square_fl2va_clay_fox_reference.png)

图片 6 · [原始输入](media/inputs/square_fl2va_clay_fox_reference.png)

[![提供给三个版本的图片 7](media/inputs/square_h3_cinematic_shot_3s.png)](media/inputs/square_h3_cinematic_shot_3s.png)

图片 7 · [原始输入](media/inputs/square_h3_cinematic_shot_3s.png)

[![提供给三个版本的图片 8](media/inputs/square_h3_suspense_title_2s.png)](media/inputs/square_h3_suspense_title_2s.png)

图片 8 · [原始输入](media/inputs/square_h3_suspense_title_2s.png)

[![提供给三个版本的图片 9](media/inputs/square_robot_arm_red_cube_1s.png)](media/inputs/square_robot_arm_red_cube_1s.png)

图片 9 · [原始输入](media/inputs/square_robot_arm_red_cube_1s.png)

完整提示词复制完整提示词

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

### 9 张图片 · 10 秒请求

243 帧 · 24 FPS · 立体声 · 匹配的提示词、参考素材、seed 与 GPU 数量

**Base**
平均延迟 193.95 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-images9-10s-seed0.mp4).
](media/posters/base-images9-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-images9-10s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-images9-10s-seed0.mp4)

**FastH3 Omni**
平均延迟 30.80 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-images9-10s-seed0.mp4).
](media/posters/fast-images9-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-images9-10s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-images9-10s-seed0.mp4)

**FastH3 Omni · 36L VAE**
质量对比

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-images9-10s-seed0.mp4).
](media/posters/decoder36-images9-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-images9-10s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-images9-10s-seed0.mp4)

**该工作负载延迟降低 6.30 倍**。端到端 193.95 秒 → 30.80 秒（三个 seed 的均值）。

源参考素材（9）

[![提供给三个版本的图片 1](media/inputs/square_character_action_reference.png)](media/inputs/square_character_action_reference.png)

图片 1 · [原始输入](media/inputs/square_character_action_reference.png)

[![提供给三个版本的图片 2](media/inputs/square_official_fl2va_0_image.png)](media/inputs/square_official_fl2va_0_image.png)

图片 2 · [原始输入](media/inputs/square_official_fl2va_0_image.png)

[![提供给三个版本的图片 3](media/inputs/square_fashion_glasses_reference_1.png)](media/inputs/square_fashion_glasses_reference_1.png)

图片 3 · [原始输入](media/inputs/square_fashion_glasses_reference_1.png)

[![提供给三个版本的图片 4](media/inputs/square_fashion_glasses_reference_2.png)](media/inputs/square_fashion_glasses_reference_2.png)

图片 4 · [原始输入](media/inputs/square_fashion_glasses_reference_2.png)

[![提供给三个版本的图片 5](media/inputs/square_fashion_glasses_reference_3.png)](media/inputs/square_fashion_glasses_reference_3.png)

图片 5 · [原始输入](media/inputs/square_fashion_glasses_reference_3.png)

[![提供给三个版本的图片 6](media/inputs/square_fl2va_clay_fox_reference.png)](media/inputs/square_fl2va_clay_fox_reference.png)

图片 6 · [原始输入](media/inputs/square_fl2va_clay_fox_reference.png)

[![提供给三个版本的图片 7](media/inputs/square_h3_cinematic_shot_3s.png)](media/inputs/square_h3_cinematic_shot_3s.png)

图片 7 · [原始输入](media/inputs/square_h3_cinematic_shot_3s.png)

[![提供给三个版本的图片 8](media/inputs/square_h3_suspense_title_2s.png)](media/inputs/square_h3_suspense_title_2s.png)

图片 8 · [原始输入](media/inputs/square_h3_suspense_title_2s.png)

[![提供给三个版本的图片 9](media/inputs/square_robot_arm_red_cube_1s.png)](media/inputs/square_robot_arm_red_cube_1s.png)

图片 9 · [原始输入](media/inputs/square_robot_arm_red_cube_1s.png)

完整提示词复制完整提示词

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

### 9 张图片 · 15 秒请求

362 帧 · 24 FPS · 立体声 · 匹配的提示词、参考素材、seed 与 GPU 数量

**Base**
平均延迟 282.81 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-images9-15s-seed0.mp4).
](media/posters/base-images9-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-images9-15s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-images9-15s-seed0.mp4)

**FastH3 Omni**
平均延迟 41.57 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-images9-15s-seed0.mp4).
](media/posters/fast-images9-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-images9-15s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-images9-15s-seed0.mp4)

**FastH3 Omni · 36L VAE**
质量对比

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-images9-15s-seed0.mp4).
](media/posters/decoder36-images9-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-images9-15s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-images9-15s-seed0.mp4)

**该工作负载延迟降低 6.80 倍**。端到端 282.81 秒 → 41.57 秒（三个 seed 的均值）。

源参考素材（9）

[![提供给三个版本的图片 1](media/inputs/square_character_action_reference.png)](media/inputs/square_character_action_reference.png)

图片 1 · [原始输入](media/inputs/square_character_action_reference.png)

[![提供给三个版本的图片 2](media/inputs/square_official_fl2va_0_image.png)](media/inputs/square_official_fl2va_0_image.png)

图片 2 · [原始输入](media/inputs/square_official_fl2va_0_image.png)

[![提供给三个版本的图片 3](media/inputs/square_fashion_glasses_reference_1.png)](media/inputs/square_fashion_glasses_reference_1.png)

图片 3 · [原始输入](media/inputs/square_fashion_glasses_reference_1.png)

[![提供给三个版本的图片 4](media/inputs/square_fashion_glasses_reference_2.png)](media/inputs/square_fashion_glasses_reference_2.png)

图片 4 · [原始输入](media/inputs/square_fashion_glasses_reference_2.png)

[![提供给三个版本的图片 5](media/inputs/square_fashion_glasses_reference_3.png)](media/inputs/square_fashion_glasses_reference_3.png)

图片 5 · [原始输入](media/inputs/square_fashion_glasses_reference_3.png)

[![提供给三个版本的图片 6](media/inputs/square_fl2va_clay_fox_reference.png)](media/inputs/square_fl2va_clay_fox_reference.png)

图片 6 · [原始输入](media/inputs/square_fl2va_clay_fox_reference.png)

[![提供给三个版本的图片 7](media/inputs/square_h3_cinematic_shot_3s.png)](media/inputs/square_h3_cinematic_shot_3s.png)

图片 7 · [原始输入](media/inputs/square_h3_cinematic_shot_3s.png)

[![提供给三个版本的图片 8](media/inputs/square_h3_suspense_title_2s.png)](media/inputs/square_h3_suspense_title_2s.png)

图片 8 · [原始输入](media/inputs/square_h3_suspense_title_2s.png)

[![提供给三个版本的图片 9](media/inputs/square_robot_arm_red_cube_1s.png)](media/inputs/square_robot_arm_red_cube_1s.png)

图片 9 · [原始输入](media/inputs/square_robot_arm_red_cube_1s.png)

完整提示词复制完整提示词

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

### 1 段短片段 · 5 秒请求

124 帧 · 24 FPS · 立体声 · 匹配的提示词、参考素材、seed 与 GPU 数量

**Base**
平均延迟 36.06 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-clip-5s-seed0.mp4).
](media/posters/base-clip-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-clip-5s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-clip-5s-seed0.mp4)

**FastH3 Omni**
平均延迟 5.17 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-clip-5s-seed0.mp4).
](media/posters/fast-clip-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-clip-5s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-clip-5s-seed0.mp4)

**FastH3 Omni · 36L VAE**
质量对比

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-clip-5s-seed0.mp4).
](media/posters/decoder36-clip-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-clip-5s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-clip-5s-seed0.mp4)

**该工作负载延迟降低 6.98 倍**。端到端 36.06 秒 → 5.17 秒（三个 seed 的均值）。

源参考素材（1）

[
[下载视频参考](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)

视频 1 · 含原始音频 · [原始输入](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)

完整提示词复制完整提示词

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

### 1 段短片段 · 10 秒请求

243 帧 · 24 FPS · 立体声 · 匹配的提示词、参考素材、seed 与 GPU 数量

**Base**
平均延迟 79.73 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-clip-10s-seed0.mp4).
](media/posters/base-clip-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-clip-10s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-clip-10s-seed0.mp4)

**FastH3 Omni**
平均延迟 8.06 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-clip-10s-seed0.mp4).
](media/posters/fast-clip-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-clip-10s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-clip-10s-seed0.mp4)

**FastH3 Omni · 36L VAE**
质量对比

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-clip-10s-seed0.mp4).
](media/posters/decoder36-clip-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-clip-10s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-clip-10s-seed0.mp4)

**该工作负载延迟降低 9.89 倍**。端到端 79.73 秒 → 8.06 秒（三个 seed 的均值）。

源参考素材（1）

[
[下载视频参考](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)

视频 1 · 含原始音频 · [原始输入](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)

完整提示词复制完整提示词

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

### 1 段短片段 · 15 秒请求

362 帧 · 24 FPS · 立体声 · 匹配的提示词、参考素材、seed 与 GPU 数量

**Base**
平均延迟 140.29 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-clip-15s-seed0.mp4).
](media/posters/base-clip-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-clip-15s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-clip-15s-seed0.mp4)

**FastH3 Omni**
平均延迟 11.76 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-clip-15s-seed0.mp4).
](media/posters/fast-clip-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-clip-15s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-clip-15s-seed0.mp4)

**FastH3 Omni · 36L VAE**
质量对比

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-clip-15s-seed0.mp4).
](media/posters/decoder36-clip-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-clip-15s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-clip-15s-seed0.mp4)

**该工作负载延迟降低 11.93 倍**。端到端 140.29 秒 → 11.76 秒（三个 seed 的均值）。

源参考素材（1）

[
[下载视频参考](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)

视频 1 · 含原始音频 · [原始输入](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)

完整提示词复制完整提示词

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

### 1 段长片段 · 5 秒请求

124 帧 · 24 FPS · 立体声 · 匹配的提示词、参考素材、seed 与 GPU 数量

**Base**
平均延迟 69.93 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-video-5s-seed0.mp4).
](media/posters/base-video-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-video-5s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-video-5s-seed0.mp4)

**FastH3 Omni**
平均延迟 8.34 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-video-5s-seed0.mp4).
](media/posters/fast-video-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-video-5s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-video-5s-seed0.mp4)

**FastH3 Omni · 36L VAE**
质量对比

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-video-5s-seed0.mp4).
](media/posters/decoder36-video-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-video-5s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-video-5s-seed0.mp4)

**该工作负载延迟降低 8.39 倍**。端到端 69.93 秒 → 8.34 秒（三个 seed 的均值）。

源参考素材（1）

[
[下载视频参考](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--official_ref2va_0_video.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--official_ref2va_0_video.mp4)

视频 1 · 含原始音频 · [原始输入](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--official_ref2va_0_video.mp4)

完整提示词复制完整提示词

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

### 1 段长片段 · 10 秒请求

243 帧 · 24 FPS · 立体声 · 匹配的提示词、参考素材、seed 与 GPU 数量

**Base**
平均延迟 139.27 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-video-10s-seed0.mp4).
](media/posters/base-video-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-video-10s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-video-10s-seed0.mp4)

**FastH3 Omni**
平均延迟 13.51 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-video-10s-seed0.mp4).
](media/posters/fast-video-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-video-10s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-video-10s-seed0.mp4)

**FastH3 Omni · 36L VAE**
质量对比

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-video-10s-seed0.mp4).
](media/posters/decoder36-video-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-video-10s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-video-10s-seed0.mp4)

**该工作负载延迟降低 10.31 倍**。端到端 139.27 秒 → 13.51 秒（三个 seed 的均值）。

源参考素材（1）

[
[下载视频参考](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--official_ref2va_0_video.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--official_ref2va_0_video.mp4)

视频 1 · 含原始音频 · [原始输入](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--official_ref2va_0_video.mp4)

完整提示词复制完整提示词

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

### 1 段长片段 · 15 秒请求

362 帧 · 24 FPS · 立体声 · 匹配的提示词、参考素材、seed 与 GPU 数量

**Base**
平均延迟 215.75 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-video-15s-seed0.mp4).
](media/posters/base-video-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-video-15s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-video-15s-seed0.mp4)

**FastH3 Omni**
平均延迟 18.41 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-video-15s-seed0.mp4).
](media/posters/fast-video-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-video-15s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-video-15s-seed0.mp4)

**FastH3 Omni · 36L VAE**
质量对比

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-video-15s-seed0.mp4).
](media/posters/decoder36-video-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-video-15s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-video-15s-seed0.mp4)

**该工作负载延迟降低 11.72 倍**。端到端 215.75 秒 → 18.41 秒（三个 seed 的均值）。

源参考素材（1）

[
[下载视频参考](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--official_ref2va_0_video.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--official_ref2va_0_video.mp4)

视频 1 · 含原始音频 · [原始输入](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--official_ref2va_0_video.mp4)

完整提示词复制完整提示词

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

### 3 段片段 · 5 秒请求

124 帧 · 24 FPS · 立体声 · 匹配的提示词、参考素材、seed 与 GPU 数量

**Base**
平均延迟 74.35 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-clips3-5s-seed0.mp4).
](media/posters/base-clips3-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-clips3-5s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-clips3-5s-seed0.mp4)

**FastH3 Omni**
平均延迟 9.45 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-clips3-5s-seed0.mp4).
](media/posters/fast-clips3-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-clips3-5s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-clips3-5s-seed0.mp4)

**FastH3 Omni · 36L VAE**
质量对比

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-clips3-5s-seed0.mp4).
](media/posters/decoder36-clips3-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-clips3-5s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-clips3-5s-seed0.mp4)

**该工作负载延迟降低 7.87 倍**。端到端 74.35 秒 → 9.45 秒（三个 seed 的均值）。

源参考素材（3）

[
[下载视频参考](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)

视频 1 · 含原始音频 · [原始输入](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)

[
[下载视频参考](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_robot_arm_red_cube_2s.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_robot_arm_red_cube_2s.mp4)

视频 2 · 含原始音频 · [原始输入](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_robot_arm_red_cube_2s.mp4)

[
[下载视频参考](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_h3_cinematic_shot_2s.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_h3_cinematic_shot_2s.mp4)

视频 3 · 含原始音频 · [原始输入](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_h3_cinematic_shot_2s.mp4)

完整提示词复制完整提示词

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

### 3 段片段 · 10 秒请求

243 帧 · 24 FPS · 立体声 · 匹配的提示词、参考素材、seed 与 GPU 数量

**Base**
平均延迟 132.62 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-clips3-10s-seed0.mp4).
](media/posters/base-clips3-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-clips3-10s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-clips3-10s-seed0.mp4)

**FastH3 Omni**
平均延迟 13.55 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-clips3-10s-seed0.mp4).
](media/posters/fast-clips3-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-clips3-10s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-clips3-10s-seed0.mp4)

**FastH3 Omni · 36L VAE**
质量对比

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-clips3-10s-seed0.mp4).
](media/posters/decoder36-clips3-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-clips3-10s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-clips3-10s-seed0.mp4)

**该工作负载延迟降低 9.79 倍**。端到端 132.62 秒 → 13.55 秒（三个 seed 的均值）。

源参考素材（3）

[
[下载视频参考](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)

视频 1 · 含原始音频 · [原始输入](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)

[
[下载视频参考](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_robot_arm_red_cube_2s.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_robot_arm_red_cube_2s.mp4)

视频 2 · 含原始音频 · [原始输入](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_robot_arm_red_cube_2s.mp4)

[
[下载视频参考](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_h3_cinematic_shot_2s.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_h3_cinematic_shot_2s.mp4)

视频 3 · 含原始音频 · [原始输入](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_h3_cinematic_shot_2s.mp4)

完整提示词复制完整提示词

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

### 3 段片段 · 15 秒请求

362 帧 · 24 FPS · 立体声 · 匹配的提示词、参考素材、seed 与 GPU 数量

**Base**
平均延迟 206.44 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-clips3-15s-seed0.mp4).
](media/posters/base-clips3-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-clips3-15s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-clips3-15s-seed0.mp4)

**FastH3 Omni**
平均延迟 18.38 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-clips3-15s-seed0.mp4).
](media/posters/fast-clips3-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-clips3-15s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-clips3-15s-seed0.mp4)

**FastH3 Omni · 36L VAE**
质量对比

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-clips3-15s-seed0.mp4).
](media/posters/decoder36-clips3-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-clips3-15s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-clips3-15s-seed0.mp4)

**该工作负载延迟降低 11.23 倍**。端到端 206.44 秒 → 18.38 秒（三个 seed 的均值）。

源参考素材（3）

[
[下载视频参考](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)

视频 1 · 含原始音频 · [原始输入](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)

[
[下载视频参考](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_robot_arm_red_cube_2s.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_robot_arm_red_cube_2s.mp4)

视频 2 · 含原始音频 · [原始输入](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_robot_arm_red_cube_2s.mp4)

[
[下载视频参考](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_h3_cinematic_shot_2s.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_h3_cinematic_shot_2s.mp4)

视频 3 · 含原始音频 · [原始输入](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_h3_cinematic_shot_2s.mp4)

完整提示词复制完整提示词

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

### 图片 + 视频 + 声音 · 5 秒请求

124 帧 · 24 FPS · 立体声 · 匹配的提示词、参考素材、seed 与 GPU 数量

**Base**
平均延迟 94.14 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-mixed-5s-seed0.mp4).
](media/posters/base-mixed-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-mixed-5s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-mixed-5s-seed0.mp4)

**FastH3 Omni**
平均延迟 13.06 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-mixed-5s-seed0.mp4).
](media/posters/fast-mixed-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-mixed-5s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-mixed-5s-seed0.mp4)

**FastH3 Omni · 36L VAE**
质量对比

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-mixed-5s-seed0.mp4).
](media/posters/decoder36-mixed-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-mixed-5s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-mixed-5s-seed0.mp4)

**该工作负载延迟降低 7.21 倍**。端到端 94.14 秒 → 13.06 秒（三个 seed 的均值）。

源参考素材（3）

[![提供给三个版本的图片 1](media/inputs/hf_character_action_reference.png)](media/inputs/hf_character_action_reference.png)

图片 1 · [原始输入](media/inputs/hf_character_action_reference.png)

[
[下载视频参考](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--official_ref2va_0_video.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--official_ref2va_0_video.mp4)

视频 1 · 含原始音频 · [原始输入](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--official_ref2va_0_video.mp4)

[下载音频参考](media/inputs/official_ref2va_1_audio.mp3)

音频 1 · [原始输入](media/inputs/official_ref2va_1_audio.mp3)

完整提示词复制完整提示词

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

### 图片 + 视频 + 声音 · 10 秒请求

243 帧 · 24 FPS · 立体声 · 匹配的提示词、参考素材、seed 与 GPU 数量

**Base**
平均延迟 172.37 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-mixed-10s-seed0.mp4).
](media/posters/base-mixed-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-mixed-10s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-mixed-10s-seed0.mp4)

**FastH3 Omni**
平均延迟 19.75 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-mixed-10s-seed0.mp4).
](media/posters/fast-mixed-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-mixed-10s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-mixed-10s-seed0.mp4)

**FastH3 Omni · 36L VAE**
质量对比

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-mixed-10s-seed0.mp4).
](media/posters/decoder36-mixed-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-mixed-10s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-mixed-10s-seed0.mp4)

**该工作负载延迟降低 8.73 倍**。端到端 172.37 秒 → 19.75 秒（三个 seed 的均值）。

源参考素材（3）

[![提供给三个版本的图片 1](media/inputs/hf_character_action_reference.png)](media/inputs/hf_character_action_reference.png)

图片 1 · [原始输入](media/inputs/hf_character_action_reference.png)

[
[下载视频参考](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--official_ref2va_0_video.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--official_ref2va_0_video.mp4)

视频 1 · 含原始音频 · [原始输入](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--official_ref2va_0_video.mp4)

[下载音频参考](media/inputs/official_ref2va_1_audio.mp3)

音频 1 · [原始输入](media/inputs/official_ref2va_1_audio.mp3)

完整提示词复制完整提示词

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

### 图片 + 视频 + 声音 · 15 秒请求

362 帧 · 24 FPS · 立体声 · 匹配的提示词、参考素材、seed 与 GPU 数量

**Base**
平均延迟 257.71 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-mixed-15s-seed0.mp4).
](media/posters/base-mixed-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-mixed-15s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-mixed-15s-seed0.mp4)

**FastH3 Omni**
平均延迟 26.71 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-mixed-15s-seed0.mp4).
](media/posters/fast-mixed-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-mixed-15s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-mixed-15s-seed0.mp4)

**FastH3 Omni · 36L VAE**
质量对比

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-mixed-15s-seed0.mp4).
](media/posters/decoder36-mixed-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-mixed-15s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-mixed-15s-seed0.mp4)

**该工作负载延迟降低 9.65 倍**。端到端 257.71 秒 → 26.71 秒（三个 seed 的均值）。

源参考素材（3）

[![提供给三个版本的图片 1](media/inputs/hf_character_action_reference.png)](media/inputs/hf_character_action_reference.png)

图片 1 · [原始输入](media/inputs/hf_character_action_reference.png)

[
[下载视频参考](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--official_ref2va_0_video.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--official_ref2va_0_video.mp4)

视频 1 · 含原始音频 · [原始输入](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--official_ref2va_0_video.mp4)

[下载音频参考](media/inputs/official_ref2va_1_audio.mp3)

音频 1 · [原始输入](media/inputs/official_ref2va_1_audio.mp3)

完整提示词复制完整提示词

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

### 9 张图片 + 3 段片段 · 5 秒请求

124 帧 · 24 FPS · 立体声 · 匹配的提示词、参考素材、seed 与 GPU 数量

**Base**
平均延迟 219.90 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-full-5s-seed0.mp4).
](media/posters/base-full-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-full-5s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-full-5s-seed0.mp4)

**FastH3 Omni**
平均延迟 37.38 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-full-5s-seed0.mp4).
](media/posters/fast-full-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-full-5s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-full-5s-seed0.mp4)

**FastH3 Omni · 36L VAE**
质量对比

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-full-5s-seed0.mp4).
](media/posters/decoder36-full-5s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-full-5s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-full-5s-seed0.mp4)

**该工作负载延迟降低 5.88 倍**。端到端 219.90 秒 → 37.38 秒（三个 seed 的均值）。

源参考素材（12）

[![提供给三个版本的图片 1](media/inputs/square_character_action_reference.png)](media/inputs/square_character_action_reference.png)

图片 1 · [原始输入](media/inputs/square_character_action_reference.png)

[![提供给三个版本的图片 2](media/inputs/square_official_fl2va_0_image.png)](media/inputs/square_official_fl2va_0_image.png)

图片 2 · [原始输入](media/inputs/square_official_fl2va_0_image.png)

[![提供给三个版本的图片 3](media/inputs/square_fashion_glasses_reference_1.png)](media/inputs/square_fashion_glasses_reference_1.png)

图片 3 · [原始输入](media/inputs/square_fashion_glasses_reference_1.png)

[![提供给三个版本的图片 4](media/inputs/square_fashion_glasses_reference_2.png)](media/inputs/square_fashion_glasses_reference_2.png)

图片 4 · [原始输入](media/inputs/square_fashion_glasses_reference_2.png)

[![提供给三个版本的图片 5](media/inputs/square_fashion_glasses_reference_3.png)](media/inputs/square_fashion_glasses_reference_3.png)

图片 5 · [原始输入](media/inputs/square_fashion_glasses_reference_3.png)

[![提供给三个版本的图片 6](media/inputs/square_fl2va_clay_fox_reference.png)](media/inputs/square_fl2va_clay_fox_reference.png)

图片 6 · [原始输入](media/inputs/square_fl2va_clay_fox_reference.png)

[![提供给三个版本的图片 7](media/inputs/square_h3_cinematic_shot_3s.png)](media/inputs/square_h3_cinematic_shot_3s.png)

图片 7 · [原始输入](media/inputs/square_h3_cinematic_shot_3s.png)

[![提供给三个版本的图片 8](media/inputs/square_h3_suspense_title_2s.png)](media/inputs/square_h3_suspense_title_2s.png)

图片 8 · [原始输入](media/inputs/square_h3_suspense_title_2s.png)

[![提供给三个版本的图片 9](media/inputs/square_robot_arm_red_cube_1s.png)](media/inputs/square_robot_arm_red_cube_1s.png)

图片 9 · [原始输入](media/inputs/square_robot_arm_red_cube_1s.png)

[
[下载视频参考](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)

视频 1 · 含原始音频 · [原始输入](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)

[
[下载视频参考](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_robot_arm_red_cube_2s.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_robot_arm_red_cube_2s.mp4)

视频 2 · 含原始音频 · [原始输入](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_robot_arm_red_cube_2s.mp4)

[
[下载视频参考](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_h3_cinematic_shot_2s.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_h3_cinematic_shot_2s.mp4)

视频 3 · 含原始音频 · [原始输入](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_h3_cinematic_shot_2s.mp4)

完整提示词复制完整提示词

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

### 9 张图片 + 3 段片段 · 10 秒请求

243 帧 · 24 FPS · 立体声 · 匹配的提示词、参考素材、seed 与 GPU 数量

**Base**
平均延迟 314.16 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-full-10s-seed0.mp4).
](media/posters/base-full-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-full-10s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-full-10s-seed0.mp4)

**FastH3 Omni**
平均延迟 48.38 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-full-10s-seed0.mp4).
](media/posters/fast-full-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-full-10s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-full-10s-seed0.mp4)

**FastH3 Omni · 36L VAE**
质量对比

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-full-10s-seed0.mp4).
](media/posters/decoder36-full-10s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-full-10s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-full-10s-seed0.mp4)

**该工作负载延迟降低 6.49 倍**。端到端 314.16 秒 → 48.38 秒（三个 seed 的均值）。

源参考素材（12）

[![提供给三个版本的图片 1](media/inputs/square_character_action_reference.png)](media/inputs/square_character_action_reference.png)

图片 1 · [原始输入](media/inputs/square_character_action_reference.png)

[![提供给三个版本的图片 2](media/inputs/square_official_fl2va_0_image.png)](media/inputs/square_official_fl2va_0_image.png)

图片 2 · [原始输入](media/inputs/square_official_fl2va_0_image.png)

[![提供给三个版本的图片 3](media/inputs/square_fashion_glasses_reference_1.png)](media/inputs/square_fashion_glasses_reference_1.png)

图片 3 · [原始输入](media/inputs/square_fashion_glasses_reference_1.png)

[![提供给三个版本的图片 4](media/inputs/square_fashion_glasses_reference_2.png)](media/inputs/square_fashion_glasses_reference_2.png)

图片 4 · [原始输入](media/inputs/square_fashion_glasses_reference_2.png)

[![提供给三个版本的图片 5](media/inputs/square_fashion_glasses_reference_3.png)](media/inputs/square_fashion_glasses_reference_3.png)

图片 5 · [原始输入](media/inputs/square_fashion_glasses_reference_3.png)

[![提供给三个版本的图片 6](media/inputs/square_fl2va_clay_fox_reference.png)](media/inputs/square_fl2va_clay_fox_reference.png)

图片 6 · [原始输入](media/inputs/square_fl2va_clay_fox_reference.png)

[![提供给三个版本的图片 7](media/inputs/square_h3_cinematic_shot_3s.png)](media/inputs/square_h3_cinematic_shot_3s.png)

图片 7 · [原始输入](media/inputs/square_h3_cinematic_shot_3s.png)

[![提供给三个版本的图片 8](media/inputs/square_h3_suspense_title_2s.png)](media/inputs/square_h3_suspense_title_2s.png)

图片 8 · [原始输入](media/inputs/square_h3_suspense_title_2s.png)

[![提供给三个版本的图片 9](media/inputs/square_robot_arm_red_cube_1s.png)](media/inputs/square_robot_arm_red_cube_1s.png)

图片 9 · [原始输入](media/inputs/square_robot_arm_red_cube_1s.png)

[
[下载视频参考](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)

视频 1 · 含原始音频 · [原始输入](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)

[
[下载视频参考](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_robot_arm_red_cube_2s.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_robot_arm_red_cube_2s.mp4)

视频 2 · 含原始音频 · [原始输入](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_robot_arm_red_cube_2s.mp4)

[
[下载视频参考](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_h3_cinematic_shot_2s.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_h3_cinematic_shot_2s.mp4)

视频 3 · 含原始音频 · [原始输入](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_h3_cinematic_shot_2s.mp4)

完整提示词复制完整提示词

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

### 9 张图片 + 3 段片段 · 15 秒请求

362 帧 · 24 FPS · 立体声 · 匹配的提示词、参考素材、seed 与 GPU 数量

**Base**
平均延迟 422.20 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-full-15s-seed0.mp4).
](media/posters/base-full-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-full-15s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--base-full-15s-seed0.mp4)

**FastH3 Omni**
平均延迟 59.77 秒

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-full-15s-seed0.mp4).
](media/posters/fast-full-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-full-15s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--fast-full-15s-seed0.mp4)

**FastH3 Omni · 36L VAE**
质量对比

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-full-15s-seed0.mp4).
](media/posters/decoder36-full-15s-seed0.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-full-15s-seed0.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--outputs--decoder36-full-15s-seed0.mp4)

**该工作负载延迟降低 7.06 倍**。端到端 422.20 秒 → 59.77 秒（三个 seed 的均值）。

源参考素材（12）

[![提供给三个版本的图片 1](media/inputs/square_character_action_reference.png)](media/inputs/square_character_action_reference.png)

图片 1 · [原始输入](media/inputs/square_character_action_reference.png)

[![提供给三个版本的图片 2](media/inputs/square_official_fl2va_0_image.png)](media/inputs/square_official_fl2va_0_image.png)

图片 2 · [原始输入](media/inputs/square_official_fl2va_0_image.png)

[![提供给三个版本的图片 3](media/inputs/square_fashion_glasses_reference_1.png)](media/inputs/square_fashion_glasses_reference_1.png)

图片 3 · [原始输入](media/inputs/square_fashion_glasses_reference_1.png)

[![提供给三个版本的图片 4](media/inputs/square_fashion_glasses_reference_2.png)](media/inputs/square_fashion_glasses_reference_2.png)

图片 4 · [原始输入](media/inputs/square_fashion_glasses_reference_2.png)

[![提供给三个版本的图片 5](media/inputs/square_fashion_glasses_reference_3.png)](media/inputs/square_fashion_glasses_reference_3.png)

图片 5 · [原始输入](media/inputs/square_fashion_glasses_reference_3.png)

[![提供给三个版本的图片 6](media/inputs/square_fl2va_clay_fox_reference.png)](media/inputs/square_fl2va_clay_fox_reference.png)

图片 6 · [原始输入](media/inputs/square_fl2va_clay_fox_reference.png)

[![提供给三个版本的图片 7](media/inputs/square_h3_cinematic_shot_3s.png)](media/inputs/square_h3_cinematic_shot_3s.png)

图片 7 · [原始输入](media/inputs/square_h3_cinematic_shot_3s.png)

[![提供给三个版本的图片 8](media/inputs/square_h3_suspense_title_2s.png)](media/inputs/square_h3_suspense_title_2s.png)

图片 8 · [原始输入](media/inputs/square_h3_suspense_title_2s.png)

[![提供给三个版本的图片 9](media/inputs/square_robot_arm_red_cube_1s.png)](media/inputs/square_robot_arm_red_cube_1s.png)

图片 9 · [原始输入](media/inputs/square_robot_arm_red_cube_1s.png)

[
[下载视频参考](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)

视频 1 · 含原始音频 · [原始输入](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)

[
[下载视频参考](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_robot_arm_red_cube_2s.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_robot_arm_red_cube_2s.mp4)

视频 2 · 含原始音频 · [原始输入](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_robot_arm_red_cube_2s.mp4)

[
[下载视频参考](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_h3_cinematic_shot_2s.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_h3_cinematic_shot_2s.mp4)

视频 3 · 含原始音频 · [原始输入](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_h3_cinematic_shot_2s.mp4)

完整提示词复制完整提示词

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

JavaScript 已禁用：全部 27 个配对配置都会显示。

1344×768 · 24 FPS · 立体声。下载保留生成的 MP4。延迟为三个 seed 的均值；所示视频使用 seed 0。

展示 [36 层 VAE](/blogs/fasth3-v21/#nvfp4-vae-decoders) 是为了对比质量；其延迟不计入时间数据。

## 结果一览[#](#results-at-a-glance)

在 27 个配对工作负载上，FastH3 Omni 在八张 GB200 GPU 上的端到端延迟比 Base **低 5.6–11.9 倍**。计时包含参考素材编码、生成、解码与最终 MP4，目标画布为 1344×768。

两条通道都使用原始视频 VAE。Base 使用 SGLang 的 `quality="lossless"` 策略，而非更严格的 `exact` 策略。这里比较的是完整模型与服务配方；见[基准方法](#benchmark-methodology)。

请求片段长度
5 秒10 秒15 秒

选择一行即可观看其配对输出。

Base · 50 次评估 FastH3 Omni · 8 次评估

[1 张图片
35.44 s
5.67 s
**6.25× ↗**](#omniref-example-image-5s)[图片 + 声音
35.92 s
5.84 s
**6.15× ↗**](#omniref-example-image-voice-5s)[3 张图片
73.09 s
12.42 s
**5.88× ↗**](#omniref-example-images3-5s)[9 张图片
121.61 s
21.59 s
**5.63× ↗**](#omniref-example-images9-5s)[1 段短片段
36.06 s
5.17 s
**6.98× ↗**](#omniref-example-clip-5s)[1 段长片段
69.93 s
8.34 s
**8.39× ↗**](#omniref-example-video-5s)[3 段片段
74.35 s
9.45 s
**7.87× ↗**](#omniref-example-clips3-5s)[图片 + 视频 + 声音
94.14 s
13.06 s
**7.21× ↗**](#omniref-example-mixed-5s)[9 张图片 + 3 段片段
219.90 s
37.38 s
**5.88× ↗**](#omniref-example-full-5s)

[1 张图片
78.53 s
9.37 s
**8.38× ↗**](#omniref-example-image-10s)[图片 + 声音
79.92 s
9.71 s
**8.23× ↗**](#omniref-example-image-voice-10s)[3 张图片
131.25 s
19.15 s
**6.85× ↗**](#omniref-example-images3-10s)[9 张图片
193.95 s
30.80 s
**6.30× ↗**](#omniref-example-images9-10s)[1 段短片段
79.73 s
8.06 s
**9.89× ↗**](#omniref-example-clip-10s)[1 段长片段
139.27 s
13.51 s
**10.31× ↗**](#omniref-example-video-10s)[3 段片段
132.62 s
13.55 s
**9.79× ↗**](#omniref-example-clips3-10s)[图片 + 视频 + 声音
172.37 s
19.75 s
**8.73× ↗**](#omniref-example-mixed-10s)[9 张图片 + 3 段片段
314.16 s
48.38 s
**6.49× ↗**](#omniref-example-full-10s)

[1 张图片
139.69 s
14.14 s
**9.88× ↗**](#omniref-example-image-15s)[图片 + 声音
140.91 s
14.44 s
**9.76× ↗**](#omniref-example-image-voice-15s)[3 张图片
206.88 s
26.53 s
**7.80× ↗**](#omniref-example-images3-15s)[9 张图片
282.81 s
41.57 s
**6.80× ↗**](#omniref-example-images9-15s)[1 段短片段
140.29 s
11.76 s
**11.93× ↗**](#omniref-example-clip-15s)[1 段长片段
215.75 s
18.41 s
**11.72× ↗**](#omniref-example-video-15s)[3 段片段
206.44 s
18.38 s
**11.23× ↗**](#omniref-example-clips3-15s)[图片 + 视频 + 声音
257.71 s
26.71 s
**9.65× ↗**](#omniref-example-mixed-15s)[9 张图片 + 3 段片段
422.20 s
59.77 s
**7.06× ↗**](#omniref-example-full-15s)

平均延迟，含音频与 MP4 交付。两条通道都使用原始 VAE。

查看全部 27 项时间及其示例

1344×768，24 FPS，八张 GB200 GPU。生成时间以秒计，均值 ± 样本标准差；越低越好。Target 指请求的输出长度。

| 参考素材 | 目标 | Base | FastH3 Omni | Base / FastH3 | 提示词、输入与输出 |
| --- | --- | --- | --- | --- | --- |
| 1 张图片 | 5 秒 | [35.44 ± 0.06](#omniref-example-image-5s) | [5.67 ± 0.02](#omniref-example-image-5s) | 6.25× | [查看示例 ↓](#omniref-example-image-5s) |
| 1 张图片 | 10 秒 | [78.53 ± 0.01](#omniref-example-image-10s) | [9.37 ± 0.01](#omniref-example-image-10s) | 8.38× | [查看示例 ↓](#omniref-example-image-10s) |
| 1 张图片 | 15 秒 | [139.69 ± 0.12](#omniref-example-image-15s) | [14.14 ± 0.01](#omniref-example-image-15s) | 9.88× | [查看示例 ↓](#omniref-example-image-15s) |
| 图片 + 声音 | 5 秒 | [35.92 ± 0.07](#omniref-example-image-voice-5s) | [5.84 ± 0.01](#omniref-example-image-voice-5s) | 6.15× | [查看示例 ↓](#omniref-example-image-voice-5s) |
| 图片 + 声音 | 10 秒 | [79.92 ± 0.06](#omniref-example-image-voice-10s) | [9.71 ± 0.15](#omniref-example-image-voice-10s) | 8.23× | [查看示例 ↓](#omniref-example-image-voice-10s) |
| 图片 + 声音 | 15 秒 | [140.91 ± 0.06](#omniref-example-image-voice-15s) | [14.44 ± 0.00](#omniref-example-image-voice-15s) | 9.76× | [查看示例 ↓](#omniref-example-image-voice-15s) |
| 3 张图片 | 5 秒 | [73.09 ± 0.98](#omniref-example-images3-5s) | [12.42 ± 0.01](#omniref-example-images3-5s) | 5.88× | [查看示例 ↓](#omniref-example-images3-5s) |
| 3 张图片 | 10 秒 | [131.25 ± 0.02](#omniref-example-images3-10s) | [19.15 ± 0.06](#omniref-example-images3-10s) | 6.85× | [查看示例 ↓](#omniref-example-images3-10s) |
| 3 张图片 | 15 秒 | [206.88 ± 0.14](#omniref-example-images3-15s) | [26.53 ± 0.01](#omniref-example-images3-15s) | 7.80× | [查看示例 ↓](#omniref-example-images3-15s) |
| 9 张图片 | 5 秒 | [121.61 ± 0.05](#omniref-example-images9-5s) | [21.59 ± 0.01](#omniref-example-images9-5s) | 5.63× | [查看示例 ↓](#omniref-example-images9-5s) |
| 9 张图片 | 10 秒 | [193.95 ± 0.05](#omniref-example-images9-10s) | [30.80 ± 0.01](#omniref-example-images9-10s) | 6.30× | [查看示例 ↓](#omniref-example-images9-10s) |
| 9 张图片 | 15 秒 | [282.81 ± 0.05](#omniref-example-images9-15s) | [41.57 ± 0.01](#omniref-example-images9-15s) | 6.80× | [查看示例 ↓](#omniref-example-images9-15s) |
| 1 段短片段 | 5 秒 | [36.06 ± 0.13](#omniref-example-clip-5s) | [5.17 ± 0.01](#omniref-example-clip-5s) | 6.98× | [查看示例 ↓](#omniref-example-clip-5s) |
| 1 段短片段 | 10 秒 | [79.73 ± 0.02](#omniref-example-clip-10s) | [8.06 ± 0.01](#omniref-example-clip-10s) | 9.89× | [查看示例 ↓](#omniref-example-clip-10s) |
| 1 段短片段 | 15 秒 | [140.29 ± 0.17](#omniref-example-clip-15s) | [11.76 ± 0.01](#omniref-example-clip-15s) | 11.93× | [查看示例 ↓](#omniref-example-clip-15s) |
| 1 段长片段 | 5 秒 | [69.93 ± 0.00](#omniref-example-video-5s) | [8.34 ± 0.00](#omniref-example-video-5s) | 8.39× | [查看示例 ↓](#omniref-example-video-5s) |
| 1 段长片段 | 10 秒 | [139.27 ± 0.02](#omniref-example-video-10s) | [13.51 ± 0.03](#omniref-example-video-10s) | 10.31× | [查看示例 ↓](#omniref-example-video-10s) |
| 1 段长片段 | 15 秒 | [215.75 ± 0.17](#omniref-example-video-15s) | [18.41 ± 0.04](#omniref-example-video-15s) | 11.72× | [查看示例 ↓](#omniref-example-video-15s) |
| 3 段片段 | 5 秒 | [74.35 ± 0.09](#omniref-example-clips3-5s) | [9.45 ± 0.01](#omniref-example-clips3-5s) | 7.87× | [查看示例 ↓](#omniref-example-clips3-5s) |
| 3 段片段 | 10 秒 | [132.62 ± 0.06](#omniref-example-clips3-10s) | [13.55 ± 0.04](#omniref-example-clips3-10s) | 9.79× | [查看示例 ↓](#omniref-example-clips3-10s) |
| 3 段片段 | 15 秒 | [206.44 ± 0.21](#omniref-example-clips3-15s) | [18.38 ± 0.01](#omniref-example-clips3-15s) | 11.23× | [查看示例 ↓](#omniref-example-clips3-15s) |
| 图片 + 视频 + 声音 | 5 秒 | [94.14 ± 0.07](#omniref-example-mixed-5s) | [13.06 ± 0.00](#omniref-example-mixed-5s) | 7.21× | [查看示例 ↓](#omniref-example-mixed-5s) |
| 图片 + 视频 + 声音 | 10 秒 | [172.37 ± 0.10](#omniref-example-mixed-10s) | [19.75 ± 0.00](#omniref-example-mixed-10s) | 8.73× | [查看示例 ↓](#omniref-example-mixed-10s) |
| 图片 + 视频 + 声音 | 15 秒 | [257.71 ± 0.06](#omniref-example-mixed-15s) | [26.71 ± 0.01](#omniref-example-mixed-15s) | 9.65× | [查看示例 ↓](#omniref-example-mixed-15s) |
| 9 张图片 + 3 段片段 | 5 秒 | [219.90 ± 0.14](#omniref-example-full-5s) | [37.38 ± 0.03](#omniref-example-full-5s) | 5.88× | [查看示例 ↓](#omniref-example-full-5s) |
| 9 张图片 + 3 段片段 | 10 秒 | [314.16 ± 0.13](#omniref-example-full-10s) | [48.38 ± 0.04](#omniref-example-full-10s) | 6.49× | [查看示例 ↓](#omniref-example-full-10s) |
| 9 张图片 + 3 段片段 | 15 秒 | [422.20 ± 0.22](#omniref-example-full-15s) | [59.77 ± 0.05](#omniref-example-full-15s) | 7.06× | [查看示例 ↓](#omniref-example-full-15s) |

下载[时间 CSV](/blogs/fastvideo-omniref-update/data/latency.csv)或[完整基准 JSON](/blogs/fastvideo-omniref-update/data/benchmark.json)。

## PDD + DMD[#](#pdd--dmd)

FastH3 Omni 把**并行解码蒸馏（PDD）**与**分布匹配蒸馏（DMD）**结合起来。PDD 在每次 transformer 评估中预测多个去噪更新；DMD 帮助训练完整的视频与音频输出。参考条件在整个生成过程中保持。方法及其图示见 [PDD 论文](https://arxiv.org/abs/2607.26004)。

* **PDD：每次前向多个更新。** 学生的输出头从单个速度预测扩展为 32 区间的细时间网格。推理时这些头以八个「四区间」融合块运行，于是一次 transformer 评估推进四个区间，整条轨迹只需八次评估，而不是 Base 的 50 次。一个教师监督的头损失让每个头的更新与冻结的 Base 模型保持一致。
* **DMD：匹配最终输出。** 在 PDD 之上，一个可训练的 critic 对学生样本的分布建模，同时由冻结的 Base 教师提供目标；学生被更新以缩小两者在完整视频与音频上的差距，而不只是每个单独步骤。critic 与学生的更新交替进行，每次学生更新伴随多次 critic 更新。
* **参考素材保持为干净的条件。** 参考图片、视频与音频从不去噪：它们在每次前向中为 student、teacher 与 critic 提供条件，只有目标视频与音频进入加噪与损失。
* **全程稀疏。** 学生以 128 行的瓦片使用 Video Sparse Attention 训练与采样，因此服务时使用的稀疏度正是它训练时的稀疏度。

非常感谢 [NVIDIA FastGen](https://github.com/NVlabs/FastGen) 团队（Julius Berner、Chao Liu 与 Arash Vahdat），他们提出了 PDD，本模型建立在其 DMD2 框架与 H3 参考工作之上。FastVideo 的 PDD 与 DMPDD 训练器把 [FastGen 仓库](https://github.com/NVlabs/FastGen)中的 PDD 目标适配到 FastVideo 的 MiniMax H3 模型、序列并行与检查点接口。

| 训练 | 数量 |
| --- | --- |
| GPU | 64 张 NVIDIA B300 |
| 训练步数 | 3,500 |
| 估算算力 | 约 7,800 GPU 小时 |

训练代码在 FastVideo 中：见 [FastH3 Omni DMPDD 训练指南](https://github.com/hao-ai-lab/FastVideo/blob/main/docs/training/omniref_dmpdd.md)。

## 用 FastVideo 的本地 AI[#](#local-ai-with-fastvideo)

FastH3 Omni 也能通过 **FastVideo 在 NVIDIA DGX Spark 与 RTX 5090 上本地运行**。先从 [FastVideo cookbook](https://haoailab.com/FastVideo/cookbook/) 与 [FastH3 Omni 配方生成器](https://haoailab.com/FastVideo/cookbook/minimax-h3/fasth3-omniref/)开始，然后按[本地推理指南](https://github.com/hao-ai-lab/FastVideo/blob/main/docs/inference/fasth3_omniref.md)做模型设置与参考输入。

| 设备 | 权重与推理配方 |
| --- | --- |
| DGX Spark（GB10，128 GB 统一内存） | [NVFP4 QAD 权重](https://huggingface.co/FastVideo/FastH3-Omni-NVFP4-QAD) · [`spark` 配方](https://github.com/hao-ai-lab/FastVideo/blob/main/examples/inference/basic/basic_fasth3_omniref_spark.yaml) |
| RTX 5090（32 GB） | [NVFP4 QAD 权重](https://huggingface.co/FastVideo/FastH3-Omni-NVFP4-QAD) · [`rtx-5090` 配方](https://github.com/hao-ai-lab/FastVideo/blob/main/examples/inference/basic/basic_fasth3_omniref_rtx5090.yaml) |

**QAD 指量化感知蒸馏：** 这些权重是为在 Blackwell 上以 NVFP4 执行而训练的。按 [DGX Spark 设置指南](https://haoailab.com/FastVideo/getting_started/installation/spark/)或 [NVIDIA GPU 设置指南](https://haoailab.com/FastVideo/getting_started/installation/gpu/)安装 FastVideo。两个设备配置默认 480p；Spark 把模型组件常驻内存，而 RTX 5090 配置会卸载文本编码器并要求预计算 AdaLN 表。本地推理指南涵盖准备该表、组装模型目录与选择解码器。请保留配方中的 attention 与精度设置。

**ComfyUI 中的 FP8** 请使用 [FastH3 Omni FP8 ComfyUI 检查点](https://huggingface.co/FastVideo/FastH3-Omni-FP8-Comfy)。FastVideo 原生推理需要兼容的 dense 或 FP8 导出；按指南中的 [FP8 设备配置](https://github.com/hao-ai-lab/FastVideo/blob/main/docs/inference/fasth3_omniref.md#device-profiles)与 [RTX 4090 配方](https://github.com/hao-ai-lab/FastVideo/blob/main/examples/inference/basic/basic_fasth3_omniref_rtx4090.yaml)做逐层卸载。文本编码器也必须与硬件匹配：随附的 NVFP4 编码器需要 Blackwell，因此其它 GPU 需要兼容的 BF16 编码器组件。NVFP4 QAD 与 FP8 是不同的数值变体；它们的输出可能与 BF16 版本不同。

可选的 [NVFP4 VAE 解码器](https://huggingface.co/FastVideo/FastH3-NVFP4-VAE-Decoder)提供 **36 层质量**档与 **8 层快速**档。按指南的 `--decoder` 设置操作；这些本地配置有自己的分辨率、显存与精度选择，因此上面的八卡 GB200 计时并不代表它们的速度。

## 用 UniServe 部署 FastH3 Omni[#](#deploy-fasth3-omni-with-uniserve)

在每个节点上安装 [UniServe](https://github.com/hao-ai-lab/uniserve)：

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

然后选择你的 GPU，在 UniServe 检出目录中运行这些步骤：

模型

GPU

GPU 数

优化目标

检查点

精度

最长片段

最长提示词

参考素材尺寸

部署文件 

随 UniServe 提供；传给 `--workers`。复制下载

[UniServe 服务指南](https://github.com/hao-ai-lab/uniserve/blob/main/docs/minimax_h3/minimax_h3.md)涵盖所有选项与请求字段。

## 基准方法[#](#benchmark-methodology)

九种参考素材组合 × 三种片段长度（5、10、15 秒），在八张 GB200 GPU 上测量。每个配置一次预热、三个测量 seed；图集统一展示 seed 0。

阅读测量设置与数值策略

* **硬件与范围。** 两台四卡托盘上的八张 NVIDIA GB200 GPU。GB200 是我们对 B200 的代理；B200 未单独测量。这些结果描述的是八卡这一组。
* **匹配的输入。** 九种参考素材组合 × 三种请求长度，全部为 1344×768、24 FPS。对齐后的输出含 124、243 或 362 帧。图片使用已发布的放大参考模式，短边 2048 像素。参考片段保留其真实音轨，独立音频仍是真实输入。
* **测量。** 一次一个请求，每个配置先用 seed 42 预热一次，然后测量 seed 0、1、2。表中报告的是从客户端到完整 MP4 可用的算术平均端到端时间；可下载数据还包含样本标准差。模型加载与服务器启动不计入。没有从缺失单元格或显存失败推断任何延迟，也没有把任何计时归一化到别的工作负载。
* **模型与运行时。** Base 是 MiniMax H3 Ref2VA，50 次去噪评估；FastH3 Omni 使用 32 区间的 PDD 学生，八次融合评估并启用 VSA。Base 通道使用 Ulysses 4 × Ring 2 与原生 FlashAttention transformer 后端；学生使用八路 Ulysses。条件缓存已禁用。模型权重、attention 模式与服务实现都不同，因此这里比较的是完整的模型/运行时配方，而不是孤立的蒸馏或 kernel 消融。
* **Base 的数值策略。** 这些 Base 测量使用 SGLang 的 `quality="lossless"` 策略，配原始未量化权重、稠密 attention 与模型的混合精度规则。它的 DiT 归一化/调制与 VAE 融合可能改变中间舍入。它们不是 SGLang 更严格的 `quality="exact"` 策略的测量，也没有确立与原参考逐位一致或感知等价。原始模型并非统一 BF16：它保留了 FP32 敏感的 DiT 运算与已发布 VAE 的混合精度执行。所示延迟未换算为 exact 策略下的估计。
* **如何解读示例。** 时间统计使用三个 seed；图集统一使用 seed 0。共享 seed 并不意味着不同模型或运行时之间的输出在数值或感知上一致。示例支持直接查看，不是定量的质量评测。

## 开始使用[#](#get-started)

从 [FastH3 Omni collection](https://huggingface.co/collections/FastVideo/fasth3-omni)下载模型权重，然后按 [UniServe 设置](#deploy-fasth3-omni-with-uniserve)用你自己的参考素材生成视频与音频。

## 致谢[#](#acknowledgements)

FastH3 构建于 [MiniMax H3](https://huggingface.co/MiniMaxAI/MiniMax-H3) 之上。感谢 MiniMax 团队发布权重与代码。

感谢 NVIDIA Enterprise Products 团队（Pengcheng Li 与 Cliff Woolley）提供 FastH3 使用的 Video Sparse Attention kernel。感谢 [NVIDIA FastGen](https://github.com/NVlabs/FastGen) 团队（Julius Berner、Chao Liu 与 Arash Vahdat）提供 DMD2 框架与 H3 参考工作，并提出[并行解码蒸馏](https://research.nvidia.com/labs/genair/pdd/)。

感谢 [Nuva Lab](https://nuvalab.ai/) 把扎根生产的创意视频工作流带到 FastH3，也感谢上游服务、kernel 与开源社区——是他们的实现让这些实验成为可能。我们同样感谢 [Reactor](https://www.reactor.inc/) 对 FastH3 Omni 的支持，以及 [vLLM 项目](https://vllm.ai/)、[NVIDIA](https://www.nvidia.com/en-us/) 与 [MBZUAI](https://mbzuai.ac.ae/) 对 FastVideo 的支持。
