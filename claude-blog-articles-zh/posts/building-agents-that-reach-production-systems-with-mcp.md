---
title: "用 MCP 构建能够触达生产系统的智能体"
title_en: "Building agents that reach production systems with MCP"
source: https://claude.com/blog/building-agents-that-reach-production-systems-with-mcp/
crawled: 2026-09-14
translated: 2026-09-14
---

# 用 MCP 构建能够触达生产系统的智能体

> 原文：[Building agents that reach production systems with MCP](https://claude.com/blog/building-agents-that-reach-production-systems-with-mcp/) · Claude 博客

智能体的有用程度，取决于它能够触达哪些系统。团队在把智能体连接到外部系统时，往往会收敛到三种方式——直接 API 调用、CLI 和 MCP。本文将说明各自适用的场景、为什么生产环境的智能体最终大多落在 MCP 上，以及高效构建这类集成的各种模式。

## 把智能体连接到外部系统

我们通常看到三条把智能体连接到外部系统的路径：直接 API 调用、CLI 和 MCP。每一种在特定场景下都合理，取决于你在构建什么。关键区别在于智能体与服务之间是否存在一个公共层，以及这个公共层能够延伸多远。

### 直接 API 调用

智能体直接调用你的 API——要么在代码执行沙箱里编写发起 HTTP 请求的代码，要么通过一个通用的函数调用工具。这是大多数团队的起点，对于一个智能体对接一个服务、或少量无需跨智能体平台复用的集成来说，它工作得很好。

挑战在规模化时开始显现。智能体与服务之间没有公共层，每一对「智能体-服务」组合都会成为一个定制的集成，各自处理认证、工具描述和边界情况——这就是 M×N 集成问题。

### 命令行界面（CLI）

智能体在 shell 中运行你的命令行工具。这种方式快速、轻量，并复用现成的工具链。它非常适合本地环境和沙箱化容器——任何有文件系统和 shell 的地方。它提供了一个公共层，但很薄。

CLI 在触达不暴露容器的移动端、Web 或云端托管平台时会遇到硬性限制，而且认证由 CLI 自身的机制处理——通常是磁盘上的一个凭证文件。它最适合本地环境中快速、宽松的集成。

### Model Context Protocol（MCP）

MCP 以协议的形式提供公共层。智能体连接到一个暴露你系统能力的服务器，认证、发现与丰富的语义都已完成标准化。一个远程服务器可以触达任何兼容的客户端（Claude、ChatGPT、Cursor、VS Code 等），适用于任何部署环境。

它需要多一点前期投入。回报是集成具备可移植性，并提供功能丰富的智能体集成所需的语义。

## 生产环境的智能体运行在云端

生产环境的智能体越来越多地运行在云端，以便扩展规模并持续运转。它们需要触达的系统同样托管在云端：你的数据所在之处、工作被跟踪之处、基础设施运行之处。这些系统往往是远程的，且位于认证之后，而 MCP 正好提供公共层。当这些系统位于私有网络而非公共互联网上时，[Claude Managed Agents 中的 MCP tunnels](https://claude.com/blog/claude-managed-agents-updates) 可以通过仅出站（outbound-only）的连接把智能体连接到它们——无需暴露端口或公共端点。

我们已经看到这一趋势在落地。[MCP SDK](https://modelcontextprotocol.io/docs/sdk) 的月下载量最近突破 3 亿次，而年初还是 1 亿次，在企业与主流智能体平台中被广泛采用。每天有数百万人搭配 Claude 使用 MCP，该协议支撑着我们近期发布的许多产品，包括 [Claude Cowork](https://claude.com/product/cowork)、[Claude Managed Agents](https://claude.com/blog/claude-managed-agents) 与 [Claude Code 中的 channels](https://code.claude.com/docs/en/channels)。

随着 MCP 持续支撑生产环境的智能体系统，我们在此分享把这些集成做好的模式：从构建高级服务器到上下文高效的客户端，以及 skills 在哪些方面与协议互补。

## 构建高效的 MCP 服务器

我们的[目录](https://claude.ai/directory/connectors)中有超过 200 个 MCP 服务器，每天有数百万人使用。从与基于该协议进行构建的企业和开发者的紧密合作中，我们总结出了一些设计模式，它们决定了智能体使用一个服务器时的可靠程度。

### 构建远程服务器以获得最大覆盖面

远程服务器才能带来分发能力——它是唯一能跨 Web、移动端和云端托管智能体运行的配置，也是每个主流客户端都针对优化的消费形态。构建远程服务器，让智能体无论在哪里运行都能使用你的系统。

### 围绕意图而非端点来组织工具

数量更少、描述完善的工具，始终胜过对 API 的一比一穷举镜像。不要把你的 API 原样包装成 MCP 服务器——围绕意图来组织工具，让智能体用一两次调用就能完成任务，而不是把许多原语拼接起来。一个 create_issue_from_thread 工具胜过 get_thread + parse_messages + create_issue + link_attachment。参阅[为智能体编写高效的工具](https://www.anthropic.com/engineering/writing-tools-for-agents)了解完整模式。

### 当服务面很大时，为代码编排而设计

如果你的服务需要数百个不同的操作，比如 Cloudflare、AWS 或 Kubernetes，按意图分组的工具集很可能覆盖不了。这时应该暴露一个接受代码的薄工具面：智能体编写一段简短的脚本，你的服务器在沙箱中针对你的 API 运行它，只有结果返回。[Cloudflare 的 MCP 服务器](https://github.com/cloudflare/mcp)是参考范例——两个工具（搜索和执行）用大约 1K token 覆盖了约 2,500 个端点。

### 在有帮助的地方提供丰富语义

[MCP Apps](https://modelcontextprotocol.io/extensions/apps/overview) 是第一个官方协议扩展，它让工具可以返回交互式界面——例如图表、表单或仪表盘——全部在聊天界面中内联渲染。提供 MCP apps 的服务器，其采用率与留存率往往显著高于只返回文本的服务器。用它在你最重要的时刻把产品的 UI 呈现在智能体或最终用户面前——该扩展已在 Claude.ai、Claude Cowork 以及许多其他顶级 AI 工具中获得支持。

[Elicitation（征询）](https://modelcontextprotocol.io/specification/2025-11-25/client/elicitation)让你的服务器可以在工具调用进行到一半时暂停，向用户请求输入。[表单模式（form mode）](https://modelcontextprotocol.io/specification/2025-11-25/client/elicitation#form-mode-elicitation-requests)发送一个简单的 schema，由客户端渲染一个原生表单——用它来请求缺失的参数、确认破坏性操作，或对选项进行消歧。[URL 模式](https://modelcontextprotocol.io/specification/2025-11-25/client/elicitation#url-mode-elicitation-requests)把用户引导到浏览器——用它来完成下游 OAuth、收款，或收集任何不应流经 MCP 客户端的凭证。两者都让用户留在工作流之中，而不是被送去设置页面。表单模式已获得广泛支持；URL 模式已在 Claude Code 中支持，更多客户端的支持正在推进。

### 依靠标准化的认证

标准化的认证让 MCP 对云端托管的智能体变得可行。如果你的服务器要求 OAuth，最新的 [MCP 规范](https://modelcontextprotocol.io/specification/2025-11-25)支持用 [CIMD](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization#client-id-metadata-documents)（Client ID Metadata Documents，客户端 ID 元数据文档）进行客户端注册——它为用户提供快速的首认证流程，并大幅减少出人意料的重复认证提示。这是我们推荐的认证方案，该能力已在 MCP SDK、Claude.ai 和 Claude Code 中获得支持，并正在全行业广泛采用。

用户完成授权之后，下一个问题是云端托管的智能体如何在运行时持有并复用这些令牌。[Claude Managed Agents](https://platform.claude.com/docs/en/managed-agents/overview) 中的 [Vaults](https://platform.claude.com/docs/en/managed-agents/vaults#mcp-oauth-credential) 解决了这个问题：一次性注册用户的 OAuth 令牌，在会话创建时通过 ID 引用该 vault，平台就会把正确的凭证注入每一条 MCP 连接，并代你刷新——无需自建密钥存储，也无需在每次调用中传递令牌。

## 让 MCP 客户端的上下文使用更高效

MCP 标准化了 AI 智能体（[*客户端*](https://modelcontextprotocol.io/docs/develop/build-client#python)）如何连接并使用它们所需的工具与数据源（[*服务器*](https://modelcontextprotocol.io/docs/develop/build-server)）。服务器安全地暴露一系列能力，而客户端负责编排它们并管理上下文。如果你在构建 MCP 客户端，请用渐进式披露（progressive disclosure）的模式让它对上下文更高效。

### 用工具搜索（tool search）按需加载工具定义

[工具搜索（tool search）](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool)不再预先把所有工具加载进上下文，而是允许智能体在运行时搜索工具目录，按需拉入相关工具。在我们的[测试](https://www.anthropic.com/engineering/advanced-tool-use)中，工具搜索往往能把工具定义 token 减少 85% 以上，同时保持很高的选择准确率。

用工具搜索降低上下文占用。来源：[高级工具使用（advanced tool use）](https://www.anthropic.com/engineering/advanced-tool-use)

### 用程序化工具调用在代码中处理工具结果

[程序化工具调用（programmatic tool calling）](https://www.anthropic.com/engineering/code-execution-with-mcp)在代码执行沙箱中处理工具结果，而不是把它们原样返回给模型。这让智能体能够在代码中对多次调用进行循环、过滤和聚合，只有最终输出进入上下文。在我们的测试中，这能把复杂多步工作流的 token 用量降低约 [37%](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling)。

这些模式可以自然地跨多个服务器组合：更精简的上下文、更少的往返、更快的响应。完整分析参见[*高级工具使用*](https://www.anthropic.com/engineering/advanced-tool-use)。

## 把 MCP 服务器与 skills 搭配使用

[Skills 与 MCP 是互补的](https://claude.com/blog/skills-explained)。MCP 让智能体能够访问来自外部系统的工具与数据，而 skills 教会智能体*如何*使用这些工具完成实际工作的程序性知识。最强大的智能体两者兼备，skills 让 MCP 服务器的能力扩展到远不止几次简单的连接。组合二者有两种常见模式：

### 把 skills 与 MCP 服务器打包为插件

面向 Claude 的[插件（plugins）](https://code.claude.com/docs/en/plugins-reference#plugin-components-reference)是一种有用的抽象，让开发者可以把 skills、MCP 服务器、hooks、LSP 服务器和专门的子智能体打包成一种易于消费的分发方式。这是以最小摩擦统一多个上下文提供方的最佳途径。

把 MCP 服务器与 skills 结合，能让 Claude 的表现更像一个领域专家。通过 MCP 获取工具，再通过 skills 让 Claude 端到端地编排工作流。以我们面向 Cowork 的[数据插件](https://claude.ai/directory/plugins/data%40knowledge-work-plugins)为例，它由 10 个 skills 和 8 个 MCP 服务器组成，覆盖 Snowflake、Databricks、BigQuery、Hex 等应用。

将 skills 与 MCP 结合。来源：[用 skills 与 MCP 服务器扩展 Claude 的能力](https://claude.com/blog/extending-claude-capabilities-with-skills-mcp-servers)

### 从 MCP 服务器分发 skills

提供方在发布 MCP 服务器的同时附带一个 skill 的做法正日益普遍，这样智能体既获得原始能力，也获得用好这些能力的成套打法（playbook）。[Canva](https://claude.com/connectors/atlassian)、[Notion](https://claude.com/connectors/notion)、[Sentry](https://claude.com/connectors/sentry) 等许多提供方今天已在 Claude 中这样做，在[网页目录](https://claude.com/connectors)中把 skill 列在自家连接器旁边。

为了让这种搭配在所有客户端之间可移植，MCP 社区正在积极开发一个直接从服务器分发 skills 的[扩展](https://github.com/modelcontextprotocol/experimental-ext-skills)。这样客户端就能自动继承相关的专业知识，并与它所依赖的 API 一起进行版本管理。我们预计随着该扩展趋于稳定，这一模式将得到广泛采用。

## 复利式增长的一层

我们在开头给出了连接智能体与外部系统的三条路径。在实践中，成熟的集成会三者齐备：API 作为地基，CLI 面向本地优先的环境，MCP 面向云端的智能体。

随着生产环境的智能体迁往云端，MCP 成为关键的一层，也是具有复利效应的一层。今天，一个远程服务器就能触达任何部署环境中的每个兼容客户端，认证、交互性与丰富语义都由协议处理。随着更多客户端采用该规范、更多扩展落入其中，同一个服务器会在你没有发布任何新东西的情况下变得更强大。

在构建集成时，如果你的目标是让云端的智能体触达你的系统，那就构建一个 MCP 服务器，并用上述模式把它做到极致。每一个基于 MCP 构建的集成都在强化整个生态：需要独自解决的边界情况更少，需要维护的定制集成更少。

### 致谢

感谢 Den Delimarsky、David Soria Parra、Henry Shi、Felix Rieseberg、Conor Kelly、Molly Vorwerck、Andy Schumeister、Kevin Garcia、Amie Rotherham、Matt Samuels、Angela Jiang、Katelyn Lesse、AJ Rebeiro 与 Jess Yan 对本文的贡献。

FAQ（常见问题）
