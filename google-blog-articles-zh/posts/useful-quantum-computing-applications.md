---
title: "通往实用量子计算应用之路"
title_en: "The road to useful quantum computing applications"
source: https://blog.google/innovation-and-ai/technology/research/useful-quantum-computing-applications/
site: google-blog
date: 2025-11-13
crawled: 2026-09-13
translated: 2026-09-13
---

# 通往实用量子计算应用之路

> 原文：[The road to useful quantum computing applications](https://blog.google/innovation-and-ai/technology/research/useful-quantum-computing-applications/) · Google

有时候，历史会在一瞬间集中发生。短短几年，就能带来数十年的进步与创新。我们现在正在量子计算领域见证这样的时刻。[四十年来的研究](https://blog.google/technology/research/quantum-hardware-verifiable-advantage/)、耕耘与投入正在汇聚，建造大规模、高性能量子计算机这一宏大挑战，已进入全人类的可及范围之内。

量子计算社区在硬件方面已取得显著进展，我们的高性能 Willow 芯片正引领这一浪潮。我们如今专注于实现[下一个里程碑](https://quantumai.google/roadmap)——长寿命逻辑量子比特，它将带来更强大、更稳定的量子计算机。尽管挑战犹存，Google 与整个社区的信心正不断增长：前路上并不存在不可逾越的障碍。

然而，一个关键问题仍然悬而未决：*面对一台拥有完整能力的容错量子计算机，我们究竟要用它来做什么？*

为了描绘从想法到实际部署的现实工具之间的旅程，我们的团队开发了一个五阶段框架，并发表在论文《[The Grand Challenge of Quantum Applications](http://arxiv.org/abs/2511.09124)》（量子应用的宏大挑战）中。今天，我们将分享这五个阶段，并评估当前一些最有前景的应用在进程中各自的所处位置。

### 从想法到影响的五个阶段

![量子应用开发的六阶段流程图（0-V），展示了一条绕过第 II–IV 阶段基准的捷径。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/stages_highres_1.width-1200.format-webp.webp)

发掘实用量子计算应用所需的广泛研究，可以划分为五个主要阶段，一个想法在通往现实影响的过程中通常会经历所有阶段。

**第 I 阶段——发现（Discovery）：** 一种新的抽象量子算法——例如用于发现隐藏模式的 [Simon 算法](https://en.wikipedia.org/wiki/Simon%27s_problem)、用于无结构搜索的 [Grover 算法](https://en.wikipedia.org/wiki/Grover%27s_algorithm)，或[量子相位估计算法](https://en.wikipedia.org/wiki/Quantum_phase_estimation_algorithm)——被提出并加以分析。这些算法在理论上可能比经典方法更快地解决某类问题，并在特定领域给出基础性成果，但在这一早期阶段，它们的直接实用价值往往尚不确定或有限。这类工作通常建立在关于量子计算特性与极限的最基础的研究之上（第 0 阶段）。

**第 II 阶段——找到合适的问题实例（Finding the right problem instances）：** 这一阶段的重点是寻找并刻画具体的、可验证的问题实例，使量子算法在其中展现出相对所有已知经典方法的优势。例如，要解决"找到分子的最低能量状态"这样一个抽象的第 I 阶段问题，就需要确定哪些具体分子（即"问题实例"）能体现出量子计算机的优势。这一步可能颇具挑战，因为现实问题的许多实例经典计算机就能解决。量子优势可能只有在最复杂的情形下才有保证，而经典难解的实例又难以识别。要通过这一阶段，量子算法必须在激烈竞争中胜过层出不穷、不断改进的大量经典方法。

**第 III 阶段——确立现实世界优势（Establishing real-world advantage）：** 这是"那又怎样？"的阶段。在刻画出我们能比经典方法更好求解的问题实例之后，这一阶段要追问：这些实例是否连接到*具体的现实*用例？例如，模拟某些我们知道经典方法难以处理的特定分子（即第 II 阶段的"问题实例"），能为药物发现创造什么价值？这一阶段的首要常见问题在于，细节决定成败——找到符合第 II 阶段所确立的量子优势标准的现实用例往往很困难。此外，量子专家与应用领域专家之间还存在知识鸿沟。例如，量子算法专家往往不了解电池化学这类应用领域的精细细节，而电池工程师也不熟悉量子算法的微妙之处。

**第 IV 阶段——面向使用的工程化（Engineering for use）：** 一旦我们得到了具备量子优势的现实问题实例，就需要弄清楚它的实际计算成本。在这一阶段，我们要针对具体用例进行实用化优化、多层编译与资源估算。这里的关键问题包括：需要多少量子比特和量子门？算法需要运行多久？对于容错量子计算用例（即使用量子纠错的情形），第 IV 阶段还涉及规划这种纠错将如何实现。

在过去十年中，第 IV 阶段的研究将对解决整数分解（左）和分子模拟（右）等问题所需资源的估算降低了多个数量级

![双散点图，显示从 2010 年到 2025 年物理量子比特数量从 $10^9$ 降至 $10^6$，FeMoco 的 Toffoli 门数量从 $10^{11}$ 降至 $10^9/10^8$。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/RoadtoQuantum_Graphs.width-1200.format-webp.webp)

**第 V 阶段——应用部署（Application deployment）：** 旅程的最后一程。经过验证的量子解决方案被部署并用于现实的实际工作流，在那里它相对于所有经典替代方案提供优势。这一阶段属于未来。由于硬件开发仍处于早期，目前尚无任何端到端量子应用在硬件上实现，并在具有现实意义的问题上取得确凿优势。

### 当今一些最有前景的应用进展如何？

我们的框架展示了三个潜在应用在各自旅程中所处的位置。

![标题为"量子模拟（第 III 和 IV 阶段）"的幻灯片。文字详述研究进展，包括量子化学和聚变反应堆建模计算资源的降低（第 IV 阶段），以及 Qualtran 等开源工具和 Quantum Echoes 算法的开发。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/QuantumCarousel1_v2.width-100.format-webp.webp)

详情请参阅我们关于[工业量子模拟](https://research.google/blog/developing-industrial-use-cases-for-physical-simulation-on-future-error-corrected-quantum-computers/)和用于[测量分子](https://arxiv.org/abs/2510.19550)的 [Quantum Echoes](https://blog.google/technology/research/quantum-echoes-willow-verifiable-quantum-advantage/) 的第 III 阶段研究；我们关于[量子化学](https://journals.aps.org/prx/abstract/10.1103/pb2g-j9cw)、[聚变反应堆](https://www.pnas.org/doi/10.1073/pnas.2317772121)和[物理模拟](https://journals.aps.org/prx/abstract/10.1103/pb2g-j9cw)的第 IV 阶段论文；以及 [Qualtran 软件库](https://quantumai.google/qualtran)。

![题为"密码分析（第 IV 阶段）"的幻灯片，带有一条蓝色竖条和一个橙色圆形图形。文字讨论了 Shor 量子算法对现行公钥密码体系的破解威胁，以及向后量子密码迁移对第 IV 阶段工作的关注。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/QuantumCarousel2_v2.width-100.format-webp.webp)

详情请参阅我们关于使用量子计算机分解大整数的[安全博客](https://security.googleblog.com/2025/05/tracking-cost-of-quantum-factori.html)及[配套论文](https://arxiv.org/abs/2505.15917)。

![题为"优化与机器学习（第 I 和 II 阶段）"的演示幻灯片。配套文字详述了新量子算法与解码量子干涉测量（DQI）的相关工作，报告了第 II 和第 IV 阶段的结果，并发现量子优势所需物理量子比特少于 100 万个。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/QuantumCarousel3_v2.width-100.format-webp.webp)

详情请参阅我们关于[优化](https://journals.aps.org/prx/abstract/10.1103/PhysRevX.15.021077)和[机器学习](https://arxiv.org/abs/2509.09033)的最新论文，以及我们在 [DQI](https://research.google/blog/a-new-quantum-toolkit-for-optimization/) 上的[第 II 阶段](https://www.nature.com/articles/s41586-025-09527-5)与[第 IV 阶段](https://arxiv.org/abs/2510.10967)工作。

### 下一步与前路的工作

我们的框架让我们看到：尽管社区在新算法与资源估算方面取得了令人瞩目的进展，但在识别合适的问题实例和寻找现实优势方面仍存在真正的瓶颈。我们从论文中摘取两点行动倡议，助力人类充分释放量子计算应用的潜力。

- **采取"算法优先"的路径：** 与其从模糊的业务问题出发（历史上这条路收效有限），我们更应专注于把算法推进到已证明优势的水平（跨过第 II 阶段），*然后*再积极寻找现实应用（第 III 阶段）。此外，一个有用的解决方案应当是可验证的，才能导向实际应用。我们的 Quantum Echoes 实验是首个在量子计算机上以可验证量子优势运行的算法范例。
- **弥合知识鸿沟：** 我们需要培养更多跨学科专家与团队，他们既能讲"量子语言"，也能讲特定领域语言（如化学、金融、材料科学）。我们乐观地认为，AI 可以成为弥合这一第 III 阶段相关鸿沟的有力工具——通过扫描海量科学文献，找到抽象量子问题与实际产业挑战之间的联系。

政府和其他科研资助机构可以发挥关键作用，将项目与资金定向投入第 II 和第 III 阶段的应用开发，从而弥补这些空白。

建造容错量子计算机是硬件层面的宏大挑战；用好它则是应用层面的宏大挑战——我们的五阶段框架为社区提供了一种更清晰的方式，去看清我们脚下的道路与前方的挑战，朝着能够带来现实益处的量子计算迈进。

完整细节请阅读我们的视角论文《[The Grand Challenge of Quantum Applications](http://arxiv.org/abs/2511.09124)》。
