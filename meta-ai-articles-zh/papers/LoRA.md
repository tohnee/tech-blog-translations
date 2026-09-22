---
title: "LoRA：大语言模型的低秩适配"
title_en: "LoRA: Low-Rank Adaptation of Large Language Models"
arxiv: 2106.09685
date: 2021-06-17
source: https://arxiv.org/abs/2106.09685
crawled: 2026-09-22
translated: 2026-09-22
---

# LoRA：大语言模型的低秩适配

> 原文：[LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685) · Microsoft arXiv

Edward Hu*、Yelong Shen*、Phillip Wallis、Zeyuan Allen-Zhu、Yuanzhi Li、Shean Wang、Lu Wang、Weizhu Chen
*同等贡献。
隶属：Microsoft Corporation（微软公司）
联系方式：{edwardhu, yeshe, phwallis, zeyuana, yuanzhil, swang, luw, wzchen}@microsoft.com
（版本 2）

###### 摘要

自然语言处理的一个重要范式是：先在通用领域数据上进行大规模预训练，再适配到特定任务或领域。
随着我们预训练的模型越来越大，重新训练所有模型参数的全量微调（full fine-tuning）变得愈发不可行。
以 GPT-3 175B 为例——部署多个独立的微调模型实例、每个都有 1750 亿参数，其成本高得令人望而却步。
我们提出低秩适配（Low-Rank Adaptation，LoRA），它冻结预训练模型权重，并在 Transformer 架构的每一层注入可训练的秩分解矩阵，从而大幅减少下游任务的可训练参数数量。
与使用 Adam 微调的 GPT-3 175B 相比，LoRA 可将可训练参数数量减少 10,000 倍，GPU 内存需求降低 3 倍。
尽管可训练参数更少、训练吞吐量更高，并且与适配器（adapter）不同、不引入任何额外推理延迟，LoRA 在 RoBERTa、DeBERTa、GPT-2 和 GPT-3 上的模型质量与微调持平或更优。
我们还对语言模型适配中的秩亏（rank-deficiency）现象进行了实证研究，揭示了 LoRA 有效的原因。
我们发布了便于将 LoRA 与 PyTorch 模型集成的软件包，并在 <https://github.com/microsoft/LoRA> 提供 RoBERTa、DeBERTa 和 GPT-2 的实现与模型检查点。

脚注：与 V1 相比，本稿包含更好的基线、GLUE 上的实验，以及更多关于适配器延迟的内容。

## 1 引言

图 1：我们的重参数化。我们只训练 $A$ 和 $B$。

自然语言处理中的许多应用都依赖于把*一个*大规模预训练语言模型适配到*多个*下游应用。
这种适配通常通过*微调*完成，即更新预训练模型的全部参数。
微调的主要缺点是：新模型包含与原始模型同样多的参数。
随着每隔几个月就有更大的模型被训练出来，这对 GPT-2（Radford et al., b）或 RoBERTa large（Liu et al., 2019）来说还只是「不便」，而对拥有 1750 亿可训练参数的 GPT-3（Brown et al., 2020）而言已成为关键的部署挑战¹。
虽然 GPT-3 175B 借助少样本学习已能取得不俗的性能，但正如附录 A 所示，微调能显著提升其性能。

许多人试图通过只适配部分参数或为新任务学习外部模块来缓解这一问题。
这样，除了预训练模型之外，每个任务只需存储和加载少量任务专属参数，从而大幅提升部署时的运营效率。
然而，现有技术往往通过加深模型来引入推理延迟（Houlsby et al., 2019；Rebuffi et al., 2017），或缩短模型可用的序列长度（Li & Liang, 2021；Lester et al., 2021；Hambardzumyan et al., 2020；Liu et al., 2021）（见第 3 节）。
更重要的是，这些方法常常无法追平微调基线，在效率与模型质量之间形成了权衡。

我们从 Li et al.（2018a）；Aghajanyan et al.（2020）中获得灵感，它们表明学习到的过参数化模型实际上处于一个低内在维度（intrinsic dimension）上。
我们假设模型适配期间的权重变化也具有很低的「内在秩（intrinsic rank）」，由此提出了低秩适配（LoRA）方法。
LoRA 让我们能够间接地训练神经网络中的某些稠密层：不是直接训练这些层的权重，而是优化其适配期间变化的秩分解矩阵，同时保持预训练权重冻结，如图 1 所示。
以 GPT-3 175B 为例，我们表明即使满秩（即 d）高达 12,288，非常低的秩（即图 1 中的 r 取一或二）就足够了，这使得 LoRA 在存储和计算上都很高效。

LoRA 具备若干关键优势。

- 一个预训练模型可以被共享，用来为不同任务构建许多小型 LoRA 模块。
  我们可以冻结共享模型，通过替换图 1 中的矩阵 $A$ 和 $B$ 来高效切换任务，显著降低存储需求和任务切换开销。
- LoRA 让训练更高效，并将使用自适应优化器时的硬件门槛最多降低 3 倍，因为我们不需要为绝大多数参数计算梯度或维护优化器状态。
  相反，我们只优化注入的、小得多的低秩矩阵。
- 我们简单的线性设计允许在部署时将可训练矩阵与冻结权重合并，从结构上保证与全量微调模型相比不引入任何推理延迟。
- LoRA 与许多先前方法正交，可以与其中许多组合使用，例如前缀微调（prefix-tuning）。我们在附录 E 中给出一个例子。

#### 术语与约定

我们频繁引用 Transformer 架构并沿用其维度的惯用术语。
我们将 Transformer 层的输入和输出维度大小记为 $d_{model}$。
我们用 $W_q$、$W_k$、$W_v$ 和 $W_o$ 指代自注意力模块中的 query/key/value/output 投影矩阵。
$W$ 或 $W_0$ 指预训练权重矩阵，$\Delta W$ 指其在适配期间累积的梯度更新。
我们用 $r$ 表示 LoRA 模块的秩。
我们遵循（Vaswani et al., 2017；Brown et al., 2020）的约定，使用 Adam（Loshchilov & Hutter, 2019；Kingma & Ba, 2017）进行模型优化，并使用 Transformer MLP 前馈维度 $d_{ffn}=4\times d_{model}$。

## 2 问题陈述

虽然我们的提案与训练目标无关，但我们聚焦于语言建模作为驱动性用例。
下面对语言建模问题，特别是给定任务专属提示时条件概率最大化，做一个简要描述。

假设给定一个由 $\Phi$ 参数化的预训练自回归语言模型 $P_{\Phi}(y|x)$。
例如，$P_{\Phi}(y|x)$ 可以是基于 Transformer 架构（Vaswani et al., 2017）的通用多任务学习器，如 GPT（Radford et al., b；Brown et al., 2020）。
考虑将该预训练模型适配到下游条件文本生成任务，如摘要、机器阅读理解（MRC）和自然语言到 SQL（NL2SQL）。
每个下游任务由一个上下文-目标对组成的训练数据集表示：$\mathcal{Z}=\{(x_{i},y_{i})\}_{i=1,..,N}$，其中 $x_{i}$ 和 $y_{i}$ 都是 token 序列。
例如，在 NL2SQL 中，$x_{i}$ 是自然语言查询，$y_{i}$ 是其对应的 SQL 命令；在摘要任务中，$x_{i}$ 是一篇文章的内容，$y_{i}$ 是它的摘要。

在全量微调期间，模型被初始化为预训练权重 $\Phi_0$，并通过反复沿梯度更新为 $\Phi_0+\Delta\Phi$，以最大化条件语言建模目标：

$$\max_{\Phi}\sum_{(x,y)\in\mathcal{Z}}\sum_{t=1}^{|y|}\text{log}\left(P_{\Phi}(y_{t}|x,y_{<t})\right)\tag{1}$$

全量微调的主要缺点之一是：对*每个*下游任务，我们都要学习一组*不同的*参数 $\Delta\Phi$，其维度 $|\Delta\Phi|$ 与 $|\Phi_0|$ 相同。
因此，如果预训练模型很大（如 GPT-3，$|\Phi_0|\approx 175$ 十亿），存储和部署许多独立的微调模型实例即便可行，也极具挑战。

在本文中，我们采用一种参数效率更高的方法：任务专属的参数增量 $\Delta\Phi=\Delta\Phi(\Theta)$ 被进一步编码为一个规模小得多的参数集 $\Theta$，且 $|\Theta|\ll|\Phi_0|$。
于是，寻找 $\Delta\Phi$ 的任务变成了对 $\Theta$ 的优化：

$$\max_{\Theta}\sum_{(x,y)\in\mathcal{Z}}\sum_{t=1}^{|y|}\log\left({p_{\Phi_{0}+\Delta\Phi(\Theta)}(y_{t}|x,y_{<t}})\right)\tag{2}$$

在后续章节中，我们提出用一种低秩表示来编码 $\Delta\Phi$，它在计算和内存上都很高效。
当预训练模型为 GPT-3 175B 时，可训练参数的数量 $|\Theta|$ 可以小至 $|\Phi_0|$ 的 0.01%。

## 3 现有解决方案还不够好吗？

我们要解决的问题绝非新问题。
自迁移学习诞生以来，已有数十项工作致力于让模型适配更具参数和计算效率。
一些知名工作的综述见第 6 节。
以语言建模为例，高效适配有两种主流策略：添加适配器层（adapter layer）（Houlsby et al., 2019；Rebuffi et al., 2017；Pfeiffer et al., 2021；Rücklé et al., 2020），或优化某种形式的输入层激活（Li & Liang, 2021；Lester et al., 2021；Hambardzumyan et al., 2020；Liu et al., 2021）。
然而，这两种策略都有其局限性，尤其是在大规模、延迟敏感的生产场景中。

#### 适配器层会引入推理延迟

适配器有许多变体。
我们关注 Houlsby et al.（2019）的原始设计——每个 Transformer 块有两个适配器层，以及 Lin et al.（2020）的较新设计——每块只有一个适配器层但附加一个 LayerNorm（Ba et al., 2016）。
虽然可以通过剪枝层或利用多任务设置来降低整体延迟（Rücklé et al., 2020；Pfeiffer et al., 2021），但没有直接的办法绕过适配器层中的额外计算。
这看起来不是问题，因为适配器层的设计初衷就是参数很少（有时不到原模型的 1%），瓶颈维度小，能增加的 FLOPs 有限。
然而，大型神经网络依赖硬件并行来保持低延迟，而适配器层必须被串行处理。
在批大小通常小至一的在线推理场景中，这就产生了差异。
在一个没有模型并行的通用场景中，例如在单块 GPU 上对 GPT-2（Radford et al., b）medium 做推理，我们看到使用适配器时延迟明显增加，即使瓶颈维度非常小（表 1）。

| 批大小 | 32 | 16 | 1 |
| --- | --- | --- | --- |
| 序列长度 | 512 | 256 | 128 |
| $\|\Theta\|$ | 0.5M | 11M | 11M |
| Fine-Tune/LoRA | 1449.4±0.8 | 338.0±0.6 | 19.8±2.7 |
| Adapter^L | 1482.0±1.0（+2.2%） | 354.8±0.5（+5.0%） | 23.9±2.1（+20.7%） |
| Adapter^H | 1492.2±1.0（+3.0%） | 366.3±0.5（+8.4%） | 25.8±2.2（+30.3%） |

表 1：GPT-2 medium 单次前向传播的推理延迟，以毫秒计，取 100 次试验的平均值。我们使用 NVIDIA Quadro RTX8000。「$\|\Theta\|$」表示适配器层中的可训练参数数量。Adapter^L 和 Adapter^H 是适配器微调的两个变体，我们在 5.1 节中描述。在在线、短序列长度场景中，适配器层引入的推理延迟可能相当显著。完整研究见附录 B。

当我们需要像 Shoeybi et al.（2020）；Lepikhin et al.（2020）那样对模型做分片时，问题会变得更糟，因为额外的深度需要更多同步 GPU 操作（如 AllReduce 和 Broadcast），除非我们把适配器参数冗余存储许多次。

#### 直接优化提示词很困难

另一个方向以前缀微调（prefix tuning）（Li & Liang, 2021）为代表，面临不同的挑战。
我们观察到前缀微调难以优化，且其性能随可训练参数数量非单调变化，这印证了原论文中的类似观察。
更根本地，为适配预留一部分序列长度必然减少可用于处理下游任务的序列长度，我们怀疑这使提示微调相比其他方法表现更差。
关于任务性能的研究留到第 5 节。

## 4 我们的方法

我们描述 LoRA 的简单设计及其实际收益。
这里阐述的原则适用于深度学习模型中的任何稠密层，不过在实验中我们只聚焦于 Transformer 语言模型中的某些权重，作为驱动性用例。

### 4.1 低秩参数化的更新矩阵

