---
title: "DeepSeek 争议辨析：成本上的中国领先、真实训练成本、闭源模型利润率影响"
title_en: "DeepSeek Debates: Chinese Leadership On Cost, True Training Cost, Closed Model Margin Impacts"
subtitle: "H100 价格飙升、受补贴的推理定价、出口管制、MLA"
date: 2025-01-31
source: https://newsletter.semianalysis.com/p/deepseek-debates
crawled: 2026-09-15
authors: ["Dylan Patel", "AJ", "Doug", "Reyk Knuhtsen"]
tags: ["Accelerators", "LLMs", "Export Controls"]
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# DeepSeek 争议辨析：成本上的中国领先、真实训练成本、闭源模型利润率影响

> 原文：[DeepSeek Debates: Chinese Leadership On Cost, True Training Cost, Closed Model Margin Impacts](https://newsletter.semianalysis.com/p/deepseek-debates) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**H100 价格飙升、受补贴的推理定价、出口管制、MLA**

## DeepSeek 叙事席卷全球

DeepSeek 席卷了世界。过去一周，DeepSeek 是全球所有人唯一愿意谈论的话题。就目前的数据看，DeepSeek 的日流量已经远高于 Claude、Perplexity，甚至 Gemini。

但对这一领域的密切观察者来说，这并不算「新」闻。[我们](https://x.com/dylan522p/status/1819431961368129554)[已经](https://semianalysis.com/2024/05/07/openai-is-doomed-et-tu-microsoft/)[在](https://x.com/dylan522p/status/1828316816273195452)[谈论](https://x.com/dylan522p/status/1875594509339521414)[DeepSeek](https://x.com/dylan522p/status/1859302712803807696) 好几个月了（每个链接都是一例）。这家公司并不新，新的只是这种狂热的炒作。SemiAnalysis 一直认为 DeepSeek 极具才华，而美国更广泛的公众此前并不在意。当全世界终于投来关注时，却是以一种并不反映现实的狂热 hype 方式。

我们想指出，叙事相比上个月已经翻转：当时流行的说法是「scaling law 已被打破」——[我们驳斥过这一迷思](https://semianalysis.com/2024/12/11/scaling-laws-o1-pro-architecture-reasoning-training-infrastructure-orion-and-claude-3-5-opus-failures/)——现在的说法则成了「算法进步太快」，而这不知怎么又成了对 Nvidia 和 GPU 的利空。

当下的叙事是：DeepSeek 效率之高意味着我们不再需要更多算力，模型层面的变化已让一切都产能严重过剩。虽然杰文斯悖论（Jevons paradox）同样被过度炒作，但它更接近现实——这些模型已经激发了需求，并在 H100 与 H200 价格上产生了可观察的实际影响。

## DeepSeek 与幻方（High-Flyer）

High-Flyer（幻方量化）是一家中国对冲基金，也是最早在交易算法中使用 AI 的先行者之一。他们很早就认识到 AI 在金融以外领域的潜力，也洞察了 scaling（规模化）这一关键命题，因此持续增加 GPU 供给。在用数千 GPU 规模的集群进行模型实验之后，High-Flyer 于 2021 年投资了 10,000 张 A100 GPU——*在任何出口限制出台之前*。这笔投资回报丰厚。随着 High-Flyer 能力提升，他们认为时机已到，于 2023 年 5 月分拆出「DeepSeek」，以更专注地追求更强的 AI 能力。High-Flyer 自掏腰包资助了这家公司，因为当时外部投资者对 AI 兴趣寥寥——主要顾虑是缺乏商业模式。如今 High-Flyer 与 DeepSeek 经常共享资源，包括人力和算力。

DeepSeek 如今已成长为一项认真投入、系统推进的事业，绝不像许多媒体所说的那样是一个「副业项目」。我们有信心认为，即便计入出口管制的影响，他们的 GPU 累计投资也超过 5 亿美元。

![](https://substack-post-media.s3.amazonaws.com/public/images/39cab87f-3291-4eb9-9355-c1b1eb696e79_975x368.png)
*来源：SemiAnalysis、Lennart Heim*

## GPU 供给状况

我们认为他们拥有约 50,000 张 Hopper 架构 GPU 的使用权——这并不等同于一些人所说的 50,000 张 H100。Nvidia 为满足不同法规要求推出了 H100 的不同合规变体（H800、H20），而目前中国模型厂商能买到的只有 H20。注意 H800 的算力与 H100 相同，只是网络带宽更低。

我们认为 DeepSeek 拥有约 10,000 张 H800 和约 10,000 张 H100 的使用权。此外，他们还有更多 H20 的在手订单——过去 9 个月里，Nvidia 已生产超过 100 万张这款中国专属 GPU。这些 GPU 由 High-Flyer 与 DeepSeek 共享，并在一定程度上做了地理分布，用于交易、推理、训练和研究。更具体的详细分析请参阅我们的[加速器行业模型](https://semianalysis.com/accelerator-industry-model/)。

![](https://substack-post-media.s3.amazonaws.com/public/images/055c28ff-9ad9-422a-a8b5-61cbfa326e68_2196x872.png)
*来源：SemiAnalysis*

我们的分析显示，DeepSeek 的服务器资本开支（capex）总额约 16 亿美元，运营此类集群还伴随约 9.44 亿美元的可观成本。类似地，所有 AI 实验室和超大规模云厂商所持有的、用于研究和训练等各类任务的 GPU，都远多于他们投入单次训练运行的规模——因为资源的集中调度本身就是难题。X.AI 是 AI 实验室中的特例：其所有 GPU 都集中在一个地点。

DeepSeek 的人才完全来自中国，不太在意过往履历，重点考察能力与好奇心。DeepSeek 定期在北京大学、浙江大学等顶尖高校举办招聘活动，许多员工即毕业于此。岗位不一定预先设定，录用者被[赋予很大灵活度](https://www.chinatalk.media/p/deepseek-ceo-interview-with-chinas)，招聘广告甚至以「可无限制使用数万张 GPU」为卖点。他们给出的条件极具竞争力，据称会为有潜力的候选人开出超过 130 万美元的年薪，远高于竞争的中国大型科技公司和 Moonshot 等 AI 实验室。公司约有 150 名员工，且在快速扩张。

历史一再表明，规模小、资金充足、高度专注的初创公司往往能推动可能性的边界。DeepSeek 没有 Google 那样的官僚体系，又因资金自给，可以快速验证想法。同时，与 Google 类似，DeepSeek（在多数情况下）运营自己的数据中心，不依赖外部第三方或供应商。这为实验打开了更大空间，使其能够在整个技术栈上做创新。

我们认为他们是当今最好的「开放权重（open weights）」实验室，胜过 Meta 的 Llama 系列努力、Mistral 以及其他同行。

## DeepSeek 的成本与性能

DeepSeek 的定价与效率引发了本周的狂热，头条数字是 DeepSeek V3「600 万美元」的训练成本。这一说法是错误的。这好比指着产品物料清单（BOM）中的某一项，把它说成产品的全部成本。预训练成本只是总成本中非常窄的一块。

## 训练成本

我们认为预训练数字与该公司在这个模型上的实际投入相去甚远。我们确信，其公司历史上的硬件支出远高于 5 亿美元。在模型开发过程中，要形成新的架构创新，需要在测试新想法、新架构方案和消融实验（ablation）上投入大量资金。DeepSeek 的关键创新之一——多头潜在注意力（Multi-Head Latent Attention）——[耗时数月](https://www.chinatalk.media/p/deepseek-ceo-interview-with-chinas)开发，消耗了整支团队的人力与 GPU 时。

论文中的 600 万美元只对应预训练运行的 GPU 成本，而这只是模型总成本的一部分。被排除在外的还有 R&D 和硬件本身的总拥有成本（TCO）等拼图中的重要部分。作为参照，Claude 3.5 Sonnet 的训练成本为数千万美元；如果那就是 Anthropic 所需的全部成本，他们就不会再向 Google 融资数十亿美元、向 Amazon 融资数百亿美元。原因在于他们还必须做实验、探索新架构、收集和清洗数据、支付员工薪酬等等。

那么 DeepSeek 是怎么拥有如此大规模集群的？出口管制的滞后是关键，我们将在下文出口管制部分展开。

## 追赶差距——V3 的性能

V3 无疑是一个出色的模型，但有必要说清楚：*相对于什么*出色。许多人把 V3 与 GPT-4o 相提并论，强调 V3 胜过 4o 的性能。这是事实，但 GPT-4o 发布于 *2024 年 5 月*。AI 迭代很快，从算法进步的角度看，2024 年 5 月已是「上一个时代」。此外，经过一段时间后，用更少算力实现相当或更强的能力并不令我们意外。推理成本的持续崩塌正是 AI 进步的标志。

![](https://substack-post-media.s3.amazonaws.com/public/images/907678eb-2886-499e-ad43-36c9fd9be879_975x459.png)
*来源：SemiAnalysis*

一个例子是：如今能在笔记本上运行的小模型已具备与 GPT-3 相当的性能，而 GPT-3 当年需要超级计算机训练、多张 GPU 推理。换言之，算法进步让同等能力的模型可以用更少算力完成训练和推理，这一模式已反复上演。这一次世界之所以注意到，是因为它来自一家*中国的*实验室。但小模型变强并不是新鲜事。

![](https://substack-post-media.s3.amazonaws.com/public/images/b39c0193-339c-4e63-bb1d-55504b1e5d6e_975x554.png)
*来源：SemiAnalysis、Artificialanalysis.ai*

到目前为止，这一模式给我们的观察是：AI 实验室投入更多的绝对美元，以换取*更多*的智能。估计显示算法进步速度为[每年 4 倍](https://epoch.ai/blog/algorithmic-progress-in-language-models)，即每过一年，实现同等能力所需的算力减少为原来的四分之一。Anthropic CEO Dario 则认为算法进步更快，可带来 [10 倍的改进](https://darioamodei.com/on-deepseek-and-export-controls)。就 GPT-3 水平能力的推理价格而言，成本已经下降了 1200 倍。

考察 GPT-4 的成本时，我们看到了类似的成本下降，只是处于曲线更早的阶段。成本降幅随时间收窄可以用一点解释：此时不再像上图那样保持能力恒定。在这一案例中，算法改进与优化带来了 10 倍的成本下降，同时能力还在提升。

![](https://substack-post-media.s3.amazonaws.com/public/images/2c3a6b7a-93dd-4f6c-9367-b3a93146913b_1024x610.png)
*来源：SemiAnalysis、OpenAI、Together.ai*

需要说明，DeepSeek 的独特之处在于他们第一个达到了这一水平的成本与能力组合。以开放权重形式发布也使其与众不同，但此前 Mistral 和 Llama 系列模型同样这样做过。DeepSeek 已把成本压到这个水平，但到今年年底，若成本再降 5 倍，请不要感到震惊。

## R1 的性能是否与 o1 相当？

另一方面，R1 取得了与 o1 相当的结果，而 o1 不过在 9 月才公布。DeepSeek 为何能如此迅速地追上？

答案在于：推理是一个新范式，迭代速度更快、唾手可得的成果更多——相比旧范式，用更少的算力就能获得有意义的收益。正如我们的 [scaling law 报告](https://semianalysis.com/2024/12/11/scaling-laws-o1-pro-architecture-reasoning-training-infrastructure-orion-and-claude-3-5-opus-failures/)所述，旧范式依赖预训练，而预训练正变得越来越贵、越来越难从中取得稳健收益。

新范式通过合成数据生成与后训练阶段的强化学习（RL），在既有模型上强化推理能力，能以更低代价更快取得进展。进入门槛低加上优化路径明确，使 DeepSeek 能以快于常规的速度复现 o1 的方法。随着各家学会在新范式中进一步 scale，我们预计能力追平的时间差会重新拉大。

请注意，R1 论文*只字未提*所使用的算力。这并非偶然——为 R1 后训练生成合成数据本身就需要可观的算力，遑论 RL。R1 是一个非常好的模型，我们不否认这一点；如此迅速地追平推理前沿，客观上令人印象深刻。DeepSeek 是中国团队且用更少资源完成追赶，这让其成就加倍耀眼。

但 R1 提到的部分基准测试也*有误导性*。比较 R1 与 o1 需要谨慎，因为 R1 恰恰略去了自己不占优的基准。而且在推理性能打平的同时，R1 并非在所有指标上都明确胜出，在许多场景下它不如 o1。

![](https://substack-post-media.s3.amazonaws.com/public/images/28789d0f-8d48-491b-af3d-2012619f5736_1020x354.png)
*来源：(Yet) another tale of Rise and Fall: DeepSeek R1*

而且我们还没提到 o3。o3 的能力显著高于 R1 和 o1。事实上，OpenAI 最近公布了 o3 的结果，其基准曲线近乎垂直拉升。「深度学习撞墙了」——但这是另一种墙。

![](https://substack-post-media.s3.amazonaws.com/public/images/91731feb-d9fd-438b-8931-447b6cf70a60_975x635.png)
*来源：AI Action Summit*

## Google 的推理模型与 R1 同样出色

在 R1 被狂热追捧之际，一家市值 2.5 万亿美元的美国公司早在一个月前就以更低价格发布了推理模型：Google 的 Gemini Flash 2.0 Thinking。该模型已可使用，而且*比 R1 便宜得多*——即便通过 API 使用时其上下文长度还大得多。

就已公布的基准而言，Flash 2.0 Thinking 胜过 R1，不过基准测试并不能说明全部。Google 只公布了 3 项基准，因此图景并不完整。尽管如此，我们认为 Google 的模型是扎实的，在许多方面可与 R1 比肩，却没有得到任何炒作。这可能与 Google 平淡的 go-to-market 策略和欠佳的用户体验有关，但 R1 是一个来自中国的「意外惊喜」也是原因之一。

![](https://substack-post-media.s3.amazonaws.com/public/images/eaf6e4b3-1b75-4e21-a157-52c29add65ac_1017x1024.jpeg)

需要说明，这些丝毫不减 DeepSeek 的卓越成就。DeepSeek 作为一家动作快、资金足、聪明且专注的初创公司，其组织形态正是它能抢在 *Meta* 等巨头之前发布推理模型的原因，这一点值得称道。

## 技术成就

DeepSeek 破解了密码，解锁了头部实验室尚未实现的创新。我们预计，DeepSeek 公开的任何改进都几乎会被西方实验室立刻跟进。

这些改进是什么？大部分架构层面的成果具体落在 V3 上——它也是 R1 的基座模型。下面逐一展开这些创新。

## 训练（预训练与后训练）

DeepSeek V3 以前所未见的规模使用了多 token 预测（Multi-Token Prediction，MTP）——新增的注意力模块会预测接下来的若干 token，而不只是单个 token。这在训练期间提升模型性能，推理时则可丢弃。这是以更低算力实现更高性能的算法创新的典型例子。

还有一些附加考量，比如在训练中使用 FP8 精度，但美国头部实验室使用 FP8 训练已有一段时间。

DeepSeek v3 也是一个混合专家（MoE）模型：由许多各有专长的小「专家」组成一个大模型——这是一种涌现行为。MoE 模型长期面临的一个难题是如何决定每个 token 交给哪个子模型（即「专家」）。DeepSeek 实现了一个「门控网络（gating network）」，以均衡的方式把 token 路由到合适的专家，同时不损害模型性能。这意味着路由非常高效：训练时每个 token 相对于模型总参数量只更新少量参数。这既提升了训练效率，也压低了推理成本。

尽管有人担心 MoE 的效率收益会抑制投资，[Dario 指出](https://darioamodei.com/on-deepseek-and-export-controls)，能力更强的 AI 模型带来的经济价值如此巨大，以至于任何成本节省都会被迅速再投入于构建更大的模型。MoE 的效率提升不会减少总体投资，反而会加速 AI 的规模化。这些公司正全力以赴：把模型 scale 到更多算力，同时在算法上让其更高效。

至于 R1，它极大地受益于强大的基座模型（v3）。这部分归功于强化学习（RL）。RL 有两个重点：格式（确保输出连贯）与有用性和无害性（确保模型实用）。推理能力是在合成数据集上微调模型的过程中涌现的。这一点**[正如我们的 scaling law 文章所述](https://semianalysis.com/2024/12/11/scaling-laws-o1-pro-architecture-reasoning-training-infrastructure-orion-and-claude-3-5-opus-failures/)**，与 o1 的经历一致。注意 R1 论文未提及算力，原因在于：一旦披露算力用量，就会显示他们拥有的 GPU 比其叙事所暗示的更多。这一规模的 RL 需要大量算力，尤其是生成合成数据。

此外，DeepSeek 所用的数据中有一部分似乎来自 OpenAI 的模型。我们认为这将对「从输出蒸馏」的政策产生影响。这在服务条款中已属违规；展望未来，一种新趋势可能是某种形式的 KYC（Know Your Customer，了解你的客户）机制来阻止蒸馏。

说到蒸馏，R1 论文中最有意思的部分也许是：用推理模型的输出微调非推理小模型，把后者变成推理模型。其数据集构建共包含 80 万（800k）条样本，如今任何人都可以用 R1 的思维链（CoT）输出构造自己的数据集，并借助这些输出打造推理模型。我们可能会看到更多小模型展现推理能力，从而提升[小模型](https://importai.substack.com/p/import-ai-397-deepseek-means-ai-proliferation)的表现。

## 多头潜在注意力（MLA）

MLA 是 DeepSeek 推理价格大幅下降背后的关键创新。原因在于：与标准注意力相比，MLA 将每个查询所需的 KV 缓存减少约 *93.3%*。KV 缓存是 transformer 模型中的一种内存机制，存储表示对话上下文的数据，从而减少不必要的计算。

正如我们在 scaling law 文章中讨论的，KV 缓存随对话上下文增长而增长，带来可观的内存约束。大幅降低每个查询所需的 KV 缓存，就减少了每个查询所需的硬件，进而降低成本。不过我们认为，DeepSeek 是在按成本价提供推理以换取市场份额，实际上并不赚钱。Google 的 Gemini Flash 2 Thinking 依然更便宜，而 Google 不太可能按成本价出售。MLA 尤其引起了多家美国头部实验室的关注。MLA 随 DeepSeek V2 于 2024 年 5 月发布。得益于比 H100 更高的内存带宽和容量，DeepSeek 在 H20 上运行推理负载也获得了额外效率。他们还宣布了与华为的合作关系，但迄今为止在昇腾（Ascend）算力上实际完成的工作很少。

我们认为最有意思的影响恰恰落在利润率上，以及这对整个生态系统的意义。下面我们给出了对整个 AI 行业未来定价结构的看法，详细说明为什么我们认为 DeepSeek 在补贴价格，以及为什么我们看到杰文斯悖论正在占上风的早期迹象。我们还会评论其对出口管制的影响、随着 DeepSeek 主导地位增强中国政府（CCP）可能作何反应等话题。
