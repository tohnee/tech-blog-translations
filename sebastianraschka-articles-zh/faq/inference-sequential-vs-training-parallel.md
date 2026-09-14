---
title: "为什么推理是串行的，而训练却可以高度并行？"
title_en: "Why is inference sequential while training is much more parallel?"
source: https://sebastianraschka.com/faq/docs/inference-sequential-vs-training-parallel.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 为什么推理是串行的，而训练却可以高度并行？

训练之所以能在一次前向传播中为许多下一 token 预测打分，是因为正确的 token 序列在训练批次中早已可得。而自回归推理并不知道后续内容是什么。它必须先选出下一个 token，将其追加到上下文中，然后才能计算再下一个 token 的分布。

考虑 token 序列 `[A, B, C, D]`。因果语言模型训练可以用 `[A, B, C]` 作为输入，用 `[B, C, D]` 作为错位后的目标。一次模型调用产生三个 logits 向量：第一个与 `B` 比对打分，第二个与 `C` 比对，第三个与 `D` 比对。

![训练序列被错位为输入和目标，因此一次前向传播即可在多个 token 位置上得到损失](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch07_compressed/inputs-targets.webp)

完整的输入张量确实同时存在于加速器上，但每个位置并不能读取整个序列。[因果掩码](https://sebastianraschka.com/faq/docs/causal-attention.html)在注意力内部屏蔽了更靠后的位置。`A` 处的表示不能使用 `B` 或 `C`，而 `C` 处的表示可以使用 `A`、`B` 和 `C`。这些不同位置的矩阵运算仍然一起执行。这种训练设置通常被称为教师强制（teacher forcing），因为每个位置拿到的都是数据集中真实的、位于其前的 token。

并行性还来自批维度。许多序列可以一起处理，模型计算也可以分布到多个加速器上。不过训练并非在所有方向上都并行：Transformer 各层仍依赖更早的层，反向传播要沿计算图进行，而一次优化器步骤要等该批次的完整梯度算完。

生成过程则在新 token 之间存在依赖。如果当前上下文以 `A` 结尾，模型可以产生 `B` 的 logits。但在 `B` 被选定之前，它无法计算 `[A, B]` 之后的正确分布。如果采样选了另一个 token，之后的所有分布都可能改变。

![自回归生成用最终的 logits 选出一个 token，追加该 token，然后执行下一个解码步骤](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch05_compressed/gpt-process.webp)

推理中仍然包含大量可并行的工作。最初的提示处理阶段——通常称为**预填充（prefill）**——在一次带掩码的前向传播中处理所有提示位置。每次前向传播内部都使用并行的矩阵运算，服务器也可以把多个请求组成批次。然而一旦进入解码阶段，同一条序列的新 token 就构成一条有序的链。

**KV 缓存**保存了提示和先前已生成 token 的键与值。这避免了在每个解码步骤重算整个前缀。它降低了每一步的开销，但并不会让 token `t+2` 独立于 token `t+1`。

投机解码（speculative decoding）等方法可以一次性提议或验证多个 token，从而降低实际运行时延。它们绕开了部分硬件低效问题，但被接受的输出仍必须遵循模型的自回归条件分布。这就是为什么以每秒 token 数衡量的训练吞吐量可以很高，而生成一个回复的时延仍受制于连续的解码步骤。
