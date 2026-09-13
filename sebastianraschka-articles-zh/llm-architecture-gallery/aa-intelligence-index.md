---
title: "Artificial Analysis 智能指数（Intelligence Index）"
title_en: "Artificial Analysis Intelligence Index"
source: https://sebastianraschka.com/llm-architecture-gallery/aa-intelligence-index/
crawled: 2026-09-06
translated: 2026-09-06
---

# Artificial Analysis 智能指数（Intelligence Index）

> 原文：[Artificial Analysis Intelligence Index](https://sebastianraschka.com/llm-architecture-gallery/aa-intelligence-index/)

画廊卡片上的大多数条目描述的是模型本身，例如注意力类型、层配置或 KV 缓存大小。我加入 [Artificial Analysis](https://artificialanalysis.ai/) 智能指数（Intelligence Index），是为了提供一个独立的性能参考。它回答的是另一个问题：发布的模型在一组共享评测上的得分如何？

卡片用两行来展示这一信息。`Total score` 直接取自对应的 Artificial Analysis 模型页面；`Profile` 则是我对 Agents、Coding、General 和 Scientific Reasoning 四个维度的紧凑诊断视图。

两者之间有一个重要区别。总分（total）是官方的 Intelligence Index；Profile 是本画廊特有的视图，不能用它来反推总分。

[架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
[AA 方法论](https://artificialanalysis.ai/methodology/intelligence-benchmarking)
[AA 评测页面](https://artificialanalysis.ai/evaluations/artificial-analysis-intelligence-index)

来源

<https://artificialanalysis.ai/>

当前方法

Intelligence Index v4.1，一个纯文本英文评测套件

类别权重

Agents 34%、Coding 24%、Scientific Reasoning 24%、General 18%

画廊数据快照

2026-08-29

## 两个条目的含义

`Total score` 是对应 Artificial Analysis 模型页面上展示的 Intelligence Index 总分。如果该页面在独立评测尚未完成时给出的是估计值，画廊也会照实记录这一估计值。

`Profile` 是我为快速对比而添加的第二视图。Agents 和 Coding 采用 Artificial Analysis 对应的分项指数（subindices）；General 综合 AA-LCR、AA-Omniscience 和 IFBench；Scientific 综合 Humanity's Last Exam、GPQA Diamond 和 CritPt。

这让 Profile 适合用来发现各维度成绩不均衡的情况，但这四个数字并不是 Index v4.1 加权所用的四个类别值。例如，画廊对 [DeepSeek V3.2](https://artificialanalysis.ai/models/deepseek-v3-2) 的快照记录了总分 24.7，以及 General 29.7、Scientific 24.2、Coding 34.6、Agents 39.8。把 v4.1 的类别权重套用到这四个 Profile 值上，是得不出 24.7 的。

我保留 Profile，是因为总分相近的两个模型在编程或智能体任务上仍可能表现迥异。它是一种方向性对比，而不是又一个官方的 Artificial Analysis 指数。

![示意图：Artificial Analysis Intelligence Index v4.1 的四个加权能力组汇成一个综合分数](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/aa-intelligence-index-breakdown.svg)

**图 1.** 官方的 Intelligence Index v4.1 给 Agents 分配 34%，Coding 和 Scientific Reasoning 各 24%，General 分配 18%。画廊的 Profile 是一个独立的诊断摘要，不参与这一计算。（原始出处：[Artificial Analysis methodology](https://artificialanalysis.ai/methodology/intelligence-benchmarking)。）

## v4.1 的构成

Artificial Analysis 于 2026 年 6 月推出了 Index v4.1。它是九项评测的加权平均，这些评测分为四个类别：

- **Agents，34%。** GDPval-AA v2 占 20%，τ³-Banking 占 14%。
- **Coding，24%。** Terminal-Bench v2.1 占 16%，SciCode 占 8%。
- **General，18%。** AA-LCR 占 6%。AA-Omniscience 提供一个 8% 的准确率成分和一个 4% 的非幻觉成分。
- **Scientific Reasoning，24%。** Humanity's Last Exam 占 12%，GPQA Diamond 和 CritPt 各占 6%。

v4.0 使用的配方不同：四个类别各占 25%，使用 Terminal-Bench Hard 和 τ²-Bench Telecom，并且包含 IFBench。Artificial Analysis 仍然单独报告 IFBench，但 v4.1 已将其排除在官方总分之外。画廊的 Profile 在 General 诊断中继续包含 IFBench，这也是不要把 Profile 当作总分分解方式的另一个原因。

## 快照日期为什么重要

Artificial Analysis 会同时修订基准测试的构成和模型的成绩。因此，画廊记录了数据抓取的日期。本页当前的快照日期是 2026-08-29。

这一日期在模型对比中很重要。在不同指数版本下收集的分数，可能同时反映了评测套件的变化和模型本身的变化。当找不到对应的模型页面或必需字段缺失时，画廊会显示 `N/A`，而不是用估计值来填补空缺。

## 这个分数能告诉我们什么

我把这个指数当作模型发布的一项宽泛校验。分数差异无法定位是哪个设计选择造成的。训练数据、后训练（post-training）、工具使用、推理设置和测试时计算，都可以与架构一起影响结果。

v4.1 套件聚焦于纯文本英文任务。Artificial Analysis 会单独评测多模态和多语言能力，因此这些能力不包含在这个数字里。Artificial Analysis 还报告说，总指数的 95% 置信区间小于 ±1%，而单项评测的置信区间可能更宽。

因此在架构对比中，我只是把这个指数当作辅助背景信息。要理解一个模型是如何构建的，架构字段和原始技术报告仍然是更好的来源。

## 参考资料

- [Artificial Analysis 智能基准测试方法论](https://artificialanalysis.ai/methodology/intelligence-benchmarking)
- [Artificial Analysis Intelligence Index 评测页面](https://artificialanalysis.ai/evaluations/artificial-analysis-intelligence-index)
- [DeepSeek V3.2 模型页面](https://artificialanalysis.ai/models/deepseek-v3-2)

[返回架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
