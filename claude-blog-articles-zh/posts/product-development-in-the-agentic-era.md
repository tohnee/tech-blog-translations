---
title: "智能体时代的产品开发"
title_en: "Product development in the agentic era"
date: 2026-04-29
source: https://claude.com/resources/articles/product-development-in-the-agentic-era
crawled: 2026-11-17
translated: 2026-11-17
---

# 智能体时代的产品开发

> 原文：[Product development in the agentic era](https://claude.com/resources/articles/product-development-in-the-agentic-era) · Claude 博客

Claude Managed Agents 产品经理 Jess Yan 分享她如何用这款产品为自己解除阻塞、腾出时间来打磨手艺。

在 AI 时代做产品经理，其中一个悖论是：我的工作感觉比以往任何时候都更像"人的工作"。

产品管理这份工作一直是手艺与协调的混合体。职业生涯的大部分时间里，我的一周都被后者占据：与跨职能相关方和队友开会、状态汇报，以及与工程团队一起梳理工单积压。我习惯了凭直觉快速做决定，然后陷入一场场艰难的攻坚战——游说、说服、争取资源；交付有影响力的产品往往更像一笔交易，而不是一次创造。

有了 Claude，我可以压力测试想法、自动化工作流、摆脱卡壳状态。我终于能把真正的时间花在用户和团队身上，投入到这份工作中始终最重要的部分：手艺。虽然这些新工作流改变了我的日常，但最有意义的转变发生在我们开始开发 [Claude Managed Agents](https://claude.com/resources/articles/claude-managed-agents)（目前处于测试阶段）的时候——这是一套可组合的 API，用于大规模构建和部署云端托管的智能体。

在本文中，我将分享 Managed Agents 如何改变了我作为产品经理的工作方式，以及一些你可以借用到自己工作流中的模式。

## **产品开发，过去与现在**

API 设计过去活在文档和评论串里；在 AI 的指数曲线上，我们以已经交付的东西来构建。一份在文档里读起来很优雅的规格，在你第一次真正基于它构建时可能就散架了。借助 Claude Code，我可以基于 API 规格的生产前版本勾勒一个智能体，一个下午之内就能端到端跑起一个真正的原型。

我们根据用自己原语构建时的所学，多次重塑了 API 抽象和 Claude Console 的用户体验——这些改动即便是为期数周的文档评审也绝不会暴露出来，否则只会在太晚的时候通过用户反馈浮现。我们仍然会为形态争论不休、跑原始 curl 请求，以确保对最底层的体验满意，但 Claude Code 能在同一次坐下来工作的过程中，把我从最基本的"hello world"测试带到可用的智能体。在构建这些智能体的过程中，我也能更具体地预判我们的运行框架（harness）和 API 可以如何随下一波模型与任务演进灵活调整。

起初，这些原型只用于塑造产品，但它们如今也在改变我的日常工作。我作为产品经理的工作流现在清晰地分布在我们的产品之间。我用 **Claude** 和 **Claude Cowork** 做开放式研究与探索——那种模糊的早期阶段探索，我需要一段持续的对话。一旦对待办工作的理解更清晰，我就用 **Claude Code** 来编写并交付一个为其定制的智能体，构建在 **Managed Agents** 之上。

这种双管齐下的回报是最大的解放。一方面，能够基于自己的产品进行构建，大幅提高了我对下一步能交付什么的上限。另一方面，一旦产品上线，同样的开发肌肉让我能够自动化那长长一尾、过去总是堵在我待办清单里的运营工作。

## **面向产品经理的 Managed Agents 用例**

现在，我会为任何"待办工作"现做专属智能体。构建一个很简单：我在 Claude Code 中加载 Managed Agents 技能，快速勾勒出我想要的东西。开发者也可以使用最新版本的 Claude Code 和内置的 `claude-api skill` 来基于 Managed Agents 构建——只需向 Claude 输入"*start onboarding for managed agents in Claude API*"即可开始。调用该技能后，Claude 会构建这个智能体，并在过程中解释其集成步骤，因此我能根据需要轻松调整方向。

这些智能体的例子包括：

* **采用情况分析。** 一个持续访问我们内部数据库、并具备理解数据模式技能的智能体，会运行查询以找出有趣的异常值和模式。凭借对以往运行的[记忆](https://claude.com/resources/articles/claude-managed-agents-memory)，它可以基于此前的发现继续累积，并持续深化自己的视角。
* **开发者情绪监测。** 一个配备预置[网络搜索工具](https://platform.claude.com/docs/en/managed-agents/tools#available-tools)并了解关注重点的智能体，会扫描一份特定域名清单以获取最新的开发者反馈，并就常见主题进行汇报。由于需要分析的内容太多，它会把研究分发到[多个智能体](https://platform.claude.com/docs/en/managed-agents/multi-agent)并行处理，等待结果并综合各项发现。
* **演示构建。** 一个可以访问演示用 GitHub 仓库、品牌素材和活动演示文稿的智能体，会把预置模板转化为面向相关受众（例如某场会议或某次客户会议）的精致演示。

Managed Agents 的会话在云端运行，所以我可以走开，回来时发现工作已经完成。那些因为每次发布都有各自古怪之处而永远无法规模化的流程，现在用 Managed Agents 很容易自动化，每次智能体运行都让人感到振奋，而不是枯燥。

## **腾出空间来打磨我的手艺**

一年前，这类工作全都只能缓慢地爬行于跨职能的人力申请、混乱的电子表格，或是我一直没机会尝试的半成品构想之中。现在，有了 Claude 和 Managed Agents，我可以扩展自己，把时间用来与团队合作开发最有影响力的产品。我的一天如今涵盖了与客户一起生成创新想法、与工程同事一起钻研模糊不清的问题，以及在前沿产品工作上投入真正的创造力。

如果你是产品经理，而且还没有构建过智能体，这就是我建议你这周开始的地方。你一直希望存在的实验和工具，离你只有一个提示词和几次 API 调用之遥。

*在我们的[文档](https://platform.claude.com/docs/en/managed-agents/overview)中了解更多。*
