---
title: "用深度神经网络在 Oculus Quest 上实现精确手部追踪"
title_en: "Using deep neural networks for accurate hand-tracking on Oculus Quest"
date: 2019-03-15
source: http://ai.facebook.com/blog/hand-tracking-deep-neural-networks
crawled: 2026-09-22
translated: 2026-09-22
---

# 用深度神经网络在 Oculus Quest 上实现精确手部追踪

> 原文：[Using deep neural networks for accurate hand-tracking on Oculus Quest](http://ai.facebook.com/blog/hand-tracking-deep-neural-networks) · Meta AI（Wayback 存档）

**研究内容：**Facebook Reality Labs 与 Oculus 的研究者和工程师共同开发了迄今唯一一个完全依靠单色摄像头的全关节手部追踪 VR 系统。该系统不使用主动深度传感技术，也不需要任何额外设备（如带传感器的手套）。我们将以软件更新的形式，把这项技术部署到 Oculus Quest——现已面向消费者发售的无线一体式 VR 头显上。通过 Quest 的四个摄像头，结合深度学习与基于模型追踪的新技术，我们实现了比基于深度的方案更大的手部追踪交互范围，而体积、重量、功耗和成本却只有其零头。处理完全在设备端完成，系统经过优化以支持交互手势，例如指向和捏合选择。

**工作原理：**深度神经网络用于预测人手的位置以及关键点（如手部关节）。这些关键点随后被用来重建人手与手指的 26 自由度姿态，得到一个包含手部构型与表面几何的 3D 模型。API 将让开发者能够在应用中使用这些 3D 模型来启用新的交互机制或驱动用户界面。我们采用了一种新颖的追踪架构，可在多种环境下稳健地产出精确、低抖动的手部姿态估计；同时采用高效的量化神经网络框架，在移动处理器上实现实时手部追踪，而不挤占留给用户应用的资源。

**为什么重要：**精确的手部追踪将解锁一系列新体验，并降低 Quest 上现有体验的使用门槛。例如，人们可以仅用一个手势就在 VR 中暂停电影，在社交游戏中更自然地表达自己。在企业应用中，培训师可以主持基于 VR 的培训课程，而无须维护一整套需要配对和充电的手柄。更广泛地说，手部追踪将让 VR 感觉更自然、更直观，帮助开发者创造人们在虚拟世界中交互的新方式。Facebook Reality Labs 和 Oculus 将寻找基于这一核心技术的更多方式，在未来增强其他 AR/VR 体验。

作者：
- Shangchen Han，研究工程师
- Beibei Liu，研究科学家
- Tsz Ho Yu，计算机视觉工程师
- Randi Cabezas，研究科学家
- Peizhao Zhang，研究科学家
- Peter Vajda，软件工程经理
- Eldad Isaac，软件工程经理
- Robert Wang，研究科学家经理
