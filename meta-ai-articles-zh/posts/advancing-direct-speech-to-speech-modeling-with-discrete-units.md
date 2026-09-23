---
title: "以离散单元推进直接语音到语音建模"
title_en: "Advancing direct speech-to-speech modeling with discrete units"
date: 2022-06-13
source: http://ai.facebook.com/blog/advancing-direct-speech-to-speech-modeling-with-discrete-units
crawled: 2026-09-22
translated: 2026-09-22
---

# 以离散单元推进直接语音到语音建模

> 原文：[Advancing direct speech-to-speech modeling with discrete units](http://ai.facebook.com/blog/advancing-direct-speech-to-speech-modeling-with-discrete-units) · Meta AI（Wayback 存档）

**研究内容：**要让人们在说不同语言时也能轻松相互理解，我们需要的不仅仅是基于文本的翻译系统。但构建语音到语音翻译系统的常规方法面临两大短板：它采用级联的一系列步骤——语音识别，然后是文本到文本翻译，最后把译文转换回语音——计算成本和推理延迟在每个阶段不断累加。此外，世界上超过 40% 的语言没有文字书写系统，使得这种方法无法把翻译扩展到每一种口头语言。为了实现更快的推理并支持无文字语言之间的翻译，Meta AI 正在分享我们直接语音到语音翻译（S2ST）方法的新工作，它不依赖文本生成作为中间步骤。我们的方法优于以往方法，并且是首个在多个语言对上用真实世界开源音频数据（而非合成音频）训练的直接 S2ST 系统。

**工作原理：**近期的语音到语音建模工作沿用传统文本到语音合成的思路。这些模型把源语音直接翻译成目标语音的频谱图（spectrogram）——即以多维连续值向量表示的频谱。然而，用语音频谱图作为目标训练翻译模型可能很困难，因为模型必须学习两种语言之间关系的多个不同方面（例如它们如何彼此对齐、声学与语言学特性如何比较）。我们不用频谱图，而是使用从自监督语音表示聚类得到的离散化语音单元。与频谱图相比，离散单元可以把语言内容与韵律信息解耦，并利用现有的自然语言处理建模技术。

借助离散化语音单元，我们取得了三项值得注意的进展：我们的 S2ST 系统优于以往的直接 S2ST 系统；它是首个在多个语言对上用真实 S2ST 数据训练的直接 S2ST 系统；它利用了未标注语音数据的预训练。

### 用离散单元进行直接语音到语音翻译

为实现用离散单元（音频样本在此）进行直接语音到语音翻译，我们使用自监督离散单元作为目标（语音到单元翻译，S2UT）来训练直接 S2ST 系统。在下图中，我们提出了一个基于 transformer 的序列到序列模型，包含语音编码器和离散单元解码器，并加入辅助任务（以虚线表示）。

（图：使用离散单元的直接 S2ST 模型示意图。）

我们使用 Fisher 西班牙语-英语语音翻译语料库进行实验，它包含 139K 句来自西班牙语电话对话的句子（约 170 小时）及对应的西班牙语和英语文本转录。我们使用高质量的自家文本到语音引擎，以单一女声准备合成目标语音作为训练目标。我们的全部实验——包括基线——都使用合成目标语音进行，且不将该 TTS 引擎用于其他用途。通过把源语言的离散单元用作辅助任务目标，所提系统可以在无文本（textless）设定下训练，相比以往工作取得显著改进。与预测频谱图特征的基线直接 S2ST 模型相比，使用离散单元带来 6.7 BLEU 的提升。

### 用真实世界数据训练多语言无文本语音到语音翻译系统

由于缺乏平行的 S2ST 训练数据，以往直接 S2ST 的工作主要依赖 TTS 生成合成目标语音来训练模型，这对支持没有标准文字书写系统的语言并不现实。鉴于 Meta AI 的 FAIR 团队最近发布了大规模 S2ST 数据，在《Textless speech-to-speech translation on real data》（音频样本在此）中，我们在 VoxPopuli S2S 数据（下载）和自动挖掘的 S2S 数据（下载）上训练所提 S2UT 系统，无需任何额外文本监督。关键是一种用少至一小时语音数据即可训练的语音归一化技术。该方法在不改变词汇内容的前提下去除真实目标语音中多说话者带来的变异，相比未归一化目标改善了 S2UT 性能。此外，我们最好的无文本直接语音翻译模型达到了与级联的基于文本系统相当的性能，且无需人工标注来构建转录目标语音的 ASR 模型。在训练中进一步纳入自动挖掘的 S2ST 数据带来了额外 2.0 BLEU 的增益。这是无文本 S2ST 系统首次在多种语言上用公开可得的真实世界数据成功训练并展现出有竞争力的结果。我们相信它也是首个证明挖掘所得 S2ST 数据有用性的实证研究。

### 通过预训练进一步改进语音到语音翻译

最后，我们在《Enhanced direct speech-to-speech translation using self-supervised pretraining and data augmentation》（音频样本在此）中，通过未标注语音数据的预训练，继续改进前两篇论文中系统的 S2UT 性能。我们表明，从最先进语音到文本翻译（S2T）系统借鉴的预训练思路，在使用离散单元作为目标时可以很好地迁移到直接 S2ST，带来至少 6.5 BLEU 的增益，追平甚至超越级联系统的性能。此外，我们用超过 1K 小时语音生成的弱监督数据增强训练数据，带来额外 2.7 BLEU 的增益。我们的工作为未来的语音到语音翻译研究开辟了道路，进一步提升翻译质量，为用户带来更无缝的交流体验。

（示例视频：西班牙语到英语：源语音与翻译。英语到西班牙语：源语音与翻译。在这些示例中，我们的 S2ST 模型直接生成了翻译，并未先生成文本翻译。屏幕上显示的文字是由 ASR 模型生成的，以便让示例对读者更清晰。）

**为什么重要：**用离散单元进行直接语音到语音建模，为构建更好的翻译系统展现了激动人心的未来。除了翻译质量，基准测试还表明，与基于频谱图的 S2ST 系统和级联系统相比，我们提出的系统在运行时间、FLOPS 和最大内存方面都最为高效。这里讨论的工作也让我们更接近于对无文字语言同样好用的翻译系统——这类语言在世界各地的方言中仍然流行，却基本得不到支持。随着论文和代码的发布，我们希望助力研究界未来的直接语音到语音翻译进展。我们的评估使用开源模型完成。我们希望我们的测量协议能被采用，让未来的所有进展都能得到公平、公开的比较。

阅读完整论文并获取代码：

- 样本与代码
- Direct Speech-to-Speech Translation With Discrete Units
- Textless Speech-to-Speech Translation on Real Data
- Enhanced Direct Speech-to-Speech Translation Using Self-supervised Pre-training and Data Augmentation

本篇博文讨论的这系列工作离不开 Yossi Adi、Peng-Jen Chen、Paul-Ambroise Duquenne、Hongyu Gong、Jiatao Gu、Qing He、Wei-Ning Hsu、Ann Lee、Xutai Ma、Juan Pino、Adam Polyak、Sravya Popuri、Holger Schwenk、Yun Tang、Changhan Wang（按姓氏字母序排列）的贡献。我们感谢 Necip Fazil Ayan、Brian Bui、Andy Chung、Jade Copet、Ning Dong、Emmanuel Dupoux、Hirofumi Inaguma、Semarley Jarrett、Justine Kao、Evgeny Kharitonov、Felix Kreuk、Ilia Kulikov、Kushal Lakhotia、Abdelrahman Mohamed、Tu Anh Nguyen、Brian O'Horo、Gustavo Gandia Rivera、Morgane Rivière、Chris Summers、Jeff Wang、Carleigh Wood、Ethan Ye 和 Al Youngblood（按姓氏字母序排列）对这项工作的支持与讨论。

**作者**

- Ann Lee，研究科学家
- Juan Pino，研究科学家
- Jeff Wang，产品经理
- Ethan Ye，产品设计师
