---
title: "开源 fastText 的超参数自动调优"
title_en: "Open-sourcing hyperparameter autotuning for fastText"
date: 2019-03-15
source: http://ai.facebook.com/blog/fasttext-blog-post-open-source-in-brief
crawled: 2026-09-22
translated: 2026-09-22
---

# 开源 fastText 的超参数自动调优

> 原文：[Open-sourcing hyperparameter autotuning for fastText](http://ai.facebook.com/blog/fasttext-blog-post-open-source-in-brief) · Meta AI（Wayback 存档）

**新内容：**超参数自动调优——我们 fastText 库的新功能。该功能自动为你的数据集确定最佳超参数，以构建高效的文本分类器。使用自动调优时，研究者输入训练数据、验证集与时间约束，fastText 随后在限定时间内搜索能在验证集上取得最佳性能的超参数。研究者还可以选择约束最终模型的尺寸，此时 fastText 会使用压缩技术缩减模型体积。我们探索各种超参数的策略受 Nevergrad 等现有工具启发，但通过利用模型的特定结构为 fastText 量身定制。我们的自动调优通过采样探索超参数：起初在一个大域中采样，随着时间推移逐渐收缩到已发现的最佳组合周围。

**为什么重要：**与大多数机器学习模型一样，fastText 有许多超参数，包括学习率、模型维度与训练轮数。这些因素对最终模型的性能都有很强影响，而最优值往往随数据集或任务而异。即便对专家用户而言，手动搜索最佳超参数也可能令人望而生畏且耗时。我们的新功能让这一任务实现自动化。在许多场景下（如在设备或云端部署模型时），保持较小的内存占用也很重要。fastText 还允许研究者轻松为其数据构建尺寸受限的文本分类器。

**了解更多：**关于 fastText 自动调优的更多信息。

**用途：**用一行命令构建高效文本分类器。研究者现在可以为各种任务构建内存高效的分类器，包括情感分析、语言识别、垃圾内容检测、标签预测与主题分类。

**在 GitHub 获取：**带超参数自动调优的 fastText

Onur Çelebi，研究工程师；Edouard Grave，研究科学家
