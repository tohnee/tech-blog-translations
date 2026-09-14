---
title: "为什么 `bfloat16` 这类混合精度在实践中如此有用？"
title_en: "Why does mixed precision such as `bfloat16` help so much in practice?"
source: https://sebastianraschka.com/faq/docs/mixed-precision-bfloat16.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 为什么 `bfloat16` 这类混合精度在实践中如此有用？

混合精度（mixed precision）可以同时改善内存占用和吞吐量，因为许多神经网络运算并不需要 32 位输入。在原生支持 `bfloat16` 的硬件上，低精度矩阵乘法更快，而且在内存中搬运 16 位张量所需的字节数只有 `float32` 的一半。不过，整个训练任务并不会自动变成两倍速度或只占一半内存，因为部分张量和运算仍会保持 32 位精度。

数值格式解释了 `bfloat16` 为什么广受欢迎。它使用 1 个符号位、8 个指数位和 7 个尾数位。`Float32` 同样使用 8 个指数位，但有 23 个尾数位。标准 `float16` 分配了 10 个尾数位，却只有 5 个指数位。

![Bfloat16 保留了 float32 的 8 个指数位，同时减少了尾数位的数量](https://sebastianraschka.com/images/blog/2023/llm-mixed-precision/bfloat16.webp)

因此，`bfloat16` 的动态范围与 `float32` 大致相同。由于携带的尾数位更少，它的数值排布更稀疏。`Float16` 在其范围内能更精确地表示相邻的数值，但它的指数位更小，发生上溢或下溢的时间要早得多。这就是为什么 `float16` 训练通常需要使用损失缩放（loss scaling），而 `bfloat16` 通常无需梯度缩放器（gradient scaler）即可工作。

**混合**这个词在这里很关键。在 [PyTorch 自动混合精度](https://docs.pytorch.org/docs/stable/amp.html)中，autocast 会为每个符合条件的运算选择数据类型。矩阵乘法和卷积可以用低精度输入运行。归约（reduction）等对数值敏感的运算则可能在 `float32` 中运行。在 TPU 这类加速器上，乘法可以使用 `bfloat16` 输入，而累加使用 `float32`。

一个最小化的 PyTorch 训练步骤如下所示：

```python
optimizer.zero_grad(set_to_none=True)

with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
    logits = model(input_ids)
    loss = loss_fn(logits, targets)

loss.backward()
optimizer.step()
```

前向传播和损失计算位于 autocast 区域内部。反向传播则在该区域退出后运行。与典型的 `float16` AMP 循环不同，这个例子没有使用 `GradScaler`。启用 autocast 时，我也会避免手动调用 `model.bfloat16()` 或转换每一个输入。autocast 的设计意图就是由它来做针对每个运算的数据类型选择。

节省多少内存取决于实际以低精度存储的内容。在计入任何框架开销之前，70 亿参数在 `float32` 下大约需要 28 GB，在 `bfloat16` 下需要 14 GB。只有当这些参数以相应的数据类型存储时，这减半的效果才会成立。基本的 autocast 设置通常让模型参数保持在 `float32`，只针对选定的运算转换操作数。这种设置仍然可以节省可观的激活内存，但不会把参数分配减半。

大模型训练框架提供了多种精度策略。一种策略可以把模型参数保持在 `bfloat16`，同时保留 `float32` 的优化器状态或权重主副本（master copy）。另一种策略则把参数保持在 `float32`，只在 forward 和 backward 计算期间使用 `bfloat16`。梯度也可以根据具体配置采用任一精度。因此，`bf16-mixed` 和 `bf16-true` 这类标签描述的是实质上不同的内存布局。

这一区别对 Adam 很重要。它的两个矩缓冲区（moment buffer）通常以 `float32` 存储，即使模型计算使用的是 `bfloat16`。如果模型参数、权重主副本和优化器状态都保持在 `float32`，那么整体训练内存的缩减就会远小于激活内存的缩减。推理则更简单，因为它没有优化器状态，所以把权重和 KV 缓存以 16 位格式存储往往能带来更直接的内存节省。

![混合精度只是众多实用优化之一，其收益应当在目标硬件上实测](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/pytorch-tips/pytorch-tips.webp)

加速效果同样取决于瓶颈所在。一个以矩阵运算为主的 LLM 通常会在加速器拥有原生 `bfloat16` 内核时受益。更小的张量减少了内存流量，专用矩阵单元则提供更高的低精度吞吐量。缺少原生支持的较旧设备可能会模拟这些运算，或者退回到更慢的内核。而数据加载瓶颈不会因为改变计算数据类型而消失。

更宽的指数范围让 `bfloat16` 更宽容，但它并不能省去数值检查。较低的尾数精度可能会把很小的更新或彼此接近的数值舍入到一起。我会监控损失是否出现 `NaN` 或无穷大，用一个简短的 `float32` 基线来对比验证指标，并检查 autocast 处理不好的任何自定义运算。

在实践中，当硬件支持时，`bfloat16` autocast 是很好的第一个实验。使用与 `float32` 基线相同的批大小，记录峰值内存和每秒 token 数。如果运行稳定，省下的内存可以用于更大的 microbatch、更长的上下文或更大的模型。[单 GPU 优化清单](https://sebastianraschka.com/faq/docs/first-optimizations-before-multi-gpu.html)把这项精度调整放在了训练改进的更完整顺序中。
