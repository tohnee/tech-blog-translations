---
title: "用 DINO 降低英国政府开支并提升绿地可达性"
title_en: "Reducing Government Costs and Increasing Access to Greenspaces in the United Kingdom with DINO"
date: 2026-02-09
source: https://ai.meta.com/blog/forest-research-dino
crawled: 2026-09-22
translated: 2026-09-22
---

# 用 DINO 降低英国政府开支并提升绿地可达性

> 原文：[Reducing Government Costs and Increasing Access to Greenspaces in the United Kingdom with DINO](https://ai.meta.com/blog/forest-research-dino) · Meta AI（Wayback 存档）

2026 年 2 月 9 日 · 阅读时长约 6 分钟

英格兰的公园和绿地每年在健康、气候变化和环境方面带来的收益估计达 66 亿英镑（约合 84 亿美元）。目前，英格兰 80% 的人口居住在城镇，但仍有三分之一的英格兰民众无法获得高质量绿地。2023 年，英国政府发布了一项雄心勃勃的《环境改善计划》（Environmental Improvement Plan），提出每个英格兰居民住处距绿地的步行时间不应超过 15 分钟，并且从家中能看到至少三棵树。此外，政府还承诺通过植树和造林，到 2050 年将英格兰的树冠覆盖率提高 2%。鉴于这项国家《环境改善计划》为英国居民描绘了令人期待的未来，对树冠覆盖进行频繁而精确的监测——并细化到单株树木层面、贯穿长期时间尺度——至关重要。

2025 年 4 月，林业委员会（Forestry Commission）旗下研究机构、负责监测英国树木、林地和森林的 Forest Research 发布了全新的「林地外树木」（Trees Outside Woodlands，ToW）地图。该项目由英国政府的自然资本与生态系统评估（Natural Capital and Ecosystem Assessment，NCEA）计划资助，该计划正在对英格兰的陆地、淡水和海岸生态系统进行评估，以便在 2029 年前建立一份英国自然资产基线。这一工具绘制了英格兰林地外树木的分布，并且首次将数据免费开放。Forest Research 目前正在使用 DINOv2 构建一个模型，以提升其地图的精度。这一改进对 NCEA 计划同样不可或缺，它能强化基线评估，并为环境、食品与农村事务部（Defra）的政策决策提供可靠证据。

此前，Forest Research 结合实地调查与 LiDAR 数据——一种通过激光和卫星成像获取的地理空间信息——来评估全国的树冠分布。然而，持续采购这类数据源的成本极其高昂，使精确的森林监测成为一个长期难题。对孤立的树木、成组树木以及面积小于 0.5 公顷的林地而言，监测尤其困难；而英格兰大约 30% 的树冠属于这些林地类型，因此 DINOv2 在制图与监测工作中发挥了极大价值。

Meta 与世界资源研究所（World Resources Institute，WRI）合作，用 1800 万张卫星图像训练其开源计算机视觉模型 DINOv2，制作出分辨率达 1 米的全球树冠高度开源地图，使在全球尺度上检测单株树木成为可能。自 2024 年 4 月发布该地图以来，全球许多国家的政府都表现出浓厚兴趣，希望利用这一模型和地图改进本国的再造林工作。

Forest Research 遥感负责人 Freddie Hunter 表示：「基于 DINOv2 的高分辨率树冠高度模型是近年来发布的最强大的开源 AI 模型，对全国尺度的单株树木检测与监测而言是一次格局性改变。」

Hunter 和团队目前正致力于将树冠高度图（Canopy Height Maps）应用于国家航空影像，希望在全国尺度上为孤立树木、成组树木和小型林地提供更新的树冠覆盖与高度估算，并估算树木被砍伐带来的木材蓄积量损失。将该模型应用于航空影像，可能得到一个在单株树木识别方面质量始终更高（至少不逊色）的合成树冠高度模型（Canopy Height Model，CHM），有望超过环境署（Environment Agency）的全国 LIDAR 调查。这将使 Forest Research 能够以三年为周期滚动估算树木密度和树冠面积。

Forest Research 还希望利用树冠高度图中的结构信息，通过为模型开发特征并在城镇等复杂环境中估算树冠，来加强全国尺度的树种分布制图工作。使用 Meta 与 WRI 的开源模型，可能使 Forest Research 无需再自行创建和训练预测树冠高度的模型，从而降低其对 LiDAR 和调查数据的依赖，以便监测国家绿地目标的进展。此外，利用树冠模型勾绘树冠轮廓并估算树木密度，还可能在数据采购上节省大量成本、提高数据更新频率并提升数据质量。最终，这将有助于改进对政府树冠覆盖目标的监测，并可能直接影响环境政策。

在 DINOv2 取得成功的基础上，Meta 最近推出了 DINOv3，以助力提升视觉智能。我们希望通过进一步提升树冠高度图的精度，世界各国政府都可以选择利用包括 DINOv3 在内的开源模型，帮助监测其再造林投入。

想了解更多合作伙伴如何将 Meta 的 AI 用于社会影响类应用？请访问我们的 AI For Good（AI 向善）网站。
