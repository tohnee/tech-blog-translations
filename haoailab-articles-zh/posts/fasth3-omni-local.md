---
title: "FastH3 Omni 落地本地：DGX Spark、RTX 与 Apple Silicon"
title_en: "FastH3 Omni Goes Local: DGX Spark, RTX and Apple Silicon"
date: 2026-10-21
source: https://haoailab.com/blogs/fasth3-omni-local/
crawled: 2026-11-16
translated: 2026-11-16
---

# FastH3 Omni 落地本地：DGX Spark、RTX 与 Apple Silicon

> 原文：[FastH3 Omni Goes Local: DGX Spark, RTX and Apple Silicon](https://haoailab.com/blogs/fasth3-omni-local/) · Hao AI Lab @ UCSD

同一个 FastH3 Omni 请求，使用匹配的提示词、参考素材与随机种子，在 DGX Spark、RTX GPU 和一台 Apple M5 Max 上端到端运行。

2026 年 10 月 21 日 · 17 分钟 · Aryan Kumar、Will Lin、Hao Zhang

[![](https://img.shields.io/github/stars/hao-ai-lab/FastVideo?style=social)](https://github.com/hao-ai-lab/FastVideo)[![](https://img.shields.io/badge/🤗%20huggingface--green.svg?style=social)](https://huggingface.co/collections/FastVideo/fasth3-omni)[![Slack](https://img.shields.io/badge/Slack--4A154B?style=social&logo=slack&logoColor=blue)](https://join.slack.com/t/fastvideo/shared_invite/zt-3f4lao1uq-u~Ipx6Lt4J27AlD2y~IdLQ)

昨天我们发布了 [**FastH3 Omni**](/blogs/fastvideo-omniref-update/)：给它一段提示词，加上图片、视频片段和一段声音，它会返回一段音画同步的成品视频。在八台 GB200 上，从一张参考照片生成 5 秒 768p 片段只需 **5.7 秒**。

今天它来到你的桌面。我们把**完全相同的请求**——提示词、参考素材与随机种子都一致——端到端跑在单台与双台 **NVIDIA DGX Spark**、一块 **RTX 5090**、一块 **RTX 3090** 以及一台 **Apple M5 Max**（64 GB）上。

[![
你的浏览器不支持带音频的 MP4 视频。](media/hero/spark-montage-poster.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--hero--spark-montage-768p.mp4)

这段视频里的每个片段都在 DGX Spark 上生成——按标注使用一台或两台 Spark——素材是照片、视频片段和声音。请打开声音。

## TL;DR[#](#tldr)

* **DGX Spark 能跑通所有参考素材组合。** 从一张照片生成 5 秒 480p 片段，**单台 Spark 约 3 分钟，两台约 2 分钟**；128 GB 统一内存覆盖了我们测试的全部情形，从一张照片到三张图片、再到一段长参考视频，480p 与 768p 均可。
* **跨本地硬件。** 同样的单图请求，在 **RTX 5090** 上 **62 秒**，在 **RTX 3090** 上约 **17 分钟**（另加模型加载），在 **Apple M5 Max** 上借助 FastVideo 新的 MLX 运行时为 **19.5 分钟**（单次运行）。
* **七周提速 4.6 倍。** Spark 上的文生视频从首次本地发布时的 243 秒降到今天的 52.6 秒。FastH3 Omni 跑在同一套栈上，因此这些收益一并继承。
* **参考素材才是真正的成本。** 一张参考照片会让请求比同机文生视频慢 3.3–4.4 倍。我们会解释原因，以及如何换回其中一部分速度。

## 同一个请求，每台机器[#](#same-request-every-machine)

选一种参考素材组合，然后按 **一起播放（Play together）**。每个面板使用相同的提示词、参考素材和随机种子；不同硬件的输出会有差异，因此请比较质量而非像素。

参考素材
1 张图片图片 + 声音3 张图片1 段短片段1 段长片段
5 秒
下一个示例 →
832×480 · 5 秒 · seed 0

一起播放
全部暂停
听
DGX Spark · 36L 解码器DGX Spark · 8L 解码器Apple M5 Max · 36L 解码器全部静音

按下播放后才会开始。用「听」选择一条音轨。

### 1 张图片 · 5 秒请求

124 帧 · 24 FPS · 立体声 · 每台设备使用相同的提示词、参考素材和随机种子

**DGX Spark · 36L 解码器**
端到端 192 秒 · 三个种子的均值

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-36l-image-480p.mp4)。
](media/posters/spark1x-36l-image-480p.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-36l-image-480p.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-36l-image-480p.mp4)

**DGX Spark · 8L 解码器**
端到端 184 秒 · 三个种子的均值

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-8l-image-480p.mp4)。
](media/posters/spark1x-8l-image-480p.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-8l-image-480p.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-8l-image-480p.mp4)

