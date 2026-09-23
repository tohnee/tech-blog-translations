---
title: "面向多语言语音研究的全新开放数据集"
title_en: "A new open data set for multilingual speech research"
date: 2021-01-22
source: https://ai.facebook.com/blog/a-new-open-data-set-for-multilingual-speech-research
crawled: 2026-09-22
translated: 2026-09-22
---

# 面向多语言语音研究的全新开放数据集

> 原文：[A new open data set for multilingual speech research](https://ai.facebook.com/blog/a-new-open-data-set-for-multilingual-speech-research) · Meta AI（Wayback 存档）

**它是什么：**Facebook AI 正在发布多语言 LibriSpeech（Multilingual LibriSpeech，MLS）——一个旨在帮助推进自动语音识别（ASR）研究的大规模开源数据集。MLS 旨在支持语音研究社区在英语之外语言上的工作，让世界各地的人们都能从各种 AI 驱动服务的改进中受益。MLS 提供八种语言共计超过 50000 小时的音频：英语、德语、荷兰语、法语、西班牙语、意大利语、葡萄牙语和波兰语。它还提供语言模型训练数据和预训练语言模型，以及基线，帮助研究者比较不同的 ASR 系统。由于 MLS 利用了 LibriVox 项目的公有领域有声书，它提供了一个说话人广泛多样的大数据集，并可以以非限制性许可证发布。

**工作原理：**MLS 是一个朗读语音数据集，利用了 LibriVox 有声书数据。它建立在广泛使用的 LibriSpeech ASR 基准之上，将其扩大到更大规模，并从仅限英语扩展到上述另外七种语言。为了创建它，我们对音频进行切分并与有声书文本对齐，以便为音频片段检索最佳匹配的转写。由于有声书可能非常长，我们使用 Facebook AI 的开源 wav2letter@anywhere 框架执行流式推理与对齐。受 Libri-Light（一个面向有限或无监督 ASR 的基准）成功的启发，我们还为所有收录语言提供了标注数据有限的子集（10 分钟、1 小时和 10 小时），使其适合只有少量标注数据可用的训练场景，例如自监督和半监督设定。

在准备语言建模数据时，我们利用了古腾堡计划（Project Gutenberg）数字图书馆的公有领域书籍。然后我们仔细过滤了与开发集和测试集重叠的书，并执行了语言特定的文本归一化来创建语言模型语料库。我们训练了基线声学模型，并为每种语言使用 5-gram 语言模型进行解码。在用标准 LibriSpeech 含噪测试集评估用 MLS 英语子集训练的模型时，与用 LibriSpeech 数据训练的同一模型相比，我们的词错误率改善了 20%。

**为什么重要：**开放数据集和基准一直是 AI 近来进展的关键驱动力。MLS 为 ASR 系统大规模训练研究提供了宝贵资源。它的英语数据集比 LibriSpeech 中的训练数据大约 47 倍。虽然也存在面向非英语语言的数据集和基准，但它们往往相对较小或散落在不同地方，而且很少以开放、宽松的许可证提供。我们相信，通过提供带非限制性许可证的大型多语言数据集并建立公共基准，MLS 将促进多语言 ASR 的开放协作研究，并改进世界更多语言的语音识别系统。

**获取：**MLS 已在 OpenSLR 上提供，可在此下载。所有预训练模型以及训练和评估模型的配方可在此处找到。

论文：MLS: A large-scale multilingual dataset for speech research

**作者**

- Vineel Pratap，研究工程师
- Qiantong Xu，研究工程师
- Anuroop Sriram，研究工程师
- Gabriel Synnaeve，研究科学家
- Ronan Collobert，研究科学家
