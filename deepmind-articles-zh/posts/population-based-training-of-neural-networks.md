---
title: "神经网络的基于种群的训练（PBT）"
title_en: "Population based training of neural networks"
source: https://deepmind.google/blog/population-based-training-of-neural-networks/
site: deepmind
date: 2017-11-27
crawled: 2026-09-13
translated: 2026-09-13
---

# 神经网络的基于种群的训练（PBT）

> 原文：[Population based training of neural networks](https://deepmind.google/blog/population-based-training-of-neural-networks/) · Google DeepMind

神经网络已经取得了巨大成功，从围棋和雅达利（Atari）游戏到图像识别和语言翻译，无所不包。但常被忽视的一点是：神经网络在特定应用上的成功，往往取决于研究开始之初作出的一系列选择，包括使用什么类型的网络，以及用什么数据和方法来训练它。目前，这些选择——被称为超参数（hyperparameters）——是凭借经验、随机搜索或计算密集型的搜索过程来确定的。

在[最新论文](https://arxiv.org/abs/1711.09846)中，我们提出了一种训练神经网络的新方法，让实验者能够快速为任务挑选出最佳的超参数组合和模型。这项技术——称为基于种群的训练（Population Based Training，PBT）——同时训练并优化一系列网络，从而快速找到最优设置。关键在于，它不增加任何计算开销，可以像传统技术一样快，并且易于集成到现有的机器学习流程中。

这项技术是超参数优化中最常用的两种方法——随机搜索和手工调参——的混合体。在随机搜索中，一群神经网络被独立地并行训练，训练结束时选出表现最好的模型。通常，这意味着种群中只有一小部分网络是用好的超参数训练的，而更多的网络用的是坏的超参数，白白浪费了计算资源。

![示意图，展示三条彼此独立的并行训练：固定的超参数随着时间推移影响每个模型的顺序训练进展与最终性能。](https://lh3.googleusercontent.com/n8IJcqZq44hIxXNPS5X5mh3XLwyP18Q_WHZ7iHWhw1u9pWbIwiFBVtl5vQvs3ut1WMLa40RdH6mFx8q-4UlX7X7T9dZLk75svweGbtJ8yPXbHyfUfg=w1440)

超参数的随机搜索：许多超参数被并行尝试，但彼此独立。有些超参数会产生性能良好的模型，有些则不然

而在手工调参中，研究人员必须先猜测最佳超参数，再用它们训练模型，然后评估性能。如此反复进行，直到研究人员对网络的表现满意为止。虽然这可以带来更好的性能，但缺点是耗时漫长，有时需要数周甚至数月才能找到完美设置。尽管有一些方法可以让这一过程自动化——例如贝叶斯优化——它依然耗时很长，并且需要多次顺序的训练运行才能找到最佳超参数。

![示意图，展示基于种群的训练的顺序过程：随时间推移，模型的超参数与参数被周期性评估，表现不佳的模型从更好的模型复制参数并探索新的超参数。](https://lh3.googleusercontent.com/2w0BX5atTa8QeO3UMI_YnmUERKWEsSyM1AWuaGOq34zbZEwFWpd_PUhO6v-kqmYL-EvihLvzLdQTCacadJBoLlGIlwXiWDEbPGpI7LiUJQAwZqbxXdE=w1440)

手工调参和贝叶斯优化等方法要通过顺序观察多次训练运行来修改超参数，因此这些方法速度很慢

PBT 与随机搜索一样，一开始就用随机超参数并行训练许多神经网络。但与各网络独立训练不同，它利用种群中其他成员的信息来改进超参数，并把计算资源导向展现出潜力的模型。它的灵感来自遗传算法：种群中的每个成员——称为 worker（工作进程）——可以利用种群中其余成员的信息。例如，一个 worker 可以从表现更好的 worker 那里复制模型参数。它还可以通过随机改变当前取值来探索新的超参数。

随着神经网络种群的训练推进，这种利用（exploit）与探索（explore）的过程被周期性地执行，确保种群中所有 worker 都具备良好的基础性能，同时也保证新的超参数得到持续探索。这意味着 PBT 能够快速利用好的超参数，可以把更多训练时间分配给有潜力的模型，而且至关重要的是，它能在整个训练过程中自适应地调整超参数取值，从而自动学习出最佳配置。

![示意图，展示基于种群的训练的顺序过程：模型的超参数与参数被周期性评估，表现不佳的模型从更好的模型复制参数（利用）并探索新的超参数（探索）。](https://lh3.googleusercontent.com/1GRFJPRkeWtdSv5qwjD3GCdaz7f-tOn3OPRlEfy-f6UFQq21JPhntOFFQygaD_SOtj3kPg_nRCRSLX20ILUOeW-SNucc5w-bKCcctIm2n8U3iJwCsA=w1440)

神经网络的基于种群的训练像随机搜索一样开始，但允许 worker 随训练推进利用其他 worker 的阶段性成果并探索新的超参数

我们的实验表明，PBT 在众多任务和领域都非常有效。例如，我们在 DeepMind Lab、Atari 和《星际争霸 II》的一整套富有挑战性的强化学习问题上，用最先进的方法对该算法进行了严格测试。在所有情形中，PBT 都稳定了训练过程，快速找到好的超参数，并交出了超越最先进基线的结果。

![五幅柱状图，对比标准基线（灰色柱）与基于种群的训练（蓝色分段）在不同任务上的表现：DM Lab（UNREAL vs PBT：0.93 到 1.06）、Atari（FuN vs PBT：1.47 到 1.81）、StarCraft II（A3C vs PBT：0.36 到 0.39）、机器翻译（Transformer BLEU 分数：22.30 到 22.65）以及 GAN（DCGAN Inception 分数：6.45 到 6.89）。PBT 在所有任务上均稳定地提升了性能。](https://lh3.googleusercontent.com/EybG_XFyyq3Z_iCavC6IHKnQeRiOPPAwAK2jemU82uqs-aruFYty83jqXcTv9ImhXdy7UOcW7llX1cKC1VDarkdmqP5Eo5rbsopidEWpF3F13N3H4g=w1440)

我们还发现 PBT 对训练生成对抗网络（GAN）非常有效，而 GAN 是出了名的难以调参。具体而言，我们用 PBT 框架最大化 Inception Score——一种视觉保真度的度量——结果从 6.45 显著提升到 6.9。

我们还把它应用于谷歌最先进的机器翻译神经网络之一。这类网络通常要用精心手工调制的超参数时间表来训练，而调制这些时间表需要数月才能完善。借助 PBT，我们自动找到了与现有性能相当甚至更优的超参数时间表，而且无需任何调参，所用时间也只相当于做一次训练运行。

![动画可视化，对比基于种群的训练（PBT）过程中 GAN 种群的发展（左侧，以 Inception Score 衡量）与 FuN 种群的发展（右侧，以累积期望奖励衡量）。两个面板都展示了训练运行的分支树，说明随着时间推移，表现不佳的模型如何被剪枝，并通过复制（利用）和变异（探索）表现更好的运行的超参数而被替换，从而带来整体性能的提升。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622672bd27482f02e110af3b_PBT205.gif)

CIFAR-10 上训练 GAN 以及 Ms Pacman 上训练 Feudal Networks（FuN）期间种群演化。粉点代表初始智能体，蓝点代表最终智能体。

我们相信，这项技术才刚刚起步。在 DeepMind，我们还发现 PBT 对于训练引入了新超参数的新算法和神经网络架构尤其有用。随着我们继续完善这一流程，它为发现和开发更精密、更强大的神经网络模型提供了可能。

**说明**

阅读[完整论文](https://arxiv.org/abs/1711.09846)。

这项工作由 Max Jaderberg、Valentin Dalibard、Simon Osindero、Wojciech M. Czarnecki、Jeff Donahue、Ali Razavi、Oriol Vinyals、Tim Green、Iain Dunning、Karen Simonyan、Chrisantha Fernando 和 Koray Kavukcuoglu 完成。
