---
title: "DeepMind 与 Blizzard 开放《星际争霸 II》作为 AI 研究环境"
title_en: "DeepMind and Blizzard open StarCraft II as an AI research environment"
source: https://deepmind.google/blog/deepmind-and-blizzard-open-starcraft-ii-as-an-ai-research-environment/
site: deepmind
date: 2017-08-09
crawled: 2026-09-13
translated: 2026-09-13
---

# DeepMind 与 Blizzard 开放《星际争霸 II》作为 AI 研究环境

> 原文：[DeepMind and Blizzard open StarCraft II as an AI research environment](https://deepmind.google/blog/deepmind-and-blizzard-open-starcraft-ii-as-an-ai-research-environment/) · Google DeepMind

DeepMind 的科学使命，是通过开发能够学习解决复杂问题的系统来拓展 AI 的边界。为此，我们设计智能体，并在从专门构建的 [DeepMind Lab](https://arxiv.org/pdf/1612.03801.pdf) 到[雅达利（Atari）](https://github.com/mgbellemare/Arcade-Learning-Environment)、[围棋](https://deepmind.com/research/case-studies/alphago-the-story-so-far)等成熟游戏的广泛环境中测试它们的能力。

让我们的智能体在那些并非专为 AI 研究设计、而人类又玩得很好的游戏中接受检验，对于衡量智能体的性能至关重要。正因如此，我们非常高兴能与[合作伙伴 Blizzard Entertainment](https://starcraft2.com/en-us/) 一道，宣布发布 SC2LE——一套我们希望将加速即时战略游戏《星际争霸 II》（StarCraft II）领域 AI 研究的工具。SC2LE 的发布内容包括：

- 由 Blizzard 开发的一套[机器学习 API](https://github.com/Blizzard/s2client-proto)，为研究人员和开发者提供接入游戏的钩子。其中首次包含了面向 Linux 的工具。
- 一个[匿名化的对局回放数据集](https://github.com/Blizzard/s2client-proto#replay-packs)，它将在未来几周内从 6.5 万局增加到超过 50 万局。
- DeepMind 工具集 [PySC2](https://github.com/deepmind/pysc2) 的开源版本，让研究人员能够轻松地在自己的智能体中使用 Blizzard 的特征层 API。
- 一系列简单的强化学习（RL）小游戏，供研究人员测试智能体在特定任务上的表现。
- 一篇[联合论文](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/deepMind-and-blizzard-open-starcraft-ii-as-an-ai-research-environment/sc2le.pdf)，概述了这一环境，并报告了在小游戏、从回放中进行监督学习，以及与内置 AI 对战的完整 1v1 天梯对局上的初步基线结果。

![《星际争霸 II》中带有发光绿色全息屏幕、按钮和开关的未来感控制面板。](https://lh3.googleusercontent.com/5zO_kwU78AYi-WFYhkuHDAEe5PtFk8HyW6ERBaVuBePBTSU5Usw5zTRtGHeGn4-1JZfylEnMu1EhX_7wVbckP1jqKvBeX2zHpoA5o6_QXdS1bAAXKqM=w1440)

《星际争霸 II》是一款以科幻为背景的即时战略游戏，于 2010 年发行

《星际争霸》和《星际争霸 II》是有史以来规模最大、最成功的游戏之一，玩家在各类锦标赛中竞技已超过 20 年。原版游戏也早已被 AI 与机器学习（ML）研究人员使用，他们每年都在 [AIIDE 机器人竞赛](http://www.cs.mun.ca/~dchurchill/starcraftaicomp/)中一较高下。《星际争霸》之所以长盛不衰，部分原因在于其丰富、多层次的游戏玩法，这也使它成为 AI 研究的理想环境。

举例来说，虽然游戏的目标是击败对手，但玩家还必须执行并平衡一系列子目标，例如采集资源或建造建筑。此外，一局游戏可能需要几分钟到一小时才能完成，这意味着游戏早期采取的行动可能要过很久才会见效。最后，地图只能被部分观察到，这意味着智能体必须结合记忆与规划才能取得成功。

这款游戏还有其他吸引研究者的特质，例如每天在线竞技的庞大而狂热的玩家群体。这保证了有大量可供学习的回放数据——同样也有大量极具天赋的对手等待着 AI 智能体。

就连《星际争霸》的动作空间本身也是一个挑战：可供选择的基本动作超过 300 个。与之对比，雅达利游戏只有大约 10 个（例如上、下、左、右等）。除此之外，《星际争霸》中的动作是分层级的，可以被修改和扩展，而且其中许多动作还需要指定屏幕上的一个点。即使假设屏幕尺寸小到 84x84，可用的可能动作也约有 1 亿种。

![一幅《星际争霸 II》游戏画面可视化，显示一个带绿色血条的蓝色小单位，下方标注了「人类动作」「智能体动作」和「可用动作」等分区。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622662820ee9d9abfa26f4e3_StarCraft2022002.gif)

人类和智能体可用的动作都取决于当前选中的单位

这次发布意味着，研究人员现在可以使用 Blizzard 自己的工具来构建自己的任务和模型，以应对其中一些挑战。

我们的 [PySC2](https://github.com/deepmind/pysc2) 环境封装提供了一个灵活且易用的接口，帮助强化学习智能体玩这款游戏。在本次初始发布中，我们将游戏分解为「特征层」（feature layers），把单位类型、生命值和地图可见性等游戏元素彼此隔离，同时保留了游戏的核心视觉与空间要素。

这次发布还包含一系列「小游戏」（mini-games）——这是一种成熟的技术，用于把游戏拆解成可管理的模块，用来在[特定](https://arxiv.org/abs/1703.10069)[任务](https://arxiv.org/abs/1609.02993)上测试智能体，例如移动视角、[采集矿物晶体](https://youtu.be/6L448yg0Sm0)或选择单位。我们希望研究人员既能在这些小游戏上测试自己的技术，也能提出新的小游戏，供其他研究者竞技和评估。

我们的初步研究表明，我们的智能体在这些小游戏上表现良好。但一旦进入完整对局，即使是[A3C](https://arxiv.org/abs/1602.01783) 这样强的基线智能体，也无法在哪怕最简单的内置 AI 面前赢下一局。例如，下面的视频展示了一个早期训练阶段的智能体（左）未能让自己的工人持续采矿——这对人类来说是一项轻而易举的任务。经过训练后（右），智能体能够执行更有意义的动作，但如果要具备竞争力，我们还需要在深度强化学习及相关领域取得进一步的突破。

我们知道，有一种技术能让我们的智能体学到更强的策略，那就是模仿学习。得益于 Blizzard 承诺持续发布从《星际争霸 II》天梯中收集的数十万份匿名回放，这类训练很快会变得容易得多。这不仅能让研究人员训练监督式智能体来玩这款游戏，还开辟了序列预测和长期记忆等其他有趣的研究方向。

我们希望这些新工具的发布能在 AI 社区在《星际争霸》上已有工作的基础上更进一步，鼓励更多深度强化学习（DeepRL）研究，并让研究人员更容易聚焦于本领域的前沿。

我们期待看到社区做出新的发现。

**附注**

更多信息请参阅 [Blizzard 博客](https://starcraft2.com/en-us/)。

PySC2 可从 [DeepMind 的 GitHub 页面](https://github.com/deepmind/pysc2)获取。

Blizzard 的《星际争霸》API 可在[这里](https://github.com/Blizzard/s2client-proto)获取，其中包含如何获取 Linux 版本、回放及其他内容的细节。

如果你在研究中使用了我们的环境，请引用[发布论文](https://deepmind.com/research/publications/Starcraft-II-A-New-Challenge-for-Reinforcement-Learning)。
