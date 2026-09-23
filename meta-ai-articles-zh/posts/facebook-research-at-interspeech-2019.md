---
title: "Facebook 研究团队在 Interspeech 2019"
title_en: "Facebook research at Interspeech 2019"
date: 2019-03-15
source: https://ai.facebook.com/blog/facebook-research-at-interspeech-2019
crawled: 2026-09-22
translated: 2026-09-22
---

# Facebook 研究团队在 Interspeech 2019

> 原文：[Facebook research at Interspeech 2019](https://ai.facebook.com/blog/facebook-research-at-interspeech-2019) · Meta AI（Wayback 存档）

Facebook AI 与语音及语言研究社区的其他成员将于 9 月 15 日（周日）至 19 日（周四）齐聚奥地利格拉茨，参加国际语音通信协会第 20 届年会（Interspeech）。Interspeech约有 2000 名参会者，被视为世界上最大、最全面的口语处理科学与技术会议。整个会议期间，Facebook AI 的语音与自然语言处理（NLP）研究者将在海报环节与口头报告中展示最新工作，包括歌唱声音转换的新深度学习方法、免词典语音识别、训练语音识别模型的新自监督方法，以及面向上下文端到端 ASR 的字素与音素联合嵌入研究。

Facebook 的语音团队有两大方向：人机交互与语音界面，以及视频内容理解。软件工程经理 Christian Fuegen 鼓励博士生与业界专业人士到 F7 展位了解 Facebook 语音团队的工作。「我们始终希望与语音研究社区保持联系，」他说，「无法参加 Interspeech 的人，请通过社交媒体保持联系。」Facebook Research 有多个沟通渠道，包括 Twitter 和 Facebook 上的 @facebookai 以及 Facebook 上的 @academics。有兴趣进一步了解 Facebook 语音研究的博士生，还可以申请口语处理与音频分类方向的 Facebook 奖学金。获奖者将被邀请参加年度峰会，进一步了解 Facebook 的研究。申请截止日期为 10 月 4 日太平洋标准时间 23:59。要查看 Facebook 在 Interspeech 的论文与其他活动日程（含报告地点与招聘信息），请点击此处。

## Facebook 在 Interspeech 上展示的研究

**面向上下文端到端 ASR 的字素与音素联合嵌入（Joint Grapheme and Phoneme Embeddings for Contextual End-to-End ASR）**
Zhehuai Chen、Mahaveer Jain、Michael L. Seltzer、Yongqiang Wang、Christian Fuegen
Listen-Attend-Spell（LAS）等端到端自动语音识别方法，把传统语音识别器的所有组件融合进统一模型。虽然这简化了训练与解码流水线，但当训练与测试数据存在失配（尤其当该信息动态变化）时，统一模型难以适配。上下文 LAS（CLAS）框架试图通过把上下文实体编码为定长嵌入、并利用注意力机制建模这些实体出现的概率来解决该问题。在本工作中，我们通过提出若干提取上下文实体嵌入的新策略来改进 CLAS 方法。我们比较了基于字素与音素输入和/或输出序列的嵌入提取器，表明联合面向字素与音素训练的编码器-解码器模型优于其他方法。利用音素信息对书写相近的字素序列获得更好的判别性，也有助于模型更好地泛化到训练中未见过的字素序列。我们展示了相较原始 CLAS 方法的显著改进，并证明所提方法在多个领域的大量上下文实体上扩展性更好。

**用时间-深度可分离卷积做序列到序列语音识别（Sequence-to-Sequence Speech Recognition with Time-Depth Separable Convolutions）**
Awni Hannun、Ann Lee、Qiantong Xu、Ronan Collobert
我们提出一个带简单高效解码器的全卷积序列到序列编码器架构。我们的模型在 LibriSpeech 上改进了 WER，同时比强 RNN 基线高效一个数量级。方法的关键是时间-深度可分离卷积块，它大幅减少模型参数量，同时保持感受野较大。我们还给出一个稳定高效的束搜索推断流程，使我们能有效集成语言模型。结合卷积语言模型，我们的时间-深度可分离卷积架构在带噪 LibriSpeech 测试集上，比此前已报告的最佳序列到序列结果相对改进超过 22% 的 WER。

**无监督歌唱声音转换（Unsupervised Singing Voice Conversion）**
Eliya Nachmani、Lior Wolf
我们提出一种歌唱声音转换的深度学习方法。所提网络不以文本或音符为条件，直接把一位歌手的音频转换为另一位歌手的声音。训练完全不带任何监督：没有歌词或任何音素特征、没有音符、也没有歌手之间的匹配样本。所提网络对所有歌手使用单个 CNN 编码器、单个 WaveNet 解码器，以及一个强制潜在表示与歌手无关的分类器。每位歌手用一个嵌入向量表示，解码器以它为条件。为应对相对较小的数据集，我们提出新的数据增强方案，以及基于回译的新训练损失与协议。我们的评估提供的证据表明，转换产生自然且高度可辨识为目标歌手的歌声。

**wav2vec：面向语音识别的无监督预训练（wav2vec: Unsupervised Pre-training for Speech Recognition）**
Steffen Schneider、Alexi Baevski、Ronan Collobert、Michael Auli
我们通过学习原始音频的表示来探索语音识别的无监督预训练。wav2vec 在大量无标注音频数据上训练，所得表示随后用于改进声学模型训练。我们预训练一个通过噪声对比二分类任务优化的简单多层卷积神经网络。我们在 WSJ 上的实验表明，当只有几小时转录数据可用时，强字符级 log-mel 滤波器组基线的 WER 最高降低 36%。我们的方法在 nov92 测试集上达到 2.43% 的 WER，胜过文献中已报告的最佳字符级系统 Deep Speech 2，而使用的带标注训练数据少两个数量级。

**谁需要词？免词典语音识别（Who Needs Words? Lexicon-Free Speech Recognition）**
Tatiana Likhomanenko、Gabriel Synnaeve、Ronan Collobert
免词典语音识别天然处理词表外（OOV）词的问题。在本文中，我们表明字符级语言模型（LM）在语音识别上可以取得与词级 LM 相当的词错误率（WER），即便不把解码限制在词典内。我们研究字符级 LM，表明卷积 LM 能有效利用大（字符）上下文——这是下游良好语音识别性能的关键。我们特别表明，在含 OOV 词的话语上，使用字符级 LM 的免词典解码性能（WER）优于基于词典的解码（无论字符还是词级 LM）。

## Interspeech 2019 的其他活动

**2019 零资源语音挑战赛：没有 T 的 TTS**
组织委员会：Robin Algayres、Juan Benjumea、Mathieu Bernard、Laurent Besacier、Alan W. Black、Xuan-Nga Cao、Charlotte Dugrain、Ewan Dunbar、Emmanuel Dupoux、Julien Karadayi、Lucie Miskic、Lucas Ondel、Sakriani Sakti
