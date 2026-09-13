---
title: "全新深度学习模型从太空绘制全球甲烷排放地图"
title_en: "A new deep learning model maps global methane emissions from space."
source: https://blog.google/innovation-and-ai/models-and-research/google-research/mapping-global-methane-emissions-from-space/
site: google-blog
date: 2026-09-09
crawled: 2026-09-13
translated: 2026-09-13
---

# 全新深度学习模型从太空绘制全球甲烷排放地图

> 原文：[A new deep learning model maps global methane emissions from space.](https://blog.google/innovation-and-ai/models-and-research/google-research/mapping-global-methane-emissions-from-space/) · Google

在发表于 [PNAS](https://www.pnas.org/doi/10.1073/pnas.2612145123) 的一项新研究中，Google 与 NASA 喷气推进实验室（JPL）推出了 MAPL-EMIT——一款利用 NASA 的 [EMIT](https://www.jpl.nasa.gov/missions/emit-earth-surface-mineral-dust-source-investigation/) 仪器从太空追踪全球甲烷排放的 AI 模型。

甲烷是一种强效温室气体。在 100 年的时间尺度上，其增温潜势是二氧化碳的 30 倍。MAPL-EMIT 解决了甲烷探测中的一个关键瓶颈。该模型在 360 万个物理模拟甲烷羽流（排放到大气中的甲烷气体云）上训练而成，能够穿透复杂且充满噪声的地形，探测到的羽流数量比人类专家多出 50%，并在全球多识别出超过 23,000 个羽流，其中包括全球 25 个最大排放垃圾填埋场中的 24 个。通过让甲烷排放源更容易被大规模发现，MAPL-EMIT 使更快速、更有针对性的气候减缓行动成为可能。

Google 已在 [Earth Engine](https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_ghg_emit_mapl_emit_plumes_v1_0) 上发布了全球羽流数据库，并配套推出一款 [Earth Engine 应用](https://nature-trace.projects.earthengine.app/view/mapl-emit)以可视化这些数据。开源模型可在 [Kaggle](https://www.kaggle.com/models/vishalbatchu/emit-methane-plume-detection-and-quantification/) 上获取，推理工具则发布在 [GitHub](https://github.com/google-research/mapl) 上，以支持研究人员、政策制定者和运营方。更多内容请阅读 [Google Research 博客](https://research.google/blog/mapping-global-methane-emissions-from-space-with-deep-learning/)。

![一幅由六幅卫星图组成的图表，展示了在美国加利福尼亚州、土库曼斯坦、印度德里、巴西圣保罗、波兰卡托维兹和中国山西探测到的甲烷羽流及排放热力图。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Map_Global_Methane_social.width-1200.format-webp.webp)
