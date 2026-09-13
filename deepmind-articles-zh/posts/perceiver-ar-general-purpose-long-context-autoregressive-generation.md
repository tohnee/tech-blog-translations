---
title: "Perceiver AR：通用、长上下文的自回归生成"
title_en: "Perceiver AR: general-purpose, long-context autoregressive generation"
source: https://deepmind.google/blog/perceiver-ar-general-purpose-long-context-autoregressive-generation/
site: deepmind
date: 2022-07-16
crawled: 2026-09-13
translated: 2026-09-13
---

# Perceiver AR：通用、长上下文的自回归生成

> 原文：[Perceiver AR: general-purpose, long-context autoregressive generation](https://deepmind.google/blog/perceiver-ar-general-purpose-long-context-autoregressive-generation/) · Google DeepMind

过去几年，自回归 Transformer 在生成建模领域带来了一连串突破。这类模型逐个预测元素，从而生成样本的每个组成部分——图像的像素、文本的字符（通常以"token"块为单位）、音频波形的采样点等等。在预测下一个元素时，模型可以回看先前已生成的元素。

然而，随着用作输入的元素增多，Transformer 的每一层的计算开销都会随之增长，因此研究者只能在长度不超过约 2048 个元素的序列上训练深层 Transformer。于是，大多数基于 Transformer 的模型在进行预测时会忽略最近过去（约 1500 个词或一张小图像的 1/6）之外的所有元素。

相比之下，我们近期开发的 [Perceiver 模型](https://deepmind.google/blog/building-architectures-that-can-handle-the-worlds-data/)在多达约 10 万个元素的各种现实任务上都取得了出色的结果。Perceiver 使用交叉注意力（cross-attention）将输入编码到一个潜在空间（latent space）中，把输入的计算需求与模型深度解耦。而且无论输入大小如何，Perceiver 几乎在每一层都只花费固定的成本。

虽然潜在空间编码可以在一次前向传播中处理所有元素，但自回归生成假定处理是逐个元素进行的。为解决这一问题，Perceiver AR 提出了一个简单的方案：将潜在向量（latents）与输入的末尾元素逐一对应，并仔细地对输入进行掩码（masking），使每个潜在向量只能看到更早的元素。

![Perceiver AR 架构图，展示如何使用带因果掩码的交叉注意力将大量输入映射到少量潜在向量，随后通过潜在自注意力层来预测目标输出。](https://lh3.googleusercontent.com/Ck0klfj8QgSgTWELIbAJuXqhVNaExAsUia6ysY8C9yj8-uV6nUaqwJ-YfwwWpoN47kP5huaYPqXToKS7pl7QgmB7Rp_7tZRFDsgNmciCDtN4AY7JMw=w1440)

Perceiver AR 通过交叉注意力将输入序列（P e r c e i v e r A R）映射到一个小的潜在空间，为每个目标 token 生成一个潜在向量（图中展示了 3 个潜在向量，分别对应目标 A、R、<EOS>，<EOS> 表示**序**列**结**束）。这些潜在向量随后由一个深层的自注意力层堆栈处理。Perceiver AR 可以端到端地训练进行自回归生成，同时还能利用非常长的输入序列。

其结果就是上图所示的架构：它能处理的输入长度最高可达标准 Transformer 的 50 倍，同时又能像标准 decoder-only Transformer 一样被广泛部署（部署难度也基本相同）。

![散点图对比 Perceiver AR（蓝色）、Transformer-XL（橙色）和标准 Transformer（绿色）的训练速度（纵轴，每秒步数）与上下文长度（横轴）的关系。与其他架构相比，Perceiver AR 能扩展到更长的上下文长度（最高 65,536），同时保持更高的训练速度和更深的模型层数（以圆圈大小表示）。](https://lh3.googleusercontent.com/y8wMRp9d0-ADOts7ZXylO4Uzs83MNYBMPH3ZnnvdjnG5pvFOQc6C25d_gerF7iBx2rLPMzWEp1Tw5BRavbAYkcGV5rMj2DMAggIdXk44SkdlbaQuSg=w1440)

随着上下文长度或模型规模的增加，训练模型所需的算力也随之增长。我们可以通过测量不同模型在真实硬件上的速度（TPUv3 上每秒的步数）来量化其算力预算，观察其随输入上下文长度和模型规模变化的规律。与 Transformer 或 Transformer-XL 等其他生成模型不同，Perceiver AR 将输入上下文长度与模型深度解耦，使我们能够轻松地在现役 TPU 或 GPU 上部署建模长序列所需的深层模型。

在多种实际序列长度下，Perceiver AR 随规模扩展的表现都明显优于标准 Transformer 和 Transformer-XL 模型。这一特性使我们能够构建非常高效的长上下文模型。例如，我们发现一个上下文长度为 8192 的 60 层 Perceiver AR 在书本长度的生成任务上优于 42 层的 Transformer-XL，而且以真实时钟时间衡量运行得更快。

在标准的长上下文图像（ImageNet 64x64）、语言（PG-19）和音乐（MAESTRO）生成基准测试上，Perceiver AR 取得了最先进的结果。通过将输入规模与算力预算解耦来增加输入上下文，带来了几个引人入胜的结果：

- 算力预算可以在评估时调整，让我们既能花得更少、平滑地降低质量，也能花得更多以改进生成效果。
- 更大的上下文让 Perceiver AR 即使在与 Transformer-XL 花费相同算力的情况下也能胜出。我们发现，即使在可负担的规模（约 10 亿参数）下，更大的上下文也能提升模型性能。
- Perceiver AR 的样本质量对元素生成顺序的敏感度要低得多。这使 Perceiver AR 很容易应用于那些没有自然从左到右顺序的场景，例如图像这类结构跨越多个维度的数据。

我们用钢琴音乐数据集训练 Perceiver AR 从零开始生成新的乐曲。由于每个新音符都是基于之前完整音符序列预测的，Perceiver AR 能够创作出旋律、和声与节奏高度连贯的乐曲：

了解更多关于使用 Perceiver AR 的信息：

- 在 [Github](https://github.com/google-research/perceiver-ar) 上下载用于训练 Perceiver AR 的 JAX 代码
- 在 [arXiv](https://arxiv.org/abs/2202.07765) 上阅读我们的论文
- 观看我们在 [ICML 2022](https://icml.cc/virtual/2022/spotlight/17886) 上的 spotlight 报告

查看 Google Magenta 的[博客文章](https://magenta.tensorflow.org/perceiver-ar)，聆听更多音乐！
