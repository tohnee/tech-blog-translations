---
title: "AI 新兴 GPU 云（Neocloud）手册与剖析"
title_en: "AI Neocloud Playbook and Anatomy"
subtitle: "H100 租金下调、新兴 GPU 云巨头与新锐 GPU 云、H100 集群物料清单与集群部署、日常运营、成本优化、拥有成本与回报"
date: 2024-10-03
source: https://newsletter.semianalysis.com/p/ai-neocloud-playbook-and-anatomy
crawled: 2026-09-15
authors: ["Dylan Patel", "Daniel Nishball"]
tags: ["Hardware Architecture", "AI Infrastructure", "Neoclouds"]
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# AI 新兴 GPU 云（Neocloud）手册与剖析

> 原文：[AI Neocloud Playbook and Anatomy](https://newsletter.semianalysis.com/p/ai-neocloud-playbook-and-anatomy) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**H100 租金下调、新兴 GPU 云巨头与新锐 GPU 云、H100 集群物料清单与集群部署、日常运营、成本优化、拥有成本与回报**

## H100 租金下调、新兴 GPU 云巨头与新锐 GPU 云、H100 集群物料清单与集群部署、日常运营、成本优化、拥有成本与回报

AI 新兴 GPU 云（Neocloud）的崛起吸引了整个计算行业的目光。从企业到初创公司，所有人都在通过它们获取 GPU 算力。即便是拥有自建数据中心建设和运营团队的微软，目前每月也要通过 AI 新兴 GPU 云斥资约 $200 million 购买 GPU 算力。Nvidia 则通过直接投资、大笔 GPU 产能配给以及在各场演讲与活动中的褒奖，为多家 AI 新兴 GPU 云的快速扩张摇旗呐喊。

AI 新兴 GPU 云的定义是：一类专注于提供 GPU 算力租赁的新型云计算服务商。这些纯 GPU 云为客户提供尖端性能与灵活性，但支撑它们运转的经济学仍在演化之中，市场也才刚开始理解它们的商业模式如何运作。

在本篇深度解析的前半部分，我们将层层剥开运营一家新兴 GPU 云的各个环节——从编制集群物料清单（BoM），到部署、融资与日常运营的种种复杂性。我们将在 BoM 与集群架构方面给出若干关键建议。

在报告的后半部分，我们将解释 AI 新兴 GPU 云经济学，详细讨论这些新兴 GPU 云的市场进入（go-to-market）策略、总拥有成本（TCO）、利润率，以及多种情形下的商业案例与潜在投资回报。

最后，**我们将讨论多家超大规模云厂商与新兴 GPU 云的 H100 GPU 租赁价格的快速变化**，谈谈仅在过去一个月里**按需价格的显著下滑**、H100 GPU 合同定价期限结构的变化，以及随着 Blackwell GPU 即将部署、市场将如何演进。

更多 SKU、更高频率、更细颗粒度的 GPU 价格数据，请见我们的 AI GPU 租赁价格追踪器（AI GPU Rental Price Tracker）。关于未来算力容量、算力成本的细颗粒度数据与建模，以及多款现有与未来 GPU SKU 的租赁价格预测，请见我们的 [AI 云 TCO 模型（AI Cloud TCO model）](https://semianalysis.com/ai-cloud-tco-model)。

## 巨头与新锐

AI 新兴 GPU 云市场由四大类供应商构成：传统超大规模云厂商、新兴 GPU 云巨头（Neocloud Giants）、新锐 GPU 云（Emerging Neoclouds），以及经纪商/平台/聚合商。

AI 新兴 GPU 云市场体量巨大，是 GPU 需求最有意义的增量驱动因素。粗略地看，我们预计新兴 GPU 云将增长至总需求的三分之一以上。

提供 AI 云服务的传统超大规模云厂商包括 Google Cloud（GCP）、Microsoft Azure、Amazon Web Services（AWS）、Oracle、腾讯、百度、阿里巴巴。相比之下，Meta、xAI、字节跳动和特斯拉虽然同样拥有强大的 GPU 机队和可观的扩容计划，但目前并不对外提供 AI 服务，因此不属于这一类。

传统超大规模云厂商多元化的商业模式使其资本成本最低，但其整合的生态系统与数据湖、既有的企业客户群，意味着定价远高于其他玩家。超大规模云厂商的云业务利润率通常很高，因此定价被定得远高于 AI 云场景的合理水平。

新兴 GPU 云巨头与传统超大规模云厂商不同，几乎专注于 GPU 云服务这一件事。最大的几家目前或未来几年规划的产能，在所有站点合计远超 100k H100 等效算力，[有的还在为 OpenAI 规划数十万颗 Blackwell GPU](https://semianalysis.com/multi-datacenter-training-openais)。四大新兴 GPU 云巨头是 Crusoe、Nebius、Lambda Labs 和 CoreWeave，其中 CoreWeave 规模遥遥领先。它们的资本成本高于超大规模云厂商，但相比新锐 AI 新兴 GPU 云通常更容易以合理利率获得资金，这意味着新兴 GPU 云巨头的相对拥有成本更低。

新锐 AI 新兴 GPU 云（Emerging Neoclouds）包括一条长长的尾巴——[我们跟踪的数十家 GPU 云](https://semianalysis.com/accelerator-model)，它们的产能规模尚小，运营数据中心基础设施的经验也相对不足。这些后起之秀[通常资本成本更高](https://semianalysis.com/ai-cloud-tco-model)，也是我们今天着墨最多的一类。新锐 GPU 云中还包括许多区域性玩家，它们归入「主权 AI（Sovereign AI）」范畴——其定义为：任何将商业模式聚焦于向美国或中国以外次级地区提供 AI 云服务的新兴 GPU 云。

这些地区目前的 AI 技术远远落后，包括欧洲、印度、中东、马来西亚等。尤其是，出于监管、隐私、数据安全或其他商业原因，这些地区的客户通常希望 GPU 算力不落在美国或中国境内。虽然大多数新锐 GPU 云的 GPU 数量不足 10k、甚至尚未部署 GPU，但其中不少怀有极其宏大的规划，可能很快把少数几家推进新兴 GPU 云巨头的行列。

最后一类是经纪商（Broker）、平台（Platform）与聚合商（Aggregator），它们通常聚合供需，但倾向于轻资产运营，回避直接的 GPU 租赁价格敞口，因此自身并不拥有任何 GPU。这一类别下有两种主要商业模式：平台模式——提供类似 Shopify 的平台，帮助 GPU 持有方和数据中心代为营销、撮合其算力资源；聚合商模式——为 GPU 持有方提供类似 Amazon Marketplace 的市场，让他们把算力卖给不同的买家。

平台可以为那些想持有 GPU 算力、却缺乏集群部署或营销能力的托管方提供 IaaS 基础设施以及搭建和采购支持；而经纪商和平台相比单纯的类 Amazon 市场聚合商通常需要更多人工触点，类似帮你找房、按成交额抽佣的房产中介。与任何经纪或市场服务一样，经纪商抽取的分成对终端客户而言可能并不透明。

上述类别之外，还有一种有趣的新兴商业模式——风投集群（VC Clusters）：由风险投资机构（VC）或类 VC 主体建设集群，专供其投资组合公司或其他关联公司使用。知名案例包括 Andromeda、[Computefund.ai](https://computefund.ai/)，以及 [Andreessen Horowitz 计划打造的 GPU 集群](https://www.theinformation.com/articles/andreessen-horowitz-is-building-a-stash-of-more-than-20-000-gpus-to-win-ai-deals)。凭借自建集群，这些风投可以提供极其灵活的算力租赁选项——例如以远低于其他新兴 GPU 云的租金，短期出租 512 或 1k GPU 的大集群，以换取股权。它们还可以向投资组合或关联公司提供更慷慨的租赁条款。

![](https://substack-post-media.s3.amazonaws.com/public/images/e347a756-d864-4e1b-983e-9bde22c34e53_1024x479.png)
*来源：SemiAnalysis*

## 第一部分：如何打造一家 AI 新兴 GPU 云

## 理解集群物料清单

先从一个简单的框架讲起。假设你想创办一家 AI 新兴 GPU 云，你会怎么做？这就是我们的分步指南：从 BoM 开始，到完成新兴 GPU 云的搭建为止。

理解并定制 AI 集群报价与物料清单（BoM）是新兴 GPU 云部署中最重要的环节之一，做得好不好，可能决定你是坐享丰厚利润率还是陷入财务困境。我们建议从 CEO 到工程师、销售，每个人都读懂 BoM 里的每一行条目。

当今部署的大多数新兴 GPU 云集群不超过 2048 个 GPU。最常见的物理集群规模是 2048、1024、512 和 256 个 GPU，2048 GPU 及以下集群的部署成本随 GPU 数量线性变化。本文分析将以 1024 GPU 部署为基准，作为新锐 GPU 云的最大公约数。

OEM 和 Nvidia 在出具 BoM 报价时自然会设法向上销售。BoM 通常细分为四个层级：计算机箱级、机柜级、集群级和软件级。

![](https://substack-post-media.s3.amazonaws.com/public/images/ee9c7400-29f2-45e3-9c27-56767659cef9_875x639.jpeg)
*来源：SemiAnalysis*

## 计算机箱物料清单

我们从最低的抽象层级讲起：计算机箱物料清单（BoM），它是集群中最昂贵的部分。默认的计算机箱 BoM 报价往往采用顶尖配置——Supermicro、Dell 等 OEM 起初会报出接近顶配的 Intel Emerald Rapids CPU，以及配备 2TB 内存和 30TB 本地 NVMe SSD 闪存的整机配置。

微调这份报价是 AI 新兴 GPU 云最容易上手的一项优化。优化的第一步是改选中端 Intel CPU，因为许多客户的工作负载本来就用不了多少 CPU。LLM 训练是重度消耗 GPU 的工作负载，但对 CPU 来说负载强度极轻。CPU 主要跑的是一些简单任务：PyTorch 及其他控制 GPU 的进程、发起网络与存储调用，可能再加上一个 hypervisor。

![](https://substack-post-media.s3.amazonaws.com/public/images/63bed6d9-bb0b-4203-858d-64842590b4a9_1335x800.png)
*来源：SuperMicro*

总体而言，虽然在大多数纯 CPU 任务上 AMD CPU 更强，但我们建议使用 Intel CPU：在 Intel 平台上更容易把 NCCL 性能调对、更容易做虚拟化，整体体验的坑也更少。

举例来说，在 AMD CPU 上，你需要设置 NCCL_IB_PCI_RELAXED_ORDERING 并反复尝试不同的 NUMA NPS 配置才能达到可接受的性能。如果打算做虚拟化，你必须把虚拟核心正确绑定到对应的 NUMA 区域，否则 Device-to-Host 与 Host-to-Device 的带宽和时延都不会理想。说清楚一点：如果你技术过硬，这并非做不到。

许多标准配置带 2TB CPU DDR5 内存，但你的大多数客户用不了那么多。内存是计算机箱 BoM 中第四贵的部件。我们建议从标准的 2TB 降配到仅 1TB。你的新兴 GPU 云的客户多半不会过问内存容量，因为他们的工作负载根本不受 CPU 内存限制。

![](https://substack-post-media.s3.amazonaws.com/public/images/72b39708-91f7-404f-b058-e17879ea5e10_1071x535.png)
*来源：SemiAnalysis*
![](https://substack-post-media.s3.amazonaws.com/public/images/968dd75b-9eed-4329-9044-572c2dba3bca_1096x714.jpeg)
*来源：SuperMicro*

跳出核心计算部件，另一个潜在的省钱点是删掉标准报价中配备的两块 NVIDIA Bluefield-3 DPU。这类 DPU 最初被开发并兜售时，更多是面向传统 CPU 云的一种降本手段——让更多 CPU 核心可以拿来出租，而不必让这些核心去跑网络虚拟化。

但你的新兴 GPU 云客户反正用不了多少 CPU 算力，用一部分宿主机 CPU 核心跑网络虚拟化无伤大雅。更何况很多时候你本来就会把裸金属服务器直接交给客户，根本不需要任何网络虚拟化。再者，Bluefield-3 DPU 相当昂贵，贵到再买一颗 54 核 CPU 都比买一块 Bluefield-3 便宜。干脆跳过 Bluefield-3，前端直接用标准的 ConnectX 网卡。

![](https://substack-post-media.s3.amazonaws.com/public/images/63b4952d-4ea0-46d6-93f5-8ae99ce7b750_1600x900.jpeg)
*来源：Nvidia*

把上述前几项成本优化合在一起，我们估算可节省 $13.6k，把单个计算节点（即一台服务器）的成本从 $270k USD 降到 $256.4k USD——大约省 5%。在 128 个计算节点组成的 1024 H100 集群里，合计节省 $1.74M USD。随着采购量足够大，价格还能更低。如需谈判与设计方面的协助，请联系我们。

![](https://substack-post-media.s3.amazonaws.com/public/images/16e77c19-2983-4e15-ad3f-6dc0242aa617_1063x597.png)
*来源：SemiAnalysis*

在典型 BoM 中，每台 H100 计算服务器配 8 块 400Gbit/s ConnectX-7 NIC，每台服务器总带宽 3,200Gbit/s。一些新兴 GPU 云只选配 4 块 NIC，后端网络带宽因此减少 50%。

虽然我们认为对某些工作负载而言，这样做或许能带来更优的性能/总拥有成本比，但大多数新兴 GPU 云的目标客户对每台计算服务器低于 8x400Gbit/s InfiniBand 带宽的配置毫无兴趣，因为这确实影响工作负载性能。这也是许多公司对 Google Cloud「过敏」的主要原因之一：Google Cloud 部署的 H100 采用 8x200G 以太网（Falcon/GRD）。即便 Google 由此省了钱，在某些情况下这仍会拖累性能。

![](https://substack-post-media.s3.amazonaws.com/public/images/ee205804-b185-4716-ae4e-dccfd43c714f_1266x697.jpeg)
*来源：Nvidia*

机柜级暂且跳过，我们直接进入集群级 BoM，先从网络说起——它是继计算节点之后最大的集群成本项。

## 集群级——网络物料清单

H100 集群中有三张不同的网络：

- 前端网络（以太网）
- 后端网络（InfiniBand 或 RoCEv2 以太网）
- 带外管理网络

简单复习一下：前端网络就是一张普通以太网，用于连接互联网、SLURM/Kubernetes，以及连接用于加载训练数据和模型 checkpoint 的网络存储。这张网络通常按每 GPU 25-50Gb/s 配置，因此在 HGX H100 服务器上，相当于每台 200-400Gbit/s。

与之相对，后端计算网络用于把 GPU-GPU 通信从几十个机柜扩展到数千个机柜。这张网络既可以采用 Nvidia 的 InfiniBand 或 Nvidia 的 Spectrum-X 以太网，也可以采用 Broadcom 等交换芯片厂商的以太网方案，通过 Arista、Cisco 以及各家 OEM/ODM 提供设备。Nvidia 的选项比 Broadcom 以太网方案更贵。尽管按性能/TCO 论以太网并不吃亏，我们仍建议新兴 GPU 云选用 InfiniBand 或 Spectrum X：它性能最好，也最好卖，因为客户已经把 InfiniBand 与最佳性能画上了等号。客户常常以为以太网「性能差得多」，尽管事实并非如此。这种印象主要源于：新兴 GPU 云和客户必须做一系列工程优化才能把 NCCL 调到最优。我们做过这些优化，除非你有过硬的工程人才和时间，否则并不轻松。此外，许多人相信 Nvidia 会把优先的产能配给留给采购其网络方案的客户。

最后是带外管理网络。它用于重装操作系统镜像、监控节点健康状态（风扇转速、温度、功耗等）。服务器上的基板管理控制器（BMC）、PDU、交换机、CDU 通常都接入这张网络，用于监控和控制服务器及其他各类 IT 设备。

前端网络方面，Nvidia 和 OEM/系统集成商通常会在服务器上配 2x200GbE 前端网络连接，并用 Nvidia Spectrum 以太网 SN4600 交换机组网。但我们不建议这样做：每台 HGX 服务器 400Gbit/s 的带宽远超客户可能用到的量。客户只会用前端网络做存储与互联网调用，以及 SLURM 和 Kubernetes 的带内管理。由于前端网络不会承载时延敏感、带宽密集的梯度 All Reduce 集合通信，每台 400Gbit/s 属于严重超配。因此就整体前端网络部署而言，我们建议改用 Arista、Cisco 或各家 OEM/ODM 的通用以太网交换机，每台 HGX 服务器只配 2x100GbE。

下一个唾手可得的优化点在带外管理网络。默认 BoM 包含 SN2201 Nvidia Spectrum 1GbE 交换机，但其价格溢价可观，对带外网络这么简单的东西来说难以 justify。这就好比放着通用名布洛芬（Ibuprofen）不买，去买品牌 Advil。使用任何通用带外交换机都能降低带外网络成本，因此我们建议使用通用 1GbE 交换机。

![](https://substack-post-media.s3.amazonaws.com/public/images/58fa8d97-61bc-4286-9bba-2e825ea03d64_1482x907.png)
*来源：SemiAnalysis*

## 优化后端网络

后端网络的选择要复杂得多，需要对高性能网络有深得多的理解——而新兴的新锐 GPU 云公司恰恰时常缺乏这种理解。这张网络要承载大象级突发的 All Reduce、All Gather、Reduce Scatter，也就是你的各类集合通信。由于集合通信的突发特性，后端网络的流量形态与传统云网络完全不同。

我们先讲 Nvidia 参考网络拓扑。参考拓扑是一个两层、8 轨道优化（rail-optimized）、无阻塞互连的胖树。在无阻塞胖树网络中，如果把节点任意两两配对，所有配对都应能同时以全带宽互通。当然在实践中，由于拥塞、不完美的自适应路由以及额外交换跳数带来的时延，往往达不到理想状态。

![](https://substack-post-media.s3.amazonaws.com/public/images/f2ff06f5-cc7f-4c7a-9bce-12c6d919d308_1117x740.jpeg)
*来源：Nvidia*

当一张网络做了 8 轨道优化时，不再是 4 台服务器的全部 32 个 GPU 都接入同一台机柜顶（ToR）交换机，而是 32 台服务器里 8 个 GPU 编号中的每一个编号都有自己的专属交换机。也就是说，所有 32 台服务器的 0 号 GPU 都接到 0 号 leaf 交换机，所有 1 号 GPU 都接到 1 号 leaf 交换机，依此类推。

轨道优化网络的主要好处是减少拥塞。如果同一台服务器的所有 GPU 都接到同一台 ToR 交换机，当它们同时向网络发送流量时，这些流量试图使用相同链路穿越胖树网络的概率会非常高，从而导致拥塞。用于 AI 训练的 GPU 本来就应该被预期为经常性地一齐发送数据，因为交换梯度、更新新参数都需要集合操作。

下面第一幅图展示的是 8 轨道优化网络：集合通信产生的 8 条并行流分别接入 8 台不同的 leaf 交换机；第二幅图则是非轨道优化设计：服务器统一接入一台 ToR 交换机。

![](https://substack-post-media.s3.amazonaws.com/public/images/497421ba-645e-4c36-b28b-550698de7582_1614x781.png)
*来源：SemiAnalysis*
![](https://substack-post-media.s3.amazonaws.com/public/images/587968b2-ca33-48bc-b1a7-d6965c8a6ff7_1809x792.png)
*来源：SemiAnalysis*

Nvidia 参考架构还把集群划分为 4 个 pod（也称可扩展单元，scalable unit，SU），每个 pod 含 32 台 HGX 服务器（256 颗 H100）和 8 条轨道。同一 pod 内，任一 GPU 编号到其他服务器中相同编号的 GPU 永远只有一跳。这一点很重要，因为它减少了 spine 交换机上的网络流量——即便在无阻塞网络中，spine 也很容易成为拥塞热点。

与普遍看法相反，轨道优化以及顶层流量/拥塞的削减，在 GPU 新兴 GPU 云这类多租户环境（租户/客户并存是常态）中尤其重要。在 8 轨道优化网络中，每个工作负载的全部 8 条流在物理上彼此隔离，因此不会发生路由/交换冲突。在我们即将推出的 Nvidia NCCL 与 AMD RCCL 集合通信深度解析中，我们将讨论轨道优化配置的好处，以及为什么拥塞可能成为严重问题——对 AI 新兴 GPU 云这类多租户环境尤甚。

遗憾的是，拥塞很难通过 nccl-tests 之类工具测出来，只有真实世界的并发工作负载才能揭示噪声邻居（noisy neighbor）/拥塞问题如何影响端到端工作负载吞吐。租户之间只要没有物理隔离，噪声邻居就永远存在。基于我们对拥塞的观察，我们强烈建议采用某种形式的 8 轨道优化拓扑。

轨道优化拓扑还有一点好处：由于大多数流量都局限在 leaf 交换机本地，可以对网络的 spine 层做超额订阅（oversubscription）——这一架构优化我们将在本文后文讨论。

![](https://substack-post-media.s3.amazonaws.com/public/images/cfc524f0-4cbc-4066-97b2-cb4eaf029fc5_1139x791.jpeg)
*来源：Nvidia*

## 光网络与电网络的优化取舍

网络中使用光模块的优势是传输距离长得多，缺点则是额外功耗与极其高昂的光收发器成本——在必须直接向 Nvidia 采购时尤其如此（InfiniBand 网络基本只能这样）。优化物理网络拓扑和机柜布局可以减少光收发器的使用，把它留给真正需要长距离连接的场景。

![](https://substack-post-media.s3.amazonaws.com/public/images/91bf1126-5981-423a-af5c-62630a6c95f7_1536x2048.jpeg)
*来源：Daniel Gross*

在 Nvidia 参考设计中，leaf 交换机位于一个单独的网络机柜，spine 交换机位于另一个专用网络机柜，这意味着必须 100% 使用光模块。

![](https://substack-post-media.s3.amazonaws.com/public/images/092c5674-ef7c-479d-9d1f-a005aeae3380_1614x781.png)
*来源：SemiAnalysis*

为此可以考虑的一种网络拓扑是**无阻塞机柜顶（ToR）设计**。传统网络背景出身的人对这种设计一眼就熟——它是传统网络中最常见的设计：在机柜中部或顶部放一台交换机，连接机柜内所有服务器。由于 ToR 交换机到服务器的距离不足 3 米，我们可以用「廉价」的无源铜缆——即直接连接铜缆（DAC）——把服务器连到 leaf 交换机。对于这种设计，我们建议把 InfiniBand 交换机放在机柜中部，以缩短 DAC 线缆的走线距离。

![](https://substack-post-media.s3.amazonaws.com/public/images/0019415d-e1d3-444a-8832-e47289c0f423_476x957.png)
*来源：SemiAnalysis*

从 leaf 交换机到顶层的 spine 交换机，我们仍然不得不用光模块。这很昂贵，但至少 50% 的连接如今换成了更便宜的 DAC 铜缆。

![](https://substack-post-media.s3.amazonaws.com/public/images/18db89ee-bd81-4a91-a16c-d60cdc61aed6_1809x792.png)
*来源：SemiAnalysis*

遗憾的是，这种设计无法实现 8 轨道优化网络，因此即便网络无阻塞，spine 层也常常出现拥塞热点，因为现在有 8 条流要跨越多级交换机，每条流都需要动态使用不同路径来避开拥塞。在完美的自适应路由存在的理想世界里，ToR 会是一种运转良好的拓扑，因为路由总能绕开拥塞路径。但现实中完美的自适应路由并不存在，采用这种拓扑会严重损害网络性能。

![](https://substack-post-media.s3.amazonaws.com/public/images/d01d6f51-a490-44a0-a1e8-fbf7b375b094_1024x947.png)
*来源：Nvidia*

下图是我们对这种无阻塞 ToR 网络仿真得到的热力图：颜色越浅表示拥塞导致的可用带宽越低，深蓝表示接近满线速。可以看到，采用 ToR 拓扑时虽然能够达到线速，但由于 8 条流全部涌入一台交换机，拥塞依然相当可观，这些流的吞吐因拥塞而变得抖动更大、带宽更低。

![](https://substack-post-media.s3.amazonaws.com/public/images/b5106d7c-44de-452b-bb60-c48c11160878_908x917.png)
*来源：SemiAnalysis*

尽管这种设计对新兴 GPU 云这类多租户环境来说性能并不出色，但省下的钱非常可观——可节省 34.8% 的后端 InfiniBand 网络造价。

![](https://substack-post-media.s3.amazonaws.com/public/images/8a21dcfd-a0da-4602-8c5f-2f0457f56b1b_1235x326.png)
*来源：SemiAnalysis*

## 虚拟模块化交换机

**那么，能不能两全其美——既得到 8 轨道优化的性能优势，又享受 ToR 的成本节约？**

这就轮到虚拟模块化交换机（virtual modular switch）登场了。它的逻辑拓扑与 Nvidia 参考设计相同，但凭借巧妙的机房平面规划和交换机点位规划，leaf 到 spine 交换机之间可以使用铜缆。

![](https://substack-post-media.s3.amazonaws.com/public/images/68c906c0-8d32-4fae-9809-fa4180c29ae6_1644x763.png)
*来源：SemiAnalysis*

基本思路是把交换机机柜彼此紧邻摆放：spine 交换机位于中间机柜，leaf 交换机位于左右两侧机柜，如下图的示意。这样，leaf 与 spine 交换机之间的连接可以全部走铜缆，而服务器与 leaf 交换机之间的连接仍使用光模块。

由于拓扑仍是 8 轨道优化，8 条流中的每一条都在物理上彼此隔离，拥塞大幅减少。

这种设计理应让我们鱼与熊掌兼得，那么这种拓扑的缺点是什么？

遗憾的是，这些交换机之间的 DAC 铜缆往往弯曲半径很差、线缆很粗，会阻挡气流。我们见过这类设计在生产环境中部署，只要理线做得好，这些问题可以克服。也可以用有源铜缆（ACC）来解决——ACC 几乎和多模光纤一样细，弯曲半径也理想。遗憾的是，我们听说的一个潜在问题是 Nvidia LinkX NDR ACC 线缆的误码率不太理想。

![](https://substack-post-media.s3.amazonaws.com/public/images/d0ea1dbf-324f-4994-96f2-a0e765f167ad_1115x825.png)
*来源：SemiAnalysis*

采用这种无阻塞虚拟模块化交换机设计，与参考架构相比，**后端网络可节省 24.9%**，同时性能不变。另一个巨大好处是，无源铜缆通常远比光收发器可靠。收发器故障率很高，激光器是主要的失效部件。高故障率带来更换收发器部件、集群停机和维修人力的成本。

![](https://substack-post-media.s3.amazonaws.com/public/images/2ff4aceb-191d-4f40-98ec-1ddb117f8bd7_1695x518.png)
*来源：SemiAnalysis*

## 后端网络超额订阅优化

我们可以更进一步，摆脱「网络必须无阻塞」这一约束，把成本优化再推一步。在 8 轨道优化设计中，大多数流量都局限在 32 台服务器的 pod 内部，加上 InfiniBand 的自适应路由足够好用，你可以在 leaf 到 spine 之间设计超额订阅。即使集群由单一租户只跑一个工作负载，这样做也有收益。使用 1024 GPU 时，单个模型副本永远不会超过 256 GPU。这意味着带宽消耗通常更大的张量并行、专家并行和流水线并行将在 32 台服务器的 pod 内运行。

这部分流量将局限在第一层交换机本地，而带宽压力较轻的数据并行、梯度和 All Reduce 则跨越 spine 交换机进行。由于 spine 层的带宽需求处于频谱的低端，且 InfiniBand 的自适应路由足够好用，仅靠设计就能实现超额订阅。

在 Meta 的 24k H100 集群上，他们在 pod 之间实现了 7:1 的超额订阅；但我们认为设计上保守一些更有道理，小型集群我们建议只用 2:1 超额订阅。

![](https://substack-post-media.s3.amazonaws.com/public/images/afab1c3f-be0c-4b90-9251-67983663f899_1591x763.png)
*来源：SemiAnalysis*

这种设计的好处是：1024 颗 H100 所需的 spine 交换机从 16 台降到 8 台。把 2:1 超额订阅与虚拟模块化交换机设计结合后，中间机柜里的交换机更少，理线也轻松得多。另一个好处是 leaf 交换机上留出了空余端口，将来当 pod 间流量变重时，你可以轻松加设更多 spine 交换机、降低超额订阅程度。

![](https://substack-post-media.s3.amazonaws.com/public/images/62e95616-536e-4220-9fa8-59bd219fe913_1391x1064.png)
*来源：SemiAnalysis*

我们估算，2:1 超额订阅加**虚拟模块化交换机相比参考架构可节省 31.6%**，比只用无阻塞虚拟模块化交换机设计时的 24.9% 更进一步。无阻塞设计唯一的缺点（除了更贵之外）是：你需要把客户相当合理地分配到物理服务器上，并避免在 pod 边界出现碎片化。我们相信，一支称职的团队可以轻松做到。

![](https://substack-post-media.s3.amazonaws.com/public/images/ebabc5ab-04bb-455c-a9f2-6e6175818646_1697x526.png)
*来源：SemiAnalysis*

Nvidia 也通过 CS9500 系列为 NDR InfiniBand 提供了自己的物理模块化交换机。你可以用这种交换机构建同样的 8 轨道优化胖树拓扑，也可以按需做超额订阅。这种模块化交换机最多支持 2048 个 400Gbit/s 外部端口，因此可扩展至连接 2048 颗 H100。spine 交换机 ASIC 位于机柜后侧，leaf 交换机 ASIC 与 OSFP 笼口位于机柜前侧。spine 交换机 ASIC 通过铜背板与 leaf 交换机 ASIC 相连，类似于 NVL72 的背板。遗憾的是，它只提供液冷方案。

CS9500 的液冷要求正是我们建议大多数新兴 GPU 云部署虚拟模块化交换机而非物理模块化交换机的原因。当前 GB200 带来的液冷就绪数据中心机房需求，加上机房供给整体紧张，意味着新锐 GPU 云很难拿到价格合理的产能。由于 Nvidia 按对终端用户的价值定价，而这种物理模块化交换机对大型集群部署（量级在 O(10k) 到 O(100k)）可能非常有价值，我们认为它的成本高于自建虚拟模块化交换机。

![](https://substack-post-media.s3.amazonaws.com/public/images/8d7bf232-cdad-4f48-b5ad-957d4ab64a87_1000x667.jpeg)
*来源：FRONTERA*

遗憾的是，使用 InfiniBand 的缺点之一是：想要一个像样的 REST 接口，你就得购买 UFM 管理许可证。统一网络管理器（Unified Fabric Manager，UFM）是 Nvidia 提供的软件包，负责网络管理、性能优化与监控。2048 GPU 以下的集群建议使用 UFM，更大规模的集群则硬性要求 UFM。UFM 许可证按 NIC 端点计费，也就是说，一个 1024 GPU 集群需要购买 1024 个许可证。

不购买 UFM 的替代方案是使用开放子网管理器（open subnet manager），但它只能通过终端命令行使用；好在你可以搭一个简单的 REST 服务器封装这些命令行，用 Python 的 subprocess 库代为执行。对于你的第一个集群，我们建议直接购买 UFM 许可证；但对于后续集群，我们建议新兴 GPU 云研究这条路子以节省成本。

## AI 新兴 GPU 云的存储

接下来谈 H100 集群中下一个最昂贵的部分：网络化 NVMe 存储。这是所有客户都想要的东西，也是运行 SLURM 的事实性前提。存储部署基本只有两个条目：你的物理存储服务器，以及 Weka、Vast Data 等存储软件厂商的许可证。这两家因与 OEM 的渠道合作而成为最流行的供应商。

![](https://substack-post-media.s3.amazonaws.com/public/images/760cc81a-a5d9-4519-8320-9076c85068cb_1003x478.png)
*来源：Weka*

为了高可用，大多数存储软件厂商建议至少部署 8 台存储服务器。实际上，大多数新兴 GPU 云也只部署 8 台这一最低配置。有 8 台存储服务器，在大块尺寸下，所有存储服务器合计可提供 250GByte/s 至 400GByte/s 的聚合存储带宽。对于你能在 1024 颗 H100 上运行的绝大多数或合理或不合理 AI 工作负载，这都绰绰有余。

![](https://substack-post-media.s3.amazonaws.com/public/images/22a384bd-f52a-4d19-8262-1276c49355dd_572x272.png)
*来源：SuperMicro*

由于存储设备交期很短，对于 1024 H100 集群，我们建议起步先配 2 PetaByte 总存储容量，之后若发现客户用满了已部署容量，再轻松扩容即可。我们的建议是：在存储部署中预留足够的端口、NVMe 盘位、电力和机柜空间，以便轻松扩展。存储成本的大头在存储软件许可证，而不在物理存储服务器本身。

![](https://substack-post-media.s3.amazonaws.com/public/images/9f55223b-d43a-4e0b-b06e-c73426cb055e_1240x199.png)
*来源：SemiAnalysis*

虽然你的存储服务器可以跑在 InfiniBand 后端计算网络上，但凡是试过的人都掉了不少头发！这种部署通常会把 0 号 GPU 的 IB NIC 同时兼作存储 NIC。在跑分式的存储基准测试中，它能给出漂亮的时延和带宽；但在真实工作负载下，这会让你的 0 号 GPU 成为掉队者（straggler），因为把 IB NIC 用于存储会造成冲突。当存储集群中的磁盘故障触发重建时，计算网络上会出现可观的流量，导致更严重的拥塞。你也可以另购一张专用存储网络，但那属于过度设计——把存储流量放在前端网络上就够了。

我们的建议是：把存储服务器和存储流量放在前端网络上。前端网络经常处于利用率不足的状态，因为它主要承载互联网流量、SLURM/Kubernetes 管理和容器镜像拉取。

## 更多网络管理与软件包

在带内管理方面，为了运行高可用的 UFM 和 CPU 管理节点，我们建议至少部署 3 个 CPU 节点。这 3 个节点中，两个需要配 ConnectX NIC 来管理 InfiniBand 网络，第三个 CPU 节点仅用于其他非 InfiniBand 的管理任务。此外还需要一些杂项 IT 设备，如物理防火墙、42U 机柜、带监控的 PDU 等，但这些物件的价格对集群总资本开支影响不大。

在默认的 Superpod 参考架构中，Nvidia 及其 OEM 合作伙伴会试图向你推销一款叫「Nvidia AI Enterprise」或「Base Command Manager（BCM）」的软件，其建议零售价为每 GPU 每年 $4,500。BCM 是一个提供 AI 工作流与集群管理的软件包，但大多数客户会自行满足其工作流需求，因此对新兴 GPU 云业务而言这款软件价值不大，可销售代表仍会把它塞进首张采购订单里推销。这是我们的 SemiAnalysis 优化集群 BoM 中另一个可大幅省钱的来源。

## 集群 BoM 资本开支小结：参考架构对比 SemiAnalysis 优化架构

如下所示，采用 Nvidia Superpod 参考架构（RA）时，集群的全包成本约为每台计算服务器 ~$318k（不含存储）；而采用带 2:1 超额订阅的 SemiAnalysis 优化架构时，全包总成本仅为每台计算服务器 $283k（同样不含存储）。我们曾通过谈判协助和进一步的成本削减（尤其是大型集群），帮助新兴 GPU 云实现超出图中所示的更深度优化。

![](https://substack-post-media.s3.amazonaws.com/public/images/ea96c5ef-d5e8-4f71-8820-0e3fe395faea_1480x911.png)
*来源：SemiAnalysis*

## 驱动、用户体验与软件

如果你来自大型科技公司或国家 HPC 实验室，用户需求是明摆着的：用户要能正常使用的 GPU、网络、正确安装的驱动、可用的共享存储，以及 SLURM 或 Kubernetes 这样的调度器。然而现实是，绝大多数新兴 GPU 云无法满足这些用户需求，用户体验因而很糟糕。

先说运行 GPU 所需的 GPU 驱动——我们需要 cuda-drivers-5xx 和 fabricmanager-5xx，以及 cuda-toolkit-12-x。

Cuda-drivers-5xx 是 ubuntu/Linux 与 GPU 交互所需的内核态 Nvidia 驱动。接下来是 fabricmanager-5xx，这个软件包负责配置节点内的 NVLink 网络。没有 fabricmanager-5xx，节点内的 8 颗 GPU 将无法通过 NVLink 相互通信。Cuda-toolkit-12-x 则是包含所有用户态工具和 API 的工具包，比如 NVCC——把 CUDA C++ 代码编译成 PTX 汇编和 Nvidia 机器码的编译器。

网络方面，每台 GPU 服务器都需要安装 Mellanox OpenFabrics Enterprise Distribution（MLNX_OFED）驱动。这个软件包是 ConnectX-7 InfiniBand NIC 执行 RDMA（Remote Direct Memory Access，远程直接内存访问）并绕过操作系统内核所需的驱动。要让 GPU 直接与 NIC 通信，你还需要 [GPUDirect RDMA——一个附加的内核驱动，包含在 cuda-drivers-5xx 中但默认未启用](https://docs.nvidia.com/cuda/gpudirect-rdma/)。没有这个驱动，GPU 必须先把消息缓存在 CPU 内存中，才能送往 NIC。启用 GPUDirect RDMA 的命令是 `sudo modprobe nvidia-peermem`。要进一步优化 GPU 与 NIC 的通信，还需要下载一个叫 Nvidia HPC-X 的软件包。

没有上述 GPUDirect RDMA 和 HPC-X 软件包，你的 GPU 在每 GPU 400Gbit/s 的线速下只能以 80Gbit/s 收发流量。启用这些软件包后，[你的点对点收发速率](https://github.com/linux-rdma/perftest)应能在 400Gbit/s 线速下达到 391Gbit/s。

接下来，用户会想要调度与作业启动软件。在新兴 GPU 云市场，70% 的用户要求 SLURM 开箱即用，另有 20% 要求 Kubernetes 开箱即用，最后 10% 大多想自行安装调度器。

新兴 GPU 云必须做到 SLURM 或 Kubernetes 开箱即用，这一点相当重要，因为终端用户通常不擅长安装这类调度器。来自大型科技公司或国家/大学实验室的用户，背后通常有专人负责安装和运维这些 SLURM 软件。终端用户若要自己花 1-2 天安装 SLURM，代价不菲——安装期间他们实际上在为一座闲置的 GPU 集群付钱。

最后，100% 的客户还必须能够在需要时手动获得进入 GPU 节点的交互式终端（即 ssh）——托管式 SLURM 天然提供这一功能。有了 SLURM，你只需运行 `srun –gres=gpu=8 -w NODE_NAME –pty bash` 就能进入任意节点的交互式终端。

像 Crusoe 和 TogetherAI 这样的新兴 GPU 云是黄金标准。因为所需的 InfiniBand 驱动、GPU 驱动和调度软件全部开箱即用，它们能比竞争对手收取溢价，客户流失率也更低。

![](https://substack-post-media.s3.amazonaws.com/public/images/f967e248-1abb-43b1-855a-e9c223e37a57_2168x715.png)
*来源：TogetherAI*

构成最低可用体验的下一个用户需求，是响应迅速的共享主目录和共享数据存储目录。所有 GPU 节点和登录节点都会把共享存储挂载在 /home/$USER/ 和 /data 上。这实际上意味着：终端用户无论进入哪个 GPU 节点的交互式终端，节点上都有相同的主目录和文件。这非常棒——分给用户的每个 GPU 节点都成为可互换的，用户不必在意自己用的到底是哪台 GPU 服务器。此外，启动多节点训练作业时，用户的所有代码已自动存在于每个 GPU 节点上，不必再通过 ssh（scp）手动把代码拷到每个节点。

![](https://substack-post-media.s3.amazonaws.com/public/images/26e9a8c7-5a9d-4bb5-af94-4815580fd2f2_1672x747.png)
*来源：SemiAnalysis*

在新兴 GPU 云的存储上，用户最郁闷的两大来源是文件卷随机卸载，以及遇到大量小文件（LOSF）问题。随机卸载问题的解决方案是使用一个叫「[autofs](https://docs.kernel.org/filesystems/autofs.html)」的程序，它能让你的共享文件系统保持挂载。

至于 LOSF 问题，它很容易避免：只有当你决定自建存储方案（比如 NFS 服务器）、而不是付费购买 Weka 或 Vast 这类存储软件时，它才会成为问题。终端用户会很快察觉集群上的 LOSF 问题——如果集群存在 LOSF 问题，光是把 PyTorch 导入 Python 这一步都会彻底卡死。

下图来自我们在 Crusoe 集群上的测试，展示了一个经过优化、没有 LOSF 问题的集群存储方案应有的表现。可以看到，即便 GPU 数量不断放大，把 PyTorch 导入 Python 进程的耗时仍基本保持平坦。

![](https://substack-post-media.s3.amazonaws.com/public/images/2a87294c-f233-42e0-b3f7-c879c1968c7f_1286x852.png)
*来源：SemiAnalysis*

这与运行在未优化共享存储上的集群有天壤之别：在后者上，Python 多节点训练中导入 PyTorch 所需的时间会爆炸式增长，往往导致集群完全不可用。请注意黄金标准 Crusoe 与另一个存在 LOSF 问题的集群的表现差异。

![](https://substack-post-media.s3.amazonaws.com/public/images/6af5f775-b94a-4a24-8e44-3b8142766f80_1286x848.png)
*来源：SemiAnalysis*

## 多租户

除非某个客户（租户）长期整租整个物理集群，否则每个物理集群多半都会有多个并发的客户。这意味着你需要对前端以太网和后端 InfiniBand 网络做隔离，并在客户之间实现存储隔离。每个客户通常整租一台 GPU 服务器，也就是说每台物理服务器只有一个客户，因此计算服务器上并不严格需要虚拟化。在切分节点上花时间不值得。前端以太网的隔离用标准 vLAN 很容易搞定。在 vLAN 中，虽然物理以太网是共享的，但每个客户的节点只能与分配给同一客户的其他节点通信。

![](https://substack-post-media.s3.amazonaws.com/public/images/00d5ed4f-e715-423d-a467-17041697c0d8_1951x760.png)
*来源：SemiAnalysis*

与以太网 vLAN 相比，InfiniBand 的多租户设置和自动化没那么容易，但学习曲线很短。在 InfiniBand 的世界里，网络隔离通过分区键（Partition Key，pKey）实现——本质上与 vLAN 同一概念。每个客户通过 pKey 获得自己隔离的 InfiniBand 网络，只有持有相同 pKey 的节点才能相互通信。

![](https://substack-post-media.s3.amazonaws.com/public/images/5c03fc79-4bc8-436d-adf6-050e5088c01e_1931x734.png)
*来源：SemiAnalysis*

pKey 的创建与挂接既可以通过 UFM 的 UI 仪表盘轻松完成，也可以使用 [UFM REST API](https://docs.nvidia.com/networking/display/ufmenterpriserestapiv6151/pkey+guids+rest+api)。对许多工程师来说，这可能反而比自动化以太网 vLAN 更容易，因为 InfiniBand pKey 有一套好用的 POST/GET/DELETE API。

遗憾的是，我们从自己的测试经验中看到，一些新兴 GPU 云的 pKey 配置不当，导致一家客户的用户能在 InfiniBand 网络上看到其他租户的节点。我们强烈建议客户亲自验证自己的 InfiniBand 网络与其他客户是否妥善隔离。

![](https://substack-post-media.s3.amazonaws.com/public/images/5647d102-d584-4272-8984-bf4b87baf6a0_1195x732.png)
*来源：Nvidia*
![](https://substack-post-media.s3.amazonaws.com/public/images/773ad294-b669-4123-9821-104f9586b038_913x486.png)
*来源：Nvidia*

说到存储，多租户尤为重要。好在存储的管理也相当简单：AI 领域的两大存储供应商 Weka 和 Vast 都把多租户作为一等原语支持。

![](https://substack-post-media.s3.amazonaws.com/public/images/0ace0d0a-eb88-4022-9dfb-86bb0b1b8d39_1986x743.png)
*来源：SemiAnalysis*

在 Weka 和 Vast Data 的软件中，你可以轻松创建租户（在 Weka 中称为 Organization），并为每个存储卷设定只分配给某一个租户的访问控制策略。这些软件提供了强保证：只要策略设置正确，每个客户的用户就只能访问自己的存储卷。

![](https://substack-post-media.s3.amazonaws.com/public/images/a6b3e559-aa4f-4e0d-bff2-84674232ef7d_1572x746.jpeg)
*来源：Vast Data*
![](https://substack-post-media.s3.amazonaws.com/public/images/2fedd95a-3e12-4bad-966a-6c99822de7e7_2304x847.jpeg)
*来源：Weka*

## 裸金属还是虚拟化

对于 H100 SXM，最小算力单位是一台服务器，也就是说每台服务器同一时刻只有一个客户。这意味着可以采用裸金属部署，同时不牺牲安全性。裸金属可行而且确实常见，但我们确实看到使用 VM 有额外好处：更短的平均恢复时间（MTTR）和更强的可靠性。

使用 VM 时，如果客户所用的一台物理 GPU 服务器坏了，新兴 GPU 云可以轻松地在热备机上为客户迁移或新起一台 VM。

![](https://substack-post-media.s3.amazonaws.com/public/images/5f2bf3a7-f690-4f12-8b19-2e432de9f34d_1393x659.png)
*来源：SemiAnalysis*

在 GPU VM 上创建虚拟机可以用 qemu-kvm 这样的开源 hypervisor：启动 VM 时把 vCPU 绑定（pin）到物理 CPU，并留出几个核不绑定、用于运行 hypervisor。

你还需要把 vLAN 以太网接口绑定到 GPU VM 上。用常见 hypervisor 创建 CPU VM 是如今大多数计算机专业毕业生都会的简单任务。要把 VM 变成 GPU VM，你还需要对 GPU 和 InfiniBand NIC 做 PCIe 直通（passthrough）。对新兴 GPU 云而言幸运的是，NVIDIA 迄今还没想出办法对 GPU 和 NIC 的 PCIe 直通收费。我们也见过一些新兴 GPU 云用 [SR-IOV](https://docs.nvidia.com/networking/display/mlnxofedv522230/single+root+io+virtualization+(sr-iov)) 创建虚拟 InfiniBand NIC 并直通进虚拟机，而不只是直通物理 InfiniBand NIC，不过 SR-IOV 并非严格必需。

![](https://substack-post-media.s3.amazonaws.com/public/images/4d6bd621-80ef-4502-9539-cbadecd55803_1995x782.png)
*来源：SemiAnalysis*

还有一步必须记得做：手动通过 NCCL_TOPO_FILE 变量把 NUMA 区域和 PCIe 拓扑文件传入 /etc/nccl.conf，因为 NCCL 和 Nvidia 驱动此刻运行在 GPU VM 内部，无法自动探测 NUMA 区域和 PCIe 拓扑。少了这一步，NCCL 的带宽性能只有应有水平的 50%。

![](https://substack-post-media.s3.amazonaws.com/public/images/031437ff-b5ba-4372-9bba-e43dc5a2abe0_2318x739.jpeg)
*NCCL PCIe 拓扑文件，来源：SemiAnalysis*

与裸金属相比，虚拟机的一个缺点是：由于启用了 [IOMMU](https://lenovopress.lenovo.com/lp1467-an-introduction-to-iommu-infrastructure-in-the-linux-kernel)，CPU 与 GPU 之间的传输带宽和时延略差。但我们认为虚拟机仍然值得用，因为终端用户的平均恢复时间更快，而且 HostToDevice 传输通常本就与计算重叠，终端用户甚至可能察觉不到差别。

由于配有 1-2TB 的 CPU 内存，kvm-qemu hypervisor 开箱即用时 VM 启动很慢。相比之下，cloud-hypervisor 有一项优化：系统用多个 pthread 并行预取（prefault）内存，把 1TB 内存的预取时间从 80 秒缩短到仅 6 秒。这项优化由 Crusoe Cloud 开发，并[幸运地上游合并](https://github.com/cloud-hypervisor/cloud-hypervisor/pull/6156)了。根据我们的测试，Crusoe 的 VM 能在 90 秒内完成启动。

快速启动的重要好处在于：当客户的 GPU 服务器不可避免地发生故障时，新兴 GPU 云运营方可以非常快地在热备节点上部署一台 VM 并加入客户的 SLURM 集群，让客户非常快地恢复训练。

![](https://substack-post-media.s3.amazonaws.com/public/images/0422b889-123d-46a1-9934-2ae81b21e4ff_809x672.png)
*来源：SemiAnalysis*

## 监控与常见错误

监控仪表盘方面，我们至少建议通过 Grafana 和 Prometheus 搭建 Nvidia Datacenter Manager 仪表盘，让用户能追踪 GPU 温度、功耗和活跃的 XID 错误。

![](https://substack-post-media.s3.amazonaws.com/public/images/3211eab1-3966-4347-9c65-354cc707fe61_2974x1604.png)
*来源：SemiAnalysis 内部 GPU 监控仪表盘*

此外，我们还建议新兴 GPU 云安装 ipmi-exporter，监控整体风扇转速、温度及其他 BMC 指标。在运行 CPU 部署时，拥有一个集中汇总这些指标的仪表盘是标准做法。

![](https://substack-post-media.s3.amazonaws.com/public/images/65a202a3-7395-4dbf-9347-63790ee7be76_1920x971.png)
*来源：Grafana*

监控的软件架构是：在每个 GPU 节点上跑 IPMI exporter 和 DCGM exporter，再在一台 CPU 管理节点上部署 Prometheus 抓取器（scraper）与各 GPU exporter 通信，并把数据存入 InfluxDB 数据库。然后，Grafana Web 服务器可以连接 Prometheus，将采集到的数据可视化。

高级的新兴 GPU 云运营方还会部署 promtail 日志器，聚合每台服务器的内核诊断（dmesg）日志。两类需要立即标记的常见 dmesg 信息是「线缆被拔出（Cable being Unplugged）」以及 NIC 和/或收发器温度过热。出现任一信息，多半意味着你有一条抖动（flapping）的 InfiniBand 链路，必须在客户开始流失之前迅速处理。

![](https://substack-post-media.s3.amazonaws.com/public/images/b8e9b925-510d-4315-9580-06309044df97_1208x817.png)
*来源：SemiAnalysis*

另一类常见错误是：GPU 通过 dmesg 或 DCGM XID 错误完全查不出任何报错，却输出错误的矩阵乘法结果。这类错误称为静默数据损坏（SDC）。判断 GPU 上是否存在 SDC 最简单的办法是用 Nvidia DCGMI 诊断 level 4 工具（sudo dcgmi diag -r 4）。该工具能抓住 95% 最常见的 SDC，但不幸会漏掉剩下 5% 的 SDC，带来极其漫长的调试过程和极其愤怒的客户。

NCCL 死锁和卡顿都是非常常见的问题，会让训练作业先卡住 30-35 分钟，然后被 PyTorch 的 NCCL watchdog 整个杀掉。我们认为这是新兴 GPU 云可以为客户创造价值的一个点：自建后台 NCCL 检查器，巡检活跃的 SLURM 作业，看它们在过去 4 分钟内功耗是否一直高于 150W。如果功耗低于 150W，多半说明 NCCL 挂起了、出现了某种死锁，此时应该有一个机器人自动给客户发邮件，提醒他们重启 SLURM 作业。

InfiniBand UFM 最需要跟踪的问题错误码包括：110（Symbol error，符号错误）、112（Link downed，链路断开）、329（Link went down，链路掉线）、702（Port is considered unhealthy，端口被认为不健康）和 918（Symbol bit error warning，符号位错误警告）。我们一般建议：在跟踪 UFM 错误时一旦遇到上述任一错误码，应立即呼叫工程师深入排查。不过现实一点说，等到发现这些问题时，它们多半早已给新兴 GPU 云的许多客户造成严重影响，客户早就把运营方的电话打爆了。

我们强烈建议新兴 GPU 云运营方使用 Jira 之类的工单系统，跟踪所有硬件故障和客户问题。没有工单和客户管理系统，问题就会掉进缝隙，推高客户流失率。

![](https://substack-post-media.s3.amazonaws.com/public/images/6374ba0f-2d5f-4d3a-9b59-e0d90859f2af_1665x860.jpeg)
*TensorWave Jira 门户，来源：TensorWave*

## 更多技巧与测试

另一个我们没见多少新兴 GPU 云运营方使用的功能是 SLURM topology.conf。SLURM 的拓扑配置功能会在启动用户的 SLURM 训练作业时为每个 rank 分配 SLURM_ID，以减少 spine 层流量。对某些关键消息，SLURM_ID 分配不当会导致 20-30% 的减速。我们将在此后推出的 Nvidia NCCL 与 AMD RCCL 集合通信深度解析中进一步讨论。

一般而言，我们建议你使用 [nccl-tests](https://github.com/NVIDIA/nccl-tests) 对整个集群做性能剖析，并与 Nvidia 和你的 OEM 的参考数据对比，看是否存在性能 shortfall 或退化。

为了让 NCCL 测试变得简单，我们正在开发一个一键式工具 ClusterMAX-NCCL，用来运行测试并把你的集群与一组参考结果做对比。

在 ClusterMAX-NCCL 中，我们针对从 16MiB 到 256MiB 的所有重要消息尺寸、所有不同类型的集合通信进行测试。我们最近发布了该工具的 beta 版，支持单节点 NCCL 测试。下面是加载并运行 ClusterMAX-NCCL 的一行命令：

`docker run --gpus all --ipc=host --shm-size 192G -v $(pwd)/results:/workspace/results semianalysiswork/clustermax-nccl`

如果你的节点配置正确，你应当看到类似下面的结果：

![](https://substack-post-media.s3.amazonaws.com/public/images/4e7e7f2a-d70e-4e9c-9b19-41a8033aaeb0_1634x847.png)
*来源：SemiAnalysis*

提供有竞争力的定价、过硬的可靠性和配置正确的集群，构成了大多数新兴 GPU 云价值差异化的主体。在此之外，我们见过的唯一差异化价值来自一家名叫 TogetherAI 的新兴 GPU 云——Flash Attention 的发明人 Tri Dao 在那里工作。TogetherAI 为其 GPU 客户提供一套独家的高度优化 CUDA 内核，可轻松集成进客户现有的训练代码，从而让客户的训练吞吐量快速提升 10-15%。

从根本上说，训练提速 10-15% 意味着客户可以省下 10-15% 的 GPU 开支，或者用同样的 GPU 预算多训 10-15% 的 token，换来模型性能的提升。我们认为，不克隆一个 Tri Dao，Together 创造的价值无法在别处复制。

![](https://substack-post-media.s3.amazonaws.com/public/images/38efa77c-4cb4-41c2-b71e-fb0d8f0a84c2_2000x1064.png)
*来源：TogetherAI*

## 集群部署与验收测试

集群部署通常依托 OEM 的机柜级集成与部署团队。这些团队会在 OEM 的集成工厂里逐台服务器、再全集群地进行集成与测试，期间完成网络测试。我们建议全集群的高温烤机（burn-in）至少持续 3-4 周，以暴露节点元器件的所有早期失效（infant mortality）相关故障。集成团队极力推销用 LINPACK 做烤机和验收流程的做法非常普遍，但我们认为这不是一个很好的测试：LINPACK 对网络的使用不多，也压不出 GPU HBM 的负载，只是反复使用并测试 GPU 的 FP64 核心。相比之下，ML 训练对网络、HBM 和 BF16/FP16/FP8 张量核心的消耗都非常重。因此，我们认为需要一种真正把相关部件「烤」到位的烤机与验收测试。

![](https://substack-post-media.s3.amazonaws.com/public/images/2d3f22fa-4313-439b-ac08-b2d413d36ecf_1193x805.png)
*来源：SemiAnalysis*

在集成工厂完成集成与烤机后，OEM 会把全部机柜和线缆打包，运往新兴 GPU 云的数据中心，随后还需要约两周时间把集群部署进这处托管机房。我们建议集群在 onsite 搭好后，即便集成工厂已经烤过机，也要再做一次 2-3 天的烤机/验收测试，以确保没有硬件在运输或现场部署中受损。一个非常常见的问题是：运输和安装过程中积累在光纤连接端点上的灰尘，导致 InfiniBand 链路抖动。解决办法是清洁抖动端点的光纤端面。不过有时也存在必须找出并解决的更深层问题。

## 日常运营

新兴 GPU 云的日常运营，主要内容就是一个接一个地打地鼠。拥有良好的内部管理和调试工具，能让这个过程顺畅运转、甚至颇为令人享受；但现实往往是新兴 GPU 云没有足够的工程师去做这些工具——讽刺的是，工程师的大部分时间都花在打地鼠上，而不是打造更好的打地鼠工具。

集群里最常冒头的一些地鼠包括：抖动的 IB 收发器、GPU「从总线上掉线」、GPU HBM 错误和 SDC。大多数时候，这些问题只需对物理服务器发起一次硬重启就能解决；很多情况下，做一个 UI 按钮或教客户自己硬断电重启服务器即可。另一些情况下，解决办法是拔下再插回 InfiniBand 收发器，或擦掉光纤线缆上的灰尘。还有些情况，则需要叫来 OEM 或系统集成商走保修 RMA，整机更换服务器。

如前文所述，新兴 GPU 云集群的早期阶段故障非常频繁，因为大多数新兴 GPU 云在交给客户之前不做烤机。正如 Yi Tay 注意到的：不做烤机的集群，可靠性比做烤机测试的集群差几个数量级。

这是 TogetherAI 和 Crusoe 得高分的又一个维度：它们是少数几家在向客户交付集群前进行数周烤机的新兴 GPU 云。此外，聘用并留住了拥有多年 Nvidia GPU 和 InfiniBand 网络运维经验人员的公司，故障率往往会低得多——大量关于搭建可靠集群的知识，属于一部如何正确调试和预防 AI 集群错误的「只可意会」的经验知识库（tribal knowledge）。

![](https://substack-post-media.s3.amazonaws.com/public/images/919e82cd-1005-447c-a0d0-0a6cde699bc1_1294x650.png)
*来源：Yi Tay*

我们看到，顶级 H100 运营方的 512 H100 集群，平均故障间隔时间（MTBF）通常约为 7 天。对这些顶级运营方而言，大多数故障只需重启节点即可轻松修复。

![](https://substack-post-media.s3.amazonaws.com/public/images/b2aea0dc-f580-4c4f-a0e0-89ffb1213e6b_971x356.png)
*来源：SemiAnalysis*

现在，我们转入本篇深度解析的第二部分，重点讨论 AI 新兴 GPU 云的经济学与商业案例。这部分分析对投资者和商业战略分析师尤其有用，但也能为买家提供一些洞见，帮助他们更好地理解这里生效的定价动态与经济学。我们也认为，新兴 GPU 云的所有管理者、工程师、客户和投资者，都应当理解并内化第一部分的 AI 新兴 GPU 云部署深度解析。

## 第二部分：AI 新兴 GPU 云经济学

## 需求生态系统
