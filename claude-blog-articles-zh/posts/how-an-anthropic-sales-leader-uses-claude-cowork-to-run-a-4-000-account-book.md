---
title: "Anthropic 一位销售负责人如何用 Claude Cowork 管理 4,000 个账户"
title_en: "How an Anthropic sales leader uses Claude Cowork to run a 4,000-account book"
date: 2026-05-20
source: https://claude.com/resources/articles/how-an-anthropic-sales-leader-uses-claude-cowork-to-run-a-4-000-account-book
crawled: 2026-11-17
translated: 2026-11-17
---

# Anthropic 一位销售负责人如何用 Claude Cowork 管理 4,000 个账户

> 原文：[How an Anthropic sales leader uses Claude Cowork to run a 4,000-account book](https://claude.com/resources/articles/how-an-anthropic-sales-leader-uses-claude-cowork-to-run-a-4-000-account-book) · Claude 博客

*Anthropic 美国中端市场 GTM 负责人 Travis Bryant 分享他如何用 [Claude Cowork](https://claude.com/product/cowork) 准备客户简报和每周预测，并运行一项过去需要跨职能团队投入数百小时的隔夜销售区域评分。*

Travis 详细介绍了自己如何使用 Claude Cowork 准备客户简报、提取每周预测，并在一夜之间为 4,000 个账户评分。

[参加网络研讨会](https://claude.com/resources/webinars/how-anthropics-sales-leader-runs-his-week-with-claude)

在销售领导岗位上，工作核心是做出判断：把团队的时间投在哪里，以及如何向管理层说明本季度的走势。围绕这些决策的工作——比如从四个系统汇总数据，以及每次数字刷新后重新建立基线——过去会占掉我一周的大部分时间。[Claude Cowork](https://claude.com/product/cowork)改变了这种平衡：它负责数据汇总和重新排版，让我能把更多时间投入到客户沟通和战略决策上。

我负责 Anthropic 的美国中端市场 GTM（go-to-market），这意味着我要管理 4,000 个账户，分属中端市场科技与行业两个板块。中端市场包括那些已经不再是初创公司、但尚未成为大型企业的科技公司。行业板块则覆盖其余所有客户，从金融服务、医疗健康到零售和制造。

我的工作横跨三种节奏：每日客户通话准备、每周向 Anthropic 销售管理层汇总的预测，以及每季度覆盖全部 4,000 个账户的销售区域和潜在客户名单工作。每一项本身都是大量工作，而要把三者都做好，过去几乎不可能。

我试过 Claude Code，但一直不太适应在终端里工作。Claude Cowork 把同一套引擎包在我能上手操作的界面里。那一刻我豁然开朗：我终于有办法把工作交出去，并且相信它能被完成。

## **我每天、每周、每季度在 Claude Cowork 中运行什么**

我从 Claude Cowork 节省下来的时间，大部分来自它为我运行的、每天约 90 分钟的小胜利，也就是微优化。

每天早晨，一个定时任务会运行一项[技能](https://claude.com/skills)，扫描我的 Google 日历，为任何缺少会议室的对外会议预订会议室。第二项技能会在每次会议前运行客户通话准备，从 BigQuery 拉取支出数据、从 Salesforce 拉取商机状态，汇总成一份简报，等我打开笔记本电脑时已经准备就绪。调度器比技能本身更像真正的解锁点。一旦准备流程不再是我必须记得去敲的斜杠命令，而是自行运行，我就不会忘记了。

周五的预测工作是更高一档的收益，每周能为我节省约三个小时。一项定时技能会从 Salesforce 的 Forecast 选项卡拉取商机记录和已提交的预测承诺，从 BigQuery 拉取 token 支出，再从几份内部文档中提取备注。它会按照 Anthropic 销售管理层希望阅读的精确格式，汇总成一份单页网页报告：核心指标、重点交易、上升与下滑的客户，以及从每位一线经理逐级汇总的预测快照。该技能会在周一预测电话会之前把页面部署到一个内部共享链接。我周一的工作是补充评论：Claude 构建“是什么”，我负责“为什么”。

我通过 Claude Cowork 运行的最大项目，是为整个中端市场板块做账户倾向评分。每个财年，账户盘中的每个账户都需要一个评分，帮助对应客户经理（AE）排定销售区域的优先级。在以前的公司和岗位上，这类工作需要 RevOps、FP&A 和市场营销投入数百小时。我只用了一个晚上。

我先和 Claude 定义了两套五维评分标准：一套用于科技账户，一套用于行业账户。科技账户的维度是智能体机会、内部转型、AI 承诺、相对于现有支出的空白空间，以及行业契合度。行业账户使用另一套标准，维度包括知识工作者密度（例如律所可能非常高，而制造业较低，因为很多员工在车间工作），以及通过公司公开招聘页面的提及情况衡量的公开 AI 承诺。

标准确定后，我把 4,000 个账户的名单交给 Claude Cowork。Claude Cowork 通宵运行，借助深度网络研究、Salesforce 数据和 BigQuery 数据，逐一为每个账户评分，为每个维度给出数值评分和书面理由。然后我让 Claude Cowork 根据结果构建一个交互式仪表盘。每位 AE 点击进入自己销售区域对应的饼图区块，就能看到账户按评分排序，并附有每个维度生成的理由。将鼠标悬停在账户上，会显示潜在用例和可用于拓客的同类案例研究。仪表盘把评分从一次数据练习变成了可用的销售工具。

![](https://assets.claude.com/79b63fbd0fc51883815a854c84146bcdffc2c2ab.png)

销售区域评分仪表盘，此处展示的是演示数据。

这些提示词都不涉及技术。模式是：告诉 Claude 要按哪些维度评分，先跑一个测试区域，检查输出，调整权重（“我觉得 D4 的权重可能有点重，稍微调低一点”），再跑下一个区域。

## **Claude Cowork 为什么适合我**

Claude Cowork 让我坚持用下来的，是它的界面。提示词读起来像英文句子，输出落在我本就在用的格式里（文档、网页和 Salesforce 更新），而且 human-in-the-loop（人在回路）模式是内置的，Claude 提出方案，我在任何内容交付前批准。

销售行业里有很多人入行就是为了和客户交流。Claude Cowork 可以把这些时间还给他们，让他们专注于这件事。

## **销售团队应该从哪里开始**

我自己一周工作中的两个模式，值得带回到销售团队。

第一是把准备工作交给定时任务。定时任务自行运行；我不必再记得去做那些零散的小日常任务，而它们加起来会占用相当多时间。把团队要求的格式固化到技能里也很重要：我的预测会以管理层阅读的精确版式呈现，所以周一的时间花在评论上，而不是排版上。如果你想为自己的配置找一个起点，Anthropic 的 [Sales 插件](https://claude.com/plugins/sales)自带基础技能，包括通话准备那一个。这些技能本来就是供你按团队实际工作方式定制的。

第二是把大型战略项目作为隔夜的 Claude Cowork 例行任务来运行。4,000 个账户的评分是展示性案例，但同样的形态也适用于 TAM 规模测算、账户研究、薪酬基准分析，以及任何过去因为没有团队有时间而长期搁置的事情。如有需要，你可以在第二天早上再完善提示词。

在使用 Claude Cowork 之前，数据汇总、报告排版，以及数字变化后的重新建立基线，会填满我的一周。现在，我拿回了这些时间，可以投入到推动业务进展的战略工作和客户关系工作上。

***[进一步了解销售团队如何使用 Claude Cowork](https://claude.com/resources/tutorials/using-claude-cowork-for-sales-account-research)，并[立即开始使用](https://claude.com/product/cowork)。***
