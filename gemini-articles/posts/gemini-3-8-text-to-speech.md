---
title: "Gemini 3.8 text-to-speech says hello"
source: https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-8-text-to-speech/
site: gemini
date: 2026-09-23
authors: Leland Rechis
crawled: 2026-09-24
---

Today, we’re introducing two new text-to-speech models to the Gemini family, transforming voice generation from static presets into a dynamic creative studio. These models enable creators, developers, and enterprises to create richer, more expressive audio experiences, while enabling improved user experiences in products like [Gemini Notebook](https://notebook.google.com/) and [Google Vids](http://vids.new/).

- **Gemini 3.8 Flash TTS:** Built for deep creative direction and character design. Create entirely new voices from scratch using natural language prompts to bring characters to life across gaming, immersive audiobooks, podcasts, and interactive media. Direct every performance line by line with granular control over acting cues, pacing, dialect shifts, and backchanneling.
- **Gemini 3.8 Flash-Lite TTS:** Built for high-volume, cost-efficient scale. Optimized for high-volume dubbing, audio content creation, and expressive voice agents with fine-grained control over tone, pacing, and expressive nuance.

These models complement our fast-growing Gemini Audio family, following [3.5 Live Translate](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-live-3-5-translate/), [3.5 Transcribe](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-5-transcribe/), [3.8 Live, and 3.8 Live Extended Thinking](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-8-live-gemini-3-8-live-extended-thinking/).

## Create and customize your own voices

Scale up from 30 original voices to an infinite library. Whether you need an entirely original character voice or a consistent brand ambassador, our 3.8 Flash TTS model powers a full vocal studio. This enables you to create and use expressive, natural-sounding voices for every moment, while empowering developers and enterprises to easily build custom audio experiences.

- **Generative voice design:** With Gemini 3.8 Flash TTS, create bespoke voices from scratch by customizing role, accent and voice characteristics across more than 100 languages and dialects using natural language prompting — whether you're bringing a dramatic, fire-breathing dragon to life or crafting a charismatic narrator with a distinct regional cadence.

Hear how Gemini 3.8 Flash TTS generates a high-energy DJ voice from Melbourne.

Hear how Gemini 3.8 Flash TTS generates a super-tinny, monotone robot voice.

Hear how Gemini 3.8 Flash TTS brings a Japanese dragon to life.

- **Expansive voice library:** Access 2,000+ production-ready voices with broad language coverage — including regional varieties like Mexican Spanish, Quebec French, and Scots English.
- **Voice replication:** Recreate consistent vocal profiles from just a 30-second audio sample of your voice or a voice you have the rights to use, backed by built-in consent verification, SynthID watermarking, and C2PA credentials to protect both developers and their vocal talent.
- **Save and scale:** Save and manage the custom voices you designed to ensure consistent performance and minimal drift across ongoing projects.
- **Voice remixing:** Coming soon, pick a voice from our voice library and fine-tune timbre, pitch, pace, and accent. Use prompts to dial in characteristics (e.g. “add subtle Southern US accent” or “soften the delivery”).

## Direct the performance, line by line

Once you've selected your voices, both TTS models give you precise control over how each line is delivered.

- **Direct performance line by line:** Write your own stage directions or let Gemini steer delivery with natural script cues — from a calm customer service agent to a whispered suspense scene.

Hear how Gemini 3.8 Flash TTS enables natural, highly expressive conversations for interactive voice agents.

Watch and hear how Gemini 3.8 Flash TTS uses granular script control to build a deeply engaging, immersive audio experience.

- **Long-form generation:** Maintain high voice quality, natural pacing, and character timbre across hours of continuous audio with minimal speaker drift — ideal for podcasts and audiobooks.
- **Native two-speaker scene staging:** Direct multi-turn conversations seamlessly from a single script —whether for a podcast or dramatic storytelling—while keeping both voices distinctly separated with natural conversational turn-taking.
- **Scripted vocal bursts & backchanneling:** Add realistic conversational texture using non verbal cues (like <laughs>, <sigh>, <gasp> and active-listening interjections (like |mhm| or|yeah|) for precise comedic timing and reaction beats.

*See how Gemini 3.8 Flash TTS turns natural language prompts into bespoke vocal personas from scratch.*

*Watch how Gemini 3.8 Flash TTS enables creators to design custom scenes to bring animated dialogue to life.*

*See how Gemini 3.8 Flash TTS turns scripts into fully performed dialogue scenes, letting creators direct vocal delivery, and natural turn-taking.*

## Get expressive high-quality speech generation built for global scale

Gemini 3.8 Flash TTS delivers leading voice customization capabilities, securing the #1 overall spot on [Hume AI’s](https://www.hume.ai/rw-voice-eq) Voice Design Benchmark (71.4) and also leading in accent modeling (60.8).

Gemini 3.8 Flash TTS and Gemini 3.8 Flash-Lite TTS enable truly expressive performances without sacrificing reliability, also securing the #1 and #2 spots respectively on Hume AI’s Overall Quality Index. The model shows major improvements on a wide range of use cases such as long-form content and dual-speaker screenplay control compared to Gemini 3.1 Flash TTS.

In blind human preference evaluations on [Voice Arena](https://voicearena.com/tts-leaderboard/us-english)), Gemini 3.8 Flash and Flash-Lite TTS secure top positions amongst competitors in key global languages, including Japanese, Brazilian Portuguese, Vietnamese, Modern Standard Arabic (MSA), Mexican Spanish and Hindi. With support for over 100 languages, these models empower creators, developers, and enterprises to build high-quality, multilingual voice experiences worldwide.

![An evaluation showing text-to-speech quality benchmark Hume AI](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/blog-gemini-3.8-flash-tts__evals_.width-100.format-webp_21WnKg9.webp)

![an evaluation chart showing text to speech voice design leaderboard Hume AI](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/blog-gemini-3.8-flash-tts__evals_.width-100.format-webp_tbi15co.webp)

![an evaluation chart showing text to speech leaderboard for Voice Arena](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/blog-gemini-3.8-flash-tts__evals_.width-100.format-webp_47W1vK6.webp)

## Build with trust, consent, and transparency

We built our voice creation and replication capabilities with strict safeguards to help protect voice talent, respect identity, and ensure content transparency. For voice replication our system leverages consent verification: users must provide a verbal consent recording from the voice owner that matches the reference speaker before a voice can be created.

More broadly, every audio clip generated by our Gemini Audio models is watermarked with [SynthID](https://deepmind.google/models/synthid/). This imperceptible watermark is woven directly into the audio output, ensuring AI-generated speech remains detectable to help prevent misinformation. For more details on our approach to safety and responsibility, review the [model card](https://deepmind.google/models/model-cards/gemini-3-8-audio/).

## Try our new Google AI Studio audio playground

Starting today, developers can experience these new [speech generation](https://aistudio.google.com/docs/speech-generation) capabilities in [Google AI Studio](https://aistudio.google.com/generate-speech?model=gemini-3.8-flash-tts). Built like a voice design workspace, you can prompt entirely new vocal identities from scratch or replicate your own voice
[1](#footnote-1)
, then bring them directly into a dual-speaker screenplay editor to direct line-by-line delivery.

Try voice replication in Google AI Studio.

## Deploy high-performance voice interfaces with ease

By using the Gemini API, developer platforms such as [Agora](http://docs.agora.io/en/ai/models/tts/gemini), [LiveKit](https://docs.livekit.io/agents/models/tts/gemini/), [Pipecat](https://docs.pipecat.ai/api-reference/server/services/tts/google#geminittsservice), [Vercel](https://vercel.com/docs/ai-gateway/modalities/text-to-speech) enable developers to build and deploy high-performance speech generation experiences with ease.

We’re partnering with companies like Figma, HeyGen, Linguana, Wondercraft, 99.co, and Ollang, who are integrating our latest TTS models to help accelerate global dubbing, localize media with nuanced regional accents, and power conversational voice agents at scale.

![a quote from Darius Cheung, CEO and Co-Founder of 99 Group](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-audio__testimonial-99-grou.width-100.format-webp.webp)

![a quote from Mason Adams, Developer Evangelist, Agora](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-audio__testimonial-agora__.width-100.format-webp.webp)

![a quote from Jonathan Gur-Zeev, Director of Product, Figma Weave](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-audio__testimonial-figma-w.width-100.format-webp.webp)

![a quote from Bin Liu, VP of Engineering for Hygen](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-audio__testimonial-heygen_.width-100.format-webp.webp)

![a quote card from Luke Pane, Developer, katsuyo](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-audio__testimonial-katsuyo.width-100.format-webp.webp)

![quote from Ritwik Baranwal, Associate Director AI/ML of kuku.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-audio__testimonial-kuku-FM.width-100.format-webp.webp)

![a quote from Oded Shafran, Co-Founder & CTO of linguana](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-audio__testimonial-linguan.width-100.format-webp.webp)

![Aziz Ulak, CTO & Co-founder, Ollang](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-audio__testimonial-olang__.width-100.format-webp.webp)

![a quote from Phil Marshall, Founder and CEO of Spoken](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-audio__testimonial-spoken_.width-100.format-webp.webp)

![quote from Zina Rahman, Co-Founder and CEO, Transforms.AI](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-audio__testimonial-transit.width-100.format-webp.webp)

![quote from Mei Ki Yiu, CTO of Wondercraft](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-audio__testimonial-wonderc.width-100.format-webp.webp)

## Start using our latest Gemini Audio models:

Gemini 3.8 Flash TTS is rolling out starting today:

- **For developers**: In the [Gemini API](https://aistudio.google.com/docs/speech-generation) and [Google AI Studio](https://aistudio.google.com/generate-speech?model=gemini-3.8-flash-tts)
- **For enterprises**: Coming soon via API in [Gemini Enterprise](https://docs.cloud.google.com/gemini-enterprise-agent-platform)
- **For everyone**: In [Gemini Notebook](https://notebook.google.com/).

Gemini 3.8 Flash-Lite TTS is rolling out starting today:

- **For developers**: In the [Gemini API](https://aistudio.google.com/docs/speech-generation) and [Google AI Studio](https://aistudio.google.com/generate-speech?model=gemini-3.8-flash-lite-tts)
- **For enterprises**: Coming soon via API in [Gemini Enterprise](https://docs.cloud.google.com/gemini-enterprise-agent-platform)
- **For everyone**: In [Google Vids](http://vids.new/)
