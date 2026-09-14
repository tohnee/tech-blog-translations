---
title: "语言模型的 LoRA 与全量微调"
title_en: "LoRA vs. Full Finetuning of Language Models"
source: https://sebastianraschka.com/faq/docs/lora-vs-full-finetuning.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 语言模型的 LoRA 与全量微调

**LoRA** 是 **Low-Rank Adaptation（低秩适配）** 的缩写，它常常是适配大型预训练模型时的实用起点。它保持原始权重冻结，只为选定的线性层学习小的更新。而全量微调则允许模型的所有可训练权重都发生变化。

假设某个线性层包含权重矩阵 \(W\)。全量微调直接学习 \(W\) 的更新版本。LoRA 则把改动表示为两个更小矩阵的乘积，

\[W\_{adapted} = W + AB,\]

其中 \(A\) 和 \(B\) 的内维度就是 LoRA 的秩 rank。预训练矩阵 \(W\) 在训练期间保持冻结。

![全量微调更新原始权重矩阵，而 LoRA 学习的是一个独立的低秩更新](https://sebastianraschka.com/images/LLMs-from-scratch-images/appendix-e_compressed/lora-1.webp)

这一差异对优化器内存影响很大。全量微调要为每个可训练的模型参数保存梯度和优化器状态。LoRA 只需为适配器权重保存这些训练专用的张量。对于一个形状为 \(d\_{out} \times d\_{in}\)、LoRA 秩为 \(r\) 的矩阵，适配器大约包含 \(r(d\_{in}+d\_{out})\) 个参数，而不是 \(d\_{in}d\_{out}\) 个参数。

LoRA 仍然需要加载冻结的基座模型，前向传播也仍然要执行该模型中的大型矩阵乘法。它还保留了反向传播所需的大部分激活内存。因此，可训练参数减少 99% 并不等于峰值内存或训练时间减少 99%。QLoRA 可以通过以量化格式保存冻结权重来进一步降低基座模型的内存占用。

![一个 LoRA 包装器在冻结线性层旁增加一条小的可训练通路](https://sebastianraschka.com/images/LLMs-from-scratch-images/appendix-e_compressed/lora-3.webp)

检查点存储是使用 LoRA 的另一个强有力的理由。一个团队可以只保留一个基座模型，然后为每个任务或每个客户保存一个小适配器。在推理时，适配器可以保持独立，也可以合并进基座权重的一份副本。一次全量微调会产生一个完整的任务专用检查点，作为单一制品分发更简单，但存储体积要大得多。

在模型质量方面，并没有自动的赢家。当所需的权重改动能够被低秩更新很好地表达时，LoRA 可以媲美全量微调。这常常使它很适合指令微调、分类，以及其他预训练模型已具备大部分所需能力的适配任务。

全量微调拥有更多自由，因为每个权重都可以独立变化。这种自由在领域迁移很大、需要大量延续训练、或 LoRA 已明显触及性能上限的任务上可能会有帮助。但它也引入了多得多的可训练参数。在较小的数据集上，这些额外的自由度并不能保证带来更好的验证结果。

我实际的决策流程很简单。当 GPU 内存有限、预期要维护多个任务专用变体、或想快速比较不同训练方案时，我会从 LoRA 开始。如果调优得当的 LoRA 仍然达不到要求，且算力预算允许，全量微调就是下一个值得做的实验。这也给了这种更昂贵的方法一个需要超越的具体性能目标。

做对比时应当使用相同的数据划分和评估流程。LoRA 的结果还取决于适配器的秩、缩放系数和目标模块。一个孱弱的 LoRA 配置并不能证明参数高效微调已经到了极限。

相关细节可参见[为什么与 LoRA 相比全量微调如此昂贵？](https://sebastianraschka.com/faq/docs/full-finetuning-vs-lora-cost.html)（Why is full finetuning so expensive compared with LoRA?）、[秩 rank 和缩放系数 alpha 在实践中如何影响 LoRA 的行为？](https://sebastianraschka.com/faq/docs/lora-rank-alpha.html)（How do rank and alpha affect LoRA behavior in practice?），以及[LoRA 适配器插入 LLM 的哪些位置影响最大？](https://sebastianraschka.com/faq/docs/where-to-insert-lora-adapters.html)（Where should LoRA adapters be inserted in an LLM for the biggest impact?）。
