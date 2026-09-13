---
title: "我们在机器人灵巧性方面的最新进展"
title_en: "Our latest advances in robot dexterity"
source: https://deepmind.google/blog/advances-in-robot-dexterity/
site: deepmind
date: 2024-09-12
crawled: 2026-09-13
translated: 2026-09-13
---

# 我们在机器人灵巧性方面的最新进展

> 原文：[Our latest advances in robot dexterity](https://deepmind.google/blog/advances-in-robot-dexterity/) · Google DeepMind

两个新 AI 系统——ALOHA Unleashed 和 DemoStart——帮助机器人学会执行需要灵巧动作的复杂任务

人们每天都在完成许多任务，比如系鞋带或拧紧螺丝。但对机器人来说，学会这些高度灵巧的任务并做对是极其困难的。要让机器人在人们的生活中更有用，它们需要更擅长在动态环境中与物理物体发生接触。

今天，我们发布两篇新论文，展示我们在机器人灵巧性研究上的最新人工智能（AI）进展：[ALOHA Unleashed](https://aloha-unleashed.github.io/assets/aloha_unleashed.pdf) 帮助机器人学会执行复杂而新颖的双臂操作任务；[DemoStart](https://arxiv.org/abs/2409.06613) 则利用仿真来提升多指机器手在真实世界中的表现。

通过帮助机器人从人类演示中学习并把图像转化为动作，这些系统正在为能够完成各种各样有用任务的机器人铺平道路。

## 用两条机械臂改进模仿学习

到目前为止，大多数先进的 AI 机器人只能用单臂拿起和放置物体。在[我们的新论文](https://aloha-unleashed.github.io/assets/aloha_unleashed.pdf)中，我们提出了 ALOHA Unleashed，它在双臂操作上达到了很高的灵巧水平。借助这一新方法，我们的机器人学会了系鞋带、挂衬衫、修理另一个机器人、安装齿轮，甚至打扫厨房。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![你的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

双臂机器人理顺鞋带并系成蝴蝶结的示例。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![你的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

双臂机器人把一件 Polo 衫平铺在桌上、套上衣架、再挂到晾衣架上的示例。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![你的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

双臂机器人修理另一个机器人的示例。

ALOHA Unleashed 方法建立在我们基于斯坦福大学（Stanford University）原始 [ALOHA](https://tonyzhaozh.github.io/aloha/)（一个低成本开源双臂遥操作硬件系统）打造的 [ALOHA 2](https://aloha-2.github.io/) 平台之上。

ALOHA 2 比以往系统灵巧得多，因为它拥有两只易于遥操作的手，可用于训练和数据采集，而且它让机器人能够用更少的演示学会执行新任务。

我们在最新系统中还改进了机器人硬件的人体工学，并强化了学习流程。首先，我们通过远程操作机器人的行为来采集演示数据，执行系鞋带、挂 T 恤这类困难任务。接着，我们应用了一种扩散方法，从随机噪声中预测机器人动作，类似于我们的 [Imagen](https://deepmind.google/technologies/imagen-3/) 模型生成图像的方式。这帮助机器人从数据中学习，从而能够自己完成同样的任务。

## 从少量仿真演示中学习机器人行为

控制一只灵巧的机器手是一项复杂任务，每多一个手指、关节和传感器，复杂度都会增加。在另一篇[新论文](https://arxiv.org/abs/2409.06613)中，我们提出了 DemoStart，它使用强化学习算法帮助机器人在仿真中习得灵巧行为。这些习得的行为对多指手等复杂本体（embodiment）尤其有用。

DemoStart 先从简单的状态学起，随着时间推移，开始从更困难的状态中学习，直到尽其所能掌握一项任务。与通常从真实世界样本中学习达到同样目的相比，它学习如何在仿真中求解一项任务所需的仿真演示少了 100 倍。

在仿真中，该机器人在多项不同任务上的成功率超过 98%，包括把立方体翻转到指定颜色一面、拧紧螺母和螺栓，以及整理工具。在真实环境设置中，它在立方体翻转与拾起上取得了 97% 的成功率，在一个需要高度手指协调与精度的插头-插座插入任务上取得 64% 的成功率。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![你的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

机器臂学习成功插入一个黄色连接器的示例：左侧为仿真，右侧为真实环境设置。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![你的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

机器臂在仿真中学习拧紧螺栓的示例。

我们使用开源物理仿真器 [MuJoCo](https://mujoco.org/) 开发了 DemoStart。在仿真中掌握一系列任务、并使用域随机化等标准技术缩小仿真到现实的差距之后，我们的方法几乎可以零样本迁移到物理世界。

在仿真中进行机器人学习可以降低开展真实物理实验所需的成本与时间。但设计这些仿真本身就很难，而且它们并不总能成功转化为真实世界的表现。通过把强化学习与少量演示学习相结合，DemoStart 的渐进式学习自动生成一座连接仿真与现实差距的课程（curriculum），使知识更容易从仿真迁移到实体机器人上，并降低了运行物理实验所需的成本与时间。

为了通过密集实验实现更先进的机器人学习，我们在一只名为 [DEX-EE](https://www.shadowrobot.com/dex-ee/) 的三指机器手上测试了这一新方法，该机器手是与 [Shadow Robot](https://www.shadowrobot.com/) 合作开发的。

![DEX-EE 三指机器手的特写，手指为黑色、带有关节、可多关节活动，背景为纯白色。](https://lh3.googleusercontent.com/uuY20ESjCaU6ldnvE53s9PX5q4GovZlFSwsO900w6SOBiEQBQPX4hS9NFpO4AQkGzh0HboLmPKu6XpeF63G2z4xj34fGreyQwaFRtTWXtTFuySi2=w1440)

DEX-EE 灵巧机器手的图片，由 Shadow Robot 与 Google DeepMind 机器人团队合作开发（图片来源：Shadow Robot）。

## 机器人灵巧性的未来

机器人学是 AI 研究中一个独特的领域，它检验我们的方法在真实世界中的表现。例如，一个大语言模型可以告诉你如何拧紧螺栓或系鞋带，但即便把它装进机器人身体，它也无法亲自完成这些任务。

终有一天，AI 机器人将在家中、工作场所等各处帮助人们完成各种各样的任务。灵巧性研究——包括我们今天介绍的这些高效、通用的学习方法——将帮助让那样的未来成为可能。

在机器人能够像人一样轻松而精准地抓取和操控物体之前，我们还有很长的路要走，但我们正在取得重大进展，每一项突破性创新都是朝着正确方向迈出的又一步。

[阅读我们的 ALOHA Unleashed 论文](https://aloha-unleashed.github.io/assets/aloha_unleashed.pdf)[阅读我们的 DemoStart 论文](https://arxiv.org/abs/2409.06613)[了解更多关于 ALOHA 2 的信息](https://aloha-2.github.io/)

**致谢**

DemoStart 的作者：Maria Bauza、Jose Enrique Chen、Valentin Dalibard、Nimrod Gileadi、Roland Hafner、Antoine Laurens、Murilo F. Martins、Joss Moore、Rugile Pevceviciute、Dushyant Rao、Martina Zambelli、Martin Riedmiller、Jon Scholz、Konstantinos Bousmalis、Francesco Nori、Nicolas Heess。

Aloha Unleashed 的作者：Tony Z. Zhao、Jonathan Tompson、Danny Driess、Pete Florence、Kamyar Ghasemipour、Chelsea Finn、Ayzaan Wahid。
