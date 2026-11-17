---
title: "在 Excel、PowerPoint、Word 和 Outlook 中与 Claude 协作"
title_en: "Collaborate with Claude across Excel, PowerPoint, Word and Outlook"
date: 2026-05-07
source: https://claude.com/resources/articles/collaborate-with-claude-across-excel-powerpoint-word-and-outlook
crawled: 2026-11-17
translated: 2026-11-17
---

# 在 Excel、PowerPoint、Word 和 Outlook 中与 Claude 协作

> 原文：[Collaborate with Claude across Excel, PowerPoint, Word and Outlook](https://claude.com/resources/articles/collaborate-with-claude-across-excel-powerpoint-word-and-outlook) · Claude 博客

*一次对话，上下文贯穿全部四个应用*

从今天起，Claude for Excel、Claude for PowerPoint 和 Claude for Word 正式可用（generally available），Claude for Outlook 也在所有付费套餐中进入公测。当 Claude 在你的 Microsoft 应用之间切换任务时，它会保留整段对话的完整上下文。

## **一次对话，贯穿四个应用**

大多数工作并不只存在于一个应用里，所以 Claude 会随你在应用之间流转。在 Outlook 里分诊一封邮件，在 Word 中打开附件、按团队模板起草一份备忘录，在 Excel 里做出支撑分析，再在 PowerPoint 里把它变成一套演示文稿——全程无需重新解释你在做什么。在 Excel 里调整一个假设，PowerPoint 里的图表和 Word 备忘录里的数字也会自动更新。

Claude 可跨打开的文件工作，所以把表格、演示文稿和备忘录并排打开，改动就会在它们之间流动。

对话会随每个文件持久保留，你可以关闭侧边栏，第二天再打开，用键盘或语音从上次停下的地方继续。

## **Claude for Outlook**

Claude for Outlook 把 Claude 带进你的收件箱。让 Claude 分诊你的收件箱，它会按"哪些需要你回复""哪些它可以替你起草""哪些是噪音"给邮件分类。回复会以草稿形式落到 Outlook 的撰写窗格中，收件人、主题和正文都已填好。日历邀请会检查参会者的空闲时间，并在 Outlook 原生的日程事件表单中打开。

在 Word 或 Excel 中打开附件时，Claude 已经知道发件人提出了什么要求。每一封回复和每一个日历邀请都由你审阅后才发出，在你点击发送之前，什么都不会发出去。

## **在整个组织范围内部署 Claude for Microsoft 365**

Claude for Excel、PowerPoint 和 Word 现已正式可用，并具备 IT 管理员和组织所需要的管控能力。一个 AppSource 条目覆盖 Excel、PowerPoint 和 Word，另一个独立条目以 beta 形式加入 Outlook。管理员可以从 Microsoft 管理中心部署这两者。

企业管理员可以配置 [OpenTelemetry](https://support.claude.com/en/articles/14447276-configure-a-custom-opentelemetry-collector-for-office-agents)，把提示词、工具调用和文档引用流式发送到自己的采集器，让安全团队确切看到 Claude 在每个应用中做了什么。[Analytics API](https://support.claude.com/en/articles/13703965-claude-enterprise-analytics-api-reference-guide) 则按用户、按应用、按天拆解活动数据。

组织可以用 Claude 账号访问全部四个加载项，也可以通过现有的 LLM 网关把流量路由到运行在 Amazon Bedrock、Google Cloud Vertex AI 或 Microsoft Foundry 上的 Claude 模型。

Microsoft 365 Copilot 客户也可以直接在 [Excel](https://support.microsoft.com/en-gb/topic/choose-your-model-when-editing-with-copilot-in-excel-b2c3b3ec-154b-484b-84d0-914a80df395a) 和 [PowerPoint](https://support.microsoft.com/en-gb/topic/choose-your-model-in-agent-mode-25ba645b-2932-4f10-a910-fea4ae76d65c) 中使用 Claude AI 模型。

## **组织如何用 Claude for Microsoft 365**

![Citadel](https://assets.claude.com/6974233e910a5ba470a017719933cbf677a74d0b.svg)

> "我们的投资专业人士整日与数据和分析模型打交道，Claude for Excel 就在那里与他们相遇。分析师正用它构建和更新覆盖模型、从噪音中分离信号、对自己的工作做压力测试——效率提升是阶跃式的。"

Atte Lahtiranta，核心工程负责人

![Bain & Company](https://assets.claude.com/687ae4df36a08c5cd73be9019650f3358fc4c3b2.svg)

> "Excel 中的 Claude 让我的团队能更快搭出复杂模型的初版，使他们可以专注于打磨模型、对输入和假设做压力测试，并探索更多情景和权衡。这帮助我们更早地与客户展开更丰富、更深入的讨论。"

Gene Rapoport，私募股权 AI 业务负责人

![Deloitte](https://assets.claude.com/d799180e9a468d82dc23a32c1ddfe94dcee116d0.svg)

> "Claude 让从粗糙想法到打磨精美、符合品牌的交付物之间的过渡在演示文稿、文档和表格三类应用中无缝衔接，而不打断工作流。这种端到端的一致性大幅节省了时间，尤其在质量、格式和速度都重要的时候。"

Vivek Kulkarni，美国 AI 转型负责人

![British Columbia Investment Management Corp](https://assets.claude.com/f9578c1cf0c050b2131464fceb3ac9bc1cb19062.svg)

> "我们可以让 Claude 根据某位高管以往的书面沟通记录构建一份风格指南，这样我们的行政助理（EA）就能用他的口吻起草邮件。这是高杠杆的工作，团队原本绝不会有时间手工搭建。"

Ben Letalik，数字化转型与创新高级总监

![ServiceNow](https://assets.claude.com/fe0e4049f1a44dacc4b0e11ea7be3c1e5eb6b255.svg)

> "Claude for M365 正在 ServiceNow 内部被迅速采用。Claude 直接在 Excel 里完成工作，而不是要求我们在工具之间搬运内容，带来了生产力的阶跃式提升。"

Rajeev Sethi，企业技术 GVP

## **快速开始**

所有付费套餐的 Mac 和 Windows 用户都可以使用 [Claude for Microsoft 365](https://claude.com/claude-for-microsoft-365)。[Claude for Outlook](https://claude.com/claude-for-microsoft-365) 在所有付费套餐中以 beta 形式提供。管理员可以通过 Microsoft 管理中心从 Microsoft AppSource 部署这些加载项。
