---
title: "GPT 风格模型的主要构建模块有哪些？"
title_en: "What are the main building blocks of a GPT-style model?"
source: https://sebastianraschka.com/faq/docs/gpt-style-model-building-blocks.html
crawled: 2026-09-06
translated: 2026-09-14
---

# GPT 风格模型的主要构建模块有哪些？

> 原文：[What are the main building blocks of a GPT-style model?](https://sebastianraschka.com/faq/docs/gpt-style-model-building-blocks.html) · Sebastian Raschka's FAQ

一个 GPT 风格模型包含输入嵌入阶段、一叠解码器块（decoder block），以及一个为下一个 token 打分的输出层。分词器在模型之前运行，它把文本转换成 token ID 并定义词表，但通常被视为预处理步骤，而不是神经网络的一层。

假设一个批次包含 `B` 个长度为 `T` 的 token ID 序列，模型宽度为 `d`。token 嵌入表把每个 ID 映射为一个可学习的向量，得到形状为 `B x T x d` 的张量。仓库中的 GPT-2 风格实现为每个 token 向量加上一个可学习的位置嵌入。更新的模型则可能通过 RoPE 在注意力内部提供[位置信息](https://sebastianraschka.com/faq/docs/positional-information-transformer.html)。

![GPT 风格模型将分词后的文本映射为嵌入，用重复的 transformer 块进行处理，再将最终表示投影为词表 logit](https://sebastianraschka.com/images/blog/2024/building-a-gpt-style-llm-classifier/image2.png)

重复堆叠的 transformer 块承担了绝大部分工作。在仓库采用的预归一化（pre-normalization）设计中，它的两次更新可以概括为：

`x = x + attention(norm(x))`

`x = x + feed_forward(norm(x))`

注意力子层在各个 token 位置之间混合信息。它的[因果掩码](https://sebastianraschka.com/faq/docs/causal-attention.html)允许位置 `t` 使用位置 `0` 到 `t` 的信息，同时屏蔽更靠后的 token。多头注意力并行执行多个这样的混合，让不同的头可以关注不同的 token 关系。

前馈子层的工作方式不同。它对每个位置独立地施加同一个小型神经网络。在 GPT-2 风格的块中，这个网络先扩展隐藏维度，施加 GELU 之类的非线性激活，再把结果投影回宽度 `d`。注意力负责跨位置通信，而前馈层负责变换每个位置上存储的特征。

归一化和残差连接是这两次更新共有的部分。归一化控制进入每个子层的输入的尺度；残差加法为已有表示保留一条直接通路，使深层堆叠更容易优化。张量穿过所有 transformer 块时始终保持 `B x T x d` 的形状。

![每个 transformer 块包含因果多头注意力和一个逐位置的前馈网络，两个子层周围都有归一化和残差路径](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch04_compressed/03.webp)

在最后一个块之后，一层最终的归一化为输出头准备好隐藏状态。这个线性投影把每个 `d` 维向量映射为 `V` 个分数，其中 `V` 是词表大小，结果形状为 `B x T x V`。这些原始分数就是 logit。有些实现把输出投影的权重与 token 嵌入表绑定（weight tying），另一些则学习一个独立的矩阵。

训练时，每个位置的 logit 都通过交叉熵损失与下一个 token 进行比较。生成时，只需要最后可用位置的 logit 来选择下一个 token；新 token 被追加到序列末尾，然后重复这一过程。

GPT 之所以被称为 **decoder-only（仅解码器）**，是因为这个堆叠使用因果自注意力，没有独立的编码器，也没有编码器-解码器之间的交叉注意力模块。现代 LLM 可能用 RMSNorm 替代 LayerNorm、用 RoPE 替代可学习位置嵌入、或用 GQA 替代标准多头注意力。这些改动都保留了从 token ID 到上下文相关表示、再到词表 logit 的同一条总体路径。
