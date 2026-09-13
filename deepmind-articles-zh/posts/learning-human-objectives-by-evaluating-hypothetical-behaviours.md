---
title: "通过评估假设行为学习人类目标"
title_en: "Learning human objectives by evaluating hypothetical behaviours"
source: https://deepmind.google/blog/learning-human-objectives-by-evaluating-hypothetical-behaviours/
site: deepmind
date: 2019-12-13
crawled: 2026-09-13
translated: 2026-09-13
---

# 通过评估假设行为学习人类目标

> 原文：[Learning human objectives by evaluating hypothetical behaviours](https://deepmind.google/blog/learning-human-objectives-by-evaluating-hypothetical-behaviours/) · Google DeepMind

TL;DR：我们提出了一种方法，用于在存在未知不安全状态的情况下，基于人类反馈训练强化学习智能体。

当我们在真实世界中训练强化学习（RL）智能体时，我们不希望它们探索不安全的状态，比如把移动机器人开进沟里，或者给上司写一封令人尴尬的邮件。在不安全状态存在的情况下训练 RL 智能体，被称为[安全探索问题（safe exploration problem）](http://www.jmlr.org/papers/volume16/garcia15a/garcia15a.pdf)。我们着手解决的是这个问题最困难的版本：智能体一开始既不知道环境如何运作，也不知道不安全状态在哪里。它只有一个信息来源：人类用户关于不安全状态的反馈。

[现有](https://deepmind.com/blog/article/learning-through-human-feedback)[的](https://arxiv.org/abs/1709.10163)[多种](https://arxiv.org/abs/1701.06049)[基于](https://arxiv.org/abs/1811.06521)[人类反馈训练智能体的方法](https://bair.berkeley.edu/blog/2019/05/28/end-to-end/)都会请用户去评估智能体在环境中行动的数据。也就是说——为了了解不安全状态，智能体必须先访问这些状态，用户才能对其提供反馈。这使得先前的工作无法适用于需要安全探索的任务。

在[最新论文](https://arxiv.org/abs/1912.05652)中，我们提出了一种分两阶段运行的[奖励建模（reward modeling）](https://medium.com/@deepmindsafetyresearch/scalable-agent-alignment-via-reward-modeling-bf4ab06dfd84)方法。第一阶段，系统被鼓励通过合成生成的假设行为去探索广泛的状态。用户对这些假设行为提供反馈，系统以交互方式学习用户奖励函数的模型。只有当模型成功地学会预测奖励和不安全状态之后，我们才部署一个安全执行目标任务的 RL 智能体。

我们从一个初始状态的生成模型和一个前向动力学模型开始，它们在离策略数据（如随机轨迹或安全的专家示范）上训练。我们的方法利用这些模型来合成假设行为，请用户为这些行为标注奖励，然后训练一个神经网络来预测这些奖励。关键思路是主动地从零开始合成假设行为，使其信息量尽可能大，**而无需与环境交互**。我们把这种方法称为基于轨迹优化的奖励查询合成（reward query synthesis via trajectory optimisation，ReQueST）。

![ReQueST 的系统示意图：一个「生成模型」输入到一个三步训练循环中，包括「假设行为」「用户反馈」和「奖励模型」，最终输出一个训练好的「RL 智能体」。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62273c70cd838a48a117c932_Human20Objectives2002.svg)

ReQueST：我们在不安全状态存在的情况下，让智能体行为与用户目标安全对齐的方法。(1) 利用一个动力学模型，(2) 通过用户对假设行为的反馈以交互方式学习奖励模型，(3) 然后部署一个基于模型的 RL 智能体来优化学到的奖励。

## 利用轨迹优化合成信息量大的假设行为

要让这种方法奏效，我们需要系统能够模拟和探索广泛的行为，以有效训练奖励模型。为了鼓励奖励模型训练期间的探索，ReQueST 使用梯度下降轨迹优化来合成**四种不同类型的假设行为**。第一种假设行为**最大化奖励模型集成的不确定性**，为信息价值最高的行为引出用户标注。第二种假设行为**最大化预测奖励**，让奖励模型可能错误预测高奖励的行为浮出水面；即[奖励作弊（reward hacking）](https://openai.com/blog/faulty-reward-functions/)。第三种假设行为**最小化预测奖励**，把潜在不安全的假设行为加入训练数据。这些数据使奖励模型能够了解不安全状态。第四种假设行为**最大化轨迹的新颖性**，鼓励探索广泛的状态，而不论预测奖励如何。

## 用监督学习训练奖励模型

每个假设行为由一串状态转移 (s, a, s') 组成。我们请用户为每个状态转移标注一个奖励 r。然后，给定标注好的转移数据集 (s, a, r, s')，我们使用最大似然目标训练一个神经网络来预测奖励。我们采用基于梯度下降的标准监督学习技术。

## 部署基于模型的 RL 智能体

一旦用户对奖励模型满意，我们就部署一个基于规划的智能体，它使用模型预测控制（MPC）来选择能优化学到的奖励的动作。与通过试错学习的无模型 RL 算法（如 Q-learning 或策略梯度方法）不同，MPC 这类基于模型的 RL 算法让智能体在部署期间能够借助动力学模型预判自身动作的后果，从而避开不安全状态。

## 实验评估

我们在一个基于状态的二维导航任务和基于图像的 Car Racing 视频游戏上，用模拟用户对 ReQueST 进行评估。结果表明，ReQueST 满足三项重要的安全性质：它可以**在不访问不安全状态的情况下训练出能检测这些状态的奖励模型**；它可以在部署智能体之前**纠正奖励作弊**；并且它倾向于学习出稳健的奖励模型，**迁移到新环境中仍表现良好**。

## 在玩具级二维导航任务中测试泛化能力

为了测试奖励模型的泛化能力，我们搭建了一个带有独立训练环境和测试环境的二维导航任务。

![一幅二维导航网格图，展示智能体从 (0,0) 到 (1,1) 的路径。该路径由一串蓝色阴影的点表示，成功地绕开了两个圆形障碍区域——一个位于左下角附近、以绿色描边，另一个位于右上角附近、以红色描边。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62273c9689c64cb11491faa9_Human20Objectives2003.svg)

在这个二维导航环境中，智能体必须到达目标区域（绿色），同时避开陷阱区域（红色）。

我们有意在初始状态分布上引入了显著的偏移：智能体在训练环境中从左下角 (0, 0) 出发，而在测试环境中从右上角 (1, 1) 出发。那些通过在训练环境中部署智能体来收集数据的先前方法，不太可能了解到右上角的陷阱，因为它们会立即找到目标，然后便不再继续探索。ReQueST 则合成了各种各样的假设状态，包括陷阱内部及其周边的状态。用户为这些状态标注奖励，ReQueST 借此学习出一个稳健的奖励模型，使智能体能够在测试环境中绕开陷阱。

![两幅热图，展示二维环境中的预测奖励。ReQueST（左图）成功标出了右上角的高惩罚红色区域；基线方法（右图）呈现均匀的蓝色区域，未能检测到惩罚区域。](https://lh3.googleusercontent.com/-qRWWy1MBo7Bo8kQbhUkpW5GnLARMa1wPL-tcmoxwzcDRJk6aYRIeEpJEIBMbE7TUk2Oo_aQlmyICKVYlWJyDIKh_KqS4P4Z3YIUkgE0_AFg8M0cBg=w1440)

ReQueST 学到的奖励模型准确刻画了目标区域和陷阱区域的边界。从先前工作改编的其他方法则没有学到陷阱区域，并且错误地把目标区域外推了出去。

![折线图，对比各模型在二维导航测试环境中的成功率与查询次数的关系。ReQueST（蓝色实线带阴影方差）在查询次数增加时保持 0.6 到 0.8 左右的高成功率，而随机策略（橙色线）等基线方法始终停留在 0.0 的成功率。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62273cc7c19b8f0dd6876f5b_Human20Objectives2005.svg)

![折线图，对比二维导航测试环境中的碰撞率与查询次数的关系。ReQueST（深蓝色实线带蓝色阴影方差）随查询次数增加从 0.9 的碰撞率陡降至接近 0.0，而随机轨迹（青绿色）和奖励最大化轨迹（橙色）等基线方法的碰撞率保持在 0.7 到 0.9 之间的高位。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62273cd61bcb8d8cf2992691_Human20Objectives2006.svg)

ReQueST（蓝色）产生的智能体，成功率显著高于从先前工作改编的基线方法（青绿色和橙色）。尤其值得一提的是，ReQueST 学到的奖励模型对不安全状态的检测足够准确，使智能体能够完全避开它们（0% 碰撞率）。

## 在基于图像的 Car Racing 中测试可扩展性

为了检验 ReQueST 能否扩展到像图像这样具有高维连续状态的领域，我们使用了 OpenAI Gym 中的 [Car Racing](https://gym.openai.com/envs/CarRacing-v0/) 视频游戏。

![一幅简单的电脑游戏画面中，一辆赛车沿赛道行驶。它先沿赛道左转，再右转，随后失控旋转冲进了路边的草地。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62273cf6c19b8f617c878ea4_Human20Objectives2007.gif)

在 Car Racing 环境中，智能体必须访问尽可能多的路面区块，同时避开草地。

![Car Racing 的四个片段并排展示。第一个片段设置为最大化不确定性，赛车沿着道路中线或刚出路边行驶。第二个片段设置为最大化奖励，赛车在赛道上经过几个急弯。第三个片段最小化奖励，赛车立即驶上草地。第四个片段最大化新颖性，赛车停在道路中央。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62273d6556f2230ed678811b_Human20Objectives2008.gif)

ReQueST 合成的假设行为分别是：(1) 最大化奖励不确定性，(2) 最大化预测奖励，(3) 最小化预测奖励，(4) 最大化新颖性。这些视频展示的是由完全训练好的奖励模型合成的假设，使用了 VAE 图像解码器和 LSTM 动力学模型。最大化不确定性的行为显示赛车驶向路边并减速。最大化奖励的行为显示赛车沿路行驶并转弯。最小化奖励的行为显示赛车尽快冲出道路。最大化新颖性的行为显示赛车保持静止。

![折线图，展示 Car Racing 环境中的奖励与查询次数的关系。ReQueST（蓝色实线带阴影方差）取得了最高的奖励，峰值接近 1700，优于随机轨迹（绿色）和奖励最大化轨迹（橙色）等保持在 1000 以下的基线方法。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62273d864fecbb5cf935777d_Human20Objectives2009.svg)

ReQueST（蓝色）产生的智能体，在驶向新的路面区块和避开草地方面的表现显著优于从先前工作改编的方法（青绿色和橙色）。

除了将 ReQueST 与先前方法进行基准比较之外，我们还进行了一次超参数扫描和消融研究：在轨迹优化中改变动力学模型的正则化强度以及所合成假设行为的子集，以衡量 ReQueST 对这些设置的敏感度。我们发现，ReQueST 可以在生成「真实」与「有信息量」的查询之间进行权衡，而最优权衡点因领域而异。我们还发现，四种假设行为各自的有用程度取决于具体领域和收集到的训练数据量。

## 下一步是什么？

据我们所知，ReQueST 是第一个能够安全地学习不安全状态、并能扩展到在高维连续状态环境中训练神经网络奖励模型的奖励建模算法。

ReQueST 依赖于初始状态的生成模型和前向动力学模型，而对于具有复杂动力学的视觉领域，这两者可能难以获得。到目前为止，我们只在动力学相对简单的模拟环境中展示了 ReQueST 的有效性。未来的一个方向是在物理更真实、环境中还有其他智能体活动的三维领域中测试 ReQueST。

**注释**

如果你想了解更多，请查看我们的 [arXiv 预印本](https://arxiv.org/abs/1912.05652)：Siddharth Reddy, Anca D. Dragan, Sergey Levine, Shane Legg, Jan Leike, Learning Human Objectives by Evaluating Hypothetical Behavior, arXiv, 2019。

为鼓励复现与扩展，我们已开源[代码](https://github.com/rddy/ReQueST)。

欢迎收听我们的[播客](https://deepmind.com/blog/article/podcast-episode-4-ai-robot)，进一步了解 DeepMind 对构建安全 AI 的承诺。

感谢 Zac Kenton 和 Kelly Clancy 对本文早期草稿的反馈，感谢 Paulo Estriga 的设计工作。
