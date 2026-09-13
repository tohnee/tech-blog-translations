---
title: "我们如何用 AI 支持更好的热带气旋预测"
title_en: "How we're supporting better tropical cyclone prediction with AI"
source: https://deepmind.google/blog/how-were-supporting-better-tropical-cyclone-prediction-with-ai/
site: deepmind
date: 2025-06-12
crawled: 2026-09-13
translated: 2026-09-13
---

# 我们如何用 AI 支持更好的热带气旋预测

> 原文：[How we're supporting better tropical cyclone prediction with AI](https://deepmind.google/blog/how-were-supporting-better-tropical-cyclone-prediction-with-ai/) · Google DeepMind

我们正在上线 Weather Lab，发布我们的实验性气旋预测，并与美国国家飓风中心合作，在这个气旋季为他们的预报和警报提供支持。

热带气旋极其危险，威胁生命并肆虐沿途的社区。在过去 50 年里，它们造成了[1.4 万亿美元的经济损失](https://wmo.int/topics/tropical-cyclone)。

这些巨大的旋转风暴也被称为飓风或台风，在温暖的海水上空形成——由热量、水汽和对流驱动。它们对大气条件中哪怕微小的差异都极为敏感，因此出了名地难以准确预报。然而，提高气旋预测的准确性可以通过[更有效的灾害备灾](https://www.nber.org/digest/202409/value-improving-hurricane-forecasts)和更早的撤离来帮助保护社区。

今天，Google DeepMind 与 Google Research 推出 [Weather Lab](https://deepmind.google.com/science/weatherlab?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=)——一个用于分享我们人工智能（AI）天气模型的交互式网站。Weather Lab 的核心是我们最新的实验性 AI 热带气旋模型，基于随机神经网络构建。该模型可以预测气旋的生成、路径、强度、大小和形状——生成 50 种可能情景，最远可提前 15 天。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![你的浏览器不支持视频标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

动画展示我们实验性气旋模型的一个预测。我们的模型（蓝色）在气旋 Honde 和 Garance 活跃期间准确预测了它们在马达加斯加以南海域的路径。我们的模型还捕捉到了印度洋上气旋 Jude 和 Ivone 将近 7 天之后的路径，稳健地预测出那些最终将增强为热带气旋的风暴天气区域。

我们发布了一篇[新论文](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/how-we-re-supporting-better-tropical-cyclone-prediction-with-ai/skillful-joint-probabilistic-weather-forecasting-from-marginals.pdf?utm_source=&utm_medium=&utm_campaign=&utm_content=)介绍我们的核心天气模型，并在 Weather Lab 上提供历史气旋路径数据档案，用于评估和回测。

内部测试显示，我们模型对气旋路径和强度的预测与当前基于物理的方法同样准确，且往往更加准确。我们一直在与美国国家飓风中心（[NHC](https://www.nhc.noaa.gov/)）合作——该机构负责评估大西洋和东太平洋盆地的气旋风险——以对我们方法和输出进行科学验证。

NHC 的专家预报员现在可以实时查看我们实验性 AI 模型的预测，与其他基于物理的模型和观测并列。我们希望这些数据能帮助改进 NHC 的预报，为与热带气旋相关的灾害提供更早、更准确的预警。

## Weather Lab 的实时与历史气旋预测

[Weather Lab](https://deepmind.google.com/science/weatherlab?utm_source=&utm_medium=&utm_campaign=&utm_content=) 展示不同 AI 天气模型的实时与历史气旋预测，以及来自欧洲中期天气预报中心（[ECMWF](https://www.ecmwf.int/)）的基于物理的模型。我们的多个 AI 天气模型正在实时运行：WeatherNext Graph、WeatherNext Gen 以及我们最新的实验性气旋模型。我们还在上线时提供了两年多的历史预测，供专家和研究者下载与分析，从而能够对我们模型在所有大洋盆地进行外部评估。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![你的浏览器不支持视频标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

动画展示我们的模型对气旋 Alfred 在珊瑚海达到 3 级气旋时的预测。模型的集合平均预测（加粗蓝线）正确预见了气旋 Alfred 将迅速减弱为热带风暴，并在 7 天后在澳大利亚布里斯班附近登陆，且以较高概率沿昆士兰海岸某处登陆。

Weather Lab 用户可以探索并比较各种 AI 与物理模型的预测。把这些预测放在一起解读，可以帮助气象机构和应急服务专家更好地预判气旋的路径与强度。这有助于专家和决策者更好地为不同情景做准备、传达相关风险信息，并支持管理气旋影响的决策。

需要强调的是，Weather Lab 是一个研究工具。所展示的实时预测由仍在开发中的模型生成，并非官方警报。使用该工具时请牢记这一点，包括基于 Weather Lab 生成的预测来支持决策时。获取官方天气预报和警报，请查询你所在地的气象机构或国家气象局。

## AI 驱动的气旋预测

在基于物理的气旋预测中，为满足业务运行需求所做的近似意味着单一模型很难同时在气旋路径和强度预测上都表现出色。这是因为气旋的路径由广域大气引导气流主导，而气旋的强度则取决于其致密核心内部及其周围的复杂湍流过程。全球低分辨率模型在预测气旋路径上表现最佳，但无法捕捉决定气旋强度的精细尺度过程——这正是需要区域高分辨率模型的原因。

我们的实验性气旋模型是克服这一取舍的单一系统，内部评估显示它在气旋路径和强度上都达到业界领先的准确性。它的训练目标是建模两类不同的数据：一个从数百万条观测中重建过去全球天气的庞大再分析数据集，以及一个专门数据库，包含过去 45 年间近 5000 个已观测气旋的路径、强度、大小和风圈半径等关键信息。

把再分析数据与气旋数据一起建模，极大地提升了气旋预测能力。例如，我们对 NHC 观测飓风数据的初步评估（测试年份为 2023 和 2024 年，覆盖北大西洋和东太平洋盆地）显示，我们模型的 5 天气旋路径预测平均比 ENS——ECMWF 领先的全球物理集合模型——接近真实气旋位置 140 公里。这相当于 ENS 3.5 天预测的精度——而这样 1.5 天的改进以往通常需要[超过十年才能实现](https://ourworldindata.org/grapher/hurricane-track-error)。

虽然以往的 AI 天气模型在计算气旋强度上一直表现不佳，我们的实验性气旋模型超越了美国国家海洋和大气管理局（[NOAA](https://www.noaa.gov/)）飓风分析与预报系统（[HAFS](https://www.aoml.noaa.gov/hurricane-modeling-prediction/#hafs)）的平均强度误差——HAFS 是领先的区域高分辨率物理模型。初步测试还表明，我们模型对大小和风圈半径的预测与物理基线相当。

这里我们可视化路径和强度预测误差，并展示我们的实验性气旋模型提前最多 5 天的平均性能评测结果，与 ENS 和 HAFS 对比。

![四联图对比气旋路径与强度预测误差，展示实验性 AI 模型相对既有模型的准确性](https://lh3.googleusercontent.com/z3RtVV-EUuIRNZQkKDSkjxk6bAOTiAwC4tFvriyZ5GvA3MTNekYtkio2MwujmjF_A-w6EjKncdPN7yoUFCbWLww7lVvu4guQV9A6-4IXXESwW5selLg=w1440)

我们的实验性气旋模型路径与强度预测的评测结果，与领先的物理模型 ENS 和 HAFS-A 对比。我们的评测以 NHC 最佳路径数据为基准真值，并遵循其同质化验证协议。

## 为决策者提供更有用的数据

除了 NHC，我们还一直与科罗拉多州立大学大气研究合作研究所（[CIRA](https://www.cira.colostate.edu/)）紧密合作。CIRA 研究科学家 Kate Musgrave 博士和她的团队评估了我们的模型，认为它「在路径和强度上具备与最佳业务模型相当或更高的技巧水平」。Musgrave 表示：「我们期待在 2025 年飓风季的实时预报中确认这些结果。」我们还与[英国气象局](https://www.metoffice.gov.uk/)、[东京大学](https://www.u-tokyo.ac.jp/en/)、日本 [Weathernews Inc.](https://global.weathernews.com/) 等机构及其他专家合作，以改进我们的模型。

我们新的实验性热带气旋模型是我们一系列开创性 [WeatherNext 研究](https://deepmind.google/science/weathernext/?utm_source=&utm_medium=&utm_campaign=&utm_content=)中的最新里程碑。通过 Weather Lab 负责任地分享我们的 AI 天气模型，我们将继续收集气象机构和应急服务专家的重要反馈，了解我们的技术如何改进官方预报、辅助拯救生命的决策。

[访问 Weather Lab](https://deepmind.google.com/science/weatherlab?utm_source=&utm_medium=&utm_campaign=&utm_content=)[阅读我们的论文](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/how-we-re-supporting-better-tropical-cyclone-prediction-with-ai/skillful-joint-probabilistic-weather-forecasting-from-marginals.pdf?utm_source=&utm_medium=&utm_campaign=&utm_content=)

**致谢**
本研究由 Google DeepMind 与 Google Research 共同开发。

我们感谢合作方 NOAA 的 NHC、CIRA、英国气象局、东京大学、日本 Weathernews Inc.、FOX Weather 的 Bryan Norcross，以及在整个 Weather Lab 开发过程中提供了宝贵反馈的其他可信测试者合作伙伴。
