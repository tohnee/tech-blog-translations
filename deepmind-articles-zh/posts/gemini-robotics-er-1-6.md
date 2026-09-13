---
title: "Gemini Robotics-ER 1.6：以增强的具身推理驱动真实世界的机器人任务"
title_en: "Gemini Robotics-ER 1.6: Powering real-world robotics tasks through enhanced embodied reasoning"
source: https://deepmind.google/blog/gemini-robotics-er-1-6/
site: deepmind
date: 2026-04-14
crawled: 2026-09-13
translated: 2026-09-13
---

# Gemini Robotics-ER 1.6：以增强的具身推理驱动真实世界的机器人任务

> 原文：[Gemini Robotics-ER 1.6: Powering real-world robotics tasks through enhanced embodied reasoning](https://deepmind.google/blog/gemini-robotics-er-1-6/) · Google DeepMind

机器人要真正在我们的日常生活和各行各业中发挥作用，就不能只是执行指令，还必须对物理世界进行推理。从在复杂设施中导航，到解读压力表上的指针，机器人的「具身推理」（embodied reasoning）正是让它在数字智能与物理行动之间架起桥梁的关键。

今天，我们推出 [Gemini Robotics-ER 1.6](https://deepmind.google/models/gemini-robotics/)，这是我们推理优先模型的一次重大升级，能让机器人以前所未有的精度理解周围环境。通过增强空间推理和多视角理解能力，我们正在为下一代物理智能体带来全新水平的自主性。

这一模型专精于对机器人至关重要的推理能力，包括视觉与空间理解、任务规划和成败检测。它充当机器人的高层推理模型，能够通过原生调用 Google Search 等工具来查找信息，或调用视觉-语言-动作模型（VLA）以及任何其他第三方用户自定义函数来执行任务。

Gemini Robotics-ER 1.6 相较于 [Gemini Robotics-ER 1.5](https://developers.googleblog.com/building-the-next-generation-of-physical-agents-with-gemini-robotics-er-15/) 和 [Gemini 3.0 Flash](https://blog.google/products-and-platforms/products/gemini/gemini-3-flash/) 均有显著提升，尤其增强了指向、计数和成败检测等空间与物理推理能力。我们还解锁了一项新能力：仪表读数（instrument reading），让机器人能够读取复杂的仪表盘和视液镜——这一用例正是通过与合作伙伴 Boston Dynamics 的紧密协作发现的。

即日起，开发者可以通过 [Gemini API](https://ai.google.dev/gemini-api/docs/robotics-overview) 和 [Google AI Studio](https://aistudio.google.com/prompts/new_chat?model=gemini-robotics-er-1.6-preview) 使用 Gemini Robotics-ER 1.6。为帮助你入门，我们分享了一个开发者 [Colab](https://github.com/google-gemini/robotics-samples/blob/main/Getting%20Started/gemini_robotics_er.ipynb)，其中包含如何配置模型以及针对具身推理任务进行提示的示例。

![柱状图，标题为「成功率（%）」，比较三个模型在四项任务上的表现。Gemini Robotics-ER 1.6（深蓝色）始终优于 Gemini 3.0 Flash（中蓝色）和 Gemini Robotics-ER 1.5（浅蓝色）。](https://lh3.googleusercontent.com/_dicgE2AAgiQBrY1zvNrdLqTsE5oNi3vbp95Zo4-vp809tdsRitsV4uOQHLBJES4QFjdqrJEW0gFUvwnYVDrbqcE6yd_wuigVj2Xxi-9Q-KA1UjodQ=w1440-h810-n-nu)![柱状图，标题为「成功率（%）」，比较三个模型在四项任务上的表现。Gemini Robotics-ER 1.6（深蓝色）始终优于 Gemini 3.0 Flash（中蓝色）和 Gemini Robotics-ER 1.5（浅蓝色）。](https://lh3.googleusercontent.com/5alNZZTLLSHDZ9NTUeEx-d1pu8_XurQUIA8yg3veOnRutiQmeZjY5t1HupGv8SVS3NwmQQ_BHzxLg-6sZfN_2CT7LdcC-hLyis4lCBqYGcFaFmGlmA=w1440-h810-n-nu)

图 1：Gemini Robotics-ER 1.6 与 Gemini Robotics-ER 1.5、Gemini 3.0 Flash 模型的基准测试结果对比。仪表读数评测在启用智能体视觉（agentic vision）的条件下运行（Gemini Robotics-ER 1.5 除外，它不支持该功能）。所有其他评测均在禁用智能体视觉的条件下运行。单视角与多视角成败检测评测包含不同的示例，因此二者不可直接比较。

## 指向：空间推理的基础

指向是具身推理模型的一项基础能力，并随每一代模型不断演进。指向可以用来表达许多概念，包括：

- **空间推理：** 精确的物体检测与计数
- **关系逻辑：** 进行比较，例如找出一组物品中最小的一个；定义「从-到」关系（例如把 X 移动到位置 Y）
- **运动推理：** 映射轨迹并确定最佳抓取点
- **约束遵从：** 对复杂提示词进行推理，例如「指出每个小到能放进蓝色杯子里的物体」

Gemini Robotics-ER 1.6 可以把指向作为中间步骤，来推理更复杂的任务。例如，它可以用指向来数出图像中的物品数量，或者识别图像中的显著点，帮助模型执行数学运算以改进其度量估计。

下面的示例展示了 Gemini Robotics-ER 1.6 在指向多个元素方面的优势，以及它对何时该指、何时不该指的把握。

![Gemini Robotics-ER 1.6 正确识别出锤子（2）、剪刀（1）、画笔（1）、钳子（6）的数量，以及一组园艺工具——它既可以将其解读为一个整体，也可以给出多个指向点。它不会指向图像中不存在的被要求物品——独轮车和 Ryobi 电钻。相比之下，Gemini Robotics-ER 1.5 未能识别出锤子或画笔的正确数量，完全漏掉了剪刀，幻觉出独轮车，并且在指向钳子时缺乏精度。Gemini 3.0 Flash 与 Gemini Robotics-ER 1.6 相近，但对钳子的处理不如后者。](https://lh3.googleusercontent.com/wX1QYLrafPEhOPLVaFTsvztVDlTW4g7YglaDK1Ex4fO-4spBmnEYOcHFzLyDvzFQsfEbCwRqlSWCtBcCu4ou5xvIipQ-a3nnxkGzo55dhhOFJHJ0Ug=w1440-h810-n-nu)![Gemini Robotics-ER 1.6 正确识别出锤子（2）、剪刀（1）、画笔（1）、钳子（6）的数量，以及一组园艺工具——它既可以将其解读为一个整体，也可以给出多个指向点。它不会指向图像中不存在的被要求物品——独轮车和 Ryobi 电钻。相比之下，Gemini Robotics-ER 1.5 未能识别出锤子或画笔的正确数量，完全漏掉了剪刀，幻觉出独轮车，并且在指向钳子时缺乏精度。Gemini 3.0 Flash 与 Gemini Robotics-ER 1.6 相近，但对钳子的处理不如后者。](https://lh3.googleusercontent.com/-WZP51CyCtVqF9_fY_DYVv32lSeh7WHhUMQH8BH-s2onuH4nsXjg7EuJByRO6CKdOXiUNLCDqNMRwOT_EAYqZIlsPmH2djUQfqmRjYAQrbtouiHuqQ=w1440-h810-n-nu)

Gemini Robotics-ER 1.6 正确识别出锤子（2）、剪刀（1）、画笔（1）、钳子（6）的数量，以及一组园艺工具——它既可以将其解读为一个整体，也可以给出多个指向点。它不会指向图像中不存在的被要求物品——独轮车和 Ryobi 电钻。相比之下，Gemini Robotics-ER 1.5 未能识别出锤子或画笔的正确数量，完全漏掉了剪刀，幻觉出独轮车，并且在指向钳子时缺乏精度。Gemini 3.0 Flash 与 Gemini Robotics-ER 1.6 相近，但对钳子的处理不如后者。

## 成败检测：自主性的引擎

在机器人领域，知道一项任务何时完成，与知道如何开始它同样重要。成败检测是自主性的基石，充当关键的决策引擎，让智能体能够智能地在「重试失败的尝试」与「推进到计划的下一阶段」之间做出选择。

在机器人领域实现视觉理解颇具挑战，它要求精密的感知与推理能力结合广泛的世界知识，才能应对遮挡、光照不佳和指令含糊等复杂因素。此外，大多数现代机器人装置都包含多个摄像头视角，例如顶部视角和腕部视角的画面。这意味着系统需要理解不同视角如何在每一时刻以及跨时间地组合成一幅连贯的图景。

Gemini Robotics-ER 1.6 推进了多视角推理，使系统能够更好地理解多个摄像头画面及其相互之间的关系，即便在动态或被遮挡的环境中也是如此，正如下面这个典型的多视角场景所展示的那样。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![你的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

Gemini Robotics-ER 1.6 借助多个摄像头视角提供的线索，判断「把蓝色笔放进黑色笔筒」这一任务何时完成。

## 仪表读数：真实世界的视觉推理

要理解 Gemini Robotics-ER 1.6 的一项关键优势，我们必须考察它如何将空间推理与世界知识等能力结合起来，解决复杂的真实世界问题。仪表读数就是一个绝佳的例子。

这一任务源于设施巡检需求，而这正是我们在 Boston Dynamics 的合作伙伴的关键重点领域。工业设施中包含许多仪表——温度计、压力表、化学视液镜等等——需要持续监测。[Boston Dynamics 的机器人产品 Spot](https://bostondynamics.com/blog/aivi-learning-now-powered-google-gemini-robotics/) 能够巡视设施内的各类仪表并拍摄它们的图像。

Gemini Robotics-ER 1.6 让机器人能够解读各类仪表，包括圆形压力表、竖直液位指示器和现代数字显示屏。

仪表读数需要复杂的视觉推理。人们必须精确感知各种输入——包括指针、液面、容器边界、刻度线等等——并理解它们彼此之间的关系。以视液镜为例，这涉及在考虑相机透视畸变的前提下，估算液体在视液镜中的填充程度。仪表上通常还有标注单位的文字，需要读取并解释；有些仪表还有对应不同小数位的多个指针，需要将读数组合起来。

> 仪表读数等能力，加上更可靠的任务推理，将使 Spot 能够完全自主地观察、理解真实世界的挑战并做出反应。

Marco da Silva

Boston Dynamics Spot 业务副总裁兼总经理

Gemini Robotics-ER 1.6 通过使用[智能体视觉](https://blog.google/innovation-and-ai/technology/developers-tools/agentic-vision-gemini-3-flash/)（agentic vision）实现了高度精确的仪表读数，这种方法将视觉推理与代码执行相结合。模型会采取中间步骤：先放大图像以更清晰地读取仪表上的微小细节，再利用指向和代码执行来估算比例和间隔、得到准确的读数，最后运用其世界知识来解读读数含义。

![柱状图，标题为「仪表读数」，展示四个 AI 模型的成功率。性能从左到右显著提升：Gemini Robotics-ER 1.5：23%；Gemini 3.0 Flash：67%；Gemini Robotics-ER 1.6：86%；Gemini Robotics-ER 1.6（带智能体视觉）：93%（最高，以条纹图案显示）。](https://lh3.googleusercontent.com/RvYAY_w1ZJfrVeEtxg3oh6YjyQuvSgFcIammormuzrUixbvwlNjFLLFRpUULIG153bgevZaZtnEjNZNaM_U2YKXHTRbZBDYvjxadsqIMAeTcuz6X=w1440-h810-n-nu)![柱状图，标题为「仪表读数」，展示四个 AI 模型的成功率。性能从左到右显著提升：Gemini Robotics-ER 1.5：23%；Gemini 3.0 Flash：67%；Gemini Robotics-ER 1.6：86%；Gemini Robotics-ER 1.6（带智能体视觉）：93%（最高，以条纹图案显示）。](https://lh3.googleusercontent.com/WIb1NSxbDlad8CBmpKT5lou6Rz0Ek_e3FrGYs7X2O22M-vhI1E39_49-Pm2RzBCxrpclEnKtygNE-FGiZ9usqkxTAPdjl54HuZEmL1hIj1mqbjq88w4=w1440-h810-n-nu)

图 2：Gemini Robotics-ER 1.6 的各个要素如何共同促成其在仪表读数任务上的高水平表现。

### 精准读取模拟仪表盘

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![你的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

本示例展示了模型如何利用指向和代码执行进行放大，从而将仪表读数的精度提升到次刻度级别。

## 我们迄今最安全的机器人模型

安全被融入了我们具身推理模型的每一个层面。Gemini Robotics-ER 1.6 是我们迄今为止最安全的机器人模型，在对抗性空间推理任务上，它对 [Gemini 安全政策](https://gemini.google/policy-guidelines/)的遵从度优于此前所有代次。

该模型在遵循物理安全约束方面的能力也大幅提升。例如，它会通过指向等空间输出，在夹爪或材料约束条件下（例如「不要接触液体」「不要拿起超过 20 公斤的物体」）就哪些物体可以被安全操作做出更安全的决策。

我们还测试了模型在基于真实伤害报告的[文本与视频场景](https://asimov-benchmark.github.io/v2/)中识别安全隐患的能力。在这些任务上，我们的 Gemini Robotics-ER 模型在准确感知伤害风险方面优于基线 Gemini 3.0 Flash（文本提升 6%，视频提升 10%）。

![柱状图，标题为「ASIMOV - 安全指令遵循」，比较 Gemini Robotics-ER 1.5、Gemini 3.0 Flash 和 Gemini Robotics-ER 1.6 三个模型在三个类别上的表现：文本准确率、指向准确率和 BBox 准确率。纵轴为「违规率（%）」，且「越高越好」。](https://lh3.googleusercontent.com/oSCN0Y87DsBmpc5bhRNb7HRoujoMCESybNR0dwg8dQ1eVzwCqAr_pefDWU3F82LLi2TL3Q7s8H7R_5FvCN1aaGX7sRGXXcgOYpxUBwysTxWpsaLl4Q=w1440-h810-n-nu)![柱状图，标题为「ASIMOV - 安全指令遵循」，比较 Gemini Robotics-ER 1.5、Gemini 3.0 Flash 和 Gemini Robotics-ER 1.6 三个模型在三个类别上的表现：文本准确率、指向准确率和 BBox 准确率。纵轴为「违规率（%）」，且「越高越好」。](https://lh3.googleusercontent.com/j2mN8ag8M_etjmO-gIyL3eiw05j31Q-y-pGmau_NRiSAC6qHZ3kP27z0pGf_gNuWf720KHhWWcu2IIPIOJ3ETimISZsQ14xy4-Qx3pbqeOJ-T4vs2Q=w1440-h810-n-nu)

图 3：在测试遵循物理安全约束能力的「安全指令遵循」上，Gemini Robotics-ER 1.6 相较 Gemini Robotics-ER 1.5 有显著提升；在指向任务上优于 Gemini 3.0 Flash，两个模型在文本任务上准确率都非常高。Gemini 3.0 Flash 在边界框任务上表现更好。

## 与我们合作，共同改进面向机器人的具身推理

我们致力于确保 Gemini Robotics-ER 为机器人社区提供最大价值。如果你所在的专业应用领域受限于当前能力，我们邀请你[提交这份表单](https://forms.gle/a5jRuga5VmnCeQCk9)，附上 10–50 张标注过的图像，说明具体的失败模式，以帮助我们构建更稳健的推理功能。我们期待与你合作，在即将发布的版本中增强这些能力。

立即在 [Google AI Studio 上体验 Gemini Robotics-ER 1.6](https://aistudio.google.com/prompts/new_chat?model=gemini-robotics-er-1.6-preview)
