---
title: "用 AI 在量子尺度上模拟物质"
title_en: "Simulating matter on the quantum scale with AI"
source: https://deepmind.google/blog/simulating-matter-on-the-quantum-scale-with-ai/
site: deepmind
date: 2021-12-09
crawled: 2026-09-13
translated: 2026-09-13
---

# 用 AI 在量子尺度上模拟物质

> 原文：[Simulating matter on the quantum scale with AI](https://deepmind.google/blog/simulating-matter-on-the-quantum-scale-with-ai/) · Google DeepMind

要解决 21 世纪的一些重大挑战，例如生产清洁电力或开发高温超导体，需要我们设计具有特定性质的新材料。要在计算机上做到这一点，就需要对电子进行模拟——电子是亚原子粒子，支配着原子如何键合成分子，也是固体中电流流动的原因。尽管经过数十年的努力并取得了若干重大进展，精确建模电子的量子力学行为仍然是一个悬而未决的挑战。如今，在发表于 Science 的[论文](https://www.science.org/stoken/author-tokens/ST-218/full)（[开放获取 PDF](https://storage.googleapis.com/deepmind-media/papers/Data_Driven_Density_Functional_Design/data_driven_density_functional_design_unformatted.pdf)）中，我们提出了 DM21，一个在化学的众多领域达到最先进精度的神经网络。为了加速科学进步，我们还[开源了代码](https://github.com/deepmind/deepmind-research/tree/master/density_functional_approximation_dm21)，供任何人使用。

大约一个世纪前，Erwin Schrödinger（薛定谔）提出了[他那个著名的方程](https://www.nobelprize.org/prizes/physics/1933/schrodinger/facts/)，用以描述量子力学粒子的行为。将这一方程应用于分子中的电子极具挑战性，因为所有电子都相互排斥。这看似需要追踪每一个电子位置的概率——即便电子数量很少，这也是一项极其复杂的任务。一个重大突破出现在 20 世纪 60 年代，Pierre Hohenberg 和 Walter Kohn（瓦尔特·科恩）意识到，没有必要逐一追踪每个电子。相反，只要知道任意电子处于每个位置的概率（即电子密度），就足以精确计算所有的相互作用。Kohn 在证明这一点后获得了[诺贝尔化学奖](https://www.nobelprize.org/prizes/chemistry/1998/kohn/facts/)，并由此创立了密度泛函理论（DFT）。

尽管 DFT 证明了这种映射的存在，但 50 多年来，电子密度与相互作用能量之间这一映射的确切性质——即所谓的密度泛函——一直不为人知，只能靠近似。尽管 DFT 本质上包含一定程度的近似，它仍是研究物质在微观层面如何以及为何以某种方式表现的唯一实用方法，因而已成为整个科学领域使用最广泛的技术之一。多年来，研究者针对精确泛函提出了许多精度各异的近似。尽管这些近似广受欢迎，但它们都存在系统性误差，因为它们未能捕捉精确泛函的某些关键数学性质。

通过将泛函表示为神经网络，并将这些精确性质纳入训练数据，我们学到了免于重要系统性误差的泛函——从而能更好地描述一大类化学反应。

![一张示意图，展示将分子的三维电子密度通过一个泛函神经网络（图中以中央方框表示）映射为一个标量能量值的过程。](https://lh3.googleusercontent.com/p5U1EZotSmzxsQTeE1_DP7hYDByTCTyYKDFJoavfQsaw36BjqPaXCog7n74YlbQpqTaZHPM3rEwauuoPgA_IJ4XO-3awxrXdReDx8py80lUmTGwbpw=w1440)

我们特别解决了传统泛函的两个长期存在的问题：

- **离域化误差**：在 DFT 计算中，泛函通过寻找使能量最小化的电子构型来确定分子的电荷密度。因此，泛函中的误差会导致计算出的电子密度出现误差。大多数现有的密度泛函近似会倾向于不切实际地将电子密度铺展在多个原子或分子上，而不是正确定域在单个分子或原子周围（见图 2）。
- **自旋对称性破缺**：在描述化学键断裂时，现有泛函往往不切实际地偏好那些破坏了被称为自旋对称性的基本对称性的构型。由于对称性在我们理解物理学和化学中起着至关重要的作用，这种人为的对称性破缺暴露了现有泛函的一个重大缺陷。

原则上，任何涉及电荷移动的化学物理过程都可能受到离域化误差的影响，任何涉及化学键断裂的过程都可能受到自旋对称性破缺的影响。电荷移动和键断裂是许多重要技术应用的核心，但这些问题也可能导致泛函在最简单的分子（如氢）的描述上出现彻底的定性失败。既然 DFT 是如此关键的技术，那么在设计泛函时，先让它们把这个简单的化学算对，再去要求它们解释复杂得多的分子相互作用（例如可能发生在电池或太阳能电池中的那些），是十分重要的。

![一张电子密度模拟对比图：传统 B3LYP 泛函显示电荷云不切实际地铺展（离域化）在两个分子之间，而 DM21 神经网络泛函则正确地建模了定域（未铺展）的电子密度。](https://lh3.googleusercontent.com/EEmwVCY4WA6uUGn9eUuvN4Onk8gChBl3-3Ah1xPZHfNLt8bxV96r3dPJxM8d1fwauuCVdLfeY5cov-9h2mk9sGtjMCivuf-Gvhodn1seFRs8vjL-Bg=w1440)

图 2 | 左：传统泛函（B3LYP）预测电荷被铺展在两个相邻分子上。右：学习得到的泛函（DM21）正确地将电荷定域在一个分子上。

这些长期存在的挑战都与泛函在面对一个表现出「分数电子特征」的系统时的行为有关。通过用神经网络表示泛函，并精心构建训练数据集以捕捉精确泛函所应有的分数电子行为，我们发现可以解决离域化和自旋对称性破缺这两个问题。我们的泛函还在宽泛的大规模基准测试中表现出很高的精度，这表明这种数据驱动的方法能够捕捉到迄今难以捉摸的精确泛函的某些面向。

多年来，计算机模拟一直在现代工程中扮演着核心角色，使得为「这座桥会不会塌？」「这枚火箭能不能进入太空？」之类的问题提供可靠答案成为可能。随着技术日益转向量子尺度去探索关于材料、药物和催化剂的问题——包括那些我们从未见过甚至从未想象过的——深度学习展现出在这一量子力学层面精确模拟物质的前景。

**附注**

请[在此](https://www.science.org/stoken/author-tokens/ST-218/full)阅读 Science 论文。

论文的开放获取 PDF 请见[此处](https://storage.googleapis.com/deepmind-media/papers/Data_Driven_Density_Functional_Design/data_driven_density_functional_design_unformatted.pdf)。
