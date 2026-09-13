---
title: "以基于 AI 的海龟面部识别推进自然保护"
title_en: "Advancing conservation with AI-based facial recognition of turtles"
source: https://deepmind.google/blog/advancing-conservation-with-ai-based-facial-recognition-of-turtles/
site: deepmind
date: 2022-08-25
crawled: 2026-09-13
translated: 2026-09-13
---

# 以基于 AI 的海龟面部识别推进自然保护

> 原文：[Advancing conservation with AI-based facial recognition of turtles](https://deepmind.google/blog/advancing-conservation-with-ai-based-facial-recognition-of-turtles/) · Google DeepMind

寻找改进海龟重识别的解决方案，并支持非洲各地的机器学习项目

保护我们周围的生态系统，对于守护地球及其所有生灵的未来至关重要。所幸，新的人工智能（AI）系统正在为世界各地的自然保护工作带来进展，帮助大规模应对复杂问题——从[研究塞伦盖蒂动物群落的行为](https://deepmind.google/blog/using-machine-learning-to-accelerate-ecological-research/)以保护日益萎缩的生态系统，到[发现偷猎者及其伤害的猎物](https://www.newscientist.com/article/2305616-ai-can-spot-wounded-wild-animals-and-poachers-in-camera-trap-footage/)以防止物种灭绝。

作为我们「以所开发的技术造福人类」这一使命的一部分，确保由多元群体来构建未来的 AI 系统非常重要，如此才能实现公平与公正。这包括拓宽机器学习（ML）社区，并与更广泛的受众一起利用 AI 解决重要问题。

通过调研，我们发现了 [Zindi](https://zindi.africa/)——一家目标互补的专注合作伙伴。它是非洲最大的数据科学家社区，主办聚焦于解决非洲最紧迫问题的竞赛。

我们的[科学团队](https://www.deepmind.com/about/science)的多元、公平与包容（DE&I）团队与 Zindi 合作，确定了一个既能推进自然保护工作、又能扩大 AI 参与度的科学挑战。受 Zindi 的[海龟边界框挑战](https://zindi.africa/competitions/local-ocean-conservation-sea-turtle-face-detection)启发，我们敲定了一个具有切实影响潜力的项目：海龟面部识别。

生物学家将海龟视为指示物种。这类生物的行为能帮助科学家理解其生态系统底层健康状况。例如，河流中水獭的存在一直被视为河流洁净、健康的标志——自 20 世纪 70 年代禁止含氯杀虫剂以来，这一物种已从灭绝边缘恢复。

海龟也是这样的物种。它们通过啃食海草覆盖层来培育生态系统，为众多鱼类和甲壳类动物提供栖息地。传统上，生物学家通过物理标牌来识别和追踪每一只海龟，但这些标牌在海水中经常丢失或被侵蚀，使这种方法并不可靠。为帮助解决其中一些难题，我们发起了一项名为 [Turtle Recall](https://zindi.africa/competitions/turtle-recall-conservation-challenge) 的 ML 挑战赛。

![四张从顶部、左侧和右侧角度拍摄的海龟头部示例照片，配有数据集标签：图像文件名、图像位置和海龟 ID。](https://lh3.googleusercontent.com/vbmpvxhQ6o1WgE9C_NPZuHCqZK0JR4iis5lGgCIKiKKSM3hlDH6O17kvQsQbJdSyugDnhmmB2wY5doaUgt7uC9ZmtVNfHtbY3Hye6txoW2jMEz1H=w1440)

来自教程 colab notebook 的四只海龟的图像数据示例。光照、尺度、背景、姿态的差异以及海龟之间的相似性，都增加了这一预测挑战的复杂度。图片来源：Zindi。

考虑到让海龟保持足够静止以便定位其标牌的额外困难，Turtle Recall 挑战赛旨在通过海龟面部识别来绕开这些问题。这是可行的，因为海龟面部的鳞片图案对每个个体而言都是独一无二的，并在其长达数十年的生命周期中保持不变。

该挑战赛旨在提高海龟重识别的可靠性与速度，并有望提供一种彻底取代使用不适感强的物理标牌的方法。要做到这一点，我们需要一个数据集作为基础。所幸，在 Zindi 此前与肯尼亚慈善机构 [Local Ocean Conservation](https://localocean.co/) 合作举办的海龟挑战赛之后，相关团队慷慨地分享了一个带有标注的海龟面部图像数据集。

![一幅三格图，展示 AI 对海龟的面部识别：左格为海龟头部的特写侧面，突出其独特的鳞片图案；中格为机器学习模型检测到的面部特征的模糊热力图；右格将这一热力图叠加在海龟面部之上。](https://lh3.googleusercontent.com/J0hJ-FIr2bGtuj4mqCJwPRKLk3UE7eZtj2EK0M6a3ffyX7UC5jAjSsLKQHKj4IB06qSTC7IbP1iGAbTJa29sn9VNdJ5Z1kV17ls5O5d0TkINSaSwBg=w1440)

神经网络在预测照片中是哪只海龟个体时关注海龟头部哪些区域的可视化。左：数据集中一只海龟的脸。中/右：DenseNet121 和 EfficientNetB5 在同一图像上的激活。图片来源：Zindi 及 Zindi 讨论区用户 ZFTurbo。

比赛于 2021 年 11 月开始，历时五个月。为鼓励参赛者参与，团队提供了一个 [colab notebook](https://research.google.com/colaboratory/)——一种浏览器内编程环境，其中介绍了两种常见的编程工具：[JAX](https://deepmind.google/blog/using-jax-to-accelerate-our-research/) 和 [Haiku](https://en.wikipedia.org/wiki/Haiku_(operating_system)#:~:text=Haiku%20is%20written%20in%20C,provides%20an%20object%2Doriented%20API.)。

参赛者的任务是下载挑战赛数据并训练模型，在给定从特定角度拍摄的照片时，尽可能准确地预测海龟的身份。在向从模型中扣留的数据提交预测之后，他们可以访问一个公开排行榜，追踪每位参赛者的进展。

社区参与度极为积极，各团队在挑战赛期间展现的技术创新同样出色。在比赛过程中，我们收到了来自 13 个非洲国家的多元 AI 爱好者的提交——其中包括在最大的 ML 会议上传统上代表性不足的国家，例如加纳和贝宁。

我们的海龟保护合作伙伴表示，参赛者达到的预测准确度将可立即用于在野外识别海龟，这意味着这些模型能够对野生动物保护产生切实而即时的影响。

作为 Zindi 持续支持气候正向挑战的努力的一部分，他们还在肯尼亚开展[斯瓦希里语音频分类](https://zindi.africa/competitions/swahili-audio-classification)以协助翻译和应急服务，并在乌干达开展[空气质量预测](https://zindi.africa/competitions/layerai-air-quality-prediction-challenge)以改善社会福利。

我们感谢 Zindi 的伙伴合作，感谢所有为 Turtle Recall 挑战赛和日益壮大的保护领域 AI 贡献时间的人。我们期待看到世界各地的人们继续探索各种方式，将 AI 技术用于为地球构建健康、可持续的未来。

在 [Zindi 的博客](https://zindi.medium.com/facial-recognition-for-turtles-how-crowd-sourced-ai-can-help-marine-conservation-efforts-6bc7a69e6712)上进一步了解 Turtle Recall，并在 <https://zindi.africa/> 认识 Zindi。