神经网络包含许多执行矩阵乘法的稠密层。
这些层中的权重矩阵通常是满秩的。
在适配特定任务时，Aghajanyan et al.（2020）表明预训练语言模型具有较低的「内在维度」，即使随机投影到更小的子空间仍能高效学习。
受此启发，我们假设适配期间对权重的更新也具有较低的「内在秩」。
对于预训练权重矩阵 $W_0\in\mathbb{R}^{d\times k}$，我们通过低秩分解 $W_0+\Delta W=W_0+BA$ 来约束其更新，其中 $B\in\mathbb{R}^{d\times r}$，$A\in\mathbb{R}^{r\times k}$，且秩 $r\ll\min(d,k)$。
训练期间，$W_0$ 被冻结、不接收梯度更新，而 $A$ 和 $B$ 包含可训练参数。
注意 $W_0$ 和 $\Delta W=BA$ 与相同的输入相乘，各自的输出向量按坐标求和。
对于 $h=W_0x$，我们修改后的前向传播为：

$$h=W_{0}x+\Delta Wx=W_{0}x+BAx\tag{3}$$

我们在图 1 中展示了这一重参数化。
我们对 $A$ 使用随机高斯初始化，对 $B$ 使用零初始化，因此 $\Delta W=BA$ 在训练开始时为零。
然后我们将 $\Delta Wx$ 按 $\frac{\alpha}{r}$ 缩放，其中 $\alpha$ 是 $r$ 的一个常数。
使用 Adam 优化时，如果我们适当缩放初始化，调节 $\alpha$ 与调节学习率大致相同。
因此，我们简单地把 $\alpha$ 设为我们尝试的第一个 $r$，不再调节它。
这一缩放有助于减少我们改变 $r$ 时重新调节超参数的需求（Yang & Hu, 2021）。

全量微调的一种推广。更一般形式的微调允许只训练预训练参数的一个子集。
LoRA 更进一步，不要求适配期间对权重矩阵的累积梯度更新是满秩的。
这意味着，当对所有权重矩阵应用 LoRA 并训练所有偏置²（脚注 2：与权重相比，它们代表的参数数量可以忽略不计。）时，通过把 LoRA 的秩 $r$ 设为预训练权重矩阵的秩，我们大致恢复全量微调的表达能力。
换句话说，随着我们增加可训练参数的数量³（脚注 3：适配困难任务时的必然要求。），训练 LoRA 大致收敛于训练原始模型，而基于适配器的方法收敛于一个 MLP，基于前缀的方法收敛于一个无法接受长输入序列的模型。

无额外推理延迟。在生产部署时，我们可以显式计算并存储 $W=W_0+BA$，然后照常推理。
注意 $W_0$ 和 $BA$ 都在 $\mathbb{R}^{d\times k}$ 中。
当我们需要切换到另一个下游任务时，可以通过减去 $BA$ 恢复 $W_0$，再加上不同的 $B'A'$，这是一个内存开销极小的快速操作。
关键在于，这从结构上保证了与微调模型相比，我们在推理期间不引入任何额外延迟。

### 4.2 将 LoRA 应用于 Transformer

原则上，我们可以对神经网络中任意子集的权重矩阵应用 LoRA，以减少可训练参数数量。
在 Transformer 架构中，自注意力模块有四个权重矩阵（$W_q$、$W_k$、$W_v$、$W_o$），MLP 模块有两个。
我们将 $W_q$（或 $W_k$、$W_v$）视为维度为 $d_{model}\times d_{model}$ 的单个矩阵，尽管输出维度通常会被切分到各个注意力头。
我们将研究限定为只对注意力权重做下游任务适配，并冻结 MLP 模块（使其在下游任务中不被训练），这既是为了简单也是为了参数效率。我们在 7.1 节中进一步研究对 Transformer 中不同类型注意力权重矩阵的适配效果。
对 MLP 层、LayerNorm 层和偏置的适配的实证研究留待未来工作。

实际收益与局限。最显著的收益来自内存和存储使用的减少。
对于用 Adam 训练的大型 Transformer，当 $r\ll d_{model}$ 时，我们可将 VRAM 使用最多减少 2/3，因为不需要为冻结参数存储优化器状态。
在 GPT-3 175B 上，我们将训练期间的 VRAM 消耗从 1.2TB 降到 350GB。
当 $r=4$ 且只适配 query 和 value 投影矩阵时，检查点大小缩减约 10,000×（从 350GB 到 35MB）⁴（脚注 4：部署时我们仍需要 350GB 的模型；但存储 100 个适配后的模型只需 350GB + 35MB × 100 ≈ 354GB，而非 100 × 350GB ≈ 35TB。）。
这使我们能够用少得多的 GPU 训练，并避免 I/O 瓶颈。
另一个收益是，部署时只需更换 LoRA 权重而非全部参数，即可低得多的成本在任务之间切换。
这使得可以在将预训练权重存放在 VRAM 中的机器上，创建许多可即时换入换出的定制模型。
我们还观察到，在 GPT-3 175B 上训练相比全量微调有 25% 的加速⁵（脚注 5：对 GPT-3 175B，全量微调的训练吞吐量为每块 V100 GPU 32.5 tokens/s；在模型并行权重分片数相同的情况下，LoRA 的吞吐量为每块 V100 GPU 43.1 tokens/s。），因为我们不需要为绝大多数参数计算梯度。

LoRA 也有其局限。
例如，如果选择把 $A$ 和 $B$ 吸收进 $W$ 以消除额外推理延迟，那么在单次前向传播中对使用不同 $A$ 和 $B$ 的不同任务的输入做批处理就不那么直接。
不过，对于延迟不关键的场景，可以选择不合并权重，并为一个批次中的样本动态选择要使用的 LoRA 模块。

## 5 实证实验

我们在 RoBERTa（Liu et al., 2019）、DeBERTa（He et al., 2021）和 GPT-2（Radford et al., b）上评估 LoRA 的下游任务性能，随后扩展到 GPT-3 175B（Brown et al., 2020）。
我们的实验覆盖从自然语言理解（NLU）到生成（NLG）的广泛任务。
具体而言，我们在 GLUE（Wang et al., 2019）基准上评估 RoBERTa 和 DeBERTa。
在 GPT-2 上我们遵循 Li & Liang（2021）的设置以便直接比较，并为 GPT-3 的大规模实验加入 WikiSQL（Zhong et al., 2017）（自然语言到 SQL 查询）和 SAMSum（Gliwa et al., 2019）（对话摘要）。
我们使用数据集的更多细节见附录 C。
所有实验均使用 NVIDIA Tesla V100。

### 5.1 基线

为了与其他基线广泛比较，我们复现先前工作使用的设置，并尽可能复用他们报告的数字。
不过，这意味着某些基线可能只出现在部分实验中。

微调（Fine-Tuning，FT）是一种常见的适配方法。
微调时，模型被初始化为预训练的权重和偏置，所有模型参数都进行梯度更新。一个简单的变体是只更新部分层而冻结其余层。
我们纳入先前工作（Li & Liang, 2021）在 GPT-2 上报告的一个这样的基线，即只适配最后两层（**FT**^**Top2**）。

仅偏置（Bias-only）或 BitFit 是只训练偏置向量、冻结其余一切的基线。
同期，该基线也由 BitFit（Zaken et al., 2021）研究过。

前缀嵌入微调（Prefix-embedding tuning，PreEmbed）在输入 token 中插入特殊 token。
这些特殊 token 拥有可训练的词嵌入，且通常不在模型词表中。
此类 token 放置在哪里会影响性能。
我们关注「prefixing」（将此类 token 前置到提示）和「infixing」（附加到提示之后）；两者都在 Li & Liang（2021）中讨论过。
我们用 $l_p$（相应地 $l_i$）表示前缀（相应地中缀）token 的数量。
可训练参数数量为 $|\Theta|=d_{model}\times(l_{p}+l_{i})$。

前缀层微调（Prefix-layer tuning，PreLayer）是前缀嵌入微调的扩展。
不只是为某些特殊 token 学习词嵌入（或等价地，嵌入层之后的激活），而是学习每个 Transformer 层之后的激活。
来自前面各层计算的激活被直接替换为可训练的激活。
可训练参数数量为 $|\Theta|=L\times d_{model}\times(l_{p}+l_{i})$，其中 $L$ 是 Transformer 层数。

Houlsby et al.（2019）提出的适配器微调（Adapter tuning）在自注意力模块（和 MLP 模块）与后续残差连接之间插入适配器层。
一个适配器层中有两个带偏置的全连接层，中间有一个非线性。
我们称这一原始设计为 **Adapter**^**H**。
最近，Lin et al.（2020）提出一种更高效的设计，适配器层只应用于 MLP 模块之后且在一个 LayerNorm 之后。
我们称之为 **Adapter**^**L**。
这与 Pfeiffer et al.（2021）提出的另一种设计非常相似，我们称之为 **Adapter**^**P**。
我们还纳入另一个叫 AdapterDrop（Rücklé et al., 2020）的基线，它丢弃一些适配器层以获得更高效率（**Adapter**^**D**）。
我们尽可能引用先前工作的数字，以最大化可比较的基线数量；这些在第一列中带星号（*）的行中。
在所有情况下，我们有 $|\Theta|=\hat{L}_{Adpt}\times(2\times d_{model}\times r+r+d_{model})+2\times\hat{L}_{LN}\times d_{model}$，其中 $\hat{L}_{Adpt}$ 是适配器层数，$\hat{L}_{LN}$ 是可训练 LayerNorm 的数量（例如在 **Adapter**^L 中）。

LoRA 在现有权重矩阵旁并行地添加可训练的秩分解矩阵对。
如 4.2 节所述，为简单起见我们在大多数实验中只对 $W_q$ 和 $W_v$ 应用 LoRA。
可训练参数数量由秩 $r$ 和原始权重的形状决定：$|\Theta|=2\times\hat{L}_{LoRA}\times d_{model}\times r$，其中 $\hat{L}_{LoRA}$ 是我们应用 LoRA 的权重矩阵数量。

### 5.2 RoBERTa base/large

| 模型与方法 | 可训练参数量 | MNLI | SST-2 | MRPC | CoLA | QNLI | QQP | RTE | STS-B | 平均 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RoB_base（FT）* | 125.0M | 87.6 | 94.8 | 90.2 | 63.6 | 92.8 | 91.9 | 78.7 | 91.2 | 86.4 |
| RoB_base（BitFit）* | 0.1M | 84.7 | 93.7 | 92.7 | 62.0 | 91.8 | 84.0 | 81.5 | 90.8 | 85.2 |
| RoB_base（Adpt^D）* | 0.3M | 87.1±.0 | 94.2±.1 | 88.5±1.1 | 60.8±.4 | 93.1±.1 | 90.2±.0 | 71.5±2.7 | 89.7±.3 | 84.4 |
| RoB_base（Adpt^D）* | 0.9M | 87.3±.1 | 94.7±.3 | 88.4±.1 | 62.6±.9 | 93.0±.2 | 90.6±.0 | 75.9±2.2 | 90.3±.1 | 85.4 |
| RoB_base（LoRA） | 0.3M | 87.5±.3 | 95.1±.2 | 89.7±.7 | 63.4±1.2 | 93.3±.3 | 90.8±.1 | 86.6±.7 | 91.5±.2 | 87.2 |
| RoB_large（FT）* | 355.0M | 90.2 | 96.4 | 90.9 | 68.0 | 94.7 | 92.2 | 86.6 | 92.4 | 88.9 |
| RoB_large（LoRA） | 0.8M | 90.6±.2 | 96.2±.5 | 90.9±1.2 | 68.2±1.9 | 94.9±.3 | 91.6±.1 | 87.4±2.5 | 92.6±.2 | 89.0 |
| RoB_large（Adpt^P）† | 3.0M | 90.2±.3 | 96.1±.3 | 90.2±.7 | 68.3±1.0 | 94.8±.2 | 91.9±.1 | 83.8±2.9 | 92.1±.7 | 88.4 |
| RoB_large（Adpt^P）† | 0.8M | 90.5±.3 | 96.6±.2 | 89.7±1.2 | 67.8±2.5 | 94.8±.3 | 91.7±.2 | 80.1±2.9 | 91.9±.4 | 87.9 |
| RoB_large（Adpt^H）† | 6.0M | 89.9±.5 | 96.2±.3 | 88.7±2.9 | 66.5±4.4 | 94.7±.2 | 92.1±.1 | 83.4±1.1 | 91.0±1.7 | 87.8 |
| RoB_large（Adpt^H）† | 0.8M | 90.3±.3 | 96.3±.5 | 87.7±1.7 | 66.3±2.0 | 94.7±.2 | 91.5±.1 | 72.9±2.9 | 91.5±.5 | 86.4 |
| RoB_large（LoRA）† | 0.8M | 90.6±.2 | 96.2±.5 | 90.2±1.0 | 68.2±1.9 | 94.8±.3 | 91.6±.2 | 85.2±1.1 | 92.3±.5 | 88.6 |
| DeB_XXL（FT）* | 1500.0M | 91.8 | 97.2 | 92.0 | 72.0 | 96.0 | 92.7 | 93.9 | 92.9 | 91.1 |
| DeB_XXL（LoRA） | 4.7M | 91.9±.2 | 96.9±.2 | 92.6±.6 | 72.4±1.1 | 96.0±.1 | 92.9±.1 | 94.9±.4 | 93.0±.2 | 91.3 |

