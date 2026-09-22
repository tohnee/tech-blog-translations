---
title: "Grok Imagine 1.5 Preview"
date: 2026-06-03
source: https://x.ai/news/grok-imagine-1-5
crawled: 2026-09-22
---

[Back to news](/news)

Jun 3, 2026

# Grok Imagine 1.5 Preview

grok-imagine-video-1.5-preview, our latest image-to-video model, is now available via the xAI API in preview.

---

[Create API key](https://console.x.ai/team/default/api-keys?campaign=grok-imagine-1-5-blog)

Our latest image-to-video model, `grok-imagine-video-1.5-preview`, is now available via the xAI API in preview.

`grok-imagine-video-1.5-preview` turns a single still image into fluid, cinematic video. Give it a starting frame and a prompt describing the motion, and it animates the scene, including camera moves, atmosphere, and physics, while staying faithful to your source image. You can generate clips at up to 720p.

[![

Your browser does not support the video tag.

](/images/news/grok-imagine-1-5/prompt-to-video-poster.jpg)](/images/news/grok-imagine-1-5/prompt-to-video.mp4)

Direct the shot with natural-language prompts. Describe the camera move, the pacing, and the sound design, then set your resolution and clip length. The model holds detail and lighting from the input frame, so the result continues the original image rather than reinterpreting it.

The model also works well for sequences. Stage each frame, animate it, and chain the shots together into longer scenes that keep a consistent look across an entire project.

[![

Your browser does not support the video tag.

](/images/news/grok-imagine-1-5/imagine-gallery-poster.jpg)](/images/news/grok-imagine-1-5/imagine-gallery.webm)

Animate an image in a few lines of code.

Copy

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
