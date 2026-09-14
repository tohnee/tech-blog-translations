---
title: "有限硬件上 LLM 的训练与推理瓶颈"
title_en: "LLM Training and Inference Bottlenecks on Limited Hardware"
source: https://sebastianraschka.com/faq/docs/llm-limited-hardware-bottlenecks.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 有限硬件上 LLM 的训练与推理瓶颈

起限制作用的资源取决于具体工作负载。推理时模型权重或许放得下，但当上下文或批次增大时内存可能耗尽。全量微调即使在短上下文下也可能失败，因为梯度和优化器状态会超出可用内存。而一次运行也可能明明放得下却依然很慢，因为加速器在等待数据，或张量正在经由一条狭窄的内存通路搬运。

**检查点与权重内存**

原始权重需求大约等于参数量乘以每个参数的字节数。一个 70 亿参数模型在计入临时缓冲区和框架开销之前，bf16 权重就需要约 14 GB。量化可以减少这份存储，前提是硬件针对所选格式有高效的核（kernel）。

加载本身也有峰值。朴素的实现可能会先构建模型，再加载一个独立的状态字典，短时间内会在主机内存中保留两份副本。流式分片加载、内存映射或在 meta 设备上初始化都可以避免这一尖峰。

![内存高效加载减少了检查点实例化期间产生的临时 RAM 和 VRAM 副本](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/memory-efficient-loading/memory-efficient-loading.webp)

**训练状态内存**

全量微调要为每个可训练参数保存梯度和优化器状态。Adam 通常保留两个 32 位的矩（moment）缓冲区，某些混合精度设置还会额外保留主权重（master weights）。[全量微调对比](https://sebastianraschka.com/faq/docs/full-finetuning-vs-lora-cost.html)给出了一个具体的 7B 示例。LoRA 可以减少需要训练的梯度和优化器状态，而 QLoRA 还能进一步压缩冻结的基座权重。

激活值是另一项独立开销。它会随微批次（microbatch）大小、序列长度、模型宽度和层数增长，因为反向传播所需的张量必须被保留下来。激活检查点（activation checkpointing）通过重新计算选定的前向操作来节省内存。梯度累积可以增大有效批次大小，但并不能减少单个微批次所需的内存。

**推理内存与延迟**

自回归推理需要模型权重，外加每个活跃序列各自的 KV 缓存。缓存内存随保留的 token 数、产生缓存的层数、KV 头数和精度而增长。[长上下文 FAQ](https://sebastianraschka.com/faq/docs/kv-cache-long-context-bottleneck.html)展示了 Qwen3 8B 在单序列 32,768 个 token 时会达到约 4.5 GiB 的逻辑 bf16 缓存。

提示词预填充（prefill）与逐 token 解码的性能特征也不同。预填充会一次处理很多位置，可能偏计算密集。解码每序列每次只处理一个新位置，并反复读取权重和缓存状态，因此内存带宽和批处理往往决定吞吐量。CPU 或磁盘卸载（offload）或许能让模型放得下，但经由 PCIe 或存储的传输可能让它慢得多。

**核与输入流水线的利用率**

GPU 利用率低且能看到明显的空闲间隙，通常指向数据加载、主机到设备的传输、同步或过小的工作负载。利用率高但注意力很慢，则说明是计算或核瓶颈。在受支持的硬件上，bf16、融合算子、缩放点积注意力和 FlashAttention 风格的核可以改善速度或内存占用。`torch.compile` 对稳定的工作负载有帮助，但编译时间、重编译和额外内存都应当实测。

![PyTorch 优化笔记汇总了精度、注意力、编译、优化器和数据管线方面的改动，这些改动都应基于同一基线做基准测试](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/pytorch-tips/pytorch-tips.webp)

如果是我来诊断有限硬件，会按这个顺序进行。先记录失败的阶段、设备和主机内存峰值、每秒 token 数以及加速器利用率。然后缩减一个负载维度，比如模型规模、上下文长度或微批次大小。接着测试一种合适的精度和针对该阶段的内存技术。只有当运行稳定之后，我才会加入优化核、卸载或多设备。[单 GPU 优化 FAQ](https://sebastianraschka.com/faq/docs/first-optimizations-before-multi-gpu.html)给出了更详细的测量流程。

对症才能下药。FlashAttention 解决不了因加载重复权重副本导致的内存不足（OOM）错误。LoRA 也无法应对推理时庞大的 KV 缓存。当设备缺少优化过的量化核时，量化或许能缓解容量压力，却带不来速度提升。
