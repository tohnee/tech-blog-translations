---
title: "LLM 预训练的输入-目标训练样本是如何构造的？"
title_en: "How are input-target training examples constructed for LLM pretraining?"
source: https://sebastianraschka.com/faq/docs/input-target-pretraining-examples.html
crawled: 2026-09-06
translated: 2026-09-14
---

# LLM 预训练的输入-目标训练样本是如何构造的？

LLM 预训练样本直接来自分词后的文本。对于训练序列长度 `L`，数据加载器首先取 `L+1` 个连续的 token ID。前 `L` 个 token 作为模型输入，后 `L` 个 token 作为目标。

对于一个五 token 的片段，切分方式如下：

`tokens = [t0, t1, t2, t3, t4]`

`input = [t0, t1, t2, t3]`

`target = [t1, t2, t3, t4]`

因此，每个数组位置上的目标就是相应输入位置后面的那个 token。上下文长度为 256 时，需要 257 个源 token 才能构造 256 个输入和 256 个下一 token 目标。

![一条分词后的序列错开一个位置，形成对齐的输入和目标数组](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch07_compressed/inputs-targets.webp)

目标张量供损失函数使用。它并不作为单独的答案追加到模型输入后面。模型处理输入数组，并在每个位置返回一个覆盖整个词表的 logits 向量。[因果掩码](https://sebastianraschka.com/faq/docs/causal-attention.html)阻止位置 `j` 读取更靠后的输入位置，交叉熵则将该位置的 logits 与 `target[j]` 比较。这样一条序列就产生了 `L` 个监督信号。

下一个决定是如何在 token 流上移动。**步长（stride）**给出了相邻起始位置之间的距离。当 `L=4` 且步长为 4 时，相邻样本互不重叠。步长为 2 则会复用前一样本的部分上下文：

`example 1 source = [t0, t1, t2, t3, t4]`

`example 2 source = [t2, t3, t4, t5, t6]`

第 2 章的数据加载器使用的正是这种滑动窗口设置，因为它使上下文长度与重叠之间的关系一目了然。

![滑动窗口可以按完整上下文长度前进，也可以用更小的步长生成重叠的样本](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch02_compressed/13.webp)

重叠能让一个 token 获得更多周边上下文，但也会重复训练目标并增加计算量。大型预训练流水线通常把分词后的文档打包成基本不重叠的定长序列，以获得更好的数据效率。当多个文档共享一条打包后的序列时，可以用文本结束（end-of-text）token 标记文档边界。

结尾的短片段也需要一个处理策略。流水线可以丢弃它们、把它们与另一篇文档拼接，或者填充到长度 `L`。如果使用填充，相应的目标位置应当从损失中排除。否则，模型会把容量浪费在学习预测人为的填充 token 上。

构造完成的样本被堆叠成形状为 `B x L` 的输入张量和目标张量，其中 `B` 是批大小。对于大小为 `V` 的词表，模型输出的形状为 `B x L x V`，损失函数则在批次内聚合所有有效的下一 token 预测。

![一个小批次堆叠多条定长 token 序列，使它们的下一 token 损失可以一起计算](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch05_compressed/batching.webp)

这种构造方式被称为自监督（self-supervised），因为标签来自文本中本来就连着的后续内容。人类标注者不必为每个 token 位置创建目标。
