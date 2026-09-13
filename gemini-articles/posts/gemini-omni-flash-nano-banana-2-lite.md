---
title: "Start building with Nano Banana 2 Lite and Gemini Omni Flash"
source: https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-omni-flash-nano-banana-2-lite/
site: gemini
date: 2026-06-30
authors: Alisa Fortin
crawled: 2026-09-13
---

Today, we’re making it faster and easier to experiment, refine and scale your ideas with two major releases:

- **Introducing** [**Nano Banana 2 Lite:**](https://deepmind.google/models/gemini-image/flash-lite/) Our fastest, most cost-efficient image model in the Nano Banana family yet, built for high throughput, speed and scale. Nano Banana 2 Lite is available today in [Google AI Studio](https://aistudio.google.com/prompts/new_chat?model=gemini-3.1-flash-lite-image)**,** [Gemini API](https://ai.google.dev/gemini-api/docs/image-generation) and [Gemini Enterprise Agent Platform](https://console.cloud.google.com/agent-platform/studio/multimodal?model=gemini_omni_flash_preview)**.** It is also rolling out today in Google consumer surfaces including AI Mode in Search, Gemini app and many other products**.**
- **Bringing** [**Gemini Omni Flash**](http://deepmind.google/models/gemini-omni) **to developers:** Our high quality, cost-efficient model for video generation and conversational editing, now available in [Google AI Studio](https://aistudio.google.com/prompts/new_chat?model=gemini-omni-flash-preview&utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=)**,** the [Gemini API](https://ai.google.dev/gemini-api/docs/omni) and [Gemini Enterprise Agent Platform](https://console.cloud.google.com/agent-platform/studio/multimodal?model=gemini_omni_flash_preview) for the first time. Omni Flash is also available in the [Gemini app](http://gemini.google/) and [Google Flow](http://flow.google/).

Building with generative media is often about creative iteration. With these two models, developers can build comprehensive, end-to-end multimedia experiences that connect rapid image generation with video creation and editing. Whether your workflow requires generating thousands of images or editing multi-turn video sequences, you now have two new models to build faster, iterate seamlessly and bring your creative vision to life.

## Nano Banana 2 Lite: our fastest most cost-efficient Gemini Image model

Watch a side-by-side comparison of image generation speed and quality between Nano Banana 2 Lite and Nano Banana 2 using a simple prompt.

Nano Banana 2 Lite (gemini-3.1-flash-lite-image) is designed for rapid ideation and high-velocity developer pipelines where speed and cost are the primary constraints. It’s our recommended replacement for developers currently using our first version of Nano Banana (gemini-2.5-flash-image), you can swap it out now for immediate benefits across key performance dimensions.

Performance benchmarks for Nano Banana 2 and 2 Lite compared to competitor AI image models, evaluating trade-offs between generation/editing quality (Elo scores), processing latency and cost per 1K-resolution image.

![a gif showing image generation and editing vs latency and price](https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/nb2-lite__benchmark_blog.gif)

### Nano Banana 2 Lite shines in:

- **Latency:** Delivers text-to-image outputs in 4 seconds. This makes it ideal for interactive prototyping and rapid visual drafting.
- **Cost-efficiency ($0.034 per 1K image):** A cost-efficient choice for developers focused on drafting, ideating, managing operational budgets or low-bandwidth usage.

Despite prioritizing speed, Nano Banana 2 Lite retains reliable prompt adherence, strong character consistency and legible in-image text rendering.

### Understanding the [Nano Banana](https://ai.google.dev/gemini-api/docs/image-generation) family

![a chart showing the model table comparing Nano Banana 2 Lite, Nano Banana 2 and Nano Banana Pro](https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/Copy_of_nb2-lite__model_table_light_V2.gif)

- **Nano Banana 2 Lite (Gemini 3.1 Flash Lite Image):** Built for speed. Optimized for near-real-time, high-volume workflows where ultra-low latency is critical.
- **Nano Banana 2 (Gemini 3.1 Flash Image):** The generalist workhorse. Delivers high quality at a lower latency, offering the best balance of performance and cost.
- **Nano Banana Pro (Gemini 3 Pro Image):** Optimized for complex, professional use cases. It provides the most robust control and advanced reasoning for tasks where accuracy is more important than speed.
- **Nano Banana (Gemini 2.5 Flash Image):** Our legacy model. We recommend upgrading to Nano Banana 2 Lite for better quality, faster speeds and lower costs.

To see the full list of model capabilities and how to integrate check out the developer [docs](https://ai.google.dev/gemini-api/docs/omni).

Alongside its release on developer platforms, Nano Banana 2 Lite is also coming to Google consumer surfaces including AI Mode in Search, Gemini app, NotebookLM, Google Photos, Stitch, Google Flow, and Google Ads.

## Experience high-quality, cost-efficient video editing and generation with Gemini Omni Flash

Watch as someone uses Gemini Omni to perform four digital magic tricks, like pulling a 3D balloon word out of her phone and pouring water from the screen into a glass. There is a small “original" video in the corner revealing how she actually filmed the tricks before the Omni generated special effects were added.

At Google I/O we introduced [Gemini Omni Flash](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-omni/)**,** the model where Gemini’s multimodal reasoning meets video generation and editing. Today, Gemini Omni Flash (gemini-omni-flash-preview) is rolling to developers via the Gemini API and Google AI Studio, natively supporting high-quality video generation and conversational editing from a combination of text, image and video inputs. This model is priced competitively at $0.10 per second of video output, which is the same as Veo 3.1 Fast.

Omni Flash shines in:

- **Conversational video editing:** Refine and edit videos using natural language.
- **Multimodal referencing:** Combine inputs like images, text and video to maintain control and consistency over your scene.
- **Real-world knowledge:** Omni draws on Gemini’s knowledge such as history, biology and narrative logic to construct compelling videos.
- **Text and action synchronization:** Connect text and graphics directly to video actions, through simple prompting.

For comprehensive benchmarking information, please visit Google DeepMind's [Gemini Omni](https://deepmind.google/models/gemini-omni/) webpage.

![a benchmarking chart on video editing](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Video_Editing__-_Descending_-_Ch.width-1200.format-webp.webp)

Limitations:

- Omni offers 10-second video generations currently, with longer durations coming soon.
- Uploading audio references and scene extension is not yet supported in the Gemini API for this model.
- Video references up to 3 seconds in duration are accepted by the API schema but are not correctly processed by the model at this time.
- Character consistency when changing scenes or panning movements has some limitations but we are working to make this better.

Gemini Omni is available in public preview starting today in Google AI Studio and the Gemini API. To see the full list of model capabilities and regional specific limitations check out the developer [docs](https://ai.google.dev/gemini-api/docs/omni).

## Build with both models today

The real magic happens when you chain these models together. Use Nano Banana 2 Lite as a high-speed image generation model, then pass that image as a reference to Gemini Omni Flash to animate it into a high-quality video. Plus, by using the [Interactions API](https://ai.google.dev/api/interactions-api) for these multi-turn experiences, you can maintain session history and context so users can stack up to three sequential edits.

To help you get started we created a few demo apps you can remix that let you experience how you can pair both Nano Banana 2 Lite and Gemini Omni Flash into one workflow.

[Anywhere](https://aistudio.google.com/apps/bundled/anywhere) is a demo app built to showcase the strong capabilities of both models. Take a selfie or upload a photo, and the app uses Nano Banana 2 Lite to instantly transport you to dozens of iconic landmarks. Then, when an image is clicked, Omni Flash is used to turn the generated image into an animated clip of the location.

[Space Lift](https://aistudio.google.com/apps/bundled/space-lift) is a demo interior design app powered by Nano Banana 2 Lite and Gemini Omni, that lets you instantly reimagine any room by uploading a photo. The app automatically generates fully realized concepts across various design aesthetics. Once you find a look you love, tap the video button to watch Omni bring the design to life with a cinematic showcase, letting you experience your new space in motion before making it a reality.

[Omni product studio](https://aistudio.google.com/apps/bundled/omni-product-studio) is a demo app that converts static images created by Nano Banana 2 Lite into cinematic e-commerce videos created by Gemini Omni. This demo illustrates building interactive media by merging multimodal inputs through quick interaction with an image-to-video output.

![Quote from Ali Sadeghian, Co-Founder & CTO, Astrocade](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-omni-flash__blog-testimoni.width-100.format-webp.webp)

![Quote from Yunus Emra, CAIO, AI Lab (HubX)](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-omni-flash__blog-testimoni.width-100.format-webp_9ojqAYU.webp)

![Quote from Nick Walton, CEO & Co-Founder, Latitude](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-omni-flash__blog-testimoni.width-100.format-webp_p9M5qxu.webp)

![Quote from Path Chadha, Founder & CEO, Stan](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-omni-flash__blog-testimoni.width-100.format-webp_cTixMlp.webp)

![Quote from Joaquin Cuenca, CEO & Founder, Magnific](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-omni-flash__blog-testimoni.width-100.format-webp_RxcxodD.webp)

![Quote from Ada Liu, Head of Product, Agent Opus](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-omni-flash__blog-testimoni.width-100.format-webp_FC4Jx5D.webp)

![Quote from Andrew Carr, Co-Founder, Cartwheel](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-omni-flash__blog-testimoni.width-100.format-webp_E4dbiGT.webp)

![Quote from Alec Jo, Head of Apllied AI, Flora](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-omni-flash__blog-testimoni.width-100.format-webp_NSVqwjq.webp)

## Build with safety and transparency

Built on Google’s secure infrastructure, Gemini Omni and Nano Banana 2 Lite use [SynthID](https://deepmind.google/blog/identifying-ai-generated-images-with-synthid/) watermarking. You can verify AI content through the Gemini app, Gemini in Chrome or Search. [Learn more about](https://blog.google/innovation-and-ai/products/identifying-ai-generated-media-online) how we're expanding our verification tools to help you understand how content was created and edited across the web.

## Start your project today

Nano Banana 2 Lite resources:

- Head over to [Google AI Studio](https://aistudio.google.com/prompts/new_chat?model=gemini-3.1-flash-lite-image) to experiment with the model in the playground.
- Dive into our [Gemini API Documentation](https://ai.google.dev/gemini-api/docs/image-generation).
- Check out our Nano Banana [prompting guide](https://ai.google.dev/gemini-api/docs/image-generation#prompt-guide), filled with best practices and example prompts.

Gemini Omni Flash resources:

- Head over to [Google AI Studio](https://aistudio.google.com/prompts/new_chat?model=gemini-omni-flash-preview&utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=) to experiment with the model in the playground.
- Dive into our [Gemini API Documentation](https://ai.google.dev/gemini-api/docs/omni).
- Check out our Gemini Omni Flash [prompting guide](https://ai.google.dev/gemini-api/docs/omni#prompt-guide), filled with best practices and example prompts.
