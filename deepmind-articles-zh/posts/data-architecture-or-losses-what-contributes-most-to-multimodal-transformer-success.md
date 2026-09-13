---
title: "数据、架构还是损失函数：什么对多模态 Transformer 的成功贡献最大？"
title_en: "Data, Architecture, or Losses: What Contributes Most to Multimodal Transformer Success?"
source: https://deepmind.google/blog/data-architecture-or-losses-what-contributes-most-to-multimodal-transformer-success/
site: deepmind
date: 2021-02-02
crawled: 2026-09-13
translated: 2026-09-13
---

# 数据、架构还是损失函数：什么对多模态 Transformer 的成功贡献最大？

> 原文：[Data, Architecture, or Losses: What Contributes Most to Multimodal Transformer Success?](https://deepmind.google/blog/data-architecture-or-losses-what-contributes-most-to-multimodal-transformer-success/) · Google DeepMind

将语言锚定（grounding）到视觉是现实世界 AI 系统的一个基本能力；它在一系列任务（例如视觉问答）和应用（例如为视障人士生成描述）中都很有用。多模态模型（在图像-语言对上预训练）正是为了解决这一锚定问题。最近出现的一类模型——多模态 Transformer（如 Lu et al., 2019；Chen et al., 2020；Tan and Bansal, 2019；Li et al., 2020）——在一系列多模态基准测试中取得了最先进的性能，这表明联合编码器（joint-encoder）Transformer 架构比以往的方法（如双编码器）更适合捕捉图像-语言对之间的对齐。

![对比示意图：双编码器（Dual Encoders）使用相互独立的图像编码器和语言编码器，配合图像-语言匹配损失；联合编码器（多模态 Transformer，Joint Encoders）则在单一统一的 Transformer 内同时处理图像块与文本 token，使用图像建模、语言建模和匹配损失。](https://lh3.googleusercontent.com/gEZUcDKk0hxz89Ks7KY2-puji53klG42-XFvkY4E7hpyvO0NGmZmcS3buCcSl0Creo1RrNoTw9BaGXtTvCZU2Zh9_ggiJv7nAZb1xKAuCPtMFeph=w1440)

特别值得一提的是，与两种模态之间没有交叉交互（cross-talk）的双编码器架构相比，多模态 Transformer（联合编码器）的样本效率更高。在下图中我们看到，在零样本图像检索测试中，一个现成的多模态 Transformer（UNITER）的表现与一个训练数据多 100 倍的大规模双编码器（CLIP）相当。

![散点图：比较零样本图像检索性能（R@1）与预训练图像数量。图中显示，在相同训练数据量下，多模态 Transformer（MMT）优于双编码器（BOW-DE）；同时，多模态 Transformer（UNITER）在与双编码器（CLIP）取得相同性能的同时，所需的训练图像显著更少。](https://lh3.googleusercontent.com/XoD7vsvUuc1uG8yBOln2ITw0xAjYAwwA9XeAb9uJI1xS3syVuQl7n0JSGdBb6kKvPtxCKK5P7qao-mraqHDfiePUByMEe1kuDNSgyEFUFfyvGta-rw=w1440)

BOW-DE: Miech & Alayrac et al. Arxiv 2021, MMT: Hendricks et al. TACL 2021, UNITER: Chen et al. ECCV 2020, CLIP: Radford et al. Arxiv 2021, ALIGN: Jia et al. Arxiv 2021

在这项工作中，我们考察了多模态 Transformer 的哪些方面——注意力、损失函数和预训练数据——对其在多模态预训练中的成功至关重要。我们发现多模态注意力（multimodal attention），即语言与图像 Transformer 相互关注彼此，是这些模型成功的关键。采用其他类型注意力的模型（即便深度更深或参数更多）也无法取得与使用多模态注意力的更浅更小模型相当的结果。此外，即便不用最初为多模态 Transformer 提出的图像（掩码区域建模）损失，也能取得可比的结果。这表明我们当前的模型并没有充分利用图像模态中的有用信号，原因可能在于图像损失的设计方式。

我们还研究了多模态数据集的不同属性，例如数据集规模，以及语言对相应图像的描述程度（噪声水平）。我们发现数据集的规模并不总能预测多模态 Transformer 的性能；其噪声水平以及语言与评估任务的相似性都是重要的贡献因素。这些结果表明，整理噪声更少的图像-文本数据集非常重要，尽管当前的趋势是从网络上收集带噪声的数据集。

总体而言，我们的分析表明，多模态 Transformer（在预训练数据量相同的情况下）强于双编码器架构，主要原因在于多模态注意力带来的交叉交互。然而，在设计多模态模型时仍存在许多开放问题，包括针对图像模态更好的损失函数，以及对数据集噪声的鲁棒性。
