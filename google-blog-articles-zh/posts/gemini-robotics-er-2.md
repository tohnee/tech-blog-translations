---
title: "Gemini Robotics ER 2 正式发布"
title_en: "Introducing Gemini Robotics ER 2"
source: https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-robotics-er-2/
site: google-blog
date: 2026-07-30
crawled: 2026-09-13
translated: 2026-09-13
---

# Gemini Robotics ER 2 正式发布

> 原文：[Introducing Gemini Robotics ER 2](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-robotics-er-2/) · Google

要让机器人在日常环境中协助人类，仅有精准的空间推理是不够的。机器人还必须快速思考，让自己的决策与推理跟上物理世界的实时节奏。

正因如此，我们今天正式发布 [Gemini Robotics ER 2](https://deepmind.google/models/model-cards/gemini-robotics-er-2/)——我们面向机器人领域最强大的「具身推理」（embodied reasoning）模型。你可以把 Gemini Robotics ER 2 看作机器人的高级大脑：它让机器人能够与人类对话、理解物理世界、规划多步骤任务，然后把运动执行交给任意给定的更底层视觉-语言-动作（VLA）模型。Gemini Robotics ER 2 还能原生调用 Google Search 等工具来查找信息，或调用任何用户自定义的函数。这样的设计让机器人可以在执行动作的同时「思考」接下来要做什么。

相较 [Gemini Robotics ER 1.6](https://deepmind.google/blog/gemini-robotics-er-1-6/)，Gemini Robotics ER 2 是一次重大升级。通过观察连续的视频流，机器人现在能够追踪自身进度、在出现意外时灵活调整，并准确知道何时进入下一步。我们还引入了多机器人协作，让多台机器人可以在共享空间中协同工作，完成单台机器人无法独立胜任的复杂工作流。

Gemini Robotics ER 2 现已通过 [Gemini API](https://ai.google.dev/gemini-api/docs/robotics-overview) 和 [Google AI Studio](https://ai.dev/prompts/new_chat?model=gemini-robotics-er-2-preview) 向开发者公开提供，并在 [Gemini Enterprise Agent Platform](https://console.cloud.google.com/agent-platform/publishers/google/model-garden/gemini-robotics-er-2-preview-info) 上开启私密预览。为帮助你上手，我们分享了如何配置模型并对其进行提示的[示例](https://github.com/google-gemini/robotics-samples/blob/main/Getting%20Started/gemini_robotics_er.ipynb)，以驱动更实用的物理 AI 任务。

## 推进物理智能体能力

物理世界中的大多数任务都很复杂，需要多个步骤才能完成。Gemini Robotics ER 2 是一个物理智能体：它为机器人编排任务步骤，使其能够自我纠错，并泛化到更多新颖情境。要搭建智能体化系统，开发者可以把底层控制接口——例如视觉-语言-动作（VLA）模型或导航 API——声明为工具，并将多模态视频、音频或文本直接流入模型。

Gemini Robotics ER 2 改进了这种工具编排工作流。我们可以在仿真环境中用机器人评估其性能，也可以在真实机器人控制下评估，甚至让它与一名远程操控机器人的人类搭档配合。

在真实 VLA、仿真 VLA 和人类遥操作三种控制模式下，Gemini Robotics ER 2 的工具编排表现均稳定超越 ER 1.6。

![比较 Gemini Robotics ER 1.6 与 Gemini Robotics ER 2 物理智能体性能的图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Physical_agent_performance_Chart.width-1200.format-webp.webp)

在机器人领域，高级推理有赖于执行速度。Gemini Robotics ER 2 集成了 [Gemini Live API](https://ai.google.dev/gemini-api/docs/live-api)，使用针对延迟敏感任务优化的双向流式端点。其结果是流畅的编排：Gemini Robotics ER 2 指挥动作模型和机器人 API 完成多步骤任务，没有令人不适的「停下来想一想」式停顿。

为了说明这一点，我们与合作伙伴 [Boston Dynamics](https://bostondynamics.com/) 的 [Spot](https://bostondynamics.com/products/spot/) 一起构建了一个演示。我们用 Gemini Robotics ER 2 来编排 [Spot API](https://dev.bostondynamics.com/python/readme)（例如导航和机械臂移动），打造出一台能为你取物的交互式机器人。

由 Gemini Robotics ER 2 驱动的 Boston Dynamics Spot 在收到自然语言指令后取来一份爆米花零食。

代码及更多示例已在 [Github](https://github.com/google-gemini/robotics-samples/tree/main/live-api) 上开放。

## 释放时序智能，实现稳健的任务完成

机器人领域最困难的挑战之一，是判断一项任务何时才算完成。Gemini Robotics ER 2 在视频理解和进度追踪上带来跨越式提升，用于验证复杂任务——比如拧紧灯泡或系紧垃圾袋——是否已按要求完成，然后再切换到下一个任务。

在本次更新中，我们在任务进度理解的两大基础能力上取得了进展：进度分类（progress classification）和关键时刻定位（moment finding）。

### 连续进度分类

进度分类指的是机器人追踪任务完成进度的能力。在我们的评测中，我们把视频流中的每一帧划入五个进度等级（0–20%、20–40%、40–60%、60–80%、80–100%）。通过量化任务进度，Gemini Robotics ER 2 为机器人提供了实时态势感知，使其能够即时调整动作，或在某个步骤失败时重试，而不必重启整个工作流。

Gemini Robotics ER 2 在进度分类任务上达到 57.4% 的准确率，优于上一代模型和其他竞品前沿模型。

![不同机器人进度分类表现对比图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Progress_Classification_Comparis.width-1200.format-webp.webp)

### 精准关键时刻定位

关键时刻定位衡量的是模型找出关键事件发生的精确视频帧的能力（例如，何时该停止往杯子里倒咖啡）。Gemini Robotics ER 2 在关键时刻定位上的性能显著提升，使机器人能够精准地在任务之间切换、验证是否成功并提出修正建议。

在关键时刻定位任务上，Gemini Robotics ER 2 达到了 91.3% 的准确率和 0.96 秒的平均绝对距离。它与规模大得多的模型类别不相上下，但只用了其中一小部分算力成本，执行速度却快 4 倍——而这低于一秒的延迟，正是现实世界中安全操控物理机器人所真正需要的。

![关键时刻定位：准确率与距离关系图](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Moment_finding__accuracy_vs_dist.width-1200.format-webp.webp)

### 多机器人协作

没有哪台机器人能胜任所有任务——轮式漫游车擅长室内作业，而人形机器人可能更适应崎岖地形。Gemini Robotics 2 支持多机器人协作，让不同的机器通过共享的语义理解进行通信，从而交接并完成复杂任务。点击[这里](https://deepmind.google/blog/gemini-robotics-2-brings-whole-body-intelligence-to-robots)看看 Gemini Robotics ER 2 如何让 [Apptronik](https://apptronik.com/) 的 [Apollo 2](https://apptronik.com/apollo/apollo-2) 与 [Franka F3 Duo](https://franka.de/mobile-fr3-duo) 展开协作。

## 提升通用空间智能

Gemini Robotics ER 2 提升了我们的核心空间推理能力，以三项基准测试衡量：

- **成功/失败检测：** 现在可作用于原始视频流而非静态截图，以捕捉执行过程中出现的洒漏、滑落或错位等失败。
- **通用仪表读数：** 不再局限于圆形表盘和观测玻璃管，还涵盖数字显示屏、线性刻度、直尺和液体温度计。我们在 10 种不同类型的仪表上进行了测试。
- **增强空间 VQA：** 借助 Gemini 在多模态理解上的进步，改进视觉问答。

Gemini Robotics ER 2 在所有核心能力上均取得最高准确率，亮点包括成功检测（图像/视频）、问答（ERQA）以及通用仪表读数。

![不同机器人 ER 指标对比](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/ER_metrics_comparison_Chart.width-1200.format-webp.webp)

## 推进具身智能的安全

Gemini Robotics ER 2 是我们最安全的模型，在 Safety Instruction Following 和 Human Proximity 两项基准测试上取得显著提升——这两项基准分别评估模型在推理任务中对物理约束的遵循程度，以及用于检测人类的空间感知能力。我们发现，当有人靠近时，Gemini Robotics ER 2 能成功让人形机器人停下，并只在确认区域无碍后才自主恢复工作。为推进物理智能体的安全，我们推出了一项新基准，通过测试模型执行安全约束、监控环境、评估物理可行性以及向人类求证澄清的能力，来评估基础模型作为安全 VLA 编排者的能力。详情请参阅我们的[安全技术报告](https://storage.googleapis.com/deepmind-media/gemini-robotics/Gemini-Robotics-2-Safety.pdf)。

Gemini Robotics ER 2 在 Safety Instruction Following 与 Human Proximity 基准测试上优于 ER 1.6 和其他前沿模型。

![不同机器人安全性能对比](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Safety_Performance_light_-_Chart.width-1200.format-webp.webp)

展望未来，我们计划推动这些模型应对更复杂的任务，以加速开发实用的机器人，并支持机器人社区的发展。
