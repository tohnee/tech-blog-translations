---
title: "GPT、Llama、Qwen 与 Gemma 架构对比"
title_en: "GPT, Llama, Qwen, and Gemma Architectures Compared"
source: https://sebastianraschka.com/faq/docs/gpt-llama-qwen-gemma-comparison.html
crawled: 2026-09-06
translated: 2026-09-14
---

# GPT、Llama、Qwen 与 Gemma 架构对比

> 原文：[GPT, Llama, Qwen, and Gemma Architectures Compared](https://sebastianraschka.com/faq/docs/gpt-llama-qwen-gemma-comparison.html) · Sebastian Raschka's FAQ

从高层来看，这些架构是近亲。有公开文档的 GPT 风格模型、Llama、Qwen 和 Gemma 都使用自回归的 decoder-only transformer。它们围绕残差连接重复堆叠因果自注意力层和前馈层，然后预测下一个 token。

仅凭家族名称不足以做精确比较，因为每个家族在世代更迭间都会变化。此外，OpenAI 并未公布近期专有 GPT 模型完整的模块级规格。因此，我用公开的 GPT-2 和 GPT-3 设计作为较早的 GPT 风格参照，用有名称的开放权重检查点代表较新的家族。

![仓库的 GPT-to-Llama 材料遵循有据可查的演进路径：从 GPT-2 风格的解码器到 Llama 2 再到 Llama 3](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/gpt-to-llama/gpt2-to-llama2-llama3.webp)

下面这个代表性对比概括了模块级的主要差异：

| 代表性设计 | 归一化 | 位置信息 | 注意力 | 前馈层 | 参数布局 |
| --- | --- | --- | --- | --- | --- |
| GPT-2/3 风格 | LayerNorm | 可学习的绝对位置嵌入 | 多头注意力 | GELU MLP | 稠密 |
| Llama 3 | RMSNorm | RoPE | 分组查询注意力 | SwiGLU | 稠密 |
| Qwen3 8B | RMSNorm | RoPE | 带 QK-Norm 的 GQA | SwiGLU | 稠密 |
| Gemma 3 27B | RMSNorm（附加了更多归一化位置） | RoPE | 带 QK-Norm 与局部/全局层的 GQA | GeGLU | 稠密 |

较老的 GPT 风格设计作为干净的基线很有用。它在 token 嵌入之上加入可学习的位置嵌入，使用 LayerNorm，并为每个注意力头配备各自的 key 和 value 投影。它的前馈块使用 GELU。仓库中的小型 GPT 实现遵循这一模式，因为每个部分都便于检查和实现。

Llama 保持了相同的解码器结构，同时更换了若干组件。RMSNorm 取代 LayerNorm，RoPE 把位置信息移入注意力，SwiGLU 取代了普通的 GELU MLP。Llama 3 还使用了[分组查询注意力](https://sebastianraschka.com/faq/docs/grouped-query-attention.html)，让一组查询头共享 key 和 value 头，从而减少生成时的 KV 缓存内存。

Qwen3 的稠密模型与这套 Llama 风格配方相似。Qwen3 8B 在注意力内部加入了 QK-Norm，并使用更大的词表。该家族还包含专家混合（MoE）模型，每个 token 只激活可用前馈专家的一个子集。稠密与 MoE 是真正的架构差异；而 base、instruct、coder、reasoning 这类标签通常描述的是训练方式或预期用途，不应被当作 transformer 模块的特征。

![Qwen 概览将稠密与 MoE 架构同 base、instruct、coder 和面向推理的发布版本区分开来](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/qwen/qwen-overview.webp)

Gemma 3 做出了另一组选择。它使用 GeGLU 而非 SwiGLU，并在注意力和前馈子层周围更多位置放置 RMSNorm。Gemma 3 27B 以 5 比 1 的模式将滑动窗口注意力与周期性的全局注意力层结合。大多数层处理局部上下文，而全局层允许信息跨越整个序列流动。

![Gemma 3 与 Qwen3 的对比展示了两个现代解码器家族，它们在注意力调度、归一化布局和前馈激活上各不相同](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/gemma3/gemma3-vs-qwen3.webp)

这些组件选择会影响内存占用、训练稳定性和推理成本，但架构本身并不决定模型质量。参数量、分词器、训练数据、优化方法、上下文长度训练以及后训练（post-training）至少同样重要。做实用对比时，更好的做法是点名确切的检查点，并把它们的架构与训练配方及实测表现区分开来。
