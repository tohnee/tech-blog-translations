---
title: "开源 DeepFocus：让 VR 图像更逼真的 AI 系统"
title_en: "Open-sourcing DeepFocus, an AI-powered system for more realistic VR images"
date: 2018-12-19
source: https://ai.facebook.com/blog/open-sourcing-deepfocus-an-ai-powered-system-for-more-realistic-vr-images
crawled: 2026-09-22
translated: 2026-09-22
---

# 开源 DeepFocus：让 VR 图像更逼真的 AI 系统

> 原文：[Open-sourcing DeepFocus, an AI-powered system for more realistic VR images](https://ai.facebook.com/blog/open-sourcing-deepfocus-an-ai-powered-system-for-more-realistic-vr-images) · Meta AI（Wayback 存档）

**研究内容：**一个在 VR 中渲染自然、逼真聚焦效果的新型 AI 框架。DeepFocus 可配合先进的头显原型工作，实时渲染不同焦距下的模糊效果。例如，当佩戴支持 DeepFocus 的头显的人看向近处物体时，该物体会立即显得清晰锐利、处于焦点之中，而背景物体则显得失焦——正如现实生活中的样子。这种失焦模糊（也称视网膜模糊）对于在 VR 中实现真实感和深度感知非常重要。DeepFocus 是首个能为 VR 应用实时产生这一效果的系统。我们现在开源我们的工作和数据集，以帮助 VR 研究社区的其他人。

**工作原理：**一些传统方法（如使用累积缓冲区）可以实现物理上准确的失焦模糊。但它们无法对复杂、丰富的内容实时产生该效果，因为即便是最先进的芯片也难以满足其处理需求。我们转而用深度学习解决这个问题。我们开发了一个新颖的端到端卷积神经网络，在眼睛看向场景不同部位的瞬间就能生成带有准确视网膜模糊的图像。该网络包含新的保体积交错层（volume-preserving interleaving layer），用于在完全保留图像细节的同时降低输入的空间维度。网络的卷积层随后在同一降低后的空间分辨率上运算，显著缩短运行时间。

**为什么重要：**随着新型 VR 头显技术研究的推进，DeepFocus 将能够模拟产生极度逼真视觉所需的准确视网膜模糊。该平台还证明 AI 可以帮助解决在 VR 中渲染高计算量视觉的挑战。DeepFocus 为克服未来新型显示系统的实际渲染与优化限制奠定了基础。由于 DeepFocus 仅依赖标准 RGB-D 颜色和深度输入，它几乎可以与所有现有 VR 游戏和应用配合工作。它还兼容当前 VR 研究社区正在探索的三类支持调节（accommodation）的头显：可变焦显示器（如 Half Dome）、多焦点显示器（例如 FRL 的这项先前工作）以及光场显示器。

了解 Facebook Reality Labs 如何创建 DeepFocus 的更多细节。

**阅读完整论文：**DeepFocus: Learned Image Synthesis for Computational Displays
