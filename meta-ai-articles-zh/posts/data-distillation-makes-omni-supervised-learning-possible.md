---
title: "数据蒸馏让全监督学习成为可能"
title_en: "Data distillation makes omni-supervised learning possible"
date: 2018-09-24
source: https://ai.meta.com/blog/data-distillation-makes-omni-supervised-learning-possible
crawled: 2026-09-22
translated: 2026-09-22
---

# 数据蒸馏让全监督学习成为可能

> 原文：[Data distillation makes omni-supervised learning possible](https://ai.meta.com/blog/data-distillation-makes-omni-supervised-learning-possible) · Meta AI（Wayback 存档）

2018 年 9 月 24 日

## 这项研究是什么

对全监督学习（omni-supervised learning）的一项研究。这是一种半监督学习，组合使用为训练目的而人工标注的数据（监督数据）与无标注数据（无监督数据），并有潜力超越最先进的全监督方法。所提出的方法使用数据蒸馏（data distillation）这一简单的全监督手段来训练 AI 模型。

## 它是如何工作的

数据蒸馏基于自训练这一经典思想，即在无标注数据上做预测并用这些预测更新模型。类似地，模型用预测来填补自身训练数据中的空白。研究者设计了一个四步流程：在大量监督数据上训练模型；将训练好的模型应用于无监督数据；为该无监督数据生成标签；最后，同时纳入监督数据和（此时已自动标注的）无监督数据，回过头来重新训练模型。他们发现，用数据蒸馏训练的模型优于仅用监督数据训练的模型。

## 为什么它重要

这些实验证明，全监督学习有可能超越大规模监督学习所取得的结果。将较传统的精选训练数据与大量无标注数据相结合是一种可行的策略，并开启了从真实世界来源汲取信息、加速 AI 系统创建的可能性。

**阅读完整论文：** Data Distillation: Towards Omni-Supervised Learning
