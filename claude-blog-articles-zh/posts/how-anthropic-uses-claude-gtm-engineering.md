---
title: "一位 Anthropic 销售如何用 Claude Code 重建团队工作流"
title_en: "How one Anthropic seller rebuilt his team's workflows with Claude Code"
date: 2026-06-05
source: https://claude.com/resources/articles/how-anthropic-uses-claude-gtm-engineering
crawled: 2026-11-17
translated: 2026-11-17
---

# 一位 Anthropic 销售如何用 Claude Code 重建团队工作流

> 原文：[How one Anthropic seller rebuilt his team's workflows with Claude Code](https://claude.com/resources/articles/how-anthropic-uses-claude-gtm-engineering) · Claude 博客

*加入 Anthropic 之前，GTM 产品经理 Jared Sires 从未打开过终端。如今，Anthropic 的销售团队在用的正是他做的工具。*

2024 年加入 Anthropic 之前，Jared Sires 从未写过一行代码。也难怪——他当时是一家创业公司的客户主管。

正如快节奏成长的公司里常见的那样，Jared 负责的客户名单很快增长到 600 或 700 个。每天 10 到 15 通客户电话，加上不断膨胀的客户名单，Jared 发现自己坐在桌前，每晚回复客户邮件到九十点。

"管理收件箱几乎是不可能的，"他说。"在此之上还要做外呼，你根本不知道该把重点放在哪里。"

Jared 转向 Claude Code 寻求帮助。没有任何编程经验，他做出了 CLAFTS，即 *Claude Drafts* 的缩写：一个运行在 Gmail 内、使用 Claude API 起草客户邮件回复的应用。经过多次迭代，Jared 估计 CLAFTS 最终每天为他节省两到三个小时。他第二天早上在 Slack 上分享，24 小时内，销售组织的其他人就开始使用它，并取得了类似效果。

这引出了 Jared 在 Anthropic 角色的转变：如今他是 GTM（go-to-market）团队的产品经理，这个角色的全部重心是识别 Anthropic 销售组织运作方式中的问题，并构建由 Claude 驱动的解决方案来修复它们。在这个新角色中，Jared 构建了自动化客户沟通、在通话前调研客户背景、以及从会议记录生成跟进邮件的工具。他随后把它们打包为 [Claude Cowork](https://claude.com/product/cowork) 中的插件，让整个销售团队都能使用。

他把这次职业转变形容为"我经历过的最赋予力量的事"。

以下是 Jared 如何用 Claude 大规模处理收件箱、他接下来在构建什么，以及 GTM 团队可以从他的方法中借鉴的最佳实践。

## **被行政事务淹没的销售代表**

邮件量并不是 Jared 作为客户主管面临的唯一挑战。Anthropic 每 24 到 48 小时就发布产品变更，而客户的问题往往落在最新细节上：batch API 的 SLA、提示缓存折扣、模型定价、SDK 行为。要答得好，就得在 Slack、Google Docs、内部知识库和开发者文档之间搜索——而且日复一日地重做，事实组合还略有不同。

"把技术文档转述给客户相当困难，尤其是在 Anthropic，产品演进得如此之快，"Jared 说。

他最早对 Claude 的实验之一小而实用。Jared 使用 Apps Script（Google 的轻量开发平台）和 Claude，从内部系统拉取产品使用数据，让 Claude 每天早上按增长速度给他的客户账户排序。

"每天 Claude 会给我一份简报，告诉我根据使用量该重点关注谁，"他说。他的名单上有 700 个账户，这份每日简报帮助他决定该把外呼时间花在哪里。

## **开发 CLAFTS**

更难的挑战是 Jared 的收件箱，以及他不得不花在回复邮件上的深夜时光。

借助 Claude Code，他开始开发一个用自己的语气起草客户邮件回复的系统。"Claude Code 后面带着'code'这个词，光是开始就让我有点望而生畏，"他说。"但过了一段时间，我理解了它能接入我的电脑、回答关于其中文件的问题，这种能力有多强大。"

CLAFTS 建立在约 4,300 行代码之上，几乎所有代码都由 Claude Code 编写。它从共享的 Google Drive 文件夹和其他第三方工具中获取上下文，通过网页搜索引用 Anthropic 的公开文档，并匹配 Jared 的写作风格。当他一天结束时打开草稿文件夹，回复已经等在那里待审阅。

每当 Anthropic 发布产品变更，文档就会反映它，Claude 在下一份草稿中就会采纳这一变更。"Claude 能够用网页搜索理解我们网站上的最新文档，并在生成邮件时引用这些材料，"Jared 说。"我不需要把这一切都记在脑子里。"

开箱即用时，Claude 的写作倾向于更长、更多使用模糊措辞，于是 Jared 反复修改系统提示词，直到草稿与自己的写作风格相符。"我大概对 CLAFTS 的系统提示词做了数百次迭代，为我生成不同的写作内容，"他说。

接着，他开发了 CLAFTS Tones 功能，用模式匹配来模仿他在不同关系中的语气。客户、同事和家人的邮件读起来各不相同，草稿会相应调整。

Jared 用个人账户给自己写了一连串越来越愤怒的邮件来测试这个功能。Claude 捕捉到了这种语气，然后拒绝继续下去。

"Claude 开始模仿那种语气，到某个时候我开始遇到拒绝，因为 Claude 不想生成给客户的愤怒邮件，"他说。"那时我就知道 CLAFTS Tones 起作用了。"

### **衡量 CLAFTS 的影响**

虽然 CLAFTS 每周为 Jared 节省 10–15 小时，但他最在意的变化是工作的准确性。由于 Claude 在每份草稿中都从文档中拉取最新产品细节，客户收到的答案与最新发布的内容挂钩，而不是与 Jared 碰巧记得的东西挂钩。

"在 CLAFTS 之前，我觉得自己做的行政工作比真正花在客户身上的时间还多，"Jared 说。"在 CLAFTS 之后，我终于能更多做我想做的事，也就是销售。"

## **扩展 Anthropic 的 GTM 工具包**

除了 Jared，一位经常工作到午夜之后给客户发邮件的 BDR——John Albert——参与共同构建了 CLAFTS。业务开发团队的其他成员在看到同事每天省下几个小时之后也加入了进来。从那以后，宣传推广基本由他们自己完成。

Jared 接下来构建的一组工具，是在日程两端各放一个[技能](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)（skill）：每日简报和每日回顾。

每天早晨，"每日简报"技能读取他的日历，对即将会面的人进行网页搜索，并在第一通电话前生成谈话要点。该技能通过 [MCP 服务器](https://www.anthropic.com/news/model-context-protocol)连接 Google Calendar 和 CRM 数据，拉取每位客户的相关信息。

一天结束时，"每日回顾"技能从 Google Docs 和会议笔记中提取内容，起草跟进邮件，与 CLAFTS 类似。

"把这两者结合起来，你就得到让 Claude 管理日常任务的组合，本质上就变成了一个智能体，"他说。

Jared 的工作现在更深入到智能体领域，他正在试验 [Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview)，把工作流串联起来，让一次 Claude 运行的输出成为下一次运行的输入。

为了确保他用 Claude Code 构建的工具能在他支持的更大团队中规模化使用，他通过 Claude Cowork 发布它们，把技能和 MCP 连接器打包成任何人都能在几分钟内安装的插件。

销售插件发布后的几个月内，Anthropic 销售组织中约 80% 的人都在使用它。剩下的 20% 主要是新员工，Jared 把这视为下一个要解决的挑战，因为这些技能正是为帮助人们更快上手而构建的。

在插件之前，每位新员工都要花几周摸索自己的工作流。现在，新员工可以在第一天安装它，让 20 多个技能直接接入他们使用的工具：Salesforce、Intercom、Gong、Google Calendar、Gmail、Google Drive 和 BigQuery。

两个技能构成销售团队插件的支柱：

1. `/customer-context` 在约 90 秒内跨所有这些来源拉取 360 度的客户账户视图。
2. `/pipeline-management` 呈现有风险的交易、预测指引和推进建议。

这个包还与 Cowork 的调度功能集成，让销售代表可以把技能排入队列自动运行。

"我们的销售人员可以回到有意义的对话中，而不是去更新各种不同的应用，"他说。

## **设计下一步**

Jared 的角色也随着工具一同演变。作为 GTM 架构师（GTM Architect），他现在与产品工程师一起参与设计讨论，帮助为 Anthropic 的销售团队塑造新工具。

"我觉得随着技术壁垒消融，我几乎能设计更多产品，并让资深工程师帮我实现到最后一步，"Jared 说。"我能够增强自己、做更多事情。"

对于想知道自己能否构建类似东西的销售人员，他的建议是打开 Claude Code，找到一个拖慢自己的任务，然后问 Claude 如何为它构建解决方案。

"如果一年前你告诉我我会成为 Anthropic 的 GTM 产品经理，我会相当吃惊，"他说。"我从来没有参与这些对话的技术功底。有了 Claude，我能够设计和构建不仅改善我自己日常工作流、也改善我所在更大团队工作流的东西。我有了更富创造性、更具战略性地工作的空间，而且没有回头路。"

*今天就[开始使用 Claude](https://claude.ai/)。敬请关注"Anthropic 如何使用 Claude"系列的更多故事。*
