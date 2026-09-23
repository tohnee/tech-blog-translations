---
title: "语音识别新进展：为 AR 体验等提供动力"
title_en: "New advances in speech recognition to power AR experiences and more"
date: 2022-05-19
source: https://ai.facebook.com/blog/new-advances-in-speech-recognition-to-power-ar-experiences-and-more
crawled: 2026-09-22
translated: 2026-09-22
---

# 语音识别新进展：为 AR 体验等提供动力

> 原文：[New advances in speech recognition to power AR experiences and more](https://ai.facebook.com/blog/new-advances-in-speech-recognition-to-power-ar-experiences-and-more) · Meta AI（Wayback 存档）

构建新的增强现实体验，需要的不只是计算机视觉上的技术突破。尤其是智能助手——那些能理解自然、细腻对话语言的助手——将需要下一代语音系统，其能力远不止帮我们免提打电话或在手机上打开应用。明天的语音识别系统必须高效得多，以便在超轻、紧凑、时尚的眼镜上以端侧方式运行。它们还必须更准确、更鲁棒——能像人一样消歧词语、理解上下文，能应对大词表和罕见词，并在背景噪声大、多人同时说话等有挑战的环境中良好工作。Meta AI 致力于推进语音技术的最先进水平，并构建创造新增强现实与虚拟现实体验所需的技术——这将是元宇宙的重要组成部分。

语音识别系统已经是我们产品和服务中越来越重要的一部分。Meta 最近在我们多个应用中部署了新的语音功能，以支持视频字幕。这对无障碍性是一项很好的成果：耳聋或有听力损失的用户可以在各产品的视频上阅读高质量字幕。FB 和 IG Stories 中的字幕甚至已成为故事视觉个性的组成部分，人们通过调整字体、颜色、位置来进行创意表达。Meta 的语音技术还为 Portal、Quest 和 Ray-Ban Stories 设备上的免提交互提供支持。在这篇博客中，我们将重点介绍 Meta 的语音识别新研究，包括本月将在国际声学、语音与信号处理会议（ICASSP）上发表的部分论文。这些项目将助力 Meta AI 和 Meta 的 Reality Labs 共同构建帮助人们连接的新一代设备。我们很高兴能进一步推进前沿，让人们以更新颖、更有用、更愉悦的方式与设备、内容和彼此交互。

## 面向真实世界需求改进语音识别

业界和学界的语音识别研究者不断在广泛使用的公开基准上发布越来越好的结果。但尽管有这些重要进展，重大挑战依然存在。在某种程度上，解决这些挑战需要把焦点从典型的语音识别指标（如测试集上的总错误数，即平均词错误率）转向更能捕捉当前系统短板的新指标。

### 改进罕见词识别

在很多情况下，即使平均词错误率相当低，错误识别某些关键词也足以毁掉体验。想想科普视频中的专业术语，或口述消息中你朋友的名字。识别这些罕见或从未见过的词，对 RNN-T 模型等现代「端到端」语音识别系统尤其困难。为解决这一问题，我们此前创建了一套多管齐下的方法：在标准浅融合（shallow fusion）的基础上，纳入基于字典树（trie）的深偏置和神经网络语言模型上下文化。相比浅融合，错误减少了 20%。在 ICASSP 上，我们将展示神经 FST 类语言模型（Neural-FST Class Language Model，NFCLM），它进一步改进了这项工作。NFCLM 用统一的数学框架对通用背景文本和带实体的结构化查询（如点歌请求）建模。由此得到的模型在罕见词与常见词识别之间取得了更好的性能权衡，还有额外的好处：模型体积缩小了 10 倍以上。

### 公平性与负责任的语音识别

我们关注的另一个领域是公平性与负责任 AI。研究界使用的主要词错误率指标关注的是代表数据集总错误数的单一数字，无法捕捉不同人群之间的性能差异。Meta AI 最近发布了 Casual Conversations 数据集——一组旨在从性别、年龄和表观肤色维度度量计算机视觉系统公平性的视频。在 ICASSP 上，我们将分享对该语料库语音识别性能沿相同维度的最新分析，其中观察到了性别和肤色之间的显著差异。我们正在公开 Casual Conversations 数据集的转写文本，希望激励其他研究者研究这一问题，打造对所有人群都有效的语音系统。我们还引入了一种方法，用于更准确地度量和解读所关注亚群体之间语音准确率的任何差异。

### 零样本与少样本学习

改进公平性的挑战之一是获取有代表性的训练数据。除了用匹配的训练数据创建模型之外，另一种途径是创建更通用的模型，然后轻松微调到任何特定任务（或用户群体）。我们最近利用大规模半监督训练，用超过 450 万小时的自动标注数据创建了最多 100 亿参数的 ASR 模型。我们在公开的失语症语音数据集上评估了该模型。失语症是一种因大脑部分区域受损（最常见于中风）而导致的言语语言障碍。这类语音对语音识别系统来说极难准确转写。我们对通用模型应用了相对少量失语症语音的少样本学习。相比仅用失语症语音训练的系统，错误减少了 60% 以上，证明通用模型是为所有人提供高质量转写的可行途径。

尽管语音识别在过去几年取得了不可思议的进展，要确保我们构建的系统在所有用例上都有效、对所有人都有效，仍有巨大挑战。过去一年我们在这方面取得了显著进展，但正如我们在 Meta 常说的：旅程才完成了 1%。

## Meta AI 在 ICASSP 2022 上的语音识别论文

- Neural-FST class language model for end-to-end speech recognition
- Towards measuring fairness in speech recognition: Casual conversations dataset transcriptions
- Model-based approach for measuring the fairness in ASR
- Omni-sparsity DNN: Fast sparsity optimization for on-device streaming E2E ASR via supernet
- Streaming transformer transducer-based speech recognition using non-causal convolution
- Pseudo-labeling for massively multilingual speech recognition
- Word order does not matter for speech recognition
- Parallel composition of weighted finite-state transducers
- TorchAudio: Building blocks for audio and speech processing

作者：Mike Seltzer，研究总监
