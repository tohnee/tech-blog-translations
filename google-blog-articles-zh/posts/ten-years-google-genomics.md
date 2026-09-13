---
title: "Google 基因组学研究十年"
title_en: "10 years of genomics research at Google"
source: https://blog.google/innovation-and-ai/technology/research/ten-years-google-genomics/
site: google-blog
date: 2025-10-16
crawled: 2026-09-13
translated: 2026-09-13
---

# Google 基因组学研究十年

> 原文：[10 years of genomics research at Google](https://blog.google/innovation-and-ai/technology/research/ten-years-google-genomics/) · Google

*最后更新：2025 年 10 月 24 日*

几十年来，科学家一直在努力理解基因组——地球上所有生命的操作手册。这本手册以无穷的变异形式存在于每个生物体的 DNA 之中，影响着从生物体的发育到更广泛的生命规则的方方面面，然而它却是生物学中人们了解最少的领域之一。

我们为遗传学家开发技术、以研究数十亿人类、植物和动物基因组的旅程始于 10 年前。Google 的一个小型研究团队决定将深度学习应用于各种基因组测序挑战，使其更快、更准确、更高效。这项始于 2015 年的基础研究工作，如今已发展为一项全球性计划，包括与全球的科学家和机构合作，以加速科学发现、推进医疗保健并保护生物多样性。

这项工作已经展现出造福人类健康的可观突破——包括今天[宣布的 DeepSomatic](https://blog.google/technology/research/deepsomatic-an-open-source-ai-model-is-speeding-up-genetic-analysis-for-cancer-research/)，一种能更准确地识别癌症变异的新工具。但我们的工作尚未完成，更多工具还在路上。今天，让我们稍作停留，回顾我们在基因组学头 10 年中借助 AI 实现的一些关键里程碑和突破性工具。

> 读懂基因组

实践证明，AI 在攻克基因组学最根本的挑战——准确而高效地读取生命密码——方面功不可没。

- **2015 年 - 研究起步：** Google 首次将前沿深度学习技术应用于基因组学领域，赢得了 2016 年 PrecisionFDA Truth Challenge，开启了该领域长达十年的探索。
- **2018 年 - 准确识别遗传变异：** 我们公开发布了当时最先进的变异检测工具 [DeepVariant](https://www.nature.com/articles/nbt.4235)。这款基于深度学习的工具能够准确识别 DNA 测序数据中的遗传变异，如今已被广泛使用，直接促成了首个真正完整的人类基因组序列等里程碑式成果。
- **2022 年 - 更准确的基因测序：** 我们推出了 [DeepConsensus](https://www.nature.com/articles/s41587-022-01435-7)，这是一个可提高长读长测序数据准确性、减少原始基因组数据错误的深度学习模型。此后，研究人员获得的最高质量序列读段的通量提升了 250%。
- **2022 年 - 完成人类基因组**：[NIH 端粒到端粒（T2T）联盟](https://sites.google.com/corp/ucsc.edu/t2tworkinggroup)破译了人类基因组最后 8% 的序列，生成了首个完整[人类参考基因组](https://www.science.org/doi/10.1126/science.abj6987)，填补了我们遗传蓝图中最后缺失的片段，为世界各地的研究人员打造了一份资源。这项工作使用 DeepVariant 的一种特殊应用来打磨组装后的序列。
- **2023 年 - 人类泛基因组参考序列：** 工程师们使用 DeepConsensus 和 DeepVariant，帮助创建了[人类泛基因组的首个草图](https://www.nature.com/articles/s41586-023-05896-x)。这个新的参考基因组包含来自多个不同血统个体的序列，是确保所有人都能受益于基因组医学的关键一步。
- **2025 年 - 更精确的基因组组装**：我们推出了 [DeepPolisher](https://research.google/blog/highly-accurate-genome-polishing-with-deeppolisher-enhancing-the-foundation-of-genomic-research/)，这是一个深度学习工具，可提高人类、动物和植物基因组组装的准确性，改善研究中使用的参考基因组的质量。

> 理解基因组

在能够准确读取基因组之后，下一个挑战是更全面地理解序列的特定部分编码了什么功能，并识别哪些微小变异会导致疾病。

- **2021 年 - 预测基因表达**：[Enformer](https://www.nature.com/articles/s41592-021-01252-x) 发布——这是一个从基因组序列预测基因表达的模型，旨在更好地理解非编码遗传变异并设计细胞类型特异的 DNA 序列，推进对基础生物学的理解。
- **2023 年 - 评估编码遗传变异的致病潜力：** 我们开发了 [AlphaMissense](https://www.science.org/doi/10.1126/science.adg7492)，这个模型可以预测基因组蛋白编码区中的哪些遗传变异更可能导致疾病，为遗传学家提供了强大的新工具。
- **2025 年 - 非编码变异效应的统一模型**：我们的新 AI 模型 [AlphaGenome](https://deepmind.google/discover/blog/alphagenome-ai-for-better-understanding-the-genome/) 可以预测单个 DNA 变异如何影响生物过程，帮助研究人员理解基因组的"暗物质"。

![明亮的蓝色 3D 渲染 DNA 双螺旋居中呈现，背景是模糊、若隐若现的 DNA 链以及粉色与蓝色光的渐变。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/AlphaGenoma-OG-1200-630-000000.width-1200.format-webp.webp)

> 为人类与地球加速科学发现

我们的 AI 工具正在帮助研究人员攻克重大生物学难题，带来健康领域的突破，并助力濒危物种的保护工作。

- **2021 年 - 眼部疾病表型分析：** 我们在[视网膜图像与基因组学的大规模生物银行数据上训练 AI](https://www.cell.com/ajhg/fulltext/S0002-9297(21)00188-9) 的方法，发现了眼病新的遗传关联，为青光眼等疾病的药物开发确定了潜在靶点。
- **2022 年 - 破纪录的遗传诊断：** [由斯坦福大学医学院牵头的一项合作](https://med.stanford.edu/news/all-news/2022/01/dna-sequencing-technique.html)创下了最快遗传诊断的吉尼斯世界纪录，利用 Google 的 AI 在不到 8 小时内识别出致病变异。
- **2023 年 - 为保护而测序 DNA：** Google 为一项测序所有真核生命的宏大计划提供技术与算力支持。我们的合作已经助力了 17 个极度濒危物种的基因组项目，展现了 AI 在保护工作中的作用。
- **2024 年 - 用 AI 解析常见健康指标：** Google 开发的 AI 方法利用常见的医学检查来发现我们的基因如何影响心肺疾病。通过更好地理解遗传学如何影响人体的基本过程，我们的方法[改善了疾病预测与遗传发现](https://www.nature.com/articles/s41588-024-01831-6)。
- **2025 年 - 识别癌细胞中的变异**：我们开发了一个 AI 模型 [DeepSomatic](https://research.google/blog/using-ai-to-identify-genetic-variants-in-tumors-with-deepsomatic)，能够更准确地识别与癌症相关的基因突变。在多种癌症类型上测试时，我们的方法识别出了以往最先进工具遗漏的关键变异，有望改善癌症的诊断与治疗。

![发光的蓝色与紫色数字神经网络插图，黑色背景上呈现相互连接的类神经元细胞。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/DeepSomatic_Hero.width-1200.format-webp.webp)

过去十年基因组学的进步，归根结底源于我们打造"创新飞轮"的方法：我们被一个真实世界的问题驱动——比如理解人类基因组以提供更好的医疗保健——去开展基础计算机科学研究。这项研究催生了解决方案，而这些方案又让我们能够发掘更多值得解决的有趣问题，例如把这项工作应用于保护地球物种和维护生物多样性。

经过十年推动突破性发现从研究走向现实、推进遗传学发展之后，如今已有一个卓越的研究社区在使用这套强大的科学工具开展协作，以改善这个星球上每一个生命的生活。

我们迫不及待想看到，未来 10 年的共同研究将带来什么。
