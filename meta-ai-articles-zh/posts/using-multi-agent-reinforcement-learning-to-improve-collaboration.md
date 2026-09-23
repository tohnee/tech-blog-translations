---
title: "用多智能体强化学习改进协作"
title_en: "Using Multi-Agent Reinforcement Learning to Improve Collaboration"
date: 2019-03-15
source: https://ai.facebook.com/blog/using-multi-agent-reinforcement-learning-to-improve-collaboration
crawled: 2026-09-22
translated: 2026-09-22
---

# 用多智能体强化学习改进协作

> 原文：[Using Multi-Agent Reinforcement Learning to Improve Collaboration](https://ai.facebook.com/blog/using-multi-agent-reinforcement-learning-to-improve-collaboration) · Meta AI（Wayback 存档）

**研究内容：** 一种用于协作式多智能体强化学习（RL）的新方法，它将任务分配给群体中的各个智能体，从而提升整个群体的协作能力。我们在即时战略游戏《星际争霸®：母巢之战®》（StarCraft®: Brood War®）中测试了该方法，发现我们用 RL 训练的模型显著胜过了依赖精心调校的规则基线的电脑控制玩家。也许最重要的是，这些优势延续到了部队规模远超训练场景的对局中。我们正在 TorchCraftAI GitHub 仓库发布该方法的源代码，并详述我们的结果——结果表明，把协作式多智能体 RL 视为动态分配问题，可以培育出更善于泛化到更复杂情境的智能体群体。

**工作原理：** 我们的方法聚焦于多智能体协作（multi-agent collaborative，MAC）问题，其中智能体必须完成多个中间任务才能达成一个更大的目标。随着此类 MAC 问题中智能体和任务数量的增加，复杂度呈指数级增长，使系统无法直接从大规模场景中学习。系统必须从小场景泛化，去应对那些不在其基于 RL 的试错训练中出现过的任务。由于 RL 训练的系统往往恰好在这类泛化上举步维艰，我们的方法把 MAC 策略分解为高层策略和低层策略。高层策略决定哪些智能体应被分配哪些具体任务。为鼓励智能体之间的协作，我们采用一个针对长期表现优化的二次代价函数，并调整高层分配以遵循最高效的协同模式。智能体被分配任务后，依据固定的低层策略执行任务，由其决定完成任务所需的具体动作。

这段视频从宏观上展示了我们的多智能体协作方法，包括我们如何利用任务分配在《星际争霸®：母巢之战®》中赢得战斗。

我们通过解决《星际争霸®：母巢之战®》中的目标选择问题测试了该方法。当两支部队交战时，每个单位必须选择攻击敌方部队的哪个成员。视情形而定，智能体学会将火力集中在少数单位上，或者把伤害分散到更多脆弱目标上。我们的智能体还学会利用移动模式，包括推迟攻击直到敌方单位靠近，从而在智能体保持更紧密、更高效阵型的同时有效分割敌军。除了表现出色——在某些配置下约 99% 的时间击败基于规则的对手——这些基于 RL 的系统还展现了令人瞩目的泛化能力，在参战单位数量达到训练时五倍之多的战斗中依然取胜。

**为什么重要：** 构建能有效协作的智能体，对各种各样的问题都很重要。例如，一队机器人可能需要协作探索陌生空间。除了帮助解决这些挑战外，我们的方法还回应了 RL 领域内一个更广泛的挑战：开发能适应新情况的训练技术。这一方法证明了从小问题中学到的经验可以应用到明显更大的问题上，这对各类 AI 系统的训练技术都可能产生影响。

阅读完整论文：《A structured prediction approach for generalization in cooperative multi-agent reinforcement learning》

本工作的源代码已在 GitHub 上提供。参加 NeurIPS 2019 的观众可以在 12 月 10 日（周二）的 spotlight 报告和海报环节（海报 #194）了解更多——分别于当地时间下午 4:35 和 5:30 开始。
