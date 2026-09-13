---
title: "Gemini image generation got it wrong. We'll do better."
source: https://blog.google/products-and-platforms/products/gemini/gemini-image-generation-issue/
site: gemini
date: 2024-02-23
authors: Prabhakar Raghavan
crawled: 2026-09-13
---

Three weeks ago, we launched a new [image generation](https://blog.google/technology/ai/google-imagen-2/) feature for the [Gemini conversational app](https://gemini.google.com/) (formerly known as Bard), which included the ability to create images of people.

It’s clear that this feature missed the mark. Some of the images generated are inaccurate or even offensive. We’re grateful for users’ feedback and are sorry the feature didn't work well.

We’ve [acknowledged the mistake](https://twitter.com/Google_Comms/status/1760603321944121506) and temporarily paused image generation of people in Gemini while we work on an improved version.

## What happened

The Gemini conversational app is a specific product that is separate from Search, our underlying AI models, and our other products. Its image generation feature was built on top of an AI model called [Imagen 2](https://blog.google/technology/ai/google-imagen-2/).

When we built this feature in Gemini, we tuned it to ensure it doesn’t fall into some of the traps we’ve seen in the past with image generation technology — such as creating violent or sexually explicit images, or depictions of real people. And because our users come from all over the world, we want it to work well for everyone. If you ask for a picture of football players, or someone walking a dog, you may want to receive a range of people. You probably don’t just want to only receive images of people of just one type of ethnicity (or any other characteristic).

However, if you prompt Gemini for images of a specific type of person — such as “a Black teacher in a classroom,” or “a white veterinarian with a dog” — or people in particular cultural or historical contexts, you should absolutely get a response that accurately reflects what you ask for.

So what went wrong? In short, two things. First, our tuning to ensure that Gemini showed a range of people failed to account for cases that should clearly *not* show a range. And second, over time, the model became way more cautious than we intended and refused to answer certain prompts entirely — wrongly interpreting some very anodyne prompts as sensitive.

These two things led the model to overcompensate in some cases, and be over-conservative in others, leading to images that were embarrassing and wrong.

## Next steps and lessons learned

This wasn’t what we intended. We did not want Gemini to refuse to create images of any particular group. And we did not want it to create inaccurate historical — or any other — images. So we turned the image generation of people off and will work to improve it significantly before turning it back on. This process will include extensive testing.

One thing to bear in mind: Gemini is built as a creativity and productivity tool, and it may not always be reliable, especially when it comes to generating images or text about current events, evolving news or hot-button topics. It will make mistakes. As we’ve said from the beginning, hallucinations are a known challenge with all LLMs — there are instances where the AI just gets things wrong. This is something that we’re constantly working on improving.

Gemini tries to give factual responses to prompts — and our double-check feature helps evaluate whether there’s content across the web to substantiate Gemini’s responses — but we recommend relying on Google Search, where separate systems surface fresh, high-quality information on these kinds of topics from sources across the web.

I can’t promise that Gemini won’t occasionally generate embarrassing, inaccurate or offensive results — but I can promise that we will continue to take action whenever we identify an issue. AI is an emerging technology which is helpful in so many ways, with huge potential, and we’re doing our best to roll it out safely and responsibly.