表 2：RoBERTa_base、RoBERTa_large 和 DeBERTa_XXL 采用不同适配方法在 GLUE 基准上的表现。我们报告 MNLI 的总体（matched 与 mismatched）准确率、CoLA 的 Matthew 相关系数、STS-B 的 Pearson 相关系数，以及其他任务的准确率。所有指标越高越好。* 表示先前工作发表的数字。† 表示为公平比较而按照与 Houlsby et al.（2019）类似的设置进行的运行。

RoBERTa（Liu et al., 2019）优化了最初在 BERT（Devlin et al., 2019a）中提出的预训练配方，在不引入更多可训练参数的情况下提升了后者的任务性能。
尽管近年来 RoBERTa 在 GLUE 基准（Wang et al., 2019）等 NLP 榜单上已被大得多的模型超越，但就其规模而言，它仍是从业者中一个有竞争力且受欢迎的预训练模型。
我们从 HuggingFace Transformers 库（Wolf et al., 2020）获取预训练的 RoBERTa base（125M）和 RoBERTa large（355M），并评估不同高效适配方法在 GLUE 基准任务上的表现。
我们还根据其设置复现了 Houlsby et al.（2019）和 Pfeiffer et al.（2021）。
为确保公平比较，在与适配器比较时，我们对 LoRA 的评估方式做了两处关键改动。
第一，所有任务使用相同的批大小，并使用 128 的序列长度以匹配适配器基线。
第二，对 MRPC、RTE 和 STS-B，我们将模型初始化为预训练模型，而不是像微调基线那样使用已适配到 MNLI 的模型。
遵循 Houlsby et al.（2019）这一更受限设置的运行以 † 标注。
结果展示在表 2（前三部分）。
所用超参数的细节见 D.1 节。

### 5.3 DeBERTa XXL

DeBERTa（He et al., 2021）是 BERT 的一个较新变体，在更大的规模上训练，在 GLUE（Wang et al., 2019）和 SuperGLUE（Wang et al., 2020）等基准上极具竞争力。
我们评估 LoRA 能否在 GLUE 上追平全量微调的 DeBERTa XXL（1.5B）的性能。
结果展示在表 2（底部部分）。
所用超参数的细节见 D.2 节。

### 5.4 GPT-2 medium/large

在展示 LoRA 可以成为 NLU 上全量微调的有力替代之后，我们希望回答 LoRA 在 NLG 模型（如 GPT-2 medium 和 large，Radford et al., b）上是否依然占优。
为便于直接比较，我们使设置尽可能接近 Li & Liang（2021）。
由于篇幅限制，本节只展示我们在 E2E NLG Challenge 上的结果（表 3）。
WebNLG（Gardent et al., 2017）和 DART（Nan et al., 2020）上的结果见 F.1 节。
我们在 D.3 节列出所用超参数清单。

| 模型与方法 | 可训练参数量 | BLEU | NIST | MET | ROUGE-L | CIDEr |
| --- | --- | --- | --- | --- | --- | --- |
| GPT-2 M（FT）* | 354.92M | 68.2 | 8.62 | 46.2 | 71.0 | 2.47 |
| GPT-2 M（Adapter^L）* | 0.37M | 66.3 | 8.41 | 45.0 | 69.8 | 2.40 |
| GPT-2 M（Adapter^L）* | 11.09M | 68.9 | 8.71 | 46.1 | 71.3 | 2.47 |
| GPT-2 M（Adapter^H） | 11.09M | 67.3±.6 | 8.50±.07 | 46.0±.2 | 70.7±.2 | 2.44±.01 |
| GPT-2 M（FT^Top2）* | 25.19M | 68.1 | 8.59 | 46.0 | 70.8 | 2.41 |
| GPT-2 M（PreLayer）* | 0.35M | 69.7 | 8.81 | 46.1 | 71.4 | 2.49 |
| GPT-2 M（LoRA） | 0.35M | 70.4±.1 | 8.85±.02 | 46.8±.2 | 71.8±.1 | 2.53±.02 |
| GPT-2 L（FT）* | 774.03M | 68.5 | 8.78 | 46.0 | 69.9 | 2.45 |
| GPT-2 L（Adapter^L） | 0.88M | 69.1±.1 | 8.68±.03 | 46.3±.0 | 71.4±.2 | 2.49±.0 |
| GPT-2 L（Adapter^L） | 23.00M | 68.9±.3 | 8.70±.04 | 46.1±.1 | 71.3±.2 | 2.45±.02 |
| GPT-2 L（PreLayer）* | 0.77M | 70.3 | 8.85 | 46.2 | 71.7 | 2.47 |
| GPT-2 L（LoRA） | 0.77M | 70.4±.1 | 8.89±.02 | 46.8±.2 | 72.0±.2 | 2.47±.02 |

表 3：GPT-2 medium（M）和 large（L）采用不同适配方法在 E2E NLG Challenge 上的表现。所有指标越高越好。LoRA 以相当或更少的可训练参数胜过若干基线。我们自己运行的实验给出置信区间。* 表示先前工作发表的数字。

| 模型与方法 | 可训练参数量 | WikiSQL 准确率（%） | MNLI-m 准确率（%） | SAMSum R1/R2/RL |
| --- | --- | --- | --- | --- |
| GPT-3（FT） | 175,255.8M | 73.8 | 89.5 | 52.0/28.0/44.5 |
| GPT-3（BitFit） | 14.2M | 71.3 | 91.0 | 51.3/27.4/43.5 |
| GPT-3（PreEmbed） | 3.2M | 63.1 | 88.6 | 48.3/24.2/40.5 |
| GPT-3（PreLayer） | 20.2M | 70.1 | 89.5 | 50.8/27.3/43.5 |
| GPT-3（Adapter^H） | 7.1M | 71.9 | 89.8 | 53.0/28.9/44.8 |
| GPT-3（Adapter^H） | 40.1M | 73.2 | 91.5 | 53.2/29.0/45.1 |
| GPT-3（LoRA） | 4.7M | 73.4 | 91.7 | 53.8/29.8/45.9 |
| GPT-3（LoRA） | 37.7M | 74.0 | 91.6 | 53.4/29.2/45.1 |

表 4：不同适配方法在 GPT-3 175B 上的表现。我们报告 WikiSQL 上的逻辑形式验证准确率、MultiNLI-matched 的验证准确率，以及 SAMSum 上的 Rouge-1/2/L。LoRA 表现优于先前方法，包括全量微调。WikiSQL 结果的波动约为 ±0.5%，MNLI-m 约为 ±0.1%，SAMSum 三项指标约为 ±0.2/±0.2/±0.1。

### 5.5 扩展到 GPT-3 175B

作为对 LoRA 的最终压力测试，我们扩展到拥有 1750 亿参数的 GPT-3。
由于训练成本高昂，我们只报告给定任务在随机种子上的典型标准差，而非为每个条目都提供。
所用超参数的细节见 D.4 节。

如表 4 所示，LoRA 在全部三个数据集上追平或超越微调基线。
注意，并非所有方法都随可训练参数增多而单调受益，如图 2 所示。
我们观察到，当为前缀嵌入微调使用超过 256 个特殊 token、或为前缀层微调使用超过 32 个特殊 token 时，性能显著下降。
这与 Li & Liang（2021）中的类似观察一致。
尽管对这一现象的深入探究超出本工作范围，我们怀疑更多的特殊 token 使输入分布进一步偏离预训练数据分布。
另外，我们在 F.3 节研究不同适配方法在低数据量情况下的表现。

图 2：GPT-3 175B 在 WikiSQL 和 MNLI-matched 上，若干适配方法的验证准确率与可训练参数数量的关系。LoRA 展现出更好的可扩展性和任务性能。所绘数据点的更多细节见 F.2 节。

## 6 相关工作

Transformer 语言模型。Transformer（Vaswani et al., 2017）是一种大量使用自注意力的序列到序列架构。
Radford et al.（a）通过使用一叠 Transformer 解码器将其应用于自回归语言建模。
此后，基于 Transformer 的语言模型主导了 NLP，在许多任务上取得最优表现。
随着 BERT（Devlin et al., 2019b）和 GPT-2（Radford et al., b）——两者都是在大量文本上训练的大型 Transformer 语言模型——出现了新范式：在通用领域数据预训练之后再在任务专属数据上微调，相比直接在任务专属数据上训练带来显著的性能提升。
训练更大的 Transformer 通常带来更好的性能，仍是一个活跃的研究方向。
GPT-3（Brown et al., 2020）是迄今为止训练的最大单体 Transformer 语言模型，拥有 1750 亿参数。

提示工程与微调。虽然 GPT-3 175B 仅凭少量额外训练样本即可调整其行为，但结果严重依赖于输入提示（Brown et al., 2020）。
这就催生了一门通过组合和格式化提示来最大化模型在目标任务上表现的实证艺术，被称为提示工程（prompt engineering）或提示破解（prompt hacking）。
微调将一个在通用领域预训练的模型重新训练到特定任务（Devlin et al., 2019b；Radford et al., a）。
其变体包括只学习参数的一个子集（Devlin et al., 2019b；Collobert & Weston, 2008），但从业者往往重新训练全部参数以最大化下游性能。
然而，GPT-3 175B 的庞大体积使其难以按常规方式微调：它产生的检查点巨大，且硬件门槛高（其内存占用与预训练相同）。

参数高效的适配。许多人提出在神经网络现有层之间插入适配器层（Houlsby et al., 2019；Rebuffi et al., 2017；Lin et al., 2020）。
我们的方法使用类似的瓶颈结构，对权重更新施加低秩约束。
关键的功能差异在于，我们学到的权重可以在推理时与主权重合并，因而不引入任何延迟，而适配器层做不到这一点（第 3 节）。
适配器的一个同期扩展是 compacter（Mahabadi et al., 2021），它本质上是用 Kronecker 乘积和某种预定的权重共享方案来参数化适配器层。
类似地，将 LoRA 与其他基于张量积的方法结合可能会提升其参数效率，我们将其留作未来工作。
最近，许多人提出优化输入词嵌入来替代微调，类似于提示工程的连续、可微泛化（Li & Liang, 2021；Lester et al., 2021；Hambardzumyan et al., 2020；Liu et al., 2021）。
我们在实验部分纳入了与 Li & Liang（2021）的比较。
然而，这条工作路线只能通过在提示中使用更多特殊 token 来扩展，当学习位置嵌入时，这些 token 会占用任务 token 的可用序列长度。

深度学习中的低秩结构。低秩结构在机器学习中非常常见。
许多机器学习问题具有某种内在低秩结构（Li et al., 2016；Cai et al., 2010；Li et al., 2018b；Grasedyck et al., 2013）。
此外，众所周知，对许多深度学习任务，尤其是使用严重过参数化神经网络的任务，训练后的神经网络会享有低秩性质（Oymak et al., 2019）。
一些先前工作甚至在训练原始神经网络时显式施加低秩约束（Sainath et al., 2013；Povey et al., 2018；Zhang et al., 2014；Jaderberg et al., 2014；Zhao et al., 2016；Khodak et al., 2021；Denil et al., 2014）；然而，据我们所知，这些工作都没有考虑对冻结模型的低秩更新以*适配下游任务*。
在理论文献中，已知当底层概念类具有某种低秩结构时，神经网络优于其他经典学习方法，包括相应的（有限宽度）神经正切核（Allen-Zhu et al., 2019；Li & Liang, 2018）（Ghorbani et al., 2020；Allen-Zhu & Li, 2019；Allen-Zhu & Li, 2020a）。
Allen-Zhu & Li（2020b）的另一理论结果表明，低秩适配可能对对抗训练有用。
总之，我们相信文献为我们提出的低秩适配更新提供了充分的动机。

## 7 理解低秩更新

鉴于 LoRA 的实证优势，我们希望进一步解释从下游任务中学到的低秩适配的性质。
注意，低秩结构不仅降低了硬件门槛（使我们能并行运行多个实验），还提供了更新权重与预训练权重如何相关的更好可解释性。
我们将研究聚焦于 GPT-3 175B，在这里我们在不影响任务性能的情况下实现了可训练参数的最大缩减（最多 10,000×）。

我们进行一系列实证研究来回答以下问题：
1) 给定参数预算约束，预训练 Transformer 中*哪些权重矩阵子集*应该被适配以最大化下游性能？
2) 「最优」适配矩阵 $\Delta W$ *真的秩亏吗*？如果是，实践中用多大的秩比较好？
3) $\Delta W$ 与 $W$ 之间有什么联系？$\Delta W$ 与 $W$ 高度相关吗？$\Delta W$ 相比 $W$ 有多大？

我们相信，对问题 (2) 和 (3) 的回答能揭示将预训练语言模型用于下游任务的基本原理，这是 NLP 中的关键议题。

### 7.1 应该对 Transformer 中的哪些权重矩阵应用 LoRA？

给定有限的参数预算，应该用 LoRA 适配哪些类型的权重才能在下游任务上取得最佳性能？
如 4.2 节所述，我们只考虑自注意力模块中的权重矩阵。
我们在 GPT-3 175B 上设定 18M 的参数预算（以 FP16 存储约 35MB），这对应于对全部 96 层、若适配一种类型的注意力权重则 $r=8$，若适配两种类型则 $r=4$。
结果展示在表 5 中。

