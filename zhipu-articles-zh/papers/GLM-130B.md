---
title: "GLM-130B：开放双语预训练模型"
title_en: "GLM-130B: An Open Bilingual Pre-trained Model"
arxiv: 2210.02414
date: 2022-10-05
source: https://arxiv.org/abs/2210.02414
crawled: 2026-09-22
translated: 2026-09-22
---

# GLM-130B：开放双语预训练模型

> 原文：[GLM-130B: An Open Bilingual Pre-trained Model](https://arxiv.org/abs/2210.02414) · 智谱 Z.ai arXiv

Aohan Zeng⋄†*、Xiao Liu⋄†*、Zhengxiao Du⋄†、Zihan Wang⋄、Hanyu Lai⋄、Ming Ding⋄、Zhuoyi Yang⋄、Yifan Xu⋄、Wendi Zheng⋄、Xiao Xia⋄、Weng Lam Tam、Zixuan Ma⋄、Yufei Xue、Jidong Zhai⋄、Wenguang Chen⋄、Peng Zhang、Yuxiao Dong⋄‡、Jie Tang⋄‡

清华大学⋄　智谱 AI（Zhipu.AI）

###### 摘要

我们介绍 GLM-130B，一个拥有 1300 亿参数的双语（英文与中文）预训练语言模型。这是一次开源 100B 规模模型的尝试——该模型至少与 GPT-3（davinci）同样好——并揭示这一规模的模型如何能够被成功预训练。在这项努力的过程中，我们面临大量意料之外的技术与工程挑战，尤其是损失尖峰（loss spike）与发散。本文介绍 GLM-130B 的训练过程，包括其设计选择、兼顾效率与稳定性的训练策略以及工程努力。最终得到的 GLM-130B 模型在众多流行英文基准上显著优于 GPT-3 175B（davinci），而在 OPT-175B 与 BLOOM-176B 上均未观察到这种性能优势。在相关基准上，它也持续且显著地超越最大的中文语言模型 ERNIE TITAN 3.0 260B。最后，我们利用 GLM-130B 一项独特的缩放性质，无需后训练即实现 INT4 量化，且几乎没有性能损失，这在 100B 规模模型中尚属首例；更重要的是，这使得它可以在 4×RTX 3090（24G）或 8×RTX 2080 Ti（11G）GPU 上进行高效推理——这是迄今使用 100B 规模模型所需的最为平价的 GPU。GLM-130B 模型权重可公开获取，其代码、训练日志、相关工具包以及经验教训均已在 <https://github.com/THUDM/GLM-130B/> 开源。

†† 有关作者贡献的详细信息，请参阅附录 E。

> 注 1：两位共同第一作者 AZ 与 XL 贡献相同（{zengaohan,shawliu9}@gmail.com）。
> 注 2：本工作的一部分在 AZ、XL 与 ZD 于智谱 AI（Zhipu.AI）实习期间完成。
> 注 3：团队负责人：YD 与 JT；通讯作者：JT（jietang@tsinghua.edu.cn）。

## 1 引言

大语言模型（LLM），尤其是参数量超过 1000 亿（100B）的模型（[Brown et al., 2020](#bib.bib12)；[Thoppilan et al., 2022](#bib.bib107)；[Rae et al., 2021](#bib.bib81)；[Chowdhery et al., 2022](#bib.bib18)；[Wang et al., 2021](#bib.bib117)），展现出了引人注目的缩放定律（[Wei et al., 2022b](#bib.bib121)），零样本与少样本能力随之突然涌现。其中，拥有 175B 参数的 GPT-3（[Brown et al., 2020](#bib.bib12)）开创了 100B 规模 LLM 的研究：仅凭 32 个带标注样本，它便在多种基准上取得显著优于全监督 BERT-Large 模型的表现。然而，无论是 GPT-3（以及许多其他闭源 100B 规模模型）——即模型本身——还是它如何被训练，至今对公众都不透明。训练一个这种规模的高质量 LLM，并将模型与训练过程向所有人公开，具有重要价值。

因此，我们旨在预训练一个开放且高精度的 100B 规模模型，并将伦理考量纳入其中。在尝试的过程中，我们逐渐意识到，与训练 10B 规模模型相比，预训练这一规模的稠密 LLM 在预训练效率、稳定性与收敛性方面带来了大量意料之外的技术与工程挑战。类似的困难也同期出现在 OPT-175B（[Zhang et al., 2022](#bib.bib133)）与 BLOOM-176B（[Scao et al., 2022](#bib.bib94)）的训练中，进一步凸显了 GPT-3 作为开创性研究的意义。

图 1：性能评测与伦理研究概览。

表 1：GLM-130B 与其他 100B 规模 LLM 以及 PaLM 540B 的对比。（LN：层归一化；FPF：浮点格式；MIP：多任务指令预训练；CN：中文）

| | 架构与数据 | | | | 训练 | | 推理 | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 模型 | 开源 | 目标函数 | LN | 主要语言 | 浮点格式 | 稳定化 | 量化 | 所需 GPU |
| GPT-3 175B | × | | | 英文 | FP16 | 未公开 | 未公开 | 未公开 |
| OPT-175B | ✓ | | | 英文 | FP16 | 手动调整 | INT8 | 8 × 3090 |
| BLOOM-176B | ✓ | GPT | Pre-LN | 多语言 | BF16 | 嵌入归一化 | INT8 | 8 × 3090 |
| PaLM 540B | × | GPT | Pre-LN | 英文 | BF16 | 手动调整 | 未公开 | 未公开 |
| GLM-130B | ✓ | GLM（空白填充与 MIP） | DeepNorm | 双语（中英） | FP16 | 嵌入梯度收缩 | INT4 | 4 × 3090 或 8 × 1080 Ti |

在本工作中，我们从工程努力、模型设计选择、兼顾效率与稳定性的训练策略，以及面向低成本推理的量化等方面，介绍 100B 规模模型 GLM-130B 的预训练。由于人们已广泛认识到，逐一实证枚举训练 100B 规模 LLM 的所有可能设计在计算上不可负担，我们不仅呈现训练 GLM-130B 的成功之处，也呈现许多失败的选项与经验教训。特别是，训练稳定性是这一规模模型训练成败的决定性因素。与 OPT-175B 手动调整学习率、以及 BLOOM-176B 以牺牲性能为代价使用嵌入归一化等做法不同，我们实验了多种选项，发现嵌入梯度收缩（embedding gradient shrink）策略可以显著稳定 GLM-130B 的训练。

具体而言，GLM-130B 是一个双语（英文与中文）双向稠密模型，拥有 1300 亿参数，于 2022 年 5 月 6 日至 7 月 3 日期间在一个包含 96 台 NVIDIA DGX-A100（8×40G）GPU 节点的集群上、在 4000 亿 token 上完成预训练。我们没有使用 GPT 风格的架构，而是采用通用语言模型（General Language Model，GLM）算法（[Du et al., 2022](#bib.bib27)），以利用其双向注意力优势与自回归空白填充目标。表 1 总结了 GLM-130B、GPT-3 与另外两项开源努力——OPT-175B 与 BLOOM-176B——之间的对比，并以大 4 倍的 PaLM 540B（[Chowdhery et al., 2022](#bib.bib18)）作为参照。

总而言之，概念上的独特性与工程努力使 GLM-130B 在广泛基准（共 112 项任务）上展现出超越 GPT-3 水平的性能，并且在许多情况下优于 PaLM 540B，而在 OPT-175B 与 BLOOM-176B 上均未观察到对 GPT-3 的超越（参见图 1 左）。在零样本性能方面，GLM-130B 在 LAMBADA（[Paperno et al., 2016](#bib.bib73)）上优于 GPT-3 175B（+5.0%）、OPT-175B（+6.5%）与 BLOOM-176B（+13.0%），并在 Big-bench-lite（[Srivastava et al., 2022](#bib.bib102)）上取得比 GPT-3 好 3 倍的表现。在 5-shot MMLU（[Hendrycks et al., 2021](#bib.bib40)）任务上，它优于 GPT-3 175B（+0.9%）与 BLOOM-176B（+12.7%）。作为一个同时支持中文的双语 LLM，它在 7 个零样本 CLUE（[Xu et al., 2020](#bib.bib127)）数据集（+24.26%）与 5 个零样本 FewCLUE（[Xu et al., 2021](#bib.bib128)）数据集（+12.75%）上显著优于最大的中文 LLM——ERNIE TITAN 3.0 260B（[Wang et al., 2021](#bib.bib117)）。重要的是，如图 1 右所示，作为一个开放模型，GLM-130B 相比同规模的其他 100B 级模型具有显著更低的偏见与生成毒性。

最后，我们将 GLM-130B 设计为能让尽可能多的人开展 100B 规模 LLM 研究。首先，不同于 OPT 与 BLOOM 使用 175B+ 参数，130B 的规模是经过斟酌的，因为这一规模支持在单台 A100（8×40G）服务器上推理。其次，为进一步降低 GPU 需求，我们在不进行后训练的情况下将 GLM-130B 量化到 INT4 精度，而 OPT 与 BLOOM 只能达到 INT8。得益于 GLM 架构的一项独特性质，GLM-130B 的 INT4 量化带来的性能下降可以忽略不计，例如在 LAMBADA 上为 -0.74%，在 MMLU 上甚至为 +0.05%，使其仍优于未压缩的 GPT-3。这使得 GLM-130B 能够在 4×RTX 3090（24G）或 8×RTX 2080 Ti（11G）服务器上以性能保证进行快速推理——这是迄今使用 100B 规模 LLM 所需的最为平价的 GPU。

我们将模型检查点、代码、训练日志、相关工具包以及经验教训开源。

## 2 GLM-130B 的设计选择

机器学习模型的架构定义了其归纳偏置。然而，人们已经意识到，为 LLM 探索各种架构设计在计算上是不可负担的。我们在此介绍并解释 GLM-130B 的独特设计选择。

### 2.1 GLM-130B 的架构

以 GLM 为骨干。最近的 100B 规模 LLM，如 GPT-3、PaLM、OPT 与 BLOOM，都遵循仅解码器自回归语言建模的传统 GPT 风格（[Radford et al., 2019](#bib.bib80)）架构。而在 GLM-130B 中，我们尝试探索以双向 GLM——通用语言模型（[Du et al., 2022](#bib.bib27)）——作为其骨干的潜力。

GLM 是一个基于 transformer 的语言模型，采用自回归空白填充作为训练目标。简言之，对于文本序列 $\bm{x}=[x_{1},\cdots,x_{n}]$，从中采样文本 span $\{\bm{s}_{1},\cdots,\bm{s}_{m}\}$，其中每个 $\bm{s}_{i}$ 表示一段连续 token $[s_{i,1},\cdots,s_{i,l_{i}}]$，并被替换（即破坏）为单个 mask token 以构成 $\bm{x}_{\text{corrupt}}$。模型被要求自回归地恢复它们。为了允许被破坏 span 之间的交互，它们彼此的可见性由对其顺序随机采样得到的一个排列决定。

GLM 对未屏蔽（即未破坏）上下文的双向注意力，使 GLM-130B 区别于使用单向注意力的 GPT 风格 LLM。为同时支持理解与生成，它混合了两种破坏目标，各由一个特殊的 mask token 指示：

- [MASK]：句子中的短空白，其长度总和占输入的一定比例。
- [gMASK]：位于句子末尾、随机长度的长空白，并提供前缀上下文。

图 2：GLM-130B 与相似规模的 LLM 在零样本 LAMBADA 语言建模上的表现。

GLM 双向注意力的细节见 [Du et al. (2022)](#bib.bib27)。

从概念上讲，带双向注意力的空白填充目标能够比 GPT 风格模型更有效地理解上下文：使用 [MASK] 时，GLM-130B 的表现如同 BERT（[Devlin et al., 2019](#bib.bib24)）与 T5（[Raffel et al., 2020](#bib.bib82)）；使用 [gMASK] 时，GLM-130B 的表现类似于 PrefixLM（[Liu et al., 2018](#bib.bib60)；[Dong et al., 2019](#bib.bib26)）。

从经验上看，GLM-130B 在零样本 LAMBADA 上取得 80.2% 的创纪录准确率，在图 2 中同时超越 GPT-3 与 PaLM 540B。通过设置注意力掩码，GLM-130B 的单向变体与 GPT-3 及 OPT-175B 相当。我们的观察与既有发现一致（[Liu et al., 2018](#bib.bib60)；[Dong et al., 2019](#bib.bib26)）。

图 3：GLM-130B 训练中不同 LayerNorm 的试验。结果表明 DeepNorm 是最稳定的选择，其梯度范数小，且在训练早期不出现尖峰。

层归一化（LayerNorm，LN，[Ba et al. (2016)](#bib.bib4)）。训练不稳定是训练 LLM 的主要挑战之一（[Zhang et al., 2022](#bib.bib133)；[Scao et al., 2022](#bib.bib94)；[Chowdhery et al., 2022](#bib.bib18)）（若干 100B 规模模型训练崩溃的例子参见附录图 10）。恰当的 LN 选择有助于稳定 LLM 的训练。我们实验了既有实践，如 Pre-LN（[Xiong et al., 2020](#bib.bib126)）、Post-LN（[Ba et al., 2016](#bib.bib4)）、Sandwich-LN（[Ding et al., 2021](#bib.bib25)），遗憾的是它们都无法稳定我们 GLM-130B 的测试运行（详见图 3(a) 与附录 B.2）。

由于 Post-LN 在初步实验中具有更理想的下游结果，尽管它无法稳定 GLM-130B，我们的搜索随后聚焦于 Post-LN。幸运的是，以新提出的 DeepNorm（[Wang et al., 2022b](#bib.bib116)）初始化 Post-LN 的一次尝试产生了有希望的训练稳定性。具体而言，给定 GLM-130B 的层数 $N$，我们采用 $\textrm{DeepNorm}(\bm{x})=\textrm{LayerNorm}(\alpha\cdot\bm{x}+\textrm{Network}(\bm{x}))$，其中 $\alpha=(2N)^{\frac{1}{2}}$，并对 ffn、v_proj 与 out_proj 应用缩放因子为 $(2N)^{-\frac{1}{2}}$ 的 Xavier 正态初始化。此外，所有偏置项均初始化为零。图 3 显示这显著改善了 GLM-130B 的训练稳定性。

位置编码与前馈网络。我们在训练稳定性与下游性能两方面实证测试了位置编码（PE）与 FFN 改进的不同选项（详见附录 B.3）。对于 GLM-130B 的 PE，我们采用旋转位置编码（RoPE，[Su et al. (2021)](#bib.bib104)）而非 ALiBi（[Press et al., 2021](#bib.bib76)）。为改进 Transformer 中的 FFN，我们选择带 GeLU（[Hendrycks & Gimpel, 2016](#bib.bib39)）激活的 GLU 作为替代。

### 2.2 GLM-130B 的预训练设置

受近期工作（[Aribandi et al., 2022](#bib.bib2)；[Wei et al., 2022a](#bib.bib120)；[Sanh et al., 2022](#bib.bib93)）启发，GLM-130B 的预训练目标不仅包括自监督的 GLM 自回归空白填充，还包括针对一小部分 token 的多任务学习。这有望帮助提升其下游零样本性能。

自监督空白填充（95% token）。回顾 GLM-130B 在此任务中同时使用 [MASK] 与 [gMASK]。每条训练序列在任一时刻独立地应用其中之一。具体而言，[MASK] 用于在 30% 的训练序列中屏蔽连续 span 以进行空白填充，span 长度服从泊松分布（$\lambda=3$），总长度占输入的 15%。对其余 70% 的序列，保留每条序列的前缀作为上下文，并用 [gMASK] 屏蔽其余部分。被屏蔽的长度从均匀分布中采样。

预训练数据包括 1.2T 的 Pile（train 划分）（[Gao et al., 2020](#bib.bib32)）英文数据、1.0T 的中文悟道语料库（WudaoCorpora，[Yuan et al., 2021](#bib.bib129)），以及我们从网络上抓取的 250G 中文语料（包括在线论坛、百科与问答），构成中英文内容均衡的配比。

多任务指令预训练（Multi-task Instruction Pre-training，MIP，5% token）。T5（[Raffel et al., 2020](#bib.bib82)）与 ExT5（[Aribandi et al., 2022](#bib.bib2)）指出，预训练中的多任务学习可能比微调更有帮助，因此我们提出在 GLM-130B 的预训练中纳入多种指令提示数据集，涵盖语言理解、生成与信息抽取。

与近期利用多任务提示微调来改进零样本任务迁移的工作（[Wei et al., 2022a](#bib.bib120)；[Sanh et al., 2022](#bib.bib93)）相比，MIP 只占 5% 的 token，且设置在预训练阶段，以避免损害 LLM 的其他通用能力，例如无条件自由生成。具体而言，我们纳入了来自（[Sanh et al., 2022](#bib.bib93)；[Wang et al., 2022a](#bib.bib115)）的 74 个提示数据集，列于附录 C 与表 12。建议 GLM-130B 的用户按照第 5 节所述标准，避免在这些数据集上评测其零样本与少样本能力。

### 2.3 面向平台的并行策略与模型配置

GLM-130B 在一个包含 96 台 DGX-A100 GPU（8×40G）服务器的集群上训练，可用时长为 60 天。目标是让尽可能多的 token 通过训练，因为一项近期研究（[Hoffmann et al., 2022](#bib.bib41)）指出，大多数现有 LLM 在很大程度上训练不足。

3D 并行策略。数据并行（[Valiant, 1990](#bib.bib109)）与张量模型并行（[Shoeybi et al., 2019](#bib.bib100)）是训练十亿级规模模型的事实标准（[Wang & Komatsuzaki, 2021](#bib.bib114)；[Du et al., 2022](#bib.bib27)）。为进一步应对巨大的 GPU 显存需求，以及节点间施加张量并行所导致的整体 GPU 利用率下降——因为训练 GLM-130B 使用的是 40G 而非 80G 的 A100——我们将流水线模型并行与另外两种策略结合，构成 3D 并行策略。

流水线并行将模型划分为每个并行组的若干顺序阶段；为进一步最小化流水线引入的气泡，我们利用 DeepSpeed（[Rasley et al., 2020](#bib.bib84)）中的 PipeDream-Flush（[Narayanan et al., 2021](#bib.bib71)）实现，以相对较大的全局批大小（4,224）训练 GLM-130B，以减少时间与 GPU 显存的浪费。通过数值与经验双重检验，我们采用 4 路张量并行与 8 路流水线并行（详见附录 B.4）。按照（[Chowdhery et al., 2022](#bib.bib18)）的计算方式，我们报告了 43.3% 的硬件 FLOPs 利用率（HFU），以及因重计算（re-materialization）而为 32.5% 的模型 FLOPs 利用率（MFU）。

GLM-130B 配置。我们的目标是让 100B 规模的 LLM 能在单台 DGX-A100（40G）节点上以 FP16 精度运行。基于我们从 GPT-3 采用的 12,288 隐藏状态维度，最终模型规模必须不超过 130B 参数，因此得名 GLM-130B。为最大化 GPU 利用率，我们基于平台及其相应并行策略来配置模型。为避免因两端额外的词嵌入导致中间阶段显存利用不足，我们从首尾各移除一层以平衡流水线划分，使 GLM-130B 共有 9×8−2=70 个 transformer 层。

在 60 天的集群使用期内，我们以每条样本 2,048 的固定序列长度，用 4000 亿 token（中英文各约 2000 亿）训练 GLM-130B。对于 [gMASK] 训练目标，我们使用 2,048 token 的上下文窗口；对于 [MASK] 与多任务目标，我们使用 512 的上下文窗口，并将四条样本拼接以满足 2,048 的序列长度。我们在前 2.5% 的样本上将批大小从 192 预热至 4224。我们使用 AdamW（[Loshchilov & Hutter, 2019](#bib.bib63)）作为优化器，$\beta_{1}$ 与 $\beta_{2}$ 分别设为 0.9 与 0.95，权重衰减为 0.1。学习率在前 0.5% 的样本上从 $10^{-7}$ 预热至 $8\times 10^{-5}$，随后按 $10\times$ 余弦调度衰减。我们使用 0.1 的 dropout 率，并以 1.0 的截断值裁剪梯度（完整配置参见表 11）。

## 3 GLM-130B 的训练稳定性

训练稳定性是 GLM-130B 质量的决定性因素，而它又在很大程度上受通过 token 数量的影响（[Hoffmann et al., 2022](#bib.bib41)）。因此，在算力使用约束下，浮点（FP）格式必须在效率与稳定性之间取舍：低精度 FP 格式（如 16 位精度 FP16）提升计算效率，但容易发生上溢与下溢错误，导致训练崩溃。

图 4：EGS 降低梯度尺度与方差，以稳定 LLM 的预训练。

混合精度。我们遵循混合精度（[Micikevicius et al., 2018](#bib.bib65)）策略（Apex O2）的常见做法，即前向与反向传播使用 FP16，优化器状态与主权重使用 FP32，以降低 GPU 显存占用并提升训练效率。与 OPT-175B 和 BLOOM-176B 类似（参见附录图 10），这一选择使 GLM-130B 的训练面临频繁的损失尖峰，且随训练进行往往愈发频繁。与精度相关的尖峰往往没有明确原因：有些会自行恢复；另一些则伴随梯度范数突然飙升的先兆，最终导致损失尖峰甚至 NaN。OPT-175B 尝试通过手动跳过数据与调整超参数来修复；BLOOM-176B 则通过嵌入归一化技术（[Dettmers et al., 2021](#bib.bib21)）解决。我们花费数月时间对这些尖峰进行实证研究，意识到当 transformer 扩展到该规模时会出现以下几个问题：

第一，如果使用 Pre-LN，transformer 主干分支的值尺度在更深层可能极大。GLM-130B 通过使用基于 DeepNorm 的 Post-LN（参见第 2.1 节）解决了这一问题，使值尺度始终有界。

第二，随着模型规模扩大，注意力分数增长得过大，超出了 FP16 的表示范围。LLM 中有若干选项可以克服这一问题。在 CogView（[Ding et al., 2021](#bib.bib25)）中，PB-Relax 被提出用于移除偏置项并在注意力计算中扣除极值以避免该问题，遗憾的是它无助于避免 GLM-130B 的不收敛。在 BLOOM-176B 中，由于 BF16 在 NVIDIA Ampere GPU（即 A100）上值域更宽，转而使用 BF16 格式。然而在我们的实验中，由于梯度累加时需转换为 FP32，BF16 比 FP16 多消耗约 15% 的运行时 GPU 显存；更重要的是，它不被其他 GPU 平台（如 NVIDIA Tesla V100）支持，限制了所产出 LLM 的可及性。BLOOM-176B 的另一个选项是在 BF16 上应用嵌入归一化，但要以显著的模型性能损失为代价，因为他们注意到嵌入归一化会损害模型的零样本学习（参见（[Scao et al., 2022](#bib.bib94)）第 4.3 节）。

嵌入层梯度收缩（Embedding Layer Gradient Shrink，EGS）。我们的实证搜索发现，梯度范数可以作为训练崩溃的信息性指标。具体而言，我们发现训练崩溃通常滞后于梯度范数的一次「尖峰」若干训练步。这类尖峰通常由嵌入层的异常梯度引起，因为我们观察到在 GLM-130B 训练早期，其梯度范数常常比其他层大数个数量级（参见图 4(a)）。此外，它在训练早期往往剧烈波动。视觉模型（[Chen et al., 2021](#bib.bib16)）通过冻结 patch 投影层处理了这一问题。遗憾的是，我们无法在语言模型中冻结嵌入层的训练。

最终，我们发现嵌入层上的梯度收缩能够克服损失尖峰，从而稳定 GLM-130B 的训练。该策略最早用于多模态 transformer CogView（[Ding et al., 2021](#bib.bib25)）。设 $\alpha$ 为收缩因子，该策略可通过 $\mathsf{word\_embedding}=\mathsf{word\_embedding}*\alpha+\mathsf{word\_embedding.detach()}*(1-\alpha)$ 轻松实现。图 4(b) 表明，实证上设置 $\alpha=0.1$ 即可消除我们原本会遭遇的大多数尖峰，且延迟可以忽略不计。

事实上，最终的 GLM-130B 训练只经历了三次后期损失发散（尽管它曾因硬件故障多次失败）。对于这三次意外尖峰，进一步收缩嵌入梯度仍能帮助稳定 GLM-130B 的训练。详见我们代码仓库中的训练笔记与 Tensorboard 日志。

## 4 GLM-130B 在 RTX 2080 Ti 上的推理

GLM-130B 的主要目标之一，是在不损失效率与效果的前提下，降低使用 100B 规模 LLM 的硬件门槛。

如前所述，130B 的模型规模是为了让完整的 GLM-130B 模型能在单台 A100（40G×8）服务器上运行，而非 OPT-175B 与 BLOOM-176B 所需的高端 A100（80G×8）机器。为加速 GLM-130B 推理，我们还利用 FasterTransformer（[Timonin et al., 2022](#bib.bib108)）以 C++ 实现 GLM-130B。与 Huggingface 上 BLOOM-176B 的 PyTorch 实现相比，GLM-130B 在同一台 A100 单机服务器上的解码推理快 7–8.4 倍（详见附录 B.5）。

面向 RTX 3090/2080 的 INT4 量化。为进一步支持普及型 GPU，我们尝试在保持性能优势的同时尽可能压缩 GLM-130B，特别是通过量化（[Zafrir et al., 2019](#bib.bib130)；[Shen et al., 2020](#bib.bib97)；[Tao et al., 2022](#bib.bib106)）实现，它为生成式语言模型引入的任务无关性能下降很小。

![图 5](2210.02414v2/figures/quantization-scaling-law.png)

图 5：（左）attn-dense 与 w2 的权重分布；（右）GLM-130B 的 INT4 权重量化缩放定律。

通常的做法是将模型权重与激活都量化到 INT8。然而，我们在附录 B.6 中的分析表明，LLM 的激活可能包含极端异常值。同期，OPT-175B 与 BLOOM-176B 中涌现的异常值也被发现（[Dettmers et al., 2022](#bib.bib22)），它们只影响约 0.1% 的特征维度，因此可以通过对异常维度做矩阵乘法分解来解决。不同的是，GLM-130B 的激活中存在约 30% 的异常值，使上述技术的效率大打折扣。因此，我们决定专注于模型权重（即主要是线性层）的量化，同时对激活保持 FP16 精度。量化后的模型在运行时动态转换为 FP16 精度，引入少量计算开销，但大幅降低了存储模型权重所需的 GPU 显存。

令人兴奋的是，我们成功实现了 GLM-130B 的 INT4 权重量化，而既有的成功迄今只达到 INT8。在显存方面，与 INT8 相比，INT4 版本额外节省一半所需 GPU 显存至 70GB，从而支持在 4×RTX 3090 Ti（24G）或 8×RTX 2080 Ti（11G）上推理 GLM-130B。在性能方面，表 2 左表明，在不进行任何后训练的情况下，INT4 版 GLM-130B 几乎没有性能下降，从而在常见基准上保持了对 GPT-3 的性能优势。

GLM 的 INT4 权重量化缩放定律。我们研究了图 5 右所展示的这一独特 INT4 权重量化缩放定律的底层机制。我们在图 5 左绘制了权重值分布，它直接影响量化质量。具体而言，分布更宽的线性层需要用更大的量化桶来量化，导致更多精度损失。因此，分布宽的 attn-dense 与 w2 矩阵解释了 GPT 风格 BLOOM 的 INT4 量化失败。相反，GLM 的分布往往比同等规模 GPT 窄得多，且随着 GLM 模型规模扩大，INT4 与 FP16 版本之间的差距持续缩小（详见附录图 15）。

表 2：左：量化 GLM-130B 在若干基准上的表现；右：INT4 量化 GLM-130B 使用 FasterTransformer 的推理速度（编码与解码）。

| 模型精度 | GLM-130B FP16 | GLM-130B INT8 | GLM-130B INT4 | GPT-3 FP16 |
| --- | --- | --- | --- | --- |
| MMLU（acc，↑） | 44.75 | 44.71 | 44.80 | 43.9 |
| LAMBADA（acc，↑） | 80.21 | 80.21 | 79.47 | 76.2 |
| Pile（部分，BPB，↓） | 0.634 | 0.638 | 0.641 | 0.74 |

| GPU 类型 | 128 编码 | 128 解码 | 512 编码 | 512 解码 |
| --- | --- | --- | --- | --- |
| 8×A100（40G） | 0.15s | 4.29s | 0.18s | 17.7s |
| 8×V100（32G） | 0.31s | 6.97s | 0.67s | 28.1s |
| 4×RTX 3090（24G） | 0.37s | 8.16s | 1.30s | 32.3s |
| 8×RTX 2080 Ti（11G） | 0.39s | 6.77s | 1.04s | 27.3s |

## 5 实验结果

我们遵循 GPT-3 与 PaLM 等 LLM 的常见设置来评测 GLM-130B 的英文性能¹。作为一个同时支持中文的双语 LLM，GLM-130B 也在中文基准上被评测。

¹ OPT-175B 论文中的结果被直接引用，因为对其的访问申请已数月未获批准。

关于 GLM-130B 零样本学习范围的讨论。由于 GLM-130B 经过了 MIP 训练，我们在此澄清其零样本评测的范围。事实上，「零样本」在社区中似乎存在有争议的解释，尚无共识。我们遵循一篇有影响力的相关综述（[Xian et al., 2018](#bib.bib125)），其中写道「在测试时，零样本学习设置的目标是将测试图像分配给一个未见过的类别标签」，其中涉及未见过的类别标签是关键。因此，我们得出挑选 GLM-130B 零样本（与少样本）数据集的标准：

- 英文：1）对于具有固定标签的任务（如自然语言推理）：此类任务下的任何数据集均不应被评测；2）对于没有固定标签的任务（如（多选）问答、主题分类）：只应考虑与 MIP 中数据集存在明显领域迁移的数据集。
- 中文：所有数据集都可以评测，因为存在零样本跨语言迁移。

过滤测试数据集。遵循先前实践（[Brown et al., 2020](#bib.bib12)；[Rae et al., 2021](#bib.bib81)）与我们上述标准，我们进行过滤，并避免报告可能受污染数据集的评测结果。对于 LAMBADA 与 CLUE，我们在 13-gram 设置下发现的重叠极少。Pile、MMLU 与 BIG-bench 要么是留出集，要么在语料抓取之后才发布。

### 5.1 语言建模

LAMBADA。LAMBADA（[Paperno et al., 2016](#bib.bib73)）是一个测试最后一个词语言建模能力的数据集。此前图 2 所示的结果表明，GLM-130B 凭借其双向注意力取得 80.2 的零样本准确率，创下 LAMBADA 新纪录。

表 3：GLM-130B 在 Pile 评测（18 个子数据集）上的平均 BPB。

| | Jurassic-1 | GPT-3 | GLM-130B |
| --- | --- | --- | --- |
| 平均 BPB | 0.650 | 0.742 | 0.634 |

Pile。Pile 测试集（[Gao et al., 2020](#bib.bib32)）包含一系列语言建模基准。按加权 BPB 计算，与 GPT-3 和 Jurassic-1（[Lieber et al., 2021](#bib.bib56)）相比——其中 GPT-3 的结果亦直接取自后者的报告——GLM-130B 在其 18 个共享测试集上平均而言表现最佳，展现了其强大的语言能力（详见附录 C.4）。

### 5.2 大规模多任务语言理解（MMLU）

MMLU（[Hendrycks et al., 2021](#bib.bib40)）是一个多样化基准，包含 57 项多选问答任务，涉及从高中水平到专家水平的人类知识。它在 Pile 抓取之后发布，是评测 LLM 少样本学习的理想测试平台。GPT-3 的结果取自 MMLU 官方，BLOOM-176B 则使用与 GLM-130B 相同的提示进行测试（详见附录 C.6 与表 15）。

图 7 中，GLM-130B 在 MMLU 上的少样本（5-shot）性能在看过约 3000 亿 token 后逼近 GPT-3（43.9），并随训练继续上升，在训练不得不结束时（即总共看过 4000 亿 token）达到 44.8 的准确率。这与（[Hoffmann et al., 2022](#bib.bib41)）的观察一致，即大多数现有 LLM 远未被充分训练。

### 5.3 超越模仿游戏基准（BIG-bench）

图 6：GLM-130B 在 MMLU（57 项任务）上随训练步数的变化。

图 7：不同规模模型在 BIG-bench-lite 评测（24 项任务）上的表现。

| 模型 | 0-shot | 1-shot | 3-shot |
| --- | --- | --- | --- |
| GPT-3 2.6B | 0.60 | 0.71 | 1.83 |
| GPT-3 6.7B | -0.06 | 2.93 | 5.40 |
| GPT-3 13B | 1.77 | 5.43 | 7.95 |
| GPT-3 175B | 4.35 | 11.34 | 13.18 |
| PaLM 540B | 8.05 | 37.77 | - |
| GLM-130B | 13.31 | 14.91 | 15.12 |

表 4：BIG-bench-lite（24 项任务）详情。

BIG-bench（[Srivastava et al., 2022](#bib.bib102)）对涉及模型推理、知识与常识能力的挑战性任务进行基准评测。鉴于在其全部 150 项任务上评测对 LLM 而言十分耗时，我们目前报告 BIG-bench-lite——一个官方的 24 任务子集。从图 7 与表 4 可以看到，GLM-130B 在零样本设置下超越 GPT-3 175B，甚至超越 PaLM 540B（大 4 倍）。这可能归功于 GLM-130B 的双向上下文注意力与 MIP，后者已被证明能改进未见任务上的零样本结果（[Wei et al., 2022a](#bib.bib120)；[Sanh et al., 2022](#bib.bib93)）。随着 shot 数量增加，GLM-130B 的性能持续上升，保持了对 GPT-3 的优势（各模型与任务的详情参见附录 C.5 与表 14）。

局限与讨论。在上述实验中，我们观察到 GLM-130B 的性能随少样本数量增加的增长（13.31 到 15.12）不如 GPT-3 显著（4.35 到 13.18）。这里给出我们对这一现象的直观理解。

首先，GLM-130B 的双向特性可能带来强劲的零样本表现（如零样本语言建模所示），从而比单向 LLM 更接近相似规模（即 100B 规模）模型的少样本「上界」。其次，这也可能归因于既有 MIP 范式（[Wei et al., 2022a](#bib.bib120)；[Sanh et al., 2022](#bib.bib93)）的缺陷，其训练中只涉及零样本预测，可能使 GLM-130B 偏向更强的零样本学习，而上下文少样本表现相对较弱。为纠正这一偏差，我们想到的一个潜在解决方案是，使用带有不同数量上下文样本的 MIP，而非仅使用零样本。

最后，尽管与 GPT-3 架构几乎相同，PaLM 540B 在少样本上下文学习上的相对增长显著高于 GPT-3。我们推测，这种性能增长的进一步加速源自 PaLM 高质量且多样的私有收集训练语料。结合我们的经验与（[Hoffmann et al., 2022](#bib.bib41)）的洞见，我们认识到应进一步投入更好的架构、更好的数据与更多的训练 FLOPS。

### 5.4 中文语言理解评测（CLUE）

我们在成熟的中文 NLP 基准 CLUE（[Xu et al., 2020](#bib.bib127)）与 FewCLUE（[Xu et al., 2021](#bib.bib128)）上评测 GLM-130B 的中文零样本性能。注意，我们没有在 MIP 中纳入任何中文下游任务。迄今，我们已完成对这两项基准中部分数据集的测试，包括 7 个 CLUE 与 5 个 FewCLUE 数据集（详见附录 C.7）。我们将 GLM-130B 与现有最大的中文单语语言模型——260B 的 ERNIE Titan 3.0（[Wang et al., 2021](#bib.bib117)）——进行比较，并遵循其设置在开发集上报告零样本结果。GLM-130B 在全部 12 项任务上持续超越 ERNIE Titan 3.0（参见图 8）。有趣的是，GLM-130B 在两个生成式机器阅读理解（MRC）数据集（DRCD 与 CMRC2018）上比 ERNIE 至少高出 260%，这可能是因为 GLM-130B 的预训练目标与生成式 MRC 的形式天然契合。

图 8：GLM-130B 与 ERNIE Titan 3.0 260B 在零样本 CLUE 与 FewCLUE 上的评测结果。

## 6 相关工作

在本节中，我们回顾与 GLM-130B 相关的工作，主题涵盖预训练、迁移以及预训练 LLM 的推理（[Qiu et al., 2020](#bib.bib78)；[Bommasani et al., 2021](#bib.bib11)）。

预训练。朴素语言建模指仅解码器自回归模型（如 GPT（[Radford et al., 2018](#bib.bib79)）），但它也认可文本上任何形式的自监督目标。近来，基于 transformer（[Vaswani et al., 2017](#bib.bib110)）的语言模型呈现出迷人的缩放定律：随着模型规模从 1.5B（[Radford et al., 2019](#bib.bib80)）、10B 级语言模型（[Raffel et al., 2020](#bib.bib82)；[Shoeybi et al., 2019](#bib.bib100)；[Black et al., 2022](#bib.bib9)）扩展到 100B 级的 GPT-3（[Brown et al., 2020](#bib.bib12)），新能力（[Wei et al., 2022b](#bib.bib121)）不断涌现。此后，尽管英文与中文领域出现了许多 100B 级 LLM（[Lieber et al., 2021](#bib.bib56)；[Thoppilan et al., 2022](#bib.bib107)；[Rae et al., 2021](#bib.bib81)；[Smith et al., 2022](#bib.bib101)；[Chowdhery et al., 2022](#bib.bib18)；[Wu et al., 2021](#bib.bib124)；[Zeng et al., 2021](#bib.bib131)；[Wang et al., 2021](#bib.bib117)），它们均不向公众开放，或仅能通过有限的 API 访问。LLM 的封闭性严重阻碍了其发展。GLM-130B 的努力，连同近期的 ElutherAI、OPT-175B（[Zhang et al., 2022](#bib.bib133)）与 BLOOM-176B（[Scao et al., 2022](#bib.bib94)），旨在为社区提供高质量的开源 LLM。

迁移。尽管微调一直是迁移学习的事实标准，但由于 LLM 体量巨大，其评测一直聚焦于提示与上下文学习（[Brown et al., 2020](#bib.bib12)；[Liu et al., 2021a](#bib.bib59)）。不过，近期也有一些关于语言模型参数高效学习（[Houlsby et al., 2019](#bib.bib43)）与提示微调（即 P-tuning，[Li & Liang (2021)](#bib.bib53)；[Liu et al. (2021b)](#bib.bib61)；[Lester et al. (2021)](#bib.bib51)；[Liu et al. (2022)](#bib.bib62)）的尝试。目前我们不关注它们，将它们在 GLM-130B 上的全面测试留待未来研究。

推理。如今大多数可公开访问的 LLM 都通过有限的 API 提供服务。在本工作中，我们努力的重要组成部分之一是 LLM 的高效快速推理。相关工作包括蒸馏（[Sanh et al., 2019](#bib.bib92)；[Jiao et al., 2020](#bib.bib46)；[Wang et al., 2020](#bib.bib118)）、量化（[Zafrir et al., 2019](#bib.bib130)；[Shen et al., 2020](#bib.bib97)；[Tao et al., 2022](#bib.bib106)）与剪枝（[Michel et al., 2019](#bib.bib64)；[Fan et al., 2019](#bib.bib31)）。非常近期的工作（[Dettmers et al., 2022](#bib.bib22)）表明，得益于异常维度的特殊分布，OPT-175B 与 BLOOM-176B 等 LLM 可以被量化到 8 比特。在本工作中，我们展示了 GLM 的 INT4 权重量化缩放定律，使 GLM-130B 能在少至 4×RTX 3090（24G）或 8×RTX 2080 Ti（11G）GPU 上推理。

## 7 结论与经验教训

我们介绍 GLM-130B，一个旨在促进开放与包容 LLM 研究的双语预训练语言模型。GLM-130B 的技术与工程实践为 LLM 的架构、预训练目标、训练稳定性与效率以及低成本推理提供了洞见。总而言之，这使得 GLM-130B 在 112 项任务的语言性能，以及偏见与毒性基准的伦理结果两方面都具有高质量。我们将成功与失败两方面的经验凝结为训练 100B 级 LLM 的经验教训，附于附录 B.10。

## 致谢

本研究受国家自然科学基金（NSFC）61825602、62276148 以及智谱 AI（Zhipu.AI）资助。我们感谢清华大学知识工程组（KEG）、移动、加速与网络系统并行架构与编译技术组（PACMAN）、自然语言处理组（THUNLP）以及智谱 AI 的所有合作者与伙伴。

## 伦理声明

我们在此确认，本工作所有共同作者均知悉 ICLR 伦理准则并遵守其行为规范。本工作介绍一个开源大语言模型（LLM），它可能被用于为有害应用生成合成文本，例如电话营销诈骗、政治宣传与个人骚扰，正如（[Weidinger et al., 2021](#bib.bib123)；[Sheng et al., 2021](#bib.bib98)；[Dev et al., 2021](#bib.bib23)）中所讨论的。我们不预期在使用该模型后出现任何危险的输出，尤其是针对弱势群体与历史上处于不利地位的群体。

为了更好地与社区协作、从技术上预防并最终消除这些风险，我们在本工作中做出以下关键的开放努力：

面向伦理风险研究的开源 LLM。虽然有些人认为限制 LLM 的访问可以防止此类有害应用，我们主张提升 LLM 的包容性能够更好地防御 LLM 可能造成的潜在危害。当前，只有政府与大企业能负担预训练 LLM 的可观成本，而拥有雄厚资金的组织并不保证不会利用 LLM 作恶。若无法接触此类 LLM，个人甚至无法意识到 LLM 在危害中扮演的角色。

反过来，发布开放的 LLM 可以为所有研究者提供访问途径与透明度，促进降低 LLM 潜在危害的研究，例如识别合成文本的算法（[Gehrmann et al. (2019)](#bib.bib34)）。同样众所周知的是，LLM 可能在公平性、偏见、隐私与真实性方面存在问题（[Zhang et al. (2021)](#bib.bib132)；[Lin et al. (2022)](#bib.bib58)；[Liang et al. (2021)](#bib.bib55)；[Bender et al. (2021)](#bib.bib6)）。开放的 LLM 可以揭示与特定输入对应的模型参数与内部状态，而非仅仅为黑盒模型提供 API。总之，研究者能够深入分析 LLM 的缺陷，并提出改进的算法加以解决。

伦理评测与改进。我们还在广泛的英文伦理评测基准上评测我们的模型，包括偏见测量（[Nadeem et al., 2021](#bib.bib69)；[Nangia et al., 2020](#bib.bib70)）、仇恨言论检测（[Mollas et al., 2020](#bib.bib68)）与毒性生成估计（[Gehman et al., 2020](#bib.bib33)）。尽管存在不足（[Blodgett et al., 2021](#bib.bib10)；[Jacobs & Wallach, 2021](#bib.bib45)），这些数据集仍是迈向 LLM 开放定量评测的有意义的第一步。

我们的评测表明，我们的算法设计——尤其是 LLM 的双语预训练——可以显著缓解 LLM 可能表现出的偏见与毒性，同时与其他用单语英文语料训练的 LLM（[Brown et al., 2020](#bib.bib12)；[Zhang et al., 2022](#bib.bib133)）相比保持强劲的语言性能（更多细节参见附录 A）。

## 可复现性

与主流闭源 LLM——包括 GPT-3 175B（[Brown et al., 2020](#bib.bib12)）、PaLM 540B（[Chowdhery et al., 2022](#bib.bib18)）、Gopher（[Rae et al., 2021](#bib.bib81)）、Chinchilla（[Hoffmann et al., 2022](#bib.bib41)）、LaMDA（[Thoppilan et al., 2022](#bib.bib107)）、FLAN（[Wei et al., 2022a](#bib.bib120)）等——相比，GLM-130B 是开源的，并从一开始就致力于促进 LLM 研究的开放与包容。

我们付出了巨大努力来确保评测的可复现性。对于预训练部分，尽管当下重现所需的成本难以负担，我们仍尽最大努力公开 GLM-130B 预训练的代码、细节与完整过程。我们让 GLM-130B 能在 3090/2080 Ti 等少数普及型 GPU 上推理的努力，也与可复现性的承诺一致，因为这使得大多数学术研究者能够在自己的离线机器上复现 GLM-130B 的结果。我们还为个人用户提供免费 API，以测试 GLM-130B 的能力。

预训练。我们在我们的仓库中提供预训练的完整训练笔记、Tensorboard 日志与代码（参见摘要）。预训练超参数与集群配置见第 2.3 节与表 11。训练语料构成与多任务指令预训练的细节见第 2.2 节与附录 C.1、C.2。

评测。我们将所有评测——包括语言基准（LAMBADA、Pile、MMLU、BIG-bench、CLUE 与 FewCLUE）与伦理基准（CrowS-Pairs、StereoSet、ETHOS、RealToxicPrompts）——组织为我们代码仓库中一键运行的 bash 脚本。语言建模基准的数据处理细节见第 5.1 节与附录 C.4，MMLU 的见第 5.2 节与附录 C.6，BIG-bench 的见第 5.3 节与附录 C.5，CLUE 与 FewCLUE 的见第 5.4 节。所有伦理评测的细节请参见附录 A。

## 参考文献
- Agarwal et al. (2021)

  Oshin Agarwal, Heming Ge, Siamak Shakeri, and Rami Al-Rfou.
  Knowledge graph based synthetic corpus generation for
  knowledge-enhanced language model pre-training.
  In *Proceedings of the 2021 Conference of the North American
  Chapter of the Association for Computational Linguistics: Human Language
  Technologies*, pp. 3554–3565, 2021.
- Aribandi et al. (2022)

  Vamsi Aribandi, Yi Tay, Tal Schuster, Jinfeng Rao, Huaixiu Steven Zheng,
  Sanket Vaibhav Mehta, Honglei Zhuang, Vinh Q Tran, Dara Bahri, Jianmo Ni,
  et al.
  Ext5: Towards extreme multi-task scaling for transfer learning.
  In *International Conference on Learning Representations*, 2022.
- Artetxe et al. (2021)

  Mikel Artetxe, Shruti Bhosale, Naman Goyal, Todor Mihaylov, Myle Ott, Sam
  Shleifer, Xi Victoria Lin, Jingfei Du, Srinivasan Iyer, Ramakanth Pasunuru,
  et al.
  Efficient large scale language modeling with mixtures of experts.
  *arXiv preprint arXiv:2112.10684*, 2021.
- Ba et al. (2016)

  Jimmy Lei Ba, Jamie Ryan Kiros, and Geoffrey E Hinton.
  Layer normalization.
  *arXiv preprint arXiv:1607.06450*, 2016.
- Bach et al. (2022)

  Stephen Bach, Victor Sanh, Zheng Xin Yong, Albert Webson, Colin Raffel, Nihal V
  Nayak, Abheesht Sharma, Taewoon Kim, M Saiful Bari, Thibault Févry,
  et al.
  Promptsource: An integrated development environment and repository
  for natural language prompts.
  In *Proceedings of the 60th Annual Meeting of the Association
  for Computational Linguistics: System Demonstrations*, pp. 93–104, 2022.
- Bender et al. (2021)

  Emily M. Bender, Timnit Gebru, Angelina McMillan-Major, and Shmargaret
  Shmitchell.
  On the dangers of stochastic parrots: Can language models be too big?
  In *FAccT ’21: 2021 ACM Conference on Fairness,
  Accountability, and Transparency, Virtual Event / Toronto, Canada, March
  3-10, 2021*, pp. 610–623. ACM, 2021.
- Berant et al. (2013)

  Jonathan Berant, Andrew Chou, Roy Frostig, and Percy Liang.
  Semantic parsing on freebase from question-answer pairs.
  In *Proceedings of the 2013 conference on empirical methods in
  natural language processing*, pp. 1533–1544, 2013.
- Bisk et al. (2020)

  Yonatan Bisk, Rowan Zellers, Jianfeng Gao, Yejin Choi, et al.
  Piqa: Reasoning about physical commonsense in natural language.
  In *Proceedings of the AAAI conference on artificial
  intelligence*, volume 34, pp. 7432–7439, 2020.
- Black et al. (2022)

  Sidney Black, Stella Biderman, Eric Hallahan, Quentin Anthony, Leo Gao,
  Laurence Golding, Horace He, Connor Leahy, Kyle McDonell, Jason Phang, et al.
  Gpt-neox-20b: An open-source autoregressive language model.
  In *Proceedings of BigScience Episode\\backslash# 5–Workshop
  on Challenges & Perspectives in Creating Large Language Models*, pp. 95–136, 2022.
- Blodgett et al. (2021)

  Su Lin Blodgett, Gilsinia Lopez, Alexandra Olteanu, Robert Sim, and Hanna
  Wallach.
  Stereotyping norwegian salmon: An inventory of pitfalls in fairness
  benchmark datasets.
  In *Proceedings of the 59th Annual Meeting of the Association
  for Computational Linguistics and the 11th International Joint Conference on
  Natural Language Processing (Volume 1: Long Papers)*, pp. 1004–1015, 2021.
- Bommasani et al. (2021)

  Rishi Bommasani, Drew A Hudson, Ehsan Adeli, Russ Altman, Simran Arora, Sydney
  von Arx, Michael S Bernstein, Jeannette Bohg, Antoine Bosselut, Emma
  Brunskill, et al.
  On the opportunities and risks of foundation models.
  *arXiv preprint arXiv:2108.07258*, 2021.
- Brown et al. (2020)

  Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla
  Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell,
  et al.
  Language models are few-shot learners.
  *Advances in neural information processing systems*,
  33:1877–1901, 2020.
- Cao et al. (2021)

  Nicola De Cao, Wilker Aziz, and Ivan Titov.
  Editing factual knowledge in language models.
  In *Proceedings of the 2021 Conference on Empirical Methods in
  Natural Language Processing, EMNLP 2021, Virtual Event / Punta Cana,
  Dominican Republic, 7-11 November, 2021*, pp. 6491–6506. Association for
  Computational Linguistics, 2021.
- Carreras & Màrquez (2005)

  Xavier Carreras and Lluís Màrquez.
  Introduction to the conll-2005 shared task: Semantic role labeling.
  In *CoNLL*, pp. 152–164, 2005.
- Castro Ferreira et al. (2020)

  Thiago Castro Ferreira, Claire Gardent, Nikolai Ilinykh, Chris van der Lee,
  Simon Mille, Diego Moussallem, and Anastasia Shimorina.
  The 2020 bilingual, bi-directional WebNLG+ shared task: Overview
  and evaluation results (WebNLG+ 2020).
  In *Proceedings of the 3rd International Workshop on Natural
  Language Generation from the Semantic Web (WebNLG+)*, pp. 55–76, Dublin,
  Ireland (Virtual), 12 2020. Association for Computational Linguistics.
  URL <https://aclanthology.org/2020.webnlg-1.7>.
- Chen et al. (2021)

  Xinlei Chen, Saining Xie, and Kaiming He.
  An empirical study of training self-supervised vision transformers.
  In *Proceedings of the IEEE/CVF International Conference on
  Computer Vision*, pp. 9640–9649, 2021.
- Chiu & Alexander (2021)

  Ke-Li Chiu and Rohan Alexander.
  Detecting hate speech with gpt-3.
  *arXiv preprint arXiv:2103.12407*, 2021.
- Chowdhery et al. (2022)

  Aakanksha Chowdhery, Sharan Narang, Jacob Devlin, Maarten Bosma, Gaurav Mishra,
  Adam Roberts, Paul Barham, Hyung Won Chung, Charles Sutton, Sebastian
  Gehrmann, et al.
  Palm: Scaling language modeling with pathways.
  *arXiv preprint arXiv:2204.02311*, 2022.
- Clark et al. (2018)

  Peter Clark, Isaac Cowhey, Oren Etzioni, Tushar Khot, Ashish Sabharwal, Carissa
  Schoenick, and Oyvind Tafjord.
  Think you have solved question answering? try arc, the ai2 reasoning
  challenge.
  *arXiv preprint arXiv:1803.05457*, 2018.
- Dai et al. (2019)

  Zihang Dai, Zhilin Yang, Yiming Yang, Jaime G Carbonell, Quoc Le, and Ruslan
  Salakhutdinov.
  Transformer-xl: Attentive language models beyond a fixed-length
  context.
  In *Proceedings of the 57th Annual Meeting of the Association
  for Computational Linguistics*, pp. 2978–2988, 2019.
- Dettmers et al. (2021)

  Tim Dettmers, Mike Lewis, Sam Shleifer, and Luke Zettlemoyer.
  8-bit optimizers via block-wise quantization.
  *arXiv preprint arXiv:2110.02861*, 2021.
- Dettmers et al. (2022)

  Tim Dettmers, Mike Lewis, Younes Belkada, and Luke Zettlemoyer.
  Llm. int8 (): 8-bit matrix multiplication for transformers at scale.
  *arXiv preprint arXiv:2208.07339*, 2022.
- Dev et al. (2021)

  Sunipa Dev, Masoud Monajatipoor, Anaelia Ovalle, Arjun Subramonian, J. M.
  Phillips, and Kai Wei Chang.
  Harms of gender exclusivity and challenges in non-binary
  representation in language technologies.
  *ArXiv*, abs/2108.12084, 2021.
- Devlin et al. (2019)

  Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova.
  Bert: Pre-training of deep bidirectional transformers for language
  understanding.
  In *Proceedings of the 2019 Conference of the North American
  Chapter of the Association for Computational Linguistics: Human Language
  Technologies, Volume 1 (Long and Short Papers)*, pp. 4171–4186, 2019.
- Ding et al. (2021)

  Ming Ding, Zhuoyi Yang, Wenyi Hong, Wendi Zheng, Chang Zhou, Da Yin, Junyang
  Lin, Xu Zou, Zhou Shao, Hongxia Yang, et al.
  Cogview: Mastering text-to-image generation via transformers.
  *Advances in Neural Information Processing Systems*,
  34:19822–19835, 2021.
- Dong et al. (2019)

  Li Dong, Nan Yang, Wenhui Wang, Furu Wei, Xiaodong Liu, Yu Wang, Jianfeng Gao,
  Ming Zhou, and Hsiao-Wuen Hon.
  Unified language model pre-training for natural language
  understanding and generation.
  *Advances in Neural Information Processing Systems*, 32, 2019.
- Du et al. (2022)

  Zhengxiao Du, Yujie Qian, Xiao Liu, Ming Ding, Jiezhong Qiu, Zhilin Yang, and
  Jie Tang.
  Glm: General language model pretraining with autoregressive blank
  infilling.
  In *Proceedings of the 60th Annual Meeting of the Association
  for Computational Linguistics (Volume 1: Long Papers)*, pp. 320–335, 2022.
- Dušek et al. (2019)

  Ondřej Dušek, David M. Howcroft, and Verena Rieser.
  Semantic noise matters for neural natural language generation.
  In *Proceedings of the 12th International Conference on Natural
  Language Generation*, pp. 421–426, Tokyo, Japan, October–November 2019.
  Association for Computational Linguistics.
  doi: 10.18653/v1/W19-8652.
  URL <https://aclanthology.org/W19-8652>.
- Elsahar et al. (2018)

  Hady Elsahar, Pavlos Vougiouklis, Arslen Remaci, Christophe Gravier, Jonathon
  Hare, Frederique Laforest, and Elena Simperl.
  T-rex: A large scale alignment of natural language with knowledge
  base triples.
  In *Proceedings of the Eleventh International Conference on
  Language Resources and Evaluation (LREC 2018)*, 2018.
- Eric et al. (2020)

  Mihail Eric, Rahul Goel, Shachi Paul, Abhishek Sethi, Sanchit Agarwal, Shuyang
  Gao, Adarsh Kumar, Anuj Kumar Goyal, Peter Ku, and Dilek Hakkani-Tür.
  Multiwoz 2.1: A consolidated multi-domain dialogue dataset with state
  corrections and state tracking baselines.
  In *LREC*, 2020.
- Fan et al. (2019)

  Angela Fan, Edouard Grave, and Armand Joulin.
  Reducing transformer depth on demand with structured dropout.
  *arXiv preprint arXiv:1909.11556*, 2019.
- Gao et al. (2020)

  Leo Gao, Stella Biderman, Sid Black, Laurence Golding, Travis Hoppe, Charles
  Foster, Jason Phang, Horace He, Anish Thite, Noa Nabeshima, et al.
  The pile: An 800gb dataset of diverse text for language modeling.
  *arXiv preprint arXiv:2101.00027*, 2020.
- Gehman et al. (2020)

  Samuel Gehman, Suchin Gururangan, Maarten Sap, Yejin Choi, and Noah A. Smith.
  Realtoxicityprompts: Evaluating Neural Toxic Degeneration in
  Language Models.
  *dblp://journals/dblp*, 2020.
- Gehrmann et al. (2019)

  Sebastian Gehrmann, Hendrik Strobelt, and Alexander Rush.
  GLTR: Statistical detection and visualization of generated text.
  In *Proceedings of the 57th Annual Meeting of the Association
  for Computational Linguistics: System Demonstrations*, pp. 111–116,
  Florence, Italy, July 2019. Association for Computational Linguistics.
- Gehrmann et al. (2021)

  Sebastian Gehrmann, Tosin Adewumi, Karmanya Aggarwal, Pawan Sasanka
  Ammanamanchi, Aremu Anuoluwapo, Antoine Bosselut, Khyathi Raghavi Chandu,
  Miruna Clinciu, Dipanjan Das, Kaustubh D Dhole, et al.
  The gem benchmark: Natural language generation, its evaluation and
  metrics.
  *GEM 2021*, pp. 96, 2021.
- Geva et al. (2021)

  Mor Geva, Daniel Khashabi, Elad Segal, Tushar Khot, Dan Roth, and Jonathan
  Berant.
  Did aristotle use a laptop? a question answering benchmark with
  implicit reasoning strategies.
  *Transactions of the Association for Computational Linguistics*,
  9:346–361, 2021.
- Hase et al. (2021)

  Peter Hase, Mona T. Diab, Asli Celikyilmaz, Xian Li, Zornitsa Kozareva, Veselin
  Stoyanov, Mohit Bansal, and Srinivasan Iyer.
  Do language models have beliefs? methods for detecting, updating, and
  visualizing model beliefs.
  *CoRR*, abs/2111.13654, 2021.
- He et al. (2021)

  Ruining He, Anirudh Ravula, Bhargav Kanagal, and Joshua Ainslie.
  Realformer: Transformer likes residual attention.
  In *Findings of the Association for Computational Linguistics:
  ACL-IJCNLP 2021*, pp. 929–943, 2021.
- Hendrycks & Gimpel (2016)

  Dan Hendrycks and Kevin Gimpel.
  Gaussian error linear units (gelus).
  *arXiv preprint arXiv:1606.08415*, 2016.
- Hendrycks et al. (2021)

  Dan Hendrycks, Collin Burns, Steven Basart, Andy Zou, Mantas Mazeika, Dawn
  Song, and Jacob Steinhardt.
  Measuring massive multitask language understanding.
  In *International Conference on Learning Representations*, 2021.
- Hoffmann et al. (2022)

  Jordan Hoffmann, Sebastian Borgeaud, Arthur Mensch, Elena Buchatskaya, Trevor
  Cai, Eliza Rutherford, Diego de Las Casas, Lisa Anne Hendricks, Johannes
  Welbl, Aidan Clark, et al.
  Training compute-optimal large language models.
  *arXiv preprint arXiv:2203.15556*, 2022.
- Hong et al. (2022)

  Wenyi Hong, Ming Ding, Wendi Zheng, Xinghan Liu, and Jie Tang.
  Cogvideo: Large-scale pretraining for text-to-video generation via
  transformers.
  *arXiv preprint arXiv:2205.15868*, 2022.
- Houlsby et al. (2019)

  Neil Houlsby, Andrei Giurgiu, Stanislaw Jastrzebski, Bruna Morrone, Quentin
  De Laroussilhe, Andrea Gesmundo, Mona Attariyan, and Sylvain Gelly.
  Parameter-efficient transfer learning for nlp.
  In *International Conference on Machine Learning*, pp. 2790–2799. PMLR, 2019.
- Huang et al. (2019)

  Yanping Huang, Youlong Cheng, Ankur Bapna, Orhan Firat, Dehao Chen, Mia Chen,
  HyoukJoong Lee, Jiquan Ngiam, Quoc V Le, Yonghui Wu, et al.
  Gpipe: Efficient training of giant neural networks using pipeline
  parallelism.
  *Advances in neural information processing systems*, 32, 2019.
- Jacobs & Wallach (2021)

  Abigail Z Jacobs and Hanna Wallach.
  Measurement and fairness.
  In *Proceedings of the 2021 ACM conference on fairness,
  accountability, and transparency*, pp. 375–385, 2021.
- Jiao et al. (2020)

  Xiaoqi Jiao, Yichun Yin, Lifeng Shang, Xin Jiang, Xiao Chen, Linlin Li, Fang
  Wang, and Qun Liu.
  Tinybert: Distilling bert for natural language understanding.
  In *Findings of the Association for Computational Linguistics:
  EMNLP 2020*, pp. 4163–4174, 2020.
- Joshi et al. (2017)

  Mandar Joshi, Eunsol Choi, Daniel S Weld, and Luke Zettlemoyer.
  Triviaqa: A large scale distantly supervised challenge dataset for
  reading comprehension.
  In *Proceedings of the 55th Annual Meeting of the Association
  for Computational Linguistics (Volume 1: Long Papers)*, pp. 1601–1611,
  2017.
- (48)

  Paul R Kingsbury and Martha Palmer.
  From treebank to propbank.
  Citeseer.
- Kwiatkowski et al. (2019)

  Tom Kwiatkowski, Jennimaria Palomaki, Olivia Redfield, Michael Collins, Ankur
  Parikh, Chris Alberti, Danielle Epstein, Illia Polosukhin, Jacob Devlin,
  Kenton Lee, et al.
  Natural questions: a benchmark for question answering research.
  *Transactions of the Association for Computational Linguistics*,
  7:453–466, 2019.
- Lacoste et al. (2019)

  Alexandre Lacoste, Alexandra Luccioni, Victor Schmidt, and Thomas Dandres.
  Quantifying the carbon emissions of machine learning.
  *CoRR*, abs/1910.09700, 2019.
- Lester et al. (2021)

  Brian Lester, Rami Al-Rfou, and Noah Constant.
  The power of scale for parameter-efficient prompt tuning.
  In *Proceedings of the 2021 Conference on Empirical Methods in
  Natural Language Processing*, pp. 3045–3059, 2021.
- Levesque et al. (2012)

  Hector Levesque, Ernest Davis, and Leora Morgenstern.
  The winograd schema challenge.
  In *Thirteenth international conference on the principles of
  knowledge representation and reasoning*, 2012.
- Li & Liang (2021)

  Xiang Lisa Li and Percy Liang.
  Prefix-tuning: Optimizing continuous prompts for generation.
  In *Proceedings of the 59th Annual Meeting of the Association
  for Computational Linguistics and the 11th International Joint Conference on
  Natural Language Processing (Volume 1: Long Papers)*, pp. 4582–4597, 2021.
- Li et al. (2021)

  Xiangyang Li, Yu Xia, Xiang Long, Zheng Li, and Sujian Li.
  Exploring text-transformers in aaai 2021 shared task: Covid-19 fake
  news detection in english.
  In *CONSTRAINT@AAAI*, 2021.
- Liang et al. (2021)

  Paul Pu Liang, Chiyu Wu, Louis-Philippe Morency, and Ruslan Salakhutdinov.
  Towards understanding and mitigating social biases in language
  models.
  In *Proceedings of the 38th International Conference on Machine
  Learning, ICML 2021, 18-24 July 2021, Virtual Event*, volume 139 of
  *Proceedings of Machine Learning Research*, pp. 6565–6576. PMLR,
  2021.
- Lieber et al. (2021)

  Opher Lieber, Or Sharir, Barak Lenz, and Yoav Shoham.
  Jurassic-1: Technical details and evaluation.
  *White Paper. AI21 Labs*, 2021.
- Lin (2004)

  Chin-Yew Lin.
  ROUGE: A package for automatic evaluation of summaries.
  In *Text Summarization Branches Out*, pp. 74–81, Barcelona,
  Spain, July 2004. Association for Computational Linguistics.
  URL <https://aclanthology.org/W04-1013>.
- Lin et al. (2022)

  Stephanie Lin, Jacob Hilton, and Owain Evans.
  TruthfulQA: Measuring how models mimic human falsehoods.
  In *Proceedings of the 60th Annual Meeting of the Association
  for Computational Linguistics (Volume 1: Long Papers)*, pp. 3214–3252,
  Dublin, Ireland, May 2022. Association for Computational Linguistics.
- Liu et al. (2021a)

  Pengfei Liu, Weizhe Yuan, Jinlan Fu, Zhengbao Jiang, Hiroaki Hayashi, and
  Graham Neubig.
  Pre-train, prompt, and predict: A systematic survey of prompting
  methods in natural language processing.
  *arXiv preprint arXiv:2107.13586*, 2021a.
- Liu et al. (2018)

  Peter J Liu, Mohammad Saleh, Etienne Pot, Ben Goodrich, Ryan Sepassi, Lukasz
  Kaiser, and Noam Shazeer.
  Generating wikipedia by summarizing long sequences.
  In *International Conference on Learning Representations*, 2018.
- Liu et al. (2021b)

  Xiao Liu, Yanan Zheng, Zhengxiao Du, Ming Ding, Yujie Qian, Zhilin Yang, and
  Jie Tang.
  Gpt understands, too.
  *arXiv preprint arXiv:2103.10385*, 2021b.
- Liu et al. (2022)

  Xiao Liu, Kaixuan Ji, Yicheng Fu, Weng Tam, Zhengxiao Du, Zhilin Yang, and Jie
  Tang.
  P-tuning: Prompt tuning can be comparable to fine-tuning across
  scales and tasks.
  In *Proceedings of the 60th Annual Meeting of the Association
  for Computational Linguistics (Volume 2: Short Papers)*, pp. 61–68, 2022.
- Loshchilov & Hutter (2019)

  Ilya Loshchilov and Frank Hutter.
  Decoupled weight decay regularization.
  In *7th International Conference on Learning Representations,
  ICLR 2019, New Orleans, LA, USA, May 6-9, 2019*, 2019.
- Michel et al. (2019)

  Paul Michel, Omer Levy, and Graham Neubig.
  Are sixteen heads really better than one?
  *Advances in neural information processing systems*, 32, 2019.
- Micikevicius et al. (2018)

  Paulius Micikevicius, Sharan Narang, Jonah Alben, Gregory Diamos, Erich Elsen,
  David Garcia, Boris Ginsburg, Michael Houston, Oleksii Kuchaiev, Ganesh
  Venkatesh, and Hao Wu.
  Mixed precision training.
  In *International Conference on Learning Representations*, 2018.
- Mihaylov et al. (2018)

  Todor Mihaylov, Peter Clark, Tushar Khot, and Ashish Sabharwal.
  Can a suit of armor conduct electricity? a new dataset for open book
  question answering.
  In *Proceedings of the 2018 Conference on Empirical Methods in
  Natural Language Processing*, pp. 2381–2391, 2018.
- Mitchell et al. (2022)

  Eric Mitchell, Charles Lin, Antoine Bosselut, Christopher D. Manning, and
  Chelsea Finn.
  Memory-based model editing at scale.
  In *International Conference on Machine Learning, ICML 2022,
  17-23 July 2022, Baltimore, Maryland, USA*, volume 162 of *Proceedings
  of Machine Learning Research*, pp. 15817–15831. PMLR, 2022.
- Mollas et al. (2020)

  Ioannis Mollas, Zoe Chrysopoulou, Stamatis Karlos, and Grigorios Tsoumakas.
  Ethos: an online hate speech detection dataset.
  *arXiv preprint arXiv:2006.08328*, 2020.
- Nadeem et al. (2021)

  Moin Nadeem, Anna Bethke, and Siva Reddy.
  Stereoset: Measuring stereotypical bias in pretrained language
  models.
  In *Proceedings of the 59th Annual Meeting of the Association
  for Computational Linguistics and the 11th International Joint Conference on
  Natural Language Processing (Volume 1: Long Papers)*, pp. 5356–5371, 2021.
- Nangia et al. (2020)

  Nikita Nangia, Clara Vania, Rasika Bhalerao, and Samuel Bowman.
  Crows-pairs: A challenge dataset for measuring social biases in
  masked language models.
  In *Proceedings of the 2020 Conference on Empirical Methods in
  Natural Language Processing (EMNLP)*, pp. 1953–1967, 2020.
- Narayanan et al. (2021)

  Deepak Narayanan, Amar Phanishayee, Kaiyu Shi, Xie Chen, and Matei Zaharia.
  Memory-efficient pipeline-parallel dnn training.
  In *International Conference on Machine Learning*, pp. 7937–7947. PMLR, 2021.
- Ohta et al. (2002)

  Tomoko Ohta, Yuka Tateisi, and Jin-Dong Kim.
  The genia corpus: An annotated research abstract corpus in molecular
  biology domain.
  In *HLT*, pp. 82–86, 2002.
- Paperno et al. (2016)

  Denis Paperno, Germán Kruszewski, Angeliki Lazaridou, Ngoc-Quan Pham,
  Raffaella Bernardi, Sandro Pezzelle, Marco Baroni, Gemma Boleda, and Raquel
  Fernández.
  The lambada dataset: Word prediction requiring a broad discourse
  context.
  In *Proceedings of the 54th Annual Meeting of the Association
  for Computational Linguistics (Volume 1: Long Papers)*, pp. 1525–1534,
  2016.
- Patterson et al. (2021)

  David A. Patterson, Joseph Gonzalez, Quoc V. Le, Chen Liang, Lluis-Miquel
  Munguia, Daniel Rothchild, David R. So, Maud Texier, and Jeff Dean.
  Carbon emissions and large neural network training.
  *CoRR*, abs/2104.10350, 2021.
- Pradhan et al. (2013)

  Sameer Pradhan, Alessandro Moschitti, Nianwen Xue, Hwee Tou Ng, Anders
  Björkelund, Olga Uryupina, Yuchen Zhang, and Zhi Zhong.
  Towards robust linguistic analysis using ontonotes.
  In *CoNLL*, pp. 143–152, 2013.
- Press et al. (2021)

  Ofir Press, Noah Smith, and Mike Lewis.
  Train short, test long: Attention with linear biases enables input
  length extrapolation.
  In *International Conference on Learning Representations*, 2021.
- Pu et al. (2021)

  Amy Pu, Hyung Won Chung, Ankur Parikh, Sebastian Gehrmann, and Thibault Sellam.
  Learning compact metrics for MT.
  In *Proceedings of the 2021 Conference on Empirical Methods in
  Natural Language Processing*, pp. 751–762, Online and Punta Cana,
  Dominican Republic, November 2021. Association for Computational Linguistics.
  doi: 10.18653/v1/2021.emnlp-main.58.
  URL <https://aclanthology.org/2021.emnlp-main.58>.
- Qiu et al. (2020)

  Xipeng Qiu, Tianxiang Sun, Yige Xu, Yunfan Shao, Ning Dai, and Xuanjing Huang.
  Pre-trained models for natural language processing: A survey.
  *Science China Technological Sciences*, 63(10):1872–1897, 2020.
- Radford et al. (2018)

  Alec Radford, Karthik Narasimhan, Tim Salimans, and Ilya Sutskever.
  Improving language understanding with unsupervised learning.
  2018.
- Radford et al. (2019)

  Alec Radford, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei, Ilya
  Sutskever, et al.
  Language models are unsupervised multitask learners.
  *OpenAI blog*, 1(8):9, 2019.
- Rae et al. (2021)

  Jack W Rae, Sebastian Borgeaud, Trevor Cai, Katie Millican, Jordan Hoffmann,
  Francis Song, John Aslanides, Sarah Henderson, Roman Ring, Susannah Young,
  et al.
  Scaling language models: Methods, analysis & insights from training
  gopher.
  *arXiv preprint arXiv:2112.11446*, 2021.
- Raffel et al. (2020)

  Colin Raffel, Noam Shazeer, Adam Roberts, Katherine Lee, Sharan Narang, Michael
  Matena, Yanqi Zhou, Wei Li, Peter J Liu, et al.
  Exploring the limits of transfer learning with a unified text-to-text
  transformer.
  *J. Mach. Learn. Res.*, 21(140):1–67, 2020.
- Ramesh et al. (2021)

  Aditya Ramesh, Mikhail Pavlov, Gabriel Goh, Scott Gray, Chelsea Voss, Alec
  Radford, Mark Chen, and Ilya Sutskever.
  Zero-shot text-to-image generation.
  In *International Conference on Machine Learning*, pp. 8821–8831. PMLR, 2021.
- Rasley et al. (2020)

  Jeff Rasley, Samyam Rajbhandari, Olatunji Ruwase, and Yuxiong He.
  Deepspeed: System optimizations enable training deep learning models
  with over 100 billion parameters.
  In *Proceedings of the 26th ACM SIGKDD International Conference
  on Knowledge Discovery & Data Mining*, pp. 3505–3506, 2020.
- Riedel et al. (2010)

  Sebastian Riedel, Limin Yao, and Andrew McCallum.
  Modeling relations and their mentions without labeled text.
  In *ECML-PKDD*, pp. 148–163, 2010.
- Roberts et al. (2020)

  Adam Roberts, Colin Raffel, and Noam Shazeer.
  How much knowledge can you pack into the parameters of a language
  model?
  In *Proceedings of the 2020 Conference on Empirical Methods in
  Natural Language Processing (EMNLP)*, pp. 5418–5426, 2020.
- Roth & Yih (2004)

  Dan Roth and Wen-tau Yih.
  A linear programming formulation for global inference in natural
  language tasks.
  In *HLT-NAACL*, pp. 1–8, 2004.
- Rudinger et al. (2018)

  Rachel Rudinger, Jason Naradowsky, Brian Leonard, and Benjamin Van Durme.
  Gender bias in coreference resolution.
  In *NAACL-HLT (2)*, 2018.
- (89)

  Chitwan Saharia, William Chan, Saurabh Saxena, Lala Li, Jay Whang, Emily
  Denton, Seyed Kamyar Seyed Ghasemipour, Raphael Gontijo-Lopes, Burcu Karagol
  Ayan, Tim Salimans, et al.
  Photorealistic text-to-image diffusion models with deep language
  understanding.
  In *Advances in Neural Information Processing Systems*.
- Sakaguchi et al. (2021)

  Keisuke Sakaguchi, Ronan Le Bras, Chandra Bhagavatula, and Yejin Choi.
  Winogrande: An adversarial winograd schema challenge at scale.
  *Communications of the ACM*, 64(9):99–106,
  2021.
- Sang & Meulder (2003)

  Erik F. Tjong Kim Sang and Fien De Meulder.
  Introduction to the conll-2003 shared task: Language-independent
  named entity recognition.
  In *HLT-NAACL*, pp. 142–147, 2003.
- Sanh et al. (2019)

  Victor Sanh, Lysandre Debut, Julien Chaumond, and Thomas Wolf.
  Distilbert, a distilled version of bert: smaller, faster, cheaper and
  lighter.
  *arXiv preprint arXiv:1910.01108*, 2019.
- Sanh et al. (2022)

  Victor Sanh, Albert Webson, Colin Raffel, Stephen Bach, Lintang Sutawika, Zaid
  Alyafeai, Antoine Chaffin, Arnaud Stiegler, Teven Le Scao, Arun Raja, et al.
  Multitask prompted training enables zero-shot task generalization.
  In *The Tenth International Conference on Learning
  Representations*, 2022.
- Scao et al. (2022)

  Teven Le Scao, Angela Fan, Christopher Akiki, Ellie Pavlick, Suzana Ilić,
  Daniel Hesslow, Roman Castagné, Alexandra Sasha Luccioni, François
  Yvon, Matthias Gallé, et al.
  Bloom: A 176b-parameter open-access multilingual language model.
  *arXiv preprint arXiv:2211.05100*, 2022.
- Schick et al. (2021)

  Timo Schick, Sahana Udupa, and Hinrich Schütze.
  Self-diagnosis and self-debiasing: A proposal for reducing
  corpus-based bias in nlp.
  *Transactions of the Association for Computational Linguistics*,
  9:1408–1424, 2021.
- Scialom et al. (2020)

  Thomas Scialom, Paul-Alexis Dray, Sylvain Lamprier, Benjamin Piwowarski, and
  Jacopo Staiano.
  MLSUM: The multilingual summarization corpus.
  In *Proceedings of the 2020 Conference on Empirical Methods in
  Natural Language Processing (EMNLP)*, pp. 8051–8067, Online, November
  2020. Association for Computational Linguistics.
  doi: 10.18653/v1/2020.emnlp-main.647.
  URL <https://aclanthology.org/2020.emnlp-main.647>.
- Shen et al. (2020)

  Sheng Shen, Zhen Dong, Jiayu Ye, Linjian Ma, Zhewei Yao, Amir Gholami,
  Michael W Mahoney, and Kurt Keutzer.
  Q-bert: Hessian based ultra low precision quantization of bert.
  In *Proceedings of the AAAI Conference on Artificial
  Intelligence*, volume 34, pp. 8815–8821, 2020.
- Sheng et al. (2021)

  Emily Sheng, Kai-Wei Chang, P. Natarajan, and Nanyun Peng.
  Societal biases in language generation: Progress and challenges.
  In *ACL*, 2021.
- Shleifer et al. (2021)

  Sam Shleifer, Jason Weston, and Myle Ott.
  Normformer: Improved transformer pretraining with extra
  normalization.
  *arXiv preprint arXiv:2110.09456*, 2021.
- Shoeybi et al. (2019)

  Mohammad Shoeybi, Mostofa Patwary, Raul Puri, Patrick LeGresley, Jared Casper,
  and Bryan Catanzaro.
  Megatron-lm: Training multi-billion parameter language models using
  model parallelism.
  *arXiv preprint arXiv:1909.08053*, 2019.
- Smith et al. (2022)

  Shaden Smith, Mostofa Patwary, Brandon Norick, Patrick LeGresley, Samyam
  Rajbhandari, Jared Casper, Zhun Liu, Shrimai Prabhumoye, George Zerveas,
  Vijay Korthikanti, et al.
  Using deepspeed and megatron to train megatron-turing nlg 530b, a
  large-scale generative language model.
  *arXiv preprint arXiv:2201.11990*, 2022.
- Srivastava et al. (2022)

  Aarohi Srivastava, Abhinav Rastogi, Abhishek Rao, Abu Awal Md Shoeb, Abubakar
  Abid, Adam Fisch, Adam R Brown, Adam Santoro, Aditya Gupta, Adrià
  Garriga-Alonso, et al.
  Beyond the imitation game: Quantifying and extrapolating the
  capabilities of language models.
  *arXiv preprint arXiv:2206.04615*, 2022.
- Strubell et al. (2019)

  Emma Strubell, Ananya Ganesh, and Andrew McCallum.
  Energy and policy considerations for deep learning in NLP.
  In *Proceedings of the 57th Conference of the Association for
  Computational Linguistics, ACL 2019, Florence, Italy, July 28- August 2,
  2019, Volume 1: Long Papers*, pp. 3645–3650. Association for Computational
  Linguistics, 2019.
- Su et al. (2021)

  Jianlin Su, Yu Lu, Shengfeng Pan, Bo Wen, and Yunfeng Liu.
  Roformer: Enhanced transformer with rotary position embedding.
  *arXiv preprint arXiv:2104.09864*, 2021.
- Talmor et al. (2019)

  Alon Talmor, Jonathan Herzig, Nicholas Lourie, and Jonathan Berant.
  Commonsenseqa: A question answering challenge targeting commonsense
  knowledge.
  In *Proceedings of the 2019 Conference of the North American
  Chapter of the Association for Computational Linguistics: Human Language
  Technologies, Volume 1 (Long and Short Papers)*, pp. 4149–4158, 2019.
- Tao et al. (2022)

  Chaofan Tao, Lu Hou, Wei Zhang, Lifeng Shang, Xin Jiang, Qun Liu, Ping Luo, and
  Ngai Wong.
  Compression of generative pre-trained language models via
  quantization.
  In *Proceedings of the 60th Annual Meeting of the Association
  for Computational Linguistics (Volume 1: Long Papers)*, pp. 4821–4836,
  2022.
- Thoppilan et al. (2022)

  Romal Thoppilan, Daniel De Freitas, Jamie Hall, Noam Shazeer, Apoorv
  Kulshreshtha, Heng-Tze Cheng, Alicia Jin, Taylor Bos, Leslie Baker, Yu Du,
  et al.
  Lamda: Language models for dialog applications.
  *arXiv preprint arXiv:2201.08239*, 2022.
- Timonin et al. (2022)

  Denis Timonin, Bo Yang Hsueh, and Vinh Nguyen.
  Accelerated inference for large transformer models using nvidia
  triton inference server.
  *NVIDIA blog*, 2022.
- Valiant (1990)

  Leslie G Valiant.
  A bridging model for parallel computation.
  *Communications of the ACM*, 33(8):103–111,
  1990.
- Vaswani et al. (2017)

  Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones,
  Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin.
  Attention is all you need.
  *Advances in neural information processing systems*, 30, 2017.
- Wadden et al. (2019)

  David Wadden, Ulme Wennberg, Yi Luan, and Hannaneh Hajishirzi.
  Entity, relation, and event extraction with contextualized span
  representations.
  In *Proceedings of the 2019 Conference on Empirical Methods in
  Natural Language Processing and the 9th International Joint Conference on
  Natural Language Processing (EMNLP-IJCNLP)*, pp. 5784–5789, 2019.
- Walker & Consortium (2005)

  C. Walker and Linguistic Data Consortium.
  *ACE 2005 Multilingual Training Corpus*.
  Linguistic Data Consortium, 2005.
  ISBN 9781585633760.
- Wang et al. (2019)

  Alex Wang, Yada Pruksachatkun, Nikita Nangia, Amanpreet Singh, Julian Michael,
  Felix Hill, Omer Levy, and Samuel R. Bowman.
  SuperGLUE: A Stickier Benchmark for General-Purpose
  Language Understanding Systems.
  In *NeurIPS 2019*, pp. 3261–3275, 2019.
- Wang & Komatsuzaki (2021)

  Ben Wang and Aran Komatsuzaki.
  GPT-J-6B: A 6 Billion Parameter Autoregressive Language Model.
  <https://github.com/kingoflolz/mesh-transformer-jax>, May 2021.
- Wang et al. (2022a)

  Chenguang Wang, Xiao Liu, Zui Chen, Haoyun Hong, Jie Tang, and Dawn Song.
  Deepstruct: Pretraining of language models for structure prediction.
  In *Findings of the Association for Computational Linguistics:
  ACL 2022*, pp. 803–823, 2022a.
- Wang et al. (2022b)

  Hongyu Wang, Shuming Ma, Li Dong, Shaohan Huang, Dongdong Zhang, and Furu Wei.
  Deepnet: Scaling transformers to 1,000 layers.
  *arXiv preprint arXiv:2203.00555*, 2022b.
- Wang et al. (2021)

  Shuohuan Wang, Yu Sun, Yang Xiang, Zhihua Wu, Siyu Ding, Weibao Gong, Shikun
  Feng, Junyuan Shang, Yanbin Zhao, Chao Pang, et al.
  Ernie 3.0 titan: Exploring larger-scale knowledge enhanced
  pre-training for language understanding and generation.
  *arXiv preprint arXiv:2112.12731*, 2021.
- Wang et al. (2020)

  Wenhui Wang, Furu Wei, Li Dong, Hangbo Bao, Nan Yang, and Ming Zhou.
  Minilm: Deep self-attention distillation for task-agnostic
  compression of pre-trained transformers.
  *Advances in Neural Information Processing Systems*,
  33:5776–5788, 2020.
- Wang et al. (2022c)

  Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le, Ed Chi, and Denny Zhou.
  Rationale-augmented ensembles in language models.
  *arXiv preprint arXiv:2207.00747*, 2022c.
- Wei et al. (2022a)

  Jason Wei, Maarten Bosma, Vincent Zhao, Kelvin Guu, Adams Wei Yu, Brian Lester,
  Nan Du, Andrew M Dai, and Quoc V Le.
  Finetuned language models are zero-shot learners.
  In *International Conference on Learning Representations*,
  2022a.
- Wei et al. (2022b)

  Jason Wei, Yi Tay, Rishi Bommasani, Colin Raffel, Barret Zoph, Sebastian
  Borgeaud, Dani Yogatama, Maarten Bosma, Denny Zhou, Donald Metzler, et al.
  Emergent abilities of large language models.
  *arXiv preprint arXiv:2206.07682*, 2022b.
- Wei et al. (2022c)

  Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Ed Chi, Quoc Le, and
  Denny Zhou.
  Chain of thought prompting elicits reasoning in large language
  models.
  *arXiv preprint arXiv:2201.11903*, 2022c.
- Weidinger et al. (2021)

  Laura Weidinger, John Mellor, Maribeth Rauh, Conor Griffin, Jonathan Uesato,
  Po-Sen Huang, Myra Cheng, Mia Glaese, Borja Balle, Atoosa Kasirzadeh, et al.
  Ethical and social risks of harm from language models.
  *arXiv preprint arXiv:2112.04359*, 2021.
- Wu et al. (2021)

  Shaohua Wu, Xudong Zhao, Tong Yu, Rongguo Zhang, Chong Shen, Hongli Liu, Feng
  Li, Hong Zhu, Jiangang Luo, Liang Xu, et al.
  Yuan 1.0: Large-scale pre-trained language model in zero-shot and
  few-shot learning.
  *arXiv preprint arXiv:2110.04725*, 2021.
- Xian et al. (2018)

  Yongqin Xian, Christoph H Lampert, Bernt Schiele, and Zeynep Akata.
  Zero-shot learning—a comprehensive evaluation of the good, the bad
  and the ugly.
  *IEEE transactions on pattern analysis and machine
  intelligence*, 41(9):2251–2265, 2018.
- Xiong et al. (2020)

  Ruibin Xiong, Yunchang Yang, Di He, Kai Zheng, Shuxin Zheng, Chen Xing,
  Huishuai Zhang, Yanyan Lan, Liwei Wang, and Tieyan Liu.
  On layer normalization in the transformer architecture.
  In *International Conference on Machine Learning*, pp. 10524–10533. PMLR, 2020.
- Xu et al. (2020)

  Liang Xu, Hai Hu, Xuanwei Zhang, Lu Li, Chenjie Cao, Yudong Li, Yechen Xu, Kai
  Sun, Dian Yu, Cong Yu, et al.
  Clue: A chinese language understanding evaluation benchmark.
  In *Proceedings of the 28th International Conference on
  Computational Linguistics*, pp. 4762–4772, 2020.
- Xu et al. (2021)

  Liang Xu, Xiaojing Lu, Chenyang Yuan, Xuanwei Zhang, Huilin Xu, Hu Yuan, Guoao
  Wei, Xiang Pan, Xin Tian, Libo Qin, et al.
  Fewclue: A chinese few-shot learning evaluation benchmark.
  *arXiv preprint arXiv:2107.07498*, 2021.
- Yuan et al. (2021)

  Sha Yuan, Hanyu Zhao, Zhengxiao Du, Ming Ding, Xiao Liu, Yukuo Cen, Xu Zou,
  Zhilin Yang, and Jie Tang.
  Wudaocorpora: A super large-scale chinese corpora for pre-training
  language models.
  *AI Open*, 2:65–68, 2021.
- Zafrir et al. (2019)

  Ofir Zafrir, Guy Boudoukh, Peter Izsak, and Moshe Wasserblat.
  Q8bert: Quantized 8bit bert.
  In *2019 Fifth Workshop on Energy Efficient Machine Learning and
  Cognitive Computing-NeurIPS Edition (EMC2-NIPS)*, pp. 36–39. IEEE, 2019.
- Zeng et al. (2021)

  Wei Zeng, Xiaozhe Ren, Teng Su, Hui Wang, Yi Liao, Zhiwei Wang, Xin Jiang,
  ZhenZhang Yang, Kaisheng Wang, Xiaoda Zhang, et al.
  Pangu-\α\backslash\alpha: Large-scale autoregressive pretrained
  chinese language models with auto-parallel computation.
  *arXiv preprint arXiv:2104.12369*, 2021.
- Zhang et al. (2021)

  Chiyuan Zhang, Daphne Ippolito, Katherine Lee, Matthew Jagielski, Florian
  Tramèr, and Nicholas Carlini.
  Counterfactual memorization in neural language models.
  *CoRR*, abs/2112.12938, 2021.
- Zhang et al. (2022)

  Susan Zhang, Stephen Roller, Naman Goyal, Mikel Artetxe, Moya Chen, Shuohui
  Chen, Christopher Dewan, Mona Diab, Xian Li, Xi Victoria Lin, et al.
  Opt: Open pre-trained transformer language models.
  *arXiv preprint arXiv:2205.01068*, 2022.
- Zhang et al. (2017)

  Yuhao Zhang, Victor Zhong, Danqi Chen, Gabor Angeli, and Christopher D.
  Manning.
  Position-aware attention and supervised data improve slot filling.
  In *EMNLP*, pp. 35–45, 2017.
- Zhou et al. (2019)

  Ben Zhou, Daniel Khashabi, Qiang Ning, and Dan Roth.
  “going on a vacation” takes longer than “going for a walk”: A
  study of temporal commonsense understanding.
  In *Proceedings of the 2019 Conference on Empirical Methods in
  Natural Language Processing and the 9th International Joint Conference on
  Natural Language Processing (EMNLP-IJCNLP)*, pp. 3363–3369, 2019.
- Zhu et al. (2020)

  Chen Zhu, Ankit Singh Rawat, Manzil Zaheer, Srinadh Bhojanapalli, Daliang Li,
  Felix X. Yu, and Sanjiv Kumar.
  Modifying memories in transformer models.
  *CoRR*, abs/2012.00363, 2020.

## 附录

### 附录 A 伦理：偏见与毒性评测

尽管 LLM 在语言及更广领域拥有强大能力、能为人类带来可观福祉，它们也可能产生有毒与非法内容并被用于恶意用途（[Weidinger et al., 2021](#bib.bib123)；[Sheng et al., 2021](#bib.bib98)；[Dev et al., 2021](#bib.bib23)；[Bommasani et al., 2021](#bib.bib11)）。对于 GLM-130B，在向申请者授予模型权重之前，我们在模型许可证中要求申请者同意不会将其用于任何可能危害社会与人类的行径。

此外，从技术角度看，我们认为也必须理解 LLM 的有毒与偏见行为，并最终消除它们。这与我们对「LLM 包容性（LLM Inclusivity）」的承诺一致——让更多人参与开源 LLM 研究才能推动这一进程。而且，如果一个 LLM 被证明擅长识别有毒与偏见内容，那么诸如自我诊断（[Schick et al., 2021](#bib.bib95)）之类的技术可以在一个自洽的后处理流程中帮助减少有害生成。因此，作为第一步，我们在多种相关基准上评测 GLM-130B，以照亮这一充满挑战的课题。尽管这些基准存在局限（[Blodgett et al., 2021](#bib.bib10)；[Jacobs & Wallach, 2021](#bib.bib45)）、有待未来工作解决，它们仍是唤起社区对该问题关注的一个良好开端。

#### A.1 偏见度量：CrowS-Pairs

表 5：CrowS-Pairs（[Nangia et al., 2020](#bib.bib70)）偏见度量。分数越低越好。

| 类别 | GPT-3 | OPT-175B | GLM-130B |
| --- | --- | --- | --- |
| 性别 | 62.6 | 65.7 | 55.7 |
| 宗教 | 73.3 | 68.6 | 73.3 |
| 种族/肤色 | 64.7 | 68.6 | 58.5 |
| 性取向 | 76.2 | 78.6 | 60.7 |
| 年龄 | 64.4 | 67.8 | 63.2 |
| 国籍 | 61.6 | 62.9 | 64.1 |
| 残障 | 76.7 | 76.7 | 71.6 |
| 外貌 | 74.6 | 76.2 | 74.6 |
| 社会经济地位 | 73.8 | 76.2 | 70.9 |
| 总体 | 67.2 | 69.5 | 65.8 |

CrowS-Pairs（[Nangia et al., 2020](#bib.bib70)），即众包刻板印象对（Crowdsourced Stereotype Pairs）基准，被广泛用于度量掩码语言模型的偏见。它收集了 1508 个例子，覆盖九种不同的常见偏见，并采用基于探针的方法，比较一对刻板印象句与反刻板印象句的伪对数似然。由于 GLM-130B 以自回归空白填充预训练，CrowS-Pairs 评测可以直接适用。我们将（[Zhang et al., 2022](#bib.bib133)）中报告的 GPT-3 Davinci 与 OPT-175B 在 CrowS-Pairs 上的结果与 GLM-130B 进行比较。

我们的结果见表 5。除宗教与国籍外，GLM-130B 在几乎所有类型的刻板印象上都表现出更少的偏见。我们推测这是因为 GLM-130B 是双语预训练 LLM，会同时从英文与中文语料中学习特定内容的语义。由于 CrowS-Pairs 的刻板印象主要取自美国平等就业机会委员会的清单²，两种不同文化与语言中的偏见分布可能不同，从而在一个原本为英语社会设计的基准上，调和了 GLM-130B 的社会偏见。我们认为这是一个有趣的发现——多语言预训练或许能帮助 LLM 呈现更少的有害偏见、实现更好的公平性。最后，我们也承认 GLM-130B 反过来可能呈现某些特有的中文偏见，目前尚缺乏相应的测试基准，需要大量未来努力去检测与防范。

² <https://www.eeoc.gov/prohibited-employment-policiespractices>

#### A.2 偏见度量：StereoSet

另一个广泛使用的偏见与刻板印象评测基准是 StereoSet（[Nadeem et al., 2021](#bib.bib69)），它也被（[Lieber et al., 2021](#bib.bib56)；[Artetxe et al., 2021](#bib.bib3)；[Zhang et al., 2022](#bib.bib133)）采用。为在偏见检测与语言建模质量之间取得平衡，StereoSet 报告一系列指标，包括语言建模分数（LMS）、刻板印象分数（SS），以及作为总体平均指标的理想化语境关联测试分数（ICAT）。例如，给定前提「She is the twin's mother」，StereoSet 提供三个候选假设：1）「the water is deep」；2）「she is a lazy, unkind person」；3）「she is a kind, caring woman」。第一个选项作为干扰项，用于测试模型的语言能力并计算 LMS；第二、第三个陈述分别是对刻板印象的反转与符合，用于计算 SS。这里一种被广泛采用的技术是按选项长度校准其似然（[Lieber et al., 2021](#bib.bib56)；[Zhang et al., 2022](#bib.bib133)），因为干扰项特别短。

遵循（[Zhang et al., 2022](#bib.bib133)），我们按 token 而非字符（[Lieber et al., 2021](#bib.bib56)）对分数做归一化，以得到用于计算指标的模型预测。结果见表 6。可以看到，GLM-130B 在所有指标上都大幅超越 GPT-3 Davinci 与 OPT-175B。这一结果与我们在语言建模实验与 CrowS-Pairs 偏见评测中的发现精确吻合：GLM-130B 在语言建模与社会公平两方面都具备高质量。

表 6：StereoSet（[Nadeem et al., 2021](#bib.bib69)）偏见度量，LMS（↑）、SS（↓）与 ICAT（↑）。

| 类别 | 职业 | | | 性别 | | | 宗教 | | | 种族 | | | 总体 | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 指标 | LMS | SS | ICAT | LMS | SS | ICAT | LMS | SS | ICAT | LMS | SS | ICAT | LMS | SS | ICAT |
| GPT-3 | 78.4 | 63.4 | 57.5 | 75.6 | 66.5 | 50.6 | 80.8 | 59.0 | 66.3 | 77.0 | 57.4 | 65.7 | 77.6 | 60.8 | 60.8 |
| OPT-175B | 74.1 | 62.6 | 55.4 | 74.0 | 63.6 | 53.8 | 84.0 | 59.0 | 68.9 | 74.9 | 56.8 | 64.8 | 74.8 | 59.9 | 60.0 |
| GLM-130B | 86.5 | 59.6 | 69.9 | 83.9 | 63.5 | 61.2 | 91.0 | 53.5 | 84.6 | 85.7 | 54.1 | 78.7 | 86.0 | 57.3 | 73.5 |

#### A.3 仇恨言论检测：ETHOS

社交媒体语料可能包含仇恨言论，考察 LLM 在多大程度上了解并能够帮助识别它们至关重要。我们采用最初由（[Mollas et al., 2020](#bib.bib68)）提出的 ETHOS 数据集，在（[Chiu & Alexander, 2021](#bib.bib17)）构建的零样本或少样本数据集上检测性别歧视与种族主义言论。GPT-3 Davinci（GPT-3 175B 的一个公开可用变体）与 OPT 175B 也在该基准上被测试（其结果报告于（[Zhang et al., 2022](#bib.bib133)））。对于包括 Zero-shot、One-shot 与 Few-shot（binary）（回答「yes」或「no」）在内的二分类，我们报告二分类 F1；对于多分类（回答「yes」「no」或「neither」），我们报告 micro F1。我们采用的提示词与（[Chiu & Alexander, 2021](#bib.bib17)）几乎相同，只是将 Few-shot（binary）提示词对齐到 One-shot 所用的形式，并在原始 Few-shot（multiclass）提示词的冒号前加上单词「Classification」。

表 7：ETHOS（[Mollas et al., 2020](#bib.bib68)）仇恨言论检测。「(bi)」与「(mul)」分别表示二分类与多分类。所有分数均为 F1，越高越好。

| | GPT-3 | OPT-175B | GLM-130B |
| --- | --- | --- | --- |
| Zero-shot | 62.8 | 66.7 | 68.8 |
| One-shot | 61.6 | 71.3 | 79.1 |
| Few-shot (bi) | 35.4 | 75.9 | 79.7 |
| Few-shot (mul) | 67.2 | 81.2 | 85.8 |

结果见表 7。我们发现 GLM-130B 在四种不同设置下均优于另外两个 LLM。一方面，GLM-130B 在来自在线论坛与社交媒体的无监督多样语料（包括「hackernews」「stackexchange」「pile_cc」等分片）上的预训练，可以赋予模型识别这类言论的背景知识；另一方面，MIP 训练也可能提升 GLM-130B 的零样本与少样本能力。

#### A.4 毒性生成：RealToxicPrompts

图 9：RealToxicPrompts（[Gehman et al., 2020](#bib.bib33)）评测。续写的毒性概率越低越好。

评测模型在给定提示下生成的毒性，是其安全部署的重要组成部分。我们在 RealToxicPrompts（[Gehman et al., 2020](#bib.bib33)）数据集上评测 GLM-130B 的毒性生成。遵循其设置，我们使用核采样（p=0.9）为随机抽样的 10K 条提示各生成 25 个续写，并将最大生成长度限制为 128 个 token。随后我们报告由 Perspective API³ 评估的 25 个续写的平均毒性概率。为了在不同分词方法下进行公平比较，我们只报告续写中第一个完整句子的毒性分数，因为我们发现 Perspective API 返回的分数似乎随句子长度增加而升高。

³ <https://www.perspectiveapi.com/>

结果见图 9。总体而言，随着给定提示毒性的增加，两个模型续写的毒性概率都相应上升。与 GPT-3 Davinci 相比，GLM-130B 在所有情况下都具有更低的毒性率，表明 GLM-130B 不太容易生成有毒内容。

![图 10](2210.02414v2/collapse.png)

图 10：处理训练崩溃与不稳定是训练 LLM 时的第一要务。

### 附录 B 技术细节

本节介绍我们在 GLM-130B 训练全程中发现并解决的技术问题的额外细节。连同同期的开源 LLM 努力，我们相信这些公开的细节可以作为未来 LLM 训练的重要基石。

#### B.1 分词

对于语料的分词，我们基于 icetk 包实现了一个文本分词器并做了若干调整。作为一个图文统一分词器，icetk 的词表大小为 150000：前 20000 个 token 是图像 token，其余是文本 token。icetk 的文本分词器由 sentencepiece⁴ 在一份 25GB、中英文内容各半的双语语料上构建和训练。我们将分词器识别的 token 划分为四类：通用 token 编号从 No.20000 到 No.20099，由不含扩展定义的标点、数字与空格构成；No.20100 至 No.83822 为英文 token；No.83823 至 No.145653 为中文 token；No.145653 之后是其他特殊 token，包括连接的标点与其他语言的片段等。

⁴ <https://github.com/google/sentencepiece>

在我们的实现中，我们忽略前 20000 个图像 token，仅使用面向文本分词的后 130000 个。我们启用对换行符的分词，将换行标记 \n 分词为 No.20004 token `<n>`。在原有 token 的基础上，我们为模型预测添加了特殊 token [MASK] 与 [gMASK]，并添加特殊 token `<sop>`、`<eop>`、`<eos>` 用于句子与段落分隔。

#### B.2 层归一化

这里我们简要介绍层归一化在语言建模问题中的历史、其变体在近期 LLM 中的表现，以及我们在 GLM-130B 上对它们进行的实验。

Post-LN（[Vaswani et al., 2017](#bib.bib110)）。Post-LN 与 transformer 架构一同提出，被放置在残差块之间。它随后被 BERT（[Devlin et al., 2019](#bib.bib24)）用于双向语言模型预训练。然而，Post-LN 后来被指会导致 transformer 收敛缓慢且脆弱（[Xiong et al., 2020](#bib.bib126)），Pre-LN 随之作为替代出现。

Pre-LN（[Xiong et al., 2020](#bib.bib126)）。相反，Pre-LN 位于残差块内部，可减少梯度爆炸，在既有语言模型中占主导地位，包括所有近期的 LLM。然而，OPT-175B（[Zhang et al., 2022](#bib.bib133)）、BLOOM（[Scao et al., 2022](#bib.bib94)）与文生图模型 CogView（[Ding et al. (2021)](#bib.bib25)）后来观察到，当模型扩展到 100B 或遇到多模态数据时，Pre-LN 仍无法应对脆弱的训练。这一点也在 GLM-130B 的初步实验中得到验证：Pre-LN 在其训练早期持续崩溃。

此外，Pre-LN transformer 的另一个深层问题是，与 Post-LN 相比，它可能损害微调之后的模型性能。这一现象在（[He et al., 2021](#bib.bib38)）中被观察到。

Sandwich-LN（[Ding et al., 2021](#bib.bib25)）。作为补救，CogView（以及后来的 Normformer（[Shleifer et al., 2021](#bib.bib99)））在 Pre-LN 基础上开发了 Sandwich-LN，在每个残差分支的末端追加额外的归一化。配合 PB-Relax（精度瓶颈松弛，Precision-Bottleneck Relaxation）技术，它们稳定了一个 40 亿参数文生图模型的训练。尽管优于 Pre-LN，遗憾的是 Sandwich-LN 在 GLM-130B 训练中同样被证明会崩溃；更不用说其 Pre-LN 本质可能带来的更弱微调性能。

#### B.3 位置编码与前馈网络

**位置编码。** 原始 transformer 采用绝对（正弦）位置编码，后来演化为相对位置编码（[Dai et al., 2019](#bib.bib20)）。相对 PE 比绝对位置编码能更好地捕捉词间相关性。旋转位置编码（RoPE，[Su et al., 2021](#bib.bib104)）是一种以绝对位置编码形式实现的相对位置编码，其核心思想如以下公式所示：

$$
(\bm{R}_{m}q)^{\top}(\bm{R}_{n}k)=q^{\top}\bm{R}_{m}^{\top}\bm{R}_{n}k=q^{\top}\bm{R}_{n-m}k \tag{1}
$$

位置 $m$ 的 $q$ 与位置 $n$ 的 $k$ 的乘积只与它们的距离 $n-m$ 相关，这体现了该位置编码的相对性。上式中 $\bm{R}$ 的定义为

$$
\bm{R}_{\theta,m}^{d}=\left(\begin{array}[]{ccccccc}\cos m\theta_{1}&-\sin m\theta_{1}&0&0&\cdots&0&0\\ \sin m\theta_{1}&\cos m\theta_{1}&0&0&\cdots&0&0\\ 0&0&\cos m\theta_{2}&-\sin m\theta_{2}&\cdots&0&0\\ \ 0&0&\sin m\theta_{2}&\cos m\theta_{2}&\cdots&0&0\\ \ \vdots&\vdots&\vdots&\vdots&\ddots&\vdots&\vdots\\ 0&0&0&0&\cdots&\cos m\theta_{d/2}&-\sin m\theta_{d/2}\\ 0&0&0&0&\cdots&\sin m\theta_{d/2}&\cos m\theta_{d/2}\end{array}\right) \tag{2}
$$

为了让其值随距离增加而衰减，$\theta$ 取值为

$$
\theta=\left\{\theta_{i}=10000^{\frac{-2(i-1)}{d}},\quad i\in\left[1,2,\cdots,\frac{d}{2}\right]\right\} \tag{3}
$$

原始 GLM 提出了一种二维绝对位置编码方法，用于同时建模 span 内与 span 间的位置信息。在 GLM-130B 中，与原始 GLM 使用的二维位置编码不同，我们回归到传统的一维位置编码。原因在于我们最初认为二维形式无法直接应用于 RoPE⁵。作为替代方案，我们在 GLM-130B 中直接移除了原始 GLM 使用的第二维，因为我们发现 [MASK] 生成所用的单向注意力掩码子矩阵同样能指示 token 顺序。基于这一观察，我们按以下策略将 GLM-130B 的位置编码转换为一维：

⁵ 我们后来从其作者的博客 <https://kexue.fm/archives/8397> 找到了实现二维 RoPE 的说明，但那时我们的训练已经进行了数周。

- 对于被短 span 破坏的序列，我们丢弃第二维位置编码。
- 对于末尾被长 span 破坏的序列，我们将位置 id 改为一维的 $0,1,\cdots,s-1$，生成的 token 将直接从最后一个上下文 token $s-1$ 起延长第一维位置编码。

**前馈网络。** 近期一些改进 transformer 架构的努力集中在 FFN 上，包括用 GLU 替换它（PaLM 采用）。研究表明使用 GLU 可以提升模型性能，这与我们的实验结果一致（参见表 8）。具体而言，我们使用带 GeLU（[Hendrycks & Gimpel, 2016](#bib.bib39)）激活的 GLU，即

$$
\operatorname{FFN}_{\mathrm{GeGLU}}\left(\bm{x};\bm{W}_{1},\bm{V},\bm{W}_{2}\right)=\left(\mathrm{GeLU}(\bm{x}\bm{W}_{1})\otimes\bm{x}\bm{V}\right)\bm{W}_{2} \tag{4}
$$

为了保持与原始 FFN 相同的参数量，前馈层尺寸 $d_{\mathrm{ffn}}$（通常为 $4d_{\mathrm{H}}$，其中 $d_{\mathrm{H}}$ 为隐藏维度）由于额外引入了 $\bm{V}$ 而缩减为 $\frac{8}{3}d_{\mathrm{H}}$。

表 8：GLMBase 上 PE 与 FFN 的消融研究

| 模型 | 测试 PPL |
| --- | --- |
| GLMBase | 24.58 |
| + ALiBi | 24.14 |
| + RoPE | 22.95 |
| + RoPE + GeGLU | 22.31 |

**PE 与 FFN 的消融研究。** 为验证我们的 PE 与 FFN 选择，我们在实验中在一个随机抽取的 50G 中英混合语料上预训练 GLMBase（110M）来测试它们。我们将绝对 PE 与两种近期流行的相对 PE 变体——RoPE（[Chowdhery et al., 2022](#bib.bib18)）与 ALiBi（[Press et al., 2021](#bib.bib76)）——进行比较。对于 FFN，我们将原始 FFN 与带 GeLU 激活的门控线性单元（GLU）进行比较。表 8 的结果表明，ALiBi 与 RoPE 都能改善测试集困惑度，其中 RoPE 的提升更显著，而使用 GeGLU 可以进一步提升模型性能。

#### B.4 流水线并行分析

(a) 朴素的流水线实现，可能极其低效。

(b) GPipe（[Huang et al., 2019](#bib.bib44)）实现。

(c) Pipedream（[Narayanan et al., 2021](#bib.bib71)）实现（GLM-130B 采用）。

图 11：不同流水线策略及其概念对比。

在流水线并行中，每个阶段包含三种操作（参见图 11(a)）：前向（记为 F）、反向（记为 B）与优化器更新（记为 U）。然而，朴素的顺序流水线实现会导致难以承受的气泡（bubble）数量。改进的 GPipe（[Huang et al., 2019](#bib.bib44)）（参见图 11(b)）策略通过将数据切分为微批次大幅减少气泡；微批次越多，一次迭代中可以同时计算的阶段就越多。近期的 PipeDream-Flush（[Narayanan et al., 2021](#bib.bib71)）（参见图 11(c)）通过交错不同阶段的前向与反向进一步优化了 GPU 显存使用，以减少前向激活的显存占用。

我们通过假设流水线段数为 $p$、微批次数量为 $m$、每个微批次的前向与反向耗时分别为 $t_{f}$ 与 $t_{b}$，来分析 GLM-130B 预训练中的气泡占比。理想情况下，前向与反向耗时 $t_{\mathrm{ideal}}=m(t_{f}+t_{b})$。但实践中，默认的流水线传递策略分别造成 $p-1$ 次前向传播与 $p-1$ 次反向传播气泡，总耗时 $t_{\mathrm{bubble}}=(p-1)(t_{f}+t_{b})$，因此气泡占比为

$$
\text{bubble-ratio}=\frac{t_{\mathrm{bubble}}}{t_{\mathrm{ideal}}+t_{\mathrm{bubble}}}=\frac{p-1}{m+p-1} \tag{5}
$$

当微批次数量较大时，气泡比例会降低到可接受的水平。特别地，GPipe（[Huang et al. (2019)](#bib.bib44)）的实验表明，当 $m\geq 4p$ 时，由于反向传播中的前向重计算技术允许部分计算与通信重叠，流水线气泡时间的总占比降至可忽略的水平，这说明流水线模型并行引入的气泡不会严重损耗训练效率。

一般来说，为了充分利用硬件，常见做法是将模型放入由多个节点组成的模型并行组，并尽量用满每个节点的显存。在这种情况下，我们可以自由调整流水线模型并行与张量模型并行的比例。由于数据并行几乎不影响计算时间，我们假设数据并行规模为 $d=1$、节点总数为 $n$、张量模型并行规模为 $t$、流水线模型并行规模为 $p$，且满足 $n=t\times p$，则此时气泡占比为

$$
\text{bubble-ratio}=\frac{n/t-1}{m+n/t-1} \tag{6}
$$

由上式可见，增大张量并行规模会进一步降低气泡比例。然而，张量并行规模不能无限增大，否则会导致计算粒度下降，并在超过一定阈值后大幅增加通信开销。因此我们可以得出结论：张量模型并行规模应随模型规模增大而缓慢增加，但不应超过单机显卡数量。在 GLM-130B 的训练中，实验表明最优张量并行规模为 $t=4$，在 DGX-A100 系统中没有扩展到 $t=8$ 的规模。其他参数为 $m=176$、$p=8$，计算得气泡占比仅为 3.8%，足以证明流水线模型并行的效率。

#### B.5 推理加速

表 9：我们实测中 BLOOM-176B（[Scao et al., 2022](#bib.bib94)）（来自 Huggingface Transformers）与 GLM-130B 实现在 16 位精度、8×A100（80G）下的解码速度。

| 解码 token 数 | 128 | 512 | 1024 | 2048 |
| --- | --- | --- | --- | --- |
| BLOOM-176B | 36.76s | 137.91s | 287.93s | 631.81s |
| GLM-130B | 4.40s（×8.4） | 18.77s（×7.3） | 39.81s（×7.2） | 89.88s（×7.0） |

模型的纯 PyTorch 实现易于阅读与运行，但对 LLM 而言可能慢得难以忍受。基于 NVIDIA 的 FasterTransformer⁶，我们花费两个月将 GLM-130B 用 C++ 实现，以加速推理，主要包括以下优化：

⁶ <https://github.com/NVIDIA/FasterTransformer>

- 优化 GeGLU、层归一化、SoftMax 等耗时操作。
- 减少 GPU kernel 调用次数（例如将 MultiheadAttention 融合为一个计算 kernel）。
- 调用 cuBLAS 时指定性能最佳的算法。
- 通过提前转置模型参数提升计算效率。
- 在 FP16 计算中使用 half2，使 half 的访问带宽与计算吞吐翻倍。

目前我们已将 GLM-130B 的完整 FasterTransformer 实现打包为即插即用的 docker 镜像以方便用户使用；我们仍在努力使其适配我们的 PyTorch 实现——只需改动一行代码。我们加速版 GLM-130B 实现与迄今 Huggingface Transformers 中默认可用的 BLOOM-176B 实现⁷的对比见表 9。我们的 GLM-130B 实现可以比 BLOOM-176B 的 PyTorch 实现快 7.0 至 8.4 倍。为使 LLM 达到可容忍的响应速度而付出的努力，对其普及可能至关重要。

⁷ <https://huggingface.co/docs/transformers/model_doc/bloom>

![图 12](2210.02414v2/activation_outliers_plot2d_combine.png)

图 12：GLM-130B 激活中异常值的分布。纵轴表示隐藏状态维度（4,096 而非 12,288，因为这是一个并行分段），横轴表示输入句子的 token。使用 128×128 的二维直方图以更清楚地观察异常值分布。右图交换了部分纵坐标，从而可以清楚看到异常值出现在约 30% 的维度上。

#### B.6 激活异常值分析

如前文所述，GLM-130B 的权重可以量化到 INT4，以大幅削减推理中的参数冗余。然而，我们也发现 GLM-130B 的激活（即层间隐藏状态）无法被恰当量化，因为它们包含数值异常值，同期文献也指出了这一点（[Dettmers et al., 2022](#bib.bib22)）。

GLM-130B 的特殊之处在于，其 30% 的维度可能出现数值异常值（参见图 12），而其他基于 GPT 的 LLM（如 OPT-175B 与 BLOOM 176B）只有极少数异常维度（[Dettmers et al., 2022](#bib.bib22)）。因此，（[Dettmers et al., 2022](#bib.bib22)）提出的对异常维度做矩阵乘法分解以实现更高精度计算的方案并不适用于 GLM-130B。

![图 13](2210.02414v2/figures/outlier_scale.png)

图 13：GLM-130B 激活异常值的绝对值尺度。

我们研究了这些异常值在 LLM 量化中能否被忽略，答案有趣地是「不能」。这些值可能比普通激活值大数个数量级（参见图 13）。当大多数值（占一个隐藏状态 99.98% 的维度）小于 6 时，那两个异常维度却可以达到 50 甚至超过 100。据推测，它们是 GLM-130B 以及潜在其他 LLM 记忆某些固定世界或语言知识的重要线索，因此在量化中移除或忽略它们会导致显著的性能退化。

#### B.7 权重量化

##### B.7.1 预备知识

**Absmax 量化**是一种对称量化，将 $x$ 的区间 $[-\mathrm{absmax}(x),\mathrm{absmax}(x)]$ 映射到 $[-(2^{b}-1),2^{b}-1]$：

$$
s_{x}=\frac{\mathrm{absmax}(x)}{2^{b-1}-1} \tag{7}
$$

$$
x_{q}=\mathrm{round}(x/s_{x}) \tag{8}
$$

其中 $s_{x}$ 为缩放因子，$x_{q}$ 为量化结果，$b$ 为位宽。

**Zeropoint 量化**是一种非对称量化，将区间 $[\min(x),\max(x)]$ 映射到 $[-(2^{b}-1),2^{b}-1]$：

$$
s_{x}=\frac{\max(x)-\min(x)}{2^{b}-2} \tag{9}
$$

$$
z_{x}=\mathrm{round}(\min(x)/s_{x})+2^{b-1}-1 \tag{10}
$$

$$
x_{q}=\mathrm{round}(x/s_{x})-z_{x} \tag{11}
$$

其中 $z_{x}$ 为零点。

**列/行级量化（Col/Row-wise Quantization）。** 对权重矩阵使用单一缩放因子往往导致更大的量化误差，因为某一个异常值就会导致其他所有元素量化精度的下降。常见的解决办法是按行或按列对权重矩阵分组，每组单独量化并拥有独立的缩放因子。

#### B.8 量化设置

我们的目标是在不损害模型性能的前提下尽可能节省 GPU 显存。实践中，我们只量化占据 transformer 绝大部分参数的线性层，而保持输入/输出嵌入、层归一化与偏置项不变。在 INT4 量化精度下，两个 INT4 权重被压缩为一个 INT8 权重，以节省 GPU 显存占用。我们采用 Absmax 量化，因为我们发现它足以维持模型性能，且比 zeropoint 量化计算效率更高。推理时，GPU 显存中只存储量化权重，线性层的 FP16 权重将在运行时反量化。

##### B.8.1 各规模的量化结果

表 10：GLM 与 BLOOM 家族模型在 100M 至 176B 规模、不同量化精度下于 LAMBADA 数据集上的准确率。

| | BLOOM-560M | BLOOM-1B1 | BLOOM-3B | BLOOM-7B | BLOOM-176B |
| --- | --- | --- | --- | --- | --- |
| Original | 31.40% | 40.68% | 48.30% | 54.91% | 64.37% |
| Absmax INT8, col-wise | 26.12% | 40.69% | 48.83% | 55.33% | 65.03% |
| Absmax INT4, col-wise | 9.30% | 17.43% | 37.88% | 38.04% | 34.83% |
| Absmax INT4, row-wise | 21.37% | 35.80% | 40.95% | 46.75% | NaN |
| Zeropoint INT4, col-wise | 11.51% | 26.51% | 41.65% | 46.63% | 48.26% |
| Zeropoint INT4, row-wise | 24.95% | 33.05% | 43.63% | 49.41% | NaN |

| | GLM-110M | GLM-335M | GLM-2B | GLM-10B | GLM-130B |
| --- | --- | --- | --- | --- | --- |
| Original | 29.36% | 48.51% | 68.19% | 72.35% | 80.21% |
| Absmax INT8, row-wise | 29.25% | 48.69% | 68.12% | 72.37% | 80.21% |
| Absmax INT4, row-wise | 3.26% | 38.25% | 62.62% | 71.03% | 79.47% |
| Zeropoint INT4, row-wise | 5.45% | 42.64% | 64.74% | 70.50% | 80.63% |

110M 至 10B 规模的 GLM 模型来自 GLM 的原始论文（[Du et al., 2022](#bib.bib27)）。尽管较小规模 GLM 的架构与 GLM-130B 不相同，我们相信训练目标才是量化的关键因素。表 10 展示了 GLM 与 BLOOM 家族模型在不同规模、不同量化方法下于 LAMBADA 数据集上的表现。几乎所有模型在 INT8 精度下都保持了性能。总体而言，随着规模扩大，GLM 在 INT4 精度下比 BLOOM 保持了更好的性能。

##### B.8.2 权重分布分析

为实现 INT4 权重量化，我们在直方图中分析了 GLM-130B 与对照模型 BLOOM-176B 主要线性层的权重值分布（参见图 15）。横轴表示权重值，纵轴以对数尺度表示该值权重的数量。可以看到，BLOOM-176B 中主要是 w2 线性层呈现偏斜分布，这会阻碍对称量化。相反，GLM-130B 的 w2 分布良好、没有太多异常值与偏斜分布，从而为其几乎不损失性能的 INT4 量化铺平了道路。

#### B.9 贡献归因消融

图 14：GLM 目标与 MIP 训练的贡献归因分析。我们在消融中以 GLM-10B（仅英文）为例。总体而言，GLM 目标的双向注意力贡献了 70% 的提升，而 MIP 的主要贡献在于文本相似度任务。

我们分析了 GLM-130B 中所用技术的贡献归因。论文中已呈现一系列消融研究，为便于阅读，它们原本散落在全文各处。这里我们将它们汇总为以下列表，供读者参考：

- 普通 PostLN 与 DeepNorm 的消融：图 3。
- 双向/单向注意力的消融：图 2（LAMBADA）、表 16（条件 NLG）、图 17（SuperGLUE）。
- 嵌入层梯度收缩（EGS）的消融：图 4。
- 位置编码与 FFN 的消融：附录 B.3、表 8。

此外，我们进行了以下研究，以论证 GLM-130B 中两项最有影响力的技术——GLM 目标与多任务指令预训练（MIP）——的贡献。

GLM 目标与 MIP。从头消融一个 100B 规模的 LLM 代价过于高昂。作为替代，我们尽力在 GLM-10B（（[Du et al., 2022](#bib.bib27)）发布的仅英文版本，未经 MIP）上进行 GLM 目标与 MIP 的对比。我们额外从中间阶段的原始检查点初始化，训练了一个带 MIP（5%）的 GLM-10B，以匹配原始纯自监督 GLM-130B 的训练 token 数。这一次的 MIP 完全遵循 T0（[Sanh et al., 2022](#bib.bib93)）的数据集设置以及 GLM-130B 中的信息抽取数据集，以便在某些类型的任务（如 NLI）上进行正确评测。

图 14 展示了消融结果。在我们测试的 8 个数据集上，我们发现 GLM 目标是性能提升的主要贡献者（从 GLM（uni）到 GLM + MIP（bi））。例如，它贡献了 LAMBADA 上 73% 的提升与 MMLU 上 90% 的提升——这两者都是 LLM 领域被广泛采用的挑战性基准。至于 MIP，在一些数据集（如 WiC、ReCoRD、Hellaswag）上，MIP 甚至可能损害性能；而对于与文本相似度及共指消解相关的数据集（如 WSC、BoolQ、ANLI R1），MIP 是主要贡献者。这可能是因为，文本相似度与共指这类人们通常为测试语言模型能力而有意构造的挑战，在构成人们日常书面文本的自监督语料中很少见到。因此，MIP 训练主要帮助弥合自监督预训练与这些任务之间的差距。

#### B.10 经验教训

> **双向架构**：除 GPT 之外，双向注意力的 GLM 是一种强大的架构替代选择。

> **面向平台的配置**：根据所用集群与并行策略配置 LLM，以榨取硬件潜力。

> **改进的 Post-LN**：与直觉相反，作为 Post-LN 的一种，DeepNorm 才是稳定 GLM-130B 的选项。

> **训练不稳定性的分类**：LLM 遭受的意外训练不稳定会系统性地与数值性地出现。

> **系统性不稳定：FP16**：尽管 FP16 带来更多不稳定，它使训练与推理可以在多样平台上进行。

> **数值不稳定：嵌入梯度收缩**：将嵌入层梯度收缩至其 0.1 倍即可解决大多数数值不稳定问题。

> **GLM 的 INT4 量化缩放定律**：GLM 拥有一种在 GPT 风格 BLOOM 中未被观察到的独特 INT4 权重量化缩放定律。

> **未来方向**：要创造强大的 LLM，主要关注点可以是：1）更多且更好的数据；2）更好的架构与预训练目标；3）更充分的训练。

![图 15](2210.02414v2/figures/quantization-appendix.png)

图 15：GLM-130B（橙色：attn-dense、attn-qkv、glu-w1、glu-w2）与 BLOOM-176B（蓝色：attn-dense、attn-qkv、ffn-w1、ffn-w2）前 28 个 transformer 层线性层的权重值分布。总体而言，对 GLM-130B 来说，attn-dense 与 w2 可能呈现较窄的值分布；attn-qkv 与 w1 也可能是使 GLM-130B 中间层能够进行 INT4 量化的原因。

表 11：GLM-130B 训练的完整配置

| 配置键 | 取值 |
| --- | --- |
| adam_beta1 | 0.9 |
| adam_beta2 | 0.95 |
| adam_eps | 1e-08 |
| aggregated_samples_per_sequence | 4 |
| attention_dropout | 0.1 |
| attention_softmax_in_fp32 | True |
| average_block_length | 3 |
| bias_dropout_fusion | True |
| checkpoint_activations | True |
| checkpoint_in_cpu | False |
| checkpoint_num_layers | 1 |
| clip_grad | 1.0 |
| contigious_checkpointing | False |
| cpu_optimizer | False |
| data_parallel_size | 24 |
| deepnorm | True |
| distributed_backend | nccl |
| eval_interval | 1000 |
| eval_iters | 3 |
| ffn_hidden_size | 32768 |
| fp16 | True |
| global_batch_size | 4224 |
| glu_activation | geglu |
| gpt_prob | 0.7 |
| hidden_dropout | 0.1 |
| hidden_size | 12288 |
| hysteresis | 2 |
| init_method_std | 0.0052 |
| init_method_xavier_uniform | False |
| initial_loss_scale | 65536 |
| layernorm_epsilon | 1E-05 |
| learnable_rotary_embedding | False |
| length_per_sample | 2000 |
| log_interval | 1 |
| loss_scale | 0 |
| loss_scale_window | 2000 |
| lr | 8e-05 |
| lr_decay_iters | None |
| lr_decay_samples | 197753905 |
| lr_decay_style | cosine |
| lr_warmup_samples | 1098632 |
| make_vocab_size_divisible_by | 768 |
| mask_prob | 0.15 |
| masked_softmax_fusion | True |
| micro_batch_size | 1 |
| min_gmask_ratio | 0.2 |
| min_loss_scale | 1.0 |
| min_lr | 8e-06 |
| multitask_ratio | 0.05 |
| num_attention_heads | 96 |
| num_layers | 70 |
| onnx_safe | None |
| optimizer | adam |
| partition_activations | True |
| pipeline_model_parallel_size | 8 |
| position_embedding_type | rotary |
| rampup_batch_size | 192, 24, 5493164 |
| save_interval | 250 |
| seed | 1234 |
| seq_length | 2048 |
| short_seq_prob | 0.02 |
| shrink_embedding_gradient_alpha | 0.1 |
| single_span_prob | 0.02 |
| split | 949,50,1 |
| tensor_model_parallel_size | 4 |
| tokenizer_type | IceTokenizer |
| weight_decay | 0.1 |
| zero_contigious_gradients | False |
| zero_reduce_bucket_size | 500000000 |
| zero_reduce_scatter | False |
| zero_stage | 1 |
| zero-optimization.allgather_bucket_size | 500000000 |
| tokenizer_type | IceTokenizer |
| weight_decay | 0.1 |
| world_size | 768 |
| zero_contigious_gradients | FALSE |
| zero_reduce_bucket_size | 500000000 |
| zero_reduce_scatter | FALSE |
| zero_stage | 1 |
| zero-optimization.allgather_bucket_size | 500000000 |

表 12：多任务指令预训练（MIP）所涉及的 74 个数据集。来自 T0-PromptSource（[Sanh et al., 2022](#bib.bib93)；[Bach et al., 2022](#bib.bib5)）的数据集以其 Hugging Face 数据集标识符命名；来自 DeepStruct（[Wang et al., 2022a](#bib.bib115)）的数据集在附录 C.2 中描述。

| 任务 | 数据集 | 任务 | 数据集 |
| --- | --- | --- | --- |
| 指代消解 | super_glue/wsc.fixed | 多选问答 | cos_e/v1.11 |
| 指代消解 | winogrande/winogrande_xl | 多选问答 | cosmos_qa |
| 自然语言推理 | super_glue/cb | 多选问答 | dream |
| 自然语言推理 | super_glue/rte | 多选问答 | openbookqa/main |
| 自然语言推理 | anli | 多选问答 | qasc |
| 复述识别 | glue/mrpc | 多选问答 | quail |
| 复述识别 | glue/qqp | 多选问答 | quarel |
| 复述识别 | paws/labeled_final | 多选问答 | quartz |
| 闭卷问答 | ai2_arc/ARC_Challenge | 多选问答 | race/high |
| 闭卷问答 | ai2_arc/ARC_Easy | 多选问答 | race/middle |
| 闭卷问答 | kilt_tasks/hoptpotqa | 多选问答 | sciq |
| 闭卷问答 | trivia_qa/unfiltered | 多选问答 | social_i_qa |
| 闭卷问答 | web_questions | 多选问答 | super_glue/boolq |
| 闭卷问答 | wiki_qa | 多选问答 | super_glue/multirc |
| 抽取式问答 | adversarial_qa/dbidaf | 多选问答 | wiki_hop/original |
| 抽取式问答 | adversarial_qa/dbert | 多选问答 | wiqa |
| 抽取式问答 | adversarial_qa/droberta | 多选问答 | piqa |
| 抽取式问答 | duorc/SelfRC | 主题分类 | ag_news |
| 抽取式问答 | duorc/ParaphraseRC | 主题分类 | dbpedia_14 |
| 抽取式问答 | ropes | 主题分类 | trec |
| 抽取式问答 | squad_v2 | 词义消歧 | super_glue/wic |
| 抽取式问答 | super_glue/record | 对话状态追踪 | multiwoz_2.1 |
| 抽取式问答 | quoref | 事件抽取 | ace05 |
| 情感 | amazon_polarity | 命名实体识别 | conll03 |
| 情感 | app_reviews | 命名实体识别 | genia |
| 情感 | imdb | 命名实体识别 | ontonotes5.0 |
| 情感 | rotten_tomatoes | 命名实体识别 | ace2005 |
| 情感 | yelp_review_full | 命名实体识别 | conll04 |
| 句子补全 | super_glue/copa | 命名实体识别 | nyt29 |
| 句子补全 | hellaswag | 关系抽取 | conll04 |
| 结构到文本 | common_gen | 关系抽取 | nyt29 |
| 结构到文本 | wiki_bio | 关系抽取 | ace2005 |
| 摘要 | cnn_dailymail/3.0.0 | 关系抽取 | kelm |
| 摘要 | gigaword | 关系分类 | tacred |
| 摘要 | multi_news | 语义角色标注 | conll05 |
| 摘要 | samsum | 语义角色标注 | conll12 |
| 摘要 | xsum | 语义角色标注 | propbank |

### 附录 C 数据集与评测细节

#### C.1 多任务指令预训练（MIP）

遵循既有实践（[Raffel et al., 2020](#bib.bib82)；[Wei et al., 2022a](#bib.bib120)；[Sanh et al., 2022](#bib.bib93)；[Aribandi et al., 2022](#bib.bib2)），我们在 GLM-130B 的 MIP 训练中纳入了若干指令提示数据集，占训练 token 的 5%。T0 数据集的全部提示来自 PromptSource（[Bach et al., 2022](#bib.bib5)），DeepStruct 数据集的提示则为新创建。其构成见表 12，由来自 T0（[Sanh et al., 2022](#bib.bib93)）与 promptsource（[Bach et al., 2022](#bib.bib5)）的自然语言理解与生成数据集，以及来自 DeepStruct（[Wang et al., 2022a](#bib.bib115)）的信息抽取数据集组成。在 GLM-130B 的训练中，我们估算每个数据集约 36% 的样本已被模型见过。

T0 最初将数据集划分为两部分：1）多任务提示训练与 2）零样本任务迁移。我们最初计划只纳入 T0 多任务提示训练部分的训练集与 DeepStruct（[Wang et al., 2022a](#bib.bib115)），但由于一次失误，我们将多任务提示训练与零样本任务迁移两个部分的数据集都纳入了 MIP，并排除了 DeepStruct 数据集。该失误在约 23k 步时得到修复，模型随后继续在正确版本上训练。

自然语言理解与生成。我们采用来自 promptsource（[Bach et al., 2022](#bib.bib5)）的数据集与对应提示。对每个数据集的全部提示样本，我们设置每数据集最多 100,000 个样本的截断，并将它们合并为 MIP 数据集。提示样本与数据集的细节见 promptsource 的 GitHub 仓库⁸。

⁸ <https://github.com/bigscience-workshop/promptsource>

信息抽取。基于 DeepStruct（[Wang et al., 2022a](#bib.bib115)）——一种面向信息抽取任务的多任务语言模型预训练方法——的数据集，我们为其部分数据集创建了指令与提示（见表 12）。我们将信息抽取任务重构为指令微调格式，以实现对新的抽取 schema 的零样本泛化。对每个数据集的全部提示样本，由于信息抽取数据集数量少于常见的语言理解与生成数据集，我们设置每数据集最多 200,000 个样本的截断。对于 KELM（[Agarwal et al., 2021](#bib.bib1)）与 PropBank（[Kingsbury & Palmer,](#bib.bib48)）数据集，由于其原始规模巨大，我们从其提示样本中各抽样 500,000 个样本。

#### C.2 MIP 中 DeepStruct 的数据与提示

DeepStruct（[Wang et al., 2022a](#bib.bib115)）中所有数据集的提示与指令均由作者手动新创。每个数据集的介绍、任务描述与完整提示附于以下小节。为支持模板填充，所有提示均以 Jinja⁹ 模板写成。当以我们的格式提供数据集样本时，Jinja 引擎会将其渲染为带指令的提示样本。

⁹ <https://github.com/pallets/jinja>

对 GLM-130B 信息抽取能力的更系统性评测留作未来工作，因为本工作的重心在于 LLM 的训练与设计细节。

##### C.2.1 对话状态追踪

我们采用 Multiwoz 2.1（[Eric et al., 2020](#bib.bib30)）对话状态追踪数据集。该数据集被重构为两个任务，各对应一个提示：

- 对话状态追踪：要求模型在给定一组特定槽位（如 taxi_arrival_time 与 destination）列表的情况下，从对话中抽取信息。
- 槽位填充：模型应填充一个给定槽位，并识别无答案的情形。

（对话状态追踪，Prompt 0）

```text
Read the dialogues between "[User]" and "[Agent]",

{{text}}

identify and extract the information related to the following categories (from top to down):

- {{allowed_relations | join("\n- ")}}

in the form of "( [User] ; Y ; Z )": ||| {{format_triple(relations, allowed_relations) | join(" ")}}
```

（槽位填充，Prompt 0）

```text
Given the following dialogue:

{{text}}

please answer the question: has "[User]" mentioned "{{allowed_relations[relation_idx].split(’: ’) | join("’s ")}}" ? If yes, please write down the answer from the dialogue; if not, please answer "not given".

Answer: ||| {% if filter_relation(relations, allowed_relations[relation_idx]).__len__() > 0 %}{{filter_relation(relations, allowed_relations[relation_idx])[0][’tail’]}}{% else %}not given{% endif %}
```

##### C.2.2 事件抽取

我们采用 ACE05（[Walker & Consortium, 2005](#bib.bib112)）事件抽取数据集，遵循（[Wadden et al., 2019](#bib.bib111)）中的设置。该数据集被重构为两个任务、共三个提示，如下所述：

- 事件论元抽取：给定文本中的一个触发词及其论元角色列表，要求模型从给定文本中抽取论元。
- 论元识别：给定一个触发词与某个论元角色，要求模型在论元存在于给定文本时将其抽取出来；否则，模型不应生成任何内容。

（事件论元抽取，Prompt 0）

```text
For the task of "Event Extraction", given a trigger one should extract its related arguments conditioned on a list of potential roles.

Given the following list of roles:

- {{shuffle(allowed_arguments[trigger[’event_type’]].values()) | join("\n- ")}}

extract related arguments of the trigger "{{trigger[’text’]}} ({{allowed_triggers[trigger[’event_type’]]}})" in the following sentence:

{{text}}

Extractions: ||| {{format_triple(relations, "") | join(" ")}}
```

（事件论元抽取，Prompt 1）

```text
TEST

1. (Event Extraction) {{text}}

Please write down ALL event arguments related to the trigger "{{trigger[’text’]}} ({{allowed_triggers[trigger[’event_type’]]}})" marked with "[ ]", given the following categories:

- {{shuffle(allowed_arguments[trigger[’event_type’]].values()) | join("\n- ")}}

Answer: ||| {{format_triple(relations, "") | join(" ")}}
```

（论元识别，Prompt 0）

```text
Let extract event related arguments!

In the following passage, an argument with the type "{{query_arg}}" is related to the event trigger "{{trigger[’text’]}} ({{allowed_triggers[trigger[’event_type’]]}})":

{{text}}

The argument should be (copy from the context if you find it; if not, do not generate): ||| {{filter_type(relations, query_arg) | join(" ")}}
```

##### C.2.3 联合实体与关系抽取

联合实体与关系抽取旨在从一段文本中识别命名实体并判断它们之间的关系。它与知识获取密切相关，其最终目标是将非结构化的网络内容结构化为知识三元组（如 (London, capital_of, Britain)）。该任务既可以形式化为流水线框架（命名实体识别与关系抽取的组合），也可以端到端训练。

本工作中，我们采用三个经典的联合实体与关系抽取数据集：CoNLL04（[Roth & Yih, 2004](#bib.bib87)）、NYT（[Riedel et al., 2010](#bib.bib85)）与 ACE2005（[Walker & Consortium, 2005](#bib.bib112)）。在 GLM-130B 中，我们遵循（[Wang et al., 2022a](#bib.bib115)）将这类挑战形式化为序列到序列生成：输入为原始文本，输出为三元组。这里我们只对这些数据集进行关系相关任务，实体相关任务留待命名实体识别小节。

- 关系抽取：在给定关系候选列表的情况下，抽取由「头实体」「关系」「尾实体」组成的知识三元组。例如，给定输入「In Kunming the 800-some faculty and student established the National Southwestern Associated University.」，模型输出可以是 (National Southwestern Associated University, location of formation, Kunming)。
- 条件关系抽取：给定单个关系候选，判断输入文本是否包含该关系。若是，抽取所有相关三元组；若否，不生成。
- 知识槽位填充：指定文本中的某个实体，要求模型抽取所有以该实体为头的三元组。
- 关系分类：给定文本中的两个实体，要求模型基于候选关系列表判断它们之间的关系。

（关系抽取，Prompt 0）

```text
Can you figure out all triples regarding the relations of "{{shuffle(allowed_relations) | join(’", "’)}}" from the sentence? List them in the shape of "( X ; Y ; Z )":

{{text}} => ||| {{format_triple(relations, allowed_relations) | join(" ")}}
```

（条件关系抽取，Prompt 0）

```text
Conditioned on the relation "{{allowed_relations[relation_idx]}}", what knowledge triples can be extracted from:

{{text}}

Please write them down here: ||| {{format_triple(relations, [allowed_relations[relation_idx]]) | join(" ")}}
```

（知识槽位填充，Prompt 0）

```text
{% if entity_types.__len__() > 0 %}
In the sentence

{{text}}

the X = "{{entities[entity_idx]}}" is an entity of the type "{{entity_types[entity_idx]}}". Extract all possible triples contains "{{entities[entity_idx]}}" in the form of ( X ; Y ; Z ), given the following candidate properties Y:

{% for r in allowed_relations %}- {{r}}
{% endfor %}
Answer: ||| {% for r in relations %}{% if r[’head’][0] == entities[entity_idx] %}{{format_triple([r], allowed_relations) | join(" ")}}{% endif %}{% endfor %}
{% endif %}
```

（关系分类，Prompt 0）

```text
QUIZ

1. Given the candidate relations:

- {{shuffle(allowed_relations) | join("\n- ")}}

what is the relation between "{{relations[triple_idx][’head’][0]}}" and "{{relations[triple_idx][’tail’][0]}}" in the following sentence?

{{text}}

Answer: ||| {{relations[triple_idx][’relation’]}}
```

然而，既有的联合实体与关系抽取数据集的关系 schema 非常有限。例如，CoNLL04 只包含五种不同关系；最多样化的 NYT 数据集包含 24 个 Freebase 谓词。为使模型能够捕捉多样化的潜在言语化谓词，我们用来自 KELM（[Agarwal et al., 2021](#bib.bib1)）的自动生成的知识-文本对齐数据扩展了该任务。我们没有纳入其他远程监督数据集（如 T-Rex（[Elsahar et al., 2018](#bib.bib29)）），因为它们可能极其嘈杂。

对于 KELM 数据，由于它基于完整的 Wikidata schema（包含的关系多到无法枚举），我们为关系抽取与知识槽位填充任务创建了两个 KELM 专属提示：

（关系抽取，Prompt 1，仅 KELM）

```text
{# kelm #}
Can you figure out all knowledge triples regarding whole Wikidata properties from the sentence? List them in the shape of "( X ; Y ; Z )":

{{text}} => ||| {{format_triple(relations, "") | join(" ")}}
```

（知识槽位填充，Prompt 1，仅 KELM）

```text
{# kelm #}
Given the entity "{{entities[entity_idx]}}" marked with "[" and "]" in the context:

{{text}}

please list all triples related to it (do not generate if there is no answer): ||| {% for r in relations %}{% if r[’head’][0] == entities[entity_idx] %}{{format_triple([r], "") | join(" ")}}{% endif %}{% endfor %}
```

##### C.2.4 命名实体识别

命名实体识别是一项以从原始文本语料中识别命名实体并为其赋予恰当实体类型为目标的任务。例如，在句子「In 1916 GM was reincorporated in Detroit as "General Motors Corporation".」中，General Motors Corporation 的实体类型可以是组织机构。我们基于命名实体识别数据集 CoNLL03（[Sang & Meulder, 2003](#bib.bib91)）、OntoNotes 5.0（[Pradhan et al., 2013](#bib.bib75)）与 GENIA（[Ohta et al., 2002](#bib.bib72)）设计了两种不同类型的任务。我们还纳入了联合实体与关系数据集中的命名实体识别子任务。

- 命名实体识别：给定一组可能的实体类型（如 location、person、organization），从给定文本内容中抽取所有相关实体。
- 实体分型：实体分型是命名实体识别的重要衍生任务之一。它旨在（在未知实体类型的情况下）判断某个实体提及的正确类型，常作为后处理附加在实体提及抽取之后。

（命名实体识别，Prompt 0）

```text
Given the following list of entity types:

Z = {{shuffle(allowed_types) | join(", ")}}

please extract all mentioned entities from left to right in the sentence, in the form of "( X ; instance of ; Z )".

{{text}} => ||| {% for entity, type in zip(entities, entity_types) %}( {{entity}} ; instance of ; {{type}} ) {% endfor %}
```

（实体分型，Prompt 0）

```text
Extract all entity mentioned in the sentence with entity type "{{allowed_types[type_idx]}}" in the form of "( X ; instance of ; {{allowed_types[type_idx]}} )"

{{text}} => ||| {% for entity, type in zip(entities, entity_types) %}{% if type == allowed_types[type_idx] %}( {{entity}} ; instance of ; {{type}} ) {% endif %}{% endfor %}
```

（实体分型，Prompt 1）

```text
List all "{{allowed_types[type_idx]}}" entities appeared in the following passage, joined by " | ":

{{text}} => ||| {{filter_type(zip(entities, entity_types), allowed_types[type_idx]) | join(" | ")}}
```

（实体分型，Prompt 2）

```text
{% if entity_types.__len__() > 0 %}
Based on the list of potential entity types and ignore their order:

- {{shuffle(allowed_types) | join("\n- ")}}

the entity "{{entities[entity_idx]}}" marked with "[" and "]" in the following sentence:

{{text}}

belongs to ||| {{entity_types[entity_idx]}}
{% endif %}
```

##### C.2.5 关系分类

关系分类是信息抽取中的一项基础任务，从候选列表中识别两个给定实体之间的关系。这是一个长期存在的问题，因为它深受数据标注高昂成本之苦：知识密集型任务的人工标注需要受过教育且收费高昂的标注者。关系抽取中事实上的数据创建方法依赖远程监督，即将知识库中既有的知识三元组自动对齐到文本内容，并假设这种对齐在某些条件下是正确的。这里我们只纳入 TacRED（[Zhang et al., 2017](#bib.bib134)）数据集，并基于它创建若干不同任务。

- 关系分类：最传统的任务形式。给定文本中的两个实体，从候选列表中分类它们的关系。形式既可以直接回答关系，也可以以三元组形式（类似关系抽取）。
- 知识槽位填充：将任务改为给定头实体与关系，判断尾实体是否存在于输入文本中。若不存在，不生成任何内容。
- 是非问题：将该问题转化为类似自然语言推理的任务。例如，给定句子「The series focuses on the life of Carnie Wilson, daughter of Brian Wilson, founder of the Beach Boys.」，模型将被要求通过回答「yes」或「no」来判断一个三元组（如 Carnie Wilson, father, Brian Wilson）的正确性。

（关系分类，Prompt 0）

```text
{% if entity_types.__len__() > 0 %}
Given the following categories of relations:

- {{shuffle(allowed_relations.values()) | join("\n- ")}}

predict the relation between "{{relations[0][’head’]}}" and "{{relations[0][’tail’]}}" in the following sentence:

{{text}}

The relation should be : ||| {{allowed_relations[relations[0][’relation’]]}}
{% endif %}
```

（关系分类，Prompt 1）

```text
1. (Relation Extraction) Answer the relation between entities in the form of "( X ; Y ; Z )":

{{text}}

The relation between "{{relations[0][’head’]}}" and "{{relations[0][’tail’]}}" is: ||| ( {{relations[0][’head’]}} ; {{allowed_relations[relations[0][’relation’]]}} ; {{relations[0][’tail’]}} )
```

（知识槽位填充，Prompt 0）

```text
Based on the sentence provided below, infer the missing argument asked by the question:

{{text}}

Question: What/Who/Where is "{{relations[0][’head’]}}" {{allowed_relations[relations[0][’relation’]]}} ?

Answer: ||| {{relations[0][’tail’]}}
```

##### C.2.6 语义角色标注

语义角色标注是一项历史久远的信息任务，旨在识别句子中与给定谓词相关的语义论元。例如，在句子「Grant was employed at IBM for 21 years where she held several executive positions.」及其中的谓词「employed」上，语义角色标注将 Grant 识别为主语、IBM 识别为第二个宾语。

我们基于语义角色标注数据集 CoNLL05（[Carreras & Màrquez, 2005](#bib.bib14)）、CoNLL12（[Pradhan et al., 2013](#bib.bib75)）与 PropBank（[Kingsbury & Palmer,](#bib.bib48)）创建了两种不同的任务。

- 语义角色标注：传统任务形式，在文本中标注一个动词（即谓词），要求模型生成相关的语义角色。
- 语义角色填充：给定一个动词与一个潜在语义角色，要求模型判断该角色是否存在于句子中并将其生成出来。
- 谓词识别：给定句子片段及其对应的语义角色，识别它与哪个动词相关。

（语义角色标注，Prompt 0）

```text
Provided with the target verb "{{verb}}" marked with "[" and "]" in the following sentence, find out its "{{allowed_types[type_idx]}}":

{{text}} => ||| {% for entity, type in zip(entities, entity_types) %}{% if type == allowed_types[type_idx] %}{{entity}}{% endif %}{% endfor %}
```

（语义角色填充，Prompt 0）

```text
Given the following list of argument types:

Z = {{allowed_types | join(", ")}}

find out all arguments related to verb "{{verb}}" mentioned in the following sentence from left to right, in the form of "( X ; instance of ; Z )".

{{text}} => ||| {% for entity, type in zip(entities, entity_types) %}( {{entity}} ; argument type ; {{type}} ) {% endfor %}
```

（谓词识别，Prompt 0）

```text
FINAL EXAM

1. Based on the fact that "{{entities[entity_idx]}}" is a "{{entity_types[entity_idx]}}", which verb in the following sentence should it related to?

{{text}}

Answer: ||| {{verb}}
```

#### C.3 GPT-3、BLOOM-176B 与 OPT-175B 的结果来源

这里说明 GPT-3、BLOOM-176B 与 OPT-175B 的结果来源。我们可能比较的其他 LLM 大多完全闭源，因此其结果均取自既有预印本、出版物，或 BIG-bench 仓库¹⁰中存储的结果。

¹⁰ <https://github.com/google/BIG-bench>

对于 GPT-3，本文中其结果如无特别说明大多取自既有文献，其余通过我们自己请求 OpenAI Davinci API 获得的结果均已明确注明。对于 BLOOM-176B 与 OPT-175B，如无特别标注，其结果：

- 取自 OPT 论文（[Zhang et al., 2022](#bib.bib133)）。
- 取自 EAI-Eval BigScience Arch&Scale Google 表格¹¹。
- 取自 Huggingface Datasets 中 BigScience 评测结果仓库¹²。

¹¹ <https://docs.google.com/spreadsheets/d/1CI8Q9RCblLRzUOPJ6ViqBmo284-8ojluQ-CmaEuhuv0>
¹² <https://huggingface.co/datasets/bigscience/evaluation-results/tree/main/bloom/bloomzeval/transformers/evaluation_val>

特别地，我们无法自行评测 OPT-175B，因为尽管过去数月中我们提交了多次申请，至今仍未被正式授予该检查点。

#### C.4 Pile 测试集评测

表 13：GLM-130B 与相近规模 LLM 在 Pile 测试集上的 BPB 结果。

| | Jurassic-1 | GPT-3 | GLM-130B |
| --- | --- | --- | --- |
| dm_mathematics | 1.040 | 1.370 | 0.786 |
| ubuntu_irc | 0.857 | 0.946 | 0.977 |
| opensubtitles | 0.879 | 0.932 | 0.889 |
| hackernews | 0.869 | 0.975 | 0.873 |
| books33 | 0.835 | 0.802 | 0.803 |
| pile_cc | 0.669 | 0.698 | 0.771 |
| philpapers | 0.741 | 0.723 | 0.766 |
| gutenberg_pg_19 | 0.890 | 1.160 | 0.821 |
| arxiv | 0.680 | 0.838 | 0.570 |
| stackexchange | 0.655 | 0.773 | 0.611 |
| nih_exporter | 0.590 | 0.612 | 0.614 |
| pubmed_abstracts | 0.587 | 0.625 | 0.610 |
| uspto_backgrounds | 0.537 | 0.566 | 0.537 |
| pubmed_central | 0.579 | 0.690 | 0.510 |
| freelaw | 0.514 | 0.612 | 0.499 |
| github | 0.358 | 0.645 | 0.329 |
| enron_emails | 0.621 | 0.958 | 0.604 |
| youtube_subtitles | 0.825 | 0.815 | 0.746 |
| 加权平均 | 0.650 | 0.742 | 0.634 |

Pile 评测（[Gao et al., 2020](#bib.bib32)）是一个综合语言建模基准，最初包含来自不同领域的 22 个文本数据集。我们在有既定基线结果（[Lieber et al., 2021](#bib.bib56)）的 18 个数据集上报告结果。与传统语言建模基准不同，Pile 评测报告 BPB（bits-per-byte）困惑度，以避免不同词表模型之间的不公平比较——因为一般来说，若不加限制，词表更大的语言模型在困惑度比较中更占优势。评测中我们严格遵循（[Gao et al., 2020](#bib.bib32)）的设置：使用 [gMASK] 与双向注意力的 1,024 上下文长度，其余 1024 个 token 以自回归方式计算 BPB。加权平均 BPB 基于各共享数据集在 Pile 训练集中的比例（[Gao et al., 2020](#bib.bib32)）计算。

Pile 测试集上的详细指标见表 13。我们观察到，与 GPT-3 相比，GLM-130B 在 phil_papers 与 pile_cc 上表现明显较弱，这可能源于 GLM-130B 的双语特性，以及缺乏更多样、更高质量的私有收集语料。

#### C.5 BIG-bench-lite 评测

图 16：BIG-bench-lite（24 个任务）评测全景。

近期工作（[Wei et al., 2022c](#bib.bib122)；[Wang et al., 2022c](#bib.bib119)）揭示 LLM 能够进行超出常规语言任务的推理。作为回应，BIG-bench（[Srivastava et al., 2022](#bib.bib102)）近期通过向全球研究者众包新型任务而建立，用于测试 LLM 未被探索的能力。出于经济性考虑，我们在原始 150 任务 BIG-bench 的官方子集——包含 24 个任务的 BIG-bench-lite——上评测 GLM-130B。这些任务可分为两类：一类是基于带选项的多选问答；另一类是不带选项的直接生成。对于第一类，我们评估每个选项完整内容的概率并选择最大者作为答案；对于第二类，我们使用贪心解码生成答案。BIG-bench 中的所有评测均基于 [MASK]，因为这里的答案通常是较短的文本片段。三个 LLM 在 24 个 BIG-bench-lite（[Srivastava et al., 2022](#bib.bib102)）数据集上的全部结果见表 14 与图 16。我们直接采用 BIG-bench 的原始提示，并使用官方实现生成少样本评测的示范样本以及计算最终分数。

表 14：GLM-130B、GPT-3 175B（[Brown et al., 2020](#bib.bib12)）与 PaLM 540B（[Chowdhery et al., 2022](#bib.bib18)）在 BIG-bench-lite 上 0、1、3-shot 的详细结果。每个任务报告「normalized preferred metric」。GPT-3 与 PaLM 的结果报告于 BIG-bench 的 GitHub 仓库，且 PaLM 540B 的 3-shot 结果未能找到。

| | GLM-130B | | | GPT-3 175B | | | PaLM 540B | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | 0 | 1 | 3 | 0 | 1 | 3 | 0 | 1 |
| auto_debugging | 11.76 | 20.59 | 23.53 | 0.00 | 0.00 | 0.00 | 0.00 | 38.23 |
| bbq_lite_json | 22.26 | 37.50 | 59.73 | -8.33 | 40.75 | 61.21 | -4.39 | 77.73 |
| code_line_description | 0.22 | 9.09 | -8.64 | 9.09 | 9.09 | 9.09 | 0.22 | 49.00 |
| conceptual_combinations | 37.51 | 31.33 | 27.86 | 2.37 | 3.70 | 14.33 | 45.68 | 73.36 |
| conlang_translation | 34.72 | 38.01 | 33.88 | 46.82 | 47.07 | 51.60 | 36.88 | 61.92 |
| emoji_movie | 1.25 | 4.88 | 3.75 | -10.00 | -2.49 | -1.24 | 17.50 | 88.75 |
| formal_fallacies_syllogisms_negation | 0.83 | 1.46 | 0.35 | 1.00 | 6.80 | 5.60 | -0.20 | 4.40 |
| hindu_knowledge | 32.23 | 37.56 | 34.52 | 10.15 | 40.61 | 44.42 | 41.37 | 93.15 |
| known_unknowns | -4.35 | 0.00 | 4.35 | 21.74 | 4.35 | 0.00 | 13.04 | 34.78 |
| language_identification | 9.62 | 1.97 | 1.90 | 7.49 | 3.20 | 1.98 | 12.11 | 31.03 |
| linguistics_puzzles | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.10 |
| logic_grid_puzzle | 9.88 | 13.66 | 5.24 | 0.16 | 3.35 | 0.01 | 1.47 | 16.12 |
| logical_deduction | 24.18 | 22.20 | 20.35 | 2.22 | 10.80 | 14.71 | 2.17 | 15.34 |
| misconceptions_russian | -26.53 | -46.94 | -26.53 | -34.70 | -34.70 | -30.61 | -42.86 | -30.61 |
| novel_concepts | 6.25 | 21.87 | 25.78 | 33.59 | 33.59 | 45.31 | 33.59 | 49.22 |
| operators | 14.76 | 18.10 | 18.10 | 30.0 | 34.29 | 33.33 | 30.48 | 56.19 |
| parsinlu_reading_comprehension | 7.14 | 7.72 | 11.58 | 0.00 | 0.00 | 0.00 | 9.46 | 44.40 |
| play_dialog_same_or_different | 2.88 | 5.33 | 3.80 | 8.00 | 0.80 | -5.40 | -33.0 | 0.10 |
| repeat_copy_logic | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 37.5 |
| strange_stories | 43.86 | 51.76 | 42.31 | 8.27 | 25.68 | 12.93 | 39.25 | 74.46 |
| strategyqa | 21.10 | 18.74 | 16.82 | 4.60 | 13.20 | 14.20 | 28.00 | 38.00 |
| symbol_interpretation | 1.39 | 1.89 | 1.77 | 0.51 | -0.63 | 2.77 | 0.76 | 2.40 |
| vitaminc_fact_verification | 71.87 | 60.72 | 56.55 | -31.55 | 22.15 | 29.05 | -28.85 | 55.60 |
| winowhy | -3.49 | 5.38 | 3.0 | 3.0 | 10.60 | 13.00 | -5.0 | 31.80 |

#### C.6 MMLU 评测

GLM-130B 与 BLOOM 176B 在 57 个 MMLU（[Hendrycks et al., 2021](#bib.bib40)）数据集上的全部结果见表 15。在第 5.2 节，我们报告了 GLM-130B、GPT-3 175B 与 BLOOM 176B 的加权平均准确率（即按样本平均的准确率，而非按学科平均）。

表 15：GLM-130B 与 BLOOM 176B（[Scao et al., 2022](#bib.bib94)）在 MMLU（[Hendrycks et al., 2021](#bib.bib40)）上的详细结果。我们发现没有既有文献报告过 GPT-3 175B 的数值准确率。BLOOM 使用 Huggingface Transformer 实现评测。

| | 学科 | GLM-130B | BLOOM 176B |
| --- | --- | --- | --- |
| STEM | abstract_algebra | 24.00 | 24.00 |
| | anatomy | 48.90 | 38.52 |
| | astronomy | 48.03 | 34.87 |
| | colledge_biology | 47.22 | 37.50 |
| | college_chemistry | 34.00 | 19.00 |
| | colledge_computer_science | 44.00 | 1.00 |
| | colledge_mathematcis | 27.00 | 31.00 |
| | colledge_physics | 30.39 | 24.50 |
| | computer_security | 61.00 | 40.00 |
| | conceptual_physics | 38.72 | 31.49 |
| | electrical_engineering | 45.52 | 32.41 |
| | elementary_mathematics | 31.75 | 29.63 |
| | high_school_biology | 51.29 | 27.42 |
| | high_school_chemistry | 34.98 | 27.09 |
| | high_school_computer_science | 53.00 | 30.00 |
| | high_school_mathematics | 28.15 | 25.93 |
| | high_school_physics | 29.80 | 30.46 |
| | high_school_statistics | 38.43 | 26.39 |
| | machine_learning | 40.18 | 29.46 |
| 社会科学 | econometrics | 26.32 | 26.32 |
| | high_school_geography | 53.54 | 36.36 |
| | high_school_government_and_politics | 62.18 | 40.41 |
| | high_school_macroeconomics | 42.56 | 30.77 |
| | high_school_microeconomics | 45.80 | 26.89 |
| | high_school_psychology | 54.13 | 39.27 |
| | human_sexuality | 51.15 | 35.11 |
| | professional_psychology | 42.48 | 31.54 |
| | public_relations | 55.46 | 33.64 |
| | security_studies | 44.90 | 34.29 |
| | sociology | 51.74 | 31.84 |
| | us_foreign_policy | 61.00 | 46.00 |
| 人文学科 | formal_logic | 27.78 | 23.02 |
| | high_school_european_history | 58.18 | 35.76 |
| | high_school_us_history | 58.33 | 40.69 |
| | high_school_world_history | 67.09 | 32.07 |
| | international_law | 56.20 | 42.15 |
| | jurisprudence | 43.52 | 35.19 |
| | logical_fallacies | 57.06 | 31.29 |
| | moral_disputes | 47.11 | 36.71 |
| | moral_scenarios | 24.25 | 24.36 |
| | philosophy | 45.34 | 35.37 |
| | prehistory | 50.93 | 40.43 |
| | professional_law | 37.94 | 29.53 |
| | world_religions | 55.56 | 42.11 |
| 其他 | business_ethics | 51.00 | 34.00 |
| | clinical_knowledge | 48.68 | 35.85 |
| | colledge_medicine | 43.35 | 28.90 |
| | glocal_facts | 35.00 | 23.00 |
| | human_aging | 45.29 | 32.29 |
| | management | 56.31 | 27.18 |
| | marketing | 67.52 | 39.74 |
| | medical_genetics | 48.00 | 45.00 |
| | miscellaneous | 61.18 | 40.23 |
| | nutrition | 50.65 | 32.35 |
| | professional_accounting | 35.46 | 28.72 |
| | professional_medicine | 43.38 | 18.01 |
| | virology | 39.16 | 28.31 |

下面是一个带 1-shot 引导的提示示例。我们在下一个 token 上预测 ['A', 'B', 'C', 'D'] 的概率，并取概率最大者作为答案。

（MMLU 1-shot 示例）

```text
The following are multiple choice questions about philosophy.

According to d’Holbach, people always act according to _____.
(A) free choices (B) dictates of the soul (C) necessary natural laws (D) undetermined will
Answer: (C) necessary natural laws

Epicurus holds that philosophy is:
(A) not suitable for the young. (B) not suitable for the old. (C) important, but unpleasant. (D) none of the above.
Answer: (
```

#### C.7 中文语言理解评测

这里详述我们用于 CLUE（[Xu et al., 2020](#bib.bib127)）与 FewCLUE（[Xu et al., 2021](#bib.bib128)）评测的提示。在中文数据集上，提示会遇到一些挑战，因为中文文本以单字而非词为单位组织，很多情况下 verbalizer 长度并不相等。尽管数据集特定的校准（[Wang et al., 2021](#bib.bib117)；[Wu et al., 2021](#bib.bib124)）可以帮助缓解该问题，这种过于特定的技术在实现上可能相当复杂。本文的评测采用一种更易解决、利用 GLM-130B 独有特性的方法。由于 GLM-130B 是带英文 MIP 的双语 LLM，我们在中文数据集评测中采用（[Bach et al., 2022](#bib.bib5)）中类似任务的英文提示与 verbalizer，并发现这一策略相当有效。在评测指标方面，除 DRCD 与 CMRC2018 两个问答数据集报告 EM 外，其余数据集均报告准确率。

#### C.8 自然语言生成

自然语言生成，或这里的条件自然语言生成，指基于给定信息（如表格与文档）生成文本的任务。我们在数据到文本与摘要任务上评测 GLM-130B。数据集包括来自 GEM 生成基准（[Gehrmann et al., 2021](#bib.bib35)）的 WebNLG 2020（[Castro Ferreira et al., 2020](#bib.bib15)）、Clean E2E NLG（[Dušek et al., 2019](#bib.bib28)）与 WikiLingua（[Scialom et al., 2020](#bib.bib96)）。我们选择测试集中完整的 WebNLG 2020 与 Clean E2E NLG，并遵循（[Chowdhery et al., 2022](#bib.bib18)）的做法从 WikiLingua 中随机选择 5000 个测试样本。遵循 PaLM 中的设置，摘要任务使用的提示为「Summarize the following article:」，数据到文本任务使用的提示为「Verbalize:」。一个例外是 E2E：我们使用 promptsource 中提供的「generate-gramatically-correct-text from」提示为 GLM-130B 与 GPT-3 175B（Davinci）处理数据。所有评测均为 one-shot，示范样本从训练集中随机采样。我们报告 ROUGE-2、ROUGE-L（[Lin, 2004](#bib.bib57)）与 BLEURT-20（[Pu et al., 2021](#bib.bib77)）的 F 值。我们将我们的模型与 LaMDA、GPT-3 175B（Davinci）以及 PaLM 进行比较，其中 LaMDA 与 PaLM 的结果由（[Chowdhery et al., 2022](#bib.bib18)）报告，我们通过 OpenAI API 评测 GPT-3 175B（Davinci）¹³。

¹³ 我们使用 <https://github.com/google-research/google-research/tree/master/rouge> 的 ROUGE 实现与 <https://github.com/google-research/google-research/tree/master/rouge> 的 BLEURT-20 实现，后者的检查点可在 <https://storage.googleapis.com/bleurt-oss-21/BLEURT-20.zip> 获取。

结果见表 16。结果表明，GLM-130B 在所有任务上都比 LaMDA 与 GPT-3（Davinci）表现更好。在数据到文本任务上，GLM-130B 略逊于 PaLM-540B；而在摘要任务上，GLM-130B 的 ROUGE 结果甚至更高。我们还将 GLM-130B 消融为单向以展示双向注意力的优势。单向 GLM-130B 在全部三个数据集上都不及 GPT-3 175B，但当它切换为双向注意力后立即获得提升，使 GLM-130B 在少数情况下甚至可与 PaLM-540B 媲美。这表明，对给定上下文（即前缀）的双向注意力同样有益于文本生成任务。

表 16：1-shot GEM 英文自然语言生成任务（WebNLG、E2E 与 WikiLingua）。我们比较两个版本的 GLM-130B（uni：单向注意力；bi：双向注意力），表明双向注意力同样能提升条件生成的性能。

| 任务 | 数据集 | 指标 | LaMDA 137B | GPT-3 175B (Davinci) | GLM-130B | | PaLM-540B |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | | uni | bi | |
| 数据到文本 | WebNLG | ROUGE-2 | 30.5 | 29.9 | 25.3 | 38.5 | 44.4 |
| | | ROUGE-L | - | 41.2 | 36.7 | 49.3 | 53.8 |
| | | BLEURT-20 | - | 59.0 | 53.2 | 67.7 | 73.9 |
| | E2E | ROUGE-2 | 29.2 | 30.3 | 30.9 | 33.9 | 35.2 |
| | | ROUGE-L | - | 39.2 | 40.0 | 42.6 | 43.9 |
| | | BLEURT-20 | - | 64.5 | 65.0 | 68.1 | 69.7 |
| 摘要 | WikiLingua | ROUGE-2 | 5.4 | 7.2 | 5.8 | 10.4 | 9.9 |
| | | ROUGE-L | - | 18.9 | 16.4 | 23.4 | 20.6 |
| | | BLEURT-20 | - | 41.2 | 39.4 | 45.0 | 47.7 |

（E2E 示例，不含示范样本）

```text
Aleksandr_Prudnikov , height , 185.0 (centimetres).
FC_Spartak_Moscow , ground , Otkrytiye_Arena.
Aleksandr_Prudnikov , club , FC_Spartak_Moscow.
Verbalize:

Groundtruth: 185 centimetre tall Aleksandr Prudnikov played for the Otkrytiye Arena based FC Spartak, Moscow.
GPT-3 175B (Davinci): Aleksandr Prudnikov is a midfielder for FC Spartak Moscow, a football (soccer) club based in Moscow, Russia.
GLM-130B: Aleksandr Prudnikov is 185.0 cm tall and plays for FC Spartak Moscow.
```

（E2E 示例，不含示范样本）

```text
Combine all of the following data into a concise and grammatically correct text:
name : Blue Spice
eatType : coffee shop
area : riverside

Groundtruth: At the riverside, there is a coffee shop called The Blue Spice.
GPT-3 175B (Davinci): Blue Spice is a riverside coffee shop which is located on the corner of River Street and Riverbank Street.
GLM-130B: There’s a coffee shop that serves coffee in the riverside area, Blue Spice.
```

（WikiLingua 示例，不含示范样本）

```text
The majority of your customers will search for you online, so it’s essential to have a user-friendly website. At the very least, your website should include information about your business and your history in the moving industry, details about the quoting process, contact information, and a description of the services you offer. If possible, allow customers to schedule quotes online, view your availability, or read testimonials from other customers. One of the easiest ways to start your business is by helping people you already know with their moves. You can be on the lookout for any announcements related to moving that your friends make on social media. Once you have provided good service to friends, they are likely to recommend you to others. In order to spread the word about your business, have some professional looking promotional materials printed and distribute them around your community. You can distribute business cards at public events, tuck them into local bulletin boards, or even print them in directories, yearbooks, and other local print media. Flyers can be mailed, posted in public places, or distributed to businesses that might be able to refer customers to like you, such as furniture stores. Make sure you have a professional, recognizable logo that is consistent across all of your marketing materials. Another way to get your business’s name out there is to make yourself visible. Whether it’s by working with partners at local events, volunteering, or using your vehicle for an ad campaign, visibility is key for driving business. Build relationships with influential people in your community. Realtors are a great source of referrals to movers, as are the owners of local furniture stores or the office staff at a large apartment complex. You can use directory sites like Craigslist to advertise your services to people in your local community for free. Social media is also a great way to spread the word about your business. There are many options for advertising, depending on your budget and your target market. Consider options like PPC advertising, television and radio commercials, newspaper ads, direct mail flyers, or memberships with referral services. The best thing you can do to grow your business is to provide excellent service to your customers. Be sure to always be on time, be friendly, be respectful of your customers’ belongings, and offer accurate price quotes. Be sure to ask your happy customers to post reviews about you online. New customers will see these reviews and will have more faith in you as a reputable company if they see that others have had a good experience. You will inevitably end up having to deal with an unhappy customer at some point, but do your best to resolve the problem to the customer’s satisfaction. The last thing you want is negative reviews about your business circulating the internet! Summarize the article:

Groundtruth: Create a website. Start with friends. Distribute business cards and flyers. Network for promotion. Seek out free advertising opportunities. Consider paid advertising. Gain a good reputation.
GPT-3 175B (Davinci): Market yourself online. Look for opportunities to market your services offline.
GLM-130B: Have a user-friendly website. Promote your business through social media. Build relationships with influential people in your community. Use directory sites like Craigslist to advertise your services.
```

表 17：Winograd 风格任务评测（Winogender 与 Winograd273）。所有分数均为准确率。K 表示 shot 数量。∗PaLM 540B 未报告确切的 0-shot Winogender 结果，因此我们只能从其图中估算一个数值。

| 任务 | K | GPT-3 (Davinci) | OPT 175B | BLOOM 176B | PaLM 540B | Chinchilla | Gopher 280B | GLM-130B |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Winogender | 0 | 64.2 | 54.8 | 49.1 | 75.0∗ | 78.3 | 71.4 | 79.7 |
| Winogender | 1 | 62.6 | - | 53.1 | 79.4 | - | - | 80.7 |
| Winograd273 | 0 | 88.3 | 52.9 | 49.1 | 90.1 | - | - | 84.3 |

表 18：闭卷问答（Natural Questions、StrategyQA）。

| | GPT-3 (Davinci) | BLOOM 176B | PaLM 540B | Chinchilla | Gopher 280B | GLM-130B |
| --- | --- | --- | --- | --- | --- | --- |
| Natural Questions (EM) | 14.6 | 13.1 | 21.2 | 16.6 | 10.1 | 11.7 |
| StrategyQA (Acc) | 52.3 | 49.8 | 64.0 | - | - | 60.6 |

表 19：常识推理（Commonsense QA、MC-TACO）。K 表示 shot 数量。

| | K | GPT-3 (Davinci) | OPT 175B | BLOOM 176B | GLM-130B |
| --- | --- | --- | --- | --- | --- |
| Commonsense QA (Acc) | 0 | 57.2 | - | 42.8 | 61.6 |
| Commonsense QA (Acc) | 1 | 61.2 | - | - | 62.2 |
| MC-TACO (EM) | 0 | - | 12.4 | 13.1 | 13.6 |

#### C.9 Winograd 风格任务

我们纳入了 Winograd 风格任务的评测，它源自经典的 Winograd 模式挑战（[Levesque et al., 2012](#bib.bib52)），旨在测试机器在歧义语境下对共指消解的理解。由于 MIP 中已纳入 Winogrande（[Sakaguchi et al., 2021](#bib.bib90)）与 SuperGLUE WSC（[Wang et al., 2019](#bib.bib113)），这里我们在 Winogender（[Rudinger et al., 2018](#bib.bib88)）与 Winograd273（[Levesque et al., 2012](#bib.bib52)）上测试。对于 Winogender，GPT-3 的结果通过 OpenAI API 获取，BLOOM 的 1-shot 结果由我们自行评测。对于 Winograd273，由于既有工作（[Brown et al., 2020](#bib.bib12)；[Chowdhery et al., 2022](#bib.bib18)）表明 1-shot 学习几乎不带来提升，我们只测试零样本结果。另一件需要注意的是，尽管 GPT 风格模型（如 GPT-3、PaLM）采用（[Radford et al., 2019](#bib.bib80)）所述的「部分评测（partial evaluation）」，我们发现提示「<sentence> The "<pronoun>" refers to [MASK]」对 GLM-130B 更好，因此在评测中采用它。

结果见表 17。GLM-130B 在 Winogender 上于所有被评测 LLM 中表现最佳，在 Winograd273 上略逊于 GPT-3 与 PaLM。

#### C.10 闭卷问答

闭卷问答（CBQA）（[Roberts et al., 2020](#bib.bib86)）是与传统「开卷」评测相对的、被广泛采用的任务，用于评测语言模型对事实性知识的记忆。由于我们已在 MIP 训练中纳入 TriviaQA（[Joshi et al., 2017](#bib.bib47)）与 WebQuestions（[Berant et al., 2013](#bib.bib7)），这里选择 Natural Questions（[Kwiatkowski et al., 2019](#bib.bib49)）与 StrategyQA（[Geva et al., 2021](#bib.bib36)）作为 CBQA 的评测数据集。

结果见表 18。GLM-130B 在 Natural Questions 上表现相对较弱，在 StrategyQA 上表现良好。我们推测，GLM-130B 在 Natural Questions 上的欠佳表现可能源于对英文语料的拟合不足——它大约只见过 200B 英文 token，因此没有很好地记住细粒度的知识。由于 CBQA 似乎是一项尤其强调记忆的任务（Chinchilla（[Hoffmann et al., 2022](#bib.bib41)）的强劲表现即说明了这一点），我们认为经过后续充分训练，GLM-130B 可以表现更好。

#### C.11 常识推理

这里我们在常识推理能力上评测 GLM-130B 与其他一些 LLM。由于 MIP 训练中已纳入 PIQA（[Bisk et al., 2020](#bib.bib8)）、ARC（[Clark et al., 2018](#bib.bib19)）与 OpenbookQA（[Mihaylov et al., 2018](#bib.bib66)），我们在评测中另外选择了两个被广泛采用的常识推理数据集：Commonsense QA（[Talmor et al., 2019](#bib.bib105)）与多选时序常识（MC-TACO，[Zhou et al. (2019)](#bib.bib135)）。对于 Commonsense QA，我们通过 OpenAI Davinci API 测试 GPT-3，通过其 Huggingface 实现测试 BLOOM-176B，GLM-130B 则使用 promptsource（[Bach et al., 2022](#bib.bib5)）中的提示「answer_given_question_without_options」。对于 StrategyQA，我们遵循（[Zhou et al., 2019](#bib.bib135)）提供的 EM 计算方法。

结果见表 19。可以看到，GLM-130B 在 Commonsense QA 与 MC-TACO 上均在被评测 LLM 中表现最佳，表明 GLM-130B 对常识知识有良好的掌握。OPT 的结果因附录 C.3 中所述的原因未予纳入。

#### C.12 固定标签数据集：以自然语言推理为例

如第 5 节所述，由于使用了 MIP，我们在 GLM-130B 的评测中对零/少样本学习数据集的挑选采用了相当严格的标准。然而，该标准显著减少了我们目前可以评测的数据集，尤其是部分读者质疑不评测 MIP 已见过的固定标签数据集（如自然语言推理 NLI）是否有必要，并建议我们可以在独立章节中报告它们以避免混淆。

坦率地说，在这种设置下 GLM-130B 的零/少样本学习可能相当占优。下面我们以 NLI 为典型例子，展示 GLM-130B 在这些场景中的优势表现。我们纳入 6 个广泛使用的 NLI 数据集——它们未被纳入 GLM-130B 的 MIP 训练——作为基准。结果见表 20，它表明由于已见过的任务类型，GLM-130B 的「零样本」表现可能会好得多。

表 20：GLM-130B 在 6 个典型自然语言推理（NLI）数据集上的「零样本」结果。∗免责声明：尽管这些数据集从未被见过，但一些其他 NLI 数据集已被纳入 GLM-130B 的 MIP，使其区别于既有的标准零样本设置。

| | BLOOM 176B | OPT 175B | GLM-130B∗ |
| --- | --- | --- | --- |
| qnli (valid, median of 5 prompts) | 50.9 | 55.4 | 86.7 |
| mnli (valid, median of 15 prompts) | 35.5 | 36.0 | 85.7 |
| mnli_mismatched (valid, median of 15 prompts) | 35.5 | 36.0 | 84.6 |
| wnli (valid, median of 5 prompts) | 57.7 | 53.5 | 67.6 |
| glue/cola (valid, median of 5 prompts) | 39.0 | 44.4 | 57.6 |
| glue/mrpc (valid, median of 5 prompts) | 31.6 | 44.6 | 87.3 |

#### C.13 SuperGLUE

图 17：GLM-130B（uni 与 bi）在 SuperGLUE 开发集上的未微调结果，使用 promptsource（[Bach et al., 2022](#bib.bib5)）的提示与任务形式。免责声明：请注意，部分 SuperGLUE 训练集已被纳入 MIP 训练。我们在此报告结果仅供参考。

我们还报告 GLM-130B 在 SuperGLUE（[Wang et al., 2019](#bib.bib113)）基准上的评测，该基准由 8 个不同的自然语言理解挑战组成。请注意，这些结果既不是零/少样本结果，也不是微调结果，因为 8 个任务中有 7 个（ReCoRD 除外）的训练集已与其他 67 个多任务数据集一同被纳入 GLM-130B 的 MIP 训练；然而，GLM-130B 也没有在其中任何一个任务上被单独微调。因此，这些结果不能用于与其他模型做相对比较，仅供读者参考 GLM-130B 的绝对能力。

| | BoolQ | CB | COPA | MultiRC | ReCoRD | RTE | WiC | WSC |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GLM-130B | 89.69 | 98.21 | 100 | 89.32 | 92.11 | 94.22 | 76.96 | 88.5 |

表 21：GLM-130B 使用 P-tuning v2（[Liu et al., 2022](#bib.bib62)）在 SuperGLUE 数据集上取得的结果。除 MultiRC（F1a）与 ReCoRD（F1）外，所有数据集均报告 Accuracy 指标。

结果见图 17。我们消融了单向与双向 GLM-130B，以论证 GLM 目标在提升 LLM 理解能力方面的作用。图中每个点对应一个特定提示的结果，提示来自 promptsource（[Bach et al., 2022](#bib.bib5)）仓库。我们同样采用 promptsource 的任务形式。可以观察到，GLM（bi）在所有任务上都具有小得多的方差与更高的性能。对于部分任务（如 CB、MultiRC、RTE、COPA 与 BoolQ），GLM-130B 甚至可以达到超过 80% 的准确率。

我们还尝试在 SuperGLUE 数据集上微调 GLM-130B。然而，当我们在下游任务上使用全参数微调时，遇到了单个 epoch 内迅速过拟合的问题，导致验证集上表现不佳。为解决这一问题，我们探索了高效参数微调方法——它们只调整少量参数，更不易过拟合。在试验多种方法后，我们采用 P-Tuning v2（[Liu et al., 2022](#bib.bib62)），它在 GLM-130B 上取得了与全参数微调相当的结果，但只调整 0.1% 至 3% 的参数。我们使用 P-Tuning v2 的实验结果见表 21。

#### C.14 思维链提示

图 18：与标准提示相比，思维链提示同样能提升 GLM-130B 在推理任务上的表现。

我们遵循 [Wei et al. (2022c)](#bib.bib122) 的设置，评测末字母拼接（Last letter concatenation，LLC）、抛硬币（Coin Flip）、反转列表（Reverse List），以及 BIG-bench（[Srivastava et al. (2022)](#bib.bib102)）的两个任务——运动理解（Sports understanding）与日期理解（Date understanding）——上的思维链提示表现。结果见图 18。我们发现，思维链提示可以提升 GLM-130B 在符号推理与常识推理上的表现。

末字母拼接（LLC）。该任务要求模型拼接一个名字中各单词的末字母（如 "Elon Musk" -> "nk"）。我们通过从姓名普查数据¹⁴中随机拼接前 1000 个名字与姓氏来生成全名。

¹⁴ <https://namecensus.com>

抛硬币。该任务要求模型回答一枚最初正面朝上的硬币，在人们翻转或不翻转之后是否仍然正面朝上（如 "A coin is heads up. Phoebe flips the coin. Osvaldo does not flip the coin. Is the coin still heads up?" -> "no"）。我们还额外评测了查询样本中人数多于上下文示例中人数的场景，即分布外（OOD）设置。

反转列表。该任务要求模型反转一个日常物品列表的顺序（如 "cigar, umbrella, key, gum, alarm" -> "alarm, gum, key, umbrella, cigar"）。我们通过从日常物品词表¹⁵中随机采样生成这些列表。

¹⁵ <https://www.vocabulary.com/lists/189583>

运动理解。该任务要求模型判断一个关于运动员的陈述的真实性（如 "Joao Moutinho caught the screen pass in the NFC championship" -> "false"）。

日期理解。该任务要求模型从给定上下文推断日期（如 "2015 is coming in 36 hours. What is the date one week from today in MM/DD/YYYY?" -> "01/05/2015"）。

我们使用与 [Wei et al. (2022c)](#bib.bib122) 相同的示例与思维链。对每个任务，我们尝试两种不同的提示格式以及单向与双向两种注意力机制，并报告最佳表现。第一种格式是「Question: {context} Answer: {target}」；第二种是在第一种提示格式的示例前加上序号。结果见图 18。

图 19：GLM-130B 的对数缩放能力任务。这些任务的表现随 GLM 参数量对数增长。大多数传统 NLP 任务遵循相同模式。

图 20：GLM-130B 的涌现能力任务。这些任务的表现直到模型规模达到某个阈值（如 100B 或 10B）之前都增长不多；达到阈值后，模型表现迅速飙升。BIG-bench（[Srivastava et al., 2022](#bib.bib102)）基准收集了许多这类挑战。

### 附录 D GLM-130B 的缩放与涌现能力

扩大预训练语言模型的规模已被证明能在广泛任务上持续提升下游性能。然而，从小规模无法预测的涌现能力也随之出现。为说明这一点，我们进行了大量实验来探索缩放性质与涌现能力。遵循既有文献（[Wei et al., 2022b](#bib.bib121)），我们基于观察将 NLP 任务分为两类：

- 对数缩放能力任务（参见图 19）：任务表现随模型参数数量对数增长。典型任务与数据集包括 LAMBADA、Wikitext-103、Wikitext-2、Penn Tree Bank。
- 涌现能力任务（参见图 20）：任务表现只有在模型参数量达到某个阈值后才飙升。典型任务与数据集包括 MMLU，以及来自 BIG-bench（[Srivastava et al., 2022](#bib.bib102)）的 hindu_knowledge、crass_ai、implicatures、understanding_fables、modified_arithmetic、implicit_relations 与 gre_reading_comprehension。

与（[Wei et al., 2022b](#bib.bib121)）的观察一致，我们表明 GLM-130B 也呈现与 GPT-3、LaMDA、PaLM 等其他 LLM 类似的两种缩放行为。尽管 LLM 为何以及如何呈现这些引人入胜的性质仍不清楚，GLM-130B 为所有研究者提供了开放的机会来检验并理解其背后的原因。

### 附录 E 贡献

GLM-130B 项目于 2021 年 12 月构想，其预训练部分于 2022 年 7 月 3 日完成，评测与应用仍在进行中。在此过程中，我们经历了各种技术与工程挑战（详见附录 F 与图 21）。如果没有多个团队的合作，不可能达到当前状态——清华大学知识工程组（KEG）、移动、加速与网络系统并行架构与编译技术组（PACMAN）、自然语言处理组（THUNLP），以及智谱 AI（Zhipu.AI）。详细贡献列举如下。

#### E.1 准备

- 模型实现：Aohan Zeng、Zhengxiao Du
- 自监督数据处理：Ming Ding、Wendi Zheng
- 多任务数据处理：Xiao Liu、Xiao Xia
- 模型架构：Aohan Zeng、Xiao Liu、Zhengxiao Du、Hanyu Lai
- 训练稳定性：Aohan Zeng、Xiao Liu、Ming Ding
- 3D 并行与训练效率：Aohan Zeng、Zixuan Ma、Jiaao He、Zhenbo Sun

#### E.2 模型训练

- 大规模训练与监控：Aohan Zeng、Xiao Liu
- 模型性能验证：Aohan Zeng

#### E.3 后训练

- 评测框架：Aohan Zeng、Zhengxiao Du
- 语言建模评测：Aohan Zeng
- MMLU 与 BIG-Bench 评测：Aohan Zeng
- CLUE 与 FewCLUE 评测：Xiao Liu、Aohan Zeng
- 伦理评测：Yifan Xu、Aohan Zeng、Xiao Liu、Zihan Wang
- 基线评测：Xiao Liu、Jifan Yu、Weng Lam Tam
- INT4 量化：Aohan Zeng、Zihan Wang、Xiao Liu、Hanyu Lai
- 推理加速：Zihan Wang、Aohan Zeng
- 低资源推理：Gouyang Zeng、Xu Han、Weilin Zhao、Zhiyuan Liu
- 演示与 API：Hanyu Lai、Jifan Yu、Xiaohan Zhang、Yufei Xue、Shan Wang、Jiecai Shan、Haohan Jiang、Zhengang Guo
- 手稿撰写：Xiao Liu、Yuxiao Dong 与 Jie Tang 撰写正文，Xiao Liu、Aohan Zeng 与 Zhengxiao Du 撰写附录。

#### E.4 项目管理

- 学生负责人：Aohan Zeng、Xiao Liu
- 技术顾问：Yuxiao Dong、Jidong Zhai、Wenguang Chen、Zhiyuan Liu、Peng Zhang、Jie Tang
- 项目负责人：Jie Tang

#### E.5 算力赞助

- GPU 赞助：智谱 AI（Zhipu.AI）

### 附录 F GLM-130B 简史

![图 21](2210.02414v2/glm130b-timeline-v2.png)

图 21：截至 2022 年 7 月 31 日，GLM-130B 训练所遇到并解决的主要问题时间线。

GLM-130B 项目¹⁶于 2021 年 12 月在清华 KEG 的一次头脑风暴会议中被构想。我们坚信，预训练一个高精度语言模型——尤其是同时面向中文与英文——具有重要价值。尽管 GPT-3（[Brown et al., 2020](#bib.bib12)）是这一努力的先驱，但世界上大多数人无法使用它；此外，它只支持英文。因此我们决定启动 GLM-130B 项目。请注意，我们去年构建的悟道 1.75T 模型是一个具有 480 个专家的稀疏混合专家（MoE）模型，而非 GPT-3 那样的稠密模型。我们的目标是训练一个在下游任务上具有高精度的双语预训练稠密模型，并向世界上所有人开放——任何人在任何地方都可以下载它，并在配备合适 GPU 的单台服务器上使用它。

¹⁶ 本节大部分内容提取并更新自清华 KEG 的 GLM-130B 博客介绍 <http://keg.cs.tsinghua.edu.cn/glm-130b/>（发布日期：2022 年 8 月 4 日）。

这个雄心勃勃的项目很快面临几个重要挑战：

- 缺乏算力资源：没有组织愿意赞助这样一个大项目并免费将其公开。
- 缺乏稳健的预训练算法：尽管 GPT-3 在英文语料上取得了成功，但如何为英文与中文训练一个高精度的双语模型尚不清楚。
- 缺乏快速推理方案：由于目标是让模型面向所有人公开，我们需要设计资源需求低的快速推理方案来运行模型。

对于预训练算法，我们最终选择了 GLM（[Du et al., 2022](#bib.bib27)），因为其在实践中的高性能。经过数轮讨论与探索，我们最终决定训练一个 1300 亿参数的 GLM 模型，因为这样的规模使其有可能在单台 A100（40G×8）服务器上运行推理。

我们对模型的第一次训练尝试是在 2022 年 1 月，此前不久我们刚收到一小批用于测试运行的 GPU 赞助。然而我们很快意识到，我们严重低估了预训练这一规模（>100B）模型的技术难度。预训练一个高精度的 100B 规模模型似乎与训练 10B 规模模型大不相同。由于频繁的随机硬件故障、模型梯度爆炸、算法中意外的过量显存占用、在新版 Megatron 与 DeepSpeed 框架中对 3D 流水线的调试、无法从优化器状态恢复、进程间 TCP 响应阻塞，以及许许多多意想不到的「bug」，项目多次延期。在这个艰难时刻，清华 PACMAN 团队伸出援手，我们一起成功修复了大部分「bug」。

到 3 月，我们仍缺乏算力资源，但幸运地得到机会在另外几个平台上尝试测试运行，包括昇腾 910（Ascend 910）、海光 DCU（Hygon DCU）、NVIDIA 与神威（Sunway）。直接的挑战是让我们的训练代码适配这些不同的平台，因为底层算子的差异相当大。这也带来了许多新问题：不支持大维度向量快速计算的逐元素算子；种种阻碍收敛的问题——输入嵌入的大梯度范数、原生 Post-LN、Pre-LN 与 Sandwich-LN、dataloader 状态种子，以及 Softmax 与 Attention 中的计算精度选择——还有我们自己犯的无数错误。在所有慷慨伙伴的巨大帮助下，我们最终成功使我们的预训练算法在所有平台上均可运行——坦率地说，这对本项目是一项令人惊讶的成就。图 21 中 GLM-130B 的时间线涵盖了截至撰写本文时我们遇到并解决的大部分问题。

4 月 26 日，我们收到了智谱 AI（Zhipu.AI）的慷慨算力赞助——这是一家旨在教机器像人类一样思考的 AI 创业公司。又经过一周的测试，我们于 5 月 6 日在其 96 台 A100（40G×8）服务器上正式启动 GLM-130B 模型的训练。此外，智谱 AI 还派出一个团队帮助评测预训练模型并搭建演示网站。

训练期历时两个月，期间我们开始开发一套工具包，利用交换（swapping）技术与量化实现 GLM-130B 在低资源环境下的推理。尽管它已经是同规模模型中最易获取的，我们仍与来自清华 NLP 的伙伴一起，持续探索普及型硬件平台的极限，以真正让 100B 规模模型惠及尽可能多的人。到目前为止，我们成功实现了 GLM-130B 的 INT4 权重量化。重要的是，未经后训练的 INT4 版 GLM-130B 与未压缩原版相比性能下降可忽略，而其 GPU 显存消耗仅为未压缩版本的 25%，从而支持在 4×RTX 3090 Ti（24G）或 8×RTX 2080 Ti（11G）上高效推理。我们将尝试进一步降低资源需求，并就这一重要工作项持续向社区更新。

### 附录 G 更广泛的影响

本文介绍了一个拥有 1300 亿参数的开放双语预训练语言模型。目前，大多数参数量超过 1000 亿的预训练语言模型由政府与大公司私有（[Brown et al., 2020](#bib.bib12)；[Thoppilan et al., 2022](#bib.bib107)；[Rae et al., 2021](#bib.bib81)；[Chowdhery et al., 2022](#bib.bib18)；[Wang et al., 2021](#bib.bib117)）。其中少数（[Brown et al., 2020](#bib.bib12)；[Lieber et al., 2021](#bib.bib56)）提供收费的有限推理 API。相比之下，GLM-130B 的权重与代码向所有对 LLM 感兴趣的人开放。此外，我们通过加速实现与 INT4 量化显著降低了推理的硬件要求。本文可以对研究社区、个人开发者与小公司以及社会产生更广泛的影响。

#### G.1 对 AI 研究的影响

大多数研究机构无法承担预训练大语言模型的巨额成本。因此，除政府与大公司的员工外，大多数研究者只能访问收费的有限推理 API。借助推理 API，研究者只能将模型输出当作黑盒来分析，这限制了潜在工作的范围。有了 GLM-130B，研究者可以分析模型参数以及特定输入对应的内部状态，从而对 LLM 的理论、能力与缺陷进行深入研究。研究者还可以修改模型架构与权重，以验证所提出的改进 LLM 的算法 [Zhu et al. (2020)](#bib.bib136)；[Cao et al. (2021)](#bib.bib13)；[Hase et al. (2021)](#bib.bib37)；[Mitchell et al. (2022)](#bib.bib67)。

借助 INT4 量化，GLM-130B 可以在 4×RTX 3090 或 8×RTX 2080 Ti 等普及型 GPU 上执行推理，这些 GPU 通过云服务很容易获取。因此，负担不起 DGX-A100 等强力数据中心 GPU 服务器的研究者也可以利用 GLM-130B。

#### G.2 对个人开发者与小公司的影响

目前，希望将 LLM 集成到业务中的个人开发者与小公司只能选择付费推理 API，由此增加的成本可能阻碍他们的尝试。相反，GLM-130B 可以部署在他们自有或可通过云服务获取的普及型硬件上以降低成本。此外，他们可以利用蒸馏技术 [Sanh et al. (2019)](#bib.bib92)；[Jiao et al. (2020)](#bib.bib46) 获得在其特定任务上保持相当性能的更小模型。虽然一些开发者可能缺乏独立完成部署与蒸馏的能力，我们相信随着 GLM-130B 以及未来更多开放 LLM 的出现，相应的工具链与服务提供方将更加可得。

我们还注意到，目前大多数 LLM 应用基于提示工程，部分原因在于推理 API 的限制。在线客服等下游场景中，公司积累了包含领域知识的海量人工生成数据。有了开源权重与代码，开发者可以在自己的数据上微调 GLM-130B，以弥补领域知识的差距。

#### G.3 社会影响

大语言模型与其他不同模态的机器学习模型（如图像（[Ramesh et al., 2021](#bib.bib83)；[Ding et al., 2021](#bib.bib25)；[Saharia et al.,](#bib.bib89)）与视频（[Hong et al., 2022](#bib.bib42)））一起，可能被用于为有害应用生成合成文本，例如电话营销诈骗、政治宣传与个人骚扰，正如（[Weidinger et al., 2021](#bib.bib123)；[Sheng et al., 2021](#bib.bib98)；[Dev et al., 2021](#bib.bib23)）中所讨论的。我们不预期在使用该模型后会出现任何危险的输出，尤其是针对弱势群体与历史上处于不利地位的群体。

虽然一些人认为限制对 LLM 的访问可以防止此类有害应用，我们主张推动 LLM 包容性能够更好地防御 LLM 可能造成的伤害。目前，只有政府与大公司负担得起预训练 LLM 的可观成本。拥有雄厚资金去预训练 LLM 的组织，并不能保证不会用它作恶。如果无法接触这样的 LLM，个人甚至无法意识到 LLM 在其中扮演的角色。相反，发布一个开放的 LLM 可以为所有研究者提供访问与透明度，并推动减少 LLM 潜在伤害的研究，例如识别合成文本的算法 [Gehrmann et al. (2019)](#bib.bib34) 或检测假新闻 [Li et al. (2021)](#bib.bib54)。

同样众所周知的是，LLM 可能存在公平性、偏见、隐私与真实性方面的问题 [Zhang et al. (2021)](#bib.bib132)；[Lin et al. (2022)](#bib.bib58)；[Liang et al. (2021)](#bib.bib55)；[Bender et al. (2021)](#bib.bib6)。开放的 LLM 可以揭示模型参数以及特定输入对应的内部状态，而不是只为黑盒模型提供 API。总之，研究者可以深入分析 LLM 的缺陷，并提出改进算法来解决这些问题。

### 附录 H 环境影响

对大语言模型的主要担忧之一，是其巨大的能源消耗与相应的碳排放 [Strubell et al. (2019)](#bib.bib103)；[Lacoste et al. (2019)](#bib.bib50)；[Patterson et al. (2021)](#bib.bib74)；[Bender et al. (2021)](#bib.bib6)。据估算，GPT-3 产生了 500 吨的碳排放足迹（CO2eq）[Patterson et al. (2021)](#bib.bib74)。我们在为期 60 天的训练过程中共消耗 442.4MWh 电力。按当地电网 0.5810 kg/kWh 的碳效率计算，预训练释放了 257.01 吨二氧化碳。这大约是 GPT-3 碳足迹的一半，可能得益于高效的并行策略与 NVIDIA 的硬件改进。该碳排放量大致相当于 18 个美国人一年的排放量。然而我们相信，随着 GLM-130B 的发布，可以节省更多用于复现 100B 规模 LLM 的碳排放。
