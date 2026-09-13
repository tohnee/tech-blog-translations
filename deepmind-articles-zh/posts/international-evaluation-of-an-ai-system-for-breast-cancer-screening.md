---
title: "乳腺癌筛查 AI 系统的国际评估"
title_en: "International evaluation of an AI system for breast cancer screening"
source: https://deepmind.google/blog/international-evaluation-of-an-ai-system-for-breast-cancer-screening/
site: deepmind
date: 2020-01-01
crawled: 2026-09-13
translated: 2026-09-13
---

# 乳腺癌筛查 AI 系统的国际评估

> 原文：[International evaluation of an AI system for breast cancer screening](https://deepmind.google/blog/international-evaluation-of-an-ai-system-for-breast-cancer-screening/) · Google DeepMind

乳腺癌是女性因癌症死亡的第二大原因，但研究已证明，如果能够早期发现并治疗，预后会得到改善。正因如此，世界上许多国家都建立了乳腺癌筛查项目，目标是在疾病的较早阶段识别乳腺癌，因为此时治疗更有可能成功。

然而，解读乳腺 X 光片（钼靶摄影）仍然充满挑战，专家在检测癌症时表现的巨大差异性就是明证。在与 [Google Health](https://health.google/)、[Cancer Research UK Imperial Centre（英国癌症研究院帝国中心）](https://www.cancerresearchuk.org/)、[西北大学（Northwestern University）](https://www.northwestern.edu/)以及[皇家萨里郡立医院（Royal Surrey County Hospital）](https://www.royalsurrey.nhs.uk/)合作完成的这项研究（[现已发表于 Nature](https://www.nature.com/articles/s41586-019-1799-6.epdf?author_access_token=V_LKV2xpSv9G1dhANYeWM9RgN0jAjWel9jnR3ZoTv0M5zwPVx5jT4z_z-YkUZTBT6_1AtRXi8QouJM7xB-oSN-cVBoH7f_QTgx-yQN3UBEVfkvO1_5urNT-CZHGCEQNGlCuO69tMQYak4SmdoDqyzg%3D%3D)）中，我们开发了一套 AI 系统，经活检证实，它在根据乳腺 X 光片预测乳腺癌方面能够超越英国和美国的临床专家。

## 乳腺癌筛查数据集

各国的乳腺癌筛查项目不尽相同。在美国，女性通常每一到两年接受一次筛查，其乳腺 X 光片由一名放射科医生解读。在英国，女性每三年筛查一次，但每张乳腺 X 光片由两名放射科医生解读，如有分歧则进入仲裁流程。我们利用在这两个国家收集的大型数据集来开发和评估这套 AI 系统。

英国评估数据集由 2012 年至 2015 年间在伦敦两个筛查点接受筛查性乳腺 X 光检查的所有女性中随机抽取 10% 组成，包含 25,856 名女性，其中 785 人接受了活检，414 人在影像检查后三年内确诊癌症。这些去标识化数据由 Cancer Research UK 作为 [OPTIMAM](http://commercial.cancerresearchuk.org/optimam-mammography-image-database-and-viewing-software) 数据库项目的一部分收集，并受到严格的隐私约束。

美国评估数据集由 2001 年至 2018 年间从一家学术医疗中心收集的 3,097 名女性的去标识化筛查性乳腺 X 光片组成。我们纳入了该时间段内接受活检的全部 1,511 名女性的影像，以及从未接受活检的女性的随机子集。在接受活检的女性中，有 686 人在影像检查后两年内确诊癌症。

![一张乳腺 X 光片，包含四张图像——每侧乳房两个不同角度的视图。](https://lh3.googleusercontent.com/fGcjpi6UWNSINjcTGkl9H7MlnCGFDuDpBQZ-l-1orGh6y4XHybt9dAdRufyX7GLh_OKM7XS83yz5F4zQgrIZ-9JZqFrpj_fGDMBYsNKuzxjbTpYVbEU=w1440)

每张乳腺 X 光片包含四张图像——每侧乳房两个不同角度的视图。

## 评估 AI 系统的表现

我们将 AI 系统的表现与原始筛查就诊中人类专家个人做出的判断进行了比较。在这一评估中我们发现，与人类专家相比，AI 的假阳性（被错误转诊做进一步检查的女性）在美国受试者中绝对降低 5.7%，在英国受试者中降低 1.2%；假阴性（被错误漏诊、未转诊做进一步检查的女性）在美国受试者中降低 9.4%，在英国受试者中降低 2.7%。更全面的结果请参见[论文](https://www.nature.com/articles/s41586-019-1799-6.epdf?author_access_token=V_LKV2xpSv9G1dhANYeWM9RgN0jAjWel9jnR3ZoTv0M5zwPVx5jT4z_z-YkUZTBT6_1AtRXi8QouJM7xB-oSN-cVBoH7f_QTgx-yQN3UBEVfkvO1_5urNT-CZHGCEQNGlCuO69tMQYak4SmdoDqyzg%3D%3D)。

![两条 ROC 曲线，对比 AI 系统与人类阅片者在乳腺癌筛查中的表现。左图展示英国结果（3 年内乳腺癌），AI 曲线旁标注了第一阅片者均值、第二阅片者均值、仲裁共识以及 AI 的工作点。右图展示美国结果（2 年内乳腺癌），呈现 AI 系统的 ROC 曲线、其工作点，以及代表人类阅片者均值的标记。](https://lh3.googleusercontent.com/_1zMrIxm4bwgRtC-A54GK0QErvYmo2AYSppuuMpoxKbQHTtBCO9Nppv0SpGThAOyZaoFFCFfmyF66d4am00E9X1ex3Qsr2XYAERN1B-6Z7tpMVzhsg=w1440)

仅凭筛查性乳腺 X 光片，AI 系统就能准确预测患者的活检是否会呈乳腺癌阳性（请注意，只有一小部分筛查就诊最终会进行活检）。它的预测比人类专家个人更准确，且假阳性率更低（英国数据集以三年内癌症预测为准，美国数据集以两年内为准）。左上角表示峰值性能，即无假阳性也无假阴性。图片来源：McKinney et al, Nature

## 跨人群的泛化能力

为了评估该 AI 系统是否能够在不同人群和不同筛查环境中泛化，我们进行了一项实验：只允许 AI 从英国受试者的数据中学习，然后在美国受试者的数据上进行评估。这一实验表明，该 AI 系统在美国数据上仍然超越了人类专家的表现。

这是未来研究一条令人鼓舞的方向，也让我们对 AI 系统的稳健性更有信心。即使在没有大量筛查性乳腺 X 光影像历史可供训练的地区，AI 诊断系统也可能发挥作用。

## 未来研究与应用前景

我们尚未确定如何最好地将 AI 系统部署到乳腺 X 光检查的临床应用中。不过，我们研究了其中一种可能的场景：将 AI 系统用作「第二阅片者」。我们通过如下方式进行模拟：把 AI 系统的预测视为对每张乳腺 X 光片的独立第二意见，替代英国「双重阅片」体系中的「第二阅片者」。当 AI 与临床医生意见不一致时，将启动现有的仲裁流程。在这些模拟实验中，我们展示了 AI 辅助的双重阅片系统只需承担目前第二阅片者 12% 的工作量，就能达到与英国体系相当（非劣效）的表现。

这项技术能在多大程度上惠及乳腺癌筛查项目，还需要进一步的研究，包括前瞻性临床研究，才能完全厘清。