| 可训练参数量 = 18M | | | | | | |
| --- | --- | --- | --- | --- | --- | --- |
| 权重类型 | $W_q$ | $W_k$ | $W_v$ | $W_o$ | $W_q,W_k$ | $W_q,W_v$ | $W_q,W_k,W_v,W_o$ |
| 秩 $r$ | 8 | 8 | 8 | 8 | 4 | 4 | 2 |
| WikiSQL（±0.5%） | 70.4 | 70.0 | 73.0 | 73.2 | 71.4 | 73.7 | 73.7 |
| MultiNLI（±0.1%） | 91.0 | 90.8 | 91.0 | 91.3 | 91.3 | 91.3 | 91.7 |

表 5：在可训练参数数量相同的前提下，对 GPT-3 中不同类型注意力权重应用 LoRA 后在 WikiSQL 和 MultiNLI 上的验证准确率。同时适配 $W_q$ 和 $W_v$ 总体表现最佳。我们发现给定数据集上随机种子间的标准差是一致的，报告在第一列中。

注意，把所有参数都放在 $\Delta W_q$ 或 $\Delta W_k$ 中会导致明显更低的性能，而同时适配 $W_q$ 和 $W_v$ 取得最佳结果。
这表明，即使秩为四也足以在 $\Delta W$ 中捕获足够信息，因而适配更多权重矩阵优于以更大秩适配单一类型的权重。

### 7.2 LoRA 的最优秩 $r$ 是多少？

我们将注意力转向秩 $r$ 对模型性能的影响。
我们适配 $\{W_q,W_v\}$、$\{W_q,W_k,W_v,W_o\}$ 和仅 $W_q$ 进行比较。

| | 权重类型 | r=1 | r=2 | r=4 | r=8 | r=64 |
| --- | --- | --- | --- | --- | --- | --- |
| WikiSQL（±0.5%） | $W_q$ | 68.8 | 69.6 | 70.5 | 70.4 | 70.0 |
| | $W_q,W_v$ | 73.4 | 73.3 | 73.7 | 73.8 | 73.5 |
| | $W_q,W_k,W_v,W_o$ | 74.1 | 73.7 | 74.0 | 74.0 | 73.9 |
| MultiNLI（±0.1%） | $W_q$ | 90.7 | 90.9 | 91.1 | 90.7 | 90.7 |
| | $W_q,W_v$ | 91.3 | 91.4 | 91.3 | 91.6 | 91.4 |
| | $W_q,W_k,W_v,W_o$ | 91.2 | 91.7 | 91.7 | 91.5 | 91.4 |

表 6：不同秩 $r$ 下在 WikiSQL 和 MultiNLI 上的验证准确率。令我们惊讶的是，在这些数据集上，同时适配 $W_q$ 和 $W_v$ 时小至一的秩就足够了，而单独训练 $W_q$ 需要更大的 $r$。我们在 H.2 节对 GPT-2 进行了类似实验。

表 6 表明，令人惊讶的是，LoRA 在非常小的 $r$ 下就已具有竞争力（$\{W_q,W_v\}$ 比仅 $W_q$ 更明显）。
这表明更新矩阵 $\Delta W$ 可能具有非常小的「内在秩」。⁶（脚注 6：不过，我们并不期望小 $r$ 对每个任务或数据集都有效。试考虑如下思想实验：如果下游任务使用的语言与预训练不同，重新训练整个模型（类似 $r=d_{model}$ 的 LoRA）当然会胜过小 $r$ 的 LoRA。）
为进一步支持这一发现，我们检查了不同 $r$ 选择和不同随机种子所学子空间的重叠情况。我们论证，增大 $r$ 并不会覆盖一个更有意义的子空间，这表明低秩适配矩阵已经足够。

不同 $r$ 之间的子空间相似度。给定 $A_{r=8}$ 和 $A_{r=64}$——用*同一个预训练模型*分别以秩 $r=8$ 和 64 学习到的适配矩阵——我们执行奇异值分解，得到右奇异酉矩阵 $U_{A_{r=8}}$ 和 $U_{A_{r=64}}$。⁷（脚注 7：注意，可以用 $B$ 和左奇异酉矩阵进行类似分析——我们的实验坚持用 $A$。）
我们希望回答：$U_{A_{r=8}}$ 中前 $i$ 个奇异向量张成的子空间（$1\leq i\leq 8$）有多少包含在 $U_{A_{r=64}}$ 中前 $j$ 个奇异向量张成的子空间（$1\leq j\leq 64$）中？
我们用基于 Grassmann 距离的归一化子空间相似度来度量这一数量（更正式的讨论见附录 G）：

$$\phi(A_{r=8},A_{r=64},i,j)=\frac{||U_{A_{r=8}}^{i\top}U_{A_{r=64}}^{j}||_{F}^{2}}{\min(i,j)}\in[0,1]\tag{4}$$

其中 $U_{A_{r=8}}^{i}$ 表示 $U_{A_{r=8}}$ 中对应前 $i$ 个奇异向量的列。

$\phi(\cdot)$ 的取值范围是 $[0,1]$，其中 1 表示子空间完全重叠，0 表示完全分离。
$\phi$ 随 $i$ 和 $j$ 变化的情况见图 3。
由于篇幅限制，我们只看第 48 层（共 96 层），但结论对其他层同样成立，如 H.1 节所示。

![图 3](2106.09685v2/qv8_qv64.png)

图 3：$A_{r=8}$ 与 $A_{r=64}$ 的列向量之间的子空间相似度，同时给出 $\Delta W_q$ 和 $\Delta W_v$。第三和第四幅图放大了前两幅图中左下三角区域。r=8 中的顶部方向包含在 r=64 中，反之亦然。

我们从图 3 中得出一个*重要观察*。

与顶部奇异向量对应的方向在 $A_{r=8}$ 与 $A_{r=64}$ 之间显著重叠，而其他方向则不然。具体来说，$A_{r=8}$ 的 $\Delta W_v$（相应地 $\Delta W_q$）与 $A_{r=64}$ 的 $\Delta W_v$（相应地 $\Delta W_q$）共享一个维度为 1、归一化相似度 >0.5 的子空间，这解释了为什么在 GPT-3 的下游任务中 $r=1$ 表现相当好。

由于 $A_{r=8}$ 和 $A_{r=64}$ 都是用同一个预训练模型学习得到的，图 3 表明 $A_{r=8}$ 和 $A_{r=64}$ 的顶部奇异向量方向是最有用的，而其他方向可能主要包含训练期间累积的随机噪声。
因此，适配矩阵确实可以具有非常低的秩。

![图 4](2106.09685v2/UA_across_random_seeds.png)

图 4：左图与中图：来自两个随机种子、$A_{r=64}$ 列向量之间的归一化子空间相似度，同时给出第 48 层的 $\Delta W_q$ 和 $\Delta W_v$。右图：两个随机高斯矩阵列向量之间的相同热图。其他层见 H.1 节。

不同随机种子之间的子空间相似度。我们通过绘制两次随机种子、$r=64$ 运行之间的归一化子空间相似度进一步确认这一点，见图 4。
$\Delta W_q$ 看起来比 $\Delta W_v$ 具有更高的「内在秩」，因为两次运行为 $\Delta W_q$ 学到了更多共同的奇异值方向，这与我们在表 6 中的实证观察一致。
作为比较，我们还绘制了两个随机高斯矩阵，它们彼此之间不共享任何共同的奇异值方向。

### 7.3 适配矩阵 $\Delta W$ 与 $W$ 相比如何？

我们进一步研究 $\Delta W$ 与 $W$ 之间的关系。
特别地，$\Delta W$ 与 $W$ 高度相关吗？（或者从数学上说，$\Delta W$ 是否主要包含在 $W$ 的顶部奇异方向中？）另外，$\Delta W$ 相比其在 $W$ 中对应的方向有多「大」？
这可以为适配预训练语言模型的底层机制提供线索。

为回答这些问题，我们通过计算 $U^{\top}WV^{\top}$ 将 $W$ 投影到 $\Delta W$ 的 $r$ 维子空间上，其中 $U$/$V$ 是 $\Delta W$ 的左/右奇异向量矩阵。然后，我们比较 $\|U^{\top}WV^{\top}\|_{F}$ 与 $\|W\|_{F}$ 的 Frobenius 范数。
作为比较，我们还将 $U,V$ 替换为 $W$ 的前 $r$ 个奇异向量或一个随机矩阵，计算 $\|U^{\top}WV^{\top}\|_{F}$。

| | r=4 | | | r=64 | | |
| --- | --- | --- | --- | --- | --- | --- |
| | $\Delta W_q$ | $W_q$ | Random | $\Delta W_q$ | $W_q$ | Random |
| $\|U^{\top}W_qV^{\top}\|_F=$ | 0.32 | 21.67 | 0.02 | 1.90 | 37.71 | 0.33 |
| $\|W_q\|_F=61.95$ | $\|\Delta W_q\|_F=6.91$ | | | $\|\Delta W_q\|_F=3.57$ | | |

表 7：$U^{\top}W_qV^{\top}$ 的 Frobenius 范数，其中 $U$ 和 $V$ 是以下三者之一的左/右前 $r$ 个奇异向量方向：(1) $\Delta W_q$，(2) $W_q$，或 (3) 一个随机矩阵。权重矩阵取自 GPT-3 的第 48 层。

我们从表 7 中得出*若干结论*。
第一，与随机矩阵相比，$\Delta W$ 与 $W$ 有更强的相关性，表明 $\Delta W$ 放大了 $W$ 中已经存在的某些特征。
第二，$\Delta W$ 不是重复 $W$ 的顶部奇异方向，而只是*放大了 $W$ 中未被强调的方向*。
第三，放大因子相当大：r=4 时 $21.5\approx 6.91/0.32$。
为何 r=64 的放大因子较小，见 H.4 节。
我们还在 H.3 节提供了随着纳入 $W_q$ 的更多顶部奇异方向、相关性如何变化的可视化。
这表明，低秩适配矩阵可能*放大了那些在通用预训练模型中已学到但未被强调的、对特定下游任务重要的特征*。

## 8 结论与未来工作

微调超大语言模型在硬件需求以及为不同任务托管独立实例的存储/切换成本上都极其昂贵。
我们提出 LoRA，一种既不引入推理延迟也不缩短输入序列长度、同时保持高模型质量的高效适配策略。
重要的是，它通过共享绝大部分模型参数，在作为服务部署时允许快速切换任务。
虽然我们聚焦于 Transformer 语言模型，所提出的原则普遍适用于任何含稠密层的神经网络。

未来工作有许多方向。
1) LoRA 可以与其他高效适配方法结合，可能提供正交的改进。
2) 微调或 LoRA 背后的机制还远未明晰——预训练期间学到的特征是如何被转化为在下游任务上表现出色的？
我们相信，相比全量微调，LoRA 使回答这一问题更可行。
3) 我们主要依赖启发式方法来选择应用 LoRA 的权重矩阵。
有没有更有原则的做法？
4) 最后，$\Delta W$ 的秩亏表明 $W$ 本身也可能是秩亏的，这也可以成为未来工作的灵感来源。

## 参考文献

- Aghajanyan et al. (2020)

  Armen Aghajanyan, Luke Zettlemoyer, and Sonal Gupta.
  Intrinsic Dimensionality Explains the Effectiveness of
  Language Model Fine-Tuning.
  *arXiv:2012.13255 [cs]*, December 2020.
  URL <http://arxiv.org/abs/2012.13255>.
- Allen-Zhu & Li (2019)

  Zeyuan Allen-Zhu and Yuanzhi Li.
  What Can ResNet Learn Efficiently, Going Beyond Kernels?
  In *NeurIPS*, 2019.
  Full version available at <http://arxiv.org/abs/1905.10337>.
- Allen-Zhu & Li (2020a)

  Zeyuan Allen-Zhu and Yuanzhi Li.
  Backward feature correction: How deep learning performs deep
  learning.
  *arXiv preprint arXiv:2001.04413*, 2020a.
- Allen-Zhu & Li (2020b)

  Zeyuan Allen-Zhu and Yuanzhi Li.
  Feature purification: How adversarial training performs robust deep
  learning.
  *arXiv preprint arXiv:2005.10190*, 2020b.
- Allen-Zhu et al. (2019)

  Zeyuan Allen-Zhu, Yuanzhi Li, and Zhao Song.
  A convergence theory for deep learning via over-parameterization.
  In *ICML*, 2019.
  Full version available at <http://arxiv.org/abs/1811.03962>.
- Ba et al. (2016)

  Jimmy Lei Ba, Jamie Ryan Kiros, and Geoffrey E. Hinton.
  Layer normalization, 2016.
- Brown et al. (2020)

  Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan,
  Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda
  Askell, Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan,
  Rewon Child, Aditya Ramesh, Daniel M. Ziegler, Jeffrey Wu, Clemens Winter,
  Christopher Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott Gray,
  Benjamin Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford,
  Ilya Sutskever, and Dario Amodei.
  Language Models are Few-Shot Learners.
  *arXiv:2005.14165 [cs]*, July 2020.
  URL <http://arxiv.org/abs/2005.14165>.
