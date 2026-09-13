---
title: "大型 Transformer 模型推理优化"
title_en: "Large Transformer Model Inference Optimization"
source: https://lilianweng.github.io/posts/2023-01-10-inference-optimization/
crawled: 2026-09-08
translated: 2026-09-08
---

# 大型 Transformer 模型推理优化

> 原文：[Large Transformer Model Inference Optimization](https://lilianweng.github.io/posts/2023-01-10-inference-optimization/) · Lilian Weng（翁荔）

[更新于 2023-01-24：增加了一小节关于[蒸馏](#distillation)的内容。]

如今，大型 Transformer 模型已是主流，在各类任务上不断创造最优（SoTA）成绩。它们功能强大，但训练和使用都非常昂贵。无论是时间还是内存，极高的推理成本都是大规模采用强大的 Transformer 来解决现实任务的一大瓶颈。

**为什么运行大型 Transformer 模型的推理很困难？** 除了 SoTA 模型的规模不断增长之外，还有两个造成推理挑战的主要因素（[Pope et al. 2022](https://arxiv.org/abs/2211.05102)）：

1. *内存占用大*。推理时，模型参数和中间状态都需要驻留在内存中。例如：
   - 解码期间需要把 KV 缓存（KV cache）保存在内存中；例如，当批大小为 512、上下文长度为 2048 时，KV 缓存总计可达 3TB，是模型大小的 3 倍（！）。
   - 注意力机制带来的推理开销随输入序列长度呈平方增长。
2. *可并行性低*。推理生成以自回归方式执行，使得解码过程难以并行。

本文将探讨几种让 Transformer 推理更高效的方法。其中一些是通用的网络压缩方法，另一些则专门针对 Transformer 架构。

# 方法概览

我们通常将以下几项视为模型推理优化的目标：

- 使用更少的 GPU 设备、占用更少的 GPU 内存，从而降低模型的内存占用；
- 降低所需的 FLOPs 数量，从而降低计算复杂度；
- 降低推理延迟，让一切跑得更快。

有多种方法可以让推理在内存上更省、在时间上更快，或两者兼得。

1. 施加各种*并行*（parallelism）策略，将模型扩展到大量 GPU 上。对模型组件和数据进行巧妙的并行化，使运行数万亿参数的模型成为可能。
2. 内存*卸载*（offloading）：把暂时不用的数据卸载到 CPU，之后再按需读回。这有助于降低内存占用，但会带来更高的延迟。
3. 巧妙的批处理策略；例如 [EffectiveTransformer](https://github.com/bytedance/effective_transformer) 将连续的序列打包在一起，消除一个批次内部的填充。
4. 网络*压缩*（compression）技术，如*剪枝、量化、蒸馏*。参数量或位宽更小的模型理应占用更少内存、运行更快。
5. 针对特定模型架构的改进。许多*架构上的改动*，尤其是注意力层的改动，有助于提升 Transformer 的解码速度。

关于训练并行的不同类型以及包括 CPU 内存卸载在内的省内存设计，请参阅[上一篇关于大模型训练的文章](https://lilianweng.github.io/posts/2021-09-25-train-large/)。本文聚焦于网络压缩技术以及针对 Transformer 模型的架构改进。

# 蒸馏

**知识蒸馏**（Knowledge Distillation，KD；[Hinton et al. 2015](https://arxiv.org/abs/1503.02531)、[Gou et al. 2020](https://arxiv.org/abs/2006.05525)）是构建一个更小、更廉价模型（“学生模型”）来加速推理的直接方法：把预训练昂贵模型（“教师模型”）的能力迁移到学生中。除了学生的输出空间需要与教师匹配、以便构造合适的学习目标之外，学生架构如何设计几乎没有限制。

![](https://lilianweng.github.io/posts/2023-01-10-inference-optimization/distillation.png)

*教师-学生知识蒸馏训练的通用框架。（图片来源：Gou et al. 2020）*

给定一个数据集，学生模型通过蒸馏损失训练来模仿教师的输出。神经网络通常带有 softmax 层；例如，LLM 会输出 token 上的概率分布。我们把教师模型和学生模型中紧邻 softmax 之前的 logits 层分别记为 $\mathbf{z}_t$ 与 $\mathbf{z}_s$。*蒸馏损失*（distillation loss）最小化两个 softmax 输出在较高温度 $T$ 下的差异。当已知真实标签 $\mathbf{y}$ 时，我们还可以将其与真实标签和学生软 logits 之间的*监督*学习目标（例如交叉熵）结合。

$$
\mathcal{L}_\text{KD} = \mathcal{L}_\text{distll}(\text{softmax}(\mathbf{z}_t, T), \text{softmax}(\mathbf{z}_s, T)) + \lambda\mathcal{L}_\text{CE}(\mathbf{y}, \mathbf{z}_s)
$$

其中 $\lambda$ 是用于平衡软学习目标与硬学习目标的超参数。$\mathcal{L}_\text{distll}$ 的常见选择是 KL 散度 / 交叉熵。

一次成功的早期尝试是 **DistilBERT**（[Sanh et al. 2019](https://arxiv.org/abs/1910.01108)），它将 BERT 的参数量减少了 40%，在微调后的下游任务上保持了 BERT 97% 的性能，同时运行速度提升 71%。DistilBERT 的预训练损失由软蒸馏损失、监督训练损失（对 BERT 而言即[掩码语言建模损失](https://lilianweng.github.io/posts/2019-01-31-lm/#MLM) $\mathcal{L}_\text{MLM}$）以及一个用于对齐教师与学生隐状态向量的特殊*余弦嵌入损失*（cosine embedding loss）组合而成。

蒸馏可以很方便地与[量化](#quantization)、[剪枝](#pruning)或[稀疏化](#sparsity)技术结合：教师模型是原始的全精度稠密模型，而学生模型则被量化、剪枝或裁剪至更高的稀疏程度。

# 量化

在深度神经网络上应用量化有两种常见做法：

1. *训练后量化（Post-Training Quantization，PTQ）*：模型先训练至收敛，然后在不进行额外训练的情况下将其权重转换为较低精度。与训练相比，这种做法的实现成本通常很低。
2. *量化感知训练（Quantization-Aware Training，QAT）*：在预训练或进一步微调的过程中应用量化。QAT 能取得更好的性能，但需要额外的计算资源以及有代表性的训练数据。

我们应当意识到理论最优量化策略与硬件算子（kernel）支持之间的差距。由于 GPU 缺乏对某些类型矩阵乘法（如 INT4 x FP16）的算子支持，下文的方法并非都能带来实际推理的加速。

## Transformer 量化的挑战

许多关于 Transformer 模型量化的研究有着相同的观察：简单的低精度（如 8 比特）训练后量化会导致显著的性能下降，主要原因在于激活值的高动态范围，而朴素的激活量化策略无法维持模型容量。

![](https://lilianweng.github.io/posts/2023-01-10-inference-optimization/quantization-experiment-table.png)

*只把模型权重量化到 8 比特、激活保持全精度（`W8A32`），比把激活也量化到 8 比特——无论权重是否为低精度（`W8A8` 与 `W32A8`）——效果好得多。（图片来源：Bondarenko et al. 2021）*

[Bondarenko et al. (2021)](https://arxiv.org/abs/2109.12948) 在一个小型 BERT 模型中观察到，由于输出张量中存在强烈的离群值（outlier），FFN（前馈网络）的输入和输出具有非常不同的动态范围。因此，对 FFN 的残差和做逐张量（per-tensor）量化很可能造成显著误差。

随着模型规模增长到数十亿参数，高幅值的离群特征开始在*所有* transformer 层中出现，导致简单的低位量化失效。[Dettmers et al. (2022)](https://arxiv.org/abs/2208.07339) 在参数量超过 6.7B 的 [OPT](https://arxiv.org/abs/2205.01068) 模型上观察到了这一现象。模型越大，含极端离群值的层越多，而这些离群特征对模型性能有显著影响。少数维度上激活离群值的尺度可能比其余大多数值高出约 100 倍。

![](https://lilianweng.github.io/posts/2023-01-10-inference-optimization/OPT-models-outlier.png)

*规模递增的 OPT 模型在一组语言任务（WinoGrande、HellaSwag、PIQA、LAMBADA）上的平均零样本准确率。（图片来源：Dettmers et al. 2022）*

## 训练后量化（PTQ）

### 混合精度量化

解决上述量化挑战最直接的方法，是对权重与激活采用不同精度的量化。

GOBO（[Zadeh et al. 2020](https://arxiv.org/abs/2005.03842)）是最早把训练后量化应用于 transformer（即一个小型 BERT 模型）的工作之一。它假设每层的模型权重服从高斯分布，因此通过跟踪每层的均值和标准差来检测离群值。离群特征保持原样，其余数值则被切分到多个桶（bin）中，只需存储权重对应的桶索引以及质心值。

基于只有 BERT 中某些激活层（如 FFN 后的残差连接）会导致大幅性能下降这一观察，[Bondarenko et al. (2021)](https://arxiv.org/abs/2109.12948) 采用了混合精度量化：对有问题的激活使用 16 比特量化，对其他激活使用 8 比特。

`LLM.int8()`（[Dettmers et al. 2022](https://arxiv.org/abs/2208.07339)）中的混合精度量化通过两种混合精度分解来实现：

1. 矩阵乘法包含一组行向量与列向量之间相互独立的内积，因此可以对每个内积独立地施加量化：每行和每列先按各自元素的绝对值最大值进行缩放，然后量化为 INT8。
2. 离群激活特征（例如比其他维度大 20 倍）保持 FP16，但它们只占权重总量中极小的一部分。如何识别离群值则凭经验确定。

![](https://lilianweng.github.io/posts/2023-01-10-inference-optimization/LLM-int8.png)

*`LLM.int8()` 的两种混合精度分解。（图片来源：Dettmers et al. 2022）*

### 细粒度量化

![](https://lilianweng.github.io/posts/2023-01-10-inference-optimization/quantization-granularity.png)

*不同粒度量化的对比。$d$ 是模型尺寸 / 隐状态维度，$h$ 是一个 MHSA（多头自注意力）组件中的头数。*

朴素地把一层的整个权重矩阵一起量化（“逐张量”或“逐层”量化）最容易实现，但得不到好的量化粒度。

**Q-BERT**（[Shen, Dong & Ye, et al. 2020](https://arxiv.org/abs/1909.05840)）对微调后的 BERT 模型应用*分组量化*（group-wise quantization）：把 MHSA（多头自注意力）中*每个头*对应的一个单独矩阵 $W$ 视为一组，然后应用基于 Hessian 矩阵的混合精度量化。

*逐嵌入分组（Per-embedding group，PEG）*激活量化源于这一观察：离群值只出现在 $d$（隐状态 / 模型尺寸）个维度中的少数几个（[Bondarenko et al. 2021](https://arxiv.org/abs/2109.12948)）。逐嵌入量化的计算开销相当大；相比之下，PEG 量化沿嵌入维度把激活张量切分为若干大小相同的组，同组元素共享量化参数。为确保所有离群值都被分到同一组，他们对嵌入维度做确定性的、基于数值范围的置换，即按各维度的取值范围排序。

**ZeroQuant**（[Yao et al. 2022](https://arxiv.org/abs/2206.01861)）对权重使用与 Q-BERT 相同的*分组量化*，对激活使用*逐 token 量化*（token-wise quantization）。为避免昂贵的量化与反量化计算，ZeroQuant 构建了定制*算子*（kernel），把量化操作与其前一个算子*融合*（fuse）在一起。

### 用于量化的二阶信息

Q-BERT（[Shen, Dong & Ye, et al. 2020](https://arxiv.org/abs/1909.05840)）为其混合精度量化提出了 Hessian 感知量化（Hessian AWare Quantization，HAWQ）。其动机是：Hessian 谱较高（即较大的特征值更大）的参数对量化更敏感，因而需要更高的精度。这本质上是一种识别离群值的方式。

从另一个角度看，量化问题是一个优化问题。给定权重矩阵 $\mathbf{W}$ 和输入矩阵 $\mathbf{X}$，我们希望找到一个量化后的权重矩阵 $\hat{\mathbf{W}}$ 来最小化 MSE：

$$
\hat{\mathbf{W}}^* = {\arg\min}_{\hat{\mathbf{W}}} | \mathbf{W}\mathbf{X} - \hat{\mathbf{W}}\mathbf{X}|
$$

**GPTQ**（[Frantar et al. 2022](https://arxiv.org/abs/2210.17323)）把权重矩阵 $\mathbf{W}$ 视为行向量 ${\mathbf{w}}$ 的集合，并对每一行独立地施以量化。GPTQ 迭代地量化更多权重，这些权重以贪心方式选出，以最小化量化误差。对被选中权重的更新利用 Hessian 矩阵得到了闭式公式。如果感兴趣，可以阅读论文以及 OBQ（Optimal Brain Quantization；[Frantar & Alistarh 2022](https://arxiv.org/abs/2208.11580)）方法的更多细节。GPTQ 能把 OPT-175B 的权重位宽降到 3 或 4 比特而几乎没有性能损失，但它只适用于模型权重，不适用于激活。

### 离群值平滑

众所周知，在 transformer 模型中，激活比权重更难量化。**SmoothQuant**（[Xiao & Lin 2022](https://arxiv.org/abs/2211.10438)）提出了一个巧妙的方案：通过数学等价变换把激活中的离群特征平滑地转移到权重上，然后对权重和激活都启用量化（`W8A8`）。正因如此，SmoothQuant 比混合精度量化具有更好的硬件效率。

![](https://lilianweng.github.io/posts/2023-01-10-inference-optimization/SmoothQuant.png)

*SmoothQuant 在离线状态下把尺度方差从激活迁移到权重，以降低激活量化的难度。得到的新权重矩阵和激活矩阵都易于量化。（图片来源：Xiao & Lin 2022）*

考虑一个逐通道（per-channel）的平滑因子 $\mathbf{s}$，SmoothQuant 按下式对权重进行缩放：

$$
\mathbf{Y} = (\mathbf{X} \text{diag}(\mathbf{s})^{-1}) \cdot (\text{diag}(\mathbf{s})\mathbf{W}) = \hat{\mathbf{X}}\hat{\mathbf{W}}
$$

该平滑因子可以在离线时轻松融合进前一层的参数。超参数 $\alpha$ 控制把量化难度从激活迁移到权重的程度：$\mathbf{s} = \max (\vert \mathbf{X}_j \vert)^\alpha  / \max( \vert \mathbf{W}_j \vert )^{1-\alpha}$。论文发现，在实验中 $\alpha=0.5$ 是许多 LLM 的最佳平衡点。对于激活中离群值更显著的模型，可以把 $\alpha$ 调得更大。

## 量化感知训练（QAT）

量化感知训练把量化操作融入预训练或微调过程，直接以低比特表示学习模型权重，以额外的训练时间和计算为代价换取更好的性能。

最直接的做法是在量化之后，在与预训练数据集相同或能代表它的训练数据集上**微调**模型。训练目标可以与预训练目标相同（如一般语言模型训练中的 NLL/MLM），也可以针对我们关心的下游任务（如分类任务的交叉熵）。

另一种做法是把全精度模型视为教师、低精度模型视为学生，然后用**蒸馏**损失优化低精度模型。蒸馏通常不需要使用原始数据集；例如维基百科数据集就是一个不错的选择，甚至随机 token 也能带来不错的性能提升。*逐层知识蒸馏*（Layer-by-layer Knowledge Distillation，LKD；[Yao et al. 2022](https://arxiv.org/abs/2206.01861)）方法逐层量化网络，并使用其原始的未量化版本作为教师模型。给定相同输入，LKD 最小化“与层权重相乘”和“与量化后层权重相乘”之间的 MSE。

# 剪枝

网络剪枝（pruning）通过剪掉不重要的模型权重或连接来缩减模型规模，同时保持模型容量。它可能需要重训练，也可能不需要。剪枝可以是**非结构化**的或**结构化**的。

- *非结构化剪枝*（unstructured pruning）可以丢弃任意权重或连接，因此不保留原始网络架构。非结构化剪枝在现代硬件上往往效果不佳，无法带来实际的推理加速。
- *结构化剪枝*（structured pruning）旨在保持稠密矩阵乘法的形式，只是其中一些元素为零。它们可能需要遵循特定的模式限制，以配合硬件算子所支持的形式。这里我们关注通过结构化剪枝在 transformer 模型中实现*高稀疏度*。

构建剪枝网络的常规工作流分为三步：

1. 训练一个稠密网络直至收敛；
2. 对网络剪枝，去掉不需要的结构；
3. （可选）重新训练网络，用新权重恢复性能。

通过网络剪枝在稠密模型中发现一个仍能保持相近性能的稀疏结构，这一想法的动机来自[**彩票假说**（Lottery Ticket Hypothesis，LTH）](https://lilianweng.github.io/posts/2019-03-14-overfit/#the-lottery-ticket-hypothesis)：一个随机初始化的稠密前馈网络中包含一池子网络，其中只有一部分（一个稀疏网络）是*“中奖彩票”*（winning tickets），它们单独训练即可达到最优性能。

## 如何剪枝？

**幅度剪枝**（magnitude pruning）是最简单却相当有效的剪枝方法——把绝对值最小的权重剪掉。事实上，一些研究（[Gale et al. 2019](https://arxiv.org/abs/1902.09574)）发现，*简单的幅度剪枝方法可以达到与复杂剪枝方法相当甚至更好的结果*，例如变分 dropout（[Molchanov et al. 2017](https://arxiv.org/abs/1701.05369)）和 $l_0$ 正则化（[Louizos et al. 2017](https://arxiv.org/abs/1712.01312)）。幅度剪枝易于应用于大模型，并且在很宽的超参数范围内都能取得相当稳定的性能。

[Zhu & Gupta (2017)](https://arxiv.org/abs/1710.01878) 发现，*大的稀疏模型能够比小而稠密的对应模型取得更好的性能*。他们提出了**渐进幅度剪枝**（Gradual Magnitude Pruning，GMP）算法，在训练过程中逐步提高网络的稀疏度。在每个训练步，绝对值最小的权重被掩码为零，以达到目标稀疏度 $s$，且被掩码的权重在反向传播期间不接收梯度更新。目标稀疏度 $s$ 随训练步数增加而提高。GMP 的过程对学习率调度很敏感：学习率应高于稠密网络训练所用的值，但也不能高到无法收敛。

**迭代式剪枝**（[Renda et al. 2020](https://arxiv.org/abs/2003.02389)）将第 2 步（剪枝）和第 3 步（重训练）迭代多次：每次迭代只剪掉一小部分权重，然后重新训练模型。如此重复，直到达到目标稀疏度。

## 如何重训练？

重训练这一步可以只是用相同的预训练数据或其他任务专用数据集做简单的微调。

[彩票假说](https://lilianweng.github.io/posts/2019-03-14-overfit/#the-lottery-ticket-hypothesis)提出了一种**权重回卷**（weight rewinding）重训练技术：剪枝之后，未被剪掉的权重被*重新初始化为训练早期阶段的原始值*，然后按相同的学习率调度重新训练。

**学习率回卷**（[Renda et al. 2020](https://arxiv.org/abs/2003.02389)）只把学习率重置回早期的值，而未剪权重保持上一训练阶段结束时的状态不变。他们观察到：(1) 在各种网络和数据集上，权重回卷重训练都优于微调式重训练；(2) 在所有测试场景中，学习率回卷与权重回卷持平或更优。

# 稀疏化

稀疏化（sparsity）是在扩大模型容量的同时保持推理计算效率的有效手段。这里我们考虑 transformer 的两类稀疏化：

- 对稠密层做稀疏化，包括自注意力层和 FFN 层。
- 稀疏的模型架构，即通过引入专家混合（Mixture-of-Experts，MoE）组件。

## 通过剪枝实现 N:M 稀疏化

**N:M 稀疏性**（N:M sparsity）是一种与现代 GPU 硬件优化配合良好的结构化稀疏模式：每 $M$ 个连续元素中有 $N$ 个为零。例如，Nvidia A100 GPU 的稀疏张量核心支持 2:4 稀疏性，以实现更快的推理（[Nvidia 2020](https://images.nvidia.com/aem-dam/en-zz/Solutions/data-center/nvidia-ampere-architecture-whitepaper.pdf)）。

![](https://lilianweng.github.io/posts/2023-01-10-inference-optimization/2-to-4-sparsity.png)

*一个具有 2:4 结构化稀疏性的矩阵及其压缩表示。（图片来源：Nvidia 博客）*

要把稠密神经网络稀疏化为符合 N:M 结构化稀疏模式，[Nvidia (2020)](https://images.nvidia.com/aem-dam/en-zz/Solutions/data-center/nvidia-ampere-architecture-whitepaper.pdf) 建议采用训练剪枝网络的三步[常规工作流](#routine-workflow)：训练 –> 剪枝以满足 2:4 稀疏性 –> 重训练。

对列做置换（permutation）可以在剪枝过程中提供更多选择，以保留大幅值的参数或满足诸如 N:M 稀疏性之类的特殊限制（[Pool & Yu 2021](https://proceedings.neurips.cc/paper/2021/hash/6e8404c3b93a9527c8db241a1846599a-Abstract.html)）。只要两个矩阵的成对轴按相同顺序置换，矩阵乘法的结果就不会改变。例如：

(1) 在自注意力模块内，如果对查询嵌入矩阵 $\mathbf{Q}$ 的轴 1 和键嵌入矩阵 $\mathbf{K}^\top$ 的轴 0 施加相同的置换顺序，那么 $\mathbf{Q}\mathbf{K}^\top$ 矩阵乘法的最终结果保持不变。

![](https://lilianweng.github.io/posts/2023-01-10-inference-optimization/permutation-QK.png)

*对 $\mathbf{Q}$（轴 1）与 $\mathbf{K}^\top$（轴 0）施加相同置换、从而保持自注意力模块结果不变的示意图。*

(2) 在包含两个 MLP 层和一个 ReLU 非线性层的 FFN 层内，我们可以按相同顺序对第一个线性权重矩阵 $\mathbf{W}_1$ 沿轴 1、第二个线性权重矩阵 $\mathbf{W}_2$ 沿轴 0 做置换。

![](https://lilianweng.github.io/posts/2023-01-10-inference-optimization/permutation-FFN.png)

*对 $\mathbf{W}_1$（轴 1）与 $\mathbf{W}_2$（轴 0）施加相同置换、从而保持 FFN 层输出不变的示意图。为简单起见，图中省略了偏置项，但同样的置换也应施加于偏置。*

为了强制实现 N:M 结构化稀疏性，我们把一个矩阵的列切分为多个由 $M$ 列组成的条带（stripe），容易看出：条带内各列的顺序以及各条带之间的顺序，对 N:M 稀疏性限制都没有影响。

[Pool & Yu (2021)](https://proceedings.neurips.cc/paper/2021/hash/6e8404c3b93a9527c8db241a1846599a-Abstract.html) 提出了一种迭代贪心算法来寻找最优置换，使 N:M 稀疏性下的权重幅值最大化。所有通道对都被试探性地交换，只采纳使幅值增加最大的那一次交换，从而生成一个新的置换并完成一次迭代。贪心算法可能只找到局部极小值，因此他们引入了两种跳出局部极小的技术：

1. 有界回退（bounded regressions）：实践中随机交换两个通道，最多进行固定次数。解搜索被限制在仅一次通道交换的深度，以保持搜索空间广而浅。
2. 窄而深的搜索：选择多个条带并同时优化。

![](https://lilianweng.github.io/posts/2023-01-10-inference-optimization/N-to-M-sparsity-permutation-algo.png)

*以贪心且迭代的方式为 N:M 稀疏性寻找最佳置换的算法。（图片来源：Pool & Yu 2021）*

与按默认通道顺序剪枝相比，先对网络做置换再剪枝可以取得更好的性能。

为了从零训练具有 N:M 稀疏性的模型，[Zhou & Ma, et al. (2021)](https://arxiv.org/abs/2102.04010) 扩展了 STE（直通估计器，Straight-Through Estimator；[Bengio et al. 2013](https://arxiv.org/abs/1308.3432)）——它通常用于模型量化中的反向传播更新——使其适用于幅度剪枝和稀疏参数更新。

STE 计算稠密参数相对于剪枝后网络 $\widetilde{W}$ 的梯度 $\partial \mathcal{L}/\partial \widetilde{W}$，并将其作为近似应用到稠密网络 $W$ 上：

$$
W_{t+1} \gets W_t - \gamma \frac{\partial\mathcal{L}}{\partial\widetilde{W}}
$$

扩展版本 **SR-STE**（Sparse-refined STE）按下式更新稠密权重 $W$：

$$
W_{t+1} \gets W_t - \gamma \frac{\partial\mathcal{L}}{\partial\widetilde{W}}  + \lambda_W (\bar{\mathcal{E}} \odot W_t)
$$

其中 $\bar{\mathcal{E}}$ 是 $\widetilde{W}$ 的掩码矩阵，$\odot$ 表示逐元素相乘。提出 SR-STE 是为了防止二值掩码发生大幅变化，具体做法是：(1) 限制 $\widetilde{W}_t$ 中被剪权重的取值，(2) 促进 $\widetilde{W}_t$ 中未被剪的权重。

![](https://lilianweng.github.io/posts/2023-01-10-inference-optimization/SR-STE.png)

*STE 与 SR-STE 的对比。$\odot$ 是逐元素乘积，$\otimes$ 是矩阵乘法。（图片来源：Zhou & Ma, et al. 2021）*

与 STE 或 SR-STE 不同，**Top-KAST**（[Jayakumar et al. 2021](https://arxiv.org/abs/2106.03517)）方法可以在整个训练过程中（前向和反向传播都）保持恒定的稀疏度，同时不需要以稠密参数或稠密梯度做前向传播。

在训练步 $t$，Top-KAST 的处理流程如下：

1. *稀疏前向传播*：选取参数子集 $A^t \subset \Theta$，其中包含每层按幅值排名的 top-$K$ 参数，并限制在权重的前 $D$ 比例之内。时刻 $t$ 的参数化 $\alpha^t$ 会把不在 $A^t$（活跃权重）中的参数置零。

$$
\alpha^t_i = \begin{cases}
\theta^t_i & \text{ if } i \in A^t = \{i \mid \theta^t_i \in \text{TopK}(\theta^t, D) \}\\ 
0 & \text{ otherwise}
\end{cases}
$$

其中 $\text{TopK}(\theta, x)$ 基于幅值从 $\theta$ 中选出前 $x$ 比例的权重。

2. *稀疏反向传播*：然后将梯度应用到一个更大的参数子集 $B \subset \Theta$ 上，其中 $B$ 包含 $(D+M)$ 比例的权重且 $A \subset B$。更新更大比例的权重能更有效地探索不同的剪枝掩码，从而更有可能在处于前 $D$ 比例的活跃权重中引起名次变动。

$$
\Delta_{\theta^t_i} = \begin{cases}
-\eta \nabla_{\alpha_t} \mathcal{L}(y, x, \alpha^t)_i & \text{ if } i\in  B^t = \{i \mid \theta^t_i \in \text{TopK}(\theta^t, D+M) \} \\
0 & \text{ otherwise }
\end{cases}
$$

训练被分为两个阶段，集合 $B \setminus A$ 中多出的坐标控制引入多少探索。探索量应在训练过程中逐渐减少，掩码最终趋于稳定。

![](https://lilianweng.github.io/posts/2023-01-10-inference-optimization/Top-KAST-stabilize.png)

*Top-KAST 的剪枝掩码随时间趋于稳定。（图片来源：Jayakumar et al. 2021）*

为防止“强者愈强”（rich-get-richer）现象，Top-KAST 通过 L2 正则化损失惩罚活跃权重的幅值，以鼓励对新条目的更多探索。$B \setminus A$ 中的参数比 $A$ 中的受到更强惩罚，以便在更新时维持更高的入选门槛，从而稳定掩码。

$$
L_\text{penalty}(\alpha^t_i) = \begin{cases}
\vert \theta^t_i\vert  & \text{ if } i \in A^t \\ 
\vert \theta^t_i\vert / D  & \text{ if } i \in B^t \setminus A^t \\ 
0 & \text{ otherwise}
\end{cases}
$$

## 稀疏化 Transformer

*Scaling Transformer*（[Jaszczur et al. 2021](https://arxiv.org/abs/2111.12763)）对 transformer 架构中的自注意力层和 FFN 层都进行了稀疏化，在单样本推理上实现了 37 倍加速。

![](https://lilianweng.github.io/posts/2023-01-10-inference-optimization/scaling-transformer-speedup-table.png)

*对不同层施加稀疏化时，transformer 模型解码单个 token（非批处理推理）的速度。（图片来源：Jaszczur et al. 2021）*

**稀疏 FFN 层**：每个 FFN 层包含两个 MLP，中间夹一个 ReLU。由于 ReLU 会引入大量零，他们对激活值施加固定结构，强制每 $N$ 个元素组成的一块中只有 1 个非零值。稀疏模式是动态的，每个 token 各不相同。

$$
\begin{aligned}
Y_\text{sparse} &= \max(0, xW_1 + b_1) \odot \text{Controller}(x) \\
\text{SparseFFN}(x) &= Y_\text{sparse} W_2 + b_2 \\
\text{Controller}(x) &= \arg\max(\text{Reshape}(x C_1 C_2, (-1, N)))
\end{aligned}
$$

其中 $Y_\text{sparse}$ 中的每个激活值对应 $W_1$ 的一列和 $W_2$ 的一行。控制器实现为一个低秩瓶颈稠密层，$C_1 \in \mathbb{R}^{d_\text{model} \times d_\text{lowrank}}, C_2 \in \mathbb{R}^{d_\text{lowrank} \times d_\text{ff}}$，且 $d_\text{lowrank} = d_\text{model} / N$。推理时它用 $\arg\max$ 选择哪些列应为非零，训练时用 Gumbel-softmax 技巧（[Jang et al. 2016](https://arxiv.org/abs/1611.01144)）。由于我们可以在加载 FFN 权重矩阵之前先计算 $\text{Controller}(x)$，就能提前知道哪些列会被置零，从而选择*不把这些列加载*进内存，以加速推理。

![](https://lilianweng.github.io/posts/2023-01-10-inference-optimization/sparse-FFN.png)

*(a) 稀疏 FFN 层；红色列不会被加载进内存以加速推理。(b) 用于 1:4 稀疏化的稀疏 FFN 控制器。（图片来源：Jaszczur et al. 2021）\*翁荔注\*：论文插图中的 (a) 实际上是 $Y_\text{sparse} = \max\big(0, (xW_1 + b_1) \odot \text{Controller}(x)\big)$，但这不影响结果。*

**稀疏 QKV（注意力）层**：在注意力层中，维度 $d_\text{model}$ 被划分为 $S$ 个模块，每个大小为 $M=d_\text{model} /S$。为确保每个子块都能访问嵌入的任意部分，Scaling Transformer 引入了乘法层（multiplicative layer；即把来自多个神经网络层的输入逐元素相乘的层），它可以表示任意置换，但参数比稠密层更少。

给定输入向量 $x \in \mathbb{R}^{d_\text{model}}$，乘法层输出 $y \in \mathbb{R}^{S \times M}$：

$$
y_{s,m} = \sum_i x_i D_{i,s} E_{i,m}
\quad\text{where }D \in \mathbb{R}^{d_\text{model} \times S}, D \in \mathbb{R}^{d_\text{model} \times M}
$$

乘法层的输出是一个尺寸为 $\in \mathbb{R}^{\text{batch size}\times \text{length} \times S \times M}$ 的张量，随后由一个二维卷积层处理，其中 $\text{length}$ 和 $S$ 被视为图像的高和宽。这样的卷积层进一步减少了注意力层的参数量和计算时间。

![](https://lilianweng.github.io/posts/2023-01-10-inference-optimization/sparse-QKV.png)

*(a) 引入乘法层，使各分区都能访问嵌入的任意部分。(b) 乘法稠密层与二维卷积层的组合减少了注意力层的参数量和计算时间。（图片来源：Jaszczur et al. 2021）*

为了更好地处理长序列，Scaling Transformer 进一步配备了来自 [Reformer](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/#locality-sensitive-hashing-reformer)（[Kitaev, et al. 2020](https://arxiv.org/abs/2001.04451)）的 LSH（局部敏感哈希）注意力以及 FFN 块循环，由此得到 *Terraformer*。

## 专家混合

专家混合（MoE）模型依赖一组“专家”网络，每个样本只激活其中一部分网络来得到预测。这一思想最早可追溯至 20 世纪 90 年代（[Jacobs et al. 1991](https://www.cs.toronto.edu/~hinton/absps/jjnh91.pdf)），与集成方法密切相关。关于如何把 MoE 模块引入 transformer 的细节，请参阅我[之前关于大模型训练技巧的文章](https://lilianweng.github.io/posts/2021-09-25-train-large/)以及 [Fedus et al. 2022](https://arxiv.org/abs/2209.01667) 的 MoE 综述论文。

采用 MoE 架构时，解码时刻只使用部分参数，因此可以节省推理成本。每个专家的容量可以用超参数——容量因子 $C$——来调节，专家容量定义为：

$$
\text{Expert capacity} = \text{round}(C \cdot k \cdot \frac{\text{total # tokens in one batch}}{\text{# experts}})
$$

其中每个 token 选出 top-$k$ 个专家。$C$ 越大，专家容量越高、性能越好，但计算开销也更大。当 $C>1$ 时，会加入富余容量；反之，当 $C<1$ 时，路由网络需要忽略一些 token。

### 路由策略改进

MoE 层有一个路由网络，为每个输入 token 分配一个专家子集。朴素 MoE 模型中的路由策略是按 token 出现的自然顺序，把它们分别路由到各自偏好的专家。如果某个 token 被路由到已达容量的专家，该 token 就会被标记为*“溢出并跳过”*。

**V-MoE**（Vision MoE；[Riquelme et al. 2021](https://arxiv.org/abs/2106.05974)）在 ViT（Vision Transformer）中加入 MoE 层。它匹配了此前 SoTA 的性能，却只需*一半*的推理计算。V-MoE 可以扩展到 15B 参数。他们的实验使用 $k=2$、32 个专家以及每隔一层的专家布置（意思是每两层放置一个 MoE）。

由于每个专家的容量有限，一些重要且信息量大的 token 如果在预定义的序列顺序中出现得太晚（例如句子中词的顺序，或图像 patch 的顺序），就可能不得不被丢弃。为避免朴素路由方案的这一缺陷，V-MoE 采用**批优先路由（Batch Priority Routing，BPR）**，先把专家分配给优先级得分高的 token。BPR 在分配专家前为每个 token 计算一个优先级得分（top-$k$ 路由得分的最大值或总和），并据此调整 token 的顺序。这保证了专家容量缓冲区会先被关键 token 填满。

![](https://lilianweng.github.io/posts/2023-01-10-inference-optimization/BPR.png)

*当 $C < 1$ 时，图像 patch 如何依据优先级得分被丢弃。（图片来源：Riquelme et al. 2021）*

在 $C\leq 0.5$ 时（此时模型开始丢弃大量 token），BPR 明显优于朴素路由。它使模型即使在相当低的容量下也能与稠密网络相抗衡。

在考察如何解释图像类别-专家关联时，他们观察到：靠前的 MoE 层更通用，而靠后的 MoE 层可能专门针对少数几个图像类别。

**Task MoE**（Task-level Mixture-of-Experts；[Kudugunta et al. 2021](https://arxiv.org/abs/2110.03742)）把任务信息纳入考虑，在机器翻译中按*任务*级别而非词或 token 级别路由。他们以 MNMT（多语言神经机器翻译）为例，根据目标语言或语言对对翻译任务分组。

token 级路由是动态的，每个 token 的路由决策彼此独立地做出。因此，推理时服务器需要预加载所有专家。相比之下，在任务固定的情况下，任务级路由是*静态*的，因此单个任务的推理服务器只需预加载 $k$ 个专家（假设采用 top-$k$ 路由）。根据他们的实验，与稠密模型基线相比，Task MoE 能取得与 token MoE 相当的性能提升，同时峰值吞吐量提高 2.6 倍，解码器规模仅为原来的 1.6%。

任务级 MoE 本质上是按照预定义的*启发式规则*对任务分布进行分类，并把这种人类知识融入路由器。当这类启发式规则不存在时（例如考虑一般的句子续写任务），如何利用 Task MoE 就不那么直接了。

**PR-MoE**（Pyramid residual MoE；[Rajbhandari et al. 2022](https://arxiv.org/abs/2201.05596)）让每个 token 经过一个固定的 MLP 和一个选中的专家。基于“靠后的层加 MoE 更有利”的观察，PR-MoE 在靠后的层采用更多专家。DeepSpeed 库实现了灵活的多专家、多数据并行，以支持训练各层专家数量不同的 PR-MoE。

![](https://lilianweng.github.io/posts/2023-01-10-inference-optimization/PR-MoE.png)

*PR-MoE 架构与标准 MoE 的对比示意图。（图片来源：Rajbhandari et al. 2022）*

### 算子改进

专家网络可以托管在不同设备上。然而，随着 GPU 数量增加，每块 GPU 上的专家数减少，专家之间的通信（“all-to-all”）开销变得越来越高。跨多块 GPU 的专家间 all-to-all 通信依赖 NCCL 的 P2P API，而后者在大规模场景下无法跑满高速链路（如 NVLink、HDR InfiniBand）的带宽，因为使用的节点越多，单个数据块就越小。现有的 all-to-all 算法在大规模、小负载的场景下表现不佳。为了实现更高效的 MoE 计算，出现了各种各样的算子改进，例如让 all-to-all 通信更便宜、更快速。

*DeepSpeed* 库（[Rajbhandari et al. 2022](https://arxiv.org/abs/2201.05596)）和 TUTEL（[Hwang et al. 2022](https://arxiv.org/abs/2206.03382)）都实现了基于树的**层级式 all-to-all**算法：先运行节点内 all-to-all，再运行节点间 all-to-all。它把通信跳数从 $O(G)$ 降低到 $O(G_\text{node} + G / G_\text{node})$，其中 $G$ 是 GPU 节点总数，$G_\text{node}$ 是每节点的 GPU 核数。尽管这种实现的通信量翻倍，但由于批量较小时瓶颈在延迟而非通信带宽，它在大规模小批量场景下的扩展性更好。

*DynaMoE*（[Kossmann et al. 2022](https://arxiv.org/abs/2205.01848)）使用**动态重编译**（dynamic recompilation）让计算资源适配专家间的动态负载。`RECOMPILE` 机制从头编译计算图，并且只在需要时才重新分配资源。它测量分配给每个专家的样本数量，并动态调整它们的容量因子 $C$，以降低运行时的内存和计算需求。基于样本-专家分配在训练早期就收敛的观察，收敛之后引入*样本分配缓存*，再用 `RECOMPILE` 来消除门控网络与专家之间的依赖。

# 架构优化

关于*高效 Transformer*（Efficient Transformers）的综述论文（[Tay et al. 2020](https://arxiv.org/abs/2009.06732)）回顾了一系列为了更好的*计算与内存效率*而改进的新 transformer 架构，强烈推荐一读。你也可以看看我的文章[《The Transformer Family Version 2.0》](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/)，其中深入介绍了多种多样的 transformer 架构改进，包括让模型运行更省钱的改动。

![](https://lilianweng.github.io/posts/2023-01-10-inference-optimization/efficient-transformer.png)

*高效 transformer 模型的分类。（图片来源：Tay et al. 2020）*

由于自注意力机制具有平方级的时间和内存复杂度，而这正是提升 transformer 解码效率的主要瓶颈，所有高效 transformer 模型都对本应稠密的注意力层施加了某种形式的稀疏化。这里只给出高层次的概览，其中若干条衍生自 [Tay et al. 2020](https://arxiv.org/abs/2009.06732)。

## 稀疏注意力模式

1. *固定模式*（Fixed Patterns）使用预定义的固定模式来限制注意力矩阵的视野。

   - 把输入序列切成固定块，例如[块级注意力（Blockwise Attention）](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/##strided-context)；
   - [Image Transformer](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/##fixed-local-context) 使用局部注意力；
   - [Sparse Transformer](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/##strided-context) 使用带步长的注意力模式。
2. *组合模式*（Combined Patterns）通过学习对输入 token 排序/聚类——在保留固定模式效率优势的同时，获得对序列更优的全局视野。

   - [Sparse Transformer](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/#sparse-attention-matrix-factorization-sparse-transformers) 结合了带步长注意力与局部注意力；
   - 给定高维输入张量时，[Axial Transformer](https://arxiv.org/abs/1912.12180) 不对展平后的输入施加注意力，而是施加多个注意力，每个沿输入张量的单个轴进行。
   - [ETC、Longformer 与 Big Bird](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/#combination-of-local-and-global-context) 结合了局部与全局上下文，以及带步长或随机注意力。
3. *可学习模式*（Learnable Patterns）通过学习来识别最优注意力模式。

   - [Reformer](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/#content-based-attention) 基于哈希相似度（LSH）把 token 聚成簇；
   - [Routing Transformer](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/#content-based-attention) 对 token 运行 $k$ 均值聚类；
   - [Sinkhorn Sorting Network](https://arxiv.org/abs/2002.11296) 学习对输入序列的块排序。

## 循环

循环（recurrence）机制通过循环把多个块/段连接起来。

- [Transformer-XL](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/#context-memory) 通过在段之间复用隐状态来利用更长的上下文。
- [Universal Transformer](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/#make-it-recurrent) 把自注意力与 RNN 的循环机制相结合。
- [Compressive Transformer](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/#context-memory) 是 Transformer-XL 的扩展，带有额外的记忆：一组存放过往激活值的记忆槽，以及一组存放压缩激活值的压缩记忆槽。每当模型接收一个新的输入段，主记忆中最老的激活值就会被移入压缩记忆并施加压缩函数。

## 省内存设计

省内存设计指为使用更少内存而对架构做出的改动。

- [Linformer](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/#low-rank-attention) 把键和值的长度维度投影到低维表示（$N \to k$），从而把内存复杂度从 $N \times N$ 降低到 $N \times k$。
- [Shazeer (2019)](https://arxiv.org/abs/1911.02150) 提出了*多查询注意力*（multi-query attention），让不同注意力“头”共享键和值，大幅减少了这些张量的尺寸和内存开销。
- [随机特征注意力与 Performer](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/#low-rank-attention) 使用[核方法（kernel methods）]((https://lilianweng.github.io/posts/2022-09-08-ntk/#kernel--kernel-methods))来得到一种数学上更廉价的自注意力机制形式。

## 自适应注意力

*自适应注意力*（adaptive attention）使模型能够学习最优的注意力跨度，或者针对不同的输入 token 决定何时提前退出（early exiting）。

- [Adaptive Attention Span](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/#adaptive-attention-span) 通过 token 与其他键之间的软掩码，训练模型逐 token、逐头地学习最优注意力跨度。
- [Universal Transformer](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/#make-it-recurrent) 引入循环机制，并使用 [ACT（自适应计算时间）](https://lilianweng.github.io/posts/2020-04-07-the-transformer-family/#adaptive-computation-time-act)来动态决定循环步数。
- [Depth-Adaptive Transformer 与 CALM](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/#depth-adaptive-transformer) 利用置信度度量逐 token 地学习何时提前退出计算层，以取得良好的性能-效率折中。

# 引用

引用方式：

> Weng, Lilian. (Jan 2023). Large Transformer Model Inference Optimization. Lil'Log. https://lilianweng.github.io/posts/2023-01-10-inference-optimization/.

或

```
@article{weng2023inference,
  title   = "Large Transformer Model Inference Optimization",
  author  = "Weng, Lilian",
  journal = "Lil'Log",
  year    = "2023",
  month   = "Jan",
  url     = "https://lilianweng.github.io/posts/2023-01-10-inference-optimization/"
}
```

# 参考文献

[1] Bondarenko et al. [“Understanding and overcoming the challenges of efficient transformer quantization”](https://arxiv.org/abs/2109.12948) ACL 2021.

[2] Dettmers et al. [“LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale”](https://arxiv.org/abs/2208.07339) NeuriPS 2022

[3] Zadeh et al. [“Gobo: Quantizing attention-based NLP models for low latency and energy efficient inference.”](https://arxiv.org/abs/2005.03842) MICRO 2020

[4] Shen, Dong & Ye, et al. [“Q-BERT: Hessian based ultra low precision quantization of BERT”](https://arxiv.org/abs/1909.05840) AAAI 2020.

[5] Yao et al. [“ZeroQuant: Efficient and affordable post-training quantization for large-scale transformers”](https://arxiv.org/abs/2206.01861) arXiv preprint arXiv:2206.01861 (2022).

[6] Frantar et al. [“GPTQ: Accurate Quantization for Generative Pre-trained Transformers”](https://arxiv.org/abs/2210.17323) arXiv preprint arXiv:2210.17323 (2022).

[7] Xiao & Lin [“SmoothQuant: Accelerated sparse neural training: A provable and efficient method to find N:M transposable masks.”](https://arxiv.org/abs/2211.10438) arXiv preprint arXiv:2211.10438 (2022). | [code](https://github.com/mit-han-lab/smoothquant)

[8] Pool & Yu. [“Channel Permutations for N:M Sparsity.”](https://proceedings.neurips.cc/paper/2021/hash/6e8404c3b93a9527c8db241a1846599a-Abstract.html) NeuriPS 2021. | [code](https://github.com/NVIDIA/apex/tree/master/apex/contrib/sparsity)

[9] Zhou & Ma, et al. [“Learning N:M fine-grained structured sparse neural networks from scratch.”](https://arxiv.org/abs/2102.04010) arXiv preprint arXiv:2102.04010 (2021).

[10] Jayakumar et al. [“Top-KAST: Top-K Always Sparse Training.”](https://arxiv.org/abs/2106.03517) NeuriPS 2020.

[11] Nvidia. [“Nvidia A100 tensor core GPU architecture.”](https://images.nvidia.com/aem-dam/en-zz/Solutions/data-center/nvidia-ampere-architecture-whitepaper.pdf) 2020.

[12] Gale, Elsen & Hooker [“The State of Sparsity in Deep Neural Networks.”](https://arxiv.org/abs/1902.09574) arXiv preprint arXiv:1902.09574 (2019).

[13] Zhu & Gupta. [“To Prune, or Not to Prune: Exploring the Efficacy of Pruning for Model Compression.”](https://arxiv.org/abs/1710.01878) arXiv preprint arXiv:1710.01878 (2017).

[14] Renda et al. [“Comparing rewinding and fine-tuning in neural network pruning.”](https://arxiv.org/abs/2003.02389) arXiv preprint arXiv:2003.02389 (2020).

[15] Zhou & Ma, et al. [“Learning N:M fine-grained structured sparse neural networks from scratch.”](https://arxiv.org/abs/2102.04010) arXiv preprint arXiv:2102.04010 (2021).

[16] Pool & Yu. [“Channel Permutations for N:M Sparsity.”](https://proceedings.neurips.cc/paper/2021/hash/6e8404c3b93a9527c8db241a1846599a-Abstract.html) NeuriPS 2021. | [code](https://github.com/NVIDIA/apex/tree/master/apex/contrib/sparsity)

[17] Jaszczur et al. [“Sparse is Enough in Scaling Transformers.”](https://arxiv.org/abs/2111.12763) NeuriPS 2021.

[18] Mishra et al. [“An Survey of Neural Network Compression.”](https://arxiv.org/abs/2010.03954) arXiv preprint arXiv:1710.09282 (2017).

[19] Fedus et al. [“A Review of Sparse Expert Models in Deep Learning.”](https://arxiv.org/abs/2209.01667) arXiv preprint arXiv:2209.01667 (2022)..

[20] Riquelme et al. [“Scaling vision with sparse mixture of experts.”](https://arxiv.org/abs/2106.05974) NeuriPS 2021.

[21] Kudugunta et al. [“Beyond Distillation: Task-level Mixture-of-Experts for Efficient Inference.”](https://arxiv.org/abs/2110.03742) arXiv preprint arXiv:2110.03742 (2021).

[22] Rajbhandari et al. [“DeepSpeed-MoE: Advancing mixture-of-experts inference and training to power next-generation ai scale.”](https://arxiv.org/abs/2201.05596) arXiv preprint arXiv:2201.05596 (2022).

[23] Kossmann et al. [“Optimizing mixture of experts using dynamic recompilations.”](https://arxiv.org/abs/2205.01848) arXiv preprint arXiv:2205.01848 (2022).

[24] Hwang et al. [“Tutel: Adaptive mixture-of-experts at scale.”](https://arxiv.org/abs/2206.03382) arXiv preprint arXiv:2206.03382 (2022). | [code](https://github.com/microsoft/tutel)

[25] Noam Shazeer. [“Fast Transformer Decoding: One Write-Head is All You Need.”](https://arxiv.org/abs/1911.02150) arXiv preprint arXiv:1911.02150 (2019).

[26] Tay et al. [“Efficient Transformers: A Survey.”](https://arxiv.org/abs/2009.06732) ACM Computing Surveys 55.6 (2022): 1-28.

[27] Pope et al. [“Efficiently Scaling Transformer Inference.”](https://arxiv.org/abs/2211.05102) arXiv preprint arXiv:2211.05102 (2022).

[28] Frankle & Carbin. [“The Lottery Ticket Hypothesis: Finding Sparse, Trainable Neural Networks”](https://arxiv.org/abs/1803.03635) ICLR 2019.

[29] Elabyad et al. [“Depth-Adaptive Transformer”](https://arxiv.org/abs/1910.10073) ICLR 2020.

[30] Schuster et al. [“Confident Adaptive Language Modeling”](https://arxiv.org/abs/2207.07061) arXiv preprint arXiv:2207.07061 (2022).

[31] Gou et al. [“https://arxiv.org/abs/2006.05525”](https://arxiv.org/abs/2006.05525) arXiv preprint arXiv:2006.05525 (2020).

[32] Hinton et al. [“Distilling the Knowledge in a Neural Network”](https://arxiv.org/abs/1503.02531) NIPS 2014.

[33] Sanh et al. [“DistilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter”](https://arxiv.org/abs/1910.01108) Workshop on Energy Efficient Machine Learning and Cognitive Computing @ NeuriPS 2019.
