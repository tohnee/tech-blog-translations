---
title: "通用能力智能体从开放式博弈中涌现"
title_en: "Generally capable agents emerge from open-ended play"
source: https://deepmind.google/blog/generally-capable-agents-emerge-from-open-ended-play/
site: deepmind
date: 2021-07-27
crawled: 2026-09-13
translated: 2026-09-13
---

# 通用能力智能体从开放式博弈中涌现

> 原文：[Generally capable agents emerge from open-ended play](https://deepmind.google/blog/generally-capable-agents-emerge-from-open-ended-play/) · Google DeepMind

近年来，人工智能智能体已在一系列复杂的游戏环境中取得成功。例如，[AlphaZero](https://deepmind.com/blog/article/alphazero-shedding-new-light-grand-games-chess-shogi-and-go) 在仅知道基本游戏规则的情况下，击败了国际象棋、将棋和围棋的世界冠军程序。通过[强化学习](https://en.wikipedia.org/wiki/Reinforcement_learning)（RL），这一单一系统通过反复试错的博弈过程进行学习。但 AlphaZero 仍然需要对每个游戏单独训练——无法在不从头重复强化学习过程的情况下直接学会另一个游戏或任务。强化学习的其他成果也是如此，例如 [Atari](https://deepmind.com/blog/article/Agent57-Outperforming-the-human-Atari-benchmark)、[Capture the Flag](https://deepmind.com/blog/article/capture-the-flag-science)、[StarCraft II](https://deepmind.com/blog/article/AlphaStar-Grandmaster-level-in-StarCraft-II-using-multi-agent-reinforcement-learning)、Dota 2 和[捉迷藏](https://openai.com/blog/emergent-tool-use/)（Hide-and-Seek）。DeepMind「通过解决智能来推进科学与造福人类」的使命促使我们探索如何克服这一局限，创造出行为更通用、更具适应性的 AI 智能体。这些智能体不再一次只学一个游戏，而是能够对全新的情况做出反应，玩转一整个游戏与任务的宇宙，包括从未见过的任务。

今天，我们发布了《[Open-Ended Learning Leads to Generally Capable Agents](https://arxiv.org/abs/2107.12808)》（开放式学习造就通用能力智能体）预印本，详细介绍了我们训练一个无需人类交互数据、能够玩多种不同游戏的智能体的初步尝试。我们创建了一个名为 XLand 的庞大游戏环境，其中包含一致且人类可理解的 3D 世界中的众多多人游戏。这一环境使我们能够设计新的学习算法，动态控制智能体的训练方式及其训练所用的游戏。智能体的能力随着训练中出现的挑战而迭代提升，学习过程不断调整训练任务，使智能体永不停止学习。最终得到的智能体能够在广泛谱系的任务中取得成功——从简单的寻找物体问题，到捉迷藏、夺旗等训练中从未遇到过的复杂游戏。我们发现该智能体表现出实验探索等通用的、启发式的行为，这些行为广泛适用于众多任务，而非专属于某个单一任务。这一新方法朝着创造更通用、能在不断变化的环境中快速适应的智能体迈出了重要一步。

## 一个训练任务的宇宙

训练数据的匮乏——这里的「数据」点是不同的任务——一直是限制强化学习训练出的智能体行为足够通用、难以跨游戏应用的主要因素之一。由于无法在足够庞大的任务集合上训练智能体，用强化学习训练的智能体一直无法将其学到的行为适配到新任务上。但通过设计一个支持[程序化生成任务](https://en.wikipedia.org/wiki/Procedural_generation)的仿真空间，我们的团队开创了一种方法，可以在程序化创建的任务上进行训练并从中生成经验。这使我们能够在 XLand 中纳入数十亿个任务，涵盖多样的游戏、世界和玩家。

我们的 AI 智能体以 3D 第一人称化身栖身于一个旨在模拟物理世界的多人环境中。玩家通过观察 RGB 图像感知周围环境，并获得其目标的文字描述，在一系列游戏上接受训练。这些游戏有的非常简单，例如寻找物体和在世界中导航的合作游戏，玩家的目标可以是「靠近紫色立方体」。更复杂的游戏可以基于在多个有奖励的选项中进行选择，例如「靠近紫色立方体，或将黄色球体放到红色地板上」；更具竞争性的游戏则包括与共同玩家对抗，例如对称捉迷藏，每个玩家的目标是「看到对手，并让对手看不到我」。每个游戏定义玩家的奖励，每个玩家的最终目标是最大化奖励。

由于 XLand 可以通过程序来定义，游戏空间能够以自动化、算法化的方式生成数据。而且由于 XLand 中的任务涉及多个玩家，共同玩家的行为会极大影响 AI 智能体面临的挑战。这些复杂的非线性交互构成了理想的训练数据来源，因为有时环境中组件的微小变化就可能导致智能体所面临挑战的巨大变化。

![信息图：解释"XLand 宇宙"，其中任务被定义为游戏加世界加共同玩家。图中以繁星密布的星云表示"游戏星系"，并标注了"Capture the Cube"、"Match a Sphere and a Cube"和"Hide and Seek"等示例游戏，各自详述规则与游戏特征。下方是一个由多样化的基于 3D 网格的"世界"构成的球状天体，指向带有方块、坡道和彩色平台的具体 3D 竞技场设计。](https://lh3.googleusercontent.com/5isaSjl6ovHtYp_920guPbSnifCuPQDVHKIDetX_2s61TxlCQJyAukQsFPbzy0sFxKfGyLpcLx0dDjlH78PS3LpbFjoKAxVtA0QqUnNy-DPPapORZQ=w1440)

XLand 由一个游戏星系构成（图中以嵌入 2D 的点表示，颜色与大小基于其属性），每个游戏可以在许多不同的仿真世界中游玩，这些世界的拓扑结构与特性平滑变化。XLand 任务的一个实例将游戏与世界及共同玩家组合在一起。

## 训练方法

我们研究的核心是深度强化学习在训练智能体神经网络中的作用。我们使用的神经网络架构在智能体的内部循环状态之上提供了注意力机制——借助针对智能体当前所玩游戏独有的子目标估计来引导智能体的注意力。我们发现这种目标注意力智能体（GOAT，goal-attentive agent）能学到更通用的能力策略。

我们还探索了这样一个问题：什么样的训练任务分布才能产生最好的智能体，尤其是在如此庞大的环境中？我们使用的动态任务生成允许持续改变智能体训练任务的分布：每个任务的生成都既不太难也不太易，恰好适合训练。接着，我们使用[基于种群的训练](https://deepmind.com/blog/article/population-based-training-neural-networks)（PBT），依据旨在提升智能体通用能力的适应度来调整动态任务生成的参数。最后，我们将多轮训练串联起来，让每一代智能体都能以前一代为基础实现自我提升。

由此形成了一个以深度强化学习为核心的最终训练流程，每一步经验都会更新智能体的神经网络：

- 经验的每一步都来自根据智能体行为动态生成的训练任务；
- 智能体的任务生成函数会根据智能体的相对表现与鲁棒性发生变异；
- 在最外层循环中，各代智能体相互承接、不断为多人环境提供更丰富的共同玩家，并重新定义进展本身的度量方式。

这一训练过程从零开始，迭代式地构建复杂性，不断改变学习问题以让智能体保持学习。这一组合学习系统的迭代特性——它优化的不是一个有界的性能指标，而是迭代定义的通用能力谱系——为智能体带来一个潜在开放式（open-ended）的学习过程，其上限仅受环境空间与智能体神经网络表达能力的限制。

![示意图：展示通用能力智能体跨越四代的迭代训练过程，突出 XLand 中基于种群的训练（PBT）、带目标注意力模块的智能体架构，以及性能评估指标。](https://lh3.googleusercontent.com/lu3egyHeqNE0w1wgoyBBK-M2ciMC2SHqrU0bhZTMTCDrs1vdLe4anzbYmvPj1xUXu47Tf-E8Wub8m_dbIn_EkaNrseblbJFGMbPhRJ12pJceKjlH=w1440)

智能体的学习过程由多个时间尺度上的动态构成。

## 度量进展

为了度量智能体在这个庞大宇宙中的表现，我们使用与训练数据相分离的游戏和世界创建了一组评估任务。这些「留存」（held-out）任务包括专门由人类设计的任务，例如捉迷藏和夺旗。

由于 XLand 规模庞大，理解并刻画智能体的表现本身就是一项挑战。每个任务涉及不同的复杂程度、不同量级的可达奖励以及不同的智能体能力，因此仅仅对留存任务的奖励取平均，就会掩盖复杂度与奖励的实际差异——并实际上等于把所有任务视为同等有趣，而这在程序化生成的环境中并不成立。

为了克服这些局限，我们采用了另一种方法。首先，我们使用当前训练的玩家集合计算纳什均衡值，对每个任务的分数进行归一化。其次，我们考虑归一化分数的完整分布——不看平均归一化分数，而是看归一化分数的不同分位数——以及智能体至少获得一步奖励的任务占比：即参与率。这意味着，只有当某个智能体在所有分位数上都超过另一个智能体时，才认为它更好。这种度量方式为我们评估智能体的表现与鲁棒性提供了有意义的途径。

## 更通用的智能体

在训练了五代智能体之后，我们看到学习和表现在留存评估空间中持续改进。在 XLand 中游玩了约 70 万个不同游戏、4,000 个不同世界之后，最后一代的每个智能体经由 340 万个不同任务积累了 2,000 亿个训练步骤。到此时，我们的智能体已经能够参与每一个程序化生成的评估任务，只有少数几个连人类也无法完成的任务除外。我们看到的结果清晰地展现出跨任务空间的通用零样本行为——归一化分数分位数的前沿在不断推进。

![图表：展示各代智能体的评估进展。上方为测试评估性能的 3D 可视化，涵盖不同分位数与最多 152G 的学习步数，并配有归一化性能分位数折线图，突出智能体参与 94% 的游戏、取得 110% 的归一化性能中位数。下方为条形图，展示第 1G、38G 和 152G 代智能体在手工设计关卡（Tool use、Ridge-Fencing、Hide and Seek、Capture the Cube、Cooperate or Compete 和 Counter Yellow Sphere）上的零样本泛化能力。](https://lh3.googleusercontent.com/AOo8I0VlRJu1s7R_8msYQDJKqcBcG-lry6XakgzCg278ex2lSjuB-fzESRO81uJmv-vH1DZa1Zepflk9S9JOrZabde7jkW7ppDTpzN_bwxy6rjw8KQ=w1440)

最后一代智能体的学习进展，展示了我们的测试指标如何随时间推进，并同样转化为手工设计留存测试任务上的零样本表现。

从定性角度观察我们的智能体，我们经常看到通用的、启发式的行为涌现——而不是针对个别任务高度优化的特定行为。智能体并非确切知道在新情境中该做什么「最优之事」，我们看到的证据是智能体会不断实验、改变世界状态，直到达到一个有奖励的状态。我们还看到智能体依赖于使用其他工具，包括用来遮挡视线、搭建坡道以及取回其他物体的道具。由于环境是多人环境，我们可以考察智能体在训练留存的社会困境任务时的行为演化，例如「胆小鬼博弈」（chicken）这样的游戏。随着训练的推进，我们的智能体在与自身副本对战时似乎表现出更多合作行为。鉴于环境的性质，很难精确判定意图——我们看到的行为往往看似出于偶然，但我们仍然观察到它们持续出现。

![示意图：测试示例 1，XLand 中的智能体动态评估并改变其目标，从将黑色金字塔放到橙色地板上，变为将黑色金字塔放到黄色球体附近；图中展示了游戏世界布局、目标选项、价值预测曲线，以及逐步的智能体观测、内部状态可视化和第三人称视角。](https://lh3.googleusercontent.com/QHiWeiyNX490opQVk4ltuHV5xteKvQd0BYTSOBG0BMy2KCQly0IlokZOngRqwMPTtLFRq-eVAf-Tn6W7JnNBJt7GLiRgPFFx5HOUUPElG8wYV3B9Cw=w1440)

![示意图：测试示例 2，XLand 中的智能体学会使用工具够到紫色金字塔，图中展示了世界布局、目标、智能体在一个回合中的价值预测、第一人称观测、内部状态表示以及游戏的第三人称视角。](https://lh3.googleusercontent.com/fgDlhsMosxHKCjpJyoOvimEHZuoAo7ANbRqZoApxx5YVtlrh1yd347ZYNQb0ubot0kNHL9NdfaDWx3V1BKvFQqM8ieF_Q65XZuO5tlzJN-jyi_eW=w1440)

![示意图：测试示例 3，XLand 中的智能体面对一个逻辑谜题，图中展示了世界布局、多谓词目标、智能体在一个回合中的价值预测、第一人称观测、内部状态表示以及游戏的第三人称视角。](https://lh3.googleusercontent.com/uRNQN7sg8w1LqaPHzi9RbNkoOysY4o-o6TuAsrNdrk-8Ztls19sYw8DPH9kN7g7ZpP9MXdIZg4K-HKjPLC1kyH6S9_-mFqvcX8St9tUVCf3_xyiu=w1440)

上图：涌现出哪些类型的行为？(1) 智能体展现出随战术局势展开而切换目标选项的能力。(2) 智能体展现了工具使用的苗头，例如搭建坡道。(3) 智能体学会了一种通用的试错实验行为，在识别到正确状态已找到时停止。下图：在同一个手工设计的探针任务中，相同的智能体以多种方式利用物体到达作为目标的紫色金字塔。

![3D 动画：一个蓝色胶囊形状的智能体在带有红色、黄色和紫色方块的 XLand 多层游戏竞技场中穿行，绕过障碍物抵达紫色金字塔。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6227da78191c65b6b3fd8b84_Fig207.gif)

在同一个手工设计的探针任务中，相同的智能体以多种方式利用物体到达作为目标的紫色金字塔。

![3D 仿真：XLand 竞技场中一个蓝色胶囊形状的智能体，用一根横梁抬起紫色立方体以绕过障碍物，抵达紫色金字塔。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6227da8818c4c5fe8891d327_Fig208.gif)

在同一个手工设计的探针任务中，相同的智能体以多种方式利用物体到达作为目标的紫色金字塔。

![3D 仿真：XLand 竞技场中一个蓝色胶囊形状的智能体，用一根横梁抬起紫色立方体以绕过障碍物，抵达紫色金字塔。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6227da95b896c3762bbd77cf_Fig209.gif)

在同一个手工设计的探针任务中，相同的智能体以多种方式利用物体到达作为目标的紫色金字塔。

通过分析智能体的内部表示，我们可以说：通过在庞大任务空间中采用这种强化学习方法，我们的智能体感知到了自身身体的基本属性与时间的流逝，并且理解它们所遇到游戏的高层结构。或许更有意思的是，它们能清晰地识别环境中的奖励状态。这种在新任务中的通用性与行为多样性，暗示了在这些智能体上进行下游任务微调的潜力。例如，我们在技术论文中展示，只需对一个新提出的复杂任务进行 30 分钟的针对性训练，智能体就能快速适应，而从零开始用强化学习训练的智能体则完全学不会这些任务。

通过开发 XLand 这样的环境以及支持开放式复杂性生成的新训练算法，我们看到了强化学习智能体零样本泛化的明确迹象。虽然这些智能体开始在这一任务空间内具备通用能力，我们期待继续研究与开发，进一步提升它们的表现，创造出适应性更强的智能体。

更多细节请参阅[我们技术论文的预印本](https://arxiv.org/abs/2107.12808)，以及我们所见结果的[视频](https://youtu.be/lTmL7jwFfdw)。希望这能帮助其他研究者同样看到一条创造适应性更强、更具通用能力 AI 智能体的新路径。如果你为这些进展感到兴奋，欢迎考虑加入我们的团队。

**致谢**

本博文基于开放式学习团队（Open-Ended Learning Team）的共同工作（按名字字母顺序排列）：Adam Stooke、Anuj Mahajan、Catarina Barros、Charlie Deck、Jakob Bauer、Jakub Sygnowski、Maja Trebacz、Max Jaderberg、Michael Mathieu、Nat McAleese、Nathalie Bradley-Schmieg、Nathaniel Wong、Nicolas Porcel、Roberta Raileanu、Steph Hughes-Fitt、Valentin Dalibard、Wojciech Marian Czarnecki。
