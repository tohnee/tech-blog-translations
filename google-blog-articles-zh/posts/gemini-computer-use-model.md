---
title: "推出 Gemini 2.5 Computer Use 模型"
title_en: "Introducing the Gemini 2.5 Computer Use model"
source: https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-computer-use-model/
site: google-blog
date: 2025-10-07
crawled: 2026-09-13
translated: 2026-09-13
---

# 推出 Gemini 2.5 Computer Use 模型

> 原文：[Introducing the Gemini 2.5 Computer Use model](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-computer-use-model/) · Google

今年早些时候，我们曾[提到](https://www.youtube.com/live/o8NiE3XMPrM?si=9uCZ5JXT0xtGyr1H&t=874)，我们将通过 Gemini API 为开发者带来计算机操作（computer use）能力。今天，我们正式发布 [Gemini 2.5 Computer Use 模型](http://ai.google.dev/gemini-api/docs/computer-use)——这是我们基于 Gemini 2.5 Pro 的视觉理解与推理能力打造的新一代专业化模型，可为能够与用户界面（UI）交互的智能体提供支持。它在多个网页与移动端操控基准测试上优于领先的替代方案，且延迟更低。开发者可以通过 [Google AI Studio](http://ai.google.dev/gemini-api/docs/computer-use) 和 [Vertex AI](https://cloud.google.com/vertex-ai/generative-ai/docs/computer-use) 中的 Gemini API 使用这些能力。

尽管 AI 模型可以通过结构化 API 与软件交互，但许多数字任务仍然需要直接操作图形用户界面，例如填写并提交表单。要完成这些任务，智能体必须像人类一样浏览网页和应用：通过点击、输入和滚动。能够原生填写表单、操作下拉菜单和筛选器等交互元素，以及在登录之后进行操作，是构建强大的通用智能体的关键一步。

## 工作原理

该模型的核心能力通过 Gemini API 中新的 `computer\_use` 工具开放，并应在循环中运行。该工具的输入包括用户请求、环境的屏幕截图以及近期操作的历史记录。输入还可以指定是否从[受支持 UI 操作的完整列表](http://ai.google.dev/gemini-api/docs/computer-use#supported-actions)中排除某些函数，或指定要额外包含的自定义函数。

Gemini 2.5 Computer Use 模型流程

![AI 智能体循环示意图：初始任务产生屏幕截图/上下文，发送给模型，模型返回响应给计算机环境以执行操作。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/CTU-Diagram-RD4-V01.width-1200.format-webp.webp)

模型随后分析这些输入并生成响应，通常是一个函数调用，代表某种 UI 操作，例如点击或输入。该响应也可能包含请求最终用户确认的内容，某些操作（例如购买）需要此类确认。客户端代码随后执行收到的操作。

操作执行完成后，一张新的 GUI 屏幕截图和当前 URL 会作为函数响应发送回 Computer Use 模型，重新启动循环。这一迭代过程持续进行，直到任务完成、出现错误，或因安全响应或用户决定而终止交互。

Gemini 2.5 Computer Use 模型主要针对网页浏览器优化，但在移动端 UI 操控任务上也展现出强大潜力。它尚未针对桌面操作系统级控制进行优化。

请看下面的几个演示，了解模型的实际运行情况（此处以 3 倍速播放）。

**提示词：**"从 <https://tinyurl.com/pet-care-signup> 获取所有加利福尼亚州居民宠物的全部详细信息，并把它们作为客户添加到我在 <https://pet-luxe-spa.web.app/> 的宠物美容 CRM 中。然后，为 10 月 10 日上午 8 点之后的任意时间，与专家 Anima Lavar 安排一次复诊预约。就诊原因与其申请的护理项目相同。"

**提示词：**"我的艺术社在集市前集思广益列出了一些任务。看板很混乱，我需要你帮忙把这些任务归类到我创建的一些类别中。打开 [sticky-note-jam.web.app](http://sticky-note-jam.web.app)，确保便签清楚地放在正确的分区里。如果没有，就把它们拖过去。"

## 性能表现

Gemini 2.5 Computer Use 模型在多个网页与移动端操控基准测试中表现出色。下表包含自报数据、Browserbase 运行的评估以及我们自行运行的评估结果。评估详情见 [Gemini 2.5 Computer Use 评估信息](https://storage.googleapis.com/deepmind-media/gemini/computer_use_eval_additional_info.pdf)以及 [Browserbase 的博客文章](https://www.browserbase.com/blog/evaluating-browser-agents)。除非另有说明，所展示的分数均为通过 API 提供的 computer use 工具的成绩。

Gemini 2.5 Computer Use 在多个基准测试上优于领先的替代方案

![基准测试性能表：Gemini 2.5 Computer Use 在 Online-Mind2Web、WebVoyager 和 AndroidWorld 基准测试中领先。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/CTU-Benchmark_Chart-RD5_V01.width-1200.format-webp.webp)

以 Browserbase 的 Online-Mind2Web 测试框架上的表现来衡量，该模型以最低延迟提供了领先的浏览器操控质量。

Gemini 2.5 Computer Use 在保持低延迟的同时实现高准确率

![延迟与质量散点图：Gemini 2.5 Computer Use 延迟最低、准确率最高（准确率 70% 以上，延迟约 225 秒）。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/CTU-Scatterplot-RD7.width-1200.format-webp.webp)

## 我们如何确保安全

我们相信，要构建能让所有人受益的智能体，唯一的方法就是从一开始就坚持负责任。控制计算机的 AI 智能体带来了独特的风险，包括用户的故意滥用、模型的意外行为，以及网页环境中的提示词注入和诈骗。因此，谨慎地实施安全防护措施至关重要。

我们已将安全功能直接训练进模型，以应对这三个关键风险（详见 [Gemini 2.5 Computer Use System Card](https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-2-5-Computer-Use-Model-Card.pdf)）。

此外，我们还为开发者提供安全控制手段，让开发者能够阻止模型自动完成潜在的高风险或有害操作。这类操作的例子包括：损害系统完整性、危害安全性、绕过验证码（CAPTCHA），或控制医疗设备。这些控制手段包括：

- **逐操作安全服务（per-step safety service）：** 一种模型之外、推理时运行的安全服务，在模型提议的每个操作执行之前对其进行评估。
- **系统指令：** 开发者可以进一步指定智能体在执行特定类型的高风险操作之前予以拒绝或请求用户确认。（示例见[文档](https://ai.google.dev/gemini-api/docs/computer-use#safety-security)。）

关于安全措施和最佳实践的更多开发者建议，请参阅我们的[文档](https://ai.google.dev/gemini-api/docs/computer-use#safety-best-practices)。虽然这些防护措施旨在降低风险，但我们敦促所有开发者在上线前对系统进行彻底测试。

## 早期测试者如何使用它

Google 团队已在生产环境中部署该模型，用例包括 UI 测试——它可以让软件开发显著提速。该模型的多个版本也在为 [Project Mariner](https://deepmind.google/models/project-mariner/)、[Firebase Testing Agent](https://firebase.blog/posts/2025/04/app-testing-agent/)，以及 [Search 中 AI Mode](https://blog.google/products/search/ai-mode-agentic-personalized/) 的部分智能体化功能提供支持。

我们早期体验计划的用户也在测试该模型，用它驱动个人助理、工作流自动化和 UI 测试，并取得了出色的效果。用他们自己的话说：

## 如何上手

从今天起，该模型以公开预览版形式提供，可通过 Google AI Studio 和 Vertex AI 上的 Gemini API 访问。

- **立即试用：** 在 [Browserbase](http://gemini.browserbase.com/) 托管的演示环境中体验。
- **开始构建：** 深入阅读我们的[参考代码](https://github.com/google/computer-use-preview)和[文档](http://ai.google.dev/gemini-api/docs/computer-use)（企业使用请参见 [Vertex AI 文档](https://cloud.google.com/vertex-ai/generative-ai/docs/computer-use)），了解如何使用 Playwright 在本地构建你自己的智能体循环，或通过 Browserbase 在云端虚拟机中构建。
- **加入社区：** 我们很期待看到你构建的作品。在我们的[开发者论坛](https://discuss.ai.google.dev/c/gemini-api/4)中分享反馈，帮助我们规划路线图。
