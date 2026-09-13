---
title: "Google DeepMind 参加 NeurIPS 2023"
title_en: "Google DeepMind at NeurIPS 2023"
source: https://deepmind.google/blog/google-deepmind-at-neurips-2023/
site: deepmind
date: 2023-12-08
crawled: 2026-09-13
translated: 2026-09-13
---

# Google DeepMind 参加 NeurIPS 2023

> 原文：[Google DeepMind at NeurIPS 2023](https://deepmind.google/blog/google-deepmind-at-neurips-2023/) · Google DeepMind

迈向更多模态、更鲁棒、更通用的 AI 系统

下周，第 37 届神经信息处理系统年度大会（NeurIPS）即将开幕，这是世界上最大的人工智能（AI）会议。[NeurIPS 2023](https://nips.cc/) 将于 12 月 10 日至 16 日在美国新奥尔良举行。

来自 Google DeepMind 各团队的团队将在主会与工作坊上发表 180 余篇论文。

我们将展示面向[全球天气预报](https://deepmind.google/discover/blog/graphcast-ai-model-for-faster-and-more-accurate-global-weather-forecasting/)、[材料发现](https://deepmind.google/discover/blog/millions-of-new-materials-discovered-with-deep-learning)和[为 AI 生成内容添加水印](https://deepmind.google/discover/blog/identifying-ai-generated-images-with-synthid/)的前沿 AI 模型演示。届时还将有机会聆听 [Gemini](https://deepmind.google/technologies/gemini/#introduction)（我们最大、最强的 AI 模型）背后的团队的分享。

以下是我们的部分研究亮点：

[Google DeepMind at NeurIPS 2023 日程](https://deepmind.events/events/neurips-2023/resources)[Google at NeurIPS 2023 博客](https://blog.research.google/2023/12/google-at-neurips-2023.html)

## 多模态：语言、视频、行动

![一组动作照片的网格：电灯开关、正在清洁的机械臂，以及桌上的积木。](https://lh3.googleusercontent.com/HYY6sjOk71mM7Qhh8EVzlVDdnsSzPdkCeUD0wzEE9KYC68UN9qL50izYPqdjMEEolE4ETIBDTLYn55AE9h-p_YMi6bh0d45fZ7GLBX-QyFGbSD6z=w1440)

UniSim 是一个真实世界交互的通用模拟器。

生成式 AI 模型可以作画、作曲和写故事。但无论这些模型在某一媒介上多么强大，大多数模型都难以把这些技能迁移到另一媒介。我们深入探讨了生成能力如何帮助跨模态学习。在一场 spotlight 报告中，我们展示[扩散模型可以无需额外训练就能用于图像分类](https://openreview.net/pdf?id=fxNQJVMwK2)。像 Imagen 这样的扩散模型以比其他模型更像人类的方式分类图像，依赖形状而非纹理。此外，我们还展示了仅仅[从图像预测字幕就能改进计算机视觉学习](https://openreview.net/pdf?id=A7feCufBhL)。我们的方法在视觉与语言任务上超越了现有方法，并展现出更大的扩展潜力。

更多模态的模型可以催生更有用的数字与机器人助手，帮助人们的日常生活。在一张 spotlight 海报中，我们[构建了能像人类一样与数字世界交互的智能体](https://openreview.net/pdf?id=3PjCt4kmRx)——通过截图以及键盘和鼠标操作。另外，我们展示通过[利用视频生成（包括字幕与隐藏字幕），模型可以通过为真实机器人动作预测视频方案来迁移知识](https://openreview.net/pdf?id=bo8q5MRcwy)。

下一个里程碑之一，可能是生成对人类、机器人和其他类型交互智能体所执行动作做出响应的真实体验。我们将展示 [UniSim](https://universal-simulator.github.io/unisim/)（我们的真实世界交互通用模拟器）的演示。这类技术可以在从电子游戏、电影，到为真实世界训练智能体等各行各业中找到应用。

## 构建安全且可理解的 AI

![下方铺着一块用来接住积木的毯子，上面是彩色的积木。](https://lh3.googleusercontent.com/CQHfz0ozRHIIEp-2Bkyl4naTv1wZX5CISfedfMoE5I7QGsrLNH_4QC78bT75gqfwQnF363E_IaHf8GY1_u51iOpBnt8vhhMVbNUOYkhe9tFwtd26IA=w1440)

一幅由艺术家创作的人工智能（AI）插图。本图描绘 AI 安全研究。由艺术家 Khyati Trehan 创作，作为 Google DeepMind 发起的 Visualising AI 项目的一部分。

在开发和部署大型模型时，隐私需要贯穿每一步。

在一篇获得 [NeurIPS 最佳论文奖](https://blog.neurips.cc/2023/12/11/announcing-the-neurips-2023-paper-awards/)的论文中，我们的研究者展示了如何评估隐私保护的[训练，所用技术足够高效](https://openreview.net/pdf?id=q15zG9CHi8)可用于真实场景。在训练方面，我们的团队正在研究如何测量[语言模型是否在记忆数据](https://openreview.net/pdf?id=67o9UQgTD0)——以保护私密与敏感材料。在另一场口头报告中，我们的科学家研究了通过拥有不同访问级别和受攻击脆弱性的「学生」与「教师」模型进行[训练的局限](https://openreview.net/pdf?id=a2Yg9Za6Rb)。

大语言模型能生成令人印象深刻的回答，但容易产生「幻觉」——看似正确却是编造的文本。我们的研究者提出了一个问题：一种定位事实存储位置（localization）的方法能否实现对该事实的编辑。令人惊讶的是，他们发现[事实的定位与对位置的编辑并不能编辑该事实](https://openreview.net/pdf?id=EldbUlZtbd)，这暗示了理解和控制 LLM 中存储信息的复杂性。借助 Tracr，我们提出了一种评估可解释性方法的[新方式](https://openreview.net/pdf?id=tbbId8u7nP)：把人类可读的程序翻译成 Transformer 模型。我们已经[开源了 Tracr 的一个版本](https://github.com/google-deepmind/tracr)，帮助作为评估可解释性方法的真值基准。

## 涌现能力

![一幅抽象的多层建筑插图，包含楼梯、立柱和平台，点缀着绿色苔藓和垂下的藤蔓，象征 AI 涌现能力的概念结构。](https://lh3.googleusercontent.com/g2HYzBSuD-1M8R6_8ZCfXm_shrnh8yExnxBplKVmykYdmYTF_C5bPXlzBGOx0MK_qZ5SQWiVNA4cGA9SAdYiMa0th8civEWSv-8TPkxfl0nk6WcX3w=w1440)

一幅由艺术家创作的人工智能（AI）插图。本图想象通用人工智能（AGI）。由 Novoto Studio 创作，作为 Google DeepMind 发起的 Visualising AI 项目的一部分。

随着大型模型能力的增强，我们的研究正在拓展新能力的边界，以发展更通用的 AI 系统。

虽然语言模型被用于通用任务，但它们缺乏解决更复杂问题所必需的探索性思维和上下文理解。我们介绍 [Tree of Thoughts——一个语言模型推理的新框架](https://openreview.net/pdf?id=5Xc1ecxO1h)，帮助模型在广泛的可能解空间中探索和推理。通过把推理与规划组织成一棵树，而非常用的扁平思维链，我们证明语言模型能够更准确地解决诸如「24 点游戏」这样的复杂任务。

为了帮助人们解决问题、找到所需信息，AI 模型需要高效处理数十亿个独特取值。借助 [Feature Multiplexing，单一表示空间被用于多种不同特征](https://openreview.net/pdf?id=hJzEoQHfCe)，让大型嵌入模型（LEMs）得以扩展到服务数十亿用户的产品。

最后，借助 DoReMi，我们展示了用 AI 自动化[训练数据类型配比可以显著加快语言模型训练](https://openreview.net/pdf?id=lXuByUeHhd)，并提升在新任务和未见任务上的表现。

## 培育全球 AI 社区

我们很自豪能够赞助 NeurIPS，并支持由 [LatinX in AI](https://www.latinxinai.org/)、[QueerInAI](https://www.queerinai.com/) 和 [Women In ML](https://wimlworkshop.org/) 主持的工作坊，帮助促进研究合作，建设多元的 AI 与机器学习社区。今年，NeurIPS 将设立一个创意赛道，展示我们的 Visualising AI 项目——该项目委托艺术家创作更多元、更易懂的 AI 视觉表达。

如果你将参加 NeurIPS，欢迎来我们的展位，了解更多前沿研究，并与主持工作坊、在会议各环节作报告的团队见面。

**了解更多**

[Google DeepMind at NeurIPS 2023 日程](https://deepmind.events/events/neurips-2023/resources)[Google at NeurIPS 2023 博客](https://blog.research.google/2023/12/google-at-neurips-2023.html)
