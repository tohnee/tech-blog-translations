---
title: "grok-code-fast-1"
date: 2025-08-28
source: https://x.ai/news/grok-code-fast-1
crawled: 2026-09-22
---

August 28, 2025

## Grok Code Fast 1

We're thrilled to introduce grok-code-fast-1, a speedy and economical reasoning model that excels at agentic coding.

![Abstract digital cheetah](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fgrok-code-fast.18c66acf.webp&w=1200&q=75)

## [A speedy daily driver](#a-speedy-daily-driver)

While today's models are undeniably powerful, they often don't feel purpose-built for agentic coding workflows, where loops of reasoning and tool calls can feel frustratingly slow. As heavy users of agentic coding tools, our engineers saw room for a more nimble, responsive solution optimized for our day-to-day tasks.

We built `grok-code-fast-1` from scratch, starting with a brand-new model architecture. To lay a robust foundation, we carefully assembled a pre-training corpus rich with programming-related content. For post-training, we curated high-quality datasets that reflect real-world pull requests and coding tasks.

Throughout the training process, we collaborated closely with our launch partners to refine and sharpen the model’s behavior inside their agentic platforms. `grok-code-fast-1` has mastered the use of common tools like grep, terminal, and file editing, and thus should feel right at home in your favorite IDE.

We've teamed up with select launch partners to offer `grok-code-fast-1` for free for a limited time, including GitHub Copilot, Cursor, Cline, Roo Code, Kilo Code, opencode, and Windsurf.

