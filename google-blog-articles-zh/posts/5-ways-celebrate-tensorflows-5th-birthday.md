---
title: "庆祝 TensorFlow 五岁生日的 5 种方式"
title_en: "5 ways to celebrate TensorFlow's 5th birthday"
source: https://blog.google/innovation-and-ai/technology/ai/5-ways-celebrate-tensorflows-5th-birthday/
site: google-blog
date: 2020-11-13
crawled: 2026-09-13
translated: 2026-09-13
---

# 庆祝 TensorFlow 五岁生日的 5 种方式

> 原文：[5 ways to celebrate TensorFlow's 5th birthday](https://blog.google/innovation-and-ai/technology/ai/5-ways-celebrate-tensorflows-5th-birthday/) · Google

五年前，[我们将 TensorFlow 开源](https://ai.googleblog.com/2015/11/tensorflow-googles-latest-machine.html)——这是我们的机器学习[框架](http://tensorflow.org/)，可用于研究和生产。我们的目标是让最先进的机器学习工具触手可及，让人人都能使用。

从那以后，TensorFlow 已成为世界上最受欢迎的机器学习库，下载量超过 1.6 亿次。看到这么多人使用 TensorFlow，是一种令人难以置信又令人心怀谦卑的体验。我们也感谢 Google 之外的数千位贡献者——他们贡献代码、创建教学内容、在世界各地组织开发者活动，支持着 TensorFlow 和不断壮大的机器学习社区。

为了庆祝 TensorFlow 五周年，我们想介绍几个只需在浏览器中点击一下就能体验的交互式演示，以及一些能帮助你创建自己项目的教程。如果你刚接触 TensorFlow，这些是感受它能做什么的好途径。如果你喜欢所见之物并想深入一些，请看看 [TensorFlow Blog](https://blog.tensorflow.org/)。

### 体验一些由机器学习驱动的交互式演示

TensorFlow 支持多种编程语言和环境。让我们从 JavaScript 开始快速浏览，并试用三个点击即可体验的交互式演示。

[TensorFlow.js](https://blog.tensorflow.org/2018/03/introducing-tensorflowjs-machine-learning-javascript.html) 让你可以完全在浏览器中编写和运行机器学习模型。这对隐私保护应用（数据无需发送到服务器）和交互式机器学习程序都有重要意义。

一个很好的例子是这个[虹膜关键点追踪](https://blog.tensorflow.org/2020/11/iris-landmark-tracking-in-browser-with-MediaPipe-and-TensorFlowJS.html)程序，它可为免手持界面和辅助技术提供支持；你可以在浏览器中[亲自试用这个模型](https://storage.googleapis.com/tfjs-models/demos/face-landmarks-detection/index.html)（请耐心等待——加载可能需要一点时间！）。

![动画 gif：一位女士倾斜头部，软件通过分析她的虹膜来追踪这一动作。](https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/image1_R129cUq.gif)

与眼动追踪类似，你也可以用 TensorFlow.js 来追踪[手部动作](https://blog.tensorflow.org/2019/11/handtrackjs-tracking-hand-interactions.html)。

![动画 gif：一只手在比划数字，追踪软件描绘出这一动作。](https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/image5_TvKma6W.gif)

这两个演示都只需要一个网络摄像头，而且没有任何数据离开你的电脑。

### 训练你自己的模型，无需写代码

你可以使用 [Teachable Machine](https://teachablemachine.withgoogle.com/) 训练自己的模型（无需任何编码）。它是一种在浏览器中创建机器学习模型的快速、有趣且简单的方式。例如，你可以教一个模型识别图像，或识别你用麦克风录制的声音。

![截图展示了可以用 Teachable Machine 完成的三种项目：图像项目、音频项目或姿势项目。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/image2_J19wFcj.width-1200.format-webp.webp)

### 通过教程深入探索

TensorFlow 包含一个功能强大的 Python 库。要开始使用它，这里有一些适合初学者和专家的[教程](https://www.tensorflow.org/tutorials)。这些教程（包含完整的端到端代码）涵盖从机器学习基础到计算机视觉和机器翻译等主题——甚至会教你如何用机器学习生成艺术作品。

[图片](https://www.flickr.com/photos/27614859@N04/11944957684/) CC-BY，作者 Virginia McMillan。

![图片展示了粉色的玫瑰。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/image4_6taiUzH.width-1200.format-webp.webp)

### 把 TensorFlow 带进移动应用

[TensorFlow Lite](https://www.tensorflow.org/lite) 让你可以在移动和小型嵌入式设备上构建由机器学习驱动的应用。印度的一组工科学生使用 TensorFlow Lite 开发了一款 Android 应用，仅用智能手机摄像头就能提供当地[空气质量信息](https://blog.tensorflow.org/2019/02/air-cognizer-predicting-air-quality.html)。

![照片显示一个人在绿树环绕的景观前举起智能手机分析空气质量。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/image6_HLCMkWe.width-1200.format-webp.webp)

你甚至可以做得更小：[TensorFlow Lite Micro](https://www.tensorflow.org/lite/microcontrollers) 让你可以在微控制器（能握在掌心的小型计算机）上运行机器学习模型。

### 理解如何负责任地构建

随着全球数十亿人继续使用以机器学习为核心的产品和服务，以负责任的方式设计和部署这些系统已变得越来越重要。TensorFlow 为[负责任的 AI](https://blog.tensorflow.org/2020/06/responsible-ai-with-tensorflow.html) 提供了大量工具和最佳实践，包括 [What-If Tool](https://pair-code.github.io/what-if-tool/)，它可以测试机器学习模型在假设情境中对不同人的表现。

你还可以做更多。TensorFlow 包含一整套为[生产](http://tensorflow.org/tfx)机器学习系统提供支撑的工具，甚至支持[量子计算](https://www.tensorflow.org/quantum)领域的最新研究。

这仅仅是个开始，我们很期待下一个五年会带来什么。要进一步了解 TensorFlow，请访问 [tensorflow.org](https://tensorflow.org/)，阅读[博客](http://blog.tensorflow.org/)，在[社交媒体](https://twitter.com/tensorflow)上关注我们，或订阅我们的 [YouTube 频道](https://www.youtube.com/tensorflow)。
