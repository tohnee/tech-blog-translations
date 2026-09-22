---
title: "Grok 4.5 发布"
title_en: "Introducing Grok 4.5"
date: 2026-07-08
source: https://x.ai/news/grok-4-5
crawled: 2026-09-22
translated: 2026-09-22
---

# Grok 4.5 发布

> 原文：[Introducing Grok 4.5](https://x.ai/news/grok-4-5) · xAI

[返回新闻列表](/news)

2026 年 7 月 8 日

Grok 4.5 是 SpaceXAI 为编码、智能体任务和知识工作打造的最聪明模型。

[免费试用](https://x.ai/cli)[开始构建](https://console.x.ai)

今天，我们发布 **Grok 4.5**——SpaceXAI 最聪明的模型，为在编码、智能体（agentic）任务和知识工作中的卓越表现而打造。它是我们有史以来最强的模型，并与 [Cursor](https://cursor.com/blog/spacex-model-training) 联合训练。

## [真实世界工程中的卓越表现](#real-world-engineering-excellence)

Grok 4.5 的训练数据集涵盖编码、科学、工程和数学知识。凭借智能而高效的推理，Grok 4.5 在真实工程任务上表现出色，并在此类任务上超越同类领先模型。该模型同样擅长办公工作，在 Harvey 的法律智能体基准上排名第一。

DeepSWE 1.0DeepSWE 1.1Terminal Bench 2.1SWE Bench Pro

0%20%40%60%DeepSWE 得分（pass@1）66.1%Fable max64.3%GPT 5.5 xhigh62%Grok 4.555.8%Opus 4.8 max在各模型提供商自己的框架内

模型得分柱状图。DeepSWE 1.0（在各模型提供商自己的框架内）：Fable (max) 66.1%、GPT 5.5 (xhigh) 64.31%、Grok 4.5 62.0%、Opus 4.8 (max) 55.75%。DeepSWE 1.1（由 DataCurve 运行的 mini-swe-agent 框架）：Fable (max) 70%、GPT 5.5 (xhigh) 67%、Opus 4.8 (max) 59%、Grok 4.5 53%、GLM 5.2 44%。Terminal Bench 2.1：Fable (max) 84.3%、GPT 5.5 (xhigh) 83.4%、Grok 4.5 83.3%、Opus 4.8 (max) 78.9%。SWE Bench Pro 解决率：Fable (max) 80.4%、Opus 4.8 (max) 69.2%、Grok 4.5 64.7%、GLM 5.2 62.1%、GPT 5.5 (xhigh) 58.6%。

## [Grok 4.5 的训练](#training-grok-45)

Grok 4.5 在数万块 NVIDIA GB300 GPU 上训练，并采用了为超大规模运行设计的训练与稳定性技术。除了原始 token 数量之外，我们还在数据过滤和治理上投入巨大：去重、质量评分和面向领域的选择，使数据混合保持高覆盖、高信号。

我们扩展了强化学习，并尤其注重每 token 的智能。我们的 RL 训练覆盖数十万个任务，以多步软件工程和其他技术工作为中心，采用自动化和基于模型的评分。我们的技术栈为高度异步的训练而构建，智能体的 rollout 可以运行数小时，同时学习在数万块 GPU 上持续进行。其结果是在真实工程和智能体任务上更智能、更高效的推理。

### 一个提示词构建而成

Grok 4.5 的编码能力强得惊人，从有挑战性的 Rust 和 C/C++ 任务，到从提示词到上线的端到端应用构建。下面是一些由该模型用一个提示词构建的示例。即使规格说明极少，Grok 4.5 也能高效创建设计精良、端到端可用的应用。

太阳系

做一个漂亮的宇宙和太阳系模拟。要有可调节的时间加速、逼真的运动、轨道和星星。用 threejs。HUD 要样式精美并符合现代设计原则。

做一个漂亮的宇宙和太阳系模拟。要有可调节的时间加速、逼真的运动、轨道和星星。用 threejs。HUD 要样式精美并符合现代设计原则。

app.localhost — cosmos

正在加载太阳系…

## [比 flash 类模型更快](#faster-than-flash-models)

Grok 4.5 以 **80 TPS** 的快速模型级别速度提供服务。加上在相同任务上比最新领先模型高出两倍的 token 效率，该模型能更快地为你交付智能结果，且成本低得多。

Token 效率

每个 SWE Bench Pro 任务的平均输出 token 数

Grok 4.500

Opus 4.8 (max)00

4.2×更少的 token

070k tokens

Token 效率，每个 SWE Bench Pro 任务的平均输出 token 数——Grok 4.5 平均以 15,954 个输出 token 解决任务，约为 Opus 4.8 (max)（67,020 个）的 1/4.2

## [擅长办公工作](#excels-at-office-work)

Grok 4.5 现已是 [Grok Build](https://x.ai/cli) 的默认模型。除了编码能力之外，Grok Build 还能构建复杂的 Excel 模型，包括从网络调研、跨多表使用公式，甚至留下便签或备注供日后参考。

在 PowerPoint 和 Word 中，Grok 4.5 同样细致入微。该模型能够使用原生 PowerPoint 形状构建复杂图表、设计直观的幻灯片内容，并在 Word 中撰写清晰的文稿。

为一份 5 页的季度业务回顾列大纲

AutoSave

Q3 Review.pptx

搜索

开始插入设计切换动画审阅

批注共享

新建幻灯片版式BIU排列设计灵感加载项Grok

1

季度回顾10 月 · FY26

Q3 业务回顾

营收、利润率、商机管道——以及我们下一步的投资方向

01营收02利润率03商机管道04展望

起草这份幻灯片

处理任何内容……

第 1 页，共 5 页 · English (US)100%

进一步了解我们的 [Word](https://marketplace.microsoft.com/en-us/product/office/WA200011055?tab=Overview)、[PowerPoint](https://marketplace.microsoft.com/en-us/product/office/WA200011057?tab=Overview) 和 [Excel](https://marketplace.microsoft.com/en-us/product/office/WA200011056?tab=Overview) 插件。

## [定价](#pricing)

与其他领先模型相比，Grok 4.5 的使用成本极具竞争力。Grok 4.5 定价为每百万输入 token 2 美元、每百万输出 token 6 美元。该模型的 token 效率还约为同类领先模型的 2 倍，以不到一半的步骤数解决任务。总体而言，Grok 4.5 交付了每单位时间和成本下最高的智能。

## [开始使用](#getting-started)

Grok 4.5 今天起在 Grok Build、所有套餐的 Cursor 以及 [SpaceXAI 控制台](https://console.x.ai/)中可用。只需获取一个 API 密钥，用几行代码即可开始：

复制

```
curl -s https://api.x.ai/v1/responses \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model
```
