---
title: "AMD MI300——驯服炒作——AI 性能、量产爬坡、客户、成本、IO、网络、软件"
title_en: "AMD MI300 – Taming The Hype – AI Performance, Volume Ramp, Customers, Cost, IO, Networking, Software"
subtitle: "工程上令人惊叹，但通往市场的路呢？"
date: 2023-06-12
source: https://newsletter.semianalysis.com/p/amd-mi300-taming-the-hype-ai-performance
crawled: 2026-09-15
authors: ["Dylan Patel", "George Cozma", "Gerald Wong"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# AMD MI300——驯服炒作——AI 性能、量产爬坡、客户、成本、IO、网络、软件

> 原文：[AMD MI300 – Taming The Hype – AI Performance, Volume Ramp, Customers, Cost, IO, Networking, Software](https://newsletter.semianalysis.com/p/amd-mi300-taming-the-hype-ai-performance) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**工程上令人惊叹，但通往市场的路呢？**

在 GPU 大规模短缺、NVIDIA 相对制造成本收取约 5 倍溢价的背景下，整个行业都在迫切寻找替代方案。虽然凭借成熟的软硬件——[他们的 TPU](https://www.semianalysis.com/p/google-ai-infrastructure-supremacy) 和 [OCS](https://www.semianalysis.com/p/google-apollo-the-3-billion-game)——[Google 在内部 AI 工作负载上相对其他大型科技公司拥有结构性的性能/TCO 优势](https://www.semianalysis.com/p/google-ai-infrastructure-supremacy)，但我们认为存在一些结构性问题，将阻止 Google 成为面向外部市场的领导者。

1. Google TPU 永远只能从 1 家公司的 1 个云上获得。
2. Google [往往要到芯片部署很久之后才公开披露](https://www.semianalysis.com/p/google-ai-infrastructure-supremacy)，而大买家需要在产品发布前就有完整文档，并在量产爬坡前拿到早期试用系统。
3. Google 多年来一直对用户隐瞒多个重要硬件特性，包括[内存/计算相关](https://www.semianalysis.com/i/114314781/google-dlrm-optimizations)和[网络/部署灵活性](https://www.semianalysis.com/i/114314781/google-ocs)方面的特性。
4. Google 拒绝对外提供底层的硬件文档，供那些希望编写自定义核心（kernel）以榨取最大性能的高手使用。

除非 Google 改变其行事方式，否则对 AI 基础设施领域最重大技术进展的层层把守，将使其在结构上相对基于 NVIDIA 的云服务处于被动。其他云厂商的自研芯片，如 [Amazon](https://www.semianalysis.com/p/amazons-cloud-crisis-how-aws-will) 和 [Microsoft](https://twitter.com/dylan522p/status/1648016247575945233?s=20) 的产品，仍然非常非常落后。

在商用芯片（merchant silicon）的世界里，[Cerebras 目前是最近的竞争者，在 GPT-3 上有扎实的性能](https://www.semianalysis.com/p/gpt-model-training-competition-heats)和[令人印象深刻的开源模型](https://www.semianalysis.com/p/google-we-have-no-moat-and-neither)，但其硬件可获得性非常有限——[每台单独的服务器就要数百万美元](https://www.semianalysis.com/i/97006309/the-memory-wall)。在云端使用 Cerebras 的唯一途径是通过他们自己的云服务。缺乏可获得性损害了开发的灵活性。NVIDIA 生态的生命线在于开发者能在各种各样的系统上进行开发，从几百美元的游戏 GPU，到最终能够扩展到本地数万张 GPU 的系统，或与全部第三方云服务商合作。虽然 [Tenstorrent 等其他初创公司展现了潜力](https://www.semianalysis.com/p/tenstorrent-blackhole-grendel-and)，我们认为其软硬件距离真正进入状态还有一段距离。

Intel 是全球最大的商用芯片供应商，尽管收购了 Nervana 和 Habana 两家数据中心 AI 硬件公司，如今却不见踪影。Nervana 在几年前被砍掉，Habana 现在似乎也难逃同样命运。Intel 目前处于第二代 Habana Gaudi 2 阶段，除了 AWS 上可用的少量实例外，几乎无人采用。此外，Intel 已经明确表示这条路线图已死，产品将并入 2025 年的 Falcon Shores GPU。Intel 的 GPU Ponte Vecchio 处境也好不到哪里去。它严重迟到，直到最近才完成向一再推迟的 Aurora 超算的交付，后续产品还要再等 2 年。其性能总体上无法与 NVIDIA 的 H100 GPU 竞争。

顺带一提，我们将于 6 月 27 日在圣何塞主办一场关于开源 AI、AI 硬件和 RISC-V 的讨论，嘉宾包括 Raja Koduri、Tenstorrent 的 Jim Keller、Cerebras 的 Andrew Feldman 以及 Meta 的 Horace He。[免费注册！](https://www.eventbrite.com/e/2023-andes-risc-v-con-silicon-valley-registration-624048886017)

## **AMD MI300：解析炒作从何而来**

要驯服炒作，必须先弄清炒作从何而来。人人都想要替代品。AMD 是唯一一家在高性能计算领域有成功交付芯片记录的公司。虽然这主要体现在其 CPU 业务这台运转良好的执行机器上，但也不止于此。AMD 曾在 2021 年为世界首台 ExaFLOP 级超算 Frontier 交付了 HPC GPU 芯片。虽然为 Frontier 供电的 MI250X 充分完成了其主要使命，但未能在云厂商和超大规模厂商这些大金主那里赢得任何筹码。

现在，所有人都在期待 AMD 将于今年晚些时候交付给其第二个百亿亿次超算项目 El Capitan 的 MI300。正因如此，AMD 即将推出的 MI300 GPU 是离开 NVIDIA 领地之后被讨论最多的芯片之一。SemiAnalysis [自去年上半年以来一直在讨论 MI300 芯片的进展](https://www.semianalysis.com/i/59924892/datacenter-gpu-and-ai)。我们也一直密切关注其软件生态，包括 [Meta 的 PyTorch 2.0 和 OpenAI 的 Triton](https://www.semianalysis.com/p/nvidiaopenaitritonpytorch)。自 NVIDIA 的 Volta GPU 和 AMD 的 Rome CPU 之后，还没有哪款数据中心芯片引发过这么大的热度。

![](https://substack-post-media.s3.amazonaws.com/public/images/bfd1877e-4029-4c7e-b702-a2f75a8b2d31_2880x3016.png)

MI300，代号 Aqua Vanjaram，由多个复杂层级的硅片组成，坦率地说是一项工程奇迹。CEO 苏姿丰（Lisa Su）今年早些时候在 CES 上举起过 MI300 封装，让我们得以一窥 MI300 的结构。我们看到 4 个象限的硅片，周围环绕着 8 个 HBM 堆叠。那是 HBM3 中最高 5.6 GT/s 的速度档，8 个 16GB 或 24GB 堆叠组成 128GB 或 192GB 统一内存，带宽高达 5.6 TB/s。

**与带宽 3.3 TB/s 的 NVIDIA H100 SXM 80GB 相比，[带宽高出 72%，容量高出 60% 至 140%](https://www.semianalysis.com/p/nvidiaopenaitritonpytorch)。**

AMD 能否分到 AI 计算的任何一块蛋糕，最终归结为能否成为超大规模云厂商相对于 NVIDIA 的可靠第二供应源。其前提假设是「水涨众船高」。想必，AI 数据中心基础设施上的巨额开支总会以某种方式惠及 AMD，对吧？

恐怕不然，AMD 硬件在这场 AI 支出狂潮中顶多算个脚注。事实上，[目前 AMD 是生成式 AI 基础设施建设中的相对输家](https://www.semianalysis.com/p/ai-server-cost-analysis-memory-is)，原因在于其数据中心 GPU 屡屡失利、未能拿下 HGX H100 系统的 CPU 订单，以及[整体支出从 CPU 转移](https://www.semianalysis.com/p/ai-server-cost-analysis-memory-is)。因此，MI300 的成功至关重要。

本报告将揭开 AMD MI300 的面纱。我们将涵盖小芯片（chiplet）设计、架构、IO 速率、系统工程、FLOPS、性能、制造成本、设计成本、发布时点、量产爬坡、软件和客户。虽然各版本面向不同市场，我们将特别聚焦面向 AI 的版本。

请注意，这是我们数月来持续向客户提供的一份报告及点评的扩展版。先从硬件基本构建模块开始，再谈更偏商业层面的内容。

## **基础构建模块——Elk Range 有源中介层裸片（AID）**

MI300 的所有版本都始于同一个基础构建模块，即 AID（active interposer die，有源中介层裸片）。这颗小芯片名为 Elk Range，采用 TSMC N6 工艺制造，尺寸约 370mm²。该芯片容纳了 2 个 HBM 内存控制器、64MB 内存挂载末级缓存（MALL，Memory Attached Last Level）Infinity Cache、3 个最新一代视频解码引擎、36 条 xGMI/PCIe/CXL 通道，以及 AMD 的片上网络（NOC）。在 4 裸片配置下，MALL 缓存合计 256MB，而 H100 只有 50MB。

AID 最重要的特性在于它对 CPU 与 GPU 计算是模块化的。[AMD 和 TSMC 使用混合键合](https://www.semianalysis.com/p/advanced-packaging-part-2-review)将 AID 与其他小芯片相连。这种通过铜硅通孔（TSV）实现的连接，使 AMD 可以灵活搭配最优的 CPU 与 GPU 比例。4 个 AID 之间的对分带宽超过 4.3 TB/s，由超短距（USR）物理层实现，与 AMD Navi31 游戏 GPU 小芯片互连中的做法类似，只不过这次同时具备水平和垂直链路，且读写带宽对称。方形拓扑还意味着，对角线连接需要 2 跳，而相邻 AID 之间只需 1 跳。

![](https://substack-post-media.s3.amazonaws.com/public/images/22b60d95-2275-4ce3-9efb-b1e437d52450_2880x3016.png)

依 MI300 版本不同，2 个或 4 个带有不同计算配置的 AID 被组合到 [CoWoS 硅中介层](https://www.semianalysis.com/p/advanced-packaging-part-2-review)之上。AID 有两个不同的流片版本，它们互为镜像，[与 Intel 的 Sapphire Rapids 如出一辙](https://www.semianalysis.com/p/intel-emerald-rapids-backtracks-on)。

## **计算小芯片——Banff XCD 与 DG300 Durango CCD**

位于 AID 之上的模块化计算裸片既可以是 CPU，也可以是 GPU。

在 GPU 一侧，计算小芯片称为 XCD，代号 Banff。Banff 采用 TSMC N5 工艺，尺寸约 ~115mm²。它总共包含 40 个计算单元（CU），但只启用了 38 个。该架构由 AMD 的 MI250X 演化而来，在 GitHub 上 AMD 称之为 gfx940，但公开名称是 CDNA3。它针对计算优化，虽然名为「GPU」，实际上并不能真正做图形处理。NVIDIA 的 H100 其实也一样，其大部分 GPC 并不具备图形能力。

![](https://substack-post-media.s3.amazonaws.com/public/images/8da7fe16-eadf-4b06-be4d-618f5c400eba_1216x705.png)

每个 AID 最多可搭配 2 颗 Banff 裸片，合计 76 个 CU。MI300 的最大 XCD/GPU 配置将提供 304 个 CU。相比之下，AMD 的 MI250X 为 220 个 CU。

MI300 模块化计算的另一面是 CPU 侧。AMD 部分复用了其 Zen 4 CCD 小芯片，但做了些修改。他们改动了少数几层金属层掩膜，以便为与 AID 的 SoIC 键合创建键合焊盘，这需要重新流片并重新设计部分金属掩膜。这颗修改版 Zen 4 CCD——GD300 Durango——禁用了 GMI3 PHY。它与 AID 之间的带宽显著高于 GMI3。该 CCD 采用 TSMC 5nm 工艺，裸片面积与桌面及服务器端 Zen 4 CCD 相同，约 ~70.4mm²。

每个 AID 最多可搭配 3 颗 Zen 4 小芯片，共 24 个核心。MI300 的最大 CCD/CPU 配置最高可提供 96 个核心。

## **先进封装——未来的一瞥**

AMD 的 [MI300 是当今世界上最不可思议的先进封装形态](https://www.semianalysis.com/p/advanced-packaging-part-1-pad-limited)。超过 100 片硅片被组合在一起，全部落在一块破纪录的 3.5 倍光罩面积的硅中介层上，采用 TSMC 的 CoWoS-S 技术。这些硅片从 HBM 存储层、有源中介层、计算裸片，到用于结构支撑的空白硅片，不一而足。这块巨型中介层的面积接近 NVIDIA H100 上那颗的两倍。MI300 的封装工艺流程极为复杂，我们今后必须专门另文深入，逐一讲解每一步的确切工艺流程和所用设备，因为它确实[是行业的未来](https://www.semianalysis.com/p/advanced-packaging-part-1-pad-limited)。

复杂的封装要求 AMD 付出极大的灵活性和多次修订，才能让 MI300 按时落地。原始设计是采用有机再布线层（RDL）中介层，使用 TSMC 的 [CoWoS-R 技术](https://www.semianalysis.com/p/packaging-developments-from-ectc)。事实上，TSMC 去年确实展示过一个 CoWoS-R 测试封装，其结构与 MI300 惊人地相似。或许中介层材料的变更，是出于对如此大尺寸有机中介层在翘曲和热稳定性方面的担忧。

AID 与 XCD、CCD 之间采用第一代 SoIC 混合键合，键合间距 9μm。AMD 原本计划转向[键合间距 6μm 的 TSMC 第二代 SoIC](https://www.semianalysis.com/p/packaging-developments-from-ectc)，但因技术尚不成熟而作罢。随后这些裸片被封装到 CoW 无源中介层之上。整个工艺过程中会用到十几片支撑硅片。最终成品 MI300 中既有传统的倒装芯片批量回焊（mass reflow）和 TCB（热压键合），也有晶圆上贴芯片（chip on wafer）、晶圆对晶圆（wafer on wafer）以及重构晶圆对晶圆的混合键合。

## **MI300 的配置**

AMD MI300 共有 4 种不同配置，尽管我们并不确定这 4 种是否都会真正发布。

MI300A 是以异构 CPU+GPU 计算抢占头条的那一款，也是 El Capitan 百亿亿次超算所采用的版本。MI300A 带集成散热顶盖（IHS）封装在 72 x 75.4mm 基板上，可插入 SH5 LGA 插槽的主板，每块主板 4 颗处理器。它实际上承担（抵偿）了开发成本。它已经在出货，但真正的放量要等到第三季度。标准服务器/节点将是 4 颗 MI300A。无需主机 CPU，因为它已经内置。这是目前市场上最好的 HPC 芯片，而且在未来一段时间内仍将如此。

![](https://substack-post-media.s3.amazonaws.com/public/images/5d57444c-19b8-499d-b4dd-31470460a9b5_1036x526.png)

MI300X 是面向 AI 超大规模云厂商的版本，若成功将成为真正的走量主力。它是全 GPU 配置，以实现 AI 最大性能。AMD 在此主推的服务器级配置是 8 颗 MI300X + 2 颗 Genoa CPU。它还配备密度更高的 SK Hynix 24GB HBM 堆叠。

MI300C 则走向相反方向，是仅含 CPU 的 96 核 Zen4 + HBM，对标 Intel 的 Sapphire Rapids HBM。不过，这个市场可能太小、产品太贵，AMD 未必会将这一版本产品化。

MI300P 像是缩小一半的 MI300X。它可以以更低功耗做成 PCIe 卡。它同样需要主机 CPU。这将是开发者最容易上手的一款，不过我们认为它更像是 2024 年发布的产品。

本报告将涵盖 IO 速率、网络、系统工程、FLOPS、性能、制造成本、设计成本、发布时点、量产爬坡、软件、客户合作与竞争态势。虽然各版本面向不同市场，我们将特别聚焦面向最大市场——AI——的版本。

[团体订阅享 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
