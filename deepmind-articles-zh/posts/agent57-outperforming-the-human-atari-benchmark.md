---
title: "Agent57：超越人类 Atari 基准"
title_en: "Agent57: Outperforming the human Atari benchmark"
source: https://deepmind.google/blog/agent57-outperforming-the-human-atari-benchmark/
site: deepmind
date: 2020-03-31
crawled: 2026-09-13
translated: 2026-09-13
---

# Agent57：超越人类 Atari 基准

> 原文：[Agent57: Outperforming the human Atari benchmark](https://deepmind.google/blog/agent57-outperforming-the-human-atari-benchmark/) · Google DeepMind

Atari57 游戏套件是一个由来已久的基准，用于衡量智能体在广泛任务上的性能。

我们开发了 [Agent57](https://arxiv.org/abs/2003.13350)，这是首个在全部 57 款 Atari 2600 游戏上都取得高于人类基线分数的深度强化学习智能体。Agent57 把一种高效探索算法与一个元控制器（meta-controller）相结合，后者可以自适应地调整智能体的探索以及长期与短期行为。

## 如何衡量通用人工智能？

在 DeepMind，我们感兴趣的是构建能在广泛任务上表现出色的智能体。一个在足够宽的任务范围上表现得足够好的智能体，就可以被归类为[智能的](https://arxiv.org/pdf/0706.3639.pdf)。游戏是构建自适应算法的绝佳试验场：它们提供了一整套丰富的任务，玩家必须发展出复杂的行为策略才能驾驭；同时它们还提供了一个便于衡量进展的指标——游戏分数——可供优化。最终目标并不是开发擅长游戏的系统，而是把游戏当作垫脚石，开发出能够学会应对广泛挑战的系统。通常，人类表现被作为任务上「足够好」的基线：智能体在每个任务上获得的分数可以相对于有代表性的人类表现来度量，得到一个人工归一化分数：0% 表示智能体表现与随机无异，100% 或以上表示智能体的表现达到或超过人类水平。

2012 年，[街机学习环境（Arcade Learning Environment）](https://arxiv.org/abs/1207.4708)——包含 57 款 Atari 2600 游戏（称为 Atari57）——被提出作为一套基准任务：这些经典的 Atari 游戏为智能体提出了广泛的挑战。研究界普遍使用这一基准来衡量构建日益智能的智能体的进展。人们往往希望把智能体在广泛任务上的表现概括为单个数字，因此在 Atari57 基准上的平均表现（所有游戏的均值或中位数）常被用来总结智能体的能力。平均分数随时间不断上升。遗憾的是，平均表现无法反映智能体在多少个任务上表现出色，因此它并不是判断智能体「通用程度」的好统计量：它只能说明智能体表现得足够好，却不能说明它在足够宽的任务集合上都表现得足够好。所以尽管平均分数不断上升，截至目前，高于人类水平的游戏数量却并没有增加。举个直观的例子：设想一个由二十个任务组成的基准。假设智能体 A 在八个任务上得到 500%，在四个任务上得到 200%，在八个任务上得到 0%（均值 = 240%，中位数 = 200%），而智能体 B 在所有任务上都得到 150%（均值 = 中位数 = 150%）。平均来看，智能体 A 比智能体 B 表现更好。然而，智能体 B 具有更通用的能力：它在比智能体 A 更多的任务上达到人类水平的表现。

![两张横向柱状图，比较智能体 A 与智能体 B 在 20 款游戏上的表现。智能体 A 的分数在 0 到 500 之间大幅波动，均值 240，中位数 200，第 5 百分位为 0。智能体 B 的所有分数一致为 150，因此第 5 百分位、中位数与均值都等于 150。两张图中均有一条粉色虚线标出位于 100 的「平均人类」基线。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62274e3d1abb0e3acb26be8e_Fig201.svg)

图 1：两个假想智能体在同一组 20 个任务的基准上均值、中位数与第 5 百分位表现的示意。

如果某些任务远比其他任务容易，这一问题会进一步加剧。通过在非常容易的任务上表现极佳，智能体 A 可以表面上胜过在容易和困难任务上都表现良好的智能体 B。

中位数较少受少数简单游戏中异常出色表现的扭曲——作为指示[分布中心](https://en.wikipedia.org/wiki/Central_tendency)的统计量，它比均值更[稳健](https://en.wikipedia.org/wiki/Robust_statistics)。然而，在衡量通用性时，分布的尾部变得更加重要，尤其是当任务数量更大时。例如，在最难的 5% 游戏上的表现度量，可能更能代表一个智能体的通用程度。

自 Atari57 基准诞生以来，研究人员一直专注于最大化智能体的平均表现，过去八年间平均表现显著提升。但正如上面直观的例子所示，并非所有 Atari 游戏都一样难，有些游戏比其他游戏容易得多。如果不看平均表现，而是考察智能体在最难的 5% 游戏上的表现，我们会发现自 2012 年以来并没有太大变化：事实上，2019 年发表的智能体仍在 2012 年发表的智能体所挣扎的同一些游戏上挣扎。Agent57 改变了这一局面，它是自该基准诞生以来在 Atari57 上最通用的智能体。Agent57 终于在基准集中最难的游戏上以及最容易的游戏上都取得了高于人类水平的表现。

![一张散点图，展示 2015 至 2020 年间「Atari-57 第 5 百分位表现」随时间的变化。y 轴为人工归一化分数，一条紫色虚线标出位于 100 的「平均人类」水平。单 actor 智能体（A 到 E，浅青色）和分布式智能体（F 到 J，蓝色）按其发表日期绘制。只有 2020 年初绘制的 Agent57（J）以超过 110 的分数越过人类基线，此前的智能体分数都明显更低。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62274e5504f53c5ece33f088_Fig202.svg)

图 2。使用分布式设定的智能体为蓝色，单 actor 智能体为青色。第 5 百分位分析显示，MuZero 和 R2D2 等最先进算法的表现远低于人类基准（紫色点线），而 Agent57 在最难的 Atari 游戏上表现优于人类。

## Agent57 的谱系

早在 2012 年，DeepMind 就开发了[深度 Q 网络智能体](https://www.nature.com/articles/nature14236)（DQN）来攻克 Atari57 套件。此后，研究界开发了许多对 DQN 的扩展与替代方案。尽管有这些进展，所有深度强化学习智能体却始终在四款游戏上拿不到分：《Montezuma's Revenge》《Pitfall》《Solaris》和《Skiing》。

《Montezuma's Revenge》和《Pitfall》需要大量探索才能取得好成绩。学习中的一个核心困境是[探索-利用问题](http://incompleteideas.net/book/the-book.html)：是继续执行已知有效的行为（利用），还是尝试新东西（探索）以发现可能更成功的策略？例如，你是总在常去的餐馆点同一道最爱的菜，还是尝试可能超越旧爱的新菜？探索意味着采取许多次优动作来收集必要的信息，以发现最终更强的行为。

《Solaris》和《Skiing》是长期信用分配问题：在这些游戏中，把智能体动作的后果与其获得的奖励对应起来非常困难。智能体必须在很长的时间尺度上收集信息，才能获得学习所需的反馈。

视频列表：Agent57 游玩 Atari57 中最具挑战性的四款游戏——《Montezuma's Revenge》《Pitfall》《Solaris》和《Skiing》

为了让 Agent57 在应对其他 Atari57 游戏之外还能攻克这四款富有挑战性的游戏，有必要对 DQN 做出若干改变。

![一张谱系图，描绘从 2015 年 DQN 到 2020 年 Agent57 的演进路径。图中显示 DQN（2015）经由「DQN 改进」（Double DQN、优先回放、Dueling 头、分布式）和「短期记忆」（LSTM、GRU）发展为 R2D2（2019）。R2D2 再通过引入「情景记忆」（记忆网络、神经情景控制、Transformer）和「探索」技术（包括好奇心、内在动机和密度模型）演化为 Never Give Up（2019）。最后，Never Give Up 与「元控制器」（PBT、Bandits、元梯度、自适应 Bandits）相结合，促成 2020 年 Agent57 的诞生。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62274eaa75887b03a74748ef_Fig203.svg)

图 3。对 DQN 的一系列概念性进展，最终造就了更通用的智能体。

## DQN 的改进

早期对 DQN 的改进提升了其学习效率与稳定性，包括 [double DQN](https://arxiv.org/pdf/1509.06461.pdf)、[优先经验回放](https://arxiv.org/pdf/1511.05952.pdf)和 [dueling 架构](https://arxiv.org/pdf/1511.06581.pdf)。这些改动让智能体能更高效、更有效地利用自身经验。

## 分布式智能体

接下来，研究人员引入了 **分布式** 版本的 DQN：[Gorila DQN](https://arxiv.org/pdf/1507.04296.pdf) 和 [ApeX](https://openreview.net/pdf?id=H1Dy---0Z)，它们可以同时在多台计算机上运行。这让智能体能更快地采集并从经验中学习，使研究人员得以快速迭代想法。Agent57 同样是一个把数据采集与学习过程解耦的分布式 RL 智能体。多个 actor 与环境的独立副本交互，把数据以优先回放缓冲区的形式喂给中央的「记忆库」。然后一个 learner从这个回放缓冲区采样训练数据，如图 4 所示——这类似于一个人回忆既有记忆以便更好地从中学习。learner利用这些回放的经验构造损失函数，据此估计动作或事件的代价；然后通过最小化损失来更新其神经网络参数。最后，每个 actor 与 learner共享相同的网络架构，但拥有自己的权重副本。learner的权重会频繁发送给各个 actor，使它们能够按照各自的优先级、以各自的方式更新自己的权重，我们稍后会讨论这一点。

![一张示意图，展示 Agent57 的分布式强化学习架构，三个主要组件呈三角形排布：「Actors」在顶部，「Replay Buffer」在右下，「Learner」在左下。Actors 基于内在动机生成智能体经验（转移与初始优先级）并送入 Replay Buffer。Learner使用优先采样从 Replay Buffer 采样训练数据，把更新后的优先级写回缓冲区，最小化强化学习与内在动机损失，并把更新后的网络权重发回 Actors，完成反馈回路。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62274ed18c20e6cd21a3a90c_Fig204.svg)

图 4。Agent 57 的分布式设定。

## 短期记忆

智能体需要记忆，才能把之前的观测纳入其决策。这使智能体不仅能基于当前观测（通常是部分的，即智能体只能看到其世界的一部分）做决策，还能基于过去的观测——后者可以揭示关于环境整体的更多信息。例如，设想一个任务：智能体逐个房间走动，以统计一栋建筑里椅子的数量。没有记忆，智能体只能依赖对单个房间的观测。有了记忆，智能体可以记住之前房间里的椅子数量，只需把当前房间观测到的椅子数量加上去就能完成任务。因此，记忆的作用是聚合来自过去观测的信息，以改进决策过程。在深度 RL 和深度学习中，诸如[长短期记忆网络](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.676.4320&rep=rep1&type=pdf)（LSTM）之类的循环神经网络被用作短期记忆。

把记忆与行为对接，对构建自学习系统至关重要。在强化学习中，智能体可以是一个 on-policy 学习器——只能学习其直接动作的价值；也可以是一个 off-policy 学习器——即使没有执行那些动作，也能学到关于最优动作的知识。例如，它可能在执行随机动作，但仍能学到最佳可能动作是什么。因此，off-policy 学习是智能体的一种理想属性，帮助它们在彻底探索环境的同时学习最佳行动方案。把 off-policy 学习与记忆结合起来很有挑战，因为你需要知道在执行另一种行为时自己可能会记住什么。例如，寻找苹果时你可能选择记住的东西（例如苹果在哪里），不同于寻找橙子时你会记住的东西。但如果你当时在找橙子，偶然碰到苹果时你仍然可以学到如何找到苹果，以备将来需要。首个把记忆与 off-policy 学习结合的深度 RL 智能体是[深度循环 Q 网络](https://arxiv.org/pdf/1507.06527.pdf)（DRQN）。更近一些，Agent57 谱系中发生了一次重大「物种分化」：[Recurrent Replay Distributed DQN](https://openreview.net/pdf?id=r1lyTjAqYX)（R2D2）把短期记忆的神经网络模型与 off-policy 学习、分布式训练相结合，并在 Atari57 上取得了非常强的平均表现。R2D2 改造了从过去经验中学习的回放机制，使其能与短期记忆协同工作。这些因素加在一起，帮助 R2D2 高效地学习有利可图的行为，并**利用**它们获取奖励。

## 情景记忆

我们设计了 [Never Give Up](https://openreview.net/pdf?id=Sye57xStvB)（NGU），用另一种记忆形式——情景记忆（episodic memory）——来增强 R2D2。这使 NGU 能够检测何时遇到了游戏的新部分，从而智能体可以探索这些新区域，以防它们藏有奖励。这使得智能体的行为（**探索**）显著偏离它试图学习的策略（在游戏中获得高分）；因此，off-policy 学习在这里再次扮演关键角色。NGU 是首个在不借助领域知识的情况下在《Pitfall》上获得正奖励的智能体——自 Atari57 基准推出以来，没有任何智能体在这款游戏上得过分——在其他富有挑战性的 Atari 游戏上也是如此。遗憾的是，NGU 牺牲了在历史上那些「较容易」游戏上的表现，因此平均而言不如 R2D2。

## 用内在动机方法促进有方向的探索

为了发现最成功的策略，智能体必须探索其环境——但有些探索策略比其他策略更高效。在 DQN 时代，研究人员尝试用一种称为 epsilon-greedy 的无方向探索策略来解决探索问题：以固定概率（epsilon）采取随机动作，否则选择当前最佳动作。然而，这一类技术难以扩展到困难的探索问题上：在没有奖励的情况下，它们需要长得离谱的时间去探索庞大的状态-动作空间，因为它们依赖无方向的随机动作选择来发现未见的状态。为了克服这一局限，许多有方向的探索策略被提了出来。其中一条路线专注于开发**内在动机奖励**，通过为寻求新异性的行为提供更密集的「内部」奖励，鼓励智能体探索并访问尽可能多的状态。在这一路线中，我们区分两类奖励：第一，长期新异性奖励鼓励在整个训练过程中、跨越多个回合（episode）访问大量状态。第二，短期新异性奖励鼓励在短时间内（例如单个游戏回合内）访问大量状态。

## 在长时间尺度上寻求新异性

[长期新异性奖励](https://openreview.net/pdf?id=Sye57xStvB)在智能体一生中遇到前所未见的状态时发出信号，它是训练中迄今所见状态密度的函数：也就是说，它会根据智能体见过与当前状态相似状态的频率（相对于总体见过的状态）进行调整。当密度很高（表明该状态很熟悉）时，长期新异性奖励就低，反之亦然。当所有状态都变得熟悉时，智能体会退回到无方向的探索策略。然而，学习高维空间的密度模型问题重重，根源在于[维度灾难](https://en.wikipedia.org/wiki/Curse_of_dimensionality)。实践中，当智能体用深度学习模型学习密度模型时，会遭受[灾难性遗忘](https://www.pnas.org/content/114/13/3521)（随着遇到新经验而忘记之前见过的信息），以及无法对所有输入给出精确输出的问题。例如，在《Montezuma's Revenge》中，与无方向探索策略不同，长期新异性奖励让智能体能超越人类基线。不过，即便是[在该游戏上表现最好的方法](https://arxiv.org/pdf/1810.12894.pdf)，也需要以恰当的速度仔细地训练密度模型：当密度模型显示第一个房间里的状态已经熟悉时，智能体应该能够稳定地抵达陌生区域。

视频列表：DQN 与 Agent57 游玩《Montezuma's Revenge》

## 在短时间尺度上寻求新异性

[短期新异性奖励](https://openreview.net/pdf?id=Sye57xStvB)可用于鼓励智能体探索其近期历史中未曾遇到的状态。最近，模仿[情景记忆](https://arxiv.org/pdf/1703.01988.pdf)某些特性的神经网络已被用于加速强化学习智能体的学习。由于情景记忆也被认为对[识别新异经验](https://link.springer.com/content/pdf/10.3758/BF03210977.pdf)很重要，我们改造了这些模型，赋予 Never Give Up 短期新异性的概念。情景记忆模型是计算短期新异性奖励的高效而可靠的候选方案，因为它们能快速学到一个可以即时调整的非参数密度模型（无需学习或调整模型参数）。在这里，奖励的大小通过测量当前状态与情景记忆中记录的先前状态之间的距离来确定。

然而，并非所有关于距离的定义都能鼓励有意义的探索形式。例如，考虑在有许多行人和车辆的繁忙城市中导航的任务。如果一个智能体被编程为使用一种把每个微小视觉变化都计入的距离定义，那么它仅仅通过被动地观察环境、甚至站着不动，就会访问大量不同的状态——这是一种徒劳的探索。为避免这种情况，智能体应当改为学习那些对探索而言重要的特征，例如可控性，并只针对这些特征计算距离。这类模型此前已被用于探索，而把它们与情景记忆相结合正是 [Never Give Up 探索方法](https://openreview.net/pdf?id=Sye57xStvB)的主要进展之一，它带来了在《Pitfall!》上超越人类的表现！

视频列表：NGU 与 Agent57 游玩《Pitfall!》

Never Give Up（NGU）使用了这种基于[可控状态](https://arxiv.org/pdf/1705.05363.pdf)的短期新异性奖励，并用[随机网络蒸馏](https://openai.com/blog/reinforcement-learning-with-prediction-based-rewards/)将其与长期新异性奖励混合。混合方式是把两个奖励相乘，其中长期新异性是有界的。这样，短期新异性奖励的效果得以保留，但可以随着智能体在一生中对游戏愈发熟悉而被向下调制。NGU 的另一个核心思想是，它学习一族策略，范围从纯利用型到高度探索型。这是通过利用分布式设定实现的：在 [R2D2](https://openreview.net/pdf?id=r1lyTjAqYX) 的基础上，各 actor 基于对总新异性奖励的不同重要性权重、以不同策略产生经验。这些经验在该族各权重之间均匀产生。

## 元控制器：学习平衡探索与利用

Agent57 建立在如下观察之上：如果智能体能够学会什么时候利用更好、什么时候探索更好呢？我们引入了元控制器（meta-controller）的概念，用以自适应地调整探索-利用权衡，以及一个可为需要更长时序信用分配的游戏调整的时间跨度（time horizon）。有了这一改变，Agent57 能够两全其美：在简单游戏和困难游戏上都取得高于人类水平的表现。

具体来说，内在动机方法有两个缺点：

- **探索：**许多游戏都适合纯利用型策略，尤其是在游戏被完全探索之后。这意味着在 Never Give Up 中由探索型策略产生的许多经验，最终会在智能体探索完所有相关状态后变得浪费。
- **时间跨度：**有些任务需要很长的时间跨度（例如《Skiing》《Solaris》），在这些任务中，重视遥远未来才能获得的奖励，对于最终学到好的利用型策略、甚至学到任何好策略都可能是重要的。与此同时，如果对未来奖励加权过度，另一些任务可能学得又慢又不稳定。这一权衡在强化学习中通常由折扣因子控制，更高的折扣因子使得从更长的时间跨度中学习成为可能。

这促使我们使用一种在线自适应机制，控制用不同策略产生的经验数量，同时具备可变长度的时间跨度和赋予新异性的重要性。研究人员尝试过用多种方法解决这个问题，包括[训练一群具有不同超参数取值的智能体](https://arxiv.org/abs/1711.09846)、[通过梯度下降直接学习超参数取值](https://arxiv.org/abs/1805.09801)，或者使用[集中式 bandit 学习超参数取值](https://arxiv.org/abs/1912.06910)。

我们使用了一个 bandit 算法来选择智能体应当用哪个策略来产生经验。具体而言，我们为每个 actor 训练了一个[滑动窗口 UCB bandit](https://arxiv.org/pdf/0805.3415.pdf)，用以选择其策略应具有的探索偏好程度和时间跨度。

视频列表：NGU 与 Agent57 游玩《Skiing》

## Agent57：集大成

为了实现 Agent57，我们把先前的探索智能体 Never Give Up 与一个元控制器结合了起来。这个智能体计算长期与短期内在动机的混合，以进行探索并学习一族策略，其中策略的选择由元控制器完成。元控制器让智能体的每个 actor 都可以在近期与长期表现之间、以及探索新状态与利用已知内容之间选择不同的权衡（图 4）。强化学习是一个反馈回路：所选动作决定了训练数据。因此，元控制器也决定了智能体从什么数据中学习。

![一张对比表，展示 Agent57、NGU、R2D2 和 MuZero 在 Atari57 基准上的性能统计。表中显示，Agent57 是唯一在全部 57 款游戏上取得高于人类水平表现的智能体，其第 5 百分位人工归一化分数（HNS）为 116.67%，而 MuZero 虽拥有最高的均值和中位数 HNS，但在第 5 百分位上只有 0.03%。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62274f7abe6ea3d07da4b661_Fig205.svg)

## 结论与未来

凭借 Agent57，我们成功构建了一个更通用的智能体，它在 Atari57 基准的所有任务上都拥有超越人类的表现。它建立在先前的智能体 Never Give Up 之上，并实例化了一个自适应元控制器，帮助智能体知道何时探索、何时利用，以及在什么时间跨度下学习会有用。广泛的任务自然需要这两种权衡的不同选择，因此元控制器提供了一种动态调整这些选择的方式。

Agent57 能够随计算量的增加而扩展：训练得越久，分数越高。虽然这使 Agent57 取得了强劲的总体表现，但它需要大量计算和时间；其数据效率显然还有改进空间。此外，这个智能体在 Atari57 游戏集合上展现出更好的第 5 百分位表现。这绝不意味着 Atari 研究的终结——无论是在数据效率方面，还是在总体表现方面。对此我们提供两点看法：第一，分析各百分位上的表现，能让我们对算法的通用程度获得新的洞见。虽然 Agent57 在 57 款游戏的前几个百分位上取得了强劲结果，并且均值和中位数表现优于 NGU 或 R2D2，但正如 [MuZero](https://arxiv.org/abs/1911.08265) 所示，它仍有可能获得更高的平均表现。第二，目前所有算法在某些游戏中都[远未达到最优表现](https://arxiv.org/abs/1908.04683)。为此，值得采用的关键改进可能是增强 Agent57 用于探索、规划和信用分配的表示。

**说明**

论文请见[这里](https://arxiv.org/abs/2003.13350)。

工作由以下人员完成：Adrià Puigdomènech, Bilal Piot, Steven Kapturowski, Pablo Sprechmann, Alex Vitvitskyi, Daniel Guo, Charles Blundell

图表设计：Paulo Estriga 和 Adam Cain

**参考文献**

Agent57 谱系

DQN: Mnih, Volodymyr, et al. "[Human-level control through deep reinforcement learning](https://www.nature.com/articles/nature14236)." Nature 518.7540 (2015): 529-533.Double DQN: van Hasselt, Hado, Arthur Guez, and David Silver.

"[Deep reinforcement learning with double Q-learning](https://arxiv.org/abs/1509.06461)." CoRR abs/1509.06461 (2015)." arXiv preprint arXiv:1509.06461 (2015).Dueling: Wang, Ziyu, et al.

"[Dueling network architectures for deep reinforcement learning](https://arxiv.org/abs/1511.06581)." arXiv preprint arXiv:1511.06581 (2015).Prioritised replay: Schaul, Tom, et al.

[P"rioritized experience replay.](https://arxiv.org/abs/1511.05952)" arXiv preprint arXiv:1511.05952 (2015).Apex: Horgan, Dan, et al.

"[Distributed prioritized experience replay](https://arxiv.org/abs/1803.00933)." arXiv preprint arXiv:1803.00933 (2018).R2D2: Kapturowski, Steven, et al.

"[Recurrent experience replay in distributed reinforcement learning](https://openreview.net/pdf?id=r1lyTjAqYX)." ICLR (2019).NGU: Badia, Adrià Puigdomènech, et al.

"[Never Give Up: Learning Directed Exploration Strategies](https://arxiv.org/abs/2002.06038)." ICLR (2020).

**情景记忆相关**

Memory Networks: Weston, Jason, Sumit Chopra, and Antoine Bordes. "[Memory networks](https://arxiv.org/abs/1410.3916)." arXiv preprint arXiv:1410.3916 (2014).

Neural Episodic Control: Pritzel, Alexander, et al. ["Neural episodic control"](https://arxiv.org/abs/1703.01988)." Proceedings of the 34th International Conference on Machine Learning-Volume 70. JMLR. org, 2017. Transformer: Vaswani, Ashish, et al.

"[Attention is all you need](https://arxiv.org/abs/1706.03762)." Advances in neural information processing systems. 2017. Wayne, Greg, et al. "Unsupervised predictive memory in a goal-directed agent." arXiv preprint arXiv:1803.10760 (2018).

**探索相关**

Curiosity: Schmidhuber, Jürgen. "A possibility for implementing curiosity and boredom in model-building neural controllers." Proc. of the international conference on simulation of adaptive behavior: From animals to animats. 1991.

Intrinsic motivation: Oudeyer, Pierre-Yves, Frdric Kaplan, and Verena V. Hafner. "[Intrinsic motivation systems for autonomous mental development.](http://www.pyoudeyer.com/ims.pdf)" IEEE transactions on evolutionary computation 11.2 (2007): 265-286.

Intrinsic motivation: Barto, Andrew G. "[Intrinsic motivation and reinforcement learning](https://link.springer.com/chapter/10.1007/978-3-642-32375-1_2)." Intrinsically motivated learning in natural and artificial systems. Springer, Berlin, Heidelberg, 2013. 17-47.

Visit counts: Bellemare, Marc, et al. "[Unifying count-based exploration and intrinsic motivation](https://arxiv.org/abs/1606.01868)." Advances in neural information processing systems. 2016.

Density models: Ostrovski, Georg, et al. "[Count-based exploration with neural density models](https://arxiv.org/abs/1703.01310)." Proceedings of the 34th International Conference on Machine Learning-Volume 70. JMLR. org, 2017.

Ex2: Fu, Justin, John Co-Reyes, and Sergey Levine. "[Ex2: Exploration with exemplar models for deep reinforcement learning](https://arxiv.org/abs/1703.01260)."

Advances in neural information processing systems. 2017. Hashing: Tang, Haoran, et al.

"[Exploration: A study of count-based exploration for deep reinforcement learning](https://arxiv.org/abs/1611.04717)." Advances in neural information processing systems. 2017. Random Network Distillation: Burda, Yuri, et al.

"[Exploration by random network distillation](https://arxiv.org/abs/1810.12894)." arXiv preprint arXiv:1810.12894 (2018).CoEx: Choi, Jongwook, et al.

"[Contingency-aware exploration in reinforcement learning](https://arxiv.org/abs/1811.01483)." arXiv preprint arXiv:1811.01483 (2018). Reachability: Savinov, Nikolay, et al.

"[Episodic curiosity through reachability](https://arxiv.org/abs/1810.02274)." ICLR, 2019.

Never Give Up: Puigdomènech Badia, Adrià, et al. "[Never Give Up: Learning Directed Exploration Strategies](https://arxiv.org/abs/2002.06038)." arXiv (2020): arXiv-2002.

**元控制器相关**

Population-based training: Jaderberg, Max, et al. "[Population based training of neural networks](https://arxiv.org/abs/1711.09846)." arXiv preprint arXiv:1711.09846 (2017).

Meta-gradients: Xu, Zhongwen, Hado P. van Hasselt, and David Silver. "[Meta-gradient reinforcement learning](https://arxiv.org/abs/1805.09801)."

Advances in neural information processing systems. 2018. Bandits: Schaul, Tom, et al. "[Adapting Behaviour for Learning Progress.](https://arxiv.org/abs/1912.06910)" arXiv preprint arXiv:1912.06910 (2019).
