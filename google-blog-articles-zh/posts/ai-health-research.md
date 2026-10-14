---
title: "运用技术理解与治疗疾病"
title_en: "Applying technology to understand and treat disease"
source: https://blog.google/innovation-and-ai/technology/health/ai-health-research/
site: google-blog
date: 2026-10-12
crawled: 2026-10-15
translated: 2026-10-15
---

# 运用技术理解与治疗疾病

> 原文：[Applying technology to understand and treat disease](https://blog.google/innovation-and-ai/technology/health/ai-health-research/) · Google

Google 的健康研究与工具，涵盖了从基础细胞发现、实验室分析到患者影响的完整链条。过去五年间，Google 各团队发表了 90 篇关于理解与应对疾病的同行评审研究论文，累计获得超过 9 万次引用。基于[技术可以加速科学、改善生活](https://blog.google/innovation-and-ai/technology/ai/ai-applications-science-people/)这一愿景，我们正与临床医生、学术机构和研究人员合作，确保各项发现能够走出实验室、惠及患者。以下是我们如何推动医学研究与公共卫生解决方案的进展。

## 解码疾病的分子机制

AlphaGenome Atlas 是迄今最全面的预测目录，涵盖人类基因组中任何单个字母变异会如何影响分子生物学。

![照片展示了一个培养皿的特写。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Genetic_Variants.width-1200.format-webp_PDssfpH.webp)

要有效治疗一种疾病，就需要理解它在分子、基因与细胞层面如何运作。我们的早期生物学模型充当科学家协作研究工具，揭示自然隐藏的运行机制，推动医学发现。

- **加速药物发现：**巴塞罗那全球健康研究所的研究人员利用 [AlphaFold](https://deepmind.google/science/alphafold/) 对 3 万种化合物进行了针对恰加斯病（Chagas disease）的抗寄生虫活性虚拟筛选。恰加斯病是一种被忽视的热带疾病，影响约 800 万人，若不及时治疗可能导致危及生命的并发症。这项研究帮助该研究所找到了两种可重新用于恰加斯病的 FDA 已批准药物，缩短了从发现到治疗的时间。
- **绘制与衰老相关的基因变异图谱：**要识别哪些罕见基因变化与特定疾病相关非常困难，因为大量无影响的突变会形成「背景噪音」。埃克塞特大学的研究人员利用 [AlphaGenome Atlas](https://deepmind.google/blog/alphagenome-atlas-a-predictive-map-of-every-possible-dna-letter-change-in-the-human-genome/) 检索了 5.4 万多名个体的基因组数据，精确定位了驱动人体内关键循环蛋白丰度的特定变异，包括 PLA2G7（与衰老相关）和 EGLN1（重要的细胞氧传感器）。
- **纳米尺度重建大脑：**我们与哈佛大学 Lichtman 实验室合作，[以纳米级分辨率重建了一块人脑组织](https://research.google/blog/ten-years-of-neuroscience-at-google-yields-maps-of-human-brain/)，并通过 [Neuroglancer](https://h01-release.storage.googleapis.com/explore.html) 公开提供了这些数据。我们还绘制了包括[果蝇](https://www.cell.com/cell/fulltext/S0092-8674%2826%2900942-6)、[斑马鱼幼体](https://www.biorxiv.org/content/10.1101/2025.06.10.658982v1)和[鸣禽](https://www.biorxiv.org/content/10.1101/2025.10.25.684569v1)在内的模式生物的大脑。这些神经映射资源让研究人员能够深入推进大脑功能的研究。

## 加速打造医学解决方案工具

在 AlphaFold 支持下开发的蛋白质可视化图谱。

![一名男子看着电脑屏幕，屏幕上在深色背景下显示一个由红绿原子与化学键构成的 3D 分子结构。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Understanding_Disease_inline_2.width-1200.format-webp.webp)

实验室是生物学发现得到验证、工程化改造，并转化为潜在医学与公共卫生解决方案的地方。我们的模型用能够快速、准确处理海量数据的系统，取代了缓慢、迭代的流程。

- **以超快速基因组测序辅助遗传诊断：**我们与斯坦福大学医学院合作，在一项临床试验中使用 [DeepVariant](https://www.nature.com/articles/nbt.4235) 和 [DeepConsensus](https://blog.google/innovation-and-ai/products/a-new-genome-sequencing-tool-powered-with-our-technology/)，帮助确定时间紧迫病例的遗传疾病病因。该项目实现了不到 8 小时完成全基因组测序的遗传诊断这一前所未有的成绩，[促成了挽救生命的干预](https://www.nejm.org/doi/full/10.1056/NEJMc2112090)，并因此获得[吉尼斯世界纪录](https://stanmed.stanford.edu/genome-sequencing-breaks-speed-record/)认证。
- **从零开始设计定制酶：**我们推出了 [AlphaProtein Novo](https://www.biorxiv.org/content/10.64898/2026.10.01.756017v1.full.pdf)，一个基于第一性原理创建自然界中不存在的新酶的机器学习流水线。在实验室测试中，它成功设计出可合成关键药物基序的定制酶，以及可在极端条件下降解有害环境塑料的酶——这展示了设计出超越自然界已知范围的功能性蛋白质的能力。
- **支持前瞻性公共卫生行动：**一个社区的健康与其[地理环境密切相关](https://blog.google/innovation-and-ai/technology/health/google-earth-ai-global-public-health/)。我们正在将 [Google Earth AI](https://ai.google/earth-ai/) 模型与环境、天气、流动等数据相结合，[帮助公共卫生负责人](https://blog.google/innovation-and-ai/technology/health/google-earth-ai/)预测疾病暴发，并向脆弱社区提供医疗服务。在 [WHO 非洲区域办事处](https://afro.who.int/)（WHO AFRO）与刚果（金）[INRB](https://www.inrb.net/) 的新研究中，对话式地理空间模型取代了耗时数周的人工编码，帮助更早识别埃博拉的暴露与传播风险——使当地响应人员得以主动部署移动实验室。

## 用机器学习模型为医疗服务提供者提供支持

新的乳腺 X 线筛查系统有助于发现历来被漏诊的间隔期癌症，并减轻专科医生的阅片工作量。

![一名留着深色短发、身穿浅色外套的医护人员正在查看电脑屏幕上的乳腺 X 线影像。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Understanding_Disease_inline_3.width-1200.format-webp.webp)

医学突破只有真正帮助到现实中的人才有意义。我们的研究表明，机器学习模型既能辅助疾病检测，也能减轻行政工作负担，让医疗服务提供者专注于照护患者。

- **标示历来被漏诊的癌症征象：**在与帝国理工学院及英国国家医疗服务体系（NHS）合作、发表于 *Nature Cancer* 的[两](https://www.nature.com/articles/s43018-026-01128-z)[项](https://www.nature.com/articles/s43018-026-01127-0)研究中，我们在 12.5 万名女性中评估了一套乳腺 X 线筛查系统。该系统[发现](https://blog.google/innovation-and-ai/technology/health/google-ai-breast-cancer-detection/)了 25% 的历来被漏诊的间隔期癌症，同时显示出可将专科医生阅片工作量最多降低 40% 的可能——这有望为面临严重放射科医生短缺的医疗体系提供关键支持。
- **发现隐藏的儿童白血病突变：**当 Children's Mercy Hospital 将 [DeepSomatic](https://blog.google/innovation-and-ai/technology/research/deepsomatic-an-open-source-ai-model-is-speeding-up-genetic-analysis-for-cancer-research/) 应用于此前已完成测序的真实儿童白血病病例时，它确认了所有已知变异，同时还检测出 10 个此前被漏掉的突变——而这一切是在仅有肿瘤样本（缺少对照样本）的困难条件下完成的。DeepSomatic 已公开可用，有望为围绕患者风险与靶向治疗的临床判断提供依据。
- **预测全球流感高峰：**一个 Google [流感预测模型](https://blog.google/innovation-and-ai/models-and-research/google-research/google-science-ai-flu-forecasts/)在 2025–2026 流感季因预测流感相关住院人数而被美国疾病控制与预防中心（CDC）评为第一名。该模型使用我们的 [Empirical Research Assistance](https://research.google/blog/four-ways-google-research-scientists-have-been-using-empirical-research-assistance/) 工具开发，在准确匹配实际住院数据方面胜过了其他 38 个系统，展现了这项技术如何帮助公共卫生官员预判医疗服务需求，更好地为季节性疾病暴发做准备。

## 让人人都能享有更好的健康

变革健康事业需要科学家、研究人员与机构携手同行。因此，我们为科学界提供先进模型与开放获取平台来推动突破性研究，并提供研究所需的公益资金与算力，帮助这些研究落地应用。

通过 Google.org，我们正在支持[马凯雷雷大学传染病研究所](https://blog.google/company-news/outreach-and-initiatives/google-org/announcing-ai-for-science-awardees/)等组织利用 AlphaFold 与 AlphaMissense 预测疟疾耐药突变，并支持宾夕法尼亚大学利用 AlphaProteo 与 AlphaFold 设计新型细胞疗法，以增强针对实体瘤和复杂疾病的治疗手段。2026 年，Google.org 已向全球范围内运用先进模型变革疾病理解与治疗方式的组织提供了超过 6000 万美元的资金。

通过与疾病在每一个阶段正面交锋，我们可以把最棘手的人类健康挑战转化为可行的解决方案，帮助世界各地的人们活得更长、更健康。
