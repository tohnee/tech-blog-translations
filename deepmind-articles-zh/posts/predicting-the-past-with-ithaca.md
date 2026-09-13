---
title: "用 Ithaca 预测过去"
title_en: "Predicting the past with Ithaca"
source: https://deepmind.google/blog/predicting-the-past-with-ithaca/
site: deepmind
date: 2022-03-09
crawled: 2026-09-13
translated: 2026-09-13
---

# 用 Ithaca 预测过去

> 原文：[Predicting the past with Ithaca](https://deepmind.google/blog/predicting-the-past-with-ithaca/) · Google DeepMind

通过 AI 与历史学家的协作，复原、定位并断代古代文本

人类书写的诞生标志着[历史学](https://en.wikipedia.org/wiki/History#History_and_prehistory)的开端，对我们理解过去的文明以及今天生活的世界至关重要。例如，2500 多年前，希腊人开始在石头、陶器和金属上书写，记录从租约、法律到历法、神谕的一切，为了解地中海地区提供了详尽的窗口。遗憾的是，这份记录并不完整。许多幸存的铭文在几个世纪里遭到损毁，或从原址被移走。此外，现代断代技术（如[放射性碳测年](https://en.wikipedia.org/wiki/Radiocarbon_dating)）无法用于这些材料，使得铭文的释读既困难又耗时。

秉承 [DeepMind 的使命](https://deepmind.com/about)——破解智能以推进科学与人类福祉——我们与[威尼斯大学人文学院（Ca' Foscari University of Venice）](https://www.unive.it/pag/27720/)、[牛津大学古典学部](https://www.classics.ox.ac.uk/)以及[雅典经济与商业大学信息学系](https://www.dept.aueb.gr/en/infotech-overview-en)合作，探索机器学习如何帮助历史学家更好地释读这些铭文——从而更丰富地理解古代历史，并开启 AI 与历史学家合作的潜力。

在今天发表于 Nature 的[论文](https://www.nature.com/articles/s41586-022-04448-z)中，我们共同推出了 Ithaca——首个能够复原受损铭文缺失文本、判断其原始出处、并帮助确定其创作年代的深度神经网络。Ithaca 得名于[《荷马史诗·奥德赛》](https://en.wikipedia.org/wiki/Odyssey)中的希腊岛屿，它建立并扩展了我们此前专注于文本复原的系统 [Pythia](https://deepmind.com/research/publications/2019/Restoring-ancient-text-using-deep-learning-a-case-study-on-Greek-epigraphy)。我们的评估显示，Ithaca 在复原受损文本上达到 62% 的准确率，在判断原始出处上达到 71% 的准确率，并且能把文本断代到距真实年代区间中点 30 年以内。历史学家已经用这个工具重新评估了希腊历史上的重要时期。

为了让研究成果广泛服务于研究人员、教育工作者、博物馆工作人员和其他人士，我们与 [Google Cloud](https://cloud.google.com/) 和 [Google Arts & Culture](https://artsandculture.google.com/) 合作，推出了[免费的 Ithaca 交互版本](https://ithaca.deepmind.com/)。为进一步助力研究，我们还将代码、预训练模型和一个交互式 Colaboratory 笔记本[开源](https://github.com/deepmind/ithaca)。

![一段动画，展示 AI 如何利用拼接后的石碑残片，预测缺失或已被毁坏的内容。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6231e47ba59f4a050e873f3a_Fig201animated.gif)

图 1。这方经复原的铭文（IG I3 4B）记录了一项关于雅典卫城的法令，年代为公元前 485/4 年。（CC BY-SA 3.0, WikiMedia）。

![Ithaca 神经网络架构图，展示希腊语输入文本中的字符和单词如何连同位置信息，经过一个带稀疏多头注意力的 Torso 模块处理，生成用于文本复原、地理归属和年代归属的输出。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6231e4946bcb81d92694d69a_Fig202.2.svg)

图 2。Ithaca 的架构。文本受损的部分用短横线"-"表示。这里我们人为损坏了字符"δημ."。在这些输入之下，Ithaca 复原了文本，并识别出文本的书写时间和地点。

## 协作式工具

Ithaca 在来自[帕卡德人文研究所（Packard Humanities Institute）](https://packhum.org/)的[最大的希腊铭文数字化数据集](https://inscriptions.packhum.org/)上训练。[自然语言处理](https://en.wikipedia.org/wiki/Natural_language_processing)模型通常以单词为单位训练，因为单词在句子中出现的顺序及其相互关系提供了额外的上下文和含义。例如，"很久很久以前"（once upon a time）比分开看的每个字符或单词承载更多意义。然而，历史学家想用 Ithaca 分析的许多铭文都已受损，常常缺失成段文字。为确保模型在面对这类铭文时仍然有效，我们同时以单词和单个字符作为输入进行训练。模型核心的稀疏自注意力机制并行评估这两种输入，使 Ithaca 能够按需评估铭文。

![一个界面，展示 Ithaca 对一方古希腊铭文的文本复原、地理归属和年代归属预测。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6231e4aed783c158e7bc03a1_Fig203.2.svg)

图 3。Ithaca 的输出。(a) 对一方雅典铭文（IG II2 116）中 6 个缺失字符（短横线）的复原预测。排名第一的复原结果（绿色）是正确的（συμμαχία，"同盟"）。注意排在后面的假设（ἐκκλησία，"公民大会"和 προξενία，"城邦与外邦人的协定"）以红色高亮，它们通常出现在雅典的政治法令中，体现出 Ithaca 对上下文的敏感性。(b) 一方来自阿莫尔戈斯岛（Amorgos）铭文（IG XII 7, 2）的地理归属。Ithaca 的首选预测正确，而最接近的预测都是相邻地区。(c) 一方来自提洛岛（Delos）铭文（IG XI 4, 579）的年代分布。真实年代区间为公元前 300-250 年（灰色）；Ithaca 的预测分布为黄色，均值在公元前 273 年（绿色）。

为了最大化 Ithaca 作为研究工具的价值，我们还创建了一系列可视化辅助，确保历史学家能够轻松解读 Ithaca 的结果：

- **复原假设**：Ithaca 为文本复原任务生成多个预测假设，供历史学家凭自身专业知识选择。
- **地理归属**：Ithaca 通过给出所有可能预测的概率分布来展示其不确定性——而不是只输出单一结果。它会返回 84 个古代区域的概率，代表其确信程度，并在地图上可视化这些结果，以揭示古代世界之间潜在的地理联系。
- **年代归属**：为文本断代时，Ithaca 会生成从公元前 800 年到公元 800 年每十年为一个刻度的预测日期分布。这能让历史学家可视化模型对特定年代区间的置信度，可能提供有价值的历史洞见。
- **显著性图**：为了向历史学家传达结果，Ithaca 采用了计算机视觉中常用的一种技术，识别哪些输入序列对预测贡献最大。输出以不同颜色强度高亮那些引导 Ithaca 对缺失文本、位置和日期做出预测的单词。

![顶部一行的输入文本有六个空白字符，用短横线表示。其下方，Ithaca 对每一行的相应字符进行复原。输出的译文为："诸神。Nikophemos 任执政官期间。雅典人与色萨利人缔结永世同盟。"](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6231e4cfc0dd671ee8e1dc1b_Fig204.2.svg)

图 4。这方文本（IG II2 116，雅典，公元前 361/0 年）记录了雅典人与色萨利人之间的一项同盟。借助显著性图，我们可以看到 Ithaca 在复原受损词"同盟"时"聚焦"于上下文关键单词"雅典人"和"色萨利人"。

## 参与史学争论

我们的实验评估展示了 Ithaca 的设计选择和可视化辅助如何让研究者更容易解读结果。与我们合作的专家历史学家单独复原古代文本时准确率为 25%，但使用 Ithaca 后，他们的表现提升到 72%，超越了模型单独的表现，展示了人机合作推进历史释读、为历史事件建立相对年代、乃至参与当下方法论争论的潜力。

例如，在苏格拉底、伯里克利等名人生活的年代所颁布的一系列重要[雅典法令](https://staff.mq.edu.au/teach/teaching-macquarie/ancient-history-for-schools/greece-resources/resources-for-year-12-ancient-greek-studies/three-bar-sigma)的确切年代，历史学家至今仍有分歧。这些法令长期以来被认为写于公元前 446/445 年之前，尽管新证据表明其年代应为公元前 420 年代。虽然这看起来是个小差异，但这些法令是我们理解古典时期雅典政治史的基石。

我们的训练数据集包含较早的公元前 446/445 年这一数字。为检验 Ithaca 的预测，我们在一个不含这些带年代铭文的数据集上重新训练了它，然后把这些留出的文本提交分析。引人注目的是，Ithaca 对这些法令的平均预测年代是公元前 421 年，与最新的断代突破相吻合，展示了机器学习如何能够为围绕希腊历史上最重要时刻之一的学术争论做出贡献。

![箱线图，比较 PHI 与 Ithaca 的断代误差（单位：年），显示 Ithaca 的中位数和平均误差（低于 10 年）显著低于 PHI（超过 20 年）。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6231e4e8ad33cf33f6d57c3c_Fig205.2.svg)

图 5。Ithaca 的预测与帕卡德人文研究所（PHI）数据集的真实标注，同近期史学重新评估的对比。PHI 的标注平均偏离重新评估结果 27 年，而 Ithaca 的预测平均只偏离新提出的真实标注 5 年。

我们相信，这只是 Ithaca 这类工具以及机器学习与人文学科合作潜力的起点。古希腊在我们对地中海世界的理解中扮演着关键角色，但它仍只是全球文明宏大图景中的一部分。为此，我们目前正在开发在其他古代语言上训练的 Ithaca 版本，而历史学家已经可以在现有架构中使用他们自己的数据集来研究其他古代书写系统——从[阿卡德语](https://en.wikipedia.org/wiki/Akkadian_language)到[世俗体埃及语](https://en.wikipedia.org/wiki/Demotic_(Egyptian))，从[希伯来语](https://en.wikipedia.org/wiki/Hebrew_language)到[玛雅语](https://en.wikipedia.org/wiki/Mayan_languages)。我们希望像 Ithaca 这样的模型能够释放 AI 与人文学科之间的合作潜力，变革性地影响我们研究和书写人类历史上一些最重要时期的方式。

- 阅读[论文](https://www.nature.com/articles/s41586-022-04448-z)
- 探索 Ithaca 的[交互版本](https://ithaca.deepmind.com/)
- 获取[开源](https://github.com/deepmind/ithaca)代码
- 阅读本博客的[希腊语译文](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/restoring-and-attributing-ancient-texts-using-deep-neural-networks/Ancient_Texts_(Greek).pdf)

**注记**

这项工作由一个团队完成，贡献者包括 Yannis Assael、Thea Sommerschield、Brendan Shillingford、Mahyar Bordbar、John Pavlopoulos、Marita Chatzipanagiotou、Ion Androutsopoulos、Jonathan Prag 和 Nando de Freitas。Ithaca 网页界面由来自 Google Cloud 的 Justin Grayston、Benjamin Maynard 和 Ricardo Cardenas 开发。