**Apple M5 Max · 36L 解码器**
端到端 19.5 分钟 · 单次运行

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--m5max-36l-image-480p.mp4)。
](media/posters/m5max-36l-image-480p.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--m5max-36l-image-480p.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--m5max-36l-image-480p.mp4)

源参考素材（1）

[![每台设备都提供的图片 1](/blogs/fastvideo-omniref-update/media/inputs/hf_character_action_reference.png)](/blogs/fastvideo-omniref-update/media/inputs/hf_character_action_reference.png)

图片 1

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

### 图片 + 声音 · 5 秒请求

124 帧 · 24 FPS · 立体声 · 每台设备使用相同的提示词、参考素材和随机种子

**DGX Spark · 36L 解码器**
端到端 198 秒 · 三个种子的均值

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-36l-image-voice-480p.mp4)。
](media/posters/spark1x-36l-image-voice-480p.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-36l-image-voice-480p.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-36l-image-voice-480p.mp4)

**DGX Spark · 8L 解码器**
端到端 191 秒 · 三个种子的均值

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-8l-image-voice-480p.mp4)。
](media/posters/spark1x-8l-image-voice-480p.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-8l-image-voice-480p.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-8l-image-voice-480p.mp4)

**Apple M5 Max · 36L 解码器**
端到端 20.1 分钟 · 单次运行

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--m5max-36l-image-voice-480p.mp4)。
](media/posters/m5max-36l-image-voice-480p.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--m5max-36l-image-voice-480p.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--m5max-36l-image-voice-480p.mp4)

源参考素材（2）

[![每台设备都提供的图片 1](/blogs/fastvideo-omniref-update/media/inputs/hf_character_action_reference.png)](/blogs/fastvideo-omniref-update/media/inputs/hf_character_action_reference.png)

图片 1

[下载音频参考](/blogs/fastvideo-omniref-update/media/inputs/official_ref2va_1_audio.mp3)

音频 1

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

### 3 张图片 · 5 秒请求

124 帧 · 24 FPS · 立体声 · 每台设备使用相同的提示词、参考素材和随机种子

**DGX Spark · 36L 解码器**
端到端 10.7 分钟 · 三个种子的均值

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-36l-images3-480p.mp4)。
](media/posters/spark1x-36l-images3-480p.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-36l-images3-480p.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-36l-images3-480p.mp4)

**DGX Spark · 8L 解码器**
端到端 10.6 分钟 · 三个种子的均值

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-8l-images3-480p.mp4)。
](media/posters/spark1x-8l-images3-480p.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-8l-images3-480p.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-8l-images3-480p.mp4)

**Apple M5 Max · 36L 解码器**
端到端 59.1 分钟 · 单次运行

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--m5max-36l-images3-480p.mp4)。
](media/posters/m5max-36l-images3-480p.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--m5max-36l-images3-480p.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--m5max-36l-images3-480p.mp4)

源参考素材（3）

[![每台设备都提供的图片 1](/blogs/fastvideo-omniref-update/media/inputs/hf_character_action_reference.png)](/blogs/fastvideo-omniref-update/media/inputs/hf_character_action_reference.png)

图片 1

[![每台设备都提供的图片 2](/blogs/fastvideo-omniref-update/media/inputs/hf_fashion_glasses_reference_3.png)](/blogs/fastvideo-omniref-update/media/inputs/hf_fashion_glasses_reference_3.png)

图片 2

