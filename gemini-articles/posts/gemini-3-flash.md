---
title: "Gemini 3 Flash: frontier intelligence built for speed"
source: https://blog.google/products-and-platforms/products/gemini/gemini-3-flash/
site: gemini
date: 2025-12-17
authors: Tulsee Doshi
crawled: 2026-09-13
---

Today, we're expanding the Gemini 3 model family with the release of Gemini 3 Flash, which offers frontier intelligence built for speed at a fraction of the cost. With this release, we’re making Gemini 3’s next-generation intelligence accessible to everyone across Google products.

Last month, we kicked off Gemini 3 with [Gemini 3 Pro](https://blog.google/products/gemini/gemini-3/#note-from-ceo) and [Gemini 3 Deep Think](https://blog.google/products/gemini/gemini-3-deep-think/) mode, and the response has been incredible. Since launch day, we have been processing over 1T tokens per day on our API. We’ve seen you use Gemini 3 to [vibe code simulations](https://x.com/googleaidevs/status/1991333601959350306) to learn about complex topics, build and design [interactive games](https://x.com/googleaidevs/status/1991318283065131160) and understand all types of [multimodal content](https://x.com/googleaidevs/status/1997033279610818745?s=20).

With Gemini 3, we introduced frontier performance across complex reasoning, [multimodal and vision understanding](https://blog.google/technology/developers/gemini-3-pro-vision/) and agentic and vibe coding tasks. Gemini 3 Flash retains this foundation, combining Gemini 3's Pro-grade reasoning with Flash-level latency, efficiency and cost. It not only enables everyday tasks with improved reasoning, but also is our most impressive model for agentic workflows.

Starting today, Gemini 3 Flash is rolling out to millions of people globally:

- For developers in the Gemini API in [Google AI Studio](https://blog.google/technology/developers/build-with-gemini-3-flash), [Gemini CLI](https://developers.googleblog.com/gemini-3-flash-is-now-available-in-gemini-cli/) and our new agentic development platform [Google Antigravity](https://antigravity.google/blog/gemini-3-flash-in-google-antigravity)
- For everyone via the [Gemini app](https://blog.google/products/gemini/gemini-3-flash-gemini-app/) and in [AI Mode in Search](https://blog.google/products/search/google-ai-mode-update-gemini-3-flash)
- For enterprises in [Vertex AI and Gemini Enterprise](https://cloud.google.com/blog/products/ai-machine-learning/gemini-3-flash-for-enterprises)

## Gemini 3 Flash: frontier intelligence at scale

Gemini 3 Flash demonstrates that speed and scale don’t have to come at the cost of intelligence. It delivers frontier performance on PhD-level reasoning and knowledge benchmarks like GPQA Diamond (90.4%) and Humanity’s Last Exam (33.7% without tools), rivaling larger frontier models, and significantly outperforming even the best 2.5 model, Gemini 2.5 Pro, across a number of benchmarks. It also reaches state-of-the-art performance with an impressive score of 81.2% on MMMU Pro, comparable to Gemini 3 Pro.

![A benchmark comparison table showing performance scores and prices for several language models including Gemini 3 Flash, Gemini 3 Pro Thinking, Gemini 2.5 Flash Thinking, Gemini 2.5 Pro Thinking, Claude Sonnet 4.5, GPT-5.2 Extra high, and Grok 4.1 Fast, across various tasks like academic reasoning, scientific knowledge, math, multi-modal understanding, coding, and long context performance.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-flash_final_benchmark-t.width-1200.format-webp.webp)

In addition to its frontier-level reasoning and multimodal capabilities, Gemini 3 Flash was built to be highly efficient, pushing the Pareto frontier of quality vs. cost and speed. When processing at the highest thinking level, Gemini 3 Flash is able to modulate how much it thinks. It may think longer for more complex use cases, but it also uses 30% fewer tokens on average than 2.5 Pro, as measured on typical traffic, to accurately complete everyday tasks with higher performance.

Gemini 3 Flash pushes the Pareto frontier on performance vs. cost and speed.

Performance, here, is measured by [LMArena](https://lmarena.ai/) Elo Score.

![A scatter plot showing LMArena Elo Score versus Price per million tokens for various language models, with a line highlighting the Pareto frontier through 'gemini-3-pro', 'gemini-3-flash', and 'gemini-3-flash-lite'.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-flash_pareto_graph_dec1.width-1200.format-webp.webp)

Gemini 3 Flash’s strength lies in its raw speed, building on the Flash series that developers and consumers already love. It outperforms 2.5 Pro while being 3x faster (based on [Artificial Analysis](https://artificialanalysis.ai/models/gemini-3-flash-reasoning) benchmarking) at a fraction of the cost. Gemini 3 Flash is priced at $0.50/1M input tokens and $3/1M output tokens (audio input remains at $1/1M input tokens).

Gemini 3 Flash outperforms 2.5 Pro in [speed and quality](https://youtu.be/XHhCZOk2WvY).

## For developers: intelligence that keeps up

Gemini 3 Flash is made for iterative development, offering Gemini 3’s Pro-grade coding performance with low latency — it’s able to reason and solve tasks quickly in high-frequency workflows. On SWE-bench Verified, a benchmark for evaluating coding agent capabilities, Gemini 3 Flash achieves a score of 78%, outperforming not only the 2.5 series, but also Gemini 3 Pro. It strikes an ideal balance for agentic coding, production-ready systems and responsive interactive applications.

Gemini 3 Flash’s strong performance in reasoning, tool use and multimodal capabilities is ideal for developers looking to do more complex video analysis, data extraction and visual Q&A, which means it can enable more intelligent applications — like in-game assistants or A/B test experiments — that demand both quick answers and deep reasoning.

Gemini 3 Flash enables multimodal reasoning in a hand-tracked "ball launching puzzle game" game [providing near real-time AI assistance](https://www.youtube.com/watch?v=DNPLK-MvoSg).

Gemini 3 Flash builds and A/B tests [new loading spinner designs in near real-time](https://youtu.be/bY_RarpUdUw), streamlining the design-to-code process.

Gemini 3 Flash uses multimodal reasoning to [analyze and caption an image with contextual UI overlays](https://youtu.be/f0TL0GG_lo8) in near real-time, ultimately transforming a static image into an interactive experience.

Gemini 3 Flash takes a single instruction prompt and [codes three unique design variations](https://youtu.be/z4x9fkbe8SI).

We’ve received a tremendous response from companies using Gemini 3 Flash. Companies like JetBrains, Bridgewater Associates, and Figma are already using it to transform their businesses, recognizing how its inference speed, efficiency and reasoning capabilities perform on par with larger models. Gemini 3 Flash is available today to enterprises via Vertex AI and Gemini Enterprise.

![JetBrains customer testimonial quote](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3Flash_blog_quote-jetbrain.width-100.format-webp.webp)

![Bridgewater customer testimonial quote](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3Flash_blog_quote-aia-labs.width-100.format-webp.webp)

![Figma customer testimonial quote](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3Flash_blog_quote-figma_li.width-100.format-webp.webp)

![Cursor customer testimonial quote](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3Flash_blog_quote-cursor_l.width-100.format-webp.webp)

![Warp customer testimonial quote](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3Flash_blog_quote-warp_lig.width-100.format-webp.webp)

![Harvey customer testimonial quote](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3Flash_blog_quote-harvey_l.width-100.format-webp.webp)

![Astrocade customer testimonial quote](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3Flash_blog_quote-astrocad.width-100.format-webp.webp)

![Presentations.ai customer testimonial quote](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3Flash_blog_quote-presenta.width-100.format-webp.webp)

![Replit customer testimonial quote](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3Flash_blog_quote-replit_l.width-100.format-webp.webp)

![Latitude customer testimonial quote](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3Flash_blog_quote-latitude.width-100.format-webp.webp)

## For everyone: Gemini 3 Flash is rolling out globally

Gemini 3 Flash is now the default model in the Gemini app, replacing 2.5 Flash. That means all of our Gemini users globally will get access to the Gemini 3 experience at no cost, giving their everyday tasks a major upgrade.

Because of Gemini 3 Flash’s incredible multimodal reasoning capabilities, you can use it to help you see, hear and understand any type of information faster. For example, you can ask Gemini to understand your videos and images and turn that content into a helpful and actionable plan in just a few seconds.

Gemini 3 Flash in the Gemini app can [analyze short video content and give you a plan](https://youtu.be/q4rIiPOwimI), like how to improve your golf swing.

As Gemini 3 Flash is optimized for speed, it can [see and guess what you’re drawing](https://youtu.be/wRy269MqaSo) while you’re still sketching it.

You can upload an audio recording and Gemini 3 Flash will [identify your knowledge gaps, create a custom quiz](https://www.youtube.com/watch?v=zg_66Q3oSss), and give you detailed explanations on the answers.

Or you can quickly build fun, useful apps from scratch using your voice without prior coding knowledge. Just dictate to Gemini on the go, and it can transform your unstructured thoughts into a functioning app in minutes.

Gemini 3 Flash is also starting to roll out as the default model for AI Mode in Search with access to everyone around the world.

Building on the reasoning capabilities of Gemini 3 Pro, AI Mode with Gemini 3 Flash is more powerful at parsing the nuances of your question. It considers each aspect of your query to serve thoughtful, comprehensive responses that are visually digestible — pulling real-time local information and helpful links from across the web. The result effectively combines research with immediate action: you get an intelligently organized breakdown alongside specific recommendations — at the speed of Search.

This shines when tackling complex goals with multiple considerations like trying to plan a last-minute trip or learning complex educational concepts quickly.

## Try Gemini 3 Flash today

Gemini 3 Flash is available now in preview via the [Gemini API](https://ai.google.dev/gemini-api/docs/models#gemini-3-flash) in Google AI Studio, [Google Antigravity,](https://antigravity.google/) [Vertex AI](https://cloud.google.com/vertex-ai?e=48754805) and [Gemini Enterprise](https://cloud.google.com/gemini-enterprise?e=48754805). You can also access it through other developer tools like [Gemini CLI](https://developers.googleblog.com/gemini-3-flash-is-now-available-in-gemini-cli/) and [Android Studio](https://android-developers.googleblog.com/2025/12/build-smarter-apps-with-gemini-3-flash). It’s also starting to roll out to everyone in the [Gemini app](https://gemini.google.com/) and [AI Mode](https://www.google.com/search?udm=50&aep=11) in Search, bringing fast access to next-generation intelligence at no cost.

We’re looking forward to seeing what you bring to life with this expanded family of models: Gemini 3 Pro, Gemini 3 Deep Think and now, Gemini 3 Flash.
