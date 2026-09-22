---
title: "MiMo-Audio：音频语言模型是少样本学习者"
title_en: "MiMo-Audio: Audio Language Models are Few-Shot Learners"
arxiv: 2512.23808
date: 2025-12-29
source: https://arxiv.org/abs/2512.23808
crawled: 2026-09-22
translated: 2026-09-22
---

# MiMo-Audio：音频语言模型是少样本学习者

> 原文：[MiMo-Audio](https://arxiv.org/abs/2512.23808) · 小米 MiMo arXiv

小米 LLM-Core

###### 摘要

现有音频语言模型通常依赖任务特定的微调来完成特定音频任务。相比之下，人类仅凭少量示例或简单指令就能泛化到新的音频任务。
GPT-3 已经证明，扩展 next-token 预测预训练可以在文本领域带来强大的泛化能力，我们相信这一范式同样适用于音频领域。
通过将 MiMo-Audio 的预训练数据扩展到一亿小时以上，我们观察到在多样化的音频任务上涌现出少样本学习能力。
我们对这些能力进行了系统评测，发现 MiMo-Audio-7B-Base 在开源模型中于语音智能与音频理解基准上均取得 SOTA 性能。
在标准指标之外，MiMo-Audio-7B-Base 还能泛化到训练数据中不存在的任务，例如语音转换（voice conversion）、风格迁移与语音编辑。
MiMo-Audio-7B-Base 还展现出强大的语音续写能力，能够生成高度逼真的脱口秀、朗诵、直播与辩论。
在后训练阶段，我们策展了多样化的指令微调语料，并将思考（thinking）机制引入音频理解与生成。
MiMo-Audio-7B-Instruct 在音频理解基准（MMSU、MMAU、MMAR、MMAU-Pro）、语音对话基准（Big Bench Audio、MultiChallenge Audio）与指令 TTS 评测上取得开源 SOTA，接近或超越闭源模型。
模型检查点与完整评测套件可在 <https://github.com/XiaomiMiMo/MiMo-Audio> 获取。

  

图 1：预训练中的涌现行为及与 SOTA 模型的性能对比。

## 1 引言

人类语音交互以其非凡的灵活性与多样性为特征。
个体通过整合大量上下文因素——如说话人、口音、环境与社交场合——来形成对语音的理解，同时根据自身内部状态（如情绪、意图与身体状况）调节自己的声音表达，如语气与韵律（[Sumner, 2011](#bib.bib42)；[Lehet and Holt, 2020](#bib.bib43)；[Bradlow and Bent, 2008](#bib.bib45)）。
这种适应能力迅速而动态，例如，人类在安静的图书馆里会自然压低声音，而在激烈的辩论中会随情境变化提高音量。
相比之下，现有音频语言模型在理解与生成上缺乏这种固有的声音智能与泛化能力（[Zhang et al., 2023a](#bib.bib48)；[Défossez et al., 2024](#bib.bib13)；[KimiTeam et al., 2025](#bib.bib15)；[Wu et al., 2025](#bib.bib17)）。
要完成一系列语音任务，包括语音对话、语音翻译与语音风格迁移，这些模型仍需用任务特定的数据集进行微调。

GPT-3（[Brown et al., 2020b](#bib.bib44)）的成功已经证明，以 next-token 预测范式扩展预训练，是在文本领域实现任务泛化的一条可行路径。
我们假设这一原理可以延伸到语音领域：用 next-token 预测目标在海量语音语料上进行预训练，可以赋予模型跨广泛语音任务的强泛化能力。
尽管先前的工作已探索过面向语音的 next-token 预测预训练（[Borsos et al., 2023](#bib.bib49)；[Zhang et al., 2023a](#bib.bib48)；[Défossez et al., 2024](#bib.bib13)；[Zeng et al., 2024](#bib.bib46)；[Li et al., 2025](#bib.bib30)），这些模型都未能实现对通用语音任务的广泛、通用化泛化（[Fang et al., 2025](#bib.bib50)；[Xu et al., 2025](#bib.bib16)；[KimiTeam et al., 2025](#bib.bib15)；[Wu et al., 2025](#bib.bib17)；[Goel et al., 2025](#bib.bib60)）。

我们认为，面向语音的 next-token 预测预训练有两个关键方面。
其一是让语音信息无损流动的架构。
为充分释放 next-token 预测范式的潜力，我们希望语音信号中的全部信息都能在模型中流通。
这意味着我们不能使用会带来副语言信息损失的语音表示，这使我们的方法有别于当前的主流方案（[Zeng et al., 2024](#bib.bib46)；[KimiTeam et al., 2025](#bib.bib15)；[Wu et al., 2025](#bib.bib17)）。
第二个方面是规模化。
我们相信持续扩大预训练数据的规模会带来持续的性能提升与意想不到的涌现能力（[Wei et al., 2022a](#bib.bib51)）。
因此，我们将训练数据扩展到一亿小时以上，比现有最大开源语音模型所用的数据高出一个数量级。
这一预训练的目标是赋予模型在语音领域的任务泛化能力，即模型在训练时发展出一组广泛的原子技能，然后在推理时利用这些能力快速适应或识别任何语音任务。
我们预训练方法的指导原则是：确保语音信号中的所有信息都被保留并在模型架构中流动。

- •

  分词器（Tokenizer）：我们认为音频分词器的首要标准是重建保真度，且其 token 应适合下游语言建模。为此，我们提出 MiMo-Audio-Tokenizer。这一 12 亿参数模型采用基于 Transformer 的架构，包含编码器、离散化层与解码器，以 25Hz 帧率运行，通过 8 层残差向量量化（RVQ）每秒生成 200 个 token。通过整合语义与重建目标，我们在 1000 万小时语料上从零开始训练它，在重建质量上取得卓越表现，并便于下游语言建模。
- •

  架构：为提升对高 token 率（每秒 200 个 token）序列的建模效率，并缓解语音与文本模态之间的长度差异，我们提出一种结合 patch 编码器、LLM 与 patch 解码器的新架构。patch 编码器将连续四个时间步的 RVQ token 聚合为单个 patch，把序列下采样为 6.25Hz 表示送入 LLM。随后，patch 解码器自回归地生成完整的 25Hz RVQ token 序列。
- •

  训练：为实现理解与生成的统一预训练范式并赋予模型高级声音智能，我们设计了以 MiMo-7B-Base（[Xiaomi, 2025](#bib.bib12)）初始化的两阶段训练策略。阶段 1 专注于语音理解，阶段 2 在统一框架中同时整合理解与生成。每个阶段都有量身定制的训练任务。值得注意的是，我们在这一过程中观察到语音上下文学习能力的自发涌现。
- •

  数据：我们已将预训练语料扩展到前所未有的超过 1 亿小时语音数据，相对任何现有开源语音模型都是数量级的提升。这得益于一条专门构建的端到端数据管线，用于预处理、标注与筛选。
- •

  评测：我们开发了一套综合基准，以严格评估模型在语音领域的上下文学习能力。该基准旨在评估多个层面，包括模态不变的通用知识、听觉理解与推理，以及多样的语音到语音生成任务。

经过大规模预训练，MiMo-Audio-7B-Base 展现出强大的少样本学习能力（[Brown et al., 2020a](#bib.bib10)）。
在我们构建的 SpeechMMLU（源自 MMLU（[Hendrycks et al., 2021](#bib.bib11)），通过将其任务合成为语音构建而成）上评测时，它表现出极高的「语音智能」与强大的模态对齐。
MiMo-Audio-7B-Base 在语音输入与输出下均取得卓越性能，结果紧逼基于文本的 MMLU，且文本性能只有轻微退化。
它还对未见任务展现出出色泛化：只需上下文中给出少量示例，它就能完成语音转换、风格迁移、语速控制、去噪与语音翻译等任务。
此外，MiMo-Audio-7B-Base 展示出强大的语音续写能力，能以脱口秀、演讲、辩论、播客与游戏解说等形式，生成高度逼真且语义连贯的独白或多说话人对话。

我们相信，后训练的核心目标是让模型预训练获得的泛化能力与指令遵循能力对齐。
为此，我们通过聚合覆盖多个领域的高质量开源与内部数据，为音频理解与生成构建了高度多样化的指令微调语料。
为进一步增强模型的跨模态推理能力，我们还为音频理解与生成任务创建了高质量的「思考」（[Wei et al., 2022b](#bib.bib56)，思维链；）数据。
为获得拟人且风格可控的语音对话数据，我们在超过 700 万小时数据上训练了 MiMo-TTS-7B，将基于文本的对话转换为语音。
MiMo-Audio-7B-Instruct 在后训练后展现出卓越的音频理解与推理能力。
它在 MMSU（[Wang et al., 2025](#bib.bib23)）、
MMAU（[Sakshi et al., 2025](#bib.bib24)）、MMAR（[Ma et al., 2025](#bib.bib25)）与 MMAU-Pro（[Kumar et al., 2025](#bib.bib26)）等音频理解/推理基准上取得开源模型中的 SOTA 结果，接近或超越闭源模型的性能。
MiMo-Audio-7B-Instruct 还展现出卓越的语音智能与指令遵循能力，在 Big Bench Audio 与 MultiChallenge Audio（[Sirdeshmukh et al., 2025](#bib.bib27)）等语音对话基准上显著超越其他开源模型。
在指令遵循 TTS 任务上，其性能与 GPT-4o-mini-tts 相当。

我们的主要贡献如下：

- •

  我们提供了首个实证证据：将无损、基于压缩的语音预训练扩展到前所未有的 1 亿小时，可解锁涌现的任务泛化，其标志是强大的少样本学习能力。我们认为这代表着语音领域的「GPT-3 时刻」。
- •

  我们提出了首个全面且可复现的生成式语音预训练蓝图，包括一个新颖的分词器、一个可扩展的架构、一个分阶段训练策略与一套完整的评测套件。
- •

  我们率先将思考（thinking）融入语音理解与生成双方的建模过程，弥合感知与复杂认知任务之间的鸿沟。

## 2 模型架构

### 2.1 MiMo-Audio-Tokenizer

现有音频分词方法的一个主要难题在于有效平衡音频信号中语义信息与声学信息的固有取舍。
语义 token 通常来自自监督学习模型（[Hsu et al., 2021](#bib.bib28)；[Chung et al., 2021](#bib.bib29)；[Zhang et al., 2023c](#bib.bib31)）或 ASR 模型（[Zeng et al., 2024](#bib.bib46)；[Li et al., 2025](#bib.bib30)），与语言内容强相关，便于与文本模态对齐。
然而其主要缺点是丢失细粒度声学信息，制约了原始波形重建的质量。
相比之下，由神经音频编解码器（[Zeghidour et al., 2021](#bib.bib32)；[Défossez et al., 2022a](#bib.bib33)）生成的声学 token 能够实现高保真音频重建，却难以与文本语义空间建立有效对齐。

为了同时捕获语义与声学信息，先前的工作如 SpeechTokenizer（[Zhang et al., 2023b](#bib.bib34)）与 Mimi（[Défossez et al., 2024](#bib.bib13)）尝试将语义蒸馏策略纳入神经音频编解码器以获得统一音频 token。
然而，受限于编码器规模有限，这些方法难以完全化解语义与声学信息的冲突，其语义表达能力仍逊于语义 token。
另一些方法，如 X-Codec（[Ye et al., 2025a](#bib.bib36)）与 XY-Tokenizer（[Gong et al., 2025](#bib.bib35)），采用带独立语义与声学编码器的双流架构来缓解这些问题。
但这些方法仍依赖预训练的语义模型，且其双编码器架构导致语义与声学信息来自彼此分离的表示空间。

为解决这些局限，我们提出 MiMo-Audio-Tokenizer——一个从零开始训练的统一分词器，既能捕获语义信息，又能实现高保真音频重建。
通过扩大模型参数与训练数据，MiMo-Audio-Tokenizer 进一步缓解了语义-声学表示冲突，从而同时增强跨模态对齐与语音重建质量。

![Refer to caption](2512.23808v1/SLMTokenizer.png)

图 2：
MiMo-Audio-Tokenizer 框架示意图。

#### 2.1.1 架构

如图 [2](#S2.F2) 所示，MiMo-Audio-Tokenizer 的架构包含四个主要组件：音频编码器、离散化模块、音频解码器与声码器。
音频编码器由一个带双向注意力的中央 Transformer 编码器构成，输入输出两端各配 2×2\times 下采样层。
中央编码器有 32 层、20 个注意力头，采用旋转位置编码（[Su et al., 2024](#bib.bib40)，RoPE；）与 GELU 激活（[Hendrycks and Gimpel, 2016](#bib.bib41)）。
我们将模型维度设为 1280，FFN 内部维度设为 5120。
为缓解语义与声学信息之间的冲突，我们将第 3 层隐藏状态通过逐元素求和加到最终层输出上。
离散化模块是一个 20 层的残差向量量化器（[van den Oord et al., 2018](#bib.bib4)；[Zeghidour et al., 2021](#bib.bib32)，RVQ；），其中前两层码本大小为 1024，其余层使用 128。
音频解码器采用与编码器镜像的结构，但使用因果自注意力以支持流式生成。
声码器沿用 Vocos 设计（[Siuzdak, 2024](#bib.bib3)），但将 ConvNeXt（[Liu et al., 2022](#bib.bib2)）骨干替换为 Transformer，从而支持序列打包（packing）以获得更高效的训练。
该 Transformer 有 16 层、16 个头，模型维度 256，FFN 维度 1024。
它引入 RoPE 与窗口大小为 [40, 10] 的滑动窗口注意力，为声码器提供 [6.4s, 1.6s] 的感受野。

给定一段以 24 kHz 采样的单声道音频波形 $X$，我们首先将其转换为帧率为 100 Hz 的梅尔频谱。
该频谱随后被送入音频编码器，转换成长度为 $M$、帧率 25 的连续表示序列。
离散化模块中的 RVQ 随后将这些连续表示量化为离散索引的二维矩阵 $A\in\mathbb{N}^{M\times R}$，其中 $R$ 为 RVQ 层数。
这些索引随后通过查找并求和码本中相应的嵌入，重建出量化表示 $\mathbf{Q}$。
最后，音频解码器与声码器从 $\mathbf{Q}$ 重建音频波形 $\hat{X}$。

#### 2.1.2 训练

受 Wu et al. (2023) 启发，我们采用两阶段训练范式以提升训练效率，如图 [2](#S2.F2) 所示。
在阶段 1，模型在大规模数据集上进行多任务学习。
具体而言，我们将训练数据扩展到超过 1100 万小时。
这一充分训练使模型能够联合编码语义与声学信息。
在阶段 2，音频编码器与离散化模块的参数被冻结。
我们引入判别器来训练音频解码器与声码器，专注于改善原始音频波形中细粒度细节的重建并消除声码化伪影。

##### 统一表示学习

在阶段 1，我们结合音频重建任务与音频到文本（A2T）任务，在对齐音频与文本表示空间的同时确保声学信息的保留。
为给 A2T 目标提供监督，我们引入一个与 MiMo-Audio-Tokenizer 联合训练的 LLM。
MiMo-Audio-Tokenizer 与 LLM 的所有参数均从零开始训练。
我们将 A2T 目标表述为作用于 LLM 文本输出的 next-token 预测损失，定义为：

$$
\mathcal{L}_{\text{A2T}}=-\sum_{i=1}^{N}\log{p(t_{i}|\tilde{\mathbf{Q}},t_{1},\dots,t_{i-1})}, \tag{1}
$$

其中 $T=[t_{1},\dots,t_{N}]$ 为目标文本序列，$\tilde{\mathbf{Q}}$ 为量化后的音频表示，$N$ 为文本序列总长。

对于音频重建任务，我们采用多尺度梅尔频谱重建损失，定义为 $L1$ 距离：

$$
\mathcal{L}_{\text{recon}}=\sum_{i\in e}\lVert\mathcal{S}_{i}(X)-\mathcal{S}_{i}(\hat{X})\lVert_{1}, \tag{2}
$$

其中 $\mathcal{S}_{i}$ 表示尺度为 $i$、带 $2^{i}$ 个频带的梅尔频谱，使用窗口大小为 $15\cdot 2^{i-1}$、跳跃长度为 $15\cdot 2^{i-2}$ 的归一化短时傅里叶变换（STFT）计算。
尺度集合定义为 $e=\{5,6,7\}$。最后，加上来自离散化模块的承诺损失 $\mathcal{L}_{\text{commit}}$，阶段 1 的总损失为加权求和：

$$
\mathcal{L}_{\text{stage1}}=\lambda_{\text{A2T}}\mathcal{L}_{\text{A2T}}+\lambda_{\text{recon}}\mathcal{L}_{\text{recon}}+\lambda_{\text{commit}}\mathcal{L}_{\text{commit}}, \tag{3}
$$

其中 $\lambda_{\mathrm{A2T}}{=}10.0,\;\lambda_{\mathrm{recon}}{=}1.0,\;\lambda_{\mathrm{commit}}{=}1.0$。

##### 对抗微调

在阶段 2，我们引入额外的判别器进行对抗训练，以改善波形重建质量。
在此阶段，所有参与音频分词过程的参数都被冻结，以保留音频 token 空间的语义结构。
我们采用多任务 GAN 训练配方，联合优化：(i) 阶段 1 的梅尔频谱重建损失，(ii) 对抗损失，(iii) 判别器特征匹配损失。
为在时域与频域同时提供监督，我们采用多周期判别器（[Kong et al., 2020](#bib.bib8)，MPD；）与多尺度 STFT 判别器（[Défossez et al., 2022b](#bib.bib7)，MS-STFT；）。
我们采用 Hinge-GAN（[Lim and Ye, 2017](#bib.bib5)；[Miyato et al., 2018](#bib.bib6)）训练框架，对所有判别器层施加谱归一化，并在判别器训练期间禁用权重衰减。
令 $\mathcal{D}=\{D_{k}\}_{k=1}^{K}$ 表示 MPD 与 MS-STFT 中全部子判别器的集合。
给定真实波形 $X$ 与生成波形 $\hat{X}$，判别器目标可表述为

$$
\mathcal{L}_{D}=\frac{1}{K}\sum_{k=1}^{K}\Big[\mathbb{E}_{X}\big[\max(0,\,1-D_{k}(X))\big]+\mathbb{E}_{\hat{X}}\big[\max(0,\,1+D_{k}(\hat{X}))\big]\Big], \tag{4}
$$

生成器的对抗目标为

$$
\tilde{\mathcal{L}}_{\mathrm{adv}}=-\,\frac{1}{K}\sum_{k=1}^{K}\mathbb{E}_{\hat{X}}\big[D_{k}(\hat{X})\big], \tag{5}
$$

其中以 $\tfrac{1}{K}$ 归一化可防止子判别器数量主导优化。
对于特征匹配，我们最小化判别器中间激活之间的 $\ell_{1}$ 距离：

$$
\mathcal{L}_{\mathrm{fm}}=\frac{1}{K}\sum_{k=1}^{K}\frac{1}{L_{k}}\sum_{\ell=1}^{L_{k}}\big\|f_{k,\ell}(X)-f_{k,\ell}(\hat{X})\big\|_{1}, \tag{6}
$$

其中 $f_{k,\ell}(\cdot)$ 返回 $D_{k}$ 的第 $\ell$ 层特征，$L_{k}$ 表示所纳入中间层的数量。
在构成复合目标时，我们为各单独损失分配固定权重，以保持它们的梯度幅度处于可比的量级。
生成器以如下目标训练

$$
\mathcal{L}_{G}=\lambda_{\mathrm{recon}}\,\mathcal{L}_{\mathrm{recon}}+\lambda_{\mathrm{adv}}\,\tilde{\mathcal{L}}_{\mathrm{adv}}+\lambda_{\mathrm{fm}}\,\mathcal{L}_{\mathrm{fm}},\quad \tag{7}
$$

其中 $\lambda_{\mathrm{recon}}{=}1.0,\;\lambda_{\mathrm{adv}}{=}1.0,\;\lambda_{\mathrm{fm}}{=}2.0$。

#### 2.1.3 评测

##### 设置

我们用多项指标评估音频分词对声学信息的保留。
这些指标包括：说话人相似度（SIM），以预训练说话人验证模型嵌入的余弦相似度计算（https://github.com/microsoft/UniSpeech/tree/main/downstreams/speaker_verification）；短时客观可懂度（[Taal et al., 2010](#bib.bib38)，STOI；）；以及语音质量感知评估（[Rix et al., 2001](#bib.bib39)，PESQ；）。
所有评测在 Seed-TTS-Eval（[Anastassiou et al., 2024](#bib.bib57)）的真值录音上进行。
对比基线包括 GLM-4-Voice-Tokenizer（[Zeng et al., 2024](#bib.bib46)）、Baichuan-Audio-Tokenizer（[Li et al., 2025](#bib.bib30)）、XY-Tokenizer（[Gong et al., 2025](#bib.bib35)）、Mimi（[Défossez et al., 2024](#bib.bib13)）、XCodec（[Ye et al., 2025b](#bib.bib1)）与 BigCodec（[Xin et al., 2024](#bib.bib47)）。
考虑到下游的 MiMo-Audio 仅使用 MiMo-Audio-Tokenizer 前 8 个码本产生的音频 token 训练，我们评测并比较仅用这些码本解码的波形重建质量。
该协议忠实反映了下游语言模型可访问音频的保真度。
为保持一致，我们在同一协议下评测 Mimi。

##### 结果

如表 [1](#S2.T1) 所示，MiMo-Audio-Tokenizer 在 Seed-TTS-Eval 上交付了强劲的重建质量。
在中文与英文两个 split 上，它在 PESQ-NB/WB、SIM 与 STOI 上均取得最高分，在相近比特率下大幅超越所有基线。
关键在于，这些增益恰好是在用于下游建模的码本上测得的，表明 MiMo-Audio 保留了语音信息的全部保真度，进而在多样语音任务上带来强泛化。

| 系统 | kBPS | SEED-ZH：PESQ-NB | PESQ-WB | SIM | STOI | SEED-EN：PESQ-NB | PESQ-WB | SIM | STOI |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MiMo-Audio-Tokenizer | 1.55 | **3.30** | **2.71** | **0.89** | **0.93** | **3.02** | **2.43** | **0.85** | **0.92** |
| GLM-4-Voice-Tokenizer | 0.175 | 1.11 | 1.06 | 0.33 | 0.61 | 1.11 | 1.05 | 0.12 | 0.60 |
| Baichuan-Audio-Tokenizer | 1.0 | 2.37 | 1.84 | 0.78 | 0.86 | 2.11 | 1.62 | 0.69 | 0.85 |
| XY-Tokenizer | 1.0 | 2.88 | 2.24 | 0.87 | 0.90 | 2.69 | 2.14 | 0.82 | 0.90 |
| Mimi | 1.1 | 2.57 | 2.05 | 0.73 | 0.88 | 2.60 | 2.07 | 0.74 | 0.89 |
| XCodec2.0 | 0.8 | 2.69 | 2.10 | 0.81 | 0.89 | 2.57 | 2.01 | 0.78 | 0.89 |
| BigCodec | 1.04 | 2.88 | 2.26 | 0.80 | 0.91 | 2.80 | 2.22 | 0.80 | 0.91 |

表 1：音频分词器在 Seed-TTS-Eval 数据集上的评测。每个系统的中/英文（ZH/EN）split 结果列于同一行。kBPS 表示分词后音频流的有效比特率（千比特每秒）。

### 2.2 MiMo-Audio

图 3：
MiMo-Audio 模型架构。

MiMo-Audio 是一个统一的生成式音频语言模型，联合建模文本与音频 token 序列，如图 [3](#S2.F3) 所示。
该模型同时接受文本与音频 token 作为输入，并自回归地预测文本或音频 token，从而支持涉及文本与音频模态任意组合的全面任务。

形式上，令 $T=[t_{1},\ldots,t_{N}]$ 表示文本序列，音频 token 序列定义为：

$$
A=[A_{1},\ldots,A_{M}],\qquad A_{i}\triangleq(a_{i,1},\ldots,a_{i,R^{\prime}}), \tag{8}
$$

其中 $N$ 表示文本序列长度，$M$ 为音频序列长度，$R^{\prime}=8$ 为用于 LLM 训练的 RVQ 码本数量。
由于音频序列的信息密度相对较低，单个音频帧所携带的信息远少于文本 token。
为缓解这种跨模态的粒度失配并促进跨模态知识迁移，我们将音频序列划分为每组 $G$ 个连续帧，构成音频 patch：

$$
P=[P_{1},\ldots,P_{M/G}],\qquad P_{i}=[A_{(i-1)G+1},\ldots,A_{iG}]. \tag{9}
$$

MiMo-Audio 的输入是文本 token 与音频 patch 交错构成的序列。
令 $S=[s_{1},\ldots,s_{L}]$ 表示该交错序列，其中每个元素 $s_{i}$ 是一个文本 token 或一个音频 patch。
模型以自回归方式训练：

$$
p(S)=\prod_{i=1}^{L}p(s_{i}|s_{1},\dots,s_{i-1}), \tag{10}
$$

其中 $p(s_{i}|s_{1},\dots,s_{i-1})$ 在 $s_{i}$ 为文本 token 时表示 next-token 预测，在 $s_{i}$ 为音频 patch 时表示 next-patch 预测。
这种统一建模方式能够无缝处理任意文本-音频交错序列。
MiMo-Audio 包含三个主要组件：patch 编码器、LLM 骨干与 patch 解码器，下面将详细描述。

#### 2.2.1 Patch 编码器

patch 编码器将每个 patch 内的音频 token 变换为单个隐藏向量。
我们维护 $R^{\prime}$ 个独立的嵌入表 $\{E_{r}\}_{r=1}^{R^{\prime}}$，将音频 token 映射到相应的嵌入向量。
对每个音频 token $a_{i,r}$，我们得到其嵌入 $\mathbf{e}_{i,r}=E_{r}(a_{i,r})$。
第 $i$ 帧在所有 RVQ 码本上的嵌入被聚合为统一表示：

$$
\mathbf{e}_{i}=\sum_{r=1}^{R^{\prime}}\mathbf{e}_{i,r}. \tag{11}
$$

每个 patch 内由此产生的序列由一个 $L_{\mathrm{enc}}=6$ 层的 Transformer 编码器处理。
每层的隐藏维度为 1024，64 个注意力头，FFN 维度为 4096。
该编码器采用双向自注意力，使模型能够捕获跨帧的局部上下文信息。
patch 内所有帧的输出随后被拼接，并经一个线性变换层投影，以匹配 LLM 的输入维度。

#### 2.2.2 大语言模型

我们采用 MiMo-7B-Base（[Xiaomi, 2025](#bib.bib12)）作为 LLM 骨干。
模型在每个位置接受文本 token 嵌入或由 patch 编码器产生的音频 patch 表示作为输入。
所得隐藏状态可经输出投影层处理用于文本 token 预测，或送入 patch 解码器用于音频 patch 生成，详见下一节。

#### 2.2.3 Patch 解码器

patch 解码器在音频生成期间自回归地生成每个 patch 内的音频 token。
它包含 $L_{\mathrm{dec}}=16$ 层 Transformer，每层隐藏维度 1024、64 个注意力头、FFN 维度 4096。
解码器在自注意力机制中采用因果掩码。
patch 解码器使用与 patch 编码器相同的 $R^{\prime}$ 个嵌入表，每个 RVQ 码本对应一个。
为便于 RVQ token 生成，该 Transformer 配备 $R^{\prime}$ 个独立的输出头，每个专门负责预测特定 RVQ 码本的 token。

形式上，给定来自 LLM 的隐藏状态 $\mathbf{h}$，令 $P=[A_{1},\ldots,A_{G}]$ 表示待生成的音频 patch。
朴素做法是沿时间维度在每个 patch 内自回归地生成音频帧：

$$
p(P|\mathbf{h})=\prod_{i=1}^{G}p(A_{i}|\mathbf{h},A_{1},\dots,A_{i-1}), \tag{12}
$$

其中每帧 $A_{i}$ 的概率在 $R^{\prime}$ 个码本上分解：

$$
p(A_{i}|\mathbf{h},A_{1},\dots,A_{i-1})=\prod_{r=1}^{R^{\prime}}p(a_{i,r}|\mathbf{h},A_{1},\dots,A_{i-1}). \tag{13}
$$

然而，由于不同 RVQ 层的 token 之间存在依赖，在每个时间步同时预测所有 RVQ token 颇具挑战，常导致音频生成质量不佳。
为缓解这一局限，受 Copet et al. (2023) 启发，我们为音频 token 生成引入延迟机制。
具体而言，我们引入逐层延迟 $D=[d_{1},\ldots,d_{R^{\prime}}]$，其中 $d_{r}$ 表示在 RVQ 层 $r$ 生成 token 的延迟（以时间步计）。
延迟后的音频 patch 形式化为：

$$
P^{\prime}=[A^{\prime}_{1},\ldots,A^{\prime}_{G+\max(D)}], \tag{14}
$$

其中

$$
a^{\prime}_{i,r}=\begin{cases}a_{i-d_{r},r}&\text{若 }1\leq i-d_{r}\leq G\\ 0&\text{否则}\end{cases} \tag{15}
$$

对 $i\in[1,G+\max(D)]$ 与 $r\in[1,R^{\prime}]$ 成立。
这里，0 表示一个空 token，在编码与解码过程中均被忽略。
patch 解码器按照上述公式自回归地建模这些延迟音频 patch，并在解码阶段保持该延迟模式。
我们在表 [2](#S2.T2) 中列出详细的模型配置。

| 超参数 | Patch 编码器 | LLM | Patch 解码器 |
| --- | --- | --- | --- |
| 模型架构 | | | |
| 模型维度 | 1024 | 4096 | 1024 |
| FFN 维度 | 4096 | 11008 | 4096 |
| 注意力头数 | 64 | 32 | 64 |
| 层数 | 6 | 36 | 16 |
| 上下文长度 | 4 | 8192 | 11 |
| 输入/输出空间 | | | |
| 文本词表大小 | 151680 | | |
| 音频通道数 | 8 | | |
| 音频词表大小 | 1024-1024-128-128-128-128-128-128 | | |
| 音频帧率 | 6.25 Hz | | |

表 2：模型架构与输入/输出空间配置。

## 3 预训练

### 3.1 数据

我们的预训练语料由单模态数据（纯文本与纯语音）与多模态数据（语音-文本）组成。
纯文本语料的构建流程见 MiMo（[Xiaomi, 2025](#bib.bib12)）。
对于语音模态，目标是向模型提供大规模、高质量且多样的音频数据。
为此，我们开发了一条综合数据管线，整合数据收集、自动化处理、多维标注与质量控制。

#### 3.1.1 数据预处理

我们的预训练数据包含数亿小时的真实场景（in-the-wild）音频数据，并确保数据在来源与内容上的多样性。

- •

  来源多样性：数据覆盖多种来源，如公开播客、有声书、新闻广播、访谈与会议录音。这种多源、异构的数据组合确保模型不会偏向特定的录音环境或说话风格。
- •

  内容多样性：数据覆盖日常交流、娱乐媒体、商业创业、文化艺术与科学研究等主题领域。这使模型得以学习丰富的知识领域。

为将大规模原始音频转化为高质量训练数据，我们设计并实现了一条高效可扩展的自动化管线，其思路受先前工作启发（[Yu et al., 2023](#bib.bib53)；[He et al., 2024](#bib.bib54)；[Kang et al., 2024](#bib.bib52)；[Song et al., 2024](#bib.bib55)）。
该管线集成了音频归一化、说话人分离（diarization）、语音活动检测（VAD）、自动语音识别（ASR）与音频质量评估等模块。

#### 3.1.2 数据标注

为准确评估并过滤预训练数据，我们构建了一套覆盖语义与非语义维度的自动化标注系统，为每条数据生成丰富的结构化属性标签。

- •

  语义维度：基于 ASR 等模块的转写结果，我们构建了文本质量评估模型。该模型能从对话质量、知识密度、逻辑推理等多个维度为内容的语义价值打分。
- •

  非语义维度：为获取非语义层面的信息，我们训练了一个音频描述（captioning）模型。该模型能直接为音频生成丰富的自然语言描述（如音色特征、情绪风格与背景环境等非语义信息）。

这种双维度标注方法不仅度量了数据质量，还赋予语料更细粒度的属性信息，从而支撑更高效、更有针对性的过滤与训练。

#### 3.1.3 数据筛选

在多维数据标注的基础上，我们对数据进行了严格的过滤与采样。

- •

  低质数据过滤：依据预设的质量阈值，我们移除包含过多噪声、低质量与不安全内容的片段，确保最终语料的可靠性。
- •

  高质数据采样：我们整合语义与非语义维度的评分指标，设计了采样策略，确保模型能从高质量语料中高效学习。

### 3.2 训练

| 超参数 | 预训练：理解 | 预训练：理解-生成 | 后训练 |
| --- | --- | --- | --- |
| LR（Patch 编码器） | 2e-4 | 2e-4 | 5e-5 |
| LR（LLM） | 3e-5 | 3e-5 | 1e-5 |
| LR（Patch 解码器） | - | 2e-4 | 5e-5 |
| LR 调度器 | constant | cosine | cosine |
| batch size | 16.8M tokens | 16.8M tokens | 2.1M tokens |
| warmup 比例 | 0.01 | 0.01 | 0.01 |
| 损失权重 | 1-0-0-0-0-0-0-0-0 | 100-12-8-6-4-2-2-1-1 | 100-12-8-6-4-2-2-1-1 |
| 延迟模式 | - | 0-1-2-3-4-5-6-7 | 0-1-2-3-4-5-6-7 |

表 3：各阶段训练配置。LR 表示学习率。

我们的训练从 MiMo-7B-Base 模型出发。
为在最大程度保留其文本能力的同时赋予模型语音理解与生成能力，MiMo-Audio 采用渐进式的两阶段预训练方法。

#### 3.2.1 理解训练

在第一阶段，我们训练模型的 patch 编码器与 LLM 组件。
该阶段旨在使模型掌握语音理解能力。
我们构建了总计 2.6T token 的数据集，由 1.2T 文本 token 与 1.4T 语音相关 token（按 6.25Hz 语音帧率折算）组成。
数据包括四种任务格式：语音-文本交错数据、ASR 数据、通用音频描述数据与纯文本预训练数据。
在此阶段，我们只在文本 token 上计算损失。
如表 [3](#S3.T3) 所述，patch 编码器的学习率为 2e-4，LLM 的学习率为 3e-5，采用恒定（constant）学习率调度器。
每个 batch 包含 16.8M token，训练上下文长度为 8192。

#### 3.2.2 理解-生成联合训练

在第二阶段，我们训练模型的所有参数，包括 patch 编码器、LLM 与 patch 解码器。
该阶段旨在为模型提供语音理解与生成的整合能力。
训练数据集有 5T token，包括 2.6T 文本 token 与 2.4T 音频 token（按 6.25Hz 语音帧率折算）。
这包括七种任务格式：语音续写、语音-文本交错数据、ASR、TTS、通用音频描述、指令遵循 TTS 与文本预训练数据。
对于需要语音生成的任务，如语音续写，或生成语音-文本交错数据与 TTS 数据中的语音片段，我们采用文本引导的交错生成策略来提升语音生成质量。
具体而言，模型以固定 5:5 的比例交错生成文本 token 与语音 patch。
文本生成完成后，模型继续生成剩余的语音 token 直至完成。
在此阶段，我们在文本与音频 token 上均计算损失。
文本 token 的损失权重为 100，各 RVQ token 的权重依次为 12、8、6、4、2、2、1 与 1。
如表 [3](#S3.T3) 所示，patch 编码器与解码器的学习率为 2e-4，LLM 的学习率为 3e-5，学习率调度器采用 cosine 衰减。
batch size 与上下文长度与阶段 1 保持一致。

### 3.3 评测

我们从两类评测评估 MiMo-Audio-7B-Base：少样本上下文学习评测与语音续写评测。

#### 3.3.1 少样本上下文学习

为系统评估大规模预训练后 MiMo-Audio-7B-Base 的整体能力，我们沿用 GPT-3 风格的评测范式（[Brown et al., 2020a](#bib.bib10)），从三个维度采用语音-文本能力的少样本上下文学习协议：模态不变的通用知识、听觉理解与推理，以及语音到语音生成。
表 [4](#S3.T4) 概述了我们的少样本上下文学习评测设置。

##### 模态不变的通用知识

我们将模态不变的通用知识定义为：无论输入或输出模态为何，都能访问并表达相同底层知识的能力。
为在语音与文本上评估这一点，我们通过将 MMLU 数据集（[Hendrycks et al., 2021](#bib.bib11)）中的题目与选项合成为语音、同时保留其语义内容，构建了 SpeechMMLU（https://huggingface.co/datasets/XiaomiMiMo/SpeechMMLU）。
该数据集按科目与长度过滤，最终覆盖 34 个科目、共 8,549 条。
我们使用带多样音色的商用 TTS 系统进行合成。
它由四个平行 split 组成，支持同题跨模态对照，用于评估文本到文本、语音到文本、文本到语音与语音到语音场景下的知识。

- •

  文本到文本（T2T）：作为文本能力保留的度量，显示文本预训练获得的能力是否被语音-文本预训练稀释；同时为语音性能提供上界参考。
- •

  语音到文本（S2T）：与 T2T 相比，S2T 量化了在通用知识条目上，将口头问题映射到其语义形式并产生文本答案的跨模态代价。
- •

  文本到语音（T2S）：相对 T2T，T2S 探究在通用知识条目上将语义内容转换为口头输出的一致性与可控性。
- •

  语音到语音（S2S）：S2S 通过完成「听-想-说」闭环，对模型在通用知识上端到端语音交互的整合潜力提供综合度量。

| 能力 | 数据集 | 输入模态 | 输出模态 | 示例数 |
| --- | --- | --- | --- | --- |
| 通用知识 | SpeechMMLU | 文本 | 文本 | 5 |
| | | 语音 | 文本 | 5 |
| | | 文本 | 语音 | 5 |
| | | 语音 | 语音 | 5 |
| 音频理解 | MMAU | 音频+文本 | 文本 | 5 |
| 语音到语音 | 见表 [5](#S3.T5) | 语音 | 语音 | 16 |

表 4：少样本上下文学习评测设置。

##### 听觉理解与推理

虽然 SpeechMMLU 的 S2T split 评估了模型从语音中恢复语义并回答通用知识问题的能力，但它对非语义听觉因素的覆盖有限。
为充分刻画大规模语音-文本预训练后 MiMo-Audio 在听觉理解上的上限，我们将评测从基础语义理解扩展到声学世界的其他维度。
为此，我们在少样本上下文学习设置下于 MMAU 测试套件（[Sakshi et al., 2024](#bib.bib9)）上评估模型。
MMAU 包含跨越语音、环境声与音乐三个领域的音频信息抽取与推理问答。

##### 语音到语音生成

MiMo-Audio 以高保真音频 token 表示语音，作为感知与生成的统一接口，从而将预训练塑造为对大规模语音语料的高保真压缩。
我们假设足够有效的压缩会诱导出上下文学习能力，并在无需参数更新的情况下自然泛化到各种下游语音到语音任务。
为验证这一点，我们设计了一套少样本上下文语音到语音评测协议，仅以上下文中提供的成对语音示例作为条件。
各语音到语音生成任务的详细描述见表 [5](#S3.T5)。

| 任务 | 示例 | 输入 | 期望输出 |
| --- | --- | --- | --- |
| 语音转换 | 来自说话人 A 与 B 的成对话语，语义内容完全相同。 | 来自说话人 A 的话语，其语义不同于示例。 | 保留输入语义、但以说话人 B 音色呈现的话语。 |
| 情绪转换 | 来自固定说话人、分别带情绪 A 与情绪 B 的成对话语；每对语义相同。 | 来自同一说话人、带情绪 A 的话语，其语义不同于示例。 | 与输入音色和语义相同、但带情绪 B 的话语。 |
| 语速转换 | 来自固定说话人、分别带语速 A 与语速 B 的成对话语；每对语义相同。 | 来自同一说话人、带语速 A 的话语，其语义不同于示例。 | 与输入音色和语义相同、但带语速 B 的话语。 |
| 语音去噪 | 来自固定说话人的成对话语，包含一条带噪录音及其对应的干净版本。 | 来自同一说话人的带噪话语，其语义不同于示例。 | 输入话语的去噪版本。 |
| 语音翻译 | 中英成对话语，各示例间说话人不固定。 | 待翻译的英语句子。 | 翻译后的中文句子。 |

表 5：少样本上下文语音到语音评测的示例任务。

#### 3.3.2 语音续写

续写是自回归语言模型的一项基础能力。
通过在广泛文本语料上的生成式预训练，GPT-3（[Brown et al., 2020a](#bib.bib10)）等文本语言模型获得了从输入提示产生连贯文本续写的能力。
类似地，MiMo-Audio 在大规模语音语料上进行生成式预训练，并对高保真音频 token 执行语言建模。
这一训练范式赋予模型通用的语音续写能力：给定简短的语音提示，MiMo-Audio-7B-Base 能够生成语义连贯的续写，同时保留输入的关键声学特征，包括：(i) 说话人特有特征，如身份与音色；(ii) 韵律特征，涵盖节奏、语调与语速；(iii) 环境声学与非语音音频元素（如掌声、笑声、叹息）。

为探测这一能力，我们收集了来自多样领域的语音提示，包括单口喜剧、公开演讲、广播新闻、诗歌朗诵、有声书叙述与学术讲座，以及辩论、访谈与戏剧表演等多说话人场景。

### 3.4 结果

| 任务 | | Baichuan-Audio 7B-Base | Kimi-Audio 7B-Base | Step-Audio2-mini 7B-Base | MiMo-Audio 7B-Base |
| --- | --- | --- | --- | --- | --- |
| SpeechMMLU | S2S | 31.9 | 11.8 | 51.8 | **69.1** |
| | S2T | 29.9 | 67.9 | 67.8 | **69.5** |
| | T2S | 16.7 | 0.0 | 63.4 | **71.5** |
| | T2T | 71.1 | 70.7 | 74.1 | 72.5 |
| MMAU | Overall | 25.9 | 28.6 | 60.3 | **66.0** |
| | Speech | 14.4 | 29.4 | 55.0 | **67.6** |
| | Sound | 30.3 | 31.5 | 67.9 | 65.2 |
| | Music | 32.9 | 24.8 | 58.1 | **65.3** |

表 6：SpeechMMLU 与 MMAU 上的结果。我们将 MiMo-Audio-7B-Base 与 Baichuan-Audio-Base（[Li et al., 2025](#bib.bib30)）、Kimi-Audio-Base（[KimiTeam et al., 2025](#bib.bib15)）及 Step-Audio2-mini-Base（[Wu et al., 2025](#bib.bib17)）进行比较。

##### 涌现能力

如图 [1](#S0.F1.fig1) 所示，我们在多个评测基准上观察到显著的涌现能力，包括 5-shot SpeechMMLU（T2S 与 S2S）、16-shot 语音转换与 16-shot 语音到语音翻译。
在初始训练阶段（数据量达到约 0.7 万亿 token 之前），模型在这些任务上的表现微不足道，表明它尚未掌握解决这些复杂问题所需的原子技能。
然而，一旦训练量跨过这一关键阈值，模型性能便经历急剧的非线性跃升，呈现特征性的「相变」。
跃升之后，性能持续稳步提升并最终趋于稳定，表明模型已完全掌握并巩固了这一新能力。

这种从近零基线而非渐进改善中涌现出的能力，是模型通过大规模学习自主发展出高级泛化能力的直接体现。
这一发现有力支持了我们的论断：这代表着语音领域的「GPT-3 时刻」——通过足够大规模、无损的基于压缩的预训练，模型能够自发学会解决复杂的、前所未见的任务，从而实现任务泛化。

##### 语音智能

MiMo-Audio 模型在语音智能任务上交付了卓越性能，其优势主要体现在两个关键维度：SpeechMMLU 分数与「模态鸿沟」的幅度。

我们用 SpeechMMLU 分数衡量模型直接以语音为输入或输出进行复杂推理与知识问答的能力。
如表 [6](#S3.T6) 所示，MiMo-Audio 在 SpeechMMLU-S2S（69.1）、SpeechMMLU-S2T（69.5）与 SpeechMMLU-T2S（71.5）上均取得最高分。
Step-Audio2 mini-base 在 S2T 上取得相对有竞争力的分数（67.8），但在 S2S 上降至 51.8，暴露出在不同语音任务间的显著波动。
Kimi-Audio-base 在 S2T 上表现中等（67.9），却在 S2S 上暴露关键短板。
Baichuan-Audio-base 则在两项任务上得分持续偏低（31.9 与 29.9）。
因此，MiMo-Audio 是唯一能在所有语音推理任务上保持高水平表现的受评模型。

模态鸿沟是衡量模型在语音与文本模态之间能力一致性的指标，以模型 text2text 分数与 speech2speech（S2S）分数之差计算。
MiMo-Audio 的模态鸿沟为 3.4 分，而 Step-Audio2 mini-base 的鸿沟为 22.3 分，Kimi-Audio-base 为 58.9 分，Baichuan-Audio-base 为 39.2 分。
数据证实 MiMo-Audio 在所有模型中拥有最小的模态鸿沟，这凸显了其架构设计在跨不同输入模态保持核心推理能力连续性上的独特有效性。

##### 通用音频理解

如表 [6](#S3.T6) 所示，MiMo-Audio 在当前开源模型中展现出卓越的通用音频理解能力。
这一优势不仅体现在总分上，也体现在所有子任务的均衡表现上。

在 MMAU 总分上，MiMo-Audio 取得 66.0 分，比第二名 Step-Audio2 mini-base（60.3 分）高 5.7 分。
与 Kimi-Audio-base（28.6 分）和 Baichuan-Audio-base（25.9 分）相比，MiMo-Audio 的分数显著更高。
总分的领先直观反映了其整体性能优势。

通用音频理解要求模型在多样音频类型上均有良好表现，而 MiMo-Audio 以均衡的能力分布胜出。
它在三个子领域持续取得高分：语音（67.6）、音效（65.2）与音乐（65.3），没有明显的性能短板。
相比之下，Step-Audio2 mini-base 虽在音效上取得最高分（67.9），但在语音（55.0）与音乐（58.1）上表现相对较差。
Kimi-Audio-base 与 Baichuan-Audio-base 则在所有子任务上得分持续偏低。

##### 语音任务泛化

图 [1](#S0.F1.fig1) 报告了 16-shot 上下文学习设置下语音转换与语音到语音翻译的结果。
对于其他较难自动评测的语音到语音生成任务，我们提供定性演示（https://xiaomimimo.github.io/MiMo-Audio-Demo）。
我们强烈鼓励读者访问演示页面并试听结果。
在图 [1](#S0.F1.fig1) 中，少样本提示揭示：通用语音到语音生成与模态不变通用知识（SpeechMMLU，T2S/S2S）的能力在相近的训练规模上同时涌现。
这种对齐暗示一种共享的底层语音能力正在涌现，使 MiMo-Audio 能够泛化到对说话人身份、情绪与语速等细粒度因素的受控变换。

##### 语音续写

我们强烈建议访问演示页面试听我们的语音续写演示。
如演示页面所示，在这些多样的情境中，MiMo-Audio-Base 能够针对不同场景进行语音续写——包括游戏直播、教学、朗诵、歌唱、脱口秀与辩论——生成语义连贯、韵律衔接自然、声学条件一致且切合场景的语音，无需任何参数适配。
具体而言，对于歌唱语音，它能生成一致而悦耳的歌声旋律；对于脱口秀续写，它甚至能在恰当时刻产出观众的欢呼；对于双人辩论续写，它能生成观点一致、语义连贯、韵律流畅的双人语音；对方言语音续写，它能生成口音一致的内容；对于游戏直播与教学等场景，它能生成极富表现力与口语化的语音，并在恰当时机加入音量变化与结巴等口语化表达；对于朗诵语音续写，它能生成具备专业朗诵水准的情感语音。
这些结果表明，通过在大规模自然音频录音上的生成式预训练，MiMo-Audio-Base 已习得全面且可泛化的音频知识，展示了其在更广泛音频理解与生成应用中的潜力。

## 4 后训练

### 4.1 数据

我们后训练数据策略的目标，是使用一系列有监督指令微调数据集，激活预训练模型在不同任务上的理解与生成能力。

#### 4.1.1 音频理解

为激活模型的音频理解与推理能力，我们整合了覆盖语音、声音与音乐的多个开源数据集。
针对数据中的标签噪声与任务范式单一等问题，我们设计了一条基于 LLM 的数据清洗与增强管线。
这最终生成了大量多样的音频理解数据，如音频描述与音频问答。

#### 4.1.2 语音生成

为激活模型的语音生成能力，我们从预训练数据中抽取了高质量语音子集，并基于音频描述构建指令数据。
模型需要根据该指令生成相匹配的音频。
这一训练方法旨在强化模型的指令遵循能力，实现可控、高质量的语音生成。

#### 4.1.3 语音对话

为激活模型在不同对话场景中生成多样风格、高表现力语音的能力，我们构建了海量语音对话数据集，包含单轮与多轮对话。
这些语音对话由用户查询与助手回复组成。
其内容主要源自经严格筛选的文本数据，以确保可靠的质量。

为使 MiMo-Audio 适应多样的对话风格，我们首先对经口语化适配的问答对进行风格化改写。
随后使用内部 MiMo-TTS 系统合成具备恰当风格与情绪的语音。
合成时，我们从包含大量音色的声音库中随机选择提示音频，以确保覆盖不同的声音表现力。

| 任务类型 | 数据集 | 输入模态 | 输出模态 |
| --- | --- | --- | --- |
| ASR | AISHELL1 | 语音 | 文本 |
| | LibriSpeech test-clean | 语音 | 文本 |
| TTS | SeedTTS test-Zh | 文本 | 语音 |
| | SeedTTS test-En | 文本 | 语音 |
| | InstructTTSEval-Zh | 文本 | 语音 |
| | InstructTTSEval-En | 文本 | 语音 |
| 音频理解与推理 | MMSU | 语音+文本 | 文本 |
| | MMAU | 音频+文本 | 文本 |
| | MMAR | 音频+文本 | 文本 |
| | MMAU-Pro | 音频+文本 | 文本 |
| 语音对话 | Big Bench Audio S2T | 语音 | 文本 |
| | Big Bench Audio S2S | 语音 | 语音 |
| | MultiChallenge Audio S2T | 语音 | 文本 |
| | MultiChallenge Audio S2S | 语音 | 语音 |

表 7：MiMo-Audio-7B-Instruct 的评测设置。

### 4.2 训练

在后训练阶段，包括 patch 编码器、LLM 与 patch 解码器在内的所有模型参数都被微调。
为此，我们策展了 1000 亿 token 的综合训练数据集，涵盖六种不同的任务格式：ASR、TTS、音频理解、语音对话、指令遵循 TTS 与文本对话。
ASR、TTS 与文本对话的数据取自开源集合，其余任务则使用第 [4.1](#S4.SS1) 节详述的高质量数据集。

对于语音生成与语音对话任务，我们沿用第二预训练阶段的文本引导交错策略，模型以固定 5:5 的比例交错生成文本 token 与语音 patch。
损失权重也与该阶段保持一致：文本 token 为 100，音频 token 依次为 12、8、6、4、2、2、1、1。
如表 [3](#S3.T3) 所示，我们将 patch 编码器与解码器的学习率设为 5e-5，LLM 设为 1e-5，采用 cosine 衰减调度。
模型以 8192 的上下文长度与 2.1M token 的 batch size 训练。

**音频理解**

| 基准 | 模型 | 各项成绩 |
| --- | --- | --- |
| MMAU（Speech / Sound / Music / Overall） | MiMo-Audio-7B-Instruct | 68.47 / 82.58 / 73.65 / 74.90 |
| | Gemini 2.5 Flash | 76.58 / 73.27 / 65.57 / 71.80 |
| | Audio Flamingo 3 | 66.37 / 79.58 / 66.77 / 73.30 |
| | Step-Audio2-mini | 68.16 / 79.30 / 68.44 / 72.73 |
| | Kimi-Audio-Instruct | 62.16 / 75.68 / 66.77 / 68.20 |
| | Qwen2.5-Omni | 70.60 / 78.10 / 65.90 / 71.50 |
| | GLM-4-Voice | 35.44 / 27.63 / 27.84 / 30.30 |
| MMAU-Pro | MiMo-Audio-7B-Instruct | 53.35 |
| | Gemini 2.5 Flash | 59.20 |
| | Audio Flamingo 3 | 51.70 |
| | Step-Audio2-mini | 47.91 |
| | Kimi-Audio-Instruct | 46.60 |
| | Qwen2.5-Omni | 52.20 |
| | GLM-4-Voice | 38.25 |
| | GPT-4o-Audio | 52.50 |
| MMAR | MiMo-Audio-7B-Instruct | 63.60 |
| | Gemini 2.5 Flash | 65.60 |
| | Audio Flamingo 3 | 58.50 |
| | Step-Audio2-mini | 55.80 |
| | Kimi-Audio-Instruct | 48.00 |
| | Qwen2.5-Omni | 56.70 |
| | GLM-4-Voice | 29.50 |
| | GPT-4o-Audio | 63.50 |
| MMSU（Perception / Reasoning / Overall） | MiMo-Audio-7B-Instruct | 46.86 / 76.98 / 61.70 |
| | MiMo-Audio-7B-Instruct +Think | 51.71 / 74.79 / 62.88 |
| | Gemini 1.5 Pro | - / - / 60.70 |
| | Audio Flamingo 3 | - / - / 61.40 |
| | Step-Audio2-mini | 42.71 / 72.60 / 57.18 |
| | Kimi-Audio-Instruct | 44.84 / 75.70 / 59.78 |
| | Qwen2.5-Omni | 42.67 / 77.64 / 58.10 |
| | GLM-4-Voice | 11.04 / 16.16 / 13.30 |

**语音对话**

| 基准 | 模型 | 各项成绩 |
| --- | --- | --- |
| Big Bench Audio（S2T / S2S） | MiMo-Audio-7B-Instruct | 72.90 / 60.20 |
| | gpt-4o-audio-preview-2024-12-17 | 70.20 / 67.20 |
| | Step-Audio2-mini | 50.90 / 47.50 |
| | Kimi-Audio-Instruct | 59.40 / 51.00 |
| | Qwen2.5-Omni | 54.20 / 53.60 |
| | GLM-4-Voice | 44.80 / 42.70 |
| MultiChallenge Audio（S2T / S2S） | MiMo-Audio-7B-Instruct | 15.15 / 10.10 |
| | Step-Audio2-mini | 13.64 / 8.08 |
| | Kimi-Audio-Instruct | 7.07 / 1.01 |
| | Qwen2.5-Omni | 11.11 / 8.08 |
| | GLM-4-Voice | 9.09 / 6.06 |

表 8：音频理解与语音对话基准上的结果。粗体表示整体最佳性能，下划线标记开源模型中的最佳表现。+Think 表示开启思考。

| 基准 | 模型 | 各项成绩 |
| --- | --- | --- |
| Seed-TTS-Eval（ZH / EN / ZH-Hard） | MiMo-Audio-7B-Instruct | 1.96 / 5.37 / 14.14 |
| | Step-Audio2-mini | 2.13 / 3.18 / 16.31 |
| InstructTTSEval-EN（APS / DSD / RP / Overall） | MiMo-Audio-7B-Instruct | 80.60 / 77.63 / 59.54 / 72.59 |
| | GPT-4o-mini-tts | 76.40 / 74.30 / 54.80 / 68.50 |
| InstructTTSEval-ZH（APS / DSD / RP / Overall） | MiMo-Audio-7B-Instruct | 75.74 / 74.3 / 61.54 / 70.52 |
| | GPT-4o-mini-tts | 54.90 / 52.30 / 46.0 / 51.07 |
| ASR（Librispeech-test-clean / AISHELL） | MiMo-Audio-7B-Instruct | 3.50 / 1.65 |
| | Step-Audio2-mini | 1.87 / 0.95 |
| | Kimi-Audio-Instruct | 2.13 / 0.62 |

表 9：ASR 与 TTS 基准上的结果。

### 4.3 评测

后训练之后，我们对 MiMo-Audio-7B-Instruct 进行了系统评测，覆盖音频理解、语音对话以及语音识别与生成。
各任务类型的具体配置见表 [7](#S4.T7)。以下小节对每类任务进行详细描述。

#### 4.3.1 音频理解

作为通用音频模型，我们首先评估模型的通用音频理解能力。
首先，我们采用 MMSU（[Wang et al., 2025](#bib.bib23)）基准，其专注于多任务口语理解。
在语音之外，我们还使用 MMAU（[Sakshi et al., 2025](#bib.bib24)）基准将评测扩展到涉及声音与音乐的更广音频理解任务。
为进一步评估模型的音频推理能力，我们还使用 MMAR（[Ma et al., 2025](#bib.bib25)）与 MMAU-Pro（[Kumar et al., 2025](#bib.bib26)），它们评估模型处理混合音频输入（如语音、音乐与环境声）的能力及其对音频知识的掌握。

#### 4.3.2 语音对话

语音交互是人机通信最关键的模态之一。
为评估音频语言模型在多轮对话中遵循用户指令并完成任务的能力，沿用 OpenAI（https://openai.com/index/introducing-gpt-realtime/）的做法，我们首先在 Big Bench Audio（https://huggingface.co/datasets/ArtificialAnalysis/big_bench_audio）（[Srivastava et al., 2022](#bib.bib58)；[Suzgun et al., 2022](#bib.bib59)）上评估模型表现，这是一个旨在衡量音频语言模型智能水平的基准。
回复质量分数来自基于 GPT 的评估。
对于语音回复，先用 Whisper-Large-V3（[Radford et al., 2023](#bib.bib20)）模型转写音频，再由 GPT-4o-mini 评估。

接下来，为评估模型处理更复杂对话的能力，我们使用 MultiChallenge（[Sirdeshmukh et al., 2025](#bib.bib27)）数据集。
该数据集要求模型根据前文对话历史，为最后一轮生成恰当回复。

由于 MultiChallenge 最初是基于文本的多轮交互基准，我们通过以下步骤将其转换为语音版本：

- •

  过滤掉包含过多数学符号、表格、URL 或其他非口语格式的样本。
- •

  使用商用 TTS 模型将剩余样本转换为语音。同一样本内同一说话人的话语以一致的音色合成，音色从 250 个声音的池中选取。

由此得到 MultiChallenge Audio 的两个语音版本：S2T（语音到文本）与 S2S（语音到语音）。
在 S2T 版本中，对话历史以文本呈现；而在 S2S 版本中，全程均为语音。

#### 4.3.3 语音识别与生成

作为原生音频语言模型，语音识别与语音构成实现更高级语音任务的基础。
为此，我们将 MiMo-Audio-7B-Instruct 与其他音频语言模型（[Xu et al., 2025](#bib.bib16)；[KimiTeam et al., 2025](#bib.bib15)；[Wu et al., 2025](#bib.bib17)）在自动语音识别（ASR）与文本转语音（TTS）任务上进行比较。

对于 ASR，我们使用广泛采用的 LibriSpeech（[Panayotov et al., 2015](#bib.bib18)）test-clean 集（英语）与 AISHELL-1（[Bu et al., 2017](#bib.bib19)）测试集（中文）进行评测。
ASR 任务以词错误率（WER）为指标。

在识别能力之外，我们还评估 MiMo-Audio-7B-Instruct 的语音生成能力。
我们首先在 SeedTTS（[Anastassiou et al., 2024](#bib.bib57)）基准上评估 MiMo-Audio-7B-Instruct 的 TTS 性能，该基准包括英语与中文子集，以及更具挑战性的中文 hardcase 子集。
除常规 TTS 评测外，我们还在 InstructTTSEval（[Huang et al., 2025](#bib.bib22)）基准上进行更高级的评估，该基准衡量模型遵循复杂自然语言风格控制指令来合成相应语音的能力，从而联合评估保真度与表现力生成。
对于 TTS 任务，我们采用 WER 作为基础评测指标：合成语音先由 ASR 模型（[Radford et al., 2023](#bib.bib20)；[Gao et al., 2023](#bib.bib21)）转写，再与参考文本比较。
此外，InstructTTSEval 利用基于 Gemini 的打分进一步评估生成语音与输入指令之间的对齐程度。

### 4.4 结果

##### 音频理解

对于音频理解任务，如表 [8](#S4.T8) 所示，MMSU 与 MMAU 基准上的结果表明 MiMo-Audio-7B-Instruct 在语音、音频与音乐问答上取得领先性能。
它在这两个基准上的总分超越所有开源模型，也超越 Gemini 2.5 Flash 与 Gemini 1.5 Pro 等闭源模型。

对于更具挑战性的音频推理任务，MiMo-Audio-7B-Instruct 同样在 MMAU-Pro 与 MMAR 基准上领先，取得接近 Gemini 2.5 Flash 的结果。
这些结果共同表明，MiMo-Audio-7B-Instruct 是一个通用且强大的音频理解模型。

##### 语音对话

如表 [8](#S4.T8) 所示，MiMo-Audio-7B-Instruct 在 Big-Bench-audio 与 Multi-Challenge-Audio 两项任务上均取得所有开源模型中的最佳性能，其结果接近专有模型 gpt-4o。
在 Big-Bench-audio 基准上，MiMo-Audio-7B-Instruct 取得 72.90（S2T）与 60.20（S2S），仅次于 gpt-4o 排名第二，同时显著超越所有其他开源模型。
类似地，在 Multi-Challenge-Audio 基准上，它取得 15.15（S2T）与 10.10（S2S），同样以明显优势领跑开源阵营。
总之，MiMo-Audio-7B-Instruct 不仅以大幅优势超越所有其他开源模型，还缩小了与最先进专有模型 gpt-4o 的差距，展现出强劲的竞争力与实用潜力。
我们鼓励你访问我们的演示页面（https://xiaomimimo.github.io/MiMo-Audio-Demo）体验语音到语音对话演示。
我们的模型展现出强烈的拟人感与富有表现力的对话能力，在知识理解、情绪智能、对话技巧与指令遵循方面均有扎实表现，还支持方言与多语言交流。

##### 语音识别与生成

如表 [9](#S4.T9) 所示，MiMo-Audio-7B-Instruct 在开源大型语音模型中的 ASR 与 TTS 任务上均表现出色。
在 ASR 与 TTS 基准上，它取得与 Step-Audio2-mini、Kimi-Audio-Instruct 等其他开源模型相当的结果。
在 InstructTTS 评测中，MiMo-Audio-7B-Instruct 在英语与中文子集上均优于 gpt-4o-mini-tts，在总体指标上尤为有竞争力。
这些结果凸显了 MiMo-Audio-7B-Instruct 在可控文本转语音生成上的有效性，使其成为该领域领先的开源方案。

## 5 结论

在本工作中，我们证明了在海量无损音频数据上扩展 next-token 预测预训练，是实现通用语音智能的一条可行路径。
通过在超过 1 亿小时的前所未有语料上预训练，MiMo-Audio 成功超越了现有音频语言模型所特有的任务特定微调的局限。

我们的首要贡献是实证验证了「GPT-3 时刻」在语音领域是可以实现的。
我们观察到，跨过关键数据阈值之后，强大的少样本学习能力显著涌现，使模型能够泛化到广泛的任务——包括复杂的语音转换、风格迁移与语音编辑——而无需任务特定训练。
此外，我们给出了这一范式的完整蓝图，涵盖一个新颖的统一高保真音频分词器、一个可扩展的架构与一套分阶段训练策略。
MiMo-Audio-7B-Instruct 在多个基准上取得最先进性能，可与闭源系统比肩。

归根结底，本研究为构建真正通用的音频语言模型提供了基础方法论。
我们相信这项工作标志着向创建更自然、更灵活、更智能的系统迈出的重要一步——这些系统能够以类人的适应性理解并生成语音。

## 6 局限性与未来工作

##### 有限的上下文学习能力

MiMo-Audio-Base 的上下文学习能力仍然受限。
虽然预训练模型能够通过上下文学习完成预训练范围之外的多种新任务，但在某些场景下表现欠佳——例如带背景音乐的语音生成与复杂声音事件的处理。
展望未来，我们计划增强 MiMo-Audio 在通用音频生成上的能力。

##### 不稳定的语音对话表现

MiMo-Audio-Instruct 在语音对话中表现出若干局限，包括音色不连续、音频质量不稳定、发音错误以及遵循系统提示不一致。
值得注意的是，它极易读错复杂符号与公式，对话中的风格控制也不稳定。
在未来的工作中，我们将利用强化学习（RL）提升模型表现的稳定性。

##### 有限的思考性能

在整合思考机制时，MiMo-Audio-Instruct 仅在语音相关的理解任务上带来性能提升，而在声音与音乐理解任务中导致性能下降。
我们对失败案例（bad case）的分析表明，这一现象源于模型在思考过程中引入的幻觉。
展望未来，我们计划通过强化学习（RL）增强模型的音频理解能力。

## 参考文献


- Anastassiou et al. (2024)
  P. Anastassiou, J. Chen, J. Chen, Y. Chen, Z. Chen, Z. Chen, J. Cong, L. Deng, C. Ding, L. Gao, et al.
  Seed-tts: a family of high-quality versatile speech generation models.
  arXiv preprint arXiv:2406.02430.
  Cited by: [§2.1.3](#S2.SS1.SSS3.Px1.p1.1 "Settings ‣ 2.1.3 Evaluation ‣ 2.1 MiMo-Audio-Tokenizer ‣ 2 Model Architecture ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners"),
  [§4.3.3](#S4.SS3.SSS3.p3.1 "4.3.3 Speech Recognition and Generation ‣ 4.3 Evaluation ‣ 4 Post-Training ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Borsos et al. (2023)
  Z. Borsos, R. Marinier, D. Vincent, E. Kharitonov, O. Pietquin, M. Sharifi, D. Roblek, O. Teboul, D. Grangier, M. Tagliasacchi, and N. Zeghidour
  AudioLM: a language modeling approach to audio generation.
  External Links: 2209.03143,
  [Link](https://arxiv.org/abs/2209.03143)
  Cited by: [§1](#S1.p2.1 "1 Introduction ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Bradlow and Bent (2008)
  A. R. Bradlow and T. Bent
  Perceptual adaptation to non-native speech.
  Cognition 106 (2), pp. 707–729.
  External Links: ISSN 0010-0277,
  [Document](https://dx.doi.org/https%3A//doi.org/10.1016/j.cognition.2007.04.005),
  [Link](https://www.sciencedirect.com/science/article/pii/S0010027707001126)
  Cited by: [§1](#S1.p1.1 "1 Introduction ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Brown et al. (2020a)
  T. B. Brown, B. Mann, N. Ryder, M. Subbiah, J. Kaplan, P. Dhariwal, A. Neelakantan, P. Shyam, G. Sastry, A. Askell, S. Agarwal, A. Herbert-Voss, G. Krueger, T. Henighan, R. Child, A. Ramesh, D. M. Ziegler, J. Wu, C. Winter, C. Hesse, M. Chen, E. Sigler, M. Litwin, S. Gray, B. Chess, J. Clark, C. Berner, S. McCandlish, A. Radford, I. Sutskever, and D. Amodei
  Language models are few-shot learners.
  External Links: 2005.14165,
  [Link](https://arxiv.org/abs/2005.14165)
  Cited by: [§1](#S1.p5.1 "1 Introduction ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners"),
  [§3.3.1](#S3.SS3.SSS1.p1.1 "3.3.1 Few-shot In-context Learning ‣ 3.3 Evaluation ‣ 3 Pre-Training ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners"),
  [§3.3.2](#S3.SS3.SSS2.p1.1 "3.3.2 Speech Continuation ‣ 3.3 Evaluation ‣ 3 Pre-Training ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Brown et al. (2020b)
  T. Brown, B. Mann, N. Ryder, M. Subbiah, J. D. Kaplan, P. Dhariwal, A. Neelakantan, P. Shyam, G. Sastry, A. Askell, S. Agarwal, A. Herbert-Voss, G. Krueger, T. Henighan, R. Child, A. Ramesh, D. Ziegler, J. Wu, C. Winter, C. Hesse, M. Chen, E. Sigler, M. Litwin, S. Gray, B. Chess, J. Clark, C. Berner, S. McCandlish, A. Radford, I. Sutskever, and D. Amodei
  Language models are few-shot learners.
  In Advances in Neural Information Processing Systems, H. Larochelle, M. Ranzato, R. Hadsell, M.F. Balcan, and H. Lin (Eds.),
  Vol. 33, pp. 1877–1901.
  External Links: [Link](https://proceedings.neurips.cc/paper_files/paper/2020/file/1457c0d6bfcb4967418bfb8ac142f64a-Paper.pdf)
  Cited by: [§1](#S1.p2.1 "1 Introduction ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Bu et al. (2017)
  H. Bu, J. Du, X. Na, B. Wu, and H. Zheng
  AISHELL-1: an open-source mandarin speech corpus and a speech recognition baseline.
  In 2017 20th Conference of the Oriental Chapter of the International Coordinating Committee on Speech Databases and Speech I/O Systems and Assessment (O-COCOSDA),
  Vol. , pp. 1–5.
  External Links: [Document](https://dx.doi.org/10.1109/ICSDA.2017.8384449)
  Cited by: [§4.3.3](#S4.SS3.SSS3.p2.1 "4.3.3 Speech Recognition and Generation ‣ 4.3 Evaluation ‣ 4 Post-Training ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Chung et al. (2021)
  Y. Chung, Y. Zhang, W. Han, C. Chiu, J. Qin, R. Pang, and Y. Wu
  W2v-bert: combining contrastive learning and masked language modeling for self-supervised speech pre-training.
  In 2021 IEEE Automatic Speech Recognition and Understanding Workshop (ASRU),
  pp. 244–250.
  Cited by: [§2.1](#S2.SS1.p1.1 "2.1 MiMo-Audio-Tokenizer ‣ 2 Model Architecture ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Copet et al. (2023)
  J. Copet, F. Kreuk, I. Gat, T. Remez, D. Kant, G. Synnaeve, Y. Adi, and A. Défossez
  Simple and controllable music generation.
  Advances in Neural Information Processing Systems 36, pp. 47704–47720.
  Cited by: [§2.2.3](#S2.SS2.SSS3.p2.3 "2.2.3 Patch Decoder ‣ 2.2 MiMo-Audio ‣ 2 Model Architecture ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Défossez et al. (2022a)
  A. Défossez, J. Copet, G. Synnaeve, and Y. Adi
  High fidelity neural audio compression.
  arXiv preprint arXiv:2210.13438.
  Cited by: [§2.1](#S2.SS1.p1.1 "2.1 MiMo-Audio-Tokenizer ‣ 2 Model Architecture ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Défossez et al. (2022b)
  A. Défossez, J. Copet, G. Synnaeve, and Y. Adi
  High fidelity neural audio compression.
  External Links: 2210.13438,
  [Link](https://arxiv.org/abs/2210.13438)
  Cited by: [§2.1.2](#S2.SS1.SSS2.Px2.p1.1 "Adversarial Fine-tuning ‣ 2.1.2 Training ‣ 2.1 MiMo-Audio-Tokenizer ‣ 2 Model Architecture ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Défossez et al. (2024)
  A. Défossez, L. Mazaré, M. Orsini, A. Royer, P. Pérez, H. Jégou, E. Grave, and N. Zeghidour
  Moshi: a speech-text foundation model for real-time dialogue.
  Technical report
  External Links: 2410.00037,
  [Link](https://arxiv.org/abs/2410.00037)
  Cited by: [§1](#S1.p1.1 "1 Introduction ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners"),
  [§1](#S1.p2.1 "1 Introduction ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners"),
  [§2.1.3](#S2.SS1.SSS3.Px1.p1.1 "Settings ‣ 2.1.3 Evaluation ‣ 2.1 MiMo-Audio-Tokenizer ‣ 2 Model Architecture ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners"),
  [§2.1](#S2.SS1.p2.1 "2.1 MiMo-Audio-Tokenizer ‣ 2 Model Architecture ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Fang et al. (2025)
  Q. Fang, S. Guo, Y. Zhou, Z. Ma, S. Zhang, and Y. Feng
  LLaMA-omni: seamless speech interaction with large language models.
  External Links: 2409.06666,
  [Link](https://arxiv.org/abs/2409.06666)
  Cited by: [§1](#S1.p2.1 "1 Introduction ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Gao et al. (2023)
  Z. Gao, S. Zhang, I. McLoughlin, and Z. Yan
  Paraformer: fast and accurate parallel transformer for non-autoregressive end-to-end speech recognition.
  External Links: 2206.08317,
  [Link](https://arxiv.org/abs/2206.08317)
  Cited by: [§4.3.3](#S4.SS3.SSS3.p3.1 "4.3.3 Speech Recognition and Generation ‣ 4.3 Evaluation ‣ 4 Post-Training ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Goel et al. (2025)
  A. Goel, S. Ghosh, J. Kim, S. Kumar, Z. Kong, S. Lee, C. H. Yang, R. Duraiswami, D. Manocha, R. Valle, et al.
  Audio flamingo 3: advancing audio intelligence with fully open large audio language models.
  arXiv preprint arXiv:2507.08128.
  Cited by: [§1](#S1.p2.1 "1 Introduction ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Gong et al. (2025)
  Y. Gong, L. Jin, R. Deng, D. Zhang, X. Zhang, Q. Cheng, Z. Fei, S. Li, and X. Qiu
  XY-tokenizer: mitigating the semantic-acoustic conflict in low-bitrate speech codecs.
  arXiv preprint arXiv:2506.23325.
  Cited by: [§2.1.3](#S2.SS1.SSS3.Px1.p1.1 "Settings ‣ 2.1.3 Evaluation ‣ 2.1 MiMo-Audio-Tokenizer ‣ 2 Model Architecture ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners"),
  [§2.1](#S2.SS1.p2.1 "2.1 MiMo-Audio-Tokenizer ‣ 2 Model Architecture ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- He et al. (2024)
  H. He, Z. Shang, C. Wang, X. Li, Y. Gu, H. Hua, L. Liu, C. Yang, J. Li, P. Shi, Y. Wang, K. Chen, P. Zhang, and Z. Wu
  Emilia: an extensive, multilingual, and diverse speech dataset for large-scale speech generation.
  External Links: 2407.05361,
  [Link](https://arxiv.org/abs/2407.05361)
  Cited by: [§3.1.1](#S3.SS1.SSS1.p3.1 "3.1.1 Data Preprocessing ‣ 3.1 Data ‣ 3 Pre-Training ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Hendrycks et al. (2021)
  D. Hendrycks, C. Burns, S. Basart, A. Zou, M. Mazeika, D. Song, and J. Steinhardt
  Measuring massive multitask language understanding.
  External Links: 2009.03300,
  [Link](https://arxiv.org/abs/2009.03300)
  Cited by: [§1](#S1.p5.1 "1 Introduction ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners"),
  [§3.3.1](#S3.SS3.SSS1.Px1.p1.1 "Modality-Invariant General Knowledge ‣ 3.3.1 Few-shot In-context Learning ‣ 3.3 Evaluation ‣ 3 Pre-Training ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Hendrycks and Gimpel (2016)
  D. Hendrycks and K. Gimpel
  Gaussian error linear units (gelus).
  arXiv preprint arXiv:1606.08415.
  Cited by: [§2.1.1](#S2.SS1.SSS1.p1.1 "2.1.1 Architecture ‣ 2.1 MiMo-Audio-Tokenizer ‣ 2 Model Architecture ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Hsu et al. (2021)
  W. Hsu, B. Bolte, Y. H. Tsai, K. Lakhotia, R. Salakhutdinov, and A. Mohamed
  Hubert: self-supervised speech representation learning by masked prediction of hidden units.
  IEEE/ACM transactions on audio, speech, and language processing 29, pp. 3451–3460.
  Cited by: [§2.1](#S2.SS1.p1.1 "2.1 MiMo-Audio-Tokenizer ‣ 2 Model Architecture ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Huang et al. (2025)
  K. Huang, Q. Tu, L. Fan, C. Yang, D. Zhang, S. Li, Z. Fei, Q. Cheng, and X. Qiu
  InstructTTSEval: benchmarking complex natural-language instruction following in text-to-speech systems.
  External Links: 2506.16381,
  [Link](https://arxiv.org/abs/2506.16381)
  Cited by: [§4.3.3](#S4.SS3.SSS3.p3.1 "4.3.3 Speech Recognition and Generation ‣ 4.3 Evaluation ‣ 4 Post-Training ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Kang et al. (2024)
  W. Kang, X. Yang, Z. Yao, F. Kuang, Y. Yang, L. Guo, L. Lin, and D. Povey
  Libriheavy: a 50,000 hours asr corpus with punctuation casing and context.
  External Links: 2309.08105,
  [Link](https://arxiv.org/abs/2309.08105)
  Cited by: [§3.1.1](#S3.SS1.SSS1.p3.1 "3.1.1 Data Preprocessing ‣ 3.1 Data ‣ 3 Pre-Training ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- KimiTeam et al. (2025)
  KimiTeam, D. Ding, Z. Ju, Y. Leng, S. Liu, T. Liu, Z. Shang, K. Shen, W. Song, X. Tan, H. Tang, Z. Wang, C. Wei, Y. Xin, X. Xu, J. Yu, Y. Zhang, X. Zhou, Y. Charles, J. Chen, Y. Chen, Y. Du, W. He, Z. Hu, G. Lai, Q. Li, Y. Liu, W. Sun, J. Wang, Y. Wang, Y. Wu, Y. Wu, D. Yang, H. Yang, Y. Yang, Z. Yang, A. Yin, R. Yuan, Y. Zhang, and Z. Zhou
  Kimi-audio technical report.
  External Links: 2504.18425,
  [Link](https://arxiv.org/abs/2504.18425)
  Cited by: [§1](#S1.p1.1 "1 Introduction ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners"),
  [§1](#S1.p2.1 "1 Introduction ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners"),
  [§1](#S1.p3.1 "1 Introduction ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners"),
  [Table 6](#S3.T6 "In 3.4 Results ‣ 3 Pre-Training ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners"),
  [Table 6](#S3.T6.5 "In 3.4 Results ‣ 3 Pre-Training ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners"),
  [§4.3.3](#S4.SS3.SSS3.p1.1 "4.3.3 Speech Recognition and Generation ‣ 4.3 Evaluation ‣ 4 Post-Training ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Kong et al. (2020)
  J. Kong, J. Kim, and J. Bae
  HiFi-gan: generative adversarial networks for efficient and high fidelity speech synthesis.
  External Links: 2010.05646,
  [Link](https://arxiv.org/abs/2010.05646)
  Cited by: [§2.1.2](#S2.SS1.SSS2.Px2.p1.1 "Adversarial Fine-tuning ‣ 2.1.2 Training ‣ 2.1 MiMo-Audio-Tokenizer ‣ 2 Model Architecture ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Kumar et al. (2025)
  S. Kumar, Š. Sedláček, V. Lokegaonkar, F. López, W. Yu, N. Anand, H. Ryu, L. Chen, M. Plička, M. Hlaváček, W. F. Ellingwood, S. Udupa, S. Hou, A. Ferner, S. Barahona, C. Bolaños, S. Rahi, L. Herrera-Alarcón, S. Dixit, S. Patil, S. Deshmukh, L. Koroshinadze, Y. Liu, L. P. G. Perera, E. Zanou, T. Stafylakis, J. S. Chung, D. Harwath, C. Zhang, D. Manocha, A. Lozano-Diez, S. Kesiraju, S. Ghosh, and R. Duraiswami
  MMAU-pro: a challenging and comprehensive benchmark for holistic evaluation of audio general intelligence.
  External Links: 2508.13992,
  [Link](https://arxiv.org/abs/2508.13992)
  Cited by: [§1](#S1.p6.1 "1 Introduction ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners"),
  [§4.3.1](#S4.SS3.SSS1.p1.1 "4.3.1 Audio Understanding ‣ 4.3 Evaluation ‣ 4 Post-Training ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Lehet and Holt (2020)
  M. Lehet and L. L. Holt
  Nevertheless, it persists: dimension-based statistical learning and normalization of speech impact different levels of perceptual processing.
  Cognition 202, pp. 104328.
  External Links: ISSN 0010-0277,
  [Document](https://dx.doi.org/https%3A//doi.org/10.1016/j.cognition.2020.104328),
  [Link](https://www.sciencedirect.com/science/article/pii/S0010027720301475)
  Cited by: [§1](#S1.p1.1 "1 Introduction ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Li et al. (2025)
  T. Li, J. Liu, T. Zhang, Y. Fang, D. Pan, M. Wang, Z. Liang, Z. Li, M. Lin, G. Dong, et al.
  Baichuan-audio: a unified framework for end-to-end speech interaction.
  arXiv preprint arXiv:2502.17239.
  Cited by: [§1](#S1.p2.1 "1 Introduction ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners"),
  [§2.1.3](#S2.SS1.SSS3.Px1.p1.1 "Settings ‣ 2.1.3 Evaluation ‣ 2.1 MiMo-Audio-Tokenizer ‣ 2 Model Architecture ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners"),
  [§2.1](#S2.SS1.p1.1 "2.1 MiMo-Audio-Tokenizer ‣ 2 Model Architecture ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners"),
  [Table 6](#S3.T6 "In 3.4 Results ‣ 3 Pre-Training ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners"),
  [Table 6](#S3.T6.5 "In 3.4 Results ‣ 3 Pre-Training ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Lim and Ye (2017)
  J. H. Lim and J. C. Ye
  Geometric gan.
  External Links: 1705.02894,
  [Link](https://arxiv.org/abs/1705.02894)
  Cited by: [§2.1.2](#S2.SS1.SSS2.Px2.p1.1 "Adversarial Fine-tuning ‣ 2.1.2 Training ‣ 2.1 MiMo-Audio-Tokenizer ‣ 2 Model Architecture ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Liu et al. (2022)
  Z. Liu, H. Mao, C. Wu, C. Feichtenhofer, T. Darrell, and S. Xie
  A convnet for the 2020s.
  External Links: 2201.03545,
  [Link](https://arxiv.org/abs/2201.03545)
  Cited by: [§2.1.1](#S2.SS1.SSS1.p1.1 "2.1.1 Architecture ‣ 2.1 MiMo-Audio-Tokenizer ‣ 2 Model Architecture ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Ma et al. (2025)
  Z. Ma, Y. Ma, Y. Zhu, C. Yang, Y. Chao, R. Xu, W. Chen, Y. Chen, Z. Chen, J. Cong, K. Li, K. Li, S. Li, X. Li, X. Li, Z. Lian, Y. Liang, M. Liu, Z. Niu, T. Wang, Y. Wang, Y. Wang, Y. Wu, G. Yang, J. Yu, R. Yuan, Z. Zheng, Z. Zhou, H. Zhu, W. Xue, E. Benetos, K. Yu, E. Chng, and X. Chen
  MMAR: a challenging benchmark for deep reasoning in speech, audio, music, and their mix.
  External Links: 2505.13032,
  [Link](https://arxiv.org/abs/2505.13032)
  Cited by: [§1](#S1.p6.1 "1 Introduction ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners"),
  [§4.3.1](#S4.SS3.SSS1.p1.1 "4.3.1 Audio Understanding ‣ 4.3 Evaluation ‣ 4 Post-Training ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Miyato et al. (2018)
  T. Miyato, T. Kataoka, M. Koyama, and Y. Yoshida
  Spectral normalization for generative adversarial networks.
  External Links: 1802.05957,
  [Link](https://arxiv.org/abs/1802.05957)
  Cited by: [§2.1.2](#S2.SS1.SSS2.Px2.p1.1 "Adversarial Fine-tuning ‣ 2.1.2 Training ‣ 2.1 MiMo-Audio-Tokenizer ‣ 2 Model Architecture ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Panayotov et al. (2015)
  V. Panayotov, G. Chen, D. Povey, and S. Khudanpur
  Librispeech: an asr corpus based on public domain audio books.
  In 2015 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP),
  Vol. , pp. 5206–5210.
  External Links: [Document](https://dx.doi.org/10.1109/ICASSP.2015.7178964)
  Cited by: [§4.3.3](#S4.SS3.SSS3.p2.1 "4.3.3 Speech Recognition and Generation ‣ 4.3 Evaluation ‣ 4 Post-Training ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Radford et al. (2023)
  A. Radford, J. W. Kim, T. Xu, G. Brockman, C. McLeavey, and I. Sutskever
  Robust speech recognition via large-scale weak supervision.
  In Proceedings of the 40th International Conference on Machine Learning,
  ICML’23.
  Cited by: [§4.3.2](#S4.SS3.SSS2.p1.1 "4.3.2 Spoken Dialogue ‣ 4.3 Evaluation ‣ 4 Post-Training ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners"),
  [§4.3.3](#S4.SS3.SSS3.p3.1 "4.3.3 Speech Recognition and Generation ‣ 4.3 Evaluation ‣ 4 Post-Training ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Rix et al. (2001)
  A. W. Rix, J. G. Beerends, M. P. Hollier, and A. P. Hekstra
  Perceptual evaluation of speech quality (pesq)-a new method for speech quality assessment of telephone networks and codecs.
  In 2001 IEEE international conference on acoustics, speech, and signal processing. Proceedings (Cat. No. 01CH37221),
  Vol. 2, pp. 749–752.
  Cited by: [§2.1.3](#S2.SS1.SSS3.Px1.p1.1 "Settings ‣ 2.1.3 Evaluation ‣ 2.1 MiMo-Audio-Tokenizer ‣ 2 Model Architecture ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Sakshi et al. (2024)
  S. Sakshi, U. Tyagi, S. Kumar, A. Seth, R. Selvakumar, O. Nieto, R. Duraiswami, S. Ghosh, and D. Manocha
  MMAU: a massive multi-task audio understanding and reasoning benchmark.
  External Links: 2410.19168,
  [Link](https://arxiv.org/abs/2410.19168)
  Cited by: [§3.3.1](#S3.SS3.SSS1.Px2.p1.1 "Auditory Comprehension and Reasoning ‣ 3.3.1 Few-shot In-context Learning ‣ 3.3 Evaluation ‣ 3 Pre-Training ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Sakshi et al. (2025)
  S. Sakshi, U. Tyagi, S. Kumar, A. Seth, R. Selvakumar, O. Nieto, R. Duraiswami, S. Ghosh, and D. Manocha
  MMAU: a massive multi-task audio understanding and reasoning benchmark.
  In The Thirteenth International Conference on Learning Representations,
  External Links: [Link](https://openreview.net/forum?id=TeVAZXr3yv)
  Cited by: [§1](#S1.p6.1 "1 Introduction ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners"),
  [§4.3.1](#S4.SS3.SSS1.p1.1 "4.3.1 Audio Understanding ‣ 4.3 Evaluation ‣ 4 Post-Training ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Sirdeshmukh et al. (2025)
  V. Sirdeshmukh, K. Deshpande, J. Mols, L. Jin, E. Cardona, D. Lee, J. Kritz, W. Primack, S. Yue, and C. Xing
  MultiChallenge: a realistic multi-turn conversation evaluation benchmark challenging to frontier llms.
  External Links: 2501.17399,
  [Link](https://arxiv.org/abs/2501.17399)
  Cited by: [§1](#S1.p6.1 "1 Introduction ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners"),
  [§4.3.2](#S4.SS3.SSS2.p2.1 "4.3.2 Spoken Dialogue ‣ 4.3 Evaluation ‣ 4 Post-Training ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Siuzdak (2024)
  H. Siuzdak
  Vocos: closing the gap between time-domain and fourier-based neural vocoders for high-quality audio synthesis.
  External Links: 2306.00814,
  [Link](https://arxiv.org/abs/2306.00814)
  Cited by: [§2.1.1](#S2.SS1.SSS1.p1.1 "2.1.1 Architecture ‣ 2.1 MiMo-Audio-Tokenizer ‣ 2 Model Architecture ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Song et al. (2024)
  X. Song, M. Xing, C. Ma, S. Li, D. Wu, B. Zhang, F. Pan, D. Zhou, Y. Zhang, S. Lei, Z. Peng, and Z. Wu
  TouchTTS: an embarrassingly simple tts framework that everyone can touch.
  External Links: 2412.08237,
  [Link](https://arxiv.org/abs/2412.08237)
  Cited by: [§3.1.1](#S3.SS1.SSS1.p3.1 "3.1.1 Data Preprocessing ‣ 3.1 Data ‣ 3 Pre-Training ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Srivastava et al. (2022)
  A. Srivastava, A. Rastogi, A. Rao, A. A. M. Shoeb, A. Abid, A. Fisch, A. R. Brown, A. Santoro, A. Gupta, A. Garriga-Alonso, et al.
  Beyond the imitation game: quantifying and extrapolating the capabilities of language models.
  arXiv preprint arXiv:2206.04615.
  Cited by: [§4.3.2](#S4.SS3.SSS2.p1.1 "4.3.2 Spoken Dialogue ‣ 4.3 Evaluation ‣ 4 Post-Training ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Su et al. (2024)
  J. Su, M. Ahmed, Y. Lu, S. Pan, W. Bo, and Y. Liu
  Roformer: enhanced transformer with rotary position embedding.
  Neurocomputing 568, pp. 127063.
  Cited by: [§2.1.1](#S2.SS1.SSS1.p1.1 "2.1.1 Architecture ‣ 2.1 MiMo-Audio-Tokenizer ‣ 2 Model Architecture ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Sumner (2011)
  M. Sumner
  The role of variation in the perception of accented speech.
  Cognition 119 (1), pp. 131–136.
  External Links: ISSN 0010-0277,
  [Document](https://dx.doi.org/https%3A//doi.org/10.1016/j.cognition.2010.10.018),
  [Link](https://www.sciencedirect.com/science/article/pii/S0010027710002556)
  Cited by: [§1](#S1.p1.1 "1 Introduction ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Suzgun et al. (2022)
  M. Suzgun, N. Scales, N. Schärli, S. Gehrmann, Y. Tay, H. W. Chung, A. Chowdhery, Q. V. Le, E. H. Chi, D. Zhou, and J. Wei
  Challenging big-bench tasks and whether chain-of-thought can solve them.
  arXiv preprint arXiv:2210.09261.
  Cited by: [§4.3.2](#S4.SS3.SSS2.p1.1 "4.3.2 Spoken Dialogue ‣ 4.3 Evaluation ‣ 4 Post-Training ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Taal et al. (2010)
  C. H. Taal, R. C. Hendriks, R. Heusdens, and J. Jensen
  A short-time objective intelligibility measure for time-frequency weighted noisy speech.
  In 2010 IEEE international conference on acoustics, speech and signal processing,
  pp. 4214–4217.
  Cited by: [§2.1.3](#S2.SS1.SSS3.Px1.p1.1 "Settings ‣ 2.1.3 Evaluation ‣ 2.1 MiMo-Audio-Tokenizer ‣ 2 Model Architecture ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- van den Oord et al. (2018)
  A. van den Oord, O. Vinyals, and K. Kavukcuoglu
  Neural discrete representation learning.
  External Links: 1711.00937,
  [Link](https://arxiv.org/abs/1711.00937)
  Cited by: [§2.1.1](#S2.SS1.SSS1.p1.1 "2.1.1 Architecture ‣ 2.1 MiMo-Audio-Tokenizer ‣ 2 Model Architecture ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Wang et al. (2025)
  D. Wang, J. Wu, J. Li, D. Yang, X. Chen, T. Zhang, and H. Meng
  MMSU: a massive multi-task spoken language understanding and reasoning benchmark.
  External Links: 2506.04779,
  [Link](https://arxiv.org/abs/2506.04779)
  Cited by: [§1](#S1.p6.1 "1 Introduction ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners"),
  [§4.3.1](#S4.SS3.SSS1.p1.1 "4.3.1 Audio Understanding ‣ 4.3 Evaluation ‣ 4 Post-Training ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Wei et al. (2022a)
  J. Wei, Y. Tay, R. Bommasani, C. Raffel, B. Zoph, S. Borgeaud, D. Yogatama, M. Bosma, D. Zhou, D. Metzler, E. H. Chi, T. Hashimoto, O. Vinyals, P. Liang, J. Dean, and W. Fedus
  Emergent abilities of large language models.
  External Links: 2206.07682,
  [Link](https://arxiv.org/abs/2206.07682)
  Cited by: [§1](#S1.p3.1 "1 Introduction ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Wei et al. (2022b)
  J. Wei, X. Wang, D. Schuurmans, M. Bosma, F. Xia, E. Chi, Q. V. Le, D. Zhou, et al.
  Chain-of-thought prompting elicits reasoning in large language models.
  Advances in neural information processing systems 35, pp. 24824–24837.
  Cited by: [§1](#S1.p6.1 "1 Introduction ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Wu et al. (2025)
  B. Wu, C. Yan, C. Hu, C. Yi, C. Feng, F. Tian, F. Shen, G. Yu, H. Zhang, J. Li, M. Chen, P. Liu, W. You, X. T. Zhang, X. Li, X. Yang, Y. Deng, Y. Huang, Y. Li, Y. Zhang, Z. You, B. Li, C. Wan, H. Hu, J. Zhen, S. Chen, S. Yuan, X. Zhang, Y. Jiang, Y. Zhou, Y. Yang, B. Li, B. Ma, C. Song, D. Pang, G. Hu, H. Sun, K. An, N. Wang, S. Gao, W. Ji, W. Li, W. Sun, X. Wen, Y. Ren, Y. Ma, Y. Lu, B. Wang, B. Li, C. Miao, C. Liu, C. Xu, D. Shi, D. Hu, D. Wu, E. Liu, G. Huang, G. Yan, H. Zhang, H. Nie, H. Jia, H. Zhou, J. Sun, J. Wu, J. Wu, J. Yang, J. Yang, J. Lin, K. Li, L. Yang, L. Shi, L. Zhou, L. Gu, M. Li, M. Li, M. Li, N. Wu, Q. Han, Q. Tan, S. Pang, S. Fan, S. Liu, T. Cao, W. Lu, W. He, W. Xie, X. Zhao, X. Li, Y. Yu, Y. Yang, Y. Liu, Y. Lu, Y. Wang, Y. Ding, Y. Liang, Y. Lu, Y. Luo, Y. Yin, Y. Zhan, Y. Zhang, Z. Yang, Z. Zhang, B. Jiao, D. Jiang, H. Shum, J. Chen, J. Li, X. Zhang, and Y. Zhu
  Step-audio 2 technical report.
  External Links: 2507.16632,
  [Link](https://arxiv.org/abs/2507.16632)
  Cited by: [§1](#S1.p1.1 "1 Introduction ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners"),
  [§1](#S1.p2.1 "1 Introduction ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners"),
  [§1](#S1.p3.1 "1 Introduction ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners"),
  [Table 6](#S3.T6 "In 3.4 Results ‣ 3 Pre-Training ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners"),
  [Table 6](#S3.T6.5 "In 3.4 Results ‣ 3 Pre-Training ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners"),
  [§4.3.3](#S4.SS3.SSS3.p1.1 "4.3.3 Speech Recognition and Generation ‣ 4.3 Evaluation ‣ 4 Post-Training ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Wu et al. (2023)
  Y. Wu, I. D. Gebru, D. Marković, and A. Richard
  Audiodec: an open-source streaming high-fidelity neural audio codec.
  In ICASSP 2023-2023 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP),
  pp. 1–5.
  Cited by: [§2.1.2](#S2.SS1.SSS2.p1.1 "2.1.2 Training ‣ 2.1 MiMo-Audio-Tokenizer ‣ 2 Model Architecture ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Xiaomi (2025)
  L. Xiaomi
  MiMo: unlocking the reasoning potential of language model – from pretraining to posttraining.
  External Links: 2505.07608,
  [Link](https://arxiv.org/abs/2505.07608)
  Cited by: [3rd item](#S1.I1.i3.p1.1 "In 1 Introduction ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners"),
  [§2.2.2](#S2.SS2.SSS2.p1.1 "2.2.2 Large Language Model ‣ 2.2 MiMo-Audio ‣ 2 Model Architecture ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners"),
  [§3.1](#S3.SS1.p1.1 "3.1 Data ‣ 3 Pre-Training ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Xin et al. (2024)
  D. Xin, X. Tan, S. Takamichi, and H. Saruwatari
  Bigcodec: pushing the limits of low-bitrate neural speech codec.
  arXiv preprint arXiv:2409.05377.
  Cited by: [§2.1.3](#S2.SS1.SSS3.Px1.p1.1 "Settings ‣ 2.1.3 Evaluation ‣ 2.1 MiMo-Audio-Tokenizer ‣ 2 Model Architecture ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Xu et al. (2025)
  J. Xu, Z. Guo, J. He, H. Hu, T. He, S. Bai, K. Chen, J. Wang, Y. Fan, K. Dang, B. Zhang, X. Wang, Y. Chu, and J. Lin
  Qwen2.5-omni technical report.
  External Links: 2503.20215,
  [Link](https://arxiv.org/abs/2503.20215)
  Cited by: [§1](#S1.p2.1 "1 Introduction ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners"),
  [§4.3.3](#S4.SS3.SSS3.p1.1 "4.3.3 Speech Recognition and Generation ‣ 4.3 Evaluation ‣ 4 Post-Training ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Ye et al. (2025a)
  Z. Ye, P. Sun, J. Lei, H. Lin, X. Tan, Z. Dai, Q. Kong, J. Chen, J. Pan, Q. Liu, et al.
  Codec does matter: exploring the semantic shortcoming of codec for audio language model.
  In Proceedings of the AAAI Conference on Artificial Intelligence,
  Vol. 39, pp. 25697–25705.
  Cited by: [§2.1](#S2.SS1.p2.1 "2.1 MiMo-Audio-Tokenizer ‣ 2 Model Architecture ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Ye et al. (2025b)
  Z. Ye, X. Zhu, C. Chan, X. Wang, X. Tan, J. Lei, Y. Peng, H. Liu, Y. Jin, Z. Dai, H. Lin, J. Chen, X. Du, L. Xue, Y. Chen, Z. Li, L. Xie, Q. Kong, Y. Guo, and W. Xue
  Llasa: scaling train-time and inference-time compute for llama-based speech synthesis.
  External Links: 2502.04128,
  [Link](https://arxiv.org/abs/2502.04128)
  Cited by: [§2.1.3](#S2.SS1.SSS3.Px1.p1.1 "Settings ‣ 2.1.3 Evaluation ‣ 2.1 MiMo-Audio-Tokenizer ‣ 2 Model Architecture ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Yu et al. (2023)
  J. Yu, H. Chen, Y. Bian, X. Li, Y. Luo, J. Tian, M. Liu, J. Jiang, and S. Wang
  AutoPrep: an automatic preprocessing framework for in-the-wild speech data.
  External Links: 2309.13905,
  [Link](https://arxiv.org/abs/2309.13905)
  Cited by: [§3.1.1](#S3.SS1.SSS1.p3.1 "3.1.1 Data Preprocessing ‣ 3.1 Data ‣ 3 Pre-Training ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Zeghidour et al. (2021)
  N. Zeghidour, A. Luebs, A. Omran, J. Skoglund, and M. Tagliasacchi
  Soundstream: an end-to-end neural audio codec.
  IEEE/ACM Transactions on Audio, Speech, and Language Processing 30, pp. 495–507.
  Cited by: [§2.1.1](#S2.SS1.SSS1.p1.1 "2.1.1 Architecture ‣ 2.1 MiMo-Audio-Tokenizer ‣ 2 Model Architecture ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners"),
  [§2.1](#S2.SS1.p1.1 "2.1 MiMo-Audio-Tokenizer ‣ 2 Model Architecture ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Zeng et al. (2024)
  A. Zeng, Z. Du, M. Liu, K. Wang, S. Jiang, L. Zhao, Y. Dong, and J. Tang
  Glm-4-voice: towards intelligent and human-like end-to-end spoken chatbot.
  arXiv preprint arXiv:2412.02612.
  Cited by: [§1](#S1.p2.1 "1 Introduction ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners"),
  [§1](#S1.p3.1 "1 Introduction ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners"),
  [§2.1.3](#S2.SS1.SSS3.Px1.p1.1 "Settings ‣ 2.1.3 Evaluation ‣ 2.1 MiMo-Audio-Tokenizer ‣ 2 Model Architecture ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners"),
  [§2.1](#S2.SS1.p1.1 "2.1 MiMo-Audio-Tokenizer ‣ 2 Model Architecture ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Zhang et al. (2023a)
  D. Zhang, S. Li, X. Zhang, J. Zhan, P. Wang, Y. Zhou, and X. Qiu
  SpeechGPT: empowering large language models with intrinsic cross-modal conversational abilities.
  In Findings of the Association for Computational Linguistics: EMNLP 2023, H. Bouamor, J. Pino, and K. Bali (Eds.),
  Singapore, pp. 15757–15773.
  External Links: [Link](https://aclanthology.org/2023.findings-emnlp.1055/),
  [Document](https://dx.doi.org/10.18653/v1/2023.findings-emnlp.1055)
  Cited by: [§1](#S1.p1.1 "1 Introduction ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners"),
  [§1](#S1.p2.1 "1 Introduction ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Zhang et al. (2023b)
  X. Zhang, D. Zhang, S. Li, Y. Zhou, and X. Qiu
  Speechtokenizer: unified speech tokenizer for speech large language models.
  arXiv preprint arXiv:2308.16692.
  Cited by: [§2.1](#S2.SS1.p2.1 "2.1 MiMo-Audio-Tokenizer ‣ 2 Model Architecture ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").
- Zhang et al. (2023c)
  Y. Zhang, W. Han, J. Qin, Y. Wang, A. Bapna, Z. Chen, N. Chen, B. Li, V. Axelrod, G. Wang, et al.
  Google usm: scaling automatic speech recognition beyond 100 languages.
  arXiv preprint arXiv:2303.01037.
  Cited by: [§2.1](#S2.SS1.p1.1 "2.1 MiMo-Audio-Tokenizer ‣ 2 Model Architecture ‣ MiMo-Audio: Audio Language Models are Few-Shot Learners").

## 附录 A 贡献与致谢

我们谨向所有贡献者表达诚挚谢意，感谢他们宝贵的支持与付出，包括小米 LLM-Plus、NGK、MiChat、Mify、Data Platform 与 CloudML 团队，以及未在本文中明确列出的贡献者。
各角色内的作者按名字的字母顺序排列。

**核心贡献者**
Dong Zhang、Gang Wang、Jinlong Xue、Kai Fang、Liang Zhao、Rui Ma、Shuhuai Ren、Shuo Liu、Tao Guo、Weiji Zhuang、Xin Zhang、Xingchen Song、Yihan Yan、Yongzhe He、Cici†

**部署与评测**
Bowen Shen、Chengxuan Zhu、Chong Ma、Chun Chen、Heyu Chen、Jiawei Li、Lei Li、Menghang Zhu、Peidian Li、Qiying Wang、Sirui Deng、Weimin Xiong、Wenshan Huang、Wenyu Yang、Yilin Jiang、Yixin Yang、Yuanyuan Tian、Yue Ma、Yue Yu、Zihan Zhang、Zihao Yue

† 通讯作者

**其他贡献者**
Bangjun Xiao、Bingquan Xia、Bofei Gao、Bowen Ye、Can Cai、Chang Liu、Chenhong He、Chunan Li、Dawei Zhu、Duo Zhang、Fengyuan Shi、Guoan Wang、Hailin Zhang、Hanglong Lv、Hanyu Li、Hao Tian、Heng Qu、Hongshen Xu、Houbin Zhang、Huaqiu Liu、Jiangshan Duo、Jianguang Zuo、Jianyu Wei、Jiebao Xiao、Jinhao Dong、Jun Shi、Junhao Hu、Kainan Bao、Kang Zhou、Linghao Zhang、Meng Chen、Nuo Chen、Peng Zhang、Qianli Chen、Qiantong Wang、Rang Li、Shaohui Liu、Shengfan Wang、Shicheng Li、Shihua Yu、Shijie Cao、Shimao Chen、Shuhao Gu、Weikun Wang、Wenhan Ma、Xiangwei Deng、Xing Yong、Xing Zhang、Xu Wang、Yifan Song、Yihao Zhao、Yingbo Zhao、Yizhao Gao、Yu Cheng、Yu Tu、Yudong Wang、Zhaojun Huang、Zhengju Tang、Zhenru Lin、Zhichao Song、Zhipeng Xu、Zhixian Zheng、Zihan Jiang
