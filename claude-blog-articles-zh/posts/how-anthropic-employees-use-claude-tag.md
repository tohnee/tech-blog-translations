---
title: "Anthropic 员工如何使用 Claude Tag"
title_en: "How Anthropic employees use Claude Tag"
date: 2026-08-28
author: Aleksandra Todorova
source: https://claude.com/resources/articles/how-anthropic-employees-use-claude-tag
crawled: 2026-11-17
translated: 2026-11-17
---

# Anthropic 员工如何使用 Claude Tag

> 原文：[How Anthropic employees use Claude Tag](https://claude.com/resources/articles/how-anthropic-employees-use-claude-tag) · Claude 博客

*制作可直接交付客户的物料、汇总每周问题报告、执行法律审查——全都在工作原本发生的地方完成。*

[Claude Tag](https://www.anthropic.com/news/introducing-claude-tag) 把 Claude 带入 Slack 这类聊天工具：你可以像 @ 一位同事那样，在对话串里 @Claude，它会读取对话上下文、完成任务，并把答案或结果发回该对话串。它还能[跟进对话](https://claude.com/resources/articles/claude-tag-now-reads-even-more-of-the-room)，并结合可用上下文、记忆以及被授予的常驻指令，自行判断何时参与聊天。过去几个月里，Anthropic 的各个团队一直在用 Claude Tag 在共享频道中[自助完成数据分析](https://claude.com/resources/articles/self-service-data-analytics-in-slack-how-anthropic-deploys-claude-tag-for-ad-hoc-questions)、处理支持工单，或帮助定位棘手 bug 的[根本原因](https://www.anthropic.com/news/introducing-claude-tag)。

我们整理了一份[包含十多个 Claude Tag 用例示例](https://claude.com/docs/claude-tag/users/use-cases)的清单，灵感来自我们在 Anthropic 的工作，并附有具体提示词和设置说明。本文重点介绍 Anthropic 员工用 Claude Tag 提升工作流与流程效率的三种方式，以及他们使用的提示词，供你借用或调整成最适合自己工作的版本。

## 把 Slack 对话串变成一份打磨好的文档

在最近一次功能发布期间，一位销售代表需要一份非技术性物料，向客户和潜在客户解释该功能如何运作；产品营销团队的 Hema Thanki 在 45 分钟内，就把随后的 Slack 对话串变成了一份可供评审的文档。

那个 Slack 对话串有 15 条以上消息，多人插话提出建议或补充需求，围绕「到底需要什么」以及「现有技术材料是否足够」还带着一点紧张气氛。Hema 没有去澄清这些模糊之处，而是直接在对话串里 @ 了 Claude：

`@Claude, go through this Slack thread and come up with a one pager that [the requester] is asking for.`

![](https://assets.claude.com/cd6e52d544d5810794a2a25fd2d232f5beb22fdb.png)

让 Claude 基于一段 Slack 对话串生成营销物料。此图片为说明用例而生成，不含真实信息。

Claude 在大约两分钟内生成了一份两页草稿，涵盖该功能的通俗说明、其商业价值、实施涉及的内容，以及一个提供更详细信息的附录。

接下来，Hema 要求 Claude 核实其内容：

`@Claude, is everything in this doc factual and correct?`

Claude 把文档中的表述分为两类：一类已对照公开文档得到验证，另一类是它自己的措辞，后者被标记为需要产品负责人签字确认。Hema 提供了两份包含相关信息的官方资料，Claude 据此改写了一个章节，使其与这些资料中已获批的措辞一致。

![](https://assets.claude.com/b1a32b3705407471a5fdd9d472361a56725ab419.png)

对 Claude 的后续指令同样发生在 Slack 里。此图片为说明用例而生成，不含真实信息。

此时 Hema 注意到，被截断的对话串让框架出现了偏差，于是她粘贴了更完整的上下文。她与 Claude 来回迭代，总共出了四个版本。在首次提出需求约 45 分钟后，她把文档分享给该功能的产品负责人评审。Hema 没有把时间花在数小时的研究和起草上，而是用于质疑准确性、提供信息来源、决定纳入哪些信息——这些都是需要人类判断的任务，也让这份客户资产变得更强。

除了从 Slack 对话串生成简报，Hema 在日常工作中也使用 Claude Tag。她与 Claude 共用一个私有 Slack 频道，在不同对话串中提出请求，像 @ 同事一样 @Claude。在这个频道里，Claude 会阅读她粘贴或附上的任何内容，搜索 Slack 工作区和公开文档，并在后台工作，发布一份随进度更新的检查清单。Claude 的访问权限是刻意限定范围的：它只能使用[被授予访问权限](https://claude.com/resources/articles/agent-identity-access-model)的频道和文档，如果无法访问这些资源，它会告诉她。

## 汇总并跟进散落在各个 Slack 频道中的需求

新功能发布时，销售代表通常会持续跟踪，并把消息传达给那些曾提出该功能需求、由他们负责的客户。这些需求通过 Slack 或产品反馈中心传达，可能散落在长达数月的历史记录中。产品战略与运营团队的 Steph Soderborg 得以把与一项即将发布功能相关的所有需求汇总起来，并直接通知每一位代表客户提出需求的销售代表，整个过程约 26 分钟。

首先，Steph 给 Claude 发去搜索目标、一句话的匹配定义，以及一份她想要的输出示例——上一次发布时整理出的七条目清单：

`@Claude We are about to GA [a new feature]. Can you search Slack ... find me anyone who has asked for this functionality for their customer ... include their Slack handle and team, the account that asked for this, and link the ask from Slack.`

Claude 在多个频道以及整个工作区运行了约 20 种搜索变体。产品反馈中心阻止了它的直接访问，于是它转而通过 Slack 的交叉引用找出反馈中心的条目，并把另一个内部助手此前发布的第一版清单合并进来，对两份结果做了去重。整合后的清单在约 26 分钟后返回，涵盖约 24 个客户账户，每个需求方一行，包含其 Slack 用户名、团队、账户，以及指向原始需求的链接。

![](https://assets.claude.com/96945facf5688f10a4116c1f22bf8ff58f7e8a1f.png)

让 Claude 生成一份清单，列出所有在 Slack 中提出过某项功能需求的人。此图片为说明用例而生成，不含真实信息。

随后，Steph 又交给 Claude 一项规模更大的汇总工作——这项工作她此前根本没有余力自己完成：她想要一幅全景图，涵盖企业客户在过去一周报告的所有产品问题，包括哪里坏了、哪些已经修复，以及哪些报告（如果有）指向同一个底层问题。她让 Claude 读取所有涉及事故、升级、支持和产品反馈的 Slack 频道；大约 50 分钟后，Claude 发布了一份按产品领域组织的报告，包含 23 个仍待解决的问题和 14 个已解决的问题，是从约 120 条原始发现中凝练出来的。每个问题都附有摘要和指向来源对话串的链接。Steph 随后要求 Claude 复查自己的工作，Claude 又发现了 15 个问题。

Steph 估计，梳理、分析并综合如此大量的信息，至少需要她一周的全职工作，或者这项工作根本永远不会有人去做。而借助 Claude Tag，她只用几分钟就把需求表述清楚，Claude 则在后台完成工作。

Steph 也会在私有频道中与 Claude 协作，一开始就发去完整指令，包括在哪里搜索、什么算作匹配，通常还会附上一份输出格式示例。Claude 会搜索工作区、读取它受邀加入的频道，并在工作过程中发布进度更新。当反馈中心阻止访问时，Claude 会尝试通过可访问的文档和频道收集相关或有用的信息，甚至请求获得这些频道的访问权限。

## 加速法律文件审查

Anthropic 的法务团队会在每篇博客、落地页、邮件或其他任何物料公开发布前进行审查。在产品发布前的几天里，营销团队可能会在紧迫的截止期限下排队提交数十份不同资产等待审查。这还不包括流经审查队列的其他所有营销物料——从一段话的社交文案，到 2,500 词的博客草稿、带十几个标签页的规划文档，以及覆盖多个触点、包含多个版本的邮件系列。法务团队的产品法务顾问 Molly Villagra 创建了一个专门的 Slack 频道，让 Claude Tag 先审查每一份营销资产，把营销法务审查的周转时间从一天（或更久）压缩到每份资产 30 分钟。

为了申请法务审查，营销人员会在该 Slack 频道中发布文档链接；Molly 没有工程背景，却为 Claude 设置了具体的规则和指令。Claude 不仅能指出法律层面的问题（例如缺乏依据的营销声明），还能帮助核查营销内容中的事实陈述，因为它可以访问公司 Slack、内部知识索引和公开网络。如果发现问题，Claude 会列出这些标记，并附上具体的处理说明，直接与请求者协作解决。对于仍需法务签字确认的遗留问题，Claude 会 @ 相应的产品法务顾问，后者可以快速审阅被标记的表述。

![](https://assets.claude.com/96c9ecf2f2b83550f60188647cd55f738e11b17b.png)

营销人员在专门的 Slack 频道中发布文档链接以申请法务审查。此图片为说明用例而生成，不含真实信息。

例如，在最近一次新闻通讯审查中，Claude 标记了三个关键事项；仅仅几分钟后，它就未经提示地解决了其中一项——因为它在内部文档中找到了所需信息。Molly 希望把它变成默认行为，于是在营销法务审查频道中 @Claude：

`Your three bullets are good callouts, but they can all be verified by you. Will you try to verify these things in real time when you flag them in the future?`

应 Molly 的要求，Claude Tag 把这条新指令加入了它在今后所有审查中遵循的指令集，使它能够借助频道反馈实时改进。

这个反馈循环启发了 Molly 创建一项新的例行任务（routine）：让 Claude 每周五审阅本周的法务顾问反馈，并针对共享指令提出更新建议，供她审批。

我们上面分享的每一个工作流，都为 Anthropic 员工节省了数小时乃至数天的工作，并让一些原本根本不会发生的项目得以推进。你的团队会最先把手头的哪些工作流或项目交给 Claude？

Claude Tag 目前处于公开测试阶段，已在 Anthropic 第一方服务的 Team 和 Enterprise 方案中提供。可在 [claude.ai/admin-settings/claude-tag](https://claude.ai/admin-settings/claude-tag) 为你的工作区完成设置，或访问 [claude.com/docs/claude-tag](https://claude.com/docs/claude-tag) 了解更多。

*本文中的周转时间反映的是个别员工在特定任务上的体验；结果会因任务、所连接的工具以及 Claude Tag 的设置方式而异。*

*所有图片均为说明用例而生成，不含真实姓名或信息。*
