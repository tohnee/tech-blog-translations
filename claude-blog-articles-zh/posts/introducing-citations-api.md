---
title: "在 Anthropic API 上推出 Citations"
title_en: "Introducing Citations on the Anthropic API"
source: https://claude.com/blog/introducing-citations-api/
crawled: 2026-09-14
translated: 2026-09-14
---

# 在 Anthropic API 上推出 Citations

> 原文：[Introducing Citations on the Anthropic API](https://claude.com/blog/introducing-citations-api/) · Claude 博客

***更新：现已登陆 Amazon Bedrock。（2025 年 6 月 30 日）***

今天，我们推出 Citations——一项新的 API 功能，让 Claude 把回答锚定在源文档之上。Claude 现在可以为生成回答时所使用的确切句子和段落提供详细引用，从而带来更可验证、更值得信赖的输出。

Citations 已在 Anthropic API 和 Google Cloud 的 Vertex AI 上正式发布（generally available）。

### 通过验证建立信任

所有 Claude 模型在训练时就以值得信赖、易于引导（steerable）为设计目标。Citations 在这一基础之上，回应了 AI 应用中的一个具体需求：核实 AI 生成回答背后的来源。

过去，开发者依赖复杂的提示来指示 Claude 附上来源信息，效果往往不稳定，还要在提示工程和测试上投入大量时间。有了 Citations，用户现在可以把源文档加入上下文窗口；在查询模型时，Claude 会自动在其输出中为那些从这些来源推断出的论断标注引用。

**我们的内部评估显示，Claude 内置的引用能力优于大多数自定义实现，召回准确率最高可提升 15%。¹**

### 使用场景

借助 Citations，开发者可以打造具有更强可追责性的 AI 解决方案，适用于以下场景：

- 文档摘要：为案卷等长文档生成简明摘要，每个要点都可回溯到其原始出处。
- 复杂问答：跨财务报表等大规模文档语料回答用户提问，回答中的每个元素都能追溯到相关文本的具体章节。
- 客户支持：构建能够引用多份产品手册、FAQ 和支持工单来回答复杂查询的支持系统，并始终注明信息的准确出处。

### 工作原理

启用 Citations 后，API 会把用户提供的源文档（PDF 文档和纯文本文件）按句子分块（chunking）。这些分块后的句子连同用户提供的上下文，会随用户的查询一起传给模型。用户也可以为源文档自行提供分块。

Claude 分析查询，并基于所提供的分块与上下文，为任何源自源材料的论断生成带有精确引用的回答。被引用的文本会指向源文档，以尽量减少幻觉。

这种方式具备出色的灵活性与易用性：无需文件存储，并能与 Messages API 无缝集成。

### 定价

Citations 采用我们标准的按 token 计价模式。虽然处理文档可能消耗额外的输入 token，但返回引用文本本身的输出 token 不向用户收费。

### 客户聚焦：Thomson Reuters

Thomson Reuters 使用 Claude 驱动其 AI 平台 CoCounsel，帮助法律与税务专业人士整合专家知识，为客户提供全面的建议。

「要让 CoCounsel 获得执业律师的信任并能即拿即用，它必须为自己的结论给出引用。我们最初自己做了一套，但构建和维护都非常困难。正因如此，我们很高兴能测试 Anthropic 的 Citations 功能。它让引用一手来源并建立链接，在构建、维护和向用户部署上都容易得多。这项能力不仅有助于把幻觉风险降到最低，也增强了人们对 AI 生成内容的信任。Citations 功能将帮助我们为律师打造更精确、更周密的 AI 助手。」Thomson Reuters CoCounsel 产品负责人 Jake Heller 表示。

### 客户聚焦：Endex

Endex 使用 Claude 为金融公司驱动一款自主智能体（Autonomous Agent）。

「借助 Anthropic 的 Citations，我们把来源幻觉和格式问题从 10% 降到了 0%，每次回答的引用数量提升了 20%。这让我们无需再围绕引用做精细的提示工程，也提高了我们开展复杂多阶段金融研究时的准确性。」Endex 首席执行官 Tarun Amasa 表示。

### 开始使用

Citations 现已在新的 Claude 3.5 Sonnet 和 Claude 3.5 Haiku 上可用。要开始使用 Citations，请查阅我们的[文档](https://docs.anthropic.com/en/docs/build-with-claude/citations)。

FAQ（常见问题）
