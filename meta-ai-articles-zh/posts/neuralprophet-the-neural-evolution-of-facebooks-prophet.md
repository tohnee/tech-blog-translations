---
title: "NeuralProphet：Meta Prophet 的神经进化"
title_en: "NeuralProphet: The neural evolution of Meta's Prophet"
date: 2021-11-30
source: https://ai.facebook.com/blog/neuralprophet-the-neural-evolution-of-facebooks-prophet
crawled: 2026-09-22
translated: 2026-09-22
---

# NeuralProphet：Meta Prophet 的神经进化

> 原文：[NeuralProphet: The neural evolution of Meta's Prophet](https://ai.facebook.com/blog/neuralprophet-the-neural-evolution-of-facebooks-prophet) · Meta AI（Wayback 存档）

**研究内容**：NeuralProphet 基于 Meta 内部数据科学家的实际需求以及外部行业从业者的请求，为用户一些最常见的需求提供了解决方案，目标是最大化时间序列预测的可扩展性与灵活性。随着各行业在决策中使用深度学习日趋成熟，时间序列预测已成为一种主流数据类型。无论是为充足备货而预测产品需求，还是为疾病防控项目预测感染率，不断增长的数据规模都在呼唤新方法。于是，更复杂的深度学习模型日益流行——得益于其非参数性质（当数据不服从正态分布时很有用）以及与复杂数据集相匹配的可扩展性。然而它们的黑箱性质，使得当预测会塑造既需要准确又需要易于解释的业务或运营决策时，用处会打折扣。而 ARIMA（差分整合移动平均自回归）和 ETS（指数平滑状态空间）等统计模型，作为依赖底层数据、假设受限的参数化模型，也缺乏吸纳大规模数据和复杂模式的可扩展性。可解释的经典模型与现代深度学习模型之间的这一鸿沟，在很大程度上仍是一个开放的研究课题。我们的观点是：需要混合模型来弥合两者之间的距离。在 Meta AI，我们带来了一个升级方案：NeuralProphet——一个可扩展、易用的混合预测模型框架，继承了我们 2017 年发布的开源预测库 Facebook Prophet 的衣钵。

NeuralProphet 通过解决 Prophet 的三个关键短板对其进行改进：框架的可扩展性、预测缺少局部上下文，以及预测准确率。

- NeuralProphet 高度可扩展、易用且易于扩展，因为它完全用 PyTorch 构建并用标准深度学习方法训练。
- NeuralProphet 通过支持自回归和滞后协变量引入了局部上下文。
- NeuralProphet 通过混合模型提升预测准确率，其中部分模型组件可配置为神经网络。

**工作原理**：NeuralProphet 以用户友好的 Python 包形式提供，融合经典组件与神经网络，快速产出高精度的时间序列预测。现有的 Prophet 用户会觉得该包在设计上很熟悉。该框架提供自动超参数选择，对初学者来说是一个便捷易用的工具。高级预测从业者则可以通过自定义模块超集、模型权重稀疏化和全局建模能力融入领域知识、发挥更深厚的专长。作为一个模块化框架，NeuralProphet 由可解释、可扩展且可独立配置的组件构成。所有模块都通过小批量随机梯度下降（SGD）联合训练。任何可由 SGD 训练的模型组件都可以作为模块纳入，这使得用未来的最先进预测方法扩展该框架变得容易。NeuralProphet 包含原版 Prophet 模型的全部组件：趋势、季节性、周期性事件和回归量。此外，NeuralProphet 现在还支持自回归和滞后协变量。这在「近期未来取决于系统当前状态」的应用中尤其相关。大多数时间序列预测都展现出这种动态，体现在能耗、交通模式、空气质量指标等场景中。例如，当服务器负载出现强劲上升时，它可能由一个可能持续很长时间的近期事件触发，这应当反映在近期预测中。在下面链接的论文中，我们在合成数据上演示了该框架的可解释分解能力，并与 Prophet 进行对比。此外，我们还在广泛的工业应用上对两个模型进行了基准测试。

**为什么重要**：作为 Meta 内外最受欢迎的预测工具之一，Prophet 设立了行业标准。但它在关键特性上的局限（例如缺少局部上下文）给用户带来了挑战。由于 Prophet 构建在概率编程语言 Stan 之上，扩展原有的预测库并不简单。这就是「扩展 Prophet 的能力」成为用户在 GitHub 上最常请求的功能之一的原因。NeuralProphet 自下而上重塑了 Prophet，用既灵活又易用的 PyTorch 取代 Stan 来应对这些挑战。这让开发者可以轻松地用新功能扩展框架、采纳新研究。举例来说，我们受 AR-Net 启发，让用户能够把自回归和协变量模块无缝配置为经典时间序列组件或深度神经网络。用 NeuralProphet 升级 Prophet，为一线工程师和业务负责人赋能，其洞察可以改进一系列工业应用。例如，NeuralProphet 可以帮助公用事业公司在热浪期间高效满足客户需求。NeuralProphet 为预测从业者提供了一个快速、可解释、精度合理的模型，打包在一个便捷、可扩展、可在任何现代计算机上训练的框架中。

阅读完整论文

我们要感谢斯坦福大学土木与环境工程副教授 Ram Rajagopal、数据科学与人工智能高级讲师 Christoph Bergmeir、Netflix 高级数据科学家 Italo Lima，以及 Meta 研究数据科学家 Caner Komurlu 对 NeuralProphet 的贡献。

作者：Nikolay Laptev，研究科学家；Oskar Triebe，斯坦福大学可持续系统实验室博士生（部分由斯坦福大学与 Total S.A. 的研究协议资助）；Hansika Hewamalage，莫纳什大学博士研究生