- Cai et al. (2010)

  Jian-Feng Cai, Emmanuel J Candès, and Zuowei Shen.
  A singular value thresholding algorithm for matrix completion.
  *SIAM Journal on optimization*, 20(4):1956–1982, 2010.
- Cer et al. (2017)

  Daniel Cer, Mona Diab, Eneko Agirre, Inigo Lopez-Gazpio, and Lucia Specia.
  Semeval-2017 task 1: Semantic textual similarity multilingual and
  crosslingual focused evaluation.
  *Proceedings of the 11th International Workshop on Semantic
  Evaluation (SemEval-2017)*, 2017.
  doi: 10.18653/v1/s17-2001.
  URL <http://dx.doi.org/10.18653/v1/S17-2001>.
- Collobert & Weston (2008)

  Ronan Collobert and Jason Weston.
  A unified architecture for natural language processing: deep neural
  networks with multitask learning.
  In *Proceedings of the 25th international conference on
  Machine learning*, ICML ’08, pp. 160–167, New York, NY, USA, July
  2008. Association for Computing Machinery.
  ISBN 978-1-60558-205-4.
  doi: 10.1145/1390156.1390177.
  URL <https://doi.org/10.1145/1390156.1390177>.
- Denil et al. (2014)

  Misha Denil, Babak Shakibi, Laurent Dinh, Marc’Aurelio Ranzato, and Nando
  de Freitas.
  Predicting parameters in deep learning, 2014.
- Devlin et al. (2019a)

  Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova.
  Bert: Pre-training of deep bidirectional transformers for language
  understanding, 2019a.
- Devlin et al. (2019b)

  Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova.
  BERT: Pre-training of Deep Bidirectional Transformers for
  Language Understanding.
  *arXiv:1810.04805 [cs]*, May 2019b.
  URL <http://arxiv.org/abs/1810.04805>.
  arXiv: 1810.04805.
- Dolan & Brockett (2005)

  William B. Dolan and Chris Brockett.
  Automatically constructing a corpus of sentential paraphrases.
  In *Proceedings of the Third International Workshop on
  Paraphrasing (IWP2005)*, 2005.
  URL <https://aclanthology.org/I05-5002>.
- Gardent et al. (2017)

  Claire Gardent, Anastasia Shimorina, Shashi Narayan, and Laura
  Perez-Beltrachini.
  The webnlg challenge: Generating text from rdf data.
  In *Proceedings of the 10th International Conference on Natural
  Language Generation*, pp. 124–133, 2017.
- Ghorbani et al. (2020)

  Behrooz Ghorbani, Song Mei, Theodor Misiakiewicz, and Andrea Montanari.
  When do neural networks outperform kernel methods?
  *arXiv preprint arXiv:2006.13409*, 2020.
- Gliwa et al. (2019)

  Bogdan Gliwa, Iwona Mochol, Maciej Biesek, and Aleksander Wawer.
  Samsum corpus: A human-annotated dialogue dataset for abstractive
  summarization.
  *CoRR*, abs/1911.12237, 2019.
  URL <http://arxiv.org/abs/1911.12237>.
- Grasedyck et al. (2013)

  Lars Grasedyck, Daniel Kressner, and Christine Tobler.
  A literature survey of low-rank tensor approximation techniques.
  *GAMM-Mitteilungen*, 36(1):53–78, 2013.
- Ham & Lee (2008)

  Jihun Ham and Daniel D. Lee.
  Grassmann discriminant analysis: a unifying view on subspace-based
  learning.
  In *ICML*, pp. 376–383, 2008.
  URL <https://doi.org/10.1145/1390156.1390204>.
- Hambardzumyan et al. (2020)

  Karen Hambardzumyan, Hrant Khachatrian, and Jonathan May.
  WARP: Word-level Adversarial ReProgramming.
  *arXiv:2101.00121 [cs]*, December 2020.
  URL <http://arxiv.org/abs/2101.00121>.
  arXiv: 2101.00121.
- He et al. (2021)

  Pengcheng He, Xiaodong Liu, Jianfeng Gao, and Weizhu Chen.
  Deberta: Decoding-enhanced bert with disentangled attention, 2021.
- Houlsby et al. (2019)

  Neil Houlsby, Andrei Giurgiu, Stanislaw Jastrzebski, Bruna Morrone, Quentin
  de Laroussilhe, Andrea Gesmundo, Mona Attariyan, and Sylvain Gelly.
  Parameter-Efficient Transfer Learning for NLP.
  *arXiv:1902.00751 [cs, stat]*, June 2019.
  URL <http://arxiv.org/abs/1902.00751>.
- Jaderberg et al. (2014)

  Max Jaderberg, Andrea Vedaldi, and Andrew Zisserman.
  Speeding up convolutional neural networks with low rank expansions.
  *arXiv preprint arXiv:1405.3866*, 2014.
- Khodak et al. (2021)

  Mikhail Khodak, Neil Tenenholtz, Lester Mackey, and Nicolò Fusi.
  Initialization and regularization of factorized neural layers, 2021.
- Kingma & Ba (2017)

  Diederik P. Kingma and Jimmy Ba.
  Adam: A method for stochastic optimization, 2017.
- Lepikhin et al. (2020)

  Dmitry Lepikhin, HyoukJoong Lee, Yuanzhong Xu, Dehao Chen, Orhan Firat, Yanping
  Huang, Maxim Krikun, Noam Shazeer, and Zhifeng Chen.
  Gshard: Scaling giant models with conditional computation and
  automatic sharding, 2020.
- Lester et al. (2021)

  Brian Lester, Rami Al-Rfou, and Noah Constant.
  The Power of Scale for Parameter-Efficient Prompt Tuning.
  *arXiv:2104.08691 [cs]*, April 2021.
  URL <http://arxiv.org/abs/2104.08691>.
  arXiv: 2104.08691.
- Li et al. (2018a)

  Chunyuan Li, Heerad Farkhoor, Rosanne Liu, and Jason Yosinski.
  Measuring the Intrinsic Dimension of Objective Landscapes.
  *arXiv:1804.08838 [cs, stat]*, April 2018a.
  URL <http://arxiv.org/abs/1804.08838>.
  arXiv: 1804.08838.
- Li & Liang (2021)

  Xiang Lisa Li and Percy Liang.
  Prefix-Tuning: Optimizing Continuous Prompts for
  Generation.
  *arXiv:2101.00190 [cs]*, January 2021.
  URL <http://arxiv.org/abs/2101.00190>.
- Li & Liang (2018)

  Yuanzhi Li and Yingyu Liang.
  Learning overparameterized neural networks via stochastic gradient
  descent on structured data.
  In *Advances in Neural Information Processing Systems*, 2018.
- Li et al. (2016)

  Yuanzhi Li, Yingyu Liang, and Andrej Risteski.
  Recovery guarantee of weighted low-rank approximation via alternating
  minimization.
  In *International Conference on Machine Learning*, pp. 2358–2367. PMLR, 2016.
- Li et al. (2018b)

  Yuanzhi Li, Tengyu Ma, and Hongyang Zhang.
  Algorithmic regularization in over-parameterized matrix sensing and
  neural networks with quadratic activations.
  In *Conference On Learning Theory*, pp. 2–47. PMLR,
  2018b.
- Lin et al. (2020)

  Zhaojiang Lin, Andrea Madotto, and Pascale Fung.
  Exploring versatile generative language model via parameter-efficient
  transfer learning.
  In *Findings of the Association for Computational Linguistics:
  EMNLP 2020*, pp. 441–459, Online, November 2020. Association for
  Computational Linguistics.
  doi: 10.18653/v1/2020.findings-emnlp.41.
  URL <https://aclanthology.org/2020.findings-emnlp.41>.
- Liu et al. (2021)

  Xiao Liu, Yanan Zheng, Zhengxiao Du, Ming Ding, Yujie Qian, Zhilin Yang, and
  Jie Tang.
  GPT Understands, Too.
  *arXiv:2103.10385 [cs]*, March 2021.
  URL <http://arxiv.org/abs/2103.10385>.
  arXiv: 2103.10385.
- Liu et al. (2019)

  Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Mandar Joshi, Danqi Chen, Omer
  Levy, Mike Lewis, Luke Zettlemoyer, and Veselin Stoyanov.
  Roberta: A robustly optimized bert pretraining approach, 2019.
- Loshchilov & Hutter (2017)

  Ilya Loshchilov and Frank Hutter.
  Decoupled weight decay regularization.
  *arXiv preprint arXiv:1711.05101*, 2017.
- Loshchilov & Hutter (2019)

  Ilya Loshchilov and Frank Hutter.
  Decoupled weight decay regularization, 2019.
- Mahabadi et al. (2021)

  Rabeeh Karimi Mahabadi, James Henderson, and Sebastian Ruder.
  Compacter: Efficient low-rank hypercomplex adapter layers, 2021.
- Nan et al. (2020)

  Linyong Nan, Dragomir Radev, Rui Zhang, Amrit Rau, Abhinand Sivaprasad,
  Chiachun Hsieh, Xiangru Tang, Aadit Vyas, Neha Verma, Pranav Krishna, et al.
  Dart: Open-domain structured data record to text generation.
  *arXiv preprint arXiv:2007.02871*, 2020.
- Novikova et al. (2017)

  Jekaterina Novikova, Ondřej Dušek, and Verena Rieser.
  The e2e dataset: New challenges for end-to-end generation.
  *arXiv preprint arXiv:1706.09254*, 2017.
- Oymak et al. (2019)

  Samet Oymak, Zalan Fabian, Mingchen Li, and Mahdi Soltanolkotabi.
  Generalization guarantees for neural networks via harnessing the
  low-rank structure of the jacobian.
  *arXiv preprint arXiv:1906.05392*, 2019.
- Pfeiffer et al. (2021)

  Jonas Pfeiffer, Aishwarya Kamath, Andreas Rücklé, Kyunghyun Cho, and Iryna
  Gurevych.
  Adapterfusion: Non-destructive task composition for transfer
  learning, 2021.
- Povey et al. (2018)

  Daniel Povey, Gaofeng Cheng, Yiming Wang, Ke Li, Hainan Xu, Mahsa Yarmohammadi,
  and Sanjeev Khudanpur.
  Semi-orthogonal low-rank matrix factorization for deep neural
  networks.
  In *Interspeech*, pp. 3743–3747, 2018.
- Radford et al. (a)

  Alec Radford, Karthik Narasimhan, Tim Salimans, and Ilya Sutskever.
  Improving Language Understanding by Generative
  Pre-Training.
  pp.  12, a.
- Radford et al. (b)

  Alec Radford, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei, and Ilya
  Sutskever.
  Language Models are Unsupervised Multitask Learners.
  pp.  24, b.
- Rajpurkar et al. (2018)

  Pranav Rajpurkar, Robin Jia, and Percy Liang.
  Know what you don’t know: Unanswerable questions for squad.
  *CoRR*, abs/1806.03822, 2018.
  URL <http://arxiv.org/abs/1806.03822>.
- Rebuffi et al. (2017)

  Sylvestre-Alvise Rebuffi, Hakan Bilen, and Andrea Vedaldi.
  Learning multiple visual domains with residual adapters.
  *arXiv:1705.08045 [cs, stat]*, November 2017.
  URL <http://arxiv.org/abs/1705.08045>.
  arXiv: 1705.08045.
- Rücklé et al. (2020)

  Andreas Rücklé, Gregor Geigle, Max Glockner, Tilman Beck, Jonas Pfeiffer,
  Nils Reimers, and Iryna Gurevych.
  Adapterdrop: On the efficiency of adapters in transformers, 2020.
- Sainath et al. (2013)

  Tara N Sainath, Brian Kingsbury, Vikas Sindhwani, Ebru Arisoy, and Bhuvana
  Ramabhadran.
  Low-rank matrix factorization for deep neural network training with
  high-dimensional output targets.
  In *2013 IEEE international conference on acoustics, speech and
  signal processing*, pp. 6655–6659. IEEE, 2013.
- Shoeybi et al. (2020)

  Mohammad Shoeybi, Mostofa Patwary, Raul Puri, Patrick LeGresley, Jared Casper,
  and Bryan Catanzaro.
  Megatron-lm: Training multi-billion parameter language models using
  model parallelism, 2020.
- Socher et al. (2013)

  Richard Socher, Alex Perelygin, Jean Wu, Jason Chuang, Christopher D. Manning,
  Andrew Ng, and Christopher Potts.
  Recursive deep models for semantic compositionality over a sentiment
  treebank.
  In *Proceedings of the 2013 Conference on Empirical Methods in
  Natural Language Processing*, pp. 1631–1642, Seattle, Washington, USA,
  October 2013. Association for Computational Linguistics.
  URL <https://aclanthology.org/D13-1170>.
- Vaswani et al. (2017)

  Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones,
  Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin.
  Attention is all you need.
  In *Proceedings of the 31st International Conference on Neural
  Information Processing Systems*, pp. 6000–6010, 2017.
- Wang et al. (2019)

  Alex Wang, Amanpreet Singh, Julian Michael, Felix Hill, Omer Levy, and
  Samuel R. Bowman.
  Glue: A multi-task benchmark and analysis platform for natural
  language understanding, 2019.
