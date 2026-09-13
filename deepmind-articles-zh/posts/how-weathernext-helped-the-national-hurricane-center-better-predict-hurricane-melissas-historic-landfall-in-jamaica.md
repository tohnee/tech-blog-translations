---
title: "WeatherNext 如何帮助国家飓风中心更好地预测飓风 Melissa 在牙买加的历史性登陆"
title_en: "How WeatherNext helped the National Hurricane Center better predict Hurricane Melissa’s historic landfall in Jamaica"
source: https://deepmind.google/blog/how-weathernext-helped-the-national-hurricane-center-better-predict-hurricane-melissas-historic-landfall-in-jamaica/
site: deepmind
date: 2026-05-19
crawled: 2026-09-13
translated: 2026-09-13
---

# WeatherNext 如何帮助国家飓风中心更好地预测飓风 Melissa 在牙买加的历史性登陆

> 原文：[How WeatherNext helped the National Hurricane Center better predict Hurricane Melissa’s historic landfall in Jamaica](https://deepmind.google/blog/how-weathernext-helped-the-national-hurricane-center-better-predict-hurricane-melissas-historic-landfall-in-jamaica/) · Google DeepMind

国家飓风中心得以提前发布天气预警，为牙买加社区争取到更多提前量去准备、撤离并保护生计。

2025 年 10 月，飓风 Melissa 创造了历史。它是有记录以来登陆牙买加的最强飓风，并并列成为大西洋最强的飓风。

国家飓风中心（NHC）的预报同样标志着一个历史性里程碑。他们首次从 1 级风速起报，预测一场风暴将达到 5 级强度。我们的 AI 模型 [WeatherNext](https://deepmind.google/science/weathernext/) 帮助 NHC 做出了这一决策——它以高置信度预测了这场风暴的快速增强和在牙买加的登陆，而最关键的是，这一预测提前了五天。

更早、更准确地预测危险风暴，有助于地面团队更好地调动资源、有效协调撤离。

[您的浏览器不支持 video 标签。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/9LLVffEBUW8TWF_I/weathernext__case-study__bg.webm)

观看 WeatherNext 如何为 2025 年的飓风 Melissa 及其以 5 级强度在牙买加登陆提供准确、早期的预报。

## 快速增强的挑战

预测风暴的路径很难，而预测强度的突然跃升——即所谓的「快速增强（rapid intensification）」——更是难上加难。这种情况发生在飓风风速在短短 24 小时内增加至少 35 英里/小时的时候。这类事件极难预测，也极其危险，因为一个弱的系统可以一夜之间变成强飓风，几乎没有时间做防备。

> 热带风暴和飓风在结构和强度上都可能变化非常快，这使得它们比其他类型的天气系统更难预测。

Michael Brennan

国家飓风中心主任

从历史上看，气象学家面临一种取舍：大型全球模式擅长预测风暴路径，但往往缺乏分辨率，看不清驱动风暴「引擎」的小尺度雷暴；反过来，高分辨率局地模式能更好地把握强度，却缺乏准确预报路径所需的全球背景。这意味着模式要么在预测热带气旋路径上表现出色，要么在强度上表现出色，但无法两者兼得。

## WeatherNext 带来的科学突破

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

从登陆前七天到 2025 年 10 月 28 日（飓风 Melissa 以 5 级强度登陆牙买加当天）的飓风 Melissa 预测路径集合。

由 Google DeepMind 和 Google Research 开发的我们的 AI 天气模型 WeatherNext，凭借在路径和强度预测上的双双出色表现，弥合了这一历史性鸿沟。作为 Google [Earth AI](https://ai.google/earth-ai/) 计划的一部分，该模型通过在数十年的全球天气模式以及极端热带气旋的专门数据集上训练，实现了这种双重能力。

WeatherNext 不只是提供一个单一的「最佳猜测」，它还可以运行由 50 个不同「假设情境」组成的集合（ensemble），为专家提供更宽的可能性范围以辅助决策。我们通过 [Weather Lab](https://deepmind.google.com/science/weatherlab?utm_source=&utm_medium=&utm_campaign=&utm_content=&_gl=1*147gps6*_ga*MTIxNTc3OTU3MC4xNzc2MTY5NzM4*_ga_LS8HVHCNQ0*czE3NzYxNjk3MzgkbzEkZzEkdDE3NzYxNjk4MjQkajU3JGwwJGgw) 将这些数据作为实验性展示向所有人开放。

当飓风 Melissa 最初被识别为一个弱热带低压时，传统模式在「它将以弱系统袭击海地」还是「向牙买加方向增强」之间摇摆不定。而 WeatherNext 提前五天以 80% 的置信度预测它将以 5 级强度登陆牙买加，到提前三天时置信度升至接近 100%。这是首次有风暴从如此低的初始风速被成功预测达到 5 级强度。从如此不起眼的起点识别出顶级飓风，标志着在预判极端增强事件能力上的历史性转折点。

Melissa 在大西洋飓风季的末段来袭，此时 NHC 的预报员已经花了几个月时间验证 WeatherNext 并对其建立信心。平均而言，WeatherNext 在路径和强度两方面都始终表现卓越。这一表现让预报员在像 Melissa 这样的情形中充满信心——在这种情形下，强度和登陆预测都至关重要。

![WeatherNext 在预测热带气旋路径和强度方面达到最先进水平。图表显示 2025 年大西洋与北太平洋合并区域的加权平均数据。](https://lh3.googleusercontent.com/fBWnJ6TUGlMVaR27KiPpDJouf9hm9WXsvcNnDG-ZqoCUTGOQtvUeWPET_JG0v1lNES5D7uDtJ37mKEKHoXhwpQps0-IIXzOQ1mNpAtB_hSzJTfKqRAw=w1440)![WeatherNext 在预测热带气旋路径和强度方面达到最先进水平。图表显示 2025 年大西洋与北太平洋合并区域的加权平均数据。](https://lh3.googleusercontent.com/Iy_incPkUbjZSNlR5gyVUMhKzN3kJLNgnXiQoQTSVfn3hp414r4IaP96dyViiWf6ZZijVwlsY3hoLoQcUv1wX2luxDrnHkJXRHnEOkps9sKRDqhm1g=w1440)

WeatherNext 在预测热带气旋路径和强度方面表现卓越。图表显示 2025 年各大业务模式在大西洋与北太平洋合并区域的加权平均数据。图表根据 [NHC 年度验证报告](https://www.nhc.noaa.gov/verification/pdfs/Verification_2025.pdf)中的数据编制。

## 帮助保护地面上的社区

![牙买加气象局首席主管 Evan Thompson 在阴天的天空下，从屋顶露台眺望金斯顿市。](https://lh3.googleusercontent.com/KTo4xuv5qXlJDL7NEAWoOL0G81yB3YYpNfzuru9uWpDrxNP81agTvxtIn2-CXsKIqFmUaFK2NqYqmKdEAR5BqHYUTBB0d06yUzumijBZmOaPDVP2=w1440-h810-n-nu)

Evan Thompson 是牙买加气象局（Meteorological Service Jamaica）首席主管，常驻牙买加金斯顿。

NHC 担任世界气象组织（WMO）负责大西洋和东太平洋热带气旋的区域专业气象中心，为近 30 个国家提供预报和警报。

在 WeatherNext 的预测，以及 HAFS 等基于物理的模式、来自卫星和「飓风猎人」飞机的实时数据的支持下，NHC 得以为牙买加气象局提供前所未有的提前量。这使当地官员得以调动资源、有效协调撤离。

> 有了提前撤离和更充分的准备，危害的减少确实会给我们的人民带来真正的改变。[...] 它真的能挽救他们的生命，并保住他们想要守护的生计。

Evan Thompson

牙买加气象局首席主管

## 将安全扩展到全球

WeatherNext 在飓风 Melissa 期间发挥的作用，是 Google 与 NHC 多年合作的成果。在 2025 年整个飓风季中，[NHC 年度验证报告](https://www.nhc.noaa.gov/verification/pdfs/Verification_2025.pdf)发现，WeatherNext 是支持专家决策的路径与强度预测中表现最佳的单一模式。随着即将到来的飓风季拉开帷幕，我们将继续与 NHC 并肩工作。我们将继续作为 NHC 路径与强度指导套件中不可或缺的一部分，并希望我们的模型能为他们挽救生命的关键工作提供支持。

我们也在积极地将这些研究能力带给其他受灾严重的地区，包括菲律宾（PAGASA）、台湾（CWA）、印度尼西亚（BMKG）和越南（VNMHA）。未来的优先事项还包括与日本、澳大利亚和印度的本地机构开展合作，我们希望与当地专家继续推进这项研究。在所有这些研究工作中，所有官方天气警报与警告均仅由各自国家的气象主管机构发布。

通过将 AI 的速度与准确性与专家预报员不可替代的经验相结合，我们的目标是降低自然灾害造成的[人员与经济](https://www.nber.org/digest/202409/value-improving-hurricane-forecasts)损失。

我们已将这项技术集成到 Search 中 NOAA 覆盖地区的预报中，并正努力将访问范围扩展到其他地区。

**注意：官方天气预报与警报请以你所在地的气象机构或国家天气服务为准。**

[访问 Weather Lab](https://deepmind.google.com/science/weatherlab?utm_source=&utm_medium=&utm_campaign=&utm_content=&_gl=1*147gps6*_ga*MTIxNTc3OTU3MC4xNzc2MTY5NzM4*_ga_LS8HVHCNQ0*czE3NzYxNjk3MzgkbzEkZzEkdDE3NzYxNjk4MjQkajU3JGwwJGgw)[阅读 NHC 关于飓风 Melissa 的报告](https://www.nhc.noaa.gov/data/tcr/AL132025_Melissa.pdf)[阅读 NHC 关于 2025 年飓风季的报告](https://www.nhc.noaa.gov/verification/pdfs/Verification_2025.pdf)

## 致谢

我们感谢 Ferran Alet, Tom Andersson, Ilan Price, Stratis Markou, Andrew El-Kadi, Dominic Masters, Amy Li, Samier Merchant, Natalie Williams, Gregory Thornton, Ken MacKay, Olivia Graham, Ben Gaiarin, Elinor Kruse, Akib Uddin, Juanita Bawagan, Armin Senoner, Devaja Shah, Jacklynn Stott, Remi Lam, Aaron Bell, Paul Komarek, Matthew Willson, Alvaro Sanchez-Gonzalez 和 Peter Battaglia。

我们还感谢国家飓风中心、英国气象局（UK Met Office）和大气研究合作研究所（Cooperative Institute for Research in the Atmosphere）的团队。

最后，我们感谢 Raia Hadsell、Zoubin Ghahramani、Yossi Matias 和 Demis Hassabis 对这项工作的支持。
