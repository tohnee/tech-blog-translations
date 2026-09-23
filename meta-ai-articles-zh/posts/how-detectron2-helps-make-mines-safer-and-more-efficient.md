---
title: "Detectron2 如何帮助矿山更安全、更高效"
title_en: "How Detectron2 helps make mines safer and more efficient"
date: 2020-06-09
source: https://ai.facebook.com/blog/how-detectron2-helps-make-mines-safer-and-more-efficient
crawled: 2026-09-22
translated: 2026-09-22
---

# Detectron2 如何帮助矿山更安全、更高效

> 原文：[How Detectron2 helps make mines safer and more efficient](https://ai.facebook.com/blog/how-detectron2-helps-make-mines-safer-and-more-efficient) · Meta AI（Wayback 存档）

2020 年 6 月 9 日

视具体配置而定，采矿现场每天可产出 100 到 1000 米（接近九个足球场长度）的钻孔岩芯，每周产生数百张参考图像。所有这些样品都必须由地质学家仔细分析——不仅为了评估岩石质量，也为了发现断层和裂隙等潜在隐患的迹象——这两者对矿山的设计与工程以及效率和生产率都至关重要。这是一个劳动密集型的手工流程，亟需机器学习（ML）方案。

澳大利亚科技服务公司 DiUS 与 Solve Geosolutions 合作开发了这一 ML 方案。面向采矿行业的 SaaS 解决方案 Datarock 利用多种 PyTorch 工具（包括基于 PyTorch 的目标检测库 Detectron2），用地质图像训练 ML 模型。Detectron2 旨在支持图像分类和目标检测领域广泛的图像分析模型，还提供模块化设计以及对全景分割（panoptic segmentation）的支持，这使它能够执行前沿研究以及新颖商业与企业应用中的精密目标识别任务。

Datarock 让采矿作业得以使用 ML 和计算机视觉分析矿床地质，并利用钻探现场产出的海量图像，把它们变成数据集——处理原始图像并分割其中的重要地质信息——从而简化这一艰辛的流程。借助 Detectron2，Datarock 的开发者得以创建能够进行岩石质量指标（用于理解岩石强度的度量）、岩石裂隙预测等高价值但难以采集的地质分析的模型。据 DiUS 介绍，Datarock 平台已处理了相当于 100 多万米的钻孔岩芯图像。

DiUS 和 Solve Geosolutions 表示，Detectron2 的特殊优势在于其训练速度最高可达此前开发模型的四倍。我们计划继续改进和升级 Detectron2，增强其灵活性并实现新模型，以支持像 Datarock 这样的新颖用例。

进一步了解支持这项工作的 PyTorch 工具。
