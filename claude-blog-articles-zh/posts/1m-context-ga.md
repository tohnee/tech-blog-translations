---
title: "1M 上下文现已在 Opus 4.6 和 Sonnet 4.6 上正式发布"
title_en: "1M context is now generally available for Opus 4.6 and Sonnet 4.6"
source: https://claude.com/blog/1m-context-ga/
crawled: 2026-09-14
translated: 2026-09-14
---

# 1M 上下文现已在 Opus 4.6 和 Sonnet 4.6 上正式发布

> 原文：[1M context is now generally available for Opus 4.6 and Sonnet 4.6](https://claude.com/blog/1m-context-ga/) · Claude 博客

Claude Opus 4.6 和 Sonnet 4.6 现已在 Claude Platform 上以标准定价提供完整的 1M 上下文窗口。标准定价适用于整个窗口——Opus 4.6 为每百万 token $5/$25，Sonnet 4.6 为 $3/$15。没有价格乘数：一个 900K token 的请求与一个 9K token 的请求按相同的单价计费。

**正式发布带来了哪些新变化：**

- **一个价格，完整上下文窗口。** 没有长上下文溢价。
- **任意上下文长度都享受完整的速率限制。** 你账户的标准吞吐量适用于整个窗口。
- **每个请求可承载 6 倍的媒体内容。** 最多 600 张图片或 PDF 页面，此前为 100。现已登陆 Claude Platform 原生服务、Microsoft Foundry 和 Google Cloud 的 Vertex AI。
- **无需 beta 请求头。** 超过 200K token 的请求自动生效。如果你已经在发送 beta 请求头，它会被忽略，因此无需修改任何代码。

**1M 上下文现已随 Opus 4.6 纳入面向 Max、Team 和 Enterprise 用户的 Claude Code。** Opus 4.6 会话可以自动使用完整的 1M 上下文窗口，这意味着更少的上下文压缩（compaction）、更多对话内容得以完整保留。此前使用 1M 上下文需要额外消耗用量。

### **经得起考验的长上下文**

一百万 token 的上下文只有在模型能够召回正确细节并据此进行推理时才有意义。Opus 4.6 在 MRCR v2 上得分 78.3%，是同等上下文长度下前沿模型中的最高分。

Claude Opus 4.6 和 Sonnet 4.6 在完整的 1M 窗口内保持准确率。每一代模型的长上下文检索能力都在提升。

这意味着你可以加载整个代码库、数千页的合同，或一个长时间运行智能体的完整轨迹——工具调用、观察结果、中间推理——并直接加以使用。此前长上下文工作所需的工程改造、有损摘要和上下文清理都不再必要。完整的对话保持原封不动。

> Claude Code 在搜索 Datadog、Braintrust、数据库和源码时可能烧掉 100K+ token。然后上下文压缩启动。细节消失。你陷入循环调试。有了 1M 上下文，我可以在同一个窗口里搜索、反复搜索、汇总边缘情况并提出修复方案。

> 在 Opus 4.6 的 1M 上下文窗口出现之前，用户一旦加载大型 PDF、数据集或图片，我们就不得不立即压缩上下文——恰恰在最关键的工作上损失保真度。我们的上下文压缩事件减少了 15%。现在我们的智能体能全部记住，连续运行数小时也不会忘记第一页读了什么。

> Opus 4.6 的 1M 上下文窗口让我们的 Devin Review 智能体显著更加高效。大型 diff 装不进 200K 上下文窗口，智能体只能对上下文分块，导致更多轮次和跨文件依赖的丢失。有了 1M 上下文，我们把完整 diff 直接喂进去，用更简单、更省 token 的执行框架（harness）就能得到更高质量的评审。

> Eve 默认启用 1M 上下文，因为原告律师最棘手的问题需要它。无论是交叉引用一份 400 页的庭外取证笔录，还是在整个案卷中挖掘关键关联，扩展后的上下文窗口让我们能够给出比以往质量高得多的答案。

> 科学发现需要同时跨越研究文献、数学框架、数据库和仿真代码进行推理。Claude Opus 4.6 的 1M 上下文和扩大的媒体限制让我们的智能体系统能够一次性综合数百篇论文、证明和代码库，帮助我们大幅加速基础与应用物理研究。

> 有了 Claude 的 1M 上下文，一名内部律师可以把一份 100 页合伙协议的五轮谈判放进同一个会话，终于能看到整场谈判的全貌。不必再在不同版本之间来回切换，也不会弄丢三轮之前改了什么。

> 大规模生产系统有着无尽的上下文，生产事故也可能变得极其复杂。借助 Claude 的 1M 上下文窗口，从第一次告警到修复完成，我们能够始终掌握每一个实体、每一个信号和每一个工作假设，而无需反复压缩上下文，也不必牺牲对这些系统细微之处的把握。

> 我们把 Opus 的上下文窗口从 200k 提升到 500k，智能体的运行效率反而更高了——整体消耗的 token 其实更少。开销更少，更专注于手头的目标。

> 真实世界的电子表格任务需要深入研究和复杂的多步骤规划。Claude 的 1M 上下文窗口让我们得以保持任务一致性以及对细节的关注。

### **开始使用**

1M 上下文现已在 Claude Platform 原生可用，并可通过 Amazon Bedrock、Google Cloud 的 Vertex AI 和 Microsoft Foundry 使用。在 Opus 4.6 上使用 Claude Code 的 Max、Team 和 Enterprise 用户将自动默认获得 1M 上下文。

详情请参阅我们的[文档](https://platform.claude.com/docs/en/build-with-claude/context-windows)与[定价](https://platform.claude.com/docs/en/about-claude/pricing)。

FAQ（常见问题）
