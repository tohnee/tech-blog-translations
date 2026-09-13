---
title: "循环 Transformer（Looped Transformer）"
title_en: "Looped Transformer"
source: https://sebastianraschka.com/llm-architecture-gallery/looped-depth-sharing/
crawled: 2026-09-06
translated: 2026-09-06
---

# 循环 Transformer（Looped Transformer）

> 原文：[Looped Transformer](https://sebastianraschka.com/llm-architecture-gallery/looped-depth-sharing/)

循环 Transformer（looped transformer）的核心思想是让同一组层（即同一个 transformer 块）被多次应用。这种方法通常也被称为循环深度（recurrent depth）或循环深度共享（looped depth sharing）。从某种意义上说，它就像一个常规 transformer：上一轮传递得到的隐藏状态成为下一轮的输入，只是其中一些层被重复使用。

我们可以把它视为逐深度权重绑定（depth-wise weight tying）的一种形式。例如，如果一个 transformer 有 `L` 个不同的块和 `T` 轮传递，那么：

```python
effective block applications = L × T
```

在常规 transformer 中，`T=1`；而在循环 transformer 中，`T>1`。

由于隐藏状态要经过更多层，激活内存和 KV 缓存内存也会随轮数的增加而增长（取决于具体实现）。因此从某种意义上说，循环深度改变了参数量与计算量之间的权衡。

这一基本思想可以追溯到 2018 年的 [Universal Transformers 论文](https://arxiv.org/abs/1807.03819)，研究者在其中把循环变换与逐 token 位置的自适应停机（adaptive halting）结合在一起。后来 ByteDance 的 [Ouro 论文](https://arxiv.org/abs/2510.25741)则明确把 LoopLM 归入这一工作脉络。现代循环 Transformer 复用的仍是同样的逐深度权重共享思路，只是采用了不同的循环和退出机制。

例如，2025 年有两篇论文接续了 Universal Transformer 的工作。首先是[循环深度论文](https://arxiv.org/abs/2502.05171)（Recurrent Depth），它探索了通过把一个循环块展开到更深的层数来扩展测试时计算；随后，[Mixture-of-Recursions 论文](https://arxiv.org/abs/2507.10524)加入了 token 级路由，使不同的 token 位置可以获得不同的递归深度。前文提到的 Ouro 于 2025 年 10 月问世；而另一个模型 Nanbeige 4.2（2026）则简化了循环 Transformer 的思路：直接重复同一个 22 层堆叠，不使用专门的路由或停机策略。

[架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
[Universal Transformers 论文](https://arxiv.org/abs/1807.03819)
[Ouro 论文](https://arxiv.org/abs/2510.25741)

![Nanbeige 4.2 架构：共享的 22 层 transformer 堆叠外带一个循环](https://sebastianraschka.com/llm-architecture-gallery/images/architectures/nanbeige-4-2-3b.webp)

**图 1.** Nanbeige 4.2 让隐藏状态两次通过同一个 22 层堆叠。绿色的返回路径表示
第二次经过共享权重。

共享内容

transformer 层的权重在各轮传递之间复用

有效深度

Nanbeige 4.2 达到 44 次块应用；Ouro-Thinking 2.6B 在四轮传递下达到 192 次

示例架构

[Nanbeige 4.2 3B](https://sebastianraschka.com/llm-architecture-gallery/#card-nanbeige-4-2-3b) ·
[Ouro-Thinking 2.6B](https://sebastianraschka.com/llm-architecture-gallery/#card-ouro-thinking-2-6b)

## Nanbeige 4.2 的两次固定传递

上图所示的 [Nanbeige 4.2 3B](https://sebastianraschka.com/llm-architecture-gallery/#card-nanbeige-4-2-3b) 是画廊中较新但更简单的循环 Transformer 示例。Nanbeige 让隐藏状态两次通过同一个 22 层 transformer 堆叠。这相当于用 22 个不同的层实现 44 次块应用，执行路径固定为两轮。

[Nanbeige 4.2 技术报告](https://huggingface.co/Nanbeige/Nanbeige4.2-3B/blob/main/Nanbeige42_report.pdf)第 2.1 节指出，两轮传递带来了最佳权衡，保留了标准架构约 75% 的 token 效率。研究者尝试过增加更多轮数，但发现在建模性能（或训练损失）上几乎没有收益，反而让训练更慢、更昂贵。

## Ouro 的四轮传递与可学习退出门

[Ouro 论文](https://arxiv.org/abs/2510.25741)在同样的基本机制上做了扩展：最大循环深度为 4，并引入一个可学习的退出门，这使它更接近最初的 Universal Transformers 思想。

具体来说，画廊收录的 [Ouro-Thinking 2.6B](https://sebastianraschka.com/llm-architecture-gallery/#card-ouro-thinking-2-6b) 示例有 48 个不同的 transformer 块。其发布配置将 `total_ut_steps` 设为 4，即一次初始传递加上三次对共享堆叠的重复，对应 192 次有效的 transformer 块应用。

其训练目标会在每轮传递后评估中间表示，并学习一个关于从第 1 到第 4 步退出的概率分布。在推理时，论文的 Q-exit 规则选择累计退出概率首次越过给定阈值的步骤。阈值越低越倾向于提前退出；阈值为 1 时则会用满全部四轮。

有一个实现细节值得与论文中的提前退出描述区分开。截至撰写本文时，发布的 [Hugging Face 实现](https://huggingface.co/ByteDance/Ouro-2.6B-Thinking/blob/main/modeling_ouro.py)尚未实现这一退出门控：它先计算所有配置的轮次，保存中间隐藏状态和门分数，然后再从中选择一个表示或构成加权输出。在默认的 `total_ut_steps: 4` 和 `early_exit_threshold: 1.0` 下，四轮都会被计算，并选用第四个表示。减小 `total_ut_steps` 会降低实际执行的深度；而只改阈值目前只会改变由哪一个已计算好的表示来提供输出。

[模型卡](https://huggingface.co/ByteDance/Ouro-2.6B-Thinking)的架构表中列出的是 24 层。然而，发布的 [`config.json`](https://huggingface.co/ByteDance/Ouro-2.6B-Thinking/blob/main/config.json) 将 `num_hidden_layers` 设为 48，实现中也实例化了这一 48 层堆叠。因此画廊对这一四轮配置采用 48 个不同层和 192 次块应用的数据。

![Ouro-Thinking 2.6B 架构：共享的 48 层 transformer 堆叠四次传递，并带有一个可学习退出门](https://sebastianraschka.com/llm-architecture-gallery/images/architectures/ouro-2-6b.webp)

**图 2.** 在发布配置中，Ouro-Thinking 2.6B 将其 48 层堆叠复用四次。绿色返回路径表示三次重复传递，门则对每轮传递产生的表示进行打分。

## 固定循环与 token 级路由

画廊中的示例都在整个堆叠层面施加循环。Nanbeige 对每个 token 都执行两轮传递；Ouro 对第 1 到第 4 轮产生的表示训练一个退出分布，尽管其发布实现会先算完所有配置的轮次再选择输出。

[Mixture-of-Recursions](https://arxiv.org/abs/2507.10524) 采用更细粒度的方式。它的路由器为单个 token 位置分配不同的递归深度：仍然活跃的 token 继续进入更深的递归，其他 token 则跳过这些计算。这也让模型可以把更深递归中的注意力计算和 KV 缓存限制在活跃 token 上。因此，潜在的计算与内存节省是以额外的路由和缓存管理复杂度为代价的。

关于这些内容，我在下方链接的视频中有更多讲解。

## 循环 Transformer 与 KV 缓存

共享 transformer 权重并不意味着只共享一个 KV 缓存。Ouro 的发布实现为每一个"层 × 轮次"组合分配独立的缓存索引。在四轮传递、48 层、16 个 KV 头、头维度为 128 的设置下，这相当于 bf16 格式下的 `1.5 MiB/token`。完整计算见 [KV 缓存计算页面](https://sebastianraschka.com/llm-architecture-gallery/kv-cache-calculations/)。

Ouro 论文报告称，提示词预填充（prefill）阶段需要保留全部四个缓存。而在自回归解码时，在报告的实验中只复用最后一轮的缓存可以把内存减少 4 倍，且性能损失很小。这种缓存复用优化是一种额外的推理策略，它与共享 transformer 权重是两回事，也并非发布版 Hugging Face 实现的默认行为。

关于循环深度和循环 Transformer 的更长讲解，请看我下面的视频。

参考资料

[Dehghani et al. (2018), *Universal Transformers*](https://arxiv.org/abs/1807.03819)
[Geiping et al. (2025), *Scaling up Test-Time Compute with Latent Reasoning*](https://arxiv.org/abs/2502.05171)
[Bae et al. (2025), *Mixture-of-Recursions*](https://arxiv.org/abs/2507.10524)
[Zhu et al. (2025), *Scaling Latent Reasoning via Looped Language Models*](https://arxiv.org/abs/2510.25741)
[Nanbeige 4.2 技术报告](https://huggingface.co/Nanbeige/Nanbeige4.2-3B/blob/main/Nanbeige42_report.pdf)
[Nanbeige 4.2 配置](https://huggingface.co/Nanbeige/Nanbeige4.2-3B/blob/main/config.json)
[Ouro-2.6B-Thinking 模型卡](https://huggingface.co/ByteDance/Ouro-2.6B-Thinking)
[Ouro-2.6B-Thinking 配置](https://huggingface.co/ByteDance/Ouro-2.6B-Thinking/blob/main/config.json)
[Ouro-2.6B-Thinking 实现](https://huggingface.co/ByteDance/Ouro-2.6B-Thinking/blob/main/modeling_ouro.py)
[KV 缓存 / token 画廊计算](https://sebastianraschka.com/llm-architecture-gallery/kv-cache-calculations/)

[返回架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
