---
title: "Facebook 研究团队在 ICASSP 2020"
title_en: "Facebook Research at ICASSP 2020"
date: 2020-05-01
source: https://ai.facebook.com/blog/facebook-research-at-icassp-2020
crawled: 2026-09-22
translated: 2026-09-22
---

# Facebook 研究团队在 ICASSP 2020

> 原文：[Facebook Research at ICASSP 2020](https://ai.facebook.com/blog/facebook-research-at-icassp-2020) · Meta AI（Wayback 存档）

2020 年 5 月 1 日

Facebook AI 的研究者将于 2020 年 5 月 4 日至 8 日线上出席第 45 届国际声学、语音与信号处理会议（ICASSP）并展示他们的工作。今年，我们在语音识别的主要领域取得了显著进展，涵盖自动语音识别（ASR）的最先进研究（包括基于 Transformer 的模型）、用空间注意力改进远场 ASR、半监督与自监督训练的新技术与资源、面向语音翻译的数据增强、弱标注声学事件检测，以及环境感知的噪声抑制。除了下面的摘要清单，我们还将分享其中三篇论文的细节：我们用基于 Transformer 的混合 ASR 系统刷新了标准 LibriSpeech 基准的纪录；提出了一种利用视频评论与描述作为上下文训练数据的新型半监督预训练方法；并发布了 Libri-Light——一个大型开源数据集，提供三项以自监督为重点的新基准任务。这些只是 Facebook AI 研究者今年在 ICASSP 上展示的部分论文。我们将以视频形式展示被 ICASSP 2020 接收的论文。完整摘要清单见下文，每个视频演示就绪后我们会附上链接。ICASSP 研究展示的逐日完整日程见此处。

## 基于 Transformer 的混合模型

我们新颖的基于 Transformer 的声学模型在 LibriSpeech（语音识别最流行的公开数据集之一）上取得了最低词错误率（WER），使混合系统的性能与端到端替代方案相当。这是一个重要里程碑，因为混合系统是相对成熟的技术，且每天仍在服务数十亿人。这是流行的 Transformer 架构首次成功应用于混合 ASR 的声学建模。优化 ASR Transformer 的若干关键技术包括：用迭代损失训练深度神经网络，以及用卷积方法替代传统正弦位置嵌入来编码必要的位置信息。这两种方法都直接改进了该模型的 WER。在此观看虚拟演示。

## 面向弱监督训练的文本元数据生成

为减少对标注训练数据的需求，我们开发了一种新颖的弱监督训练方法，利用公开视频周边的文本元数据。虽然它们不是语音片段的逐字转录，但作为与音频松散相关的远距标签很有效。我们使用公开视频及随附帖子或评论文本作为线索，训练编码器-解码器 transformer 模型生成会出现在视频中的句子。在 5 万小时公开视频的大规模评估中，我们最佳的编码器-解码器模型相较 1000 小时有监督基线平均降低 20.8% 的 WER，仅使用弱监督编码器组件时平均降低 13.4% 的 WER。

## Libri-Light：有限或无监督数据集

推进语音研究中自监督学习的一大障碍，是缺乏足够的基准与数据集。为帮助加速研究，我们引入了 Libri-Light——最大的语音识别开源数据集。它包含 6 万小时无标注数据、三项新基准任务，以及基线系统与评测。由于 Libri-Light 使用标准 LibriSpeech 作为测试数据集，它是首个能够直接比较使用不同学习技术方法的基准，研究者可以更好地理解自监督学习相对有监督学习性能的进展。你可以进一步了解研究者如何利用这些额外的无标注训练数据，通过自监督表示学习改进语音识别性能。在此观看虚拟演示。

## Facebook 在 ICASSP 2020 上展示的研究完整清单

**极化码的门控超网解码器（A gated hypernet decoder for polar codes）**
Eliya Nachmani、Lior Wolf
超网络（Hypernetworks）近来被证明能改进用于解码纠错码的消息传递算法的性能。在本工作中，我们展示如何通过对极化置信传播解码方案的新形式化，把超网络应用于极化码解码。我们证明该方法改进了神经极化解码器的先前结果，并在大信噪比下取得了与连续列表消除（SCL）方法相同的比特错误率性能——后者已知优于任何置信传播解码器，且非常接近最大似然解码器。在此观看虚拟演示。

**AIPNet：面向端到端语音识别的口音不变网络生成对抗预训练（AIPNet: Generative adversarial pre-training of accent-invariant networks for end-to-end speech recognition）**
Yi-Chen Chen、Zhaojun Yang、Ching-Feng Yeh、Mahaveer Jain、Michael Seltzer
作为语音变异的主要来源之一，口音对语音识别系统的鲁棒性构成了巨大挑战。在本文中，我们的目标是构建一个跨口音泛化良好的统一端到端语音识别系统。为此，我们提出基于生成对抗网络（GAN）的新颖预训练框架 AIPNet，用于口音不变表示学习：口音不变预训练网络。我们在转录未必可得的带口音数据上通过对抗训练，预训练 AIPNet 以从声学特征中解耦口音不变与口音特定特性。我们进一步把口音不变模块与基于注意力的编码器-解码器模型连接并微调，用于多口音语音识别。实验中，我们的方法与包括口音依赖与口音无关模型在内的四个基线比较。九种英语口音上的实验结果表明：当所有口音的转录可得时，所提方法以平均 2.3%～4.5% 的相对 WER 降低胜过所有基线；当仅美式口音转录可得时，相对降低 1.6%～6.1%。在此观看虚拟演示。

**基于 transformer 的神经语言模型适配的实证研究（An empirical study of transformer-based neural language model adaptation）**
Ke Li、Zhe Liu、Tianxing He、Hongzhao Huang、Fuchun Peng、Daniel Povey、Sanjeev Khudanpur
我们探索深度基于 Transformer 的神经语言模型（LM）用于自动语音识别的两种适配方法。第一种是预训练-微调框架：先在大规模文本语料上从头预训练 Transformer LM，再通过微调适配到相对较小的目标域。第二种是分别训练于源域与目标域的模型经动态加权的混合器，旨在用动态加权改进简单线性插值。我们在 Switchboard（SWBD）与《华尔街日报》（WSJ）上把这两种方法与三个基线——不适配、合并数据、简单插值——进行比较。实验表明，混合器模型总体优于基线与微调。与不适配相比，微调与混合器方法在 SWBD 上分别取得最高 11.5% 与 14.1% 的相对 WER 降低。混合器模型也胜过线性插值与合并数据。在 WSJ 上，混合器方法取得了新的最先进 WER 结果。在此观看虚拟演示。

**既视感：深度 Transformer 网络中的双重特征呈现与迭代损失（Deja-vu: Double feature presentation and iterated loss in deep Transformer networks）**
Andros Tjandra、Chunxi Liu、Frank Zhang、Xiaohui Zhang、Yongqiang Wang、Gabriel Synnaeve、Satoshi Nakamura、Geoffrey Zweig
深度声学模型通常在网络第一层接收特征，并在后续层处理越来越抽象的表示。在这里，我们提议在声学模型的多个深度馈入输入特征。我们的动机是让声学模型能够结合部分假设重新审视其输入特征，因此引入了中间模型头与损失函数。我们在深度 Transformer 网络的语境下研究该架构，并对前一层激活与输入特征都使用注意力机制。为训练该模型的中间输出假设，我们在每次特征复用之前的每一层应用目标函数。我们发现，这种迭代损失本身就能显著改进性能，同时也使输入特征复用成为可能。我们在 LibriSpeech 与一个大规模视频数据集上给出结果，LibriSpeech 相对改进 10-20%，视频相对改进 3.2-13%。在此观看虚拟演示。

**自监督预训练对语音识别的有效性（Effectiveness of self-supervised pre-training for speech recognition）**
Alexei Baevski、Michael Auli、Abdelrahman Mohamed
我们比较了显式量化音频数据与不量化学习表示的自监督表示学习算法。我们发现前者更准确，因为它通过 vq-wav2vec 建立了良好的数据词表，使后续 BERT 训练能有效学习表示。与以往工作不同，我们用连接时序分类（CTC）损失直接在转录语音上微调预训练的 BERT 模型，而非把表示送入任务专用模型。我们还提出直接从连续音频数据学习的 BERT 风格模型，并比较了原始音频与频谱特征的预训练。用带 vq-wav2vec 词表的 BERT 模型在 10 小时带标注 LibriSpeech 数据上微调，效果在 test-clean 上几乎与已知的在 100 小时带标注数据上训练的最佳系统相当，同时在 test-other 上降低 25% 的 WER。当只使用 10 分钟标注数据时，test-other 上 WER 为 25.2，test-clean 上为 16.3。这表明自监督可以让语音识别系统在近乎零转录数据上训练。在此观看虚拟演示。

**环境感知的可重构噪声抑制（Environment-aware reconfigurable noise suppression）**
Jun Yang、Joshua Bingham
本文提出一种高效、鲁棒、可重构的技术，为任意采样率抑制多种类型的噪声。理论分析以及主观与客观测试结果表明，所提噪声抑制（NS）方案显著提升了语音传输指数（STI）、语音可懂度（SI）、信噪比（SNR）与主观听感。STI 与 SI 分为五个等级：差、较差、中等、良好、优秀。最常见的噪声条件为 SNR 在 -5 到 8 dB 之间。对输入 SNR 在 -5 到 2.5 dB 之间，所提 NS 把 STI 与 SI 从中等提升到良好；对输入 SNR 在 2.5 到 8 dB 之间，STI 与 SI 从良好提升到优秀。所提 NS 可用于 VoIP、语音唤醒与自动语音识别应用的采集与播放两条通路。

**G2G：面向字形混合 ASR 的 TTS 驱动发音学习（G2G: TTS-driven pronunciation learning for graphemic hybrid ASR）**
Duc Le、Thilo Koehler、Christian Fuegen、Michael Seltzer
基于字素（grapheme）的声学建模近来被证明在混合与端到端自动语音识别（ASR）中都胜过基于音素的方法，即便在英语等非语音文字语言上也是如此。然而，字形 ASR 在不遵循训练中标准拼写规范的低频词（如实体名）上仍有问题。在本工作中，我们提出一种新颖方法，在文本转语音数据上训练统计字素到字素（G2G）模型，把任意字符序列改写为发音上更一致的形式。我们表明，在解码时用 G2G 提供替代发音，相较强字形基线相对降低 3% 到 11% 的词错误率，并在稀有名字识别上追平等效的语音设置。与许多以往方法不同，我们的方法不需要对声学模型训练流程做任何改动。这项工作再次确认了基于字形建模的有效性，并表明在可得时可利用专门的语言学知识改进字形 ASR。在此观看虚拟演示。

**Libri-Light：有限或无监督 ASR 的（大）数据集（Libri-Light: A (large) dataset for ASR with limited or no supervision）**
Jacob Kahn、Morgan Rivière、Weiyi Zheng、Evgeny Kharitonov、Qiantong Xu、Pierre-Emmanuel Mazaré、Julien Karadayi、Vitaliy Liptchinsky、Ronan Collobert、Christian Fuegen、Tatiana Likhomanenko、Gabriel Synnaeve、Armand Joulin、Abdelrahman Mohamed、Emmanuel Dupoux
我们引入一个新的英语口语音频合集，适用于有限或无监督条件下训练语音识别系统。它源自 LibriVox 项目的开源有声书，包含超过 6 万小时音频——据我们所知，这是最大的免费语音语料。音频已用语音活动检测切分，并标注了 SNR、说话人 ID 与体裁描述。此外，我们提供在三种设置下工作的基线系统与评估指标：（1）零资源/无监督设置（ABX）；（2）半监督设置（PER、CER）；（3）远距监督设置（WER）。设置（2）与（3）使用与语音对齐的有限文本资源（10 分钟到 10 小时），设置（3）还使用大量未对齐文本。它们在标准 LibriSpeech 开发与测试集上评估，以便与有监督最先进水平比较。在此观看虚拟演示。

**Lookahead 收敛到光滑非凸函数的驻点（Lookahead converges to stationary points of smooth non-convex functions）**
Jianyu Wang、Vinayak Tantia、Nicolas Ballas、Mike Rabbat
Lookahead 优化器 [Zhang 等，2019] 近来被提出并被证明能改进训练深度神经网络的随机一阶方法的性能。Lookahead 可视为双时间尺度算法：快动态（内层优化器）确定搜索方向，慢动态（外层优化器）沿该方向移动执行更新。我们证明，在适当选择步长的情况下，Lookahead 收敛到光滑非凸函数的驻点。尽管 Lookahead 被描述和实现为串行算法，我们的分析基于把 Lookahead 视为两个周期性通信智能体的多智能体优化方法。在此观看虚拟演示。

**面向 ASR 的高效二遍解码与开放词表词级 RNNLM 重评分的 OOV 恢复（OOV recovery with efficient 2nd pass decoding and open-vocabulary word-level RNNLM rescoring for ASR）**
Xiaohui Zhang、Dan Povey、Sanjeev Khudanpur
在本文中，我们研究混合自动语音识别（ASR）系统中的词表外（OOV）词恢复，重点是面向基于加权有限状态转换器（WFST）解码与词级 RNNLM 重评分的动态词表扩展。我们首先描述基于带音素序列约束的混合词法模型（HLM）的 OOV 候选生成方法。接着，我们引入一个用动态扩展词表高效执行第二遍 OOV 恢复的框架，并表明通过对 OOV 候选的语言模型（LM）分数做校准，相较基于 HLM 的第一遍解码显著改进了 OOV 恢复与整体解码性能。最后，我们提出开放词表词级循环神经网络语言模型（RNNLM）重评分框架，使对包含已恢复 OOV 的 ASR 假设重评分成为可能——用一个训练时对 OOV 一无所知的单一词级 RNNLM。通过在西班牙语/英语 ASR 任务上评估 OOV 恢复与整体解码性能，我们表明所提 OOV 恢复流水线有潜力构成高效的开放词表基于词的 ASR 解码框架，相较标准 WFST 解码与 RNNLM 重评分流水线仅增加极少计算。在此观看虚拟演示。

**用可学习分段特征做音素边界检测（Phoneme boundary detection using learnable segmental features）**
Felix Kreuk、Yaniv Sheena、Joseph Keshet、Yossi Adi
音素边界检测是说话人分离、语音科学、关键词检测等多种语音处理应用的重要第一步。在本工作中，我们提出一个神经架构加上参数化结构化损失函数，为音素边界检测任务学习分段表示。首先，我们在不给定所说音素作为输入的情况下评估模型。TIMIT 与 Buckeye 语料上的结果表明，所提模型优于基线模型，在 F1 与 R 值上达到最先进性能。我们进一步探索用音标转写作为额外监督，表明这带来轻微的性能改进但收敛速率大幅改善。我们还在一个希伯来语语料上评估模型，证明这种语音监督在多语言设置中是有益的。在此观看虚拟演示。

**SeCoST：面向弱标注声学事件检测的顺序协同监督（SeCoST: Sequential co-supervision for weakly labeled audio event detection）**
Anurag Kumar、Vamsi Krishna Ithapu
弱监督学习算法对于把声学事件检测扩展到数百个声音类别至关重要。这类学习模型不仅要以最少的类别专属标注高效消歧声音事件，还要对标签噪声鲁棒——弱标签下噪声比强标注更明显。在本工作中，我们通过融合序列学习与知识蒸馏的思想，提出一个设计弱监督学习模型的新框架。我们把所提方法称为 SeCoST（读作「sequest」）——训练世代学生的顺序协同监督。SeCoST 通过新颖的知识转移方法增量构建学生-教师对级联。我们在 Audioset（现有最大的弱标注数据集）上的评估表明，SeCoST 取得 0.383 的平均精度均值，大幅胜过此前最先进水平。在此观看虚拟演示。

**面向端到端语音识别的自训练（Self-training for end-to-end speech recognition）**
Jacob Kahn、Ann Lee、Awni Hannun
我们在端到端语音识别的语境下重新审视自训练。我们证明，用伪标签训练可以大幅改进基线模型的精度。我们的方法使用一个用于生成伪标签的强基线声学与语言模型、针对序列到序列模型常见错误定制的过滤机制，以及一种增加伪标签多样性的新颖集成方法。LibriSpeech 语料上的实验表明：结合四个模型的集成与标签过滤，在带噪语音设置下自训练相较在 100 小时带标注数据上训练的基线取得 33.9% 的相对 WER 改进。在干净语音设置下，自训练恢复了基线与 oracle 模型之间差距的 59.3%，至少比以往方法能达成的高出 93.8%（相对值）。

**SkinAugment：面向自动语音翻译的自编码说话人转换（SkinAugment: Auto-encoding speaker conversions for automatic speech translation）**
Aray D. McCarthy、Liezl Puzon、Juan Pino
我们提出面向自动语音翻译（AST）训练数据增强的自编码说话人转换技术。该技术直接变换音频序列，使合成的音频听起来像另一位说话人的声音。在英语-法语与英语-罗马尼亚语自动语音翻译任务以及低资源英语自动语音识别（ASR）任务上，我们的方法表现优于 SpecAugment。此外，消融实验显示了增强数据在数量与多样性上的双重益处。最后，我们表明可以把该方法与机器翻译转录增强相结合，得到有竞争力的端到端 AST 模型，在英语-法语 AST 任务上胜过一个非常强的级联模型。我们的方法足够通用，可应用于其他语音生成与分析任务。在此观看虚拟演示。

**用深度波束形成神经网络做远场语音识别的空间注意力（Spatial attention for far-field speech recognition with deep beamforming neural networks）**
Weipeng He、Lu Lu、Biqiao Zhang、Jay Mahadeokar、Kaustubh Kalgaonkar、Christian Fuegen
在本文中，我们引入空间注意力，用于精化多方向神经波束形成器中的信息，以服务远场自动语音识别。以往具有多个注视方向的神经波束形成器方法（如分解复线性投影）已显示有前景的结果。然而这类方法提取的特征含有冗余信息，因为只有目标语音的方向是相关的。我们提议用空间注意力子网为来自不同方向的特征加权，使后续声学模型能聚焦于与语音识别最相关的特征。实验结果表明，空间注意力相较无注意力的方法最高带来 9% 的相对词错误率改进。在此观看虚拟演示。

**通过生成上下文信息训练 ASR 模型（Training ASR models by generation of contextual information）**
Kritika Singh、Dmytro Okhonko、Jun Liu、Yongqiang Wang、Frank Zhang、Ross Girshick、Sergey Edunov、Fuchun Peng、Yatharth Saraf、Geoffrey Zweig、Abdelrahman Mohamed
有监督 ASR 模型的精度已达到前所未有的水平，部分得益于不断增长的带标注训练数据。然而在许多应用与地区，只有中等规模的数据可用，这推动了半监督与弱监督学习研究的兴起。在本文中，我们用松散相关的上下文信息作为真值标签的替代，对弱监督学习在语音识别中的有效性进行大规模评估。弱监督训练中，我们使用 5 万小时公开英语社交媒体视频及其相应标题与帖子文本，训练编码器-解码器 Transformer 模型。我们最佳的编码器-解码器模型相较 1000 小时有监督基线平均降低 20.8% 的 WER，仅使用弱监督编码器做 CTC 微调时平均降低 13.4%。结果表明，我们的弱监督设置同时改进了编码器声学表示与解码器语言生成能力。在此观看虚拟演示。

**面向混合语音识别的基于 Transformer 的声学建模（Transformer-based acoustic modeling for hybrid speech recognition）**
Yongqiang Wang、Abdelrahman Mohamed、Duc Le、Chunxi Liu、Alex Xiao、Jay Mahadeokar、Hongzhao Huang、Andros Tjandra、Xiaohui Zhang、Frank Zhang、Christian Fuegen、Geoffrey Zweig、Michael L. Seltzer
我们提出并评估面向混合语音识别的基于 Transformer 的声学模型（AM）。本工作讨论了若干建模选择，包括多种位置嵌入方法以及支持训练深度 Transformer 的迭代损失。我们还展示了在 Transformer 模型中使用有限右侧上下文的初步研究，使其可用于流式应用。我们证明，在广泛使用的 LibriSpeech 基准上，使用标准 n-gram 语言模型（LM）时，我们基于 Transformer 的 AM 比已发表的最佳混合结果相对高出 19% 到 26%。结合神经网络 LM 重评分，我们的方法在 LibriSpeech 上取得最先进结果。我们的发现也在一个大得多的内部数据集上得到确认。在此观看虚拟演示。

**无监督预训练跨语言良好迁移（Unsupervised pretraining transfers well across languages）**
Morgane Rivière、Armand Joulin、Pierre-Emmanuel Mazaré、Emmanuel Dupoux
自动语音识别（ASR）的跨语言与多语言训练在有监督设置下已被广泛研究，这假设存在语音与正字法转录的平行语料。近来，对比预测编码（CPC）算法被提出用于用无标注数据预训练 ASR 系统。在本工作中，我们研究无监督预训练是否跨语言良好迁移。我们表明，对 CPC 预训练稍作修改即可提取能良好迁移到其他语言的特征，与有监督预训练相当甚至更优。这显示了无监督方法对语言资源稀缺语言的潜力。在此观看虚拟演示。
