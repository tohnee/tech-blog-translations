---
title: "Facebook Research 在 EMNLP 2019 上的研究"
title_en: "Facebook Research at EMNLP 2019"
date: 2019-03-15
source: https://ai.meta.com/blog/-facebook-research-at-emnlp-2019/
crawled: 2026-09-22
translated: 2026-09-22
---

# Facebook Research 在 EMNLP 2019 上的研究

> 原文：[Facebook Research at EMNLP 2019](https://ai.meta.com/blog/-facebook-research-at-emnlp-2019/) · Meta AI（Wayback 存档）

2019 年自然语言处理实证方法会议（EMNLP）本周（11 月 3 日至 7 日）在香港举行。EMNLP 由 ACL 语言数据特别兴趣组（SIGDAT）组织，是自然语言处理领域领先的研究会议之一，包括三天主会和两天的研讨会与教程。Facebook 的研究者将与来自世界各地的 2000 至 2500 名学者、业界专业人士和研究者一起，讨论 NLP 与计算语言学的最新进展。Facebook 研究科学家 Kyunghyun Cho 是 EMNLP 的三位主题演讲者之一，将发表题为《Curiosity-driven Journey into Neural Sequence Models》的演讲。Kyunghyun 的演讲摘要如下：「在这次演讲中，我将带领大家回顾我在构建神经序列模型方面的早期与近期经历。我会从早期使用循环网络做序列到序列学习的经历谈起，再谈注意力机制。我将讨论这些早期方法成功背后的因素，以及它们在成为最先进技术之前就如何被社区所接纳。随后我会转向非常规神经序列模型的更多近期研究方向——这些模型自动学习决定生成的顺序。」

Facebook 研究者将在口头报告、海报环节和研讨会中展示超过 25 篇论文。对于参会者，请务必到 Facebook Research 的 C 展台，与我们的项目经理、研究者和招聘人员交流。EMNLP 上展示研究的逐日日程可在此处查阅。

## Facebook 在 EMNLP 上展示的研究

**A Discrete Hard EM Approach for Weakly Supervised Question Answering**
（弱监督问答的一种离散硬 EM 方法）
Sewon Min、Danqi Chen、Hannaneh Hajishirzi、Luke Zettlemoyer
许多问答（QA）任务只对答案应如何计算提供弱监督。例如，TRIVIAQA 的答案是可以在支持文档中被提及多次的实体，而 DROP 的答案可以通过从参考文本中的数字推导出许多不同的等式来计算。本文表明，可以把这类任务转换为离散潜在变量学习问题，使用一个预先计算的、任务特定的候选解集合（如不同的提及或等式），其中包含一个正确选项。然后我们设计一种硬 EM 学习方案，每次更新时相对于最可能的解计算梯度。尽管简单，我们表明该方法在六个 QA 任务上显著优于以往方法，绝对提升 2–10%，并在其中五个任务上达到最先进水平。使用硬更新而非最大化边际似然是这些结果的关键，因为它鼓励模型找到那一个正确答案——我们通过详细的定性分析证明了这一点。

**BERT for Coreference Resolution: Baselines and Analysis**
（用于指代消解的 BERT：基线与分析）
Mandar Joshi、Omer Levy、Luke Zettlemoyer、Daniel Weld
我们将 BERT 应用于指代消解，在 OntoNotes（+3.9 F1）和 GAP（+11.5 F1）基准上取得了强劲提升。对模型预测的定性分析表明，与 ELMo 和 BERT-base 相比，BERT-large 尤其更擅长区分相关但不同的实体（例如总裁与 CEO）。不过，在建模文档级上下文、对话和提及改述方面仍有改进空间。我们的代码和模型已公开。

**Bridging the Gap Between Relevance Matching and Semantic Matching for Short Text Similarity Modeling**
（为短文本相似度建模弥合相关性匹配与语义匹配之间的鸿沟）
Jinfeng Rao、Linqing Liu、Yi Tay、Wei Yang、Peng Shi、Jimmy Lin
信息检索（IR）的一个核心问题是相关性匹配，即按与用户查询的相关性对文档排序。另一方面，许多 NLP 问题（如问答和释义识别）可以视为语义匹配的变体，即衡量两段短文本之间的语义距离。虽然相关性匹配和语义匹配在高层面上都要求建模文本相似性，但许多面向其中一者的现有技术难以直接迁移到另一者。为弥合这一鸿沟，我们提出一个新模型 HCAN（Hybrid Co-Attention Network，混合共同注意力网络），它包含：(1) 混合编码器模块，包括基于 ConvNet 和基于 LSTM 的编码器；(2) 相关性匹配模块，以多粒度的重要性加权度量软词项匹配；(3) 带共同注意力机制的语义匹配模块，捕捉上下文感知的语义关联。在多个 IR 和 NLP 基准上的评估表明，与不利用外部数据预训练的方法相比，该模型达到了最先进的有效性。大量消融研究表明，无论选择何种底层编码器，相关性和语义匹配信号在许多问题设定中都是互补的。

**Build It Break It Fix It for Dialogue Safety: Robustness from Adversarial Human Attack**
（对话安全的「构建-破坏-修复」：来自对抗性人类攻击的鲁棒性）
Emily Dinan、Samuel Humeau、Bharath Chintagunta、Jason Weston
在对话语境中检测冒犯性语言已成为自然语言处理日益重要的应用。公共论坛中的喷子检测（Galan-García et al., 2016）和聊天机器人在公共领域的部署（Wolf et al., 2017）是两个例子，说明了对人类一方对抗性冒犯行为设防的必要性。在这项工作中，我们开发了一种训练方案，通过「构建、破坏、修复」的迭代策略（人类和模型都在闭环中），使模型对这类人类攻击变得鲁棒。在详细的实验中，我们表明该方法比以前的系统鲁棒得多。此外，我们表明对话中使用的冒犯性语言关键性地依赖对话语境，不能像大多数以往工作那样视为单句冒犯检测任务。我们新收集的任务和方法全部开源并公开可用。

**Cloze-Driven Pretraining of Self-Attention Networks**
（自注意力网络的完形填空驱动预训练）
Alexei Baevski、Sergey Edunov、Yinhan Liu、Luke Zettlemoyer、Michael Auli
我们提出一种预训练双向 transformer 模型的新方法，在多种语言理解问题上带来显著性能提升。我们的模型求解完形填空式词重建任务：每个词被消隐，必须根据文本其余部分预测出来。实验表明，模型在 GLUE 上取得大幅性能提升，在 NER 以及成分句法分析基准上取得与 BERT 一致的新的最先进结果。我们还对促成有效预训练的若干因素做了详细分析，包括数据领域与规模、模型容量，以及完形填空目标函数的变体。

**CLUTRR — A Diagnostic Benchmark for Inductive Reasoning from Text**
（CLUTRR——一个从文本进行归纳推理的诊断基准）
Koustuv Sinha、Shagun Sodhani、Jin Dong、Joelle Pineau、William L. Hamilton
自然语言理解（NLU）系统近来的成功被一些结果所困扰：这些结果凸显了此类模型无法以系统、鲁棒的方式泛化。在这项工作中，我们引入一个名为 CLUTRR 的诊断基准套件，以澄清与 NLU 系统鲁棒性和系统性相关的一些关键问题。受归纳逻辑程序设计的经典工作启发，CLUTRR 要求 NLU 系统推断短故事中人物之间的亲属关系。要在此任务上取得成功，既需要提取实体之间的关系，也需要推断支配这些关系的逻辑规则。CLUTRR 让我们能够通过在留出的逻辑规则组合上评估，精确度量模型的系统泛化能力；并通过添加精心策划的噪声事实来评估模型的鲁棒性。我们的实证结果凸显了最先进 NLU 模型（如 BERT 和 MAC）与一个直接处理符号输入的图神经网络模型之间的巨大性能差距——基于图的模型表现出更强的泛化能力和更大的鲁棒性。

**Countering Language Drift via Grounding**
（通过接地对抗语言漂移）
Jason Lee、Kyunghyun Cho、Douwe Kiela
虽然强化学习在多智能体通信方面展现了很大前景——例如微调智能体通过交流达成某个目标——但对潜在语言漂移的研究很少：当用外部奖励训练系统时，智能体的通信协议可能轻易且彻底地偏离自然语言。我们研究了为缓解漂移应施加哪些约束，并表明句法与语义（经由接地）约束的结合带来最佳通信性能，使预训练智能体在学习传达预期含义的同时保留英语句法。

**Don't Forget the Long Tail! A Comprehensive Analysis of Morphological Generalization in Bilingual Lexicon Induction**
（别忘长尾！双语词典归纳中形态泛化的全面分析）
Paula Czarnowska、Sebastian Ruder、Edouard Grave、Ryan Cotterell、Ann Copestake
由于语言中词的齐夫分布，人类译者经常要翻译词的罕见屈折形式。从西班牙语翻译时，好的译者不难识别像 hablarámos 这样统计上罕见的屈折形式的恰当译法。注意词位本身 hablar 相当常见。在这项工作中，我们研究最先进的双语词典归纳器是否能学会这类泛化。我们引入 10 种语言的 40 部形态完整的词典，并在低频形态形式的翻译任务上评估三个最先进模型。我们证明，最先进模型在不常见形态屈折形式上的评估性能大幅下降；进而表明在训练时加入简单的形态约束可以提升性能，证明双语词典归纳器可以从更好的形态编码中受益。

**EASSE: Easier Automatic Sentence Simplification Evaluation**
（EASSE：更简单的自动句子简化评估）
Fernando Alva-Manchego、Louis Martin、Carolina Scarton、Lucia Specia
我们介绍 EASSE，一个旨在便利化并标准化句子简化（SS）系统自动评估与比较的 Python 包。EASSE 提供对广泛评估资源的单一访问入口：评估 SS 输出的标准自动指标（如 SARI）、针对特定简化转换的词级准确率分数、独立于参考的质量估计特征（如压缩率），以及 SS 评估的标准测试数据（如 TurkCorpus）。最后，EASSE 生成易于可视化的报告，涵盖上述各种指标和特征，以及特定 SS 输出相对于参考简化的表现。通过实验，我们表明这些功能有助于更好地比较和理解 SS 系统的性能。

**EGG: A Toolkit for Research on Emergence of lanGuage in Games**
（EGG：研究游戏中语言涌现的工具包）
Eugene Kharitonov、Rahma Chaabouni、Diane Bouchacourt、Marco Baroni
在深度神经智能体之间模拟语言涌现重新引起关注——它们通过通信共同求解任务；其动力既来自开发支持语言的交互式 AI 的现实目标，也来自关于人类语言演化的理论问题。然而，优化由离散通信信道（语言即在此类信道中涌现）连接的深度架构在技术上是挑战。我们介绍 EGG，一个极大简化涌现语言通信游戏实现的工具包。EGG 的模块化设计提供一组构件，用户可以组合它们创建新游戏，轻松驾驭优化和架构空间。我们希望该工具能降低技术门槛，鼓励不同背景的研究者在这一激动人心的领域做出原创工作。

**Emergent Linguistic Phenomena in Multi-Agent Communication Games**
（多智能体通信游戏中的涌现语言学现象）
Laura Graesser、Kyunghyun Cho、Douwe Kiela
我们描述一个多智能体通信框架，用于在社区层面考察高层语言学现象。我们证明，自然语言中观察到的复杂语言行为可以在这一简单设定中复现：1) 社区之间接触的结果是组间与组内连通性的函数；2) 语言接触要么收敛到多数协议，要么在势均力敌的情形下产生复杂度较低的新型克里奥尔语言；3) 会涌现出一个语言连续统，相邻语言之间的互懂程度高于距离较远的语言。我们的结论是：语言演化的至少某些精巧性质未必依赖演化出的复杂语言能力，而可以从具备感知能力的智能体玩通信游戏时的简单社会交流中涌现。

