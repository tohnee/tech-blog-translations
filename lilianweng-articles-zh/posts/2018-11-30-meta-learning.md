---
title: "元学习：学会快速学习"
title_en: "Meta-Learning: Learning to Learn Fast"
source: https://lilianweng.github.io/posts/2018-11-30-meta-learning/
crawled: 2026-09-08
translated: 2026-09-08
---

# 元学习：学会快速学习

> 原文：[Meta-Learning: Learning to Learn Fast](https://lilianweng.github.io/posts/2018-11-30-meta-learning/) · Lilian Weng（翁荔）

> 元学习（meta-learning）也称"学习如何学习（learning to learn）"，旨在设计能用少量训练样本快速学习新技能或适应新环境的模型。常见方法有三类：1) 学习高效的距离度量（基于度量）；2) 使用带外部或内部记忆的（循环）网络（基于模型）；3) 显式地为快速学习优化模型参数（基于优化）。

<span style="color: #286ee0;">[更新于 2019-10-01：感谢 Tianhao，本文有了[中文译本](https://wei-tianhao.github.io/blog/2019/09/17/meta-learning.html)！]</span>

一个好的机器学习模型往往需要大量样本的训练。相比之下，人类学习新概念和新技能要快得多、高效得多。只看过几次猫和鸟的孩子能很快把它们区分开。会骑自行车的人很可能在很少甚至没有演示的情况下快速学会骑摩托车。有没有可能设计一个具有类似性质的机器学习模型——只用少量训练样本就能快速学习新概念和新技能？这正是**元学习**要解决的问题。

我们期望一个好的元学习模型能够良好地适应或泛化到训练期间从未遇到过的新任务和新环境。适应过程本质上是一次小型的学习会话，发生在测试阶段，但对新任务配置的接触有限。最终，适应后的模型能完成新任务。这就是元学习也被称为 [learning to learn](https://www.cs.cmu.edu/~rsalakhu/papers/LakeEtAl2015Science.pdf) 的原因。

任务可以是任何定义明确的机器学习问题族：监督学习、强化学习等。例如，下面是几个具体的元学习任务：
- 一个在非猫图像上训练的分类器，在看了一小撮猫的图片后能判断给定图像是否包含猫。
- 一个游戏机器人能够快速掌握一款新游戏。
- 一个小型机器人在测试时能完成上坡表面的任务，尽管它只在平地环境中训练过。

## 定义元学习问题

本文聚焦于每个目标任务都是监督学习问题（如图像分类）的情形。关于强化学习问题的元学习（即"元强化学习"）有许多有趣的文献，但不在本文覆盖范围内。

### 一个简单的视角

一个好的元学习模型应该在多种学习任务上训练，并针对任务分布（包括可能未见的任务）上的最佳性能进行优化。每个任务关联一个数据集 $$\mathcal{D}$$，包含特征向量和真实标签。最优模型参数为：

$$
\theta^* = \arg\min_\theta \mathbb{E}_{\mathcal{D}\sim p(\mathcal{D})} [\mathcal{L}_\theta(\mathcal{D})]
$$

它看起来非常像普通的学习任务，只是*一个数据集*被视为*一个数据样本*。

*小样本分类（few-shot classification）*是元学习在监督学习领域的一个实例。数据集 $$\mathcal{D}$$ 常被分成两部分：用于学习的支持集（support set）$$S$$ 和用于训练或测试的预测集 $$B$$，$$\mathcal{D}=\langle S, B\rangle$$。我们常考虑 *K-shot N-class 分类*任务：支持集包含 N 个类别各 K 个带标注的样本。

![few-shot-classification](https://lilianweng.github.io/posts/2018-11-30-meta-learning/few-shot-classification.png)

*图 1：4-shot 2-class 图像分类示例。（图像缩略图来自 [Pinterest](https://www.pinterest.com/)）*

### 训练与测试方式一致

数据集 $$\mathcal{D}$$ 包含特征向量与标签对，$$\mathcal{D} = \{(\mathbf{x}_i, y_i)\}$$，每个标签属于已知的标签集合 $$\mathcal{L}^\text{label}$$。设参数为 $$\theta$$ 的分类器 $$f_\theta$$ 输出给定特征向量 $$\mathbf{x}$$ 时数据点属于类别 $$y$$ 的概率 $$P_\theta(y\vert\mathbf{x})$$。

最优参数应最大化多个训练批次 $$B \subset \mathcal{D}$$ 上真实标签的概率：

$$
\begin{aligned}
\theta^* &= {\arg\max}_{\theta} \mathbb{E}_{(\mathbf{x}, y)\in \mathcal{D}}[P_\theta(y \vert \mathbf{x})] &\\
\theta^* &= {\arg\max}_{\theta} \mathbb{E}_{B\subset \mathcal{D}}[\sum_{(\mathbf{x}, y)\in B}P_\theta(y \vert \mathbf{x})] & \scriptstyle{\text{; trained with mini-batches.}}
\end{aligned}
$$

在小样本分类中，目标是给定一个小支持集后"快速学习"（想想"微调"是怎么工作的），降低未知标签数据样本上的预测误差。为了让训练过程模仿推理时发生的事情，我们想用标签的一个子集来"伪造"数据集，避免把所有标签都暴露给模型，并相应修改优化过程以鼓励快速学习：
1. 采样一个标签子集 $$L\subset\mathcal{L}^\text{label}$$。
2. 采样一个支持集 $$S^L \subset \mathcal{D}$$ 和一个训练批次 $$B^L \subset \mathcal{D}$$。二者都只包含标签属于所采标签集 $$L$$ 的数据点，$$y \in L, \forall (x, y) \in S^L, B^L$$。
3. 支持集是模型输入的一部分。<!-- , $$\hat{y}=f_\theta(\mathbf{x}, S^L)$$ -->
4. 最终优化用 mini-batch $$B^L$$ 计算损失并通过反向传播更新模型参数，与监督学习中的用法相同。

你可以把每对采样出的数据集 $$(S^L, B^L)$$ 视为一个数据点。模型的训练使其能泛化到其他数据集。红色符号是为元学习在监督学习目标之外新增的部分。

$$
\theta = \arg\max_\theta \color{red}{E_{L\subset\mathcal{L}}[} E_{\color{red}{S^L \subset\mathcal{D}, }B^L \subset\mathcal{D}} [\sum_{(x, y)\in B^L} P_\theta(x, y\color{red}{, S^L})] \color{red}{]}
$$

这个想法在某种程度上类似于当只有有限的任务专属数据样本时，在图像分类（ImageNet）或语言建模（大型文本语料）中使用预训练模型。元学习把这一想法又推进了一步：不是按单一下游任务微调，而是优化模型使其擅长很多（如果不是全部）任务。

### 学习器与元学习器

元学习的另一个流行视角把模型更新分解为两个阶段：
- 分类器 $$f_\theta$$ 是"学习器（learner）"模型，为完成给定任务而训练；
- 与此同时，优化器 $$g_\phi$$ 学习如何通过支持集 $$S$$ 更新学习器模型的参数，$$\theta' = g_\phi(\theta, S)$$。

于是在最终优化步骤中，我们需要同时更新 $$\theta$$ 和 $$\phi$$ 以最大化：

$$
\mathbb{E}_{L\subset\mathcal{L}}[ \mathbb{E}_{S^L \subset\mathcal{D}, B^L \subset\mathcal{D}} [\sum_{(\mathbf{x}, y)\in B^L} P_{g_\phi(\theta, S^L)}(y \vert \mathbf{x})]]
$$

### 常见方法

元学习有三种常见方法：基于度量、基于模型和基于优化。Oriol Vinyals 在 NIPS 2018 元学习研讨会上的[演讲](http://metalearning-symposium.ml/files/vinyals.pdf)中有一个漂亮的总结：

| ------------- | ------------- | ------------- | ------------- |
|  | 基于模型 | 基于度量 | 基于优化 |
| ------------- | ------------- | ------------- | ------------- |
| **核心思想** | RNN；记忆 | 度量学习 | 梯度下降 |
| **$$P_\theta(y \vert \mathbf{x})$$ 如何建模？** | $$f_\theta(\mathbf{x}, S)$$ | $$\sum_{(\mathbf{x}_i, y_i) \in S} k_\theta(\mathbf{x}, \mathbf{x}_i)y_i$$ (*) | $$P_{g_\phi(\theta, S^L)}(y \vert \mathbf{x})$$ |

(*) $$k_\theta$$ 是度量 $$\mathbf{x}_i$$ 与 $$\mathbf{x}$$ 相似度的核函数。

接下来我们逐类回顾经典模型。

## 基于度量

基于度量的元学习核心思想与最近邻算法（如 [k-NN](https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm) 分类器和 [k-means](https://en.wikipedia.org/wiki/K-means_clustering) 聚类）以及[核密度估计](https://en.wikipedia.org/wiki/Kernel_density_estimation)类似。在一组已知标签 $$y$$ 上的预测概率是支持集样本标签的加权和。权重由核函数 $$k_\theta$$ 生成，度量两个数据样本的相似度。

$$
P_\theta(y \vert \mathbf{x}, S) = \sum_{(\mathbf{x}_i, y_i) \in S} k_\theta(\mathbf{x}, \mathbf{x}_i)y_i 
$$ 

学习一个好的核对基于度量的元学习模型的成败至关重要。[度量学习](https://en.wikipedia.org/wiki/Similarity_learning#Metric_learning)与这一意图高度契合，因为它旨在学习对象上的度量或距离函数。"好度量"的概念取决于具体问题，它应能表示输入在任务空间中的关系并有助于解决问题。

下面介绍的所有模型都显式学习输入数据的嵌入向量，并用它们设计合适的核函数。

### 卷积孪生神经网络

[孪生神经网络（Siamese Neural Network）](https://papers.nips.cc/paper/769-signature-verification-using-a-siamese-time-delay-neural-network.pdf)由两个孪生网络组成，它们的输出在顶部被联合训练以学习成对输入数据样本之间的关系。孪生网络完全相同，共享相同的权重和网络参数。换言之，二者都指同一个嵌入网络，学习能揭示数据点对之间关系的高效嵌入。

[Koch, Zemel & Salakhutdinov (2015)](http://www.cs.toronto.edu/~rsalakhu/papers/oneshot1.pdf) 提出用孪生神经网络做单样本（one-shot）图像分类。首先，孪生网络针对"判断两张输入图像是否属于同一类"的验证任务训练，输出两张图像属于同一类的概率。然后，测试时，孪生网络处理测试图像与支持集中每张图像组成的所有图像对。最终预测是概率最高的支持图像的类别。

![siamese](https://lilianweng.github.io/posts/2018-11-30-meta-learning/siamese-conv-net.png)

*图 2：用于小样本图像分类的卷积孪生神经网络架构。*

1. 首先，卷积孪生网络学习通过含若干卷积层的嵌入函数 $$f_\theta$$ 把两张图像编码为特征向量。
2. 两个嵌入之间的 L1 距离为 $$\vert f_\theta(\mathbf{x}_i) - f_\theta(\mathbf{x}_j) \vert$$。
3. 距离经一个线性前馈层和 sigmoid 转换为概率 $$p$$，即两张图像来自同一类的概率。
4. 直观上，损失是交叉熵，因为标签是二值的。

<!-- In this way, an efficient image embedding is trained so that the distance between two embeddings is proportional to the similarity between two images. -->

$$
\begin{aligned}
p(\mathbf{x}_i, \mathbf{x}_j) &= \sigma(\mathbf{W}\vert f_\theta(\mathbf{x}_i) - f_\theta(\mathbf{x}_j) \vert) \\
\mathcal{L}(B) &= \sum_{(\mathbf{x}_i, \mathbf{x}_j, y_i, y_j)\in B} \mathbf{1}_{y_i=y_j}\log p(\mathbf{x}_i, \mathbf{x}_j) + (1-\mathbf{1}_{y_i=y_j})\log (1-p(\mathbf{x}_i, \mathbf{x}_j))
\end{aligned}
$$

训练批次 $$B$$ 中的图像可以用形变做数据增强。当然，你可以把 L1 距离换成其他距离度量，L2、余弦等。只要保证它们可微，其余一切照旧。

给定支持集 $$S$$ 和测试图像 $$\mathbf{x}$$，最终预测类别为：

$$
\hat{c}_S(\mathbf{x}) = c(\arg\max_{\mathbf{x}_i \in S} P(\mathbf{x}, \mathbf{x}_i))
$$

其中 $$c(\mathbf{x})$$ 是图像 $$\mathbf{x}$$ 的类别标签，$$\hat{c}(.)$$ 是预测标签。

这里的假设是学到的嵌入能泛化，对度量未知类别图像之间的距离依然有用。这与通过采用预训练模型做迁移学习背后的假设相同；例如，期望在 ImageNet 上预训练的模型学到的卷积特征有助于其他图像任务。然而，当新任务偏离模型训练的原始任务时，预训练模型的好处会下降。

### 匹配网络

**匹配网络（Matching Networks）**（[Vinyals et al., 2016](http://papers.nips.cc/paper/6385-matching-networks-for-one-shot-learning.pdf)）的任务是为任意给定（小）支持集 $$S=\{x_i, y_i\}_{i=1}^k$$ 学习一个分类器 $$c_S$$（*k-shot* 分类）。该分类器定义给定测试样本 $$\mathbf{x}$$ 时输出标签 $$y$$ 上的概率分布。与其他基于度量的模型类似，分类器输出定义为支持样本标签以注意力核 $$a(\mathbf{x}, \mathbf{x}_i)$$ 加权的和——注意力核应与 $$\mathbf{x}$$ 和 $$\mathbf{x}_i$$ 的相似度成正比。

![siamese](https://lilianweng.github.io/posts/2018-11-30-meta-learning/matching-networks.png)

*图 3：匹配网络的架构。（图片来源：[原论文](http://papers.nips.cc/paper/6385-matching-networks-for-one-shot-learning.pdf)）*

$$
c_S(\mathbf{x}) = P(y \vert \mathbf{x}, S) = \sum_{i=1}^k a(\mathbf{x}, \mathbf{x}_i) y_i
\text{, where }S=\{(\mathbf{x}_i, y_i)\}_{i=1}^k
$$

注意力核依赖两个嵌入函数 $$f$$ 和 $$g$$，分别用于编码测试样本和支持集样本。两个数据点之间的注意力权重是其嵌入向量之间的余弦相似度 $$\text{cosine}(.)$$，经 softmax 归一化：

$$
a(\mathbf{x}, \mathbf{x}_i) = \frac{\exp(\text{cosine}(f(\mathbf{x}), g(\mathbf{x}_i))}{\sum_{j=1}^k\exp(\text{cosine}(f(\mathbf{x}), g(\mathbf{x}_j))}
$$

#### 简单嵌入

在简单版本中，嵌入函数是以单个数据样本为输入的神经网络。我们可以设 $$f=g$$。

#### 全上下文嵌入

嵌入向量是构建好分类器的关键输入。仅以单个数据点为输入可能不足以高效地丈量整个特征空间。因此，匹配网络模型进一步提出增强嵌入函数：除原始输入外，还以整个支持集 $$S$$ 为输入，使学到的嵌入能基于与其他支持样本的关系得到调整。

- $$g_\theta(\mathbf{x}_i, S)$$ 用双向 LSTM 在整个支持集 $$S$$ 的上下文中编码 $$\mathbf{x}_i$$。
- $$f_\theta(\mathbf{x}, S)$$ 通过一个对支持集 $$S$$ 带读取注意力的 LSTM 编码测试样本 $$\mathbf{x}$$。
    1. 首先测试样本经过一个简单的神经网络（如 CNN）提取基本特征 $$f'(\mathbf{x})$$。
    2. 然后训练一个 LSTM，其隐藏状态的一部分是对支持集的读取注意力向量：<br/>
    $$
    \begin{aligned}
    \hat{\mathbf{h}}_t, \mathbf{c}_t &= \text{LSTM}(f'(\mathbf{x}), [\mathbf{h}_{t-1}, \mathbf{r}_{t-1}], \mathbf{c}_{t-1}) \\
    \mathbf{h}_t &= \hat{\mathbf{h}}_t + f'(\mathbf{x}) \\
    \mathbf{r}_{t-1} &= \sum_{i=1}^k a(\mathbf{h}_{t-1}, g(\mathbf{x}_i)) g(\mathbf{x}_i) \\
    a(\mathbf{h}_{t-1}, g(\mathbf{x}_i)) &= \text{softmax}(\mathbf{h}_{t-1}^\top g(\mathbf{x}_i)) = \frac{\exp(\mathbf{h}_{t-1}^\top g(\mathbf{x}_i))}{\sum_{j=1}^k \exp(\mathbf{h}_{t-1}^\top g(\mathbf{x}_j))}
    \end{aligned}
    $$
    3. 若做 K 步"读取"，最终 $$f(\mathbf{x}, S)=\mathbf{h}_K$$。

这种嵌入方法称为"全上下文嵌入（Full Contextual Embeddings，FCE）"。有趣的是，它确实能提升困难任务（mini ImageNet 上的小样本分类）上的性能，但在简单任务（Omniglot）上没有差别。

匹配网络的训练过程设计为与测试时的推理相匹配，细节见前文[小节](#training-in-the-same-way-as-testing)。值得一提的是，匹配网络论文精炼了"训练与测试条件应当匹配"这一思想。

$$
\theta^* = \arg\max_\theta \mathbb{E}_{L\subset\mathcal{L}}[ \mathbb{E}_{S^L \subset\mathcal{D}, B^L \subset\mathcal{D}} [\sum_{(\mathbf{x}, y)\in B^L} P_\theta(y\vert\mathbf{x}, S^L)]]
$$

### 关系网络

**关系网络（Relation Network，RN）**（[Sung et al., 2018](http://openaccess.thecvf.com/content_cvpr_2018/papers_backup/Sung_Learning_to_Compare_CVPR_2018_paper.pdf)）与[孪生网络](#convolutional-siamese-neural-network)类似，但有几点不同：
1. 关系不再由特征空间中的简单 L1 距离捕捉，而是由 CNN 分类器 $$g_\phi$$ 预测。一对输入 $$\mathbf{x}_i$$ 和 $$\mathbf{x}_j$$ 的关系分数为 $$r_{ij} = g_\phi([\mathbf{x}_i, \mathbf{x}_j])$$，其中 $$[.,.]$$ 是拼接。
2. 目标函数是 MSE 损失而非交叉熵，因为概念上 RN 更侧重预测关系分数——这更像回归而非二分类，$$\mathcal{L}(B) = \sum_{(\mathbf{x}_i, \mathbf{x}_j, y_i, y_j)\in B} (r_{ij} - \mathbf{1}_{y_i=y_j})^2$$。

![relation-network](https://lilianweng.github.io/posts/2018-11-30-meta-learning/relation-network.png)

*图 4：带一个查询样本的 5-way 1-shot 问题的关系网络架构。（图片来源：[原论文](http://openaccess.thecvf.com/content_cvpr_2018/papers_backup/Sung_Learning_to_Compare_CVPR_2018_paper.pdf)）*

（注意：DeepMind 还提出过另一个用于关系推理的[关系网络](https://deepmind.com/blog/neural-approach-relational-reasoning/)，不要混淆。）

### 原型网络

**原型网络（Prototypical Networks）**（[Snell, Swersky & Zemel, 2017](http://papers.nips.cc/paper/6996-prototypical-networks-for-few-shot-learning.pdf)）用嵌入函数 $$f_\theta$$ 把每个输入编码为 $$M$$ 维特征向量。每个类别 $$c \in \mathcal{C}$$ 定义一个*原型*特征向量，为该类嵌入支持样本的均值向量。

$$
\mathbf{v}_c = \frac{1}{|S_c|} \sum_{(\mathbf{x}_i, y_i) \in S_c} f_\theta(\mathbf{x}_i)
$$

![prototypical-networks](https://lilianweng.github.io/posts/2018-11-30-meta-learning/prototypical-networks.png)

*图 5：小样本与零样本场景下的原型网络。（图片来源：[原论文](http://papers.nips.cc/paper/6996-prototypical-networks-for-few-shot-learning.pdf)）*

给定测试输入 $$\mathbf{x}$$，类别上的分布是测试数据嵌入与原型向量之间距离的负值上的 softmax。

$$
P(y=c\vert\mathbf{x})=\text{softmax}(-d_\varphi(f_\theta(\mathbf{x}), \mathbf{v}_c)) = \frac{\exp(-d_\varphi(f_\theta(\mathbf{x}), \mathbf{v}_c))}{\sum_{c' \in \mathcal{C}}\exp(-d_\varphi(f_\theta(\mathbf{x}), \mathbf{v}_{c'}))}
$$

其中 $$d_\varphi$$ 可以是任何距离函数，只要 $$\varphi$$ 可微。论文中用的是欧氏距离平方。

损失函数为负对数似然：$$\mathcal{L}(\theta) = -\log P_\theta(y=c\vert\mathbf{x})$$。

## 基于模型

基于模型的元学习模型不对 $$P_\theta(y\vert\mathbf{x})$$ 的形式做任何假设。它依赖一个专为快速学习设计的模型——一个只需少量训练步骤就能迅速更新参数的模型。这种快速参数更新可以由其内部架构实现，或由另一个元学习器模型控制。

### 记忆增强神经网络

一族模型架构使用外部存储器来促进神经网络的学习过程，包括[神经图灵机](https://lilianweng.github.io/posts/2018-06-24-attention/#neural-turing-machines)和[记忆网络](https://arxiv.org/abs/1410.3916)。有了显式的存储缓冲，网络更容易快速吸收新信息且未来不遗忘。这样的模型称为 **MANN**，即 "**Memory-Augmented Neural Network**"（记忆增强神经网络）的缩写。注意，只有*内部记忆*的循环网络（如朴素 RNN 或 LSTM）不是 MANN。

由于 MANN 被期望能快速编码新信息、从而在只见过少量样本后适应新任务，它非常契合元学习。以神经图灵机（NTM）为基础模型，[Santoro et al. (2016)](http://proceedings.mlr.press/v48/santoro16.pdf) 对训练设定和记忆检索机制（或"寻址机制"，决定如何给记忆向量分配注意力权重）提出了一组修改。如果不熟悉这一主题，请先阅读我另一篇文章中的 [NTM 小节](https://lilianweng.github.io/posts/2018-06-24-attention/#neural-turing-machines)。

快速回顾：NTM 把控制器神经网络与外部存储器耦合。控制器学会通过软注意力读写记忆行，而记忆充当知识仓库。注意力权重由其寻址机制生成：基于内容 + 基于位置。

![NTM](https://lilianweng.github.io/posts/2018-11-30-meta-learning/NTM.png)

*图 6：神经图灵机（NTM）架构。时间 t 的记忆 $$\mathbf{M}_t$$ 是大小 $$N \times M$$ 的矩阵，包含 N 个向量行，每行 M 维。*

#### 用于元学习的 MANN

要把 MANN 用于元学习任务，我们需要以这样的方式训练它：记忆能快速编码并捕获新任务的信息，同时任何存储的表示都容易且稳定地被访问。

[Santoro et al., 2016](http://proceedings.mlr.press/v48/santoro16.pdf) 描述的训练以一种有趣的方式进行：强制记忆把信息保持得更久，直到稍后适当的标签被给出。在每个训练回合中，真实标签 $$y_t$$ 以**一步偏移**呈现，$$(\mathbf{x}_{t+1}, y_t)$$：它是上一时间步 t 输入的真实标签，却作为时间步 t+1 的输入的一部分呈现。

![NTM](https://lilianweng.github.io/posts/2018-11-30-meta-learning/mann-meta-learning.png)

*图 7：MANN 用于元学习的任务设定（图片来源：[原论文](http://proceedings.mlr.press/v48/santoro16.pdf)）。*

这样，MANN 就有动机去记住新数据集的信息，因为记忆必须保持当前输入直到稍后标签出现，然后检索旧信息据此做出预测。

接下来看记忆如何为高效的信息检索与存储而更新。

#### 用于元学习的寻址机制

除训练过程外，还使用了一种新的纯基于内容的寻址机制，使模型更适合元学习。

**>> 如何从记忆读取？**
<br/>
读注意力纯粹基于内容相似度构建。

首先，控制器在时间步 t 产生一个键特征向量 $$\mathbf{k}_t$$，它是输入 $$\mathbf{x}$$ 的函数。与 NTM 类似，N 个元素的读权重向量 $$\mathbf{w}_t^r$$ 计算为键向量与每个记忆向量行之间的余弦相似度，经 softmax 归一化。读向量 $$\mathbf{r}_t$$ 是以此权重加权的记忆记录之和：

$$
\mathbf{r}_i = \sum_{i=1}^N w_t^r(i)\mathbf{M}_t(i)
\text{, where } w_t^r(i) = \text{softmax}(\frac{\mathbf{k}_t \cdot \mathbf{M}_t(i)}{\|\mathbf{k}_t\| \cdot \|\mathbf{M}_t(i)\|})
$$

其中 $$M_t$$ 是时间 t 的记忆矩阵，$$M_t(i)$$ 是该矩阵的第 i 行。

**>> 如何写入记忆？**
<br/>
把新接收的信息写入记忆的寻址机制运行起来很像[缓存替换](https://en.wikipedia.org/wiki/Cache_replacement_policies)策略。**最近最少使用访问（Least Recently Used Access，LRUA）**写入器是为让 MANN 更好地在元学习场景中工作而设计的。LRUA 写头偏好把新内容写入*最少使用*的记忆位置或*最近使用*的记忆位置。
* 很少使用的位置：这样我们能保留频繁使用的信息（见 [LFU](https://en.wikipedia.org/wiki/Least_frequently_used)）；
* 最后使用的位置：动机是一旦一条信息被检索过一次，它可能一段时间内不会再被调用（见 [MRU](https://en.wikipedia.org/wiki/Cache_replacement_policies#Most_recently_used_(MRU))）。

缓存替换算法有很多，每一种在不同用例下都可能以更好的性能替代这里的设计。此外，学习记忆使用模式和寻址策略（而非任意设定）会是个好主意。

LRUA 的偏好以一切皆可微的方式实现：
1. 时间 t 的使用权重 $$\mathbf{w}^u_t$$ 是当前读、写向量之和，再加上衰减的上一次使用权重 $$\gamma \mathbf{w}^u_{t-1}$$，其中 $$\gamma$$ 是衰减因子。
2. 写向量是上一次读权重（偏好"最后使用的位置"）与上一次最少使用权重（偏好"很少使用的位置"）的插值。插值参数是超参数 $$\alpha$$ 的 sigmoid。
3. 最少使用权重 $$\mathbf{w}^{lu}$$ 按使用权重 $$\mathbf{w}_t^u$$ 缩放，其中小于向量第 n 小元素的维度保持 1，否则为 0。

$$
\begin{aligned}
\mathbf{w}_t^u &= \gamma \mathbf{w}_{t-1}^u + \mathbf{w}_t^r + \mathbf{w}_t^w \\
\mathbf{w}_t^r &= \text{softmax}(\text{cosine}(\mathbf{k}_t, \mathbf{M}_t(i))) \\
\mathbf{w}_t^w &= \sigma(\alpha)\mathbf{w}_{t-1}^r + (1-\sigma(\alpha))\mathbf{w}^{lu}_{t-1}\\
\mathbf{w}_t^{lu} &= \mathbf{1}_{w_t^u(i) \leq m(\mathbf{w}_t^u, n)}
\text{, where }m(\mathbf{w}_t^u, n)\text{ is the }n\text{-th smallest element in vector }\mathbf{w}_t^u\text{.}
\end{aligned}
$$

最后，在由 $$\mathbf{w}_t^{lu}$$ 指示的最少使用记忆位置被置零后，每个记忆行更新为：

$$
\mathbf{M}_t(i) = \mathbf{M}_{t-1}(i) + w_t^w(i)\mathbf{k}_t, \forall i
$$

### 元网络

**元网络（Meta Networks）**（[Munkhdalai & Yu, 2017](https://arxiv.org/abs/1703.00837)），简称 **MetaNet**，是一个架构和训练过程专为跨任务*快速*泛化设计的元学习模型。

#### 快权重

MetaNet 的快速泛化依赖"快权重（fast weights）"。关于这一主题有一些论文，但我没有全部细读，也未能找到一个很具体的定义，只有概念上的模糊共识。通常神经网络中的权重由目标函数上的随机梯度下降更新，这个过程是出了名的慢。一种更快的学习方式是用一个神经网络预测另一个神经网络的参数，生成的权重称为*快权重*。相比之下，普通的基于 SGD 的权重称为*慢权重*。

在 MetaNet 中，损失梯度被用作*元信息*来生成学习快权重的模型。慢权重和快权重组合起来在神经网络中做预测。

![slow-fast-weights](https://lilianweng.github.io/posts/2018-11-30-meta-learning/combine-slow-fast-weights.png)

*图 8：在 MLP 中组合慢权重与快权重。$$\bigoplus$$ 是逐元素求和。（图片来源：[原论文](https://arxiv.org/abs/1703.00837)）。*

#### 模型组件

> 免责声明：下面你会发现我的标注与论文中的不同。在我看来，论文写得不怎么样，但思想仍然有趣，所以我用自己的语言来呈现。

MetaNet 的关键组件有：
- 嵌入函数 $$f_\theta$$，由 $$\theta$$ 参数化，把原始输入编码为特征向量。与[孪生神经网络](#convolutional-siamese-neural-network)类似，这些嵌入的训练目的是有助于判断两个输入是否属于同一类（验证任务）。
- 基学习器模型 $$g_\phi$$，由权重 $$\phi$$ 参数化，完成实际的学习任务。

如果到此为止，它看起来就像[关系网络](#relation-network)。MetaNet 除此之外还显式建模两个函数的快权重，并把它们聚合回模型中（见图 8）。

因此我们还需要两个函数分别为 $$f$$ 和 $$g$$ 输出快权重。
- $$F_w$$：由 $$w$$ 参数化的 LSTM，学习嵌入函数 $$f$$ 的快权重 $$\theta^+$$。它以 $$f$$ 在验证任务上的嵌入损失的梯度为输入。
- $$G_v$$：由 $$v$$ 参数化的神经网络，从基学习器 $$g$$ 的损失梯度为其学习快权重 $$\phi^+$$。在 MetaNet 中，学习器的损失梯度被视为任务的*元信息*。

好，现在看元网络如何训练。训练数据包含多对数据集：支持集 $$S=\{\mathbf{x}'_i, y'_i\}_{i=1}^K$$ 和测试集 $$U=\{\mathbf{x}_i, y_i\}_{i=1}^L$$。回忆我们有四个网络和四组要学习的模型参数 $$(\theta, \phi, w, v)$$。

![meta-net](https://lilianweng.github.io/posts/2018-11-30-meta-learning/meta-network.png)

*图 9：MetaNet 架构。*

#### 训练过程

1. 在每个时间步 t 从支持集 $$S$$ 中采样一对随机输入，$$(\mathbf{x}'_i, y'_i)$$ 和 $$(\mathbf{x}'_j, y_j)$$。设 $$\mathbf{x}_{(t,1)}=\mathbf{x}'_i$$，$$\mathbf{x}_{(t,2)}=\mathbf{x}'_j$$。<br/>
对 $$t = 1, \dots, K$$：
    * a\. 计算表征学习损失；即验证任务的交叉熵：<br/>
    $$\mathcal{L}^\text{emb}_t = \mathbf{1}_{y'_i=y'_j} \log P_t + (1 - \mathbf{1}_{y'_i=y'_j})\log(1 - P_t)\text{, where }P_t = \sigma(\mathbf{W}\vert f_\theta(\mathbf{x}_{(t,1)}) - f_\theta(\mathbf{x}_{(t,2)})\vert)$$
2. 计算任务级快权重：
$$\theta^+ = F_w(\nabla_\theta \mathcal{L}^\text{emb}_1, \dots, \mathcal{L}^\text{emb}_T)$$
3. 接下来遍历支持集 $$S$$ 中的样本，计算样本级快权重。同时用学到的表示更新记忆。<br/>
对 $$i=1, \dots, K$$：
    * a\. 基学习器输出概率分布：$$P(\hat{y}_i \vert \mathbf{x}_i) = g_\phi(\mathbf{x}_i)$$，损失可以是交叉熵或 MSE：$$\mathcal{L}^\text{task}_i = y'_i \log g_\phi(\mathbf{x}'_i) + (1- y'_i) \log (1 - g_\phi(\mathbf{x}'_i))$$
    * b\. 提取任务的元信息（损失梯度）并计算样本级快权重：
    $$\phi_i^+ = G_v(\nabla_\phi\mathcal{L}^\text{task}_i)$$
        * 然后把 $$\phi^+_i$$ 存入"值"记忆 $$\mathbf{M}$$ 的第 $$i$$ 个位置。<br/>
    * d\. 用慢权重和快权重一起把支持样本编码为任务专属的输入表示：$$r'_i = f_{\theta, \theta^+}(\mathbf{x}'_i)$$
        * 然后把 $$r'_i$$ 存入"键"记忆 $$\mathbf{R}$$ 的第 $$i$$ 个位置。
4. 最后用测试集 $$U=\{\mathbf{x}_i, y_i\}_{i=1}^L$$ 构造训练损失。<br/>
从 $$\mathcal{L}_\text{train}=0$$ 开始：<br/>
对 $$j=1, \dots, L$$：
    * a\. 把测试样本编码为任务专属的输入表示：
    $$r_j = f_{\theta, \theta^+}(\mathbf{x}_j)$$
    * b\. 通过关注记忆 $$\mathbf{R}$$ 中支持集样本的表示计算快权重。注意力函数任选。这里 MetaNet 用余弦相似度：<br/>
    $$
    \begin{aligned}
    a_j &= \text{cosine}(\mathbf{R}, r_j) = [\frac{r'_1\cdot r_j}{\|r'_1\|\cdot\|r_j\|}, \dots, \frac{r'_N\cdot r_j}{\|r'_N\|\cdot\|r_j\|}]\\
    \phi^+_j &= \text{softmax}(a_j)^\top \mathbf{M}
    \end{aligned}
    $$
    * c\. 更新训练损失：$$\mathcal{L}_\text{train} \leftarrow \mathcal{L}_\text{train} + \mathcal{L}^\text{task}(g_{\phi, \phi^+}(\mathbf{x}_i), y_i) $$
5. 用 $$\mathcal{L}_\text{train}$$ 更新全部参数 $$(\theta, \phi, w, v)$$。

## 基于优化

深度学习模型通过梯度反向传播学习。然而，基于梯度的优化既不是为应对少量训练样本设计的，也不是为在少量优化步骤内收敛设计的。有没有办法调整优化算法，使模型擅长用少量样本学习？这正是基于优化的元学习算法的意图。

### LSTM 元学习器

优化算法可以被显式建模。[Ravi & Larochelle (2017)](https://openreview.net/pdf?id=rJY0-Kcll) 这样做了，并把它命名为"元学习器（meta-learner）"，而处理任务的原始模型称为"学习器（learner）"。元学习器的目标是高效地用小支持集更新学习器的参数，使学习器快速适应新任务。

把学习器模型记为参数 $$\theta$$ 的 $$M_\theta$$，元学习器为参数 $$\Theta$$ 的 $$R_\Theta$$，损失函数为 $$\mathcal{L}$$。

#### 为什么用 LSTM？

元学习器被建模为 LSTM，原因有二：
1. 反向传播中基于梯度的更新与 LSTM 中单元状态的更新之间存在相似性。
2. 知道梯度的历史有益于梯度更新；想想[动量](http://ruder.io/optimizing-gradient-descent/index.html#momentum)是怎么工作的。

时间步 t 以学习率 $$\alpha_t$$ 更新学习器参数：

$$
\theta_t = \theta_{t-1} - \alpha_t \nabla_{\theta_{t-1}}\mathcal{L}_t
$$

若设遗忘门 $$f_t=1$$、输入门 $$i_t = \alpha_t$$、单元状态 $$c_t = \theta_t$$、新单元状态 $$\tilde{c}_t = -\nabla_{\theta_{t-1}}\mathcal{L}_t$$，它与 LSTM 的单元状态更新形式相同：

$$
\begin{aligned}
c_t &= f_t \odot c_{t-1} + i_t \odot \tilde{c}_t\\
    &= \theta_{t-1} - \alpha_t\nabla_{\theta_{t-1}}\mathcal{L}_t
\end{aligned}
$$

固定 $$f_t=1$$ 和 $$i_t=\alpha_t$$ 可能不是最优的，二者都可以是可学习的、可适应不同数据集的。

$$
\begin{aligned}
f_t &= \sigma(\mathbf{W}_f \cdot [\nabla_{\theta_{t-1}}\mathcal{L}_t, \mathcal{L}_t, \theta_{t-1}, f_{t-1}] + \mathbf{b}_f) & \scriptstyle{\text{; how much to forget the old value of parameters.}}\\
i_t &= \sigma(\mathbf{W}_i \cdot [\nabla_{\theta_{t-1}}\mathcal{L}_t, \mathcal{L}_t, \theta_{t-1}, i_{t-1}] + \mathbf{b}_i) & \scriptstyle{\text{; corresponding to the learning rate at time step t.}}\\
\tilde{\theta}_t &= -\nabla_{\theta_{t-1}}\mathcal{L}_t &\\
\theta_t &= f_t \odot \theta_{t-1} + i_t \odot \tilde{\theta}_t &\\
\end{aligned}
$$

#### 模型设定

![lstm-meta-learner](https://lilianweng.github.io/posts/2018-11-30-meta-learning/lstm-meta-learner.png)

*图 10：学习器 $$M_\theta$$ 与元学习器 $$R_\Theta$$ 如何训练。（图片来源：[原论文](https://openreview.net/pdf?id=rJY0-Kcll)，加了更多标注）*

训练过程模仿测试时发生的事情，因为这在[匹配网络](#matching-networks)中已被证明有益。每个训练轮次，我们先采样一个数据集 $$\mathcal{D} = (\mathcal{D}_\text{train}, \mathcal{D}_\text{test}) \in \hat{\mathcal{D}}_\text{meta-train}$$，然后从 $$\mathcal{D}_\text{train}$$ 采样 mini-batch 更新 $$\theta$$ 共 $$T$$ 轮。学习器参数的最终状态 $$\theta_T$$ 用于在测试数据 $$\mathcal{D}_\text{test}$$ 上训练元学习器。

两个需要额外注意的实现细节：
1. 如何压缩 LSTM 元学习器的参数空间？由于元学习器建模的是另一个神经网络的参数，它将有几十万个变量要学。遵循跨坐标共享参数的[思想](https://arxiv.org/abs/1606.04474)，
2. 为简化训练过程，元学习器假设损失 $$\mathcal{L}_t$$ 与梯度 $$\nabla_{\theta_{t-1}} \mathcal{L}_t$$ 相互独立。

![train-meta-learner](https://lilianweng.github.io/posts/2018-11-30-meta-learning/train-meta-learner.png)

### MAML

**MAML** 是 **Model-Agnostic Meta-Learning**（[Finn, et al. 2017](https://arxiv.org/abs/1703.03400)）的缩写，是一个相当通用的优化算法，兼容任何通过梯度下降学习的模型。

设模型为参数 $$\theta$$ 的 $$f_\theta$$。给定任务 $$\tau_i$$ 及其关联数据集 $$(\mathcal{D}^{(i)}_\text{train}, \mathcal{D}^{(i)}_\text{test})$$，我们可以用一步或多步梯度下降更新模型参数（下例只含一步）：

$$
\theta'_i = \theta - \alpha \nabla_\theta\mathcal{L}^{(0)}_{\tau_i}(f_\theta)
$$

其中 $$\mathcal{L}^{(0)}$$ 是用编号 (0) 的 mini 数据批次计算的损失。

![MAML](https://lilianweng.github.io/posts/2018-11-30-meta-learning/maml.png)

*图 11：MAML 示意图。（图片来源：[原论文](https://arxiv.org/abs/1703.03400)）*

上面这个公式只针对一个任务优化。为了在多种任务上取得良好的泛化，我们想找到最优的 $$\theta^*$$，使任务专属的微调更高效。现在，我们采样编号 (1) 的新数据批次来更新元目标。记为 $$\mathcal{L}^{(1)}$$ 的损失依赖 mini-batch (1)。$$\mathcal{L}^{(0)}$$ 与 $$\mathcal{L}^{(1)}$$ 的上标只表示不同的数据批次，它们对同一任务指相同的损失目标。

$$
\begin{aligned}
\theta^* 
&= \arg\min_\theta \sum_{\tau_i \sim p(\tau)} \mathcal{L}_{\tau_i}^{(1)} (f_{\theta'_i}) = \arg\min_\theta \sum_{\tau_i \sim p(\tau)} \mathcal{L}_{\tau_i}^{(1)} (f_{\theta - \alpha\nabla_\theta \mathcal{L}_{\tau_i}^{(0)}(f_\theta)}) & \\
\theta &\leftarrow \theta - \beta \nabla_{\theta} \sum_{\tau_i \sim p(\tau)} \mathcal{L}_{\tau_i}^{(1)} (f_{\theta - \alpha\nabla_\theta \mathcal{L}_{\tau_i}^{(0)}(f_\theta)}) & \scriptstyle{\text{; updating rule}}
\end{aligned}
$$

![MAML Algorithm](https://lilianweng.github.io/posts/2018-11-30-meta-learning/maml-algo.png)

*图 12：MAML 算法的一般形式。（图片来源：[原论文](https://arxiv.org/abs/1703.03400)）*

#### 一阶 MAML

上面的元优化步骤依赖二阶导数。为降低计算代价，MAML 的一个修改版本省略了二阶导数，得到简化且更省的实现，称为**一阶 MAML（First-Order MAML，FOMAML）**。

考虑执行 $$k$$ 步内层梯度更新的情形，$$k\geq1$$。从初始模型参数 $$\theta_\text{meta}$$ 出发：

$$
\begin{aligned}
\theta_0 &= \theta_\text{meta}\\
\theta_1 &= \theta_0 - \alpha\nabla_\theta\mathcal{L}^{(0)}(\theta_0)\\
\theta_2 &= \theta_1 - \alpha\nabla_\theta\mathcal{L}^{(0)}(\theta_1)\\
&\dots\\
\theta_k &= \theta_{k-1} - \alpha\nabla_\theta\mathcal{L}^{(0)}(\theta_{k-1})
\end{aligned}
$$

然后在外层循环，我们采样新的数据批次更新元目标。

$$
\begin{aligned}
\theta_\text{meta} &\leftarrow \theta_\text{meta} - \beta g_\text{MAML} & \scriptstyle{\text{; update for meta-objective}} \\[2mm]
\text{where } g_\text{MAML}
&= \nabla_{\theta} \mathcal{L}^{(1)}(\theta_k) &\\[2mm]
&= \nabla_{\theta_k} \mathcal{L}^{(1)}(\theta_k) \cdot (\nabla_{\theta_{k-1}} \theta_k) \dots (\nabla_{\theta_0} \theta_1) \cdot (\nabla_{\theta} \theta_0) & \scriptstyle{\text{; following the chain rule}} \\
&= \nabla_{\theta_k} \mathcal{L}^{(1)}(\theta_k) \cdot \Big( \prod_{i=1}^k \nabla_{\theta_{i-1}} \theta_i \Big) \cdot I &  \\
&= \nabla_{\theta_k} \mathcal{L}^{(1)}(\theta_k) \cdot \prod_{i=1}^k \nabla_{\theta_{i-1}} (\theta_{i-1} - \alpha\nabla_\theta\mathcal{L}^{(0)}(\theta_{i-1})) &  \\
&= \nabla_{\theta_k} \mathcal{L}^{(1)}(\theta_k) \cdot \prod_{i=1}^k (I - \alpha\nabla_{\theta_{i-1}}(\nabla_\theta\mathcal{L}^{(0)}(\theta_{i-1}))) &
\end{aligned}
$$

MAML 梯度为：

$$
g_\text{MAML} = \nabla_{\theta_k} \mathcal{L}^{(1)}(\theta_k) \cdot \prod_{i=1}^k (I - \alpha \color{red}{\nabla_{\theta_{i-1}}(\nabla_\theta\mathcal{L}^{(0)}(\theta_{i-1}))})
$$

一阶 MAML 忽略红色部分的二阶导数项。它简化如下，等价于最后一次内层梯度更新结果的导数。

$$
g_\text{FOMAML} = \nabla_{\theta_k} \mathcal{L}^{(1)}(\theta_k)
$$

### Reptile

**Reptile**（[Nichol, Achiam & Schulman, 2018](https://arxiv.org/abs/1803.02999)）是一个出奇简单的元学习优化算法。它与 MAML 在许多方面相似：二者都依赖通过梯度下降的元优化，且都与模型无关。

Reptile 的工作方式是反复地：
* 1) 采样一个任务，
* 2) 用多步梯度下降在其上训练，
* 3) 然后把模型权重向新参数移动。

见下面的算法：
$$\text{SGD}(\mathcal{L}_{\tau_i}, \theta, k)$$ 从初始参数 $$\theta$$ 出发，对损失 $$\mathcal{L}_{\tau_i}$$ 执行 k 步随机梯度更新并返回最终参数向量。批处理版本在每次迭代内采样多个任务而非一个。Reptile 梯度定义为 $$(\theta - W)/\alpha$$，其中 $$\alpha$$ 是 SGD 操作使用的步长。

![Reptile Algorithm](https://lilianweng.github.io/posts/2018-11-30-meta-learning/reptile-algo.png)

*图 13：Reptile 算法的批处理版本。（图片来源：[原论文](https://arxiv.org/abs/1803.02999)）*

乍一看，该算法很像普通的 SGD。然而，由于任务专属的优化可以多于一步，当 k > 1 时，它最终使 $$\text{SGD}(\mathbb{E}
_\tau[\mathcal{L}_{\tau}], \theta, k)$$ 不同于 $$\mathbb{E}_\tau [\text{SGD}(\mathcal{L}_{\tau}, \theta, k)]$$。

#### 优化假设

假设任务 $$\tau \sim p(\tau)$$ 存在一个最优网络构型的流形 $$\mathcal{W}_{\tau}^*$$。当 $$\theta$$ 落在 $$\mathcal{W}_{\tau}^*$$ 的曲面上时，模型 $$f_\theta$$ 在任务 $$\tau$$ 上取得最佳性能。要找一个跨任务都好的解，我们想找离所有任务的最优流形都近的参数：

$$
\theta^* = \arg\min_\theta \mathbb{E}_{\tau \sim p(\tau)} [\frac{1}{2} \text{dist}(\theta, \mathcal{W}_\tau^*)^2]
$$

![Reptile Algorithm](https://lilianweng.github.io/posts/2018-11-30-meta-learning/reptile-optim.png)

*图 14：Reptile 算法交替更新参数，使其更接近不同任务的最优流形。（图片来源：[原论文](https://arxiv.org/abs/1803.02999)）*

用 L2 距离作为 $$\text{dist}(.)$$，点 $$\theta$$ 与集合 $$\mathcal{W}_\tau^*$$ 的距离等于 $$\theta$$ 与流形上离 $$\theta$$ 最近的点 $$W_{\tau}^*(\theta)$$ 的距离：

$$
\text{dist}(\theta, \mathcal{W}_{\tau}^*) = \text{dist}(\theta, W_{\tau}^*(\theta)) \text{, where }W_{\tau}^*(\theta) = \arg\min_{W\in\mathcal{W}_{\tau}^*} \text{dist}(\theta, W)
$$

欧氏距离平方的梯度为：

$$
\begin{aligned}
\nabla_\theta[\frac{1}{2}\text{dist}(\theta, \mathcal{W}_{\tau_i}^*)^2]
&= \nabla_\theta[\frac{1}{2}\text{dist}(\theta, W_{\tau_i}^*(\theta))^2] & \\
&= \nabla_\theta[\frac{1}{2}(\theta - W_{\tau_i}^*(\theta))^2] & \\
&= \theta - W_{\tau_i}^*(\theta) & \scriptstyle{\text{; See notes.}}
\end{aligned}
$$

注：根据 Reptile 论文，"点 Θ 与集合 S 之间欧氏距离平方的梯度是向量 2(Θ − p)，其中 p 是 S 中离 Θ 最近的点"。技术上 S 中最近的点也是 Θ 的函数，但我不确定为什么梯度不需要考虑 p 的导数。（如果你有想法，欢迎留言或发邮件给我。）

因此一步随机梯度的更新规则为：

$$
\theta = \theta - \alpha \nabla_\theta[\frac{1}{2} \text{dist}(\theta, \mathcal{W}_{\tau_i}^*)^2] = \theta - \alpha(\theta - W_{\tau_i}^*(\theta)) = (1-\alpha)\theta + \alpha W_{\tau_i}^*(\theta)
$$

最优任务流形上最近的点 $$W_{\tau_i}^*(\theta)$$ 无法精确计算，但 Reptile 用 $$\text{SGD}(\mathcal{L}_\tau, \theta, k)$$ 来近似它。

#### Reptile 与 FOMAML

为展示 Reptile 与 MAML 之间更深层的联系，我们用一个执行两步梯度（$$\text{SGD}(.)$$ 中 k=2）的例子展开更新公式。与[上文](#maml)定义相同，$$\mathcal{L}^{(0)}$$ 和 $$\mathcal{L}^{(1)}$$ 是用不同 mini-batch 数据的损失。为便于阅读，采用两个简化记号：$$g^{(i)}_j = \nabla_{\theta} \mathcal{L}^{(i)}(\theta_j)$$，$$H^{(i)}_j = \nabla^2_{\theta} \mathcal{L}^{(i)}(\theta_j)$$。

$$
\begin{aligned}
\theta_0 &= \theta_\text{meta}\\
\theta_1 &= \theta_0 - \alpha\nabla_\theta\mathcal{L}^{(0)}(\theta_0)= \theta_0 - \alpha g^{(0)}_0 \\
\theta_2 &= \theta_1 - \alpha\nabla_\theta\mathcal{L}^{(1)}(\theta_1) = \theta_0 - \alpha g^{(0)}_0 - \alpha g^{(1)}_1
\end{aligned}
$$

根据[前面小节](#first-order-maml)，FOMAML 的梯度是最后一次内层梯度更新的结果。因此当 k=1 时：

$$
\begin{aligned}
g_\text{FOMAML} &= \nabla_{\theta_1} \mathcal{L}^{(1)}(\theta_1) = g^{(1)}_1 \\
g_\text{MAML} &= \nabla_{\theta_1} \mathcal{L}^{(1)}(\theta_1) \cdot (I - \alpha\nabla^2_{\theta} \mathcal{L}^{(0)}(\theta_0)) = g^{(1)}_1 - \alpha H^{(0)}_0 g^{(1)}_1
\end{aligned}
$$

Reptile 梯度定义为：

$$
g_\text{Reptile} = (\theta_0 - \theta_2) / \alpha = g^{(0)}_0 + g^{(1)}_1
$$

到目前为止我们有：

![Reptile vs FOMAML](https://lilianweng.github.io/posts/2018-11-30-meta-learning/reptile_vs_FOMAML.png)

*图 15：一轮元优化中 Reptile 与 FOMAML 的对比。（图片来源：Yoonho Lee 的 Reptile [幻灯片](https://www.slideshare.net/YoonhoLee4/on-firstorder-metalearning-algorithms)。）*

$$
\begin{aligned}
g_\text{FOMAML} &= g^{(1)}_1 \\
g_\text{MAML} &= g^{(1)}_1 - \alpha H^{(0)}_0 g^{(1)}_1 \\
g_\text{Reptile} &= g^{(0)}_0 + g^{(1)}_1
\end{aligned}
$$

接下来用[泰勒展开](https://en.wikipedia.org/wiki/Taylor_series)进一步展开 $$g^{(1)}_1$$。回忆在数 $$a$$ 处可微的函数 $$f(x)$$ 的泰勒展开为：

$$
f(x) = f(a) + \frac{f'(a)}{1!}(x-a) + \frac{f''(a)}{2!}(x-a)^2 + \dots = \sum_{i=0}^\infty \frac{f^{(i)}(a)}{i!}(x-a)^i
$$

我们可以把 $$\nabla_{\theta}\mathcal{L}^{(1)}(.)$$ 视为一个函数，把 $$\theta_0$$ 视为取值点。$$g_1^{(1)}$$ 在取值点 $$\theta_0$$ 处的泰勒展开为：

$$
\begin{aligned}
g_1^{(1)} &= \nabla_{\theta}\mathcal{L}^{(1)}(\theta_1) \\
&= \nabla_{\theta}\mathcal{L}^{(1)}(\theta_0) + \nabla^2_\theta\mathcal{L}^{(1)}(\theta_0)(\theta_1 - \theta_0) + \frac{1}{2}\nabla^3_\theta\mathcal{L}^{(1)}(\theta_0)(\theta_1 - \theta_0)^2 + \dots & \\
&= g_0^{(1)} - \alpha H^{(1)}_0 g_0^{(0)} + \frac{\alpha^2}{2}\nabla^3_\theta\mathcal{L}^{(1)}(\theta_0) (g_0^{(0)})^2 + \dots & \scriptstyle{\text{; because }\theta_1-\theta_0=-\alpha g_0^{(0)}} \\
&= g_0^{(1)} - \alpha H^{(1)}_0 g_0^{(0)} + O(\alpha^2)
\end{aligned}
$$

把展开后的 $$g_1^{(1)}$$ 代入一步内层梯度更新的 MAML 梯度：

$$
\begin{aligned}
g_\text{FOMAML} &= g^{(1)}_1 = g_0^{(1)} - \alpha H^{(1)}_0 g_0^{(0)} + O(\alpha^2)\\
g_\text{MAML} &= g^{(1)}_1 - \alpha H^{(0)}_0 g^{(1)}_1 \\
&= g_0^{(1)} - \alpha H^{(1)}_0 g_0^{(0)} + O(\alpha^2) - \alpha H^{(0)}_0 (g_0^{(1)} - \alpha H^{(1)}_0 g_0^{(0)} + O(\alpha^2))\\
&= g_0^{(1)} - \alpha H^{(1)}_0 g_0^{(0)} - \alpha H^{(0)}_0 g_0^{(1)} + \alpha^2 \alpha H^{(0)}_0 H^{(1)}_0 g_0^{(0)} + O(\alpha^2)\\
&= g_0^{(1)} - \alpha H^{(1)}_0 g_0^{(0)} - \alpha H^{(0)}_0 g_0^{(1)} + O(\alpha^2)
\end{aligned}
$$

Reptile 梯度变为：

$$
\begin{aligned}
g_\text{Reptile} 
&= g^{(0)}_0 + g^{(1)}_1 \\
&= g^{(0)}_0 + g_0^{(1)} - \alpha H^{(1)}_0 g_0^{(0)} + O(\alpha^2)
\end{aligned}
$$

至此我们有了三种梯度的公式：

$$
\begin{aligned}
g_\text{FOMAML} &= g_0^{(1)} - \alpha H^{(1)}_0 g_0^{(0)} + O(\alpha^2)\\
g_\text{MAML} &= g_0^{(1)} - \alpha H^{(1)}_0 g_0^{(0)} - \alpha H^{(0)}_0 g_0^{(1)} + O(\alpha^2)\\
g_\text{Reptile}  &= g^{(0)}_0 + g_0^{(1)} - \alpha H^{(1)}_0 g_0^{(0)} + O(\alpha^2)
\end{aligned}
$$

训练中，我们常对多个数据批次取平均。在我们的例子中，mini-batch (0) 和 (1) 是可交换的，因为二者都是随机抽取的。期望 $$\mathbb{E}_{\tau,0,1}$$ 是对任务 $$\tau$$ 的编号 (0) 和 (1) 两个数据批次取平均。

设，
- $$A = \mathbb{E}_{\tau,0,1} [g_0^{(0)}] = \mathbb{E}_{\tau,0,1} [g_0^{(1)}]$$；它是任务损失的平均梯度。我们期望沿 $$A$$ 指向的方向改进模型参数以取得更好的任务性能。
- $$B = \mathbb{E}_{\tau,0,1} [H^{(1)}_0 g_0^{(0)}] = \frac{1}{2}\mathbb{E}_{\tau,0,1} [H^{(1)}_0 g_0^{(0)} + H^{(0)}_0 g_0^{(1)}] = \frac{1}{2}\mathbb{E}_{\tau,0,1} [\nabla_\theta(g^{(0)}_0 g_0^{(1)})]$$；它是增大同一任务两个不同 mini-batch 梯度内积的方向（梯度）。我们期望沿 $$B$$ 指向的方向改进模型参数以取得对不同数据更好的泛化。

总结：当梯度更新由前三阶主导项近似时，MAML 与 Reptile 的优化目标相同——更好的任务性能（由 A 引导）和更好的泛化（由 B 引导）。

$$
\begin{aligned}
\mathbb{E}_{\tau,1,2}[g_\text{FOMAML}] &= A - \alpha B + O(\alpha^2)\\
\mathbb{E}_{\tau,1,2}[g_\text{MAML}] &= A - 2\alpha B + O(\alpha^2)\\
\mathbb{E}_{\tau,1,2}[g_\text{Reptile}]  &= 2A - \alpha B + O(\alpha^2)
\end{aligned}
$$

我不清楚被忽略的 $$O(\alpha^2)$$ 项是否会对参数学习产生大影响。但鉴于 FOMAML 能取得与完整版 MAML 相近的性能，或许可以放心地说：更高阶导数在梯度下降更新中并非关键。

---

引用格式：

```
@article{weng2018metalearning,
  title   = "Meta-Learning: Learning to Learn Fast",
  author  = "Weng, Lilian",
  journal = "lilianweng.github.io/lil-log",
  year    = "2018",
  url     = "http://lilianweng.github.io/lil-log/2018/11/29/meta-learning.html"
}
```

*如果你发现本文中的错误，请毫不犹豫地留言或联系我 [lilian dot wengweng at gmail dot com]，我会非常乐意尽快修正。*

下一篇文章见！

## 参考文献

[1] Brenden M. Lake, Ruslan Salakhutdinov, and Joshua B. Tenenbaum. ["Human-level concept learning through probabilistic program induction."](https://www.cs.cmu.edu/~rsalakhu/papers/LakeEtAl2015Science.pdf) Science 350.6266 (2015): 1332-1338.

[2] Oriol Vinyals' talk on ["Model vs Optimization Meta Learning"](http://metalearning-symposium.ml/files/vinyals.pdf)

[3] Gregory Koch, Richard Zemel, and Ruslan Salakhutdinov. ["Siamese neural networks for one-shot image recognition."](http://www.cs.toronto.edu/~rsalakhu/papers/oneshot1.pdf) ICML Deep Learning Workshop. 2015.

[4] Oriol Vinyals, et al. ["Matching networks for one shot learning."](http://papers.nips.cc/paper/6385-matching-networks-for-one-shot-learning.pdf) NIPS. 2016.

[5] Flood Sung, et al. ["Learning to compare: Relation network for few-shot learning."](http://openaccess.thecvf.com/content_cvpr_2018/papers_backup/Sung_Learning_to_Compare_CVPR_2018_paper.pdf) CVPR. 2018.

[6] Jake Snell, Kevin Swersky, and Richard Zemel. ["Prototypical Networks for Few-shot Learning."](http://papers.nips.cc/paper/6996-prototypical-networks-for-few-shot-learning.pdf) CVPR. 2018.

[7] Adam Santoro, et al. ["Meta-learning with memory-augmented neural networks."](http://proceedings.mlr.press/v48/santoro16.pdf) ICML. 2016.

[8] Alex Graves, Greg Wayne, and Ivo Danihelka. ["Neural turing machines."](https://arxiv.org/abs/1410.5401) arXiv preprint arXiv:1410.5401 (2014).

[9] Tsendsuren Munkhdalai and Hong Yu. ["Meta Networks."](https://arxiv.org/abs/1703.00837) ICML. 2017.

[10] Sachin Ravi and Hugo Larochelle. ["Optimization as a Model for Few-Shot Learning."](https://openreview.net/pdf?id=rJY0-Kcll) ICLR. 2017.

[11] Chelsea Finn's BAIR blog on ["Learning to Learn"](https://bair.berkeley.edu/blog/2017/07/18/learning-to-learn/).

[12] Chelsea Finn, Pieter Abbeel, and Sergey Levine. ["Model-agnostic meta-learning for fast adaptation of deep networks."](https://arxiv.org/abs/1703.03400) ICML 2017.

[13] Alex Nichol, Joshua Achiam, John Schulman. ["On First-Order Meta-Learning Algorithms."](https://arxiv.org/abs/1803.02999) arXiv preprint arXiv:1803.02999 (2018).

[14] [Slides on Reptile](https://www.slideshare.net/YoonhoLee4/on-firstorder-metalearning-algorithms) by Yoonho Lee.
