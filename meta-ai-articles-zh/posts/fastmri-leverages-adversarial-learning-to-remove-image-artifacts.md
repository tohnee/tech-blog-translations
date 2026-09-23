---
title: "fastMRI 利用对抗学习消除图像伪影"
title_en: "fastMRI leverages adversarial learning to remove image artifacts"
date: 2019-03-15
source: https://ai.facebook.com/blog/fastmri-leverages-adversarial-learning-to-remove-image-artifacts
crawled: 2026-09-22
translated: 2026-09-22
---

# fastMRI 利用对抗学习消除图像伪影

> 原文：[fastMRI leverages adversarial learning to remove image artifacts](https://ai.facebook.com/blog/fastmri-leverages-adversarial-learning-to-remove-image-artifacts) · Meta AI（Wayback 存档）

**这是什么：**作为把 MRI 扫描速度最高提升 10 倍的 fastMRI 项目的一部分，Facebook AI 与 NYU Langone Health 的研究者开发了一种用深度学习解决 AI 加速 MRI 图像伪影问题的新方法。这一被称为「方向对抗者」（orientation adversary）的技术还显著提升了整体图像质量。fastMRI 团队通过一项与 NYU Langone Health 六位委员会认证放射科医生的盲测研究评估了该方法。结果压倒性地表明，经方向对抗训练的模型产生的图像伪影更少，且细节毫无损失。「图像的质量至关重要，以确保构成我们诊断基础的信号异常的保真度，」参与研究的放射科医生之一 Mitch Kline 说，「方向对抗者减少了条带伪影，同时保持了最佳的信噪比与图像分辨率。」我们在此分享大规模 MRI 测量与临床图像数据集。左侧是一张真值 MRI 图像；中间是同一扫描的 AI 加速版本，右上角尤其可见水平条带伪影；右侧是用方向对抗者生成的加速扫描，条带伪影几乎完全消除。

**工作原理：**用深度学习从较少原始数据生成高精度 MRI 扫描的一个挑战是，这些重建常受条带与条纹伪影困扰，分散注意力或遮挡图像细节。这些伪影对非专家而言可能不易察觉，但对受过识别图像中最细微变化训练的放射科医生来说显而易见。「在审阅加速图像时，我们注意到明显的水平条带伪影，它显著降低了图像质量，并有可能遮蔽病变，」NYU Langone Health 放射学系主任兼 Louis Marx 放射学教授 Michael P. Recht 医学博士说。

为解决这些问题，fastMRI 团队利用对抗训练技术，产出一个以加速 MRI 扫描原始数据为输入、产生无这些伪影的准确 MRI 图像的深度学习模型。在对抗学习中，训练目标增加了一个额外的损失项，鼓励模型以某种方式「欺骗」对抗者。在本例中，fastMRI 团队使用的对抗者的目标是预测条带图案的方向。训练期间，通过在重建前后随机转置输入数据，产生水平与垂直两种条带图案。对抗者与重建模型同时训练，使对抗者随着重建改进不断适应，直到不再有条带。此图展示了带方向对抗者的训练流水线。

**为什么重要：**fastMRI 是一个开源协作项目，力求用 AI 把扫描加速 10 倍，让更多人用上 MRI、缩短等待时间，并减轻难以或无法长时间待在扫描仪内的患者的痛苦。为帮助更广泛的研究社区为 fastMRI 做贡献并探索不同途径，我们最近发布了神经 MRI 数据集并组织了首届 fastMRI 挑战赛。由于图像伪影一直是 AI 加速 MRI 的主要挑战，这一新技术有可能让项目更接近临床环境中的落地。我们的技术适用面广，可用于任何能获得全采样真值数据的重建模型与数据集。此外，虽然当今最先进的设施使用 3 特斯拉 MRI 机器，磁体强度较低的扫描仪（如 1.5 特斯拉）在世界各地仍很常用。这些扫描仪往往产生带更多条带伪影的图像。我们的方向对抗者技术可以帮助这些设备产生更好的重建并加速扫描，从而把加速 MRI 的益处带给更多人。

**阅读论文：**https://arxiv.org/abs/2001.08699

**作者：**

- Aaron Defazio，研究科学家
- Nafissa Yakubova，访问研究员
- Tullie Murrell，应用研究科学家
