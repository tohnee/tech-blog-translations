---
title: "Project Genie：探索无限交互世界的实验"
title_en: "Project Genie: Experimenting with infinite, interactive worlds"
source: https://blog.google/innovation-and-ai/models-and-research/google-deepmind/project-genie/
site: google-blog
date: 2026-01-29
crawled: 2026-09-13
translated: 2026-09-13
---

# Project Genie：探索无限交互世界的实验

> 原文：[Project Genie: Experimenting with infinite, interactive worlds](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/project-genie/) · Google

8 月，我们[预览了 Genie 3](https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/)——一个能够生成多样化交互环境的通用世界模型。即使在这一早期形态中，受信测试者也能够创建出令人惊叹的丰富世界和体验，并发现了全新的使用方式。下一步，是通过一个专注于沉浸式世界创作的专属交互式原型来扩大访问范围。

从今天开始，我们向美国的 Google AI Ultra 订阅用户（18 岁以上）推出 [Project Genie](http://labs.google/projectgenie/) 的访问权限。这个实验性研究原型让用户可以创建、探索和混搭（remix）属于自己的交互式世界。

## 我们如何推进世界模型

世界模型模拟环境的动态，预测环境如何演化以及动作如何影响环境。虽然 Google DeepMind 在国际象棋或围棋等特定环境的智能体方面有着深厚积累（如 [Chess](https://deepmind.google/research/alphazero-and-muzero/) 和 [Go](https://deepmind.google/research/alphago/?_gl=1*1rofsan*_up*MQ..*_ga*MTU2MTkwNzU1Ni4xNzY5Mzc1ODQz*_ga_LS8HVHCNQ0*czE3NjkzNzU4NDMkbzEkZzAkdDE3NjkzNzU4NDMkajYwJGwwJGgw)），但构建通用人工智能（AGI）需要能够在真实世界的多样性中穿行的系统。

为了应对这一挑战并支持我们的 AGI 使命，我们开发了 Genie 3。与基于静态 3D 快照的可探索体验不同，Genie 3 会在你移动和与世界交互时实时生成前方的路径。它为动态世界模拟物理规律和交互，而其突破性的一致性使模拟任何真实世界场景成为可能——从机器人和建模、动画与虚构内容，到探索各类地点和历史场景。

在我们与来自各行各业和领域的受信测试者开展模型研究的基础上，我们正以一个实验性研究原型迈出下一步：Project Genie。

## Project Genie 如何工作

Project Genie 是一个由 Genie 3、[Nano Banana Pro](https://deepmind.google/models/gemini-image/pro/) 和 [Gemini](http://gemini.google.com/) 驱动的原型 Web 应用，让用户能够亲身体验我们世界模型的沉浸式体验。这一体验围绕三项核心能力：

### 1. 世界速写（World sketching）

用文本以及生成或上传的图像进行提示，创建一个鲜活的、不断扩展的环境。创建你的角色、你的世界，并定义你想如何探索它——从步行到骑行，从飞行到驾驶，乃至一切超越。

为了实现更精确的控制，我们将「世界速写」与 Nano Banana Pro 集成。这让你可以在进入世界之前预览它的样子，并修改图像以微调你的世界。你还可以为角色定义视角——如第一人称或第三人称——让你在进入之前就能掌控体验场景的方式。

### 2. 世界探索（World exploration）

你的世界是一个等待探索的可导航环境。当你移动时，Project Genie 会根据你采取的行动实时生成前方的路径。你还可以在穿越世界的过程中调整镜头。

### 3. 世界混搭（World remixing）

通过在现有世界的提示词之上进行构建，把它们混搭成全新的诠释。你也可以在画廊中浏览精选世界，或点击随机图标寻找灵感，或在其基础上继续构建。完成之后，你还可以下载自己的世界以及探索过程的视频。

## 我们如何负责任地构建

Project Genie 是 Google Labs 中的一个实验性研究原型，由 Genie 3 驱动。与我们迈向通用 AI 系统的所有工作一样，我们的使命是负责任地构建 AI 以造福人类。由于 Genie 3 是一个早期研究模型，目前存在一些已知的待改进之处：

- 生成的世界可能看起来不完全逼真，或并不总是紧贴提示词、图像或现实世界的物理规律
- 角色有时可控性较差，或控制延迟较高
- 单次生成时长限制在 60 秒以内

我们在 8 月宣布的部分 Genie 3 模型能力——例如可提示事件（promptable events，在你探索世界的过程中改变世界）——尚未包含在这个原型中。你可以[在这里](http://deepmind.google/genie)了解更多关于模型限制以及我们未来如何改进体验的细节。

在我们与受信测试者开展工作的基础上，我们很高兴与使用我们最先进 AI 的用户分享这个原型，以更好地了解人们将在 AI 研究和生成式媒体的众多领域中如何使用世界模型。

Project Genie 的访问权限从今天开始向美国的 [Google AI Ultra 订阅用户](https://one.google.com/about/google-ai-plans/)
[1](#footnote-1)
（18 岁以上）推出，并将在适当时候扩展到更多地区。我们期待看到他们创造的无限多样的世界；我们的目标是，最终让更多用户也能获得这些体验和技术。
