---
title: "Imagine Video 1.5 with References"
date: 2026-07-31
source: https://x.ai/news/grok-imagine-video-1-5-references
crawled: 2026-09-22
---

[Back to news](/news)

Jul 31, 2026

# Imagine Video 1.5 with References

Our best video model, now with text, image, and voice references — generating up to 1080p.

[Open Grok.com](https://grok.com/imagine?referrer=website&campaign=imagine-video-1-5-references-blog)

When we launched [Imagine Video 1.5](/news/grok-imagine-video-1-5) last month, it was our best video model yet — better motion, better physics, and better audio. Today it goes further: image and voice references, video from a prompt alone, and native 1080p generation.

Image and voice references start today in the US for SuperGrok Heavy and SuperGrok Plus on [grok.com/imagine](https://grok.com/imagine?referrer=website&campaign=imagine-video-1-5-references-blog) and [iOS](https://apps.apple.com/app/grok-ai-chat-video/id6670324846), rolling out to all tiers over the next few days.

## [Text-to-Video and native 1080p](#text-to-video-and-native-1080p)

Describe the shot — no starting image needed. Text-to-video pairs our image generation with image-to-video. Native 1080p is now supported with text-to-video and image-to-video. Text-to-video and native 1080p are generally available on grok.com/imagine, iOS, and [Android](https://play.google.com/store/apps/details?id=ai.x.grok).

## [Voice consistency](#voice-consistency)

Pass in a character image and a voice reference, and both hold — the same face and the same voice in every scene.

![Reference photo of the character](/_next/image?url=https%3A%2F%2Fmedia.x.ai%2Fv1%2Fwebsite%2Fonevoice-character-f7d66216.jpg&w=3840&q=75)

Character

Voice

## [Multi-Reference](#multi-reference)

Each reference image locks one thing in place — a face, a product, a location. Keep a character and swap the scene, keep the scene and swap the character, or hold both and change only the action. Up to seven references per generation.

![Reference photo of a man](/_next/image?url=https%3A%2F%2Fmedia.x.ai%2Fv1%2Fwebsite%2Fpodcaster-character-f50cf3a1.jpg&w=3840&q=75)

Character

![Reference photo of a podcast studio](/_next/image?url=https%3A%2F%2Fmedia.x.ai%2Fv1%2Fwebsite%2Fpodcaster-scene-5d14579c.jpg&w=3840&q=75)

Scene

![Reference photo of a man](/_next/image?url=https%3A%2F%2Fmedia.x.ai%2Fv1%2Fwebsite%2Fpodcaster-character-f50cf3a1.jpg&w=3840&q=75)

Character

![Reference photo of a warmly lit podcast studio with a leather armchair](/_next/image?url=https%3A%2F%2Fmedia.x.ai%2Fv1%2Fwebsite%2Fpodcaster-2-scene-6ac920e9.png&w=3840&q=75)

Scene

![Reference photo of a woman in a grey sweater](/_next/image?url=https%3A%2F%2Fmedia.x.ai%2Fv1%2Fwebsite%2Fpodcaster-3-character-12939291.jpg&w=3840&q=75)

Character

![Reference photo of a warmly lit podcast studio with a leather armchair](/_next/image?url=https%3A%2F%2Fmedia.x.ai%2Fv1%2Fwebsite%2Fpodcaster-2-scene-6ac920e9.png&w=3840&q=75)

Scene

## [In the API](#in-the-api)

Image references, text-to-video, and native 1080p are live in the [xAI API](https://docs.x.ai/developers/model-capabilities/video/generation) with our best video model, `grok-imagine-video-1.5`. Voice reference support is available [on request](/contact-sales?interest=imagine).

Copy

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

## [Try it today](#try-it-today)

[Open

Grok.com](https://grok.com/imagine?referrer=website&campaign=imagine-video-1-5-references-blog)[Build

Imagine API](https://console.x.ai/team/default/video?mode=reference&model=grok-imagine-video-1.5&flow=explore&campaign=imagine-video-1-5-references-blog&utm_source=website&utm_medium=referral&utm_campaign=imagine-video-1-5-references-blog)[![iOS App Store Icon](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fapp-store.14o4a9tiapc8g.png&w=48&q=75)

Open

Grok on iOS](https://apps.apple.com/us/app/grok/id6670324846)[![Android Play Store Icon](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fplay-store.12t07rhe487yz.png&w=48&q=75)

Open

Grok on Android](https://play.google.com/store/apps/details?id=ai.x.grok)
