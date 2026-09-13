---
title: "机器学习让环保人士有了发推的好素材"
title_en: "Machine learning gives environmentalists something to tweet about"
source: https://blog.google/innovation-and-ai/technology/ai/machine-learning-gives-environmentalists-something-tweet-about/
site: google-blog
date: 2017-11-30
crawled: 2026-09-13
translated: 2026-09-13
---

# 机器学习让环保人士有了发推的好素材

> 原文：[Machine learning gives environmentalists something to tweet about](https://blog.google/innovation-and-ai/technology/ai/machine-learning-gives-environmentalists-something-tweet-about/) · Google

***编者注：**[TensorFlow](https://www.tensorflow.org/)，我们的开源机器学习库，正如其名——对所有人开放。企业、非营利组织、研究者和开发者已经用 TensorFlow 做出了一些非常酷的东西，我们正在 Keyword 博客上分享这些故事。下面就是其中之一。*

Victor Anton 在三年间采集了数万条鸟鸣录音。但他没有办法弄清哪段鸟鸣属于哪种鸟。

这些录音采集自新西兰一处名为 “[Zealandia](http://www.visitzealandia.com/Home/gclid/EAIaIQobChMI1ui595vv1wIVQh0rCh20cQEdEAAYASAAEgKVhPD_BwE)” 的鸟类保护区周边的 50 个地点，是一项旨在更好地了解 Hihi、Tīeke 和 Kākāriki 等受威胁物种的活动规律与数量规模的行动的一部分。由于研究者缺乏关于这些鸟类身在何处、如何活动的可靠信息，很难就实地保育工作的投入方向作出正确决策。

濒危物种包括 Kākāriki、Hihi 和 Tīekei。

![濒危物种包括 Kākāriki、Hihi 和 Tīekei](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Gx0upGDmPCKtb5LyCXxokXhsCVyC3fZ0.width-1200.format-webp.webp)

这正是录音发挥作用的所在。然而音频数据量之大令人望而生畏。于是 Victor——新西兰惠灵顿维多利亚大学的博士生——和他的团队转向了技术。

“我们知道自己有大量极其宝贵的数据锁在这些录音里，但我们既没有足够的人力，也没有可行的方案来解锁它们，”Victor 告诉我们。“所以我们求助于机器学习。”

以下是一些设置在保护区周边 50 个站点的音频录音设备。

![以下是一些设置在保护区周边 50 个站点的音频录音设备](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/MxGu8Nwl3RCHjYCSUg9FYES_eoPdokoR.width-1200.format-webp.webp)

在机器学习较为别致的应用之一中，他们训练了一个基于 Google TensorFlow 的系统来识别特定的鸟鸣并测量鸟类活动。它破译的音频越多，学到的东西就越多，准确度也随之提高。

它的工作原理是这样的：AI 系统读取已录制并存储的音频，将其切分为一分钟的片段，然后把文件转换为声谱图。声谱图再被切成若干小块，每块跨度不足一秒，由一个深度卷积神经网络逐一处理。随后，一个循环神经网络将这些小块串联起来，对整段一分钟音频中三种目标鸟类的在场情况进行连续预测。这些片段汇总起来，便勾勒出鸟类存在与活动的更完整图景。

TensorFlow 处理这些声谱图，并学会了识别不同物种的鸣叫。

![TensorFlow 处理这些声谱图，并学会了识别不同物种的鸣叫](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/GZjTBRFvNrA0m8cfHmzI3N7aaKCeLibd.width-1200.format-webp.webp)

团队面临一些独特的挑战：他们起步时可用的已标注数据很少；软件经常会录进施工、汽车甚至门铃等其他噪音；有些鸟类的鸣叫多种多样，或者两种鸟同时鸣唱。

为了克服这些障碍，他们对系统进行了反复多次的测试、验证和再训练。由此，他们从中获知了一些原本会继续锁在数千小时数据里的信息。虽然还为时尚早，但已经有一些保育团体在与 Victor 商谈如何利用这些初步成果来更有针对性地开展保育工作。此外，团队看到了足够多令人鼓舞的迹象，相信他们的工具可以应用到其他保育项目中。

“对于如何运用机器学习来帮助我们保护不同的动物，我们才刚刚开始了解各种可能性，”Victor 说，“这最终将帮助我们解决世界各地的其他环境挑战。”
