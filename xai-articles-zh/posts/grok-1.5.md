---
title: "Grok-1.5 发布"
title_en: "Announcing Grok-1.5"
date: 2025-03-11
source: https://x.ai/news/grok-1.5
crawled: 2026-09-22
translated: 2026-09-22
---

# Grok-1.5 发布

> 原文：[Announcing Grok-1.5](https://x.ai/news/grok-1.5) · xAI

2024 年 3 月 28 日

Grok-1.5 带来了更强的推理能力和 128,000 token 的上下文长度。即将在 𝕏 上推出。

---

**介绍 Grok-1.5，我们最新的模型，具备长上下文理解和高级推理能力。Grok-1.5 将在未来几天向我们的早期测试者和 𝕏 平台上的现有 Grok 用户开放。**

两周前我们发布了 Grok-1 的模型权重和网络架构，展示了 xAI 截至去年 11 月取得的进展。此后，我们在最新模型 Grok-1.5 中改进了推理和解决问题的能力。

## 能力与推理

Grok-1.5 最显著的改进之一是它在编码和数学相关任务上的表现。在我们的测试中，Grok-1.5 在 MATH 基准上取得 50.6% 的分数，在 GSM8K 基准上取得 90% 的分数——这两个数学基准涵盖了从小学到高中竞赛的广泛题目。此外，它在评估代码生成和解决问题能力的 HumanEval 基准上得分 74.1%。

| 基准 | Grok-1 | **Grok-1.5** | Mistral Large | Claude 2 | Claude 3 Sonnet | Gemini Pro 1.5 | GPT-4 | Claude 3 Opus |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MMLU | 73% 5-shot | 81.3% 5-shot | 81.2% 5-shot | 75% 5-shot | 79% 5-shot | 83.7% 5-shot | 86.4% 5-shot | 86.8 5-shot |
| MATH | 23.9% 4-shot | 50.6% 4-shot | — | — | 40.5% 4-shot | 58.5% 4-shot | 52.9% 4-shot | 61% 4-shot |
| GSM8K | 62.9 8-shot | 90% 8-shot | 81% 5-shot | 88% 0-shot CoT | 92.3% 0-shot CoT | 91.7% 11-shot | 92% 5-shot | 95% 0-shot CoT |
| HumanEval | 63.2% 0-shot | 74.1% 0-shot | 45.1% 0-shot | 70% 0-shot | 73% 0-shot | 71.9% 0-shot | 67% 0-shot | 84.9% 0-shot |

## 长上下文理解

Grok-1.5 的一项新特性是能够在上下文窗口内处理长达 128K token 的长上下文。这使 Grok 的记忆容量最高提升至此前上下文长度的 16 倍，能够利用长得多的文档中的信息。

![图中展示了一张可视化模型从其上下文窗口中回忆信息能力的图表。横轴为上下文窗口长度，纵轴为待检索信息在窗口中的相对位置。我们用颜色标记召回率。整张图都是绿色的，意味着对每个上下文窗口长度和每个信息位置，召回率都是 100%。](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fcontext.f27d1f23.webp&w=1920&q=75)

此外，该模型能够处理更长、更复杂的提示词，同时随着上下文窗口扩大仍保持指令遵循能力。在大海捞针（Needle In A Haystack，NIAH）评测中，Grok-1.5 在长达 128K token 的上下文中对嵌入文本展现了强大的检索能力，取得了完美的检索结果。

## Grok-1.5 基础设施

在超大规模 GPU 集群上运行的尖端大语言模型（LLM）研究，需要健壮而灵活的基础设施。Grok-1.5 构建在基于 JAX、Rust 和 Kubernetes 的自定义分布式训练框架之上。这套训练技术栈使我们的团队能够以极小的代价进行原型验证并大规模训练新架构。在大型算力集群上训练 LLM 的一大挑战是最大化训练任务的可靠性和正常运行时间。我们自研的训练编排器能自动检测故障节点并将其从训练任务中剔除。我们还优化了检查点、数据加载和训练任务重启，以将故障发生时的停机时间降到最低。如果你觉得参与我们的训练技术栈开发很有意思，欢迎[申请加入团队](https://x.ai/careers)。

## 展望

Grok-1.5 很快将向早期测试者开放，我们期待收到你的反馈来帮助改进 Grok。随着我们逐步向更广泛的用户推出 Grok-1.5，我们很高兴在未来几天内推出若干新功能。

*注意：GPT-4 的分数取自 2023 年 3 月发布版。MATH 和 GSM8K 我们给出的是 maj@1 结果；HumanEval 报告的是 pass@1 基准分数。*

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
