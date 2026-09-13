---
title: "一份帮助精准定位疾病成因的基因突变目录"
title_en: "A catalogue of genetic mutations to help pinpoint the cause of diseases"
source: https://deepmind.google/blog/a-catalogue-of-genetic-mutations-to-help-pinpoint-the-cause-of-diseases/
site: deepmind
date: 2023-09-19
crawled: 2026-09-13
translated: 2026-09-13
---

# 一份帮助精准定位疾病成因的基因突变目录

> 原文：[A catalogue of genetic mutations to help pinpoint the cause of diseases](https://deepmind.google/blog/a-catalogue-of-genetic-mutations-to-help-pinpoint-the-cause-of-diseases/) · Google DeepMind

新 AI 工具对 7100 万个「错义」突变的效应进行分类

揭示疾病的根源是人类遗传学最大的挑战之一。面对数以百万计的可能突变和有限的实验数据，哪些突变可能致病在很大程度上仍是谜团。这一知识对更快的诊断和开发挽救生命的疗法至关重要。

今天，我们发布了一份[「错义」突变目录](https://zenodo.org/record/8360242)，研究人员可以在其中进一步了解这些突变可能产生的影响。错义变异（missense variants）是可以影响人类蛋白质功能的基因突变。在某些情况下，它们可能导致囊性纤维化、镰状细胞贫血或癌症等疾病。

这份 AlphaMissense 目录是使用 AlphaMissense——我们的新型 AI 模型，用于对错义变异进行分类——开发的。在发表于《科学》（Science）的一篇[论文](https://www.science.org/doi/10.1126/science.adg7492)中，我们展示了它把 7100 万个可能的错义变异中的 89% 归类为「可能致病」或「可能良性」。相比之下，此前只有 0.1% 经过人类专家确认。

能够准确预测变异效应的 AI 工具，有力量加速从分子生物学到临床与统计遗传学各领域的研究。[揭示致病突变的实验](https://genomebiology.biomedcentral.com/articles/10.1186/s13059-023-02986-x)既昂贵又费时——每种蛋白质都是独一无二的，每个实验都必须单独设计，可能耗时数月。借助 AI 预测，研究人员可以一次性预览数千种蛋白质的结果，这有助于优先分配资源并加速更复杂的研究。

我们已把全部预测免费开放给商业和研究用途，并开源了 [AlphaMissense 的模型代码](https://github.com/deepmind/alphamissense)。

![一张可视化图，比较对全部 7100 万个人类错义变异的预测。上方的饼图显示 AlphaMissense 的预测：57% 可能良性（蓝色）、32% 可能致病（粉色）、11% 不确定（灰色）。下方的图显示人类注释：约 6% 在人类中被观察到（深蓝色圆），约 0.1% 经过人类专家确认（其中一个小紫色圆），仅占总变异的一小部分。](https://lh3.googleusercontent.com/sbPsonVn4kyy5ZQ3kFmJ0BQb1jIolWkueQwpcUuIKDxemcFlLAQFLl_NWr2mbJsSZdCLVSNjqQBl9CkWebx-Q9qc7GsdWsfYu3W4naAu_B0OMawz=w1440)

AlphaMissense 预测了全部 7100 万个可能错义变异的致病性。它对其中 89% 进行了分类——预测 57% 可能为良性，32% 可能为致病。

## 什么是错义变异？

错义变异是 DNA 上的单个字母替换，导致蛋白质中一个不同的氨基酸。如果把 DNA 想象成一门语言，换掉一个字母可能改变一个词，并彻底改变一个句子的含义。在这里，替换改变了被翻译的氨基酸，从而可能影响蛋白质的功能。

普通人携带[超过 9000 个错义变异](https://www.nature.com/articles/s41586-021-04103-z/tables/1)。大多数是良性的，几乎没有影响，但另一些是致病的，可能严重破坏蛋白质功能。错义变异可用于罕见遗传病的诊断——在这种情况下，少数甚至单个错义变异就可能直接致病。它们对研究复杂疾病也很重要，比如 2 型糖尿病，它可能由许多不同类型的基因变化共同导致。

对错义变异进行分类是理解哪些蛋白质变化可能致病的重要一步。在已经在人类中观察到的 400 多万个错义变异中，只有 2% 被专家标注为致病或良性，约占全部 7100 万个可能错义变异的 0.1%。其余的由于缺乏关于其影响的实验或临床数据，被视为「意义未明变异」。借助 AlphaMissense，我们如今获得了迄今最清晰的图景：使用一个在已知致病变异目录上达到 90% 精确率的阈值，对 89% 的变异进行了分类。

## 致病还是良性：AlphaMissense 如何分类变异

AlphaMissense 以我们的突破性模型 [AlphaFold](https://www.deepmind.com/research/highlighted-research/alphafold) 为基础——后者从氨基酸序列预测了科学界已知几乎所有蛋白质的结构。我们改造后的模型可以预测改变蛋白质单个氨基酸的错义变异的致病性。

为了训练 AlphaMissense，我们用区分「在人类及近缘灵长类群体中观察到的变异」的标签对 AlphaFold 进行了微调。常见变异被视为良性，从未见过的变异被视为致病。AlphaMissense 并不预测突变后蛋白质结构的改变或对蛋白质稳定性的其他影响。相反，它利用相关蛋白质序列的数据库和变异的结构情境，生成一个介于 0 和 1 之间的分数，大致评定一个变异致病的可能性。这一连续分数让用户可以按照自己的精度要求选择阈值，把变异分类为致病或良性。

![示意图展示 AlphaMissense 的工作流程。在「Input（输入）」下，参考 DNA 密码子（CAG）和蛋白质氨基酸（Q）突变为错义变异（CGG 和 R）。在「AlphaMissense」下，该输入通过「1. Structure context（结构情境）」和「2. Protein language modeling（蛋白质语言建模）」进行处理。在「Output（输出）」下，AlphaMissense 预测一个 0 到 1 的致病性分数，把变异分类为致病（粉色，接近 1）、不确定（灰色）或良性（蓝色，接近 0）。](https://lh3.googleusercontent.com/g3tJ2fMpu0Zn1KBxI_Z1bVJ_F7b6S4kp-oYSDfFEc4GYwC4cO0PMl5IoOwjvEMCOWeULbFjbHhuTH2ccb0rNbvSimX2I-dwNR9Gl_mctAlW5hqov=w1440)

AlphaMissense 如何分类人类错义变异的示意图。输入一个错义变异，AI 系统为其打分，判定为致病或可能良性。AlphaMissense 结合结构情境与蛋白质语言建模，并在人类和灵长类变异群体频率数据库上进行微调。

AlphaMissense 在广泛的遗传学与实验基准上实现了最先进的预测，而所有这些都无需在此类数据上显式训练。在用于分类来自 ClinVar（一个记录人类变异与疾病关系的公共档案库）的变异时，我们的工具优于其他计算方法。我们的模型也是预测实验室结果最准确的方法，这表明它与不同的致病性度量方式相一致。

![两张水平柱状图，比较 AlphaMissense 与其他计算方法的表现。左图为 ClinVar 分类（auROC），AlphaMissense 以超过 0.9 的分数优于其他模型。右图为跨 25 种蛋白质的实验测定（平均 Spearman 相关），AlphaMissense 再次取得最高分，接近 0.5。](https://lh3.googleusercontent.com/cxViWkcfi2AVD3dhVQEdBjJ-zzFU4ToCyfS8SD5U0iNpwgjSedQ3icOpwTJ5Zs2VrTHfGpa7A0KBFfEGLRMyJHsNPDODmj-wpwzdanE9GH-nOMHkg3A=w1440)

**AlphaMissense 在预测错义变异效应上优于其他计算方法。**
**左：** 比较 AlphaMissense 与其他方法在分类 ClinVar 公共档案库变异上的表现。以灰色显示的方法曾直接在 ClinVar 上训练，它们在此基准上的表现可能被高估，因为其部分训练变异包含在这个测试集中。
**右：** 比较 AlphaMissense 与其他方法在预测生物学实验测量值上的表现图。

## 构建社区资源

AlphaMissense 建立在 AlphaFold 之上，以增进世界对蛋白质的理解。一年前，我们发布了用 AlphaFold 预测的 [2 亿个蛋白质结构](https://www.deepmind.com/blog/alphafold-reveals-the-structure-of-the-protein-universe)——它正在帮助全球数百万科学家加速研究、为新的发现铺路。我们期待看到 AlphaMissense 如何帮助解决基因组学核心乃至整个生物科学中的开放问题。

我们已把 AlphaMissense 的预测免费开放给商业界和科学界。我们还在与 EMBL-EBI 合作，通过 [Ensembl Variant Effect Predictor](https://www.ensembl.org/info/docs/tools/vep/script/vep_plugins.html#alphamissense) 让这些预测更易于使用。

除了我们的错义突变查询表，我们还分享了对超过 19,000 个人类蛋白质全部 2.16 亿种可能的单氨基酸序列替换的扩展预测。我们还为每个基因提供了平均预测值，它类似于衡量一个基因的演化约束——这表明该基因对生物体存活有多重要。

![两幅按 AlphaMissense 致病性预测着色的 3D 蛋白质结构可视化图，红色表示可能致病的区域，蓝色表示可能良性的区域。左侧是血红蛋白亚基 β（HBB）蛋白，小球标出变异位置；右侧是极其复杂的囊性纤维化跨膜传导调节蛋白（CFTR）结构。](https://lh3.googleusercontent.com/Dm6KiKU9UFGlJ153Ii1zKWtBEGDKU79p1qN4gZqMJUnfcTPmfgxLDzeBpt-p3uIggSw038EKx6qyeEiM7JujpFgj9_OrPfAxgAtFTzGJZ76iOmQK3w=w1440)

AlphaMissense 预测叠加在 AlphaFold 预测结构上的示例（红色=预测为致病，蓝色=预测为良性，灰色=不确定）。红点代表已知的致病错义变异，蓝点代表来自 ClinVar 数据库的已知良性变异。
**左：** HBB 蛋白。该蛋白的变异可导致镰状细胞贫血。
**右：** CFTR 蛋白。该蛋白的变异可导致囊性纤维化。

## 加速遗传疾病研究

把这项研究转化为应用的关键一步是与科学界合作。我们一直与 Genomics England 合作，探索这些预测如何帮助研究罕见遗传病的遗传学基础。Genomics England 将 AlphaMissense 的发现与此前与人类参与者共同汇总的变异致病性数据进行了交叉比对。他们的评估确认了我们的预测准确且一致，为 AlphaMissense 提供了另一个真实世界的基准。

虽然我们的预测并非设计为直接用于临床——而且应结合其他证据来源加以解读——这项工作有潜力改进罕见遗传病的诊断，并帮助发现新的致病基因。

归根结底，我们希望 AlphaMissense 与其他工具一起，能让研究人员更好地理解疾病，并开发新的挽救生命的疗法。

了解更多关于 AlphaMissense 的信息：

[阅读我们发表于《科学》的论文](https://www.science.org/stoken/author-tokens/ST-1429/full)[Ensembl Variant Effect Predictor 插件](https://www.ensembl.org/info/docs/tools/vep/script/vep_plugins.html#alphamissense)[下载 AlphaMissense 代码](https://github.com/google-deepmind/alphamissense)

**说明**

\* 自 2024 年 3 月 13 日起，AlphaMissense 预测以 [CC BY v.4](https://creativecommons.org/licenses/by/4.0/legalcode) 许可证提供，从而取消了此前仅限非商业用途的限制。请参阅[已发布数据库](https://console.cloud.google.com/storage/browser/dm_alphamissense)和 [Zenodo](https://zenodo.org/records/10813168) 了解更多获取信息。

我们感谢 Juanita Bawagan、Jess Valdez、Katie McAtackney、Kathryn Seager 和 Hollie Dobson 在文字与图表方面的帮助。我们也感谢外部合作伙伴 Genomics England 和 EMBL-EBI 的持续支持。这项工作有赖于以下共同作者的贡献：Guido Novati、Joshua Pan、Clare Bycroft、Akvilė Žemgulytė、Taylor Applebaum、Alexander Pritzel、Lai Hong Wong、Michal Zielinski、Tobias Sargeant、Rosalia G. Schneider、Andrew W. Senior、John Jumper、Demis Hassabis（德米斯·哈萨比斯）、Pushmeet Kohli。我们还要感谢 Kathryn Tunyasuvunakool、Rob Fergus、Eliseo Papa、David La、Zachary Wu、Sara-Jane Dunn、Kyle R. Taylor、Natasha Latysheva、Hamish Tomlinson、Augustin Žídek、Roz Onions、Mira Lutfi、Jon Small、Molly Beck、Annette Obika、Hannah Gladman、Folake Abu、Alyssa Pierce、James Tam、Q Green、Meera Last、Tharindi Hapuarachchi 以及更广大的 Google DeepMind 团队的支持、帮助与反馈。