**Finding Generalizable Evidence by Learning to Convince Q and A Models**
（通过学习说服问答模型来寻找可泛化的证据）
Ethan Perez、Siddharth Karamcheti、Rob Fergus、Jason Weston、Douwe Kiela、Kyunghyun Cho
我们提出一个系统，为给定的问题答案找到最强支持证据，以基于段落的问答（QA）为试验场。我们训练证据智能体去选择最能说服某个预训练 QA 模型相信给定答案的段落句子——前提是 QA 模型收到的是这些句子而非完整段落。我们发现，智能体找到的不是只说服单一模型的证据，而是可泛化的证据：智能体选出的证据提高了被支持答案的可信度——无论由其他 QA 模型还是人类评判。鉴于其通用性质，这一方法以鲁棒的方式改进 QA：使用智能体选择的证据，1) 人类仅凭完整段落约 20% 的内容即可正确回答问题；2) QA 模型能泛化到更长的段落和更难的问题。

**The FLORES Evaluation Datasets for Low-Resource Machine Translation: Nepali-English and Sinhala-English**
（面向低资源机器翻译的 FLORES 评估数据集：尼泊尔语-英语和僧伽罗语-英语）
Francisco Guzmán、Peng-Jen Chen、Myle Ott、Juan Pino、Guillaume Lample、Philipp Koehn、Vishrav Chaudhary、Marc'Aurelio Ranzato
对机器翻译而言，世界上绝大多数语言对都被视为低资源，因为可用的平行数据很少。除了在有限监督下学习的技术挑战之外，由于缺乏免费公开的基准，评估在低资源语言对上训练的方法也很困难。在这项工作中，我们介绍基于从维基百科翻译的句子的尼泊尔语-英语和僧伽罗语-英语 FLORES 评估数据集。与英语相比，这些语言的形态和句法差异很大，可用的域外平行数据很少，而相对大量的单语数据可以免费获取。我们描述了收集和交叉核查翻译质量的过程，并报告了若干学习设定下的基线性能：全监督、弱监督、半监督和完全无监督。我们的实验表明，当前最先进的方法在该基准上表现相当差，这对从事低资源机器翻译的研究社区提出了挑战。复现实验的数据和代码可在此获取。

