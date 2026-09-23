---
title: "结合声学模型与语言模型训练，实现更高效的语音识别"
title_en: "Combining acoustic and language model training for more efficient speech recognition"
date: 2019-06-10
source: https://ai.facebook.com/blog/combining-acoustic-and-language-model-training-for-speech-recognition
crawled: 2026-09-22
translated: 2026-09-22
---

# 结合声学模型与语言模型训练，实现更高效的语音识别

> 原文：[Combining acoustic and language model training for more efficient speech recognition](https://ai.facebook.com/blog/combining-acoustic-and-language-model-training-for-speech-recognition) · Meta AI（Wayback 存档）

**这项研究是什么：**一种自动语音识别的新方法，联合训练声学模型和语言模型。这两类模型通常分开训练，然后在推理时用束搜索解码器组合。通过在训练时利用语言模型，这一称为可微分束搜索解码器（differentiable beam search decoder，DBD）的端到端技术简化了声学模型。DBD 让整个系统更轻量，整体推理过程更高效。

**工作原理：**束搜索解码是自然语言处理（NLP）和自动语音识别（ASR）系统在推理时常用的一种技术。NLP 和 ASR 系统通常被训练来预测字母或子词单元，而在推理时需要生成实际的词。在 ASR 中，声学模型以音频为输入、输出字母。要从字母得到词，需要用搜索过程把输出约束在一组允许的词之内。由于精确搜索的计算开销过于昂贵，系统使用近似搜索算法，例如束搜索。搜索期间通常还会使用语言模型来选出更可能的词序列。对语音识别而言，使用语言模型尤为重要，因为声学信息往往不足以区分发音相同的词。

只在推理时使用束搜索解码器并非最优，因为模型在推理时的行为与训练时不同。这项工作证明，即使声学模型和语言模型在不同粒度（字母或词）上运行，也可以穿过束搜索解码器进行训练。这项工作还表明，在训练声学模型时整合语言模型，可以得到更轻量的声学模型和更高效的推理。最后，DBD 可以联合训练声学模型和语言模型。与此前学习隐式语言模型的完全端到端方法不同，DBD 学习的是显式语言模型，既保留了完全端到端训练的好处，又拥有更灵活的组件。

**为什么重要：**在与只使用声学数据和转录的最先进语音识别系统的对比测试中，用 DBD 训练的模型明显更简单，同时取得了更低的词错误率。这种方法有望带来不仅训练更快、还能运行在时延和吞吐等硬件约束严苛的系统上的语音模型。虽然我们的结果应用于语音，但这是一种通用方法，我们相信可以很容易地推广到 NLP 领域的其他方向。

阅读完整论文：A fully differentiable beam search decoder
