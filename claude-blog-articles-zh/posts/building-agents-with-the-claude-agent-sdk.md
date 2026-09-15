---
title: "使用 Claude Agent SDK 构建智能体"
title_en: "Building agents with the Claude Agent SDK"
source: https://claude.com/blog/building-agents-with-the-claude-agent-sdk/
crawled: 2026-09-14
translated: 2026-09-14
---

# 使用 Claude Agent SDK 构建智能体

> 原文：[Building agents with the Claude Agent SDK](https://claude.com/blog/building-agents-with-the-claude-agent-sdk/) · Claude 博客

去年，我们与客户一起分享了[构建高效智能体](https://www.anthropic.com/engineering/building-effective-agents)的经验。此后，我们发布了 [Claude Code](https://claude.com/product/claude-code)——一个智能体编码解决方案，最初是为了提升 Anthropic 内部开发者的生产力而构建的。

过去几个月里，Claude Code 早已不只是一个编码工具。在 Anthropic 内部，我们一直[在用它](https://www.anthropic.com/news/how-anthropic-teams-use-claude-code)做深度研究、视频创作和记笔记，以及其他数不清的非编码应用。事实上，它已经开始支撑我们几乎所有主要的智能体循环。

换句话说，[驱动 Claude Code 的智能体执行框架（harness）](https://claude.com/blog/harnessing-claudes-intelligence)（即 Claude Code SDK）同样可以驱动许多其他类型的智能体。为了体现这一更宏大的愿景，我们将把 Claude Code SDK 更名为 Claude Agent SDK。

在本文中，我们将说明我们为什么要构建 Claude Agent SDK、如何用它构建你自己的智能体，并分享我们的团队在实际部署中总结出的最佳实践。

## 给 Claude 一台电脑

Claude Code 背后的[关键设计原则](https://www.youtube.com/watch?v=vLIDHi-1PVU)是：Claude 需要拥有与程序员日常使用的相同的工具。它需要能够在代码库中找到合适的文件、写入和编辑文件、对代码进行 lint、运行代码、调试、再编辑，有时还要迭代地执行这些操作，直到代码成功运行为止。

我们发现，让 Claude 通过终端访问用户的计算机之后，它就具备了像程序员那样编写代码所需的一切。

但这也让 Claude Code 中的 Claude 在*非*编码任务上同样高效。通过为它提供运行 bash 命令、编辑文件、创建文件和搜索文件的工具，Claude 可以读取 CSV 文件、搜索网络、构建可视化、解读指标，完成各种其他数字化工作——简而言之，就是给智能体一台电脑，打造通用型智能体。Claude Agent SDK 背后的关键设计原则，就是给你的智能体一台电脑，让它们像人类一样工作。

## 创造新型智能体

我们相信，给 Claude 一台电脑，将解锁构建比以往更高效的智能体的能力。例如，借助我们的 SDK，开发者可以构建：

- **金融智能体**：构建能够理解你的投资组合和目标的智能体，并通过访问外部 API、存储数据和运行代码进行计算，帮助你评估投资。
- **个人助理智能体**。构建能够帮你预订差旅、管理日历的智能体，并通过连接你的内部数据源、跨应用追踪上下文，完成安排预约、整理简报等更多工作。
- **客户支持智能体**：构建能够处理高模糊度用户请求（如客服工单）的智能体，通过收集和审阅用户数据、连接外部 API、回复用户消息，并在必要时升级转人工处理。
- **深度研究智能体**：构建能够跨大型文档集合开展全面研究的智能体，通过搜索文件系统、分析和综合来自多个来源的信息、跨文件交叉核对数据，并生成详尽的报告。

还有更多可能。SDK 的核心，是为你提供构建智能体的基础组件（primitives），帮你自动化任何想自动化的工作流。

## 构建你的智能体循环

在 Claude Code 中，Claude 通常在一个特定的反馈回路中运行：收集上下文 -> 采取行动 -> 验证工作 -> 重复。

智能体通常在一个特定的反馈回路中运行：收集上下文 -> 采取行动 -> 验证工作 -> 重复。

这为我们思考其他智能体以及应当赋予它们哪些能力提供了一个有用的视角。为了说明这一点，我们将以如何在 Claude Agent SDK 中构建一个邮件智能体为例进行讲解。

## 收集上下文

开发智能体时，你希望给它的不只是一个提示：它还需要能够自行获取和更新上下文。以下是 SDK 中的各项功能可以提供的帮助。

### **智能体搜索与文件系统**

文件系统代表着*可能*被拉入模型上下文的信息。

当 Claude 遇到大型文件（如日志或用户上传的文件）时，它会使用 `grep`、`tail` 等 bash 脚本来决定以何种方式将这些内容加载进上下文。从本质上讲，智能体的文件夹和文件结构本身就构成了一种[上下文工程](http://anthropic.com/news/context-management)。

我们的邮件智能体可能会把此前的对话存储在一个名为 "Conversations" 的文件夹中。这样，当被问及相关内容时，它就可以检索这些对话来获取上下文。

### **语义搜索**

[语义搜索](https://www.anthropic.com/news/contextual-retrieval)通常比智能体搜索更快，但准确性更低、维护难度更大、透明度也更低。它需要先对相关上下文进行「分块」（chunking），把这些分块嵌入为向量，然后通过查询这些向量来检索相关概念。鉴于其局限性，我们建议从智能体搜索入手，只有当你需要更快的结果或更多样的检索方式时，再引入语义搜索。

### **子智能体**

Claude Agent SDK 默认支持子智能体（subagent）。[子智能体](https://docs.claude.com/en/api/agent-sdk/subagents)之所以有用，主要有两个原因。首先，它们支持并行化：你可以同时启动多个子智能体处理不同任务。其次，它们有助于管理上下文：子智能体使用各自隔离的上下文窗口，只把相关信息回传给编排器，而不是其完整上下文。这使它们非常适合那些需要从海量信息中筛选、而大部分信息并无用处的任务。

在设计我们的邮件智能体时，我们可以赋予它「搜索子智能体」的能力。这样，邮件智能体就可以并行启动多个搜索子智能体——每个子智能体针对你的邮件历史运行不同的查询——并让它们只返回相关摘录，而不是完整的邮件串。

### **压缩（compaction）**

当智能体长时间运行时，上下文维护就变得至关重要。Claude Agent SDK 的压缩功能会在接近上下文上限时自动总结之前的消息，从而避免你的智能体耗尽上下文。这一功能构建自 Claude Code 的 [compact 斜杠命令](https://docs.claude.com/en/docs/claude-code/sdk/sdk-slash-commands#%2Fcompact-compact-conversation-history)。

## 采取行动

收集完上下文之后，你就要为智能体提供灵活多样的行动方式。

### **工具**

[工具](https://www.anthropic.com/engineering/writing-tools-for-agents)是智能体执行环节的主要构件。工具在 Claude 的上下文窗口中占据显著位置，是 Claude 决定如何完成任务时首要考虑的行动。这意味着你应该慎重设计工具，以最大化上下文效率。更多最佳实践请参阅我们的博客文章[《为智能体编写高效工具——用智能体来写》](https://www.anthropic.com/engineering/writing-tools-for-agents)。

因此，你的工具应当对应你希望智能体执行的主要动作。了解如何在 Claude Agent SDK 中[创建自定义工具](https://docs.claude.com/en/api/agent-sdk/custom-tools)。

对于我们的邮件智能体，我们可以把 `fetchInbox`、`searchEmails` 这样的工具定义为该智能体最主要、最高频的动作。

### **Bash 与脚本**

bash 是一种通用工具，可以让智能体借助计算机灵活地完成各种工作。

在我们的邮件智能体中，用户的重要信息可能存放在附件里。Claude 可以编写代码来下载 PDF、将其转换为文本，然后进行全文检索以找到有用信息，如下方所示：

### **代码生成**

Claude Agent SDK 在代码生成方面表现出色——这是有充分理由的。代码精确、可组合、可无限复用，对于需要可靠执行复杂操作的智能体来说，代码是理想的输出形式。

在构建智能体时，请思考：哪些任务适合用代码来表达？答案往往能解锁可观的扩展能力。

例如，我们近期推出的 [Claude.AI 文件创建](https://www.anthropic.com/news/create-files)功能就完全依赖代码生成。Claude 编写 Python 脚本来创建 Excel 电子表格、PowerPoint 演示文稿和 Word 文档，确保了格式的一致性和复杂功能的实现——这些用其他方式很难做到。

在我们的邮件智能体中，我们可能希望允许用户为收到的邮件创建规则。为此，我们可以编写代码，在相应事件发生时执行。

### **MCP**

[Model Context Protocol](https://modelcontextprotocol.io/)（MCP）为外部服务提供标准化的集成方式，自动处理身份验证和 API 调用。这意味着你可以把智能体连接到 Slack、GitHub、Google Drive 或 Asana 等工具，而无需自己编写定制集成代码或管理 OAuth 流程。

对于我们的邮件智能体，我们可能希望 `search Slack messages`（搜索 Slack 消息）来了解团队上下文，或者 `check Asana tasks`（查看 Asana 任务）来确认是否已有人被指派处理某个客户请求。借助 MCP 服务器，这些集成开箱即用——你的智能体只需调用 search_slack_messages 或 get_asana_tasks 这类工具，剩下的都由 MCP 处理。

不断成长的 [MCP 生态](https://github.com/modelcontextprotocol/servers)意味着，随着预构建集成的不断涌现，你可以快速为智能体添加新能力，从而专注于智能体行为本身。

## 验证工作

Claude Code SDK 通过评估自身工作来闭合智能体循环。能够检查并改进自身输出的智能体在根本上更加可靠——它们能在错误累积之前发现问题，在偏离方向时自我纠正，并在迭代中不断进步。

关键在于给 Claude 提供评估其工作的具体手段。以下是我们发现行之有效的三种方法：

### **定义规则**

最好的反馈形式是：为输出明确定义规则，然后说明哪些规则未通过以及原因。

[代码 lint](https://stackoverflow.com/questions/8503559/what-is-linting) 是一种极佳的基于规则的反馈。反馈越深入越好。例如，生成 TypeScript 并对其进行 lint，通常优于生成纯 JavaScript，因为前者能为你提供多个额外的反馈层面。

在生成邮件时，你可能希望 Claude 检查邮箱地址是否有效（无效则抛出错误），以及用户此前是否给对方发过邮件（如果发过，则抛出警告）。

### **视觉反馈**

当使用智能体完成视觉类任务（如 UI 生成或测试）时，视觉反馈（以截图或渲染图的形式）会很有帮助。例如，如果要发送一封带 HTML 格式的邮件，你可以对生成的邮件截图，再把它返回给模型进行视觉验证和迭代打磨。模型随后会检查视觉输出是否符合要求。

例如：

- **布局** - 各元素位置是否正确？间距是否合适？
- **样式** - 颜色、字体和格式是否如预期呈现？
- **内容层级** - 信息是否以正确的顺序呈现、重点是否得当？
- **响应式表现** - 看起来是否有破版或过于拥挤？（不过单张截图所能提供的视口信息有限）

借助 Playwright 这样的 MCP 服务器，你可以将这一视觉反馈回路自动化——对渲染后的 HTML 截图、捕捉不同视口尺寸，甚至测试交互元素——全部在智能体的工作流内完成。

来自大语言模型（LLM）的视觉反馈可以为你的智能体提供有益的指引。

### **以 LLM 为评判（LLM as a judge）**

你也可以让另一个语言模型基于模糊规则来「评判」智能体的输出。这种方法通常不够稳健，且可能带来较大的延迟代价，但对于那些性能上任何提升都值得付出成本的应用场景，它仍有帮助。

我们的邮件智能体可以让另一个单独的子智能体来评判草稿的语气，看其是否与用户以往的消息风格相符。

## 测试并改进你的智能体

在完整跑过几轮智能体循环之后，我们建议对智能体进行测试，确保它为任务配备了足够的装备。改进智能体的最佳方式是仔细审视它的输出，尤其是它失败的场景，并站在它的角度思考：它是否拥有完成任务所需的[合适工具](https://www.anthropic.com/engineering/writing-tools-for-agents)？

在评估你的智能体是否具备完成任务的充分条件时，还可以问自己以下问题：

- 如果智能体误解了任务，它可能缺少关键信息。你能否调整搜索 API 的结构，让它更容易找到所需的信息？
- 如果智能体在某项任务上反复失败，你能否在工具调用中加入一条正式规则来识别并修复该失败？
- 如果智能体无法自行修复错误，你能否为它提供更实用或更有创意的工具，让它换一种思路解决问题？
- 如果随着功能增加，智能体的表现出现波动，可以基于客户使用情况构建一个有代表性的测试集，用于程序化评估（即 eval）。

## 开始使用

Claude Agent SDK 让 Claude 可以访问一台计算机，在其中写入文件、运行命令并迭代改进自己的工作，从而让自主智能体的构建变得更加容易。

记住智能体循环（收集上下文、采取行动、验证工作），你就能构建出可靠且易于部署和迭代的智能体。

你可以从今天开始[上手](https://docs.claude.com/en/api/agent-sdk/overview) Claude Agent SDK。已经在使用该 SDK 进行开发的开发者，我们建议按照[这份指南](https://docs.claude.com/en/docs/claude-code/sdk/migration-guide)迁移到最新版本。

## 致谢

本文由 Thariq Shihipar 撰写，Molly Vorwerck、Suzanne Wang、Alex Isken、Cat Wu、Keir Bradwell、Alexander Bricken 和 Ashwin Bhat 提供了注释与编辑。

FAQ（常见问题）
