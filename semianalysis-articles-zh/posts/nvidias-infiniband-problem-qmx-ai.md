---
title: "Nvidia 的 InfiniBand 难题——Spectrum-X AI Fabric、Tomahawk-5、Jericho-3AI、Quantum-2"
title_en: "Nvidia's InfiniBand Problem - Spectrum-X AI Fabric, Tomahawk-5, Jericho-3AI, Quantum-2"
subtitle: "团队与技术路线相争，这次转向能否撼动 Broadcom 的统治地位"
date: 2023-05-28
source: https://newsletter.semianalysis.com/p/nvidias-infiniband-problem-qmx-ai
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# Nvidia 的 InfiniBand 难题——Spectrum-X AI Fabric、Tomahawk-5、Jericho-3AI、Quantum-2

> 原文：[Nvidia's InfiniBand Problem - Spectrum-X AI Fabric, Tomahawk-5, Jericho-3AI, Quantum-2](https://newsletter.semianalysis.com/p/nvidias-infiniband-problem-qmx-ai) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**团队与技术路线相争，这次转向能否撼动 Broadcom 的统治地位**

在这场建设 AI 基础设施的淘金热中，GPU 就是铲子和镐头。随着 Nvidia 上周创纪录的财报出炉，半导体市场一路飙升。市场错误地拉高了另一些 AI 敞口小得多的公司，试图沾一沾淘金热的光。需要明确的是，AI 基础设施支出中占比最大的是 AI 加速器。而金额份额变化第二大的则是网络。摸清各家超大规模云厂商分别在使用什么网络设备极其重要。

从外部看，Nvidia 显然拥有 21 世纪最有远见的 CEO——黄仁勋（Jensen Huang），以及围绕加速计算和 AI 的大一统宏大战略。几年前，Nvidia 收购了领先的网络公司 Mellanox，以推进这一愿景。尽管目标清晰，但在网络技术栈内部，存在着极度的复杂性。正因如此，Nvidia 内部正激战正酣。Nvidia 的 InfiniBand 网络技术栈存在一个根本性问题。
