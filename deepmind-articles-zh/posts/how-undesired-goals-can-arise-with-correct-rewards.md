---
title: "奖励正确时，非预期目标如何产生"
title_en: "How undesired goals can arise with correct rewards"
source: https://deepmind.google/blog/how-undesired-goals-can-arise-with-correct-rewards/
site: deepmind
date: 2022-10-07
crawled: 2026-09-13
translated: 2026-09-13
---

# 奖励正确时，非预期目标如何产生

> 原文：[How undesired goals can arise with correct rewards](https://deepmind.google/blog/how-undesired-goals-can-arise-with-correct-rewards/) · Google DeepMind

探讨目标错误泛化（goal misgeneralisation）的实例——AI 系统能力成功泛化，目标却未随之泛化

随着我们构建越来越先进的人工智能（AI）系统，我们要确保它们不会追求非预期目标（undesired goals）。AI 智能体的这类行为，往往是[规格作弊](https://deepmind.com/blog/article/Specification-gaming-the-flip-side-of-AI-ingenuity)（specification gaming）的结果——钻了奖励设定不佳的空子。在[最新论文](https://arxiv.org/abs/2210.01790)中，我们探讨了 AI 系统可能无意间学会追求非预期目标的一种更微妙的机制：[目标错误泛化](https://arxiv.org/abs/2105.14111)（goal misgeneralisation，GMG）。

GMG 发生在一个系统的能力成功泛化、而其目标却没有按预期泛化的时候，于是系统便有条不紊地追求错误的目标。关键在于，与规格作弊不同，即便 AI 系统是用正确的规格训练的，GMG 也可能发生。

我们此前[关于文化传递的工作](https://deepmind.google/blog/learning-robust-real-time-cultural-transmission-without-human-data/)曾引出一个我们并未有意设计的 GMG 行为实例。一个智能体（下图中的蓝色圆点）必须在自己的环境中四处移动，按正确顺序访问彩色球体。训练时，环境中有一个"专家"智能体（红色圆点）会按正确顺序访问彩色球体。该智能体学到：跟随红色圆点是一种有回报的策略。

![动态图像，显示由蓝色圆点代表的智能体观察由红色圆点代表的专家，以确定该前往哪个球体。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/633fee1aaa8967568ee1a5b9_following_expert_with_rewards.gif)

智能体（蓝色）观察专家（红色），以确定该前往哪个球体。

遗憾的是，虽然该智能体在训练期间表现出色，但当训练结束后我们把专家替换为一个按错误顺序访问球体的"反专家"时，它的表现就很差了。

![智能体（蓝色圆点）跟随反专家（红色圆点）的动态图像，不断累积负奖励。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/633fee50d7c574b38004a005_following_anti_expert_with_rewards.gif)

智能体（蓝色）跟随反专家（红色），不断累积负奖励。

尽管智能体能够观察到自己正在得到负奖励，它却不去追求"按正确顺序访问球体"这一期望目标，而是有条不紊地追求"跟随红色智能体"这一目标。

GMG 并不局限于这样的强化学习环境。事实上，它可能发生在任何学习系统中，包括大语言模型（LLM）的"少样本学习"。少样本学习方法旨在用更少的训练数据构建准确的模型。

我们提示一个大语言模型 [Gopher](https://arxiv.org/abs/2112.11446) 去求值包含未知变量和常数的线性表达式，例如 x+y-3。要求解这些表达式，Gopher 必须先询问未知变量的取值。我们为它提供了十个训练样例，每个样例都涉及两个未知变量。

在测试时，我们用含零个、一个或三个未知变量的问题询问模型。虽然模型能正确泛化到含一个或三个未知变量的表达式，但当表达式中没有未知数时，它仍会提出冗余的问题，比如"What's 6?"。模型在给出答案之前总会至少查询用户一次，即便毫无必要。

![一张包含三列的表格，展示用户（User）与 Gopher 之间的对话。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/63400170626042521ef973b3_GMG.svg)

在"表达式求值"（Evaluating Expressions）任务上与 Gopher 进行少样本学习的对话，GMG 行为已高亮标出。

在论文中，我们还在其他学习场景中提供了更多实例。

解决 GMG 问题对于让 AI 系统与其设计者的目标对齐十分重要，原因很简单：它是 AI 系统可能失灵的一种机制。当我们逼近通用人工智能（AGI）时，这一点将尤为关键。

设想两种可能类型的 AGI 系统：

- **A1：符合意图的模型。** 这个 AI 系统会按设计者的意图行事。
- **A2：欺骗性模型。** 这个 AI 系统追求某个非预期目标，但（按假设）它也足够聪明，知道如果自己的行为违背设计者的意图就会受到惩罚。

由于 A1 和 A2 在训练期间会表现出相同的行为，GMG 的可能性意味着最终形成的可能是其中任何一个模型——即便规格只奖励符合意图的行为也是如此。如果学到的是 A2，它就会试图颠覆人类的监督，以便把它的计划推向那个非预期目标。

我们的研究团队乐于见到后续工作去探究 GMG 在实践中发生的可能性有多大，以及可能的缓解措施。在论文中，我们提出了一些思路，包括[机制](https://distill.pub/2020/circuits/zoom-in/)[可解释性](https://www.transformer-circuits.pub/2021/framework/index.html)与[递归式](https://arxiv.org/abs/1805.00899)[评估](https://arxiv.org/abs/1810.08575)，这两者我们都在积极研究之中。

我们目前正在这份[公开可用的表格](http://tinyurl.com/goal-misgeneralisation)中收集 GMG 的实例。如果你在 AI 研究中遇到过目标错误泛化，欢迎你[在此提交实例](https://docs.google.com/forms/d/e/1FAIpQLSdEsL9BuLJAm9wdK8IK8eTTm7tbGFASbJ4AcWCmwvVPFxbl8g/viewform?resourcekey=0-_ADP04VQHl9_Yr0WmoNQtQ)。
