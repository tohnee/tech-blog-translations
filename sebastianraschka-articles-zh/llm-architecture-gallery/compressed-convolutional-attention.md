---
title: "压缩卷积注意力"
title_en: "Compressed convolutional attention"
source: https://sebastianraschka.com/llm-architecture-gallery/compressed-convolutional-attention/
crawled: 2026-09-06
translated: 2026-09-06
---

# 压缩卷积注意力

> 原文：[Compressed convolutional attention](https://sebastianraschka.com/llm-architecture-gallery/compressed-convolutional-attention/)

压缩卷积注意力（Compressed Convolutional Attention，CCA）直接在压缩的潜在空间中执行注意力运算。ZAYA1-8B 将它与分组查询注意力（GQA）搭配使用。

与 Laguna 类似，ZAYA1-8B 是开放权重市场上的又一位新玩家。它由 [Zyphra](https://www.zyphra.com/post/zaya1-8b) 开发，围绕这次发布的一个有趣细节是：该模型是在 AMD GPU 上训练的，而不是更常见的 NVIDIA GPU（或 Google TPU）配置。

不过，最核心的架构细节是 CCA，它与分组查询注意力搭配使用。与 MLA 风格的设计（主要把潜在表示当作一种紧凑的 KV 缓存格式）不同，CCA 直接在压缩潜在空间中执行注意力运算，这一点后面还会展开。

（题外话：ZAYA1-8B 的 [`config.json`](https://huggingface.co/Zyphra/ZAYA1-8B/blob/main/config.json) 列出了 80 个交替出现的层条目，而不是 40 个常规 transformer 块。这些条目在 CCA/GQA 注意力层与 MoE 前馈层之间交替。但为了便于绘制架构图，把它可视化为 40 组重复的"注意力 + MoE"对更方便，两者在概念上是等价的。）

[架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
[文章章节](https://magazine.sebastianraschka.com/p/recent-developments-in-llm-architectures#%C2%A74-compressed-convolutional-attention-zaya1-8b)
[CCA 论文](https://arxiv.org/abs/2510.04476)
[ZAYA1 配置](https://huggingface.co/Zyphra/ZAYA1-8B/blob/main/config.json)

![采用压缩卷积注意力的 ZAYA1-8B 架构](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/zaya1-cca-architecture.webp)

图 11. 采用压缩卷积注意力 transformer 块的 ZAYA1-8B。（原始出处
[*Recent Developments in LLM Architectures*](https://magazine.sebastianraschka.com/p/recent-developments-in-llm-architectures)。）

## 什么是压缩卷积注意力？

正如上图所暗示的，ZAYA1-8B 将 CCA 与 4:1 的 GQA 布局结合使用。关键在于，它的注意力块是围绕 CCA 构建的，而不是标准的滑动窗口注意力块。

我认为 CCA 在精神上与 DeepSeek 模型中的[多头潜在注意力（MLA）](https://sebastianraschka.com/llm-architecture-gallery/mla/)有关联，因为两者都在注意力块中引入了压缩的潜在表示。但它们对这个潜在空间的使用方式不同。MLA 主要用潜在表示来缩减 KV 缓存：在 MLA 中，KV 张量以紧凑形式存储，随后再被投影到注意力头空间中进行实际的注意力计算。

![多头潜在注意力与压缩卷积注意力的并排对比](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/zaya1-cca-mla-comparison.webp)

图 13. 多头潜在注意力（MLA）与压缩卷积注意力（CCA）的并排对比。
（原始出处
[*Recent Developments in LLM Architectures*](https://magazine.sebastianraschka.com/p/recent-developments-in-llm-architectures)。）

## 卷积在哪里发挥作用

CCA 压缩 Q、K、V，并直接在压缩潜在空间中执行注意力运算。这正是 CCA 不仅能够减小 KV 缓存大小，还能降低预填充（prefill）和训练期间注意力 FLOPs 的原因。

如图 13 所示，在 CCA 中，压缩后的潜在表示直接进入注意力机制，随后得到的压缩注意力向量再被向上投影。

注意，它叫"压缩卷积注意力"，而不是仅仅叫"压缩注意力"，因为在潜在 K 和 Q 表示上还发生了一个额外的卷积混合过程。图 13 没有展示这个卷积混合部分，因为画进去会太拥挤，但它其实相当直观。

如图 13 所暗示的，卷积混合直接作用在压缩后的 Q 和 K 张量上。这里的要点是：压缩使 Q、K、V 变窄，从而节省计算和缓存开销，但这也可能让注意力的表达能力下降。这些卷积是一种廉价的方式，可以在压缩后的 Q 和 K 向量被用于计算注意力分数之前，为它们补充更多局部上下文。（卷积混合只作用于 Q 和 K，而不作用于 V，因为 Q 和 K 决定注意力分数，而 V 代表通过这些分数被加权平均的内容。）

![对压缩查询和键做序列混合的卷积](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/zaya1-cca-convolutional-mixing.webp)

图 14. 序列混合卷积的概念性概览。（原始出处
[*Recent Developments in LLM Architectures*](https://magazine.sebastianraschka.com/p/recent-developments-in-llm-architectures)。）

除了图 14 所示的序列混合之外，还有一个通道混合（channel-mixing）组件。其原理与之类似，因此我略去了配图。

## 论文报告了什么

CCA 似乎是 Zyphra 提出的一种注意力机制，出现时间早于 ZAYA1-8B 技术报告。独立的 CCA 论文《[Compressed Convolutional Attention: Efficient Attention in a Compressed Latent Space](https://arxiv.org/abs/2510.04476)》于 2025 年 10 月首次发布，正式提出了 CCA。随后，ZAYA1-8B 将这一机制用作其核心组件之一。

但问题在于："它比 MLA 更好吗？"根据 CCA 论文自己的实验，答案是肯定的：他们报告在可比压缩设置下，CCA 优于 MLA。

总的来说，这里真正有趣的部分其实是这个新的注意力机制。该模型还使用了相当极端（= 非常稀疏）的 MoE 配置，每个 token 只有一个路由专家处于激活状态，但这部分相对更眼熟。CCA 之所以更不寻常，是因为它直接在压缩潜在空间中执行注意力运算，然后对压缩后的 Q 和 K 表示施加卷积混合，以减轻这种压缩注意力带来的限制。简而言之，ZAYA1-8B 不仅试图在前馈层中节省计算，也在注意力机制本身中节省计算。

参考资料

[Recent Developments in LLM Architectures](https://magazine.sebastianraschka.com/p/recent-developments-in-llm-architectures#%C2%A74-compressed-convolutional-attention-zaya1-8b)
[Compressed Convolutional Attention 论文](https://arxiv.org/abs/2510.04476)
[ZAYA1-8B 技术报告](https://arxiv.org/abs/2605.05365)
[ZAYA1-8B config.json](https://huggingface.co/Zyphra/ZAYA1-8B/blob/main/config.json)
[Zyphra ZAYA1-8B 发布文章](https://www.zyphra.com/post/zaya1-8b)

[返回架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
