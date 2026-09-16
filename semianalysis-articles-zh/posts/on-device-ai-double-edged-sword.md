---
title: "端侧 AI——双刃剑"
title_en: "On Device AI – Double-Edged Sword"
subtitle: "扩展极限、模型尺寸约束、为何服务端 AI 胜出，以及未来的硬件改进"
date: 2023-05-13
source: https://newsletter.semianalysis.com/p/on-device-ai-double-edged-sword
crawled: 2026-09-15
authors: ["Dylan Patel", "Sophia Wisdom"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 端侧 AI——双刃剑

> 原文：[On Device AI – Double-Edged Sword](https://newsletter.semianalysis.com/p/on-device-ai-double-edged-sword) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**扩展极限、模型尺寸约束、为何服务端 AI 胜出，以及未来的硬件改进**

AI 行业被讨论最多的部分，是追逐那些只有科技巨头才开发得起的越来越大的语言模型。训练这些模型成本高昂，而在某些方面，部署它们甚至更难。事实上，OpenAI 的 GPT-4 规模之大、计算之密集，仅运行推理就需要**多台**约 $250,000 的服务器，每台配备 8 块 GPU、大量内存和一堆高速网络设备。Google 对其全尺寸 [PaLM 模型采取类似做法——运行它需要 64 颗 TPU 和 16 颗 CPU](https://www.semianalysis.com/p/google-ai-infrastructure-supremacy)。Meta [2021 年最大的推荐模型需要 128 块 GPU 才能服务用户](https://www.semianalysis.com/i/114314781/the-largest-at-scale-ai-model-architecture-dlrm)。越来越强大模型的世界还会继续扩张，尤其是有 MosaicML 这类专注 AI 的云和 ML Ops 公司协助企业开发与部署 LLM……但更大并不总是更好。

AI 行业还有一个完全不同的宇宙，它拒绝大型机式的计算。[围绕可在客户端设备上运行的小模型的开源运动](https://www.semianalysis.com/p/google-we-have-no-moat-and-neither)大概是这个行业第二受关注的部分。虽然 GPT-4 或完整 PaLM 规模的模型永远别指望在笔记本和智能手机上运行——即便再有 5 年硬件进步，因为[内存墙](https://www.semianalysis.com/i/97006309/the-memory-wall)——但面向端侧推理的模型开发生态正蓬勃发展。

今天我们要讨论的就是这些运行在笔记本、手机等客户端设备上的较小模型。讨论将聚焦推理性能的决定因素、模型尺寸的根本极限，以及未来的硬件发展将如何划定这里的发展边界。

## **为什么需要本地模型**

端侧 AI 的潜在用例广泛而多样。人们想摆脱科技巨头掌控自己全部数据的局面。Google、Meta、百度和字节跳动——AI 领域 5 强中的 4 家——当前的几乎全部盈利都建立在利用用户数据定向投放广告之上。看看整个 [IDFA 风波](https://www.economist.com/the-economist-explains/2022/02/03/how-apples-privacy-push-cost-meta-10bn)就知道，用户隐私的丧失对这些公司有多重要。端侧 AI 可以帮助解决这一问题，同时通过独特的按用户对齐与调优来增强能力。

让较小的语言模型[达到上一代大模型的性能](https://www.semianalysis.com/p/google-we-have-no-moat-and-neither)，是过去几个月 AI 领域最重要的发展之一。

一个简单且容易解决的例子是端侧语音转文字。它相当糟糕，即便是当前标杆级的 Google Pixel 智能手机也是如此。往返云端模型的延迟对自然使用体验也非常突兀，而且严重依赖良好的网络连接。随着 [OpenAI Whisper](https://huggingface.co/openai/whisper-large) 等模型在移动设备上运行，端侧语音转文字的世界正在快速变化。（Google IO 也展示了这些能力可能很快迎来大幅升级。）

更大的例子是 Siri、Alexa 等作为个人助理的糟糕体验。[借助自然语音合成 AI](https://www.npr.org/2023/04/21/1171032649/ai-music-heart-on-my-sleeve-drake-the-weeknd) 的大型语言模型，可以解锁远更有人性、更智能、能协助你生活的 AI 助理。从创建日历事件到总结对话再到搜索，每台设备上都将有一个基于多模态语言模型的个人助理。这些模型[已经远比](https://open-assistant.io/) Siri、Google Assistant、Alexa、Bixby 等强大，而我们仍处于非常早期的阶段。

在某些方面，生成式 AI 正迅速呈现双峰分布：一端是巨型基础模型，另一端是可在客户端设备上运行的较小模型，两者拿走了大部分投资，中间则是一道巨大的鸿沟。

## **端侧推理的根本极限**

尽管端侧 AI 的前景无疑诱人，但存在一些根本性限制，使本地推理比大多数人预想的更具挑战。绝大多数客户端设备没有、也永远不会有独立 GPU，所以所有这些挑战都必须在 SoC 上解决。首要顾虑之一是 GPT 式模型巨大的内存占用和所需算力。计算需求虽然高，但这个问题会在未来 5 年随着更专门的架构、摩尔定律向 3nm/2nm 的推进以及芯片的 3D 堆叠而迅速解决。

最高端的客户端移动设备将因 Intel、AMD、Apple、Google、三星、Qualcomm 和 MediaTek 等公司管线中的架构创新，配备约 500 亿晶体管和远超端侧 AI所需的 TFLOP/s。需要说明，他们现有的客户端 AI 加速器都不适合 transformer，但几年后就会改变。芯片数字逻辑侧的这些进步将解决计算问题，却无法应对真正的底层难题——[内存墙](https://www.semianalysis.com/i/97006309/the-memory-wall)与数据复用。

GPT 式模型的训练目标是给定前文 token 预测下一个 token（≈ 词）。用它们生成文本时，你输入提示词，让它预测下一个 token，再把生成的 token 追加到提示里，再让它预测下一个 token，如此往复。要做到这一点，每次预测下一个 token 时，都必须把全部参数从内存送到处理器。第一个问题是，你必须把所有这些参数存得离计算尽可能近。另一个问题是，你必须能在恰好的时刻把这些参数从内存加载到芯片上。

![](https://substack-post-media.s3.amazonaws.com/public/images/7c034e5a-0d7a-4b83-988f-ceac6c1439b7_704x513.jpeg)

在存储层级中，把频繁访问的数据缓存在片上是大多数工作负载的常见做法。这对端侧 LLM 的问题在于：参数占用的内存空间大到无法缓存。以 FP16 或 BF16 等 16 位数字格式存储的参数占 2 字节。即便最小的「像样的」通用大语言模型 LLAMA 也至少有 70 亿参数，更大的版本质量**显著**更高。仅运行这一模型，16 位精度下就至少需要 14GB 内存。虽然有各种降低内存容量的技术，如[迁移学习、稀疏化和量化](https://www.semianalysis.com/i/98654125/sparsity)，但它们并非没有代价，会影响模型精度。

而且，这 14GB 还没有算上其他应用、操作系统以及[激活值/KV 缓存等相关开销](https://kipp.ly/blog/transformer-inference-arithmetic/)。即便开发者可以假设客户端设备具备所需的算力，这也直接限制了能在端侧部署的模型大小。把 14GB 参数放进客户端处理器在物理上不可能。最常见的片上内存是 SRAM，[即便在 TSMC 3nm](https://www.semianalysis.com/p/tsmcs-3nm-conundrum-does-it-even) 上也只有约每 100mm² 0.6GB。

作为参照，这大约是即将发布的 iPhone 15 Pro 的 A17 芯片的尺寸，比即将发布的 M3 小约 25%。况且该数字还未计入辅助电路、阵列效率、NOC 等开销。大量本地 SRAM 对客户端推理行不通。FeRAM、MRAM 等新兴存储器确实带来了一线曙光，但距离以 GB 为规模的产品化还相当遥远。

层级再往下一层是 DRAM。最高端的 iPhone 14 Pro Max 配 6GB 内存，但主流（众数）iPhone 只有 3GB。高端 PC 会有 16GB 以上，但大多数*新*销售的 PC 是 8GB 内存。典型客户端设备跑不了量化到 FP16 的 70 亿参数模型！

这就引出了一个问题：为什么不再往层级下面走一层？能不能不放在内存里，而是让这些模型直接从基于 NAND 的 SSD 上运行？

很遗憾，这实在太慢了。70 亿参数模型在 FP16 下，仅为流入权重以产出 1 个 token（约 4 个字符）就需要 14GB/s 的 IO！最快的 PC 存储驱动器顶多 6GB/s，而大多数手机和 PC 不到 1GB/s。在 1GB/s 下、4-bit 量化，能跑的最大模型仍只有约 20 亿参数量级——而且这还是让 SSD 为单个应用满负荷运转、完全无视其他用例的结果。

![](https://substack-post-media.s3.amazonaws.com/public/images/3acdf863-fa8e-461f-8c96-6a5221bcf2d4_1010x735.png)

除非你愿意在普通设备上干等 7 秒钟吐出半个词，否则把参数放在存储里不是选项。它们必须放在内存里。

## **模型尺寸的极限**

普通人阅读速度约为每分钟 250 词。作为良好用户体验的下限，端侧 AI 必须每秒生成 8.33 个 token，也就是每 120ms 一个。熟练的速读者可以达到每分钟 1,000 词，因此作为上限，端侧 AI 必须能每秒生成 33.3 个 token，即每 30ms 一个。下图按平均阅读速度（而非速读）的下限假设绘制。

![](https://substack-post-media.s3.amazonaws.com/public/images/194956ff-1cd2-43c1-996d-041c607c0b0e_1701x790.png)

如果我们保守地假设普通非 AI 应用以及[激活值/KV 缓存](https://kipp.ly/blog/transformer-inference-arithmetic/)消耗一半带宽，那么 iPhone 14 上可行的最大模型尺寸约为 10 亿 FP16 参数，或约 40 亿 int4 参数。这就是基于智能手机的 LLM 的根本极限。再大就会把装机量中太大的一部分排除在外，导致无法普及。

这是本地 AI 能做多大、多强的根本极限。也许 Apple 这样的公司可以借此向上推销更贵、AI 更强的新手机，但那还比较遥远。按同样的假设，在 PC 上，Intel 顶级的 13 代 i9 CPU 和 Apple 的 M2 的上限约为 30 亿至 40 亿参数。

总体而言，这些只是消费类设备的下限。再强调一次，我们忽略了多个因素，包括采用理论 IO 速度（实际永远达不到），以及为简化起见忽略的[激活值/KV 缓存](https://kipp.ly/blog/transformer-inference-arithmetic/#intermediate-memory-costs)。这些因素只会把带宽需求推得更高，把模型尺寸压得更小。下面我们会进一步谈明年将至、有望重塑格局的创新硬件平台，但[内存墙](https://www.semianalysis.com/p/nvidiaopenaitritonpytorch)限制着当前和未来大多数设备。

## **为何服务端 AI 胜出**

由于极端的内存容量和带宽需求，生成式 AI 受[内存墙](https://www.semianalysis.com/i/97006309/the-memory-wall)的影响超过以往任何应用。在客户端推理中，对于文本生成模型，batch size（批大小）几乎总是 1。每个后续 token 都要求把此前的 token/提示词重新输入，意味着每次把一个参数从内存加载到芯片上，只能摊给仅仅 1 个生成的 token。没有其他用户可以分摊这一瓶颈。[内存墙](https://www.semianalysis.com/i/97006309/the-memory-wall)在服务端计算上同样存在，但每次加载一个参数，可以摊给多个用户的多个生成 token（批大小）。

我们的数据显示，HBM 内存接近 H100 或 TPUv5 这类服务器级 AI 芯片制造成本的一半。虽然客户端计算确实用得上便宜得多的 DDR 和 LPDDR 内存（每 GB 约 1/4 的价格），但那部分内存成本无法摊给多个并发推理。批大小也不能无限拉大，因为那会引入另一个棘手问题：任何一个 token 都必须等其他所有 token 处理完，才能追加其结果并开始生成新 token 的工作。

![](https://substack-post-media.s3.amazonaws.com/public/images/bb322200-39e6-42e0-b8e8-98d2502a2236_468x373.png)

这个问题的解法是把模型切分到多颗芯片上。上图是生成 20 个 token 的延迟。方便的是，PaLM 模型在 64 颗芯片以批大小 256 运行推理时，恰好达到每秒 6.67 个 token、即约每分钟 200 词的最低可行目标。这意味着每次加载一个参数，它被用于 256 个不同的推理。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

随着批大小增加，FLOPS 利用率会改善，因为[内存墙](https://www.semianalysis.com/i/97006309/the-memory-wall)得到了缓解。而延迟只有通过把工作切分到更多芯片上才能降到合理水平。即便如此，也只有 40% 的 FLOPS 被真正利用。Google 曾展示[ PaLM 推理达到 76% 的 FLOPS 利用率、延迟 85.2 秒](https://arxiv.org/pdf/2211.05102.pdf)，所以[内存墙](https://www.semianalysis.com/i/97006309/the-memory-wall)显然仍是一个巨大的制约因素。

所以服务端效率高得多，但本地模型又能扩展到什么程度？

## **客户端模型架构演进与硬件进步**

有多种技术可以尝试增加客户端模型可用的参数量。此外，特别是来自 Apple 和 AMD 的一些有趣硬件进展，可能有助于进一步扩展。

[团体订阅享 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