**FlowSeq: Non-Autoregressive Conditional Sequence Generation with Generative Flow**
（FlowSeq：基于生成流的非自回归条件序列生成）
Xuezhe Ma、Chunting Zhou、Xian Li、Graham Neubig、Eduard Hovy
大多数序列到序列（seq2seq）模型是自回归的：它们以已生成的词元为条件逐个生成词元。相比之下，非自回归 seq2seq 模型一次通过生成所有词元，借助 GPU 等硬件上的并行处理带来效率提升。然而，直接同时建模所有词元的联合分布颇具挑战，而且即使模型结构越来越复杂，准确率仍显著落后于自回归模型。本文提出一个简单、高效且有效的非自回归序列生成模型，采用潜在变量模型。具体来说，我们求助于生成流——一种用神经网络建模复杂分布的优雅技术，并设计了若干专门为建模序列潜在变量条件密度而定制的流层。我们在三个神经机器翻译（NMT）基准数据集上评估该模型，取得了与最先进非自回归 NMT 模型相当的性能，且解码时间相对序列长度几乎恒定。

**Improving Generative Visual Dialog by Answering Diverse Questions**
（通过回答多样化问题改进生成式视觉对话）
Vishvak S. Murahari、Prithvijit Chattopadhyay、Dhruv Batra、Devi Parikh、Abhishek Das
先前用强化学习训练生成式视觉对话模型的工作（Das et al., 2017b）探索了 Q-BOT-A-BOT 猜图游戏，并表明这种「自言自语」方法可以改进下游对话条件猜图任务的性能。然而，这一提升在几轮交互后便饱和并开始退化，也没有带来更好的视觉对话模型。我们发现，这部分是由于自言自语期间 Q-BOT 与 A-BOT 之间重复的交互对图像而言没有信息量。为改进这一点，我们设计了一个简单的辅助目标，激励 Q-BOT 提出多样化的问题，从而减少重复，进而让 A-BOT 在强化学习中探索更大的状态空间——即接触到更多可谈论的视觉概念和更多样的问题来回答。我们通过一系列自动指标和人类研究评估该方法，证明它带来更好的对话——更多样（重复更少）、更一致（冲突交流更少）、更流畅（更像人类）、更详细，同时在与先前工作和消融版本相比时保持相当的图像相关性。

