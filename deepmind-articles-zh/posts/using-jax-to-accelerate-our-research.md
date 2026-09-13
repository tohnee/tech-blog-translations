---
title: "使用 JAX 加速我们的研究"
title_en: "Using JAX to accelerate our research"
source: https://deepmind.google/blog/using-jax-to-accelerate-our-research/
site: deepmind
date: 2020-12-04
crawled: 2026-09-13
translated: 2026-09-13
---

# 使用 JAX 加速我们的研究

> 原文：[Using JAX to accelerate our research](https://deepmind.google/blog/using-jax-to-accelerate-our-research/) · Google DeepMind

DeepMind 的工程师们通过构建工具、扩展算法规模，以及创建用于训练和测试人工智能（AI）系统的富有挑战性的虚拟与物理世界，来加速我们的研究。作为这项工作的一部分，我们持续评估新的机器学习库和框架。

最近，我们发现越来越多的项目都可以很好地借助 [JAX](https://github.com/google/jax#jax-autograd-and-xla-) 完成——这是由 [Google Research](https://research.google/) 团队开发的机器学习框架。JAX 与我们的工程理念高度契合，并在过去一年中被我们的研究社区广泛采用。在这里，我们分享使用 JAX 的经验，概述为什么我们发现它对我们的 AI 研究很有用，并介绍我们正在构建的、旨在支持世界各地研究者的生态系统。

![JAX 的标志，由蓝色、绿色和紫色的 3D 方块拼成。](https://lh3.googleusercontent.com/wBCIw9Mu04RHjWEB5A1To_jIHcnjpvyIRxsudBvcOhOfMJvs6KZElN62hlSxLmBdWFnwXdu3iiSFZcZkajS-F5vN89SJ8i55wxoEW6VpZvLEHC0nNR0=w1440)

## 为什么选择 JAX？

JAX 是一个专为高性能数值计算（尤其是机器学习研究）设计的 Python 库。它的数值函数 API 基于 [NumPy](https://www.nature.com/articles/s41586-020-2649-2)——科学计算中广泛使用的一组函数。Python 和 NumPy 都被广泛使用且为大家所熟悉，这使 JAX 简单、灵活且易于采用。

除了 NumPy API 之外，JAX 还包含一个可扩展的、可组合的函数变换系统，为机器学习研究提供支持，包括：

- **微分：** 基于梯度的优化是机器学习的基石。JAX 原生支持对任意数值函数进行前向与反向模式的[自动微分](https://jax.readthedocs.io/en/latest/notebooks/autodiff_cookbook.html)，通过 grad、hessian、jacfwd 和 jacrev 等函数变换实现。
- **向量化：** 在机器学习研究中，我们经常把同一个函数应用于大量数据，例如计算一个批次的损失，或为差分隐私学习[评估逐样本梯度](https://arxiv.org/abs/2010.09063)。JAX 通过 vmap 变换提供自动向量化，简化了这类编程。例如，研究者在实现新算法时无需考虑批处理。JAX 还通过相关的 pmap 变换支持大规模数据并行，能够优雅地分布那些超出单个加速器内存容量的数据。
- **JIT 编译：** [XLA](https://www.tensorflow.org/xla) 用于在 GPU 和 [Cloud TPU](https://cloud.google.com/tpu) 加速器上对 JAX 程序进行即时（JIT）编译与执行。JIT 编译加上 JAX 与 NumPy 一致的 API，使没有高性能计算经验的研究者也能轻松扩展到一个或多个加速器。

我们发现，JAX 使新算法与新架构的快速实验成为可能，如今它已支撑起我们的许多近期论文。想了解更多，欢迎参加 12 月 9 日星期三格林尼治标准时间 19:00 在 [NeurIPS](https://neurips.cc/) 线上会议举行的我们的 JAX 圆桌讨论。

## DeepMind 中的 JAX

支持最先进的 AI 研究，意味着要在快速原型设计与快速迭代，以及以传统上与生产系统相关联的规模部署实验之间取得平衡。这类项目之所以特别有挑战性，在于研究格局演进迅速且难以预测。任何时候，一项新的研究突破都可能——而且经常确实——改变整个团队的轨迹与需求。在这个不断变化的环境中，我们工程团队的一项核心职责，就是确保为一个研究项目所积累的经验与编写的代码，能够在下一个项目中被有效地复用。

一种被证明成功的方法是模块化：我们把每个研究项目中开发的最重要的关键构建块提取为经过充分测试且高效的**组件**。这让研究者能够专注于自己的研究，同时从我们核心库所实现的算法成分的代码复用、缺陷修复与性能改进中获益。我们还发现，确保每个库有清晰定义的范围、保证它们可互操作又相互独立也很重要。**渐进式采用（incremental buy-in）**——即可以自由挑选所需特性而不被锁定在其他特性中——对于为研究者提供最大灵活性、始终支持他们为工作选择合适工具至关重要。

我们在开发 JAX 生态系统时的其他考量包括：尽可能与现有 [TensorFlow](https://www.tensorflow.org/guide) 库（例如 [Sonnet](https://deepmind.com/blog/article/open-sourcing-sonnet) 和 [TRFL](https://deepmind.com/blog/article/trfl)）的设计保持一致。我们还力求构建的组件（在相关时）尽可能贴近其底层数学原理，做到自我描述，最大限度减少「从论文到代码」的思维跳跃。最后，我们选择把这些库[开源](https://github.com/deepmind)，以促进研究成果的共享，并鼓励更广泛的社区探索 JAX 生态系统。


## Haiku

![一段动态展示的代码页面。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62277dc798849b366fe787ef_Haiku.gif)

JAX 可组合函数变换的编程模型，在处理有状态对象（例如带有可训练参数的神经网络）时会比较复杂。Haiku 是一个神经网络库，它让用户既能使用熟悉的面向对象编程模型，又能借助 JAX 纯函数式范式的强大与简洁。

Haiku 被 DeepMind 和 Google 的数百名研究者积极使用，并已在多个外部项目中得到采用（例如 [Coax](https://github.com/microsoft/coax)、[DeepChem](https://github.com/deepchem/jaxchem)、[NumPyro](https://github.com/pyro-ppl/numpyro/blob/master/numpyro/contrib/module.py)）。它构建在 [Sonnet](https://github.com/deepmind/sonnet) 的 API 之上——Sonnet 是我们在 TensorFlow 中基于模块的神经网络编程模型——我们的目标是让从 Sonnet 移植到 Haiku 尽可能简单。

[**在 GitHub 上了解更多**](https://github.com/deepmind/dm-haiku)

## Optax

![一段动态展示的代码页面。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62277de6e5d933b07c0a6039_Optax.gif)

基于梯度的优化是机器学习的基石。Optax 提供了一个梯度变换库，并配有组合算子（例如 chain），可以用区区一行代码实现许多标准优化器（例如 RMSProp 或 Adam）。

Optax 的组合性天然支持在自定义优化器中重新组合相同的基础成分。它还提供了许多用于随机梯度估计与二阶优化的实用工具。

许多 Optax 用户同时采用了 Haiku，但遵循我们渐进式采用的理念，任何把参数表示为 JAX 树结构的库都受支持（例如 [Elegy](https://github.com/poets-ai/elegy)、[Flax](https://github.com/google/flax) 和 [Stax](https://jax.readthedocs.io/en/latest/jax.experimental.stax.html)）。有关这个丰富的 JAX 库生态的更多信息，请见[这里](https://github.com/google/jax#neural-network-libraries)。

[**在 GitHub 上了解更多**](https://github.com/deepmind/optax)

## RLax

![一段动态展示的代码页面。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62277e08098cb3c9c586e2f2_RLax.gif)

我们许多最成功的项目都位于深度学习与强化学习（RL）的交汇处，也被称为[深度强化学习](https://deepmind.com/blog/article/deep-reinforcement-learning)。RLax 是一个为构建 RL 智能体提供有用构建块的库。

RLax 中的组件覆盖了广泛的算法与思想：TD 学习、策略梯度、演员-评论家、MAP、近端策略优化、非线性价值变换、一般价值函数，以及多种探索方法。

虽然提供了一些入门[示例智能体](https://github.com/deepmind/rlax/tree/master/examples)，但 RLax 的定位并不是一个用于构建和部署完整 RL 智能体系统的框架。建立在 RLax 组件之上的全功能智能体框架的一个例子是 [Acme](https://deepmind.com/research/publications/Acme)。

[**在 GitHub 上了解更多**](https://github.com/deepmind/rlax)

## Chex

![一段动态展示的代码页面。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62277e21a0b933fa2006f5cd_Chex.gif)

测试对软件可靠性至关重要，研究代码也不例外。从研究实验中得出科学结论，需要对代码的正确性有信心。Chex 是一组测试工具，库作者用它来验证常见构建块的正确性与稳健性，终端用户则用它检查自己的实验代码。

Chex 提供了各种实用工具，包括感知 JAX 的单元测试、对 JAX 数据类型属性的断言、mock 与 fake，以及多设备测试环境。Chex 贯穿 DeepMind 的整个 JAX 生态系统，也被 [Coax](https://github.com/microsoft/coax) 和 [MineRL](https://github.com/dzorlu/minerl) 等外部项目使用。

[**在 GitHub 上了解更多**](https://github.com/deepmind/chex)

## Jraph

![一段动态展示的代码页面。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62277e3aa0b933afca071647_Jraph.gif)

[图神经网络](https://arxiv.org/abs/1806.01261)（GNN）是一个令人兴奋的研究领域，具有许多有前景的应用。例如，参见我们近期在 Google Maps 上的[交通预测](https://deepmind.com/blog/article/traffic-prediction-with-advanced-graph-neural-networks)工作，以及我们在[物理仿真](https://www.youtube.com/watch?v=2Bw5f4vYL98)方面的工作。Jraph（发音为 "giraffe"）是一个轻量级库，用于支持在 JAX 中使用 GNN。

Jraph 提供了图的标准数据结构、一组处理图的实用工具，以及一个易于分叉和扩展的图神经网络模型「动物园」。其他关键特性包括：能够高效利用硬件加速器的 GraphTuple 批处理、通过填充与掩码支持变长形状图的 JIT 编译，以及定义在输入分区上的损失。与 Optax 和我们的其他库一样，Jraph 对用户选择何种神经网络库不做任何限制。

通过我们丰富的[示例](https://github.com/deepmind/jraph/tree/master/jraph/examples)合集了解该库的使用方法。

[**在 GitHub 上了解更多**](https://github.com/deepmind/jraph)

我们的 JAX 生态系统在不断演进，我们鼓励机器学习研究社区探索[我们的库](https://deepmind.com/research?filters=%7B%22collection%22:%5B%22OpenSource%22%5D%7D)以及 JAX 加速自身研究的潜力。

**引用 DeepMind JAX 生态系统**

如果 DeepMind JAX 生态系统对你的工作有所帮助，请使用[此引用格式](https://github.com/deepmind/jax/blob/main/deepmind2020jax.txt)（托管在 GitHub 上）。
