---
title: "NVIDIA 的圣诞礼物：GB300 与 B300——推理模型推理、Amazon、内存与供应链"
title_en: "Nvidia's Christmas Present: GB300 & B300 - Reasoning Inference, Amazon, Memory, Supply Chain"
subtitle: "Blackwell 延期、Microsoft 订单、GB300 物料清单（BOM）、NVIDIA 毛利率、ConnectX-8、VRM、美光（Micron）、三星（Samsung）、SK Hynix、纬创（Wistron）、FII 富士康、Aspeed、Axiado"
date: 2024-12-25
source: https://newsletter.semianalysis.com/p/nvidias-christmas-present-gb300-b300-reasoning-inference-amazon-memory-supply-chain
crawled: 2026-09-15
authors: ["Dylan Patel", "Myron Xie", "Daniel Nishball"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# NVIDIA 的圣诞礼物：GB300 与 B300——推理模型推理、Amazon、内存与供应链

> 原文：[Nvidia's Christmas Present: GB300 & B300 - Reasoning Inference, Amazon, Memory, Supply Chain](https://newsletter.semianalysis.com/p/nvidias-christmas-present-gb300-b300-reasoning-inference-amazon-memory-supply-chain) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**Blackwell 延期、Microsoft 订单、GB300 物料清单（BOM）、NVIDIA 毛利率、ConnectX-8、VRM、美光（Micron）、三星（Samsung）、SK Hynix、纬创（Wistron）、FII 富士康、Aspeed、Axiado**

圣诞快乐——这要归功于[「圣诞老人」黄仁勋](https://www.youtube.com/watch?v=5CX0OcclFvQ)。尽管 NVIDIA 的 Blackwell GPU 历经多次延期——我们曾[在此](https://semianalysis.com/2024/08/04/nvidias-blackwell-reworked-shipment/)讨论过，并因[芯片](https://semianalysis.com/2024/08/04/nvidias-blackwell-reworked-shipment/)、[封装](https://semianalysis.com/2024/08/04/nvidias-blackwell-reworked-shipment/)和[背板问题](https://www.semianalysis.com/p/accelerator-model)在 [Accelerator Model](https://www.semianalysis.com/p/accelerator-model) 中多次提及——但这丝毫没有阻挡 NVIDIA 一往无前的进击步伐。

在 GB200 和 B200 发布仅 6 个月后，NVIDIA 就要向市场推出全新 GPU——GB300 与 B300。表面听上去只是小幅迭代，但水面之下的东西远比看上去多。

这些变化之所以格外重要，是因为它们带来了[推理模型推理与训练性能的巨大提升](https://semianalysis.com/2024/12/11/scaling-laws-o1-pro-architecture-reasoning-training-infrastructure-orion-and-claude-3-5-opus-failures/)。NVIDIA 为所有超大规模云厂商——尤其是 Amazon——以及供应链上的某些玩家、内存厂商和它们的投资者准备了一份特别的圣诞礼物。随着向 B300 的切换，整条供应链都在重组与迁移：许多赢家收到礼物，也有一些输家只拿到煤块。

## **B300 与 GB300——不只是渐进式升级**

B300 GPU 是基于台积电（TSMC）4NP 制程节点的一次全新流片，也就是说，计算裸片（die）的设计经过了调整。这使得该 GPU 在产品层面相比 B200 提供**高出 50% 的 FLOPS**。部分性能提升来自 200W 的额外功耗：GB300 与 B300 HGX 的 TDP 分别提升至 1.4KW 和 1.2KW（GB200 和 B200 分别为 1.2KW 和 1KW）。

其余的性能提升则来自架构增强与系统级增强，例如 CPU 与 GPU 之间的"功率挪移"（power sloshing）。所谓功率挪移，是指 CPU 和 GPU 在运行中动态地在两者之间重新分配功率。

除了更多 FLOPS，内存也从 8 层堆叠（8-Hi）HBM3E 升级到 12 层堆叠（12-Hi）HBM3E，单颗 GPU 的 HBM 容量增至 288GB。不过引脚速率保持不变，因此单 GPU 内存带宽仍为 8TB/s。注意，三星（Samsung）这次从圣诞老人那里拿到的是煤块——至少未来 9 个月内，他们没有任何机会进入 GB200 或 GB300 的供应体系。

此外，或许是出于圣诞精神，NVIDIA 这次的定价相当有意思。这将改变 Blackwell 的利润率结构，但定价与利润率的话题留待后文。首先最重要的，是谈谈性能变化。

## **为推理模型的推理而生**

内存方面的改进，对 [OpenAI O3 式的 LLM 推理训练与推理（inference）至关重要——因为超长的序列长度会使 KV 缓存（KVCache）不断膨胀，进而限制关键的批尺寸（batch size）并推高延迟](https://semianalysis.com/2024/12/11/scaling-laws-o1-pro-architecture-reasoning-training-infrastructure-orion-and-claude-3-5-opus-failures/)。我们在[为 Scaling Laws 辩护的文章](https://semianalysis.com/2024/12/11/scaling-laws-o1-pro-architecture-reasoning-training-infrastructure-orion-and-claude-3-5-opus-failures/)中解释过这一点，其中讨论了推理模型训练、合成数据、推理等大量话题。

下图展示了 NVIDIA 当代各款 GPU 在 1k 输入 token、19k 输出 token 场景下 token 经济学（tokenomics）的改善——该场景类似于 OpenAI o1 和 o3 模型的思维链（chain of thought）。这一演示性的 roofline 仿真在 FP8 精度的 LLAMA 405B 上运行，因为它是我们能模拟的最好的公开模型；所用 GPU 为 H100 和 H200，也就是我们手头能拿到的 GPU。

![](https://substack-post-media.s3.amazonaws.com/public/images/e5e584ba-53c6-419c-9998-fa7cd319510b_1024x862.jpeg)
*来源：SemiAnalysis*

从 H100 换到 H200——这纯粹只是内存更多、更快的升级——会带来两个效果：

1. 在所有可比批尺寸下，交互性（interactivity）普遍提升 43%，得益于更高的内存带宽（H200 为 4.8TB/s，H100 为 3.35TB/s）。
2. 成本降低约 3 倍，因为 H200 能以比 H100 更高的批尺寸运行，每秒可生成的 token 数达到 3 倍。这一差异主要源于 KV 缓存对总批尺寸的限制。

更大的内存容量带来看似不成比例的巨大收益，这种动态效应的影响是惊人的。对运营商而言，这两款 GPU 之间的性能与经济性差距，远大于纸面规格所暗示的水平：

1. 推理模型的用户体验可能很差，因为从发出请求到收到响应之间等待时间很长。如果你能提供显著更快的推理耗时，将提升用户使用并为之付费的意愿。
2. 3 倍的成本差距是巨大的。仅凭一次世代中期的内存升级就让硬件带来 3 倍改善，坦率地说近乎疯狂，远超摩尔定律、黄氏定律，以及我们见过的任何一种硬件改进速度。
3. 我们观察到，最有能力、最具差异化的模型，即便只比稍弱的模型强一点，也能收取显著的溢价。前沿模型的毛利率超过 70%，而面临开源竞争的落后模型的毛利率则不到 20%。[推理模型并不局限于单一思维链。](https://semianalysis.com/2024/12/11/scaling-laws-o1-pro-architecture-reasoning-training-infrastructure-orion-and-claude-3-5-opus-failures/)搜索是存在的，并且可以像在 O1 Pro 和 O3 中那样[通过扩大搜索规模来提升性能](https://semianalysis.com/2024/12/11/scaling-laws-o1-pro-architecture-reasoning-training-infrastructure-orion-and-claude-3-5-opus-failures/)。这使得更聪明的模型能解决更多问题，并在每颗 GPU 上产生显著更高的收入。

当然，能增加内存容量的不止 NVIDIA 一家。ASIC 也能做到；事实上，凭借相对 NVIDIA 普遍更高的内存容量——MI300X 的 192GB、MI325X 的 256GB、MI350X 的 288GB——AMD 的处境可能相当不错……只不过，[「圣诞老人」黄仁勋](https://www.youtube.com/watch?v=5CX0OcclFvQ)还有一头名叫 [NVLink](https://www.youtube.com/watch?v=5CX0OcclFvQ) 的红鼻子驯鹿。

再往前走到 GB200 NVL72 和 GB300 NVL72，NVIDIA 系统的性能与成本会大幅改善。在推理中使用 NVL72 的关键在于：它能让 72 颗 GPU 以极低延迟协同处理同一个问题并共享内存。世界上没有其他任何加速器拥有全互联（all-to-all）交换式连接。世界上也没有其他任何加速器能通过交换机完成 all-reduce。

NVIDIA 的 GB200 NVL72 与 GB300 NVL72 对以下几项关键能力的实现至关重要：

1. 高得多的交互性，使每条思维链的延迟更低。
2. 用 72 颗 GPU 分摊 KV 缓存，支撑长得多的思维链（更高的智能）。
3. 相较典型的 8 GPU 服务器，批尺寸扩展性好得多，成本也就低得多。
4. 在同一问题上可以搜索多得多的样本，从而提升准确性并最终提升模型性能。

因此，NVL72 的 token 经济学改善超过 10 倍，在长推理链上尤为明显。KV 缓存吞噬内存对经济性是致命的，而 NVL72 是唯一能在高批尺寸下将推理长度扩展到 100k+ token 的途径。

## **为 GB300 而重组的 Blackwell 供应链**

到了 GB300，供应链以及 NVIDIA 供货的内容发生了剧变。在 [GB200 上，NVIDIA 提供整块 Bianca 板](https://semianalysis.com/2024/07/17/gb200-hardware-architecture-and-component/)（包括 Blackwell GPU、Grace CPU、512GB LPDDR5X，以及全部集成在一块 PCB 上的 VRM 元器件），此外还提供交换盘（switch tray）和铜背板。

![](https://substack-post-media.s3.amazonaws.com/public/images/a422b320-32ee-4ce1-aaf4-1de769fb37ed_1024x819.png)
*来源：SemiAnalysis*

在 GB300 上，NVIDIA 不再提供整块 Bianca 板，而是只提供：以"SXM Puck"模块形式交付的 B300、采用 BGA 封装的 Grace CPU，以及 HMC——后者将由美国初创公司 Axiado 提供，取代 GB200 上的 Aspeed。

终端客户现在将直接采购计算板上的其余元器件，第二层内存将改用 LPCAMM 模块，而非焊死的 LPDDR5X。美光（Micron）将是这些模块的主要供应商。

交换盘和铜背板维持不变，仍由 NVIDIA 全额供货。

![](https://substack-post-media.s3.amazonaws.com/public/images/c2addf1b-d59e-4cca-8948-622babbdca3c_1024x450.png)
*来源：SemiAnalysis*

转向 SXM Puck 为更多 OEM 和 ODM 参与计算盘（compute tray）制造打开了机会。此前只有纬创（Wistron）和 FII 能够制造 Bianca 计算板，现在更多 OEM/ODM 都可以加入。在 ODM 阵营中，纬创是最大的输家，因为其在 Bianca 板上的份额流失。对 FII（富士康）而言，Bianca 板层面的份额损失被另一个事实抵消：它是 SXM Puck 及其插座（socket）的独家制造商。NVIDIA 正试图为 Puck 和插座引入其他供应商，但目前尚未向其他任何一家下过订单。

另一个重大变化发生在 VRM 元器件上。虽然 SXM Puck 上仍有一部分 VRM，但板上 VRM 的大部分元器件将由超大规模云厂商/OEM 直接向 VRM 供应商采购。10 月 25 日，我们向 [Core Research 订阅者](https://semianalysis.com/core-research/)发送了一篇报告，讲 B300 如何围绕[电压调节模块（VRM）](https://semianalysis.com/2023/08/01/energizing-ai-power-delivery-competition/)重塑供应链。我们明确指出[Monolithic Power Systems 将因商业模式转变而丢失市场份额，以及哪些新进入者正在抢份额](https://semianalysis.com/core-research/)。在我们向客户发出报告后的一个月里，MPWR 股价下跌超过 37%，因为市场消化了我们这项领先研究揭示的事实。

NVIDIA 还在 GB300 平台上提供 800G ConnectX-8 NIC，在 InfiniBand 和以太网上提供两倍的横向扩展（scale-out）带宽。此前 NVIDIA 一度取消了 GB200 的 ConnectX-8，原因是上市时间的复杂性，以及放弃在 Bianca 板上启用 PCIe Gen 6。

ConnectX-8 相比 ConnectX-7 是一次巨大飞跃。它不仅带宽翻倍，还拥有 48 条 PCIe 通道（此前为 32 条），从而催生了[风冷 MGX B300A](https://www.semianalysis.com/p/nvidias-blackwell-reworked-shipment) 这类独特架构。此外，ConnectX-8 [原生支持 SpectrumX；而在上一代 400G](https://www.semianalysis.com/p/nvidias-infiniband-problem-qmx-ai) 上，SpectrumX 需要借助[能效低得多的 Bluefield 3 DPU](https://www.semianalysis.com/p/100000-h100-clusters-power-network)。

## **GB300 对超大规模云厂商的影响**

GB200 延期与 GB300 的接棒，对超大规模云厂商的影响是：许多原定第三季度启动的订单转到了 NVIDIA 这款更贵的新 GPU 上。截至上周，所有超大规模云厂商都已决定推进 GB300。一部分原因是 GB300 凭借更高 FLOPS 和更大内存带来了性能提升，另一部分原因则是终于能把命运掌握在自己手里。

由于上市时间的挑战以及机柜、散热、供电/功率密度的重大变化，超大规模云厂商在服务器层面几乎不被允许对 GB200 做什么改动。其结果是，Meta 放弃了从 Broadcom 和 NVIDIA 多元采购 NIC 的全部希望，转而完全依赖 NVIDIA；另一些案例中，比如 Google，则放弃了自研 NIC，只采用 NVIDIA 方案。

对超大规模云厂商里那些数千人规模的组织而言，这犹如指甲刮黑板般刺耳——他们习惯于对一切进行成本优化，从 CPU、网络设备，一直到螺丝和钣金件。

最极端的例子是 [Amazon：它选择了一套非常不理想的配置，总拥有成本（TCO）比参考设计更差](https://semianalysis.com/2024/07/17/gb200-hardware-architecture-and-component/)。具体来说，由于使用 PCIe 交换机以及需要风冷的、能效更低的 200G Elastic Fabric Adapter NIC，Amazon 无法像 Meta、Google、Microsoft、Oracle、X.AI 和 Coreweave 那样部署 NVL72 机柜。受制于自研 NIC，Amazon 只能采用 NVL36，而由于背板和交换内容更多，其单 GPU 成本反而更高。总而言之，受定制化约束所累，Amazon 的配置是次优的。

如今有了 GB300，超大规模云厂商可以定制主板、散热乃至更多环节。这使 Amazon 得以打造自己的定制主板：采用水冷，并把此前风冷的元器件（如 Astera Labs 的 PCIe 交换芯片）集成进来。对更多元器件实施水冷，加上 K2V6 400G NIC 终于在 2025 年三季度进入高量产（HVM），意味着 Amazon 可以重回 NVL72 架构，大幅改善其 TCO。

但有一个很大的不利之处：超大规模云厂商需要设计、验证和确认（validate）的东西多得多。这很容易就是超大规模云厂商迄今设计过的最复杂平台（Google 的 TPU 系统除外）。部分厂商能快速完成设计，但团队较慢的一些已经落后。总体来看，尽管市场上有取消订单的传闻，我们认为 Microsoft 是部署 GB300 最慢的厂商之一，原因是其设计速度——他们[第四季度仍在采购部分 GB200](https://semianalysis.com/accelerator-industry-model/)。

随着元器件从 NVIDIA 的层层加价（margin stacking）中剥离、转由 ODM 承担，客户支付的总价会有很大不同。ODM 的营收会受到影响，而最重要的是，NVIDIA 的毛利率也会在年内发生位移。下面我们将展示这些影响。
