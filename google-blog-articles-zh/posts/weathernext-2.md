---
title: "WeatherNext 2：我们最先进的天气预报模型"
title_en: "WeatherNext 2: Our most advanced weather forecasting model"
source: https://blog.google/innovation-and-ai/models-and-research/google-deepmind/weathernext-2/
site: google-blog
date: 2025-11-17
crawled: 2026-09-13
translated: 2026-09-13
---

# WeatherNext 2：我们最先进的天气预报模型

> 原文：[WeatherNext 2: Our most advanced weather forecasting model](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/weathernext-2/) · Google

天气影响着我们每天做出的重要决策——从全球供应链、航班航线，到你每天的通勤。近年来，人工智能（AI）极大拓展了天气预报的可能性，以及我们使用天气信息的方式。

今天，Google DeepMind 与 Google Research 发布 [WeatherNext 2](https://deepmind.google/science/weathernext/)，我们最先进、最高效的预报模型。WeatherNext 2 的预报生成速度提升 8 倍，分辨率最高可达 1 小时级。这一突破得益于一种能够提供数百种可能情景的新模型。借助这项技术，我们已通过[实验性气旋预测](https://deepmind.google/blog/how-were-supporting-better-tropical-cyclone-prediction-with-ai/)，支持气象机构基于一系列情景做出决策。

我们现在正把研究成果带出实验室，交到用户手中。WeatherNext 2 的预报数据现已在 [Earth Engine](https://developers.google.com/earth-engine/datasets/catalog/projects_gcp-public-data-weathernext_assets_weathernext_2_0_0) 和 [BigQuery](https://console.cloud.google.com/bigquery/analytics-hub/exchanges/projects/871883017250/locations/us/dataExchanges/weathernext_19397e1bcb7/listings/weathernext_2_19a39fe59dd) 中可用。我们还在 Google Cloud 的 Vertex AI 平台上推出[抢先体验计划](https://console.cloud.google.com/vertex-ai/publishers/google/model-garden/weather-next-v2)，支持自定义模型推理。

通过引入 WeatherNext 技术，我们已升级了 Search、Gemini、Pixel Weather 和 Google Maps Platform 的 [Weather API](https://mapsplatform.google.com/maps-products/weather/) 中的天气预报。未来几周内，它还将为 Google Maps 中的天气信息提供支持。

## 预测更多可能的情景

从单一输入出发，我们使用独立训练的神经网络，并在函数空间中注入噪声，从而在天气预报预测中创造连贯的变异性。

![展示 WeatherNext 2 所用新算法的示意图。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/WeatherNext_2-blog-figure-03_lar.width-1200.format-webp.webp)

天气预测需要覆盖完整的可能性区间——包括最需要为之做准备的极端糟糕情景。

WeatherNext 2 能够从同一个起点预测数百种可能的天气结果。每一次预测在单个 TPU 上耗时不到一分钟；而使用基于物理的模型，超级计算机则需要数小时。

我们的模型同样技艺高超，并能够做出更高分辨率的预测，精细到小时级。总体而言，WeatherNext 2 在 99.9% 的变量（如温度、风速、湿度）和预报时效（0-15 天）上超越了我们此前最先进的 WeatherNext 模型，带来更实用、更准确的预报。

这一性能提升得益于一种名为[函数生成网络](https://arxiv.org/abs/2506.10772)（Functional Generative Network，FGN）的全新 AI 建模方法，它把「噪声」直接注入模型架构，使其生成的预报在物理上保持真实且相互关联。

这种方法对于预测气象学家所说的「边际量（marginals）」与「联合量（joints）」尤为有用。边际量是彼此独立的单一天气要素：某个具体地点的精确温度、某一海拔高度的风速，或湿度。我们方法的创新之处在于，模型只在这些边际量上训练；然而凭借这种训练，它学会了熟练预报「联合量」——那些庞大、复杂、相互关联，取决于所有个体要素如何组合在一起的系统。这类「联合」预报是我们最有价值的预测所必需的，例如识别受高温影响的整个区域，或估算一座风电场的预期发电量。

连续分级概率评分（CRPS）：WeatherNext 2 与 WeatherNext Gen 的对比

![热力图显示，在几乎所有大气变量、气压层和预报时效上，WeatherNext 2 都持续优于 WeatherNext Gen。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/WeatherNext2vs_graphic.width-1200.format-webp.webp)

## 从研究走向现实

借助 WeatherNext 2，我们正把前沿研究转化为高影响力的应用。我们致力于推进这项技术的最前沿，并把最新工具提供给全球社区。

展望未来，我们正在积极研究以改进模型的能力，包括整合新的数据源，并进一步扩大访问范围。通过提供强大的工具与开放的数据，我们希望加速科学发现，赋能由研究人员、开发者和企业组成的全球生态，让他们能够就当今最复杂的问题做出决策，并为未来而构建。

要进一步了解 Google 在地理空间平台与 AI 方面的工作，请查看 [Google Earth](http://earth.google.com/)、[Earth Engine](https://earthengine.google.com/)、[AlphaEarth Foundations](https://deepmind.google/blog/alphaearth-foundations-helps-map-our-planet-in-unprecedented-detail/) 和 [Earth AI](https://ai.google/earth-ai/)。

## 进一步了解 WeatherNext 2

- [阅读我们的论文](https://arxiv.org/abs/2506.10772)
- [WeatherNext 开发者文档](https://developers.google.com/weathernext)
- 探索 [Earth Engine 数据目录](https://developers.google.com/earth-engine/datasets/catalog/projects_gcp-public-data-weathernext_assets_weathernext_2_0_0)
- 在 [BigQuery](https://console.cloud.google.com/bigquery/analytics-hub/exchanges/projects/871883017250/locations/us/dataExchanges/weathernext_19397e1bcb7/listings/weathernext_2_19a39fe59dd) 中查询预报数据
- 注册 Cloud Vertex AI 的[抢先体验计划](https://console.cloud.google.com/vertex-ai/publishers/google/model-garden/weather-next-v2)
