---
title: "Gemini 3.1 Flash TTS: the next generation of expressive AI speech"
source: https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-flash-tts/
site: gemini
date: 2026-04-15
authors: Vilobh Meshram
crawled: 2026-09-13
---

Today, we’re introducing Gemini 3.1 Flash TTS, the latest text-to-speech model that delivers improved controllability, expressivity and quality — empowering developers, enterprises and everyday users to build the next generation of AI-speech applications.

Starting today, 3.1 Flash TTS is rolling out:

- For developers in preview via the Gemini API and [Google AI Studio](http://aistudio.google.com/generate-speech)
- For enterprises in preview on [Vertex AI](https://console.cloud.google.com/vertex-ai/studio/media/speech)
- For Workspace users via [Google Vids](https://docs.google.com/videos/create?usp=blog)

## Improved speech quality and controllability

We’ve improved the overall speech quality of Gemini 3.1 Flash TTS, making it our most natural and expressive model to date. On the [Artificial Analysis TTS leaderboard](https://artificialanalysis.ai/text-to-speech/models), a benchmark that captures thousands of blind human preferences, 3.1 Flash TTS achieved an impressive Elo score of 1,211.

![a gif showing artificial analysis text to speech arena quality elo](https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/gemini_flash_tts_evals_blog.gif)

Artificial Analysis has also positioned Gemini 3.1 Flash TTS within its “[most attractive quadrant](https://artificialanalysis.ai/text-to-speech/models?quality=quality-vs-price)” for its ideal blend of high-quality speech generation and low cost. The model stands out further with native multi-speaker dialogue, support for 70+ languages, and granular creative control via natural language.

## New audio tags for more expressive speech generation

3.1 Flash TTS also introduces audio tags — an intuitive way to control vocal style, pace and delivery. By embedding natural language commands directly into the text input, you can steer AI-speech output with improved levels of granularity.

## 3.1 Flash TTS supports a range of audio tags to add nuanced, engaging delivery to a synonym word hunt app.

You can start experimenting with these audio tags along with other updates to the developer experience in Google AI Studio with configurable controls that place the developer in the “director’s chair”:

- **Scene direction:** Set the stage by defining the environment and providing specific dialogue instructions. This world-building context helps characters remain “in-character” and react to one another naturally across multiple turns.
- **Speaker-level specificity:** Cast characters using unique Audio Profiles, then specify Director’s Notes to toggle pace, tone and accent. Using [inline tags](https://ai.google.dev/gemini-api/docs/speech-generation#transcript-tags), speakers can pivot from these high-level settings to change expression mid-sentence.
- **Seamless export:** Once the performance is perfected, these exact parameters can be exported as Gemini API code to ensure consistent, recognizable voices across various projects and platforms.

With these new configurations, developers can enhance precision for specific scenarios, creating memorable characters and immersive audio experiences.

Get started with high-fidelity speech generation in the [Google AI Studio Playground](http://aistudio.google.com/generate-speech).

## Built for global scale

Gemini 3.1 Flash TTS delivers high-fidelity speech and more precise control across more than 70 languages. These core optimizations bring advanced style, pacing and accent control to major markets — helping developers create localized, expressive speech experiences for users at global scale.

Early developer and enterprise testers are already seeing the impact of 3.1 Flash TTS, highlighting its impressive controllability and expressivity. They’ve told us how audio tags provide a new level of creative precision, transforming simple text into a high-fidelity vocal performance.

![Quote from Jay of StyleUAI](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3.1-flash_tts_blog_quote_1.width-100.format-webp.webp)

![Quote from CTO of AIM Intelligence](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3.1-flash_tts_blog_quote_4.width-100.format-webp.webp)

![Quote from Idan Yonas of Artlist](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3.1-flash_tts_blog_quote_5.width-100.format-webp.webp)

![Quote from Lydia Xu of Sierra](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3.1-flash_tts_blog_quote_6.width-100.format-webp.webp)

![Quote from Shivam Rastogi of Invideo AI](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3.1-flash_tts_blog_quote_7.width-100.format-webp.webp)

![Quote from Fernanda Bejarano of biia](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3.1-flash_tts_blog_quote_8.width-100.format-webp.webp)

![Quote from John Wu of HeyGen](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3.1-flash_tts_blog_quote_9.width-100.format-webp.webp)

![Quote from Soami Kapadia of You learn.AI](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3.1-flash_tts_blog_quote_1.width-100.format-webp_N5HV1Wc.webp)

![Quote from Angel Wen of Sylph.ai](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3.1-flash_tts_blog_quote_2.width-100.format-webp.webp)

![Quote from Artugrul Cavusoglu of Mindlid](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3.1-flash_tts_blog_quote_3.width-100.format-webp.webp)

## Watermarked with SynthID

All audio generated by Gemini 3.1 Flash TTS is watermarked with SynthID. This imperceptible watermark is interwoven directly into the audio output, allowing the reliable detection of AI-generated content to help prevent misinformation. For more information on our approach to safety and responsibility, you can review the [model card](https://deepmind.google/models/model-cards/gemini-3-1-flash-audio/).
