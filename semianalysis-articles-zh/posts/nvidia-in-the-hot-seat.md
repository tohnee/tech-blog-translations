---
title: "Nvidia 坐上烫手席位？"
title_en: "Nvidia In The Hot Seat?"
subtitle: "Intel Habana、Graphcore、Google TPU 与 Nvidia A100 的 AI 训练对比"
date: 2022-06-29
source: https://newsletter.semianalysis.com/p/nvidia-in-the-hot-seat
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
translated: 2026-09-15
---

# Nvidia 坐上烫手席位？

> 原文：[Nvidia In The Hot Seat?](https://newsletter.semianalysis.com/p/nvidia-in-the-hot-seat) · SemiAnalysis

**Intel Habana、Graphcore、Google TPU 与 Nvidia A100 的 AI 训练对比**

凭借灵活、易编程且强大的硬件，Nvidia 一直是 AI 训练工作负载的王者。但这种情况可能正在改变，因为 AI 本身非常动态，各种不同的 AI 工作负载正在分化。训练并不是一个铁板一块的整体，因此最适合你工作负载的硬件与软件方案，未必适合另一个工作负载。再加上模型演进的飞快节奏，一些 AI 训练硬件开始找到自己的利基。

今天我们将剖析几家向 MLPerf 2.0 提交性能结果的主要玩家，以及这些硬件可以在哪里找到利基。我们也会讨论机器学习模型正在发生的一些演进。

在深入各份提交结果之前，我们想先指出几点。这张来自 ML Commons 的图表展示了任何配置 8 颗处理器/加速器的系统的峰值性能，以及它们在几个主流模型上的表现，并与通俗定义的「摩尔定律」（即每两年翻倍）做了对比。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/e7d6b78f-20bc-4b0c-ab06-a70b1afce1b6_1023x581.png)

这些结果透露了一个非常重要的细节：虽然制程节点微缩和架构变化随时间推移确实重要，但 AI 中最关键的因素是软件。取决于模型，3.5 年间性能提升最高可达 8 倍。而在这段时间里，Nvidia、Graphcore、Google、Habana 这些公司都只经历了 1 次硬件迭代和 1 次制程节点微缩。

大部分收益要归功于软件而非硬件。在各家软件栈之上运行的、支撑扩展能力的算法类型才是最重要的因素。软件是最大的差异化变量，但随着不同任务的模型进一步分化，这给其他厂商留下了针对少数工作负载做优化的利基空间——至少许多加速器公司是这么暗示的。

MLPerf 是由非营利联盟 [MLCommons](https://mlcommons.org/en/) 开发的、包含 8 个模型的基准测试套件。这些基准可以由 1 颗处理器一直跑到数千颗。虽然对它有一些合理的批评，但它迄今为止是比较 AI 硬件与软件性能的最佳公开手段。我们先看一部分结果并逐一拆解。

# **Intel Habana Gaudi2**

Habana 很有意思，因为他们的第一代芯片表现并不出色。去年其产品终于通过 AWS 上线时，软件栈还不成熟。他们最近发布了第二代 Gaudi AI 训练芯片，把性能拉到与行业更接近的水平——至少他们自己是这么宣称的。Habana 在 8 个模型中的 2 个上提交了基准。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/f6010b5d-309b-4104-835d-9f37d7ec3890_1022x328.png)

在极小的 ResNet-50 模型上，Habana 以明显优势获胜；在小型 BERT 自然语言处理模型上则以非常微弱的优势胜出。我们希望看到 Habana 提交更大、更多样的模型，但这已是一次强有力的亮相。

从经济学角度看，Nvidia 的 A100 与 Intel 的 Habana Gaudi2 都是光罩极限的台积电 7nm 裸片，配 6 组 HBM 堆叠（Nvidia 为良率禁用了 1 组）。因此这个对比相当对等。Gaudi2 功耗 600W，Nvidia 为 400W，但 Gaudi2 不需要额外的 InfiniBand 网卡和 NVSwitch 来在单台服务器内部或多台服务器之间连接 GPU。这节省了大量功耗和硅成本。值得注意的是，Habana 在 ResNet-50 上以个位数百分比击败 Graphcore，在 BERT 上以两位数百分比胜出。表现非常亮眼。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/ad1ba96f-0d8e-4f9b-8424-896c61bca137_1024x518.png)

