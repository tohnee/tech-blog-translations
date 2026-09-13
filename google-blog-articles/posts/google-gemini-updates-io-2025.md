---
title: "Gemini 2.5: Our most intelligent models are getting even better"
source: https://blog.google/innovation-and-ai/models-and-research/google-deepmind/google-gemini-updates-io-2025/
site: google-blog
date: 2025-05-20
authors: Tulsee Doshi
crawled: 2026-09-13
---

In March, we announced [Gemini 2.5 Pro](https://blog.google/technology/google-deepmind/gemini-model-thinking-updates-march-2025/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=), our most intelligent model yet, and two weeks ago, we brought you our [I/O update early](https://blog.google/products/gemini/gemini-2-5-pro-updates/) for developers to build incredible web apps. Today, we’re sharing even more updates to our [Gemini 2.5](https://deepmind.google/technologies/gemini/?_gl=1*1hcx28i*_up*MQ..*_ga*OTE5NDY4NDk5LjE3NDc1NzI2Mzk.*_ga_LS8HVHCNQ0*czE3NDc1NzI2MzgkbzEkZzAkdDE3NDc1NzI2MzgkajAkbDAkaDA.) model series:

- Beyond 2.5 Pro’s incredible performance [on academic benchmarks](https://deepmind.google/technologies/gemini/pro/), it’s now the world-leading model across the [WebDev Arena](https://web.lmarena.ai/leaderboard) and [LMArena](https://lmarena.ai/?leaderboard) leaderboards, and for [helping people learn](https://blog.google/outreach-initiatives/education/google-gemini-learnlm-update).
- We’re bringing new capabilities to 2.5 Pro and 2.5 Flash: native audio output for a more natural conversational experience, advanced security safeguards, and [Project Mariner](https://deepmind.google/technologies/project-mariner/?_gl=1*1c8pzpn*_up*MQ..*_ga*MTg3MDY5NzA5LjE3NDc0MTgwOTc.*_ga_LS8HVHCNQ0*czE3NDc0MTgwOTckbzEkZzAkdDE3NDc0MTgxMDAkajAkbDAkaDA.)’s computer use capabilities. 2.5 Pro will get even better with [Deep Think](https://deepmind.google/models/gemini/pro), an experimental, enhanced reasoning mode for highly-complex math and coding.
- We continue to invest in the developer experience, introducing thought summaries in the [Gemini API](https://www.googleadservices.com/pagead/aclk?sa=L&ai=DChcSEwisvpPlh62NAxVhkVAGHQQyExAYABABGgJkZw&co=1&ase=2&gclid=Cj0KCQjwiqbBBhCAARIsAJSfZkb2UNm71aDTiQj43uE6u_X4kdQjkW-zJE4ys1-WPCsHAjQPW0JsAfEaAnO5EALw_wcB&ohost=www.google.com&cid=CAESVuD2XZH0cGUhnUN_hgWfLPh0qxdkyaxfS7GgJW3CE1EWqyyuEGeFtJxpp-RPP_6lGT_tcrNml8Z0ycbys16CbucweCE9iTf9Fezie1FFOvssm7ZxarUX&category=acrcp_v1_5&sig=AOD64_3P3Z7aCoP-AB8jidfzdFepXVjQQg&q&nis=4&adurl&ved=2ahUKEwjz0Y7lh62NAxXXSEEAHTUKO98Q0Qx6BAgKEAE) and in [Vertex AI](https://console.cloud.google.com/freetrial?redirectPath=/vertex-ai/studio) for more transparency, extending thinking budgets to 2.5 Pro for more control, and adding support for MCP tools in the Gemini API and [SDK](https://ai.google.dev/gemini-api/docs/migrate) for access to more open source tools.
- 2.5 Flash is now available to everyone in the [Gemini app](http://gemini.google.com/), and we'll make our updated version generally available in [Google AI Studio](http://aistudio.google.com/) for developers and in [Vertex AI](https://console.cloud.google.com/freetrial?redirectPath=/vertex-ai/studio) for enterprises in early June, with 2.5 Pro soon after.

This remarkable progress is the result of the relentless effort of teams across Google to improve our technologies, and develop and release them safely and responsibly. Let’s dive in.

## 2.5 Pro performs better than ever

We recently [updated 2.5 Pro](https://blog.google/products/gemini/gemini-2-5-pro-updates/) to help developers build richer, interactive web apps. It’s great to see the [positive reaction from users and developers](https://www.youtube.com/watch?v=c6UkBTTOIAE%27) and we’re continuing to make improvements based on user feedback.

In addition to its strong performance on academic benchmarks, the new 2.5 Pro is now leading the popular coding leaderboard, [WebDev Arena](https://web.lmarena.ai/leaderboard), with an ELO score of 1415. It’s also leading across all leaderboards of the [LMArena](https://lmarena.ai/?leaderboard), which evaluates human preference in various dimensions. And, with its 1 million-token context window, 2.5 Pro has state-of-the-art [long context and video understanding performance](https://developers.googleblog.com/en/gemini-2-5-video-understanding/).

Since incorporating LearnLM, our family of models built with educational experts, 2.5 Pro is also now the [leading model for learning](https://blog.google/outreach-initiatives/education/google-gemini-learnlm-update). In head-to-head comparisons evaluating its pedagogy and effectiveness, educators and experts preferred Gemini 2.5 Pro over other models across a diverse range of scenarios. And, it [outperformed top models](https://goo.gle/LearnLM-May25) on every one of the [five principles of learning science](http://goo.gle/learnlm) used to build AI systems for learning.

Read more in our updated [Gemini 2.5 Pro model card](https://storage.googleapis.com/model-cards/documents/gemini-2.5-pro-preview.pdf) and on the [Gemini technology page](https://deepmind.google/technologies/gemini/#introduction).

### Deep Think

Through exploring the frontiers of Gemini’s thinking capabilities, we’re starting to test an enhanced reasoning mode called [Deep Think](https://deepmind.google/models/gemini/pro) that uses new research techniques enabling the model to consider multiple hypotheses before responding.

2.5 Pro Deep Think gets an impressive score on [2025 USAMO](https://maa.org/news/2025-usamo-and-usajmo-thresholds-now-available/), currently one of the hardest math benchmarks. It also leads on [LiveCodeBench](https://livecodebench.github.io/leaderboard.html), a difficult benchmark for competition-level coding, and scores 84.0% on [MMMU](https://mmmu-benchmark.github.io/), which tests multimodal reasoning.

![Chart demonstrating Gemini 2.5 Pro Deep think's advanced capabilities](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/deep-think-chart.width-1200.format-webp.webp)

Because we're defining the frontier with 2.5 Pro DeepThink, we're taking extra time to conduct more frontier safety evaluations and get further input from safety experts. As part of that, we’re going to make it available to trusted testers via the [Gemini API](https://ai.google.dev/) to get their feedback before making it widely available.

## An even better 2.5 Flash

[2.5 Flash](https://deepmind.google/technologies/gemini/flash/) is our most efficient workhorse model designed for speed and low-cost — and it’s now better across many dimensions. It’s improved across key benchmarks for reasoning, multimodality, code and long context while getting even more efficient, using 20-30% less tokens in our evaluations.

![Chart comparing Gemini 2.5 Flash with other models](https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/gemini_2-5_flashcomp_benchmarks_cropped_light2x.gif)

The new 2.5 Flash is now available for preview in [Google AI Studio](http://aistudio.google.com/) for developers, in [Vertex AI](https://console.cloud.google.com/vertex-ai/studio/multimodal?model=gemini-2.5-flash-preview-05-20) for enterprise and in the [Gemini app](http://gemini.google.com/) for everyone. And in early June, it’ll be generally available for production.

Read more in our updated [Gemini 2.5 Flash model card](https://storage.googleapis.com/model-cards/documents/gemini-2.5-flash-preview.pdf) and on the [Gemini technology page](https://deepmind.google/technologies/gemini/#introduction).

### Native audio output and improvements to Live API

Today, the [Live API](https://ai.google.dev/gemini-api/docs/live) is introducing a preview version of audio-visual input and native audio out dialogue, so you can directly build conversational experiences, with a more natural and expressive Gemini.

It also allows the user to steer its tone, accent and style of speaking. For example, you can tell the model to use a dramatic voice when telling a story. And it supports tool use, to be able to search on your behalf.

You can experiment with a set of early features, including:

- Affective Dialogue, in which the model detects emotion in the user's voice and responds appropriately.
- Proactive Audio, in which the model will ignore background conversations and know when to respond.
- Thinking in the Live API, in which the model leverages Gemini’s thinking capabilities to support more complex tasks.

We’re also releasing new previews for text-to-speech in 2.5 Pro and 2.5 Flash. These have first-of-its-kind support for multiple speakers, enabling text-to-speech with two voices via native audio out.

Like Native Audio dialogue, text-to-speech is expressive, and can capture really subtle nuances, such as whispers. It works in over 24 languages and seamlessly switches between them.

This text-to-speech capability will be available later today in the [Gemini API](https://ai.google.dev/).

### Computer use

We're bringing [Project Mariner](https://deepmind.google/technologies/project-mariner/)'s computer use capabilities into the [Gemini API](https://ai.google.dev/) and [Vertex AI](https://console.cloud.google.com/freetrial?redirectPath=/vertex-ai/studio). Companies like Automation Anywhere, UiPath, Browserbase, Autotab, The Interaction Company and Cartwheel are exploring its potential, and we're excited to roll it out more broadly for developers to experiment with this summer.

### Better security

We’ve also significantly increased protections against security threats, like indirect prompt injections. This is when malicious instructions are embedded into the data an AI model retrieves. Our [new security approach](https://storage.googleapis.com/deepmind-media/Security%20and%20Privacy/Gemini_Security_Paper.pdf) helped significantly increase Gemini’s protection rate against indirect prompt injection attacks during tool use, making Gemini 2.5 our most secure model family to date.

Read more about [our work across safety, responsibility and security](https://deepmind.google/about/responsibility-safety/?_gl=1*10qw615*_up*MQ..*_ga*NDcyMjA1ODA3LjE3NDc0MDI5ODA.*_ga_LS8HVHCNQ0*czE3NDc0MDI5ODAkbzEkZzAkdDE3NDc0MDI5ODAkajAkbDAkaDA.), and [how we’re advancing Gemini’s security safeguards](https://deepmind.google/discover/blog/advancing-geminis-security-safeguards/) on the Google DeepMind blog.

### Thought summaries

2.5 Pro and Flash will now include thought summaries in the [Gemini API](https://ai.google.dev/) and in [Vertex AI](https://console.cloud.google.com/freetrial?redirectPath=/vertex-ai/studio). Thought summaries take the model’s raw thoughts and organize them into a clear format with headers, key details and information about model actions, like when they use tools.

We hope that with a more structured, streamlined format on the model’s thinking process, developers and users will find the interactions with Gemini models easier to understand and debug.

### Thinking budgets

We launched 2.5 Flash with thinking budgets to give developers more control over cost by balancing latency and quality. And we’re extending this capability to 2.5 Pro. This allows you to control the number of tokens a model uses to think before it responds, or even turn its thinking capabilities off.

Gemini 2.5 Pro with budgets will be generally available for stable production use in the coming weeks, along with our generally available model.

### MCP support

We added native SDK support for Model Context Protocol (MCP) definitions in the Gemini API for easier integration with open-source tools. We’re also exploring ways to deploy MCP servers and other hosted tools, making it easier for you to build agentic applications.

We’re always innovating on new approaches to improve our models and our developer experience, including making them more efficient and performant, and continuing to respond to developer feedback, so please keep it coming! We also continue to double down on the breadth and depth of our fundamental research — pushing the frontiers of Gemini’s capabilities. More to come soon.

Learn more about [Gemini and its capabilities on our website](https://deepmind.google/technologies/gemini/#introduction).
