---
title: "Google DeepMind 参加 NeurIPS 2024"
title_en: "Google DeepMind at NeurIPS 2024"
source: https://deepmind.google/blog/google-deepmind-at-neurips-2024/
site: deepmind
date: 2024-12-05
crawled: 2026-09-13
translated: 2026-09-13
---

# Google DeepMind 参加 NeurIPS 2024

> 原文：[Google DeepMind at NeurIPS 2024](https://deepmind.google/blog/google-deepmind-at-neurips-2024/) · Google DeepMind

推进自适应 AI 智能体、赋能 3D 场景创建、创新 LLM 训练，共创更智能、更安全的未来

下周，全球 AI 研究者将齐聚[第 38 届神经信息处理系统年度会议](https://neurips.cc/)（NeurIPS），会议将于 12 月 10 日至 15 日在温哥华举行。

两篇由 Google DeepMind 研究者主导的论文将因其对该领域"无可争议的影响"而获得[时间考验奖（Test of Time）](https://blog.neurips.cc/2024/11/27/announcing-the-neurips-2024-test-of-time-paper-awards/)。Ilya Sutskever 将介绍[《Sequence to Sequence Learning with Neural Networks》](https://arxiv.org/abs/1409.3215)，该论文与 Google DeepMind 突破性研究副总裁 Oriol Vinyals 以及杰出科学家 Quoc V. Le 合著。Google DeepMind 科学家 Ian Goodfellow 和 David Warde-Farley 将介绍[《Generative Adversarial Nets》](https://arxiv.org/abs/1406.2661)。

我们还将展示如何把基础研究转化为现实世界的应用，现场演示包括 [Gemma Scope](https://deepmind.google/discover/blog/gemma-scope-helping-the-safety-community-shed-light-on-the-inner-workings-of-language-models/)、[AI 音乐生成](https://deepmind.google/discover/blog/new-generative-ai-tools-open-the-doors-of-music-creation/)、[天气预报](https://deepmind.google/research/publications/24820/)等。

Google DeepMind 各团队将发表 100 多篇新论文，主题涵盖 AI 智能体、生成式媒体以及创新学习方法。

[Google Research at NeurIPS 2024 日程](https://research.google/conferences-and-events/google-at-neurips-2024/)

## 构建自适应、智能且安全的 AI 智能体

基于 LLM 的 AI 智能体在通过自然语言指令执行数字任务方面展现出潜力。然而，它们的成功依赖于与复杂用户界面的精确交互，而这需要大量训练数据。通过 [AndroidControl](https://neurips.cc/virtual/2024/poster/97433)，我们分享了迄今最多样化的控制数据集，包含跨 800 多个应用的 15,000 多条人工采集演示。使用该数据集训练的 AI 智能体表现出显著的性能提升，我们希望这有助于推动更具通用性的 AI 智能体研究。

AI 智能体要在任务间泛化，就需要从它遇到的每一次经历中学习。我们提出了一种[上下文内抽象学习](https://neurips.cc/virtual/2024/poster/96600)方法，帮助智能体从不完美的演示和自然语言反馈中把握关键任务模式与关系，从而提升其性能与适应性。

![一个人在炉灶前做饭的第一人称视角画面，厨房中的各种物体被编号以用于数据集演示。](https://lh3.googleusercontent.com/hYU1cKrYubfWtrnBJfHtPSCuvL0ivAGVV7f3ZbZM10v9tHrr-DUUhjzyZeGihb4-2aIaNlVtNeddEvRK2rz9WJtgR41FAGNTQkjlCcyXZSaP2dxYhQ=w1440)

一段制作酱汁的视频演示中的一帧，各个元素被识别并编号。ICAL 能够提取该过程中的重要方面

开发能够努力实现用户目标的智能体化 AI 有助于让这项技术更有用，但当 AI 代表我们行动时，对齐至关重要。为此，我们提出了一种[测量 AI 系统目标导向程度](https://neurips.cc/virtual/2024/poster/93645)的理论方法，并展示了[模型对其用户的感知如何影响其安全过滤器](https://neurips.cc/virtual/2024/poster/94269)。这些洞见共同凸显了稳健防护措施的重要性，以防止意外或不安全行为，确保 AI 智能体的行动始终与安全、预期的用途保持一致。

## 推进 3D 场景创建与仿真

随着游戏和视觉特效等行业对高质量 3D 内容需求的增长，创建逼真的 3D 场景仍然成本高昂且耗时。我们近期的工作引入了新颖的 3D 生成、仿真与控制方法，简化内容创作流程，实现更快、更灵活的工作流。

制作高质量、逼真的 3D 素材和场景通常需要捕捉并建模数千张 2D 照片。我们展示了 [CAT3D](https://neurips.cc/virtual/2024/poster/95046)，一个能在短短一分钟内从任意数量的图像——哪怕只有一张图像或一段文本提示词——创建 3D 内容的系统。CAT3D 通过一个多视角扩散模型从许多不同视点生成额外的一致性 2D 图像，并将这些生成的图像作为传统 3D 建模技术的输入。其结果在速度和质量上都超越了以往方法。

![一张示意图，展示 CAT3D 系统从各种输入创建 3D 内容：一只机器猫的文本提示词（左）、汽车里一只狗的单张照片（中）、以及乐高盆景树三个不同角度的照片（右）。蓝色箭头从这些输入向下指向生成的 3D 模型和多视点渲染结果。](https://lh3.googleusercontent.com/GY3_w3clElUUoznz1JSljAUCVXe-sx0XkAPh9vBrmnmDQqd74MZpsGDv1Au45MOUmvoJjeSGpuYdnrFDtQVUTCBgPQVlUaQPozUNZRF01AXFtsgggg=w1440)

CAT3D 支持从任意数量的生成图像或真实图像创建 3D 场景。

从左至右：文本到图像再到 3D、一张真实照片到 3D、多张照片到 3D。

用许多刚体仿真场景——比如杂乱的桌面或翻滚的乐高积木——在计算上同样非常昂贵。为了克服这一障碍，我们提出了一种名为 SDF-Sim 的[新技术](https://neurips.cc/virtual/2024/poster/95252)，它以可扩展的方式表示物体形状，加快碰撞检测，并能高效仿真大型复杂场景。

![数百只鞋子掉落并碰撞的复杂仿真，使用 SDF-Sim 精确建模](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/pile_of_shoes.gif)

使用 SDF-Sim 精确建模的鞋子掉落并碰撞的复杂仿真

基于扩散模型的 AI 图像生成器难以控制多个物体的 3D 位置和朝向。我们的解决方案 [Neural Assets](https://neural-assets.github.io/) 引入了物体专属的表示，通过在动态视频数据上训练，同时捕捉外观与 3D 姿态。Neural Assets 让用户能够在场景间移动、旋转或替换物体——这对动画、游戏和虚拟现实都是实用工具。

![一系列图像，按六列展示 Neural Assets 技术："Original Image"（原始图像）、"Translate Obj."（平移物体）、"Rotate Obj."（旋转物体）、"Rescale Obj."（缩放物体）、"Replace Obj."（替换物体）和"Replace Bg."（替换背景）。上排将这些编辑应用于绿色 3D 边界框标出的紫色鞋子，下排将它们应用于城市街道上的汽车。](https://lh3.googleusercontent.com/SdRwaLJ5jFNJAir4vEjMouPGAwPFi_1rBRdluqmSXxKoEh4ZsuFf3ciZqv8ak_9uJCReH0_MrgLCTxqF2fi6I9PNNLhzXheYXyqc_eXQm72CrKub=w1440)

给定一张源图像和物体的 3D 边界框，我们可以平移、旋转和缩放该物体，或在图像之间转移物体或背景

## 改进 LLM 的学习与响应方式

我们还在推进 LLM 的训练、学习和对用户的响应方式，在多个方面提升性能与效率。

借助更大的上下文窗口，LLM 现在可以一次从潜在的数千个样例中学习——这被称为多样本上下文内学习（many-shot in-context learning，ICL）。这一过程能提升模型在数学、翻译和推理等任务上的表现，但通常需要高质量的人工生成数据。为了让训练更具成本效益，我们探索了[改造多样本 ICL 的方法](https://neurips.cc/virtual/2024/poster/96277)，以减少对手工精选数据的依赖。可用于训练语言模型的数据是如此之多，团队构建模型的主要约束变成了可用算力。我们[回答了一个重要问题](https://arxiv.org/pdf/2405.15074)：在固定算力预算下，如何选择合适的模型规模以获得最佳结果？

另一种我们称之为[时间反转语言模型](https://neurips.cc/virtual/2024/poster/93684)（Time-Reversed Language Models，TRLM）的创新方法，探索了预训练并微调一个反向工作的 LLM。当把传统 LLM 的回答作为输入时，TRLM 会生成可能产生这些回答的查询。与传统 LLM 搭配使用时，这种方法不仅有助于确保回答更好地遵循用户指令，还能改进对摘要文本的引用生成，并增强针对有害内容的安全过滤器。

为大型 AI 模型整理高质量数据至关重要，但人工整理难以规模化。为此，我们的[联合样例选择](https://neurips.cc/virtual/2024/poster/97437)（Joint Example Selection，JEST）算法通过在更大的批次中识别最可学习的数据来优化训练，使训练轮数最多减少 13 倍、计算量减少 10 倍，超越了最先进的多模态预训练基线。

规划任务是 AI 面临的另一项挑战，尤其是在随机环境中，结果会受到随机性或不确定性的影响。研究者使用各种推理类型进行规划，但缺乏一致的方法。我们证明[规划本身可以被视为一种独特的概率推理类型](https://neurips.cc/virtual/2024/poster/95030)，并提出了一个框架，根据不同推理技术的规划效果对其进行排序。

## 凝聚全球 AI 社区

我们很自豪成为本届会议的钻石赞助商，并支持 [Women in Machine Learning](https://docs.google.com/document/d/1Yi_76ABz08xzF5On0h_vdob1wAl8LAAB4CvwfwJcjY8/edit?tab=t.0)、[LatinX in AI](https://www.latinxinai.org/) 和 [Black in AI](https://www.blackinai.org/) 在世界各地建设从事 AI、机器学习和数据科学工作的社区。

如果您今年参加 NeurIPS，欢迎莅临 Google DeepMind 和 [Google Research](https://research.google/conferences-and-events/google-at-neurips-2024/) 展台，在整个会议期间通过演示、工作坊等方式探索前沿研究。
