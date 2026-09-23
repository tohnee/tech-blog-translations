---
title: "HuBERT：面向语音识别、生成与压缩的自监督表示学习"
title_en: "HuBERT: Self-supervised representation learning for speech recognition, generation, and compression"
date: 2021-06-15
source: https://ai.facebook.com/blog/hubert-self-supervised-representation-learning-for-speech-recognition-generation-and-compression
crawled: 2026-09-22
translated: 2026-09-22
---

# HuBERT：面向语音识别、生成与压缩的自监督表示学习

> 原文：[HuBERT: Self-supervised representation learning for speech recognition, generation, and compression](https://ai.facebook.com/blog/hubert-self-supervised-representation-learning-for-speech-recognition-generation-and-compression) · Meta AI（Wayback 存档）

2021 年 6 月 15 日

**研究内容：**许多 AI 研究项目的北极星，是持续地仅通过聆听和与他人互动来更好地识别和理解语音，就像婴儿学习第一语言那样。这不仅要分析一个人说了哪些词，还要捕捉这些词被表达方式中的许多其他线索，例如说话人身份、情绪、犹豫和打断。此外，要像人一样完整理解情境，AI 系统必须区分并解读与语音信号重叠的噪声，例如笑声、咳嗽、咂嘴声、背景车辆声或鸟鸣。为了给在音频中建模这类丰富的词汇与非词汇信息打开大门，我们发布 HuBERT——我们学习自监督语音表示的新方法。HuBERT 在语音识别、生成和压缩的语音表示学习上匹配或超越了 SOTA 方法。为此，我们的模型使用离线 k-means 聚类步骤，并通过预测被遮蔽音频片段的正确聚类来学习口语输入的结构。HuBERT 通过在聚类和预测步骤之间交替，渐进式地改进其学到的离散表示。HuBERT 的简洁性与稳定性将帮助自然语言处理和语音研究者在其工作中更广泛地采用学习到的离散表示。此外，HuBERT 学到的表示的质量便于轻松部署到许多不同的下游语音应用。

**工作原理：**HuBERT 的灵感来自 Facebook AI 用于自监督视觉学习的 DeepCluster 方法。它利用序列上的掩码预测损失（例如 Google 的 BERT 方法）来表示语音的序列结构。HuBERT 使用离线聚类步骤为掩码语言模型预训练生成带噪标签。具体而言，HuBERT 接收被遮蔽的连续语音特征，预测预先确定的聚类分配。预测损失只应用于被遮蔽的区域，迫使模型学习未遮蔽输入的良好高层表示，以便正确推断被遮蔽区域的目标。HuBERT 从连续输入中同时学习声学模型和语言模型。第一，模型需要把未遮蔽的音频输入编码为有意义的连续潜在表示，这对应经典的声学建模问题。第二，为降低预测误差，模型需要捕捉所学表示之间的长程时序关系。启发这项工作的一个关键洞见是：k-means 从音频输入到离散目标的映射的一致性（而不仅是正确性）非常重要，它使模型得以专注于建模输入数据的序列结构。例如，如果早期聚类迭代无法区分 /k/ 和 /g/ 音，导致出现包含两者的单一超级簇，预测损失就会学习到刻画其他辅音和元音如何与该超级簇协同构成单词的表示。于是，后续聚类迭代会利用新学到的表示创建更好的簇。我们的实验表明，聚类与预测步骤的交替能带来表示的渐进改进。

当 HuBERT 在标准 LibriSpeech 960 小时或 Libri-Light 60000 小时数据上预训练后，它在 10 分钟、1 小时、10 小时、100 小时和 960 小时的全部微调子集上，要么匹配要么超越了最先进的 wav2vec 2.0 的性能。图表展示了两种规模（LARGE 300M 和 X-LARGE 1B）的 HuBERT 结果。在 60000 小时 Libri-Light 数据上预训练时，X-LARGE 模型在 dev-other 和 test-other 评测子集上分别带来最高 19% 和 13% 的相对 WER 改进。

语音表示学习的这一显著成功，使直接对语音信号进行语言建模成为可能，而不依赖任何词汇资源（无监督标签、文本语料或词典）。这进而为建模非词汇信息（如戏剧性的停顿或急促的打断）以及背景噪声打开了大门。在我们的生成式口语建模（GSLM）工作中，我们迈出了利用 CPC、Wav2Vec2.0 和 HuBERT 学到的语音表示来合成语音的第一步。在离散化潜在表示上训练的单元语言模型，支持语音的条件生成与无条件生成。在自动评测和人工评测中，HuBERT 生成的样本在质量上可与最顶尖的基于字符的有监督语言模型和生成相竞争。你可以在此试听所有系统的条件与无条件生成样本：https://speechbot.github.io/ 。（上述图表展示了 HuBERT 在语言生成上的表现。）

在语音压缩方面，我们近期的论文《Speech Resynthesis from Discrete Disentangled Self-Supervised Representations》使用 HuBERT 在不降低质量的前提下达到了 365bps 的比特率。你可以试听 HuBERT 压缩音频的样本（https://resynthesis-ssl.github.io/ ）。在多刺激隐藏参考与锚点（MUSHRA）主观测试中，HuBERT 仅次于未压缩音频（256kbps）。

**为什么重要：**HuBERT 可以帮助 AI 研究社区开发完全在音频上训练的 NLP 系统，而非依赖文本样本。这将让我们能用自发口语的全部表现力来丰富现有 NLP 应用，让 AI 语音助手得以带着真人般的细微差异和情感说话。不依赖大量标注数据地学习语音表示，对覆盖新语言和新领域日益增长的工业应用和产品也至关重要。它将帮助 AI 社区构建覆盖仅有口语的方言和语言的更具包容性的应用。

阅读完整论文 / 获取代码与预训练模型

作者：
- Abdelrahman Mohamed，研究科学家
- Wei-Ning Hsu，研究科学家
- Kushal Lakhotia，软件工程师
