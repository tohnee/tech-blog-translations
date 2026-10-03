---
title: "我们推出 SynthID Bio：将水印技术引入合成生物学"
title_en: "We’re introducing SynthID Bio, bringing our watermarking technology to synthetic biology."
source: https://blog.google/innovation-and-ai/models-and-research/google-deepmind/synthid-bio/
site: deepmind
date: 2026-09-30
crawled: 2026-10-03
translated: 2026-10-03
---

# 我们推出 SynthID Bio：将水印技术引入合成生物学

> 原文：[We’re introducing SynthID Bio, bringing our watermarking technology to synthetic biology.](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/synthid-bio/) · Google DeepMind

今天，我们推出 SynthID Bio——一项在保持生物功能的前提下，为 AI 设计的蛋白质添加水印的新技术。

SynthID Bio 将一种无法察觉、可验证的水印直接嵌入生物设计之中，例如 AI 生成的蛋白质序列和预测的 3D 结构。

在针对多个目标蛋白的实验室测试中，我们的带水印设计在性能和自然多样性上均成功比肩未加水印的版本。由此形成了一个至关重要的溯源层，可强化生物安全，并维护开放科学数据库的完整性。

你可以在 [Google DeepMind 网站](https://deepmind.google/blog/introducing-synthid-bio/)上阅读完整博文与研究。

![一张分子蛋白质结构的 3D 可视化图，高亮显示了一段带水印的序列。主体背景为棕色的分子表面表示，前景中有两个螺旋结构，其带状骨架沿轴向以橙色和蓝色渐变进行颜色编码。左上角的图例标示「Watermark Signal（水印信号）」，从代表「Strong（强）」的蓝色渐变到代表「Weak（弱）」的橙色。右上角写有亲和常数 $K_D = 0.344,\mu\text{M}$。底部是一条带颜色编码的氨基酸序列条，标注为「Watermarked Sequence（带水印序列）」，并带有从 6 到 56.1 的残基索引标记。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/watermarked_VEGF-A.width-100.format-webp.webp)

*我们带水印的 VEGF-A 蛋白结合体的预测结构可视化，每个氨基酸的颜色表示其水印信号。*

![此处为描述该图的替代文本：一张小提琴图，比较了三种目标蛋白——PD-L1、SC2RBD 和 VEGF-A——在未加水印（橙色）与加水印（蓝色）两种条件下的结合亲和力（$K\_d$）值。纵轴表示结合亲和力，采用从 $10^{-5}$ 到 $10^{-10}$ 的对数刻度。在全部三种目标蛋白中，未加水印与加水印数据集的结合亲和力分布几乎完全相同。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Binding_affinity.width-100.format-webp.webp)

*以 KD 衡量的结合亲和力，比较三个目标上未加水印与加水印的蛋白质设计。数值越低表示结合能力越强。*

![在 7PPA 上，我们展示了 AF3 预测结构（左）、真实结构（中）和带水印结构（右）。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/7PPA_structures_v2.width-100.format-webp.webp)

*在 7PPA 上，我们展示了 AF3 预测结构（左）、真实结构（中）和带水印结构（右）。*
