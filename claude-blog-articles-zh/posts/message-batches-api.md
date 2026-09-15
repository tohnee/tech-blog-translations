---
title: "推出 Message Batches API"
title_en: "Introducing the Message Batches API"
source: https://claude.com/blog/message-batches-api/
crawled: 2026-09-14
translated: 2026-09-14
---

# 推出 Message Batches API

> 原文：[Introducing the Message Batches API](https://claude.com/blog/message-batches-api/) · Claude 博客

***更新：**Message Batches API 现已在 Anthropic API 上正式发布（Generally Available）。在 Amazon Bedrock 中使用 Claude 的客户可以使用批量推理。批量预测也已在 Google Cloud 的 Vertex AI 上进入预览。（2024 年 12 月 17 日）*

我们推出全新的 [Message Batches API](https://docs.anthropic.com/en/docs/build-with-claude/message-batches)——一种以异步方式处理大规模查询的强大且经济高效的途径。

开发者每个批次最多可发送 10,000 条查询。每个批次都会在 24 小时内处理完毕，价格比标准 API 调用低 50%。这让处理非时间敏感的任务变得更高效、更省成本。

Batches API 今天以公开测试版的形式上线，在 Anthropic API 上支持 Claude 3.5 Sonnet、Claude 3 Opus 和 Claude 3 Haiku。在 Amazon Bedrock 中使用 Claude 的客户可以使用[批量推理](https://docs.aws.amazon.com/bedrock/latest/userguide/batch-inference.html)。[Google Cloud 的 Vertex AI 上的 Claude](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-claude) 对批处理的支持也即将推出。

## 一半的成本，高吞吐量

开发者经常使用 Claude 处理海量数据——从分析客户反馈到语言翻译——这些场景并不需要实时响应。

你无需管理复杂的排队系统，也无需为速率限制操心，只需使用 Batches API 提交最多 10,000 条查询组成的组，让 Anthropic 以五折优惠完成处理。批次会在 24 小时内处理完毕，通常还会快得多。其他好处包括：

- **更高的吞吐量：**享受更高的速率限制，处理大得多的请求量，且不影响你的标准 API 速率限制。
- **面向大数据的可扩展性：**处理数据集分析、大型数据集分类或大规模模型评估等任务，无需为基础设施操心。

Batches API 解锁了此前不太现实或成本过高的全新大规模数据处理可能。例如，分析企业的完整文档库——可能涉及数百万个文件——借助我们的批处理折扣在经济上变得更加可行。

## 定价

Batches API 让你直接受益于基础设施成本节约，输入和输出 token 均享受五折优惠。

| 模型 | 批量输入 | 批量输出 |
|---|---|---|
| **Claude 3.5 Sonnet**<br>我们迄今最智能的模型<br>200K 上下文窗口 | $1.50 / MTok | $7.50 / MTok |
| **Claude 3 Opus**<br>面向复杂任务的强大模型<br>200K 上下文窗口 | $7.50 / MTok | $37.50 / MTok |
| **Claude 3 Haiku**<br>最快、最具性价比的模型<br>200K 上下文窗口 | $0.125 / MTok | $0.625 / MTok |

## 客户聚焦：Quora

[Quora](https://cloud.google.com/customers/quora?hl=en) 是一个用户问答平台，他们利用 Anthropic 的 Batches API 做摘要和要点提取，打造新的终端用户功能。

「Anthropic 的 Batches API 不仅节省成本，还降低了运行大量无需实时处理的查询的复杂度。」Quora 产品经理 Andy Edmonds 说，「提交一个批次并在 24 小时内下载结果非常方便，不用再去应付为了拿到同样结果而运行大量并行实时查询的复杂度。这让我们的工程师可以把时间花在更有意思的问题上。」

## 开始使用

要在 Anthropic API 上开始使用公开测试版的 Batches API，请查阅我们的[文档](https://docs.anthropic.com/en/docs/build-with-claude/message-batches)与[定价页面](https://docs.anthropic.com/en/docs/build-with-claude/message-batches)。

FAQ（常见问题）
