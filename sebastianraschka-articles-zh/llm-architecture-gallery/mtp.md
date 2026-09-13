---
title: "多 token 预测（MTP）"
title_en: "Multi-Token Prediction (MTP)"
source: https://sebastianraschka.com/llm-architecture-gallery/mtp/
crawled: 2026-09-06
translated: 2026-09-06
---

# 多 token 预测（MTP）

> 原文：[Multi-Token Prediction (MTP)](https://sebastianraschka.com/llm-architecture-gallery/mtp/)

多 token 预测（MTP）改变了语言模型在每个序列位置上学习的目标数量。在普通的下一 token 训练中，位置 `t` 的隐藏状态被用来预测 token `t+1`；MTP 则通过辅助预测头或浅层 MTP 模块，为更靠后的 token（如 `t+2` 和 `t+3`）增加损失项。

主解码器仍然保持因果性：它在生成文本时无法看到未来的 token，也仍然可以一次生成一个 token。不过，这条额外路径还有第二种可能的用途——一些推理引擎会把它保留为一个用于投机解码（speculative decoding）的小型内部草稿模型。

当模型卡提到 MTP 时，我通常会检查两个方面：训练了几个额外的预测深度？以及推理时的服务栈是否真的用上了它们？

[架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
[MTP 论文](https://arxiv.org/abs/2404.19737)

![下一 token 预测与多 token 预测的对比](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/mtp-next-token-vs-multi-token.webp)

图 1. MTP 在每个训练位置提供多个未来 token 目标。下排仍然每步生成一个
token，因为在推理时并不必使用这些额外的头。（原始出处：
[*A Dream of Spring for Open-Weight LLMs*](https://magazine.sebastianraschka.com/p/a-dream-of-spring-for-open-weight)。）

训练改动

每个序列位置为多个未来 token 偏移量贡献损失

推理选项

辅助路径可以起草若干候选 token，供主模型一并验证

示例架构

[DeepSeek V3](https://sebastianraschka.com/llm-architecture-gallery/#card-deepseek-v3)、
[Qwen3-Next 80B-A3B](https://sebastianraschka.com/llm-architecture-gallery/#card-qwen3-next-80b-a3b)、
[Step 3.5 Flash 196B](https://sebastianraschka.com/llm-architecture-gallery/#card-step-3-5-flash-196b)、
[Nemotron 3 Super 120B-A12B](https://sebastianraschka.com/llm-architecture-gallery/#card-nemotron-3-super-120b-a12b)、
[Nemotron 3.5 Lightning 30B-A3B](https://sebastianraschka.com/llm-architecture-gallery/#card-nemotron-3-5-lightning-30b-a3b) 以及
[Tencent Hy4-preview](https://sebastianraschka.com/llm-architecture-gallery/#card-tencent-hy4-preview-770b-a49b)

## 一个隐藏状态，多个目标

[最初的 MTP 论文](https://arxiv.org/abs/2404.19737)使用共享的 transformer 主干（trunk），并为每个未来 token 偏移量设置一个输出头。所有头都读取位置 `t` 处的主干表示：一个预测 `t+1`，另一个预测 `t+2`，依此类推。这些头内部包含 transformer 层，并共享最终的 unembedding 矩阵，因此它们不只是各自独立的线性分类器。为了做对齐比较的实验，论文在每增加一个头时就去掉一个主干层，以保持总参数量相等。

一种常见的现代记法是在常规下一 token 目标之外再使用 `D` 个额外预测深度，把它们的损失取平均后，以权重 \(\lambda\) 加进来。

\[\mathcal{L} = \mathcal{L}\_{\mathrm{next}} +
\frac{\lambda}{D}\sum\_{k=1}^{D}\mathcal{L}\_{\mathrm{MTP}}^{(k)}.\]

这为同一个前缀提供了多份监督信号。最初的研究发现，在 7B 规模下的 MBPP 和 HumanEval 设置中，预测四个未来 token 效果最好，而在 APPS 上则是六个最好。因此"四"只是那组代码训练消融实验的结论，并不是 MTP 的固定规则。

命名上还有一个小麻烦。论文中的 `n=4` 指的是总共四个预测，包括常规的下一 token；而工业界的标签如 MTP-1 通常指的是一个*额外的*预测深度。按照这种约定，模型在每个位置学习两个目标。

## DeepSeek 保持因果链

[DeepSeek V3](https://arxiv.org/abs/2412.19437) 使用 MTP-1 并修改了头的设计。在训练时，其额外模块把主解码器的隐藏状态与下一个真实（ground-truth）token 的嵌入组合起来，经过归一化和一个投影后，由一个 transformer 块预测下一个 token。当存在多个模块时，这一过程按顺序逐个未来偏移量继续进行。

这种安排保持了被预测 token 之间的因果关系。它也不同于原论文中彼此独立的并行头：DeepSeek 与主模型共享 token 嵌入和输出头，而每个预测深度各自拥有自己的投影和 transformer 块。

DeepSeek 的报告主要把 MTP 当作辅助训练目标。在普通自回归推理时可以丢弃该模块，主解码器的推理开销保持不变；同一个模块也可以改作投机解码之用。

## 把 MTP 用作内部草稿模型

投机解码把辅助路径变成一个提议者：它起草一小段后续内容，主模型用一次前向传播核验这些候选 token；被接受的 token 一起推进生成，一旦某个候选被拒绝，其余草稿即被丢弃并开始新一轮。

加速效果在很大程度上取决于草稿成本和接受率。[Qwen3-Next](https://huggingface.co/Qwen/Qwen3-Next-80B-A3B-Instruct) 为多步推理训练了其 MTP 路径，并为 SGLang 和 vLLM 提供了专门设置。其模型卡还指出，MTP 并不能通过 Hugging Face Transformers 通用使用——仅仅加载检查点并不会激活更快的解码路径。

这些标签仍然不足以描述完整的设计。Step 3.5 Flash 在训练和推理中使用三个额外模块，并把这一配置称为 MTP-3。[Nemotron 3 Super](https://research.nvidia.com/labs/nemotron/files/NVIDIA-Nemotron-3-Super-Technical-Report.pdf) 训练了两个共享权重的 MTP 层，可以递归地应用该共享模块来起草两个以上的 token，以缓解固定偏移训练与更长自回归草稿之间的不匹配。

因此，MTP 可以只作为训练期目标存在，也可以成为推理系统的一部分。论文报告的吞吐量增益包含了服务引擎、批大小、硬件、草稿长度和接受行为等因素，不应被解读为仅由训练损失单独带来的加速。

参考资料

[Gloeckle et al. (2024), *Better & Faster Large Language Models via Multi-token Prediction*](https://arxiv.org/abs/2404.19737)
[DeepSeek V3 技术报告](https://arxiv.org/abs/2412.19437)
[Qwen3-Next 模型卡](https://huggingface.co/Qwen/Qwen3-Next-80B-A3B-Instruct)
[Step 3.5 Flash 技术报告](https://arxiv.org/abs/2602.10604)
[Nemotron 3 Super 技术报告](https://research.nvidia.com/labs/nemotron/files/NVIDIA-Nemotron-3-Super-Technical-Report.pdf)
[A Dream of Spring for Open-Weight LLMs](https://magazine.sebastianraschka.com/p/a-dream-of-spring-for-open-weight)
[The Big LLM Architecture Comparison](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)

[返回架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