Habana 还为其上一代 Gaudi1 芯片提交了更多基准，扩展到了比以往更高的芯片数量。性能本身不算亮眼，但看到他们的芯片能轻松扩展到更多加速器是件好事，因为把以太网直接集成进 AI 芯片本来就是他们的全部承诺。

虽然 Habana 提交的模型种类不多，但他们确实想强调一个关于优化的非常有趣的点。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/e8c96f1c-6faa-4ac7-8d72-417edcb4eb7a_1023x393.png)

Habana 表示，他们在向 MLPerf 提交成绩时有意识地使用开箱即用的软件、只做最少优化。他们通过与运行开箱即用软件的 Nvidia GPU 对比来证明这一点。这些数字和设置只能在 Intel 官网上找到，而不在 MLPerf 提交内容里。这样做的目的是不与 Nvidia 及其伙伴那种高度优化的 MLPerf 提交做比较。这确实是一个有趣的视角。如果能在更多样的模型上证明这一点成立，我们会更信服。

# **Google TPU**

Google 的处境很有意思，他们的 AI 硬件架构已经迭代到第 4 代。可以说，Nvidia 在这项任务上才刚走到第 3 代架构：Volta GPU 是首个包含 AI 专用张量核心的架构，Ampere 是当前一代，下一代 Hopper 正在送样、今年晚些时候批量出货。

他们的芯片基本只在内部使用，而且一直就是本着这一目标设计的。作为 AI 领域最前沿的公司之一，Google 必须应对扩展到超大模型规模的挑战。因此他们的提交也围绕配置数千颗加速器的巨型系统展开。我们编辑了 MLPerf 的表格，让它更易一眼读懂。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/6586e761-5234-413a-8b5e-bff526bdfc15_1024x323.png)

有趣的是，Google 通常按 2:1 的 TPU 与 CPU 比例配置，尽管有些系统是 4:1。而 Nvidia 通常是 4:1 或 8:1。性能上互有胜负。迄今为止，TPU 在云服务商领域几乎没取得什么成功，但 Google 在自家数据中心里为内部推理和训练工作负载部署了数万颗 TPU。Google 能否通过 Google Cloud 让更广泛的市场用起 TPU，值得关注。

# **Graphcore Bow**

Graphcore 与 Intel 的 Habana 类似，在 closed 组别中只提交了 2 种模型的结果。但他们提交的系统规模跨度大得多，从 16 到 256 颗加速器不等。这些系统搭载新发布的 [Bow IPU——业界首款晶圆对晶圆混合键合的处理器](https://semianalysis.substack.com/p/graphcore-announces-worlds-first?s=w)。

Bow 芯片在架构上与上一代完全相同，区别只在于采用晶圆对晶圆键合来[在不增加功耗的情况下把频率提高约 40%](https://semianalysis.substack.com/p/graphcore-announces-worlds-first?s=w)。这带来的一个副产品是软件与上一代完全一致。自最初在 MLPerf 基准中[彻底失利](https://semianalysis.com/graphcore-looks-like-a-complete-failure-in-machine-learning-training-performance/)以来，软件的持续进步让 Graphcore 走了很长的路。现在的结果好了很多，而且在 Graphcore 展示的这两个模型上，他们确实跑出了比 Nvidia 更好的性能。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/785e8ad4-3b74-4942-af7c-af91f26d4af1_1024x580.png)

在软件方面，另一个非常有趣的细节是：百度（Baidu）用自己的 PaddlePaddle 框架跑通了 IPU，而不是使用 Graphcore 的专用框架。PaddlePaddle 是一个聚焦分布式训练的开源训练框架，在中国非常流行，因此这对 Graphcore 在中国的潜在销售可能是一大利好。

Graphcore 还花了一些时间向我们介绍机器学习模型的当前路径，以及它将如何撞上重大路障。他们认为需要新的模型架构方法，并论证这些方法在他们新颖的 IPU 架构上会运行得更好。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/52485f6c-3d06-4b78-8bf7-3b53ae0914ff_1023x574.png)

事情的另一面是，当前模型正快速朝着越来越大的 transformer 演进。只要你舍得堆足够的算力和数据，这些模型在精度和训练时间上都表现出色。通过实现条件化与动态路由（conditional and dynamic routing），它们可以在更多样的任务上匹敌或击败任何其他模型架构，这让它们极具泛化性。我们在[这篇讨论 Tenstorrent](https://semianalysis.substack.com/p/tenstorrent-blackhole-grendel-and?s=w) 硬件架构、软件、路线图以及 Google Pathways 模型的文章中探讨过这一想法。

# **Nvidia A100**

面对竞争，Nvidia 并没有坐着不动。所有 MLPerf 结果用的都是发布已有 2 年的 A100，但 H100 GPU 已经在送样，今年晚些时候出货。Nvidia 非常自豪的一点是：他们是唯一一家向 MLPerf 全部 8 项基准都提交成绩的厂商。此外，多家系统集成商和服务器厂商伙伴也提交了搭载他们 GPU 的系统。Nvidia 总共在 4/8 项测试中夺魁。按单芯片计，这颗 2 年前发布的 A100 GPU 在 6/8 项测试中最快。竞争对手在大多数测试中干脆没有参赛，这很可能意味着他们内部测过、但决定不提交最终成绩/代码。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/c1119b32-3b21-4777-a875-fa83fb9fb5ce_1023x580.png)

Nvidia 对 AI 训练的口径有所转变。他们过去宣称处处称王，现在则只在大多数方面称王。这本身并不是大事，因为真正的决定因素不是每美元矩阵乘法次数。

训练的重要指标是总拥有成本（TCO）。Nvidia 仍在多个维度上继续统治。

首先，他们的 GPU 更灵活。即便相对于其他厂商在小型图像识别网络上不是最强，他们拥有最灵活的硬件，能适应广泛的工作负载。机器学习领域演进飞快，大型训练集群需要灵活的硬件。现实世界的 AI 很少只是单一模型，而是多个模型相互衔接。而如果是单一巨型模型，那它就是 transformer——而 transformer 似乎恰恰长得越来越适合在 GPU 上高效运行。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/dd4cc879-02e1-40e2-b9f4-2a615fa9eb72_1024x282.png)

