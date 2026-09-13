---
title: "MuZero、AlphaZero 与 AlphaDev：优化计算机系统"
title_en: "MuZero, AlphaZero, and AlphaDev: Optimizing computer systems"
source: https://deepmind.google/blog/muzero-alphazero-and-alphadev-optimizing-computer-systems/
site: deepmind
date: 2023-06-12
crawled: 2026-09-13
translated: 2026-09-13
---

# MuZero、AlphaZero 与 AlphaDev：优化计算机系统

> 原文：[MuZero, AlphaZero, and AlphaDev: Optimizing computer systems](https://deepmind.google/blog/muzero-alphazero-and-alphadev-optimizing-computer-systems/) · Google DeepMind

作为我们构建能力日益强大、更加通用的人工智能（AI）系统这一目标的一部分，我们正在创造对世界具有更广泛理解的 AI 工具。这能让有用的知识在不同类型的任务之间迁移。

借助强化学习，我们的 AI 系统 AlphaZero 和 MuZero 在博弈中取得了超越人类的性能。此后，我们扩展了它们的能力，帮助设计更好的计算机芯片，同时优化数据中心和视频压缩。而我们的 AlphaZero 特化版本——AlphaDev——也在数字社会的根基之处发现了加速软件运行的新算法。

早期结果表明了更通用 AI 工具的变革性潜力。在这里，我们解释这些进展如何塑造计算的未来——并已经在帮助数十亿人和我们的星球。

![](https://lh3.googleusercontent.com/dzUtBJ3epFNS_8F38J-3fuK-mwCLWNNMbXjjxTCHUHbgOllAqj5npzEv9NHHyYGjPsYoldmvxxWNbdLAyKXKEeFyJZ_ZHC2wuEZJ_G1pq2bApFnDCQ=w1440-h810-n-nu)

## 设计更好的计算机芯片

专用硬件对于确保当今的 AI 系统在大规模用户场景下高效利用资源至关重要。但设计和生产新的计算机芯片可能需要多年的工作。

我们的研究人员开发了一种基于 AI 的方法来设计更强大、更高效的电路。通过把电路当作神经网络来处理，我们找到了加速芯片设计、把性能推向新高度的方法。

神经网络通常被设计为接收用户输入并生成输出，例如图像、文本或视频。在神经网络内部，边以图状结构连接到节点。

为了创建电路设计，我们的团队提出了「电路神经网络」（circuit neural networks）——一种新型神经网络，它把边变成导线，把节点变成逻辑门，并学习如何将它们连接起来。

![电路神经网络示意图，展示二进制电路输入如何经过三层由密集虚线网络连接的逻辑门隐藏层，产生电路输出。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/64be3d05d906a15808441b38_64b659c99dad7b8061b8a6f8_CHIP-_FIGX-5-01_goqZXL2.gif)

电路神经网络学习电路设计的动画示意图。它决定哪些边（导线）连接到哪些节点（逻辑门），以改进整体电路设计。

我们在保持电路功能的同时，针对计算速度、能效和尺寸对学到的电路进行了优化。利用「模拟退火」（simulated annealing）——一种向前看一步的经典搜索技术——我们还测试了不同的选项以找到最优配置。

凭借这项技术，我们赢得了 [IWLS 2023 编程竞赛](https://www.iwls.org/contest/)——在竞赛中 82% 的电路设计问题上取得最佳解决方案。

我们的团队还使用了能够向前看很多步的 AlphaZero，把这一挑战当作一个待解的博弈来改进电路设计。

到目前为止，我们结合电路神经网络与强化学习奖励函数的研究，已经展现出构建更先进计算机芯片的极佳前景。

![等距矢量插图，将 Google DeepMind 的 AI 系统——AlphaZero、MuZero 和 AlphaDev——描绘成计算机棋盘游戏上相互连接的彩色路径，其中包含棋子、视频帧、计算机芯片和游戏手柄等元素。](https://lh3.googleusercontent.com/kYbwB0FNBt9SlVGZ7OKUAKbz0Lms1tOlEjDuowkDzkKkId8rgUyvJlYUSHT4XwIvxrx_bniAmO3oWgeavhEQqKqfwnCGfMrAPuILMZEAkN0TCJlC=w1440)

## 优化数据中心资源

数据中心承担着从提供搜索结果到处理数据集的一切工作。一个名为 [Borg](https://storage.googleapis.com/pub-tools-public-publication-data/pdf/43438.pdf) 的系统像多维俄罗斯方块一样，管理和优化 Google 庞大数据中心内的工作负载。

为了调度任务，Borg 依赖人工编写的规则。但在 Google 的规模下，人工编写的规则无法覆盖不断变化的工作负载分布的多样性。因此这些规则被设计为「一刀切」，以尽量适配所有情况。

这正是 AlphaZero 这类机器学习技术尤为有用的地方：它们能够大规模工作，自动创建针对各种工作负载分布量身定制、达到最优的单独规则。

在训练过程中，AlphaZero 学会了识别进入数据中心的任务中的模式，还学会了预测管理容量的最佳方式，做出具有最佳长期结果的决策。

当我们在实验性试验中将 AlphaZero 应用于 Borg 时，我们发现可以将数据中心中未充分利用的硬件比例降低最多 19%。

![等距矢量插图并排比较数据中心优化效果：一个干净、空置的蓝色线框立方体标注为「已优化」，旁边是一个同样式线框立方体标注为「未优化」，里面杂乱堆放着各种色彩斑斓、无序的 3D 方块。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/64807c135294d98635791646_6464c6b5be889dc90e670f40_Figure202.gif)

整齐、经过优化的数据存储与杂乱、未经优化的存储的动画可视化对比。

## 高效压缩视频

视频流占据了互联网流量的大部分。因此，找到让流媒体更高效的方法——无论改进大小——都将对每天观看视频的数百万人产生巨大影响。

我们与 YouTube 合作，利用 MuZero 的问题解决能力来压缩和传输视频。[通过将码率降低 4%，MuZero 改善了 YouTube 的整体体验](https://www.deepmind.com/blog/muzeros-first-step-from-research-into-the-real-world)——同时不损害视觉质量。

我们最初应用 MuZero 来优化每个单独视频帧的压缩。现在，我们扩展了这项工作，帮助决策帧在编码过程中如何分组和引用，从而带来更多码率节省。

前两步的结果表明，MuZero 有潜力成为更泛化的工具，帮助在整个视频压缩流程中找到最优解决方案。

![一幅抽象的白线图，展示视频帧被分组和压缩的一系列步骤，说明 MuZero 的视频压缩过程。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/64807c135294d9863579165c_6464ba81cad8de9f10319887_Copy20of20Figure1.gif)

一幅可视化图，演示 MuZero 如何压缩视频文件。它定义视觉上相似的画面组（group of pictures）进行压缩。单个关键帧先被压缩。随后 MuZero 以关键帧为参考压缩其他帧。这一过程在视频其余部分反复进行，直到压缩完成。

## 发现更快的算法

[AlphaDev](https://www.deepmind.com/blog/alphadev-discovers-faster-sorting-algorithms) 是 AlphaZero 的一个版本，当它发现更快的排序（sorting）和哈希（hashing）算法时，在计算机科学上取得了新颖的突破。这些基础过程每天被使用数万亿次，用于排序、存储和检索数据。

**AlphaDev 的排序算法**

排序算法帮助数字设备处理和显示信息，从在线搜索结果和社交帖子的排名，到用户推荐。

与 C++ 库中的算法相比，AlphaDev 发现的算法将对短序列元素排序的效率提高了 70%，对超过 25 万个元素的序列提高了约 1.7%。这意味着用户查询产生的结果可以更快地完成排序。在大规模使用时，这节省了大量的时间和能源。

**AlphaDev 的哈希算法**

哈希算法常用于数据存储和检索，例如在客户数据库中。它们通常使用一个键（例如用户名「Jane Doe」）生成一个唯一的哈希值，该值对应需要检索的数据（例如「订单号 164335-87」）。

就像图书馆员利用分类系统快速找到特定书籍一样，在哈希系统中，计算机已经知道自己在找什么、去哪里找。当应用于数据中心的 9–16 字节范围的哈希函数时，AlphaDev 的算法将效率提升了 30%。

**这些算法的影响**

我们将排序算法添加到 [LLVM 标准 C++ 库](https://reviews.llvm.org/D118029)中——替换了沿用十多年的子例程。并将 AlphaDev 的哈希算法贡献给了 [abseil 库](https://abseil.io/docs/cpp/guides/hash)。

从那时起，数百万开发者和公司开始在云计算、在线购物和供应链管理等各行各业使用这些算法。

![一幅绿、紫、黑三色渐变的等距矢量插图，描绘一个中央计算立方体，通过一条蜿蜒的电路板式轨道连接到四个玻璃球体，分别代表技术优化的不同领域：一座房子、一辆自动驾驶汽车、一道代表能源的闪电，以及一颗带心电图线的爱心。](https://lh3.googleusercontent.com/SOV2QO8AGpIp8ph-GvybvqXj6HF1IIhHEcu68BMD6zCub9YGMkJxG6pdTvQDbl0r4zMfbFXRo9S_18XabydvzkTimT8Q8xaKW3dYu883_9ru6m8Upg=w1440)

## 为我们的数字未来提供动力的通用工具

我们的 AI 工具已经在为数十亿人节省时间和能源。这只是开始。我们展望这样一个未来：通用 AI 工具能够帮助优化全球计算生态。

我们尚未抵达那里——我们仍然需要更快、更高效、更可持续的数字基础设施。

要创建完全泛化的 AI 工具，还需要更多的理论与技术突破。但这些工具的潜力——遍及技术、科学和医学——让我们对未来充满期待。

**进一步了解 AlphaDev**

[阅读论文](https://www.nature.com/articles/s41586-023-06004-9)
