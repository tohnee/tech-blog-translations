---
title: "无地图的城市导航学习"
title_en: "Learning to navigate in cities without a map"
source: https://deepmind.google/blog/learning-to-navigate-in-cities-without-a-map/
site: deepmind
date: 2018-03-29
crawled: 2026-09-13
translated: 2026-09-13
---

# 无地图的城市导航学习

> 原文：[Learning to navigate in cities without a map](https://deepmind.google/blog/learning-to-navigate-in-cities-without-a-map/) · Google DeepMind

你是如何学会在童年的街区里认路的？去朋友家、去学校、去杂货店——多半不需要地图，只是记住了沿途街道和路口的模样。随着你逐渐探索周边，你会越来越有信心，熟悉自己身处的位置，并学会新的、越来越复杂的路线。你可能偶尔迷路，但借助地标重新找到方向，甚至可能靠太阳充当临时指南针。

导航是一项重要的认知任务，它使人类和动物无需地图便能在复杂世界中长距离穿行。这种长程导航可以同时支持自我定位（「我在这里」）和目标表征（「我要去那里」）。

在《[Learning to Navigate in Cities Without a Map](https://arxiv.org/abs/1804.00168)》中，我们构建了一个交互式导航环境，它使用来自 [Google Street View](https://en.wikipedia.org/wiki/Google_Street_View) 的第一人称视角照片（经 StreetLearn 项目和学术研究批准使用），并将该环境游戏化以训练 AI。与 Street View 图像的标准做法一样，人脸和车牌都做了模糊处理，无法辨认。我们构建了基于神经网络的人工智能体，它学会利用视觉信息（Street View 图像的像素）在多座城市中导航。请注意，这项研究关注的是一般意义上的导航而非驾驶；我们没有使用交通信息，也没有尝试对车辆控制建模。

![三幅并排的 Google Street View 全景图，展示用于 AI 导航训练的多样城市环境：纽约市时代广场的黄色出租车和广告牌、中央公园毕士达露台的葱郁绿意，以及伦敦圣保罗大教堂和标志性的红色双层巴士。](https://lh3.googleusercontent.com/po6lqhaBy-0k3SBx2lTBKMqJ2hkfyCFgbNwmpl5zSBEpMj0Ji6U9mntN0x0OxnBvUM62rYmRzMJFjGA3_aPo5hH-SvkRAN6JSff3lWTdRGvVanVtSg=w1440)

我们的智能体在视觉上多样的环境中导航，且无法访问环境地图。

当智能体到达目标目的地（例如以一对经纬度坐标指定）时会获得奖励，就像一个接到源源不断送货任务却没有地图的快递员。随着时间推移，AI 智能体学会了以这种方式横穿整座城市。我们还证明，智能体可以在多座城市中学习该任务，然后稳健地适应一座新城市。

![一段动画 GIF，展示 AI 智能体以第一人称视角在巴黎通过 Google Street View 导航，叠加的航拍小地图显示其实时路径和位置追踪。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622681de9a678443ffbca1e1_Stop20Motion.gif)

在巴黎训练的智能体的定格动画。图像叠加了城市地图，其中显示目标位置（红色）以及智能体的位置和视野（绿色）。注意，智能体并看不到地图，只能看到目标位置的经纬度坐标。

## 不建地图地学习导航

我们有别于依赖显式建图与探索的传统方法（就像地图绘制者一边定位自己一边绘制地图）。相反，我们的方法是像人类过去那样学会导航：不靠地图、GPS 定位或其他辅助手段，只使用视觉观察。我们构建了一个神经网络智能体，输入从环境中观察到的图像，预测它在该环境中应采取的下一个动作。我们使用深度强化学习对其进行端到端训练，与近来一些关于[在复杂 3D 迷宫中学习导航](https://arxiv.org/pdf/1611.03673.pdf)和[结合无监督辅助任务的强化学习](https://arxiv.org/pdf/1611.05397.pdf)玩游戏的工作类似。与那些在小规模模拟迷宫环境中进行的研究不同，我们使用的是城市尺度的真实世界数据，涵盖伦敦、巴黎和纽约的复杂路口、步道、隧道以及多样的拓扑结构。此外，我们所用的方法既支持针对特定城市的学习与优化，也支持通用的、可迁移的导航行为。

## 可迁移至新城市的模块化神经网络架构

我们智能体内部的神经网络由三部分组成：1) 一个能够处理图像并提取视觉特征的卷积网络；2) 一个地区特定（locale-specific）的循环神经网络，它隐性地承担着记忆环境的任务，并学习「这里」（智能体当前位置）和「那里」（目标位置）的表征；3) 一个地区无关（locale-invariant）的循环网络，针对智能体的动作生成导航策略。地区特定模块被设计为可替换的，顾名思义，它对智能体导航的每座城市各不相同；而视觉模块和策略模块则可以是地区无关的。

![模块化神经网络架构示意图：(a) 单城市设置；(b) 为三座城市分别配备地区特定通路的多城市设置；(c) 迁移学习设置，展示智能体适配新城市时被冻结的模块（灰色）。](https://lh3.googleusercontent.com/o8vl9t-boK_7Hp9XPBA9LmUXjH9kZlhQGV3LlfxR3_c2Jy1q2tRpF-BgDjnAwyHMIUjoMloL1dzQzSo3gEmoDcGkg6XZo3vsOrf607MPBEgCsM8n-Q=w1440)

CityNav 架构 (a)、为每座城市配备地区特定通路的 MultiCityNav 架构 (b) 的对比，以及将智能体适配到新城市时的训练与迁移流程示意 (c)。

与 Google Street View 界面一样，智能体可以在可能的情况下原地旋转，或前进到下一个全景图。与 Google Maps 和 Street View 环境不同的是，智能体看不到小箭头、局部或全局地图，也看不到著名的「谷歌小人」（Pegman）：它必须学会区分可通行的道路与人行道。目标目的地在现实世界中可能相隔数公里，智能体需要走过数百个全景图才能抵达。

我们证明了所提方法可以提供一种向新城市迁移知识的机制。与人类一样，当我们的智能体来到一座新城市时，我们预期它需要学习一套新的地标，但不必重新学习其视觉表征或行为（例如沿街道前进或在路口转弯）。因此，使用 MultiCity 架构，我们先在若干城市上训练，然后冻结策略网络和视觉卷积网络，只在新城市上训练一个新的地区特定通路。这种方法使智能体能够获取新知识而不遗忘已学内容，类似于[渐进神经网络（progressive neural networks）](https://arxiv.org/pdf/1606.04671.pdf?)架构。

![一张图，展示本研究所使用的曼哈顿五个区域：下曼哈顿、格林威治村、中城、中央公园和哈莱姆。](https://lh3.googleusercontent.com/qJZSpzPTn8JJE2-mLbrQOmBZDbmFKKY1InOKlbPCWvxm66cAE6jIGPyZlrQ5hA27jYKxjsBYVwtS5u7nvXnWQMTXgyuK-DWpYLM3K4TeLQrnvDXB=w1440)

本研究所使用的曼哈顿五个区域

研究导航是人工智能研究与发展的基础性课题，而尝试在人工智能体中复现导航，也能帮助科学家理解其生物学基础。