[![每台设备都提供的图片 3](/blogs/fastvideo-omniref-update/media/inputs/official_fl2va_0_image.png)](/blogs/fastvideo-omniref-update/media/inputs/official_fl2va_0_image.png)

图片 3

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

### 1 段短片段 · 5 秒请求

124 帧 · 24 FPS · 立体声 · 每台设备使用相同的提示词、参考素材和随机种子

**DGX Spark · 36L 解码器**
端到端 195 秒 · 三个种子的均值

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-36l-clip-480p.mp4)。
](media/posters/spark1x-36l-clip-480p.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-36l-clip-480p.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-36l-clip-480p.mp4)

**DGX Spark · 8L 解码器**
端到端 199 秒 · 三个种子的均值

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-8l-clip-480p.mp4)。
](media/posters/spark1x-8l-clip-480p.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-8l-clip-480p.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-8l-clip-480p.mp4)

**Apple M5 Max · 36L 解码器**
端到端 14.4 分钟 · 单次运行

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--m5max-36l-clip-480p.mp4)。
](media/posters/m5max-36l-clip-480p.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--m5max-36l-clip-480p.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--m5max-36l-clip-480p.mp4)

源参考素材（1）

[
[下载视频参考](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--clip_official_ref2va_0_2s.mp4)

视频 1 · 含原始音频

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

### 1 段长片段 · 5 秒请求

124 帧 · 24 FPS · 立体声 · 每台设备使用相同的提示词、参考素材和随机种子

**DGX Spark · 36L 解码器**
端到端 505 秒 · 三个种子的均值

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-36l-video-480p.mp4)。
](media/posters/spark1x-36l-video-480p.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-36l-video-480p.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-36l-video-480p.mp4)

**DGX Spark · 8L 解码器**
端到端 499 秒 · 三个种子的均值

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-8l-video-480p.mp4)。
](media/posters/spark1x-8l-video-480p.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-8l-video-480p.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--spark1x-8l-video-480p.mp4)

**Apple M5 Max · 36L 解码器**
端到端 44.3 分钟 · 单次运行

