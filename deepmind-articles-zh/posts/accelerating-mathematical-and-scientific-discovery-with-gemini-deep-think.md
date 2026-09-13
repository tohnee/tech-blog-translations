---
title: "用 Gemini Deep Think 加速数学与科学发现"
title_en: "Accelerating Mathematical and Scientific Discovery with Gemini Deep Think"
source: https://deepmind.google/blog/accelerating-mathematical-and-scientific-discovery-with-gemini-deep-think/
site: deepmind
date: 2026-02-11
crawled: 2026-09-13
translated: 2026-09-13
---

# 用 Gemini Deep Think 加速数学与科学发现

> 原文：[Accelerating Mathematical and Scientific Discovery with Gemini Deep Think](https://deepmind.google/blog/accelerating-mathematical-and-scientific-discovery-with-gemini-deep-think/) · Google DeepMind

你的浏览器不支持 audio 元素。

**收听本文** 10 分钟

在数学家与科学家的专业指导下，Gemini Deep Think 正在解决数学、物理和计算机科学领域的专业研究问题

2025 年夏天，Gemini Deep Think 的一个进阶版本[在国际数学奥林匹克竞赛（IMO）中达到金牌水准](https://goo.gle/imo-gold)；随后，一个更新的版本又在国际大学生程序设计竞赛（ICPC）中[取得了类似的成绩](https://deepmind.google/blog/gemini-achieves-gold-medal-level-at-the-international-collegiate-programming-contest-world-finals/)。这些结果表明，该模型能够对一些为学生设计、最具挑战性的数学与编程问题进行推理。自那以后，Gemini Deep Think 模式已进入科学、工程和企业工作流程，去应对更复杂、更开放性的挑战。

上周，我们的团队发表了两篇论文（[1](https://arxiv.org/abs/2602.10177)、[2](https://arxiv.org/abs/2602.03837)），详细介绍了一项跨学科工作：使用 Gemini Deep Think 模式解决专业研究问题。这些成果源自数学家、物理学家和计算机科学家之间的深度协作。

## 纯数学的前沿

与 IMO 试题不同，研究级数学需要来自浩瀚文献的先进技巧。基础模型虽然拥有庞大的知识库，但在高深主题上，数据稀缺往往导致理解肤浅和幻觉。

为了解决这个问题，我们构建了一个数学研究智能体（内部代号 Aletheia），由 Gemini Deep Think 模式驱动。它配备了一个自然语言验证器，用于识别候选解中的缺陷，并支持生成与修订解的迭代过程。至关重要的是，这个智能体能够承认自己未能解出问题——这一关键特性提升了研究人员的效率。

此外，该研究智能体还使用 Google 搜索和网页浏览来检索复杂的研究资料，从而在综合已发表文献时避免虚假引用和计算错误。

![题为「Aletheia: Powered by Gemini Deep Think」的流程图，展示了一个多步骤的解验证过程。中央线性路径从「Problem（问题）」到「Generator（生成器）」，再到「Candidate solution（候选解）」，然后是「Verifier（验证器）」，最后到「Final output（最终输出）」。验证器作为一个决策点，带有三条反馈回路：正确：直接进入「Final output」。需要小修：经由「Reviser（修订器）」返回更新「Candidate solution」。存在严重缺陷：触发红色虚线返回「Generator」，重启该过程。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/DeepThink-maths-science-discovery__figure-01-Aletheia__light_UP14tvS.svg)![题为「Aletheia: Powered by Gemini Deep Think」的流程图，展示了一个多步骤的解验证过程。中央线性路径从「Problem（问题）」到「Generator（生成器）」，再到「Candidate solution（候选解）」，然后是「Verifier（验证器）」，最后到「Final output（最终输出）」。验证器作为一个决策点，带有三条反馈回路：正确：直接进入「Final output」。需要小修：经由「Reviser（修订器）」返回更新「Candidate solution」。存在严重缺陷：触发红色虚线返回「Generator」，重启该过程。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/DeepThink-maths-science-discovery__figure-01-Aletheia__dark_MQtmOaf.svg)

Aletheia 概览：一个由 Deep Think 驱动、可针对研究级数学问题迭代地生成、验证和修订解的数学研究智能体。

自 2025 年 7 月达到 IMO 金牌水准以来，Gemini Deep Think 进展迅速：随着推理时计算规模的扩大，它在 IMO-ProofBench Advanced [测试](https://imobench.github.io/)中最高取得 90% 的得分。我们证明，随着我们超越奥赛级别、进入博士级练习（依据我们内部的 FutureMath Basic 基准），标度律依然成立。值得注意的是，Aletheia 展示了可以在更低的推理时计算下获得更高的推理质量。

![题为「IMO-ProofBench Advanced (Olympiad level)」的折线图，比较了 Gemini Deep Think 两个版本与名为 Aletheia 的基准的表现。纵轴为得分百分比（30% 至 90%），横轴为对数刻度的推理时计算。2026 年 1 月版本（浅蓝）始终优于 2025 年 7 月版本（深蓝），两者随算力增加均呈稳定上升趋势。2026 年 1 月版本峰值约为 90%，几乎触及位于略高于 90% 处的 Aletheia 基准（绿色星标）。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/DeepThink-maths-science-discovery__figure-01-chart__light.svg)![题为「IMO-ProofBench Advanced (Olympiad level)」的折线图，比较了 Gemini Deep Think 两个版本与名为 Aletheia 的基准的表现。纵轴为得分百分比（30% 至 90%），横轴为对数刻度的推理时计算。2026 年 1 月版本（浅蓝）始终优于 2025 年 7 月版本（深蓝），两者随算力增加均呈稳定上升趋势。2026 年 1 月版本峰值约为 90%，几乎触及位于略高于 90% 处的 Aletheia 基准（绿色星标）。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/DeepThink-maths-science-discovery__figure-01-chart__dark.svg)

截至 2026 年 1 月的 Deep Think 最新进阶版本，在奥赛级问题上显著超越了 IMO 金牌版本（2025 年 7 月）。Aletheia 则以更低的推理时计算，在推理质量上实现了进一步飞跃。所有结果均由人类专家评分。

![题为「(b) FutureMath Basic (Ph.D level exercises)」的折线图，绘制了 Gemini Deep Think（2026 年 1 月）的得分随推理时计算（对数刻度）增加的变化。纵轴为得分百分比（0% 至 45%）。表现从 0% 起步，呈现波动的上升趋势，先达到 30% 的早期峰值，随后起伏，最终攀升至约 38% 的高点。代表「Aletheia」的绿色星标作为基准标记在约 46% 处，显著高于模型所达到的最高表现。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/DeepThink-maths-science-discovery__figure-02-chart__light.svg)![题为「(b) FutureMath Basic (Ph.D level exercises)」的折线图，绘制了 Gemini Deep Think（2026 年 1 月）的得分随推理时计算（对数刻度）增加的变化。纵轴为得分百分比（0% 至 45%）。表现从 0% 起步，呈现波动的上升趋势，先达到 30% 的早期峰值，随后起伏，最终攀升至约 38% 的高点。代表「Aletheia」的绿色星标作为基准标记在约 46% 处，显著高于模型所达到的最高表现。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/DeepThink-maths-science-discovery__figure-02-chart__dark.svg)

推理时标度律同样可以迁移到博士级练习。

在研究级数学方面，Aletheia 已经通过不同程度的自主研究催生了若干进展：

- 可靠的自主研究。一篇完全由 AI 生成、没有任何人工干预的研究论文（[Feng26](https://arxiv.org/abs/2601.23245)），计算了算术几何中称为「特征权重（eigenweights）」的某些结构常数。
- AI 引导的协作。一篇研究论文（[LeeSeo26](https://arxiv.org/abs/2602.02450)），展示了人机协作证明称为「独立集（independent sets）」的相互作用粒子系统的界。
- 一项大规模半自主评估（[Feng et al., 2026b](https://arxiv.org/abs/2601.22401）），针对 Bloom 的埃尔德什猜想[数据库](https://www.erdosproblems.com/)中的 700 个开放问题，其中包括对其中列出的四个开放问题的自主求解。在 Erdős-1051 上，我们的模型自主求解并促成了一个在研究论文（[BKKKZ26](https://arxiv.org/abs/2601.21442)）中报告的推广。

该智能体还为另外两篇论文（[FYZ26](https://arxiv.org/abs/2601.18557)）和（[ACGKMP26](https://arxiv.org/abs/2601.23229)）贡献了中间命题。同样值得注意的是，此前已有在较小规模上（就合作数量和所处理问题数量而言）使用 Gemini 进行研究级数学的[工作](https://arxiv.org/abs/2601.07222)。

在与数学界广泛讨论之后，我们提出了一套分类法，按重要性和 AI 贡献程度对 AI 辅助的数学研究进行分类——以此参与关于 AI 生成结果的负责任记录、评估与传播的更广泛讨论。属于第 2 级（「可发表质量」）的工作已提交给知名期刊。目前，我们不宣称任何第 3 级（「重大进展」）和第 4 级（「里程碑式突破」）的成果。

![题为「Classification of all AI-assisted mathematics results encompassed in this work」的表格，按新颖性和协作类型对研究分类。Level 0（自主）：Erdős-652、654、1040（Feng et al., 2026b）。Level 1（自主）：Erdős-1051（Feng et al., 2026b）。Level 2（人类 + AI）：复杂度界（ACGKMP26）与算术体积（FYZ26）。Level 2（协作）：独立多项式（LeeSeo26）与广义 Erdős-1051（BKKKZ26）。Level 2（自主）：特征权重（Feng26）。Level 3 与 Level 4 目前为空。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/DeepThink-maths-science-discovery__figure-04-table__light.svg)![题为「Classification of all AI-assisted mathematics results encompassed in this work」的表格，按新颖性和协作类型对研究分类。Level 0（自主）：Erdős-652、654、1040（Feng et al., 2026b）。Level 1（自主）：Erdős-1051（Feng et al., 2026b）。Level 2（人类 + AI）：复杂度界（ACGKMP26）与算术体积（FYZ26）。Level 2（协作）：独立多项式（LeeSeo26）与广义 Erdős-1051（BKKKZ26）。Level 2（自主）：特征权重（Feng26）。Level 3 与 Level 4 目前为空。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/DeepThink-maths-science-discovery__figure-04-table__dark.svg)

本文涵盖的所有 AI 辅助数学成果的分类。\* 表中列为 Level 2 的工作已提交发表。

提示词与模型输出可在[此处](https://github.com/google-deepmind/superhuman/tree/main/aletheia)获取。关于 AI 贡献的讨论、我们的「人机交互卡片（Human-AI Interaction card）」以及社区影响，请参见我们的[论文](https://arxiv.org/abs/2602.10177)。

## 扩展到物理学与计算机科学

Gemini Deep Think 模式在计算机科学和物理学中也展现出了前景。[第二篇论文](http://arxiv.org/abs/2602.03837)建立在类似的智能体化推理思想之上，识别出了有效的协作「配方」，特别是「Advisor（顾问）」模式：人类通过迭代式的「氛围证明（Vibe-Proving）」循环引导 AI，以验证直觉并完善证明。我们还详述了诸如「平衡提示词（balanced prompting）」——同时请求证明*或*反驳以防止确认偏误——以及代码辅助验证等战术性技巧。这些方法，加上模型通过深层结构关联连接不同科学领域的能力，正在改变理论研究的方式。这项工作建立在我们成功部署 Gemini Deep Think 进阶版本、协助[为 STOC’26 会议评审计算机科学理论论文](https://research.google/blog/gemini-provides-automated-feedback-for-theoretical-computer-scientists-at-stoc-2026/)的基础之上。

![题为「Network layer」的流程图，展示了一个深度推理过程。顶部一个标注为「Extensive exploration of solution space（解空间的大规模探索）」的括号汇聚到一个过滤图标，继而进入由一系列相互连接的节点和波形图案表示的中央「Deep reasoning（深度推理）」部分。该过程以一个指向「Output（输出）」的人物图标收尾。底部最后的标签将该过程描述为「Long tail of automated + human verification（自动化 + 人工验证的长尾）」。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/DeepThink-maths-science-discovery__figure-05-Network-layer__light.svg)![题为「Network layer」的流程图，展示了一个深度推理过程。顶部一个标注为「Extensive exploration of solution space（解空间的大规模探索）」的括号汇聚到一个过滤图标，继而进入由一系列相互连接的节点和波形图案表示的中央「Deep reasoning（深度推理）」部分。该过程以一个指向「Output（输出）」的人物图标收尾。底部最后的标签将该过程描述为「Long tail of automated + human verification（自动化 + 人工验证的长尾）」。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/DeepThink-maths-science-discovery__figure-05-Network-layer__dark.svg)

AI 推理流水线示意图：展示了网络层的大规模解空间探索如何汇聚为结构化推理，并通过自动化与人工验证加以确认。

通过与专家合作处理 18 个研究问题，Gemini Deep Think 的一个进阶版本帮助解决了横跨算法、机器学习与组合优化、信息论以及经济学的长期瓶颈。我们的[「Accelerating Research with Gemini」论文](http://arxiv.org/abs/2602.03837)中的亮点包括（括号内为论文对应章节号）：

1. **跨越数学边界求解网络难题**：「最大割（Max-Cut）」（高效切分网络）和「斯坦纳树（Steiner Tree）」（连接高维点）等经典计算机科学问题的进展一度停滞。Gemini 通过跳出思维定式打破了这两处僵局。它从毫不相关的连续数学分支中引入先进工具——如 Kirszbraun 定理、测度论和 Stone-Weierstrass 定理——解开了这些离散算法难题。见[第 4.1 和 4.2 节](https://arxiv.org/pdf/2602.03837)。
2. **解决在线次模优化中一个长达十年的猜想**：一篇 [2015 年的理论论文](https://research.google/pubs/online-submodular-welfare-maximization-greedy-beats-12-in-random-order/)为数据流提出了一条看似显而易见的规则：为到达的物品制作副本的价值总是低于直接移动原物品。专家们花了十年时间试图证明这一点。Gemini 构造了一个高度特化的三物品组合反例，严格证明了这一长期存在的人类直觉是错误的。见[第 3.1 节](https://arxiv.org/pdf/2602.03837)。
3. **机器学习优化：** 训练 AI 过滤噪声通常需要工程师手动调节一个数学「惩罚项」。研究人员创造了一种自动完成此项调节的新技术，但无法从数学上解释其原理。Gemini 分析了方程，证明该方法之所以成功，是因为它在运行过程中暗中生成了自己的「自适应惩罚」。见[第 8.3 节](https://arxiv.org/pdf/2602.03837)。
4. **为 AI 升级经济理论：** 最近一个用于 AI 生成 token 拍卖的「显示原理（Revelation Principle）」，在数学上只在出价被限制为有理数时成立。把定义域扩展到连续实数会使原证明失效。Gemini 运用先进的拓扑学与序理论扩展了该定理，使之适用于现实世界中连续的拍卖动态。见[第 8.4 节](https://arxiv.org/pdf/2602.03837)。
5. **宇宙弦的物理学：** 计算宇宙弦产生的引力辐射需要为包含「奇点」的棘手积分找到解析解。Gemini 使用 Gegenbauer 多项式找到了一种新颖解法。它自然地吸收了奇点，把一个无穷级数收敛为闭式的有限和。见[第 6.1 节](https://arxiv.org/pdf/2602.03837)。

这些成果横跨多个领域——从信息论与复杂度理论到密码学与机制设计——展示了 AI 正如何从根本上改变研究方式。详情请见[我们的论文](https://arxiv.org/pdf/2602.03837)。

鉴于计算机科学以会议为主导、灵活多变的发表渠道，我们按学术发展轨迹而非僵化的分类法来描述这些成果。约有一半成果瞄准了强会议——包括一篇 ICLR ’26 的录用——而其余大部分发现将构成未来的期刊投稿。即便是纠正领域方向的工作——如识别错误（[第 3.2 节](https://arxiv.org/pdf/2602.03837)）或反驳猜想（[第 3.1 节](https://arxiv.org/pdf/2602.03837)）——也彰显了 AI 作为高水平科学协作者的价值。

## 人机协作的未来

在 Google 此前一系列突破（[1](https://deepmind.google/blog/exploring-the-beauty-of-pure-mathematics-in-novel-ways/)、[2](https://deepmind.google/blog/funsearch-making-new-discoveries-in-mathematical-sciences-using-large-language-models/)、[3](https://deepmind.google/blog/ai-solves-imo-problems-at-silver-medal-level/)、[4](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/)、[5](https://research.google/blog/gemini-provides-automated-feedback-for-theoretical-computer-scientists-at-stoc-2026/)）的基础上，这项工作表明：通用基础模型若辅以智能体化推理工作流，可以成为一个强大的科学伙伴。

在数学家、物理学家和计算机科学家的专业指导下，Gemini Deep Think 模式正在证明自己在复杂数学、逻辑与推理为核心任务的各个领域的效用。

我们正在见证科学工作流程的根本性转变。随着 Gemini 的演进，它扮演着人类智力的「力量倍增器」：承担知识检索与严格验证，让科学家得以专注于概念深度与创造性方向。无论是完善证明、寻找反例，还是连接互不相通的领域，AI 都正在成为科学进步新篇章中一位宝贵的协作者。

## 致谢

我们感谢由数学家、物理学家和计算机科学家组成的专业社群在本项目中给予的帮助与建议。

本项目是 Google 内部一次大规模的协作，其成功归功于众多个人与团队的共同努力。Thang Luong 和 Vahab Mirrokni 领导了总体研究方向，Tony Feng 和 David Woodruff 提供了深厚的技术专业支持。

第一篇论文「Towards Autonomous Mathematics Research」的作者包括：Tony Feng、Trieu H. Trinh、Garrett Bingham、Dawsen Hwang、Yuri Chervonyi、Junehyuk Jung、Joonkyung Lee、Carlo Pagano、Sang-hyun Kim、Federico Pasqualotto、Sergei Gukov、Jonathan N. Lee、Junsu Kim、Kaiying Hou、Golnaz Ghiasi、Yi Tay、YaGuang Li、Chenkai Kuang、Yuan Liu、Hanzhao (Maggie) Lin、Evan Zheran Liu、Nigamaa Nayakanti、Xiaomeng Yang、Heng-Tze Cheng、Demis Hassabis、Koray Kavukcuoglu、Quoc V. Le、Thang Luong。我们感谢以下专家对本工作的反馈与讨论：Jarod Alper、Kevin Barreto、Thomas Bloom、Sourav Chatterjee、Otis Chodosh、Michael Hutchings、Seongbin Jeon、Youngbeom Jin、Aiden Yuchan Jung、Jiwon Kang、Jimin Kim、Vjekoslav Kovač、Daniel Litt、Ciprian Manolescu、Mona Merling、Agustin Moreno、Carl Schildkraut、Johannes Schmitt、Insuk Seo、Jaehyeon Seo、Terence Tao、Cheng-Chiang Tsai、Ravi Vakil、Zhiwei Yun、Shengtong Zhang、Wei Zhang、Yufei Zhao。

第二篇论文「Accelerating Scientific Research with Gemini: Case Studies and Common Techniques」的作者包括 David P. Woodruff、Vincent Cohen-Addad、Lalit Jain、Jieming Mao、Song Zuo、MohammadHossein Bateni、Simina Branzei、Michael P. Brenner、Lin Chen、Ying Feng、Lance Fortnow、Gang Fu、Ziyi Guan、Zahra Hadizadeh、Mohammad T. Hajiaghayi、Mahdi JafariRaviz、Adel Javanmard、Karthik C. S.、Ken-ichi Kawarabayashi、Ravi Kumar、Silvio Lattanzi、Euiwoong Lee、Yi Li、Ioannis Panageas、Dimitris Paparas、Benjamin Przybocki、Bernardo Subercaseaux、Ola Svensson、Shayan Taherijam、Xuan Wu、Eylon Yogev、Morteza Zadimoghaddam、Samson Zhou、Yossi Matias、Jeff Dean、James Manyika、Vahab Mirrokni。这份名单既包括在 Gemini 之上构建智能体化推理的 Google 研究人员，也包括与 Gemini 验证、协作的学术专家合作者。我们还要感谢 Corinna Cortes 对论文的细致审阅。

我们感谢 DeepThink 团队的其他成员提供的基础性支持：Anirudh Baddepudi、Michael Brenner、Irene Cai、Kristen Chiafullo、Paul Covington、Rumen Dangovski、Chenjie Gu、Huan Gui、Vihan Jain、Rajesh Jayaram、Melvin Johnson、Rosemary Ke、Maciej Kula、Nate Kushman、Jane Labanowski、Steve Li、Pol Moreno、Sidharth Mudgal、William Nelson、Ada Maksutaj Oflazer、Sahitya Potluri、Navneet Potti、Shubha Raghvendra、James Roggeveen、Siamak Shakeri、Archit Sharma、Xinying Song、Mukund Sundararajan、Qijun Tan、Zak Tsai、Erik Wang、Theophane Weber、Winnie Xu、Zicheng Xu、Junwen Yao、Shunyu Yao、Adams Yu、Lijun Yu 和 Honglei Zhuang。

我们要感谢 Gemini Post-Training 团队为 Deep Think 构建基础模型：Arash Ahmadian、Ankesh Anand、Charles Chen、Yong Cheng、Kedar Dhamdhere、Philipp Fränken、Justin Gilmer、Elena Gribovskaya、Luheng He、Yangsibo Huang、Rishabh Joshi、Ajay Kannan、Arvind Kannan、Guangda Lai、Robert Leland、Hanzhao (Maggie) Lin、Yingjie Miao、Bryce Petrini、Corbin Quick、Vikash Sehwag、Yue Song、Pranav Talluri、Ankur Taly、George Tucker、Michael Voznesensky、Manish Reddy Vuyyuru、Yiming Wang、Jinliang Wei、Qiao Zhang、Yuan Zhang、Zizhao Zhang。

我们感谢 Quoc Le、Koray Kavukcuoglu、Demis Hassabis（德米斯·哈萨比斯）、James Manyika、Yossi Matias 和 Jeff Dean 对本项目的支持。

最后，我们感谢 Divy Thakkar、Adam Brown、Vinay Ramasesh、Alex Davies、Thomas Hubert、Eugénie Rives、Pushmeet Kohli 和 Benoit Schillings 对项目的反馈与支持。
