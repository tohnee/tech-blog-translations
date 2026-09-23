---
title: "用集成式机器学习实现低延迟移动 VR 图形"
title_en: "Using integrated ML to deliver low-latency mobile VR graphics"
date: 2019-03-15
source: https://ai.facebook.com/blog/using-integrated-ml-to-deliver-low-latency-mobile-vr-graphics
crawled: 2026-09-22
translated: 2026-09-22
---

# 用集成式机器学习实现低延迟移动 VR 图形

> 原文：[Using integrated ML to deliver low-latency mobile VR graphics](https://ai.facebook.com/blog/using-integrated-ml-to-deliver-low-latency-mobile-vr-graphics) · Meta AI（Wayback 存档）

**这是什么：** 一个面向使用移动芯片组的一体式 VR 设备、在渲染管线中运行机器学习的新型低延迟、低功耗框架。该架构使在这些设备上用机器学习显著提升图像质量和视频渲染成为可能。我们在此框架下创建了一个示例应用，用于重建更高分辨率的渲染（即超分辨率，super-resolution），在计算资源极其有限的移动芯片组上提升 VR 图形保真度。这个新框架还可用于流媒体内容的压缩伪影去除、帧预测、特征分析，以及注视点渲染（foveated rendering）引导的反馈。

**工作原理：** 在典型的移动 VR 渲染系统中，应用引擎在每帧开始时获取运动跟踪数据，并利用这些信息为每只眼睛生成图像。要在 VR 应用中有效工作，整条图形管线的处理时间通常受到严格约束——例如，为了达到 90 Hz 刷新率，两只眼睛缓冲的渲染时间预算为 11 毫秒。为克服这些约束，我们的新架构将模型执行卸载，使其在专用处理器上异步运行。在这一设计中，数字信号处理器（DSP）或神经网络处理单元（NPU）与图形处理器（GPU）流水线化，接收部分或全部已渲染的缓冲做进一步处理。处理后的内容由 GPU 的 timewarp 线程异步接手做延迟补偿，然后送往显示。

这张图展示了我们如何让机器学习模型在 DSP 上的执行与图形显示管线中的其他处理器并行。

为提升性能，我们修改了操作系统的图形内存分配系统，对 GPU-DSP 共享内存使用专用分配器。这比直接映射更高效，因为图形帧缓冲通常针对 GPU 独占访问优化（在 CPU 上表现很差），而且需要专门的内存注册流程以避免运行时远程调用带来的拷贝。

我们用一个示例应用测试了这条管线：对中心区域应用深度学习提升图像质量，而对场景其他部分使用更高效的低分辨率渲染。超分辨率后的内容在异步 timewarp 中与周围区域混合。如果我们按每个方向约 70% 的幅度降低渲染分辨率，可以节省约 40% 的 GPU 时间，开发者可以用这些资源生成更好的内容。为了在 VR 中获得时间上连贯、视觉上悦目的结果，我们开发了用专门设计的时间损失函数训练的循环网络（recurrent network）。下方视频展示了 2 倍超分辨率下网络预测与真值（ground truth）的质量对比。

这段视频以游戏 Beat Saber 为例演示这项研究工作的能力。左图由应用于 2 倍低分辨率内容的快速超分辨率网络生成，右图是全分辨率真值。

**为什么重要：** 打造下一代 VR 和 AR 体验，需要找到渲染高质量、低延迟图形的全新高效方式。传统渲染和超分辨率技术在 VR 头显使用的低余晖（low-persistence）显示器上可能不可接受，因为时间性伪影更容易被察觉。该方法提供了一条在移动芯片组设备上用 AI 应对这一挑战的新路。除 AR/VR 应用之外，我们相信这个新框架能为移动计算图形学的创新打开大门——解除内存约束，并为图像质量增强、伪影去除和帧外推等领域的新创新创造条件。

阅读完整论文：https://dl.acm.org/doi/10.1145/3355088.3365154

**作者**
- Behnam Bastani，首席系统架构师
- Haomiao Jiang，渲染工程师
- Rohit Rao Padebettu，软件工程师
- Kazuki Sakamoto，软件工程师
