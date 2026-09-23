---
title: "NetHack 学习环境：推进深度强化学习"
title_en: "The NetHack Learning Environment to advance deep reinforcement learning"
date: 2020-06-25
source: https://ai.facebook.com/blog/nethack-learning-environment-to-advance-deep-reinforcement-learning
crawled: 2026-09-22
translated: 2026-09-22
---

# NetHack 学习环境：推进深度强化学习

> 原文：[The NetHack Learning Environment to advance deep reinforcement learning](https://ai.facebook.com/blog/nethack-learning-environment-to-advance-deep-reinforcement-learning) · Meta AI（Wayback 存档）

**研究内容**：NetHack 学习环境（NetHack Learning Environment）是一个新颖的研究环境，用于测试强化学习（RL）智能体的鲁棒性与系统性泛化能力。该环境基于 NetHack——最古老、最受欢迎的程序化生成 roguelike 游戏之一。现有的 RL 环境要么足够复杂，要么基于快速模拟，但很少能兼得。相比之下，NetHack 学习环境把闪电般的模拟速度与即便对人类也难以精通的复杂游戏动态相结合。这使我们的智能体能在合理时间内经历数十亿步的环境交互，同时仍然挑战当前方法所能达到的极限，推动探索、规划、技能习得和语言条件化 RL 等课题的长期研究。NetHack 的复杂性体现在数百种物品和怪物类型，以及它们与玩家和环境之间的丰富交互。而智能体有一个明确的目标：下到 50 多层致命的地牢深处取回护身符，然后飞升成为半神。由于 NetHack 的关卡是程序化生成的，每局游戏都不同，考验着当前最先进方法的泛化极限。为了精通这款游戏，甚至人类玩家也常常需要查阅 NetHack Wiki 等外部资源，以识别关键策略或发现新的前进路径。我们相信这使 NetHack 成为超越「白板」（tabula rasa）RL 的令人兴奋的研究环境。

（题图说明：NetHack 中智能体的标注示例。）所有这些复杂性都由一个主要以 C 语言编写的游戏引擎，以回合制网格世界、ASCII 字符画的形式呈现。这种极其轻量的模拟——舍弃除最简单物理之外的一切、渲染符号而非像素——让我们的模型能在此环境中非常快速地学习，而不会把算力浪费在模拟游戏动态或渲染观测上——这两者对挑战学习智能体的根本技能都无关紧要。

**工作原理**：该环境由三部分组成：使用流行的 OpenAI Gym API 的 NetHack Python 接口；一套基准任务；以及基于 TorchBeast（IMPALA 的 PyTorch 实现）的分布式深度强化学习基线智能体。由于我们认为「解开 NetHack」这一总体目标在可预见的未来仍遥不可及，我们定义了七个基准任务来度量进展：

- **staircase（楼梯）**：下到地牢更深层
- **pet（宠物）**：照顾你的宠物（让它活着并带它进入地牢更深处）
- **eat（进食）**：寻找无毒的食物来源并进食，以免饿死
- **gold（金币）**：在地牢各处收集金币
- **scout（侦察）**：尽可能多地探索地牢
- **score（得分）**：取得高游戏得分（例如击杀怪物、下潜、收集金币）
- **oracle（神谕）**：到达一个重要地标——神谕（Oracle，出现在地牢 4-9 层处）

这些只是我们用来度量模型当前能力的代理任务，还可以轻松定义更多任务。（题图说明：随 NetHack 学习环境一同发布的基线模型概览。）使用单块高端 GPU，就可以通过 TorchBeast 框架每天训练智能体数亿环境步；该框架还支持通过增加 GPU 或机器进一步扩展。这为智能体提供了充足的学习经验，也让我们研究者能把更多时间花在验证新想法上，而不是等待结果。此外，我们相信它让资源较受限实验室的研究者也能使用，同时不牺牲环境的难度与丰富性。我们的基线智能体实现基于一个循环策略，对 NetHack 观测空间的各个部分进行编码。

NetHack 还包含大量外部资源，可用于未来研究以提升智能体在游戏中的表现。例如，存在人类玩家回放数据的大型仓库，模型可以直接从中学习。还有许多人类玩家为提升游戏水平而查阅的资源，包括随游戏发布的《NetHack Guidebook》、由玩家社区维护的 NetHack Wiki，以及大量在线视频和论坛讨论。如何有效利用这些资源中的任何一种，对于希望借助外部知识源提升模型性能和样本效率的 RL 研究者来说都是开放问题。

（视频说明：一个强化学习智能体在 NetHack 中探索侏儒矿。）

**为什么重要**：NetHack 提出的挑战正处于当前方法的前沿，而又不带来其他高挑战模拟环境的计算成本。当前在 NetHack 上运行的标准深度强化学习智能体仅探索了整个游戏的一小部分。要在这个富有挑战的新环境中取得进展，需要 RL 智能体超越白板式学习——例如，研究与自然语言理解的协同，以利用 NetHack Wiki 上的信息。我们相信 NetHack 学习环境将激发对强化学习中鲁棒探索策略、长时程规划，以及从模拟之外的资源迁移常识知识的进一步研究。

阅读完整论文：The NetHack Learning Environment
