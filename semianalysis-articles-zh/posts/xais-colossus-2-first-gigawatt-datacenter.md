---
title: "xAI 的 Colossus 2——全球首座吉瓦级数据中心、独特 RL 方法论与融资"
title_en: "xAI's Colossus 2 - First Gigawatt Datacenter In The World, Unique RL Methodology, Capital Raise"
subtitle: "现场燃气轮机、密西西比扩张、Solaris Energy、xAI 付得起吗？、中东资金、Tesla、人才流失、API 收入、消费者增长、RL 环境"
date: 2025-09-16
source: https://newsletter.semianalysis.com/p/xais-colossus-2-first-gigawatt-datacenter
crawled: 2026-09-15
authors: ["Jeremie Eliahou Ontiveros", "Dylan Patel", "Wei Zhou", "AJ", "Maya Barkin"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# xAI 的 Colossus 2——全球首座吉瓦级数据中心、独特 RL 方法论与融资

> 原文：[xAI's Colossus 2 - First Gigawatt Datacenter In The World, Unique RL Methodology, Capital Raise](https://newsletter.semianalysis.com/p/xais-colossus-2-first-gigawatt-datacenter) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**现场燃气轮机、密西西比扩张、Solaris Energy、xAI 付得起吗？、中东资金、Tesla、人才流失、API 收入、消费者增长、RL 环境**

关于 xAI 的 Colossus 1，外界已经写得很多。孟菲斯的这项建设足以载入史册：全球最大的 AI 训练集群，从零起步仅用 122 天建成。拥有约 200,000 颗 H100/H200 和约 30,000 颗 GB200 NVL72，它至今仍是全球最大的完整投运的单一致性集群（[多数据中心训练大师](https://semianalysis.com/2024/09/04/multi-datacenter-training-openais/) Google 另当别论）。

然而，与 [OpenAI](https://semianalysis.com/2025/06/30/how-oracle-is-winning-the-ai-compute-market/)、[Meta](https://semianalysis.com/2025/07/11/meta-superintelligence-leadership-compute-talent-and-data/) 和 [Anthropic](https://semianalysis.com/?p=150449616&preview=true) 正在建设中的吉瓦级集群相比，Colossus 1 的约 300 MW 就显得温和了。他们的超大规模云厂商合作伙伴乐意动用自家资产负债表，用真金白银砸开市场、赢下订单。

xAI 的强势表现只是一次性的奇迹吗？今天我们将公开部分来自我们[过去一年行业领先数据中心模型](https://semianalysis.com/datacenter-industry-model/)的数据，完整数据面向客户开放。正是这套专有数据，早在 Oracle 交易官宣数月之前就做出了预判。

![](https://substack-post-media.s3.amazonaws.com/public/images/d6c5b75b-df0f-4ba0-a9f9-0aa1e6380ec0_1024x552.png)
*来源：SemiAnalysis 数据中心行业模型——注：数据中心投运与 GPU 投运之间存在时间差；Google 及确切数字可在模型中查看*

**简短回答：不是**。xAI 仍稳稳身处前沿 AI 竞赛之中，且有望在算力上再次超越大多数对手。据我们估计，到 2025 年第三季度，其单个训练集群的总数据中心容量将超过 Meta Superintelligence 和 Anthropic。数据中心容量将就绪，等待 GPU 搬入，再次打造出全球最大的单一数据中心。xAI 必须为这些 GPU 募集资金，但他们已拿到 NVIDIA 的产能配给，可以在明年初全面开跑大规模模型训练。

Elon 想出了**一个新的天才招数**，在上市时间上击败对手。Colossus 2 将比 xAI 的第一个集群更令人惊叹。让我们深入一探。

本报告前半部分将深挖 Colossus 2 的实力。后半部分将讨论 Grok 模型、我们对 xAI 的中长期看法，以及 xAI 正在使用的可能使其反超 OpenAI、Anthropic 和 Google 的**独特 RL 方法**。

---

## SemiAnalysis 正在招聘

我们正在寻找一位高度自我驱动、技术过硬的技术团队成员（Member of Technical Staff），加入我们不断成长的特别项目工程团队。你将在开发行业领先的 GPU 云基准测试与评估框架中扮演关键角色。我们的 GPU 云评估框架已获得许多一级和二级前沿实验室的背书。如果你具备以下经验，可能非常适合这个职位：

- 通过工作经历、个人项目或个人 Substack 博客，展示过使用 PyTorch 或 JAX 等 ML 框架的经验
- 1-2 年使用 GPU 或 TPU 集群和/或运维多租户 GPU 集群的经验
- 曾在超大规模云厂商或 GPU 云工作过（优先）
- 对 SLURM、Kubernetes、NCCL 及 GPU 云行业有扎实理解
- 较强的研究能力，能够综合多来源信息得出洞察

薪酬具有竞争力；作为面试流程的一部分，你将完成一项带薪编程挑战，其设计贴近 SemiAnalysis 的典型日常工作

[在此申请](https://app.dover.com/apply/SemiAnalysis/f4631653-e731-4e16-823b-eec3c5d90eba/?rs=76643084)

---

## Colossus 2：六个月从零到 200MW

Colossus 2 项目于 2025 年 3 月 7 日启动，当天 xAI 收购了孟菲斯一座 100 万平方英尺的仓库，以及两处相邻、合计 100 英亩的地块。到 2025 年 8 月 22 日，我们在现场清点到 119 台风冷冷水机组，即[约 200MW 制冷容量](https://semianalysis.com/2025/02/13/datacenter-anatomy-part-2-cooling-systems/#air-cooled-and-water-cooled-chillers)。这足以支撑约 110k 颗 GB200 NVL72。而 [Elon 的一条推文](https://x.com/elonmusk/status/1947715674429919279)显示 7 月就已有机柜完成安装。

xAI 用六个月建成了 [Oracle、Crusoe 和 OpenAI 花 15 个月才完成的建设！](https://semianalysis.com/datacenter-industry-model/)

![](https://substack-post-media.s3.amazonaws.com/public/images/5eee61f4-1b16-4664-966a-e07eae116158_1024x832.png)
*来源：SemiAnalysis 数据中心行业模型*

细看上图，[熟悉我们数据中心解剖（Datacenter Anatomy）系列的读者](https://semianalysis.com/2024/10/14/datacenter-anatomy-part-1-electrical/)可能会疑惑：电力基础设施在哪里？图中既看不到现场变电站，也看不到现场燃气轮机……这座数据中心到底靠什么供电？

## Colossus 2：在田纳西、密西西比……还是两地兼有？

再把[大孟菲斯商会 5 月的一份声明](https://www.actionnews5.com/2025/07/22/xai-begins-installing-computing-infrastructure-colossus-2/#:~:text=Colossus%202%20is%20expected%20to,within%20the%20next%20few%20weeks)考虑进来，事情就更加扑朔迷离了：**孟菲斯境内不会设置任何燃气轮机**。他们没有说谎。

孟菲斯和田纳西州方面一直承受大量阻力，于是 xAI 的天才一招是把吉瓦级能源枢纽建在**州界正对面**的**密西西比州 Southaven**。2025 年年中，公司收购了 Southaven 一座 Duke Energy 的退役电厂。此后不久，**密西西比州**监管机构[批准](https://512pixels.net/2025/08/xai-turbines-southaven/#:~:text=,the%20Mississippi%20Public%20Records%20Act) xAI 在无许可证的情况下临时运行燃气轮机，为期最长 12 个月！

![](https://substack-post-media.s3.amazonaws.com/public/images/052bac5a-a53f-4054-ac0d-574181eb0481_712x1024.png)
*来源：SemiAnalysis 数据中心行业模型*

为了输送和管理密西西比电厂发出的电力，xAI 正在 Colossus 2 附近建设基础设施。下图展示了首批部署的 Tesla Megapack，以及连接两处场地的中压电力线路。

![](https://substack-post-media.s3.amazonaws.com/public/images/c6d8454a-f182-4bb1-abc1-7293803e7ea5_1024x938.png)
*来源：SemiAnalysis 数据中心行业模型*

## 从 200MW 到 1.1GW 与 Solaris Energy Infrastructure 的合作

在密西西比州 Southaven，xAI 正在以光速推进。这座退役电厂如今已有七台 35MW 燃气轮机投运。

![](https://substack-post-media.s3.amazonaws.com/public/images/c5f17aae-5cff-4c9d-94e3-fd79422fd36d_1024x542.png)
*来源：SemiAnalysis 数据中心行业模型*

为了比同行更快部署，xAI 依赖燃气轮机租赁公司。纽交所上市的 Solaris Energy Infrastructure 拥有一支 600MW 的燃气轮机机队，其中约 400MW 目前服务于 xAI。马斯克的公司占 SEI 1700MW 在手订单的 67%，即 1,140MW。其中约 240MW 位于孟菲斯 Colossus 1 场地，其余 900MW 将由一家 Solaris 持股 50.1%、xAI 持股 49.9% 的合资公司持有。

![](https://substack-post-media.s3.amazonaws.com/public/images/01fbd1e6-74c2-4155-887c-9a58369984fd_1024x451.png)
*来源：Solaris Energy Infrastructure*

如下图所示，目前约 460MW 已安装并投运/在建。

![](https://substack-post-media.s3.amazonaws.com/public/images/40744dbf-04f6-4852-b56e-5e05f66c087d_1024x555.png)
*来源：SemiAnalysis 数据中心行业模型*

这家新组建的合资公司在 2025 年第二季度已投入 1.12 亿美元资本开支。经历缓慢的第三季度后，支出将在 2025 年第四季度和 2026 年第一季度再度加速。Solaris 预计到 2027 年第二季度将为 xAI 提供超过 1.1GW 完整投运的燃气轮机。目前还剩约 425MW 可供签约，我们认为 xAI 很可能会果断出手，把总毛电力推到 1.5GW 以上。Solaris 似乎还在临时从第三方租赁发电产能，以加快交付：

> *"第二季度，Power Solutions 板块从约 600 兆瓦容量中产生营收，环比增长超过 50%。这一增长由客户需求上升驱动，我们正通过新设备交付与**选择性短期采购第三方发电产能**相结合的方式来满足需求。"*

——Solaris Energy Infrastructure，2025 年第二季度

![](https://substack-post-media.s3.amazonaws.com/public/images/fab97fc5-05b0-4883-9245-d991eeecd62c_1024x549.png)
*来源：Solaris Energy Infrastructure*

如此一来，xAI 已经从电力角度解决了扩展到 1GW 以上的问题。在数据中心空间方面，我们看到四种选择：

- 考虑到 40 英尺的层高，xAI 可以把 100 万平方英尺的仓库改造成两层数据中心，空间翻倍。按超高功率密度计算，200 万平方英尺可能就足以支撑 1GW 以上。
- xAI 可以在 3 号地块（parcel 3）新建第二座较小的设施
- 他们可以收购更多土地，可能在密西西比州、靠近 Southaven 电厂之处。
- 采用非标准的数据中心布局，现有场地即可实现 1GW 以上。

![](https://substack-post-media.s3.amazonaws.com/public/images/d2988a90-87eb-4331-a916-069a859b210a_1024x736.png)
*xAI 在 Colossus 2 场地所持的各地块（parcels）*

## xAI 付得起 Colossus 2 吗？

进一步扩张需要充足资金。Colossus 2 所需资本开支将以数百亿美元计，而 xAI 尚未产生任何有意义的外部收入——传闻中九位数 ARR 营收的绝大部分，其实是 X.com 向 xAI 的内部转移。我们已在机构研究服务 [Core Research](https://semianalysis.com/core-research/) 中对 xAI 的资本开支做了预测，并正在通过我们的[新 Tokenomics 模型](https://semianalysis.com/tokenomics-model/)密切追踪各超大规模云厂商与 AI 实验室 AI 投资的 ROIC。

![](https://substack-post-media.s3.amazonaws.com/public/images/74fb771a-5d3d-4b0b-9927-1f645de02c10_1024x512.png)
*来源：SemiAnalysis Tokenomics 模型估算*

### 中东——资金 + 数据中心，制胜组合？

需要说明的是，以 xAI 和 Elon 的一贯风格，这家公司的未来高度不可预测。但考虑到资金需求，我们认为其在中东进行大规模扩张的可能性很大。马斯克与中东的关系由来已久：

- 沙特阿拉伯的 Kingdom Holding Company（公共投资基金持股 16.87%）在马斯克 2022 年将 Twitter 私有化时，持有并继续保留了 $1.9B 的 Twitter 股份。在与 X 合并之前，它还持有 xAI 的 $800M 股份。
- 阿联酋的私人资本 Vy Capital 在 2022 年为支持 Elon 收购 Twitter 出资 $700M。它还与阿联酋国家基金 MGX 一道投资了 xAI 的 C 轮。
- 卡塔尔的 QIA 也持有并保留了 Twitter 的 $375M 股份，并参与了 xAI 的 C 轮融资。

[据 FT 报道](https://www.reuters.com/business/musks-xai-seeks-up-200-billion-valuation-next-fundraising-ft-reports-2025-07-11/#:~:text=Saudi%20Arabia%27s%20PIF%20sovereign%20wealth,million%20investment%20in%20the%20firm)，xAI 正在准备一轮数百亿美元的新融资，估值接近 $200B，沙特主权财富基金 PIF 将扮演重要角色。不过这颇具挑战，因为对多数投资者而言，很难为 xAI 给出高于 Anthropic 的估值找到合理依据。

我们听说融资规模最高可达 $40B。鉴于该地区数据中心需求暴涨，我们认为很可能达成双向交易：xAI 将这笔资金投入到沙特王国境内一座全新的大规模数据中心。

![](https://substack-post-media.s3.amazonaws.com/public/images/c454a625-3380-422c-ad7d-a771c7b72e53_1024x526.png)
*来源：SemiAnalysis 数据中心行业模型*

下图展示了 xAI 扩张的一个可能选址：沙特阿拉伯一处近期破土动工的大型规划园区。尽管为时尚早，那里有充裕的土地和电力，足以支撑大规模 AI 园区。

![](https://substack-post-media.s3.amazonaws.com/public/images/b167e795-070a-421b-90f7-b1bd87de76fc_1024x452.png)
*来源：SemiAnalysis 数据中心行业模型*

关于中东 AI 扩张的更多细节，请参阅我们 2025 年 5 月的深度解析。

除了外部资本，Elon 还可以在内部生成资本。自 X.com 与 xAI 合并组建 X Holdings 以来，我们认为 xAI 营收中不断增大的一块是公司间转移，即调用 @Grok 回答问题，或 X.com 为搜索、广告推荐系统乃至内容创作等功能授权使用该 LLM 技术。

这不过是把钱从 Elon 的右口袋挪到左口袋。从我们外部可追踪的数据看，Ani 曾极大提振 Grok 应用收入，但即便这条收入流的增长近几个月也已趋平。Ani 需要更多抽卡（gacha）内容才能进一步拉动收入。

![](https://substack-post-media.s3.amazonaws.com/public/images/dbaaab2c-2842-4779-be4f-6fa4bcfb959b_1024x512.png)
*来源：SemiAnalysis 估算与 Sensortower*

归根结底，Elon 可以让 Tesla 增加投资，或以更多 Tesla 和 SpaceX 股票质押贷款，向 xAI 投入数百亿美元。这将让他们有能力建成 Colossus 2。没有人真正知道 Elon 目前的杠杆有多高，但外界普遍认为，他随时可以出售股票，把更多「干火药」解锁投入 xAI。Elon 会竭尽所能不输给 Sam Altman。

现在来讨论作为一门生意的 xAI，以及我们认为这家公司有没有机会成为前沿 AI 实验室、撑起数千亿美元的估值。下文我们掌握一些独特的信息与洞察，并解释为什么凭借与众不同的路径，他们有机会率先抵达 AGI。

## xAI 有机会成为前沿实验室吗？
