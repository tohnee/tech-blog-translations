---
title: "Try Deep Think in the Gemini app"
source: https://blog.google/products-and-platforms/products/gemini/gemini-2-5-deep-think/
site: gemini
date: 2025-08-01
authors: The Deep Think team
crawled: 2026-09-13
---

Today, we’re making Deep Think available in the [Gemini app](https://gemini.google/) to [Google AI Ultra subscribers](https://one.google.com/about/google-ai-plans/) — the latest in a lineup of extremely capable AI tools and features made exclusively available to them.

This new release incorporates feedback from early trusted testers and research breakthroughs. It’s a significant improvement over what was first [announced at I/O](https://blog.google/technology/google-deepmind/google-gemini-updates-io-2025/#deep-think), as measured in terms of key benchmark improvements and trusted tester feedback. It is a variation of the model that [recently achieved](https://deepmind.google/discover/blog/advanced-version-of-gemini-with-deep-think-officially-achieves-gold-medal-standard-at-the-international-mathematical-olympiad/) the gold-medal standard at this year’s International Mathematical Olympiad (IMO). While that model takes hours to reason about complex math problems, today’s release is faster and more usable day-to-day, while still reaching Bronze-level performance on the 2025 IMO benchmark, based on internal evaluations.

Deep Think could be a powerful tool in creative problem solving:

As we put Deep Think in the hands of Google AI Ultra subscribers, we’re also sharing the official version of the Gemini 2.5 Deep Think model that [achieved](https://deepmind.google/discover/blog/advanced-version-of-gemini-with-deep-think-officially-achieves-gold-medal-standard-at-the-international-mathematical-olympiad/) the gold-medal standard with a small group of mathematicians and academics. We look forward to hearing how it could enhance their research and inquiry, and we’ll use their feedback as we continue to improve this offering.

This release represents a significant step forward in our mission to build more helpful and capable AI, and furthers our commitment to using Gemini to push the frontier of human knowledge.

## How Deep Think works: extending Gemini’s parallel “thinking time”

Just as people tackle complex problems by taking the time to explore different angles, weigh potential solutions, and refine a final answer, Deep Think pushes the frontier of thinking capabilities by using parallel thinking techniques. This approach lets Gemini generate many ideas at once and consider them simultaneously, even revising or combining different ideas over time, before arriving at the best answer.

Moreover, by extending the inference time or "thinking time," we give Gemini more time to explore different hypotheses, and arrive at creative solutions to complex problems.

We’ve also developed novel reinforcement learning techniques that encourage the model to make use of these extended reasoning paths, thus enabling Deep Think to become a better, more intuitive problem-solver over time.

## How Deep Think stacks up: state-of-the-art performance

Deep Think can help people tackle problems that require creativity, strategic planning and making improvements step-by-step, such as:

- **Iterative development and design:** We’ve been impressed by Deep Think’s performance on tasks that require building something complex, piece by piece. For example, we’ve observed Deep Think can improve both the aesthetics and functionality of web development tasks.

Deep Think in the Gemini app uses parallel thinking techniques to deliver more detailed, creative and thoughtful responses.

![A comparison of three AI-generated voxel art scenes. Each image shows a pagoda in a garden with trees and cherry blossoms, demonstrating increasing detail and complexity from left to right. The images are labeled "Gemini 2.5 Flash," "Gemini 2.5 Pro," and "Gemini 2.5 Deep Think."](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/2-5-deep-think_blog-image_pagoda.width-1200.format-webp.webp)

- **Scientific and mathematical discovery:** Because it can reason through highly complex problems, Deep Think can be a powerful tool for researchers. It can help formulate and explore mathematical conjectures or reason through complex scientific literature, potentially accelerating the path to discovery.
- **Algorithmic development and code:** Deep Think particularly excels at [tough coding problems](https://x.com/GoogleDeepMind/status/1925676461651791992) in which problem formulation and careful consideration of tradeoffs and time complexity is paramount.

Deep Think’s performance is also reflected in challenging benchmarks that measure coding, science, knowledge and reasoning capabilities. For example, compared to other models without tool use, Gemini 2.5 Deep Think achieves state-of-the-art performance across LiveCodeBench V6, which measures competitive code performance, and Humanity’s Last Exam, a challenging benchmark that measures expertise in different domains, including science and math.

![A set of four bar charts comparing AI model performance. Gemini 2.5 is the top performer in reasoning, code, and math benchmarks against Gemini 2.5 Pro, OpenAI 03, and Grok 4.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/all_benchmarks_blog.width-1200.format-webp.webp)

## How we’re advancing Gemini responsibly

We continue to build safety and responsibility into Gemini throughout the training and deployment lifecycle. In testing, Gemini 2.5 Deep Think demonstrated improved content safety and tone-objectivity compared to Gemini 2.5 Pro, but did have a higher tendency to refuse benign requests.

As Gemini's problem-solving abilities advance, we are taking a deeper look at risks that come with increased complexity, including our frontier safety evaluations and the implementation of planned mitigations for critical capability levels.

Further details on the safety outcomes of Gemini 2.5 Deep Think are available in the [model card](https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-2-5-Deep-Think-Model-Card.pdf).

## How to use Deep Think in the Gemini app today

If you’re a Google AI Ultra subscriber, you can use Deep Think in the Gemini app today with a fixed set of prompts a day by toggling “Deep Think” in the prompt bar when selecting 2.5 Pro in the model drop down. Deep Think automatically works with tools such as code execution and Google Search, and can produce much longer responses.

We are also working to release Deep Think with and without tools to a set of trusted testers via the Gemini API in the coming weeks, to better understand its usability for developer and enterprise use cases.

Teams at nearly every layer of the stack, from research to deployment, have worked to make Deep Think faster, more reliable, and user friendly for Gemini app users. We can’t wait to see what you build with it.
