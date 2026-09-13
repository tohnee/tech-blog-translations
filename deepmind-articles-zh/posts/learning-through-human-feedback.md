---
title: "通过人类反馈进行学习"
title_en: "Learning through human feedback"
source: https://deepmind.google/blog/learning-through-human-feedback/
site: deepmind
date: 2017-06-12
crawled: 2026-09-13
translated: 2026-09-13
---

# 通过人类反馈进行学习

> 原文：[Learning through human feedback](https://deepmind.google/blog/learning-through-human-feedback/) · Google DeepMind

我们相信，人工智能将是有史以来最重要、最能广泛造福人类的科学进步之一，能够帮助人类应对从气候变化到提供先进医疗保健等一些最重大的挑战。但要让 AI 兑现这一承诺，我们知道这项技术[必须以负责任的方式构建](https://ai.googleblog.com/2016/06/bringing-precision-to-ai-safety.html)，并且必须考虑所有潜在的挑战与风险。

正因如此，DeepMind 参与共同发起了诸如[造福人类与社会的 AI 伙伴关系（Partnership on AI to Benefit People and Society）](https://www.partnershiponai.org/)之类的倡议，也正是因此，我们拥有一支专门致力于技术性 AI 安全的团队。这一领域的研究需要开放与协作，以确保最佳实践得到尽可能广泛的采用，这也是我们与 [OpenAI](https://openai.com/) 就[技术性 AI 安全研究](https://openai.com/blog/deep-reinforcement-learning-from-human-preferences/)开展合作的原因。

这一领域的核心问题之一是：如何让人类告诉一个系统我们希望它做什么——同样重要的是——我们不希望它做什么。随着我们用机器学习解决的问题日益复杂并应用于现实世界，这个问题变得越来越重要。

此次合作取得的[首批成果](https://arxiv.org/abs/1706.03741)展示了一种解决之道：让没有任何技术经验的人能够教一个强化学习（reinforcement learning，RL）系统——一种通过试错学习的 AI——去实现一个复杂的目标。这样就无需人类事先为算法指定目标。这是重要的一步，因为目标哪怕设定得稍有偏差，就可能导致不良甚至危险的行为。在某些情况下，来自非专业人士的短短 30 分钟反馈就足以训练我们的系统，包括教会它全新的复杂行为，例如让一个模拟机器人完成后空翻。

![AI 控制的模型完成后空翻。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622378d1616ef655e7c8590d_unnamed-2_1.gif)

教会这个算法完成后空翻，大约需要人类提供 900 条反馈

这一系统在[我们的论文《Deep Reinforcement Learning from Human Preferences》](https://arxiv.org/abs/1706.03741)中有详细描述。它不同于经典的 RL 系统：智能体的训练不是基于它在探索环境时收集到的奖励，而是基于一个被称为"奖励预测器"（reward predictor）的神经网络。

它由三个并行运行的过程组成：

1. 强化学习智能体探索并与环境交互，例如玩一款 Atari 游戏。
2. 系统定期把智能体行为的两段 1-2 秒短片发送给人类操作员，请其选出其中哪一段更好地展示了朝目标迈进的过程。
3. 人类的选择被用来训练奖励预测器，奖励预测器再去训练智能体。随着时间推移，智能体学会最大化来自预测器的奖励，并按照人类的偏好改进自身行为。

![带有人类反馈的强化学习流程示意图。RL 算法通过动作与观察和环境交互（第 1 步）。人类操作员向奖励预测器提供反馈（第 2 步），奖励预测器随后把预测奖励发回给 RL 算法（第 3 步）。](https://lh3.googleusercontent.com/KJJQZzwUEjjKAJXIuBFmS5NTJyj0jNy2o2OzIbNPhmKn8vabt_p8zwuXMNukS5PyiIr-mOstZyT1JlK57Kyw1bxjkifDL15XMRm7bFATCVaBPhAIFQ=w1440)

这一系统把"学习目标"与"学习实现目标的行为"分离开来

这种迭代式的学习方式意味着，人类可以发现并纠正任何不受欢迎的行为，这是任何安全系统的关键组成部分。这一设计也不会给人类操作员带来繁重负担：操作员只需审查智能体大约 0.1% 的行为，就能让它按自己的意愿行事。不过，这可能意味着要审查几百到几千对短片，要让这一方法适用于现实世界的问题，这一负担还需要降低。

![并排比较界面，显示 Atari 游戏 Q*bert 的两段短片，分别标注为"Left"和"Right"，下方带有供人类操作员评估哪个智能体行为更好的交互按钮，选项包括"Left is better"、"Right is better"、"It's a tie"和"Can't tell"。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6223794abf2cca4c6a9dc751_unnamed.gif)

人类操作员必须在两段短片之间做出选择。在这个 Atari 游戏 Qbert 的例子中，右边那段展示的是更好的——得分的——行为

在 Atari 游戏 Enduro 中，玩家需要驾驶一辆汽车超越一整排其他车辆，传统 RL 网络的试错技术极难学会这个游戏，而人类反馈最终让我们的系统取得了超越人类的成绩。在其他游戏和模拟机器人任务中，它的表现与标准 RL 设置相当；而在 Qbert 和 Breakout 等少数几款游戏中，它则完全失效。

但这类系统的最终目的，是让人类能够为智能体指定一个目标，哪怕这个目标并不存在于环境之中。为了验证这一点，我们教会了智能体各种新颖的行为，例如完成后空翻、单腿行走，或者在 Enduro 中学会与另一辆车并排行驶，而不是通过超越前车来最大化游戏得分。

![智能体玩电子游戏 Enduro 的录像。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62237af8d24c681a8e67e81e_unnamed-3.gif)

Enduro 的正常目标是尽可能超越更多的车。但利用我们的系统，我们可以训练智能体追求不同的目标，例如与其他车辆并排行驶

尽管这些测试显示出一些积极的结果，另一些测试也暴露了它的局限。特别是，如果在训练早期就中断人类反馈，我们的系统就容易受到奖励作弊（reward hacking）的影响——也就是钻奖励函数的空子。在这种情况下，智能体仍会继续探索环境，这意味着奖励预测器不得不为它从未收到过反馈的情形估计奖励。这可能导致它高估奖励，进而诱使智能体学到错误的——往往十分怪异——行为。下面的视频就是一个例子：智能体发现，来回击球比赢球或丢分是"更好"的策略。

![智能体与自己对打电子游戏 Pong 的录像。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62237b1eede3d70a945ba522_unnamed-4.gif)

智能体钻了自己奖励函数的空子，认定来回击球比赢球或丢分更好

理解这类缺陷至关重要，这能确保我们避免失败，构建出按预期行事的 AI 系统。

要测试并完善这一系统，还有更多工作要做，但它已经展示了几项关键的第一步：打造可以由非专业用户教授的系统、让系统对所需反馈量更加经济、并使其能够扩展到各种不同的问题上。

其他值得探索的方向包括：减少所需人类反馈的数量，或者让人类能够通过自然语言界面提供反馈。这将标志着在打造一个能够轻松从复杂人类行为中学习的系统方面迈出飞跃性的一步，也是朝着创建与全人类协作并服务于全人类的 AI 迈出的关键一步。

**注**

这项研究是 DeepMind 的 Jan Leike、Miljan Martic 和 Shane Legg 与 OpenAI 的 Paul Christiano、Dario Amodei 和 Tom Brown 之间持续合作的一部分。

阅读[完整论文](https://arxiv.org/abs/1706.03741)

阅读 [OpenAI 的博客文章](https://openai.com/blog/deep-reinforcement-learning-from-human-preferences/)

阅读《[Concrete Problems in AI Safety](https://arxiv.org/abs/1606.06565)》以了解该主题的更多背景
