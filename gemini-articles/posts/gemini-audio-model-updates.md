---
title: "Improved Gemini audio models for powerful voice interactions"
source: https://blog.google/products-and-platforms/products/gemini/gemini-audio-model-updates/
site: gemini
date: 2025-12-12
authors: Bibo Xu
crawled: 2026-09-13
---

Earlier this week, we introduced greater control over audio generation with an upgrade to our [Gemini 2.5 Pro and Flash Text-to-Speech models](https://blog.google/technology/developers/gemini-2-5-text-to-speech).

But generating expressive speech is only one side of the conversation. Today, we’re releasing an updated Gemini 2.5 Flash Native Audio for live voice agents. This update improves the model’s ability to handle complex workflows, navigate user instructions, and hold natural conversations.

Gemini 2.5 Flash Native Audio is now available across Google products including [Google AI Studio](https://aistudio.google.com/prompts/new_chat?model=gemini-2.5-flash-native-audio-preview-12-2025), [Vertex AI](https://cloud.google.com/blog/products/ai-machine-learning/gemini-live-api-available-on-vertex-ai), and has also started rolling out in [Gemini Live](https://gemini.google/overview/gemini-live/) and [Search Live](https://blog.google/products/search/live-audio-gemini-model-update/), bringing the naturalness of native audio to Search Live for the first time. This means you can more effectively brainstorm live with Gemini, get real-time help in Search Live, or build the next generation of enterprise-ready customer service agents.

Beyond powering helpful agents, native audio unlocks new possibilities for global communication. We’re introducing live speech translation, a capability that enables streaming speech-to-speech translation for headphones. It preserves the speaker’s intonation, pacing and pitch. This beta experience is rolling out in the [Google Translate app](https://blog.google/products/search/gemini-capabilities-translation-upgrades/) starting today.

## Live Voice Agents

To enable the breadth of use cases across surfaces and products, we have improved Gemini 2.5 Native Audio in three key areas:

- **Sharper function calling:** We’ve improved the model's reliability when triggering external functions. It can now more accurately identify when to fetch real-time information during a conversation and seamlessly weave that data back into the audio response, without breaking the flow. On [ComplexFuncBench Audio](https://github.com/zai-org/ComplexFuncBench?tab=readme-ov-file#citatio), an eval that captures multi-step function calling with various constraints, Gemini 2.5 Native Audio leads with a score of 71.5%.
- **Robust instruction following:** The model is now better at handling complex instructions resulting in higher user satisfaction on content completeness. With a 90% adherence rate to developer instructions (up from 84%), it delivers more reliable outputs.
- **Smoother conversations:** We’ve achieved significant gains in multi-turn conversation quality. Gemini 2.5 Flash Native Audio is able to retrieve context from previous turns more effectively, creating more cohesive conversations.

The updated Gemini 2.5 Flash Native Audio’s performance against previous versions and industry competitors on [ComplexFuncBench](https://github.com/zai-org/ComplexFuncBench?tab=readme-ov-file#citatio)

![updated Gemini 2.5 Flash Native Audio’s performance against previous versions and industry competitors](https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/gemini-audio_blog_light_blue_16x9_v1_25-12-12_1.gif)

### What customers are saying

[Google Cloud customers](https://cloud.google.com/blog/products/ai-machine-learning/gemini-live-api-available-on-vertex-ai) are already using Gemini’s native audio capabilities to drive real business results, from mortgage processing to customer calls.

- *“Users often forget they’re talking to AI within a minute of using Sidekick, and in some cases have thanked the bot after a long chat…New Live API AI capabilities offered through Gemini [2.5 Flash Native Audio] empower our merchants to win.”* – David Wurtz, VP of Product, Shopify
- *"By integrating the Gemini 2.5 Flash Native Audio model…we've significantly enhanced Mia's capabilities since launching in May 2025. This powerful combination has enabled us to generate over 14,000 loans for our broker partners.*" – Jason Bressler, Chief Technology Officer, United Wholesale Mortgage (UWM)
- *“Working with the Gemini 2.5 Flash Native Audio model through Vertex AI allows Newo.ai AI Receptionists to achieve unmatched conversational intelligence ... .They can identify the main speaker even in noisy settings, switch languages mid-conversation, and sound remarkably natural and emotionally expressive.”* – David Yang, Co-founder, Newo.ai

## Live Speech Translation

Gemini now natively supports new live speech-to-speech translation capabilities designed to handle both continuous listening and two-way conversation.

With continuous listening, Gemini automatically translates speech in multiple languages into a single target language. This allows you to put headphones in and hear the world around you in your language.

For two-way conversation, Gemini’s live speech translation handles translation between two languages in real-time, automatically switching the output language based on who is speaking. For example, if you speak English and want to chat with a Hindi speaker, you’ll hear English translations in real-time in your headphones, while your phone broadcasts Hindi when you’re done speaking.

Gemini’s live speech translation has a number of key capabilities that help in the real world:

- **Language coverage**: Translates speech in over 70 languages and 2000 language pairs by combining Gemini model’s world knowledge and multilingual capabilities with its native audio capabilities
- **Style transfer:** Captures the nuance of human speech, preserving the speaker’s intonation, pacing and pitch so the translation sounds natural.
- **Multilingual input:** Understands multiple languages simultaneously in a single session, helping you follow multilingual conversations without needing to fiddle around with language settings.
- **Auto detection:** Identifies the spoken language and begins translation, so you don’t even need to know what language is being spoken to start translating.
- **Noise robustness**: Filters out ambient noise so you can converse comfortably even in loud, outdoor environments.

Starting today, you can try it in a new beta experience in the Google Translate app for [real-time translation in your headphones](https://blog.google/products/search/gemini-capabilities-translation-upgrades/) by connecting them to your device and tapping “Live translate.” This experience is rolling out to all Android devices in the US, Mexico and India with support for iOS and more regions coming soon.

Based on feedback, we will continue to iterate on this experience and bring it to more Google products including the Gemini API in 2026.

## Get started today

Start building voice agents today with Gemini 2.5 Flash Native Audio, now generally available on [Vertex AI](https://cloud.google.com/blog/products/ai-machine-learning/gemini-live-api-available-on-vertex-ai) and as preview in [the Gemini API](https://ai.google.dev/gemini-api/docs/live). Try it out in [Google AI Studio](https://ai.dev/prompts/new_chat?model=gemini-2.5-flash-native-audio-preview-12-2025).

Gemini 2.5 Flash and 2.5 Pro text-to-speech models are also available via the Gemini API in Google AI Studio. Get started with the [speech generation docs](https://ai.google.dev/gemini-api/docs/speech-generation), explore the [prompting guide](https://ai.google.dev/gemini-api/docs/speech-generation#prompting-guide), or check out the [Gemini API Cookbook](https://github.com/google-gemini/cookbook/blob/main/quickstarts/Get_started_TTS.ipynb) to get started.
