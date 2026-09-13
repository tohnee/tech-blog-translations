---
title: "AI 如何通过提前的天气预报帮助 3800 万农民"
title_en: "How AI is helping 38 million farmers with advance weather predictions"
source: https://blog.google/innovation-and-ai/technology/research/indian-farmers-monsoon-prediction/
site: google-blog
date: 2025-09-15
crawled: 2026-09-13
translated: 2026-09-13
---

# AI 如何通过提前的天气预报帮助 3800 万农民

> 原文：[How AI is helping 38 million farmers with advance weather predictions](https://blog.google/innovation-and-ai/technology/research/indian-farmers-monsoon-prediction/) · Google

今年夏天，印度 3800 万农民收到了由 AI 驱动的季风季开始时间预报，帮助他们就本季作物何时播种做出更明智的决策。这些预报部分由 Google Research 的模型 NeuralGCM 提供支持，该模型将传统的基于物理的建模与机器学习相结合，以提高模拟的精度和效率。

## 一个预测天气与气候的 AI 模型

多年来，天气和气候模型一直成本高昂且复杂，往往需要超级计算机才能运行。Google Research 的团队想看看能否更高效、更准确地构建这些模型，于是诞生了 NeuralGCM。与纯粹依赖硬编码物理规律的传统模型不同，这个 AI 驱动的模型在数十年的历史天气数据上训练，以推断规律并从过去的事件中学习，同时仍然运用物理学。关键在于，它的设计灵活而高效——可以在一台笔记本电脑上运行，让高质量预报更容易为科学界所用。

## 与芝加哥大学的合作

当我们开源 NeuralGCM 时，我们希望社区能利用这个新工具来驱动自己的创新应用。芝加哥大学的 [Human-Centered Weather Forecasts Initiative](https://humancenteredforecasts.climate.uchicago.edu/)（以人为本的天气预报计划）正是这样做的。他们意识到，对印度农民而言，影响最深远、却也日益困难的决策之一，就是何时把种子播进土里。热带地区数亿小农的生计，都依赖关于每年雨季（即季风）何时来临的信息。然而，准确预测季风何时开始——尤其是在较长提前量和局地尺度上——始终是一个百年难题。

通过严谨测试多个 AI 天气模型，芝加哥大学团队发现，将 NeuralGCM 与欧洲中期天气预报中心（ECMWF）的人工智能/综合预报系统（AIFS）等其他先进模型以及历史数据相融合，正是完成这项工作的正确工具。它最迟可提前一个月准确预测印度季风的开始，甚至捕捉到了季风推进过程中一段反常的少雨期。

左图显示的是 120 年历史数据的平均值（即通常预期的情况）。中图是印度气象局实际观测到的结果。右图则是 AI 预报提前 15 天做出的预测。

图片来源：芝加哥大学气候与增长研究所（Institute for Climate and Growth）的 Human-Centered Weather Forecasts Initiative。

![三联地图显示印度轮廓及用颜色标示的降雨数据。三个面板分别对比了历史平均值、2025 年一段两周的少雨期，以及 AI 对该少雨期的成功预报。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/videoframe_4656.width-1200.format-webp.webp)

## 真实世界的大规模影响

在与印度农业与农民福利部的合作中，这个由芝加哥大学开创的 AI 模型融合方案，今年夏天通过短信向 3800 万农民成功送达了定制化的提前预报。这项举措帮助农民主动调整种植决策——何时播种、是否多买种子、改种其他作物，还是干脆等待——使他们得以适应异常推迟的季风季。

芝加哥大学已有的[研究](https://climate.uchicago.edu/impacts/providing-farmers-with-better-forecasts-helps-them-adapt-to-climate-change/)表明，提供提前约一个月的准确预报，农民可以使其决策与即将到来的天气保持一致，从而改善结果。该研究发现，提前预报能使他们的年收入几乎翻倍。

这个项目有力地证明：源自研究的 AI 基础技术可以服务于真实世界的用例，最终帮助世界各地的社区建设气候韧性。
