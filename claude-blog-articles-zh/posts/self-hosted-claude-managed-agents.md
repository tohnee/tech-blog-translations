---
title: "在你的安全边界内运行 Claude Managed Agents"
title_en: "Operate Claude Managed Agents inside your security perimeter"
date: 2026-11-12
source: https://claude.com/resources/articles/self-hosted-claude-managed-agents
crawled: 2026-11-17
translated: 2026-11-17
---

# 在你的安全边界内运行 Claude Managed Agents

> 原文：[Operate Claude Managed Agents inside your security perimeter](https://claude.com/resources/articles/self-hosted-claude-managed-agents) · Claude 博客

推出自托管的 Claude Managed Agents。现在，你可以在自己的环境中运行智能体，无论是在自己的云上还是本地部署。智能体、凭据和会话历史都由你托管，发往 Claude 的请求也可以由你选择发送到哪里。

[自托管的 Claude Managed Agents](https://platform.claude.com/docs/en/managed-agents/self-hosted) 现已开放内测（private beta）。开发者可以构建直接在公司代码和内部系统中工作的智能体，并在自己的环境中运行这些智能体。

自托管是运行 [Managed Agents](https://claude.com/platform/claude-managed-agents) 的一种新方式。Managed Agents 是一套可组合的 API，用于构建和部署自主智能体，提供 agent harness（智能体执行框架）、沙箱、凭据处理和会话历史，帮助长时运行的智能体进入生产环境。

## 在你自己的环境中运行智能体控制平面

我们最初将 Managed Agents 作为 Claude Platform 上的托管服务推出，由 Anthropic 为你运行基础设施。对于需要让代码留在自己环境中的团队，我们随后增加了[自托管沙箱](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes)。

此后，智能体变得更强，开始承担更关键的工作，例如修复构建失败、测试发布、分诊告警，以及清理 bug 积压。它们在无人值守的情况下运行于你的代码之上，需要访问你的内部系统。对于拥有这种访问权限的智能体，一些团队希望整个服务都放在自己的环境中，而不只是沙箱。在此之前，这意味着必须自行搭建平台。

使用自托管的 Managed Agents，服务的每个部分都运行在你自己的云上或本地，包括 harness、沙箱、凭据和会话历史。你负责运行 Managed Agents 服务器、其数据库，以及智能体执行 shell 和文件工具所用的 worker。模型请求发送到你选择的目的地：Anthropic 直连、你的云服务商（Amazon Bedrock、Google 的 Agent Platform 或 Microsoft Foundry），或你自己的网关。开发者构建智能体时使用的核心 API 与托管的 Managed Agents 服务完全一致。

会话历史存储在你自己的数据库中。如果你的组织与 Anthropic 之间已启用[零数据保留（ZDR）](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention#zero-data-retention-zdr-scope)，那么它对发往 Claude 的请求的适用方式与其他任何 Messages API 调用相同。

![图 1：自托管的 Claude Managed Agents](https://assets.claude.com/7607c90e3d3d6e3bf9f7d1af0d39afb006be1413.svg)

## 为智能体安全而设计

当智能体无人值守地运行在你的代码和系统内部时，你无法依赖某个人去检查每一步，因此限制必须内建在系统本身之中。这就是为什么智能体安全要从架构开始，也是我们围绕四条原则设计 Managed Agents 的原因。无论是 Anthropic 托管全部、你只托管沙箱，还是你托管整个服务，这些原则都适用。

**大脑与双手分离**

harness（大脑）负责调用 Claude，沙箱（双手）是智能体代码运行的地方。两者在设计上相互分离：智能体代码在沙箱中运行，而智能体循环、会话历史和 vault 密钥都留在沙箱之外。[分离二者](https://www.anthropic.com/engineering/managed-agents)还意味着，智能体不依赖某一个沙箱存活于整个运行过程；沙箱只在某个工具需要时才启动，会话历史则以事件日志的形式存在于沙箱之外。

**凭据不进沙箱**

Vault 的设计目标是让凭据不进入沙箱。对于 MCP 工具和受支持的 API 调用，[沙箱之外的代理会把凭据添加到请求中](https://platform.claude.com/docs/en/managed-agents/vaults)。使用自托管的 Managed Agents，你还可以把凭据存放在自己的密钥管理器中。

**网络访问可以受限**

你可以把每个环境限制在[一份允许访问的主机列表](https://platform.claude.com/docs/en/managed-agents/secure-deployment)内，发往其他任何主机的请求都会被阻止。对于修复构建失败的智能体，这份列表可能只有你的 git 主机和包仓库。当你自行托管沙箱时，可以在自己的防火墙中设置同样的限制。

**每个会话都留下完整记录**

Managed Agents 会记录智能体所走的每一步，包括它发起的工具调用以及返回的结果。该记录可通过 [OpenTelemetry](https://platform.claude.com/docs/en/manage-claude/opentelemetry) 导出，因此你可以把它发送到现有的监控工具，像查看其他系统一样审查智能体活动。

## 开始使用

自托管的 Claude Managed Agents 现已开放内测。请联系你的 Anthropic 客户团队申请访问权限，或阅读[文档](https://platform.claude.com/docs/en/managed-agents/self-hosted)了解更多。
