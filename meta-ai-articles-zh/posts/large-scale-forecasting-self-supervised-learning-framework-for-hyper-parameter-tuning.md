---
title: "大规模预测：用于超参数调优的自监督学习框架"
title_en: "Large-scale forecasting: Self-supervised learning framework for hyperparameter tuning"
date: 2021-04-05
source: https://ai.facebook.com/blog/large-scale-forecasting-self-supervised-learning-framework-for-hyper-parameter-tuning
crawled: 2026-09-22
translated: 2026-09-22
---

# 大规模预测：用于超参数调优的自监督学习框架

> 原文：[Large-scale forecasting: Self-supervised learning framework for hyperparameter tuning](https://ai.facebook.com/blog/large-scale-forecasting-self-supervised-learning-framework-for-hyper-parameter-tuning) · Meta AI（Wayback 存档）

**这项研究是什么：**一个用于模型选择（SSL-MS）与超参数调优（SSL-HPT）的新自监督学习框架，能以更少的计算时间与资源提供准确预测。与基线搜索类算法相比，SSL-HPT 算法估计超参数的速度快 6-20 倍，同时在多种应用中产生准确度相当的预测结果。在时间序列分析（用于发现趋势或预测未来值）中，超参数的细微差异可能导致同一模型产生截然不同的预测结果，因此选择最优超参数值非常重要。大多数现有超参数调优方法——如网格搜索、随机搜索和贝叶斯最优搜索——都基于一个关键组件：搜索。正因如此，它们计算开销高昂，无法用于快速、可扩展的时间序列超参数调优。我们的框架 SSL-HPT 以时间序列特征为输入，在不牺牲准确率的前提下用更短时间产出最优超参数。

**工作原理：**我们为预测领域中的两个主要任务开发了该自监督学习框架：SSL-MS 与 SSL-HPT。

SSL-MS：用于模型选择的自监督学习框架包含三步，如下所述：

1. 离线训练数据准备：我们获得 (a) 每条时间序列的时间序列特征，以及 (b) 通过离线穷举式超参数调优得到的每条时间序列表现最佳的模型。
2. 离线训练：用第 1 步的数据训练一个分类器（自监督学习器），其中输入特征（预测变量）是时间序列特征，标签是第 1 步得到的表现最佳的模型。
3. 在线模型预测：在我们的在线服务中，对新时间序列数据提取特征，再用预训练分类器（如随机森林模型）做推理。

（SSL-MS 的工作流程。）

SSL-HPT：SSL-MS 的工作流程可以自然地扩展为 SSL-HPT。如下图所示，给定一个模型，在预定义参数空间内的所有超参数设置都会针对每条时间序列进行探索，最有希望的那个被选为输出 𝑌。输入 𝑋 使用的时间序列特征与 SSL-MS 中相同。自监督学习器一旦训练完成，我们就能直接预测超参数，并为任意新时间序列数据生成预测结果。

（SSL-HPT 的工作流程。）

（基于 Facebook 基础设施数据与开源数据的实验结果。）我们在内部与外部数据集上对算法做了实证评估，得到了相似结论：SSL 框架可以显著提升模型选择与超参数调优的效率，在预测准确率相当的情况下把运行时间缩短 6-20 倍。

**为什么重要：**预测是我们在 Facebook 从事的核心数据科学与机器学习任务之一，因此对海量时间序列数据提供快速、可靠、准确的预测结果对我们的业务十分重要。该框架的应用包括容量规划与管理、需求预测、能源预测和异常检测。计算技术的快速进步使企业能够追踪大量时间序列数据集，因此定期预测数百万条时间序列的需求日益普遍。为大量时间序列获得快速而准确的预测依然充满挑战。我们的 SSL 框架提供了一种高效解决方案：以低计算成本、短运行时间提供高质量预测结果。该方法独立于具体的预测模型与算法，因此我们仍能享受各种预测技术各自的优势，比如 Prophet 模型的可解释性。初步分析表明，该框架还可以扩展到模型推荐，并增强我们自研 AX 库中的贝叶斯优化算法。

阅读完整论文：Self-supervised learning for fast and scalable time series hyperparameter tuning

这是与普渡大学统计学博士生 Peiyi Zhang、Yang Yu、Nikolay Pavlovich Laptev、Caner Komurlu、Peng Gao 和 Ginger Holt 的合作成果。我们还要感谢 Alessandro Panella 和 Dario Benavides 的宝贵反馈。

**作者**

- Xiaodong Jiang，研究数据科学家
