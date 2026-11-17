---
title: "Claude Tag 现支持在频道中使用个人连接器"
title_en: "Claude Tag now supports personal connectors in channels"
date: 2026-09-24
source: https://claude.com/resources/articles/claude-tag-now-supports-personal-connectors-in-channels
crawled: 2026-11-17
translated: 2026-11-17
---

# Claude Tag 现支持在频道中使用个人连接器

> 原文：[Claude Tag now supports personal connectors in channels](https://claude.com/resources/articles/claude-tag-now-supports-personal-connectors-in-channels) · Claude 博客

Claude Tag 现在可以为你本人在频道中发起的请求使用你的连接器。其他人无法使用它们，输出如何呈现也由你掌控。

[Claude Tag（测试版）](https://claude.com/product/tag)让你可以把 Claude 加入 Slack 频道，与你的团队[并肩工作](https://claude.com/resources/articles/claude-tag-guide-for-startups)。此前，Claude 只能使用[管理员为频道挂接的连接器](https://claude.com/resources/articles/agent-identity-access-model)，而大多数组织会有意让这份清单保持很短：他们希望访问权限跟随人，而不是跟随频道。

现在，Claude 可以为你本人在频道中发起的请求使用你自己的[连接器](https://claude.com/docs/claude-tag/concepts/settings-map)。例如你的日历、你的云盘、CRM 中分配给你的客户账号，或你的预发布部署环境。只要你[已将其连接到自己的 Claude 账号](http://claude.ai/customize)，就能在频道中使用它。

当你让 Claude 访问你的连接器时，由你决定信息以何种方式呈现。你可以先审阅每一条回复再发布。或者，你可以使用自动模式自动发布——除非 Claude 判断存在需要你审阅的敏感内容。在 Enterprise 套餐中，管理员将能够要求所有人必须审阅。

个人连接器为管理员提供了更多治理选项。他们可以在某个智能体身份下提供一组共享工具的访问权限，让频道成员只使用个人连接器、从而依赖现有的基于角色的访问控制，或逐个工具地做出决定。

Claude Tag 中的个人连接器现已在 Team 套餐中推出，Enterprise 即将跟进。

## **使用个人连接器**

人们在频道中需要的大部分信息都藏在各自的登录之后：一个适合你日历的时间、你正在推进的交易、一份只有你能打开的方案。现在，你也可以在频道中获取这些信息了。

例如，#checkout-migration 频道（已连接 GitHub）中的 Priya 问道：“@Claude，把我 Google Drive 里的文档‘Checkout migration, Q3’与我们已上线的部分对照一下。还有哪些没完成？”

![](https://assets.claude.com/de1942de3fd966774ee0a9d7293fd9bd3477e1c4.png)

Priya 在 #checkout-migration 中请 Claude 把她的计划与已上线的内容对照。该频道接入了 GitHub。只有 Priya 能打开这份文档。

Claude 通过该频道的 GitHub 连接器读取已合并的拉取请求。那份文档只有 Priya 能打开。换作以前，Claude 只能到此为止。

现在，Claude 通过 Priya 的 Google Drive 连接器读取该文档——这与频道自身的工作相互独立——并发布已上线和尚未完成的内容。Priya 的计划并不敏感，因此她使用自动模式，由 Claude 在发布前对该对照结果进行筛查。如果是她希望先自行核对的文档，她可以切换到审阅模式，在频道看到之前先查看回复。

![](https://assets.claude.com/cff3d307d116b93a1370e70074c0102e3e2cfc97.png)

同一个话题串。Claude 带有对照结果的回复，以及在实际发布前显示将要发布内容的审阅提示。

Claude 通过你的连接器所做的一切都会出现在该工具自己的日志中、记在你的账号名下，与你目前使用私信时一样。频道自身的工作仍记在它的服务账号下，这正是你的安全团队已经在跟踪的那个账号。

你可以决定 Claude 能访问什么、频道能看到什么，与你使用私信中的连接器时相同，并且你可以随时断开某个连接器。

## **频道自身连接器仍然重要的场景**

个人连接器不会在无人值守的情况下运行。定时例程以及 Claude 自主发起的任何操作，都使用管理员挂接到频道的连接器。无人值守操作所需的工具，或整个频道都依赖的操作，应当使用共享连接器。

例如，你可能想把 Claude 加入 [#on-call 频道，协助进行 CI 分诊和响应](https://claude.com/resources/articles/ai-ci-cd-on-call)。如果你为运行手册、监控工具和部署历史设置了共享连接器，Claude 就能识别并协助修复问题（即使在非工作时间）。

仅依赖个人连接器的频道适合受到密切监督的工作。例如，协作起草一份 RFP 回复，可能需要从定价或其他敏感来源调取数据，而这些数据并未向整个频道开放。Claude 发布的任何内容对频道中的所有人可见。

## **下一步**

无需安装任何东西。当你的某个请求需要用到你的某个连接器时，Claude 会在第一次询问你，之后就会在该话题串中使用它。

在频道中 @Claude，获取只有你能访问的信息。进一步了解 [Claude Tag](https://claude.com/product/tag)。
