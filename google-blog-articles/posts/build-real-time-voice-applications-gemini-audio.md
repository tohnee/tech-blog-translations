---
title: "Build real-time voice applications with Gemini 3.8 Live and 3.5 Transcribe"
source: https://blog.google/innovation-and-ai/technology/developers-tools/build-real-time-voice-applications-gemini-audio/
site: google-blog
date: 2026-09-15
authors: Alisa Fortin
crawled: 2026-09-18
---

Today, we [released](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-8-live-gemini-3-8-live-extended-thinking/) new Gemini Live models in the [Gemini API](https://ai.google.dev/gemini-api/docs/live) and [Google AI Studio](http://ai.studio/live), expanding our developer suite for building real-time, voice-first product experiences:

[**Gemini 3.8 Live**](https://aistudio.google.com/live?model=gemini-3.8-live) and [**3.8 Live Extended Thinking**](https://aistudio.google.com/live?model=gemini-3.8-live-extended-thinking)**:** Gemini 3.8 Live brings a step change to our native speech-to-speech models, capable of performing tasks while maintaining dialogue. For complex requests, 3.8 Live Extended Thinking delivers deeper reasoning, ranking #1 on Artificial Analysis’ Speech-to-Speech leaderboard.

[**Gemini 3.5 Transcribe**](https://aistudio.google.com/live?model=gemini-3.5-transcribe-live): Our dedicated speech-to-text model brings highly precise transcription across 85+ languages. Released last month, it achieved an average Word Error Rate (WER) of 4.0% (streaming) and 2.6% (non-streaming).

## Gemini 3.8 Live & 3.8 Live Extended Thinking: Build more intelligent conversational agents

Our new models, [Gemini 3.8 Live](https://aistudio.google.com/live?model=gemini-3.8-live) and [3.8 Live Extended Thinking](https://aistudio.google.com/live?model=gemini-3.8-live-extended-thinking) enable developers to build voice agents that can reason and execute tasks while maintaining the flow of conversations. Key capabilities include:

- **Asynchronous function calling:** Execute API and tool calls in the background while continuing to stream audio responses to the user
- **Visual context:** Ground dialogue in live visual inputs to help enable agents that can understand what users say *and* see
- **Alphanumeric precision:** Accurately parse confirmation codes, claim numbers, and technical data
- **Multilingual support:** Reach global audiences with coverage for 97+ languages and accent consistency
- **Incremental content updates:** Seamlessly merge real-time audio with structured data to return context-aware responses

3.8 Live Extended Thinking also supports [configurable thinking](https://ai.google.dev/gemini-api/docs/live-api/thinking) to help handle complex, multi-step reasoning in the background, while responding or narrating its progress in the main conversation. These models represent a step-change from our previous live models and provide a more streamlined alternative to cascaded architectures.

![Jamie Wood, cofounder and Chief of Technology & Products, says," Ambr AI trains enterprise teams to negotiate, lead, and resolve difficult customer conversations through realistic AI simulations. Switching to the Gemini 3.8 Live Extended Thinking made our simulations faster, more expressive, and better at handling complex conversations. It’s also enabled us to deliver training in over 70 languages through a single integration, helping our customers develop these skills across their global workforce."](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-liveapi-ambrai_1.width-1200.format-webp.webp)

Gemini 3.8 Live and Gemini 3.8 Live Extended Thinking are available via the [Live API](https://ai.google.dev/gemini-api/docs/live). Competitively [priced](http://ai.google.dev/gemini-api/docs/pricing#gemini-3.8-live) at $0.005/min for audio input and $0.018/min
[1](#footnote-1)
for audio output, they allow developers to scale voice applications with industry-leading performance.

![Benchmarks on Artificial Analysis Speech-to-Speech Index](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-8-audio__evals__S2S-inde.width-100.format-webp_VVJ0h6W.webp)

![Benchmark on Agentic Performance](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-8-audio__evals__agentic-.width-100.format-webp_y7iUxFh.webp)

![Benchmark of Tau-bench leaderboard](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-8-audio__evals__t3-banki.width-100.format-webp_PNTg1az.webp)

![Artificial Analysis Overall Cost of Audio](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-8-audio__evals__big-benc.width-100.format-webp_3GHiXLF.webp)

Developers can also access the models through [Agora](https://docs.agora.io/en/ai/models/mllm/gemini), [Fishjam](https://docs.fishjam.io/tutorials/gemini-live-integration), [LiveKit](https://docs.livekit.io/agents/models/realtime/plugins/gemini/), [LangChain](https://docs.langchain.com/langsmith/trace-gemini-live), [Pipecat](https://docs.pipecat.ai/pipecat/features/gemini-live), [Vercel](https://vercel.com/docs/ai-gateway/modalities/realtime), and [Vision Agents](https://visionagents.ai/integrations/realtime/gemini), our Live API integration partners that handle media streaming infrastructure for real-world deployment:

![Live API partners include Pipecat, LiveKit, LangChain, Agora, Fishjam, Voximplant, Vercel, and VisionAgents.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-live-api-partners-launch-.width-1200.format-webp.webp)

## Gemini 3.5 Transcribe: Convert streamed speech to text

Real-time speech understanding is critical for voice-first interfaces. Last month, we released Gemini 3.5 Transcribe for low-latency transcription with high precision, achieving a 4.0% WER, and useful features:

- **Automatic code-switching:** Handle intra-sentence and inter-sentential code- and language-switching without manual configuration
- **Custom vocabulary biasing:** Steer speech recognition toward domain-specific terms, uncommon jargon, company names, and proper nouns by passing a custom\_vocabulary list of up to 1,000 terms
- **Smart transcription mode**: Deliver polished, reader-ready transcripts with structured formatting, self-corrections, and disfluency removal that eliminates filler words

3.5 Transcribe supports 85+ languages and provides a strong listening engine for voice experiences and stateless tasks like sub-second captioning, call center agents, and real-time audio analytics. You can also access the model via the Interactions API to transcribe audio files up to 1 hour long with structured timestamps and speaker labeling. Read our [developer guide](https://aistudio.google.com/learn/gemini-3-5-transcribe-developer-guide) to learn more.

## Our complete audio suite for developers

To get started, try out the models in [ai.studio/live](https://ai.studio/live), clone example apps from [GitHub](https://github.com/google-gemini/gemini-live-api-examples), or equip your agent with our [live api skill](https://ai.google.dev/gemini-api/docs/coding-agents#gemini-live-api-dev).

You can also create audio experiences with our speech and music generation models, all available in the Gemini API:

- [**Gemini 3.5 Live Translate**](https://ai.google.dev/gemini-api/docs/live-api/live-translate): Speech-to-speech translation across more than 70 languages
- [**Gemini 3.1 Flash TTS**](https://ai.google.dev/gemini-api/docs/speech-generation): Highly configurable speech generation (with more updates coming soon)
- [**Lyria 3.5**](https://ai.google.dev/gemini-api/docs/music-generation): Production-grade music generation

The mic is yours, and we can’t wait to hear what you build!
