---
title: "开源 Sonnet——一个用于构建神经网络的新库"
title_en: "Open sourcing Sonnet - a new library for constructing neural networks"
source: https://deepmind.google/blog/open-sourcing-sonnet-a-new-library-for-constructing-neural-networks/
site: deepmind
date: 2017-04-07
crawled: 2026-09-13
translated: 2026-09-13
---

# 开源 Sonnet——一个用于构建神经网络的新库

> 原文：[Open sourcing Sonnet - a new library for constructing neural networks](https://deepmind.google/blog/open-sourcing-sonnet-a-new-library-for-constructing-neural-networks/) · Google DeepMind

距离 DeepMind [决定让整个研究组织转向使用 TensorFlow（TF）](https://ai.googleblog.com/2016/04/deepmind-moves-to-tensorflow.html)已将近一年。事实证明这是一个好选择——我们的许多模型学习速度显著加快，内置的分布式训练功能也大大简化了我们的代码。在此过程中，我们发现 TF 的灵活性与适应性非常适合为特定用途构建更高层的框架，于是我们编写了一个框架，用于用 TF 快速构建神经网络模块。我们仍在积极开发这个代码库，但目前的成果已经能很好地满足我们的研究需求，我们很高兴地宣布，今天我们将它开源。我们把这个框架称为 [Sonnet](https://github.com/deepmind/sonnet)。

自 2015 年 11 月首次发布以来，围绕 [TensorFlow](https://www.tensorflow.org/) 已涌现出一个多样化的更高层次库的生态系统，让常见任务得以更快完成。Sonnet 与其中一些现有的神经网络库有许多相似之处，但具备一些专门围绕我们研究需求而设计的特性。[Learning to learn 论文](https://arxiv.org/abs/1606.04474)所附带的[代码发布](https://github.com/deepmind/learning-to-learn)中就包含了一个初步版本的 Sonnet，而其他即将发布的代码也将构建在我们今天发布的这个完整库之上。

将 Sonnet 公开，可以让 DeepMind 内部创建的其他模型方便地与社区共享，我们也希望社区能利用 Sonnet 推进自己的研究。近几个月来，我们还开源了旗舰平台 [DeepMind Lab](https://deepmind.google/research/)，并正在与 [Blizzard 合作开发一个支持 StarCraft II 中 AI 研究的开源 API](https://deepmind.com/blog/announcements/deepmind-and-blizzard-release-starcraft-ii-ai-research-environment)。未来还会有更多发布，它们都将共享在我们新的[开源页面](https://deepmind.com/research?filters=%7B%22collection%22:%5B%22OpenSource%22%5D%7D)上。

该库采用面向对象的方法，与 Torch/NN 类似，允许创建一些模块来定义某个计算的前向传播。模块以一些输入 Tensor 被"调用"，这会向计算图中添加操作并返回输出 Tensor。我们的设计选择之一，是确保变量共享被透明地处理——对同一模块的后续调用会自动复用变量。

文献中的许多模型都可以自然地视为一种层级结构——例如，一个可微神经计算机（Differentiable Neural Computer）包含一个控制器，控制器可能是一个 LSTM，而 LSTM 又可以实现为包含一个标准线性层。我们发现，编写显式表示子模块的代码能够带来方便的代码复用与快速的实验迭代——Sonnet 鼓励编写在内部声明其他子模块的模块，或者在构造时传入其他模块。

![Sonnet 标志。](https://lh3.googleusercontent.com/oq_ck82hUcoq8aOt0HqEoPEoMN0jbcIMUY2ifRM8gvJq2GhUjhJLYTpne1xYOcEw0hJXRn6I73mh8KybKVOuWZhrgx3hqhs3cjMvVHTBtd9c8HKfUyk=w1440)

我们发现非常有用的最后一个技术是，允许某些模块在任意嵌套的 Tensor 组合上进行操作。循环神经网络（RNN）的状态往往最适合表示为一组异构 Tensor 的集合，而把它们表示成一个扁平列表容易出错。Sonnet 提供了处理这些任意层级结构的工具，因此把实验改成使用另一种 RNN 时，不需要繁琐的代码修改。我们也对 TF 核心做了修改，以更好地支持这一使用场景。

Sonnet 专为与 TensorFlow 配合而设计，因此它不会阻止你访问诸如 Tensor 和 variable\_scopes 之类的底层细节。用 Sonnet 编写的模型可以与原生 TF 代码自由混用，也可以与其他高层库中的代码混用。

这不是一次性的发布——我们将定期更新 Github 仓库，使之与我们的内部版本保持一致。我们有许多新功能的构想正在推进中，准备就绪后就会发布。我们非常期待社区的贡献。

**注**

在 [Github](http://www.github.com/deepmind/sonnet) 上查看 Sonnet
