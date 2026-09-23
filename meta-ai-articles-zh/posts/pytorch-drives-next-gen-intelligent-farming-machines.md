---
title: "PyTorch 驱动下一代智能农业机械"
title_en: "PyTorch drives next-gen intelligent farming machines"
date: 2020-08-06
source: https://ai.facebook.com/blog/pytorch-drives-next-gen-intelligent-farming-machines
crawled: 2026-09-22
translated: 2026-09-22
---

# PyTorch 驱动下一代智能农业机械

> 原文：[PyTorch drives next-gen intelligent farming machines](https://ai.facebook.com/blog/pytorch-drives-next-gen-intelligent-farming-machines) · Meta AI（Wayback 存档）

2020 年 8 月 6 日

PyTorch 正助力驱动新一代 AI 增强的农业机械。对农民而言，杂草对作物健康构成非常现实的威胁——与此同时，全球人口增长正在推高粮食需求，也使土地和水资源等日益稀缺。为了帮助农民用更少资源生产更多粮食，总部位于加州、约翰迪尔（John Deere）旗下的 Blue River Technology 求助于人工智能和机器人技术。该公司的 See & Spray 机器人农机将机器学习（ML）与计算机视觉相结合，实时识别作物中的杂草并在除草时不伤作物——为农民提供一种更稳定、更精准、更高效的除草方式。

当 See & Spray 机器在田间行进时，它通过高分辨率摄像头阵列采集作物和杂草的图像。摄像头捕获的每一帧都由启用 PyTorch 的神经网络分析，以识别杂草和作物并绘制它们的位置图。地图一旦生成，机器人便在几毫秒内只对发现杂草的位置喷洒。这种方式减少了除草剂用量，既为农民节省成本，也促进可持续农业实践。

「这是一个颇具挑战性的问题，因为许多杂草看起来和作物一模一样。」Blue River Technology 计算机视觉与机器学习总监 Chris Padwick 在一篇 PyTorch Medium 文章中写道。为解决这一问题，Padwick 说 Blue River Technology 团队咨询了专业农学家和杂草科学家，以正确标注杂草，并使用 PyTorch 训练他们所有的机器学习模型。「我们选择 PyTorch 是因为它非常灵活且易于调试。新团队成员能快速上手，文档也很全面。」Padwick 写道，「这个框架让我们能够同时支持生产模型工作流和研究工作流。」

See & Spray 能区分作物（绿色）与杂草（红色）。

持续改进其 AI 驱动的农业流程，不仅仅是把神经网络模型部署到机器人上那么简单。Blue River Technology 的工程师还需要定期开展实验和研究来提升模型性能，这一过程还涉及大量与测试和流程改进相关的数据科学与分析。为了监控和评估这些机器学习运行，工程师使用 Weights & Biases 平台，它也让 PyTorch 模型在训练期间的可视化变得容易。Padwick 写道，PyTorch 的优势在于速度和灵活性，让工程师能非常快速地添加新功能。「我们在 PyTorch 之上构建了一组内部库，让我们能够执行可重复的机器学习实验。」他写道，「归根结底，我们要为田间机械打造最准确、最快速的模型。PyTorch 让我们得以快速迭代，然后将模型生产化并部署到田间。」

了解更多 Blue River 如何使用 PyTorch 构建智能农业机械。
