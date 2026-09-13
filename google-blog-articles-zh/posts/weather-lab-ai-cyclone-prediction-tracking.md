---
title: "我们如何利用 AI 帮助追踪和预测气旋"
title_en: "How we’re using AI to help track and predict cyclones"
source: https://blog.google/innovation-and-ai/models-and-research/google-deepmind/weather-lab-ai-cyclone-prediction-tracking/
site: google-blog
date: 2025-08-04
crawled: 2026-09-13
translated: 2026-09-13
---

# 我们如何利用 AI 帮助追踪和预测气旋

> 原文：[How we’re using AI to help track and predict cyclones](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/weather-lab-ai-cyclone-prediction-tracking/) · Google

今年 3 月，Google DeepMind 的 Ferran Alet 和 Tom Andersson 到访了位于迈阿密的[国家飓风中心](https://www.nhc.noaa.gov/)（NHC）堡垒般的总部。两人回忆说，让他们印象深刻的是运作室——人们聚集在展示卫星影像、雷达和模拟结果、如万花筒般琳琅满目的屏幕前——以及大楼 10 英寸厚的混凝土墙，其设计足以承受时速高达 130 英里的大风。

即便在[五级风暴](https://www.nhc.noaa.gov/aboutsshws.php)来袭时，NHC 也必须 24/7 全天候运转，发布警报和更新，帮助人们为飓风做好准备并安然度过——飓风在世界其他地区也被称为气旋（cyclone）或台风（typhoon）。Ferran 和 Tom 此行的目的，是向他们首次展示一个新的 AI 驱动的实验性气旋模型，帮助他们更好地完成这项工作。

在会议室里预览这一模型的专家中，有一位顶尖的飓风专家——几年前他曾发表论文，认为气旋路径预测可能已触及极限。"听完我们的演示后，他告诉我们，我们模型的表现有可能带来革命性变化，"Tom 说，"这让我们深感荣幸。"

如今，Google DeepMind 与 Google Research 正让会议室之外的公众首次一睹这个新模型的风采。与在超级计算机上模拟大气复杂物理过程的传统预报模型不同，它能以前所未有的速度对气旋的路径、规模和强度做出预测。我们正向 NHC 分享其预报结果，并推出 [Weather Lab](https://deepmind.google.com/science/weatherlab)——一个承载其实时与历史预测的全新数据与可视化平台。

我们的模型（蓝色所示）准确预测了马达加斯加以南气旋 Honde 和 Garance 的路径，并在气旋 Jude 和 Ivone 于印度洋形成之前近七天就捕捉到了它们的走向。

对风暴移动与强度的预报越及时、越准确，预报员就越能获得发布飓风灾害监视与警报所需的信息——也让身处灾区的人们有足够的时间撤离或加固家园。但气旋带来一个特殊难题：它们既是世界上最具破坏力的天气事件之一，也是最难预测的天气之一。

"就天气而言，数据中微小的差异和变化就可能导致截然不同的未来，"Ferran 说，"而气旋的极端条件使其尤其难以模拟。它们是混沌系统。"

Google DeepMind 与 Google Research 之前曾在利用历史数据预测气旋路径方面展现出一定潜力，相关天气模型包括 [GenCast](https://blog.google/feed/gencast-weather-prediction/)、[GraphCast](https://deepmind.google/discover/blog/graphcast-ai-model-for-faster-and-more-accurate-global-weather-forecasting/) 和 [NeuralGCM](https://research.google/blog/fast-accurate-climate-modeling-with-neuralgcm/)。但它们是为一般天气设计的，训练所用的历史数据分辨率较低，强度预测也不理想，预报员并不完全信任它们。于是，团队开始开发他们的实验性气旋模型，以填补这一空白。

"气旋的风速和涡度既稀疏又强烈，我们不得不改变模型实际的训练方式，"Ferran 说，"我们现在同时在一般天气数据和稀疏的气旋专属数据上训练。为此，我们没有采用分步迭代运行的扩散模型，而是使用了一种新的概率模型——它在预测过程中引入随机扰动，一步完成运算，最终为风暴生成 50 种可能结果的集合。"

根据初步内部评估，这一新的实验性气旋模型在气旋路径和强度两方面都达到了最先进的准确度。它同样擅长预测气旋的规模。

该模型的集合平均预测（加粗蓝线）正确预判了气旋 Alfred 将迅速减弱为热带风暴，并在七天之后于澳大利亚布里斯班附近登陆，同时给出了在昆士兰州沿海某处登陆的高概率。

可信赖的测试者已使用该模型的预报约两个月，他们为团队提供了宝贵反馈——不仅涉及准确度，还包括信息呈现方式的实用性，以及哪些额外功能能对他们的工作有所帮助。

在她自己的 NHC 之行中——她也对那些坚固的墙壁记忆犹新——Google Research 产品经理 Olivia Graham 与一位预报员并肩而坐，向她演示了[这个界面](https://deepmind.google.com/science/weatherlab)。界面上，在全球地图上展示了来自新模型以及其他 Google 天气模型对当前风暴的路径和强度预测，同时还并列展示了预报员目前使用的官方模型，以便对照。

"那位预报员告诉我，虽然这很有帮助，但他们的许多工作是在气旋形成之前、也就是气旋生成（cyclogenesis）阶段，研判各种可能的结果，"Olivia 说，"这直接促成了面向可信赖测试者的『专家模式』的开发：你可以探索潜在的气旋，地图上成组的小圆圈，每一个代表约 2% 的气旋形成概率。这样，一旦气旋形成，你就能看到它可能的路径和强度。"

这种紧密协作至关重要。"我们是在与 NHC 每天都要使用这项技术的人们共同开发它——询问他们哪些数据最重要、他们希望如何使用，"Olivia 说，"身处危险路径上的人们依赖它，我们要确保提供最好、最相关的信息，帮助他们拯救生命。"
