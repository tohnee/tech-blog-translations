---
title: "多 GPU 训练之前应先做的单 GPU 优化"
title_en: "Single-GPU Optimizations Before Multi-GPU Training"
source: https://sebastianraschka.com/faq/docs/first-optimizations-before-multi-gpu.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 多 GPU 训练之前应先做的单 GPU 优化

> 原文：[Single-GPU Optimizations Before Multi-GPU Training](https://sebastianraschka.com/faq/docs/first-optimizations-before-multi-gpu.html) · Sebastian Raschka's FAQ

在增加更多 GPU 之前，我会先测量单 GPU 训练循环。有用的基线指标包括每秒处理的 token 数、峰值分配内存、GPU 利用率，以及等待下一个批次所花的时间。还应记录损失曲线，以便把更快的实现与原始训练行为进行核对。

这个基线能告诉我们哪种优化最可能奏效。存在空闲间隙的 GPU 可能在等数据；接近满载但注意力吞吐量很低的 GPU 可能会从更好的核函数中受益；而显存不足（OOM）错误需要的是内存层面的改动，而不是调整数据加载器。

![仓库中包含一个直接对比的工作流，用于检查优化后的单 GPU 代码与基线实现之间的差异](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/llm-training-speed/vs-code-compare.png)

在较新的加速器上，**bfloat16 混合精度**通常是一个很好的首个实验。它能降低激活和梯度的内存占用，并让受支持的矩阵乘法使用 tensor core。损失应与全精度基线进行比较，尤其是在更改精度设置或梯度缩放行为时。

注意力实现往往是下一个大的优化机会。PyTorch 的 scaled dot-product attention 可以选择优化后端，包括在硬件、数据类型和张量布局受支持时使用 FlashAttention 风格的核函数。融合优化器以及融合的归一化或激活核函数可以减少模型块其他部分的启动和内存开销。

在模型以稳定形状正确运行之后，`torch.compile` 值得一试。编译有启动开销，而且当形状或控制流发生变化时可能触发重新编译，所以我会测量预热之后的训练区间，而不是最初几步。

输入管线应能跟上优化后的模型。锁页（pinned）主机内存、异步设备传输、合适数量的数据加载器工作进程以及预取（prefetching）都会有所帮助。只有当性能分析表明输入准备或传输处于关键路径上时，这些改动才有意义。

一旦更快的核函数和精度设置就位，批次大小就更容易调优。增大 microbatch 可以提升 GPU 利用率，直到内存或核函数效率不再改善为止。梯度累积可以在不增加每步 microbatch 的情况下提高有效批次大小；而激活检查点（activation checkpointing）通过在反向传播时重算部分前向计算来节省激活内存。

![仓库的优化总结汇集了在分布式化训练循环之前应先测量的一系列单 GPU 改动](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/pytorch-tips/pytorch-tips.webp)

当优化后的运行仍然太慢，或者模型状态无法装入单个设备时，多 GPU 训练才成为合适的选择。这一区别很重要：分布式数据并行（Distributed Data Parallel）会在每块 GPU 上复制模型和优化器，因此每台设备仍需足够的显存来容纳一份完整副本。FSDP 和 ZeRO 类方法会对参数、梯度或优化器状态进行分片，可以解决模型装不下的问题。

分布式化之后，除了总吞吐量，我还应报告扩展效率。两块 GPU 很少能恰好提供两倍的单 GPU 速度，因为梯度同步和通信会消耗时间。单 GPU 基线仍然有用，可用于判断增加的硬件和调试复杂度是否物有所值。
