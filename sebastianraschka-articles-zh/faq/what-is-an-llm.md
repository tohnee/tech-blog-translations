---
title: "什么是大语言模型（LLM）？"
title_en: "What is a large language model?"
source: https://sebastianraschka.com/faq/docs/what-is-an-llm.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 什么是大语言模型（LLM）？

**大语言模型（LLM）**是一种神经网络，它使用大量数据和算力来训练，以对 token 序列建模。给定一个 token 序列，文本生成式 LLM 会给出可能的下一个 token 上的概率分布。

并不存在一个官方的参数量门槛，达到它语言模型就算"大"。这个词是相对于其所处时代的模型和硬件而言的。在当前的用法中，它通常指一个经过广泛预训练、拥有足以支撑众多语言任务的容量的模型，而不是为每个任务单独开发的模型。

当前大多数文本 LLM 使用 decoder-only（仅解码器）的 transformer 架构，并通过下一个 token 预测来学习。这些是常见的设计选择，并不是定义中内含的要求。BERT 这类仅编码器（encoder-only）模型同样被描述为大型预训练语言模型，而大语言模型也可以使用 transformer 之外的架构。

## 文本生成式 LLM 在计算什么

假设提示是 `Every effort moves you`。一个 GPT 风格的模型会按如下方式处理它。

1. 分词器把文本转换为 token ID。分词器属于模型管线的一部分，但通常位于神经网络本身之外。
2. 嵌入表把每个 token ID 转换成一个向量，并加入它在序列中位置的信息。
3. 一叠 transformer 块更新这些向量。因果自注意力让每个位置都能使用更早的 token，而前馈层则分别变换每个位置。
4. 最后一个线性层在每个输入位置上为词表中的每个 token 产生一个 **logit**。
5. 生成时，最后一个位置的 logit 被转换为概率。解码器选出一个 token，将其追加到输入中，然后重复这个过程。

![GPT 风格语言模型把输入文本映射为 token ID，产生词表 logit，再把选中的 token ID 解码回文本](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch05_compressed/gpt-process.webp)

因此，模型是一次一个 token 地生成文本。一个 token 可能是一个词、词的一部分、标点、空白符或其他符号，取决于分词器。[分词 FAQ](https://sebastianraschka.com/faq/docs/tokenization-bpe.html) 解释了为什么使用这种表示，[自回归生成 FAQ](https://sebastianraschka.com/faq/docs/autoregressive-text-generation.html) 则更详细地介绍解码循环。

## 下一个 token 预训练如何工作

预训练期间，目标来自文本本身。对于一个 token 序列 (x\_1, x\_2, \ldots, x\_T)，模型学习诸如

[
p(x\_t \mid x\_1, \ldots, x\_{t-1}).
]

的条件概率。

每个训练样本都偏移一个位置。输入可以包含 token (x\_1) 到 (x\_{T-1})，而目标则包含 (x\_2) 到 (x\_T)。交叉熵损失度量模型分给真实下一个 token 的概率有多少，基于梯度的优化随之调整模型参数。

训练可以并行地评估一个序列中的所有目标位置，因为因果掩码防止某个位置看到未来的 token。生成仍是串行的，因为模型的下一个输入取决于刚刚选出的 token。这一区别在[下一个 token 预测 FAQ](https://sebastianraschka.com/faq/docs/next-token-prediction.html) 中有专门讨论。

跨书籍、文章、代码和其他文本学习这一目标，给了模型很强的动力去表示语法、语义、事实关联、写作格式以及反复出现的问题求解模式。这些规律性分布在数值参数之中。它们并不提供数据库那种精确检索的保证，这也是 LLM 可能生成流畅却不正确的文本的原因之一。

## 现代 LLM 与早期语言模型有何不同

语言建模比 transformer 早了几十年。各主要模型家族的差别在于如何表示上下文，以及能多高效地从大型数据集中学习。

| 模型家族 | 如何使用上下文 | 实际局限 |
| --- | --- | --- |
| *n*-gram 模型 | 统计短 token 序列出现的频率 | 使用固定的短窗口，未见过的序列需要平滑处理 |
| 前馈神经语言模型 | 学习嵌入，但读取的仍是固定大小的窗口 | 无法直接使用窗口之外的 token |
| RNN 或 LSTM | 串行处理 token 并向前传递隐藏状态 | 串行训练难以并行化，长程信息难以保留 |
| Transformer 语言模型 | 对可用上下文使用自注意力 | 在并行硬件上扩展性好，但随着上下文增长标准注意力变得昂贵 |

Transformer 让在更大数据集上训练更大模型变得可行。它们学到的 token 表示还允许统计证据在相关上下文之间共享。随后，扩展同一通用架构产生了可以通过提示或少量额外训练完成众多任务的模型。

GPT-2 家族展示了同一架构家族内参数量如何变化。其四个标准尺寸从 1.24 亿到 15.58 亿参数不等，差别在于宽度、注意力头数量以及重复 transformer 块的数量。

![GPT-2 家族通过改变宽度、注意力头、层数和总参数量来扩展同一个 decoder-only transformer 设计](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch05_compressed/gpt-sizes.webp)

这些模型在发布时被认为是大模型。当前的模型家族覆盖的范围宽得多，既包括只有几十亿参数的紧凑模型，也包括总参数很多但每个 token 激活参数更少的专家混合（MoE）模型。因此，参数量只有在与架构、训练数据和算力以及评估结果一起报告时才最有用。

## LLM 不自动等于聊天助手

宽泛的下一个 token 预训练产生的是**基座模型（base model）**。基座模型可以回答一些问题并延续其提示中存在的模式，但它的训练目标是文本续写。它未必被训练成把每个提示都理解为用户请求。

指令微调和偏好优化可以把这个基座检查点变成更可靠遵循请求的**指令模型（instruct model）**。额外的训练可以侧重工具使用、安全策略、编程或多步推理。[基座、指令与推理模型 FAQ](https://sebastianraschka.com/faq/docs/base-vs-instruct-vs-reasoning-model.html) 解释了这些标签。

![预训练产生一个基础模型，之后可以微调为分类器或遵循指令的助手](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch05_compressed/chapter-overview.webp)

这也解释了为什么同一个预训练模型可以支撑摘要、分类、问答、代码生成和许多其他任务。预训练创建了可复用的内部表示。提示、微调或任务特定的输出层随后把这些表示引向特定用途。

## LLM 这个标签没有告诉我们什么

把一个系统称为 LLM，仍会留下几个重要问题没有答案。

- **质量：** 更大的参数量本身并不保证更好的准确性、推理能力或效率。
- **时效性：** 模型参数反映的是其训练过程。最新信息需要更新训练数据或外部来源。
- **记忆：** 上下文窗口是临时输入，不是跨独立对话的持久记忆。
- **可靠性：** 下一个 token 预测可能产生没有依据或错误的、看似合理的陈述。
- **获取方式：** 开放权重、托管 API 和专有模型都可以是 LLM。
- **模态：** 同时处理图像或音频的系统常被称为多模态 LLM，不过对于完整系统而言，**大多模态模型（large multimodal model）**是更精确的说法。

对于一个当前的生成式模型，信息量最大的描述包括它的架构、参数化方式、上下文长度、预训练目标、后训练阶段以及预期用途。仅凭这个缩写只能识别一个宽泛的模型类别，而不是一份完整的技术规格。
