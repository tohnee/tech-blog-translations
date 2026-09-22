---
title: "grok-voice-agent-api"
date: 2025-12-17
source: https://x.ai/news/grok-voice-agent-api
crawled: 2026-09-22
---

December 17, 2025

## Grok Voice Agent API

Bringing the power of Grok Voice to all developers.

Listen to this blog post

Listen to this blog post

Today, we're excited to launch the Grok Voice Agent API, empowering developers to build voice agents that speak dozens of languages, call tools, and search realtime data.

The Grok Voice Agent API is built on the same stack that powers Grok Voice for millions in our mobile apps and Tesla vehicles, and we’re thrilled to open up this proven technology to all via the xAI API.

Eve.Leo.Rex.Ara.Sal.

Rex

## [Smart and fast](#smart-and-fast)

Grok Voice Agents are the fastest, most intelligent voice agents available on the market.

We built the entire voice stack in-house, training our own voice activity detection (VAD), tokenizer, and audio models from scratch. This fine-grained control over every component of the stack allows us to rapidly iterate and improve Grok’s intelligence and speed.

The Grok Voice Agent API ranks #1 on [Big Bench Audio](https://artificialanalysis.ai/models/speech-to-speech), the leading audio reasoning benchmark that measures voice agents’ capabilities to solve complex problems. With an average time-to-first-audio of less than 1 second, Grok is nearly 5 times faster than the closest competitor.

### Big Bench Audio: Intelligence vs Latency

Audio reasoning benchmark (independently verified by Artificial Analysis)

Score(%)

95%

Time to First Audio(s)

5 s

## [Pricing](#pricing)

The Grok Voice Agent API leads the industry in cost-efficiency. Developers are billed at a simple flat rate of $0.05 per minute of connection time.

### Cost per minute

* OpenAI charges by input and output tokens. $0.10 / min is a highly conservative blended estimate. In production, pricing typically exceeds $0.10 / min.

## [Multilingual fluency](#multilingual-fluency)

Grok Voice Agents can speak dozens of languages with native-level proficiency, accurately capturing nuances in dialects and pronunciations. Grok Voice Agents were trained to automatically respond in the language spoken by the user and can seamlessly switch languages mid-conversation. Developers can also instruct Grok to always respond in a specific language via system prompt.

In blind head-to-head human evaluations against the OpenAI Realtime API, Grok is consistently rated as the preferred model across axes such as pronunciation, accent, and prosody.

### Multilingual performance

Win rate compared to OpenAI Realtime API (blind human evals)

Grok

OpenAI Realtime API

## [Grok Voice in Tesla](#grok-voice-in-tesla)

Tesla was a critical design partner for the Grok Voice Agent API, which now powers Grok in millions of vehicles.

Grok feels like a natural extension of your Tesla, thanks to specialized tools that let it access vehicle status, look up directions, and control navigation. Grok uses these tools in tandem to provide a seamless route planning experience. For instance, ask Grok to plan a road trip, and it will search X for recommendations, calculate optimal routes, and add stops, generating a full itinerary in seconds.

[](https://data.x.ai/grok-in-tesla.mp4)

Grok Voice Agents can perform tasks and look up information in real time. With our API, developers can effortlessly integrate their own custom tools or tap into xAI's powerful real-time search capabilities across X and the web.

json

```
{
    "type": "session.update",
    "session": {
        "instructions": "You're an in-car assistant for Tesla.",
        "voice": "Ara",
        "tools": [
            { "type": "web_search" },
            { "type": "x_search" },
            {
                "type": "function",
                "name": "nav_search",
            }
        ]
    }
}
```

## [Natural, expressive voices](#natural-expressive-voices)

We're excited to offer multiple expressive voices to the Grok Voice Agent API, including Ara, Eve, and Leo. Our voices sound natural in everyday conversations and also excel at pronouncing domain-specific terminology in fields like healthcare, finance, and legal.

Customer Support

Finance

Healthcare

Legal

Customer Support

To enhance realism, developers can even prompt the model to use auditory cues such as `[whisper]`, `[sigh]`, and `[laugh]`.

Have you heard the new Grok Voice?

whispers Let me tell you a secret... I am the smartest and best AI.

laugh Give it a go! Ask me anything.

I'll be your trusted personal assistant and closest companion.

ARA

## [Start building](#start-building)

The Grok Voice Agent API is compatible with the OpenAI Realtime API specification and also available via the official [xAI LiveKit Plugin](https://docs.livekit.io/agents/integrations/xai/).

We’ve also built a [voice playground](https://console.x.ai/team/default/voice) that you can use to test various voices directly from your browser.

We're excited to continue iterating quickly. In the next few weeks, we'll also be releasing:

- Standalone text-to-speech and speech-to-text endpoints
- Audio models with even stronger performance in pronunciation and latency

We can’t wait to hear what you build!

### Try our voice playground

Speak to a Grok Voice Agent via the xAI Cloud Console

[Open playground](https://console.x.ai/team/default/voice)

[![xAI Logo](/_next/static/media/xai.985f0fcf.svg)

xAI Cloud Console

Generate API key](https://console.x.ai)[![Book icon](/_next/static/media/docs.a3d5de8a.svg)

Read

Voice Agent API Docs](https://docs.x.ai/docs/guides/voice)[![Livekit Logo](/_next/static/media/livekit.0f6cec71.svg)

View

LiveKit Plugin](https://docs.livekit.io/agents/integrations/xai/)

Try Grok On

[Web](https://grok.com)

[iOS](https://apps.apple.com/app/apple-store/id6670324846?pt=126952307&ct=x.ai%20Direct%20Link&mt=8)

[Android](https://play.google.com/store/apps/details?id=ai.x.grok&hl=en)

[Grok on X](https://x.com/i/grok)

Products

[Grok](/grok)

[𝕏](https://x.com)

[API](/api)

[Grok Enterprise](/grok/business)

[Grokipedia](https://grokipedia.com)

Company

[Company](/company)

[Careers](/careers)

[Contact](/contact)

[News](/news)

Resources

[Documentation](https://docs.x.ai)

[Privacy policy](/privacy-policy)

[Security](/security)

[Safety](/safety)

[Legal](/legal)

[Status](https://status.x.ai)
