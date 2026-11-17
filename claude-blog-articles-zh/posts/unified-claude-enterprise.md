---
title: "Claude Cowork 与聊天在 Claude Enterprise 中合而为一"
title_en: "Claude Cowork and chat come together for Enterprise"
date: 2026-10-23
source: https://claude.com/resources/articles/unified-claude-enterprise
crawled: 2026-11-17
translated: 2026-11-17
---

# Claude Cowork 与聊天在 Claude Enterprise 中合而为一

> 原文：[Claude Cowork and chat come together for Enterprise](https://claude.com/resources/articles/unified-claude-enterprise) · Claude 博客

*编者注：本文内容写于 2026 年 10 月 30 日之前，文中提到的 Max 涵盖如今已分为 Max 和 Ultra 的套餐。*

聊天与 Cowork 于今年 9 月率先在 Pro 和 Max 套餐中[合而为一](https://claude.com/resources/articles/cowork-is-now-claude)。如今，同样的统一 Claude 体验已在 Claude Enterprise 套餐中正式可用。

在网页端、桌面端和移动端，聊天与 Cowork 如今已是同一个 Claude，你的团队可以在同一段对话里既问一个简单问题，也交出一整个项目。智能体式的工作在 Anthropic 托管的云环境中运行，[Claude Enterprise 管理员](https://claude.com/resources/webinars/unified-claude-what-it-means-for-admins)可以按角色控制访问权限，并借助新的高效模式（Efficient mode）管理用量。

## 一个 Claude，应对所有任务

团队成员在开始用 Claude 工作之前，不必再在聊天和 Cowork 之间做选择。对话从聊天开始，简单的问题依然能快速得到回答。当任务需要运行代码或处理文件时，Claude 会在云端继续工作，并返回完成的文档、分析或演示文稿。由于工作在云端运行，即使有人合上笔记本电脑，它也会继续进行，之后可以在网页端、桌面端或移动端接着处理。聊天、项目、连接器、技能和插件都会延续到新的统一体验中。

各组织已经在团队中体会到统一 Claude 体验带来的价值：

![DXC](https://assets.claude.com/a6cc538462d716535ab150bb67609835002f2376.svg)

> "在聊天和 Cowork 的能力合并之前，它们是两套必须分别使用、分别管理的独立体验。把它们合到一起让一切都变简单了，对用户和管理员都是如此。过渡非常顺畅，我们的连接器、技能和 MCP 都没有出问题，我们有信心把它推广到更大范围。"

Daniel Padilla，LabX 首席技术官

![LifeMoves](https://assets.claude.com/3bf5eaab2f0360b235789384c0f4535f6e7f7258.png)

> "我们不再需要在聊天和 Cowork 之间做选择。只用了不到十分钟的提示，Claude 就梳理了大批县、州和联邦预算以及公开会议文件，理清了各项资金流之间的关联，并生成了一份我们团队原本要花数周才能完成的综合报告。我自始至终都不必决定哪一步该用哪个工具。那份报告将影响我们的战略规划和即将到来的预算流程。"

Paul Simpson，首席财务官兼技术负责人

![Quantium](https://assets.claude.com/0e6b8d1ab806b1a949b793cce5bc3b294fe8d88c.svg)

> "把聊天和 Cowork 合在一起，回答了客户一直在问我们的问题：'我该用哪个 Claude'、'哪个负责做什么'。它会适配你在移动端、桌面端和浏览器上的工作方式与场所。在 Quantium，它正帮助我们扩大自身的 AI 抱负，以及我们能为客户做的事。"

Harley Barnes，AI 技术执行经理

![Carvana](https://assets.claude.com/6d55e4e27973e13fce3e66d63ef5618d65cb12ae.svg)

> "在 Carvana，工作并不只发生在办公桌后。统一的 Claude 体验让员工可以在电脑上开始一项任务，再在手机上接着做，并在 Claude 有结果或需要他们输入时收到通知。无论团队是在工位还是到现场走访，它都契合我们的工作方式。"

Charles Sellers，工程高级总监

## 维持安全

如果你的组织已经批准使用 Claude 聊天，那么这次统一是建立在你们现有的企业管控措施之上的，包括单点登录（SSO）和 Compliance API。Anthropic 仍会对传输中和静态的数据进行加密，并且默认不会将其用于模型训练。

Claude 在云会话中执行智能体式的工作，每个会话都运行在自己独立的虚拟机中：对 Claude Enterprise 而言，网络出口默认关闭，连接器凭据则保存在沙箱之外。由于这些工作统一运行在 Anthropic 管理的环境中，你的安全团队可以集中查看并管控它。Anthropic 信任中心上的[安全最佳实践指南](https://trust.anthropic.com/resources?s=3puokpm2aa1nn24nbcp0l&name=unified-claude-security-best-practices)涵盖了完整架构。

## 管理成本

Claude Enterprise 的定价仍按用量计费。最新的 Claude 模型比前代更高效：按用量计费时，在典型工作负载下，Claude Opus 5.5 的[运行成本比 Claude Opus 5 低 40%](https://claude.dev/blog/what-a-task-costs-on-opus-5-5/)，而对大多数工作而言，Claude Sonnet 5.5 的成本比 Claude Sonnet 5 最多低 30%。

视任务而定，智能体式工作可能比一次快速聊天消耗更多 token。Claude Enterprise 管理员有四种管控用量的手段。高效模式是一项新设置，可将统一的 Claude 体验限定在 Sonnet 和 Haiku 模型上。模型授权（model entitlements）决定每个角色可以使用哪些模型。[消费上限](https://claude.com/resources/articles/giving-admins-more-visibility-and-control-over-claude-usage-and-spend)适用于组织、分组和成员级别，分组共享预算则为一个分组提供一笔每月共享的额度供其支取。

## 开始使用

统一的 Claude 体验即日起在 Claude Enterprise 套餐中正式可用。管理员可以在组织设置中管理推广范围。对 Claude Code 采用零数据保留、使用符合 HIPAA 要求的配置，或使用客户自管加密密钥的组织，将继续沿用当前配置。

详情请参阅[管理员设置指南](https://support.claude.com/en/articles/17444462)。如果你是现有的 Claude Enterprise 客户，你会收到一封关于贵组织推广安排的邮件。
