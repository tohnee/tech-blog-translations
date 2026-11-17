---
title: "在前沿工作：Hebbia 如何为不能错过任何细节的金融尽职调查构建 AI"
title_en: "Working at the frontier: How Hebbia builds AI for financial diligence that can't miss a detail"
date: 2026-07-13
source: https://claude.com/resources/articles/working-at-the-frontier-how-hebbia-builds-ai-for-financial-diligence-that-cant-miss-a-detail
crawled: 2026-11-17
translated: 2026-11-17
---

# 在前沿工作：Hebbia 如何为不能错过任何细节的金融尽职调查构建 AI

> 原文：[Working at the frontier: How Hebbia builds AI for financial diligence that can't miss a detail](https://claude.com/resources/articles/working-at-the-frontier-how-hebbia-builds-ai-for-financial-diligence-that-cant-miss-a-detail) · Claude 博客

Hebbia 为金融专业人士构建研究与尽调软件，并用与专家实际成果挂钩的金融评估来测试每一个新模型。在测试中，Claude Fable 5 取得了其研究团队有记录以来最大的准确率提升，并能跟住此前模型反复漏掉的复杂查询。

Hebbia 是一个为机构级金融的严谨性而打造的 AI 平台，服务对象包括排名前 50 的资产管理公司中超过三分之一，以及一级投资银行和律师事务所。公司创始产品经理 Divya Mehta 大约有一半时间花在最大的投资银行、私募股权和信贷客户身上。

这些客户的决策建立在横跨数千份密集文档的分析之上——一个错误的数字就可能改变整笔交易的结局。

## Hebbia 如何守住准确性底线

银行家或投资者在评估一个机会时，必须梳理所有可能影响决策的数据，包括公司的公开申报文件、信贷协议、内部文件，以及来自 CRM 之类的结构化数据。Hebbia 的 meta-prompting 把自然语言请求转换为提示，然后由 Claude 在数百份文档上执行分析的每一步。每个答案都落在 Hebbia Matrix 网格中各自的单元格里，从而实现完全的透明性、可追溯性和可操控性。

要让这些答案在大规模下保持准确，是 Adithya Ramanathan 领导的应用 AI 研究团队的本职工作。对 Ramanathan 来说，这项工作的意义在于找到信号：让模型在正确的上下文里调用正确的数据，并呈现出客户真正想知道的东西。

「当你把它连接到正确的数据、放进正确的生态系统中，」Ramanathan 说，「你才能得到金融专业人士真正追逐的那种 alpha。」

要做到这一点，每个新模型都必须通过 Hebbia 的金融专用基准测试，与它将要取代的模型正面比较；同时，基准测试的衡量范围随每次发布而扩展，以跟上模型进步的速度。这个基准是刻意设计得很难的。

「标准极高，而我们的客户也用这个极高的标准要求我们——这理所当然，」Mehta 说，「归根结底，他们是在基于 Hebbia 中构建的分析和最终交付成果，做出规模极大的投资决策。」

![](https://assets.claude.com/89ea204c3b0753eca5f0b4a8e3b694f87b6f0492.jpg)

Hebbia 团队让每个新的 Claude 模型都通过金融专用基准测试，与它将要取代的模型正面对比。

## 以迄今最大的幅度通过 Hebbia 的评估

应用 AI 团队的研究员 Joe Renner 会让每个新的 Claude 模型跑这套基准，其中包含一组复现金融知识工作者关键用例的测试。其中一项测试覆盖金融文档上的问答与引用查找。另一项测试则经由 Hebbia 的智能体系统、使用其聊天产品所用的工具，完成客户实际会做的那种开放式、多来源分析。

Claude Fable 5 以 Renner 测到过的最大幅度通过了这两项测试。在问答与引用测试中，它在金融文档上的准确率取得了约 20% 的相对提升，是他从任何新模型中见过的最好成绩。引用匹配率大致持平——Renner 认为，这一提升来自模型对所找到证据的更好理解。

「归根结底是两项看似基础的能力：从密集的数据集中找到正确信息，然后正确地综合它，」Divya 说，「这些看起来是基础能力，但放到金融与研究的工作流中，影响是巨大的。」在智能体测试中，它能同时把握一个多部分请求的每一个部分，逐一作答，并把每个答案都引用回其来源。

Claude Fable 5 还展现出更广的覆盖范围。在开放式分析中，它从更广泛的数据切面进行推理，得出的结论让团队认为值得进一步细看。Renner 将此归因于模型维持长任务的方式：它让请求的每一部分始终在视野之内，调用自己的子智能体和工具以取回正确的事实，并把每个论断都落在来源之上，而非凭空推断。

## 用 Claude Fable 5 为交易尽调树立新标准

能为客户带来优势的信息，通常藏在非结构化的专有文档里。

相比金融已经擅长建模的结构化定量数据，这类文档一直更难在大规模上分析。Hebbia 构建 Matrix 是为了让这种定性工作系统化，而每代模型都在拓宽它能承担的范围。

这可能是一个装着数千份文档的数据室，任务是找到相关信号、标注引用，并起草每一节[投资备忘录](https://claude.com/resources/guides/the-ai-investment-firm)。也可能是分析与一笔信贷交易相关的每一份文档（信贷协议、修订条款、附函，每份都有数百页密集的技术性内容），并从这团非结构化材料中提取出完整的契约条款包——既有财务条款，也有经营限制。

「实际上，这些正是 Anthropic 模型一直非常擅长的文档类型，」Mehta 说。

在此前的 Sonnet 和 Opus 模型上，Matrix 已经能够提取并综合信贷协议中的契约条款——即贷款方为自己写下的那些密集的保护性条款。而在 Claude Fable 5 的加持下，Hebbia 正把手伸向剩下的工作：在契约条款之上做多步骤分析，将它们与实时监控数据对比，标记风险，一路做到契约审查的初稿和内部备忘录。这类审查，信贷公司过去要花大价钱请外部团队手工完成。

![](https://assets.claude.com/675280af0230cbc453d91b56ebfd4040588920ec.jpg)

Claude Fable 5 让 Matrix——Hebbia 为金融专业人士打造的 AI 平台——能够承担运行时间更长、多步骤的任务，例如综合信贷协议中的契约条款。

## 下一步

既然 Claude Fable 5 这样的模型能把这项工作端到端地完成，衡量它的标尺就变成了它所替代的专家工时。

在 AI 出现之前，一位董事总经理需要一份向 CEO 推介的演示文稿时，初级银行家要花 2 到 3 天去了解公司、整理财务数据、制作幻灯片。在 Opus 之前的时代，产出初稿的时间已经压缩了 12 到 24 小时；而 Mehta 说，随着更早的 Opus 模型在 Hebbia 上投入使用，时间进一步缩短到约一天完成端到端流程。此后，Hebbia 把整个工作固化进一个 Matrix：以一组确定性的智能体步骤跨来源收集数据，完成分析，并在几分钟内生成最终演示文稿、财务模型和内部研究，让银行家可以把时间花在追逐哪些买家、如何定位这些买家上。她说，Claude Fable 5 又把这一时间进一步收紧。

把工作拆解成步骤仍然重要，「无论模型多么聪明」，因为公司希望控制哪些文档进入分析、每一步如何构建。因此，Hebbia 正在采用 Claude Agent SDK，把这些任务组合成更小、可重复、经过检查的步骤，而不是依赖单次模型运行。

「压缩交易生命周期，对一家机构争夺这些投资的能力有巨大影响，」Mehta 说。这一点她从客户对话中就能听出来。两三年前，问题还带有防守意味，围绕幻觉和计算是否正确。「如今，这些对话已经完全变了。他们问的是：我怎么把更多工作流自动化？我怎么把更多步骤串起来？我怎么一键生成十份、十五份、二十份高保真、高一致性的幻灯片？」

**从 [Claude Fable 5](https://www.anthropic.com/claude/fable) 开始使用。**

本系列更多内容：[Rakuten](/resources/articles/working-at-the-frontier-rakuten) 和 [Cognition](/resources/articles/working-at-the-frontier-how-cognition-trusts-claude-fable-5-to-work-through-the-night)
