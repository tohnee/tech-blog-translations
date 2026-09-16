---
title: "AI 砖墙——稠密 Transformer 模型扩展的实用极限，以及 GPT 4 将如何突破它"
title_en: "The AI Brick Wall – A Practical Limit For Scaling Dense Transformer Models, and How GPT 4 Will Break Past It"
date: 2023-01-24
source: https://newsletter.semianalysis.com/p/the-ai-brick-wall-a-practical-limit
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# AI 砖墙——稠密 Transformer 模型扩展的实用极限，以及 GPT 4 将如何突破它

> 原文：[The AI Brick Wall – A Practical Limit For Scaling Dense Transformer Models, and How GPT 4 Will Break Past It](https://newsletter.semianalysis.com/p/the-ai-brick-wall-a-practical-limit) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

大型生成式 AI 模型为世界释放了巨大价值，但图景并非只有玫瑰。这些重新定义文明的模型，其训练成本正以惊人的速度膨胀。现代 AI 的建立，靠的是参数量、token 数和总体复杂度每年提升一个数量级的扩展。本报告将讨论稠密（dense）Transformer 模型扩展面临的砖墙、为突破这堵墙而开发的技术与策略，以及 GPT 4 将采用其中哪些具体手段。

最著名的模型，如 GPT、BERT、Chinchilla、Gopher、Bloom、MT-NLG、PaLM 和 LaMDA，都是 Transformer。Transformer 是多层感知机（MLP）网络的一种，*通常*被视为稠密矩阵模型。稠密模型是全连接的：一层的所有「神经元」与下一层的所有「神经元」相连。这使模型能够学习特征之间的复杂交互、学习非线性函数。海量的信息可以嵌入这些模型的数十亿参数之中。

值得指出的是，自然界的大脑并不是这样运作的。动物王国的大脑网络架构与现有硬件的匹配度不佳，因此其 [FLOPS 利用率](https://www.semianalysis.com/i/97006309/machine-learning-training-components)会低得多。历史上，稠密矩阵模型在参数量、数据（token）和复杂度的扩展上，一直远优于其他模型架构。

## **先有鸡还是先有蛋？**

这是个脑筋急转弯——先有的是 GPU。

Nvidia 的 GPU 架构天生就非常适合运行稠密矩阵模型，这推动 Transformer 的能力扩展速度远超其他任何模型架构。能力增强的同时也带来了人气的爆发。规模在 AI 里几乎意味着一切，于是那个价值十亿美元的问题来了：这些模型未来几年还能否继续依托现有的稠密架构扩展下去？

[MosaicML](https://www.mosaicml.com/blog/gpt-3-quality-for-500k) 已经声称能够以不到 $500,000 的成本训练出 GPT-3 品质的模型，以约 $2,500,000 训练出 [Chinchilla](https://arxiv.org/pdf/2203.15556.pdf) 规模和品质的模型。[他们今天就已经在向客户提供这个价格。](https://www.mosaicml.com/cloud)

这比多数人预想的便宜得多，于是引出问题：我们还能往上扩多少？

上周，我们讨论了机器学习的组成要素、模型利用率以及软件栈。

[![](https://substackcdn.com/image/fetch/$s_!HwSb!,w_56,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fbucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com%2Fpublic%2Fimages%2F0150776c-9bf2-4bea-a9c2-41b24b7a0f15_1280x1280.png)SemiAnalysisNvidia 的 CUDA 机器学习垄断正在被打破——OpenAI Triton 与 PyTorch 2.0（How Nvidia's CUDA Monopoly In Machine Learning Is Breaking - OpenAI Triton And PyTorch 2.0）过去十年，机器学习软件开发的格局发生了重大变化。许多框架来了又去，但大多数都严重依赖 Nvidia 的 CUDA，并在 Nvidia GPU 上表现最佳。然而，随着 PyTorch 2.0 和 OpenAI Triton 的到来，Nvidia 在这一领域的主导地位——主要源于其软件护城河——正在被颠覆……阅读更多 · 4 年前 · 67 个赞 · 16 条评论 · Dylan Patel](https://www.semianalysis.com/p/nvidiaopenaitritonpytorch?utm_source=substack&utm_campaign=post_embed&utm_medium=web)

关键的结论是：即便用上生态系统在 2022 年开发的全部优化技术，Nvidia A100 GPU 在训练大语言模型时的模型/硬件 FLOPS 利用率上限也只有约 60%（[模型/硬件 FLOPS 利用率](https://github.com/mosaicml/examples/tree/main/llm/throughput)）。

SemiAnalysis 的研究团队调研了许多初创公司和 enterprises，得出一个基线成本：对于配备 NVLink 和 1.6T 网络的 **256 GPU 大型集群**，每块 SXM A100 GPU 每小时约 $1.5。一些公司与 AWS、Azure、Oracle Cloud、CoreWeave 等拿到了更好的价格，但这是一个基线。如果采购 GPU 的公司同意签三年合约，条件还会好得多。例如 Azure 的目录价只有每小时 $1.36，但为 2020 年发布的 A100 签下三年合约并不是多数人愿意做的事。如果稼动率高，自建（on-premises）在多年维度上也会更便宜，但这对多数企业和初创公司来说都很难承诺、也很难做到。

## **当前最先进模型一览**

![](https://substack-post-media.s3.amazonaws.com/public/images/1d30755f-7ece-47d4-bb91-acad82473df8_3362x2035.png)

上表展示了公开披露的最先进模型及其各自的参数量和 token 数（训练数据单位）。那条线是 [Google DeepMind 的 Chinchilla 扩展观测](https://arxiv.org/pdf/2203.15556.pdf)（对较大的误差线做了平滑处理）。线上每个点表示训练对应参数量和 token 数的模型所需的理论 FLOPS。所示 FLOPS 数字忽略了激活值的重计算、checkpointing 等。

这些公开披露的模型相当密集地聚在一起。疯狂的是，通过我们做风险投资尽调掌握的情况，我们知道有 21 家初创公司和另外 11 家大公司正在训练参数量/token 数足以在理论上达到 GPT-3 品质或更好的大模型。现在完全是蛮荒西部，观察并投资于胜出者将非常激动人心。

一旦知道参数量、token 数和模型架构，就能很容易地算出许多知名模型的理论训练成本。在这个例子中，我们使用 Nvidia A100，按每 GPU 每小时 $1.5 计算。正如我们[在此](https://www.semianalysis.com/i/97006309/the-memory-wall)解释的，随着模型规模增大，[模型/硬件「FLOPS 利用率」](https://github.com/mosaicml/examples/tree/main/llm/throughput)会从 40% 提升到 60%，但总体而言，在大型分布式系统上已没有多少再往上走的空间。

## **最先进模型的训练成本**

![](https://substack-post-media.s3.amazonaws.com/public/images/95802dd0-c7c3-4fc0-9bef-be31971cbf85_1677x822.png)

这张表是用 Nvidia A100 训练模型的理论最优成本。它没有计入所需人员、ML Ops 工具、数据收集/预处理、故障恢复、one-shot/few-shot 学习样本、推理等。其中许多环节的成本高得惊人。在这一口径下，[MosaicML 对 GPT-30B 收 $450k、对 GPT-70B 收 $2.5M](https://www.mosaicml.com/blog/gpt-3-quality-for-500k) 的报价，与 $326k 和 $1.75M 的最优训练成本相当接近。应当指出，Mosaic 的价格包含了诸多 ML Ops 工具，这显著降低了可靠训练一个模型所需的人力。

沿着这张表往下看，Google 的 Pathways 语言模型（PaLM）是已训练并公开详述的最先进稠密模型。虽然我们用 Nvidia A100 作为成本比较的基线，但要注意 PaLM 是在 6,144 块 Google 自研 TPU v4 上训练的。Google 实现了 [46.2% 的模型 FLOPS 利用率和 57.8% 的硬件 FLOPS 利用率。](https://arxiv.org/pdf/2204.02311.pdf)训练 PaLM 的算力成本并不算高不可攀。

如今，多数人训练稠密模型会更遵循 [Chinchilla 扩展观测](https://arxiv.org/pdf/2203.15556.pdf)。该观测指出：在给定算力下，相比当前最先进模型，训练一个参数更少但数据更多的模型更具成本效益。尽管 Chinchilla 观测受到很多批评（包括极宽的误差线和对结果的过度外推），但其方向性判断是准确的。

## **稠密 Transformer 的扩展之墙**

![](https://substack-post-media.s3.amazonaws.com/public/images/1e394df3-9c1e-435e-9968-d9c48f803bed_1691x692.png)

就参数量增长而言，用稠密模型在现有硬件上，产业界已逼近极限——训练一个 1 万亿参数模型的成本约为 $3 亿。用 100,000 块 A100 组成 12,500 套 HGX / DGX 系统，训练大约需要约 3 个月。对于最大的那批科技公司，这在当前硬件的可行范围内毫无问题。集群硬件成本将在几十亿美元量级，完全装得进 Meta、Microsoft、Amazon、Oracle、Google、Baidu、腾讯、阿里巴巴这些巨头的数据中心资本开支（capex）预算。

再往上扩一个数量级就是 10 万亿参数。按小时费率计算，训练成本将放大到约 $300 亿。即便用 100 万块 A100 组成 125,000 套 HGX / DGX 系统，训练这个模型也要超过两年。仅加速器系统和网络的功耗就会超过一座核反应堆的发电量。如果目标是约 3 个月内训练完这个模型，按当前硬件，所需的服务器总 capex 将达数千亿美元。

这不现实，而且考虑到当前的错误率和量化估计，模型也很可能根本无法扩展到这个规模。

[分享](https://newsletter.semianalysis.com/p/the-ai-brick-wall-a-practical-limit?utm_source=substack&utm_medium=email&utm_content=share&action=share)

以当前硬件、按 Chinchilla 最优方式训练的稠密 Transformer，其实用极限在算力成本上介于约 1 万亿至约 10 万亿参数之间。在后续报告中，我们将针对稠密 vs. 稀疏模型，以及 Google TPUv4、TPUv5、Nvidia A100、H100 和 AMD MI300 的成本竞争力，进一步讨论这个区间。数据是另一个问题，我们以后可以展开。

虽然 1 万亿到 10 万亿是当前硬件的实用极限，但新硬件正在到来。此外，过去一年里发展出了相当多的策略与技术，既能降低训练成本，又能扩展到更高的参数量。

训练效率（training efficiency）是关键观察指标。训练效率指相对于此前最先进水平，为达到更优模型品质所消耗的算力和训练时间。模型架构不会停滞不前，训练效率将会提升。

本报告接下来的 **2/3 内容为订户专享**，覆盖能够提升训练效率、降低大模型推理成本的具体策略与技术。请记住：训练好的模型在部署运行推理之前毫无用处，而多数硬件成本最终将来自模型推理。

这些策略将随 2023 年的新模型落地，其中包括 OpenAI 将在 GPT 4 中使用的某些具体手段。这些技术与策略也将被 Google、Deepmind、MosaicML、Microsoft、Nvidia、清华大学、HuggingFace、Stability、AI21、Anthropic、Cerebras、SambaNova、TensTorrent、Cohere、Neural Magic 等公司大量采用。

我们下面将讨论的所有策略与技术，以及更多内容，都由上述公司在 NeurIPS 上发表过。NeurIPS 是机器学习的顶级会议。今年约 10,000 份投稿中有约 2,905 篇论文入选，现场参会者约 10,000 人。今天我们聚焦那些已走出研究阶段、进入应用世界的工作。如果想看一份对研究界覆盖更细的优秀 newsletter，推荐 [Davis Summarizes Papers——Davis Blalock 已总结了数百篇方法新颖的论文。](https://dblalock.substack.com/)

[![](https://substackcdn.com/image/fetch/$s_!2Iqq!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fbucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com%2Fpublic%2Fimages%2F4da41de1-cb9d-4505-984f-e6e63c23ef0c_512x512.png)Davis Summarizes Papers我每周通读机器学习 arXiv 的全部投稿，并从中挑选 10 到 20 篇我最喜欢的做总结。
永久免费，已有超过 2000 位机器学习研究者与从业者阅读。作者：Davis Blalock](https://dblalock.substack.com?utm_source=substack&utm_campaign=publication_embed&utm_medium=web)

[团体订阅享 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
