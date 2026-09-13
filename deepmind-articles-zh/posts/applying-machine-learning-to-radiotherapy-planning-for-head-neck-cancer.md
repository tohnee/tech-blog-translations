---
title: "把机器学习应用于头颈癌的放疗规划"
title_en: "Applying machine learning to radiotherapy planning for head & neck cancer"
source: https://deepmind.google/blog/applying-machine-learning-to-radiotherapy-planning-for-head-neck-cancer/
site: deepmind
date: 2016-08-30
crawled: 2026-09-13
translated: 2026-09-13
---

# 把机器学习应用于头颈癌的放疗规划

> 原文：[Applying machine learning to radiotherapy planning for head & neck cancer](https://deepmind.google/blog/applying-machine-learning-to-radiotherapy-planning-for-head-neck-cancer/) · Google DeepMind

我们很高兴地宣布与伦敦大学学院医院 NHS 基金会信托（University College London Hospitals NHS Foundation Trust）放疗科达成一项新的研究合作，该科室提供世界领先的癌症治疗。

每 75 名男性和每 150 名女性中，就有 1 人会在一生中被诊断出患有口腔癌；自 20 世纪 70 年代以来，口腔癌发病率上升了 92%。仅在英国，头颈癌每年就影响超过 11,000 名患者。

放疗等治疗手段的进步提高了生存率，但由于这一身体部位集中了大量脆弱的结构，临床医生必须极其细致地规划治疗，确保重要神经或器官不受损伤。

例如，口腔后部或鼻窦处的癌症因此特别难以用放疗治疗。

于是，我们与 UCLH 世界领先的放疗团队的临床医生一道，正在探索机器学习方法能否缩短为这类癌症规划放疗所需的时间。在实施放疗之前，临床医生必须绘制出身体中待治疗区域与需避开区域的详细地图。

这一过程称为分割（segmentation），包括围绕解剖结构的不同部分进行勾画，并把信息传送给放疗设备，后者便可在照射癌症的同时不伤及健康组织。

但当肿瘤与重要的解剖结构距离如此之近——例如在头颈部——临床医生勾画的轮廓就必须精细入微。

对于这类癌症，分割可能耗时约四个小时。尽管 UCLH 专门头颈癌中心的专家团队在这一流程上处于全国领先地位，仍有创新的空间。我们认为机器学习可以发挥作用。

在这次合作中，我们将仔细分析来自 UCLH 多达七百名既往患者的匿名扫描影像，以确定机器学习让放疗规划更高效的潜力。

放疗治疗方案的决策权仍将握在临床医生手中，但我们希望分割流程能够从最多四个小时缩短到一小时左右。

我们希望随着时间推移，这项研究能够带来两项尤为重要的收益：

1. 把临床医生的时间解放出来，让他们更专注于患者护理、教学与研究
2. 开发出一种有望应用于身体其他部位的放疗分割算法

与我们与 NHS 的所有合作一样，我们将以最大的审慎和尊重来对待本项目中使用的患者数据。所有扫描影像在共享给 DeepMind 之前，都会按照 UCLH 信息治理政策进行匿名化处理。你可以[在此](https://deepmind.com/about/health)进一步了解我们自身的信息治理方法。

这类研究仍处于探索阶段，但我们认为它具有帮助临床医生与患者的巨大潜力。

![一张患者头颈部的轴位 CT 扫描图像，显示脊柱、气道及周围组织等精细解剖结构，用于放疗规划。](https://lh3.googleusercontent.com/Koc4qA9xMnSQsZBJPIMIn6i_kX4zRP2Ro92a7P5g64GYXTHwElbWYuM957Y2BkcIxFQYBwnGBijEikZetjEdYmCvIyYjYCEHpfWMEzH_ckbILNXW=w1440)

一例头颈癌患者计算机断层扫描（CT）序列中的示例图像。此图仅作演示之用，并非在与 UCLH 合作中共享给 DeepMind 的扫描影像之一。

**说明**

本图像依据[知识共享署名 3.0 未移植许可协议](http://creativecommons.org/licenses/by/3.0/)的条款，未经修改地转载自 [The Cancer Image Archive](https://wiki.cancerimagingarchive.net/display/Public/TCGA-HNSC)。

Zuley ML, Jarosz R, Kirk S, et al. 2016. Radiology Data from The Cancer Genome Atlas Head-Neck Squamous Cell Carcinoma [TCGA-HNSC] collection. [The Cancer Imaging Archive](https://wiki.cancerimagingarchive.net/display/Public/TCGA-HNSC).
Clark K, Vendt B, Smith K, et al. 2013. The Cancer Imaging Archive (TCIA): Maintaining and Operating a Public Information Repository. Journal of Digital Imaging, 26:6:1045-1057
