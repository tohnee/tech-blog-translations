---
title: "TacticAI：足球战术 AI 助手"
title_en: "TacticAI: an AI assistant for football tactics"
source: https://deepmind.google/blog/tacticai-ai-assistant-for-football-tactics/
site: deepmind
date: 2024-03-19
crawled: 2026-09-13
translated: 2026-09-13
---

# TacticAI：足球战术 AI 助手

> 原文：[TacticAI: an AI assistant for football tactics](https://deepmind.google/blog/tacticai-ai-assistant-for-football-tactics/) · Google DeepMind

作为我们与利物浦足球俱乐部（Liverpool FC）多年合作的一部分，我们开发了一套完整的 AI 系统，可以就角球向教练提供建议

「快速开出角球……Origi！」

利物浦足球俱乐部在 2019 年欧洲冠军联赛半决赛中上演了历史性逆转。其中最具标志性的时刻之一，是 Trent Alexander-Arnold 的一记角球找到 Divock Origi 完成破门，这一球作为[利物浦足球俱乐部史上最伟大的进球](https://www.liverpoolfc.com/news/first-team/454462-corner-taken-quickly-origi-voted-liverpool-s-greatest-ever-goal)载入史册。

角球具有很高的进球潜力，但设计一套角球战术既依赖人类直觉，也依赖博弈设计，用以识别对手球队的模式并即时做出应对。

今天，我们在《Nature Communications》上发布 TacticAI：一个人工智能（AI）系统，能够通过预测式与生成式 AI 为专家提供战术洞见，尤其是在角球方面。尽管角球的黄金标准数据十分有限，TacticAI 仍通过几何深度学习方法取得了最先进的结果，帮助构建更具泛化能力的模型。

我们与利物浦足球俱乐部的专家共同开发并评估了 TacticAI，这是多年研究合作的一部分。人类专家评审在 90% 的情况下更青睐 TacticAI 的建议，而非实战中出现的战术布置。

TacticAI 展示了辅助型 AI 技术为球员、教练和球迷变革体育运动的潜力。足球等体育项目也是发展 AI 的动态领域，因为它们以真实世界的多智能体交互为特征，并伴随多模态数据。推进面向体育的 AI 可以转化为场上场下的许多领域——从电子游戏和[机器人技术](https://deepmind.google/blog/from-motor-control-to-embodied-intelligence/)，到交通协调。

![一幅示意图，说明 TacticAI 通过预测模型（「会发生什么？」）、嵌入/检索（「发生了什么？」）和引导式生成（「如何让它发生？」）来回答三个核心战术问题。](https://lh3.googleusercontent.com/S-Zqa29JwHj32RaAujqBAdPTIfDbxdr0Z4kiay85nqZRp2ULbiU9xSPAVq6TYYr83eNNwGQipwZuj4rBIhaFkLcqW41kN1zXkL6BxHLdtm3s3kNudXo=w1440)

TacticAI 是一套完整的 AI 系统，结合了预测模型与生成模型，用以分析以往比赛回合中发生了什么，以及如何做出调整以使特定结果更有可能发生。

## 与利物浦足球俱乐部共同制定比赛方案

五年前，我们开启了与利物浦足球俱乐部的多年合作，以推进面向体育分析的 AI。

我们的第一篇论文 [Game Plan](https://deepmind.google/blog/advancing-sports-analytics-through-ai-research/) 探讨了为什么应当用 AI 辅助足球战术，重点介绍了分析点球等例子。2022 年，我们开发了 [Graph Imputer](https://www.nature.com/articles/s41598-022-12547-0)，展示了 AI 如何作为一个预测系统原型用于足球分析中的下游任务。该系统可以在没有追踪数据的情况下预测镜头外球员的运动——否则俱乐部就需要派出球探亲临现场观看比赛。

如今，我们开发出了结合预测模型与生成模型的完整 AI 系统 TacticAI。我们的系统让教练能够为每个感兴趣的战术回合采样不同的球员布置方案，然后直接评估这些备选方案的可能结果。

TacticAI 旨在回答三个核心问题：

1. 对于给定的角球战术布置，会发生什么？例如，谁最有可能接到球，是否会出现射门尝试？
2. 在某个布置已经执行之后，我们能否理解发生了什么？例如，类似的战术在过去是否奏效？
3. 我们如何调整战术，使特定结果发生？例如，应当如何重新站位防守球员，以降低射门尝试的概率？

## 用几何深度学习预测角球结果

当球在触及防守方球员之后越出底线时，就会判给角球。预测角球结果十分复杂，原因在于单个球员比赛行为的随机性以及球员之间的动态互动。这对 AI 建模同样具有挑战性，因为可用的黄金标准角球数据很有限——英超每个赛季的每场比赛中大约只出现 10 次角球。

![上方是一个足球场，圆点连接成网络并有箭头指向另一个网络。下方是一个足球场，箭头通向四个较小的场地，这些场地连接到由蓝色箭头构成的网络。](https://lh3.googleusercontent.com/kLYJc6CiJFSnMUFwiy8pJ4PChxuU_iqpPFLjEt_teaqqaN-9cOeQ2iUfNnkTQ5XZs7zugryE80ggjqA55AIrbqJoyLwYmVHpcs54QxjjVybl2acjow=w1440)

（A）角球情境如何被转换为图表示。每名球员被视为图中的一个节点。图神经网络在该图上运行，通过消息传递更新每个节点的表示。

（B）TacticAI 如何处理给定的角球。所有四种可能的镜像翻转组合都被施加于该角球情境，并输入核心 TacticAI 模型。它们相互作用以计算最终的球员表示，这些表示可用于预测结果。

TacticAI 通过应用几何深度学习方法成功预测角球比赛过程。首先，我们通过将角球布置表示为图来直接建模球员之间的隐含关系，其中节点代表球员（带有位置、速度、身高等特征），边代表它们之间的关系。然后，我们利用足球场的一种近似对称性。我们的几何架构是[群等变卷积网络](https://proceedings.mlr.press/v48/cohenc16.pdf)（Group Equivariant Convolutional Network）的一个变体，它生成给定情境的全部四种可能镜像（原始、水平翻转、垂直翻转、水平垂直翻转），并强制我们的对接球者和射门尝试的预测在这四种镜像下完全一致。这种方法将神经网络可表示的可能函数的搜索空间缩小到尊重镜像对称的那些函数——并以更少的训练数据得到更具泛化能力的模型。

## 向人类专家提供建设性建议

借助其预测模型与生成模型，TacticAI 可以通过查找相似的角球和测试不同的战术来辅助教练。

传统上，为了制定战术与反制战术，分析师需要反复观看大量比赛视频，寻找相似案例并研究对手球队。TacticAI 自动计算球员的数值表示，使专家能够轻松高效地检索相关的历史回合。我们通过与足球专家开展大量定性研究进一步验证了这一直观观察：专家发现 TacticAI 的 top-1 检索结果有 63% 的情况下是相关的，几乎是基于直接分析球员位置相似性来推荐配对的方法所取得的 33% 基准的两倍。

TacticAI 的生成模型还允许人类教练重新设计角球战术，以优化某些结果的概率，例如在防守布置中降低射门尝试的概率。TacticAI 提供的战术建议会调整某一支球队所有球员的位置。从这些建议的调整中，教练可以更快地识别出重要模式，以及决定一项战术成败的关键球员。

![一幅四个象限的图像，其中三个象限是带有蓝色和红色圆圈的足球场俯视图，一个象限是柱状图。](https://lh3.googleusercontent.com/K5unXt_sDNeeouaR2MLYxvEEuYiNEks8N75RGiSK5io8dizGeM_JZ5aMVTJp0qkrxtRVWyLV-kX9sj-4fJ5tVApw_9paE4R1BTpN-tMdfqsG1mGfdSY=w1440-h810-n-nu)

（A）现实中确实发生了射门尝试的一次角球示例。

（B）TacticAI 可以生成一个反事实设定：通过调整防守球员的站位和速度，射门概率已被降低。

（C）建议的防守球员站位使进攻球员 2-4 的接球概率下降。

（D）该模型能够生成多个这样的场景，教练可以查看不同的选项。

在我们的定量分析中，我们表明 TacticAI 在预测角球接球者和射门情境上是准确的，且球员重新站位与真实比赛的展开方式相似。我们还通过一项盲测案例研究对这些建议进行了定性评估，评审者并不知道哪些战术来自真实比赛、哪些由 TacticAI 生成。来自利物浦足球俱乐部的人类足球专家发现，我们的建议无法与真实角球区分开来，并且在 90% 的情况下比原有情境更受青睐。这表明 TacticAI 的预测不仅准确，而且有用、可部署。

![一幅包含四对足球场的图像。一幅带有蓝色和红色圆圈，另一幅高亮显示移动了的圆圈。](https://lh3.googleusercontent.com/Rg6Zmt1Ne-5AMKwwlrZVo0cOjojmBi2mXdQpJndpJmoDYzTegrBDBjAE9cd8tqbWtpdt4O-dB5xAsRpBt8EI5eZf-F4K63KZThcAlhoSq8tUvZvcRVE=w1440-h810-n-nu)

评审者更青睐这些相对于原始比赛的战术改进示例，其中 TacticAI 建议：

（A）四名球员的建议获得大多数评审者的青睐。

（B）距离角球最远的防守球员做出更好的保护性跑位

（C）禁区内一群居中防守球员的保护性跑位得到改善

（D）两名居中防守球员的盯防跑位显著改善，另外两名防守球员在球门区域的站位也更好。

## 推进面向体育的 AI

TacticAI 是一套完整的 AI 系统，可以为教练提供即时、广泛且准确的战术洞见——并且在球场上切实可用。借助 TacticAI，我们开发了一个能力出众的足球战术 AI 助手，在开发有用的体育 AI 助手方面达成了一个里程碑。我们希望未来的研究能够帮助开发扩展到球员数据之外更多模态输入的助手，并以更多方式帮助专家。

我们展示了 AI 如何用于足球，但足球同样能教会我们很多关于 AI 的东西。这是一项高度动态、极具分析挑战的运动，包含从体能到心理的诸多人为因素。即便是经验丰富的教练这样的专家，也难以察觉所有模式。借助 TacticAI，我们希望积累许多经验，用于开发更广泛的辅助技术，融合人类专长与 AI 分析，在真实世界中帮助人们。

**进一步了解 TacticAI**

[阅读我们发表在 Nature Communications 上的论文](https://www.nature.com/articles/s41467-024-45965-x)

本项目是 Google DeepMind 团队与利物浦足球俱乐部之间的合作。TacticAI 的作者包括：Zhe Wang、Petar Veličković、Daniel Hennes、Nenad Tomašev、Laurel Prince、Michael Kaisers、Yoram Bachrach、Romuald Elie、Li Kevin Wenliang、Federico Piccinini、William Spearman、Ian Graham、Jerome Connor、Yi Yang、Adrià Recasens、Mina Khan、Nathalie Beauguerlange、Pablo Sprechmann、Pol Moreno、Nicolas Heess、Michael Bowling、Demis Hassabis 和 Karl Tuyls。
