---
title: "GenCast 以最先进的准确度预测天气及极端天气风险"
title_en: "GenCast predicts weather and the risks of extreme conditions with state-of-the-art accuracy"
source: https://deepmind.google/blog/gencast-predicts-weather-and-the-risks-of-extreme-conditions-with-sota-accuracy/
site: deepmind
date: 2024-12-04
crawled: 2026-09-13
translated: 2026-09-13
---

# GenCast 以最先进的准确度预测天气及极端天气风险

> 原文：[GenCast predicts weather and the risks of extreme conditions with state-of-the-art accuracy](https://deepmind.google/blog/gencast-predicts-weather-and-the-risks-of-extreme-conditions-with-sota-accuracy/) · Google DeepMind

新的 AI 模型推进了天气不确定性与风险的预测，可提前 15 天提供更快、更准确的预报

天气影响着我们每一个人——塑造着我们的决策、安全和生活方式。随着气候变化引发更多极端天气事件，准确可信的预报比以往任何时候都更加重要。然而，天气无法被完美预测，预报在几天之后尤其充满不确定性。

由于完美的天气预报并不存在，科学家和气象机构使用概率集合预报，让模型预测一系列可能的天气情景。这样的集合预报比依赖单一预报更有用，因为它为决策者提供了未来几天和几周内可能的天气状况及其各自发生概率的更完整图景。

今天，在[发表于《自然》（Nature）的论文](https://www.nature.com/articles/s41586-024-08252-9)中，我们介绍了 GenCast——我们的新高分辨率（0.25°）AI 集合模型。GenCast 对日常天气和极端事件的预报均优于顶尖业务系统——欧洲中期天气预报中心（[ECMWF](https://www.ecmwf.int/)）的 ENS——可提前 15 天。我们将发布模型的代码、权重和预报结果，以支持更广泛的天气预报社区。

## AI 天气模型的演进

GenCast 标志着基于 AI 的天气预测的关键进展，它建立在我们之前的[天气模型](https://deepmind.google/discover/blog/graphcast-ai-model-for-faster-and-more-accurate-global-weather-forecasting/)之上——后者是确定性的，提供对未来天气的单一最优估计。相比之下，GenCast 的预报包含 50 个或更多预测成员的集合，每个成员代表一种可能的天气轨迹。

GenCast 是一个扩散模型，这类生成式 AI 模型支撑了近期[图像](https://deepmind.google/technologies/imagen-3/)、[视频](https://deepmind.google/technologies/veo/)和[音乐生成](https://deepmind.google/discover/blog/new-generative-ai-tools-open-the-doors-of-music-creation/)领域的快速进步。不过，GenCast 与它们的不同之处在于：它适配地球的球面几何，并学会在给定最近天气状态作为输入时，准确生成未来天气情景的复杂概率分布。

为了训练 GenCast，我们向它提供了来自 ECMWF [ERA5 档案](https://www.ecmwf.int/en/forecasts/dataset/ecmwf-reanalysis-v5)的四十年历史天气数据。这些数据包括不同海拔高度的温度、风速和气压等变量。模型直接从这些处理过的天气数据中学习了 0.25° 分辨率的全球天气模式。

## 为天气预报设立新标准

为了严格评估 GenCast 的性能，我们用它训练至 2018 年的历史天气数据，并在 2019 年的数据上进行测试。GenCast 展现出优于 ECMWF ENS 的预报技巧——后者是许多国家和地区日常决策所依赖的顶尖业务集合预报系统。

我们对两个系统进行了全面测试，考察不同变量在不同预见期上的预报——共计 1,320 种组合。GenCast 在其中 97.2% 的目标上比 ENS 更准确，在预见期超过 36 小时的目标上这一比例达到 99.8%。

![两张图对比 GenCast 与 ENS 在极端高温和大风上的表现，显示 GenCast 在 1 天和 5 天预见期上提供了更高的相对经济价值。](https://lh3.googleusercontent.com/TaPUItEf5BIjjGyyiefLTOh_Imebp0qVuHwngs5K6CSJnBHlXzhj5O4dYB-cXlwZo-vS4-QBiAbftn_8S0P6d9zoUtqvCZZAw3LUQjpF9JgU5TcAeKM=w1440)

对热浪或强风等极端天气更好的预报，使人们能够及时且经济高效地采取预防措施。在广泛的决策场景中，GenCast 在极端天气防备决策方面比 ENS 提供更大的价值。

集合预报通过做出多个代表不同可能情景的预测来表达不确定性。如果大多数预测都显示气旋将袭击同一地区，则不确定性低；但如果它们预测了不同的地点，不确定性就更高。GenCast 恰到好处地把握了这种平衡，既不夸大也不低估其对预报的信心。

在 GenCast 的集合中，只需一块 Google Cloud TPU v5 就能在 8 分钟内生成一个 15 天预报，而且集合中的每个预报都可以同时并行生成。传统的基于物理的集合预报——例如 ENS 生成的 0.2° 或 0.1° 分辨率预报——则需要在拥有数万个处理器的超级计算机上运行数小时。

## 针对极端天气事件的高级预报

对极端天气风险更准确的预报，可以帮助官员守护更多生命、避免损失并节省开支。当我们测试 GenCast 预测极端高温、严寒和高风速的能力时，GenCast 始终优于 ENS。

再看看热带气旋，也就是通常所说的飓风和台风。更早、更精准地获知它们将在何处登陆，价值无可估量。GenCast 对这些致命风暴路径的预测表现卓越。

![GenCast 在台风"海贝思"登陆前 7、5、3、1 天对其路径的预报，显示越接近登陆，预测越集中、越准确。](https://lh3.googleusercontent.com/XRybf2wdWzz9gjGDd7iEK65en5sl_PLkKBIZqCY-2jFzAOlmXQ5njnjLVgV74fGpFFII1OHWpObDFN5s9svoiYx5XSZaRBKIQd-Ow46uwQuNaZ2arA=w1440)

GenCast 的集合预报在提前 7 天时展示了台风"海贝思"广泛的可能路径，但随着这场毁灭性气旋逼近日本海岸，预测路径的散布在几天内收紧为一个高置信度的准确集群。

更好的预报还可能在社会的其他方面发挥关键作用，例如可再生能源规划。例如，风电预测的改进直接提高了风电作为可持续能源的可靠性，并可能加速其采用。在一项分析全球风力发电场组群总发电量预测的概念验证实验中，GenCast 比 ENS 更准确。

## Google 的下一代预报与气候理解

GenCast 是 Google 不断壮大的下一代 AI 天气模型家族的一员，其中包括 Google DeepMind 基于 AI 的[确定性中期预报](https://www.science.org/doi/10.1126/science.adi2336)，以及 Google Research 的 [NeuralGCM](https://research.google/blog/fast-accurate-climate-modeling-with-neuralgcm/)、[SEEDS](https://research.google/blog/generative-ai-to-quantify-uncertainty-in-weather-forecasting/) 和[洪水模型](https://www.nature.com/articles/s41586-024-07145-1)。这些模型已开始为 Google 搜索和地图上的用户体验提供支持，并改进对[降水](https://research.google/blog/metnet-3-a-state-of-the-art-neural-weather-model-available-in-google-products/)、[野火](https://blog.google/outreach-initiatives/sustainability/google-ai-wildfire-detection/)、[洪水](https://research.google/blog/a-flood-forecasting-ai-model-trained-and-evaluated-globally/)和[极端高温](https://blog.google/outreach-initiatives/sustainability/google-ai-research-extreme-heat-resilience/)的预测。

我们非常重视与气象机构的伙伴关系，并将继续与他们合作开发增强其预报能力的 AI 方法。与此同时，传统模型对这项工作仍然不可或缺。一方面，它们为 GenCast 这类模型提供所需的训练数据和初始天气条件。AI 与传统气象学之间的这种合作凸显了相结合的方法在改进预报、更好地服务社会方面的力量。

为了促进更广泛的合作，帮助加速天气和气候社区的研究与开发，我们已将 GenCast 开放为开放模型，并发布了其[代码](https://github.com/google-deepmind/graphcast)和[权重](https://console.cloud.google.com/storage/browser/dm_graphcast)，就像我们之前对确定性中期全球天气预报模型所做的那样。

我们很快将发布 GenCast 及以往模型的实时和历史预报，这将使任何人都能把这些天气输入整合到自己的模型和研究工作流中。

我们渴望与更广泛的天气社区互动，包括学术研究者、气象学家、数据科学家、可再生能源公司，以及专注于粮食安全和灾害响应的组织。这样的伙伴关系能带来深刻洞见和建设性反馈，也提供商业与非商业影响的宝贵机会——所有这些对我们"用模型造福人类"的使命都至关重要。

[阅读我们的论文](https://www.nature.com/articles/s41586-024-08252-9)

**致谢**

我们要感谢 Raia Hadsell 对这项工作的支持。我们感谢 Molly Beck 提供法律支持；Ben Gaiarin、Roz Onions 和 Chris Apps 提供许可支持；Matthew Chantry、Peter Dueben 以及 ECMWF 敬业的团队提供的帮助和反馈；以及《自然》的审稿人认真而富有建设性的反馈。

这项工作凝聚了论文共同作者的心血：Ilan Price、Alvaro Sanchez-Gonzalez、Ferran Alet、Tom Andersson、Andrew El-Kadi、Dominic Masters、Timo Ewalds、Jacklynn Stott、Shakir Mohamed、Peter Battaglia、Remi Lam 和 Matthew Willson。
