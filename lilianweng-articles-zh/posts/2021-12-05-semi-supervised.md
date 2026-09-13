---
title: "数据不足时的学习 Part 1：半监督学习"
title_en: "Learning with not Enough Data Part 1: Semi-Supervised Learning"
source: https://lilianweng.github.io/posts/2021-12-05-semi-supervised/
crawled: 2026-09-08
translated: 2026-09-08
---

# 数据不足时的学习 Part 1：半监督学习

> 原文：[Learning with not Enough Data Part 1: Semi-Supervised Learning](https://lilianweng.github.io/posts/2021-12-05-semi-supervised/) · Lilian Weng（翁荔）

> 监督学习任务的性能随更多高质量标签的可用而提升。然而，收集大量标注样本代价高昂。机器学习中有几种范式应对标签稀缺的场景。半监督学习是候选之一：把大量无标注数据与少量标注数据结合使用。

当监督学习任务面对有限标注数据时，通常讨论四种方法。
1. *预训练 + 微调*：在大型无监督数据语料上预训练一个强大的任务无关模型，如在自由文本上[预训练语言模型](https://lilianweng.github.io/posts/2019-01-31-lm/)，或通过[自监督学习](https://lilianweng.github.io/posts/2019-11-10-self-supervised/)在无标注图像上预训练视觉模型，然后在下游任务上用少量标注样本微调。
2. *半监督学习*：同时从标注与无标注样本学习。视觉任务上这一方向已有大量研究。
3. *主动学习*：标注昂贵，但在成本预算内我们仍想收集更多。主动学习学会选择最有价值的无标注样本来收集，帮助我们在有限预算下聪明行事。
4. *预训练 + 数据集自动生成*：给定一个能力足够的预训练模型，我们可以用它自动生成多得多的标注样本。这在语言领域尤其流行，受少样本学习成功的推动。

我计划就"数据不足时的学习"写一个系列。第 1 部分是*半监督学习*。

## 什么是半监督学习？

半监督学习同时使用标注与无标注数据训练模型。

有趣的是，现有半监督学习文献大多聚焦视觉任务；而语言任务上预训练 + 微调是更常见的范式。

本文介绍的所有方法都有组合两部分的损失：$$\mathcal{L} = \mathcal{L}_s +  \mu(t) \mathcal{L}_u$$。给定全部标注样本，监督损失 $$\mathcal{L}_s$$ 容易得到。我们将聚焦无监督损失 $$\mathcal{L}_u$$ 如何设计。权重项 $$\mu(t)$$ 的常见选择是一个随时间增大 $$\mathcal{L}_u$$ 重要性的斜坡函数，$$t$$ 是训练步数。

> *免责声明*：本文不覆盖聚焦模型架构修改的半监督方法。如何在半监督学习中使用生成模型与基于图的方法，请看[这份综述](https://arxiv.org/abs/2006.05278)。

## 符号

| 符号 | 含义 |
| --- | --- |
| $$L$$ | 唯一标签数。 |
| $$(\mathbf{x}^l, y) \sim \mathcal{X}, y \in \{0, 1\}^L$$ | 标注数据集。$$y$$ 是真实标签的独热表示。|
| $$\mathbf{u} \sim \mathcal{U}$$ | 无标注数据集。|
| $$\mathcal{D} = \mathcal{X} \cup \mathcal{U}$$ | 整个数据集，含标注与无标注样本。|
| $$\mathbf{x}$$ | 任意样本，可标注也可无标注。|
| $$\bar{\mathbf{x}}$$ | 施加了数据增强的 $$\mathbf{x}$$。 |
| $$\mathbf{x}_i$$ | 第 $$i$$ 个样本。 |
| $$\mathcal{L}$$、$$\mathcal{L}_s$$、$$\mathcal{L}_u$$ | 损失、监督损失与无监督损失。 |
| $$\mu(t)$$ | 无监督损失权重，随时间增大。 |
| $$p(y \vert \mathbf{x}), p_\theta(y \vert \mathbf{x})$$ | 给定输入时标签集上的条件概率。 |
| $$f_\theta(.)$$ | 实现的权重为 $$\theta$$ 的神经网络，即我们要训练的模型。 |
| $$\mathbf{z} = f_\theta(\mathbf{x})$$ | $$f$$ 输出的 logit 向量。 |
| $$\hat{y} = \text{softmax}(\mathbf{z})$$ | 预测的标签分布。 |
| $$D[.,.]$$ | 两个分布之间的距离函数，如 MSE、交叉熵、KL 散度等。 |
| $$\beta$$ | [教师](#mean-teachers)模型权重的 EMA 加权超参数。 |
| $$\alpha, \lambda$$ | MixUp 参数，$$\lambda \sim \text{Beta}(\alpha, \alpha)$$。 |
| $$T$$ | 锐化预测分布的温度。 |
| $$\tau$$ | 选择合格预测的置信度阈值。 |

## 假设

文献中讨论了若干支持半监督学习方法中特定设计决策的假设。

- H1：**平滑性假设**：若两个数据样本在特征空间的高密度区域相近，它们的标签应相同或非常相似。

- H2：**聚类假设**：特征空间既有稠密区域也有稀疏区域。稠密聚拢的数据点自然形成簇。同一簇中的样本被期望有相同标签。这是 H1 的一个小扩展。

- H3：**低密度分离假设**：类之间的决策边界倾向位于稀疏、低密度区域，否则决策边界会把一个高密度簇切成两个类、对应两个簇，违背 H1 与 H2。

- H4：**流形假设**：高维数据倾向位于低维流形上。尽管真实世界数据可能在很高维度被观测（如真实世界物体/场景的图像），它们实际上可被一个更低维的流形捕捉——某些属性被捕捉、相似点被紧密分组（如真实世界物体/场景的图像并非从所有像素组合的均匀分布中抽取）。这使我们能学习更高效的表示，以发现和度量无标注数据点之间的相似性。这也是表示学习的基础。[见[一个有用的链接](https://stats.stackexchange.com/questions/66939/what-is-the-manifold-assumption-in-semi-supervised-learning)]。

## 一致性正则化

**一致性正则化（Consistency Regularization**，也称**一致性训练，Consistency Training**）假设：神经网络内部的随机性（如 Dropout）或数据增强变换不应改变给定相同输入时的模型预测。本节每个方法都以一致性正则化损失作为 $$\mathcal{L}_u$$。

这一思想已被多个[自监督](https://lilianweng.github.io/posts/2019-11-10-self-supervised/)[学习](https://lilianweng.github.io/posts/2021-05-31-contrastive/)方法采纳，如 SimCLR、BYOL、SimCSE 等。同一样本的不同增强版本应产生相同表示。语言建模中的[跨视图训练](https://lilianweng.github.io/posts/2019-01-31-lm/#cross-view-training)与自监督学习中的多视图学习动机相同。

### Π-模型

![Pi Model](https://lilianweng.github.io/posts/2021-12-05-semi-supervised/PI-model.png)

*图 1：Π-模型概览。同一输入的两个版本（不同随机增强与 dropout 掩码）穿过网络，输出被期望一致。（图片来源：[Laine & Aila (2017)](https://arxiv.org/abs/1610.02242)）*

[Sajjadi et al. (2016)](https://arxiv.org/abs/1606.04586) 提出一个无监督学习损失：对同一数据点，以随机变换（如 dropout、随机最大池化）两次穿过网络，最小化两次输出之差。标签未被显式使用，因此该损失可用于无标注数据集。[Laine & Aila (2017)](https://arxiv.org/abs/1610.02242) 后来为这一设定起名 **Π-模型**。

$$
\mathcal{L}_u^\Pi = \sum_{\mathbf{x} \in \mathcal{D}} \text{MSE}(f_\theta(\mathbf{x}), f'_\theta(\mathbf{x}))
$$

其中 $$f'$$ 是施加了不同随机增强或 dropout 掩码的同一神经网络。该损失利用整个数据集。

### 时间集成

![Temporal Ensembling](https://lilianweng.github.io/posts/2021-12-05-semi-supervised/temperal-ensembling.png)

*图 2：时间集成概览。每样本 EMA 标签预测是学习目标。（图片来源：[Laine & Aila (2017)](https://arxiv.org/abs/1610.02242)）*

Π-模型要求网络对每个样本跑两趟，翻倍计算成本。为降低成本，**时间集成（Temporal Ensembling**，[Laine & Aila 2017](https://arxiv.org/abs/1610.02242)）为每个训练样本维护模型预测随时间的指数滑动平均（EMA）$$\tilde{\mathbf{z}}_i$$ 作为学习目标，每轮只评估和更新一次。因为集成输出 $$\tilde{\mathbf{z}}_i$$ 初始化为 $$\mathbf{0}$$，它被 $$(1-\alpha^t)$$ 归一化以矫正这一启动偏差。Adam 优化器出于同样原因有[偏差矫正](https://stats.stackexchange.com/questions/232741/why-is-it-important-to-include-a-bias-correction-term-for-the-adam-optimizer-for)项。

$$
\tilde{\mathbf{z}}^{(t)}_i = \frac{\alpha \tilde{\mathbf{z}}^{(t-1)}_i + (1-\alpha) \mathbf{z}_i}{1-\alpha^t}
$$

其中 $$\tilde{\mathbf{z}}^{(t)}$$ 是第 $$t$$ 轮的集成预测，$$\mathbf{z}_i$$ 是当前轮的模型预测。注意由于 $$\tilde{\mathbf{z}}^{(0)} = \mathbf{0}$$，矫正后 $$\tilde{\mathbf{z}}^{(1)}$$ 在第 1 轮就简单地等价于 $$\mathbf{z}_i$$。

### 平均教师

![Mean Teacher](https://lilianweng.github.io/posts/2021-12-05-semi-supervised/mean-teacher.png)

*图 3：平均教师框架概览。（图片来源：[Tarvaninen & Valpola, 2017](https://arxiv.org/abs/1703.01780)）*

时间集成为每个训练样本跟踪标签预测的 EMA 作为学习目标。然而该标签预测*每轮*才变一次，训练集大时方法显得笨重。**平均教师（Mean Teacher**，[Tarvaninen & Valpola, 2017](https://arxiv.org/abs/1703.01780)）被提出以克服目标更新慢的问题：改为跟踪模型权重而非模型输出的滑动平均。把权重为 $$\theta$$ 的原始模型称为*学生*模型，把连续学生模型权重 $$\theta’$$ 的滑动平均称为*平均教师*：$$\theta’ \gets \beta \theta’ + (1-\beta)\theta$$

一致性正则化损失是学生与教师预测之间的距离，学生-教师差距应被最小化。平均教师被期望提供比学生更准确的预测。这在经验实验中得到确认（见图 4）。

![Mean teacher experiments](https://lilianweng.github.io/posts/2021-12-05-semi-supervised/mean-teacher-results.png)

*图 4：平均教师与 Π-模型在 SVHN 上的分类错误率。平均教师（橙色）优于学生模型（蓝色）。（图片来源：[Tarvaninen & Valpola, 2017](https://arxiv.org/abs/1703.01780)）*

根据他们的消融研究：
- 输入增强（如输入图像随机翻转、高斯噪声）或学生模型 dropout 对良好性能是必要的。教师模型不需要 dropout。
- 性能对 EMA 衰减超参数 $$\beta$$ 敏感。好策略是在爬升阶段用小 $$\beta=0.99$$，后期当学生模型改进放缓时用更大的 $$\beta=0.999$$。
- 他们发现 MSE 作为一致性代价函数优于 KL 散度等其他代价函数。

### 带噪样本作为学习目标

近期若干一致性训练方法学习最小化原始无标注样本与其增强版本之间的预测差异。这与 Π-模型相当相似，但一致性正则化损失*只*施加于无标注数据。

![Consistency training with noisy samples](https://lilianweng.github.io/posts/2021-12-05-semi-supervised/consistency-training-with-noisy-samples.png)

*图 5：用带噪样本做一致性训练。*

对抗训练（[Goodfellow et al. 2014](https://arxiv.org/abs/1412.6572)）向输入施加对抗噪声并训练模型对此类对抗攻击鲁棒。该设定在监督学习中工作：

$$
\begin{aligned}
\mathcal{L}_\text{adv}(\mathbf{x}^l, \theta) &= D[q(y\mid \mathbf{x}^l), p_\theta(y\mid \mathbf{x}^l + r_\text{adv})] \\
r_\text{adv} &= {\arg\max}_{r; \|r\| \leq \epsilon} D[q(y\mid \mathbf{x}^l), p_\theta(y\mid \mathbf{x}^l + r_\text{adv})] \\
r_\text{adv} &\approx \epsilon \frac{g}{\|g\|_2} \approx \epsilon\text{sign}(g)\quad\text{where }g = \nabla_{r} D[y, p_\theta(y\mid \mathbf{x}^l + r)]
\end{aligned}
$$

其中 $$q(y \mid \mathbf{x}^l)$$ 是真实分布，用真实标签 $$y$$ 的独热编码近似。$$p_\theta(y \mid \mathbf{x}^l)$$ 是模型预测。$$D[.,.]$$ 是度量两分布间差异的距离函数。

**虚拟对抗训练（Virtual Adversarial Training，VAT**；[Miyato et al. 2018](https://arxiv.org/abs/1704.03976)）把该思想扩展到半监督学习。因为 $$q(y \mid \mathbf{x}^l)$$ 未知，VAT 用当前权重 $$\hat{\theta}$$ 下对原始输入的当前模型预测替换它。注意 $$\hat{\theta}$$ 是模型权重的固定副本，因此不对 $$\hat{\theta}$$ 做梯度更新。

$$
\begin{aligned}
\mathcal{L}_u^\text{VAT}(\mathbf{x}, \theta) &= D[p_{\hat{\theta}}(y\mid \mathbf{x}), p_\theta(y\mid \mathbf{x} + r_\text{vadv})] \\
r_\text{vadv} &= {\arg\max}_{r; \|r\| \leq \epsilon} D[p_{\hat{\theta}}(y\mid \mathbf{x}), p_\theta(y\mid \mathbf{x} + r)]
\end{aligned}
$$

VAT 损失同时适用于标注与无标注样本。它是当前模型预测流形在每个数据点处的负平滑度度量。优化该损失促使流形更平滑。

**插值一致性训练（Interpolation Consistency Training，ICT**；[Verma et al. 2019](https://arxiv.org/abs/1903.03825)）通过加入更多数据点的插值来增强数据集，并期望模型预测与相应标签的插值一致。MixUp（[Zheng et al. 2018](https://arxiv.org/abs/1710.09412)）操作用简单加权和混合两张图像，并结合标签平滑。沿 MixUp 思想，ICT 期望预测模型在 mixup 样本上产生的标签匹配相应输入预测的插值：

$$
\begin{aligned}
\text{mixup}_\lambda (\mathbf{x}_i, \mathbf{x}_j) &= \lambda \mathbf{x}_i + (1-\lambda)\mathbf{x}_j \\
p(\text{mixup}_\lambda (y \mid \mathbf{x}_i, \mathbf{x}_j)) &\approx \lambda p(y \mid \mathbf{x}_i) + (1-\lambda) p(y \mid \mathbf{x}_j)
\end{aligned}
$$

其中 $$\theta'$$ 是 $$\theta$$ 的滑动平均，即[平均教师](#mean-teachers)。

![ICT](https://lilianweng.github.io/posts/2021-12-05-semi-supervised/ICT.png)

*图 6：插值一致性训练概览。应用 MixUp 产生更多带插值标签（作为学习目标）的插值样本。（图片来源：[Verma et al. 2019](https://arxiv.org/abs/1903.03825)）*

由于两个随机选择的无标注样本属于不同类的概率高（如 ImageNet 有 1000 个物体类），对两个随机无标注样本应用 mixup 的插值很可能发生在决策边界附近。按低密度分离[假设](#hypotheses)，决策边界倾向位于低密度区域。

$$
\mathcal{L}^\text{ICT}_{u} = \mathbb{E}_{\mathbf{u}_i, \mathbf{u}_j \sim \mathcal{U}} \mathbb{E}_{\lambda \sim \text{Beta}(\alpha, \alpha)} D[p_\theta(y \mid \text{mixup}_\lambda (\mathbf{u}_i, \mathbf{u}_j)), \text{mixup}_\lambda(p_{\theta’}(y \mid \mathbf{u}_i), p_{\theta'}(y \mid \mathbf{u}_j)]
$$

其中 $$\theta'$$ 是 $$\theta$$ 的滑动平均。

与 VAT 类似，**无监督数据增强（Unsupervised Data Augmentation，UDA**；[Xie et al. 2020](https://arxiv.org/abs/1904.12848)）学习对无标注样本与其增强版本预测相同输出。UDA 特别聚焦研究噪声的*"质量"*如何影响一致性训练下的半监督学习性能。使用先进的数据增强方法产生有意义、有效的带噪样本至关重要。好的数据增强应产生有效（即不改变标签）且多样的噪声，并携带针对性的归纳偏置。

图像上，UDA 采用 RandAugment（[Cubuk et al. 2019](https://arxiv.org/abs/1909.13719)），从 [PIL](https://pillow.readthedocs.io/en/stable/) 可用的增强操作中均匀采样，无学习或优化，因此比 AutoAugment 便宜得多。

![UDA vision](https://lilianweng.github.io/posts/2021-12-05-semi-supervised/UDA-image-results.png)

*图 7：多种半监督学习方法在 CIFAR-10 分类上的对比。完全监督的 Wide-ResNet-28-2 与 PyramidNet+ShakeDrop 在 50,000 个样本上（无 RandAugment）训练的错误率分别为 **5.4** 与 **2.7**。（图片来源：[Xie et al. 2020](https://arxiv.org/abs/1904.12848)）*

语言上，UDA 结合回译与基于 TF-IDF 的词替换。回译保留高层含义但可能不保留某些词，而基于 TF-IDF 的词替换丢弃 TF-IDF 分数低的无信息词。在语言任务实验中，他们发现 UDA 与迁移学习、表示学习互补；例如，在域内无标注数据上微调过的 BERT（即图 8 中的 $$\text{BERT}_\text{FINETUNE}$$）能进一步提升性能。

![UDA language](https://lilianweng.github.io/posts/2021-12-05-semi-supervised/UDA-language-results.png)

*图 8：UDA 以不同初始化配置在多个文本分类任务上的对比。（图片来源：[Xie et al. 2020](https://arxiv.org/abs/1904.12848)）*

计算 $$\mathcal{L}_u$$ 时，UDA 发现两个训练技巧有助于改进结果。
- *低置信度掩蔽*：掩掉预测置信度低于阈值 $$\tau$$ 的样本。
- *锐化预测分布*：softmax 中用低温度 $$T$$ 锐化预测概率分布。
- *域内数据过滤*：为从大型域外数据集中提取更多域内数据，他们训练了一个分类器预测域内标签，然后保留高置信预测的样本作为域内候选。

$$
\begin{aligned}
&\mathcal{L}_u^\text{UDA} = \mathbb{1}[\max_{y'} p_{\hat{\theta}}(y'\mid \mathbf{x}) > \tau ] \cdot D[p^\text{(sharp)}_{\hat{\theta}}(y \mid \mathbf{x}; T), p_\theta(y \mid \bar{\mathbf{x}})] \\
&\text{where } p_{\hat{\theta}}^\text{(sharp)}(y \mid \mathbf{x}; T) = \frac{\exp(z^{(y)} / T)}{ \sum_{y'} \exp(z^{(y')} / T) }
\end{aligned}
$$

其中 $$\hat{\theta}$$ 与 VAT 一样是模型权重的固定副本、不更新梯度，$$\bar{\mathbf{x}}$$ 是增强后的数据点。$$\tau$$ 是预测置信度阈值，$$T$$ 是分布锐化温度。

## 伪标签

**伪标签（Pseudo Labeling**，[Lee 2013](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.664.3543&rep=rep1&type=pdf)）基于当前模型预测的最大 softmax 概率为无标注样本分配假标签，然后在纯监督设定下同时用标注与无标注样本训练模型。

伪标签为什么会有效？伪标签实际上等价于*熵正则化（Entropy Regularization）*（[Grandvalet & Bengio 2004](https://papers.nips.cc/paper/2004/hash/96f2b50b5d3613adf9c27049b2a888c7-Abstract.html)）：最小化无标注数据类别概率的条件熵，以促成类间低密度分离。换言之，预测的类别概率实际上是类重叠的度量，最小化熵等价于减少类重叠、从而实现低密度分离。

![Pseudo labeling segregation](https://lilianweng.github.io/posts/2021-12-05-semi-supervised/pseudo-label-segregation.png)

*图 9：在 600 个标注数据外加 60000 个无标注样本上（a）不带与（b）带伪标签训练的模型在 MNIST 测试集上输出的 t-SNE 可视化。伪标签使学到的嵌入空间分离更好。（图片来源：[Lee 2013](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.664.3543&rep=rep1&type=pdf)）*

伪标签训练天然是一个迭代过程。我们把产生伪标签的模型称为教师，用伪标签学习的模型称为学生。

### 标签传播

**标签传播（Label Propagation**，[Iscen et al. 2019](https://arxiv.org/abs/1904.04717)）是基于特征嵌入在样本间构造相似图的想法。然后伪标签从已知样本"扩散"到无标注样本，传播权重与图中成对相似度分数成正比。概念上它类似 k-NN 分类器，同样有难以随大数据集扩展的问题。

![Label propagation](https://lilianweng.github.io/posts/2021-12-05-semi-supervised/label-propagation.png)

*图 10：标签传播工作方式示意。（图片来源：[Iscen et al. 2019](https://arxiv.org/abs/1904.04717)）*

### 自训练

**自训练（Self-Training）**不是新概念（[Scudder 1965](https://ieeexplore.ieee.org/document/1053799)、[Nigram & Ghani CIKM 2000](http://www.kamalnigam.com/papers/cotrain-CIKM00.pdf)）。它是一个迭代算法，在以下两步之间交替，直到每个无标注样本都被分配标签：
- 最初在标注数据上构建一个分类器。
- 然后用该分类器预测无标注数据的标签，并把最自信的转为标注样本。

[Xie et al. (2020)](https://arxiv.org/abs/1911.04252) 把自训练应用于深度学习并取得出色结果。在 ImageNet 分类任务上，他们先训练一个 EfficientNet（[Tan & Le 2019](https://arxiv.org/abs/1905.11946)）模型作为教师，为 3 亿张无标注图像生成伪标签，然后训练一个更大的 EfficientNet 作为学生，同时用真标签与伪标签图像学习。其设定的一个关键要素是：学生模型训练时有*噪声*，而教师产生伪标签时无噪声。因此他们的方法被称为**噪声学生（Noisy Student）**。他们用随机深度（[Huang et al. 2016](https://arxiv.org/abs/1603.09382)）、dropout 和 RandAugment 给学生加噪。噪声对于学生超越教师很重要。加入的噪声有复合效应，促使模型的决策边界在标注与无标注数据上都更平滑。

噪声学生自训练的其他几个重要技术配置：
- 学生模型应足够大（即大于教师）以拟合更多数据。
- 噪声学生应搭配数据均衡，尤其要均衡每个类的伪标签图像数量。
- 软伪标签优于硬伪标签。

尽管模型未针对对抗鲁棒性优化，噪声学生还提升了对抗 FGSM（Fast Gradient Sign Attack = 该攻击用损失对输入数据的梯度并调整输入数据以最大化损失）攻击的鲁棒性。

[Du et al. (2020)](https://arxiv.org/abs/2010.02194) 提出的 SentAugment 旨在解决语言域自训练时域内无标注数据不足的问题。它依靠句子嵌入从大型语料中找出无标注域内样本，并用检索到的句子做自训练。

### 减少确认偏差

确认偏差（confirmation bias）是不完美的教师模型提供错误伪标签带来的问题。过拟合错误标签未必带来更好的学生模型。

为减少确认偏差，[Arazo et al. (2019)](https://arxiv.org/abs/1908.02983) 提出两项技术。一是采用带软标签的 MixUp。给定两个样本 $$(\mathbf{x}_i, \mathbf{x}_j)$$ 及其对应的真实或伪标签 $$(y_i, y_j)$$，插值标签方程可以转化为带 softmax 输出的交叉熵损失：

$$
\begin{aligned}
&\bar{\mathbf{x}} = \lambda \mathbf{x}_i + (1-\lambda) \mathbf{x}_j \\
&\bar{y} = \lambda y_i + (1-\lambda) y_j \Leftrightarrow
\mathcal{L} = \lambda [y_i^\top \log f_\theta(\bar{\mathbf{x}})] + (1-\lambda) [y_j^\top \log f_\theta(\bar{\mathbf{x}})]
\end{aligned}
$$

标注样本太少时 MixUp 不够。他们进一步通过对标注样本过采样，为每个 mini batch 设定标注样本的最小数量。这优于上调标注样本权重，因为它带来更频繁的更新而非少数大幅更新（后者可能更不稳定）。与一致性正则化一样，数据增强和 dropout 对伪标签良好工作也很重要。

**元伪标签（Meta Pseudo Labels**，[Pham et al. 2021](https://arxiv.org/abs/2003.10580)）根据学生在标注数据集上表现如何的反馈持续调整教师模型。教师与学生并行训练：教师学习生成更好的伪标签，学生从伪标签学习。

设教师与学生模型权重分别为 $$\theta_T$$ 和 $$\theta_S$$。学生在标注样本上的损失定义为 $$\theta_T$$ 的函数 $$\theta^\text{PL}_S(.)$$，我们想通过相应优化教师模型来最小化该损失。

$$
\begin{aligned}
\min_{\theta_T} &\mathcal{L}_s(\theta^\text{PL}_S(\theta_T)) = \min_{\theta_T} \mathbb{E}_{(\mathbf{x}^l, y) \in \mathcal{X}} \text{CE}[y, f_{\theta_S}(\mathbf{x}^l)]  \\
\text{where } &\theta^\text{PL}_S(\theta_T)
= \arg\min_{\theta_S} \mathcal{L}_u (\theta_T, \theta_S)
= \arg\min_{\theta_S} \mathbb{E}_{\mathbf{u} \sim \mathcal{U}} \text{CE}[(f_{\theta_T}(\mathbf{u}), f_{\theta_S}(\mathbf{u}))]
\end{aligned}
$$

然而优化上式并不平凡。借用 [MAML](https://arxiv.org/abs/1703.03400) 的思想，用 $$\theta_S$$ 的一步梯度更新近似多步 $$\arg\min_{\theta_S}$$：

$$
\begin{aligned}
\theta^\text{PL}_S(\theta_T) &\approx \theta_S - \eta_S \cdot \nabla_{\theta_S} \mathcal{L}_u(\theta_T, \theta_S) \\
\min_{\theta_T} \mathcal{L}_s (\theta^\text{PL}_S(\theta_T)) &\approx \min_{\theta_T} \mathcal{L}_s \big( \theta_S - \eta_S \cdot \nabla_{\theta_S} \mathcal{L}_u(\theta_T, \theta_S) \big)
\end{aligned}
$$

用软伪标签时上述目标可微。但若用硬伪标签，它不可微，因此需要用 RL，如 REINFORCE。

优化过程在训练两个模型之间交替：
- *学生模型更新*：给定一批无标注样本 $$\{ \mathbf{u} \}$$，我们用 $$f_{\theta_T}(\mathbf{u})$$ 生成伪标签，用一步 SGD 优化 $$\theta_S$$：$$\theta’_S = \color{green}{\theta_S - \eta_S \cdot \nabla_{\theta_S} \mathcal{L}_u(\theta_T, \theta_S)}$$。
- *教师模型更新*：给定一批标注样本 $$\{(\mathbf{x}^l, y)\}$$，我们复用学生的更新来优化 $$\theta_T$$：$$\theta’_T = \theta_T  - \eta_T \cdot \nabla_{\theta_T} \mathcal{L}_s ( \color{green}{\theta_S - \eta_S \cdot \nabla_{\theta_S} \mathcal{L}_u(\theta_T, \theta_S)} )$$。此外，UDA 目标被施加于教师模型以纳入一致性正则化。

![MPL experiment results](https://lilianweng.github.io/posts/2021-12-05-semi-supervised/MPL-results.png)

*图 11：元伪标签与其他半监督或自监督学习方法在图像分类任务上的对比。（图片来源：[Pham et al. 2021](https://arxiv.org/abs/2003.10580)）*

## 伪标签 + 一致性正则化

可以把上述两种方法结合，同时用伪标签与一致性训练运行半监督学习。

### MixMatch

**MixMatch**（[Berthelot et al. 2019](https://arxiv.org/abs/1905.02249)）作为半监督学习的整体性方法，通过融合以下技术利用无标注数据：
1. *一致性正则化*：鼓励模型对扰动后的无标注样本输出相同预测。
2. *熵最小化*：鼓励模型对无标注数据输出自信预测。
3. *MixUp* 增强：鼓励模型在样本间具有线性行为。

给定一批标注数据 $$\mathcal{X}$$ 与无标注数据 $$\mathcal{U}$$，我们通过 $$\text{MixMatch}(.)$$ 创建它们的增强版本 $$\bar{\mathcal{X}}$$ 与 $$\bar{\mathcal{U}}$$，含增强样本及无标注样本的猜测标签。

$$
\begin{aligned}
\bar{\mathcal{X}}, \bar{\mathcal{U}} &= \text{MixMatch}(\mathcal{X}, \mathcal{U}, T, K, \alpha) \\
\mathcal{L}^\text{MM}_s &= \frac{1}{\vert \bar{\mathcal{X}} \vert} \sum_{(\bar{\mathbf{x}}^l, y)\in \bar{\mathcal{X}}} D[y, p_\theta(y \mid \bar{\mathbf{x}}^l)] \\
\mathcal{L}^\text{MM}_u &= \frac{1}{L\vert \bar{\mathcal{U}} \vert} \sum_{(\bar{\mathbf{u}}, \hat{y})\in \bar{\mathcal{U}}} \| \hat{y} - p_\theta(y \mid \bar{\mathbf{u}}) \|^2_2 \\
\end{aligned}
$$

其中 $$T$$ 是降低猜测标签重叠的锐化温度；$$K$$ 是每个无标注样本生成的增强数；$$\alpha$$ 是 MixUp 的参数。

对每个 $$\mathbf{u}$$，MixMatch 生成 $$K$$ 个增强 $$\bar{\mathbf{u}}^{(k)} = \text{Augment}(\mathbf{u})$$（$$k=1, \dots, K$$），伪标签基于平均猜测：$$\hat{y} = \frac{1}{K} \sum_{k=1}^K p_\theta(y \mid \bar{\mathbf{u}}^{(k)})$$。

![MixMatch](https://lilianweng.github.io/posts/2021-12-05-semi-supervised/MixMatch.png)

*图 12：MixMatch 中"标签猜测"的过程：平均 $$K$$ 个增强、矫正预测边缘分布、最后锐化分布。（图片来源：[Berthelot et al. 2019](https://arxiv.org/abs/1905.02249)）*

根据他们的消融研究，MixUp 尤其在无标注数据上至关重要。去除伪标签分布的温度锐化大幅损害性能。标签猜测时对多个增强取平均也是必要的。

**ReMixMatch**（[Berthelot et al. 2020](https://arxiv.org/abs/1911.09785)）通过引入两个新机制改进 MixMatch：

![ReMixMatch](https://lilianweng.github.io/posts/2021-12-05-semi-supervised/ReMixMatch.png)

*图 13：ReMixMatch 相对 MixMatch 引入的两项改进示意。（图片来源：[Berthelot et al. 2020](https://arxiv.org/abs/1911.09785)）*

- *分布对齐（Distribution alignment）*。它鼓励边缘分布 $$p(y)$$ 接近真实标签的边缘分布。设 $$p(y)$$ 是真实标签中的类别分布，$$\tilde{p}(\hat{y})$$ 是无标注数据中预测类别分布的滑动平均。对无标注样本的模型预测 $$p_\theta(y \vert \mathbf{u})$$ 被归一化为 $$\text{Normalize}\big( \frac{p_\theta(y \vert \mathbf{u}) p(y)}{\tilde{p}(\hat{y})} \big)$$ 以匹配真实边缘分布。
    - 注意若边缘分布不均匀，熵最小化不是有用的目标。
    - 我确实觉得"标注与无标注数据上的类别分布应匹配"这一假设太强，真实世界设定中未必成立。
- *增强锚定（Augmentation anchoring）*。给定一个无标注样本，先用弱增强生成一个"锚"版本，再用 CTAugment（Control Theory Augment）平均 $$K$$ 个强增强版本。CTAugment 只采样保持模型预测在网络容忍度内的增强。

ReMixMatch 损失是若干项的组合：
- 施加数据增强与 MixUp 的监督损失；
- 施加数据增强与 MixUp、以伪标签为目标的非监督损失；
- 对单张重度增强、未用 MixUp 的无标注图像的 CE 损失；
- 自监督学习中的[旋转](https://lilianweng.github.io/posts/2019-11-10-self-supervised/#distortion)损失。

### DivideMix

**DivideMix**（[Junnan Li et al. 2020](https://arxiv.org/abs/2002.07394)）把半监督学习与带噪标签学习（LNL）结合。它用 [GMM](https://scikit-learn.org/stable/modules/mixture.html) 建模每样本损失分布，把训练数据动态划分为含干净样本的标注集与含噪声样本的无标注集。沿 [Arazo et al. 2019](https://arxiv.org/abs/1904.11238) 的思路，他们对每样本交叉熵损失 $$\ell_i = y_i^\top \log f_\theta(\mathbf{x}_i)$$ 拟合一个双分量 GMM。干净样本预期比噪声样本更快获得更低损失。均值较小的分量是对应干净标签的簇，记作 $$c$$。若 GMM 后验概率 $$w_i = p_\text{GMM}(c \mid \ell_i)$$（即样本属于干净样本集的概率）大于阈值 $$\tau$$，该样本被视为干净样本，否则为噪声样本。

数据聚类步骤被命名为*协同划分（co-divide）*。为避免确认偏差，DivideMix 同时训练两个分叉的网络，每个网络使用另一网络的数据集划分；可类比 Double Q Learning 的工作方式。

![DivideMix](https://lilianweng.github.io/posts/2021-12-05-semi-supervised/DivideMix.png)

*图 14：DivideMix 独立训练两个网络以减少确认偏差。它们一起运行协同划分、协同精炼与协同猜测。（图片来源：[Junnan Li et al. 2020](https://arxiv.org/abs/2002.07394)）*

与 MixMatch 相比，DivideMix 多了一个处理噪声样本的*协同划分*阶段，以及训练中的以下改进：
- *标签协同精炼（Label co-refinement）*：把真实标签 $$y_i$$ 与网络预测 $$\hat{y}_i$$ 线性组合——后者在 $$\mathbf{x}_i$$ 的多个增强上取平均——由另一网络产生的干净集概率 $$w_i$$ 引导。
- *标签协同猜测（Label co-guessing）*：对无标注数据样本平均两个模型的预测。

![Algorithm of DivideMix](https://lilianweng.github.io/posts/2021-12-05-semi-supervised/DivideMix-algo.png)

*图 15：DivideMix 算法。（图片来源：[Junnan Li et al. 2020](https://arxiv.org/abs/2002.07394)）*

### FixMatch

**FixMatch**（[Sohn et al. 2020](https://arxiv.org/abs/2001.07685)）对无标注样本用弱增强生成伪标签，只保留高置信预测。弱增强与高置信过滤都帮助产生高质量、可信的伪标签目标。然后 FixMatch 学习在重度增强样本上预测这些伪标签。

![FixMatch](https://lilianweng.github.io/posts/2021-12-05-semi-supervised/FixMatch.png)

*图 16：FixMatch 工作方式示意。（图片来源：[Sohn et al. 2020](https://arxiv.org/abs/2001.07685)）*

$$
\begin{aligned}
\mathcal{L}_s &= \frac{1}{B} \sum^B_{b=1} \text{CE}[y_b, p_\theta(y \mid \mathcal{A}_\text{weak}(\mathbf{x}_b))] \\
\mathcal{L}_u &= \frac{1}{\mu B} \sum_{b=1}^{\mu B} \mathbb{1}[\max(\hat{y}_b) \geq \tau]\;\text{CE}(\hat{y}_b, p_\theta(y \mid \mathcal{A}_\text{strong}(\mathbf{u}_b)))
\end{aligned}
$$

其中 $$\hat{y}_b$$ 是无标注样本的伪标签；$$\mu$$ 是决定 $$\mathcal{X}$$ 与 $$\mathcal{U}$$ 相对大小的超参数。
- 弱增强 $$\mathcal{A}_\text{weak}(.)$$：标准的翻转-平移增强
- 强增强 $$\mathcal{A}_\text{strong}(.)$$：AutoAugment、Cutout、RandAugment、CTAugment

![FixMatch results](https://lilianweng.github.io/posts/2021-12-05-semi-supervised/FixMatch-results.png)

*图 17：FixMatch 与若干其他半监督学习方法在图像分类任务上的性能。（图片来源：[Sohn et al. 2020](https://arxiv.org/abs/2001.07685)）*

根据 FixMatch 的消融研究：
- 使用阈值 $$\tau$$ 时，用温度参数 $$T$$ 锐化预测分布没有显著影响。
- Cutout 与 CTAugment 作为强增强的一部分对好性能必要。
- 当标签猜测的弱增强换成强增强时，模型训练早期发散。若完全丢弃弱增强，模型过拟合猜测标签。
- 伪标签预测用弱而非强增强导致性能不稳定。强数据增强至关重要。

## 与强大预训练结合

尤其语言任务中，常见范式是先通过自监督学习在大型无监督数据语料上预训练任务无关模型，然后在下游任务上用小标注数据集微调。研究表明，把半监督学习与预训练结合可获得额外收益。

[Zoph et al. (2020)](https://arxiv.org/abs/2006.06882) 研究了[自训练](#self-training)在何种程度上比预训练更好。其实验设定是用 ImageNet 做预训练或自训练来改进 COCO。注意用 ImageNet 做自训练时，它丢弃标签、只把 ImageNet 样本当作无标注数据点。[He et al. (2018)](https://arxiv.org/abs/1811.08883) 已证明若下游任务差异很大（如目标检测），ImageNet 分类预训练效果不佳。

![self-training-pre-training](https://lilianweng.github.io/posts/2021-12-05-semi-supervised/self-training-pre-training.png)

*图 18：(a) 数据增强（从弱到强）与 (b) 标注数据集大小对目标检测性能的影响。图例中：`Rand Init` 指随机权重初始化的模型；`ImageNet` 用 84.5% top-1 ImageNet 准确率的预训练检查点初始化；`ImageNet++` 用更高准确率 86.9% 的检查点初始化。（图片来源：[Zoph et al. 2020](https://arxiv.org/abs/2006.06882)）*

他们的实验展示了一系列有趣的发现：
- 随下游任务可用标注样本增多，预训练的有效性递减。预训练在低数据区间（20%）有帮助，在高数据区间中性或有害。
- 自训练在高数据/强增强区间有帮助，即使预训练有害时亦然。
- 自训练可在预训练之上带来叠加改进，即使使用同一数据源。
- 自监督预训练（如经 SimCLR）在高数据区间损害性能，与监督预训练类似。
- 联合训练监督与自监督目标帮助解决预训练与下游任务间的失配。预训练、联合训练与自训练都是可叠加的。
- 噪声标签或非定向标注（即预训练标签与下游任务标签不对齐）比定向伪标注更差。
- 自训练在计算上比在预训练模型上微调更贵。

[Chen et al. (2020)](https://arxiv.org/abs/2006.10029) 提出三步流程，融合自监督预训练、监督微调与自训练的收益：
1. 无监督或自监督预训练一个大模型。
2. 在少量标注样本上监督微调。使用大（深且宽）的神经网络很重要。*更大的模型用更少标注样本取得更好性能。*
3. 通过在自训练中采用伪标签，用无标注样本做蒸馏。
   - 可以把知识从大模型蒸馏进小模型，因为任务专属使用不需要所学表示的额外容量。
   - 蒸馏损失形如如下，教师网络以固定权重 $$\hat{\theta}_T$$。

     $$
     \mathcal{L}_\text{distill} = - (1-\alpha) \underbrace{\sum_{(\mathbf{x}^l_i, y_i) \in \mathcal{X}} \big[ \log p_{\theta_S}(y_i \mid \mathbf{x}^l_i) \big]}_\text{Supervised loss} - \alpha \underbrace{\sum_{\mathbf{u}_i \in \mathcal{U}} \Big[ \sum_{i=1}^L p_{\hat{\theta}_T}(y^{(i)} \mid \mathbf{u}_i; T) \log p_{\theta_S}(y^{(i)} \mid \mathbf{u}_i; T) \Big]}_\text{Distillation loss using unlabeled data}
     $$

![big-self-supervised-model](https://lilianweng.github.io/posts/2021-12-05-semi-supervised/big-self-supervised-model.png)

*图 19：一个半监督学习框架通过（左）任务无关的无监督预训练与（右）任务专属的自训练和蒸馏来利用无标注数据语料。（图片来源：[Chen et al. 2020](https://arxiv.org/abs/2006.10029)）*

他们在 ImageNet 分类任务上实验。自监督预训练用 SimCLRv2，即 [SimCLR](https://lilianweng.github.io/posts/2021-05-31-contrastive/#simclr) 的直接改进版。经验研究中的观察确认了几条经验，与 [Zoph et al. 2020](https://arxiv.org/abs/2006.06882) 一致：
- 更大的模型更省标签；
- SimCLR 中更大/更深的投影头改进表示学习；
- 用无标注数据蒸馏改进半监督学习。

![big-self-supervised-model-results](https://lilianweng.github.io/posts/2021-12-05-semi-supervised/big-self-supervised-model-results.png)

*图 20：SimCLRv2 + 半监督蒸馏在 ImageNet 分类上的性能对比。（图片来源：[Chen et al. 2020](https://arxiv.org/abs/2006.10029)）*

---
💡 近期半监督学习方法的共同主题速览（许多旨在减少确认偏差）：
- 用先进的数据增强方法对样本施加有效且多样的噪声。
- 处理图像时，MixUp 是有效的增强。MixUp 也能用于语言，带来小幅增量改进（[Guo et al. 2019](https://arxiv.org/abs/1905.08941)）。
- 设定阈值，丢弃低置信度的伪标签。
- 设定每个 mini-batch 的最小标注样本数。
- 锐化伪标签分布以减少类重叠。

---
引用格式：
```
@article{weng2021semi,
  title   = "Learning with not Enough Data Part 1: Semi-Supervised Learning",
  author  = "Weng, Lilian",
  journal = "lilianweng.github.io/lil-log",
  year    = "2021",
  url     = "https://lilianweng.github.io/lil-log/2021/12/05/semi-supervised-learning.html"
}
```

## 参考文献

[1] Ouali, Hudelot & Tami. ["An Overview of Deep Semi-Supervised Learning"](https://arxiv.org/abs/2006.05278) arXiv preprint arXiv:2006.05278 (2020).

[2] Sajjadi, Javanmardi & Tasdizen ["Regularization With Stochastic Transformations and Perturbations for Deep Semi-Supervised Learning."](https://arxiv.org/abs/1606.04586) arXiv preprint arXiv:1606.04586 (2016).

[3] Pham et al. ["Meta Pseudo Labels."](https://arxiv.org/abs/2003.10580) CVPR 2021.

[4] Laine & Aila. ["Temporal Ensembling for Semi-Supervised Learning"](https://arxiv.org/abs/1610.02242) ICLR 2017.

[5] Tarvaninen & Valpola. ["Mean teachers are better role models: Weight-averaged consistency targets improve semi-supervised deep learning results."](https://arxiv.org/abs/1703.01780) NeuriPS 2017 

[6] Xie et al. ["Unsupervised Data Augmentation for Consistency Training."](https://arxiv.org/abs/1904.12848) NeuriPS 2020.

[7] Miyato et al. ["Virtual Adversarial Training: A Regularization Method for Supervised and Semi-Supervised Learning."](https://arxiv.org/abs/1704.03976) IEEE transactions on pattern analysis and machine intelligence 41.8 (2018).

[8] Verma et al. ["Interpolation consistency training for semi-supervised learning."](https://arxiv.org/abs/1903.03825) IJCAI 2019 

[9] Lee. ["Pseudo-label: The simple and efficient semi-supervised learning method for deep neural networks."](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.664.3543&rep=rep1&type=pdf) ICML 2013 Workshop: Challenges in Representation Learning.

[10] Iscen et al. ["Label propagation for deep semi-supervised learning."](https://arxiv.org/abs/1904.04717) CVPR 2019.

[11] Xie et al. ["Self-training with Noisy Student improves ImageNet classification"](https://arxiv.org/abs/1911.04252) CVPR 2020.

[12] Jingfei Du et al. ["Self-training Improves Pre-training for Natural Language Understanding."](https://arxiv.org/abs/2010.02194) 2020

[13] Iscen et al. ["Label propagation for deep semi-supervised learning."](https://arxiv.org/abs/1904.04717) CVPR 2019

[14] Arazo et al. ["Pseudo-labeling and confirmation bias in deep semi-supervised learning."](https://arxiv.org/abs/1908.02983) IJCNN 2020.

[15] Berthelot et al. ["MixMatch: A holistic approach to semi-supervised learning."](https://arxiv.org/abs/1905.02249) NeuriPS 2019

[16] Berthelot et al. ["ReMixMatch: Semi-supervised learning with distribution alignment and augmentation anchoring."](https://arxiv.org/abs/1911.09785) ICLR 2020

[17] Sohn et al. ["FixMatch: Simplifying semi-supervised learning with consistency and confidence."](https://arxiv.org/abs/2001.07685)  CVPR 2020

[18] Junnan Li et al. ["DivideMix: Learning with Noisy Labels as Semi-supervised Learning."](https://arxiv.org/abs/2002.07394)  2020 [[code](https://github.com/LiJunnan1992/DivideMix)]

[19] Zoph et al. ["Rethinking pre-training and self-training."](https://arxiv.org/abs/2006.06882) 2020.

[20] Chen et al. ["Big Self-Supervised Models are Strong Semi-Supervised Learners"](https://arxiv.org/abs/2006.10029) 2020
