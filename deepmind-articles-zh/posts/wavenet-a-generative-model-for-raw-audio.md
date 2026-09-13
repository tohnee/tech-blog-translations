---
title: "WaveNet：一种针对原始音频的生成模型"
title_en: "WaveNet: A generative model for raw audio"
source: https://deepmind.google/blog/wavenet-a-generative-model-for-raw-audio/
site: deepmind
date: 2016-09-08
crawled: 2026-09-13
translated: 2026-09-13
---

# WaveNet：一种针对原始音频的生成模型

> 原文：[WaveNet: A generative model for raw audio](https://deepmind.google/blog/wavenet-a-generative-model-for-raw-audio/) · Google DeepMind

本文介绍 [WaveNet](https://arxiv.org/pdf/1609.03499.pdf)，一种针对原始音频波形的深度生成模型。我们展示 WaveNet 能够生成模仿任何人声的语音，其自然程度超过现有的最佳文本转语音（TTS）系统，把与人类水平的差距缩小了 50% 以上。

我们还证明，同一网络也可用于合成音乐等其他音频信号，并展示了一些自动生成的钢琴曲的惊人样本。

## 会说话的机器

让人与机器对话是人机交互领域由来已久的梦想。过去几年，深度神经网络的应用（例如 [Google 语音搜索](https://ai.googleblog.com/2015/09/google-voice-search-faster-and-more.html)）彻底改变了计算机理解自然语音的能力。然而，让计算机生成语音——这一过程通常称为[语音合成](https://en.wikipedia.org/wiki/Speech_synthesis)（speech synthesis）或文本转语音（TTS）——在很大程度上仍然依赖所谓的[拼接式 TTS](https://scholar.google.com/citations?view_op=view_citation&hl=en&user=Es-YRKMAAAAJ&citation_for_view=Es-YRKMAAAAJ:u5HHmVD_uO8C)（concatenative TTS）：从单一说话人录制一个非常庞大的短语音片段数据库，然后重新组合这些片段来构成完整的语句。这使得很难修改声音（例如切换到不同的说话人，或改变其语音的重音或情感），除非录制一整套全新的数据库。

因此，对[参数式 TTS](https://scholar.google.com/citations?view_op=view_citation&hl=en&user=z3IRvDwAAAAJ&citation_for_view=z3IRvDwAAAAJ:d1gkVwhDpl0C)（parametric TTS）的需求很大：在参数式 TTS 中，生成数据所需的全部信息都存储在模型参数里，语音的内容与特征可以通过模型的输入加以控制。然而到目前为止，参数式 TTS 听起来往往不如拼接式自然。现有的参数式模型通常要将其输出经过称为[声码器](https://en.wikipedia.org/wiki/Vocoder)（vocoder）的信号处理算法来生成音频信号。

WaveNet 改变了这一范式：它直接对音频信号的原始波形建模，一次生成一个样本。除了带来更自然的语音之外，使用原始波形还意味着 WaveNet 可以对任何类型的音频建模，包括音乐。

## WaveNets

![一段代表一秒钟声音的蓝色原始音频波形，其下方有一条滑动的灰色条，示意放大的选区窗口。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62227b13d0dea8074a97b55c_unnamed.gif)

研究者们通常回避对原始音频建模，因为它的变化节奏太快：通常每秒有 16,000 个甚至更多样本，并且在许多时间尺度上都存在重要结构。构建一个完全自回归的模型——其中每一个样本的预测都受之前所有样本的影响（用统计学的说法，每个预测分布都以之前所有的观测为条件）——显然是一项极具挑战的任务。

不过，我们今年早些时候发表的 [PixelRNN](https://arxiv.org/abs/1601.06759) 与 [PixelCNN](https://arxiv.org/abs/1606.05328) 模型表明，生成复杂的自然图像不仅可以一次生成一个像素，还可以一次生成一个颜色通道，每张图像需要数千次预测。这启发我们把二维的 PixelNet 改造成一维的 WaveNet。

![示意图，展示 WaveNet 的分层结构：底部一行蓝色输入节点，中间三行灰色隐藏层节点，顶部一行橙色输出节点。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62227b1d1dd26da452c9e160_unnamed-2.gif)

上面的动画展示了 WaveNet 的结构。它是一个全卷积神经网络，其卷积层具有各种不同的膨胀系数（dilation factor），使其感受野随深度呈指数增长，可以覆盖数千个时间步。

训练时，输入序列是从真人说话者录制的真实波形。训练之后，我们可以从网络采样来生成合成语句。采样过程中的每一步，都会从网络计算出的概率分布中抽取一个值，然后把这个值反馈回输入，再对下一步做出新的预测。像这样一步一个样本地构建，计算开销很大，但我们发现这对生成复杂、听起来真实的音频至关重要。

## 改进最先进水平

我们使用 Google 的一些 TTS 数据集训练了 WaveNet，以便评估其性能。下图展示了 WaveNet 在 1 到 5 分制上的质量，并与 Google 当前最好的 TTS 系统（[参数式](http://research.google.com/pubs/pub45379.html)与[拼接式](http://research.google.com/pubs/pub45564.html)）以及人类语音进行比较，使用的是[平均意见得分（MOS）](https://en.wikipedia.org/wiki/Mean_opinion_score)。MOS 是主观音质测试的标准度量，通过让人类受试者参加盲测获得（对 100 个测试句子获得了 500 多次评分）。可以看到，无论是美式英语还是普通话，WaveNet 都把最先进水平与人类水平之间的差距缩小了 50% 以上。

在中文和英文上，Google 现有的 TTS 系统都被视为全球最佳之列，因此用一个模型同时在两者上取得改进是一项重大成就。

![柱状图，比较美式英语与普通话语音合成系统的平均意见得分（MOS）。美式英语：拼接式（3.86）、参数式（3.67）、WaveNet（4.21）、人类语音（4.55）。普通话：拼接式（3.47）、参数式（3.79）、WaveNet（4.08）、人类语音（4.21）。](https://lh3.googleusercontent.com/g2GvSF8JC-wdkqf6DHp09CZaKFKlL3W2jiiia4wPfUspvxirl7nvA4EuCBDUIfVYoX-QXrI0pGjw9v2ld2k9HNihEZfBlU3TXkDaxLm5a1ekvVncLw=w1440)

下面是这三种系统的一些样本，你可以亲自聆听并比较：

#### 参数式（Parametric）

您的浏览器不支持音频元素。您的浏览器不支持音频元素。

#### 拼接式（Concatenative）

您的浏览器不支持音频元素。您的浏览器不支持音频元素。

#### WaveNet

您的浏览器不支持音频元素。您的浏览器不支持音频元素。


#### 参数式（Parametric）

您的浏览器不支持音频元素。您的浏览器不支持音频元素。

#### 拼接式（Concatenative）

您的浏览器不支持音频元素。您的浏览器不支持音频元素。

#### WaveNet

您的浏览器不支持音频元素。您的浏览器不支持音频元素。

## 知道该说什么

要用 WaveNet 把文本转换成语音，我们必须告诉它文本是什么。做法是：把文本转换成一个由语言学与语音学特征组成的序列（其中包含当前音素、音节、单词等信息），再把它输入 WaveNet。这意味着网络的预测不仅以前面的音频样本为条件，也以我们希望它说出文本为条件。

如果我们在训练时不提供文本序列，网络仍然会生成语音，但此时它必须自行决定说什么。正如你从下面的样本中听到的那样，这会产生一种类似咿呀学语的效果：真实的词语夹杂着编造出来的、像词一样的音节：

您的浏览器不支持音频元素。您的浏览器不支持音频元素。您的浏览器不支持音频元素。您的浏览器不支持音频元素。您的浏览器不支持音频元素。您的浏览器不支持音频元素。

请注意，WaveNet 有时也会生成非语音的声音，例如呼吸声和嘴部动作；这体现了原始音频模型更大的灵活性。

正如你从这些样本中听到的，单个 WaveNet 能够学会许多不同声音的特征，包括男声和女声。为了确保它知道对任意给定的语句该使用哪种声音，我们以说话人身份为条件来训练网络。有趣的是，我们发现用许多说话人一起训练，比只用该说话人本人单独训练能更好地对其建模，这暗示了一种迁移学习的形式。

通过改变说话人身份，我们可以用 WaveNet 用不同的声音说同一句话：

您的浏览器不支持音频元素。您的浏览器不支持音频元素。您的浏览器不支持音频元素。您的浏览器不支持音频元素。

类似地，我们还可以向模型提供额外的输入，例如情感或口音，让语音更加多样、更有趣。

## 创作音乐

既然 WaveNet 可以用来对任何音频信号建模，我们觉得尝试生成音乐也会很有趣。与 TTS 实验不同，我们没有以一个告诉它该演奏什么的输入序列（例如乐谱）为条件；相反，我们干脆让它自由发挥、想生成什么就生成什么。当我们用一个古典钢琴音乐数据集训练它时，它生成了如下这些迷人的样本：

您的浏览器不支持音频元素。您的浏览器不支持音频元素。您的浏览器不支持音频元素。您的浏览器不支持音频元素。您的浏览器不支持音频元素。您的浏览器不支持音频元素。

WaveNet 为 TTS、音乐生成乃至一般的音频建模开辟了许多可能性。用深度神经网络逐个时间步直接生成 16kHz 音频这件事居然能行得通，本身就令人惊讶，更不用说它还超越了最先进的 TTS 系统。我们很期待接下来能用它做出什么。

**说明**

请阅读论文：[WaveNet: A Generative Model for Raw Audio](https://arxiv.org/pdf/1609.03499.pdf)
