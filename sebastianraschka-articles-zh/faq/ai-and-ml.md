---
title: "人工智能与机器学习是什么关系？"
title_en: "How are Artificial Intelligence and Machine Learning related?"
source: https://sebastianraschka.com/faq/docs/ai-and-ml.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 人工智能与机器学习是什么关系？

> 原文：[How are Artificial Intelligence and Machine Learning related?](https://sebastianraschka.com/faq/docs/ai-and-ml.html) · Sebastian Raschka's FAQ

人工智能（Artificial Intelligence，AI）最初是计算机科学的一个分支，其重点是解决那些人类能做到、但计算机做不到的任务（例如图像识别）。实现 AI 的途径有很多，比如编写一个计算机程序来实现一套由领域专家制定的规则。然而，手工打造规则可能非常费力且耗时。

机器学习领域——最初我们可以把它看作 AI 的一个子领域——关注的是开发算法，使计算机能够从数据中自动学习（预测）模型。

举例来说，假设我们想开发一个能从图像中识别手写数字的程序。一种办法是查看所有这些图像，想出一套（嵌套的）「如果……那么……」规则，来判断某张特定图像上显示的是哪个数字（例如通过观察像素的相对位置）。另一种办法是使用机器学习算法，基于我们可能已收集到数据库中的数千张带标注的图像样本来拟合一个预测模型。此外还有深度学习，它又是机器学习的一个子领域，指的是一类特定的模型，它们在某些任务上表现得尤为出色，比如图像识别和自然语言处理。

简而言之，机器学习（以及深度学习）无疑有助于开发「AI」，但 AI 并不一定非要用机器学习来开发——尽管机器学习让「AI」的实现变得方便得多 ;）

tldr；用一张图直观地总结我的观点：

![](https://sebastianraschka.com/images/faq/ai-and-ml/ai-and-ml-1.png)
