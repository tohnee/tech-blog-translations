---
title: "Capture the Flag（夺旗）：复杂合作智能体的涌现"
title_en: "Capture the Flag: the emergence of complex cooperative agents"
source: https://deepmind.google/blog/capture-the-flag-the-emergence-of-complex-cooperative-agents/
site: deepmind
date: 2019-05-30
crawled: 2026-09-13
translated: 2026-09-13
---

# Capture the Flag（夺旗）：复杂合作智能体的涌现

> 原文：[Capture the Flag: the emergence of complex cooperative agents](https://deepmind.google/blog/capture-the-flag-the-emergence-of-complex-cooperative-agents/) · Google DeepMind

驾驭多人电子游戏所涉及的策略、战术理解与团队配合，是 AI 研究面临的一项关键挑战。

在我们最新的、[现已发表于《科学》（Science）杂志的论文](http://science.sciencemag.org/cgi/content/full/364/6443/859?ijkey=rZC5DWj2KbwNk&keytype=ref&siteid=sci)中，我们展示了强化学习方面的新进展，使智能体在 Quake III Arena 的 Capture the Flag（夺旗）模式中达到了人类水平的表现。这是一个复杂的多智能体环境，也是经典的 3D 第一人称多人游戏之一。这些智能体既能与人造队友成功合作，也能与人类队友成功合作，即便在以与人类玩家相当的反应时间进行训练时，依然展现出卓越性能。此外，我们还展示了这些方法如何成功超越研究用 Capture the Flag 环境，扩展到完整的 Quake III Arena 游戏。

![并排的第一人称视角游戏画面，展示修改版 Quake III Arena Capture the Flag 中的两个不同程序生成环境：左侧是方块状的城市建筑，右侧是带有树木与仙人掌的沙漠景观。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622724d86793159dd36203c6_CTF2001.gif)

智能体玩 Capture the Flag 的画面，以红队某名玩家的第一人称视角呈现，左为室内环境，右为室外环境。

![并排的第一人称视角游戏画面，展示修改版 Quake III Arena Capture the Flag 中的两个不同程序生成环境：左侧是方块状的城市建筑，右侧是一座砖砌城堡。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62272519604e646b14f736d4_CTF2002.gif)

智能体在完整比赛地图上玩另外两种 Quake III Arena 多人游戏模式：Future Crossings 地图上的 Harvester（左）与 Ironwood 地图上的 One Flag Capture the Flag（右），具备完整游戏中的全部道具与装备。

数十亿人居住在这个星球上，每个人都有各自的目标与行动，却仍能通过团队、组织与社会凝聚在一起，展现出令人惊叹的集体智慧。这就是我们所说的多智能体学习场景：许多独立的智能体必须各自独立行动，却要学会与其他智能体互动与合作。这是一个极其困难的问题——因为当各个智能体共同适应时，世界在不断变化。

为了研究这一问题，我们把目光投向 3D 第一人称多人电子游戏。这类游戏是最流行的游戏类型，凭借其沉浸式的玩法，以及它在策略、战术、手眼协调和团队配合上提出的挑战，吸引了数百万游戏玩家。我们的智能体面临的挑战是直接从原始像素中学习并产生动作。这种复杂性使第一人称多人游戏成为 AI 社区内一个成果丰硕且活跃的研究领域。

我们在这项工作中聚焦的游戏是 Quake III Arena（我们对它做了视觉风格上的修改，但所有游戏机制保持不变）。Quake III Arena 奠定了许多现代第一人称游戏的基础，并长期拥有一个竞争激烈的电竞圈子。我们训练的智能体以个体的身份学习和行动，但必须能够与任何其他智能体——无论是人造的还是人类的——组队并肩作战，或与之对抗。

CTF 的规则很简单，但动态却很复杂。两支由单个玩家组成的队伍在给定地图上竞技，目标是夺取对方队伍的旗帜，同时保护自己的旗帜。为了取得战术优势，他们可以标记（tag）对方队员，把对方送回出生点。五分钟后夺旗次数最多的一方获胜。

从多智能体的角度看，CTF 要求玩家既与队友成功合作，又与对方队伍竞争，同时对可能遇到的任何打法都保持稳健。

为了让事情更有意思，我们考虑了 CTF 的一个变体：地图布局在每场比赛之间都会变化。这样一来，我们的智能体被迫掌握一般性策略，而不是死记地图布局。此外，为了公平起见，我们的学习智能体以与人类相似的方式体验 CTF 世界：它们观察像素图像流，并通过模拟的游戏手柄发出动作。

我们的智能体必须从零开始学习如何在未见过的环境中观察、行动、合作与竞争，而学习信号只有每场比赛一个：它们的队伍是否获胜。这是一个富有挑战的学习问题，其解决方案基于三个关于强化学习的一般性思想：

- 我们不是训练单个智能体，而是**训练一个智能体种群**，它们通过相互博弈来学习，从而提供多样的队友与对手。
- 种群中的每个智能体**学习自己的内部奖励信号**，使智能体能够生成自己的内部目标，比如夺取一面旗帜。一个**双层优化过程**直接以获胜为目标优化智能体的内部奖励，并在内部奖励上使用强化学习来学习智能体的策略。
- 智能体**在快慢两个时间尺度上运行**，这提升了它们利用记忆并生成连贯动作序列的能力。

![FTW 智能体的架构图，展示游戏观测、得分与获胜信号如何输入快慢两个循环神经网络，以优化内部奖励、策略与动作。](https://lh3.googleusercontent.com/5PHNViS_pfp2_Hi4IknNq1CXEVZZVM9GUqLWBwK7Eghos_rROM9YOPnPGl6biUFFmsV1ZyeuEHmSth-3m1Sp6FSNqBwHCK5WKfLR9wCMV6-hguVX=w1440)

For The Win（FTW）智能体架构示意图。该智能体结合了快慢两个时间尺度上的循环神经网络（RNN），包含一个共享记忆模块，并学习从游戏得分到内部奖励的转换。

由此得到的智能体被称为 For The Win（FTW）智能体，它学会以极高的水准玩 CTF。关键在于，学习到的智能体策略对地图大小、队友数量以及队内其他玩家都具有稳健性。在下文中，你可以观看 FTW 智能体在室外程序生成环境中相互对抗的一些比赛，以及人类与智能体在室内程序生成环境中并肩作战的比赛。

我们举办了一场锦标赛，有 40 名人类玩家参加，人类与智能体在比赛中随机配对——既作为对手，也作为队友。

![若干人类玩家坐在配有电脑显示器的桌前玩多人电子游戏。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6227269607daf72e1b316f54_CTF2004.gif)

一场早期测试锦标赛：人类与训练好的智能体及其他人类在 CTF 中合作与对抗。

FTW 智能体学会后变得远强于强大的基线方法，并超过了人类玩家的胜率。事实上，在参与者的一项调查中，它们被评为比人类参与者更具合作性。

![折线图，展示 45 万局训练对局中智能体 Elo 等级分的变化。FTW 智能体（蓝色线）稳步上升，在约 10 万局时超过普通人类基线，在约 18 万局时超过强人类基线，达到接近 1600 的 Elo。Self-play + RS 智能体（红色线）峰值低于强人类水平，而 Self-play 智能体（深灰色线）一直徘徊在 500 Elo 的随机智能体基线附近。](https://lh3.googleusercontent.com/qlB3GyTaGuLxfVhFICNcr8MwIB6fyOCgodqYFShtiu2A4u0RatfTLI6KAKfYHUh1AeXjViRcRecwF2boCzTX8NdgJ3BJb9P7ao9LHICD8CPGYNYP9ZQ=w1440)

我们的智能体在训练期间的表现。我们的新智能体——FTW 智能体——获得了远高于人类玩家以及 Self-play + RS 与 Self-play 基线方法的 Elo 等级分（该分数对应获胜概率）。

超越单纯的性能评估，理解这些智能体的行为与内部表示中涌现出的复杂性同样重要。

为了理解智能体如何表示游戏状态，我们把智能体神经网络的激活模式绘制在一个平面上。下图中的点代表游戏过程中的各种情境，相邻的点代表相似的激活模式。这些点按照智能体所处的高级 CTF 游戏状态着色：智能体在哪个房间？旗帜处于什么状态？能看到哪些队友与对手？我们观察到相同颜色的点聚集成簇，表明智能体以相似的方式表示相似的高级游戏状态。

![智能体神经表示的示意图，展示单个神经元的选择性（例如针对「本方旗帜被夺」或「智能体正在重生」）如何映射到基本的夺旗情境，这些情境再组合成整体智能体状态的大规模 t-SNE 嵌入中按颜色区分的簇。](https://lh3.googleusercontent.com/zVf8uFhVFoqtxF4TliLjQj3uw0pTOrGAuDraseBOx0ITJK0Uq6xVW5SG109ZglCHksD7O3e9RfLeRyvtI7fbab8QH2t0jgOfQdBTYgzLcgMixWpm=w1440)

一窥我们的智能体如何表示游戏世界。在上图中，某一时刻的神经激活模式按照彼此的相似程度被绘制出来：两个点在空间中越接近，它们的激活模式越相似。随后这些点按当时的游戏局势着色——颜色相同，局势相同。我们看到这些神经激活模式是有组织的，并形成了颜色的簇，表明智能体以一种定型、有条理的方式表示游戏玩法中有意义的方面。训练出的智能体甚至表现出一些人造神经元，直接对特定局势编码。

我们从未告诉智能体任何游戏规则，它们却学到了基本的游戏概念，并有效培养出对 CTF 的直觉。事实上，我们能找到直接对某些最重要的游戏状态编码的特定神经元，例如在智能体自己的旗帜被夺时激活的神经元，或在智能体的队友持有旗帜时激活的神经元。论文提供了进一步的分析，涵盖智能体对记忆与视觉注意力的使用。

## 与人类相当的智能体

我们的智能体为何表现如此出色？首先，我们注意到这些智能体的反应时间极快，标记（tagging）动作也非常精准，这或许可以解释它们的表现（标记是一种把对手送回起点的战术动作）。由于生物信号传导较慢，人类处理感官输入并做出行动相对较慢。[这里有一个反应时间测试，你可以亲自试试](https://faculty.washington.edu/chudler/java/redgreen.html)。因此，我们智能体的卓越表现可能是其更快的视觉处理与运动控制的结果。然而，通过人为降低这种精准度与反应时间，我们发现这只是它们成功的因素之一。在进一步的研究中，我们训练了内置四分之一秒（267 毫秒）延迟的智能体——也就是说，这些智能体在观察世界之前有 267 毫秒的滞后——这与已报道的人类电子游戏玩家反应时间相当。这些响应延迟的智能体仍然胜过人类参与者，强人类玩家获胜的概率只有 21%。

![一张数据表和柱状图，展示带 267 毫秒响应延迟的智能体的结果。上方表格显示人类对抗这些延迟智能体的胜率：可利用性测试者为 30%，强人类玩家为 21%，中等水平人类玩家为 12%。下方的柱状图比较普通人类、强人类、延迟智能体队友与延迟智能体对手的平均游戏事件数——夺旗、拾旗、救旗以及标记对手——显示延迟智能体执行的夺旗相关动作始终多于人类玩家。](https://lh3.googleusercontent.com/46bqyRgJjBFhp44RnTHdcl9H728CDe-KAOkezbZzF_uXyDfmZq2QnIZxUjmyy5QVu2fJsCNcDloBkB_tMeHVJb9sEcHbr5yC-t91FDGqB_jlc63TAQ=w1440)

人类玩家对响应延迟智能体的胜率很低，表明即便拥有与人类相当的反应延迟，智能体仍然胜过人类玩家。此外，观察人类与响应延迟智能体的平均游戏事件数，可以看到标记事件的数量相当，说明这些智能体在这一方面并不具备对人类的优势。

通过无监督学习，我们确立了智能体与人类的原型行为，从而发现智能体实际上学到了类似人类的行为，例如跟随队友以及在对方基地里蹲守（camping）。

![三种自动发现的行为：本方基地防守、对方基地蹲守与队友跟随。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622726eac975f27c5d7cd03c_CTF2008.gif)

训练出的智能体表现出的自动发现行为的三个例子。

这些行为在训练过程中通过强化学习与种群层面的演化而涌现，某些行为——例如队友跟随——会随着智能体学会以更互补的方式合作而逐渐被弃用。

FTW 智能体种群的训练进程。左上：30 个智能体在训练中相互演化时各自的 Elo 等级分。右上：这些演化事件的谱系树。下方的图表展示了知识的演进、部分内部奖励以及行为概率在智能体训练全程中的变化。

## 更进一步

虽然本文聚焦于 Capture the Flag，但研究贡献是普适的，我们很期待看到其他研究者在不同的复杂环境中如何在我们技术的基础上继续构建。自首次发表这些结果以来，我们已成功将这些方法扩展到完整的 Quake III Arena 游戏，其中包括职业比赛用地图、除 Capture the Flag 之外的更多多人游戏模式，以及更多装备与道具。初步结果表明，智能体可以在多种游戏模式和多张地图上进行有竞争力的对局，并开始在测试赛中挑战我们人类研究者的技巧。事实上，这项工作中引入的思想——例如基于种群的多智能体强化学习——构成了[我们在 StarCraft II 工作中 AlphaStar 智能体](https://deepmind.com/blog/alphastar-mastering-real-time-strategy-game-starcraft-ii/)的基石。

总的来说，这项工作凸显了多智能体训练在推动人工智能发展方面的潜力：利用多智能体训练提供的天然课程，并促使智能体发展出足够的稳健性——甚至能够与人类组队。

**注释**

更多细节，请参阅[论文](http://science.sciencemag.org/cgi/content/full/364/6443/859?ijkey=rZC5DWj2KbwNk&keytype=ref&siteid=sci)（[PDF](https://science.sciencemag.org/content/sci/364/6443/859.full.pdf?ijkey=rZC5DWj2KbwNk&keytype=ref&siteid=sci)）与[完整补充视频](https://youtu.be/dltN4MxV1RI)。

这项工作由 Max Jaderberg、Wojciech M. Czarnecki、Iain Dunning、Luke Marris、Brendan Tracey、Guy Lever、Antonio Garcia Castaneda、Charles Beattie、Neil Rabinowitz、Ari Morcos、Avraham Ruderman、Nicolas Sonnerat、Tim Green、Louise Deason、Joel Z. Leibo、David Silver、Demis Hassabis、Koray Kavukcuoglu 与 Thore Graepel 完成。

可视化由 Adam Cain、Damien Boudot、Doug Fritz、Jaume Sanchez Elias、Paul Lewis、Max Jaderberg、Wojciech M. Czarnecki 与 Luke Marris 制作。

我们感谢 Patrick Howard 与 Dan “Scancode” Gold 允许我们使用他们设计的 Quake III Arena 地图。

更新于 2019 年 5 月 30 日。请阅读下方「与人类相当的智能体」与「更进一步」两节中关于我们新工作的介绍。
