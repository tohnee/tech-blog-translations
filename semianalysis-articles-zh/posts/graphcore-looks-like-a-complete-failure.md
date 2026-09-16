---
title: "Graphcore 在机器学习训练性能上看起来是一场彻底的失败"
title_en: "Graphcore Looks Like A Complete Failure In Machine Learning Training Performance"
date: 2021-07-01
source: https://newsletter.semianalysis.com/p/graphcore-looks-like-a-complete-failure
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
translated: 2026-09-15
---

# Graphcore 在机器学习训练性能上看起来是一场彻底的失败

> 原文：[Graphcore Looks Like A Complete Failure In Machine Learning Training Performance](https://newsletter.semianalysis.com/p/graphcore-looks-like-a-complete-failure) · SemiAnalysis

最近，衡量标准模型 AI 性能的行业标准 MLPerf v1.0 [发布了](https://mlcommons.org/en/training-normal-10/)。MLPerf Training 测量的是在图像分类、目标检测、NLP、推荐和强化学习等多种任务中，将机器学习模型训练到标准质量目标所需的时间。来自英伟达（Nvidia）、谷歌（Google）、Graphcore、AMD、英特尔（Intel）、Habana 和华为（Huawei）的处理器，通过多家服务器 OEM 纷纷登场。

英伟达提交的结果覆盖面最广，从 4 GPU 一路到 4096 GPU。谷歌在少数几个提交的基准中也表现得极为强劲。MLPerf 的一个缺点是：许多公司只提交自己擅长的少数模型的成绩，其余的干脆留白。

Graphcore 为闭源组（closed division）拿出了一些耐人寻味的结果。他们测试了 4 种不同的系统配置、2 套不同的软件栈，最终却只提交了……总共 4 项结果。没错，你没听错：每个系统只提交 1 项结果。这相当反常。没有任何其他硬件厂商对每套独立系统只提交 1 项结果。连华为和英特尔/Habana 都为单套系统提交了多项结果。

此外，他们还进一步挑选提交范围：只向 2 个不同模型提交了结果。图像分类网络 ResNet-50 用的是 TensorFlow SDK；自然语言处理网络 BERT 用的是 PopART。这与我们通过业内小道消息听到的 Graphcore 硬件情况吻合：软件栈孱弱，需要非常高水平的程序员进行大量手工调优。

即便经过了这番明显经过精心手工调优的、挑挑拣拣的基准选择，Graphcore 还试图把这宣传成一场胜利。顺便说一句，即使只看他们自己的营销材料，这些结果也实在拿不出手。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/aef5df7e-1faa-4fc8-963d-7abcde8c930c_1024x580.jpeg)

而且从迷你的 ResNet50 放大到稍大一点、但依然很小的 BERT 模型，成绩还进一步恶化。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/27261d44-bf1a-4b20-bbd9-d9cf94afe876_1024x552.jpeg)

Graphcore 制作这些营销图来吹嘘自己的成绩，但这个对比存在一系列问题。

1. 他们用 16 颗由台积电（TSMC）代工的 7nm 823mm^2 IPU，对比英伟达 8 颗同样由台积电代工的 7nm 826mm^2 A100。用两倍的硅片面积来对比，相当不诚实。
2. Graphcore 系统的内存容量小得多。
3. Graphcore 系统更慢。
4. Graphcore 刻意选用了 80GB 版 A100 而非 40GB 版，前者价格要高出 1.5 倍。
5. Graphcore 刻意选用了英伟达的 DGX 系统——它包含调优过的软件库和英伟达的直接支持——而不是 OEM 的现货系统。

如果拿 A100 系统与第三方商业现货的 SuperMicro 系统相比，结果就大不一样了。原本 ResNet 模型上 1.6 倍、BERT 模型上 1.3 倍的性价比（价格/$）优势，变成了 Graphcore 的落败。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/2e9a8b22-3c37-4929-818a-7816e877564e_1024x160.png)

Graphcore 的胜利变成了失败。当我们放大规模、与 64 IPU 系统的成绩相比时，结果看上去更加难堪。Graphcore 的劣势清单如下。

1. 更差的性能和性价比（性能/$）
2. 2 倍的 7nm 硅片面积，意味着性能/mm^2 远为逊色
3. 在扩展到需要大量 AI 硅片的大模型时存在问题
4. 在处理器数量上扩展（scale-up）存在问题
5. 从框架和运行时支持到性能调优与部署，软件支持都远为逊色

Graphcore 团队不乏聪明友善的人，但他们正在被碾压。这家频频见诸媒体、被许多人宠爱的 AI 初创公司，估值看起来严重虚高。他们的 AI ASIC 即便经过手工调优，在 AI 上仍不如英伟达更老的 GPU。即便在功耗上，IPU 服务器也只不过与 8 颗 A100 SXM4 的 HGX 服务器打平。

英伟达在初始性价比、TCO 和软件上都占优，同时其芯片的通用性还远胜对手。英伟达还正在筹备于明年上半年用一款 AI 性能超过 2 倍的 GPU 来接替 A100。Graphcore 连英伟达的现有产品都追不上，更将被其毫不松懈的执行节奏远远甩开。一旦谈到盈利能力，Graphcore 的处境更加难看：卖出 2 倍的硅片、价格却几乎与英伟达持平，这不是一个能赢的公式。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

[分享](https://newsletter.semianalysis.com/p/graphcore-looks-like-a-complete-failure?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[发表评论](https://newsletter.semianalysis.com/p/graphcore-looks-like-a-complete-failure/comments)

*本文最初于 2021 年 7 月 1 日发布于 [SemiAnalysis](https://semianalysis.com/graphcore-looks-like-a-complete-failure-in-machine-learning-training-performance/)。*

*SemiAnalysis 的客户及员工可能持有本文所提及公司的仓位。*
