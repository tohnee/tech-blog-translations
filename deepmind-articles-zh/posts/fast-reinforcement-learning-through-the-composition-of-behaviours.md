---
title: "通过行为组合实现快速强化学习"
title_en: "Fast reinforcement learning through the composition of behaviours"
source: https://deepmind.google/blog/fast-reinforcement-learning-through-the-composition-of-behaviours/
site: deepmind
date: 2020-10-12
crawled: 2026-09-13
translated: 2026-09-13
---

# 通过行为组合实现快速强化学习

> 原文：[Fast reinforcement learning through the composition of behaviours](https://deepmind.google/blog/fast-reinforcement-learning-through-the-composition-of-behaviours/) · Google DeepMind

## 智能的组合性本质

想象一下，每次想学一道新菜谱时，你都得从头重新学习如何切菜、削皮和搅拌。在许多机器学习系统中，智能体在面对新挑战时往往必须从零开始学习。然而显而易见，人类的学习效率要高得多：他们能够组合此前已经学会的能力。就像一本有限的词汇字典可以重新组装成意义近乎无限句子一样，人们会重新利用并重新组合自己已经掌握的技能，以应对新的挑战。

在自然界中，学习产生于动物为了获取食物和其他奖励而探索环境、与环境互动的过程。这正是[强化学习](http://incompleteideas.net/book/the-book-2nd.html)（RL）所刻画的范式：与环境的交互会根据由此产生的奖励（或惩罚）来强化或抑制特定的行为模式。最近，强化学习与[深度学习](https://www.nature.com/articles/nature14539)的结合取得了令人瞩目的成果，例如能够学会下[围棋](https://deepmind.com/blog/article/alphazero-shedding-new-light-grand-games-chess-shogi-and-go)和[国际象棋](https://arxiv.org/abs/1911.08265)等棋盘游戏的智能体、掌握全部 [Atari](https://deepmind.com/blog/article/Agent57-Outperforming-the-human-Atari-benchmark) 游戏的智能体，以及更现代、更困难的视频游戏如 [Dota](https://openai.com/projects/five/) 和[《星际争霸 II》](https://deepmind.com/blog/article/alphastar-mastering-real-time-strategy-game-starcraft-ii)。

强化学习的一大局限在于，当前的方法需要海量的训练经验。例如，为了学会玩单一一款 Atari 游戏，一个强化学习智能体通常要消耗相当于连续玩上数周的数据量。一项由 MIT 和哈佛的研究人员主导的[研究](http://gershmanlab.webfactional.com/pubs/Tsividis17.pdf)表明，在某些情况下，人类只需玩十五分钟就能达到同样的水平。

造成这种差距的一个可能原因是，与人类不同，强化学习智能体通常要从零开始学习一个新任务。我们希望智能体能利用在先前任务中习得的知识来更快地学习新任务，就像一位厨师学新菜谱会比从未做过菜的人轻松得多一样。在发表于《美国国家科学院院刊》（PNAS）的一篇[论文](https://www.pnas.org/content/early/2020/08/13/1907370117)中，我们描述了一个旨在赋予强化学习智能体这种能力的框架。

## 表示世界的两种方式

为了说明我们的方法，我们以一项（或至少曾经是）日常例行活动为例：通勤上班。设想如下场景：一个智能体每天必须从家通勤到办公室，路上总会买一杯咖啡。在智能体的家和办公室之间有两家咖啡馆：一家的咖啡很棒，但路线更长；另一家的咖啡尚可，但通勤更近（图 1）。根据智能体对咖啡品质的看重程度与当天赶时间程度的权衡，它可能会选择两条路线中的一条（图 1 地图中的黄色和蓝色路径）。

![一张示意地图，展示了从「家」到「办公室」的三条路线：蓝色路径经过「咖啡馆 A」（咖啡三星、食物五星），黄色路径经过「咖啡馆 B」（咖啡五星、食物三星），还有一条橙色路径从「家」出发经「公园」到「咖啡馆 A」，再连接到「咖啡馆 B」，最后抵达「办公室」。](https://lh3.googleusercontent.com/94uCFjigjYHUt5vLxw50vU2PvgaflGrkHyiiMz57I4f7QjTcr8xs9EEM2o6RiVQDsa2qthy_cDg1cLJtsLr75gtztHsf9dOq6_AfB0PoxP3Ks3oUDw=w1440)

图 1：一张示意性的上班通勤地图。

传统上，强化学习算法分为两大类别：[基于模型的智能体和无模型的智能体](https://www.jair.org/index.php/jair/article/view/10166)（图 2 与图 3）。基于模型的智能体（图 2）会构建环境中许多方面的表示。这类智能体可能知道各个地点之间如何连接、每家咖啡馆咖啡的品质，以及其他任何被认为相关的信息。无模型的智能体（图 3）对环境的表示则紧凑得多。例如，一个基于价值的无模型智能体会为从家出发的每条可能路线关联一个数字；这就是每条路线的期望「价值」，反映了在咖啡品质与通勤时长之间的某种特定权衡。以上文图 1 中的蓝色路径为例。假设这条路径长度为 4，智能体沿这条路径买到的咖啡被评为三星。如果智能体对通勤距离的在意程度比它对咖啡品质的在意程度高 50%，那么这条路径的价值就是 (-1.5 x 4) + (1 x 3) = -3（我们对距离使用负权重，以表明更长的通勤是不可取的）。

![一张蓝色六边形信息图，描绘了从「家」到「办公室」的路线网络。图中包含「公园」「咖啡馆 A」和「咖啡馆 B」作为中间节点，路径上标注了距离的数值，并为每家咖啡馆标注了咖啡和食物的价值。](https://lh3.googleusercontent.com/qu0UEh4uIwg-ufTtF4lam_l4wVLiKDub_Bq8qQa8z9lm8ngx-VPB319EcfE4QUQtaQagFpmcXPd-QX-zuPV1nwKSXoDNl4Y58skD77GMx1CdaoJG_Q=w1440)

图 2：基于模型的智能体如何表示世界。表示中只捕捉与智能体相关的细节（对比图 1）。不过，这一表示仍然比无模型智能体所使用的表示复杂得多（对比图 3）。

![一张蓝色六边形信息图，展示使用后继特征的智能体如何表示其环境：图中为「家」「咖啡馆 A」「咖啡馆 B」和「公园」设置了决策节点，并标出各转移选项及其期望价值。](https://lh3.googleusercontent.com/w0i8pXBuiAKDBVRROPhu8wU-TM7ZKILG1epkbluglispHzhQ1WIUoc236rsB8INECUUDd9ruysT7reRcrAGAWH5gQQ-hy5q2TRSElLum2-NJfFERkA=w1440)

图 3：基于价值的无模型智能体如何表示世界。对每个地点，智能体为每种可能的行动方案关联一个数字；这个数字就是智能体可用的每个选项的「价值」。当处于某个地点时，智能体会查看可用的价值，并仅根据这一信息做出决策（右图以「家」这个地点为例进行了说明）。与基于模型的表示不同，这些信息以非空间的方式存储，也就是说，各个地点之间没有连接（对比图 2）。

我们可以把咖啡品质相对通勤距离的权重比理解为智能体的偏好。对任意一组固定的偏好而言，无模型智能体和基于模型的智能体会选择相同的路线。既然最终结果一样，为什么还要像基于模型的智能体那样采用更复杂的世界表示呢？既然智能体最终喝到的还是同一杯咖啡，为什么还要了解那么多关于环境的信息呢？

偏好是会日复一日变化的：智能体在规划去办公室的路线时，可能会考虑自己有多饿，或者开会是否要迟到了。无模型智能体应对这一点的一种办法是，为每一种可能的偏好组合学习最佳路线。这并不理想，因为学习所有可能的偏好组合将耗费很长时间。而且，如果偏好组合有无穷多种，就不可能为每一种组合都学出一条路线。

相比之下，基于模型的智能体可以适应任何偏好组合，而无需任何学习：它只需「设想」所有可能的路线，并评估它们能在多大程度上满足自己当前的心态。然而这种方法也有缺陷。首先，「在脑内」生成并评估所有可能的轨迹在计算上可能非常昂贵。其次，在复杂环境中为整个世界建模可能非常困难。

无模型智能体学得更快，但对变化脆弱。基于模型的智能体灵活，但学习可能很慢。有没有折中的解决方案？

## 后继特征：一种折中方案

行为科学与神经科学领域最近的一项[研究](https://www.nature.com/articles/s41562-017-0180-8)表明，在某些情况下，人类和动物做决策所依据的算法模型是无模型方法与基于模型方法之间的折中（参见[这里](https://deepmind.com/blog/article/hippocampus-predictive-map)和[这里](https://papers.nips.cc/paper/9522-a-neurally-plausible-model-learns-successor-representations-in-partially-observable-environments.pdf)）。该假说认为，与无模型智能体一样，人类也以数字的形式计算备选策略的价值。但是，人类总结的不是单一数量，而是描述周围世界的许多不同数量——这一点又让人联想到基于模型的智能体。

我们也可以赋予强化学习智能体同样的能力。在我们的例子中，这样的智能体会为每条路线保存两个数字：一个表示期望的咖啡品质，另一个表示到办公室的距离。它还可以为一些并非刻意优化、但仍可供日后参考的事物保存数字（例如每家咖啡馆食物的品质）。智能体关心并持续追踪的世界维度有时被称为「特征」。因此，这种世界表示被称为后继特征（successor features，其最初形态被称为「后继表示」，见其[原始论文](https://www.mitpressjournals.org/doi/abs/10.1162/neco.1993.5.4.613?journalCode=neco)）。

后继特征可以被视为无模型表示与基于模型表示之间的折中。与后者一样，后继特征总结了多个不同的数量，捕捉了超越单一价值的世界。然而，与无模型表示一样，智能体追踪的数量只是对其所关心特征的简单统计汇总。从这个意义上说，后继特征就像无模型智能体的「解包」版本。图 4 展示了使用后继特征的智能体会如何看待我们这个示例环境。

![一张蓝色六边形信息图，展示使用后继特征的智能体如何表示其环境：图中为「家」「咖啡馆 A」「咖啡馆 B」和「公园」设置了决策节点，并标出各转移选项及其期望价值。](https://lh3.googleusercontent.com/XT3mqYTbd-7Epb1-Zf62a3ekWpXckzpULmkEbagd_A9hKhrSHebMcDyduCaeiSPVVdl-6n_5ia_YjontOdjE-TkC9AVVRTUwAMqEolwlfPlkIll0=w1440)

图 4：用后继特征表示世界。这与无模型智能体表示世界的方式类似，但每条路径关联的不是单个数字，而是多个数字（在本例中为咖啡、食物和距离）。也就是说，在「家」这个地点，智能体需要根据当前偏好权衡的数字是九个而不是三个（对比图 3）。

## 使用后继特征：从策略字典中组合出新计划

后继特征之所以是一种有用的表示，是因为它允许在多组不同偏好下评估同一条路线。我们再次以图 1 中的蓝色路线为例。利用后继特征，智能体会为这条路径保存三个数字：其长度（4）、咖啡品质（3）和食物品质（5）。如果智能体已经吃过早餐，它可能不太在乎食物；此外，如果它迟到了，它对通勤距离的在意程度可能会超过咖啡品质——比方说像之前一样高 50%。在这种情况下，蓝色路径的价值为 (-1.5 x 4) + (1 x 3) + (0 x 5) = -3，与上文的例子一致。但在某一天，智能体饿了，对食物的在意程度和对咖啡一样高，它就可以立即把这条路线的价值更新为 (-1.5 x 4) + (1 x 3) + (1 x 5) = 2。使用同样的策略，智能体可以按照任意一组偏好评估任何路线。

在我们的例子中，智能体是在不同路线之间做选择。更一般地说，智能体要搜索的是一个策略（policy）：一份关于在每种可能情况下该做什么的处方。策略与路线密切相关：在我们的例子中，一个策略若选择从家走向咖啡馆 A 的路，再在咖啡馆 A 选择去办公室的路，就会走完蓝色路径。因此在这里，我们可以把策略和路线当作可以互换的说法（如果环境中有随机性，这一点就不成立了，但我们暂且把这个细节放到一边）。我们讨论了后继特征如何让一条路线（或策略）在不同偏好组合下得到评估。我们把这个过程称为广义策略评估（generalised policy evaluation），简称 GPE。

为什么 GPE 有用？假设智能体拥有一本策略字典（例如一组已知的去办公室的路线）。给定一组偏好，智能体可以用 GPE 立即评估字典中每个策略在这些偏好下的表现。现在到了真正有趣的部分：基于对已知策略的这种快速评估，智能体可以即时创造出全新的策略。它的做法很简单：每当智能体需要做一个决策时，它都会问这样一个问题：「如果我做出这个决策，然后此后一直遵循价值最大的那个策略，哪个决策会带来最大的整体价值？」令人惊讶的是，如果智能体在每种情况下都选择带来最大整体价值的决策，它最终得到的策略往往会优于用来构造它的那些单独策略。

这种把一组策略「拼接」起来以创造更优策略的过程称为广义策略改进（generalised policy improvement），简称 GPI。图 5 用我们贯穿全文的例子展示了 GPI 的工作方式。

![由三幅并排六边形地图组成的信息图，说明广义策略改进（GPI）的工作原理。在左图中，「家」处的机器人智能体评估通往「公园」「咖啡馆 A」和「咖啡馆 B」的已知路径。在中图中，智能体选定通往「咖啡馆 A」的路径作为最佳下一步决策。在右图中，智能体从「咖啡馆 A」移动到「咖啡馆 B」，从而构造出一条优化路线。](https://lh3.googleusercontent.com/wyxmoz4HoOvkQgEyCvCX0v7gy9Dh6-1BakfugJqLKE4wQx9ft5gYS5Qm2wK8xnxuew4sZsiKleARczC_oRdDRifZiFBxzHRFMoTNeD5nM8xAnPkuURs=w1440)

图 5：GPI 的工作方式。在这个例子中，智能体对通勤距离的在意程度比对咖啡和食物品质高 50%。此时最佳做法是先去咖啡馆 A，再去咖啡馆 B，最后前往办公室。智能体知道与蓝色、黄色和橙色路径相关联的三个策略（见图 1）。每个策略走的是不同的路径，但没有一个与期望的路线完全重合。利用 GPE，智能体按照它当前的一组偏好（即与距离、咖啡和食物分别关联的权重 -1.5、1 和 1）评估这三个策略。基于这一评估，智能体在家时提出这样一个问题：「如果我沿三个策略中的某一个一路走到办公室，哪一个最好？」由于答案是对应蓝色路径的策略，智能体便先遵循它。不过，智能体并不会一路坚持蓝色策略：当它到达咖啡馆 A 时，它会再次提出同样的问题。这一次，它不再走蓝色路径，而是改走橙色路径。通过重复这一过程，智能体最终会走上一条在其偏好下通往办公室的最佳路径——尽管它的任何一个已知策略单独拿出来都做不到这一点。

通过 GPI 创造的策略的性能取决于智能体知道多少个策略。例如，在我们贯穿全文的例子中，只要智能体知道蓝色和黄色两条路径，它就能为关于咖啡品质与通勤长度的任意偏好找到最佳路线。但 GPI 策略并不总能找到最佳路线。在图 1 中，如果智能体事先不知道一个把咖啡馆 A 和咖啡馆 B 以这种方式连接起来的策略（比如图中的橙色路线），它就永远不会先去咖啡馆 A 再去咖啡馆 B。

### 一个展示 GPE 与 GPI 实际效果的简单例子

为了说明 GPE 和 GPI 的好处，我们现在管窥一下我们近期发表的工作中的一个实验（完整细节见[论文](https://www.pnas.org/content/early/2020/08/13/1907370117)）。该实验使用了一个简单的环境，以抽象方式呈现我们的方法能够发挥作用的那类问题。如图 6 所示，环境是一个 10 x 10 的网格，其中散布着 10 个物体。智能体只有拾取物体时才会得到非零奖励，此时另一个物体会随机出现在某个位置。与物体相关的奖励取决于其类型。物体类型旨在表示具体或抽象的概念；为了与我们贯穿全文的例子呼应，我们假定每个物体要么是「咖啡」，要么是「食物」（这正是智能体追踪的特征）。

![一张 10x10 的网格世界地图，展示从一个机器人图标出发的三条高亮路径：红色路径通向咖啡图标，蓝色路径通向食物图标，灰色路径则通向咖啡图标并避开食物。](https://lh3.googleusercontent.com/239JaXxj4NoXrxIkNFdnP7JnvAKoDwkf_hzUxifhTa89gpY5CZU7gMuVUEfgGeM2zGV0b0MGcL6rRBmVeAT_cHBMZqFoH5AtjhE_DST2lPS_zKCCVQ=w1440)

图 6：用于说明 GPE 和 GPI 用处的简单环境。智能体使用四个方向性动作（「上」「下」「左」「右」）移动，并在拾取物体时获得非零奖励。与物体相关的奖励由其类型（「咖啡」或「食物」）决定。

显然，智能体的最佳策略取决于它当前对咖啡或食物的偏好。例如，在图 6 中，只在乎咖啡的智能体可能会走红色路径，而只专注食物的智能体会走蓝色路径。我们还可以设想中间情形：智能体以不同权重同时想要咖啡和食物，其中包括智能体想避开其中一者的情形。例如，如果智能体想要咖啡但完全不想要食物，图 6 中的灰色路径可能比红色路径是更好的选择。

这个问题的挑战在于快速适应一组新偏好（或一个「任务」）。在实验中，我们展示了如何借助 GPE 和 GPI 做到这一点。我们的智能体学习了两个策略：一个寻找咖啡，一个寻找食物。然后我们测试了由 GPE 和 GPI 计算出的策略在与不同偏好相关联的任务上的表现。在图 7 中，我们将我们的方法与一个无模型智能体在「寻找咖啡同时避开食物」的任务上进行比较。请注意，使用 GPE 和 GPI 的智能体如何即时综合出一个合理的策略，尽管它从未学过如何刻意避开物体。当然，由 GPE 和 GPI 计算出的策略可以作为一个初始解，之后再通过学习加以精化，这意味着它最终能达到与无模型智能体相同的性能，但很可能会更快到达那里。

![一张折线图，比较无模型智能体（Q-learning）与 GPE-GPI 智能体随时间变化的平均奖励总和。以粉色虚线表示的无模型智能体起步时奖励极低，随后沿 S 形曲线缓慢上升，最终超过 GPE-GPI 智能体。以蓝色实线表示的 GPE-GPI 智能体则瞬时达到较高且稳定的平均奖励总和，没有学习曲线。](https://lh3.googleusercontent.com/9RzYF1zQ4CcCP5PWSuO8aZEf_StLX_xpDnScuG8jQZfd9-zkfN8aKxZyfpGmJXU1cgXYUhn17iGwU6LKN1_FSDKNbtQ4KQ2N9SBz4o9do9BXD1fqcQ=w1440)

图 7：相比无模型方法（Q-learning），GPE-GPI 智能体用少得多的训练数据就学会了良好表现。这里的任务是寻找咖啡并避开食物。GPE-GPI 智能体学习了两个策略，一个寻找咖啡，一个寻找食物。尽管从未接受过避开物体的训练，它却成功地避开了食物。阴影区域为 100 次运行的一个标准差。

图 7 展示了 GPE 和 GPI 在一个特定任务上的表现。我们还在许多其他任务上测试了同一个智能体。图 8 展示了当我们改变咖啡与食物的相对重要性时，无模型智能体和 GPE-GPI 智能体的表现变化。请注意，无模型智能体必须为每个任务分别从零学起，而 GPE-GPI 智能体只需学习两个策略，随后便能快速适应所有任务。

![一张柱状图，比较 GPE-GPI 智能体在不同任务上的表现与无模型智能体的表现。蓝色竖条代表 GPE-GPI 智能体在各种偏好组合下取得的平均奖励总和，偏好组合的范围从「避开咖啡」到「寻找咖啡」，以及从「寻找食物」到「避开食物」。图表顶部的一条紫色虚线代表必须逐个解决每个任务的无模型智能体（Q-learning）的高且稳定的基准性能。](https://lh3.googleusercontent.com/MMP1FmfHjpbRJDHLBLw4tWNE0MXpzhBPT05I64xu1stjT-Y9Hb6rhkhKkSjuwxwjOEIJIJ2-8RpjnZmi-T_K3PUFFwWxserYP88--_Z6LIBwryDv0g=w1440)

图 8：GPE-GPI 智能体在不同任务上的表现。每根柱子对应由一组关于咖啡与食物的偏好所诱导的任务。图下方的颜色渐变表示偏好组合：蓝色表示正权重，白色表示零权重，红色表示负权重。举例来说，在图表两端，任务的目标基本上是避开一类物体而忽略另一类；而在图表中央，任务是以同等力度同时寻找两类物体。误差条为 10 次运行的一个标准差。

上述实验使用了一个简单环境，其设计目的是在去除不必要混淆因素的前提下展现 GPE 和 GPI 所需的性质。但 GPE 和 GPI 也已被应用于大规模任务。例如，在先前的论文中（见[这里](http://proceedings.mlr.press/v80/barreto18a/barreto18a.pdf)和[这里](https://openreview.net/pdf?id=S1VWjiRcKX)），我们展示了当把网格世界替换成一个三维环境、智能体以第一人称视角接收观测时，同样的策略依然有效（示意视频见[这里](https://www.youtube.com/watch?v=-dTnqfwTRMI&feature=youtu.be)和[这里](https://www.youtube.com/watch?v=0afwHJofbB0&feature=youtu.be)）。我们还利用 GPE 和 GPI，让一个四足仿真机器人在只学会了沿三个方向移动之后，便能够沿任意方向导航（论文见[这里](https://papers.nips.cc/paper/9463-the-option-keyboard-combining-skills-in-reinforcement-learning)，视频见[这里](https://www.youtube.com/watch?v=39Ye8cMyelQ&feature=youtu.be)）。

## GPE 与 GPI 的来龙去脉

关于 GPE 和 GPI 的工作处于两条独立研究分支的交汇处，这两条分支各自与其中一个操作相关。第一条与 GPE 相关，是关于后继表示的研究，始于 Dayan 1993 年的开创性[论文](https://www.mitpressjournals.org/doi/abs/10.1162/neco.1993.5.4.613?journalCode=neco)。Dayan 的论文开创了神经科学中一条至今仍十分活跃的研究脉络（见延伸阅读：「神经科学中的后继表示」）。最近，后继表示在强化学习的语境中重新浮现（链接见[这里](https://papers.nips.cc/paper/6994-successor-features-for-transfer-in-reinforcement-learning)和[这里](https://arxiv.org/abs/1606.02396)），在那里它也被称为「后继特征」，并成为该领域的活跃研究方向（见延伸阅读：「GPE、后继特征及相关方法」）。后继特征还与[广义价值函数](https://www.cs.swarthmore.edu/~meeden/DevelopmentalRobotics/horde1.pdf)密切相关，后者的基础是 Sutton 等人的假说：相关的知识可以表达为对世界的许多预测（也在[这里](https://link.springer.com/chapter/10.1007/978-3-642-33093-3_30)有讨论）。后继特征的定义也曾在强化学习的[其他情境](https://ai.stanford.edu/~ang/papers/icml04-apprentice.pdf)中独立出现，并与通常与深度强化学习相关联的一些[较新的方法](http://proceedings.mlr.press/v37/schaul15.pdf)有关。

GPE 和 GPI 源起的第二条研究分支与后者相关，即通过组合行为来创造新行为。执行子控制器的去中心化控制器的想法多年来被多次提出（如 [Brooks, 1986](https://ieeexplore.ieee.org/document/1087032)），其基于价值函数的实现至少可以追溯到 1997 年 [Humphrys](https://www.computing.dcu.ie/~humphrys/PhD/index.html) 和 [Karlsson](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.37.8338&rep=rep1&type=pdf) 的博士论文。GPI 还与分层强化学习密切相关，后者的基础奠定于 20 世纪 90 年代和 21 世纪初 [Dayan 和 Hinton](https://papers.nips.cc/paper/714-feudal-reinforcement-learning)、[Parr 和 Russell](https://papers.nips.cc/paper/1384-reinforcement-learning-with-hierarchies-of-machines)、[Sutton, Precup 和 Singh](https://www.sciencedirect.com/science/article/pii/S0004370299000521) 以及 [Dietterich](https://jair.org/index.php/jair/article/view/10266) 的工作。如今，行为组合与分层强化学习都是活跃的研究领域（见延伸阅读：「GPI、分层强化学习及相关方法」）。

[Mehta 等人](http://homes.sice.indiana.edu/natarasr/Papers/var-reward.pdf)可能是最早联合使用 GPE 和 GPI 的人，不过在他们的场景中，GPI 退化为开始时的单次选择（也就是说，不存在策略的「拼接」）。本博文讨论的 GPE 和 GPI 版本于 2016 年首次被[提出](https://arxiv.org/abs/1606.05312)，作为促进[迁移学习](https://www.jmlr.org/papers/volume10/taylor09a/taylor09a.pdf)的一种机制。强化学习中的迁移可以追溯到 1992 年 [Singh 的工作](https://link.springer.com/article/10.1007/BF00992700)，最近在深度强化学习的语境中经历了[复兴](https://arxiv.org/abs/2009.07888)，并至今仍是一个活跃的研究领域（见延伸阅读：「GPE + GPI、迁移学习及相关方法」）。

关于这些工作的更多信息见下文，我们还提供了一份延伸阅读建议清单。

## 一种组合式的强化学习路径

总而言之，无模型智能体难以适应新情况，例如无法轻松满足它从未经历过的偏好组合。基于模型的智能体可以适应任何新情况，但为此它首先必须为整个世界学出一个模型。基于 GPE 和 GPI 的智能体提供了一种折中方案：尽管它学到的世界模型远小于基于模型的智能体，但它可以快速适应某些情况，并且往往有不错的表现。

我们讨论了 GPE 和 GPI 的具体实现，但它们其实是更一般的概念。在抽象层面上，使用 GPE 和 GPI 的智能体分两步进行。首先，面对一个新任务时，它问：「已知任务的解在新任务上会有怎样的表现？」这就是 GPE。然后，基于这一评估，智能体组合已有的解来构造新任务的解——也就是说，它执行 GPI。GPE 和 GPI 背后的具体机制不如原理本身重要，寻找实现这些操作的替代方式可能是一个令人兴奋的研究方向。有趣的是，行为科学领域的一项新[研究](https://www.biorxiv.org/content/10.1101/815332v1)提供了初步证据，表明人类在多任务场景中的决策遵循一条与 GPE 和 GPI 高度相似的原理。

GPE 和 GPI 提供的快速适应能力，对于构建学习更快的强化学习智能体充满前景。更一般地说，它提示了一条为问题学习灵活解法的新途径。智能体不必把一个问题当作单一的、不可分割的任务来处理，而可以把它分解成更小、更易处理的子任务。子任务的解随后可以被复用和重组，从而更快地解决整体任务。这就形成了一种组合式的强化学习路径，有望催生更具可扩展性的智能体。至少，这些智能体不会再因为一杯咖啡而迟到。

论文以 PNAS 首发版本[在此](https://www.pnas.org/content/early/2020/08/13/1907370117)阅读。

感谢 Jim Kynvin、Adam Cain 和 Dominic Barlow 制作图表，感谢 Kimberly Stachenfeld 提供神经科学文献的指引，感谢 Kelly Clancy 对文本的帮助。

**延伸阅读**

GPE、后继特征及相关方法

[Improving Generalisation for Temporal Difference Learning: The Successor Representation.](http://www.gatsby.ucl.ac.uk/~dayan/papers/d93b.pdf) Peter Dayan. Neural Computation, 1993.

[Apprenticeship Learning Via Inverse Reinforcement Learning.](https://ai.stanford.edu/~ang/papers/icml04-apprentice.pdf) Pieter Abbeel and Andrew Y. Ng. Proceedings of the International Conference on Machine learning (ICML), 2004.

[Horde: A Scalable Real-time Architecture for Learning Knowledge from Unsupervised Sensorimotor Interaction.](https://www.cs.swarthmore.edu/~meeden/DevelopmentalRobotics/horde1.pdf) Richard S. Sutton, Joseph Modayil, Michael Delp, Thomas Degris, Patrick M. Pilarski, Adam White. Proceedings of the International Conference on Autonomous Agents and Multiagent Systems (AAMAS), 2011.

[Multi-timescale Nexting in a Reinforcement Learning Robot.](https://link.springer.com/chapter/10.1007/978-3-642-33093-3_30) Joseph Modayil, Adam White, Richard S. Sutton. From Animals to Animats, 2012.

[Universal Value Function Approximators.](http://proceedings.mlr.press/v37/schaul15.pdf) Tom Schaul, Dan Horgan, Karol Gregor, David Silver. Proceedings of the International Conference on Machine learning (ICML), 2015.

[Deep Successor Reinforcement Learning.](https://arxiv.org/abs/1606.02396) Tejas D. Kulkarni, Ardavan Saeedi, Simanta Gautam, Samuel J. Gershman. arXiv, 2017.

[Visual Semantic Planning Using Deep Successor Representations.](https://openaccess.thecvf.com/content_ICCV_2017/papers/Zhu_Visual_Semantic_Planning_ICCV_2017_paper.pdf) Yuke Zhu, Daniel Gordon, Eric Kolve, Dieter Fox, Li Fei-Fei, Abhinav Gupta, Roozbeh Mottaghi, Ali Farhadi. Proceedings of the IEEE International Conference on Computer Vision (ICCV), 2017.

[Deep Reinforcement Learning with Successor Features for Navigation Across Similar Environments.](https://ieeexplore.ieee.org/abstract/document/8206049/authors#authors) Jingwei Zhang, Jost Tobias Springenberg, Joschka Boedecker, Wolfram Burgard. IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), 2017.

[Universal Successor Representations for Transfer Reinforcement Learning.](https://arxiv.org/abs/1804.03758) Chen Ma, Junfeng Wen, Yoshua Bengio. arXiv, 2018.

[Eigenoption Discovery through the Deep Successor Representation.](https://openreview.net/pdf?id=Bk8ZcAxR-) Marlos C. Machado, Clemens Rosenbaum, Xiaoxiao Guo, Miao Liu, Gerald Tesauro, Murray Campbell. International Conference on Learning Representations (ICLR), 2018.

[Successor Options: An Option Discovery Framework for Reinforcement Learning.](https://www.ijcai.org/Proceedings/2019/0458.pdf) Rahul Ramesh, Manan Tomar, Balaraman Ravindran. Proceedings of the International Joint Conference on Artificial Intelligence (IJCAI), 2019.

[Successor Uncertainties: Exploration and Uncertainty in Temporal Difference Learning.](https://papers.nips.cc/paper/8700-successor-uncertainties-exploration-and-uncertainty-in-temporal-difference-learning.pdf) David Janz, Jiri Hron, Przemysław Mazur, Katja Hofmann, José Miguel Hernández-Lobato, Sebastian Tschiatschek. Advances in Neural Information Processing Systems (NeurIPS), 2019.

[Successor Features Combine Elements of Model-Free and Model-based Reinforcement Learning.](https://arxiv.org/abs/1901.11437) Lucas Lehnert, Michael L. Littman. arXiv, 2019.

[Count-Based Exploration with the Successor Representation.](https://aaai.org/ojs/index.php/AAAI/article/view/5955) Marlos C. Machado, Marc G. Bellemare, Michael Bowling. Proceedings of the AAAI Conference on Artificial Intelligence (AAAI), 2020.

GPI、分层强化学习及相关方法

[A Robust Layered Control System for a Mobile Robot.](https://ieeexplore.ieee.org/document/1087032) R. Brooks. IEEE Journal on Robotics and Automation, 1986.

[Feudal Reinforcement Learning.](https://papers.nips.cc/paper/714-feudal-reinforcement-learning) Peter Dayan and Geoffrey E. Hinton. Advances in Neural Information Processing Systems (NIPS), 1992.

[Action Selection Methods Using Reinforcement Learning.](https://www.computing.dcu.ie/~humphrys/PhD/index.html) Mark Humphrys. PhD thesis, University of Cambridge, Cambridge, UK, 1997.

[Learning to Solve Multiple Goals.](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.37.8338&rep=rep1&type=pdf) Jonas Karlsson. PhD thesis, University of Rochester, Rochester, New York, 1997.

[Reinforcement Learning with Hierarchies of Machines.](https://papers.nips.cc/paper/1384-reinforcement-learning-with-hierarchies-of-machines) Ronald Parr and Stuart J. Russell. Advances in Neural Information Processing Systems (NIPS), 1997.

[Between MDPs and Semi-MDPs: A Framework for Temporal Abstraction in Reinforcement Learning.](https://www.sciencedirect.com/science/article/pii/S0004370299000521) Richard S.Sutton, DoinaPrecup, Satinder Singh. Artificial Intelligence, 1999.

[Hierarchical Reinforcement Learning with the MAXQ Value Function Decomposition.](https://jair.org/index.php/jair/article/view/10266) T. G. Dietterich. Journal of Artificial Intelligence Research, 2000.

[Multiple-Goal Reinforcement Learning with Modular Sarsa(O).](https://www.ijcai.org/Proceedings/03/Papers/233.pdf) Nathan Sprague and Dana Ballard. Proceedings of the International Joint Conference on Artificial Intelligence (IJCAI), 2003.

[Q-decomposition for Reinforcement Learning Agents.](https://people.eecs.berkeley.edu/~russell/papers/ml03-qdecomp.pdf) Stuart J. Russell and Andrew Zimdars. Proceedings of the International Conference on Machine Learning (ICML), 2003.

[Compositionality of Optimal Control Laws.](https://papers.nips.cc/paper/3842-compositionality-of-optimal-control-laws) E. Todorov. Advances in Neural Information Processing Systems (NIPS), 2009.

[Linear Bellman combination for control of character animation.](https://homes.cs.washington.edu/~jovan/papers/dasilva-2009-lbc.pdf) M. da Silva, F. Durand, and J. Popovic. ACM Transactions on Graphics, 2009.

[Hierarchy Through Composition with Multitask LMDPS.](http://proceedings.mlr.press/v70/saxe17a.html) A. M. Saxe, A. C. Earle, and B. Rosman. Proceedings of the International Conference on Machine Learning (ICML), 2017.

[Hybrid Reward Architecture for Reinforcement Learning.](https://papers.nips.cc/paper/7123-hybrid-reward-architecture-for-reinforcement-learning) Harm van Seijen, Mehdi Fatemi, Joshua Romoff, Romain Laroche, Tavian Barnes, and Jeffrey Tsang. Advances in Neural Information Processing Systems (NIPS), 2017.

[Feudal Networks for Hierarchical Reinforcement Learning.](https://arxiv.org/abs/1703.01161) Alexander Sasha Vezhnevets, Simon Osindero, Tom Schaul, Nicolas Heess, Max Jaderberg, David Silver, Koray Kavukcuoglu. Proceedings of the International Conference on Machine Learning (ICML), 2017.

[Composable Deep Reinforcement Learning for Robotic Manipulation.](https://arxiv.org/abs/1803.06773) T. Haarnoja, V. Pong, A. Zhou, M. Dalal, P. Abbeel, and S. Levine. IEEE International Conference on Robotics and Automation (ICRA), 2018.

[Composing Value Functions in Reinforcement Learning.](http://proceedings.mlr.press/v97/van-niekerk19a.html) Benjamin Van Niekerk, Steven James, Adam Earle, Benjamin Rosman. Proceedings of the International Conference on Machine Learning (ICML), 2019.

[Planning in Hierarchical Reinforcement Learning: Guarantees for Using Local Policies.](http://proceedings.mlr.press/v117/zahavy20a.html) Tom Zahavy, Avinatan Hasidim, Haim Kaplan, Yishay Mansour. International Conference on Algorithmic Learning Theory (ALT), 2020.

GPE + GPI、迁移学习及相关方法

[Transfer of Learning by Composing Solutions of Elemental Sequential Tasks.](https://link.springer.com/article/10.1007/BF00992700) Satinder Singh. Machine Learning, 1992.

[Transfer Learning for Reinforcement Learning Domains: A Survey.](https://www.jmlr.org/papers/volume10/taylor09a/taylor09a.pdf) Matthew E. Taylor and Peter Stone. Journal of Machine Learning Research, 2009.

[Transfer in Variable-Reward Hierarchical Reinforcement Learning.](http://homes.sice.indiana.edu/natarasr/Papers/var-reward.pdf) Neville Mehta, Sriraam Natarajan, Prasad Tadepalli, Alan Fern. Machine Learning, 2008.

[Learning and Transfer of Modulated Locomotor Controllers.](https://arxiv.org/abs/1610.05182) Nicolas Heess, Greg Wayne, Yuval Tassa, Timothy Lillicrap, Martin Riedmiller, David Silver. arXiv, 2016.

[Learning to Reinforcement Learn.](https://arxiv.org/abs/1611.05763) Jane X. Wang, Zeb Kurth-Nelson, Dhruva Tirumala, Hubert Soyer, Joel Z. Leibo, Remi Munos, Charles Blundell, Dharshan Kumaran, Matt Botvinick. arXiv, 2016.

[RL2: Fast Reinforcement Learning via Slow Reinforcement Learning.](https://arxiv.org/abs/1611.02779) Yan Duan, John Schulman, Xi Chen, Peter L. Bartlett, Ilya Sutskever, Pieter Abbeel. arXiv, 2016.

[Model-Agnostic Meta-Learning for Fast Adaptation of Deep Networks.](https://dl.acm.org/doi/10.5555/3305381.3305498) Chelsea Finn, Pieter Abbeel, Sergey Levine. Proceedings of the International Conference on Machine Learning (ICML), 2017.

[Successor Features for Transfer in Reinforcement Learning.](https://papers.nips.cc/paper/6994-successor-features-for-transfer-in-reinforcement-learning) André Barreto, Will Dabney, Rémi Munos, Jonathan J. Hunt, Tom Schaul, Hado van Hasselt, David Silver. Advances in Neural Information Processing Systems (NIPS), 2017.

[Transfer in Deep Reinforcement Learning Using Successor Features and Generalised Policy Improvement.](https://arxiv.org/pdf/1901.10964) André Barreto, Diana Borsa, John Quan, Tom Schaul, David Silver, Matteo Hessel, Daniel Mankowitz, Augustin Žídek, Rémi Munos. Proceedings of the International Conference on Machine Learning (ICML), 2018.

[Composing Entropic Policies Using Divergence Correction.](http://proceedings.mlr.press/v97/hunt19a/hunt19a.pdf) Jonathan Hunt, André Barreto, Timothy Lillicrap, Nicolas Heess. Proceedings of the International Conference on Machine Learning (ICML), 2019.

[Universal Successor Features Approximators.](https://arxiv.org/pdf/1812.07626) Diana Borsa, André Barreto, John Quan, Daniel Mankowitz, Rémi Munos, Hado van Hasselt, David Silver, Tom Schaul. International Conference on Learning Representations (ICLR), 2019.

[The Option Keyboard: Combining Skills in Reinforcement Learning.](https://papers.nips.cc/paper/9463-the-option-keyboard-combining-skills-in-reinforcement-learning) André Barreto, Diana Borsa, Shaobo Hou, Gheorghe Comanici, Eser Aygün, Philippe Hamel, Daniel Toyama, Jonathan J. Hunt, Shibl Mourad, David Silver, Doina Precup. Advances in Neural Information Processing Systems (NeurIPS), 2019.

[Transfer Learning in Deep Reinforcement Learning: A Survey.](https://arxiv.org/abs/2009.07888) Zhuangdi Zhu, Kaixiang Lin, Jiayu Zhou, arXiv, 2020.

[Fast Task Inference with Variational Intrinsic Successor Features.](https://openreview.net/pdf?id=BJeAHkrYDS) Steven Hansen, Will Dabney, André Barreto, Tom Van de Wiele, David Warde-Farley, Volodymyr Mnih. International Conference on Learning Representations (ICLR), 2020.

[Fast Reinforcement Learning with Generalized Policy Updates.](https://www.pnas.org/content/early/2020/08/13/1907370117) André Barreto, Shaobo Hou, Diana Borsa, David Silver, Doina Precup. Proceedings of the National Academy of Sciences, 2020.

神经科学中的后继表示

[The Hippocampus as a Predictive Map.](https://www.nature.com/articles/nn.4650) Kimberly Stachenfeld, Matthew Botvinick, Samuel Gershman. Nature Neuroscience, 2017.

[The Successor Representation in Human Reinforcement Learning.](https://www.nature.com/articles/s41562-017-0180-8) I. Momennejad, E. M. Russek, J. H. Cheong, M. M. Botvinick, N. D. Daw, S. J. Gershman. Nature Human Behaviour, 2017.

[Predictive Representations Can Link Model-Based Reinforcement Learning to Model-Free Mechanisms.](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005768) E. Russek, I. Momennejad, M. M. Botvinick, S. J. Gershman, N. D. Daw. PLOS Computational Biology, 2017.

[The Successor Representation: Its Computational Logic and Neural Substrates.](https://www.jneurosci.org/content/38/33/7193.short) Samuel J. Gershman. Journal of Neuroscience, 2018.

[Better Transfer Learning with Inferred Successor Maps.](https://papers.nips.cc/paper/9104-better-transfer-learning-with-inferred-successor-maps.pdf) Tamas J. Madarasz, Timothy E. Behrens. Advances in Neural Information Processing Systems (NeurIPS), 2019.

[Multi-Task Reinforcement Learning in Humans.](https://www.biorxiv.org/content/10.1101/815332v1.full.pdf) Momchil S. Tomov, Eric Schulz, and Samuel J. Gershman. bioRxiv, 2019.

[A neurally plausible model learns successor representations in partially observable environments.](https://papers.nips.cc/paper/9522-a-neurally-plausible-model-learns-successor-representations-in-partially-observable-environments) Eszter Vertes, Maneesh Sahani. Advances in Neural Information Processing Systems (NeurIPS), 2019.

[Neurobiological Successor Features for Spatial Navigation.](https://onlinelibrary.wiley.com/doi/abs/10.1002/hipo.23246) William de Cothi, Caswell Barry. Hippocampus, 2020.

[Linear Reinforcement Learning: Flexible Reuse of Computation in Planning, Grid Fields, and Cognitive Control.](https://www.biorxiv.org/content/10.1101/856849v3) Payam Piray, Nathaniel D. Daw. bioRxiv, 2020.
