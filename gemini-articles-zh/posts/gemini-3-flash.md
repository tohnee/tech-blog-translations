---
title: "Gemini 3 Flash：为速度而生的前沿智能"
title_en: "Gemini 3 Flash: frontier intelligence built for speed"
source: https://blog.google/products-and-platforms/products/gemini/gemini-3-flash/
site: gemini
date: 2025-12-17
crawled: 2026-09-13
translated: 2026-09-13
---

# Gemini 3 Flash：为速度而生的前沿智能

> 原文：[Gemini 3 Flash: frontier intelligence built for speed](https://blog.google/products-and-platforms/products/gemini/gemini-3-flash/) · Google

今天，我们通过发布 Gemini 3 Flash 扩展了 Gemini 3 模型家族，它以极低的成本提供了为速度而打造的前沿智能。通过这次发布，我们让 Gemini 3 的下一代智能通过 Google 各产品触达每一个人。

上个月，我们以 [Gemini 3 Pro](https://blog.google/products/gemini/gemini-3/#note-from-ceo) 和 Gemini 3 Deep Think 模式拉开了 Gemini 3 的序幕，反响非常热烈。自发布之日起，我们的 API 每天处理的 token 量已超过 1 万亿。我们看到大家用 Gemini 3 来 vibe code 出模拟程序以学习复杂的主题、构建和设计[互动游戏](https://x.com/googleaidevs/status/1991318283065131160)，以及理解各类[多模态内容](https://x.com/googleaidevs/status/1997033279610818745?s=20)。

在 Gemini 3 中，我们在复杂推理、[多模态与视觉理解](https://blog.google/technology/developers/gemini-3-pro-vision/)以及智能体化和 vibe coding 任务上实现了前沿性能。Gemini 3 Flash 延续了这一基础，将 Gemini 3 的 Pro 级推理能力与 Flash 级的延迟、效率和成本结合在一起。它不仅能以更强的推理能力完成日常任务，还是我们在智能体化工作流上最令人印象深刻的模型。

从今天起，Gemini 3 Flash 开始面向全球数百万人推送：

- 面向开发者的版本可通过 [Google AI Studio](https://blog.google/technology/developers/build-with-gemini-3-flash) 中的 Gemini API、[Gemini CLI](https://developers.googleblog.com/gemini-3-flash-is-now-available-in-gemini-cli/) 以及我们全新的智能体化开发平台 [Google Antigravity](https://antigravity.google/blog/gemini-3-flash-in-google-antigravity) 使用
- 面向所有人的版本可通过 [Gemini 应用](https://blog.google/products/gemini/gemini-3-flash-gemini-app/)以及 Search 中的 [AI Mode](https://blog.google/products/search/google-ai-mode-update-gemini-3-flash) 使用
- 面向企业的版本可通过 [Vertex AI 和 Gemini Enterprise](https://cloud.google.com/blog/products/ai-machine-learning/gemini-3-flash-for-enterprises) 使用

## Gemini 3 Flash：大规模的前沿智能

Gemini 3 Flash 证明了速度与规模不必以牺牲智能为代价。它在 GPQA Diamond（90.4%）和 Humanity's Last Exam（不使用工具时 33.7%）等博士级推理与知识基准测试上表现出前沿性能，可与更大的前沿模型相媲美，并在多项基准测试上显著超越 2.5 系列中最好的模型 Gemini 2.5 Pro。它还在 MMMU Pro 上以 81.2% 的出色成绩达到最先进水平，与 Gemini 3 Pro 相当。

![一张基准测试对比表，展示了 Gemini 3 Flash、Gemini 3 Pro Thinking、Gemini 2.5 Flash Thinking、Gemini 2.5 Pro Thinking、Claude Sonnet 4.5、GPT-5.2 Extra high 和 Grok 4.1 Fast 等多个语言模型在学术推理、科学知识、数学、多模态理解、编程和长上下文性能等各类任务上的性能得分与价格。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-flash_final_benchmark-t.width-1200.format-webp.webp)

除了前沿级的推理与多模态能力之外，Gemini 3 Flash 还被打造得极为高效，不断推进质量与成本、速度之间的帕累托前沿。在最高思考级别下处理任务时，Gemini 3 Flash 能够调节自身的思考量。面对更复杂的使用场景，它可能会思考更久，但按典型流量测算，它平均比 2.5 Pro 少用 30% 的 token，就能以更高的性能准确地完成日常任务。

Gemini 3 Flash 在性能与成本、速度之间推进了帕累托前沿。

这里的性能以 [LMArena](https://lmarena.ai/) Elo 分数衡量。

![一张散点图，横轴为每百万 token 的价格，纵轴为 LMArena Elo 分数，图中标出了多个语言模型，并用一条线勾勒出经过 gemini-3-pro、gemini-3-flash 和 gemini-3-flash-lite 的帕累托前沿。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-flash_pareto_graph_dec1.width-1200.format-webp.webp)

Gemini 3 Flash 的优势在于其原始速度，它建立在开发者和消费者早已喜爱的 Flash 系列之上。它以更低的成本超越了 2.5 Pro，同时速度快 3 倍（基于 [Artificial Analysis](https://artificialanalysis.ai/models/gemini-3-flash-reasoning) 的基准测试）。Gemini 3 Flash 的定价为输入 token 每百万 0.5 美元、输出 token 每百万 3 美元（音频输入仍为每百万 1 美元）。

Gemini 3 Flash 在[速度与质量](https://youtu.be/XHhCZOk2WvY)上均超越 2.5 Pro。

## 面向开发者：跟得上的智能

Gemini 3 Flash 为迭代式开发而生，以低延迟提供 Gemini 3 的 Pro 级编程性能——它能够在高频工作流中快速推理并完成任务。在用于评估编程智能体能力的基准测试 SWE-bench Verified 上，Gemini 3 Flash 取得了 78% 的成绩，不仅超越 2.5 系列，还超越了 Gemini 3 Pro。它在智能体化编程、可投产系统和响应迅速的交互式应用之间取得了理想平衡。

Gemini 3 Flash 在推理、工具使用和多模态能力上的出色表现，非常适合希望进行更复杂视频分析、数据提取和视觉问答的开发者，这意味着它可以支撑更智能的应用——比如游戏内助手或 A/B 测试实验——这类应用既要求快速响应，又要求深度推理。

Gemini 3 Flash 在一款手部追踪的「发射小球的解谜游戏」中实现多模态推理，[提供近乎实时的 AI 辅助](https://www.youtube.com/watch?v=DNPLK-MvoSg)。

Gemini 3 Flash 构建 A/B 测试并在[近乎实时地迭代新的加载动画设计](https://youtu.be/bY_RarpUdUw)，简化从设计到代码的流程。

Gemini 3 Flash 使用多模态推理，在近乎实时的情况下[为图像添加带有上下文 UI 覆盖层的分析与图注](https://youtu.be/f0TL0GG_lo8)，最终将一张静态图像转变为可交互的体验。

Gemini 3 Flash 接收单条指令提示词，就能[写出三种独特的设计变体](https://youtu.be/z4x9fkbe8SI)。

我们已经收到了使用 Gemini 3 Flash 的企业的热烈反响。JetBrains、Bridgewater Associates 和 Figma 等公司已经在使用它来变革自身业务，它们看中的是其在推理速度、效率和推理能力上与更大模型不相上下的表现。Gemini 3 Flash 现已通过 Vertex AI 和 Gemini Enterprise 面向企业开放。

![JetBrains 客户证言](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3Flash_blog_quote-jetbrain.width-100.format-webp.webp)

![Bridgewater 客户证言](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3Flash_blog_quote-aia-labs.width-100.format-webp.webp)

![Figma 客户证言](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3Flash_blog_quote-figma_li.width-100.format-webp.webp)

![Cursor 客户证言](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3Flash_blog_quote-cursor_l.width-100.format-webp.webp)

![Warp 客户证言](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3Flash_blog_quote-warp_lig.width-100.format-webp.webp)

![Harvey 客户证言](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3Flash_blog_quote-harvey_l.width-100.format-webp.webp)

![Astrocade 客户证言](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3Flash_blog_quote-astrocad.width-100.format-webp.webp)

![Presentations.ai 客户证言](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3Flash_blog_quote-presenta.width-100.format-webp.webp)

![Replit 客户证言](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3Flash_blog_quote-replit_l.width-100.format-webp.webp)

![Latitude 客户证言](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3Flash_blog_quote-latitude.width-100.format-webp.webp)

## 面向所有人：Gemini 3 Flash 正在全球推送

Gemini 3 Flash 现已成为 Gemini 应用中的默认模型，取代 2.5 Flash。这意味着我们全球所有 Gemini 用户都能免费获得 Gemini 3 的体验，让他们的日常任务得到一次重大升级。

得益于 Gemini 3 Flash 出色的多模态推理能力，你可以借助它更快地看、听并理解任何类型的信息。例如，你可以让 Gemini 理解你的视频和图片，并在几秒钟内把这些内容转化为一份实用且可执行的计划。

Gemini 应用的 Gemini 3 Flash 可以[分析短视频内容并给你一份计划](https://youtu.be/q4rIiPOwimI)，比如如何改进你的高尔夫挥杆动作。

由于 Gemini 3 Flash 针对速度进行了优化，它可以在你还在涂画时就[看懂并猜出你画的是什么](https://youtu.be/wRy269MqaSo)。

你还可以上传一段录音，Gemini 3 Flash 会[找出你的知识盲区并生成一份定制测验](https://www.youtube.com/watch?v=zg_66Q3oSss)，并针对答案给出详细讲解。

或者，你无需任何编程知识，只用语音就能从零快速构建有趣且实用的应用。只需随时随地对着 Gemini 口述，它就能在几分钟内把你零散的想法变成一个可以运行的应用。

Gemini 3 Flash 也开始作为 Search 中 AI Mode 的默认模型向全球所有用户推送。

凭借 Gemini 3 Pro 的推理能力，搭载 Gemini 3 Flash 的 AI Mode 在解析问题细微差别方面更为强大。它会考虑你查询的每个方面，给出周到、全面且视觉上易于消化的回答——同时从全网拉取实时本地信息与实用链接。其结果实际上把研究与即时行动结合了起来：你会得到一份组织清晰的拆解分析，并附带具体建议——而且是以 Search 的速度完成。

在处理包含多重考量的复杂目标时，比如计划一场说走就走的旅行，或者快速学习复杂的教育概念，这一点尤为出彩。

## 今天就来试试 Gemini 3 Flash

Gemini 3 Flash 现已通过 Google AI Studio 中的 [Gemini API](https://ai.google.dev/gemini-api/docs/models#gemini-3-flash)、[Google Antigravity](https://antigravity.google/)、[Vertex AI](https://cloud.google.com/vertex-ai?e=48754805) 和 [Gemini Enterprise](https://cloud.google.com/gemini-enterprise?e=48754805) 以预览版形式提供。你也可以通过 [Gemini CLI](https://developers.googleblog.com/gemini-3-flash-is-now-available-in-gemini-cli/) 和 [Android Studio](https://android-developers.googleblog.com/2025/12/build-smarter-apps-with-gemini-3-flash) 等其他开发者工具使用它。它同时开始向 [Gemini 应用](https://gemini.google.com/)和 Search 中的 [AI Mode](https://www.google.com/search?udm=50&aep=11) 的所有用户推送，让大家免费、快速地使用下一代智能。

我们期待看到你用这个不断壮大的模型家族——Gemini 3 Pro、Gemini 3 Deep Think，以及现在的 Gemini 3 Flash——创造出怎样的作品。
