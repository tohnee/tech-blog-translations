---
title: "扩展社会科学研究"
title_en: "Scaling social science research"
source: https://openai.com/index/scaling-social-science-research/
crawled: 2026-09-13
category: research
translated: 2026-09-13
---

# 扩展社会科学研究

> 原文：[Scaling social science research](https://openai.com/index/scaling-social-science-research/) · OpenAI 博客

我们 OpenAI 工作的核心部分，就是让科学家能够更快地前进、解决更难的问题。今天，我们的经济研究团队（Economic Research Team）正式发布 GABRIEL：一个开源工具包，它利用 GPT 把非结构化的文本和图像转化为定量测量。它专为经济学家、社会科学家和数据科学家设计，用于大规模研究定性数据。

定性数据讲述着关于这个世界最丰富的故事——人们说什么、写什么、教什么、争论什么、经历什么。它涵盖了从课程大纲和访谈，到社交媒体和照片的一切。这类数据数量庞大。但把这类数据转化为严谨的证据极其耗时。很多时候根本不可行。在太多的情况下，社会科学家被迫放弃重要的研究路径——不是因为数据不存在，而是因为它无法被分析。

GABRIEL 的设计初衷就是让定性数据更容易被利用。它允许研究者用日常语言描述自己想要测量什么——比如「这份招聘启事对家庭友好程度如何？」——然后把同一个问题一致地应用到数千（乃至数百万）份文档上，并为每一份返回一个分数。这让研究者可以把更少的时间花在重复性的数据标注上，把更多时间留给真正需要专业判断的工作：选择要测量什么、验证结果、以及得出审慎的结论。

例如，GABRIEL 可以分析一大批科学论文，看看使用了哪些具体方法、这些方法如何随时间演变。它可以查看课程大纲，测量不同学科或技能获得的关注程度。它可以为欧洲的每一个小镇提取结构化的历史细节，也可以检视一大堆顾客评论，发现人们最看重什么。在[我们的论文](https://cdn.openai.com/pdf/7517a586-5bfa-4b87-bd3d-6ea0e9e844c7/GPT-as-a-measurement-tool.pdf)中，我们对 GPT 在众多用例中标注定性数据的表现进行了基准测试，发现它具有很高的准确性。

除了这类测量之外，GABRIEL 还提供了研究者经常需要的实用工具。这些工具包括：即使在列名不匹配的情况下也能合并数据集、智能去重、文本段落编码（passage coding）、构思新的科学理论，以及对文本中的个人信息去标识化以保护隐私。

GABRIEL 现已作为一个[开源 Python 库](https://github.com/openai/GABRIEL)发布，并提供了一个帮助上手的[教程笔记本](https://colab.research.google.com/drive/1RMUeAWACpViqiUMlPMMwPTKyGU-OX756?usp=sharing)。它的设计目标是对技术背景的要求降到最低。我们将根据学术界的反馈持续改进 GABRIEL。我们希望这个工具能帮助更多研究者把定性数据的丰富性和人类故事的厚度带入他们的工作。
