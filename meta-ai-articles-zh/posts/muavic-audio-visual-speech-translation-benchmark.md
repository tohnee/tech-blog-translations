---
title: "MuAViC：首个音视频语音翻译基准"
title_en: "MuAViC: The first audio-video speech translation benchmark"
date: 2023-03-08
source: https://ai.facebook.com/blog/muavic-audio-visual-speech-translation-benchmark
crawled: 2026-09-22
translated: 2026-09-22
---

# MuAViC：首个音视频语音翻译基准

> 原文：[MuAViC: The first audio-video speech translation benchmark](https://ai.facebook.com/blog/muavic-audio-visual-speech-translation-benchmark) · Meta AI（Wayback 存档）

在无数日常场景中，背景噪声——车流声、音乐、其他人说话——都会让人更难听清别人在说什么。人类常常借助其他感官的信息，尤其是视觉，来帮助交流（正如 Harry McGurk 和 John MacDonald 在 1976 年的研究「Hearing Lips and Seeing Voices（听唇见声）」中所指出的）。例如，在喧闹的演唱会上和朋友交谈时，你很可能会盯着对方的脸，来补充你听到的内容。AI 研究者最近构建了利用视觉信息提升英语语音识别任务性能的系统（如 Meta AI 公开可用的 AV-HuBERT 和 RAVen 模型）。现在，Meta AI 发布 MuAViC（Multilingual Audio-Visual Corpus，多语言音视频语料库）——首个让音视频学习可以用于高精度语音翻译的基准。我们用 MuAViC 训练 AV-HuBERT 模型，在嘈杂、有挑战的环境中翻译语音，其表现优于其他领先的翻译模型。

（视频说明：在此示例中，AV-HuBERT 模型的转写包含一处错误（把「Hi there」写成「Either」），但准确率仍远高于另一个模型。）

凭借「No Language Left Behind」和通用语音翻译器等项目，Meta 一直聚焦语音翻译研究，因为它在打破沟通壁垒、把人们连接在一起方面有不可思议的潜力。我们很高兴看到研究社区的其他人如何用 MuAViC 打造在真实世界条件下也能良好工作的翻译系统。

## 创建 MuAViC

由于合适的训练数据稀缺，把音视频理解扩展到语音翻译此前一直无人探索。采集和处理音视频数据通常比仅采集音频数据需要更多资源。MuAViC 是首个音视频语音翻译基准，也是最大的多语言音视频语音识别基准。它包含约 1200 小时的转写数据，覆盖 9 种语言。

对于英语讲话，我们复用 LRS3 数据集的音视频数据，并用文本匹配算法将其与机器翻译语料对齐。匹配到的样本再与机器翻译语料中相应的目标句子配对，作为翻译标签。我们对开发集和测试集样本采用精确文本匹配，以确保最佳准确率。对于没有匹配到的训练集样本，我们用机器翻译模型获取伪翻译标签。对于非英语讲话，我们复用语音翻译数据集中采集的纯音频数据、转写和文本翻译。为加入视觉模态，我们获取原始录音的视频轨道，并将处理后的视频数据与音频数据对齐，构成音视频数据。虽然所有音频数据都有转写，但只有一部分被翻译。我们使用与之前相同的机器翻译模型获取伪翻译标签。

## 训练端到端模型

我们使用 Meta 的 AV-HuBERT 架构创建了端到端的音视频语音识别和音视频语音翻译模型。给定一对对齐的音视频数据，我们的模型能够同时处理两种模态，并把它们的表示融合到一个统一空间，可用于语音识别或翻译任务。而且如果任一模态缺失，AV-HuBERT 仍可处理可用的输入模态（但效率会降低）。

（视频说明：在此视频中，模型必须应对背景音乐（而非第一个视频中的背景噪声）。）

我们模型最值得注意的特性是对噪声的鲁棒性。如果音频模态因噪声或其他因素而失真，模型会更加依赖视觉模态来正确完成任务。我们在有噪声和无噪声环境中，将我们的模型与语音识别和 X-En（多语言到英语）语音翻译任务的最先进模型进行了对比测试。（图表说明：该图比较了覆盖九种语言的语音识别任务上的模型表现。Meta 的 AV-HuBERT 模型在嘈杂环境中不会显著退化，而当前最先进模型则会。）类似地，在覆盖六种语言的 X-En 语音翻译任务上，Meta 的 AV-HuBERT 模型的性能相较最先进模型也没有显著下降。

## 迈向鲁棒的语音翻译

MuAViC 让研究者得以为不同语言构建鲁棒的语音识别和翻译系统。我们已发布语料库以及覆盖九种语言的音视频语音识别和翻译模型。我们希望这能帮助社区构建更好、更鲁棒的语音模型。我们对强大鲁棒模型的未来充满期待。

阅读完整论文：MuAViC: A Multilingual Audio-Visual Corpus for Robust Speech Recognition and Robust Speech-to-Text Translation；MuAViC GitHub 仓库。

我们要感谢 Vedanju Goswami、Wei-Ning Hsu、Bowen Shi 对本篇博客所讨论工作的贡献。

作者：Mohamed Anwar，Meta AI 驻留成员；Jeff Wang，产品经理；Juan Pino，研究科学家；Changhan Wang，研究工程师
