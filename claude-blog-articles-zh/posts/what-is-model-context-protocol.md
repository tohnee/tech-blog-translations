---
title: "什么是模型上下文协议？把 AI 连接到你的世界"
title_en: "What is Model Context Protocol? Connect AI to your world"
source: https://claude.com/blog/what-is-model-context-protocol/
crawled: 2026-09-14
translated: 2026-09-14
---

# 什么是模型上下文协议？把 AI 连接到你的世界

> 原文：[What is Model Context Protocol? Connect AI to your world](https://claude.com/blog/what-is-model-context-protocol/) · Claude 博客

AI 模型的好坏取决于提供给它的上下文。像 [Claude](https://claude.ai) 这样的 AI 助手可以回答问题、完成范围惊人的各种任务，但如果它们无法访问所需的数据或工具，它们能为你做的事就会受限。你通常的解决办法是把上下文从一个标签页复制粘贴到另一个：无论是在 Google Drive 里编辑文档、在 Slack 里回复讨论串，还是在 IDE 中更新代码。这个过程缓慢、依赖手工，而且容易遗漏重要的上下文。

**模型上下文协议（Model Context Protocol，MCP）**提供了一个开放的解决方案，并在所有 AI 应用和助手中广泛可用。在本文中，你将了解 MCP 是什么、它如何工作、为什么重要，以及它是为谁而设计的。你会看到 MCP 实际运用的例子，并明白从今天起如何开始使用 MCP 或基于 MCP 进行构建。

## 什么是模型上下文协议（MCP）？

**模型上下文协议（Model Context Protocol）**是一个开放标准，定义了大语言模型（LLM）如何与外部系统通信。

可以把 MCP 想象成**大语言模型的 USB-C**。正如 USB-C 为你的手机、笔记本和其他设备提供了通用接口，MCP 为大语言模型连接外部系统提供了通用格式。在 USB-C 出现之前，每个电子设备都有自己的线缆：iPhone 用 Lightning，安卓用 micro-USB，相机用专有接口。随着越来越多设备采用 USB-C，整个生态的连接变得畅通无阻。

MCP 把同样的简洁性带给了 AI 集成。在 MCP 出现之前，每个应用和数据库都需要定制代码才能与大语言模型连接：Google Drive 需要自己的集成，Slack 需要另一套，Figma 又是另一套。现在，MCP 提供了一种单一的、标准化的格式，用于把这些工具连接到 Claude 和其他 AI 应用。

## MCP 从何而来？

MCP 由 David Soria Parra 和 Justin Spahr-Summers 在 Anthropic 创造。这个想法源于 David 的一个困扰：他总是在 Claude Desktop 和自己的集成开发环境（IDE）之间来回复制代码。意识到这是一个典型的 M×N 问题——多个应用需要多套集成——David 向 Justin 提议构建一个协议来解决这个问题。他们在流行的语言服务器协议（Language Server Protocol）的基础上设计了 MCP，并在 Anthropic 的支持下于 2024 年 11 月将其开源，确保整个 AI 生态都能受益。

## MCP 如何工作？

MCP 通过双向的方式运作。像 Claude 这样的 AI 智能体和聊天机器人会创建 **MCP 客户端（MCP Client）**，从而连接到 Notion、Canva 或 Figma 等应用；这些应用则通过 **MCP 服务器（MCP Server）**对外提供自己的工具和数据。

通过构建 **MCP 客户端**，AI 智能体和聊天机器人可以访问社区构建的数千个 MCP 服务器，为它们扩展能力提供了一条直接路径。智能体还可以通过 [MCP 隧道](https://claude.com/blog/claude-managed-agents-updates)访问你防火墙之后的 MCP 服务器。通过构建 **MCP 服务器**，公司和开发者可以让自己的产品轻松为 AI 所用，开辟一条提供价值的新途径。

由于 MCP 是开源的，任何人都可以构建 MCP 服务器或客户端。

## MCP 为什么重要？

MCP 让大语言模型超越聊天，执行真实世界的任务：阅读一封邮件往来并发送回复、访问一个代码库并部署更新，或者审阅一份设计简报并生成初稿。该协议为大语言模型连接外部系统、工具和应用以访问数据、采取行动奠定了基础。这带来：

### AI 的通用兼容性

**AI 助手获得数千种工具的访问能力** —— 一旦某个 AI 助手实现了 MCP（通过 MCP 客户端），它就能立即连接到数千个与 MCP 兼容的应用，从专业编码工具到企业工作流平台，而无需为每一个单独构建定制集成。

**工具和应用同时连接所有 AI 助手** —— Notion、Figma、Asana 这样的公司只需构建一个 MCP 服务器，即可与任何兼容的 AI 助手（即实现了 MCP 客户端的助手）协作。开发者只需构建一次集成，即可覆盖所有 AI 连接。

### 开放的 AI 原生生态

**任何人都可以构建和分享** —— 作为一项开放标准，开发者或公司发布的 MCP 服务器与任何 MCP 客户端兼容。这种开放性催生了一个由数千个社区构建服务器组成的繁荣生态，加速了 AI 助手可用工具和应用的增长。

**让软件天生对 AI 可访问** —— 传统软件是为使用网页界面的人类而构建的。MCP 提供了一个为 AI 交互设计的并行接口，让应用真正成为 AI 原生。这意味着 AI 模型与人们已在使用的工具之间，能有更好、更可靠的集成。

### 智能体的基础协议

MCP 为 AI 智能体访问任意数量的服务和工具创造了基础设施，实现真正的端到端任务自动化。随着越来越多的应用采用该协议，AI 智能体能够独立处理复杂多步工作流的愿景正变得越来越现实。

## MCP 是为谁设计的？

开发者获得了一种标准化的方式：只需构建一次集成，就能与任何兼容的 AI 协作。企业获得安全、由 IT 掌控、可在整个组织内扩展的 AI 连接能力。消费者则可以把自己的常用工具立即接入 AI，无需任何技术知识。

### 面向开发者：连接 AI 与应用的统一标准

开发者只需遵循一个标准，就能把外部产品接入你的 AI 应用和智能体。这简化了构建集成的过程，扩大了可供连接的产品数量，并提升了生态中连接的整体质量与安全性。

你在构建一个要连接许多应用的智能体？还是在构建一个要连接许多智能体的应用？MCP 让你以精简的集成方式接入一个由兼容工具组成的生态。

### 面向企业：覆盖全组织的安全、可扩展 AI 连接

由于 MCP 简化了把你的系统接入 AI 的过程，企业可以更有效地推动内部采用 AI 工具和应用。这有助于让 AI 在你的组织内更深度地连接，为其员工扩展 AI 的能力与实用性。

### 面向消费者：即刻访问你的常用工具

MCP 为最终用户在他们喜爱的 AI 助手和工作工具之间提供了无缝连接。它让任务自动化更容易，也免去了跨标签页复制粘贴的麻烦。简而言之，MCP 让 AI 更深度地接入你的世界。

在 [Claude](https://claude.ai) 中，你可以立即连接到 MCP 服务器，即[**连接器（Connectors）**](https://claude.com/partners/mcp)。这为你提供了一条把 Claude 连接到你常用办公应用的直接途径。

## 连接器（MCP）实战

当你在自己已在使用的工具上看到 MCP 实际运作时，它的真正价值就显而易见了。以下是一些 MCP 为 Claude 中的集成提供动力的例子，这些集成被称为**连接器（Connectors）**：

### Claude 中的 Canva

Canva 连接器让 Claude 可以直接在 Canva 中生成新设计。借助 MCP，Claude 可以连接到 Canva 提供的工具，在画布上生成设计。

### Claude 中的 Notion 和 Linear

通过 Notion 和 Linear 连接器，Claude 可以访问你在 Notion 中的页面，并用它们更新 Linear 中的工单。在这里，MCP 实现了把非结构化上下文无缝转换成另一个项目管理系统中有序工单的过程。

### Claude Code 中的 Figma

Figma 连接器让 Claude 可以访问 Figma 中的设计。这使 Claude Code 能够基于在 Figma 中创建的设计，制作网站、应用或用户界面可运行的原型。

### 可用的 Claude 连接器

Claude 连接器包括以下集成：

- **Notion**——工作区文档
- **Linear**——问题跟踪
- **Stripe**——支付数据
- **Canva** 与 **Figma**——设计辅助
- **Hubspot**——CRM 任务自动化
- **Sentry**——错误跟踪
- ……以及更多

每个连接器只需几秒钟即可完成配置，成为 Claude 工作上下文的一部分。在 Claude 之外，[开源 MCP Registry](https://modelcontextprotocol.io)上还有一个 MCP 服务器生态。

## 开始探索 MCP

根据你的需求，有两条路径可选。

### Claude 中的连接器

[连接器](https://claude.com/partners/mcp)是预先构建好的，让 Claude 即刻访问工具、数据库和应用，也为你提供一整套新能力。打开 [Claude](https://claude.ai/directory)，浏览可用的连接器，点击即可添加。

### 构建自定义 MCP 连接

MCP 是开源的，也就是说任何人都可以采用 MCP 来连接 AI 与应用。[模型上下文协议文档](https://modelcontextprotocol.io)详细讲解了如何基于 MCP 进行构建。

## 开始使用

如果你想尝试 MCP，可以先浏览找一个能立即与 Claude 一起使用的 Claude 连接器。

如果还不存在现成的 MCP 服务器，自己创建一个需要一些工作量，但只要你懂 TypeScript 或 Python，就不算太复杂。[模型上下文协议快速入门](https://modelcontextprotocol.io/quickstart)提供了可以按需修改的可用示例。

FAQ（常见问题）

不是。MCP 是一个开源协议。虽然 Claude 率先采用了 MCP，但其他 AI 提供商现在也已采用同一协议，任何人都可以连接到同一个 MCP 服务器生态。

使用[连接器](https://claude.com/partners/mcp)不需要。浏览、安装、完成认证，就这样。构建自定义 MCP 服务器则需要 TypeScript 或 Python 知识，但不断壮大的[连接器库](https://claude.com/partners/mcp)已覆盖大多数主流工具。

每个服务器都会申请特定权限，以允许 Claude 访问它。你可以批准或拒绝访问，并随时撤销权限。

MCP 使用高效的协议。本地服务器采用的 stdio 传输开销极小；远程服务器采用的服务器推送事件（SSE）和可流式 HTTP（Streamable HTTP）可维持持久连接。响应流式传输可避免大数据操作超时。该协议还支持分页、过滤和部分响应，以高效处理大规模数据集。
