---
title: "AI 如何从文本创建照片级真实感图像"
title_en: "How AI creates photorealistic images from text"
source: https://blog.google/innovation-and-ai/technology/research/how-ai-creates-photorealistic-images-from-text/
site: google-blog
date: 2022-06-22
crawled: 2026-09-13
translated: 2026-09-13
---

# AI 如何从文本创建照片级真实感图像

> 原文：[How AI creates photorealistic images from text](https://blog.google/innovation-and-ai/technology/research/how-ai-creates-photorealistic-images-from-text/) · Google

![巢中幼犬从破裂的蛋壳里钻出来的图片。俯瞰飞艇穿梭的蒸汽朋克城市的照片。两个机器人在电影院度过浪漫夜晚的图片。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Final_Hero_Image_Imagen_Parti.width-1200.format-webp.webp)

你见过从破裂的蛋壳里钻出来、卧在巢中的幼犬吗？一张俯瞰飞艇穿梭的蒸汽朋克城市的照片呢？或者两个机器人在电影院度过浪漫夜晚的画面？这些听起来可能有些异想天开，但一种叫做文本到图像生成的新型机器学习技术使之成为可能。这些模型可以根据一段简单的文本提示生成高质量的照片级真实感图像。

在 Google Research 内部，我们的科学家和工程师一直在使用各种 AI 技术探索文本到图像生成。经过大量测试，我们最近发布了两个新的文本到图像模型——[Imagen](https://imagen.research.google/) 和 [Parti](https://parti.research.google/)。两者都能生成照片级真实感图像，但采用了不同的方法。我们想再多分享一点这些模型的工作原理和潜力。

### 文本到图像模型的工作原理

使用文本到图像模型时，人们提供一段文本描述，模型则生成尽可能符合描述的图像。描述可以简单到"一个苹果"或"一只坐在沙发上的猫"，也可以包含更复杂的细节、交互和描述性提示，比如"一只可爱的树懒抱着一个小宝箱。宝箱里透出明亮的金色光芒。"

![一只可爱的树懒抱着一个小宝箱的图片。宝箱里透出明亮的金色光芒](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Sloth_Image.width-1200.format-webp.webp)

在过去几年里，机器学习模型在带有相应文本描述的大型图像数据集上进行训练，产生了更高质量的图像和更广的描述范围。这引发了该领域的重大突破，包括 OpenAI 的 [DALL-E 2](https://openai.com/dall-e-2/)。

### Imagen 和 Parti 的工作原理

Imagen 和 Parti 建立在此前模型的基础上。Transformer 模型能够处理句子中词语之间的相互关系。它们是我们在文本到图像模型中表示文本的基础。两个模型还使用了一种[新技术](https://openreview.net/forum?id=qw8AKxfYbI)，帮助生成与文本描述更贴近的图像。虽然 Imagen 和 Parti 使用相似的技术，但它们采取了不同但互补的策略。

Imagen 是一个扩散模型（Diffusion model），它学习把随机点的图案转换成图像。这些图像起初分辨率较低，然后逐步提高分辨率。最近，扩散模型在[图像](https://iterative-refinement.github.io/palette/)和[音频](https://wavegrad.github.io/)任务中都取得了成功，例如增强图像分辨率、为黑白照片重新上色、编辑图像区域、扩展图像画幅以及语音合成。

Parti 的方法首先把一组图像[转换](https://ai.googleblog.com/2022/05/vector-quantized-image-modeling-with.html)成类似拼图碎片的代码条目序列。然后，给定的文本提示被[翻译](https://ai.googleblog.com/2017/08/transformer-novel-neural-network.html)成这些代码条目，从而创建一张新图像。这种方法利用了 [PaLM](https://ai.googleblog.com/2022/04/pathways-language-model-palm-scaling-to.html) 等大语言模型的现有研究和基础设施，对于处理冗长复杂的文本提示并生成高质量图像至关重要。

这些模型有很多局限。例如，两者都无法可靠地生成特定数量的物体（例如"十个苹果"），也无法根据特定的空间描述正确摆放它们（例如"一个红色球体，位于一个上面放着黄色三角形的蓝色方块左侧"）。此外，当提示变得更复杂时，模型开始失准，要么遗漏细节，要么引入提示中并未提供的细节。这些行为源于若干不足，包括缺乏明确的训练材料、数据表示有限以及缺乏三维感知能力。我们希望通过更广泛的表示和更有效地融入文本到图像生成过程来弥补这些差距。

### 以负责任的态度对待 Imagen 和 Parti

文本到图像模型是激发灵感和创造力的激动人心的工具。它们也带来了与虚假信息、偏见和安全相关的风险。我们正在围绕负责任的 AI 实践以及安全推进这项技术的必要步骤展开讨论。作为初步措施，我们使用易于识别的水印，确保人们始终能够识别由 Imagen 或 Parti 生成的图像。我们还在进行实验，以更好地理解模型的偏见——例如它们如何呈现人和文化——同时探索可能的缓解措施。[Imagen](https://arxiv.org/pdf/2205.11487.pdf) 和 [Parti](https://parti.research.google/paper) 论文对这些问题进行了广泛讨论。

### Google 文本到图像模型的下一步

我们将推进结合两个模型各自优势的新想法，并扩展到相关任务，例如增加通过文本交互式生成和编辑图像的能力。我们还在继续进行深入的比较和评测，以符合我们的[负责任的 AI 原则](https://ai.google/principles/)。我们的目标是以安全、负责任的方式，把基于这些模型的用户体验带给世界，激发创造力。
