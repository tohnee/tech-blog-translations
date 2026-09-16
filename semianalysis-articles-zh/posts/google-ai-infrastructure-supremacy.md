---
title: "Google AI 基础设施的霸主地位：系统比微架构更重要"
title_en: "Google AI Infrastructure Supremacy: Systems Matter More Than Microarchitecture"
subtitle: "从 DLRM 到 LLM，内部工作负载是赢家，但 Google 在外部工作负载上表现如何？"
date: 2023-04-12
source: https://newsletter.semianalysis.com/p/google-ai-infrastructure-supremacy
crawled: 2026-09-15
authors: ["Dylan Patel", "George Cozma", "Gerald Wong"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# Google AI 基础设施的霸主地位：系统比微架构更重要

> 原文：[Google AI Infrastructure Supremacy: Systems Matter More Than Microarchitecture](https://newsletter.semianalysis.com/p/google-ai-infrastructure-supremacy) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**从 DLRM 到 LLM，内部工作负载是赢家，但 Google 在外部工作负载上表现如何？**

AI 时代的黎明已至，而理解这一点至关重要：AI 驱动的软件，其成本结构与传统软件大相径庭。芯片微架构与系统架构在这些全新软件形态的开发与扩展中扮演着关键角色。与开发者成本占比更大的前几代软件相比，AI 软件所运行的硬件基础设施对资本开支（capex）和运营开支（opex）、进而对毛利率的影响显著更大。因此，投入大量精力优化你的 AI 基础设施以支撑 AI 软件的部署，就变得愈发关键。在基础设施上占优的公司，在部署和规模化 AI 应用的能力上也将占优。

Google [早在 2006 年就开始鼓吹建设 AI 专用基础设施](https://cloud.google.com/blog/products/ai-machine-learning/an-in-depth-look-at-googles-first-tensor-processing-unit-tpu)，但问题在 2013 年到了沸腾的临界点。他们意识到，若想以任何可观的规模部署 AI，数据中心数量就得翻倍。于是，他们开始为 TPU 芯片打地基，并于 2016 年投产。有趣的是，可以拿 Amazon 做对比——同一年，Amazon 也意识到需要自研芯片。[2013 年他们启动了 Nitro 项目](https://www.semianalysis.com/i/108660819/amazon-nitro)，专注于[开发优化通用 CPU 计算与存储的芯片](https://www.semianalysis.com/i/108660819/amazon-nitro)。两家截然不同的公司，分别为[不同时代计算与软件范式](https://www.semianalysis.com/i/108660819/the-next-era-of-computing)优化了各自的基础设施努力。

自 2016 年以来，Google 已打造了 6 款不同的 AI 专用芯片：TPU、TPUv2、TPUv3、TPUv4i、TPUv4 和 TPUv5。这些芯片主要由 Google 设计，Broadcom 以不同程度参与了中后端协作。所有芯片均由台积电（TSMC）制造。自 TPUv2 起，芯片还采用了三星（Samsung）和 SK Hynix 的 HBM 内存。虽然 Google 的芯片架构很有意思——我们会在本报告后面深入探讨——但还有一个远为重要的话题。

Google 拥有近乎无与伦比的能力，能够低成本、高性能、可靠地大规模部署 AI。话虽如此，我们还是要给这个论点注入一些理性，因为 Google 在芯片级性能上也发表过不够诚实的说法，需要加以纠正。我们认为，凭借从微架构到系统架构的整体化思路，Google 在 AI 工作负载上相对微软（Microsoft）和 Amazon 拥有性能/总拥有成本（perf/TCO）优势。至于[将生成式 AI 商业化卖给企业和消费者的能力，那是另一回事](https://www.semianalysis.com/p/peeling-the-onions-layers-large-language)。

技术领域是一场永不停歇的军备竞赛，而 AI 是其中变化最快的战场。被训练和部署的模型架构随时间发生了巨大变迁。Google 的内部数据就是明证：2016 到 2019 年 CNN 模型迅速崛起，随后又回落。CNN 在计算、内存访问、网络等方面的特征画像，与 DLRM、Transformer、RNN 各不相同。RNN 也经历了同样的命运，被 Transformer 彻底取代。

![](https://substack-post-media.s3.amazonaws.com/public/images/36218128-bae1-4b25-a731-26d94053f912_2218x806.png)

因此，硬件必须对行业的发展保持灵活并予以支持。底层硬件不能过度特化于任何特定模型架构，否则会随模型架构的变迁面临被淘汰的风险。芯片从开发到大规模量产后部署通常需要 4 年，因此硬件可能跟不上软件想在它上面做的事。这一点从某些初创公司的 AI 加速器架构上已经可见——它们把特定模型类型当作优化基准点。这是多数 AI 硬件初创公司已经或将要以失败告终的众多原因之一。

这一点在 Google 自己的 TPUv4i 芯片上尤为明显：它专为推理设计，[却无法在 PaLM 等 Google 最好的模型上运行推理](https://www.semianalysis.com/i/108660819/google)。上一代的 Google TPUv4 和 Nvidia A100 在设计时不可能预见到大语言模型。同样，最近部署的 Google TPUv5 和 Nvidia H100 也不可能为[AI 砖墙](https://www.semianalysis.com/p/the-ai-brick-wall-a-practical-limit)而设计，更不可能为应对砖墙而发展出的新模型架构策略而设计。而这些策略正是 GPT-4 模型架构的核心组成部分。

[![](https://substackcdn.com/image/fetch/$s_!HwSb!,w_56,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fbucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com%2Fpublic%2Fimages%2F0150776c-9bf2-4bea-a9c2-41b24b7a0f15_1280x1280.png)SemiAnalysisThe AI Brick Wall – A Practical Limit For Scaling Dense Transformer Models, and How GPT 4 Will Break Past ItLarge generative AI models unlock massive value for the world, but the picture isn't only roses. Costs for training for these civilization-redefining models have been ballooning at an incredible pace. Modern AI has been built on scaling parameter counts, tokens, and general complexity an order of magnitude every single year. This report will discuss the brick wall for scaling dense transformer models, the techniques and strategies being developed to break through that wall, and which specific ones will be used in GPT 4…Read more4 years ago · 44 likes · 9 comments · Dylan Patel](https://www.semianalysis.com/p/the-ai-brick-wall-a-practical-limit?utm_source=substack&utm_campaign=post_embed&utm_medium=web)

硬件架构师只能对自己所设计芯片的未来机器学习走向做出最佳猜测。这包括内存访问模式、张量尺寸、数据复用结构、算术密度与网络开销的权衡等等。

此外，芯片微架构只占 AI 基础设施真实成本的一小部分。系统级架构和部署灵活性是重要得多的因素。今天，我们想深入探讨 Google 的 TPU 微架构、系统架构、部署切片（slicing）、可扩展性，以及它相对其他科技巨头在基础设施上的巨大优势。其中包括我们用一个 TCO 模型比较 Google AI 基础设施与微软、Amazon 和 Meta 的成本。

我们还将直接把 Google 的架构与 Nvidia 的做对比——这是当下最受关注的话题，尤其从性能和网络的角度。我们也会简要对比其他公司的 AI 硬件，包括 AMD、Intel、Graphcore、Amazon、Sambanova、Cerebras、Enflame、Groq、Biren（壁仞）、Iluvatar（燧原）和 Preferred Networks。

我们还将从大型模型研究、训练和部署从业者的视角来审视这一切。我们还想深入探讨 DLRM 模型——尽管它当前是规模最大的量产 AI 模型架构，却常常少有人讨论。此外，我们将讨论 DLRM 与 LLM 两类模型在基础设施上的差异。最后，我们将讨论 Google 用 TPU 服务外部云客户能否成功。文末还有一个彩蛋：Google TPU 上的一处异常，我们认为是个错误。

## **Google 的系统级基础设施优势**

Google 基础设施优势的一部分在于，他们始终从系统级视角来设计 TPU。也就是说，单颗芯片固然重要，但它在真实世界的系统中如何协同使用远为重要。因此，我们的分析将从系统架构到部署应用再到芯片层面，逐层展开。

虽然 [Nvidia 也从系统视角思考](https://www.semianalysis.com/p/meta-discusses-ai-hardware-and-co)，但他们的[系统规模一直比 Google 的更小、更窄](https://www.semianalysis.com/i/108660819/google)。而且，直到不久前，Nvidia 还没有云端部署的经验。Google AI 基础设施最大的创新之一，是在 TPU 之间使用自研网络栈——ICI。相对于昂贵的以太网和 InfiniBand 部署，这条链路低延迟、高性能。它更接近 Nvidia 的 NVLink。

Google 的 TPUv2 可扩展到 256 颗 TPU 芯片，与 Nvidia 当代 H100 GPU 的数量相同。TPUv3 将这一数字提升到 1024，TPUv4 提升到 4096。按趋势线推断，我们估计当代的 TPUv5 无需经过低效的以太网即可扩展到 16,384 颗芯片。虽然这对大规模模型训练的性能视角很重要，但更重要的是他们把这一切切分出来投入实际使用的能力。

![](https://substack-post-media.s3.amazonaws.com/public/images/fb6b25dd-ed90-428c-a6a3-2d4a40997217_1088x828.png)

Google 的 TPUv4 系统每台服务器配 8 颗 TPUv4 芯片和 2 颗 CPU。这一配置与 Nvidia 的 GPU 相同——每台服务器 8 颗 A100 或 H100 加 2 颗 CPU。GPU 部署通常以单台服务器为计算单元，但对 TPU 而言，部署单元是一个更大的「切片」：64 颗 TPU 芯片加 16 颗 CPU。这 64 颗芯片通过 ICI 网络以 4^3 立方体结构、经由直连铜缆内部互联。

![](https://substack-post-media.s3.amazonaws.com/public/images/9058da21-69e9-4528-8401-2077abc5d73c_2084x560.png)

超出这个 64 芯片单元之后，通信就转入光域。[这些光收发器的价格是无源铜缆的 10 倍以上](https://www.semianalysis.com/p/marvells-dsp-dilemma-networkings)，所以 Google 把切片尺寸优化为 64 这个数，以从网络角度最小化系统级成本。

对比一下 2023 年的 Nvidia SuperPod 部署：NVLink 最多连接 256 颗 GPU，比 2020 年 4096 颗芯片的 TPUv4 pod 小 16 倍。而且，从 Nvidia 第一方渲染图和 DGX Superpod 系统来看，Nvidia 对密度和网络成本的关注明显少得多。Nvidia 的部署通常每机柜 4 台服务器。

[超出 4 台服务器、32 颗 GPU 的范围后，通信通常就必须走光](https://www.semianalysis.com/p/thick-cables-thin-margins-microsoft)。因此，大规模部署时 Nvidia 需要多得多的光收发器。

## **Google OCS**

Google 部署了自研光交换机（OCS），使用基于 MEMS 的微镜阵列在 64 TPU 切片之间切换。简单概括：Google 声称其自研网络能提升 30% 吞吐、省 40% 功耗、少 30% 资本开支、缩短 10% 流完成时间，且全网停机时间减少 50 倍。更详细的原理请看这篇报告。

[![](https://substackcdn.com/image/fetch/$s_!HwSb!,w_56,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fbucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com%2Fpublic%2Fimages%2F0150776c-9bf2-4bea-a9c2-41b24b7a0f15_1280x1280.png)SemiAnalysisGoogle Apollo: The >$3 Billion Game-Changer in Datacenter NetworkingNetworking is a critical part of any datacenter, especially with the rise of networking-intensive large language models. As such, it was a clear target for Google's infrastructure optimization efforts. Over the last year at conferences such as OFC and SIGCOMM, Google disclosed their custom networking stack, Jupiter, from in-house switches all the way through to custom reconfigurable software…Read more3 years ago · 28 likes · 7 comments · George Cozma and Dylan Patel](https://www.semianalysis.com/p/google-apollo-the-3-billion-game?utm_source=substack&utm_campaign=post_embed&utm_medium=web)

Google 用这些 OCS 构建其数据中心脊层（spine），也用它们在 TPU pod 之间和内部做互联。这种 OCS 的一大优势是：在 4096 颗 TPU 的 Pod 内，从任一 64 TPU 切片到任一其他 TPU 切片，信号始终保持在光域。

对比一个由多个 Nvidia SuperPod 组成的 4096 颗 GPU 的 Nvidia 部署：这样的系统需要多层交换，总计约 568 台 InfiniBand 交换机。Google 的 4096 TPU 部署只需要 48 台自研光交换机。

应当指出，若直接从 Google 的代工制造商处采购，Google 的 OCS [按单台交换机计要贵约 3.2 到 3.5 倍](https://www.semianalysis.com/i/109073285/ocs-obstacles-addressing-high-upfront-costs-insertion-loss-and-more)，对比对象是第三方从 Nvidia 采购的 InfiniBand 交换机。不过这不是公平比较，因为后者包含了 Nvidia 约 75% 的数据中心毛利率。

如果只比较代工制造成本，即 Google 的成本对 Nvidia 的成本，那么价差拉大到 Nvidia InfiniBand 交换机的 12.8 到 14 倍。部署 4096 颗芯片所需交换机数量是 48 对 568，即 11.8 倍。单论交换机制造，Nvidia 方案更便宜。但[把额外的光收发器成本算进来](https://www.semianalysis.com/p/marvells-dsp-dilemma-networkings)，这个等式就拉平甚至转向有利于 Google。

交换层与层之间的每个连接都是需要更多线缆的又一个节点。虽然部分可以走直连铜缆，但仍有多个节点信号必须走光。每层交换之间都要完成电—光—电的转换。这会使大型电交换系统的功耗远高于 Google 的 OCS。

Google 声称，所有这些功耗和成本节省如此之大，以至于其网络成本只占 TPU v4 超级计算机总资本成本的 <5%、总功耗的 <3%。这可不只是把电交换换成自研光交换机就能做到的。

## **用拓扑最小化网络成本**

尽管 Google 大力推销这一观点，但必须认识到，Google 与 Nvidia 网络的拓扑完全不同。Nvidia 系统部署的是「非阻塞」的 Clos 网络。这意味着它们可以在所有输入输出对之间同时建立全带宽连接，没有任何冲突或阻塞。这种设计为数据中心中连接大量设备提供了可扩展的方案，最小化延迟并增强冗余。

![](https://substack-post-media.s3.amazonaws.com/public/images/13eaaaff-5df8-4903-b0cf-eca48325cd22_1435x457.png)

Google 的 TPU 网络放弃了这一路线。他们使用 3D 环面（torus）拓扑，把节点连成三维网格结构。每个节点与网格中的六个相邻节点相连（上、下、左、右、前、后），在三个维度（X、Y、Z）上各形成一个闭环。这形成了一个高度互联的结构，节点在所有三个维度上构成连续环路。

![](https://substack-post-media.s3.amazonaws.com/public/images/54b9e0f0-5a70-448e-b27f-3ac3c54f3b4b_1388x1400.png)

第一张图偏逻辑示意，但只要你琢磨一会儿、肚子又有点饿，就会发现这个网络拓扑活脱脱是一只甜甜圈！

![](https://substack-post-media.s3.amazonaws.com/public/images/8255e86c-932b-465e-bc9a-ee4ee5d95b13_2306x1516.png)

环面拓扑相对 Nvidia 采用的 Clos 拓扑有几项优势：

1. 更低延迟：3D 环面拓扑凭借相邻节点之间短促、直接的链路可提供更低延迟。这对运行需要节点间频繁通信的紧耦合并行应用（如某些类型的 AI 模型）尤其有用。
2. 更好的局部性：在 3D 环面网络中，物理上相近的节点在逻辑上也相近，可带来更好的数据局部性并降低通信开销。延迟只是一个方面，功耗也是一大红利。
3. 更低网络直径：在节点数相同时，3D 环面拓扑的网络直径低于 Clos 网络。由于相对 Clos 网络所需的交换机少得多，可节省大量成本。

硬币的另一面是，3D 环面网络也有许多劣势：

1. 可预测的性能：Clos 网络，尤其在数据中心环境中，凭借非阻塞特性可提供可预测、一致的性能。它们保证所有输入输出对都能同时以全带宽连接而无冲突或阻塞，3D 环面网络则无法保证。
2. 更易扩展：在脊叶（spine-leaf）架构中，向网络添加新的叶交换机（例如为了容纳更多服务器）相对简单，不需要对现有基础设施做大改动。相比之下，扩展 3D 环面网络可能需要重配整个拓扑，更复杂也更耗时。
3. 负载均衡：Clos 网络在任意两节点之间提供更多路径，可实现更好的负载均衡和冗余。虽然 3D 环面网络也提供多条路径，但取决于网络配置，Clos 网络的备选路径数量可以更多。

总体而言，虽然 Clos 有其优势，但 Google 的 OCS 化解了其中许多。OCS 让多个切片之间、多个 pod 之间的扩展变得简单。

![](https://substack-post-media.s3.amazonaws.com/public/images/9a77ae9a-0234-43b7-91f0-bb7e8f5aae26_842x628.png)

3D 环面拓扑面临的最大问题是，故障可能成为更大的麻烦。故障会冒头，也确实会冒头。即使主机可用性达到 99%，一个 2048 颗 TPU 的切片几乎为 0 的概率能正常工作。即使达到 99.9%，没有 Google 的 OCS，一次 2000 颗 TPU 的训练也只有 50% 的有效吞吐（goodput）。

OCS 的美妙之处在于，它让路由可以实时重配。

![](https://substack-post-media.s3.amazonaws.com/public/images/30447f25-b18c-4a39-9251-26e61d2216ba_1408x860.png)

要允许在有节点故障的情况下继续调度任务，就需要备件。不然的话，运营商无法现实地从 4096 节点的 pod 里切出两个 2048 节点的切片而不冒故障风险。基于 Nvidia 的训练经常需要投入过多开销专用于保存检查点、摘除故障节点并重启。Google 则在一定程度上把这件事简化成了直接绕开故障节点路由。

OCS 的另一个好处是，切片一部署好就能投入使用，而不必等整个网络就绪。

## **部署基础设施——用户视角**

从成本和功耗角度看，这些基础设施效率很美好，让 Google 每一美元能部署的 TPU 多于其他公司能部署的 GPU，但这对使用而言毫无意义。Google 内部用户享受到的最大优势之一，是他们可以按自己的模型定制基础设施需求。

没有任何芯片或系统能同时匹配所有用户想要的内存、网络和各类计算特征画像。芯片必须做泛化，但与此同时，用户想要那种灵活性，他们不要一刀切的方案。Nvidia 的对策是提供大量不同的 SKU 变体。此外，他们还提供不同的内存容量档位，以及 Grace + Hopper、面向 SuperPod 的 NVLink Network 等更紧密的集成选项。

Google 负担不起这种奢侈。每多一个 SKU，就意味着单个 SKU 的总部署量更低。这反过来会降低其整体基础设施的稼动率。SKU 更多还意味着用户更难在想用的时候拿到想要的那类算力，因为某些选项难免被超订。那些用户将被迫使用次优配置。

于是，Google 面临一个棘手难题：既要给研究员们喂上他们确切想要的产品，又要把 SKU 变体压到最少。Google 恰好只有一种 TPUv4 部署配置——4096 颗 TPU；相比之下，Nvidia 为更大、更多样的客户群必须支持数百种不同规模的部署和 SKU。即便如此，Google 仍能以独特的方式切分组合，让内部用户拥有他们渴望的基础设施灵活性。

Google 的 OCS 还支持创建自定义网络拓扑，比如扭曲环面（twisted torus）网络。这类 3D 环面网络的某些维度被扭曲，即网络边缘的节点以非平凡、非线性的方式相连，在节点之间创造额外的捷径。这进一步改善了网络直径、负载均衡和性能。

![](https://substack-post-media.s3.amazonaws.com/public/images/8d377fcd-3a0e-4724-9c13-bbab3aee4b82_1064x570.png)

Google 的团队大量利用这一点来辅助特定模型架构。下面是 2022 年 11 月仅一天内按芯片数和网络拓扑统计的各种 TPU 配置热度快照。配置超过 30 种——尽管许多配置系统中的芯片数相同——以适配正在开发的各类模型架构。这是 Google 就其 TPU 使用情况和灵活性给出的极具洞察力的披露。而且，还有许多未在图中展示的更少用的拓扑。

![](https://substack-post-media.s3.amazonaws.com/public/images/3fc750a2-bad8-4b64-aaeb-32800d035d7a_2552x1282.png)

为了充分利用可用带宽，用户把数据并行映射在 3D 环面的一个维度上，把两个模型并行参数放到另外两个维度。Google 声称，选择最优拓扑可带来 1.2 到 2.3 倍的性能提升。

[分享](https://newsletter.semianalysis.com/p/google-ai-infrastructure-supremacy?utm_source=substack&utm_medium=email&utm_content=share&action=share)

软件栈和外部用户的话题，我们将在本报告后文讨论。

## **规模最大的量产 AI 模型架构：DLRM**

不谈深度学习推荐模型（DLRM），任何关于 AI 基础设施的讨论都不完整。这些 DLRM 是百度（Baidu）、Meta、字节跳动（ByteDance）、Netflix 和 Google 这类公司的支柱。它是广告、搜索排序、社交媒体信息流排序等每年超过一万亿美元营收的引擎。这些模型包含数十亿权重，在超过一万亿条样本上训练，并[以每秒超过 30 万次查询的负载处理推理](https://www.semianalysis.com/p/the-inference-cost-of-search-disruption)。这些模型的规模（10TB+）甚至远超最大的 Transformer 模型，如 GPT-4——后者量级为 1TB+（模型架构不同）。

上述所有公司的共同点是：它们依赖持续更新的 DLRM 来驱动其个性化内容、产品或服务的业务，横跨电商、搜索、社交媒体和流媒体服务等行业。这些模型的成本极其庞大，硬件必须与之协同优化。DLRM 并非一成不变，而是在不断改进，但让我们先解释一下通用模型架构。我们尽量讲得简单些。

DLRM 的目标是通过建模类别特征与数值特征，学习用户—物品交互的有意义表示。其架构由两大组件构成：嵌入组件（Embedding Component，处理类别特征）和多层感知机（MLP）组件（处理数值特征）。

![](https://substack-post-media.s3.amazonaws.com/public/images/7711875e-af0d-4d0b-a16e-c73522aae8f7_1074x945.png)

用最简化的说法：[多层感知机组件是稠密的](https://www.semianalysis.com/p/the-ai-brick-wall-a-practical-limit)。特征被送入一系列全连接层。这类似于[GPT-4 之前的早期 Transformer 架构，同样是稠密的](https://www.semianalysis.com/p/the-ai-brick-wall-a-practical-limit)。[稠密层与硬件上的大型矩阵乘单元映射得非常好](https://www.semianalysis.com/p/nvidiaopenaitritonpytorch)。

嵌入组件是 DLRM 独有的，也是使其计算画像如此独特的关键。DLRM 的输入是以离散、稀疏向量表示的类别特征。一次简单的 Google 搜索只包含整个语言中的少数几个词。这些稀疏输入无法与硬件上的大型矩阵乘单元很好映射，因为它们本质上更接近哈希表，而非张量。由于神经网络通常在稠密向量上表现更好，需要用嵌入（embedding）把类别特征转换为稠密向量。

- 稀疏输入：[0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
- 稠密向量：[0.3261477, 0.4263801, 0.5121493]

嵌入函数把类别空间（英语词汇、对一条社交媒体帖子的互动、对某类帖子的行为）映射到一个更小的稠密空间（每个词用 100 维向量表示）。这些函数用查找表实现，查找表是 DLRM 的关键组成部分，往往构成 DLRM 模型的第一层。嵌入表的规模差异巨大，从几十 MB 到几百 GB 乃至数 TB 不等。

[Meta 两年前的 DLRM 就已超过 12 万亿参数](https://arxiv.org/pdf/2104.05158.pdf)，需要 128 颗 GPU 做推理。如今，最大的生产级 DLRM 模型至少又大了数倍，仅模型嵌入就消耗超过 30TB 内存。预期明年嵌入规模将增长到 70TB 以上！因此，这些表必须切分到许多颗芯片的内存上。切分方法主要有三种：列切分（column sharding）、行切分（row sharding）和表切分（table sharding）。

DLRM 的性能主要受制于内存带宽、内存容量、向量处理性能以及芯片之间的网络/互连。嵌入查找操作主要由小规模的 gather/scatter 内存访问构成，算术强度很低（FLOPS 完全不重要）。对嵌入表的访问本质上是非结构化稀疏。每次查询都必须从分片在成百上千颗芯片上的 30TB+ 嵌入中拉取数据。这可能导致 DLRM 推理超级计算机上计算、内存和通信负载的不均衡。

这与 MLP 和类 GPT-3 Transformer 中的稠密操作大不相同。[芯片的 FLOPS/sec 仍是主要性能驱动力之一](https://www.semianalysis.com/i/97006309/machine-learning-training-components)。当然，[FLOPS 之外](https://www.semianalysis.com/i/97006309/the-memory-wall)还有多种因素拖累性能，但在 Chinchilla 式 LLM 上，GPU [仍能实现超过 71% 的硬件 FLOPS 利用率](https://github.com/mosaicml/examples/tree/release/v0.0.4/examples/llm/throughput)。

## **Google 的 TPU 架构**

Google 的 TPU 在架构上引入了一些使其有别于其他处理器的关键创新。与传统处理器不同，TPU v4 没有专用指令缓存，而是采用直接内存访问（DMA）机制，类似 Cell 处理器。TPU v4 的向量缓存不属于标准缓存层级，而是用作便签存储（scratchpad）。便签存储与标准缓存的不同在于它需要手动写管理，而标准缓存自动处理数据。Google 之所以能用上这种更高效的基础设施，是因为不需要服务庞大的通用计算市场。这确实对编程模型有一定影响，不过 Google 工程师认为 XLA 编译器栈处理得很好。对外部用户可就不能这么说了。

TPU v4 拥有 160MB SRAM 便签存储，以及 2 个 TensorCore，每个 TensorCore 含 1 个向量单元、4 个矩阵乘单元（MXU）和 16MB 向量内存（VMEM）。两个 TensorCore 共享 128MB 内存。它们支持 275 TFLOPS 的 BF16，也支持 INT8 数据类型。TPU v4 的内存带宽为 1200GB/s。片间互连（ICI）通过 6 条 50GB/s 链路提供 300GB/s 的数据传输速率。

TPU v4 内含一个 322 位超长指令字（VLIW）标量计算单元。在 VLIW 架构中，指令被组成单条超长指令字，再分发给处理器执行。这些成组指令（也称 bundle）由编译器在程序编译期间显式定义。VLIW bundle 最多包含 2 条标量指令、2 条向量 ALU 指令、1 条向量加载和 1 条向量存储指令，以及 2 个向 MXU 收发数据的槽位。

向量处理单元（VPU）配备 32 个 2D 寄存器，每个含 128x8 个 32 位元素，构成一个 2D 向量 ALU。矩阵乘单元（MXU）在 v2、v3、v4 上为 128x128，v1 版本为 256x256 配置。改动的原因是：Google 模拟发现四个 128x128 MXU 的利用率比一个 256x256 MXU 高 60%，而四者面积与一个 256x256 MXU 相同。MXU 输入采用 16 位浮点（FP），以 32 位浮点（FP）累加。

这些更大的单元能实现更高效的数据复用，从而突破内存墙。

## **Google 的 DLRM 优化**

Google 是最早在搜索产品上规模化使用 DLRM 的公司之一。这一独特需求催生了非常独特的解法。上述架构有一个重大缺陷：无法有效处理 DLRM 的嵌入。Google 的主力 TensorCore 非常大，与这些嵌入的计算画像不匹配。Google 不得不在 TPU 中开发出一类全新的「SparseCore」，有别于上文描述的、面向稠密层的「TensorCore」。

![](https://substack-post-media.s3.amazonaws.com/public/images/87af5db8-25e0-4e27-b358-795b69d02a88_1168x614.png)

SparseCore（SC）为 Google TPU 中的嵌入提供硬件支持。早在 TPU v2 起，这些领域专用处理器就拥有与每条 HBM 通道/子通道直接绑定的瓦片。它们加速了深度学习推荐模型（DLRM）训练中内存带宽最密集的部分，却只占约 5% 的裸片面积和功耗。通过用每颗 TPU v4 芯片上的高速 HBM2 承载嵌入（而非 CPU），Google 的内部生产级 DLRM 相比把嵌入留在主机 CPU 主存上获得了 7 倍加速（TPU v4 SparseCore 对 TPU v4 嵌置于 Skylake-SP）。

![](https://substack-post-media.s3.amazonaws.com/public/images/87d8a645-9916-4f6b-8cdf-76de4f05fbcc_1558x512.png)

SparseCore 实现从 HBM 的快速内存访问，配专用取数、处理和清写（flush）单元，把数据搬入稀疏向量内存（Spmem）组，并由一个可编程的 8 通道 SIMD 向量处理单元（scVPU）负责更新。16 个此类计算瓦片组成一个 SparseCore。

额外的跨通道单元执行特定嵌入操作（DMA、排序、稀疏归约、分叉、拼接）。每颗 TPU v4 芯片有 4 个 SparseCore，每个带 2.5MB Spmem。展望未来，我们推测 TPUv5 的 SparseCore 数量会随 HBM3 子通道数增加而继续增至 6 个，瓦片数增至 32。

迁移到 HBM 的性能收益是巨大的，但性能扩展仍受互连对分（bisection）带宽制约。TPU v4 的 ICI 新 3D 环面有助于进一步扩展嵌入查找性能。然而扩展到 1024 颗芯片以上时改善逐渐消失，因为 SparseCore 的开销成为瓶颈。

![](https://substack-post-media.s3.amazonaws.com/public/images/4dfb4fca-dcb4-490e-85e2-792413d67da6_1250x782.png)

如果 Google 认为其 DLRM 需要在约 512 颗芯片以上的规模继续扩大容量，这一瓶颈很可能导致 TPUv5 的每瓦片 Spmem 也随之增加。

[分享](https://newsletter.semianalysis.com/p/google-ai-infrastructure-supremacy?utm_source=substack&utm_medium=email&utm_content=share&action=share)

本报告的其余部分将用大语言模型训练的真实数据把 Google TPU 与 Nvidia GPU 做对比，而不是你常常见到的那种与训练预算毫不相关的小模型对比。

我们还将把微架构与 Nvidia GPU 以及其他公司的 AI 硬件做对比，包括 AMD、Intel、Graphcore、Amazon、Sambanova、Cerebras、Enflame、Groq、Biren（壁仞）、Iluvatar（燧原）和 Preferred Networks。

我们也会比较其他科技巨头与 Google 的 AI 基础设施成本。最后，还有 Google TPU 上一处我们只能认定为错误的诡异异常。

[团体订阅享 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
