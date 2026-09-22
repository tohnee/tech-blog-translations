---
title: "Grok Imagine Video 1.5"
title_en: "Grok Imagine Video 1.5"
date: 2026-06-16
source: https://x.ai/news/grok-imagine-video-1-5
crawled: 2026-09-22
translated: 2026-09-22
---

# Grok Imagine Video 1.5

> 原文：[Grok Imagine Video 1.5](https://x.ai/news/grok-imagine-video-1-5) · xAI

[返回新闻列表](/news)

2026 年 6 月 16 日

质量更上一层楼，速度反而更快。

[在 Grok 上试用](https://grok.com/imagine?referrer=website&campaign=imagine-video-1-5-blog)[在 API 上试用](https://console.x.ai/team/default/imagine?campaign=imagine-video-1-5-blog&mode=video)

Grok Imagine Video 1.5 现已在 [Imagine API](https://console.x.ai/team/default/imagine?campaign=imagine-video-1-5-blog&mode=video) 上正式可用。我们还把 Video 1.5 Fast 推向了 [grok.com/imagine](https://grok.com/imagine?referrer=website&campaign=imagine-video-1-5-blog) 以及我们的 [iOS](https://apps.apple.com/app/grok-ai-chat-video/id6670324846) 和 [Android](https://play.google.com/store/apps/details?id=ai.x.grok) 应用。这是我们迄今最好的图生视频模型：更好的运动、更好的物理、更好的音频，而且速度最快。我们也在为 Grok Imagine 增加完善创作工作流的新功能。

与上一代模型相比，1.5 在真实创作工作的每个关键维度上都有提升：

## [音频与语音](#audio-and-speech)

音效、环境声和对白在同一次生成中产出，并与画面精确对位。语音更清晰，同步更好。

## [运动与物理](#motion-and-physics)

运动在整个片段中保持连贯——扭曲变形更少，重量感和动量更可信。

## [速度](#speed)

Grok Imagine Video 1.5 Fast 几乎把生成速度翻倍：生成 6 秒 720p 视频约需 25 秒，而上一代模型需要 40 秒以上。

0s

上一代模型

0s

Grok Imagine Video 1.5

## [幕后花絮——Odyssey](#behind-the-scenes---odyssey)

看看 David Thompson（[@heavypulp](https://x.com/heavypulp)）如何完全用 Grok Imagine 1.5 做出配得上大银幕的预告片：

![](/_next/image?url=https%3A%2F%2Fdata.x.ai%2Freleases%2Fimagine%2Fvideo-1-5%2Fodyssey-trailer-poster.jpg&w=3840&q=75)

## [效率提升](#enhanced-productivity)

与 Imagine Video 1.5 一起，我们将在未来几天陆续推出新功能，改进你的创作工作流：

### [项目](#projects)

把你的作品组织成项目，显示在左侧边栏中。

[![](https://data.x.ai/releases/imagine/video-1-5/projects-poster.jpg)](https://data.x.ai/releases/imagine/video-1-5/projects.mp4)

### [多智能体](#multiple-agents)

在你的项目上并行启动多个智能体。不必等一次生成结束再开始下一次，你可以同时运行多条提示词，让它们同时为你干活。

[![](https://data.x.ai/releases/imagine/video-1-5/multiple-agents-poster.jpg)](https://data.x.ai/releases/imagine/video-1-5/multiple-agents.mp4)

### [搜索](#search)

通过搜索你的素材库找到任何你做过的图像或视频——再也不用翻来翻去找那一段片段了。

[![](https://data.x.ai/releases/imagine/video-1-5/search-poster.jpg)](https://data.x.ai/releases/imagine/video-1-5/search.mp4)

## [现已在 API 结束预览](#now-out-of-preview-in-the-api)

Imagine Video 1.5 已结束预览，在 [xAI API](https://docs.x.ai/developers/model-capabilities/video/generation) 中以 `grok-imagine-video-1.5` 正式可用。给它一张起始图像，描述运动，然后选择分辨率和时长。

复制

```
import os
import xai_sdk

client = xai_sdk.Client(api_key=os.getenv("XAI_API_KEY"))

response = client.video.generate(
    prompt="Slow cinematic push-in as embers drift across the battlefield and the helmet's crest stirs in the wind",
    model="grok-imagine-video-1.5",
    image_url="https://your-host.com/helmet.jpg",
    duration=10,
    resolution="720p",
)

print(response.url)
```

python

## [今天就试试](#try-it-today)

[构建

Imagine API](https://console.x.ai/team/default/imagine?campaign=imagine-video-1-5-blog&mode=video)[打开

Grok.com](https://grok.com/imagine?referrer=website&campaign=imagine-video-1-5-blog)[![iOS App Store 图标](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fapp-store.0d46h4ow-x.vz.png&w=48&q=75&dpl=a37f00c5c6cb871fa7d68ef7f3b4d4a2f20d99ce)

打开

iOS 上的 Grok](https://apps.apple.com/us/app/grok/id6670324846)[![Android Play Store 图标](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fplay-store.0cl68ca2nyhgk.png&w=48&q=75&dpl=a37f00c5c6cb871fa7d68ef7f3b4d4a2f20d99ce)

打开

Android 上的 Grok](https://play.google.com/store/apps/details?id=ai.x.grok)

我们迫不及待想看到你的作品。
