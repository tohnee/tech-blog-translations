---
title: "Anthropic API 上的省 token 更新"
title_en: "Token-saving updates on the Anthropic API"
source: https://claude.com/blog/token-saving-updates/
crawled: 2026-09-14
translated: 2026-09-14
---

# Anthropic API 上的省 token 更新

> 原文：[Token-saving updates on the Anthropic API](https://claude.com/blog/token-saving-updates/) · Claude 博客

我们对 Anthropic API 做出了多项更新，让开发者能够以 Claude 3.7 Sonnet 显著提升吞吐量并减少 token 用量。这些更新包括：缓存感知速率限制、更简单的提示缓存（prompt caching），以及省 token 工具使用（token-efficient tool use）。

这些更新加在一起，能帮助你在既有速率限制内处理更多请求，并以极少的代码改动降低成本。

### 用提示缓存提升吞吐量

[提示缓存（prompt caching）](https://www.anthropic.com/news/prompt-caching)让开发者可以在多次 API 调用之间存储并复用频繁访问的上下文。这让 Claude 无需在每次请求中重复发送同样的信息，就能保持对大型文档、指令或示例的记忆——对长提示而言，成本最高可降低 90%，延迟最高可降低 85%。我们为 Claude 3.7 Sonnet 发布了两项相辅相成的提示缓存改进，帮助你更高效地扩展。

#### 缓存感知速率限制

在 Anthropic API 上，提示缓存读取 token 不再计入 Claude 3.7 Sonnet 的每分钟输入 token 数（ITPM）限制。这意味着你现在可以优化提示缓存的使用来提升吞吐量，从既有的 ITPM 速率限制中获得更多价值。你的每分钟输出 token 数（OTPM）速率限制保持不变。

这让 Claude 3.7 Sonnet 对那些需要大上下文、同时又要求高吞吐量的应用格外强大，例如：

- 需要在上下文中维护大型知识库的文档分析平台
- 需要引用庞大规模代码库的编程助手
- 利用详细产品文档的客户支持系统

[缓存感知 ITPM 限制](https://docs.anthropic.com/en/api/rate-limits#rate-limits)现已在 Anthropic API 上面向 Claude 3.7 Sonnet 提供。

#### 更简单的缓存管理

我们更新了提示缓存，让它更易用。现在，当你设置一个缓存断点时，Claude 会自动从你最长的先前缓存前缀读取。

你不再需要手动跟踪并指定使用哪些缓存段——我们会自动识别并使用最相关的缓存内容。这不仅减轻了你的工作负担，还释放了更多 token。

该功能现已在 Anthropic API 与 Google Cloud 的 Vertex AI 上可用。欢迎查阅我们的[文档](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)了解更多。

### 省 token 工具使用

Claude 已经具备与外部客户端工具和函数交互的能力。本次更新让你可以为 Claude 装备你自己的自定义工具来执行任务——例如从非结构化文本中提取结构化数据，或通过 API 自动化简单任务。Claude 3.7 Sonnet 现已支持[以省 token 的方式调用工具](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/token-efficient-tool-use)，输出 token 消耗最高可减少 70%。早期用户平均看到了 14% 的降幅。

要使用该功能，只需在发给 Claude 3.7 Sonnet 的工具使用请求中添加 beta 头部 *token-efficient-tools-2025-02-19*。如果你在使用 SDK，请确保使用的是带有 *anthropic.beta.messages* 的 beta SDK。

省 token 工具使用目前以 beta 形式在 Anthropic API、Amazon Bedrock 与 Google Cloud 的 Vertex AI 上可用。

#### text_editor 工具

我们还推出了新的 *text_editor* 工具，专为用户与 Claude 协作处理文档的应用而设计。借助这个新工具，Claude 可以对源代码、文档或研究报告中的特定文本片段做有针对性的编辑。这降低了 token 消耗与延迟，同时提升了准确性。

开发者只需在 API 请求中提供该工具并处理工具使用响应，就能在应用中轻松实现它。

*text_editor* 工具现已在 Anthropic API、Amazon Bedrock 与 Google Cloud 的 Vertex AI 上可用。请参阅我们的[文档](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/text-editor-tool)开始使用。

### 客户聚焦：Cognition

Cognition 等早期用户正在利用这些更新来提升 token 效率与响应质量。Cognition 是一家应用 AI 实验室，也是 Devin 的创造者——Devin 是一个协作型 AI 队友，帮助有雄心的工程团队成就更多。

"提示缓存让我们能够提供更多关于代码库的上下文来获得更高质量的结果，同时降低成本与延迟。有了缓存感知 ITPM 限制，我们进一步优化提示缓存的使用，提升吞吐量，从既有速率限制中获得更多价值。"Cognition 联合创始人兼 CEO Scott Wu 表示。

### 立即开始

这些功能今天起面向所有 Anthropic API 客户开放。你可以立即实现它们，代码改动极少：

1. **利用缓存感知速率限制：**在 Claude 3.7 Sonnet 上使用[提示缓存](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)。
2. **实现省 token 工具使用：**在请求中添加 beta 头部 *token-efficient-tools-2025-02-19*，开始节省 token。
3. **试试 *text_editor* 工具：**把它集成到你的应用中，打造更高效的文档编辑工作流。

FAQ（常见问题）
