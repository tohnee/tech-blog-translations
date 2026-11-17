---
title: "Code w/ Claude 旧金山 2026 回顾：在 AI 指数级增长之上构建"
title_en: "Code w/ Claude SF 2026 recap: Building on the AI exponential"
date: 2026-05-12
source: https://claude.com/resources/articles/code-w-claude-sf-2026-sf
crawled: 2026-11-17
translated: 2026-11-17
---

# Code w/ Claude 旧金山 2026 回顾：在 AI 指数级增长之上构建

> 原文：[Code w/ Claude SF 2026 recap: Building on the AI exponential](https://claude.com/resources/articles/code-w-claude-sf-2026-sf) · Claude 博客

错过了我们在旧金山举办的 Code w/ Claude 开发者大会？主题演讲和分组会议现已上线 YouTube。

本周，我们在旧金山举办了年度开发者大会 [Code w/ Claude](https://claude.com/code-with-claude/san-francisco#agenda)。这场活动汇聚了开发者、工程师和创始人，为期两天，包含主题演讲、分组会议，以及与构建 Claude 的团队共同参与的研讨会。

从提示词编写和[模型选择](https://www.youtube.com/watch?v=OXJO4LldSnc&list=PLmWCw1CzcFim2obQ-w3ohbULOfwp5lApR&index=12)，到设计技能架构和[扩展 AI 原生工程团队](https://www.youtube.com/watch?v=igO8iyca2_g&list=PLmWCw1CzcFim2obQ-w3ohbULOfwp5lApR&index=11)，每一场会议都围绕同一个转变：从想法到生产软件之间的距离正在缩短，而获得最大杠杆的团队，是在为 AI 的指数级增长做设计——而不是被动应对它。

我们通过[现场编程环节](https://www.youtube.com/watch?v=DlTCu_pNDHE&list=PLmWCw1CzcFim2obQ-w3ohbULOfwp5lApR&index=5)、[客户深度解析](https://www.youtube.com/watch?v=EdmuYPBt_EM&list=PLmWCw1CzcFim2obQ-w3ohbULOfwp5lApR&index=2)和动手教程展示了这一切在当下的样貌。

![](https://assets.claude.com/5ce47761e06eea0ebce95e7f6fa878ca6de07b81.jpg)

联合创始人兼总裁 Daniela Amodei 与联合创始人兼 CEO Dario Amodei 参加由 CPO Ami Vora 主持的炉边对话。

## 我们发布了什么

在大会上我们宣布，[将 Claude Code 的速率限制提高一倍](https://www.anthropic.com/news/higher-limits-spacex)，并提高了 Claude Opus 的 API 限制，让开发者、初创企业和大型企业能够更可靠地大规模构建。两项变更现均已生效。

我们还为 Claude Platform 上的 [Claude Managed Agents](https://platform.claude.com/docs/en/managed-agents/overview) 引入了新能力，旨在帮助团队大规模构建和部署云端托管的智能体。四项[新功能](https://claude.com/resources/articles/new-in-claude-managed-agents)现已向所有开发者开放：

* **Dreaming（梦境）。**一个按计划运行的流程，会回顾过去的智能体会话、发现模式并整理记忆，让智能体在多次运行之间不断改进。反复出现的错误、共享的工作流和团队偏好会被归集到更有用的记忆存储中。
* **多智能体编排。**主智能体可以把工作分派给在共享文件系统上并行工作的专业子智能体，每个子智能体都有自己的模型、提示词和工具。整个流程可在 Claude Console 中追踪。
* **Outcomes（成果）。**开发者定义一份衡量好产出的评分标准。一个独立的评分器会在自己的上下文窗口中评估每个结果，并把智能体打回去修改，直到达到标准。在我们的内部基准上，Outcomes 让最难问题上的任务成功率最高提升了 10 个百分点。
* **Webhooks**：定义好 outcome 之后，你可以让智能体自行运行，并在完成时通过 webhook 收到通知。

## 如果你错过了

![](https://assets.claude.com/7bc45a832ecc1123b17c72c613f9d85a4107d799.jpg)

Claude Code 的创造者 Boris Cherny 在旧金山 Code w/ Claude 2026 上演讲。

如果你错过了直播，可以在[此处](https://www.youtube.com/playlist?list=PLmWCw1CzcFim2obQ-w3ohbULOfwp5lApR)观看我们的主题演讲和分组会议录像。

我们的演讲深入 Anthropic 团队构建 Claude 的幕后，并分享 [Asana](https://www.youtube.com/watch?v=BrpB-h1e--k&list=PLmWCw1CzcFim2obQ-w3ohbULOfwp5lApR&index=10)、[Cursor](https://www.youtube.com/watch?v=BbYSGxtsMic&list=PLmWCw1CzcFim2obQ-w3ohbULOfwp5lApR&index=15)、[GitHub](https://www.youtube.com/watch?v=y5TmF_6o6xk&list=PLmWCw1CzcFim2obQ-w3ohbULOfwp5lApR&index=7)、[Replit](https://www.youtube.com/watch?v=snroDwX1-JU&list=PLmWCw1CzcFim2obQ-w3ohbULOfwp5lApR&index=14) 和 [Vercel](https://www.youtube.com/watch?v=bJKdXhnw7NU&list=PLmWCw1CzcFim2obQ-w3ohbULOfwp5lApR&index=3&pp=iAQB0gcJCQMLAYcqIYzv) 等客户如何设计可用于生产的智能体、拓展智能体开发的边界。

我们还将把 Code w/ Claude 带到[伦敦](https://claude.com/code-with-claude/london)（5 月 20-21 日）和[东京](https://claude.com/code-with-claude/tokyo)（6 月 5-6 日）。第一天所有主题演讲和分组会议都将直播。

*敬请期待由我们的演讲衍生的技术教程、指南和客户故事。*
