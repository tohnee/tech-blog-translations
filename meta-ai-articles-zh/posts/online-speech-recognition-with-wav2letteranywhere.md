---
title: "使用 wav2letter@anywhere 进行在线语音识别"
title_en: "Online speech recognition with wav2letter@anywhere"
date: 2019-03-15
source: https://ai.facebook.com/blog/online-speech-recognition-with-wav2letteranywhere
crawled: 2026-09-22
translated: 2026-09-22
---

# 使用 wav2letter@anywhere 进行在线语音识别

> 原文：[Online speech recognition with wav2letter@anywhere](https://ai.facebook.com/blog/online-speech-recognition-with-wav2letteranywhere) · Meta AI（Wayback 存档）

从输入音频流中实时转录语音的过程被称为在线语音识别。大多数自动语音识别（ASR）研究都专注于在不受实时性约束的前提下提升准确率。然而对于直播视频字幕或设备端转录这类应用而言，降低音频与对应转录之间的时延非常重要。在这些场景下，需要时延有限的在线语音识别才能提供良好的用户体验。

为满足这一需求，我们开发并开源了 wav2letter@anywhere——一个可用于执行在线语音识别的推理框架。wav2letter@anywhere 构建在 Facebook AI 此前发布的 wav2letter 和 wav2letter++ 之上。大多数现有的在线语音识别解决方案只支持循环神经网络（RNN）。而 wav2letter@anywhere 改用全卷积声学模型，在部分推理模型上实现了 3 倍的吞吐量提升，并在 LibriSpeech 上取得了当时最先进的性能。

要让一个系统在生产规模下运行（在服务器 CPU 上，或在低功耗环境中于设备端运行），必须确保系统在计算上高效。把一个 ASR 系统从研究环境带到低时延、计算高效且高度准确的系统，需要对实现和算法都做出不小的改动。这篇文章介绍了我们如何打造 wav2letter@anywhere。

下图展示了我们的在线系统如何处理语音。每段语音块首先被送入声学模型，计算词片（word-piece）分数。随后这些分数通过轻量级的束搜索解码器与语言模型结合，基于输入序列和所选语言模型输出最可能的词序列。

wav2letter@anywhere 推理平台

wav2letter@anywhere 是 wav2letter++ 仓库的一部分，可用于执行在线语音识别。该框架基于以下目标构建：

- 流式 API 的推理应当高效，同时足够模块化，能处理各种类型的语音识别模型。
- 框架应支持并发音频流——在生产规模执行任务时，这是获得高吞吐量的必要条件。
- API 应足够灵活，便于在不同平台（个人电脑、iOS、Android）上轻松使用。

我们的模块化流式 API 让框架能够支持多种模型，包括 RNN 和（更快的）卷积神经网络。wav2letter@anywhere 用 C++ 编写，独立自足且效率尽可能高，可以嵌入到任何地方。我们使用了 FBGEMM 等高效后端，以及针对 iOS 和 Android 的专用例程。它从一开始就是面向流式场景设计的（不像一些依赖通用推理管线的替代方案），这使我们能够实现高效的内存分配设计。

时延控制 ASR 领域的许多近期工作使用时延控制双向 LSTM（LC-BLSTM）RNN、RNN Transducer（RNN-T）或这些方法的变体。与这些先前工作不同，我们提出了采用连接时序分类（CTC）准则的全卷积声学模型。我们的论文表明，这样的系统部署效率显著更高，同时能取得更低的词错误率（WER）和更低的时延。

## 低时延声学建模

wav2letter@anywhere 的一个重要构件是时间深度可分离（time-depth separable，TDS）卷积，它在保持准确率的同时大幅缩减了模型规模和计算量。我们对所有卷积使用非对称填充，在输入开头一侧加入更多填充。这减少了声学模型看到的未来上下文，从而降低时延。

TDS 卷积模块。

在将我们的系统与两个强基线（同一基准上的 LC-BLSTM + lattice-free MMI 混合系统和 LC-BLSTM + RNN-T 端到端系统）比较时，我们在 WER、吞吐量和时延上都取得了更好的表现。最值得一提的是，即使推理以 FP16 运行，我们的模型仍比以 INT8 运行推理的基线快 3 倍。

我们的 TDS + CTC 系统与其他系统的实验结果对比。

在近期的一项工作中，我们在监督与半监督两种设置下，将 wav2letter++ 与现代声学和语言模型架构结合使用。我们重新审视了一种标准半监督技术：用仅在 1,000 小时有标注数据上训练的声学模型，对 60,000 小时无标注音频生成伪标签，再用全部 61,000 小时伪标签数据训练一个新的声学模型，从而在 LibriSpeech 上刷新了当时的最先进纪录。与监督设置下训练的最先进模型相比，我们取得了超过 16% 的相对改进。

我们正在发布与该论文相关的模型，以及适合 wav2letter@anywhere、用于快速实时推理的时延约束模型。

自一年前开源 wav2letter++ 以来，我们做了大量改进，包括增强解码器性能（seq2seq 解码提速 10 倍）、为特征、解码器、准则等添加 Python 绑定，以及更完善的文档。我们相信，wav2letter@anywhere 通过实现在线语音识别并显著降低音频与转录之间的时延，又向前迈出了一大步。我们很高兴能与社区分享这个开源框架。

关于 wav2letter@anywhere 的更多信息，请阅读完整论文并访问 wiki。

我们要感谢 Qiantong Xu、Jacob Kahn、Gilad Avidov、Tatiana Likhomanenko、Awni Hannun、Vitaliy Liptchinsky 和 Gabriel Synnaeve 在 wav2letter@anywhere 上的工作。

**作者**

- Vineel Pratap，研究工程师
- Ronan Collobert，研究科学家
