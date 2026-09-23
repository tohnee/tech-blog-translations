---
title: "BrightHeart 如何使用 Meta 的 DINOv2 变革胎儿心脏筛查"
title_en: "How BrightHeart uses Meta's DINOv2 to transform fetal heart screenings"
date: 2025-01-23
source: https://ai.meta.com/blog/brightheart-transforms-fetal-heart-screenings-dinov2
crawled: 2026-09-22
translated: 2026-09-22
---

# BrightHeart 如何使用 Meta 的 DINOv2 变革胎儿心脏筛查

> 原文：[How BrightHeart uses Meta's DINOv2 to transform fetal heart screenings](https://ai.meta.com/blog/brightheart-transforms-fetal-heart-screenings-dinov2) · Meta AI（Wayback 存档）

对于出生时患有先天性心脏病（CHD）的儿童来说，出生前的早期诊断至关重要，这样才能确保婴儿在分娩后获得优化的照护，争取最好的结果。然而，目前只有 34% 的先天性心脏病能在产前被发现。总部位于巴黎的医疗技术公司 BrightHeart 把改进胎儿心脏筛查作为自己的使命。该公司在 Meta DINOv2 模型的支持下打造了 AI 驱动的医疗软件，帮助临床医生更快、更准确地识别或排除提示先天性心脏病的迹象，目标是改善患儿的预后。

BrightHeart 最近以前所未有的速度为其首款人工智能软件取得了 FDA 510(k) 许可——距公司成立仅两年——这在一定程度上要归功于高效部署 Meta 开源 DINOv2 模型等先进工具来加速研发。

DINOv2 在 2021 年 DINO 模型的基础上构建，利用自监督学习获得对图像和视频更深入的理解。这带来了极其精确的视频分类性能，可以辅助先天性心脏病的早期检测。通过借助 AI 与机器学习的力量，BrightHeart 希望彻底变革胎儿心脏筛查，让先天性心脏病患儿拥有健康快乐人生的最大机会。

BrightHeart 由两位儿科心脏病学家创立，他们发现了 CHD 检测中的一个显著缺口：超声检查复杂、正确检测所需的专业知识与经验水平高，加上 CHD 在通常不到 1 厘米的胎儿心脏中形态表现多样，这类缺陷常被忽视。这种疏忽可能造成严重后果，显著影响发病率与死亡率。

BrightHeart 设备分析的示意图：通过分析胎儿心脏的八项形态特征来识别可疑发现（左）。结果逐帧展示给用户（右上），不显示任何分割或测量数据。

鉴于 CHD 未被检出所伴随的严重负面后果，BrightHeart 团队正争分夺秒地尽快把他们的创新软件推向市场。有鉴于此，在研发阶段选择既满足其严格的隐私与安全标准、又能以创纪录速度交付无与伦比效果的工具就显得尤为重要。从一开始，DINOv2 就脱颖而出——不仅因为其质量与创新，还因为它的开源特性允许模型被下载并在私有环境中使用，所有数据都严格留在 BrightHeart 生态系统之内。

「我们选择神经网络工具时的主要目标是，拥有一个高质量、创新且高效的神经网络，而且能在几分钟内运行起来。」BrightHeart 的首席数据科学家 Eric Askinazi 说，「我们的评估过程从近十几个候选分类模型开始，DINOv2 是毫无悬念的选择。」

团队利用 DINOv2 的开源特性加速了产品开发过程。由于时间是他们的最大约束，他们发现预训练模型极其便利，可以专注于把技术集成到自己的解决方案中，而不必从零构建。

BrightHeart 以 DINOv2 为基础训练他们的模型，用于分析超声检查的视频片段，判断检查是否正常，或在视频中出现可能提示 CHD 存在的迹象时加以标记。「它让我们真正快速上手，更快地取得更好的结果。」Askinazi 指出。

原始结果发表：Lam-Rachlin, J., et al. (2024), OP02.05: AI-enhanced detection of congenital heart disease suspicion in second trimester ultrasounds by OBGYN and MFM. Ultrasound Obstet Gynecol, 64: 63-63. https://doi.org/10.1002/uog.27887

一旦准备进入生产阶段，团队希望 CHD 的产前诊断率能显著提升，从而帮助避免出生后可能出现的并发症。Askinazi 表示，如果没有 DINOv2，如此迅速地取得近期的 FDA 许可是不可能的。他确信 BrightHeart 能为新生儿诊断和护理标准的未来带来重大影响。

「在性能与推理速度之比方面，我们还没有见过任何能与之接近的东西，所以 DINOv2 对我们来说是一个出色的工具。」Askinazi 说，「我们对迄今为止快速的产品开发进展感到满意，现在的目标是把它交到临床医生手中，加速改善患者照护。」
