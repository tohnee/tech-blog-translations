---
title: "DeepMind 在 NIPS 2017 的论文"
title_en: "DeepMind papers at NIPS 2017"
source: https://deepmind.google/blog/deepmind-papers-at-nips-2017/
site: deepmind
date: 2017-12-01
crawled: 2026-09-13
translated: 2026-09-13
---

# DeepMind 在 NIPS 2017 的论文

> 原文：[DeepMind papers at NIPS 2017](https://deepmind.google/blog/deepmind-papers-at-nips-2017/) · Google DeepMind

12 月 4 日至 9 日，数千名研究人员和专家将齐聚加利福尼亚州长滩，参加第三十一届[神经信息处理系统](https://nips.cc/)年度大会（NIPS）。

在这里你可以看到 DeepMind 研究人员将要报告的论文概览。


### 对多样行为的鲁棒模仿（Robust imitation of diverse behaviours）

**作者：** Ziyu Wang, Josh Merel, Greg Wayne, Nando de Freitas, Scott Reed, Nicolas Heess

「我们提出了一种神经网络架构，它建立在最先进的生成模型之上，能够学习不同行为之间的关系，并模仿向它展示的特定动作。经过训练后，我们的系统可以编码单个观察到的动作，并基于该演示创造出一种全新的动作。它还可以在不同类型的行为之间切换，即使从未见过这些行为之间的过渡，例如在多种行走风格之间切换。」更多内容请见[博客](https://deepmind.com/blog/article/producing-flexible-behaviours-simulated-environments)

- 阅读[论文](https://arxiv.org/abs/1707.02747)
- 欢迎在 **18:30-22:30** 前往 **Pacific Ballroom #143** 观看**海报**

### 神经网络的 Sobolev 训练（Sobolev training for neural networks）

**作者：** Wojtek Czarnecki, Simon Osindero, Max Jaderberg, Grzegorz Świrszcz, Razvan Pascanu

这篇论文展示了一种把目标函数导数的相关知识纳入深度神经网络训练的简单方法。我们证明，现代基于 ReLU 的架构非常适合此类任务，并在三个问题上评估了它们的有效性——低维回归、策略蒸馏，以及使用合成梯度进行训练。我们观察到训练效率显著提升，尤其是在低数据量的情形下，并且训练出了第一个基于合成梯度的 ImageNet 模型，其准确率接近最先进水平。

- 阅读[论文](https://arxiv.org/abs/1706.04859)
- 欢迎在 **18:30-22:30** 前往 **Pacific Ballroom #139** 观看**海报**


### 滤波变分目标（Filtering variational objectives）

**作者：** Chris J. Maddison, Dieterich Lawson, George Tucker, Nicolas Heess, Mohammad Norouzi, Andriy Mnih, Arnaud Doucet, Yee Whye Teh

我们考虑将变分下界扩展为一族由粒子滤波器对边际似然的估计量定义的下界——即滤波变分目标。这些滤波目标能够利用模型的时序结构，形成更紧的下界，并为深度生成模型的模型学习提供更好的目标。在实验中，我们发现使用滤波目标进行训练，相比用变分下界训练同一模型架构带来了显著的改进。

- 阅读[论文](https://arxiv.org/abs/1705.09279)
- 欢迎在 **18:30-22:30** 前往 **Pacific Ballroom #114** 观看**海报**

### 视觉交互网络：从视频学习物理模拟器（Visual interaction networks: Learning a physics simulator from video）

**作者：** Nicholas Watters, Andrea Tacchetti, Theophane Weber, Razvan Pascanu, Peter Battaglia, Daniel Zoran

「在这项工作中，我们开发了『视觉交互网络』（Visual Interaction Network，VIN），这是一种无需先验知识即可学习物理动力学的神经网络模型。VIN 能够仅凭几帧视频推断出多个物理对象的状态，然后用它们预测未来许多步的对象位置。它还能推断出不可见对象的位置，并学习依赖于质量等对象属性的动力学。」更多细节请阅读[博客](https://deepmind.com/blog/article/neural-approach-relational-reasoning)。

- 阅读[论文](https://arxiv.org/abs/1706.01433)
- 欢迎在 **18:30-22:30** 前往 **Pacific Ballroom #123** 观看**海报**

### 神经离散表示学习（Neural discrete representation learning）

**作者：** Aäron van den Oord, Oriol Vinyals, Koray Kavukcuoglu

在没有监督的情况下学习有用的表示，仍然是机器学习中的一个关键挑战。在这项工作中，我们提出了一个简单而强大的生成模型——向量量化变分自编码器（Vector Quantised Variational AutoEncoder，VQ-VAE）——来学习这样的离散表示。当这些表示与自回归先验配对时，该模型能够生成高质量的图像、视频和语音，还能完成高质量的说话人转换。

- 阅读[论文](https://arxiv.org/abs/1711.00937)
- 欢迎在 **18:30-22:30** 前往 **Pacific Ballroom #116** 观看**海报**

### 生成模型中的变分内存寻址（Variational memory addressing in generative models）

**作者：** Jörg Bornschein, Andriy Mnih, Daniel Zoran, Danilo Jimenez Rezende

基于注意力的记忆可以用来增强神经网络，以支持小样本学习、快速适应性，以及更普遍地支持非参数化扩展。我们没有使用流行的可微软注意力机制，而是提出在生成模型中使用随机硬注意力来检索记忆内容。这使我们能够把变分推断应用于内存寻址，从而利用目标信息获得精确得多的内存查找，尤其是在拥有大容量内存缓冲区且内存中存在大量干扰条目的模型中。

- 阅读[论文](https://arxiv.org/abs/1709.07116)
- 欢迎在 **18:30-22:30** 前往 **Pacific Ballroom #117** 观看**海报**


### REBAR：离散潜变量模型的低方差无偏梯度估计（REBAR: Low-variance, unbiased gradient estimates for discrete latent variable models）

**作者：** George Tucker, Andriy Mnih, Chris J Maddison, Dieterich Lawson, Jascha Sohl-Dickstein

由于梯度估计量方差很高，在含离散潜变量的模型中学习颇具挑战。以往的方法要么产生高方差的无偏梯度，要么产生低方差的有偏梯度。REBAR 使用控制变量法和重参数化技巧兼得两者之长：低方差的无偏梯度，从而更快地收敛到更好的结果。

- 阅读[论文](https://arxiv.org/abs/1703.07370)
- 参加 **Hall A** **10:35-10:50** 的**口头报告**专场
- 欢迎在 **06:30-22:30** 前往 **Pacific Ballroom #178** 观看**海报**

### 面向深度强化学习的想象力增强智能体（Imagination-augmented agents for deep reinforcement learning）

**作者：** Sébastien Racanière, Théophane Weber, David P. Reichert, Lars Buesing, Arthur Guez, Danilo Rezende, Adria Puigdomènech Badia, Oriol Vinyals, Nicolas Heess, Yujia Li, Razvan Pascanu, Peter Battaglia, Demis Hassabis, David Silver, Daan Wierstra.

「我们描述了一族全新的基于想象的规划方法……我们还引入了新的架构，为智能体提供学习和构建计划的新方式，以最大化任务效率。这些架构高效、对复杂且不完美的模型具有鲁棒性，并能采用灵活的策略来利用它们的想象力。我们引入的智能体受益于一个『想象编码器』——一个学习提取任何对智能体未来决策有用信息、同时忽略无关内容的神经网络。」更多内容请见[博客](https://deepmind.com/blog/article/agents-imagine-and-plan)。

- 阅读[论文](https://arxiv.org/abs/1707.06203)
- 参加 **Hall A** **15:05-15:20** 的**口头报告**专场
- 欢迎在 **18:30-22:30** 前往 **Pacific Ballroom #139** 观看**海报**

### 用于关系推理的简单神经网络模块（A simple neural network module for relational reasoning）

**作者：** Adam Santoro, David Raposo, David Barrett, Mateusz Malinowski, Razvan Pascanu, Peter Battaglia, Timothy Lillicrap

「我们展示了一个简单、即插即用的神经网络模块，可用于解决需要复杂关系推理的任务。这个模块被称为关系网络（Relation Network），它可以接收非结构化的输入——比如图像或故事——并对其中蕴含的关系进行隐式推理。」更多内容请见[博客](https://deepmind.com/blog/article/neural-approach-relational-reasoning)。

- 阅读[论文](https://arxiv.org/abs/1706.01427)
- 收听 **Hall A** **15:25-15:30** 的**亮点报告**（spotlight）
- 欢迎在 **18:30-22:30** 前往 **Pacific Ballroom #129** 观看**海报**

### 使用深度集成进行简单且可扩展的预测不确定性估计（Simple and scalable predictive uncertainty estimation using deep ensembles）

**作者：** Balaji Lakshminarayanan, Alexander Pritzel, Charles Blundell

量化神经网络（NN）的预测不确定性是一个具有挑战性且尚未解决的问题。大多数工作聚焦于贝叶斯方案，但这些方案计算量大，且需要对训练流程进行大幅修改。我们提出了一种贝叶斯神经网络的替代方案：实现简单、易于并行、几乎不需要超参数调节，并能产生高质量的预测不确定性估计。通过在分类和回归基准上的一系列实验，我们证明我们的方法能产生校准良好的不确定性估计，其表现与近似贝叶斯神经网络相当甚至更好。

- 阅读[论文](https://arxiv.org/abs/1612.01474)
- 收听 **Hall A** **15:45-15:50** 的**亮点报告**（spotlight）
- 欢迎在 **18:30-22:30** 前往 **Pacific Ballroom #133** 观看**海报**

### 自然价值近似器：学习何时信任过去的估计（Natural value approximators: learning when to trust past estimates）

**作者：** Zhongwen Xu, Joseph Modayil, Hado van Hasselt, Andre Barreto, David Silver, Tom Schaul

我们重新审视了强化学习中价值近似器的结构，其出发点是一个观察：典型的价值近似器随输入平滑变化，而真实价值会在奖励到来时发生突变。我们提出的方法旨在通过带投影价值估计的插值来拟合这种非对称的不连续性。

- 阅读[论文](http://papers.nips.cc/paper/6807-natural-value-approximators-learning-when-to-trust-past-estimates)
- 收听 **Hall A** **17:25-17:30** 的**亮点报告**（spotlight）
- 欢迎在 **18:30-22:30** 前往 **Pacific Ballroom #6** 观看**海报**

### 用于强化学习迁移的后继特征（Successor features for transfer in reinforcement learning）

**作者：** Andre Barreto, Will Dabney, Remi Munos, Jonathan Hunt, Tom Schaul, David Silver, Hado van Hasselt.

我们提出了一个强化学习的迁移框架。我们的方法建立在两个关键思想上：「后继特征（successor features）」——一种把环境动力学与奖励解耦的价值函数表示；以及「广义策略改进（generalised policy improvement）」——动态规划中策略改进步骤的推广，它考虑的是一组策略而非单个策略。两者结合，形成了一种能够无缝融入强化学习框架的方法，使任务之间的迁移不受任何限制。

- 阅读[论文](https://arxiv.org/abs/1606.05312)
- 收听 **Hall A** **17:40-17:45** 的**亮点报告**（spotlight）
- 欢迎在 **18:30-22:30** 前往 **Pacific Ballroom #9** 观看**海报**

### 基于人类偏好的深度强化学习（Deep reinforcement learning from human preferences）

**作者：** Paul Christiano (Open AI), Jan Leike, Tom B. Brown, Miljan Martic, Shane Legg, Dario Amodei (Open AI)

「技术 AI 安全的一个核心问题是：如何告诉一个算法我们想让它做什么。我们与 OpenAI 合作，展示了一套新颖的系统，它能让没有任何技术经验的人教会 AI 如何完成复杂任务，比如操纵一只模拟的机械臂。」更多内容请见[博客](https://deepmind.com/blog/article/learning-through-human-feedback)。

- 阅读[论文](https://arxiv.org/abs/1706.03741)
- 欢迎在 **18:30-22:30** 前往 **Pacific Ballroom #1** 观看**海报**

### 公共资源占用的多智能体强化学习模型（A multi-agent reinforcement learning model of common-pool resource appropriation）

**作者：** Julien Perolat, Joel Z Leibo, Vinicius Zambaldi, Charles Beattie, Karl Tuyls, Thore Graepel

这篇论文研究了公共资源占用问题的复杂性。这些问题涉及渔业、牧场或淡水获取等系统——大量的人或行为者都可以使用同一种资源。社会科学中的传统模型往往表明，能够获取资源的一方会以自利的方式行事，最终导致资源被不可持续地耗尽。然而，从人类社会我们知道，实际存在多种多样的可能结果。渔业等资源有时被过度开发，有时却被可持续地收获。在这项工作中，我们提出了新的建模技术，可用于旨在解释现实世界观察与传统模型预测之间这一差距的研究。

- 阅读[论文](https://arxiv.org/abs/1707.06600)
- 欢迎在 **18:30-22:30** 前往 **Pacific Ballroom #86** 观看**海报**

### DisTraL：鲁棒的多任务强化学习（DisTraL: Robust multitask reinforcement learning）

**作者：** Yee Whye Teh, Victor Bapst, Wojciech Czarnecki, John Quan, James Kirkpatrick, Raia Hadsell, Nicholas Heess, Razvan Pascanu

我们开发了一种在多个任务上进行强化学习的方法。其假设是这些任务彼此相关（例如处于同一环境或拥有相同的物理规则），因此良好的动作序列往往会在不同任务间反复出现。我们的方法通过两个机制实现这一点：一方面把任务专属策略同时蒸馏进一个共同的默认策略，另一方面通过把所有任务专属策略向默认策略正则化，将这一共同知识跨任务迁移。我们证明这能带来更快、更鲁棒的学习。

- 阅读[论文](https://arxiv.org/abs/1707.04175)
- 欢迎在 **18:30-22:30** 前往 **Pacific Ballroom #138** 观看**海报**

### 多智能体强化学习的统一博弈论方法（A unified game-theoretic approach to multiagent reinforcement learning）

**作者：** Marc Lanctot, Vinicius Zambaldi, Audrunas Gruslys, Angeliki Lazaridou, Karl Tuyls, Julien Perolat, David Silver, Thore Graepel

在这项工作中，我们首先观察到独立的强化学习器所产生的策略可能存在联合相关性，导致在与其他智能体共同执行时无法很好地泛化。我们通过提出一个名为「联合策略相关性（joint policy correlation）」的新指标来量化这一效应。随后，我们提出了一种以博弈论基础为启发的算法，它推广了此前的多种方法，如虚拟对弈（fictitious play）、迭代最优响应（iterated best response）、独立强化学习和双重预言机（double oracle）。我们证明，该算法能在第一人称协调博弈中显著降低联合策略相关性，并在一个常见扑克基准博弈中找到鲁棒的对抗策略。

- 阅读[论文](https://arxiv.org/abs/1711.00832)
- 欢迎在 **18:30-22:30** 前往 **Pacific Ballroom #203** 观看**海报**

我们的研究人员还将在 NIPS 期间主持并参与形式多样的工作坊、教程和研讨会。完整日程（包括我们参与合作的论文详情）请下载我们的[行程表](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/deepmind-papers-at-nips-2017/DeepMind_Itinerary_NIPS2017.pdf)（PDF），或访问[官方网站](https://nips.cc/)。
