---
title: "OpenAI 要完蛋了？——微软，还有你？"
title_en: "OpenAI Is Doomed? - Et tu, Microsoft?"
subtitle: "Meta、Google、Anthropic、DeepSeek、Inflection Phi 奇才，分发/整合 vs 资本/算力？"
date: 2024-05-07
source: https://newsletter.semianalysis.com/p/openai-is-doomed-et-tu-microsoft
crawled: 2026-09-15
authors: ["Dylan Patel", "Daniel Nishball"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# OpenAI 要完蛋了？——微软，还有你？

> 原文：[OpenAI Is Doomed? - Et tu, Microsoft?](https://newsletter.semianalysis.com/p/openai-is-doomed-et-tu-microsoft) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**Meta、Google、Anthropic、DeepSeek、Inflection Phi 奇才，分发/整合 vs 资本/算力？**

所有人的目光都聚焦在这场不盈利的 AI 支出还能持续多久。[H100 租赁价格逐月下跌](https://www.semianalysis.com/p/ai-cloud-tco-model)，而[定价公道的中小型集群](https://www.semianalysis.com/p/ai-cloud-tco-model)供给也在快速增长。尽管如此，需求侧的动能显然依然强劲。虽然大型科技公司仍是最大的买家，但[全球买家名单正愈发多元，且仍在环比增加 GPU 采购](https://www.semianalysis.com/p/accelerator-model)。

这股狂热大多并非源于任何实际的收入增长，而是源于基于未来业务梦想、竞相打造更大模型的抢跑。大多数人心目中明确的目标就是追平 OpenAI、甚至取而代之。如今，许多公司在 Chatbot ELO 榜单上与 OpenAI 最新的 GPT-4 只有毫厘之差，而且在上下文长度和[视频](https://www.youtube.com/watch?v=wa0MT8OwHuk)模态等某些方面，一些公司已经领先。

![](https://substack-post-media.s3.amazonaws.com/public/images/4bf91480-95ad-409e-9cfb-9ccdcb7c5241_1579x954.png)
*来源：SemiAnalysis，ArtificalAnalysis.ai*

显然，只要算力给够，最大的几家科技公司就能追平 OpenAI 的 GPT-4。传闻 Gemini 2 Ultra 将在各方面超越 GPT-4 Turbo。此外，Meta 的 Llama 3 405B 也将追平 GPT-4，而且是开源的——这意味着任何租得起 H100 服务器的人都能用上 GPT-4 级别的智能。

## **东方凤凰**

迅速追上来的不只是大型科技公司。昨天，中国的 [DeepSeek](https://www.deepseek.com/) 开源了一个新模型，它比 Meta 的 Llama 3 70B 运行成本更低、效果更好。虽然该模型更针对中文查询（分词器/训练数据集）和政府对特定议题的审查做了调优，但它恰好在[代码（HumanEval）和数学（GSM 8k）这些通用语言](https://github.com/deepseek-ai/DeepSeek-V2/blob/main/deepseek-v2-tech-report.pdf)上也都胜出。

而且，其定价便宜得惊人。DeepSeek 的模型显著便宜于任何其他有竞争力的模型。他们的定价甚至一举跳过了[风投砸钱给推理 API 服务商、亏本承运 Meta 和 Mistral 模型的这场逐底竞赛](https://www.semianalysis.com/p/inference-race-to-the-bottom-make)。

![](https://substack-post-media.s3.amazonaws.com/public/images/2a58c633-f733-4bdf-91a7-f56f7fea79c0_1552x1030.png)
*来源：SemiAnalysis，ArtificalAnalysis.ai，各模型基准测试*

DeepSeek 声称，单节点 8x[H800](https://www.semianalysis.com/p/nvidias-new-china-ai-chips-circumvent) GPU 可以实现每秒超过 50,000 个 decode token 的峰值吞吐（或在配 disaggregate prefill 的节点上实现 100k prefill）。按仅计输出 token 的报价 API 价格计算，这相当于每节点每小时 50.4 美元的收入。中国一台 8xH800 节点的成本约为每小时 15 美元，因此假设利用率完美，DeepSeek 每台服务器每小时最多可赚 35.4 美元，毛利率最高可达 70%+。

即使假设服务器永远达不到完美利用率、batch size 低于峰值能力，DeepSeek 在碾压所有人推理经济学的同时仍有充足的盈利空间。Mixtral、Claude 3 Sonnet、Llama 3 和 DBRX 本已在痛击 OpenAI 的 GPT-3.5 Turbo，而这是给棺材钉上的又一颗钉子。

更有意思的是 DeepSeek 带到市场的新颖架构。他们没有照抄西方公司的做法，而是在 MoE、RoPE 和 Attention 上做出了全新创新。他们的模型拥有超过 160 个专家，每次前向传播路由 6 个；总参数 2,360 亿，每次前向传播激活 210 亿。此外，DeepSeek 实现了一种新颖的多头潜在注意力（Multi-Head Latent Attention）机制，他们声称它比其他注意力形式具有更好的扩展性，同时精度也更高。

![](https://substack-post-media.s3.amazonaws.com/public/images/8aac5f93-78c8-4b1a-8cef-98fd92e3e05b_1526x619.png)
*来源：DeepSeek*
![](https://substack-post-media.s3.amazonaws.com/public/images/d02cf5c0-065d-4f7a-86c1-c383fc212ce2_1323x285.png)
*来源：DeepSeek*

他们用 8.1 万亿 token 训练了该模型。DeepSeek V2 以 Meta Llama 3 70B 五分之一的算力，实现了惊人的训练效率，模型性能还优于其他开放模型。给一直在做记录的人：DeepSeek V2 的训练所需 FLOPS 仅为 [GPT-4 的 1/20](https://www.semianalysis.com/p/gpt-4-architecture-infrastructure)，性能却相差不远。

![](https://substack-post-media.s3.amazonaws.com/public/images/9b80a125-64d6-4a7b-9a40-02cf09a01943_1564x1049.png)
*来源：SemiAnalysis，ArtificalAnalysis.ai，各模型发布公告*

这些结果表明中国公司如今也具备了竞争力。[而且这篇论文很可能是今年在信息量和细节分享方面最出色的一篇。](https://github.com/deepseek-ai/DeepSeek-V2/blob/main/deepseek-v2-tech-report.pdf)

外国竞争对手对 OpenAI 固然是一大挑战，但他们最大的合作伙伴才是最需要提防的对象。

## **微软到底有没有下定决心？**

微软直接为 OpenAI 花掉了超过 100 亿美元的资本开支，但他们并没有把大部分 GPU 产能划给 OpenAI。微软[每年超过 500 亿美元的 AI 数据中心开支](https://www.semianalysis.com/p/google-ai-infrastructure-supremacy)中的大部分都投给了内部工作负载。其中很多一直是为了在其自有产品和服务中部署 OpenAI 模型做推理，但这种情况正在改变。

微软被迫寻找备用方案，原因在于 OpenAI 独特怪异的结构。OpenAI 是一家非营利组织，其首要目标是创造安全、造福全人类的人工通用智能（AGI）。[OpenAI 可以、而且将会撕毁让 Microsoft 得以使用 OpenAI 模型的协议，而 Microsoft 没有任何追索权。](https://openai.com/our-structure)

> 虽然我们与 Microsoft 的合作伙伴关系包括数十亿美元的投资，但 OpenAI 仍是一家完全独立的公司，由 OpenAI 非营利组织治理。Microsoft 是无投票权的董事会观察员，没有控制权。
>
> AGI 被明确排除在所有商业和 IP 许可协议之外。
>
> 董事会决定我们何时达成 AGI。再次说明，我们所说的 AGI 指的是一个高度自主、在大多数具有经济价值的工作上超越人类的系统。该系统被排除在与 Microsoft 的 IP 许可及其他商业条款之外，后者仅适用于前 AGI（pre-AGI）技术。

对 Microsoft 而言，最令人担忧的是：OpenAI 的董事会可以在任何时刻——无需 Microsoft 任何投票参与——宣布他们已实现 AGI，而 Microsoft 将无权获得用它的投资换来的 IP。

再把这一点叠加到 OpenAI 非营利与营利两条线本就存在的[重大治理问题](https://www.nongaap.com/p/p-oppenhaimer-part-1)之上，Microsoft 就必须制定备用方案。

## **微软计划如何降低对 OpenAI 的依赖**

微软正试图把其大部分推理流量从 OpenAI 的模型迁移到自己直接拥有 IP 的模型上。这包括驱动微软 AI 叙事主线的 Copilot 和 Bing。当只有 OpenAI 的模型能力达标时，Microsoft 当然会在产品中使用它；但除此之外，大多数查询他们会优先用自家模型。

问题是：怎么做？

虽然 Microsoft 在 AI 人才上还竞争不过 OpenAI、甚至连 Meta 都比不过，但他们正以最快速度急起直追。对 Inflection 的「准收购」让他们快速获得了一个尚可的模型以及一支扎实的预训练与基础设施团队，但要追上 OpenAI 这个不断移动的靶心，还需要更多。

![](https://substack-post-media.s3.amazonaws.com/public/images/5f88abbc-c2be-4c3d-8219-b1e46f88770b_1499x931.png)
*来源：SemiAnalysis，OpenAI，Inflection AI*

Microsoft 已经拥有一些实力强劲的团队在研究合成数据，这可以说是下一代模型最重要的战场之一。Microsoft 的 Phi 模型团队以用大量来自更大模型的合成数据训练小模型而闻名。[最新的 Phi-3 模型发布相当惊艳。](https://arxiv.org/abs/2404.14219)如果目标只是保持在 OpenAI 身后一点点，这个策略是行得通的。

Microsoft 的另一个团队 WizardLM 创造了更了不起的东西，叫「Evol-Instruct」。这是一种用 AI 为 LLM 生成大规模、多样化指令集的方法。目标是提升 LLM 遵循复杂指令的能力，而不依赖人工创建的数据——人工数据昂贵、耗时，而且量与多样性都不足。

取而代之的是由 AI 来创建和筛选数据，通过与自身的模拟对话递归地自我改进。AI 会判断质量并迭代生成更好的数据。它还利用渐进式学习（progressive learning）来改变数据配比：从简单开始，逐步提升训练数据的难度和复杂度，让模型学得更高效。

Microsoft 冲击 GPT-4 级别的第一次大动作，是目前正在进行的 MAI-1 约 500B 参数 MOE 模型。它利用了 Inflection 的预训练团队及其数据集，再结合 Microsoft 自有的一部分合成数据。目标是到本月月底拿出自研的、从零训练的 GPT-4 级模型。

我们不确定它能否一步到位，但 MAI-1 计划只是激进的自研模型长征的起点。Microsoft 已为其内部团队规划了一个 100k GPU 集群，是 GPT-4 训练集群规模的 5 倍。

许多公司通过 Azure 使用 OpenAI 的技术。财富 500 强中超过 65% 已在用 Azure OpenAI 服务。值得注意的是，这并非直接经由 OpenAI。只要 Microsoft 改推自家模型，OpenAI 就可能流失大量业务，而不需要 Google Deepmind 或 Amazon Anthropic 抢走任何份额。

## **分发与整合为王？**

随着 DeepSeek 和 Llama 3 405B 走向开源，企业几乎没有理由不自建模型托管。Zuckerberg 用开源模型拖慢竞争对手商业化步伐、同时吸引更多人才的战略正在创造奇迹。微调也不再是一项浩大工程——Databricks 同样极其擅长从零训练出优于 GPT 3.5 质量的通用模型。

OpenAI 的优势之一是他们在收集使用数据方面一直领先，但这一优势很快就会易主。因为 Meta 和 Google 都比 OpenAI 更直接地触达消费者。只有四分之一的美国人曾经试用过 ChatGPT，而且大多数人没有持续使用。未来绝大多数消费者 LLM 使用都将经由现有平台发生：Google、Instagram、WhatsApp、Facebook、iPhone/Android。

虽然 Meta 还没找到变现方法，但其由 Llama 3 70B 驱动的 Meta AI 已可在 Facebook、Instagram、WhatsApp 上使用。已宣布的推送范围已扩展到[包括美国在内的 14 个国家](https://about.fb.com/news/2024/04/meta-ai-assistant-built-with-llama-3/)，人口合计 11 亿。已经有数量极其可观的用户用上了优于免费版 ChatGPT 的模型。Meta AI 仍处于增长曲线早期，距离覆盖其全部 32.4 亿日活用户仅走完了三分之一。

虽然 Llama 3 70B 可能欠缺更大、更强模型的许多功能——但对于以移动为中心的用户（包括新兴市场的众多用户）而言，它很可能恰好是正确的产品市场契合——可以推测，这类移动优先用户的查询大概是简短的通识性问答，而非高输入 token 量的智能体重度用例。Meta 的部署对 Google 搜索的伤害，可能远超 Bing 或 Perplexity 未来的任何作为。

要服务 30 亿人——你显然需要一个小而高效的模型来压低推理成本。要么 Meta 已经把财务账算通了，要么就是准备好重金投入、在消费者 AI 领域跑马圈地。无论哪种，对在位者都是灾难。

而且整装待发的不止 Meta 一家——Google 的用户触达规模与 Meta 在同一量级。如果 Google 与 Apple 达成交易，[让它的 Gemini 模型独家登上了 iPhone](https://www.bloomberg.com/news/articles/2024-03-18/apple-in-talks-to-license-google-gemini-for-iphone-ios-18-generative-ai-tools)，那么十多年前 Google 用来巩固搜索市场霸主的同一套策略将在这里重演。

## **算力与资本为王？**

另一种可能的论点是算力与资本为王。若是如此，[王者是 Google](https://www.semianalysis.com/p/google-gemini-eats-the-world-gemini)，因为[他们 TPU 建设节奏极为激进](https://www.semianalysis.com/p/broadcoms-google-tpu-revenue-explosion)。讽刺的是，如今 Google 反而目标聚焦，把所有大规模训练力量集中到一个合并后的 Google Deepmind 团队；而 Microsoft 却开始分散焦点，把资源投向与 OpenAI 竞争的自家内部模型。

> 这里有一个资本问题：到了哪一步，继续投入资本就不值得了？
>
> [Mark Zuckerberg](https://www.youtube.com/watch?v=bc6uFV9CJGg&t=24s)

OpenAI 最大的风险之一，就是这场博弈最终只看资本。如果是那样，投资最多的科技公司就是赢家。虽然 Microsoft 今天投得最多，但他们相对 Meta、Google 和 Amazon/Anthropic 的领先并不大。Meta 和 Google 全神贯注，而 Amazon 和 Microsoft 因为对自家盟友 AI 实验室缺乏控制力，只能束着一只手臂打架。

自研芯片是另一个关键变量，因为它能大幅降低算力成本，相对于采购 Nvidia 芯片而言。[Microsoft 是其云中部署自研 AI 芯片最少的](https://www.semianalysis.com/p/datacenter-model)，而且至少到 2026 年都会如此。与此同时，[Google、Meta 和 Amazon 正在不同量级上爬坡其内部芯片](https://www.semianalysis.com/p/accelerator-model)，这给了它们算力成本上的优势。

虽然上面是一场好玩的「魔鬼代言人」练习，但我们并不认为 OpenAI 要完蛋了——这一切只是在下一代模型发布前，把空头论点演练一遍的表面文章。我们将在下文简要讨论。

[团体订阅享 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
