---
title: "AI 与神经科学：一场良性循环"
title_en: "AI and Neuroscience: A virtuous circle"
source: https://deepmind.google/blog/ai-and-neuroscience-a-virtuous-circle/
site: deepmind
date: 2017-08-02
crawled: 2026-09-13
translated: 2026-09-13
---

# AI 与神经科学：一场良性循环

> 原文：[AI and Neuroscience: A virtuous circle](https://deepmind.google/blog/ai-and-neuroscience-a-virtuous-circle/) · Google DeepMind

近来 AI 的进展令人瞩目。人工系统如今已在[雅达利电子游戏](https://deepmind.com/research/publications/human-level-control-through-deep-reinforcement-learning/)、[古老的围棋](https://deepmind.com/research/case-studies/alphago-the-story-so-far)以及[单挑扑克的高 stakes 对局](http://science.sciencemag.org/content/356/6337/508)中超越人类专家。它们还能产出与人类难以区分的[手写字迹](https://web.mit.edu/cocosci/Papers/Science-2015-Lake-1332-8.pdf)与[语音](https://deepmind.com/blog/article/wavenet-generative-model-raw-audio)，在多种语言之间互译，甚至能把你的度假照片重新渲染成[梵高](https://deepart.io/)名画的风格。

这些进步归功于多个因素，包括新统计方法的应用以及计算机处理能力的提升。但在[《神经元》（Neuron）杂志近期发表的一篇 Perspective](https://www.cell.com/neuron/fulltext/S0896-6273(17)30509-3) 中，我们认为，一个常被忽视的贡献是：来自实验神经科学与理论神经科学的思想的运用。

心理学与神经科学在 AI 的历史中扮演过关键角色。[Donald Hebb](https://en.wikipedia.org/wiki/Donald_O._Hebb)、[Warren McCulloch](https://en.wikipedia.org/wiki/Warren_Sturgis_McCulloch)、[Marvin Minsky](https://en.wikipedia.org/wiki/Marvin_Minsky) 和 [Geoff Hinton](https://en.wikipedia.org/wiki/Geoffrey_Hinton) 等奠基人物，最初都是出于理解大脑如何工作的愿望而投入这一领域。事实上，整个 20 世纪晚期，神经网络发展中的许多关键工作并非在数学或物理实验室完成，而是在心理学与神经生理学系完成的。

> 利害如此之重，神经科学与 AI 这两个领域走到一起的需要，如今比以往任何时候都更加迫切。

在 DeepMind，我们认为，尽管两个领域都在快速进步，研究者们不应忘记这一愿景。我们呼吁神经科学与 AI 的研究者找到一种共同语言，让知识得以自由流动，从而使两线工作能够持续推进。

我们认为，在 AI 研究中从神经科学汲取灵感之所以重要，有两个原因。第一，神经科学可以帮助验证已有的 AI 技术。简而言之，如果我们发现自己某个人工算法模拟了大脑中的某种功能，这暗示我们的方法可能走在正确的方向上。第二，神经科学可以为构建人工大脑时采用的新型算法与架构提供丰富的灵感来源。传统 AI 方法历来由基于逻辑的方法和理论数学模型主导。我们认为，神经科学可以通过识别那些可能对认知功能至关重要的生物计算类别，来补充这些方法。

以神经科学近期一项开创性发现为例：对离线经验「重放」（replay）的发现。在睡眠或安静休息期间，生物大脑会「重放」此前活跃时段产生的神经元活动的时间模式。例如，大鼠在迷宫中奔跑时，「位置」细胞会随着动物移动而被激活。在休息时，可以观察到同样的神经元活动序列，仿佛大鼠在脑海中重新想象自己过去的移动，并利用它们来优化未来的行为。事实上，已有研究表明，干扰重放会损害它们随后完成相同任务的表现。

![抽象的复古电子游戏精灵与方块，以发光的 3D 轮廓形式漂浮在数字网格之上。](https://lh3.googleusercontent.com/XRaO1hKI_b8279Tiv59-FHGq_dNESFSL51Zu3l6x4By_LmupaIAgaAE0z14Nv_sh66q1eQM8z2_xFyx5Z85_P0B5ZbW5W8wH6ke8lEs4anX8AzUMvZg=w1440)

「重放」是 DQN 的关键组成部分。DQN 是一个通用智能体，能够不断调整自身行为以适应新环境

乍看之下，构建一个需要「睡觉」的人工智能体似乎有违直觉——毕竟，人们本指望它们能在程序员上床睡觉之后，还在为某个计算问题埋头苦干。但这一原则是我们[深度 Q 网络（DQN）](https://deepmind.com/research/publications/human-level-control-through-deep-reinforcement-learning/)的关键部分。DQN 是一种算法，仅以原始像素和得分为输入，就学会了以超人类水平驾驭风格各异的多种 Atari 2600 游戏。DQN 模拟「经验重放」：存储一部分训练数据并「离线」回顾，使它能够从过去发生的成功或失败中重新学习。

这样的成功让我们有信心相信，神经科学已经是 AI 思想的一个重要来源。但展望未来，我们认为它在帮助我们攻克尚未解决的问题——例如高效学习、对物理世界的理解以及想象——方面将变得不可或缺。

[想象](https://www.ncbi.nlm.nih.gov/pubmed/19528007)对人类和动物而言是一项极其重要的功能，它使我们不必实际采取行动就能为未来情境做规划；而实际行动可能是要付出代价的。考虑一个简单的例子，比如规划一次度假。为此，我们调动自己对世界的知识（或者说「模型」），用它向前投射时间，评估未来的状态，从而计算出需要走的路线，或者为晴天该打包哪些衣物。人类神经科学的前沿研究正开始揭示支撑这类思维的计算与系统机制，但这些新认识中还有许多尚未被纳入人工模型。

![一幅插图：一棵形似人脑的树，左半边由数字像素和电路构成，右半边由有机的树枝和绿叶构成，象征人工智能与神经科学之间的联系。](https://lh3.googleusercontent.com/wtrBw4LC9a7fk2XgAoX0GZ5-YVljIOjfMEx0i_5YuuXLcyQZZ2FetVzwpemxKYARg3Vh2YDpni3UXEOvdcg7rP_100GxWvTFOFzmrzZMicIAi67hmg=w1440)

神经科学与人工智能这两个领域有着漫长而交织的历史

当代 AI 研究的另一个关键挑战被称为迁移学习（transfer learning）。为了有效应对新情况，人工智能体需要具备在已有知识之上构建、进而做出明智决策的能力。人类早已擅长此事——一个会开车、会用笔记本电脑、会主持会议的人，即使面对不熟悉的车辆、操作系统或社交场合，通常也能应付自如。

研究者们如今已开始迈出第一步，去理解这在人工系统中如何成为可能。例如，一类被称为「渐进网络」（progressive network）的新型网络架构，可以把在一个电子游戏中学到的知识用于学习另一个游戏。同一架构还被证明能把知识从仿真机械臂迁移到真实世界的机械臂上，大幅缩短训练时间。耐人寻味的是，这些网络与[人类顺序任务学习的模型](http://science.sciencemag.org/content/344/6191/1481.long)存在某些相似之处。这些引人遐想的联系表明，未来 AI 研究有着向神经科学工作取经的巨大机会。

但这种知识交换不能是单行道。神经科学也能从 AI 研究中受益。以强化学习为例——它是当代 AI 研究的核心方法之一。虽然最初的想法来自心理学中的动物学习理论，但它是由机器学习研究者发展和精细化的。这些后来的思想又反馈回神经科学，帮助我们理解神经生理学现象，例如哺乳动物基底神经节中[多巴胺神经元的放电特性](http://science.sciencemag.org/content/275/5306/1593.long)。

这种往复交流至关重要，唯有如此，两个领域才能不断建立在彼此的洞见之上，形成一种良性循环：AI 研究者借助来自神经科学的思想构建新技术，神经科学家则通过观察人工智能体的行为来更好地解读生物大脑。事实上，得益于光遗传学等近期进展——它们使我们能够精确测量和操控大脑活动，产生可用机器学习工具分析的海量数据——这一循环很可能进一步加速。

因此我们相信，把智能提炼成算法，并将它们与人类大脑进行比较，如今已至关重要。这不仅能助力我们开发 AI 的征程——我们希望这一工具能够[创造新知识、推动科学发现](https://www.ft.com/content/048f418c-2487-11e7-a34a-538b4cb30025)——还可能让我们更好地理解自己头脑中正在发生什么。这或许能照亮神经科学中一些最持久的谜团，例如创造力的本质、梦，甚至有朝一日，意识本身。利害如此之重，神经科学与 AI 这两个领域走到一起的需要，如今比以往任何时候都更加迫切。

**附注**

阅读论文：[Neuroscience-Inspired Artificial Intelligence](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/ai-and-neuroscience-a-virtuous-circle/Neuron.pdf)
