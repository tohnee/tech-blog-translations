---
title: "Aeneas 改变历史学家连接过去的方式"
title_en: "Aeneas transforms how historians connect the past"
source: https://deepmind.google/blog/aeneas-transforms-how-historians-connect-the-past/
site: deepmind
date: 2025-07-23
crawled: 2026-09-13
translated: 2026-09-13
---

# Aeneas 改变历史学家连接过去的方式

> 原文：[Aeneas transforms how historians connect the past](https://deepmind.google/blog/aeneas-transforms-how-historians-connect-the-past/) · Google DeepMind

介绍首个用于古代铭文情境化的模型，旨在帮助历史学家更好地解读、断代和修复残缺的文本。

在罗马世界，文字无处不在——从帝国纪念碑到日常物品，一切都被镌刻其上。从政治涂鸦、情诗和墓志铭，到商业交易、生日请柬和咒语，铭文为现代历史学家提供了窥见罗马世界日常生活多样性的丰富洞见。

这些文本往往残缺不全、风化剥蚀，或是被人刻意损毁。若没有情境信息，修复、断代和定位它们几乎是不可能的，尤其是在比对相似铭文的时候。

今天，我们在《自然》（Nature）上发表了一篇[论文](https://www.nature.com/articles/s41586-025-09292-5)，介绍 [Aeneas](http://predictingthepast.com/?utm_source=&utm_medium=&utm_campaign=&utm_content=)——首个用于古代铭文情境化的人工智能（AI）模型。

在处理古代铭文时，历史学家传统上依靠自身的专业知识和专门资源来寻找「平行文本（parallels）」——即在措辞、句法、标准化套语或出土地上存在相似性的文本。

Aeneas 极大地加速了这项复杂而耗时的工作。它对数千篇拉丁铭文进行推理，能在数秒内检索出文本与情境上的平行文本，让历史学家得以在模型发现的基础上进行解读与延伸。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![你的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

我们的模型还可以适配到其他古代语言、文字和载体——从纸草文献到钱币——扩展其能力，帮助在更广泛的历史证据之间建立关联。

我们与诺丁汉大学共同开发了 Aeneas，并与华威大学、牛津大学以及雅典经济与商业大学（AUEB）的研究人员合作。这项工作是一个更宏大计划的一部分：探索生成式 AI 如何帮助历史学家更好地大规模识别与解读平行文本。

我们希望这项研究能惠及尽可能多的人，因此我们在 [predictingthepast.com](http://predictingthepast.com/?utm_source=&utm_medium=&utm_campaign=&utm_content=) 上向研究人员、学生、教育工作者、博物馆专业人士等免费提供 Aeneas 的交互版本。为支持后续研究，我们还将[代码和数据集](http://github.com/google-deepmind/predictingthepast)开源。

## Aeneas 的先进能力

Aeneas 以希腊罗马神话中的流浪英雄命名，它建立在我们早前利用 AI 修复、断代和定位古希腊铭文的工作 [Ithaca](https://deepmind.google/discover/blog/predicting-the-past-with-ithaca/) 之上。

Aeneas 更进一步：帮助历史学家解读文本并将其情境化，让孤立的残片获得意义，得出更丰富的结论，并拼合出对古代历史更好的理解。

我们模型的先进能力包括：

- **平行文本检索：** 它在庞大的拉丁铭文集合中检索平行文本。通过把每篇文本转化为一种「历史指纹」，Aeneas 能够识别出深层的关联，帮助历史学家把铭文置于更宏大的历史脉络之中。
- **处理多模态输入：** Aeneas 是首个使用多模态输入判定文本地理出处的模型。它同时分析文本和视觉信息，比如铭文的图像。
- **修复未知长度的空缺：** Aeneas 首次能够修复缺失长度未知的文本空缺。这使得它成为历史学家处理严重受损材料的更通用工具。
- **最先进的性能：** Aeneas 在修复受损文本以及预测其书写时间和地点方面树立了新的最先进基准。

![白色背景上一块深色、残缺的罗马青铜军事文凭，上面刻有拉丁文](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/bronze.gif)

一件来自撒丁岛、公元 113/14 年的青铜军事文凭修复动画（*CIL* XVI, 60）。

## Aeneas 的工作原理

Aeneas 是一个多模态生成式神经网络，它把铭文的文本和图像作为输入。为了训练 Aeneas，我们整理了一个庞大而可靠的数据集，借鉴了历史学家数十年构建数字化藏品的工作，尤其是[罗马铭文数据库](https://zenodo.org/records/3575495)（Epigraphic Database Roma，EDR）、[海德堡铭文数据库](https://zenodo.org/records/3575155)（Epigraphic Database Heidelberg，EDH）和[铭文数据库 Clauss Slaby](https://zenodo.org/records/7072337)（EDCS-ELT）。

我们对这些记录进行了清洗、统一和关联，形成了一个单一的机器可操作数据集，我们称之为[拉丁铭文数据集](http://github.com/google-deepmind/predictingthepast)（Latin Epigraphic Dataset，LED），包含来自整个古代罗马世界的超过 17.6 万篇拉丁铭文。

我们的模型使用基于 transformer 的解码器来处理铭文的文本输入。专门的网络使用文本完成字符修复和断代，而地理归属还会把铭文的图像作为输入。该解码器从 LED 中检索出相似的铭文，并按相关性排序。

对于每篇铭文，Aeneas 的情境化机制使用一种称为「嵌入（embeddings）」的技术检索平行文本列表——把每篇铭文的文本与情境信息编码为一种「历史指纹」，其中包含文本说了什么、使用什么语言、来自何时何地，以及它与其他铭文有何关联等细节。

![示意图展示 Aeneas 的技术架构，说明它如何通过 Torso 解码器、视觉网络（Vision network）和专门的任务头（Task Heads）处理多模态输入（受损的文本残片和铭文图像），生成诸如行省归属、日期分布、缺失文本修复以及从数据集中按相关性排序的情境平行文本列表等输出。](https://lh3.googleusercontent.com/zQP7-nljtyONJHitREu1Xf_HqL0EI2QvFf28LGKsfBZw4WTGoETM1uqNPSYea3rS7aA4WAgYgfwvueQZ8Rkj80Jt-zN9UXcnd3kwQuRlnRe5LHPoMSQ=w1440)

Aeneas 架构图，展示模型如何以文本和图像为输入，生成行省、日期和修复预测。

## 最先进的性能

如下方可视化所示，Aeneas 按书写日期对铭文进行分组的清晰度远高于其他同样在拉丁语上训练的通用模型。

![两张散点图，比较 Aeneas 与一个通用 LLM 在按日期对罗马铭文分组上的表现。Aeneas 的图呈现出按时间顺序排列、彼此分明的彩色数据点聚类，时间跨度从公元前 650 年到公元 800 年；而通用 LLM 的图则呈现出高度混杂、无组织的分布。](https://lh3.googleusercontent.com/_fZt8LFZ8UCtCkFlgKZN7af848HnOY4KrM77JsxPCCwZ7xEk-t4SRwtrgXOqWcNhK9Nh0UPd8tHFgjPJMIHNo0xO0ZYd-iPilNcbfFf8kgAClcjD-w=w1440)

一致流形逼近与投影（UMAP）可视化：对比 Aeneas 丰富的历史嵌入与通用大语言模型文本嵌入的时间归属表现。

Aeneas 修复受损铭文时，在最长十个字符的空缺上 Top-20 准确率为 73%。当修复长度未知时——这本身就是一项极具挑战性的任务——准确率也只降到 58%。它还能以可解释的方式呈现推理过程，提供显著性图（saliency map），高亮输入中影响其预测的部分。得益于对视觉数据的使用，我们的模型能以 72% 的准确率把铭文归属于 62 个古罗马行省之一。在断代方面，Aeneas 可以把文本的年代定位在历史学家给出的日期区间 13 年的范围之内。

## 观察历史争论的新透镜

为了检验 Aeneas 在一个正在进行中的研究争论上的能力，我们给了它一篇最著名的罗马铭文：*Res Gestae Divi Augusti*（《奥古斯都功德录》），即奥古斯都皇帝以第一人称记述自己功绩的文本。

历史学家对这篇铭文的断代长期争论不休。Aeneas 并没有预测单一的固定日期，而是生成了一个详细的可能日期分布，呈现出两个明显的峰值：一个较小的峰值在公元前 10-1 年前后，另一个更大、更确信的峰值在公元 10-20 年之间。这些结果以定量的方式同时捕捉了两种主流断代假说。

![《Res Gestae Divi Augusti》断代的概率分布图，蓝色的模型预测曲线与紫色的两大历史争论假说并列突出显示，模型预测峰值位于公元 15 年。](https://lh3.googleusercontent.com/7U-MZdGGrZHfsnyLWFmrBTxDohuDGJDTZfgDMgqAhVKQ8omHx5ti8l_gZywERPdLdyxw9N20e0SNmz6TiiV5hFgUD5BH2zXTua_EUXIjbzQsBmTa9Q=w1440)

直方图展示 Aeneas 对《Res Gestae》的时间归属预测，为围绕这篇著名铭文断代的学术争论建模。

Aeneas 的预测基于微妙的语言学特征和历史标记，比如文本中提到的官衔和纪念碑。通过把断代问题转化为一个建立在语言学与情境数据之上的概率估计，我们的模型为参与长期悬而未决的历史争论提供了一种全新的定量方式。

最重要的是，Aeneas 还检索出了许多与奥古斯都政治遗产相关的帝国法律文本平行段落，凸显了帝国意识形态如何在不同的载体与地理之间被复制传播。

## 以协作方式推进历史研究

为了评估 Aeneas 作为研究辅助工具的影响，我们开展了一项大规模的历史学家与 AI 协作研究。我们邀请了 23 位经常处理铭文的历史学家，使用 Aeneas 对一组文本进行修复、断代和定位。

我们的评估（汇总于下表）显示：当历史学家把 Aeneas 的情境信息与其对罗马铭文修复和归属的预测结合使用时，取得了最有效的结果。

![一张表格，汇总了不同方法的性能评估——人名学基线（Onomastics baseline）、历史学家、使用 Aeneas 平行文本的历史学家、同时使用 Aeneas 平行文本与预测的历史学家，以及单独使用 Aeneas——评估指标包括修复的字符错误率（CER）、行省准确率、日期预测偏差、历史学家信心、作为研究起点的潜力以及新增平行文本数量。结果表明，将历史学家与 Aeneas 的平行文本及预测相结合能取得最佳整体结果。](https://lh3.googleusercontent.com/lj_ZyKrAdWJHzI78rd2RV2NzRlV_QgurcQDyvlN30cNg9VJNnbPXIW8NKxHvPCWC9U-vGhsis39WQ3Oj2pn0J5zKMUgks3BeKt5TLTyhbNitH22g998=w1440)

表格展示历史学家在我们数据库测试集的 60 篇铭文上完成三项铭文学任务（修复、地理归属、断代）的表现。任务首先独立完成，然后借助 Aeneas 的平行文本信息，或同时使用平行文本与预测。

在我们的研究中，Aeneas 帮助历史学家发现了新的平行文本，并提升了他们处理复杂铭文学任务的信心。历史学家一致强调了 Aeneas 在加速其工作、扩展最相关平行铭文范围方面的价值。

> Aeneas 找到的平行文本彻底改变了我对这篇铭文的看法。它注意到了那些对修复文本和判定年代至关重要的细节。

我们研究中的匿名历史学家

## 分享工具，塑造未来

Aeneas 的设计目标是可以融入历史学家现有的研究工作流。通过把专家知识与机器学习相结合，它开启了一种协作流程，提供可解释的建议，作为历史探究的宝贵起点。

作为今天发布的一部分，我们将古希腊模型 [Ithaca](https://deepmind.google/discover/blog/predicting-the-past-with-ithaca/) 升级为由 Aeneas 驱动，加入情境化功能、未知长度修复能力，并整体提升了性能。

我们还共同设计了一份新的[教学大纲](https://www.robbewulgaert.be/education/predicting-the-past-aeneas)，用于在课堂中衔接技术技能与历史思维。该大纲与多项 AI 素养计划保持一致，包括欧盟委员会的[公民数字能力框架](https://publications.jrc.ec.europa.eu/repository/handle/JRC128415)（DigComp 2.2）、联合国教科文组织的[学生 AI 能力框架](https://www.unesco.org/en/articles/ai-competency-framework-students)，以及欧盟委员会与经济合作与发展组织（OECD）发布的 [AILit 框架](https://ailiteracyframework.org/about/)预览版。

Aeneas 团队将继续与各领域的专家合作，使用 Aeneas 帮助照亮我们的古代历史——敬请期待更多进展。

**了解更多关于 Aeneas 的信息**

[阅读我们的论文](https://www.nature.com/articles/s41586-025-09292-5)[试用 Aeneas](http://predictingthepast.com/)[获取代码和数据集](http://github.com/google-deepmind/predictingthepast)[阅读我们的意大利语版博客](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/aeneas-transforms-how-historians-connect-the-past/aeneas-transforms-how-historians-connect-the-past-italian-version.pdf)[阅读我们的希腊语版博客](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/aeneas-transforms-how-historians-connect-the-past/aeneas-transforms-how-historians-connect-the-past-greek-version.pdf)

**致谢**

本研究由 Yannis Assael 和 Thea Sommerschield 共同领导。

贡献者包括：Alison Cooley、Brendan Shillingford、John Pavlopoulos、Priyanka Suresh、Bailey Herms、Jonathan Prag、Alex Mullen 和 Shakir Mohamed。Aeneas 网页界面由 Justin Grayston、Benjamin Maynard 和 Nicholas Dietrich 开发，由 Google Cloud 提供支持。

教学大纲由比利时根特 Sint-Lievenscollege 的 Robbe Wulgaert 开发。
