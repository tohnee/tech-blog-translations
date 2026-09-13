---
title: "我们如何构建了大脑活动研究中最具雄心的数据集之一"
title_en: "How we built one of the most ambitious datasets in brain activity research"
source: https://blog.google/innovation-and-ai/technology/research/zapbench-zebrafish-brain-mapping/
site: google-blog
date: 2025-06-09
crawled: 2026-09-13
translated: 2026-09-13
---

# 我们如何构建了大脑活动研究中最具雄心的数据集之一

> 原文：[How we built one of the most ambitious datasets in brain activity research](https://blog.google/innovation-and-ai/technology/research/zapbench-zebrafish-brain-mapping/) · Google

近十年来，Michał Januszewski 一直在思考鱼在想些什么。

Michał 隶属于 Google Research，该团队正与 HHMI Janelia 和哈佛大学的合作者一起，构建迄今为止大脑活动研究领域最具雄心的数据集之一：一个同时追踪单条幼年斑马鱼整个大脑的神经活动与纳米尺度结构的数据集——这可能为我们理解自身的大脑带来重大突破。

"多年来，我们团队一直专注于所谓的连接组学（connectomics），研究的是大脑的结构测绘——我们对大脑的微小片段拍摄极高分辨率的图像，并尝试识别所有细胞以及它们之间的所有连接，"Michał 说。"这能给你一个大脑在任意给定时刻的静态快照，却无法告诉你大脑在真正活着、进行思考时正在做什么。"

因此，Michał 的团队着手构建一个新的多模态数据集，能够预测并展示生物体思考时的神经活动。他们选择从斑马鱼入手，因为它符合几个关键条件：斑马鱼是脊椎动物，大脑功能比昆虫等动物更为复杂，而且它的大脑足够小，团队可以获得整个大脑的数据集，而不只是其中极小的一部分。

而且——或许最为关键的是——刚孵化的斑马鱼几乎完全透明，这使得团队能够使用一套专用激光装置，扫描一条活鱼大脑中超过 70,000 个神经元近两个小时的大脑活动——此时鱼正在对周围投射的各种图案与刺激做出反应。

今年 4 月，Google Research 将这些数据发布为同类首个基准测试，名为 [ZAPBench](https://github.com/google-research/zapbench)（Zebrafish Activity Prediction Benchmark，斑马鱼活动预测基准），它能够帮助推动神经科学的发展，让开发出可以预测大脑活动的更精确 AI 模型成为可能。

研究人员使用光片显微镜记录幼年斑马鱼的大脑活动。

![蓝光照射下培养皿中的斑马鱼，周围环绕着三个显微镜镜头](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/ZAPBench_Diagram.width-1200.format-webp.webp)

Google 的研究人员已经创建了大量 AI 模型基准测试，以推动其他领域模型的改进，例如用于改进天气预报的 [WeatherBench 2](https://sites.research.google/weatherbench/)，或面向语言模型的 [One Billion Word Benchmark](https://research.google/pubs/one-billion-word-benchmark-for-measuring-progress-in-statistical-language-modeling/)。然而，ZAPBench 填补的是一个独特的需求。要复核 AI 模型对天气预测之类结果的准确性并不难——比如把头伸出窗外看看——但对于大脑活动的预测模型，却没有什么简单的检验办法，因为获取扫描数据本身就十分困难。

"神经科学研究者一直在构建关于大脑如何工作的模型，但很少有机会实际检验这些模型预测大脑活动的能力，"研究科学家 Viren Jain 说。"有了 ZAPBench，任何人都可以创建模型并进行评估，既可以对照基准测试，也可以与其他模型比较。"Google 团队在自己的测试中已经看到了一些有趣的结果，例如模型往往在大脑的特定区域出现预测错误，而在预测其他区域的活动时则更为准确。

原始记录的大脑活动数据（左），以及 ZAPBench 能够帮助进行基准测试的预测大脑活动图像（右）。

创建 ZAPBench 只是第一步。Google Research 团队还在既有工作的基础上继续推进：为这条被成像记录过活动数据的幼年斑马鱼大脑的数万个神经元绘制连接组。他们希望通过把特定标本大脑的连接组与该大脑的活动配对，我们能够在基础层面获得关于大脑工作方式的新洞见——无论是对于鱼类，还是有一天甚至对于人类。

"这里的长远目标是弄清大脑在真正的机制层面是如何运作的，"Viren 说。"如果我们能开发出一个模型，更好地预测所有这些不同组件如何驱动大脑活动，这将显著提升大脑工作基础模型的水平以及我们对它们的信心——这可能推动医学、脑机接口或未来各种有益应用的发展。"