[![Cursor Logo](/_next/static/media/cursor.c6f1f8ea.svg)

Try free on

Cursor](https://cursor.com)[![GitHub Copilot Logo](/_next/static/media/copilot.a16b7bcb.svg)

Try free on

GitHub Copilot](https://github.com/features/copilot)[![Cline Logo](/_next/static/media/cline.9216a6a2.svg)

Try free on

Cline](https://cline.bot/)

## [Blazing fast](#blazing-fast)

Our inference and supercomputing teams developed several innovative techniques to dramatically accelerate our serving speed, creating a uniquely responsive experience where the model will have already called dozens of tools before you even finish reading the first paragraph of the thinking trace. We've also invested in prompt caching optimizations, regularly achieving cache hit rates above 90% when used with our launch partners.

## [A versatile programmer](#a-versatile-programmer)

`grok-code-fast-1` is exceptionally versatile across the full software development stack and is particularly adept at TypeScript, Python, Java, Rust, C++, and Go. It can complete common programming tasks with minimal oversight, ranging from building zero-to-one projects and providing insightful answers to codebase questions to performing surgical bug fixes.

Example 1 of 2Battle Simulator

[](https://data.x.ai/battle-sim.mp4)

![Danny Limanseta](/_next/image?url=https%3A%2F%2Fpbs.twimg.com%2Fprofile_images%2F1653760191542996994%2FgxsaTn-0_400x400.png&w=96&q=75)

[Danny Limanseta

@dannylimanseta](https://x.com/dannylimanseta)

It's so quick that I actually had to change up how I work in Cursor.

Read more

Grok Code Fast is ridiculously fast, it’s probably the fastest model out there right now. It's so quick that I actually had to change up how I work in Cursor.

I threw together this battle simulator prototype in less than a day with Grok Code Fast on Cursor. Because it responds so fast and follows instructions well, I've found I'm better off giving it smaller, focused tasks. That way I can iterate quickly and steer it exactly where I want.

For this battle simulator, my workflow is to have it plan out big features first, then break them down and execute in phases. Works way better than dumping a huge prompt on it all at once. The battle simulator came together so smoothly this way, just rapid iterations in Cursor until I get it to what I want.

## [An economical choice](#an-economical-choice)

We designed `grok-code-fast-1` to be widely accessible, priced at:

- $0.20 per million input tokens
- $1.50 per million output tokens
- $0.02 per million cached input tokens

`grok-code-fast-1` was crafted to shine in the tasks developers face every day, striking a compelling balance between performance and cost. Its strength lies in delivering strong performance in a economical, compact form factor, making it a versatile choice for tackling common coding tasks quickly and cost-effectively.

### Model Performance

Tokens per Second vs Output Price

Tokens per second(TPS)

190

Output price/ per 1M tokens

$18

### Methodology

### TPS metrics were calculated by directly measuring response generation speed via each model provider's API, considering only the final response tokens.

- Gemini 2.5 Pro, GPT-5, and Claude Sonnet 4: Measured using their respective public APIs.

- Grok Code Fast 1 and Grok 4: Measured using the xAI API.

- Qwen3-Coder: Hosted on DeepInfra at low precision (fp4), which reduces response quality.

We took a holistic approach to evaluating model performance, blending public benchmarks with real-world testing. On the full subset of SWE-Bench-Verified, `grok-code-fast-1` scored 70.8% using our own internal harness.

While benchmarks like SWE-Bench provide valuable insights, we've found they don't fully reflect the nuances of real-world software engineering, particularly the end-user experience in agentic coding workflows.

To guide our model training, we pair these benchmarks with routine human assessments, where experienced developers rate the model's end-to-end performance on everyday tasks. We've also built automated evaluations to track key aspects of behavior, helping us balance trade-offs in design.

When developing `grok-code-fast-1`, we focused on usability and user satisfaction, guided by real-world human evaluations. The result is a model rated by programmers as fast and reliable for everyday coding tasks.

## [Grok Code for everyone](#grok-code-for-everyone)

For a limited time, we’re excited to offer `grok-code-fast-1` for free on exclusive launch partners. Here’s what our launch partners had to say about our the model, which was recently released in stealth under the codename `sonic`.

### Free for a limited time

We’re excited to offer Grok Code Fast 1 for free on exclusive launch partners.

"In early testing, Grok Code Fast has shown both its speed and quality in agentic coding tasks. Empowering developers with powerful tools is a core part of our mission at GitHub Copilot, and this is a compelling new option for our developers."

[![Mario Rodriguez](/_next/image?url=https%3A%2F%2Fpbs.twimg.com%2Fprofile_images%2F1783313134117376000%2FhWT1AJWp_400x400.jpg&w=64&q=75)

Mario Rodriguez (@mariorod1)

Chief Product Officer, GitHub](https://x.com/mariorod1)

Instructions

View instructions

[![GitHub Copilot](/_next/static/media/copilot.a16b7bcb.svg)

Try free on

GitHub Copilot](https://github.com/features/copilot)

## [Prompt Engineering Guide](#prompt-engineering-guide)

Our team has crafted a [Prompt Engineering Guide](https://docs.x.ai/docs/guides/grok-code-prompt-engineering) with tips on how to get the best from `grok-code-fast-1`.

The model is generally available via the xAI API, priced at $0.20 / 1M input tokens, $1.50 / 1M output tokens, and $0.02 / 1M cached input tokens.

[![xAI Logo](/_next/static/media/xai.985f0fcf.svg)

Open

xAI Cloud Console](https://console.x.ai)[![Prompt Engineering Guide icon](/_next/static/media/prompt-engineering.fc779cee.svg)

Read

Prompt Engineering Guide](https://docs.x.ai/docs/guides/grok-code-prompt-engineering)

## [What to expect in the next few weeks](#what-to-expect-in-the-next-few-weeks)

Last week, we quietly released `grok-code-fast-1` under the codename `sonic`. During this stealth phase, our team carefully monitored community channels and deployed multiple new model checkpoints to address feedback.

As we advance this new model family, we're excited to iterate rapidly on your input. We highly value the developer community's support and encourage you to freely [share all feedback](https://discord.gg/x-ai), positive and negative.

We'll focus on delivering consistent updates to `grok-code-fast-1`, with improvements arriving in days rather than weeks. A new variant that supports multimodal inputs, parallel tool calling, and extended context length is already in training.

Read the `grok-code-fast-1` [model card here](https://data.x.ai/2025-08-26-grok-code-fast-1-model-card.pdf). We’re excited to see what you build!

Try Grok On

[Web](https://grok.com)

[iOS](https://apps.apple.com/app/apple-store/id6670324846?pt=126952307&ct=x.ai%20Direct%20Link&mt=8)

[Android](https://play.google.com/store/apps/details?id=ai.x.grok&hl=en)

[Grok on X](https://x.com/i/grok)

Products

[Grok](/grok)

[API](/api)

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
