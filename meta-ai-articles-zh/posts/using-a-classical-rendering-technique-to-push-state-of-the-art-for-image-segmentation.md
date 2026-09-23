---
title: "用经典渲染技术推动图像分割达到业界最优"
title_en: "Using a classical rendering technique for state of the art image segmentation"
date: 2020-06-12
source: https://ai.facebook.com/blog/using-a-classical-rendering-technique-to-push-state-of-the-art-for-image-segmentation
crawled: 2026-09-22
translated: 2026-09-22
---

# 用经典渲染技术推动图像分割达到业界最优

> 原文：[Using a classical rendering technique for state of the art image segmentation](https://ai.facebook.com/blog/using-a-classical-rendering-technique-to-push-state-of-the-art-for-image-segmentation) · Meta AI（Wayback 存档）

2020 年 6 月 12 日

**研究内容：** 一种名为 PointRend 的新型高效高分辨率图像分割方法，其灵感来自计算机图形学渲染中使用的经典自适应采样技术。与以往最先进的方法相比，它对物体和场景的分割更锐利、更准确。

现代图像分割方法基于卷积神经网络，将计算均匀分布到整幅输入图像上。通常，这些方法会在比输入图像更粗糙的分辨率上做预测，以限制计算复杂度。这类技术把大部分计算预算（过度采样）花在图像中不模糊的区域，比如狗的躯干或背景，却对物体更具挑战性的部分采样不足，漏掉了狗爪这类细粒度细节，或更普遍的物体边缘。

使用标准 Mask R-CNN 分割头（左）与 PointRend 分割头（右）得到的实例分割结果。从视觉效果上看，PointRend 在以往方法被过度平滑的区域输出清晰锐利的物体边界。

PointRend 模块在自适应选定的位置执行基于点的分割预测，其灵感来自计算机图形学渲染中使用的经典自适应细分（adaptive subdivision）技术。因此，我们的模型能够高效地生成明显更细致的分割，达到以往最佳分割方法（如 Mask R-CNN 或 Semantic FPN）无法企及的像素级精度。从定量上看，PointRend 在实例分割和语义分割两项任务的两大主要基准测试上都带来了显著提升。加上 PointRend 分割头增强的 Mask R-CNN 所生成的掩码比标准 Mask R-CNN 模型输出细致 8 倍，平均精度最高提升 2.8 个百分点。代码已在此处开源。

**工作原理：** PointRend 方法建立在 Mask R-CNN、Semantic FPN 和 Deeplab 等现有图像分割方法之上，这些方法能高效地产生粗粒度预测。PointRend 从粗粒度的全局预测出发，逐步放大并细化预测，只需几步即可达到输入图像的分辨率。在每一步中，PointRend 会在放大后的预测上选出一组需要细化的位置。对于其中每个位置，新模型都会利用底层卷积神经网络中间表示中的特征独立更新其预测。你可以在上面的动画中看到该过程的示例。

总体而言，这项技术让研究者只需对输入图像中一小部分像素真正做出预测，就能获得高分辨率分割。PointRend 避免在粗粒度预测即可完美覆盖的区域上消耗过多计算，同时针对物体或场景中困难区域的像素细化预测。这种自适应性带来了高效的推理，可以根据手头的计算资源进行调整，而且无需重新训练模型。

**为什么重要：** 与现有方法相比，PointRend 的效率使原本在内存或计算上不切实际的输出分辨率成为可能。随着内存和算力约束的降低，我们将能够把图像分割模型部署到更小的设备和低资源环境中。像素级完美的分割还能增强各种此前受到限制的 AR/VR 体验，比如无缝变换背景，或在场景中插入更精确、更逼真的物体。

阅读完整论文 | 获取代码

这项工作将在 CVPR 2020 上展示。在此处了解 Facebook AI 在 CVPR 的全部详情。
