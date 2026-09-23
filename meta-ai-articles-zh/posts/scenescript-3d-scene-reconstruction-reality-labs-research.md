---
title: "介绍 SceneScript：一种新颖的 3D 场景重建方法"
title_en: "Introducing SceneScript, a novel approach for 3D scene reconstruction"
date: 2024-03-20
source: https://ai.meta.com/blog/scenescript-3d-scene-reconstruction-reality-labs-research
crawled: 2026-09-22
translated: 2026-09-22
---

# 介绍 SceneScript：一种新颖的 3D 场景重建方法

> 原文：[Introducing SceneScript, a novel approach for 3D scene reconstruction](https://ai.meta.com/blog/scenescript-3d-scene-reconstruction-reality-labs-research) · Meta AI（Wayback 存档）

2024 年 3 月 20 日

**要点**

- 今天，我们介绍 SceneScript——一种重建环境、表示物理空间布局的新颖方法。
- SceneScript 在模拟中使用 Aria Synthetic Environments 数据集训练，该数据集可供学术使用。

设想一副时尚、轻便的眼镜，它把情境化 AI 与显示屏结合，在你需要时无缝提供实时信息，并在你度过一天时主动提供帮助。要让这样一副增强现实（AR）眼镜成为现实，系统必须能够理解你物理环境的布局，以及世界在 3D 中的形状。这种理解让 AR 眼镜得以针对你和你的个人情境定制内容——比如把数字叠层与你的物理空间无缝融合，或为你提供逐向导航，帮你在陌生地点找路。

然而，构建这些 3D 场景表示是一项复杂任务。当前的 MR 头显（如 Meta Quest 3）基于来自摄像头或 3D 传感器的原始视觉数据，创建物理空间的虚拟表示。这些原始数据被转换为一系列描述环境显著特征的形状，如墙壁、天花板和门。通常，这些系统依赖预定义规则把原始数据转换为形状。但这种启发式方法往往导致错误，尤其是在具有独特或不规则几何结构的空间中。

## 介绍 SceneScript

今天，Reality Labs Research 发布 SceneScript——一种用语言生成场景布局和表示场景的新颖方法。SceneScript 不是用硬编码规则把原始视觉数据转换为房间建筑元素的近似，而是经训练用端到端机器学习直接推断房间的几何结构。由此得到的物理场景表示是：

- **紧凑的**——把内存需求降低到仅几个字节；
- **完整的**——产生清晰的几何，类似可缩放矢量图形；
- 且重要的是，**可解释的**——意味着我们可以轻松阅读并编辑这些表示。

## SceneScript 如何训练？

像 Llama 这样的大语言模型（LLM）使用一种叫「下一 token 预测」的技术运作：AI 模型根据之前的词预测句子中的下一个词。例如，如果你输入「猫坐在……」，模型会预测下一个词很可能是「垫子」或「地板」。SceneScript 利用了 LLM 所用的同一「下一 token 预测」概念。不过，SceneScript 模型预测的不是通用语言 token，而是下一个「建筑 token」，比如「墙」或「门」。通过为网络提供大量训练数据，SceneScript 模型学会了如何把视觉数据编码为场景的基本表示，再将其解码为描述房间布局的语言。这使 SceneScript 能够从视觉数据解读并重建复杂环境，并创建能有效描述其所分析场景结构的文本描述。

然而，团队需要大量数据来训练网络、教它物理空间通常如何布局——而且他们需要确保保护隐私。这带来了独特的挑战。

## 在模拟中训练 SceneScript

LLM 依赖海量训练数据——通常来自网络上的各种公开文本来源，但如此规模、可供训练端到端模型的物理空间信息库尚不存在。于是 Reality Labs Research 团队必须另寻出路。SceneScript 团队没有依赖物理环境的数据，而是创建了一个名为 Aria Synthetic Environments 的室内环境合成数据集。该数据集包含 10 万个完全独特的室内环境，每个环境都用 SceneScript 语言描述，并配有一段穿行该场景的模拟视频。每个场景中渲染的视频使用与 Project Aria（Reality Labs Research 用于加速 AI 与机器学习研究的眼镜）相同的传感器特性进行模拟。这一方式让 SceneScript 模型能够在保护隐私的条件下完全在模拟中训练。随后可以用 Project Aria 眼镜采集的真实世界影像验证模型，确认其泛化到真实环境的能力。去年，我们向学术研究者开放了 Aria Synthetic Environments 数据集，希望助力加速这一激动人心的研究领域的公共研究。

## 扩展 SceneScript 以描述物体、状态和复杂几何

SceneScript 的另一强项是可扩展性。只需在 Aria Synthetic Environments 数据集中描述门的场景语言里增加几个参数，网络就可以经训练准确预测物理环境中门的开启程度。此外，通过在建筑语言中添加新特征，还可以准确预测物体的位置，并进一步把物体分解为组成部分。例如，一张沙发在 SceneScript 语言中可以表示为一组几何形状，包括坐垫、腿和扶手。这种程度的细节终有一天可以供设计师用来创建真正适配各种物理环境的 AR 内容。

## 加速 AR、推动 LLM 前进，并推进 AI 与机器学习研究的技术前沿

SceneScript 可以为 MR 头显和未来的 AR 眼镜解锁关键用例，比如生成视障人士逐向导航所需的地图——卡内基梅隆大学在 2022 年已做过演示。SceneScript 还赋予 LLM 推理物理空间所需的词汇。这最终可能释放下一代数字助手的潜力，为它们提供回答复杂空间问题所需的物理世界上下文。例如，凭借推理物理空间的能力，我们可以向聊天助手提出这样的问题：「这张桌子放得进我的卧室吗？」或「粉刷这个房间需要几罐油漆？」无需找卷尺、记下尺寸、再用信封背面的粗略数学尽力估算，一个能访问 SceneScript 的聊天助手可以在短短几分之一秒内得出答案。我们相信，SceneScript 是通往真正 AR 眼镜、连接物理与数字世界之路上的重要里程碑。随着我们在 Reality Labs Research 深入挖掘这一潜力，我们为这一开创性方法将如何帮助塑造 AI 与机器学习研究的未来而振奋。

在此了解更多关于 SceneScript 的内容。获取论文
