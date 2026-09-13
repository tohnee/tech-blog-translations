---
title: "当 DeepMind 遇上 Android"
title_en: "DeepMind, meet Android"
source: https://deepmind.google/blog/deepmind-meet-android/
site: deepmind
date: 2018-05-08
crawled: 2026-09-13
translated: 2026-09-13
---

# 当 DeepMind 遇上 Android

> 原文：[DeepMind, meet Android](https://deepmind.google/blog/deepmind-meet-android/) · Google DeepMind

我们很高兴地宣布，[DeepMind for Google](https://deepmind.com/about/deepmind-for-google) 与全球最受欢迎的移动操作系统 Android 达成了一项新的合作。我们共同打造了两项新功能，将于今年晚些时候向运行 Android P 的设备用户提供：

- 自适应电池（Adaptive Battery）：一套智能电池管理系统，利用机器学习预测你接下来会用到哪些应用，带来更可靠的电池体验。
- 自适应亮度（Adaptive Brightness）：个性化的屏幕亮度体验，其背后的算法能够学习你在不同环境中的亮度偏好。

对我们而言，这是一次激动人心的「第一次」。我们此前与 Google 的合作都建立在超大规模基础设施之上，包括[降低数据中心能耗](https://deepmind.com/blog/article/deepmind-ai-reduces-google-data-centre-cooling-bill-40)、优化 Google Play 推荐以及为 [Google Assistant](https://deepmind.com/blog/article/wavenet-launches-google-assistant) 和全球 [Google Cloud Platform](https://cloud.google.com/text-to-speech/docs/wavenet) 客户带来 WaveNet 语音等项目。

但这一次，我们部署的技术只需运行在一台移动设备的算力之上——这比典型的机器学习应用低了几个数量级。下面介绍它们的工作原理：

## 自适应电池（Adaptive Battery）

Android 的每一次系统版本发布都在努力提升电池续航。这并不奇怪，因为针对智能手机用户的[调查](https://today.yougov.com/topics/technology/articles-reports/2018/02/20/smartphone-users-still-want-longer-battery-life)显示，电池续航是用户最优先关注的问题。

如今，电量被消耗在让应用保持在[后台](https://developer.android.com/about/versions/oreo/background)处于最新状态，以便用户下次打开时内容是新鲜的。但没有人会以相同频率使用手机上的所有应用，因此在许多情况下，这种电量消耗可能并不必要。

为了解决这一问题，我们与 Android 团队合作开发了名为 Adaptive Battery 的功能，它使用深度[卷积神经网络](https://en.wikipedia.org/wiki/Convolutional_neural_network)来预测你未来几小时会使用哪些应用，而哪些应用可能过一段时间才会用到。

Android 会利用这一信息来适应你的使用模式，从而只把电量花在你需要的应用上。初步结果非常可观：在内部测试中，我们看到后台活动显著减少。

## 自适应亮度（Adaptive Brightness）

有时候，阳光明媚的白天屏幕却暗得让人恼火，而半夜伸手看手机时屏幕又亮得刺眼。这是因为系统采取「一刀切」的设置，没有考虑你的个人偏好。于是你不得不手动调整——比如晚上躺在床上看书时把屏幕调暗，早上醒来后又调亮。

为了改善这一体验，我们与 Android 合作，将机器学习引入名为 Adaptive Brightness 的功能。该功能现在会学习你在不同环境光下如何调节亮度滑块，然后按照你的偏好调整屏幕亮度。在内部测试期间，相当比例的 Android P 用户减少了手动亮度调节的次数。

我们很高兴能与出色的 Android 团队合作，在节省电量的同时让人们的生活更加轻松，并期待未来有更多成果。如果你有兴趣参与真实的机器学习挑战——从全球规模的基础设施到端上设备优化——DeepMind for Google 团队[始终在寻找杰出的人才](https://deepmind.com/careers/)！
