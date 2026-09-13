---
title: "Google Research：加速科学突破走向现实影响"
title_en: "Google Research: accelerating scientific breakthroughs to real-world impact"
source: https://blog.google/innovation-and-ai/technology/research/google-research-team-tackles-big-challenges-with-science/
site: google-blog
date: 2025-10-23
crawled: 2026-09-13
translated: 2026-09-13
---

# Google Research：加速科学突破走向现实影响

> 原文：[Google Research: accelerating scientific breakthroughs to real-world impact](https://blog.google/innovation-and-ai/technology/research/google-research-team-tackles-big-challenges-with-science/) · Google

过去两周，Google Research 迎来了密集的新成果——从基因组学到量子计算，再到地理空间理解。

这些突破恰恰印证了我所说的[研究的"魔力循环"](https://blog.google/technology/research/what-is-google-research/)：以基础研究应对全球性挑战与机遇，并直接催生现实世界的应用与解决方案。这些解决方案不仅惠及全球数百万人，还会揭示出更多值得解决的重要问题。

在更强大的模型以及 [AI 共同科学家](https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/)、基于 AI 的[专家级实证软件](https://research.google/blog/accelerating-scientific-discovery-with-ai-powered-empirical-software/)等智能体化工具的推动下，这一魔力循环正在显著加速。它适用于众多[学科与领域](https://research.google/blog/google-research-2024-breakthroughs-for-impact-at-every-scale/)。

研究是我们改善日常生活、应对社会挑战与把握机遇的契机，也是我们的责任——这也意味着，研究与创新永远没有"完成"的那一天。

以下展示了 Google Research 的研究方式如何在三个影响深远的领域帮助解决挑战：

### 1. 用 AI 对抗癌症

儿童白血病和许多其他癌症拥有极其复杂的基因特征，需要根据其特定突变制定针对性治疗方案。如果我们能更精确地对这些癌变细胞进行基因组测序，准确找出使它们癌变的具体变异，会怎样？

这正是 [DeepSomatic](https://research.google/blog/using-ai-to-identify-genetic-variants-in-tumors-with-deepsomatic/) 的由来——我们的全新 AI 工具，帮助科学家和医生发现癌细胞中的基因变异。我们在堪萨斯城的合作伙伴 Children's Mercy 使用 DeepSomatic 在儿童白血病样本中识别出 10 个被既往技术遗漏的新基因变异。如果他们能查明某种特定癌症影响患者的机制与原因，就有可能开发出个性化的治疗方法。

更了不起的是，DeepSomatic 还能泛化到它从未见过的癌症。例如，在没有接受过脑癌胶质母细胞瘤训练的情况下，DeepSomatic 就能准确定位导致该病的基因变异。这表明它甚至可以用于罕见或新类型的癌症——这是标志着[ Google 基因组学研究十周年](https://blog.google/technology/research/ten-years-google-genomics/)的重要里程碑。

在与耶鲁大学和 Google DeepMind 的合作中，我们还推出了 [Cell2Sentence-Scale 27B](https://blog.google/technology/ai/google-gemma-ai-cancer-therapy-discovery/)，一个基于 Gemma 的新一代 270 亿参数 AI 模型，能够理解单个细胞的"语言"。它生成了一个关于癌症疗法的新颖假设，我们在活细胞中进行了验证，发现一种药物组合能让癌细胞在实验室环境中显著更容易被免疫系统识别。这是我们用 AI 帮助对抗癌症的一种强大新方式。

### 2. 借助量子计算迈向更好的药物与材料

设计更好的药物和材料——比如性能更强的电池——需要精确理解原子和分子的行为。但当今最强大的经典计算机难以建模这些微妙之处，因为它们依赖近似方法以及由 0 和 1 构成的严格二进制语言；即便是世界上最强大的超级计算机，也无法完全捕捉分子在真实环境中的种种细微行为。原因在于，在这种极小的尺度上，粒子并不遵循"经典"规律，而是服从量子力学：它们可以处于叠加态——不再处于某个简单确定的状态，而是"弥散"在一系列可能性之中；它们还可以相互纠缠——多个原子可以步调一致地联动，而非各自独立行事。

这正是 Google Research [建造量子计算机](https://blog.google/technology/research/behind-the-scenes-google-quantum-ai-lab/)最有说服力的理由之一——它能以任何经典计算机都无法企及的方式"讲量子语言"，精确建模大自然在亚原子层面的真实运作方式。我们[全新的 Quantum Echoes 算法](https://blog.google/technology/research/quantum-echoes-willow-verifiable-quantum-advantage/)展示了我们的 Willow 芯片在哪些计算上可以快得多——这些计算对于以完整精度描述分子行为极为有用。这是世界上首个指向量子计算最终实用化的算法，例如设计更好的材料、更好的药物等等。我们已开始与加州大学伯克利分校的研究人员合作，通过实验探索它的潜力。

### 3. 理解地球

行星科学与危机响应中最难、也最重要的问题，从来都不仅仅是关于某一类地理空间信息——而是如何把它们汇聚到一起。例如，若想预测在一场即将来临的风暴中哪些社区最为脆弱、哪些基础设施面临风险，仅仅知道风暴何时登陆或建筑物在哪里是不够的。我们需要全貌：风暴的路径与强度、人口密度、交通模式，以及对脆弱基础设施的预计影响。这种综合视角需要同时合成多种类型的地理空间数据，以及预测地球不同侧面的众多模型——而且要一并进行。

正因如此，我们正在开发 [Earth AI](https://blog.google/technology/research/new-updates-and-more-access-to-google-earth-ai/)——把所有这些信息与预测能力编织在一起。那些目前因过于复杂、需要调用太多彼此分散的地理空间资源而无法回答的问题，将变得可以着手解决。而这又将催生新的研究——对地球有用数据的新采集、新型传感器，以及用 AI 建模全球复杂互联模式的新用法。这项多年的努力将在新的现实用途与新的研究之间持续循环，揭示我们如何才能在这颗星球上更好地生活的更深层洞见。

以上只是 3 个领域——而这样的领域还有几十个！——Google Research 正在其中取得基础性突破，并展示如何将它们规模化，为人们带来真实、可感的影响。这些突破并非孤立产生：我们坚信，某一科学领域的突破能够助益另一领域——无论是用更好的量子数据加速 AI 发现，还是将地理空间数据与公共卫生洞见相连。这就是我们铺就通向未来之路的方式，一切都根植于能让人们的现实变得更好的研究。
