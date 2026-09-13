---
title: "用 AlphaTensor 发现新算法"
title_en: "Discovering novel algorithms with AlphaTensor"
source: https://deepmind.google/blog/discovering-novel-algorithms-with-alphatensor/
site: deepmind
date: 2022-10-05
crawled: 2026-09-13
translated: 2026-09-13
---

# 用 AlphaTensor 发现新算法

> 原文：[Discovering novel algorithms with AlphaTensor](https://deepmind.google/blog/discovering-novel-algorithms-with-alphatensor/) · Google DeepMind

AlphaZero 首次拓展到数学领域，为研究开启新的可能

数千年来，算法一直在帮助数学家完成基本运算。古埃及人创造了一种不需要乘法表就能把两个数相乘的算法；希腊数学家欧几里得（Euclid）描述了一种计算最大公约数的算法，至今仍在使用。

在伊斯兰黄金时代，波斯数学家[花拉子米（Muhammad ibn Musa al-Khwarizmi）](https://en.wikipedia.org/wiki/Muhammad_ibn_Musa_al-Khwarizmi)设计了解线性方程与二次方程的新算法。事实上，花拉子米的名字转写为拉丁文"Algoritmi"，正是"算法"（algorithm）一词的来源。然而，尽管如今算法已为人们所熟悉——从课堂代数到前沿科学研究，整个社会无处不在——发现新算法的过程却极其困难，它是人类思维惊人推理能力的一个例证。

在今天发表于《自然》（Nature）的[论文](https://www.nature.com/articles/s41586-022-05172-4)中，我们介绍了 AlphaTensor：第一个能为矩阵乘法等基本任务发现新颖、高效且可证明正确的算法的人工智能（AI）系统。这为数学中一个悬置 50 年的开放性问题——寻找两个矩阵相乘的最快方法——带来了新的曙光。

这篇论文是 DeepMind 使命中垫下的一块基石：推进科学进步，用 AI 攻克最根本的问题。我们的系统 AlphaTensor 构建在 AlphaZero 之上——后者是一个在国际象棋、围棋、将棋等棋盘游戏中展现出超人表现的智能体。这项工作展示了 AlphaZero 从下棋到首次攻克未解数学问题的历程。

## 矩阵乘法

矩阵乘法是代数中最简单的运算之一，通常在高中数学课上就会讲授。但在课堂之外，这个看似朴素的数学运算对当代数字世界影响巨大，在现代计算中无处不在。

![一张示意图，展示两个 3x3 矩阵的乘法，高亮显示第一个矩阵的一行与第二个矩阵的一列的点积，用以计算结果矩阵中的一个元素。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/633c31b866f7323281c5adaf_633c1c9aaaf084ffbeed2333_MM_Fig1.svg)

两个 3x3 矩阵相乘过程的示例。

这一运算被用于在智能手机上处理图像、识别语音指令、为电脑游戏生成图形、运行天气预报模拟、压缩数据和视频以便在互联网上分享等等，不一而足。世界各地的公司投入大量时间和金钱开发能够高效进行矩阵乘法的计算硬件。因此，哪怕是对矩阵乘法效率的微小改进，都可能产生广泛的影响。

几个世纪以来，数学家们一直认为标准矩阵乘法算法就是效率上所能达到的最优。但在 1969 年，德国数学家 Volker Strassen [震惊了数学界](https://link.springer.com/article/10.1007/BF02165411)：他证明了确实存在更好的算法。

![一幅并排对比图，说明如何用标准算法（需要 8 次乘法，h1 到 h8）与 Strassen 算法（通过巧妙组合矩阵元素，将过程减少到 7 次乘法，h1 到 h7）计算两个 2x2 矩阵的乘积。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/633c31b82381e038cc3a90ea_633c1d0f5ed3f701034748c5_MM_Fig2.svg)

标准算法与 Strassen 算法的对比：后者在计算 2x2 矩阵乘法时少用一次标量乘法（7 次而非 8 次）。乘法次数对整体效率的影响远大于加法。

通过研究非常小的矩阵（2x2 大小），他发现了一种巧妙的矩阵元素组合方式，得到了更快的算法。尽管 Strassen 的突破之后有数十年的研究，这一问题的更大规模版本仍未解决——以至于就连两个 3x3 矩阵相乘最高能做到多高效，人们也一无所知。

在论文中，我们探索了现代 AI 技术如何推进矩阵乘法新算法的自动发现。在人类直觉的基础上更进一步，AlphaTensor 为许多矩阵尺寸发现了比当前最优方法更高效的算法。我们由 AI 设计的算法超越了人类设计的算法，这是算法发现领域的一大步。

## 自动化算法发现的流程与进展

首先，我们把寻找矩阵乘法高效算法的问题转化为一个单人游戏。在这个游戏中，棋盘是一个三维张量（数字数组），刻画当前算法距离正确的程度。玩家通过一组允许的移动——对应算法指令——尝试修改张量，把它的元素清零。当玩家成功做到这一点时，就得到一个对任意矩阵对都可证明正确的矩阵乘法算法，其效率由清零张量所需的步数决定。

这个游戏极具挑战性——即便对于矩阵乘法的小规模情形，需要考虑的可能算法数量也远超宇宙中的原子总数。与围棋相比——围棋曾[让 AI 困惑了几十年](https://www.deepmind.com/research/highlighted-research/alphago)——我们的游戏在每一步的可能移动数量比围棋大 30 个数量级（在我们考虑的某个设定下超过 10 的 33 次方）。

从本质上讲，要想玩好这个游戏，就得在一个由无数可能组成的巨型干草堆里找出最细小的针。为应对这一与传统棋类游戏截然不同的领域的挑战，我们开发了多个关键组件，包括一个融入了针对问题的归纳偏置（inductive bias）的新型神经网络架构、一个生成有用合成数据的过程，以及一个利用问题对称性的配方。

然后，我们用强化学习训练了一个 AlphaTensor 智能体来玩这个游戏，起点是对现有矩阵乘法算法一无所知。通过学习，AlphaTensor 随时间不断进步，重新发现了 Strassen 算法等历史上的快速矩阵乘法算法，最终超越了人类直觉的疆域，发现了比已知更快的算法。

![示意图，展示 AlphaTensor 逐步的强化学习循环：智能体修改代表当前算法状态的三维张量网格，以发现新算法。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/633c31b879d44219c89ee786_633c1dbed481f1536ecc0ad1_MM_Fig3.svg)

AlphaTensor 玩的单人游戏，目标是找到一个正确的矩阵乘法算法。游戏状态是一个立方体状的数字阵列（0 显示为灰色、1 为蓝色、-1 为绿色），代表尚待完成的工作。

举例来说，如果学校里教的传统算法用 100 次乘法计算一个 4x5 矩阵与一个 5x5 矩阵的乘积，而人类的智慧把这个数字降到了 80，那么 AlphaTensor 找到的算法只需 76 次乘法即可完成同样的运算。

![一幅示意图，展示 AlphaTensor 计算 4x5 矩阵乘 5x5 矩阵的 76 步算法，列出因子 h1 到 h76 的公式以及结果矩阵 C 的各元素。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/633c31b8194b542332281409_633c1e36d481f1811ccc110b_MM_Fig4.svg)

AlphaTensor 发现的使用 76 次乘法的算法，是对当前最优算法的改进。

除了这个例子，AlphaTensor 的算法还首次改进了 Strassen 的有限域两级算法——自 50 年前问世以来的第一次。这些用于小型矩阵乘法的算法可以作为基本构件，用于计算任意尺寸的大得多的矩阵。

此外，AlphaTensor 还发现了一组具有最优复杂度的多样算法——每种矩阵尺寸下最多可达数千个矩阵乘法算法，这表明矩阵乘法算法的空间比以往认为的更加丰富。

这一丰富空间中的算法具有不同的数学与实践特性。借助这种多样性，我们对 AlphaTensor 进行了改造，使其专门寻找在特定硬件上运行快速的算法，例如 Nvidia V100 GPU 和 Google TPU v2。这些算法在相同硬件上进行大型矩阵乘法时，比常用算法快 10-20%，展示了 AlphaTensor 在优化任意目标方面的灵活性。

![一张流程图，说明 AlphaTensor 如何设计新的定制算法。一个代表矩阵乘法的初始"问题规格"（Problem specification）输入"AlphaTensor"系统。一条双向箭头表示 AlphaTensor 对硬件拥有"黑盒访问权限"（Black box access to hardware，以 GPU 图标示意）。这一过程产出"新的定制算法"（New tailored algorithm），以蓝色网格显示。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/633c31b82381e06d7f3a90e9_633c1e777cc74cc57c3960c3_MM_V4.svg)

AlphaTensor 以算法运行时间为目标。当发现一个正确的矩阵乘法算法后，会在目标硬件上进行基准测试，结果再反馈给 AlphaTensor，以便它在目标硬件上学出更高效的算法。

## 探索对未来研究与应用的影响

从数学角度来看，我们的结果可以引导复杂性理论的进一步研究——该领域旨在确定求解计算问题的最快算法。通过以比以往方法更有效的方式探索可能算法的空间，AlphaTensor 帮助加深了我们对矩阵乘法算法丰富性的理解。理解这一空间或许能带来新的成果，帮助确定矩阵乘法的渐近复杂度——这是[计算机科学中最根本的开放性问题之一](https://www.cambridge.org/core/books/geometry-and-complexity-theory/15E3ABA3FF14E1054574663F60250D80#fndtn-information)。

由于矩阵乘法是许多计算任务的核心组件——涵盖计算机图形学、数字通信、神经网络训练和科学计算——AlphaTensor 发现的算法可以让这些领域的计算显著更加高效。AlphaTensor 考虑任意目标的灵活性还可能催生新的应用，例如设计能够优化能耗和数值稳定性等指标的算法，帮助防止小的舍入误差随着算法运行而滚雪球般放大。

虽然我们在这里聚焦于矩阵乘法这一特定问题，但我们希望我们的论文能激励其他人用 AI 引导其他基本计算任务的算法发现。我们的研究还表明，AlphaZero 是一个强大的算法，可以远超传统棋类的领域加以拓展，帮助解决数学中的开放性问题。在我们的研究之上，我们希望推动更多工作涌现——用 AI 帮助社会解决数学以及各科学领域一些最重要的挑战。

你可以在 [AlphaTensor 的 GitHub 仓库](https://github.com/deepmind/alphatensor)找到更多信息。

**致谢**

感谢 Francisco R. Ruiz、Thomas Hubert、Alexander Novikov、Alex Gaunt 对本文的反馈。感谢 Sean Carlson、Arielle Bier、Gabriella Pearl、Katie McAtackney、Max Barnett 在文本与图表方面的帮助。这项工作由以下贡献者组成的团队完成：Alhussein Fawzi、Matej Balog、Aja Huang、Thomas Hubert、Bernardino Romera-Paredes、Mohammadamin Barekatain、Francisco Ruiz、Alexander Novikov、Julian Schrittwieser、Grzegorz Swirszcz、David Silver、Demis Hassabis 与 Pushmeet Kohli。