从语音识别、视觉到推荐模型，多种不同模型类型协同工作之际，选一个只最适合单一模型类型的加速器，是通往糟糕 TCO 的必经之路。在数据中心里，最重要的指标之一是利用率。Nvidia 是唯一一家硬件既能用于数据准备、又能用于训练和推理的公司。其他许多公司只聚焦训练和推理，或仅训练。

最后，拥有优秀的软件是拼图中的关键一块。成本大头在于开发模型和软件，而不是运行它们。

> AI 并非简单地只看每美元能做多少次简单计算、只盯单台 AI 服务器成本。部署 AI 需要非常有价值的数据科学家、ML 工程师和应用开发者，他们才是 AI 基础设施成本的大头。
>
> Shar Narasimhan，Nvidia

除了最大的那几家运营商，对几乎所有公司而言，软件栈都极其重要，因为它占了成本的大头。让开发者能够轻松调整模型、部署、测试和迭代，对降低开发成本至关重要。

软件灵活性、开发成本与更高利用率的组合，使 Nvidia 仍然稳坐 TCO 王座。要为本文标题违反「贝特里奇头条定律」（Betteridge's law of headlines，即以问句作标题时答案往往是「否」）道个歉——但它确实让你点进来读到了这里，不是吗！

[分享](https://newsletter.semianalysis.com/p/nvidia-in-the-hot-seat?utm_source=substack&utm_medium=email&utm_content=share&action=share)

如今正出现一批规模足够大的玩家，他们的利用率会很高、灵活性不再那么重要。这些玩家很多在开发自研芯片，或与「第二供应商」合作。问题是这些第二供应商能否捕获足够的市场以长期存活。在我们看来，未来的世界将是：Google、Amazon、Microsoft、Facebook、阿里巴巴、腾讯和百度等超大规模云厂商尝试开发自己的硬件，而 Nvidia 一边奋力保持领先，一边努力让云客户继续想要 Nvidia 的硬件。

英特尔和 AMD 这类成熟公司也许有机会，但要打破 Nvidia 的垄断需要好几代人次的努力。推理侧才是我们预期许多不同架构和初创公司能够成功的地方。我们认为 Graphcore 有潜力脱颖而出获得成功，但这条路会很难走——除了软件要继续变好，他们的下一代硬件也必须足够出色。

[发表评论](https://newsletter.semianalysis.com/p/nvidia-in-the-hot-seat/comments)
