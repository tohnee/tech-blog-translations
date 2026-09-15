---
title: "在 Claude 中使用提示缓存"
title_en: "Prompt caching with Claude"
source: https://claude.com/blog/prompt-caching/
crawled: 2026-09-14
translated: 2026-09-14
---

# 在 Claude 中使用提示缓存

> 原文：[Prompt caching with Claude](https://claude.com/blog/prompt-caching/) · Claude 博客

***更新**：提示缓存现已在 Anthropic API 正式发布（Generally Available）。提示缓存也在 Amazon Bedrock 和 Google Cloud 的 Vertex AI 上以预览形式提供。（2024 年 12 月 17 日）*提示缓存（prompt caching）让开发者能够在多次 API 调用之间缓存常用的上下文，现已在 Anthropic API 上可用。借助提示缓存，客户可以为 Claude 提供更多背景知识和示例输出——同时把长提示的成本最多降低 90%、延迟最多降低 85%。提示缓存现已针对 Claude 3.5 Sonnet、Claude 3 Opus 和 Claude 3 Haiku 开启公开测试（public beta）。

## 何时使用提示缓存

当你想一次性发送大量提示上下文、然后在后续请求中反复引用这些信息时，提示缓存会很有效，包括：

- **对话式智能体：** 降低长对话的成本和延迟，尤其是带有长指令或上传文档的对话。
- **编码助手：** 在提示中保留代码库的摘要版本，改进自动补全和代码库问答。
- **大型文档处理：** 把包含图片的完整长篇材料纳入提示，而不增加响应延迟。
- **详细指令集：** 分享大量的指令、流程和示例，以微调 Claude 的响应。开发者通常会在提示中放几个示例，但借助提示缓存，放入几十个多样化的高质量输出示例，可以获得更好的效果。
- **智能体搜索与工具使用：** 提升涉及多轮工具调用和迭代修改场景的表现——这类场景的每一步通常都需要一次新的 API 调用。
- **与书籍、论文、文档、播客文字稿及其他长篇内容对话：** 把整份（或多份）文档嵌入提示，让用户直接向它提问，让任何知识库都「活」起来。

早期客户在多种用例中都从提示缓存中获得了显著的速度和成本改进——从纳入完整知识库、100 个示例（100-shot），到把对话的每一轮都放进提示。

提示缓存（Prompt caching）

| 用例 | 无缓存延迟（首 token 时间） | 有缓存延迟（首 token 时间） | 成本降幅 |
|---|---|---|---|
| 与一本书对话（100,000 token 缓存提示）[1] | 11.5s | 2.4s（-79%） | -90% |
| 多示例提示（10,000 token 提示）[1] | 1.6s | 1.1s（-31%） | -86% |
| 多轮对话（带长系统提示的 10 轮对话）[2] | ~10s | ~2.5s（-75%） | -53% |

### 缓存提示如何计价

缓存提示按你缓存的输入 token 数量以及使用这些内容的频率计价。对任何给定模型，写入缓存的费用比基础输入 token 价格高 25%，而使用缓存内容则便宜得多，只需基础输入 token 价格的 10%。

定价

| 模型 | 输入 | 提示缓存 | 输出 |
|---|---|---|---|
| **Claude 3.5 Sonnet**（迄今最智能的模型，200K 上下文窗口） | $3 / MTok | 写入缓存 $3.75 / MTok · 读取缓存 $0.30 / MTok | $15 / MTok |
| **Claude 3 Opus**（应对复杂任务的强大模型，200K 上下文窗口） | $15 / MTok | 写入缓存 $18.75 / MTok · 读取缓存 $1.50 / MTok | $75 / MTok |
| **Claude 3 Haiku**（最快、最具性价比的模型，200K 上下文窗口） | $0.25 / MTok | 写入缓存 $0.30 / MTok · 读取缓存 $0.03 / MTok | $1.25 / MTok |

### 客户聚焦：Notion

[Notion](https://www.notion.so/product/ai) 正在为其 AI 助手 Notion AI 的 Claude 驱动功能接入提示缓存。得益于更低的成本和更快的速度，Notion 得以优化内部运营，并为客户打造更精致、响应更迅捷的用户体验。

> 我们很高兴使用提示缓存让 Notion AI 更快、更便宜，同时保持最先进的品质。

— Notion 联合创始人 Simon Last

### 开始使用

要开始在 Anthropic API 上使用提示缓存公开测试版，请查阅我们的[文档](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)和[定价页面](https://www.anthropic.com/pricing#anthropic-api)。

FAQ（常见问题）
