---
title: "策略梯度算法"
title_en: "Policy Gradient Algorithms"
source: https://lilianweng.github.io/posts/2018-04-08-policy-gradient/
crawled: 2026-09-08
translated: 2026-09-08
---

# 策略梯度算法

> 原文：[Policy Gradient Algorithms](https://lilianweng.github.io/posts/2018-04-08-policy-gradient/) · Lilian Weng（翁荔）

> 摘要：本文将深入探讨策略梯度（policy gradient）：它为什么有效，以及近年来提出的许多新策略梯度算法：vanilla policy gradient、actor-critic、off-policy actor-critic、A3C、A2C、DPG、DDPG、D4PG、MADDPG、TRPO、PPO、ACER、ACKTR、SAC、TD3 与 SVPG。

<span style="color: #286ee0;">[更新于 2018-06-30：新增两种策略梯度方法 [SAC](#sac) 和 [D4PG](#d4pg)。]</span>
<br/>
<span style="color: #286ee0;">[更新于 2018-09-30：新增一种策略梯度方法 [TD3](#td3)。]</span>
<br/>
<span style="color: #286ee0;">[更新于 2019-02-09：新增[自动调节温度的 SAC](#sac-with-automatically-adjusted-temperature)。]</span>
<br/>
<span style="color: #286ee0;">[更新于 2019-06-26：感谢 Chanseok，本文有了[韩语版本](https://talkingaboutme.tistory.com/entry/RL-Policy-Gradient-Algorithms)。]</span>
<br/>
<span style="color: #286ee0;">[更新于 2019-09-12：新增一种策略梯度方法 [SVPG](#svpg)。]</span>
<br/>
<span style="color: #286ee0;">[更新于 2019-12-22：新增一种策略梯度方法 [IMPALA](#impala)。]</span>
<br/>
<span style="color: #286ee0;">[更新于 2020-10-15：新增一种策略梯度方法 [PPG](#ppg)，并在 [PPO](#ppo) 中增加了一些新的讨论。]</span>
<br/>
<span style="color: #286ee0;">[更新于 2021-09-19：感谢 Wenhao 与 爱吃猫的鱼，本文有了[中文译本1](https://tomaxent.com/2019/04/14/%E7%AD%96%E7%95%A5%E6%A2%AF%E5%BA%A6%E6%96%B9%E6%B3%95/) 和 [中文译本2](https://paperexplained.cn/articles/article/detail/31/)。]</span>

## 什么是策略梯度

策略梯度是求解强化学习问题的一种方法。如果你还没有接触过强化学习领域，请先阅读 ["A (Long) Peek into Reinforcement Learning >> Key Concepts"](https://lilianweng.github.io/posts/2018-02-19-rl-overview/#key-concepts) 一节，了解问题定义和关键概念。

### 符号约定

下面是本文用到的一系列符号，帮助你轻松读懂各公式。

| 符号 | 含义 |
| ----------------------------- | ------------- |
| $$s \in \mathcal{S}$$ | 状态。 |
| $$a \in \mathcal{A}$$ | 动作。 |
| $$r \in \mathcal{R}$$ | 奖励。 |
| $$S_t, A_t, R_t$$ | 一条轨迹在时间步 $$t$$ 的状态、动作和奖励。有时我也用 $$s_t, a_t, r_t$$。 |
| $$\gamma$$ | 折扣因子；对未来奖励不确定性的惩罚；$$0<\gamma \leq 1$$。 |
| $$G_t$$ | 回报；或折扣未来奖励；$$G_t = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1}$$。 |
| $$P(s', r \vert s, a)$$ | 在当前状态 $$s$$ 采取动作 $$a$$、获得奖励 $$r$$ 后转移到下一状态 $$s'$$ 的转移概率。 |
| $$\pi(a \vert s)$$ | 随机策略（智能体行为策略）；$$\pi_\theta(.)$$ 是参数为 $$\theta$$ 的策略。 |
| $$\mu(s)$$ | 确定性策略；也可以记作 $$\pi(s)$$，但用一个不同的字母能更好地加以区分，使我们无需额外解释就能轻易分辨策略是随机的还是确定性的。$$\pi$$ 或 $$\mu$$ 都是强化学习算法要学习的东西。 |
| $$V(s)$$ | 状态价值函数，度量状态 $$s$$ 的期望回报；$$V_w(.)$$ 是参数为 $$w$$ 的价值函数。|
| $$V^\pi(s)$$ | 遵循策略 $$\pi$$ 时状态 $$s$$ 的价值；$$V^\pi (s) = \mathbb{E}_{a\sim \pi} [G_t \vert S_t = s]$$。 |
| $$Q(s, a)$$ | 动作价值函数，与 $$V(s)$$ 类似，但评估的是一对状态与动作 $$(s, a)$$ 的期望回报；$$Q_w(.)$$ 是参数为 $$w$$ 的动作价值函数。 |
| $$Q^\pi(s, a)$$ | 与 $$V^\pi(.)$$ 类似，遵循策略 $$\pi$$ 时（状态, 动作）对的价值；$$Q^\pi(s, a) = \mathbb{E}_{a\sim \pi} [G_t \vert S_t = s, A_t = a]$$。 |
| $$A(s, a)$$ | 优势函数，$$A(s, a) = Q(s, a) - V(s)$$；可以视为以状态价值为基线从而降低方差后的另一个版本的 Q 值。 |

### 策略梯度

强化学习的目标是为智能体找到最优行为策略以获得最优奖励。**策略梯度**方法直接对策略建模并优化。策略通常用关于 $$\theta$$ 参数化的函数建模，$$\pi_\theta(a \vert s)$$。奖励（目标）函数的值取决于这个策略，然后可以用各种算法优化 $$\theta$$ 以获得最佳奖励。

奖励函数定义为：

$$
J(\theta) 
= \sum_{s \in \mathcal{S}} d^\pi(s) V^\pi(s) 
= \sum_{s \in \mathcal{S}} d^\pi(s) \sum_{a \in \mathcal{A}} \pi_\theta(a \vert s) Q^\pi(s, a)
$$

其中 $$d^\pi(s)$$ 是 $$\pi_\theta$$ 的马尔可夫链平稳分布（$$\pi$$ 下的同策略状态分布）。为简单起见，当策略出现在其他函数的下标中时，策略 $$\pi_\theta$$ 的参数 $$\theta$$ 会被省略；例如 $$d^{\pi}$$ 和 $$Q^\pi$$ 完整写出时应为 $$d^{\pi_\theta}$$ 和 $$Q^{\pi_\theta}$$。

想象你可以沿着马尔可夫链的状态永远走下去，最终随着时间推移，你停留在某个状态的概率不再变化——这就是 $$\pi_\theta$$ 的平稳概率。$$d^\pi(s) = \lim_{t \to \infty} P(s_t = s \vert s_0, \pi_\theta)$$ 是从 $$s_0$$ 出发、遵循策略 $$\pi_\theta$$ 走 t 步后 $$s_t=s$$ 的概率。事实上，马尔可夫链平稳分布的存在正是 PageRank 算法得以奏效的主要原因之一。想了解更多可以看[这里](https://jeremykun.com/2015/04/06/markov-chain-monte-carlo-without-all-the-bullshit/)。

很自然地可以预期：基于策略的方法在连续空间中更有用。因为需要估计价值的动作和（或）状态有无限多个，基于价值的方法在连续空间中计算代价过高。例如，在[广义策略迭代](https://lilianweng.github.io/posts/2018-02-19-rl-overview/#policy-iteration)中，策略改进步骤 $$\arg\max_{a \in \mathcal{A}} Q^\pi(s, a)$$ 需要全量扫描动作空间，受[维度灾难](https://en.wikipedia.org/wiki/Curse_of_dimensionality)之苦。

利用*梯度上升*，我们可以让 $$\theta$$ 朝梯度 $$\nabla_\theta J(\theta)$$ 指示的方向移动，找到能为 $$\pi_\theta$$ 产生最高回报的最佳 $$\theta$$。

### 策略梯度定理

计算梯度 $$\nabla_\theta J(\theta)$$ 很棘手，因为它既依赖于动作选择（直接由 $$\pi_\theta$$ 决定），也依赖于遵循目标选择行为后状态的平稳分布（间接由 $$\pi_\theta$$ 决定）。鉴于环境通常是未知的，很难估计一次策略更新对状态分布的影响。

幸运的是，**策略梯度定理**来拯救世界了！哇哦！它对目标函数的导数做了一个漂亮的改写，使其不涉及状态分布 $$d^\pi(.)$$ 的导数，从而大大简化了梯度计算 $$\nabla_\theta J(\theta)$$。

$$
\begin{aligned}
\nabla_\theta J(\theta) 
&= \nabla_\theta \sum_{s \in \mathcal{S}} d^\pi(s) \sum_{a \in \mathcal{A}} Q^\pi(s, a) \pi_\theta(a \vert s) \\
&\propto \sum_{s \in \mathcal{S}} d^\pi(s) \sum_{a \in \mathcal{A}} Q^\pi(s, a) \nabla_\theta \pi_\theta(a \vert s) 
\end{aligned}
$$

### 策略梯度定理的证明

这一节相当密集，因为我们要过一遍证明（[Sutton & Barto, 2017](http://incompleteideas.net/book/bookdraft2017nov5.pdf)；第 13.1 节），弄清楚策略梯度定理为什么成立。

我们先从状态价值函数的导数开始：

$$
\begin{aligned}
& \nabla_\theta V^\pi(s) \\
=& \nabla_\theta \Big(\sum_{a \in \mathcal{A}} \pi_\theta(a \vert s)Q^\pi(s, a) \Big) & \\
=& \sum_{a \in \mathcal{A}} \Big( \nabla_\theta \pi_\theta(a \vert s)Q^\pi(s, a) + \pi_\theta(a \vert s) \color{red}{\nabla_\theta Q^\pi(s, a)} \Big) & \scriptstyle{\text{; Derivative product rule.}} \\
=& \sum_{a \in \mathcal{A}} \Big( \nabla_\theta \pi_\theta(a \vert s)Q^\pi(s, a) + \pi_\theta(a \vert s) \color{red}{\nabla_\theta \sum_{s', r} P(s',r \vert s,a)(r + V^\pi(s'))} \Big) & \scriptstyle{\text{; Extend } Q^\pi \text{ with future state value.}} \\
=& \sum_{a \in \mathcal{A}} \Big( \nabla_\theta \pi_\theta(a \vert s)Q^\pi(s, a) + \pi_\theta(a \vert s) \color{red}{\sum_{s', r} P(s',r \vert s,a) \nabla_\theta V^\pi(s')} \Big) & \scriptstyle{P(s',r \vert s,a) \text{ or } r \text{ is not a func of }\theta}\\
=& \sum_{a \in \mathcal{A}} \Big( \nabla_\theta \pi_\theta(a \vert s)Q^\pi(s, a) + \pi_\theta(a \vert s) \color{red}{\sum_{s'} P(s' \vert s,a) \nabla_\theta V^\pi(s')} \Big) & \scriptstyle{\text{; Because }  P(s' \vert s, a) = \sum_r P(s', r \vert s, a)}
\end{aligned}
$$

现在我们有：

$$
\color{red}{\nabla_\theta V^\pi(s)} 
= \sum_{a \in \mathcal{A}} \Big( \nabla_\theta \pi_\theta(a \vert s)Q^\pi(s, a) + \pi_\theta(a \vert s) \sum_{s'} P(s' \vert s,a) \color{red}{\nabla_\theta V^\pi(s')} \Big)
$$

这个方程有一个漂亮的递归形式（看红色的部分！），未来的状态价值函数 $$V^\pi(s')$$ 可以按同一方程反复展开。

考虑如下访问序列，把遵循策略 $$\pi_\theta$$ 从状态 s 经 k 步转移到状态 x 的概率记为 $$\rho^\pi(s \to x, k)$$。

$$
s \xrightarrow[]{a \sim \pi_\theta(.\vert s)} s' \xrightarrow[]{a \sim \pi_\theta(.\vert s')} s'' \xrightarrow[]{a \sim \pi_\theta(.\vert s'')} \dots
$$

* 当 k = 0：$$\rho^\pi(s \to s, k=0) = 1$$。
* 当 k = 1，我们扫描所有可能的动作，把转移到目标状态的转移概率加总：$$\rho^\pi(s \to s', k=1) = \sum_a \pi_\theta(a \vert s) P(s' \vert s, a)$$。
* 设想目标是遵循策略 $$\pi_\theta$$ 经 k+1 步从状态 s 走到 x。我们可以先在 k 步内从 s 走到某个中间点 s'（任何状态都可以是中间点，$$s' \in \mathcal{S}$$），再在最后一步走到终点状态 x。这样我们就能递归地更新访问概率：$$\rho^\pi(s \to x, k+1) = \sum_{s'} \rho^\pi(s \to s', k) \rho^\pi(s' \to x, 1)$$。

然后我们回头展开 $$\nabla_\theta V^\pi(s)$$ 的递归表示！令 $$\phi(s) = \sum_{a \in \mathcal{A}} \nabla_\theta \pi_\theta(a \vert s)Q^\pi(s, a)$$ 来简化数学。如果我们无限地继续扩展 $$\nabla_\theta V^\pi(.)$$，很容易发现在这个展开过程中，我们可以从起始状态 s 经过任意步数转移到任何状态，把所有访问概率加总，就得到 $$\nabla_\theta V^\pi(s)$$！

$$
\begin{aligned}
& \color{red}{\nabla_\theta V^\pi(s)} \\
=& \phi(s) + \sum_a \pi_\theta(a \vert s) \sum_{s'} P(s' \vert s,a) \color{red}{\nabla_\theta V^\pi(s')} \\
=& \phi(s) + \sum_{s'} \sum_a \pi_\theta(a \vert s) P(s' \vert s,a) \color{red}{\nabla_\theta V^\pi(s')} \\
=& \phi(s) + \sum_{s'} \rho^\pi(s \to s', 1) \color{red}{\nabla_\theta V^\pi(s')} \\
=& \phi(s) + \sum_{s'} \rho^\pi(s \to s', 1) \color{red}{\nabla_\theta V^\pi(s')} \\
=& \phi(s) + \sum_{s'} \rho^\pi(s \to s', 1) \color{red}{[ \phi(s') + \sum_{s''} \rho^\pi(s' \to s'', 1) \nabla_\theta V^\pi(s'')]} \\
=& \phi(s) + \sum_{s'} \rho^\pi(s \to s', 1) \phi(s') + \sum_{s''} \rho^\pi(s \to s'', 2)\color{red}{\nabla_\theta V^\pi(s'')} \scriptstyle{\text{ ; Consider }s'\text{ as the middle point for }s \to s''}\\
=& \phi(s) + \sum_{s'} \rho^\pi(s \to s', 1) \phi(s') + \sum_{s''} \rho^\pi(s \to s'', 2)\phi(s'') + \sum_{s'''} \rho^\pi(s \to s''', 3)\color{red}{\nabla_\theta V^\pi(s''')} \\
=& \dots \scriptstyle{\text{; Repeatedly unrolling the part of }\nabla_\theta V^\pi(.)} \\
=& \sum_{x\in\mathcal{S}}\sum_{k=0}^\infty \rho^\pi(s \to x, k) \phi(x)
\end{aligned}
$$

上面这个漂亮的改写让我们得以排除 Q 值函数的导数 $$\nabla_\theta Q^\pi(s, a)$$。把它代入目标函数 $$J(\theta)$$，得到：

$$
\begin{aligned}
\nabla_\theta J(\theta)
&= \nabla_\theta V^\pi(s_0) & \scriptstyle{\text{; Starting from a random state } s_0} \\
&= \sum_{s}\color{blue}{\sum_{k=0}^\infty \rho^\pi(s_0 \to s, k)} \phi(s) &\scriptstyle{\text{; Let }\color{blue}{\eta(s) = \sum_{k=0}^\infty \rho^\pi(s_0 \to s, k)}} \\
&= \sum_{s}\eta(s) \phi(s) & \\
&= \Big( {\sum_s \eta(s)} \Big)\sum_{s}\frac{\eta(s)}{\sum_s \eta(s)} \phi(s) & \scriptstyle{\text{; Normalize } \eta(s), s\in\mathcal{S} \text{ to be a probability distribution.}}\\
&\propto \sum_s \frac{\eta(s)}{\sum_s \eta(s)} \phi(s) & \scriptstyle{\sum_s \eta(s)\text{  is a constant}} \\
&= \sum_s d^\pi(s) \sum_a \nabla_\theta \pi_\theta(a \vert s)Q^\pi(s, a) & \scriptstyle{d^\pi(s) = \frac{\eta(s)}{\sum_s \eta(s)}\text{ is stationary distribution.}}
\end{aligned}
$$

在情节式（episodic）情形中，比例常数（$$\sum_s \eta(s)$$）是一个情节的平均长度；在持续性（continuing）情形中，它为 1（[Sutton & Barto, 2017](http://incompleteideas.net/book/bookdraft2017nov5.pdf)；第 13.2 节）。梯度可以进一步写成：

$$
\begin{aligned}
\nabla_\theta J(\theta) 
&\propto \sum_{s \in \mathcal{S}} d^\pi(s) \sum_{a \in \mathcal{A}} Q^\pi(s, a) \nabla_\theta \pi_\theta(a \vert s)  &\\
&= \sum_{s \in \mathcal{S}} d^\pi(s) \sum_{a \in \mathcal{A}} \pi_\theta(a \vert s) Q^\pi(s, a) \frac{\nabla_\theta \pi_\theta(a \vert s)}{\pi_\theta(a \vert s)} &\\
&= \mathbb{E}_\pi [Q^\pi(s, a) \nabla_\theta \ln \pi_\theta(a \vert s)] & \scriptstyle{\text{; Because } (\ln x)' = 1/x}
\end{aligned}
$$

其中 $$\mathbb{E}_\pi$$ 指 $$\mathbb{E}_{s \sim d_\pi, a \sim \pi_\theta}$$，即状态分布和动作分布都遵循策略 $$\pi_\theta$$（同策略）。

策略梯度定理为各种策略梯度算法奠定了理论基础。这种原始（vanilla）策略梯度更新无偏差但方差很高。后续许多算法的提出都是为了在保持偏差不变的同时降低方差。

$$
\nabla_\theta J(\theta)  = \mathbb{E}_\pi [Q^\pi(s, a) \nabla_\theta \ln \pi_\theta(a \vert s)]
$$

这里有一个借自 [GAE](https://arxiv.org/pdf/1506.02438.pdf)（general advantage estimation，广义优势估计）论文的策略梯度方法一般形式的漂亮总结（[Schulman et al., 2016](https://arxiv.org/abs/1506.02438)），而这篇[文章](https://danieltakeshi.github.io/2017/04/02/notes-on-the-generalized-advantage-estimation-paper/)深入讨论了 GAE 中的若干组件，强烈推荐。

![一般形式](https://lilianweng.github.io/posts/2018-04-08-policy-gradient/general_form_policy_gradient.png)

*图 1：策略梯度方法的一般形式。（图片来源：[Schulman et al., 2016](https://arxiv.org/abs/1506.02438)）*

## 策略梯度算法

近年来提出的策略梯度算法多如牛毛，我不可能穷尽。这里介绍一些我恰好知道并读过的。

### REINFORCE

**REINFORCE**（蒙特卡洛策略梯度）依靠[蒙特卡洛](https://lilianweng.github.io/posts/2018-02-19-rl-overview/#monte-carlo-methods)方法用情节样本估计的回报来更新策略参数 $$\theta$$。REINFORCE 之所以有效，是因为样本梯度的期望等于真实梯度：


$$
\begin{aligned}
\nabla_\theta J(\theta)
&= \mathbb{E}_\pi [Q^\pi(s, a) \nabla_\theta \ln \pi_\theta(a \vert s)] & \\
&= \mathbb{E}_\pi [G_t \nabla_\theta \ln \pi_\theta(A_t \vert S_t)] & \scriptstyle{\text{; Because } Q^\pi(S_t, A_t) = \mathbb{E}_\pi[G_t \vert S_t, A_t]}
\end{aligned}
$$

因此我们能够从真实的样本轨迹中测量 $$G_t$$ 并用它来更新策略梯度。它依赖完整轨迹，所以是一种蒙特卡洛方法。

过程非常直接：
1. 随机初始化策略参数 $$\theta$$。
2. 按策略 $$\pi_\theta$$ 生成一条轨迹：$$S_1, A_1, R_2, S_2, A_2, \dots, S_T$$。
3. 对 t=1, 2, ... , T：
    1. 估计回报 $$G_t$$；
    2. 更新策略参数：$$\theta \leftarrow \theta + \alpha \gamma^t G_t \nabla_\theta \ln \pi_\theta(A_t \vert S_t)$$

REINFORCE 的一个广为使用的变体是从回报 $$G_t$$ 中减去一个基线值，以*在保持偏差不变的同时降低梯度估计的方差*（记住，只要可能我们总想这么做）。例如，一个常见的基线是从动作价值中减去状态价值，若这样做，我们在梯度上升更新中就使用优势 $$A(s, a) = Q(s, a) - V(s)$$。这篇[文章](https://danieltakeshi.github.io/2017/03/28/going-deeper-into-reinforcement-learning-fundamentals-of-policy-gradients/)很好地解释了基线为何能降低方差，此外还讲了一组策略梯度的基础知识。

### Actor-Critic

策略梯度的两个主要组件是策略模型和价值函数。除策略之外同时学习价值函数非常有意义，因为知道价值函数可以辅助策略更新，比如降低原始策略梯度中的梯度方差，而这正是 **Actor-Critic**（演员-评论家）方法所做的。

Actor-critic 方法由两个模型组成，它们可以选择性地共享参数：
* **Critic（评论家）** 更新价值函数参数 w，依据具体算法，它可以是动作价值 $$Q_w(a \vert s)$$ 或状态价值 $$V_w(s)$$。
* **Actor（演员）** 按评论家建议的方向更新 $$\pi_\theta(a \vert s)$$ 的策略参数 $$\theta$$。

看一个简单的动作价值 actor-critic 算法如何工作：
1. 随机初始化 $$s, \theta, w$$；采样 $$a \sim \pi_\theta(a \vert s)$$。
2. 对 $$t = 1 \dots T$$：
    1. 采样奖励 $$r_t \sim R(s, a)$$ 和下一状态 $$s' \sim P(s' \vert s, a)$$；
    2. 然后采样下一动作 $$a' \sim \pi_\theta(a' \vert s')$$；
    3. 更新策略参数：$$\theta \leftarrow \theta + \alpha_\theta Q_w(s, a) \nabla_\theta \ln \pi_\theta(a \vert s)$$；
    4. 计算时间 t 动作价值的修正（TD 误差）：<br/>$$\delta_t = r_t + \gamma Q_w(s', a') - Q_w(s, a)$$ <br/>并用它更新动作价值函数的参数：<br/> $$w \leftarrow w + \alpha_w \delta_t \nabla_w Q_w(s, a)$$
    5. 更新 $$a \leftarrow a'$$ 和 $$s \leftarrow s'$$。

预定义两个学习率 $$\alpha_\theta$$ 和 $$\alpha_w$$，分别用于策略和价值函数参数的更新。

### 离策略策略梯度

REINFORCE 和原始版本的 actor-critic 方法都是同策略（on-policy）的：训练样本按照目标策略收集——正是我们要优化的那个策略。而离策略（off-policy）方法带来了几项额外优势：
1. 离策略方法不要求完整轨迹，可以复用任何过往情节（["经验回放"](https://lilianweng.github.io/posts/2018-02-19-rl-overview/#deep-q-network)），样本效率高得多。
2. 样本收集遵循一个与目标策略不同的行为策略，带来更好的[探索](https://lilianweng.github.io/posts/2018-02-19-rl-overview/#exploration-exploitation-dilemma)。

现在看离策略策略梯度如何计算。用于收集样本的行为策略是一个已知策略（像超参数一样预先定义），记为 $$\beta(a \vert s)$$。目标函数对该行为策略定义的状态分布上的奖励求和：


$$
J(\theta)
= \sum_{s \in \mathcal{S}} d^\beta(s) \sum_{a \in \mathcal{A}} Q^\pi(s, a) \pi_\theta(a \vert s)
= \mathbb{E}_{s \sim d^\beta} \big[ \sum_{a \in \mathcal{A}} Q^\pi(s, a) \pi_\theta(a \vert s) \big]
$$

其中 $$d^\beta(s)$$ 是行为策略 $$\beta$$ 的平稳分布；回忆 $$d^\beta(s) = \lim_{t \to \infty} P(S_t = s \vert S_0, \beta)$$；$$Q^\pi$$ 是关于目标策略 $$\pi$$（而非行为策略！）估计的动作价值函数。

鉴于训练观测由 $$a \sim \beta(a \vert s)$$ 采样，我们可以把梯度改写为：


$$
\begin{aligned}
\nabla_\theta J(\theta)
&= \nabla_\theta \mathbb{E}_{s \sim d^\beta} \Big[ \sum_{a \in \mathcal{A}} Q^\pi(s, a) \pi_\theta(a \vert s)  \Big] & \\ 
&= \mathbb{E}_{s \sim d^\beta} \Big[ \sum_{a \in \mathcal{A}} \big( Q^\pi(s, a) \nabla_\theta \pi_\theta(a \vert s) + \color{red}{\pi_\theta(a \vert s) \nabla_\theta Q^\pi(s, a)} \big) \Big] & \scriptstyle{\text{; Derivative product rule.}}\\
&\stackrel{(i)}{\approx} \mathbb{E}_{s \sim d^\beta} \Big[ \sum_{a \in \mathcal{A}} Q^\pi(s, a) \nabla_\theta \pi_\theta(a \vert s) \Big] & \scriptstyle{\text{; Ignore the red part: } \color{red}{\pi_\theta(a \vert s) \nabla_\theta Q^\pi(s, a)}}. \\
&= \mathbb{E}_{s \sim d^\beta} \Big[ \sum_{a \in \mathcal{A}} \beta(a \vert s) \frac{\pi_\theta(a \vert s)}{\beta(a \vert s)} Q^\pi(s, a) \frac{\nabla_\theta \pi_\theta(a \vert s)}{\pi_\theta(a \vert s)} \Big] & \\
&= \mathbb{E}_\beta \Big[\frac{\color{blue}{\pi_\theta(a \vert s)}}{\color{blue}{\beta(a \vert s)}} Q^\pi(s, a) \nabla_\theta \ln \pi_\theta(a \vert s) \Big] & \scriptstyle{\text{; The blue part is the importance weight.}}
\end{aligned}
$$

其中 $$\frac{\pi_\theta(a \vert s)}{\beta(a \vert s)}$$ 是[重要性权重](http://timvieira.github.io/blog/post/2014/12/21/importance-sampling/)。因为 $$Q^\pi$$ 是目标策略的函数，从而是策略参数 $$\theta$$ 的函数，按乘积法则我们也应该对 $$\nabla_\theta Q^\pi(s, a)$$ 求导。然而现实中计算 $$\nabla_\theta Q^\pi(s, a)$$ 超级难。幸运的是，如果我们忽略 Q 的梯度而使用近似梯度，仍能保证策略改进，并最终达到真正的局部极小值。[这里](https://arxiv.org/pdf/1205.4839.pdf)（Degris, White & Sutton, 2012）的证明给出了论证。

总结：在离策略设定下应用策略梯度时，我们只需用一个加权和来调整，权重即目标策略与行为策略之比 $$\frac{\pi_\theta(a \vert s)}{\beta(a \vert s)}$$。

### A3C

[[论文](https://arxiv.org/abs/1602.01783)\|[代码](https://github.com/dennybritz/reinforcement-learning/tree/master/PolicyGradient/a3c)]

**Asynchronous Advantage Actor-Critic**（[Mnih et al., 2016](https://arxiv.org/abs/1602.01783)），简称 **A3C**，是一种特别关注并行训练的经典策略梯度方法。

在 A3C 中，critic 学习价值函数，而多个 actor 并行训练并不时与全局参数同步。因此，A3C 的设计天然适合并行训练。

以状态价值函数为例。状态价值的损失函数是最小化均方误差 $$J_v(w) = (G_t - V_w(s))^2$$，用梯度下降即可找到最优的 w。该状态价值函数在策略梯度更新中用作基线。

算法概要如下：
1. 我们有全局参数 $$\theta$$ 和 $$w$$；以及类似的线程专属参数 $$\theta'$$ 和 $$w'$$。
2. 初始化时间步 $$t = 1$$。
3. 当 $$T \leq T_\text{MAX}$$：
    1. 重置梯度：$$\mathrm{d}\theta = 0$$ 且 $$\mathrm{d}w = 0$$。
    2. 将线程专属参数与全局参数同步：$$\theta' = \theta$$ 且 $$w' = w$$。
    3. $$t_\text{start}$$ = t 并采样起始状态 $$s_t$$。
    4. 当（$$s_t$$ != TERMINAL）且 $$t - t_\text{start} \leq t_\text{max}$$：
        1. 选取动作 $$A_t \sim \pi_{\theta'}(A_t \vert S_t)$$ 并接收新奖励 $$R_t$$ 和新状态 $$s_{t+1}$$。
        2. 更新 $$t = t + 1$$ 且 $$T = T + 1$$。
    5. 初始化保存回报估计的变量 $$R = \begin{cases} 
	0 & \text{if } s_t \text{ is TERMINAL} \\
	V_{w'}(s_t) & \text{otherwise}
	\end{cases}
	$$
    6. 对 $$i = t-1, \dots, t_\text{start}$$：
        1. $$R \leftarrow \gamma R + R_i$$；这里 R 是 $$G_i$$ 的蒙特卡洛度量。
        2. 累积关于 $$\theta'$$ 的梯度：$$d\theta \leftarrow d\theta + \nabla_{\theta'} \log \pi_{\theta'}(a_i \vert s_i)(R - V_{w'}(s_i))$$；<br/>累积关于 w' 的梯度：$$dw \leftarrow dw + 2 (R - V_{w'}(s_i)) \nabla_{w'} (R - V_{w'}(s_i))$$。
    7. 用 $$\mathrm{d}\theta$$ 异步更新 $$\theta$$，用 $$\mathrm{d}w$$ 更新 $$w$$。

A3C 实现了多智能体训练的并行化。梯度累积步骤（6.2）可以视为基于 minibatch 的随机梯度更新的并行化改造：$$w$$ 或 $$\theta$$ 的值被每个训练线程独立地朝各自的方向小幅修正。

### A2C

[[论文](https://arxiv.org/abs/1602.01783)\|[代码](https://github.com/openai/baselines/blob/master/baselines/a2c/a2c.py)]

**A2C** 是 A3C 的同步、确定性版本；这也是它被命名为 "A2C" 的原因——去掉了第一个 "A"（"asynchronous"）。在 A3C 中，每个智能体独立地与全局参数交互，因此有时线程专属的智能体可能在不同版本的策略上运行，聚合后的更新未必最优。为解决这种不一致，A2C 中的一个协调器等待所有并行 actor 完成工作后再更新全局参数，然后在下一轮迭代中并行 actor 从相同的策略出发。同步的梯度更新让训练更有凝聚力，收敛也可能更快。

A2C 已被[证明](https://blog.openai.com/baselines-acktr-a2c/)能更高效地利用 GPU，在大批量大小下工作更好，同时取得与 A3C 相同或更好的性能。

![A2C](https://lilianweng.github.io/posts/2018-04-08-policy-gradient/A3C_vs_A2C.png)

*图 2：A3C 与 A2C 的架构。*

### DPG

[[论文](https://hal.inria.fr/file/index/docid/938992/filename/dpg-icml2014.pdf)\|代码]

在上面介绍的方法中，策略函数 $$\pi(. \vert s)$$ 总是被建模为给定当前状态下动作 $$\mathcal{A}$$ 上的概率分布，因此是*随机*的。**确定性策略梯度（Deterministic policy gradient，DPG）**则把策略建模为一个确定性的决策：$$a = \mu(s)$$。这看起来有点奇怪——当策略只输出单个动作时，你怎么计算动作概率的梯度呢？让我们一步步来看。

先回顾几个便于讨论的符号：
* $$\rho_0(s)$$：状态的初始分布。
* $$\rho^\mu(s \to s', k)$$：从状态 s 出发，按策略 $$\mu$$ 移动 k 步后在状态 s' 的访问概率密度。
* $$\rho^\mu(s')$$：折扣状态分布，定义为 $$\rho^\mu(s') = \int_\mathcal{S} \sum_{k=1}^\infty \gamma^{k-1} \rho_0(s) \rho^\mu(s \to s', k) ds$$。

要优化的目标函数如下：

$$
J(\theta) = \int_\mathcal{S} \rho^\mu(s) Q(s, \mu_\theta(s)) ds
$$

**确定性策略梯度定理**：现在是计算梯度的时候了！按照链式法则，我们先对 Q 关于动作 a 求梯度，再对确定性策略函数 $$\mu$$ 关于 $$\theta$$ 求梯度：


$$
\begin{aligned}
\nabla_\theta J(\theta) 
&= \int_\mathcal{S} \rho^\mu(s) \nabla_a Q^\mu(s, a) \nabla_\theta \mu_\theta(s) \rvert_{a=\mu_\theta(s)} ds \\
&= \mathbb{E}_{s \sim \rho^\mu} [\nabla_a Q^\mu(s, a) \nabla_\theta \mu_\theta(s) \rvert_{a=\mu_\theta(s)}]
\end{aligned}
$$

我们可以把确定性策略视为随机策略的*特例*——当概率分布在某一个动作上只包含一个非零的极值时。事实上，在 DPG [论文](https://hal.inria.fr/file/index/docid/938992/filename/dpg-icml2014.pdf)中，作者已经证明：如果随机策略 $$\pi_{\mu_\theta, \sigma}$$ 由确定性策略 $$\mu_\theta$$ 和一个方差变量 $$\sigma$$ 重参数化，那么当 $$\sigma=0$$ 时随机策略最终等价于确定性情形。与确定性策略相比，我们预期随机策略需要更多样本，因为它要在整个状态和动作空间上对数据做积分。

确定性策略梯度定理可以嵌入常见的策略梯度框架。

考虑一个同策略 actor-critic 算法的例子来展示流程。在同策略 actor-critic 的每次迭代中，两个动作都确定性地选取 $$a = \mu_\theta(s)$$，策略参数上的 [SARSA](https://lilianweng.github.io/posts/2018-02-19-rl-overview/#sarsa-on-policy-td-control) 更新依赖于我们刚才算出的新梯度：


$$
\begin{aligned}
\delta_t &= R_t + \gamma Q_w(s_{t+1}, a_{t+1}) - Q_w(s_t, a_t) & \scriptstyle{\text{; TD error in SARSA}}\\
w_{t+1} &= w_t + \alpha_w \delta_t \nabla_w Q_w(s_t, a_t) & \\
\theta_{t+1} &= \theta_t + \alpha_\theta \color{red}{\nabla_a Q_w(s_t, a_t) \nabla_\theta \mu_\theta(s) \rvert_{a=\mu_\theta(s)}} & \scriptstyle{\text{; Deterministic policy gradient theorem}}
\end{aligned}
$$

然而，除非环境中有足够的噪声，由于策略的确定性，很难保证充分的[探索](https://lilianweng.github.io/posts/2018-02-19-rl-overview/#exploration-exploitation-dilemma)。我们可以给策略加噪声（讽刺的是这让它变得非确定！），或者按离策略方式学习：遵循另一个不同的随机行为策略来收集样本。

比如在离策略方法中，训练轨迹由随机策略 $$\beta(a \vert s)$$ 生成，因此状态分布遵循相应的折扣状态密度 $$\rho^\beta$$：


$$
\begin{aligned}
J_\beta(\theta) &= \int_\mathcal{S} \rho^\beta Q^\mu(s, \mu_\theta(s)) ds \\
\nabla_\theta J_\beta(\theta) &= \mathbb{E}_{s \sim \rho^\beta} [\nabla_a Q^\mu(s, a) \nabla_\theta \mu_\theta(s)  \rvert_{a=\mu_\theta(s)} ]
\end{aligned}
$$

注意因为策略是确定性的，我们只需要 $$Q^\mu(s, \mu_\theta(s))$$ 而不是 $$\sum_a \pi(a \vert s) Q^\pi(s, a)$$ 作为给定状态 s 的估计奖励。
在使用随机策略的离策略方法中，通常用重要性采样来修正行为策略与目标策略之间的失配，如我们[上文](#off-policy-policy-gradient)所述。但由于确定性策略梯度消除了对动作的积分，我们可以避免重要性采样。

### DDPG

[[论文](https://arxiv.org/pdf/1509.02971.pdf)\|[代码](https://github.com/openai/baselines/tree/master/baselines/ddpg)]

**DDPG**（[Lillicrap, et al., 2015](https://arxiv.org/pdf/1509.02971.pdf)）是 **Deep Deterministic Policy Gradient** 的缩写，是一种无模型（model-free）的离策略 actor-critic 算法，将 [DPG](#dpg) 与 [DQN](https://lilianweng.github.io/posts/2018-02-19-rl-overview/#deep-q-network) 相结合。回忆 DQN（Deep Q-Network）通过经验回放和冻结的目标网络来稳定 Q 函数的学习。原始 DQN 工作在离散空间，DDPG 借助 actor-critic 框架把它扩展到连续空间，同时学习一个确定性策略。

为了做更好的探索，通过加噪声 $$\mathcal{N}$$ 构造一个探索策略 $$\mu'$$：

$$
\mu'(s) = \mu_\theta(s) + \mathcal{N}
$$

此外，DDPG 对 actor 和 critic 的参数都做软更新（"conservative policy iteration"），$$\tau \ll 1$$：$$\theta' \leftarrow \tau \theta + (1 - \tau) \theta'$$。这样目标网络的值被约束为缓慢变化，不同于 DQN 中目标网络在一段时间内保持冻结的设计。

论文中一个对机器人特别有用的细节是关于如何归一化低维特征的不同物理量纲。例如，一个模型被设计为以机器人的位置和速度为输入学习策略；这些物理统计量本质上是不同的，甚至同类统计量在不同机器人之间也可能差异很大。论文用[批归一化](http://proceedings.mlr.press/v37/ioffe15.pdf)解决：在一个 minibatch 内跨样本归一化每个维度。

![DDPG](https://lilianweng.github.io/posts/2018-04-08-policy-gradient/DDPG_algo.png)

*图 3：DDPG 算法。（图片来源：[Lillicrap, et al., 2015](https://arxiv.org/pdf/1509.02971.pdf)）*

### D4PG

[[论文](https://openreview.net/forum?id=SyZipzbCb)\|代码（搜索 "github d4pg" 会找到几个。）]

**Distributed Distributional DDPG（D4PG）** 在 DDPG 上应用了一组改进，使其以分布式（distributional）方式运行。

(1) **分布式 Critic**：critic 把期望 Q 值估计为一个随机变量 ~ 由 $$w$$ 参数化的分布 $$Z_w$$，因此 $$Q_w(s, a) = \mathbb{E} Z_w(x, a)$$。学习分布参数的损失是最小化两个分布之间某种距离度量——分布式 TD 误差：$$L(w) = \mathbb{E}[d(\mathcal{T}_{\mu_\theta}, Z_{w'}(s, a), Z_w(s, a)]$$，其中 $$\mathcal{T}_{\mu_\theta}$$ 是 Bellman 算子。

确定性策略梯度更新变为：

$$
\begin{aligned}
\nabla_\theta J(\theta) 
&\approx \mathbb{E}_{\rho^\mu} [\nabla_a Q_w(s, a) \nabla_\theta \mu_\theta(s) \rvert_{a=\mu_\theta(s)}] & \scriptstyle{\text{; gradient update in DPG}} \\
&= \mathbb{E}_{\rho^\mu} [\mathbb{E}[\nabla_a Z_w(s, a)] \nabla_\theta \mu_\theta(s) \rvert_{a=\mu_\theta(s)}] & \scriptstyle{\text{; expectation of the Q-value distribution.}}
\end{aligned}
$$

(2) **$$N$$ 步回报**：计算 TD 误差时，D4PG 计算 $$N$$ 步 TD 目标而非一步，以纳入更远未来步的奖励。于是新的 TD 目标为：

$$
r(s_0, a_0) + \mathbb{E}[\sum_{n=1}^{N-1} r(s_n, a_n) + \gamma^N Q(s_N, \mu_\theta(s_N)) \vert s_0, a_0 ]
$$

(3) **多个分布式并行 Actor**：D4PG 使用 $$K$$ 个独立的 actor，并行收集经验并喂给同一个回放缓冲区。

(4) **优先经验回放（[PER](https://arxiv.org/abs/1511.05952)）**：最后一项修改是从大小为 $$R$$ 的回放缓冲区以非均匀概率 $$p_i$$ 采样。这样，样本 $$i$$ 以概率 $$(Rp_i)^{-1}$$ 被选中，因此重要性权重为 $$(Rp_i)^{-1}$$。

![DDPG](https://lilianweng.github.io/posts/2018-04-08-policy-gradient/D4PG_algo.png)

*图 4：D4PG 算法（图片来源：[Barth-Maron, et al. 2018](https://openreview.net/forum?id=SyZipzbCb)）；注意原论文中变量字母的选取与本文略有不同；即我用 $$\mu(.)$$ 而非 $$\pi(.)$$ 表示确定性策略。*

### MADDPG

[[论文](https://arxiv.org/pdf/1706.02275.pdf)\|[代码](https://github.com/openai/maddpg)]

**Multi-agent DDPG（MADDPG）**（[Lowe et al., 2017](https://arxiv.org/pdf/1706.02275.pdf)）把 DDPG 扩展到多个智能体仅凭局部信息协作完成任务的环境。从一个智能体的视角看，环境是非平稳的，因为其他智能体的策略在快速升级且保持未知。MADDPG 是专为应对这种变化的环境和智能体间交互而重新设计的 actor-critic 模型。

该问题可以用多智能体版的 MDP 形式化，也称*马尔可夫博弈（Markov games）*。MADDPG 针对部分可观测的马尔可夫博弈提出。设有 N 个智能体，状态集合为 $$\mathcal{S}$$。每个智能体拥有一个可能的动作集合 $$\mathcal{A}_1, \dots, \mathcal{A}_N$$ 和一个观测集合 $$\mathcal{O}_1, \dots, \mathcal{O}_N$$。状态转移函数涉及所有状态、动作和观测空间 $$\mathcal{T}: \mathcal{S} \times \mathcal{A}_1 \times \dots \mathcal{A}_N \mapsto \mathcal{S}$$。每个智能体的随机策略只涉及自己的状态和动作：$$\pi_{\theta_i}: \mathcal{O}_i \times \mathcal{A}_i \mapsto [0, 1]$$，是给定自身观测时动作上的概率分布；或者是确定性策略：$$\mu_{\theta_i}: \mathcal{O}_i \mapsto \mathcal{A}_i$$。

设 $$\vec{o} = {o_1, \dots, o_N}$$，$$\vec{\mu} = {\mu_1, \dots, \mu_N}$$，策略由 $$\vec{\theta} = {\theta_1, \dots, \theta_N}$$ 参数化。

MADDPG 中的 critic 为第 i 个智能体学习一个集中式（centralized）动作价值函数 $$Q^\vec{\mu}_i(\vec{o}, a_1, \dots, a_N)$$，其中 $$a_1 \in \mathcal{A}_1, \dots, a_N \in \mathcal{A}_N$$ 是所有智能体的动作。每个 $$Q^\vec{\mu}_i$$ 对 $$i=1, \dots, N$$ 分别独立学习，因此多个智能体可以有任意的奖励结构，包括竞争设定下相互冲突的奖励。同时，多个 actor（每个智能体一个）各自探索并升级策略参数 $$\theta_i$$。

**Actor 更新**：

$$
\nabla_{\theta_i} J(\theta_i) = \mathbb{E}_{\vec{o}, a \sim \mathcal{D}} [\nabla_{a_i} Q^{\vec{\mu}}_i (\vec{o}, a_1, \dots, a_N) \nabla_{\theta_i} \mu_{\theta_i}(o_i) \rvert_{a_i=\mu_{\theta_i}(o_i)} ]
$$

其中 $$\mathcal{D}$$ 是用于经验回放的内存缓冲区，包含多条情节样本 $$(\vec{o}, a_1, \dots, a_N, r_1, \dots, r_N, \vec{o}')$$ —— 给定当前观测 $$\vec{o}$$，智能体采取动作 $$a_1, \dots, a_N$$ 并获得奖励 $$r_1, \dots, r_N$$，产生新观测 $$\vec{o}'$$。

**Critic 更新**：

$$
\begin{aligned}
\mathcal{L}(\theta_i) &= \mathbb{E}_{\vec{o}, a_1, \dots, a_N, r_1, \dots, r_N, \vec{o}'}[ (Q^{\vec{\mu}}_i(\vec{o}, a_1, \dots, a_N) - y)^2 ] & \\
\text{where } y &= r_i + \gamma Q^{\vec{\mu}'}_i (\vec{o}', a'_1, \dots, a'_N) \rvert_{a'_j = \mu'_{\theta_j}} & \scriptstyle{\text{; TD target!}}
\end{aligned}
$$

其中 $$\vec{\mu}'$$ 是带延迟软更新参数的目标策略。

如果在 critic 更新期间策略 $$\vec{\mu}$$ 未知，我们可以让每个智能体学习并演化自己对其他智能体策略的近似。使用近似策略，MADDPG 仍然可以高效学习，尽管推断出的策略可能不精确。

为缓解环境中竞争或协作智能体之间交互引发的高方差，MADDPG 提出了又一个要素——*策略集成（policy ensembles）*：
1. 为一个智能体训练 K 个策略；
2. 情节回放时随机挑选一个策略；
3. 用这 K 个策略的集成做梯度更新。

总结：MADDPG 在 DDPG 之上增加了三项要素使其适应多智能体环境：
* 集中式 critic + 去中心化 actor；
* actor 能够使用其他智能体的估计策略来学习；
* 策略集成有利于降低方差。

![MADDPG](https://lilianweng.github.io/posts/2018-04-08-policy-gradient/MADDPG.png)

*图 5：MADDPG 的架构设计。（图片来源：[Lowe et al., 2017](https://arxiv.org/pdf/1706.02275.pdf)）*

### TRPO

[[论文](https://arxiv.org/pdf/1502.05477.pdf)\|[代码](https://github.com/openai/baselines/tree/master/baselines/trpo_mpi)]

为了提升训练稳定性，我们应避免一步之内改变策略过多的参数更新。**信赖域策略优化（Trust region policy optimization，TRPO）**（[Schulman, et al., 2015](https://arxiv.org/pdf/1502.05477.pdf)）通过在每次迭代对策略更新的大小施加 [KL 散度](https://lilianweng.github.io/posts/2017-08-20-gan/#kullbackleibler-and-jensenshannon-divergence)约束来实现这一想法。

考虑我们做离策略 RL 的情形：在 rollout worker 上收集轨迹所用的策略 $$\beta$$ 不同于要优化的策略 $$\pi$$。离策略模型中的目标函数度量状态访问分布与动作上的总优势，而训练数据分布与真实策略状态分布之间的失配由重要性采样估计器补偿：

$$
\begin{aligned}
J(\theta)
&= \sum_{s \in \mathcal{S}} \rho^{\pi_{\theta_\text{old}}} \sum_{a \in \mathcal{A}} \big( \pi_\theta(a \vert s) \hat{A}_{\theta_\text{old}}(s, a) \big) & \\
&= \sum_{s \in \mathcal{S}} \rho^{\pi_{\theta_\text{old}}} \sum_{a \in \mathcal{A}} \big( \beta(a \vert s) \frac{\pi_\theta(a \vert s)}{\beta(a \vert s)} \hat{A}_{\theta_\text{old}}(s, a) \big) & \scriptstyle{\text{; Importance sampling}} \\
&= \mathbb{E}_{s \sim \rho^{\pi_{\theta_\text{old}}}, a \sim \beta} \big[ \frac{\pi_\theta(a \vert s)}{\beta(a \vert s)} \hat{A}_{\theta_\text{old}}(s, a) \big] &
\end{aligned}
$$

其中 $$\theta_\text{old}$$ 是更新前的策略参数，因而是已知的；$$\rho^{\pi_{\theta_\text{old}}}$$ 的定义与[上文](#dpg)相同；$$\beta(a \vert s)$$ 是收集轨迹的行为策略。注意我们使用估计的优势 $$\hat{A}(.)$$ 而非真实优势函数 $$A(.)$$，因为真实奖励通常未知。

同策略训练时，理论上收集数据的策略与我们要优化的策略相同。然而，当 rollout worker 和优化器并行异步运行时，行为策略可能过时。TRPO 考虑了这一微妙差异：它把行为策略标记为 $$\pi_{\theta_\text{old}}(a \vert s)$$，于是目标函数变为：

$$
J(\theta) = \mathbb{E}_{s \sim \rho^{\pi_{\theta_\text{old}}}, a \sim \pi_{\theta_\text{old}}} \big[ \frac{\pi_\theta(a \vert s)}{\pi_{\theta_\text{old}}(a \vert s)} \hat{A}_{\theta_\text{old}}(s, a) \big]
$$

TRPO 旨在最大化目标函数 $$J(\theta)$$，同时满足*信赖域约束*——它强制新旧策略之间用 [KL 散度](https://en.wikipedia.org/wiki/Kullback%E2%80%93Leibler_divergence)度量的距离足够小，在参数 δ 之内：

$$
\mathbb{E}_{s \sim \rho^{\pi_{\theta_\text{old}}}} [D_\text{KL}(\pi_{\theta_\text{old}}(.\vert s) \| \pi_\theta(.\vert s)] \leq \delta
$$

这样，当这一硬约束被满足时，新旧策略就不会相差太远。同时，TRPO 仍能保证对策略迭代的单调改进（很妙，对吧？）。感兴趣的话请阅读[论文](https://arxiv.org/pdf/1502.05477.pdf)中的证明 :)

### PPO

[[论文](https://arxiv.org/pdf/1707.06347.pdf)\|[代码](https://github.com/openai/baselines/tree/master/baselines/ppo1)]

鉴于 TRPO 相对复杂而我们仍想实现类似的约束，**近端策略优化（proximal policy optimization，PPO）**用截断的替代目标将其简化，同时保持相近的性能。

首先，把新旧策略之间的概率比记为：

$$
r(\theta) = \frac{\pi_\theta(a \vert s)}{\pi_{\theta_\text{old}}(a \vert s)}
$$

于是 TRPO（同策略）的目标函数变为：

$$
J^\text{TRPO} (\theta) = \mathbb{E} [ r(\theta) \hat{A}_{\theta_\text{old}}(s, a) ]
$$

<a name="ppo_loss" />若不对 $$\theta_\text{old}$$ 与 $$\theta$$ 之间的距离加以限制，最大化 $$J^\text{TRPO} (\theta)$$ 会因极端巨大的参数更新和策略比值而导致不稳定。PPO 通过强制 $$r(\theta)$$ 保持在 1 附近的小区间内施加约束，确切地说是 $$[1-\epsilon, 1+\epsilon]$$，其中 $$\epsilon$$ 是一个超参数。

$$
J^\text{CLIP} (\theta) = \mathbb{E} [ \min( r(\theta) \hat{A}_{\theta_\text{old}}(s, a), \text{clip}(r(\theta), 1 - \epsilon, 1 + \epsilon) \hat{A}_{\theta_\text{old}}(s, a))]
$$

函数 $$\text{clip}(r(\theta), 1 - \epsilon, 1 + \epsilon)$$ 把比值截断为不超过 $$1+\epsilon$$、不低于 $$1-\epsilon$$。PPO 的目标函数在原始值与截断版本之间取较小者，因此我们失去了把策略更新推向极端以获取更高奖励的动机。

当 PPO 应用在策略（actor）与价值（critic）函数共享参数的网络架构上时，除截断奖励外，目标函数还增加了价值估计的误差项（红色公式）和熵项（蓝色公式）以鼓励充分探索。

$$
J^\text{CLIP'} (\theta) = \mathbb{E} [ J^\text{CLIP} (\theta) - \color{red}{c_1 (V_\theta(s) - V_\text{target})^2} + \color{blue}{c_2 H(s, \pi_\theta(.))} ]
$$

其中 $$c_1$$ 和 $$c_2$$ 是两个超参数常数。

PPO 已在一组基准任务上测试，并被证明以简单得多的方式产生了出色的结果。

在 [Hsu et al., 2020](https://arxiv.org/abs/2009.10897) 的后续论文中，重新审视了 PPO 的两个常见设计选择，确切地说是 (1) 用于策略正则化的截断概率比，以及 (2) 用连续高斯或离散 softmax 分布参数化策略动作空间。他们首先识别出 PPO 的三种失效模式，并对这两种设计提出了替代方案。

失效模式有：
1. 在连续动作空间上，当奖励在有界支撑之外消失时，标准 PPO 不稳定。
2. 在稀疏高奖励的离散动作空间上，标准 PPO 常常卡在次优动作上。
3. 当初始化附近存在局部最优动作时，策略对初始化敏感。

离散化动作空间或使用 Beta 分布有助于避免与高斯策略相关的失效模式 1 和 3。使用 KL 正则化（与 [TRPO](#trpo) 动机相同）作为替代代理模型有助于解决失效模式 1 和 2。

![PPG](https://lilianweng.github.io/posts/2018-04-08-policy-gradient/ppo-loss-functions.png)

### PPG

[[论文](https://arxiv.org/abs/2009.04416)\|[代码](https://github.com/openai/phasic-policy-gradient)]

在策略网络与价值网络之间共享参数有利有弊。它允许策略和价值函数共享学习到的特征，但可能导致相互竞争的目标之间的冲突，并要求同时训练两个网络时使用相同的数据。**Phasic policy gradient（PPG**；[Cobbe, et al 2020](https://arxiv.org/abs/2009.04416)）修改了传统的同策略 [actor-critic](#actor-critic) 策略梯度算法——确切地说是 [PPO](#ppo)——为策略和价值函数设置分开的训练阶段。在两个交替的阶段中：
1. *策略阶段*：通过优化 PPO [目标](#ppo_loss) $$L^\text{CLIP} (\theta)$$ 更新策略网络；
2. *辅助阶段*：在行为克隆损失之外优化一个辅助目标。论文中价值函数误差是唯一的辅助目标，但它可以很泛化，包含任何其他额外的辅助损失。

$$
\begin{aligned}
L^\text{joint} &= L^\text{aux} + \beta_\text{clone} \cdot \mathbb{E}_t[\text{KL}[\pi_{\theta_\text{old}}(\cdot\mid s_t), \pi_\theta(\cdot\mid s_t)]] \\
L^\text{aux} &= L^\text{value} = \mathbb{E}_t \big[\frac{1}{2}\big( V_w(s_t) - \hat{V}_t^\text{targ} \big)^2\big]
\end{aligned}
$$

其中 $$\beta_\text{clone}$$ 是一个超参数，控制在优化辅助目标时我们希望策略偏离原行为多少。

![PPG](https://lilianweng.github.io/posts/2018-04-08-policy-gradient/PPG_algo.png)

*图 6：PPG 算法。（图片来源：[Cobbe, et al 2020](https://arxiv.org/abs/2009.04416)）*

其中
- $$N_\pi$$ 是策略阶段中策略更新迭代的次数。注意策略阶段在单个辅助阶段之间执行多轮迭代更新。
- $$E_\pi$$ 和 $$E_V$$ 分别控制策略函数和价值函数的样本复用（即对回放缓冲区中数据执行的训练轮数）。注意这发生在策略阶段内，因此 $$E_V$$ 影响的是真实价值函数而非辅助价值函数的学习。
- $$E_\text{aux}$$ 定义辅助阶段中的样本复用。在 PPG 中，价值函数优化能容忍高得多的样本复用；例如论文的实验中，$$E_\text{aux} = 6$$ 而 $$E_\pi = E_V = 1$$。

相比 PPO，PPG 带来了样本效率上的显著提升。

![PPG](https://lilianweng.github.io/posts/2018-04-08-policy-gradient/PPG_exp.png)

*图 7：PPG 与 PPO 在 [Procgen](https://arxiv.org/abs/1912.01588) 基准上的平均归一化性能。（图片来源：[Cobbe, et al 2020](https://arxiv.org/abs/2009.04416)）*

### ACER

[[论文](https://arxiv.org/pdf/1611.01224.pdf)\|[代码](https://github.com/openai/baselines/tree/master/baselines/acer)]

**ACER** 是 **actor-critic with experience replay**（[Wang, et al., 2017](https://arxiv.org/pdf/1611.01224.pdf)）的缩写，是一个带经验回放的离策略 actor-critic 模型，大幅提升了样本效率并降低了数据相关性。A3C 为 ACER 奠定了基础，但它是同策略的；ACER 是 A3C 的离策略对应版本。把 A3C 变成离策略的主要障碍是如何控制离策略估计器的稳定性。ACER 提出三个设计来克服它：
* 使用 Retrace Q 值估计；
* 截断重要性权重并做偏差修正；
* 应用高效的 TRPO。

**Retrace Q 值估计**

[*Retrace*](http://papers.nips.cc/paper/6538-safe-and-efficient-off-policy-reinforcement-learning.pdf) 是一种基于回报的离策略 Q 值估计算法，对任意目标策略与行为策略对 $$(\pi, \beta)$$ 都有良好的收敛保证，外加不错的数据效率。

回顾 TD 学习如何做预测：
1. 计算 TD 误差：$$\delta_t = R_t + \gamma \mathbb{E}_{a \sim \pi} Q(S_{t+1}, a) - Q(S_t, A_t)$$；项 $$r_t + \gamma \mathbb{E}_{a \sim \pi} Q(s_{t+1}, a) $$ 被称为 "TD 目标"。使用期望 $$\mathbb{E}_{a \sim \pi}$$ 是因为对于未来步，我们能做出的最好估计是遵循当前策略 $$\pi$$ 时的回报。
2. 通过向目标修正误差来更新价值：$$Q(S_t, A_t) \leftarrow Q(S_t, A_t) + \alpha \delta_t$$。换言之，Q 的增量更新与 TD 误差成正比：$$\Delta Q(S_t, A_t) = \alpha \delta_t$$。

当 rollout 是离策略时，我们需要在 Q 更新上应用重要性采样：

$$
\Delta Q^\text{imp}(S_t, A_t) 
= \gamma^t \prod_{1 \leq \tau \leq t} \frac{\pi(A_\tau \vert S_\tau)}{\beta(A_\tau \vert S_\tau)} \delta_t
$$

当我们开始想象重要性权重的乘积如何导致超高方差甚至爆炸时，它看起来相当吓人。Retrace Q 值估计方法修改 $$\Delta Q$$，使重要性权重被截断为不超过常数 $$c$$：

$$
\Delta Q^\text{ret}(S_t, A_t) 
= \gamma^t \prod_{1 \leq \tau \leq t} \min(c, \frac{\pi(A_\tau \vert S_\tau)}{\beta(A_\tau \vert S_\tau)})  \delta_t
$$

ACER 用 $$Q^\text{ret}$$ 作为目标，通过最小化 L2 误差项 $$(Q^\text{ret}(s, a) - Q(s, a))^2$$ 来训练 critic。

**重要性权重截断**

为降低策略梯度 $$\hat{g}$$ 的高方差，ACER 用常数 c 截断重要性权重，并附加一个修正项。标记 $$\hat{g}_t^\text{acer}$$ 为时间 t 的 ACER 策略梯度。

$$
\begin{aligned}
\hat{g}_t^\text{acer}
= & \omega_t \big( Q^\text{ret}(S_t, A_t) - V_{\theta_v}(S_t) \big) \nabla_\theta \ln \pi_\theta(A_t \vert S_t) 
  & \scriptstyle{\text{; Let }\omega_t=\frac{\pi(A_t \vert S_t)}{\beta(A_t \vert S_t)}} \\
= & \color{blue}{\min(c, \omega_t) \big( Q^\text{ret}(S_t, A_t) - V_w(S_t) \big) \nabla_\theta \ln \pi_\theta(A_t \vert S_t)} \\
  & + \color{red}{\mathbb{E}_{a \sim \pi} \big[ \max(0, \frac{\omega_t(a) - c}{\omega_t(a)}) \big( Q_w(S_t, a) - V_w(S_t) \big) \nabla_\theta \ln \pi_\theta(a \vert S_t) \big]}
  & \scriptstyle{\text{; Let }\omega_t (a) =\frac{\pi(a \vert S_t)}{\beta(a \vert S_t)}}
\end{aligned}
$$

其中 $$Q_w(.)$$ 和 $$V_w(.)$$ 是参数为 w 的 critic 预测的价值函数。第一项（蓝色）包含截断的重要性权重。截断有助于降低方差，此外还减去状态价值函数 $$V_w(.)$$ 作为基线。第二项（红色）做修正以实现无偏估计。

**高效 TRPO**

此外，ACER 采纳了 TRPO 的思想但做了小调整使其计算更高效：不是度量一次更新前后策略之间的 KL 散度，ACER 维护过去策略的滑动平均，并强制更新后的策略不偏离这个平均太远。

ACER [论文](https://arxiv.org/pdf/1611.01224.pdf)内容密集、公式很多。希望凭借 TD 学习、Q-learning、重要性采样和 TRPO 的前置知识，你会发现[论文](https://arxiv.org/pdf/1611.01224.pdf)读起来稍微轻松一些 :)

### ACKTR

[[论文](https://arxiv.org/pdf/1708.05144.pdf)\|[代码](https://github.com/openai/baselines/tree/master/baselines/acktr)]

**ACKTR（actor-critic using Kronecker-factored trust region）**（[Yuhuai Wu, et al., 2017](https://arxiv.org/pdf/1708.05144.pdf)）提出使用 Kronecker 分解近似曲率（[K-FAC](https://arxiv.org/pdf/1503.05671.pdf)）对 critic 和 actor 做梯度更新。K-FAC 改进了*自然梯度*的计算，它与我们的*标准梯度*颇为不同。[这里](http://kvfrans.com/a-intuitive-explanation-of-natural-gradient-descent/)有一个关于自然梯度的好而直观的解释。一句话概括大概是：

> "我们首先考虑能产生与旧网络相距恒定 KL 散度的新网络的所有参数组合。这个恒定值可以视为步长或学习率。在所有这些可能的组合中，我们选择使损失函数最小的那一个。"

我把 ACTKR 列在这里主要是为了本文的完整性，但不会深入细节，因为它涉及大量关于自然梯度和优化方法的理论知识。如果感兴趣，在读 ACKTR 论文之前请先看这些论文/文章：
* Amari. [Natural Gradient Works Efficiently in Learning](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.452.7280&rep=rep1&type=pdf). 1998
* Kakade. [A Natural Policy Gradient](https://papers.nips.cc/paper/2073-a-natural-policy-gradient.pdf). 2002
* [A intuitive explanation of natural gradient descent](http://kvfrans.com/a-intuitive-explanation-of-natural-gradient-descent/)
* [Wiki: Kronecker product](https://en.wikipedia.org/wiki/Kronecker_product)
* Martens & Grosse. [Optimizing neural networks with kronecker-factored approximate curvature.](http://proceedings.mlr.press/v37/martens15.pdf) 2015.

以下是 K-FAC [论文](https://arxiv.org/pdf/1503.05671.pdf)的一个高层总结：

> "这一近似分两个阶段构建。第一阶段，Fisher 矩阵的行和列被分组，每组对应某一层的全部权重，由此产生矩阵的块分割。然后这些块被近似为小得多的矩阵之间的 Kronecker 积，我们表明这等价于对网络梯度统计量做某些近似假设。

> 第二阶段，该矩阵被进一步近似为拥有块对角或块三对角的逆。我们通过仔细考察逆协方差、树结构图模型与线性回归之间的关系来论证这一近似。值得注意的是，这一论证并不适用于 Fisher 矩阵本身，而我们的实验证实：虽然逆 Fisher 确实（近似）具备这种结构，Fisher 本身并不具备。"

### SAC

[[论文](https://arxiv.org/abs/1801.01290)\|[代码](https://github.com/haarnoja/sac)]

**Soft Actor-Critic（SAC）**（[Haarnoja et al. 2018](https://arxiv.org/abs/1801.01290)）把策略的熵度量纳入奖励以鼓励探索：我们期望学到一个尽可能随机行动、同时又仍能完成任务的策略。它是一个遵循最大熵强化学习框架的离策略 actor-critic 模型。前身工作是 [Soft Q-learning](https://arxiv.org/abs/1702.08165)。

SAC 的三个关键组件：
- 分离的策略与价值函数网络的 [actor-critic](#actor-critic) 架构；
- 能够复用先前收集数据以提升效率的[离策略](#off-policy-policy-gradient)表述；
- 熵最大化，以获得稳定性与探索。

策略的训练目标是同时最大化期望回报和熵：

$$
J(\theta) = \sum_{t=1}^T \mathbb{E}_{(s_t, a_t) \sim \rho_{\pi_\theta}} [r(s_t, a_t) + \alpha \mathcal{H}(\pi_\theta(.\vert s_t))]
$$

其中 $$\mathcal{H}(.)$$ 是熵度量，$$\alpha$$ 控制熵项的重要性，被称为*温度*参数。熵最大化带来的策略能够 (1) 更多探索，(2) 捕捉接近最优策略的多个模式（即，如果存在多个看起来同样好的选项，策略应赋予每个选项相等的被选概率）。

确切地说，SAC 旨在学习三个函数：
- 参数为 $$\theta$$ 的策略 $$\pi_\theta$$。
- 参数为 $$w$$ 的软 Q 值函数 $$Q_w$$。
- 参数为 $$\psi$$ 的软状态价值函数 $$V_\psi$$；理论上知道了 $$Q$$ 和 $$\pi$$ 就能推出 $$V$$，但实践中它有助于稳定训练。

软 Q 值和软状态价值定义为：

$$
\begin{aligned}
Q(s_t, a_t) &= r(s_t, a_t) + \gamma \mathbb{E}_{s_{t+1} \sim \rho_{\pi}(s)} [V(s_{t+1})] & \text{; according to Bellman equation.}\\
\text{where }V(s_t) &= \mathbb{E}_{a_t \sim \pi} [Q(s_t, a_t) - \alpha \log \pi(a_t \vert s_t)] & \text{; soft state value function.}
\end{aligned}
$$

$$
\text{Thus, } Q(s_t, a_t) = r(s_t, a_t) + \gamma \mathbb{E}_{(s_{t+1}, a_{t+1}) \sim \rho_{\pi}} [Q(s_{t+1}, a_{t+1}) - \alpha \log \pi(a_{t+1} \vert s_{t+1})]
$$

$$\rho_\pi(s)$$ 和 $$\rho_\pi(s, a)$$ 表示由策略 $$\pi(a \vert s)$$ 诱导的状态分布的状态边缘分布与状态-动作边缘分布；参见 [DPG](#dpg) 小节中的类似定义。

软状态价值函数的训练目标是最小化均方误差：

$$
\begin{aligned}
J_V(\psi) &= \mathbb{E}_{s_t \sim \mathcal{D}} [\frac{1}{2} \big(V_\psi(s_t) - \mathbb{E}[Q_w(s_t, a_t) - \log \pi_\theta(a_t \vert s_t)] \big)^2] \\
\text{with gradient: }\nabla_\psi J_V(\psi) &= \nabla_\psi V_\psi(s_t)\big( V_\psi(s_t) - Q_w(s_t, a_t) + \log \pi_\theta (a_t \vert s_t) \big)
\end{aligned}
$$

其中 $$\mathcal{D}$$ 是回放缓冲区。

软 Q 函数的训练目标是最小化软 Bellman 残差：

$$
\begin{aligned}
J_Q(w) &= \mathbb{E}_{(s_t, a_t) \sim \mathcal{D}} [\frac{1}{2}\big( Q_w(s_t, a_t) - (r(s_t, a_t) + \gamma \mathbb{E}_{s_{t+1} \sim \rho_\pi(s)}[V_{\bar{\psi}}(s_{t+1})]) \big)^2] \\
\text{with gradient: } \nabla_w J_Q(w) &= \nabla_w Q_w(s_t, a_t) \big( Q_w(s_t, a_t) - r(s_t, a_t) - \gamma V_{\bar{\psi}}(s_{t+1})\big) 
\end{aligned}
$$

其中 $$\bar{\psi}$$ 是目标价值函数，是指数滑动平均（或只以"硬"方式周期性更新），就像 [DQN](https://lilianweng.github.io/posts/2018-02-19-rl-overview/#deep-q-network) 中目标 Q 网络参数的处理方式一样，用以稳定训练。

SAC 更新策略以最小化 [KL 散度](https://en.wikipedia.org/wiki/Kullback%E2%80%93Leibler_divergence)：

$$
\begin{aligned}
\pi_\text{new} 
&= \arg\min_{\pi' \in \Pi} D_\text{KL} \Big( \pi'(.\vert s_t) \| \frac{\exp(Q^{\pi_\text{old}}(s_t, .))}{Z^{\pi_\text{old}}(s_t)} \Big) \\[6pt]
&= \arg\min_{\pi' \in \Pi} D_\text{KL} \big( \pi'(.\vert s_t) \| \exp(Q^{\pi_\text{old}}(s_t, .) - \log Z^{\pi_\text{old}}(s_t)) \big) \\[6pt]
\text{objective for update: } J_\pi(\theta) &= \nabla_\theta D_\text{KL} \big( \pi_\theta(. \vert s_t) \| \exp(Q_w(s_t, .) - \log Z_w(s_t)) \big) \\[6pt]
&= \mathbb{E}_{a_t\sim\pi} \Big[ - \log \big( \frac{\exp(Q_w(s_t, a_t) - \log Z_w(s_t))}{\pi_\theta(a_t \vert s_t)} \big) \Big] \\[6pt]
&= \mathbb{E}_{a_t\sim\pi} [ \log \pi_\theta(a_t \vert s_t) - Q_w(s_t, a_t) + \log Z_w(s_t) ]
\end{aligned}
$$

其中 $$\Pi$$ 是我们可以用来建模策略的候选策略集合，以保持可解性；例如 $$\Pi$$ 可以是高斯混合分布族，建模昂贵但表达力强且仍然可解。$$Z^{\pi_\text{old}}(s_t)$$ 是用于归一化分布的配分函数。它通常不可解，但不影响梯度。如何最小化 $$J_\pi(\theta)$$ 取决于我们对 $$\Pi$$ 的选择。

这一更新保证了 $$Q^{\pi_\text{new}}(s_t, a_t) \geq Q^{\pi_\text{old}}(s_t, a_t)$$，该引理的证明请看原[论文](https://arxiv.org/abs/1801.01290)附录 B.2。

一旦我们定义了软动作-状态价值、软状态价值和策略网络的目标函数与梯度，软 actor-critic 算法就直截了当了：

![SAC](https://lilianweng.github.io/posts/2018-04-08-policy-gradient/SAC_algo.png)

*图 8：软 actor-critic 算法。（图片来源：[原论文](https://arxiv.org/abs/1801.01290)）*

### 自动调节温度的 SAC

[[论文](https://arxiv.org/abs/1812.05905)\|[代码](https://github.com/rail-berkeley/softlearning)]

SAC 对温度参数很敏感。不幸的是温度很难调节，因为熵在不同任务之间以及训练过程中（随着策略变好）都会不可预测地变化。对 SAC 的一个改进将其表述为一个约束优化问题：在最大化期望回报的同时，策略应满足最小熵约束：

$$
\max_{\pi_0, \dots, \pi_T} \mathbb{E} \Big[ \sum_{t=0}^T r(s_t, a_t)\Big] \text{s.t. } \forall t\text{, } \mathcal{H}(\pi_t) \geq \mathcal{H}_0
$$

其中 $$\mathcal{H}_0$$ 是预定义的最小策略熵阈值。

期望回报 $$\mathbb{E} \Big[ \sum_{t=0}^T r(s_t, a_t)\Big]$$ 可以分解为所有时间步奖励之和。因为时间 t 的策略 $$\pi_t$$ 对更早时间步的策略 $$\pi_{t-1}$$ 没有影响，我们可以在时间上倒序地最大化不同步的回报——这本质上就是**动态规划（DP）**。

$$
\underbrace{\max_{\pi_0} \Big( \mathbb{E}[r(s_0, a_0)]+ \underbrace{\max_{\pi_1} \Big(\mathbb{E}[...] + \underbrace{\max_{\pi_T} \mathbb{E}[r(s_T, a_T)]}_\text{1st maximization} \Big)}_\text{second but last maximization} \Big)}_\text{last maximization}
$$

其中我们考虑 $$\gamma=1$$。

所以我们从最后一个时间步 $$T$$ 开始优化：

$$
\text{maximize } \mathbb{E}_{(s_T, a_T) \sim \rho_{\pi}} [ r(s_T, a_T) ] \text{ s.t. } \mathcal{H}(\pi_T) - \mathcal{H}_0 \geq 0
$$

首先，定义如下函数：

$$
\begin{aligned}
h(\pi_T) &= \mathcal{H}(\pi_T) - \mathcal{H}_0 = \mathbb{E}_{(s_T, a_T) \sim \rho_{\pi}} [-\log \pi_T(a_T\vert s_T)] - \mathcal{H}_0\\
f(\pi_T) &= \begin{cases}
\mathbb{E}_{(s_T, a_T) \sim \rho_{\pi}} [ r(s_T, a_T) ], & \text{if }h(\pi_T) \geq 0 \\
-\infty, & \text{otherwise}
\end{cases}
\end{aligned}
$$

于是优化变为：

$$
\text{maximize } f(\pi_T) \text{ s.t. } h(\pi_T) \geq 0
$$

要求解带不等式约束的最大化优化问题，可以构造带拉格朗日乘子（也称"对偶变量"）$$\alpha_T$$ 的[拉格朗日表达式](https://cs.stanford.edu/people/davidknowles/lagrangian_duality.pdf)：

$$
L(\pi_T, \alpha_T) = f(\pi_T) + \alpha_T h(\pi_T)
$$

考虑*关于 $$\alpha_T$$ 最小化 $$L(\pi_T, \alpha_T)$$* 的情形——给定某个特定的 $$\pi_T$$ 值：
- 若约束被满足，$$h(\pi_T) \geq 0$$，最好设 $$\alpha_T=0$$，因为我们无法控制 $$f(\pi_T)$$ 的值。于是 $$L(\pi_T, 0) = f(\pi_T)$$。
- 若约束被违反，$$h(\pi_T) < 0$$，取 $$\alpha_T \to \infty$$ 可使 $$L(\pi_T, \alpha_T) \to -\infty$$。于是 $$L(\pi_T, \infty) = -\infty = f(\pi_T)$$。

无论哪种情形，我们都能还原出以下方程，

$$
f(\pi_T) = \min_{\alpha_T \geq 0} L(\pi_T, \alpha_T)
$$

同时我们想最大化 $$f(\pi_T)$$，

$$
\max_{\pi_T} f(\pi_T) = \min_{\alpha_T \geq 0} \max_{\pi_T} L(\pi_T, \alpha_T)
$$

因此，为最大化 $$f(\pi_T)$$，对偶问题列出如下。注意为确保 $$\max_{\pi_T} f(\pi_T)$$ 被恰当地最大化而不变成 $$-\infty$$，约束必须被满足。

$$
\begin{aligned}
\max_{\pi_T} \mathbb{E}[ r(s_T, a_T) ]
&= \max_{\pi_T} f(\pi_T) \\
&= \min_{\alpha_T \geq 0}  \max_{\pi_T} L(\pi_T, \alpha_T) \\
&= \min_{\alpha_T \geq 0}  \max_{\pi_T} f(\pi_T) + \alpha_T h(\pi_T) \\ 
&= \min_{\alpha_T \geq 0}  \max_{\pi_T} \mathbb{E}_{(s_T, a_T) \sim \rho_{\pi}} [ r(s_T, a_T) ] + \alpha_T ( \mathbb{E}_{(s_T, a_T) \sim \rho_{\pi}} [-\log \pi_T(a_T\vert s_T)] - \mathcal{H}_0) \\ 
&= \min_{\alpha_T \geq 0}  \max_{\pi_T} \mathbb{E}_{(s_T, a_T) \sim \rho_{\pi}} [ r(s_T, a_T)  - \alpha_T \log \pi_T(a_T\vert s_T)] - \alpha_T \mathcal{H}_0 \\
&= \min_{\alpha_T \geq 0}  \max_{\pi_T} \mathbb{E}_{(s_T, a_T) \sim \rho_{\pi}} [ r(s_T, a_T)  + \alpha_T \mathcal{H}(\pi_T) - \alpha_T \mathcal{H}_0 ]
\end{aligned}
$$

我们可以迭代地计算最优的 $$\pi_T$$ 和 $$\alpha_T$$。首先给定当前的 $$\alpha_T$$，求最大化 $$L(\pi_T^{*}, \alpha_T)$$ 的最佳策略 $$\pi_T^{*}$$。然后代入 $$\pi_T^{*}$$，求最小化 $$L(\pi_T^{*}, \alpha_T)$$ 的 $$\alpha_T^{*}$$。假设我们用一个神经网络表示策略、一个网络表示温度参数，这一迭代更新过程更贴合我们训练时更新网络参数的方式。

$$
\begin{aligned}
\pi^{*}_T
&= \arg\max_{\pi_T} \mathbb{E}_{(s_T, a_T) \sim \rho_{\pi}} [ r(s_T, a_T)  + \alpha_T \mathcal{H}(\pi_T) - \alpha_T \mathcal{H}_0 ] \\
\color{blue}{\alpha^{*}_T}
&\color{blue}{=} \color{blue}{\arg\min_{\alpha_T \geq 0} \mathbb{E}_{(s_T, a_T) \sim \rho_{\pi^{*}}} [\alpha_T \mathcal{H}(\pi^{*}_T) - \alpha_T \mathcal{H}_0 ]}
\end{aligned}
$$

$$
\text{Thus, }\max_{\pi_T} \mathbb{E} [ r(s_T, a_T) ] 
= \mathbb{E}_{(s_T, a_T) \sim \rho_{\pi^{*}}} [ r(s_T, a_T)  + \alpha^{*}_T \mathcal{H}(\pi^{*}_T) - \alpha^{*}_T \mathcal{H}_0 ]
$$

现在回到软 Q 值函数：

$$
\begin{aligned}
Q_{T-1}(s_{T-1}, a_{T-1}) 
&= r(s_{T-1}, a_{T-1}) + \mathbb{E} [Q(s_T, a_T) - \alpha_T \log \pi(a_T \vert s_T)] \\
&= r(s_{T-1}, a_{T-1}) + \mathbb{E} [r(s_T, a_T)] + \alpha_T \mathcal{H}(\pi_T) \\
Q_{T-1}^{*}(s_{T-1}, a_{T-1}) 
&= r(s_{T-1}, a_{T-1}) + \max_{\pi_T} \mathbb{E} [r(s_T, a_T)] +  \alpha_T \mathcal{H}(\pi^{*}_T) & \text{; plug in the optimal }\pi_T^{*}
\end{aligned}
$$

因此，当我们再往回退一步到时间步 $$T-1$$ 时，期望回报如下：

$$
\begin{aligned}
&\max_{\pi_{T-1}}\Big(\mathbb{E}[r(s_{T-1}, a_{T-1})] + \max_{\pi_T} \mathbb{E}[r(s_T, a_T] \Big) \\
&= \max_{\pi_{T-1}} \Big( Q^{*}_{T-1}(s_{T-1}, a_{T-1}) - \alpha^{*}_T \mathcal{H}(\pi^{*}_T) \Big) & \text{; should s.t. } \mathcal{H}(\pi_{T-1}) - \mathcal{H}_0 \geq 0 \\
&= \min_{\alpha_{T-1} \geq 0}  \max_{\pi_{T-1}} \Big( Q^{*}_{T-1}(s_{T-1}, a_{T-1}) - \alpha^{*}_T \mathcal{H}(\pi^{*}_T) + \alpha_{T-1} \big( \mathcal{H}(\pi_{T-1}) - \mathcal{H}_0 \big) \Big) & \text{; dual problem w/ Lagrangian.} \\
&= \min_{\alpha_{T-1} \geq 0}  \max_{\pi_{T-1}} \Big( Q^{*}_{T-1}(s_{T-1}, a_{T-1}) + \alpha_{T-1} \mathcal{H}(\pi_{T-1}) - \alpha_{T-1}\mathcal{H}_0 \Big) - \alpha^{*}_T \mathcal{H}(\pi^{*}_T)
\end{aligned}
$$

与前一步类似，

$$
\begin{aligned}
\pi^{*}_{T-1} &= \arg\max_{\pi_{T-1}} \mathbb{E}_{(s_{T-1}, a_{T-1}) \sim \rho_\pi} [Q^{*}_{T-1}(s_{T-1}, a_{T-1}) + \alpha_{T-1} \mathcal{H}(\pi_{T-1}) - \alpha_{T-1} \mathcal{H}_0 ] \\
\color{green}{\alpha^{*}_{T-1}} &\color{green}{=} \color{green}{\arg\min_{\alpha_{T-1} \geq 0} \mathbb{E}_{(s_{T-1}, a_{T-1}) \sim \rho_{\pi^{*}}} [ \alpha_{T-1} \mathcal{H}(\pi^{*}_{T-1}) - \alpha_{T-1}\mathcal{H}_0 ]}
\end{aligned}
$$

<span style="color: #32CD32;">绿色</span>的更新 $$\alpha_{T-1}$$ 的方程与上面<span style="color: #1E90FF;">蓝色</span>的更新 $$\alpha_{T-1}$$ 的方程格式相同。通过重复这一过程，我们可以在每一步通过最小化同一目标函数来学习最优温度参数：

$$
J(\alpha) = \mathbb{E}_{a_t \sim \pi_t} [-\alpha \log \pi_t(a_t \mid s_t) - \alpha \mathcal{H}_0]
$$

最终算法与 SAC 相同，只是显式地按目标 $$J(\alpha)$$ 学习 $$\alpha$$（见图 7）：

![SAC2](https://lilianweng.github.io/posts/2018-04-08-policy-gradient/SAC2_algo.png)

*图 9：带自动调节温度的软 actor-critic 算法。（图片来源：[原论文](https://arxiv.org/abs/1812.05905)）*

### TD3

[[论文](https://arxiv.org/abs/1802.09477)\|[代码](https://github.com/sfujim/TD3)]

众所周知，Q-learning 算法常受价值函数过高估计之苦。这种过高估计会随训练迭代传播并对策略产生负面影响。这一性质直接催生了 [Double Q-learning](https://papers.nips.cc/paper/3964-double-q-learning) 和 [Double DQN](https://arxiv.org/abs/1509.06461)：通过使用两个价值网络，把动作选择与 Q 值更新解耦。

**Twin Delayed Deep Deterministic**（简称 **TD3**；[Fujimoto et al., 2018](https://arxiv.org/abs/1802.09477)）在 [DDPG](#ddpg) 上应用了几项技巧以防止价值函数的过高估计：

(1) **截断双 Q 学习（Clipped Double Q-learning）**：在 Double Q-Learning 中，动作选择和 Q 值估计由两个网络分别做出。在 DDPG 设定下，给定两个确定性 actor $$(\mu_{\theta_1}, \mu_{\theta_2})$$ 和两个相应的 critic $$(Q_{w_1}, Q_{w_2})$$，Double Q-learning 的 Bellman 目标形如：

$$
\begin{aligned}
y_1 &= r + \gamma Q_{w_2}(s', \mu_{\theta_1}(s'))\\
y_2 &= r + \gamma Q_{w_1}(s', \mu_{\theta_2}(s'))
\end{aligned}
$$

然而，由于策略变化缓慢，这两个网络可能过于相似而无法做出独立的决策。*截断双 Q 学习*改为取两者中较小的估计，从而偏好低估偏差——它很难在训练中传播：

$$
\begin{aligned}
y_1 &= r + \gamma \min_{i=1,2}Q_{w_i}(s', \mu_{\theta_1}(s'))\\
y_2 &= r + \gamma \min_{i=1,2} Q_{w_i}(s', \mu_{\theta_2}(s'))
\end{aligned}
$$

(2) **目标网络与策略网络的延迟更新**：在 [actor-critic](https://lilianweng.github.io/posts/2018-02-19-rl-overview/#actor-critic) 模型中，策略与价值的更新深度耦合：当策略很差时，价值估计会因过高估计而发散；而价值估计本身不准时，策略也会变差。

为降低方差，TD3 以低于 Q 函数的频率更新策略。策略网络保持不变，直到若干次更新后价值误差足够小。这个思想类似于 [DQN](https://lilianweng.github.io/posts/2018-02-19-rl-overview/#dqn) 中周期更新的目标网络作为稳定目标。

(3) **目标策略平滑**：鉴于确定性策略可能对价值函数中的窄峰过拟合，TD3 在价值函数上引入了平滑正则化策略：对被选中的动作添加少量截断的随机噪声，并在 mini-batch 上取平均。

$$
\begin{aligned}
y &= r + \gamma Q_w (s', \mu_{\theta}(s') + \epsilon) & \\
\epsilon &\sim \text{clip}(\mathcal{N}(0, \sigma), -c, +c) & \scriptstyle{\text{ ; clipped random noises.}}
\end{aligned}
$$

这一做法模仿了 [SARSA](https://lilianweng.github.io/posts/2018-02-19-rl-overview/#sarsa-on-policy-td-control) 更新的思想，强制相似的动作具有相似的价值。

最终算法如下：

![TD3](https://lilianweng.github.io/posts/2018-04-08-policy-gradient/TD3.png)

*图 10：TD3 算法。（图片来源：[Fujimoto et al., 2018](https://arxiv.org/abs/1802.09477)）*

### SVPG

[[论文](https://arxiv.org/abs/1704.02399)\|[SVPG 代码](https://github.com/dilinwang820/Stein-Variational-Gradient-Descent)]

Stein 变分策略梯度（**SVPG**；[Liu et al, 2017](https://arxiv.org/abs/1704.02399)）应用 [Stein](https://www.cs.dartmouth.edu/~qliu/stein.html) 变分梯度下降（**SVGD**；[Liu and Wang, 2016](https://arxiv.org/abs/1608.04471)）算法来更新策略参数 $$\theta$$。

在最大熵策略优化的设定下，$$\theta$$ 被视为随机变量 $$\theta \sim q(\theta)$$，模型期望学到这个分布 $$q(\theta)$$。假设我们知道 $$q$$ 可能形态的先验 $$q_0$$，我们希望通过优化以下目标函数来引导学习过程，使 $$\theta$$ 不至于离 $$q_0$$ 太远：

$$
\hat{J}(\theta) = \mathbb{E}_{\theta \sim q} [J(\theta)] - \alpha D_\text{KL}(q\|q_0)
$$

其中 $$\mathbb{E}_{\theta \sim q} [R(\theta)]$$ 是 $$\theta \sim q(\theta)$$ 时的期望奖励，$$D_\text{KL}$$ 是 KL 散度。

如果我们没有任何先验信息，可以把 $$q_0$$ 设为均匀分布，即 $$q_0(\theta)$$ 为常数。于是上述目标函数就变成了 [SAC](#SAC)，其中熵项鼓励探索：

$$
\begin{aligned}
\hat{J}(\theta) 
&= \mathbb{E}_{\theta \sim q} [J(\theta)] - \alpha D_\text{KL}(q\|q_0) \\
&= \mathbb{E}_{\theta \sim q} [J(\theta)] - \alpha \mathbb{E}_{\theta \sim q} [\log q(\theta) - \log q_0(\theta)] \\
&= \mathbb{E}_{\theta \sim q} [J(\theta)] + \alpha H(q(\theta))
\end{aligned}
$$

对 $$\hat{J}(\theta) = \mathbb{E}_{\theta \sim q} [J(\theta)] - \alpha D_\text{KL}(q\|q_0)$$ 关于 $$q$$ 求导：

$$
\begin{aligned}
\nabla_q \hat{J}(\theta) 
&= \nabla_q \big( \mathbb{E}_{\theta \sim q} [J(\theta)] - \alpha D_\text{KL}(q\|q_0) \big) \\
&= \nabla_q \int_\theta \big( q(\theta) J(\theta) - \alpha q(\theta)\log q(\theta) + \alpha q(\theta) \log q_0(\theta) \big) \\
&= \int_\theta \big( J(\theta) - \alpha \log q(\theta) -\alpha + \alpha \log q_0(\theta) \big) \\
&= 0
\end{aligned}
$$

最优分布为：

$$
\log q^{*}(\theta) = \frac{1}{\alpha} J(\theta) + \log q_0(\theta) - 1 \text{ thus } \underbrace{ q^{*}(\theta) }_\textrm{"posterior"} \propto \underbrace{\exp ( J(\theta) / \alpha )}_\textrm{"likelihood"} \underbrace{q_0(\theta)}_\textrm{prior}
$$

温度 $$\alpha$$ 决定了利用与探索之间的权衡。当 $$\alpha \rightarrow 0$$ 时，$$\theta$$ 只按期望回报 $$J(\theta)$$ 更新。当 $$\alpha \rightarrow \infty$$ 时，$$\theta$$ 始终遵循先验信念。

用 SVGD 方法估计目标后验分布 $$q(\theta)$$ 时，它依赖一组粒子 $$\{\theta_i\}_{i=1}^n$$（独立训练的策略智能体），每个粒子按如下方式更新：

$$
\theta_i \gets \theta_i + \epsilon \phi^{*}(\theta_i) \text{ where } \phi^{*} = \max_{\phi \in \mathcal{H}} \{ - \nabla_\epsilon D_\text{KL} (q'_{[\theta + \epsilon \phi(\theta)]} \| q) \text{ s.t. } \|\phi\|_{\mathcal{H}} \leq 1\} 
$$

其中 $$\epsilon$$ 是学习率，$$\phi^{*}$$ 是 [RKHS](http://mlss.tuebingen.mpg.de/2015/slides/gretton/part_1.pdf)（再生核希尔伯特空间）$$\mathcal{H}$$ 中 $$\theta$$ 形状取值向量的单位球中，能最大程度降低粒子与目标分布之间 KL 散度的那个元素。$$q'(.)$$ 是 $$\theta + \epsilon \phi(\theta)$$ 的分布。

比较不同的基于梯度的更新方法：

| 方法 | 更新空间 |
| ----------------------------- | ------------- |
| 朴素梯度 | 参数空间上的 $$\Delta \theta$$ |
| [自然梯度](https://lilianweng.github.io/posts/2019-09-05-evolution-strategies/#natural-gradients) | 搜索分布空间上的 $$\Delta \theta$$ |
| SVGD | 核函数空间上的 $$\Delta \theta$$（编者注） |

$$\phi^{*}$$ 的一种[估计](https://arxiv.org/abs/1608.04471)具有如下形式。正定核 $$k(\vartheta, \theta)$$，例如高斯[径向基函数](https://en.wikipedia.org/wiki/Radial_basis_function)，度量粒子之间的相似度。

$$
\begin{aligned}
\phi^{*}(\theta_i) 
&= \mathbb{E}_{\vartheta \sim q'} [\nabla_\vartheta \log q(\vartheta) k(\vartheta, \theta_i) + \nabla_\vartheta k(\vartheta, \theta_i)]\\
&= \frac{1}{n} \sum_{j=1}^n [\color{red}{\nabla_{\theta_j} \log q(\theta_j) k(\theta_j, \theta_i)} + \color{green}{\nabla_{\theta_j} k(\theta_j, \theta_i)}] & \scriptstyle{\text{;approximate }q'\text{ with current particle values}}
\end{aligned}
$$

- <span style="color:#fc0303;">红色</span>的第一项鼓励 $$\theta_i$$ 学习朝向 $$q$$ 的高概率区域，该区域为相似粒子所共享。=> 与其他粒子相似
- <span style="color:#00c925;">绿色</span>的第二项把粒子彼此推开，从而使策略多样化。=> 与其他粒子不相似

![SVPG](https://lilianweng.github.io/posts/2018-04-08-policy-gradient/SVPG.png)

温度 $$\alpha$$ 通常遵循退火方案，使训练过程在开始时做更多探索，在后期做更多利用。

### IMPALA
[[论文](https://arxiv.org/abs/1802.01561)\|[代码](https://github.com/deepmind/scalable_agent)]

为了把 RL 训练扩展到极高的吞吐量，**IMPALA**（"Importance Weighted Actor-Learner Architecture"）框架在基本 actor-critic 设定之上将行动（acting）与学习（learning）解耦，并用 **V-trace** 离策略修正从所有经验轨迹中学习。

多个 actor 并行生成经验，而 learner 使用所有生成的经验同时优化策略和价值函数参数。Actor 周期性地用 learner 的最新策略更新自己的参数。由于行动与学习解耦，我们可以添加更多的 actor 机器，在单位时间内生成多得多的轨迹。由于训练策略与行为策略不完全同步，两者之间存在*差距*，因此需要离策略修正。

![IMPALA](https://lilianweng.github.io/posts/2018-04-08-policy-gradient/IMPALA.png)

设价值函数 $$V_\theta$$ 由 $$\theta$$ 参数化，策略 $$\pi_\phi$$ 由 $$\phi$$ 参数化。我们还知道回放缓冲区中的轨迹是由稍旧的策略 $$\mu$$ 收集的。

在训练时间 $$t$$，给定 $$(s_t, a_t, s_{t+1}, r_t)$$，价值函数参数 $$\theta$$ 通过当前价值与 V-trace 价值目标之间的 L2 损失学习。$$n$$ 步 V-trace 目标定义为：

$$
\begin{aligned}
v_t  &= V_\theta(s_t) + \sum_{i=t}^{t+n-1} \gamma^{i-t} \big(\prod_{j=t}^{i-1} c_j\big) \color{red}{\delta_i V} \\
&= V_\theta(s_t) + \sum_{i=t}^{t+n-1} \gamma^{i-t} \big(\prod_{j=t}^{i-1} c_j\big) \color{red}{\rho_i (r_i + \gamma V_\theta(s_{i+1}) - V_\theta(s_i))}
\end{aligned}
$$

其中<span style="color:#fc0303;">红色</span>部分 $$\delta_i V$$ 是 $$V$$ 的时间差分。$$\rho_i = \min\big(\bar{\rho}, \frac{\pi(a_i \vert s_i)}{\mu(a_i \vert s_i)}\big)$$ 和 $$c_j = \min\big(\bar{c}, \frac{\pi(a_j \vert s_j)}{\mu(a_j \vert s_j)}\big)$$ 是*截断的[重要性采样（IS）](#off-policy-policy-gradient)权重*。乘积 $$c_t, \dots, c_{i-1}$$ 度量时间 $$i$$ 观测到的时间差分 $$\delta_i V$$ 对更早时间 $$t$$ 价值函数更新的影响程度。在同策略情形，我们有 $$\rho_i=1$$ 且 $$c_j=1$$（假设 $$\bar{c} \geq 1$$），因此 V-trace 目标退化为同策略的 $$n$$ 步 Bellman 目标。

$$\bar{\rho}$$ 和 $$\bar{c}$$ 是两个截断常数，且 $$\bar{\rho} \geq \bar{c}$$。$$\bar{\rho}$$ 影响我们收敛到的价值函数的不动点，$$\bar{c}$$ 影响收敛速度。当 $$\bar{\rho} =\infty$$（不截断）时，我们收敛到目标策略的价值函数 $$V^\pi$$；当 $$\bar{\rho}$$ 接近 0 时，我们评估的是行为策略的价值函数 $$V^\mu$$；居中时，我们评估介于 $$\pi$$ 和 $$\mu$$ 之间的某个策略。

价值函数参数因此朝以下方向更新：

$$
\Delta\theta = (v_t - V_\theta(s_t))\nabla_\theta V_\theta(s_t)
$$

策略参数 $$\phi$$ 通过策略梯度更新，

$$
\begin{aligned}
\Delta \phi 
&= \rho_t \nabla_\phi \log \pi_\phi(a_t \vert s_t) \big(r_t + \gamma v_{t+1} - V_\theta(s_t)\big) + \nabla_\phi H(\pi_\phi)\\
&= \rho_t \nabla_\phi \log \pi_\phi(a_t \vert s_t) \big(r_t + \gamma v_{t+1} - V_\theta(s_t)\big) - \nabla_\phi \sum_a \pi_\phi(a\vert s_t)\log \pi_\phi(a\vert s_t)
\end{aligned}
$$

其中 $$r_t + \gamma v_{t+1}$$ 是估计的 Q 值，从中减去了一个依赖状态的基线 $$V_\theta(s_t)$$。$$H(\pi_\phi)$$ 是鼓励探索的熵奖励。

在实验中，IMPALA 被用来在多个任务上训练一个智能体。涉及两种不同的模型架构：浅层模型（左）和深层残差模型（右）。

![IMPALA](https://lilianweng.github.io/posts/2018-04-08-policy-gradient/IMPALA-arch.png)

## 快速总结

读完全部上述算法后，我列出一些它们中间似乎共通的构件或原则：

* 尽量降低方差、保持偏差不变，以稳定学习。
* 离策略带来更好的探索，并帮助我们更高效地使用数据样本。
* 经验回放（从回放内存缓冲区采样训练数据）；
* 目标网络，或周期性冻结，或以比主动学习的策略网络更慢的速度更新；
* 批归一化；
* 熵正则化的奖励；
* critic 和 actor 可以共享网络较低的层参数，并有两个分别输出策略和价值函数的头。
* 用确定性策略而非随机策略学习是可行的。
* 对策略更新之间的散度施加约束。
* 新的优化方法（如 K-FAC）。
* 策略的熵最大化有助于鼓励探索。
* 尽量不要高估价值函数。
* 策略网络和价值网络是否共享参数要三思。
* 待补充更多。

---

引用格式：
```
@article{weng2018PG,
  title   = "Policy Gradient Algorithms",
  author  = "Weng, Lilian",
  journal = "lilianweng.github.io/lil-log",
  year    = "2018",
  url     = "https://lilianweng.github.io/lil-log/2018/04/08/policy-gradient-algorithms.html"
}
```

## 参考文献

[1] jeremykun.com [Markov Chain Monte Carlo Without all the Bullshit](https://jeremykun.com/2015/04/06/markov-chain-monte-carlo-without-all-the-bullshit/)

[2] Richard S. Sutton and Andrew G. Barto. [Reinforcement Learning: An Introduction; 2nd Edition](http://incompleteideas.net/book/bookdraft2017nov5.pdf). 2017.

[3] John Schulman, et al. ["High-dimensional continuous control using generalized advantage estimation."](https://arxiv.org/pdf/1506.02438.pdf) ICLR 2016.

[4] Thomas Degris, Martha White, and Richard S. Sutton. ["Off-policy actor-critic."](https://arxiv.org/pdf/1205.4839.pdf) ICML 2012.

[5] timvieira.github.io [Importance sampling](http://timvieira.github.io/blog/post/2014/12/21/importance-sampling/)

[6] Mnih, Volodymyr, et al. ["Asynchronous methods for deep reinforcement learning."](https://arxiv.org/abs/1602.01783) ICML. 2016.

[7] David Silver, et al. ["Deterministic policy gradient algorithms."](https://hal.inria.fr/file/index/docid/938992/filename/dpg-icml2014.pdf) ICML. 2014.

[8] Timothy P. Lillicrap, et al. ["Continuous control with deep reinforcement learning."](https://arxiv.org/pdf/1509.02971.pdf) arXiv preprint arXiv:1509.02971 (2015).

[9] Ryan Lowe, et al. ["Multi-agent actor-critic for mixed cooperative-competitive environments."](https://arxiv.org/pdf/1706.02275.pdf) NIPS. 2017.

[10] John Schulman, et al. ["Trust region policy optimization."](https://arxiv.org/pdf/1502.05477.pdf) ICML. 2015.

[11] Ziyu Wang, et al. ["Sample efficient actor-critic with experience replay."](https://arxiv.org/pdf/1611.01224.pdf) ICLR 2017.

[12] Rémi Munos, Tom Stepleton, Anna Harutyunyan, and Marc Bellemare. ["Safe and efficient off-policy reinforcement learning"](http://papers.nips.cc/paper/6538-safe-and-efficient-off-policy-reinforcement-learning.pdf) NIPS. 2016.

[13] Yuhuai Wu, et al. ["Scalable trust-region method for deep reinforcement learning using Kronecker-factored approximation."](https://arxiv.org/pdf/1708.05144.pdf) NIPS. 2017.

[14] kvfrans.com [A intuitive explanation of natural gradient descent](http://kvfrans.com/a-intuitive-explanation-of-natural-gradient-descent/)

[15] Sham Kakade. ["A Natural Policy Gradient."](https://papers.nips.cc/paper/2073-a-natural-policy-gradient.pdf). NIPS. 2002.

[16] ["Going Deeper Into Reinforcement Learning: Fundamentals of Policy Gradients."](https://danieltakeshi.github.io/2017/03/28/going-deeper-into-reinforcement-learning-fundamentals-of-policy-gradients/) - Seita's Place, Mar 2017.

[17] ["Notes on the Generalized Advantage Estimation Paper."](https://danieltakeshi.github.io/2017/04/02/notes-on-the-generalized-advantage-estimation-paper/) - Seita's Place, Apr, 2017.

[18] Gabriel Barth-Maron, et al. ["Distributed Distributional Deterministic Policy Gradients."](https://arxiv.org/pdf/1804.08617.pdf) ICLR 2018 poster.

[19] Tuomas Haarnoja, Aurick Zhou, Pieter Abbeel, and Sergey Levine. ["Soft Actor-Critic: Off-Policy Maximum Entropy Deep Reinforcement Learning with a Stochastic Actor."](https://arxiv.org/pdf/1801.01290.pdf) arXiv preprint arXiv:1801.01290 (2018).

[20] Scott Fujimoto, Herke van Hoof, and Dave Meger. ["Addressing Function Approximation Error in Actor-Critic Methods."](https://arxiv.org/abs/1802.09477) arXiv preprint arXiv:1802.09477 (2018).

[21] Tuomas Haarnoja, et al. ["Soft Actor-Critic Algorithms and Applications."](https://arxiv.org/abs/1812.05905) arXiv preprint arXiv:1812.05905 (2018).

[22] David Knowles. ["Lagrangian Duality for Dummies"](https://cs.stanford.edu/people/davidknowles/lagrangian_duality.pdf) Nov 13, 2010.

[23] Yang Liu, et al. ["Stein variational policy gradient."](https://arxiv.org/abs/1704.02399) arXiv preprint arXiv:1704.02399 (2017).

[24] Qiang Liu and Dilin Wang. ["Stein variational gradient descent: A general purpose bayesian inference algorithm."](https://papers.nips.cc/paper/6338-stein-variational-gradient-descent-a-general-purpose-bayesian-inference-algorithm.pdf) NIPS. 2016.

[25] Lasse Espeholt, et al. ["IMPALA: Scalable Distributed Deep-RL with Importance Weighted Actor-Learner Architectures"](https://arxiv.org/abs/1802.01561) arXiv preprint 1802.01561 (2018).

[26] Karl Cobbe, et al. ["Phasic Policy Gradient."](https://arxiv.org/abs/2009.04416) arXiv preprint arXiv:2009.04416 (2020).

[27] Chloe Ching-Yun Hsu, et al. ["Revisiting Design Choices in Proximal Policy Optimization."](https://arxiv.org/abs/2009.10897) arXiv preprint arXiv:2009.10897 (2020).
