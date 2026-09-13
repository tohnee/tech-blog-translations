---
title: "Google DeepMind 参加 ICLR 2024"
title_en: "Google DeepMind at ICLR 2024"
source: https://deepmind.google/blog/google-deepmind-at-iclr-2024/
site: deepmind
date: 2024-05-03
crawled: 2026-09-13
translated: 2026-09-13
---

# Google DeepMind 参加 ICLR 2024

> 原文：[Google DeepMind at ICLR 2024](https://deepmind.google/blog/google-deepmind-at-iclr-2024/) · Google DeepMind

开发下一代 AI 智能体、探索新模态、开拓基础学习

下周，来自全球的 AI 研究者将齐聚第十二届[国际学习表征会议](https://iclr.cc/)（ICLR），会议定于 5 月 7 日至 11 日在奥地利维也纳举行。

Google DeepMind 研究副总裁 Raia Hadsell 将发表主题演讲，回顾该领域过去 20 年的历程，并重点介绍这些经验教训如何塑造造福人类的 AI 未来。

我们还将提供现场演示，展示我们如何把基础研究变为现实，从 [Robotics Transformers](https://deepmind.google/discover/blog/shaping-the-future-of-advanced-robotics/) 的开发，到 [Gemma](https://blog.google/technology/developers/gemma-open-models/) 等工具包与开源模型的打造。

今年，来自 Google DeepMind 各团队将发表 70 余篇论文。部分研究亮点如下：

[Google Research at ICLR 2024](https://research.google/conferences-and-events/google-at-iclr-2024/)

## 解决问题的智能体与受人类启发的做法

大语言模型（LLM）已经在变革高级 AI 工具，但它们的全部潜力仍未被挖掘。例如，能够采取有效行动的基于 LLM 的 AI 智能体，可以把数字助手转变为更有帮助、更直观的 AI 工具。

能够遵循自然语言指令、代表人们在网络上执行任务的 AI 助手将极大节省时间。在一场口头报告中，我们将介绍 [WebAgent](https://openreview.net/pdf?id=9JQtrumvg8)，这是一个由 LLM 驱动的智能体，通过自身经验学习，在真实网站上导航并管理复杂任务。

为了进一步提升 LLM 的通用实用性，我们专注于增强它们解决问题的能力。我们展示了如何通过赋予基于 LLM 的系统一种传统上属于人类的做法来实现这一点：[生产并使用「工具」](https://openreview.net/forum?id=qV83K9d5WB)。另外，我们提出了一种训练技术，确保语言模型持续产出[更符合社会规范的输出。我们的方法](https://openreview.net/forum?id=NddKiWtdUm)使用一个沙盒排练空间来体现[社会的价值观](https://deepmind.google/discover/blog/the-ethics-of-advanced-ai-assistants/)。

## 突破视觉与编程的边界

![一组动画视频片段网格，展示日常物体（包括围棋棋盘、马克杯、钥匙、食物和室内场景）的不同机位视角，说明 Dynamic Scene Transformer（DyST）模型从不同视角生成 3D 视频表征的能力。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/Figure-1.gif)

我们的 Dynamic Scene Transformer（DyST）模型利用真实世界的单摄像机视频，提取场景中物体及其运动的 3D 表征。

直到最近，大型 AI 模型大多聚焦于文本和图像，为大规模模式识别与数据解读奠定了基础。如今，该领域正超越这些静态领域，迈向真实世界视觉环境的动态特性。随着计算的全面进步，以最高效率生成和优化底层代码也变得越来越重要。

当你在平面屏幕上观看视频时，你会直观地把握场景的三维特性。然而，机器在缺乏显式监督的情况下难以模仿这种能力。我们将展示我们的 [Dynamic Scene Transformer](https://openreview.net/forum?id=MnMWa94t12)（DyST）模型，它利用真实世界的单摄像机视频提取场景中物体及其运动的 3D 表征。更进一步，DyST 还能在用户控制相机角度和内容的情况下，生成同一视频的全新版本。

模仿人类的认知策略也能造就更好的 AI 代码生成器。程序员在编写复杂代码时，通常会把任务「分解」为更简单的子任务。借助 [ExeDec](https://openreview.net/pdf?id=oTRwljRgiv)，我们提出了一种新颖的代码生成方法，利用分解策略提升 AI 系统的编程能力与泛化性能。

在另一篇并行的 [spotlight 论文](https://openreview.net/forum?id=ix7rLVHXyY&referrer=%5BAuthor%20Console%5D%28%2Fgroup%3Fid%3DICLR.cc%2F2024%2FConference%2FAuthors%23your-submissions)中，我们探索了机器学习的新颖用途：不仅生成代码，还要优化代码，并为此引入了一个[用于代码性能稳健基准测试的数据集](https://pie4perf.com/)。代码优化极具挑战性，需要复杂的推理，而我们的数据集使一系列 ML 技术的探索成为可能。我们证明，由此得到的学习策略优于人工设计的代码优化。

![代码优化的并排对比：左侧显示复杂的原始 C++ 源代码，右侧显示「Generated Code」，速度提升达 18.80 倍。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/Figure_2.gif)

ExeDec 提出了一种新颖的代码生成方法，利用分解策略提升 AI 系统的编程能力与泛化性能

## 推进基础学习

我们的研究团队正在攻克 AI 的重大问题——从探索机器认知的本质，到理解先进 AI 模型如何泛化——同时也在努力克服关键的理论挑战。

对人类和机器而言，因果推理与预测事件的能力是密切相关的概念。在一场 spotlight 报告中，我们探讨[强化学习如何受到基于预测的训练目标的影响](https://openreview.net/forum?id=agPpmEgf8C)，并将其与同样与预测相关的大脑活动变化进行类比。

当 AI 智能体能够对新场景良好泛化时，是不是因为它们像人类一样，学到了所处世界的底层因果模型？这是先进 AI 中的一个关键问题。在一场口头报告中，我们揭示这类模型[确实已经学到了产生其训练数据的过程的近似因果模型](https://openreview.net/forum?id=pOoKI3ouv1)，并讨论其深远含义。

AI 中的另一个关键问题是信任，它在一定程度上取决于模型能多准确地估计其输出的不确定性——这是可靠决策的关键因素。我们在贝叶斯深度学习的不确定性估计方面取得了[重大进展](https://openreview.net/forum?id=Sx7BIiPzys)，所用方法简单且几乎没有额外成本。

最后，我们探索博弈论中的纳什均衡（Nash equilibrium，NE）——即在其他参与者策略不变的情况下，没有参与者能通过改变自身策略而获益的状态。在简单的双人博弈之外，即便是近似求解纳什均衡在计算上也是难以处理的，但在一场口头报告中，我们[揭示了从扑克到拍卖等谈判交易问题上新的最先进方法](https://openreview.net/forum?id=cc8h3I3V4E)。

## 凝聚 AI 社区

我们很高兴赞助 ICLR，并支持 [Queer in AI](https://www.queerinai.com/) 和 [Women In Machine Learning](https://www.wiml.org/) 等举措。这样的伙伴关系不仅促进研究合作，也培育了 AI 与机器学习领域充满活力、多元包容的社区。

如果你来到 ICLR 现场，请务必参观我们的展位以及隔壁 [Google Research](https://research.google/conferences-and-events/google-at-iclr-2024/) 同事的展位。了解我们的开创性研究，与主持工作坊的团队见面，并与在会议各环节作报告的专家交流。我们期待与你相见！
