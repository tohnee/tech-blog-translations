---
title: "Fluid, natural voice translation with Gemini 3.5 Live Translate"
source: https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-live-3-5-translate/
site: gemini
date: 2026-06-09
authors: Anuda Weerasinghe
crawled: 2026-09-13
---

Twenty years ago, [translation at Google](https://blog.google/products-and-platforms/products/translate/fun-facts-google-translate-20-years/) began as one of our pioneering machine learning experiments to turn the science of language into the magic of human connection. That experiment has come a long way with over a trillion words being translated for billions of users across our products every month.

Today, we’re taking our next step with the release of Gemini 3.5 Live Translate, our latest audio model for live speech-to-speech translation.

The model automatically detects 70+ languages and generates smooth, natural-sounding translated speech that preserves the speakers' intonation, pacing and pitch. Unlike turn by turn systems that wait for the speaker to finish speaking before responding, 3.5 Live Translate generates speech continuously, balancing the trade-off between waiting for context to improve quality and translating immediately to stay in sync with the speaker. It delivers fluid audio without awkward pauses and stays just a few seconds behind the speaker throughout the session.

Gemini 3.5 Live Translate is rolling out starting today across Google products:

- For developers in public preview via the [Gemini Live API](https://ai.google.dev/gemini-api/docs/live-api/live-translate) and [Google AI Studio](https://aistudio.google.com/live?model=gemini-3.5-live-translate-preview)
- For enterprises in private preview starting this month in [Google Meet](https://workspace.google.com/products/meet/)
- For everyone via Google Translate on [Android](https://play.google.com/store/apps/details?id=com.google.android.apps.translate&26hl=en) and [iOS](https://apps.apple.com/us/app/google-translate/id414706506)

## Build with 3.5 Live Translate

Gemini 3.5 Live Translate processes speech as it’s streamed, enabling a more seamless connection across languages. The model handles multilingual inputs without the need to manually configure settings. At the same time, its noise robustness ensures applications can handle loud, unpredictable environments. You can use its capabilities to help facilitate live interpretation for multilingual calls, meetings, lessons, broadcasts and more.

Watch the Gemini Live API in action, enabling dubbing and simultaneous multi-language translation. Dive into the [demo](https://github.com/google-gemini/gemini-live-api-examples/tree/main/gemini-live-translate-livekit) or more [example code](https://github.com/google-gemini/gemini-live-api-examples) in the Gemini Cookbook.

By utilizing the Gemini Live API, developer platforms like [Agora](https://docs.agora.io/en/conversational-ai/models/mllm/gemini), [Fishjam](https://docs.fishjam.io/tutorials/gemini-live-integration), [LiveKit](https://docs.livekit.io/agents/models/realtime/plugins/gemini/), [Pipecat](https://docs.pipecat.ai/guides/features/gemini-live), and [Vision Agents](https://visionagents.ai/integrations/gemini) enable developers to build and deploy voice translation apps with ease. These integrations handle the complex real-time media streaming infrastructure, so developers can focus on the user experience.

Our partners at Grab are testing the model to enable multilingual communication in near real-time between drivers and travelers at pickups. These users make over 10 million voice calls per month through Grab.

## Read the early reviews

In addition to Grab, companies like CJ ENM, LiveKit and others have shared positive feedback on 3.5 Live Translate highlighting its impressive translation quality, accuracy and low latency:

## Experience 3.5 Live Translate in your video meetings

[Speech translation](https://support.google.com/meet/answer/16221730?hl=en) in Google Meet will soon use 3.5 Live Translate, improving the experience by:

- Offering 70+ languages, an improvement from the previous limit of just five languages,
- Enabling conversations across over 2000+ language combinations in one meeting, expanding from the previous state of only translating to and from English,
- Updating the interface to provide instant access to speech translation.

We’re launching this update in private preview for select business Google Workspace customers starting this month, followed by a broader rollout later this year.

## Get 3.5 Live Translate in the Google Translate app on Android or iOS

The model is also rolling out on the Google Translate app globally, on both [Android](https://play.google.com/store/apps/details?id=com.google.android.apps.translate) and [iOS](https://apps.apple.com/us/app/google-translate/id414706506). When using the Live translate feature, simply connect any pair of headphones to experience a more seamless translation that mirrors the speaker’s tone across 70+ languages.

For Android users, we’re also starting to roll out a new ‘listening mode’ with 3.5 Live Translate that lets you hear translations directly through your phone’s earpiece. Simply hold your phone to your ear just like a regular call, and the translated audio streams straight to you. This new experience can be helpful in situations where you want to quickly hear translations without others hearing, and you don’t have your headphones handy.

Using the new listening mode, users can hear a near real-time English translation of a guided tour in Spanish directly through their phone's earpiece.

## Watermarked with SynthID

All audio generated by our models is watermarked with SynthID. This imperceptible watermark is woven directly into the audio output, ensuring AI-generated content remains detectable to help prevent misinformation. For details on our approach to safety and responsibility, review the [model card](https://deepmind.google/models/model-cards/gemini-3-5-audio/).
