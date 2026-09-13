---
title: "推出 Gemini 3.6 Flash、3.5 Flash-Lite 与 3.5 Flash Cyber"
title_en: "Introducing Gemini 3.6 Flash, 3.5 Flash-Lite, and 3.5 Flash Cyber"
source: https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber/
site: gemini
date: 2026-07-21
crawled: 2026-09-13
translated: 2026-09-13
---

# 推出 Gemini 3.6 Flash、3.5 Flash-Lite 与 3.5 Flash Cyber

> 原文：[Introducing Gemini 3.6 Flash, 3.5 Flash-Lite, and 3.5 Flash Cyber](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber/) · Google

构建生产级 AI 智能体的开发者与客户，需要更高的 token 效率、更低的延迟和更可靠的性能。我们的 Flash 系列模型正是为效率与质量的黄金平衡点而生，帮助智能体工作流规模化扩展。在 Gemini 3.5 Flash 的基础上，我们推出以下新模型：

- **3.6 Flash：**我们的主力模型，带来更出色的编程、知识工作与多模态性能。根据 [Artificial Analysis Index](https://artificialanalysis.ai/models/gemini-3-6-flash)，与 3.5 Flash 相比，它的输出 token 用量降低了 17%，而在 [Datacurve](https://deepswe.datacurve.ai/) 的 DeepSWE 等部分基准测试上，降幅最高可达 65%，同时单个输出 token 的成本更低。
- **3.5 Flash-Lite：**我们最快、最具性价比的 3.5 系列模型，按照 Artificial Analysis Index 的测量可达每秒 350 个输出 token，在智能体工作流中的表现也显著超越此前的 Flash-Lite 世代。
- **CodeMender 中的 3.5 Flash Cyber：**成功的网络安全应用需要对模型与智能体基础设施进行精心编排。我们推出了一套全新组合：一个高效、专注网络安全的专用模型，搭配我们的代码安全智能体 CodeMender，展现出前沿水平的竞争力。

除了今天发布的这些，Gemini 3.5 Pro 目前正在与合作伙伴进行测试，我们计划在其就绪后尽快广泛推出。与此同时，我们的团队已经在专注构建下一代模型。我们已启动迄今最具雄心的预训练项目——Gemini 4，并对目前的进展感到兴奋。

## 3.6 Flash：比 3.5 Flash 更高效、质量更佳

Gemini 3.6 Flash 直接建立在开发者和客户对 3.5 Flash 的反馈之上。3.6 Flash 不仅在编程和知识工作上更进一步，还在此基础上显著提升了 token 效率。例如，在 Artificial Analysis Index 上，3.6 Flash 的输出 token 消耗比 3.5 Flash 少 17%。完成多步骤工作流所需的推理步骤和工具调用次数也更少。

这种效率提升还伴随着比 3.5 Flash 更低的价格。输入 token 为 1.50 美元/100 万、输出 token 为 7.50 美元/100 万，3.6 Flash 降低了每个智能体任务的整体成本，让构建和运行智能体更具成本效益。

在 OSWorld 验证任务（API）中，3.6 Flash 相比 3.5 Flash 展现出更好的 token 效率和更低的冗余输出

在提升效率的同时，3.6 Flash 在各用例上的性能相比 3.5 Flash 仍有提升：

- 3.6 Flash 以更少的多余代码编辑和更少的执行循环实现了更高的精确度，在 DeepSWE 上表现为（49% 对 37%），并在 ML Research 上有显著改进，在 MLE Bench 上表现为（63.9% 对 49.7%）。
- 它的计算机操作（computer use）能力有所提升，在 OSWorld-Verified 上表现为（83.0% 对 78.4%）。计算机操作现在已作为内置客户端工具，通过 Gemini API 和 Gemini Enterprise 提供。
- 它在知识工作上优于 3.5 Flash，GDPval-AA v2 等基准测试可以证明（1421 对 1349）。Hebbia 和 Harvey 等客户发现它在文档解析、图表与数据分析、报告起草等多模态任务上尤为出色。

3.6 Flash 借助 AIS 上的 Managed Agents，可以比 3.5 Flash 更高效、更准确地解析和分析金融数据与会议记录（AIS）

3.6 Flash 使用 AGY 上的多智能体编排来执行代码迁移，相比 3.5 Flash 延迟更低、质量更高（AGY）

3.6 Flash 借助 canvas 帮助开发面向 3D 工作流的摄影级纹理提取器（Gemini 应用）

3.6 Flash 凭借强大的视觉理解能力，使用 AGY 和 tldraw 离线编辑器构建交互式主题工作室（AGY）。

![图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-6-flash__evals__figure-.width-1200.format-webp.webp)

![图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-6-flash__evals__quality.width-1200.format-webp.webp)

客户反映，3.6 Flash 在成本和质量上都是一次跨越，在复杂工作流和知识型任务中平衡了 token 效率、准确性与速度：

![来自 Figma 的评价](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-6__testimonial-figma__ke.width-100.format-webp_fLGaXIs.webp)

![来自 Harvey 的评价](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-6__testimonial-harvey__k.width-100.format-webp_LYvvm1L.webp)

![来自 Hebbia 的评价](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-6__testimonial-hebbia__k.width-100.format-webp_UIh1200.webp)

![来自 JetBrains 的评价](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-6__testimonial-jetbrains.width-100.format-webp_xEv9X02.webp)

## 以安全为本

3.6 Flash 发布时即内置了增强的[前沿安全框架](https://deepmind.google/blog/strengthening-our-frontier-safety-framework/)防护措施，覆盖化学、生物、放射与核（CBRN）以及网络攻击滥用等领域。这些防护措施让模型对越狱攻击的抵抗力大幅提升。与此同时，模型经过训练，能尽量减少对有益用途的拒绝。

更多信息请参阅 [3.6 Flash](https://deepmind.google/models/model-cards/gemini-3-6-flash/) 模型卡。

## 3.5 Flash-Lite：为智能体工作流的规模化而生

除 Flash 之外，我们还发布了 Gemini 3.5 Flash-Lite，专为低延迟任务以及高吞吐量对开发者工作流至关重要的任务而设计，例如智能体搜索和文档处理。

3.5 Flash-Lite 是 3.5 系列中最快的模型。根据 [Artificial Analysis](https://artificialanalysis.ai/models/gemini-3-5-flash-lite) 的测量，它以 350 输出 token/秒的速度运行。其定价为输入 token 0.3 美元/100 万、输出 token 2.5 美元/100 万，质量显著优于 3.1 Flash-Lite，为运行高吞吐量生产流量的开发者和客户提供了出色的性价比。

3.5 Flash-Lite 以低于 3.5 Flash 的延迟执行大批量任务。

3.5 Flash-Lite 支持智能体系统的高效扩展。在各个思考级别上，该模型都显著优于 3.1 Flash-Lite。开发者可以根据工作负载灵活配置：对大批量任务使用 minimal 和 low 思考级别，优先保证低延迟、低成本的执行；或启用更高的思考级别来处理多步骤的子智能体工作负载。该模型现在还内置了计算机操作工具，可以在各平台上可靠地支持这些智能体任务。

它在编程和智能体任务上有显著提升，Terminal-Bench 2.1 可为例证（54% 对 31%）；长上下文方面同样如此，GDM-MRCR v2 可为例证（72.2% 对 60.1%）；真实世界任务执行方面亦然，GDPval-AA v2 可为例证（1140 对 642）。

![图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-5-flash-lite__evals__co.width-1200.format-webp.webp)

事实上，在许多智能体和编程评测中，3.5 Flash-Lite 甚至超越了 3 Flash，包括 SWE-Bench Pro（54.2% 对 49.6%）和 OSWorld-Verified（74.0% 对 65.1%），这让它成为在 2.5 和 3 Flash 上运行工作负载时更快、更强大的选择。

![图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-5-flash-lite__evals__co.width-1200.format-webp_TEfcucF.webp)

3.5 Flash-Lite 从海量电商数据集中提取产品特性并进行综合。

3.5 Flash-Lite 作为主智能体与 3.6 Flash 协作，即时生成 25 个独特的、可供探索的网页设计概念。

3.5 Flash-Lite 凭借多模态理解能力，可以规模化完成小票的翻译与摘要。

3.5 Flash-Lite 通过即时生成并迭代多个方案来构建游戏。

3.5 Flash-Lite 的早期客户特别强调了它在速度、智能与成本效率上的独特组合，这正是扩展智能体工作流和数据处理任务所需要的：

![来自 Ashler 的评价](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-5-flash-lite__testimonia.width-100.format-webp.webp)

![来自 Palo Alto Networks 的评价](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-5-flash-lite__testimonia.width-100.format-webp_CdSRKRm.webp)

![来自 Ramp 的评价](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-5-flash-lite__testimonia.width-100.format-webp_dgscSYO.webp)

关于该模型的更多信息，请参阅 [3.5 Flash-Lite](https://deepmind.google/models/model-cards/gemini-3-5-flash-lite/) 模型卡。

## CodeMender 中的 3.5 Flash Cyber：高效发现并修复漏洞

AI 模型发现安全漏洞的速度，已经超过了现有系统的修复速度。应对这一日益严峻的威胁，需要一种能力强大且高效的方式来保障软件安全。

Flash 的性能与效率使其成为大规模检测、验证和修补代码安全问题的理想基础。[Gemini 3.5 Flash Cyber](https://deepmind.google/blog/introducing-gemini-3-5-cyber-flash/) 构建在 3.5 Flash 之上，并针对网络安全漏洞的发现与修复进行了微调，每 token 价格低于更大的模型。

CodeMender 使用多个 3.5 Flash Cyber 智能体协同工作，最终产出一份汇总报告；在该产品中，3.5 Flash Cyber 在流行基准测试 CyberGym 上达到了前沿水平的竞争力。

![图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-5-flash-cyber__evals__c.width-1200.format-webp.webp)

鉴于这项技术的双重用途性质，我们对 3.5 Flash Cyber 的部署采取了审慎的方式。该模型即将作为受限访问试点计划的一部分，仅通过 [CodeMender](https://deepmind.google/blog/introducing-codemender-an-ai-agent-for-code-security/) 向政府和受信任的合作伙伴开放。这将让一线防御者在关键漏洞被利用之前抢先发现并修复它们，同时遏制更广泛的滥用。

## 3.6 Flash 与 3.5 Flash-Lite：即刻上手

3.6 Flash 与 3.5 Flash-Lite 从今天起即可使用：

- 开发者可通过 [Google AI Studio](https://aistudio.google.com/prompts/new_chat?model=gemini-3.6-flash) 和 [Android Studio](https://developer.android.com/studio) 使用 Gemini API。3.6 Flash 也在 [Google Antigravity](https://antigravity.google/) 中可用。请从[开发者指南](https://ai.google.dev/gemini-api/docs/latest-model)开始。
- 企业用户可通过 [Gemini Enterprise Agent Platform](https://console.cloud.google.com/agent-platform/studio/multimodal/) 使用。3.6 Flash 也在 [Gemini Enterprise 应用](https://cloud.google.com/gemini-enterprise?e=48754805)中可用。
- 所有人都可通过 [Gemini 应用](http://gemini.google/)使用。3.5 Flash-Lite 也正在 Google Search 中开始推送。

在开始使用 3.6 Flash 和 3.5 Flash-Lite 构建时，我们欢迎您的反馈，以改进未来的 Gemini 模型，并期待尽快发布 3.5 Pro。
