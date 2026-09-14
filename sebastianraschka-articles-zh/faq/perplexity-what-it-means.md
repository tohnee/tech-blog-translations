---
title: "什么是困惑度，它究竟能告诉我们关于 LLM 的什么信息？"
title_en: "What is perplexity, and what does it actually tell us about an LLM?"
source: https://sebastianraschka.com/faq/docs/perplexity-what-it-means.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 什么是困惑度，它究竟能告诉我们关于 LLM 的什么信息？

**困惑度（perplexity）**衡量语言模型在特定数据集上预测实际出现的下一个 token 的好坏程度。它是平均交叉熵损失的指数。困惑度越低，说明模型分配给实际出现 token 的概率越高。

对于有效的目标位置 (\mathcal{I})，平均下一 token 损失为

[
\mathcal{L}
= -\frac{1}{N}
\sum\_{i \in \mathcal{I}}
\log p\_\theta(x\_i \mid x\_{<i}),
]

其中 (N) 是纳入计算的 token 数量。当对数取自然对数时，困惑度为

[
\operatorname{PPL} = \exp(\mathcal{L}).
]

若使用以 2 为底的对数，损失以"每 token 比特数"计量，困惑度为 (2^\mathcal{L})。只要对数与指数运算使用相同的底数，困惑度的数值就不会改变。

同一个量也可以写成"分配给实际出现 token 的概率倒数的几何平均数"：

[
\operatorname{PPL}
= \left(
\prod\_{i \in \mathcal{I}}
\frac{1}{p\_\theta(x\_i \mid x\_{<i})}
\right)^{1/N}.
]

这一形式给了困惑度一个有用的数值解释。如果模型对每个正确的下一个 token 都分配 0.25 的概率，那么平均损失为 (-\log(0.25) = \log(4))，困惑度就是 4。完美的预测器的困惑度为 1。在 (V) 个 token 的词表上做均匀预测的模型，其困惑度为 (V)。困惑度本身既不是概率，也不是百分比。

"有效选择数"这个说法有时被用来描述这种解释，但它应当只被当作一种直觉。困惑度为 4 并不意味着每个位置上恰好有四个等概率的候选。真实的 token 分布在不同位置之间差异很大。

![Perplexity exponentiates the same average cross-entropy loss used for next-token training.](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch05_compressed/cross-entropy.webp)

困惑度最适合用于评估设置保持固定的比较场景。例如，它可以帮助回答：更晚的训练检查点是否更好地预测了留出语料；在相同训练配方下，某个架构改动是否改进了语言建模；训练是否已开始过拟合。

留出数据集很重要。训练困惑度可以随着模型记忆训练样本而持续下降。验证困惑度衡量的是模型对所选验证分布中未见文本的泛化能力，因此通常是更有参考价值的数字。在新闻文章上困惑度低，并不能保证在源代码、医学文本或对话数据上也低。

![Training and validation loss curves show whether token prediction improves on held-out data or only on the training set.](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch05_compressed/train-steps.webp)

此外，若干评估细节也必须一致：

- **分词器（tokenizer）。** 不同的分词器会把同一段文本切分成不同的目标序列。来自两个分词器的 token 级困惑度通常不能直接比较。
- **语料与预处理。** 文档边界、归一化方式、文本结束标记以及纳入哪些文本，都会影响结果。
- **上下文策略。** 窗口长度、滑动步长，以及上下文是否在文档或分块边界处重置，都会改变模型可利用的前文数量。
- **损失掩码。** 填充（padding）位置和任何有意排除的提示词位置，都不应计入总损失或 token 计数。
- **模型模式。** 应当关闭 dropout，并且困惑度应当从模型原始的下一 token 概率出发计算，不经过采样、top-k 过滤或温度调整。

当分词器不同时，每字节比特数或每字符比特数可以提供更可比的归一化方式，但原始文本编码和预处理仍须保持一致。对于滑动窗口评估，即使重叠窗口提供了额外的前文，每个目标 token 也只应被计数一次。

[下一 token 预测 FAQ](https://sebastianraschka.com/faq/docs/next-token-prediction.html)解释了单个 token 损失是如何计算的。困惑度只是通过指数运算，把它们的平均值重新放回一个类似概率的尺度上。由于指数函数是单调的，在其他一切不变的情况下，比较困惑度等价于比较平均交叉熵。

困惑度并不直接衡量事实准确性、推理能力、指令遵循、安全性，或完整生成回复的质量。一个模型可能对常见文本模式赋予很高的似然，却仍给出错误的答案。反过来，经过指令微调的模型可以在不改善某个无关预训练语料上困惑度的情况下，变得更适合对话。

困惑度还会掩盖平均值内部的差异。少数几个领域或 token 类型可能损失很高，而总体数字看起来还不错。逐 token 损失和分领域的独立结果有助于揭示这类情况。排查指南[为什么模型训练损失很低，生成的文本却很差？](https://sebastianraschka.com/faq/docs/low-loss-but-poor-text.html)讨论了 token 级优化与生成质量之间的相应落差。

因此，我会把困惑度当作一种受控的语言建模指标来使用。它非常适合用于训练曲线和相同设置下的消融实验。更广泛的模型选择则应将它与面向任务的检查和输出评估结合起来，如[为什么评估 LLM 输出很困难？](https://sebastianraschka.com/faq/docs/evaluating-llm-outputs.html)所述。