**Language Models as Knowledge Bases?**
（语言模型能当知识库用吗？）
Fabio Petroni、Tim Rocktaschel、Sebastian Riedel、Patrick Lewis、Anton Bakhtin、Yuxiang Wu、Alexander H. Miller
在大型文本语料库上预训练语言模型的最新进展，为下游 NLP 任务带来了一波提升。在学习语言知识的同时，这些模型可能也存储了训练数据中存在的关联知识，并可能能够回答以「填空」完形陈述形式构造的查询。语言模型相较结构化知识库有诸多优势：无需模式工程、允许从业者查询开放类的关系、易于扩展到更多数据、训练无需人类监督。我们对一系列最先进预训练语言模型中已经存在（无需微调）的关联知识做了深入分析。我们发现：1) 无需微调，BERT 包含的关联知识可与部分接触了先验知识的传统 NLP 方法相竞争；2) BERT 在开放域问答上相对一个有监督基线也表现出色；3) 某些类型的事实知识比其他类型更容易被标准语言模型预训练方法学到。这些模型在无任何微调情况下回忆事实知识的惊人能力，展示了它们作为无监督开放域 QA 系统的潜力。复现分析代码可在此获取。

**Learning Programmatic Idioms for Scalable Semantic Parsing**
（为可扩展语义解析学习程序化习语）
Srinivasan Iyer、Alvin Cheung、Luke Zettlemoyer
程序员通常用高层编码模式或习语结构（如嵌套循环、异常处理器和递归块）来组织可执行源代码，而不是逐个代码词元。相比之下，最先进（SOTA）的语义解析器仍是通过一次一个节点地构建代码语法树，把自然语言指令映射到源代码。本文引入一种迭代方法，从大型源代码语料库中提取代码习语：反复折叠语法树中最常见的深度为 2 的子树，并训练语义解析器在解码时应用这些习语。在一个近期的上下文相关语义解析任务上，基于习语的解码将 SOTA 提升 2.2% BLEU，同时将训练时间缩短逾 50%。这一速度提升使我们能够在扩大 5 倍的扩展训练集上训练模型，进一步将 SOTA 提升额外的 2.3% BLEU 和 0.9% 精确匹配。最后，在训练数据有限时，习语也显著提升了 ATIS-SQL 数据集上语义解析到 SQL 的准确率。

