---
title: "Grok Code Fast 1"
title_en: "Grok Code Fast 1"
date: 2025-08-28
source: https://x.ai/news/grok-code-fast-1
crawled: 2026-09-22
translated: 2026-09-22
---

# Grok Code Fast 1

> 原文：[Grok Code Fast 1](https://x.ai/news/grok-code-fast-1) · xAI

2025 年 8 月 28 日

我们很高兴地介绍 grok-code-fast-1，一个快速且经济、擅长智能体编码的推理模型。

![抽象数字猎豹](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fgrok-code-fast.18c66acf.webp&w=1200&q=75)

## [一台飞快的日常主力](#a-speedy-daily-driver)

如今的模型固然强大，但它们往往不像是为智能体编码工作流专门打造的那样——推理与工具调用的循环常常慢得让人着急。作为智能体编码工具的重度用户，我们的工程师看到了空间：需要一个更敏捷、响应更快的方案，为日常任务优化。

我们从零开始构建 `grok-code-fast-1`，起点是一个全新的模型架构。为了打下坚实的基础，我们精心组装了富含编程相关内容的预训练语料。在后训练阶段，我们精选了反映真实世界 pull request 和编码任务的高质量数据集。

在整个训练过程中，我们与发布合作伙伴密切协作，打磨模型在他们智能体平台内的行为。`grok-code-fast-1` 已熟练掌握 grep、终端和文件编辑等常用工具，因此在你的心头好 IDE 里应当宾至如归。

我们与精选的发布合作伙伴联手，限时免费提供 `grok-code-fast-1`，包括 GitHub Copilot、Cursor、Cline、Roo Code、Kilo Code、opencode 和 Windsurf。

[![Cursor 标识](/_next/static/media/cursor.c6f1f8ea.svg)

免费试用

Cursor](https://cursor.com)[![GitHub Copilot 标识](/_next/static/media/copilot.a16b7bcb.svg)

免费试用

GitHub Copilot](https://github.com/features/copilot)[![Cline 标识](/_next/static/media/cline.9216a6a2.svg)

免费试用

Cline](https://cline.bot/)

## [快如闪电](#blazing-fast)

我们的推理与超算团队开发了多项创新技术，大幅提升了服务速度，带来独一无二的响应体验——你还没读完思考轨迹的第一段，模型就已经调用完几十个工具了。我们还在提示词缓存优化上下了功夫，与发布合作伙伴配合使用时，缓存命中率经常超过 90%。

## [一位多面手程序员](#a-versatile-programmer)

`grok-code-fast-1` 在整个软件开发技术栈上都异常全能，尤其擅长 TypeScript、Python、Java、Rust、C++ 和 Go。它可以在极少的监督下完成常见编程任务：从从零到一构建项目、对代码库问题给出富有洞见的回答，到实施外科手术式的 bug 修复。

示例 1，共 2 个战斗模拟器

[](https://data.x.ai/battle-sim.mp4)

![Danny Limanseta](/_next/image?url=https%3A%2F%2Fpbs.twimg.com%2Fprofile_images%2F1653760191542996994%2FgxsaTn-0_400x400.png&w=96&q=75)

[Danny Limanseta

@dannylimanseta](https://x.com/dannylimanseta)

它快到我不得不改变自己在 Cursor 里的工作方式。

阅读更多

Grok Code Fast 快得离谱，它可能是我目前用过的最快的模型。它快到我不得不改变自己在 Cursor 里的工作方式。

我用 Cursor 上的 Grok Code Fast 不到一天就拼出了这个战斗模拟器原型。因为它响应极快、指令遵循又好，我发现给它更小、更专注的任务反而效果更好。这样我可以快速迭代，把它精确引向我想要的方向。

做这个战斗模拟器时，我的工作流是先让它规划大功能，再拆解成分阶段执行。这比一次性甩给它一个巨大的提示词效果好得多。战斗模拟器就是这样顺畅完成的——在 Cursor 里快速迭代，直到达到我想要的样子。

## [一个经济的选择](#an-economical-choice)

我们将 `grok-code-fast-1` 定位为人人可用的模型，定价为：

- 每百万输入 token 0.20 美元
- 每百万输出 token 1.50 美元
- 每百万缓存输入 token 0.02 美元

`grok-code-fast-1` 为开发者每天面对的任务而打造，在性能与成本之间取得了出色的平衡。它的长处在于以经济、紧凑的形态交付强劲性能，是快速且高性价比地处理常见编码任务的多面手选择。

### 模型性能

每秒 token 数与输出价格对比

每秒 token 数（TPS）

190

输出价格/每 100 万 token

$18

### 方法说明

TPS 指标通过各模型提供商的 API 直接测量响应生成速度计算得出，只统计最终响应的 token。

- Gemini 2.5 Pro、GPT-5 和 Claude Sonnet 4：使用各自的公开 API 测量。

- Grok Code Fast 1 和 Grok 4：使用 xAI API 测量。

- Qwen3-Coder：部署在 DeepInfra 上，以低精度（fp4）运行，会降低响应质量。

我们采取整体性的方式评估模型性能，将公开基准与真实世界测试相结合。在 SWE-Bench-Verified 的完整子集上，`grok-code-fast-1` 使用我们自己的内部框架取得 70.8%。

尽管 SWE-Bench 这类基准提供了有价值的洞察，但我们发现它们无法完全反映真实世界软件工程的微妙之处，尤其是智能体编码工作流中的最终用户体验。

为指导模型训练，我们将这些基准与例行人工评估相结合——由经验丰富的开发者对模型在日常任务上的端到端表现打分。我们还构建了自动化评测来追踪行为的关键方面，帮助我们在设计中权衡取舍。

在开发 `grok-code-fast-1` 时，我们以可用性和用户满意度为核心，以真实世界的人工评估为指引。最终得到的模型被程序员评为日常编码任务中快速而可靠的选择。

## [Grok Code 面向所有人](#grok-code-for-everyone)

限时期间，我们很高兴在独家发布合作伙伴处免费提供 `grok-code-fast-1`。以下是发布合作伙伴对这个模型的评价——它此前曾以代号 `sonic` 悄然发布。

### 限时免费

我们很高兴在独家发布合作伙伴处免费提供 Grok Code Fast 1。

「在早期测试中，Grok Code Fast 在智能体编码任务上展现了速度与质量兼备的实力。用强大的工具赋能开发者是 GitHub Copilot 使命的核心组成部分，这对我们的开发者来说是一个非常有吸引力的新选择。」

[![Mario Rodriguez](/_next/image?url=https%3A%2F%2Fpbs.twimg.com%2Fprofile_images%2F1783313134117376000%2FhWT1AJWp_400x400.jpg&w=64&q=75)

Mario Rodriguez (@mariorod1)

GitHub 首席产品官](https://x.com/mariorod1)

说明

查看说明

[![GitHub Copilot](/_next/static/media/copilot.a16b7bcb.svg)

免费试用

GitHub Copilot](https://github.com/features/copilot)

## [提示词工程指南](#prompt-engineering-guide)

我们的团队编写了一份 [提示词工程指南](https://docs.x.ai/docs/guides/grok-code-prompt-engineering)，教你如何从 `grok-code-fast-1` 获得最佳效果。

该模型现已在 xAI API 上正式可用，定价为每 100 万输入 token 0.20 美元、每 100 万输出 token 1.50 美元、每 100 万缓存输入 token 0.02 美元。

[![xAI 标识](/_next/static/media/xai.985f0fcf.svg)

打开

xAI 云控制台](https://console.x.ai)[![提示词工程指南图标](/_next/static/media/prompt-engineering.fc779cee.svg)

阅读

提示词工程指南](https://docs.x.ai/docs/guides/grok-code-prompt-engineering)

## [未来几周可以期待什么](#what-to-expect-in-the-next-few-weeks)

上周，我们以代号 `sonic` 悄然发布了 `grok-code-fast-1`。在这段隐身期里，我们的团队密切关注社区渠道，并部署了多个新模型检查点以回应反馈。

在推进这个新模型家族的过程中，我们期待基于你的意见快速迭代。我们高度珍视开发者社区的支持，鼓励你自由地 [分享所有反馈](https://discord.gg/x-ai)，无论正面还是负面。

我们将专注于为 `grok-code-fast-1` 持续交付更新，改进以天而非周为单位到来。一个支持多模态输入、并行工具调用和更长上下文的新变体已在训练中。

在 [这里](https://data.x.ai/2025-08-26-grok-code-fast-1-model-card.pdf) 阅读 `grok-code-fast-1` 的模型卡。我们期待看到你的作品！

在以下平台试用 Grok

[Web](https://grok.com)

[iOS](https://apps.apple.com/app/apple-store/id6670324846?pt=126952307&ct=x.ai%20Direct%20Link&mt=8)

[Android](https://play.google.com/store/apps/details?id=ai.x.grok&hl=en)

[X 上的 Grok](https://x.com/i/grok)

产品

[Grok](/grok)

[API](/api)

公司

[公司介绍](/company)

[招聘](/careers)

[联系我们](/contact)

[新闻](/news)

资源

[文档](https://docs.x.ai)

[隐私政策](/privacy-policy)

[安全](/security)

[安全中心](/safety)

[法律](/legal)

[状态](https://status.x.ai)
