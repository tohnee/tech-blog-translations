---
title: "AlphaGenome：更好地理解基因组的 AI"
title_en: "AlphaGenome: AI for better understanding the genome"
source: https://deepmind.google/blog/alphagenome-ai-for-better-understanding-the-genome/
site: deepmind
date: 2025-06-25
crawled: 2026-09-13
translated: 2026-09-13
---

# AlphaGenome：更好地理解基因组的 AI

> 原文：[AlphaGenome: AI for better understanding the genome](https://deepmind.google/blog/alphagenome-ai-for-better-understanding-the-genome/) · Google DeepMind

介绍一个新的统一 DNA 序列模型，它推动了调控变异效应预测的进步，并有望为基因组功能带来新的认识——现已通过 API 提供。

**2026 年 1 月更新：**这项研究已发表于 Nature。你可以[在这里](https://www.nature.com/articles/s41586-025-10014-0)阅读完整论文，并[在这里](https://github.com/google-deepmind/alphagenome_research)获取模型。

基因组是我们的细胞说明书。它是指导生物体几乎每个方面的完整 DNA 集合——从外观和功能到生长和繁殖。基因组 DNA 序列中的微小变异可以改变生物体对环境的反应或对疾病的易感性。但破译基因组的指令如何在分子层面被读取——以及一个微小的 DNA 变异发生时会发生什么——仍然是生物学最大的谜团之一。

今天，我们推出 [AlphaGenome](https://storage.googleapis.com/deepmind-media/papers/alphagenome.pdf?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=)——一个新的人工智能（AI）工具，它能更全面、更准确地预测人类 DNA 序列中的单个变异或突变如何影响调控基因的众多生物过程。这得益于多项技术进展，其中包括让模型能够处理长 DNA 序列并输出高分辨率预测。

为推进科学研究，我们正通过 [AlphaGenome API](https://github.com/google-deepmind/alphagenome) 以预览版形式向非商业研究提供 AlphaGenome，并计划在未来发布该模型。

我们相信 AlphaGenome 可以成为科学界的宝贵资源，帮助科学家更好地理解基因组功能与疾病生物学，并最终推动新的生物学发现和新疗法的开发。

## AlphaGenome 的工作原理

我们的 AlphaGenome 模型以一段长 DNA 序列作为输入——最长可达 100 万个字母（也称为碱基对）——并预测表征其调控活动的数千种分子性质。它还可以通过比较突变序列与未突变序列的预测，为遗传变异或突变的影响打分。

被预测的性质包括：在不同细胞类型和组织中基因的起始与终止位置、它们被剪接的位置、产生的 RNA 数量，以及哪些 DNA 碱基是可及的、彼此靠近的或与特定蛋白质结合的。训练数据来自 [ENCODE](http://encodeproject.org/)、[GTEx](https://www.gtexportal.org/)、[4D Nucleome](https://4dnucleome.org/) 和 [FANTOM5](https://fantom.gsc.riken.jp/5/) 等大型公共联盟，这些联盟以实验方式测量了这些性质，覆盖数百种人类和小鼠细胞类型与组织中基因调控的重要模态。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![你的浏览器不支持视频标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

动画展示 AlphaGenome 以一百万个 DNA 字母作为输入，预测不同组织和细胞类型中的多种分子性质。

AlphaGenome 的架构首先用卷积层检测基因组序列中的短模式，用 Transformer 在序列所有位置之间传递信息，最后用一系列层把检测到的模式转换为针对不同模态的预测。在训练期间，这一计算分布在多个互连的张量处理单元（TPU）上，针对单条序列进行。

这个模型构建于我们之前的基因组学模型 [Enformer](https://deepmind.google/discover/blog/predicting-gene-expression-with-ai/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=) 之上，并与 [AlphaMissense](https://deepmind.google/discover/blog/a-catalogue-of-genetic-mutations-to-help-pinpoint-the-cause-of-diseases/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=) 互补——后者专注于对蛋白质编码区内的变异效应进行分类。这些区域占基因组的 2%。其余 98% 称为非编码区，对编排基因活动至关重要，并包含许多与疾病相关的变异。AlphaGenome 为解读这些广袤序列及其中的变异提供了新的视角。

## AlphaGenome 的独特之处

与现有的 DNA 序列模型相比，AlphaGenome 提供了若干独特功能：

### 高分辨率的长序列上下文

我们的模型可分析多达 100 万个 DNA 字母，并以单个字母的分辨率进行预测。长序列上下文对于覆盖远距离调控基因的区域非常重要，而碱基级分辨率对于捕捉细粒度的生物学细节非常重要。

以往的模型不得不在序列长度和分辨率之间取舍，这限制了它们能够联合建模和准确预测的模态范围。我们的技术进步解决了这一局限，而无需显著增加训练资源——训练单个 AlphaGenome 模型（不含蒸馏）耗时四小时，所用算力预算只有训练最初 Enformer 模型的一半。

### 全面的多模态预测

通过为长输入序列解锁高分辨率预测，AlphaGenome 能够预测最多样化的模态范围。由此，AlphaGenome 为科学家提供了关于基因调控复杂步骤的更全面的信息。

### 高效的变异打分

除了预测多样的分子性质外，AlphaGenome 还能在一秒内高效地为遗传变异对所有这些性质的影响打分。它通过对比突变序列与未突变序列的预测来实现这一点，并针对不同模态采用不同方法高效地总结这一对比。

### 新颖的剪接位点建模

许多罕见遗传病，如脊髓性肌萎缩症和某些形式的囊性纤维化，可能由 RNA 剪接错误引起——剪接是把 RNA 分子的部分片段移除（「剪接出去」）并把余下的末端重新连接的过程。AlphaGenome 首次能够直接从序列显式建模这些剪接位点的位置与表达水平，为遗传变异对 RNA 剪接的影响提供更深入的洞见。

## 在各类基准测试中的领先表现

AlphaGenome 在广泛的基因组预测基准测试中达到业界领先水平，例如预测 DNA 分子的哪些部分会彼此靠近、某个遗传变异会提高还是降低某个基因的表达，或者它是否会改变基因的剪接模式。

![两张横向柱状图，展示 AlphaGenome 在不同模态下的相对性能提升。左图标题为「序列任务」（Sequence tasks），提升幅度从组蛋白修饰的 +3.1% 到 RNA 表达的 +17.4% 不等。右图标题为「变异效应任务」（Variant effect tasks），提升幅度从转录因子结合因果性的 +6.0% 到 RNA 表达方向的 +25.5% 不等。](https://lh3.googleusercontent.com/T3o3tze7lwqmp5QwIKSujpZTtKpKEXu_cLD59W2rYHlnIESVvcDAUlaS5LrYkqHciA9RNdPSLafTZ2KPSuUzZ8M_kKOIZSxR38vGbCWWDPML_BgcJ_I=w1440-h810-n-nu)

柱状图展示 AlphaGenome 在选定的 DNA 序列与变异效应任务上相对于各类别当前最佳方法结果的相对提升。

在为单条 DNA 序列生成预测时，AlphaGenome 在 24 项评测中的 22 项上超越了最佳外部模型。在预测变异的调控效应时，它在 26 项评测中的 24 项上持平或超越了表现最佳的外部模型。

这一对比包括为单个任务专门设计的模型。AlphaGenome 是唯一能够联合预测所有被评估模态的模型，凸显了其通用性。更多内容请阅读[我们的预印本](https://storage.googleapis.com/deepmind-media/papers/alphagenome.pdf?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=)。

## 统一模型的好处

AlphaGenome 的通用性让科学家只需一次 API 调用，就能同时探索一个变异对多种模态的影响。这意味着科学家可以更快速地生成和检验假设，而不必使用多个模型来研究不同的模态。

此外，AlphaGenome 的强劲表现表明它学到了基因调控语境下 DNA 序列相对通用的表征。这使它成为更广泛的社区可以依托的坚实基础。模型完全发布后，科学家将能够在自己的数据集上适配和微调它，以更好地解决各自独特的研究问题。

最后，这一方法为未来提供了灵活、可扩展的架构。通过扩展训练数据，AlphaGenome 的能力可以得到延伸，以获得更好的性能、覆盖更多物种，或纳入更多模态，使模型更加全面。

> 这是该领域的一个里程碑。我们首次拥有了一个统一长程上下文、碱基级精度和全谱系基因组任务业界领先表现的单一模型。

Caleb Lareau 博士

纪念斯隆-凯特琳癌症中心

## 一个强大的研究工具

AlphaGenome 的预测能力可以助力多条研究路径：

1. **疾病理解：**通过更准确地预测遗传破坏，AlphaGenome 可以帮助研究者更精确地定位疾病的潜在原因，更好地解读与某些性状相关变异的功能影响，并有可能发现新的治疗靶点。我们认为该模型特别适合研究可能产生较大影响的罕见变异，例如导致罕见孟德尔疾病的变异。
2. **合成生物学：**它的预测可用于指导设计具有特定调控功能的合成 DNA——例如，只在神经细胞中激活某个基因，而在肌肉细胞中不激活。
3. **基础研究：**它可以协助绘制基因组关键功能元件的图谱并定义其作用，识别调控特定细胞类型功能最核心的 DNA 指令，从而加速我们对基因组的理解。

例如，我们用 AlphaGenome 研究了一个癌症相关突变的潜在机制。在一项针对 T 细胞急性淋巴细胞白血病（T-ALL）患者的已有[研究](https://www.science.org/doi/10.1126/science.1259037)中，研究人员在基因组的特定位置观察到了突变。利用 AlphaGenome，我们预测这些突变会通过引入一个 MYB DNA 结合基序来激活附近的基因 [TAL1](https://alphafold.ebi.ac.uk/entry/P17542?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=)，这与已知的疾病机制相吻合，凸显了 AlphaGenome 将特定非编码变异与疾病基因关联起来的能力。

> AlphaGenome 将是这个领域的一个强大工具。判断不同非编码变异的相关性可能极具挑战，尤其是要大规模地进行。这个工具将提供拼图中关键的一块，帮助我们建立更好的联系，理解癌症等疾病。

Marc Mansour 教授

伦敦大学学院

## 当前的局限

AlphaGenome 迈出了重要一步，但也必须承认它目前的局限。

与其他基于序列的模型一样，准确捕捉相距非常遥远的调控元件（例如超过 10 万个 DNA 字母之外的元件）的影响，仍然是一个持续的挑战。未来工作的另一个优先事项，是进一步增强模型捕捉细胞与组织特异性模式的能力。

我们尚未针对个人基因组预测来设计或验证 AlphaGenome——这是 AI 模型的一个已知难题。我们更专注于刻画它在单个遗传变异上的表现。而且，虽然 AlphaGenome 可以预测分子层面的结果，但它无法完整呈现遗传变异如何导致复杂性状或疾病。后者往往涉及更广泛的生物过程，例如发育和环境因素，超出了我们模型的直接范围。

我们正在持续改进模型，并收集反馈，以帮助我们弥补这些缺口。

## 让社区释放 AlphaGenome 的潜力

AlphaGenome 现已通过我们的 [AlphaGenome API](https://github.com/google-deepmind/alphagenome) 供非商业用途使用。请注意，我们模型的预测仅用于研究用途，并未针对直接的临床目的进行设计或验证。

我们邀请全球的研究者交流 AlphaGenome 的潜在用例，并通过[社区论坛](https://www.alphagenomecommunity.com/)提问或分享反馈。

我们希望 AlphaGenome 能成为更好理解基因组的重要工具，并致力于与学术界、产业界和政府组织的外部专家并肩工作，确保 AlphaGenome 造福尽可能多的人。

与更广泛科学社区的集体努力一道，我们希望它能加深我们对 DNA 序列所编码的复杂细胞过程及变异效应的理解，并推动基因组学和医疗健康领域激动人心的新发现。

进一步了解 AlphaGenome

[在 Nature 上阅读我们的论文](https://www.nature.com/articles/s41586-025-10014-0)[使用 AlphaGenome API](https://github.com/google-deepmind/alphagenome)[加入社区论坛](https://www.alphagenomecommunity.com/)[登记商业使用意向](https://docs.google.com/forms/d/e/1FAIpQLSd0iyoC0Mo1DGB1uiuECBB8OErYzSCNYocy6hZ7nbsCd_TXhQ/viewform)

**致谢**

我们感谢 Juanita Bawagan、Arielle Bier、Stephanie Booth、Irina Andronic、Armin Senoner、Dhavanthi Hariharan、Rob Ashley、Agata Laydon 和 Kathryn Tunyasuvunakool 在文字与图表上的帮助。

这项工作有赖于 AlphaGenome 合著者的贡献：Žiga Avsec、Natasha Latysheva、Jun Cheng、Guido Novati、Kyle R. Taylor、Tom Ward、Clare Bycroft、Lauren Nicolaisen、Eirini Arvaniti、Joshua Pan、Raina Thomas、Vincent Dutordoir、Matteo Perino、Soham De、Alexander Karollus、Adam Gayoso、Toby Sargeant、Anne Mottram、Lai Hong Wong、Pavol Drotár、Adam Kosiorek、Andrew Senior、Richard Tanburn、Taylor Applebaum、Souradeep Basu、Demis Hassabis（德米斯·哈萨比斯）和 Pushmeet Kohli。

我们还要感谢 Dhavanthi Hariharan、Charlie Taylor、Ottavia Bertolli、Yannis Assael、Alex Botev、Anna Trostanetski、Lucas Tenório、Victoria Johnston、Richard Green、Kathryn Tunyasuvunakool、Molly Beck、Uchechi Okereke、Rachael Tremlett、Sarah Chakera、Ibrahim I. Taskiran、Andreea-Alexandra Muşat、Raiyan Khan、Ren Yi 以及 Google DeepMind 更大的团队的支持、帮助与反馈。