**Learning to Speak and Act in a Fantasy Text Adventure Game**
（在奇幻文字冒险游戏中学习说话与行动）
Jack Urbanek、Angela Fan、Siddharth Karamcheti、Saachi Jain、Samuel Humeau、Emily Dinan、Tim Rocktäschel、Douwe Kiela、Arthur Szlam、Jason Weston
我们引入一个大规模众包文字冒险游戏，作为研究接地对话的平台。在游戏中，智能体可以感知、表达情绪并采取行动，同时与其他智能体对话。模型和人类都可以扮演游戏中的角色。我们描述了在这一设定下训练最先进的生成式与检索式模型的结果。我们表明，除了利用过去的对话，这些模型还能有效利用底层世界的状态来调节预测。特别是，我们表明，接地于局部环境的细节——包括位置描述，以及其中的物体（及其可供性）和角色（及其先前行动）——可以更好地预测智能体行为和对话。我们分析了在这一设定下成功接地所需的要素，以及这些因素各自与能成功交谈和行动的智能体之间的关系。

**Mask-Predict: Parallel Decoding of Conditional Masked Language Models**
（Mask-Predict：条件掩码语言模型的并行解码）
Marjan Ghazvininejad、Omer Levy、Yinhan Liu、Luke Zettlemoyer
大多数机器翻译系统自左向右自回归地生成文本。我们则使用掩码语言建模目标来训练模型，使其在输入文本和部分掩蔽的目标翻译的条件下预测目标词的任意子集。这一方法支持高效的迭代解码：先非自回归地预测所有目标词，然后反复掩蔽并重新生成模型最没把握的词的子集。将这一策略应用固定的迭代次数后，我们的模型把非自回归与并行解码翻译模型的最新性能水平平均提升超过 4 BLEU。它还能达到与典型的从左到右 transformer 模型相差约 1 BLEU 以内的水平，同时解码显著更快。

