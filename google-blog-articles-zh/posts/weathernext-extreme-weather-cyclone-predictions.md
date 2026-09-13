---
title: "问问科学家：研究人员如何用 AI 预测气旋？"
title_en: "Ask a Scientist: How do researchers use AI to predict a cyclone?"
source: https://blog.google/innovation-and-ai/models-and-research/google-deepmind/weathernext-extreme-weather-cyclone-predictions/
site: google-blog
date: 2026-09-01
crawled: 2026-09-13
translated: 2026-09-13
---

# 问问科学家：研究人员如何用 AI 预测气旋？

> 原文：[Ask a Scientist: How do researchers use AI to predict a cyclone?](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/weathernext-extreme-weather-cyclone-predictions/) · Google

随着极端天气事件影响全球更多社区，准确预测风暴路径的能力对保障人们安全至关重要。通过将数十年的历史大气数据与先进 AI 相结合，Google 的研究人员在气旋预报精度上实现了[巨大飞跃](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/weathernext-2-cyclones/)——把过去需要大楼般庞大的超级计算机才能完成的工作，变成了可以在单个 TPU 上运行的救命模型。我们与帮助开发 [WeatherNext](https://deepmind.google/science/weathernext/) 模型的 Google DeepMind 研究科学家 Ferran Alet 进行了对谈，探讨这项突破性技术如何在气旋来袭前，为人们和第一响应者争取到宝贵的时间。

**你在 Google 做什么工作？**

我来自学术界，之前的研究探索 AI 与物理学的交叉，之后加入了 Google DeepMind 的天气团队。现在，我把这一背景用于将 AI 应用到传统的基于物理的模型中，以更好地预测未来的天气。我的团队负责 WeatherNext 预报模型，我们构建它们是为了帮助气象学家和科学家获取 AI 驱动的极端天气预测。这些预测帮助人们在气旋等可能造成毁灭性影响的天气事件到来之前，获得更准确的预报和预警。

**在继续之前先问一句：气旋、飓风、台风——到底该叫什么？**

它们其实是同一个东西！气旋（cyclone）是飓风和台风的全球科学统称。在大西洋地区，人们称之为飓风（hurricane）；在北太平洋，则叫台风（typhoon）。但所有这些名称指的都是同一种在温暖海洋上形成的大尺度旋转风暴系统。海洋的温暖使温暖湿润的空气上升，在下方形成低压区并吸入较冷的空气。地球的自转让这种"湿空气上升、冷空气汇入"的循环旋转起来。再加上暴雨和强风，你就得到了一个气旋……或者叫飓风、台风，取决于你住在哪里。

**过去研究人员是如何预测气旋的？**

过去，气旋预报依赖于由集装箱大小、甚至三层楼高的超级计算机驱动的物理模型。科学家用这些机器模拟流体力学定律，基于全球传感器提供的*当前*天气数据预测未来的天气。但这些全球传感器的数据往往不完整或充满噪声，而模拟精确物理需要巨大的算力，这拖慢了我们在气旋等预报上取得进展的速度。气象界历来大约每十年才能提高一天的预报准确度，靠的是构建更好的模型、发射更多卫星和获得更多算力。通过将 AI 应用于这些物理模型的数据，我们在 WeatherNext 模型的一次代际跃迁中就看到了同样的[十年进步](https://deepmind.google/blog/weathernext-ai-model-achieves-breakthrough-in-forecasting-cyclones/)。

**我们如何用 AI 改变气旋预测的方式？**

物理模型非常擅长告诉我们过去和现在的情况。AI 则让我们能够根据过去的模式和现在的数据，更好地预测未来。在 WeatherNext 中，我们用 50 年的历史天气数据训练 AI。研究人员无需依赖大楼般的超级计算机，就可以在单个 TPU 上运行这些更快的模型。这给科学界带来了准确度的巨大飞跃，同时改进了对气旋将在何处登陆以及登陆时强度如何的预测。气象机构正着眼于将公共预报时效从 5 天延长到 7 天，为社区在气旋来袭前争取关键的额外准备时间。

**这些额外的时间能给需要的人带来怎样的改变？**

去年飓风 [Melissa](https://deepmind.google/blog/how-weathernext-helped-the-national-hurricane-center-better-predict-hurricane-melissas-historic-landfall-in-jamaica)（梅丽莎）来袭时，我们看到了这段时间有多么关键。在飓风季到来之前，我们与国家飓风中心（National Hurricane Center）合作，为他们的预报提供支持。Melissa 的特别之处在于：虽然这场飓风起初看起来很弱，但 AI 的高置信度预测帮助国家飓风中心发布了一份历史性的预报，提醒当局注意它将从 1 级风暴快速增强为 5 级。事实证明，它是史上最强的飓风之一，而我们的模型在它登陆前好几天就预见到了这一点。多出的一天预警时间让牙买加当局得以做出挽救生命的应急准备。

**像 WeatherNext 这样的技术对极端天气预报的未来意味着什么？**

我们已经[开源](https://github.com/google-deepmind/weathernext)了 WeatherNext 2 和 WeatherNext 气旋模型，并开发了交互式 [Weather Lab](https://deepmind.google.com/science/weatherlab) 网站，为全球科学界推进科学研究。这种广泛的开放获取帮助学者和科学家自由地试验这些模型，并有望做出帮助世界各地人们的新发现。
