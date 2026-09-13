---
title: "使用 Unity 帮助解决智能问题"
title_en: "Using Unity to Help Solve Intelligence"
source: https://deepmind.google/blog/using-unity-to-help-solve-intelligence/
site: deepmind
date: 2020-11-18
crawled: 2026-09-13
translated: 2026-09-13
---

# 使用 Unity 帮助解决智能问题

> 原文：[Using Unity to Help Solve Intelligence](https://deepmind.google/blog/using-unity-to-help-solve-intelligence/) · Google DeepMind

## 广泛的环境

在追求通用人工智能（AGI）的过程中，我们力求创建能够在广泛环境中达成目标的智能体。随着我们的智能体掌握我们所创建的环境，我们必须持续创建新环境，以探测尚未测试过的认知能力。

游戏一直为人工智能（AI）研究提供挑战，最著名的是双陆棋、国际象棋和围棋等棋盘游戏。近年来，《太空侵略者》（Space Invaders）、Quake III Arena、Dota 2 和 StarCraft II 等电子游戏也已成为 AI 研究的热门对象。游戏之所以理想，是因为它们有明确的成功衡量标准，使进展能够得到实证检验，并可直接与人类进行基准对比。

随着 AGI 研究的推进，研究社区对更复杂游戏的兴趣也在增长。与此同时，把单个电子游戏改造为研究环境所需的工程工作量变得难以管理。越来越多的情况下，通用游戏引擎成为创建广泛交互环境的最具可扩展性的方式。

## 通用游戏引擎

许多 AGI 研究已经在游戏引擎中进行，例如基于 Minecraft 的 [Project Malmo](https://www.microsoft.com/en-us/research/project/project-malmo/)、基于 Doom 的 [ViZDoom](http://vizdoom.cs.put.edu.pl/)，以及基于 Quake III Arena 的 [DeepMind Lab](https://github.com/deepmind/lab)。这些引擎可以通过脚本快速创建新环境——而且由于许多引擎是为较旧的硬件编写的，它们在现代硬件上能够极快地运行，从而消除了环境本身成为性能瓶颈的可能。

但这些游戏引擎缺少一些重要特性。例如，DeepMind Lab 非常适合学习导航，但在学习常识性概念——例如物体如何运动以及彼此如何交互——方面表现不佳。

## Unity

在 DeepMind，我们使用 Unity——一个灵活且功能丰富的游戏引擎。Unity 真实的物理仿真让智能体能够体验与真实世界联系更紧密的环境。现代渲染管线提供了更细微的视觉线索，例如逼真的光照与阴影。Unity 脚本使用 C# 编写，易于阅读，而且与定制引擎不同，它能访问所有游戏引擎特性。多平台支持让我们既能在自己的笔记本上在家运行环境，也能在 Google 的数据中心大规模运行。最后，随着 Unity 引擎不断演进，我们无需耗费大量自己的工程时间就能保持技术不落伍。

Unity 包含一个开箱即用的机器学习工具包 [ML-Agents](https://unity.com/products/machine-learning-agents)，专注于简化把现有游戏变为学习环境的过程。DeepMind 专注于构建各种异构环境并大规模运行，因此我们改用 dm\_env\_rpc（见下文）。

![DeepMind 创建的 Unity 环境的四幅截屏](https://lh3.googleusercontent.com/DW-eKf83KbI3sYOIflGj2CG6DZeui2qBmhDVKH4HO3B2247NrVvviFRDvEjae2ciCqdUWktSkE0cxByVQOKL7Ha2fDhBwr8yQUJcRD0bf4D3FIcJ_3Q=w1440)

DeepMind 创建的 Unity 环境的截屏

## 与传统游戏的差异

传统电子游戏实时渲染自身：屏幕上的一秒等于仿真中的一秒。但对 AI 研究者来说，游戏只是数据流。游戏往往可以比实时快得多的速度处理，即使游戏速度在不同时刻剧烈波动也没有问题。

此外，许多强化学习算法可以随多个实例扩展。也就是说，一个 AI 可以同时进行数千局游戏，并立刻从所有对局中学习。

因此，我们优化的是吞吐量而非延迟。也就是说，我们尽可能多地更新游戏，而不必以稳定的速率生成这些更新。我们在一台计算机上运行多个游戏，每个处理器核心运行一个游戏。由垃圾回收等功能造成的停顿——传统游戏制作者的常见烦恼——对我们来说无关紧要，只要游戏总体上运行迅速即可。

## 容器化与 dm\_env\_rpc

游戏输出图像、文本和声音供玩家观看和聆听，同时接受来自某种游戏控制器的输入命令。这些数据的结构对 AI 研究者很重要。例如，文本通常单独呈现，而不是绘制到屏幕上。由于这种数据格式的灵活性至关重要，我们创建了一个新的开源库 [dm\_env\_rpc](https://github.com/deepmind/dm_env_rpc)，作为环境与智能体之间的边界。

通过使用 dm\_env\_rpc，我们可以将环境容器化并公开发布。容器化是指使用 [Docker](https://www.docker.com/) 等技术打包预编译的环境二进制文件。容器化让我们的研究能够被独立验证。与开源相比，它是一种更可靠、更便捷的实验复现方式——开源可能因编译器或操作系统差异而产生混淆。有关我们如何将环境容器化的更多细节，请参阅我们在 [dm\_memorytasks](https://github.com/deepmind/dm_memorytasks) 上的工作。
