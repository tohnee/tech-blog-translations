---
title: "Gemini 2.5: Our most intelligent AI model"
source: https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-model-thinking-updates-march-2025/
site: google-blog
date: 2025-03-25
authors: Koray Kavukcuoglu
crawled: 2026-09-13
---

*Last updated March 26*

Today we’re introducing Gemini 2.5, our most intelligent AI model. Our first 2.5 release is an experimental version of 2.5 Pro, which is state-of-the-art on a wide range of benchmarks and debuts at #1 on [LMArena](https://lmarena.ai/?leaderboard) by a significant margin.

[Gemini 2.5 models](https://deepmind.google/technologies/gemini) are thinking models, capable of reasoning through their thoughts before responding, resulting in enhanced performance and improved accuracy.

In the field of AI, a system’s capacity for “reasoning” refers to more than just classification and prediction. It refers to its ability to analyze information, draw logical conclusions, incorporate context and nuance, and make informed decisions.

For a long time, we’ve explored ways of making AI smarter and more capable of reasoning through techniques like [reinforcement learning](https://www.nature.com/articles/nature16961) and [chain-of-thought prompting](https://arxiv.org/abs/2201.11903). Building on this, we recently introduced our first thinking model, [Gemini 2.0 Flash Thinking](https://deepmind.google/technologies/gemini/flash-thinking/).

Now, with Gemini 2.5, we've achieved a new level of performance by combining a significantly enhanced base model with improved post-training. Going forward, we’re building these thinking capabilities directly into all of our models, so they can handle more complex problems and support even more capable, context-aware agents.

## Introducing Gemini 2.5 Pro

Gemini 2.5 Pro Experimental is our most advanced model for complex tasks. It tops the [LMArena](https://lmarena.ai/?leaderboard) leaderboard — which measures human preferences — by a significant margin, indicating a highly capable model equipped with high-quality style. 2.5 Pro also shows strong reasoning and code capabilities, leading on common coding, math and science benchmarks.

Gemini 2.5 Pro is available now in [Google AI Studio](http://aistudio.google.com/app/prompts/new_chat?model=gemini-2.5-pro-exp-03-25) and in the [Gemini app](https://gemini.google.com/) for Gemini Advanced users, and will be coming to [Vertex AI](https://console.cloud.google.com/freetrial?redirectPath=/vertex-ai/studio) soon. We’ll also introduce pricing in the coming weeks, enabling people to use 2.5 Pro with higher rate limits for scaled production use.

Updated March 26 with new MRCR (Multi Round Coreference Resolution) evaluations

![Detailed table displays performance of multiple large language models on tests like math, coding, and reasoning. Gemini 2.5 Pro shows top results in several categories, indicated by highlighted cells. Fine print at the bottom provides context for the data.](https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/gemini_benchmarks_cropped_light2x_1PPmDuP.gif)

## Enhanced reasoning

Gemini 2.5 Pro is state-of-the-art across a range of benchmarks requiring advanced reasoning. Without test-time techniques that increase cost, like majority voting, 2.5 Pro leads in math and science benchmarks like GPQA and AIME 2025.

It also scores a state-of-the-art 18.8% across models without tool use on Humanity’s Last Exam, a dataset designed by hundreds of subject matter experts to capture the human frontier of knowledge and reasoning.

![Bar charts comparing the performance of Gemini 2.5 Pro with other AI models like OpenAI GPT-4.5 and Claude 3.7 Sonnet across three categories: Reasoning, Science, and Mathematics. Gemini 2.5 Pro shows strong results in all categories.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/final_2.5_blog_1.width-1200.format-webp.webp)

## Advanced coding

We’ve been focused on coding performance, and with Gemini 2.5 we’ve achieved a big leap over 2.0 — with more improvements to come. 2.5 Pro excels at creating visually compelling web apps and agentic code applications, along with code transformation and editing. On SWE-Bench Verified, the industry standard for agentic code evals, Gemini 2.5 Pro scores 63.8% with a custom agent setup.

Here’s an example of how 2.5 Pro can use its reasoning capabilities to create a video game by producing the executable code from a single line prompt.

## Building on the best of Gemini

Gemini 2.5 builds on what makes Gemini models great — native multimodality and a long context window. 2.5 Pro ships today with a 1 million token context window (2 million coming soon), with strong performance that improves over previous generations. It can comprehend vast datasets and handle complex problems from different information sources, including text, audio, images, video and even entire code repositories.

Developers and enterprises can start experimenting with Gemini 2.5 Pro in [Google AI Studio](http://aistudio.google.com/app/prompts/new_chat?model=gemini-2.5-pro-exp-03-25) now, and [Gemini Advanced](https://gemini.google.com/) users can select it in the model dropdown on desktop and mobile. It will be available on [Vertex AI](https://console.cloud.google.com/freetrial?redirectPath=/vertex-ai/studio) in the coming weeks.

As always, we welcome feedback so we can continue to improve Gemini’s impressive new abilities at a rapid pace, all with the goal of making our AI more helpful.
