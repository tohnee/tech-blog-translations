---
title: "一窥强化学习（长文）"
title_en: "A (Long) Peek into Reinforcement Learning"
source: https://lilianweng.github.io/posts/2018-02-19-rl-overview/
crawled: 2026-09-08
translated: 2026-09-08
---

# 一窥强化学习（长文）

> 原文：[A (Long) Peek into Reinforcement Learning](https://lilianweng.github.io/posts/2018-02-19-rl-overview/) · Lilian Weng（翁荔）

> 在这篇文章中，我们将简要梳理强化学习（Reinforcement Learning, RL）领域，从基础概念讲到经典算法。希望这篇综述足够有用，让新手在入门时不会迷失在专业术语和行话之中。[警告] 这是一篇长文。

<span style="color: #286ee0;">[更新于 2020-09-03：更新了 [SARSA](#sarsa-on-policy-td-control) 与 [Q-learning](#q-learning-off-policy-td-control) 的算法描述，使两者的区别更加鲜明。</span>
<br />
<span style="color: #286ee0;">[更新于 2021-09-19：感谢 爱吃猫的鱼，本文有了[中文版](https://paperexplained.cn/articles/article/detail/33/)]。</span>

近年来，人工智能（Artificial Intelligence, AI）领域接连出现了一些激动人心的新闻：AlphaGo 击败了人类最强的职业围棋选手；很快，其扩展算法 AlphaGo Zero 在不使用人类知识做监督学习的情况下，以 100 比 0 击败了 AlphaGo；顶尖职业游戏玩家在 DOTA2 1v1 比赛中不敌 OpenAI 开发的机器人。了解到这些之后，很难不对这些算法背后的魔法——强化学习（RL）——感到好奇。我写这篇文章，就是想对这一领域做一番简要梳理。我们会先介绍若干基础概念，然后深入讲解求解 RL 问题的经典方法。希望这篇文章能成为新手的一个良好起点，为日后追踪前沿研究架起桥梁。

## 什么是强化学习？

假设我们有一个处于未知环境中的智能体（agent），它可以通过与环境交互获得一些奖励（reward）。智能体应当采取动作，以最大化累积奖励。在现实中，这样的场景可以是一个为了刷高分而玩游戏的程序，也可以是一个尝试用实物完成物理任务的机器人，而且远不止这些。

![强化学习问题示意图](https://lilianweng.github.io/posts/2018-02-19-rl-overview/RL_illustration.png)

*图 1. 智能体与环境交互，尝试采取聪明的动作以最大化累积奖励。*

强化学习（RL）的目标是让智能体从实验性尝试以及收到的相对简单的反馈中学习出一个好策略。有了最优策略，智能体便能主动适应环境，使未来奖励最大化。

### 关键概念

下面我们来正式定义 RL 中的一组关键概念。

智能体在**环境**（environment）中行动。环境如何对特定动作做出反应，由一个**模型**（model）来定义，而这个模型我们可能知道，也可能不知道。智能体可以处于环境中许多**状态**（state）之一（$$s \in \mathcal{S}$$），并选择采取多种**动作**（action）之一（$$a \in \mathcal{A}$$），从一个状态切换到另一个状态。智能体会到达哪个状态，由状态之间的转移概率（$$P$$）决定。一旦执行了动作，环境就会给出一个**奖励**（reward，$$r \in \mathcal{R}$$）作为反馈。

模型定义了奖励函数和转移概率。我们可能知道、也可能不知道模型是如何运作的，这就区分出两种情形：
- **已知模型**：拥有完美信息的规划；做基于模型（model-based）的 RL。当我们完全了解环境时，可以通过[动态规划](https://en.wikipedia.org/wiki/Dynamic_programming)（Dynamic Programming, DP）求出最优解。你还记得算法入门课上的「最长递增子序列」或「旅行商问题」吗？哈哈。不过这并不是本文的重点。
- **未知模型**：在不完整信息下学习；做无模型（model-free）的 RL，或者把显式学习模型作为算法的一部分。下文的大部分内容都服务于模型未知的场景。

智能体的**策略**（policy）$$\pi(s)$$ 给出了在某个状态下采取什么最优动作的准则，<span style="color: #e01f1f;">**其目标是最大化总奖励**</span>。每个状态都关联着一个**价值**（value）函数 $$V(s)$$，用于预测在该状态下按相应策略行动所能获得的未来奖励的期望。换言之，价值函数量化了一个状态有多好。策略和价值函数正是我们在强化学习中要学习的东西。

![RL 算法的分类](https://lilianweng.github.io/posts/2018-02-19-rl-overview/RL_algorithm_categorization.png)

*图 2. 基于「我们想对价值、策略还是环境建模」对 RL 各类方法的总结。（图片来源：根据 David Silver 的 RL 课程[第 1 讲](https://youtu.be/2pWv7GOvuf0)重绘。）*

智能体与环境之间的交互涉及时间 $$t=1, 2, \dots, T$$ 上的一系列动作和观测到的奖励。在此过程中，智能体不断积累关于环境的知识，学习最优策略，并决定下一步采取什么动作，以便高效地学得最佳策略。我们把时刻 t 的状态、动作和奖励分别记为 $$S_t$$、$$A_t$$ 和 $$R_t$$。于是，整段交互序列可以用一个**回合**（episode，也称为 "trial" 或 "trajectory"）完整描述，序列终止于终止状态 $$S_T$$：

$$
S_1, A_1, R_2, S_2, A_2, \dots, S_T
$$

深入不同类别的 RL 算法时，你会频繁遇到以下术语：
- **基于模型（Model-based）**：依赖环境模型；模型要么是已知的，要么由算法显式学习得到。
- **无模型（Model-free）**：学习过程中不依赖模型。
- **同策略（On-policy）**：使用目标策略本身的确定性结果或样本来训练算法。
- **离策略（Off-policy）**：在由另一个不同的行为策略（behavior policy）而非目标策略产生的转移或回合分布上进行训练。


#### 模型：转移与奖励

模型是对环境的描述。有了模型，我们就可以学习或推断环境会如何与智能体交互并给出反馈。模型主要有两个部分：转移概率函数 $$P$$ 和奖励函数 $$R$$。

假设我们处于状态 s，决定采取动作 a，到达下一个状态 s' 并获得奖励 r。这称为一步**转移**（transition），用元组 (s, a, s', r) 表示。

转移函数 P 记录了在采取动作 a 并获得奖励 r 的前提下，从状态 s 转移到 s' 的概率。我们用 $$\mathbb{P}$$ 作为「概率」的符号。

$$
P(s', r \vert s, a)  = \mathbb{P} [S_{t+1} = s', R_{t+1} = r \vert S_t = s, A_t = a]
$$

因此，状态转移函数可以定义为 $$P(s', r \vert s, a)$$ 的函数：

$$
P_{ss'}^a = P(s' \vert s, a)  = \mathbb{P} [S_{t+1} = s' \vert S_t = s, A_t = a] = \sum_{r \in \mathcal{R}} P(s', r \vert s, a)
$$

奖励函数 R 预测由一个动作触发的下一个奖励：

$$
R(s, a) = \mathbb{E} [R_{t+1} \vert S_t = s, A_t = a] = \sum_{r\in\mathcal{R}} r \sum_{s' \in \mathcal{S}} P(s', r \vert s, a)
$$


#### 策略

策略是智能体的行为函数 $$\pi$$，它告诉我们处于状态 s 时应该采取哪个动作。它是从状态 s 到动作 a 的映射，既可以是确定性的，也可以是随机性的：
- 确定性：$$\pi(s) = a$$。
- 随机性：$$\pi(a \vert s) = \mathbb{P}_\pi [A=a \vert S=s]$$。


#### 价值函数

价值函数通过预测未来奖励来衡量一个状态有多好，或者说一个状态或一个动作能带来多少奖励。未来的奖励也称为**回报**（return），是往后所有折扣奖励的总和。我们来计算从时刻 t 开始的回报 $$G_t$$：

$$
G_t = R_{t+1} + \gamma R_{t+2} + \dots = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1}
$$

折扣因子（discount factor）$$\gamma \in [0, 1]$$ 会削弱未来奖励的权重，原因如下：
- 未来的奖励可能带有更高的不确定性，比如股票市场；
- 未来的奖励无法带来即时的好处，比如作为人类，我们可能更愿意今天享乐，而不是 5 年后再享乐 ；)；
- 折扣带来了数学上的便利，比如我们不需要为了计算回报而永远跟踪未来的所有步；
- 我们不必担心状态转移图中的无限循环。

一个状态 s 的**状态价值**（state-value）是当我们在时刻 t 处于该状态（$$S_t = s$$）时的期望回报：

$$
V_{\pi}(s) = \mathbb{E}_{\pi}[G_t \vert S_t = s]
$$

类似地，我们定义状态-动作对的**动作价值**（action-value，「Q 值」；我猜 Q 取自 "Quality"（质量）？）为：

$$
Q_{\pi}(s, a) = \mathbb{E}_{\pi}[G_t \vert S_t = s, A_t = a]
$$

此外，由于我们遵循目标策略 $$\pi$$，可以利用可能动作上的概率分布和 Q 值来还原状态价值：

$$
V_{\pi}(s) = \sum_{a \in \mathcal{A}} Q_{\pi}(s, a) \pi(a \vert s)
$$

动作价值与状态价值之差就是动作**优势**（advantage）函数（「A 值」）：

$$
A_{\pi}(s, a) = Q_{\pi}(s, a) - V_{\pi}(s)
$$


#### 最优价值与最优策略

最优价值函数给出最大回报：

$$
V_{*}(s) = \max_{\pi} V_{\pi}(s),
Q_{*}(s, a) = \max_{\pi} Q_{\pi}(s, a)
$$

最优策略达到最优价值函数：

$$
\pi_{*} = \arg\max_{\pi} V_{\pi}(s),
\pi_{*} = \arg\max_{\pi} Q_{\pi}(s, a)
$$

当然，我们有 $$V_{\pi_{*}}(s)=V_{*}(s)$$ 和 $$Q_{\pi_{*}}(s, a) = Q_{*}(s, a)$$。


### 马尔可夫决策过程

更正式地说，几乎所有 RL 问题都可以表述为**马尔可夫决策过程**（Markov Decision Processes, MDP）。MDP 中的所有状态都具有「马尔可夫」性质，指的是未来只取决于当前状态，而与历史无关：

$$
\mathbb{P}[ S_{t+1} \vert S_t ] = \mathbb{P} [S_{t+1} \vert S_1, \dots, S_t]
$$

换句话说，给定现在，未来与过去**条件独立**，因为当前状态已经囊括了决定未来所需的全部统计信息。


![MDP 中的智能体-环境交互](https://lilianweng.github.io/posts/2018-02-19-rl-overview/agent_environment_MDP.png)

*图 3. 马尔可夫决策过程中的智能体-环境交互。（图片来源：Sutton & Barto (2017) 第 3.1 节。）*


一个马尔可夫决策过程由五个元素组成：$$\mathcal{M} = \langle \mathcal{S}, \mathcal{A}, P, R, \gamma \rangle$$，这些符号与[上一节](#key-concepts)关键概念的含义相同，与 RL 问题设置高度吻合：
- $$\mathcal{S}$$——状态集合；
- $$\mathcal{A}$$——动作集合；
- $$P$$——转移概率函数；
- $$R$$——奖励函数；
- $$\gamma$$——未来奖励的折扣因子。
在未知环境中，我们对 $$P$$ 和 $$R$$ 并没有完备的知识。


![MDP 示例](https://lilianweng.github.io/posts/2018-02-19-rl-overview/mdp_example.jpg)

*图 4. 一个有趣的马尔可夫决策过程示例：典型的一天工作。（图片来源：[randomant.net/reinforcement-learning-concepts](https://randomant.net/reinforcement-learning-concepts/)）*


### Bellman 方程

Bellman 方程（贝尔曼方程）是指一组把价值函数分解为即时奖励加上折扣后未来价值的方程。

$$
\begin{aligned}
V(s) &= \mathbb{E}[G_t \vert S_t = s] \\
&= \mathbb{E} [R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + \dots \vert S_t = s] \\
&= \mathbb{E} [R_{t+1} + \gamma (R_{t+2} + \gamma R_{t+3} + \dots) \vert S_t = s] \\
&= \mathbb{E} [R_{t+1} + \gamma G_{t+1} \vert S_t = s] \\
&= \mathbb{E} [R_{t+1} + \gamma V(S_{t+1}) \vert S_t = s]
\end{aligned}
$$

对 Q 值同理，

$$
\begin{aligned}
Q(s, a) 
&= \mathbb{E} [R_{t+1} + \gamma V(S_{t+1}) \mid S_t = s, A_t = a] \\
&= \mathbb{E} [R_{t+1} + \gamma \mathbb{E}_{a\sim\pi} Q(S_{t+1}, a) \mid S_t = s, A_t = a]
\end{aligned}
$$


#### Bellman 期望方程

这一递归更新过程还可以进一步分解为同时建立在状态价值函数和动作价值函数之上的方程。随着我们沿未来的动作步越走越远，我们按照策略 $$\pi$$ 交替地扩展 V 和 Q。


![Bellman 方程](https://lilianweng.github.io/posts/2018-02-19-rl-overview/bellman_equation.png)

*图 5. Bellman 期望方程如何更新状态价值函数和动作价值函数的示意图。*


$$
\begin{aligned}
V_{\pi}(s) &= \sum_{a \in \mathcal{A}} \pi(a \vert s) Q_{\pi}(s, a) \\
Q_{\pi}(s, a) &= R(s, a) + \gamma \sum_{s' \in \mathcal{S}} P_{ss'}^a V_{\pi} (s') \\
V_{\pi}(s) &= \sum_{a \in \mathcal{A}} \pi(a \vert s) \big( R(s, a) + \gamma \sum_{s' \in \mathcal{S}} P_{ss'}^a V_{\pi} (s') \big) \\
Q_{\pi}(s, a) &= R(s, a) + \gamma \sum_{s' \in \mathcal{S}} P_{ss'}^a \sum_{a' \in \mathcal{A}} \pi(a' \vert s') Q_{\pi} (s', a')
\end{aligned}
$$


#### Bellman 最优方程

如果我们只关心最优值，而不是按某个策略计算期望，那么就可以在交替更新中直接跳到最大回报，而不需要使用任何策略。回顾一下：最优值 $$V_*$$ 和 $$Q_*$$ 是我们所能获得的最优回报，定义见[这里](#optimal-value-and-policy)。

$$
\begin{aligned}
V_*(s) &= \max_{a \in \mathcal{A}} Q_*(s,a)\\
Q_*(s, a) &= R(s, a) + \gamma \sum_{s' \in \mathcal{S}} P_{ss'}^a V_*(s') \\
V_*(s) &= \max_{a \in \mathcal{A}} \big( R(s, a) + \gamma \sum_{s' \in \mathcal{S}} P_{ss'}^a V_*(s') \big) \\
Q_*(s, a) &= R(s, a) + \gamma \sum_{s' \in \mathcal{S}} P_{ss'}^a \max_{a' \in \mathcal{A}} Q_*(s', a')
\end{aligned}
$$

毫不意外，它们看起来和 Bellman 期望方程非常相似。

如果我们拥有环境的完整信息，问题就变成了一个规划问题，可以用 DP 求解。遗憾的是，在大多数场景下，我们并不知道 $$P_{ss'}^a$$ 或 $$R(s, a)$$，因此无法直接套用 Bellman 方程求解 MDP，但它为许多 RL 算法奠定了理论基础。



## 常见方法

现在，我们来梳理求解 RL 问题的主要方法和经典算法。在后续文章中，我计划对每种方法做更深入的探讨。


### 动态规划

当模型完全已知时，依照 Bellman 方程，我们可以使用[动态规划](https://en.wikipedia.org/wiki/Dynamic_programming)（DP）来迭代地评估价值函数并改进策略。


#### 策略评估

策略评估（Policy Evaluation）旨在计算状态价值 $$V_\pi$$，这里的价值是针对给定策略 $$\pi$$ 而言的：

$$
V_{t+1}(s) 
= \mathbb{E}_\pi [r + \gamma V_t(s') | S_t = s]
= \sum_a \pi(a \vert s) \sum_{s', r} P(s', r \vert s, a) (r + \gamma V_t(s'))
$$

#### 策略改进

基于价值函数，策略改进（Policy Improvement）通过贪心地行动来生成一个更好的策略 $$\pi' \geq \pi$$。

$$
Q_\pi(s, a) 
= \mathbb{E} [R_{t+1} + \gamma V_\pi(S_{t+1}) \vert S_t=s, A_t=a]
= \sum_{s', r} P(s', r \vert s, a) (r + \gamma V_\pi(s'))
$$

#### 策略迭代

*广义策略迭代（Generalized Policy Iteration, GPI）* 算法指的是把策略评估与策略改进结合起来、以此迭代改进策略的过程。

$$
\pi_0 \xrightarrow[]{\text{evaluation}} V_{\pi_0} \xrightarrow[]{\text{improve}}
\pi_1 \xrightarrow[]{\text{evaluation}} V_{\pi_1} \xrightarrow[]{\text{improve}}
\pi_2 \xrightarrow[]{\text{evaluation}} \dots \xrightarrow[]{\text{improve}}
\pi_* \xrightarrow[]{\text{evaluation}} V_*
$$

在 GPI 中，价值函数被反复逼近，以越来越接近当前策略的真实价值；与此同时，策略被反复改进，逐步趋向最优。这一策略迭代过程是有效的，并且总能收敛到最优，但为什么会这样呢？

假设我们有一个策略 $$\pi$$，然后通过贪心地选择动作生成改进版 $$\pi'$$，即 $$\pi'(s) = \arg\max_{a \in \mathcal{A}} Q_\pi(s, a)$$。这个改进后的 $$\pi'$$ 的价值保证会更好，因为：

$$
\begin{aligned}
Q_\pi(s, \pi'(s))
&= Q_\pi(s, \arg\max_{a \in \mathcal{A}} Q_\pi(s, a)) \\
&= \max_{a \in \mathcal{A}} Q_\pi(s, a) \geq Q_\pi(s, \pi(s)) = V_\pi(s)
\end{aligned}
$$


### 蒙特卡洛方法

首先，回顾一下 $$V(s) = \mathbb{E}[ G_t \vert S_t=s]$$。蒙特卡洛（Monte-Carlo, MC）方法的思想很简单：它直接从原始经验的回合中学习，而不对环境动态建模，并把观测到的平均回报作为期望回报的近似。为了计算经验回报 $$G_t$$，MC 方法需要从<span style="color: #e01f1f;">**完整**</span>的回合 $$S_1, A_1, R_2, \dots, S_T$$ 中学习，以计算 $$G_t = \sum_{k=0}^{T-t-1} \gamma^k R_{t+k+1}$$，而且所有回合最终必须终止。

状态 s 的经验平均回报为：

$$
V(s) = \frac{\sum_{t=1}^T \mathbb{1}[S_t = s] G_t}{\sum_{t=1}^T \mathbb{1}[S_t = s]}
$$

其中 $$\mathbb{1}[S_t = s]$$ 是一个二元指示函数。我们可以每次都统计状态 s 的出现，这样一个状态在一个回合中可能被多次统计（「每次访问」，every-visit）；也可以只在一个回合中首次遇到某个状态时才统计（「首次访问」，first-visit）。这种近似方式很容易推广到动作价值函数，只需按 (s, a) 对来计数。

$$
Q(s, a) = \frac{\sum_{t=1}^T \mathbb{1}[S_t = s, A_t = a] G_t}{\sum_{t=1}^T \mathbb{1}[S_t = s, A_t = a]}
$$

要用 MC 学到最优策略，我们可以按照与 [GPI](#policy-iteration) 类似的思路进行迭代。

![用 MC 进行策略迭代](https://lilianweng.github.io/posts/2018-02-19-rl-overview/MC_control.png)


1. 相对当前价值函数贪心地改进策略：$$\pi(s) = \arg\max_{a \in \mathcal{A}} Q(s, a)$$。
2. 用新策略 $$\pi$$ 生成一个新回合（例如借助 [ε-贪心](https://lilianweng.github.io/posts/2018-01-23-multi-armed-bandit/#%CE%B5-greedy-algorithm)之类的算法，可以帮助我们在利用与探索之间取得平衡）。
3. 用新回合估计 Q：$$q_\pi(s, a) = \frac{\sum_{t=1}^T \big( \mathbb{1}[S_t = s, A_t = a] \sum_{k=0}^{T-t-1} \gamma^k R_{t+k+1} \big)}{\sum_{t=1}^T \mathbb{1}[S_t = s, A_t = a]}$$


### 时序差分学习

与蒙特卡洛方法类似，时序差分（Temporal-Difference, TD）学习是无模型的，同样从经验回合中学习。不过，TD 学习可以从<span style="color: #e01f1f;">**不完整**</span>的回合中学习，因此我们不需要一直跟踪回合直到终止。TD 学习非常重要，Sutton & Barto (2017) 在他们的 RL 书中把它描述为「对强化学习而言处于核心地位且新颖的一个思想」。


#### 自举

TD 学习方法依据已有的估计值来更新目标，而不是像 MC 方法那样完全依赖真实奖励和完整回报。这种方式被称为**自举**（bootstrapping）。


#### 价值估计

TD 学习的关键思想是让价值函数 $$V(S_t)$$ 向一个估计回报 $$R_{t+1} + \gamma V(S_{t+1})$$（称为「**TD 目标**」）靠拢。价值函数的更新幅度由学习率超参数 α 控制：

$$
\begin{aligned}
V(S_t) &\leftarrow (1- \alpha) V(S_t) + \alpha G_t \\
V(S_t) &\leftarrow V(S_t) + \alpha (G_t - V(S_t)) \\
V(S_t) &\leftarrow V(S_t) + \alpha (R_{t+1} + \gamma V(S_{t+1}) - V(S_t))
\end{aligned}
$$

类似地，对于动作价值估计：

$$
Q(S_t, A_t) \leftarrow Q(S_t, A_t) + \alpha (R_{t+1} + \gamma Q(S_{t+1}, A_{t+1}) - Q(S_t, A_t))
$$

接下来，让我们进入有趣的部分：如何在 TD 学习中学到最优策略（又称「TD 控制」）。做好准备，这一节你会看到许多经典算法的大名。


#### SARSA：同策略 TD 控制

「SARSA」指的是沿着序列 $$\dots, S_t, A_t, R_{t+1}, S_{t+1}, A_{t+1}, \dots$$ 更新 Q 值的过程。其思路与 [GPI](#policy-iteration) 一脉相承。在一个回合内，它的流程如下：

1. 初始化 $$t=0$$。
2. 从 $$S_0$$ 出发，选择动作 $$A_0 = \arg\max_{a \in \mathcal{A}} Q(S_0, a)$$，通常配合 $$\epsilon$$-贪心使用。
3. 在时刻 $$t$$，执行动作 $$A_t$$ 后，我们观测到奖励 $$R_{t+1}$$，并进入下一个状态 $$S_{t+1}$$。
4. 然后按照与第 2 步相同的方式选取下一个动作：$$A_{t+1} = \arg\max_{a \in \mathcal{A}} Q(S_{t+1}, a)$$。
5. 更新 Q 值函数：$$ Q(S_t, A_t) \leftarrow Q(S_t, A_t) + \alpha (R_{t+1} + \gamma Q(S_{t+1}, A_{t+1}) - Q(S_t, A_t)) $$。
6. 令 $$t = t+1$$，并从第 3 步开始重复。

在 SARSA 的每一步中，我们都需要按照*当前*策略来选取*下一个*动作。


#### Q-learning：离策略 TD 控制

Q-learning（[Watkins & Dayan, 1992](https://link.springer.com/content/pdf/10.1007/BF00992698.pdf)）的提出是强化学习早期的一次重大突破。在一个回合内，它的流程如下：

1. 初始化 $$t=0$$。
2. 从 $$S_0$$ 出发。
3. 在时刻步 $$t$$，我们根据 Q 值挑选动作，$$A_t = \arg\max_{a \in \mathcal{A}} Q(S_t, a)$$，通常配合 $$\epsilon$$-贪心使用。
4. 执行动作 $$A_t$$ 后，我们观测到奖励 $$R_{t+1}$$，并进入下一个状态 $$S_{t+1}$$。
5. 更新 Q 值函数：$$Q(S_t, A_t) \leftarrow Q(S_t, A_t) + \alpha (R_{t+1} + \gamma \max_{a \in \mathcal{A}} Q(S_{t+1}, a) - Q(S_t, A_t))$$。
6. 令 $$t = t+1$$，并从第 3 步开始重复。

与 SARSA 的关键区别在于，Q-learning 选取第二个动作 $$A_{t+1}$$ 时并不遵循当前策略。它从最优 Q 值出发估计 $$Q^*$$，但到底是哪个动作（记为 $$a^*$$）带来了这个最大 Q 值并不重要，下一步 Q-learning 未必会采取 $$a^*$$。


![SARSA 与 Q-learning](https://lilianweng.github.io/posts/2018-02-19-rl-overview/sarsa_vs_q_learning.png)

*图 6. Q-learning 与 SARSA 的回溯图（backup diagram）。（图片来源：根据 Sutton & Barto (2017) 图 6.5 重绘）*


#### 深度 Q 网络

理论上，在 Q-learning 中我们可以把所有状态-动作对的 $$Q_*(.)$$ 都记忆下来，就像存进一张巨大的表格。然而，当状态空间和动作空间很大时，这在计算上很快就变得不可行。于是人们使用函数（也就是一个机器学习模型）来近似 Q 值，这被称为**函数近似**（function approximation）。例如，如果我们用一个参数为 $$\theta$$ 的函数来计算 Q 值，就可以把 Q 值函数记为 $$Q(s, a; \theta)$$。

遗憾的是，当 Q-learning 与非线性 Q 值函数近似及[自举](#bootstrapping)结合时，训练可能会不稳定甚至发散（见[问题 #2](#deadly-triad-issue)）。

深度 Q 网络（"DQN"；Mnih et al. 2015）旨在通过两种创新机制大幅改进并稳定 Q-learning 的训练过程：
- **经验回放（Experience Replay）**：所有回合步骤 $$e_t = (S_t, A_t, R_t, S_{t+1})$$ 都被存入一个回放记忆（replay memory）$$D_t = \{ e_1, \dots, e_t \}$$ 中。$$D_t$$ 汇集了许多回合的经验元组。在 Q-learning 更新时，样本从回放记忆中随机抽取，因此一个样本可能被多次使用。经验回放提高了数据效率，消除了观测序列中的相关性，并平滑了数据分布的变化。
- **周期性更新的目标（Periodically Updated Target）**：Q 朝着只周期性更新的目标值进行优化。Q 网络被克隆下来，每 C 步（C 是一个超参数）保持冻结，作为优化目标。这一改动克服了短期震荡，使训练更加稳定。

损失函数如下：

$$
\mathcal{L}(\theta) = \mathbb{E}_{(s, a, r, s') \sim U(D)} \Big[ \big( r + \gamma \max_{a'} Q(s', a'; \theta^{-}) - Q(s, a; \theta) \big)^2 \Big]
$$

其中 $$U(D)$$ 是回放记忆 D 上的均匀分布；$$\theta^{-}$$ 是被冻结的目标 Q 网络的参数。

此外，实践中还发现把误差项裁剪到 [-1, 1] 之间也有帮助。（我对这类参数裁剪总是心情复杂：许多研究表明它在经验上确实有效，但让数学变得难看多了。 :/）


![DQN 算法](https://lilianweng.github.io/posts/2018-02-19-rl-overview/DQN_algorithm.png)

*图 7. 带经验回放和周期性冻结优化目标的 DQN 算法。其中的预处理序列是对 Atari 游戏输入图像运行若干处理流程后的输出。不必太纠结它，把它们当作输入特征向量即可。（图片来源：Mnih et al. 2015）*


DQN 有许多改进原始设计的扩展，例如采用对偶架构（dueling architecture）的 DQN（Wang et al. 2016），它用共享的网络参数同时估计状态价值函数 V(s) 和优势函数 A(s, a)。


### 结合 TD 与 MC 学习

在前文关于 TD 学习中价值估计的[小节](#value-estimation)里，我们计算 TD 目标时只沿动作链向前多追溯一步。我们可以很容易地把它扩展为向前追溯多步来估计回报。

我们把往后跟随 n 步得到的估计回报记为 $$G_t^{(n)}, n=1, \dots, \infty$$，于是有：


| $$n$$        | $$G_t$$           | 备注  |
| ------------- | ------------- | ------------- |
| $$n=1$$ | $$G_t^{(1)} = R_{t+1} + \gamma V(S_{t+1})$$ | TD 学习 |
| $$n=2$$ | $$G_t^{(2)} = R_{t+1} + \gamma R_{t+2} + \gamma^2 V(S_{t+2})$$ | |
| ... | | |
| $$n=n$$ | $$ G_t^{(n)} = R_{t+1} + \gamma R_{t+2} + \dots + \gamma^{n-1} R_{t+n} + \gamma^n V(S_{t+n}) $$ | |
| ... | | |
| $$n=\infty$$ | $$G_t^{(\infty)} = R_{t+1} + \gamma R_{t+2} + \dots + \gamma^{T-t-1} R_T + \gamma^{T-t} V(S_T) $$ | MC 估计 |

广义的 n 步 TD 学习更新价值函数的形式仍与[之前](#value-estimation)相同：

$$
V(S_t) \leftarrow V(S_t) + \alpha (G_t^{(n)} - V(S_t))
$$

![TD lambda](https://lilianweng.github.io/posts/2018-02-19-rl-overview/TD_lambda.png)



在 TD 学习中，我们可以随心选定任意 $$n$$。那么问题来了：最好的 $$n$$ 是多少？哪个 $$G_t^{(n)}$$ 能给出最好的回报近似？一个常见而聪明的做法是对所有可能的 n 步 TD 目标做加权和，而不是挑选单一的最佳 n。权重随 n 按因子 λ 衰减，即 $$\lambda^{n-1}$$；其直觉与我们在计算回报时[为什么](#value-estimation)要对未来奖励打折扣类似：看得越远，信心越少。为了让所有权重（n → ∞）之和为 1，我们将每个权重都乘以 (1-λ)，因为：

$$
\begin{aligned}
\text{let } S &= 1 + \lambda + \lambda^2 + \dots \\
S &= 1 + \lambda(1 + \lambda + \lambda^2 + \dots) \\
S &= 1 + \lambda S \\
S &= 1 / (1-\lambda)
\end{aligned}
$$

这个由许多 n 步回报组成的加权和被称为 λ-回报（λ-return）$$G_t^{\lambda} = (1-\lambda) \sum_{n=1}^{\infty} \lambda^{n-1} G_t^{(n)}$$。采用 λ-回报来更新价值的 TD 学习记为 **TD(λ)**。我们在[上文](#value-estimation)介绍的原始版本等价于 **TD(0)**。


![回溯图](https://lilianweng.github.io/posts/2018-02-19-rl-overview/TD_MC_DP_backups.png)

*图 8. 蒙特卡洛、时序差分学习与动态规划在状态价值函数上回溯图的对比。（图片来源：David Silver 的 RL 课程[第 4 讲](http://www0.cs.ucl.ac.uk/staff/d.silver/web/Teaching_files/MC-TD.pdf)："Model-Free Prediction"）*


### 策略梯度

前面介绍的所有方法都着眼于学习状态/动作价值函数，然后据此选择动作。策略梯度（Policy Gradient）方法则直接用一个关于 $$\theta$$ 参数化的函数学习策略，即 $$\pi(a \vert s; \theta)$$。我们把奖励函数（与损失函数相对）定义为*期望回报*，并以最大化奖励函数为目标来训练算法。我的[下一篇文章](https://lilianweng.github.io/posts/2018-04-08-policy-gradient/)解释了策略梯度定理为何成立（含证明），并介绍了多种策略梯度算法。

在离散空间中：

$$
\mathcal{J}(\theta) = V_{\pi_\theta}(S_1) = \mathbb{E}_{\pi_\theta}[V_1]
$$

其中 $$S_1$$ 是初始起始状态。

或者在连续空间中：

$$
\mathcal{J}(\theta) = \sum_{s \in \mathcal{S}} d_{\pi_\theta}(s) V_{\pi_\theta}(s) = \sum_{s \in \mathcal{S}} \Big( d_{\pi_\theta}(s) \sum_{a \in \mathcal{A}} \pi(a \vert s, \theta) Q_\pi(s, a) \Big)
$$

其中 $$d_{\pi_\theta}(s)$$ 是 $$\pi_\theta$$ 对应马尔可夫链的平稳分布（stationary distribution）。如果你不熟悉「平稳分布」的定义，请参阅这份[参考资料](https://jeremykun.com/2015/04/06/markov-chain-monte-carlo-without-all-the-bullshit/)。

使用*梯度上升*，我们可以找到产生最高回报的最优 θ。很自然地可以预期，基于策略的方法在连续空间中更有用，因为在连续空间中需要估计价值的状态和/或动作有无限多个，基于价值的方法在计算上要昂贵得多。


#### 策略梯度定理

*数值地*计算梯度，可以通过在第 k 个维度上对 θ 施加微小扰动 ε 来实现。即使 $$J(\theta)$$ 不可微它也能工作（妙！），但不出所料，速度非常慢。

$$
\frac{\partial \mathcal{J}(\theta)}{\partial \theta_k} \approx \frac{\mathcal{J}(\theta + \epsilon u_k) - \mathcal{J}(\theta)}{\epsilon}
$$

或者*解析地*，

$$
\mathcal{J}(\theta) = \mathbb{E}_{\pi_\theta} [r] = \sum_{s \in \mathcal{S}} d_{\pi_\theta}(s) \sum_{a \in \mathcal{A}} \pi(a \vert s; \theta) R(s, a)
$$

实际上，我们有漂亮的理论支持（把 $$d(.)$$ 替换为 $$d_\pi(.)$$）：

$$
\mathcal{J}(\theta) = \sum_{s \in \mathcal{S}} d_{\pi_\theta}(s) \sum_{a \in \mathcal{A}} \pi(a \vert s; \theta) Q_\pi(s, a) \propto \sum_{s \in \mathcal{S}} d(s) \sum_{a \in \mathcal{A}} \pi(a \vert s; \theta) Q_\pi(s, a)
$$

至于为什么成立，请查阅 Sutton & Barto (2017) 的第 13.1 节。

然后，

$$
\begin{aligned}
\mathcal{J}(\theta) &= \sum_{s \in \mathcal{S}} d(s) \sum_{a \in \mathcal{A}} \pi(a \vert s; \theta) Q_\pi(s, a) \\
\nabla \mathcal{J}(\theta) &= \sum_{s \in \mathcal{S}} d(s) \sum_{a \in \mathcal{A}} \nabla \pi(a \vert s; \theta) Q_\pi(s, a) \\
&= \sum_{s \in \mathcal{S}} d(s) \sum_{a \in \mathcal{A}} \pi(a \vert s; \theta) \frac{\nabla \pi(a \vert s; \theta)}{\pi(a \vert s; \theta)} Q_\pi(s, a) \\
& = \sum_{s \in \mathcal{S}} d(s) \sum_{a \in \mathcal{A}} \pi(a \vert s; \theta) \nabla \ln \pi(a \vert s; \theta) Q_\pi(s, a) \\
& = \mathbb{E}_{\pi_\theta} [\nabla \ln \pi(a \vert s; \theta) Q_\pi(s, a)]
\end{aligned}
$$

这一结果被称为「策略梯度定理」（Policy Gradient Theorem），它为各种策略梯度算法奠定了理论基础：

$$
\nabla \mathcal{J}(\theta) = \mathbb{E}_{\pi_\theta} [\nabla \ln \pi(a \vert s, \theta) Q_\pi(s, a)]
$$


#### REINFORCE

REINFORCE 也称蒙特卡洛策略梯度，它依赖 $$Q_\pi(s, a)$$——用回合样本经 [MC](#monte-carlo-methods) 方法估计出的回报——来更新策略参数 $$\theta$$。

REINFORCE 的一个常用变体是从回报 $$G_t$$ 中减去一个基线（baseline）值，从而在保持偏差不变的同时降低梯度估计的方差。例如，一个常用的基线是状态价值；若采用它，我们在梯度上升更新中就会使用 $$A(s, a) = Q(s, a) - V(s)$$。

1. 随机初始化 θ
2. 生成一个回合 $$S_1, A_1, R_2, S_2, A_2, \dots, S_T$$
3. 对 t=1, 2, ... , T：
	1. 估计自时刻 t 起的回报 G_t。
	2. $$\theta \leftarrow \theta + \alpha \gamma^t G_t \nabla \ln \pi(A_t \vert S_t, \theta)$$。


#### Actor-Critic

如果在策略之外还学习价值函数，我们就得到了 actor-critic 算法。
- **Critic（评论家）**：更新价值函数参数 w，依据具体算法，它可以是动作价值 $$Q(a \vert s; w)$$ 或状态价值 $$V(s; w)$$。
- **Actor（演员）**：按 critic 建议的方向更新策略参数 θ，即 $$\pi(a \vert s; \theta)$$。

我们来看它在一个动作价值 actor-critic 算法中是如何运作的。

1. 随机初始化 s、θ、w；采样 $$a \sim \pi(a \vert s; \theta)$$。
2. 对 t = 1… T：
	1. 采样奖励 $$r_t  \sim R(s, a)$$ 和下一个状态 $$s' \sim P(s' \vert s, a)$$。
	2. 再采样下一个动作 $$a' \sim \pi(s', a'; \theta)$$。
	3. 更新策略参数：$$\theta \leftarrow \theta + \alpha_\theta Q(s, a; w) \nabla_\theta \ln \pi(a \vert s; \theta)$$。
	4. 计算时刻 t 动作价值的修正量：<br/>
	$$G_{t:t+1} = r_t + \gamma Q(s', a'; w) - Q(s, a; w)$$ <br/>
	并用它更新价值函数参数：<br/>
	$$w \leftarrow w + \alpha_w G_{t:t+1} \nabla_w Q(s, a; w) $$。
	5. 更新 $$a \leftarrow a'$$ 与 $$s \leftarrow s'$$。

$$\alpha_\theta$$ 和 $$\alpha_w$$ 分别是策略参数更新和价值函数参数更新的两个学习率。


#### A3C

**异步优势 actor-critic**（Asynchronous Advantage Actor-Critic，Mnih et al., 2016），简称 A3C，是一种经典的策略梯度方法，其特别之处在于专注于并行训练。

在 A3C 中，critic 学习状态价值函数 $$V(s; w)$$，同时多个 actor 并行训练，并不时与全局参数同步。因此，A3C 天生就适合并行训练，比如在单台多核 CPU 机器上。

状态价值的损失函数是最小化均方误差 $$\mathcal{J}_v (w) = (G_t - V(s; w))^2$$，我们用梯度下降求最优的 w。这个状态价值函数在策略梯度更新中被用作基线。

算法流程如下：
1. 我们有全局参数 θ 和 w，以及类似的线程专属参数 θ' 和 w'。
2. 初始化时间步 t = 1
3. 当 T <= T_MAX：
	1. 重置梯度：dθ = 0 且 dw = 0。
	2. 同步线程专属参数与全局参数：θ' = θ 且 w' = w。
	3. $$t_\text{start}$$ = t，并获取 $$s_t$$。
	4. 当（$$s_t \neq \text{TERMINAL}$$）且（$$t - t_\text{start} <= t_\text{max}$$）：
		1. 选取动作 $$a_t \sim \pi(a_t \vert s_t; \theta')$$，获得新奖励 $$r_t$$ 和新状态 $$s_{t+1}$$。
		2. 更新 t = t + 1 且 T = T + 1。
	5. 初始化保存回报估计的变量 $$R = \begin{cases} 
		0 & \text{if } s_t \text{ is TERMINAL} \\
		V(s_t; w') & \text{otherwise}
		\end{cases}$$。
	6. 对 $$i = t-1, \dots, t_\text{start}$$：
		1. $$R \leftarrow r_i + \gamma R$$；这里的 R 是 $$G_i$$ 的一个 MC 度量。
		2. 累积关于 θ' 的梯度：$$d\theta \leftarrow d\theta + \nabla_{\theta'} \log \pi(a_i \vert s_i; \theta')(R - V(s_i; w'))$$；<br/>
		累积关于 w' 的梯度：$$dw \leftarrow dw + \nabla_{w'} (R - V(s_i; w'))^2$$。
	7. 用 dθ 同步更新 θ，用 dw 同步更新 w。

A3C 实现了多智能体训练的并行化。梯度累积步骤（6.2）可以看作基于 minibatch 的随机梯度更新的一种变体：w 或 θ 的值沿着每个训练线程各自的方向被独立地小幅修正。


### 进化策略

[进化策略](https://en.wikipedia.org/wiki/Evolution_strategy)（Evolution Strategies, ES）是一类与模型无关的优化方法。它通过模仿达尔文的物种自然选择进化论来学习最优解。应用 ES 有两个前提：(1) 我们的解能够自由地与环境交互，看看它们能否解决问题；(2) 我们能够计算一个**适应度**（fitness）分数来衡量每个解有多好。解决问题时，我们不必知道环境的配置。

比如说，我们从一个由随机解组成的种群开始。它们都能与环境交互，只有适应度高的候选者才能存活（*在有限资源的竞争中，只有最适者才能生存*）。然后通过重组高适应度幸存者的设置（*基因突变*）来产生新一代。如此反复，直到新的解足够好为止。

与我们上面介绍的流行的基于 MDP 的方法大不相同，ES 的目标是在不做价值近似的情况下学习策略参数 $$\theta$$。假设参数 $$\theta$$ 上的分布是一个[各向同性](https://math.stackexchange.com/questions/1991961/gaussian-distribution-is-isotropic)的多元高斯分布，均值为 $$\mu$$，固定协方差为 $$\sigma^2I$$。$$F(\theta)$$ 的梯度计算如下：

$$
\begin{aligned}
& \nabla_\theta \mathbb{E}_{\theta \sim N(\mu, \sigma^2)} F(\theta) \\
=& \nabla_\theta \int_\theta F(\theta) \Pr(\theta) && \text{Pr(.) is the Gaussian density function.} \\
=& \int_\theta F(\theta) \Pr(\theta) \frac{\nabla_\theta \Pr(\theta)}{\Pr(\theta)} \\
=& \int_\theta F(\theta) \Pr(\theta) \nabla_\theta \log \Pr(\theta) \\
=& \mathbb{E}_{\theta \sim N(\mu, \sigma^2)} [F(\theta) \nabla_\theta \log \Pr(\theta)] && \text{Similar to how we do policy gradient update.} \\
=& \mathbb{E}_{\theta \sim N(\mu, \sigma^2)} \Big[ F(\theta) \nabla_\theta \log \Big( \frac{1}{\sqrt{2\pi\sigma^2}} e^{-\frac{(\theta - \mu)^2}{2 \sigma^2 }} \Big) \Big] \\
=& \mathbb{E}_{\theta \sim N(\mu, \sigma^2)} \Big[ F(\theta) \nabla_\theta \Big( -\log \sqrt{2\pi\sigma^2} - \frac{(\theta - \mu)^2}{2 \sigma^2} \Big) \Big] \\
=& \mathbb{E}_{\theta \sim N(\mu, \sigma^2)} \Big[ F(\theta) \frac{\theta - \mu}{\sigma^2} \Big]
\end{aligned}
$$


我们可以用一个「均值」参数 $$\theta$$（与上面的 $$\theta$$ 不同；这个 $$\theta$$ 是供后续突变的基础基因）和 $$\epsilon \sim N(0, I)$$ 来改写这个公式，于是 $$\theta + \epsilon \sigma \sim N(\theta, \sigma^2)$$。$$\epsilon$$ 控制了为产生突变而加入多少高斯噪声：

$$
\nabla_\theta \mathbb{E}_{\epsilon \sim N(0, I)} F(\theta + \sigma \epsilon) = \frac{1}{\sigma} \mathbb{E}_{\epsilon \sim N(0, I)} [F(\theta + \sigma \epsilon) \epsilon]
$$


![EA](https://lilianweng.github.io/posts/2018-02-19-rl-overview/EA_RL_parallel.png)

*图 9. 一个简单的基于进化策略的并行 RL 算法。并行的工作进程共享随机种子，从而只需极小的通信带宽即可重构高斯噪声。（图片来源：Salimans et al. 2017。）*


ES 作为一种黑箱优化算法，是求解 RL 问题的另一种途径（<span style="color: #999999;">*我最初的措辞是「一个不错的替代方案」；[Seita](https://danieltakeshi.github.io/) 向我指出了这个[讨论](https://www.reddit.com/r/MachineLearning/comments/6gke6a/d_requesting_openai_to_justify_the_grandiose/dir9wde/)，于是我修改了措辞。*</span>）。它有若干优良特性（Salimans et al., 2017），使其训练快速而容易：
- ES 不需要价值函数近似；
- ES 不进行梯度反向传播；
- ES 不受延迟奖励或长期奖励的影响；
- ES 高度可并行，且数据通信量极小。


## 已知问题

### 探索-利用困境

探索与利用（exploration vs exploitation）的两难问题，我在之前的[文章](https://lilianweng.github.io/posts/2018-01-23-multi-armed-bandit/#exploitation-vs-exploration)中讨论过。当 RL 问题面对未知环境时，这一问题对于找到好的解尤为关键：探索不够，我们就无法充分了解环境；利用不够，我们就无法完成奖励优化任务。

不同的 RL 算法以不同的方式在探索与利用之间取得平衡。在 [MC](#monte-carlo-methods) 方法、[Q-learning](#q-learning-off-policy-td-control) 或许多同策略算法中，探索通常通过 [ε-贪心](https://lilianweng.github.io/posts/2018-01-23-multi-armed-bandit/#%CE%B5-greedy-algorithm)实现；在 [ES](#evolution-strategies) 中，探索则由策略参数的扰动来体现。在设计新的 RL 算法时，请把这一点考虑在内。

### 致命三要素问题

我们确实追求涉及自举的 TD 方法所带来的高效与灵活。然而，当离策略学习、非线性函数近似和自举在同一个 RL 算法中凑齐时，训练可能变得不稳定且难以收敛。这个问题被称为**致命三要素**（deadly triad）（Sutton & Barto, 2017）。人们提出了许多使用深度学习模型的架构来解决该问题，其中包括通过经验回放和周期性冻结目标网络来稳定训练的 DQN。


## 案例研究：AlphaGo Zero

几十年来，[围棋](https://en.wikipedia.org/wiki/Go_(game))一直是人工智能领域中极难的问题，直到近几年才被攻破。AlphaGo 和 AlphaGo Zero 是 DeepMind 的一个团队开发的两个程序。两者都结合了深度卷积神经网络（[CNN](https://lilianweng.github.io/posts/2017-12-15-object-recognition-part-2/#cnn-for-image-classification)）与蒙特卡洛树搜索（Monte Carlo Tree Search, MCTS），并且都被证明达到了人类职业棋手的水平。与依赖人类专家棋谱做监督学习的 AlphaGo 不同，AlphaGo Zero 只使用强化学习和自我对弈（self-play），除基本规则外不借助任何人类知识。

![围棋棋盘](https://lilianweng.github.io/posts/2018-02-19-rl-overview/go_config.png)

*图 10. 围棋棋盘。两名玩家在由 19 x 19 条线构成的棋盘的空交叉点上轮流落黑子与白子。一块棋必须至少有一个空点（交叉点，称为「气」（liberty））才能留在棋盘上，并且必须至少有两个及以上被围住的气（称为「眼」）才能保持「活」棋。任何棋子都不得重现先前的局面。*

带着上面学到的全部 RL 知识，我们来看看 AlphaGo Zero 是如何工作的。其主要组件是一个作用于棋盘局面的深度 [CNN](https://lilianweng.github.io/posts/2017-12-15-object-recognition-part-2/#cnn-for-image-classification)（确切地说，是一个带批归一化和 ReLU 的 [ResNet](https://lilianweng.github.io/posts/2017-12-15-object-recognition-part-2/#resnet-he-et-al-2015)）。这个网络输出两个值：

$$
(p, v) = f_\theta(s)
$$

- $$s$$：棋盘局面，19 x 19 x 17 的堆叠特征平面；每个位置有 17 个特征：当前玩家的 8 个历史局面（含当前）+ 对手的 8 个历史局面 + 1 个指示颜色的特征（1=黑，0=白）。我们需要专门编码颜色，因为网络在与自己对弈，当前玩家和对手的颜色会随步数切换。
- $$p$$：在 19^2 + 1 个候选动作上选择落子的概率（棋盘上 19^2 个位置，外加一手虚着（pass））。
- $$v$$：当前局面下的获胜概率。

在自我对弈过程中，MCTS 会进一步改进动作概率分布 $$\pi \sim p(.)$$，然后从改进后的策略中采样动作 $$a_t$$。奖励 $$z_t$$ 是一个二元值，指示当前玩家*最终*是否获胜。每一步棋都会生成一个回合元组 $$(s_t, \pi_t, z_t)$$，并保存到回放记忆中。受篇幅所限，本文跳过 MCTS 的细节；如果你有兴趣，请阅读原始[论文](https://www.dropbox.com/s/yva172qos2u15hf/2017-silver.pdf?dl=0)。


![AlphaGo Zero 训练](https://lilianweng.github.io/posts/2018-02-19-rl-overview/alphago-zero-selfplay.png)

*图 11. AlphaGo Zero 通过自我对弈训练，MCTS 在每一步进一步改进输出的策略。（图片来源：Silver et al., 2017 的图 1a。）*

网络用回放记忆中的样本来训练，以最小化损失：

$$
\mathcal{L} = (z - v)^2 - \pi^\top \log p + c \| \theta \|^2
$$

其中 $$c$$ 是控制 L2 惩罚强度以避免过拟合的超参数。

AlphaGo Zero 去掉了监督学习，并把相互分离的策略网络和价值网络合并为一个，从而简化了 AlphaGo。结果表明，AlphaGo Zero 在训练时间大幅缩短的情况下，取得了大幅提升的性能！我强烈建议把[这](https://pdfs.semanticscholar.org/1740/eb993cc8ca81f1e46ddaadce1f917e8000b5.pdf)[两篇](https://www.dropbox.com/s/yva172qos2u15hf/2017-silver.pdf?dl=0)论文并排对照阅读、比较它们的差异，超级有趣。

我知道这是一篇长文，但希望它值得一读。*如果你发现本文中的错误与问题，请随时通过 [lilian dot wengweng at gmail dot com] 联系我。*我们下篇文章见！:)


## 参考文献

[1] Yuxi Li. [Deep reinforcement learning: An overview.](https://arxiv.org/pdf/1701.07274.pdf) arXiv preprint arXiv:1701.07274. 2017.

[2] Richard S. Sutton and Andrew G. Barto. [Reinforcement Learning: An Introduction; 2nd Edition](http://incompleteideas.net/book/bookdraft2017nov5.pdf). 2017.

[3] Volodymyr Mnih, et al. [Asynchronous methods for deep reinforcement learning.](http://proceedings.mlr.press/v48/mniha16.pdf) ICML. 2016.

[4] Tim Salimans, et al. [Evolution strategies as a scalable alternative to reinforcement learning.](https://arxiv.org/pdf/1703.03864.pdf) arXiv preprint arXiv:1703.03864 (2017).

[5] David Silver, et al. [Mastering the game of go without human knowledge](https://www.dropbox.com/s/yva172qos2u15hf/2017-silver.pdf?dl=0). Nature 550.7676 (2017): 354.

[6] David Silver, et al. [Mastering the game of Go with deep neural networks and tree search.](https://pdfs.semanticscholar.org/1740/eb993cc8ca81f1e46ddaadce1f917e8000b5.pdf) Nature 529.7587 (2016): 484-489.

[7] Volodymyr Mnih, et al. [Human-level control through deep reinforcement learning.](https://www.cs.swarthmore.edu/~meeden/cs63/s15/nature15b.pdf) Nature 518.7540 (2015): 529.

[8] Ziyu Wang, et al. [Dueling network architectures for deep reinforcement learning.](https://arxiv.org/pdf/1511.06581.pdf) ICML. 2016.

[9] [Reinforcement Learning lectures](https://www.youtube.com/playlist?list=PL7-jPKtc4r78-wCZcQn5IqyuWhBZ8fOxT) by David Silver on YouTube.

[10] OpenAI Blog: [Evolution Strategies as a Scalable Alternative to Reinforcement Learning](https://blog.openai.com/evolution-strategies/)

[11] Frank Sehnke, et al. [Parameter-exploring policy gradients.](https://mediatum.ub.tum.de/doc/1287490/file.pdf) Neural Networks 23.4 (2010): 551-559.

[12] Csaba Szepesvári. [Algorithms for reinforcement learning.](https://sites.ualberta.ca/~szepesva/papers/RLAlgsInMDPs.pdf) 1st Edition. Synthesis lectures on artificial intelligence and machine learning 4.1 (2010): 1-103.

---

*如果你发现本文中的错误与问题，请不要犹豫，随时通过 [lilian dot wengweng at gmail dot com] 联系我，我会非常乐意立即修正！*
