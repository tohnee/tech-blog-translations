---
title: "MCP 2026-07-28 规范：无状态核心，登陆 Claude"
title_en: "MCP 2026-07-28 spec: stateless core, coming to Claude"
source: https://claude.com/blog/bringing-mcp-2026-07-28-to-claude/
crawled: 2026-09-14
translated: 2026-09-14
---

# MCP 2026-07-28 规范：无状态核心，登陆 Claude

> 原文：[MCP 2026-07-28 spec: stateless core, coming to Claude](https://claude.com/blog/bringing-mcp-2026-07-28-to-claude/) · Claude 博客

Model Context Protocol 的第五个规范版本 [**MCP 2026-07-28**](https://modelcontextprotocol.io/specification/2026-07-28) 现已正式发布。最新规范把 MCP 迁移到无状态核心，同时强化了授权机制，并将官方扩展正式转正。相关支持正在各类 Claude 产品中陆续推出。

## MCP 的新变化

MCP 的月度 SDK 下载量最近突破 4 亿次，今年增长了 4 倍，并已成为连接 AI 智能体与应用程序的行业标准。MCP 2026-07-28 是迄今最重要的规范版本之一：**无状态核心。** MCP 从双向有状态协议转向请求/响应模型。服务器现在可以部署在无服务器（serverless）与边缘基础设施上。这简化了为 Claude 构建 MCP 服务器、并随着采用增长而扩展其用量的体验。

**标准化的扩展。** [MCP Apps](https://modelcontextprotocol.io/extensions/apps/overview) 与 [Tasks](https://modelcontextprotocol.io/extensions/tasks/overview) 现在在一个带版本号的扩展框架下发布，为开发者提供了一条正式路径，可以在不改动核心协议的情况下添加交互式 UI、长时间运行的工作等能力。

**授权强化。** 授权现在与生产环境的 OAuth 2.0 和 OIDC 部署保持一致，MCP 服务器无需任何变通方案即可接入 Entra 或 Okta 等企业身份系统。

自 beta 阶段起，生态中的各家公司就与 MCP 社区一起基于新规范进行构建：

「更多开发者正在使用我们的 MCP 服务器，把生成的成果带入 Figma 的画布，与团队一起探索、发挥并将其打磨成脱颖而出的产品。随着使用量增长，我们的无状态架构可以随之扩展；而借助 MCP Apps、Tasks 和企业托管认证（Enterprise-Managed Auth），我们能做更多事情，让设计与代码在一条相连的流程中保持同步。」

「MCP 是连接 AI 智能体与工具、数据的行业标准，Intuit 很自豪能够支持全新的 MCP 2026-07-28 规范。无状态协议核心与扩展框架（包括 MCP Apps 和 Tasks）让我们的技术人员和客户能够在企业规模上构建并连接智能体体验，也让 Intuit 能够继续为其 1 亿消费者与企业客户提供值得信赖的金融智能体验，无论他们选择在哪里工作。」

「2026-07-28 规范中的无状态核心让 MCP 成为一等公民的 HTTP 工作负载，不再需要绕开会话管理。我们的客户希望 Netlify 上的 MCP 能像平台的其他部分一样简单，而这份新规范从核心上实现了这一点。把 MCP Apps 构建进新的扩展框架，是整个生态在可扩展性、可访问性与能力上向前迈出的一大步。」

「把 MCP 迁移到无状态协议，让我们扩展自己的服务变得更容易，也让我们更容易为客户添加 MCP 服务器的分析能力。这帮助我们向用户展示他们的 MCP 工具是如何被使用的、用户想用而又缺失了哪些工具。很高兴看到这个协议朝这个方向发展。」

「Anthropic 将前沿模型与不断抬高标准的开发者体验相结合。开放的 MCP 2026-07-28 规范中的无状态核心降低了我们所管理的复杂度，让我们能够更快、更大规模地向客户交付更多功能。」

「在 Zoom，我们相信组织上下文是 AI 交付有意义工作的关键，这也是我们构建 MCP 服务器、把 Zoom 会议智能安全地带入 Claude 等 AI 平台的原因。新的 MCP 规范让在标准 HTTP 基础设施上部署和扩展 MCP 服务器变得容易得多——用户可以更快、更可靠地获得 Zoom 的会议智能，就在他们每天依赖的 AI 工作流之中。」

完整细节请参阅 [MCP 2026-07-28 发布公告](https://blog.modelcontextprotocol.io/posts/2026-07-28/)。

## 在 Claude 中推进 MCP

Claude 现已在[连接器目录](https://claude.ai/directory/connectors)中收录超过 950 个 MCP 服务器，每天有数百万人使用。今年，我们在发布新协议扩展支持的同时，也推出了让 MCP 更易构建、更易部署的功能：

[MCP Apps](https://claude.com/blog/interactive-tools-in-claude) 让服务器直接在对话中渲染交互式 UI。用户可以看到连接器正在做什么，并在对话内直接与之协作，无需切换标签页。

[企业托管认证](https://claude.com/blog/enterprise-managed-auth)（Enterprise-managed auth）让管理员能够通过其身份提供方为整个组织配置 MCP 连接器。管理员只需对连接器授权一次，用户通过现有的 IdP 组继承访问权限，并在首次登录时即完成连接：对最终用户而言是零操作设置。

[面向连接器开发者的可观测性](https://claude.com/blog/observability-for-developers-building-connectors)为我们目录中已发布的连接器提供一个仪表盘，展示它们在各 Claude 产品面上的表现。开发者可以用它跟踪采用情况、诊断错误与延迟，并按产品细分用量。

[MCP tunnels（研究预览）](https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/overview)在不向公共互联网暴露的前提下，把 Claude 连接到私有网络内的 MCP 服务器。团队无需入站防火墙规则、无需公共端点、也无需在源站配置 IP 允许列表，就能把内部工具接入 Claude。

2026-07-28 规范中的无状态核心、标准化扩展与强化的授权，将帮助开发者以更低的摩擦、更一致的最终用户体验把更多应用带入 Claude。我们将继续与社区一起投资 MCP 这一开放标准，并持续投资那些让 MCP 在生产环境中更易用、更有效的 Claude 功能。

## 开始使用

即刻探索[规范](https://modelcontextprotocol.io/specification/2026-07-28/)与 [SDK](https://modelcontextprotocol.io/docs/sdk) 上手。相关支持即将在各类 Claude 产品中推出。如果你计划把你的 MCP 服务器提交到 Claude 的[连接器目录](https://claude.ai/directory/connectors)，可以在[这里](https://claude.com/docs/connectors/building/submission)了解更多。

FAQ（常见问题）
