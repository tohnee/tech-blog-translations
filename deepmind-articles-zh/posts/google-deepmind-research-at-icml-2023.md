---
title: "Google DeepMind 在 ICML 2023 上的最新研究"
title_en: "Google DeepMind's latest research at ICML 2023"
source: https://deepmind.google/blog/google-deepmind-research-at-icml-2023/
site: deepmind
date: 2023-07-20
crawled: 2026-09-13
translated: 2026-09-13
---

# Google DeepMind 在 ICML 2023 上的最新研究

> 原文：[Google DeepMind's latest research at ICML 2023](https://deepmind.google/blog/google-deepmind-research-at-icml-2023/) · Google DeepMind

探索面向真实世界的 AI 安全、适应性与效率

下周，第 40 届[国际机器学习大会](https://icml.cc/)（ICML 2023）即将开幕，会议将于 7 月 23 日至 29 日在夏威夷檀香山举行。

ICML 汇聚人工智能（AI）社区，分享新想法、新工具和新数据集，建立联系以推动领域发展。从计算机视觉到机器人学，来自世界各地的研究人员将展示他们的最新进展。

我们的科学、技术与社会总监 Shakir Mohamed 将发表[一场关于具有社会目标的机器学习的演讲](https://icml.cc/virtual/2023/invited-talk/21547)，应对医疗与气候领域的挑战，采取社会技术视角，并加强全球社区建设。

我们很荣幸以白金赞助商的身份支持本次大会，并继续与我们的长期合作伙伴 [LatinX in AI](https://www.latinxinai.org/)、[Queer in AI](https://www.queerinai.com/) 和 [Women in Machine Learning](https://wimlworkshop.org/) 携手合作。

在大会上，我们还将展示 [AlphaFold](https://www.deepmind.com/research/highlighted-research/alphafold) 的演示、我们在[聚变科学](https://deepmind.google/blog/accelerating-fusion-science-through-learned-plasma-control/)方面的进展，以及 [PaLM-E](https://ai.googleblog.com/2023/03/palm-e-embodied-multimodal-language.html)（面向机器人学）和 [Phenaki](https://sites.research.google/phenaki/)（从文本生成视频）等新模型。

Google DeepMind 的研究人员今年将在 ICML 上展示 80 多篇新论文。由于许多论文是在 [Google Brain 与 DeepMind 合并](https://deepmind.google/blog/announcing-google-deepmind/)之前提交的，最初以 Google Brain 附属机构名义提交的论文将收录在 [Google Research 博客](https://ai.googleblog.com/2023/07/google-at-icml-2023.html)中，而本博客重点介绍以 DeepMind 附属机构名义提交的论文。

[查看完整的 ICML 2023 日程](https://deepmind.events/events/icml-2023)

## （模拟）世界中的 AI

能够读、写、创造的 AI 之所以成功，其基石是基础模型——在海量数据集上训练、能够学习执行多种任务的 AI 系统。我们的最新研究探索了如何将这些成果转化到真实世界中，并为更通用、更具具身性的 AI 智能体奠定基础，使其能够更好地理解世界的动态规律，为更有用的 AI 工具开辟新的可能。

在一场口头报告中，我们介绍了 [AdA](https://arxiv.org/abs/2301.07608)——一个能够像人类一样适应并解决模拟环境中新问题的 AI 智能体。在几分钟内，AdA 就可以应对具有挑战性的任务：以新颖的方式组合物体、在地形未知的环境中导航、与其他玩家合作。

同样，我们展示了如何[利用视觉-语言模型帮助训练具身智能体](https://arxiv.org/abs/2301.12507)——例如，告诉机器人它正在做什么。

## 强化学习的未来

要开发负责任、值得信赖的 AI，我们必须理解这些系统核心的目标。在强化学习中，定义目标的一种方式是通过奖励。

在一场口头报告中，我们旨在[了结奖励假说](https://arxiv.org/abs/2212.10420#:~:text=The%20reward%20hypothesis%20posits%20that,to%20fully%20settle%20this%20hypothesis.)——该假说由 Richard Sutton 首次提出，认为所有目标都可以被视为最大化期望累积奖励。我们解释了该假说成立的精确条件，并在强化学习问题的一般形式下，阐明了哪些目标可以、哪些不能由奖励以一般形式捕捉。

在部署 AI 系统时，它们必须足够鲁棒才能适应真实世界。我们研究了如何更好地[在约束条件下训练强化学习算法](https://arxiv.org/abs/2302.01275)——出于安全和效率的考虑，AI 工具往往必须受到限制。

在我们的研究（获得 [ICML 2023 杰出论文奖](https://icml.cc/Conferences/2023/Awards)认可）中，我们探索了如何用[不完全信息博弈](https://arxiv.org/abs/2212.12567)教模型在不确定性下掌握复杂的长期策略。我们展示了模型如何在不知道对手位置和可能动作的情况下，依然在双人博弈中取胜。

## AI 前沿的挑战

人类可以轻松地学习、适应并理解我们周围的世界。开发能够以类人方式进行泛化的先进 AI 系统，将有助于创造我们可以在日常生活中使用的 AI 工具，以应对新的挑战。

AI 适应的一种方式是根据新信息快速调整其预测。在一场口头报告中，我们研究了[神经网络的可塑性](https://arxiv.org/abs/2303.01486#:~:text=We%20find%20that%20loss%20of,units%20or%20divergent%20gradient%20norms.)，以及它在训练过程中如何丢失——以及防止丢失的方法。

我们还展示了一项研究：通过研究[在统计特性会自发变化的数据源上进行元训练的神经网络](https://arxiv.org/abs/2302.03067)——例如自然语言预测——它可能有助于解释大语言模型中涌现的上下文学习。

在一场口头报告中，我们介绍了一类在长期推理任务上表现更好的新型循环神经网络[(RNN)](https://arxiv.org/abs/2303.06349)，以释放这类模型面向未来的潜力。

最后，在「[分位数信用分配](https://openreview.net/pdf?id=4yoLVter71)」中，我们提出了一种将运气与技能解耦的方法。通过在动作、结果和外部因素之间建立更清晰的关系，AI 可以更好地理解复杂的真实世界环境。
