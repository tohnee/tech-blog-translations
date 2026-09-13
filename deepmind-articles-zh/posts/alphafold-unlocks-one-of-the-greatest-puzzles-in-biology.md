---
title: "AlphaFold 解开生物学最重大的谜题之一"
title_en: "AlphaFold unlocks one of the greatest puzzles in biology"
source: https://deepmind.google/blog/alphafold-unlocks-one-of-the-greatest-puzzles-in-biology/
site: deepmind
date: 2022-07-28
crawled: 2026-09-13
translated: 2026-09-13
---

# AlphaFold 解开生物学最重大的谜题之一

> 原文：[AlphaFold unlocks one of the greatest puzzles in biology](https://deepmind.google/blog/alphafold-unlocks-one-of-the-greatest-puzzles-in-biology/) · Google DeepMind

AI 系统帮助研究人员拼合人类细胞中最大的分子结构之一

当 Pietro Fontana 于 2019 年 5 月加入哈佛医学院和波士顿儿童医院的 Wu 实验室时，摆在他面前的是被称为世界上最难、最巨大的拼图之一。这项任务是拼出一个核孔复合体（nuclear pore complex）的模型——人类细胞中最大的分子机器之一。

「从一开始就非常具有挑战性，」他解释道。这个复合体被称为[庞然大物](https://www.nature.com/articles/d41586-022-00997-5)是有充分理由的：它由 30 多种不同的蛋白质亚基（称为核孔蛋白，nucleoporins）构成，总数超过 1000 个，彼此复杂地交织在一起。

> 我认为 AlphaFold 已经彻底改变了结构生物学的理念

Pietro Fontana

博士后研究员

因此，当两年后他第一次坐下来在工作中使用 AlphaFold——与对这一 AI 系统更为熟悉的加州大学伯克利分校的 Alexander Tong 一起——他并不确定它是否会有所帮助。但接下来，2021 年的夏天成了一个不期而至的突破时刻。AlphaFold 预测出了此前未曾确定的核孔蛋白结构，并在此过程中揭示出核孔复合体的更多面貌。多亏这一 AI，他们得以生成该复合体细胞质环近乎完整的模型。

![一幅 3D 分子模型，显示环状的核孔复合体，其中一段以浅蓝色高亮显示，衬在带纹理的灰色结构上。](https://lh3.googleusercontent.com/wcTreMWOYa1R2gZqU5zJrIgw3QxzK4bN3MkOShq834oM_35_53_zZopozkHcqIc_Itg2QUJaWpU7Wkhe-pUCY4vzRgnbon3ZoNSYX2NiNK6v73gQZA=w1440)

核孔复合体细胞质环模型。图片来源：Fontana et al. Science 2022

「许多组分早已为人熟知，但借助 AlphaFold，我们还构建了那些结构未知的组分，」他说。「我开始意识到，它确实是一个对我们而言庞大而有用的工具。我认为 AlphaFold 已经彻底改变了结构生物学的理念。」

像 Fontana 这样的分子科学家数十年来一直致力于解读核孔复合体。它之所以重要，是因为它是进出细胞核的一切物质的守门人，并被认为掌握着[越来越多严重人类疾病](https://www.science.org/doi/10.1126/science.abm9326)的答案，包括[肌萎缩侧索硬化症（ALS）和其他神经退行性疾病](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8835831/)。了解这个复合体如何组装，可能为其他突破性、甚至能拯救生命的发现打开大门。

![Pietro Fontana 的半身照，他在实验室环境中微笑，背景中有一台 FEI Vitrobot。](https://lh3.googleusercontent.com/aGbu03vzAhW058CihG1pIiUci-2oJR-g5flClwX3hl1w8f4ejfJkUt4_pJqpEsjpsY-5evmgXeuco8SREGRZkzOq2nDtnoqTe9oaBuv30z95kaQAaw=w1440)

光是复合体本身的庞大体量就已经够具挑战性了，而它繁多的不同部件又增添了额外的复杂度。「这是达到足够[清晰]的分辨率、让我们能够解读复合体的序列与结构的一大难点，」该实验室的首席研究员 Hao Wu 说。即便拥有大量数据，团队此前也只能获得中等分辨率的结构图像。

缺失的拼图碎片同样阻碍了进展。Wu 说，如果不掌握整套碎片，很难判断拼图如何拼合。「要弄清不同的蛋白质亚基如何组合在一起，你真的需要借助它们各自结构的帮助，」Wu 解释道。

这正是 AlphaFold 为 Wu 实验室（成员还包括 Ying Dong 和 Xiong Pi）带来转机的地方。团队在非洲爪蛙（Xenopus laevis，用作模式系统）卵中发现的蛋白质上运行 AlphaFold，成功绘制出了当时未知的所有不同亚基的结构。「当我们开始尝试时，我们并不真的知道这些预测能否很好地贴合地图，」Wu 回忆道。「但事情就是这样发生了。那相当了不起。」

当然，科学是一项协作事业。要解开核孔复合体这样一个错综复杂的谜题，这不仅是团队合作，更是[世界各地许多团队](https://www.science.org/doi/10.1126/science.abq4792)勤勉与坚韧的结晶。在大西洋彼岸，来自德国马克斯·普朗克生物物理研究所（MPIBP）和欧洲分子生物学实验室（EMBL）的科学家们将 AlphaFold 与冷冻电子断层扫描相结合，为人类核孔复合体（NPC）建模。他们迄今取得的成果是一个[新模型](https://www.biorxiv.org/content/10.1101/2021.10.26.465776v1)，完整度达到旧模型的两倍。如今它覆盖了 NPC 的三分之二，拼图的很大一部分已经解决，向理解它如何控制进出细胞核的物质迈出了一大步。

![一幅环状核孔复合体的 3D 分子模型，黑色背景上，由高饱和多彩蛋白质组成的内环映衬在较暗的蓝色外环之上。](https://lh3.googleusercontent.com/1_8J3ZJiII1waTDBB-x2ZgpYfEwiMQqRShMIEJYJOMKuaBoLsvCDZcBSnbG0Hq9--vsZyy63nkKXDyOjCKk0UpoqDs37pcHEyD5G5X1AGz6zVWLRsw=w1440)

德国 MPIBP 和 EMBL 科学家制作的人类核孔复合体模型。图片来源：Agnieszka Obarska-Kosinska

前路仍长——最后的三分之一尚未完成。虽然 AlphaFold 将使剩余的拼图更容易解决，科学家们也清楚它的局限。据 Wu 说，AI 系统在核孔复合体这一案例中表现出色，是因为其亚基包含重复的螺旋结构，这类结构往往更容易预测。但对其他蛋白质而言，情况可能就没这么简单了。

重要的是，不要把 AlphaFold——或任何其他 AI 工具——视为无所不能的终极法宝。Tong 对此深有同感。「事实上，AlphaFold 有时会给出一些非常奇怪的结果，」Wu 说。「但如果你理解它是如何预测的，你就可以在分析中把这一点考虑进去。」

尽管如此，显而易见的是，AlphaFold 不仅拓展了科学的边界，而且是在一个此前被认为不可能的时间尺度上做到的。「我很高兴 AlphaFold 在恰当的时机问世，因为它显著加快了一切进程，」Fontana 说。

Fontana P., Dong Y., Pi X., Tong A.B., Hecksel C.W., Wang L., Fu TM., Bustamante C., Wu H. Structure of cytoplasmic ring of nuclear pore complex by integrative cryo-EM and AlphaFold. Science 376, 6598, (2022). DOI:10.1126/science.abm9326.
