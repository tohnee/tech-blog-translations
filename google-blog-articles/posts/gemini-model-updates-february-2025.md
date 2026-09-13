---
title: "Gemini 2.0 is now available to everyone"
source: https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-model-updates-february-2025/
site: google-blog
date: 2025-02-05
authors: Koray Kavukcuoglu
crawled: 2026-09-13
---

In December, we [kicked off](https://blog.google/technology/google-deepmind/google-gemini-ai-update-december-2024/) the agentic era by releasing an experimental version of Gemini 2.0 Flash — our highly efficient workhorse model for developers with low latency and enhanced performance. Earlier this year, we updated [2.0 Flash Thinking Experimental](https://deepmind.google/technologies/gemini/flash-thinking/) in Google AI Studio, which improved its performance by combining Flash’s speed with the ability to reason through more complex problems.

And last week, we [made an updated 2.0 Flash available to all users of the Gemini app](https://blog.google/feed/gemini-app-model-update-january-2025) on desktop and mobile, helping everyone discover new ways to create, interact and collaborate with Gemini.

Today, we’re making the updated Gemini 2.0 Flash generally available via the Gemini API in [Google AI Studio](https://aistudio.google.com/prompts/new_chat?model=gemini-2.0-flash) and [Vertex AI](https://console.cloud.google.com/freetrial?redirectPath=/vertex-ai/studio). Developers can now build production applications with 2.0 Flash.

We’re also releasing an experimental version of Gemini 2.0 Pro, our best model yet for coding performance and complex prompts. It is available in [Google AI Studio](https://aistudio.google.com/prompts/new_chat?model=gemini-2.0-pro-exp-02-05) and [Vertex AI](https://console.cloud.google.com/freetrial?redirectPath=/vertex-ai/studio), and in the [Gemini app](https://gemini.google.com/) for Gemini Advanced users.

We’re releasing a new model, Gemini 2.0 Flash-Lite, our most cost-efficient model yet, in public preview in [Google AI Studio](https://aistudio.google.com/prompts/new_chat?model=gemini-2.0-flash-lite-preview-02-05) and [Vertex AI](https://console.cloud.google.com/freetrial?redirectPath=/vertex-ai/studio).

Finally, [2.0 Flash Thinking Experimental will be available to Gemini app](http://blog.google/feed/gemini-app-experimental-models) users in the model dropdown on desktop and mobile.

All of these models will feature multimodal input with text output on release, with more modalities ready for general availability in the coming months. More information, including specifics about pricing, can be found in the [Google for Developers blog](https://developers.googleblog.com/en/gemini-2-family-expands). Looking ahead, we’re working on more updates and improved capabilities for the Gemini 2.0 family of models.

## 2.0 Flash: a new update for general availability

[First introduced](https://blog.google/technology/ai/google-gemini-update-flash-ai-assistant-io-2024/) at I/O 2024, the Flash series of models is popular with developers as a powerful workhorse model, optimal for high-volume, high-frequency tasks at scale and highly capable of multimodal reasoning across vast amounts of information with a context window of 1 million tokens. We’ve been thrilled to see its [reception](https://developers.googleblog.com/en/gemini-20-family-expands/) by the developer community.

2.0 Flash is now generally available to more people across our AI products, alongside improved performance in key benchmarks, with image generation and text-to-speech coming soon.

Try Gemini 2.0 Flash in the [Gemini app](https://gemini.google.com/) or the Gemini API in [Google AI Studio](https://aistudio.google.com/prompts/new_chat?model=gemini-2.0-flash) and [Vertex AI](https://console.cloud.google.com/freetrial?redirectPath=/vertex-ai/studio). Pricing details can be found in the [Google for Developers blog](https://developers.googleblog.com/en/gemini-2-family-expands).

## 2.0 Pro Experimental: our best model yet for coding performance and complex prompts

As we’ve continued to share early, experimental versions of Gemini 2.0 like [Gemini-Exp-1206](https://blog.google/feed/gemini-exp-1206/), we’ve gotten excellent feedback from developers about its strengths and best use cases, like coding.

Today, we’re releasing an experimental version of Gemini 2.0 Pro that responds to that feedback. It has the strongest coding performance and ability to handle complex prompts, with better understanding and reasoning of world knowledge, than any model we’ve released so far. It comes with our largest context window at 2 million tokens, which enables it to comprehensively analyze and understand vast amounts of information, as well as the ability to call tools like Google Search and code execution.

![This table compares the capabilities of different versions of Gemini, including 1.5 Flash, 1.5 Pro, 2.0 Flash-Lite, 2.0 Flash, and 2.0 Pro, across various benchmarks. It shows the performance of each version on tasks like general knowledge, code generation, reasoning, factuality, multilingual understanding, math, long-context understanding, image understanding, audio translation, and video analysis.](https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/gemini_benchmarks_cropped_light1x.gif)

Gemini 2.0 Pro is available now as an experimental model to developers in [Google AI Studio](https://aistudio.google.com/prompts/new_chat?model=gemini-2.0-pro-exp-02-05) and [Vertex AI](https://console.cloud.google.com/freetrial?redirectPath=/vertex-ai/studio) and to Gemini Advanced users in the model drop-down on desktop and mobile.

## 2.0 Flash-Lite: our most cost-efficient model yet

We’ve gotten a lot of positive feedback on the price and speed of 1.5 Flash. We wanted to keep improving quality, while still maintaining cost and speed. So today, we’re introducing 2.0 Flash-Lite, a new model that has better quality than 1.5 Flash, at the same speed and cost. It outperforms 1.5 Flash on the majority of benchmarks.

Like 2.0 Flash, it has a 1 million token context window and multimodal input. For example, it can generate a relevant one-line caption for around 40,000 unique photos, costing less than a dollar in Google AI Studio’s paid tier.

Gemini 2.0 Flash-Lite is available in [Google AI Studio](https://aistudio.google.com/prompts/new_chat?model=gemini-2.0-flash-lite-preview-02-05) and [Vertex AI](https://console.cloud.google.com/freetrial?redirectPath=/vertex-ai/studio) in public preview.

## Our responsibility and safety work

As the Gemini model family becomes more capable, we’ll continue to invest in robust measures that enable safe and secure use. For example, our Gemini 2.0 lineup was built with new reinforcement learning techniques that use Gemini itself to critique its responses. This resulted in more accurate and targeted feedback and improved the model's ability to handle sensitive prompts, in turn.

We’re also leveraging automated red teaming to assess safety and security risks, including those posed by risks from indirect prompt injection, a type of cybersecurity attack which involves attackers hiding malicious instructions in data that is likely to be retrieved by an AI system.
