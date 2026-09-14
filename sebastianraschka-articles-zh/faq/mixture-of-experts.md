---
title: "专家混合（MoE）与稠密 LLM 的对比"
title_en: "Mixture-of-Experts (MoE) vs. Dense LLMs"
source: https://sebastianraschka.com/faq/docs/mixture-of-experts.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 专家混合（MoE）与稠密 LLM 的对比

**专家混合（MoE）** LLM 把一些稠密的前馈块替换为若干个备选的前馈网络，这些网络称为专家（expert）。一个可学习的路由器（router）为每个 token 选择其中一小部分专家。而稠密 LLM 则让每个 token 都经过同一个前馈块。

在这两种架构中，注意力通常都保持稠密。MoE 的改动通常施加在 transformer 块的前馈部分，因为该部分占了模型参数的很大份额。

![稠密前馈块对每个 token 使用同一个网络，而 MoE 层加入了一个路由器和若干个专家网络](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/moe-memory/1.webp)

对于一个 token 表示 \(x\)，路由器会为每个专家产生一个得分。它保留得分最高的 \(k\) 个专家（top \(k\)），并用路由权重组合它们的输出。一个简化后的表达式为

\[\operatorname{MoE}(x) = \sum\_{i \in \operatorname{TopK}(x)} g\_i(x) E\_i(x),\]

其中 \(E\_i\) 是第 \(i\) 个专家，\(g\_i(x)\) 是它的路由器权重。路由通常按 token 逐个进行，因此同一句话中的两个 token 可以使用不同的专家。

这就产生了两种有用的参数量。**总参数量（total parameters）**包括检查点中存储的所有专家。**活跃参数量（active parameters）**包括被选中的专家以及单个 token 所用到的模型共享部分。诸如 `235B-A22B` 这样的模型命名就利用了这一区别：第一个数字描述近似总参数量，第二个数字描述近似活跃参数量。

做对比时需要小心一些。假设一个稠密前馈块有 \(P\) 个参数。一个含有八个同等规模专家的 MoE 层会存储约 \(8P\) 个专家参数。如果它的路由器选择两个专家，那么对于单个 token，约 \(2P\) 个专家参数参与计算。这远少于激活全部 \(8P\) 个参数，但相比原来 \(P\) 个参数的稠密块，它也用到了更多专家计算量。MoE 在提升容量的同时，并没有让单 token 计算量按存储参数量同样的倍数增长。

![随着存储专家数量的增长，总专家参数量的增长可以远快于单个 token 被选中的参数量](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/moe-memory/2.webp)

路由器和专家在训练期间共同学习。被路由到某个专家的 token 为该专家提供训练信号。如果路由器把大多数 token 都发给少数几个专家，这些专家就会过载，而其他专家几乎得不到有用的训练。因此 MoE 系统会使用负载均衡机制，例如辅助目标（auxiliary objective）、路由偏置或专家容量约束。具体方法因架构而异。

负载均衡还是一个系统工程问题。路由完成之后，分配给同一个专家的 token 会被组织成批次（batch），以便专家高效处理。当专家分布在多个加速器上时，token 表示可能需要移动到拥有所选专家的设备上，然后再返回到它们原来的序列位置。这种全互联（all-to-all）通信可能占据训练和服务时间的很大一部分。

这就是为什么活跃参数量只是运行时开销的一个近似。注意力、嵌入、归一化层和输出头仍然要运行。路由会额外带来打分、排序、token 搬移和内存访问的开销。一个拥有 220 亿活跃参数的模型，其延迟不一定与一个 220 亿参数的稠密模型相同。

完整的专家检查点也必须存储在某处。单张 GPU 需要容纳分配给它的全部权重，否则就必须把专家分片（shard）到多个设备上。相对于总参数量，稀疏激活降低了每个 token 的专家算术量。但检查点仍然包含每一个专家，而且注意力的 KV 缓存基本不受影响，因为 MoE 改动的是前馈路径。

一些架构还会加入一个**共享专家（shared expert）**，它与被路由的专家并行，对每个 token 都运行。共享专家可以处理常见模式，从而给被路由的专家留出更多专门化的空间。共享专家是可选的，一旦存在，活跃参数量就必须把这条路径包括进去。

![共享专家始终处于激活状态，而路由器为每个 token 额外选择若干专家](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/moe-memory/3.webp)

专家的专门化也没有名字暗示的那么干净利落。并不一定会有一个专家变成纯粹的"数学专家"，另一个专门处理语法。路由模式可能相互重叠，而且专门化程度会因层、token 位置或训练阶段而异。

在实践中，当训练和部署系统能够分发专家权重并高效路由大批 token 时，MoE 很有吸引力。稠密模型在少量设备上训练、微调和部署都更简单。当额外的总容量确有价值、且硬件栈能够处理稀疏路由而不至于让理论上的计算优势被通信和低利用率抵消时，MoE 才更有用。

若需一个可视化的架构示例，可参见[专家混合架构图鉴页](https://sebastianraschka.com/llm-architecture-gallery/moe/)。相关 FAQ [为什么 MoE 模型参数量巨大但每个 token 的活跃计算量更低？](https://sebastianraschka.com/faq/docs/why-moe-huge-params-lower-active-compute.html)侧重于解读已公布的模型规模。
