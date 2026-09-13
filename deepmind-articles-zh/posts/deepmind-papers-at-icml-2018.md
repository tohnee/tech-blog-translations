---
title: "DeepMind 在 ICML 2018 的论文"
title_en: "DeepMind papers at ICML 2018"
source: https://deepmind.google/blog/deepmind-papers-at-icml-2018/
site: deepmind
date: 2018-07-09
crawled: 2026-09-13
translated: 2026-09-13
---

# DeepMind 在 ICML 2018 的论文

> 原文：[DeepMind papers at ICML 2018](https://deepmind.google/blog/deepmind-papers-at-icml-2018/) · Google DeepMind

[2018 年国际机器学习大会](https://icml.cc/)（ICML 2018）将于 7 月 10 日至 15 日在瑞典斯德哥尔摩举行。

为与会者规划这一周的行程提供便利，我们在此分享 DeepMind 在 ICML 的报告日程（**可在此下载 pdf 版本** [**这里**](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/deepmind-papers-at-icml-2018/ICML2018-DM-schedule.pdf)）。我们期待会议上必将涌现的众多精彩讨论、想法与合作！


### 高效神经音频合成（Efficient Neural Audio Synthesis）

**作者：** Nal Kalchbrenner、Erich Elsen、Karen Simonyan、Seb Nouri、Norman Casagrande、Edward Lockhart、Sander Dieleman、Aaron van den Oord、Koray Kavukcuoglu

序列模型在音频、视觉和文本领域，无论是在估计数据分布还是生成目标样本方面，都取得了最先进的结果。然而，让这一类模型实现高效采样、同时几乎不损失质量，一直是一项难以企及的任务。以文本到语音合成为重点，我们展示了紧凑的循环架构、极高程度的权重稀疏化以及一种新颖的变量重排序，能够在保持高音频保真度的同时大幅降低采样延迟。我们首先描述了一个紧凑的单层循环神经网络 WaveRNN，它带有一个新颖的双 softmax 层，质量可与最先进的 WaveNet 模型相匹敌。WaveRNN 的持久化 GPU 内核能够以 4 倍于实时的速度合成 24kHz 16 位音频。随后，我们对模型应用了权重稀疏化技术。我们证明，在权重数量恒定的条件下，大型稀疏网络的性能优于小型稠密网络。利用大型 Sparse WaveRNN，我们展示了在低功耗手机 CPU 上进行实时高保真音频合成的可行性，这也是首次在资源受限的手机 CPU 上实现实时高保真音频合成。最后，我们引入了一种对联合分布分解中变量的新颖重排序。这一重排序使得可以用「对遥远未来样本的空洞依赖」换取「分批生成的能力」。Batch WaveRNN 每步可产生多达 16 个样本并保持高质量，使音频合成的速度达到实时的 40 倍。

**报告：**

- 上午 11:00 – 11:20 @ Victoria（口头报告）
- 下午 06:15 – 09:00 @ Hall B #105（海报）

### 使用 MCTS 网络学习搜索（Learning to Search with MCTSnets）

**作者：** Arthur Guez\*、Theophane Weber\*、Ioannis Antonoglou、Karen Simonyan、Oriol Vinyals、Daan Wierstra、Remi Munos、David Silver

规划问题是人工智能中最重要、被研究得最充分的问题之一。它们通常由树搜索算法求解：算法向未来模拟推进、评估未来状态，并将这些评估回传至搜索树的根节点。在这些算法中，蒙特卡洛树搜索（Monte-Carlo tree search，MCTS）是最通用、最强大且使用最广泛的算法之一。MCTS 的典型实现使用精心设计的规则，并针对特定领域的特点进行优化。这些规则控制模拟向何处遍历、对到达的状态评估什么、以及如何回传这些评估。在本文中，我们改为学习在何处、评估什么、如何搜索。我们的架构被称为 MCTSnet，它将基于模拟的搜索纳入神经网络内部，通过扩展、评估和回传一个向量嵌入来实现。网络的参数通过基于梯度的优化进行端到端训练。当应用于著名的规划问题「推箱子」（Sokoban）中的小规模搜索时，学习到的搜索算法显著优于 MCTS 基线。

**报告：**

- 上午 11:20 – 11:30 @ Victoria（口头报告）
- 下午 06:15 – 09:00 @ Hall B #92（海报）

### LeapsAndBounds：一种近似最优的算法配置方法（LeapsAndBounds: A Method for Approximately Optimal Algorithm Configuration）

**作者：** Gellert Weisz、Andras Gyorgy 和 Csaba Szepesvari

我们研究为通用求解器进行配置的问题，使其能在从未知分布中抽取的问题实例上高效运行。配置器的目标是找到一个在大多数实例上平均运行快速的配置，同时使总工作量最少。它可以在一个随机实例上运行选定的求解器，直到求解器完成或达到超时。我们提出 LEAPSANDBOUNDS，一种在随机选取的问题实例上以越来越长的时间测试各配置的算法。我们证明，LEAPSANDBOUNDS 返回的配置的受限期望运行时间接近最优期望运行时间，同时我们的算法自身运行时间接近最优。我们的结果表明，LEAPSANDBOUNDS 比 Kleinberg 等人（2017）最近的算法更高效——据我们所知，后者是唯一另一种声称拥有非平凡理论保证的算法配置方法。在公开基准上配置一个公开 SAT 求解器的实验结果也印证了我们方法的优越性。

**报告：**

- 上午 11:30 – 11:40 @ A6（口头报告）
- 下午 06:15 – 09:00 @ Hall B #165（海报）

### 用于分布式强化学习的隐式分位数网络（Implicit Quantile Networks for Distributional Reinforcement Learning）

**作者：** Will Dabney\*、Georg Ostrovski\*、David Silver、Remi Munos

在这项工作中，我们建立在分布式强化学习的最新进展之上，给出了一个普遍适用、灵活且达到最先进水平的 DQN 分布式变体。我们通过使用分位数回归来近似状态-动作回报分布的完整分位数函数来实现这一点。通过对样本空间上的分布进行重参数化，这产生了一个隐式定义的回报分布，并衍生出一大类风险敏感策略。我们展示了在 ALE 的 57 个 Atari 2600 游戏上的性能提升，并利用算法隐式定义的分布研究了风险敏感策略在 Atari 游戏中的影响。

**报告：**

- 上午 11:40 – 11:50 @ A1（口头报告）
- 下午 06:15 – 09:00 @ Hall B #3（海报）

### 图网络作为可学习物理引擎用于推理与控制（Graph Networks as Learnable Physics Engines for Inference and Control）

**作者：** Alvaro Sanchez、Nicolas Heess、Jost Tobias Springenberg、Josh Merel、Martin Riedmiller、Raia Hadsell、Peter Battaglia

理解并与日常物理场景交互，需要关于世界结构的丰富知识——这些知识或者隐式地表示在价值或策略函数中，或者显式地表示在转移模型中。在这里，我们介绍一类新的可学习模型——基于图网络——它们为复杂动态系统的以物体为中心和以关系为中心的表示实现了一种归纳偏置。我们的结果表明，作为前向模型，我们的方法在八个不同的物理系统（我们在参数和结构上对其进行了变化）上支持准确的预测，以及出人意料地强大而高效的泛化。我们还发现，我们的推理模型可以从真实和仿真数据中进行系统辨识。我们的模型也是可微的，支持通过基于梯度的轨迹优化进行在线规划，以及离线策略优化。我们的框架为利用和开发关于世界的丰富知识提供了新的机会，并朝着构建拥有更像人类的世界表示的机器迈出了关键一步。

**报告：**

- 上午 11:50 – 中午 12:00 @ Victoria（口头报告）
- 下午 06:15 – 09:00 @ Hall B #84（海报）

### 更稳健的双稳健离策略评估（More Robust Doubly Robust Off-policy Evaluation）

**作者：** Mehrdad Farajtabar、Yinlam Chow 和 Mohammad Ghavamzadeh

我们研究强化学习（RL）中的离策略评估（OPE）问题，其目标是根据由另一（些）策略生成的数据来估计某个策略的性能。特别地，我们关注由重要性采样（IS）组件和一个性能模型组成的双稳健（DR）估计器，它们同时利用了 IS 的低（或零）偏差和模型的低方差。虽然模型的准确性对 DR 的整体性能有巨大影响，但在 OPE 中使用 DR 估计器的大多数工作都集中在改进 IS 部分，而对如何学习模型着墨不多。在本文中，我们提出了一类替代的 DR 估计器，称为更稳健双稳健（MRDR），它通过最小化 DR 估计器的方差来学习模型参数。我们首先给出在 RL 中学习 DR 模型的一个表述，然后推导出 DR 估计器在上下文老虎机和 RL 两种情形下的方差公式，使其关于模型参数的梯度可以从样本中估计，并提出高效最小化方差的方法。我们证明 MRDR 估计器具有强一致性和渐近最优性。最后，我们在老虎机和 RL 基准问题上评估 MRDR，并将其性能与现有方法进行比较。

**报告：**

- 上午 11:50 – 中午 12:00 @ A1（口头报告）
- 下午 06:15 – 09:00 @ Hall B #62（海报）

### 条件神经过程（Conditional Neural Processes）

**作者：** Marta Garnelo、Dan Rosenbaum、Christopher Maddison、Tiago Ramalho、David Saxton、Murray Shanahan、Yee Whye Teh、Danilo Rezende、S. M. Ali Eslami

深度神经网络擅长函数逼近，但它们通常需要为每个新函数从头训练。另一方面，贝叶斯方法（如高斯过程，GP）能够利用先验知识在测试时快速推断新函数的形状。然而，GP 计算代价高昂，且设计合适的先验可能很困难。在本文中，我们提出了一族神经模型——条件神经过程（Conditional Neural Processes，CNPs）——结合了二者的优点。CNP 的灵感来自 GP 等随机过程的灵活性，但其结构是神经网络，并通过梯度下降训练。CNP 在仅观察少量训练数据点后就能做出准确预测，同时可以扩展到复杂函数和大型数据集。我们在一系列经典的机器学习任务（包括回归、分类和图像补全）上展示了该方法的性能与多功能性。

**报告：**

- 下午 02:10 – 02:20 @ Victoria（口头报告）
- 下午 06:15 – 09:00 @ Hall B #130（海报）

### 面向部分可观测环境的带空间记忆的生成式时序模型（Generative Temporal Models with Spatial Memory for Partially Observed Environments）

**作者：** Marco Fraccaro、Danilo Jimenez Rezende、Yori Zwols、Alexander Pritzel、S. M. Ali Eslami、Fabio Viola

在基于模型的强化学习中，可以利用环境的生成模型与时序模型来提升智能体性能：或是在训练期间调整智能体的表示，或是作为显式规划机制的一部分。然而，由于在更大、可能部分可观测的 3D 环境中训练此类模型十分困难，它们的实际应用一直局限于过于简化的环境。在这项工作中，我们为这类具有挑战性的环境引入了一种新颖的动作条件生成模型。该模型的特点是一个非参数化空间记忆系统，我们在其中存储学到的、解耦的环境表示。低维空间更新由一个状态空间模型计算，该模型利用了移动智能体先验动态的知识；高维视觉观测则由一个变分自编码器建模。其结果是一个可扩展的架构，能够在一系列部分可观测的 2D 和 3D 环境中进行跨越数百个时间步的连贯预测。

**报告：**

- 下午 02:30 – 02:50 @ A7（口头报告）
- 下午 06:15 – 09:00 @ Hall B #101（海报）

### 通过因子化实现解耦（Disentangling by Factorising）

**作者：** Hyunjik Kim、Andriy Mnih

我们定义并解决了一个无监督学习问题：对由独立变化因子生成的数据进行解耦表示学习。我们提出 FactorVAE，该方法通过鼓励表示的分布呈因子化（从而在各维度上相互独立）来实现解耦。我们证明它改进了 β-VAE：在解耦程度与重建质量之间提供了更好的权衡，并且对训练迭代次数更加鲁棒。此外，我们指出了常用解耦度量的问题，并引入了一种不受这些问题困扰的新度量。

**报告：**

- 下午 02:50 – 03:00 @ A7（口头报告）
- 下午 06:15 – 09:00 @ Hall B #90（海报）

### 在玩耍中学习——从零解决稀疏奖励任务（Learning by Playing – Solving Sparse Reward Tasks from Scratch）

**作者：** Martin Riedmiller、Roland Hafner、Thomas Lampe、Michael Neunert、Jonas Degrave、Tobias Springenberg

我们提出调度辅助控制（Scheduled Auxiliary Control，SAC），这是强化学习（RL）情境下的一种新学习范式。SAC 使智能体能够在存在多个稀疏奖励信号的情况下从零开始学习复杂行为。为此，智能体被配备一组通用的辅助任务，并通过离策略 RL 同时尝试学习这些任务。我们方法背后的关键思想是：主动地（以学习到的方式）调度和执行辅助策略，能让智能体高效地探索其环境——使其在稀疏奖励 RL 中表现出色。我们在多个具有挑战性的机器人操作设定中的实验证明了这一方法的威力。

更多内容请见 DeepMind [博客](https://deepmind.com/blog/learning-playing/)。

**报告：**

- 下午 04:20 – 04:40 @ A1（口头报告）
- 下午 06:15 – 09:00 @ Hall B #41（海报）

### 利用激活记忆实现快速参数学习（Fast Parametric Learning with Activation Memorization）

**作者：** Jack W Rae、Chris Dyer、Peter Dayan、Timothy P Lillicrap

用反向传播训练的神经网络往往难以识别仅被观察到少数几次的类别。在大多数类别标签都很稀少的应用（如语言建模）中，这可能成为性能瓶颈。一种潜在的补救办法是为网络增配一个快速学习的非参数模型，让它关注近期的激活。我们探索了一种简化的架构，将模型参数的一个子集视为快速记忆存储。相比传统记忆，这有助于在更长的时间间隔内保留信息，且不需要额外的空间或计算。在图像分类任务中，我们在 Omniglot 图像课程任务上展示了对新类别的更快绑定。我们还展示了基于词的语言模型在新闻报道（GigaWord）、书籍（Project Gutenberg）和维基百科文章（WikiText-103）上的性能提升——后者达到了最先进的困惑度。

**报告：**

- 下午 04:40 – 04:50 @ Victoria（口头报告）
- 下午 06:15 – 09:00 @ Hall B #121（海报）

### 用学习矩方法学习隐式生成模型（Learning Implicit Generative Models with the Method of Learned Moments）

**作者：** Suman Ravuri、Shakir Mohamed、Mihaela Rosca 和 Oriol Vinyals

我们提出了一种用于训练大规模隐式生成模型的矩方法（MoM）算法。在这一设定下，矩估计面临两个问题：定义学习模型参数所需的数百万个矩往往很困难；而且难以确定在指定矩时哪些属性是有用的。针对第一个问题，我们引入了一个矩网络，并将矩定义为网络输出关于其参数和隐含单元的梯度。为解决第二个问题，我们使用渐近理论阐明了对矩的期望——即它们应当最小化估计模型参数的渐近方差——并引入了一个目标来学习更好的矩。由这一学习矩方法（MoLM）产生的目标序列能够训练高质量的神经图像采样器。在 CIFAR-10 上，我们证明 MoLM 训练的生成器比用梯度惩罚正则化对抗目标训练的生成器取得了显著更高的 Inception 分数和更低的 Frechet Inception 距离。这些生成器在 CelebA 上还取得了接近满分的多尺度结构相似性分数，并能生成分辨率高达 128×128 的高质量样本。

**报告：**

- 下午 04:40 – 04:50 @ A7（口头报告）
- 下午 06:15 – 09:00 @ Hall B #112（海报）

### 为强化学习智能体自动生成目标（Automatic Goal Generation for Reinforcement Learning Agents）

**作者：** David Held、Xinyang Geng、Carlos Florensa、Pieter Abbeel

强化学习是训练智能体执行任务的强大技术。然而，用强化学习训练的智能体只能完成由其奖励函数指定的单一任务。这样的方法无法很好地扩展到智能体需要执行多样化任务集合的场景，例如导航到房间中的不同位置，或将物体移动到不同地点。相反，我们提出了一种方法，让智能体能够自动发现它有能力完成的任务范围。我们使用一个生成器网络为智能体提出要尝试实现的任务，任务以目标状态的形式指定。生成器网络通过对抗训练进行优化，以产生对智能体而言难度始终合适的任务。因此，我们的方法能够自动生成一个供智能体学习的任务课程。我们展示，通过使用这一框架，智能体可以在无需任何环境先验知识的情况下高效且自动地学会执行一组广泛的任务。我们的方法还能学会完成稀疏奖励的任务——这类任务历来构成重大挑战。

**报告：**

- 下午 04:40 – 04:50 @ A1（口头报告）
- 下午 06:15 – 09:00 @ Hall B #135（海报）

### 机器心智理论（Machine Theory of Mind）

**作者：** Neil C. Rabinowitz、Frank Perbet、H. Francis Song、Chiyuan Zhang、S. M. Ali Eslami、Matthew Botvinick

心智理论（Theory of mind，ToM）广义上指人类表征他人心理状态的能力，包括他人的欲望、信念和意图。我们提议训练机器也构建这样的模型。我们设计了一个心智理论神经网络——ToMnet——它使用元学习来为其遇到的智能体构建模型。ToMnet 为智能体的未来行为学习一个强大的先验模型，并且仅凭少量行为观察，就能引导出关于智能体特征和心理状态的更丰富预测。我们将 ToMnet 应用于在简单网格世界环境中行动的智能体，表明它能够为来自不同种群的随机、算法和深度 RL 智能体建模，并且通过了经典的 ToM 任务，例如「Sally-Anne」测试——即识别出他人可能对世界抱有错误信念。

**报告：**

- 下午 05:00 – 05:20 @ A3（口头报告）
- 下午 06:15 – 09:00 @ Hall B #208（海报）

### Tsallis 熵正则化 MDP 中的路径一致性学习（Path Consistency Learning in Tsallis Entropy Regularized MDPs）

**作者：** Ofir Nachum、Yinlam Chow 和 Mohammad Ghavamzadeh

我们研究稀疏熵正则化强化学习（ERL）问题，其中熵项是 Tsallis 熵的一种特殊形式。这一表述的最优策略是稀疏的，即在每个状态上，它只对少数动作具有非零概率。这解决了标准香农熵正则化 RL（soft ERL）表述的主要缺点——后者的最优策略是 softmax 形式，因此可能给非最优动作分配不可忽略的概率质量。随着动作数量增加，这一问题会加剧。在本文中，我们延续 Nachum 等人（2017）在 soft ERL 设定下的工作，为稀疏 ERL 问题提出了一类新颖的路径一致性学习（PCL）算法，称为稀疏 PCL，它既可使用在策略数据，也可使用离策略数据。我们首先推导出一个稀疏一致性方程，它刻画了稀疏 ERL 的最优价值函数与策略沿任意系统轨迹之间的关系。至关重要的是，其弱形式的逆命题同样成立：我们量化了满足稀疏一致性的策略的次优性，并证明随着动作数量增加，这一次优性优于 soft ERL 最优策略的次优性。然后我们利用这一结果推导出稀疏 PCL 算法。我们通过实验比较稀疏 PCL 与其 soft 版本，并展示了它的优势，尤其是在动作数量庞大的问题中。

**报告：**

- 下午 05:20 – 05:40 @ A1（口头报告）
- 下午 06:15 – 09:00 @ Hall B #172（海报）

### 使用后继特征与广义策略改进实现深度强化学习中的迁移（Transfer in Deep Reinforcement Learning Using Successor Features and Generalised Policy Improvement）

**作者：** Andre Barreto、Diana Borsa、John Quan、Tom Schaul、David Silver、Matteo Hessel、Daniel Makowitz、Augustin Zidek、Remi Munos

跨任务迁移技能的能力，有潜力把强化学习（RL）智能体扩展到目前无法企及的环境。最近，一个基于后继特征（successor features，SFs）与广义策略改进（generalised policy improvement，GPI）两个思想的框架被提出，作为迁移技能的一种原则性方法。在本文中，我们研究将 SF&GPI 与深度学习的表示能力相结合的可行性。由于在深度 RL 中我们需要同时学习 SF&GPI 的所有组件，它们之间现存的相互依赖可能导致不稳定。在这项工作中，我们为这一问题提出了一种解决方案，使 SF 与 GPI 能够在线地、大规模地使用。为了通过实验验证这一主张，我们将所提出的方法应用于一个需要数亿次转移才能求解的复杂 3D 环境。我们表明，SF&GPI 所促成的迁移几乎能立即在未见任务上产生合理的策略。我们还展示了如何在迁移来的策略基础上学习针对新任务特化的策略，然后可以将其加入智能体的技能集以备将来使用。

**报告：**

- 下午 05:20 – 05:40 @ A3（口头报告）
- 下午 06:15 – 09:00 @ Hall B #163（海报）

### 曾经沧海：带情景回忆的元学习（Been There, Done That: Meta-Learning with Episodic Recall）

**作者：** Samuel Ritter、Jane Wang、Sid Jayakumar、Zeb Kurth-Nelson、Charles Blundell、Razvan Pascanu、Matt Botvinick

元学习智能体已经展示了快速探索并利用从其训练所用任务分布中抽取的新任务的能力。然而，当这些智能体遇到它们在遥远的过去探索过的情境时，它们无法记住以往探索的结果。因此，它们无法立即利用先前发现的解决方案，而必须再次从头探索。在这项工作中，我们主张：记住过去探索结果的必要性在自然环境中无处不在。我们提出一种形式化方法来建模这类反复出现的环境结构，然后开发了一个用于求解此类环境的元学习架构。该架构将标准的 LSTM 工作记忆与可微的神经情景记忆融合在一起。我们在四种循环状态随机过程环境中探索这一情景 LSTM 的能力：1）情景上下文老虎机；2）组合式上下文老虎机；3）情景两步任务；4）上下文水迷宫导航。

**报告：**

- 下午 05:40 – 05:50 @ A3（口头报告）
- 下午 06:15 – 09:00 @ Hall B #209（海报）

### 对抗风险与以弱攻击做评估的危险（Adversarial Risk and the Dangers of Evaluating Against Weak Attacks）

**作者：** Jonathan Uesato、Brendan O'Donoghue、Aaron van den Oord 和 Pushmeet Kohli。

本文研究了最近提出的对抗样本防御方法与对抗鲁棒性评估方法。训练后的神经网络中对抗样本的存在反映出这样一个事实：仅凭期望风险无法刻画模型面对最坏情况输入时的性能。我们论证了将对抗风险作为目标的做法，尽管它难以精确计算。然后，我们将常用的攻击和评估指标界定为对真实对抗风险的一个可处理的代理目标。这表明，通过优化这一代理目标而非真实对抗风险，模型可能对对手形成「遮蔽」。我们通过把无梯度优化技术改造为对抗攻击来证明这是实践中的一个严重问题：我们用这些攻击将几个近期提出的防御的准确率降至接近零。我们希望我们的表述和结果能帮助研究者开发更强大的防御。

**报告：**

- 下午 05:50 – 06:00 @ A7（口头报告）
- 下午 06:15 – 09:00 @ Hall B #132（海报）

## 7 月 12 日 星期四

[**在重复单阶段多智能体决策问题中用协调图学习协调**](http://proceedings.mlr.press/v80/bargiacchi18a/bargiacchi18a.pdf)（Learning to Coordinate with Coordination Graphs in Repeated Single-Stage Multi-Agent Decision Problems）

**作者：** Eugenio Bargiacchi（布鲁塞尔自由大学）、Timothy Verstraeten（布鲁塞尔自由大学）、Diederik Roijers（布鲁塞尔自由大学 / 阿姆斯特丹自由大学）、Ann Nowé（布鲁塞尔自由大学）、Hado van Hasselt

在许多强化学习问题中，学习多个智能体之间的协调是一个重要问题。学习协调的关键在于利用松耦合——即智能体之间的条件独立性。在本文中，我们研究重复完全合作博弈（多智能体多臂老虎机，MAMABs）中的学习问题，其中期望奖励可以表示为一个协调图。我们提出多智能体上置信探索（MAUCE），一种利用松耦合的 MAMAB 新算法，它使我们能够证明一个遗憾界：该界关于拉臂次数是对数的，且仅关于智能体数量是线性的。我们通过实验将 MAUCE 与稀疏合作 Q 学习以及一种最先进的组合老虎机方法进行比较，表明它在包括风电场控制策略学习在内的多种设定下表现好得多。

**报告：**

- 上午 11:00 – 11:10 @ A3（口头报告）
- 下午 06:15 – 09:00 @ Hall B #126（海报）

### 带延迟、聚合匿名反馈的老虎机（Bandits with Delayed, Aggregated Anonymous Feedback）

**作者：** Ciara Pike-Burke、Shipra Agrawal、Csaba Szepesvari、Steffen Grunewalder

我们研究随机 K 臂老虎机问题的一个变体，称之为「带延迟、聚合匿名反馈的老虎机」。在这个问题中，当玩家拉动一个臂时会生成一个奖励，但不会立即被观察到。相反，在每轮结束时，玩家只观察到恰好在给定轮次到达的若干先前生成奖励的总和。奖励被随机延迟，而且由于观测的聚合性质，哪个臂产生了哪个特定奖励的信息丢失了。问题在于：这种延迟的、聚合的匿名反馈导致的信息损失代价是什么？以往的工作研究了带随机、非匿名延迟的老虎机，发现遗憾只增加一个与期望延迟相关的加性因子。在本文中，我们表明：当期望延迟（或其上界）已知时，这一加性遗憾增加可以在更困难的延迟、聚合匿名反馈设定下得以保持。我们提供了一个算法：当延迟有界时，它恰好匹配非匿名问题的最坏情况遗憾；对于无界延迟，则相差对数因子或一个加性方差项。

**报告：**

- 下午 02:50 – 03:10 @ A5（口头报告）
- 下午 06:15 – 09:00 @ Hall B #123（海报）

### n 人可微博弈的动力学机制（The Mechanics of n-Player Differentiable Games）

**最佳论文亚军（Best Paper Runner Up）**

**作者：** David Balduzzi、Sébastien Racaniere、James Martens、Jakob Foerster、Karl Tuyls、Thore Graepel

支撑深度学习的基石是这样一条保证：对目标函数做梯度下降会收敛到局部极小值。遗憾的是，在存在多个相互作用的损失的场景中——例如生成对抗网络——这一保证失效了。基于梯度的方法在博弈中的行为尚未被很好地理解——而随着对抗性和多目标架构的激增，它正变得越来越重要。在本文中，我们开发了一些新技术来理解和控制一般博弈中的动力学。关键结果是将二阶动力学分解为两个组成部分。第一部分与势博弈（potential games）相关，它可归结为对一个隐式函数的梯度下降；第二部分与哈密顿博弈（Hamiltonian games）相关——这是一类新的博弈，遵守某种守恒律，类似于经典力学系统中的守恒律。这一分解催生了辛梯度调整（Symplectic Adjustment，SGA），一种在一般博弈中寻找稳定不动点的新算法。基础实验表明，SGA 与最近提出的在 GAN 中寻找局部纳什均衡的算法相比具有竞争力——同时它还适用于（并拥有理论保证于）广泛得多的一般博弈。

**报告：**

- 下午 04:00 – 04:20 @ A7（口头报告）
- 下午 06:15 – 09:00 @ Hall B #201（海报）

### LaVAN：局部化且可见的对抗噪声（LaVAN: Localized and Visible Adversarial Noise）

**作者**：Danny Karmon（巴伊兰大学）、Daniel Zoran、Yoav Goldberg（巴伊兰大学）

大多数关于深度学习图像分类器对抗样本的工作所使用的噪声虽然幅度小，却覆盖整幅图像。我们探讨这样一种情形：允许噪声可见，但将其限制在图像的一个小的局部区域，不覆盖图像中的任何主要物体。我们表明，可以生成仅覆盖图像中 2% 像素、且没有任何像素落在主要物体上的局部化对抗噪声；它们可以跨图像、跨位置迁移，并以非常高的成功率成功欺骗最先进的 Inception v3 模型。

**报告：**

- 下午 04:50 – 05:00 @ A7（口头报告）
- 下午 06:15 – 09:00 @ Hall B #116（海报）

### 使用强化对抗学习为图像合成程序（Synthesizing Programs for Images using Reinforced Adversarial Learning）

**作者：** Yaroslav Ganin、Tejas Kulkarni、Igor Babuschkin、S.M. Ali Eslami、Oriol Vinyals

深度生成网络的进展近年来带来了令人瞩目的成果。尽管如此，这类模型常常把容量浪费在数据集的细枝末节上，这大概是由于其解码器的归纳偏置较弱。这正是图形引擎可以派上用场的地方，因为它们抽象掉低层细节，将图像表示为高层程序。目前结合深度学习与渲染器的方法受到以下限制：手工设计的似然或距离函数、需要大量监督，或推理算法难以扩展到更丰富的数据集。为缓解这些问题，我们提出 SPIRAL——一个经过对抗训练的智能体，它生成一个程序，由图形引擎执行以解释和采样图像。该智能体的目标是一个判别器网络——用于区分真实数据与渲染数据——它通过分布式强化学习设置训练，不使用任何监督。一个惊人的发现是：使用判别器的输出作为奖励信号，是让智能体在匹配目标渲染输出方面取得实质性进展的关键。据我们所知，这是首个在具有挑战性的真实世界数据集（MNIST、Omniglot、CelebA）和合成 3D 数据集上演示端到端、无监督、对抗式逆图形智能体的工作。

**报告：**

- 下午 05:00 – 05:20 @ A7（口头报告）
- 下午 06:15 – 09:00 @ Hall B #84（海报）

### 测量神经网络的抽象推理能力（Measuring abstract reasoning in neural networks）

**作者：** David Barrett\*、Felix Hill\*、Adam Santoro\*、Ari Morcos、Tim Lillicrap

神经网络究竟是在学习抽象推理，还是仅仅依赖表层统计特征，这是近期争论的话题。在这里，我们提出了一个旨在探测抽象推理的数据集和挑战，其灵感来自一个著名的人类 IQ 测试。要在这一挑战中取得成功，模型必须应对各种泛化「设定」——训练数据与测试数据以清晰定义的方式存在差异。我们表明，ResNet 等流行模型表现不佳，即便训练集与测试集之间只有极小差异；而我们提出的一种新颖架构——其结构经过专门设计以鼓励推理——表现明显更好。当我们改变测试问题与训练数据相异的方式时，我们发现我们的模型在某些泛化形式上相当擅长，而在另一些形式上则明显薄弱。我们进一步表明，如果训练模型为其答案预测符号化的解释，它的泛化能力会显著提升。总而言之，我们引入并探索了测量与诱导神经网络更强抽象推理能力的多种途径。我们免费提供的数据集应能推动这一方向的进一步进展。

**报告：**

- 下午 05:20 – 05:40 @ K1（口头报告）
- 下午 06:15 – 09:00 @ Hall B #110（海报）

更多内容请见 DeepMind [博客](https://deepmind.com/blog/article/measuring-abstract-reasoning)。


### 基于重要性加权 Actor-Learner 架构的可扩展分布式深度强化学习（Scalable Distributed Deep-RL with Importance Weighted Actor-Learner Architectures）

**作者：** Lasse Espeholt、Hubert Soyer、Remi Munos、Karen Simonyan、Volodymir Mnih、Tom Ward、Yotam Doron、Vlad Firoiu、Tim Harley、Iain Dunning、Shane Legg、Koray Kavukcuoglu

在这项工作中，我们的目标是用一个具有单一参数集的强化学习智能体解决一大批任务。一个关键挑战是处理增加的数据量和延长的训练时间。我们开发了一个新的分布式智能体 IMPALA（Importance Weighted Actor-Learner Architecture），它不仅在单机训练中更高效地利用资源，还能扩展到数千台机器，而不牺牲数据效率或资源利用率。通过将行动与学习解耦并结合一种称为 V-trace 的新颖离策略修正方法，我们实现了高吞吐量下的稳定学习。我们在 DMLab-30（来自 DeepMind Lab 环境的 30 个任务集合（Beattie 等，2016））和 Atari-57（街机学习环境中的全部可用 Atari 游戏（Bellemare 等，2013a））上展示了 IMPALA 在多任务强化学习中的有效性。我们的结果表明，IMPALA 能够用更少的数据取得比以往智能体更好的性能，而且至关重要的是，其多任务方法带来了任务间的正向迁移。

更多内容请见 DeepMind [博客](https://deepmind.com/blog/impala-scalable-distributed-deeprl-dmlab-30/)，并可在 [GitHub](https://github.com/deepmind/scalable_agent) 查看我们的开源实现。

**报告：**

- 上午 09:50 – 10:10 @ A1（口头报告）
- 下午 06:15 – 09:00 @ Hall B #176（海报）

### Mix & Match——面向强化学习的智能体课程（Mix & Match - Agent Curricula for Reinforcement Learning）

**作者：** Wojtek Czarnecki\*、Siddhant Jayakumar\*、Max Jaderberg、Leonard Hasenclever、Yee Whye Teh、Nicolas Heess、Simon Osindero、Razvan Pascanu

我们介绍 Mix & Match（M&M）——一个旨在促进 RL 智能体快速有效学习的训练框架，尤其适用于那些以其他方式训练会太慢或太难处理的智能体。关键创新是一个让我们能够自动构建智能体层面课程的过程。通过这样的课程，我们可以循序渐进地训练更复杂的智能体——实际上是通过从更简单智能体找到的解中进行自举。与典型的课程学习方法不同，我们不是逐渐修改呈现的任务或环境，而是用一个过程逐渐改变策略在内部的表示方式。我们通过在三种不同实验设定中展示显著的性能提升来证明该方法的广泛适用性：（1）我们训练了一个能在具有挑战性的 3D 第一人称任务中控制 700 多个动作的智能体；利用我们的方法推进动作空间课程，我们比传统方法同时获得了更快的训练速度和更好的最终性能。（2）我们进一步表明，M&M 可以成功地用于推进定义智能体内部状态的架构变体课程。（3）最后，我们说明了如何用我们方法的一个变体来提升智能体在多任务设定下的性能。

**报告：**

- 上午 10:10 – 10:20 @ A1（口头报告）
- 下午 06:15 – 09:00 @ Hall B #13（海报）

### Parallel WaveNet：快速高保真语音合成（Parallel WaveNet: fast high-Fidelity Speech Synthesis）

**作者：** Aaron van den Oord、Yazhe Li、Igor Babuschkin、Karen Simonyan、Oriol Vinyals、Koray Kavukcuoglu

近期开发的 WaveNet 架构是逼真语音合成的当前最先进水平，在多种不同语言上一直被评为比以往任何系统都更自然。然而，由于 WaveNet 依赖逐个音频样本的顺序生成，它不太适合当今的大规模并行计算机，因此难以部署到实时生产环境中。本文介绍概率密度蒸馏（Probability Density Distillation），这是一种从训练好的 WaveNet 训练并行前馈网络的新方法，质量上没有显著差异。得到的系统能够以超过实时 20 倍的速度生成高保真语音样本，并已由 Google Assistant 在线上部署，包括提供多种英语和日语语音。

**报告：**

- 下午 04:00 – 04:20 @ A7（口头报告）
- 下午 06:15 – 09:00 @ Hall B #25（海报）

更多内容请见 DeepMind [博客](https://deepmind.com/blog/learning-playing/)。

### 进展与压缩：一个可扩展的持续学习框架（Progress & Compress: A scalable framework for continual learning）

**作者：** Jonathan Schwarz、Jelena Luketina、Wojciech M. Czarnecki、Agnieszka Grabska-Barwinska、Yee Whye Teh、Razvan Pascanu\* Raia Hadsell\*

我们为一个概念上简单且可扩展的持续学习框架做出贡献，适用于按顺序学习任务的领域。我们的方法参数数量恒定，旨在保持对先前遇到任务的性能，同时加速在后续问题上的学习进度。这是通过训练两个神经网络实现的：一个知识库，能够解决先前遇到的问题；以及一个活动列（active column），用于高效学习当前任务。在学完一个新任务后，活动列被蒸馏进知识库，同时注意保护所有先前学到的任务。这一「主动学习（进展）+ 巩固（压缩）」的循环不需要架构增长，不需要访问或存储以往的数据或任务，也没有任务专用参数。因此，这是一个可以伴随任务持续一生的学习过程，同时支持前向迁移并将遗忘降至最低。我们在手写字母的顺序分类以及两个强化学习领域——Atari 游戏和 3D 迷宫导航——上展示了进展与压缩方法。

**报告：**

- 下午 04:00 – 04:20 @ Victoria（口头报告）
- 下午 06:15 – 09:00 @ Hall B #168（海报）

### 面向生成建模的自回归分位数网络（Autoregressive Quantile Networks for Generative Modeling）

**作者：** Georg Ostrovski\*、Will Dabney\*、Remi Munos

我们介绍自回归隐式分位数网络（AIQN），一种与常用方法根本不同的生成建模方法，它使用分位数回归隐式地刻画分布。AIQN 能够取得更优的感知质量和评测指标改进，而不损失样本多样性。该方法可以应用于许多现有模型和架构。在这项工作中，我们用 AIQN 扩展 PixelCNN 模型，并在 CIFAR-10 和 ImageNet 上使用 Inception 分数、FID、非精挑样本和图像修复结果进行演示。我们一致观察到，AIQN 得到一个高度稳定的算法，在保持高度多样化分布的同时提升了感知质量。

**报告：**

- 下午 04:20 – 04:40 @ A7（口头报告）
- 下午 06:15 – 09:00 @ Hall B #110（海报）

### 不确定性贝尔曼方程与探索（The Uncertainty Bellman Equation and Exploration）

**作者：** Brendan O'Donoghue、Ian Osband、Remi Munos、Volodymyr Mnih

我们考虑强化学习中的探索/利用问题。对于利用，众所周知贝尔曼方程将任意时间步的价值与后续时间步的期望价值联系起来。在本文中，我们考虑一个类似的*不确定性*贝尔曼方程（UBE），它将任意时间步的不确定性与后续时间步的期望不确定性联系起来，从而把策略的潜在探索收益扩展到单个时间步之外。我们证明，UBE 的唯一不动点给出由任意策略诱导的 Q 值后验分布方差的一个上界。这一上界可能比传统的基于计数的奖励项紧得多——后者累加的是标准差而非方差。重要的是，与现有的若干乐观方法不同，该方法可以自然地扩展到具有复杂泛化能力的大型系统。将我们基于 UBE 的探索策略替代 ε-贪心策略，使 DQN 在 Atari 套件 57 个游戏中的 51 个上性能得到提升。

**报告：**

- 下午 05:50 – 06:00 @ A1（口头报告）
- 下午 06:15 – 09:00 @ Hall B #14（海报）

### 与稀疏交互工人的众包（Crowdsourcing with Sparsely Interacting Workers）

**作者：** Yao Ma（波士顿大学）、Alexander Olshevsky（波士顿大学）、Csaba Szepesvari、Venkatesh Saligrama（波士顿大学）

我们考虑在对称噪声下的单硬币众包二分类模型中，从工人-任务交互数据（标签未知）估计工人技能的问题。我们定义（工人）交互图：其节点为工人，两节点之间的边表示这两个工人是否参与了同一个任务。我们证明，技能是渐近可辨识的，当且仅当该交互图的一个合适的极限版本是不可约的且含有奇圈。然后，我们在不可约、非周期的交互图上基于观测构造一个加权秩一优化问题来估计技能。我们提出一种梯度下降方案，并证明对于此类交互图，估计值渐近收敛到全局最小值。我们用交互图的符号拉普拉斯矩阵的谱性质刻画了梯度方案的噪声鲁棒性。随后，我们证明基于估计技能的即插即用估计器在多个真实数据集上取得了最先进的性能。我们的结果对秩一矩阵补全问题也有启示：梯度下降可以证明地基于一个含单个奇圈的连通图的 W+1 个非对角观测，恢复 W×W 的秩一矩阵。

**报告：**

- 下午 05:50 – 06:00 @ K11（口头报告）
- 下午 06:15 – 09:00 @ Hall B #77（海报）
