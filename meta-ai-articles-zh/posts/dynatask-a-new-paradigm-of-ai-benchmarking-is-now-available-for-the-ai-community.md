---
title: "Dynatask：面向 AI 社区的新一代 AI 基准测试范式现已可用"
title_en: "Dynatask, a new paradigm of AI benchmarking is now available for the AI community"
date: 2021-09-24
source: https://ai.facebook.com/blog/dynatask-a-new-paradigm-of-ai-benchmarking-is-now-available-for-the-ai-community
crawled: 2026-09-22
translated: 2026-09-22
---

# Dynatask：面向 AI 社区的新一代 AI 基准测试范式现已可用

> 原文：[Dynatask, a new paradigm of AI benchmarking is now available for the AI community](https://ai.facebook.com/blog/dynatask-a-new-paradigm-of-ai-benchmarking-is-now-available-for-the-ai-community) · Meta AI（Wayback 存档）

2021 年 9 月 24 日

Facebook AI 推出 Dynabench——一个从根本上重新思考 AI 基准测试的开创性平台——已有一年。从今天起，我们为 AI 社区解锁 Dynabench 的全部能力：AI 研究者现在可以免费创建自己的自定义任务，在更灵活、动态和真实的场景中更好地评估自然语言处理（NLP）模型的性能。这一名为 Dynatask 的新特性，让研究者能够轻松借助人类标注者，通过自然交互主动欺骗 NLP 模型并识别其弱点。与以往基于固定数据点测试、容易饱和的基准相比，这种动态方式可以说更好地反映了人们的行为与反应。研究者还可以使用我们的评估即服务能力，在我们的动态排行榜上比较模型——它超越了单纯的准确率，探索对公平性、鲁棒性、计算和内存的更整体度量。

Dynabench 最初以四个任务启动：自然语言推理（由北卡罗来纳大学教堂山分校的 Yixin Nie 和 Mohit Bansal 创建）、问答（由 UCL 的 Max Bortolo、Pontus Stenetorp 和 Sebastian Riedel 创建）、情感分析（由斯坦福大学的 Atticus Geiger 和 Chris Potts 创建）以及仇恨言论检测（由图灵研究所的 Bertie Vidgen 和谢菲尔德大学/西蒙弗雷泽大学的 Zeerak Waseem Talat 完成）。过去一年，我们推出了视觉问答任务和低资源机器翻译任务，还为机器翻译研讨会（WMT）的多语言翻译挑战提供了支持。累计而言，这些动态数据收集工作迄今已产出八篇发表论文、40 万个原始示例和四个开源大规模数据集。

「Dynatask 为任务创建者打开了一个充满可能性的世界。他们几乎不需要编程经验就能建立自己的任务，轻松自定义标注界面，并与托管在 Dynabench 上的模型交互。这使动态对抗数据收集对研究社区来说可及得多。」——伦敦大学学院 Max Bartolo。

现在，我们希望通过为整个 AI 社区启用自定义 NLP 任务，赋能该领域探索全新的研究方向。高质量、整体性的模型评估对 AI 的长期成功至关重要，我们相信作为协作努力的 Dynabench 将在基准测试的未来扮演重要角色。

## 如何使用 Dynatask

Dynatask 高度灵活、可定制。单个任务可以有一个或多个所有者，由他们定义每个任务的设置。例如，所有者可以选择在评估即服务框架中想使用哪些现有数据集。他们可以从多种评估指标中选择来衡量模型表现，不仅包括准确率，还包括鲁棒性、公平性、计算和内存。任何人都可以把模型上传到任务的评估云，在选定的数据集上计算分数和其他指标。一旦这些模型被上传并评估，就可以将它们放入循环，用于动态数据收集和人在环评估。任务所有者还可以通过 dynabench.org 的网页界面或与标注者（如 Mechanical Turk）收集数据。

让我们通过一个具体例子来了解各个组件。假设还没有自然语言推理任务，而你想创建一个。

- **第 1 步：**登录你的 Dynabench 账户，在个人资料页填写「申请新任务」表单。
- **第 2 步：**获批后，你将拥有一个专属任务页面和由你（作为任务所有者）控制的相应管理仪表盘。
- **第 3 步：**在仪表盘上，选择模型上传后要评估的现有数据集，以及你想用于评估的指标。
- **第 4 步：**接着提交基线模型，或请社区提交。
- **第 5 步：**如果你想收集新一轮动态对抗数据（让标注者创建骗过模型的示例），可以向系统上传新的上下文，并通过任务所有者界面开始收集数据。
- **第 6 步：**一旦你积累了足够的数据并发现在这些数据上训练有助于改进系统，就可以上传更好的模型，再把它们放进数据收集循环，构建更强大的模型。

我们正是用同样的基本流程构建了若干动态数据集，例如对抗自然语言推理（Adversarial Natural Language Inference）。现在，随着我们的工具向更广泛的 AI 社区开放，任何人都可以构建人与模型在环的数据集。

## 现在就开始使用 Dynatask

Dynabench 以社区为中心。我们希望赋能 AI 社区探索更好、更整体、更可复现的模型评估方法。我们的目标是让任何人都能轻松构建高质量的人与模型在环数据集。借助 Dynatask，你可以超越只有准确率的排行榜，走向与模型交互者的期望和需求更紧密对齐的、更整体的 AI 模型评估。

在 Facebook AI，我们信奉协作的开放科学、科学严谨性和负责任的创新。当然，随着社区的成长，平台将继续演进和变化，这也符合它的动态本质。我们邀请你加入我们的 Dynabench 社区：创建骗过现有模型的新示例、上传新模型接受评估，或现在就申请你自己的 Dynabench 任务。

前往用户资料下的 Tasks，今天就开始创建任务。

**作者**

- Tristan Thrush，研究助理
- Adina Williams，研究科学家
- Douwe Kiela，研究科学家
