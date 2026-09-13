---
title: "WeatherNext 3 发布：我们最先进、最精准的全球天气 AI 模型"
title_en: "Introducing WeatherNext 3, our most advanced and accurate global weather AI model"
source: https://blog.google/innovation-and-ai/models-and-research/google-deepmind/introducing-weathernext-3/
site: google-blog
date: 2026-09-03
crawled: 2026-09-13
translated: 2026-09-13
---

# WeatherNext 3 发布：我们最先进、最精准的全球天气 AI 模型

> 原文：[Introducing WeatherNext 3, our most advanced and accurate global weather AI model](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/introducing-weathernext-3/) · Google

每一天，天气都在影响数十亿个决定。有些简单到出门前带把伞，另一些则重要得多。风、雨以及热浪和干旱等极端天气事件，会在农业、全球供应链、清洁能源生产和国民经济中产生连锁影响。

近年来，AI 彻底改变了天气预报，利用历史记录做出比传统方法更快、更准确的预测。然而，预测高度局部且快速变化的天气仍是一大挑战。以往的模型往往缺乏足够的空间分辨率，也难以纳入卫星等来源的实时天气数据。

今天，Google DeepMind 和 Google Research 推出 [WeatherNext 3](https://arxiv.org/abs/2609.03582)——据 Brightband 的独立[实时评测](https://owb.brightband.com/)，这是迄今最先进、最精准的全球天气模型。我们的模型直接从实时观测中学习，能够针对对人们影响最大的天气事件提供及时、更局部化的预测。通过利用原始卫星数据每小时生成一次高分辨率预报，我们的模型让可靠的预报通过全球各地的 Google 产品触手可及。

## 前所未有分辨率下的快速天气预测

预报的价值往往取决于细节，以及它在时间和空间上的精细程度。WeatherNext 3 以多种空间分辨率生成逐小时预报，从大范围的全球风场形态一直到局地地形，都保持物理一致性。

借助 WeatherNext 3，我们可以以 5 公里分辨率可视化温度和湿度等关键地表变量，其他地表变量为 10 公里，风速等大气变量为 25 公里。总体而言，这提供了比上一代模型 WeatherNext 2（以 25 公里网格、6 小时间隔生成预报）清晰约五倍的全球天气图景。

图 1：WeatherNext 3 端到端系统架构。模型将实时 1 小时地球静止卫星拼图与传统历史分析一同输入一个单一而灵活的 Functional Generative Network（FGN）网格 transformer，原生输出密集网格场、离散气旋路径，并直接预测站点级稀疏坐标。

![WeatherNext 3 系统架构示意图](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/WeatherNext3_diagrams_fig-01.width-1200.format-webp.webp)

图 2：英国上空 2 米温度预报对比。WeatherNext 2（左）为 25 公里（0.25°）分辨率，WeatherNext 3（右）为原生 5 公里（0.05°）分辨率。WeatherNext 3 能分辨复杂的局地地形，避免了旧模型中像素化、过度平滑的温度表现。

## 持续全球尺度的真实世界数据

WeatherNext 3 最大的飞跃在于它的学习来源。大多数 AI 天气模型（包括 WeatherNext 2）都是在数值天气预报（NWP）模型的数据上训练的。NWP 模型虽然有用，但它们是由超级计算机驱动的复杂物理模拟，带有 6 小时的数据滞后。这种滞后会给降雨或地表温度等快速变化的变量带来偏差。

通过摄入实时全球地球静止卫星数据拼图，我们的新模型获得了丰富且持续更新的大气视图。这使模型能够每小时生成一次新预报，每一次都以可获得的最新卫星观测为依据，分辨率最高可达 5 公里。

这一点很重要，因为关键天气发展得很快。当风暴、锋面或降水系统骤然成形时，我们快速更新的周期和更高的分辨率能够提供更早、更细致的洞见，帮助推动有效应对。

温度和湿度等一些变量在短短几公里内就可能剧烈波动，这对靠近海岸线、山谷或山脉的社区尤为相关。传统模型在这里力不从心，因为它们训练所用的对大气的刻画缺乏细节，会遗漏极端的局地变化。

为解决这一问题，WeatherNext 3 改为直接在稀疏的气象站观测数据上训练。这使我们能够制作考虑地形等区域细节的 5 公里网格全球预报。

这一突破对拉丁美洲、非洲和亚太地区的各个区域尤为重要——由于传统区域模型的巨额超级计算成本，这些地区长期以来难以获得高分辨率预报。它为这些地区的数十亿人和本地企业带来本地化、高保真度的预报。

除了更高的分辨率和预报频率，我们的模型还引入了专门为可再生能源生产设计的预测。模型预报 100 米高度风速（大致相当于风机轮毂高度）以精确估算风电出力，同时提供高分辨率的云量和太阳辐射水平，帮助太阳能电站估计地面实际接收到的光照。

这些数据对全球清洁能源规划至关重要，让电网运营商和可再生能源开发商能够准确预测其清洁能源资产的发电量，并将其与用户需求相匹配。

## 突破性精度的降水预报

全球天气模型在准确预测降水方面出了名地困难。雨雪系统由极小尺度上快速移动的云过程驱动，很难用传统的物理模拟准确建模。因此，AI 预报往往产生模糊的估计，或完全漏掉强风暴的边界。

为解决这个问题，我们在两个极其高质量的降水数据来源上训练模型：NASA 基于卫星的 GPM 综合多卫星反演数据（IMERG），以及我们自己的基于卫星雷达的全球降水再分析数据。

结果是降水预报精度的显著跃升。在中期全球预报中，与基线的对比评估显示：在较短预报时效上，相对 IMERG 的连续分级概率评分（CRPS）最多提升 60%，相对 MRMS 提升 30%，相对雨量计观测提升 10%。

图 3：中期降水概率（PoP > 1mm）预报对比。WeatherNext 2（左）在 25 公里分辨率下降水足迹高度弥散且像素化。WeatherNext 3（中）在 11 公里分辨率下与实际卫星地面真值（右）高度吻合，准确捕捉到天气系统清晰的对流带。

![WeatherNext 2 与 WeatherNext 3 预测对比](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/WeatherNext3_diagrams_fig-03.width-1200.format-webp.webp)

## 研究成果应用于整个生态系统

我们的首要目标是推进天气智能，使其普遍有用——无论是追踪风向突变的应急救援人员、规划航线的空中交通管制员，还是管理作物的农民。

为把这些突破带出实验室、走向真实世界，我们正在将 WeatherNext 3 集成到 Google 的核心生态系统乃至更广泛的范围：

- **高分辨率预报数据：**我们提供每小时更新的全球天气预测，无需任何模型设置即可集成到你的工作流中。这让研究者、开发者和企业能够在 BigQuery 和 Earth Engine 中[查询数据](https://developers.google.com/weathernext)，或从 Google Cloud Storage 批量下载。
- **全球可用：**从今天开始，WeatherNext 3 将为 Google Search、Gemini 应用、Google 地图、Google Maps Platform Weather API 和 Google Earth Engine 中的天气体验提供支持。此次更新显著改善了更长期的预报。在提前一天或更久做计划时，人们将看到准确度最多提升 50% 的降水预报——提升最大的正是历史上预报可靠性较低的地区。因此，无论你是在为周末出行打包行李，还是在为户外活动挑选最佳日子，现在都能获得更准确的预测来帮助你规划。

大气永远会保有一定程度的不可预测性。但通过在真实世界观测上训练并绕过传统建模的限制，WeatherNext 3 让我们更接近这样一个未来：预报真正与地面实际情况相吻合。

想进一步了解 Google 的地理空间平台与 AI 工作，请查看 [Google Earth Engine](https://earthengine.google.com/)、[AlphaEarth Foundations](https://deepmind.google/blog/alphaearth-foundations-helps-map-our-planet-in-unprecedented-detail/) 和 [Earth AI](https://ai.google/earth-ai/)。

**免责声明：官方天气预报、恶劣天气预警和公共安全公告，请以你所在地的气象机构或国家气象部门为准。**

## 进一步了解 WeatherNext 3

- [阅读我们的论文](https://arxiv.org/abs/2609.03582)
- [用 WeatherNext 3 进行构建](https://developers.google.com/weathernext)
- 探索 [Weather Lab](https://deepmind.google.com/science/weatherlab)，实时查看 WeatherNext 3 的可视化
- 查看 WeatherNext 3 在 Brightband 独立[实时排行榜](http://owb.brightband.com/)上的排名。
