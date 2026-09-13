---
title: "Reimagining the mouse pointer for the AI era"
source: https://deepmind.google/blog/ai-pointer/
site: deepmind
date: 2026-05-12
authors: Adrien Baranes, Rob Marchant
crawled: 2026-09-13
---

We are developing more seamless, intuitive ways to collaborate with AI

The mouse pointer has been a constant companion on computer screens, across every website, document and workflow. Despite how technologies have changed, the pointer has barely evolved in more than half a century.

We’ve been exploring new AI-powered capabilities to help the pointer not only understand what it’s pointing at, but also why it matters to the user.

Our goal is to address a common frustration: because a typical AI tool lives in its own window, users need to drag their world into it. We want the opposite: intuitive AI that meets users across all the tools they use, without interrupting their flow. For example, imagine pointing to an image of a building, and requesting “Show me directions”. Nothing more is needed when the AI system already understands the context.

Today, we’re outlining the underlying principles guiding our thinking on future user interfaces, and sharing experimental demos of an AI-enabled pointer, powered by Gemini. For example, you could visit Google AI Studio to [edit an image](https://aistudio.google.com/apps/bundled/ai-pointer-create?showPreview=true&showAssistant=true&fullscreenApplet=true) or [find places on the map](https://aistudio.google.com/apps/bundled/ai-pointer-find?showPreview=true&showAssistant=true&fullscreenApplet=true), just by pointing and speaking.

![](https://lh3.googleusercontent.com/0CBS9A2z90df_b-DENgsypA2v7Wxcg_q7eqFeH8EZwmr9gFebGcVRdBwezunCAYoeKkkqZVaTWosYCnSKUz-RoLBelAG2FXR0gfpTJOxQecyltQ7=w1440-h810-n-nu)

This video showcases the experimental environment for our AI-enabled pointer. Sequences are shortened throughout.

## Our interaction principles

We’ve developed four principles that together shift the hard work of conveying context and intent from the user to the computer, replacing text-heavy prompts with simpler, more intuitive interactions. Here are illustrations of our approach and principles.

### Maintain the flow

AI capabilities should work across all apps, not force users into “AI detours” between them. Our prototype AI-enabled pointer is available wherever the user is working. For example, they could point at a PDF and request a bullet-point summary to paste directly into an email, hover over a table of statistics and request a pie chart version, or highlight a recipe and ask for all the ingredients doubled.

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

### Show and tell

Current AI models demand precise instructions. To get a good response, a user has to write a detailed prompt. An AI-enabled pointer would streamline this process by smoothly capturing the visual and semantic context around the pointer, letting the computer “see” and understand what’s important to the user. In our experimental system, just point, and the AI knows exactly which word, paragraph, part of an image, or code block the user needs help with.

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

### Embrace the power of "This" and "That"

In everyday interactions with each other, humans rarely speak in long, detailed paragraphs. We might say, "Fix this", "Move that here", or “What does this mean?” — while relying on physical gestures and our shared context to fill in any gaps in understanding. An AI system that understands this combination of context, pointing and speech would allow users to make complex requests in natural shorthand, no fiddly prompting required.

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

### Turn pixels into actionable entities

For decades, computers have only tracked *where* we are pointing. AI can now also understand *what* the user is pointing at. This transforms pixels into structured entities, such as places, dates, and objects, that users can interact with instantly. A photo of a scribbled note becomes an interactive to-do list; a paused frame in a travel video becomes a booking link for that cool-looking restaurant.

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

Building technology that adapts to human behavior — rather than forcing users to adapt to it — enables a future where collaborating with AI feels truly intuitive, fluid and seamless.

We’re excited that these human-first concepts are being woven into products we use every day.

## Applying this work in our products

We are now integrating these principles to reimagine pointing in Chrome and our new [Googlebook](https://blog.google/products-and-platforms/platforms/android/meet-googlebook) laptop experience. Starting today, instead of writing a complex prompt, you can now use your pointer to ask [Gemini in Chrome](https://gemini.google/overview/gemini-in-chrome/) about the part of the webpage you care about. For example, you can select a few products on a page and ask to compare, or point to where you want to visualize a new couch in your living room. Similarly, we'll soon roll out Magic Pointer in Googlebook, allowing users to harness Gemini at their fingertips for a more intuitive experience. Because there are so many other potentially great applications, we'll continue to test future concepts across our platforms, including [Google Labs’ Disco](https://labs.google/disco).

**Try the AI-enabled pointer in Google AI Studio**

[Edit an image](https://aistudio.google.com/apps/bundled/ai-pointer-create?showPreview=true&showAssistant=true&fullscreenApplet=true)[Find places on the map](https://aistudio.google.com/apps/bundled/ai-pointer-find?showPreview=true&showAssistant=true&fullscreenApplet=true)
