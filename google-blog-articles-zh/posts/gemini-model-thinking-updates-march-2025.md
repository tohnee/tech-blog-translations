---
title: "Gemini 2.5：我们最智能的 AI 模型"
title_en: "Gemini 2.5: Our most intelligent AI model"
source: https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-model-thinking-updates-march-2025/
site: google-blog
date: 2025-03-25
crawled: 2026-09-13
translated: 2026-09-13
---

# Gemini 2.5：我们最智能的 AI 模型

> 原文：[Gemini 2.5: Our most intelligent AI model](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-model-thinking-updates-march-2025/) · Google

*最后更新于 3 月 26 日*

今天，我们推出 Gemini 2.5——我们最智能的 AI 模型。2.5 系列的首个版本是 2.5 Pro 的实验版，它在广泛的基准测试中达到业界最先进水平，并以显著优势在 [LMArena](https://lmarena.ai/?leaderboard) 上首次亮相即排名第一。

[Gemini 2.5 模型](https://deepmind.google/technologies/gemini)是思考（thinking）模型，能够在回答之前先对自身的思考进行推理，从而带来更强的性能和更高的准确性。

在 AI 领域，一个系统的「推理」能力不仅仅指分类和预测，更指它分析信息、得出逻辑结论、纳入上下文与细微差别，并做出明智决策的能力。

长期以来，我们一直在探索通过[强化学习](https://www.nature.com/articles/nature16961)和[思维链提示](https://arxiv.org/abs/2201.11903)等技术让 AI 更聪明、更擅长推理的方法。在此基础上，我们最近推出了第一个思考模型 [Gemini 2.0 Flash Thinking](https://deepmind.google/technologies/gemini/flash-thinking/)。

现在，借助 Gemini 2.5，我们通过将大幅增强的基础模型与改进的后训练相结合，实现了新的性能高度。接下来，我们会把这些思考能力直接构建到我们所有的模型中，让它们能够处理更复杂的问题，并支持更强大、更具上下文感知能力的智能体。

## 推出 Gemini 2.5 Pro

Gemini 2.5 Pro Experimental 是我们面向复杂任务的最先进模型。它以显著优势登顶衡量人类偏好的 [LMArena](https://lmarena.ai/?leaderboard) 排行榜，表明这是一个能力出众、兼具高质量风格的模型。2.5 Pro 还展现出强大的推理和代码能力，在常见的编程、数学和科学基准测试中处于领先地位。

Gemini 2.5 Pro 现已在 [Google AI Studio](http://aistudio.google.com/app/prompts/new_chat?model=gemini-2.5-pro-exp-03-25) 和 [Gemini 应用](https://gemini.google.com/)中面向 Gemini Advanced 用户提供，并将很快登陆 [Vertex AI](https://console.cloud.google.com/freetrial?redirectPath=/vertex-ai/studio)。我们还将在未来几周内公布定价，让用户能够以更高的速率限制将 2.5 Pro 用于规模化生产环境。

3 月 26 日更新：新增 MRCR（多轮共指消解，Multi Round Coreference Resolution）评测

![详细表格展示多个大语言模型在数学、编程和推理等测试上的表现。Gemini 2.5 Pro 在多个类别中名列前茅，以高亮单元格标示。底部的小字为数据提供了背景说明。](https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/gemini_benchmarks_cropped_light2x_1PPmDuP.gif)

## 增强的推理能力

在一系列需要高级推理的基准测试中，Gemini 2.5 Pro 达到了业界最先进水平。在不使用会增加成本的测试时技术（如多数投票）的情况下，2.5 Pro 在 GPQA 和 AIME 2025 等数学和科学基准测试中处于领先地位。

在「人类最后的考试」（Humanity's Last Exam）上，它还在不使用工具的模型中取得了业界最先进的 18.8% 的成绩——这一数据集由数百位领域专家设计，旨在捕捉人类知识与推理的前沿。

![柱状图对比 Gemini 2.5 Pro 与 OpenAI GPT-4.5、Claude 3.7 Sonnet 等 AI 模型在推理、科学和数学三个类别上的表现。Gemini 2.5 Pro 在所有类别中都表现出色。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/final_2.5_blog_1.width-1200.format-webp.webp)

## 高级编程能力

我们一直专注于编程性能，借助 Gemini 2.5，我们相比 2.0 实现了巨大飞跃——未来还会有更多改进。2.5 Pro 擅长创建视觉效果出众的 Web 应用和智能体化代码应用，以及代码转换和编辑。在智能体代码评测的行业标杆 SWE-Bench Verified 上，Gemini 2.5 Pro 使用自定义智能体配置取得了 63.8% 的成绩。

下面是一个示例，展示 2.5 Pro 如何运用其推理能力，仅凭一行提示词生成可执行代码，从而创建一款电子游戏。

## 站在 Gemini 最佳特性的基础上

Gemini 2.5 建立在 Gemini 模型的过人之处之上——原生多模态和长上下文窗口。2.5 Pro 今日发布即配备 100 万 token 的上下文窗口（200 万 token 即将到来），并且性能强劲，较前代产品持续提升。它能够理解庞大的数据集，处理来自不同信息源的复杂问题，包括文本、音频、图像、视频，甚至整个代码仓库。

开发者和企业现在就可以在 [Google AI Studio](http://aistudio.google.com/app/prompts/new_chat?model=gemini-2.5-pro-exp-03-25) 中试用 Gemini 2.5 Pro，[Gemini Advanced](https://gemini.google.com/) 用户也可以在桌面端和移动端的模型下拉菜单中选择它。它将在未来几周内登陆 [Vertex AI](https://console.cloud.google.com/freetrial?redirectPath=/vertex-ai/studio)。

一如既往，我们欢迎反馈，以便以更快的速度持续改进 Gemini 出众的新能力——这一切的目标都是让我们的 AI 更有帮助。
