---
title: "AI 如何推动生物声学科学的发展以拯救濒危物种"
title_en: "How AI is helping advance the science of bioacoustics to save endangered species"
source: https://deepmind.google/blog/how-ai-is-helping-advance-the-science-of-bioacoustics-to-save-endangered-species/
site: deepmind
date: 2025-08-07
crawled: 2026-09-13
translated: 2026-09-13
---

# AI 如何推动生物声学科学的发展以拯救濒危物种

> 原文：[How AI is helping advance the science of bioacoustics to save endangered species](https://deepmind.google/blog/how-ai-is-helping-advance-the-science-of-bioacoustics-to-save-endangered-species/) · Google DeepMind

我们的新 Perch 模型帮助保护工作者更快地分析音频，保护从夏威夷管舌雀到珊瑚礁的濒危物种。

科学家保护地球野生生态系统健康的方式之一，是利用麦克风（或水下听音器）收集大量充满鸟、蛙、昆虫、鲸、鱼等鸣声的音频。这些录音能告诉我们某一区域内有哪些动物，以及关于该生态系统健康状况的其他线索。然而，解读如此庞大的数据仍是一项浩大的工程。

今天，我们发布 [Perch](http://arxiv.org/abs/2508.04665) 的更新版——我们为帮助保护工作者分析生物声学数据而设计的 AI 模型。新模型的开箱即用鸟类物种预测比上一版达到更高的业界领先水平。它能更好地适应新环境，尤其是珊瑚礁这样的水下环境。它的训练数据覆盖了更广的动物范围，包括哺乳动物、两栖动物和人为噪声——数据总量几乎翻倍，来自 [Xeno-Canto](https://xeno-canto.org/) 和 [iNaturalist](https://neurips.cc/virtual/2024/poster/97701) 等公开来源。它能在数千甚至数百万小时的音频数据中理清复杂的声学场景。而且它用途多样，能帮助回答各种不同的问题，从「有多少幼崽出生了」到「给定区域内有多少只个体动物」。

为了帮助科学家保护地球的生态系统，我们将以开放模型的形式发布这一新版 Perch，并在 [Kaggle](https://www.kaggle.com/models/google/bird-vocalization-classifier/tensorFlow2/perch_v2) 上提供。

![由十幅照片组成的拼贴画，展示生物声学监测的多样生态系统与物种，包括红眼树蛙、座头鲸、长臂猿、色彩斑斓的珊瑚礁、一群狐獴、斑海豹、倒挂的蝙蝠、蚊子、海象，以及珊瑚礁的航拍图。](https://lh3.googleusercontent.com/kJ2OlrhiAEdXxydXx9yt4fNNCDp1jsPTaUv321UUB0D-tqcAjZabF_Zxkki1faXfUD1tRKS5fkEVgfWIITLPk7qX-T8AJoew7A9WHsqpL7y_Y83kQA=w1440)

Perch 不仅能识别鸟类物种的声音。我们的新模型训练数据覆盖了更广的动物范围，包括哺乳动物、两栖动物和人为噪声。

## 成功案例：野外的 Perch

自 2023 年首次发布以来，Perch 初版已被[下载超过 25 万次](https://www.kaggle.com/models/google/bird-vocalization-classifier)，其开放可用的方案如今已深度融入一线生物学家的工具之中。例如，Perch 的向量搜索库现在是康奈尔大学广泛使用的 [BirdNet Analyzer](https://github.com/birdnet-team/BirdNET-Analyzer) 的一部分。

此外，Perch 正在帮助 BirdLife Australia 和澳大利亚声学观测站为多个独特的澳洲物种构建分类器。例如，我们的工具促成了[发现](https://www.theguardian.com/environment/2025/feb/12/plains-wanderers-spotted-in-melbournes-west-for-first-time-in-30-years-with-help-of-ai)了一个难以捕捉的领鹑（Plains Wanderer）新种群。

> 这是一项令人惊叹的发现——这样的声学监测将帮助塑造许多濒危鸟类物种的未来。

Paul Roe

澳大利亚詹姆斯库克大学研究院长

最近的研究还发现，早期版本的 Perch 可用于[识别鸟类个体](https://www.sciencedirect.com/science/article/pii/S1574954125003395)和[追踪鸟类数量](https://www.sciencedirect.com/science/article/pii/S1470160X24013876)，有望减少为监测种群而进行捕捉-放归研究的需要。

最后，夏威夷大学 [LOHE 生物声学实验室](https://lohelab.org/)的生物学家已用它来监测和保护管舌雀种群——这些鸟类对[夏威夷神话](https://www.mauiforestbirds.org/cultural-significance)意义重大，并因非本地蚊子传播的禽疟威胁而濒临灭绝。Perch 帮助 LOHE 实验室以比以往方法快近 50 倍的速度找到管舌雀的鸣声，使他们能在更大范围内监测更多管舌雀物种。我们期待新模型将进一步加速这些工作。

![](https://lh3.googleusercontent.com/ItTZW3LgJsjeCWxuC3GSzzAfqs0jXrDkaeEWrgQt7efPUBlVRd495QZmHHOW_1zhDqzkT6O0hnE7aDt9nvOT18_zWCy2lHym6w84PlLv_WWK3bYZLLA=w1440-h810-n-nu)

## 理清地球的歌单

Perch 模型可以预测录音中出现了哪些物种，但这只是故事的一部分：我们还提供[工具](https://github.com/google-research/perch-hoplite)，让科学家能够从单个样本出发快速构建新分类器，监测训练数据稀缺的物种或非常特定的声音（如幼鸟鸣叫）。给定一个声音样本，利用 Perch 进行向量搜索就能在数据集中找出最相似的声音。然后，当地专家可以把搜索结果标记为相关或不相关，以训练分类器。

向量搜索与主动学习结合强嵌入模型的这一组合被称为[敏捷建模（agile modeling）](https://openaccess.thecvf.com/content/ICCV2023/papers/Stretcu_Agile_Modeling_From_Concept_to_Classifier_in_Minutes_ICCV_2023_paper.pdf)***。***我们最近的论文——[「The Search for Squawk: Agile Modeling in Bioacoustics」（寻找鸣叫：生物声学中的敏捷建模）](https://arxiv.org/abs/2505.03071)——表明这一方法在鸟类和珊瑚礁上都行之有效，可以在一小时内构建出高质量分类器。

## 展望未来：生物声学的前景

我们的模型与方法合力帮助保护工作发挥最大影响，为有意义的实地工作留出更多时间和资源。从夏威夷的森林到海洋的礁盘，Perch 项目展示了当我们将技术专长应用于世界最紧迫的挑战时所能产生的深远影响。每构建一个分类器、每分析一小时数据，都让我们离一个目标更近一步——让我们星球的原声带成为丰富而蓬勃的生物多样性之歌。

**了解更多**

[从 Kaggle Models 下载新的 Perch 模型](https://www.kaggle.com/models/google/bird-vocalization-classifier/tensorFlow2/perch_v2)[在 arXiv 上阅读我们的论文](http://arxiv.org/abs/2508.04665)[阅读我们关于生物声学敏捷建模的论文](https://arxiv.org/abs/2505.03071)[探索我们的 GitHub 仓库](https://github.com/google-research/perch-hoplite)

**致谢**

本研究由 Perch 团队开发：Bart van Merriënboer、Jenny Hamer、Vincent Dumoulin、Lauren Harrell 和 Tom Denton，以及来自 Google Research 的 Otilia Stretcu。我们还要感谢夏威夷大学的合作者 Amanda Navine 和 Pat Hart，以及康奈尔鸟类学实验室的 Holger Klinck、Stefan Kahl 和 BirdNet 团队。还要感谢所有朋友与合作伙伴——如果我们还有再多一千字的篇幅，一定会在这篇博文中一一致谢。
