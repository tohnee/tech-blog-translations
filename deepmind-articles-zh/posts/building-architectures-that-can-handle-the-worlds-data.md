---
title: "构建能够处理世界各类数据的架构"
title_en: "Building architectures that can handle the world’s data"
source: https://deepmind.google/blog/building-architectures-that-can-handle-the-worlds-data/
site: deepmind
date: 2021-08-03
crawled: 2026-09-13
translated: 2026-09-13
---

# 构建能够处理世界各类数据的架构

> 原文：[Building architectures that can handle the world’s data](https://deepmind.google/blog/building-architectures-that-can-handle-the-worlds-data/) · Google DeepMind

Perceiver 与 Perceiver IO 是 AI 领域的多用途工具。

如今 AI 系统使用的大多数架构都是专才。2D 残差网络或许是处理图像的好选择，但对于其他类型的数据——例如自动驾驶汽车使用的激光雷达信号，或机器人学中使用的力矩——它充其量只能勉强适配。更糟的是，标准架构往往只为单一任务而设计，这常常迫使工程师们费尽心思对输入输出进行重塑、变形或其他修改，指望标准架构能够学会正确处理他们的问题。而要处理不止一种数据——比如构成视频的声音和图像——就更加复杂了，即便对于简单任务，通常也需要由许多不同部件组成的复杂且经过手工调优的系统。作为 DeepMind「通过解决智能来推进科学与造福人类」使命的一部分，我们希望构建能够解决使用多种输入输出类型问题的系统，因此我们开始探索一种更通用、更多能、可以处理所有类型数据的架构。

![Perceiver IO 架构示意图：展示从输入数组经过编码、处理、解码模块最终到达输出数组的流程，其中利用了潜在数组与输出查询数组。](https://lh3.googleusercontent.com/KcLLFZfiq3COmFqB6qd__g_YOdmKQ-qvCmKmRlo2FnYuUpuC0Jbi_t3hrSApqScKKjSvQLD7EH82RrsOXfvkMqUesXWF_jON_FyXc8fRktnX70KbDQ=w1440)

图 1. Perceiver IO 架构借助一个较小的潜在数组将输入数组映射为输出数组，这使其即便面对非常庞大的输入和输出也能从容扩展。Perceiver IO 使用一种可泛化到多种不同类型数据的全局注意力机制。

在 [ICML 2021](https://icml.cc/)（国际机器学习会议）上发表并在 [arXiv 上以预印本形式发布](https://arxiv.org/abs/2103.03206)的一篇论文中，我们提出了 Perceiver——一种能够处理图像、点云、音频、视频及其组合数据的通用架构。虽然 Perceiver 能够处理多种输入数据，但它仅限于分类这类输出简单的任务。一篇[新的 arXiv 预印本](https://arxiv.org/abs/2107.14795)介绍了 Perceiver IO，它是 Perceiver 架构更通用的版本。Perceiver IO 能够从多种不同输入生成种类繁多的输出，使其适用于语言、视觉、多模态理解以及《星际争霸 II》（StarCraft II）等高难度游戏等现实世界领域。为帮助研究者及整个机器学习社区，我们现已[开源了代码](https://github.com/deepmind/deepmind-research/tree/master/perceiver)。

![文本分析示例图：按"局部"、"周期性"和"句法元素"分类，通过对一个关于熊的笑话中的不同单词和标点符号进行高亮，展示模型的注意力模式。](https://lh3.googleusercontent.com/IgHvJn3pfIBpwwOwyar4dt4CTibzoLHEiBygEJ79F2bmVTakSB5VLKNE9Wj9DQvDy15OdoH2XQT96LBecuvPksYmifvahUsUxF9AhUwYQrapxmpQ=w1440)

图 2. Perceiver IO 处理语言时首先选择要关注哪些字符。该模型学会使用几种不同的策略：网络中有些部分关注输入中的特定位置，而另一些部分则关注标点符号等特定字符。

Perceiver 建立在 [Transformer](https://en.wikipedia.org/wiki/Transformer_(machine_learning_model)) 之上。Transformer 是一种使用「注意力」操作将输入映射为输出的架构。通过比较输入的所有元素，Transformer 会依据元素之间以及元素与任务之间的关系来处理输入。注意力机制简单且适用广泛，但 Transformer 使用注意力的方式会随着输入数量的增长而迅速变得昂贵。这意味着 Transformer 适用于最多几千个元素的输入，而图像、视频和书籍等常见数据形式很容易包含数百万个元素。在最初的 Perceiver 中，我们解决了通用架构面临的一个重大难题：将 Transformer 的注意力操作扩展到非常庞大的输入，同时不引入任何领域特定的假设。Perceiver 的做法是先用注意力将输入编码为一个较小的潜在数组，随后对该潜在数组的进一步处理，其代价与输入大小无关。这使得 Perceiver 的内存与计算需求能够随输入增大而从容增长，即便对于特别深的模型也是如此。

![动态分屏对比：上方面板显示现实生活中工人在传送带上搬运甘蔗茎，下方面板显示 Perceiver IO 模型的光流可视化，用彩虹色系追踪相同元素的运动，颜色代表画面中每个点的运动方向。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/fig_3a.gif)

![动态分屏对比：上方面板显示一位女士在广场上走过一群四散的鸽子，下方面板显示 Perceiver IO 模型的光流可视化，用鲜艳的色彩追踪这位女士和每只飞鸟的运动，颜色代表它们的运动方向。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/fig_3b.gif)

![动态分屏对比：上方面板显示一群身着传统服饰的舞者在寺庙前进行仪式表演，下方面板显示 Perceiver IO 模型的光流可视化，用鲜艳的色彩追踪每位舞者的运动，颜色代表其运动方向。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/fig_3c.gif)

![示意图：彩色箭头从中心点向外指，形成一个圆形色轮，表示光流可视化中运动方向与颜色的映射关系。](https://lh3.googleusercontent.com/vct_DvboFWGKkNH8DDC38drvFect9ZFV-ikay93ChPTURa0_4hBI_4XSwNiUGtNFXnxpUAWlhFOfiJka0JOXe9W6SYYEbcLpCL5as_dwa7VftxbxWiY=w1440)

图 3. Perceiver IO 在光流估计这一极具挑战性的任务上取得了最先进的结果——光流估计即追踪图像中所有像素的运动。每个像素的颜色表示 Perceiver IO 估计出的运动方向与速度，如上方图例所示。

这种「从容扩展」的能力使 Perceiver 达到了前所未有的通用程度——它在基于图像、3D 点云以及音频加图像的基准测试上与领域专用模型不相上下。但由于最初的 Perceiver 对每个输入只能产生一个输出，它并不像研究者需要的那么多能。Perceiver IO 解决了这个问题：它不仅用注意力编码到潜在数组，还用注意力从潜在数组解码，这赋予了网络极大的灵活性。Perceiver IO 现在可以扩展到庞大而多样的输入和输出，甚至能同时处理多个任务或多种类型的数据。这为各类应用敞开了大门，例如从文本的每个字符理解文本含义、追踪图像中所有点的运动、处理构成视频的声音、图像和标签，甚至玩游戏——而这一切都只使用一个比替代方案更简单的架构。

原始画面

Perceiver IO

原始画面

Perceiver IO

原始画面

Perceiver IO

在实验中，我们看到 Perceiver IO 在语言、视觉、多模态数据和游戏等众多基准领域中都行之有效，为处理多种类型的数据提供了一种开箱即用的方式。希望[我们最新的预印本](https://arxiv.org/abs/2107.14795)和 [GitHub 上提供的代码](https://github.com/deepmind/deepmind-research/tree/master/perceiver)能帮助研究者和从业者解决问题，而无需投入大量时间和精力、借助专用系统构建定制化方案。随着我们继续从探索新型数据中学习，我们期待进一步改进这一通用架构，让解决科学与机器学习领域的问题变得更快、更容易。
