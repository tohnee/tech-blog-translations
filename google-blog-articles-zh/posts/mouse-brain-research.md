---
title: "小鼠大脑研究正在帮助我们更好地理解人类心智"
title_en: "Mouse brain research is helping us better understand human minds"
source: https://blog.google/innovation-and-ai/technology/research/mouse-brain-research/
site: google-blog
date: 2024-07-08
crawled: 2026-09-13
translated: 2026-09-13
---

# 小鼠大脑研究正在帮助我们更好地理解人类心智

> 原文：[Mouse brain research is helping us better understand human minds](https://blog.google/innovation-and-ai/technology/research/mouse-brain-research/) · Google

Google 的研究人员最近公布了[迄今最大、最精细的人脑图谱](https://blog.google/technology/research/google-ai-research-new-images-human-brain/)。它描绘的只是 1 立方毫米的脑组织——大约半粒米大小——但分辨率高到足以显示单个神经元及其相互连接，并且需要 1.4 *PB*（petabytes）的数据来编码。

虽然这只是大脑极小的一小片，这张图谱却带来了多项令人惊讶的发现。"举个例子，我们发现有些'导线'会把自己缠绕成巨大的结，"Google 研究科学家 Viren Jain 谈到这些神经元时说，"我们完全不知道为什么——此前从未有人见过这种现象。"

如今，Viren 和他的团队把目光转向了小鼠大脑。这自有其道理——这些哺乳动物可能有助于解开自人类诞生以来一直困扰我们的心智之谜。比如这些谜题：记忆是如何存储和提取的？我们如何识别物体和面孔？为什么我们需要那么多睡眠？还有，在阿尔茨海默病和其他脑部疾病中，究竟是哪里出了问题？

"我们没有这些问题的答案，原因之一是我们还没有研究大脑所需的足够数据，"Viren 说。

人脑约有 860 亿个神经元，由超过 100 万亿个突触相互连接，让你能够思考、感受、运动并与世界互动。通过绘制这些神经连接的图谱——即所谓的"连接组"（connectome）——我们可以解锁关于大脑如何运作、以及为何有时失灵的新认识。

要在突触层面构建精细的图谱，研究人员需要以纳米级分辨率对大脑成像，并处理海量数据。这是一项重大的技术挑战，需要在成像技术、AI 算法和数据管理工具上持续创新。正因如此，10 年前 Google Research 组建了它的[连接组学团队（Connectomics team）](https://research.google/teams/connectomics/)。

过去十年，该团队开发了能[更高效地处理、分析和共享数据](https://sites.research.google/neural-mapping/)的技术，让研究人员在理解大脑的进展上大幅加速。例如，他们提出了[洪泛填充网络（flood-filling networks）](https://research.google/blog/improving-connectomics-by-an-order-of-magnitude/)，用机器学习自动追踪神经元穿越各层组织的路径，取代了过去在脑部图像上人工为细胞上色的繁琐工作。在此基础上，他们的 [SegCLR 算法](https://research.google/blog/multi-layered-mapping-of-brain-tissue-via-segmentation-guided-contrastive-learning/)能在这些网络中自动识别细胞的不同部分和细胞类型。他们还创建了 [TensorStore](https://research.google/blog/tensorstore-for-high-performance-scalable-array-storage/) 和 [Neuroglancer](https://github.com/google/neuroglancer/) 等软件，帮助存储、处理和可视化大型多维图像与体数据。

尽管如此，绘制完整的人脑连接组将需要采集和分析多达 1 ZB（zettabyte，十亿 TB）的数据，这超出了现有技术的能力。"如果现在就要绘制整个人脑，可能需要数十亿美元和数百年的时间，"Viren 说。

因此，研究人员转而专注于两个方向：要么绘制小型动物大脑的大部分，要么绘制大型动物脑组织的一小块。2020 年，连接组学团队绘制了[果蝇大脑的一半](https://research.google/blog/releasing-the-drosophila-hemibrain-connectome-the-largest-synapse-resolution-map-of-brain-connectivity/)，揭示了 25,000 个神经元之间的连接。通过与该领域研究人员的合作，他们还创建了[斑胸草雀](https://www.nature.com/articles/s41592-018-0049-4)和[斑马鱼幼体](https://www.nature.com/articles/s41592-022-01621-0)部分大脑的连接组。而在今年 5 月，前文提到的 [1 立方毫米人脑组织图谱发表在《科学》（Science）上](https://www.science.org/doi/10.1126/science.adk4858)。

世界各地已有数千名研究人员使用了这些项目产生的数据集，由此产出了数百项已发表的发现。

研究人员为一小块人脑组织中几乎每一个神经元及其连接构建了 3D 图像。上方的图像显示兴奋性神经元，下方的图像显示抑制性神经元。

![上方图像显示一块人脑组织中所有兴奋性神经元以黄色点亮，下方图像显示同一样本中所有抑制性神经元以蓝色点亮。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/3D_neuron_and_connection_stills.width-1200.format-webp.webp)

现在，连接组学团队正在与哈佛大学、普林斯顿大学等地的合作伙伴合作，绘制小鼠的海马体（hippocampus）——大脑中负责编码记忆、注意力和空间导航的部分，约占小鼠整个大脑的 2-3%。

在没有时间或技术绘制整个人脑的情况下，分析小鼠连接组是退而求其次的最佳选择。它足够小，在技术上可行，又可能为我们自己的心智带来相关洞见。"当你在电子显微镜下观察小鼠大脑时，它看上去与人类大脑一模一样。事实上，它就是一个人脑的微缩版本，"哈佛大学分子与细胞生物学教授 Jeff W. Lichtman 说。这正是科学家们频繁使用小鼠来研究人类大脑疾病的原因。

小鼠只是连接组学的最新前沿；数十年来，神经科学家一直在努力绘制越来越大、越来越复杂的大脑。第一个连接组是一条蠕虫的大脑——它于 1986 年发表，耗费了 16 年才完成绘制。

跨越数十年的连接组学研究。

![一张展示不同连接组学项目对照表的图示，顶端是一条有 302 个神经元、需要 TB 级存储的蛔虫（roundworm），于 20 世纪 70 年代完成。表格向下依次为果蝇、人脑碎片、小鼠海马体、小鼠，直至完整人脑，规模逐级增大。人脑的神经元数量急剧增加到 100,000,000,000 个，将需要数百 EB 的存储空间。](https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/Brain_in-line_2.gif)

尽管小鼠大脑比人脑小 1,000 倍，绘制它的图谱仍然是一项巨大的技术挑战。一个纳米级分辨率的小鼠大脑连接组数据集可能是有史以来最大的生物学数据集，估计约为 20,000-30,000 TB。

"所以不仅是采集数据，光是存储并准确处理所有这些数据就是一大挑战，"Viren 说，"但这也正是我们对这个领域独有的贡献：开发把精度推向最先进水平的工具，然后真正把它们大规模应用于越来越大的数据集。"

如果成功，连接组学团队的小鼠大脑项目将是科学家首次绘制哺乳动物海马体的一部分。这也将是研究人员有史以来尝试绘制的最大的脑组织区块。

"基础研究会创造非凡的价值，"Viren 说，"让我感到兴奋的是，终有一天，我们将精确理解我们如何形成记忆、精神障碍或疾病背后的机制是什么。但要做到这一点，我们必须打造这个技术闭环——就在二十年前，这还是不可想象的事情。"
