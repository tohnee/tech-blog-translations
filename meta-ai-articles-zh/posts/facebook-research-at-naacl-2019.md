---
title: "Facebook 研究团队在 NAACL 2019"
title_en: "Facebook Research at NAACL 2019"
date: 2019-06-02
source: https://ai.facebook.com/blog/facebook-research-at-naacl-2019
crawled: 2026-09-22
translated: 2026-09-22
---

# Facebook 研究团队在 NAACL 2019

> 原文：[Facebook Research at NAACL 2019](https://ai.facebook.com/blog/facebook-research-at-naacl-2019) · Meta AI（Wayback 存档）

2019 年 6 月 2 日

自然语言理解、计算语言学与对话式 AI 领域的专家本周齐聚明尼阿波利斯，参加计算语言学协会北美分会：人类语言技术会议（NAACL-HLT）2019 年会。Facebook 的研究将在口头 spotlight 和集体海报环节展示。我们的研究员和工程师还将在本周参与其他活动，包括 FAIRSEQ 演示——FAIRSEQ 是一个开源序列建模工具包，允许研究者和开发者训练用于翻译、摘要、语言建模及其他文本生成任务的定制模型。参加 NAACL-HLT 的人请务必访问 Facebook Research 展位。

## Facebook 在 NAACL-HLT 上展示的研究

**用图卷积网络做辱骂语言检测（Abusive Language Detection with Graph Convolutional Networks）**
Pushkar Mishra、Marco Del Tredici、Helen Yannakoudakis、Ekaterina Shutova
网络辱骂是我们这个时代的重要社会问题。此前关于 Twitter 上自动辱骂语言检测的研究表明，基于社区的用户画像是有前景的技术。然而现有方法只通过建模关注-被关注关系捕捉在线社区的浅层属性。与之相反，我们提出首个基于图卷积网络（GCN）、同时捕捉在线社区结构及其中用户语言行为的方法。我们表明，这种异构图结构化社区建模显著推进了辱骂语言检测的当前技术水平。

**CLEVR-Dialog：面向视觉对话多轮推理的诊断数据集（CLEVR-Dialog: A Diagnostic Data Set for Multi-Round Reasoning in Visual Dialog）**
Satwik Kottur、José M. F. Moura、Devi Parikh、Dhruv Batra、Marcus Rohrbach
视觉对话是一个多模态任务：以对话历史为上下文，回答基于某图像的一系列问题。它蕴含视觉、语言、推理与落地方面的挑战。然而，在大型真实数据集上孤立研究这些子任务并不可行，因为需要对所有图像与对话的「状态」做完整标注，成本高得惊人。我们开发了 CLEVR-Dialog——一个用于研究视觉对话多轮推理的大型诊断数据集。具体而言，我们构造了一个落地于 CLEVR 数据集图像场景图的对话文法。这一组合产出了一个视觉对话所有方面都被完整标注的数据集。CLEVR-Dialog 总共为约 8.5 万张 CLEVR 图像提供五组 10 轮对话实例，共计 425 万个问答对。我们用 CLEVR-Dialog 对标准视觉对话模型做基准测试，尤其是视觉指代消解（作为指代距离的函数）。这是首个此类视觉对话模型分析——没有该数据集就无法做到。我们希望 CLEVR-Dialog 的发现有助于指导未来视觉对话模型的开发。数据集与代码将公开。

**句法与语义解耦的协作学习（Cooperative Learning of Disjoint Syntax and Semantics）**
Serhii Havrylov、Germán Kruszewski、Armand Joulin
学习联合推断表达式句法结构与语义的模型一直备受关注。然而，Nangia 与 Bowman（2018）最近表明，当前最佳系统无法在由简单上下文无关文法生成的数学表达式上学到正确的解析策略。在本工作中，我们提出一个受 Choi 等（2018）启发的递归模型，在该任务上达到接近完美的精度。我们的模型由句法与语义两个分离的模块组成，用标准的连续与离散优化方案协作训练。我们的模型不需要任何语言结构监督，其递归特性允许以极小的性能损失实现域外泛化。此外，我们的方法在自然语言推理与情感分析等多个自然语言任务上表现有竞争力。

**面向多语言任务型对话的跨语言迁移学习（Cross-lingual Transfer Learning for Multilingual Task-Oriented Dialog）**
Sebastian Schuster、Sonal Gupta、Rushin Shah、Mike Lewis
许多任务型对话 AI 系统话语解释流水线的第一步是识别用户意图与相应槽位。由于该任务机器学习模型的数据收集耗时，理想的做法是利用高资源语言的现有数据来训练低资源语言模型。然而，多语言训练数据的缺乏在很大程度上阻碍了此类模型的开发。在本文中，我们提出一个新数据集，包含天气、闹钟与提醒三个领域、共 5.7 万条标注话语：英语（4.3 万）、西班牙语（8600）与泰语（5000）。我们用该数据集评估三种跨语言迁移方法：（1）翻译训练数据；（2）使用跨语言预训练嵌入；（3）使用多语言机器翻译编码器作为上下文词表示的新方法。我们发现，给定目标语言的几百个训练样本时，后两种方法优于翻译训练数据。此外，在极低资源设置下，多语言上下文词表示比使用跨语言静态嵌入效果更好。我们还把跨语言方法与以 ELMo 上下文表示形式的单语言资源做了比较，发现只要给定少量目标语言数据，该方法就胜过所有跨语言方法，这凸显了对更精巧跨语言方法的需求。

**LSTM 语言模型中数与句法单元的涌现（The Emergence of Number and Syntax Units in LSTM Language Models）**
Yair Lakretz、Germán Kruszewski、Théo Desbordes、Dieuwke Hupkes、Stanislas Dehaene、Marco Baroni
近期工作表明，在通用语言建模目标上训练的 LSTM 能捕捉长距离数一致等对句法敏感的泛化。然而，我们对其如何实现这一壮举缺乏机制层面的理解。有人猜测它依赖并不真正考虑层级结构的启发式。我们在此从单个神经元层面详细研究 LSTM 中数追踪的内部机制。我们发现，长距离数信息主要由两个「数单元」管理。重要的是，这些单元的行为部分受其他被独立证明可追踪句法结构的单元控制。我们得出结论：LSTM 在某种程度上确实实现了句法处理机制，为更普遍地理解 LSTM 中的语法编码铺平了道路。

**生成、过滤、排序：面向可投产 NLG 系统的语法性分类（Generate, Filter, and Rank: Grammaticality Classification for Production-Ready NLG Systems）**
Ashwini Challa、Kartikeya Upasani、Anusha Balakrishnan、Rajen Subba
神经方法在面向目标的对话自然语言生成（NLG）上前景可期。然而将其投产的挑战之一是控制回复质量、确保生成回复可接受的能力。我们提出「生成、过滤、排序」框架：先过滤候选回复以剔除不可接受的，再排序以选出最佳回复。可接受性包含语法正确与语义正确，本文只聚焦语法性分类，并表明现有的语法纠错数据集并未正确捕捉数据驱动生成器可能犯的错误分布。我们发布了一个天气领域的语法性分类与语义正确性分类数据集，由三个数据驱动 NLG 系统生成的回复组成。然后我们探索两种有监督学习方法（CNN 与 GBDT）做语法性分类。实验表明，语法性分类对数据中的错误分布非常敏感，而这些分布随回复来源与领域显著变化。我们表明，在我们的数据集上可以在合理召回率下达到高精度。

**知识增强语言模型及其在无监督命名实体识别中的应用（Knowledge-Augmented Language Model and Its Application to Unsupervised Named-Entity Recognition）**
Angli Liu、Jingfei Du、Veselin Stoyanov
传统语言模型无法高效建模文本中出现的实体名称。除最流行的命名实体外，大多数在文本中出现频率很低，提供的上下文不足。近期工作认识到上下文可以在同类型（如人物或地点）实体名称之间泛化，并为语言模型配备了对外部知识库（KB）的访问。我们的知识增强语言模型（KALM）延续了这条路线，用 KB 增强传统模型。与以往方法不同，我们用端到端预测目标训练，优化文本困惑度，不需要命名实体标签等任何额外信息。除改进语言建模性能外，KALM 还利用模型中潜在的实体类型信息，以完全无监督的方式学会识别命名实体。在命名实体识别（NER）任务上，KALM 取得了与最先进有监督模型相当的性能。我们的工作表明，命名实体（可能还有其他类型的世界知识）可以通过预测学习与在大规模文本语料上的训练成功建模，无需任何额外信息。

**论序列到序列模型对抗扰动的评估（On Evaluation of Adversarial Perturbations for Sequence-to-Sequence Models）**
Paul Michel、Xian Li、Graham Neubig、Juan Miguel Pino
对抗样本——对模型输入施加扰动却在输出端引发巨大变化——已被证明是评估序列到序列（seq2seq）模型鲁棒性的有效途径。然而，只有当这些扰动没有把输入改变到合法地导致期望输出变化的地步时，它们才指示模型弱点。这一事实在日益增多的相关文献评估中大多被忽视。以机器翻译（MT）的无目标攻击为例，我们为 seq2seq 模型的对抗攻击提出新的评估框架，考虑扰动前后输入的语义等价性。利用该框架，我们证明现有方法总体上可能不保持意义，破坏了「源端扰动不应导致期望输出变化」的上述假设。我们进一步用该框架证明，对攻击施加额外约束可以得到更保义但仍大幅改变输出序列的对抗扰动。最后，我们表明用保义攻击执行无目标对抗训练有助于模型的对抗鲁棒性，且不损害测试性能。

**论汉语量词系统的特异性（On the Idiosyncrasies of the Mandarin Chinese Classifier System）**
Shijia Liu、Hongyuan Mei、Adina Williams、Ryan Cotterell
汉语量词系统的特异性一直是语言学家深入研究的课题（Adams 与 Conklin，1973；Erbaugh，1986；Lakoff，1986），但用统计方法量化它们的工作不多。在本文中，我们引入度量特异性的信息论方法；我们考察知晓量词所修饰名词的语义信息后，汉语量词的不确定性可以降低多少。利用已解析的中文 Gigaword 语料库（Graff 等，2005）中量词的经验分布，我们计算量词分布与其他语言量分布之间的互信息（比特）。我们研究名词与形容词的语义类别在降低量词选择不确定性方面的差异，发现它并非完全特异：虽然大多数语义类别没有明显趋势，但形状类名词对量词选择不确定性的降低最多。

**pair2vec：面向跨句推理的组合词对嵌入（pair2vec: Compositional Word-Pair Embeddings for Cross-Sentence Inference）**
Mandar Joshi、Eunsol Choi、Omer Levy、Daniel Weld、Luke Zettlemoyer
推理词对之间的隐含关系（如复述、常识、百科）对许多跨句推理问题至关重要。本文提出学习并使用词对嵌入的新方法，隐式表示关于此类关系的背景知识。我们的成对嵌入计算为词表示上的组合函数，通过最大化与两词共现上下文的逐点互信息（PMI）学习得到。我们把这些表示加入现有推理模型（如用于问答的 BiDAF、用于 NLI 的 ESIM）的跨句注意力层，而非扩展或替换现有词嵌入。实验表明，在最新发布的 SQuAD 2.0 上提升 2.7%，在 MultiNLI 上提升 1.3%。我们的表示还有助于更好的泛化：在对抗性 SQuAD 数据集上提升约 6%-7%，在 Glockner 等（2018）的对抗蕴含测试集上提升 8.8%。

**面向语言生成的预训练语言模型表示（Pretrained Language Model Representations for Language Generation）**
Sergey Edunov、Alexei Baevski、Michael Auli
预训练语言模型表示已在广泛的语言理解任务中取得成功。在本文中，我们考察把预训练表示整合进序列到序列模型的不同策略，并应用于神经机器翻译与抽象式摘要。我们发现，把预训练表示加入编码器网络最有效，推断仅减慢 14%。我们在机器翻译上的实验表明，在模拟的资源匮乏设置中增益最高达 5.3 BLEU。虽然随着带标注数据增多回报递减，但在数百万句对可用时仍能观察到改进。最后，在抽象式摘要上，我们在 CNN-DailyMail 全文版上取得新的最先进水平。

**用于短社交媒体帖子排序的简单基于注意力的表示学习（Simple Attention-Based Representation Learning for Ranking Short Social Media Posts）**
Peng Shi、Jinfeng Rao、Jimmy Lin
本文探索用神经网络针对用户查询对短社交媒体帖子排序的问题。我们不从复杂架构入手，而是自底向上，考察用基于注意力的机制增强的简单词级孪生架构捕捉查询与帖子 token 间语义「软」匹配的有效性。在 TREC 微博客追踪数据集上的大量实验表明，我们的简单模型不仅比现有复杂得多或利用更多样相关性信号的方法效果更好，而且快得多。我们与社区共享 samCNN（Simple Attention-based Matching CNN）模型的实现以支持后续工作。

**什么成就一次好对话？可控属性如何影响人类判断（What Makes a Good Conversation? How Controllable Attributes Affect Human Judgments）**
Abigail See、Stephen Roller、Douwe Kiela、Jason Weston
好的对话需要平衡——简洁与详尽之间；扣题与转换话题之间；提问与回答之间。虽然对话智能体通常通过人类对整体质量的判断来评估，但质量与这些个体因素之间的关系研究较少。在本工作中，我们考察两种可控神经文本生成方法——条件训练与加权解码——以控制闲聊对话的四个重要属性：重复性、特异性、回复相关性与提问。我们进行大规模人类评估，测量这些控制参数对 PersonaChat 任务多轮交互对话的影响。我们详细分析了它们与对话高层方面的关系，并表明通过控制这些变量的组合，我们的模型在人类质量判断上获得明确改进。
