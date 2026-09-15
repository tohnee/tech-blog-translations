---
title: "Codex 作为平台：在开放的智能体执行框架上构建"
title_en: "Codex as a platform: build on the open agent harness"
source: https://developers.openai.com/blog/codex-as-a-platform/
crawled: 2026-09-14
translated: 2026-09-14
---

# Codex 作为平台：在开放的智能体执行框架上构建

> 原文：[Codex as a platform: build on the open agent harness](https://developers.openai.com/blog/codex-as-a-platform/) · OpenAI 开发者博客

大多数人通过[应用（App）](https://developers.openai.com/codex/app)、[命令行界面（CLI）](https://developers.openai.com/codex/cli)或 [IDE 扩展](https://developers.openai.com/codex/ide)认识 Codex。这些体验很重要，但它们只是同一底层系统的几种使用方式而已。

为所有这些体验提供支撑的，是[开源的 Codex 执行框架（harness）](https://github.com/openai/codex)。它帮助模型收集上下文、对任务进行推理、使用工具、在配置好的边界内运作、请求批准，并把工作向前推进。

这改变了开发者能够构建的东西。你不必要求每个团队把自己的工作迁移到一个通用的编程助手里，而是可以把智能体带入围绕实际工作设计的软件中：一个工程工作流、一个运维仪表盘、一次安全调查、一个客服控制台，或为某个专门团队打造的内部应用。

## 可复用的部分是智能体循环

一个有能力的智能体不只是「一个提示词加一个模型响应」。它需要一种方式来理解任务、随时间维护上下文、检查相关信息、调用工具、展示进度、处理失败、在必要时请求人类批准，并返回有用的结果。

这个围绕四周的执行系统就是执行框架（harness）。

执行框架的设计能实质性地改变结果：在 [ARC-AGI-3](https://openai.com/index/how-two-settings-tripled-our-arc-agi-3-scores/) 上，保留推理与上下文压缩（compaction）把 GPT-5.6 Sol 的得分从 13.3% 提升到 38.3%，同时把输出 token 减少到原来的六分之一。

我们构建 Codex 执行框架，是为了管理会话状态、流式执行、使用工具、强制执行配置好的沙箱与批准策略，并把工作跨越多轮向前推进。通过 [Codex app-server](https://developers.openai.com/codex/app-server)，我们以一份有文档的客户端协议暴露这些能力：应用可以创建线程（thread）、开始回合（turn）、接收事件、处理批准请求。

如果你在构建需要智能体的软件，你可以从 Codex 出发，而不必发明一个新的运行时，然后再决定周围的应用应该拥有什么。

## 一个开发者可以检视与改造的开放执行框架

由于执行框架是开源的，你可以检视应用与模型之间的那一层，理解它的行为，并调整集成方式以适配你的产品。

这让开发者能够掌控那些让智能体契合其产品的部分：

- 界面。团队可以保留现有的仪表盘、编辑器、队列、地图、记录与审批流，而不必把每一次交互都塞进一个通用的聊天窗口。
- 上下文与工具。应用可以暴露对特定工作流重要的系统、文档、数据与操作，包括应用自有的 [MCP 服务](https://developers.openai.com/codex/extend/mcp)。
- 运营边界。宿主应用可以决定智能体在哪里运行、它可以访问哪些文件或工具、哪些操作需要批准、工作如何被观察，以及结果如何返回到记录系统（system of record）。

我们将 [Codex CLI](https://developers.openai.com/codex/cli)、[app-server](https://developers.openai.com/codex/app-server) 与[官方 Codex SDK](https://developers.openai.com/codex/codex-sdk) 作为开源组件发布。我们的[开源组件指南](https://developers.openai.com/codex/open-source)列出了可用的组件以及每个组件所在的位置。

开源层是执行框架与集成面；模型访问与托管服务保持独立。

## 选择合适的集成层

基于 Codex 构建，并不意味着每个用例都要用同一种集成方式。

- 对于脚本、CI 任务或一次性的后台任务，[codex exec](https://developers.openai.com/codex/non-interactive-mode) 可以运行一个有边界的智能体工作流并返回结构化输出。
- 对于需要启动、恢复或流式传输 Codex 任务的应用代码，[官方 Codex SDK](https://developers.openai.com/codex/codex-sdk) 提供了直接的编程接口。

可运行的示例参见 [Codex SDK 文档](https://learn.chatgpt.com/docs/codex-sdk)。

当智能体本身就是产品的一部分时，请使用 Codex app-server。它让你的应用连接到本地的 Codex 进程、保持会话开启、流式接收事件、中断工作、暴露工具，并响应批准请求。SDK 简化了常见的编程工作流；app-server 则让产品团队直接掌控生命周期与用户体验。

## 围绕工作流构建软件

最有趣的机会不是给 Codex 应用换个 logo 复刻一遍，而是构建能够反映某个特定的人或团队既有工作方式的软件：

一位安全分析师可能需要调查队列、近期警报、受影响的服务，以及在开出修复工单之前的批准环节。一位支持工程师可能需要账户历史、产品日志、内部文档和一份回复草稿。一个产品团队可能希望有一个任务板：把某个 issue 移动到「就绪」状态，就会启动一个范围受限的实现工作流。

在每个例子里，界面都是体验的重要组成部分。它告诉智能体用户正在看什么，为它提供合适的工具，并为用户提供一个可以审视后续进展的地方。

图 1. 你的应用拥有产品上下文、业务规则与工具；Codex app-server 提供智能体循环与沙箱化执行。

## 示例：Relay

我们基于 Codex app-server 构建了 Relay，作为运维类示例应用。它把一个智能体放在一个虚构的货运仪表盘旁边，把它连接到应用自有的 MCP 工具，并要求在重新预订（rebook）货物之前获得人类批准。

用户不必从零开始写提示词。他们选中一个货运单，然后点击诸如 **Compare recovery（比较恢复方案）** 的操作。应用提供相关上下文，Codex 拉取最新的示例运营数据，智能体解释可用的选项，而任何有实质影响的写入操作都需要批准。

Codex 随后可以使用应用的 MCP 工具获取当前数据，然后再推荐某个操作——或者在获得批准之后执行它。当某个工具改变了底层记录时，应用会刷新其业务视图。执行框架负责智能体循环、会话状态、流式活动与工具交互；产品继续拥有自己的仪表盘、记录与控件。

Relay 使用的是虚构的种子数据，但这种集成模式是通用的。同样的模式可以支撑事件响应、账户运营、研究工作流，或其他需要智能体在既有产品体验中工作的应用。

图 2. Relay 把 Codex 嵌入货运运营仪表盘，配备应用自有的 MCP 工具，并对有实质影响的操作要求人类批准。

## 开发者们正在构建什么

这一模式已经出现在公开的实现中：

- [GitHub 与 JetBrains](https://github.blog/changelog/2026-07-07-codex-as-agent-provider-and-agentic-enhancements-in-jetbrains-ides/) 把 Codex 带入现有的 IDE 工作流。
- [Cisco](https://blogs.cisco.com/ai/from-an-idea-to-a-live-app-on-cisco-in-minutes) 在 Cisco Cloud Control 的 App Builder 中使用 Codex SDK。
- [Thrive Holdings 与 Crete](https://openai.com/index/building-self-improving-tax-agents-with-codex/) 在一个融入从业者反馈的报税工作流中使用 Codex。他们的试点处理了 7,000 份申报表，并把准备时间缩短了约三分之一。

这些例子并不局限于工程领域：同样的模式适用于调查客户问题的支持团队、协调工作流的运营团队、分诊安全事件的安全团队、研究客户账户的销售团队，以及策划营销活动的市场团队。在每种情况下，应用都提供上下文、工具与批准环节，而 Codex 为底层智能体循环提供动力。

## 超越显而易见去构建

对许多类型的工作来说，关键上下文都根植于一个仪表盘、一条时间线、一张地图、一份文档或一条系统记录之中。这些视图不是为了好看：它们正是人们真正理解正在发生什么、做出决策并保持掌控的方式。

机会不在于用一个万能聊天框取代这些界面，而在于赋予它们一个智能体——能够理解工作、调查正确的上下文、提出下一步建议并执行已获批准的操作——从而让这些界面更加强大。

Codex 应用、CLI 与 IDE 扩展展示了执行框架能做什么。通过将执行框架开源，我们为开发者提供了一条路径：检视这些能力、集成它们，并把它们适配到自己的产品与工作流中。

如果你想基于 Codex 执行框架构建，请从[开源的 Codex 仓库](https://github.com/openai/codex)开始，然后选择适合你产品的集成方式：非交互式任务用 [codex exec](https://developers.openai.com/codex/non-interactive-mode)，编程式智能体工作流用 [Codex SDK](https://developers.openai.com/codex/codex-sdk)，需要持久会话、流式事件与批准处理的应用用 [Codex app-server](https://developers.openai.com/codex/app-server)。
