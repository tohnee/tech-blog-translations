---
title: "AlphaGenome Atlas：人类基因组中每一种可能的 DNA 字母变化的预测图谱"
title_en: "AlphaGenome Atlas: A predictive map of every possible DNA letter change in the human genome"
source: https://deepmind.google/blog/alphagenome-atlas-a-predictive-map-of-every-possible-dna-letter-change-in-the-human-genome/
site: deepmind
date: 2026-09-08
crawled: 2026-09-13
translated: 2026-09-13
---

# AlphaGenome Atlas：人类基因组中每一种可能的 DNA 字母变化的预测图谱

> 原文：[AlphaGenome Atlas: A predictive map of every possible DNA letter change in the human genome](https://deepmind.google/blog/alphagenome-atlas-a-predictive-map-of-every-possible-dna-letter-change-in-the-human-genome/) · Google DeepMind

预测人类基因组中每一种可能的单字母 DNA 变异的分子影响，将帮助我们加速理解生物学。

今天，我们推出 AlphaGenome Atlas：一个平台（[详见我们的论文](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/alphagenome-atlas-a-predictive-map-of-every-possible-dna-letter-change-in-the-human-genome/alphagenome-atlas.pdf)），其中包含对人类基因组中 **90 亿个单核苷酸变异——即每一种可能的单字母变化——的影响预测。** 这是迄今为止关于基因突变如何影响分子生物学最全面的目录，并通过一个直观且免费使用的[网站门户](https://alphagenome.google/atlas)向学术研究开放。

DNA 是生命的语言。掌握它是一项宏大的挑战，有可能变革我们理解生物学和治疗疾病的能力。但这一领域的进展一直受制于一个根本问题：如何在分子层面解释基因变异对生物学的影响。人类基因组中大约存在 90 亿种可能的单字母突变，要在实验室中逐一验证几乎是不可能的。

Google DeepMind 已凭借 AlphaGenome 在这一挑战上取得进展——这是一个能够预测基因变异如何影响生物过程的人工智能（AI）模型。AlphaGenome 对分析特定变异很有帮助，并已在研究中得到广泛使用，但我们希望向研究人员展示整个基因组中变异的全景视图。

通过大规模预计算 AlphaGenome 的预测结果，我们创建了一个易于访问的资源，极大地扩展了该模型的覆盖范围。正如地图集（atlas）是地图的集合，将海拔、位置等陆地特征联系在一起，AlphaGenome Atlas 也绘制了整个基因组中 DNA 变异的分子效应图谱。

为了帮助科学家快速找到影响最大的基因变化，我们还发布了 AlphaGenome Variant Impact（AVI）评分。AVI 结合了 AlphaGenome 和 AlphaMissense——我们用于预测改变蛋白质的 DNA 变异影响的模型——的优势，将两个模型的预测浓缩为一个数字。现在，研究人员可以同时对变异进行快速排序并解读其分子效应。

我们信赖的外部合作者已经利用 AlphaGenome Atlas 在未解的罕见病研究中识别并实验验证了关键变异，并找到了与常见性状相关的罕见变异。

AlphaGenome Atlas 今天起可通过一个[直观的网站门户](https://alphagenome.google/atlas)、我们的 [AlphaGenome API](https://github.com/google-deepmind/alphagenome) 以及 [Google Antigravity](https://antigravity.google/use-cases/science) 中的技能（skill）来使用。

[阅读我们的论文](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/alphagenome-atlas-a-predictive-map-of-every-possible-dna-letter-change-in-the-human-genome/alphagenome-atlas.pdf)[探索 AlphaGenome](https://deepmind.google/science/alphagenome/)

## AlphaGenome Atlas

![](https://lh3.googleusercontent.com/XtSeskvW7gYRyovhEWB7bkB6ezvdjdtW0a7NSw9TYgIMshiJMT5AS3lMKLa-Qq6mICrmZgb1vrSQmG9TJOkD97EzWM9GPQ0XEWPXOD9DWRU5sdWRww=w1440-h810-n-nu)

AlphaGenome Atlas 是一个规模达 1 PB 的数据集，比 AlphaFold Database 大 30 多倍。当我们在 2022 年扩充 AlphaFold Database 时，[我们将](https://deepmind.google/blog/alphafold-reveals-the-structure-of-the-protein-universe/)可用的三维结构信息从约 19 万个实验解析结构扩展到超过 2 亿个结构预测——覆盖了科学界已知的几乎所有已编目蛋白质。该数据库为没有编程经验的研究人员提供了一个可用的门户，提供了直观的可视化，并使大规模蛋白质结构分析变得更加容易。它迅速成为推动生命科学各领域发现的关键资源，并在无数领域持续加速研究人员的重要工作。

在构建 AlphaGenome Atlas 时，我们同样希望让预测结果更易获取，并为科学家提供一种探索庞大数据集的直观方式。

AlphaGenome Atlas 提供了若干功能强大且相互关联的资源，让研究人员能够将变异直接与其所破坏的功能性 DNA 序列关联起来。

- **分子效应预测** Atlas 为每个变异提供数千项分子效应预测，覆盖基因调控的多个重要方面，涉及数百种人类和小鼠细胞类型与组织。这是进一步使用其他资源的起点。
- **AVI 评分** 一个描述每种基因变异影响的单一数字。
- **AVI 特征归因** 每个 AVI 评分还与驱动它的特定生物学特征相关联，例如 AlphaGenome 预测的基因调控各方面，或来自 AlphaMissense 的蛋白质影响评分。
- **DNA 序列基序（motif）** 收录超过 2,500 个反复出现的 DNA 序列——基因组的「词汇」——及其位置的全面集合。

这些资源共同支持研究人员开展广泛的基因研究任务，从快速变异排序到深入探究变异功能。

广泛的社区合作指导了 AlphaGenome Atlas 的设计。AVI 评分帮助研究人员根据潜在影响快速打分和排序变异。至关重要的是，它同时适用于编码区（基因组中编码蛋白质的 2%）和非编码区（其余 98%），后者调控基因活动，并容纳了大多数与性状相关的变异。

我们的测试表明，AVI 评分在许多变异致病性和罕见病基准测试中提供了一流的性能。为了帮助解读这些评分，我们还计算了 AVI 特征归因，突出显示每种变异被预测最可能破坏的分子过程——例如 RNA 剪接或基因表达。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

**AlphaGenome Atlas 概览。****(1)** 为超过 90 亿个单核苷酸变异生成全基因组的预计算效应。**(2)** 由此为每个变异推导出一个等位基因分辨率的 AlphaGenome Variant Impact（AVI）评分。为便于变异解读，AlphaGenome Atlas 随后将 AVI 评分分解为跨可解释类别（如染色质可及性、剪接和保守性）的加性特征贡献。**(3)** 预计算的变异效应、AVI 评分和 AVI 特征归因相互关联，并与全基因组*从头*基序（*de novo* motif）汇编结合，从而能够对变异功能获得高分辨率的机制性洞察。

## 现实世界的影响：从罕见病到群体遗传学与分子生物学

AlphaGenome Atlas 提供了基因组的高分辨率全局视图。这些大规模预测在应用于有针对性的研究问题时才能发挥最大作用。通过将这些数据转化为可操作的生物学洞察，我们的学术合作伙伴已经在揭示基因变异与疾病之间的联系。

**理解未解的罕见病。** 理解罕见病的一大障碍，是在数千个候选变异中精确定位少数致病变异这一艰巨任务。在与 [GREGoR Consortium](https://gregorconsortium.org/) 的合作中，研究人员将 AVI 评分应用于未解罕见病研究，对这些「大海捞针」式的基因变异进行优先级排序。当 Broad Institute 的 [Laura Covill](https://scholar.google.com/citations?user=2Hm3siUAAAAJ&hl=en) 和 [Anne O'Donnell-Luria](https://www.broadinstitute.org/bios/anne-o%E2%80%99donnell-luria) 及其同事使用 AVI 评分来对先前研究中所忽视的罕见病驱动变异进行优先排序时，团队发现了一个影响名为 *DNM1* 的基因的变异，该基因与癫痫性脑病密切相关。

至关重要的是，AVI 评分所依赖的 AlphaGenome 预测准确显示了该变异的作用机制：它产生了一个错误的剪接位点（细胞遗传指令中的一个错误），导致所生成蛋白质出现异常延伸。实验筛选验证了这一研究预测，并发现了具有类似效应的邻近变异，表明 Atlas 是理解有影响的基因组变异的强大工具。

**绘制与蛋白质水平和复杂性状相关的罕见变异图谱。** 超越单个罕见病研究，AlphaGenome Atlas 还能帮助揭示普通人群中常见性状的遗传架构。要确定哪些罕见非编码变异与特定性状或疾病相关是出了名的困难，因为数量庞大的无害基因变化会形成统计上的「背景噪声」。

为了检验 AlphaGenome Atlas 能在多大程度上提升我们发现影响人类性状的非编码变异的能力，埃克塞特大学医学研究委员会研究员 [Gareth Hawkes](https://experts.exeter.ac.uk/28140-gareth-hawkes) 将 AlphaGenome Atlas 应用于超过 54,000 名 UK Biobank 参与者的全基因组数据，使这些难以捕捉的信号更加明显。通过根据预测的分子效应对罕见变异进行分组，Hawkes 多发现了 22% 的非编码遗传关联，这些关联原本会被淹没在统计噪声中而无法检出。这使 Hawkes 能够精确定位驱动人体循环系统中关键蛋白质丰度的特定调控变异，包括 PLA2G7（与衰老相关）和 EGLN1（一种关键的细胞氧传感器）。

Hawkes 进一步推进了这一方法，他利用 AlphaGenome Atlas 研究 UK Biobank 中数以亿计的非编码变异如何可能与身体质量指数（BMI）相关。通过聚焦于 Atlas 预测影响力最大的 1% 非编码变异，他识别出 19 个遗传区域，这可以为该性状下一阶段的定向研究指明方向。

**识别基因组的调控「词汇」。** Atlas 还可用于识别哪些反复出现的短序列（即基序）在不同细胞类型中驱动着不同基因的分子过程。这些基序可以提供关键线索，例如定位转录因子（开启或关闭基因的蛋白质）的结合位点，并为非编码变异提供额外的解读。例如，Stowers Institute for Medical Research 的 [Julia Zeitlinger](https://www.stowers.org/people/julia-zeitlinger) 和 [Melanie Weilert](https://labs.stowers.org/zeitlinger/people/melanie-weilert?modal=true) 利用这一资源，对哪些转录因子只影响 DNA 的可及性、而哪些还能开启和关闭基因进行了分类。

## 加速基因组发现

通过 AlphaGenome Atlas，我们正在创建新的信息层，以帮助进一步加深对人类遗传密码的理解。我们希望这将成为科学家们的宝贵资源，但我们也将其视为一个基线而非终点。随着 AlphaGenome 等 AI 模型的改进，我们绘制的整个人类基因组图谱将变得越来越全面和精确。

AlphaGenome Atlas 单独使用已经十分强大，但它也代表着我们迈向为生物学家打造广泛、统一解决方案这一愿景的一步。其资源可以集成到我们更广泛的智能体系统中，例如 [Google Antigravity](https://antigravity.google/use-cases/science)，以帮助增强端到端的科学工作流。

同样重要的是，AlphaGenome Atlas 的科学知识应当被广泛获取，因此我们从今天起通过[我们的网站](https://deepmind.google.com/science/alphagenome/atlas)向非商业用途开放，并即将在 Google Cloud 上支持商业用途。（AlphaGenome 基础模型已可在 [GitHub](https://github.com/google-deepmind/alphagenome_research) 上和通过 [AlphaGenome API](https://github.com/google-deepmind/alphagenome) 供学术使用，也可通过 [Cloud 上的 Model Garden](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/open-models/alphagenome) 供商业使用。）

这些工具将共同帮助研究人员和行业合作伙伴加快生物学发现的步伐：发现新的治疗靶点、更好地理解遗传疾病，并推动下一波定向实验验证。

[探索 AlphaGenome](https://deepmind.google/science/alphagenome/)[探索 AlphaGenome Atlas](https://deepmind.google.com/science/alphagenome/atlas)[使用 AlphaGenome Atlas 技能](https://antigravity.google/use-cases/science)[与 AlphaGenome 用户建立联系](https://www.alphagenomecommunity.com/)[阅读我们的论文](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/alphagenome-atlas-a-predictive-map-of-every-possible-dna-letter-change-in-the-human-genome/alphagenome-atlas.pdf)

## 致谢

我们感谢埃克塞特大学、Broad Institute、波士顿儿童医院、Stowers Institute for Medical Research、哈佛大学、纪念斯隆-凯特琳癌症中心、麻省总医院基因组医学中心以及堪萨斯大学医学中心的研究合作者。

这项工作的完成得益于以下人员的贡献：Jun Cheng, Kyle R. Taylor, Lauren Nicolaisen, Joshua Pan, Clare Bycroft, Matteo Perino, Tom Ward, Raina W. Thomas, Natasha Latysheva, Gareth Hawkes, Laura E. Covill, Melanie Weilert, Maile J. Hirschmann, Xi Dawn Chen, Robin N Beaumont, V Kartik Chundru, Michael N Weedon, Simon Bourdareau, Hoyin Chu, Dhavi Hariharan, Thais Kagohara, Lucas Tenório, Yosuke Ushigome, Amanda Stafford, Courtney A. Shearer, Barbara Ikica, Ada Fang, Mouad Naciri, Victoria Johnston, Richard Green, Elisa Lai Hong Wong, Vincent Dutordoir, Anne Mottram, Adam Gayoso, Eirini Arvaniti, Guido Novati, Heidi L. Rehm, Fei Chen, Caleb A. Lareau, Caroline F Wright, Anne O'Donnell-Luria, Julia Zeitlinger, Pushmeet Kohli, Žiga Avsec。

我们感谢队友和合作者的技术支持与反馈，包括：Kathryn Tunyasuvunakool, Alexander Karollus, Risha Patel, Francesca Pietra, Alisha Eastep, Doga Fadillioglu, Charlie Taylor, Raphael Aboyeji, Uchechi Okereke, Gemma Gibbs, Olufemi Duduyemi, Juan Mateos-Garcia, Mariana Felix, Sahar Abdulrahman, Antonia Mould, Rachael Tremlett, Chang Yun, Salil Deshpande, Anshul Kundaje, Samantha Bryen, Greg Findlay, Phoebe Dace, Kinga Bujakowska, Emma Sherrill, Aubrie Soucy Verran, Boxun Zhao, Tim Yu, Francesca Pietra, Brendah Namugamba, Cassie Gray, Daniel MacArthur, Lingyi Wang, Marc Mansour, Mohamad Hajjari, Mounica Vallurupalli, Philip Montgomery, Phoebe Dace, Roisin Sullivan, Sam Bryen, Teresa Niccoli。

最后，我们感谢 Evie Gray、Adriana Fernandez Lara、Alex Wilkins、Danielle Breen、Mariana Montes、Inês Ayer、Ryan Smith、Ross West 和 Gaby Pearl 在传播这项工作上提供的专业支持。

---

AlphaGenome Atlas 提供的信息并非旨在替代专业的医疗建议、诊断或治疗，也不构成医疗或其他专业建议。AlphaGenome 尚未针对任何临床用途进行验证，也未获批准用于任何临床用途。
