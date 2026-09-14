---
title: "LLM 中的自注意力"
title_en: "Self-attention in LLMs"
source: https://sebastianraschka.com/faq/docs/self-attention.html
crawled: 2026-09-06
translated: 2026-09-14
---

# LLM 中的自注意力

**自注意力（self-attention）** 让每个 token 通过对同一序列中各 token 的信息做加权求和来形成新的表示。权重取决于当前的 token 表示，因此模型可以针对每个输入、在每一层以不同的方式路由信息。

「自」这个词用来把该机制与交叉注意力（cross-attention）区分开。在自注意力中，查询、键和值都来自同一个输入序列；而交叉注意力从一个序列构造查询，从另一个序列构造键和值，例如文本解码器关注图像特征。

对于包含 \(T\) 个 token 表示的输入矩阵 \(X\)，一个注意力头首先应用三个学习到的线性投影：

\[Q=XW\_q, \qquad K=XW\_k, \qquad V=XW\_v.\]

**查询（query）** 描述一个 token 正在寻找什么。**键（key）** 描述一个 token 如何被匹配，而**值（value）** 包含可以传递给输出的信息。这些描述只是对学习到的向量的直观理解，并不是被单独编程设定的角色。

完整的缩放点积注意力计算为

\[A=\operatorname{softmax}\left(\frac{QK^\mathsf{T}}{\sqrt{d\_k}}+M\right),
\qquad Z=AV.\]

其中 \(d\_k\) 是键维度，\(M\) 是可选的掩码。softmax 沿每一行应用，这使 \(A\) 中一行内的元素非负且总和为 1。第 \(i\) 行描述 token \(i\) 如何混合来自可见 token 位置的值向量。得到的 \(Z\) 的对应行通常被称为**上下文向量（context vector）**。

![自注意力先计算得分，再将其归一化为权重，然后用这些权重形成上下文向量。](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch03_compressed/12.webp)

除以 \(\sqrt{d\_k}\) 很重要，因为点积的幅度往往随向量维度的增大而增大。未缩放的大得分可能把 softmax 推入梯度极小的饱和区。缩放让得分的范围在优化过程中表现更稳定。

注意力矩阵是动态的。假设一个序列中包含单词 "bank"。它的查询可以在一个句子中把权重分配给与金钱相关的词，在另一个句子中分配给 "river"。模型从训练目标中学习这些模式。没有人会把某个头标注为「金融头」，也没有人规定它该连接哪些 token 对。

![单个注意力头把输入投影为查询、键和值，计算 token 到 token 的权重，并把值混合成上下文向量。](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch03_compressed/18.webp)

GPT 和 Llama 等仅解码器 LLM 使用**因果自注意力（causal self-attention）**。其掩码 \(M\) 会把指向后续位置的得分项设为负无穷。经过 softmax 之后，这些项的权重为零。一个 token 可以使用它自身和之前的前缀，但不能读取它本应帮助预测的未来 token。

这个掩码让训练可以并行处理一个序列的所有位置。注意力矩阵的每一行看到的仍是不同的前缀。而生成依旧是串行的，因为直到模型采样出下一个 token 之前，它并不存在。KV 缓存可以避免为旧 token 重新计算键和值，尽管新的查询仍要与缓存中的键交互。

一个注意力头产生一个 token 到 token 的权重矩阵。现代 transformer 通常并行运行多个头。每个头在一个更小的学习子空间中工作，可以产生不同的路由模式。它们的输出被拼接起来并经过一个输出投影。[多头注意力 FAQ](https://sebastianraschka.com/faq/docs/multi-head-attention.html) 涵盖了张量形状、参数量以及键值共享的变体。

位置信息是另一项独立的需求。如果没有依赖位置的信号，无掩码的自注意力对排列是等变的。它比较 token 的内容，却不知道某个匹配的 token 是在另一个之前还是之后，也不知道它们相距多远。因此 LLM 会把注意力与某种机制结合，例如学习式绝对位置嵌入、RoPE 或相对位置偏置。因果掩码通过「可见前缀」的结构提供了方向性，但它并不是一个精确的距离坐标。

自注意力有两个实用的优势。它让每个 token 到每个可见 token 都有一条直接路径，这有助于长程依赖。它还能把所有训练位置的计算表达为可在加速器上高效运行的矩阵运算。循环网络必须通过一连串隐藏状态更新来传播信息，这导致远距离 token 之间的路径更长，训练的并行性也更差。

主要的代价来自 \(T \times T\) 的得分矩阵和权重矩阵。对于全注意力，得分计算随序列长度呈二次增长。FlashAttention 减少了内存访问量，并避免在慢速显存中完整物化整个矩阵，但它计算的是完全相同的精确注意力结果。滑动窗口注意力、稀疏注意力以及循环或线性替代方案则通过改变计算哪些交互来降低长上下文成本。

注意力权重也需要谨慎解读。一个大的权重意味着某个头为该查询把更多特定的值向量路由到了它的输出中，但它并不是「哪个输入 token 导致了模型最终预测」的可靠独立度量。值投影、输出投影、其他头、残差连接、前馈层以及后续的 transformer 块都可能改变或重新定向这些信息。

自注意力之所以是标准 transformer LLM 的核心，是因为它提供了 token 位置之间依赖于内容的通信。完整的模型仍然需要嵌入、位置处理、前馈层、归一化、残差连接和一个输出层。一些较新的混合架构会用循环或状态空间块替换许多注意力层，同时保留一些全注意力层用于精确的 token 检索。

关于掩码的细节，参见[什么是因果注意力，为什么 GPT 风格模型不能看到未来的 token？](https://sebastianraschka.com/faq/docs/causal-attention.html)。最初的缩放点积形式化出现在 [Attention Is All You Need](https://arxiv.org/abs/1706.03762) 中，[从零实现](https://sebastianraschka.com/blog/2023/self-attention-from-scratch.html)则用代码逐步演示了这一计算。
