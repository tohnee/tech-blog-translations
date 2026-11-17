---
title: "Claude Managed Agents 新功能：自托管沙箱与 MCP 隧道"
title_en: "New in Claude Managed Agents: self-hosted sandboxes and MCP tunnels"
date: 2026-05-19
source: https://claude.com/resources/articles/claude-managed-agents-updates
crawled: 2026-11-17
translated: 2026-11-17
---

# Claude Managed Agents 新功能：自托管沙箱与 MCP 隧道

> 原文：[New in Claude Managed Agents: self-hosted sandboxes and MCP tunnels](https://claude.com/resources/articles/claude-managed-agents-updates) · Claude 博客

从今天起，[Claude Managed Agents](https://claude.com/resources/articles/claude-managed-agents) 可以在由你掌控的沙箱中运行，并能连接你私有的模型上下文协议（MCP）服务器。智能体执行工具所在的沙箱，以及它所访问的服务，都运行在企业既定的边界之内，处于你的安全和运行时控制之下。

沙箱既可以运行在你自己的基础设施上，也可以交给 [Cloudflare](https://developers.cloudflare.com/sandbox/claude-managed-agents/)、[Daytona](https://www.daytona.io/docs/en/guides/claude/claude-managed-agents)、[Modal](https://github.com/modal-labs/claude-managed-agents-modal-sandbox/tree/main)、[Vercel](https://vercel.com/kb/guide/run-claude-managed-agent-tools-with-vercel-sandbox) 等托管服务商，由它们为你处理计算和隔离。

在 Claude Platform 上，[自托管沙箱](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes) 以公开 beta 提供，MCP 隧道处于研究预览阶段（[申请访问](https://claude.com/form/claude-managed-agents)）。

## 自托管沙箱：让智能体执行保持在你的边界之内

自托管沙箱让 Claude Managed Agent 在你掌控的基础设施上、或通过托管沙箱服务商执行工具。代码执行、敏感文件、软件包、服务与数据都留在企业边界之内，处于你的安全与运行时控制之下。

使用自托管沙箱时，敏感文件、软件包和服务保留在你自己的基础设施中，或放在托管沙箱服务商处。负责编排、上下文管理和错误恢复的[智能体循环](https://www.anthropic.com/engineering/managed-agents)仍运行在 Anthropic 的基础设施上，而工具执行则转移到你配置好的环境中。

在你的边界之内，网络策略、审计日志和安全工具已经就位，文件和代码库不会外流。计算资源也由你掌控：资源规格和运行时镜像在你这一侧设定，因此执行长时间构建、图像生成等重计算任务的智能体能获得任务所需的 CPU、内存和容量。

![](https://assets.claude.com/42f264f794fcb8b8a7c160efddd61ad4e9c941fe.png)

## 选择你的沙箱客户端

你可以使用任意沙箱客户端，也可以从我们支持的以下服务商开始：

* [**Cloudflare**](https://developers.cloudflare.com/sandbox/claude-managed-agents/) 使用 microVM 和更轻量的 isolate 大规模运行沙箱。出站网络请求由你控制：零信任的密钥注入、可定制的代理以审计、重路由或修改出站流量，以及通过 Cloudflare 网络连接内部服务的能力。[**Amplitude**](https://amplitude.com/blog/design-agent) 正在基于 Managed Agents 和 Cloudflare 构建 Design Agent——一个用于符合品牌规范的生产级 UI 与营销设计的内部工具——以获得更紧密的可观测性和控制。
* [**Daytona**](https://www.daytona.io/docs/en/guides/claude/claude-managed-agents) 的沙箱是完整的可组合计算机，可长时间运行且有状态。同一个原语既能跑一次快速突发任务，也能支撑一个连续工作数小时的智能体。会话运行期间，沙箱可通过 SSH 或带认证的预览 URL 访问，也可以暂停后再恢复，完整保留状态。[**Clay**](http://clay.com/) 的 GTM 工程智能体 Sculptor 就在 Managed Agents 和 Daytona 上自主构建、测试和监控工作流。
* [**Modal**](https://modal.com/blog/introducing-claude-managed-agents-with-modal-sandboxes) 是为 AI 工作负载打造的云平台，其沙箱与 Modal 的函数、存储和网络原语共享同一套基础，为你提供构建生产级 AI 系统所需的一切。Modal 的自定义容器运行时可在任意镜像上实现亚秒级启动，可扩展到数十万个并发沙箱，并按需提供 CPU 和 GPU 资源。
* [**Vercel**](https://vercel.com/kb/guide/run-claude-managed-agent-tools-with-vercel-sandbox) 的沙箱结合了 VM 安全、VPC 对等连接和自带云（bring your own cloud），启动时间为毫秒级。Managed Agents 负责模型、工具和会话状态，而 Vercel Sandbox 防火墙在网络边界注入凭证，使其永远不会进入沙箱。[**Rogo**](https://rogo.ai/) 是一家面向机构金融的 AI 平台，正在基于 Managed Agents 和 Vercel Sandbox 构建分析师智能体，以安全地处理其专有数据。

## MCP 隧道：连接你私有网络内的服务

[MCP 隧道](http://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/overview) 可以把 Claude Managed Agents 连接到位于你私有网络内的模型上下文协议（MCP）服务器，而无需将它们暴露到公网。内部数据库、私有 API、知识库和工单系统都会成为智能体可以调用的工具。你部署一个轻量网关，由它建立单一出站连接：无需入站防火墙规则，没有公网端点，流量端到端加密。

MCP 隧道在 Managed Agents 和 Messages API 中均受支持。MCP 隧道由组织管理员在 [Claude Console](https://platform.claude.com/) 的工作区设置中管理。

![](https://assets.claude.com/f594547db5f92c19b5fd55f16200055920e26db2.png)

![Mason](https://assets.claude.com/dc5e9a8c6de2d2566eed3e94e3814ce42e7ad408.svg)

> “我们的用例需要在复杂的产品面上安全地编排内部工具。Modal 的沙箱提供了我们企业客户所需的安全边界，再与 Claude Managed Agents 结合，就给了我们一个强大的执行框架，而无需再手工搭建额外的复杂度。我们在一周之内就跑通了可用版本，为客户提升了可靠性。”

Sai Yandapalli，CTO

![Amplitude](https://assets.claude.com/8d26ba2d0a3509fa32dbe993b1aa1cb455419f1a.svg)

> “Claude Managed Agents 与 Cloudflare 让我们在两天内，就在已经熟悉并信任的基础设施上跑起了设计智能体的第一个可用版本。”

Will Newton，设计

![Doordash](https://assets.claude.com/23e9f66a28975a13266abe3f53567c17a5bdb888.svg)

> “在面向本地企业扩展智能体式商业（agentic commerce）的过程中，我们需要一条极其高效的通向生产环境的路径，具备完整的执行框架控制、规模与可靠性。我们很期待评估 Claude Managed Agents 作为下一步方案，在基于 Modal 的 AI 基础设施之上继续构建！”

Andy Fang，联合创始人

![Clay](https://assets.claude.com/267a4deeacbde106146d26ffa4ef2b08fbb3cb4f.svg)

> “构建 Sculptor——Clay 用于自主构建和测试 GTM 工作流的 GTM 工程智能体——时，我们想给它一种比‘循环里调用工具’更灵活、更强大的行动方式。Claude Managed Agents 让我们能复现本地智能体的能力，同时拥有云智能体的可靠性、版本管理和后台执行能力。而用 Daytona 这类沙箱来运行，则让我们掌控文件系统，可以挂载外部文件存储并即时安装软件包。”

Ryan Chang，AI 工程

![Rogo](https://assets.claude.com/c0fcb1875e1dc462ab8875733bd22e98359457d6.svg)

> “Claude Managed Agents 负责智能体循环，Vercel 的沙箱给了我们一个可以按自身工作负载配置的环境。这让我们能够利用一流的基础设施，同时专注于对金融 AI 平台真正有复利效应的事情：工具与数据的深度和广度，以及一个按投资者和银行家真实工作方式构建的产品界面。”

Strib Walker，产品负责人

## 开始使用

自托管沙箱和 [MCP 隧道](https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/overview) 都运行在 Managed Agents 支持的同一套核心原语之上。自托管沙箱以公开 beta 提供，MCP 隧道处于研究预览阶段。要开始使用 MCP 隧道，请[申请访问](https://claude.com/form/claude-managed-agents)。

浏览我们的[文档](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes)了解更多，参考我们的 [cookbook](https://github.com/anthropics/claude-cookbooks/tree/main/managed_agents/self_hosted_sandboxes) 配置你的沙箱服务商，或在 [Claude Console](https://platform.claude.com/) 中部署你的第一个智能体。
