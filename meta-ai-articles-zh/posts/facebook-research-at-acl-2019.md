---
title: "Facebook 研究团队在 ACL 2019"
title_en: "Facebook Research at ACL 2019"
date: 2019-03-15
source: https://ai.facebook.com/blog/facebook-research-at-acl-2019
crawled: 2026-09-22
translated: 2026-09-22
---

# Facebook 研究团队在 ACL 2019

> 原文：[Facebook Research at ACL 2019](https://ai.facebook.com/blog/facebook-research-at-acl-2019) · Meta AI（Wayback 存档）

第 57 届计算语言学协会（ACL）会议今年将于 7 月 28 日至 8 月 2 日在意大利佛罗伦萨举行。Facebook 的研究者将通过口头 spotlight、海报环节、受邀报告和其他研讨会活动展示他们的工作。举例来说，在第四届机器翻译会议（WMT）上，多位 Facebook AI 研究者通过参加新闻翻译任务和并行语料过滤任务，检验了他们在机器翻译方面的最新进展。对于参加 ACL 的人，请务必到 F 展位驻足，与研究员、招聘人员和计划经理聊聊 Facebook AI 的研究以及潜在的职业机会。Facebook 论文、研讨会和教程在 ACL 的完整日程请见此处。

## Facebook 在 ACL 2019 上展示的研究

**Transformer 中的自适应注意力跨度（Adaptive Attention Span in Transformers）**
Sainbayar Sukhbaatar、Edouard Grave、Piotr Bojanowski、Armand Joulin
我们提出一种能够学习自身最优注意力跨度的新颖自注意力机制。这使我们能够在控制内存占用与计算时间的同时，显著扩展 Transformer 所使用的最大上下文规模。我们在字符级语言建模任务上展示了该方法的有效性：使用 8K 字符的最大上下文，在 text8 和 enwiki8 上取得了最先进的性能。

**通过形态学改进字符语言建模（Better Character Language Modeling Through Morphology）**
Terra Blevins、Luke Zettlemoyer
我们通过多任务学习把形态学监督纳入字符语言模型（CLM），并证明即便形态学数据与语言建模数据不相交，这一补充也能在 24 种语言上改进每字符比特数（BPC）性能。对 CLM 的分析表明，屈折词比非屈折词更能从显式形态建模中受益；而且随着语言建模数据量增长，形态学监督仍能带来性能提升。随后，我们跨语言迁移形态学监督，改进了低资源场景下的语言建模性能。

**如何走出芝麻街：超越语言建模的句子级预训练（How to Get Past Sesame Street: Sentence-Level Pretraining Beyond Language Modeling）**
Alex Wang、Jan Hula、Patrick Xia、Raghavendra Pappagar、R. Thomas Mccoy、Roma Patel、Najoung Kim、Ian Tenney、Yinghui Huang、Katherin Yu、Shuning Jin、Berlin Chen、Benjamin Van Durme、Edouard Grave、Ellie Pavlick、Samuel R. Bowman
自然语言理解近来因 ELMo（Peters 等，2018a）和 BERT（Devlin 等，2019）等句子编码器的使用而取得巨大进展，这些编码器在语言建模的变体上预训练。我们对候选预训练任务开展了首个大规模系统研究，比较了 19 种不同任务——既作为语言建模的替代，也作为其补充。我们的主要结果支持使用语言建模，尤其是与额外有标注数据任务上的预训练相结合时。然而，结果在不同预训练任务间好坏参半，并显示出一些令人担忧的趋势：在 ELMo 的「先预训练后冻结」范式中，随机基线强得令人不安，且不同目标任务间结果差异悬殊。此外，在中间任务上微调 BERT 往往会对下游迁移产生负面影响。我们还从多任务训练中看到了适度收益，这提示更精巧的多任务与迁移学习技术是一个值得进一步研究的方向。

**发现 CNN 比 RNN 更会「四处跳跃」：序列到序列卷积网络中的组合泛化（CNNs Found to Jump Around More Skillfully than RNNs: Compositional Generalization in Seq2seq Convolutional Networks）**
Roberto Dessi、Marco Baroni
Lake 与 Baroni（2018）提出了 SCAN 数据集，用以探查 seq2seq 模型捕捉组合泛化的能力，例如从组成词零样本推断「jump around」的含义。循环网络（RNN）被发现完全无法通过最具挑战性的泛化用例。我们在这些任务上测试了卷积网络（CNN），报告了相较 RNN 大幅提升的性能。尽管改进巨大，CNN 也并未归纳出系统性规则，这表明组合行为与非组合行为之间的界限并非泾渭分明。

**CoDraw：以协作绘画作为落地目标驱动交流的测试平台（CoDraw: Collaborative Drawing as a Testbed for Grounded Goal-Driven Communication）**
Jin-Hwa Kim、Nikita Kitaev、Xinlei Chen、Marcus Rohrbach、Byoung-Tak Zhang、Yuandong Tian、Dhruv Batra、Devi Parikh
在本工作中，我们提出一个结合语言、感知与行动的目标驱动协作任务。具体而言，我们开发了一个双智能体协作绘图游戏 CoDraw。游戏发生在一个包含可移动剪贴画对象的虚拟世界中，涉及两名玩家：讲述者（Teller）和画者（Drawer）。讲述者看到一个包含多件剪贴画、按语义有意义方式排布的抽象场景，画者则尝试用可用的剪贴画在空白画布上重建该场景。两名玩家使用自然语言交流。我们收集了 CoDraw 数据集，包含人类玩家之间约 1 万段对话、约 13.8 万条消息。我们为这一测试平台定义了评估学习智能体的协议与指标，并强调需要一种新颖的「串扰」（crosstalk）评估条件——把在不相交训练子集上独立训练的智能体配对。我们为该任务提出了模型，并使用全自动评估以及与人类实时对弈两种方式对其进行基准测试。

**面向任务型对话中组合表示的神经 NLG 约束解码（Constrained Decoding for Neural NLG from Compositional Representations in Task-Oriented Dialogue）**
Anusha Balakrishnan、Jinfeng Rao、Kartikeya Upasani、Michael White、Rajen Subba
从结构化语义表示生成流畅的自然语言回复，是任务型会话系统的关键一步。E2E NLG Challenge 等赛事推动了该问题的神经方法尤其是序列到序列（seq2seq）模型的发展。然而，所用的语义表示往往欠规格，这加重了生成模型在句子规划上的负担，也限制了在线系统中生成回复的可控程度。在本文中，我们（1）提议使用树状语义表示（如传统基于规则的 NLG 系统所用），以获得更好的语篇级组织与句子级规划；（2）引入一个在天气领域使用这种表示的富有挑战的数据集；（3）提出一种针对 seq2seq 模型的约束解码方法，利用该表示提升语义正确性；（4）在我们自己的数据集和 E2E 数据集上展示了令人鼓舞的结果。

**对话自然语言推理（Dialogue Natural Language Inference）**
Sean Welleck、Jason Weston、Arthur Szlam、Kyunghyun Cho
一致性是对话模型长期面临的难题。在本文中，我们把对话智能体的一致性表述为自然语言推理（NLI），并创建了一个名为 Dialogue NLI 的新数据集。我们提出的方法证明，在 Dialogue NLI 上训练的模型可用于改进对话模型的一致性，并通过人类评估以及专为衡量对话模型一致性设计的一组评估集上的自动指标对该方法进行了评估。

**ELI5：长篇问答（ELI5: Long-Form Question Answering）**
Angela Fan、Yacine Jernite、Ethan Perez、David Grangier、Jason Weston、Michael Auli
我们介绍了首个大规模长篇问答语料库——这一任务要求对开放式问题给出详尽、深入的回答。该数据集包含来自 Reddit 论坛「像给五岁小孩解释一样」（Explain like I'm Five，ELI5）的 27 万个帖子，这个线上社区为问题提供五岁儿童也能理解的回答。与现有数据集相比，ELI5 包含需要多句回答的多样问题。我们提供了大量网页文档来帮助回答问题。自动与人工评估显示，以多任务目标训练的抽象式模型优于传统 seq2seq、语言建模以及强抽取式基线。然而，我们最好的模型仍远不及人类水平——评估者在超过 86% 的情况下更青睐标准答案，未来仍有充足改进空间。

**通过忽略伪相关改进零样本神经机器翻译（Improved Zero-Shot Neural Machine Translation via Ignoring Spurious Correlations）**
Jiatao Gu、Yong Wang、Kyunghyun Cho、Victor O.K. Li
零样本翻译——翻译神经机器翻译（NMT）系统从未训练过的语言对——是多语言环境下训练系统时涌现的一种特性。然而，朴素的零样本 NMT 训练很容易失败，且对超参数设置敏感。其性能通常远逊于更传统的基于枢轴（pivot）的方法——后者借助第三种语言作枢轴翻译两次。在本工作中，我们通过定量分析源句与解码句语言 ID 之间的互信息，解决因捕捉伪相关而导致的退化问题。受此分析启发，我们提出两种简单而有效的方法：（1）解码器预训练；（2）回译。这些方法在三个具有挑战性的多语言数据集上较原始零样本翻译有显著提升（4～22 个 BLEU 点），并取得与枢轴方法相当或更好的结果。

**通过双曲嵌入从文本语料推断概念层级（Inferring Concept Hierarchies from Text Corpora via Hyperbolic Embeddings）**
Matthew Le、Stephen Roller、Laetitia Papaxanthos、Douwe Kiela、Maximilian Nickel
我们考虑从大型文本语料推断「是一个」（is-a）关系的任务。为此，我们提出一种结合双曲嵌入与 Hearst 模式的新方法。这一途径使我们可以为从分布式上下文推断概念层级设置恰当约束，同时能够预测缺失的 is-a 关系并纠正错误抽取。此外——与其他方法不同——双曲空间的层级本质使我们能学到高度高效的表示，并改进推断层级的分类学一致性。实验表明，我们的方法在多个常用基准上取得了最先进的性能。

**做笔记：带草稿板编码器的条件自然语言生成（Keeping Notes: Conditional Natural Language Generation with a Scratchpad Encoder）**
Ryan Benmalek、Madian Khabsa、Suma Desu、Claire Cardie、Michele Banko
我们提出「草稿板机制」（Scratchpad Mechanism）——序列到序列（seq2seq）神经网络架构的一项新颖补充，并证明它能有效提升 seq2seq 模型在自然语言生成任务上的整体流畅度。通过让解码器在每个时间步都能写入编码器的所有输出层，Scratchpad 可以把编码器当作一块「草稿板」内存，记录到目前为止已生成的内容，从而引导后续生成。我们在三个被充分研究的自然语言生成任务——机器翻译（MT）、问题生成和文本摘要——的语境下评估 Scratchpad，在每个任务的标准数据集上取得最先进或相当的性能。人类评判（问题生成）、注意力可视化（MT）和输出样例（摘要）等定性评估，进一步证明了 Scratchpad 生成流畅且富有表现力输出的能力。

**部署后从对话中学习：喂饱你自己，聊天机器人！（Learning from Dialogue after Deployment: Feed Yourself, Chatbot!）**
Braden Hancock、Antoine Bordes、Pierre-Emmanuel Mazare、Jason Weston
对话智能体一生中所见的大多数对话，发生在它已被训练并部署之后，这留下了大量未开发的潜在训练信号。在本工作中，我们提出「自喂食」聊天机器人（self-feeding chatbot）——一种能从其参与的对话中提取新训练样本的对话智能体。当我们的智能体进行对话时，它还会估计用户对其回复的满意程度。当对话看起来进展顺利时，用户的回复成为供模仿的新训练样本；当智能体认为自己犯了错误时，它会请求反馈，而学会预测将获得的反馈能进一步提升聊天机器人的对话能力。在拥有超过 13.1 万个训练样本的 PERSONACHAT 闲聊数据集上，我们发现无论传统监督数据量多少，自喂食聊天机器人的对话学习都显著提升了性能。

**用四元数网络实现轻量高效的神经自然语言处理（Lightweight and Efficient Neural Natural Language Processing with Quaternion Networks）**
Yi Tay、Aston Zhang、Anh Tuan Luu、Jinfeng Rao、Shuai Zhang、Shuohang Wang、Jie Fu、Siu Cheung Hui
许多最先进的 NLP 神经模型参数量巨大，因而内存效率低下。本文为一系列自然语言处理（NLP）任务提出了一组轻量且内存高效的神经架构。为此，我们的模型利用四元数代数与超复数空间的计算，不仅实现了富有表现力的组件间交互，还凭借 Hamilton 乘积中更少的自由度显著缩减（75%）了参数规模。我们提出多种模型的四元数变体，催生了四元数注意力模型、四元数 Transformer 等新架构。在一批 NLP 任务上的大量实验证明了所提四元数启发模型的效用：参数规模最高可缩减 75% 而性能无显著损失。

**基于多语言句子嵌入与边际的并行语料挖掘（Margin-Based Parallel Corpus Mining with Multilingual Sentence Embeddings）**
Mikel Artetxe、Holger Schwenk
机器翻译对训练数据的规模与质量高度敏感，这引发了收集和过滤大型并行语料的兴趣。在本文中，我们为此任务提出一种基于多语言句子嵌入的新方法。以往方法依赖最近邻检索并在余弦相似度上设硬阈值，与之不同，我们提出的方法考虑了该度量的尺度不一致性，转而考察给定句对与其最近候选之间的边际（margin）。实验显示相较现有方法有大幅改进。我们在 BUCC 挖掘任务和 UN 重建任务上分别以超过 10 个 F1 点和 30 个精度点击败了已发表的最佳结果。用我们的方法过滤英德 ParaCrawl 语料后，在 newstest2014 上获得 31.2 BLEU，比最佳官方过滤版本高出 1 点多。

**工具小姐与水果先生：学习物体可供性的智能体中的涌现交流（Miss Tools and Mr Fruit: Emergent Communication in Agents Learning about Object Affordances）**
Diane Bouchacourt、Marco Baroni
近期研究关注被分配联合任务的深度网络智能体社群中的交流涌现，希望借此洞察人类语言的演化。我们在此提出一个新任务，它捕捉了人类环境的关键面向（如自然物体可供性）以及人类对话的关键面向（如参与者之间的完全对称）。通过对涌现协议进行细致的语用与语义分析，我们表明智能体通过真正的双边指称交流解决了共享任务。然而，智能体发展出了多种「个人方言」（idiolects），这使我们得出结论：完全对称并非共同语言涌现的充分条件。

**论深层子句嵌入的分布：一项大规模跨语言研究（On the Distribution of Deep Clausal Embeddings: A Large Cross-Linguistic Study）**
Damian Blasi、Ryan Cotterell、Lawrence Wolf-Sonkin、Sabine Stoll、Balthasar Bickel、Marco Baroni
把一个子句嵌入另一个子句（「那个[喜欢跑得快的[汽车]的女孩]到了」）是一种基础资源，被认为是语言表达力的关键驱动力。正因如此，它在关于「人类语言独特之处及其可能如何演化」的根本争论中占据核心地位。然而，关于嵌入的普遍性与限度的经验证据，一直基于实验室设置或规模相对有限的语料数据。我们在此引入 17 种语言的大型依存句法标注书面语料集合，使我们首次能够通过依存图捕捉子句嵌入并评估其分布。结果表明，没有证据显示存在对嵌入深度的硬性约束：深度分布的尾部很重。此外，尽管深层嵌套子句往往更短（暗示处理负载问题），含大量嵌入的复杂句子并未表现出偏向更浅嵌入的趋势。综合来看，这些结果表明书面语言并不排斥深层嵌入。更广泛地说，我们的研究展示了最新一代大数据 NLP 的资源与方法如何能为理论语言学的根本问题提供新视角。

**OpenDialKG：基于知识图谱注意力游走的可解释会话推理（OpenDialKG: Explainable Conversational Reasoning with Attention-Based Walks over Knowledge Graphs）**
Seungwhan Moon、Pararth Shah、Anuj Kumar、Rajen Subba
我们研究一种会话推理模型，它在大型常识知识图谱（KG）上策略性地游走，以引入引人入胜且上下文多样的实体与属性。为此，我们收集了一个新的开放式对话-KG 平行语料 OpenDialKG：来自 1.5 万段人类角色扮演对话的每条话语，都人工标注了对应实体与路径的真值参照，KG 含超过 100 万条事实。随后，我们提出 DialKG Walker 模型，把对话上下文的符号转移学习为 KG 上的结构化游走，并通过新颖的领域无关、基于注意力的图路径解码器，预测给定先前对话上下文后适合引入的自然实体。自动与人工评估表明，无论域内还是跨域任务，我们的模型都能比最先进基线或基于规则的模型检索到更自然、更像人类的回复。所提模型还为每个检索到的实体生成一条 KG 游走路径，为会话推理提供了自然的可解释方式。

**指称阅读器：用于指代消解的循环实体网络（The Referential Reader: A Recurrent Entity Network for Anaphora Resolution）**
Fei Liu、Luke Zettlemoyer、Jacob Eisenstein
我们提出一种在在线文本处理过程中存储和访问实体提及的新架构。在阅读文本时，实体指称被识别，并可以通过更新或覆盖定长内存中的某个单元来存储。更新操作意味着与同一单元中存储的其他提及同指；覆盖操作则使这些提及被遗忘。通过把内存操作编码为可微门，模型可以端到端训练，同时使用有监督指代消解目标和辅助语言建模目标。在一个代词-人名指代数据集上的评估显示，纯增量式文本处理即可取得强劲性能。

**面向长叙事阅读理解的简单有效的课程指针-生成器网络（Simple and Effective Curriculum Pointer-Generator Networks for Reading Comprehension over Long Narratives）**
Yi Tay、Shuohang Wang、Anh Tuan Luu、Jie Fu、Minh C. Phan、Xingdi Yuan、Jinfeng Rao、Siu Cheung Hui、Aston Zhang
本文处理长叙事上的阅读理解问题，文档动辄跨越数千 token。我们提出基于课程学习（CL）的指针-生成器框架，用于在大型文档上阅读/采样，基于「交替上下文难度」的理念实现神经模型的多样化训练。这可以解释为一种域随机化和/或训练期间的生成式预训练。为此，指针-生成器的使用放宽了「答案必须位于上下文中」的要求，使我们能构建多样的训练样本供学习。此外，我们提出新的内省对齐层（Introspective Alignment Layer，IAL），使用基于块的自注意力对分解后的对齐进行推理。我们在 NarrativeQA 阅读理解基准上评估所提方法，取得最先进性能，BLEU-4 相对现有基线提升 51%，Rouge-L 相对提升 17%。大量消融实验证实了 IAL 与 CL 组件的有效性。

**构建故事生成的策略（Strategies for Structuring Story Generation）**
Angela Fan、Mike Lewis、Yann Dauphin
作家写长篇故事时常依赖大纲或草图，但当前大多数语言模型都是从左到右逐词生成。我们探索用于创作数百词叙事文本的由粗到细模型，并引入通过抽象动作与实体来分解故事的新模型。模型先生成文本的谓词-论元结构，其中同一实体的不同提及用占位符标记；然后生成该谓词-论元结构的表层实现；最后把实体占位符替换为上下文敏感的名称和指称。人类评判更喜欢我们模型生成的故事，胜过此前一系列层级式文本生成方法。大量分析表明，我们的方法有助于提升生成故事中事件与实体的多样性和连贯性。

**迈向共情开放域对话模型：新基准与数据集（Towards Empathetic Open-Domain Conversation Models: A New Benchmark and Dataset）**
Hannah Rashkin、Eric Michael Smith、Margaret Li、Y-Lan Boureau
对话智能体面临的一个挑战是识别对话对象的感受并据此回复——这是一项关键的沟通技能。对人类而言，在对话中识别并回应他人的感受轻而易举，但对 AI 系统来说却是重大挑战，因为缺乏合适的公开数据集用于训练与评估。本工作提出了一个新的共情对话生成基准，以及 EMPATHETICDIALOGUES——一个包含 2.5 万段基于情绪情境的对话的新数据集。我们的实验表明，与仅在大规模网络对话数据上训练的模型相比，使用我们数据集的对话模型在人类评估者眼中更具共情能力。我们还对面向共情回复的对话模型适配进行了实证比较，利用现有模型或数据集而无需对完整模型进行耗时重训。

**迈向语言无关的通用表示（Towards Language Agnostic Universal Representations）**
Armen Aghajanyan、Xia Song、Saurabh Tiwary
当一个双语学生学会用一种语言解数学应用题时，我们期望该学生能用其精通的两种语言解题，即便数学课只用其中一种语言教授。然而，机器学习中当前的表示是依赖语言的。在本工作中，我们提出一种把语言与问题解耦的方法：学习语言无关的表示，从而可以用一种语言训练模型，以零样本方式应用到另一种语言。我们受语言学启发——特别是普遍语法假说——学习语言无关的通用潜在表示（Chomsky，2014；Montague，1970）。我们通过以下方式展示这些表示的能力：使用语言无关表示在单一语言上训练的模型，在其他语言上取得非常接近的准确率。

**通过边际化切分训练混合语言模型（Training Hybrid Language Models by Marginalizing over Segmentations）**
Edouard Grave、Sainbayar Sukhbaatar、Piotr Bojanowski、Armand Joulin
在本文中，我们研究混合语言建模问题，即使用既能预测字符又能预测字符 n-gram 或词等更大单元的模型。使用这类模型时，一个给定字符串通常存在多种潜在切分，例如一种用词、一种只用字符。因此，字符串的概率是所有可能切分概率之和。在这里，我们展示如何高效地对切分做边际化，以计算序列的真实概率。我们在包含七种语言的三个数据集上应用该技术，相比强字符级语言模型有所提升。

**翻译「翻译体」：无监督机器翻译的两步方法（Translating Translationese: A Two-Step Approach to Unsupervised Machine Translation）**
Nima Pourdamghani、Nada Aldarrab、Marjan Ghazvininejad、Kevin Knight、Jonathan May
给定源语言句子的粗糙逐词直译，目标语言母语者能够还原出译文背后完全流畅的表达。在本工作中，我们探索这一直觉，把翻译拆成两步：先用词典生成粗糙直译，再把得到的伪译文——「翻译体」（Translationese）——「翻译」成完全流畅的译文。我们从一堆以目标语言为共同语言的平行数据中一次性构建翻译体解码器，然后可按需用无监督技术构建词典，从而快速生成面向众多源语言的无监督神经 MT 系统。我们把这一流程应用于 14 种测试语言，在高资源语言上取得比此前发表的无监督 MT 研究更好或相当的结果，并在此前从未用于无监督 MT 场景的低资源语言上获得高质量结果。

**通过完形填空翻译的无监督问答（Unsupervised Question Answering by Cloze Translation）**
Patrick Lewis、Ludovic Denoyer、Sebastian Riedel
为问答（QA）获取训练数据耗时耗力，且现有 QA 数据集只覆盖有限的领域和语言。在本工作中，我们探索高质量训练数据对抽取式 QA 究竟有多必需，并研究无监督抽取式 QA 的可能性。我们首先以无监督方式学习生成「上下文-问题-答案」三元组，再用它们自动合成抽取式 QA 训练数据。为生成这样的三元组，我们先从大型文档语料中随机采样上下文段落，再从段落中随机选取名词短语或命名实体提及作为答案；接着把上下文中的答案转换为挖空完形填空问题，最后将其翻译为自然问题。我们提出并比较了多种无监督的完形填空到自然问题的翻译方法，包括利用自然问题与完形填空问题的非对齐语料训练无监督 NMT 模型，以及基于规则的方法。我们发现，现代 QA 模型仅用合成训练数据就能出人意料地学会回答人类问题。我们证明，完全不使用 SQuAD 训练数据，我们的方法在 SQuAD v1 上达到 56.4 F1（答案为命名实体提及时为 64.5 F1），胜过早期的有监督模型。

**深度智能体涌现交流中的词序偏好（Word-Order Biases in Deep-Agent Emergent Communication）**
Rahma Chaabouni、Evgeny Kharitonov、Alessandro Lazari、Emmanuel Dupoux、Marco Baroni
序列处理神经网络在许多 NLP 任务上取得了显著进展。因此，人们越来越有兴趣了解它们在多大程度上像人类一样处理语言。我们的目标是揭示这类模型对自然词序约束表现出哪些偏好。我们训练模型在简单网格世界中交流路径，所用微型语言或遵循、或违反多种自然语言趋势，如避免冗余的倾向或最小化长距离依赖。我们研究微型语言的受控特性如何影响个体学习及其在多个网络世代间的稳定性。结果喜忧参半：一方面，神经网络表现出避免长距离依赖的强烈倾向；另一方面，对于自然语言中广泛证实的对高效、非冗余信息编码的偏好，则没有明确倾向。因此我们建议向神经网络注入「代价」概念，作为使其语言行为更像人类的可能途径。

## ACL 的研讨会与教程

**面向对话式 AI 的 NLP**
受邀报告：《Putting Together the Threads of Conversational AI?》——Jason Weston
论文：《OpenDialKG: Explainable Conversational Reasoning with Attention-Based Walks over Knowledge Graphs》——Seungwhan Moon、Pararth Shah、Anuj Kumar、Rajen Subba

**SIGMORPHON**
受邀报告：《Grammatical gender: What does it mean?》——Adina Williams

**WMT @ ACL**
论文：《Facebook FAIR's WMT19 News Translation Task Submission》——Nathan Ng、Kyra Yee、Alexei Baevski、Myle Ott、Michael Auli、Sergey Edunov
论文：《Findings of the WMT 2019 Shared Task on Parallel Corpus Filtering for Low-Resource Conditions》——Philipp Koehn、Francisco Guzmán、Vishrav Choudhary、Juan Pino
论文：《Low-Resource Corpus Filtering Using Multilingual Sentence Embeddings》——Vishrav Chaudhary、Yuqing Tang、Francisco Guzmán、Holger Schwenk、Philipp Koehn

**NLP 表示学习研讨会**
受邀报告：《Language Emergence as Representation Learning》——Marco Baroni
