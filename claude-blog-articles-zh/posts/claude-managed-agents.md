---
title: "Claude Managed Agents：以 10 倍速度进入生产环境"
title_en: "Claude Managed Agents: get to production 10x faster"
date: 2026-04-08
source: https://claude.com/resources/articles/claude-managed-agents
crawled: 2026-11-17
translated: 2026-11-17
---

# Claude Managed Agents：以 10 倍速度进入生产环境

> 原文：[Claude Managed Agents: get to production 10x faster](https://claude.com/resources/articles/claude-managed-agents) · Claude 博客

宣布推出 Claude Managed Agents——Anthropic 全新的一套可组合 API，用于大规模构建和部署云端托管的智能体。

## Claude Managed Agents 是什么

Claude Managed Agents 是一套可组合 API，用于大规模构建和部署云端托管的智能体。它将 Anthropic 托管的执行框架与生产级基础设施相结合，提供状态、记忆、权限和[定时执行](https://claude.dev/blog/building-effective-agent-automations/)能力。

在今天的发布之前，构建智能体意味着把开发周期花在安全基础设施、状态管理、权限配置上，而且每次模型升级都要重做智能体循环。Managed Agents 把经过性能调优的智能体执行框架与生产基础设施结合在一起，让从原型到上线的时间从几个月缩短到几天。

无论你构建的是单任务执行器还是[复杂的多智能体流水线](https://claude.com/resources/articles/building-agents-when-to-fold-subagents-into-your-main-agent-loop)，都可以专注于用户体验，而不是运维负担。

Managed Agents 即日起在 Claude Platform 上公开 beta。

## **以 10 倍速度构建和部署智能体**

交付一个生产级智能体需要沙箱化的代码执行、检查点、凭据管理、作用域权限和端到端追踪。在用户看到任何东西之前，这就是数月的基础设施工作。

Managed Agents 处理这些复杂性。你定义智能体的任务、工具和防护栏，我们负责在我们的基础设施上运行它。内置的编排执行框架决定何时调用工具、如何管理上下文以及如何从错误中恢复。

Managed Agents 包括：

* **生产级智能体**：安全沙箱、身份认证和工具执行都由平台代劳。
* **长时间运行的会话**：可自主运行数小时，进度和输出即使在连接中断后也能保留。
* **多智能体协同**：智能体可以创建并指挥其他智能体，将复杂工作并行化（*研究预览*阶段，[在此申请](http://claude.com/form/claude-managed-agents)）。
* **可信治理**：让智能体访问真实系统，内置作用域权限、身份管理和执行追踪。

![](https://assets.claude.com/08b6a06365ef3624bef93f9cdcff4b29e80ad7f2.png)

Claude Managed Agents 架构

## **为充分发挥 Claude 的能力而设计**

Claude 模型是为智能体工作而构建的。Managed Agents 专为 Claude 量身打造，让你以更少的投入获得更好的智能体结果。

使用 Managed Agents，你定义结果和成功标准，Claude 会自我评估并迭代，直到达成目标（*研究预览*阶段，[在此申请](http://claude.com/form/claude-managed-agents)）。当你需要更强的控制时，它也支持传统的提示-响应式工作流。

在围绕结构化文件生成的内部测试中，Managed Agents 相比标准的提示循环使结果导向任务的成功率最高提升了 10 个百分点，在最难的问题上提升最大。

会话追踪、集成分析和故障排查指引直接内置于 Claude Console，让你可以检查每一次工具调用、决策和失败模式。

## **各团队正在构建什么**

各团队已经在多种生产用例中借助 Managed Agents 以 10 倍速度交付。有的编程智能体会读取代码库、规划修复方案并提交 PR；有的效率智能体会加入项目、领取任务，与团队其他成员并肩交付工作；还有的财务与法务智能体处理文档并提取关键信息。每种情况下，以天为单位的交付都意味着更快地为用户提供价值。

* [**Notion**](https://claude.com/customers/notion-qa) 让团队直接在自己的工作区内把工作委派给 Claude（目前已作为 Notion Custom Agents 中的私有 alpha 可用）。工程师用它交付代码，知识工作者用它生成网站和演示文稿。数十个任务可以并行运行，同时整个团队在产出上协作。
* [**Rakuten**](https://claude.com/customers/rakuten-qa) 在产品、销售、市场和财务等条线交付了接入 Slack 和 Teams 的企业级智能体，让员工可以分派任务，并拿回电子表格、幻灯片和应用等交付物。每个专家智能体的部署都在一周内完成。
* [**Asana**](https://claude.com/customers/asana-qa) 构建了 AI Teammates——在 Asana 项目内与人类并肩工作的协作式 AI 智能体，承担任务并起草交付物。该团队借助 Managed Agents 添加高级功能，速度远超其他方式。
* [**Vibecode**](https://claude.com/customers/vibecode) 帮助客户从提示直达已部署的应用，把 Managed Agents 作为默认集成，驱动新一代 AI 原生应用。用户现在能以至少 10 倍于以往的速度搭建同样的基础设施。
* [**Sentry**](https://claude.com/customers/sentry) 将他们的调试智能体 Seer 与一个由 Claude 驱动、负责写补丁并提交 PR 的智能体配对，让开发者从被标记的 bug 到可审阅的修复在同一流程中完成。在 Managed Agents 上，这个集成的交付只用了数周而非数月。

[Anthropic 自己的销售团队也在用它处理入库线索](https://claude.com/resources/articles/how-anthropics-sales-team-rebuilt-inbound-with-claude-managed-agents)。

![Atlassian](https://assets.claude.com/4870b3d6c0253cea01b100c98ad2030b8e4f8ce1.svg)

> "Atlassian 帮助企业编排人与智能体协同的工作。借助 Claude Managed Agents，我们能在数周而非数月内把面向开发者的智能体直接构建进团队已经依赖的工作流，让客户可以直接在 Jira 里分派任务。Managed Agents 处理了沙箱、会话和作用域权限这些难啃的部分，这意味着我们的工程师可以少花时间在基础设施上，多花时间为最终用户构建出色的功能。"

Sanchan Saxena，Teamwork Collection 高级副总裁、产品负责人

![General Legal](https://assets.claude.com/cdec3718a68a04655d28ce94cd0118bbe12d7f02.svg)

> "使用 Claude Managed Agents，我们构建了一个能从用户的文档和往来信函中提取信息、回答他们提出的任何查询的系统，即使我们没有为此专门构建数据检索工具。在 Managed Agents 之前，我们必须预判用户可能想问的每一个问题，并为每个问题构建工具或提示工作流。现在有了 Managed Agents，它可以在运行时现场编码出所需的任何工具，从而处理几乎任何用户查询。这把开发时间缩短了 10 倍，让我们可以专注于用户体验和集成更多数据源。"

Javed Qadrud-Din，CTO

![Blockit](https://assets.claude.com/3cae7291e5befcd2bc2ef5f1281ce3daf4cf6e38.svg)

> "Claude Managed Agents 让构建生产就绪的会议准备智能体快了 3 倍。我们从想法到上线只用了几天。我们的智能体会在会议前研究每一位参与者，找出推动对话前进的关键信息。自定义工具让我们可以接入自己的日历和联系人数据，MCP 让连接会议记录工具、CRM 等外部系统变得简单，而托管执行框架承担了繁重的工作，包括沙箱化执行和内置的网页搜索。让我们可以专注于构建产品，而不是基础设施。"

John Han，联合创始人

![Notion](https://assets.claude.com/19e0cdfaef9d2980bddd19cd993076d62b46c0c7.svg)

> "我们希望 Notion 成为团队与智能体协作完成工作的最佳场所。为此我们集成了 Claude Managed Agents，它可以处理长时间运行的会话、管理记忆，并随时间推移持续交付高质量产出。我们的用户现在可以委派开放式、复杂的任务——从写代码到生成幻灯片和电子表格——而无需离开 Notion。"

Eric Liu，产品经理

![Rakuten](https://assets.claude.com/5463fa5a44d12868ceec5ae30bfc8c412cafdeae.svg)

> "借助 Claude Managed Agents，我们的高级用户就像伽利略一样，跨领域贡献，远远超出单一专业或学科的边界。我们在一周内部署每个专家智能体，在沙箱环境中管理横跨工程、产品、销售、市场和财务的长时任务，生成应用、提案演示文稿和电子表格。随着智能体能力增强，Managed Agents 让我们能够安全地扩展，而无需自建智能体基础设施，从而可以完全专注于让创新在公司内部普惠化。"

Yusuke Kaji，AI for Business 总经理

![Asana](https://assets.claude.com/b8ffecd4a133f2860151d51156002816a54772e7.svg)

> "Claude Managed Agents 大幅加速了 Asana AI Teammates 的开发——帮助我们更快交付高级能力——并让我们腾出手来专注于打造企业级多人协作体验。"

Amritansh Raghav，CTO

![Vibecode](https://assets.claude.com/5f87469e4a2c00123682d8b35785892ff55bd4f4.svg)

> "在 Claude Managed Agents 之前，用户得手动在沙箱中运行 LLM、管理其生命周期、为它们配备合适的工具，并监督其执行，整个过程可能需要数周乃至数月来搭建。现在，只需几行代码，用户就能以至少 10 倍于以往的速度搭建同样的基础设施。这让开发者和 vibe coder 都能构建更多东西。我们将看到 Web 和移动端涌现大量 AI 原生应用。"

Ansh Nanda，联合创始人

![Sentry](https://assets.claude.com/410f375f04040180bb6545e287b4ad178b0d7767.svg)

> "事实证明，光告诉开发者代码哪里有问题还不够：他们还希望你来修。客户现在可以从 Seer 的根本原因分析，直接交给一个由 Claude 驱动、负责写修复并提交 PR 的智能体。我们选择 Claude Managed Agents，是因为它提供了一个安全、完全托管的智能体运行时，让我们能把精力集中在围绕这一交接打造无缝的开发者体验上。Managed Agents 不仅让我们在数周而非数月内完成了初始集成，还消除了维护定制智能体基础设施的持续运维负担。"

Indragie Karunaratne，AI/ML 工程高级总监

## Claude Managed Agents 的新进展

新能力持续推出。智能体现在可以通过[内置记忆](https://claude.com/resources/articles/claude-managed-agents-memory)跨会话学习，并通过 [dreaming、结果导向（outcomes）和多智能体编排](https://claude.com/resources/articles/new-in-claude-managed-agents)实现自我改进。它们可以在凭据存放于保管库的[定时部署](https://claude.com/resources/articles/whats-new-in-claude-managed-agents)中无人值守地运行，还可以借助[自托管沙箱和 MCP 隧道](https://claude.com/resources/articles/claude-managed-agents-updates)在你自己的安全边界内运行。

## 开始使用

Managed Agents 按用量计费。适用 Claude Platform 的标准 token 价格，此外活跃运行时间按每会话小时 0.08 美元收费。完整定价详见[文档](https://platform.claude.com/docs/en/about-claude/pricing#claude-managed-agents-pricing)。

Managed Agents 现已在 Claude Platform 上可用。阅读我们的[文档](https://platform.claude.com/docs/en/managed-agents/overview)了解更多，前往 [Claude Console](https://platform.claude.com/workspaces/default/agent-quickstart)，或使用我们新的 CLI 部署你的第一个智能体。

开发者还可以使用最新版 Claude Code 和内置的 claude-api Skill 来基于 Managed Agents 构建。只需说 "start onboarding for managed agents in Claude API" 即可开始。
