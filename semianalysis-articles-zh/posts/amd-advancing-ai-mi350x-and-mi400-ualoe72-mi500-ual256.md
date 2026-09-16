---
title: "AMD Advancing AI：MI350X 与 MI400 UALoE72、MI500 UAL256"
title_en: "AMD Advancing AI: MI350X and MI400 UALoE72, MI500 UAL256"
subtitle: "软件改进、营销现实扭曲力场、AMD 培育新兴 GPU 云生态、MI355 并非机柜级方案、MI400 用的是 UALoE 而非 UALink"
date: 2025-06-13
source: https://newsletter.semianalysis.com/p/amd-advancing-ai-mi350x-and-mi400-ualoe72-mi500-ual256
crawled: 2026-09-15
authors: ["Kimbo Chen", "Dylan Patel", "Daniel Nishball", "Wega Chu", "Ivan Chiam", "Gerald Wong", "Patrick Zhou"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# AMD Advancing AI：MI350X 与 MI400 UALoE72、MI500 UAL256

> 原文：[AMD Advancing AI: MI350X and MI400 UALoE72, MI500 UAL256](https://newsletter.semianalysis.com/p/amd-advancing-ai-mi350x-and-mi400-ualoe72-mi500-ual256) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**软件改进、营销现实扭曲力场、AMD 培育新兴 GPU 云生态、MI355 并非机柜级方案、MI400 用的是 UALoE 而非 UALink**

过去六个月里，[AMD 一直处于战时状态](https://semianalysis.com/2025/04/23/amd-2-0-new-sense-of-urgency-mi450x-chance-to-beat-nvidia-nvidias-new-moat/)。他们一直在为实现与 Nvidia 竞争的目标而拼命且聪明地工作。在 Advancing AI 2025 活动上，AMD 发布了 MI350X/MI355X GPU，在中小规模 LLM 推理场景下，以单位 TCO 性能衡量，它们足以与 Nvidia 的 HGX B200 方案一较高下。尽管 AMD 投射出强大的现实扭曲力场（RDF），但 MI355X 并不是一款机柜级（rack scale）产品，在前沿模型推理或训练上也无法与 Nvidia 的 GB200 NVL72 竞争。

真正称得上机柜级解决方案的是 MI400 系列，它有望在 2026 年下半年与 Nvidia 的 VR200 NVL144 机柜级方案展开竞争。MI400 系列周围也缠绕着一些营销话术：AMD 把原来的"IF over Ethernet"协议改名为"UALink Protocol over Ethernet"，而这并不是真正的 UALink。

本文将讨论 AMD 新品的相对竞争力，并分析其总拥有成本（TCO）。我们还会详述 AMD 新的超大规模云客户 AWS，以及另一面——现有客户 Microsoft 后续订单持续令人失望的情况。

最近，Nvidia 推出 DGX Lepton Marketplace，旨在把算力商品化，这让不少新兴 GPU 云（Neocloud）合作伙伴感到不安。我们认为，这一事态也为 AMD 打开了一扇机会之窗，去培育自己的新兴 GPU 云生态。我们将解释 AMD 为何更愿意投资新兴 GPU 云、他们为帮助这些新兴 GPU 云所采用的巧妙财务工程，以及 AMD 对自研内部研发集群的投入。

## 执行摘要

1. MI355X 在中小模型推理上可与 HGX B200 竞争，但无法与 GB200 NVL72 抗衡
2. 尽管有 AMD 的[营销 RDF](https://en.wikipedia.org/wiki/Reality_distortion_field)，MI355 的 128 GPU 机柜并不是"机柜级解决方案"——它的纵向扩展 world size（扩展域内 GPU 数）只有 8 个 GPU，而 GB200 NVL72 的 world size 是 72 个 GPU。在大型前沿推理模型推理上，GB200 NVL72 的单位 TCO 性能将胜过 MI355X
3. MI355X 的集合通信性能与 HGX B200 大体相当，但其集合通信速度至少比 GB200 NVL72 上慢 18 倍，甚至可能更慢
4. AMD 宣布推出开发者云（Developer Cloud），将 MI300 的按需租用价格降至 $1.99/hr/GPU，而当前 AMD 新兴 GPU 云市场价格为 $3.00/hr/GPU，此举可能让租用 AMD GPU 与租用 Nvidia GPU 相比具备竞争力
5. Nvidia 的 DGX Lepton Marketplace 得罪了一大批新兴 GPU 云，这可能给了 AMD 一个切入点，去说服新兴 GPU 云同时支持 Nvidia 和 AMD
6. AMD 终于采取了与 Nvidia 类似的策略，利用其雄厚的资产负债表支持新兴 GPU 云和超大规模云生态采纳 AMD——从云厂商处回租一部分 GPU。这有助于加速终端用户对 AMD 系统的采纳
7. MI400 系列将是机柜级解决方案，有望在 2026 年下半年与 Nvidia 的 VR200 NVL144 竞争
8. 一项正在推进的新举措旨在提高 AMD 工程师薪酬，使其更接近市场水平，并让薪酬与 AMD 的成功更紧密挂钩。AMD 何时向其 AI 工程师宣布此事仍有待观察
9. MI400 系列机柜的纵向扩展网络实际上并没有使用真正的 UALink。AMD 只是把 Infinity Fabric Over Ethernet 改名为"UALink over Ethernet"，并用它来构建其纵向扩展网络
10. MI400 系列纵向扩展网络将使用 Broadcom 的以太网 Tomahawk 6 交换机，因为 Marvell 和 Astera Labs 的 UALink 交换机要到 2026 年底才能就绪
11. 尽管有上述几点，采用 UALink over Ethernet 的 MI400 系列在纵向扩展带宽方面仍将与 VR200 NVL144 的 NVLink 具有竞争力，并且其纵向扩展 world size 同样达到 72 个逻辑 GPU
12. 2027 年底，AMD 将发布 MI500 UAL256，它将拥有 256 个物理/逻辑芯片，而不像 VR300 NVL576 那样只有 144 个物理/逻辑芯片

## MI350X 与 MI355X 规格

本系列有两种版本的 CDNA4 芯片——MI350X 和 MI355X。MI350X 是 1,000W 的风冷版本，而 MI355X 是 1,400W 版本，同时支持风冷和冷板式直冷（DLC）液冷。尽管 MI355X 功耗高出 1.4 倍，但纸面规格显示其 TFLOPS 吞吐只比 MI350X 快不到 10%。不过，我们预计实际性能差距会大于 10%，因为受功耗限制，公开规格往往永远无法达成。这些公开规格假设峰值时钟频率在真实负载下能够维持，但无论 AMD 还是 Nvidia 的系统都做不到这一点。

MI350X 和 MI355X 的纸面规格在 BF16/FP8/FP4 数据类型（dtype）上均与 HGX B200 具有竞争力。我们预计训练将使用 BF16 和 FP8，而推理将使用 FP8/FP6/FP4。在 HGX B200 上，FP6 与 FP8 共用同一套物理电路，因此纸面上 FP8/FP6 的 FLOP/s 相同。而在 MI355X 上，FP6 与 FP4 共用同一套物理电路，因此 FP6 的峰值 TFLOP/s 与 FP4 相同。这意味着 MI355X 的 FP6 比 B200 的 FP6 快 2.2 倍。在实际使用中，由于 AI 芯片始终受功耗限制，MI355X 的 FP6 至少会比 MI355X 的 FP4 慢 20%。

[SemiAnalysis 的基准测试已经表明](https://semianalysis.com/2024/12/22/mi300x-vs-h100-vs-h200-benchmark-part-1-training/)，尽管 MI300X 和 H100 在纸面上 FP16 与 BF16 的 TFLOP/s 相同（即 Nvidia 的 FP16 TF = BF16 = 989 TFLOP/s，AMD 的 FP16 = BF16 = 1307 TFLOP/s），但在实际运行中，每张卡在跑 FP16 与 BF16 时交付的实际 TFLOPs 并不相同。我们将在近期发布一篇微基准测试文章，测算 MI355X FP6 相对于 FP4 的真实 TFLOP/s。

![](https://substack-post-media.s3.amazonaws.com/public/images/0dbf89d7-a405-4a9a-939f-da8bf2af0d29_1616x578.png)
*来源：SemiAnalysis*

在 4 位浮点格式方面，MI355X 将只支持 OCP MX4，即对每 32 个元素组成的数据块施加一个微指数（microexponent）缩放因子。相比之下，Nvidia 的 Blackwell GPU 同时支持 OCP MX4 和 NVFP4，其中 NVFP4 采用更小的 16 元素块，在做 QAT/PTQ 量化校准数值精度时挑战会更少。我们与一些 vLLM 和开源推理贡献者交流过，他们提到 NVFP4 对信息/模型质量的保留远好于 MX4，但 MX4 有可能通过额外的运行时量化软件技术达到同样的质量。

在 Blackwell Ultra B300 HGX NVL8 上，Nvidia 砍掉了大部分 FP64 和 int8 张量核心，腾出空间多放了 1.4 倍的 FP4 张量核心电路。这使得 B300 在 FP4 推理上压倒没有采用这种优化的 MI350 和 MI355。结果就是，B300 的 FP4 TFLOP/s 比 MI355X 快 1.3 倍，而功耗还低 200W。

在 HBM 方面，MI350/MI355 的内存带宽和容量与 B300 相同，但 HBM 容量远高于 B200 的 180GB，达到 288GB。这是 AMD 单节点推理的一大关键优势。然而，在多节点高秩专家并行和预填充分离（disaggregated prefill）的时代，单 GPU 更大的 HBM 虽然仍然有益，却不再那么关键。带宽要重要得多，这也正是两家 HBM 厂商为两个不同的高调 ASIC 项目加急赶工 8Hi HBM4 的原因。更多细节请参阅 SemiAnalysis 加速器与 HBM 模型。

在 MI350/MI355 的纵向扩展网络方面，AMD 把其 XGMI 协议（使用 PCIe 5.0 PHY SerDes）"超频"了 1.2 倍，从 64GByte/s 提升到 76.8GByte/s。其实现方式是采用 PCIe 5.0 PHY 扩展速率模式，每条链路提供约 38GT/s 而非 32GT/s。尽管如此，同级的 Nvidia 产品在纵向扩展网络速度上仍然碾压 MI350/MI355，因为 HGX B200/B300 采用交换式全互联（all-to-all）拓扑，比 MI350/MI355 基于网状（mesh）拓扑的纵向扩展网络快 1.6 倍。至于 GB200 NVL72/GB300 NVL72，与 MI350/MI355 的纵向扩展方案相比根本谈不上比较或竞争：GB200 NVL72/GB300 NVL72 是真正的机柜级解决方案，在单一纵向扩展域内连接 72 个 GPU，而 MI350/MI355 的纵向扩展域只把 8 个 GPU 连在一起。

![](https://substack-post-media.s3.amazonaws.com/public/images/4761c86a-12e9-42a3-9110-3e7d827bd110_1127x975.png)
*来源：SemiAnalysis*

再看横向扩展域，MI350/MI355 支持每 GPU 400 Gbit/s 的速率——与 B200 和 GB200 NVL72 相同，但很快就会被 B300 HGX NVL8 和 GB300 NVL72 超越，这两者均提供每 GPU 800 Gbit/s 的网络。AMD 整体上将在横向扩展网络上落后，因为 Nvidia 今年晚些时候将开始大规模部署其 800GbE ConnectX-8 NIC，而 AMD 的 800GbE "Vulcano" NIC 要到 2026 年下半年才会开始大规模部署。

## 与 HGX B200 NVL8 相比具备竞争力的单位 TCO 性能

我们认为，在中小规模 LLM 生产推理负载上，MI355X 能够与 HGX B200 竞争。原因在于：对自持集群而言，MI355X 的总拥有成本比 HGX B200 低 33%，同时它提供大得多的 HBM 内存容量、略高的 FP8 和 FP4 TFLOP/s 以及翻倍的 FP6 TFLOP/s。在 AMD 的 AI 软件掌门人 Anush 的领导下，AMD 软件的快速改进也将进一步推高 MI355X 的单位 TCO 性能优势。

AMD 对 MI355X 竞争力的宣传核心，在于它不需要冷板式直冷液冷（DLC）。这在一定程度上确有道理，但颇具讽刺意味的是：AMD 仍把下一代的 MI355X 定位为 Nvidia "经济舱"级 HGX 产品的竞争对手——而那些产品早已上市多时。由于上文提到的更小的纵向扩展 world size，AMD 的 MI355X 无法与 Nvidia 旗舰 GB200 NVL72 在前沿推理模型的推理上正面竞争，因此被定位为与风冷 HGX B200 NVL8 和风冷 HGX B300 NVL8 竞争。

话虽如此，这一细分市场将出货可观的量，具体取决于 MI355X 的软件质量以及 AMD 愿意接受的销售价格。我们预计，它最能赢得那些使用中小模型、无法从大纵向扩展 world size 中受益的用户的青睐。但对于那些确实受益于大规模分离式部署的推理模型和前沿推理部署，或采用能利用大纵向扩展网络的混合专家（MoE）模型的场景，GB200 NVL72 在性能和单位 TCO 性能上仍将占据主导，尤其是在推理方面。

![](https://substack-post-media.s3.amazonaws.com/public/images/e1a3295f-0074-45b9-a44d-a281e4d92143_1471x632.png)
*来源：SemiAnalysis*

## Nvidia 的 DGX Lepton 正在得罪新兴 GPU 云

本周在 GTC Paris 上，黄仁勋进一步阐述了 DGX Lepton 及其商业战略，这可能导致 AI 算力在全球范围内被商品化。这意味着客户将能够在理论上保持相同软件用户界面和体验的前提下，自动、无缝地把推理负载在不同云之间迁移。这对主要关注推理和小规模训练负载的客户尤其有吸引力，因为我们不认为超大规模的推理部署或大规模训练会使用 DGX Lepton。

如果 DGX Lepton 取得成功，他们将打造出一种标准化的用户体验——在所有新兴 GPU 云上具备完全一致的功能集、价值主张和性能——这将把所有新兴 GPU 云拖入价格逐底的竞赛。实际上等于把新兴 GPU 云的利润率压缩到超低的商品化水平。

就像 Uber/Lyft 是连接乘客与司机的平台一样，DGX Lepton 似乎想成为 GPU 算力领域的那个平台。众所周知，Uber/Lyft 催生了一大批被平台牢牢锁定的低利润零工经济从业者。DGX Lepton 对新兴 GPU 云可能产生同样的效应。

另一方面，正如 Uber/Lyft 一样，DGX Lepton 对消费者是好事。通过压低中间商利润率，Nvidia 实际上在不影响自身令人瞠目的利润率的情况下，提高了终端用户的单位 TCO 性能。算力将变得更便宜，而体验将被标准化。

从与各家新兴 GPU 云的交流来看，出于上述原因，许多家对 DGX Lepton Marketplace 并不满意。尽管不满，许多新兴 GPU 云仍觉得有义务参与其中，以维持与 Nvidia 的良好关系。[The Information 最近发表的一篇文章](https://www.theinformation.com/articles/nvidia-muscles-gpu-cloud-market-rankling-new-rivals)也详述了新兴 GPU 云内部非常矛盾的心态以及对 DGX Lepton 的总体不满。[据称，NVIDIA Lepton 团队的一些工程师也对与新兴 GPU 云的工作关系将如何演变感到焦虑。](https://x.com/anissagardizy8/status/1932942527574782087)

Jensen 在 DGX Lepton 上可以采取的另一种做法，是将 Lepton 出色的软件平台完全开源，允许参与的新兴 GPU 云在参与 DGX Lepton 市场之余自托管 Lepton 软件时，免费部署 Lepton 的软件。

这将让新兴 GPU 云拥有独立于 Nvidia 市场之外的多个销售渠道，同时仍能为消费者带来强劲的性能和更好的体验，抬高整个生态的水位。

DGX Lepton 风波的一个结果是：新兴 GPU 云开始重新审视完全依赖单一供应商的做法，许多家最终可能会寻求替代方案来缓解这一风险。这一事态为 AMD 创造了绝佳的切入点，使其能够快速加强与新兴 GPU 云的接触，迅速扩大托管 AMD GPU 的新兴 GPU 云数量。

## MI355X 不是机柜级解决方案——AMD 的营销话术

AMD 一直在把 MI355X 当作"机柜级解决方案"来营销，但无论按哪种定义，MI355X 都不是机柜级解决方案。MI355X 的"128 GPU 机柜"只是把 16 台 MI355X UBB8 服务器放进同一个机柜，并没有一个贯穿整个机柜的连贯纵向扩展域。

MI355 的"128 GPU 机柜"是 Temu 网站批发来的机柜级方案。把 MI355 DLC 机柜称为"机柜级解决方案"，就好比你想说服制片人，在你即将开拍的好莱坞大片里[用 Jesse Plemons 顶替 Matt Damon](https://people.com/jesse-plemons-does-not-really-think-he-bears-a-resemblance-to-matt-damon-8662275)。

正如我们将在下文进一步展开的，这意味着 MI355X "机柜级解决方案"的集合通信性能比 GB200 NVL72 差 18 倍。对 MI355X 而言，UBB8 服务器 A 里的 GPU 与同一机柜内 UBB8 服务器 B 里 GPU 通信时，只能走 400Gbit/s 的以太网；而对 GB200 NVL72 来说，不同计算托盘（compute tray）之间的 GPU 以 900GByte/s 的速率通信。

![](https://substack-post-media.s3.amazonaws.com/public/images/7e5c9244-689c-49f9-94fb-74f92cb73fe5_963x441.jpeg)
*来源：AMD*

如果 MI355 128 GPU 机柜算得上"机柜级解决方案"，那为什么不把众多 H100 机柜也称作"机柜级解决方案"？显然，如果 MI355 被贴上"机柜级解决方案"的标签，H100 也理应被视为"机柜级解决方案"。这是个荒谬的命题，因为没有人把 xAI 每机柜 64 个 GPU 的 H100 部署称作"机柜级解决方案"。和 MI355 一样，这套 H100 部署并没有跨越全部 64 个 GPU 的连贯纵向扩展域，它只是一台机柜里的八台 HGX H100 NVL8 服务器。

![](https://substack-post-media.s3.amazonaws.com/public/images/f1ef59ca-a43e-4546-8aca-5a37d8755032_1199x800.jpeg)
*xAI 的"机柜级解决方案"。来源：ServeTheHome*

在混合专家（MoE）模型的推理和训练中，最重要、通信量最大的集合通信操作是 all-to-all，它负责把 token 路由到正确的专家。在 all-to-all 通信上，MI355X 比 GB200 NVL72 慢 18 倍，比 HGX B300 NVL8 慢 2 倍。对于使用 2D+ 并行训练模型，LLM 的一种常见模式是使用 split mask 为 0x7 的 all-reduce，对于这一操作，MI355X 同样比 GB200 NVL72 慢 18 倍。这个例子清楚地说明，MI355X 显然不是机柜级产品，与 GB200 NVL72 不在一个量级上。

![](https://substack-post-media.s3.amazonaws.com/public/images/9d15aa33-b0a1-46cc-83ce-14d8aae7c595_1322x748.png)
*来源：SemiAnalysis*

## 超大规模云厂商与 AI 实验室对新 AMD 产品的采纳

尽管 MI355 机柜的营销方式颇为滑稽，我们关于总拥有成本以及强劲的单位 TCO 性能潜力的观点，显然已经引起了超大规模云厂商和大型 AI 实验室客户的共鸣，我们看到与这些客户的接触非常踊跃、订单势头良好。

AWS 是 AMD Advancing AI 活动的冠名赞助商，它将首次认真投入，大规模采购并部署 AMD GPU 用于对外出租。

Meta 在 AMD 问题上通常聚焦推理场景，如今也开始在 AMD 上进行训练。他们是 72 GPU 机柜背后的关键推动力，并将采购 MI355X 和 MI400。Meta 的 PyTorch 工程师现在甚至也在参与 AMD Torch 的开发，而不再只是 AMD 自己的工程师在搞 AMD Torch。

至于 OpenAI，Sam Altman 出席了 AMD 活动并登台。在我们[首篇 AMD 与 Nvidia 基准对比文章](https://semianalysis.com/2024/12/22/mi300x-vs-h100-vs-h200-benchmark-part-1-training/)发表后，OpenAI 很欣赏 AMD 行动速度的大幅提升。

x.AI 将把这些即将面世的 AMD 系统用于生产推理，扩大 AMD 的存在感。过去，只有很小比例的生产推理使用 AMD，大多数负载跑在 Nvidia 系统上。

GCP 正在与 AMD 洽谈，但谈判已经持续了相当长时间。我们认为，AMD 应该给 GCP 与给几家关键新兴 GPU 云相同的条件——即通过提出为 AMD 内部研发需求回租算力，来引导启动 AMD 租赁产品。

Oracle 是快速部署新兴 GPU 云产能的公认先驱，也计划部署 30,000 颗 MI355X。

Microsoft 是唯一仍在观望的超大规模云厂商，只订购了少量的 MI355，不过其对部署 MI400 的态度正在转暖。

这些超大规模云厂商中的许多家，由于其传统数据中心设计架构而拥有大量风冷数据中心，鉴于 MI355X 风冷方案极具吸引力的单位 TCO 性能主张，他们非常乐意采纳风冷 MI355X。总体而言，我们预计所有这些超大规模云厂商都会部署 MI355，其中许多还会继续部署 MI400 这一真正的机柜级解决方案。

## AMD 正在解决其新兴 GPU 云租赁市场的短板

提高 AMD 采纳度的主要挑战之一是：目前专注于 AMD 的新兴 GPU 云寥寥无几，而专注 Nvidia 的超过一百家。租赁市场供给稀缺、产品多样性不足，导致 AMD GPU 租赁价格被人为推高，侵蚀了 AMD GPU 的整体成本竞争力。

[2025 年第二季度至今](https://semianalysis.com/ai-cloud-tco-model/)，H200 当前 1 个月期限合约的市场租赁价格大约在 $2.50/hr/GPU，价格差异很大，低质量云的价格更低。MI325X 的 1 个月租赁合约根本不存在。MI300X 的 1 个月租赁合约定价为 $2.50/hr，这使得 MI300X 在租赁市场上相对 H200 缺乏竞争力。下面我们展示，MI300X 和 MI325X 的 1 个月租赁价格大约需要达到多少，才能与租用 Nvidia H200 相比具备竞争力。这一分析在很大程度上基于[我们的真实世界推理基准测试](https://semianalysis.com/2025/05/23/amd-vs-nvidia-inference-benchmark-who-wins-performance-cost-per-million-tokens/#what-rental-price-would-make-amd-gpus-competitive-with-nvidia-for-renters-of-compute-for-inference)。

对于推理式推理任务（1k 输入、4k 输出），MI300X 的 1 个月合约价格需要低于 $2.10-2.40/hr，才能获得与 H200 相当的性价比。MI325X 需要定价在 $2.75/hr/GPU 到 $3.00/hr/GPU 之间（取决于交互性）才具备竞争力。这是一个目前没有任何 AMD 新兴 GPU 云不经艰难谈判就能提供的价格区间，这意味着 Nvidia 目前在租赁性价比上的胜利，部分正是这种市场低效的结果。

![](https://substack-post-media.s3.amazonaws.com/public/images/4e4c7ac3-bb71-4442-bcb3-d175e0419346_1600x954.png)
*来源：SemiAnalysis*

## 挂挡加速——AMD 正在加速发展 AMD 新兴 GPU 云生态

直到几个月前，AMD 对推动其产品在新兴 GPU 云生态中更快增长并不十分上心，也没有为 GPU 云提供足够的激励，让它们愿意承担托管 AMD GPU 却可能租不出去的风险。在过去几个月里，AMD 管理层认识到，建设一个健康的新兴 GPU 云生态非常重要：这有助于提升开发者采纳度，也有助于压低被人为推高的 AMD GPU 租赁价格。最终结果是终端用户获得更高的性价比，以及更多熟悉 AMD、能够回馈更广泛 AMD 生态的开发者。

为此，AMD 向 AWS、OCI、Digital Ocean、Vultr、Tensorwave、Crusoe 及其他新兴 GPU 云提供了强有力的激励，支持这些超大规模云厂商和新兴 GPU 云采纳 AMD 并降低商业风险。AMD 达成的交易是：作为客户愿意购买更多 AMD GPU 的交换，AMD 将以长期合约的形式回租其中相当大的一部分产能，用于 AMD 内部软件开发目的。这与 Nvidia 已有的做法类似——为满足自身庞大的内部算力需求，Nvidia 已经从 GCP、OCI、AWS、Azure、CoreWeave 回租大规模 GPU 集群。对某些新兴 GPU 云，AMD 提供的激励可以完全消除投资风险：如果新兴 GPU 云无法把产能全部卖出，AMD 自己会把它租下来作为兜底。我们知道许多新兴 GPU 云目前正在探讨与 AMD 达成类似激励结构的潜在合作。

有了这些激励，甚至可以这样说：与那些只以短期为基础租赁 Nvidia 集群、承担相当大价格和出租率风险的同行相比，这些与 AMD 合作的新兴 GPU 云构建的商业风险反而更低。

AMD 开发者云的推出，也是让 AMD 算力以有竞争力的价格普遍可及的关键战略。作为此次发布的一部分，AMD 大幅下调了 MI300X GPU 的租赁价格，让更广泛的开发者群体都能用上。遗憾的是，在我们测试时，默认配额被设为零个 GPU，而且很难申请提高 GPU 配额。我们建议 AMD 把新用户的默认配额设为至少 16 个 MI300X GPU，以便更有效地把开发者引入其生态。由于 AMD 开发者云的按需价格定在 $1.99/hr/GPU 这一合理得多的水平，我们预计提供按需 MI300 的 AMD 新兴 GPU 云可能需要把目前 $3/hr/GPU 的高价下调到 $2/hr/GPU 来对齐。

![](https://substack-post-media.s3.amazonaws.com/public/images/41cb9b83-52e0-4dc7-a77b-01950af62c75_1121x532.png)
*来源：SemiAnalysis、AMD*

## ROCm 软件改进

AMD 发布了聚焦推理能力和性能的 ROCm 7。在推理吞吐性能上，AMD 宣称 ROCm 7 相比 ROCm 6 平均提升 3.5 倍，在服务 DeepSeek R1 时 ROCm 7 相比 Nvidia B200 提升 1.3 倍。我们期待验证这些说法。

AMD 也致力于与开放生态合作开展分布式推理。除支持推理框架 vLLM 和 SGLang 外，AMD 还支持编排框架 llm-d（Nvidia Dynamo 的替代方案），以实现 PD 分离（预填充/解码分离）这一分布式推理技术。llm-d 技术栈仍缺少不少功能，尚无法起到与 Nvidia Dynamo KVCache 管理器相同的作用。KV 缓存管理器非常重要，它能为推理负载带来巨大的 TCO 收益，为许多推理负载解锁数倍的吞吐提升。

ROCm 对 kernel 编写库 Triton 的支持在过去几个版本中也有大幅改进。ROCm 去年实现了对 Triton 的功能性支持，ROCm 7 则聚焦性能提升。我们希望 AMD 继续这项工作，并扩大对 FlexAttention 等高级特性的支持。

最近，ByteDance Seed 创建了 Triton Distributed，一个基于 Triton 的库，可实现计算与 GPU 通信的重叠。AMD 对 Triton Distributed 表现出浓厚兴趣，并谈到将加大支持力度。不过，OpenAI（Triton 的维护者）是否会接受把 ByteDance 的 Triton Distributed 特性贡献回原生的 Triton 库，仍不清楚。OpenAI 有可能正在走自己的路线，为 Triton 实现分布式计算-通信 kernel。

此外，考虑到对中国的重大芯片出口管制，ByteDance 可能会逐步退出为西方 GPU 的开源库做贡献。话虽如此，ByteDance 正在 AMD 上重金投入，我们预计他们会租下可观的基于 AMD 的租赁 GPU 产能。不过 ByteDance 仍将主要站在 Nvidia 阵营，因为其算力扩张的绝大部分将来自租用基于 Nvidia 的产能。ByteDance 的大部分算力要么来自云租赁，要么来自位于中国以外的大规模专用裸金属集群，而其大多数新兴 GPU 云和云提供商目前仍主要依赖 Nvidia 算力。

在更底层的层面，AMD 声称正在集成流行的数据传输接口 Mooncake Transfer Engine 和专家并行通信库 DeepEP。但截至本文写作时，我们仍未在任何开源 ROCm 仓库中看到 DeepEP 或 Mooncake。

最后，AMD 宣布了开发者云（Developer Cloud）和开发者积分（Developer Credits）计划。除了简洁的算力申请界面外，AMD 还创建了 Python 包 "rocm"，让开发者能轻松安装 ROCm PyTorch、HipBLAS 等 ROCm 库以及这些 ROCm 库的开发工具。所有代码已在 GitHub 仓库 [ROCm/TheRock](https://github.com/ROCm/TheRock) 开源。

## MI355X 的 PyTorch 持续集成（CI）与测试

AMD 已开始为 MI355 芯片向 PyTorch 添加 CI 和自动化测试。请注意，MI355X 的 PR 目前一个都还没有被合并，但很高兴看到 AMD 从第一天起就在考虑开源 PyTorch 的 MI355X CI。对 Nvidia 而言，Blackwell 大规模交付至今已过去六个月，他们却尚未启动开源 PyTorch 的 CI，一直只专注于内部 Blackwell CI。事实上，PyTorch CI 的大部分成本由 Meta 支付，每月支出超过 $100 万，而 AMD 自己则为 AMD 上的开源 PyTorch CI 买单。虽然 Nvidia 迄今未向开源 PyTorch CI 捐出可观的资金或算力，但它已有相关计划，打算通过从 DGX Cloud 捐赠大量算力积分、以及把从其各家新兴 GPU 云提供商处租来的 GPU 产能捐给 Meta 开源 PyTorch 来做贡献。

Nvidia 正积极为开源 B200 PyTorch CI 做加法，并已承诺向 PyTorch 基金会捐赠 48 块 B200 用于 PyTorch CI。虽然大家都更希望从第 0 天就有 CI，但迟到六个月才给 PyTorch 加上 Blackwell 开源 CI，也算亡羊补牢。我们对 AMD 缺乏 CI 的聚焦报道，很可能促使他们在这方面取得了重大进展。Nvidia 应当继续甚至更大力度地投入 Blackwell 的 PyTorch CI。此外，其消费级 GPU 也需要纳入 PyTorch CI 和主流推理库，以确保消费级 AI 的稳定性。目前，由于 CI 资源不足，Nvidia 消费级 GPU 在使用某些框架时会遇到一些不稳定的情况。

## ROCm 的 MLPerf Training 提交

上个月，AMD 提交了其首个 MLPerf Training 成绩：单节点 Llama2 70B LoRA 微调和 BERT 训练。这是一个非常重要的进展，它表明训练可以在单个 AMD 节点上运行。下一步，AMD 应该参与更多真实世界的训练基准，例如 MLPerf Llama 405B 多节点训练基准。我们认为他们能在这个测试中拿出有竞争力的结果。

[在基准测试方面，我们欣赏 AMD 通过为其 MLPerf 运行提供易于遵循的可复现指令，清晰展示其解决方案何时运行良好](https://rocm.blogs.amd.com/artificial-intelligence/reproduce-mlperf-training-v5.0/README.html)。这与 Nvidia 的 MLPerf 提交形成鲜明对比——后者极难复现。

![](https://substack-post-media.s3.amazonaws.com/public/images/f5e06951-94dd-4c69-ae96-77291ef76ca3_1708x956.png)
*来源：AMD*

## MIG 分区正在浪费时间与工程资源

AMD 目前正在其宠物项目上浪费大量工程资源和资金，该项目旨在支持 GPU 分区——允许用户把单个 GPU 变成 8 个更小的 GPU。没有任何客户在要求这个。Meta、OpenAI、x.AI 都没有要求这个，因为所有在线推理负载至少需要一个 GPU。我们认为这是不合逻辑的：AMD 硬件工程师辛苦开发出单 GPU 配备海量 HBM 的最先进芯片之一，到头来却想把这个 GPU 拆成 8 份。

事实上，Meta、OpenAI、x.AI 想要的恰恰相反：他们希望 AMD 通过 DeepEP 和预填充分离等技术，更好地支持至少 16 个 GPU 的多节点推理。

![](https://substack-post-media.s3.amazonaws.com/public/images/5948c718-6a46-4252-b3d7-d39152fa5b7b_1236x698.jpeg)
*来源：AMD*

## MI355X 制造——更新的小芯片架构

![](https://substack-post-media.s3.amazonaws.com/public/images/1d1dd3c5-8be4-4b71-aa94-58727f99cf06_1748x1053.png)
*来源：SemiAnalysis*

AMD 利用 MI300 发布以来的两年时间打磨其小芯片（chiplet）架构。从上图的裸片（die shot）可以看出，芯片布局做了微调：底部的有源中介层裸片（AID）从四个象限合并为两个光罩尺寸的半区。对 HBM 位置的微调，把结构支撑硅片从 HBM 位点之间挪到了四角。

其好处在跨小芯片通信上一目了然：省掉了整整一个维度的 2.5D Infinity Fabric 先进封装链路，因需要跨越的芯片边界更少而节省了功耗和面积。它还消除了两跳场景——MI300 上处于对角的象限彼此通信时，必须跨越裸片跳两次。

不过，这种排布也让 3D 堆叠良率变得更加关键。AMD 继续使用台积电（TSMC）的 SoIC 混合键合工艺，现在需要把两倍数量的加速复合裸片（XCD）附着到每片基片裸片上，一旦出问题，可能会放大良率损失并造成额外的硅浪费。AMD 选择这条路线，印证了台积电 SoIC 流程的成熟度，以及 AMD 的代工技术与运营团队与台积电超过 5 年的深度合作——AMD 一直是 SoIC 的首席客户。

![](https://substack-post-media.s3.amazonaws.com/public/images/7a4b9cc7-8f7b-40e1-be95-f778ea334af7_2560x1695.png)
*来源：AMD Advancing AI*

基片仍停留在台积电 N6，但获得了多项速度升级。剩余的裸片间链路从 4.8TB/s 的等效对分带宽升级到 MI350 上 5.5TB/s 的等效对分带宽。用于纵向扩展的 Infinity Fabric 速度提升了 20%。更重要的是，内存控制器现在可以支持更快的 HBM3E。AMD 坚持使用久经考验的 CoWoS-S 做 AID 与 HBM 的贴装，并指出封装占位与 MI300 保持一致。

计算裸片方面，XCD 从 N5 迁移到台积电的 N3P 节点，并采用下文详述的更新版 CDNA4 架构。这一次，AMD 只启用了裸片上印制的 36 个 CU 中的 32 个，而 MI300 是 40 个中启用 38 个。有趣的是，XCD 在 AID 上的朝向发生了变化，数据键合焊盘落在 AID 的中央区域，数据随后向外流经 256MB 的内存直挂末级（MALL）缓存，最终抵达 HBM。

总体而言，新芯片集成了 1,850 亿（185 Billion）只晶体管，比 MI300 增加 21%。我们估计每片 AID 约含 230 亿只晶体管，每片 XCD 含 174 亿只晶体管。这意味着从 N5 到 N3P，晶体管预算增加了 30%。

## CDNA4 微架构（UArch）

AMD 的架构设计正逐渐从传统的 HPC 取向转向针对 AI 负载的优化。在 CDNA 4 上，我们看到传统 HPC 的残留影响继续消退，AMD 在架构上进一步转向 AI，不过 CDNA4 仍在 FP64 矩阵核心上浪费大量裸片面积。

CDNA 4 拥有 256 个计算单元（CU）、160KB 的本地数据共享存储（LDS，相当于 SMEM），以及每 CU 每周期 4,096 FLOPs 的 FP16 矩阵核心。与 CDNA 3 相比，CU 数量减少了 16%，LDS 容量增至 1.5 倍，矩阵核心吞吐增至 2 倍。这些变化都是架构向更大阵列尺寸的 AI 负载收敛的标志。HPC 负载通常受益于大量的 CU，而 AI 负载受益于每个 CU 计算大型矩阵，这两种需求在功耗和面积预算上互相竞争。LDS 容量的增加表明矩阵核心速度太快，AMD 需要增大二级缓冲容量，才能足够快地向核心喂送数据。鉴于 AMD 增加的是 LDS 而非典型的暂存缓冲 VGPR（相当于 RMEM），我们怀疑下一代矩阵核心需要大幅的架构变革，才能继续扩展矩阵核心性能。

CDNA 4 的 FP8 吞吐是 FP16 的 2 倍，FP4 是 4 倍。有趣的是，CDNA 4 的 FP6 吞吐在理论上与其 FP4 吞吐完全相同，因为 FP6 与 FP4 共享数据通路。然而，由于真实环境中的功耗限制，FP6 吞吐仍会略低于 FP4。这一点与 Nvidia Blackwell 不同，后者的 FP6 吞吐标注为与 FP8 相同。

然而，与 Nvidia 的 Blackwell 设计相比，CDNA 4 没有异步特性、数据搬运加速硬件（如 sm90/sm100 的 TMA）、TMA 多播或专用存储（sm100 的 TMEM）。这导致 CDNA4 相比 Nvidia 的 SM100，每单位"智能"的皮焦耳数更差。截至写作时，我们仍在等待 ISA 细节，以了解 MFMA 操作有哪些变化，看看是否存在 WGMMA 的等价物。话虽如此，CDNA 4 也表明这些特性是进一步提升性能所必需的，因此我们预计 CDNA-NEXT 会出现剧烈的架构变化。

## AMD Advancing AI 的开发者分论坛令人失望

AMD 今年在 [ROCM 博客](https://rocm.blogs.amd.com/)上的开发者内容已有很大改进。我们是抱着希望来参加 AMD Advancing AI 的，期待 AMD 举办覆盖整个技术栈的众多开发者专场，但实际的演讲和场次令我们兴致索然。从 RCCL 到 Composable Kernels、rocSHMEM、aiter 等，大多数 AMD 库都没有专题演讲。我们希望 AMD 扩大演讲和研讨会的范围，以便在今年晚些时候更聚焦的会议上，让开发者能更深入自己感兴趣的领域。

![](https://substack-post-media.s3.amazonaws.com/public/images/570ad021-a55d-41cd-bfab-80a0ff1c3c92_1974x920.png)
*来源：SemiAnalysis、Nvidia、AMD*

## RCCL——ROCm 集合通信库

AMD 宣布其新的 400G NIC 将具备 Ultra Ethernet（UEC）就绪能力，并同时支持现有的 RoCEv2 协议和新的 Ultra Ethernet 传输（UEC）协议。在 UEC 模式下，该 NIC 将能够支持包喷洒（packet spraying），并可乱序直接落位到 GPU 显存，而无需像 Bluefield-3 那样使用 NIC 重排序缓冲。AMD 自研的新 400G NIC 让他们能够更轻松地进行软件垂直整合并改善开箱体验，而不必依赖 Nvidia 的 CX-7 NIC 或 Broadcom 的 Thor-2 NIC。Oracle 以及 Tensorwave 等 AMD 新兴 GPU 云已承诺采纳 AMD 的 NIC，不过 Meta 有所保留——初期测试尚未让他们放心采纳 AMD NIC，其 MI355X 集群将改用 ConnectX-7 NIC。Broadcom 的 Thor 2 和 Thor 3 NIC 在市场采纳上一直面临挑战，原因是 AMD 和 Nvidia 都在推行把 NIC 垂直整合进自家解决方案的策略。不过，我们确实认为 Broadcom 的 NIC 在各种 ASIC 项目中仍有一席之地。

AMD 的自研 400GbE NIC 还支持一些有趣的特性，例如为 RING 和 PAT 等算法卸载 all-gather 集合通信。AMD 声称 CPU 代理线程也将被卸载到 NIC，但我们不确定这是否意味着他们使用的是 IBGDA，还是在做别的事情。

ROCm 7.0 的 RCCL 通信库也已发布，遗憾的是，它看起来仍只是 Nvidia NCCL 的照抄分支（fork），因此它依然是拖累 AMD 多节点能力的关键瓶颈。正如我们在 AMD 2.0 一文中所建议的，我们仍然认为 AMD 需要从零开始完全重写其通信库，而不是依赖 fork Nvidia 的软件。

## AMD 为 AI 工程师支付市场水平薪酬的新举措

[业内众所周知，大多数 AMD AI 工程师的薪酬一直低于市场水平](https://semianalysis.com/2025/04/23/amd-2-0-new-sense-of-urgency-mi450x-chance-to-beat-nvidia-nvidias-new-moat/)。唯一的例外似乎仅限于最近几个月的少数新员工，以及通过收购加入的工程师。例如，两年前从 NodAI 收购中带来的大多数 AI 工程师，即使拉平经验和技能组合来看，其薪酬也显著高于 AMD 现有工程师。有趣的是，AMD 的人力资源部门几个季度前就已提出这个问题，承认这种薪酬差距并在内部逐级上报，但 AMD 管理层至今没有把此事提升到低优先级议题之上。[在我们公开发文说明 AMD 给 AI 工程师的薪酬远低于市场之后](https://semianalysis.com/2025/04/23/amd-2-0-new-sense-of-urgency-mi450x-chance-to-beat-nvidia-nvidias-new-moat/#amd-management%e2%80%99s-blind-spot-%e2%80%93-amd-ai-software-engineer-compensation)，AMD 的人力资源负责人立即把此事提升为最高优先级，并正在积极推进一项流程以解决这些巨大的薪酬差距——但落实仍是进行时。鉴于 AMD 手握数十亿美元现金，我们希望 AMD 会做正确的事，为其顶级个人贡献者（IC）支付有竞争力的总薪酬，并使其与 AMD 的成功挂钩。

## MI400 系列的柔性输入输出（I/O）

AMD 从 MI300X 的失误中吸取了教训——他们部署的 Infinity Fabric 远逊于 NVLink。他们也意识到，自己缺乏打造 NVSwitch 等价物的硬件人才。此外，他们也不想因过度垂直整合而侵犯行业生态。因此，他们选择了"霰弹枪"策略——支持一切能支持的东西。

于是有了柔性 I/O lane。AMD 不再为 PCIe、纵向扩展等每种不同类型的 I/O 配备独立的 SerDes 和 I/O 通路，而是提供 144 条可支持多种不同标准的 I/O lane。这些 I/O lane 可支持 PCIe 6.0、64G 的 Infinity Fabric、128G 的 UALink、128G 的 xGMI 4（某种意义上的 UALink 超集），以及 212G 的 Infinity Fabric over Ethernet。这种做法让 AMD 的硅工程团队在各种不同用例中拥有最大的灵活性。

借助柔性 I/O，AMD 可以部署 UALink 纵向扩展，也可以部署 UALink over Ethernet。他们可以支持直连 GPU 的 SSD，也可以通过 UALink 挂载 NIC。可能性几乎无穷无尽。这是一个极其庞大的系统排列组合空间，为变化和演进留出了巨大余地。

然而，在硅工程上实现这些不同形态的 I/O 并不容易。AMD 必须打造能在所有这些排列组合下正常工作的 SerDes 和数据通路。这是一条极其艰难、充满工程风险的路线。

在接下来的章节中，我们将更深入地剖析 MI400 这款真正的机柜级解决方案，讨论关键的纵向扩展架构选择，并借助立面图和电路板设计图讲解整机柜设计。我们还将提供详细的物料清单（BOM）拆解，以及总拥有成本和单位 TCO 性能分析。
