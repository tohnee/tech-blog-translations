---
title: "问问科学家：研究人员如何用 AI 预测洪水？"
title_en: "Ask a Scientist: How can researchers use AI to predict a flood?"
source: https://blog.google/innovation-and-ai/technology/research/flood-prediction-ai/
site: google-blog
date: 2026-08-18
crawled: 2026-09-13
translated: 2026-09-13
---

# 问问科学家：研究人员如何用 AI 预测洪水？

> 原文：[Ask a Scientist: How can researchers use AI to predict a flood?](https://blog.google/innovation-and-ai/technology/research/flood-prediction-ai/) · Google

2018 年，我们在印度[试点](https://blog.google/products-and-platforms/products/search/helping-keep-people-safe-ai-enabled-flood-forecasting/)了一款依靠实时河流数据预测洪水的洪水预报模型。此后，我们在 AI 方面的[进步](https://research.google/blog/a-flood-forecasting-ai-model-trained-and-evaluated-globally/)使我们能够为全球 150 个国家、20 多亿人所居住的地区做出预测。2026 年 3 月，我们[发布了 Groundsource](https://blog.google/innovation-and-ai/technology/research/gemini-help-communities-predict-crisis/)——一种全新的 AI 驱动方法论，将公开的灾害数据转化为高质量的数据档案，首先从城市山洪开始。我们与 Google Research 资深研究科学家 Deborah Cohen 进行了对谈，了解 AI 如何让洪水预测成为可能，以及这项研究在预测其他自然灾害方面的潜力。

**你在 Google 做什么工作？**

我在气候危机韧性（Climate Crisis Resilience）团队负责洪水预测工作。我们的目标是利用 AI 让人们免受自然灾害的伤害，从洪水开始——它是最常见、也最致命的自然灾害之一。预警能够避免洪水造成的很多危害。这正是我们启动 Google 洪水预测计划（Google Flood Forecasting Initiative）的原因：我们希望每个人都能获得预报和预警，从而安全无虞、心中有数。

**Google 如何用 AI 预测洪水？**

自近十年前我们启动这项研究以来，方法已经变了好几次！但最基本地说，我们使用一组模型来处理海量全球数据——包括降雨、河流水位和地表状况等——以便在河流洪水来袭最多七天前、城市山洪来袭最多 24 小时前做出预测。这些预测存放在我们的 [Flood Hub](https://sites.research.google/floods/) 工具中，当人们在其所在地区查找洪水相关信息时，也会显示在 Search 中。我们还提供 Floods API，让组织能够获取洪水预测，帮助他们在最严重的洪水来袭之前预警并支援民众。

Flood Hub 实况

![Flood Hub 工具截图，显示一幅以不同深浅标示洪水风险的世界地图。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Flood_Hub.width-1200.format-webp.webp)

**Flood Hub 是做什么的？**

Flood Hub 汇集来自世界各地的顶尖气象数据，利用 AI 在地图上生成预测警报。相较于通常需要当地水位等历史数据来进行校准的传统洪水模型，这是一个巨大的飞跃。我们的 AI 让我们可以调用全球各地的信息，在没有历史数据的地点也能提供预测——这一点至关重要，因为最需要预警的人往往生活在数据匮乏的地区。

我们最初构建 Flood Hub 工具时，只能预测河流何时泛滥。在过去几年中，我们构建了一种名为 Groundsource 的新 AI 方法论，将覆盖范围扩展到了城市山洪。

**为什么把城市山洪整合进 Flood Hub 花了更长时间？**

关于河流洪水，我们拥有海量全球数据；而关于城市山洪，数据几乎为零。Flood Hub 用两个 AI 模型预测河流洪水，它们处理一系列公开可用的数据源。水文模型（Hydrologic Model）利用天气和地表条件预测将流经河流的水量，淹没模型（Inundation Model）利用流量数据预测哪些区域会受到影响。世界各地的河流中布设有大量物理水位计（也就是标尺）来长期测量水位，这有助于上述预测。而在城市地区，监测山洪的传感器极为罕见，所以我们没有城市山洪的这类历史数据。

**你们从哪里找到城市洪水数据的？**

既然没有权威的全球城市洪水数据集，我们知道自己必须亲手构建一个。这正是我们想出 Groundsource 的契机。首先，它用 Gemini 阅读了跨越 20 年的 500 多万篇洪水新闻报道，创建了一个庞大而独特的数据集，涵盖 150 多个国家的 260 万个历史洪水事件。随后，我们将这些数据整合进一个现已上线 Flood Hub 的全新城市山洪模型。

**Flood Hub 如何帮助受洪水影响的社区？**

研究人员和援助组织（如 [Give Directly](https://www.givedirectly.org/flood-forecast-ai)）正在使用 Flood Hub 来了解洪水将在哪里发生、谁面临风险。去年，通过使用我们的[洪水预测 API](https://developers.google.com/flood-forecasting)，Give Directly 得以在河水真正上涨之前，把钱送到尼日利亚科吉州（Kogi）——西非受洪水影响最严重的地区之一——的人们手中。他们发现，这笔提前送达的资金帮助家庭撤离、保护财产并重建生活。收入翻了一倍多，粮食不安全状况下降了 90%，93% 的受助者表示对未来洪水有了更充分的准备。

**Flood Hub 和 Groundsource 下一步计划是什么？**

目前支撑 Flood Hub 的模型仅限于预测城市地区的山洪，因为那里的数据质量最好。我们正在研究提高模型质量的方法，并纳入农村地区山洪以及沿海洪水的预测。就我们目前拥有的数据集而言，这相当困难，但我们从未因此却步——这正是我们创建 Groundsource 来填补数据空白的原因。我们也在这方面开展更多研究，探索 Groundsource 方法论能否用于热浪或泥石流等其他灾害。

**研究人员可以在哪里找到这些数据？**

为了更好地保护最需要这些信息的社区，我们[开源](https://research.google/blog/the-next-chapter-in-flood-resilience-open-sourcing-googles-hydrology-framework/)了我们的水文学框架。这使各国国家气象与水文部门（NMHS）和其他气象机构能够将自己的数据与模型整合，生成定制化预报，并将其用于各自的具体需求。我们还公开了 [Groundsource 数据集](https://zenodo.org/records/18647054)和[洪水预测 API](https://developers.google.com/flood-forecasting)，帮助改进未来的洪水研究。归根结底，这一切都是我们目标的一部分：用 AI 帮助准确预测自然灾害，尽可能保护更多人的安全。
