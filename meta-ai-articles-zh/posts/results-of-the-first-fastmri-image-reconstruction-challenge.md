---
title: "首届 fastMRI 图像重建挑战赛的结果"
title_en: "Results of the first fastMRI image reconstruction challenge"
date: 2019-03-15
source: https://ai.facebook.com/blog/results-of-the-first-fastmri-image-reconstruction-challenge
crawled: 2026-09-22
translated: 2026-09-22
---

# 首届 fastMRI 图像重建挑战赛的结果

> 原文：[Results of the first fastMRI image reconstruction challenge](https://ai.facebook.com/blog/results-of-the-first-fastmri-image-reconstruction-challenge) · Meta AI（Wayback 存档）

Facebook AI 与纽约大学朗格尼医学中心（NYU Langone Health）创建了 fastMRI 项目，旨在通过 AI 加速 MRI 扫描。fastMRI 通过用 AI 从显著更少的原始数据创建 ground truth 级准确度的图像，力图让扫描比现在快多达十倍，从而改善患者体验，让 MRI 扫描更便宜、更可及。作为该项目的一部分，我们发布了最大的公开去标识原始 MRI 膝关节测量数据集，现在我们高兴地分享首届 fastMRI 图像重建挑战赛的结果。

通过这次挑战赛，来自整个 AI 共同体的研究者得以探索新方法并比较结果。共有 34 支队伍参赛，使用了 U-net、可变形卷积网络、循环神经网络等多种模型架构。由阿姆斯特丹大学的 Patrick Putzky（单线圈 4 倍加速）、联合智能影像/约翰霍普金斯大学的 Puyang Wang（多线圈 4 倍）以及飞利浦的 Nicola Pezzotti（多线圈 4 倍和 8 倍）分别领衔的三支队伍被评为表现最强。这些队伍受邀于 12 月 14 日（周六）在温哥华 NeurIPS 大会的 Medical Imaging Meets NeurIPS 研讨会上做展示。

提交的作品首先由结构相似性度量（SSIM）评估，它量化图像结构信息的变化。SSIM 得分最高的前四名再由放射科医师小组就视觉质量进行评判。虽然这一评估有助于了解各方法的相对优势，但这些方法是否具有临床可行性，尚需尚未开展的彻底临床研究来确定。（注意，挑战赛使用的数据集包含临床环境中使用的两种 MRI 序列。）

图中是两个多线圈 4 倍加速挑战赛的提交作品（左、中）及其对应的 ground truth 图像（右）。最左边的图像 SSIM 最高，却被放射科医师排在第三；中间的图像 SSIM 排第四，却被放射科医师排第一。这一差异凸显了依据放射科医师评估来决定胜者的重要性。总体而言，挑战赛中的顶尖模型的 SSIM 得分彼此相差不到小数点后一位。这表明多种方法都会有效，也让我们更加乐观地相信 AI 将能够改进 MRI 扫描。

## 一项以放射科医师需求为核心设计的挑战赛

挑战赛参赛者使用开源的 fastMRI 膝关节数据集训练模型，然后用挑战赛数据集重建膝关节 MRI 以供评估。他们提交的重建结果面向单线圈 4 倍加速赛道，或多线圈 4 倍或 8 倍加速赛道。多线圈赛道与临床更相关，而单线圈赛道为加速扫描这一挑战提供了复杂度较低的入口。需要指出的是，本挑战赛并非临床研究，其结果不应被视为判定哪种方法最具临床可行性。

为确保可复现性并让共同体得以继续在这项工作之上构建，我们鼓励参赛者分享代码，已有若干队伍这样做。Facebook AI 与纽约大学朗格尼医学中心打算将他们为 fastMRI 项目共同开发的许多模型开源。这些图表展示了按 SSIM 衡量的 fastMRI 挑战赛顶尖参赛者的结果。（Facebook AI 与纽约大学朗格尼医学中心未参赛。）更多信息见 https://fastmri.org/leaderboards/challenge。

在 SSIM 得分最高的参赛者确定后，七位专业的肌骨骼亚专科放射科医师从多个维度为前四名打分：对比噪声比、伪影、清晰度、诊断信心和总体图像质量。然后对提交作品排序并平均得分，以确定最强者。注意，这些方法相对于原始 ground truth MRI 的诊断可互换性并未测试。

fastMRI 挑战赛的结果还凸显了放射科医师评审的重要性。当放射科医师评估 SSIM 得分最高的作品时，他们有时更偏爱并非绝对最高分的作品。「放射科医师评审是挑战赛的重要组成部分，因为只有打动放射科医师，才能确保这项技术在最终可用时被广泛采用。正因如此，对于纽约大学朗格尼医学中心与 Facebook AI 的 AI 重建图像，我们也与放射科医师开展了可互换性研究，并计划很快在同行评审期刊上发表结果。」纽约大学朗格尼医学中心放射学系 Louis Marx 讲席教授兼系主任 Michael P. Recht 医学博士说。Recht 将于 12 月 5 日在芝加哥举行的北美放射学会年会上介绍更多细节。

## 迈向用 AI 改进现实世界的 MRI

挑战赛的结果令我们备受鼓舞，我们高兴地看到更广泛的共同体成功参与到该项目中。我们相信，通过开放与协作，我们将更快地向最终目标迈进。计算机视觉其他子领域的研究常常受益于举办此类开放的公共挑战赛，但它们在医学影像领域还不常见。我们希望 fastMRI 倡议将推进 AI 研究、改善潜在救命技术的可及性，并激发该领域更多开放、可复现的研究实践。

## 作者

Tullie Murrell

研究工程师

Nafissa Yakubova

访问研究员

Anuroop Sriram

研究工程经理

Mike Rabbat

研究科学家

Larry Zitnick

研究科学家
