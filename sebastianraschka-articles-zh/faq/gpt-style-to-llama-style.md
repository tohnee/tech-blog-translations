---
title: "从 GPT 风格到 Llama 风格模型的架构变化"
title_en: "Architectural Changes from GPT-Style to Llama-Style Models"
source: https://sebastianraschka.com/faq/docs/gpt-style-to-llama-style.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 从 GPT 风格到 Llama 风格模型的架构变化

> 原文：[Architectural Changes from GPT-Style to Llama-Style Models](https://sebastianraschka.com/faq/docs/gpt-style-to-llama-style.html) · Sebastian Raschka's FAQ

Llama 保留了 GPT 风格解码器的基本骨架，只更换了其中的若干组件。token 嵌入、因果 transformer 块、残差路径、下一个 token 预测目标以及词表输出层都得以保留。主要的替换是 RMSNorm、RoPE、SwiGLU、无偏置的线性层，以及后期变体中的分组查询注意力。

在本文的比较中，「GPT 风格」指的是有公开文档的 GPT-2 设计，而非模块级细节未公开的近期专有 GPT 模型。

![仓库的实现遵循从 GPT-2 风格解码器到 Llama 2 再到 Llama 3 的演进，同时保持相同的自回归 transformer 主干](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/gpt-to-llama/gpt2-to-llama2-llama3.webp)

GPT-2 在其预归一化残差块中使用 LayerNorm。Llama 用 [RMSNorm](https://sebastianraschka.com/faq/docs/rmsnorm-vs-layernorm.html) 取而代之，后者依据激活值的均方根对其进行缩放，并省去了 LayerNorm 的均值中心化操作。这是一个在每个注意力和前馈子层之前都要重复执行的小小简化。

位置处理的变化更为显眼。GPT-2 为上下文窗口中的每个位置学习一个绝对位置向量，并将其加到 token 嵌入上。Llama 使用[旋转位置嵌入](https://sebastianraschka.com/faq/docs/rope-vs-absolute-positional-embeddings.html)（RoPE），在注意力内部旋转查询和键向量。注意力得分因此携带了关于 token 位置距离的结构化信息。RoPE 还避免了可学习的输入位置表，不过要把模型扩展到远超其训练上下文长度之外仍需谨慎处理。

前馈块从 GELU MLP 换成了 [SwiGLU](https://sebastianraschka.com/faq/docs/swiglu-modern-llms.html)。一个 SwiGLU 块会计算一个内容投影和一个门控，对门控施加 SiLU 激活，将两条路径相乘后再投影回模型宽度。实现中会调整中间维度，使这条额外的门控路径不会单纯地膨胀参数量。

Llama 还从大多数线性投影中去掉了可学习的偏置向量。相比权重矩阵，这节省的参数相当有限，但这一省略在整个堆叠中保持一致。[偏置项 FAQ](https://sebastianraschka.com/faq/docs/bias-terms-modern-llms.html) 更详细地讨论了这一选择。

注意力的演进是分阶段发生的。GPT-2 为每个查询头配备各自的键头和值头。Llama 2 7B 和 13B 保持了这种标准多头注意力设计，而 Llama 2 70B 使用了[分组查询注意力](https://sebastianraschka.com/faq/docs/grouped-query-attention.html)。Llama 3 在其主要模型规模上全面采用 GQA。GQA 保留多个查询头，同时共享数量更少的键头和值头，从而减少生成时的 KV 缓存。

![更宽视野的 GPT 与 Llama 对比显示：残差解码器堆叠始终清晰可辨，而归一化、位置处理、前馈层和注意力共享则随世代而变](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/gpt-to-llama/gpt-and-all-llamas.webp)

分词器和词表的变化同样重要，尽管它们位于 transformer 块之外。Llama 3 的词表相比 Llama 2 和 GPT-2 大幅扩展。这会影响分词效率以及嵌入层和输出层的规模。

这些架构替换会改变内存占用、优化过程和推理成本，但它们本身并不能解释模型质量。Llama 与 GPT-2 在规模、训练数据、上下文长度训练和后训练配方上同样存在差异。一次公平的实现对比，应当把这些因素与 transformer 块设计区分开来。
