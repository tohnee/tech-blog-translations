---
title: "为什么许多现代 LLM 使用 RMSNorm 而不是 LayerNorm？"
title_en: "Why do many modern LLMs use RMSNorm instead of LayerNorm?"
source: https://sebastianraschka.com/faq/docs/rmsnorm-vs-layernorm.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 为什么许多现代 LLM 使用 RMSNorm 而不是 LayerNorm？

许多现代 LLM 使用 **RMSNorm**，是因为它保留了**层归一化（LayerNorm）**中激活重缩放的部分，同时省去了均值中心化。这节省了一次沿隐藏维度归约的计算，并且通常还能去掉一个可学习的偏置向量。对完整模型而言，由此带来的加速取决于具体工作负载，但 RMSNorm 已在许多大型 pre-norm transformer 中表现良好。

两种方法都是对每个 token 各自的隐藏特征做归一化。它们不会在序列中的 token 之间或批次中的样本之间计算统计量。对于隐藏向量 \(x \in \mathbb{R}^d\)，LayerNorm 首先计算

\[\mu = \operatorname{mean}(x)\]

然后应用

\[\operatorname{LayerNorm}(x) =
\gamma \odot
\frac{x-\mu}
{\sqrt{\operatorname{mean}((x-\mu)^2)+\epsilon}}
+\beta.\]

在学习到的缩放参数 \(\gamma\) 和平移参数 \(\beta\) 之前，输出近似具有零均值和单位方差。而 RMSNorm 计算的是

\[\operatorname{RMSNorm}(x) =
\gamma \odot
\frac{x}
{\sqrt{\operatorname{mean}(x^2)+\epsilon}}.\]

它把均方根幅度缩放到约等于 1，但输出通常不以零为中心。一个典型的 RMSNorm 层只有一个可学习的缩放参数 \(\gamma\)，而没有可学习的平移参数。对于模型宽度 \(d\)，这意味着 \(d\) 个仿射参数，而不是常见 LayerNorm 形式中的 \(2d\) 个。相对于 LLM 中的权重矩阵而言，这点参数节省微不足道。

![对一个小型线性层输出做 LayerNorm 与 RMSNorm 的数值比较。](https://sebastianraschka.com/images/blog/2025/from-gpt-2-to-gpt-oss/12.webp)

LayerNorm 会对激活做中心化和重缩放，而 RMSNorm 只做重缩放，因此其结果可能保留非零均值。

下表总结了二者的实际区别。

| 属性 | LayerNorm | RMSNorm |
| --- | --- | --- |
| 是否减去特征均值 | 是 | 否 |
| 除以什么 | 标准差 | 均方根幅度 |
| 通常的可学习参数 | 缩放和平移 | 缩放 |
| 仿射变换前，对每个特征加同一常数是否不改变结果 | 是 | 否 |
| 除 \(\epsilon\) 外，对整个向量的正缩放是否不敏感 | 是 | 是 |

平移行为用一个小例子更容易看清。假设 \(x=[1,2,3]\)。LayerNorm 先减去均值，得到 \([-1,0,1]\)，再除以标准差。给每个元素加 10 会得到同样的中心化结果。RMSNorm 则会保留这个正的偏移。在应用 \(\gamma\) 之前，它的归一化向量约为 \([0.463, 0.926, 1.389]\)。加 10 之后，RMS 归一化后的三个值全都会改变。

这种差异有时用不变性来描述。LayerNorm 会消除特征上的整体平移并归一化其尺度；RMSNorm 归一化尺度，但保留了向量均值的信息。RMSNorm 的实证成功表明，在当前仅解码器（decoder-only）的训练方案中，显式的重新中心化往往并不是必需的。

RMSNorm 的计算也略简单一些。LayerNorm 需要均值和均方差偏差，随后还要做减法和除法；RMSNorm 只需要在除法之前计算平方值的均值。融合的 GPU 核函数可以让两者都跑得很快，因此节省的这部分计算不应被理解为端到端训练或推理时间的显著保证性降低。注意力和前馈层的矩阵乘法仍然占计算量的大头。

在混合精度实现中，平方值及其均值通常先在 float32 中计算，再把结果转换回输入的数据类型。这降低了溢出和累积舍入误差的风险。分母中很小的 \(\epsilon\) 防止了除零，也意味着对于非常小的输入，尺度不变性只是近似的。

归一化的类型与归一化的摆放位置是两个相互独立的架构选择。GPT-2 在其注意力和前馈子层之前使用 LayerNorm；Llama 则在类似的 pre-norm 位置使用 RMSNorm。另一些架构把 RMSNorm 放在子层之后，或者在注意力内部为查询和键单独添加归一化。这些摆放决策会改变残差路径，应当与 LayerNorm 与 RMSNorm 之间的选择分开评估。

因此，RMSNorm 的流行只能支持一个适度的结论：它更简单、略微更便宜，并且在成功的 Llama 式训练方案中被证明是稳定的。它并不能证明 RMSNorm 总能产生更好的模型。架构之间的比较通常把归一化与位置嵌入、前馈层、注意力变体、优化器设置以及训练数据放在一起改动。要把质量差异单独归因于 RMSNorm，需要受控的消融实验。

关于更宏观的架构背景，参见[哪些架构变化把 GPT 风格模型变成了 Llama 风格模型？](https://sebastianraschka.com/faq/docs/gpt-style-to-llama-style.html)以及[GPT、Llama、Qwen、Gemma 等架构在宏观上有何不同？](https://sebastianraschka.com/faq/docs/gpt-llama-qwen-gemma-comparison.html)。
