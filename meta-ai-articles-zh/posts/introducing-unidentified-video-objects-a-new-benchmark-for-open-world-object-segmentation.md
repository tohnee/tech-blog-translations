---
title: "推出 Unidentified Video Objects：开放世界物体分割新基准"
title_en: "Introducing Unidentified Video Objects, a new benchmark for open-world object segmentation"
date: 2021-08-12
source: https://ai.facebook.com/blog/introducing-unidentified-video-objects-a-new-benchmark-for-open-world-object-segmentation
crawled: 2026-09-22
translated: 2026-09-22
---

# 推出 Unidentified Video Objects：开放世界物体分割新基准

> 原文：[Introducing Unidentified Video Objects, a new benchmark for open-world object segmentation](https://ai.facebook.com/blog/introducing-unidentified-video-objects-a-new-benchmark-for-open-world-object-segmentation) · Meta AI（Wayback 存档）

**这是什么：**我们分享 Unidentified Video Objects（UVO）——一个促进开放世界分割研究的新基准。开放世界分割是计算机视觉的一项重要任务，目标是在视频中穷尽地检测、分割并跟踪所有物体。机器通常必须先学习特定的物体概念才能识别它们，而 UVO 可以帮助机器模仿人类检测陌生视觉物体的能力。

过去几年，物体分割已成为计算机视觉最活跃的研究领域之一，因为它是正确识别场景中物体、理解其位置的关键。为此，研究者提出了多种分割视觉场景中物体的方法，如 Mask R-CNN 和 MaskProp。这些最先进的模型在「封闭世界」假设下表现良好——在计算机视觉中，该假设认为模型看到的任何物体都必须属于预先确定的物体类别列表。换言之，模型在训练和部署阶段都已知道它应当检测与分割哪些概念。但在具身 AI 或增强现实助理等真实应用中，存在模型从未见过、也从未学过的无数物体概念，比如预定义词典之外的东西。由于不可能用所有这些开放世界的未见物体来训练模型，模型通常难以分割它们可能遇到的每一个物体。例如，若训练数据中没有长号或羽毛球，模型就很难在新影像中识别长号和羽毛球。而人类即便对陌生物体——如新式乐器或未知运动器材——毫无先验知识，也能检测到它们；尽管陌生，人们毫不费力就能把它们感知为独立的物体实例，就连 UFO 这种电影式的例子也会被识别为独立物体。因此，一个重要的研究问题是：机器是否也能在不预先知晓物体概念的情况下学会分割物体？这些问题促使我们探索开放世界设定：机器的任务是检测并分割它遇到的任何物体，无论已知还是未知。

UVO 包含取自流行的动作识别基准 Kinetics 的真实世界视频，附带稠密、穷尽、高质量的物体掩码标注。所含视频片段平均每段有 13.5 个独立物体实例，是基于封闭世界假设构建的现有数据集的八倍。我们相信 UVO 是一个多功能的试验台，供研究者开发开放世界物体分割的新方法，同时激发超越分类与检测、构建更全面视频理解的新研究——这在以往数据集与基准的设计下是不可能的。此外，为视频中的物体做标注极其耗费资源，这类工作此前从未有人做过。过去研究者主要聚焦于解决封闭世界问题——开放世界问题虽然重要，却难度大、常被忽视。我们希望通过提供 UVO 数据集唤起对这一研究领域的关注。我们已发布数据集标注的体验版，并在 ICCV 2021 组织挑战赛与研讨会。

（UVO 中视频帧的示例标注可视化；物体被以高质量掩码穷尽标注。）

**工作原理：**我们研究的核心直觉基于人类的能力：不论类别为何都能检测新物体，能检测并定位陌生物体。我们相信，开发出能应对开放世界设定的模型是可能的。我们的做法是从 Kinetics 数据集中随机选取视频，该数据集由来源广泛的 YouTube 视频构成。训练模型时，我们不预先定义要标注的物体，而是使用众包服务标注片段中所有可见物体。因此，数据集包含大量高难场景，包括经典分类体系之外的物体、快速移动的物体、运动模糊、拥挤场景等。这项工作如今能够完成，是因为我们采用了半自动化流水线：从已标注帧向未标注帧自动生成预测来辅助人类标注者；标注者无需从零开始，只需在预计算的掩码上做修正。

**为什么重要：**教会机器检测任何物体——无论熟悉还是全新——将使它们能够执行当今 AI 力不能及的众多重要任务。例如，物体搜索、实例配准、人-物交互建模和人类活动理解，都需要开放世界的预测能力。开放世界设定对机器人、自动驾驶或增强现实助理等领域中激动人心的新应用也是自然而然的，这些应用经常出现全新场景。当前的视频模型只能理解和预测很短的片段（约 2 秒）。而开放世界物体分割为长视频建模以及更复杂的预测任务提供了机会，比如学习视频或图像中物体之间的关系。它还使得在长视频片段中识别并检索物体成为可能，例如找出视频中出现的滑板画面。把像素分组为语义实体（包括未知类别），将为现有 3D CNN 提供合理的替代方案，例如对物体及其交互进行推理。

阅读完整论文

获取数据集

致谢：我们感谢 Abhijit Ogale、Mike Zheng Shou、Dhruv Mahajan、Kristen Grauman、Lorenzo Torresani、Manohar Paluri、Rakesh Ranjan 和 Federico Perazzi 对数据集的宝贵反馈；感谢 Jiabo Hu、Haoqi Fan 和 William Wen 的工程支持；感谢 Sally Yoo、Yasmine Babaei 和 Eric Alamillo 对标注后勤的支持；并感谢所有标注者的辛勤工作。

**作者**

- Weiyao Wang，软件工程师
- Matt Feiszli，研究科学家
- Heng Wang，应用研究科学家
- Du Tran，研究科学家
