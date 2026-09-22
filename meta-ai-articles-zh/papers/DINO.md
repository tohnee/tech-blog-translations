---
title: "自监督视觉 Transformer 中的涌现特性"
title_en: "Emerging Properties in Self-Supervised Vision Transformers"
arxiv: 2104.14294
date: 2021-04-29
source: https://arxiv.org/abs/2104.14294
crawled: 2026-09-22
translated: 2026-09-22
---

# 自监督视觉 Transformer 中的涌现特性

> 原文：[Emerging Properties in Self-Supervised Vision Transformers](https://arxiv.org/abs/2104.14294) · Meta AI（FAIR）arXiv

Mathilde Caron　Hugo Touvron　Ishan Misra　Hervé Jegou　Julien Mairal　Piotr Bojanowski　Armand Joulin

（Facebook AI Research　Inria*　Sorbonne University）

∗Univ. Grenoble Alpes, Inria, CNRS, Grenoble INP, LJK, 38000 Grenoble, France.

联系方式：mathilde@fb.com

代码：<https://github.com/facebookresearch/dino>

###### 摘要

在本文中，我们提出这样一个问题：自监督学习是否会为视觉 Transformer（Vision Transformer，ViT）[10] 带来与卷积网络（convnet）相比脱颖而出的新特性。除了将自监督方法适配到这一架构的效果尤其出色之外，我们还得到以下观察：首先，自监督 ViT 特征显式包含图像语义分割的信息，这一特性在监督 ViT 或卷积网络中都不会如此清晰地涌现。其次，这些特征本身也是出色的 k-NN 分类器，使用小型 ViT 即可在 ImageNet 上达到 78.3% 的 Top-1 准确率。我们的研究还强调了动量编码器 [13]、多裁剪（multi-crop）训练 [3] 以及在 ViT 中使用小图块（patch）的重要性。我们将这些发现实现为一个简单的自监督方法，称为 DINO，可以将其解释为一种无标签的自蒸馏（self-distillation with no labels）形式。我们用 ViT-Base 在 ImageNet 线性评估中取得 80.1% 的 Top-1 准确率，展示了 DINO 与 ViT 之间的协同效应。

![图 1](2104.14294v2/attn6.png)

图 1：无监督训练的、使用 8×8 图块的视觉 Transformer 的自注意力。我们观察最后一层各头部上 [CLS] 词元（token）的自注意力。该词元不与任何标签或监督绑定。这些注意力图表明，模型自动学到了类别特定的特征，从而实现无监督的物体分割。

## 1 引言

Transformer [70] 最近成为卷积神经网络（convnet）在视觉识别中的一种替代方案 [10, 25, 83]。它的采用伴随着一种受自然语言处理（NLP）启发的训练策略，即先在海量数据上预训练，再在目标数据集上微调 [9, 55]。由此得到的视觉 Transformer（ViT）[10] 已可与卷积网络竞争，但尚未展现出相对后者的明显优势：它们计算开销更大、需要更多训练数据，其特征也未表现出独有的特性。

在本文中，我们质疑：Transformer 在视觉领域不温不火的成功，是否可以归因于其预训练中使用了监督。我们的动机是，Transformer 在 NLP 中成功的主要要素之一是自监督预训练，例如 BERT 中的完形填空任务（close procedure）[9] 或 GPT 中的语言建模 [55]。这些自监督预训练目标利用句子中的词来构造前置任务（pretext task），提供了比「每个句子预测单一标签」的监督目标更丰富的学习信号。类似地，在图像领域，图像级监督往往将图像包含的丰富视觉信息压缩为一个从几千个预定义物体类别中挑选出的单一概念 [21]。

虽然 NLP 中使用的自监督前置任务是文本特定的，但许多现有自监督方法已经在卷积网络的图像任务上展现了潜力 [3, 4, 12, 13]。它们通常共享相似的结构，只是用于避免平凡解（塌缩，collapse）或提升性能的组件不同 [7]。在本工作中，受这些方法启发，我们研究自监督预训练对 ViT 特征的影响。我们特别识别出若干在监督 ViT 或卷积网络中都不会涌现的有趣特性：

- 自监督 ViT 特征显式包含场景布局，尤其是物体边界，如图 1 所示。这一信息可直接从最后一个块（block）的自注意力模块中获取。
- 自监督 ViT 特征配合一个基本的最近邻分类器（k-NN）表现尤为出色，**无需任何微调、线性分类器或数据增强**，即可在 ImageNet 上达到 78.3% 的 Top-1 准确率。

分割掩码的涌现似乎是自监督方法共有的特性。然而，k-NN 上的优异性能只有在组合某些组件（如动量编码器 [13] 与多裁剪增强 [3]）时才会涌现。我们研究的另一项发现是：在 ViT 中使用更小的图块对提升所得特征的质量十分重要。

总体而言，我们关于这些组件重要性的发现促使我们设计了一种简单的自监督方法，可以将其解释为一种无标签的知识蒸馏 [35] 形式。由此得到的框架 DINO 通过标准的交叉熵损失让学生网络直接预测教师网络的输出，从而简化了自监督训练，其中教师网络由动量编码器构建。有趣的是，我们的方法只需对教师输出做中心化（centering）和锐化（sharpening）即可避免塌缩，而其他常用组件（如预测器 [12]、高级归一化 [3] 或对比损失 [13]）在稳定性或性能上几乎没有额外收益。尤为重要的是，我们的框架足够灵活，同时适用于卷积网络和 ViT，无需修改架构，也无需适配内部归一化 [58]。

我们进一步验证 DINO 与 ViT 的协同效应：在 ImageNet 线性分类基准上，使用小图块的 ViT-Base 取得 80.1% 的 Top-1 准确率，超越了以往的自监督特征。我们还确认 DINO 适用于卷积网络——用 ResNet-50 架构达到与当前最优相当的水平。最后，我们讨论了在计算和内存受限的情形下使用 DINO 训练 ViT 的几种方案。特别地，用两台 8-GPU 服务器训练 DINO ViT 只需 3 天即可在 ImageNet 线性基准上达到 76.1%，以显著降低的计算需求超越了规模相当的自监督卷积网络系统 [3, 12]。

图 2：无标签自蒸馏。为简单起见，我们以单对视图（$x_{1}$、$x_{2}$）为例展示 DINO。模型将同一输入图像的两种不同随机变换分别送入学生网络和教师网络。两个网络架构相同但参数不同。教师网络的输出用 batch 上计算的均值进行中心化。每个网络输出一个 $K$ 维特征，并在特征维度上用带温度的 softmax 归一化。随后用交叉熵损失度量二者的相似度。我们对教师施加停止梯度（sg）算子，使梯度只经由学生传播。教师参数用学生参数的指数移动平均（ema）更新。

## 2 相关工作

##### 自监督学习。

大量自监督工作聚焦于被称为「实例分类」（instance classification）的判别式方法 [4, 20, 13, 27]，它把每张图像视为一个不同的类别，训练模型在数据增强之下区分它们。然而，显式学习一个区分所有图像的分类器 [20] 无法随图像数量很好地扩展。Wu et al. [27] 提出使用噪声对比估计（NCE）[32] 来比较实例而非对实例分类。这种做法的一个缺陷是需要同时比较大量图像的特征。实践中这需要大 batch [4] 或记忆库 [13, 27]。若干变体允许以聚类的形式自动分组实例 [2, 8, 2, 36, 42, 74, 80, 85]。

最近的工作表明，我们可以在不区分图像的情况下学习无监督特征。其中尤为值得关注的是，Grill et al. [12] 提出一种称为 BYOL 的度量学习形式，通过将特征与动量编码器得到的表示相匹配来训练特征。像 BYOL 这样的方法即使没有动量编码器也能工作，只是性能会有所下降 [7, 12]。其他若干工作呼应了这一方向，表明可以匹配更复杂的表示 [26, 27]、训练特征去逼近均匀分布 [6]，或使用白化 [23, 81]。我们的方法受 BYOL 启发，但使用不同的相似度匹配损失，且学生与教师使用完全相同的架构。如此，我们的工作延续了 BYOL 开启的解读——将自监督学习视为一种无标签的 Mean Teacher 自蒸馏 [24]。

##### 自训练与知识蒸馏。

自训练（self-training）旨在通过把一小组初始标注传播到大量无标注实例来提升特征质量。这种传播可以通过标签的硬分配 [41, 78, 79] 或软分配 [76] 完成。使用软标签时，该方法通常被称为知识蒸馏 [7, 35]，其最初的设计目的是训练小网络模仿大网络的输出以压缩模型。Xie et al. [76] 表明蒸馏可用于在自训练流水线中向无标注数据传播软伪标签，建立了自训练与知识蒸馏之间的本质联系。我们的工作建立在这一关系之上，将知识蒸馏扩展到没有任何标签可用的情形。以往的工作也组合过自监督学习与知识蒸馏 [25, 63, 5, 47]，实现了自监督模型的压缩与性能增益。然而，这些工作依赖一个**预先训练好的**固定教师，而我们的教师在训练过程中动态构建。如此一来，知识蒸馏不再作为自监督预训练的后处理步骤，而是被直接改造为一种自监督目标。最后，我们的工作也与协同蒸馏（codistillation）[1] 相关，其中学生与教师架构相同并在训练中使用蒸馏。但协同蒸馏中的教师也在从学生蒸馏，而在我们的工作中教师由学生的平均来更新。

## 3 方法

### 3.1 基于知识蒸馏的自监督学习

本工作使用的框架 DINO 与近期的自监督方法 [3, 7, 4, 12, 13] 共享相同的总体结构。不过，我们的方法也与知识蒸馏 [35] 有相似之处，因此我们从这一角度来介绍它。我们在图 2 中展示 DINO，并在算法 1 中给出伪代码实现。

知识蒸馏是一种学习范式：训练学生网络 $g_{\theta_{s}}$ 去匹配给定教师网络 $g_{\theta_{t}}$ 的输出，两者分别由参数 $\theta_{s}$ 和 $\theta_{t}$ 参数化。给定输入图像 $x$，两个网络输出 $K$ 维概率分布，记为 $P_{s}$ 与 $P_{t}$。概率 $P$ 由网络 $g$ 的输出经 softmax 函数归一化得到。更精确地说，

$$
P_{s}(x)^{(i)}=\frac{\exp(g_{\theta_{s}}(x)^{(i)}/\tau_{s})}{\sum_{k=1}^{K}\exp(g_{\theta_{s}}(x)^{(k)}/\tau_{s})},\tag{1}
$$

其中 $\tau_{s}>0$ 是控制输出分布锐度的温度参数，$P_{t}$ 也有类似的公式，温度为 $\tau_{t}$。给定固定的教师网络 $g_{\theta_{t}}$，我们通过最小化关于学生网络参数 $\theta_{s}$ 的交叉熵损失来学习匹配这些分布：

$$
\min_{\theta_{s}}H(P_{t}(x),P_{s}(x)),\tag{2}
$$

其中 $H(a,b)=-a\log b$。

在下文中，我们详述如何将式 (2) 适配到自监督学习。首先，我们用多裁剪策略 [3] 构造同一图像的不同失真视图（裁剪）。更精确地说，从给定图像生成包含不同视图的集合 $V$。该集合包含两个**全局**视图 $x^{g}_{1}$、$x^{g}_{2}$，以及若干较小分辨率的**局部**视图。所有裁剪都送入学生，而只有**全局**视图送入教师，从而鼓励「局部到全局」的对应关系。我们最小化损失：

$$
\min_{\theta_{s}}\sum_{x\in\{x^{g}_{1},x^{g}_{2}\}}\quad\sum_{\begin{subarray}{c}x^{\prime}\in V\\ x^{\prime}\neq\,x\end{subarray}}\quad H(P_{t}(x),P_{s}(x^{\prime})).\tag{3}
$$

算法 1　DINO 的 PyTorch 伪代码（不含 multi-crop）。

```python
# gs, gt: student and teacher networks
# C: center (K)
# tps, tpt: student and teacher temperatures
# l, m: network and center momentum rates
gt.params = gs.params
for x in loader: # load a minibatch x with n samples
    x1, x2 = augment(x), augment(x) # random views

    s1, s2 = gs(x1), gs(x2) # student output n-by-K
    t1, t2 = gt(x1), gt(x2) # teacher output n-by-K

    loss = H(t1, s2)/2 + H(t2, s1)/2
    loss.backward() # back-propagate

    # student, teacher and center updates
    update(gs) # SGD
    gt.params = l*gt.params + (1-l)*gs.params
    C = m*C + (1-m)*cat([t1, t2]).mean(dim=0)

def H(t, s):
    t = t.detach() # stop gradient
    s = softmax(s / tps, dim=1)
    t = softmax((t - C) / tpt, dim=1) # center + sharpen
    return - (t * log(s)).sum(dim=1).mean()
```

该损失是通用的，可用于任意数量的视图，甚至只用 2 个。不过我们遵循 multi-crop 的标准设置：使用 2 个分辨率为 $224^{2}$、覆盖原图较大区域（例如大于 50%）的全局视图，以及若干分辨率为 $96^{2}$、仅覆盖原图较小区域（例如小于 50%）的局部视图。除非另有说明，我们将这一设置称为 DINO 的基本参数化。

两个网络共享同一架构 $g$，但参数集 $\theta_{s}$ 与 $\theta_{t}$ 不同。我们通过随机梯度下降最小化式 (3) 来学习参数 $\theta_{s}$。

##### 教师网络。

与知识蒸馏不同，我们没有**事先**给定的教师 $g_{\theta_{t}}$，因此我们从学生网络的过往迭代中构建它。我们在第 5.2 节研究教师的不同更新规则，并表明在我们的框架中，将教师网络冻结一个 epoch 的效果出人意料地好，而把学生权重复制给教师则无法收敛。尤为值得关注的是，对学生权重使用指数移动平均（EMA），即动量编码器 [13]，特别适合我们的框架。更新规则为 $\theta_{t}\leftarrow\lambda\theta_{t}+(1-\lambda)\theta_{s}$，其中 $\lambda$ 在训练期间按余弦调度从 0.996 增至 1 [12]。动量编码器最初是作为对比学习中队列的替代品被提出的 [13]。但在我们的框架中，它的作用有所不同，因为我们既没有队列也没有对比损失，其角色可能更接近自训练中使用的平均教师（mean teacher）[24]。事实上，我们观察到该教师执行的是一种带指数衰减的 Polyak-Ruppert 平均式的模型集成 [20, 59]。使用 Polyak-Ruppert 平均做模型集成是提升模型性能的标准做法 [38]。我们观察到，该教师在整个训练过程中都优于学生，因而通过提供更高质量的目标特征来引导学生的训练。这种动态在此前的工作 [12, 58] 中未被观察到。

表 1：网络配置。「Blocks」是 Transformer 块的数量，「dim」是通道维度，「heads」是多头注意力的头数。「# tokens」是按 $224^{2}$ 分辨率输入考虑的词元序列长度，「# params」是参数总量（不计投影头），「im/s」是在 NVIDIA V100 GPU 上每次前向 128 个样本的推理时间。

| 模型 | blocks | dim | heads | # tokens | # params | im/s |
| --- | --- | --- | --- | --- | --- | --- |
| ResNet-50 | – | 2048 | – | – | 23M | 1237 |
| ViT-S/16 | 12 | 384 | 6 | 197 | 21M | 1007 |
| ViT-S/8 | 12 | 384 | 6 | 785 | 21M | 180 |
| ViT-B/16 | 12 | 768 | 12 | 197 | 85M | 312 |
| ViT-B/8 | 12 | 768 | 12 | 785 | 85M | 63 |

##### 网络架构。

神经网络 $g$ 由主干 $f$（ViT [10] 或 ResNet [34]）和投影头 $h$ 组成：$g=h\circ f$。用于下游任务的特征是主干 $f$ 的输出。投影头由一个 3 层多层感知机（MLP）构成，隐藏维度为 2048，后接 $\ell_{2}$ 归一化和一个带权重归一化的全连接层 [22]，输出 $K$ 维，这与 SwAV [3] 的设计类似。我们测试过其他投影头，这一特定设计对 DINO 效果最好（附录 C）。我们不使用预测器 [12, 7]，因此学生和教师网络的架构完全相同。尤为值得关注的是，与标准卷积网络不同，ViT 架构默认不使用批归一化（BN）。因此，将 DINO 应用于 ViT 时，投影头中我们也不使用任何 BN，使系统**完全不含 BN（entirely BN-free）**。

##### 避免塌缩。

若干自监督方法的差别在于用于避免塌缩的操作：或通过对比损失 [27]、聚类约束 [8, 3]、预测器 [12]，或通过批归一化 [12, 58]。虽然我们的框架可以用多种归一化 [3] 来稳定，但它也可以只靠对动量教师的输出做中心化和锐化来避免模型塌缩。如第 5.3 节的实验所示，中心化可防止单一维度占主导，但会鼓励塌缩到均匀分布，而锐化的作用恰好相反。同时施加两种操作可平衡二者的效应，足以在存在动量教师的情况下避免塌缩。选择这种避免塌缩的方法，是以牺牲部分稳定性来换取对 batch 的更小依赖：中心化操作只依赖一阶 batch 统计量，可解释为给教师添加一个偏置项 $c$：$g_{t}(x)\leftarrow g_{t}(x)+c$。中心 $c$ 用指数移动平均更新，使该方法在不同 batch 大小下都表现良好，见第 5.5 节：

$$
c\leftarrow mc+(1-m)\frac{1}{B}\sum_{i=1}^{B}g_{\theta_{t}}(x_{i}),\tag{4}
$$

其中 $m>0$ 是速率参数，$B$ 是 batch 大小。输出锐化通过在教师 softmax 归一化中使用较低的温度值 $\tau_{t}$ 来实现。

### 3.2 实现与评估协议

在本节中，我们给出用 DINO 训练的实现细节，并介绍实验中使用的评估协议。

##### 视觉 Transformer。

我们简要描述视觉 Transformer（ViT）的机制 [10, 70]，关于 Transformer 的细节请参阅 Vaswani et al. [70]，关于其对图像的适配请参阅 Dosovitskiy et al. [10]。我们沿用 DeiT [25] 中的实现。我们在表 1 中汇总本文所用不同网络的配置。ViT 架构以一组互不重叠、分辨率 $N\times N$ 的连续图像图块作为输入。本文通常使用 $N=16$（「/16」）或 $N=8$（「/8」）。图块随后经过一个线性层，形成一组嵌入。我们向序列中添加一个额外的可学习词元 [9, 10]。该词元的作用是聚合整个序列的信息，我们在其输出上接投影头 $h$。为与以往工作 [9, 10, 25] 保持一致，我们将该词元称为类词元 [CLS]，尽管在我们的情形中它不与任何标签或监督绑定。图块词元集合与 [CLS] 词元一起被送入一个带「pre-norm」层归一化的标准 Transformer 网络 [11, 39]。Transformer 是一系列自注意力层与前馈层的堆叠，并配有跳跃连接。自注意力层通过注意力机制观察其他词元的表示来更新词元的表示 [4]。

##### 实现细节。

我们在 ImageNet 数据集 [21] 上不带标签地预训练模型。使用 ViT-S/16 时，我们用 adamw 优化器 [44] 训练，batch 大小为 1024，分布在 16 块 GPU 上。学习率在前 10 个 epoch 内线性升温至由以下线性缩放规则 [29] 确定的基准值：$lr=0.0005*\text{batchsize}/256$。预热之后，学习率按余弦调度衰减 [43]。权重衰减同样按余弦调度从 0.04 升至 0.4。温度 $\tau_{s}$ 设为 0.1，而 $\tau_{t}$ 在前 30 个 epoch 内从 0.04 线性预热至 0.07。我们沿用 BYOL [12] 的数据增强（颜色抖动、高斯模糊与日光化）以及 multi-crop [3]，并用双三次插值将位置嵌入适配到不同尺度 [10, 25]。复现我们结果的代码和模型已公开可得。

##### 评估协议。

自监督学习的标准协议，要么是在冻结特征上学习线性分类器 [82, 13]，要么是在下游任务上微调特征。对于线性评估，我们在训练期间施加随机尺寸裁剪与水平翻转增强，并在中心裁剪上报告准确率。对于微调评估，我们用预训练权重初始化网络并在训练中适配。然而，这两种评估都对超参数敏感，例如改变学习率时，我们在多次运行之间观察到较大的准确率方差。因此，我们还用一个简单的加权最近邻分类器（k-NN）来评估特征质量，如 [27] 所做。我们冻结预训练模型，计算并存储下游任务训练数据的特征。最近邻分类器随后将一张图像的特征与 $k$ 个最近的已存储特征匹配，由后者对标签投票。我们扫描了不同数量的最近邻，发现在我们大多数运行中 20 个 NN 始终效果最好。这一评估协议不需要任何其他超参数调优，也不需要数据增强，只需在下游数据集上跑一遍即可完成，极大地简化了特征评估。

表 2：ImageNet 上的线性与 k-NN 分类。我们报告不同自监督方法在 ImageNet 验证集上线性与 k-NN 评估的 Top-1 准确率。我们聚焦 ResNet-50 与 ViT-small 架构，但也报告跨架构取得的最佳结果。带 ∗ 的是我们运行的。我们对官方发布权重的模型运行 k-NN 评估。吞吐量（im/s）在 NVIDIA V100 GPU 上以每次前向 128 个样本计算。参数量（M）为特征提取器的参数量。

| 方法 | 架构 | 参数 | im/s | 线性 | k-NN |
| --- | --- | --- | --- | --- | --- | --- |
| 监督 | RN50 | 23 | 1237 | 79.3 | 79.3 |
| SCLR [4] | RN50 | 23 | 1237 | 69.1 | 60.7 |
| MoCov2 [6] | RN50 | 23 | 1237 | 71.1 | 61.9 |
| InfoMin [67] | RN50 | 23 | 1237 | 73.0 | 65.3 |
| BarlowT [81] | RN50 | 23 | 1237 | 73.2 | 66.0 |
| OBoW [27] | RN50 | 23 | 1237 | 73.8 | 61.9 |
| BYOL [12] | RN50 | 23 | 1237 | 74.4 | 64.8 |
| DCv2 [3] | RN50 | 23 | 1237 | 75.2 | 67.1 |
| SwAV [3] | RN50 | 23 | 1237 | 75.3 | 65.7 |
| DINO | RN50 | 23 | 1237 | 75.3 | 67.5 |
| 监督 | ViT-S | 21 | 1007 | 79.8 | 79.8 |
| BYOL∗ [12] | ViT-S | 21 | 1007 | 71.4 | 66.6 |
| MoCov2∗ [6] | ViT-S | 21 | 1007 | 72.7 | 64.4 |
| SwAV∗ [3] | ViT-S | 21 | 1007 | 73.5 | 66.3 |
| DINO | ViT-S | 21 | 1007 | 77.0 | 74.5 |
| 跨架构比较 | | | | | |
| SCLR [4] | RN50w4 | 375 | 117 | 76.8 | 69.3 |
| SwAV [3] | RN50w2 | 93 | 384 | 77.3 | 67.3 |
| BYOL [12] | RN50w2 | 93 | 384 | 77.4 | – |
| DINO | ViT-B/16 | 85 | 312 | 78.2 | 76.1 |
| SwAV [3] | RN50w5 | 586 | 76 | 78.5 | 67.1 |
| BYOL [12] | RN50w4 | 375 | 117 | 78.6 | – |
| BYOL [12] | RN200w2 | 250 | 123 | 79.6 | 73.9 |
| DINO | ViT-S/8 | 21 | 180 | 79.7 | 78.3 |
| SCLRv2 [5] | RN152w3+SK | 794 | 46 | 79.8 | 73.1 |
| DINO | ViT-B/8 | 85 | 63 | 80.1 | 77.4 |

## 4 主要结果

我们首先在 ImageNet 标准自监督基准上验证本研究使用的 DINO 框架。然后研究所得特征在检索、物体发现和迁移学习上的特性。

### 4.1 在 ImageNet 上与其他 SSL 框架比较

我们考虑两种不同设置：同架构比较与跨架构比较。

##### 同架构比较。

在表 2 的上半部分，我们以相同架构（ResNet-50 [34] 或遵循 DeiT-S [25] 设计的 ViT-small）将 DINO 与其他自监督方法比较。选择 ViT-S 的理由是它在多个维度与 ResNet-50 相近：参数量（21M 对 23M）、吞吐量（1237/秒 对 1007 im/秒）以及按 [25] 训练流程在 ImageNet 上的监督性能（79.3% 对 79.8%）。我们在附录 D 中探索 ViT-S 的变体。首先，我们观察到 DINO 在 ResNet-50 上与当前最优持平，验证了 DINO 在标准设置下有效。当切换到 ViT 架构时，DINO 以线性分类 +3.5%、k-NN 评估 +7.9% 的幅度超越 BYOL、MoCov2 与 SwAV。更令人惊讶的是，简单 k-NN 分类器的性能几乎与线性分类器持平（74.5% 对 77.0%）。这一特性只在 DINO 与 ViT 架构结合时才会涌现，在其他现有自监督方法或 ResNet-50 上都不会出现。

##### 跨架构比较。

在表 2 的下半部分，我们比较跨架构取得的最佳性能。这一设置的意义不在于直接比较方法，而在于评估用 DINO 训练的 ViT 在转向更大架构时的极限。用 DINO 训练更大的 ViT 可以提升性能，而缩小图块尺寸（「/8」变体）对性能的影响更大。缩小图块尺寸虽不增加参数，却仍会导致运行时间显著变慢和内存占用增大。尽管如此，用 DINO 训练的 8×8 图块 base ViT 在线性分类中达到 80.1% Top-1、k-NN 分类器下达到 77.4%，参数量比以往最优 [5] 少 10 倍，运行速度快 1.4 倍。

### 4.2 自监督训练的 ViT 的特性

我们从最近邻搜索、保留物体位置信息以及向下游任务的可迁移性三个方面评估 DINO 特性的质量。

表 3：图像检索。我们比较用监督或在 ImageNet 与 Google Landmarks v2（GLDv2）数据集上用 DINO 预训练的现成（off-the-shelf）特征在检索中的性能。我们报告 revisited Oxford 与 Paris 上的 mAP。在地标数据集上用 DINO 预训练的表现尤为出色。作为参考，我们还报告了使用现成特征的最佳检索方法 [57]。

| 预训练 | 架构 | 预训练数据 | ℛOx M | ℛOx H | ℛPar M | ℛPar H |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Sup. [57] | RN101+R-MAC | ImNet | 49.8 | 18.5 | 74.0 | 52.1 |
| 监督 | ViT-S/16 | ImNet | 33.5 | 8.9 | 63.0 | 37.2 |
| DINO | ResNet-50 | ImNet | 35.4 | 11.1 | 55.9 | 27.5 |
| DINO | ViT-S/16 | ImNet | 41.8 | 13.7 | 63.1 | 34.4 |
| DINO | ViT-S/16 | GLDv2 | 51.5 | 24.3 | 75.3 | 51.6 |

#### 4.2.1 DINO ViT 的最近邻检索

ImageNet 分类的结果已经揭示了我们的特征在依赖最近邻检索的任务上的潜力。在这组实验中，我们进一步在地标检索与拷贝检测任务上巩固这一结论。

##### 图像检索。

我们考虑 revisited Oxford 与 Paris 图像检索数据集 [53, 50]。它们包含 3 个难度递进的划分（split），由查询/图库对组成。我们报告 Medium（M）与 Hard（H）划分的平均精度均值（mAP）。在表 3 中，我们比较由监督或 DINO 训练得到的不同**现成**特征的性能。我们冻结特征并直接用 k-NN 做检索。我们观察到 DINO 特征优于在 ImageNet 上带标签训练的特征。

自监督方法的一个优势是可以在任意数据集上训练，而不需要任何形式的标注。我们在 Google Landmarks v2（GLDv2）[72] 的 1.2M 干净子集上训练 DINO，这是一个为检索目的设计的地标数据集。在 GLDv2 上训练的 DINO ViT 特非常出色，超越了以往发表的基于现成描述子的方法 [68, 57]。

表 4：拷贝检测。我们报告在 Copydays「strong」子集 [21] 上拷贝检测的 mAP 性能。作为参考，我们还报告专门为特定物体检索训练的 multigrain 模型 [5] 的性能。

| 方法 | 架构 | 维度 | 分辨率 | mAP |
| --- | --- | --- | --- | --- | --- |
| Multigrain [5] | ResNet-50 | 2048 | $224^{2}$ | 75.1 |
| Multigrain [5] | ResNet-50 | 2048 | 最长边 800 | 82.5 |
| 监督 [25] | ViT-B/16 | 1536 | $224^{2}$ | 76.4 |
| DINO | ViT-B/16 | 1536 | $224^{2}$ | 81.7 |
| DINO | ViT-B/8 | 1536 | $320^{2}$ | 85.5 |

##### 拷贝检测。

我们还评估用 DINO 训练的 ViT 在拷贝检测任务上的性能。我们报告 INRIA Copydays 数据集 [21]「strong」子集上的平均精度均值。该任务是识别经过模糊、插入、打印扫描等失真处理的图像。遵循先前工作 [5]，我们额外加入从 YFCC100M 数据集 [66] 随机采样的 1 万张干扰图像。我们直接用余弦相似度在预训练网络得到的特征上执行拷贝检测。特征由输出 [CLS] 词元与 GeM 池化 [54] 的输出图块词元拼接得到。这为 ViT-B 得到一个 1536 维描述子。遵循 [5]，我们对特征施加白化。我们在 YFCC100M 的另外 2 万张随机图像上学习这一变换，与干扰图像互不重叠。表 4 表明用 DINO 训练的 ViT 在拷贝检测上极具竞争力。

表 5：DAVIS 2017 视频物体分割。我们评估冻结特征在视频实例跟踪上的质量。我们报告平均区域相似度 $\mathcal{J}_{m}$ 与平均基于轮廓的准确率 $\mathcal{F}_{m}$。我们与现有自监督方法以及在 ImageNet 上监督训练的 ViT-S/8 比较。图像分辨率为 480p。

| 方法 | 数据 | 架构 | $(\mathcal{J}\&\mathcal{F})_{m}$ | $\mathcal{J}_{m}$ | $\mathcal{F}_{m}$ |
| --- | --- | --- | --- | --- | --- | --- |
| 监督 | | | | | |
| ImageNet | INet | ViT-S/8 | 66.0 | 63.9 | 68.1 |
| STM [18] | I/D/Y | RN50 | 81.8 | 79.2 | 84.3 |
| 自监督 | | | | | |
| CT [26] | VLOG | RN50 | 48.7 | 46.4 | 50.0 |
| MAST [15] | YT-VOS | RN18 | 65.5 | 63.3 | 67.6 |
| STC [14] | Kinetics | RN18 | 67.6 | 64.8 | 70.2 |
| DINO | INet | ViT-S/16 | 61.8 | 60.2 | 63.4 |
| DINO | INet | ViT-B/16 | 62.3 | 60.7 | 63.9 |
| DINO | INet | ViT-S/8 | 69.9 | 66.6 | 73.1 |
| DINO | INet | ViT-B/8 | 71.4 | 67.9 | 74.9 |

图 3：来自多个头部的注意力图。我们考察用 DINO 训练的 ViT-S/8 最后一层的各个头，并以 [CLS] 词元为查询展示其自注意力。不同的头（以不同颜色表示）关注代表不同物体或部位的不同位置（更多示例见附录）。

#### 4.2.2 发现场景的语义布局

如图 1 定性所示，我们的自注意力图包含图像分割的信息。在本研究中，我们既在标准基准上度量这一特性，也直接探测从这些注意力图生成的掩码的质量。

##### 视频实例分割。

在表 5 中，我们在 DAVIS-2017 视频实例分割基准 [52] 上评估输出的图块词元。我们遵循 Jabri et al. [14] 的实验协议，用相邻帧之间的最近邻来分割场景；因此我们没有在特征之上训练任何模型，也没有为该任务微调任何权重。我们在表 5 中观察到，尽管我们的训练目标和架构都不是为密集任务设计的，其在该基准上的表现仍具竞争力。由于网络未经微调，模型的输出必然保留了某些空间信息。最后，对这个密集识别任务，小图块变体（「/8」）的表现要好得多（ViT-B 的 $(\mathcal{J}\&\mathcal{F})_{m}$ 提升 +9.1%）。

##### 探测自注意力图。

在图 3 中，我们展示不同的头可以关注图像的不同语义区域，即使这些区域被遮挡（第三行的灌木丛）或很小（第二行的旗帜）。可视化使用 480p 图像，对应 ViT-S/8 的 3601 个词元组成的序列。在图 4 中，我们从定性和定量两方面表明，监督 ViT 在存在杂乱（clutter）时无法很好地关注物体。我们报告真值（ground truth）与通过阈值化自注意力图以保留 60% 质量所得分割掩码之间的 Jaccard 相似度。注意，自注意力图是平滑的且并非为产生掩码而优化。尽管如此，监督模型与 DINO 模型之间在 Jaccard 相似度上仍有明显差距。还要注意，自监督卷积网络也包含分割信息，但需要专门的方法才能从其权重中提取 [31]。

图 4：监督与 DINO 的分割对比。我们可视化对自注意力图做阈值化以保留 60% 质量所得的掩码。上方展示监督训练与 DINO 训练的 ViT-S/8 得到的掩码。我们为两个模型各展示表现最好的头。下方的表比较这些掩码与真值在 PASCAL VOC12 验证图像上的 Jaccard 相似度。

| | 随机 | 监督 | DINO |
| --- | --- | --- | --- |
| ViT-S/16 | 22.0 | 27.3 | 45.9 |
| ViT-S/8 | 21.8 | 23.7 | 44.7 |

#### 4.2.3 下游任务迁移学习

在表 6 中，我们评估用 DINO 预训练的特征在不同下游任务上的质量。我们与相同架构、在 ImageNet 上监督训练的特征比较。我们遵循 Touvron et al. [25] 的协议，在每个下游任务上微调特征。我们观察到，对 ViT 架构而言，自监督预训练的迁移效果优于监督训练的特征，这与在卷积网络上的观察一致 [3, 13, 62]。最后，自监督预训练显著提升了 ImageNet 上的结果（+1-2%）。

表 6：通过在不同数据集上微调预训练模型进行迁移学习。我们报告 Top-1 准确率。DINO 自监督预训练的迁移效果优于监督预训练。

| | Cifar10 | Cifar100 | INat18 | INat19 | Flwrs | Cars | INet |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ViT-S/16 | | | | | | | |
| 监督 [25] | 99.0 | 89.5 | 70.7 | 76.6 | 98.2 | 92.1 | 79.9 |
| DINO | 99.0 | 90.5 | 72.0 | 78.2 | 98.5 | 93.0 | 81.5 |
| ViT-B/16 | | | | | | | |
| 监督 [25] | 99.0 | 90.8 | 73.2 | 77.7 | 98.4 | 92.1 | 81.8 |
| DINO | 99.1 | 91.7 | 72.6 | 78.6 | 98.8 | 93.0 | 82.8 |

## 5 DINO 消融研究

在本节中，我们对应用于 ViT 的 DINO 进行实证研究。整个研究考虑的模型是 ViT-S。我们还请读者参阅附录以获得补充研究。

### 5.1 不同组件的重要性

我们展示在我们的框架中为 ViT 添加自监督学习不同组件的影响。

表 7：自监督 ViT 预训练的重要组件。模型为 ViT-S/16，训练 300 个 epoch。我们研究对 k-NN 与线性（「Lin.」）评估重要的不同组件。对不同变体，我们标出与 DINO 默认设置的差异。最佳组合是动量编码器 + multi-crop 增强 + 交叉熵损失。我们还报告 BYOL [12]、MoCo-v2 [6] 与 SwAV [3] 的结果。

| | 方法 | 动量 | SK | MC | 损失 | 预测器 | k-NN | Lin. |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | DINO | ✓ | ✗ | ✓ | CE | ✗ | 72.8 | 76.1 |
| 2 | | ✗ | ✗ | ✓ | CE | ✗ | 0.1 | 0.1 |
| 3 | | ✓ | ✓ | ✓ | CE | ✗ | 72.2 | 76.0 |
| 4 | | ✓ | ✗ | ✗ | CE | ✗ | 67.9 | 72.5 |
| 5 | | ✓ | ✗ | ✓ | MSE | ✗ | 52.6 | 62.4 |
| 6 | | ✓ | ✗ | ✓ | CE | ✓ | 71.8 | 75.6 |
| 7 | BYOL | ✓ | ✗ | ✗ | MSE | ✓ | 66.6 | 71.4 |
| 8 | MoCov2 | ✓ | ✗ | ✗ | INCE | ✗ | 62.0 | 71.6 |
| 9 | SwAV | ✗ | ✓ | ✓ | CE | ✗ | 64.7 | 71.8 |

SK：Sinkhorn-Knopp；MC：Multi-Crop（多裁剪）；Pred.：预测器
CE：交叉熵；MSE：均方误差；INCE：InfoNCE

在表 7 中，我们报告增删组件后的不同模型变体。首先，我们观察到没有动量时我们的框架无法工作（行 2），需要更高级的操作（例如 SK）来避免塌缩（行 9）。但在有动量的情况下，使用 SK 的影响很小（行 3）。此外，比较行 3 与行 9 突显了动量编码器对性能的重要性。其次，在行 4 与行 5 中，我们观察到 multi-crop 训练与 DINO 中的交叉熵损失是获得良好特征的重要组件。我们还观察到，给学生网络添加预测器的影响甚微（行 6），而它在 BYOL 中对防止塌缩至关重要 [7, 12]。为完整起见，我们在附录 B 中给出该消融研究的扩展版本。

##### 图块尺寸的重要性。

在图 5 中，我们比较使用不同图块尺寸（16×16、8×8 与 5×5）训练的 ViT-S 模型的 k-NN 分类性能。我们还与 16×16 和 8×8 图块的 ViT-B 比较。所有模型都训练 300 个 epoch。我们观察到随着图块尺寸减小，性能大幅提升。有趣的是，不增加任何额外参数也能大幅提升性能。然而，使用更小图块的性能增益以吞吐量为代价：使用 5×5 图块时，吞吐量降至 44 im/s，而 8×8 图块为 180 im/s。

图 5：图块尺寸的影响。以 ViT-B 与 ViT-S 的不同输入图块尺寸，k-NN 评估性能随吞吐量的变化。模型训练 300 个 epoch。

### 5.2 教师网络选择的影响

在本消融中，我们用不同的教师网络做实验，以理解其在 DINO 中的作用。我们比较训练 300 个 epoch 的模型，采用 k-NN 协议。

##### 从学生构建不同的教师。

在图 6（右）中，除动量教师外，我们比较从学生的过往版本构建教师的不同策略。首先考虑用上一个 epoch 的学生网络做教师。这一策略曾被用于记忆库 [27]，或作为一种聚类硬蒸馏 [8, 2, 14]。其次，考虑用上一次迭代的学生网络，以及直接复制学生作为教师。在我们的设置中，使用基于学生近期版本的教师无法收敛。这一设置需要更多归一化才能工作。有趣的是，我们观察到使用上一个 epoch 的教师不会塌缩，其 k-NN 评估性能与 MoCo-v2 或 BYOL 等现有框架相当。虽然动量编码器明显优于这种朴素教师，但这一发现表明，教师的设计仍有替代方案值得探索。

##### 分析训练动态。

为进一步理解动量教师为何在我们的框架中有效，我们在图 6 的左图中研究 ViT 训练期间它的动态。一个关键观察是：该教师在训练期间始终优于学生，并且用 ResNet-50 训练时我们也观察到同样行为（附录 D）。其他同样使用动量的框架 [13, 12] 以及教师取自上一个 epoch 的设置都未观察到这一行为。我们提出将 DINO 中的动量教师解释为一种带指数衰减的 Polyak-Ruppert 平均 [20, 59]。Polyak-Ruppert 平均常用于模拟模型集成，以在训练结束时提升网络的性能 [38]。我们的方法可解释为在训练过程中持续应用 Polyak-Ruppert 平均，来不断构建性能更优的模型集成。该模型集成随后引导学生网络的训练 [24]。

| 教师 | Top-1 |
| --- | --- |
| 学生副本 | 0.1 |
| 上一次迭代 | 0.1 |
| 上一个 epoch | 66.6 |
| 动量 | 72.8 |

图 6：用 k-NN 分类器在 ImageNet 验证集上的 Top-1 准确率。（左）训练期间动量教师与学生性能的比较。（右）不同类型教师网络的比较。动量编码器带来最佳性能，但并非唯一可行的选项。

### 5.3 避免塌缩

图 7：塌缩研究。（左）教师目标熵随训练 epoch 的演变；（右）教师与学生输出之间 KL 散度的演变。

我们研究中心化与目标锐化在避免塌缩上的互补作用。塌缩有两种形式：无论输入如何，模型输出在所有维度上均匀分布，或被单一维度主导。中心化避免了由主导维度引起的塌缩，但会鼓励均匀输出。锐化则引起相反的效果。我们通过将交叉熵 $H$ 分解为熵 $h$ 与 Kullback-Leibler 散度（「KL」）$D_{KL}$ 来展示这种互补性：

$$
H(P_{t},P_{s})=h(P_{t})+D_{KL}(P_{t}|P_{s}).\tag{5}
$$

KL 等于零表明输出恒定，即发生了塌缩。在图 7 中，我们绘制了有/无中心化与锐化时训练过程中的熵与 KL。如果缺少任一操作，KL 收敛到零，表明发生塌缩。但熵 $h$ 收敛到不同的值：无中心化时为 0，无锐化时为 $-\log(1/K)$，说明两种操作诱发不同形式的塌缩。同时施加两种操作可平衡这些效应（锐化参数 $\tau_{t}$ 的研究见附录 D）。

### 5.4 计算需求

表 8：时间与内存需求。我们展示在两台 8-GPU 机器上运行 ViT-S/16 DINO 模型的总运行时间与每 GPU 峰值内存（「mem.」）。我们对若干 multi-crop 变体报告线性评估的 ImageNet 验证 Top-1 准确率，每个变体的计算需求水平不同。

| | | 100 epochs | | | 300 epochs | | |
| --- | --- | --- | --- | --- | --- | --- | --- |
| multi-crop | | top-1 | 时间 | | top-1 | 时间 | 内存 |
| 2×$224^{2}$ | | 67.8 | 15.3h | | 72.5 | 45.9h | 9.3G |
| 2×$224^{2}$+2×$96^{2}$ | | 71.5 | 17.0h | | 74.5 | 51.0h | 10.5G |
| 2×$224^{2}$+6×$96^{2}$ | | 73.8 | 20.3h | | 75.9 | 60.9h | 12.9G |
| 2×$224^{2}$+10×$96^{2}$ | | 74.6 | 24.2h | | 76.1 | 72.6h | 15.4G |

在表 8 中，我们详述在两台 8-GPU 机器上运行 ViT-S/16 DINO 模型的时间与 GPU 内存需求。我们报告若干 multi-crop 训练变体的结果，每种的计算需求水平不同。我们在表 8 中观察到，使用 multi-crop 改善了 DINO 训练的准确率/运行时间权衡。例如，不用 multi-crop（即 2×$224^{2}$）时训练 46 小时后性能为 72.5%，而 2×$224^{2}$+10×$96^{2}$ 裁剪设置的 DINO 仅 24 小时就达到 74.6%。这相当于时间减半（所需的训练时间少 2 倍）仍提升 +2%，尽管内存占用更高（15.4G 对 9.3G）。我们观察到，2×$224^{2}$ 设置下更长的训练无法追平 multi-crop 带来的性能提升，这显示了「局部到全局」增强的价值。最后，对更长的训练，添加更多视图的收益递减（从 6 个增加到 10 个 $96^{2}$ 裁剪仅 +0.2%）。

总体而言，用两台 8-GPU 服务器训练 3 天，DINO 与视觉 Transformer 即可达到 76.1 的 Top-1 准确率。这一结果以显著降低的计算需求，超越了规模相当的最先进自监督卷积网络系统 [12, 3]。我们的代码可用于在有限数量的 GPU 上训练自监督 ViT。

### 5.5 小 batch 训练

| bs | 128 | 256 | 512 | 1024 |
| --- | --- | --- | --- | --- |
| top-1 | 57.9 | 59.1 | 59.6 | 59.9 |

表 9：batch 大小的影响。训练 100 个 epoch、无 multi-crop 的模型的 k-NN Top-1。

在表 9 中，我们研究 batch 大小对 DINO 所得特征的影响。我们还在附录 D 中研究式 (4) 中中心化更新规则所用平滑参数 $m$ 的影响。我们将学习率随 batch 大小线性缩放 [29]：$lr=0.0005*\text{batchsize}/256$。表 9 确认我们可以用小 batch 训练出高性能模型。较小 batch（bs=128）的结果略低于我们 bs=1024 的默认训练设置，且肯定需要重新调优动量速率等超参数。注意，batch 大小为 128 的实验仅在 1 块 GPU 上运行。我们还探索过用 batch 大小 8 训练模型，50 个 epoch 后达到 35.2%，显示了训练「每块 GPU 仅勉强放得下一张图像」的大型模型的潜力。

## 6 结论

在本工作中，我们展示了自监督预训练一个标准 ViT 模型的潜力，其性能可与专为此设置设计的最佳卷积网络相当。我们还看到涌现出两个可用于未来应用的特性：特征在 k-NN 分类中的质量显示出其在图像检索中的潜力，ViT 在该领域已展现出可喜的结果 [22]。特征中场景布局信息的存在也可惠及弱监督图像分割。然而，本文的主要结果是：我们有证据表明，自监督学习可能是基于 ViT 开发类 BERT 模型的关键。未来，我们计划探索用 DINO 在随机未筛选的图像上预训练大型 ViT 模型，看能否突破视觉特征的极限 [28]。

##### 致谢。

我们感谢 Mahmoud Assran、Matthijs Douze、Allan Jabri、Jure Zbontar、Alaaeldin El-Nouby、Y-Lan Boureau、Kaiming He、Thomas Lucas 以及 Thoth 与 FAIR 团队在本项目中给予的帮助、支持与讨论。Julien Mairal 受 ERC 拨款 714381（SOLARIS 项目）与 ANR 3IA MIAI@Grenoble Alpes（ANR-19-P3IA-0003）资助。

## 参考文献

- [1]

  Rohan Anil, Gabriel Pereyra, Alexandre Passos, Robert Ormandi, George E Dahl,
  and Geoffrey E Hinton.
  Large scale distributed neural network training through online
  distillation.
  arXiv preprint arXiv:1804.03235, 2018.
- [2]

  Yuki Markus Asano, Christian Rupprecht, and Andrea Vedaldi.
  Self-labelling via simultaneous clustering and representation
  learning.
  In ICLR, 2020.
- [3]

  Mahmoud Assran, Nicolas Ballas, Lluis Castrejon, and Michael Rabbat.
  Recovering petaflops in contrastive semi-supervised learning of
  visual representations.
  preprint arXiv:2006.10803, 2020.
- [4]

  Dzmitry Bahdanau, Kyunghyun Cho, and Yoshua Bengio.
  Neural machine translation by jointly learning to align and
  translate.
  preprint arXiv:1409.0473, 2014.
- [5]

  Maxim Berman, Hervé Jégou, Vedaldi Andrea, Iasonas Kokkinos, and
  Matthijs Douze.
  MultiGrain: a unified image embedding for classes and instances.
  arXiv preprint arXiv:1902.05509, 2019.
- [6]

  Piotr Bojanowski and Armand Joulin.
  Unsupervised learning by predicting noise.
  In ICML, 2017.
- [7]

  Cristian Buciluǎ, Rich Caruana, and Alexandru Niculescu-Mizil.
  Model compression.
  In SIGKDD, 2006.
- [8]

  Mathilde Caron, Piotr Bojanowski, Armand Joulin, and Matthijs Douze.
  Deep clustering for unsupervised learning of visual features.
  In ECCV, 2018.
- [9]

  Mathilde Caron, Piotr Bojanowski, Julien Mairal, and Armand Joulin.
  Unsupervised pre-training of image features on non-curated data.
  In ICCV, 2019.
- [10]

  Mathilde Caron, Ishan Misra, Julien Mairal, Priya Goyal, Piotr Bojanowski, and
  Armand Joulin.
  Unsupervised learning of visual features by contrasting cluster
  assignments.
  In NeurIPS, 2020.
- [11]

  Mia Xu Chen, Orhan Firat, Ankur Bapna, Melvin Johnson, Wolfgang Macherey,
  George Foster, Llion Jones, Niki Parmar, Mike Schuster, Zhifeng Chen, et al.
  The best of both worlds: Combining recent advances in neural machine
  translation.
  preprint arXiv:1804.09849, 2018.
- [12]

  Ting Chen, Simon Kornblith, Mohammad Norouzi, and Geoffrey Hinton.
  A simple framework for contrastive learning of visual
  representations.
  preprint arXiv:2002.05709, 2020.
- [13]

  Ting Chen, Simon Kornblith, Kevin Swersky, Mohammad Norouzi, and Geoffrey
  Hinton.
  Big self-supervised models are strong semi-supervised learners.
  In NeurIPS, 2020.
- [14]

  Weijie Chen, Shiliang Pu, Di Xie, Shicai Yang, Yilu Guo, and Luojun Lin.
  Unsupervised image classification for deep representation learning.
  arXiv preprint arXiv:2006.11480, 2020.
- [15]

  Xinlei Chen, Haoqi Fan, Ross Girshick, and Kaiming He.
  Improved baselines with momentum contrastive learning.
  preprint arXiv:2003.04297, 2020.
- [16]

  Xinlei Chen and Kaiming He.
  Exploring simple siamese representation learning.
  preprint arXiv:2011.10566, 2020.
- [17]

  Marco Cuturi.
  Sinkhorn distances: Lightspeed computation of optimal transport.
  In NeurIPS, 2013.
- [18]

  Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova.
  Bert: Pre-training of deep bidirectional transformers for language
  understanding.
  preprint arXiv:1810.04805, 2018.
- [19]

  Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov, Dirk Weissenborn,
  Xiaohua Zhai, Thomas Unterthiner, Mostafa Dehghani, Matthias Minderer, Georg
  Heigold, Sylvain Gelly, et al.
  An image is worth 16x16 words: Transformers for image recognition at
  scale.
  preprint arXiv:2010.11929, 2020.
- [20]

  Alexey Dosovitskiy, Philipp Fischer, Jost Tobias Springenberg, Martin
  Riedmiller, and Thomas Brox.
  Discriminative unsupervised feature learning with exemplar
  convolutional neural networks.
  TPAMI, 2016.
- [21]

  Matthijs Douze, Hervé Jégou, Harsimrat Sandhawalia, Laurent Amsaleg,
  and Cordelia Schmid.
  Evaluation of gist descriptors for web-scale image search.
  In CIVR, 2009.
- [22]

  Alaaeldin El-Nouby, Natalia Neverova, Ivan Laptev, and Hervé Jégou.
  Training vision transformers for image retrieval.
  preprint arXiv:2102.05644, 2021.
- [23]

  Aleksandr Ermolov, Aliaksandr Siarohin, Enver Sangineto, and Nicu Sebe.
  Whitening for self-supervised representation learning.
  preprint arXiv:2007.06346, 2020.
- [24]

  Mark Everingham, Luc Van Gool, Christopher KI Williams, John Winn, and Andrew
  Zisserman.
  The pascal visual object classes (voc) challenge.
  IJCV, 2010.
- [25]

  Zhiyuan Fang, Jianfeng Wang, Lijuan Wang, Lei Zhang, Yezhou Yang, and Zicheng
  Liu.
  Seed: Self-supervised distillation for visual representation.
  2021.
- [26]

  Spyros Gidaris, Andrei Bursuc, Nikos Komodakis, Patrick Pérez, and Matthieu
  Cord.
  Learning representations by predicting bags of visual words.
  In CVPR, 2020.
- [27]

  Spyros Gidaris, Andrei Bursuc, Gilles Puy, Nikos Komodakis, Matthieu Cord, and
  Patrick Pérez.
  Online bag-of-visual-words generation for unsupervised representation
  learning.
  arXiv preprint arXiv:2012.11552, 2020.
- [28]

  Priya Goyal, Mathilde Caron, Benjamin Lefaudeux, Min Xu, Pengchao Wang, Vivek
  Pai, Mannat Singh, Vitaliy Liptchinsky, Ishan Misra, Armand Joulin, et al.
  Self-supervised pretraining of visual features in the wild.
  preprint arXiv:2103.01988, 2021.
- [29]

  Priya Goyal, Piotr Dollár, Ross Girshick, Pieter Noordhuis, Lukasz
  Wesolowski, Aapo Kyrola, Andrew Tulloch, Yangqing Jia, and Kaiming He.
  Accurate, large minibatch sgd: Training imagenet in 1 hour.
  preprint arXiv:1706.02677, 2017.
- [30]

  Jean-Bastien Grill, Florian Strub, Florent Altché, Corentin Tallec,
  Pierre H Richemond, Elena Buchatskaya, Carl Doersch, Bernardo Avila Pires,
  Zhaohan Daniel Guo, Mohammad Gheshlaghi Azar, Bilal Piot, Koray Kavukcuoglu,
  Rémi Munos, and Michal Valko.
  Bootstrap your own latent: A new approach to self-supervised
  learning.
  In NeurIPS, 2020.
- [31]

  Shir Gur, Ameen Ali, and Lior Wolf.
  Visualization of supervised and self-supervised neural networks via
  attribution guided factorization.
  preprint arXiv:2012.02166, 2020.
- [32]

  Michael Gutmann and Aapo Hyvärinen.
  Noise-contrastive estimation: A new estimation principle for
  unnormalized statistical models.
  In International Conference on Artificial Intelligence and
  Statistics, 2010.
- [33]

  Kaiming He, Haoqi Fan, Yuxin Wu, Saining Xie, and Ross Girshick.
  Momentum contrast for unsupervised visual representation learning.
  In CVPR, 2020.
- [34]

  Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun.
  Deep residual learning for image recognition.
  In CVPR, 2016.
- [35]

  Geoffrey Hinton, Oriol Vinyals, and Jeff Dean.
  Distilling the knowledge in a neural network.
  preprint arXiv:1503.02531, 2015.
- [36]

  Jiabo Huang, Qi Dong, Shaogang Gong, and Xiatian Zhu.
  Unsupervised deep learning by neighbourhood discovery.
  In ICML, 2019.
- [37]

  Allan Jabri, Andrew Owens, and Alexei A Efros.
  Space-time correspondence as a contrastive random walk.
  2020.
- [38]

  Sébastien Jean, Kyunghyun Cho, Roland Memisevic, and Yoshua Bengio.
  On using very large target vocabulary for neural machine translation.
  preprint arXiv:1412.2007, 2014.
- [39]

  Guillaume Klein, Yoon Kim, Yuntian Deng, Jean Senellart, and Alexander M Rush.
  Opennmt: Open-source toolkit for neural machine translation.
  preprint arXiv:1701.02810, 2017.
- [40]

  Zihang Lai, Erika Lu, and Weidi Xie.
  Mast: A memory-augmented self-supervised tracker.
  In CVPR, 2020.
- [41]

  Dong-Hyun Lee et al.
  Pseudo-label: The simple and efficient semi-supervised learning
  method for deep neural networks.
  In Workshop on challenges in representation learning, ICML,
  2013.
- [42]

  Junnan Li, Pan Zhou, Caiming Xiong, and Steven C.H. Hoi.
  Prototypical contrastive learning of unsupervised representations.
  ICLR, 2021.
- [43]

  Ilya Loshchilov and Frank Hutter.
  Sgdr: Stochastic gradient descent with warm restarts.
  preprint arXiv:1608.03983, 2016.
- [44]

  Ilya Loshchilov and Frank Hutter.
  Fixing weight decay regularization in adam.
  2018.
- [45]

  Julien Mairal.
  Cyanure: An open-source toolbox for empirical risk minimization for
  python, c++, and soon more.
  preprint arXiv:1912.08165, 2019.
- [46]

  Maria-Elena Nilsback and Andrew Zisserman.
  Automated flower classification over a large number of classes.
  In 2008 Sixth Indian Conference on Computer Vision, Graphics &
  Image Processing, 2008.
- [47]

  Mehdi Noroozi, Ananth Vinjimoor, Paolo Favaro, and Hamed Pirsiavash.
  Boosting self-supervised learning via knowledge transfer.
  In CVPR, 2018.
- [48]

  Seoung Wug Oh, Joon-Young Lee, Ning Xu, and Seon Joo Kim.
  Video object segmentation using space-time memory networks.
  In ICCV, 2019.
- [49]

  Hieu Pham, Qizhe Xie, Zihang Dai, and Quoc V Le.
  Meta pseudo labels.
  preprint arXiv:2003.10580, 2020.
- [50]

  James Philbin, Ondrej Chum, Michael Isard, Josef Sivic, and Andrew Zisserman.
  Lost in quantization: Improving particular object retrieval in large
  scale image databases.
  In CVPR, 2008.
- [51]

  Boris T Polyak and Anatoli B Juditsky.
  Acceleration of stochastic approximation by averaging.
  SIAM journal on control and optimization, 30(4):838–855, 1992.
- [52]

  Jordi Pont-Tuset, Federico Perazzi, Sergi Caelles, Pablo Arbeláez, Alex
  Sorkine-Hornung, and Luc Van Gool.
  The 2017 davis challenge on video object segmentation.
  preprint arXiv:1704.00675, 2017.
- [53]

  Filip Radenović, Ahmet Iscen, Giorgos Tolias, Yannis Avrithis, and
  Ondřej Chum.
  Revisiting oxford and paris: Large-scale image retrieval
  benchmarking.
  2018.
- [54]

  Filip Radenović, Giorgos Tolias, and Ondřej Chum.
  Fine-tuning cnn image retrieval with no human annotation.
  IEEE transactions on pattern analysis and machine intelligence,
  2018.
- [55]

  Alec Radford, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei, and Ilya
  Sutskever.
  Language models are unsupervised multitask learners.
- [56]

  Ilija Radosavovic, Raj Prateek Kosaraju, Ross Girshick, Kaiming He, and Piotr
  Dollár.
  Designing network design spaces.
  In CVPR, 2020.
- [57]

  Jerome Revaud, Jon Almazán, Rafael S Rezende, and Cesar Roberto de Souza.
  Learning with average precision: Training image retrieval with a
  listwise loss.
  In ICCV, 2019.
- [58]

  Pierre H Richemond, Jean-Bastien Grill, Florent Altché, Corentin Tallec,
  Florian Strub, Andrew Brock, Samuel Smith, Soham De, Razvan Pascanu, Bilal
  Piot, et al.
  Byol works even without batch statistics.
  preprint arXiv:2010.10241, 2020.
- [59]

  David Ruppert.
  Efficient estimations from a slowly convergent robbins-monro process.
  Technical report, 1988.
- [60]

  Olga Russakovsky, Jia Deng, Hao Su, Jonathan Krause, Sanjeev Satheesh, Sean Ma,
  Zhiheng Huang, Andrej Karpathy, Aditya Khosla, Michael Bernstein, Alexander C
  Berg, and Li Fei-Fei.
  Imagenet large scale visual recognition challenge.
  IJCV, 2015.
- [61]

  Tim Salimans and Diederik P Kingma.
  Weight normalization: A simple reparameterization to accelerate
  training of deep neural networks.
  NeurIPS, 2016.
- [62]

  Mert Bulent Sariyildiz, Yannis Kalantidis, Diane Larlus, and Karteek Alahari.
  Concept generalization in visual representation learning.
  arXiv preprint arXiv:2012.05649, 2020.
- [63]

  Zhiqiang Shen, Zechun Liu, Jie Qin, Lei Huang, Kwang-Ting Cheng, and Marios
  Savvides.
  S2-bnn: Bridging the gap between self-supervised real and 1-bit
  neural networks via guided distribution calibration.
  arXiv preprint arXiv:2102.08946, 2021.
- [64]

  Kihyuk Sohn, David Berthelot, Chun-Liang Li, Zizhao Zhang, Nicholas Carlini,
  Ekin D Cubuk, Alex Kurakin, Han Zhang, and Colin Raffel.
  Fixmatch: Simplifying semi-supervised learning with consistency and
  confidence.
  In NeurIPS, 2020.
- [65]

  Antti Tarvainen and Harri Valpola.
  Mean teachers are better role models: Weight-averaged consistency
  targets improve semi-supervised deep learning results.
  preprint arXiv:1703.01780, 2017.
- [66]

  Bart Thomee, David A Shamma, Gerald Friedland, Benjamin Elizalde, Karl Ni,
  Douglas Poland, Damian Borth, and Li-Jia Li.
  Yfcc100m: The new data in multimedia research.
  arXiv preprint arXiv:1503.01817, 2015.
- [67]

  Yonglong Tian, Chen Sun, Ben Poole, Dilip Krishnan, Cordelia Schmid, and
  Phillip Isola.
  What makes for good views for contrastive learning.
  NeurIPS, 2020.
- [68]

  Giorgos Tolias, Ronan Sicre, and Hervé Jégou.
  Particular object retrieval with integral max-pooling of cnn
  activations.
  arXiv preprint arXiv:1511.05879, 2015.
- [69]

  Hugo Touvron, Matthieu Cord, Matthijs Douze, Francisco Massa, Alexandre
  Sablayrolles, and Hervé Jégou.
  Training data-efficient image transformers & distillation through
  attention.
  preprint arXiv:2012.12877, 2020.
- [70]

  Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones,
  Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin.
  Attention is all you need.
  In NeurIPS, 2017.
- [71]

  Xiaolong Wang, Allan Jabri, and Alexei A Efros.
  Learning correspondence from the cycle-consistency of time.
  In CVPR, 2019.
- [72]

  Tobias Weyand, Andre Araujo, Bingyi Cao, and Jack Sim.
  Google landmarks dataset v2-a large-scale benchmark for
  instance-level recognition and retrieval.
  2020.
- [73]

  Zhirong Wu, Yuanjun Xiong, Stella X Yu, and Dahua Lin.
  Unsupervised feature learning via non-parametric instance
  discrimination.
  In CVPR, 2018.
- [74]

  Junyuan Xie, Ross Girshick, and Ali Farhadi.
  Unsupervised deep embedding for clustering analysis.
  In ICML, 2016.
- [75]

  Qizhe Xie, Zihang Dai Dai, Eduard Hovy, Minh-Thang Luong, and Quoc V. Le.
  Unsupervised data augmentation for consistency training.
  preprint arXiv:1904.12848, 2020.
- [76]

  Qizhe Xie, Minh-Thang Luong, Eduard Hovy, and Quoc V Le.
  Self-training with noisy student improves imagenet classification.
  In CVPR, 2020.
- [77]

  Haohang Xu, Xiaopeng Zhang, Hao Li, Lingxi Xie, Hongkai Xiong, and Qi Tian.
  Seed the views: Hierarchical semantic alignment for contrastive
  representation learning.
  arXiv preprint arXiv:2012.02733, 2021.
- [78]

  Qiantong Xu, Tatiana Likhomanenko, Jacob Kahn, Awni Hannun, Gabriel Synnaeve,
  and Ronan Collobert.
  Iterative pseudo-labeling for speech recognition.
  preprint arXiv:2005.09267, 2020.
- [79]

  I Zeki Yalniz, Hervé Jégou, Kan Chen, Manohar Paluri, and Dhruv
  Mahajan.
  Billion-scale semi-supervised learning for image classification.
  preprint arXiv:1905.00546, 2019.
- [80]

  Jianwei Yang, Devi Parikh, and Dhruv Batra.
  Joint unsupervised learning of deep representations and image
  clusters.
  In CVPR, 2016.
- [81]

  Jure Zbontar, Li Jing, Ishan Misra, Yann LeCun, and Stéphane Deny.
  Barlow twins: Self-supervised learning via redundancy reduction.
  arXiv preprint arXiv:2103.03230, 2021.
- [82]

  Richard Zhang, Phillip Isola, and Alexei A Efros.
  Colorful image colorization.
  In ECCV, 2016.
- [83]

  Hengshuang Zhao, Jiaya Jia, and Vladlen Koltun.
  Exploring self-attention for image recognition.
  In CVPR, 2020.
- [84]

  Bolei Zhou, Agata Lapedriza, Jianxiong Xiao, Antonio Torralba, and Aude Oliva.
  Learning deep features for scene recognition using places database.
  In NeurIPS, 2014.
- [85]

  Chengxu Zhuang, Alex Lin Zhai, and Daniel Yamins.
  Local aggregation for unsupervised learning of visual embeddings.
  In ICCV, 2019.

## 附录

### A 补充结果

##### k-NN 分类。

在表 10 中，我们用线性与 k-NN 两种评估协议，评估由 DINO 预训练的 ResNet-50 或 ViT-small 给出的冻结表示。在两种评估中，我们都在不使用任何数据增强的情况下从预训练网络提取表示。然后，用加权 k-NN 或用 cyanure 库 [16] 学习的线性回归进行分类。在表 10 中我们看到，无论用线性还是 k-NN 分类器，ViT-S 的准确率都优于 RN50。但用 k-NN 评估时的性能差距比线性评估显著得多。例如在 ImageNet 1% 上，ViT-S 以 +14.1% 的大幅优势超越 ResNet-50（k-NN 评估）。这表明用 DINO 训练的 Transformer 架构或许能提供更有利于 k-NN 评估的模型灵活性。k-NN 分类器的巨大优势是部署快速且轻量，无需任何域适应。总体而言，用 DINO 训练的 ViT 提供了与 k-NN 分类器结合得特别好的特征。

表 10：以 DINO 预训练的 ViT-S/16 与 ResNet-50 的 k-NN 与线性评估。我们使用 ImageNet-1k [21]（「Inet」）、Places205 [29]、PASCAL VOC [11] 与 Oxford-102 flowers（「FLOWERS」）[17]。用 DINO 训练的 ViT 提供对 k-NN 特别友好的特征。

| | 逻辑回归 | | | | k-NN | | |
| --- | --- | --- | --- | --- | --- | --- | --- |
| | RN50 | ViT-S | Δ | | RN50 | ViT-S | Δ |
| Inet 100% | 72.1 | 75.7 | 3.6 | | 67.5 | 74.5 | 7.0 |
| Inet 10% | 67.8 | 72.2 | 4.4 | | 59.3 | 69.1 | 9.8 |
| Inet 1% | 55.1 | 64.5 | 9.4 | | 47.2 | 61.3 | 14.1 |
| Pl. 10% | 53.4 | 52.1 | -1.3 | | 46.9 | 48.6 | 1.7 |
| Pl. 1% | 46.5 | 46.3 | -0.2 | | 39.2 | 41.3 | 2.1 |
| VOC07 | 88.9 | 89.2 | 0.3 | | 84.9 | 88.0 | 3.1 |
| FLOWERS | 95.6 | 96.4 | 0.8 | | 87.9 | 89.1 | 1.2 |
| 平均 Δ | | | 2.4 | | | | 5.6 |

表 11：不同预训练下的 ImageNet 分类。监督 ViT-B/16 模型在不同预训练、或使用一个额外预训练卷积网络引导训练下的 ImageNet Top-1 准确率。各方法使用不同的图像分辨率（「res.」）与训练流程（「tr. proc.」，即数据增强与优化）。「MPP」指掩码图块预测（Masked Patch Prediction）。

| 预训练 | | | | | |
| --- | --- | --- | --- | --- | --- |
| 方法 | 数据 | | res. | tr. proc. | Top-1 |
| 在额外数据上预训练 | | | | | |
| MMP | JFT-300M | | 384 | [10] | 79.9 |
| 监督 | JFT-300M | | 384 | [10] | 84.2 |
| 使用额外模型训练 | | | | | |
| 随机初始化 | - | | 224 | [25] | 83.4 |
| 无额外数据与模型 | | | | | |
| 随机初始化 | - | | 224 | [10] | 77.9 |
| 随机初始化 | - | | 224 | [25] | 81.8 |
| 监督 | ImNet | | 224 | [25] | 81.9 |
| DINO | ImNet | | 224 | [25] | 82.8 |

##### ViT 的自监督 ImageNet 预训练。

在本实验中，我们研究用我们的方法预训练一个监督 ViT 模型的影响。在表 11 中，我们比较以不同预训练初始化、或在训练中由额外预训练卷积网络引导的监督 ViT 模型的性能。第一组模型在由 3 亿张图像组成的大型筛选数据集上做有/无监督预训练。第二组模型从预训练监督 RegNetY [56] 做硬知识蒸馏。最后一组模型不使用任何额外数据或模型，或随机初始化，或在 ImageNet 上以 DINO 预训练后初始化。与随机初始化相比，DINO 预训练带来 +1% 的性能增益。这并非由更长的训练造成，因为用监督代替 DINO 做预训练并不能提升性能。自监督预训练缩小了与「在额外数据上预训练」或「从卷积网络蒸馏」的模型之间的差距。

##### ImageNet 上的少样本学习。

我们评估将 DINO 应用于 ViT-S 所得特征在少样本（low-shot）学习上的表现。在表 12 中，我们报告在带 1% 与 10% 标签的冻结特征（frozen）上训练逻辑回归的验证准确率。逻辑回归用 cyanure 库 [16] 训练。在参数量与 images/sec 相近的模型之间比较时，我们观察到我们的特征与最先进的半监督模型相当。有趣的是，这一性能是通过在**冻结特征上**训练多类逻辑回归得到的——**无需数据增强、无需微调**。

表 12：用冻结 ViT 特征在 ImageNet 上做少样本学习。我们在冻结特征上训练逻辑回归（frozen）。注意，这一冻结评估是在**不做任何微调、不做数据增强**的情况下进行的。我们报告 Top-1 准确率。作为参考，我们列出以往使用微调与半监督学习的发表结果。

| | | | Top 1 | |
| --- | --- | --- | --- | --- |
| 方法 | 架构 | 参数 | 1% | 10% |
| 自监督预训练 + 微调 | | | | |
| UDA [28] | RN50 | 23 | – | 68.1 |
| SimCLRv2 [5] | RN50 | 23 | 57.9 | 68.4 |
| BYOL [12] | RN50 | 23 | 53.2 | 68.8 |
| SwAV [3] | RN50 | 23 | 53.9 | 70.2 |
| SimCLRv2 [7] | RN50w4 | 375 | 63.0 | 74.4 |
| BYOL [12] | RN200w2 | 250 | 71.2 | 77.7 |
| 半监督方法 | | | | |
| SimCLRv2+KD [5] | RN50 | 23 | 60.0 | 70.5 |
| SwAV+CT [1] | RN50 | 23 | – | 70.8 |
| FixMatch [23] | RN50 | 23 | – | 71.5 |
| MPL [19] | RN50 | 23 | – | 73.9 |
| SimCLRv2+KD [5] | RN152w3+SK | 794 | 76.6 | 80.9 |
| 冻结的自监督特征 | | | | |
| DINO -frozen | ViT-S/16 | 21 | 64.5 | 72.2 |

图 8：一组参考点的自注意力。我们可视化用 DINO 训练的 ViT-S/8 最后一块的自注意力模块。尽管完全没有使用监督训练，该网络仍能分离物体。

### B 方法比较

我们比较不同自监督框架 MoCo-v2 [6]、SwAV [3] 与 BYOL [12] 在卷积网络或 ViT 上的性能。在表 13 中，我们看到用 ResNet-50（卷积网络）训练时，DINO 与 SwAV、BYOL 表现相当。但 DINO 在 ViT 上充分释放了潜力，以大幅优势超越 MoCo-v2、SwAV 与 BYOL（线性评估 +4.3%，k-NN 评估 +6.2%）。在本节余下部分，我们做消融以更好地理解 DINO 应用于 ViT 的性能。特别地，我们与使用动量编码器的方法（即 MoCo-v2 与 BYOL）以及使用 multi-crop 的方法（即 SwAV）做详细比较。

表 13：DEIT-small 与 ResNet-50 的方法比较。我们报告 300 个 epoch 预训练后 ImageNet 线性与 k-NN 评估的验证准确率。所有数字均由我们运行，并与发表结果持平或更优。

| | | ResNet-50 | | | ViT-small | |
| --- | --- | --- | --- | --- | --- | --- |
| 方法 | | 线性 | k-NN | | 线性 | k-NN |
| MoCo-v2 | | 71.1 | 62.9 | | 71.6 | 62.0 |
| BYOL | | 72.7 | 65.4 | | 71.4 | 66.6 |
| SwAV | | 74.1 | 65.4 | | 71.8 | 64.7 |
| DINO | | 74.5 | 65.6 | | 76.1 | 72.8 |

##### 与 MoCo-v2 和 BYOL 的关系。

在表 14 中，我们展示消融 DINO、MoCo-v2 与 BYOL 之间差异组件的影响：损失的选择、学生头中的预测器、中心化操作、投影头中的批归一化，以及 multi-crop 增强。DINO 的损失是锐化 softmax 输出上的交叉熵（CE），MoCo-v2 使用 InfoNCE 对比损失（INCE），BYOL 使用 l2 归一化输出上的均方误差（MSE）。MSE 准则下不施加锐化。不过，DINO 在把损失函数换成 MSE 时出人意料地仍能工作，但性能显著改变（见行 (1, 2) 与 (4, 9)）。我们还观察到添加预测器的影响甚微（1, 3）。但在 BYOL 的情形中，预测器对防止塌缩至关重要（7, 8），这与以往研究 [7, 12] 一致。有趣的是，我们观察到教师输出中心化使 BYOL 在没有预测器和批归一化的情况下避免了塌缩（7, 9），但性能显著下降，原因很可能是我们的中心化算子是为与锐化配合使用而设计的。最后，我们观察到 multi-crop 与 DINO 和 MoCo-v2 配合得特别好，去掉它会使性能下降 2-4%（1 对 4，以及 5 对 6）。给 BYOL 添加 multi-crop 无法开箱即用（7, 10），详见附录 E，可能需要进一步适配。

表 14：与 MoCo-v2 和 BYOL 的关系。我们消融 DINO、MoCo-v2 与 BYOL 之间的差异组件：损失函数（交叉熵 CE、InfoNCE INCE、均方误差 MSE）、multi-crop 训练、中心化算子、投影头中的批归一化以及学生预测器。模型为 ViT-S/16，训练 300 个 epoch。我们报告 ImageNet 线性评估的 Top-1 准确率。

| | 方法 | 损失 | multi-crop | 中心化 | BN | 预测器 | Top-1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | DINO | CE | ✓ | ✓ | | | 76.1 |
| 2 | – | MSE | ✓ | ✓ | | | 62.4 |
| 3 | – | CE | ✓ | ✓ | | ✓ | 75.6 |
| 4 | – | CE | | ✓ | | | 72.5 |
| 5 | MoCov2 | INCE | | | ✓ | | 71.4 |
| 6 | | INCE | ✓ | | ✓ | | 73.4 |
| 7 | BYOL | MSE | | | ✓ | ✓ | 71.4 |
| 8 | – | MSE | | | ✓ | | 0.1 |
| 9 | – | MSE | | ✓ | | | 52.6 |
| 10 | – | MSE | ✓ | | ✓ | ✓ | 64.8 |

表 15：与 SwAV 的关系。我们在中心化、沿 batch 维度的 softmax 与 Sinkhorn-Knopp 算法之间改变教师输出上的操作。我们还通过用带停止梯度的学生硬拷贝替换动量编码器来消融动量编码器。模型为 ViT-S/16，训练 300 个 epoch。我们报告 ImageNet 线性评估的 Top-1 准确率。

| | 方法 | 动量 | 操作 | Top-1 |
| --- | --- | --- | --- | --- |
| 1 | DINO | ✓ | 中心化 | 76.1 |
| 2 | – | ✓ | Softmax(batch) | 75.8 |
| 3 | – | ✓ | Sinkhorn-Knopp | 76.0 |
| 4 | – | | 中心化 | 0.1 |
| 5 | – | | Softmax(batch) | 72.2 |
| 6 | SwAV | | Sinkhorn-Knopp | 71.8 |

##### 与 SwAV 的关系。

在表 15 中，我们评估 DINO 与 SwAV 之间的差异：动量编码器的存在，以及教师输出之上的操作。没有动量时，使用带停止梯度的学生副本。我们考虑教师输出上的三种操作：中心化、Sinkhorn-Knopp 或沿 batch 轴的 Softmax。该 Softmax 类似于单次 Sinkhorn-Knopp 迭代，细节见下一段。首先，这些消融表明使用动量编码器显著提升 ViT 的性能（3 对 6，以及 2 对 5）。其次，动量编码器还在只使用中心化时避免了塌缩（行 1）。没有动量时，对输出做中心化行不通（4），需要更高级的操作（5、6）。总体而言，这些消融突显了动量编码器的重要性——不仅为了性能，也为了稳定训练，使除中心化之外无需其他归一化。

##### Softmax(batch) 变体的细节。

SwAV [3] 中使用的迭代式 Sinkhorn-Knopp 算法 [8] 可用如下 PyTorch 风格代码简单实现。

```python
# tau is Sinkhorn regularization param
x = exp(x / tau)
for _ in range(num_iters): # 1 iter of Sinkhorn
    # total weight per dimension (or cluster)
    c = sum(x, dim=0, keepdim=True)
    x /= c
    # total weight per sample
    n = sum(x, dim=1, keepdim=True)
    # x sums to 1 for each sample (assignment)
    x /= n
```

当只执行单次 Sinkhorn 迭代（num_iters=1）时，实现可高度简化为仅两行代码，这便是我们的 softmax(batch) 变体：

```python
x /= sum(x, dim=1, keepdim=True)
```

我们在表 15 中看到，这一高度简化的 SwAV 变体与 SwAV 相比仍具竞争力。直观上，batch 轴上的 softmax 操作为每个维度（或「聚类」）选出其在 batch 中的最佳匹配。

##### 验证我们的实现。

我们在表 13 中观察到，我们复现的 BYOL、MoCo-v2、SwAV 在 ResNet-50 上与相应发表数字持平或更优。实际上，在这一 300 epoch 设置下我们得到 BYOL 72.7%，而 [12] 报告 72.5%。我们训练 300 个 epoch 后得到 MoCo 71.1%，而 [6] 训练 800 个 epoch 后报告 71.1%。相比 [6] 实现的改进可由更大的投影头（3 层、使用批归一化且投影维度为 256）解释。

##### 与其他工作的关系。

DINO 也与 UIC [14] 相关，后者使用上一个 epoch 的输出作为「无监督分类」的硬伪标签。不过，我们用中心化防止塌缩，而 UIC 诉诸 [8] 中的均衡采样技术。我们的工作可解释为一种带动量教师的软 UIC 变体。

并行工作 CsMI [77] 同样在 ImageNet 上用简单 k-NN 分类器表现出强劲性能，即便用卷积网络也是如此。与 DINO 一样，CsMI 组合了动量网络与 multi-crop 训练——我们在 ViT 实验中已看到，二者对良好的 k-NN 性能都至关重要。我们相信研究该工作将帮助我们更精确地识别对良好 k-NN 性能重要的组件，并把这一考察留作未来工作。

### C 投影头

与其他自监督框架类似，使用投影头 [4] 极大地提升了我们方法的准确率。投影头从一个 $n$ 层多层感知机（MLP）开始。隐藏层为 2048 维，并使用高斯误差线性单元（GELU）激活。MLP 的最后一层不带 GELU。然后我们施加 $\ell_{2}$ 归一化和一个带权重归一化的 $K$ 维全连接层 [7, 22]。这一设计受 SwAV [3] 中带「原型层（prototype layer）」的投影头启发。我们不施加批归一化。

##### 无 BN 系统。

与标准卷积网络不同，ViT 架构默认不使用批归一化（BN）。

| ViT-S，100 epochs | 头不带 BN | 头带 BN |
| --- | --- | --- |
| k-NN top-1 | 69.7 | 68.6 |

因此，将 DINO 应用于 ViT 时，投影头中我们也不使用任何 BN。在本表中，我们评估在头中添加 BN 的影响。我们观察到在投影头中添加 BN 的影响甚微，表明 BN 在我们的框架中并不重要。*总体而言，将 DINO 应用于 ViT 时，我们在任何地方都不使用任何 BN，使系统完全不含 BN（entirely BN-free）。*这是 DINO + ViT 的一大优势：无需任何 BN 即可达到最先进的性能。事实上，带 BN 的训练通常会显著拖慢训练，尤其当这些 BN 模块需要跨进程同步时 [13, 3, 2, 12]。

图 9：带或不带 l2-norm 瓶颈的投影头设计。

##### 投影头中的 L2 归一化瓶颈。

我们在图 9 中展示带或不带 l2 归一化瓶颈的投影头设计。

| 投影头线性层数 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- |
| 带 l2-norm 瓶颈 | – | 62.2 | 68.0 | 69.3 |
| 不带 l2-norm 瓶颈 | 61.6 | 62.9 | 0.1 | 0.1 |

我们评估带或不带 l2 归一化瓶颈训练的 DINO 模型的准确率，并改变投影头中线性层的数量。带 l2 瓶颈时，线性层总数为 $n+1$（$n$ 层来自 MLP，1 层来自权重归一化层）；不带瓶颈时，头中线性层的总数为 $n$。在本表中，我们报告 ViT-S/16 预训练 100 个 epoch 后的 ImageNet top-1 k-NN 评估准确率。本实验中输出维度 $K$ 设为 4096。我们观察到，当投影头加深时，没有 l2 归一化瓶颈的 DINO 训练会失败。L2 归一化瓶颈稳定了带深投影头的 DINO 训练。我们观察到增加投影头深度可提升准确率。我们的默认设置是总共 4 个线性层：3 层在 MLP 中，1 层在 l2 瓶颈之后。

##### 输出维度。

在本表中，我们评估改变输出维度 $K$ 的影响。

| $K$ | 1024 | 4096 | 16384 | 65536 | 262144 |
| --- | --- | --- | --- | --- | --- |
| k-NN top-1 | 67.8 | 69.3 | 69.2 | 69.7 | 69.1 |

我们观察到较大的输出维度可提升性能。我们注意到，l2 归一化瓶颈的使用使得可以采用较大的输出维度，而参数总量仅适度增加。我们的默认设置是 $K$ 等于 65536，瓶颈 $d=256$。

##### GELU 激活。

默认情况下，ViT 使用的激活是高斯误差线性单元（GELU）。

| ViT-S，100 epochs | 头带 GELU | 头带 ReLU |
| --- | --- | --- |
| k-NN top-1 | 69.7 | 68.9 |

因此，为了架构内部的一致性，我们选择在投影头中也使用 GELU。我们在本表中评估用 ReLU 替代 GELU 的效果，观察到把激活单元换成 ReLU 的影响相对较小。

### D 补充消融

我们已在正文中详述，中心化与锐化的组合对避免 DINO 中的塌缩很重要。下面我们对这两种操作的超参数做消融。我们还研究训练时长的影响以及 ViT 网络的一些设计选择。

##### 在线中心化。

我们研究教师网络输出中所用中心 $c$ 的更新规则中平滑参数的影响。

| $m$ | 0 | 0.9 | 0.99 | 0.999 |
| --- | --- | --- | --- | --- |
| k-NN top-1 | 69.1 | 69.7 | 69.4 | 0.1 |

收敛对很宽范围内的平滑取值都稳健，只有当更新过慢（即 $m=0.999$）时模型才塌缩。

##### 锐化。

我们通过调节教师 softmax 温度参数 $\tau_{t}$ 来强化尖锐目标。在本表中，我们观察到为避免塌缩需要低于 0.06 的温度。

| $\tau_{t}$ | 0 | 0.02 | 0.04 | 0.06 | 0.08 | 0.04→0.07 |
| --- | --- | --- | --- | --- | --- | --- |
| k-NN top-1 | 43.9 | 66.7 | 69.6 | 68.7 | 0.1 | 69.7 |

当温度高于 0.06 时，训练损失始终收敛到 $ln(K)$。但我们观察到，如果训练从一个较小的值开始并在最初几个 epoch 内逐渐升高，那么高于 0.06 的温度也不会塌缩。实践中，我们在训练的前 30 个 epoch 内对 $\tau_{t}$ 从 0.04 到 0.07 做线性预热。最后，注意 $\tau\rightarrow 0$（极端锐化）对应 argmax 操作并得到 one-hot 硬分布。

##### 更长的训练。

我们在本表中观察到，更长的训练提升了 DINO 应用于 ViT-Small 的性能。

| DINO ViT-S | 100-ep | 300-ep | 800-ep |
| --- | --- | --- | --- |
| k-NN top-1 | 70.9 | 72.8 | 74.5 |

这一观察与卷积架构上的自监督结果 [4] 一致。我们注意到，在我们对 ViT-S 上 BYOL 的实验中，超过 300 epoch 的训练相比我们的 300 epoch 运行反而得到更差的性能。因此，我们在表 2 中报告 BYOL 训练 300 个 epoch，而 SwAV、MoCo-v2 与 DINO 训练 800 个 epoch。

##### 教师优于学生。

我们已在图 6 中展示动量教师在 ViT 上优于学生，在本图中我们展示在 ResNet-50 上同样如此。

教师持续优于学生这一事实，进一步支持将 DINO 解读为一种 Mean Teacher [24] 自蒸馏形式。事实上，如 Tarvainen et al. [24] 所论证的，权重平均通常产生比每次迭代的单个模型更好的模型 [20]。以一个优于学生的教师所得到的目标为学习目标，学生的表示随之改善。相应地，教师也随之改善，因为它直接由学生权重构建。

##### 监督与自监督学习的自注意力图。

我们评估对自注意力图做阈值化以保留 80% 质量所得的掩码。

| ViT-S/16 权重 | |
| --- | --- |
| 随机权重 | 22.0 |
| 监督 | 27.3 |
| DINO | 45.9 |
| DINO 不带 multicrop | 45.1 |
| MoCo-v2 | 46.3 |
| BYOL | 47.8 |
| SwAV | 46.8 |

我们在 PASCAL VOC12 验证图像上比较真值与这些掩码的 Jaccard 相似度，对象是以不同框架训练的不同 ViT-S。「ViT 的自注意力图显式包含场景布局、尤其是物体边界」这一特性在不同自监督方法上都被观察到。

##### ViT-S 中头数的影响。

我们研究 ViT-S 中头数对准确率与吞吐量（单块 V100 GPU 推理时每秒处理的图像数）的影响。

| # 头 | dim | dim/头 | # 参数 | im/秒 | k-NN |
| --- | --- | --- | --- | --- | --- |
| 6 | 384 | 64 | 21 | 1007 | 72.8 |
| 8 | 384 | 48 | 21 | 971 | 73.1 |
| 12 | 384 | 32 | 21 | 927 | 73.7 |
| 16 | 384 | 24 | 21 | 860 | 73.8 |

我们发现增加头数可提升性能，代价是吞吐量略微变差。在我们的论文中，所有实验均使用默认模型 DeiT-S [25]，即只有 6 个头。

### E Multi-crop

在本附录中，我们研究 DINO 的一个核心组件：multi-crop 训练 [3]。

##### multi-crop 的尺度范围。

为生成不同的视图，我们使用 PyTorch 中 torchvision.transforms 模块的 RandomResizedCrop 方法。

| (0.05, s), (s, 1), s: | 0.08 | 0.16 | 0.24 | 0.32 | 0.48 |
| --- | --- | --- | --- | --- | --- |
| k-NN top-1 | 65.6 | 68.0 | 69.7 | 69.8 | 69.5 |

我们采样尺度范围为 $(s,1)$ 的两个全局视图并调整为 $224^{2}$，以及尺度在 $(0.05,s)$ 内采样的 6 个局部视图并调整为 $96^{2}$ 像素。注意，沿用 SwAV 的原始设计，我们任意选择让全局视图与局部视图的尺度范围不重叠。但这两个范围完全可以重叠，更精细的超参数搜索实验可能得到更优的设置。在本表中，我们改变控制 multi-crop 所用尺度范围的参数 $s$，发现在我们的实验中最优值约为 0.3。我们注意到这高于 SwAV 所用的参数 0.14。

##### 不同自监督框架中的 multi-crop。

我们比较近期不同的自监督学习框架 MoCo-v2 [6]、BYOL [12] 与 SwAV [3]，均使用 ViT-S/16 架构。

| crops | 2×$224^{2}$ | | | 2×$224^{2}$+6×$96^{2}$ | |
| --- | --- | --- | --- | --- | --- |
| 评估 | k-NN | 线性 | | k-NN | 线性 |
| BYOL | 66.6 | 71.4 | | 59.8 | 64.8 |
| SwAV | 60.5 | 68.5 | | 64.7 | 71.8 |
| MoCo-v2 | 62.0 | 71.6 | | 65.4 | 73.4 |
| DINO | 67.9 | 72.5 | | 72.7 | 75.9 |

为公平比较，所有模型都用两个 $224^{2}$ 裁剪或 multi-crop [3] 训练（即每张图像两个 $224^{2}$ 裁剪加六个 $96^{2}$ 裁剪）来预训练。我们报告训练 300 个 epoch 后的 k-NN 与线性探测评估。multi-crop 对各框架的收益并不均等，这一点在只考虑双裁剪设置的基准 [7] 中被忽视了。multi-crop 的有效性取决于所考虑的框架，这使得 multi-crop 成为一个模型的核心组件，而非能以同样方式提升任何框架的简单「附加项」。不带 multi-crop 时，DINO 的准确率仍优于其他框架，但优势温和（1%）。值得注意的是，DINO 从 multi-crop 训练中获益最多（线性评估 +3.4%）。有趣的是，我们还观察到框架的排名取决于所采用的评估协议。

##### 用 multi-crop 训练 BYOL。

当对 ViT-S 上的 BYOL 施加 multi-crop 时，我们观察到在最初的若干训练 epoch，迁移性能高于不带 multi-crop 的基线。

然而，迁移性能的增速会放缓，并在一定训练量之后开始下降。我们对这一设置做了学习率、权重衰减、multi-crop 参数的扫描，都系统性地观察到同样的模式。更精确地说，我们在学习率基准值 {1e-5, 3e-5, 1e-4, 3e-4, 1e-3, 3e-3}、权重衰减 {0.02, 0.05, 0.1} 以及不同数量的小裁剪 {2, 4, 6} 上做了实验。我们所有的运行都在头中使用了同步批归一化。使用低学习率时，我们没有观察到性能拐点，即迁移性能在训练期间持续改善，但总体准确率较低。我们尝试过在 ResNet-50 上用 multi-crop 训练，也观察到同样的行为。由于把 multi-crop 集成到 BYOL 不是本研究的重点，我们没有继续推进该方向。但我们相信，「为何 multi-crop 在我们的实验中与 BYOL 结合不佳」值得研究，并将其留作未来工作。

### F 评估协议

#### F.1 k-NN 分类

遵循 Wu et al. [27] 的设置，我们用简单的加权 k 最近邻分类器评估特征质量。我们冻结预训练模型，计算并存储下游任务训练数据的特征。为分类一张测试图像 $x$，我们计算其表示，并与所有已存储的训练特征 $T$ 比较。图像的表示由输出 [CLS] 词元给出：其维度对 ViT-S 为 $d=384$，对 ViT-B 为 $d=768$。前 $k$ 个 NN（记为 $\mathcal{N}_{k}$）通过加权投票进行预测。具体地，类别 $c$ 获得总权重 $\sum_{i\in\mathcal{N}_{k}}\alpha_{i}\mathbf{1}_{c_{i}=c}$，其中 $\alpha_{i}$ 是贡献权重。我们取 $\alpha_{i}=\exp(T_{i}x/\tau)$，$\tau$ 等于 0.07，与 [27] 一致且未经调优。我们评估了不同的 $k$ 值，发现 $k=20$ 在我们的运行中始终带来最佳准确率。这一评估协议不需要超参数调优、不需要数据增强，只需在下游数据集上跑一遍即可完成。

#### F.2 线性分类

遵循自监督学习的常见做法，我们用线性分类器评估表示质量。移除投影头，在冻结特征之上训练一个监督线性分类器。该线性分类器用 SGD 训练，batch 大小为 1024，在 ImageNet 上训练 100 个 epoch。我们不施加权重衰减。对每个模型，我们扫描学习率取值。训练期间，我们只施加随机尺寸裁剪（使用 PyTorch RandomResizedCrop 的默认参数）与水平翻转作为数据增强。我们报告中心裁剪 Top-1 准确率。评估卷积网络时，常见做法是在线性分类器之前对最终特征图做全局平均池化。下面我们描述评估 ViT 时如何调整这一设计。

##### 用于线性评估的 ViT-S 表示。

遵循 BERT [9] 中基于特征的评估，我们拼接最后 $l$ 层的 [CLS] 词元。

| 拼接最后 $l$ 层 | 1 | 2 | 4 | 6 |
| --- | --- | --- | --- | --- |
| 表示维度 | 384 | 768 | 1536 | 2304 |
| ViT-S/16 线性评估 | 76.1 | 76.6 | 77.0 | 77.0 |

我们实验了拼接不同数量 $l$ 的层，与 [9] 类似地发现 $l=4$ 最优。

##### 用于线性评估的 ViT-B 表示。

对 ViT-B，我们发现拼接最后 $l$ 层的表示并未带来任何性能增益，因此只考虑最后一层（$l=1$）。

| 池化策略 | 仅 [CLS] 词元 | 拼接 [CLS] 词元 |
| --- | --- | --- |
| | | 与平均池化图块词元 |
| 表示维度 | 768 | 1536 |
| ViT-B/16 线性评估 | 78.0 | 78.2 |

在这一设置中，我们改造卷积网络所用的流水线：对输出图块词元做全局平均池化。我们把这些池化特征与最终 [CLS] 输出词元拼接。

### G 自注意力可视化

我们在图 8 与图 10 中提供更多自注意力可视化。图像随机选自 COCO 验证集，未在 DINO 的训练中使用。在图 8 中，我们展示 DINO ViT-S/8 最后一层对若干参考点的自注意力。

### H 类别表示

作为最后的可视化，我们提议观察 ImageNet 概念在 DINO 特征空间中的分布。我们用每个 ImageNet 类别在其验证图像上的平均特征向量来表示该类。我们用 PCA 把这些特征的维度降到 30，然后运行 t-SNE（困惑度 20，学习率 200，迭代 5000 次）。我们在图 11 中展示得到的类别嵌入。我们的模型恢复了类别之间的结构：相近的动物物种被分到一起，形成连贯的鸟类（上方）或犬类——尤其是梗犬（最右侧）——的聚类。

图 10：最后一层的自注意力头。我们以 [CLS] 词元为查询，观察最后一层不同头的注意力图。注意，[CLS] 词元不与任何标签或监督绑定。

图 11：用 DINO 表示的 ImageNet 类别的 t-SNE 可视化。对每个类别，我们取该类别在验证集所有图像上特征的均值得到其嵌入。

## 补充材料：带动量教师的视觉 Transformer 自监督学习（Self-Supervised Learning of Visual Transformers with a Momentum Teacher）

| |
| --- |
| 匿名 ICCV 投稿 |
| 论文编号 7530 |

## 附录

### A 补充结果

##### k-NN 分类。

在表 1 中，我们用线性与 k-NN 两种评估协议，评估由 DINO 预训练的 ResNet-50 或 ViT-small 给出的冻结表示。在两种评估中，我们都在不使用任何数据增强的情况下从预训练网络提取表示。然后，用加权 k-NN 或用 cyanure 库 [16] 学习的线性回归进行分类。在表 1 中我们看到，无论用线性还是 k-NN 分类器，ViT-S 的准确率都优于 RN50。但用 k-NN 评估时的性能差距比线性评估显著得多。例如在 ImageNet 1% 上，ViT-S 以 +14.1% 的大幅优势超越 ResNet-50（k-NN 评估）。这表明用 DINO 训练的 Transformer 架构或许能提供更有利于 k-NN 评估的模型灵活性。k-NN 分类器的巨大优势是部署快速且轻量，无需任何域适应。总体而言，用 DINO 训练的 ViT 提供了与 k-NN 分类器结合得特别好的特征。

表 1：以 DINO 预训练的 ViT-S/16 与 ResNet-50 的 k-NN 与线性评估。我们使用 ImageNet-1k [21]（「Inet」）、Places205 [29]、PASCAL VOC [11] 与 Oxford-102 flowers（「FLOWERS」）[17]。用 DINO 训练的 ViT 提供对 k-NN 特别友好的特征。

| | 逻辑回归 | | | | k-NN | | |
| --- | --- | --- | --- | --- | --- | --- | --- |
| | RN50 | ViT-S | Δ | | RN50 | ViT-S | Δ |
| Inet 100% | 72.1 | 75.7 | 3.6 | | 67.5 | 74.5 | 7.0 |
| Inet 10% | 67.8 | 72.2 | 4.4 | | 59.3 | 69.1 | 9.8 |
| Inet 1% | 55.1 | 64.5 | 9.4 | | 47.2 | 61.3 | 14.1 |
| Pl. 10% | 53.4 | 52.1 | -1.3 | | 46.9 | 48.6 | 1.7 |
| Pl. 1% | 46.5 | 46.3 | -0.2 | | 39.2 | 41.3 | 2.1 |
| VOC07 | 88.9 | 89.2 | 0.3 | | 84.9 | 88.0 | 3.1 |
| FLOWERS | 95.6 | 96.4 | 0.8 | | 87.9 | 89.1 | 1.2 |
| 平均 Δ | | | 2.4 | | | | 5.6 |

表 2：不同预训练下的 ImageNet 分类。监督 ViT-B/16 模型在不同预训练、或使用一个额外预训练卷积网络引导训练下的 ImageNet Top-1 准确率。各方法使用不同的图像分辨率（「res.」）与训练流程（「tr. proc.」，即数据增强与优化）。「MPP」指掩码图块预测（Masked Patch Prediction）。

| 预训练 | | | | | |
| --- | --- | --- | --- | --- | --- |
| 方法 | 数据 | | res. | tr. proc. | Top-1 |
| 在额外数据上预训练 | | | | | |
| MMP | JFT-300M | | 384 | [10] | 79.9 |
| 监督 | JFT-300M | | 384 | [10] | 84.2 |
| 使用额外模型训练 | | | | | |
| 随机初始化 | - | | 224 | [25] | 83.4 |
| 无额外数据与模型 | | | | | |
| 随机初始化 | - | | 224 | [10] | 77.9 |
| 随机初始化 | - | | 224 | [25] | 81.8 |
| 监督 | ImNet | | 224 | [25] | 81.9 |
| DINO | ImNet | | 224 | [25] | 82.8 |

##### ViT 的自监督 ImageNet 预训练。

在本实验中，我们研究用我们的方法预训练一个监督 ViT 模型的影响。在表 2 中，我们比较以不同预训练初始化、或在训练中由额外预训练卷积网络引导的监督 ViT 模型的性能。第一组模型在由 3 亿张图像组成的大型筛选数据集上做有/无监督预训练。第二组模型从预训练监督 RegNetY [56] 做硬知识蒸馏。最后一组模型不使用任何额外数据或模型，或随机初始化，或在 ImageNet 上以 DINO 预训练后初始化。与随机初始化相比，DINO 预训练带来 +1% 的性能增益。这并非由更长的训练造成，因为用监督代替 DINO 做预训练并不能提升性能。自监督预训练缩小了与「在额外数据上预训练」或「从卷积网络蒸馏」的模型之间的差距。

##### ImageNet 上的少样本学习。

我们评估将 DINO 应用于 ViT-S 所得特征在少样本（low-shot）学习上的表现。在表 3 中，我们报告在带 1% 与 10% 标签的冻结特征（frozen）上训练逻辑回归的验证准确率。逻辑回归用 cyanure 库 [16] 训练。在参数量与 images/sec 相近的模型之间比较时，我们观察到我们的特征与最先进的半监督模型相当。有趣的是，这一性能是通过在**冻结特征上**训练多类逻辑回归得到的——**无需数据增强、无需微调**。

表 3：用冻结 ViT 特征在 ImageNet 上做少样本学习。我们在冻结特征上训练逻辑回归（frozen）。注意，这一冻结评估是在**不做任何微调、不做数据增强**的情况下进行的。我们报告 Top-1 准确率。作为参考，我们列出以往使用微调与半监督学习的发表结果。

| | | | Top 1 | |
| --- | --- | --- | --- | --- |
| 方法 | 架构 | 参数 | 1% | 10% |
| 自监督预训练 + 微调 | | | | |
| UDA [28] | RN50 | 23 | – | 68.1 |
| SimCLRv2 [5] | RN50 | 23 | 57.9 | 68.4 |
| BYOL [12] | RN50 | 23 | 53.2 | 68.8 |
| SwAV [3] | RN50 | 23 | 53.9 | 70.2 |
| SimCLRv2 [7] | RN50w4 | 375 | 63.0 | 74.4 |
| BYOL [12] | RN200w2 | 250 | 71.2 | 77.7 |
| 半监督方法 | | | | |
| SimCLRv2+KD [5] | RN50 | 23 | 60.0 | 70.5 |
| SwAV+CT [1] | RN50 | 23 | – | 70.8 |
| FixMatch [23] | RN50 | 23 | – | 71.5 |
| MPL [19] | RN50 | 23 | – | 73.9 |
| SimCLRv2+KD [5] | RN152w3+SK | 794 | 76.6 | 80.9 |
| 冻结的自监督特征 | | | | |
| DINO -frozen | ViT-S/16 | 21 | 64.5 | 72.2 |

图 1：一组参考点的自注意力。我们可视化用 DINO 训练的 ViT-S/8 最后一块的自注意力模块。尽管完全没有使用监督训练，该网络仍能分离物体。

### B 方法比较

我们比较不同自监督框架 MoCo-v2 [6]、SwAV [3] 与 BYOL [12] 在卷积网络或 ViT 上的性能。在表 4 中，我们看到用 ResNet-50（卷积网络）训练时，DINO 与 SwAV、BYOL 表现相当。但 DINO 在 ViT 上充分释放了潜力，以大幅优势超越 MoCo-v2、SwAV 与 BYOL（线性评估 +4.3%，k-NN 评估 +6.2%）。在本节余下部分，我们做消融以更好地理解 DINO 应用于 ViT 的性能。特别地，我们与使用动量编码器的方法（即 MoCo-v2 与 BYOL）以及使用 multi-crop 的方法（即 SwAV）做详细比较。

表 4：DEIT-small 与 ResNet-50 的方法比较。我们报告 300 个 epoch 预训练后 ImageNet 线性与 k-NN 评估的验证准确率。所有数字均由我们运行，并与发表结果持平或更优。

| | | ResNet-50 | | | ViT-small | |
| --- | --- | --- | --- | --- | --- | --- |
| 方法 | | 线性 | k-NN | | 线性 | k-NN |
| MoCo-v2 | | 71.1 | 62.9 | | 71.6 | 62.0 |
| BYOL | | 72.7 | 65.4 | | 71.4 | 66.6 |
| SwAV | | 74.1 | 65.4 | | 71.8 | 64.7 |
| DINO | | 74.5 | 65.6 | | 76.1 | 72.8 |

##### 与 MoCo-v2 和 BYOL 的关系。

在表 5 中，我们展示消融 DINO、MoCo-v2 与 BYOL 之间差异组件的影响：损失的选择、学生头中的预测器、中心化操作、投影头中的批归一化，以及 multi-crop 增强。DINO 的损失是锐化 softmax 输出上的交叉熵（CE），MoCo-v2 使用 InfoNCE 对比损失（INCE），BYOL 使用 l2 归一化输出上的均方误差（MSE）。MSE 准则下不施加锐化。不过，DINO 在把损失函数换成 MSE 时出人意料地仍能工作，但性能显著改变（见行 (1, 2) 与 (4, 9)）。我们还观察到添加预测器的影响甚微（1, 3）。但在 BYOL 的情形中，预测器对防止塌缩至关重要（7, 8），这与以往研究 [7, 12] 一致。有趣的是，我们观察到教师输出中心化使 BYOL 在没有预测器和批归一化的情况下避免了塌缩（7, 9），但性能显著下降，原因很可能是我们的中心化算子是为与锐化配合使用而设计的。最后，我们观察到 multi-crop 与 DINO 和 MoCo-v2 配合得特别好，去掉它会使性能下降 2-4%（1 对 4，以及 5 对 6）。给 BYOL 添加 multi-crop 无法开箱即用（7, 10），详见附录 E，可能需要进一步适配。

表 5：与 MoCo-v2 和 BYOL 的关系。我们消融 DINO、MoCo-v2 与 BYOL 之间的差异组件：损失函数（交叉熵 CE、InfoNCE INCE、均方误差 MSE）、multi-crop 训练、中心化算子、投影头中的批归一化以及学生预测器。模型为 ViT-S/16，训练 300 个 epoch。我们报告 ImageNet 线性评估的 Top-1 准确率。

| | 方法 | 损失 | multi-crop | 中心化 | BN | 预测器 | Top-1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | DINO | CE | ✓ | ✓ | | | 76.1 |
| 2 | – | MSE | ✓ | ✓ | | | 62.4 |
| 3 | – | CE | ✓ | ✓ | | ✓ | 75.6 |
| 4 | – | CE | | ✓ | | | 72.5 |
| 5 | MoCov2 | INCE | | | ✓ | | 71.4 |
| 6 | | INCE | ✓ | | ✓ | | 73.4 |
| 7 | BYOL | MSE | | | ✓ | ✓ | 71.4 |
| 8 | – | MSE | | | ✓ | | 0.1 |
| 9 | – | MSE | | ✓ | | | 52.6 |
| 10 | – | MSE | ✓ | | ✓ | ✓ | 64.8 |

表 6：与 SwAV 的关系。我们在中心化、沿 batch 维度的 softmax 与 Sinkhorn-Knopp 算法之间改变教师输出上的操作。我们还通过用带停止梯度的学生硬拷贝替换动量编码器来消融动量编码器。模型为 ViT-S/16，训练 300 个 epoch。我们报告 ImageNet 线性评估的 Top-1 准确率。

| | 方法 | 动量 | 操作 | Top-1 |
| --- | --- | --- | --- | --- |
| 1 | DINO | ✓ | 中心化 | 76.1 |
| 2 | – | ✓ | Softmax(batch) | 75.8 |
| 3 | – | ✓ | Sinkhorn-Knopp | 76.0 |
| 4 | – | | 中心化 | 0.1 |
| 5 | – | | Softmax(batch) | 72.2 |
| 6 | SwAV | | Sinkhorn-Knopp | 71.8 |

##### 与 SwAV 的关系。

在表 6 中，我们评估 DINO 与 SwAV 之间的差异：动量编码器的存在，以及教师输出之上的操作。没有动量时，使用带停止梯度的学生副本。我们考虑教师输出上的三种操作：中心化、Sinkhorn-Knopp 或沿 batch 轴的 Softmax。该 Softmax 类似于单次 Sinkhorn-Knopp 迭代，细节见下一段。首先，这些消融表明使用动量编码器显著提升 ViT 的性能（3 对 6，以及 2 对 5）。其次，动量编码器还在只使用中心化时避免了塌缩（行 1）。没有动量时，对输出做中心化行不通（4），需要更高级的操作（5、6）。总体而言，这些消融突显了动量编码器的重要性——不仅为了性能，也为了稳定训练，使除中心化之外无需其他归一化。

##### Softmax(batch) 变体的细节。

SwAV [3] 中使用的迭代式 Sinkhorn-Knopp 算法 [8] 可用如下 PyTorch 风格代码简单实现。

```python
# tau is Sinkhorn regularization param
x = exp(x / tau)
for _ in range(num_iters): # 1 iter of Sinkhorn
    # total weight per dimension (or cluster)
    c = sum(x, dim=0, keepdim=True)
    x /= c
    # total weight per sample
    n = sum(x, dim=1, keepdim=True)
    # x sums to 1 for each sample (assignment)
    x /= n
```

当只执行单次 Sinkhorn 迭代（num_iters=1）时，实现可高度简化为仅两行代码，这便是我们的 softmax(batch) 变体：

```python
x /= sum(x, dim=1, keepdim=True)
```

我们在表 6 中看到，这一高度简化的 SwAV 变体与 SwAV 相比仍具竞争力。直观上，batch 轴上的 softmax 操作为每个维度（或「聚类」）选出其在 batch 中的最佳匹配。

##### 验证我们的实现。

我们在表 4 中观察到，我们复现的 BYOL、MoCo-v2、SwAV 在 ResNet-50 上与相应发表数字持平或更优。实际上，在这一 300 epoch 设置下我们得到 BYOL 72.7%，而 [12] 报告 72.5%。我们训练 300 个 epoch 后得到 MoCo 71.1%，而 [6] 训练 800 个 epoch 后报告 71.1%。相比 [6] 实现的改进可由更大的投影头（3 层、使用批归一化且投影维度为 256）解释。

##### 与其他工作的关系。

DINO 也与 UIC [14] 相关，后者使用上一个 epoch 的输出作为「无监督分类」的硬伪标签。不过，我们用中心化防止塌缩，而 UIC 诉诸 [8] 中的均衡采样技术。我们的工作可解释为一种带动量教师的软 UIC 变体。

并行工作 CsMI [77] 同样在 ImageNet 上用简单 k-NN 分类器表现出强劲性能，即便用卷积网络也是如此。与 DINO 一样，CsMI 组合了动量网络与 multi-crop 训练——我们在 ViT 实验中已看到，二者对良好的 k-NN 性能都至关重要。我们相信研究该工作将帮助我们更精确地识别对良好 k-NN 性能重要的组件，并把这一考察留作未来工作。

### C 投影头

与其他自监督框架类似，使用投影头 [4] 极大地提升了我们方法的准确率。投影头从一个 $n$ 层多层感知机（MLP）开始。隐藏层为 2048 维，并使用高斯误差线性单元（GELU）激活。MLP 的最后一层不带 GELU。然后我们施加 $\ell_{2}$ 归一化和一个带权重归一化的 $K$ 维全连接层 [7, 22]。这一设计受 SwAV [3] 中带「原型层（prototype layer）」的投影头启发。我们不施加批归一化。

##### 无 BN 系统。

与标准卷积网络不同，ViT 架构默认不使用批归一化（BN）。

| ViT-S，100 epochs | 头不带 BN | 头带 BN |
| --- | --- | --- |
| k-NN top-1 | 69.7 | 68.6 |

因此，将 DINO 应用于 ViT 时，投影头中我们也不使用任何 BN。在本表中，我们评估在头中添加 BN 的影响。我们观察到在投影头中添加 BN 的影响甚微，表明 BN 在我们的框架中并不重要。*总体而言，将 DINO 应用于 ViT 时，我们在任何地方都不使用任何 BN，使系统完全不含 BN（entirely BN-free）。*这是 DINO + ViT 的一大优势：无需任何 BN 即可达到最先进的性能。事实上，带 BN 的训练通常会显著拖慢训练，尤其当这些 BN 模块需要跨进程同步时 [13, 3, 2, 12]。

图 2：带或不带 l2-norm 瓶颈的投影头设计。

##### 投影头中的 L2 归一化瓶颈。

我们在图 2 中展示带或不带 l2 归一化瓶颈的投影头设计。

| 投影头线性层数 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- |
| 带 l2-norm 瓶颈 | – | 62.2 | 68.0 | 69.3 |
| 不带 l2-norm 瓶颈 | 61.6 | 62.9 | 0.1 | 0.1 |

我们评估带或不带 l2 归一化瓶颈训练的 DINO 模型的准确率，并改变投影头中线性层的数量。带 l2 瓶颈时，线性层总数为 $n+1$（$n$ 层来自 MLP，1 层来自权重归一化层）；不带瓶颈时，头中线性层的总数为 $n$。在本表中，我们报告 ViT-S/16 预训练 100 个 epoch 后的 ImageNet top-1 k-NN 评估准确率。本实验中输出维度 $K$ 设为 4096。我们观察到，当投影头加深时，没有 l2 归一化瓶颈的 DINO 训练会失败。L2 归一化瓶颈稳定了带深投影头的 DINO 训练。我们观察到增加投影头深度可提升准确率。我们的默认设置是总共 4 个线性层：3 层在 MLP 中，1 层在 l2 瓶颈之后。

##### 输出维度。

在本表中，我们评估改变输出维度 $K$ 的影响。

| $K$ | 1024 | 4096 | 16384 | 65536 | 262144 |
| --- | --- | --- | --- | --- | --- |
| k-NN top-1 | 67.8 | 69.3 | 69.2 | 69.7 | 69.1 |

我们观察到较大的输出维度可提升性能。我们注意到，l2 归一化瓶颈的使用使得可以采用较大的输出维度，而参数总量仅适度增加。我们的默认设置是 $K$ 等于 65536，瓶颈 $d=256$。

##### GELU 激活。

默认情况下，ViT 使用的激活是高斯误差线性单元（GELU）。

| ViT-S，100 epochs | 头带 GELU | 头带 ReLU |
| --- | --- | --- |
| k-NN top-1 | 69.7 | 68.9 |

因此，为了架构内部的一致性，我们选择在投影头中也使用 GELU。我们在本表中评估用 ReLU 替代 GELU 的效果，观察到把激活单元换成 ReLU 的影响相对较小。

### D 补充消融

我们已在正文中详述，中心化与锐化的组合对避免 DINO 中的塌缩很重要。下面我们对这两种操作的超参数做消融。我们还研究训练时长的影响以及 ViT 网络的一些设计选择。

##### 在线中心化。

我们研究教师网络输出中所用中心 $c$ 的更新规则中平滑参数的影响。

| $m$ | 0 | 0.9 | 0.99 | 0.999 |
| --- | --- | --- | --- | --- |
| k-NN top-1 | 69.1 | 69.7 | 69.4 | 0.1 |

收敛对很宽范围内的平滑取值都稳健，只有当更新过慢（即 $m=0.999$）时模型才塌缩。

##### 锐化。

我们通过调节教师 softmax 温度参数 $\tau_{t}$ 来强化尖锐目标。在本表中，我们观察到为避免塌缩需要低于 0.06 的温度。

| $\tau_{t}$ | 0 | 0.02 | 0.04 | 0.06 | 0.08 | 0.04→0.07 |
| --- | --- | --- | --- | --- | --- | --- |
| k-NN top-1 | 43.9 | 66.7 | 69.6 | 68.7 | 0.1 | 69.7 |

当温度高于 0.06 时，训练损失始终收敛到 $ln(K)$。但我们观察到，如果训练从一个较小的值开始并在最初几个 epoch 内逐渐升高，那么高于 0.06 的温度也不会塌缩。实践中，我们在训练的前 30 个 epoch 内对 $\tau_{t}$ 从 0.04 到 0.07 做线性预热。最后，注意 $\tau\rightarrow 0$（极端锐化）对应 argmax 操作并得到 one-hot 硬分布。

##### 更长的训练。

我们在本表中观察到，更长的训练提升了 DINO 应用于 ViT-Small 的性能。

| DINO ViT-S | 100-ep | 300-ep | 800-ep |
| --- | --- | --- | --- |
| k-NN top-1 | 70.9 | 72.8 | 74.5 |

这一观察与卷积架构上的自监督结果 [4] 一致。我们注意到，在我们对 ViT-S 上 BYOL 的实验中，超过 300 epoch 的训练相比我们的 300 epoch 运行反而得到更差的性能。因此，我们在表 2（主文）中报告 BYOL 训练 300 个 epoch，而 SwAV、MoCo-v2 与 DINO 训练 800 个 epoch。

##### 教师优于学生。

我们已在图 6（主文）中展示动量教师在 ViT 上优于学生，在本图中我们展示在 ResNet-50 上同样如此。

教师持续优于学生这一事实，进一步支持将 DINO 解读为一种 Mean Teacher [24] 自蒸馏形式。事实上，如 Tarvainen et al. [24] 所论证的，权重平均通常产生比每次迭代的单个模型更好的模型 [20]。以一个优于学生的教师所得到的目标为学习目标，学生的表示随之改善。相应地，教师也随之改善，因为它直接由学生权重构建。

##### 监督与自监督学习的自注意力图。

我们评估对自注意力图做阈值化以保留 80% 质量所得的掩码。

| ViT-S/16 权重 | |
| --- | --- |
| 随机权重 | 22.0 |
| 监督 | 27.3 |
| DINO | 45.9 |
| DINO 不带 multicrop | 45.1 |
| MoCo-v2 | 46.3 |
| BYOL | 47.8 |
| SwAV | 46.8 |

我们在 PASCAL VOC12 验证图像上比较真值与这些掩码的 Jaccard 相似度，对象是以不同框架训练的不同 ViT-S。「ViT 的自注意力图显式包含场景布局、尤其是物体边界」这一特性在不同自监督方法上都被观察到。

##### ViT-S 中头数的影响。

我们研究 ViT-S 中头数对准确率与吞吐量（单块 V100 GPU 推理时每秒处理的图像数）的影响。

| # 头 | dim | dim/头 | # 参数 | im/秒 | k-NN |
| --- | --- | --- | --- | --- | --- |
| 6 | 384 | 64 | 21 | 1007 | 72.8 |
| 8 | 384 | 48 | 21 | 971 | 73.1 |
| 12 | 384 | 32 | 21 | 927 | 73.7 |
| 16 | 384 | 24 | 21 | 860 | 73.8 |

我们发现增加头数可提升性能，代价是吞吐量略微变差。在我们的论文中，所有实验均使用默认模型 DeiT-S [25]，即只有 6 个头。

### E Multi-crop

在本附录中，我们研究 DINO 的一个核心组件：multi-crop 训练 [3]。

##### multi-crop 的尺度范围。

为生成不同的视图，我们使用 PyTorch 中 torchvision.transforms 模块的 RandomResizedCrop 方法。

| (0.05, s), (s, 1), s: | 0.08 | 0.16 | 0.24 | 0.32 | 0.48 |
| --- | --- | --- | --- | --- | --- |
| k-NN top-1 | 65.6 | 68.0 | 69.7 | 69.8 | 69.5 |

我们采样尺度范围为 $(s,1)$ 的两个全局视图并调整为 $224^{2}$，以及尺度在 $(0.05,s)$ 内采样的 6 个局部视图并调整为 $96^{2}$ 像素。注意，沿用 SwAV 的原始设计，我们任意选择让全局视图与局部视图的尺度范围不重叠。但这两个范围完全可以重叠，更精细的超参数搜索实验可能得到更优的设置。在本表中，我们改变控制 multi-crop 所用尺度范围的参数 $s$，发现在我们的实验中最优值约为 0.3。我们注意到这高于 SwAV 所用的参数 0.14。

##### 不同自监督框架中的 multi-crop。

我们比较近期不同的自监督学习框架 MoCo-v2 [6]、BYOL [12] 与 SwAV [3]，均使用 ViT-S/16 架构。

| crops | 2×$224^{2}$ | | | 2×$224^{2}$+6×$96^{2}$ | |
| --- | --- | --- | --- | --- | --- |
| 评估 | k-NN | 线性 | | k-NN | 线性 |
| BYOL | 66.6 | 71.4 | | 59.8 | 64.8 |
| SwAV | 60.5 | 68.5 | | 64.7 | 71.8 |
| MoCo-v2 | 62.0 | 71.6 | | 65.4 | 73.4 |
| DINO | 67.9 | 72.5 | | 72.7 | 75.9 |

为公平比较，所有模型都用两个 $224^{2}$ 裁剪或 multi-crop [3] 训练（即每张图像两个 $224^{2}$ 裁剪加六个 $96^{2}$ 裁剪）来预训练。我们报告训练 300 个 epoch 后的 k-NN 与线性探测评估。multi-crop 对各框架的收益并不均等，这一点在只考虑双裁剪设置的基准 [7] 中被忽视了。multi-crop 的有效性取决于所考虑的框架，这使得 multi-crop 成为一个模型的核心组件，而非能以同样方式提升任何框架的简单「附加项」。不带 multi-crop 时，DINO 的准确率仍优于其他框架，但优势温和（1%）。值得注意的是，DINO 从 multi-crop 训练中获益最多（线性评估 +3.4%）。有趣的是，我们还观察到框架的排名取决于所采用的评估协议。

##### 用 multi-crop 训练 BYOL。

当对 ViT-S 上的 BYOL 施加 multi-crop 时，我们观察到在最初的若干训练 epoch，迁移性能高于不带 multi-crop 的基线。

然而，迁移性能的增速会放缓，并在一定训练量之后开始下降。我们对这一设置做了学习率、权重衰减、multi-crop 参数的扫描，都系统性地观察到同样的模式。更精确地说，我们在学习率基准值 {1e-5, 3e-5, 1e-4, 3e-4, 1e-3, 3e-3}、权重衰减 {0.02, 0.05, 0.1} 以及不同数量的小裁剪 {2, 4, 6} 上做了实验。我们所有的运行都在头中使用了同步批归一化。使用低学习率时，我们没有观察到性能拐点，即迁移性能在训练期间持续改善，但总体准确率较低。我们尝试过在 ResNet-50 上用 multi-crop 训练，也观察到同样的行为。由于把 multi-crop 集成到 BYOL 不是本研究的重点，我们没有继续推进该方向。但我们相信，「为何 multi-crop 在我们的实验中与 BYOL 结合不佳」值得研究，并将其留作未来工作。

### F 评估协议

#### F.1 k-NN 分类

遵循 Wu et al. [27] 的设置，我们用简单的加权 k 最近邻分类器评估特征质量。我们冻结预训练模型，计算并存储下游任务训练数据的特征。为分类一张测试图像 $x$，我们计算其表示，并与所有已存储的训练特征 $T$ 比较。图像的表示由输出 [CLS] 词元给出：其维度对 ViT-S 为 $d=384$，对 ViT-B 为 $d=768$。前 $k$ 个 NN（记为 $\mathcal{N}_{k}$）通过加权投票进行预测。具体地，类别 $c$ 获得总权重 $\sum_{i\in\mathcal{N}_{k}}\alpha_{i}\mathbf{1}_{c_{i}=c}$，其中 $\alpha_{i}$ 是贡献权重。我们取 $\alpha_{i}=\exp(T_{i}x/\tau)$，$\tau$ 等于 0.07，与 [27] 一致且未经调优。我们评估了不同的 $k$ 值，发现 $k=20$ 在我们的运行中始终带来最佳准确率。这一评估协议不需要超参数调优、不需要数据增强，只需在下游数据集上跑一遍即可完成。

#### F.2 线性分类

遵循自监督学习的常见做法，我们用线性分类器评估表示质量。移除投影头，在冻结特征之上训练一个监督线性分类器。该线性分类器用 SGD 训练，batch 大小为 1024，在 ImageNet 上训练 100 个 epoch。我们不施加权重衰减。对每个模型，我们扫描学习率取值。训练期间，我们只施加随机尺寸裁剪（使用 PyTorch RandomResizedCrop 的默认参数）与水平翻转作为数据增强。我们报告中心裁剪 Top-1 准确率。评估卷积网络时，常见做法是在线性分类器之前对最终特征图做全局平均池化。下面我们描述评估 ViT 时如何调整这一设计。

##### 用于线性评估的 ViT-S 表示。

遵循 BERT [9] 中基于特征的评估，我们拼接最后 $l$ 层的 [CLS] 词元。

| 拼接最后 $l$ 层 | 1 | 2 | 4 | 6 |
| --- | --- | --- | --- | --- |
| 表示维度 | 384 | 768 | 1536 | 2304 |
| ViT-S/16 线性评估 | 76.1 | 76.6 | 77.0 | 77.0 |

我们实验了拼接不同数量 $l$ 的层，与 [9] 类似地发现 $l=4$ 最优。

##### 用于线性评估的 ViT-B 表示。

对 ViT-B，我们发现拼接最后 $l$ 层的表示并未带来任何性能增益，因此只考虑最后一层（$l=1$）。

| 池化策略 | 仅 [CLS] 词元 | 拼接 [CLS] 词元 |
| --- | --- | --- |
| | | 与平均池化图块词元 |
| 表示维度 | 768 | 1536 |
| ViT-B/16 线性评估 | 78.0 | 78.2 |

在这一设置中，我们改造卷积网络所用的流水线：对输出图块词元做全局平均池化。我们把这些池化特征与最终 [CLS] 输出词元拼接。

### G 自注意力可视化

我们在图 1 与图 3 中提供更多自注意力可视化。图像随机选自 COCO 验证集，未在 DINO 的训练中使用。在图 1 中，我们展示 DINO ViT-S/8 最后一层对若干参考点的自注意力。

### H 类别表示

作为最后的可视化，我们提议观察 ImageNet 概念在 DINO 特征空间中的分布。我们用每个 ImageNet 类别在其验证图像上的平均特征向量来表示该类。我们用 PCA 把这些特征的维度降到 30，然后运行 t-SNE（困惑度 20，学习率 200，迭代 5000 次）。我们在图 4 中展示得到的类别嵌入。我们的模型恢复了类别之间的结构：相近的动物物种被分到一起，形成连贯的鸟类（上方）或犬类——尤其是梗犬（最右侧）——的聚类。

图 3：最后一层的自注意力头。我们以 [CLS] 词元为查询，观察最后一层不同头的注意力图。注意，[CLS] 词元不与任何标签或监督绑定。

图 4：用 DINO 表示的 ImageNet 类别的 t-SNE 可视化。对每个类别，我们取该类别在验证集所有图像上特征的均值得到其嵌入。

## 参考文献

- [1]

  Mahmoud Assran, Nicolas Ballas, Lluis Castrejon, and Michael Rabbat.
  Recovering petaflops in contrastive semi-supervised learning of
  visual representations.
  arXiv preprint arXiv:2006.10803, 2020.
- [2]

  Mathilde Caron, Piotr Bojanowski, Julien Mairal, and Armand Joulin.
  Unsupervised pre-training of image features on non-curated data.
  In Proceedings of the International Conference on Computer
  Vision (ICCV), 2019.
- [3]

  Mathilde Caron, Ishan Misra, Julien Mairal, Priya Goyal, Piotr Bojanowski, and
  Armand Joulin.
  Unsupervised learning of visual features by contrasting cluster
  assignments.
  In Proceedings of Advances in Neural Information Processing
  Systems (NeurIPS), 2020.
- [4]

  Ting Chen, Simon Kornblith, Mohammad Norouzi, and Geoffrey Hinton.
  A simple framework for contrastive learning of visual
  representations.
  arXiv preprint arXiv:2002.05709, 2020.
- [5]

  Ting Chen, Simon Kornblith, Kevin Swersky, Mohammad Norouzi, and Geoffrey
  Hinton.
  Big self-supervised models are strong semi-supervised learners.
  In Proceedings of Advances in Neural Information Processing
  Systems (NeurIPS), 2020.
- [6]

  Xinlei Chen, Haoqi Fan, Ross Girshick, and Kaiming He.
  Improved baselines with momentum contrastive learning.
  arXiv preprint arXiv:2003.04297, 2020.
- [7]

  Xinlei Chen and Kaiming He.
  Exploring simple siamese representation learning.
  arXiv preprint arXiv:2011.10566, 2020.
- [8]

  Marco Cuturi.
  Sinkhorn distances: Lightspeed computation of optimal transport.
  In Proceedings of Advances in Neural Information Processing
  Systems (NeurIPS), 2013.
- [9]

  Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova.
  Bert: Pre-training of deep bidirectional transformers for language
  understanding.
  arXiv preprint arXiv:1810.04805, 2018.
- [10]

  Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov, Dirk Weissenborn,
  Xiaohua Zhai, Thomas Unterthiner, Mostafa Dehghani, Matthias Minderer, Georg
  Heigold, Sylvain Gelly, et al.
  An image is worth 16x16 words: Transformers for image recognition at
  scale.
  arXiv preprint arXiv:2010.11929, 2020.
- [11]

  Mark Everingham, Luc Van Gool, Christopher KI Williams, John Winn, and Andrew
  Zisserman.
  The pascal visual object classes (voc) challenge.
  International Journal of Computer Vision (IJCV), 2010.
- [12]

  Jean-Bastien Grill, Florian Strub, Florent Altché, Corentin Tallec,
  Pierre H Richemond, Elena Buchatskaya, Carl Doersch, Bernardo Avila Pires,
  Zhaohan Daniel Guo, Mohammad Gheshlaghi Azar, et al.
  Bootstrap your own latent: A new approach to self-supervised
  learning.
  In Proceedings of Advances in Neural Information Processing
  Systems (NeurIPS), 2020.
- [13]

  Kaiming He, Haoqi Fan, Yuxin Wu, Saining Xie, and Ross Girshick.
  Momentum contrast for unsupervised visual representation learning.
  In Proceedings of the Conference on Computer Vision and Pattern
  Recognition (CVPR), 2020.
- [14]

  Allan Jabri, Andrew Owens, and Alexei A Efros.
  Space-time correspondence as a contrastive random walk.
  2020.
- [15]

  Zihang Lai, Erika Lu, and Weidi Xie.
  Mast: A memory-augmented self-supervised tracker.
  In Proceedings of the IEEE/CVF Conference on Computer Vision and
  Pattern Recognition, pages 6479–6488, 2020.
- [16]

  Julien Mairal.
  Cyanure: An open-source toolbox for empirical risk minimization for
  python, c++, and soon more.
  arXiv preprint arXiv:1912.08165, 2019.
- [17]

  Maria-Elena Nilsback and Andrew Zisserman.
  Automated flower classification over a large number of classes.
  In 2008 Sixth Indian Conference on Computer Vision, Graphics &
  Image Processing, 2008.
- [18]

  Seoung Wug Oh, Joon-Young Lee, Ning Xu, and Seon Joo Kim.
  Video object segmentation using space-time memory networks.
  In Proceedings of the IEEE/CVF International Conference on
  Computer Vision, pages 9226–9235, 2019.
- [19]

  Hieu Pham, Qizhe Xie, Zihang Dai, and Quoc V Le.
  Meta pseudo labels.
  arXiv preprint arXiv:2003.10580, 2020.
- [20]

  Boris T Polyak and Anatoli B Juditsky.
  Acceleration of stochastic approximation by averaging.
  SIAM journal on control and optimization, 30(4):838–855, 1992.
- [21]

  Olga Russakovsky, Jia Deng, Hao Su, Jonathan Krause, Sanjeev Satheesh, Sean Ma,
  Zhiheng Huang, Andrej Karpathy, Aditya Khosla, Michael Bernstein, Alexander C
  Berg, and Li Fei-Fei.
  Imagenet large scale visual recognition challenge.
  International Journal of Computer Vision (IJCV), 2015.
- [22]

  Tim Salimans and Diederik P Kingma.
  Weight normalization: A simple reparameterization to accelerate
  training of deep neural networks.
  Proceedings of Advances in Neural Information Processing Systems
  (NeurIPS), 2016.
- [23]

  Kihyuk Sohn, David Berthelot, Chun-Liang Li, Zizhao Zhang, Nicholas Carlini,
  Ekin D Cubuk, Alex Kurakin, Han Zhang, and Colin Raffel.
  Fixmatch: Simplifying semi-supervised learning with consistency and
  confidence.
  In Proceedings of Advances in Neural Information Processing
  Systems (NeurIPS), 2020.
- [24]

  Antti Tarvainen and Harri Valpola.
  Mean teachers are better role models: Weight-averaged consistency
  targets improve semi-supervised deep learning results.
  arXiv preprint arXiv:1703.01780, 2017.
- [25]

  Hugo Touvron, Matthieu Cord, Matthijs Douze, Francisco Massa, Alexandre
  Sablayrolles, and Hervé Jégou.
  Training data-efficient image transformers & distillation through
  attention.
  arXiv preprint arXiv:2012.12877, 2020.
- [26]

  Xiaolong Wang, Allan Jabri, and Alexei A Efros.
  Learning correspondence from the cycle-consistency of time.
  In Proceedings of the IEEE/CVF Conference on Computer Vision and
  Pattern Recognition, pages 2566–2576, 2019.
- [27]

  Zhirong Wu, Yuanjun Xiong, Stella X Yu, and Dahua Lin.
  Unsupervised feature learning via non-parametric instance
  discrimination.
  In Proceedings of the Conference on Computer Vision and Pattern
  Recognition (CVPR), 2018.
- [28]

  Qizhe Xie, Zihang Dai Dai, Eduard Hovy, Minh-Thang Luong, and Quoc V. Le.
  Unsupervised data augmentation for consistency training.
  arXiv preprint arXiv:1904.12848, 2020.
- [29]

  Bolei Zhou, Agata Lapedriza, Jianxiong Xiao, Antonio Torralba, and Aude Oliva.
  Learning deep features for scene recognition using places database.
  In Proceedings of Advances in Neural Information Processing
  Systems (NeurIPS), 2014.