- Wang et al. (2020)

  Alex Wang, Yada Pruksachatkun, Nikita Nangia, Amanpreet Singh, Julian Michael,
  Felix Hill, Omer Levy, and Samuel R. Bowman.
  Superglue: A stickier benchmark for general-purpose language
  understanding systems, 2020.
- Warstadt et al. (2018)

  Alex Warstadt, Amanpreet Singh, and Samuel R Bowman.
  Neural network acceptability judgments.
  *arXiv preprint arXiv:1805.12471*, 2018.
- Williams et al. (2018)

  Adina Williams, Nikita Nangia, and Samuel Bowman.
  A broad-coverage challenge corpus for sentence understanding through
  inference.
  In *Proceedings of the 2018 Conference of the North American
  Chapter of the Association for Computational Linguistics: Human Language
  Technologies, Volume 1 (Long Papers)*, pp. 1112–1122, New Orleans,
  Louisiana, June 2018. Association for Computational Linguistics.
  doi: 10.18653/v1/N18-1101.
  URL <https://www.aclweb.org/anthology/N18-1101>.
- Wolf et al. (2020)

  Thomas Wolf, Lysandre Debut, Victor Sanh, Julien Chaumond, Clement Delangue,
  Anthony Moi, Pierric Cistac, Tim Rault, Rémi Louf, Morgan Funtowicz, Joe
  Davison, Sam Shleifer, Patrick von Platen, Clara Ma, Yacine Jernite, Julien
  Plu, Canwen Xu, Teven Le Scao, Sylvain Gugger, Mariama Drame, Quentin Lhoest,
  and Alexander M. Rush.
  Transformers: State-of-the-art natural language processing.
  In *Proceedings of the 2020 Conference on Empirical Methods in
  Natural Language Processing: System Demonstrations*, pp. 38–45, Online,
  October 2020. Association for Computational Linguistics.
  URL <https://www.aclweb.org/anthology/2020.emnlp-demos.6>.
- Yang & Hu (2021)

  Greg Yang and Edward J. Hu.
  Feature Learning in Infinite-Width Neural Networks.
  *arXiv:2011.14522 [cond-mat]*, May 2021.
  URL <http://arxiv.org/abs/2011.14522>.
  arXiv: 2011.14522.
- Zaken et al. (2021)

  Elad Ben Zaken, Shauli Ravfogel, and Yoav Goldberg.
  Bitfit: Simple parameter-efficient fine-tuning for transformer-based
  masked language-models, 2021.
- Zhang et al. (2014)

  Yu Zhang, Ekapol Chuangsuwanich, and James Glass.
  Extracting deep neural network bottleneck features using low-rank
  matrix factorization.
  In *2014 IEEE international conference on acoustics, speech and
  signal processing (ICASSP)*, pp. 185–189. IEEE, 2014.
- Zhao et al. (2016)

  Yong Zhao, Jinyu Li, and Yifan Gong.
  Low-rank plus diagonal adaptation for deep neural networks.
  In *2016 IEEE International Conference on Acoustics, Speech and
  Signal Processing (ICASSP)*, pp. 5005–5009. IEEE, 2016.
- Zhong et al. (2017)

  Victor Zhong, Caiming Xiong, and Richard Socher.
  Seq2sql: Generating structured queries from natural language using
  reinforcement learning.
  *CoRR*, abs/1709.00103, 2017.
  URL <http://arxiv.org/abs/1709.00103>.

## 附录 A 大语言模型仍然需要参数更新

当我们只有寥寥几个训练样本时，少样本学习（即提示工程）非常有优势。
然而在实践中，对于性能敏感的应用，我们往往负担得起整理几千个或更多的训练样本。
如表 8 所示，在大数据集和小数据集上，微调相比少样本学习都大幅提升了模型性能。
我们采用 GPT-3 论文（Brown et al., 2020）中 RTE 的 GPT-3 少样本结果。
对于 MNLI-matched，我们每类使用两个示例，共六个上下文内示例。

| 方法 | MNLI-m（验证准确率/%） | RTE（验证准确率/%） |
| --- | --- | --- |
| GPT-3 少样本 | 40.6 | 69.0 |
| GPT-3 微调 | 89.5 | 85.4 |

表 8：在 GPT-3（Brown et al., 2020）上，微调显著优于少样本学习。

## 附录 B 适配器层引入的推理延迟

适配器层是以串行方式添加到预训练模型上的外部模块，而我们的提案 LoRA 可以看作以并行方式添加的外部模块。
因此，适配器层必须在基础模型之外被计算，不可避免地引入额外延迟。
不过正如 Rücklé et al.（2020）指出的，当模型批大小和/或序列长度大到足以充分利用硬件并行时，适配器层引入的延迟可以得到缓解。
我们通过在 GPT-2 medium 上类似的延迟研究确认了他们的观察，并指出在某些场景下（特别是在线推理中批大小很小时），增加的延迟可能相当显著。

我们在 NVIDIA Quadro RTX8000 上通过取 100 次试验的平均值测量单次前向传播的延迟。
我们改变输入批大小、序列长度和适配器瓶颈维度 $r$。
我们测试两种适配器设计：Houlsby et al.（2019）的原始设计（我们称之为 **Adapter**^H）和 Lin et al.（2020）的更高效变体（我们称之为 **Adapter**^L）。
设计的更多细节见 5.1 节。
我们在图 5 中绘制了相对无适配器基线的百分比减速。

![图 5](2106.09685v2/latency.png)

图 5：相对无适配器（r=0）基线的推理延迟百分比减速。第一行为 **Adapter**^H 的结果，第二行为 **Adapter**^L。更大的批大小和序列长度有助于缓解延迟，但在在线、短序列长度场景中减速可高达 30% 以上。我们调整了颜色映射以提高可见度。

## 附录 C 数据集详情

GLUE 基准
是一个覆盖面广泛的自然语言理解任务集合。
它包括 MNLI（推理，Williams et al., 2018）、SST-2（情感分析，Socher et al., 2013）、MRPC（复述检测，Dolan & Brockett, 2005）、CoLA（语言学可接受性，Warstadt et al., 2018）、QNLI（推理，Rajpurkar et al., 2018）、QQP⁸（脚注 8：https://quoradata.quora.com/First-Quora-Dataset-Release-Question-Pairs ）（问答）、RTE（推理）和 STS-B（文本相似度，Cer et al., 2017）。
其广泛覆盖使 GLUE 基准成为评估 RoBERTa、DeBERTa 等 NLU 模型的标准指标。
各个数据集在不同的宽松许可证下发布。

WikiSQL
由 Zhong et al.（2017）提出，包含 56,355/8,421 个训练/验证样本。
任务是从自然语言问题和表结构生成 SQL 查询。
我们将上下文编码为 $x=\{\text{table schema},\text{query}\}$，目标编码为 $y=\{\text{SQL}\}$。
该数据集在 BSD 3-Clause 许可证下发布。

SAMSum
由 Gliwa et al.（2019）提出，包含 14,732/819 个训练/测试样本。
它由两人之间的情景聊天对话以及语言学家撰写的相应抽象式摘要组成。
我们将上下文编码为以 "\n" 拼接的话语后跟一个 "\n\n"，目标编码为 $y=\{\text{summary}\}$。
该数据集在非商业许可证 Creative Commons BY-NC-ND 4.0 下发布。

E2E NLG Challenge
最早由 Novikova et al.（2017）提出，作为训练端到端、数据驱动的自然语言生成系统的数据集，常用于数据到文本评估。E2E 数据集包含来自餐饮领域的大约 42,000 个训练、4,600 个验证和 4,600 个测试样本。每张作为输入的源表可以有多个参考。每个输入样本 $(x,y)$ 由一列槽-值对以及相应的自然语言参考文本组成。
该数据集在 Creative Commons BY-NC-SA 4.0 下发布。

DART
是 Nan et al.（2020）描述的开放域数据到文本数据集。
DART 的输入被组织为 ENTITY — RELATION — ENTITY 三元组序列。
总共有约 82K 个样本，与 E2E 相比，DART 是一个规模显著更大、更复杂的数据到文本任务。
该数据集在 MIT 许可证下发布。

WebNLG
是另一个常用的数据到文本评估数据集（Gardent et al., 2017）。总共有约 22K 个样本，WebNLG 包含 14 个不同的类别，其中九个在训练中见过。由于 14 个类别中有五个在训练中未见过、但出现在测试集中，评估通常按「见过」类别（S）、「未见」类别（U）和「全部」（A）分别进行。每个输入样本由一列 SUBJECT — PROPERTY — OBJECT 三元组表示。
该数据集在 Creative Commons BY-NC-SA 4.0 下发布。

## 附录 D 实验所用超参数

### D.1 RoBERTa

我们使用 AdamW 和线性学习率衰减日程训练。
我们为 LoRA 扫掠学习率、训练轮数和批大小。
遵循 Liu et al.（2019），在适配 MRPC、RTE 和 STS-B 时，我们将 LoRA 模块初始化为我们最佳的 MNLI 检查点，而非通常的初始化；预训练模型在所有任务中保持冻结。
我们报告 5 个随机种子上的中位数；每次运行的结果取最佳轮次。
为了与 Houlsby et al.（2019）和 Pfeiffer et al.（2021）的设置公平比较，我们将模型序列长度限制为 128，并对所有任务使用固定批大小。
重要的是，在适配 MRPC、RTE 和 STS-B 时，我们从预训练的 RoBERTa large 模型出发，而不是已适配到 MNLI 的模型。
带有这一受限设置的运行以 † 标注。
我们运行所用的超参数见表 9。

| 方法与超参数 | MNLI | SST-2 | MRPC | CoLA | QNLI | QQP | RTE | STS-B |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 优化器 | AdamW | | | | | | | |
| 预热比例 | 0.06 | | | | | | | |
| 学习率日程 | Linear | | | | | | | |
| RoBERTa base LoRA 批大小 | 16 | 16 | 16 | 32 | 32 | 16 | 32 | 16 |
| RoBERTa base LoRA 轮数 | 30 | 60 | 30 | 80 | 25 | 25 | 80 | 40 |
| RoBERTa base LoRA 学习率 | 5E-04 | 5E-04 | 4E-04 | 4E-04 | 4E-04 | 5E-04 | 5E-04 | 4E-04 |
| RoBERTa base LoRA 配置 | $r_q=r_v=8$ | | | | | | | |
| RoBERTa base LoRA α | 8 | | | | | | | |
| RoBERTa base 最大序列长度 | 512 | | | | | | | |
| RoBERTa large LoRA 批大小 | 4 | 4 | 4 | 4 | 4 | 4 | 8 | 8 |
| RoBERTa large LoRA 轮数 | 10 | 10 | 20 | 20 | 10 | 20 | 20 | 30 |
| RoBERTa large LoRA 学习率 | 3E-04 | 4E-04 | 3E-04 | 2E-04 | 2E-04 | 3E-04 | 4E-04 | 2E-04 |
| RoBERTa large LoRA 配置 | $r_q=r_v=8$ | | | | | | | |
| RoBERTa large LoRA α | 16 | | | | | | | |
| RoBERTa large 最大序列长度 | 128 | 128 | 512 | 128 | 512 | 512 | 512 | 512 |
| RoBERTa large LoRA† 批大小 | 4 | | | | | | | |
| RoBERTa large LoRA† 轮数 | 10 | 10 | 20 | 20 | 10 | 20 | 20 | 10 |
| RoBERTa large LoRA† 学习率 | 3E-04 | 4E-04 | 3E-04 | 2E-04 | 2E-04 | 3E-04 | 4E-04 | 2E-04 |
| RoBERTa large LoRA† 配置 | $r_q=r_v=8$ | | | | | | | |
| RoBERTa large LoRA† α | 16 | | | | | | | |
| RoBERTa large LoRA† 最大序列长度 | 128 | | | | | | | |
| RoBERTa large Adpt^P（3M）† 批大小 | 32 | | | | | | | |
| RoBERTa large Adpt^P（3M）† 轮数 | 10 | 20 | 20 | 20 | 10 | 20 | 20 | 20 |
| RoBERTa large Adpt^P（3M）† 学习率 | 3E-05 | 3E-05 | 3E-04 | 3E-04 | 3E-04 | 3E-04 | 3E-04 | 3E-04 |
| RoBERTa large Adpt^P（3M）† 瓶颈 r | 64 | | | | | | | |
| RoBERTa large Adpt^P（3M）† 最大序列长度 | 128 | | | | | | | |
| RoBERTa large Adpt^P（0.8M）† 批大小 | 32 | | | | | | | |
| RoBERTa large Adpt^P（0.8M）† 轮数 | 5 | 20 | 20 | 20 | 10 | 20 | 20 | 20 |
| RoBERTa large Adpt^P（0.8M）† 学习率 | 3E-04 | 3E-04 | 3E-04 | 3E-04 | 3E-04 | 3E-04 | 3E-04 | 3E-04 |
| RoBERTa large Adpt^P（0.8M）† 瓶颈 r | 16 | | | | | | | |
| RoBERTa large Adpt^P（0.8M）† 最大序列长度 | 128 | | | | | | | |
| RoBERTa large Adpt^H（6M）† 批大小 | 32 | | | | | | | |
| RoBERTa large Adpt^H（6M）† 轮数 | 10 | 5 | 10 | 10 | 5 | 20 | 20 | 10 |
| RoBERTa large Adpt^H（6M）† 学习率 | 3E-05 | 3E-04 | 3E-04 | 3E-04 | 3E-04 | 3E-04 | 3E-04 | 3E-04 |
| RoBERTa large Adpt^H（6M）† 瓶颈 r | 64 | | | | | | | |
| RoBERTa large Adpt^H（6M）† 最大序列长度 | 128 | | | | | | | |
| RoBERTa large Adpt^H（0.8M）† 批大小 | 32 | | | | | | | |
| RoBERTa large Adpt^H（0.8M）† 轮数 | 10 | 5 | 10 | 10 | 5 | 20 | 20 | 10 |
| RoBERTa large Adpt^H（0.8M）† 学习率 | 3E-04 | 3E-04 | 3E-04 | 3E-04 | 3E-04 | 3E-04 | 3E-04 | 3E-04 |
| RoBERTa large Adpt^H（0.8M）† 瓶颈 r | 8 | | | | | | | |
| RoBERTa large Adpt^H（0.8M）† 最大序列长度 | 128 | | | | | | | |

