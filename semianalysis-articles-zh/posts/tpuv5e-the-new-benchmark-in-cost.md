---
title: "TPUv5e：<200B 参数模型成本高效推理与训练的新基准"
title_en: "TPUv5e: The New Benchmark in Cost-Efficient Inference and Training for <200B Parameter Models"
subtitle: "延迟、性能、微调、扩展性与网络"
date: 2023-09-01
source: https://newsletter.semianalysis.com/p/tpuv5e-the-new-benchmark-in-cost
crawled: 2026-09-15
authors: ["Dylan Patel", "Aleksandar Kostovic"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# TPUv5e：<200B 参数模型成本高效推理与训练的新基准

> 原文：[TPUv5e: The New Benchmark in Cost-Efficient Inference and Training for <200B Parameter Models](https://newsletter.semianalysis.com/p/tpuv5e-the-new-benchmark-in-cost) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**延迟、性能、微调、扩展性与网络**

在 Cloud Next 2023 大会上，谷歌（Google）宣布其最新 AI 芯片 TPUv5e（TPUv5 lite）正式全面上市。这款芯片堪称游戏规则改变者，原因在于它为谷歌自身以及新的 Cloud TPU 客户所带来的性能/TCO。对于许多外部机构而言，用它来训练和推理 2,000 亿（200B）参数以下的模型，直接就是一笔巨大的成本优势。

TPUv5e 还让谷歌能够以 OpenAI 运行其较小模型的相同成本，去推理比 OpenAI 更大的模型。这将极大地帮助谷歌拉平竞争环境，因为他们玩得起一场别人玩不起的暴力堆算力游戏。[由于相较谷歌存在巨大的算力缺口](https://www.semianalysis.com/p/google-gemini-eats-the-world-gemini)，OpenAI 将不得不在芯片与算法的运用上聪明得多。亚马逊（Amazon）（Trainium/Inferentia）、Meta（MTIA）与微软（Microsoft）（Athena）的 AI 芯片与谷歌当前的水平都相去甚远。

今天，我们想通过 GPT-3 训练成本与 LLAMA-65B 推理成本的数据，展示这颗改变游戏规则的芯片的性能/TCO 优势，对其做详细解析。此外，我们还想讨论谷歌的牌价（list price）以及折扣后的云定价，及其与各类 GPU 定价的对比。

有趣的是，即便有着优惠的协议，对 OpenAI 而言，用搭载 TPUv5e 的 Google Cloud 来推理某些模型，经济上仍比通过 Microsoft Azure 使用 A100 和 H100 更划算。当然，一大堆政治/商业原因决定了这几乎永远不可能发生。

在深入之前，我们先安抚一下 [Sam Altman 的担忧](https://twitter.com/sama/status/1696340377098453440)。这绝不是谷歌的营销，我们与谷歌市场或 HR 部门没有任何联系。除了订阅我们的 newsletter 之外，他们没有付给我们任何钱。本文是基于谷歌官方事实数据以及一家使用 TPUv5e 的第三方 AI 初创公司数据的分析。他所提到的那些「先验」，指的是供应链渠道里全尺寸 TPUv5 的出货信息。

![](https://substack-post-media.s3.amazonaws.com/public/images/a5fd870b-0f16-4d01-8de4-bf9bdb4a5387_1800x1358.png)

回应 Elon：他们没说错。

开完玩笑，我们来讨论芯片与系统本身，然后再谈真实性能。TPUv5e（TPUv5 lite）是 TPUv4i（TPUv4 lite）的继任者，不要与 TPUv4（Pufferfish）和 TPUv5（Viperfish）主线产品混淆。TPUv4 lite 因是推理芯片，对外被冠以 i 后缀；TPUv5 lite 现在则因效率（efficiency）而带上 e 后缀。过去我们的注意力大多放在全尺寸芯片上，尽管 lite 芯片在谷歌内部推理负载中被大量使用。从 TPUv4i 到 TPUv5e，这一点发生了变化，因为这颗小芯片确实适合对外使用。

TPUv5 与其较小的兄弟 TPUv5e，显然都不是那种为追求峰值性能不惜一切代价的设计。它们的功耗、内存带宽与 FLOPS 都显著低于英伟达 H100。这是谷歌的主动决策，而不只是芯片设计能力更差的标志。由于通过博通（Broadcom）自行设计并采购芯片，谷歌为此支付的利润率显著更低。因此，在 4 年以上的使用周期里，功耗、网络成本、系统成本与部署灵活性才是决定芯片总拥有成本（TCO）的更大因素。

在英伟达的模式下，由于其硬件毛利率极高，客户 TCO 等式中资本开支（capex）占主导地位，运营开支（opex）相对小得多。因此，把 H100 推到 TPUv5 的 2 倍、TPUv5e 的约 5 倍功耗，以榨取高得多的性能，是更合乎逻辑的做法。此外，英伟达架构与 SKU 阵列的差异使其更适合做超大芯片。谷歌没有做 SKU 切分，也没有超大规模的张量单元，这意味着它们无法通过良率收割（yield harvest）达到英伟达 AI 芯片 >90% 参数良率的水平。出于这些原因，谷歌选择了低功耗小芯片，不仅是在 TPUv5e 上，TPUv5 亦然。TPUv5e 面积为 ~325mm^2。

谷歌的 TPU 内部包含一颗或两颗 Tensor Core，TPUv4 与 TPUv4i（lite）都是如此。TPUv5e（lite）相比未发布的 TPUv5（Viperfish）同样退了一步：TPUv5e 只有一颗 Tensor Core，而 TPUv5 有两颗；此外，其 HBM 堆叠数减半且速度更低；最后，网络能力被大幅削减。每颗 Tensor Core 拥有 4 个矩阵乘法单元（MXU）、一个向量单元和一个标量单元。MXU 基于 128 x 128 乘法/累加器的脉动阵列，提供 Tensor Core 的大部分算力。每个 MXU 每周期可执行 16,000 次乘加运算。TPUv5e 拥有 197 BF16 TFLOPS 与 393 Int8 TOPS。

![](https://substack-post-media.s3.amazonaws.com/public/images/9c31617f-364f-433a-884a-a397a127b1b2_406x246.png)

Tensor Core 与 16GB HBM2E 内存通信，运行速率 3200MT/s，总内存带宽 819.2GB/s。一个 pod 中最多有 256 颗 TPUv5e 芯片，由 4 个双面机柜单元构成，每面 8 个 TPUv5e sled。每个系统内含 4 颗 TPU 芯片，外加一颗 CPU 和一个 100G NIC。每 4 颗 TPU 共享 112 个 vCPU。这些实际上是 64 核的 AMD 芯片，可见谷歌仍需为 hypervisor 预留 CPU 核心，无法将其跑在 NIC 上。

![](https://substack-post-media.s3.amazonaws.com/public/images/6d534aa6-6601-4c67-8d59-0ad16250ce8c_3200x1695.jpeg)

谷歌允许你按 1 颗到 256 颗 TPUv5e 租用，随着芯片数量增加，成本线性扩展。

每颗 TPU 通过其芯片间互连（ICI）以 400Gbps（400G 发送、400G 接收）连接东、南、西、北四个方向的其他 4 颗 TPU。这使每颗 TPU 拥有高达 1.6T 的聚合带宽，相对于 TPUv5e 的算力与内存带宽而言非常高。谷歌特别注重[以他人没有的方式把光模块数量压到最少](https://www.semianalysis.com/p/nvidias-optical-ascent-1b-revenue)，以进一步降低成本。与 [TPUv4 和 TPUv5 不同，pod 内的 ICI 中没有 OCS，拓扑是扁平的，没有扭曲 Torus 或任何花哨设计](https://www.semianalysis.com/p/google-ai-infrastructure-supremacy)。这在系统层面省下了大量成本。

多个 pod 可以通过数据中心骨干网络（spine network）连接。每个 TPUv5e sled 配一个 100G NIC，意味着 pod 之间拥有 6.4T 的基于以太网的互连。此外，谷歌还提供 multi-pod。这些 pod 间连接经由 OCS。

![](https://substack-post-media.s3.amazonaws.com/public/images/e1eb5a1c-fad8-4d77-9f3f-58deea078817_1600x658.png)

谷歌分享了多达 4,096 颗 TPUv5e（即 16 个 TPUv5e pod）的性能扩展数据。虽然这表明谷歌在一个数据中心内部署了 16 个这样的 pod，但根据他们发布的[视频](https://www.youtube.com/watch?v=FsxthdQ_sL4)，我们相信仅在一个数据中心里，他们就拥有超过 128 个 TPUv5e pod（3.2 万颗 TPUv5e）。

软件方面，谷歌打造了大量软件让这颗芯片易于使用，从编译器到[让 batching 更容易的软件](https://cloud.google.com/tpu/docs/v5e-inference-converter)应有尽有。虽然 Jax+XLA 效果最佳，但 PyTorch+XLA 后端的性能也相当好，意味着许多人几乎无需修改代码即可迁移。对多数人而言，拿一个现成的 LLM 跑推理，和用 GPU 一样简单，甚至可能比英伟达 GPU 更容易达到高利用率，因为要把 GPU 推理做好需要大量手工工作。这主要源于 TensorRT 的封闭性——除了千篇一律的模型之外它几乎无法使用，也无法通过[投机解码（Speculative Decoding）](https://www.semianalysis.com/i/134355860/speculative-decoding)做进一步优化，再加上 FasterTransformers 已被弃用/无人投入。

下面我们来分享 GPT-3 在一个 TPUv5e pod 上与 A100、H100 的训练成本对比，同时分享 LLAMA-65B 的推理成本，以及推理延迟数据。

[获取 8 折团购订阅](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
