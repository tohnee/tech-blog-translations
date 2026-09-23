---
title: "面向高效神经架构搜索的改进超网训练"
title_en: "Improved supernet training for efficient neural architecture search"
date: 2021-07-14
source: http://ai.facebook.com/blog/improved-supernet-training-for-efficient-neural-architecture-search
crawled: 2026-09-22
translated: 2026-09-22
---

# 面向高效神经架构搜索的改进超网训练

> 原文：[Improved supernet training for efficient neural architecture search](http://ai.facebook.com/blog/improved-supernet-training-for-efficient-neural-architecture-search) · Meta AI（Wayback 存档）

2021 年 7 月 14 日

设计精确且计算高效的神经网络架构，是构建任何高性能机器学习系统的重要而困难的一环。神经架构搜索（NAS）可以通过探索庞大的架构空间来自动化神经网络设计，但传统 NAS 方法本身通常计算开销巨大：需要从零开始训练并评估数百个候选架构，在单块 GPU 上要花数年，即便用数千块 GPU 也需要近一个月。我们开发了两种新方法——AttentiveNAS 和 AlphaNet——显著提升了所谓「超网」（supernet）的精度。超网已成为让 NAS 更高效的有力手段。这些方法优于既有的超网训练方法，在 ImageNet 数据集上取得最先进结果，并仅用 444 MFLOPS 就达到超过 80% 的精度。

超网把各种候选架构组装成一个单一的、过参数化的权重共享网络，然后尝试同时优化它。每个候选架构对应一个子网络，通过子网络与超网的同时训练，不同架构可以直接从超网继承权重用于评估和部署。这消除了逐个训练或微调每个架构的巨大计算成本。尽管前景可期，同时优化超网的所有子网络（在权重共享下）非常困难。为稳定训练，研究者常使用「三明治」采样策略：采样多个子网络（最大、最小和两个随机选择），并为每个小批次聚合梯度。

为改进超网训练，自然产生两个问题：训练期间如何采样子网络？以及鉴于子网络通常更难训练，如何监督它们？我们的 AttentiveNAS 方法提出聚焦注意力采样策略，引导网络训练以实现帕累托最优。而 AlphaNet 用 alpha 散度监督子网络，从而同时防止对教师模型不确定性的高估或低估。这两种方法解决超网训练中相互正交的问题，可以组合使用，带来最稳定、性能最佳的超网训练。

如下面的图表所示，在广泛的算力约束下，AttentiveNAS 和 AlphaNet 帮助网络精度显著提升，优于所有先前最先进的 NAS 方法，包括 BigNAS、OFA 和 EfficientNet。（图表：AttentiveNAS、AlphaNet 与既有方法（包括 BigNAS、Once-for-all Network（OFA）和 EfficientNet）的比较。）

## 工作原理

AttentiveNAS 和 AlphaNet 从两个不同角度提升超网性能。传统超网训练方法（如 BigNAS）均匀采样搜索空间，因而对模型性能的帕累托前沿不敏感。改进超网训练的一个自然思路，是更多地关注构成精度与计算需求最佳折中的帕累托最优子网络。与此同时，改进表现最差的模型也可能有价值，因为推高最差帕累托集合的性能极限，可能带来更优化的权重共享图。当最佳与最差帕累托架构之间的范围更紧凑时，所有可训练组件（如通道）都将对网络架构的最终性能做出最大贡献。如下面的图表所示，在 AttentiveNAS 中，我们研究了不同的帕累托感知采样策略，把子网络采样聚焦于最佳和最差帕累托架构集合。（图：最佳与最差帕累托架构集合。）

为了在超网训练中聚焦帕累托架构，AttentiveNAS 把子网络采样分解为两步：第一，按先验分布采样一个算力目标；第二，采样满足该算力目标的精度最佳和最差的子网络。第一步采样较为容易，而选择最佳或最差子网络并非易事，因为在验证集上做精确精度评估的计算成本可能很高。为高效估计子网络的性能，我们提出了两种基于小批次损失或精度预测器的算法。我们还将 AttentiveNAS 与既有 NAS 方法（如 BigNAS、OFA 和 EfficientNet）进行了比较：在 ImageNet 数据集上评估时，AttentiveNAS 实现了精度与 FLOPS 的 SOTA 折中。

### AlphaNet：用 alpha 散度改进超网训练

在子网络的监督上，原地知识蒸馏（KD）被广泛用于利用超网最大子网络预测的软标签。标准 KD 使用 KL 散度（一种相对熵的统计度量）来衡量教师网络与学生网络之间的差异。然而使用 KL 散度时，学生模型往往高估教师模型的不确定性，并因对最重要的模式——即教师模型的正确预测——近似不准而受损。在下面的例子中，左侧的学生网络预测正确，但低估了教师模型的不确定性；中间的学生网络则高估了教师模型的不确定性并把输入分错。虽然第二种情况更不可取，但如右图所示，使用 KL 散度（alpha = 1）时，第一个学生受到的惩罚反而大得多。（左图展示不确定性低估，中图展示不确定性高估；右图绘制了这两个示例中学生模型与教师模型之间相应的 α 散度。注意 KL 散度是 α 散度在 α = 1 时的特例。我们把不确定性定义为网络 Softmax 层之后预测的熵。）

为缓解 KL 散度的问题，我们的 AlphaNet 方法使用更泛化的 alpha 散度。如上面右图所示，通过控制 alpha，我们可以显式控制如何惩罚对教师模型不确定性的高估和低估。更具体地说，在训练期间，我们评估不同 alpha 下的 alpha 散度损失，并显式选择最大的损失用于梯度计算。为展示 alpha 散度的收益，我们在下面的图表中比较了性能帕累托前沿与最小网络的精度（与基线 KL 散度对比）。由 alpha 散度得到的网络家族 AlphaNet 显著超越所有既有方法。此外，在与既有 EfficientNet 比较迁移学习精度时，AlphaNet 在所有下游任务上都优于其他方法，同时计算效率更高。（图表：与 EfficientNet 的迁移学习精度比较。注意 EfficientNet-B0 和 B1 分别为 390 MFLOPS 和 700 MFLOPS，而 AlphaNet-A0 和 A6 分别为 203 MFLOPS 和 709 MFLOPS。）

**为什么重要：**智能手机、平板和 VR 头显等边缘设备，在世界各地人们的日常生活中扮演着日益重要的角色。要把先进的计算机视觉和其他 AI 系统带到这些设备上，研究社区需要设计既精确又高度高效的神经网络。随着 AR 眼镜等新设备日益普及、IoT 芯片组被用于新产品，这一需求可能还会增长。NAS 为自动化高效网络设计提供了强大工具，但它一直未能惠及许多研究者。传统 NAS 算法计算昂贵，需要数十万 GPU 小时，进而依赖大规模计算资源的获取。基于超网的 NAS 把网络训练与搜索过程解耦，可以比传统 NAS 技术高效若干个数量级，同时通过权重共享达到卓越且最先进的网络性能。所提出的 AttentiveNAS 和 AlphaNet 方法从两个根本层面改进了基于超网的 NAS，二者可以协同工作，进一步把 NAS 技术普及给 AI 社区的所有研究者，并为边缘端交付性能更强的网络。

阅读论文并获取代码：

- AttentiveNAS 论文（CVPR 2021）：https://arxiv.org/pdf/2011.09011.pdf
- AttentiveNAS GitHub：https://github.com/facebookresearch/AttentiveNAS
- AlphaNet 论文（ICML 2021 长报告）：https://arxiv.org/pdf/2102.07954.pdf
- AlphaNet GitHub：https://github.com/facebookresearch/AlphaNet

作者：Meng Li，研究科学家
