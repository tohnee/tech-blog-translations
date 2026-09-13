---
title: "规格作弊：AI 灵光巧思的另一面"
title_en: "Specification gaming: the flip side of AI ingenuity"
source: https://deepmind.google/blog/specification-gaming-the-flip-side-of-ai-ingenuity/
site: deepmind
date: 2020-04-21
crawled: 2026-09-13
translated: 2026-09-13
---

# 规格作弊：AI 灵光巧思的另一面

> 原文：[Specification gaming: the flip side of AI ingenuity](https://deepmind.google/blog/specification-gaming-the-flip-side-of-ai-ingenuity/) · Google DeepMind

**规格作弊（specification gaming）**是指一种满足目标的字面规格、却没有实现预期结果的行为。我们都有过规格作弊的体验，即便当时并不叫这个名字。读者可能听过[迈达斯国王](https://en.wikipedia.org/wiki/Midas)点物成金的神话：国王要求他碰到的任何东西都变成金子——但很快发现，连食物和饮料在他手中也变成了金属。在现实世界里，当因完成好作业而获得奖励时，学生可能会抄袭另一位同学来得到正确答案，而不是学习知识本身——从而钻了任务规格的空子。

这个问题也出现在人工智能体的设计中。例如，一个强化学习智能体可以找到一条获得大量奖励的捷径，却无需按人类设计者的意图完成任务。这类行为很常见，我们迄今已[收集](http://tinyurl.com/specification-gaming)了大约 60 个例子（汇总了[既有](https://arxiv.org/abs/1803.03453)[清单](https://www.gwern.net/Tanks#alternative-examples)以及 AI 社区持续的[贡献](https://docs.google.com/forms/d/e/1FAIpQLSeQEguZg4JfvpTywgZa3j-1J-4urrnjBVeoAO7JHIH53nrBTA/viewform)）。在这篇博文中，我们回顾规格作弊的可能成因，分享实践中发生这种情况的例子，并主张针对克服规格问题的原则性方法开展进一步研究。

我们来看一个例子。在一个[乐高积木堆叠任务](https://arxiv.org/abs/1704.03073)中，期望的结果是红色方块最终位于蓝色方块的顶部。智能体得到的奖励取决于红色方块底面的高度（以它不接触积木为条件）。智能体没有执行相对困难的操作——拿起红色方块并放到蓝色方块顶上——而是简单地把红色方块翻了个身来拿取奖励。这种行为实现了声明的目标（红色方块底面高度高），却牺牲了设计者真正关心的目标（把它叠在蓝色方块上面）。

![一段动画：一只机械臂旁边有一块蓝色和一块红色乐高积木。机械臂把红色乐高积木翻了个身。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6227555f56f22324228ee43e_Fig201.gif)

来源：Data-Efficient Deep Reinforcement Learning for Dexterous Manipulation (Popov et al, 2017)

我们可以从两个不同的视角看待规格作弊。在开发强化学习（RL）算法的范围内，目标是构建学会达成给定目标的智能体。例如，当我们以 Atari 游戏作为训练 RL 算法的基准时，目标是评估我们的算法能否解决困难的任务。在这种语境下，智能体是否通过钻空子来完成任务并不重要。从这个视角看，规格作弊是一个好迹象——智能体找到了实现既定目标的新颖方式。这些行为展示了算法「精确地按我们说的去做」的灵光巧思与力量。

然而，当我们希望智能体真正去堆叠乐高积木时，同样的巧思就可能成为问题。在构建能在世界中实现预期结果的[对齐智能体](https://medium.com/@deepmindsafetyresearch/scalable-agent-alignment-via-reward-modeling-bf4ab06dfd84)这一更大的范围内，规格作弊是有害的，因为它涉及智能体钻规格的空子而牺牲预期结果。这些行为的根源是对预期任务的规格设定失误，而非 RL 算法本身的缺陷。除了算法设计之外，构建对齐智能体的另一个必要组成部分是奖励设计。

![一张概述「对齐 RL 智能体设计」的示意图：RL 算法设计（目标是得到获得高奖励的智能体，此语境下规格作弊是合理的）与奖励设计（目标是得到捕捉预期结果的奖励函数，此语境下规格作弊是有害的）相结合，共同实现总体目标：实现预期结果的智能体。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6227557e567d38d44320c2d9_Fig202.svg)

设计能准确反映人类设计者意图的任务规格（奖励函数、环境等）往往很困难。即便只是一点轻微的规格设定失误，一个非常好的 RL 算法也可能找到一个与预期解截然不同的复杂解，而一个较差的算法反而找不到这个解，从而给出更接近预期结果的方案。这意味着，随着 RL 算法的改进，正确地设定意图对于实现期望结果会变得越来越重要。因此，研究人员正确设定任务的能力必须跟上智能体寻找新颖解法的能力，这一点至关重要。

我们在广义上使用**任务规格（task specification）**一词，涵盖智能体开发过程的许多方面。在 RL 设定中，任务规格不仅包括奖励设计，还包括训练环境的选择和辅助奖励。任务规格的正确与否，可以决定智能体的巧思是否与预期结果一致。如果规格是对的，智能体的创造力会带来理想的新颖解。正是这一点让 AlphaGo 下出了著名的[第 37 手](https://en.wikipedia.org/wiki/AlphaGo_versus_Lee_Sedol#Game_2)，这一手令人类围棋专家大为惊讶，却是它与李世石第二局对弈中的关键。如果规格是错的，它就可能产生不理想的作弊行为，比如把积木翻个身。这几类解处于一个连续谱上，而我们没有客观的办法把它们区分开来。

![一张「意外解法光谱」图：在规格正确性低的一端是「不理想的新颖解，例如把乐高积木翻身」，在规格正确性高的另一端是「理想的新颖解，例如第 37 手」。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62275591567d38eaa220d9d9_Fig203.svg)

下面我们来考虑规格作弊的一些可能成因。奖励函数设定失误的一个来源是设计不当的**奖励塑形（reward shaping）**。奖励塑形通过在智能体解决任务的路途中给予一些奖励、而不是只奖励最终结果，使某些目标更容易学习。然而，如果塑形奖励不是[基于势函数的](https://people.eecs.berkeley.edu/~pabbeel/cs287-fa09/readings/NgHaradaRussell-shaping-ICML1999.pdf)，它们可能改变最优策略。考虑一个在[Coast Runners 游戏](https://openai.com/blog/faulty-reward-functions/)中控制小船的智能体，其预期目标是尽快完成赛艇比赛。智能体因撞击赛道上的绿色方块而获得塑形奖励，这把最优策略改变成了绕圈行驶、反复撞击同一批绿色方块。

![取自电脑游戏 Coast Runners 的一段画面：一艘小船在码头周围高速绕圈，收集绿色方块和其他障碍物，而不是完成既定赛道。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622755a90ba8e091464f819f_Fig204.gif)

来源：Faulty Reward Functions in the Wild (Amodei & Clark, 2016)

设定一个能准确捕捉**期望最终结果**的奖励本身也可能颇具挑战。在乐高积木堆叠任务中，仅仅规定红色方块底面必须离开地面一定高度是不够的，因为智能体只需把红色方块翻个身就能实现这一目标。对期望结果更全面的规格还应包括：红色方块的顶面必须高于底面，且底面与蓝色方块的顶面对齐。在设定结果时很容易漏掉其中某一条标准，从而使规格过于宽泛、更容易被一个退化的解满足。

与其试图制定一个覆盖所有可能边角情况的规格，我们可以[**从人类反馈中学习奖励函数**](https://deepmind.com/blog/article/learning-through-human-feedback)。评估某个结果是否已经达成，通常比显式地描述它更容易。然而，如果奖励模型没有学到反映设计者偏好的真实奖励函数，这种方法同样可能遭遇规格作弊问题。不准确性的一个可能来源是用于训练奖励模型的人类反馈本身。例如，一个执行[抓取任务](https://openai.com/blog/deep-reinforcement-learning-from-human-preferences/)的智能体学会了把机械手悬停在摄像头与物体之间来糊弄人类评估者。

![一段动画：一只仿真机器手在平台上一个黄色球体附近悬停，一个红色球体漂浮在其上方，展示了智能体摆出一种姿势，诱使人类评估者以为它正在抓取物体。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622755d0be6ea32d75a5ee76_Fig205.gif)

来源：Deep Reinforcement Learning From Human Preferences (Christiano et al, 2017)

学到的奖励模型还可能因为其他原因而设定失准，例如泛化能力差。可以使用额外的反馈来纠正智能体试图利用奖励模型不准确性的一系列尝试。

另一类规格作弊的例子来自智能体对**仿真器缺陷（simulator bugs）**的利用。例如，一个本应学会走路的[仿真机器人](https://www.youtube.com/watch?v=K-wIZuAA3EY&feature=youtu.be&t=486)想出了把自己的腿钩在一起、贴着地面滑行的办法。

![一个由方块组成的简单人形机器人。它从站立状态把双腿折叠成身下的 W 形，然后侧着身子滑过屏幕。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622756926ee3f3940b471081_Fig206.gif)

来源：AI Learns to Walk (Code Bullet, 2019)

乍看之下，这类例子可能显得有趣但不太重要，且与在真实世界部署智能体无关，毕竟真实世界没有仿真器缺陷。然而，其根本问题并不在缺陷本身，而在于一种可被智能体利用的抽象失败。在上面的例子中，机器人的任务之所以被错误设定，是因为对仿真器物理特性的假设不正确。类似地，一个现实世界的交通优化任务也可能被错误设定：错误地假设交通路由基础设施不存在足够聪明的智能体可以发现或利用的软件缺陷或安全漏洞。这类假设不必被明确说出——更可能的情况是，它们只是设计者从未想到的细节。而且，随着任务复杂到无法考虑每一个细节，研究人员在规格设计过程中引入错误假设的可能性也更大。这就提出了一个问题：能否设计出能够纠正此类错误假设、而不是加以利用的智能体架构？

任务规格中一个常见的假设是：任务规格不会受到智能体行为的影响。这对运行在沙箱化仿真器中的智能体成立，但对在真实世界中行动的智能体不成立。任何任务规格都有其物理体现：存储在计算机上的奖励函数，或存储在人类头脑中的偏好。部署在真实世界中的智能体有可能操纵这些目标的表示，从而造成[奖励篡改（reward tampering）](https://medium.com/@deepmindsafetyresearch/designing-agent-incentives-to-avoid-reward-tampering-4380c1bb6cd)问题。对于我们假想的交通优化系统来说，满足用户的偏好（例如提供有用的路线指引）与[影响用户](https://pubsonline.informs.org/doi/10.1287/isre.2013.0497)、使其形成更容易满足的偏好（例如诱导他们选择更容易到达的目的地）之间并没有清晰的界限。前者满足目标，而后者操纵目标在世界中的表示（用户偏好），二者都会给 AI 系统带来高奖励。再举一个更极端的例子，一个非常先进的 AI 系统可以劫持它所运行的计算机，手动把它的奖励信号设为高值。

![一张概述「对齐 RL 智能体设计」的示意图：RL 算法设计（目标是得到获得高奖励的智能体，此语境下规格作弊是合理的）与奖励设计（目标是得到捕捉预期结果的奖励函数）以及避免奖励篡改（目标是消除篡改奖励通道的动机）相结合，共同实现总体目标：实现预期结果的智能体（此语境下规格作弊是有害的）。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622756b504e4a6030cce7d79_Fig207.svg)

总而言之，要解决规格作弊，至少有三个挑战需要克服：

- 我们如何在奖励函数中忠实地捕捉人类对给定任务的概念？
- 我们如何避免在对领域的隐含假设中犯错误，或者设计出纠正错误假设而不是利用它们的智能体？
- 我们如何避免奖励篡改？

尽管从奖励建模到智能体激励设计，已有许多方法被提出，规格作弊仍远未解决。[这份规格作弊行为清单](http://tinyurl.com/specification-gaming)展示了问题的规模，以及智能体钻目标规格空子的方式之多。随着 AI 系统在「以牺牲预期结果为代价满足任务规格」方面变得愈发能干，这些问题在未来很可能变得更具挑战性。随着我们构建更先进的智能体，我们将需要专门针对克服规格问题而设立的设计原则，确保这些智能体稳健地追求设计者期望的结果。

![一组动画剪辑拼贴，展示规格作弊的若干示例。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6227571a4fecbb9610562856_Fig208.gif)

**说明**

感谢 Hado van Hasselt 和 Csaba Szepesvari 对本文的反馈。

定制图表由 Paulo Estriga、Aleks Polozuns 和 Adam Cain 制作。
