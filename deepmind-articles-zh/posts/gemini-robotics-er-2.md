---
title: "推出 Gemini Robotics ER 2"
title_en: "Introducing Gemini Robotics ER 2"
source: https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-robotics-er-2/
site: deepmind
date: 2026-07-30
crawled: 2026-09-15
translated: 2026-09-15
---

# 推出 Gemini Robotics ER 2

> 原文：[Introducing Gemini Robotics ER 2](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-robotics-er-2/) · Google DeepMind

机器人要在日常环境中协助人类，仅有准确的空间推理是不够的。机器人还必须快速思考，让自己的决策与推理跟上物理世界的实时节奏。

正因如此，我们今天推出 [Gemini Robotics ER 2](https://deepmind.google/models/model-cards/gemini-robotics-er-2/)——我们能力最强的机器人"具身推理"（embodied reasoning）模型。可以把 Gemini Robotics ER 2 看作机器人的高层大脑。它让机器人能够与人类对话、理解物理世界并规划多步骤任务，然后将运动执行交由任意底层视觉-语言-动作（VLA）模型完成。Gemini Robotics ER 2 还能原生调用 Google Search 等工具来查找信息，也可以调用任何用户自定义的函数。Gemini Robotics ER 2 的设计让机器人在执行动作的同时就能"思考"接下来的步骤。

相较 [Gemini Robotics ER 1.6](https://deepmind.google/blog/gemini-robotics-er-1-6/)，Gemini Robotics ER 2 是一次重大升级。通过观看连续的视频流，机器人如今可以跟踪自身进度、在出现意外时灵活调整，并准确判断何时该进入下一步。我们还引入了多机器人协作，使多台机器人能够在共享空间中协同工作，完成单台机器人无法独立完成的复杂工作流。

Gemini Robotics ER 2 现已通过 [Gemini API](https://ai.google.dev/gemini-api/docs/robotics-overview) 和 [Google AI Studio](https://ai.dev/prompts/new_chat?model=gemini-robotics-er-2-preview) 向开发者公开提供，并在 [Gemini Enterprise Agent Platform](https://console.cloud.google.com/agent-platform/publishers/google/model-garden/gemini-robotics-er-2-preview-info) 上提供私密预览。为帮助你上手，我们分享了[示例](https://github.com/google-gemini/robotics-samples/blob/main/Getting%20Started/gemini_robotics_er.ipynb)，展示如何配置该模型并通过提示词驱动它完成更实用的物理 AI 任务。

## 提升物理智能体式（agentic）能力

物理世界中的大多数任务都很复杂，需要多个步骤才能完成。Gemini Robotics ER 2 是一个物理智能体，为机器人编排步骤，使其能够自我纠正，并泛化到更新颖的情境。要构建智能体式设置，开发者可以把底层控制接口——如视觉-语言-动作（VLA）模型或导航 API——声明为工具，并将多模态视频、音频或文本直接流式输入模型。

Gemini Robotics ER 2 改进了这一工具编排工作流。我们可以用仿真中的机器人、真实世界的机器人控制来评估它的表现，甚至可以把它与远程操控机器人的人类配对进行评估。

在真实 VLA、仿真 VLA 和人工遥操作（tele-op）三种控制模式下，Gemini Robotics ER 2 的工具编排表现均稳定优于 ER 1.6。

![比较 Gemini Robotics ER 1.6 与 Gemini Robotics ER 2 物理智能体表现的图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Physical_agent_performance_Chart.width-1200.format-webp.webp)

在机器人领域，高层推理取决于执行速度。Gemini Robotics ER 2 集成到 [Gemini Live API](https://ai.google.dev/gemini-api/docs/live-api) 中，使用针对延迟敏感任务优化的双向流式端点。其结果是流畅的编排：Gemini Robotics ER 2 指挥动作模型和机器人 API 完成多步骤任务，而不会出现令人不适的"停下来思考"式停顿。

为了直观展示这一点，我们与合作伙伴 [Boston Dynamics](https://bostondynamics.com/) 一起，用 [Spot](https://bostondynamics.com/products/spot/) 打造了一个演示。我们使用 Gemini Robotics ER 2 来编排 [Spot API](https://dev.bostondynamics.com/python/readme)（如导航和机械臂运动），打造出一台可为你取物的交互式机器人。

由 Gemini Robotics ER 2 驱动的 Boston Dynamics Spot 根据一条自然语言指令取来一份爆米花零食。

相关代码及其他示例已在 [Github](https://github.com/google-gemini/robotics-samples/tree/main/live-api) 上提供。

## 解锁时间智能，稳健完成任务

机器人领域最棘手的难题之一，是判断任务何时才算完成。Gemini Robotics ER 2 在视频理解和进度跟踪方面带来了阶跃式提升，可在切换到下一个任务之前，验证拧灯泡、系垃圾袋等复杂任务是否已按规范完成。

在本次更新中，我们在任务进度理解的两项基础能力上取得了进展：进度分类和时刻定位。

### 连续进度分类

进度分类指机器人跟踪任务完成进度的能力。在我们的评测中，模型需要将视频流中的每一帧划入五个进度等级（0-20%、20-40%、40-60%、60-80%、80-100%）之一。通过量化任务进度，Gemini Robotics ER 2 为机器人提供了实时的态势感知，使其能够即时调整动作，或重试失败的步骤，而无需重启整个工作流。

Gemini Robotics ER 2 在进度分类任务上达到 57.4% 的准确率，优于上一代模型和参与对比的前沿模型。

![比较不同机器人进度分类表现的图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Progress_Classification_Comparis.width-1200.format-webp.webp)

### 精准时刻定位

时刻定位衡量的是模型识别关键事件发生的那一帧视频的能力（例如何时停止向杯中倒咖啡）。Gemini Robotics ER 2 在时刻定位上取得了显著的性能提升，使机器人能够在任务之间精确切换、确认是否成功并提出纠正建议。

在时刻定位任务上，Gemini Robotics ER 2 达到 91.3% 的准确率和 0.96 秒的平均绝对距离。它与规模大得多的模型类别表现不相上下，却只以一小部分算力成本和 4 倍的执行速度就交付了这一精度——这正是要在真实世界中安全运行物理机器人实际所需的亚秒级延迟。

![时刻定位图表：准确率与距离的关系](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Moment_finding__accuracy_vs_dist.width-1200.format-webp.webp)

### 多机器人协作

没有任何单一机器人能胜任所有任务——轮式机器人擅长室内，而人形机器人可能更擅长不平坦的地形。Gemini Robotics 2 支持多机器人协作，让不同的机器通过共享的语义理解相互沟通，以交接并完成复杂任务。在[此处](https://deepmind.google/blog/gemini-robotics-2-brings-whole-body-intelligence-to-robots)了解 Gemini Robotics ER 2 如何让 [Apptronik](https://apptronik.com/) 的 [Apollo 2](https://apptronik.com/apollo/apollo-2) 与 [Franka F3 Duo](https://franka.de/mobile-fr3-duo) 协同工作。

## 提升通用空间智能

Gemini Robotics ER 2 推进了我们的核心空间推理能力，三项基准测试的结果如下：

- **成功/失败检测：** 现在基于原始视频流而非静态快照运行，能够捕捉执行中途的失败，例如洒漏、滑移或错位。
- **通用仪表读数：** 覆盖范围从圆形表盘和视液镜扩展到数字显示屏、线性刻度、直尺和液体温度计。我们在 10 种不同类型的仪表上对其进行了测试。
- **增强的空间 VQA：** 借助 Gemini 在多模态理解方面的进步，改进了视觉问答能力。

在所有核心能力上，Gemini Robotics ER 2 均稳定取得最高准确率，亮点包括成功检测（图像/视频）、问答（ERQA）和通用仪表读数。

![不同机器人 ER 指标对比](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/ER_metrics_comparison_Chart.width-1200.format-webp.webp)

## 推进具身智能的安全性

Gemini Robotics ER 2 是我们最安全的模型，在安全指令遵循和人类接近度基准测试上取得显著提升——这两项基准分别评估模型在推理任务中对物理约束的遵守情况，以及检测人类的空间感知能力。我们发现，当有人靠近时，Gemini Robotics ER 2 能成功地让人形机器人停止动作，并且只有当区域无人后才自主恢复工作。为了推进物理智能体的安全性，我们推出了一个新的基准测试，通过考察基础模型执行安全约束、监测环境、评估物理可行性以及主动寻求人类澄清的能力，来评估其作为安全 VLA 编排器的表现。详情请参阅我们的[安全技术报告](https://storage.googleapis.com/deepmind-media/gemini-robotics/Gemini-Robotics-2-Safety.pdf)。

在安全指令遵循和人类接近度基准测试上，Gemini Robotics ER 2 优于 ER 1.6 和其他前沿模型。

![不同机器人安全表现对比](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Safety_Performance_light_-_Chart.width-1200.format-webp.webp)

展望未来，我们计划推动这些模型去完成更复杂的任务，加速有用机器人的开发，并为机器人社区提供支持。
