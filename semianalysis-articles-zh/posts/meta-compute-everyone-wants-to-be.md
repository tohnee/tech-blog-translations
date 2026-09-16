---
title: "Meta Compute：人人都想当新兴 GPU 云"
title_en: "Meta Compute: Everyone Wants To Be A Neocloud"
subtitle: "Zuck 启用 B 计划？SpaceX 2.0、Bedrock 2.0、MSL 没有放弃、RecSys 复杂度扩展 10 倍……ClusterMAX 评级即将出炉？"
date: 2026-07-02
source: https://newsletter.semianalysis.com/p/meta-compute-everyone-wants-to-be
crawled: 2026-09-15
authors: ["Jeremie Eliahou Ontiveros", "Max Kan", "Joey Brookhart", "Crystal Huang", "Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# Meta Compute：人人都想当新兴 GPU 云

> 原文：[Meta Compute: Everyone Wants To Be A Neocloud](https://newsletter.semianalysis.com/p/meta-compute-everyone-wants-to-be) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**Zuck 启用 B 计划？SpaceX 2.0、Bedrock 2.0、MSL 没有放弃、RecSys 复杂度扩展 10 倍……ClusterMAX 评级即将出炉？**

Bloomberg 头条暗示 Meta 可能变成一家新兴 GPU 云（Neocloud），市场反应立竿见影：Coreweave、Nebius 等新兴 GPU 云遭遇激进抛售，"产能过剩"的争论卷土重来。让我们把话说清楚——我们认为**这两种解读都是错误的**，Meta 的数据中心与算力采购将会***加速***，而非放缓。2027 年的资本开支将高得惊人。仅在今年头六个月，**Meta 已在云与托管（Cloud & Colo）上签约超过 5GW 容量**，这甚至还没算上其不断加速的自建活动。一切皆计算机（everything is computer），人人皆可成为新兴 GPU 云（everything is a neocloud）。

![](https://substack-post-media.s3.amazonaws.com/public/images/5e3518a9-ee28-403f-9df5-6ab7c03ac2e9_1227x668.png)
*来源：SemiAnalysis 数据中心模型*

Meta 的在建容量一直在加速。下面展示的是 Meta 最大的两座园区——这两张图代表了 2.5GW 的在建容量！顺带一提，如果你相信了"美国一半数据中心都在延期、在建的只有 5GW"这种可笑的头条，我们在这里向你展示：仅这两座数据中心就占到了其中一半。关于这些头条为何完全离谱，请阅读我们的文章[《别再说美国一半数据中心都在延期了》](https://newsletter.semianalysis.com/p/stop-saying-half-of-2026-us-datacenter)。

![](https://substack-post-media.s3.amazonaws.com/public/images/2ec4417c-7506-447b-92a9-e81f9137c155_1872x1456.png)
*来源：SemiAnalysis 数据中心模型*

当然，这自然引出两个问题：Meta 拿这些算力做什么？如果它真的变成新兴 GPU 云，会不会把所有这些供给倾泻到市场上？总体来看，我们识别出四大高价值用例，它们彼此各异，且与传统新兴 GPU 云的玩法大不相同：

1. 前沿 AI 模型：Meta 并未放弃训练前沿模型。增量产能的大头仍流向 Meta 超级智能实验室（MSL），而且我们认为团队目前对自身进展相当兴奋。后续报告将深入拆解 MSL、其独特的数据策略，并讨论其追赶 Anthropic 和 OpenAI 的胜算。当然，我们的 [Tokenomics 模型](https://semianalysis.com/tokenomics-model/)订阅用户早已知晓我们的观点，并可实时获取全部这些内容。
2. 推荐系统（RecSys）：我们相信 Meta 认为自己可以把广告推荐系统的复杂度扩展 10 倍以上，以加速营收增长。这既需要其推荐系统模型的推理算力，也需要训练算力。它们还能做更多生成式的定向广告。
3.（***SemiAnalysis 独家***）我们相信 **Meta 正与 Anthropic 进行最终阶段谈判，以获取 Claude 私有实例的访问权**。这将类似于其他超大规模云厂商的 Bedrock、Foundry、Vertex（[深度解析见此文](https://newsletter.semianalysis.com/p/anthropic-growth-and-bedrock-mix)）。对 Meta 而言用例多种多样：从内部使用，到打造由前沿 AI 智能体驱动的顶级销售与营销（Sales & Marketing）SaaS。我们预计 Meta 将推出 token 即服务（token-as-a-service）端点，并依托其网络与分发能力逐步向协议栈上层走。初期对外是其自有模型、对内是 Anthropic 模型，但我们相信随着时间推移，它们对外也会提供 Anthropic 和 OpenAI 的模型。
4. 我们预计 Meta 将达成几笔"SpaceX 式"交易。Elon 是销售天才，他开创了一个**全新的市场细分：以巨额溢价出售的大规模按需算力**。我们认为 Meta 想分一杯羹，但会有所选择。毕竟，仅仅几百 MW 就能带来超过 $10B 的年收入！我们预计一笔百亿美元级的 Anthropic 交易将启动这个飞轮。

这种高选择性——四项高附加值选项——让 Meta 得以继续激进地签约算力。Meta 超级智能仍是核心引擎，但即便它不成功，还有许多高利润率的算力变现替代方案。这本质上是 CFO 的梦想，让全押算力变得轻而易举——我们敢打赌，Susan 在看到 SpaceX 算力交易的定价时一定来了个 180 度大转弯！Meta 不会成为一家毛利率约 30% 的普通裸金属 IaaS 供应商——它的所有选项都是高价值的，使其轻松付得起给其他新兴 GPU 云让出的利润空间，以加速自身机队建设——即便 MSL 不成功也无妨。

我们的 [数据中心模型](https://semianalysis.com/datacenter-industry-model/) 按季度拆解了其容量增量在自建、数据中心租赁与云租赁之间的分布。自 2024 年初以来签约近 10GW 之后，其容量增量如今主要通过第三方获得。我们预计这一趋势将持续，并相信 Meta 将成为 Coreweave、Nebius 等厂商 RPO（剩余履约义务）增长的巨大来源。

我们的模型还按季度将 Meta 的容量拆分为 MSL、其他 AI 与非 AI 三类。MSL 的巨额增长可以理解（他们需要跟上 Anthropic 和 OpenAI 的步伐！），而 2026 年"其他 AI"的激增表明，Meta 在 RecSys、"SpaceX 同款"以及 Bedrock 式 token 即服务上变现算力的选择余地充足。即便 RecSys 的扩展不及预期，它们还有其他选项。当然，如果 MSL 失败，云（Cloud）容量将会一飞冲天。

![](https://substack-post-media.s3.amazonaws.com/public/images/4cecc46f-29d5-47fa-aa53-da039e3ff5e1_1229x668.png)
*来源：SemiAnalysis Tokenomics 模型、数据中心模型*

现在来深挖这四个选项。我们先从类 SpaceX 交易和 Bedrock 式雄心开始。随后，在付费墙之后，我们再讨论 MSL 与 RecSys 的前景。

# SpaceX 之梦——Elon 的天才交易

Elon Musk 宣布第一笔 Anthropic 交易时，震惊了整个 AI 基础设施界。而他拿出 Google 交易时，更是让世界二次震惊。原因很简单：如下图所示，这两笔交易的每 MW 收入分别是同行收费水平的 3 倍和 4 倍。鉴于成本结构大体相同，每 MW 利润的差距当然更大。

![](https://substack-post-media.s3.amazonaws.com/public/images/4b5cf278-7508-4a2b-9ec9-54bea038868e_2430x1296.png)
*来源：AI 云 TCO 模型*

SpaceX 在 Google 交易上的定价，甚至高于我们在按需或短期租赁市场上观察到的水平。Elon 实质上发明了一个全新的市场细分。我们的 [AI 云 TCO 模型团队](https://semianalysis.com/ai-cloud-tco-model/)每年跟踪数百笔 GPU 云交易，涵盖 SLA、定价、合同期限等全部合同条款。正因如此，我们掌握着遥遥领先、按合同期限划分的全球最佳 GPU 定价信息——[可在此免费仪表板中预览](https://semianalysis.com/gpu-pricing-index/)。

我们从未见过规模那么大、期限却又那么短的交易：合同为期三年，但双方均可在 90 天内取消——所以它实际上是一笔带自动续约的 3 个月期交易。

这种交易此前从未发生，因为极少数公司才有能力做。融资负担把所有新兴 GPU 云挡在这个市场之外——对大型集群而言，它们需要锁定多年期承购方。前三大超大规模云厂商本可以做……但它们都看到了价值更高的长期选项：例如 Microsoft 以股权投资与算力换取 OpenAI 的 IP，Amazon 专注于提升 Bedrock 和 Trainium 的采用，Google 则同样押注 TPU 和 Vertex（现为 Gemini 企业平台）。

这实际上只剩下两家公司能真正吃下这个新市场：Oracle 和 Meta。对前者而言，我们认为这是一记重击。这再次证明：Oracle 本可以把手中的数吉瓦算力变现得漂亮得多。对比 Oracle 与 SpaceX 的估值轨迹，就能看到巨大的分化。对这两家公司而言，吉瓦算力在估值中的占比都在上升，也是过去一年这一演变的重要驱动力。

![](https://substack-post-media.s3.amazonaws.com/public/images/ab482cff-30fe-4058-bb0d-20853d67f43d_2206x1228.png)
*来源：SemiAnalysis、SEC、CNBC/Bloomberg/Reuters*

现在轮到 Meta 登场。由于 Meta 全神贯注于打造超级智能，它此前大概没在云这个选项上花足够心思。SpaceX 和 Elon 为它铺平了道路。按每吉瓦 $50B 年收入计算，这是一个轻松的决策。只需把 200MW 算力分配给一个外部客户，就能带来 $10B/年的收入，而且利润率高耸入云。而 90 天内可取消合同的能力让这一切更加轻松——如果想给 MSL 更多算力，短期通知即可收回。

这也与 Meta 的数据中心建设策略完美契合。一年前，我们率先跟踪到他们全新的"帐篷（tent）"超高速数据中心设计。此后，Meta 帐篷式数据中心已在美国遍地开花！通过快速让数据中心上线——哪怕"品质较低"——Meta 将更容易以 SpaceX 的方式变现算力。

![](https://substack-post-media.s3.amazonaws.com/public/images/a13793d8-3d5d-479e-8606-ea9d08e65472_2000x1400.png)
*来源：SemiAnalysis 数据中心模型*

因此，我们预计 Meta 很快就会宣布这样一笔交易。这是启动飞轮的绝佳方式。Anthropic 是我们的头号猜测对象，但其他玩家也可能入局，比如 OpenAI 或 Google。

# Meta 会打造新的 Bedrock 吗？

Meta 的另一个绝佳选项，是与前沿实验室达成深度合作，用 Meta 自家算力销售对方的模型。如前所述，我们相信 Meta 正与 Anthropic 进行最终阶段谈判，以获得其 LLM 的私有访问权，就像 Amazon 通过 Bedrock 获得的那样（[协议详解见此文](https://newsletter.semianalysis.com/p/anthropic-growth-and-bedrock-mix)）。这意味着，对 Meta 而言，变现算力的另一条路就是销售 Claude。我们看到三条主要路径：

1. 其中一部分可能仅限内部使用。Meta 需要 Claude token，而 Anthropic 的供给跟不上需求。此外还有安全与隐私层面的考量。未来，我们可能看到其他超大型企业达成类似交易——例如摩根大通（JPMorgan）如果拿不到私有实例（部署在自己数据中心内）所带来的安全与隐私保障，大概不会全面押注 Claude。
2. Meta 可以像 Bedrock 那样把 Claude 作为服务来销售。他们有产能，且拥有从 CPU 到 GPU 再到网络的完整技术栈，安全性高。不过，作为新入局者，要建立起 AWS 那样的全部企业客户关系并不容易。但 Meta 可以选择利用其广告主客户群，把前沿智能体和 LLM 更好地集成到自家产品套件中，开辟一条全新的大规模分发路径。
3. Meta 还可以更进一步垂直整合，开始自建应用。作为全球最大的广告平台之一，他们有条件打造一个销售与营销巨头。整合前沿模型与智能体，将提高其构建世界级解决方案的胜算。

当然，还有机会把模型分发给免费社交媒体用户，以及更广阔的 Meta 生态系统，包括智能眼镜之类的产品。看起来它们更可能优先使用自有模型，但保留这种选择权是好事，而且它们大概率有一条绝佳的变现路径。庞大的分发潜力与网络效应意味着，OpenAI 和 Anthropic 等公司很可能将其视为高度战略性的机会，并准备做出让步以分一杯羹。

# 扩展广告推荐系统：Meta 还能加速多少？

对 Meta 而言，核心的 AI 叙事是推荐系统如何在超大规模上贡献营收加速。2022 年末和 2023 年初，市场普遍认为这家公司正处于投资周期中的成熟与低增长阶段。今天，情况已经一清二楚：Meta 的营收增长大幅再加速，这在很大程度上要归功于 GPU 投资。GPU 在训练和推理两端都是关键触发因素：广告推荐系统模型越做越大、运行成本越来越高，但也聪明得多，为广告主带来更好的收益——体现在广告主愿意支付更高价格的同时仍能获得强劲的 ROAS（广告支出回报率）。与此同时，内容推荐系统模型让整个应用家族（Family of Apps）的用户使用时长增加，扩大了可变现的曝光面，带动广告展示量强劲增长。

![](https://substack-post-media.s3.amazonaws.com/public/images/7c13423d-c5cc-47d7-86b5-f5046464b54e_1247x664.png)
*来源：SemiAnalysis Tokenomics 模型*

现在所有人心中最大的疑问是——这可持续吗？Meta 还能把核心营收增长再加速多少？虽然 Meta 在前沿实验室这条战线上仍在追赶，但其非超级智能（non-MSL）AI 芯片机队正产生出色的 ROI。我们在 Tokenomics 模型中覆盖了这一算力划分：RecSys AI、Meta 超级智能与其他 Meta LLM 产品各占多少。

在付费墙之后，我们将讨论 RecSys 扩展的前景，随后是 Meta 超级智能实验室（MSL）的前景。
