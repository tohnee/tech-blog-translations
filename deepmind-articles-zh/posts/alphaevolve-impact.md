---
title: "AlphaEvolve：我们的 Gemini 驱动编码智能体如何在各领域扩大影响"
title_en: "AlphaEvolve: How our Gemini-powered coding agent is scaling impact across fields"
source: https://deepmind.google/blog/alphaevolve-impact/
site: deepmind
date: 2026-05-07
crawled: 2026-09-13
translated: 2026-09-13
---

# AlphaEvolve：我们的 Gemini 驱动编码智能体如何在各领域扩大影响

> 原文：[AlphaEvolve: How our Gemini-powered coding agent is scaling impact across fields](https://deepmind.google/blog/alphaevolve-impact/) · Google DeepMind

一年前，我们推出了 [AlphaEvolve](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/)，一个由 Gemini 驱动、用于设计先进算法的编码智能体。我们展示了 AlphaEvolve 能够帮助在数学与计算机科学的开放问题上做出新发现，并优化此后被部署到 Google 基础设施关键环节的算法。

今天，由于算法已经渗透到生活的几乎每一个方面，AlphaEvolve 所能企及的疆域也更加广阔。从帮助解释自然世界的物理学，到为电网和计算基础设施提供动力，AlphaEvolve 可以通过无数种方式帮助各个领域的科学家和企业加速前进。

我们很高兴分享迄今 AlphaEvolve 最具影响力的一组成果。

## 推动社会影响与可持续发展

AlphaEvolve 已经帮助揭示了健康与可持续性研究中的关键关联。

![由白色和蓝色小球构成的多个 DNA 双螺旋结构的 3D 渲染图，悬浮于深色纹理背景之上，景深较浅。](https://lh3.googleusercontent.com/AQO4-KC1y4l_eOV0jS66QbkoodWyfeeje-4HnoAnFFRgAuBz40WpwS2fbv6cPSnHrudBVPLHVboq4f6u_ZPejTGWJ_9vW1tmrpCSYHyjgLFiryaZtg=w1440-h810-n-nu)

在基因组学领域，AlphaEvolve 被用于改进 [DeepConsensus](https://www.nature.com/articles/s41587-022-01435-7)——一个由 Google Research 开发、用于纠正 DNA 测序错误的模型——使变异检测错误减少了 30%。这些改进正在帮助 [PacBio](https://www.pacb.com/blog/improving-hifi-sequencing-accuracy-with-google-deepconsensus-and-alphaevolve/) 的科学家以更低成本、更高精度分析基因数据。

*「Google 团队使用 AlphaEvolve 找到的解决方案，为我们的测序仪器解锁了显著更高的准确率。对研究人员而言，这种更高质量的数据或许能让此前隐藏的致病突变被发现。」* —— PacBio 高级总监 Aaron Wenger

![晴朗蓝天下，高压电线与输电塔横跨一片翠绿田野的广角风景照。](https://lh3.googleusercontent.com/xT26k7Gu_Lt0iDD2j_ZOQx2VmaZGH2U4j9vGCzo7cmla2UBefMcw-sQ6-12Dvb1SxDUG1Az4epE1bJg71z5KiYMxkMWdCL5eH9Rg6JiFIloZeWRBev8=w1440-h810-n-nu)

在电网优化领域，AlphaEvolve 被应用于[交流最优潮流问题（AC Optimal Power Flow）](https://arxiv.org/abs/2403.17660)。它帮助把我们训练的图神经网络（GNN）模型为该问题找到可行解的能力从 14% 提升到 88% 以上，显著减少了电网所需的其他高成本后处理步骤。

在地球科学领域，AlphaEvolve 把复杂的地理空间数据转化为更可靠、可操作的洞察。通过帮助自动化 [Earth AI](https://ai.google/earth-ai/) 模型的优化流程，[自然灾害风险预测的总体准确率](https://arxiv.org/abs/2510.18318)——覆盖野火、洪水、龙卷风等 20 个类别的汇总结果——提升了 5%。

## 推进研究前沿

AlphaEvolve 正在作为一个强大的研究伙伴，加速各学科的发现进程。

![在洁净室环境中，一只戴着手套的手托着一块表面反光的方形微芯片处理器。](https://lh3.googleusercontent.com/bhd0zRY8D-OCMR2gmX8bWQWa2auM6YuqTs1uj_UQKGFBwnqm8V6kkRj99dLZ8iVZjusyM8SS-FnlLRBP_W24nqvOM8aIeEabb6Y-St4I_DeQMtm9eQ=w1440-h810-n-nu)

在量子物理领域，AlphaEvolve 的优化通过[提出错误率比以往传统优化基线低 10 倍的量子线路](https://arxiv.org/abs/2510.19550)，使得在 [Google 的 Willow 量子处理器](https://blog.google/innovation-and-ai/technology/research/google-willow-quantum-chip/)上运行复杂的分子模拟成为可能。这让首次此类实验性的量子计算演示得以立即产生有影响力的成果——也指向了这样一个未来：AlphaEvolve 帮助找到超越经典计算机能力的算法。

![一个软件界面，展示性能得分随时间变化的折线图，其上叠加着一个「Selected Program」窗口，内含若干柱状图和一段用于优化实验的 Python 代码。](https://lh3.googleusercontent.com/0PyMvA2pLEg69CeZUEWPy4U9D_VU9urOibCixZhsim2RoeC0cbmOMjEjCat0zRj0iN4eS0RSTWJRMjJi70qIxidYDeqjtiKpNWIW2ZWPke3Tr-5i1FM=w1440-h810-n-nu)

通过与 Terence Tao 等世界知名数学家合作，该系统已经帮助解决了[埃尔德什问题（Erdős problems）](https://terrytao.wordpress.com/2025/12/08/the-story-of-erdos-problem-126/)。

*「像 AlphaEvolve 这样的工具正在赋予数学家非常有用的新能力。尤其是对优化问题，我们现在可以快速检验候选不等式是否存在反例，或确认我们对极值点的判断，这极大地改善了我们对这些问题的直觉，让我们更容易找到严格的证明。」* —— 加州大学洛杉矶分校（UCLA）数学教授 Terence Tao

AlphaEvolve 还刷新了多个经典数学难题的纪录，包括改进了[旅行商问题](https://arxiv.org/abs/2509.18057)和[拉姆齐数（Ramsey Numbers）](https://arxiv.org/abs/2603.09172)的下界。

此外，这种自主发现能力正在其他多样领域催生平行创新——从[发现可解释的神经科学模型](https://www.biorxiv.org/content/10.64898/2026.05.18.725921)和[证明微观经济学中的新市场极限](https://arxiv.org/abs/2603.08679)，到快速推进[神经网络基础组件](https://arxiv.org/abs/2602.05688)、[面向用户隐私的密码学](https://arxiv.org/abs/2605.14718)、[合成数据生成](https://arxiv.org/abs/2602.03545)，以及前沿 AI 模型的[关键安全缓解措施](https://arxiv.org/abs/2601.11516)。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![你的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

AlphaEvolve [优化](https://alphaevolve-examples.web.app/ae/experiment/f5ff0dbd_0bb3_4c6b_9bf7_6a98363b935e)「[塔姆斯问题（Tammes problem）](https://en.wikipedia.org/wiki/Tammes_problem)」的一个实例。你可以在公开的[图库（Gallery）](https://alphaevolve-examples.web.app/ae/gallery)中探索 AlphaEvolve 为其生成潜在解的其他问题精选。

## 改进 AI 基础设施

AlphaEvolve 已经从试点测试毕业，成为我们基础设施的核心组件。AlphaEvolve 已被用作常规工具，优化下一代 [TPU](https://cloud.google.com/tpu?e=48754805) 的设计。它还帮助发现了更高效的[缓存替换策略](https://arxiv.org/abs/2602.22425)，用两天时间完成了此前需要数月、密集人力协同才能完成的工作。

「*AlphaEvolve 从为我们的 AI 技术栈提供动力的最底层硬件开始优化。它提出了一种反直觉却高效的电路设计，并被直接集成进我们下一代 TPU 的硅片之中。这是 TPU 之『脑』帮助设计下一代 TPU 之『躯』的最新例证。*」—— Google DeepMind 与 Google Research 首席科学家 Jeff Dean（杰夫·迪恩）

AlphaEvolve 通过改进 [Google Spanner](https://cloud.google.com/spanner) 的[日志结构合并树（Log-Structured Merge-tree）](https://en.wikipedia.org/wiki/Log-structured_merge-tree)压缩启发式规则，提升了其运行效率。这一优化将「写放大」——写入存储的数据量与原始请求之比——降低了 20%。它还为[新的编译器优化策略](https://arxiv.org/abs/2601.21096)提供了洞见，使软件的存储占用减少了近 9%。

## 扩大商业应用

[与 Google Cloud 携手](https://cloud.google.com/blog/products/ai-machine-learning/alphaevolve-on-google-cloud?e=48754805)，我们正把 AlphaEvolve 的力量带给各行业的各类商业企业。

- 在金融服务领域，[Klarna](https://engineering.klarna.com/beyond-prompting-how-algorithmic-evolution-doubled-our-training-speed-8f874af3080d) 使用该系统优化了其最大的 transformer 模型之一——在提升模型质量的同时将训练速度翻倍。
- 在半导体制造领域，[Substrate](https://substrate.com/information-to-atoms) 将 AlphaEvolve 应用于其计算光刻框架，运行时速度提升数倍，使他们能够运行规模显著更大的先进半导体模拟。
- 在物流领域，[FM Logistic](https://cloud.google.com/blog/products/ai-machine-learning/how-fm-logistic-tackled-the-traveling-salesman-problem-at-warehouse-scale-with-alphaevolve?e=48754805) 使用这项技术优化了旅行商问题等复杂路径规划难题，在此前已高度优化的解决方案基础上将路径效率再提升 10.4%——每年节省超过 15,000 公里的行驶距离。
- 在广告与营销领域，[WPP](https://research.wpp.com/blog/cracking-the-code-of-campaign-success-with-googles-alphaevolve-agent/) 使用 AlphaEvolve 改进 AI 模型组件，驾驭复杂的高维投放数据，在与其人工模型优化方案的竞争中取得了 10% 的准确率提升。
- 在计算材料与生命科学领域，[Schrödinger](https://cloud.google.com/blog/products/ai-machine-learning/schrodinger-alphaevolve-molecular-discovery-accelerates-4x) 应用 AlphaEvolve，在机器学习力场（MLFF）训练与推理两个环节都实现了约 4 倍的加速。

*「AlphaEvolve 让我们能够比以往任何时候都更快、更高效地探索更大的化学空间。更快的 MLFF 推理带来实实在在的商业影响：它缩短了药物发现、催化剂设计和材料开发的研发周期，使企业能够以天为单位而不是数月来筛选分子候选物。」* —— Schrödinger 机器学习技术负责人 Gabriel Marques

## AlphaEvolve 的未来

过去一年表明，AlphaEvolve 正在迅速成长为一个多用途的通用系统。它证明了一个道理：下一批突破将由能够自我学习、自我演化、自我优化的算法驱动。展望未来，我们很高兴能够扩展这些能力，把这项技术的力量带给更广泛的外部挑战。

## 致谢

AlphaEvolve 由 Matej Balog、Alexander Novikov、Ngân Vũ、Marvin Eisenberger、Emilien Dupont、Po-Sen Huang、Adam Zsolt Wagner、Sergey Shirobokov、Borislav Kozlovskii、Francisco J. R. Ruiz、Abbas Mehrabian、M. Pawan Kumar、Abigail See、Swarat Chaudhuri、George Holland、Alex Davies、Sebastian Nowozin 和 Pushmeet Kohli 开发。这项研究是「用 AI 进行算法发现」这一更宏大计划的一部分。在初始开发之后，Aja Huang、Anton Kovsharov、Alexey Cherepanov、Anindya Basu、Becky Evangelakos、Jamie Smith 和 Mario Pinto 加入团队，为扩大 AlphaEvolve 的影响做出了贡献。

Adam Connors、Alex Bäuerle、Anna Trostanetski、Fernanda Viegas、Gabi Cardoso、Jonathan Caton、Lucas Dixon、Mariana Felix、Martin Wattenberg、Matin Akhlaghinia、Richard Green、Yosuke Ushigome 和 Yunhan Xu 与我们的团队合作开发了 AlphaEvolve 的用户界面，并得到了许多其他同事的支持。

Anant Nawalgaria、Diego Ballesteros、Gemma Jennings、Jakob Oesinghaus、Kartik Sanu、Laurynas Tamulevičius、Nicolas Stroppa、Nishta Dhawan、Oliver Hilsenbeck、Puneet Jagralapudi、Reah Miyara、Skander Hannachi、Tom Beyer 和 Vishal Agarwal 与我们的团队合作开发了 AlphaEvolve API，并与 Google Cloud 客户对接，同样得到了许多其他同事的支持。

我们诚挚感谢以下合作者，他们主导了 AlphaEvolve 在关键问题上的应用并为本报告做出贡献：Aaron Wenger、Abhradeep Guha Thakurta、Akanksha Jain、Alex Vitvitskyi、Amir Yazdan Bakhsh、Andrew Carroll、Aranyak Mehta、Arthur Conmy、Ansh Nagda、Davide Paglieri、Eric Perim Martins、Gabriella Marfani、Hassler Thurston、Hongzheng Chen、Jack Mason、János Kramár、Jasper Xian、Jeremy Ratcliff、Jessica Sapick、Johannes Bausch、Jonathan Katz、Kevin Miller、Kim Stachenfeld、Mark Kurzeja、Mircea Trofin、Myriam Khan、Nero Geng、Pablo Samuel Castro、Petar Veličković、Pi-Chuan Chang、Prabhakar Raghavan、Raghav Gupta、Rohin Shah、Sasha Vezhnevets、Sébastien Lahaie、Sergio Guadarrama、Shravya Shetty、Shruthi Gorantala、Terence Tao、Todd Lipcon、Tom O'Brien、Vinod Nair、Ziyue Wang、Zun Li，以及 AlphaEvolve 的众多其他用户。

最后，我们感谢领导层给予的指导与支持：Amin Vahdat、Ankur Jain、Demis Hassabis（德米斯·哈萨比斯）、Jeff Dean、Parthasarathy Ranganathan、Pushmeet Kohli、Saurabh Tiwary 和 Sundar Pichai。我们也向 Google DeepMind、Google Cloud、Google Labs、Google Research 及其他产品部门的合作团队致谢，感谢他们让由 AlphaEvolve 驱动的应用与产品得以落地。
