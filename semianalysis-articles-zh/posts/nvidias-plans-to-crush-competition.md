---
title: "NVIDIA 的剿灭竞争计划——B100、「X100」、H200、224G SerDes、OCS、CPO、PCIe 7.0、HBM3E"
title_en: "Nvidia’s Plans To Crush Competition – B100, “X100”, H200, 224G SerDes, OCS, CPO, PCIe 7.0, HBM3E"
subtitle: "路线图、供应、反竞争争议：AMD、Broadcom、Google、Amazon 和 Microsoft 任重道远"
date: 2023-10-10
source: https://newsletter.semianalysis.com/p/nvidias-plans-to-crush-competition
crawled: 2026-09-15
authors: ["Dylan Patel", "Myron Xie"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# NVIDIA 的剿灭竞争计划——B100、「X100」、H200、224G SerDes、OCS、CPO、PCIe 7.0、HBM3E

> 原文：[Nvidia’s Plans To Crush Competition – B100, “X100”, H200, 224G SerDes, OCS, CPO, PCIe 7.0, HBM3E](https://newsletter.semianalysis.com/p/nvidias-plans-to-crush-competition) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**路线图、供应、反竞争争议：AMD、Broadcom、Google、Amazon 和 Microsoft 任重道远**

NVIDIA 的 AI 解决方案当前冠绝全球，但颠覆正在逼近。Google 已经启动了[史无前例的自建 AI 基础设施计划](https://www.semianalysis.com/p/broadcoms-google-tpu-revenue-explosion)。我们独家详细披露过 Google TPUv5 与 TPUv5e 建设的[出货量](https://www.semianalysis.com/p/google-gemini-eats-the-world-gemini)和[金额](https://www.semianalysis.com/p/broadcoms-google-tpu-revenue-explosion)——既用于其内部训练/推理，也供[外部客户](https://www.semianalysis.com/p/google-gemini-eats-the-world-gemini)使用，客户包括 [Apple](https://stratechery.com/2023/an-interview-with-doug-olaughlin-and-dylan-patel-about-semiconductors-and-ai/)、Anthropic、CharacterAI、MidJourney、Assembly、Gridspace 等。

Google 并非 NVIDIA 在 AI 基础设施统治地位面临的唯一威胁。软件层面，[Meta 的 PyTorch 2.0 与 OpenAI Triton](https://www.semianalysis.com/p/nvidiaopenaitritonpytorch) 正高歌猛进，让其他硬件厂商得以被赋能。

AMD 的 GPU、Intel 的 Gaudi、Meta 的 MTIA、Microsoft 的 Athena 软件栈成熟度各不相同，但趋势已经很清楚：软件差距虽然仍然存在，却已远不如过去那般悬殊。虽然 NVIDIA 仍保持硬件领先，但这一点也很快会被追平。AMD 的 MI300 和 Intel 的 Gaudi 3 都将在未来几个月内发布，就硬件规格而言在技术上优于 NVIDIA 的 H100。

即便在 Google、AMD 和 Intel 之外，NVIDIA 还面临另一类竞争压力：这些公司的硬件设计虽落后，但背后有巨头补贴撑腰，试图摆脱 NVIDIA 在 HBM 上的层层加价。Amazon 即将推出 [Trainium2 和 Inferentia3](https://www.semianalysis.com/p/amazon-anthropic-poison-pill-or-empire)，Microsoft 也很快发布 [Athena](https://www.semianalysis.com/p/ai-capacity-constraints-cowos-and)。我们 7 月分析过[它们的供应链与明年出货量](https://www.semianalysis.com/p/ai-capacity-constraints-cowos-and)，而且这些是多年期投资，今后不会放缓。

NVIDIA 多年前就看到了不祥之兆。科技巨头们一直试图把所有硬件需求内部化，抢走 NVIDIA 的午餐。

**从这个视角看，「NVIDIA 将因这一竞争威胁而无法维持市场份额或利润率」是一个非常有理有据的论点，值得倾听。**

当然，NVIDIA 并没有坐以待毙。NVIDIA 极其成功，同时也是业内最偏执的公司之一——从管理风格到路线图决策皆是如此。黄仁勋身上体现着安迪·格鲁夫（Andy Grove）的精神。

> 成功滋生自满，自满滋生失败。只有偏执狂才能生存。
>
> Andy Grove

因此，NVIDIA 启动了一套非常雄心勃勃且高风险的多线战略，以保住 AI 硬件市场之巅。NVIDIA 的计划是超越与 Intel、AMD 等传统对手的比较，跃升为科技巨头之列——成为 Google、Microsoft、Amazon、Meta 和 Apple 的同侪。[NVIDIA 的 DGX Cloud](https://www.semianalysis.com/i/137441303/nvidias-dgx-cloud-business-model-software-as-a-service)、[软件](https://www.semianalysis.com/i/137441303/nvidias-healthcare-push-a-front-row-seat)以及[非半导体收购战略](https://www.semianalysis.com/p/nvidia-buys-illumina-the-ai-foundry)值得密切关注。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

本报告将剖析 NVIDIA 的这一多面战略，重点是其未来几年的硬件路线图，包括即将推出的 H200、B100 和「X100」GPU。NVIDIA 把 AI GPU 改为每年更新，意义重大且影响深远。我们将讨论 NVIDIA 的工艺技术规划、HBM3E 速度/容量、PCIe 6.0、PCIe 7.0，以及雄心惊人的 NVLink 与 1.6T 224G SerDes 计划。如果该计划成功，NVIDIA 将把所有人远远甩开。

我们还将讨论竞争格局以及 AMD MI300 的大单。也会谈到 AMD 已取消的 MI350X 与未来的 MI400，以及其他竞争芯片，如 Amazon 的 Trainium2、Microsoft 的 Athena 和 Intel 的 Gaudi 3。

还有一个重要话题是 NVIDIA 的商业手法——在销售策略与捆绑方面，有些人甚至可能视之为反竞争。NVIDIA 的战略采购同样精彩：供应商管理、CoWoS/HBM 产能锁定，以及光交换与共封装光学等专用技术的开发。

![](https://substack-post-media.s3.amazonaws.com/public/images/486c51a2-195a-4d4a-ba7a-281140c9bf64_2208x1230.png)
*NVIDIA 幻灯片*

以路线图为核心的讨论将更深入技术与竞争态势，先从 NVIDIA 的供应链掌控力与商业手法讲起。

## **供应链掌控——黄仁勋永远豪赌**

我们真正敬佩 NVIDIA 的一点是：他们是供应链管理大师。他们已多次证明，自己能在缺货时期创造性地扩大供应。

NVIDIA 通过承诺不可取消订单、甚至提前预付款，锁定了巨额供应。NVIDIA 拥有[111.15 亿美元的采购承诺、产能义务与库存义务](https://s201.q4cdn.com/141608511/files/doc_financials/2024/Q2FY24/Q2FY24-CFO-Commentary.pdf)，[另有 38.1 亿美元的预付供应协议](https://s201.q4cdn.com/141608511/files/doc_financials/2024/Q2FY24/Q2FY24-CFO-Commentary.pdf)。没有其他厂商望其项背，因此它们无法参与眼下这场狂热。

自 NVIDIA 早期起，黄仁勋就在供应链上采取激进策略，以支撑 NVIDIA 的庞大增长野心。只需听听黄仁勋讲述他早年与台积电创始人张忠谋的会面。

> 1997 年，Morris 和我见面时，NVIDIA 那一年的营收是 2,700 万美元。我们只有 100 个人，然后我们见面了——你们可能不信——Morris 当年可是会亲自跑销售的。你以前会亲自上门拜访客户，对吧？你会来拜访客户，我会向 Morris 解释 NVIDIA 是做什么的，我会解释我们的裸片面积需要多大，而且每一年都会变得越来越大、越来越大。你会定期回 NVIDIA 来，让我把故事再讲一遍，确保我真的需要那么多晶圆。第二年，我们开始与台积电合作。NVIDIA 的营收好像是做到了 1.27 亿美元，从那以后，我们几乎每年增长 100%，一直到现在。我是说，我们过去 10 年的复合年增长率是 70% 多。
>
> [黄仁勋与张忠谋对谈，计算机历史博物馆，2007](https://www.youtube.com/watch?v=u-x7PdnvCyI)

![](https://substack-post-media.s3.amazonaws.com/public/images/8278a1db-d3ba-407c-8652-294fbc3b2e7c_3600x1685.jpeg)
*NVIDIA 委托创作的漫画，纪念张忠谋荣退，完整版见此处*

张忠谋当时难以相信 NVIDIA 需要这么多晶圆，但黄仁勋坚持了下来，并抓住了当时游戏产业的爆发式增长。NVIDIA 靠[在供应上下重注](https://www.semianalysis.com/p/nvidias-ramp-volume-asp-cloud-pricing)取得了巨大成功，而且通常都赌对了。当然，他们时不时也得[计提数十亿美元的库存减值](https://nvidianews.nvidia.com/news/nvidia-announces-preliminary-financial-resultsfor-second-quarter-fiscal-2023)，但超额下单的账算下来仍然是净赚。既然有效，为什么要改？

这一轮，NVIDIA 揽下了 GPU 上游组件的大部分供应，包括 SK 海力士、三星和美光的 HBM。他们向全部三家 HBM 供应商都下了巨额订单，把除 [Broadcom/Google](https://www.semianalysis.com/p/broadcoms-google-tpu-revenue-explosion) 之外的供应链上其他买家的货源挤占殆尽。HBM3E 的更多内容将在路线图部分讨论。

NVIDIA 买断了台积电 CoWoS 供应的大头。他们还不止于此：又主动出击，调查并买断了 Amkor 的产能。我们已在[此处](https://www.semianalysis.com/p/ai-capacity-constraints-cowos-and)详细分析。

我们向客户提供/出售的详细模型之一，是一个按季度推演 NVIDIA、Alchip、Marvell、Broadcom、Microsoft、AMD、Cisco、T-head、Sanechips、Renesas 和 GUC 的 HBM 与 CoWoS 产能的数据库。它涵盖每片晶圆裸片数、良率、HBM 出货量、加速器出货量、ASP 及所有主要硬件厂商和超大规模云厂商芯片的营收。这些数据来自各公司、服务器 ODM、代工厂、基板供应商，以及 [HBM 和 CoWoS 制造供应链上 28 家不同的设备供应商](https://www.semianalysis.com/p/ai-expansion-supply-chain-analysis)。

NVIDIA 还锁定了其 HGX 板卡或服务器所需的大量下游组件，如重定时器（retimer）、DSP、光模块等。对 NVIDIA 的要求犹豫不决的供应商，通常会得到胡萝卜加大棒的待遇：一边是看似难以想象的海量订单，另一边是被从 NVIDIA 现有供应链中设计出局的风险。只有当供应商至关重要、无法被设计出局或多元采购时，NVIDIA 才会动用承诺性采购和不可取消订单。

每个供应商似乎都觉得自己是 AI 赢家，部分原因正是 NVIDIA 在向所有人大举下单，而他们都以为自己在其中赢得了大头——但实际上，那是因为 NVIDIA 的爬坡速度实在太快。

回到上述市场格局：NVIDIA 明年目标是拥有超过 700 亿美元数据中心销售的供应量，而只有 Google 在上游拥有足够产能，能做出超过 100 万颗量级的规模。即便 AMD 最近上调了产能规划，其 AI 总产能仍然非常有限，最多也就二十万颗出头。

## **商业手法——或涉反竞争**

NVIDIA 借 GPU 的旺盛需求向上交叉销售（upsell/cross-sell），这早已不是秘密。供应链众多信源告诉我们，NVIDIA 正基于一系列因素给予优先配给，包括但不限于：多元化采购计划、自研 AI 芯片的计划、[购买 NVIDIA 的 DGX](https://www.semianalysis.com/p/nvidias-ramp-volume-asp-cloud-pricing)、NIC、[交换机](https://www.semianalysis.com/p/nvidias-infiniband-problem-qmx-ai)和/或[光模块](https://www.semianalysis.com/p/nvidias-optical-ascent-1b-revenue)。我们在[3 月的 Amazon 云危机报告](https://www.semianalysis.com/p/amazons-cloud-crisis-how-aws-will)中详细分析过。

CoreWeave、Equinix、Oracle、AppliedDigital、Lambda Labs、Omniva、Foundry、Crusoe Cloud、Cirrascale 等基础设施提供商，正被配给大炮对准——它们拿到的量远比 Amazon 等科技巨头更接近其潜在需求。

NVIDIA 的捆绑战术极其成功：虽然此前在光收发器市场只是很小的供应商，[但他们一个季度内业务翻了三倍，未来一年出货有望超过 10 亿美元](https://www.semianalysis.com/p/nvidias-optical-ascent-1b-revenue)。这远超其 GPU 或网络芯片业务的增速。

这些手法都经过精心设计。例如当前，在 NVIDIA 系统上实现可靠 RDMA/RoCE 的 3.2T 网络，唯一途径就是用 NVIDIA 的 NIC。这主要归因于 Intel、AMD 和 Broadcom 缺乏竞争力——它们还停留在 200G。

NVIDIA 还见缝插针地管理供应链，使其 400G InfiniBand NIC 的交期明显短于 400G 以太网 NIC。要知道，这两款 NIC（ConnectX-7）的芯片和板卡设计完全相同。这主要源于 NVIDIA 的 SKU 配置策略，而非真实的供应链瓶颈。这就迫使客户购买 NVIDIA 更昂贵的 InfiniBand 交换机，而不是标准以太网交换机。唯一的例外是当你购买其 Spectrum-X 以太网络、配以 NIC 模式的 Bluefield-3 DPU 时。

还不止这些。看看[供应链对 L40 和 L40S GPU 有多么陶醉](https://www.semianalysis.com/i/136248981/l-overhyped)吧。我们[在此文](https://www.semianalysis.com/i/136248981/l-overhyped)写过这个问题，此后我们又听到了更多 NVIDIA 配给上的把戏。

OEM 厂商想要拿到更大的 H100 配额，NVIDIA 就力推 L40S。这些 OEM 承受着买更多 L40S 的压力，作为回报获得更好的 H100 配给。这与 NVIDIA 当年在 PC 市场玩的是同一套游戏：笔记本厂商和 AIB 合作伙伴必须大批采购 G106/G107（中低端 GPU），才能拿到更稀缺、利润更高的 G102/G104（高端与旗舰 GPU）的好配额。

台湾供应链中的许多人被灌输了一种叙事：L40S 优于 A100，因为 FLOPS 更高。必须说清楚：这些 GPU 不适合 LLM 推理，因为它们的内存带宽不到 A100 的一半，且没有 NVLink。这意味着，除极小模型外，在这些 GPU 上以良好 TCO 跑 LLM 几乎不可能。大批量下每用户 token 数（tokens/second/user）令人无法接受，使理论 FLOPS 对 LLM 在实践中毫无用处。

OEM 还被施压支持 NVIDIA 的 MGX 模块化服务器设计平台。这实际上把服务器设计的全部苦活都拿掉了，但同时也将其商品化，制造更多竞争、压低 OEM 利润。Dell、HPE、Lenovo 等公司显然抵制 MGX，但台湾的低成本厂商如 SuperMicro、Quanta、华硕（Asus）、技嘉（Gigabyte）、和硕（Pegatron）、ASRock 正蜂拥填补这一空缺，把低成本「企业级 AI」商品化。

方便得很，这些参与 L40S 和 MGX 炒作游戏的 OEM/ODM，也拿到了 NVIDIA 主力 GPU 产品好得多的配额。

## **路线图——B100、「X100」、H200、HBM3E、200G SerDes、PCIe 6.0、共封装光学、光交换**

本报告的主体是 NVIDIA 新路线图的 juicy 细节，包括所用的网络、内存、封装与工艺节点，各款 GPU、SerDes 选择、PCIe 6.0、共封装光学与光电路交换机。内容不止下面这一张幻灯片。

![](https://substack-post-media.s3.amazonaws.com/public/images/5a6a32a8-52e5-4797-afe8-ed85dcb37937_2208x1230.png)

由于 Google、Amazon、Microsoft、AMD 和 Intel 的竞争压力，我们认为 NVIDIA 加速了 B100 和「X100」的计划。作为对 NVIDIA 加速时间表的回应，我们听说 AMD 彻底取消了 MI350X 计划。回到我们[独家详细披露的 MI300 配置](https://www.semianalysis.com/p/amd-mi300-taming-the-hype-ai-performance)的技术规格。

模块化的 XCD 构建块为 40 个 CU，采用台积电 5nm 工艺。AMD 原有的 MI350X 使用相同的 AID，但 XCD 不同，采用台积电 3nm。该部件因多种原因被取消，其中之一是：对比两者的纸面规格，它与 B100 相比将完全没有竞争力。

[获取团体订阅 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
