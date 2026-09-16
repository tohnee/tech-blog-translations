---
title: "AI 价值捕获——向模型实验室转移"
title_en: "AI Value Capture - The Shift To Model Labs"
subtitle: "Vera Rubin VR NVL72：V 代表 Value——Rubin 带来每 TCO 性能的阶跃式提升。ROI 究竟花落谁家：终端用户、新兴 GPU 云、超大规模云厂商、AI 实验室、内存厂商还是 GPU 制造商？"
date: 2026-05-01
source: https://newsletter.semianalysis.com/p/ai-value-capture-the-shift-to-model
crawled: 2026-09-15
authors: ["Daniel Nishball", "Dylan Patel", "Cheang Kang Wen", "Crystal Huang", "Max Kan", "Ray Wang", "Myron Xie", "Zane Fong", "Clara Ee"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# AI 价值捕获——向模型实验室转移

> 原文：[AI Value Capture - The Shift To Model Labs](https://newsletter.semianalysis.com/p/ai-value-capture-the-shift-to-model) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**Vera Rubin VR NVL72：V 代表 Value——Rubin 带来每 TCO 性能的阶跃式提升。投资回报（ROI）究竟花落谁家：终端用户、新兴 GPU 云（Neocloud）、超大规模云厂商、AI 实验室、内存厂商还是 GPU 制造商？**

如今 AI 行业的一天，抵得上其他行业的一年。模型发布、软件突破与硬件改进，正把其他行业动辄数年的周期压缩到几周之内。就在过去几个月里，智能体 AI（agentic AI）跨过了一个真正的拐点，推动 token 价值发生阶跃式变化，而软件和硬件的进步又大幅降低了生成 token 的成本。

这股需求洪流的背后，是终端用户从消耗 token 中获得了巨大投资回报（ROI），而且这场需求增长可以说才刚刚开局。今年，Anthropic 的 ARR 从 $9B 爆炸式增长到如今的超过 $44B，同期其推理基础设施的毛利率也从 38% 提升到 70% 以上。

AI 如此快速的普及在整个技术栈中都创造了价值，但独特的现象在于：AI 实验室如今正在捕获全部价值，而去年它们几乎颗粒无收。

终端用户正在享受一场生产力盛宴——过去需要耗费数十个人时、成本高达数千美元的任务，如今只需几分钟和区区几美元的 token 即可完成。营收和利润率之所以如此暴涨，是因为所创造 token 的价值正在显著改善企业业务。例如，[SemiAnalysis 在 Anthropic Claude token 上的年化支出率已高达 $10.95 million](https://x.com/dylan522p/status/2047104466512400639?s=20)，但我们从中获得的价值让我们有能力击败所有竞争对手并夺取市场份额。

与一年前的 Hopper 相比，诸如 Blackwell 之类的新芯片在运行当今前沿工作负载时每秒可生成的 token 数量是前者的 30 倍，TPUv7、Trainium 3 等 ASIC 也展现出类似的提升。Fireworks、Baseten、Fal 等推理服务商的利润率正在扩大，同时其营收正处于超高速增长轨道。

甚至硬件栈的部分环节也已经重新定价：过去一年内存价格上涨了 6 倍。新兴 GPU 云的 GPU 租赁价格同样在飙升，[H100 一年期租赁合约价格](https://semianalysis.com/gpu-pricing-index/)较 2025 年 10 月的低点已上涨 40%。

不过，行业内有两家拥有惊人定价权的企业却几乎按兵不动。台积电（TSMC）和 NVIDIA 都还没有对近期 AI 模型价值创造的繁荣做出反应。

在本文中，我们将探讨 AI 创造的价值正在向何处聚集——从终端用户到推理服务商、新兴 GPU 云以及硬件供应商。我们将揭示台积电和 NVIDIA 如今正在把巨额价值释放给生态系统的每一个垂直环节。

最后，我们提出一个新框架：「One Chart to Rule Them All」（一图统天下），用它剖析 GPU 租赁经济学，并分析在终端用户、新兴 GPU 云/超大规模云厂商与 AI 系统供应商三者之间，究竟谁在 AI 生态中捕获了最多的价值。

![](https://substack-post-media.s3.amazonaws.com/public/images/9b051759-fe13-4077-a95e-e8d96ec14332_1505x905.png)
*来源：SemiAnalysis AI TCO 模型*

# AI 价值利润池

2023 到 2025 年，AI 的全部价值都被基础设施层收入囊中。NVIDIA 在 2023 年 5 月交出了第一份轰动性的财报电话会，盘后股价大涨 25%，正式标志着 AI 交易的启动。2024 年，当所有人都意识到电力正在成为关键瓶颈时，Vistra 和 GE Vernova 成为标普 500 中表现最好的两只股票（分别上涨 +265% 和 +146%）。2025 年，内存抢尽风头，SanDisk、Western Digital、Seagate 和美光（Micron）全年涨幅均超过 200%。当然这些都是笼统的概括，受益于 AI 资本开支的增长，许多其他基础设施概念股也大幅跑赢大盘。对所有细节数据感兴趣的读者请订阅我们的机构产品。

而在同一时期，所有模型开发商和推理服务商的毛利率之差是出了名的。对大多数人来说，AI 的实际效用仍然不过是锁在聊天界面后面稍微好用的 Google 搜索，以及吉卜力工作室风格的自拍。怀疑论者高调宣称：计划中的数万亿美元资本开支，AI 根本不可能兑现其回报。

# 智能体 AI 改写了游戏规则

2025 年 12 月，世界变了——智能体 AI 开始*真正可用*。SemiAnalysis 已经[撰文](https://newsletter.semianalysis.com/p/claude-code-is-the-inflection-point)[并](https://www.youtube.com/watch?v=MhedMJqzReo&pp=0gcJCdQKAYcqIYzv)[谈论](https://open.spotify.com/episode/7kwRL8e3fOvJf3XzIY9fhC?si=d66a1bf0a29a4249)过许多我们的 [Claude Code 使用情况](https://x.com/dylan522p/status/2047104466512400639?s=20)，但必须强调的是，智能体 AI 已不再仅限于编程。我们的分析师每天都在使用智能体把 Excel 模型转换成仪表盘、为所有研究简报制作图表、搭建财务模型、分析公司财报等等。这些任务要么是 1）我们以前根本做不到的，要么是 2）以前要占用初级分析师许多小时，使他们无法去做附加值高得多的事情。

下表展示了几个来自我们自身工作流的真实案例，将 token 开支与同等人工的成本进行对比：

![](https://substack-post-media.s3.amazonaws.com/public/images/8038e05b-1fd8-4145-a721-edcf0b22b037_2153x853.png)
*来源：SemiAnalysis*

SemiAnalysis 的年化 token 开支已经相当于员工薪酬的约 30%，我们人均每月消耗接近 5B 个 token（比 [Meta](https://www.theinformation.com/articles/meta-employees-vie-ai-token-legend-status?rc=2ojmhe) 高出 5 倍多！）。不过这是幂律分布的，有团队成员每月要跑超过 100B 个 token。显然这一切才刚刚开始，所有白领企业很快都将拥抱智能体 AI。

过去几个月，每个 token 的价值明显提升。我们估计，在智能体任务中运行 Opus 4.7 的真实每百万 token 混合价格为 $0.99，尽管标价为 $5/$25 per MTok。智能体工作负载的输入输出比极高（我们的 Claude Code 使用比率约为 300:1），缓存命中率也很高（90% 以上）。由于缓存输入 token 的价格仅为 $0.50/MTok，大部分 token 最终都落在最便宜的价格档。完整方法论请见[这里](https://semianalysis.com/institutional/everyone-keeps-estimating-token-prices-wrong/)。

从这个角度看，就不难理解 Anthropic 的 ARR 为何在年初至今从 $9B 爆炸式增长到可能的 $44B+。

# token 的生产成本正变得越来越低

与此同时，生产每个 token 的成本急剧下降。这是推理服务商价值增值的最大驱动力，也是大型 AI 实验室利润率大幅提升的关键原因。

token 生产成本之所以大幅下降，是因为加速器逐代涨价的幅度远被高得多的吞吐量（tokens/sec/gpu）所抵消。过去几个月，每百万 token 的平均混合价格大幅下跌——智能体工作负载天然具有多轮、更长输入输出比和更高缓存命中率的特征——但同期推理毛利率反而从 < 40% 升至 > 70%。关于 OpenAI、Anthropic 等所有主要模型的真实每百万 token 混合价格、token 产量和毛利率的深入估算，请参见我们的 [Tokenomics 模型](https://semianalysis.com/tokenomics-model/))。

[InferenceX](https://inferencex.semianalysis.com) 仍是追踪开源模型真实推理性能随时间变化（同时涵盖硬件和软件改进）的最佳基准。

下图展示了 B300 运行 DeepSeek R1、以 8k 输入 token 生成 1k 输出 token 时的吞吐量与交互性对比。最上面一条线是 wideEP + disagg + MTP 下的 token 吞吐量，中间一条是 wideEP + disagg，最下面一条则未使用这三种软件优化中的任何一种。差距令人震惊：同一块 B300 在同样的硬件上可以实现约 1k、约 8k 和约 14k tokens/sec/gpu。仅靠软件改进，吞吐量就能提升 14 倍。

![](https://substack-post-media.s3.amazonaws.com/public/images/9ab53ef3-8fd3-402d-bf7d-930177e81d1b_2064x1270.png)
*来源：SemiAnalysis InferenceX*

如果再算上硬件改进，差距就更加显著。在 FP8 下，优化程度最高的 GB300 NVL72 配置的吞吐量比优化程度最高的 H100 配置高出约 17 倍。如果切换到 Hopper 原生不支持的 FP4，差距跃升至 32 倍。而请记住，GB300 相比 H100 的单 GPU 总拥有成本（TCO）只高出约 70%。

![](https://substack-post-media.s3.amazonaws.com/public/images/a7826e90-f3b0-4749-8d85-ce18a07d3604_1531x940.png)
*来源：SemiAnalysis InferenceX*

# 模型服务商的利润率将继续提升

2025 年 11 月底，Anthropic 以每百万输入 token $5、每百万输出 token $25 的价格发布 Opus 4.5，让许多人感到意外。此前的 Opus 模型（如 4 和 4.1，分别于 2025 年 5 月和 2025 年 8 月发布）定价高出 3 倍，为 $15/$75。

然而我们认为，尽管平均售价（ASP）更低，得益于 Trainium 和 NVIDIA GPU 上的软件改进以及用 Blackwell 替换 Hopper，Anthropic 在 Opus token 上的利润率实际上*不降反升*。

迄今为止，Anthropic 的利润率扩张来自成本下降：他们能以更低的成本生成同样的 token。尽管 Opus 降价，其 ASP/token 实际上反而上升了，因为大部分用量从 Sonnet 转移到了 Opus。

即便 XPU 供应商开始大幅涨价、以更好地分享吞吐量提升带来的收益，Anthropic 仍握有进一步扩大利润率的另一个杠杆：继续把用量向更昂贵的 SKU 迁移。

如前所述，前沿级 token 的价格与其所能产出的工作的经济价值之间的差距，正处于有史以来的最大水平。Anthropic 既可以重新上调基础 Opus 系列的价格，也可以推出新产品。后者的例子已经出现：Opus fast 的定价是常规 Opus 的 6 倍，而 Mythos 的公布价格为 $25/$125（常规 Opus 定价的 5 倍）。这两个 SKU 的利润率都高于常规 Opus，然而那些对 AI 信仰最深的企业依然非常乐意支付更高的价格，因为生产力收益远超成本。如果 Anthropic 愿意让我们花 $150/$750 买 Mythos fast，我们照买不误。

前沿模型服务商低毛利率的时代已经结束。真正的智能体 AI 已永久性地抬高了每 token 的市场出清价格，再无回头路。

# 模型服务商的利润为何不会被竞争侵蚀

认为实验室无法在每 token 效用提升的同时捕获更高利润率，最显而易见的论据就是竞争。但我们认为事态不会这样发展，理由有二。

首先，事实已经证明前沿模型保有定价权。无论基准测试怎么说，在真正的知识工作上，开源模型仍明显逊色于闭源模型，而且没有理由相信这一差距会在短期内弥合。Kimi K2.6（$0.95/$4）对 Opus 定价施加的下行压力微乎其微。

其次，算力约束意味着没有任何一家前沿实验室能够独力服务整个市场。Anthropic 如今已开始把 Claude Code 锁在 $100+/月的订阅门槛之后，并封锁 OpenClaw 等第三方 harness，这已经开始疏远大片市场。在可预见的未来，token 需求将远超供给，这意味着**任何一家能提供真正前沿品质的实验室，都能够按 token 所交付的经济价值来收费，而不是彼此把对方的利润率竞争殆尽。**

# 智能体 AI 席卷市场，台积电与 NVIDIA 却纹丝不动

尽管黄仁勋在最近的 GTC 主题演讲中反复强调智能体 AI，NVIDIA 和台积电仍未完全内化过去几个月 token 经济学的颠覆性变化。从黄仁勋对 InferenceX 的反应来看，NVIDIA 已经低估过 Blackwell 的每美元性能改进，而现在看来，他们还低估了前沿 token 价值升值的速度。

NVIDIA 仍在沿用一套由旧假设塑造的框架：即每单位算力的支付意愿会随时间递减。这个假设已不再成立。在智能体工作负载爆发和每个工作流 token 消耗量激增的推动下，市场已发生实质性转变。需求不再线性增长，而是在复合增长。

而需求仍在加速。据报道，Anthropic 的 ARR 已达 $44B+，高于我们上次更新时的 $30B；同时 GLM、Kimi 等开放权重模型正在扩大可服务的算力基数。各 AI 实验室和新兴 GPU 云的融资正直接转化为增量 GPU 部署。

与此同时，算力供给仍受结构性制约。内存与先进制程晶圆的上游瓶颈持续限制供应：预计 N3 产线稼动率在 2026 年下半年将超过 100%，DRAM 晶圆厂的稼动率也已超过 90%。目前看不到任何实质性的缓解迹象。

台积电本可以大幅涨价，但它没有。我们认为这是其战略失误。即便不涨价，至少也可以要求更多的预付款。

![](https://substack-post-media.s3.amazonaws.com/public/images/ea26fd90-ffad-4b1e-a873-94081c28f5c8_1868x1104.png)
*来源：SemiAnalysis Foundry 模型、SemiAnalysis Accelerator 模型*

当前算力市场的动态表明，如果现有趋势延续，庞大 token 终端需求所创造的价值将继续聚集到 AI 实验室、超大规模云厂商、推理服务商、新兴 GPU 云和内存厂商手中。

在强劲终端需求、token 变现能力上升和单位经济性日益改善的推动下，AI 实验室正在捕获所创造价值中不成比例的份额。与此同时，NVIDIA 的定价框架尚未完全调整以反映这一转变，尽管其硬件仍是支撑这一价值创造的关键瓶颈。token 变现不断上升、单位经济性日益向好，但 NVIDIA 算力仍是这一价值创造得以实现的基石。

各层级对 NVIDIA 系统的需求都极其强劲，买家愿意签订长期合约并接受更高的价格以确保拿到产能。即使存在其他硬件选择，NVIDIA 在生态成熟度、软件栈和部署可靠性方面仍保有明显优势。对许多工作负载（尤其是前沿工作负载）而言，替代品尚不能完全互换。

定于 2026 年下半年（2H26）上市的 Rubin，正处于这些动态的中心。它带来了性能上的阶跃式提升，但同时嵌入了规模大得多的内存子系统——而此时内存恰是供应链中最紧的约束。DRAM 价格已大幅上涨且很可能维持高位，使内存成为系统成本的主要驱动因素。

在此背景下，NVIDIA 有提价空间，尤其是对于 Rubin 这类带来阶跃式性能提升的系统。系统层面所创造的增量价值远超增量成本，尤其从 $/FLOP 或终端工作负载经济性的角度来看。

![](https://substack-post-media.s3.amazonaws.com/public/images/04d13a8a-1f96-4b64-9a51-d293f287149c_2434x1728.png)
*来源：SemiAnalysis AI TCO 模型*
![](https://substack-post-media.s3.amazonaws.com/public/images/322450b9-b91e-43b1-91ba-5c52231fdee4_1437x982.png)
*来源：SemiAnalysis AI TCO 模型*

这就形成了一种明显的脱节。市场已发生结构性转变，需求扩张的速度和持续性都超过了供给的响应能力。然而 NVIDIA 的定价框架仍锚定在旧有假设上，而非调整以反映其系统如今所交付的更高价值。

简而言之，即使 NVIDIA 提高服务器价格、基础设施服务商提高算力价格，需求也不会受损。买家追求的是获得算力，终端用户追求的是尽可能多的 token，两者都在不惜一切代价锁定产能——边际成本优化不是他们当前的首要考量。

# SOCAMM 定价：NVIDIA 的下一个利润率杠杆

在 NVIDIA 能否涨价之后的下一个问题是：在系统内部的哪个环节涨价最有效。

在系统层面，内存是最自然的掌控点。Rubin 级系统向本已紧张的供应链嵌入了多得多的内存，而且与算力不同，内存可以被更干净地分层、并持续重新定价。

这是因为 VR NVL72 上的内存是一种可插拔的、基于 LPDDR 的内存方案，名为 SOCAMM（System-On-Chip Attached Memory Module，片上系统附加内存模块）。SOCAMM 专为 NVIDIA 的机柜级系统设计，可实现更高容量、模块化、更高能效，以及内存与算力的独立定价。

这使 SOCAMM 成为理解 NVIDIA 定价战略最重要的变量之一。两个因素最终决定系统级定价结果：NVIDIA 拿到的 SOCAMM 成本，以及把这些内存转售给客户时叠加的加成（markup）。考虑到 NVIDIA「极致协同设计」（extreme co-design）方式的复杂性和盘根错节的供应链动态，要对其机柜级系统的定价和物料清单（BOM）建立精确认知并非易事。

因此，SemiAnalysis 通过我们的 [VR NVL72 BOM 与功耗预算模型](https://semianalysis.com/vr-nvl72-model/)提供业界领先的拆解。此外，在确定面向终端客户的内存定价时，有两个摇摆因素在起作用：

1. NVIDIA 拿到的 SOCAMM2 价格，以及
2. NVIDIA 向客户出售 SOCAMM 时施加的加成，

两者都是影响最终客户报价的关键因素。

![](https://substack-post-media.s3.amazonaws.com/public/images/ee19ef5f-b636-4ec1-a9a4-c11dc8bced96_1762x444.png)
*来源：SemiAnalysis Memory 模型*

截至目前，我们的 Memory 模型显示，NVIDIA 支付的 SOCAMM 合约价格在 2026 年一季度（1Q26）约为 $8/GB，较 2025 年四季度（4Q25）到 1Q26 出现大幅跃升。这一跳涨由一季度 LPDDR5X 更广泛的价格飙升以及内存供应的总体紧张所驱动。我们基于以下两点锚定这一估算：

1. 鉴于开发复杂度更高、周期更长，SOCAMM 的定价应高于移动端 LPDDR5X（1Q26 约 $6–7/GB）。
2. 移动端 LPDDR5X 价格的跃升应在同期传导至 SOCAMM，因为本已紧张的 LPDDR5X 以及更广泛的通用 DRAM 供应，是在消费需求与服务器需求之间共享的。

业内传闻称，NVIDIA 已通过长期协议（LTA）形式，为其 GB300 NVL 72 和 VR NVL72 两套系统锁定了可观的 SOCAMM 供货量——我们此前已在面向 [Memory 模型](https://semianalysis.com/memory-model/)订户的[机构简报](https://semianalysis.com/institutional/nvidia-aims-to-lock-in-3-year-ltas-with-memory-suppliers/)中做过阐述。作为当今唯一达到规模的 SOCAMM 客户、且可以说是内存领域最关键的买家，NVIDIA 很可能享有优先的供应获取权和价格，而且我们相信，NVIDIA 以往在驾驭供应链方面的记录有目共睹。

话虽如此，更广泛的 DRAM 定价动态仍将不可避免地传导过来。未来几个季度移动端 LPDDR5X 的进一步涨价仍将是 SOCAMM 的关键定价参照，而鉴于 LPDDR5 分配量有限，SOCAMM 也应相应重新定价。我们认为 SOCAMM 在 2026 年底（exit '26）的价格可能超过 $13/GB，与预期的今年年底移动 DRAM 价格大致相当；因此，我们认为 ~$10/GB 是对 NVIDIA SOCAMM 成本的合理假设。

![](https://substack-post-media.s3.amazonaws.com/public/images/71e8437d-53eb-4d37-b7a1-5d43bcd2a130_2082x1330.png)
*来源：SemiAnalysis Memory 模型*

有人可能提出一个关键问题：客户凭什么接受 NVIDIA 的进一步涨价和利润率扩张？NVIDIA 又能以何种站得住脚的理由来论证这一立场？我们认为 NVIDIA 对 SOCAMM 收取 60% 的毛利率是合理的，理由有三：

- 首先，当前环境对 NVIDIA 有利。内存供应处处紧张，而 NVIDIA（至少在 SOCAMM 上）比其客户和同行竞争者锁定了更多供货量，这应能让公司利用这一供应链优势。
- 其次，VR NVL72 仍是迄今为止上市平台中每 TCO 性能最好的，且该系统的生产有一条复杂但成熟的供应链支撑。为了让算力投资最大化，客户可能别无选择，只能接受 NVIDIA 的新定价方式。
- 最后，作为 SOCAMM2 的采购方，NVIDIA 本身就面临着实质性的涨价；因此我们认为，假设客户会接受 NVIDIA 在 VR NVL72 的 SOCAMM2 成本之上叠加的毛利率，并非不合理。

# 从 GB300 到 VR NVL72 的每瓦资本开支趋势

对 GB300 而言，DRAM 是打包在板卡内、以约 75% 的毛利率加价出售的，这使得板载内存收取的利润率与 Blackwell 系统隐含定价的利润率保持一致。

对 Rubin，我们最初假设的是同样的机制，并理解 NVIDIA 会把系统整体毛利率目标定在 75% 出头（mid-70s）。因此，我们最初的物料清单（BOM）建模对整块 Strata 板应用了一致的利润率，SOCAMM 的利润率也维持在同样的 75% 出头。

然而，由于 SOCAMM2 在 Rubin 中是可插拔模块，而 GB300 使用的是焊死在板上的普通 LPDDR5X 模组，内存因此可以与基础系统拆分、单独报价。这使 NVIDIA 能够把内存作为一个独立的报价项明确定价，而不是嵌入板级定价之中。重要的是，这也为 NVIDIA 引入了额外的调整空间：在保持板卡利润率不变的同时，单独调整 SOCAMM2 上的利润率。即便 NVIDIA 最初消化了一部分内存成本通胀，它仍保留通过向客户收取更高系统级利润率来对冲的能力。

因此，从 GB300 过渡到 VR NVL72 时，我们本应预期整体每瓦资本开支上升。但事实恰恰相反——按当前定价计算，每瓦资本开支只是从 GB300 的 $37.4/W 微涨到 VR NVL72 的 $38.1/W。这还是在芯片 TDP 从 GB300 到 VR NVL72 几乎翻倍（1400W 到 2300W）、FLOPs 大幅增加的情况下。

![](https://substack-post-media.s3.amazonaws.com/public/images/46097fe3-eabd-4ca2-ad77-a1043bbc98e7_990x941.jpeg)
*来源：SemiAnalysis AI TCO 模型*

相对于服务器每瓦资本开支的总体趋势，这很不寻常。在 AMD、NVIDIA 和定制 ASIC 中，每瓦性能的逐代改进让供应商得以在系统层面捕获更多价值，因此每瓦资本开支通常会逐代上升。所以，从 GB300 到 VR NVL72，$/GW 看起来基本原地踏步，令我们感到费解。考虑到 GB300 到 VR NVL72 的每瓦性能提升超过一倍，这就更不寻常了。

NVIDIA 还有机会在内存上比在 GPU 上更大幅度地实施价格歧视，因为内存不像 GPU 那样会引起反垄断方面的担忧。

![](https://substack-post-media.s3.amazonaws.com/public/images/4a954297-1d58-48dd-a375-37e068a206de_924x637.png)
*来源：SemiAnalysis AI TCO 模型*
![](https://substack-post-media.s3.amazonaws.com/public/images/f230ea96-bb31-4cc0-87b6-4dbfa5bb8709_1408x978.png)
*来源：SemiAnalysis AI TCO 模型*

# 网络设备：价格歧视的载体

如今，NVIDIA 并不会在同一层级的不同客户之间对 GPU 定价进行大幅差异化。无论对象是超大规模云厂商、新兴 GPU 云、新崛起的新兴 GPU 云、主权客户还是企业客户，核心组件在全生态内的售价大体相近。这就为核心 GPU 和内存组件形成了相对统一的定价结构——即便在这个支付意愿差异巨大的市场里也是如此。

虽然 GPU 定价相对统一，NVIDIA 历来在网络设备上实行价格歧视，给新兴 GPU 云和其他边缘云玩家的报价比超大规模云厂商高出相当多的溢价。我们对 GPU 云服务商做了一次自主调研，发现例如 SN5610 交换机卖给新兴 GPU 云的价格可能是卖给超大规模云厂商的 2 倍。超大规模云厂商显然拥有更强的议价能力，但这并不是因为它们从 NVIDIA 采购的交换机和收发器更多。

新兴 GPU 云缺乏规模和网络专业能力去定制并优化网络集群的成本，因此最终还是偏好 NVIDIA 的交钥匙方案。超大规模云厂商则直接与 OEM 和 ODM 合作，拥有足够的网络工程人手来部署更具成本效益的方案——这些方案可能不是交钥匙部署，要正确落地更为费力。

不过，从集群总资本成本来看，新兴 GPU 云与超大规模云厂商在网络成本上的差距就没那么显著了。对两个可比集群而言，新兴 GPU 云网络成本比超大规模云厂商高 94%，折算到完整机柜级服务器的全口径资本成本上，只相当于提高了 10%。这还没算上电力、水电与运营等其他变量——这些变量会进一步侵蚀网络设备定价差异带来的成本差距。

![](https://substack-post-media.s3.amazonaws.com/public/images/e4d7e07f-58d7-4bbb-8f89-59f4d763aee6_2262x957.png)
*来源：SemiAnalysis AI Networking 模型*

尽管这是一个绝佳的案例研究，展示了 NVIDIA 如何按价值为其解决方案定价，但新兴 GPU 云与超大规模云厂商之间当前的价格差距已经很大，NVIDIA 继续拉动这个杠杆的空间有限。

# NVIDIA：AI 的中央银行

对于 NVIDIA 迄今在定价上的克制，一种解释可能是监管与战略层面的双重谨慎。

鉴于 NVIDIA 在 GPU、互连和软件上的全面主导地位，其在 AI 算力栈中的位置已受到越来越多的反垄断审视。在这种环境下，激进地重新定价系统以完全捕获所交付的价值，有可能引来更多关注——尤其当此举带来超额的利润率扩张、而下游 AI 实验室同时也在赚取可观利润时。把定价维持在与以往框架相近的水平，有助于避免在供给受限的市场中释放出定价权过强的信号。

这种行为并非没有先例。台积电历来采取类似做法。即便在满负荷运行、充当先进制程供给瓶颈的情况下，台积电也大体避免按稀缺性充分定价。相反，它把长期关系和生态稳定置于榨取短期最大利润之上，部分原因是为了避免监管和客户的反弹。

NVIDIA 似乎正走在一条相似的路上。它没有对 Rubin 系统全面重新定价以同时反映性能提升和内存成本的结构性转变，而是维持着更为审慎的定价方式。这在利润率扩张与监管风险、生态动态之间取得平衡，也兼顾了避免加速客户向替代算力平台分散的需要。

我们在[「NVIDIA 作为 AI 中央银行」的机构简报](https://semianalysis.com/institutional/nvidia-as-the-central-bank-of-ai/)中提出过类似观点。NVIDIA 在积极扶持更广泛的生态发展，着眼于长期需求扩张而非最大化近期榨取。如今，前沿实验室受益于 NVIDIA 软件驱动的效率提升，但这些改进并未在硬件层面被完全货币化。结果，尽管 NVIDIA 是主要的赋能者，增量价值仍持续向下游聚集。通过「抽干房间里的氧气」，NVIDIA 旨在确保自己在可预见的未来始终是 AI 时代的主角。

然而——既然算力需求远超算力供给，掌握稀缺资源的一方为何不该收取更高的价格、享受更丰厚的利润？

# 台积电：全世界最公平、最正义的公司

我们此前已经指出，[台积电的 N3 产能甚至更为紧张](https://newsletter.semianalysis.com/i/190110359/the-tsmc-n3-shortage)。今明两年，所有主要加速器路线图都已收敛到 N3 制程节点。NVIDIA、Broadcom、Annapurna、联发科（MediaTek）和 AMD 都在向台积电争夺更多 N3 晶圆产能配给，以便向各自的客户交付更多算力。虽然 N3 产能可以说是整个体系中约束最紧的环节，其价格却保持相对稳定。

![](https://substack-post-media.s3.amazonaws.com/public/images/1b15b856-fc6a-4df7-989e-90b2a3c2c57e_2692x1774.png)
*来源：SemiAnalysis Foundry Industry 模型*
![](https://substack-post-media.s3.amazonaws.com/public/images/4a787984-7145-4738-8161-5652d204ddd9_2692x1774.png)
*来源：SemiAnalysis Foundry Industry 模型*

台积电的战略是通过下行周期保护盈利能力。其副作用是这一政策在上行周期中也削弱了上行空间。无论如何，台积电显然把价值留在了桌面上——它所有主要的无厂设计客户都享受着很高的毛利率，而这些价值本可以转移到台积电手中。

然而，台积电完全可以在定价上采取更激进的姿态，客户不仅会接受，我们认为有些客户甚至乐见其成。如果多付晶圆钱能把付不起的竞争者挡在门外，NVIDIA 求之不得。毕竟，黄仁勋本人在 2024 年就说过台积电的晶圆应该卖得更贵，他正是这个意思。

台积电也可以选择签订带有产能保障承诺和预付款的长期协议，来替代大幅涨价。这是更可能出现的路径。

我们认为，NVIDIA 开始越来越像台积电。

在这种环境下，NVIDIA 最大的优势是采购。NVIDIA 已锁定远超比例的紧张上游供应（尤其是台积电晶圆），使其能够服务别人无法满足的需求。

因此，Anthropic 等 AI 算力买家被迫留在 NVIDIA 生态之内，因为 TPU 和 Trainium 的替代产能同样受制于上游瓶颈而供给有限。尽管拥有这一结构性优势，NVIDIA 并未在定价上充分体现。

目前，NVIDIA 的定价仍锚定在成本定价框架上。但这不太可能长久。随着推理服务商的投资回报变得更加清晰、更被广泛接受，重心将进一步转向按价值定价。这会减轻对定价的审视压力，给 GPU 基础设施供应商留出从成本定价转向价值定价的空间。一旦这一转变发生，就为 NVIDIA 提价、在系统层面捕获更多所交付价值创造了空间——这正是蛋糕做大的体现。

# 交叉验证 VR NVL72 租赁定价：成本定价法与价值定价法

定价主要有两种方法：

1. 成本定价法（cost-based pricing），以及
2. 价值定价法（value-based pricing）。

成本定价法的前提是：只有当项目满足新兴 GPU 云的最低回报门槛时，GPU 部署才会发生。若回报低于这一水平，产能就不会被部署，直到价格调整到跨过这道门槛。

因此，成本定价框架下的租赁价格，就是能让新兴 GPU 云的项目 IRR 超过部署最低门槛收益率的价格。如今大多数项目的 IRR 大致落在 15%~19%（mid-to-high teens）区间。当前一个示例性的 GB300 部署，在 5 年期、15% 预付的条件下，项目 IRR 大约可达 15.6%。

![](https://substack-post-media.s3.amazonaws.com/public/images/4bbe0fd4-467e-4e2b-880d-05b138a6afe3_727x566.jpeg)
*来源：SemiAnalysis AI TCO 模型*

部署 VR NVL72 时，新兴 GPU 云会瞄准类似的 IRR，这反过来决定了 Vera Rubin 首发 GPU 租赁价格的可能水平。按我们对 VR NVL72 的全口径服务器成本计算，一个 5 年期、15% 预付的项目若要达到多数 GB300 项目所用的 15.6% 的项目 IRR 门槛，GPU 小时租赁价格至少需要 USD 4.92/hr。

![](https://substack-post-media.s3.amazonaws.com/public/images/122fdbf8-acd4-40a9-bcdb-b822857a8069_1038x871.jpeg)
*来源：SemiAnalysis AI TCO 模型*
![](https://substack-post-media.s3.amazonaws.com/public/images/4fe88f0e-7194-4e9f-9b69-8c872ae0a5d4_1456x936.jpeg)
*来源：SemiAnalysis AI TCO 模型*

我们的第二个框架是价值定价法。我们锚定现有 SKU 所隐含的 $/FLOP，并推算它对 Rubin 意味着什么。这代表算力租用方在 Rubin 与当前一代 GPU 之间保持无差异时、理论上愿意支付的最高价格——因此构成 GPU 租赁价格的天花板。在这里，我们考察每 PFLOP 租赁价格的改善趋势。

![](https://substack-post-media.s3.amazonaws.com/public/images/13ee4084-c663-44cf-b143-9891e30f5aff_2434x1728.png)
*来源：SemiAnalysis AI TCO 模型*

对于训练工作负载，我们以 GB300 的定价为锚，在标称 FP8 稠密算力口径下比较每 PFLOP 的租赁成本。按当前 5 年期 GB300 租赁价格约 $0.70/PFLOP 计算，在平价基础上推得 VR NVL72 的天花板价格约为每 GPU 小时 $12.25。

VR NVL72 的每 TCO 价格引人注目之处在于：与 GB300 及更早的显卡不同，其价值定价与成本定价之间存在极大缺口。如果我们保守一点，取略低于趋势线的一点——例如租赁价格 $0.55/PFLOP——对应 $9.63/hr/GPU，几乎是跨过新兴 GPU 云回报门槛所需的最低租赁价格 $4.92/hr/GPU 的两倍。

![](https://substack-post-media.s3.amazonaws.com/public/images/0ec95e34-a22d-4c14-9491-fb259b46538a_1499x925.jpeg)
*来源：SemiAnalysis AI TCO 模型*

# One Chart to Rule Them All（一图统天下）

**成本定价法**构成 GPU 租赁价格的下限——低于这一租赁价格，新兴 GPU 云就不会批准新的 GPU 项目。**价值定价法**构成 GPU 租赁价格的理论天花板——不会有客户愿意以更高的 $/FLOP 去租更新一代的 GPU。

我们把这两个约束，加上一条展示给定 GPU 租赁价格下新兴 GPU 云回报的定价曲线，合并成一张定价图。这张「One Chart To Rule Them All」同时也是一个理解竞争格局与定价权的框架。

在文章开头我们提出过一个问题：AI 需求强劲的红利究竟归谁？

把新兴 GPU 云实际收取的 GPU 租赁价格与这些项目赚取的 IRR 画在一起，就能回答这个问题。沿下图中的橙色曲线向右上方移动，代表新兴 GPU 云议价能力更强：新兴 GPU 云能够收取更高的 GPU 租金，并获得远高于其 IRR 门槛的回报。

如果 NVIDIA 上调 VR NVL72 的定价，定价曲线就会向左上方移动。这是因为需要更高的租赁价格来抵消更高的系统成本，同时让新兴 GPU 云仍赚到同样的 IRR。这一移动代表 NVIDIA 等系统供应商享有更强的议价能力。

![](https://substack-post-media.s3.amazonaws.com/public/images/9b051759-fe13-4077-a95e-e8d96ec14332_1505x905.png)
*来源：SemiAnalysis AI TCO 模型*

左上角——即蓝色最大租赁价格/PFLOP 与米色新兴 GPU 云项目 IRR 最低门槛的交点——代表理论上最高的 AI 集群定价。若系统定价再高，新兴 GPU 云和终端用户还不如直接购买或租赁 GB300。当前定价曲线与左上角之间的缺口越大，NVIDIA 等 AI 集群供应商提高系统定价的空间就越大。

按今天的 VR NVL72 系统定价，新兴 GPU 云在 5 年期合约上可以收 $4.90/hr/GPU，同时仍赚到与其 GB300 项目相同的 15% IRR。对客户而言，每 PFLOP 租赁价格折合 $0.28/PFLOP，较 GB300 NVL72 的每 PFLOP 成本下降 60%——这一成本改善幅度远低于趋势水平。

这表明 NVIDIA 有可观的空间上调服务器价格。服务器价格上调约 40%，所带来的每 FLOP 价格成本改善仍低于趋势，同时还给新兴 GPU 云留下足够的提价空间，让它们能赚到更高的 IRR。即使新兴 GPU 云沿灰色曲线进一步提价——例如收 $8.00/hr/GPU、赚到 38% 的 IRR，对应成本 $0.46/PFLOP——这仍是一个低于趋势的改善幅度。

必须指出，以上分析主要聚焦于租赁价格/FLOP——但每 TCO 推理性能的改善一直在以更快的速度推进。虽然我们尚未在 InferenceX 上对 VR NVL72 系统进行基准测试，但 VR NVL72 在每 token 交付成本（美元/token）上的下降速度很可能更陡峭，这意味着 NVIDIA 从整个生态捕获更多价值的余量可能还更大。

![](https://substack-post-media.s3.amazonaws.com/public/images/8ef64f5b-4491-4b2d-931c-e4e9654a1f9d_1032x620.jpeg)
*来源：SemiAnalysis AI TCO 模型*

# VR NVL72 对比 GB300：每 TCO 性能
