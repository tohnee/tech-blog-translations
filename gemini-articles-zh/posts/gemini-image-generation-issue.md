---
title: "Gemini 的图像生成出了错。我们会做得更好。"
title_en: "Gemini image generation got it wrong. We’ll do better."
source: https://blog.google/products-and-platforms/products/gemini/gemini-image-generation-issue/
site: gemini
date: 2024-02-23
crawled: 2026-09-13
translated: 2026-09-13
---

# Gemini 的图像生成出了错。我们会做得更好。

> 原文：[Gemini image generation got it wrong. We’ll do better.](https://blog.google/products-and-platforms/products/gemini/gemini-image-generation-issue/) · Google

三周前，我们为 [Gemini 对话式应用](https://gemini.google.com/)（前身为 Bard）推出了新的[图像生成](https://blog.google/technology/ai/google-imagen-2/)功能，其中包括创建人物图像的能力。

很明显，这项功能没有达到预期。一些生成的图像不准确，甚至令人反感。我们感谢用户的反馈，并对这项功能表现不佳深表歉意。

我们已经[承认了这一错误](https://twitter.com/Google_Comms/status/1760603321944121506)，并在开发改进版本期间，暂时暂停了 Gemini 中的人物图像生成。

## 发生了什么

Gemini 对话式应用是一个具体的产品，独立于 Search、我们的底层 AI 模型以及其他产品。它的图像生成功能构建在一个名为 [Imagen 2](https://blog.google/technology/ai/google-imagen-2/) 的 AI 模型之上。

当我们在 Gemini 中构建这项功能时，我们对它进行了调校，以确保它不会落入我们过去在图像生成技术中见过的一些陷阱——比如生成暴力或色情图片，或对真实人物的描绘。而且由于我们的用户来自世界各地，我们希望它对每个人都适用。如果你请求一张橄榄球运动员或遛狗者的图片，你可能希望得到各种各样的人。你大概不会希望只收到单一族裔（或任何其他单一特征）的人的图像。

然而，如果你让 Gemini 生成某一特定类型的人的图像——比如"教室里的一位黑人教师"或"带着狗的白人兽医"——或者特定文化或历史背景下的人物，你理应得到一个准确反映你所求的回应。

那么哪里出了问题？简而言之，有两点。第一，我们为让 Gemini 呈现多元化人群所做的调校，没有考虑到那些明显*不应该*呈现多元化人群的情况。第二，随着时间推移，模型变得比我们预期的更加谨慎，甚至完全拒绝回答某些提示词——把一些非常温和的提示词错误地理解为敏感内容。

这两点导致模型在某些情况下矫枉过正，在另一些情况下又过度保守，最终生成了令人尴尬且错误的图像。

## 下一步与教训

这不是我们的本意。我们不想让 Gemini 拒绝创建任何特定群体的图像。我们也不希望它生成不准确的历史图像（或其他任何不准确的图像）。因此，我们关闭了人物图像生成功能，并将努力对它进行大幅改进，然后再重新开启。这一过程将包括大量测试。

有一点需要记住：Gemini 是作为创意和生产力工具构建的，它并不总是可靠的，尤其是在生成关于时事、进展中的新闻或争议性话题的图像或文本时。它会犯错误。正如我们从一开始就说的，幻觉是所有大语言模型（LLM）面临的已知挑战——有些情况下 AI 就是会把事情弄错。这是我们一直在持续改进的地方。

Gemini 会尽力对提示词给出符合事实的回应——我们的核查（double-check）功能也有助于评估网上是否有内容可以证实 Gemini 的回应——但我们建议依赖 Google Search，那里有独立的系统从全网来源中呈现关于这类话题的最新、高质量信息。

我无法保证 Gemini 不会偶尔生成令人尴尬、不准确或令人反感的结果——但我可以保证，只要发现问题，我们就会持续采取行动。AI 是一项新兴技术，它在许多方面都有所助益、潜力巨大，我们正在尽最大努力以安全、负责任的方式推出这项技术。
