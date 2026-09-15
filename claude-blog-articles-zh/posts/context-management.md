---
title: "在 Claude Developer Platform 上管理上下文"
title_en: "Managing context on the Claude Developer Platform"
source: https://claude.com/blog/context-management/
crawled: 2026-09-14
translated: 2026-09-14
---

# 在 Claude Developer Platform 上管理上下文

> 原文：[Managing context on the Claude Developer Platform](https://claude.com/blog/context-management/) · Claude 博客

今天，我们在 Claude Developer Platform 上推出两项管理智能体上下文的新能力：上下文编辑（context editing）与记忆工具（memory tool）。

结合我们最新的模型 [Claude Sonnet 4.5](https://www.anthropic.com/news/claude-sonnet-4-5)，这些能力让开发者能够构建胜任长时间运行任务的 AI 智能体：性能更高，不会撞上上下文限制，也不会丢失关键信息。

## 上下文窗口有上限，但真实工作没有

随着生产级智能体处理更复杂的任务、生成更多的工具结果，它们常常耗尽自己的有效上下文窗口——让开发者陷入两难：要么删减智能体的对话记录，要么接受性能下降。上下文管理从两个方面解决这一问题，帮助开发者确保只有相关数据留在上下文中，同时让有价值的洞见跨会话得到保存。

**上下文编辑（context editing）**会在接近 token 上限时，自动从上下文窗口内清除过时的工具调用与结果。随着智能体执行任务、累积工具结果，上下文编辑在保持对话流完整的同时移除过时内容，有效延长智能体无需人工干预即可持续运行的时间。由于 Claude 只关注相关的上下文，这也会提升模型的有效性能。

**记忆工具（memory tool）**让 Claude 能够通过一个基于文件的系统，在上下文窗口之外存储与查阅信息。Claude 可以在一个专用的记忆目录中创建、读取、更新和删除文件；该目录存储在你的基础设施中，并跨对话持久保存。这使智能体能够随时间积累知识库、跨会话维护项目状态、引用以往学到的经验，而不必把所有内容都留在上下文里。

记忆工具完全通过工具调用在客户端一侧运行。开发者管理存储后端，从而完全掌控数据存储在哪里、以何种方式持久化。

Claude Sonnet 4.5 以内置的上下文感知能力强化了这两项功能——在整个对话过程中追踪可用 token，以更有效地管理上下文。

这些更新合在一起，构成了一套提升智能体性能的系统：

- 通过自动从上下文中移除过时的工具结果，支持更长的对话
- 把关键信息存入记忆以提升准确性——并让这些经验延续到后续的多轮智能体会话

## 构建长时间运行的智能体

Claude Sonnet 4.5 是构建智能体的世界最佳模型。这些功能为长时间运行的智能体解锁了新的可能——处理整个代码库、分析数百份文档，或维护庞大的工具交互历史。上下文管理在这一基础之上，确保智能体高效利用这一扩展后的容量，同时仍能处理超出任何固定上限的工作流。使用场景包括：

- **编码：**上下文编辑清除旧的文件读取与测试结果，而记忆保存调试洞见与架构决策，让智能体在大型代码库上工作而不丢失进度。
- **研究：**记忆保存关键发现，上下文编辑移除旧的搜索结果，构建随时间推移不断改进性能的知识库。
- **数据处理：**智能体把中间结果存入记忆，上下文编辑清除原始数据，从而处理原本会超出 token 上限的工作流。

## 上下文管理带来的性能提升

在一个面向智能体搜索（agentic search）的内部评估集上，我们测试了上下文管理如何提升智能体在复杂多步骤任务上的表现。结果显示出显著增益：把记忆工具与上下文编辑相结合，比基线提升了 39%；仅用上下文编辑也带来了 29% 的提升。

在一项 100 轮的网页搜索评估中，上下文编辑让智能体得以完成原本会因上下文耗尽而失败的工作流——同时把 token 消耗降低了 84%。

## 开始使用

这些能力今天起已在 Claude Developer Platform 上进入公测，包括原生提供，以及在 Amazon Bedrock 和 Google Cloud 的 Vertex AI 上提供。探索[上下文编辑](https://docs.claude.com/en/docs/build-with-claude/context-editing)与[记忆工具](https://docs.claude.com/en/docs/agents-and-tools/tool-use/memory-tool)的文档，或访问我们的 [cookbook](https://platform.claude.com/cookbook/tool-use-memory-cookbook) 了解更多。

*Anthropic 与 CATAN GmbH 或 CATAN Studio 无任何隶属、背书或赞助关系。CATAN 商标与游戏为 CATAN GmbH 所有。*

FAQ（常见问题）