表 9：我们在 GLUE 基准上为 RoBERTa 使用的超参数。

### D.2 DeBERTa

我们同样使用 AdamW 和线性学习率衰减日程训练。
遵循 He et al.（2021），我们调节学习率、dropout 概率、预热步数和批大小。
我们使用与（He et al., 2021）相同的模型序列长度以保持比较公平。
遵循 He et al.（2021），在适配 MRPC、RTE 和 STS-B 时，我们将 LoRA 模块初始化为我们最佳的 MNLI 检查点，而非通常的初始化；预训练模型在所有任务中保持冻结。
我们报告 5 个随机种子上的中位数；每次运行的结果取最佳轮次。
我们运行所用的超参数见表 10。

| 方法与超参数 | MNLI | SST-2 | MRPC | CoLA | QNLI | QQP | RTE | STS-B |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 优化器 | AdamW | | | | | | | |
| 预热比例 | 0.1 | | | | | | | |
| 学习率日程 | Linear | | | | | | | |
| DeBERTa XXL LoRA 批大小 | 8 | 8 | 32 | 4 | 6 | 8 | 4 | 4 |
| DeBERTa XXL LoRA 轮数 | 5 | 16 | 30 | 10 | 8 | 11 | 11 | 10 |
| DeBERTa XXL LoRA 学习率 | 1E-04 | 6E-05 | 2E-04 | 1E-04 | 1E-04 | 1E-04 | 2E-04 | 2E-04 |
| DeBERTa XXL 权重衰减 | 0 | 0.01 | 0.01 | 0 | 0.01 | 0.01 | 0.01 | 0.1 |
| DeBERTa XXL CLS Dropout | 0.15 | 0 | 0 | 0.1 | 0.1 | 0.2 | 0.2 | 0.2 |
| DeBERTa XXL LoRA 配置 | $r_q=r_v=8$ | | | | | | | |
| DeBERTa XXL LoRA α | 8 | | | | | | | |
| DeBERTa XXL 最大序列长度 | 256 | 128 | 128 | 64 | 512 | 320 | 320 | 128 |

表 10：DeBERTa XXL 在 GLUE 基准所含任务上的超参数。

### D.3 GPT-2

我们所有 GPT-2 模型都使用 AdamW（Loshchilov & Hutter, 2017）和线性学习率日程训练 5 轮。
我们使用 Li & Liang（2021）描述的批大小、学习率和束搜索束宽。
相应地，我们也为 LoRA 调节上述超参数。
我们报告 3 个随机种子上的均值；每次运行的结果取最佳轮次。
GPT-2 中 LoRA 所用超参数列于表 11。
其他基线所用的超参数见 Li & Liang（2021）。

| 超参数 | E2E | WebNLG | DART |
| --- | --- | --- | --- |
| （训练） | | | |
| 优化器 | AdamW | | |
| 权重衰减 | 0.01 | 0.01 | 0.0 |
| Dropout 概率 | 0.1 | 0.1 | 0.0 |
| 批大小 | 8 | | |
| 轮数 | 5 | | |
| 预热步数 | 500 | | |
| 学习率日程 | Linear | | |
| 标签平滑 | 0.1 | 0.1 | 0.0 |
| 学习率 | 0.0002 | | |
| 适配配置 | $r_q=r_v=4$ | | |
| LoRA α | 32 | | |
| （推理） | | | |
| 束宽 | 10 | | |
| 长度惩罚 | 0.9 | 0.8 | 0.8 |
| no repeat ngram size | 4 | | |

表 11：GPT-2 LoRA 在 E2E、WebNLG 和 DART 上的超参数。

### D.4 GPT-3

所有 GPT-3 实验，我们使用 AdamW（Loshchilov & Hutter, 2017）训练 2 轮，批大小为 128 个样本，权重衰减因子为 0.1。
我们对 WikiSQL（Zhong et al., 2017）使用序列长度 384，MNLI（Williams et al., 2018）使用 768，SAMSum（Gliwa et al., 2019）使用 2048。
我们对所有方法-数据集组合调节学习率。
所用超参数的更多细节见 D.4 节。
对于前缀嵌入微调，我们发现最优的 $l_p$ 和 $l_i$ 分别为 256 和 8，总计 3.2M 可训练参数。
前缀层微调我们使用 $l_p=8$、$l_i=8$，共 20.2M 可训练参数，以获得总体最佳性能。
我们为 LoRA 提供两种参数预算：4.7M（$r_q=r_v=1$ 或 $r_v=2$）和 37.7M（$r_q=r_v=8$ 或 $r_q=r_k=r_v=r_o=2$）。
我们报告每次运行的最佳验证性能。
我们 GPT-3 实验使用的训练超参数列于表 12。

| 超参数 | Fine-Tune | PreEmbed | PreLayer | BitFit | Adapter^H | LoRA |
| --- | --- | --- | --- | --- | --- | --- |
| 优化器 | AdamW | | | | | |
| 批大小 | 128 | | | | | |
| 轮数 | 2 | | | | | |
| 预热 token 数 | 250,000 | | | | | |
| 学习率日程 | Linear | | | | | |
| 学习率 | 5.00E-06 | 5.00E-04 | 1.00E-04 | 1.6E-03 | 1.00E-04 | 2.00E-04 |

表 12：不同 GPT-3 适配方法使用的训练超参数。调节学习率后，我们对所有数据集使用相同超参数。

## 附录 E 将 LoRA 与前缀微调相结合

LoRA 可以自然地与现有的基于前缀的方法结合。
在本节中，我们在 WikiSQL 和 MNLI 上评估 LoRA 与前缀微调变体的两种组合。

LoRA+PrefixEmbed（LoRA+PE）将 LoRA 与前缀嵌入微调结合，其中我们插入 $l_p+l_i$ 个特殊 token，其嵌入被视为可训练参数。
关于前缀嵌入微调的更多内容见 5.1 节。

LoRA+PrefixLayer（LoRA+PL）将 LoRA 与前缀层微调结合。
我们同样插入 $l_p+l_i$ 个特殊 token；但不是让这些 token 的隐藏表示自然演化，而是在每个 Transformer 块之后将它们替换为一个与输入无关的向量。
因此，嵌入和后续 Transformer 块激活都被视为可训练参数。
关于前缀层微调的更多内容见 5.1 节。

在表 15 中，我们展示 LoRA+PE 和 LoRA+PL 在 WikiSQL 和 MultiNLI 上的评估结果。
首先，LoRA+PE 在 WikiSQL 上显著优于 LoRA 和前缀嵌入微调两者，这表明 LoRA 与前缀嵌入微调在一定程度上正交。
在 MultiNLI 上，LoRA+PE 的组合并不比 LoRA 更好，可能是因为 LoRA 单独就已经达到与人类基线相当的性能。
其次，我们注意到 LoRA+PL 即使有更多可训练参数，表现也略差于 LoRA。
我们将其归因于前缀层微调对学习率的选择非常敏感，因而使 LoRA+PL 中 LoRA 权重的优化更加困难。

## 附录 F 更多实证实验

### F.1 GPT-2 上的额外实验

我们还在 DART（Nan et al., 2020）和 WebNLG（Gardent et al., 2017）上遵循 Li & Liang（2021）的设置重复实验。
结果展示在表 13 中。
与第 5 节报告的 E2E NLG Challenge 上的结果类似，在可训练参数数量相同的情况下，LoRA 表现优于或至少持平于基于前缀的方法。

| 方法 | 可训练参数量 | DART BLEU↑ | DART MET↑ | DART TER↓ |
| --- | --- | --- | --- | --- |
| GPT-2 Medium | | | | |
| Fine-Tune | 354M | 46.2 | 0.39 | 0.46 |
| Adapter^L | 0.37M | 42.4 | 0.36 | 0.48 |
| Adapter^L | 11M | 45.2 | 0.38 | 0.46 |
| FT^Top2 | 24M | 41.0 | 0.34 | 0.56 |
| PrefLayer | 0.35M | 46.4 | 0.38 | 0.46 |
| LoRA | 0.35M | 47.1±.2 | 0.39 | 0.46 |
| GPT-2 Large | | | | |
| Fine-Tune | 774M | 47.0 | 0.39 | 0.46 |
| Adapter^L | 0.88M | 45.7±.1 | 0.38 | 0.46 |
| Adapter^L | 23M | 47.1±.1 | 0.39 | 0.45 |
| PrefLayer | 0.77M | 46.7 | 0.38 | 0.45 |
| LoRA | 0.77M | 47.5±.1 | 0.39 | 0.45 |

表 13：GPT-2 采用不同适配方法在 DART 上的表现。所有适配方法的 MET 和 TER 方差小于 0.01。

| 方法 | BLEU↑ U | BLEU↑ S | BLEU↑ A | MET↑ U | MET↑ S | MET↑ A | TER↓ U | TER↓ S | TER↓ A |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GPT-2 Medium | | | | | | | | | |
| Fine-Tune（354M） | 27.7 | 64.2 | 46.5 | .30 | .45 | .38 | .76 | .33 | .53 |
| Adapter^L（0.37M） | 45.1 | 54.5 | 50.2 | .36 | .39 | .38 | .46 | .40 | .43 |
| Adapter^L（11M） | 48.3 | 60.4 | 54.9 | .38 | .43 | .41 | .45 | .35 | .39 |
| FT^Top2（24M） | 18.9 | 53.6 | 36.0 | .23 | .38 | .31 | .99 | .49 | .72 |
| Prefix（0.35M） | 45.6 | 62.9 | 55.1 | .38 | .44 | .41 | .49 | .35 | .40 |
| LoRA（0.35M） | 46.7±.4 | 62.1±.2 | 55.3±.2 | .38 | .44 | .41 | .46 | .33 | .39 |
| GPT-2 Large | | | | | | | | | |
| Fine-Tune（774M） | 43.1 | 65.3 | 55.5 | .38 | .46 | .42 | .53 | .33 | .42 |
| Adapter^L（0.88M） | 49.8±.0 | 61.1±.0 | 56.0±.0 | .38 | .43 | .41 | .44 | .35 | .39 |
| Adapter^L（23M） | 49.2±.1 | 64.7±.2 | 57.7±.1 | .39 | .46 | .43 | .46 | .33 | .39 |
| Prefix（0.77M） | 47.7 | 63.4 | 56.3 | .39 | .45 | .42 | .48 | .34 | .40 |
| LoRA（0.77M） | 48.4±.3 | 64.0±.3 | 57.0±.1 | .39 | .45 | .42 | .45 | .32 | .38 |

表 14：GPT-2 采用不同适配方法在 WebNLG 上的表现。我们运行的实验中 MET 和 TER 方差小于 0.01。「U」表示未见类别，「S」表示见过类别，「A」表示 WebNLG 测试集中的全部类别。

### F.2 GPT-3 上的额外实验

我们在表 15 中展示 GPT-3 上不同适配方法的额外运行。
重点是识别性能与可训练参数数量之间的权衡。

