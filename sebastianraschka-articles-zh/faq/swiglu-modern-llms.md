---
title: "现代 LLM 中的 SwiGLU"
title_en: "SwiGLU in modern LLMs"
source: https://sebastianraschka.com/faq/docs/swiglu-modern-llms.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 现代 LLM 中的 SwiGLU

**SwiGLU** 是一个门控前馈层。它对同一个 token 表示计算两个投影，对其中一个投影施加 SiLU 激活，把两条路径逐元素相乘，再把结果投影回模型宽度。

这与单独使用 SiLU 不同。**SiLU**，又称 Swish，是如下激活函数

\[\operatorname{SiLU}(z)=z\,\sigma(z).\]

**SwiGLU** 则是围绕该激活构建的完整三投影块。一种常见的表述是

\[\operatorname{SwiGLU}(x)
= W\_{\text{down}}
\left[
\operatorname{SiLU}(W\_{\text{gate}}x)
\odot
(W\_{\text{up}}x)
\right].\]

名称 `gate` 和 `up` 只是实现惯例，互换它们并不改变运算本身。公式中省略了偏置项，因为许多 Llama 风格的实现不使用偏置。SwiGLU 本身并不要求无偏置设计。

一个朴素的 GPT-2 风格前馈层使用两个投影：

\[\operatorname{FFN}(x)
= W\_2\,\operatorname{GELU}(W\_1x).\]

第一个矩阵扩展模型宽度，GELU 提供非线性，第二个矩阵回到残差流的宽度。SwiGLU 把单条扩展路径替换为两条路径。经过激活的门可以在降投影之前，对另一条路径中的特征进行抑制、放行或缩放。

| 模块 | 扩展表示 | 乘性门控 | 权重矩阵数 |
| --- | --- | --- | --- |
| GELU FFN | \(\operatorname{GELU}(W\_1x)\) | 无 | 2 |
| GLU | \(\sigma(W\_gx) \odot (W\_ux)\) | Sigmoid | 3 |
| GEGLU | \(\operatorname{GELU}(W\_gx) \odot (W\_ux)\) | GELU | 3 |
| SwiGLU | \(\operatorname{SiLU}(W\_gx) \odot (W\_ux)\) | SiLU | 3 |

SwiGLU 属于 [GLU Variants Improve Transformer](https://arxiv.org/abs/2002.05202) 所研究的家族。在那些实验中，在训练设置匹配的条件下，门控变体相比朴素的 ReLU 或 GELU 前馈层改进了 Transformer 语言建模结果。后来的 Llama 风格架构将 SwiGLU 作为一揽子改动的一部分加以采用。

三个矩阵听起来可能比两个更昂贵，但必须比较的是中间维度。忽略偏置项，一个模型宽度为 \(d\)、中间宽度为 \(m\) 的朴素前馈块大约包含

\[2dm\]

个权重。一个门控中间宽度为 \(m\_g\) 的 SwiGLU 块大约包含

\[3dm\_g.\]

个权重。令 \(m\_g \approx 2m/3\)，两种块的权重数量和矩阵乘法开销就大致相当。对于 \(m=4d\) 的朴素扩展，匹配的门控宽度约为 \(8d/3\)。实际的模型配置常常把中间宽度取整为对硬件友好的倍数，或者刻意选择不同的前馈预算，因此架构配置才是事实依据。

![朴素前馈块使用两个投影，而门控版本在输出投影之前使用分开的内容路径与激活门路径。](https://sebastianraschka.com/images/blog/2025/from-gpt-2-to-gpt-oss/8.png)

多出来的路径赋予该层一种可学习的乘性交互。朴素的 GELU 块通过单条非线性路径变换每个扩展特征。SwiGLU 允许一个学习到的特征控制另一个特征的贡献。这种额外的选择性是其经验优势的一个合理解释，不过确切收益取决于模型规模、宽度、优化器、数据和训练预算。

SwiGLU 不会缩小注意力矩阵、上下文长度或 KV 缓存。它改变的是每个 transformer 块中位于注意力之后的前馈子层。前馈权重通常占稠密 LLM 参数的很大一部分，因此其中间宽度对检查点大小和每 token 计算量都有明显影响。

运行时的比较也依赖于实现。SwiGLU 有两个（而不是一个）输入投影，但在预算匹配时每个投影都可以更窄。融合核（kernel）可以合并激活运算和逐元素乘法。一个有说服力的基准测试应当固定模型宽度、等效前馈参数量、精度、批次形状和硬件。

![GPT 到 Llama 的演进中，SwiGLU 与归一化、位置处理和注意力的各自独立变化一同出现。](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/gpt-to-llama/gpt2-to-llama2-llama3.webp)

SwiGLU 也出现在许多专家混合（MoE）模型内部。每个专家都可以是一个 SwiGLU 前馈网络。其内部的门作用于发送给该专家的每个 token 的特征通道。MoE 路由器则是一个单独的机制，决定哪些专家接收该 token。把这两种运算都称作「门控」不应掩盖这一区别。

SwiGLU 的广泛使用支持一个有分寸的结论。门控前馈变体在受控研究和成功的训练配方中表现良好，而且通过调整中间宽度，其开销可以保持在接近朴素 MLP 的水平。完整模型之间的对比无法把质量差异单独归因于 SwiGLU，因为归一化、注意力、模型规模、数据和训练方式同时都在变化。

关于更宏观的块级演进，参见[哪些架构变化把 GPT 风格模型变成了 Llama 风格模型？](https://sebastianraschka.com/faq/docs/gpt-style-to-llama-style.html)。相关的[专家混合 FAQ](https://sebastianraschka.com/faq/docs/mixture-of-experts.html)讲解了独立的专家路由机制。