[![
[下载带音频的 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--m5max-36l-video-480p.mp4)。
](media/posters/m5max-36l-video-480p.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--m5max-36l-video-480p.mp4)
[下载 MP4](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--m5max-36l-video-480p.mp4)

源参考素材（1）

[
[下载视频参考](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--official_ref2va_0_video.mp4)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v1/fastvideo-omniref-update--media--inputs--official_ref2va_0_video.mp4)

视频 1 · 含原始音频

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

JavaScript 已禁用：所有示例均直接展示。

832×480 · 24 FPS · 立体声 · seed 0。Spark 的时间为三个种子的均值；Mac 的时间为单次运行。

## 端到端延迟[#](#end-to-end-latency)

每根柱子都是完整请求——从提示词与参考素材，到带音频的成品 MP4。

参考素材
1 张图片图片 + 声音3 张图片1 段短片段1 段长片段
分辨率
480p · 832×480768p · 1344×768
解码器
36 层（质量）8 层（快速）

DGX Spark其他机器

从请求到带音频的成品 MP4 的端到端秒数，5 秒片段（124 帧、24 FPS），seed 0，提示词与参考素材来自 [FastH3 Omni 发布](/blogs/fastvideo-omniref-update/)。越短越好。

**DGX Spark，覆盖每一种参考素材组合**（三个种子的均值，36 层解码器，5 秒片段）：

| 参考素材 | 2× Spark 480p | 1× Spark 480p | 2× Spark 768p | 1× Spark 768p |
| --- | --- | --- | --- | --- |
| 1 张图片 | **130.1 秒** | 192.0 秒 | **217.8 秒** | 361.3 秒 |
| 图片 + 声音 | **128.6 秒** | 198.3 秒 | **220.9 秒** | 378.5 秒 |
| 3 张图片 | **390.5 秒** | 640.3 秒 | **594.8 秒** | 957.9 秒 |
| 1 段短片段 | **116.2 秒** | 194.8 秒 | **200.6 秒** | 332.6 秒 |
| 1 段长片段 | **261.4 秒** | 504.6 秒 | **366.5 秒** | 656.9 秒 |

双 Spark 的运行使用了较早的 FastH3 Omni QAD 检查点，因此 1× 与 2× 的比值仅供参考。

**跨本地硬件**（480p，36 层解码器）：

| 参考素材 | 1× DGX Spark | RTX 5090 | RTX 3090 | Apple M5 Max |
| --- | --- | --- | --- | --- |
| 1 张图片 | 192.0 秒 | 61.9 秒 | 16.9 分钟 | 19.5 分钟 |
| 图片 + 声音 | 198.3 秒 | 63.6 秒 | 18.0 分钟 | 20.1 分钟 |
| 1 段短片段 | 194.8 秒 | 57.2 秒 | 14.5 分钟 | 14.4 分钟 |

M5 Max 数字为单次运行；RTX 3090 数字不含每个请求约 7 分钟的模型加载时间。

* **Spark 能在几分钟内跑完每一种组合**，两种分辨率、两种解码器均可。三图与长片段请求会触及当下 24–32 GB GPU 配置的显存上限；M5 Max 能跑，但需要 44–59 分钟。
* **两台 Spark 比一台快 1.5–1.9 倍**，长片段请求扩展性最好（480p 下 1.9 倍）。
* **解码器的重要性已经不大了。** 8 层解码器在 Spark 上只省几个百分点，因为 [NVFP4 解码器](/blogs/fasth3-v21/#nvfp4-vae-decoders) 只需几秒，瓶颈在 transformer。
* **每一类本地机器都能跑。** RTX 5090 是最快的单卡，约一分钟；RTX 3090 与 Apple M5 Max 都落在 15–20 分钟区间。

## 从文生视频到参考生成[#](#from-text-to-video-to-references)

本地硬件上的文生视频已经很快了。在 FastH3 首次落地的 Spark 上，同样是 5 秒 480p 片段，**单台 Spark 快 4.6 倍，两台快 6.8 倍**（8 层解码器；首次发布是冷启动测量），这还不算发布时我们相对公开 vLLM-Omni 配方测到的 [8.4 倍](/blogs/fasth3-local/)：

1× DGX Spark2× DGX Spark

[9 月 2 日](/blogs/fasth3-local/)FastH3 V1 · 4 步 · 完整 VAE

243 秒

209 秒

[10 月 6 日](/blogs/fasth3-rtx/)FastH3 V2 · 8 步 · NVFP4

141.4 秒

87.2 秒

[10 月 19 日](/blogs/fasth3-v21/)FastH3-QAD-v2 · 36 层解码器

58.1 秒

33.6 秒

[10 月 19 日](/blogs/fasth3-v21/)FastH3-QAD-v2 · 8 层解码器

52.6 秒

30.7 秒

DGX Spark 上的文生视频，5 秒、832×480、含音频片段的端到端秒数，按各篇博文发布的数据（9 月 2 日：冷启动；10 月 6 日与 10 月 19 日：热启动中位数）。

这些收益来自 [NVFP4](/blogs/fasth3-rtx/)（NVIDIA 的 4 位浮点格式）下的八步蒸馏，随后是[带 4-bit 注意力与 NVFP4 解码器的量化感知蒸馏](/blogs/fasth3-v21/)，把解码从 43 秒压到 2 秒以内。

在同一请求上增加一张参考照片，同一台机器会**多花 3.3–4.4 倍时间**：

文生视频（FastH3-QAD-v2）FastH3 Omni，1 张图片参考

**2× DGX Spark**带参考素材时多花 3.9 倍时间

33.6 秒

130.1 秒

**1× DGX Spark**带参考素材时多花 3.3 倍时间

58.1 秒

192 秒

RTX 5090带参考素材时多花 4.4 倍时间

14.07 秒

61.9 秒

端到端秒数，5 秒、832×480、含音频片段，36 层解码器。文生视频数据来自 [FastH3-QAD-v2 博文](/blogs/fasth3-v21/)（热启动中位数）；FastH3 Omni 数据来自本文（三个种子的均值）。

原因在于 token 数量。5 秒 480p 片段大约有 **14,400 个视频 token**。FastH3 Omni 会在训练所用的 **2048 像素画布**上读取每张参考图，这会增加约 **7,100 个 VAE token**，并在提示词里再加约 **7,100 个视觉 token**。一张照片让序列翻倍到约 29,000 token，三张照片则大致翻两番到接近 60,000。这就是三图请求在所有地方都最慢的原因。

因此参考画布是你手上最大的调节杠杆。`--reference-max-pixels match` 会把每张参考图缩到片段自身的尺寸：在 M5 Max 上，单图请求从 **19.5 分钟降到 4.7 分钟（4.2 倍）**。它需要显式开启，因为偏离了训练设定，会改变取景与动作：

**训练时的参考画布**M5 Max · 19.5 分钟

[![](media/posters/m5max-36l-image-480p.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--m5max-36l-image-480p.mp4)

**`--reference-max-pixels match`**M5 Max · 4.7 分钟

[![](media/posters/m5max-36l-image-480p-match.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-omni-local--media--outputs--m5max-36l-image-480p-match.mp4)

## 各机器上的运行方式[#](#how-it-runs-on-each-machine)

FastH3 Omni 把一个约 350 亿参数的 transformer 与一个约 320 亿参数的 Qwen3-VL 文本编码器搭配在一起，BF16 下远超 100 GB。每台机器以不同方式把它装进去。

### DGX Spark[#](#dgx-spark)

所有内容都常驻在 Spark 的 128 GB 统一内存里：4-bit NVFP4 transformer、文本编码器与解码器，阶段之间不发生卸载。注意力使用模型训练时的 128-token 瓦片上的 4-bit 稀疏注意力，而文本、参考素材与音频行以 8-bit 稠密方式运行，使条件信息不落入 FP4 舍入。

两台直连的 Spark 切分 token 序列：每台都持有完整模型，各处理一半 token。条件信息不像去噪那样能干净切分，这是加速比低于 2× 的原因之一。

可从 [Spark 指南](https://haoailab.com/FastVideo/getting_started/installation/spark/) 或 [Spark 双机指南](https://haoailab.com/FastVideo/getting_started/installation/spark_pair/) 开始。

### RTX GPU[#](#rtx-gpus)

**RTX 5090** 把 NVFP4 transformer 放在它的 32 GB 显存里。一张预计算的 155 MB 表替代了 26 GB 的 timestep 投影权重，把 transformer 从 44.5 GB 缩到 18.5 GB；文本编码器只在编码提示词时加载。

**RTX 3090** 没有 FP4 或 FP8 硬件，因此通过 [24 GB 配置](https://github.com/hao-ai-lab/FastVideo/blob/main/examples/inference/basic/basic_fasth3_omniref_rtx4090.yaml) 运行 FP8 权重配 BF16 计算，每次流式加载 transformer 的几个块。

### Apple Silicon[#](#apple-silicon)

FastH3 Omni 通过 FastVideo 的 [MLX 运行时](https://github.com/hao-ai-lab/FastVideo/pull/2000) 在 Mac 上原生运行：

* **INT6 transformer（17 GB）。** timestep 投影像 RTX 5090 上那样预先计算，INT6 把其余部分装进内存；Apple GPU 没有 FP4 单元。
* **不需要基础 VAE。** [LightVAE](https://huggingface.co/lightx2v/LightVAE) Lite 编码器（406 MB）读取参考素材，与 Blackwell 上相同的 NVFP4 解码器写出画面。
* **NVFP4 文本编码器原样运行**，包括其视觉塔。
* **Metal 上的训练稀疏性**，通过为模型 128-token 稀疏注意力瓦片新增的 Metal kernel 实现。

M5 Max 的峰值内存在全部五种负载下都保持在 27 到 31 GB 之间。

## 量化感知蒸馏[#](#quantization-aware-distillation)

把蒸馏好的八步模型在训练后直接舍入到 4 bit，会损失质量。**量化感知蒸馏（QAD）** 则相反：让 NVFP4 学生模型对着全精度教师训练，从第一步起就启用 FP4 数值，从而让权重学会吸收舍入误差。稀疏注意力门控与归一化层保持冻结，因为重新训练它们会改变被选中的瓦片。

FastH3 Omni 的本地权重 [`FastVideo/FastH3-Omni-NVFP4-QAD`](https://huggingface.co/FastVideo/FastH3-Omni-NVFP4-QAD) 把 [FastH3-QAD-v2 配方](/blogs/fasth3-v21/) 扩展到 4-bit 注意力。共享的训练配方见 [FastVideo #1989](https://github.com/hao-ai-lab/FastVideo/pull/1989)。

## 上手试用[#](#try-it)

| 机器 | 权重与配方 |
| --- | --- |
| DGX Spark | [NVFP4 QAD 权重](https://huggingface.co/FastVideo/FastH3-Omni-NVFP4-QAD) · [`spark` 配方](https://github.com/hao-ai-lab/FastVideo/blob/main/examples/inference/basic/basic_fasth3_omniref_spark.yaml) |
| 2× DGX Spark | [NVFP4 QAD 权重](https://huggingface.co/FastVideo/FastH3-Omni-NVFP4-QAD) · [`spark-pair` 配方](https://github.com/hao-ai-lab/FastVideo/blob/main/examples/inference/basic/basic_fasth3_omniref_spark_pair.yaml) |
| RTX 5090 | [NVFP4 QAD 权重](https://huggingface.co/FastVideo/FastH3-Omni-NVFP4-QAD) · [`rtx-5090` 配方](https://github.com/hao-ai-lab/FastVideo/blob/main/examples/inference/basic/basic_fasth3_omniref_rtx5090.yaml) |
| 24 GB RTX GPU | [FP8 权重](https://huggingface.co/FastVideo/FastH3-Omni-FP8-Comfy) · [`rtx-4090` 配方](https://github.com/hao-ai-lab/FastVideo/blob/main/examples/inference/basic/basic_fasth3_omniref_rtx4090.yaml) |
| Apple Silicon | [BF16 发布](https://huggingface.co/FastVideo/FastVideo-FastH3-Omni-8-Step-V1)，本地转换 · [Apple Silicon 配方](https://haoailab.com/FastVideo/cookbook/minimax-h3/models/fasth3-omniref-mlx/) |

从 [FastVideo cookbook](https://haoailab.com/FastVideo/cookbook/) 与 [FastH3 Omni 配方生成器](https://haoailab.com/FastVideo/cookbook/minimax-h3/fasth3-omniref/) 开始。

更喜欢可视化工作流？本地社区一直在用我们的 [ComfyUI 版本](https://huggingface.co/FastVideo/FastH3-Omni-Comfy) 做出[很棒的成果](#from-the-community)，提供 [NVFP4 QAD](https://huggingface.co/FastVideo/FastH3-Omni-NVFP4-QAD-Comfy) 与 [FP8](https://huggingface.co/FastVideo/FastH3-Omni-FP8-Comfy) 两种格式。

## 来自社区[#](#from-the-community)

发布后一天之内，就有人在用自己的 GPU 跑 FastH3 Omni 了：

**RTX 3090 · 24 GB**15 秒片段约 12 分钟

> FastH3-OmniRef（INT8版）をRTX 3090でローカル生成してみました。参照画像5枚から、5人が順番に登場してあいさつする15秒の動画です。
>
> — AIひよこ (@AibeginnerR8) [2026 年 10 月 21 日](https://x.com/AibeginnerR8/status/2112831271185388002)

**RTX 4070 · 12 GB**416 秒，稠密路径 1312 秒

> FastH3 OmniRefをComfyUIで実測！（RTX 4070 12GB／縦1024×1792・5秒）
>
> — Kamimoto (@sep\_is\_heim) [2026 年 10 月 21 日](https://x.com/sep_is_heim/status/2112748834464170432)

**16 GB GPU**5 秒片段约 3 分钟

> FastH3 OmniRef、試してみました。アニメのダンス動画と曲を渡すと、実写の子がその振り付けのまま曲に合わせて踊ってくれます
>
> — NookWright (@nookwright) [2026 年 10 月 21 日](https://x.com/nookwright/status/2112740667956871372)

**RTX 4090 · 24 GB**15 秒片段 4 分钟

> FastH3 Omni 8Stepsのテスト。4090で15秒が生成4分。
>
> — Alone1M (@Alone1Moon) [2026 年 10 月 21 日](https://x.com/Alone1Moon/status/2112930098013946059)

**RTX 4090 · 24 GB**15 秒 480p，用时 1:24

> Been testing FastH3 Omni in @comfyui since the weights were released yesterday on my 4090 RTX.
>
> — OrctonAI (@OrctonAI) [2026 年 10 月 21 日](https://x.com/OrctonAI/status/2112955932216791381)

**RTX 5090 · 32 GB**115 秒，基线 555 秒

> MiniMax-H3の8step蒸留モデル「FastH3-Omni」をComfyUIで検証✨ RTX 5090 / R2V / 768×1344 / 5秒
>
> — DeepForest (@DeepForest\_Inc) [2026 年 10 月 21 日](https://x.com/DeepForest_Inc/status/2112770785970413929)

**RTX 5090 · 32 GB**313 秒，基线 742 秒

> MiniMax-H3の8step蒸留モデル「FastH3-Omni」をComfyUIで比較 RTX 5090 / R2V / 1024×576 / 約15秒
>
> — まぷて (@mapte\_fireball) [2026 年 10 月 21 日](https://x.com/mapte_fireball/status/2112807768633831534)

**RTX 5090 · 32 GB**NVFP4 QAD 下 4:39

> 14,4s Video, same prompt, same references (image, voice), same seed. On a 5090
>
> — Mathias\_M (@matze2001) [2026 年 10 月 21 日](https://x.com/matze2001/status/2112878541327028466)

**ComfyUI**「快得离谱，而且准确」

> FastH3 Omni is insanely fast, accurate, and overall a very good model! i highly recommend!
>
> — Rebel AI (@realrebelai) [2026 年 10 月 21 日](https://x.com/realrebelai/status/2112679911614030179)

社区自测数据，各自基于不同的配置与设置。可继续滚动查看更多；点击帖子可打开。

## 下一步[#](#whats-next)

我们会继续推进 FastH3 Omni 在 Apple Silicon 上能做到的事，持续提升每台机器上的质量与速度，并发布更小的模型，以适配更广泛的消费级硬件。

## 局限[#](#limitations)

* NVFP4、FP8 与 INT6 是不同数值变体，因此相同随机种子下，输出与 BF16 版本、以及彼此之间都会有差异。
* M5 Max 数字为单次运行，RTX 3090 数字不含模型加载，双 Spark 运行使用了较早的 QAD 检查点。
* `--reference-max-pixels match` 是用参考细节换速度。

## 致谢[#](#acknowledgements)

FastH3 构建于 [MiniMax H3](https://huggingface.co/MiniMaxAI/MiniMax-H3) 之上。感谢 MiniMax 团队发布其权重与代码。

感谢 NVIDIA Enterprise Products 团队（Pengcheng Li 与 Cliff Woolley）为 FastH3 提供的 Video Sparse Attention kernel。感谢 [NVIDIA FastGen](https://github.com/NVlabs/FastGen) 团队（Julius Berner、Chao Liu 与 Arash Vahdat）提供 DMD2 框架与 H3 参考生成工作，并引入 [Parallel Decoding Distillation](https://research.nvidia.com/labs/genair/pdd/)。

感谢 [Nuva Lab](https://nuvalab.ai/) 把贴近生产环境的创意视频工作流带到 FastH3，也感谢上游的 serving、kernel 与开源社区——正是它们的实现让这些实验成为可能。我们还要感谢 [Reactor](https://www.reactor.inc/) 对 FastH3 Omni 的支持，以及 [vLLM 项目](https://vllm.ai/)、[NVIDIA](https://www.nvidia.com/en-us/) 与 [MBZUAI](https://mbzuai.ac.ae/) 对 FastVideo 的支持。

最后，感谢社区成员 [@posi\_posi8](https://x.com/posi_posi8)，他自愿提供了一台 Apple M5 Max 为本文基准测试 FastH3 Omni。

## FastVideo 团队[#](#fastvideo-team)

**贡献者：** [Aryan Kumar](https://github.com/aryan5v)

  
**技术负责人：** [Will Lin](https://github.com/SolitaryThinker)

  
**指导：** [Hao Zhang](https://github.com/zhisbug)
