---
title: "Facebook 研究团队在 Interspeech 2020"
title_en: "Facebook research at Interspeech 2020"
date: 2020-10-23
source: https://ai.facebook.com/blog/facebook-research-at-interspeech-2020
crawled: 2026-09-22
translated: 2026-09-22
---

# Facebook 研究团队在 Interspeech 2020

> 原文：[Facebook research at Interspeech 2020](https://ai.facebook.com/blog/facebook-research-at-interspeech-2020) · Meta AI（Wayback 存档）

2020 年 10 月 23 日

Facebook 将在 Interspeech 2020 上展示 23 篇论文——这是研究社区分享语音科学与技术进展的主要会议之一。这些研究代表了我们在推进口语处理领域 AI 方面持续努力的多个重要里程碑，涵盖语音识别、语音合成、语音翻译、声音转换、音频处理等。

尽管我们今年对 Interspeech 的贡献横跨多样主题，但我们正在推进的工作中仍有一些值得注意的主线。

## ASR 中的 transformer 进展

Transformer 模型已成为自然语言处理（NLP）领域的行业标准，在多种文本任务上交出最先进结果。最近我们还证明，基于 transformer 的模型在语音识别上同样能达到最先进性能。然而，在 transformer 成为语音的标准建模方法之前，仍存在一些障碍。例如，transformer 通常一次处理整个句子，使模型能学习句子中任意及所有词之间的关系。在语音世界，这被视为离线或批处理，不适合许多语音应用。例如实时字幕或数字助手，语音识别系统必须以流式方式处理传入音频，在话语被说出的同时持续输出假设词。在 Interspeech 上，我们提出一个增强记忆 transformer 模型，通过利用一组紧凑表示先前片段信息的记忆库，只处理短音频片段。这一方法相较此前创建可流式 transformer 模型的尝试带来显著增益，并比流式应用常用的标准循环网络降低 15% 的词错误率（WER）。

虽然我们从为 NLP 开发的 transformer 模型中汲取灵感，但文本与音频之间存在显著差异。与文本相比，一段音频中相邻帧彼此相关性高得多，与远处帧的相关性则低得多。基于这一观察，我们为基于 transformer 的语音识别创建了弱注意力抑制机制。对 transformer 模型中自注意力机制的这一修改，在标准基准数据集上降低 5-10% 的 WER。最后，我们展示 transformer 网络与卷积网络如何都能用于创建高效语音识别系统——这在 Facebook 规模下执行语音识别时很有帮助。

## 通过自监督与半监督学习减少标签

AI 最大的挑战之一是对带标注训练数据的需求。对语音识别而言，这通常意味着人工以逐字转录标注录音；对翻译而言，则意味着把一种语言的转录人工翻译成另一种语言。获取这类标注耗时费力，某些情况下所需的专业知识也难以找到。我们一直致力于借助自监督与半监督学习，减少在多个 AI 领域对带标注数据的依赖。这使我们能构建对带标注数据需求大幅降低的 AI 系统。

在自监督中，完全不需要标签即可创建适合模型学习的表示，通常让模型从输入的一部分预测另一部分。在语音中，这可以是根据到目前为止观察到的音频预测未来出现的音频片段。在半监督学习中，自训练是最成功的方法之一：先用少量带标注数据训练初始「教师」ASR 模型，再用它为规模大得多、没有标注的音频集合生成假设转录，然后用这些转录训练参数量相近或更少的「学生」ASR 模型。

在一系列论文中，我们展示半监督学习与自监督学习如何在多个语音任务上带来改进。例如，我们在转录社交媒体视频的任务上，把多种自训练方法与此前提出的弱监督学习版本进行比较。我们表明，当只有少量转录数据可用时，通过为两种低资源语言利用 2 万到 5 万小时无标注音频，错误最多可减少 20%。我们展示这种自训练方法可以通过模型训练与标注的迭代过程进一步改进。最后，我们把这些方法应用于语音翻译任务——AI 系统的工作更复杂：接收一种语言的音频并输出翻译成另一种语言的文本。我们展示了自监督表示与半监督自训练如何在这些场景中改进语音翻译。

## 迁移学习造福低资源场景

在某些情况下，例如世界上较少使用的语言，可用于训练的数据量可能相当有限。为这类语言提供高质量语音识别 AI 系统的一个知名途径是迁移学习。在语音识别语境中，迁移学习可用于把语言信息从一个系统迁移到另一个。特别地，在数据丰富语言（如英语）上训练的 AI 模型，可用于初始化一个将在数据有限语言上训练的模型。这使我们的系统能利用语言间的共性，把在一个语言上训练的系统的知识迁移来惠及另一语言的系统。

我们分享两种在训练数据有限的低资源设置中有效改进语音识别的方法。在一篇论文中，我们表明可以通过辅助语音翻译任务应用迁移学习来改进 ASR 性能。在另一种方法中，我们构建了一个能识别 50 种语言的大规模多语言语音识别系统。通过在大量语言间共享模型的大部分，我们能有效在这些系统间共享知识，把低资源语言的词错误率降低超过 20%。此外，我们正在发布一个基于知名 Librivox 有声书集合的大规模多语言语音语料库。我们希望该数据集能鼓励该领域的进一步工作。

## 语音合成与重建

研究社区对需要生成、增强与操纵语音信号的应用兴趣日增。为解决噪声环境中采集语音的问题，我们提出一个基于自编码器的方法，结合时域与频域重建项来去除多种噪声，包括房间混响。该方法在笔记本电脑 CPU 上实时运行的同时，取得最先进的语音增强结果。

为支持语音合成中的多种声音并实现各类娱乐应用，我们展示了声音转换（把一个人声音的音频转换为另一个人的任务）的新研究，涵盖语音与歌唱。两种方法都利用预训练的语音识别模型来编码语音信号，歌唱方法还以音高提取网络为条件。虽然这些模型是全卷积且非常高效的，但目前还不是因果的。我们还展示了一种执行语音合成的方法，使用来自传入语音请求的风格迁移。这将使数字助手能根据请求的内容与说话方式来回应用户：用户是开心、沮丧、悲伤还是匆忙？实验表明，用户更喜欢带风格的合成回复，并证明了系统模仿传入语音查询风格的能力。

以下是我们将展示的论文完整清单：

- 面向 ASR 的上下文循环神经网络转换器（Contextual recurrent neural network transducers for ASR）
- 用混合指针网络语言模型做上下文 ASR 格重评分（Contextualizing ASR lattice rescoring with hybrid pointer network language model）
- 面向同声机器翻译的高效 wait-K 模型（Efficient wait-K models for simultaneous machine translation）
- 隐藏并说话：迈向用于语音隐写的深度神经网络（Hide and speak: towards deep neural networks for speech steganography）
- 用语音翻译改进端到端 ASR 的迁移学习（Improving transfer learning for end-to-end ASR with speech translation）
- 通过联合风格分析的交互式文本转语音系统（Interactive text-to-speech system via joint style analysis）
- 面向 ASR 的迭代伪标注（Iterative pseudo-labeling for ASR）
- 面向低资源视频 ASR 的大规模弱监督与半监督学习（Large scale weakly and semi-supervised learning for low-resource video ASR）
- 大规模多语言 ASR：50 种语言、1 个模型、10 亿参数（Massively Multilingual ASR: 50 Languages, 1 Model, 1 Billion Parameters）
- MLS：面向语音研究的大规模多语言数据集（MLS: A large-scale multilingual dataset for speech research）
- 波形域的实时语音增强（Real time speech enhancement in the waveform domain）
- 用卷积网络扩展时延受控的端到端语音识别（Scaling latency-controlled end-to-end speech recognition using convnets）
- 面向无监督音素切分的自监督对比学习（Self-supervised contrastive learning for unsupervised phoneme segmentation）
- 自监督表示改进端到端语音翻译（Self-supervised representations improve end-to-end speech translation）
- 面向端到端语音翻译的自训练（Self-training for end-to-end speech translation）
- 混响声场中的空间协方差矩阵估计及其在最优波束形成中的应用（Spatial covariance matrix estimation in reverberant sound fields with application to optimal beamforming）
- 通过分块自助法对 ASR 性能做统计检验（Statistical testing on ASR performance via blockwise bootstrap）
- 用增强记忆自注意力的流式 transformer 声学模型（Streaming transformer-based acoustic models using self-attention with augmented memory）
- 时间-频率平均对混响环境中双耳说话人定位的重要性（The importance of time-frequency averaging for binaural speaker localization in reverberant environments）
- TTS 皮肤：通过 ASR 做说话人转换（TTS skins: Speaker conversion via ASR）
- 无监督跨域歌唱声音转换（Unsupervised cross-domain singing voice conversion）
- 面向基于 transformer 的语音识别的弱注意力抑制（Weak-attention suppression for transformer based speech recognition）
