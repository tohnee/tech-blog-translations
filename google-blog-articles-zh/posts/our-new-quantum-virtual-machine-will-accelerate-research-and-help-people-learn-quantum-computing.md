---
title: "我们全新的量子虚拟机将加速研究并帮助人们学习量子计算"
title_en: "Our new Quantum Virtual Machine will accelerate research and help people learn quantum computing"
source: https://blog.google/innovation-and-ai/technology/research/our-new-quantum-virtual-machine-will-accelerate-research-and-help-people-learn-quantum-computing/
site: google-blog
date: 2022-07-19
crawled: 2026-09-13
translated: 2026-09-13
---

# 我们全新的量子虚拟机将加速研究并帮助人们学习量子计算

> 原文：[Our new Quantum Virtual Machine will accelerate research and help people learn quantum computing](https://blog.google/innovation-and-ai/technology/research/our-new-quantum-virtual-machine-will-accelerate-research-and-help-people-learn-quantum-computing/) · Google

几十年前，量子计算机还只是一个概念——一个主要在阶梯教室里讨论的遥远想法。快进到今天，建造容错量子计算机、发现能以有用方式应用它们的新算法的竞赛已经展开。

尽管量子计算承载着诸多憧憬，但现实是：释放它解决现实世界问题的潜力，与建造量子计算机本身同样具有挑战性。这让我们开始思考……我们如何才能让更多人加入我们探索量子算法和应用的行列？我们能否让为近期量子计算机构建量子算法原型的过程免费且易于上手，让人们专注于眼前的挑战？我们能否为人们提供所需的工具，帮助他们掌握应用开发所必需的量子编程技能？

在 Google Quantum AI，我们有一个悠久的传统：把自己为研究而构建的工具免费提供给公众。今天，我们把[量子虚拟机](http://quantumai.google/quantum-virtual-machine)（Quantum Virtual Machine）加入这个名单。量子虚拟机（QVM）模拟在我们的实验室里对一台量子计算机编程的体验和结果，从电路验证到处理器的非理想性。我们使用物理研究团队的模型，把 Sycamore 处理器的测量数据——例如量子比特衰减、退相干、门误差和读取误差——输入 QVM，并结合设备的量子比特连接拓扑，来模拟出类似量子处理器的输出。Sycamore 芯片上的实验结果与 QVM 结果的对比可以在[这个网站](https://arxiv.org/abs/2111.02396)上查看。

量子虚拟机可以[通过一个 Colab 笔记本](http://quantumai.google/quantum-virtual-machine)立即部署，并且免费提供。你无需排队等待程序结果，可以快速迭代结果。这一点，加上类似处理器的输出，使 QVM 成为一个绝佳工具，可用于为近期量子硬件构建原型、测试和优化你的量子电路。用户目前可以模拟我们的两款处理器：Weber 和 Rainbow。Weber 是[我们 2019 年发表在《自然》上的超经典计算实验](https://www.nature.com/articles/s41586-019-1666-5)中使用的 Sycamore 处理器。Rainbow 曾用于[我们发表在《科学》上、演示变分量子本征求解器求解量子化学问题的实验](https://www.science.org/doi/10.1126/science.abb9811)。

部署好量子虚拟机后，你就可以在虚拟量子比特网格上运行你的量子程序。如果你需要的量子比特数超出了 Colab 可以模拟的范围，QVM 还可以借助你选择的高性能计算进行增强。[这个工作流程](https://quantumai.google/qsim/tutorials/multinode)帮助你使用 Google Cloud 在多个并行计算节点上设置模拟。构建量子程序时，你可以使用 Cirq 1.0，这是我们[新发布的](https://opensource.googleblog.com/2022/07/Cirq-Turns-1.0.html)开源量子编程框架版本。

我们希望你在探索量子计算——无论是研究还是教育——的过程中，会发现量子虚拟机很有用。对于教师和他们的学生来说，QVM 让他们可以在一台高质量处理器上完成课程作业和项目，而不会遇到业内常见的漫长且不可预测的排队等待。我们还创建了配套文档，介绍了 QVM 和 Cirq 1.0 的若干特性，帮助学生快速上手。

随着量子硬件的每一次重大改进，发现有用应用、培养全球未来量子人才队伍的需求也在增长。欢迎加入我们的行列，使用量子虚拟机推动量子算法创新的边界。从这里开始：[quantumai.google/software](http://quantumai.google/software)。
