---
title: "AlphaDev 发现更快的排序算法"
title_en: "AlphaDev discovers faster sorting algorithms"
source: https://deepmind.google/blog/alphadev-discovers-faster-sorting-algorithms/
site: deepmind
date: 2023-06-07
crawled: 2026-09-13
translated: 2026-09-13
---

# AlphaDev 发现更快的排序算法

> 原文：[AlphaDev discovers faster sorting algorithms](https://deepmind.google/blog/alphadev-discovers-faster-sorting-algorithms/) · Google DeepMind

新算法将改变计算的根基

数字社会正推动对计算与能源使用的需求不断增长。在过去五十年里，我们依靠硬件的进步来跟上这一步伐。但随着微芯片逼近其物理极限，改进其上运行的代码、让计算更强大更可持续就变得至关重要。这对那些每天被运行数万亿次的代码所组成的算法尤为重要。

在今天[发表于《自然》（Nature）杂志的论文](https://www.nature.com/articles/s41586-023-06004-9)中，我们介绍了 AlphaDev——一个人工智能（AI）系统，它利用强化学习发现了改进的计算机科学算法——超越了科学家和工程师数十年来打磨出的算法。

AlphaDev 发现了一个更快的排序（sorting）算法——一种为数据排序的方法。数十亿人每天都在使用这些算法而不自知。它们支撑着一切：从在线搜索结果和社交帖子的排名，到数据在计算机和手机上的处理方式。用 AI 生成更好的算法将改变我们编写计算机程序的方式，并影响我们日益数字化的社会的方方面面。

通过在[主流 C++ 库](https://reviews.llvm.org/D118029)中开源我们的新排序算法，世界各地数百万开发者和公司如今在从云计算、在线购物到供应链管理等各种行业的 AI 应用中使用它。这是该排序库的这一部分十多年来首次被改动，也是通过强化学习设计的算法首次被加入这个库。我们认为这是用 AI 优化世界代码的重要基石——一次一个算法。

## 什么是排序？

排序是一种把若干条目按特定顺序组织起来的方法。例如把三个字母按字母顺序排列、把五个数字从大到小排列，或者为一个包含数百万条记录的数据库排序。

这一方法在历史长河中不断演进。最早的例子之一可以追溯到公元二三世纪，当时学者们在亚历山大图书馆的书架上手工按字母顺序排列数千本书。工业革命之后，出现了能协助排序的机器——制表机将信息存储在打孔卡上，这些卡片曾被用来收集 1890 年美国的人口普查结果。

随着 20 世纪 50 年代商用计算机的兴起，最早的计算机科学排序算法相继诞生。如今，世界上有许多不同的排序技术与算法，被世界各地的代码库用来组织网上的海量数据。

![排序算法示意图：顶部显示一个未排序的数字序列（4, 3, 5, 2, 1），经过「排序算法」模块处理，底部输出已排序的序列（1, 2, 3, 4, 5）。](https://lh3.googleusercontent.com/lNngdizI2q5HMkV-A3v8DQOLE5a9Z3fZXW4FbtVOCUhMaYAVc-W_q1MTLpVS-MktAEsRRt33IkQUAyloMnHtqSCkNoWWnYBWhV0InNW7MKguBN9qHs8=w1440)

排序算法功能示意图。一列未排序的数字输入算法，输出排好序的数字。

当代算法凝聚了计算机科学家和程序员数十年的研究。它们已经如此高效，以至于进一步改进都是重大挑战，类似于寻找一种新的省电方法或一种更高效的数学方法。这些算法也是计算机科学的基石，在各大学的计算机科学入门课程中讲授。

## 寻找新算法

AlphaDev 从零开始发现更快的算法，而不是在现有算法上打磨，并且从大多数人类不看的地方入手：计算机的汇编指令。

汇编指令用于创建计算机执行所需的二进制代码。虽然开发者使用 C++ 等编码语言（即所谓高级语言）编写代码，但这些代码必须被翻译成「低级」汇编指令计算机才能理解。

我们相信，在这个更低的层次上存在许多改进空间，只是在更高级的编码语言中难以发现。计算机的存储和操作在这一层次更为灵活，这意味着潜在改进要多得多，并且可能对速度和能源使用产生更大影响。

![示意图展示 C++ 代码如何被编译器翻译为低级 CPU 指令（称为汇编指令），然后汇编器将汇编指令翻译成可执行的机器代码。](https://lh3.googleusercontent.com/eMBEbiz5ba2pmgemuRWSy3hp3Eb8a84fHmjmDTVg7pUyX5NQiuXYlH6jyxpOkzyynVK-80KnUMzjFg6InLieY9N-QKwPluvclVdTRCaE-y_Xzm1t=w1440)

代码通常用 C++ 这样的高级编程语言编写。随后通过编译器将其翻译为低级 CPU 指令，即汇编指令。汇编器再把汇编指令转换为计算机可以运行的可执行机器代码。

![标有 A 和 B 的两个方框并排展示代码示例。方框 A 左侧是一个 C++ 算法，方框 B 右侧是相应代码的汇编表示。](https://lh3.googleusercontent.com/vpnsK5UdJuoL_cVBZ1tkhAqQZrOihleupeSQmUUyOZzqqFBErfPaehyRjM-g28Bpi1snytEALtnal2VNdc-NEAPfL__IdUKCSlRFACkGKFgZw7Dx8Q=w1440)

**图 A：** 一个最多对两个元素排序的 C++ 算法示例。
**图 B：** 相应代码的汇编表示。

## 用博弈寻找最佳算法

AlphaDev 基于 [AlphaZero](https://deepmind.google/blog/alphazero-shedding-new-light-on-chess-shogi-and-go/)——我们的强化学习模型，曾在围棋、国际象棋和将棋等博弈中击败世界冠军。借助 AlphaDev，我们展示了这个模型如何从博弈迁移到科学挑战，从仿真迁移到真实世界的应用。

为了训练 AlphaDev 发现新算法，我们把排序转化为一个单人「汇编博弈」。每一轮，AlphaDev 观察它已生成的算法和中央处理器（CPU）中包含的信息，然后通过选择一条指令加入算法来走出一步。

这个汇编博弈极其困难，因为 AlphaDev 必须在数量巨大的指令组合中高效搜索，找到一个能够完成排序且比当前最佳算法更快的算法。可能的指令组合数量类似于宇宙中的粒子数量，或国际象棋（10^120 局）和围棋（10^700 局）中可能的着法组合数量。而且一步走错就可能使整个算法失效。

![上下两幅图。图 A 展示汇编博弈，图 B 展示奖励计算。](https://lh3.googleusercontent.com/l9DsK6OrSa0T6EtIFlDkINtRCt8lJ9A6dhpKo6dELmVBOWB3lfuwrvma2XrlnWGg7CrdXxmgRIvcw_6dfTDSBvcuc3_wMbTtnuWGCEaA5LL_zmY2o3A=w1440)

**图 A：** 汇编博弈。玩家 AlphaDev 接收系统状态 st 作为输入，通过选择一条汇编指令加入目前生成的算法，走出一步 at。
**图 B：** 奖励计算。每走一步之后，生成的算法被输入测试序列——对 sort3 而言，这对应三个元素序列的所有组合。算法随后生成一个输出，在排序任务中与排序后序列的期望输出进行比较。智能体根据算法的正确性和延迟获得奖励。

随着算法一条指令一条指令地构建，AlphaDev 通过将算法输出与期望结果进行比较来检验其正确性。对排序算法而言，这意味着无序的数字进去，正确排序的数字出来。我们既奖励 AlphaDev 正确排序数字，也奖励它排序的速度与效率。AlphaDev 通过发现一个正确且更快的程序赢得博弈。

## 发现更快的排序算法

AlphaDev 发现的新排序算法带来了 LLVM libc++ 排序库的改进：对较短的序列最高快 70%，对超过 25 万个元素的序列快约 1.7%。

我们专注于改进针对三到五个元素的短序列排序算法。这些算法属于应用最广泛的算法之列，因为它们往往作为更大排序函数的一部分被调用很多次。改进这些算法可以为对任意数量条目的排序带来整体加速。

为了让新排序算法更便于人们使用，我们对算法进行了逆向工程，并将其翻译为 C++——开发者最常用的编程语言之一。这些算法现已在 [LLVM libc++ 标准排序库](https://reviews.llvm.org/D118029)中提供，供世界各地数百万开发者和公司使用。

## 发现新颖的方法

AlphaDev 不仅找到了更快的算法，还发现了新颖的方法。它的排序算法包含新的指令序列，每次应用时都能省下一条指令。由于这些算法每天被使用数万亿次，这可以产生巨大的影响。

我们把这些称为「AlphaDev 交换与复制妙手（swap and copy moves）」。这种新颖的方法让人想起 AlphaGo 的「第 37 手」——那一步反直觉的落子震惊了旁观者，并导致一位传奇围棋棋手的落败。通过交换与复制妙手，AlphaDev 跳过了一个步骤，以一种看似错误、实则是捷径的方式连接条目。这展示了 AlphaDev 发掘原创解法的能力，也挑战了我们关于如何改进计算机科学算法的思维方式。

![两栏文字。左栏标题为「original（原始）」，三行以红色高亮，显示 min(A,B,C)。右栏标题为「AlphaDev」，两行以绿色高亮，显示 min(A,B)。](https://lh3.googleusercontent.com/KIlpvSshToNTlsEHt3coNI0qFbvYwbMeyXdDX-bczboGN3oJdqysJ2LYuwlPm55xjqWWpvZTn3-Ktq2eKGw1sB3uU6rOIlIEIBw1qV7f8tS9qEC4oA=w1440)

**左：** 使用 min(A,B,C) 的原始实现。
**右：** AlphaDev 交换妙手——AlphaDev 发现只需要 min(A,B)。

![两栏文字。左栏标题为「original（原始）」，五行以红色高亮，显示 max(B, min(A, C, D))。右栏标题为「AlphaDev」，四行以绿色高亮，显示 max(B, min(A, C))。](https://lh3.googleusercontent.com/3alYfJn_hvQApQC4iYBR3cziQorzdkBipsOQ7fSRWD8qMzMTVzMnONVF_DbgdAnRRr3YBqfTOw6QZI7-b4LHGdWShKxCD1YpvZiKIX4BObndPSdi1g=w1440)

**左：** 在一个对八个元素排序的更大排序算法中使用的 max(B, min(A, C, D)) 原始实现。
**右：** AlphaDev 发现，使用其复制妙手时只需要 max(B, min(A, C))。

## 从排序到数据结构中的哈希

在发现更快的排序算法之后，我们测试了 AlphaDev 是否能泛化并改进另一种计算机科学算法：哈希（hashing）。

哈希是计算中的一类基础算法，用于检索、存储和压缩数据。就像图书馆员利用分类系统定位某本书一样，哈希算法帮助用户知道自己在找什么、以及确切能在哪里找到它。这些算法接收特定键的数据（例如用户名「Jane Doe」）并对其进行哈希——一个把原始数据变成唯一字符串（例如 1234ghfty）的过程。计算机利用这个哈希值快速检索与该键相关的数据，而不必搜索全部数据。

我们将 AlphaDev 应用于数据结构中最常用的哈希算法之一，试图发现更快的算法。当把它应用于哈希函数的 9–16 字节范围时，AlphaDev 发现的算法快了 30%。

今年，AlphaDev 的新哈希算法已发布到开源的 [Abseil 库](https://github.com/abseil/abseil-cpp/commit/74eee2aff683cc7dcd2dbaa69b2c654596d8024e)，供全球数百万开发者使用，我们估计它现在每天被使用数万亿次。

## 一次一个算法，优化世界的代码

通过优化并发布世界各地开发者使用的改进版排序与哈希算法，AlphaDev 展示了其泛化并发现有真实世界影响的新算法的能力。我们将 AlphaDev 视为开发通用 AI 工具道路上的一步——这类工具可以帮助优化整个计算生态，并解决其他有利于社会的问题。

虽然在低级汇编指令空间中进行优化非常强大，但随着算法规模增长存在局限，我们目前正在探索 AlphaDev 直接在 C++ 等高级语言中优化算法的能力，这对开发者而言会更有用。

AlphaDev 的发现——例如交换与复制妙手——不仅表明它能改进算法，还能找到新的解法。我们希望这些发现能激励研究者和开发者创造能够进一步优化基础算法的技术与方法，共同构建一个更强大、更可持续的计算生态。

**致谢**

感谢 Juanita Bawagan、Arielle Bier、Gabriella Pearl、Duncan Smith、Katie McAtackney、Kathryn Seager、Max Barnett、Ross West、Dominic Barlow、Hollie Dobson、Domhnall Malone 对文字与图表的帮助。这项工作由以下团队完成，贡献者包括：Daniel J. Mankowitz、Andrea Michi、Anton Zhernov、Marco Gelmi、Marco Selvi、Cosmin Paduraru、Edouard Leurent、Shariq Iqbal、Jean-Baptiste Lespiau、Alex Ahern、Thomas Koppe、Kevin Millikin、Stephen Gaffney、Sophie Elster、Jackson Broshear、Chris Gamble、Kieran Milan、Robert Tung、Minjae Hwang、Taylan Cemgil、Mohammadamin Barekatain、Yujia Li、Amol Mandhane、Thomas Hubert、Julian Schrittwieser、Demis Hassabis、Pushmeet Kohli、Martin Riedmiller、Oriol Vinyals 和 David Silver。感谢 Mikita Sazanovich 和 Danila Kutenin 对哈希算法的贡献。
