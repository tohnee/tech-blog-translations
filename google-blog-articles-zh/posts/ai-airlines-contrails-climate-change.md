---
title: "AI 如何帮助航空公司减轻凝结尾迹的气候影响"
title_en: "How AI is helping airlines mitigate the climate impact of contrails"
source: https://blog.google/innovation-and-ai/technology/ai/ai-airlines-contrails-climate-change/
site: google-blog
date: 2023-08-08
crawled: 2026-09-13
translated: 2026-09-13
---

# AI 如何帮助航空公司减轻凝结尾迹的气候影响

> 原文：[How AI is helping airlines mitigate the climate impact of contrails](https://blog.google/innovation-and-ai/technology/ai/ai-airlines-contrails-climate-change/) · Google

凝结尾迹（contrails）——你有时会在飞机后方看到的细长白色线条——对我们的气候有着大得惊人的影响。2022 年的 [IPCC 报告](https://www.ipcc.ch/report/ar6/wg3/downloads/report/IPCC_AR6_WGIII_Chapter10.pdf)指出，由凝结尾迹形成的云贡献了全球航空变暖影响的约 35%，超过全球航空煤油影响的一半。
[1](#footnote-1)
[Google Research](https://research.google/) 与 [American Airlines](https://news.aa.com/esg/) 及 [Breakthrough Energy](https://breakthroughenergy.org/) 合作，汇聚了海量数据——如卫星图像、天气和航路数据——并利用 AI 开发出凝结尾迹预报图，以测试飞行员能否选择不产生凝结尾迹的航线。

夜间与白天凝结尾迹辐射效应的直观说明。夜间凝结尾迹往往比白天的更增温，因为它们只截留热量。

![一张信息图，显示飞机产生凝结尾迹及其与辐射力相互作用的方式。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Contrails_infographic_1.width-1200.format-webp.webp)

当飞机穿过湿度层时就会形成凝结尾迹，根据大气条件不同，它们可以以卷云的形式持续存在几分钟或几小时。虽然这些额外的云在白天可以将阳光反射回太空，但它们也会截留大量原本会离开地球大气层的热量。这就产生了净增温效应。避免飞经会产生凝结尾迹的区域可以减少增温。难点在于要知道哪些航线会产生凝结尾迹。

## 减少凝结尾迹的增温影响

American Airlines 的一组飞行员在六个月里执行了 70 个测试航班，使用 Google 基于 AI 的预测（并与 Breakthrough Energy 的[开源凝结尾迹模型](https://py.contrails.org/)交叉比对）来避开可能产生凝结尾迹的高度。在这些测试飞行之后，我们分析了卫星图像，发现飞行员能够将凝结尾迹减少 54%。这是首个证明商业航班可以切实验证地避免凝结尾迹、从而降低其气候影响的实证。

American Airlines 飞行运行董事总经理 John P. Dudley 机长（右）与副驾驶 Tammy Caudill（左），摄于首次避让凝结尾迹航班的驾驶舱。他们在 PACE 的 FPO 应用中使用我们的预测来避开凝结尾迹。

![两名飞行员在避让凝结尾迹测试航班驾驶舱内的照片。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/pasted_image_0_7_qKhuQ8P.width-1200.format-webp.webp)

我们与 American Airlines 测试的另一项重要发现是，尝试避免产生凝结尾迹的航班多消耗了 2% 的燃油。近期研究表明，只需调整一小部分航班，就能避免大部分凝结尾迹带来的增温。因此，摊到航空公司的全部航班上，总燃油影响可能低至 0.3%。
[2](#footnote-2)
这意味着，利用我们现有的预测，大规模避免凝结尾迹的成本约为每吨二氧化碳当量（CO2e）5–25 美元，使其成为一种高性价比的减温措施，而且预计效果还会进一步改善。

利用 AI 和 GOES-16 卫星图像在美国上空探测到的凝结尾迹。

![美国上空探测到的凝结尾迹动画。](https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/cropped_contrails_app_TSEkvUS.gif)

## 下一步是什么？

避让凝结尾迹有潜力成为一种高性价比、可扩展的方案，以减少飞行的气候影响。我们将继续研发，实现自动避让、锁定影响最大的凝结尾迹，并改进基于卫星的验证。我们致力于与整个航空业合作，利用 AI 在未来几年让凝结尾迹避让成为现实。
