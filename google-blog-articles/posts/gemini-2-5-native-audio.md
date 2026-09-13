---
title: "Advanced audio dialog and generation with Gemini 2.5"
source: https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-2-5-native-audio/
site: google-blog
date: 2025-06-03
authors: Ankur Bapna
crawled: 2026-09-13
---

Gemini is built from the ground up to be multimodal, natively understanding and generating content across text, images, audio, video and code. At I/O we showed how Gemini 2.5 marks a significant step forward with new capabilities in AI-powered audio dialog and generation.

We’re already using these models to bring audio to users globally, across numerous products, prototypes and languages. [NotebookLM’s Audio Overviews](https://blog.google/technology/google-labs/notebooklm-audio-overviews-50-languages/) and [Project Astra](https://deepmind.google/models/project-astra/) are just two examples. Here’s a closer look at what you can do with Gemini 2.5 native audio capabilities.

## Real-time audio dialog

Human conversation is rich and nuanced, with meaning conveyed not just by *what* is said, but *how* it’s spoken — through tone, accent and even non-speech vocalizations, like laughter. We believe conversation will be a key way we interact with AI. That’s why Gemini reasons and generates speech natively in audio, enabling effective, real-time communication.

Native audio dialog with Gemini 2.5 Flash preview features:

- **Natural conversation:** Voice interactions of remarkable quality, more appropriate expressivity, and prosody (patterns of rhythm), delivered with very low latency so you can converse fluidly.
- **Style control:** Using natural language prompts, you can adapt the delivery within the conversation, steering it to adopt specific accents, produce a range of tones and expressions and even whisper.
- **Tool integration:** Gemini 2.5 can use tools and function calling during dialog. This allows it to incorporate real-time information from sources like Google Search or use custom developer-built tools, making conversations more practical.
- **Conversation context awareness (proactive audio):** Our system is trained to discern and disregard background speech, ambient conversations and other irrelevant audio, responding when appropriate. Basically, it understands when *not* to speak.
- **Audio-video understanding:** With native support from streaming audio and video, Gemini 2.5 can converse with you about what it sees in a video feed or through screen sharing.
- **Multilinguality:** Converse in any of our 24+ [supported languages](https://ai.google.dev/gemini-api/docs/speech-generation#languages), or even easily mix languages within the same phrase.
- **Affective dialog:** Gemini 2.5 responds to the user's tone of voice, recognizing that the same words spoken differently can lead to very different conversations.
- **Advanced thinking dialog:** Gemini’s reasoning capabilities can enhance its conversation, leading to overall better performance across all features. This leads to more coherent and intelligent interactions, particularly for complex reasoning tasks.

## Controllable text-to-speech (TTS)

The evolution of text-to-speech technology is moving rapidly, and with our latest models, we're moving beyond naturalness to giving unprecedented control over generated audio. Now you can generate anything from short snippets to long-form narratives, precisely dictating style, tone, emotional expression and performance — all steerable through natural language prompts.

Additional controls and capabilities include:

- **Dynamic performance:** These models can bring text to life for expressive readings for anything from poetry to newscasts to engaging storytelling. They can also perform with specific emotions and produce accents when requested.
- **Enhanced pace and pronunciation control:** Control delivery speed and ensure more accuracy in pronunciation, including for specific words.
- **Multi-speaker dialogue generation:** This model can generate two-person “[NotebookLM-style](https://blog.google/technology/ai/notebooklm-audio-overviews/)” audio overview from text input, making content more engaging through conversation.
- **Multilinguality:** Create multilingual audio content effortlessly with Gemini 2.5, offering the same support for more than 24 [languages](https://ai.google.dev/gemini-api/docs/speech-generation#languages).

For controllable speech generation (TTS), choose Gemini 2.5 Pro Preview for state-of-the-art quality on complex prompts, or Gemini 2.5 Flash Preview for cost-efficient everyday applications. This allows developers to dynamically create audio for announcements, stories, podcasts, video games and more.

## Safety and responsibility

We’ve proactively assessed potential risks throughout every stage of the development process for these native audio features, using what we’ve learned to inform our mitigation strategies. We validate these measures through rigorous internal and external safety evaluations, including comprehensive [red teaming](https://blog.google/technology/safety-security/googles-ai-red-team-the-ethical-hackers-making-ai-safer/) for responsible deployment. Additionally, all audio outputs from our models are embedded with [SynthID](https://deepmind.google/science/synthid), our watermarking technology, to ensure transparency by making AI-generated audio identifiable.

## Native audio capabilities for developers

We’re bringing native audio outputs to Gemini 2.5 models, giving developers new capabilities to build richer, more interactive applications via the Gemini API in [Google AI Studio](http://aistudio.google.com/) or [Vertex AI](https://console.cloud.google.com/freetrial?redirectPath=/vertex-ai/studio).

To begin exploring, developers can try native audio dialog with Gemini 2.5 Flash preview in Google AI Studio’s [stream](https://aistudio.google.com/live) tab. Controllable speech generation (TTS) is available in preview for both Gemini 2.5 Pro and Flash by selecting speech generation in the [generate media](http://aistudio.google.com/generate-speech) tab within Google AI Studio.
