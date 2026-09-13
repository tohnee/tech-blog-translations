---
title: "Introducing Gemini 3.7 Flash"
source: https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-3-7-flash/
site: gemini
date: 2026-08-13
authors: Tulsee Doshi
crawled: 2026-09-13
---

Today, we’re building on the progress of our widely used Flash series by introducing Gemini 3.7 Flash, our most intelligent workhorse model yet for coding and agents.

This release comes just three weeks after [Gemini 3.6 Flash](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber/), and is a direct result of developer feedback and algorithmic innovations that we look forward to bringing to future models. 3.7 Flash delivers substantial improvements across software engineering, knowledge work, and web development workflows — with an introductory price of half the original 3.6 Flash cost per million tokens.

## Better intelligence for complex workflows

![a chart showing production code quality](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-7-flash__evals__frontier.width-100.format-webp.webp)

![a chart showing long-horizon software engineering](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-7-flash__evals__deepswe-.width-100.format-webp.webp)

![a chart showing web development](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-7-flash__evals__codearen.width-100.format-webp.webp)

![a chart showing Expert PDF document comprehension](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-7-flash__evals__gdp-pdf_.width-100.format-webp.webp)

![a chart showing enterprise workflow automation](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-7-flash__evals__automati.width-100.format-webp.webp)

