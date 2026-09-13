---
title: "Gemini 3.1 Flash Live: Making audio AI more natural and reliable"
source: https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-flash-live/
site: gemini
date: 2026-03-26
authors: Valeria Wu
crawled: 2026-09-13
---

Today, we’re advancing Gemini’s real-time dialogue capabilities with Gemini 3.1 Flash Live, our highest-quality audio and voice model yet. It delivers the speed and natural rhythm needed for the next generation of voice-first AI, offering a more intuitive experience for developers, enterprises and everyday users.

3.1 Flash Live is available across Google products:

- For developers in preview via the [Gemini Live API](https://ai.google.dev/gemini-api/docs/live) in [Google AI Studio](http://ai.studio/live)
- For enterprises in [Gemini Enterprise for Customer Experience](https://cloud.google.com/products/gemini-enterprise-for-customer-experience?e=48754805)
- For everyone via [Search Live](https://blog.google/products-and-platforms/products/search/search-live-global-expansion) and [Gemini Live](https://gemini.google/overview/gemini-live/)

## For developers: Robust reasoning and task execution

We’ve improved 3.1 Flash Live’s overall quality, making it more reliable for developers and enterprises to build voice-first agents that can complete complex tasks at scale. On [ComplexFuncBench Audio](https://github.com/zai-org/ComplexFuncBench?tab=readme-ov-file), a benchmark that captures multi-step function calling with various constraints, it leads with a score of 90.8% compared to our previous model.

![ComplexFuncBench audio bar graph](https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/gemini_flash_live__complexfuncbench__eval__light_Web.gif)

![BigBenchAudio bar graph](https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/gemini_flash_live__bigbenchaudio__eval__light_Web.gif)

On Scale AI’s [Audio MultiChallenge](https://labs.scale.com/leaderboard/audiomc), Gemini 3.1 Flash Live leads with a score of 36.1% with “thinking” on. The benchmark specifically tests complex instruction following and long-horizon reasoning amidst the interruptions and hesitations typical of real-world audio.

![AudioMultiChallenge bar graph](https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/gemini_flash_live__audiomultichallenge__eval__light_Web.gif)

3.1 Flash Live also has improved tonal understanding to deliver more natural dialogue. In [Gemini Enterprise for Customer Experience](https://cloud.google.com/products/gemini-enterprise-for-customer-experience?e=48754805), it’s even more effective at recognizing acoustic nuances like pitch and pace than 2.5 Flash Native Audio. It’s also better at dynamically adjusting its response to users' expressions of frustration or confusion.

3.1 Flash Live lets you build voice-ready agents that handle complex tasks in noisy environments.

Illustrative demonstration built with Gemini 3.1 Pro, powered by Gemini 3.1 Flash Live.

3.1 Flash Live lets you use your voice to vibe code and quickly iterate.

Illustrative demonstration built with Gemini 3.1 Pro, powered by Gemini 3.1 Flash Live.

Companies like Verizon, LiveKit and The Home Depot have given positive feedback on 3.1 Flash Live in their workflows, highlighting its improved, natural conversation.

![Quote from The Home Depot](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3.1-flash_live_Enterprises.width-100.format-webp.webp)

![Quote from Verizon](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3.1-flash_live_Enterprises.width-100.format-webp_Cc2KmJB.webp)

![Quote from LiveKit](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3.1-flash_live_Developers_.width-100.format-webp.webp)

![Quote from Wavera](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3.1-flash_live_Developers_.width-100.format-webp_NV2mIWo.webp)

![Quote from Stream](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3.1-flash_live_Developers_.width-100.format-webp_7gtqzd5.webp)

![Quote from YouTube](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3.1-flash_live_Enterprises.width-100.format-webp_fbYyeA9.webp)

## For everyone: More natural and intuitive interactions

In Gemini Live and Search Live, the 3.1 Flash Live model delivers more helpful and natural responses, whether you’re asking quick daily questions or engaging in more complex conversations.

With the 3.1 Flash Live model under the hood, Gemini Live delivers faster responses compared to the previous model and it can follow the thread of your conversation for twice as long, keeping your train of thought intact during longer brainstorms.

3.1 Flash Live makes Gemini Live faster and more helpful

3.1 Flash Live is also inherently multilingual, which enables this week’s [global expansion of Search Live](https://blog.google/products-and-platforms/products/search/search-live-global-expansion). With this launch, people in more than 200 countries and territories can now have real-time, multimodal conversations with Search in their preferred language.

Get real-time troubleshooting help using 3.1 Flash Live in Search Live

## Try Gemini 3.1 Flash Live

All audio generated by 3.1 Flash Live is watermarked with SynthID. This imperceptible watermark is interwoven directly into the audio output, allowing the reliable detection of AI-generated content to help prevent misinformation. For more information on our approach to safety and responsibility, see the [model card](https://deepmind.google/models/model-cards/gemini-3-1-flash-live).

Experience the naturalness and reliability of 3.1 Flash Live, starting today. We look forward to seeing how you interact and build with it.
