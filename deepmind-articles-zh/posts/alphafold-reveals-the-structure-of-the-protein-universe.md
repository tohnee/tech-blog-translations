---
title: "AlphaFold 揭示蛋白质宇宙的结构"
title_en: "AlphaFold reveals the structure of the protein universe"
source: https://deepmind.google/blog/alphafold-reveals-the-structure-of-the-protein-universe/
site: deepmind
date: 2022-07-28
crawled: 2026-09-13
translated: 2026-09-13
---

# AlphaFold 揭示蛋白质宇宙的结构

> 原文：[AlphaFold reveals the structure of the protein universe](https://deepmind.google/blog/alphafold-reveals-the-structure-of-the-protein-universe/) · Google DeepMind

距离我们发布并开源 [AlphaFold](https://deepmind.google/science/alphafold/)——一个仅凭蛋白质的一维氨基酸序列就能预测其三维结构的 AI 系统——并创建 [AlphaFold 蛋白质结构数据库](https://alphafold.ebi.ac.uk/)（AlphaFold DB）以免费向世界分享这一科学知识，已经过去一年了。蛋白质是生命的基石，支撑着每一种生物体内的每一个生物学过程。由于蛋白质的形状与其功能密切相关，了解蛋白质的结构能让我们更深入地理解它的作用及其工作原理。我们曾希望这一开创性的资源能够帮助加速全球的科学研究与发现，也希望其他团队能够学习并基于我们在 AlphaFold 上取得的进展继续创造新的突破。这一希望变成现实的速度，远远超出了我们敢于梦想的程度。仅仅十二个月后，已有超过 50 万研究人员使用过 AlphaFold，并将其用于加速解决从[塑料污染](https://unfolded.deepmind.com/stories/accelerating-the-fight-against-plastic-pollution)到[抗生素耐药性](https://unfolded.deepmind.com/stories/this-could-accelerate-drug-discovery-in-a-way-that-weve-never-seen-before)等重要现实问题的研究。

今天，我非常激动地分享这段旅程的下一阶段。在与 EMBL 欧洲生物信息学研究所（EMBL-EBI）的合作下，我们现在正在发布科学界已知的几乎所有已编目蛋白质的预测结构，这将使 [AlphaFold DB](https://alphafold.ebi.ac.uk/) **扩展超过 200 倍——从近 100 万个结构增加到超过 2 亿个结构**，有望极大地加深我们对生物学的理解。

![一张按比例绘制的圆形图表，标题为"蛋白质结构数量"，展示了一个巨大的蓝色圆圈，代表"今日的 AlphaFold DB"（超过 2 亿个结构），与之对比的是一个很小的浅蓝色圆圈，代表"以前的 AlphaFold DB"（约 100 万个结构），以及一个更小的紫色圆圈，代表"今日的实验结构（PDB）"（19 万个结构）。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62e144dd63664354fa10ac1f_AF_Announcement_Vis1202.svg)

此次更新包含植物、细菌、动物及其他生物的预测结构，为研究人员利用 AlphaFold 推进可持续性、粮食不安全和被忽视疾病等重要议题的工作开辟了许多新机会。

![一张按比例绘制的圆形图表，展示 AlphaFold DB 中所代表的物种数量，总数从约 1 万增加到约 100 万。图中以五个大实心圆代表当前数字（今日），以小得多的空心圆代表以前的数字（以前），五个类别分别是：动物（蓝色）、植物（青色）、细菌（紫色）、真菌（粉色）和其他（橙色）。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62e144cfbb3a8c07d55bfa5f_AF_Announcement_Vis2202.svg)

今天的更新意味着主蛋白质数据库 [UniProt](https://www.uniprot.org/) 上的大多数页面都将附带一个预测结构。所有超过 2 亿个结构也将可以通过 [Google Cloud Public Datasets](https://github.com/deepmind/alphafold/blob/main/afdb/README.md) 批量下载，让世界各地的科学家更容易使用 AlphaFold。

> AlphaFold 是生命科学中一项独一无二的重大进展，展现了 AI 的力量。确定一个蛋白质的三维结构过去往往需要数月甚至数年，现在只需几秒钟。AlphaFold 已经加速并促成了一批重大发现，包括破解核孔复合体的结构。随着这次新增的结构照亮了几乎整个蛋白质宇宙，我们可以期待每天都会有更多生物学谜团被解开。

Eric Topol

斯克里普斯转化研究所（Scripps Research Translational Institute）创始人兼所长

## AlphaFold 迄今的影响

在 AlphaFold 首次发布十二个月之际，回顾 AlphaFold 已经产生的惊人影响，以及我们为抵达今天这一里程碑所走过的漫长旅程，令人感慨万千。

对我们的团队而言，AlphaFold 的成功尤其令人欣慰，这既是因为它是我们迄今构建过的最复杂的 AI 系统，需要多项关键创新，也是因为它带来了最有意义的下游影响。通过证明 AI 能够以原子级的精度、大规模、在几分钟内准确预测蛋白质的形状，AlphaFold 不仅为一个 50 年的宏大挑战提供了解决方案，也成为我们创立理念的首个重大实证：人工智能可以极大地加速科学发现，进而推动人类进步。

我们开源了 AlphaFold 的代码，并在《自然》（Nature）上发表了两篇深度论文 [1, 2]，目前已被引用超过 4000 次。我们与全球领先的 EMBL-EBI [密切合作](https://unfolded.deepmind.com/stories/making-alphafolds-predictions-available-to-scientists-around-the-world)，设计了一个最能帮助生物学家访问和使用 AlphaFold 的工具，并共同发布了 AlphaFold DB——一个对所有人开放且免费的、可检索的数据库。在发布 AlphaFold 之前，本着我们[负责任地开拓](https://deepmind.google/models/gemini-robotics/on-device/)的一贯做法，我们征求了来自生物学研究、安全、伦理与安全领域的 30 多位专家的意见，帮助我们理解如何以最大化潜在收益、最小化潜在风险的方式与世界分享 AlphaFold 的成果。

迄今为止，来自 190 个国家的超过 50 万研究人员已访问 AlphaFold DB，查看了超过 200 万个结构。我们免费提供的结构还被整合进了其他公共数据集，如 Ensembl、UniProt 和 OpenTargets，数百万用户在日常工作中使用这些数据。

![一张信息图，标题为"出版物中引用的 AlphaFold 预测"，展示了六个三维蛋白质结构及简要说明：核孔复合体蛋白 Nup205、配子体表面蛋白 P45/48、CCR4-NOT 转录复合体亚基 9、冰核蛋白、F20H23.2 蛋白和卵黄蛋白原（Vitellogenin）。](https://lh3.googleusercontent.com/dUhtCvV4rOlQlxyonpvzXqIuPHmsqZ7zWrqauypSjIwnuLV0az3M8WON9o6lHS9TsP_oWIdzGqkqTImD-y2JEPeVt7ZeDP9NykLIxQcF41pBRKdo=w1440)

看到 AlphaFold 以如此之快的速度成为全世界成千上万实验室和大学中科学家们开展重要工作的必备工具，我们深感震撼。至于我们自己在 AlphaFold 上的工作，我们优先选择了我们认为能带来最大社会效益的应用，重点关注那些历史上资金不足或被忽视的领域。例如，我们[与](https://unfolded.deepmind.com/stories/accelerating-the-race-to-treat-a-deadly-parasitic-disease)[被忽视疾病药物研发倡议组织（Drugs for Neglected Diseases initiative，DNDi）](https://dndi.org/)合作，帮助他们推进研究，使其更接近找到治疗[利什曼病](https://en.wikipedia.org/wiki/Leishmaniasis)和[恰加斯病](https://en.wikipedia.org/wiki/Chagas_disease)等疾病的救命疗法——这些疾病对世界较贫困地区的人们影响尤为严重。我们还通过为[世界卫生组织](https://www.who.int/)确定为研究高优先级的生物创建结构预测，支持了[世界被忽视热带病日](https://worldntdday.org/)，帮助推进对[麻风病](https://en.wikipedia.org/wiki/Leprosy)和[血吸虫病](https://en.wikipedia.org/wiki/Schistosomiasis)等疾病的研究——这些疾病影响着全球超过 10 亿人的生活。

看到研究界以各种方式使用 AlphaFold——从[理解疾病](https://unfolded.deepmind.com/stories/accelerating-the-race-to-treat-a-deadly-parasitic-disease)、[保护蜜蜂](https://unfolded.deepmind.com/stories/it-took-me-two-days-to-do-something-that-could-have-taken-me-years)，到[破解生物学难题](http://unfolded.deepmind.com/stories/unlocking-the-nuclear-pore-complex)，再到[更深入地探究生命本身的起源](https://unfolded.deepmind.com/stories/for-me-alphafold-is-transformative)——这一切都令人深受鼓舞。

![](https://lh3.googleusercontent.com/idofVbVTMyIsuB-N8qDgmHSiXQU9QnQNYQcb4HfDXzr2287X7H2UysK8ZREnXK4qp0YB0G1pU4h_aMcXstYE5rd7K9fJI0G8YtnhI2jMre5UjdUnpQ=w1440-h810-n-nu)

由我们 AlphaFold 团队成员选出的其他令人印象深刻的例子包括：

## 一道生物学拼图，由 Kathryn Tunyasuvunakool 选出

在最近一期的《科学》杂志[特刊](https://www.science.org/doi/10.1126/science.add2210)中，多个研究小组描述了 AlphaFold 如何帮助他们拼合出核孔复合体——生物学中最令人头疼的谜题之一。这一巨型结构由数百个蛋白质部件组成，控制着进出细胞核的一切。借助现有实验方法揭示其轮廓，再利用 AlphaFold 预测来补全和解释那些不清晰的区域，其精巧的结构最终得以揭示。这种强大的组合如今正在实验室中成为常规做法，解锁新的科学发现，并展示了实验技术与计算技术如何协同工作。

[解锁核孔复合体](https://deepmind.google/blog/alphafold-unlocks-one-of-the-greatest-puzzles-in-biology/)

## 生物信息学的新世界，由 Richard Evans 选出

像 [Foldseek](https://www.biorxiv.org/content/10.1101/2022.02.07.479398v2) 和 [Dali](https://academic.oup.com/nar/advance-article/doi/10.1093/nar/gkac387/6591528?login=true) 这样的结构检索工具，让用户能够非常快速地搜索与给定蛋白质相似的条目。这可能成为从大型序列数据集中挖掘具有实用价值的蛋白质（例如那些能分解塑料的蛋白质）的第一步，也可能为蛋白质功能提供线索。数据库此次更新纳入超过 2 亿个预测结构，将进一步放大这种影响。

## 对人类健康的直接影响，由 John Jumper 选出

AlphaFold 已经对人类健康产生了重大而直接的影响。与[欧洲人类遗传学学会](https://www.eshg.org/index.php?id=home)研究人员的会面表明，AlphaFold 结构对于那些试图揭开罕见遗传病病因的生物学家和临床医生而言是多么重要。此外，AlphaFold 正通过帮助人们更好地理解可能成为药物靶点的新发现蛋白质、并协助科学家更快找到能与之结合的候选药物，从而[加速药物发现](https://unfolded.deepmind.com/stories/this-could-accelerate-drug-discovery-in-a-way-that-weve-never-seen-before)的进程。

> AlphaFold 几乎在一夜之间成为生物制药研究的重要工具，包括在 ROME Therapeutics 这里——它让我们能够预测暗基因组中从未被解析过的区域的蛋白质结构。AlphaFold 的速度和精度正在加速药物发现进程，而这仅仅是它对更快把新药送到患者手中这一影响的开始。

Rosana Kapeller

ROME Therapeutics 总裁兼 CEO、Nimbus Therapeutics 前 CSO

## 这仅仅是个开始

AlphaFold 将生物学带入了结构丰度（structural abundance）的时代，以数字速度解锁了科学探索。AlphaFold DB 就像蛋白质结构的"谷歌搜索"，让研究人员能够即时获取所研究蛋白质的预测模型，从而集中精力、加快实验工作。从[对抗疾病](https://www.mdpi.com/2073-4409/11/10/1649/htm)到[开发疫苗](https://www.biorxiv.org/content/10.1101/2022.05.24.493318v1.full)，AlphaFold 已经在应对一些最严峻的全球挑战方面取得了令人瞩目的进展，而这只是我们在未来几年将开始看到的影响的开端。我们希望这个扩展后的数据库能帮助更多科学家开展工作，并开辟全新的科学探索途径，例如宏蛋白质组学（metaproteomics）。

在 DeepMind，我们正在许多领域进行大量投入，努力兑现所有这些潜力，包括：与我们 Alphabet 的新姊妹公司 [Isomorphic Labs](https://www.isomorphiclabs.com/) 合作，以 AI 优先的方法从第一性原理出发重新构想整个药物发现过程；在著名的[弗朗西斯·克里克研究所（Francis Crick Institute）](https://www.crick.ac.uk/)[建立湿实验室](https://www.crick.ac.uk/news/2022-07-06_the-francis-crick-institute-and-deepmind-join-forces-to-apply-machine-learning-to-biology)，以加强 AI 与实验技术之间的联系，推进对生物学（包括蛋白质设计和基因组学）的理解；以及扩充我们的 [AI for Science](https://www.deepmind.com/about/science) 团队，进一步加速基础生物学研究的进展，并将 AI 应用于[气候科学](https://www.nature.com/articles/s41586-021-03854-z)、[量子化学](https://www.science.org/stoken/author-tokens/ST-218/full)和[核聚变](https://www.nature.com/articles/s41586-021-04301-9)等其他迷人而重要的科学挑战。

AlphaFold 是未来的一瞥，展示了将计算与 AI 方法应用于生物学可能实现的前景。从根本上说，生物学可以被看作一个信息处理系统，尽管它是一个极其复杂且充满涌现性的系统。正如数学是物理学的完美描述语言一样，我们相信 AI 或许正是应对生物学动态复杂性的恰当技术。AlphaFold 是这一理念的重要首个实证，也预示着未来还有更多成果。作为"数字生物学"这一新兴领域的开拓者，我们很高兴看到 AI 的巨大潜力开始显现，成为人类推进科学发现、理解生命基本机制的最有用工具之一。
