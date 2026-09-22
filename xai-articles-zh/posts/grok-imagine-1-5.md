---
title: "Grok Imagine 1.5 预览版"
title_en: "Grok Imagine 1.5 Preview"
date: 2026-06-03
source: https://x.ai/news/grok-imagine-1-5
crawled: 2026-09-22
translated: 2026-09-22
---

# Grok Imagine 1.5 预览版

> 原文：[Grok Imagine 1.5 Preview](https://x.ai/news/grok-imagine-1-5) · xAI

[返回新闻列表](/news)

2026 年 6 月 3 日

我们最新的图生视频模型 grok-imagine-video-1.5-preview，现已在 xAI API 上以预览版提供。

---

[创建 API 密钥](https://console.x.ai/team/default/api-keys?campaign=grok-imagine-1-5-blog)

我们最新的图生视频模型 `grok-imagine-video-1.5-preview`，现已在 xAI API 上以预览版提供。

`grok-imagine-video-1.5-preview` 能把单张静态图像变成流畅、电影感的视频。给它一个起始帧和一段描述运动的提示词，它就会让场景动起来——包括镜头运动、氛围和物理效果——同时忠实于你的源图像。你可以生成最高 720p 的片段。

[![

您的浏览器不支持 video 标签。

](/images/news/grok-imagine-1-5/prompt-to-video-poster.jpg)](/images/news/grok-imagine-1-5/prompt-to-video.mp4)

用自然语言提示词执导镜头。描述镜头运动、节奏和声音设计，然后设定分辨率和片段长度。模型会保留输入帧的细节和光照，因此结果是原图的延续，而不是重新演绎。

该模型同样适用于序列创作。为每一帧布景、生成动画，再把镜头串联成更长的场景，让整个项目保持一致的观感。

[![

您的浏览器不支持 video 标签。

](/images/news/grok-imagine-1-5/imagine-gallery-poster.jpg)](/images/news/grok-imagine-1-5/imagine-gallery.webm)

用几行代码让一张图像动起来。

复制

```
import os
import xai_sdk

client = xai_sdk.Client(api_key=os.getenv("XAI_API_KEY"))

response = client.video.generate(
    prompt="Slow cinematic push-in as embers drift across the battlefield and the helmet's crest stirs in the wind",
    model="grok-imagine-video-1.5-preview",
    image_url="https://your-host.com/helmet.jpg",
    duration=10,
    resolution="720p",
)

print(response.url)
```

python
