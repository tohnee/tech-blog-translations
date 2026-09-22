---
title: "支持参考的 Imagine Video 1.5"
title_en: "Imagine Video 1.5 with References"
date: 2026-07-31
source: https://x.ai/news/grok-imagine-video-1-5-references
crawled: 2026-09-22
translated: 2026-09-22
---

# 支持参考的 Imagine Video 1.5

> 原文：[Imagine Video 1.5 with References](https://x.ai/news/grok-imagine-video-1-5-references) · xAI

[返回新闻列表](/news)

2026 年 7 月 31 日

我们最好的视频模型，现在支持文本、图像和语音参考——最高可生成 1080p。

[打开 Grok.com](https://grok.com/imagine?referrer=website&campaign=imagine-video-1-5-references-blog)

上个月我们发布 [Imagine Video 1.5](/news/grok-imagine-video-1-5) 时，它已是我们最好的视频模型——更好的运动、更好的物理、更好的音频。今天它更进一步：图像与语音参考、纯提示词生成视频，以及原生 1080p 生成。

图像与语音参考今天起在美国面向 SuperGrok Heavy 和 SuperGrok Plus 用户，在 [grok.com/imagine](https://grok.com/imagine?referrer=website&campaign=imagine-video-1-5-references-blog) 和 [iOS](https://apps.apple.com/app/grok-ai-chat-video/id6670324846) 上线，并将在未来几天推广至所有档位。

## [文生视频与原生 1080p](#text-to-video-and-native-1080p)

直接描述镜头——不需要起始图像。文生视频将我们的图像生成与图生视频配对。原生 1080p 现已支持文生视频和图生视频。文生视频和原生 1080p 已在 grok.com/imagine、iOS 和 [Android](https://play.google.com/store/apps/details?id=ai.x.grok) 上正式可用。

## [语音一致性](#voice-consistency)

传入一张角色图像和一段语音参考，两者都会保持——每个场景中都是同一张脸、同一个声音。

![角色参考照片](/_next/image?url=https%3A%2F%2Fmedia.x.ai%2Fv1%2Fwebsite%2Fonevoice-character-f7d66216.jpg&w=3840&q=75)

角色

语音

## [多参考](#multi-reference)

每张参考图像锁定一样东西——一张脸、一件产品、一处场景。保留角色换场景，保留场景换角色，或者两者都保留、只改变动作。每次生成最多支持七张参考图。

![男子参考照片](/_next/image?url=https%3A%2F%2Fmedia.x.ai%2Fv1%2Fwebsite%2Fpodcaster-character-f50cf3a1.jpg&w=3840&q=75)

角色

![播客工作室参考照片](/_next/image?url=https%3A%2F%2Fmedia.x.ai%2Fv1%2Fwebsite%2Fpodcaster-scene-5d14579c.jpg&w=3840&q=75)

场景

![男子参考照片](/_next/image?url=https%3A%2F%2Fmedia.x.ai%2Fv1%2Fwebsite%2Fpodcaster-character-f50cf3a1.jpg&w=3840&q=75)

角色

![暖光播客工作室（配皮质扶手椅）参考照片](/_next/image?url=https%3A%2F%2Fmedia.x.ai%2Fv1%2Fwebsite%2Fpodcaster-2-scene-6ac920e9.png&w=3840&q=75)

场景

![灰色毛衣女子参考照片](/_next/image?url=https%3A%2F%2Fmedia.x.ai%2Fv1%2Fwebsite%2Fpodcaster-3-character-12939291.jpg&w=3840&q=75)

角色

![暖光播客工作室（配皮质扶手椅）参考照片](/_next/image?url=https%3A%2F%2Fmedia.x.ai%2Fv1%2Fwebsite%2Fpodcaster-2-scene-6ac920e9.png&w=3840&q=75)

场景

## [在 API 中](#in-the-api)

图像参考、文生视频和原生 1080p 现已在 [xAI API](https://docs.x.ai/developers/model-capabilities/video/generation) 中随我们最好的视频模型 `grok-imagine-video-1.5` 一同上线。语音参考支持可[按需申请](/contact-sales?interest=imagine)。

复制

```
import os
import xai_sdk

client = xai_sdk.Client(api_key=os.getenv("XAI_API_KEY"))

response = client.video.generate(
    prompt="Slow cinematic push-in as embers drift across the battlefield and the helmet's crest stirs in the wind",
    model="grok-imagine-video-1.5",
    reference_image_urls=["https://example.com/helmet.jpg"],
    duration=6,
    aspect_ratio="16:9",
    resolution="720p",
)

print(response.url)
```

python

## [今天就试试](#try-it-today)

[打开

Grok.com](https://grok.com/imagine?referrer=website&campaign=imagine-video-1-5-references-blog)[构建

Imagine API](https://console.x.ai/team/default/video?mode=reference&model=grok-imagine-video-1.5&flow=explore&campaign=imagine-video-1-5-references-blog&utm_source=website&utm_medium=referral&utm_campaign=imagine-video-1-5-references-blog)[![iOS App Store 图标](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fapp-store.14o4a9tiapc8g.png&w=48&q=75)

打开

iOS 上的 Grok](https://apps.apple.com/us/app/grok/id6670324846)[![Android Play Store 图标](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fplay-store.12t07rhe487yz.png&w=48&q=75)

打开

Android 上的 Grok](https://play.google.com/store/apps/details?id=ai.x.grok)
