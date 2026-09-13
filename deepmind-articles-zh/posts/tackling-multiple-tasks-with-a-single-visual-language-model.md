---
title: "用单一视觉语言模型应对多种任务"
title_en: "Tackling multiple tasks with a single visual language model"
source: https://deepmind.google/blog/tackling-multiple-tasks-with-a-single-visual-language-model/
site: deepmind
date: 2022-04-28
crawled: 2026-09-13
translated: 2026-09-13
---

# 用单一视觉语言模型应对多种任务

> 原文：[Tackling multiple tasks with a single visual language model](https://deepmind.google/blog/tackling-multiple-tasks-with-a-single-visual-language-model/) · Google DeepMind

智能的一个关键方面，是在得到简要指示后快速学会执行新任务的能力。例如，一个孩子只在书里看过几张动物的图片，到了动物园就能认出真实的动物，尽管两者之间存在差异。但对一个典型的视觉模型来说，要学习新任务，就必须在专门为该任务标注的数万个样本上训练。如果目标是数出并识别图像中的动物，比如"三只斑马"，人们就得收集数千张图片，并为每张图片标注数量和物种。这个过程低效、昂贵且资源密集：既需要大量标注数据，又要在每次面对新任务时训练一个新模型。作为 DeepMind 破解智能难题这一使命的一部分，我们探索了另一种可能性：一个只需极少量任务特定信息的模型，能否让这个过程变得更简单、更高效？

今天，在[论文](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/tackling-multiple-tasks-with-a-single-visual-language-model/flamingo.pdf)预印本中，我们介绍 Flamingo——一个单一视觉语言模型（VLM），它在广泛开放式的多模态任务上刷新了小样本学习（few-shot learning）的最新纪录。这意味着 Flamingo 仅凭少量任务特定样本（"几次尝试"）就能攻克许多难题，而且不需要任何额外训练。Flamingo 简洁的接口使这一切成为可能：它以交错的图像、视频和文本组成的提示词作为输入，然后输出相应的语言。

与大语言模型（LLM）的行为类似——它们可以通过在文本提示词中处理任务示例来解决语言任务——Flamingo 的视觉加文本接口也能引导模型去解决多模态任务。只要在 Flamingo 的提示词里给出几组视觉输入与期望文本回应的示例对，模型就能针对一张新图像或一段新视频回答问题，并生成答案。

在我们研究的 16 个任务上，Flamingo 在每个任务只给出 4 个示例的情况下，就超越了以往所有小样本学习方法。在某些情形下，同一个 Flamingo 模型的表现还优于那些针对每个任务单独微调优化、并使用多出几个数量级任务特定数据的方法。这将让非专业人士能够快速、轻松地把精确的视觉语言模型用在手头的新任务上。

![柱状图，展示 Flamingo 在 16 个任务上相对最先进水平（SOTA）的 32-shot 表现，右侧三幅图解说明 HatefulMemes、VizWiz 和 VATEX 任务的输入输出示例。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/626a705661073c5f801de094_Fig_02.svg)

图 2。**左：** Flamingo 在 16 个不同多模态任务上的小样本表现，与各任务专属的最先进水平对比。**右：** 我们 16 个基准中三个任务的期望输入输出示例。

在实践中，Flamingo 通过在其间插入新颖的架构组件，将大语言模型与强大的视觉表示融合在一起——两者各自预先训练并冻结。随后，它仅在来自网络的互补性大规模多模态数据混合上进行训练，不使用任何为机器学习目的标注的数据。按照这一方法，我们从[Chinchilla](https://deepmind.google/blog/an-empirical-analysis-of-compute-optimal-large-language-model-training/)——我们最近推出的算力最优、700 亿参数的语言模型——出发，训练出最终的 Flamingo 模型，一个 800 亿参数的 VLM。训练完成后，Flamingo 可以通过简单的小样本学习直接适配视觉任务，而无需任何额外的任务特定调优。

我们还测试了模型在现有基准之外的定性能力。在这个过程中，我们比较了模型在为涉及性别和肤色相关图像撰写说明文字时的表现，并将模型生成的说明文字送入 Google 的 Perspective API 进行文本毒性评估。虽然初步结果是积极的，但在多模态系统中评估伦理风险的更多研究至关重要。我们敦促人们在考虑将此类系统部署到现实世界之前，认真评估和思考这些问题。

多模态能力对许多重要的 AI 应用不可或缺，例如[帮助视障人士](https://vizwiz.org/tasks-and-datasets/vqa/)应对日常视觉挑战，或[改进网络上仇恨内容的识别](https://ai.facebook.com/blog/hateful-memes-challenge-and-data-set/)。Flamingo 让我们能够即时高效地适配这些示例和其他任务，而不必修改模型。有趣的是，该模型还展示了开箱即用的多模态对话能力，如下所示。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

图 3a - Flamingo 可以开箱即用地进行多模态对话，此处它正在讨论一张由 OpenAI 的 DALL·E 2 生成的、不太可能存在的"汤怪"图像

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

图 3b - 通过并识别著名的斯特鲁普测试（Stroop test）。

Flamingo 是一族高效且有效的通用模型，只需极少的任务特定样本即可应用于图像和视频理解任务。像 Flamingo 这样的模型在以切实方式造福社会方面前景广阔，我们将继续改进它们的灵活性和能力，使其能够安全地部署、惠及所有人。Flamingo 的能力为与习得型视觉语言模型进行丰富交互铺平了道路，这些交互可以带来更好的可解释性和激动人心的新应用，比如帮助人们日常生活的视觉助手——我们对目前的结果感到欣喜。

**注记**

本项目有赖于整个 Flamingo 团队的贡献：Iain Barr、Yana Hasson、Karel Lenc、Arthur Mensch、Katie Millican、Malcolm Reynolds、Roman Ring、Eliza Rutherford、Serkan Cabi、Tengda Han、Zhitao Gong、Sina Samangooei、Marianne Monteiro、Jacob Menick、Sebastian Borgeaud、Andrew Brock、Aida Nematzadeh、Sahand Sharifzadeh、Mikolaj Binkowski、Ricardo Barreira、Oriol Vinyals、Andrew Zisserman 和 Karen Simonyan。我们还要感谢博客文章的贡献者：Aliya Ahmad、Dominic Barlow、Arielle Bier、Matt Botvinick、Jordan Hoffmann、Max Barnett、Gaby Pearl 和 Emma Yousif。
