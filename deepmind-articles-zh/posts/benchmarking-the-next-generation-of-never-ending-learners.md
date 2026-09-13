---
title: "为下一代永不停止的学习者建立基准测试"
title_en: "Benchmarking the next generation of never-ending learners"
source: https://deepmind.google/blog/benchmarking-the-next-generation-of-never-ending-learners/
site: deepmind
date: 2022-11-22
crawled: 2026-09-13
translated: 2026-09-13
---

# 为下一代永不停止的学习者建立基准测试

> 原文：[Benchmarking the next generation of never-ending learners](https://deepmind.google/blog/benchmarking-the-next-generation-of-never-ending-learners/) · Google DeepMind

借助 30 年计算机视觉研究，学习如何在已有知识之上构建

短短几年间，大规模深度学习（DL）模型就在从预测蛋白质结构到自然语言处理与视觉[1, 2, 3]的众多领域取得了前所未有的成功。机器学习工程师和研究者能够取得这些成就，很大程度上要归功于强大的新硬件——它使模型得以扩展规模，并用更多数据进行训练。

扩大规模带来了惊人的能力，但也意味着深度学习模型可能非常消耗资源。例如，大型模型被部署时，它们在某个任务上所学到的知识很少被用来促进对下一个任务的学习。更糟糕的是，一旦有新数据或更多算力可用，大型模型通常要从头重新训练——这是一个代价高昂、耗时漫长的过程。

这就引出了一个疑问：我们能否改善这些大型模型在效率与性能之间的权衡，让它们更快、更可持续，同时保留其卓越能力？答案之一，是鼓励开发能够随时间不断积累知识的模型，从而更高效地适应新情境和新任务。

## 介绍 NEVIS'22

我们的新论文 [NEVIS'22: A Stream of 100 Tasks Sampled From 30 Years of Computer Vision Research](https://arxiv.org/abs/2211.11747) 提出了一个试验场，用于在受控且可复现的环境中研究高效知识迁移的问题。"永不停止的视觉分类流"（Never-Ending Visual classification Stream，NEVIS'22）不仅是一个基准测试流，还包含一套评估协议、一组初始基线和一个开源代码库。这一整套工具为研究者提供了机会，去探索模型如何能够在自身知识之上持续构建，从而更高效地学习未来的任务。

NEVIS'22 实际上由 106 个任务组成，这些任务提取自过去三十年间主要计算机视觉会议线上论文集中随机抽样的出版物。每个任务都是监督分类任务——机器学习中理解最透彻的一类方法。关键的是，这些任务按时间先后排列，因此会变得越来越有挑战性、越来越宽泛，为从一个不断增长的相关任务集合中迁移知识提供了越来越多的机会。挑战在于：如何自动地把有用的知识从一个任务迁移到下一个任务，以获得更好或更高效的表现。

以下是一些图像，取自我们论文附录 H 中引用的数据集：

NEVIS'22 是可复现的，且规模足以测试最先进的学习算法。该任务流包含丰富多样的任务，从光学字符识别和纹理分析，到人群计数和场景识别。任务挑选过程采用随机抽样，不偏袒任何特定方法，只是如实反映了计算机视觉社区多年来认为有趣的课题。

NEVIS'22 不仅关乎数据，也关乎训练和评估学习模型所用的方法论。我们依据学习者学习未来任务的能力来评估它们，以其在错误率与算力（后者以浮点运算次数衡量）之间的权衡来度量。举例来说，在 NEVIS'22 中仅仅取得更低的错误率是不够的，如果这要以不合理的计算成本为代价。相反，我们激励模型既准确又高效。

## 初步经验与开放挑战

我们的初步实验表明，取得更佳权衡的模型，是那些利用任务间共享结构、并采用某种迁移学习形式的模型。尤其是，巧妙的微调方法可以相当有竞争力，即便与大型预训练模型结合使用也是如此。后一发现凸显了进一步改进大规模模型通用表征的可能性，开辟了一条全新的研究路径。我们相信，NEVIS'22 为我们的社区提出了一个激动人心的新挑战，助力我们努力开发更高效、更有效的永不停止学习模型。

阅读[我们的论文](https://arxiv.org/abs/2211.11747)并下载[我们的代码](http://github.com/deepmind/dm_nevis)，进一步了解 NEVIS'22。

**注释**

参考文献

[1] John M Jumper, Richard Evans, Alexander Pritzel, Tim Green, Michael Figurnov, Olaf Ron-neberger, Kathryn Tunyasuvunakool, Russ Bates, Augustin Zídek, Anna Potapenko, Alex Bridgland, Clemens Meyer, Simon A A Kohl, Andy Ballard, Andrew Cowie, Bernardino Romera-Paredes, Stanislav Nikolov, Rishub Jain, Jonas Adler, Trevor Back, Stig Petersen, David A. Reiman, Ellen Clancy, Michal Zielinski, Martin Steinegger, Michalina Pacholska, Tamas Berghammer, Sebastian Bodenstein, David Silver, Oriol Vinyals, Andrew W Senior, Koray Kavukcuoglu, Pushmeet Kohli & Demis Hassabis. Highly accurate protein structure prediction with AlphaFold. Nature, 596:583 – 589, 2021.

[2] Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan, Rewon Child, AdityaRamesh, Daniel Ziegler, Jeffrey Wu, Clemens Winter, Chris Hesse, Mark Chen, EricSigler, Mateusz Litwin, Scott Gray, Benjamin Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya Sutskever, and Dario Amodei. Language models are few-shot learners. In H Larochelle, M Ranzato, R Hadsell, M F Balcan, and H Lin, editors, Advances in Neural Information Processing Systems, volume 33, pages 1877-1901. Curran Associates, Inc., 2020

[3] Jean-Baptiste Alayrac, Jeff Donahue, Pauline Luc, Antoine Miech, Iain Barr, Yana Hasson, Karel Lenc, Arthur Mensch, Katie Millican, Malcolm Reynolds, Roman Ring, Eliza Rutherford, Serkan Cabi, Tengda Han, Zhitao Gong, Sina Samangooei, Marianne Monteiro, Jacob Menick, Sebastian Borgeaud, Andrew Brock, Aida Nematzadeh, Sahand Sharifzadeh, Miko-laj Binkowski, Ricardo Barreira, Oriol Vinyals, Andrew Zisserman, and Karen Simonyan. Flamingo: a visual language model for few-shot learning, 2022.
