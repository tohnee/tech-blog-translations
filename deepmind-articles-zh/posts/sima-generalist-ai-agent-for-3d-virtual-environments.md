---
title: "SIMA：面向 3D 虚拟环境的通用 AI 智能体"
title_en: "A generalist AI agent for 3D virtual environments"
source: https://deepmind.google/blog/sima-generalist-ai-agent-for-3d-virtual-environments/
site: deepmind
date: 2024-03-13
crawled: 2026-09-13
translated: 2026-09-13
---

# SIMA：面向 3D 虚拟环境的通用 AI 智能体

> 原文：[A generalist AI agent for 3D virtual environments](https://deepmind.google/blog/sima-generalist-ai-agent-for-3d-virtual-environments/) · Google DeepMind

我们展示关于可扩展可指令多世界智能体（SIMA，Scalable Instructable Multiworld Agent）的新研究，它能够遵循自然语言指令，在各种电子游戏场景中执行任务

电子游戏是人工智能（AI）系统的关键试验场。与现实世界一样，游戏是丰富的学习环境，具有实时响应的场景和不断变化的目标。

从我们[早期对 Atari 游戏的研究](https://www.nature.com/articles/nature14236/)，到以人类大师级水平游玩《星际争霸 II》的 [AlphaStar](https://deepmind.google/discover/blog/alphastar-grandmaster-level-in-starcraft-ii-using-multi-agent-reinforcement-learning/) 系统，Google DeepMind 在 AI 与游戏领域有着悠久的历史。

今天，我们宣布一个新的里程碑——将我们的焦点从单一游戏转向一个通用、可指令的游戏 AI 智能体。

在一份新的[技术报告](https://arxiv.org/abs/2404.10179)中，我们介绍 SIMA（Scalable Instructable Multiworld Agent 的缩写），一个面向 3D 虚拟场景的通用 AI 智能体。我们与游戏开发者合作，在多种电子游戏上训练 SIMA。这项研究标志着智能体首次证明自己能够理解广泛的游戏世界，并像人类那样在其中遵循自然语言指令执行任务。

这项工作的目标不是取得高分。对 AI 系统而言，学会玩哪怕一款电子游戏都是技术壮举，但学会在各种游戏场景中遵循指令，则可能解锁对任何环境都更有帮助的 AI 智能体。我们的研究展示了如何通过语言接口，把先进 AI 模型的能力转化为有用的、真实世界的行动。我们希望 SIMA 及其他智能体研究能把电子游戏当作沙盒，以更好地理解 AI 系统如何变得更有帮助。

## 从电子游戏中学习

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

我们与八家游戏工作室合作，在九款不同的电子游戏上训练和测试 SIMA。

为了让 SIMA 接触大量环境，我们与游戏开发者建立了多项研究合作。我们与八家游戏工作室合作，在九款不同的电子游戏上训练和测试 SIMA，例如 Hello Games 的《无人深空》（No Man's Sky）和 Tuxedo Labs 的《Teardown》。SIMA 作品组合中的每款游戏都开启了一个新的交互世界，涵盖从简单导航和菜单使用，到开采资源、驾驶飞船或打造头盔等一系列需要学习的技能。

我们还使用了四个研究环境——包括我们与 [Unity](https://deepmind.google/blog/using-unity-to-help-solve-intelligence/) 合作构建的新环境「建造实验室」（Construction Lab），智能体需要在其中用积木搭建雕塑，以此考验它们的物体操控能力以及对物理世界的直觉理解。

通过从不同的游戏世界中学习，SIMA 捕捉了语言与游戏行为之间的关联。我们的第一种做法是记录成对的人类玩家在我们的游戏组合中的表现，一名玩家观看并指导另一名。我们还让玩家自由游玩，然后回看自己的操作，并录制出原本会引导他们做出那些游戏动作的指令。

![一幅详细说明 SIMA 智能体训练工作流程的图表，从左到右依次为「环境」（包括 Valheim、Teardown 等商业游戏和 Construction Lab 等研究环境）、「数据」（从人类玩家收集数据）、「智能体」（使用预训练模型进行训练），最后是「评估」（人类评估智能体在游戏中执行文本指令）。](https://lh3.googleusercontent.com/-gxeUygwIrMQel1FzsNH1cyThJZ9Wd2ZzwId17pmFxl5qXsQzXd74ZYgf5pAHqoNODEnFOOz9LytpXAAlcbSqO6Oild5sMLOFUsakRd63eVTlrJIQQ=w1440)

SIMA 由预训练视觉模型和一个主模型组成，主模型包含记忆模块并输出键盘和鼠标操作。

## SIMA：多才多艺的 AI 智能体

SIMA 是一个能够感知并理解多种环境、然后采取行动以达成被指令目标的 AI 智能体。它由一个为精确的图像-语言映射而设计的模型，和一个预测屏幕上下一步会发生什么的视频模型组成。我们在 SIMA 组合中 3D 场景专有的训练数据上对模型进行了微调。

我们的 AI 智能体不需要访问游戏的源代码，也不需要定制 API。它只需要两个输入：屏幕上的图像，以及用户提供的简单自然语言指令。SIMA 使用键盘和鼠标输出来控制游戏的主角以执行这些指令。这种简单的接口正是人类所使用的，这意味着 SIMA 理论上可以与任何虚拟环境交互。

当前版本的 SIMA 在 600 项基础技能上进行评估，涵盖导航（例如「向左转」）、物体交互（「爬上梯子」）和菜单使用（「打开地图」）。我们训练 SIMA 完成可在约 10 秒内完成的简单任务。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

SIMA 在 600 项基础技能上接受评估，涵盖导航、物体交互和菜单使用。

我们希望未来的智能体能够完成需要高层战略规划和多个子任务配合的工作，例如「寻找资源并搭建营地」。这对整个 AI 领域都是一个重要目标，因为尽管大语言模型已经催生出能够捕捉世界知识并生成计划的强大系统，它们目前仍缺乏代表我们采取行动的能力。

## 跨游戏泛化及更多

我们展示了一个在多款游戏上训练的智能体优于只学会玩单一游戏的智能体。在我们的评估中，在我们作品组合中九款 3D 游戏的集合上训练的 SIMA 智能体，显著优于所有仅在单一游戏上训练的专用智能体。更进一步，一个在除某款游戏之外的所有游戏上训练的智能体，在该未见游戏上的表现平均接近专门针对它训练的智能体。重要的是，这种在全新环境中运作的能力凸显了 SIMA 超越其训练进行泛化的能力。这是一个有前景的初步结果，但要让 SIMA 在已见和未见的游戏中都达到人类水平，还需要更多研究。

我们的结果还表明，SIMA 的表现依赖于语言。在一个没有给智能体任何语言训练或指令的对照测试中，它的行为方式虽然合理但漫无目的。例如，智能体可能去收集资源——一种常见行为——而不是走向它被指示前往的地点。

![一幅柱状图，显示 SIMA 智能体相对于环境专用基线（100%）的相对表现（%）。「在所有环境中训练」的智能体得分最高，约 165%。「面对未见环境」的智能体表现接近基线，约 90%。「未提供语言」的智能体表现不佳，仅略高于 30%。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/Sima_Fig4.svg)

我们评估了 SIMA 遵循指令完成近 1500 个独特游戏内任务的能力，其中部分借助人类评审。作为基线对比，我们使用环境专用 SIMA 智能体（在单一环境内训练并评估其遵循指令的表现）的成绩。我们将这一成绩与三类通用 SIMA 智能体进行比较，每一类都在多个环境中训练。

## 推进 AI 智能体研究

SIMA 的结果显示出开发新一代通用、语言驱动的 AI 智能体的潜力。这是早期阶段的研究，我们期待在更多训练环境中继续拓展 SIMA，并纳入更强大的模型。

随着我们让 SIMA 接触更多训练世界，我们期望它变得更具泛化能力、更加多才多艺。借助更先进的模型，我们希望提升 SIMA 对更高级语言指令的理解与执行能力，以达成更复杂的目标。

归根结底，我们的研究正朝着更通用的 AI 系统与智能体迈进，让它们能够以对线上和现实世界中的人们有帮助的方式，理解并安全地执行广泛任务。

**进一步了解 SIMA**

[阅读我们的技术报告](https://arxiv.org/abs/2404.10179)

我们感谢所有论文作者：Maria Abi Raad, Arun Ahuja, Catarina Barros, Frederic Besse, Andrew Bolt, Adrian Bolton, Bethanie Brownfield, Gavin Buttimore, Max Cant, Sarah Chakera, Stephanie Chan, Jeff Clune, Adrian Collister, Vikki Copeman, Alex Cullum, Ishita Dasgupta, Julia Di Trapani, Yani Donchev, Martin Engelcke, Ryan Faulkner, Frankie Garcia, Charles Gbadamosi, Zhitao Gong, Lucy Gonzales, Karol Gregor, Kshitij Gupta, Arne Olav Hallingstad, Tim Harley, Sam Haves, Felix Hill, Ed Hirst, Drew Hudson, Jony Hudson, Steph Hughes-Fitt, Danilo J. Rezende, Mimi Jasarevic, Laura Kampis, Rosemary Ke, Thomas Keck, Junkyung Kim, Oscar Knagg, Kavya Kopparapu, Andrew Lampinen, Rory Lawton, Shane Legg, Alexander Lerchner, Marjorie Limont, Yulan Liu, Maria Loks-Thompson, Joseph Marino, Kathryn Martin Cussons, Loic Matthey, Siobhan Mcloughlin, Piermaria Mendolicchio, Hamza Merzic, Anna Mitenkova, Alexandre Moufarek, Valeria Oliveira, Yanko Oliveira, Hannah Openshaw, Renke Pan, Aneesh Pappu, Alex Platonov, Ollie Purkiss, David Reichert, John Reid, Pierre Harvey Richemond, Tyson Roberts, Giles Ruscoe, Jaume Sanchez Elias, Tasha Sandars, Daniel P. Sawyer, Tim Scholtes, Guy Simmons, Daniel Slater, Hubert Soyer, Heiko Strathmann, Peter Stys, Allison Tam, Tayfun Terzi, Davide Vercelli, Bojan Vujatovic, Marcus Wainwright, Jane X. Wang, Zhengdong Wang, Daan Wierstra, Duncan Williams, Nathaniel Wong, Sarah York 和 Nick Young。

特别感谢与我们合作的所有游戏开发者：Coffee Stain（Valheim、Satisfactory、Goat Simulator 3）、Foulball Hangover（Hydroneer）、Hello Games（No Man's Sky）、Keen Software House（Space Engineers）、RubberbandGames（Wobbly Life）、Strange Loop Games（Eco）以及 Tuxedo Labs 与 Saber Interactive（Teardown）。
