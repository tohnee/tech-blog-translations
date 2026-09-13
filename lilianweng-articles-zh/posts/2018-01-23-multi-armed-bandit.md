---
title: "多臂老虎机问题及其解法"
title_en: "The Multi-Armed Bandit Problem and Its Solutions"
source: https://lilianweng.github.io/posts/2018-01-23-multi-armed-bandit/
crawled: 2026-09-08
translated: 2026-09-08
---

# 多臂老虎机问题及其解法

> 原文：[The Multi-Armed Bandit Problem and Its Solutions](https://lilianweng.github.io/posts/2018-01-23-multi-armed-bandit/) · Lilian Weng（翁荔）

> 多臂老虎机（multi-armed bandit）问题是展示探索与利用（exploration versus exploitation）两难困境的经典例子。本文介绍老虎机问题以及如何用不同的探索策略求解。

这些算法针对伯努利老虎机的实现见 [lilianweng/multi-armed-bandit](http://github.com/lilianweng/multi-armed-bandit)。

## 利用与探索

探索与利用的两难困境存在于我们生活的诸多方面。比如说，你最喜欢的餐厅就在街角。如果你每天都去那里，你会对将吃到什么很有把握，但也错过了发现更好选择的机会。如果你总尝试新的餐厅，你很可能时不时得吃难以下咽的饭菜。类似地，在线广告推荐系统要在"已知最吸引用户的广告"与"可能效果更好的新广告"之间寻求平衡。

![bernoulli bandit](https://lilianweng.github.io/posts/2018-01-23-multi-armed-bandit/exploration_vs_exploitation.png)

*图 1：探索与利用两难困境的现实示例：去哪儿吃饭？（图片来源：UC Berkeley AI 课程[幻灯片](http://ai.berkeley.edu/lecture_slides.html)，[第 11 讲](http://ai.berkeley.edu/slides/Lecture%2011%20--%20Reinforcement%20Learning%20II/SP14%20CS188%20Lecture%2011%20--%20Reinforcement%20Learning%20II.pptx)。）*

如果我们已经掌握了环境的全部信息，哪怕只用暴力模拟也能找到最佳策略，更别提许多其他聪明的方法了。两难困境来自*不完全*信息：我们需要在控制风险的同时收集足够的信息来做出全局最优决策。利用（exploitation）时，我们享用已知的最优选项；探索（exploration）时，我们承担一定风险去收集未知选项的信息。最佳的长期策略可能涉及短期牺牲。例如，一次探索尝试可能彻底失败，但它警示我们今后不要频繁采取那个行动。

## 什么是多臂老虎机？

[多臂老虎机](https://en.wikipedia.org/wiki/Multi-armed_bandit)问题是经典问题，完美展示了探索与利用的两难困境。想象你身处一家赌场，面对多台老虎机，每台都配置了一个未知的"一次游戏获得奖励"的概率。问题是：*实现最高长期奖励的最佳策略是什么？*

本文只讨论无限次试验的设定。有限次试验的约束会引入一类新的探索问题。例如，若试验次数少于老虎机数量，我们甚至无法试遍每台机器来估计奖励概率（！），因此必须在有限的知识和资源（即时间）面前聪明行事。

![bernoulli bandit](https://lilianweng.github.io/posts/2018-01-23-multi-armed-bandit/bern_bandit.png)

*图 2：伯努利多臂老虎机工作方式示意图。玩家**不知道**奖励概率。*

一种朴素的做法是：在一台机器上连续玩很多很多轮，最终依据[大数定律](https://en.wikipedia.org/wiki/Law_of_large_numbers)估计出"真实"奖励概率。然而这相当浪费，而且显然无法保证最佳长期奖励。

### 定义

现在给它一个科学的定义。

一个伯努利多臂老虎机可以描述为元组 $$\langle \mathcal{A}, \mathcal{R} \rangle$$，其中：
- 我们有 $$K$$ 台机器，奖励概率为 $$\{ \theta_1, \dots, \theta_K \}$$。
- 在每个时间步 t，我们在一台老虎机上采取动作 a 并获得奖励 r。
- $$\mathcal{A}$$ 是动作集合，每个动作指与一台老虎机的交互。动作 a 的价值是期望奖励，$$Q(a) = \mathbb{E} [r \vert a] = \theta$$。若时间步 t 的动作 $$a_t$$ 在第 i 台机器上，则 $$Q(a_t) = \theta_i$$。
- $$\mathcal{R}$$ 是奖励函数。在伯努利老虎机的情形下，我们以*随机*方式观测奖励 r。在时间步 t，$$r_t = \mathcal{R}(a_t)$$ 以概率 $$Q(a_t)$$ 返回奖励 1，否则返回 0。

它是[马尔可夫决策过程](https://en.wikipedia.org/wiki/Markov_decision_process)的简化版本，因为没有状态 $$\mathcal{S}$$。

目标是最大化累积奖励 $$\sum_{t=1}^T r_t$$。
如果我们知道具有最佳奖励的最优动作，那么目标等价于最小化因未选最优动作而产生的潜在[遗憾（regret）](https://en.wikipedia.org/wiki/Regret_(decision_theory))或损失。

最优动作 $$a^{*}$$ 的最优奖励概率 $$\theta^{*}$$ 为：

$$
\theta^{*}=Q(a^{*})=\max_{a \in \mathcal{A}} Q(a) = \max_{1 \leq i \leq K} \theta_i
$$

我们的损失函数是截至时间步 T 未选择最优动作而可能产生的总遗憾：

$$
\mathcal{L}_T = \mathbb{E} \Big[ \sum_{t=1}^T \big( \theta^{*} - Q(a_t) \big) \Big]
$$

### 老虎机策略

依据探索方式的不同，求解多臂老虎机有几条路径：
- 不探索：最朴素也很糟糕的做法。
- 随机探索
- 偏向不确定性的聪明探索

## ε-贪婪算法

ε-贪婪（ε-greedy）算法大多数时候选择最佳动作，但偶尔进行随机探索。动作价值依据过往经验估计：对我们迄今为止（截至当前时间步 t）观测到的与目标动作 a 相关联的奖励取平均：

$$
\hat{Q}_t(a) = \frac{1}{N_t(a)} \sum_{\tau=1}^t r_\tau \mathbb{1}[a_\tau = a]
$$

其中 $$\mathbb{1}$$ 是二值指示函数，$$N_t(a)$$ 是动作 a 迄今被选中的次数，$$N_t(a) = \sum_{\tau=1}^t \mathbb{1}[a_\tau = a]$$。

按照 ε-贪婪算法，我们以小概率 $$\epsilon$$ 采取随机动作，否则（应当占绝大多数时候，概率 1-$$\epsilon$$）选择迄今学到的最佳动作：$$\hat{a}^{*}_t = \arg\max_{a \in \mathcal{A}} \hat{Q}_t(a)$$。

我的玩具实现见[这里](https://github.com/lilianweng/multi-armed-bandit/blob/master/solvers.py#L45)。

## 置信上界

随机探索给了我们尝试所知甚少的选项的机会。然而，由于随机性，我们有可能最终又去探索了一个过去已确认很差的动作（运气不好！）。为避免这种低效探索，一种方法是随时间减小参数 ε，另一种方法是对*高不确定性*的选项保持乐观，从而偏好那些我们尚未得到自信价值估计的动作。换言之，我们青睐探索那些有很大潜力拥有最优值的动作。

置信上界（Upper Confidence Bounds，UCB）算法用奖励值的置信上界 $$\hat{U}_t(a)$$ 来度量这种潜力，使得真值以高概率满足 $$Q(a) \leq \hat{Q}_t(a) + \hat{U}_t(a)$$。上界 $$\hat{U}_t(a)$$ 是 $$N_t(a)$$ 的函数；试验次数 $$N_t(a)$$ 越多，上界 $$\hat{U}_t(a)$$ 应当越小。

在 UCB 算法中，我们始终选择最大化置信上界的贪婪动作：

$$
a^{UCB}_t = argmax_{a \in \mathcal{A}} \hat{Q}_t(a) + \hat{U}_t(a)
$$

现在的问题是*如何估计置信上界*。

### Hoeffding 不等式

如果我们不想对分布形态赋予任何先验知识，可以借助 ["Hoeffding 不等式"](http://cs229.stanford.edu/extra-notes/hoeffding.pdf)——一个适用于任何有界分布的定理。

设 $$X_1, \dots, X_t$$ 为独立同分布（i.i.d.）随机变量，且都被限制在区间 [0, 1] 内。样本均值为 $$\overline{X}_t = \frac{1}{t}\sum_{\tau=1}^t X_\tau$$。那么对 u > 0，有：

$$
\mathbb{P} [ \mathbb{E}[X] > \overline{X}_t + u] \leq e^{-2tu^2}
$$

给定一个目标动作 a，考虑：
- $$r_t(a)$$ 作为随机变量，
- $$Q(a)$$ 作为真实均值，
- $$\hat{Q}_t(a)$$ 作为样本均值，
- $$u$$ 作为置信上界，$$u = U_t(a)$$

于是有，

$$
\mathbb{P} [ Q(a) > \hat{Q}_t(a) + U_t(a)] \leq e^{-2t{U_t(a)}^2}
$$

我们想选取一个界，使真实均值以很大概率低于样本均值 + 置信上界。因此 $$e^{-2t U_t(a)^2}$$ 应当是一个小概率。假设我们接受一个极小的阈值 p：

$$
e^{-2t U_t(a)^2} = p \text{  Thus, } U_t(a) = \sqrt{\frac{-\log p}{2 N_t(a)}}
$$

### UCB1

一个启发式做法是随时间减小阈值 p，因为随着观测到的奖励增多，我们想做出更自信的界估计。设 $$p=t^{-4}$$，就得到 **UCB1** 算法：

$$
U_t(a) = \sqrt{\frac{2 \log t}{N_t(a)}} \text{  and  }
a^{UCB1}_t = \arg\max_{a \in \mathcal{A}} Q(a) + \sqrt{\frac{2 \log t}{N_t(a)}}
$$

### 贝叶斯 UCB

在 UCB 或 UCB1 算法中，我们不假设奖励分布的任何先验，因此只能依靠 Hoeffding 不等式做非常泛化的估计。如果我们能预先知道分布，就能做出更好的界估计。

例如，如果我们预期每台老虎机的平均奖励如图 2 那样服从高斯分布，就可以把 $$\hat{U}_t(a)$$ 设为两倍标准差，从而将上界设为 95% 置信区间。

![高斯先验](https://lilianweng.github.io/posts/2018-01-23-multi-armed-bandit/bern_UCB.png)

*图 3：当期望奖励服从高斯分布时。$$\sigma(a_i)$$ 是标准差，$$c\sigma(a_i)$$ 是置信上界。常数 $$c$$ 是可调的超参数。（图片来源：[UCL RL 课程第 9 讲幻灯片](http://www0.cs.ucl.ac.uk/staff/d.silver/web/Teaching_files/XX.pdf)）*

查看我用 Beta 先验对 θ 实现的 [UCB1](https://github.com/lilianweng/multi-armed-bandit/blob/master/solvers.py#L76) 和[贝叶斯 UCB](https://github.com/lilianweng/multi-armed-bandit/blob/master/solvers.py#L99) 玩具实现。

## 汤普森采样

汤普森采样（Thompson sampling）思想简单，但对求解多臂老虎机问题非常有效。

![Thompson?](https://lilianweng.github.io/posts/2018-01-23-multi-armed-bandit/klay-thompson.jpg)

*图 4：Oops，我想说的不是这位 Thompson？（致谢 [Ben Taborsky](https://www.linkedin.com/in/benjamin-taborsky)；他有一个完整的"定理"，讲 Thompson 是如何在思考该把球传给谁时发明这个方法的。没错，这个玩笑是我偷来的。）*

在每个时间步，我们想按照动作 a 是**最优**的概率来选择动作 a：

$$
\begin{aligned}
\pi(a \; \vert \; h_t) 
&= \mathbb{P} [ Q(a) > Q(a'), \forall a' \neq a \; \vert \; h_t] \\
&= \mathbb{E}_{\mathcal{R} \vert h_t} [ \mathbb{1}(a = \arg\max_{a \in \mathcal{A}} Q(a)) ]
\end{aligned}
$$

其中 $$\pi(a \; \vert \; h_t)$$ 是给定历史 $$h_t$$ 时采取动作 a 的概率。

对伯努利老虎机而言，自然可以假设 $$Q(a)$$ 服从 [Beta](https://en.wikipedia.org/wiki/Beta_distribution) 分布，因为 $$Q(a)$$ 本质上是[伯努利分布](https://en.wikipedia.org/wiki/Bernoulli_distribution)中的成功概率 θ。$$\text{Beta}(\alpha, \beta)$$ 的取值在区间 [0, 1] 内；α 和 β 分别对应我们**成功**和**失败**获得奖励的次数。

首先，我们基于某些先验知识或信念为每个动作初始化 Beta 参数 α 和 β。例如：
- α = 1 且 β = 1；我们预期奖励概率为 50%，但不太自信。
- α = 1000 且 β = 9000；我们强烈相信奖励概率是 10%。

在每个时间 t，我们为每个动作从先验分布 $$\text{Beta}(\alpha_i, \beta_i)$$ 采样一个期望奖励 $$\tilde{Q}(a)$$，并在这些采样中选出最佳动作：$$a^{TS}_t = \arg\max_{a \in \mathcal{A}} \tilde{Q}(a)$$。观测到真实奖励后，我们可以相应地更新 Beta 分布，这本质上是在已知先验和采样数据似然的情况下做贝叶斯推断计算后验。

$$
\begin{aligned}
\alpha_i & \leftarrow \alpha_i + r_t \mathbb{1}[a^{TS}_t = a_i] \\ 
\beta_i & \leftarrow \beta_i + (1-r_t) \mathbb{1}[a^{TS}_t = a_i]
\end{aligned}
$$

汤普森采样实现了[概率匹配（probability matching）](https://en.wikipedia.org/wiki/Probability_matching)的思想。因为其奖励估计 $$\tilde{Q}$$ 是从后验分布采样的，这些概率各自等价于在观测历史条件下对应动作为最优的概率。

然而，对于许多实际的复杂问题，用贝叶斯推断依据观测到的真实奖励来估计后验分布可能在计算上不可解。如果我们能用 Gibbs 采样、拉普拉斯近似和自助法（bootstrap）等方法近似后验分布，汤普森采样依然可行。这篇[教程](https://arxiv.org/pdf/1707.02038.pdf)给出了全面的综述；想深入了解汤普森采样强烈推荐阅读。

## 案例研究

我在 [lilianweng/multi-armed-bandit](https://github.com/lilianweng/multi-armed-bandit) 中实现了上述算法。可以用一组随机或预定义的奖励概率构造 [BernoulliBandit](https://github.com/lilianweng/multi-armed-bandit/blob/master/bandits.py#L13) 对象。老虎机算法实现为 [Solver](https://github.com/lilianweng/multi-armed-bandit/blob/master/solvers.py#L9) 的子类，以一个 Bandit 对象为目标问题。累积遗憾随时间被跟踪记录。

![案例研究](https://lilianweng.github.io/posts/2018-01-23-multi-armed-bandit/bandit_experiment.png)

*图 4：求解奖励概率为 {0.0, 0.1, 0.2, ..., 0.9} 的 K = 10 台老虎机组成的伯努利老虎机的小实验结果。每个求解器运行 10000 步。
（左）时间步与累积遗憾的关系图。
（中）真实奖励概率与估计概率的关系图。
（右）10000 步运行中每个动作被选中的比例。*

## 总结

我们需要探索，因为信息是有价值的。就探索策略而言，我们可以完全不探索、只专注短期回报；或者偶尔随机探索；甚至更进一步，我们探索且对探索哪些选项有所挑剔——更偏好不确定性高的动作，因为它们能带来更高的信息增益。

![bernoulli UCB](https://lilianweng.github.io/posts/2018-01-23-multi-armed-bandit/bandit_solution_summary.png)

---

引用格式：
```
@article{weng2018bandit,
  title   = "The Multi-Armed Bandit Problem and Its Solutions",
  author  = "Weng, Lilian",
  journal = "lilianweng.github.io/lil-log",
  year    = "2018",
  url     = "http://lilianweng.github.io/lil-log/2018/01/23/the-multi-armed-bandit-problem-and-its-solutions.html"
}
```

# 参考文献

[1] CS229 Supplemental Lecture notes: [Hoeffding's inequality](http://cs229.stanford.edu/extra-notes/hoeffding.pdf).

[2] RL Course by David Silver - Lecture 9: [Exploration and Exploitation](https://youtu.be/sGuiWX07sKw)

[3] Olivier Chapelle and Lihong Li. ["An empirical evaluation of thompson sampling."](http://papers.nips.cc/paper/4321-an-empirical-evaluation-of-thompson-sampling.pdf) NIPS. 2011.

[4] Russo, Daniel, et al. ["A Tutorial on Thompson Sampling."](https://arxiv.org/pdf/1707.02038.pdf) arXiv:1707.02038 (2017).
