---
title: "MuJoCo 正式开源"
title_en: "Open-sourcing MuJoCo"
source: https://deepmind.google/blog/open-sourcing-mujoco/
site: deepmind
date: 2022-05-23
crawled: 2026-09-13
translated: 2026-09-13
---

# MuJoCo 正式开源

> 原文：[Open-sourcing MuJoCo](https://deepmind.google/blog/open-sourcing-mujoco/) · Google DeepMind

2021 年 10 月，我们宣布收购了 [MuJoCo 物理模拟器](https://mujoco.org/)，并向所有人免费开放，以支持各地的研究工作。我们还承诺将 MuJoCo 打造并维护为一个免费、开源、由社区驱动且具备一流能力的项目。今天，我们很高兴地宣布：开源工作已经完成，整个代码库已在 [GitHub](https://github.com/deepmind/mujoco) 上发布！

在这篇文章中，我们将解释为什么 MuJoCo 是一个非常适合开源协作的平台，并提前分享我们接下来的路线图。

## 一个协作平台

物理模拟器是现代机器人研究中的关键工具，通常分为以下两类：

1. 闭源商业软件。
2. 开源软件，通常诞生于学术界。

第一类软件对用户来说是黑盒，虽然有时可以免费使用，但无法修改，也难以理解。第二类软件的用户群往往较小，一旦开发者或维护者毕业离校，项目就容易陷入停滞。

MuJoCo 是少数由成熟公司支持、真正开源的全功能模拟器之一。作为一个以研究为导向的组织，我们将 MuJoCo 视为一个协作平台——机器人学者和工程师可以加入我们，共同打造世界上最优秀的机器人模拟器之一。

让 MuJoCo 特别适合协作的特性包括：

- 全功能模拟器，能够[建模](https://www.youtube.com/watch?v=mfAst_GB8Sk)[复杂](https://www.youtube.com/watch?v=4J4tO8bb70I)[机构](https://www.youtube.com/watch?v=LZ7vkzZF4xk)。
- 代码可读、高性能、可移植。
- 代码库易于扩展。
- 详尽的文档：既有面向用户的文档，也有代码注释。

我们希望学术界和开源（OSS）社区的同行们能从这个平台中受益，并为代码库做出贡献，从而改善所有人的研究体验。

## 性能

MuJoCo 是一个不进行动态内存分配的 C 库，因此速度非常快。遗憾的是，裸物理计算速度历来受到 Python 封装层的拖累：由于全局解释器锁（GIL）的存在以及代码未经编译，批量、多线程操作的性能不佳。我们在下文路线图中会着手解决这一问题。

现在，我们想分享两个常见模型的基准测试结果。测试在标准 AMD Ryzen 9 5950X 机器上进行，操作系统为 Windows 10。

![性能基准测试表，展示 Humanoid 与 AnyMAL 模型在 1、16、32 线程下每秒可执行数千步。](https://lh3.googleusercontent.com/amAuTVrGXyKUGAonFwG5-stP0AZntLATPgHoysZQlOMBAyVAj55LNMGJAaPh8jrhM4lsipOyS2VTvgI5MQTSFy15aEqjSnjx5Too1RodJkhBVT_C1Q=w1440)

这些数值来自我们的 testspeed 示例代码。值得注意的是，测试会向执行器注入控制噪声，防止系统收敛到固定状态，因此结果能够代表真实场景下的性能。

## 路线图

以下是 MuJoCo 的近期路线图：

- 通过批量、多线程模拟释放 MuJoCo 的速度潜力。
- 改进内部内存管理，以支持更大规模的场景。
- 全新的增量编译器，提供更好的模型可组合性。
- 通过与 Unity 集成支持更好的渲染。
- 原生支持物理导数，包括解析导数和有限差分导数。

## 了解更多

关于 MuJoCo 的有用资源：

- [MuJoCo 文档](https://mujoco.readthedocs.io/en/latest/overview.html)
- [GitHub 上的 MuJoCo 仓库](https://github.com/deepmind/mujoco)
- [如何参与贡献](https://github.com/deepmind/mujoco/blob/main/CONTRIBUTING.md)

我们期待收到你的贡献！
