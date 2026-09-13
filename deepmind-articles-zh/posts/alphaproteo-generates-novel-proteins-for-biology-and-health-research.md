---
title: "AlphaProteo 为生物学与健康研究生成新型蛋白质"
title_en: "AlphaProteo generates novel proteins for biology and health research"
source: https://deepmind.google/blog/alphaproteo-generates-novel-proteins-for-biology-and-health-research/
site: deepmind
date: 2024-09-05
crawled: 2026-09-13
translated: 2026-09-13
---

# AlphaProteo 为生物学与健康研究生成新型蛋白质

> 原文：[AlphaProteo generates novel proteins for biology and health research](https://deepmind.google/blog/alphaproteo-generates-novel-proteins-for-biology-and-health-research/) · Google DeepMind

新的 AI 系统能设计出成功与目标分子结合的蛋白质，有望推动药物设计、疾病理解等领域的发展。

体内的每一个生物过程，从细胞生长到免疫反应，都依赖于被称为蛋白质的分子之间的相互作用。就像钥匙配锁一样，一种蛋白质可以与另一种蛋白质结合，帮助调控关键的细胞过程。像 [AlphaFold](https://deepmind.google/impact/meet-the-scientists-using-alphafold/) 这样的蛋白质结构预测工具已经让我们深入理解了蛋白质如何相互作用以发挥功能，但这些工具无法创造新的蛋白质来直接操纵这些相互作用。

不过，科学家可以创造出能与目标分子成功结合的新型蛋白质。这类结合物（binder）可以帮助研究人员在广泛的研究领域加速进展，包括药物开发、细胞与组织成像、疾病理解与诊断——甚至提高农作物对害虫的抗性。虽然[近期的机器学习方法](https://www.nature.com/articles/s41586-023-06415-8)在蛋白质设计方面已取得长足进步，但这一过程仍然费力，需要大量的实验测试。

今天，我们推出 [AlphaProteo](https://arxiv.org/abs/2409.08022)，这是我们的第一个用于设计新型、高强度蛋白质结合物的 AI 系统，可作为生物学与健康研究的构建基块。这项技术有潜力加速我们对生物过程的理解，并助力新药发现、生物传感器开发等。

AlphaProteo 可以为多种目标蛋白质生成新的蛋白质结合物，包括与癌症及糖尿病并发症相关的 [VEGF-A](https://www1.rcsb.org/structure/1BJ1)。这是 AI 工具首次成功为 VEGF-A 设计出有效的蛋白质结合物。

在我们测试的七种目标蛋白质上，AlphaProteo 还实现了比现有最佳方法更高的实验成功率和 3 到 300 倍的结合亲和力提升。

## 学习蛋白质相互结合的复杂方式

能够与目标蛋白质紧密结合的蛋白质结合物很难设计。传统方法非常耗时，需要多轮大量的实验室工作。结合物被创造出来之后，还要经过额外的实验轮次来优化结合亲和力，使其紧密结合到足以实用。

AlphaProteo 在来自[蛋白质结构数据库（PDB）](https://www.rcsb.org/)的大量蛋白质数据以及来自 AlphaFold 的超过 1 亿个预测结构上训练，已经学习了分子相互结合的种种方式。给定目标分子的结构和该分子上一组首选的结合位置，AlphaProteo 会生成一个在这些位置与目标结合的候选蛋白质。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

预测的蛋白质结合物结构与目标蛋白相互作用的示意图。蓝色显示的是由 AlphaProteo 生成的、为与目标蛋白结合而设计的预测蛋白质结合物结构。黄色显示的是目标蛋白，具体为 SARS-CoV-2 刺突蛋白受体结合域

## 在重要的蛋白质结合目标上展示成功

为了测试 AlphaProteo，我们为多种目标蛋白质设计了结合物，包括两种与感染相关的病毒蛋白——[BHRF1](https://www.rcsb.org/structure/2WH6) 和 [SARS-CoV-2](https://www.rcsb.org/structure/6M0J) 刺突蛋白受体结合域（SC2RBD）——以及五种与癌症、炎症和自身免疫疾病相关的蛋白质：[IL-7Rɑ](https://www.rcsb.org/structure/3DI3)、[PD-L1](https://www.rcsb.org/structure/5O45)、[TrkA](https://www.rcsb.org/structure/1WWW)、[IL-17A](https://www.rcsb.org/structure/4HSA) 和 [VEGF-A](https://www1.rcsb.org/structure/1BJ1)。

我们的系统拥有极具竞争力的结合成功率和同类最佳的结合强度。对于这七个目标，AlphaProteo 在计算机内（in-silico）生成的候选蛋白质经实验测试后都能与预期蛋白强烈结合。

![一系列 3D 分子渲染图，显示 AlphaProteo 设计的蛋白质结合物（蓝色）与七种不同目标蛋白（米色，接触区域为黄色）结合。标注的目标包括 BHRF1、SC2RBD、IL-7RA、PD-L1、TrkA、IL-17A 和 VEGF-A。](https://lh3.googleusercontent.com/dVPNUTwz7N2egenYKfXLNPOS__2zD5Cs0guRp8KpVRF-V9MyD71twiqqXEO-JN7atru6JOUkGNg-2FOsHrb23-Hur1DQB64POsC089w4EGtDIOUN=w1440)

AlphaProteo 成功生成结合物的七种目标蛋白预测结构插图网格。蓝色为湿实验室中测试的结合物示例，黄色为蛋白目标，深黄色高亮为预期的结合区域。

对于其中一个特定目标——病毒蛋白 [BHRF1](https://www.rcsb.org/structure/2WH6)——我们的候选分子在 [Google DeepMind 湿实验室](https://www.crick.ac.uk/news/2022-07-06_the-francis-crick-institute-and-deepmind-join-forces-to-apply-machine-learning-to-biology)测试时有 88% 成功结合。基于所测试的目标，AlphaProteo 结合物的结合强度平均也比现有最佳设计方法强 10 倍。

对另一个目标 [TrkA](https://www.rcsb.org/structure/1WWW)，我们的结合物甚至比此前针对该目标、经过[多轮实验优化](https://www.nature.com/articles/s41586-022-04654-9)的最佳设计结合物还要强。

![标题为"In vitro success (Higher is better)"（体外成功率，越高越好）的柱状图，比较 AlphaProteo（蓝色柱）与其他设计方法（浅灰色柱）在七种目标蛋白上的实验成功率。在每一个目标上，AlphaProteo 都取得了更高的成功率，其中 BHRF1 上最高达 90%，而在 VEGF-A 上其他方法成功率为零，唯有 AlphaProteo 成功。](https://lh3.googleusercontent.com/E9UEYEvqwPBkB6JbJ7-vp1UdrffLacNq3XUdo27tp0ZMXcn8EovMLecyVgkRowYdxvUIksrNYfmB2PbFdCuj6N2uTnnyT7a7NMD9xmlemx3UEpRMeFw=w1440)

柱状图显示 AlphaProteo 输出在七种目标蛋白上各自的实验体外成功率，与其他设计方法相比。成功率越高，意味着找到成功结合物所需测试的设计越少。

![标题为"Affinity of best binder (Lower is better)"（最佳结合物亲和力，越低越好）的柱状图，在对数刻度（以 Kd (nM) 计量）上比较 AlphaProteo（蓝色）与其他设计方法（浅灰色）在七种目标蛋白上的结合亲和力。在包括 BHRF1、SC2RBD、IL-7RA、PD-L1、TrkA、IL-17A 和 VEGF-A 在内的每个目标上，AlphaProteo 都取得了更低的 Kd 值，表明更强的结合亲和力，其中 VEGF-A 只有 AlphaProteo 成功。](https://lh3.googleusercontent.com/SywabQtkJ1OQTUnDF7Kr9uTBU9xT6Epp7ASX5paLO1YrXfh27JKnh1mKxN735nGSQW4T-2cDP3c7hN58_GQflRlHbKoukpB1e0c7LCmVc_93J8qYrQ=w1440)

柱状图显示 AlphaProteo 未经实验优化的设计在七种目标蛋白上各自的最佳亲和力，与其他设计方法相比。亲和力越低，意味着结合物与目标蛋白结合越紧密。请注意纵轴为对数刻度。

## 验证我们的结果

除了在计算机内验证并在自家湿实验室测试 AlphaProteo 之外，我们还邀请[弗朗西斯·克里克研究所](https://www.crick.ac.uk/)的 [Peter Cherepanov](https://www.crick.ac.uk/research/labs/peter-cherepanov)、[Katie Bentley](https://www.crick.ac.uk/research/labs/katie-bentley) 和 [David LV Bauer](https://www.crick.ac.uk/research/find-a-researcher/david-lv-bauer) 的研究团队来验证我们的蛋白质结合物。在不同的实验中，他们深入研究了我们一些较强的 SC2RBD 和 VEGF-A 结合物。这些研究团队确认，这些结合物的结合相互作用确实与 AlphaProteo 的预测相似。此外，这些团队还确认了结合物具有有用的生物学功能。例如，我们的一些 SC2RBD 结合物被证明能够阻止 SARS-CoV-2 及其部分变异株感染细胞。

AlphaProteo 的表现表明，它有可能大幅缩短涉及蛋白质结合物的各类应用的初始实验所需时间。不过，我们知道我们的 AI 系统存在局限：它未能针对第八个目标 [TNFɑ](https://www.rcsb.org/structure/1TNF)——一种与类风湿关节炎等自身免疫疾病相关的蛋白质——设计出成功的结合物。我们选择 TNFɑ 是为了有力地挑战 AlphaProteo，因为计算分析显示针对它设计结合物将极其困难。我们将继续改进和扩展 AlphaProteo 的能力，目标是最终攻克此类高难度目标。

实现强结合通常只是设计具有实际应用价值的蛋白质的第一步，在研究与开发过程中还有许多生物工程障碍需要克服。

## 迈向蛋白质设计的负责任发展

蛋白质设计是一项快速发展的技术，在从理解致病因素、加速病毒暴发诊断测试开发、支持更可持续的制造工艺，到清除环境污染物等方方面面都有推动科学的巨大潜力。

为了应对生物安全方面的潜在风险，在我们[长期秉持的责任与安全方针](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/alphafold-3-predicts-the-structure-and-interactions-of-all-lifes-molecules/Our-approach-to-biosecurity-for-AlphaFold-3-08052024)的基础上，我们正与领先的外部专家合作，为分阶段共享这项工作提供指导，并参与社区制定最佳实践的努力，包括[核威胁倡议组织（NTI）](https://www.nti.org/)新设立的 [AI Bio Forum](https://www.nti.org/news/nti-convenes-the-first-international-ai-bio-forum/)。

接下来，我们将与科学界合作，利用 AlphaProteo 解决有影响力的生物学问题，并了解其局限。我们还在 Isomorphic Labs 探索它的药物设计应用，对未来充满期待。

与此同时，我们将继续提升 AlphaProteo 算法的成功率与亲和力，扩展它所能应对的设计问题范围，并与机器学习、结构生物学、生物化学及其他学科的研究者合作，为社区开发一个负责任且更全面的蛋白质设计方案。

[阅读我们的白皮书](https://arxiv.org/abs/2409.08022)

**致谢**

这项研究由我们的蛋白质设计团队和湿实验室团队共同开发。

我们要感谢合作者 Peter Cherepanov、David Bauer、Katie Bentley 及其弗朗西斯·克里克研究所的团队提供的宝贵实验洞见与结果，感谢 AlphaFold 团队——他们早期的工作和算法提供了训练输入和评估洞见——也感谢 Google DeepMind 内部为这项计划做出贡献的许多其他团队。