**Massively Multilingual Sentence Embeddings for Zero-Shot Cross-Lingual Transfer and Beyond**
（面向零样本跨语言迁移及更多场景的大规模多语言句子嵌入）**
Mikel Artexe、Holger Schwenk
我们引入一种架构，为 93 种语言学习联合多语言句子表示，这些语言属于 30 多个不同语族、使用 28 种不同文字。我们的系统对所有语言使用单个 BiLSTM 编码器和共享的 BPE 词表，并耦合一个辅助解码器，在公开可用的平行语料库上训练。这使我们能够仅在英语标注数据上基于所得嵌入训练一个分类器，并毫无修改地把它迁移到 93 种语言中的任意一种。我们在跨语言自然语言推断（XNLI 数据集）、跨语言文档分类（MLDoc 数据集）和平行语料挖掘（BUCC 数据集）上的实验展示了该方法的有效性。我们还引入一个新的 112 种语言对齐句子测试集，并表明我们的句子嵌入在多语言相似性搜索中即使对低资源语言也能取得强劲结果。我们的实现、预训练编码器和多语言测试集可在此获取。

**Memory-Grounded Conversational Reasoning**
（记忆接地的对话推理）
Seungwhan Moon、Pararth Shah、Anuj Kumar、Rajen Subba
我们展示了一个对话系统，围绕用户的记忆与用户进行多模态、多轮对话。该系统可以针对记忆进行问答，通过响应用户查询来回忆过去情节记忆的具体属性和相关媒体（如照片）。系统还可以主动建议，从过去记忆中浮现相关事件或事实，使对话更有吸引力和更自然。为实现这样一个系统，我们收集了一个新的记忆接地对话语料库，包含给定带模拟属性的合成记忆图后人类角色扮演对话。我们的概念验证系统运行在这些合成记忆图上，但它可以训练并应用于真实的用户记忆数据（如相册）。我们给出了所提对话系统的架构以及系统支持的示例查询。

**Quantifying the Semantic Core of Gender Systems**
（量化性别系统的语义核心）
Adina Williams、Ryan Cotterell、Lawrence Wolf-Sonkin、Damián Blasi、Hanna Wallach
世界上许多语言在词位上使用语法性别。例如，西班牙语中「房子」（casa）是阴性，而「纸」（papel）是阳性。对使用无性别语言的说话者来说，这种分配似乎毫无道理可言。但无生命名词到语法性别的分配真的完全是任意的吗？我们对名词性别分配的任意性进行了首次大规模调查。为此，我们使用典型相关分析将无生命名词的语法性别与其词义的外部接地定义相关联。我们发现 18 种语言在语法性别与词汇语义之间表现出显著相关性。

**Recommendation as a Communication Game: Self-Role-Playing for Goal-Oriented Dialogue**
（推荐即通信游戏：面向目标对话的自我角色扮演）
Dongyeop Kang、Anusha Balakrishnan、Pararth Shah、Paul Crook、Y-Lan Boureau、Jason Weston
传统推荐系统产生的是静态而非交互式的推荐，不随用户的具体请求、澄清或当下心情而变化，而且如果用户品味未知，还会遭遇冷启动问题。把推荐当作交互式对话任务来处理可以缓解这些问题：一个专家推荐者可以依次询问某人的偏好，回应其请求，并推荐更合适的条目。在这项工作中，我们收集了一个目标驱动的推荐对话数据集（GoRecDial），由成对人类工作者互相推荐电影的 9125 局对话游戏和 81260 轮会话组成。该任务被专门设计为两名玩家朝着可量化共同目标合作的合作博弈。我们利用该数据集开发了一个可以同时对话和推荐的端到端对话系统。模型先被训练来模仿人类玩家的行为而不考虑任务目标本身（监督训练）。然后我们在两个成对预训练模型之间的模拟机器人-机器人对话（bot-play）上微调模型，以达成对话目标。实验表明，经 bot-play 微调的模型学到了更好的对话策略，与人类配对时更常达成对话目标，并且人类评价其比未经 bot-play 训练的模型更一致。数据集和代码通过 ParlAI 框架公开提供。

**Revisiting the Evaluation of Theory of Mind Through Question Answering**
（重新审视通过问答评估心智理论）
Matthew Le、Y-Lan Boureau、Maximilian Nickel
心智理论，即对智能体意图和信念进行推理的能力，是人工智能中的一项重要任务，也是解决自然语言对话中歧义指代的核心。在这项工作中，我们重新审视通过问答对心智理论的评估。我们表明当前的评估方法存在缺陷，现有基准任务由于数据集偏置而无需心智理论即可解决。基于先前工作，我们提出一个改进的评估协议和数据集，通过对答案空间的仔细检查来显式控制数据规律。我们表明，在现有基准上成功的最先进方法无法在我们提出的方法中求解心智理论任务。

