---
title: "Open Buildings：为瞬息万变的世界绘制 AI 驱动的地图"
title_en: "Open Buildings: AI-powered maps for a changing world"
source: https://blog.google/innovation-and-ai/technology/research/open-buildings-ai-powered-maps-for-a-changing-world/
site: google-blog
date: 2024-09-19
crawled: 2026-09-13
translated: 2026-09-13
---

# Open Buildings：为瞬息万变的世界绘制 AI 驱动的地图

> 原文：[Open Buildings: AI-powered maps for a changing world](https://blog.google/innovation-and-ai/technology/research/open-buildings-ai-powered-maps-for-a-changing-world/) · Google

根据联合国的数据，到 2050 年，全球城市人口将新增约 25 亿，其中大部分增长来自[全球南方](https://en.wikipedia.org/wiki/Global_North_and_Global_South#:~:text=According%20to%20UN%20Trade%20and,excluding%20Australia%20and%20New%20Zealand).)的人口增长与人口流动。我们需要新的工具来理解城市是如何随时间增长和变化的，从而确保所有居民都被纳入决策以及自来水、电力等基本服务的规划之中。

今天，我们正在扩展 [Open Buildings 项目](https://sites.research.google/open-buildings/)——该项目旨在帮助各类组织理解并规划这个不断变化的世界——推出一个新的数据集，其中包含建筑存在状况随时间变化的信息。[Open Buildings 2.5D 时序数据集（Open Buildings 2.5D Temporal Dataset）](https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_Research_open-buildings-temporal_v1)现已提供 2016-2023 年的数据，并首次包含建筑高度信息。

## 为什么绘制建筑地图很重要

地图是通往我们所需许多事物的生命线。要让人们获得电力、自来水等基本服务，并在危机响应中被纳入考量，决策者首先需要知道他们在哪里。通过制作地图，我们可以帮助决策者了解当前环境，确保每个人都被覆盖。正因如此，Google Research 于 2021 年启动了 Open Buildings 项目。这一项目始于我们在加纳阿克拉（Accra）的 AI 研究实验室，已绘制了非洲、亚洲、拉丁美洲和加勒比地区 18 亿栋建筑的地图，覆盖全球约 40% 的陆地面积和约 54% 的世界人口。

过去几年，各国政府、人道主义组织、研究者和企业已将 Open Buildings 数据集用于各种项目。例如，乌干达非营利组织 [Sunbird AI](https://sunbird.ai/) 利用 Open Buildings 数据集为农村电气化项目确定优先区域，把影响最大化地投放到需求最迫切的地方。这类数据可以服务于多种用途，我们也用它提升了 Google 地图（Google Maps）的准确性，为世界各地的地图添加了建筑信息。

随着时间的推移，随着合作伙伴将数据用于各自的项目，一些重要的问题开始浮现：这些建筑是何时建造的？这座城市或定居点随时间发生了怎样的变化？在最近一次危机事件之前，这个地方是什么样子，现在又是什么样子？

由于种种原因，要回答这些问题可能很困难，有时甚至不可能。例如，在资源往往稀缺的低收入和中等收入国家，这类数据可能并不存在。冲突可能普遍存在，导致数据无法记录。或者地形本身就构成障碍。但随着世界人口每年增长超过 8,000 万，获取这些信息比以往任何时候都更加重要，尤其是对于研究发展趋势和城市化的政府机构、人道主义组织和研究者而言。

## 我们如何制作这个新数据集

为制作这一数据集，我们使用 AI 对 Sentinel-2 数据集中公开可得的较低分辨率影像进行超分辨率处理，并从中提取建筑轮廓和高度。这一点很重要，因为与高分辨率影像相比，较低分辨率的卫星影像在全球南方更容易获得，所以我们需要构建能够利用这些较低保真度的影像准确分类建筑的模型。

我们正在发布[技术报告](https://arxiv.org/abs/2310.11622)以及一个[可交互的 Earth Engine 应用](https://mmeka-ee.projects.earthengine.app/view/open-buildings-temporal-dataset)，任何人都可以从中更详细地探索我们的方法和结果。

我们还将 Open Buildings 2.5D 时序数据集免费开放，以支持政策制定者、人道主义组织以及其他在全球南方工作的机构。它以 ImageCollection 的形式托管在 Earth Engine 数据目录（[链接](https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_Research_open-buildings-temporal_v1)）中，可以借助 Earth Engine 行星尺度的计算能力和庞大的其他环境数据集目录进行分析。

过去三十年，加纳的城市人口增长了两倍多。加纳第二大城市库马西（Kumasi）近年来发展迅猛。在这里，我们看到库马西郊外村庄 Pramso 的快速扩张。

2018 年 9 月 28 日，印度尼西亚近海发生 7.4 级地震并引发海啸，影响了苏拉威西岛（Sulawesi）约 150 万人。这场危机之后，建成区从海岸线后退，地震的影响在数据中清晰可见。

这些只是几个例子。你可以在我们的[完全可交互的 Earth Engine 应用](https://mmeka-ee.projects.earthengine.app/view/open-buildings-temporal-dataset)中探索整个数据集。

## 我们如何通过合作扩大影响

我们正在与将数据用于各类有影响力的项目的合作伙伴展开协作。例如，[WorldPop](https://www.worldpop.org/) 正在利用 Open Buildings 为全球生成最新、准确的人口估计。WorldPop 的估计数据被各国政府和联合国机构采用。WorldPop 还与尼日利亚的合作伙伴合作，利用这些数据识别并联系尚未接受常规免疫服务的儿童。"了解人们居住在哪里，对于确保资源公平分配、确保在提供医疗等服务时不落下任何一个人至关重要，"WorldPop 团队负责人 Andrew Tatem 教授解释道，"Google 的 Open Buildings 数据集为我们领域的开放数据增添了绝佳的一笔，支持了更准确的人口制图，而新的时序数据集则开启了更好地捕捉我们持续在全球目睹的快速人口变化的机会。"

Sunbird AI 正在与联合国全球脉动（UN Global Pulse）合作开展的 [Data Cities](https://www.datacities.ug/) 项目中使用我们的数据集，为乌干达两座新兴城市——堡港（Fort Portal）和金贾（Jinja）——创建全面的城市画像。其目标是利用地理空间数据为市政当局提供所需工具，支持他们在城市规划和政策上做出明智决策，并理解他们需要应对的更宏观的趋势。

## 局限性与我们着力改进的方向

我们在卫星影像分割、超分辨率和高程估计等方面的 AI 创新，创建了一个动态的全球数据集，让整个世界都被绘制在地图上。尽管如此，仍然存在一些可能影响数据质量、使我们无法准确绘制某些建筑的局限。

- **晴朗的天空是关键：** 我们需要一系列无云影像才能获得最佳结果。在一些多云严重的地区，这可能成为问题，导致数据可靠性下降。你可能会注意到某些年份的置信度分数较低。
- **极小的建筑可能被遗漏：** 我们能够发现比单个影像像素还小的建筑，但存在极限。非常小的建筑——比如临时搭建的棚屋——可能不会显现。
- **像素而非多边形：** 之前的数据集包含建筑的几何形状，但鉴于 Sentinel-2 输入数据分辨率较低，这一点很难实现。因此，我们关于建筑存在状况的数据以栅格（raster）格式提供，每个像素附带一个置信度分数。
- **其他问题：** 还有一些其他技术问题可能影响数据，例如影像拼接错误和一些假阳性（检测到并不存在的东西）。我们在[网站](https://sites.research.google/gr/open-buildings/temporal/)上对这些做了更详细的说明。

地图是动态的——因为世界一直在变化。借助 Open Buildings 2.5D 时序数据集，AI 帮助我们理解这种变化。我们期待把这一信息提供给那些支持可持续和包容性城市发展的合作伙伴，帮助每一个人都出现在地图上。

我们邀请世界各地的研究者、政策制定者和发展实践者探索 Open Buildings 2.5D 时序数据集，并与我们分享你的反馈。
