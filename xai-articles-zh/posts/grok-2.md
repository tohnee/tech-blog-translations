---
title: "Grok-2 Beta 发布"
title_en: "Grok-2 Beta Release"
date: 2025-03-12
source: https://x.ai/news/grok-2
crawled: 2026-09-22
translated: 2026-09-22
---

# Grok-2 Beta 发布

> 原文：[Grok-2 Beta Release](https://x.ai/news/grok-2) · xAI

2024 年 8 月 13 日

我们发布新的 Grok-2 和 Grok-2 mini 模型。

---

**我们很高兴发布 Grok-2 的早期预览版——相比之前的 Grok-1.5 迈出了重要一步，在聊天、编码和推理方面具备前沿能力。同时，我们推出 Grok-2 mini，一个虽小但能力出众的 Grok-2 姊妹模型。Grok-2 的一个早期版本曾以 "sus-column-r" 的名字在 LMSYS 排行榜上测试。截至本文撰写时，它的表现优于 Claude 3.5 Sonnet 和 GPT-4-Turbo。**

Grok-2 和 Grok-2 mini 目前正在 𝕏 上进行 beta 测试，我们也将于本月晚些时候通过企业 API 提供这两个模型。

### Grok-2 语言模型与聊天能力

我们曾以 "sus-column-r" 的名义把 Grok-2 的一个早期版本引入 <LMArena.ai> Chatbot Arena——一个流行的竞技式语言模型基准。就 LMSYS 排行榜上的总体 Elo 分数而言，它优于 Claude 和 GPT-4。

![Chatbot Arena 总体 ELO 分数](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fgraph1.65dddae1.webp&w=3840&q=75)

Chatbot Arena 总体 ELO 分数

![Grok-2 在 Chatbot Arena 上对阵各竞品的胜率](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fgraph2.505c7065.webp&w=3840&q=75)

Grok-2 在 Chatbot Arena 上对阵各竞品的胜率

![Grok 的回答质量](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fgraph3.45250b6d.webp&w=1920&q=75)

Grok 的回答质量

在内部，我们采用类似的流程来评测模型。我们的 AI 导师会在多种反映与 Grok 真实交互的任务上与模型对话。每次交互中，AI 导师会看到 Grok 生成的两个回答，并按照指南中列出的特定标准选出更好的一个。我们重点评测模型在两个关键领域的能力：遵循指令，以及提供准确、符合事实的信息。Grok-2 在结合检索内容进行推理以及工具使用能力上有显著提升，例如正确识别缺失信息、梳理事件序列、剔除无关帖子。

## 基准测试

我们在一系列学术基准上评测了 Grok-2 系列模型，涵盖推理、阅读理解、数学、科学和编码。Grok-2 和 Grok-2 mini 相较之前的 Grok-1.5 都有显著提升。它们在研究生级科学知识（GPQA）、通识知识（MMLU、MMLU-Pro）和数学竞赛题（MATH）等领域达到了与其他前沿模型相当的水平。此外，Grok-2 在视觉任务上表现出色，在视觉数学推理（MathVista）和文档问答（DocVQA）上取得了最先进的成绩。

| 基准 |  | Grok-1.5 | Grok-2 mini‡ | Grok-2‡ | GPT-4 Turbo* | Claude 3 Opus† | Gemini Pro 1.5 | Llama 3 405B | GPT-4o* | Claude 3.5 Sonnet† |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GPQA |  | 35.9% | 51.0% | 56.0% | 48.0% | 50.4% | 46.2% | 51.1% | 53.6% | 59.6% |
| MMLU |  | 81.3% | 86.2% | 87.5% | 86.5% | 85.7% | 85.9% | 88.6% | 88.7% | 88.3% |
| MMLU-Pro |  | 51.0% | 72.0% | 75.5% | 63.7% | 68.5% | 69.0% | 73.3% | 72.6% | 76.1% |
| MATH§ |  | 50.6% | 73.0% | 76.1% | 72.6% | 60.1% | 67.7% | 73.8% | 76.6% | 71.1% |
| HumanEval¶ |  | 74.1% | 85.7% | 88.4% | 87.1% | 84.9% | 71.9% | 89.0% | 90.2% | 92.0% |
| MMMU |  | 53.6% | 63.2% | 66.1% | 63.1% | 59.4% | 62.2% | 64.5% | 69.1% | 68.3% |
| MathVista |  | 52.8% | 68.1% | 69.0% | 58.1% | 50.5% | 63.9% | — | 63.8% | 67.7% |
| DocVQA |  | 85.6% | 93.2% | 93.6% | 87.2% | 89.3% | 93.1% | 92.2% | 92.8% | 95.2% |

* GPT-4-Turbo 和 GPT-4o 的分数取自 2024 年 5 月发布版。
† Claude 3 Opus 和 Claude 3.5 Sonnet 的分数取自 2024 年 6 月发布版。
‡ Grok-2 的 MMLU、MMLU-Pro、MMMU 和 MathVista 使用 0-shot CoT 评测。
§ MATH 我们给出的是 maj@1 结果。
¶ HumanEval 报告的是 pass@1 基准分数。

## 在 𝕏 上体验带实时信息的 Grok

过去几个月，我们持续改进 𝕏 平台上的 Grok。今天，我们推出 Grok 体验的下一次进化，带来重新设计的界面和新功能。

![X App 中带 Grok mini 的 Grok 页面](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fscreenshot1.f6bbecbb.webp&w=3840&q=75)

X App 中带 Grok mini 的 Grok 页面

![一张梗图照片及 Grok 的解释](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fscreenshot2.3dbfd251.webp&w=3840&q=75)

一张梗图照片及 Grok 的解释

![Grok 对一个编码问题的回答](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fscreenshot3.87a10c64.webp&w=3840&q=75)

Grok 对一个编码问题的回答

![Black Forest Labs 徽标。](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fflux-logo.b6457dc7.webp&w=256&q=75)

𝕏 Premium 和 Premium+ 用户可以使用两个新模型：Grok-2 和 Grok-2 mini。Grok-2 是我们最先进的 AI 助手，在文本和视觉理解方面都具备先进能力，整合了 𝕏 平台的实时信息，可通过 𝕏 App 中的 Grok 标签页使用。Grok-2 mini 是我们小而能干的模型，在速度和回答质量之间取得平衡。与前代相比，Grok-2 在各类任务中更直觉、更可控、更多才多艺，无论你是寻求答案、协作写作还是解决编码任务。我们还与 [Black Forest Labs](https://blackforestlabs.ai/) 合作，试验他们的 [FLUX.1](https://blackforestlabs.ai/#get-flux) 模型，以扩展 Grok 在 𝕏 上的能力。如果你是 Premium 或 Premium+ 订阅用户，请务必更新到最新版 𝕏 App 以参与 Grok-2 的 beta 测试。

### 用企业 API 基于 Grok 构建

我们也将于本月晚些时候通过新的企业 API 平台向开发者发布 Grok-2 和 Grok-2 mini。我们即将推出的 API 构建在全新定制的技术栈之上，支持多区域推理部署，在全球范围提供低延迟访问。我们提供增强的安全特性，例如强制多因素认证（如使用 Yubikey、Apple TouchID 或 TOTP）、丰富的流量统计，以及高级计费分析（包括详细数据导出）。我们进一步提供管理 API，让你可以把团队、用户和账单管理集成到你现有的内部工具与服务中。[订阅我们的邮件通讯](/api)，即可在本月晚些时候上线时收到通知。

### 接下来是什么？

Grok-2 和 Grok-2 mini 正在 𝕏 上陆续推出。我们非常期待它们在一系列 AI 驱动功能中的应用，例如增强的搜索能力、对 𝕏 帖子的更深洞察，以及改进的回复功能——全部由 Grok 驱动。很快，我们将发布多模态理解的预览版，作为 𝕏 和 API 上 Grok 体验的核心部分。

自 2023 年 11 月发布 Grok-1 以来，xAI 以惊人的速度前进，这得益于一支人才密度极高的小团队。我们推出了 Grok-2，站到了 AI 开发的前沿。我们的重点是在新的算力集群上推进核心推理能力。未来几个月我们将有更多进展可以分享。我们正在寻找加入这支小而专注团队的人，共同为人类的未来打造最具影响力的创新。[在此申请我们的职位](https://x.ai/careers)。

在以下平台试用 Grok

[网页](https://grok.com)

[iOS](https://apps.apple.com/app/grok/id6670324846)

[Android](https://play.google.com/store/apps/details?id=ai.x.grok&hl=en)

[Grok on X](https://x.com/i/grok)

产品

[Grok](/grok)

[API](/api)

公司

[公司简介](/company)

[招聘](/careers)

[联系我们](/contact)

[新闻](/news)

资源

[状态](https://status.x.ai)

[隐私政策](/privacy-policy)

[安全](/security)

[法律](/legal)
