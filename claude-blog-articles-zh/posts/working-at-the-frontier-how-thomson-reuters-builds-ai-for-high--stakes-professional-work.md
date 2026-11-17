---
title: "站在前沿：汤森路透如何为高风险专业工作构建 AI"
title_en: "Working at the frontier: How Thomson Reuters builds AI for high-stakes professional work"
date: 2026-07-08
source: https://claude.com/resources/articles/working-at-the-frontier-how-thomson-reuters-builds-ai-for-high--stakes-professional-work
crawled: 2026-11-17
translated: 2026-11-17
---

# 站在前沿：汤森路透如何为高风险专业工作构建 AI

> 原文：[Working at the frontier: How Thomson Reuters builds AI for high-stakes professional work](https://claude.com/resources/articles/working-at-the-frontier-how-thomson-reuters-builds-ai-for-high--stakes-professional-work) · Claude 博客

汤森路透（Thomson Reuters）CTO Joel Hron 多年来一直把 AI 植入律师和会计师所信赖的产品之中。以下是他为何认为 Claude Fable 5 是知识工作 AI 能力边界的一次关键演进。

汤森路透是一家全球内容与科技公司，175 年多来一直为做出重大决策的专业人士和机构打造值得信赖的内容与技术。如今，同样的使命正塑造着公司为法律、税务、会计、合规及其他高风险专业工作流构建 AI 的方式。

"我们是一家科技公司，专注于那些要求准确与精确的职业，"汤森路透 CTO Joel Hron 说。

它的产品正是这些职业赖以运转的参考工具：用于法律研究和实务指引的 Westlaw 与 Practical Law；CoCounsel Legal——汤森路透的专业级法律 AI 平台，旨在让法律专业人士更出色地完成工作，其答案经得起推敲，成果具有真实价值。Hron 四年前因自己的创业公司被收购而加入汤森路透，工作横跨产品、技术与战略。他说，在这段时间里，AI 重塑了"构建软件"的含义。选择正确的技术伙伴从未如此重要。

为这些产品挑选底层 LLM 的标准异常具体。Hron 和团队评估新模型的方式是：它的产出能否经受住律师在依赖它之前所施加的那种专业审查。

### 为法律工作评估模型

很多公司都能构建[法律 AI 工具](https://claude.com/resources/guides/claude-for-the-legal-industry)，但能做出让律师愿意署上自己名字的工具的，少得多。汤森路透为专业 AI 带来三项通用系统难以轻易复制的优势：权威内容、深厚的领域专业知识，以及工作流集成。

Hron 说，律师之所以能信赖 Westlaw 给出的答案，靠的不是模型本身，而是数十年精心整理的判例法、全球 2,700 多名领域专家每天对这些内容进行标注和增强的工作，以及汤森路透在 Claude 等模型之上构建的评测体系。"最终对工作成果负责的，仍然是那位人类专业人士。"

Claude 是重要的模型伙伴，但专业级系统来自 Anthropic 前沿模型与汤森路透权威内容、深厚领域专业知识、工作流集成和评测基础设施的结合。

汤森路透将这一方法称为"Fiduciary-Grade AI™"（信义级 AI）：以权威内容为根基、由深厚领域专业知识塑造、直接嵌入专业工作流，从而在风险高企时让输出透明、可核验、可辩护。

正是这种问责关系，使得核验在专业场景中比流畅度更重要。汤森路透围绕一批为"不仅是搜索、也不仅是检索，而是引证校验与核验"而调优的智能体重建了法律研究。其要求是：系统要帮助校验引证并清晰呈现来源，让专业人士能够放心地审阅、核实并运用自己的判断。

变化体现在客户的反馈中。Hron 说，过去"要花几十个小时"的研究，现在"几分钟就能完成"，为专业人士提供一个可以评估、打磨并据以行动的高质量起点。"深度研究彻底改变了人们对法律研究的思考方式。"

### 构建智能体优先的产品

对汤森路透而言，构建智能体不是要造一个更聪明的聊天机器人，而是体现了一种交付既有产品的新方式。Hron 和团队着手教一个智能体使用公司过去作为独立软件提供的所有工具。如今，单个智能体可以同时访问数百个公司工具。

这一转变改变了汤森路透[评估模型](https://claude.com/resources/webinars/evals-for-ai-agents-how-product-builders-get-the-most-out-of-every-new-model)的方式。"我们对 Claude 的重大考验，是真正评估它在制定计划、以及有效且正确地使用这些工具方面有多强，"他说。

CoCounsel Legal 展示了这种形态。它过去要一个接一个地运行独立技能。基于 [Claude Agent SDK](https://claude.com/resources/articles/building-agents-with-the-claude-agent-sdk) 重建后，它现在能实时规划、委派并跨工具和内容源编排，让专业人士只需定义结果，而不必规定每一步。客户数据始终受到保护，不会被用于训练第三方模型。

Hron 把这一选择追溯到两家公司最初如何开始合作。汤森路透是 Anthropic 最早的企业客户之一，而决定性因素并非某项基准分数。"最打动我们的一点，是 Anthropic 构建企业级 AI 的方式，"他说，并提到透明度、安全性和负责任的 AI 开发。第一个验证点是法律领域的深度研究——双方团队注意到 Anthropic 的工程师正以汤森路透已在交付的方式使用这些工具，于是共同开发了这一功能。

### 知识工作对模型提出了什么要求

![](https://assets.claude.com/20138f1eea22461cb39fa554d873867327d5534d.jpg)

公司内部的产品、运营和业务团队使用 Claude Cowork 进行流程自动化和轻量原型制作。

在这些项目中，Hron 的团队总结出模型必须做到的四件事，汤森路透才会信任它。

第一，作为 CoCounsel Legal 系统的一部分，模型必须核验自己的引证。系统不能只检索到一个来源就继续推进，而必须在把结论呈现给人类做最终审阅和核验之前，先校验它所引用的内容。

第二，在这个系统中，模型还必须能在长链条的工具调用中保持稳定。更长的任务要求在长时间运行中具备更好的上下文管理和可靠的工具使用。模型必须跨许多步骤、许多系统保持主线，让智能体真正完成工作，而不是中途卡住。

第三，它必须把人带入工作过程，而不只是给出答案。对于最难的任务，Hron 希望模型能"把人带入工作成果的形成过程，而不只是依赖智能体一次性给出答案"。

最后，它必须为汤森路透团队此前无暇顾及的工作腾出时间。汤森路透正在为复杂法律工作开发高级起草能力，包括动议起草和申报文件——这些工作专业人士原本"要花几天或几周打磨"，他说。这类任务"一直需要远超以往的上下文和精确度"，对早期模型来说难以胜任。而有了 Claude Fable 5，它现在触手可及。

### AI 的投资回报

Hron 对 AI 的投资回报持一种反主流观点，其他正在推广模型的管理者或许会觉得有用。"如果你过度执着于优化投资回报率的计算，就会只见树木不见森林，"他说。他希望团队先感受文化和心态的转变，再去调优单任务成本。一旦心态转变发生，回报会自己到来。

他仍然跟踪传统工程指标，如 DORA（DevOps Research and Assessment）和从想法到上线的时长，并提到一个基于 Claude 构建的内部错误修复工具，把一个生产问题从三小时的根因分析变成了四分钟的修复。"能在几分钟内而非几小时内恢复健康状态，这是实质性的差别。"

按 Hron 的说法，更深层的变化发生在工作本身。

"写代码本身不再是工作内容，"Hron 这样评价他的工程师；如今最重要的技能是系统思维、判断力和品味。他看到同样的模式正在蔓延到工程之外，AI 让人变得"更 T 型"——能够横跨产品、设计和财务，而不是固守一条赛道。

### 下一步

![](https://assets.claude.com/bb70dc6c2d7ae94da38cdc2a2db47ffaffb0da4e.jpg)

汤森路透的员工使用 Claude Code 快速熟悉代码库，并构建长时间运行的智能体。

Hron 和团队迫不及待想用 Claude Fable 5 及未来的 Claude 模型突破边界：更长时间跨度的工作、更好的上下文管理，以及在智能体执行的整条任务链上都可靠的工具调用。

他同样渴望在自己的工作中使用这些模型。Claude Code 让他"重新变得技术感十足"——几分钟而不是一天，就能熟悉一个几个月没碰过的代码库；他还会借助 Claude Cowork，从 CFO 或战略主管的视角来压力测试自己的想法。

这些正是 Claude Fable 5 这类模型围绕构建的方向。而对于最终必须在法庭上站得住脚的工作，Hron 认为那是下一步值得推进的前沿。毕竟，专业 AI 必须在"差不多正确"远远不够的环境里工作。

**开始使用 [Claude Fable 5](https://platform.claude.com/docs/en/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5)。**
