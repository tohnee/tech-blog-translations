---
title: "英伟达的爬坡——出货量、ASP、云定价、利润率、EPS、现金流、中国与竞争"
title_en: "Nvidia's Ramp – Volume, ASP, Cloud Pricing, Margins, EPS, Cashflow, China, Competition"
subtitle: "从 AI 假动作中理清供应链的混乱信号"
date: 2023-08-20
source: https://newsletter.semianalysis.com/p/nvidias-ramp-volume-asp-cloud-pricing
crawled: 2026-09-15
authors: ["Dylan Patel", "Myron Xie", "Daniel Nishball"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 英伟达的爬坡——出货量、ASP、云定价、利润率、EPS、现金流、中国与竞争

> 原文：[Nvidia's Ramp – Volume, ASP, Cloud Pricing, Margins, EPS, Cashflow, China, Competition](https://newsletter.semianalysis.com/p/nvidias-ramp-volume-asp-cloud-pricing) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**从 AI 假动作中理清供应链的混乱信号**

建设 AI 算力的惊人需求，主要受限于英伟达提升产量的能力不足。我们已经[详细解析过原因（CoWoS 与 HBM）](https://www.semianalysis.com/p/ai-capacity-constraints-cowos-and)、[助力 GPU 增产的 28 家上游供应商](https://www.semianalysis.com/p/ai-expansion-supply-chain-analysis)，以及[英伟达正在爬坡到多高的 GPU 产量](https://www.semianalysis.com/p/ai-capacity-constraints-cowos-and)。今天我们想讨论的话题是 H100 GPU 未来的出货量与平均售价（ASP）。我们还会谈及 MI300、L40 以及英伟达的下一代 GPU。我们将走一遍我们的模型，及其对英伟达直到 FY2025 的出货量、营收、利润与现金流的意义。此外，我们还将讨论基础设施定价、明年的云定价与采购策略。最后，我们会谈需求侧、中国，以及当前这轮过度投资周期的持久性。

到目前为止，供应链中英伟达以外的公司交出的成绩单，是围绕 AI 与 GPU 需求的兴奋情绪与缺乏真实、可落地的营收指引的混合体。这在一定程度上被其他终端市场的疲软所拖累，尤其是 PC、智能手机，以及整体上的中国业务。有几家被当作 AI 赢家炒作起来的公司令人失望，因为它们表明其 AI 营收/动能不足以抵消业务其他部分的疲软。我们把这批公司称为 AI 假动作（AI head-fake）。

例如，Super Micro 在今年股价飙升超过 300% 之后令人失望：下季度营收指引仅为持平。他们以及其他许多 AI 假动作并未展示出 AI 营收的爬坡，这正在打破 AI 爬坡的叙事。到目前为止的结果，与人们所认为的英伟达正在做的事情相矛盾。这为怀疑整个 AI 故事的人提供了弹药。对其中一些 AI 假动作而言，问题仅仅在于它们[试图宣称自己是 AI 赢家](https://www.semianalysis.com/p/ai-server-cost-analysis-memory-is)，但[实际上并不是受益者](https://www.semianalysis.com/p/energizing-ai-power-delivery-competition)，或者[业务高度大宗商品化](https://www.semianalysis.com/p/thick-cables-thin-margins-microsoft)。对另一些而言，则纯粹是爬坡、出货与收入确认的时点问题。

让我们就后一种情况梳理一下供应链。如果英伟达在 3 月下单，即使台积电立即投产，把抛光晶圆加工成布满 4nm 芯片的晶圆也需要数月时间。接下来是 [CoWoS 封装供应链与多层测试环节，详见此文](https://www.semianalysis.com/p/ai-expansion-supply-chain-analysis)。随后英伟达从台积电取回这些成品 H100 芯片，发料给富士康（Foxconn）制造 H100 SXM 模块。这些模块再被运往纬创（Wistron）——由纬创对模块进行集成，将 8 个模块与 4 个 NVSwitch 及散热系统组装在一起，交付完成测试的 H100 基板（baseboard）。

![](https://substack-post-media.s3.amazonaws.com/public/images/24aa2b4e-62f9-4895-9b23-dcd7fe9350a6_2724x794.png)

最后，英伟达将这些 GPU 基板发往服务器制造商，并在 7 月确认营收——此时距投产已过去 4-5 个月。接下来服务器 OEM/ODM 需要组装服务器，很多情况下还要负责安装到另一个大陆的数据中心。在这个例子中，Super Micro 可能最晚到 10 月才能确认营收，而这要到明年 1 月发布其 FY Q2 2024 财报时才会显现。Coreweave 则只能从 2023 年 11 月开始出租这些服务器。这个例子是虚构的，用以放大收入确认节点以及各公司财年报期不同所带来的挑战。实际供应链在每个单独环节上通常都更快。

在深入本报告的主要内容之前，先从我们下文模型中一个令人瞠目的数据说起——一个你在转发时可以直接引用的数字。

**英伟达的利润率与现金流转化率高到这种程度：到明年年底，其资产负债表上的现金将庞大到相当于英特尔当前市值的一半。**

敬请期待我们认为他们将如何处置那座现金山。

*我们将于 9 月 3 日在台湾举办 [AI 与半导体研讨会](https://www.eventbrite.com/e/ai-and-semiconductor-symposium-tickets-692838296997)，众多代工厂、封装厂、ODM 供应商与买方将出席。议题涵盖 AI 基础设施的未来、谷歌 Gemini 与未来 OpenAI GPT 采用的下一代模型架构、中国模拟/功率半导体晶圆厂建设，以及英伟达当前的收购目标。演讲者包括 SemiAnalysis 的多位成员、[FabricatedKnowledge](https://www.fabricatedknowledge.com/)、[Asianometry](https://www.asianometry.com/)、[Alethia Capital](https://www.aletheia-capital.com/)，以及**一位特别的神秘嘉宾**。如果你能到场，[请在此注册](https://www.eventbrite.com/e/ai-and-semiconductor-symposium-tickets-692838296997)！*

## **英伟达测算——给炒作做嗅觉测试**

我们给出的预测来自多个向量。其一是 CoWoS 与 HBM 供应链；其二是各类超大规模云厂商、初创公司与企业的终端市场需求/资本开支计划；其三是实体数据中心建设的地产/电力数据；最后是 OEM/ODM 视角。

[获取 8 折团购订阅](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
