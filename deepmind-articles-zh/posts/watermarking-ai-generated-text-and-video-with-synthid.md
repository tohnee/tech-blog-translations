---
title: "用 SynthID 为 AI 生成的文本和视频添加水印"
title_en: "Watermarking AI-generated text and video with SynthID"
source: https://deepmind.google/blog/watermarking-ai-generated-text-and-video-with-synthid/
site: deepmind
date: 2024-05-14
crawled: 2026-09-13
translated: 2026-09-13
---

# 用 SynthID 为 AI 生成的文本和视频添加水印

> 原文：[Watermarking AI-generated text and video with SynthID](https://deepmind.google/blog/watermarking-ai-generated-text-and-video-with-synthid/) · Google DeepMind

我们宣布用于 AI 生成文本和视频的全新水印方法，以及如何将 SynthID 引入 Google 的关键产品

生成式 AI 工具——以及其背后的大语言模型技术——已经激发了公众的想象。从协助工作到激发创造力，这些工具正迅速成为数百万人日常生活中所用产品的一部分。

这些技术可能带来巨大益处，但随着它们日益普及，如果 AI 生成的内容没有得到恰当识别，人们因疏忽或故意造成危害的风险（例如传播错误信息和网络钓鱼）也会增加。正因如此，[我们于去年推出了 SynthID](https://deepmind.google/discover/blog/identifying-ai-generated-images-with-synthid/)——这是我们用于为 AI 生成内容添加水印的全新数字工具包。

今天，我们正在扩展 [SynthID 的能力](https://deepmind.google/blog/in-conversation-with-ai-building-better-language-models/)：为 [Gemini 应用与网页体验](https://gemini.google.com/)中的 AI 生成文本，以及 [Veo](http://deepmind.google/technologies/veo)（我们最强大的生成式视频模型）中的视频添加水印。

文本版 SynthID 的设计目标是与大多数广泛可用的 AI 文本生成模型兼容并支持大规模部署；而视频版 SynthID 则在我们的[图像与音频水印方法](https://deepmind.google/discover/blog/identifying-ai-generated-images-with-synthid/)基础上，将水印覆盖到生成视频的所有帧。这种创新方法嵌入人眼无法察觉的水印，同时不影响文本或视频生成过程的质量、准确性、创造力或速度。

SynthID 并不是识别 AI 生成内容的灵丹妙药，但它是开发更可靠的 AI 识别工具的重要基石，可以帮助数百万人在与 AI 生成内容交互时做出知情决策。今年夏天晚些时候，我们计划开源文本水印版的 SynthID，让开发者能够基于这项技术进行构建，并将其融入自己的模型。

## 文本水印的工作原理

大语言模型在收到诸如「像我五岁那样给我讲讲量子力学」或「你最喜欢什么水果」这样的提示词时，会生成文本序列。LLM 每次预测一个 token，判断哪个 token 最可能紧随其后。

token 是生成模型处理信息的基本单元。在这里，它可以是一个字符、一个词或短语的一部分。每个可能的 token 都会被赋予一个分数，即它成为正确选择的百分比概率。分数更高的 token 更有可能被选用。LLM 不断重复这些步骤，构建出连贯的回答。

SynthID 的设计是将无法察觉的水印直接嵌入文本生成过程。它通过在生成时刻调节 token 被生成的概率，在 token 分布中引入额外信息来实现这一点——这一切都不会损害文本生成的质量、准确性、创造力或速度。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

SynthID 调整大语言模型所生成 token 的概率分数。

模型用词选择所形成的最终分数模式，与调整后的概率分数一起，被视为水印。这一分数模式会与带水印文本和不带水印文本的预期分数模式进行比较，帮助 SynthID 判断某段文本是否由 AI 工具生成，或是否可能来自其他来源。

![一幅插图，展示 SynthID 如何识别带水印的文本。输入提示词要求把一封邮件改得更专业，输出显示生成的邮件草稿。文本中的关键词和短语以深浅不一的蓝色高亮，表示调整后的概率分数。下方一个方框显示「带水印概率：99.9%」。](https://lh3.googleusercontent.com/yxJLDpIUGAOgpiDYfq8LSD-clFhstkQm9Rpg-bh4ATZoss1W8qNgesAOvvqNHX_J8lZfmf6Excs34trsrTsqFhqw9DcBMl_PhbqUH4NJ0UzDt1dUMQ=w1440)

## 这项技术的优势与局限

文本水印 SynthID 在语言模型生成较长、且形式多样的回答时效果最好——例如被要求生成一篇文章、一个剧本，或一封邮件的多个改写版本。

即便经历某些变换，例如截取部分文本、修改个别词语以及轻度改写，它的表现依然良好。然而，当 AI 生成的文本被彻底重写或翻译成其他语言时，其置信度分数可能会大幅降低。

文本水印 SynthID 对事实性提示的回答效果较差，因为在不影响事实准确性的前提下，可调整 token 分布的机会更少。这包括诸如「法国的首都是什么？」这样的提示词，以及预期几乎没有变化或完全没有变化的查询，例如「背诵一首威廉·华兹华斯的诗」。

目前许多可用的 AI 检测工具使用对数据进行标注和分类的算法，即分类器。这些分类器通常只在特定任务上表现良好，因而灵活性较低。当同一个分类器被应用于不同类型的平台和内容时，其表现并不总是可靠或一致的。这可能导致文本被错误标注，进而引发问题，例如文本被错误地识别为 AI 生成。

SynthID 单独使用即有实效，同时也可以与其他 AI 检测方法结合使用，以在更多内容类型和平台上获得更好的覆盖。虽然这项技术并非旨在直接阻止网络攻击者或黑客等有动机的对手造成危害，但它[可以让人更难将 AI 生成的内容用于恶意目的](https://arxiv.org/abs/2306.04634)。

## 视频水印的工作原理

在今年的 I/O 大会上，我们发布了 [Veo](http://deepmind.google/technologies/veo)，我们最强大的生成式视频模型。虽然视频生成技术还没有图像生成技术那样普及，但它们正在快速演进，帮助人们了解一段视频是否由 AI 生成将变得越来越重要。

视频由一帧帧单独的画面（静态图像）组成。因此，我们受图像版 SynthID 工具启发，开发了一种水印技术。该技术将水印直接嵌入每一视频帧的像素中，让人眼无法察觉，但可以被检测用于识别。

让人们知晓自己何时在与 AI 生成的媒体交互，能在帮助防止错误信息传播方面发挥重要作用。从今天起，[VideoFX](https://labs.google/) 上由 Veo 生成的所有视频都将带有 SynthID 水印。

![一幅插图，展示一系列层叠排列、顺序连接的图像帧，内容是一段 AI 生成的黄色玩具潜水艇在水下的视频，象征 SynthID 如何将水印嵌入视频的每一帧。](https://lh3.googleusercontent.com/ylGstUhDHxiJgfvlx_gv2ZaYirtCkfAZa-bgYOW3exnwyOKpBBh0iKTbw9XAfIg8LfWQnWbQo4Heje2LmDQ90u6Ta4sEOBNmOcofYN4Eeuz3jLHrJA=w1440)

视频水印 SynthID 会为生成视频的每一帧添加标记

## 将 SynthID 带入更广泛的 AI 生态

SynthID 的文本水印技术设计为兼容大多数 AI 文本生成模型，并可跨不同内容类型和平台扩展。为帮助防止 AI 生成内容被大规模滥用，我们正致力于将这项技术带入更广泛的 AI 生态。

今年夏天，我们计划通过一篇详细的研究论文发布更多关于文本水印技术的内容，并通过更新后的[负责任生成式 AI 工具包](https://ai.google.dev/responsible)（Responsible Generative AI Toolkit）开源 SynthID 文本水印——该工具包为构建更安全的 AI 应用提供指导和关键工具——让开发者能够基于这项技术进行构建，并将其融入自己的模型。

[与 Gemini 对话](https://gemini.google.com/)[试用 Gemini Advanced](https://gemini.google.com/advanced)[试用 Google Labs FX 套件](https://labs.google/)

**致谢**

SynthID 文本水印项目由 Sumanth Dathathri 和 Pushmeet Kohli 领导，主要研究与工程贡献来自（按字母顺序排列）：Vandana Bachani、Sumedh Ghaisas、Po-Sen Huang、Rob McAdam、Abi See 和 Johannes Welbl。

感谢 Po-Sen Huang 和 Johannes Welbl 帮助启动该项目。感谢 Brad Hekman、Cip Baetu、Nir Shabat、Niccolò Dal Santo、Valentin Anklin 和 Majd Al Merey 在产品集成方面的协作；感谢 Borja Balle、Rudy Bunel、Taylan Cemgil、Sven Gowal、Jamie Hayes、Alex Kaskasoli、Ilia Shumailov、Tatiana Matejovicova 和 Robert Stanforth 提供技术输入与反馈。同时感谢在 Google DeepMind 和 Google 内做出贡献的许多其他同事，包括 Gemini 和 CoreML 的合作伙伴。

SynthID 视频水印项目由 Sven Gowal 和 Pushmeet Kohli 领导，主要贡献来自（按字母顺序排列）：Rudy Bunel、Christina Kouridi、Guillermo Ortiz-Jimenez、Sylvestre-Alvise Rebuffi、Florian Stimberg 和 David Stutz。另谢 Jamie Hayes 以及上文列出的其他同事。

感谢 Nidhi Vyas 和 Zahra Ahmed 推动 SynthID 产品落地。
