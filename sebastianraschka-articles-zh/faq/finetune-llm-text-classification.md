---
title: "如何将预训练 LLM 微调用于文本分类？"
title_en: "How can a pretrained LLM be finetuned for text classification?"
source: https://sebastianraschka.com/faq/docs/finetune-llm-text-classification.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 如何将预训练 LLM 微调用于文本分类？

> 原文：[How can a pretrained LLM be finetuned for text classification?](https://sebastianraschka.com/faq/docs/finetune-llm-text-classification.html) · Sebastian Raschka's FAQ

要让一个预训练 LLM 适配文本分类，可以保留其 transformer 主干，并将下一个 token 的输出头替换为一个小型分类器。本书配套仓库的第 6 章以垃圾短信检测（spam detection）作为具体例子。

原始的语言模型输出头将每个隐藏向量映射为词表中每个 token 各对应一个 logit。而分类输出头则是将一个隐藏向量映射为 \(C\) 个 logit，其中 \(C\) 是类别数。因此，二分类的垃圾短信检测需要两个输出 logit。

![预训练的 GPT 主干可以通过替换原始输出头来适配新任务](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch06_compressed/09.webp)

分类器还需要一个代表整个输入序列的向量。对于因果（causal）的 GPT 风格模型，最后一个文本 token 处的隐藏状态是自然的选择。该位置可以关注输入中所有更早的 token，而更靠前的位置只能看到较短的前缀。

填充（padding）在这里需要小心处理。在变长批次中，数组最后一个位置可能是填充 token。分类器应当为每个样本选取最后一个非填充 token，或者使用另一种明确定义的池化规则。

![在因果 GPT 模型中，最后一个 token 的表示包含了完整前缀的信息](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch06_compressed/11.webp)

训练使用带标注的文本以及交叉熵之类的损失函数。PyTorch 的 `CrossEntropyLoss` 接收原始的类别 logit 和整数类别标签。它会在内部完成所需的 log-softmax 计算，因此训练代码不应把概率值传入该损失函数。

在推理时，对类别 logit 取 `argmax` 即可得到预测标签。如果需要概率值用于报告或阈值判断，可以先施加 softmax，不过这并不会改变得分最大的类别。

![类别 logit 可以通过 softmax 和 argmax 转换为类别预测](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch06_compressed/14.webp)

主干适配的程度是一个独立的决策。只训练新的输出头成本很低，相当于把预训练 transformer 当作固定的特征提取器。完全微调会更新每一层，需要更多内存。第 6 章采用了一种折中方案：训练新的输出头，并解冻最后一个 transformer 块以及最终的归一化层。

在微调之前，我会保持训练集、验证集和测试集的划分彼此独立。对于类别均衡的任务，准确率很有用；而对于罕见事件检测这类类别不平衡的任务，精确率、召回率和 F1 能揭示准确率可能掩盖的错误。决策阈值可以在验证集上选定，然后在测试集上保持固定。

这一流程产出的是一个专用预测器。垃圾短信分类器把文本映射到一个固定的标签集合，不再使用其输出头进行通用的下一个 token 生成。指令微调的目标则不同，它保留了生成式语言模型的接口。
