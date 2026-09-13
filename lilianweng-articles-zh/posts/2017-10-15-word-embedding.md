---
title: "学习词嵌入"
title_en: "Learning Word Embedding"
source: https://lilianweng.github.io/posts/2017-10-15-word-embedding/
crawled: 2026-09-08
translated: 2026-09-08
---

# 学习词嵌入

> 原文：[Learning Word Embedding](https://lilianweng.github.io/posts/2017-10-15-word-embedding/) · Lilian Weng（翁荔）

> 词嵌入（word embedding）是以数值向量形式对词语的稠密表示。它可以通过多种语言模型来学习。词嵌入表示能够揭示词语之间许多隐藏的关系。例如，vector("cat") - vector("kitten") 与 vector("dog") - vector("puppy") 相似。本文介绍几种学习词嵌入的模型，以及为达成这一目的它们的损失函数是如何设计的。

人类的词汇以自由文本的形式存在。为了让机器学习模型理解并处理自然语言，我们需要把自由文本的词转换为数值。最简单的转换方法之一是独热编码（one-hot encoding）：每个不同的词代表结果向量的一个维度，二值取值表示该词出现（1）与否（0）。

然而，在处理整个词表时，独热编码在计算上并不现实，因为这种表示需要几十万维。词嵌入用维度低得多（因而更稠密）的（非二值）数值向量来表示词和短语。对好的词嵌入的一个直观假设是：它们能近似词与词之间的相似性（即 "cat" 和 "kitten" 是相似的词，因此在降维后的向量空间中应当相近），或揭示隐藏的语义关系（即 "cat" 与 "kitten" 之间的关系类比于 "dog" 与 "puppy" 之间的关系）。上下文信息对学习词义和词间关系极为有用，因为相似的词往往出现在相似的上下文中。

学习词嵌入主要有两条路径，二者都依赖上下文知识。
- **基于计数（Count-based）**：第一条路径是无监督的，基于全局词共现矩阵的矩阵分解。原始的共现计数效果并不好，因此我们要在其之上做聪明的处理。
- **基于上下文（Context-based）**：第二条路径是监督式的。给定局部上下文，我们设计一个模型来预测目标词，与此同时，该模型学习到高效的词嵌入表示。

## 基于计数的向量空间模型

基于计数的向量空间模型严重依赖词频和共现矩阵，其假设是：出现在相同上下文中的词具有相似或相关的语义。这类模型把共现计数等统计量映射为小而稠密的词向量。PCA、主题模型和神经概率语言模型都是这一类的典型例子。

---

与基于计数的方法不同，基于上下文的方法构建直接以"给定相邻词预测某个词"为目标的预测模型。稠密词向量是模型参数的一部分，每个词的最佳向量表示在模型训练过程中学习得到。

## 基于上下文：Skip-Gram 模型

设想一个固定大小的滑动窗口沿句子移动：中间的词是"目标词"，滑动窗口内其左右的词是上下文词。skip-gram 模型（[Mikolov et al., 2013](https://arxiv.org/pdf/1301.3781.pdf)）被训练来预测"给定目标词时，某个词是其上下文词"的概率。

下面的例子展示了由 5 词窗口沿句子滑动生成的多组目标词—上下文词训练样本。

> "The man who passes the sentence should swing the sword." -- Ned Stark

| 滑动窗口（大小 = 5）  |  目标词  |  上下文 |
| ------------ | ------------ | ------------ |
| [The man who] | the  | man, who | 
| [The man who passes] | man | the, who, passes | 
| [The man who passes the] | who | the, man, passes, the | 
| [man who passes the sentence] | passes | man, who, the, sentence
| ... | ... | ... |
| [sentence should swing the sword] | swing | sentence, should, the, sword |
| [should swing the sword] | the | should, swing, sword |
| [swing the sword] | sword | swing, the |

每个上下文—目标对都被视为数据中的一条新观测。例如，上例中的目标词 "swing" 产生四个训练样本：("swing", "sentence")、("swing", "should")、("swing", "the") 和 ("swing", "sword")。

![Skip-Gram 模型](https://lilianweng.github.io/posts/2017-10-15-word-embedding/word2vec-skip-gram.png)

*图 1：skip-gram 模型。输入向量 $$\mathbf{x}$$ 和输出 $$\mathbf{y}$$ 都是独热编码的词表示。隐藏层即大小为 $$N$$ 的词嵌入。*

给定词表大小 $$V$$，我们要学习大小为 $$N$$ 的词嵌入向量。模型每次学习用一个目标词（输入）预测一个上下文词（输出）。

根据图 1：

- 输入词 $$w_i$$ 和输出词 $$w_j$$ 都被独热编码为大小为 $$V$$ 的二值向量 $$\mathbf{x}$$ 和 $$\mathbf{y}$$。
- 首先，二值向量 $$\mathbf{x}$$ 与大小为 $$V \times N$$ 的词嵌入矩阵 $$W$$ 相乘，得到输入词 $$w_i$$ 的嵌入向量：即矩阵 $$W$$ 的第 i 行。
- 这个新得到的 $$N$$ 维嵌入向量构成隐藏层。
- 隐藏层与大小为 $$N \times V$$ 的词上下文矩阵 $$W'$$ 相乘，产生独热编码的输出向量 $$\mathbf{y}$$。
- 输出上下文矩阵 $$W'$$ 以"作为上下文"的角色编码词义，这与嵌入矩阵 $$W$$ 不同。注意：尽管名字如此，$$W’$$ 独立于 $$W$$，不是它的转置或逆或任何诸如此类的关系。

## 基于上下文：连续词袋模型（CBOW）

连续词袋模型（Continuous Bag-of-Words，CBOW）是另一个类似的词向量学习模型。它从源上下文词（即 "sentence should the sword"）预测目标词（即 "swing"）。

![CBOW 模型](https://lilianweng.github.io/posts/2017-10-15-word-embedding/word2vec-cbow.png)

*图 2：CBOW 模型。多个上下文词的词向量被平均，得到隐藏层中固定长度的向量。其他符号含义与图 1 相同。*

由于有多个上下文词，我们把输入向量与矩阵 $$W$$ 相乘得到的对应词向量取平均。因为平均阶段抹平了大量分布信息，有人认为 CBOW 模型更适合小数据集。

## 损失函数

skip-gram 模型和 CBOW 模型的训练都应最小化一个精心设计的损失/目标函数。我们可以采用若干种损失函数来训练这些语言模型。下面的讨论将以 skip-gram 模型为例，说明损失如何计算。

### 完整 Softmax

skip-gram 模型用矩阵 $$W$$ 定义每个词的嵌入向量，用输出矩阵 $$W’$$ 定义上下文向量。给定输入词 $$w_I$$，我们把 $$W$$ 中对应的行记为向量 $$v_{w_I}$$（嵌入向量），把 $$W’$$ 中对应的列记为 $$v'_{w_I}$$（上下文向量）。最后的输出层对"给定 $$w_I$$ 时预测输出词 $$w_O$$"的概率施加 softmax，因此：

$$
p(w_O \vert w_I) = \frac{\exp({v'_{w_O}}^{\top} v_{w_I})}{\sum_{i=1}^V \exp({v'_{w_i}}^{\top} v_{w_I})}
$$

正如图 1 所示，这很精确。然而当 $$V$$ 极大时，对每个样本都遍历所有词来计算分母在计算上并不现实。对更高效的条件概率估计的需求催生了*层次 softmax（hierarchical softmax）*等新方法。

### 层次 Softmax

Morin 和 Bengio（[2005](https://www.iro.umontreal.ca/~lisa/pointeurs/hierarchical-nnlm-aistats05.pdf)）提出层次 softmax，借助二叉树结构让求和计算更快。层次 softmax 把语言模型的输出 softmax 层编码为树形层级：每个叶子是一个词，每个内部节点代表其子节点的相对概率。

![层次 Softmax](https://lilianweng.github.io/posts/2017-10-15-word-embedding/word2vec-hierarchical-softmax.png)

*图 3：层次 softmax 二叉树示意图。白色的叶子节点是词表中的词。灰色内部节点携带到达其子节点的概率信息。一条从根到叶子 $$w_i$$ 的路径，$$n(w_i, j)$$ 表示该路径上的第 j 个节点。（图片来源：[word2vec Parameter Learning Explained](https://arxiv.org/pdf/1411.2738.pdf)）*

每个词 $$w_i$$ 都有一条从根到其对应叶子的唯一路径。选中这个词的概率等价于从根出发沿树枝走到该叶子的概率。由于我们知道内部节点 $$n$$ 的嵌入向量 $$v_n$$，得到该词的概率可以由在每个内部节点站向左转或向右转的概率的乘积计算。

根据图 3，一个节点的概率为（$$\sigma$$ 是 sigmoid 函数）：

$$
\begin{align}
p(\text{turn right} \to \dots w_I \vert n) &= \sigma({v'_n}^{\top} v_{w_I})\\
p(\text{turn left } \to \dots w_I \vert n) &= 1 - p(\text{turn right} \vert n) = \sigma(-{v'_n}^{\top} v_{w_I})
\end{align}
$$

给定输入词 $$w_I$$，最终得到上下文词 $$w_O$$ 的概率为：

$$
p(w_O \vert w_I) = \prod_{k=1}^{L(w_O)} \sigma(\mathbb{I}_{\text{turn}}(n(w_O, k), n(w_O, k+1)) \cdot {v'_{n(w_O, k)}}^{\top} v_{w_I})
$$

其中 $$L(w_O)$$ 是通往词 $$w_O$$ 的路径深度，$$\mathbb{I}_{\text{turn}}$$ 是一个特殊的指示函数：若 $$n(w_O, k+1)$$ 是 $$n(w_O, k)$$ 的左子节点则返回 1，否则返回 -1。内部节点的嵌入在模型训练中学习。树结构把训练时分母估计的复杂度从 O(V)（词表大小）大幅降到 O(log V)（树的深度）。不过在预测时，由于我们事先不知道要到达哪个叶子，仍需计算每个词的概率并选出最佳的。

良好的树结构对模型性能至关重要。几条实用的原则是：按词频组织词（如 Huffman 树的实现，可简单加速）；把相似的词归入相同或相近的分支（如使用预定义的词聚类、WordNet）。

<!-- Morin and Bengio use the synsets in WordNet as clusters for the tree. Mnih and Hinton learn the tree structure with a clustering algorithm that recursively partitions the words in two clusters. -->

### 交叉熵

另一种做法完全绕开 softmax 框架。损失函数改为度量预测概率 $$p$$ 与真实二值标签 $$\mathbf{y}$$ 之间的交叉熵。

首先回顾：两个分布 $$p$$ 和 $$q$$ 之间的交叉熵为 $$ H(p, q) = -\sum_x p(x) \log q(x) $$。在我们的场景中，只有当 $$w_i$$ 是输出词时真实标签 $$y_i$$ 为 1；否则 $$y_j$$ 为 0。参数配置为 $$\theta$$ 的模型，其损失函数 $$\mathcal{L}_\theta$$ 旨在最小化预测与真值之间的交叉熵——交叉熵越低表明两个分布越相似。

$$
\mathcal{L}_\theta = - \sum_{i=1}^V y_i \log p(w_i | w_I) = - \log p(w_O \vert w_I)
$$

回忆一下：

$$
p(w_O \vert w_I) = \frac{\exp({v'_{w_O}}^{\top} v_{w_I})}{\sum_{i=1}^V \exp({v'_{w_i}}^{\top} v_{w_I})}
$$

因此，

$$
\mathcal{L}_{\theta} 
= - \log \frac{\exp({v'_{w_O}}^{\top}{v_{w_I}})}{\sum_{i=1}^V \exp({v'_{w_i}}^{\top}{v_{w_I} })}
= - {v'_{w_O}}^{\top}{v_{w_I} } + \log \sum_{i=1}^V \exp({v'_{w_i} }^{\top}{v_{w_I}})
$$

要用 SGD 反向传播开始训练模型，我们需要计算损失函数的梯度。为简单起见，记 $$z_{IO} = {v'_{w_O}}^{\top}{v_{w_I}}$$。

$$
\begin{align}
\nabla_\theta \mathcal{L}_{\theta}
&= \nabla_\theta\big( - z_{IO} + \log \sum_{i=1}^V e^{z_{Ii}} \big) \\ 
&= - \nabla_\theta z_{IO} + \nabla_\theta \big( \log \sum_{i=1}^V e^{z_{Ii}} \big) \\
&= - \nabla_\theta z_{IO} + \frac{1}{\sum_{i=1}^V e^{z_{Ii}}} \sum_{i=1}^V e^{z_{Ii}} \nabla_\theta z_{Ii} \\
&= - \nabla_\theta z_{IO} + \sum_{i=1}^V \frac{e^{z_{Ii}}}{\sum_{i=1}^V e^{z_{Ii}}} \nabla_\theta z_{Ii} \\
&= - \nabla_\theta z_{IO} + \sum_{i=1}^V p(w_i \vert w_I) \nabla_\theta z_{Ii} \\
&= - \nabla_\theta z_{IO} + \mathbb{E}_{w_i \sim Q(\tilde{w})} \nabla_\theta z_{Ii}
\end{align}
$$

其中 $$Q(\tilde{w})$$ 是噪声样本的分布。

根据上式，第一项对正确的输出词给出正向强化（$$\nabla_\theta z_{IO}$$ 越大损失越好），而其他词的负面影响由第二项刻画。

如何用一组噪声词样本来估计 $$\mathbb{E}_{w_i \sim Q(\tilde{w})} \nabla_\theta {v'_{w_i}}^{\top}{v_{w_I}}$$，而不是扫遍整个词表，是基于交叉熵的采样方法的关键。

### 噪声对比估计（NCE）

噪声对比估计（Noise Contrastive Estimation，NCE）度量旨在用一个逻辑回归分类器把目标词与噪声样本区分开来（[Gutmann and Hyvärinen, 2010](http://proceedings.mlr.press/v9/gutmann10a/gutmann10a.pdf)）。

给定输入词 $$w_I$$，正确的输出词已知为 $$w$$。同时，我们从噪声样本分布 $$Q$$ 中采样 $$N$$ 个其他词，记作 $$\tilde{w}_1
, \tilde{w}_2, \dots, \tilde{w}_N \sim Q$$。把二分类器的决策记为 $$d$$，$$d$$ 只能取二值。

$$
\mathcal{L}_\theta = - [ \log p(d=1 \vert w, w_I) + \sum_{i=1, \tilde{w}_i \sim Q}^N \log p(d=0|\tilde{w}_i, w_I) ]
$$

当 $$N$$ 足够大时，根据[大数定律](https://en.wikipedia.org/wiki/Law_of_large_numbers)，

$$
\mathcal{L}_\theta = - [ \log p(d=1 \vert w, w_I) +  N\mathbb{E}_{\tilde{w}_i \sim Q} \log p(d=0|\tilde{w}_i, w_I)]
$$

要计算概率 $$p(d=1 \vert w, w_I)$$，可以从联合概率 $$p(d, w \vert w_I)$$ 出发。在 $$w, \tilde{w}_1, \tilde{w}_2, \dots, \tilde{w}_N$$ 之中，我们有 1/(N+1) 的机会选中真实词 $$w$$（从条件概率 $$p(w \vert w_I)$$ 采样）；同时有 N/(N+1) 的机会选中一个噪声词（每个从 $$q(\tilde{w}) \sim Q$$ 采样）。于是，

$$
p(d, w | w_I) = 
  \begin{cases}
  \frac{1}{N+1} p(w \vert w_I) & \text{if } d=1 \\
  \frac{N}{N+1} q(\tilde{w}) & \text{if } d=0
  \end{cases}
$$

然后可以解出 $$p(d=1 \vert w, w_I)$$ 和 $$p(d=0 \vert w, w_I)$$：

$$
\begin{align}
p(d=1 \vert w, w_I) 
&= \frac{p(d=1, w \vert w_I)}{p(d=1, w \vert w_I) + p(d=0, w \vert w_I)}
&= \frac{p(w \vert w_I)}{p(w \vert w_I) + Nq(\tilde{w})}
\end{align}
$$

$$
\begin{align}
p(d=0 \vert w, w_I) 
&= \frac{p(d=0, w \vert w_I)}{p(d=1, w \vert w_I) + p(d=0, w \vert w_I)}
&= \frac{Nq(\tilde{w})}{p(w \vert w_I) + Nq(\tilde{w})}
\end{align}
$$

最终，NCE 二分类器的损失函数变为：

$$
\begin{align}
\mathcal{L}_\theta 
& = - [ \log p(d=1 \vert w, w_I) +  \sum_{\substack{i=1 \\ \tilde{w}_i \sim Q}}^N \log p(d=0|\tilde{w}_i, w_I)] \\
& = - [ \log \frac{p(w \vert w_I)}{p(w \vert w_I) + Nq(\tilde{w})} +  \sum_{\substack{i=1 \\ \tilde{w}_i \sim Q}}^N \log \frac{Nq(\tilde{w}_i)}{p(w \vert w_I) + Nq(\tilde{w}_i)}]
\end{align}
$$

然而 $$p(w \vert w_I)$$ 的分母仍然涉及对整个词表求和。我们把分母记为输入词的配分函数 $$Z(w_I)$$。一个常见假设是 $$Z(w) \approx 1$$，因为我们期望 softmax 输出层是归一化的（[Minh and Teh, 2012](https://www.cs.toronto.edu/~amnih/papers/ncelm.pdf)）。于是损失函数简化为：

$$
\mathcal{L}_\theta = - [ \log \frac{\exp({v'_w}^{\top}{v_{w_I}})}{\exp({v'_w}^{\top}{v_{w_I}}) + Nq(\tilde{w})} +  \sum_{\substack{i=1 \\ \tilde{w}_i \sim Q}}^N \log \frac{Nq(\tilde{w}_i)}{\exp({v'_w}^{\top}{v_{w_I}}) + Nq(\tilde{w}_i)}]
$$

噪声分布 $$Q$$ 是一个可调参数，我们希望这样设计它：
- 直觉上它应当与真实数据分布非常相似；且
- 应当容易从中采样。

例如，tensorflow 中 NCE 损失的采样实现（[log_uniform_candidate_sampler](https://github.com/tensorflow/tensorflow/blob/master/tensorflow/python/ops/candidate_sampling_ops.py#L83)）假设噪声样本服从对数均匀分布，也就是 [Zipf 定律](https://en.wikipedia.org/wiki/Zipf%27s_law)。一个词取对数后的概率期望与其排名成反比，高频词被赋予较低的排名。此时 $$q(\tilde{w}) = \frac{1}{ \log V}(\log (r_{\tilde{w}} + 1) - \log r_{\tilde{w}})$$，其中 $$r_{\tilde{w}} \in [1, V]$$ 是按频率降序排列的词排名。

### 负采样（NEG）

Mikolov 等人（[2013](https://papers.nips.cc/paper/5021-distributed-representations-of-words-and-phrases-and-their-compositionality.pdf)）提出的负采样（Negative Sampling，NEG）是 NCE 损失的一个简化变体。它因用于训练 Google 的 [word2vec](https://code.google.com/archive/p/word2vec/) 项目而格外著名。与试图近似最大化 softmax 输出对数概率的 NCE 损失不同，负采样做了进一步简化，因为它专注于学习高质量的词嵌入，而不是对自然语言中的词分布建模。

NEG 用 sigmoid 函数近似二分类器的输出：

$$
\begin{align}
p(d=1 \vert w_, w_I) &= \sigma({v'_{w}}^\top v_{w_I}) \\
p(d=0 \vert w, w_I) &= 1 - \sigma({v'_{w}}^\top v_{w_I}) = \sigma(-{v'_{w}}^\top v_{w_I})
\end{align}
$$

最终的 NCE 损失函数形如：

$$
\mathcal{L}_\theta = - [ \log \sigma({v'_{w}}^\top v_{w_I}) +  \sum_{\substack{i=1 \\ \tilde{w}_i \sim Q}}^N \log \sigma(-{v'_{\tilde{w}_i}}^\top v_{w_I})]
$$

## 学习词嵌入的其他技巧

Mikolov 等人（[2013](https://papers.nips.cc/paper/5021-distributed-representations-of-words-and-phrases-and-their-compositionality.pdf)）给出了几条能带来良好词嵌入学习效果的实用做法。

- **软滑动窗口**。在滑动窗口内配对词时，可以给距离更远的词更低的权重。一个启发式做法是——给定最大窗口大小参数 $$s_{\text{max}}$$，对每个训练样本，实际窗口大小在 1 到 $$s_{\text{max}}$$ 之间随机采样。这样，每个上下文词以 1/（它到目标词的距离）的概率被观测到，而紧邻的词总是被观测到。

- **对高频词降采样**。极高频词可能过于泛化，难以区分上下文（想想停用词）。另一方面，罕见词更可能携带独特信息。为平衡高频词与罕见词，Mikolov 等人提出在采样时以概率 $$1-\sqrt{t/f(w)}$$ 丢弃词 $$w$$。其中 $$f(w)$$ 是词频，$$t$$ 是可调阈值。

- **先学习短语**。短语常常作为一个概念单元存在，而不是单个词的简单组合。例如，即使知道 "new" 和 "york" 的含义，我们也无法真正断定 "New York" 是一个城市名。先学习这类短语、在训练词嵌入模型前把它们当作词单元，能提升结果质量。一种简单的数据驱动方法基于一元和二元计数：$$s_{\text{phrase}} = \frac{C(w_i w_j) - \delta}{ C(w_i)C(w_j)}$$，其中 $$C(.)$$ 是一元词 $$w_i$$ 或二元词组 $$w_i w_j$$ 的简单计数，$$\delta$$ 是防止极罕见词和短语的折扣阈值。分数越高，成为短语的可能性越大。要构成多于两个词的短语，可以用递减的分数阈值多次扫描词表。

## GloVe：全局向量

Pennington 等人（[2014](http://www.aclweb.org/anthology/D14-1162)）提出的全局向量（Global Vector，GloVe）模型旨在把基于计数的矩阵分解与基于上下文的 skip-gram 模型结合起来。

我们都知道计数和共现能揭示词义。为了与词嵌入语境下的 $$p(w_O \vert w_I)$$ 区分，我们把共现概率定义为：

$$
p_{\text{co}}(w_k \vert w_i) = \frac{C(w_i, w_k)}{C(w_i)}
$$

$$C(w_i, w_k)$$ 统计词 $$w_i$$ 与 $$w_k$$ 的共现次数。

设有两个词 $$w_i$$="ice" 和 $$w_j$$="steam"。第三个词 $$\tilde{w}_k$$="solid" 与 "ice" 相关而与 "steam" 无关，因此我们预期 $$p_{\text{co}}(\tilde{w}_k \vert w_i)$$ 远大于 $$p_{\text{co}}(\tilde{w}_k \vert w_j)$$，从而 $$\frac{p_{\text{co}}(\tilde{w}_k \vert w_i)}{p_{\text{co}}(\tilde{w}_k \vert w_j)}$$ 非常大。若第三个词 $$\tilde{w}_k$$ = "water" 与两者都相关，或 $$\tilde{w}_k$$ = "fashion" 与两者都无关，则 $$\frac{p_{\text{co}}(\tilde{w}_k \vert w_i)}{p_{\text{co}}(\tilde{w}_k \vert w_j)}$$ 期望接近 1。

这里的直觉是：词义由共现概率的比值而非概率本身所捕捉。全局向量把两个词相对于第三个上下文词的关系建模为：

$$
F(w_i, w_j, \tilde{w}_k) = \frac{p_{\text{co}}(\tilde{w}_k \vert w_i)}{p_{\text{co}}(\tilde{w}_k \vert w_j)}
$$

进一步，由于目标是学习有意义的词向量，$$F$$ 被设计为两词线性差 $$w_i - w_j$$ 的函数：

$$
F((w_i - w_j)^\top \tilde{w}_k) = \frac{p_{\text{co}}(\tilde{w}_k \vert w_i)}{p_{\text{co}}(\tilde{w}_k \vert w_j)}
$$

考虑到 $$F$$ 应在目标词与上下文词之间对称，最终的解决方案是把 $$F$$ 建模为一个**指数**函数。方程的更多细节请阅读原论文（[Pennington et al., 2014](http://www.aclweb.org/anthology/D14-1162)）。

$$
\begin{align}
F({w_i}^\top \tilde{w}_k) &= \exp({w_i}^\top \tilde{w}_k) = p_{\text{co}}(\tilde{w}_k \vert w_i) \\
F((w_i - w_j)^\top \tilde{w}_k) &= \exp((w_i - w_j)^\top \tilde{w}_k) = \frac{\exp(w_i^\top \tilde{w}_k)}{\exp(w_j^\top \tilde{w}_k)} = \frac{p_{\text{co}}(\tilde{w}_k \vert w_i)}{p_{\text{co}}(\tilde{w}_k \vert w_j)}
\end{align}
$$

最终，

$$
{w_i}^\top \tilde{w}_k = \log p_{\text{co}}(\tilde{w}_k \vert w_i) = \log \frac{C(w_i, \tilde{w}_k)}{C(w_i)} = \log C(w_i, \tilde{w}_k) - \log C(w_i)
$$

由于第二项 $$-\log C(w_i)$$ 与 $$k$$ 无关，我们可以为 $$w_i$$ 加上偏置项 $$b_i$$ 来捕捉 $$-\log C(w_i)$$。为保持对称形式，我们也为 $$\tilde{w}_k$$ 加上偏置 $$\tilde{b}_k$$。

$$
\log C(w_i, \tilde{w}_k) = {w_i}^\top \tilde{w}_k + b_i + \tilde{b}_k
$$

GloVe 模型的损失函数通过最小化平方误差之和来保持上式：

$$
\mathcal{L}_\theta = \sum_{i=1, j=1}^V f(C(w_i,w_j)) ({w_i}^\top \tilde{w}_j + b_i + \tilde{b}_j - \log C(w_i, \tilde{w}_j))^2
$$

加权方案 $$f(c)$$ 是 $$w_i$$ 与 $$w_j$$ 共现次数的函数，是可调的模型配置。当 $$c \to 0$$ 时它应接近零；它应是非递减的，因为更高的共现应有更大的影响；当 $$c$$ 极大时它应饱和。论文提出了如下加权函数：

$$
f(c) = 
  \begin{cases}
  (\frac{c}{c_{\max}})^\alpha & \text{if } c < c_{\max} \text{, } c_{\max} \text{ is adjustable.} \\
  1 & \text{if } \text{otherwise}
  \end{cases}
$$

## 示例：在"权力的游戏"上训练 word2vec

在回顾完上述全部理论之后，让我们用"权力的游戏语料库"做个词嵌入的小实验。使用 [gensim](https://radimrehurek.com/gensim/models/word2vec.html) 的过程非常直白。

**第 1 步：提取词**
```python
import sys
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize

STOP_WORDS = set(stopwords.words('english'))

def get_words(txt):
    return filter(
        lambda x: x not in STOP_WORDS, 
        re.findall(r'\b(\w+)\b', txt)
    )

def parse_sentence_words(input_file_names):
   """Returns a list of a list of words. Each sublist is a sentence."""
    sentence_words = []
    for file_name in input_file_names:
        for line in open(file_name):
            line = line.strip().lower()
            line = line.decode('unicode_escape').encode('ascii','ignore')
            sent_words = map(get_words, sent_tokenize(line))
            sent_words = filter(lambda sw: len(sw) > 1, sent_words)
            if len(sent_words) > 1:
                sentence_words += sent_words
    return sentence_words

# You would see five .txt files after unzip 'a_song_of_ice_and_fire.zip'
input_file_names = ["001ssb.txt", "002ssb.txt", "003ssb.txt", 
                    "004ssb.txt", "005ssb.txt"]
GOT_SENTENCE_WORDS= parse_sentence_words(input_file_names)
```

**第 2 步：喂给 word2vec 模型**
```python
from gensim.models import Word2Vec

# size: the dimensionality of the embedding vectors.
# window: the maximum distance between the current and predicted word within a sentence.
model = Word2Vec(GOT_SENTENCE_WORDS, size=128, window=3, min_count=5, workers=4)
model.wv.save_word2vec_format("got_word2vec.txt", binary=False)
```

**第 3 步：检查结果**

在 GoT 词嵌入空间中，与 "king" 和 "queen" 最相似的词是：

| ---------------- | --------------|
| `model.most_similar('king', topn=10)`<br/>（词，与 'king' 的相似度） | `model.most_similar('queen', topn=10)`<br/>（词，与 'queen' 的相似度） |
| ---------------- | --------------|
| ('kings', 0.897245) | ('cersei', 0.942618) |
| ('baratheon', 0.809675) | ('joffrey', 0.933756) |
| ('son', 0.763614) | ('margaery', 0.931099) |
| ('robert', 0.708522) | ('sister', 0.928902) |
| ('lords', 0.698684) | ('prince', 0.927364) |
| ('joffrey', 0.696455) | ('uncle', 0.922507) |
| ('prince', 0.695699) | ('varys', 0.918421) |
| ('brother', 0.685239) | ('ned', 0.917492) |
| ('aerys', 0.684527) | ('melisandre', 0.915403) |
| ('stannis', 0.682932) | ('robb', 0.915272) |

---
引用格式：
```
@article{weng2017wordembedding,
  title   = "Learning word embedding",
  author  = "Weng, Lilian",
  journal = "lilianweng.github.io/lil-log",
  year    = "2017",
  url     = "https://lilianweng.github.io/lil-log/2017/10/15/learning-word-embedding.html"
}
```

## 参考文献

[1] Tensorflow Tutorial [Vector Representations of Words](https://www.tensorflow.org/tutorials/word2vec).

[2] ["Word2Vec Tutorial - The Skip-Gram Model"](http://mccormickml.com/2016/04/19/word2vec-tutorial-the-skip-gram-model/) by Chris McCormick.

[3] ["On word embeddings - Part 2: Approximating the Softmax"](http://ruder.io/word-embeddings-softmax/) by Sebastian Ruder.

[4] Xin Rong. [word2vec Parameter Learning Explained](https://arxiv.org/pdf/1411.2738.pdf)

[5] Mikolov, Tomas, Kai Chen, Greg Corrado, and Jeffrey Dean. ["Efficient estimation of word representations in vector space."](https://arxiv.org/pdf/1301.3781.pdf) arXiv preprint arXiv:1301.3781 (2013).

[6] Frederic Morin and Yoshua Bengio. ["Hierarchical Probabilistic Neural Network Language Model."](https://www.iro.umontreal.ca/~lisa/pointeurs/hierarchical-nnlm-aistats05.pdf) Aistats. Vol. 5. 2005.

[7] Michael Gutmann and Aapo Hyvärinen. ["Noise-contrastive estimation: A new estimation principle for unnormalized statistical models."](http://proceedings.mlr.press/v9/gutmann10a/gutmann10a.pdf) Proc. Intl. Conf. on Artificial Intelligence and Statistics. 2010. 

[8] Tomas Mikolov, Ilya Sutskever, Kai Chen, Greg Corrado, and Jeffrey Dean. ["Distributed representations of words and phrases and their compositionality."](https://papers.nips.cc/paper/5021-distributed-representations-of-words-and-phrases-and-their-compositionality.pdf) Advances in neural information processing systems. 2013.

[9] Tomas Mikolov, Kai Chen, Greg Corrado, and Jeffrey Dean. ["Efficient estimation of word representations in vector space."](https://arxiv.org/pdf/1301.3781.pdf) arXiv preprint arXiv:1301.3781 (2013).

[10] Marco Baroni, Georgiana Dinu, and Germán Kruszewski. ["Don't count, predict! A systematic comparison of context-counting vs. context-predicting semantic vectors."](http://anthology.aclweb.org/P/P14/P14-1023.pdf) ACL (1). 2014.

[11] Jeffrey Pennington, Richard Socher, and Christopher Manning. ["Glove: Global vectors for word representation."](http://www.aclweb.org/anthology/D14-1162) Proc. Conf. on empirical methods in natural language processing (EMNLP). 2014.
