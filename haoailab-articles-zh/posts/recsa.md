---
title: "RecSA：以对数级成本实现百万 token 外推"
title_en: "RecSA: Million-Token Extrapolation at Logarithmic Cost"
date: 2026-11-17
source: https://haoailab.com/blogs/recsa/
crawled: 2026-11-19
translated: 2026-11-19
---

# RecSA：以对数级成本实现百万 token 外推

> 原文：[RecSA: Million-Token Extrapolation at Logarithmic Cost](https://haoailab.com/blogs/recsa/) · Hao AI Lab @ UCSD

# RecSA：以对数级成本实现百万 token 外推

2026 年 11 月 17 日 · 14 分钟 · Ruitian Wang\*、Xinyu Yang\*、Minshen Zhang\*、Hao Zhang

[![Code](https://img.shields.io/badge/Code--white?style=social&logo=github)](https://github.com/skywong14/RecSA)
[![arXiv](https://img.shields.io/badge/arXiv-2611.07232-white.svg?style=social)](https://arxiv.org/abs/2611.07232)

**TL;DR：** 有两个问题让一个在 32K 长度上训练的模型无法阅读百万 token：稠密注意力会随着上下文增长而变慢；而一旦超过 32K，模型就会遇到训练中从未见过的相对距离。我们提出 **RecSA（Recursive Sparse Attention，递归稀疏注意力）**：它在 KV cache 之上构建一棵树，让每个 query 逐层搜索，因此**选择成本以及每个 query 读取的条目数都按 $O(\log L)$ 增长**。query 未选中的节点仍会作为摘要进入同一个 softmax；并且**每个条目的 RoPE 位置就是它在该层候选中的索引**，这使相对距离保持在训练中见过的范围内。RecSA 从 Qwen3-4B 初始化，仅用 **0.62B token、且全部在 32K 长度上**训练，却在 RULER 上从 131K 到 2M 全面优于所有基线：**1M 长度得分 60.5**，而最强基线（Dense + DCA）为 40.0。在单张 H200 上，524K 长度时 prefill 加速 **3.2×**，解码加速 **3.8×**。**[论文](https://arxiv.org/abs/2611.07232) | [代码](https://github.com/skywong14/RecSA)**

![RecSA 与四个基线的 RULER 得分，以及 RecSA 与稠密注意力的解码延迟，覆盖 32K 到 2M](img/fig1_results.png#center)

图 1. RecSA 与四个基线，均从 Qwen3-4B 出发在 32K 上训练。(a) RULER 得分，13 项任务的平均值；所有稀疏方法与 RecSA 关注的条目数相同。从 131K 起，RecSA 领先所有基线，且差距随长度扩大。(b) 在单张 H200、batch size 为 1 时每 token 的解码延迟，对比同一框架内的稠密 FlashAttention。从 131K 到 524K，RecSA 稳定在约 6 ms，而 Dense 的延迟随上下文增长。空心标记：启用 KV offloading。

## 1. 长上下文为什么难[#](#1-why-long-context-is-hard)

稠密注意力在每个解码步都要读取整个 KV cache。对 Qwen3-4B 而言，在 1M token 时，cache 加权重已经超过单张 H200 的 140 GiB；到 2M 时，仅 cache 就占 275 GiB。如果溢出的部分放在主机内存中，稠密解码一步在 1M 时要 177 ms，2M 时要 2.9 s。像 [MoBA](https://arxiv.org/abs/2502.13189) 和 [DSA](https://arxiv.org/abs/2512.02556) 这样可训练的稀疏注意力只读取 cache 的一部分，但为了选出这部分，它要给前面每一个块或 token 打分，因此每个 query 的选择成本仍是 $O(L)$。

这些方法还需要在目标长度上训练，而随着长度增长，长训练文档会越来越稀缺。一个在 32K 上训练的模型一旦超过 32K 就会失效——此时 query 会遇到它在训练中从未见过的、与 key 之间的距离。像 [YaRN](https://arxiv.org/abs/2309.00071) 和 [DCA](https://arxiv.org/abs/2402.17463) 这样的上下文扩展方法可以推迟这种失效，但无法消除它（图 1a）。

此前的工作只解决了其中一个问题。像 [InfLLM](https://arxiv.org/abs/2402.04617) 这样的方法可以远超训练长度运行，但仍要给每个块打分，所以选择成本是 $O(L)$。像 [HiP](https://arxiv.org/abs/2406.09827) 这样的分层方法把成本降到 $O(\log L)$，却保留每个 key 的原始位置，仍然需要上下文扩展。RecSA 是第一个同时做到这两点的稀疏注意力：每个 query 的选择成本为 $O(\log L)$，并且只在短序列上训练，就能远超训练长度运行。

## 2. 递归稀疏注意力[#](#2-recursive-sparse-attention)

### 2.1 在 KV cache 上建树，逐层搜索[#](#21-a-tree-over-the-kv-cache-searched-level-by-level)

在每个注意力层中，RecSA 为每个 KV head 的 KV cache 构建一棵树，每个 query 从顶层开始向下搜索（图 2）。

[](img/fig2_tree.mp4)

图 2. 每层给自己的候选打分，只选出得分最高的少数几个；被选中节点的子节点成为下一层的候选。每个未选中的节点作为一个子树摘要进入注意力，因此每个 token 恰好被一个条目覆盖，层数按 log L 增长。

* **树。** 每 16 个连续 token 组成上一层的节点，每 16 个节点再组成更上一层的节点，直到顶层最多有 4K 个节点。每个节点保存一个 value（其子节点 value 的均值）和一个 key（来自一个小型可学习 pooler，见 2.3 节）。
* **搜索。** 在顶层，query 选出 256 个节点：包含它自己的那个节点，以及得分最高的 255 个。它们的子节点（最多 4K 个）成为下一层的候选，如此重复直到 token 层。
* **摘要。** 未选中的节点不会被丢弃。每个节点作为概括其子树的单个条目，与精确 token 一起进入同一个 softmax，因此每个 token 恰好被一个条目覆盖。

像 MoBA 这样的块稀疏注意力在固定的两层树上做同样的搜索——block 在 token 之上。随着上下文增长而增加层数，会改变每个 query 需要打分的内容（表 1）。

|  | MoBA | RecSA |
| --- | --- | --- |
| 树中的层数 | 任意长度下均为 2 层 | 最多 64K token 时为 2 层，2M 时为 4 层 |
| 打分的候选 | 每个 block，$O(L)$ | 每层最多 4K 个，总计 $O(\log L)$ |
| 未选中的 block 或节点 | 丢弃 | 作为摘要保留在 softmax 中 |

表 1. 在块稀疏注意力与 RecSA 中，一个 query 所做的操作。

包含 query 自身的节点在每一层都会被选中，因此紧挨在 query 之前的 token 总会被精确读取，RecSA 也不使用 attention sink 或局部窗口。在 2M 长度下，一个 query 关注约 12K 个条目，大约是 32K 时的两倍。

### 2.2 候选局部 RoPE[#](#22-candidate-local-rope)

使用标准 RoPE 时，query 与 key 之间的相对距离就是它们在序列中位置之差。一个在 32K 上训练的模型只见过小于 32K 的距离，但在 2M 长度下，query 距离上下文起点有 2M 个 token。

RecSA 数的是候选，而不是 token。在每一层，每个候选（包括最终成为摘要的节点）都以它在该层候选列表中的索引作为 RoPE 位置，query 则取最后一个索引。候选之间被跳过的序列部分不占位置，因此候选保持原有顺序，只是它们之间的空隙消失了。每层最多有 4K 个候选，所以在任何上下文长度下，query 与任何候选之间的距离都小于 4K（图 3）。当骨干模型在 32K 序列上训练时（第 3 节），最底层已经用 4K 个 token 填满了候选列表，因此训练覆盖了推理时会出现的所有距离。

![在小树上，RoPE、ReRoPE 与候选局部 RoPE 下相对 query 的距离](img/fig3_rope.png#center)

图 3. 相对 query（64 个 token 中的最后一个）的距离。(a) 标准 RoPE 给每个 token 计数，因此距离随上下文增长；[ReRoPE](https://github.com/bojone/rerope) 把窗口之外的每个 token 都放在同一距离上。(b) 在一棵每个节点 4 个子节点、每层选 2 个节点的小树上使用候选局部 RoPE：每层只按顺序给自己的候选编号，因此距离保持在 8 以下。在 RecSA 中，一层最多有 4,096 个候选，所以在任何上下文长度下所有距离都保持在 4,096 以下。

我们把候选局部 RoPE 与一个训练方式相同、但在原始 token 位置上使用标准 RoPE 的变体进行比较（图 4）。在 32K 时，两者得分相差不到一分。超过 32K 后，标准 RoPE 立刻失效。使用 YaRN 时失效来得更晚，但到 524K 时得分同样崩塌。候选局部 RoPE 在 1M 时仍保留了大部分得分。

![候选局部 RoPE、标准 RoPE 以及带 YaRN 的标准 RoPE 的 RULER 得分](img/fig4_rope_ablation.png#center)

图 4. RecSA 与一个训练方式相同但使用标准 RoPE 的变体的 RULER 得分，在 32K 之外分别在有、无 YaRN 的情况下评测。标准 RoPE 在 131K 时跌到 1.0；YaRN 推迟了下跌，但在 524K 和 1M 时得分为 1.9。候选局部 RoPE 在 1M 时保持 60.5。

### 2.3 从稠密注意力中蒸馏 pooler[#](#23-distilling-the-pooler-from-dense-attention)

一个节点的 key 对每个 query 承担两项工作：决定该节点是否被选中；如果没被选中，它就是该节点摘要进入 softmax 时的 key。常用的均值池化会稀释一个「在许多弱匹配中只有一个强匹配」的子树（图 5）。RecSA 的 pooler 从子节点 key 的均值出发，再加上两个可学习项：

* 一项沿一个可学习方向，把 key 拉向得分最高的子节点，拉动幅度由一个可学习门控决定；
* 一个小型 MLP 根据均值和这一拉动量计算修正项并加上去。

两个项都关闭时，pooler 就是普通均值池化。每个注意力层有一个约 25K 参数的 pooler，由其所有 KV head 及其树的所有层共享。

[](img/fig5_pooler.mp4)

图 5. 一个节点与一个 query，该 query 的匹配对象是此节点 16 个子节点之一。均值池化会稀释这一匹配，导致节点未被选中；RecSA 的 pooler 保留了它，于是节点被选中，搜索继续深入其子节点。分数仅作示意。

**蒸馏。** 选择是硬 top-k，因此语言建模损失只能通过摘要传达到 pooler，而无法通过「哪些节点被选中」传达。于是我们从冻结的 Qwen3-4B 中蒸馏 pooler：

* 在每一层，用一个 KL 损失让 RecSA 对候选的打分拟合教师在对应子树上的注意力质量。
* 训练只使用 32K 序列。在顶层以下，候选来自 RecSA 自身的选择，与推理时相同。
* 蒸馏时每层选择 64 个节点而非 256 个，这样即使 32K 序列也有三层，pooler 能学会对已经池化过的 key 再做池化。2M 时出现的第四层复用同一套参数。

**偏移惩罚。** MLP 可能走捷径：如果它给某一层的每个 key 加上同一个向量，候选局部 RoPE 会为每个候选以不同方式旋转该向量，于是这个偏移会带来一个取决于候选在列表中位置、而非其子树的分数。这样 KL 损失可能仅靠这种位置偏置就下降。我们对一层中所有节点共享的偏移施加惩罚，而让节点之间的差异保持自由。没有惩罚时，MLP 几乎没有帮助；有惩罚时，去掉 MLP 会在上下文越长时伤害越大。

## 3. 在 32K 上训练，在 2M 上运行[#](#3-train-at-32k-run-at-2m)

两个训练阶段都只使用 32K 序列。阶段 1 冻结原始模型，蒸馏 pooler（2.3 节）。阶段 2 冻结 pooler，在 RecSA 下用语言建模损失训练整个骨干，每层选择 256 个节点。从 Qwen3-4B 出发，两个阶段共处理 0.62B token 的数据，包括合成检索任务、文档问答、书籍、代码，以及由原始模型生成回答的指令数据。作为基线，我们用相同数据、以与阶段 2 相同的方式训练 Dense、MoBA 和 DSA 骨干，并分别用 YaRN 和 DCA 评测。InfLLM 和 [InfiniteHiP](https://arxiv.org/abs/2502.08910) 无需训练。在每个长度上，每种稀疏方法关注的条目数都与 RecSA 相同。

在 131K 到 2M 的每个长度上，RecSA 在 [RULER](https://arxiv.org/abs/2404.06654) 上得分最高（表 2），其对最强基线的领先从 131K 时约 3 分扩大到 1M 时约 20 分。在 32K 时，它与 Dense 持平。仅靠有界距离并不能解释这一领先：DSA + DCA 同样把每个相对距离保持在训练范围内，token 预算也相同，但在 1M 时它的得分比 RecSA 低约 24 分。

| 方法 | 32K | 131K | 262K | 524K | 1M | 2M |
| --- | --- | --- | --- | --- | --- | --- |
| *token 预算* | *5,888* | *8,192* | *8,704* | *9,728* | *11,575* | *11,990* |
| *占上下文比例* | *18.0* | *6.25* | *3.32* | *1.86* | *1.16* | *0.60* |
| ***无需训练*** |  |  |  |  |  |  |
| InfLLM | 45.0 | 29.3 | 29.2 | 27.4 | 25.7 | 24.2 |
| InfiniteHiP | 79.6 | 63.7 | 57.7 | 49.4 | 36.6 | 34.0 |
| ***在 32K 上训练*** |  |  |  |  |  |  |
| Dense + YaRN | 94.5 | 80.0 | 48.3 | 3.6 | 1.6 | 1.1 |
| Dense + DCA | 94.6 | 78.5 | 68.4 | 58.0 | 40.0 | 27.6 |
| MoBA + YaRN | 81.6 | 31.9 | 5.1 | 0.9 | 1.0 | 0.6 |
| MoBA + DCA | 81.8 | 37.9 | 23.8 | 18.1 | 12.5 | 7.2 |
| DSA + YaRN | **95.3** | 80.5 | 57.1 | 18.8 | 6.0 | 1.4 |
| DSA + DCA | 95.2 | 77.5 | 65.7 | 55.2 | 36.8 | 22.6 |
| **RecSA** | 94.7 | **83.3** | **75.9** | **69.7** | **60.5** | **49.3** |

表 2. RULER 得分，13 项任务的平均值。token 预算：最后一个位置的 query 所关注的条目数，在每个长度上对所有稀疏方法做统一匹配。RecSA 在 131K 到 2M 的每个长度上领先。

在九本 [PG-19](https://arxiv.org/abs/1911.05507) 书籍上，RecSA 的困惑度从 131K 到 1M 几乎保持平坦，而所有基线的困惑度都随长度上升（图 6）。

![PG-19 书籍上从 32K 到 1M 的困惑度](img/fig6_ppl.png#center)

图 6. 九本 PG-19 书籍上的困惑度。从 131K 到 1M，RecSA 保持在 10.9 到 11.1 之间；而在 1M 时，DCA 基线达到 14.6–19.2，Dense + YaRN 达到 211。

在六个短上下文基准（MMLU、ARC-C、GSM8K、IFEval、HumanEval 和 MBPP）上，RecSA 与原版 Qwen3-4B 的差距保持在 2 分以内。这些输入大多短于 4K token，此时 RecSA 退化为稠密注意力，因此差异来自阶段 2 的训练。

## 4. 对数级成本[#](#4-logarithmic-cost)

2.1 节表明，每个 query 的选择成本按 $O(\log L)$ 增长。这里我们检验这对实际耗时意味着什么：单张 H200、batch size 为 1，对比同一框架内的稠密 FlashAttention。

RecSA 的 prefill 在 32K 时略慢（1.6 s 对 1.5 s），从 64K 起更快。在 524K 时，它耗时 80 s，而稠密注意力为 257 s（图 7）。在 1M 和 2M 时，RecSA 把精确 token 放在主机内存中（第 5 节），差距进一步拉大。

![RecSA 与稠密注意力的每 token prefill 时间](img/fig7_prefill.png#center)

图 7. 单张 H200、batch size 为 1 时每 token 的 prefill 时间。在 524K 时，RecSA 比同一框架内的稠密 FlashAttention 快 3.2×。空心标记：启用 KV offloading 的 RecSA；箭头：Dense 的值超出坐标轴范围。

在每个长度上，包括 32K，RecSA 的解码都快于稠密注意力（图 1b）。从 131K 到 524K，RecSA 保持在每 token 约 6 ms，而稠密解码从约 9 ms 增长到 23 ms，因此在 524K 时 RecSA 快 3.8×。在 1M 和 2M 时，RecSA 约需 8 ms 和 11 ms。此时稠密 KV cache 已放不进 GPU 显存，稠密解码慢 20× 以上。第 5 节展示了单个解码步的时间去向。

## 5. Kernel[#](#5-kernels)

我们用 Triton 和 CUDA 实现 RecSA。本节介绍与其他稀疏注意力 kernel 不同的部分，先讲 prefill，再讲解码。

### Prefill[#](#prefill)

一些块稀疏 kernel 允许一组相邻 query 遍历它们所选 block 的并集，每个 block 只加载一次，且其 key 已按 RoPE 旋转好。在候选局部 RoPE 下这种做法失效：同一个 key 在每个 query 的候选列表中位置不同，因此不存在可以预先施加的单一旋转。

我们把旋转拆分到 key 和 query 两侧。把 query 在某层选中的第 $m$ 个节点称为它的槽位 $m$。槽位 $m$ 的子节点 $c$ 在下一层候选列表中的索引就是 $16m + c$。由于 RoPE 分数只取决于两个位置之差，我们可以只按 $c$ 旋转 key（0 到 15），这对每个 query 都相同。query 承担 $16m$ 部分：它从最后一个索引开始，每选中一个节点就向后旋转 16 个位置。这样，一个线程块中 16 个相邻 query 就能共享每个 KV block 并只加载一次（图 8）。在 PG-19 上，底层加载的每个 block 平均可服务 16 个 query 中的 4 到 8 个，具体取决于上下文长度。

![Prefill kernel：一个线程块的 16 个 query 共享每个 KV block](img/fig8_prefill_kernel.png#center)

图 8. Prefill。行是一个线程块中 16 个相邻 query，列是它们所选父节点的并集；数字给出每个父节点对每个 query 的槽位。key 侧的旋转不依赖槽位，因此带框的 16 个子节点 block 只加载一次，被所有选中其父节点的 query 共享。

### 解码[#](#decoding)

* **树更新。** 每一步追加新 token 的 key 和 value，并且只重算每层的最后一个节点，输入是其不超过 16 个子节点。
* **占用率。** 在 batch size 为 1 时，每个 KV head 一个线程块只会占用 H200 132 个 SM 中的 8 个。我们把每层的候选列表拆成 16 段并行打分，再合并各段取出前 256 个。
* **单个 CUDA graph。** 每层最多 4K 个候选，所以每个 kernel 的启动网格都是固定的，全部 36 个注意力层的解码步被捕获为一个 CUDA graph。
* **KV offloading。** 在 1M 和 2M 时，KV cache 放不进 GPU 显存（第 1 节）。RecSA 把精确 token 保存在锁页主机内存中，GPU 上只保留它们之上的各层，这些层占 cache 不到 7%。选择完全在 GPU 上运行。随后一个 gather kernel 只通过 PCIe 复制 256 个被选中的第 1 层节点下的精确 token，在任何上下文长度下每步都低于 600 MiB。空闲的 GPU 显存会缓存输入的一段后缀，gather 读取这些 block 时无需经过 PCIe。

![启用 KV offloading 的一个解码步](img/fig9_decode_kernel.png#center)

图 9. 启用 KV offloading 的一个解码步：(1) 追加新 token；(2) 用 pooler 更新每层的最后一个节点；(3) 分段给每层打分并取前 256 个；(4) 从 GPU cache 或主机内存 gather 选中的精确 token；(5) 对摘要与精确 token 计算一次 softmax。蓝色：被选中；橙色：未选中的候选，它们以摘要形式进入。

从 131K 到 524K，一个解码步保持在约 6 ms，其中一半以上的时间花在注意力之外。在 1M 和 2M 时，新增时间主要来自 gather（图 10）。

![从 32K 到 2M 解码延迟按组件拆分](img/fig10_decode_breakdown.png#center)

图 10. 一个解码步的时间拆解。从 131K 到 524K，该步保持在约 6 ms；在 1M 和 2M 时，新增时间主要来自对选中精确 token 的 gather。

## 结论[#](#conclusion)

RecSA 在 KV cache 上构建一棵树并逐层搜索，未选中节点的摘要与精确 token 共享同一个 softmax。选择成本与每个 query 读取的条目数都按 $O(\log L)$ 增长。候选局部 RoPE 让所有相对距离都保持在训练中见过的范围内，因此 RecSA 对上下文长度没有固有限制。仅在原模型的 32K 训练长度上训练，RecSA 在 RULER 上从 131K 到 2M 全面优于所有基线，并且在 prefill 与解码上从 64K 到 2M 都快于稠密注意力。下一步，我们会把 RecSA 应用到更大的模型上。

详情请见[我们的论文](https://arxiv.org/abs/2611.07232)。包括 kernel、Qwen3 集成、RULER 评测和延迟基准在内的代码位于 [skywong14/RecSA](https://github.com/skywong14/RecSA)。

## 引用[#](#citation)

```
@article{wang2026recsa,
  title   = {Recursive Sparse Attention: Million-Token Length Extrapolation at Logarithmic Cost},
  author  = {Wang, Ruitian and Yang, Xinyu and Zhang, Minshen and Zhang, Hao},
  journal = {arXiv preprint arXiv:2611.07232},
  year    = {2026}
}
```
