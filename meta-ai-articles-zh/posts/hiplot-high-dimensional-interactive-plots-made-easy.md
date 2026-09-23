---
title: "HiPlot：轻松实现高维交互式图表"
title_en: "HiPlot: High-dimensional interactive plots made easy"
date: 2019-03-15
source: https://ai.meta.com/blog/hiplot-high-dimensional-interactive-plots-made-easy
crawled: 2026-09-22
translated: 2026-09-22
---

# HiPlot：轻松实现高维交互式图表

> 原文：[HiPlot: High-dimensional interactive plots made easy](https://ai.meta.com/blog/hiplot-high-dimensional-interactive-plots-made-easy) · Meta AI（Wayback 存档）

**研究内容：**HiPlot 是一个轻量级交互式可视化工具，帮助 AI 研究者发现高维数据中的相关性和模式。它使用平行坐标图及其他图形化方式更清晰地表达信息，并且无需任何配置即可在 Jupyter notebook 中快速运行。HiPlot 让机器学习（ML）研究者能够更轻松地评估超参数的影响，例如学习率、正则化和网络架构。其他领域的研究者也可以使用它，观察并分析与自己工作相关的数据相关性。

平行坐标图是可视化和过滤高维数据的便捷方式。例如，假设你正在运行多个训练任务，每个任务有两个标量参数（命名为 dropout 和 lr）以及一个优化器（取值为「SGD」或「Adam」），并由此得到一个 loss——同样是标量。每个训练任务都可以表示为一个取值为 (dropout, lr, optimizer, loss) 的数据点。HiPlot 会为 dropout、lr、optimizer 和 loss 各画一条带刻度的竖直轴，每个训练/数据点是一条穿过其在各轴上取值的连续折线。图中以红、蓝、黑三色展示了三个不同的数据点。

**工作原理：**HiPlot 的设计使其相比其他可视化工具有若干优势：

**交互性。**HiPlot 中的平行坐标图是可交互的，便于针对不同使用场景调整可视化。例如，你可以只关注在一条或多条轴上落在某个区间或取某个值的实验、根据另一条轴设置配色方案、重排或移除坐标轴，或者导出特定的数据选择。（我们首先选择只显示训练 20 个 epoch 之后得到的数据点，然后通过在「loss」轴上切片，观察到更大的学习率带来了更好的性能（困惑度）。你可以在此复现该示例：https://facebookresearch.github.io/hiplot/_static/demo/ml1.csv.html?hip.color_by=%22valid+ppl%22 。）

**简洁性。**你可以通过两种同样简单的方式使用 HiPlot：

通过 IPython notebook。这会复现上面的第一个示例图：

```python
import hiplot as hip

data = [{'dropout':0.1, 'lr': 0.001, 'loss': 10.0, 'optimizer': 'SGD'},
        {'dropout':0.15, 'lr': 0.01, 'loss': 3.5, 'optimizer': 'Adam'},
        {'dropout':0.3, 'lr': 0.1, 'loss': 4.5, 'optimizer': 'Adam'}]

hip.Experiment.from_iterable(data).display(force_full_width=True)
```

通过 `hiplot` 命令启动服务器。然后你可以通过 http://127.0.0.1:5005/ 访问它，用它来可视化、管理和分享你的实验。简单的语法还允许你同时查看多个实验。

**可扩展性。**默认情况下，HiPlot 的 Web 服务器可以解析 CSV 或 JSON 文件。你也可以提供自定义的 Python 解析器，把你的实验转换为 HiPlot 实验。为帮助研究者进行超参数搜索，HiPlot 已兼容 Facebook AI 开源库的日志，例如 wav2letter@anywhere（我们的在线语音识别推理框架）、Nevergrad（我们的无导数优化开源工具）以及 fairseq（我们的序列建模工具包）。

**面向基于种群的训练（Population-Based Training）的可视化。**当前的超参数调优方法包括基于种群的训练等遗传算法，其中训练任务可能带着不同超参数被多次分叉（fork）。这类实验分析起来颇具挑战，还可能包含难以察觉的 bug。借助 HiPlot，这类实验可以被可视化，因为它的 XY 图可以绘制相关数据点之间的边。

**为什么重要：**ML 模型正变得日益复杂，往往拥有大量超参数。在 Facebook AI，我们一直在用 HiPlot 探索并高效分析深度神经网络的超参数调优——这些网络有数十个超参数、超过 10 万个实验。我们希望这个工具能帮助其他科学家和工程师探索并充分利用自己的实验数据，同时也为更动态的训练方法（例如受遗传算法启发的那些）铺平道路。

在 GitHub 获取：https://github.com/facebookresearch/hiplot （或使用 `pip install hiplot` 安装。）

作者：
- Daniel Haziza，研究工程师
- Jérémy Rapin，研究工程师
- Gabriel Synnaeve，研究科学家