**Simple and Effective Noisy Channel Modeling for Neural Machine Translation**
（用于神经机器翻译的简单有效的噪声信道建模）
Kyra Yee、Yann N. Dauphin、Michael Auli
以往关于神经噪声信道建模的工作依赖增量处理源句和目标句的潜在变量模型。这使得解码决策基于部分源句前缀，尽管完整源句是可用的。我们追求另一种基于标准序列到序列模型的方法，充分利用整个源句。这些模型作为信道模型表现得非常出色，尽管它们既没有在残缺目标句上训练过，也不是为此设计的。在数十亿词上训练的神经语言模型实验表明，噪声信道模型在 WMT'17 德译英上最多可比直接模型高出 3.2 BLEU。我们在四个语言对上评估，我们的信道模型始终优于强替代方案，如从右到左重排序模型和直接模型集成。

**Using Local Knowledge Graph Construction to Scale Seq2Seq Models to Multi-Document Inputs**
（利用局部知识图谱构建将 Seq2Seq 模型扩展到多文档输入）
Angela Fan、Claire Gardent、Chloe Braud、Antoine Bordes
基于查询的开放域 NLP 任务需要从冗长多样的网页结果中综合信息。当前方法使用 TF-IDF 排序等方法，抽取式地选择网页文本片段作为序列到序列模型的输入。我们提议为每个查询构建一个局部图结构知识库，压缩网络搜索信息并减少冗余。我们表明，通过把图线性化为结构化输入序列，模型可以在标准序列到序列设定中编码图表示。对于两个具有超长文本输入的生成任务——长式问答和多文档摘要——以图表示作为输入可以取得比使用检索到的文本片段更好的性能。

**VizSeq: A Visual Analysis Toolkit for Text Generation Tasks**
（VizSeq：面向文本生成任务的可视化分析工具包）
Changhan Wang、Anirudh Jain、Danlu Chen、Jiatao Gu
文本生成任务（如机器翻译、文本摘要、图像描述和视频描述）的自动评估通常严重依赖任务特定指标，如 BLEU（Papineni et al., 2002）和 ROUGE（Lin, 2004）。然而它们是抽象的数字，与人类评估并不完全一致。这提示我们应检视详细示例作为补充，以识别系统错误模式。本文介绍 VizSeq，一个面向广泛文本生成任务的实例级和语料库级系统评估可视化分析工具包。它支持多模态源和多个文本参考，在 Jupyter notebook 或 Web 应用界面中提供可视化。它可以在本地使用，也可以部署到公共服务器以进行集中数据托管和基准测试。它涵盖大多数常见的基于 n-gram 的指标（经多进程加速），还提供最新的基于嵌入的指标，如 BERTScore（Zhang et al., 2019）。

## EMNLP 上的其他活动

**Workshop on Asian Translation（亚洲翻译研讨会）**

- 论文：Facebook AI's WAT19 Myanmar-English Translation Task Submission — Peng-Jen Chen、Jiajun Shen、Matthew Le、Vishrav Chaudhary、Ahmed El-Kishky、Guillaume Wenzek、Myle Ott、Marc'Aurelio Ranzato

**Conference on Computational Natural Language Learning (CoNLL) — two-day workshop（计算自然语言学习会议，两天研讨会）**

- 论文：Walk the Memory: Memory Graph Networks for Explainable Memory-Grounded Question Answering — Seungwhan Moon、Pararth Shah、Anuj Kumar、Rajen Subba

**Workshop on Deep Learning for Low-Resource NLP（面向低资源 NLP 的深度学习研讨会）**

- 受邀演讲：Luke Zettlemoyer
- 论文：Evaluating Lottery Tickets Under Distributional Shifts — Shrey Desai、Hongyuan Zhan、Ahmed Aly

**Workshop on Neural Generation and Translation (WNGT)（神经生成与翻译研讨会）**

- 受邀演讲：Michael Auli、Jason Wetson
- 论文：Improved Variational Neural Machine Translation via Promoting Mutual Information — Xian Li、Jiatao Gu、Ning Dong、Arya McCarthy

**Machine Reading for Question Answering (MRQA)（面向问答的机器阅读）**

- 受邀演讲：Antoine Bordes

*论文由计算语言学协会汇刊（TACL）接收。
