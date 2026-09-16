---
title: "Amazon 与 Anthropic：毒丸，还是帝国的反击"
title_en: "Amazon Anthropic: Poison Pill or Empire Strikes Back"
subtitle: "Claude 3、Claude 4、Trainium2、Marvell、Alchip、Bedrock、Google 基础设施"
date: 2023-10-02
source: https://newsletter.semianalysis.com/p/amazon-anthropic-poison-pill-or-empire
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# Amazon 与 Anthropic：毒丸，还是帝国的反击

> 原文：[Amazon Anthropic: Poison Pill or Empire Strikes Back](https://newsletter.semianalysis.com/p/amazon-anthropic-poison-pill-or-empire) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**Claude 3、Claude 4、Trainium2、Marvell、Alchip、Bedrock、Google 基础设施**

Amazon 与 Anthropic 上周签署了一项重大协议，让我们拆解一下传闻中的交易条款，看看它对 Amazon 未来 AI 基础设施与服务，以及 Anthropic 的 Claude-3 和 Claude-4 模型意味着什么。

Amazon 正以可转债形式投资 12.5 亿美元，待 Anthropic 后续融资时将转为股权。Amazon 还拥有未来追加至多 40 亿美元的选择权。这些金额直接拿来讨论其实没有意义，因为它们很可能是云抵扣额度（cloud credits），Amazon 内含的利润率可能区间极大。若以抵扣额度形式提供，Amazon 实际掏出的真金白银会低得多。有人说 Amazon 给的是现金，但在我们看来这说不通。Anthropic 目前正在从其他渠道筹集更多资金。尽管投资规模可观，[Amazon 并不会获得对 Anthropic 的直接控制权](https://www.anthropic.com/index/anthropic-amazon)，甚至连其 [5 人长期利益信托（LTBT）的席位](https://www.anthropic.com/index/the-long-term-benefit-trust)都不会有。

业界对 Amazon x Anthropic 合作的看法与情绪五花八门，而我们的态度最好用我们最喜爱的诗人之一的一句歌词来概括。

> 如果你只有一次机会、一个瞬间，去抓住你梦寐以求的一切，你是会紧紧把握，还是任其溜走。

引用 Eminem 或许显得非常突兀，但请给我们一点时间，一切都会说得通。

![](https://substack-post-media.s3.amazonaws.com/public/images/2d1cfc38-96ff-41a3-9b6e-cb8e18918ce4_1024x1024.jpeg)
*由 DALL-E 3 生成，是不是很可爱！*

出于多重原因，Amazon 的业务并未搭上今年生成式 AI 的热潮。Amazon 缺乏对企业/消费者数据和使用行为的直接触达，难以自行推出 AI 服务。尽管在全公司范围内重组了 Alexa 团队和其他 AI 团队，内部 Titan 模型的开发一直进展不顺。其 CodeWhisperer 模型甚至被成立不到一年的新创公司碾压，更遑论与主要竞争对手的模型抗衡。

缺乏直接触达/销售并不是大问题，因为 Amazon 的整个商业模式本来就是扮演某种「瑞士」（中立国）。更令人担忧的是其基础设施。Nitro、Elastic Fabric Adapter、Trainium 和 Inferentia2 **目前**都不太适配 LLM。其数据库护城河对 AI 也没有那么重要，因为与 AI 的计算成本相比，存储成本和数据出口成本无足轻重，这意味着多云战略毫无劣势，锁定效应很低。最后，Amazon 从 Nvidia 拿到的配额非常少，远低于其当前的云市场份额。所有这些，我们在 6 个多月前就[详细分析过](https://www.semianalysis.com/p/amazons-cloud-crisis-how-aws-will)。

所有这些因素都直接导致 Amazon 在云计算乃至整个计算领域失去市场份额。这令人担忧，因为 Amazon 是全球最大的数据中心部署者和运营者，拥有的存储与计算资源超过任何其他公司。

我们的数据显示，Microsoft 和 Google 的 2024 年 AI 基础设施支出计划都将部署远超 Amazon 的算力。这合乎逻辑，因为两家公司都雄心勃勃地要把 LLM 部署到产品的方方面面。而 Amazon 的节奏取决于客户的意愿，相对这些科技巨头的采纳计划普遍更慢。此外，由于配额/成本问题，许多客户已转向其他服务或云，以获取更易得、更便宜的 AI 算力。如果 Microsoft/Google 与 Amazon 在支出和部署上的差距持续下去，短短几年内 Amazon 的数据中心规模就会落后。

Anthropic 与 Amazon 的联姻表面上看相当完美。Amazon 需要前沿模型能力，而这正是帝国反击的方式。Anthropic 的 Claude 2 是仅次于 OpenAI GPT-4 的最佳公开可用模型。Amazon 获得了 Claude 2 的直接使用权，可用于服务客户，还可以提供微调服务。未来的模型同样会向 Amazon 开放。Amazon 还表示将把这些模型用于药物发现和医疗健康的诸多其他方面，[进一步强化其 Amazon HealthOmics 平台](https://www.semianalysis.com/i/137441303/aws-health-omics-as-a-template-for-nvidia)。

而从 Anthropic 这边看，表面上他们既坚守了 AI 安全的核心信念，又没有把控制权签字让渡给 Amazon；但实际上，这笔交易意味着 Anthropic 实质上押上了全部身家。我们听说其中涉及相当有分量的 IP 转移——将某些现有和即将推出的模型交给 Amazon。据称，Amazon 几乎可以基于 Anthropic 的技术构建任何他们想构建的东西。

此外，我们听说交易带有某些回补（clawback）条款，即 Anthropic 必须在几年内让 Amazon 收回投资。这些只是传闻，但 Amazon 利用 Anthropic IP 打造的产品会有一部分分成，帮助满足这一条款。我们完全不知道分成比例可能是多少，但可以假设性地想象：Amazon 在 AWS 上向客户交付基于 Anthropic 模型的服务每产生 10 亿美元收入，可能只有 1 亿美元被记回 Anthropic 用于偿还 Amazon。

表面上看，这与 Microsoft-OpenAI 的交易结构类似，但存在一些重大差异。其一，OpenAI 与 Microsoft 的条款没那么不透明：[Microsoft 将获得 OpenAI 利润的 75%，直至收回投资，随后持有该公司 49% 的股权并附利润上限](https://www.cnbc.com/2023/01/10/microsoft-to-invest-10-billion-in-chatgpt-creator-openai-report-says.html)。其二，OpenAI 似乎更有能力掌控自己的命运，因为它通过应用、网站和极为成功的 API 直接触达企业和消费者。

就 Anthropic 而言，我们很难看出它如何能像 OpenAI 那样、建立对 Claude 模型部署方式的同等掌控。即便 Anthropic 提供了直营网站和 API，Amazon 大概也能与 Anthropic 同步部署这些模型。即便是 OpenAI 的情况，DALL-E 3 和 GPT-4 视觉能力在向大多数 ChatGPT 付费订阅者开放之前，就已经可以通过 Microsoft 的 Bing 使用了。

尽管存在这种「抢跑」，由于 OpenAI 已经建立起直接的客户触达，其直营使用的客户留存率非常高且仍在增长。同样，Amazon 也会像 Microsoft 那样直接部署基础模型和微调 API，但 Anthropic 未必能获得同等的客户留存/份额。这意味着 Anthropic 让渡的经济利益可能远比表面看起来要多。

虽然表面上这听起来像一颗毒丸，但归根结底，这笔交易极大加速了 Anthropic 构建基础模型的能力，使其有潜力在通往「AGI」的竞赛中跟上 Google 和 OpenAI。Anthropic 未来最大的难题是获取足够的算力资源，以免落后于 OpenAI 和 Google Deepmind。Anthropic 显然愿意不惜一切，绝不让成就伟大的机会溜走。

> 如果你只有一次机会、一个瞬间，去抓住你梦寐以求的一切，你是会紧紧把握，还是任其溜走。

Google 的明显优势在于，它是唯一一家完全拥有并掌控自家 AI 研究机构的公司。此外，它也是[唯一一家拥有出色自研芯片的公司](https://www.semianalysis.com/p/google-ai-infrastructure-supremacy)。Microsoft 和 Amazon 与 OpenAI/Anthropic 都只是保持距离的合作关系。而且，它们即将推出的自研芯片 Athena 和 Tranium2 仍然显著落后。

Google 将在其基础设施中部署多个超大规模集群用于训练，并拥有迄今最低的单次推理成本，但这并不会自动把王国的钥匙交到它手上。[如果较量的只是算力资源的获取，Google 会把 OpenAI 和 Anthropic 都碾碎](https://www.semianalysis.com/p/google-gemini-eats-the-world-gemini)。

仅凭「GPU 富足」并不意味着战争结束。[Google 将拥有多个比竞争对手更大的集群](https://www.semianalysis.com/p/broadcoms-google-tpu-revenue-explosion)，因此它有余地在预训练中试错、尝试更多不同架构。OpenAI 和 Anthropic 在算力上的欠缺，必须靠研究效率、专注度和执行力来弥补。

这种必要性加上更精简的团队，将不得不驱动创新。即使与 OpenAI 相比，Anthropic 在总算力资源上也明显落后，但两者的野心不相上下。我们期待看到 Anthropic 能否跟上。目前 Claude-2 在模型质量与成本的平衡上处于甜点位，比 GPT-4 便宜得多，但随着 4-turbo 短期内发布，Anthropic 必须再拿出别的杀手锏。

下文我们将简要讨论以下话题：Google 对 Anthropic 的投资；对 Anthropic Claude-3 与 Claude-4 基础设施的一些推测，包括这些模型潜在规模的大致区间（bounding box）；以及 Amazon Trainium1/Inferentia2 + Tranium2/Inferentia3 部署规模的测算。

[团体订阅立减 20%](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
