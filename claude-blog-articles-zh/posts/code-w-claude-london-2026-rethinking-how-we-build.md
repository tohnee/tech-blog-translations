---
title: "Code w/ Claude London 2026：重新思考我们如何构建"
title_en: "Code w/ Claude London 2026: Rethinking how we build"
date: 2026-05-26
source: https://claude.com/resources/articles/code-w-claude-london-2026-rethinking-how-we-build
crawled: 2026-11-17
translated: 2026-11-17
---

# Code w/ Claude London 2026：重新思考我们如何构建

> 原文：[Code w/ Claude London 2026: Rethinking how we build](https://claude.com/resources/articles/code-w-claude-london-2026-rethinking-how-we-build) · Claude 博客

没能来到伦敦现场？主题演讲和分会场现已上线。

本周在伦敦，我们把 [Code w/ Claude](https://claude.com/code-with-claude/london) 带到了欧洲。这场活动汇聚了构建者、开发者和创始人，与打造 Claude 的团队一起度过了为期两天的主题演讲、分会场和研讨会。

![](https://assets.claude.com/31b51736f60c127b3a7f512cd7be4c40a62dd767.jpg)

Cat Wu，Claude Code 产品负责人，在会议间隙与一位参会者交流。

Claude Code 负责人 Boris Cherny 在[主题演讲](https://www.youtube.com/watch?v=6amLO7I9xdg)开场时，讲述了第一次感受到编程“魔力”的时刻。中学时，他编写 TI-83 程序来解数学作业和考试题，还自学了 HTML，让自己在 eBay 上挂出的宝可梦卡牌卖得更好。他通过动手捣鼓来学习，而那些程序跑起来的时候，那种兴奋难以言表。

他提出，不知从什么时候起，编程变得复杂了。编译器、类型检查器、构建系统，每一层都在把“我有个想法”和“它跑起来了”之间的距离推得更远一点。而有了智能体，这段距离正在重新消失：你描述一个问题，程序就出现了。这就是计算器的那种感觉——只不过这个计算器能写出一个分布式系统。

从讲解如何用 Claude Code [超越基础](https://claude.com/code-with-claude/session/ldn-beyond-the-basics-with-claude-code)的研讨会，到优化我们各模型的[思考预算与投入等级](https://claude.com/code-with-claude/session/ldn-the-thinking-lever)，我们展示了 Anthropic 以及 [Spotify](https://claude.com/code-with-claude/session/ldn-coding-is-no-longer-the-constraint-scaling-devex-to-teams-and-agents-at-spotify)、[Base44](https://claude.com/code-with-claude/session/ldn-from-one-person-to-80-scaling-a-hypergrowth-engineering-org-with-claude-code) 和 [Legora](https://claude.com/code-with-claude/session/ldn-what-legal-agents-inherit-from-coding-agents-lessons-from-legora) 等客户，如何已经开始重新获得这种体验。

## 发布内容

![](https://assets.claude.com/c6233df0e9437b16fd5fa6660594a4384e14a9a0.jpg)

Claude 开发者平台工程负责人 Katelyn Lesse 与 Claude 开发者平台产品负责人 Angela Jiang 在 Code w/ Claude London 上演示我们新的 Claude Managed Agents 功能。

在大会上宣布，Claude Managed Agents 现在可以在你控制的沙箱中运行，并连接到你私有的 Model Context Protocol（MCP）服务器。这样一来，智能体执行工具的环境和它访问的服务，都运行在你企业既定的边界之内。这两项[新能力](https://claude.com/resources/articles/claude-managed-agents-updates)已在 Claude Platform 上提供：

* **自托管沙箱**（公开测试）。工具执行迁移到由你配置的环境——你自己的基础设施，或 Cloudflare、Daytona、Modal、Vercel 等托管服务商——而负责编排、上下文管理和错误恢复的智能体循环仍留在 Anthropic 的基础设施上。你的网络策略、审计日志和安全工具随之生效，文件和代码仓库不会离开你的边界，你也可以为高计算量的工作掌控算力规格和运行时镜像。
* **MCP 隧道**（研究预览）*。*你的智能体可以访问私有网络内的 MCP 服务器，而无需将它们暴露在公网上。你部署的一个轻量网关会建立一条单一出站连接：无需入站防火墙规则，没有公开端点，流量端到端加密。Managed Agents 和 Messages API 均支持 MCP 隧道，并由组织管理员在 Claude Console 中管理。

包括 Amplitude、Clay 和 Rogo 在内的团队已经在基于 Managed Agents 与自托管沙箱进行构建。要开始使用，请查阅[文档](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes)，参考我们的 [cookbooks](https://github.com/anthropics/claude-cookbooks/tree/main/managed_agents/self_hosted_sandboxes)，或[申请 MCP 隧道访问权限](https://claude.com/form/claude-managed-agents)。

## 如果你错过了

![](https://assets.claude.com/e442339a37c2269791017f2159a2b3022c9d598a.jpg)

研究产品经理 Lisa Crofoot 在 Code w/ Claude London 主题演讲中进行分享。

如果你错过了直播，可以查看我们的主题演讲和分会场[录像](https://claude.com/code-with-claude/london)。

Code w/ Claude 下一站将前往[东京](https://claude.com/code-with-claude/tokyo)（6 月 5 日至 6 日）。第一天的所有主题演讲和分会场将进行直播。

*敬请期待由这些分享启发的技术教程、指南和客户故事。*
