---
title: "先进机器学习帮助 Play 商店用户发现个性化应用"
title_en: "Advanced machine learning helps Play Store users discover personalised apps"
source: https://deepmind.google/blog/advanced-machine-learning-helps-play-store-users-discover-personalised-apps/
site: deepmind
date: 2019-11-18
crawled: 2026-09-13
translated: 2026-09-13
---

# 先进机器学习帮助 Play 商店用户发现个性化应用

> 原文：[Advanced machine learning helps Play Store users discover personalised apps](https://deepmind.google/blog/advanced-machine-learning-helps-play-store-users-discover-personalised-apps/) · Google DeepMind

过去几年里，我们将 DeepMind 的技术应用于 Google 的产品和基础设施，取得了显著的成果，例如降低[数据中心冷却](https://deepmind.com/blog/article/safety-first-ai-autonomous-data-centre-cooling-and-industrial-control)所需的能耗，以及延长 [Android 电池续航](https://deepmind.com/blog/announcements/deepmind-meet-android)。我们期待在未来几个月分享更多相关工作的细节。

## 我们与 Google Play 商店的合作

我们知道，当用户拥有自己喜爱的应用和游戏时，才能把手机的价值发挥到最大，而发现新的心头好也令人兴奋。在与 Google Play 的合作中，[我们负责与 Google 合作事务的团队](https://deepmind.com/about/deepmind-for-google)推动了 Play 商店发现系统的重大改进，帮助为用户带来更个性化、更直观的 Play 商店体验。

每个月，数十亿用户来到 [Google Play 商店](https://play.google.com/store?utm_source=na_Med&utm_medium=hasem&utm_content=Mar0519&utm_campaign=Evergreen&pcampaignid=MKT-DR-na-us-1000189-Med-hasem-py-Evergreen-Mar0519-Text_Search_BKWS-id_100566_%7cEXA%7cONSEM_kwid_43700023142507235&gclid=CMDln_PN0-UCFVRegQodTRECMw)为其移动设备下载应用——Play 商店支撑着世界上最大的推荐系统之一。有些用户是在寻找特定的应用（比如 Snapchat），另一些则是在浏览商店，看看有什么新鲜有趣的东西。Google Play 发现团队致力于通过提供有用的应用推荐，帮助用户发现最相关的应用和游戏。为了提供更丰富、更个性化的体验，应用会根据用户过往的偏好被推荐。然而，这需要细腻的把握——既要理解一个应用是做什么的，也要理解它与特定用户的相关性。例如，对于一位狂热的科幻游戏玩家来说，推荐类似的游戏可能正合心意；但如果用户安装了一款旅行应用，推荐一款翻译应用可能比再推荐五款旅行应用更切合需求。这些用户偏好的收集与使用受 [Google 隐私政策](https://policies.google.com/privacy)约束。

我们开始与 Play 商店合作，帮助开发和改进判定应用与用户相关性的系统。在本文中，我们将介绍为实现这一目标而开发的一些前沿机器学习技术。如今，Google Play 的推荐系统包含三个主要模型：候选生成器（candidate generator）、重排序器（reranker），以及一个用于多目标优化的模型。候选生成器是一个深度检索模型，能够分析超过一百万个应用并检索出最合适的应用。对于每个应用，重排序器（即用户偏好模型）会在多个维度上预测用户的偏好。接下来，这些预测作为多目标优化模型的输入，其解为用户给出最合适的候选应用。

![Google Play 推荐流水线示意图。箭头展示了从「应用语料库」出发，经过三个筛选阶段——「候选生成器」（另有箭头从「其他候选来源」汇入「重排序器」）、「重排序器」和「优化」——最终向显示在智能手机屏幕上的 Google Play 商店界面送达个性化推荐。](https://lh3.googleusercontent.com/hilHRIVoKtSKpHOUXVnvmDGBBM5WbR1IInHRj8VSO065FjddfN-h81zb3ED1UloWv_YQ435GDUYQiZhuxYaJMMZ2P1dOTnWwBZxHNoOgewGm4mWXog=w1440)

## 现实约束下的应用机器学习

为了改进 Google Play 推荐系统学习用户偏好的方式，我们的第一个方案是使用 [LSTM（长短期记忆网络）](https://colah.github.io/posts/2015-08-Understanding-LSTMs/)模型——一种循环神经网络，凭借强大的更新方程和反向传播动力学，它在现实场景中表现出色。LSTM 带来了显著的准确率提升，但也引入了服务延迟，因为 LSTM 在处理长序列时计算开销可能很大。为了解决这个问题，我们将 LSTM 替换为 [Transformer 模型](https://arxiv.org/abs/1706.03762)。Transformer 非常适合序列到序列的预测，并且此前在自然语言处理中已经取得了很强的结果，因为它能够比其他常用模型捕捉更长的词间依赖。Transformer 改进了模型性能，但同时也增加了训练成本。我们的第三个也是最终的方案，是实现一个高效的加性注意力模型，它适用于序列特征的任意组合，同时计算开销很低。

## 候选生成器的去偏

我们的模型（即候选生成器）会根据用户过往在 Play 商店安装的应用，学习用户更可能安装哪些应用。然而，这会引入推荐偏差问题。例如，如果应用 A 在 Play 商店中的曝光次数是应用 B 的 10 倍，它就更可能被用户安装，因而也更可能被我们的模型推荐。于是模型学到的偏差会偏向那些被展示——进而被安装——得更频繁的应用。

为了纠正这种偏差，我们在模型中引入了重要性加权。重要性权重基于每个应用的曝光-安装率与整个 Play 商店曝光-安装率中位数的比值。安装率低于中位数的应用，其重要性权重小于 1。不过，即使是安装频率较低的「小众」应用，只要其安装率高于中位数，也可以拥有较高的重要性权重。通过重要性加权，我们的候选生成器可以根据应用的安装率进行降权或升权，从而缓解推荐偏差问题。

## 重排序器推荐的改进

推荐系统通常会为用户提供一系列候选，并按最优或最相关的选项排在最前面的顺序呈现。但我们如何确保最相关的应用排在列表最顶部，让用户不必翻页数屏，也不会错过最佳选项？许多推荐系统把排序问题当作二分类问题来处理：训练数据被标注为正类或负类，排序器学习仅从这个二元标签预测一个概率。然而，这类「逐点」（pointwise）模型——一次只对单个条目排序——无法捕捉应用之间相对表现的上下文。为了提供更好的用户体验，排序器应该能基于其他候选应用的上下文来预测所展示条目的相对顺序。

我们的解决方案是重排序器模型，它学习同时展示给用户的一对应用之间的相对重要性。我们构建重排序器模型基于一个核心洞见：如果商店向用户展示了两款应用，那么用户选择安装的那一款，相比未安装的那一款，对用户更相关。据此，我们可以为这一对应用分别赋予正标签或负标签，模型尝试最小化排序中的逆序数量，从而改进应用的相对排序。这种「成对」（pairwise）模型在实践中优于逐点模型，因为预测相对顺序比预测类别标签或安装概率更贴近排序的本质。

## 多目标优化

许多推荐系统必须同时为多个目标进行优化，例如相关性、流行度或个人偏好。我们把多目标优化问题表述为一个约束优化问题：总体目标是在次要指标的期望值满足约束条件的前提下，最大化主要指标的期望值。在线服务期间，目标可能随用户需求而变化——例如，之前关注找房应用的用户可能已经找到了新公寓，于是现在对家居装饰应用感兴趣——因此我们朝着动态解的方向努力。

我们没有离线求解然后把一个固定的模型搬到线上，而是在线地、按请求地、基于服务期间各目标的实际取值来求解这个问题。我们把约束定义为相对约束，也就是说，我们希望以百分比而非绝对值来改进次要目标。这样，次要目标的任何变化都不会影响我们的求解器。

我们开发的算法可用于在多个指标之间寻找权衡。通过在权衡曲线上找到合适的点，我们的算法能够以对主要指标的轻微影响为代价，显著提升次要指标。

## 团队协作

我们从这次[合作](https://deepmind.com/about/deepmind-for-google)中得到的一个关键体会是：在现实世界中部署先进的机器学习技术时，我们需要在诸多实际约束之下开展工作。正因为 Play 商店团队与 DeepMind 团队如此紧密地协作并每日沟通，我们才能在算法设计、实现和最终测试的整个过程中充分考虑产品需求和约束，从而打造出更成功的产品。

迄今为止，我们与 Google 的合作已将[冷却 Google 数据中心](https://deepmind.com/blog/article/safety-first-ai-autonomous-data-centre-cooling-and-industrial-control)所需的电力降低了最高 30%，将 Google [风能](https://deepmind.com/blog/article/machine-learning-can-boost-value-wind-energy)的价值提升了约 20%，并创建了端上学习系统来优化 [Android](https://deepmind.com/blog/announcements/deepmind-meet-android) 电池性能。[WaveNet](https://deepmind.com/blog/article/wavenet-launches-google-assistant) 如今已服务于全世界的 Google Assistant 和 Google Cloud Platform 用户，我们与 Waymo 的[研究合作](https://deepmind.com/blog/article/how-evolutionary-selection-can-train-more-capable-self-driving-cars)也帮助改进了其模型的性能以及神经网络训练的效率。

在 Google 规模下工作会带来一系列独特的研究挑战，同时也带来机会，让我们的突破走出实验室，去应对全球性的复杂挑战。如果你有兴趣将前沿研究应用于现实世界的问题，欢迎[在这里](https://deepmind.com/about/deepmind-for-google)进一步了解主导这个项目的团队。

**注释**

合作者：Dj Dvijotham、Amogh Asgekar、Will Zhou、Sanjeev Jagannatha Rao、Xueliang Lu、Carlton Chu、Arun Nair、Timothy Mann、Bruce Chia、Ruiyang Wu、Natarajan Chendrashekar、Tyler Brabham、Amy Miao、Shelly Bensal、Natalie Mackraz、Praveen Srinivasan & Harish Chandran
