---
title: "Open Catalyst 挑战赛：用 AI 发现用于可再生能源存储的催化剂"
title_en: "Open Catalyst Challenge: Using AI to discover catalysts for renewable energy storage"
date: 2021-06-17
source: https://ai.facebook.com/blog/open-catalyst-challenge-using-ai-to-discover-catalysts-for-renewable-energy-storage
crawled: 2026-09-22
translated: 2026-09-22
---

# Open Catalyst 挑战赛：用 AI 发现用于可再生能源存储的催化剂

> 原文：[Open Catalyst Challenge: Using AI to discover catalysts for renewable energy storage](https://ai.facebook.com/blog/open-catalyst-challenge-using-ai-to-discover-catalysts-for-renewable-energy-storage) · Meta AI（Wayback 存档）

许多形式的可再生能源（如燃料电池）依赖使用催化剂来提升效率、降低生产成本的化学反应。然而，通过物理实验或传统模拟来发现新催化剂极其困难且耗时。为了寻找一种更好的可再生能源生产方式，Facebook AI 与卡内基梅隆大学化学工程系合作创建了 Open Catalyst Project。这一研究计划旨在利用机器学习（ML）加速寻找低成本催化剂，用于驱动将可再生能源转化为易于存储形式的反应。

我们现在启动 Open Catalyst 挑战赛——一项在 NeurIPS 2021 上举办的公开竞赛，邀请研究人员构建新的机器学习模型来模拟分子在催化剂表面的相互作用。如果成功，这些新技术可用于对数百万甚至数十亿种潜在催化剂材料进行筛选，服务于可再生能源存储和太阳能燃料生成所涉及的化学反应。

本次挑战赛基于我们去年公开发布的 OC20 数据集。据我们所知，这是世界上最大的量子力学模拟数据集，包含约 120 万次分子弛豫，来自约 2.5 亿次密度泛函理论（DFT）计算。基线模型、代码和评估指标已在我们的 GitHub 仓库中提供。

## 用 AI 预测弛豫能量

DFT 等量子力学模拟工具可用于识别可能有效的催化剂分子。它们估计系统的能量，并试图找到能量最低（「弛豫」）状态的构型。但这些方法计算密集，要评估数十亿种可能的催化剂需要数千年时间。

为推动寻找更好的方法，今年的 Open Catalyst 挑战赛聚焦一项主要任务：初始结构到弛豫能量（Initial Structure to Relaxed Energy，IS2RE）。在该任务中，输入是初始结构（例如 DFT 弛豫轨迹的起始状态）的原子位置，目标是预测最终弛豫状态的能量。这些弛豫能量往往与催化剂的活性和选择性相关。

（原文此处嵌入视频。）

我们对参赛者可用于解决该任务的机器学习方法不做任何限制。解决 IS2RE 任务的一种途径是用机器学习近似 DFT 弛豫，即迭代估计原子所受的力并更新原子位置，直至达到弛豫状态，最终预测该状态的能量。在为近似 DFT 弛豫而构建的模型上评估 IS2RE 任务，有助于判断这种方法对于实际应用是否足够准确和快速。这些模型还有一个额外好处：能够预测弛豫后的结构，并加速未来的 DFT 计算。另一种途径是直接预测弛豫能量，而无需估计中间弛豫状态，因为弛豫过程中的许多变化（例如由特定初始猜测策略引起的）是系统性的。这类直接 IS2RE 方法可能带来计算效率上更大的提升。

我们鼓励提交比 DFT 快得多的方案。例如，使用 DFT 进行一次标准弛豫需要 8-10 小时，而机器学习方法有望将每次弛豫缩短到 10 秒以内，或每次直接预测缩短到 1 秒以内——至少 1,000 倍的改进。我们希望这项挑战赛能让研究人员和科学家从他人的工作中学习，并推动这一重要任务的进展。

参赛指南以及数据集划分和评估指标的细节见此处。参赛者必须在 10 月 6 日前将预测结果提交到 EvalAI 上的公开评估服务器。我们将在 NeurIPS 2021 的 Open Catalyst Challenge 环节公布挑战赛排行榜，并邀请获胜团队分享他们的工作。

**作者**

- Abhishek Das，研究科学家
- Larry Zitnick，研究科学家
