---
title: "Claude Security 进入公开测试阶段"
title_en: "Claude Security is now in public beta"
date: 2026-04-30
source: https://claude.com/resources/articles/claude-security-public-beta
crawled: 2026-11-17
translated: 2026-11-17
---

# Claude Security 进入公开测试阶段

Claude Security 现已面向 Claude Enterprise 客户开放公开测试。使用 Opus 4.7，在 Claude Platform 上，或通过基于 Claude 构建的技术与服务合作伙伴，扫描代码中的漏洞并生成修复建议。

*编辑注：本文中 2026 年 10 月 30 日之前出现的 Max，如今包含 Max 与 Ultra 两个套餐。*

Claude Security 现已面向 Claude Enterprise 客户开放公开测试。

AI 网络安全能力正快速演进。今天的模型在发现软件代码缺陷方面已相当有效；下一代模型还会更强，并且在自主**利用**这些缺陷方面将尤为擅长。现在正是各组织采取行动、提升自身安全水平的时机——为一个「可用的软件漏洞利用程序变得容易得多被发现」的世界做好准备。

最近，我们把 Claude Mythos Preview 提供给一批合作伙伴——它在发现和利用软件漏洞两方面都能达到甚至超越顶尖人类专家——这是 [Project Glasswing](https://www.anthropic.com/glasswing) 的一部分。

但我们的网络安全工作不止于 Glasswing：借助 Claude Security，范围广得多的组织都能让我们最强大的通用可用模型 Claude Opus 4.7 在其代码库上工作。在发现与修复软件漏洞、以及发现那些可能被忽略的复杂、依赖上下文的问题方面，Opus 4.7 是当前最强的模型之一。

Claude Security——此前称为 Claude Code Security——已在限定范围的研究预览中由数百家不同规模的组织测试，帮助团队扫描代码库中的漏洞并生成针对性补丁。他们的反馈塑造了今天的发布：Claude Security 向所有 Enterprise 客户开放，并带来定时扫描与定向扫描、更便捷的审计系统集成，以及改进后的已分诊发现项跟踪。无需 API 集成，也无需自行构建智能体：如果你的组织在用 Claude，今天就可以开始扫描。

Opus 4.7 的能力也正通过 Claude 与许多企业已在使用的软件工具的集成，送到网络防御者手中。我们的技术合作伙伴，包括 [CrowdStrike](https://www.crowdstrike.com/en-us/press-releases/crowdstrike-puts-claude-opus-4-7-to-work-across-falcon-platform-project-quiltworks/)、Microsoft Security、[Palo Alto Networks](https://www.paloaltonetworks.com/blog/2026/04/ai-driven-defense-anthropics-claude-opus/)、[SentinelOne](https://www.sentinelone.com/press/sentinelone-unveils-wayfinder-ai/)、[TrendAI](https://newsroom.trendmicro.com/2026-04-30-TrendAI-TM-and-Anthropic-Advance-AI-Powered-Vulnerability-Detection-and-Risk-Mitigation-with-Claude-Opus-4-7) 和 [Wiz](https://www.wiz.io/blog/red-agent-claude-opus)，正把 Opus 4.7 嵌入各自的工具；此外，埃森哲、BCG、德勤、Infosys 和普华永道等服务合作伙伴，也正在帮助各组织部署集成了 Claude 的安全解决方案。

我们正进入网络安全的关键时期。AI 正在压缩从漏洞被发现到被利用之间的时间差。我们认为，正确的应对是确保防御者能以最容易获得的方式用上前沿能力——无论是直接通过 Claude，还是通过我们的合作伙伴。

## Claude Security 如何工作

可以直接从 Claude.ai 侧边栏进入 [Claude Security](https://youtu.be/0SgCiUfoYo8)，或访问 [claude.ai/security](http://claude.ai/security)。开始时，选择你的一个代码仓库（或限定到特定目录或分支），然后启动扫描。

扫描时，Claude 会像安全研究员那样对代码进行推理。它不是通过搜索已知模式来发现漏洞，而是试图理解各组件如何跨文件、跨模块交互，追踪数据流，并阅读源代码。

完成后，Claude 会为每一项发现提供详细解释，包括它认为该漏洞真实存在的置信度、严重程度、可能影响，以及如何复现。它还会生成针对性补丁的说明，用户可以在 Claude Code on the Web 中打开，在上下文中完成修复。

## 从最初的预览版中我们学到了什么

过去两个月，我们依据数百家企业在生产环境中使用 Claude Security 的经验，持续打磨它。具体来说，我们发现：

**检测质量至关重要。** 团队告诉我们，高置信度的发现项才是真正加速安全工作的关键。Claude Security 的多阶段验证流水线会在发现项送达分析师之前独立审查每一项，从而压低误报率；同时 Claude 会为每一个结果附上置信度评级。这意味着送到团队手上的信号值得采取行动。

**从扫描到修复的时间才是关键指标。** 早期用户反复强调这一点：多个团队能在一次连续工作中完成从扫描到应用补丁的全过程，而不是让安全和工程团队来回拉扯数天。

**团队要的是持续覆盖，而不是一次性审计。** 我们新增了定时扫描选项，让团队可以为发现项的审阅与处置设定固定节奏。

本次发布还新增了以下能力：把扫描定向到仓库中的特定目录；带记录理由地驳回发现项（让后续审阅者可以信任此前的分诊决策）；将发现项导出为 CSV 或 Markdown，以接入既有的跟踪与审计系统；以及通过 webhook 把扫描结果发送到 Slack、Jira 或其他工具。

以下是使用过 Claude Security 的组织对其实践的描述：

![Column logo](https://assets.claude.com/88207d00a1f7ad8c894ef632af39d9b11d1b655a.png)

> “Claude Security 理解我们代码背后的真实业务逻辑。我们的安全团队现在可以在我们信任的工具链里，几次点击就完成从扫描到修复。”

Greg Janowiak，信息安全官

![Yuno](https://assets.claude.com/1be68cb8bfce1230ce4702dbc8a2ca987e93f243.svg)

> “扫描质量正是我们想把 Claude Security 直接接入漏洞管理计划的原因——让真实问题更快到达工程团队，中间少一些分诊开销。”

Chiara La Valle，安全负责人

![Hebbia](https://assets.claude.com/a51bf0be0d5ebeb3530f010c18452357dde28d83.svg)

> “鉴于漏洞发现节奏不断加快，对我们来说最强的信号是一个发现项能多快变成我们真正可以合并的 PR，而不是一张工单。我们用 Claude Security 构建的补丁，几分钟而不是几天就关闭了真实漏洞。”

Matt Aromatorio，安全负责人

![Doordash](https://assets.claude.com/23e9f66a28975a13266abe3f53567c17a5bdb888.svg)

> “我们正通过与 Anthropic 的合作调整主动安全工作。Claude Security 帮助我们在 DoorDash 的规模与速度下，加快新代码的生成与安全加固——它准确揭示深层漏洞，并把发现结果直接接入我们的工作流，让工程师能在上下文中处置。”

Suha Can，副总裁兼首席安全官

![Snowflake](https://assets.claude.com/5137db8e735ff610a994507050d0a0cea7ce6fd0.svg)

> “在研究预览的早期测试中，Claude Security 发现了新颖、高质量的发现项，帮助我们在潜在安全问题影响自身环境或客户之前识别并处理它们。随着我们扩大使用范围，我们看到它有很大潜力。”

Krzysztof Katowicz-Kowalewski，产品安全工程师（Staff）

AI 驱动的安全尚处在早期阶段。随着模型能力提升，也随着我们从生产环境中使用 Claude Security 的团队身上不断学习，我们将继续拓展这些工具的能力边界。

## 在防御者工作的地方与他们相遇

Claude Security 是我们「把前沿能力交到防御者手中」这一更大努力的一部分。它的覆盖面很大程度上来自团队如今所依赖的平台与服务合作伙伴。

[CrowdStrike](https://www.crowdstrike.com/en-us/press-releases/crowdstrike-puts-claude-opus-4-7-to-work-across-falcon-platform-project-quiltworks/)、Microsoft Security、[Palo Alto Networks](https://www.paloaltonetworks.com/blog/2026/04/ai-driven-defense-anthropics-claude-opus/)、[SentinelOne](https://www.sentinelone.com/press/sentinelone-unveils-wayfinder-ai/)、[TrendAI](https://newsroom.trendmicro.com/2026-04-30-TrendAI-TM-and-Anthropic-Advance-AI-Powered-Vulnerability-Detection-and-Risk-Mitigation-with-Claude-Opus-4-7) 和 [Wiz](https://www.wiz.io/blog/red-agent-claude-opus) 正把 Opus 4.7 的能力集成进企业今天已在运行的安全平台。

埃森哲、BCG、德勤、Infosys 和普华永道正与企业安全组织并肩工作，为漏洞管理、安全代码审查和事件响应项目部署集成了 Claude 的安全解决方案。

合在一起，这意味着组织可以选择最契合自身运作方式的路径来采用这些能力：直接使用 Claude Security、嵌入其信任的平台，或由服务团队指导落地。

![](https://assets.claude.com/c1b1e2638fb40873dea79f8d6c747d49a8b9262c.png)

## 开始使用

Claude Security 自即日起面向 Claude Enterprise 客户开放公开测试。面向 Claude Team 和 Max 客户的访问即将推出。

管理员可以在[管理控制台](http://claude.ai/admin-settings/claude-code)中启用 Claude Security。完整操作指引请参阅我们的[上手指南](https://claude.com/resources/tutorials/getting-started-with-claude-security)。

¹Claude Opus 4.7 采用新的网络安全防护措施，可自动检测并拦截暗示被禁止或高风险网络安全用途的请求。不过，从事可能触发这些防护措施的工作的组织，可以加入我们的[网络安全验证计划](https://support.claude.com/en/articles/14604842-real-time-cyber-safeguards-on-claude)——这是我们让前沿能力可供防御者使用、同时避免其落入不当之手的努力的一部分。
