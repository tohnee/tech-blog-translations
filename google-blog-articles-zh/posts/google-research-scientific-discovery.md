---
title: "我们如何利用 AI 推动科学研究，创造更大的现实世界效益"
title_en: "How we're using AI to drive scientific research with greater real-world benefit"
source: https://blog.google/innovation-and-ai/technology/research/google-research-scientific-discovery/
site: google-blog
date: 2025-05-08
crawled: 2026-09-13
translated: 2026-09-13
---

# 我们如何利用 AI 推动科学研究，创造更大的现实世界效益

> 原文：[How we're using AI to drive scientific research with greater real-world benefit](https://blog.google/innovation-and-ai/technology/research/google-research-scientific-discovery/) · Google

长期以来，AI 一直在推动 Google 的科学进步，而当今突破发生的速度更是前所未有。AI 能力的不断增强，使得科研从突破到现实世界影响的"[魔力循环](https://blog.google/technology/research/what-is-google-research/)"（magic cycle）比以往任何时候都更宽广、更迅捷。

AI 是人类智慧与创造力的放大器。在 Google，我们的团队正利用 AI 解答基础科学问题、拓展可能性的边界，从而带来对生命的新认识，以及应对人类最重大挑战的新方案。在加速科学发现的同时，我们与产业界和学术界的科学界及生态系统紧密协作，并向合作伙伴开放我们的技术与工具，供他们开展自己的研究。

以下是 Google Research 最近分享的、具有重大科学与社会影响的四个突破领域。

## 推进生物医学科学，更好地治疗疾病

我们对 AI 在个性化医疗、科学大众化以及开辟生物与医学发现新途径方面的潜力充满期待。我们的 [AI co-scientist](https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/) 旨在帮助加快[生物医学新发现](https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/)的进程。这一多智能体系统利用 AI 综合信息与执行复杂推理任务的能力，帮助科学家用自然语言创建新颖的假设和研究提案。

我们最近推出了 [AMIE](https://research.google/blog/amie-a-research-ai-system-for-diagnostic-medical-reasoning-and-conversations/) 的[多模态版本](https://research.google/blog/amie-gains-vision-a-research-ai-agent-for-multi-modal-diagnostic-dialogue/)。AMIE 是一个用于医疗诊断对话的研究型 AI 智能体，相关成果已[发表](https://www.nature.com/articles/s41586-025-08866-7)于 [*Nature*](https://www.nature.com/articles/s41586-025-08869-4)（《自然》）杂志。它能够智能地解读视觉医学信息并进行推理，朝着更准确的诊断迈进。AMIE 建立在我们早期的 [MedPaLM](https://www.nature.com/articles/s41586-023-06291-2) 工作以及后续针对[医疗领域](https://sites.research.google/med-palm/)微调的语言模型之上。我们继续向 [Health AI Developer Foundations](https://developers.google.com/health-ai-developer-foundations) 添加资源，帮助开发者构建医疗 AI 应用；我们还发布了 [TxGemma](https://developers.googleblog.com/en/introducing-txgemma-open-models-improving-therapeutics-development/)——一套旨在提升疗法研发效率的开放模型，它基于我们用于胸部 X 光、数字病理学和皮肤学的嵌入模型构建。

我们也在持续推进基因组学研究，以便更好地理解个体的疾病遗传易感性，并诊断罕见疾病。[REGLE](https://www.nature.com/articles/s41588-024-01831-6) 是一个无监督深度学习模型，可帮助研究者发现与基因变异的关联。我们还开源了新的 [DeepVariant 模型](https://github.com/google/deepvariant/blob/r1.8/docs/pangenome-aware-wgs-vg-case-study.md)，作为[个性化泛基因组参考序列](https://www.nature.com/articles/s41592-024-02407-2)（Personalized Pangenome References）合作的一部分，在分析不同祖先的基因组时可将错误减少 30%。

## 推进神经科学研究，揭开大脑的神秘面纱

过去十年，我们为[连接组学](https://sites.research.google/neural-mapping/)（connectomics）领域作出了奠基性贡献，加深了科学界对大脑运作方式的理解。就在昨天，Google Research 与 ISTA 的团队在《自然》杂志上[发表了](https://www.nature.com/articles/s41586-025-08985-1)关于 [LICONN](https://research.google/blog/a-new-light-on-neural-connections/) 的研究——首个利用常见的光学显微镜全面测绘脑组织中神经元及其连接的方法。LICONN 将使世界各地更多实验室能够开展连接组学研究。

在神经连接的基础上更进一步，我们与 HHMI Janelia 和哈佛大学合作，推出了[斑马鱼活动预测基准](https://research.google/blog/improving-brain-models-with-zapbench/)（Zebrafish Activity Prediction Benchmark，ZAPBench），其中包含幼年斑马鱼整个大脑中超过 70,000 个神经元的活动记录。这让研究者首次得以[探究](https://arxiv.org/abs/2503.02618)整个脊椎动物大脑中结构布线与动态神经活动之间的关系。我们已经[开源了数据集和基准](https://zapbench-release.storage.googleapis.com/landing.html)，帮助神经科学家开发更精确的大脑活动模型。

我们还与[普林斯顿大学](https://hassonlab.princeton.edu/)、[纽约大学（NYU）](https://nyulangone.org/locations/comprehensive-epilepsy-center)和[希伯来大学（HUJI）](https://www.deepcognitionlab.com/)合作，通过[一](https://www.nature.com/articles/s41593-022-01026-4)[系](https://www.nature.com/articles/s41467-024-46631-y)[列](https://www.nature.com/articles/s41562-025-02105-9)研究，探索了人脑与深度语言模型在[处理自然语言](https://research.google/blog/deciphering-language-processing-in-the-human-brain-through-llm-representations/)方面的异同。我们的研究结果表明，深度学习模型可以为理解大脑的神经编码提供一个新的计算框架。

## 推进地理空间科学，应对星球尺度的挑战

Google Research 还通过让关键信息更易获取，来加速地理空间问题的求解。我们最近发射了[首颗 FireSat 卫星](https://blog.google/feed/firesat-first-satellite-launch/)，助力[应对野火](https://sites.research.google/gr/wildfires/)。随着星座扩展到 50 颗以上卫星，其每 20 分钟全球更新的高分辨率影像，将帮助应急响应人员更早发现野火，并帮助科学家理解野火的蔓延方式。我们还凭借用于[洪水预报](https://blog.google/technology/ai/google-ai-global-flood-forecasting/)的先进 [AI 模型](https://www.nature.com/articles/s41586-024-07145-1)和 [WeatherNext](https://blog.google/products/google-cloud/scientific-research-tools-ai/) 模型，推动了气候韧性与危机响应。

[地理空间推理（Geospatial Reasoning）](https://research.google/blog/geospatial-reasoning-unlocking-insights-with-generative-ai-and-multiple-foundation-models/)是一项新的研究工作，力求将我们地理空间基础模型的能力与生成式 AI 相结合，挖掘强大且可付诸行动的信息——而且只需一个简单的对话界面。它建立在洪水、野火和天气等既有模型，以及 [Open Buildings](https://sites.research.google/gr/open-buildings/) 和 [SKAI](https://disha.unglobalpulse.org/ai-from-google-research-and-un-boosts-humanitarian-disaster-response-wider-coverage-faster-damage-assessments/) 模型的基础之上，并扩展了我们先前的[人口动态](https://research.google/blog/insights-into-population-dynamics-a-foundation-model-for-geospatial-inference/)和[基于轨迹的流动性](https://dl.acm.org/doi/10.1145/3681766.3699610)基础模型。地理空间推理可以成为推进公共卫生、城市规划、综合业务规划、气候科学等领域的关键工具。

## 推进量子计算，迈向现实世界应用

十多年来，我们一直在朝构建能够解决其他方式无法解决的问题的大规模量子计算机迈进。我们全新的 [Willow](https://blog.google/technology/research/google-willow-quantum-chip/) 芯片是一个重大里程碑，展示了量子纠错能力和最先进的性能。在世界量子日，我们重点介绍了它如何让我们离[现实世界应用](https://blog.google/technology/research/google-quantum-computer-real-world-applications/)更近一步。例如，我们与 [Sandia 国家实验室](https://www.sandia.gov/research/news/sandia-and-google-unleash-new-possibilities-in-quantum-computing/)合作，[证明](https://www.pnas.org/doi/epdf/10.1073/pnas.2317772121)了一种量子算法能够更高效地模拟维持持续聚变反应所需的机制。这有望助力聚变能源成为现实，释放其大规模清洁能源的潜力。我们继续推进量子研究，最近还[分享](https://www.nature.com/articles/s41586-024-08460-3)了一种新颖的[量子模拟混合方法](https://research.google/blog/a-new-hybrid-platform-for-quantum-simulation-of-magnetism/)，为进一步的科学发现铺平了道路。

如今，AI 的承诺正在各个科学学科变为现实。我们将继续追问最重大的问题、攻克此前无解的挑战，追求能够惠及数十亿人的科学突破。
