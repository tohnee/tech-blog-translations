---
title: "三家 YC 创业公司如何用 Claude Code 构建自己的公司"
title_en: "How three YC startups built their companies with Claude Code"
date: 2025-11-17
source: https://claude.com/resources/articles/building-companies-with-claude-code
crawled: 2026-11-17
translated: 2026-11-17
---

# 三家 YC 创业公司如何用 Claude Code 构建自己的公司

> 原文：[How three YC startups built their companies with Claude Code](https://claude.com/resources/articles/building-companies-with-claude-code) · Claude 博客

从拿下政府合同的非技术背景创始人，到单枪匹马做规模化的独立开发者——智能体编码正在改写创业手册。

自 2005 年以来，创业加速器 [Y Combinator](https://www.ycombinator.com/) 已孵化超过 5,000 家公司，合计估值超过 8,000 亿美元，其中包括 Airbnb、Stripe 和 DoorDash 这样的家喻户晓的名字。

如今，像 [Claude Code](https://www.claude.com/product/claude-code) 这样的智能体编码工具，正在从根本上改变 YC 创业公司构建与扩张的方式。创始人现在可以直接在终端里交付产品，把开发周期从数周压缩到数小时，甚至让没有技术背景的创始人也能从第一天起与成熟玩家同台竞争。

我们与三家 YC 创业公司聊了聊，它们展示了这种转变正在发生：

* [HumanLayer](https://www.humanlayer.dev/)（F24）用 Claude Code 构建了整个平台，并开创了上下文工程的实践
* [Ambral](https://www.ambral.com/)（W25）用 Claude Code 和 Claude Agent SDK 构建了由子智能体驱动、足够精细的工作流，用它来规模化 AI 驱动的客户账户管理
* [Vulcan Technologies](https://vulcan-tech.com/)（S25）正在用 Claude Code 处理政府与产业面临的监管复杂性

让我们逐一来看。

## **HumanLayer：从 SQL 智能体到规模化 AI 优先的工程团队**

Dexter Horthy 当时正在构建用于管理 SQL 数据仓库的自主 AI 智能体，他注意到智能体落地面临一个根本性（但也不难理解）的挑战：公司并不放心让 AI 应用在无人监督的情况下执行删表这类敏感操作。

### **一切的起点：产品转向**

这一认识成了 HumanLayer 的核心洞察：任何软件中最有用的功能，往往同时也是风险最高的功能，对于基于 LLM 的非确定性系统尤其如此。

“我们的 MVP 是一个在 Slack 里与人协作的智能体，它能做基础的清理工作，比如删掉任何 90 多天没被查询过的表，”Horthy 解释说。“我们不放心让 AI 应用在无人监督的情况下跑原始 SQL，所以接入了一些基本的人工审批步骤。”

2024 年 8 月，Horthy 做出了 MVP，在旧金山的多家创业公司做了演示，并拿下了第一批付费客户。

这一进展让 HumanLayer 进入了 YC F24 批次，团队全力投入，提供一个 API 和 SDK，让 AI 智能体可以通过 Slack、邮件、短信和其他渠道联系人类，寻求反馈、输入和审批。

2025 年第一季度，HumanLayer 团队做了大量客户探索，与数十个构建 AI 智能体的工程团队交流，发现他们此前没有考虑到的智能体开发闭环中存在一个缺口。

“每个团队都在自己造智能体架构，”Horthy 解释说。“我们意识到，光做一个更好的 API 不够——我们需要帮助建立能让整个生态成熟的模式与原则。”

这促使 Horthy 把他们的经验整理成《[12-Factor Agents: Patterns of reliable LLM applications](https://github.com/humanlayer/12-factor-agents)》。这份指南于 2025 年 4 月发布后迅速传播，综合了他们构建生产级智能体系统的经验，并突出了新兴的上下文工程（context engineering）学科的最佳实践。

### **用 Claude Code 构建一切**

有了这些经验，HumanLayer 团队开始探索其他产品想法与转型方向。

Anthropic 推出 Claude Code 时，Horthy 和团队已经是 Claude 模型用于编码的坚定支持者。他们立刻开始用它来构建这些实验。

“我们所有东西都是用 Claude Code 写的，”Horthy 说。“当 Claude Agent SDK 随 Opus 4 和 Sonnet 4 发布、支持无头（headless）智能体执行时，我们就知道这会是件大事。”

在内部打磨了几个月 Claude Code 工作流之后，Horthy 开始把它们分享给关系密切的创始人朋友。

“让我下定决心全力投入的，是和 BoundaryML（YC W23）的 Vaibhav 一起整天的结对会话，”Horthy 回忆道。“Vaibhav 一开始是怀疑的，但我们花了 7 个小时，交付了正常情况下要 1 到 2 周的工作，他就被说服了。我意识到这套工作流可以适用于其他团队、其他代码库。”

### **构建 CodeLayer：规模化 AI 优先的工程**

如今，HumanLayer 的产品 CodeLayer 帮助团队用 worktrees 和远程云端工作节点并行运行多个 Claude 智能体会话。他们发现了一个关键模式：一旦某位工程师掌握了 Claude Code，其生产力提升如此之大，真正的挑战就变成了组织层面的问题——如何把这些工作流扩展到整个团队。

“一旦你团队里有好几个人在交付 AI 写的代码，你面对的就是完全不同类型的问题，”Horthy 解释说。“这是沟通、协作、工具链和管理的问题。你必须重新设计团队构建软件的一切方式。”

自 2025 年第四季度开始，HumanLayer 已在各种规模的工程团队中完成多个大型试点，部署这些工具与工作流——它们全部是用 Claude Code 构建的。

## **Ambral：用子智能体构建生产系统**

Jack Stettner 和 Sam Brickman 创立 Ambral，是为了解决每一位 B2B 创业公司创始人和 CRO 都熟悉的问题：随着公司扩张，驱动早期增长的、创始人层面的客户亲密关系，变得不可能维持。

### **用 Claude Agent SDK 改造客户账户管理**

无论是在高速增长的早期公司，还是在成熟的企业里，客户经理通常要同时照看 50 到 100 个客户账户。“用一个人注意力的五十分之一，你不可能提供有效的客户账户管理体验，”Stettner 解释说。曾经能装进创始人脑子里的客户上下文，如今散落在各个系统、日志、Slack 消息、会议记录和产品使用数据中。

Ambral 把来自客户活动与互动的信号综合成每个账户的 AI 模型。系统会精确指出谁需要关注以及为什么，自主推动或建议增购，同时捕捉不满的早期迹象以防止流失。

“我们想提供的体验，是每个客户都有一位一对一的客户经理，”Stettner 说。

作为这家年轻创业公司的 CTO 兼唯一的工程师，Stettner 高度依赖 Claude Code 做开发，也依赖 Claude 的 Agent SDK 驱动产品本身。其技术架构反映出他对如何从不同 Claude 模型中榨取最大价值的深入理解。

### **分工式工作流：用 Opus 思考、用 Sonnet 构建，子智能体无处不在**

Stettner 采用了一套精确的工作流，让不同 Claude 模型与子智能体各展所长：

“我用 Opus 4.1 做研究和规划。Sonnet 4.5 在执行我写的这些 Markdown 计划时，表现简直无敌，”Stettner 解释说。

他的开发过程分为三个清晰的阶段：

1. **研究阶段（Opus 4.1）**：针对某个功能实现所需的任何背景，做深度研究。“我认为最重要的是在规划之前先做研究，”Stettner 强调。“让 Claude 替你做研究，产出一份又大又长的研究文档。”他会用一系列子智能体并行研究代码库的多个区域。
2. **规划阶段（Opus 4.1）**：制定一份分阶段的计划，说明如何实现该功能。“我会让 Opus 生成一份分阶段的计划，把实际实现方式拆成一个个明确的阶段，然后我自己去修改这份计划。也许我会和 Opus 讨论某些细节上的问题，或者手动更新这个 markdown 文件。”
3. **实现阶段（Sonnet 4.5）**：系统性地执行计划中的每个阶段。“然后我会用 Sonnet 4.5 去实现每个阶段。”

这套做法胜过 Stettner 尝试过的其他工作流，其中也受到 Horthy 在 HumanLayer 所做工作的影响：“我试过所有编码工具，也几乎试过每一个模型。我只是认为 Anthropic 的模型目前在工具使用上是最好，而这会直接转化为代码能力。”

### **构建强大的研究引擎**

产品本身也映照了这种多智能体思路。Stettner 用 Claude Agent SDK 构建了 Ambral 的核心研究引擎，为每种数据类型配备专门的子智能体。

“我花了大量时间用 Claude Agent SDK 构建一个非常强大的研究引擎，它能在所有这些数据之上运作，”Stettner 解释说。“它围绕 Claude 子智能体搭建，对每一种数据，我们都有一个专门的子智能体，它是理解该数据的专家。”

无论用户与系统对话，还是 Ambral 为客户构建自动化流程，一切背后都由 [Claude Agent SDK](https://docs.claude.com/en/api/agent-sdk/overview) 和一系列子智能体支撑——它们在使用数据、Slack 消息、会议记录和产品交互之间检索并推理。

这种架构灵感直接来自 Stettner 的开发体验：“我认为 Claude Code 的子智能体表现得那么好、帮我完成开发，正是这一点启发我，把这些同样的子智能体用到产品内部的研究引擎上。”

## **Vulcan Technologies：让非技术创始人也能交付产品**

对 Vulcan 的 CEO 兼联合创始人 Tanner Jones 来说，Claude Code 的影响远不止生产力——它意味着创建公司这件事的民主化。创立公司时，Vulcan 团队相信，一定有产品能让政府为公民运转得更好。如果没有 Claude Code，这个愿景不可能实现，因为两位创始人都不具备工程背景。

### **在没有专职工程师的情况下交付产品**

Vulcan 应对的是一个积累了数百年的问题：[法规文本](https://en.wikipedia.org/wiki/Code_of_Federal_Regulations)的复杂性。弗吉尼亚州议会下院（House of Burgesses）是世界上延续时间最长的民主机构，正是这一挑战的缩影。400 多年积累的法规，造就了美国最微妙、最复杂的法典之一。

当 Aleksander Mekhanik 和 Tanner Jones 在 2025 年 4 月共同创立 Vulcan 时，两人都没有传统的工程背景。Mekhanik 在大学学的是机器学习和数学；Jones 最近一次编程经历是高中 AP JavaScript 课程，那门课上大家用纸和笔写代码。然而，这两人在 5 月 1 日前就为弗吉尼亚州州长办公室做出了第一款产品的原型——并从成熟咨询公司手中赢下了合同。

“整个原型都是用 Claude 做的，”Jones 解释说。“那是在 Claude Code 之前。真的就是把脚本复制粘贴进网页应用，然后替换方法。”做完原型后，他们聘请了 CTO Christopher Minge，他曾在 Google 参与 Gemini 和 Waymo 的工作。随后，6 月 Claude Code 发布，这三人的速度再次成倍提升。

Vulcan 的 AI 驱动监管分析通过识别冗余和重复的监管要求，帮助弗吉尼亚州新建住宅的平均价格降低了 2.4 万美元，每年为弗吉尼亚州民众节省超过 10 亿美元。弗吉尼亚州州长非常喜欢 Vulcan 的工作，甚至[签署了第 51 号行政令](https://www.govtech.com/artificial-intelligence/virginia-to-use-agentic-ai-to-power-review-of-regulations)，要求所有州政府机构使用“智能体式 AI 监管审查”。

### **让创建公司这件事民主化**

对 Jones 来说，Claude Code 的影响超越了生产力指标。

“如果你懂语言，也具备批判性思维，你就能把 Claude Code 用好，”他说。“我甚至认为，学人文的人可能会有一些边际优势，因为我们与 AI 沟通的媒介就是语言。如果你有很强的语言驾驭能力，擅长构建组织良好的有序列表、嵌套要点和深思熟虑的流程，你的提示词可能执行得更好。”

Jones 把 Claude Code 视为 Vulcan 成功的重要因素：“四个月里，三个创始人——其中只有一位是真正的技术人员——我们拿下了州和联邦政府的合同，并从一些顶级 VC 那里融到了 1,100 万美元的种子轮。没有 Anthropic 那些令人难以置信的工具，这一切都不可能。”

受过“正统技术训练”的 Vulcan CTO Christopher Minge，也经历了自己对工程认知的转变。

“感觉有点像我在 Google 有一位同事，我把所有想法和任务都交给他，他经常犯错，但我的角色变成了向多个 Claude Code 实例派活，并练就了检查常见错误、有效沟通想法的本事，”Minge 解释说。

## **来自 YC 创始人的最佳实践**

这三家创业公司已经摸索出经过实战检验的做法，让 Claude Code 发挥最大影响，其中包括：

### **1. 把研究、规划和实现拆成各自独立的会话**

“不要让 Claude 一边做研究、一边做规划、一边做实现，”Stettner 建议。“使用彼此独立的提示词，把它们变成彼此独立的步骤。”

这一模式能防止上下文污染，并让每个阶段聚焦于自己的核心目标。为每个主要阶段开启一个新的 Claude Code 会话，只把提炼后的结论传递下去，而不是拖着整段上下文历史。

### **2. 有意识地管理上下文**

Stettner 给其他创始人的建议，核心在于有意识地管理上下文：

“上下文至关重要。当我看到意料之外或质量低下的输出时，通常是因为我在某个提示词里埋下了一处矛盾，”他解释说。“你往系统提示里放什么信息、什么时候开一个新对话，都要非常刻意，因为你不希望把上下文弄浑。只要提示词里存在任何矛盾，你就会得到质量更低的输出。”

### **3. 监控并打断思维链**

“要仔细审视思维链，盯着它在做什么，”Jones 建议。“手指要放在扳机上，随时准备退出并打断任何不良行为。”

在并行运行多个实例时，这一点尤其重要。在最初几次工具调用之内及早发现方向错误，比让 Claude Code 走完整个错误路线要节省大量时间。

## **新一代构建者的优势**

这三家创业公司展示了，在 Claude Code 这类工具面前，公司的构建方式发生了根本转变。HumanLayer 完成了转型与规模化，同时把上下文工程实践沉淀下来，如今这些实践已被整个 YC 生态使用。Ambral 用精干的创始团队应对海量规模的客户成功工作。Vulcan 以非工程师的身份拿下了政府合同。

构建软件的传统壁垒——技术专长、团队规模、开发时间——正在让位于新的竞争优势：清晰的思考、结构化的问题拆解，以及与 AI 高效协作的能力。

**准备好用 Claude Code 构建了吗？**[从这里开始。](https://www.anthropic.com/claude-code)
