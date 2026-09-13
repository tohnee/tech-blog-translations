---
title: "深度强化学习中的探索策略"
title_en: "Exploration Strategies in Deep Reinforcement Learning"
source: https://lilianweng.github.io/posts/2020-06-07-exploration-drl/
crawled: 2026-09-08
translated: 2026-09-08
---

# 深度强化学习中的探索策略

> 原文：[Exploration Strategies in Deep Reinforcement Learning](https://lilianweng.github.io/posts/2020-06-07-exploration-drl/) · Lilian Weng（翁荔）

> 利用与探索（exploitation versus exploration）是强化学习中的一个关键话题。本文介绍了几种在深度强化学习中实现更好探索的常见方法。



<span style="color: #286ee0;">[更新于 2020-06-17：在「前向动力学」[章节](#forward-dynamics)中新增了 ["基于分歧的探索"](#exploration-via-disagreement)。</span>


[利用与探索](https://lilianweng.github.io/posts/2018-01-23-multi-armed-bandit/)是强化学习中的一个关键话题。我们希望 RL 智能体（agent）尽可能快地找到最优解；但与此同时，在没有充分探索的情况下过快地锁定某个解也相当糟糕，因为这可能导致陷入局部极小甚至彻底失败。以最优回报为优化目标的现代 [RL](https://lilianweng.github.io/posts/2018-02-19-rl-overview/) [算法](https://lilianweng.github.io/posts/2018-04-08-policy-gradient/)可以相当高效地实现良好的利用，而探索则更像是一个仍然开放的话题。

我想在这里讨论深度强化学习中的几种常见探索策略。由于这是一个非常大的主题，我这篇文章当然无法涵盖所有重要的子话题。我计划定期更新它，并随着时间推移逐步充实内容。






## 经典探索策略

<a name="classic-exploration-strategies"></a>先快速回顾一下：下面几种经典的探索算法在多臂老虎机（multi-armed bandit）问题或简单的表格型 RL（tabular RL）中效果相当不错。
- **ε-贪婪（epsilon-greedy）**：智能体以概率 $$\epsilon$$ 偶尔进行随机探索，并在大多数时候以概率 $$1-\epsilon$$ 采取最优动作。
- **置信上界（upper confidence bounds）**：智能体选择让置信上界 $$\hat{Q}_t(a) + \hat{U}_t(a)$$ 最大化的贪婪动作，其中 $$\hat{Q}_t(a)$$ 是截至时刻 $$t$$ 与动作 $$a$$ 相关的平均奖励，$$\hat{U}_t(a)$$ 是一个与动作 $$a$$ 已被执行次数成反比的函数。更多细节见[此处](https://lilianweng.github.io/posts/2018-01-23-multi-armed-bandit/#upper-confidence-bounds)。
- **玻尔兹曼探索（Boltzmann exploration）**：智能体根据学习到的 Q 值上的[玻尔兹曼分布](https://en.wikipedia.org/wiki/Boltzmann_distribution)（softmax）来抽取动作，并由温度参数 $$\tau$$ 调节。
- **Thompson 采样（Thompson sampling）**：智能体维护一个关于最优动作概率的信念（belief），并从这个分布中采样。更多细节见[此处](https://lilianweng.github.io/posts/2018-01-23-multi-armed-bandit/#thompson-sampling)。

当使用神经网络做函数逼近时，以下策略可用于在深度 RL 训练中获得更好的探索：
- **熵损失项（entropy loss term）**：在损失函数中加入熵项 $$H(\pi(a \vert s))$$，鼓励策略采取多样化的动作。
- **基于噪声的探索（noise-based exploration）**：在观测、动作甚至参数空间中加入噪声（[Fortunato, et al. 2017](https://arxiv.org/abs/1706.10295)、[Plappert, et al. 2017](https://arxiv.org/abs/1706.01905)）。



## 关键探索问题

当环境很少提供奖励作为反馈，或者环境中存在干扰性噪声时，良好的探索变得尤其困难。许多探索策略被提出来解决以下一个或两个问题。


### 困难探索问题

<a name="the-hard-exploration-problem"></a>「困难探索（hard-exploration）」问题是指在奖励非常稀疏甚至具有欺骗性的环境中进行探索。这类问题之所以困难，是因为在这种场景下，随机探索几乎不可能发现成功的状态或获得有意义的反馈。

[Montezuma's Revenge（蒙特祖马的复仇）](https://en.wikipedia.org/wiki/Montezuma%27s_Revenge_(video_game))是困难探索问题的一个具体例子。它至今仍是 Atari 中少数几个对深度强化学习（DRL）而言颇具挑战性的游戏。许多论文都用 Montezuma's Revenge 来检验其结果。


### 噪声电视问题

<a name="the-noisy-tv-problem"></a>「噪声电视（Noisy-TV）」问题最初是 [Burda, et al (2018)](https://arxiv.org/abs/1810.12894) 中的一个思想实验。想象一个以寻求新颖体验为奖励的 RL 智能体，一台输出无法控制、不可预测的随机噪声的电视就能永远吸引它的注意力。智能体可以持续从噪声电视获得新的奖励，却无法取得任何有意义的进展，最终变成一个「沙发土豆」。

![噪声电视问题](https://lilianweng.github.io/posts/2020-06-07-exploration-drl/the-noisy-TV-problem.gif)

*图 1. 实验中，智能体会因获得新颖体验而得到奖励。如果迷宫中放着一台噪声电视，智能体就会被它吸引，停止在迷宫中移动。（图片来源：[OpenAI 博客："Reinforcement Learning with Prediction-Based Rewards"](https://openai.com/blog/reinforcement-learning-with-prediction-based-rewards/)）*



## 作为探索加成的内在奖励

实现更好探索的一种常见方法——尤其是为了解决[困难探索](#the-hard-exploration-problem)问题——是在环境奖励之外附加一个额外的加成信号（bonus），以鼓励更多的探索。于是，策略训练时所用的奖励由两项组成：$$r_t = r^e_t + \beta r^i_t$$，其中 $$\beta$$ 是调节利用与探索之间平衡的超参数。
- $$r^e_t$$ 是时刻 $$t$$ 来自环境的*外在*奖励（extrinsic reward），依据手头任务定义。
- $$r^i_t$$ 是时刻 $$t$$ 的*内在*探索加成（intrinsic exploration bonus）。

这种内在奖励（intrinsic reward）在某种程度上受到了心理学中*内在动机*（intrinsic motivation）的启发（[Oudeyer & Kaplan, 2008](https://www.researchgate.net/profile/Pierre-Yves_Oudeyer/publication/29614795_How_can_we_define_intrinsic_motivation/links/09e415107f1b4c8041000000/How-can-we-define-intrinsic-motivation.pdf)）。好奇心驱动的探索可能是儿童成长与学习的重要方式。换句话说，探索性活动本身应当能在人脑中带来内在的回报，以鼓励这种行为。内在奖励可能与好奇心、惊异、状态的熟悉程度以及其他许多因素相关。

同样的思想也可以应用于 RL 算法。在接下来的小节中，基于加成的探索奖励方法被粗略地分为两类：
1. 发现新颖的状态
2. 增进智能体对环境的认知。



### 基于计数的探索

如果把内在奖励看作「奖励那些令我们惊讶的状况」，我们就需要一种方法来度量一个状态是新颖的还是频繁出现的。一种直观的方式是统计一个状态被遇到的次数，并据此分配加成。这种加成会引导智能体的行为，使其偏好很少被访问的状态而非常见状态。这就是**基于计数的探索（count-based exploration）**方法。

令 $$N_n(s)$$ 为*经验计数*（empirical count）函数，它跟踪状态 $$s$$ 在序列 $$s_{1:n}$$ 中被访问的真实次数。遗憾的是，直接用 $$N_n(s)$$ 来做探索并不现实，因为大多数状态都会有 $$N_n(s)=0$$，尤其是考虑到状态空间往往是连续的或高维的。我们需要对大多数状态都得到非零的计数，即使它们从未被见过。


#### 用密度模型计数

[Bellemare, et al. (2016)](https://arxiv.org/abs/1606.01868) 使用**密度模型（density model）**来近似状态访问的频率，并提出了一种从该密度模型中导出*伪计数（pseudo-count）*的新算法。首先在状态空间上定义一个条件概率：$$\rho_n(s) = \rho(s \vert s_{1:n})$$，表示在前 $$n$$ 个状态为 $$s_{1:n}$$ 的条件下，第 $$(n+1)$$ 个状态是 $$s$$ 的概率。要从经验上度量它，直接用 $$N_n(s)/n$$ 即可。

再定义状态 $$s$$ 的*重编码概率（recoding probability）*：即在*观察到 $$s$$ 又出现一次之后*，密度模型赋予 $$s$$ 的概率，$$\rho'_n(s) = \rho(s \vert s_{1:n}s)$$。

这篇论文引入了两个概念来更好地约束密度模型：*伪计数*函数 $$\hat{N}_n(s)$$ 与*伪计数总量* $$\hat{n}$$。由于它们被设计来模仿经验计数函数，我们会有：

$$
\rho_n(s) = \frac{\hat{N}_n(s)}{\hat{n}} \leq \rho'_n(s) = \frac{\hat{N}_n(s) + 1}{\hat{n} + 1}
$$

$$\rho_n(x)$$ 与 $$\rho'_n(x)$$ 之间的关系要求密度模型是*学习正（learning-positive）*的：对所有 $$s_{1:n} \in \mathcal{S}^n$$ 和所有 $$s \in \mathcal{S}$$，都有 $$\rho_n(s) \leq \rho'_n(s)$$。换言之，在观察到 $$s$$ 的一个实例之后，密度模型对同一个 $$s$$ 的预测应当上升。除了学习正之外，密度模型还应当完全*在线*地用经验状态的非随机化 mini-batch 来训练，于是自然有 $$\rho'_n = \rho_{n+1}$$。

求解上述线性方程组后，伪计数可以由 $$\rho_n(s)$$ 和 $$\rho'_n(s)$$ 计算出来：

$$
\hat{N}_n(s) = \hat{n} \rho_n(s) = \frac{\rho_n(s)(1 - \rho'_n(s))}{\rho'_n(s) - \rho_n(s)} 
$$

或者用*预测增益（prediction gain，PG）*来估计：

$$
\hat{N}_n(s) \approx (e^{\text{PG}_n(s)} - 1)^{-1} = (e^{\log \rho'_n(s) - \log \rho(s)} - 1)^{-1}
$$

基于计数的内在加成的一个常见选择是 $$r^i_t = N(s_t, a_t)^{-1/2}$$（如 MBIE-EB；[Strehl & Littman, 2008](https://www.ics.uci.edu/~dechter/courses/ics-295/fall-2019/papers/2008-littman-aij-main.pdf)）。基于伪计数的探索加成也采用类似的形式：$$r^i_t = \big(\hat{N}_n(s_t, a_t) + 0.01 \big)^{-1/2}$$。


[Bellemare et al., (2016)](https://arxiv.org/abs/1606.01868) 的实验采用了一个简单的 [CTS](http://proceedings.mlr.press/v32/bellemare14.html)（Context Tree Switching，上下文树切换）密度模型来估计伪计数。CTS 模型以 2D 图像为输入，依据与位置相关的 L 形滤波器的乘积为图像赋予一个概率，其中每个滤波器的预测由一个在过往图像上训练得到的 CTS 算法给出。CTS 模型简单，但在表达能力、可扩展性和数据效率上都存在局限。在后续论文中，[Georg Ostrovski, et al. (2017)](https://arxiv.org/abs/1703.01310) 改进了这一方法，训练一个 PixelCNN（[van den Oord et al., 2016](https://arxiv.org/abs/1606.05328)）作为密度模型。


密度模型也可以是高斯混合模型，如 [Zhao & Tresp (2018)](https://arxiv.org/abs/1902.08039)。他们使用变分 GMM 来估计轨迹（例如一个状态序列的拼接）的密度，并利用其预测概率在离策略（off-policy）设定下引导经验回放（experience replay）中的优先级排序。



#### 哈希后计数

另一种让高维状态可数的思想是将状态映射为**哈希码（hash code）**，从而使状态的出现变得可追踪（[Tang et al. 2017](https://arxiv.org/abs/1611.04717)）。状态空间用哈希函数 $$\phi: \mathcal{S} \mapsto \mathbb{Z}^k$$ 进行离散化。奖励函数中加入一个探索加成 $$r^{i}: \mathcal{S} \mapsto \mathbb{R}$$，定义为 $$r^{i}(s) = {N(\phi(s))}^{-1/2}$$，其中 $$N(\phi(s))$$ 是 $$\phi(s)$$ 出现次数的经验计数。


[Tang et al. (2017)](https://arxiv.org/abs/1611.04717) 提出使用*局部敏感哈希*（[*LSH*](https://en.wikipedia.org/wiki/Locality-sensitive_hashing)）将连续的高维数据转换为离散的哈希码。LSH 是一类流行的哈希函数，用于基于特定相似度度量来查询最近邻。如果一个哈希方案 $$x \mapsto h(x)$$ 能保留数据点之间的距离信息——相近的向量得到相似的哈希值，而相距遥远的向量得到的哈希值截然不同——它就是局部敏感的。（若有兴趣，可以看看 LSH 如何被用于 [Transformer 的改进](https://lilianweng.github.io/posts/2020-04-07-the-transformer-family/#LSH)。）[SimHash](https://www.cs.princeton.edu/courses/archive/spr04/cos598B/bib/CharikarEstim.pdf) 是一种计算高效的 LSH，它通过角距离来度量相似性：


$$
\phi(s) = \text{sgn}(A g(s)) \in \{-1, 1\}^k
$$

其中 $$A \in \mathbb{R}^{k \times D}$$ 是一个每个元素都从标准高斯分布中独立同分布地抽取的矩阵，$$g: \mathcal{S} \mapsto \mathbb{R}^D$$ 是一个可选的预处理函数。二进制码的维度为 $$k$$，控制着状态空间离散化的粒度。$$k$$ 越高，粒度越高，冲突也越少。


![#Exploration](https://lilianweng.github.io/posts/2020-06-07-exploration-drl/count-hashing-exploration.png)

*图 2. 通过 SimHash 对高维状态进行哈希、进而实现基于计数的探索的算法。（图片来源：[Tang et al. 2017](https://arxiv.org/abs/1611.04717)）*


对于高维图像，SimHash 在原始像素层面可能效果不好。[Tang et al. (2017)](https://arxiv.org/abs/1611.04717) 设计了一个自编码器（autoencoder，AE），以状态 $$s$$ 为输入来学习哈希码。它的中间有一个由 $$k$$ 个 sigmoid 函数组成的特殊稠密层，作为中间的潜在状态；然后该层的 sigmoid 激活值 $$b(s)$$ 通过四舍五入到最接近的二进制数 $$\lfloor b(s)\rceil \in \{0, 1\}^D$$ 进行二值化，作为状态 $$s$$ 的二进制哈希码。在 $$n$$ 个状态上的 AE 损失包含两项：

$$
\mathcal{L}(\{s_n\}_{n=1}^N) = \underbrace{-\frac{1}{N} \sum_{n=1}^N \log p(s_n)}_\text{reconstruction loss} + \underbrace{\frac{1}{N} \frac{\lambda}{K} \sum_{n=1}^N\sum_{i=1}^k \min \big \{ (1-b_i(s_n))^2, b_i(s_n)^2 \big\}}_\text{sigmoid activation being closer to binary}
$$


这种方法的一个问题是：不相似的输入 $$s_i, s_j$$ 可能被映射到相同的哈希码，但 AE 仍然能完美地重建它们。可以设想把瓶颈层 $$b(s)$$ 替换为哈希码 $$\lfloor b(s)\rceil$$，但这样一来梯度就无法通过取整函数反向传播了。注入均匀噪声可以缓解这一效应，因为 AE 必须学会将潜变量推开得足够远，以抵消噪声的影响。


### 基于预测的探索

第二类内在探索加成奖励的是智能体对环境认知的增进。智能体对环境动力学的熟悉程度可以通过一个预测模型来估计。用预测模型来度量*好奇心（curiosity）*的思想其实早在很久以前就被提出了（[Schmidhuber, 1991](http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.45.957)）。


#### 前向动力学

<a name="forward-dynamics"></a>学习**前向动力学预测模型（forward dynamics prediction model）**是近似估计我们的模型对环境和任务 MDP 已经掌握了多少知识的好方法。它刻画了智能体预测自身行为后果的能力，即 $$f: (s_t, a_t) \mapsto s_{t+1}$$。这样的模型不可能是完美的（例如由于部分可观测），其误差 $$e(s_t, a_t) = \| f(s_t, a_t) - s_{t+1} \|^2_2$$ 可以用来提供内在探索奖励。预测误差越高，说明我们对那个状态越不熟悉。误差率下降得越快，我们获得的学习进展信号就越多。

*智能自适应好奇心（Intelligent Adaptive Curiosity）*（**IAC**；[Oudeyer, et al. 2007](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.177.7661&rep=rep1&type=pdf)）勾勒出了用前向动力学预测模型来估计学习进展、并据此分配内在探索奖励的思路。

IAC 依赖一个存储机器人遇到的所有经验的记忆 $$M=\{(s_t, a_t, s_{t+1})\}$$，以及一个前向动力学模型 $$f$$。IAC 基于转移样本，以一种类似于决策树分裂的过程，将状态空间（即论文所讨论的机器人学语境下的感觉运动空间）增量地划分为若干独立区域：当样本数量超过某个阈值时发生分裂，且每个叶子节点中状态的方差应尽可能小。每个树节点由其独有的一组样本来刻画，并拥有自己的前向动力学预测器 $$f$$，称为「专家（expert）」。


专家的预测误差 $$e_t$$ 会被存入与每个区域关联的一个列表中。*学习进展（learning progress）*被度量为一个带偏移 $$\tau$$ 的滑动窗口的平均误差率与当前滑动窗口的平均误差率之差。内在奖励的定义就是为了跟踪学习进展：$$r^i_t = \frac{1}{k}\sum_{i=0}^{k-1}(e_{t-i-\tau} - e_{t-i})$$，其中 $$k$$ 是滑动窗口的大小。因此，预测误差率的降幅越大，我们分配给智能体的内在奖励就越高。换句话说，智能体被鼓励采取能够快速了解环境的行动。


![IAC](https://lilianweng.github.io/posts/2020-06-07-exploration-drl/IAC.png)

*图 3. IAC（智能自适应好奇心）模块的架构：内在奖励依据降低动力学模型预测误差所带来的学习进展来分配。（图片来源：[Oudeyer, et al. 2007](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.177.7661&rep=rep1&type=pdf)）*



[Stadie et al. (2015)](https://arxiv.org/abs/1507.00814) 在由 $$\phi$$ 定义的编码空间中训练前向动力学模型：$$f_\phi: (\phi(s_t), a_t) \mapsto \phi(s_{t+1})$$。模型在时刻 $$T$$ 的预测误差会按截至时刻 $$t$$ 的最大误差归一化，即 $$\bar{e}_t = \frac{e_t}{\max_{i \leq t} e_i}$$，使其始终介于 0 和 1 之间。内在奖励相应地定义为：$$r^i_t = (\frac{\bar{e}_t(s_t, a_t)}{t \cdot C})$$，其中 $$C > 0$$ 是一个衰减常数。

通过 $$\phi(.)$$ 对状态空间进行编码是必要的，因为论文中的实验表明，直接在原始像素上训练的动力学模型行为*非常糟糕*——会给所有状态分配相同的探索加成。在 [Stadie et al. (2015)](https://arxiv.org/abs/1507.00814) 中，编码函数 $$\phi$$ 通过自编码器（AE）学习，$$\phi(.)$$ 是 AE 的其中一个输出层。AE 可以用随机智能体收集到的一组图像静态地训练，也可以与策略一起动态地训练，其中早期帧通过 [$$\epsilon$$-贪婪](#classic-exploration-strategies)探索收集。

<a name="ICM"></a>*内在好奇心模块（Intrinsic Curiosity Module）*（**ICM**；[Pathak, et al., 2017](https://arxiv.org/abs/1705.05363)）没有使用自编码器，而是用一个自监督的**逆向动力学（inverse dynamics）**模型来学习状态空间编码 $$\phi(.)$$。给定智能体自身的动作去预测下一个状态并不容易，尤其是考虑到环境中有些因素既无法被智能体控制，也不影响智能体。ICM 认为，一个好的状态特征空间应当排除这些因素，因为*它们无法影响智能体的行为，因而智能体没有动机去学习它们*。通过学习逆向动力学模型 $$g: (\phi(s_t), \phi(s_{t+1})) \mapsto a_t$$，特征空间只会捕捉环境中与我们的智能体动作相关的变化，而忽略其余部分。

给定一个前向模型 $$f$$、一个逆向动力学模型 $$g$$ 以及一次观测 $$(s_t, a_t, s_{t+1})$$：


$$
g_{\psi_I}(\phi(s_t), \phi(s_{t+1})) = \hat{a}_t \quad
f_{\psi_F}(\phi(s_t), a_t) = \hat{\phi}(s_{t+1}) \quad
r_t^i = \| \hat{\phi}(s_{t+1}) - \phi(s_{t+1}) \|_2^2
$$

这样的 $$\phi(.)$$ 有望对环境中不可控的方面保持鲁棒。



![ICM](https://lilianweng.github.io/posts/2020-06-07-exploration-drl/ICM.png)

*图 4. ICM（内在好奇心模块）将前向动力学预测误差作为内在奖励分配给智能体。该动力学模型运行在一个通过逆向动力学模型学到的状态编码空间中，以排除不影响智能体行为的环境因素。（图片来源：[Pathak, et al. 2017](https://arxiv.org/abs/1705.05363)）*



[Burda, Edwards & Pathak, et al. (2018)](https://arxiv.org/abs/1808.04355) 就纯粹好奇心驱动的学习做了一系列大规模对比实验，也就是说，只向智能体提供内在奖励。在这项研究中，奖励为 $$r_t = r^i_t = \| f(s_t, a_t) - \phi(s_{t+1})\|_2^2$$。$$\phi$$ 的良好选择对学习前向动力学至关重要，它应当*紧凑*、*充分*且*稳定*，从而使预测任务更易处理，并过滤掉无关的观测。

他们比较了 4 种编码函数：
1. 原始图像像素：不做编码，$$\phi(x) = x$$。
2. <a name="random-feature"></a>随机特征（random features，RF）：每个状态经过一个固定的随机神经网络压缩。
3. [VAE](https://lilianweng.github.io/posts/2018-08-12-vae/#vae-variational-autoencoder)：使用概率编码器进行编码，$$\phi(x) = q(z \vert x)$$。
4. 逆向动力学特征（inverse dynamic features，IDF）：与 [ICM](#ICM) 中使用的特征空间相同。

所有实验都将奖励信号除以累积回报标准差的滚动估计以进行归一化。并且所有实验都在无限时域（infinite horizon）设定下运行，以避免「done」标志泄露信息。


![大规模好奇心学习](https://lilianweng.github.io/posts/2020-06-07-exploration-drl/large-scale-curiosity-learning.png)

*图 5. 仅使用好奇心信号训练时，不同状态编码函数在不同游戏中得到的平均奖励。
（图片来源：[Burda, Edwards & Pathak, et al. 2018](https://arxiv.org/abs/1808.04355)）*


有趣的是，*随机特征*的结果相当有竞争力；但在特征迁移实验中（即在《超级马力欧兄弟》1-1 关训练智能体、再到另一关测试），学习得到的 IDF 特征能更好地泛化。

他们还在开着[噪声电视](#the-noisy-tv-problem)的环境中比较了 RF 和 IDF。不出所料，噪声电视大幅拖慢了学习速度，外在奖励也一直明显更低。

![噪声电视实验](https://lilianweng.github.io/posts/2020-06-07-exploration-drl/noisy-TV-experiment.png)

*图 6. 在噪声电视开与关的环境中，使用 RF 与 IDF 特征编码的实验。曲线跟踪了训练过程中每个 episode 的外在奖励。（图片来源：[Burda, Edwards & Pathak, et al. 2018](https://arxiv.org/abs/1808.04355)）*



前向动力学的优化也可以通过变分推断来建模。**VIME**（*"Variational information maximizing exploration"* 的简称；[Houthooft, et al. 2017](https://arxiv.org/abs/1605.09674)）是一种探索策略，基于最大化智能体对环境动力学信念的*信息增益（information gain）*。关于前向动力学获得了多少额外信息，可以用熵的减少量来度量。

令 $$\mathcal{P}$$ 为环境转移函数，$$p(s_{t+1}\vert s_t, a_t; \theta)$$ 为由 $$\theta \in \Theta$$ 参数化的前向预测模型，$$\xi_t = \{s_1, a_1, \dots, s_t\}$$ 为轨迹历史。我们希望在采取一个新动作并观测到下一个状态之后降低熵，也就是最大化下式：


$$
\begin{aligned}
&\sum_t H(\Theta \vert \xi_t, a_t) - H(\Theta \vert S_{t+1}, \xi_t, a_t) \\
=& I(\Theta; S_{t+1} \vert \xi_t, a_t) \quad \scriptstyle{\text{; because } I(X; Y) = I(X) - I(X \vert Y)} \\
=& \mathbb{E}_{s_{t+1} \sim \mathcal{P}(.\vert\xi_t,a_t)} [D_\text{KL}(p(\theta \vert \xi_t, a_t, s_{t+1}) \| p(\theta \vert \xi_t, a_t))] \quad \scriptstyle{\text{; because } I(X; Y) = \mathbb{E}_Y [D_\text{KL} (p_{X \vert Y} \| p_X)]} \\
=& \mathbb{E}_{s_{t+1} \sim \mathcal{P}(.\vert\xi_t,a_t)} [D_\text{KL}(p(\theta \vert \xi_t, a_t, s_{t+1}) \| p(\theta \vert \xi_t))] \quad \scriptstyle{\text{; because } \theta \text{ does not depend on } a_t}
\end{aligned}
$$

在对新的可能状态取期望时，智能体应当采取新的动作来增大其预测模型的新信念与旧信念之间的 KL 散度（*「信息增益」*）。这一项可以作为内在奖励加入奖励函数：$$r^i_t = D_\text{KL} [p(\theta \vert \xi_t, a_t, s_{t+1}) \| p(\theta \vert \xi_t))]$$。


然而，计算后验（posterior）$$p(\theta \vert \xi_t, a_t, s_{t+1})$$ 通常是不可行的。

$$
\begin{aligned}
p(\theta \vert \xi_t, a_t, s_{t+1}) 
&= \frac{p(\theta \vert \xi_t, a_t) p(s_{t+1} \vert \xi_t, a_t; \theta)}{p(s_{t+1}\vert\xi_t, a_t)} \\
&= \frac{p(\theta \vert \xi_t) p(s_{t+1} \vert \xi_t, a_t; \theta)}{p(s_{t+1}\vert\xi_t, a_t)} & \scriptstyle{\text{; because action doesn't affect the belief.}} \\
&= \frac{\color{red}{p(\theta \vert \xi_t)} p(s_{t+1} \vert \xi_t, a_t; \theta)}{\int_\Theta p(s_{t+1}\vert\xi_t, a_t; \theta) \color{red}{p(\theta \vert \xi_t)} d\theta} & \scriptstyle{\text{; red part is hard to compute directly.}}
\end{aligned}
$$

由于直接计算 $$p(\theta\vert\xi_t)$$ 很困难，一个自然的选择是用另一个分布 $$q_\phi(\theta)$$ 来近似它。根据变分下界，我们知道对 $$q_\phi(\theta)$$ 的最大化等价于最大化 $$p(\xi_t\vert\theta)$$ 并最小化 $$D_\text{KL}[q_\phi(\theta) \| p(\theta)]$$。

使用近似分布 $$q$$ 之后，内在奖励变为：

$$
r^i_t = D_\text{KL} [q_{\phi_{t+1}}(\theta) \| q_{\phi_t}(\theta))]
$$

其中 $$\phi_{t+1}$$ 表示在看到 $$a_t$$ 和 $$s_{t+1}$$ 之后、与更新后的信念相关联的 $$q$$ 的参数。当用作探索加成时，它会通过除以该 KL 散度值的滑动中位数来进行归一化。

这里，动力学模型被参数化为一个[贝叶斯神经网络](https://link.springer.com/book/10.1007/978-1-4612-0745-0)（BNN），因为它在其权重上维护一个分布。BNN 的权重分布 $$q_\phi(\theta)$$ 被建模为完全*因子分解*的高斯分布，参数为 $$\phi = \{\mu, \sigma\}$$，于是我们可以很容易地采样 $$\theta \sim q_\phi(.)$$。在应用二阶泰勒展开之后，KL 项 $$D_\text{KL}[q_{\phi + \lambda \Delta\phi}(\theta) \| q_{\phi}(\theta)]$$ 可以用 [Fisher 信息矩阵](https://lilianweng.github.io/posts/2019-09-05-evolution-strategies/#estimation-using-fisher-information-matrix) $$\mathbf{F}_\phi$$ 来估计；由于 $$q_\phi$$ 是因子分解的高斯分布，协方差矩阵只是一个对角矩阵，因此该矩阵易于计算。更多细节请参见[论文](https://arxiv.org/abs/1605.09674)，尤其是第 2.3–2.5 节。


<a name="exploration-via-disagreement"></a>上述方法都依赖单一的预测模型。如果我们有多个这样的模型，就可以利用模型之间的分歧（disagreement）来设定探索加成（[Pathak, et al. 2019](https://arxiv.org/abs/1906.04161)）。分歧大意味着预测的置信度低，因而需要更多探索。[Pathak, et al. (2019)](https://arxiv.org/abs/1906.04161) 提出训练一组前向动力学模型，并使用模型集成（ensemble）输出的方差作为 $$r_t^i$$。确切地说，他们用[随机特征](#random-feature)编码状态空间，并在集成中学习 5 个模型。


![分歧](https://lilianweng.github.io/posts/2020-06-07-exploration-drl/exploration-via-disagreement.png)

*图 7. 通过分歧进行自监督探索的训练架构示意图。（图片来源：[Pathak, et al. 2019](https://arxiv.org/abs/1906.04161)）*


由于 $$r^i_t$$ 是可微的，模型中的内在奖励可以直接通过梯度下降来优化，从而告知策略智能体去改变动作。这种可微探索方法非常高效，但受限于较短的探索时域。



#### 随机网络

可是，如果预测任务压根与环境动力学无关呢？结果表明，当预测面向的是一个随机任务时，它依然能够帮助探索。

**DORA**（*"Directed Outreaching Reinforcement Action-Selection"* 的简称；[Fox & Choshen, et al. 2018](https://arxiv.org/abs/1804.04012)）是一个新颖的框架，它基于一个新引入的、**与任务无关**的 MDP 来注入探索信号。DORA 的思想依赖两个并行的 MDP：
- 一个是原始的任务 MDP；
- 另一个是完全相同的 MDP，但*不附带任何奖励*：相反，每个状态-动作对都被设计为具有价值 0。为第二个 MDP 学习到的 Q 值称为 *E 值（E-value）*。如果模型无法完美地预测出 E 值为零，说明它仍然缺少信息。

E 值最初被赋值为 1。这种正的初始化可以鼓励定向探索（directed exploration），以获得更好的 E 值预测。E 值估计很高的状态-动作对意味着尚未收集到足够的信息——至少不足以排除其高 E 值。在某种程度上，E 值的对数可以被视为*访问计数器（visit counter）*的一种泛化。

当使用神经网络为 E 值做函数逼近时，会额外添加一个价值头来预测 E 值，并且它被期望直接预测为零。给定预测的 E 值 $$E(s_t, a_t)$$，探索加成为 $$r^i_t = \frac{1}{\sqrt{-\log E(s_t, a_t)}}$$。



<a name="RND"></a>与 DORA 类似，**随机网络蒸馏（Random Network Distillation）**（**RND**；[Burda, et al. 2018](https://arxiv.org/abs/1810.12894)）引入了一个*与主任务无关*的预测任务。RND 探索加成定义为一个神经网络 $$\hat{f}(s_t)$$ 在预测一个*固定随机初始化*的神经网络 $$f(s_t)$$ 所给出的观测特征时的误差。其动机是：给定一个新状态，如果相似的状态在过去已被访问过很多次，预测就应该更容易，误差也就更低。探索加成为 $$r^i(s_t) = \|\hat{f}(s_t; \theta) - f(s_t) \|_2^2$$。


![RND](https://lilianweng.github.io/posts/2020-06-07-exploration-drl/RND.png)

*图 8. RND（随机网络蒸馏）如何提供内在奖励。特征 $$O_{i+1} \mapsto f_{i+1}$$ 由一个固定的随机神经网络生成。（图片来源：[OpenAI 博客："Reinforcement Learning with Prediction-Based Rewards"](https://openai.com/blog/reinforcement-learning-with-prediction-based-rewards/)）*


在 RND 实验中，有两个因素很重要：
1. 非情景（non-episodic）设定会带来更好的探索，尤其是在不使用任何外在奖励时。这意味着回报不会在「游戏结束」处被截断，内在回报可以跨多个 episode 传播。
2. 归一化很重要，因为给定一个随机神经网络作为预测目标，奖励的尺度很难调节。内在奖励通过除以内在回报标准差的滚动估计来归一化。


RND 的设置在解决困难探索问题方面效果很好。例如，最大化 RND 探索加成能够持续找到 Montezuma's Revenge 中一半以上的房间。



#### 物理属性

与模拟器中的游戏不同，机器人学等一些 RL 应用需要理解物理世界中的物体并进行直觉推理。有些预测任务要求智能体与环境进行一系列交互并观察相应的后果，例如估计物理学中的某些隐含属性（如质量、摩擦力等）。

在这些想法的启发下，[Denil, et al. (2017)](https://arxiv.org/abs/1611.01843) 发现深度强化学习智能体可以学会执行必要的探索来发现这些隐含属性。确切地说，他们考虑了两个实验：
1. *「哪个更重？」*——智能体必须与方块交互，推断哪一个更重。
2. *「塔」*——智能体需要通过推倒一座塔来推断它由多少个刚体组成。

实验中的智能体首先经历一个探索阶段，与环境交互并收集信息。探索阶段结束后，智能体被要求输出一个*作答（labeling）*动作来回答问题。如果回答正确，智能体会获得一个正奖励；否则获得一个负奖励。由于回答问题需要与场景中的物品进行相当多的交互，智能体必须学会高效地摆弄它们，从而弄清物理规律和正确答案。探索就这样自然而然地发生了。

在他们的实验中，智能体在两个任务上都能够学习，表现随任务难度而变化。尽管这篇论文并没有把物理预测任务用来提供内在奖励加成、并与另一个学习任务的外在奖励相结合，而是专注于探索任务本身，我确实很喜欢通过预测环境中的隐含物理属性来鼓励复杂探索行为的想法。



## 基于记忆的探索

基于奖励的探索存在几个缺点：
- 函数逼近的跟进速度较慢。
- 探索加成是非平稳的。
- 知识消退（knowledge fading），即状态不再新颖，无法及时提供内在奖励信号。

本节中的方法依赖外部记忆来解决基于奖励加成的探索的这些缺点。



### 情景记忆

如前所述，[RND](#RND) 更适合在非情景设定下运行，即预测知识跨多个 episode 累积。探索策略 **Never Give Up**（永不放弃；**NGU**；[Badia, et al. 2020a](https://arxiv.org/abs/2002.06038)）将一个能在单个 episode 内快速适应的情景新颖性模块，与作为终身新颖性模块的 RND 结合了起来。

确切地说，NGU 的内在奖励由来自两个模块的两部分探索加成组成，分别作用于*单个 episode 之内*与*多个 episode 之间*。

短期的单 episode 奖励由*情景新颖性模块（episodic novelty module）*提供。它包含一个情景记忆 $$M$$（一个尺寸动态变化的槽位式记忆），以及一个与 [ICM](#ICM) 中特征编码相同的 IDF（逆向动力学特征）嵌入函数 $$\phi$$：
1. 每一步都将当前状态嵌入 $$\phi(s_t)$$ 加入 $$M$$。
2. 通过比较当前观测与 $$M$$ 中内容的相似程度来确定内在加成。差异越大，加成越大。
<br/>
$$
r^\text{episodic}_t \approx \frac{1}{\sqrt{\sum_{\phi_i \in N_k} K(\phi(x_t), \phi_i)} + c}
$$
<br/>
其中 $$K(x, y)$$ 是度量两个样本之间距离的核函数。$$N_k$$ 是 $$M$$ 中依据 $$K(., .)$$ 得到的 $$k$$ 个最近邻组成的集合。$$c$$ 是一个保持分母非零的小常数。在论文中，$$K(x, y)$$ 被配置为逆核（inverse kernel）：
<br/>
$$
K(x, y) = \frac{\epsilon}{\frac{d^2(x, y)}{d^2_m} + \epsilon}
$$
<br/>
其中 $$d(.,.)$$ 是两个样本之间的欧氏距离，$$d_m$$ 是第 k 个最近邻的欧氏距离平方的滚动平均值，用于提高鲁棒性。$$\epsilon$$ 是一个小常数。


![RND](https://lilianweng.github.io/posts/2020-06-07-exploration-drl/NGU.png)

*图 9. NGU 的嵌入函数（左）与奖励生成器（右）的架构。（图片来源：[Badia, et al. 2020a](https://arxiv.org/abs/2002.06038)）*


长期的跨 episode 新颖性依赖于*终身新颖性模块（life-long novelty module）*中的 RND 预测误差。探索加成为 $$\alpha_t = 1 + \frac{e^\text{RND}(s_t) - \mu_e}{\sigma_e}$$，其中 $$\mu_e$$ 和 $$\sigma_e$$ 分别是 RND 误差 $$e^\text{RND}(s_t)$$ 的滚动均值和标准差。

> 不过，我注意到 [RND 论文](https://arxiv.org/abs/1810.12894)的结论部分有这样一段话：
>
> 「我们发现，RND 探索加成足以应对局部探索，即探索短期决策的后果，比如是否与某个特定物体交互、还是避开它。然而，涉及长时间尺度上协调决策的全局探索，超出了我们方法的能力范围。」
>
> 这让我有点困惑：RND 怎么能作为一个好的终身新颖性加成提供者呢？如果你知道原因，欢迎在下面留言。


最终组合得到的内在奖励为 $$r^i_t = r^\text{episodic}_t \cdot \text{clip}(\alpha_t, 1, L)$$，其中 $$L$$ 是一个常数形式的奖励最大标量。

NGU 的设计使其具有两个不错的性质：
1. *快速地抑制*在同一 episode *之内*重访同一状态；
2. *缓慢地抑制*重访那些跨 episode 已被访问过很多次的状态。
 
后来，DeepMind 在 NGU 的基础上提出了「Agent57」（[Badia, et al. 2020b](https://arxiv.org/abs/2003.13350)），这是第一个在*全部* 57 个 Atari 游戏上都超越标准人类基准的深度 RL 智能体。Agent57 相对 NGU 的两大主要改进是：
1. Agent57 训练了一个策略*种群（population）*，其中每个策略都配备不同的探索参数对 $$\{(\beta_j, \gamma_j)\}_{j=1}^N$$。回忆一下，给定 $$\beta_j$$，奖励构造为 $$r_{j,t} = r_t^e + \beta_j r^i_t$$，而 $$\gamma_j$$ 是奖励折扣因子。自然可以预期：$$\beta_j$$ 较高、$$\gamma_j$$ 较低的策略会在训练早期取得更大进展，而随着训练推进，预期则相反。一个元控制器（[滑动窗口 UCB 老虎机算法](https://arxiv.org/pdf/0805.3415.pdf)）被训练用来选择优先训练哪些策略。
2. 第二个改进是 Q 值函数的一种新参数化，它以与组合奖励类似的形式分解内在奖励与外在奖励的贡献：$$Q(s, a; \theta_j) = Q(s, a; \theta_j^e) + \beta_j Q(s, a; \theta_j^i)$$。训练期间，$$Q(s, a; \theta_j^e)$$ 和 $$Q(s, a; \theta_j^i)$$ 分别用奖励 $$r_j^e$$ 和 $$r_j^i$$ 独立优化。

![Agent57](https://lilianweng.github.io/posts/2020-06-07-exploration-drl/agent57.png)

*图 10. 一张相当酷的插画，展示了自 2015 年 DQN 以来随时间发展、最终通往 Agent57 的各项技术。（图片来源：[DeepMind 博客："Agent57: Outperforming the human Atari benchmark"](https://deepmind.com/blog/article/Agent57-Outperforming-the-human-Atari-benchmark)）*



[Savinov, et al. (2019)](https://arxiv.org/abs/1810.02274) 没有使用欧氏距离来度量情景记忆中状态的接近程度，而是将状态之间的转移纳入考虑，提出了一种度量从记忆中的其他状态到达某个状态所需步数的方法，称为**情景好奇心（Episodic Curiosity，EC）**模块。其新颖性加成取决于状态之间的可达性（reachability）。

1. 在每个 episode 开始时，智能体从一个空的情景记忆 $$M$$ 出发。
2. 每一步，智能体将当前状态与记忆中已保存的状态进行比较，以确定新颖性加成：如果当前状态是新颖的（即从记忆中的观测到达它所需的步数多于某个阈值），智能体就会获得加成。
3. 如果新颖性加成足够高，当前状态就会被加入情景记忆。（可以想象，如果所有状态都被加入记忆，那么任何新状态都能在 1 步之内被到达。）
4. 重复步骤 1–3，直到该 episode 结束。
 

![转移图](https://lilianweng.github.io/posts/2020-06-07-exploration-drl/transition-graph.png)

*图 11. 图中的节点是状态，边是可能的转移。蓝色节点是记忆中的状态。绿色节点可以在 $$k = 2$$ 步内从记忆到达（不新颖）。橙色节点距离更远，因此被视为新颖状态。（图片来源：[Savinov, et al. 2019](https://arxiv.org/abs/1810.02274)）*


为了估计状态之间的可达性，我们需要访问转移图，但遗憾的是转移图并不完全已知。因此，[Savinov, et al. (2019)](https://arxiv.org/abs/1810.02274) 训练了一个[孪生](https://lilianweng.github.io/posts/2018-11-30-meta-learning/#convolutional-siamese-neural-network)神经网络来预测两个状态之间相隔多少步。它包含一个嵌入网络 $$\phi: \mathcal{S} \mapsto \mathbb{R}^n$$，先将状态编码为特征向量；再包含一个比较器网络 $$C: \mathbb{R}^n \times \mathbb{R}^n \mapsto [0, 1]$$，输出一个关于两个状态在转移图中是否足够接近（即可以在 $$k$$ 步内到达）的二分类标签，即 $$C(\phi(s_i), \phi(s_j)) \mapsto [0, 1]$$。

一个情景记忆缓冲区 $$M$$ 存储同一 episode 内过去一些观测的嵌入。新观测会通过 $$C$$ 与已有的状态嵌入进行比较，结果被聚合（如取最大值、第 90 百分位数）以给出可达性分数 $$C^M(\phi(s_t))$$。探索加成为 $$r^i_t = \big(C' - C^M(f(s_t))\big)$$，其中 $$C'$$ 是决定奖励符号的预定义阈值（例如，对于固定时长的 episode，$$C'=0.5$$ 效果很好）。当新状态不容易从记忆缓冲区中的状态到达时，会被赋予较高的加成。

他们声称 EC 模块能够克服[噪声电视](#the-noisy-tv-problem)问题。


![EC 模块](https://lilianweng.github.io/posts/2020-06-07-exploration-drl/episodic-memory-overview.png)

*图 12. 用于生成内在奖励的情景好奇心（EC）模块的架构。（图片来源：[Savinov, et al. 2019](https://arxiv.org/abs/1810.02274)）*




### 直接探索

**Go-Explore**（[Ecoffet, et al., 2019](https://arxiv.org/abs/1901.10995)）是一个旨在解决「困难探索」问题的算法。它由以下两个阶段组成。

**阶段 1（「探索直至解决」）** 感觉很像在图中寻找最短路径的 [Dijkstra 算法](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)。实际上，阶段 1 完全不涉及神经网络。通过维护一个存储有趣状态以及通往这些状态的轨迹的记忆，智能体可以（在模拟器是*确定性的*前提下）回到有前景的状态，并从那里继续做*随机*探索。为了便于记忆，状态会被映射成一个简短的离散化编码（称为「单元（cell）」）。当出现新状态或找到更好/更短的轨迹时，记忆会被更新。在选择返回哪个过去的状态时，智能体可以在记忆中均匀地选择，也可以依据诸如最近性、访问次数、记忆中邻居数量等启发式规则来选择。这个过程不断重复，直到任务被解决且至少找到一条求解轨迹。

上面找到的高性能轨迹在任何带有随机性的评估环境中都无法很好地工作。因此需要**阶段 2（「鲁棒化」）**，通过模仿学习来使解变得鲁棒。他们采用了[反向算法（Backward Algorithm）](https://arxiv.org/abs/1812.03381)：让智能体从轨迹中最后一个状态附近开始，然后从那里运行 RL 优化。

关于阶段 1，一个重要提示是：为了不经探索地确定性地回到某个状态，Go-Explore 依赖于一个可重置且确定性的模拟器，这是一个很大的缺点。

为了让该算法对带有随机性的环境更具普适性，后来提出了 Go-Explore 的增强版本（[Ecoffet, et al., 2020](https://arxiv.org/abs/2004.12919)），称为**基于策略的 Go-Explore（policy-based Go-Explore）**。
- 基于策略的 Go-Explore 不再是轻松地重置模拟器状态，而是学习一个*目标条件策略（goal-conditioned policy）*，并用它来反复访问记忆中的已知状态。目标条件策略被训练来沿着此前通往记忆中所选状态的最佳轨迹行进。他们还加入了**自模仿学习（Self-Imitation Learning，SIL）**（[Oh, et al. 2018](https://arxiv.org/abs/1806.05635)）损失，以帮助从成功轨迹中尽可能多地提取信息。
- 此外，他们发现当智能体回到有前景的状态继续探索时，从策略中采样比随机动作效果更好。
- 基于策略的 Go-Explore 的另一项改进是让图像到单元的降尺度函数可调节。它会被优化，以使记忆中的单元既不过多也不过少。


![基于策略的 Go-Explore](https://lilianweng.github.io/posts/2020-06-07-exploration-drl/policy-based-Go-Explore.png)

*图 13. Go-Explore 算法概览。（图片来源：[Ecoffet, et al., 2020](https://arxiv.org/abs/2004.12919)）*


在朴素版 Go-Explore 之后，[Yijie Guo, et al. (2019)](https://arxiv.org/abs/1907.10247) 提出了 **DTSIL**（多样化轨迹条件自模仿学习，Diverse Trajectory-conditioned Self-Imitation Learning），其思想与上面基于策略的 Go-Explore 类似。DTSIL 维护一个训练期间收集的多样化演示（demonstrations）的记忆，并通过 [SIL](https://arxiv.org/abs/1806.05635) 用它们来训练一个轨迹条件策略。他们在采样时会优先选择以罕见状态结尾的轨迹。

![DTSIL](https://lilianweng.github.io/posts/2020-06-07-exploration-drl/DTSIL-algo.png)

*图 14. DTSIL（多样化轨迹条件自模仿学习）的算法。（图片来源：[Yijie Guo, et al. 2019](https://arxiv.org/abs/1907.10247)）*


类似的方法也见于 [Guo, et al. (2019)](https://arxiv.org/abs/1906.07805)。其核心思想是将*高不确定性*的目标存入记忆，以便之后智能体可以用目标条件策略反复重访这些目标状态。在每个 episode 中，智能体抛硬币（概率 0.5）来决定是相对策略贪婪地行动，还是通过从记忆中采样目标来进行定向探索。

![定向探索](https://lilianweng.github.io/posts/2020-06-07-exploration-drl/directed-exploration.png)

*图 15. 使用函数逼近进行定向探索时的各个组件。（图片来源：[Guo, et al. 2019](https://arxiv.org/abs/1906.07805)）*


状态的不确定性度量可以很简单，比如基于计数的加成；也可以很复杂，比如密度模型或贝叶斯模型。该论文训练了一个前向动力学模型，并将其预测误差作为不确定性度量.




## Q 值探索

受 [Thompson 采样](https://lilianweng.github.io/posts/2018-01-23-multi-armed-bandit/#thompson-sampling)的启发，**Bootstrapped DQN**（[Osband, et al. 2016](https://arxiv.org/abs/1602.04621)）通过[自助法（bootstrapping）](https://en.wikipedia.org/wiki/Bootstrapping_(statistics))在经典 [DQN](https://lilianweng.github.io/posts/2018-02-19-rl-overview/#deep-q-network) 的 Q 值逼近中引入了不确定性的概念。自助法是指从同一总体中多次有放回地采样，然后聚合结果，以此来近似一个分布。

多个 Q 值头被并行训练，但每个头只使用一份经自助法子采样的数据，并且各自拥有对应的目标网络。所有 Q 值头共享同一个骨干网络。

![Bootstrapped DQN](https://lilianweng.github.io/posts/2020-06-07-exploration-drl/bootstrapped-DQN-algo.png)

*图 16. Bootstrapped DQN 的算法。（图片来源：[Osband, et al. 2016](https://arxiv.org/abs/1602.04621)）*


在一个 episode 开始时，均匀随机采样一个 Q 值头，由它在该 episode 中行动并收集经验数据。然后从掩码分布 $$m \sim \mathcal{M}$$ 中采样一个二值掩码，决定哪些头可以使用这份数据进行训练。掩码分布 $$\mathcal{M}$$ 的选择决定了自助样本如何生成；例如：
- 如果 $$\mathcal{M}$$ 是参数 $$p=0.5$$ 的独立伯努利分布，就对应「非全即无」自助法（double-or-nothing bootstrap）。
- 如果 $$\mathcal{M}$$ 始终返回全 1 掩码，该算法就退化为一种集成方法。


然而，这类探索仍然受限，因为自助法引入的不确定性完全依赖于训练数据。最好注入一些独立于数据的先验信息。这种「噪声」先验有望在奖励稀疏时驱动智能体持续探索。向 Bootstrapped DQN 中加入随机先验以实现更好探索的算法（[Osband, et al. 2018](https://arxiv.org/abs/1806.03335)）依赖于贝叶斯线性回归。贝叶斯回归的核心思想是：我们可以*「在数据的噪声版本上训练，并辅以某种随机正则化，从而生成后验样本」*。

令 $$\theta$$ 为 Q 函数的参数、$$\theta^-$$ 为目标 Q 的参数，使用随机先验函数 $$p$$ 的损失函数为：

$$
\mathcal{L}(\theta, \theta^{-}, p, \mathcal{D}; \gamma) = \sum_{t\in\mathcal{D}}\Big( r_t + \gamma \max_{a'\in\mathcal{A}} (\underbrace{Q_{\theta^-} + p)}_\text{target Q}(s'_t, a') - \underbrace{(Q_\theta + p)}_\text{Q to optimize}(s_t, a_t) \Big)^2
$$




## 变分选项

选项（option）是带有终止条件的策略。搜索空间中有大量可用的选项，且它们独立于智能体的意图。通过在建模中显式地引入内在选项，智能体可以获得用于探索的内在奖励。

**VIC**（*"Variational Intrinsic Control"* 的简称；[Gregor, et al. 2017](https://arxiv.org/abs/1611.07507)）就是这样一种框架：通过建模选项并学习以选项为条件的策略，为智能体提供内在探索加成。令 $$\Omega$$ 表示一个从 $$s_0$$ 开始、在 $$s_f$$ 结束的选项。环境概率分布 $$p^J(s_f \vert s_0, \Omega)$$ 定义了给定起始状态 $$s_0$$ 时选项 $$\Omega$$ 在何处终止。可控性分布 $$p^C(\Omega \vert s_0)$$ 定义了我们可以从中采样的选项的概率分布。根据定义，有 $$p(s_f, \Omega \vert s_0) = p^J(s_f \vert s_0, \Omega) p^C(\Omega \vert s_0)$$。

在选择选项时，我们希望达成两个目标：
- 从 $$s_0$$ 出发到达多样化的终止状态集合 ⇨ 最大化 $$H(s_f \vert s_0)$$。
- 精确知道给定选项 $$\Omega$$ 会以哪个状态结束 ⇨ 最小化 $$H(s_f \vert s_0, \Omega)$$。

将两者结合起来，我们得到要最大化的互信息 $$I(\Omega; s_f \vert s_0)$$：

$$
\begin{aligned}
I(\Omega; s_f \vert s_0)
&= H(s_f \vert s_0) - H(s_f \vert s_0, \Omega) \\
&= - \sum_{s_f} p(s_f \vert s_0) \log p(s_f \vert s_0) + \sum_{s_f, \Omega} p(s_f, \Omega \vert s_0) \log \frac{p(s_f, \Omega \vert s_0)}{p^C(\Omega \vert s_0)} \\
&= - \sum_{s_f} p(s_f \vert s_0) \log p(s_f \vert s_0) + \sum_{s_f, \Omega} p^J(s_f \vert s_0, \Omega) p^C(\Omega \vert s_0) \log p^J(s_f \vert s_0, \Omega) \\
\end{aligned}
$$

由于互信息是对称的，我们可以在若干位置交换 $$s_f$$ 与 $$\Omega$$ 而不破坏等价性。又因为 $$p(\Omega \vert s_0, s_f)$$ 难以观测，我们用一个近似分布 $$q$$ 来代替它。根据变分下界，我们有 $$I(\Omega; s_f \vert s_0) \geq I^{VB}(\Omega; s_f \vert s_0)$$。

$$
\begin{aligned}
I(\Omega; s_f \vert s_0)
&= I(s_f; \Omega \vert s_0) \\
&= - \sum_{\Omega} p(\Omega \vert s_0) \log p(\Omega \vert s_0) + \sum_{s_f, \Omega} p^J(s_f \vert s_0, \Omega) p^C(\Omega \vert s_0) \log \color{red}{p(\Omega \vert s_0, s_f)}\\
I^{VB}(\Omega; s_f \vert s_0)
&= - \sum_{\Omega} p(\Omega \vert s_0) \log p(\Omega \vert s_0) + \sum_{s_f, \Omega} p^J(s_f \vert s_0, \Omega) p^C(\Omega \vert s_0) \log \color{red}{q(\Omega \vert s_0, s_f)} \\
I(\Omega; s_f \vert s_0) &\geq I^{VB}(\Omega; s_f \vert s_0)
\end{aligned}
$$




![VIC](https://lilianweng.github.io/posts/2020-06-07-exploration-drl/VIC-explicit-options.png)

*图 17. VIC（变分内在控制）的算法。（图片来源：[Gregor, et al. 2017](https://arxiv.org/abs/1611.07507)）*


这里，$$\pi(a \vert \Omega, s)$$ 可以用任意 RL 算法来优化。选项推断函数 $$q(\Omega \vert s_0, s_f)$$ 做的是监督学习。先验 $$p^C$$ 会被更新，使其倾向于选择奖励更高的 $$\Omega$$。注意 $$p^C$$ 也可以固定不变（例如一个高斯分布）。通过学习，不同的 $$\Omega$$ 会产生不同的行为。此外，[Gregor, et al. (2017)](https://arxiv.org/abs/1611.07507) 观察到，在使用函数逼近时，显式选项版本的 VIC 在实践中很难奏效，因此他们还提出了使用隐式选项的另一个 VIC 版本。

与只在起始和终止状态条件下建模 $$\Omega$$ 的 VIC 不同，**VALOR**（*"Variational Auto-encoding Learning of Options by Reinforcement"* 的简称；[Achiam, et al. 2018](https://arxiv.org/abs/1807.10299)）依赖整条轨迹来提取选项上下文 $$c$$，该上下文从一个固定的高斯分布中采样。在 VALOR 中：
- 策略充当编码器，把来自噪声分布的上下文翻译成轨迹；
- 解码器试图从轨迹中恢复出上下文，并因为让上下文更易于区分而奖励策略。训练期间解码器永远看不到动作，因此智能体必须以一种便于与解码器「沟通」的方式与环境交互，以获得更好的预测。此外，解码器以循环方式接收一条轨迹中的一系列步骤，以更好地建模时间步之间的相关性。


![VALOR](https://lilianweng.github.io/posts/2020-06-07-exploration-drl/VALOR-decoder.png)

*图 18. VALOR 的解码器是一个 biLSTM，以一条轨迹中等间隔采样的 $$N = 11$$ 个观测作为输入。（图片来源：[Achiam, et al. 2018](https://arxiv.org/abs/1807.10299)）*


DIAYN（"Diversity is all you need"；[Eysenbach, et al. 2018](https://arxiv.org/abs/1802.06070)）的思路也在同一方向，只是名字不同——DIAYN 对以潜在*技能（skill）*变量为条件的策略进行建模。更多细节见我的[前一篇博文](https://lilianweng.github.io/posts/2019-06-23-meta-rl/#learning-with-random-rewards)。

---
引用本文（Cited as）：
```
@article{weng2020exploration,
  title   = "Exploration Strategies in Deep Reinforcement Learning",
  author  = "Weng, Lilian",
  journal = "lilianweng.github.io/lil-log",
  year    = "2020",
  url     = "https://lilianweng.github.io/lil-log/2020/06/07/exploration-strategies-in-deep-reinforcement-learning.html"
}
```



## 参考文献

[1] Pierre-Yves Oudeyer & Frederic Kaplan. ["How can we define intrinsic motivation?"](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.567.6524&rep=rep1&type=pdf) Conf. on Epigenetic Robotics, 2008.

[2] Marc G. Bellemare, et al. ["Unifying Count-Based Exploration and Intrinsic Motivation"](https://arxiv.org/abs/1606.01868). NIPS 2016.

[3] Georg Ostrovski, et al. ["Count-Based Exploration with Neural Density Models"](https://arxiv.org/abs/1703.01310). PMLR 2017.

[4] Rui Zhao & Volker Tresp. ["Curiosity-Driven Experience Prioritization via
Density Estimation"](https://arxiv.org/abs/1902.08039). NIPS 2018.

[5] Haoran Tang, et al. ["#Exploration: A Study of Count-Based Exploration for Deep Reinforcement Learning"](https://arxiv.org/abs/1611.04717). NIPS 2017.

[6] Jürgen Schmidhuber. ["A possibility for implementing curiosity and boredom in model-building neural controllers"](http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.45.957) 1991.

[7] Pierre-Yves Oudeyer, et al. ["Intrinsic Motivation Systems for Autonomous Mental Development"](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.177.7661&rep=rep1&type=pdf) IEEE Transactions on Evolutionary Computation, 2007.

[8] Bradly C. Stadie, et al. ["Incentivizing Exploration In Reinforcement Learning With Deep Predictive Models"](https://arxiv.org/abs/1507.00814). ICLR 2016.

[9] Deepak Pathak, et al. ["Curiosity-driven Exploration by Self-supervised Prediction"](https://arxiv.org/abs/1705.05363). CVPR 2017.

[10] Yuri Burda, Harri Edwards & Deepak Pathak, et al. ["Large-Scale Study of Curiosity-Driven Learning"](https://arxiv.org/abs/1808.04355). arXiv 1808.04355 (2018).

[11] Joshua Achiam & Shankar Sastry. ["Surprise-Based Intrinsic Motivation for Deep Reinforcement Learning"](https://arxiv.org/abs/1703.01732) NIPS 2016 Deep RL Workshop.

[12] Rein Houthooft, et al. ["VIME: Variational information maximizing exploration"](https://arxiv.org/abs/1605.09674). NIPS 2016.

[13] Leshem Choshen, Lior Fox & Yonatan Loewenstein. ["DORA the explorer: Directed outreaching reinforcement action-selection"](https://arxiv.org/abs/1804.04012). ICLR 2018

[14] Yuri Burda, et al. ["Exploration by Random Network Distillation"](https://arxiv.org/abs/1810.12894) ICLR 2019.

[15] OpenAI Blog: ["Reinforcement Learning with
Prediction-Based Rewards"](https://openai.com/blog/reinforcement-learning-with-prediction-based-rewards/) Oct, 2018.

[16] Misha Denil, et al. ["Learning to Perform Physics Experiments via Deep Reinforcement Learning"](https://arxiv.org/abs/1611.01843). ICLR 2017.

[17] Ian Osband, et al. ["Deep Exploration via Bootstrapped DQN"](https://arxiv.org/abs/1602.04621). NIPS 2016.

[18] Ian Osband, John Aslanides & Albin Cassirer. ["Randomized Prior Functions for Deep Reinforcement Learning"](https://arxiv.org/abs/1806.03335). NIPS 2018.

[19] Karol Gregor, Danilo Jimenez Rezende & Daan Wierstra. ["Variational Intrinsic Control"](https://arxiv.org/abs/1611.07507). ICLR 2017.

[20] Joshua Achiam, et al. ["Variational Option Discovery Algorithms"](https://arxiv.org/abs/1807.10299). arXiv 1807.10299 (2018).

[21] Benjamin Eysenbach, et al. ["Diversity is all you need: Learning skills without a reward function."](https://arxiv.org/abs/1802.06070). ICLR 2019.

[22] Adrià Puigdomènech Badia, et al. ["Never Give Up (NGU): Learning Directed Exploration Strategies"](https://arxiv.org/abs/2002.06038) ICLR 2020.

[23] Adrià Puigdomènech Badia, et al.  ["Agent57: Outperforming the Atari Human Benchmark"](https://arxiv.org/abs/2003.13350). arXiv 2003.13350 (2020).

[24] DeepMind Blog: ["Agent57: Outperforming the human Atari benchmark"](https://deepmind.com/blog/article/Agent57-Outperforming-the-human-Atari-benchmark) Mar 2020.

[25] Nikolay Savinov, et al. ["Episodic Curiosity through Reachability"](https://arxiv.org/abs/1810.02274) ICLR 2019.

[26] Adrien Ecoffet, et al. ["Go-Explore: a New Approach for Hard-Exploration Problems"](https://arxiv.org/abs/1901.10995). arXiv 1901.10995 (2019).

[27] Adrien Ecoffet, et al. ["First return then explore"](https://arxiv.org/abs/2004.12919). arXiv 2004.12919 (2020).

[28] Junhyuk Oh, et al. ["Self-Imitation Learning"](https://arxiv.org/abs/1806.05635). ICML 2018.

[29] Yijie Guo, et al. ["Self-Imitation Learning via Trajectory-Conditioned Policy for Hard-Exploration Tasks"](https://arxiv.org/abs/1907.10247). arXiv 1907.10247 (2019).

[30] Zhaohan Daniel Guo & Emma Brunskill. ["Directed Exploration for Reinforcement Learning"](https://arxiv.org/abs/1906.07805). arXiv 1906.07805 (2019).

[31] Deepak Pathak, et al. [“Self-Supervised Exploration via Disagreement.”](https://arxiv.org/abs/1906.04161) ICML 2019.
