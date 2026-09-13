---
title: "数据不足时的学习 Part 2：主动学习"
title_en: "Learning with not Enough Data Part 2: Active Learning"
source: https://lilianweng.github.io/posts/2022-02-20-active-learning/
crawled: 2026-09-08
translated: 2026-09-08
---

# 数据不足时的学习 Part 2：主动学习

> 原文：[Learning with not Enough Data Part 2: Active Learning](https://lilianweng.github.io/posts/2022-02-20-active-learning/) · Lilian Weng（翁荔）

> 监督学习任务的性能会随着更多高质量标签变得可用而提升。然而，收集大量标注样本代价高昂。主动学习（active learning）是应对标注数据不足的一种范式：当我们有资源继续标注更多数据样本、但预算有限时，它便能派上用场。

本文是「监督学习任务面对有限标注数据时该怎么办」系列的第 2 部分。这一次我们会引入一定量的人工标注工作，但要控制在预算上限之内，因此在选择标注哪些样本时必须足够聪明。

## 符号

| 符号 | 含义 |
| --- | --- |
| $$K$$ | 唯一类别标签数。 |
| $$(\mathbf{x}^l, y) \sim \mathcal{X}, y \in \{0, 1\}^K$$ | 已标注数据集。$$y$$ 是真实标签的独热表示。|
| $$\mathbf{u} \sim \mathcal{U}$$ | 无标注数据集。|
| $$\mathcal{D} = \mathcal{X} \cup \mathcal{U}$$ | 整个数据集，包含已标注与无标注样本。|
| $$\mathbf{x}$$ | 任意样本，可以是已标注的，也可以是无标注的。|
| $$\mathbf{x}_i$$ | 第 $$i$$ 个样本。 |
| $$U(\mathbf{x})$$ | 主动学习选择所用的评分函数。 |
| $$P_\theta(y \vert \mathbf{x})$$ | 由 $$\theta$$ 参数化的 softmax 分类器。 |
| $$\hat{y} = \arg\max_{y \in \mathcal{Y}} P_\theta(y \vert \mathbf{x})$$ | 分类器置信度最高的预测。 |
| $$B$$ | 标注预算（最多可标注的样本数）。 |
| $$b$$ | 批次大小。 |

## 什么是主动学习？

给定无标注数据集 $$\mathcal{U}$$ 与固定的标注开销 $$B$$，主动学习的目标是从 $$\mathcal{U}$$ 中挑选出 $$B$$ 个样本送去标注，使其带来模型性能的最大化提升。在数据标注既困难又昂贵的场景下（例如医学影像），这是一种行之有效的学习方式。2010 年的这篇经典[综述论文](https://burrsettles.com/pub/settles.activelearning.pdf)列举了许多关键概念。尽管其中一些传统方法未必适用于深度学习，本文的讨论主要聚焦于深度神经模型与批量（batch）模式下的训练。

![Active learning workflow](https://lilianweng.github.io/posts/2022-02-20-active-learning/active-learning-workflow.png)

*图 1：主动学习循环工作流示意：通过聪明地选择要标注的样本，更高效地训练出更好的模型。*

为简化讨论，我们在后续所有章节中都假设任务是一个 $$K$$ 类分类问题。参数为 $$\theta$$ 的模型在候选标签上输出一个概率分布 $$P_\theta(y \vert \mathbf{x})$$（它可能经过校准，也可能没有），最可能的预测为 $$\hat{y} = \arg\max_{y \in \mathcal{Y}} P_\theta(y \vert \mathbf{x})$$。

## 采集函数

识别下一批最值得标注的样本的过程被称为「采样策略」（sampling strategy）或「查询策略」（query strategy）。采样过程中的评分函数称为「采集函数」（acquisition function），记为 $$U(\mathbf{x})$$。得分更高的数据点一旦获得标注，预期可为模型训练带来更高的价值。

以下列出一些基本的采样策略。

### 不确定性采样

**不确定性采样**（uncertainty sampling）挑选模型预测最不确定的那些样本。在只给定单个模型的情况下，可以用预测概率来估计不确定性，不过一个常见的抱怨是：深度学习模型的预测往往未经校准，与真实不确定性关联不佳。事实上，深度学习模型常常过度自信。
- *最不置信分数*（least confident score），又称*变异比率*（variation ratio）：$$U(\mathbf{x}) = 1 - P_\theta(\hat{y} \vert \mathbf{x})$$。
- *边际分数*（margin score）：$$U(\mathbf{x}) = P_\theta(\hat{y}_1 \vert \mathbf{x}) - P_\theta(\hat{y}_2 \vert \mathbf{x})$$，其中 $$\hat{y}_1$$ 与 $$\hat{y}_2$$ 分别是可能性最高与第二高的预测标签。
- *熵*：$$U(\mathbf{x}) = \mathcal{H}(P_\theta(y \vert \mathbf{x})) = - \sum_{y \in \mathcal{Y}} P_\theta(y \vert \mathbf{x}) \log P_\theta(y \vert \mathbf{x})$$。

另一种量化不确定性的方式是依赖一个由多个专家模型组成的委员会，称为委员会查询（Query-By-Committee，QBC）。QBC 基于一组意见来度量不确定性，因此让委员会成员之间保持一定程度的分歧至关重要。设委员会池中共有 $$C$$ 个模型，分别由 $$\theta_1, \dots, \theta_C$$ 参数化。
- *投票者熵*（voter entropy）：$$U(\mathbf{x}) = \mathcal{H}(\frac{V(y)}{C})$$，其中 $$V(y)$$ 统计委员会投给标签 $$y$$ 的票数。
- *共识熵*（consensus entropy）：$$U(\mathbf{x}) = \mathcal{H}(P_\mathcal{C})$$，其中 $$P_\mathcal{C}$$ 是委员会各模型预测的平均。
- *KL 散度*：$$U(\mathbf{x}) = \frac{1}{C} \sum_{c=1}^C D_\text{KL} (P_{\theta_c} \| P_\mathcal{C})$$

### 多样性采样

**多样性采样**（diversity sampling）希望找到一组能够很好地代表整个数据分布的样本。多样性之所以重要，是因为我们期望模型在现实世界中的任何数据上都表现良好，而不只是在某个狭窄子集上。被选中的样本应当能代表底层分布。常见做法通常依赖量化样本之间的相似度。

### 期望模型变化

**期望模型变化**（expected model change）指一个样本给模型训练带来的影响。这种影响既可以是对模型权重的作用，也可以是对训练损失的改进。[后文一节](#measuring-training-effects)回顾了若干关于如何度量被选数据样本所触发模型影响的工作。

### 混合策略

上述许多方法并不互斥。**混合**（hybrid）采样策略看重数据点的不同属性，把多种采样偏好组合为一体。我们常常希望选出<mark>不确定但同时也高度有代表性</mark>的样本。

## 深度采集函数

### 度量不确定性

模型不确定性通常被归为两类（[Der Kiureghian & Ditlevsen 2009](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.455.9057&rep=rep1&type=pdf)、[Kendall & Gal 2017](https://arxiv.org/abs/1703.04977)）：
- *偶然不确定性*（aleatoric uncertainty）由数据中的噪声引入（例如传感器数据、测量过程中的噪声），它可以依赖于输入，也可以不依赖于输入。由于缺少关于真实标签的信息，它通常被认为是不可消除的。
- *认知不确定性*（epistemic uncertainty）指模型参数自身的不确定性，因此我们并不知道模型是否能最好地解释数据。理论上，这类不确定性会随着数据增多而降低。

#### 集成与近似集成

机器学习中利用集成（ensemble）提升模型性能的传统由来已久。当模型之间存在显著多样性时，集成有望带来更好的结果。这一集成理论已被许多机器学习算法证实；例如，[AdaBoost](https://en.wikipedia.org/wiki/AdaBoost) 聚合许多弱学习器，达到与单个强学习器相当甚至更好的表现；[自助法](https://en.wikipedia.org/wiki/Bootstrapping_(statistics))（Bootstrapping）通过集成多次重采样试验来更准确地估计指标。随机森林和 [GBM](https://en.wikipedia.org/wiki/Gradient_boosting) 也是体现集成有效性的好例子。

为了得到更好的不确定性估计，一个直觉的做法是聚合一组独立训练的模型。然而，训练单个深度神经网络模型的成本已经很高，更不用说训练许多个了。在强化学习中，Bootstrapped DQN（[Osband, et al. 2016](https://arxiv.org/abs/1602.04621)）配备了多个价值头，依靠 Q 值近似集成之间的不确定性来引导强化学习中的[探索](https://lilianweng.github.io/posts/2020-06-07-exploration-drl/#q-value-exploration)。

在主动学习中，一种更常见的做法是用 *dropout* 来「模拟」概率高斯过程（[Gal & Ghahramani 2016](https://arxiv.org/abs/1506.02142)）。于是，我们在前向传播中对同一个模型施加不同的 dropout 掩码、收集多次采样并加以集成，以此来估计模型不确定性（认知不确定性）。该过程被称为 **MC dropout**（蒙特卡洛 dropout）：在每个权重层之前都施加 dropout，并被证明在数学上等价于对概率深度高斯过程的一种近似（[Gal & Ghahramani 2016](https://arxiv.org/abs/1506.02157)）。这一简单思路已被证明对小数据集上的分类任务行之有效，并被广泛用于需要高效估计模型不确定性的场景。

**DBAL**（深度贝叶斯主动学习；[Gal et al. 2017](https://arxiv.org/abs/1703.02910)）用 MC dropout 近似贝叶斯神经网络，从而学到模型权重上的一个分布。在他们的实验中，MC dropout 的表现优于随机基线和平均标准差（Mean STD），与变异比和熵度量的表现相近。

![DBAL experiment](https://lilianweng.github.io/posts/2022-02-20-active-learning/DBAL-exp.png)

*图 2：DBAL 在 MNIST 上的主动学习结果。（图片来源：[Gal et al. 2017](https://arxiv.org/abs/1703.02910)）*

[Beluch et al. (2018)](https://openaccess.thecvf.com/content_cvpr_2018/papers/Beluch_The_Power_of_CVPR_2018_paper.pdf) 将基于集成的模型与 MC dropout 进行了比较，发现朴素集成（即分别独立地训练多个模型）与变异比相结合，能得到比其他组合校准更好的预测。然而，朴素集成的开销*非常*昂贵，因此他们探索了几种更便宜的替代方案：
- 快照集成（snapshot ensemble）：使用循环学习率调度来训练一个隐式集成，使其收敛到不同的局部极小值。
- 鼓励多样性的集成（diversity encouraging ensemble，DEE）：将一个只训练了少量轮数的基网络作为 $$n$$ 个不同网络的初始化，每个网络在训练时都带 dropout 以鼓励多样性。
- 分头（split head）方法：一个基模型带有多个头，每个头对应一个分类器。

遗憾的是，上述所有廉价的隐式集成方案的表现都不如朴素集成。考虑到计算资源的限制，MC dropout 仍然是一个相当不错且经济的选择。自然而然地，人们也尝试将集成与 MC dropout 结合起来（[Pop & Fulop 2018](https://arxiv.org/abs/1811.03897)），通过随机化集成获得一点额外的性能增益。

#### 参数空间中的不确定性

**Bayes-by-backprop**（[Blundell et al. 2015](https://arxiv.org/abs/1505.05424)）直接度量神经网络中的权重不确定性。该方法在权重 $$\mathbf{w}$$ 上维护一个概率分布；由于真实后验 $$p(\mathbf{w} \vert \mathcal{D})$$ 无法直接求解，它被建模为变分分布 $$q(\mathbf{w} \vert \theta)$$。损失即最小化 $$q(\mathbf{w} \vert \theta)$$ 与 $$p(\mathbf{w} \vert \mathcal{D})$$ 之间的 KL 散度，

$$
\begin{aligned}
\mathcal{L}(\theta)
&= \text{KL}[q(\mathbf{w}\vert\theta) \| p(\mathbf{w} \vert \mathcal{D})] \\ 
&= \int q(\mathbf{w}\vert\theta) \log \frac{q(\mathbf{w}\vert\theta)}{p(\mathbf{w}) p(\mathcal{D}\vert \mathbf{w})} d\mathbf{w} \\ 
&= \text{KL}[q(\mathbf{w}\vert\theta) \| p(w)] - \mathbb{E}_{q(\mathbf{w}\vert\theta)} [\log p(\mathcal{D} \vert \mathbf{w})] \\
&\approx \log q(\mathbf{w} \vert \theta) - \log p(\mathbf{w}) p(\mathcal{D}\vert \mathbf{w}) & \text{; monte carlo sampling; }q(\mathbf{w} \vert \theta)\text{ & }p(\mathbf{w})\text{ are close.}
\end{aligned}
$$

变分分布 $$q$$ 通常是对角协方差高斯分布，每个权重采样自 $$\mathcal{N}(\mu_i, \sigma_i^2)$$。为确保 $$\sigma_i$$ 非负，进一步用 softplus 参数化：$$\sigma_i = \log(1 + \exp(\rho_i))$$，其中变分参数为 $$\theta = \{\mu_i , \rho_i\}^d_{i=1}$$。

Bayes-by-backprop 的流程可以概括为：
1. 采样 $$\epsilon \sim \mathcal{N}(0, I)$$
2. 令 $$\mathbf{w} = \mu + \log(1+ \exp(\rho)) \circ \epsilon$$
3. 令 $$\theta = (\mu, \rho)$$
4. 令 $$f(\mathbf{w}, \theta) = \log q(\mathbf{w} \vert \theta) - \log p(\mathbf{w})p(\mathcal{D}\vert \mathbf{w})$$
5. 计算 $$f(\mathbf{w}, \theta)$$ 对 $$\mu$$ 和 $$\rho$$ 的梯度，然后更新 $$\theta$$。
6. 在推断阶段通过采样不同的模型权重来度量不确定性。

#### 损失预测

损失目标引导着模型训练。较低的损失值表明模型能够做出良好而准确的预测。[Yoo & Kweon (2019)](https://arxiv.org/abs/1905.03677) 设计了一个**损失预测模块**（loss prediction module），用来预测无标注输入的损失值，作为模型在给定数据上预测好坏程度的一种估计。若损失预测模块对某些样本给出不确定的预测（损失值高），这些样本就会被选中。损失预测模块是一个带 dropout 的简单 MLP，以若干中间层特征作为输入，并经全局平均池化后将它们拼接起来。

![loss prediction in active learning](https://lilianweng.github.io/posts/2022-02-20-active-learning/active-learning-loss-prediction.png)

*图 3：使用带损失预测模块的模型进行主动学习选择。（图片来源：[Yoo & Kweon 2019](https://arxiv.org/abs/1905.03677)）*

设 $$\hat{l}$$ 为损失预测模块的输出，$$l$$ 为真实损失。训练损失预测模块时，简单的 MSE 损失 $$=(l - \hat{l})^2$$ 并不是好的选择，因为随着模型学得越来越好，损失会随时间下降。一个好的学习目标应当不受目标损失尺度变化的影响。他们转而依赖样本对之间的比较。在每个大小为 $$b$$ 的批次内共有 $$b/2$$ 对样本 $$(\mathbf{x}_i, \mathbf{x}_j)$$，期望损失预测模型能正确预测哪个样本的损失更大。

$$
\begin{aligned}
\mathcal{L}_\text{loss}(\mathbf{x}_i, \mathbf{x}_j) &= \max\big( 0, -\mathbb{1}(l(\mathbf{x}_i), l(\mathbf{x}_j)) \cdot (\hat{l}(\mathbf{x}_i) - \hat{l}(\mathbf{x}_j)) + \epsilon \big) \\ 
\text{where } \mathbb{1}(l_i, l_j) &= \begin{cases} +1 & \text{if }l_i > l_j \\ -1 & \text{otherwise} \end{cases} 
\end{aligned}
$$

其中 $$\epsilon$$ 是预定义的正常数边际。

在三个视觉任务的实验中，基于损失预测的主动学习选择优于随机基线、基于熵的采集以及[核心集](#core-sets-approach)方法。

![loss prediction active learning experiments](https://lilianweng.github.io/posts/2022-02-20-active-learning/active-learning-loss-prediction-exp.png)

*图 4：基于损失预测模块的主动学习选择结果，与其他方法的对比。（图片来源：[Yoo & Kweon 2019](https://arxiv.org/abs/1905.03677)）*

#### 对抗式设置

[Sinha et al. (2019)](https://arxiv.org/abs/1904.00370) 提出了一种类似 GAN 的设置，称为 **VAAL**（变分对抗主动学习，Variational Adversarial Active Learning），其中一个判别器被训练来区分无标注数据与已标注数据。有趣的是，VAAL 中的主动学习采集准则并不依赖于任务性能。

![VAAL](https://lilianweng.github.io/posts/2022-02-20-active-learning/VAAL.png)

*图 5：VAAL（变分对抗主动学习）示意。（图片来源：[Sinha et al. 2019](https://arxiv.org/abs/1904.00370)）*

- $$\beta$$-VAE 分别为已标注和无标注数据学习一个潜在特征空间 $$\mathbf{z}^l \cup \mathbf{z}^u$$，目标是*欺骗*判别器 $$D(.)$$，让它认为所有数据点都来自已标注池；
- 判别器 $$D(.)$$ 基于潜在表示 $$\mathbf{z}$$ 预测一个样本是否已被标注（1）或未标注（0）。VAAL 选择判别器得分低的无标注样本，因为这表明这些样本与先前已标注的样本足够不同。

VAAL 中 VAE 表征学习的损失既包含重建部分（最小化给定样本的 ELBO），也包含对抗部分（让已标注与无标注数据采样自同一概率分布 $$q_\phi$$）：

$$
\begin{aligned}
\mathcal{L}_\text{VAE} &= \lambda_1 \mathcal{L}^\text{rec}_\text{VAE} + \lambda_2 \mathcal{L}^\text{adv}_\text{VAE} \\
\mathcal{L}^\text{rec}_\text{VAE} &= \mathbb{E}[\log p_\theta(\mathbf{x}^l \vert \mathbf{z}^l)] - \beta \text{KL}(q_\phi(\mathbf{z}^l \vert \mathbf{x}^l) \| p(\mathbf{\tilde{z}})) + \mathbb{E}[\log p_\theta(\mathbf{u} \vert \mathbf{z}^u)] - \beta \text{KL}(q_\phi(\mathbf{z}^u \vert \mathbf{u}) \| p(\mathbf{\tilde{z}})) \\
\mathcal{L}^\text{adv}_\text{VAE} &= - \mathbb{E}[\log D(q_\phi (\mathbf{z}^l \vert \mathbf{x}^l))] - \mathbb{E}[\log D(q_\phi(\mathbf{z}^u \vert \mathbf{u}))]
\end{aligned}
$$

其中 $$p(\mathbf{\tilde{z}})$$ 是预定义的先验——单位高斯分布，$$\beta$$ 是拉格朗日参数。

判别器的损失为：

$$
\mathcal{L}_D = -\mathbb{E}[\log D(q_\phi (\mathbf{z}^l \vert \mathbf{x}^l))] - \mathbb{E}[\log (1 - D(q_\phi (\mathbf{z}^u \vert \mathbf{u})))]
$$

![VAAL experiments](https://lilianweng.github.io/posts/2022-02-20-active-learning/VAAL-exp.png)

*图 6：VAAL（变分对抗主动学习）在若干图像分类任务上的实验结果。（图片来源：[Sinha et al. 2019](https://arxiv.org/abs/1904.00370) *

消融研究表明，VAE 与判别器的联合训练至关重要。他们的结果对有偏的初始已标注池、不同的标注预算以及有噪声的标注者（oracle）都表现出鲁棒性。

**MAL**（极小化极大主动学习，Minimax Active Learning；[Ebrahimiet al. 2021](https://arxiv.org/abs/2012.10467)）是 VAAL 的扩展。MAL 框架由一个熵最小化的特征编码网络 $$F$$ 与一个随其之后的熵最大化分类器 $$C$$ 组成。这种极小化极大设置缩小了已标注与无标注数据之间的分布差距。

![MAL](https://lilianweng.github.io/posts/2022-02-20-active-learning/MAL.png)

*图 7：MAL（极小化极大主动学习）框架示意。（图片来源：[Ebrahimiet al. 2021](https://arxiv.org/abs/2012.10467)）*

特征编码器 $$F$$ 将样本编码为一个 $$\ell_2$$ 归一化的 $$d$$ 维潜在向量。假设共有 $$K$$ 个类别，分类器 $$C$$ 由 $$\mathbf{W} \in \mathbb{R}^{d \times K}$$ 参数化。

（1）首先，用一个简单的交叉熵损失在已标注样本上训练 $$F$$ 和 $$C$$，以取得良好的分类结果，

$$
\mathcal{L}_\text{CE} = -\mathbb{E}_{(\mathbf{x}^l, y) \sim \mathcal{X}} \sum_{k=1}^K \mathbb{1}[k=y] \log\Big( \sigma(\frac{1}{T} \frac{\mathbf{W}^\top F\big(\mathbf{x}^l)}{\|F(\mathbf{x}^l)\|}\big) \Big)
$$

（2）在无标注样本上训练时，MAL 依赖一种*极小化极大*博弈设置

$$
\begin{aligned}
\mathcal{L}_\text{Ent} &= -\sum^K_{k=1} p(y=k \vert \mathbf{u}) \log p(y=k\vert \mathbf{u}) \\
\theta^*_F, \theta^*_C &= \min_F\max_C \mathcal{L}_\text{Ent} \\
\theta_F &\gets \theta_F - \alpha_1 \nabla \mathcal{L}_\text{Ent} \\
\theta_C &\gets \theta_C + \alpha_2 \nabla \mathcal{L}_\text{Ent}
\end{aligned}
$$

其中，
- 首先，最小化 $$F$$ 的熵会鼓励预测标签相近的无标注样本拥有相似的特征。
- 以对抗的方式最大化 $$C$$ 的熵，使预测趋向更均匀的类别分布。<span style="color: #888;">（我对此的理解是：由于无标注样本的真实标签未知，我们尚不应优化分类器去最大化其预测标签。）</span>

判别器的训练方式与 VAAL 中相同。

MAL 的采样策略同时考虑多样性与不确定性：
- 多样性：$$D$$ 的得分反映一个样本与先前见过的样本的相似程度。得分越接近 0，越有利于选取不熟悉的数据点。
- 不确定性：使用由 $$C$$ 得到的熵。熵得分越高，表明模型尚无法做出置信的预测。

实验在图像分类与分割任务上将 MAL 与随机、熵、core-set、BALD 及 VAAL 等基线进行了比较，结果看起来相当强劲。

![MAL experiments](https://lilianweng.github.io/posts/2022-02-20-active-learning/MAL-exp.png)

*图 8：MAL 在 ImageNet 上的性能。（表格来源：[Ebrahimiet al. 2021](https://arxiv.org/abs/2012.10467)）*

**CAL**（对比主动学习，Contrastive Active Learning；[Margatina et al. 2021](https://arxiv.org/abs/2109.03764)）旨在选取[对比](https://lilianweng.github.io/posts/2021-05-31-contrastive/)样本。在 CAL 中，若两个标签不同的数据点拥有相似的网络表示 $$\Phi(.)$$，它们就被视为对比样本。给定一对对比样本 $$(\mathbf{x}_i, \mathbf{x}_j)$$，它们应当满足

$$
d(\Phi(\mathbf{x}_i), \Phi(\mathbf{x}_j)) < \epsilon \quad\text{and}\quad \text{KL}(p(y\vert \mathbf{x}_i) \| p(y\vert \mathbf{x}_j)) \rightarrow \infty
$$

给定一个无标注样本 $$\mathbf{x}$$，CAL 执行以下流程：
1. 在已标注样本 $$\{(\mathbf{x}^l_i, y_i\}_{i=1}^M \subset \mathcal{X}$$ 中，选取模型特征空间中最近的 top $$k$$ 个近邻。
2. 计算 $$\mathbf{x}$$ 与 $$\{\mathbf{x}^l\}$$ 中每个样本的模型输出概率之间的 KL 散度。$$\mathbf{x}$$ 的对比得分是这些 KL 散度值的平均：$$s(\mathbf{x}) = \frac{1}{M} \sum_{i=1}^M \text{KL}(p(y \vert \mathbf{x}^l_i \| p(y \vert \mathbf{x}))$$。
3. *对比得分高*的样本被选中用于主动学习。

在多种分类任务上，CAL 的实验结果与熵基线看起来相近。

### 度量代表性

#### 核心集方法

**核心集**（core-set）是计算几何中的一个概念，指一小组能够近似更大点集形状的点。近似程度可由某种几何度量来刻画。在主动学习中，我们期望在核心集上训练的模型与在整个数据点上训练的模型表现相当。

[Sener & Savarese (2018)](https://arxiv.org/abs/1708.00489) 将主动学习视为一个核心集选择问题。假设训练期间总共有 $$N$$ 个样本可用。在主动学习过程中，每个时间步 $$t$$ 都会有一小批数据点获得标注，记为 $$\mathcal{S}^{(t)}$$。学习目标的上界可以写成如下形式，其中*核心集损失*（core-set loss）定义为已标注样本上的平均经验损失与包含无标注样本在内的整个数据集上的损失之差。

$$
\begin{aligned}
\mathbb{E}_{(\mathbf{x}, y) \sim p} [\mathcal{L}(\mathbf{x}, y)]
\leq& \bigg\vert \mathbb{E}_{(\mathbf{x}, y) \sim p} [\mathcal{L}(\mathbf{x}, y)] - \frac{1}{N} \sum_{i=1}^N \mathcal{L}(\mathbf{x}_i, y_i) \bigg\vert & \text{; Generalization error}\\
+& \frac{1}{\vert \mathcal{S}^{(t)} \vert} \sum_{j=1}^{\vert \mathcal{S}^{(t)} \vert} \mathcal{L}(\mathbf{x}^l_j, y_j) & \text{; Training error}\\
+& \bigg\vert \frac{1}{N} \sum_{i=1}^N \mathcal{L}(\mathbf{x}_i, y_i) - \frac{1}{\vert \mathcal{S}^{(t)} \vert} \sum_{j=1}^{\vert \mathcal{S}^{(t)} \vert} \mathcal{L}(\mathbf{x}^l_j, y_j) \bigg\vert & \text{; Core-set error}
\end{aligned}
$$

于是，主动学习问题可以重新定义为：

$$
\min_{\mathcal{S}^{(t+1)} : \vert \mathcal{S}^{(t+1)} \vert \leq b} \bigg\vert \frac{1}{N}\sum_{i=1}^N \mathcal{L}(\mathbf{x}_i, y_i) - \frac{1}{\vert \mathcal{S}^{(t)} \cup \mathcal{S}^{(t+1)} \vert} \sum_{j=1}^{\vert \mathcal{S}^{(t)} \cup \mathcal{S}^{(t+1)} \vert} \mathcal{L}(\mathbf{x}^l_j, y_j) \bigg\vert
$$

它等价于 [$$k$$-中心问题](https://en.wikipedia.org/wiki/Metric_k-center)：选出 $$b$$ 个中心点，使数据点与其最近中心之间的最大距离最小化。该问题是 NP 难的，近似解依赖贪心算法。

![Core-sets experiments](https://lilianweng.github.io/posts/2022-02-20-active-learning/core-sets-exp.png)

*图 9：核心集算法的主动学习结果，与若干常见基线在 CIFAR-10、CIFAR-100、SVHN 上的对比。（图片来源：[Sener & Savarese 2018](https://arxiv.org/abs/1708.00489)）*

当类别数较少时，该方法在图像分类任务上效果很好。当类别数变得很大或数据维度增加（「维度灾难」）时，核心集方法的有效性会下降（[Sinha et al. 2019](https://arxiv.org/abs/1904.00370)）。

由于核心集选择的代价高昂，[Coleman et al. (2020)](https://arxiv.org/abs/1906.11829) 用较弱的模型（例如更小、更弱的架构，未充分训练的模型）做了实验，发现经验上以弱模型作为代理可以显著缩短「训练模型 + 挑选样本」这一反复迭代的数据选择周期，而几乎不损害最终误差。他们的方法被称为 **SVP**（Selection via Proxy，基于代理的选择）。

#### 多样梯度嵌入

**BADGE**（Batch Active learning by Diverse Gradient Embeddings，基于多样梯度嵌入的批量主动学习；[Ash et al. 2020](https://arxiv.org/abs/1906.03671)）在梯度空间中同时追踪模型不确定性与数据多样性。不确定性通过网络最后一层相关梯度的大小来度量，多样性则由在梯度空间中铺展开的一组多样样本刻画。
- 不确定性。给定一个无标注样本 $$\mathbf{x}$$，BADGE 首先计算预测 $$\hat{y}$$ 以及损失在 $$(\mathbf{x}, \hat{y})$$ 上相对于最后一层参数的梯度 $$g_\mathbf{x}$$。他们观察到，$$g_\mathbf{x}$$ 的范数保守地估计了该样本对模型学习的影响，而高置信度样本往往有幅值较小的梯度嵌入。
- 多样性。给定许多样本的大量梯度嵌入 $$g_\mathbf{x}$$，BADGE 运行 [$$k$$-means++](https://en.wikipedia.org/wiki/K-means%2B%2B) 来相应地采样数据点。

![BADGE algorithm](https://lilianweng.github.io/posts/2022-02-20-active-learning/BADGE-algo.png)

*图 10：BADGE（基于多样梯度嵌入的批量主动学习）算法。（图片来源：[Ash et al. 2020](https://arxiv.org/abs/1906.03671)）*

### 度量训练效应

#### 量化模型变化

[Settles et al. (2008)](https://papers.nips.cc/paper/2007/hash/a1519de5b5d44b31a01de013b9b51a80-Abstract.html) 提出了一种主动学习查询策略，称为 **EGL**（Expected Gradient Length，期望梯度长度）。其动机是找到那些一旦标签已知、就能触发模型最大更新的样本。

设 $$\nabla \mathcal{L}(\theta)$$ 为损失函数关于模型参数的梯度。具体来说，给定一个无标注样本 $$\mathbf{x}_i$$，我们需要在假设标签为 $$y \in \mathcal{Y}$$ 的情况下计算梯度 $$\nabla \mathcal{L}^{(y)}(\theta)$$。由于真实标签 $$y_i$$ 未知，EGL 依靠当前模型的信念来计算期望的梯度变化：

$$
\text{EGL}(\mathbf{x}_i) = \sum_{y_i \in \mathcal{Y}} p(y=y_i \vert \mathbf{x}) \|\nabla \mathcal{L}^{(y_i)}(\theta)\|
$$

**BALD**（Bayesian Active Learning by Disagreement，基于分歧的贝叶斯主动学习；[Houlsby et al. 2011](https://arxiv.org/abs/1112.5745)）旨在识别能最大化关于模型权重的信息增益的样本，这等价于最大化期望后验熵的下降量。

$$
\begin{aligned}
I[\boldsymbol{\theta}, y \vert x,\mathcal{D}] 
&= H(\boldsymbol{\theta} \vert \mathcal{D}) - \mathbb{E}_{y \sim p(y \vert \boldsymbol{x}, \mathcal{D})} \big[ H(\boldsymbol{\theta} \vert y, \boldsymbol{x}, \mathcal{D}) \big] & \text{; Decrease in expected posterior entropy}\\ 
&= H(y \vert \boldsymbol{x}, \mathcal{D}) - \mathbb{E}_{\boldsymbol{\theta} \sim p(\boldsymbol{\theta} \vert \mathcal{D})} \big[ H(y \vert \boldsymbol{x}, \mathcal{\theta}) \big]
\end{aligned}
$$

其内在解读是「寻找这样的 $$\mathbf{x}$$：模型对 $$y$$ 整体上最不确定（$$H(y \vert \mathbf{x}, \mathcal{D})$$ 高），但参数的每种单独取值都很自信（$$H(y \vert \mathbf{x}, \boldsymbol{\theta})$$ 低）」。换言之，每一次单独的后验采样都很自信，但一组采样会携带多样化的意见。

BALD 最初是针对单个样本提出的，[Kirsch et al. (2019)](https://arxiv.org/abs/1906.08158) 将其扩展到了批量模式。

#### 遗忘事件

为了研究神经网络是否有**遗忘**先前所学信息的倾向，[Mariya Toneva et al. (2019)](https://arxiv.org/abs/1812.05159) 设计了一个实验：他们在训练过程中跟踪模型对每个样本的预测，并统计每个样本从被正确分类到被错误分类（或相反）的转换次数。据此，样本可以被归为以下几类：
- *可遗忘*（冗余）样本：类别标签在训练各轮之间发生变化的样本。
- *不可遗忘*样本：类别标签的分配在训练各轮之间保持一致的样本。这些样本一旦学会就再也不会被遗忘。

他们发现，存在大量一旦学会便永不再被遗忘的不可遗忘样本。带噪声标签的样本，以及具有「不常见」特征（视觉上难以分类）的图像，属于最容易被遗忘的样本。实验从经验上验证了：不可遗忘样本可以安全移除而不损害模型性能。

在实现中，只有当样本出现在当前训练批次中时才统计遗忘事件；也就是说，他们是在同一样本于后续 mini-batch 中重复出现时计算遗忘的。每个样本的遗忘事件次数在不同随机种子间相当稳定，且可遗忘样本略微倾向于在训练后期才被首次学会。遗忘事件还被发现可以在整个训练期间以及不同架构之间迁移。

如果我们假设「模型在训练期间改变预测」是模型不确定性的一个标志，遗忘事件就可以用作主动学习采集的信号。然而，无标注样本的真实标签是未知的。[Bengar et al. (2021)](https://arxiv.org/abs/2107.14707) 为此提出了一个新指标，称为**标签分散度**（label dispersion）。设在整个训练时间里，$$c^*$$ 是输入 $$\mathbf{x}$$ 最常被预测的标签，标签分散度度量的是模型未将 $$c^**$$ 分配给该样本的训练步占比：

$$
\text{Dispersion}(\mathbf{x}) = 1 - \frac{f_\mathbf{x}}{T} \text{ where }
f_\mathbf{x} = \sum_{t=1}^T \mathbb{1}[\hat{y}_t = c^*], c^* = \arg\max_{c=1,\dots,C}\sum_{t=1}^T \mathbb{1}[\hat{y}_t = c]
$$

在他们的实现中，分散度按每个 epoch 计算。若模型始终为同一样本分配相同的标签，标签分散度就低；若预测经常变化，分散度就高。如图 11 所示，标签分散度与网络不确定性相关。

![Label dispersion](https://lilianweng.github.io/posts/2022-02-20-active-learning/label-dispersion-vs-uncertainty.png)

*图 11：标签分散度与网络不确定性相关。x 轴上数据点按标签分散度得分排序；y 轴是模型为这些样本推断标签时的预测准确率。（图片来源：[Bengar et al. 2021](https://arxiv.org/abs/2107.14707)）*

### 混合方法

以批量模式运行主动学习时，控制批次内部的多样性很重要。**Suggestive Annotation**（**SA**；[Yang et al. 2017](https://arxiv.org/abs/1706.04737)）是一种两步混合策略，旨在同时选出高不确定性与高代表性的已标注样本。它利用在已标注数据上训练的模型集成所得到的不确定性，并利用核心集来挑选有代表性的数据样本。
1. 首先，SA 选出不确定性得分最高的前 $$K$$ 张图像，构成候选池 $$\mathcal{S}_c \subseteq \mathcal{S}_U$$。这里的不确定性以多个用自助法训练的模型之间的分歧来度量。
2. 下一步是找出代表性最高的子集 $$\mathcal{S}_a \subseteq \mathcal{S}_c$$。两个输入特征向量之间的余弦相似度近似刻画了它们的相似程度。$$\mathcal{S}_a$$ 对 $$\mathcal{S}_U$$ 的代表性反映 $$\mathcal{S}_a$$ 能多好地代表 $$\mathcal{S}_u$$ 中的全部样本，定义为：

 $$
F(\mathcal{S}_a, \mathcal{S}_u) = \sum_{\mathbf{x}_j \in \mathcal{S}_u} f(\mathcal{S}_a, \mathbf{x}_j) = \sum_{\mathbf{x}_j \in \mathcal{S}_u} \max_{\mathbf{x}_i \in \mathcal{S}_a} \text{sim}(\mathbf{x}_i, \mathbf{x}_j)
$$

构造含 $$k$$ 个数据点且最大化 $$F(\mathcal{S}_a, \mathcal{S}_u)$$ 的 $$\mathcal{S}_a \subseteq \mathcal{S}_c$$，是最大集合覆盖问题的一个推广版本。它是 NP 难的，其最优的多项式时间近似算法是一个简单的贪心方法。
1. 初始时，$$\mathcal{S}_a = \emptyset$$ 且 $$F(\mathcal{S}_a, \mathcal{S}_u) = 0$$。
2. 然后，迭代地将使 $$F(\mathcal{S}_a \cup I_i, \mathcal{S}_u)$$ 最大的 $$\mathbf{x}_i \in \mathcal{S}_c$$ 加入 $$\mathcal{S}_a$$，直至 $$\mathcal{S}_s$$ 包含 $$k$$ 张图像。

[Zhdanov (2019)](https://arxiv.org/abs/1901.05954) 执行与 SA 类似的过程，但在第 2 步中用 $$k$$-means 取代了核心集，且候选池的大小是相对批次大小来配置的。给定批次大小 $$b$$ 与常数 $$beta$$（介于 10 到 50 之间），其步骤如下：
1. 在已标注数据上训练一个分类器；
2. 度量每个无标注样本的信息量（例如使用不确定性指标）；
3. 预筛选出信息量最大的前 $$\beta b \geq b$$ 个样本；
4. 将这 $$\beta b$$ 个样本聚成 $$B$$ 个簇；
5. 选取离簇中心最近的 $$b$$ 个不同样本，用于本轮主动学习。

主动学习还可以进一步与[半监督学习](https://lilianweng.github.io/posts/2021-12-05-semi-supervised/)结合以节省预算。**CEAL**（Cost-Effective Active Learning，低成本主动学习；[Yang et al. 2017](https://arxiv.org/abs/1701.03551)）并行地做两件事：
1. 通过主动学习选出不确定的样本并送去做标注；
2. 选出预测最置信的样本并为它们分配[伪标签](https://lilianweng.github.io/posts/2021-12-05-semi-supervised/#pseudo-labeling)。预测是否置信由预测熵是否低于阈值 $$\delta$$ 来判断。随着模型随时间不断变好，阈值 $$\delta$$ 也会随时间衰减。

![CEAL](https://lilianweng.github.io/posts/2022-02-20-active-learning/CEAL.png)

*图 12：CEAL（低成本主动学习）示意。（图片来源：[Yang et al. 2017][(https://arxiv.org/abs/1701.03551))*

---
引用格式：
```
@article{weng2022active,
  title   = "Learning with not Enough Data Part 1: Semi-Supervised Learning",
  author  = "Weng, Lilian",
  journal = "lilianweng.github.io/lil-log",
  year    = "2022",
  url     = "https://lilianweng.github.io/lil-log/2022/02/20/active-learning.html"
}
```

## 参考文献

[1] Burr Settles. [Active learning literature survey.](https://burrsettles.com/pub/settles.activelearning.pdf) University of Wisconsin, Madison, 52(55-66):11, 2010.

[2] [https://jacobgil.github.io/deeplearning/activelearning](https://jacobgil.github.io/deeplearning/activelearning)

[3] Yang et al. ["Cost-effective active learning for deep image classification"](https://arxiv.org/abs/1701.03551) TCSVT 2016.

[4] Yarin Gal et al. ["Dropout as a Bayesian Approximation: representing model uncertainty in deep learning."](https://arxiv.org/abs/1506.02142) ICML 2016.

[5] Blundell et al. ["Weight uncertainty in neural networks (Bayes-by-Backprop)"](https://arxiv.org/abs/1505.05424) ICML 2015.

[6] Settles et al. ["Multiple-Instance Active Learning."](https://papers.nips.cc/paper/2007/hash/a1519de5b5d44b31a01de013b9b51a80-Abstract.html) NIPS 2007.

[7] Houlsby et al. [Bayesian Active Learning for Classification and Preference Learning."](https://arxiv.org/abs/1112.5745) arXiv preprint arXiv:1112.5745 (2020).

[8] Kirsch et al. ["BatchBALD: Efficient and Diverse Batch Acquisition for Deep Bayesian Active Learning."](https://arxiv.org/abs/1906.08158) NeurIPS 2019.

[9] Beluch et al. ["The power of ensembles for active learning in image classification."](https://openaccess.thecvf.com/content_cvpr_2018/papers/Beluch_The_Power_of_CVPR_2018_paper.pdf) CVPR 2018.

[10] Sener & Savarese. ["Active learning for convolutional neural networks: A core-set approach."](https://arxiv.org/abs/1708.00489) ICLR 2018. 

[11] Donggeun Yoo & In So Kweon. ["Learning Loss for Active Learning."](https://arxiv.org/abs/1905.03677) CVPR 2019. 

[12] Margatina et al. ["Active Learning by Acquiring Contrastive Examples."](https://arxiv.org/abs/2109.03764) EMNLP 2021.

[13] Sinha et al. ["Variational Adversarial Active Learning"](https://arxiv.org/abs/1904.00370) ICCV 2019 

[14] Ebrahimiet al. ["Minmax Active Learning"](https://arxiv.org/abs/2012.10467) arXiv preprint arXiv:2012.10467 (2021).

[15] Mariya Toneva et al. ["An empirical study of example forgetting during deep neural network learning."](https://arxiv.org/abs/1812.05159) ICLR 2019.

[16] Javad Zolfaghari Bengar et al. ["When Deep Learners Change Their Mind: Learning Dynamics for Active Learning."](https://arxiv.org/abs/2107.14707) CAIP 2021.

[17] Yang et al. ["Suggestive annotation: A deep active learning framework for biomedical image segmentation."](https://arxiv.org/abs/1706.04737) MICCAI 2017.

[18] Fedor Zhdanov. ["Diverse mini-batch Active Learning"](https://arxiv.org/abs/1901.05954) arXiv preprint arXiv:1901.05954 (2019).
