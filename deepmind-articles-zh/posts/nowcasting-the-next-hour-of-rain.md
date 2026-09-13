---
title: "临近预报：下一小时的降雨"
title_en: "Nowcasting the next hour of rain"
source: https://deepmind.google/blog/nowcasting-the-next-hour-of-rain/
site: deepmind
date: 2021-09-29
crawled: 2026-09-13
translated: 2026-09-13
---

# 临近预报：下一小时的降雨

> 原文：[Nowcasting the next hour of rain](https://deepmind.google/blog/nowcasting-the-next-hour-of-rain/) · Google DeepMind

我们的生活依赖于天气。根据[一项研究](https://www.bbc.com/future/article/20151214-why-do-brits-talk-about-the-weather-so-much)，在英国的任何一个时刻，全国都有三分之一的人在过去一小时内谈论过天气，这反映了天气在日常生活中的重要性。在各种天气现象中，雨尤其重要，因为它影响着我们的日常决策：要不要带伞？遭遇暴雨的车辆该如何规划路线？户外活动要采取哪些安全措施？会不会发生洪水？

[我们的最新研究](https://www.nature.com/articles/s41586-021-03854-z)是一项最先进的模型，推动了[降水临近预报](https://public.wmo.int/en/resources/bulletin/nowcasting-guidelines-%E2%80%93-summary)（Precipitation Nowcasting，即对未来 1-2 小时降雨及其他降水现象的预测）这一科学领域的发展。在与英国气象局（Met Office）合作撰写并发表于《自然》（Nature）的[论文](https://www.nature.com/articles/s41586-021-03854-z)中，我们直接攻克了天气预报中的这一重要[重大挑战](https://www.nssl.noaa.gov/about/challenges/)。这项环境科学与 AI 之间的合作以决策者的实际价值为导向，为降雨临近预报开辟了新途径，并指出了 AI 在支持我们应对不断变化的环境中的决策挑战方面的机遇。

## 短期天气预报

纵观历史，天气预报在我们的社群和国家中一直占据重要地位。[中世纪的气象学家](https://www.cambridge.org/core/books/medieval-meteorology/12DCC7DA683729A4E520C76ADCF6502D)起初借助星辰进行预测。后来，人们开始记录季节与降雨规律的表格。几个世纪之后，Lewis Fry 构想了一座「[预报工厂](https://www.emetsoc.org/resources/rff/)」（Forecast Factory），利用计算和大气物理方程来预测全球天气。在这部不断演进的天气预报史册中，我们如今增添了一篇关于机器学习在预报中作用的新篇章。

如今的天气预报由强大的[数值天气预报](https://www.metoffice.gov.uk/weather/learn-about/how-forecasts-are-made/computer-models/history-of-numerical-weather-prediction)（NWP）系统驱动。通过求解物理方程，NWP 系统能够提供未来数天至关重要的全球尺度预测。然而，它们难以在两小时以内的短预报时效上生成高分辨率预测。临近预报（nowcasting）正是填补了这一关键时间段内的性能空白。

临近预报对水务管理、农业、航空、应急规划和[户外活动](https://journals.ametsoc.org/view/journals/wefo/25/6/2010waf2222417_1.xml)等领域至关重要。天气传感技术的进步使得高分辨率雷达数据——用于测量地面降水量的数据——能够以高频率获取（例如每 5 分钟一次、分辨率 1 公里）。现有方法难以胜任的关键领域与高质量数据的可得性相结合，为机器学习在临近预报领域做出贡献创造了机会。

![示意图：降雨深度生成模型如何利用过去 20 分钟的上下文数据，生成未来 90 分钟的降水临近预报。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6227e31239003803b4eb74db_Fig201.gif)

利用降雨深度生成模型（DGMR），过去 20 分钟的观测雷达被用于对未来 90 分钟做出概率性预测。

## 用于临近预报的生成模型

我们专注于降雨临近预报：即对未来最多 2 小时的预测，需要捕捉降雨量、时间和位置。我们采用一种被称为生成建模（generative modelling）的方法，基于过去的雷达数据对未来雷达做出细致而合理的预测。从概念上讲，这是一个生成「雷达电影」的问题。借助这类方法，我们既能准确捕捉大尺度事件，又能生成多种可供选择的降雨情景（即所谓集合预报，ensemble predictions），从而探索降雨的不确定性。我们在研究中使用了英国和美国的雷达数据。

我们尤其关注这些模型对中到大雨事件的预测能力，因为这类事件对民众和经济的影响最大。我们证明，与竞争方法相比，我们的方法在这些情形下取得了统计显著的改进。重要的是，我们在英国国家气象服务机构英国气象局对 50 多位专业气象学家进行了认知任务评估，**在与广泛使用的临近预报方法的对比中，专家们在 89% 的情况下将我们的新方法评为首选**，这表明我们的方法能够为现实世界的决策者提供洞见。

![四幅英国雷达图，展示标记为 Target、DGMR、PySTEPS 和 UNet 的降雨模式。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6227e32e3d49b17ff5eba816_Fig202.gif)

2019 年 4 月英国上空的一个具有挑战性的事件（Target 为观测雷达）。我们的生成方法（DGMR）比平流外推方法（PySTEPS）更好地捕捉了环流、强度和结构，并更准确地预测了东北部的降雨和移动。与确定性深度学习方法（UNet）不同，DGMR 还能生成清晰的预测结果。

![四幅英国雷达图，展示标记为 Target、DGMR、PySTEPS 和 UNet 的降雨模式。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6227e35deb85793243440c30_Fig203.gif)

2019 年 4 月美国东部上空的一次强降水事件（Target 为观测雷达）。与平流外推方法（PySTEPS，其强度常常偏高）相比，生成方法 DGMR 在降水强度与范围之间取得了平衡，并且不会像确定性深度学习方法（UNet）那样出现模糊。

## 下一步计划

通过统计、经济和认知分析，我们展示了一种全新且具竞争力的雷达降水临近预报方法。任何方法都有其局限，在提高长期预测精度以及对罕见强降水事件的准确性方面仍需更多工作。未来的工作需要我们开发更多评估性能的方式，并进一步将这些方法专门化以适用于特定的现实世界应用。

我们认为这是一个令人兴奋的研究领域，希望我们的论文能够通过提供数据与验证方法，使具有竞争力的验证和业务实用性成为可能，从而为新的研究奠定基础。我们也希望与英国气象局的这项合作能够促进机器学习与环境科学的更深度融合，更好地支持我们在气候变化中的决策。

阅读 2021 年 9 月 30 日出版的《自然》（Nature）杂志上的论文 [Skillful precipitation nowcasting using Deep Generative Models of Radar](https://www.nature.com/articles/s41586-021-03854-z)，其中对模型、数据和验证方法进行了详尽的讨论。你还可以通过 [GitHub](https://dpmd.ai/github_nowcasting) 探索我们用于训练的数据，并获取一个针对英国的预训练模型。

**致谢**

我们感谢英国气象局以及所有合作者和顾问对这项工作的贡献。
