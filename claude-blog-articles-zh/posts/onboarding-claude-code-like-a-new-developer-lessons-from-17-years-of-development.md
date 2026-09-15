---
title: "像带新开发者一样引导 Claude Code 入职：来自 17 年开发经验的启示"
title_en: "Onboarding Claude Code like a new developer: Lessons from 17 years of development"
source: https://claude.com/blog/onboarding-claude-code-like-a-new-developer-lessons-from-17-years-of-development/
crawled: 2026-09-14
translated: 2026-09-14
---

# 像带新开发者一样引导 Claude Code 入职：来自 17 年开发经验的启示

> 原文：[Onboarding Claude Code like a new developer: Lessons from 17 years of development](https://claude.com/blog/onboarding-claude-code-like-a-new-developer-lessons-from-17-years-of-development/) · Claude 博客

[Skyline](https://skyline.ms/home/software/Skyline/wiki-page.view?name=team) 是一款开源蛋白质分析软件，由主开发者 Brendan MacLean 在华盛顿大学 MacCoss 实验室维护，自 2008 年起持续活跃开发。Skyline 帮助研究人员在血浆、组织等样本中检测和定量蛋白质，这对生物标志物发现、疾病研究和药物开发至关重要。MacCoss 实验室的代码库包含 70 万多行 C# 代码，由一个小团队维护了 17 年，运行着 20 万多个自动化夜间测试。

*用 Blender 制作的西雅图天际线 3D 插图，代表华盛顿大学 MacCoss 实验室所在地——Brendan MacLean 和他的团队自 2008 年以来一直在这里开发并维护 Skyline。背景中的 Claude 标志是在 Claude 的帮助下加上去的。图片由 MacCoss 实验室提供。*

近三十年来，Brendan 一直是 Skyline 的「结缔组织」，为实验室引导了几十名本科生、研究生和博士后上手。

开发者来来去去，代码库吸收了他们的贡献。到 2024 年，它已经背负起长寿命项目常见的包袱：随着人员更替，某些区域变得无人敢碰。

在培训实验室成员几十年之后，Brendan 很清楚如何让研究人员快速熟悉实验室庞大的代码库。他没有料到的是，把同样的方法用在一个 AI 工具上，竟能让 Skyline 的代码库重新变得可控。

## 同样的入职问题，另一种开发者

Brendan 曾怀疑，现代 AI 编码工具能否像一款专为这种语言和环境量身打造的工具那样，真正理解这些 C# 代码。

在浏览器里用 Claude.ai 做的早期实验印证了这一判断。他会描述一个问题，得到一段回复，再把整个 C# 文件复制回项目——只限于那些无需引用项目代码就能描述清楚的封闭问题。

「一旦改动变得更细碎，整个过程就变得非常费力，」Brendan 说。

每次与 Claude.ai 的会话都像从零开始，因为它完全不了解 Skyline 是什么、各组件之间如何关联、17 年的开发沉淀了什么。

这正是 Brendan 在引导新开发者入职时面对的同样处境，由此他产生了一个想法。

「我可以通过 Claude Code 把 Claude 介绍给我的大项目，就像带一名实习生那样：解释到足以让它完成一个成功的小范围任务，并为下一轮迭代沉淀出更好的上下文，」Brendan 说。

他把所有 AI 上下文挪进了一个独立的仓库 [pwiz-ai](https://github.com/ProteoWizard/pwiz-ai)，与代码库分开存放，这样上下文就能适用于所有分支和所有时间点。根目录下的 `CLAUDE.md` 文件负责环境设置，并把 Claude 指向相关文档：可以把它理解为「总体地形概貌」，而不是专业知识本身。

专业知识则放在[技能（skills）](https://agentskills.io/home)里——这是一种赋予智能体能力与专业知识的开放格式。比如他的 `debugging` 技能，目的就是把 Claude 从他所说的「瞎猜再试」（guess and test）模式里拉出来，迫使它在尝试任何修复之前先做根因分析。技能可以手动或自动触发；Brendan 为最关键的技能设置了显式触发条件——`debugging` 技能的描述写着「调查 bug、故障或意外行为时必须加载（ALWAYS load）」。

*pwiz-ai 仓库结构，展示上下文、技能与 MCP 集成如何连接到 Skyline 的代码库。图片由 MacCoss 实验室提供。*

上下文建立之后，教会 Claude 这个代码库调试门道的开销显著降低。Claude 已经知道这些代码在做什么，交互从「理解」起步，而不是从零开始。

「曾几何时最让人担心的是『Claude 没法真正学会我的大项目』，如今答案越来越清晰：上下文不过是又一个需要维护和培育的项目产物，」Brendan 说。

## 减少技术债，加速开发

在 Skyline 中构建 Files View 面板是一个为期一年的项目——这是一个展示所有文档相关文件、支持文件系统监控与拖拽整理的新界面——在负责它的开发者离开后便一直处于未完成状态。Brendan 用 Claude Code 把它捡了起来。

两周之后项目完成，所有最终提交都由 Claude 共同署名。

「以往以那种状态搁下的工作，最后通常都被扔掉了，」Brendan 说。在学术实验室里，人员流动频繁——研究生毕业了，博士后去了别处，实习生夏天一结束就离开。换作过去，任何进行到一半的工作都会被永远束之高阁。

三年前，在失去维护者之后，Brendan 停止了为 Skyline 的夜间测试管理模块添加功能。该模块用 Java 编写，是 LabKey Server 科学数据门户网站的一部分。最近，在请一位熟练的 LabKey 开发者用 Claude Code 编写了环境搭建文档之后，Brendan 花了不到一天时间，就加上了自己期盼多年的功能，并用 CSS 更新了页面布局——过去这种 CSS 他只会雇设计师来写。

新基础设施也随之而来。

Skyline 的 2000 多张教程图片的截图复现现已完全自动化，可复现率接近 100%；借助 Claude Code 扩展出了仅显示差异（diff-only）的视图和像素变化放大功能，还配备了一个由 Claude 用 C# 编写的 MCP 服务器，让它能「看」到这些差异。Claude Code 每天早晨生成一份每日摘要，展示从 Skyline 夜间测试基础设施中提取的测试失败、异常和未关闭的支持工单，在 Brendan 坐下工作之前就送达他的收件箱。

Claude 还用 Python 编写了另一个 MCP 服务器来实现这项能力，从三个相互独立的关系型数据流中取数：LabKey Server、团队邮件，以及 GitHub 上带发布标签的代码。

*由 Claude Code 自动生成的每日摘要邮件，数据来自 Skyline 的夜间测试基础设施。图片由 MacCoss 实验室提供。*

如今 Brendan 团队的开发者几乎不再亲手写代码，主要是给 Claude Code 下指令，并用它自主生成自动化脚本和 MCP 实现。比如，实验室里一位曾对智能体编码工具持怀疑态度的开发者，构建并发布了一个新的绘图扩展——用于可视化离子迁移率数据的 mobilogram 窗格——并把功劳归于 Claude Code。

*mobilogram 窗格用 Claude Code 构建，将离子迁移率数据与质谱结果并列可视化。图片由 MacCoss 实验室提供。*

「我看到几乎每个人都在接手那些有趣的新功能——换作以前，他们大概会觉得被其他工作压得喘不过气、根本不敢尝试，」Brendan 说。

## 给维护遗留代码库的开发者的建议

基于 17 年引导开发者入职的经验，以及一年多来把同一套方法论应用于 Claude Code 的实践，以下是 Brendan 想对维护遗留代码库的开发者们说的话。

**上下文是你最好的朋友**

Claude 生成的待办清单和计划不会跨会话留存。真正留存下来的是[上下文](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)，而它必须有意识地加以维护。大多数开发者恰恰跳过了这一步，这也正是大多数人的成效止步不前的原因。

「要明白，如果不去记录『上下文』，Claude 就学不到东西。别指望魔法，」Brendan 说。「投入精力去构建和维护你的上下文层，并像对待其他项目产物一样对待它：纳入版本管理、持续扩充、用心维护。」

Brendan 把 AI 上下文放在一个单独的仓库里，因为它的增长速度与代码不同，且适用于所有分支和所有时间点——放在代码仓库内部正变得越来越受限。把上下文放在同一个仓库里也是可行的替代方案；关键在于它要有版本管理、有人维护、需要时随时可用。

**投资构建你的技能库**

用[技能（skills）](https://claude.ai/skills)把领域知识编码成任何 Claude 实例都能加载的形式。Brendan 的技能遵循「引用而不内嵌」原则：每个技能都指向一个中央文档知识库，而不是复制内容，从而保持轻量、易于维护。

他最常用的包括：`skyline-development` 技能，帮助 Claude 熟悉项目及其文档；`version-control` 技能，编码了项目特有的提交与 PR 规范；还有 `debugging` 技能，用于把 Claude 从「瞎猜再试」模式中拉出来，促使它在尝试任何修复之前先做根因分析。

**当数据访问是关键时，使用 MCP 集成**

在 Claude 需要访问真实数据的地方构建 [MCP 集成](https://anthropic.com/engineering/mcp)：测试结果、异常报告、支持工单。

对开源项目而言，构建并维护上下文层分量尤重。没有入职培训预算，除了写下来的内容之外没有任何机构记忆，也无法保证任何一位贡献者明年还在。上下文一旦建成，就对每一位贡献者开放，并在项目的整个生命周期中持续存在——这是人类头脑中的机构知识永远做不到的。`pwiz-ai` 仓库本身就是一件开源产物——这份上下文属于项目而非任何个人贡献者，并将比每一位构建者存在得更久。

## 十七年的入职引导，一个结论

你不会把一个 70 万行的代码库直接丢给新员工，指望他第一天就出成果。你会给他找一个边界清晰的小项目，带他走一遍，再随着他理解的深入逐步扩大范围。

正如 Brendan 所体会到的，你与 Claude 一起构建的上下文，道理相同。

一旦对代码库足够熟悉，工程师就能跨分支、跨时间点开展工作。Claude 在获得足够的上下文和指引后，同样可以做到。

**Anthropic 联合创始人 Dario Amodei 曾是 MacCoss 实验室的成员。**

FAQ（常见问题）
