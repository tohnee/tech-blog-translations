---
title: "完整的 Claude Platform 现已登陆 Google Cloud"
title_en: "The full Claude Platform, available on Google Cloud"
date: 2026-10-22
source: https://claude.com/resources/articles/claude-models-on-google-cloud-anthropic-managed
crawled: 2026-11-17
translated: 2026-11-17
---

# 完整的 Claude Platform 现已登陆 Google Cloud

> 原文：[The full Claude Platform, available on Google Cloud](https://claude.com/resources/articles/claude-models-on-google-cloud-anthropic-managed) · Claude 博客

*使用 Claude Models on Google Cloud（Anthropic 托管版），即可借助 Google Cloud 的身份认证、计费和承诺用量抵扣，使用 Claude Platform 的各项功能。*

Claude Models on Google Cloud（Anthropic 托管版）现已正式可用，为 Google Cloud 客户提供完整的 Claude Platform 功能，并支持 Google Cloud IAM 凭证、计费和承诺用量抵扣。Claude 也继续通过 Google 托管版提供，在该版本中 Google 是数据处理方。

## 在 Google Cloud 上访问完整的 Claude Platform

借助 Anthropic 托管版，Google Cloud 客户现在可以获得 Claude API 的全部功能，新功能和测试版会在原生 Claude Platform 上线的同一天推出。

Anthropic 托管版可与现有的 Google Cloud IAM 凭证配合使用，因此团队可以继续留在他们已经管理的工具和权限体系中。计费通过一张 Google Cloud 发票完成，Claude 用量会抵扣你现有的 Google Cloud 承诺用量。

Claude Models on Google Cloud（Anthropic 托管版）目前提供美国端点与全球端点。

![Abacus.AI](https://assets.claude.com/3000fcaf4ad00ac2cc4096d3f5aa236cc9eb415d.png)

> “借助 Anthropic 托管版，我们获得了原生 Claude API，同时以 Google Cloud 作为访问层。第一天就能用上新功能很重要。我们为企业构建 AI 智能体和助手，需要迅速把 Claude 的新能力引入产品。沿用现有的 IAM 设置，并且知道用量会计入我们的 Google Cloud 承诺用量，这让我们的团队很容易做出决定。”

Arvind Sundararajan，首席技术官

![Triple Whale](https://assets.claude.com/3720f77d05a852bc6857ae3eca424467270055b6.png)

> “我们面向电商品牌的 AI harness Moby 运行在 Claude 上。借助 Anthropic 托管版，我们能在 Google Cloud 上、基于团队已经在用的同一套 Claude API 运行 Moby。提示缓存是我们以低成本大规模运行 Moby 的核心，而在通过 Google Cloud 进行计费和访问管理的同时，我们保留了这项能力。”

Maksim Gorev，AI 工程负责人

## 包含哪些功能

使用 Anthropic 托管版的 Google Cloud 客户可以获得完整的 Claude Platform 功能，从而能够：

**构建和部署智能体：**

* [Claude Managed Agents（测试版）（在新标签页中打开）](https://platform.claude.com/docs/en/managed-agents/overview)，用于驱动长时间运行的智能体，而无需管理基础设施
* [代码执行（在新标签页中打开）](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool)，可在一次 API 调用中运行 Python 代码、创建可视化并分析数据
* [计算机使用（在新标签页中打开）](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)，让 Claude 操作浏览器或桌面以完成任务
* [智能体技能（在新标签页中打开）](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)，把可重复的工作流教给 Claude，使其交付一致的结果
* [顾问策略（测试版）（在新标签页中打开）](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool)，通过咨询顾问模型为智能体注入智力增益

**连接系统与知识：**

* [Files API（在新标签页中打开）](https://platform.claude.com/docs/en/build-with-claude/files)，用于上传文档并在多轮对话中引用
* [引用（在新标签页中打开）](https://platform.claude.com/docs/en/build-with-claude/citations)，让回答扎根于源文档
* [网络搜索（在新标签页中打开）](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool)与[网页抓取（在新标签页中打开）](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool)，用来自整个网络的实时真实数据扩充 Claude 的知识
* [MCP 连接器（测试版）（在新标签页中打开）](https://platform.claude.com/docs/en/agents-and-tools/mcp-connector)，无需编写客户端代码即可把 Claude 连接到其他工具

**管理成本与性能：**

* [提示缓存（在新标签页中打开）](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)，降低重复上下文的成本和延迟
* [批处理（在新标签页中打开）](https://platform.claude.com/docs/en/build-with-claude/batch-processing)，用于高并发的异步工作负载

Claude Opus 5.5 上的 Fast Mode 也已对使用 Claude Models on Google Cloud（Anthropic 托管版）的客户正式可用。Fast Mode 以速度为优先，输出 token 生成速度最高提升至 2.5 倍，适用于快速迭代、实时调试，以及输出速度直接影响用户体验的交互式智能体。输入和输出 token 价格分别为每百万 8 美元和 40 美元。

在[文档（在新标签页中打开）](https://platform.claude.com/docs/en/build-with-claude/claude-models-on-google-cloud/anthropic-managed)中查看 Claude Models on Google Cloud 支持的完整功能列表。

使用 Anthropic 托管版的客户还可访问 Claude Console——Anthropic 用于观察和管理 Claude 智能体的开发环境。Console 包含用于编写提示词和配置智能体的工具，可以在托管环境中运行智能体、监控用量与成本，并按工作区管理访问权限与安全设置。

Claude Fable 5.1、Opus 5.5、Sonnet 5.5 和 Haiku 5.5 均已提供，新模型发布时也会同步在 Anthropic 托管版上线。

## 在 Claude 上构建的两条路径

在 Google Cloud 上使用 Claude 有两种方式。

**Claude Models on Google Cloud（Anthropic 托管版）**面向希望在上线首日就能使用 Claude Platform 所有测试版和正式版功能的客户。它最适合那些想要通过 Google Cloud 获得与 Claude Platform 完全一致功能集的客户。该服务由 Anthropic 运营，并由 Anthropic 担任数据处理方。

**Claude Models on Google Cloud（Google 托管版）**仍然是需要 Google Cloud 作为数据处理方、有严格的区域数据驻留要求，或希望使用 Model Armor、Agent Engine 等原生 Google Cloud 集成的客户的最佳选择。

## 开始使用

Anthropic 托管版现已正式可用。要开始使用，请打开 [Claude Models on Google Cloud（Anthropic 托管版）（在新标签页中打开）](https://console.cloud.google.com/marketplace/product/anthropic/anthropic-managed-claude)，或查阅[文档（在新标签页中打开）](https://platform.claude.com/docs/en/build-with-claude/claude-models-on-google-cloud/anthropic-managed)。

如果你已有折扣，请在开始使用 Anthropic 托管版之前联系你的 Anthropic 或 Google Cloud 客户经理，以确保折扣被正确应用。折扣无法追溯适用于此前的用量。
