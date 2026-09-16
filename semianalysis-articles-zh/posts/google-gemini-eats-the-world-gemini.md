---
title: "Google Gemini 吃掉世界——Gemini 以 5 倍碾压 GPT-4，以及「GPU 穷人」们"
title_en: "Google Gemini Eats The World – Gemini Smashes GPT-4 By 5X, The GPU-Poors"
subtitle: "让所有人都显得「GPU 贫穷」的算力资源"
date: 2023-08-28
source: https://newsletter.semianalysis.com/p/google-gemini-eats-the-world-gemini
crawled: 2026-09-15
authors: ["Dylan Patel", "Daniel Nishball"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# Google Gemini 吃掉世界——Gemini 以 5 倍碾压 GPT-4，以及「GPU 穷人」们

> 原文：[Google Gemini Eats The World – Gemini Smashes GPT-4 By 5X, The GPU-Poors](https://newsletter.semianalysis.com/p/google-gemini-eats-the-world-gemini) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**让所有人都显得「GPU 贫穷」的算力资源**

新冠疫情之前，谷歌发布了 MEENA 模型，并在短短一段时间内，它是世界上最好的大语言模型。谷歌写的[博客](https://ai.googleblog.com/2020/01/towards-conversational-agent-that-can.html)和[论文](https://arxiv.org/abs/2001.09977)极其「可爱」，因为它专门拿自己与 OpenAI 对比。

> 与现有最先进的生成式模型 OpenAI GPT-2 相比，Meena 的模型容量大 1.7 倍，训练所用的数据量是 8.5 倍。

训练这个模型所需的 FLOPS 是 GPT-2 的 14 倍以上，但这在很大程度上无关紧要，因为仅仅几个月后 OpenAI 就祭出了 GPT-3：参数量多 65 倍以上、token 数多 60 倍以上、FLOPS 多 4,000 倍以上。这两个模型之间的性能差距是巨大的。

MEENA 模型催生了一份由 Noam Shazeer 撰写的内部备忘录，题为「MEENA Eats The World（MEENA 吃掉世界）」。在这份备忘录中，他预言了许多世人在 ChatGPT 发布之后才幡然醒悟的事情。核心要点是：语言模型将以各种方式日益融入我们的生活，并且将主宰全球部署的 FLOPS。Noam 写下这些时远远走在了时代前面，但当时大多被关键决策者忽视、甚至嘲笑。

让我们岔开一下，说说 Noam 到底领先时代多少。他是原始 Transformer 论文「[Attention is All You Need](https://arxiv.org/abs/1706.03762)」团队的成员，还参与了[第一篇现代混合专家（MoE）论文](https://arxiv.org/abs/1701.06538)、[Switch Transformer](https://arxiv.org/abs/2101.03961)、[Image Transformer](https://arxiv.org/abs/1802.05751)，以及 [LaMDA](https://blog.google/technology/ai/lamda/) 和 [PaLM](https://ai.googleblog.com/2022/04/pathways-language-model-palm-scaling-to.html) 的诸多组成部分。[他在 2018 年提出、至今尚未被广泛归功的想法之一](https://arxiv.org/abs/1811.03115)是[投机解码（speculative decoding）——我们在此前关于 GPT-4 的独家全解中详细讲解过](https://www.semianalysis.com/i/134355860/speculative-decoding)。投机解码能将低 batch 推理的成本降低数倍。

这里的重点是：谷歌手握王国的全部钥匙，却把到手的宝贝弄丢了。这是人人都看得明白的判断。

而未必明显的是另一个判断：沉睡的巨人谷歌已经醒来，他们的迭代速度将在年底前把 GPT-4 的总预训练 FLOPS 碾压 5 倍。按照其当前的基础设施建设进度，到明年年底达到 20 倍的路径也很清晰。至于谷歌是否有魄力在不阉割模型创造力、不破坏现有商业模式的前提下把这些模型公之于众，那是另一场讨论。

今天我们想讨论：谷歌用于 Gemini 的训练系统、Gemini 模型的迭代速度、谷歌 Viperfish（TPUv5）的爬坡、谷歌相对于其他前沿实验室的竞争力，以及一个我们称之为「GPU 穷人」（GPU-Poor）的群体。

## GPU 富豪

算力获取是一个双峰分布。少数几家握有 2 万颗以上的 A/H100 GPU，而个体研究者也能为自己的宠物项目（pet project）拿到数百乃至上千颗 GPU。其中最突出的，是 OpenAI、谷歌、Anthropic、Inflection、X 和 Meta 的研究者们，他们的算力资源与研究者人数之比将是最高的。上述公司中的少数几家以及**多家中国公司**到明年年底将拥有 10 万颗以上，不过我们不确定中国研究者的比例，只知道 GPU 数量。

我们在湾区看到的最有趣的趋势之一，是顶尖 ML 研究者炫耀自己拥有、或很快将能用到多少颗 GPU。事实上，过去约 4 个月里这一风气已经如此普遍，以至于变成了一场「攀比大赛」，并直接影响顶尖研究者决定去向。将拥有全球第二多 H100 的 Meta，正把它当作招聘战术积极使用。

## GPU 穷人

另外还有一大批初创公司与开源研究者，正用少得多的 GPU 苦苦挣扎。他们把大量时间与精力花在那些根本无济于事、坦率说也无关紧要的事情上。例如，许多研究者花无数小时纠结于用 VRAM 不够的 GPU 去微调模型。这是对其技能与时间的极度低效的使用。

这些初创公司与开源研究者用更大的 LLM 去微调更小的模型，以冲击排行榜式基准——这些评测方法千疮百孔，更看重文风而非准确性或实用性。他们普遍没有意识到：要让更小的开源模型在真实负载上变得更强，预训练数据集与 IFT 数据需要显著更大、更高质量。

是的，高效使用 GPU 非常重要，但 GPU 穷人们在很多方面恰恰忽略了这一点。他们并不关心规模化效率，时间也没有花在刀刃上。在他们 GPU 贫瘠的环境里能做出的商业化成果，对一个到明年年底将被[超过 350 万颗 H100 淹没](https://www.semianalysis.com/p/ai-capacity-constraints-cowos-and)的世界而言大多无关紧要。至于学习与实验，更弱小的游戏 GPU 完全够用。

GPU 穷人们仍在主要使用[稠密模型](https://www.semianalysis.com/p/gpt-4-architecture-infrastructure)，因为 Meta 慷慨地把 LLAMA 系列模型送到了他们腿上。若没有~~上帝~~扎克伯格（Zuck）的恩典，多数开源项目的处境还会更糟。如果他们真的在乎效率，尤其是端侧效率，他们应该运行 MoE 这类稀疏模型架构、在更大数据集上训练，并像前沿 LLM 实验室（OpenAI、Anthropic、Google Deepmind）那样[实现投机解码](https://www.semianalysis.com/i/134355860/speculative-decoding)。

弱者们应当聚焦这样的权衡：通过提高算力与内存容量需求、换取内存带宽的降低，以改善模型性能或 token 到 token 的延迟——因为那正是边缘端所需要的。他们应当专注于在共享基础设施上高效服务多个微调模型，而不必承受小 batch size 的可怕成本惩罚。然而，他们却不断地盯着内存容量限制、或过度量化，同时对真实的质量下降闭目塞听。

让这场吐槽稍微再岔开一点：总体而言，模型评测是失灵的。虽然闭源世界在大力改进这一点，但开放基准的世界毫无意义，几乎测不出任何有用的东西。不知为何，业界对 LLM 的排行榜化有一种病态执迷，还热衷于给无用的模型起愚蠢的名字造梗（WizardVicunaUncensoredXPlusPlatypus）。希望开源社区的精力能转向评测、投机解码、MoE、开放 IFT 数据，以及超过 10 万亿 token 的干净预训练数据集，否则[开源根本没有机会与商业巨头竞争](https://www.semianalysis.com/p/google-we-have-no-moat-and-neither)。

美国与中国还能继续向前狂奔，而欧洲的初创公司与政府支持的超级计算机（例如 Jules Verne）则完全没有竞争力。欧洲将因无力进行大额投资、选择维持 GPU 贫穷状态而在这场竞赛中掉队。甚至多个中东国家在 AI 大规模基础设施上的投入都比欧洲多。

GPU 贫穷并不只限于精打细算的初创公司。一些最负盛名的 AI 公司——HuggingFace、Databricks（MosaicML）和 Together——同样属于 GPU 穷人阵营。事实上，无论按每颗 GPU 摊到多少世界级研究者算，还是按 GPU 数量对比其雄心/潜在客户需求算，他们都可能是其中最穷的。他们拥有世界级的研究者，但所有人都受限于在能力低几个数量级的系统上工作。这些公司在训练真实模型方面收到了企业源源不断的涌入需求，进账的 H100 也以千计，但这仍不足以拿下多少市场。

英伟达正在吃掉他们的午餐：其 DGX Cloud 服务与多台自建超算所拥有的 GPU 数量是他们的数倍。英伟达 DGX Cloud 提供预训练模型、数据处理框架、向量数据库与个性化、优化推理引擎、API，以及 NVIDIA 专家支持，帮助企业为自定义用例调优模型。该服务已经拿下了横跨 SaaS、保险、制造、制药、生产力软件、汽车等多个行业的多家大型企业。虽然并非所有客户都已公布，但光是公开名单——Amgen、Adobe、CCC、ServiceNow、Accenture、AstraZeneca、Getty Images、Shutterstock、Morningstar、Evozyne、Insilico Medicine、Quantiphi、InstaDeep、Oxford Nanopore、Peptone、Relation Therapeutics、ALCHEMAB Therapeutics 和 Runway——已经相当亮眼。

这份名单比其他玩家的长得多，而且英伟达还有许多未披露的合作。需要说明的是，这些已公布的英伟达 DGX Cloud 客户贡献多少营收并不为人所知，但鉴于英伟达的云支出规模与自建超算投入，可以从英伟达云上购买的服务，似乎将超过 HuggingFace、Together 与 Databricks 有希望提供的总和。

HuggingFace 与 Together 合计筹集的区区几亿美元，意味着他们将继续 GPU 贫穷、被甩在身后——他们将无力训练 N-1 代 LLM 来充当客户微调的底座。这意味着他们最终无法在企业市场攫取高份额，反正这些企业今天本来就可以直接使用英伟达的服务。

HuggingFace 尤其握有行业内最响亮的品牌之一，他们需要利用这一点进行巨额投入，打造多得多的模型、定制与推理能力。他们最近一轮融资的估值定得太高，反而筹不到竞争所需的资金。HuggingFace 的排行榜恰恰暴露了他们的盲目——它实际上正在伤害开源运动，诱导后者造出一堆在真实使用中毫无用处的模型。

Databricks（MosaicML）至少还有可能赶上，凭借其数据资产与企业客户关系。问题是，如果他们想服务好超过 7,000 家客户，就必须把支出加速数倍。13 亿美元收购 MosaicML 是对这个方向的重注，但他们还需要往基础设施上砸下同样量级的钱。不幸的是，Databricks 无法用股票支付 GPU 账单。他们需要通过即将到来的私募轮/IPO 完成一次大规模融资，用这笔真金白银在硬件上四倍加注。

经济账完全站不住脚，因为他们必须先把基础设施建好客户才会来，而英伟达正在为自己的服务大把砸钱。要说清楚：许多玩家买下大量算力却赚不回本（Cohere、沙特、阿联酋），但这是参与竞争的前提。

这些卖铲子的训练与推理运营公司（Databricks、HuggingFace、Together）落后于其主要竞争对手——后者恰好也是他们几乎全部算力的来源。下一个最大的定制模型运营者，就是 OpenAI 的微调 API。

关键在于：从 Meta 到微软再到初创公司，所有人都只是在充当资本流向英伟达银行账户的管道。

谁能把我们从英伟达的奴役中解救出来？

有，有一位潜在的救世主。

## 谷歌——全球算力最富有的公司

虽然谷歌内部确实也在使用 GPU，并通过 GCP 卖出了相当数量，但他们袖中还藏着几张王牌。其中包括 Gemini，以及已经开始训练的下一代模型。他们最重要的优势，是其效率无可匹敌的基础设施。

在进入 Gemini 与其云业务之前，我们先分享几个关于其疯狂算力建设的数据点。下图展示每季度新增的先进芯片总数。这里我们给了 OpenAI 一切善意假设：其 GPU 总量将在两年内翻 4 倍。对谷歌，我们忽略了其全部存量机队——TPUv4（Pufferfish）、TPUv4 lite 与内部使用的 GPU。此外，我们也没有计入 TPUv5e（lite），尽管它很可能是较小语言模型推理的主力机型。图中谷歌的增长仅计入 TPUv5（Viperfish）。

[获取 8 折团购订阅](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
