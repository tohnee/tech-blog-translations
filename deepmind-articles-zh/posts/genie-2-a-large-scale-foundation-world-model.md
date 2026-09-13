---
title: "Genie 2：大规模基础世界模型"
title_en: "Genie 2: A large-scale foundation world model"
source: https://deepmind.google/blog/genie-2-a-large-scale-foundation-world-model/
site: deepmind
date: 2024-12-04
crawled: 2026-09-13
translated: 2026-09-13
---

# Genie 2：大规模基础世界模型

> 原文：[Genie 2: A large-scale foundation world model](https://deepmind.google/blog/genie-2-a-large-scale-foundation-world-model/) · Google DeepMind

为未来的通用智能体生成无限多样的训练环境

今天，我们推出 Genie 2，一个基础世界模型，能够生成无穷多样的、可由动作控制的、可玩的 3D 环境，用于训练和评估具身智能体。基于单张提示图像，人类或 AI 智能体都可以通过键盘和鼠标输入来游玩它。

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

游戏在人工智能（AI）研究的世界中扮演着关键角色。它们引人入胜的特质、独特的挑战组合以及可度量的进步，使其成为安全测试和推进 AI 能力的理想环境。

事实上，自创立以来，游戏对 Google DeepMind 就一直十分重要。从我们[早期的 Atari 游戏工作](https://www.nature.com/articles/nature14236/)、[AlphaGo](https://deepmind.google/research/breakthroughs/alphago/) 和 [AlphaStar](https://deepmind.google/discover/blog/alphastar-grandmaster-level-in-starcraft-ii-using-multi-agent-reinforcement-learning/) 等突破，到我们与游戏开发者合作开展的[通用智能体](https://deepmind.google/discover/blog/sima-generalist-ai-agent-for-3d-virtual-environments/)研究，游戏始终是我们研究的核心舞台。然而，训练[更通用的具身智能体](https://arxiv.org/abs/2311.02462)历来受制于缺乏足够丰富多样的训练环境。

正如我们将展示的，Genie 2 可以让未来的智能体在由新世界组成的无限课程中接受训练和评估。我们的研究也为原型化交互体验开辟了全新的创意工作流。

- [能力](#capabilities)
- [快速原型设计](#rapid-prototyping)
- [在世界模型中部署智能体](#deploying-agents-in-world-models)
- [模型架构](#model-architecture)
- [负责任的开发](#responsible-development)

## 基础世界模型的涌现能力

迄今为止，世界模型大多局限于[对狭窄领域的建模](https://danijar.com/project/dreamerv3/)。在 [Genie 1](https://deepmind.google/research/publications/60474/) 中，我们提出了生成多样化 2D 世界的方法。今天我们推出的 Genie 2 则在通用性上实现了重大飞跃。Genie 2 能够生成极其丰富多样的 3D 世界。

Genie 2 是一个世界模型，这意味着它可以模拟虚拟世界，包括执行任何动作（例如跳跃、游泳等）所带来的后果。它在大规模视频数据集上训练，与其他生成式模型一样，在规模化之后展现出各种涌现能力，例如物体交互、复杂的角色动画、物理效果，以及对其他智能体行为的建模与预测能力。

下面是人们与 Genie 2 交互的示例视频。在每个示例中，模型都以一张由 GDM 最先进的文生图模型 [Imagen 3](https://deepmind.google/technologies/imagen-3/) 生成的单张图像作为提示。这意味着任何人都可以用文字描述一个想要的世界，从中挑选最喜欢的一种呈现，然后走进并与这个新创建的世界互动（或者在其中训练或评估一个 AI 智能体）。在每一步，人或智能体提供一个键盘和鼠标动作，Genie 2 便模拟出下一帧观察结果。Genie 2 能够生成持续长达一分钟的一致性世界，所展示的大多数示例持续 10-20 秒。

### 动作控制

Genie 2 能够智能地响应按下键盘按键的动作，识别角色并正确地移动它。例如，我们的模型必须弄清楚方向键应该移动机器人，而不是树木或云朵。

![一张展示键盘控制映射的文字图形："W (forward)"（前进）、"A (move left)"（向左移动）、"S (backward)"（后退）、"D (move right)"（向右移动）和"Space (jump)"（跳跃）。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/fig_1_header_large.svg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

树林里一个可爱的人形机器人。

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

古埃及的人形机器人。

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

紫色星球上一个机器人的第一人称视角。

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

大城市顶层公寓中一个机器人的第一人称视角。

### 生成反事实

我们可以从同一起始帧生成多样的轨迹，这意味着可以为训练智能体模拟反事实经验。在每一行中，每个视频都从同一帧开始，但人类玩家执行了不同的动作。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

### 长时程记忆

Genie 2 能够记住已经不在视野中的世界部分，并在它们重新变得可见时准确地渲染出来。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

### 生成新内容的长视频

Genie 2 能即时生成新的合理内容，并保持世界一致长达一分钟。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

### 多样化的环境

Genie 2 可以创建不同的视角，例如第一人称视角、等轴测视角或第三人称驾驶视频。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

### 3D 结构

Genie 2 学会了创建复杂的 3D 视觉场景。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

### 物体可供性与交互

Genie 2 对各种物体交互进行建模，例如戳破气球、开门和射击爆炸物桶。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

### 角色动画

Genie 2 学会了为执行不同活动的各类角色制作动画。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

### NPC

Genie 2 对其他智能体建模，甚至能对与它们的复杂交互建模。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

### 物理效果

Genie 2 对水的效果建模。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

### 烟雾

Genie 2 对烟雾效果建模。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

### 重力

Genie 2 对重力建模。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

### 光照

Genie 2 对点光源和方向光建模。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

### 反射

Genie 2 对反射、泛光和彩色光照建模。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

### 从真实世界图像开始游玩

Genie 2 也可以用真实世界的图像作为提示，我们看到它能够对风中吹动的草地或河中流淌的水流建模。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

## Genie 2 支持快速原型设计

Genie 2 让多样化交互体验的快速原型设计变得简单，使研究者能够快速试验新颖环境，以训练和测试具身 AI 智能体。

例如，下面我们用 Imagen 3 生成的不同图像提示 Genie 2，来模拟驾驶纸飞机、龙、鹰或降落伞之间的差异，并测试 Genie 为不同化身制作动画的能力。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

以真实世界照片提示的 Genie 2。

得益于 Genie 2 的分布外泛化能力，概念艺术图和草图可以被转化为完全可交互的环境。这让艺术家和设计师能够快速进行原型设计，从而为环境设计启动创意流程，进一步加速研究。

这里我们展示了我们的概念艺术家创作的研究环境概念示例。

![一幅阳光明媚的稀树草原风景概念图，有一条蜿蜒的河流，形似昆虫的小生物走在小路上，还有漂浮的果冻状机器人。](https://lh3.googleusercontent.com/oWrhBfmyHBM3c5pOGVartnEG6yAB6gCUGCRRsVgKOXjbC6dDocfFkO6PnTznI-uNFQkELGOHFJ_2X4shJSUSy_kLC8NoncCm84DzS25tzbIXzwDpjQ=w1440-h810-n-nu)

Max Cant 的环境概念图

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

Genie 2

![一幅阳光明媚的稀树草原风景概念图，有猴面包树和蜿蜒的河流，栖息着形似昆虫的小生物和漂浮的果冻状机器人。](https://lh3.googleusercontent.com/IwceodaFDmA3G-He8FgjkucDxo01T8rwE-D8DxGvNiMXYW5LiZiLUhUkI_NtYIAxHvSCnbHTIKGSZEw-JxZKRervAlM_EIl5HCr0FbrfAxKpyGfN-g=w1440-h810-n-nu)

Max Cant 的环境概念图

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

Genie 2

## 在世界模型中行动的 AI 智能体

通过使用 Genie 2 为 AI 智能体快速创建丰富多样的环境，我们的研究者还可以生成智能体在训练中未曾见过的评估任务。下面我们展示了 [SIMA](https://deepmind.google/discover/blog/sima-generalist-ai-agent-for-3d-virtual-environments/) 智能体的示例——该智能体是我们与游戏开发者合作开发的——它正根据指令在由 Genie 2 通过单张图像提示合成的未见环境中行动。

![一个游戏角色的第三人称视角，站在森林中的一条木路上，位于左侧一栋带红门的小木屋和右侧另一栋小木屋之间。](https://lh3.googleusercontent.com/3Ol002AoUgfgbUd8Q9421J2y-V-uokT5RTcT2Uh1z9LnOyP74vCh7Vm9-hwWhDKGdbXD6in1vZq8zOAh8LYLjeeum0TxoUM4_S3BYAUIbvcrsU8cKw=w1440-h810-n-nu)

**由 Imagen 3 生成的图像**

提示词："A screenshot of a third-person open world exploration game. The player is an adventurer exploring a forest. There is a house with a red door on the left, and a house with a blue door on the right. The camera is placed directly behind the player. #photorealistic #immersive"

SIMA 智能体旨在通过遵循自然语言指令在一系列 3D 游戏世界中完成任务。这里我们用 Genie 2 生成了一个有两扇门——一蓝一红——的 3D 环境，并给 SIMA 智能体下达指令去打开每一扇门。在这个示例中，SIMA 通过键盘和鼠标输入控制化身，而 Genie 2 生成游戏画面。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

提示词 "Open the blue door"（打开蓝色的门）

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

提示词 "Open the red door"（打开红色的门）

我们还可以用 SIMA 来帮助评估 Genie 2 的能力。这里我们指示 SIMA 四处张望并探索房子后面，以测试 Genie 2 生成一致性环境的能力。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

提示词 "Turn around"（转身）

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

提示词 "Go behind the house"（到房子后面去）

虽然这项研究仍处于早期阶段，在智能体和环境生成能力两方面都有很大改进空间，但我们相信 Genie 2 是解决一个结构性问题的路径：如何在安全地训练具身智能体的同时，实现迈向 AGI（通用人工智能）所需的广度与通用性。

![一名身披盔甲的战士手持火把站在昏暗的石室中，面对三个拱门：左边的拱门透出生物发光的绿色洞穴，中间的拱门是一个黑暗的洞窟，右边的拱门通往一段向上的石阶。](https://lh3.googleusercontent.com/mljexYdYpKmVOxANqdlABSfCl1k6EXAivsq0MkS7hPgqFrQ2VB80SBZAC-YovyNehcQPd5nRixAZV2nCdW3p5zF7Yu0R1YgrGkQfdt6L1Uro1Xd-=w1440-h810-n-nu)

**由 Imagen 3 生成的图像**

提示词："An image of a computer game showing a scene from inside a rough hewn stone cave or mine. The viewer's position is a 3rd person camera based above a player avatar looking down towards the avatar. The player avatar is a knight with a sword. In front of the knight avatar there are x3 stone arched doorways and the knight chooses to go through any one of these doors. Beyond the first and inside we can see strange green plants with glowing flowers lining that tunnel. Inside and beyond the second doorway there is a corridor of spiked iron plates riveted to the cave walls leading towards an ominous glow further along. Through the third door we can see a set of rough hewn stone steps ascending to a mysterious destination."

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

提示词 "Go up the stairs"（走上楼梯）

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

提示词 "Go where the plants are"（去有植物的地方）

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

提示词 "Go to the middle door"（去中间的门）

## 扩散世界模型

Genie 2 是一个自回归的[潜变量扩散模型](https://openaccess.thecvf.com/content/CVPR2022/html/Rombach_High-Resolution_Image_Synthesis_With_Latent_Diffusion_Models_CVPR_2022_paper.html)，在大规模视频数据集上训练。视频帧经过一个[自编码器](https://arxiv.org/abs/1312.6114)后，其潜变量帧被送入一个大型 [transformer](https://openreview.net/forum?id=YicbFdNTTy) 动力学模型，该模型使用与大语言模型类似的因果掩码进行训练。

在推理时，Genie 2 可以以自回归方式采样，逐帧接收单个动作和过去的潜变量帧。我们使用[无分类器引导](https://arxiv.org/abs/2207.12598)来提升动作可控性。

本博客文章中的样本由未蒸馏的基础模型生成，以展示其能力上限。我们也可以实时游玩蒸馏后的版本，但输出质量会有所下降。

![Genie 2 扩散世界模型的架构图：文本提示词经 Imagen 3 处理生成起始游戏帧；该帧由编码器压缩为潜变量网格，与用户的键盘动作输入（如"W"前进、"A"向左、"E"攻击）一起被自回归处理以预测后续潜变量状态，再由解码器重建为连续的游戏帧。](https://lh3.googleusercontent.com/NWpfbDUhaC1ivgNDaRc7d3kmDjVh5vGPPOJV34yN6trHaFIPmBVasa7URKn-UQo0-l3PegAOOGUa78Bu4eSi2uht2zGm3KeIGCcVfw2a0FjyZGim7w=w1440)

## 负责任地开发我们的技术

Genie 2 展示了基础世界模型在创建多样化 3D 环境和加速智能体研究方面的潜力。这一研究方向尚处于早期阶段，我们期待在通用性和一致性方面继续改进 Genie 的世界生成能力。

[正如 SIMA 一样](https://deepmind.google/discover/blog/sima-generalist-ai-agent-for-3d-virtual-environments/)，我们的研究正在朝更通用的 AI 系统和智能体迈进，它们能够以对人们在网络和现实世界有帮助的方式，理解并安全地执行广泛的任务。

## 有趣的花絮

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

在没有任何动作的情况下，花园里出现了一个幽灵

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

比起单板滑雪，角色更喜欢跑酷。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

能力越大，责任越大。

**致谢**

Genie 2 由 Jack Parker-Holder 主导，Stephen Spencer 担任技术负责人，Philip Ball、Jake Bruce、Vibhavari Dasagi、Kristian Holsheimer、Christos Kaplanis、Alexandre Moufarek、Guy Scully、Jeremy Shar、Jimmy Shi 和 Jessica Yung 做出了关键贡献，Michael Dennis、Sultan Kenjeyev 和 Shangbang Long 亦有贡献。Yusuf Aytar、Jeff Clune、Sander Dieleman、Doug Eck、Shlomi Fruchter、Raia Hadsell、Demis Hassabis（德米斯·哈萨比斯）、Georg Ostrovski、Pieter-Jan Kindermans、Nicolas Heess、Charles Blundell、Simon Osindero、Rushil Mistry 提供了建议。过往贡献者包括 Ashley Edwards 和 Richie Steigerwald。

通用智能体团队由 Vlad Mnih 领导，Harris Chan、Maxime Gazeau、Bonnie Li、Fabio Pardo、Luyu Wang、Lei Zhang 做出了关键贡献。

[SIMA 团队](https://arxiv.org/abs/2404.10179)提供了特别支持，尤其是 Frederic Besse、Tim Harley、Anna Mitenkova 和 Jane Wang。

Tim Rocktäschel、Satinder Singh 和 Adrian Bolton 协调、管理并指导了整个项目。

我们还要感谢 Zoubin Gharamani、Andy Brock、Ed Hirst、David Bridson、Zeb Mehring、Cassidy Hardin、Hyunjik Kim、Noah Fiedel、Jeff Stanway、Petko Yotov、Mihai Tiuca、Soheil Hassas Yeganeh、Nehal Mehta、Richard Tucker、Tim Brooks、Alex Cullum、Max Cant、Nik Hemmings、Richard Evans、Valeria Oliveira、Yanko Gitahy Oliveira、Bethanie Brownfield、Charles Gbadamosi、Giles Ruscoe、Guy Simmons、Jony Hudson、Marjorie Limont、Nathaniel Wong、Sarah Chakera、Nick Young。

引用请注明 Parker-Holder et al.，BibTeX 如下

[下载 BibTeX](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/genie-2-a-large-scale-foundation-world-model/parkerholder2024genie2.bib)
