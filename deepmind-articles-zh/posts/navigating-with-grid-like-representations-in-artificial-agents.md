---
title: "人工智能体利用类网格表征进行导航"
title_en: "Navigating with grid-like representations in artificial agents"
source: https://deepmind.google/blog/navigating-with-grid-like-representations-in-artificial-agents/
site: deepmind
date: 2018-05-09
crawled: 2026-09-13
translated: 2026-09-13
---

# 人工智能体利用类网格表征进行导航

> 原文：[Navigating with grid-like representations in artificial agents](https://deepmind.google/blog/navigating-with-grid-like-representations-in-artificial-agents/) · Google DeepMind

大多数动物——包括人类——都能够灵活地在所处的世界中穿行：探索新区域、迅速回到记住的地点、抄近路。这些能力看起来如此轻松自然，以至于人们往往意识不到其背后过程究竟有多复杂。相比之下，空间导航对人工智能体而言仍然是一项重大挑战，其能力远远落后于哺乳动物。

2005年，一项惊人的发现揭示了空间行为背后神经回路中可能至关重要的一部分：当动物探索环境时，有些神经元会以异常规整的六边形模式放电。这一格点阵被认为能够促进空间导航，作用类似于地图上的网格线。这些被称为[**网格细胞（grid cells）**](https://en.wikipedia.org/wiki/Grid_cell)的神经元，不仅为动物配备了内部坐标系，近来还有假说认为它们支持**基于向量的导航（vector-based navigation）**——也就是说，让大脑能够计算出到达目的地的直线距离和方向（「[沿乌鸦飞行般的直线](https://en.wikipedia.org/wiki/Euclidean_distance)」），从而使动物即使从未走过某条确切路线，也能在两个地点之间径直穿行。

最早发现网格细胞的研究团队因阐明空间认知表征可能的工作机制，共同获得了[2014年诺贝尔生理学或医学奖](https://www.nobelprize.org/prizes/medicine/2014/summary/)。然而，自网格细胞被发现以来的十余年理论研究中，其计算功能——以及它们是否支持基于向量的导航——在很大程度上仍是一个谜。

![网格细胞在智能体穿过一组称为「放电野」的小区域时放电。彩色编码地图显示一个生物网格细胞的放电率分布，色标从蓝色（无放电）到橙色（峰值放电率）。生物网格细胞在解剖结构上被分成具有不同尺度的神经元模块（灰色椭圆）。图中显示每个尺度中有一个神经元正在放电（橙色）。通过读出网格细胞群体的活动——即所谓的「网格编码」——动物可以确定自己在环境中的位置。叠加在网格细胞放电野之上的三角形突出了遵循规则六边形结构的网格模式。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6226874bed593bcc260a76e0_Grid20Cells2001.gif)

在发表于《自然》（Nature）的[最新论文](https://www.nature.com/articles/s41586-018-0102-6)（[PDF 在此](https://www.nature.com/articles/s41586-018-0102-6.epdf?author_access_token=BjM-5BdGxd14c17YFA6PsdRgN0jAjWel9jnR3ZoTv0OEfySMT4t78PpPpCS7uExW3njb8Q4UlgcwRM32WwBCKZs73SThwkfI42wHhFEtJM-Y7sQxDsR1cR7_C9Kq1GwuxGJn46kzRnujvrDMGzc4TQ%3D%3D)）中，我们构建了一个人工智能体，用来检验「网格细胞支持基于向量的导航」这一理论，这契合我们的总体理念：用于 AI 的算法能够有意义地近似大脑的某些要素（参见[AI 与神经科学的良性循环](https://deepmind.com/blog/article/ai-and-neuroscience-virtuous-circle)）。

作为第一步，我们训练了一个循环网络，主要利用与运动相关的速度信号，在虚拟环境中执行自我定位任务。哺乳动物在不熟悉的地方穿行、或在不易辨认熟悉地标的情况下（例如在黑暗中导航）时常会使用这种能力。

我们发现，网络内部自发涌现出了类网格表征（grid-like representations，下文称「网格单元（grid units）」）——这与在觅食哺乳动物中观察到的神经活动模式惊人地一致，也印证了网格细胞为空间提供高效编码的观点。

![两行热力图对比放电率模式：上排标注「Artificial (Agent)」（人工智能体），展示来自人工智能体的类网格表征野；下排标注「Biological (Rat)」（生物大鼠），展示生物网格细胞的放电模式。](https://lh3.googleusercontent.com/pdfgh-9Uo9mNAKKKyBNSJZSrS9_lYe_4MZh8Cy0EWKy3qIV9tD31rFPXLnkh5HBKOxkh0GYk_73a7eY1katvine3Bqz5WhFuznWfpGyPCki-HsEWsQ=w1440)

我们在人工智能体上的实验得到了与觅食哺乳动物生物网格细胞惊人相似的类网格表征（「网格单元」）。

接下来，我们构建了一个人工智能体作为「实验豚鼠」，用以检验网格细胞支持基于向量导航的理论。具体做法是将最初的「网格网络」与更大的网络架构相结合，形成一个可以用深度强化学习训练、在富有挑战性的虚拟现实游戏环境中朝目标导航的智能体。

该智能体的表现达到了超越人类的水平，超过了职业游戏玩家的能力，并展现出了通常与动物相关的灵活导航方式：一旦出现新路线或近路，就会加以利用。

![两幅并排的示意图对比智能体到目标的路径：左图显示智能体在关闭的红色障碍物之间绕行的蜿蜒路径，右图显示障碍物打开时智能体沿直接的向量路径前进。](https://lh3.googleusercontent.com/iA0EDJPGVEykPI5o8Xbmmvrqe4vuzEssa342Wz5owHTIC9BfC0tyf_DCKbVXtMyySyy5Z2zmH93kod3I02g1-FU_H5GsOZ_QyE7juattK4Icu8LAyjQ=w1440)

通过一系列实验性操作，我们证明了类网格表征对基于向量的导航至关重要。例如，当网络中的网格细胞被抑制后，智能体的导航能力受损，其对到目标的距离和方向等关键度量的表征也变得不够准确。

![智能体从右下角出发（橙色），目标在左上角（绿色）。智能体探索房间，网格单元随之放电以表征智能体的位置（橙色椭圆）。智能体当前位置激活的网格单元模式即「当前网格编码」。智能体首次经由一条游荡的路径到达目标。激活颜色变为绿色，表明智能体已到达目标。智能体现在知道了目标的位置，并存储「目标网格编码」（目标处的网格单元活动模式）。智能体从起点出发，从记忆中检索目标网格编码，并计算出一个表示从起点到目标最直接路径的向量。随后利用计算出的向量沿最直接的路径走向目标。智能体借助基于向量的导航到达了目标。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622687e38a29ed50d4cb8c35_Grid20Cells2004.gif)

利用网格单元进行基于向量导航的示意图。底部的圆圈代表3个不同尺度的网格单元群；彩色格子表示处于激活状态。随着智能体移动，放电的网格单元——代表「当前网格编码」——随之变化，反映智能体进入了不同的放电野。网格单元被用于计算到目标的最短路径。

我们相信，这项研究是理解大脑中网格细胞基本计算用途的重要一步，同时也凸显了它们能为人工智能体带来的好处。这些证据有力地支持了如下理论：网格细胞提供了一个欧几里得式的空间框架——一种空间概念——使基于向量的导航成为可能。

更广义地说，我们的工作再次印证了这样一种潜力：把被认为由大脑使用的算法作为[机器学习架构的灵感来源](https://www.cell.com/neuron/fulltext/S0896-6273(17)30509-3)。此前对网格细胞的大量神经科学研究，使智能体的可解释性——这本身就是 AI 研究的一个重要课题——变得显著更容易，因为在试图理解其内部表征时，这些研究给了我们该往哪里看的线索。这项工作也展示了另一种潜力：让人工智能体在逼真的虚拟环境中主动从事复杂行为，以此检验关于大脑工作方式的理论。

将这一原则再推进一步，类似的方法也可用于检验与感知声音或控制肢体等重要脑区有关的理论。将来，这类网络很可能为科学家提供一种开展「实验」的新方式：提出新理论，甚至在某些方面补充目前在动物身上开展的研究。

更新（2018年5月14日）

我们建议你阅读 Cueva 和 Wei 的[《通过训练循环神经网络执行空间定位而涌现的类网格表征》](https://openreview.net/forum?id=B17JTOe0-)，该工作同期发表于 ICLR。虽然其范围与结论与我们的研究不同，但展示了有趣的结果。简言之，作者发现的周期性放电模式与环境围合的形状一致，例如方形环境中出现矩形网格，三角形环境中出现三角形网格（见 Cueva 与 Wei 论文图2）。这与我们的研究不同：我们发现的类网格单元，其放电模式与啮齿类网格细胞高度相似，后者通常在不同形状的环境（如方形和圆形场地）中都表现出六边形放电模式。

阅读《自然》论文：[[PDF](https://www.nature.com/articles/s41586-018-0102-6.epdf?author_access_token=BjM-5BdGxd14c17YFA6PsdRgN0jAjWel9jnR3ZoTv0OEfySMT4t78PpPpCS7uExW3njb8Q4UlgcwRM32WwBCKZs73SThwkfI42wHhFEtJM-Y7sQxDsR1cR7_C9Kq1GwuxGJn46kzRnujvrDMGzc4TQ%3D%3D)]

下载原始论文（未排版版本）：[[PDF](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/navigating-with-grid-like-representations-in-artificial-agents/Vector-based%20Navigation%20using%20Grid-like%20Representations%20in%20Artificial%20Agents.pdf)]

阅读诺贝尔奖得主 Edvard Moser 对本文的[评述](https://f1000.com/prime/733198068?key=nvlnlWetE8dlZTy)。

本工作由 Andrea Banino、Caswell Barry、Benigno Uria、Charles Blundell、Timothy Lillicrap、Piotr Mirowski、Alexander Pritzel、Martin Chadwick、Thomas Degris、Joseph Modayil、Greg Wayne、Hubert Soyer、Fabio Viola、Brian Zhang、Ross Goroshin、Neil Rabinowitz、Razvan Pascanu、Charlie Beattie、Stig Petersen、Amir Sadik、Stephen Gaffney、Helen King、Koray Kavukcuoglu、Demis Hassabis、Raia Hadsell 和 Dharshan Kumaran 完成。
