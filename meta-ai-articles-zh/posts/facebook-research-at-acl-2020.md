---
title: "Facebook 研究团队在 ACL 2020"
title_en: "Facebook Research at ACL 2020"
date: 2020-07-03
source: https://ai.facebook.com/blog/facebook-research-at-acl-2020
crawled: 2026-09-22
translated: 2026-09-22
---

# Facebook 研究团队在 ACL 2020

> 原文：[Facebook Research at ACL 2020](https://ai.facebook.com/blog/facebook-research-at-acl-2020) · Meta AI（Wayback 存档）

2020 年 7 月 3 日

计算语言学协会（ACL）会议今年将于 7 月 5 日至 10 日在线上举行。Facebook 的研究者将通过视频 spotlight、海报环节和其他研讨会活动展示他们的工作。我们的研究员、招聘人员和计划经理会在各项活动中与大家交流 Facebook AI 的研究以及潜在的职业机会。我们将分享今年展示的研究细节，覆盖 NLP 的关键领域，包括预训练、跨语言、数据集与资源、对话、机器翻译、探针分析等。

## 预训练

众所周知，预训练是构建最先进 NLP 模型的重要步骤，BERT（来自 Transformer 的双向编码器表示）便是例证。然而，把 BERT 用于序列解码任务时，预训练的只有编码器，没有解码器。为填补这一空白，我们很高兴地分享 BART——一个专为序列到序列问题预训练的新模型，它不仅能在分类任务上媲美 RoBERTa，还在文本生成任务上取得新的最先进结果。BART 的训练方式是先用任意噪声函数破坏文本，再学习一个模型重建原文。我们已在此发布代码与模型。

据我们所知，Facebook AI 还是首个把语言建模预训练同时应用于文本与表格数据的研究团队。这一被称为 TaBERT 的架构在 2600 万张表格及其英文上下文上训练，提升了问答性能。我们还发布了首个面向法语的基于 transformer 的单语语言模型，在四个下游任务上超越了原有最先进水平。对于关注预训练与效率交叉领域的人，我们考察了下游文本分类任务，发现存在一个预训练可能并无必要的临界点。我们的研究结果表明，随着训练数据量增加，BERT 等预训练语言模型的收益可能递减。

预训练论文：

- 《BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension》——Mike Lewis、Yinhan Liu、Naman Goyal、Marjan Ghazvininejad、Abdelrahman Mohamed、Omer Levy、Ves Stoyanov、Luke Zettlemoyer
- 《CamemBERT: a Tasty French Language Model》——Louis Martin、Benjamin Muller、Pedro Javier Ortiz Suárez、Yoann Dupont、Laurent Romary、Éric Villemonte de la Clergerie、Djamé Seddah、Benoît Sagot
- 《TaBERT: Pretraining for Joint Understanding of Textual and Tabular Data》——Pengcheng Yin、Graham Neubig、Wen-tau Yih、Sebastian Riedel
- 《To Pretrain or Not to Pretrain: Examining the Benefits of Pretraining on Resource Rich Tasks》——Sinong Wang、Madian Khabsa、Hao Ma

## 跨语言

Facebook AI 的另一个核心聚焦领域是跨语言研究：模型在一种语言上训练，然后无需额外训练数据即可用于其他语言。我们将展示 XLM-R——我们执行 100 种语言（包括低资源语言）跨语言任务的最先进模型。作为首个胜过依赖预训练模型的传统单语基线的多语言模型，它在四个基准上取得最先进结果，其中包括我们的问答数据集 MLQA——我们也将在 ACL 2020 上展示它。XLM-R 模型已在 GitHub、HuggingFace Transformers 和 PyText 上公开。我们还探索了跨语言模型的底层机制及其工作原理，将讨论一些有趣的、反直觉的发现：即使没有共享词表或领域，语言通用表示如何在预训练模型中涌现。此类研究除了推动 NLP 进步，还能帮助无论说何种语言的所有人获得更好体验。

跨语言论文：

- 《Unsupervised Cross-lingual Representation Learning at Scale》——Alexis Conneau、Kartikay Khandelwal、Naman Goyal、Vishrav Chaudhary、Edouard Grave、Guillaume Wenzek、Myle Ott、Ves Stoyanov、Luke Zettlemoyer
- 《Emerging Cross-lingual Structure in Pretrained Language Models》——Shijie Wu、Alexis Conneau、Haoran Li、Luke Zettlemoyer、Ves Stoyanov
- 《MLQA: Evaluating Cross-lingual Extractive Question Answering》——Patrick Lewis、Barlas Oguz、Ruty Rinott、Sebastian Riedel、Holger Schwenk

## 数据集与资源

数据集与基准在衡量和改进 NLP 模型性能方面扮演着关键角色。但过去几年，随着该领域飞速发展，当前的 NLP 基准可能趋于饱和和受限。正因如此，我们开发了新资源，帮助研究者更好地评估和改进模型。我们用一个独特的人机在环对抗过程构建了全新的大规模自然语言理解（NLU）基准，为 NLU 模型创造了一个永不停歇的移动靶标，而非一个很快就会饱和的静态基准。我们还引入两个额外资源，帮助研究者评估当前 NLU 模型的弱点。这项工作包括 ImpPRESS——一个新的语用推理评估数据集（例如，模型是否知道「约翰吃了一些饼干」通常会被理解为意味着他没有吃完所有饼干？），以及一个新的句子简化数据集。

数据集论文：

- 《Adversarial NLI: A New Benchmark for Natural Language Understanding》——Yixin Nie、Adina Williams、Emily Dinan、Mohit Bansal、Jason Weston、Douwe Kiela
- 《Are Natural Language Inference Models IMPPRESsive? Learning IMPlicature and PRESupposition》——Paloma Jeretic、Alex Warstadt、Suvrat Bhooshan、Adina Williams
- 《ASSET: A Dataset for Tuning and Evaluation of Sentence Simplification Models with Multiple Rewriting Transformations》——Fernando Alva Manchego、Louis Martin、Antoine Bordes、Carolina Scarton、Benoit Sagot、Lucia Specia

## 对话

我们将展示开放域闲聊、任务型对话以及通用神经文本生成方面的进展。我们构建并开源了有史以来最大的开放域聊天机器人，它能融合来自不同对话任务的对话技能——如共情、知识和个性。我们还构建了一个能以不同风格谈论图像的系统，并发布了包含 20 万个图像-对话对的新数据集。另外，我们引入了一种新的对话评估指标——与大多数工具不同，它不需要人类参考话语或直接人工评估，仍与人类判断高度相关。我们还研究了大规模生成式对话模型跨任务泛化的能力，发布了一组独特的 12 个 GLUE 风格任务，称为 dodecadialogue 挑战。我们还为人类向虚拟或机器人助手下达指令这一面向语义解析的沟通方式，引入了大规模数据集与数据收集框架。我们用「非似然训练」改进对话文本生成，例如最小化重复、高频词滥用、逻辑缺陷以及照搬上下文。在对话之外，我们还用新的「检索-编辑-重排」框架改进了通用神经文本生成——先检索候选，再编辑，然后对编辑后的候选重排以产生最终输出。

对话论文：

- 《Can You Put It All Together: Evaluating Conversational Agents' Ability to Blend Skills》——Eric Smith、Mary Williamson、Kurt Shuster、Jason Weston、Y-Lan Boureau
- 《Don't Say That! Making Inconsistent Dialogue Unlikely with Unlikelihood Training》——Margaret Li、Stephen Roller、Ilia Kulikov、Sean Welleck、Y-Lan Boureau、Kyunghyun Cho、Jason Weston
- 《Image-Chat: Engaging Grounded Conversations》——Kurt Shuster、Samuel Humeau、Antoine Bordes、Jason Weston
- 《Learning an Unreferenced Metric for Online Dialogue Evaluation》——Koustuv Sinha、Prasanna Parthasarathi、Jasmine Wang、Ryan Lowe、Will Hamilton、Joelle Pineau
- 《The Dialogue Dodecathlon: Open-Domain Knowledge and Image Grounded Conversational Agents》——Kurt Shuster、Dexter Ju、Stephen Roller、Emily Dinan、Y-Lan Boureau、Jason Weston
- 《Simple and Effective Retrieve-Edit-Rerank Text Generation》——Nabil Hossain、Marjan Ghazvininejad、Luke Zettlemoyer
- 《CraftAssist Instruction Parsing: Semantic Parsing for a Minecraft Assistant》——Yacine Jernite、Kavya Srinet、Jonathan Gray、Arthur Szlam

## 机器翻译

对机器翻译系统的评估仍是一个开放的研究难题。例如，为什么人类评估者偏爱的最佳回译系统在 BLEU 等自动指标上表现更差？我们详细研究了这一差异，仔细剖析了标准评估协议，并就如何改进自动评估提出建议，例如用语言模型得分补充 BLEU 以衡量流畅度。我们还提出了一种全新的 MT 评估替代方案：不使用模型生成的第一优翻译，而是依靠用多种采样技术从模型搜索空间生成的一组多样假设。我们发现这样得到的评估更稳健，与人类判断的相关性更好。这项工作帮助我们无需额外人工参考就能更好、更高效地衡量 MT 系统质量。在另一项工作中，我们分析了当前质量估计公开数据集的现状，发现了关键缺陷，如对流利的偏置和主题多样性不足。我们提出了改进数据集质量的具体建议——这是整体上改进质量估计模型的重要一步。这项工作引导我们创建了 MLQE——一个从维基百科抽取的多语言数据集，社区正在 WMT 的多语言质量估计共享任务中使用它。在另一项工作中，我们利用隐变量改进模型，在多个语言对上提升翻译质量，尤其是训练数据含噪时。

机器翻译论文：

- 《Multi-Hypothesis Machine Translation Evaluation》——Marina Fomicheva、Paco Guzmán、Lucia Specia
- 《Are We Estimating or Guesstimating Translation Quality?》——Shuo Sun、Paco Guzmán、Lucia Specia
- 《On the Evaluation of Machine Translation Systems Trained with Back-Translation》——Sergey Edunov、Myle Ott、Marc'Aurelio Ranzato、Michael Auli
- 《Addressing Posterior Collapse with Mutual Information for Improved Variational Neural Machine Translation》——Arya D. McCarthy、Xian Li、Jiatao Gu、Ning Dong

## 探针分析

要改进 NLP 模型，理解它们在哪里失败、在哪里成功至关重要。理解 NLP 模型的一种常见方法是训练「探针」（probe）——旨在发现其他模型输出表示中隐藏语言结构的模型。我们将展示一系列论文，阐明这些探针如何工作，并鼓励研究者重新思考训练探针的方法。例如，我们论证更大、更复杂的探针优于更常见、更直觉的简单方法。借助新颖的信息论视角，复杂探针的效用变得更加直观。在另一项工作中，我们将一种新探针与传统句法器比较，表明探针与被其探测的模型并无本质区别。在互补研究中，我们创建了一个新颖数据集，检验词在我们的 NLP 模型中是否对句子含义有一致贡献。我们发现这些模型倾向于以允许单个词的含义随上下文变化的方式进行泛化。

探针论文：

- 《A Tale of a Probe and a Parser》——Rowan Hall Maudsley、Joseph Valvoda、Tiago Pimentel、Adina Williams、Ryan Cotterell
- 《Probing Linguistic Similarity》——Emily Goodwin、Koustuv Sinha、Timothy J. O'Donnell
- 《Information-Theoretic Probing for Linguistic Structure》——Tiago Pimentel、Joseph Valvoda、Rowan Hall Maudsley、Ran Zmigrod、Adina Williams、Ryan Cotterell

## 涌现语言、消歧等研究

除上述研究外，我们还将展示一批不属于上述类别的值得关注的论文：

**《Active Learning for Coreference Resolution Using Discrete Annotation》**——Belinda Z. Li、Gabriel Stanovsky、Luke Zettlemoyer
我们改进了指代消解主动学习中的成对标注：当呈现的提及对被判定为不同指时，请标注者指出该提及的先行词。这一简单修改结合一种新颖的提及聚类算法（用于选择标注哪些样本），在单位标注预算下获得的性能大幅提升。在现有基准指代数据集上的实验表明，这一附加问题的信号带来了单位人工标注小时的显著性能增益。未来工作可以使用我们的标注协议为新领域高效开发指代模型。代码已公开。

**《Asking and Answering Questions to Evaluate the Factual Consistency of Summaries》**——Alex Wang、Kyunghyun Cho、Mike Lewis
抽象式摘要模型的实际应用受限于其输出与输入频繁出现的事实不一致。现有的摘要自动评估指标对这类错误大多不敏感。我们提出名为 QAGS（读作「kags」）的自动评估协议，旨在识别生成摘要中的事实不一致。QAGS 基于这样的直觉：如果我们分别就摘要及其来源提问，若摘要与来源事实一致，则应得到相似答案。为评估 QAGS，我们收集了对 CNN/DailyMail（Hermann 等，2015）和 XSUM（Narayan 等，2018）摘要数据集上模型生成摘要的事实一致性人工判断。QAGS 与这些判断的相关性远高于其他自动评估指标。此外，QAGS 提供了天然的可解释性形式：计算 QAGS 过程中生成的答案与问题指出了摘要中哪些 token 不一致以及原因。我们相信 QAGS 是自动生成可用且事实一致文本的有前景工具。

**《Compositionality and Generalization In Emergent Languages》**——Rahma Chaabouni、Eugene Kharitonov、Diane Bouchacourt、Emmanuel Dupoux、Marco Baroni
自然语言允许我们按照系统性规则组合表示各部分的表达式来指称新的复合概念，这一性质称为组合性（compositionality）。在本文中，我们研究深度多智能体仿真中涌现的语言是否具备指称新原始组合的类似能力，以及它是否通过类似人类语言组合性的策略实现这一目标。借助受表示学习解耦启发的新方法来度量涌现语言的组合性，我们确立了三个主要结果。第一，给定足够大的输入空间，涌现语言会自然发展出指称新复合概念的能力。第二，涌现语言的组合性程度与其泛化能力之间没有相关性。第三，虽然组合性对泛化并非必要，但它在语言传播方面具有优势：语言越具组合性，新学习者越容易习得，即便后者与原智能体架构不同。我们的结论是：组合性并非源于简单的泛化压力，但如果一种涌现语言碰巧具备组合性，它将更有可能存活和繁荣。

**《Joint Modeling of Emotion and Abusive Language Detection》**——Santhosh Rajamanickam、Pushkar Mishra、Helen Yannakoudakis、Ekaterina Shutova
在线交流平台的兴起伴随着一些不良影响，例如网络攻击性和辱骂行为的泛滥。为解决这一问题，自然语言处理（NLP）社区尝试了多种滥用检测技术。这些方法虽然取得了相当的成功，但迄今只关注评论语言属性和线上用户社群的建模，忽视了用户的情绪状态及其对语言的可能影响——而后者与辱骂行为密不可分。在本文中，我们提出首个情绪与辱骂语言检测的联合模型，在多任务学习框架中实验，使一个任务为另一个任务提供信息。结果表明，纳入情感特征在多个数据集上带来了辱骂检测性能的显著提升。

**《Language Models as Fact Checkers?》**——Nayeon Lee、Belinda Z. Li、Sinong Wang、Wen-tau Yih、Hao Ma、Madian Khabsa
近期工作表明，语言模型（LM）存储了从预训练数据学到的常识性与事实性知识。在本文中，我们利用这种隐式知识，仅用语言模型创建一个有效的端到端事实核查器，不依赖任何外部知识或显式检索组件。虽然此前从 LM 中提取知识的工作聚焦于开放域问答，但据我们所知，这是首个考察语言模型用作事实核查器的工作。在闭卷设置下，我们的零样本 LM 方法在标准 FEVER 任务上胜过随机基线，微调后的 LM 与标准基线相比也表现良好。尽管我们最终没有胜过使用显式知识库的方法，但我们相信这一探索表明该方法可行且大有可挖。

**《Moving Down the Long Tail of Word Sense Disambiguation with Gloss Informed Bi-encoders》**——Terra Blevins、Luke Zettlemoyer
词义消歧（WSD）的一大障碍是词义分布不均，导致现有模型在训练中罕见或未见过的词义上普遍表现不佳。我们提出一个双编码器模型，独立嵌入（1）目标词及其上下文，以及（2）每个词义的词典释义（gloss）。两个编码器在同一表示空间中联合优化，因此词义消解可通过为每个目标词嵌入寻找最近的词义嵌入来完成。我们的系统在英语全词 WSD 上超越了以往最先进模型；增益主要来自罕见词义的性能提升——较低频词义上相比先前工作减少了 31.1% 的错误。这证明通过建模词义定义可以更有效地消歧罕见词义。

**《On the Relationships Between the Grammatical Genders of Inanimate Nouns and Their Co-Occurring Adjectives and Verbs》**——Adina Williams、Ryan Cotterell、Lawrence Wolf-Sonkin、Damián Blasi、Hanna Wallach
我们使用六种有性语言的大规模语料以及 NLP 与信息论工具，检验无生命名词的语法性与用于描述这些名词的形容词之间是否存在关系。在全部六种语言中，我们都发现了统计显著的关系。我们还发现，无生命名词的语法性与以这些名词为直接宾语、间接宾语和主语的动词之间存在统计显著关系。对这些建模的更深入考察留待未来工作。

**《Predicting Declension Class from Form and Meaning》**——Adina Williams、Tiago Pimentel、Arya D. McCarthy、Hagen Blix、Eleanor Chodroff、Ryan Cotterell
许多自然语言的名词词库分为若干变格类（declension class），各具形态学特征。类别归属远非确定性，但名词的音系形式和/或含义往往能提供不完美的线索。在这里，我们考察这些线索的强度。更具体地说，我们通过测量「已知名词形式和/或含义时能获得多少比特的变格类信息」来将其操作化。我们知道形式和含义往往也提示语法性——而我们定量地证实了语法性本身也可与变格类共享信息——因此我们还对语法性做了控制。在两种印欧语（捷克语和德语）中，我们发现形式和含义分别与变格类共享大量信息（并在语法性之外贡献额外信息）。类别、形式与含义（给定语法性）的三方交互也显著。我们的研究之所以重要，原因有二：首先，我们引入了一种新方法，为「形式和含义与名词变格分类相关」这一经典语言学发现提供了额外的定量支持；其次，我们不仅表明单个变格类的线索强度在语言内部存在差异，还表明这些差异本身在语言之间也各不相同。

## Facebook AI 在 ACL 2020 的研讨会与教程

研讨会：

- 第 17 届国际口语翻译会议（IWSLT）同声语音翻译赛道，7 月 9 日与 10 日——Jiatao Gu、Juan Pino、Changhan Wang 为组织者。
- 第 2 届面向对话式 AI 的 NLP 研讨会，7 月 9 日——Antoine Bordes 为主题讲者，Anuj Kumar 为组织者。
- 第 1 届叙事理解、故事线与事件联合研讨会（NUSE），7 月 9 日——Angela Fan 为受邀讲者。
- 语言与视觉研究进展研讨会（ALVR），7 月 9 日——Xinlei Chen 为组织者。
- 第 5 届 NLP 表示学习研讨会（RepL4NLP-2020），7 月 9 日——Mike Lewis 为主题讲者，Fabio Petroni 为组织者。
- 第 1 届自然语言接口研讨会，7 月 10 日——Luke Zettlemoyer 为受邀讲者，Scott Wen-tau Yih 为组织者。
- 第 4 届神经生成与翻译研讨会，7 月 10 日——Jiatao Gu 为受邀讲者，Xian Li 为组织者。
- 第 1 届自动同声翻译研讨会，7 月 10 日——James Cross 为组织者。

教程：

- 开放域问答（前沿），7 月 5 日——Scott Wen-tau Yih 为组织者。
