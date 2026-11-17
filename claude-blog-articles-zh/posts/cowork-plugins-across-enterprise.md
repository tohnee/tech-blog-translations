---
title: "面向企业各团队的 Cowork 与插件"
title_en: "Cowork and plugins for teams across the enterprise"
date: 2026-02-24
source: https://claude.com/resources/articles/cowork-plugins-across-enterprise
crawled: 2026-11-17
translated: 2026-11-17
---

# 面向企业各团队的 Cowork 与插件

> 原文：[Cowork and plugins for teams across the enterprise](https://claude.com/resources/articles/cowork-plugins-across-enterprise) · Claude 博客

管理员现在可以创建私有插件市场，并对插件、连接器和技能拥有更好的控制。我们还新增了覆盖更多部门的插件与连接器。

今天，我们推出了一系列 Cowork 与插件更新，帮助企业在 Claude 中定制符合自身工作方式的使用体验。插件把 Claude 变成面向每个角色和部门的专用智能体。现在，你可以构建私有市场，在组织内分发这些插件。

本次发布还让插件更易于构建和定制，赋予管理员对市场和连接器更多控制，并新增了覆盖更广泛职能的插件与连接器。Claude 现在还能在 Excel 和 PowerPoint 之间进行编排，端到端地工作，并在应用之间传递上下文。

#### *Silvern Capital 是一家虚构公司。演示中的大多数团队在 Cowork 中工作，法务团队则使用 Thomson Reuters CoCounsel Legal——一个专为法律场景打造的智能体，基于 Claude Agent SDK 从零重新构想。*

## 升级插件体验

今天我们推出一整套更新，让插件在整个组织内的创建、使用和管理都更加容易。

管理员现在可以从入门模板创建插件，或从零构建，由 Claude 通过提问引导你完成设置，量身定制适合贵公司的技能、命令和连接器（MCP）。所有这些都集中在一个名为「Customize」的全新统一菜单中——它整合了插件、技能和连接器，让管理员在一处就能查看和管理一切。

![](https://assets.claude.com/b8a7594584b08cf688085642b32ac3d7508b00f2.png)

连接器体验也经过了全面改造：目录得到改进，管理员控制更精简，管理哪些连接器被打包进插件也更加容易。管理员对团队可访问哪些插件拥有更多控制，包括组织专属市场、以私有 GitHub 仓库作为插件来源（内测中）、按用户分配以及自动安装。

在用户侧，斜杠命令（slash command）现在以结构化表单的形式启动，因此运行「生成报告」或「仪表盘」这样的工作流，就像填写一份简报一样直观。Cowork 现在还全面支持公司品牌，包括为你的组织量身定制的重新设计的首页体验。

![](https://assets.claude.com/e97245debbb07158f4ff862168f295ff3e6ec7f5.png)

此外，我们新增了 [OpenTelemetry](https://claude.com/docs/cowork/monitoring#monitoring) 支持，让管理员可以跟踪各团队的使用量、成本和工具活动。

## 新的连接器与插件

当 Cowork 与你已在使用的工具连接时，它处理复杂任务的效果最好。连接器让 Claude 更贴近你工作所在的地方——帮助你在不同工具之间更快移动，而不是取代你所依赖的专业能力或软件。

来自主流企业软件供应商的新连接器现已可用，包括 Google Workspace（[Calendar](https://claude.com/connectors/google-calendar)、[Drive](https://claude.com/connectors/google-drive)、[Gmail](https://claude.com/connectors/gmail)）、[Docusign](https://claude.com/connectors/docusign)、[Apollo](https://claude.com/connectors/apollo)、[Clay](https://claude.com/connectors/clay)、[Outreach](https://claude.com/connectors/outreach)、[Similarweb](https://claude.com/connectors/similarweb)、[MSCI](https://claude.com/connectors/msci)、[LegalZoom](https://claude.com/connectors/legalzoom)、[FactSet](https://claude.com/connectors/factset)、[WordPress](https://claude.com/connectors/wordpress-com) 和 [Harvey](https://claude.com/connectors/harvey)。同时，[Slack by Salesforce](https://claude.com/plugins/slack)、[LSEG](https://claude.com/plugins/lseg)、[S&P Global](https://claude.com/plugins/sp-global)、[Apollo](https://claude.com/plugins/apollo)、[Common Room](https://claude.com/plugins/common-room) 和 Tribe AI（见下文）等公司也为共同客户构建了可供探索的插件。

我们还在扩充预构建插件模板库，让更多知识工作者能在 Cowork 中发现价值。每个模板都与相关领域的从业者共同设计，因此其工作流、术语和产出都反映该项工作实际的完成方式。新插件包括：

* [**人力资源（HR）**](https://claude.com/plugins/human-resources)：支持员工全生命周期的人力运营，从起草录用通知书、制定入职计划，到撰写绩效评估和开展薪酬分析。
* [**设计**](https://claude.com/plugins/design)：加速设计工作流，生成评审框架、起草 UX 文案、执行无障碍审计，并构建用户研究计划。
* [**工程**](https://claude.com/plugins/engineering)：精简日常工程工作流，如撰写站会纪要、协调事故响应、构建部署检查清单和起草事故复盘。
* [**运营**](https://claude.com/plugins/operations)：管理核心业务运营，包括流程文档、供应商评估、变更请求跟踪和运行手册创建。
* **[品牌语调](https://claude.com/plugins/brand-voice)（由 Tribe AI 提供）**：分析你现有的文档、市场材料和对话，把品牌语调提炼为清晰、可执行的准则。
* [**财务分析**](https://claude.com/plugins/financial-analysis)：支持每位财务分析师都需要的基础工作流，从市场与竞争研究，到财务建模以及 PowerPoint 模板的创建和质量检查。
* [**投资银行**](https://claude.com/plugins/investment-banking)：加速交易工作流，包括审阅交易文件、构建可比公司分析和准备推介材料。
* [**股票研究**](https://claude.com/plugins/equity-research)：精简研究工作流，如解析财报电话会记录、根据新指引更新财务模型、起草研究笔记。
* [**私募股权**](https://claude.com/plugins/private-equity)：通过审阅大规模文档集、提取标准化财务数据、建模情景，并依据投资标准给机会打分，支持项目获取与尽职调查。
* **财富管理**：帮助顾问分析投资组合、识别偏离与税务敞口，并大规模生成再平衡建议。

插件是简单、可移植、归你所有的文件系统。它们可在 Cowork 以及任何基于 Claude Agent SDK 构建的东西上运行，让你能轻松创建跨团队、与行业专家合作的私有插件市场。

> 「三波浪潮重塑了专业工作：生产力工具、云与搜索，以及如今的智能体 AI。PwC 正与 Anthropic 合作，把企业级智能体引入 CFO 办公室——通过为每位团队成员提供工具，去做更有雄心的项目、做出更好的决策、以过去不可能的方式推动业务增长，让财务团队成为更具战略性和价值感的职能。」——Sanjay Subramanian，PwC Anthropic 联盟负责人

> 「两年来，市场一直在向我们鼓吹 AI 智能体，说它们会像数字员工一样，围绕某个特定的、离散的工作流全天候工作。而 Anthropic 做出来的东西要好得多。」——Mark Hines，Blank Metal 首席运营官

## 跨应用工作

Claude 现在还能跨 Excel 和 PowerPoint 端到端地处理多步骤任务。Claude 可以在两个 Office 加载项之间使用并传递上下文，这使得分派给 Claude 更大的项目成为可能，例如在 Excel 中运行分析，再把它变成 PowerPoint 演示文稿。这是一个早期研究预览，指向的是 Claude 像我们一样跨应用工作。

## 开始使用

插件的所有用户体验更新对所有 Cowork 用户开放。Team 和 Enterprise 管理员可以使用公司品牌、用户分配和 MCP 控制功能。

Claude 跨 Excel 和 PowerPoint 工作的能力现已在 Mac 和 Windows 上以研究预览形式向所有付费方案开放。下载 [Claude in Excel](https://claude.com/claude-in-excel) 和 [Claude in PowerPoint](https://claude.com/claude-in-powerpoint) 加载项即可开始使用。

要进一步了解面向金融服务的 Cowork 与插件，请参阅我们的[配套博客文章](https://claude.com/resources/articles/cowork-plugins-finance)。
