---
title: "FlashAttention 如何加速 LLM 训练"
title_en: "How FlashAttention Speeds Up LLM Training"
source: https://sebastianraschka.com/faq/docs/flashattention-why-it-mattered.html
crawled: 2026-09-06
translated: 2026-09-14
---

# FlashAttention 如何加速 LLM 训练

> 原文：[How FlashAttention Speeds Up LLM Training](https://sebastianraschka.com/faq/docs/flashattention-why-it-mattered.html) · Sebastian Raschka's FAQ

原始的 [FlashAttention 论文](https://arxiv.org/abs/2205.14135)描述了一种 IO 感知的精确 scaled dot-product attention 算法。它的主要贡献是一种不同的执行顺序，减少了 GPU 高带宽内存与容量小得多但速度更快的片上内存之间的读写。

在直接了当的实现中，注意力首先计算得分矩阵 \(QK^\top\)。对于长度为 \(n\) 的序列，该矩阵为每个注意力头包含 \(n^2\) 个元素。随后实现会施加掩码和 softmax，再把概率与 \(V\) 相乘。把这些中间结果写入 GPU 内存再读回来，所消耗的时间可能超过算术运算本身。

FlashAttention 把输入切分成能装进片上内存的小块（tile）。它每次只计算一个分块的得分，并使用在线 softmax 过程来维护运行中的最大值和归一化项。输出逐块累积，因此不再需要把完整的得分矩阵和概率矩阵存放在高带宽内存中。

![仓库中的多头注意力基准测试图将更快的 PyTorch 注意力路径与较简单的从零实现基线进行了比较](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/mha-benchmark/mha-comparison.webp)

反向传播遵循同样的节省内存思路。它可以从保存的归一化统计量重新计算注意力分块，而不必存储前向传播得到的完整概率矩阵。这是用一些额外的算术换取小得多的激活内存占用。

这仍然是标准的注意力。FlashAttention 没有引入稀疏性，没有改变注意力模式，也没有对 softmax 做近似。由于浮点运算顺序的不同，可能出现微小的数值差异——其他优化核函数同样如此。

计算复杂度相对于序列长度也仍然是二次的。FlashAttention 消除了在高带宽内存中实例化 \(n \times n\) 注意力矩阵的需要，从而大幅改善了实际内存占用，但它并没有把全注意力变成线性时间操作。因此，即使长上下文能装进内存，其开销仍然可能很高。

![在仓库的优化总结中，FlashAttention 是吞吐量和预留内存两方面的重大转折点](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/pytorch-tips/pytorch-tips.webp)

仓库的训练提速实验展示了实际效果。用 PyTorch 的优化路径替换从零实现的注意力后，吞吐量大幅提升，预留内存显著下降。随着序列长度和批次大小的增长，这一收益尤为明显。

在当前的 PyTorch 版本中，当设备、数据类型、头维度等设置受支持时，`scaled_dot_product_attention` 可以分派到 FlashAttention 风格的后端。应当用基准测试确认实际运行的是哪个后端，因为不支持的配置可能会回退到其他实现。

最大的收益通常出现在训练和长提示词预填充（prefill）阶段，此时会同时处理许多查询位置。逐 token 解码每次只有一个新查询，且常常受限于读取 KV 缓存，因此其性能特征有所不同。
