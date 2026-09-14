---
title: "秩 rank 和缩放系数 alpha 在实践中如何影响 LoRA 的行为？"
title_en: "How do rank and alpha affect LoRA behavior in practice?"
source: https://sebastianraschka.com/faq/docs/lora-rank-alpha.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 秩 rank 和缩放系数 alpha 在实践中如何影响 LoRA 的行为？

LoRA 将预训练权重矩阵 \(W\) 冻结，并通过两个更小的矩阵来学习一个低秩更新。如果输入是 \(x\)，我们可以把修改后的层写成

\[y = xW + s \cdot xAB,\]

其中 \(r\) 是 \(A\) 和 \(B\) 共享的内维度，\(s\) 是一个缩放因子。秩 \(r\) 和 LoRA 的缩放系数 alpha（LoRA alpha 超参数）影响的是这个表达式的不同部分。

**秩 rank 决定适配器的大小和容量。** 对于形状为 \(d\_{out} \times d\_{in}\) 的权重矩阵，一个秩为 \(r\) 的适配器大约会增加

\[r(d\_{in} + d\_{out})\]

个可训练参数。考虑一个 \(4096 \times 4096\) 的权重矩阵。秩为 8 的适配器增加 65,536 个参数，而原始矩阵本身有 16,777,216 个参数。把秩从 8 提高到 16 会让适配器的参数量翻倍。

更高的秩给更新带来更多自由度。然而，秩翻倍并不意味着模型质量翻倍。对于范围较窄的任务，较小的秩可能已经足以刻画所需的改动。更大的秩在适配任务更复杂时才有用武之地，但它们也会增加优化器内存、检查点大小，以及在较小数据集上拟合噪声的风险。

![两个 LoRA 矩阵构成一条低秩通路，秩决定了内维度的宽度](https://sebastianraschka.com/images/LLMs-from-scratch-images/appendix-e_compressed/lora-2.webp)

**缩放系数 alpha 决定适配器更新的尺度。** alpha 很容易与优化器的学习率混淆，但它们是相互独立的超参数。学习率控制每一步优化步的大小。而 alpha 是在层运行时对 LoRA 的贡献做重新缩放。

许多 LoRA 库使用

\[s = \frac{\alpha}{r}.\]

按照这一约定，秩 8 加 alpha 16 给出的缩放是 2。如果我们在保持 alpha 为 16 的同时把秩改成 16，缩放就会降到 1。这样的对比会同时改变适配器的容量和它的显式缩放。

想要更干净地对比秩，我会保持 \(\alpha/r\) 固定。例如，秩 8 配 alpha 16 与秩 16 配 alpha 32 使用的缩放都是 2。第二个适配器的可训练参数仍是前者的两倍，但作用在其输出上的缩放保持不变。

这个公式是一个值得核实的实现细节。配套材料中那个从零实现的小型 LoRA 层直接把适配器输出乘以 `alpha`，而不除以秩。其他 LoRA 变体则使用各自依赖秩的归一化方式。因此，alpha 取 16 在两个代码库中未必意味着同一件事。

![一个 LoRA 包装器把缩放后的适配器通路加到冻结线性层的输出上](https://sebastianraschka.com/images/LLMs-from-scratch-images/appendix-e_compressed/lora-3.webp)

LoRA 实现通常把一个适配器矩阵用随机值初始化，另一个用零初始化。这样乘积 \(AB\) 在一开始为零，所以添加适配器并不会立即改变预训练模型的输出。随着零初始化的那个矩阵学到非零值，alpha 才开始起作用。

在具体实验中，我通常把秩当作容量选择，把 alpha 当作优化设置的一部分。我会先在保持缩放约定、目标模块、数据和优化器设置不变的情况下，对比几个适中的秩。然后在验证集上把 alpha 和学习率放在一起调。如果适配器欠拟合，提高秩可能有帮助。如果训练不稳定，我会先检查 alpha 和学习率，再下结论说是秩的问题。

并不存在普适的最优组合。有用的设置取决于任务、数据量、目标模块以及具体的 LoRA 实现。主要的注意事项是把生效的缩放公式连同 `rank` 和 `alpha` 一起记录下来。这样结果更容易解读和复现。

关于改变可训练参数数量对内存的影响，参见[为什么与 LoRA 相比全量微调如此昂贵？](https://sebastianraschka.com/faq/docs/full-finetuning-vs-lora-cost.html)（Why is full finetuning so expensive compared with LoRA?）
