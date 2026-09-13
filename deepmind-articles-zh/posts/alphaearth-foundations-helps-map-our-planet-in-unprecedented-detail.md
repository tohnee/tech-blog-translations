---
title: "AlphaEarth Foundations 以前所未有的细节帮助绘制我们的星球"
title_en: "AlphaEarth Foundations helps map our planet in unprecedented detail"
source: https://deepmind.google/blog/alphaearth-foundations-helps-map-our-planet-in-unprecedented-detail/
site: deepmind
date: 2025-07-30
crawled: 2026-09-13
translated: 2026-09-13
---

# AlphaEarth Foundations 以前所未有的细节帮助绘制我们的星球

> 原文：[AlphaEarth Foundations helps map our planet in unprecedented detail](https://deepmind.google/blog/alphaearth-foundations-helps-map-our-planet-in-unprecedented-detail/) · Google DeepMind

新的 AI 模型整合数 PB 的地球观测数据，生成统一的数据表征，革新全球测绘与监测

每一天，卫星都在捕捉信息丰富的图像和测量数据，为科学家和专家提供对我们星球的近乎实时的观察。虽然这些数据影响巨大，但它们的复杂性、多模态性和更新频率也带来了新的挑战：如何连接彼此割裂的数据集并有效地利用它们。

今天，我们推出 AlphaEarth Foundations，一个像虚拟卫星一样运作的人工智能（AI）模型。它把海量的地球观测数据整合成一种计算机系统易于处理的统一数字表征，或称"[嵌入](https://developers.google.com/machine-learning/crash-course/embeddings/embedding-space?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=)"，从而精确而高效地刻画地球全部陆地和近海水域。这使该模型能够为科学家提供一幅更完整、更一致的星球演化图景，帮助他们在粮食安全、森林砍伐、城市扩张和水资源等关键问题上做出更明智的决策。

为了加速研究并解锁应用场景，我们现在发布一组 AlphaEarth Foundations 的年度嵌入，作为 [Google Earth Engine](https://earthengine.google.com/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=) 中的 [Satellite Embedding 数据集](https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_SATELLITE_EMBEDDING_V1_ANNUAL?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=#description)。过去一年里，我们与 50 多家组织合作，在它们的真实世界应用中测试这一数据集。

我们的合作伙伴已经从中获得显著收益：利用这些数据更好地对尚未制图的生态系统进行分类、理解农业与环境变化，并大幅提升测绘工作的精度与速度。在本篇博客中，我们很高兴分享它们的部分反馈，展示这项新技术的切实影响。

第 1 页，共 3 页

![一幅色彩丰富、细节极为精细的地理空间嵌入可视化，显示陆地、森林地块和一条蜿蜒河流的卫星视图。](https://lh3.googleusercontent.com/FpTb4pZP1Wok3PFolYgx7xnoSy68iHC-f1q_HuCocGMDWR5yHmpxA_1pqOGoY8TRC_VqLgXyZ3oh1GX-HtGwBY-_08X-lPkk_XTBX9LDZyiZouGuBQ=w1440)

把红、绿、蓝三种颜色分配给 AlphaEarth Foundations 嵌入场 64 个维度中的三个维度，从而将我们世界的丰富细节可视化。在厄瓜多尔，模型穿透持续的云层覆盖，清晰呈现处于不同发育阶段的农田地块。在别处，它以清晰的细节绘制了南极洲一处复杂地表——由于卫星成像不规律，这一地区历来难以成像——它还让加拿大农业用地使用中肉眼不可见的差异显现出来。

![一幅色彩丰富、细节极为精细的地理空间嵌入可视化，显示陆地、森林地块和一条蜿蜒河流的卫星视图。](https://lh3.googleusercontent.com/UKQxamKhBQF9TgbB2kSI7NQiaxGZBd_5OKXMmnG3o4tj5U7V0mPEDouqIZnyMjanPveo2vldDrP22ylWVB70T67Df1jUw4dqwJfDV844T_9BmYGPVA=w1440)

把红、绿、蓝三种颜色分配给 AlphaEarth Foundations 嵌入场 64 个维度中的三个维度，从而将我们世界的丰富细节可视化。在厄瓜多尔，模型穿透持续的云层覆盖，清晰呈现处于不同发育阶段的农田地块。在别处，它以清晰的细节绘制了南极洲一处复杂地表——由于卫星成像不规律，这一地区历来难以成像——它还让加拿大农业用地使用中肉眼不可见的差异显现出来。

![一幅色彩丰富、细节极为精细的地理空间嵌入可视化，显示陆地、森林地块和一条蜿蜒河流的卫星视图。](https://lh3.googleusercontent.com/uas-H35cQHKXFfhgklQzQd7Mxdno7KMbOiw-2yZBLTuskrCsfS_yGqmJIpETNZegXrdzNSeiHwG-xGi3Qhn6Ij4giqI7dOdeUmPmNBWFnUKCXgN3gog=w1440)

把红、绿、蓝三种颜色分配给 AlphaEarth Foundations 嵌入场 64 个维度中的三个维度，从而将我们世界的丰富细节可视化。在厄瓜多尔，模型穿透持续的云层覆盖，清晰呈现处于不同发育阶段的农田地块。在别处，它以清晰的细节绘制了南极洲一处复杂地表——由于卫星成像不规律，这一地区历来难以成像——它还让加拿大农业用地使用中肉眼不可见的差异显现出来。

## AlphaEarth Foundations 的工作原理

AlphaEarth Foundations 通过解决两大挑战——数据过载与信息不一致——为理解我们的星球提供了一个强大的新透镜。

首先，它融合了来自数十个不同公开来源的信息——光学卫星图像、雷达、3D 激光测绘、气候模拟等等。它把这些信息交织在一起，以 10x10 米的精细方格分析世界的陆地和近海水域，使其能够以惊人的精度跟踪随时间发生的变化。

其次，它让这些数据变得实用。该系统的关键创新在于能为每个方格创建高度紧凑的摘要。这些摘要所需的存储空间比我们测试的其他 AI 系统生成的摘要少 16 倍，大幅降低了行星尺度分析的成本。

这一突破让科学家得以做成一件此前不可能的事情：按需创建我们世界的详细、一致的地图。无论是监测作物健康、跟踪森林砍伐，还是观察新建筑，他们都不再需要依赖单颗过顶卫星。他们如今拥有了一种全新的地理空间数据基础。

![一张示意图，展示 AlphaEarth Foundations 如何沿时间轴处理多源地球观测，生成单幅多彩的年度地理空间嵌入，该嵌入随后对天气图表、光学卫星影像和 LiDAR 3D 高度可视化中的数据进行编码。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/gif.gif)

示意图展示 AlphaEarth Foundations 的工作方式：从视频序列中非均匀采样的帧出发，为时间中的任意位置建立索引。这帮助模型创建该位置的连续视图，同时解释众多测量数据。

为确保 AlphaEarth Foundations 能投入真实世界使用，我们对其性能进行了严格测试。与传统方法和其他 AI 测绘系统相比，AlphaEarth Foundations 始终最为准确。它擅长不同时间段内的广泛任务，包括识别土地用途和估计地表属性。至关重要的是，它在标签数据稀缺的场景下也做到了这一点。平均而言，AlphaEarth Foundations 的错误率比我们测试的模型低 24%，展现了其卓越的学习效率。更多信息请见我们的[论文](https://arxiv.org/pdf/2507.22291)。

![一张信息图，展示 AlphaEarth Foundations 的 Satellite Embedding 数据集的结构：把一个全球嵌入场映射到以层叠 3D 网格呈现的 64 个多维嵌入轴，最终映射到单个单位球面上的嵌入向量。](https://lh3.googleusercontent.com/1fL__KRDBJYACpABdB9ZEhVir8fUmDwc2HHN-_tHlzBHG8HreW1_jtnkrTJ9H95J_qlrqBouWtET3pQzhw4davAYV3qj0UlZ0smZ2kChHyjP4usE=w1440)

示意图从左到右展示一个全球嵌入场如何分解为单个嵌入。每个嵌入有 64 个分量，对应 64 维球面上的坐标。

## 用 Satellite Embedding 数据集生成自定义地图

由 AlphaEarth Foundations 驱动的 Google Earth Engine 中的 [Satellite Embedding 数据集](https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_SATELLITE_EMBEDDING_V1_ANNUAL?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=#description)是同类数据集中规模最大的之一，每年包含超过 1.4 万亿个嵌入足迹。这组年度嵌入已被世界各地的组织使用，包括联合国[粮食及农业组织](https://www.fao.org/home/en)、[Harvard Forest](https://harvardforest.fas.harvard.edu/)、[地球观测组织](https://earthobservations.org/)、[MapBiomas](https://brasil.mapbiomas.org/en/)、[俄勒冈州立大学](https://oregonstate.edu/)、[Spatial Informatics Group](https://sig-gis.com/) 和[斯坦福大学](https://www.stanford.edu/)，用以创建驱动真实世界洞见的强大自定义地图。

例如，[Global Ecosystems Atlas](http://www.globalecosystemsatlas.org/) 是一项旨在创建首个综合资源、用于绘制和监测世界生态系统的行动，它正在使用这一数据集帮助各国把尚未制图的生态系统归入[沿海灌丛](https://global-ecosystems.org/explore/groups/MT2.1)和[极端干旱沙漠](https://global-ecosystems.org/explore/groups/T5.5)等类别。这一首创性资源将在帮助各国更好地确定保护区优先次序、优化修复工作以及对抗生物多样性丧失方面发挥关键作用。

> Satellite Embedding 数据集正在革新我们的工作，帮助各国绘制未知生态系统的地图——这对于确定保护工作的着力点至关重要。

Nick Murray

詹姆斯库克大学全球生态实验室主任、Global Ecosystems Atlas 全球科学负责人

在巴西，[MapBiomas](https://brasil.mapbiomas.org/en/) 正在测试这一数据集，以更深入地理解全国的农业与环境变化。这类地图为亚马逊雨林等关键生态系统中的保护策略和可持续发展举措提供依据。

正如 MapBiomas 创始人 Tasso Azevedo 所说："Satellite Embedding 数据集可以改变我们团队的工作方式——我们现在有了新的选择，可以制作更准确、更精细、产出更快的地图——这是我们以前根本做不到的。"

更多关于 Satellite Embedding 数据集的信息和教程，请见 [Google Earth Engine 博客](https://medium.com/google-earth/ai-powered-pixels-introducing-googles-satellite-embedding-dataset-31744c1f4650)。

## 用 AI 赋能他人

AlphaEarth Foundations 代表着理解我们这个不断变化的星球的状态与动态的重大一步。我们目前正在使用 AlphaEarth Foundations 生成年度嵌入，并相信当它们与 Gemini 等具备通用推理能力的大语言模型智能体结合使用时，未来还能发挥更大的作用。我们将继续探索应用该模型基于时间的能力的最佳方式，作为 [Google Earth AI](http://blog.google/technology/ai/google-earth-ai?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=) 的一部分——这是我们的地理空间模型与数据集合集，用于帮助应对地球上最紧迫的需求。

**进一步了解 AlphaEarth Foundations**

[阅读我们的论文](https://arxiv.org/pdf/2507.22291)[使用我们的 Satellite Embedding 数据集](https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_SATELLITE_EMBEDDING_V1_ANNUAL?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=)[在 Google Earth Engine 博客上了解更多](https://medium.com/google-earth/ai-powered-pixels-introducing-googles-satellite-embedding-dataset-31744c1f4650)

**致谢**

本工作是 Google DeepMind 与 Google Earth Engine 团队之间的合作。

Christopher Brown, Michal Kazmierski, Valerie Pasquarella, William Rucklidge, Masha Samsikova, Olivia Wiles, Chenhui Zhang, Estefania Lahera, Evan Shelhamer, Simon Ilyushchenko, Noel Gorelick, Lihui Lydia Zhang, Sophia Alj, Emily Schechter, Sean Askay, Oliver Guinan, Rebecca Moore, Alexis Boukouvalas, Pushmeet Kohli
