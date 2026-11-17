---
title: "Claude Cowork 上手指南：最佳实践"
title_en: "Best practices for getting started with Claude Cowork"
date: 2026-06-03
source: https://claude.com/resources/articles/best-practices-for-getting-started-with-claude-cowork
crawled: 2026-11-17
translated: 2026-11-17
---

# Claude Cowork 上手指南：最佳实践

*Anthropic 增长营销负责人 Austin Lau 讲解何时该用 Claude Cowork、如何判断哪些工作流可以委派，以及上手的具体步骤。6 月 4 日，Austin 将分享他如何用 Claude Cowork 做营销。*

[报名参加网络研讨会](https://claude.com/resources/webinars/how-anthropics-marketing-team-uses-claude-cowork)

2024 年，我们的 Claude 还待在一个聊天窗口里。你提一个问题，得到一个答案，但把答案变成有用的东西，得靠你自己。2025 年，Claude Code 让工程师的交付速度提升到让我们其他人有点羡慕的程度。

今年，我们所有人都能靠 [Claude Cowork](https://claude.com/product/cowork) 追上了。

去年我开始用 Claude Code 处理那些聊天应付不来的长链条、多步骤任务。一周之内，我就从「不知道终端是什么」变成能搭建出[在 30 秒内完成 30 分钟任务的 Claude Code 工作流](https://claude.com/resources/articles/how-anthropic-uses-claude-marketing)。我当时是用 Claude Code 做非技术工作，因为那时 Claude Cowork 还不存在。

如今，我 90% 的工作都在 [Claude Cowork](https://claude.com/product/cowork) 里完成。本文会告诉你如何判断哪些任务该交给它，带你走一遍我自己的真实例子，并让你在大约十分钟内做出第一个完成的交付物。

## Chat、Claude Cowork 与 Claude Code 怎么选

如果你的工作属于非技术性的知识工作——邮件、幻灯片、电子表格、文档、会议，以及「你能帮我把这个总结一下吗」——那么 Claude Cowork 就是为你准备的。你不需要会写代码，也不需要知道什么是「智能体」、更不需要会构建一个。

如果你过去两年一直是开着 AI 聊天标签页，和另外 100 个标签页、文件挤在一起，把提示词或问题复制进去、再把答案复制出来，那你已经会用 Claude Cowork 了。它就是那样，只是不用再复制粘贴。

Chat、Claude Cowork、Claude Code、Claude Design，以及 Claude 出现的其他任何地方，背后都是同样的 Claude 模型。它们是供你处理不同类型工作的独立工作空间，但运行的都是同一批模型。下面这个框架可以帮助你判断何时该用哪一个：

* **Chat**：这往往是知识工作者认识 Claude 的入口。你把已有的东西拿给 Claude：上传一个文件、粘贴一段文字、描述一下情况，然后得到答案。Chat 适合求答案、头脑风暴，以及把想法说出来。
* **Claude Cowork**（在 Claude 桌面应用中）把这件事反过来。不是把你的工作带给 Claude，而是把 Claude 带到你的工作里。你把它指向电脑上的某个文件夹，把它连接到你已经在用的应用，然后告诉它你想完成什么。用 Claude Cowork，你描述一个结果，走开一会儿，回来时工作已经完成。
* **Claude Code** 是为开发和交付软件的开发者打造的。如果你的工作活在代码里，就从那里开始。

很多人不知道，Claude Cowork 和 Claude Code 底层运行在同一个[引擎](https://code.claude.com/docs/en/how-claude-code-works)上。

### 什么时候该用 Claude Cowork？

搞清楚何时用 Claude Cowork、何时用 Chat，是大多数人卡住的地方，所以这是我的经验法则：

* **用 Chat**：如果你要的东西几次来回就能搞定，比如一个问题、一段解释、一次头脑风暴，或一个直觉校验。
* **用 Claude Cowork**：如果你要的是一个交付物，比如一个别人会打开的文件、一个别人会演示的幻灯片，或一张要整理好的电子表格。凡是多步骤的、涉及一个以上文件/文件类型或一个以上应用的，或者你会把它描述为「一项任务」而非「一个问题」的，都用它。用 Claude Cowork，你是在把工作**委派**给 Claude。

几个例子可以看清这条界线在哪：

| 示例问题或任务 | 使用 |
| --- | --- |
| 我们的业务复盘会上该讲些什么？ | Chat |
| 读一下这个 Google Drive 文件夹里最近三个月的会议记录，用我们的模板给我做一份 QBR 幻灯片。 | Claude Cowork |
| VLOOKUP 该怎么用？ | Chat |
| 把我所有电子表格里的 VLOOKUP 都改成 INDEX MATCH。 | Claude Cowork |
| 给这个页面推荐一个更好的 title tag 和 meta description。 | Chat |
| 按这张表里的新 title tag 和 meta description，更新这 30 个页面，用 CMS 连接器完成。 | Claude Cowork |

最常见的错误是凡事都用 Chat，于是永远体会不到 Claude Cowork 能带来的差别。另一个相反的错误是拿 Claude Cowork 处理一次性的小问题，然后干等着——而这类问题 Chat 五秒就能答完。

### 适合 Claude Cowork 的任务的五个要素

刚开始时如果你不确定哪些项目该委派给 Claude Cowork，可以把它们过一遍这份清单。你不必五项全中，但一个合适的候选任务通常能命中其中几项：

1. **输入不止一样东西。** 多个文件、一整个文件夹，或一个文件加若干连接器。如果只有一个输入，Chat 多半就够用了（不过你还是应该试试）。
2. **产出一个文件。** 你需要一个可以附件发送、演示、分享或二次利用的交付物：一份文档、一套幻灯片、一张电子表格或一个 CSV。
3. **你还会再做一次。** 一次性任务也行，但周期性任务才是甜点区。你可以把它排进日程，在你还没坐到桌前就先跑起来。
4. **你已经清楚「好」是什么样。** 你熟悉产出的形态，所以能在 15 秒内判断输出是对、是错，还是完成了七成。
5. **中间过程是无聊的部分。** 思考发生在开头（决定你想要什么）和结尾（判断结果对不对）。中间的一切（抽取、汇编、核对、重新排版）才是你交出去的部分。

## 我在 Anthropic 如何使用 Claude Cowork

我在 Anthropic 负责增长营销，所以我的例子都偏营销味。别指望照抄其中某个工作流——长期看那样帮不上忙。请留意每一个例子是如何命中上面清单中的几项的，因为那正是你要在自己的 Claude Cowork 工作流里寻找的模式。

### 每日简报

营销人员每天收到的 Slack 频道消息和邮件数量足以把人淹没。我有一个「每日简报」任务，每天早上 6 点运行。Claude Cowork 连着我的 Slack 和 Gmail，我的提示词让它检查未读邮件和我关心的频道，把它们分门别类，并生成一份简短报告。

![](https://assets.claude.com/481d42a0f045f1e716e1f9f6f6571476157f2aab.png)

这份报告给我一份「该看什么」的 TLDR、按类型归组的已标记邮件、频道摘要，以及任何可能影响营销的夜间产品事件。任何被 Slack 和邮件淹没的人都能跑一个这个工作流的变体。

### 预算投放节奏

我的工作之一是为效果营销做预算投放节奏（budget pacing）。这是没人愿意干的活，因为既无聊又琐碎。许多效果营销团队会在 Google Sheets 里跟踪每日花费和消耗速率，以估算达成目标的节奏。你要么手工从每个渠道导出每日花费、再粘贴进表格，要么花钱买第三方工具替你抽取、转换和加载数据。

![](https://assets.claude.com/4b0a081e502fc09bfc252fd2c23ea16347bc8dfd.png)

用 Claude Cowork，我连上 Google Ads 和 Meta Ads，在桌面应用里创建一个实时产物（本质上是一个 HTML 仪表盘），它会自动拉取我的每日花费并替我计算投放节奏。我也可以用大白话直接告诉 Claude 如何筛选我的广告系列、要注意什么。

拿它对照上面的清单：多种来源进（每个渠道的花费），一个文件出（这里就是仪表盘），我不断重跑它，而中间那套流程正是那种无脑、吸干灵魂的「下载—复制—粘贴」苦役，我绝对不想自己动手。由于广告平台是通过我的连接器接入的，我随时都能更新这个仪表盘。

### 报表

与其导出一堆 CSV 再手工做数据透视表或拼接文件，我让 Claude Cowork 连上 Google Search Console。它会拉取我关心的数据（查询词、国家、页面），核对后合并进一张表——而不是像 Google 那样在你手动导出时每个维度给你一个 CSV。

![](https://assets.claude.com/e7b3f3c2e2b7d73dd1e4b95da1889b53df0cfb57.png)

我还会把重点告诉 Claude，比如对比最近七天与此前七天、只筛选特定国家、标出任何显著变化，并按我想要的模板撰写报告。之后我可以进一步调整任何内容，或向 Claude 追问。

![](https://assets.claude.com/a4239b970dff8e06581af6dacb876de8c9e917af.png)

借助 Claude Cowork 的定时能力，这件事每周自动运行。报表过去每周要花我约 30 分钟，现在只要五分钟，而且我把这五分钟花在真正需要我判断的部分：补上缺失的背景，打磨要点评述。

这些只是我使用 Claude Cowork 的部分例子，但不过略窥一斑。可以看看我写的另一篇文章，其中更详细地走查了[另一个复杂用例](https://www.linkedin.com/feed/update/urn:li:activity:7448056387772833795/)，涉及插件、技能、本地 MCP 和 [Dispatch](https://support.claude.com/en/articles/13947068-assign-tasks-from-anywhere-in-claude-cowork)，还有更多最佳实践。

## 用 Claude Cowork 的头 10 分钟

第一次打开这个应用？下面这样起步：

1. 打开 Claude 桌面应用，切到 Claude Cowork 标签页。
2. 给 Claude 一些可以着手的材料。拖进几个文件、把它指向电脑上的某个文件夹，或者连接一个你常用的应用（Slack、Gmail、Notion、CRM 等）。Claude Cowork 的产出是平庸还是出色，差别几乎从来不在你的提示词，而在于你是否提供了足够丰富的上下文供它工作。
3. 告诉 Claude 你想要的结果。描述你最终想要的交付物，并提供必要的背景。
4. 从一个你非常熟悉、真实的任务开始。你会立刻看到它强在哪、哪里需要你补充上下文，而你也早就知道这件事的「好」是什么样。
5. 让 Claude 在动手前先问你问题。这是我养成的最有用的一个习惯。把这句话加进你的提示词：*在我们开始之前，把我的需求复述一遍，确认我们的理解一致，然后尽可能多地问我澄清问题。*

这会暴露出你没想到要说明的东西：比如我们看的是哪个时间段、这里的「好」指什么，或者你知道哪些 Claude 不知道的边界情况。陷阱在于假定 Claude 已经知道那些对你显而易见的事。提前回答五个问题只花你 30 秒；事后才发现同样的缺口，既费时间又费 token，而且修起来很痛苦。

还是不确定该交出去什么？问 Claude。Claude 有记忆，也能检索你过去的对话，所以你可以问它：你最常做哪些任务、哪些值得拿到 Claude Cowork 里试试。

![](https://assets.claude.com/165fc0fddf6ae311f0b915883469ee1982e4bbc5.png)

### 我仍然会用 Chat 的场合

我依然大量使用 Chat 来梳理定位问题、在拍板前对自己的想法做压力测试，或者问些没头没脑的问题，比如我家狗为什么老是舔床。

重点不是说 Chat 是「旧」东西。当输出是你脑袋里的一个想法时，用 Chat；当输出是你要交给别人的东西时，用 Claude Cowork。

## 去动手做点东西

挑一件你每周都做的重复性任务，试着用 [Claude Cowork](https://claude.com/product/cowork) 来做，看看它交回什么。头几个任务可能会有点别扭，但试过几次之后，你会很快从「我该怎么用它」变成「下一步该交给它什么」。

*本文由 Anthropic 增长团队的 Austin Lau 撰写，表达的是他个人对 Claude Cowork 的观点、使用模式与建议。*
