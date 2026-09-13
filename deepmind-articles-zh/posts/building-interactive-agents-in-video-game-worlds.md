---
title: "在电子游戏世界中构建交互式智能体"
title_en: "Building interactive agents in video game worlds"
source: https://deepmind.google/blog/building-interactive-agents-in-video-game-worlds/
site: deepmind
date: 2022-11-23
crawled: 2026-09-13
translated: 2026-09-13
---

# 在电子游戏世界中构建交互式智能体

> 原文：[Building interactive agents in video game worlds](https://deepmind.google/blog/building-interactive-agents-in-video-game-worlds/) · Google DeepMind

介绍一个用于创建 AI 智能体的框架，这些智能体能够在开放式环境中理解人类指令并执行动作

人类行为极其复杂。即便是"[把球放在盒子旁边](https://youtu.be/fKb7ONh0l3s)"这样一个简单的请求，也需要对情境化意图与语言有深入的理解。"旁边"这样一个词的含义很难界定——把球放进盒子里在字面上或许距离最近，但说话者的意思很可能是把球放在盒子边上。要正确响应这一请求，人必须能够理解并判断当前情境与周边语境。

如今大多数人工智能（AI）研究者都认为，编写能够捕捉情境化交互细微差别的计算机代码是不可能的。因此，现代机器学习（ML）研究者转而专注于从数据中学习这类交互。为了探索这些基于学习的方法，并快速构建能在开放式条件下理解人类指令、安全执行动作的智能体，我们在一个电子游戏环境中创建了一个研究框架。

今天，我们[发表一篇论文](https://arxiv.org/abs/2211.11602)和[一组视频](https://www.youtube.com/playlist?list=PLJ1sthn_UneUQ2avq5yCVszcbmcmbege6)，展示我们在构建能够理解模糊人类概念的电子游戏 AI 方面迈出的早期步伐——也因此，这类 AI 可以开始以人类自己的方式与人互动。

近来训练电子游戏 AI 的许多进展都依赖于优化游戏得分。[星际争霸](https://www.deepmind.com/publications/alphastar-grandmaster-level-in-starcraft-ii-using-multi-agent-reinforcement-learning)和 [Dota](https://openai.com/five/) 的强大 AI 智能体，都是用计算机代码算出的明确胜负来训练的。我们则不优化游戏得分，而是请人来发明任务并亲自评判进展。

利用这一方法，我们开发出一种研究范式，让我们能够通过与人类有锚定（grounding）的开放式交互来改进智能体行为。虽然这一范式仍处于起步阶段，但它创造出的智能体能够实时地倾听、交谈、提问、导航、搜索与取物、操纵物体，并执行许多其他活动。

这段合辑展示了智能体执行人类参与者所提出任务的行为：

![一幅三联图，展示一个虚拟"游戏小屋"，内有数百种可辨认的物体和随机化的布局。](https://lh3.googleusercontent.com/wsBynD1qat8y7M8d_PV5wWfuJHQ8edn4e3U0TFizOoy7AdhPH4O8vPTmtDOzA8uqEqsmuFNW5URlzmvdj_rz0Eec73JvtkSKbXdGTPvpbWBH2exnAvc=w1440)

我们创建了一个虚拟"游戏小屋"（playhouse），其中有数百种可辨认的物体和随机化的布局。这一界面为简单而安全的研究而设计，包含一个用于无约束沟通的聊天功能。

## 在"游戏小屋"中学习

我们的框架始于人与人在电子游戏世界中的交互。通过模仿学习，我们为智能体注入了一组宽泛但未经打磨的行为。这一"行为先验"（behaviour prior）对于实现可供人类评判的交互至关重要。没有这个初始模仿阶段，智能体的行为完全是随机的，几乎无法与之交互。随后由人类对智能体行为做出进一步评判，并通过强化学习（RL）对这些评判进行优化，便可产生更好的智能体，而后者还能继续被改进。

![一幅由彩色箭头组成的环形图，展示智能体是如何被构建和改进的。](https://lh3.googleusercontent.com/z08PJk5rLkN6Svzw6aRAdQLIqtNScBDpZ79T1EtaKD1CY4mXBo-bjldi_Odu1smr4GQA7_ibkZUOlab82jLWsnElnz8z6K2DzDU-f9CO_FsFx5TZ=w1440)

我们通过以下方式构建智能体：（1）模仿人与人之间的交互，然后经由（2）人机交互与人类反馈、（3）奖励模型训练和（4）强化学习构成的循环不断改进。

首先，我们基于儿童"游戏小屋"的概念构建了一个简单的电子游戏世界。这一环境为人与智能体的交互提供了安全场所，也便于快速收集大量此类交互数据。小屋里有各式各样的房间、家具和物品，每次交互都会以新的方式布置。我们还创建了一个交互界面。

人类与智能体在游戏中各有一个化身（avatar），使它们能够在环境中移动并进行操作。它们还可以实时聊天，并协作完成各种活动，例如搬运物体并相互递送、搭建积木塔，或一起打扫房间。人类参与者通过在世界中走动、设定目标以及向智能体提问来为交互设定情境。整个项目共收集了超过 25 年的实时交互数据，来自数百名（人类）参与者。

## 观察涌现的行为

我们训练的智能体能够完成极为多样的任务，其中一些连构建它们的研究者都未曾预料。例如，我们发现这些智能体能用两种交替的颜色把物体排成一排，或者从屋子里取出一件与用户手中物体相似的物品。

这些惊喜之所以涌现，是因为语言允许通过简单语义的组合产生近乎无穷的任务与问题。此外，作为研究者，我们并不具体规定智能体行为的细节。相反，是在这些交互过程中，数百名参与交互的人类自己想出了任务和问题。

## 构建创建这些智能体的框架

为创建我们的 AI 智能体，我们采用了三个步骤。我们首先训练智能体模仿简单人际交互的基本要素——即一个人请另一个人做某事或回答问题。我们把这一阶段称为创建行为先验，它使智能体能够高频地与人类进行有意义的交互。没有这一模仿阶段，智能体只会随机移动、胡言乱语，几乎不可能以任何合理的方式与之交互，给它们提供反馈就更加困难。这一阶段在我们的两篇早期论文中已有涉及：[Imitating Interactive Intelligence](https://arxiv.org/abs/2012.05672) 与 [Creating Multimodal Interactive Agents with Imitation and Self-Supervised Learning](https://arxiv.org/abs/2112.03763)，二者探索了构建基于模仿的智能体。

## 超越模仿学习

虽然模仿学习带来了有趣的交互，但它把每个交互时刻都视为同等重要。要学习高效、目标导向的行为，智能体需要追求一个目标，并在关键时刻掌握特定的动作与决策。例如，基于模仿的智能体不会可靠地抄近路，也不会比普通人类玩家更灵巧地执行任务。

这里我们展示一个基于模仿学习的智能体和一个基于强化学习的智能体执行同一条人类指令的情形：

为了赋予我们的智能体一种目标感、超越模仿所能达到的高度，我们依靠强化学习——它将试错与性能度量相结合，实现迭代改进。当我们的智能体尝试不同动作时，能提升性能的动作会被强化，降低性能的动作则会被惩罚。

在 Atari、Dota、围棋和星际争霸这类游戏中，分数就是有待提升的性能度量。而我们不用分数，而是请人来评估情境并提供反馈，帮助我们的智能体学习一个奖励模型。

## 训练奖励模型并优化智能体

为了训练奖励模型，我们请人类判断他们是否观察到显示当前指令目标取得显著进展的事件，或显著的差错与失误。然后我们在这些正面与负面事件和正面与负面偏好之间建立对应关系。由于这些事件跨越时间发生，我们把这类评判称为"跨时的"（inter-temporal）。我们训练了一个神经网络来预测这些人类偏好，由此得到一个反映人类反馈的奖励（或效用/评分）模型。

用人类偏好训练出奖励模型后，我们用它来优化智能体。我们把智能体放进模拟器，指示它们回答问题、遵循指令。当它们在环境中行动和说话时，我们训练好的奖励模型会给它们的行为打分，我们再用一个强化学习算法来优化智能体的表现。

那么，任务指令和问题从哪里来？我们探索了两种途径。第一，我们复用人类数据集中提出的任务和问题。第二，我们训练智能体模仿人类布置任务和提问的方式，如下方视频所示——两个智能体相互交互，其中一个（蓝色）经过训练、会模仿人类布置任务和提问，另一个（黄色）则受训遵循指令并回答问题：

## 评估与迭代，持续改进智能体

我们使用了多种相互独立的机制来评估智能体，从人工编写的测试，到我们在先前工作 [Evaluating Multimodal Interactive Agents](https://www.deepmind.com/publications/evaluating-multimodal-interactive-agents) 中开发的一种新机制——由人类对人们创建的开放式任务进行离线打分。重要的是，我们请人们与我们的智能体实时交互并评判它们的表现。经强化学习训练的智能体，其表现远好于仅用模仿学习训练的智能体。

![一张柱状图，对比人类、行为克隆加强化学习（BC + RL）以及仅行为克隆（BC）的任务成功率。在"总体"（Overall）、"遵循指令"（Instruction-following）和"问答"（Question-answering）类别中，人类表现最高，其次是 BC + RL，它明显优于单独的 BC。](https://lh3.googleusercontent.com/-M6m1S9uUOnegrQrKxXQNkh-FNdSGcxL2TrXjmtMxTspPdebBgIjQyWhXQORBOBkOTwDFydV19FIdEBG76CC7mxbbjp7ftQ4ODBzUMldemP0G0cBSy8=w1440)

我们请人们在实时在线交互中评估我们的智能体。人类在 5 分钟内给出指令或提问，并评判智能体的成功与否。通过使用强化学习，我们的智能体获得了比仅用模仿学习更高的成功率，在类似条件下达到了人类表现的 92%。

最后，最近的实验表明，我们可以迭代这一强化学习过程来反复改进智能体行为。当智能体经由强化学习训练完成后，我们请人们与这个新智能体交互、标注其行为、更新我们的奖励模型，然后再进行新一轮强化学习。这一方法的结果是能力越来越强的智能体。对于某些类型的复杂指令，我们甚至能创造出平均表现超过人类玩家的智能体。

![一张标题为"搭建高塔"（Build towers）的柱状图，纵轴为 0.0 到 1.0 的成功率。各列对比四个类别：人类（HUMAN，0.61）、BC+RL 第二轮（BC+RL ROUND 2，0.72）、BC+RL 第一轮（BC+RL ROUND 1，0.57）以及 BC（0.28），表明第二轮强化学习产生了最高的成功率。](https://lh3.googleusercontent.com/1-XD3M4ph1mtQAkVPOFFe0N_qXpo7uCUIaL9HzzTvZHLgF3mW9Em1AHhrimwNXtQlHFWK87M9skMb5CoqB25-DtOKKOlUJw0OK6X7bTFxd7QK1B-=w1440)

我们在搭建高塔这个问题上迭代了人类反馈与强化学习循环。模仿型智能体的表现明显逊于人类。而一轮又一轮的反馈与强化学习，解决搭塔问题的成功率超过了人类。

## 训练 AI 以契合情境化人类偏好的未来

用人类偏好作为奖励来训练 AI 的想法由来已久。在[《Deep reinforcement learning from human preferences》](https://www.deepmind.com/publications/deep-reinforcement-learning-from-human-preferences)中，研究者开创了近期的若干方法，把基于神经网络的智能体与人类偏好对齐。近来开发回合制对话智能体的工作，也探索了类似的想法，即[用人类反馈的强化学习来训练助手](https://arxiv.org/abs/2204.05862)。我们的研究对这些想法加以改造和扩展，构建出灵活的 AI，能够掌握范围广泛的多模态、具身、实时的人机交互。

我们希望，有朝一日我们的框架能催生出能够回应我们自然表达的含义的游戏 AI，而不必依赖人工编写的行为脚本。我们的框架也可用于构建供人们日常交互的数字化与机器人助手。我们期待探索应用这一框架各要素的可能性，以创造真正有帮助的安全 AI。

想了解更多？请查看[我们的最新论文](https://arxiv.org/abs/2211.11602)。欢迎反馈与评论。

**注释**

[1] Abramson, J., Ahuja, A., Barr, I., Brussee, A., Carnevale, F., Cassin, M., Chhaparia, R., Clark, S., Damoc, B., Dudzik, A. and Georgiev, P., 2020. Imitating interactive intelligence. arXiv preprint arXiv:2012.05672.

[2] Abramson, J., Ahuja, A., Brussee, A., Carnevale, F., Cassin, M., Fischer, F., Georgiev, P., Goldin, A., Harley, T. and Hill, F., 2021. Creating multimodal interactive agents with imitation and self-supervised learning. arXiv preprint arXiv:2112.03763.

[3] Abramson, J., Ahuja, A., Carnevale, F., Georgiev, P., Goldin, A., Hung, A., Landon, J., Lillicrap, T., Muldal, A., Richards, B. and Santoro, A., 2022. Evaluating Multimodal Interactive Agents. arXiv preprint arXiv:2205.13274.

[4] Bai, Y., Jones, A., Ndousse, K., Askell, A., Chen, A., DasSarma, N., Drain, D., Fort, S., Ganguli, D., Henighan, T. and Joseph, N., 2022. Training a Helpful and Harmless Assistant with Reinforcement Learning from Human Feedback. arXiv preprint arXiv:2204.05862.

[5] Christiano, P.F., Leike, J., Brown, T., Martic, M., Legg, S. and Amodei, D., 2017. Deep reinforcement learning from human preferences. Advances in neural information processing systems, 30.
