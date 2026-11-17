---
title: "AWS 上的 Claude Platform 正式推出"
title_en: "Introducing the Claude Platform on AWS"
date: 2026-05-11
source: https://claude.com/resources/articles/claude-platform-on-aws
crawled: 2026-11-17
translated: 2026-11-17
---

# AWS 上的 Claude Platform 正式推出

> 原文：[Introducing the Claude Platform on AWS](https://claude.com/resources/articles/claude-platform-on-aws) · Claude 博客

AWS 上的 Claude Platform 现已正式可用，为 AWS 客户提供了一种新方式：借助 AWS 身份认证、计费与承诺用量抵扣，访问完整的 Claude Platform 功能集。Claude 也继续在 Amazon Bedrock 上提供，那里的数据处理方是 AWS。

从今天起，AWS 上的 Claude Platform 客户可以用 [Claude Managed Agents](https://claude.com/resources/articles/claude-managed-agents) 大规模部署智能体，并使用代码执行、技能（skills）、顾问策略（advisor strategy）等工具进行构建。

## 通过 AWS 访问完整的 Claude Platform

AWS 上的 Claude Platform 首次把完整的 Claude API 功能带给 AWS 客户，所有新功能和测试版都会与原生 Claude API 同日上线。

身份认证通过 AWS IAM 进行，审计日志通过 CloudTrail 记录，计费则通过一张 AWS 发票完成，可全额抵扣现有承诺用量。客户使用现有的 AWS 凭证和 IAM 策略，因此团队仍在他们本已管理的工具与权限范围内工作。

AWS 上的 Claude Platform 将在大多数 AWS 商业区域提供，并支持全球与美国推理地理区域。

![ReliaQuest](https://assets.claude.com/81e7e7b1d5fcf826f50c7098167d206c77828a5d.svg)

> 「AWS 上的 Claude Platform 简化了我们访问 Claude 的方式，改善了 Claude Code 工程师等关键用户的体验，并为我们在现有云运营模式之内把更多前沿 AI 能力集成进网络安全与工程工作流提供了一条切实可行的路径。Anthropic 团队投入、配合，在我们扩大使用规模的过程中给了我们信心。」
>
> Jonathan Echavarria，首席研究科学家

![OpenRouter](https://assets.claude.com/e4561f4299b2abca78a6ba30728440072a3c4ef6.svg)

> 「使用 AWS 上的 Claude Platform，让 OpenRouter 和我们的用户可以直接获得原生 Claude API 最新、最强的功能；我们最前沿的客户和用例所需要的一切都可用，而且我们通过与其他 AWS 服务相同的 AWS IAM 凭证来控制访问。它在可用性、延迟和吞吐量方面表现出稳定的性能，直接与 Anthropic 团队合作也帮助我们推进得更快。」
>
> Tomas Oliva，AI 平台工程师

![Emergent.sh](https://assets.claude.com/de977cfbbd0d24ace485030e1ad6088f9b0c75db.svg)

> 「AWS 上的 Claude Platform 让我们以 AWS 作为访问层，同时获得 Anthropic 的官方 API，因此我们拥有完整的功能一致性，并能在新模型能力上线首日就用上。支持服务是其中最出色的部分之一，感觉就像两家公司组成了一个团队，而不是两段彼此分离的合作关系。在规模扩张阶段能有这样的协作相当罕见，这也是我们能够一直保持如此速度的重要原因。」
>
> Avinash Vishwakarma，首席架构师

## 包含哪些内容

AWS 上的 Claude Platform 包含原生平台功能，例如：

* [**Claude Managed Agents（测试版）**](https://platform.claude.com/docs/en/managed-agents/overview)，用于大规模构建和部署托管智能体
* [**顾问策略（测试版）**](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool)，通过咨询一个顾问模型为智能体提供智力增益
* **[网页搜索](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool)与[网页抓取](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool)**，用来自全网的最新真实数据补充 Claude 的知识
* **[代码执行](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool)**，直接在 API 调用中运行 Python 代码、创建可视化并分析数据
* [**Files API（测试版）**](https://platform.claude.com/docs/en/build-with-claude/files)，用于上传文档并在多轮对话中引用
* [**技能（Skills，测试版）**](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)，教 Claude 最佳实践，使其交付一致的结果
* [**MCP 连接器（测试版）**](https://platform.claude.com/docs/en/agents-and-tools/mcp-connector)，无需编写客户端代码即可把 Claude 连接到任意远程 MCP 服务器
* [**提示缓存**](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)，降低重复上下文带来的成本与延迟
* [**引用**](https://platform.claude.com/docs/en/build-with-claude/citations)，让回答建立在源文档之上
* [**批处理**](https://platform.claude.com/docs/en/build-with-claude/batch-processing)，面向高并发、异步负载

AWS 上的 Claude Platform 客户还可以访问 Claude Console——Anthropic 提供的、用于基于 Claude 构建和测试的开发环境。Console 包含对智能体、技能、环境、保险库（vaults）、可观测性工具等的管理能力。

目前提供 Claude Opus 4.7、Sonnet 4.6 和 Haiku 4.5，新模型发布时也会在 AWS 上的 Claude Platform 同步上线。

## 为开发者选择正确的路径

AWS 上的 Claude Platform 与 Amazon Bedrock 上的 Claude 都能让 AWS 客户基于 Claude 模型构建。区别在于由谁运营服务，以及哪些功能可用。

**AWS 上的 Claude Platform** 是 Anthropic 首个此类产品，从第一天起就提供全部原生 Claude API 功能。服务由 Anthropic 运营，数据在 AWS 边界之外处理。对于想要完整体验 Claude Platform 的公司来说，这是一个好选择。

**Amazon Bedrock 上的 Claude** 保持 AWS 作为数据处理方，并在 AWS 边界内运行。这适合有严格区域数据驻留要求、或需要数据仅在 AWS 基础设施内处理的公司。

## 开始使用

AWS 上的 Claude Platform 今日可用。要开始使用，请访问 [AWS 上的 Claude Platform](https://aws.amazon.com/claude-platform/)，或查阅[文档](https://platform.claude.com/docs/en/build-with-claude/claude-platform-on-aws)。

如果你已有 Bedrock 的私下报价（private offer），在开始使用 AWS 上的 Claude Platform 之前，请先联系你的 Anthropic 或 AWS 客户经理，以确保折扣被正确应用。折扣无法追溯适用于在 Claude Platform 私下报价被接受之前产生的用量。
