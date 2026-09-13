---
title: "GraphCast：实现更快、更准确的全球天气预报的 AI 模型"
title_en: "GraphCast: AI model for faster and more accurate global weather forecasting"
source: https://deepmind.google/blog/graphcast-ai-model-for-faster-and-more-accurate-global-weather-forecasting/
site: deepmind
date: 2023-11-14
crawled: 2026-09-13
translated: 2026-09-13
---

# GraphCast：实现更快、更准确的全球天气预报的 AI 模型

> 原文：[GraphCast: AI model for faster and more accurate global weather forecasting](https://deepmind.google/blog/graphcast-ai-model-for-faster-and-more-accurate-global-weather-forecasting/) · Google DeepMind

我们最先进的模型能在不到一分钟内以前所未有的精度提供为期 10 天的天气预报

天气以或大或小的方式影响着我们每个人。它决定了我们早晨的穿着，为我们提供绿色能源，而在最坏的情况下，它还会制造摧毁社区的风暴。在一个极端天气日益增多的世界里，快速而准确的预报从未像今天这样重要。

在[发表于《科学》（Science）杂志的一篇论文](https://www.science.org/stoken/author-tokens/ST-1550/full)中，我们介绍了 GraphCast——一个最先进的 AI 模型，能够以前所未有的精度进行中期天气预报。GraphCast 可以提前最多 10 天预测天气状况，比行业金标准的天气模拟系统——由欧洲中期天气预报中心（ECMWF）生成的高分辨率预报（High Resolution Forecast，HRES）——更准确，也快得多。

GraphCast 还能更早地对极端天气事件发出预警。它可以更精确地预测气旋的未来移动路径（预测时间更远），识别与洪水风险相关的大气河流，并预测极端高温的到来。这种能力有望通过更好的准备来拯救生命。

GraphCast 在 AI 天气预测领域迈出了重要一步，提供了更准确、更高效的预报，并为支撑对我们产业和社会需求至关重要的决策开辟了道路。而且，通过[开源 GraphCast 的模型代码](https://github.com/google-deepmind/graphcast)，我们正在让世界各地的科学家和预报员能够惠及数十亿人的日常生活。GraphCast 已被包括 ECMWF 在内的气象机构采用，ECMWF 正在其网站上运行[我们模型预报的实时实验](https://charts.ecmwf.int/products/graphcast_medium-mslp-wind850)。

![](https://lh3.googleusercontent.com/OWZ3ECzygWSBeHJhs_DT9Lkb2Sr7bQX21ImJimz3DFV172vj73m9j54swniHpHn3aK0QTKhhA19QkIH-7EuABWF3_mroVtOjWPnzebaLWlokJzZNxr8=w1440-h810-n-nu)

GraphCast 在 10 天内滚动预测结果的一部分，展示了 700 百帕（约地表以上 3 公里）处的比湿、地表温度和地表风速。

## 全球天气预报的挑战

天气预测是最古老、最具挑战性的科学事业之一。中期预测对于支持从可再生能源到活动物流等各个领域的关键决策非常重要，但要做到准确且高效却并不容易。

天气预报通常依赖于数值天气预报（Numerical Weather Prediction，NWP），它从精心设计的物理方程出发，再将这些方程转化为在超级计算机上运行的计算机算法。虽然这种传统方法是科学与工程的伟大成就，但设计方程和算法非常耗时，需要深厚的专业知识，还需要昂贵的算力资源才能做出准确的预测。

深度学习提供了另一种思路：用数据而非物理方程来构建天气预报系统。GraphCast 在数十年的历史天气数据上训练，学习控制地球天气如何从现在演化到未来的因果关系模型。

至关重要的是，GraphCast 与传统方法相辅相成：我们使用来自 ECMWF ERA5 数据集的四十年天气再分析数据训练了 GraphCast。这一数据宝库基于卫星图像、雷达和气象站等历史天气观测，并使用传统 NWP 在观测不完整之处「填补空白」，从而重建了丰富的全球历史天气记录。

## GraphCast：一个用于天气预测的 AI 模型

GraphCast 是一个基于机器学习和图神经网络（Graph Neural Networks，GNN）的天气预报系统，后者是一种特别适合处理空间结构化数据的架构。

GraphCast 以 0.25 度经度/纬度（赤道处为 28 公里 x 28 公里）的高分辨率进行预报。这相当于覆盖整个地球表面的一百多万个网格点。在每个网格点上，模型预测五个地球表面变量——包括温度、风速与风向，以及平均海平面气压——以及 37 个高度层中每一层的六个大气变量，包括比湿、风速与风向，以及温度。

虽然 GraphCast 的训练非常耗费算力，但由此得到的预报模型却非常高效。用 GraphCast 做一次 10 天预报，在一台 Google TPU v4 机器上只需不到一分钟。相比之下，使用 HRES 等传统方法做一次 10 天预报，可能需要在拥有数百台机器的超级计算机上进行数小时的计算。

在与金标准确定性系统 HRES 的全面性能评估中，GraphCast 在 1380 个测试变量和预报时效中的 90% 以上给出了更准确的预测（详情请参阅我们的[《科学》论文](https://www.science.org/stoken/author-tokens/ST-1550/full)）。当我们将评估范围限定在对流层——距离地球表面最近、高 6–20 公里、准确预报最为重要的大气区域——时，我们的模型在对未来天气的测试变量上有 99.7% 超过了 HRES。

![三步示意图展示 GraphCast 的工作方式：a) 以堆叠的全球天气图作为输入，b) 预测下一个天气状态，c) 滚动生成一系列未来预报。](https://lh3.googleusercontent.com/Ujm4BZdWGHc7JaTDZntbC4qzyawCJUseZdJHMgmFJRnO3Eu6wj3xd25n0ZiCpJhluo7J1Rm7to3ZVvLTkneLVELXj9q7kuMzPHtFcqOPEeLW-VeY=w1440)

在输入方面，GraphCast 只需要两组数据：6 小时前的天气状态和当前的天气状态。模型随后预测 6 小时后的天气。这一过程可以按 6 小时为增量不断向前滚动，从而提供提前最多 10 天的最先进预报。

## 更好地预警极端天气事件

我们的分析显示，GraphCast 还能比传统预报模型更早识别出严重的天气事件，尽管它并未被专门训练去寻找这些事件。这是 GraphCast 帮助做好准备、拯救生命、减少风暴和极端天气对社区影响的一个典型例子。

通过将一个简单的气旋追踪器直接应用于 GraphCast 预报，我们能够比 HRES 模型更准确地预测气旋移动。今年 9 月，部署在 ECMWF 网站上、公开可用的 GraphCast 模型的实时版本，提前约九天准确预测了飓风李（Hurricane Lee）将在新斯科舍（Nova Scotia）登陆。相比之下，传统预报对于登陆的地点和时间有更大的不确定性，直到提前约六天才锁定新斯科舍。

GraphCast 还能刻画大气河流——大气中将热带以外大部分水汽输送的狭窄区域。大气河流的强度可以表明它带来的是有益的降雨，还是引发洪水的倾盆大雨。GraphCast 预报可以帮助刻画大气河流的特性，从而配合[用于预报洪水的 AI 模型](https://sites.research.google/floodforecasting/?utm_source=&utm_medium=&utm_campaign=&utm_content=)规划应急响应。

最后，在我们不断变暖的世界里，预测极端气温的重要性与日俱增。GraphCast 可以刻画地球上任何指定地点的热度何时将超过历史最高气温。这对于预判热浪尤其有用——这类破坏性、危险的事件正变得越来越常见。

![两张折线图比较 GraphCast（蓝线）与 HRES 模型（黑线）随预报时效（天）变化的预报误差。左图标题为「气旋追踪」，显示 GraphCast 在 5 天预报时效内的中位路径误差（公里）更低。右图标题为「大气河流」，显示 GraphCast 在 10 天预报时效内的均方根误差（kg/m/s）更低。](https://lh3.googleusercontent.com/cIsyDic31c-LYmEWuhfK0UQGYqC63trY-UccLJphHv9sEzxyboyGRNP6HRj7hSUw2Ky97Mf_Gc6PCeJf1M9DpwFaKyEXrzD2xBUEsg_gyVheNI2LLLQ=w1440)

严重事件预测——GraphCast 与 HRES 的对比。

左：气旋追踪性能。随着预测气旋移动的时效增加，GraphCast 保持着高于 HRES 的准确度。

右：大气河流预测。在整个 10 天的预测期内，GraphCast 的预测误差都显著低于 HRES。

## AI 天气预报的未来

GraphCast 现在是世界上最准确的 10 天全球天气预报系统，能够比以往更远地预测极端天气事件。随着天气模式在不断变化的气候中演化，随着更高质量数据的出现，GraphCast 也将不断演进和改进。

为了让 AI 驱动的天气预报更容易获取，我们已经[开源了模型的代码](https://github.com/google-deepmind/graphcast)。ECMWF 已经在[试用 GraphCast 的 10 天预报](https://charts.ecmwf.int/products/graphcast_medium-mslp-wind850)，我们期待看到它为研究者解锁的可能性——从针对特定天气现象定制模型，到针对世界不同地区进行优化。

GraphCast 加入了 Google DeepMind 和 Google Research 的其他最先进天气预测系统之列，包括可提前 90 分钟生成预报的区域性[临近预报模型](https://deepmind.google/discover/blog/nowcasting-the-next-hour-of-rain/)，以及 [MetNet-3](https://blog.research.google/2023/11/metnet-3-state-of-art-neural-weather.html?utm_source=&utm_medium=&utm_campaign=&utm_content=)——一个已在美国和欧洲投入运行、能比任何其他系统更准确地提供 24 小时预报的区域天气预报模型。

开创 AI 在天气预报中的应用将惠及数十亿人的日常生活。但我们更广泛的研究不仅仅关乎预测天气——更关乎理解我们气候的更大格局。通过开发新工具、加速研究，我们希望 AI 能够赋能全球社会，共同应对最严峻的环境挑战。

![](https://lh3.googleusercontent.com/a3uPjh6ngpq8MS7AWnKkn-Kh6BbXrXwrNqUiY6FZDgFR2ODBMr1zvMztdb-3GTnE28sYbyDTVYUeKfrJDlvbjP3taDAHMIG6cAtWgPPR8CenowjfLA=w1440-h810-n-nu)

**进一步了解 GraphCast**

[在《科学》杂志上阅读我们的论文](https://www.science.org/stoken/author-tokens/ST-1550/full)[阅读我们论文的开放获取版本\*](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/graphcast-ai-model-for-faster-and-more-accurate-global-weather-forecasting/Learning_skillful_medium-range_global_weather_forecasting.pdf?utm_source=&utm_medium=&utm_campaign=&utm_content=/)[在 GitHub 上访问 GraphCast](https://github.com/google-deepmind/graphcast)[在 ECMWF 上实时查看 GraphCast](https://charts.ecmwf.int/products/graphcast_medium-mslp-wind850)

我们感谢 ECMWF 的 Matthew Chantry、Peter Dueben 和 Linus Magnusson 提供的帮助与反馈。我们还要感谢 Svetlana Grant 和 Jon Small 提供法律支持。这项工作有赖于以下共同作者的贡献：Remi Lam、Alvaro Sanchez-Gonzalez、Matthew Willson、Peter Wirnsberger、Meire Fortunato、Ferran Alet、Suman Ravuri、Timo Ewalds、Zach Eaton-Rosen、Weihua Hu、Alexander Merose、Stephan Hoyer、George Holland、Oriol Vinyals、Jacklynn Stott、Alexander Pritzel、Shakir Mohamed 和 Peter Battaglia。

\*这是作者版本的工作成果。经 AAAS 许可在此发布，仅供个人使用，不得再分发。正式版本发表于《科学》杂志，doi: 10.1126/science.adi2336。
