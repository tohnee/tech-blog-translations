---
title: "用 AI 绘制、建模并理解自然"
title_en: "Mapping, modeling, and understanding nature with AI"
source: https://deepmind.google/blog/mapping-modeling-and-understanding-nature-with-ai/
site: deepmind
date: 2025-11-05
crawled: 2026-09-13
translated: 2026-09-13
---

# 用 AI 绘制、建模并理解自然

> 原文：[Mapping, modeling, and understanding nature with AI](https://deepmind.google/blog/mapping-modeling-and-understanding-nature-with-ai/) · Google DeepMind

AI 模型可以帮助绘制物种地图、保护森林，并聆听世界各地的鸟鸣

地球的生物圈是其植物、动物、真菌和其他生物的总和。每一天，我们都依赖它生存——我们呼吸的空气、饮用的水、吃的食物，全都由地球的生态系统产出。

随着对土地和资源需求的不断增长给这些生态系统及其物种带来压力，[人工智能（AI）可以成为保护它们的一项变革性工具](https://blog.google/outreach-initiatives/sustainability/how-were-using-ai-to-help-nature-and-people-flourish-together/)。它可以让政府、企业和保护组织更便利地收集野外数据，把这些数据整合为新的洞见，并将洞见转化为行动。它还能为更好的规划提供依据，并在规划落地后监测其成效。

今天，我们宣布新的生物圈研究成果：预测毁林风险、一项绘制地球物种分布区的新项目，以及我们的生物声学模型 Perch 的最新进展。

## 预测毁林

森林是生物圈最关键的支柱之一——储存碳、调节降雨、缓解洪水，并庇护着地球大部分陆地生物多样性。然而遗憾的是，尽管意义重大，森林仍在以惊人的速度消失。

借助天基遥感，人们追踪毁林情况已有 20 多年。最近，我们与[世界资源研究所（World Resources Institute）](https://www.wri.org/)更进一步，针对 2000 至 2024 年，以前所未有的 1 平方公里分辨率开发了一个[森林损失驱动因素](https://www.wri.org/insights/forest-loss-drivers-data-trends)模型——涵盖从农业、伐木到采矿和火灾的各类因素。

今天，我们发布一个用于[预测毁林](https://research.google/blog/forecasting-the-future-of-forests-with-ai-from-counting-losses-to-predicting-risk/)风险的基准数据集。该模型只使用纯卫星输入，避免了道路等特定本地输入图层的需求，并采用了围绕视觉 Transformer（vision transformer）构建的高效模型架构。这一方法可以精准、高分辨率地预测毁林风险，最小尺度可达 30 米，并覆盖大范围区域。

![一张地图，显示 2023 年东南亚某地区的毁林风险，绿色表示已毁林区域，红色表示毁林风险较高。](https://lh3.googleusercontent.com/WAK2GGYAiNbQhdJ_HNmg4z9TNUhhbH-OL33rkDvgCr-TNwpTbqaHaYXVFrO4elmMvGD69EAQVOyOIT9FgngfA7MN6FWzQjuD_1vmNV5uW1UjO_qXJA=w1440-h810-n-nu)

一张地图，显示 2023 年东南亚某地区的毁林风险，绿色表示已毁林区域，红色表示毁林风险较高。底图数据 ©2025，影像 ©2025 Airbus、CNES / Airbus、Landsat / Copernicus、Maxar Technologies

## 为地球物种的分布建模

要保护地球上的濒危物种，我们必须知道它们在哪里。已知物种超过 200 万种，还有数百万种有待发现和命名，这是一项浩大的工程。

为帮助应对这一难题，Google 研究人员正在开发一种[新的 AI 驱动方法](https://ar5iv.labs.arxiv.org/html/2503.11900)，以前所未有的规模生成物种分布区地图——涵盖更多物种、覆盖全球更多区域、分辨率也高于以往。这个图神经网络（GNN）模型将物种野外观测的开放数据库、来自 [AlphaEarth Foundations](https://deepmind.google/discover/blog/alphaearth-foundations-helps-map-our-planet-in-unprecedented-detail/) 的[卫星嵌入](https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_SATELLITE_EMBEDDING_V1_ANNUAL)，以及物种性状信息（如体重）结合在一起。这一方法使我们能够一次性推断出许多物种可能的基础地理分布，科学家随后可以用额外的本地数据与专业知识对这些推断分布进行修正。

在与 [QCIF](https://www.qcif.edu.au/) 和 [EcoCommons](https://www.ecocommons.org.au/) 研究人员开展的试点中，我们用模型绘制了澳洲哺乳动物的分布图，例如大袋鼯（Greater Glider）：一种夜间活动、拖着蓬松尾巴的有袋动物，栖息于古老的桉树原始林中。今天，我们还将通过 [UN Biodiversity Lab](https://map.unbiodiversitylab.org/earth?basemap=grayscale&coordinates=-25.448847,132.236151,3&layers=UNBL.layer.australian-mammal-species-distributions_100) 和 [Earth Engine](https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_species_distribution_models_australia_mammals_v0) 发布其中 23 个物种地图。

借助人工智能，Google 正在为「物种栖息在哪里」这一问题带来新的认识，帮助科学家和决策者更好地保护地球野生动物。

## 通过生物声学倾听

理解并为生态系统建模的一切努力，最终都依赖于实地监测。AI 在这里同样能发挥关键作用：从监测设备自动识别栖息地与物种，为传统生态野外监测——出了名的困难与昂贵——提供增强。

一个引人注目的例子是生物声学（bioacoustics）。鸟类、两栖动物、昆虫等物种通过声音交流，这使声音成为识别当地物种、了解生态系统健康状况的绝佳模态。可靠且价格合理的生物声学监测器随处可得。但这些设备会产生海量音频数据集，其中充满了未知且相互重叠的声音，规模大到无法人工审听，又难以自动分析。

为了帮助科学家和保护工作者理清这种复杂性，我们最近发布了 [Perch 2.0](https://www.kaggle.com/models/google/bird-vocalization-classifier/tensorFlow2/perch_v2)——我们的动物鸣声分类器的升级版。这个新模型不仅在鸟类识别上达到业界领先水平，还以基础模型的形式提供，使野外生态学家能够快速适配模型，在地球任何角落识别新物种和新栖息地。

我们尤其为与夏威夷大学的合作感到自豪：Perch 正在为濒危管舌雀（honeycreeper）的保护措施提供指引，同时也被用于识别幼鸟鸣声，以了解种群健康状况。

Google 的 Perch 模型帮助科学家利用 AI 识别自然中的声音——比如夏威夷濒危鸟类的鸣叫——从而及时采取保护行动。

## AI for Nature 的未来

这项工作的目标是让各级决策者更便利地采取行动保护地球。但只有当数据足够全面——真正捕捉到某一生态系统各层面的实际状况——更好的数据才能带来更好的决策。

因此，我们正在努力把这些模型以及其他模型整合起来，结合来自更多模态的数据，如卫星数据、图像、生物声学、文档等等。同时，将这些与人类活动模型——如土地利用变化、农业实践——以及农业产量、防洪等与人类密切相关的后果模型连接起来。

通过让政策制定者全面了解生物圈面临的威胁，我们可以帮助他们采取行动，保护未来世代的植物、动物和人类。如果我们能为环境建模，或许就能帮助它欣欣向荣。

进一步了解我们的 AI 与可持续发展工作

[Google Earth AI](https://blog.google/technology/research/new-updates-and-more-access-to-google-earth-ai/)[Google Earth Engine](https://cloud.google.com/blog/topics/sustainability/look-back-at-a-year-of-earth-engine-advancements)[AlphaEarth Foundations](https://deepmind.google/blog/alphaearth-foundations-helps-map-our-planet-in-unprecedented-detail/)

## 致谢

本研究由 Google DeepMind 与 Google Research 共同开发。

Google DeepMind：Andrea Burns、Anton Raichuk、Arianna Manzini、Bart van Merrienboer、Burcu Karagol Ayan、Dominic Masters、Drew Purves、Jenny Hamer、Julia Haas、Keith Anderson、Matt Overlan、Maxim Neumann、Melanie Rey、Mustafa Chasmai、Petar Veličković、Ravi Rajakumar、Tom Denton、Vincent Dumoulin

Google Research 与 Google 合作伙伴：Ben Williams、Charlotte Stanton、Dan Morris、Elise Kleeman、Lauren Harrell、Michelangelo Conserva

我们还要感谢 UNEP-WCMC 和 QCIF 的合作伙伴，感谢其他合作者 Aditee Kumthekar、Aparna Warrier、Artlind Kortoci、Burooj Ghani、Christine Kaeser-Chen、Grace Young、Kira Prabhu、Jamie McPike、Jane Labanowski、Jerome Massot、Kuan Lu、Mélisande Teng、Michal Kazmierski、Millie Chapman、Rishabh Baghel、Scott Riddle、Shelagh McLellan、Simon Guiroy、Stefan Kahl、Tim Coleman 和 Youngin Shin，同时感谢 Peter Battaglia 和 Kat Chou 的支持。
