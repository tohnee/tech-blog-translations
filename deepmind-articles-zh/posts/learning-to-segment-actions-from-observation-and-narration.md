---
title: "从观察与解说中学习动作分割"
title_en: "Learning to Segment Actions from Observation and Narration"
source: https://deepmind.google/blog/learning-to-segment-actions-from-observation-and-narration/
site: deepmind
date: 2020-05-07
crawled: 2026-09-13
translated: 2026-09-13
---

# 从观察与解说中学习动作分割

> 原文：[Learning to Segment Actions from Observation and Narration](https://deepmind.google/blog/learning-to-segment-actions-from-observation-and-narration/) · Google DeepMind

人们在世界中完成的复杂任务，例如做薄煎饼，包含多个动作步骤（例如倒入混合物、翻面、把煎饼取出），并且是有结构的。当我们观察别人执行任务时，我们能识别出动作步骤从哪里开始、到哪里结束（现在正在倒混合物，稍后会翻面），并把重要的步骤与无关紧要的步骤区分开来。识别重要的动作步骤并把它们与时间区间关联起来，被称为动作分割（action segmentation），它是人类认知与规划的一个关键过程。当人们——尤其是儿童——学习分割动作时，他们依赖多种线索，包括执行任务者自己讲述的描述（「现在我要把所有东西搅拌均匀」……）以及任务中的结构规律（搅拌配料通常发生在加入配料之后）。

![三行内容：第一行是制作薄煎饼的文字解说，其下是该过程的视频截图，再下面是相应的动作分段。](https://lh3.googleusercontent.com/4XtdkmxuiWF_cDr3hGNHDqMwCDjD9lYBPwapAlosFoVyZkoKcNZCfBN8IXcP1bJURoZ3AICl-bEDviCgDqTZg8am---JsE_f30BgxjeERo5tz2Gh6Q=w1440)

在这项工作中，我们受到人类学习动作分割方式的启发，考察语言描述和任务规律在改进动作分割系统方面的有效性。动作分割是处理和编目视频的重要第一步：知道正在发生哪些动作、何时发生，可以让从庞大的网络规模视频集合中搜索相关视频及视频片段变得更容易。然而，用于预测视频中动作片段的标准监督式机器学习方法，需要视频带有其中出现的动作片段的标注。由于这些标注的收集成本高昂且困难，我们感兴趣的是弱监督动作分割：在没有动作片段标注的情况下进行训练。

我们聚焦于一个取自 YouTube 的教学视频的富有挑战性的数据集 [CrossTask, Zhukov et al. 2019]，其中涉及烹饪、组装家具等日常家务任务。这些视频虽然是在自然环境中产生的，但其中的任务在各个视频之间具有一定的结构规律，并配有语言描述（讲述者解说的转录文本），二者都提供了带噪声的弱监督来源。我们开发了一个灵活的无监督动作分割模型，它可以在没有动作标签的情况下训练，并可以选择性地利用来自任务规律和语言描述的这种弱监督。我们的模型与过去工作中的模型，都从这两种监督来源中获益颇多，即便是在来自最先进的神经网络动作与物体分类器的丰富特征之上也是如此。我们还发现，视频特征的生成式模型在分割任务上通常比判别式模型表现更好。

我们的发现表明，在无法获得动作片段标注时，利用语言来引导动作分割是未来工作中一个有前景的方向。