| 方法 | 超参数 | 可训练参数量 | WikiSQL | MNLI-m |
| --- | --- | --- | --- | --- |
| Fine-Tune | - | 175B | 73.8 | 89.5 |
| PrefixEmbed | $l_p=32,l_i=8$ | 0.4 M | 55.9 | 84.9 |
| PrefixEmbed | $l_p=64,l_i=8$ | 0.9 M | 58.7 | 88.1 |
| PrefixEmbed | $l_p=128,l_i=8$ | 1.7 M | 60.6 | 88.0 |
| PrefixEmbed | $l_p=256,l_i=8$ | 3.2 M | 63.1 | 88.6 |
| PrefixEmbed | $l_p=512,l_i=8$ | 6.4 M | 55.9 | 85.8 |
| PrefixLayer | $l_p=2,l_i=2$ | 5.1 M | 68.5 | 89.2 |
| PrefixLayer | $l_p=8,l_i=0$ | 10.1 M | 69.8 | 88.2 |
| PrefixLayer | $l_p=8,l_i=8$ | 20.2 M | 70.1 | 89.5 |
| PrefixLayer | $l_p=32,l_i=4$ | 44.1 M | 66.4 | 89.6 |
| PrefixLayer | $l_p=64,l_i=0$ | 76.1 M | 64.9 | 87.9 |
| Adapter^H | r=1 | 7.1 M | 71.9 | 89.8 |
| Adapter^H | r=4 | 21.2 M | 73.2 | 91.0 |
| Adapter^H | r=8 | 40.1 M | 73.2 | 91.5 |
| Adapter^H | r=16 | 77.9 M | 73.2 | 91.5 |
| Adapter^H | r=64 | 304.4 M | 72.6 | 91.5 |
| LoRA | $r_v=2$ | 4.7 M | 73.4 | 91.7 |
| LoRA | $r_q=r_v=1$ | 4.7 M | 73.4 | 91.3 |
| LoRA | $r_q=r_v=2$ | 9.4 M | 73.3 | 91.4 |
| LoRA | $r_q=r_k=r_v=r_o=1$ | 9.4 M | 74.1 | 91.2 |
| LoRA | $r_q=r_v=4$ | 18.8 M | 73.7 | 91.3 |
| LoRA | $r_q=r_k=r_v=r_o=2$ | 18.8 M | 73.7 | 91.7 |
| LoRA | $r_q=r_v=8$ | 37.7 M | 73.8 | 91.6 |
| LoRA | $r_q=r_k=r_v=r_o=4$ | 37.7 M | 74.0 | 91.7 |
| LoRA | $r_q=r_v=64$ | 301.9 M | 73.6 | 91.4 |
| LoRA | $r_q=r_k=r_v=r_o=64$ | 603.8 M | 73.9 | 91.4 |
| LoRA+PE | $r_q=r_v=8,l_p=8,l_i=4$ | 37.8 M | 75.0 | 91.4 |
| LoRA+PE | $r_q=r_v=32,l_p=8,l_i=4$ | 151.1 M | 75.9 | 91.1 |
| LoRA+PE | $r_q=r_v=64,l_p=8,l_i=4$ | 302.1 M | 76.2 | 91.3 |
| LoRA+PL | $r_q=r_v=8,l_p=8,l_i=4$ | 52.8 M | 72.9 | 90.2 |

表 15：不同适配方法在 WikiSQL 和 MNLI 上的超参数分析。随着可训练参数数量增加，前缀嵌入微调（PrefixEmbed）和前缀层微调（PrefixLayer）的表现都变差，而 LoRA 的性能保持稳定。性能以验证准确率衡量。

### F.3 低数据量情形

为评估不同适配方法在低数据量情形下的表现，我们从 MNLI 的完整训练集中随机采样 100、1k 和 10k 个训练样本，构成低数据 MNLI-nn 任务。
在表 16 中，我们展示不同适配方法在 MNLI-nn 上的表现。
令我们惊讶的是，PrefixEmbed 和 PrefixLayer 在 MNLI-100 数据集上表现非常差，PrefixEmbed 只比随机猜测略好（37.6% 对 33.3%）。
PrefixLayer 比 PrefixEmbed 好，但在 MNLI-100 上仍显著差于 Fine-Tune 或 LoRA。
随着训练样本增多，基于前缀的方法与 LoRA/微调之间的差距缩小，这可能表明基于前缀的方法不适合 GPT-3 的低数据任务。
LoRA 在 MNLI-100 和 MNLI-Full 上都取得比微调更好的性能，在 MNLI-1k 和 MNLI-10K 上考虑到随机种子带来的（±0.3）方差，结果也相当。

| 方法 | MNLI(m)-100 | MNLI(m)-1k | MNLI(m)-10k | MNLI(m)-392K |
| --- | --- | --- | --- | --- |
| GPT-3（Fine-Tune） | 60.2 | 85.8 | 88.9 | 89.5 |
| GPT-3（PrefixEmbed） | 37.6 | 75.2 | 79.5 | 88.6 |
| GPT-3（PrefixLayer） | 48.3 | 82.5 | 85.9 | 89.6 |
| GPT-3（LoRA） | 63.8 | 85.6 | 89.2 | 91.7 |

表 16：不同方法在 MNLI 子集上使用 GPT-3 175B 的验证准确率。MNLI-nn 表示含 $n$ 个训练样本的子集。我们用完整验证集评估。相比其他方法（包括微调），LoRA 展现出良好的样本效率。

不同适配方法在 MNLI-n 上的训练超参数报告在表 17 中。
我们对 PrefixLayer 在 MNLI-100 集上使用更小的学习率，因为更大的学习率下训练损失不下降。

| 超参数 | 适配方法 | MNLI-100 | MNLI-1k | MNLI-10K | MNLI-392K |
| --- | --- | --- | --- | --- | --- |
| 优化器 | - | AdamW | | | |
| 预热 token 数 | - | 250,000 | | | |
| 学习率日程 | - | Linear | | | |
| 批大小 | - | 20 | 20 | 100 | 128 |
| 轮数 | - | 40 | 40 | 4 | 2 |
| 学习率 | FineTune | 5.00E-6 | | | |
| 学习率 | PrefixEmbed | 2.00E-04 | 2.00E-04 | 4.00E-04 | 5.00E-04 |
| 学习率 | PrefixLayer | 5.00E-05 | 5.00E-05 | 5.00E-05 | 1.00E-04 |
| 学习率 | LoRA | 2.00E-4 | | | |
| 适配专属 | PrefixEmbed $l_p$ | 16 | 32 | 64 | 256 |
| 适配专属 | PrefixEmbed $l_i$ | 8 | | | |
| 适配专属 | PrefixTune | $l_p=l_i=8$ | | | |
| 适配专属 | LoRA | $r_q=r_v=8$ | | | |

表 17：不同 GPT-3 适配方法在 MNLI(m)-nn 上使用的超参数。

## 附录 G 度量子空间之间的相似度

本文中我们使用度量 $\phi(A,B,i,j)=\psi(U_{A}^{i},U_{B}^{j})=\frac{\|U_{A}^{i\top}U_{B}\|_{F}^{2}}{\min\{i,j\}}$ 来度量两个列正交矩阵 $U_{A}^{i}\in\mathbb{R}^{d\times i}$ 与 $U_{B}^{j}\in\mathbb{R}^{d\times j}$ 之间的子空间相似度，它们由取 $A$ 和 $B$ 的左奇异矩阵的列得到。
我们指出，这一相似度就是度量子空间之间距离的标准投影度量（Projection Metric）的反转（Ham & Lee, 2008）。

具体地，设 $U_{A}^{i\top}U_{B}^{j}$ 的奇异值为 $\sigma_{1},\sigma_{2},\cdots,\sigma_{p}$，其中 $p=\min\{i,j\}$。我们知道投影度量（Ham & Lee, 2008）定义为：

$$d(U_{A}^{i},U_{B}^{j})=\sqrt{p-\sum_{i=1}^{p}\sigma_{i}^{2}}\in[0,\sqrt{p}]$$

而我们的相似度定义为：

$$\phi(A,B,i,j)=\psi(U_{A}^{i},U_{B}^{j})=\frac{\sum_{i=1}^{p}\sigma_{i}^{2}}{p}=\frac{1}{p}\left(1-d(U_{A}^{i},U_{B}^{j})^{2}\right)$$

这一相似度满足：若 $U_{A}^{i}$ 与 $U_{B}^{j}$ 具有相同的列张成空间，则 $\phi(A,B,i,j)=1$。
若它们完全正交，则 $\phi(A,B,i,j)=0$。否则，$\phi(A,B,i,j)\in(0,1)$。

## 附录 H 低秩矩阵的额外实验

我们展示对低秩更新矩阵研究的额外结果。

### H.1 LoRA 模块之间的相关性

图 6 和图 7 展示了图 3 和图 4 的结果如何推广到其他层。

![图 6](2106.09685v2/qv8_qv64_more_layers.png)

图 6：96 层 Transformer 中第 1、32、64、96 层的 $A_{r=8}$ 与 $A_{r=64}$ 列向量之间的归一化子空间相似度，同时给出 $\Delta W_q$ 和 $\Delta W_v$。

图 7：96 层 Transformer 中第 1、32、64、96 层的、来自两个随机种子运行的 $A_{r=64}$ 列向量之间的归一化子空间相似度，同时给出 $\Delta W_q$ 和 $\Delta W_v$。

### H.2 $r$ 对 GPT-2 的影响

我们在 GPT-2 上重复关于 $r$ 的影响的实验（7.2 节）。
以 E2E NLG Challenge 数据集为例，我们报告训练 26,000 步后不同 $r$ 选择取得的验证损失和测试指标。
结果展示在表 18 中。
GPT-2 Medium 的最优秩在 4 到 16 之间，取决于所用指标，这与 GPT-3 175B 类似。
注意，模型规模与适配最优秩之间的关系仍是一个开放问题。

| 秩 r | val_loss | BLEU | NIST | METEOR | ROUGE_L | CIDEr |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1.23 | 68.72 | 8.7215 | 0.4565 | 0.7052 | 2.4329 |
| 2 | 1.21 | 69.17 | 8.7413 | 0.4590 | 0.7052 | 2.4639 |
| 4 | 1.18 | 70.38 | 8.8439 | 0.4689 | 0.7186 | 2.5349 |
| 8 | 1.17 | 69.57 | 8.7457 | 0.4636 | 0.7196 | 2.5196 |
| 16 | 1.16 | 69.61 | 8.7483 | 0.4629 | 0.7177 | 2.4985 |
| 32 | 1.16 | 69.33 | 8.7736 | 0.4642 | 0.7105 | 2.5255 |
| 64 | 1.16 | 69.24 | 8.7174 | 0.4651 | 0.7180 | 2.5070 |
| 128 | 1.16 | 68.73 | 8.6718 | 0.4628 | 0.7127 | 2.5030 |
| 256 | 1.16 | 68.92 | 8.6982 | 0.4629 | 0.7128 | 2.5012 |
| 512 | 1.16 | 68.78 | 8.6857 | 0.4637 | 0.7128 | 2.5025 |
| 1024 | 1.17 | 69.37 | 8.7495 | 0.4659 | 0.7149 | 2.5090 |

表 18：GPT-2 Medium 上不同秩 r 的 LoRA 在 E2E NLG Challenge 上取得的验证损失和测试集指标。与 GPT-3 上许多任务 r=1 即足够不同，这里验证损失在 r=16 处达到峰值、BLEU 在 r=4 处达到峰值，表明 GPT-2 Medium 与 GPT-3 175B 具有相近的适配内在秩。注意，我们的部分超参数是在 r=4 上调节的（与另一个基线的参数量匹配），因此对其他 r 的选择可能并非最优。

### H.3 $W$ 与 $\Delta W$ 之间的相关性

图 8 展示了不同 $r$ 下 $W$ 与 $\Delta W$ 之间的归一化子空间相似度。

再次注意，$\Delta W$ 不包含 $W$ 的顶部奇异方向，因为 $\Delta W$ 中前 4 个方向与 $W$ 中前 10% 方向之间的相似度勉强超过 0.2。这为如下观点提供了证据：$\Delta W$ 包含那些在 $W$ 中*未*被强调的「任务专属」方向。

一个有趣的后续问题是：为了让模型适配表现良好，我们需要把这些任务专属方向放大到多「强」？

![图 8](2106.09685v2/w_vs_delta_w.png)

图 8：不同 r 下 $W_q$ 的奇异方向与 $\Delta W_q$ 的奇异方向之间的归一化子空间相似度，以及随机基线。$\Delta W_q$ 放大了那些在 $W$ 中重要但未被强调的方向。r 更大的 $\Delta W$ 往往会拾取更多在 $W$ 中已被强调的方向。

### H.4 放大因子

可以很自然地把*特征放大因子*考虑为比值 $\frac{\|\Delta W\|_{F}}{\|U^{\top}WV^{\top}\|_{F}}$，其中 $U$ 和 $V$ 是 $\Delta W$ 的 SVD 分解的左、右奇异矩阵。（回忆 $UU^{\top}WV^{\top}V$ 给出 $W$ 在 $\Delta W$ 张成子空间上的「投影」。）

直观地说，当 $\Delta W$ 主要包含任务专属方向时，该量衡量其中有多少被 $\Delta W$ 放大。
如 7.3 节所示，对 r=4，这一放大因子高达 20。换句话说，（一般而言）每一层中有四个特征方向（占预训练模型 $W$ 的整个特征空间）需要被放大很大的倍数 20，才能达到我们报告的下游特定任务准确率。而且，应当预期每个不同的下游任务会放大一组截然不同的特征方向。

不过人们可能注意到，对 r=64，这一放大因子只有 2 左右，意味着 r=64 的 $\Delta W$ 中学到的*大多数*方向*没有*被放大多少。
这不应令人惊讶，实际上（再次）给出了证据：表示「任务专属方向」（从而用于模型适配）*所需*的内在秩是低的。
相比之下，秩 4 版本 $\Delta W$（对应 r=4）中的那些方向被大得多的倍数 20 放大。
