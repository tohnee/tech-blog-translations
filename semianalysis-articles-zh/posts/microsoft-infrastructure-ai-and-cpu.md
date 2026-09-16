---
title: "微软基础设施——自研 AI 与 CPU 芯片 Maia 100、Athena、Cobalt 100"
title_en: "Microsoft Infrastructure - AI & CPU Custom Silicon Maia 100, Athena, Cobalt 100"
subtitle: "规格、出货量、GPT-4 性能、下一代时间表/命名、后端设计合作伙伴"
date: 2023-11-15
source: https://newsletter.semianalysis.com/p/microsoft-infrastructure-ai-and-cpu
crawled: 2026-09-15
authors: ["Dylan Patel", "Myron Xie"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 微软基础设施——自研 AI 与 CPU 芯片 Maia 100、Athena、Cobalt 100

> 原文：[Microsoft Infrastructure - AI & CPU Custom Silicon Maia 100, Athena, Cobalt 100](https://newsletter.semianalysis.com/p/microsoft-infrastructure-ai-and-cpu) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**规格、出货量、GPT-4 性能、下一代时间表/命名、后端设计合作伙伴**

微软正在进行人类历史上规模最大的基础设施建设。这话听起来或许像夸张，但只要看看各类[超级工程](https://en.wikipedia.org/wiki/List_of_megaprojects)的年度开支——[全国性铁路网](https://en.wikipedia.org/wiki/List_of_megaprojects#Roads_and_transport_infrastructure)、[大坝](https://en.wikipedia.org/wiki/List_of_megaprojects#Water-related)、乃至[阿波罗登月等太空计划](https://en.wikipedia.org/wiki/List_of_megaprojects#Spacecraft)——它们在微软为 2024 年及以后规划的每年超过 500 亿美元数据中心开支面前全部黯然失色。这轮基础设施建设的目标直指**加速通往 AGI 之路**，并把生成式 AI 的智能带入生活的方方面面，从[生产力应用](https://www.semianalysis.com/p/gpt-4-architecture-infrastructure)到[休闲娱乐](https://www.semianalysis.com/p/ai-doomer-vs-techno-optimist-social)。

虽然中期内微软的 AI 基础设施大部分仍将基于 NVIDIA 的 GPU，但微软正在大力推动供应商多元化，转向其他芯片厂商和自研芯片。我们曾在[1 月详细解析过微软与 AMD MI300 的雄心计划](https://www.semianalysis.com/p/nvidiaopenaitritonpytorch)，最近又分析了[明年的 MI300X 订单量](https://www.semianalysis.com/p/amd-mi300-ramp-gpt-4-performance)。除加速器之外，还有对 800G PAM4 光模块、相干光模块、线缆、散热、CPU、存储、DRAM 及各种其他服务器组件的大量需求。

今天我们想深入探讨微软的自研芯片项目。在今天的 Azure Ignite 发布活动上有两项重大芯片发布：**Cobalt 100 CPU** 和 **Maia 100 AI 加速器（又称 Athena 或 M100）**。微软的系统级方法非常值得关注，因此我们还将讨论 Maia 100 的机柜级设计、网络（Azure Boost 与空心光纤）以及安全。我们将深入解析 Maia 100 的出货量、与 [AMD MI300X](https://www.semianalysis.com/p/amd-mi300-taming-the-hype-ai-performance)、[NVIDIA H100/H200/B100](https://www.semianalysis.com/p/nvidias-plans-to-crush-competition)、[Google TPUv5](https://www.semianalysis.com/p/broadcoms-google-tpu-revenue-explosion)、[Amazon Trainium/Inferentia2](https://www.semianalysis.com/p/amazons-cloud-crisis-how-aws-will) 的竞争力对比，以及微软在 AI 芯片上的长期规划（包括下一代芯片）。我们还将分享听到的关于 Maia 100 在 GPT-3.5 和 GPT-4 模型上的性能信息。

需要指出的是，虽然微软目前在数据中心部署自研芯片方面落后于 Google 和 Amazon，但它的芯片项目历史悠久。举例来说，你知道吗，微软曾开发过一款名为 E2 的自研 CPU，采用自定义指令集，基于 EDGE（显式数据图执行）架构。[他们甚至专门为这个 ISA 移植了 Windows](https://www.theregister.com/2018/06/18/microsoft_e2_edge_windows_10/)！微软历史上一直与 AMD 合作开发半定制游戏主机芯片，如今双方的合作还延伸到了定制的基于 Arm 的 Windows PC 芯片。微软还内部开发了[多代信任根](https://www.semianalysis.com/p/caliptra-first-open-source-silicon)，装在其数据中心部署的每一台服务器上。

微软的 [Project Catapult](https://www.microsoft.com/en-us/research/project/project-catapult/) 项目已运行很长时间，面向搜索、AI 和网络。最初 Project Catapult 完全基于标准 FPGA，但微软最终与 Intel 合作开发定制 FPGA。这款 FPGA 主要为 Bing 服务，但由于 Intel 的执行问题而被迫搁浅。Bing 至今仍严重依赖 FPGA，与之形成对比的是 Google 搜索主要通过 [TPU](https://www.semianalysis.com/p/broadcoms-google-tpu-revenue-explosion) 加速。

作为今日发布的一部分，微软还公布了 Azure Boost 网络适配器，这是一款 200G DPU，基于外部 FPGA 和内部设计的 ASIC 构建。该产品卸载了许多 hypervisor、主机、网络和存储相关任务，但出于某种原因，配备 Azure Boost 的 Azure 实例仍需划出主机 CPU 核心用于基础设施任务。这一点与 [Amazon 的 Nitro 不同——后者将所有主机 CPU 核心都释放给虚拟机](https://www.semianalysis.com/i/108660819/amazon-nitro)。

## **Azure Cobalt 100 CPU**

Azure Cobalt 100 CPU 是微软在其云中部署的第 2 款基于 Arm 的 CPU。它已用于微软内部产品，如 Azure SQL 服务器和 Microsoft Teams。微软部署的第一款基于 Arm 的 CPU 是[从 Ampere Computing 采购的基于 Neoverse N1 的 CPU](https://www.semianalysis.com/p/sound-the-siryn-ampereone-192-core)。Cobalt 100 在此基础上演进，采用 Armv9 的 128 个 Neoverse N2 核心和 12 通道 DDR5。Neoverse N2 相比 Neoverse N1 带来 40% 的性能提升。

Cobalt 100 主要基于 Arm 的 Neoverse Genesis CSS（计算子系统）平台。Arm 的这一产品线偏离了其只授权 IP 的经典商业模式，使得开发一款优秀的基于 Arm 的 CPU 显著更快、更简单、成本更低。

Arm 提供经过验证并完成布局的设计模块，为芯片厂商完成了设计流程中的诸多环节。我们在[此处](https://www.semianalysis.com/p/arm-and-a-leg-arms-quest-to-extract)更详细地解析过这一新商业模式。

就 Cobalt 100 而言，微软将 2 个 Genesis 计算子系统拼接成了 1 颗 CPU。

这类似于[阿里巴巴的倚天 710 CPU](https://www.servethehome.com/arm-based-alibaba-cloud-t-head-yitian-710-crushes-specrate2017_int_base/)，后者同样基于 Neoverse N2。[Chips and Cheese 对此做过剖析。](https://chipsandcheese.com/2023/08/18/arms-neoverse-n2-cortex-a710-for-servers/)

![](https://substack-post-media.s3.amazonaws.com/public/images/792cef96-8110-4fc2-9777-ef1ffc6b99dc_2196x1216.png)

Arm 此前曾夸耀，从项目启动到为某超大规模云厂商拿出可工作的芯片只花了 13 个月。鉴于我们所知 Genesis CSS 的客户只有阿里巴巴和微软两家，而阿里巴巴率先上市，Arm 在下面这张幻灯片里说的很可能就是微软。Google 的 Arm CPU 也有可能采用了 Genesis CSS。

## **Azure Maia 100（Athena）**

微软期待已久的 AI 加速器终于亮相。它是美国四大超大规模云厂商（Amazon、Google、Meta、Microsoft）中最后一家发布产品的。话虽如此，Maia 100 绝非等闲之辈。我们将对比它与 [AMD MI300X](https://www.semianalysis.com/p/amd-mi300-taming-the-hype-ai-performance)、[NVIDIA H100/H200/B100](https://www.semianalysis.com/p/nvidias-plans-to-crush-competition)、[Google TPUv5](https://www.semianalysis.com/p/broadcoms-google-tpu-revenue-explosion)、[Amazon Trainium/Inferentia2](https://www.semianalysis.com/p/amazons-cloud-crisis-how-aws-will) 的性能/TCO。

本文的主体内容在付费墙之后，将包括完整规格、网络配置与拓扑、机柜设计、出货量爬坡、性能、功耗、设计合作伙伴等。这颗芯片有一些非常独特之处，我们认为 ML 研究人员、基础设施从业者、芯片设计团队和投资者都应当了解。

[获取团体订阅 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
