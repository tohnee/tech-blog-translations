---
title: "TPUv7：Google 向王者挥棒"
title_en: "TPUv7: Google Takes a Swing at the King"
subtitle: "CUDA 护城河或将终结？Anthropic 的 1GW+ TPU 采购，Meta/SSI/xAI/OAI/Anthro 买得越多（TPU）省得越多（GPU 资本开支），下一代 TPUv8AX 与 TPUv8X 对决 Vera Rubin"
date: 2025-11-28
source: https://newsletter.semianalysis.com/p/tpuv7-google-takes-a-swing-at-the
crawled: 2026-09-15
authors: ["Dylan Patel", "Myron Xie", "Daniel Nishball", "Wei Zhou", "Jeremie Eliahou Ontiveros", "Ivan Chiam", "Cheang Kang Wen", "Clara Ee", "Wega Chu", "Kimbo Chen", "AJ", "Michael Chen"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# TPUv7：Google 向王者挥棒

> 原文：[TPUv7: Google Takes a Swing at the King](https://newsletter.semianalysis.com/p/tpuv7-google-takes-a-swing-at-the) · SemiAnalysis
> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**CUDA 护城河或将终结？Anthropic 的 1GW+ TPU 采购，Meta/SSI/xAI/OAI/Anthro 买得越多（TPU）省得越多（GPU 资本开支），下一代 TPUv8AX 与 TPUv8X 对决 Vera Rubin**

当今世界上最好的两个模型——Anthropic 的 Claude 4.5 Opus 和 Google 的 Gemini 3——其大部分训练与推理基础设施都运行在 Google 的 TPU 和 Amazon 的 Trainium 上。如今 Google 开始向多家公司实体出售 TPU。这是英伟达（Nvidia）统治地位的终结吗？

AI 时代的黎明已经到来，而理解这一点至关重要：AI 驱动的软件，其成本结构与传统软件大相径庭。芯片微架构与系统架构对这些创新型新软件的开发与可扩展性起着至关重要的作用。与开发人员成本占比较高的前几代软件相比，AI 软件所运行的硬件基础设施对资本开支（capex）和运营开支（opex）、进而对毛利率的影响要大得多。因此，为了能够部署 AI 软件，投入大量精力优化 AI 基础设施就比以往任何时候都更为关键。在基础设施上占优的公司，在部署和规模化 AI 应用方面同样会占据优势。

早在 2006 年，Google 就[开始鼓吹构建 AI 专用基础设施的理念](https://cloud.google.com/blog/products/ai-machine-learning/an-in-depth-look-at-googles-first-tensor-processing-unit-tpu)，但到 2013 年，问题彻底爆发。他们意识到，若想以任何像样的规模部署 AI，数据中心数量就必须翻倍。为此，他们开始为自研 TPU 芯片打基础，这些芯片于 2016 年投入生产。有趣的是，可以将其与 Amazon 对比：同一年，Amazon 也意识到自己需要打造定制芯片。[2013 年，他们启动了 Nitro 项目](https://www.semianalysis.com/i/108660819/amazon-nitro)，专注于[开发优化通用 CPU 计算与存储的芯片](https://www.semianalysis.com/i/108660819/amazon-nitro)。两家截然不同的公司，为[不同的计算时代与软件范式](https://www.semianalysis.com/i/108660819/the-next-era-of-computing)各自优化了基础设施投入。

我们一直认为，TPU 是全球最好的 AI 训练与推理系统之一，与丛林之王 Nvidia 不分伯仲。两年半前我们撰文论述 TPU 的霸主地位，这一论断已被证明非常正确。

TPU 的成绩有目共睹：Gemini 3 是世界上最好的模型之一，且完全在 TPU 上训练而成。在本报告中，我们将讨论 Google 战略的重大转变——真正面向外部客户将 TPU 商业化，成为 Nvidia 最新、也最具威胁性的商用芯片（merchant silicon）挑战者。

我们计划：

- （重新）向我们的客户和新读者介绍外部 TPU 客户快速增长的商业成功——从 Anthropic 开始，延伸到 Meta、SSI、xAI，甚至可能的 OpenAI……
- 证明：买得越多（TPU），省得越多（NVIDIA GPU 资本开支）！OpenAI 甚至还没部署 TPU，就已经因为竞争威胁让整个计算集群拿到约 30% 的折扣，从而提升了每 TCO 的性能
- 解释 AI 基础设施的循环经济（circular economy）交易。
- 回顾我们最初的 TPU 深度解析，温习从硅片到软件层的 TPU 硬件栈。
- 涵盖开放软件生态方面的积极进展，以及 Google 让 TPU 生态成为 CUDA 护城河真正挑战者所缺失的关键一环：开源其 XLA:TPU 编译器、运行时以及多 pod 的「MegaScaler」代码。
- 在付费墙内，我们将讨论这对 Nvidia 护城河的影响，并将 Vera Rubin 与下一代 TPUv8AX/8X（即 Sunfish/Zebrafish）进行比较
- 同时讨论对 Nvidia 的长期威胁。

首先，来谈谈这一消息对生态系统的影响。TPU 的性能显然已经引起了对手的注意。Sam Altman 已承认 [OpenAI 前方「气氛不妙」（rough vibes）](https://www.theinformation.com/articles/openai-ceo-braces-possible-economic-headwinds-catching-resurgent-google?rc=63yhkf)，因为 Gemini 抢走了 OpenAI 的风头。Nvidia 甚至发布了一份安抚人心的公关声明，告诉所有人保持冷静、照常行事——我们远远领先于竞争对手。

![](https://substack-post-media.s3.amazonaws.com/public/images/416a8d57-1b5e-4ef6-8fd3-51ff018e02d2_916x562.png)
*来源：Nvidia*

我们理解这是为什么。过去几个月，Google DeepMind、GCP 与 TPU 这个「铁三角」捷报频传：TPU 产量预测被大幅上调、Anthropic 超 1GW 的 TPU 建设、在 TPU 上训练出的 SOTA 模型 Gemini 3 与 Opus 4.5，以及如今排着队要 TPU 的目标客户名单不断扩大（Meta、SSI、xAI、OAI）。这推动市场对 Google 及 TPU 供应链的估值大幅重估（re-rating），而以 Nvidia GPU 为核心的供应链则相应失血。尽管 Google 与 TPU 供应链的「突然」崛起令许多人措手不及，但 SemiAnalysis 机构产品的订阅用户[在过去一年里](https://semianalysis.com/institutional/google-selling-tpu-systems-externally-further-tpu-revisions/)一直在提前布局这一趋势。

![](https://substack-post-media.s3.amazonaws.com/public/images/78b1f0fd-ac35-4791-98d5-3c162727ffa3_1316x832.png)
*来源：SemiAnalysis 与 Bloomberg*

Nvidia 处于守势的另一个原因，是质疑者的声浪日益高涨。他们声称 Nvidia 通过给烧钱的 AI 初创公司输血，撑起了一个「循环经济」，本质上就是把钱从一个口袋掏出来、多绕几道手续再放进另一个口袋。我们认为这种观点有失偏颇，但它显然刺痛了 Nvidia 的神经。其财务团队发布了一份详细的回应，转载如下。

![](https://substack-post-media.s3.amazonaws.com/public/images/b58d9d28-2045-4e28-853e-e94ee4380bf1_922x631.png)
*来源：Nvidia FY26Q3 财报回应、Bernstein Research*

我们认为，更现实的解释是：Nvidia 的目标是通过股权投资来保住自己在基础模型实验室（foundation labs）中的主导地位，而不是降价——降价会拉低毛利率，并引发投资者的普遍恐慌。下面我们梳理 OpenAI 与 Anthropic 的相关交易安排，展示前沿实验室如何通过购买 TPU、甚至仅仅是威胁要购买 TPU，来降低 GPU 的总拥有成本（TCO）。

![](https://substack-post-media.s3.amazonaws.com/public/images/6c9a4819-b0ac-4113-ac86-4795bd100188_977x275.png)
*来源：SemiAnalysis TCO 模型、Anthropic 与 OpenAI*

**OpenAI 甚至还没部署 TPU，就已经在整个实验室范围的 NVIDIA 集群上省下了约 30% 的成本。这说明 TPU 的每 TCO 性能优势强大到什么程度——还没开机，采用 TPU 的收益就已经到手了。**

我们的[加速器行业模型](https://semianalysis.com/accelerator-model/)、[数据中心行业模型](https://semianalysis.com/datacenter-industry-model/)与[核心研究](https://semianalysis.com/core-research/)订阅用户，早在消息公布并成为市场共识之前，就看清了行业影响。8 月初，我们[向加速器模型客户分享](https://semianalysis.com/institutional/google-selling-tpu-systems-externally-further-tpu-revisions/)了我们的观察：供应链中 Broadcom/Google TPU 的 2026 年订单将出现大规模上调。我们还揭示，订单增长的原因在于 Google 将开始向[多个外部客户](https://semianalysis.com/institutional/googles-merchant-tpu-customer-is-xai/)出售整机系统。9 月初，我们披露其中一个大外部客户将是 [Anthropic](https://semianalysis.com/institutional/anthropic-tpu-gcp/)，需求至少 100 万颗 TPU。这一点在 10 月得到 [Anthropic 与 Google 的官方确认](https://www.anthropic.com/news/expanding-our-use-of-google-cloud-tpus-and-services)。我们还在 11 月 7 日、比其他人早数周指出 [Meta 将成为 TPU 大客户](https://semianalysis.com/institutional/meta-tpu-customer-switch-skus-update-large-cisco-2026-orders-mediatek-tpu-update/)。此外，我们还讨论过其他客户。

因此，对于这场迄今为 AI 交易（AI Trade）中最大的业绩分化之一，我们的机构客户早已心中有数。SemiAnalysis 之所以能率先披露所有这些洞察，是因为没有第二家研究公司能够把从晶圆厂到供应链、再到数据中心和实验室的全链条 dots 串起来。想获取这些洞察并保持领先，请联系：[sales@semianalysis.com](mailto:sales@semianalysis.com)

下面进入交易本身。

# Google 的 TPU 大规模外销攻势与 Anthropic 交易

TPU 技术栈长期以来足以与 Nvidia 的 AI 硬件抗衡，但它主要承载 Google 的内部工作负载。典型的 Google 做派是：即便 2018 年就已向 GCP 客户开放 TPU，它也从未真正将 TPU 商业化。这种情况正在改变。过去几个月，Google 在整个技术栈上全面动员，通过 GCP 或以商用厂商身份出售完整 TPU 系统的方式，把 TPU 带给外部客户。这家搜索巨头正在利用其强大的自研芯片设计能力，成为一家真正差异化的云服务商。同时，这也契合重要客户（marquis customer）Anthropic 持续推进摆脱 NVDA 依赖的多元化战略。

![](https://substack-post-media.s3.amazonaws.com/public/images/57447724-b889-4bd8-b4cf-3147213a8f2d_3303x1653.png)
*来源：SemiAnalysis Tokenomics 模型*

Anthropic 交易是这场攻势的重要里程碑。我们了解到，GCP CEO Thomas Kurian 在谈判中扮演了核心角色。Google 早早押注，激进参与 Anthropic 的多轮融资，[甚至同意放弃投票权、并将持股比例上限设在 15%](https://www.nytimes.com/2025/03/11/technology/google-investment-anthropic.html)，以推动 TPU 在 Google 内部之外的更广泛应用。前 DeepMind TPU 人才在该实验室的存在也让这一战略更为顺畅——最终 Anthropic 在包括 TPU 在内的多种硬件上训练了 Sonnet 和 Opus 4.5。如下图所示，在我们的 AI 实验室逐楼追踪（building-by-building tracker）中，Google 已经为 Anthropic 建成了一座相当规模的设施。

![](https://substack-post-media.s3.amazonaws.com/public/images/4d02869e-1b4e-4590-9cf6-0bd239188c7f_1746x1070.png)
*来源：SemiAnalysis 数据中心行业模型*

除了通过 GCP 租用 Google 数据中心内的容量，Anthropic 还将在自己的设施中部署 TPU——这使 Google 得以作为真正的商用硬件厂商，与 Nvidia 正面竞争。

关于 100 万颗 TPU 的拆分：

1. 交易第一阶段涵盖 40 万颗 TPUv7 Ironwood，按成品机柜计价值约 100 亿美元，将由 Broadcom **直接出售**给 Anthropic。Anthropic 正是 Broadcom 最近一次财报电话会上提及的第四家客户。Fluidstack——[ClusterMax 金牌评级的新兴 GPU 云（neocloud）](https://newsletter.semianalysis.com/p/clustermax-20-the-industry-standard)服务商——将负责现场安装、布线、烧机（burn-in）、验收测试和远程值守（remote hands）等工作，Anthropic 由此把物理服务器管理外包出去。数据中心基础设施将由 TeraWulf（WULF）和 Cipher Mining（CIFR）提供。
2. 其余 60 万颗 TPUv7 将通过 GCP 租用，我们估计这笔交易约合 420 亿美元的剩余履约义务（RPO），占第三季度 GCP 报告的 490 亿美元 backlog 增量的大头。
3. 我们认为，未来几个季度与 Meta、OAI、SSI 和 xAI 的额外交易，可能为 GCP 带来更多 RPO 及直接硬件销售收入。

尽管内外部需求都极为旺盛，Google 却一直无法按自己期望的速度部署 TPU。虽然它对硬件供应的掌控力强于那些仍需讨好黄仁勋（Jensen）的其他超大规模云厂商，但 Google 的主要瓶颈是电力。

其他超大规模云厂商纷纷扩建自有园区、并锁定了大量托管（colocation）容量，而 Google 的动作要慢得多。我们认为核心症结在于合同与行政流程。每接入一家新的数据中心供应商都需要签订一份主服务协议（MSA），而这些动辄数十亿美元、跨越多年的承诺难免伴随官僚流程。但 Google 的流程尤其缓慢，从初步洽谈到签署 MSA 往往长达三年。

Google 的变通办法对新兴 GPU 云（neocloud）和寻求转型 AI 数据中心基础设施的加密矿企影响重大。Google 不直接租赁，而是提供信用兜底（credit backstop）——一张表外「欠条（IOU）」，在 Fluidstack 付不起数据中心租金时兜底。

![](https://substack-post-media.s3.amazonaws.com/public/images/52a04a94-9e9e-445e-b806-5a6cebd3f244_2236x1228.png)
*来源：TeraWulf*

Fluidstack 这类新兴 GPU 云敏捷灵活，更容易与转型矿企这类新型数据中心供应商打交道。这一机制正是我们[看多加密矿产行业](https://www.fabricatedknowledge.com/p/crypto-datacenters-nav)的关键依据——尤其值得一提的是，年初股价还大幅低于现在时，我们就[点名了包括 IREN 和 Applied Digital 在内的多家公司](https://youtu.be/-H4GakGDBy8?si=ZtQDsn9ZWHyitCMC)。

矿企的机会建立在一个简单的动态之上：数据中心行业面临严重的电力约束，而加密矿企已通过购电协议（PPA）和既有电力设施掌握着大量容量。我们预计未来数周和数季度还将有更多协议落地。

# Google 如何重塑新兴 GPU 云市场

在 Google/Fluidstack/TeraWulf 这笔交易之前，我们从没见过新兴 GPU 云市场上仅凭一张表外「欠条」就能达成的交易。这笔交易之后，我们认为它已成为事实上的新融资模板。这解决了新兴 GPU 云在锁定数据中心容量、扩张业务时的一个核心难题：

- GPU 集群的有效经济寿命为 4-5 年
- 大型数据中心租约通常长达 15 年以上，典型回收期约 8 年。

这种期限错配使新兴 GPU 云和数据中心供应商为项目融资变得非常复杂。但随着「超大规模云厂商兜底（hyperscaler backstop）」的兴起，我们认为融资难题已经解决。我们预计新兴 GPU 云行业将迎来新一轮增长。请参阅我们的[加速器](https://semianalysis.com/accelerator-model/)和[数据中心](https://semianalysis.com/datacenter-industry-model/)模型，了解主要受益者。以上便是 Anthropic 交易背后的来龙去脉，现在让我们进入硬件部分。

此外，那些把黄仁勋（Jensen）列为股东的新兴 GPU 云——如 CoreWeave、Nebius、Crusoe、Together、Lambda、Firmus 和 Nscale——都有明显的动机在自己的数据中心里**不采用**任何竞争技术：TPU、AMD GPU、甚至 Arista 交换机都是禁区！这就给 TPU 托管市场留下了一个巨大的空缺，目前由加密矿企 + Fluidstack 的组合填补。未来几个月，我们预计会看到更多新兴 GPU 云做出艰难抉择：是追逐不断增长的 TPU 托管机会，还是确保拿到最新最强 Nvidia Rubin 系统的配额。

# TPUv7 Ironwood——为什么 Anthropic 和其他客户想要 TPU？

答案很简单：它是一颗强芯，装在一个出色的系统里，这个组合为 Anthropic 提供了极具吸引力的性能与 TCO。两年半前，我们撰文分析过 Google 的计算基础设施优势。即便当时纸面硅片规格落后于 Nvidia，Google 的系统级工程仍让 TPU 技术栈在性能和成本效率上与 Nvidia 分庭抗礼。

我们当时主张「系统比微架构更重要」，过去两年不断印证这一观点。Anthropic 的大规模 TPU 订单是对该平台技术实力的直接背书。GPU 生态同样在向前演进：Nvidia 的 GB200 是一次重大跃迁，推动 Nvidia 从只设计芯片封装的公司，转变为设计完整服务器的真正系统公司。

说到 GB200 在机柜级互连上的巨大创新，有一个被低估的事实：Google 从 2017 年的 TPU v2 开始，就在机柜内和跨机柜纵向扩展 TPU 了！在报告后文，我们将深度解析 Google 的 ICI 纵向扩展网络——它是 Nvidia NVLink 唯一真正的对手。

Google 最新的 Gemini 3 模型如今被视为最先进的前沿大语言模型。与**所有**更早版本的 Gemini 一样，它完全在 TPU 上训练。这一结果为 TPU 的能力和 Google 更广泛的基础设施优势提供了实证。

如今人们的注意力往往集中在推理和后训练（post-training）硬件上，但前沿模型的预训练（pre-training）仍然是 AI 硬件中最困难、最消耗资源的挑战。TPU 平台已经决定性地通过了这场考验。这与竞争对手形成鲜明对比：自 2024 年 5 月的 GPT-4o 以来，OpenAI 的领军研究者们还没有完成过一次被广泛部署的、面向新前沿模型的完整规模预训练运行——这反衬出 Google 的 TPU 集群已经跨过了多么显著的技术门槛。

新模型的关键亮点之一，是工具调用（tool calling）和智能体（agentic）能力的显著提升，尤其是在具有经济价值的长周期（longer-horizon）任务上。Vending Bench 是一项评估，让模型扮演一家模拟自动售货机企业的老板，以此衡量模型能否长期经营一门生意——Gemini 3 碾压了竞争对手。

![](https://substack-post-media.s3.amazonaws.com/public/images/b2e21fa5-631e-460b-bc7b-280cbac462bf_1944x837.png)
*来源：Vending-Bench*

这次发布带来的不仅是能力提升，还有新产品。Antigravity 是 Google 对 OpenAI Codex 的回应，源自对 Windsurf 前 CEO Varun Mohan 及其团队的收购式招聘（acqui-hire），正式宣告 Gemini 加入 vibe coding 的吞 token 大战。

对于一家核心业务过去并非——或者说曾经并非——硬件的公司来说，Google 能悄无声息地挤进并在最困难的硬件问题之一上建立性能领先，确实是一项了不起的壮举。

# 微架构依然举足轻重：Ironwood 逼近 Blackwell

「系统比微架构更重要」的推论是：虽然 Google 一直在系统与网络设计上推进边界，TPU 硅片本身过去并不算太开创性。此后，TPU 硅片在最新几代中取得了巨大进步。

从一开始，Google 的设计理念在硅片上就比 Nvidia 更为保守。历史上，TPU 的峰值理论 FLOPS 和内存规格都显著低于同期对应的 Nvidia GPU。

原因有三。其一，Google 内部高度重视基础设施的「RAS」（可靠性、可用性与可维护性）。Google 宁愿牺牲绝对性能来换取更高的硬件正常运行时间。把硬件跑到极限意味着更高的故障率，而这会在系统停机和热备件方面带来实实在在的 TCO 代价。毕竟，用不了的硬件，其相对性能的 TCO 是无穷大。

其二，直到 2023 年，Google 的主要 AI 工作负载都是支撑其核心搜索与广告业务的推荐系统模型。推荐系统（RecSys）工作负载的算术强度（arithmetic intensity）远低于 LLM 工作负载，这意味着相对每比特传输的数据，所需的 FLOPs 更少。

![](https://substack-post-media.s3.amazonaws.com/public/images/543cf57c-a4b5-40a3-98d0-7443c7c4f841_1906x1060.png)
*来源：Meta*

其三，在于对外宣传的「峰值理论 FLOPS」数字的实际用途，以及这些数字可以被如何操纵。Nvidia 和 AMD 这类商用 GPU 厂商希望为自家芯片宣传尽可能漂亮的性能规格，这激励它们把宣传 FLOPS 拉到尽可能高的数字。实践中，这些数字根本无法持续达到。反观 TPU，它主要面向 Google 内部，几乎没有对外夸大规格的压力。这带来一些重要影响，我们后文详述。往好处想，可以说 Nvidia 更擅长 DVFS（动态电压频率调节），因此乐于只报峰值规格。

进入 LLM 时代之后，Google 的 TPU 设计理念出现了明显转向。从最近两代 LLM 时代之后设计的 TPU——TPUv6 Trillium（Ghostlite）和 TPUv7 Ironwood（Ghostfish）——可以清楚看到这种变化。下图可见，TPUv4 和 v5 的计算吞吐量远低于当时的 Nvidia 旗舰。TPUv6 在 FLOPs 上已非常接近 H100/H200，但比 H100 晚了两年。到了 TPU v7，差距进一步收窄：服务器仅晚几个季度可用，峰值理论 FLOPs 却已几乎持平。

![](https://substack-post-media.s3.amazonaws.com/public/images/9582080e-9c38-4b5e-b964-ad512e9a9106_2034x1188.png)
*来源：SemiAnalysis、Nvidia、Google*

是什么驱动了这些性能提升？部分原因是 Google 开始在 TPU 爬坡量产之际就公布，而不是等下一代都部署完了才官宣。此外，TPU v6 Trillium 与 TPU v5p 采用相同的 N5 制程节点、硅片面积相近，却以显著更低的功耗交付了整整 2 倍的峰值理论 FLOPS！对 Trillium 而言，Google 把每个脉动阵列（systolic array）的规模从 128 x 128 扩大到 256 x 256，正是阵列尺寸的扩大带来了算力的提升。

![](https://substack-post-media.s3.amazonaws.com/public/images/0be58268-c1c0-443e-a511-f7bb76961208_1816x676.png)
*来源：SemiAnalysis、Google*

Trillium 也是最后一款「E」（lite）SKU，这意味着它只配备 2 个 HBM3 位宽位（sites）。Trillium 在计算上追平了 Hopper，但在内存容量和带宽上远不及 H100/H200——只有 2 组 HBM3 堆叠，而 H100 与 H200 分别有 5 组 HBM3 和 6 组 HBM3E 堆叠。这让新手用起来非常痛苦，但如果你能把模型分片（shard）得当、把这些廉价 FLOPS 全部用满，Trillium 的性能 TCO 无出其右。

![](https://substack-post-media.s3.amazonaws.com/public/images/b39d7d10-8169-4ce5-99ab-4c35de4e78d2_1536x784.png)
*来源：SemiAnalysis*

TPU v7 Ironwood 是下一步迭代，Google 在 FLOPs、内存和带宽上几乎完全追平对应的 Nvidia 旗舰 GPU，只是全面上市（GA）比 Blackwell 晚一年。与 GB200 相比，FLOPs 和内存带宽仅有微小差距，容量则持平（都是 8-Hi HBM3E）；当然，相比配备 288GB 12-Hi HBM3E 的 GB300，差距仍然明显。

![](https://substack-post-media.s3.amazonaws.com/public/images/b1c9096c-e855-47e2-ae5b-7f74f1f00dc1_1334x784.png)
*来源：SemiAnalysis*

理论绝对性能是一回事，真正重要的是**每总拥有成本（TCO）的真实世界性能**。

虽然 Google 通过 Broadcom 采购 TPU 并支付可观的利润加成，但这远低于 Nvidia 的利润率——Nvidia 赚的不只是 GPU，还包括 CPU、交换机、NIC、系统内存、线缆和连接器在内的整个系统。从 Google 的视角看，完整 3D Torus 配置下每颗 Ironwood 芯片的全包 TCO 比 GB200 服务器低约 44%。

这足以弥补峰值 FLOPs 和峰值内存带宽约 10% 的差距。以上是从 Google 视角、按其采购 TPU 服务器的价格计算。

![](https://substack-post-media.s3.amazonaws.com/public/images/d73646cf-f488-48aa-b5d9-9eb94561c325_1819x904.png)
*来源：SemiAnalysis AI TCO 模型*

那么，当 Google 在此之上叠加自己的利润后，外部客户的情况如何？我们假设在 Google 向外部客户出租 TPU v7 并赚取利润的情形下，每小时 TCO 仍可低至比 GB200 便宜约 30%、比 GB300 便宜约 41%。我们认为这正反映了 Anthropic 通过 GCP 拿到的价格水平。

![](https://substack-post-media.s3.amazonaws.com/public/images/009c184d-569e-4ab4-85d2-2fe616cbe3c2_1650x796.png)
*来源：SemiAnalysis AI TCO 模型*

# Anthropic 为什么押注 TPU

只比理论 FLOPs 只说清了故事的一半。真正重要的是有效 FLOPs（effective FLOPs），因为现实工作负载几乎从达不到峰值。

实践中，一旦计入通信开销、内存停顿（memory stall）、功耗限制等系统效应，Nvidia GPU 通常只能达到理论峰值的一小部分。训练场景的经验法则约是 30%，但**利用率随工作负载差异极大**。差距的很大一部分来自软件与编译器效率。Nvidia 的优势源于 CUDA 护城河和开箱即用的大量开源库，帮助工作负载高效运行，实现高企的 FLOPs 与内存带宽利用率。

TPU 软件栈用起来没那么容易，不过这一局面正开始改变。在 Google 内部，TPU 受益于优秀但不对外开放的内部工具链，这使其开箱即用的性能对外部客户而言偏弱。然而，这只影响小型或懒惰的用户——Anthropic 两者都不是。

Anthropic 拥有强大的工程资源和前 Google 编译器专家，既熟悉 TPU 技术栈，又深刻理解自家模型架构。他们有能力投入定制 kernel 以驱动高 TPU 效率，从而实现大幅更高的模型 FLOP 利用率（MFU）和好得多的 $/PFLOP 表现。

我们认为，尽管宣传的峰值 FLOPs 更低，**TPU 实际能达到的模型 FLOP 利用率（MFU）可以高于 Blackwell**，这意味着 Ironwood 的有效 FLOPs 更高。一个重要原因是 Nvidia 和 AMD 宣传的 GPU FLOPs 明显虚高。即便在为最大化吞吐而设计、GEMM 形状远偏离真实负载的测试中，Hopper 也只达到峰值的约 80%，Blackwell 落在 70 出头，而 [AMD 的 MI300 系列在 50-60 区间](https://newsletter.semianalysis.com/p/h100-vs-gb200-nvl72-training-benchmarks)。

限制因素在于供电。这些芯片无法持续维持用于峰值计算的时钟频率。Nvidia 和 AMD 实施了动态电压频率调节（DVFS），即芯片的时钟频率根据功耗和温度动态调整，而不是锁定在一个实际可持续的稳定频率。而 Nvidia 和 AMD 会选取哪怕只是偶尔才能达到的最高时钟频率，用来计算峰值理论 FLOPS（每 ALU 每周期操作数 × ALU 数量 × 每秒周期数，即时钟频率）。

还有其他手法，比如用填满零的张量跑 GEMM：由于 0x0=0，晶体管无需在 0 和 1 之间切换状态，从而降低每次操作的功耗。当然，现实世界里没有人把全零张量相乘。

把低得多的 TCO 与更高的有效 FLOPs 利用率结合起来看，从 Google 的视角，每有效 FLOP 的成本便宜得多——TPU 约 15% 的 MFU 即可与 30% MFU 的 GB300 打平。也就是说，即便 Google（或 Anthropic）只达到 GB300 一半的 FLOPs 利用率，也仍能持平。当然，凭借 Google 顶尖的编译器工程团队和对自家模型的深刻理解，他们在 TPU 上实现的 MFU 有望达到 40%。那相当于每有效训练 FLOP 的成本大降约 62%！

![](https://substack-post-media.s3.amazonaws.com/public/images/361a49dc-a7e6-4834-a0b7-b61ba0be092c_1946x940.png)
*来源：SemiAnalysis AI TCO 模型*

不过，看那 60 万颗租用的 TPU 时，把 Anthropic 支付的更高 TCO（即包含 Google 叠加的利润）纳入分析，我们估计 Anthropic 从 GCP 租用 TPU 的成本为每 TPU 小时 1.60 美元，TCO 优势相应收窄。我们相信 Anthropic 能在 TPU 上实现 40% 的 MFU，这既得益于其对性能优化的专注，也因为 TPU 宣传的 FLOPs 本身更贴近现实。这使得 Anthropic 每有效 PFLOP 的 TCO 相比 GB300 NVL72 低约 52%，十分惊人。相对 GB300 基线、每有效 FLOP 的 TCO 打平时的均衡点，对 Anthropic 而言低至 19% 的实际 MFU。这意味着，Anthropic 即便相对 GB300 基线出现相当大的性能损失，训练 FLOPs 的 perf/TCO 仍能和 Nvidia 基线系统持平。

![](https://substack-post-media.s3.amazonaws.com/public/images/ff2d4087-0bd0-4e35-8710-eb9603dc914e_1556x830.png)
*来源：SemiAnalysis*

FLOPs 并非性能的全部，内存带宽对推理至关重要，尤其是在带宽密集的解码（decode）阶段。TPU 的每内存带宽成本也远低于 GB300，这一点毫不意外。有充分证据表明，在小消息尺寸（如 16MB 到 64MB，即加载单层的一个专家）场景下，TPU 甚至能取得比 GPU 更高的内存带宽利用率。

![](https://substack-post-media.s3.amazonaws.com/public/images/c4dd452f-da8a-4e3c-b522-26527097f0e1_1728x834.png)
*来源：SemiAnalysis AI TCO 模型*

所有这些都转化为训练和服务模型更高效的算力。Anthropic 发布的 Opus 4.5 延续了一贯的编码主打，创下 SWE-Bench 新纪录。最大的意外是 API 价格下调约 67%。配合该模型相对 Sonnet 更低的冗余度和更高的 token 效率（达到 Sonnet 最佳分数所需的 token 少 76%，超出其 4 分所需的 token 少 45%），Opus 4.5 成为编码用例的最佳模型，而且实际上可能抬高 Anthropic 的已实现 token 定价——因为 Sonnet 目前占其 token 结构的 90% 以上。

![](https://substack-post-media.s3.amazonaws.com/public/images/403047d3-3008-4a21-9e7e-a00df6a9b691_2362x1180.png)
*来源：SemiAnalysis Tokenomics 模型、Anthropic，数据截至 11/24/25*
![](https://substack-post-media.s3.amazonaws.com/public/images/18de9b63-a5ea-4161-9693-962d6aed6561_3397x1653.png)
*来源：Anthropic 与 SemiAnalysis Tokenomics 模型，50:1 ISL:OSL*

# Google 在利润率上走钢丝

在对外定价上，Google 需要走钢丝：既要保住自身盈利能力，又要给客户提供有竞争力的方案。我们对 Anthropic 定价的估计，处于我们听说的外部定价区间的低端。对 Anthropic 这样的旗舰客户——既能为软件和硬件路线图提供宝贵输入，又下单量巨大——我们预期会有优惠价（sweetheart pricing）。虽然 Nvidia 骇人的 4 倍加价（约 75% 毛利率）为定价灵活性留出很大空间，但相当一部分空间被 Broadcom 吸走了。Broadcom 作为 TPU 的协同设计方，在占系统物料清单（BOM）最大头的硅片上赚取高利润。尽管如此，Google 仍有充足空间赚取非常可观的利润率。

把 GCP-Anthropic 交易与我们观察到的其他大型 GPU 云交易对比即可看出。注意，这里分析的是租用的 60 万颗 TPU，其余 40 万颗 TPU v7 芯片由 Anthropic 预先买断。

在这些假设下，TPU v7 的经济性显示出比我们观察过的其他大型 GPU 云交易更优的 EBIT 利润率，只有 OCI-OpenAI 勉强接近。即便有 Broadcom 在芯片级 BOM 上的利润叠加，Google 仍能挤出远优于高度同质化 GPU 交易的利润率和回报。这正是 TPU 技术栈让 GCP 成为真正差异化 CSP 的地方。[而像 Microsoft Azure 这样自研 ASIC 项目举步维艰的厂商，则只能困于「租赁商用硬件」这门平庸生意、赚取平庸回报。](https://newsletter.semianalysis.com/i/178649945/other-asic-programs-vs-microsoft)

![](https://substack-post-media.s3.amazonaws.com/public/images/5276c013-7a03-43cd-b01b-7bc5ffd3d53f_2314x598.png)
*来源：SemiAnalysis*

# TPU 系统与网络架构

到目前为止，我们把 TPU 与 Nvidia GPU 的对比集中在单芯片规格与短板上。现在回到系统层面的讨论——那才是 TPU 能力真正开始拉开差距的地方。TPU 最鲜明的特性之一，是通过 ICI 协议实现的超大纵向扩展（scale-up）world size（可联成一体的芯片规模）。一个 TPU pod 的 world size 可达 9216 颗 Ironwood TPU，而大 pod 尺寸早在 2017 年的 TPUv2 时代就是 TPU 的特色，当时就能扩展到完整 256 颗乃至 1024 颗芯片的集群规模。让我们从机柜层面开始——它是每个 TPU superpod 的基本构建单元。

# Ironwood 机柜架构

![](https://substack-post-media.s3.amazonaws.com/public/images/98f1262a-ca61-47ee-9a1e-b58d4cb4a277_1439x813.png)
*来源：Google 于 Hot Chips 2025*
![](https://substack-post-media.s3.amazonaws.com/public/images/1a3b19e5-8159-4d64-8345-5ef508f382cd_2818x1587.png)
*来源：Google 于 Hot Chips 2025*

过去几代 TPU 机柜设计大同小异。每个机柜由 16 个 TPU 托盘（tray）、16 或 8 个主机 CPU 托盘（视散热配置而定）、一台 ToR 交换机、电源单元以及电池备份单元（BBU）组成。

![](https://substack-post-media.s3.amazonaws.com/public/images/5881ed93-4ea2-4447-8fe3-a611f6f03abb_793x1143.png)
*来源：SemiAnalysis*

每个 TPU 托盘包含 1 块 TPU 板，板上安装 4 个 TPU 芯片封装。每颗 Ironwood TPU 将有 4 个用于 ICI 连接的 OSFP 笼子（cage）和 1 个用于连接主机 CPU 的 CDFP PCIe 笼子。

![](https://substack-post-media.s3.amazonaws.com/public/images/5e62de47-9252-4c5b-b221-49581764b9d0_788x917.png)
*来源：SemiAnalysis*
![](https://substack-post-media.s3.amazonaws.com/public/images/3346625c-6b2b-4335-8467-6a109fb64ace_1478x1288.png)
*来源：Google*

Google 从 2018 年的 TPU v3 起就部署液冷 TPU 机柜，但中间也有几代 TPU 是按风冷设计的。液冷与风冷机柜的主要区别在于：风冷机柜的 TPU 托盘与主机 CPU 托盘之比为 2:1，而液冷机柜为 1:1。

![](https://substack-post-media.s3.amazonaws.com/public/images/faf8d0b1-f36c-456a-ab5b-34a4c8f30e40_744x900.png)
*来源：SemiAnalysis、Google*

TPU 液冷的一个创新设计是冷却液流量由阀门主动控制。这样冷却效率更高，因为流量可以根据每颗芯片任意时刻的负载多少来调节。Google TPU 也早已采用垂直供电（vertical power delivery），TPU 的电压调节模块（VRM）位于 PCB 板的另一侧。这些 VRM 模块同样需要冷板散热。

总体而言，TPU 机柜设计比 Nvidia Oberon NVL72 简单得多，后者密度高得多，并利用背板（backplane）将 GPU 连接到纵向扩展交换机。TPU 托盘之间的纵向扩展连接全部通过外部铜缆或光模块完成，这将在下文 ICI 一节详述。TPU 托盘与 CPU 托盘之间也通过 PCIe DAC 线缆连接。

# 片间互连（ICI）——扩展纵向扩展 world size 的关键

TPUv7 的 Google ICI 纵向扩展网络的基本构建单元，是由 64 颗 TPU 组成的 4x4x4 3D 环面（3D torus）。每个由 64 颗 TPU 构成的 4x4x4 立方体对应一个容纳 64 颗 TPU 的物理机柜。这是理想维度，因为全部 64 颗 TPU 可以彼此以电气方式连接，并且恰好装进一个物理机柜。

![](https://substack-post-media.s3.amazonaws.com/public/images/0de048fb-89a6-4865-8ff7-dbcbb7d2cda9_1740x2338.png)
*来源：Google、SemiAnalysis*

这些 TPU 以 3D 环面拓扑相互连接，每颗 TPU 总共连接 6 个邻居——X、Y、Z 每个轴各 2 个*逻辑上*相邻的 TPU。

每颗 TPU 总是通过计算托盘内的 PCB 走线与其他 2 颗 TPU 相连；而其余 4 个邻居的连接方式取决于该 TPU 在 4x4x4 立方体中的位置——或通过直接附着铜缆（DAC），或通过光收发器。

4x4x4 立方体内部的连接走铜，而立方体外部的连接（包括绕回立方体另一侧的环绕连接，以及与相邻 4x4x4 立方体的连接）则使用光收发器和 OCS。在下图中可以看到，由于这是 3D 环面网络：位于 Z+ 面的 TPU 2,3,4 通过一个 800G 光收发器并经 OCS 路由，与 Z 轴对面 Z- 面上的 TPU 2,3,1 建立环绕连接。

![](https://substack-post-media.s3.amazonaws.com/public/images/e0428839-ac3f-4ffc-923a-48295d2b9b19_2074x2144.png)
*来源：Google、SemiAnalysis*

如上所述，除了始终通过 PCB 走线相连的 2 个邻居 TPU 之外，每颗 TPU 还会根据其在 4x4x4 立方体中的位置，使用 DAC、光收发器或两者混用来连接另外 4 个邻居。

位于立方体内部的 TPU 完全通过 DAC 连接其余 4 个邻居；位于面上的 TPU 通过 3 条 DAC 和 1 个光收发器连接；位于棱上的 TPU 通过 2 个光收发器和 2 条 DAC 连接；而位于角上的 TPU 通过 1 条 DAC 和 3 个光收发器连接。判断某颗 TPU 会用多少个光收发器的窍门：数一数它有几个面朝向立方体的「外侧」。

![](https://substack-post-media.s3.amazonaws.com/public/images/0fd47a1d-3376-47a7-81c7-464e09a3909c_1302x1153.png)
*来源：SemiAnalysis*

上图与下表汇总了各类位置类型的 TPU 数量，可据此推导出 TPU v7 每颗 1.5 个光收发器的配比（attach ratio）。这些收发器连接到光路交换机（OCS），实现 4x4x4 立方体之间的互连——下一节详述。

![](https://substack-post-media.s3.amazonaws.com/public/images/68c6923d-2032-4c7d-b630-0adb7ac4a272_710x787.png)
*来源：SemiAnalysis、Google*

# ICI 的光学部分

Google 采用软件定义网络的方法，通过光路交换机（OCS）管理网络路由。一台 NxN 的 OCS 基本上就是一座[巨大的火车站](https://newsletter.semianalysis.com/p/google-apollo-the-3-billion-game)，N 条轨道进、N 条轨道出。任何进站的火车都可以被转到任何一条出站轨道，但这必须在车站内重新配置。火车不能「折返」、也不能被送回另一条进站轨道，只能被路由到 N 条出站轨道之一。

这种方法的好处是，网络可以在 ICI 网络层理论最大值 9,216 颗芯片之中，为不同工作负载组装出更小的逻辑 TPU 切片（slice）。通过对更大集群进行切片、让 ICI 路径绕开网络中的故障点，集群可用性得以提升。

与 Arista Tomahawk 5 这类电分组交换机（EPS）不同——EPS 的总带宽固定、再被拆分为若干较小带宽的端口——OCS 允许任意带宽的光纤接入其端口。OCS 的延迟也比 EPS 低，因为进入 OCS 的光信号只是简单地从输入端口反射到输出端口；而对 EPS 来说，光信号进入交换机时必须转换为电信号——这也是 OCS 通常比 EPS 更省电的关键原因之一。EPS 允许数据包从任意端口路由到任意端口，而 OCS 只允许把一个「入」端口路由到任意一个「出」端口。

![](https://substack-post-media.s3.amazonaws.com/public/images/54289801-5e75-445f-96ef-bb9443981ff4_1653x990.png)
*来源：Google*

OCS 端口只路由单独的光纤纤芯（strand）。这对标准双工（duplex）收发器是个挑战，因为带宽是在多根纤芯上传输的，这会降低 OCS 的有效端口数（radix）和带宽。为解决这一问题，需要使用 FR 光收发器，把所有波长汇聚到单根纤芯上、接入 1 个 OCS 端口。Apollo 项目分两步创新地实现了这一点：第一步，8 个波长——每条 100G 通道各占 1 个波长——通过粗波分复用（CWDM8）复用后，在单对光纤上传输 800G，而不是 8 对光纤；第二步，在波分复用（WDM）收发器上集成光环行器（optical circulator），实现全双工数据流，把需求从 1 对光纤进一步降到只有 1 根纤芯。

![](https://substack-post-media.s3.amazonaws.com/public/images/bb691eff-342c-4935-aef3-0ec7ae616fae_1610x896.png)
*来源：Google*

环行器把收发器端的发送（Tx）与接收（Rx）纤芯合并到单根纤芯上送往 OCS 交换机，从而形成双向链路。

![](https://substack-post-media.s3.amazonaws.com/public/images/22aa3bbe-7152-4dcb-aef3-4e203a942918_1581x473.png)
*来源：Google*

# 将众多 64 颗 TPU 的立方体连接起来

Google 的 ICI 纵向扩展网络的独特之处在于，它允许多个 64 颗 TPU 的 4x4x4 立方体以 3D 环面配置相连，构成超大规模的 world size。TPUv7 官方最大 world size 为 9,216 颗 TPU，但如今 Google 支持把 TPU 配置成多种不同的切片尺寸，从 4 颗 TPU 一直到 2,048 颗 TPU。

![](https://substack-post-media.s3.amazonaws.com/public/images/9f178eb8-54c3-4944-836e-fcf8140436b0_3571x2394.png)
*来源：Google*

尽管 Google 能够创新地实现 9,216 颗 TPU 这一令人印象深刻的纵向扩展集群，但在越来越大的分块（block size）——最高约 8,000 颗 TPU——上运行训练工作负载，其边际收益是递减的。因为分块越大，越容易发生故障与中断，从而降低切片可用性（slice availability）——其定义为 ICI 集群能够维持一个连续 3D 环面切片的时间占比。

![](https://substack-post-media.s3.amazonaws.com/public/images/7601089c-f8bd-41e6-99bc-f80041ff6cad_1159x740.png)
*来源：Google*

对于能完全容纳在单个 4x4x4 立方体内的切片，我们可以直接从该立方体中切出：使用机柜内的铜互连，必要时再借助立方体面/棱/角上的光收发器环绕连接，补全 3D 环面。

要理解环绕与立方体间连接如何建立，先看如何在 4x4x4 拓扑中创建一个 64 颗 TPU 的切片。我们可以用对应一个 64 颗 TPU 物理机柜的 4x4x4 单元立方体来搭建这一拓扑。4x4x4 立方体内部的全部 8 颗 TPU 可以用铜 fully 连接全部 6 个邻居。如果某颗 TPU 在给定轴向上没有内部邻居，它就会环绕连接到立方体对面的 TPU。例如，TPU 4,1,4 在 Z+ 方向没有内部邻居，于是它用 1 个 800G 光收发器连接到一台分配给 Z 轴的 OCS，由该 OCS 把这条连接引到立方体的 Z- 侧，连到 TPU 4,1,1。在 Y- 方向，TPU 1,1,1 会用光收发器连接 Y 轴 OCS，链到 TPU 1,4,1 的 Y+ 侧，依此类推。

![](https://substack-post-media.s3.amazonaws.com/public/images/00598db9-454f-4788-b769-7994f4089016_1212x1176.png)
*来源：SemiAnalysis、Google*

4x4x4 立方体的每个面通过 16 台不同的 OCS 连接——面上每颗 TPU 对应一台 OCS。

例如，在下图中，X+ 面上的 TPU 4,3,2 连接到 OCS X,3,2 的输入侧。OCS X,3,2 的输入侧还将连接 9,216 颗 TPU 集群中全部 144 个 4x4x4 立方体 X+ 面上相同 TPU 编号（4,3,2）的芯片。OCS X,3,2 的输出侧则连接集群中每个立方体相同 TPU 编号的 X- 面——也就是连接全部 144 个立方体上的 TPU 1,3,2。下图展示了立方体 A 的 X+ 面上全部 16 颗 TPU 如何通过 16 台 OCS 连接到立方体 B X- 面上的 16 颗 TPU。

这些连接允许任意立方体的任意「+」面连接到任意其他立方体的「-」面，使立方体在组建切片时完全可互换（fungible）。

有两个约束需要简单指出。第一，给定面上某一编号的 TPU 永远不能直接连接到不同的编号——所以 TPU 4,3,2 永远不会被配置为连接 TPU 1,2,3。第二，由于 OCS 本质上像一块配线板（patch panel）——连接在其输入侧的 TPU 不能「折返」去连接同样接在该 OCS 输入侧的其他 TPU——例如 TPU 4,3,2 永远不能连接 TPU 4,3,3。因此，任意「+」面上的 TPU 永远无法连接到其他任何立方体的「+」面，任意「-」面上的 TPU 也永远无法连接到其他任何立方体的「-」面。

![](https://substack-post-media.s3.amazonaws.com/public/images/961039f5-7304-4448-8ec3-354ba95581f2_2245x1261.png)
*来源：SemiAnalysis、Google*

让我们把规模放大，看看 4x4x8 拓扑如何搭建。在这种配置中，我们沿 Z 轴把两个 64 颗 TPU 的 4x4x4 立方体连接起来以扩展切片。此时，OCS 会重新配置 TPU 4,1,4 所连接的光端口，使其连接到 TPU 4,1,5，而不是像独立 4x4x4 拓扑那样环绕回 TPU 4,1,1。以此类推，两个 4x4x4 TPU 立方体的 Z- 面和 Z+ 面各伸出 16 条光连接，共 64 根纤芯接入 16 台 Z 轴 OCS。

需要提醒读者的是，下图所示的立方体 A 和立方体 B 未必物理相邻。它们通过 OCS 连接，各自可能位于数据中心内完全不同的位置。

![](https://substack-post-media.s3.amazonaws.com/public/images/e9ae9e2f-9d75-42af-b823-208452482bc8_2932x2196.png)
*来源：SemiAnalysis、Google*

现在转向一个大得多的拓扑——16x16x16 拓扑，它把我们带到 4,096 颗 TPU。在这个拓扑中，我们总共使用 48 台 OCS 连接 64 个各含 64 颗 TPU 的立方体。下图中，每个彩色立方体代表一个 64 颗 TPU 的 4x4x4 立方体。以右下角的 4x4x4 立方体为例——该立方体通过 OCS 沿 Y 轴与相邻立方体相连。

9,216 颗 TPU 的最大 world size 由 144 个 4x4x4 立方体构成，每个立方体需要 96 条光连接，总计 13,824 个端口需求。用这一总端口需求除以 288（每台 OCS 上 144 个输入端口与 144 个输出端口），意味着我们需要 48 台 144x144 的 OCS 来支撑这一最大 world size。

![](https://substack-post-media.s3.amazonaws.com/public/images/427d34ea-5af3-45f5-ad19-d5b8070f0650_1560x1375.png)

# 为什么要用 Google 的 ICI 3D 环面架构？

除了那些能让人画上无数小时的漂亮立方体示意图之外，Google 独特的 ICI 纵向扩展网络到底好在哪？

**超大的 world size：** 最直观的好处是 TPUv7 Ironwood 支持高达 9,216 颗 TPU 的最大 world size。虽然由于有效吞吐（goodput）下降的弊端，9,216 的最大切片尺寸可能很少被用到，但数千颗 TPU 规模的切片可以且经常被使用。这远超商用加速器市场和其他定制芯片供应商常见的 64 或 72 颗 GPU 的 world size。

**可重构与可互换：** OCS 的使用意味着网络拓扑天然支持重新配置网络连接，以支持大量不同的拓扑——理论上可达数千种。Google 的文档站点列出了 10 种组合（见本节前面的插图），但这些只是最常见的 3D 切片形状——可用的远不止这些。

即便尺寸相同的切片，也可以有不同的重构方式。在下图这个简化的扭曲 2D 环面（Twisted 2D Torus）示例中，我们可以看到：环回连接时改接不同 X 坐标的编号、而不是相同 X 坐标的编号，可以减少最坏情况下的跳数、并改善最坏情况下的二分带宽。这有助于提升 all-to-all 集合通信的吞吐量。TPUv7 集群将在 4x4x4 立方体层面进行扭曲。

![](https://substack-post-media.s3.amazonaws.com/public/images/988dfb38-b5ba-43c3-9e2e-f8f7e79d1291_3868x1582.png)
*来源：SemiAnalysis、Google*

可重构性还为多样化的并行策略打开了大门。在 64 或 72 颗 GPU 的 world size 中，不同的并行组合通常被限制为 64 的因子。而在 ICI 纵向扩展网络中，可实现的拓扑组合极其丰富，能够精确匹配所期望的数据并行、张量并行与流水线并行组合。

OCS 允许把任意立方体的任意「+」面连接到其他任意立方体的「-」面，这意味着立方体完全可互换。切片可以从任意一组立方体中组建。因此，即便出现故障、或用户需求与用量发生变化，也不会阻碍新拓扑切片的组建。

![](https://substack-post-media.s3.amazonaws.com/public/images/5e48f64b-a36b-446b-b9cb-bc051862329d_962x675.png)
*来源：Google*

**更低的成本：** Google 的 ICI 网络比大多数基于交换机的纵向扩展网络成本更低。虽然所用的 FR 光模块因使用环行器而略显昂贵，但网状（mesh）网络减少了所需的交换机与端口总数，并消除了交换机之间互连的成本。

![](https://substack-post-media.s3.amazonaws.com/public/images/77d42a55-42e4-4788-843e-cfc50c720fb0_2054x942.png)
*来源：SemiAnalysis*

**低延迟与更好的局部性：** TPU 之间采用直连链路，意味着对于物理上彼此邻近、或被重构为直接相连的 TPU，可以获得低得多的延迟。彼此邻近的 TPU 也拥有更好的数据局部性（data locality）。

# 数据中心网络（DCN）——扩展超越 9,216 颗 TPU

数据中心网络（DCN）是独立于 ICI 的另一张网络，同时承担典型的后端网络与前端网络角色。它连接的域更大——TPUv7 集群下可达 147k 颗 TPU。

正如我们此前关于 Mission Apollo 的文章所述——[Google 提出用 Paloma 光路交换机（OCS）取代传统「Clos」架构中采用电分组交换机（EPS）的骨干层（spine）](https://newsletter.semianalysis.com/p/google-apollo-the-3-billion-game)——Google 的 DCN 由一个光交换的数据中心网络互连（DCNI）层组成，该层把多个聚合块（aggregation block）连为一体，每个聚合块又连接多个 9,216 颗 TPU 的 ICI 集群。

2022 年，Google 的 Apollo 项目提出了一种 DCN 架构，为 pod 尺寸 4,096 颗 TPU 的 TPUv4 pod 描述了使用 136x136 OCS 交换机的方案。DCNI 层的 OCS 交换机组织为 4 个 Apollo 区（zone），每区最多 8 个机柜、每柜 8 台 OCS 交换机，共计 256 台 OCS 交换机。到了 Ironwood，为了在同一张网络上支持多达 147k 颗 TPUv7，我们推测 OCS 的端口数将近乎翻倍，而不是增加 OCS 交换机的最大数量。

下图展示了使用 32 个机柜、容纳 256 台 300x300 OCS 交换机的 Ironwood DCN 网络可能的样子。假设各聚合块的骨干层之间不存在收敛比（oversubscription），DCN 中最多可连接 16 个 ICI pod，由 4 个聚合块各连接 4 个 ICI pod——总计 147,456 颗 TPU。

DCNI 层把这 4 个聚合块连接起来——即下图中画在最顶上的一层。与 ICI 一样，连接 OCS 时使用 FR 光模块，以最大化每台 OCS 每个端口的带宽。

![](https://substack-post-media.s3.amazonaws.com/public/images/526d2520-9342-492d-a4c5-98b0db6122ad_1341x1108.png)
*来源：SemiAnalysis*

虽然现有 Ironwood 集群可能只有 1 或 2 个聚合块，但 Google DCN 的独特架构允许在无需大规模重新布线的情况下，向网络添加新的 TPU 聚合块。

通过在 DCNI 层使用 OCS，DCN fabric 的规模可以增量扩展，网络也可以重新条带化（re-stripe）以支持新的聚合块。此外，聚合块的带宽可以在不改变 DCN 层构成的情况下升级。这意味着现有聚合块的链路速率可以刷新，而无需改动网络本身的根本架构。当然，fabric 扩容的过程不能无限持续——规模一大，重新布线就变得难以管理。

![](https://substack-post-media.s3.amazonaws.com/public/images/fd069c23-c468-41cf-9ece-2f8cf8f5efb0_1965x726.png)
*来源：SemiAnalysis、Google*

# TPU 软件战略——又一次重大转变

传统上，TPU 的软件和硬件团队只面向内部。这带来一些好处，比如不会有市场部门施压、要求夸大宣传的理论 FLOPS。

只面向内部的另一个好处是，TPU 团队高度优先满足内部功能需求、优化内部工作负载；坏处则是他们不太在乎外部客户和工作负载。TPU 生态中外部开发者的数量远低于 CUDA 生态。这是 TPU 的主要弱点之一——所有非 Nvidia 加速器莫不如此。

此后 Google 修订了面向外部客户的软件战略，并已对 TPU 团队的 KPI 及其参与 AI/ML 生态的方式做出重大调整。我们将讨论两大变化：

1. 大规模投入 PyTorch TPU「原生（native）」支持
2. 大规模投入 vLLM/SGLang TPU 支持

从 Google 在各 TPU 软件仓库的提交数量上，可以清楚看到外销战略。我们看到 3 月起 vLLM 的贡献明显增加。随后 5 月创建了「tpu-inference」仓库——这是官方的 vLLM TPU 统一后端——此后活动密集涌现。

![](https://substack-post-media.s3.amazonaws.com/public/images/81b1cccf-0ee8-4833-b308-d65cd26bf111_1360x836.png)
*来源：GitHub、SemiAnalysis*

传统上，Google 只在 JAX/XLA:TPU 技术栈（以及 TensorFlow/TF-Mesh，RIP）上提供一等支持，而把 TPU 上的 PyTorch 当作二等公民。它依赖通过 PyTorch/XLA 进行惰性张量图捕获（lazy tensor graph capture），而非一等公民式的即时执行（eager execution）模式。此外，它既不支持 PyTorch 原生分布式 API（torch.distributed.*），也不支持 PyTorch 原生并行 API（DTensor、FSDP2、DDP 等），而是依赖树外（out of tree）的奇怪 XLA SPMD API（torch_xla.experimental.spmd_fsdp、torch_xla.distributed.spmd 等）。对于习惯了 GPU 上原生 PyTorch CUDA 后端、想要切换到 TPU 的外部用户来说，这带来了一种非原生的糟糕体验。

![](https://substack-post-media.s3.amazonaws.com/public/images/1f026b79-68bc-421f-9667-f332cbf63fec_1446x1012.png)
*来源：XLA*

10 月，Google 的「Captain Awesome」Robert Hundt 在 XLA 仓库悄然宣布，他们将放弃非原生的惰性张量后端，转向一个「原生」TPU PyTorch 后端：默认支持即时执行，并集成 torch.compile、DTensor、torch.distributed API 等。他们将借助 PrivateUse1 TorchDispatch key 来实现。这项工作主要是为 Meta 做的——Meta 重新萌生了购买 TPU 的兴趣、且不想迁移到 JAX。这也会让喜欢 PyTorch、不喜欢 JAX 的人用上 TPU。

此前 2020 到 2023 年间，Meta FAIR 的几个团队曾在 TPU 上大量使用 PyTorch XLA，但采用面不广，Meta 管理层最终于 2023 年取消了合同。TPU 上的 PyTorch XLA 体验并不愉快。当年 Meta FAIR 在 GCP 上的 TPU 甚至是用 SLURM 跑的，而不是 TPU 技术栈上常见的 GKE/Xmanager/borg 等。

![](https://substack-post-media.s3.amazonaws.com/public/images/db66dc94-a7f3-4fc4-a26d-fedace388034_1834x880.png)
*来源：GitHub*

这个新的 PyTorch <> TPU 将为习惯在 GPU 上使用 PyTorch 的 ML 科学家铺平切换到 TPU 上 PyTorch 的过渡之路，并享受 TPU 上更高的每 TCO 性能。

Pallas 是为 TPU 编写定制 kernel 的 kernel 编写语言（类似 cuTile、Triton 或 CuTe-DSL）。Meta 和 Google 还已开始支持把 Pallas kernel 作为 Torch Dynamo/Inductor 编译栈的代码生成（codegen）目标。这将实现 TPU 与 PyTorch 原生 torch.compile API 的原生集成，并允许最终用户把定制 Pallas 算子注册进 PyTorch。

![](https://substack-post-media.s3.amazonaws.com/public/images/71b36c94-fe57-4209-9a8d-7f2586eb4de4_2498x1094.png)
*来源：GitHub*

除了树内（in-tree）的核心 PyTorch 原生 API 之外，幕后还在进行把 TPU Pallas kernel 语言集成为 Helion 代码生成目标的工作。可以把 Helion 理解成一种用高级语言编写性能尚可 kernel 的高级语言。由于其形态与 PyTorch 原生 Aten 算子相似得多，用户应把 Helion 当作更底层的 Aten 算子，而非高层的 Triton/Pallas。

![](https://substack-post-media.s3.amazonaws.com/public/images/86f84fa9-784b-4604-be30-22c1c0c3565a_2546x1238.png)
*来源：PyTorch Foundation*
![](https://substack-post-media.s3.amazonaws.com/public/images/f1ab788f-8f2d-48bd-8783-1f11e8d26e24_1551x867.png)
*来源：PyTorch Mark Saroufim*

CUDA 生态称霸的另一个领域是开放生态推理。历史上，vLLM 与 SGLang 把 CUDA 当作一等公民支持（ROCm 算二等公民）。如今 Google 想进入 vLLM 与 SGLang 的开放推理生态，并已宣布通过一种非常「独特」的集成方式，为 vLLM 与 SGLang 提供 beta 版 TPU v5p/v6e 支持。

![](https://substack-post-media.s3.amazonaws.com/public/images/49d70e03-8d5e-41b1-930e-7137fa71d3bb_1860x720.png)
*来源：vLLM*

目前 vLLM 与 SGLang 的做法，是把 PyTorch 建模代码下层（lowering）为 JAX，并利用现有成熟的 JAX TPU 编译流程。未来一旦 PyTorch XLA RFC #9684（即原生 TPU PyTorch 后端）落地，vLLM 与 SGLang 计划评估是否改用它，从而不再通过 TorchAX 把模型从 PyTorch 翻译成 JAX。

Google 与 vLLM 声称这条下层到 JAX 的路径不需要修改任何 PyTorch 建模代码，但考虑到 vLLM TPU 目前支持的模型还那么少，我们对此表示怀疑。

此外，Google 已经开源并将其部分 TPU kernel 集成进 vLLM，例如 TPU 优化的分页注意力（paged attention）kernel、计算与通信重叠（overlap）的 GEMM kernel，以及另外几个量化 matmul kernel。他们还没有对 MLA 友好的 TPU kernel。等 Inductor 的 Pallas TPU 代码生成集成更成熟后，看看能否把 kernel 融合与模式匹配集成进现有 vLLM PassManager，会很有意思。[SGLang 也在研究实现 torch.compile PassManager](https://github.com/sgl-project/sglang/issues/10118)，以便让众多模型的 kernel 融合管理更可维护。

至于 Ragged Paged Attention v3，TPU 的处理方式与 vLLM GPU 大不相同。vLLM 用类似虚拟内存与分页的技术管理 KV 缓存。但这一技术需要取动态地址并执行 scatter 操作——TPU 并不擅长。因此，TPU kernel 利用细粒度的操作流水线（pipelining）。具体来说，TPU 的 page attention kernel 会为下一个序列预取 query 和 KV 块，使内存加载与计算重叠。

在现有的 vLLM MoE kernel 中，我们先按专家 ID 对 token 排序，把 token 分发到持有对应专家的设备，执行分组矩阵乘法，再把各专家的 token 合并回原设备。但该 kernel 性能不佳，原因有二：TPU 执行排序操作很慢，而且 kernel 无法让通信与计算重叠。

为绕开这个问题，Google 开发者设计了 all-fused MoE。all-fused MoE 每次向每台设备分发一个专家的 token，同时让 MoE 分发与 MoE 合并的通信相互重叠，并避免按专家 ID 对 token 排序。Google 工程师报告，all-fused MoE 相对现有 kernel 取得了 3-4 倍加速。

![](https://substack-post-media.s3.amazonaws.com/public/images/2596f93b-0483-486e-8be6-6b5c38432030_1312x2706.png)
*来源：SemiAnalysis*

另外，TPU 中还有一个名为 SparseCore（SC）的硬件单元，用于加速嵌入（embedding）查表与更新。SC 配备一个标量子核 SparseCore Sequencer（SCS）和多个向量子核 SparseCore Tiles（SCT）。与 TPU TensorCore 的 512 字节加载相比，SCT 支持更细粒度的 4 字节或 32 字节粒度的本地与远程直接内存访问。这使 SC 能够执行 gather/scatter 操作和 ICI 通信，同时与 TensorCore 操作重叠。

在 JAX DevLabs 上我们了解到，SparseCore 的可编程性仍在推进中。可以预期 TPU 定制 kernel 编译器 Mosaic 将以 MPMD 方式编译——SCS 与 SCT 执行不同的 kernel，不同 SparseCore 可运行不同程序。我们猜测，一旦可编程性跟上，TPU 的 MoE kernel 将能像 GPU 那样执行 dispatch 和 combine 操作，而不必按专家 ID 分发。

![](https://substack-post-media.s3.amazonaws.com/public/images/5010fb1d-576f-4449-ba71-a91911bc29d6_1734x800.png)
*来源：Google*

至于[预填充/解码分离（disaggregated prefill/decode）——我们在 AMD 2.0 一文中有深入描述](https://newsletter.semianalysis.com/i/174558631/amds-lack-of-disaggregated-prefill-inferencing-and-nvme-kv-cache-tiering)，Google 在 vLLM 上提供了单机 disagg PD 的实验性支持，但尚不支持多机 wideEP 的分离式预填充或 MTP。这些推理优化对于降低每百万 token 的 TCO、提升每美元性能和每瓦性能至关重要。此外，他们尚未把 TPU 的 vLLM 推理支持集成进 VERL 等流行的 RL 框架。在如何经营开放 AI/ML 生态、尤其是其「原生」TPU 后端方面，Google 正朝正确的方向缓慢前进。

## vLLM TPU 基准测试尚不足为凭

本周出现了一个新的 TPUv6e 推理基准测试，声称 TPUv6e 的每美元性能比 NVIDIA GPU 差 5 倍。我们不同意，主要基于两点原因。首先，这个基准跑的是 TPU 上的 vLLM——它几个月前才发布，性能尚未优化。Google 内部的 Gemini 工作负载和 Anthropic 的工作负载运行在内部定制推理栈上，其每 TCO 性能优于 NVIDIA GPU。

其次，Artificial Analysis 的每百万 token 成本用的是 TPUv6e 每小时每芯片 $2.7 的目录价（list price）。鉴于 TPUv6e 的 BOM 只相当于 H100 的很小一部分，TPU 的大客户没有任何一家付的价格接近这个数。众所周知，大多数云厂商都挂着虚高的目录价，好让客户销售去玩「汽车销售员」式的把戏、给出巨额折扣，让客户觉得占了便宜。[SemiAnalysis AI TCO 模型追踪了 TPU 在各种合约期限（1 个月、1 年、3 年等）下的实际市场租赁价格。](https://semianalysis.com/ai-cloud-tco-model/)

![artificialanalysis](https://substack-post-media.s3.amazonaws.com/public/images/68ac2ab4-62a4-46cb-951a-3cb778fcdb66_4096x1581.png)
*来源：artificialanalysis*

# TPU 软件战略的关键缺失一环

Google 软件战略仍有一处做得不对：其 XLA 图编译器、网络库和 TPU 运行时至今没有开源、文档也很不完善。这导致从高级用户到普通用户，各层次的使用者都因无法调试代码到底哪里出了问题而倍感挫败。此外，其用于多 pod 训练的 MegaScale 代码库同样没有开源。

我们坚信，为了加速普及，Google 应当开源它们——由此带来的用户增长，将超过公开并免费化这些软件 IP 的代价。正如 PyTorch 和 Linux 的开源迅速扩大了普及，开源 XLA:TPU、TPU 运行时与网络库同样会迅速加速这一进程。

# 这对 Nvidia 意味着什么？

既然 Google 已经把 TPU 的事捋顺、开始对外出售、让人们装进自己的数据中心，这对 Nvidia 的业务意味着什么？Nvidia 终于有了一个能威胁其市场份额和利润率的正经对手吗？在付费墙之后，我们将分享我们对此的看法，并披露更多关于 TPU 路线图的内容。
