---
title: "Anthropic API 现已推出网页搜索"
title_en: "Introducing web search on the Anthropic API"
source: https://claude.com/blog/web-search-api/
crawled: 2026-09-14
translated: 2026-09-14
---

# Anthropic API 现已推出网页搜索

> 原文：[Introducing web search on the Anthropic API](https://claude.com/blog/web-search-api/) · Claude 博客

***更新：****你现在可以在请求中添加 web fetch 工具，Claude 将获取并分析任意网页 URL 的内容。（2025 年 9 月 10 日）*

今天，我们在 Anthropic API 上推出网页搜索（web search）——这是一个让 Claude 访问全网最新信息的新工具。启用网页搜索后，开发者可以构建由 Claude 驱动、能够提供最新洞察的应用和智能体。

### 用来自网络的最新信息为 AI 智能体赋能

开发者现在可以在向 Messages API 发起请求时启用网页搜索工具，用最新的现实世界数据增补 Claude 的全面知识。

当 Claude 收到一个能从最新信息或专业知识中受益的请求时，它会运用推理能力判断网页搜索工具是否有助于提供更准确的回答。如果搜索网络会有帮助，Claude 会生成一个有针对性的搜索查询，检索相关结果，分析其中的关键信息，并给出附带来源引用的全面回答。

Claude 还能以智能体方式运行，进行多次渐进式搜索，用先前的结果指导后续查询，从而完成轻量级调研并生成更全面的回答。开发者可以通过调整 *max_uses* 参数来控制这一行为。在幕后，Claude 也可能优化自己的查询，以提供更准确的回答。

有了网页搜索，开发者现在可以构建接入最新信息的 AI 解决方案，而无需自行管理网络搜索基础设施。

### 用例

网页搜索让 Claude 能够支撑各类受益于实时数据和专业知识的用例，覆盖众多行业。用例包括：

- **金融服务：** 构建分析实时股价、市场趋势和监管动态的 AI 智能体。
- **法律研究：** 创建可访问近期法院判决、监管变化和法律新闻的工具。
- **开发者工具：** 让 Claude 能够引用最新的 API 文档、GitHub 发布和技术更新。
- **生产力：** 构建整合最新公司报告、竞争情报或行业研究的智能体。

### 以信任与可控性为本进行构建

每一条来自网络的回答都包含对来源材料的引用，用户可以直接核实信息。这对于要求准确性与可追责性的敏感用例尤其有价值。

组织可以通过以下管理设置保持额外的控制力：

- **域名允许列表**：指定 Claude 可以搜索并从中获取信息的域名，确保结果只来自获得批准的来源。
- **域名阻止列表**：阻止 Claude 访问某些可能包含对你组织而言敏感、涉密或不当内容的域名。
- **组织级管理**：管理员可以在组织层面允许或禁止使用网页搜索。

### 用网页搜索增强 Claude Code

网页搜索现在也可在 Claude Code 中使用，把来自网络的最新信息加入开发工作流。

启用网页搜索后，Claude Code 可以访问最新的 API 文档、技术文章，以及关于开发工具和库的其他信息。在使用全新或快速演进的框架、排查疑难错误，或实现需要特定版本 API 参考的功能时，这一点尤其有价值。

### 客户聚焦：Poe

Quora 正在其 AI 平台 Poe 中引入网页搜索。

"Anthropic 的网页搜索工具是 Poe 平台的一个受欢迎的新增功能。它成本高效，并以令人瞩目的速度返回搜索结果，这将为在 Poe 上使用 Claude 模型、同时需要获取实时信息的人带来好处。"Quora 的 Poe 产品负责人 Spencer Chan 说。

### 客户聚焦：Adaptive.ai

Adaptive 是一款面向消费者的 AI 工具，用于创建端到端应用。

"Anthropic 的网页搜索始终提供透彻的结果，表现优于我们测试过的其他工具。Claude 回答的深度与准确性，以及它作为研究智能体运作的能力，将显著改变我们帮助客户构建联网产品的效率。"Adaptive 联合创始人 Dennis Xu 说。

### 开始使用

网页搜索现已在 Anthropic API 上可用，支持 Claude 3.7 Sonnet、升级版 Claude 3.5 Sonnet 和 Claude 3.5 Haiku，价格为每 1,000 次搜索 10 美元，另加标准 token 费用。

要开始使用，请在你的 API 请求中启用网页搜索工具。浏览我们的[文档](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/web-search-tool)和[定价](https://www.anthropic.com/pricing#api)了解更多。

FAQ（常见问题）
