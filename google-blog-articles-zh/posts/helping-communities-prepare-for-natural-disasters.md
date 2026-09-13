---
title: "迈向一个没有人会被自然灾害打个措手不及的世界"
title_en: "Towards a world where no one is surprised by a natural disaster"
source: https://blog.google/innovation-and-ai/technology/research/helping-communities-prepare-for-natural-disasters/
site: google-blog
date: 2026-06-23
crawled: 2026-09-13
translated: 2026-09-13
---

# 迈向一个没有人会被自然灾害打个措手不及的世界

> 原文：[Towards a world where no one is surprised by a natural disaster](https://blog.google/innovation-and-ai/technology/research/helping-communities-prepare-for-natural-disasters/) · Google

世界正经历极端天气事件和自然灾害的急剧增加，许多社区因此遭受重创。过去十年，Google 各团队一直致力于在危机时刻——往往也是人们最需要的时刻——为人们提供有用的信息。

我们推进了基于 AI 的突破性研究，从[提供及时信息](https://blog.google/products-and-platforms/products/search/helping-people-crisis/)逐步走向对自然灾害的预报与监测，包括[野火](https://sites.research.google/gr/wildfires/)、[洪水](https://sites.research.google/gr/floodforecasting/)、[地震](https://research.google/blog/android-earthquake-alerts-a-global-system-for-early-warning/)和[极端天气](https://deepmind.google/science/weathernext/)。我们通过数十亿人使用的 Google 产品让关键信息触手可及，并与世界各国政府与组织合作，帮助社区为这些危机做好准备并加以应对。

危机时刻可行动的信息能够挽救生命与生计：我们[危机韧性](https://crisisresilience.google/)工作的北极星，就是不让任何人被自然灾害打个措手不及。

在今天的 AI for the Planet 活动上，我们分享了为实现这一愿景所取得的进展，把 AI 驱动的工具与洞见交到合作伙伴和用户手中。下面回顾我们一路走来的历程以及未来的方向。

## 推进预报与监测

十年前，大规模可靠的洪水预报在很多人看来遥不可及。我们在[洪水预报](https://sites.research.google/gr/floodforecasting/)上走向全球影响力的多年旅程，始于 2018 年在印度巴特那地区的一项[试点](https://blog.google/products-and-platforms/products/search/helping-keep-people-safe-ai-enabled-flood-forecasting/)，以及一个[假设](https://arxiv.org/abs/1901.09583)：借助机器学习，我们可以帮助大规模[预测洪水](https://sites.research.google/gr/floodforecasting/)。此后，我们逐步推进研究并扩大部署。凭借[发表于 Nature](https://www.nature.com/articles/s41586-024-07145-1) 的河流洪水[全球模型](https://research.google/blog/using-ai-to-expand-global-access-to-reliable-flood-forecasts/)突破，我们把服务扩展到数据稀缺地区；凭借新的 AI 方法论 [Groundsource](https://blog.google/innovation-and-ai/technology/research/gemini-help-communities-predict-crisis/)，我们基于 20 年的公开报告构建了高质量洪水数据集，并用它训练了山洪模型。如今，[Flood Hub](https://sites.research.google/floods/l/0/0/3) 上的预报覆盖 150 多个国家中面临重大洪水事件风险地区的 20 亿人。河流洪水预报可提前最多七天获得；我们在城市地区推出的新山洪预测，可为这类骤发性事件提供最多 24 小时的提前预警。我们已开源[山洪数据集](https://zenodo.org/records/18647054)和[水文框架](https://research.google/blog/the-next-chapter-in-flood-resilience-open-sourcing-googles-hydrology-framework/)，让研究者、企业和本地专家能够构建新的解决方案。

对于气旋等极端天气事件，[WeatherNext 2](https://deepmind.google/science/weathernext/) 带来了我们迄今最精准的预测。它能在几分钟内为全球生成高度精细的逐小时预报，并能预报风速与风向、降水和气压等关键气象变量。在 2025 年飓风季，它成功提前数天、高置信度地预测了气旋的路径和强度。

在[野火](https://sites.research.google/gr/wildfires/)方面，我们利用卫星影像在 Search 和地图中提供基于 AI 的[边界追踪](https://sites.research.google/gr/wildfires/boundary-tracking/)。自[早期工作](https://blog.google/products-and-platforms/products/search/mapping-wildfires-with-satellite-data/)以来，我们的覆盖范围已扩大到 34 个国家，其中今年新增 7 个国家。为了提升未来的火灾探测能力，我们与 [Earth Fire Alliance](https://earthfirealliance.org/) 和 [Muon Space](https://www.muonspace.com/) 共同开发了 [FireSat](https://sites.research.google/gr/wildfires/firesat/)，并获得 [Google.org](http://google.org/)、[Moore Foundation](https://www.moore.org/)、[Bezos Earth Fund](https://www.bezosearthfund.org/news-and-insights/bezos-earth-fund-commits-26-million-to-the-worlds-first-satellite-constellation-dedicated-to-the-global-wildfire-challenge) 等机构的资金支持。首颗原型飞行（protoflight）卫星于去年入轨。完整的 FireSat 星座将由 50 多颗卫星组成，能够探测地球上任何角落仅 5 x 5 米的野火，每 20 分钟更新一次。

为了应对极端高温，我们将 AI 应用于卫星与航空影像，绘制城市环境中建筑的反射率地图，相关成果刚刚[发表](https://www.nature.com/articles/s41467-026-73436-y)。这有助于城市了解如何通过凉爽屋顶（cool roofs）降低地表温度。

单个模型固然强大，但许多现实世界的问题需要整体性的方法。要回答「飓风可能在哪里登陆？哪些社区最脆弱？他们应该如何准备？」这类复杂问题，需要对影像、人口和环境进行综合推理。我们把气候与地理空间模型汇聚在 [Google Earth AI](https://ai.google/earth-ai/) 模型与数据集集合中。它实现了行星尺度智能，正在帮助企业和组织应对[灾害响应](https://www.youtube.com/watch?v=8-macH8ozr4&list=PL95lT3XlM14ROFtYnlBDYZbKipH3JLaC7&index=3)、[行星监测](https://www.youtube.com/watch?v=FviGaVEByS4&list=PL95lT3XlM14ROFtYnlBDYZbKipH3JLaC7&index=5)等挑战。

## 在最关键的时刻提供实时警报与权威信息

我们在 Search 和地图上通过 [SOS 警报](https://support.google.com/sosalerts/?hl=en#7200960)提供危机响应动态，汇集来自官方机构和可信媒体的相关信息。我们还在 90 多个国家与经授权的警报发布者和分发者合作，通过[公共警报（Public Alerts）](https://support.google.com/publicalerts/#3249690)放大紧急警报和公共预警。我们的危机信息已被浏览数十亿次；仅去年一年，Google 平均每天帮助人们获取危机信息超过 1,000 万次。

信息要有用，就必须可行动。例如，Search 中的[极端高温](https://blog.google/company-news/outreach-and-initiatives/sustainability/extreme-heat-support/)警报为 100 多个国家的人们提供预警，其中包括来自全球高温健康信息网络（Global Heat Health Information Network）的[安全提示](https://wmo.int/media/news/google-adds-health-tips-extreme-heat-warnings)。[Android 地震预警系统（Android Earthquake Alerts System）](https://research.google/blog/android-earthquake-alerts-a-global-system-for-early-warning/)能够探测地震，并在震动到达之前向 Android 用户发出警报，为他们争取转移到安全地点的时间。30 多个国家的 Google 地图提供最新的[空气质量](https://support.google.com/maps/answer/11270845?hl=en-GB)数据，帮助用户减少污染暴露。

## 为共同的全球使命提供持续支持

构建全球韧性需要协作。通过与各国政府、联合国机构、组织、科学家和一线救援人员合作，我们能够帮助世界各地的社区免受自然灾害之害。

在尼日利亚和孟加拉国，[GiveDirectly](https://www.givedirectly.org/flood-forecast-ai) 和[国际救援委员会（International Rescue Committee）](https://www.rescue.org/press-release/support-googleorg-international-rescue-committee-and-givedirectly-scale-artificial)利用我们的洪水预报开展预见性行动，在水位上涨之前发放紧急现金，让社区能够及时撤离并保全财物。飓风 Melissa 期间，美国国家飓风中心使用了我们的 WeatherNext 模型，[提前五天预测](https://deepmind.google/blog/how-weathernext-helped-the-national-hurricane-center-better-predict-hurricane-melissas-historic-landfall-in-jamaica)了飓风在牙买加登陆，使牙买加气象局得以通知公众。而在世界各地，[Google.org](http://google.org/) 正与本地组织合作，为灾后恢复工作提供资金。

过去十年，我们在推动面向气候韧性的 AI 研究突破与解决方案方面取得了进展，为世界各地的社区提供可行动的及时信息。我乐观地相信，通过善用 AI 并与合作伙伴携手，我们将更接近那个没有人会被自然灾害打个措手不及的世界。
