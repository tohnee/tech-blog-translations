---
title: "开源 Ax 与 BoTorch：面向自适应实验的新 AI 工具"
title_en: "Open-sourcing Ax and botorch: New AI tools for Adaptive Experimentation"
date: 2019-05-01
source: http://ai.facebook.com/blog/open-sourcing-ax-and-botorch-new-ai-tools-for-adaptive-experimentation
crawled: 2026-09-22
translated: 2026-09-22
---

# 开源 Ax 与 BoTorch：面向自适应实验的新 AI 工具

> 原文：[Open-sourcing Ax and botorch: New AI tools for Adaptive Experimentation](http://ai.facebook.com/blog/open-sourcing-ax-and-botorch-new-ai-tools-for-adaptive-experimentation) · Meta AI（Wayback 存档）

当评估任何一个给定配置都可能需要数小时或数天时，研究人员和工程师该如何探索存在复杂权衡的大型配置空间？这一挑战在许多领域反复出现，包括为机器学习（ML）模型调超参数、通过 A/B 测试寻找最优产品设置，以及设计下一代硬件。今天我们开源两个工具 Ax 和 BoTorch，任何人都可以用它们解决研究和生产中具有挑战性的探索问题——而且不需要海量数据。

Ax 是一个易于上手、通用性强的平台，用于理解、管理、部署和自动化自适应实验。BoTorch 构建在 PyTorch 之上，是一个灵活、现代的贝叶斯优化库——贝叶斯优化是一种数据高效的全局优化概率方法。这些工具已经在 Facebook 大规模部署，属于我们称之为「自适应实验」的持续工作的一部分：在人的引导下，机器学习算法按顺序决定接下来测试哪些配置，以达成一组目标。这些方法的原理是对实验中有限的、可能带噪声的观测数据建模，并采用有原则的探索策略（如强盗优化和贝叶斯优化）来做决策。

在 Facebook，自适应实验被用来解决广泛的问题，包括：

- 提升后端基础设施的效率，如即时编译器、内存分配和数据检索系统。
- 调优排序模型（如 News Feed 和 Instagram 所使用的模型），改善用户体验。
- 优化视频播放、Facebook Live 和媒体上传的算法，提供更高质量、更流畅的视频流。
- 提升调查问卷或产品认知提示的响应率，例如 Facebook 的献血功能。
- 与 Facebook Reality Labs 一起解决光学中的逆问题，用于 AR 和 VR 硬件设计。
- 为 Facebook 的 FBLearner 机器学习平台自动化超参数搜索，以更少的计算资源达到高模型准确率。
- 在模拟和真实环境中学习鲁棒的机器人运动策略。

BoTorch 借助 PyTorch 的特性（包括自动微分、大规模并行和深度学习）推进了贝叶斯优化研究的最先进水平。BoTorch 为研究人员提供了一个可依托的平台，并为攻克复杂优化问题解锁了新的研究方向。Ax 和 BoTorch 利用对数据高效利用的概率模型，能够有意义地量化探索问题空间新区域的成本与收益。在这些场景下，概率模型相比标准深度学习方法（如神经网络）往往有显著优势——后者常常需要大量数据才能做出准确预测，而且无法提供良好的不确定性估计。

我们希望通过降低自适应实验的门槛，Ax 能让开发者和研究人员以有原则、省资源的方式探索更多配置。我们也希望 BoTorch 通过提供一个强大、通用、且与流行深度学习库紧密集成的贝叶斯优化研究平台，成为该领域研究的催化剂。

## 支持从研究到生产的优化

在这篇博文中，我们将详细介绍这两个项目，然后通过一个带代码片段的具体示例，说明使用我们的框架寻找最优配置有多简单。

## BoTorch：面向贝叶斯优化研究的现代库

贝叶斯优化的目标是在有限的实验次数预算内找到系统的最优配置。这类方法采用概率代理模型来预测未观测配置可能产生的结果。为了搜索最优配置，我们定义一个采集函数，它利用代理模型为每个配置赋予一个效用值。效用最高的配置在系统上接受测试，然后过程不断重复。因此，贝叶斯优化算法的性能由三个组件决定：代理模型、采集函数，以及对采集函数进行数值优化的方法。

Facebook 此前已将贝叶斯优化用于简单的超参数优化任务，但我们发现现有工具无法满足日益增长的需求。于是我们开发了新方法，以支持多噪声目标优化、扩展到高度并行的测试环境、利用低保真近似，以及在高维参数空间上优化。尽管当时已有不少贝叶斯优化软件包，它们都难以扩展或定制，而且没有一个能支持应对 Facebook 所遇多样用例所需的全部特性。

为应对这些挑战，我们利用了 PyTorch 的计算能力，并重新思考了模型与优化例程的实现方式。这项工作的成果就是 BoTorch：它为组合贝叶斯优化基本组件（包括概率代理模型、采集函数和优化器）提供了模块化、易扩展的接口。它还支持：

- 通过 PyTorch 实现自动微分、现代硬件（包括 GPU）上的高度并行计算，以及与深度学习模块的无缝集成。
- GPyTorch 中最先进的概率建模，包括多任务高斯过程（GP）、可扩展 GP、深度核学习、深度 GP 和近似推断。
- 基于蒙特卡洛的重参数化技巧实现的采集函数，让新想法的实现直截了当，而无需对底层模型施加限制性假设。

在我们的工作中，BoTorch 显著提升了贝叶斯优化研究的开发效率。它为那些不存在解析解的新方法打开了大门，包括批量采集函数，以及对具有多个相关输出的丰富多任务模型的妥善处理。BoTorch 的模块化设计让研究人员可以替换或重排单个组件，从而定制算法的各个方面， empowered 他们在现代贝叶斯优化方法上开展最先进的研究。

## Ax：可扩展的自适应实验平台

Ax 提供易用的 API 与 BoTorch 交互，同时具备面向生产级服务和可复现研究所需的管理能力。这让开发者可以专注于应用问题，例如探索配置、理解目标之间的权衡。同样，它也让研究人员能把更多时间花在贝叶斯优化的基本构件上。在 Facebook，Ax 已被没有丰富机器学习经验的工程师以及 AI 研究人员广泛应用。

下图展示了 Ax 和 BoTorch 在优化生态中的使用方式。在 Facebook，Ax 与我们的主要 A/B 测试和机器学习平台对接，也与模拟器及其他类型的后端系统对接，部署配置和收集结果几乎不需要用户介入。Ax 让开发者既能创建自定义优化应用，也能在 Jupyter notebook 中临时进行优化。新算法可以用 BoTorch 库或其他应用来实现。Ax 提供了一个框架，用于把配置分派到评估配置所用的外部系统，并从其查询数据。

Ax 通过以下核心功能降低了开发者和研究人员做自适应实验的门槛：

- **框架无关的接口**，用于实现新的自适应实验算法。Ax 的优化算法大量使用 BoTorch，但同时也提供通用的 NumPy 和 PyTorch 接口，研究人员和开发者可以接入任何框架实现的方法。
- **可定制、自动化的优化例程**。Ax 根据实验的特征选择合适的优化策略——从贝叶斯优化、强盗优化及其他技术中选择。这些默认例程可以被用户轻松定制，以满足特定应用的需求。
- **系统理解工具**。交互式可视化让用户可以查看代理模型、执行诊断、理解不同结果之间的权衡。
- **人机协同优化**。除了支持多目标和深化系统理解之外，Ax 的底层数据模型让实验者可以在收集新数据的同时安全地演化搜索空间和目标。
- **创建自定义优化服务的能力**。多种 API 允许把 Ax 用作控制部署和数据收集的框架，或用作可通过远程服务调用的轻量库。
- **用于评估新自适应实验算法的基准测试套件**。轻松比较不同算法在测试问题上的优化性能，并保存结果以便复现研究。

为了展示使用 Ax 的体验，下面是一个简单优化循环的示例，用人工 Booth 函数作为评估函数：

```python
from ax import optimize

best_parameters, _, _, _ = optimize(
    parameters=[
        {
            "name": "x1",
            "type": "range",
            "bounds": [-10.0, 10.0],
        },
        {
            "name": "x2",
            "type": "range",
            "bounds": [-10.0, 10.0],
        },
    ],
    evaluation_function=lambda p: (p["x1"] + 2*p["x2"] - 7)**2 + (2*p["x1"] + p["x2"] - 5)**2,
    minimize=True,
)
best_parameters  # returns {'x1': 1.02, 'x2': 2.97}; true min is (1, 3)
```

## 深入一步：在 Ax 中使用 BoTorch 做贝叶斯优化研究

在展示了 BoTorch 和 Ax 能做什么的全景之后，我们将深入介绍如何把一个研究想法从创建带到生产。在许多应用中，人们希望按批（即多组设计点/配置）探索问题空间。例如，用于超参数优化的模拟或 ML 模型训练任务可以在计算资源集群上并行运行。要最优地完成这种批量探索，需要采集函数能评估一组设计点的联合价值。其中一个这样的采集函数是 q-期望改进算法（qEI），出自 Wang 等人的 Parallel Bayesian Global Optimization of Expensive Functions：

qEI 不存在关于后验分布参数的解析表达式。不过，它可以通过重参数化技巧用蒙特卡洛（MC）采样来估计——即利用后验协方差的 Cholesky 分解，把从标准正态分布抽取的样本关联起来：

BoTorch 中基于蒙特卡洛的采集函数示意图。模型给出给定候选集 X 上函数值的后验分布。为计算候选集的总体效用，从后验中抽取拟蒙特卡洛样本，评估每个样本的值，然后对这些值取平均。

在 BoTorch 中实现这一近似非常直截了当：

```python
import torch
from botorch.acquisition.monte_carlo import MCAcquisitionFunction
from botorch.acquisition.sampler import SobolQMCNormalSampler

class qExpectedImprovement(MCAcquisitionFunction):
    def __init__(self, model, best_f, num_samples=500):
        sampler = SobolQMCNormalSampler(num_samples)
        super().__init__(model=model, sampler=sampler)
        self.register_buffer("best_f", torch.as_tensor(best_f))

    def forward(self, X):
        posterior = self.model.posterior(X)   # evaluate posterior at X
        samples = self.sampler(posterior)     # sample from posterior
        delta = (samples - self.best_f).clamp_min(0)   # compute improvement per sample
        delta_max = delta.max(dim=-1)[0]      # compute maximum across the q points
        qei = delta_max.mean(dim=0)           # average across samples
        return qei
```

这里 MCAcquisitionFunction 是 torch.nn.Module 的子类，因此我们只需实现一个 forward 方法。self.sampler() 从 q 个设计点 X 上函数值的（联合）后验分布（由代理模型建模）中抽取 500 次拟蒙特卡洛抽样。期望改进即是 500 个样本中、q 个点上相对迄今最佳观测值（best_f）的最大改进量的样本均值。

如何优化这个量？PyTorch 的 autograd 让梯度计算轻而易举：

```python
qEI = qExpectedImprovement(model, best_f=0.0)
X = torch.rand(5, 10, requires_grad=True)
val = qEI(X)
val.backward()
grad = X.grad
```

这个自动求得的梯度随后可以接入优化器，充分利用这一信息高效找到使完整联合效用最大化的设计点集合。下图展示了单批 q=4 个设计点在优化过程中的轨迹。

单个批次四个设计点的采集函数优化示意图。起点用空心圆表示，最终位置用实心圆表示。可以看到，qEI 通过选择要么后验均值高（左图深绿）、要么不确定性大（右图深蓝）、要么两者兼备的点，来平衡探索与利用的权衡。

新造出的采集函数可以接入 Ax 的优化循环，后者内部将使用拟二阶数值优化算法并结合随机重启启发式，来优化这 q 个设计点的效用：

```python
from ax.modelbridge.factory import get_botorch

def get_qEI(model, best_f):
    return qExpectedImprovement(model, best_f=best_f)

# collect some initial data...

for i in range(num_batches):
    # evaluate all trials that have not yet been evaluated
    data = experiment.eval()
    # set up the model
    model = get_botorch(
        experiment=experiment,
        data=data,
        search_space=experiment.search_space,
        acqf_constructor=get_qEI,
    )
    # generate candidates and schedule a new trial of
    # batch size q=4
    trial = experiment.new_trial(model.gen(4))
```

下图展示了并行评估如何帮助缩短优化问题所需的时间。

qEI 与随机探索的闭环优化性能（q 表示算法的并行度）。

鉴于采集函数是贝叶斯优化的基础组件，研究人员能够轻松地为这些函数的原型开发和测试新变体非常重要。上面的例子展示了在标准 Ax 优化循环中使用自定义 BoTorch 采集函数有多容易。模型和采集函数优化器也可以用类似方式定制。这样，研究人员可以专注于在 BoTorch 中改进底层建模与优化算法，而把搭建、管理、部署和分析交给 Ax。

## Ax 与 BoTorch 自适应实验的未来

随着时间的推移，我们将不断完善软件的 beta 版本、扩充可用算法集合，并提供与流行调度软件的开箱即用集成。我们期待与社区合作，把用户贡献的模块加入 Ax 和 BoTorch，进一步完善平台。我们尤其期待的研究方向包括高维贝叶斯优化和多保真优化。我们也相信，利用感知并行化的新型求解器来改进采集函数的数值优化性能，存在显著机会。我们计划进一步探索这些以及其他新特性。

Ax 和 BoTorch 配合使用可显著加速从研究到生产的进程，我们希望它能激励更广泛的社区发现自适应实验的新用例。Ax 和 BoTorch 现已可用，工程师和研究人员今天就可以开始使用。如果你有兴趣与 Ax 和 BoTorch 团队合作，请与我们联系。

我们要感谢 Facebook 众多研究人员、工程师和数据科学家对 BoTorch 和 Ax 的贡献。BoTorch 的设计旨在与 GPyTorch 无缝协作，它的开发得到了 Uber AI Labs 的 Jake Gardner 以及康奈尔大学的 Geoff Pleiss 和 Andrew Gordon Wilson 的合作支持。

**作者**

- Eytan Bakshy，Facebook 研究经理
- Max Balandat，Facebook 研究科学家
- Kostya Kashin，Facebook 工程经理
