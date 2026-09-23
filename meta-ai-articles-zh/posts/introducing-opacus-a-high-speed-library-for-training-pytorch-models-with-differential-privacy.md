---
title: "推出 Opacus：以差分隐私训练 PyTorch 模型的高速库"
title_en: "Introducing Opacus: A high-speed library for training PyTorch models with differential privacy"
date: 2020-08-31
source: https://ai.facebook.com/blog/introducing-opacus-a-high-speed-library-for-training-pytorch-models-with-differential-privacy
crawled: 2026-09-22
translated: 2026-09-22
---

# 推出 Opacus：以差分隐私训练 PyTorch 模型的高速库

> 原文：[Introducing Opacus: A high-speed library for training PyTorch models with differential privacy](https://ai.facebook.com/blog/introducing-opacus-a-high-speed-library-for-training-pytorch-models-with-differential-privacy) · Meta AI（Wayback 存档）

我们发布 Opacus——一个新的高速库，用于以差分隐私（DP）训练 PyTorch 模型，其可扩展性优于现有最先进方法。差分隐私是一个数学上严格的框架，用于量化敏感数据的匿名化程度。它常用于分析领域，在机器学习（ML）社区中的关注度也在不断上升。借助 Opacus 的发布，我们希望为研究者和工程师在 ML 中采用差分隐私提供一条更平坦的道路，并加速该领域的 DP 研究。

Opacus 提供：

- **速度**：通过利用 PyTorch 的 Autograd 钩子，Opacus 可以计算批处理的逐样本梯度，相比依赖微批处理（microbatching）的现有 DP 库有一个数量级的加速。
- **安全性**：Opacus 在安全关键代码中使用密码学安全的伪随机数生成器，并在 GPU 上对整批参数高速处理。
- **灵活性**：得益于 PyTorch，工程师和研究者可以把我们的代码与 PyTorch 代码及纯 Python 代码混搭，快速验证想法。
- **生产力**：Opacus 附带教程、能在训练开始前就警告不兼容层的辅助函数，以及自动重构机制。
- **交互性**：Opacus 会实时跟踪你在任一时刻消耗了多少隐私预算（DP 的核心数学概念），支持提前停止与实时监控。

Opacus 通过引入 PrivacyEngine 抽象定义了一套轻量 API，它既负责跟踪隐私预算，也负责处理模型梯度。你无需直接调用它——它会附加到标准 PyTorch 优化器上，在幕后工作。用 Opacus 训练就像在训练代码开头加上下面几行一样简单：

```
model = Net()
optimizer = torch.optim.SGD(model.parameters(), lr=0.05)

privacy_engine = PrivacyEngine(
    model,
    batch_size=32,
    sample_size=len(train_loader.dataset),
    alphas=range(2,32),
    noise_multiplier=1.3,
    max_grad_norm=1.0,
)
privacy_engine.attach(optimizer)
# That's it! Now it's business as usual
```

训练结束后，产物就是一个标准 PyTorch 模型——部署隐私模型没有任何额外步骤或障碍：如果你今天能部署模型，那么在用 DP 训练之后同样可以部署，一行代码都不用改。Opacus 库还包含预训练与微调过的模型、面向大规模模型的教程，以及为隐私研究实验设计的基础设施。它已在此开源。

## 用 Opacus 实现高速隐私训练

我们设计 Opacus 的目标是：在保护每条训练样本隐私的同时，把对最终模型准确率的影响降到最低。Opacus 通过修改标准 PyTorch 优化器，在训练过程中实施（并度量）DP。更具体地说，我们的方法以差分隐私随机梯度下降（DP-SGD）为核心。该算法的核心思想是：我们可以通过干预模型用来更新权重的参数梯度（而非直接干预数据）来保护训练数据集的隐私。通过在每次迭代的梯度中加噪声，我们阻止模型记住训练样本，同时仍能让它在整体上学习。（无偏的）噪声在训练过程中的大量批次间会自然趋于相互抵消。不过，加噪声需要精妙平衡：太多会淹没信号，太少则无法保证隐私。为确定合适的尺度，我们考察梯度的范数。限制每个样本对梯度的贡献量很重要，因为离群样本的梯度比大多数样本更大。我们需要保证这些离群样本的隐私，尤其因为它们最容易被模型记住。为此，我们逐个计算一个小批量中每条样本的梯度，对梯度逐条裁剪，再累加回单个梯度张量并对总和加噪声。

这种逐样本计算是构建 Opacus 最大的难关之一。与 PyTorch 的典型操作方式相比，它更具挑战性——Autograd 通常为整个批次计算梯度张量，因为这才符合其他所有 ML 用例的需要，且性能最优。为克服这一点，我们采用了一种高效技术，在训练标准神经网络时获得所有需要的梯度向量：对模型参数，我们单独返回给定批次中每条样本的损失梯度，如下所示：

（此图展示了 Opacus 计算逐样本梯度的工作流程。）通过在运行各层时跟踪一些中间量，我们可以用任何能装进内存的批次大小训练，使我们的方法相比其他库采用的微批方法快一个数量级。

## 隐私保护 ML 的重要性

安全社区一直鼓励安全关键代码的开发者使用少量经过仔细审查、由专业人员维护的库。这条「不要自己造密码学」的原则有助于把攻击面降到最小，让应用开发者专注于他们最擅长的东西：打造优秀的产品。随着 ML 的应用与研究继续加速，ML 研究者需要易于使用的工具来获得数学上严格的隐私保证，同时不拖慢训练过程。我们希望通过开发 Opacus 这样的 PyTorch 工具，让此类隐私保护资源人人可得。我们正以一个更快、更灵活的 PyTorch 平台，弥合安全社区与普通 ML 工程师之间的鸿沟。

## 建设社区

过去几年，隐私保护机器学习（PPML）社区迅速壮大。Opacus 周围正在形成的生态令我们兴奋，其中不乏 PPML 领域的领军者。我们的关键贡献者之一是 OpenMined——一个由数千名开发者组成、以隐私为出发点构建应用的社区。OpenMined 社区已在为 CrypTen 做贡献，并利用许多 PyTorch 基础组件支撑 PySyft 和 PyGrid 的差分隐私与联邦学习。作为合作的一部分，Opacus 将成为 OpenMined 库（如 PySyft）的依赖。我们期待继续合作并进一步壮大社区。

Opacus 是 Facebook AI 更广泛努力的一部分，旨在推动面向机器学习与负责任 AI 的安全计算技术的发展。总体而言，这是推动该领域未来构建「隐私优先」系统的重要垫脚石。为帮助大家更深入理解差分隐私的概念，我们正在开启一系列关于差分隐私机器学习的 Medium 文章，第一篇聚焦关键基础概念，可在 PyTorch Medium 博客阅读。我们还提供全面的教程与 Opacus 开源库。

**作者**

- Davide Testuggine，应用研究科学家
- Ilya Mironov，应用研究科学家
