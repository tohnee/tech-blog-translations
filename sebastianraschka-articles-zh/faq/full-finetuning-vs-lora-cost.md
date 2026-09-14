---
title: "为什么完全微调比 LoRA 贵这么多？"
title_en: "Why is full finetuning so expensive compared with LoRA?"
source: https://sebastianraschka.com/faq/docs/full-finetuning-vs-lora-cost.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 为什么完全微调比 LoRA 贵这么多？

> 原文：[Why is full finetuning so expensive compared with LoRA?](https://sebastianraschka.com/faq/docs/full-finetuning-vs-lora-cost.html) · Sebastian Raschka's FAQ

完全微调会更新模型中每一个可训练权重。因此内存开销远远超出检查点本身。训练还需要为这些权重保存梯度和优化器状态，外加反向传播所需的激活值。

Adam 让这一差距一目了然。它通常为每个可训练参数维护两个矩估计。即使模型权重使用 `bfloat16`，这些缓冲区也往往以 32 位精度存储。某些混合精度设置还会保留一份 32 位的权重主副本。

作为一个粗略的量级参考：70 亿个 `bfloat16` 参数约占 14 GB；两个 32 位的 Adam 矩缓冲区再增加约 56 GB；梯度和可选的权重主副本还能再加几十 GB——这还没算激活值。确切的总数取决于优化器、精度策略，以及状态是否被分片或卸载。

**LoRA** 冻结原始矩阵，通过两个更小的矩阵来学习一个低秩更新。对于一个形状为 \(d\_{out} \times d\_{in}\)、秩为 \(r\) 的权重，适配器大约包含 \(r(d\_{in}+d\_{out})\) 个可训练值，而不是 \(d\_{in}d\_{out}\) 个。当 \(r\) 很小时，适配器的梯度和优化器状态也相应很小。

![仓库的 LoRA 介绍展示了在原始权重完全微调之外，一条小得多的低秩可训练路径](https://sebastianraschka.com/images/LLMs-from-scratch-images/appendix-e_compressed/lora-1.webp)

这节省了训练基础权重所需的内存，也让任务专属的检查点小得多。多个适配器可以共享同一份原始模型，而不必为每个任务存储一份完整的微调检查点。

LoRA 仍然必须加载冻结的基础模型。普通 LoRA 并不会让这些权重消失，也不会自动对其量化。QLoRA 将低秩适配器与量化后的冻结底座相结合，可以进一步降低这部分内存占用。

激活开销也依然存在。反向传播必须穿过网络，才能为放在较前层的适配器计算梯度。前向传播中，基础模型的大型矩阵乘法仍然要执行。因此，可训练参数的减少幅度可能远大于每步耗时或峰值内存的减少幅度。

![LoRA 可以作为轻量级可训练包装器插入现有线性层，同时保留冻结的预训练检查点](https://sebastianraschka.com/images/LLMs-from-scratch-images/appendix-e_compressed/lora-4.webp)

在部署时，适配器通常可以保持独立，也可以合并进基础权重。当一台服务器要支撑多个任务时，独立适配器很方便。合并则能为固定任务去掉额外的适配器路径，不过会产生一个新的合并检查点。

当数据和算力预算足以支撑更新整个模型，或者当低秩更新限制太大时，完全微调仍然有其价值。而当优化器内存、实验存储或维护大量任务专属变体成为主要成本时，LoRA 尤其有吸引力。
