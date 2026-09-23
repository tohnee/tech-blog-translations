---
title: "Meta Segment Anything Model 如何为 Instagram Edits 应用的抠图功能提供支持"
title_en: "How Meta Segment Anything Model enables Cutouts in the Instagram Edits app"
date: 2025-05-01
source: https://ai.meta.com/blog/instagram-edits-cutouts-segment-anything
crawled: 2026-09-22
translated: 2026-09-22
---

# Meta Segment Anything Model 如何为 Instagram Edits 应用的抠图功能提供支持

> 原文：[How Meta Segment Anything Model enables Cutouts in the Instagram Edits app](https://ai.meta.com/blog/instagram-edits-cutouts-segment-anything) · Meta AI（Wayback 存档）

2025 年 5 月 1 日 · 阅读时长约 4 分钟

我们最近发布了 Edits——Instagram 为创作者打造的全新视频创作应用。Edits 为移动优先的创作者提供短视频创作的完整方案，现已在 iOS 和 Android 全球上线。这款新应用的一大亮点功能是「抠图」（Cutouts），它由 Meta Segment Anything Model（SAM）2.1 驱动——这是 Meta 基础人工智能研究（FAIR）团队创建的广受欢迎的开源分割模型。

「2024 年，我们构建了一个演示，既是研究的一部分，也是向研究界、独立开发者和大众展示 SAM 2 的一种方式，」Meta 研究工程经理 Nikhila Ravi 说，「我们从自己的视角开发了这个演示，但也很明显，它对使用 Meta 技术的人可能有很大的实用价值。」不到一年后，作为 Segment Anything Model 2.1 开发的这项研究，如今已成为 Edits 的重要组成部分。人们可以用抠图功能跨多个视频图层编辑、对视频的特定部分应用滤镜，并轻松地把文本和贴纸等元素放到物体后面。Edits 上线后的头 24 小时内，抠图功能被使用了数十万次。我们将其视为颇有影响力的视频创作工具，创作者在 Edits 中可以轻松使用，无需昂贵的软件或高级剪辑专长。

虽然应用内的体验流畅无缝，但 Meta FAIR 团队在幕后做了大量工作，确保 Segment Anything Model 能够顺利进入 Edits。「主要有三步：首先，用户要能够交互式地、正确地选中物体，」Ravi 解释说，「其次，要能正确地在整个视频中跟踪物体，即使物体离开画面。最后，我们要让 SAM 2.1 模型跑得足够快，给用户实时体验。」

Edits 中的抠图功能使用目标检测流水线，自动建议视频中某一帧里用户可能想抠出的物体。用户也可以切换到手动模式，交互式地添加正向点击以选择要纳入抠图的区域，以及排除区域的负向点击。Segment Anything Model 2.1 会预测一个高质量掩码，定义物体在所选帧中的边界。此后，真正的创作乐趣开始了：点击「跟踪」，SAM 2.1 便会跟踪物体，在视频的每一帧预测一致的掩码，生成抠图。得到抠图后，可以把它添加到新图层，并用 Edits 提供的众多其他工具以创意方式混合和编辑。

Segment Anything Model 2 为视频引入了实时、可提示的分割，而 FAIR 团队在 2024 年秋季发布的 SAM 2.1 中进一步提升了其能力。此次更新引入了额外的数据增强技术，模拟视觉相似物体和小物体的存在——SAM 2 此前在这些场景中表现挣扎。Segment Anything Model 2.1 还通过在更长的帧序列上训练模型、并对空间与对象指针记忆（object pointer memory）的位置编码做了一些调整，改进了 SAM 2 的遮挡处理能力。这一更新让抠图功能即使在被跟踪物体被遮挡或出画时也能表现良好。

我们与 PyTorch 和生产伙伴合作，做了多项针对推理速度和延迟的性能改进。在 NVIDIA H100 GPU 上，我们把模型吞吐量提升了 1.8 倍，端到端首帧预览延迟降低了 3 倍，确保应用用户获得良好体验。我们还在 GitHub 上的 SAM 2 开源仓库中交付了速度改进。「起初我们以为需要追求更激进的模型效率方法，比如量化，但惊喜地看到 Torch Inductor 仅需极少代码改动就能有效优化模型吞吐量，」Meta 研究科学家 Joseph Greer 说。

随着使用 Segment Anything Model 的人比以往任何时候都多，团队正专注于下一个重大发布：SAM 3。这一下一代模型将是我们首个能够使用开放词汇文本或点击提示，自动检测、分割并跟踪图像和视频中物体的模型，为图像和视频编辑工具等各行各业开辟新的可能。如果你有兴趣了解更多，请加入我们的候补名单以获取最新动态。

下载 Edits