3.7 Flash shows strong gains over 3.6 Flash in coding tasks like debugging and issue resolution. It also achieves higher first-pass code accuracy and has improved performance in generating production-ready code as seen in [FrontierCode 1.1 Main](https://cognition.com/frontiercode) (43.6% vs 34.4%) and [DeepSWE v1.1](https://deepswe.datacurve.ai/) (65.3% vs 49.0%).

In web development, 3.7 Flash generates more functional layouts and feature-complete apps in fewer prompts. For UI generation, the model shows high design adherence and parity based on a reference input, whether it’s a screenshot, an image, or a full design system. It outperforms 3.6 Flash on Arena.ai’s [WebDev Arena](https://arena.ai/leaderboard/code/webdev) with an Elo score of 1588 vs 1538.

For knowledge-dense fields like finance, law, and biosciences, 3.7 Flash delivers improved reasoning and accuracy. It significantly outperforms 3.6 Flash on the GDP.pdf benchmark (34.0% vs 22.0%), an eval for testing a model’s ability to process complex documents. It also surpasses 3.6 Flash in [AutomationBench](https://zapier.com/blog/introducing-automationbench/), demonstrating it can more effectively complete real-world business workflows (30.4% vs 17.0%).

From a simple text prompt to a fully playable 3D game. We used Gemini 3.7 Flash combined with Nano Banana to dynamically generate characters, items, and textures in real-time.

Stunning, interactive landing pages generated in a single shot. We used Gemini 3.7 Flash to orchestrate sub-agents, using Gemini Omni to create smooth, interactive parallax components.

A robotics model getting trained with Gemini 3.7 Flash using multimodal understanding in a 3 agent graph loop that helps the robot learn faster.

From a static PDF to an interactive data story. Watch how complex annual reports are transformed into engaging web experiences complete with live charts and aggregated insights.

## Better developer experience and price

Gemini 3.7 Flash delivers a noticeably improved developer experience over 3.6 Flash. It better adapts to roadblocks, clarifies intent when needed, and follows instructions with greater fidelity. It thinks more diligently, putting in more effort into multi-step planning and tool calls. A more disciplined execution means less manual oversight and fewer retries across engineering workflows.

3.7 Flash is available through the end of the year at an introductory price
[1](#footnote-1)
of $0.75/1M input tokens and $3.75/1M output tokens. This price combined with the enhanced model performance enables developers and customers to scale production-ready agents cost effectively.

![an image of a performance to cost comparison chart](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-7-flash__evals__perform.width-1200.format-webp.webp)

Early customer feedback is highlighting 3.7 Flash’s performance and precision, achieving results that are significantly better than 3.6 Flash at a low cost.

![Quote from Box](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-7-flash__testimonial__bo.width-100.format-webp.webp)

![Quote from Browser Use](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-7-flash__testimonial__br.width-100.format-webp.webp)

![Quote from Cartwheel](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-7-flash__testimonial__ca.width-100.format-webp_dYz0MOf.webp)

![quote from databricks](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-7-flash__testimonial__da.width-100.format-webp.webp)

![Quote from emergent](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-7-flash__testimonial__em.width-100.format-webp.webp)

![Quote from Harvey](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-7-flash__testimonial__ha.width-100.format-webp_NtGWF6a.webp)

![Quote from Hebbia](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-7-flash__testimonial__he.width-100.format-webp_H9baWpR.webp)

![Quote from LangChain](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-7-flash__testimonial__la.width-100.format-webp_7qAt1Kr.webp)

![Quote from Nunu.ai](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-7-flash__testimonial__nu.width-100.format-webp_DyOGCzR.webp)

![Quote from Open Code](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-7-flash__testimonial__op.width-100.format-webp_wy8PPtG.webp)

![Quote from Pydantic](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-7-flash__testimonial__py.width-100.format-webp.webp)

![Quote from Stanford Department of Biology](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-7-flash__testimonial__st.width-100.format-webp_AzDrTOJ.webp)

## Improving Gemini Spark with 3.7 Flash

Gemini Spark, available to Google AI Pro and Ultra subscribers in over [160 countries](https://support.google.com/gemini/answer/17094507?hl=en&co=GENIE.Platform%3DAndroid&sjid=2353166824601345951-NA#:~:text=Available%20wherever%20Gemini%20Apps%20are%20supported%2C%20except%20in%20the%20European%20Economic%20Area%2C%20Nigeria%2C%20Switzerland%2C%20and%20the%20United%20Kingdom), will be using Gemini 3.7 Flash starting today. We launched Spark at I/O as your personal AI agent that runs 24/7, taking action on your behalf while under your direction. This model update makes Spark more efficient for knowledge work with improved tool use for Google Workspace apps, delivering improved accuracy and output quality for complex, multi-skill workflows.

With 3.7 Flash, Gemini Spark can turn ideas into action more efficiently by consolidating files, drafting emails, and updating status documents.

## Built with safety in mind

We continually work to improve the coverage and robustness of [Frontier Safety safeguards](https://deepmind.google/frontier-safety/). Gemini 3.7 Flash is shipping with updated safeguards against misuse in the domains of Chemical, Biological, Radiological, and Nuclear (CBRN) and cyber offense, while enabling beneficial use cases, in accordance with [our approach to bioresilience](https://deepmind.google/blog/our-approach-to-bioresilience/) and our [cyber program](https://deepmind.google/blog/introducing-gemini-3-5-flash-cyber/).

For more information, see the 3.7 Flash [model card](https://deepmind.google/models/model-cards/gemini-3-7-flash).

## Try it today

- **Developers**: Explore agent-first workflows in [Google Antigravity](https://antigravity.google/) or start building today in the Gemini API via [Google AI Studio](https://ai.dev/prompts/new_chat?model=gemini-3.7-flash) and [Android Studio](https://developer.android.com/studio). Get started with our [developer guide](https://ai.google.dev/gemini-api/docs/latest-model).
- **Enterprises**: Access 3.7 Flash in [Gemini Enterprise Agent Platform](https://console.cloud.google.com/agent-platform/publishers/google/model-garden/gemini-3.7-flash) and the [Gemini Enterprise](https://cloud.google.com/gemini-enterprise?e=48754805) app.
- **Individuals**: Available via Spark, your 24/7 personal agent in the Gemini app for Google AI Pro and Ultra subscribers in [supported countries](https://support.google.com/gemini/answer/17094507?hl=en&co=GENIE.Platform%3DAndroid&sjid=2353166824601345951-NA#:~:text=Available%20wherever%20Gemini%20Apps%20are%20supported%2C%20except%20in%20the%20European%20Economic%20Area%2C%20Nigeria%2C%20Switzerland%2C%20and%20the%20United%20Kingdom).

## Detailed benchmarks

![a chart displaying AI model benchmarks](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-7-flash__evals__benchma.width-1200.format-webp.webp)
