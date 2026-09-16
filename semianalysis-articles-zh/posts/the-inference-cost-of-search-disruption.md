---
title: "搜索颠覆的推理成本——大语言模型成本分析"
title_en: "The Inference Cost Of Search Disruption – Large Language Model Cost Analysis"
subtitle: "$30B 谷歌利润一夜蒸发，H100、TPUv4、TPUv5 带来的性能提升"
date: 2023-02-09
source: https://newsletter.semianalysis.com/p/the-inference-cost-of-search-disruption
crawled: 2026-09-15
authors: ["Dylan Patel", "Afzal Ahmad"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 搜索颠覆的推理成本——大语言模型成本分析

> 原文：[The Inference Cost Of Search Disruption – Large Language Model Cost Analysis](https://newsletter.semianalysis.com/p/the-inference-cost-of-search-disruption) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**$30B 谷歌利润一夜蒸发，H100、TPUv4、TPUv5 带来的性能提升**

OpenAI 的 ChatGPT 席卷全球，仅 1 月份就迅速积累起[超过 1 亿活跃用户](https://www.reuters.com/technology/chatgpt-sets-record-fastest-growing-user-base-analyst-note-2023-02-01/)。这是有史以来任何应用增长到这一规模的最快速度，此前两项纪录保持者分别是 TikTok 的 9 个月和 Instagram 的 2.5 年。所有人脑海中的头号问题是：大语言模型（LLM）对搜索的颠覆性到底有多大。微软本周的 Bing 发布震惊了世界——将 OpenAI 的技术融入搜索。

> 这个新 Bing 会让谷歌出来跳舞，我想让人们知道，是我们让他们跳起舞来的。
>
> [微软 CEO Satya Nadella](https://www.theverge.com/23589994/microsoft-ceo-satya-nadella-bing-chatgpt-google-search-ai)

谷歌近期的举动看起来确实像是在跳舞。虽然[我们认为谷歌拥有比世界上任何其他公司都更好的模型与 AI 专业能力](https://www.semianalysis.com/i/97006309/tensorflow-vs-pytorch)，但他们缺乏一种有利于落地并商业化其大量领先技术的文化。来自微软和 OpenAI 的竞争压力正在迅速改变这一点。

搜索领域的颠覆与创新并非没有代价。[正如我们在此详述的](https://www.semianalysis.com/p/the-ai-brick-wall-a-practical-limit)，训练一个 LLM 的成本高昂。更重要的是，以任何合理规模部署模型时，推理成本远超训练成本。事实上，ChatGPT 的推理成本每周都超过其训练成本。如果把类 ChatGPT 的 LLM 部署到搜索中，就意味着谷歌 $30 billion 的利润直接转移到计算行业「卖铲人」的手中。

今天我们将深入探讨 LLM 在搜索中的不同用途、ChatGPT 的每日成本、LLM 的推理成本、以数字说明谷歌搜索被颠覆的影响、LLM 推理负载的硬件需求（包括 NVIDIA H100 的性能提升数据与 TPU 成本对比）、序列长度、延迟标准、各种可调节的杠杆、微软、谷歌和 Neeva 对这一问题的不同处理方式，以及 [OpenAI 下一代模型架构（我们在此详述）](https://www.semianalysis.com/p/the-ai-brick-wall-a-practical-limit)如何在多个方面大幅降低成本。

## **搜索业务**

首先，让我们界定搜索市场的参数。我们的信源显示，谷歌每秒处理 ~320,000 次搜索查询。对照谷歌搜索业务分部 2022 年 $162.45 billion 的营收，可以算出每次查询的平均营收为 1.61 美分。在此基础上，谷歌还要为搜索、广告、网页爬取、模型开发、员工等支付巨额开销。谷歌成本结构中一个值得注意的科目是：他们向苹果支付了 ~$20B 上下的费用，以成为苹果产品上的默认搜索引擎。

谷歌服务业务部门的营业利润率为 34.15%。如果把 CoGS/运营费用分摊到每次查询，可得每次搜索查询的成本为 1.06 美分，对应 1.61 美分的营收。这意味着，带 LLM 的搜索查询成本必须显著低于每次 <0.5 美分，否则搜索业务对谷歌而言将变得极不盈利。

> 我们很高兴地宣布，新 Bing 正运行在一个全新的下一代 OpenAI 大语言模型上，它比 ChatGPT 更强大，并专门针对搜索做了定制。它汲取了 ChatGPT 与 GPT-3.5 的关键经验与技术进步——而且更快、更准确、更强大。
>
> [Microsoft](https://blogs.microsoft.com/blog/2023/02/07/reinventing-search-with-a-new-ai-powered-microsoft-bing-and-edge-your-copilot-for-the-web/)

## **ChatGPT 成本**

估算 ChatGPT 的成本是个棘手的命题，因为存在多个未知变量。我们建立的成本模型显示，ChatGPT 的计算硬件运行成本为每天 $694,444。OpenAI 需要 ~3,617 台 HGX A100 服务器（28,936 块 GPU）来支撑 ChatGPT。我们估计每次查询的成本为 0.36 美分。

###### 我们的模型是基于每次推理从零构建的，但它与 Sam Altman 的一条推文以及他最近接受的一次访谈相吻合。我们假设 OpenAI 使用 GPT-3 稠密模型架构，规模为 1,750 亿参数，隐藏维度 16k，序列长度 4k，平均每次回复 2k token，每用户 15 次回复，1,300 万日活用户，FLOPS 利用率在 <2000ms 延迟下比 FasterTransformer 高 2 倍，int8 量化，因纯空闲时间导致 50% 的硬件利用率，以及每 GPU 小时 $1 的成本。

请挑战我们的假设；我们很乐意让模型更精确，尽管我们相信自己已在正确的数量级范围内。

## **用上 ChatGPT 的搜索成本**

如果把 ChatGPT 模型生硬地塞进谷歌现有的搜索业务，影响将是毁灭性的：营业收入将减少 $36 Billion。这 $36 Billion 就是 LLM 推理成本。注意这并不是 LLM 时代搜索的真正样子，[那份分析在这里](https://www.semianalysis.com/p/peeling-the-onions-layers-large-language)。

![](https://substack-post-media.s3.amazonaws.com/public/images/41a1d485-53c4-4291-8a7b-e04583bf428e_2101x692.png)

要把当前版 ChatGPT 部署到谷歌的每一次搜索中，需要 512,820.51 台 A100 HGX 服务器，总计 4,102,568 块 A100 GPU。**这些服务器与网络设备的总成本仅 Capex 一项就超过 $100 billion**，其中英伟达（NVIDIA）将获得很大一部分。当然，这永远不会发生，但如果我们假设软件与硬件都不做任何改进，这将是一个有趣的思想实验。我们还在订阅区给出了用谷歌 TPUv4 和 v5 建模的推理成本，结果差异相当大。我们还有一些 H100 的 LLM 推理性能提升数据。

精彩之处在于，微软明知把 LLM 插入搜索会碾碎搜索的盈利能力、并需要巨额 Capex，却依然为之。我们估算的是营业利润率的变化，再看看 Satya Nadella 怎么说毛利率。

> 从今往后，搜索的[毛利率]将永远下降。
>
> [微软 CEO Satya Nadella](https://www.ft.com/content/2d48d982-80b2-49f3-8a83-f5afef98e8eb)

这甚至还没有考虑：随着搜索质量提升，搜索量可能有所下降；在 LLM 的回复中植入广告的困难；以及我们将在本报告后文讨论的无数其他技术问题。

微软正兴高采烈地炸毁搜索市场的盈利能力。

> 在搜索广告市场每夺取一个百分点的份额，对我们的广告业务来说就是 $2 billion 的营收机会。
>
> [Microsoft](https://view.officeapps.live.com/op/view.aspx?src=https://c.s-microsoft.com/en-us/CMSFiles/Transcript223.docx?version=e69dc7f8-a0b8-7d09-ff82-f821891ad767)

Bing 的市场份额微不足道。微软抢下的任何份额增长，都将给他们带来惊人的营收与利润。

> 我认为我们双方在这里都有巨大的上行空间。我们将一起发现这些新模型能做什么，但如果我坐在一个暮气沉沉的搜索垄断者的位置上，不得不设想这样一个世界——这套变现机制真的受到挑战、出现新的广告单元、甚至可能有暂时的下行压力——我的感觉不会好。
>
> 这里有这么多价值，我们居然想不出怎么敲响它的收银机，这对我来说难以想象。
>
> [OpenAI CEO Sam Altman 接受 Stratechery 采访](https://stratechery.com/2023/new-bing-and-an-interview-with-kevin-scott-and-sam-altman-about-the-microsoft-openai-partnership/)

与此同时，谷歌处于守势。如果他们的搜索摇钱树动摇，他们的利润表将面临巨大问题。份额损失的实际后果会比上述分析更难看，因为谷歌的运营成本相当臃肿。

## **谷歌的回应**

谷歌并未坐以待毙。在 ChatGPT 发布后仅仅几个月内，谷歌就已把自己带 LLM 的搜索版本推向公众。从我们目前所见的新 Bing 与新谷歌的对比来看，各有优劣。

在 LLM 能力上，Bing GPT 似乎强大得多。[谷歌甚至在其新技术的现场演示中就已经出现了准确性问题](https://www.reuters.com/technology/google-ai-chatbot-bard-offers-inaccurate-information-company-ad-2023-02-08/)。但如果你同时测量 Bing GPT 和谷歌 Bard 的响应时间，Bard 在响应时间上碾压 Bing。这些模型响应时间与质量的差异与模型大小直接相关。

> Bard 集世界知识之广博与大语言模型的力量、智能和创造力于一身。它利用网络信息提供新鲜、高质量的回答。我们最初发布的是**LaMDA 的轻量级模型版本。这个小得多的模型需要的算力显著更少**，使我们得以扩展到更多用户、获得更多反馈。
>
> [Google](https://www.youtube.com/watch?v=yLWXJ22LUEc)

谷歌正用这个更小的模型在利润率上打防守。他们本可以部署完整尺寸的 LaMDA 模型，或能力强得多、规模也大得多的 PaLM 模型，但他们选择了一个瘦得多的小模型。

这是出于必要。

谷歌无法把这些大模型部署进搜索，那会过度侵蚀其毛利率。我们将在本报告后文进一步讨论这个轻量版 LaMDA，但必须认识到，Bard 的延迟优势是其竞争力的一个因素。

如果你喜欢这篇文章，请分享！这对我们帮助很大！

[分享](https://newsletter.semianalysis.com/p/the-inference-cost-of-search-disruption?utm_source=substack&utm_medium=email&utm_content=share&action=share)

由于谷歌的搜索营收来自广告，不同用户每次搜索产生的营收水平并不相同。美国郊区的普通女性用户，每个定向广告带来的营收要远高于印度的男性农民。这也意味着他们产生的营业利润率也天差地别。

## **大语言模型在搜索中的未来**

把 LLM 直接硬塞进搜索并不是改进搜索的唯一方式。谷歌多年来一直在搜索中使用语言模型生成嵌入（embedding）。这应当能在不炸掉推理成本预算的前提下，改善最常见搜索的结果，因为这些嵌入可以生成一次、服务多人。[我们在这里剥开那颗洋葱，并介绍众多可以实现的成本优化](https://www.semianalysis.com/p/peeling-the-onions-layers-large-language)。

把 LLM 插入搜索的最大挑战之一，是序列长度增长与低延迟要求。我们将在下文讨论这些问题，以及它们将如何塑造搜索的未来。

我们还将围绕 LLM 推理与每次查询成本，讨论 NVIDIA A100、H100 和谷歌 TPU。我们还将分享 H100 的推理性能提升及其对硬件市场的影响。GPU 与 TPU 的竞争在这场战役中无处不在。

此外，无需新硬件也可以显著降低每次推理的成本。我们[在此讨论过 OpenAI 下一代 LLM 架构在训练侧的改进](https://www.semianalysis.com/p/the-ai-brick-wall-a-practical-limit)，但推理成本方面同样有改进。此外，谷歌也在使用一些独特而令人兴奋的技术，我们也将在下文讨论。

[团体订阅立减 20%](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
