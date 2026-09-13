---
title: "用 Backstory 探索网络图像的来龙去脉"
title_en: "Exploring the context of online images with Backstory"
source: https://deepmind.google/blog/exploring-the-context-of-online-images-with-backstory/
site: deepmind
date: 2025-07-21
crawled: 2026-09-13
translated: 2026-09-13
---

# 用 Backstory 探索网络图像的来龙去脉

> 原文：[Exploring the context of online images with Backstory](https://deepmind.google/blog/exploring-the-context-of-online-images-with-backstory/) · Google DeepMind

新的实验性 AI 工具帮助人们探索网上所见图像的背景脉络与来源。

人们在线使用和交互图像的方式在持续演变。去年，我们发表了一篇关于[通过背景脉络与内容溯源判断可信度](https://static.googleusercontent.com/media/publicpolicy.google/en//resources/determining_trustworthiness_en.pdf)的论文，展示了更好的评估工具如何帮助人们对互联网上看到的内容做出明智判断。

作为帮助人们做出明智选择努力的一部分，我们正在开发易用的内容溯源工具和产品内背景信息功能，并投资[信息素养](https://beinternetlegends.withgoogle.com/en_uk)等领域。

今天，我们推出 Backstory——一个实验性人工智能（AI）工具，它可以呈现信息，帮助人们进一步了解网上所见图像的来龙去脉。

在给定一张图片和一段文字提示词后，Backstory 会调查该图片是否为 AI 生成、它此前在何时何地被用于网上、以及它是否经过数字化修改。它能快速为用户提供有帮助的信息，回应进一步的提示词，描述图片是否被使用过、如何被使用，以及它的故事如何随时间演变。Backstory 还会生成易于阅读的调查报告。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![你的浏览器不支持视频标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

## 通过背景脉络与来源评估可信度

Backstory 基于 [Gemini](https://deepmind.google/models/gemini/?_gl=1*v8kbv3*_up*MQ..*_ga*Njc2NDM5MzkxLjE3NTE4ODYzMTk.*_ga_LS8HVHCNQ0*czE3NTE4ODYzMTgkbzEkZzAkdDE3NTE4ODYzMTgkajYwJGwwJGgw) 构建，融合了多种检测技术，用于识别图像是真实拍摄还是由生成式 AI 创作。随后，Backstory 会结合对图像背景脉络更全面的整体评估。它会呈现该图像在互联网上的使用情况以及其他信息（如元数据），帮助回答用户的文字提示词。

在多数情况下，判断一张图片是否为 AI 生成，并不等同于判断它是否可信。例如，一张图片可能不是 AI 生成的，但可能被修改过或在脱离上下文的情况下呈现——从而产生新的、有时具有误导性的信息。

反过来，一张用 AI 生成的图片也可能支撑一个真实、有创意或有事实依据的故事。准确评估一张图片的可信度，往往需要更多关于图片如何产生的知识，以及对它所处背景脉络更深入的理解。

## 采取整体性的方法

业界、民间社会、政府、学术界和用户必须携手合作，共同开发和完善维护信息生态完整性所需的工具与计划。

在我们继续研究并开发 Backstory 的过程中，我们与可信测试者紧密合作，其中包括内容创作者和专业的信息从业者——他们负责管理、组织和传播高质量信息。

今年全年，我们将收集关于案例、用户体验等方面的反馈，以改进我们的技术，使其更有帮助。

**探索 Backstory**

[登记对 Backstory 的兴趣](https://forms.gle/3eGVzNJQRAyc7aPu5)

**致谢**

我们感谢 Zoubin Ghahramani、Helen King、Rahul Sukthankar、Raia Hadsell 和 Chandu Thota 的领导与支持。

这项工作有赖于以下人士的贡献：Mevan Babakar、Hannah Forbes-Pollard、Nikki Hariri、Thomas Leung、Nick Dufour、Ben Usman、Min Ma、Steve Pucci、Spudde Childs、Kate Harrison、Alanna Slocum、Reza Aghajani、Sri Rajendran、Alexey Vorobyov、Ashley Eden、Rishub Jain、Stephanie Chan、Sophie Bridgers、Michiel Bakker、Sures Kumar Thoddu Srinivasan、Tesh Goyal 和 Ashish Chaudhary。

我们还要感谢 Kent Walker、Camino Rojo、Clement Wolf、J.D. Velazquez、Tom Lue、Ndidi Elue、Rachel Stigler、M.H. Tessler、Ricardo Prada、William Isaac、Tom Stepleton、Zoe Darme、Gail Kent、Vincent Ryan、Aaron Donsbach、Abhishek Bapna、Verena Rieser、Christian Plagemann、Anca Dragan、Joelle Barral、Edward Grefenstette、Sara Mahdavi、Sven Gowal、Florian Stimberg、Christopher Savcak、Allison Garcia、Eve Novakovic、Armin Senoner、Arielle Bier，以及 Google DeepMind 和 Google 更大的团队的支持、帮助与反馈。
