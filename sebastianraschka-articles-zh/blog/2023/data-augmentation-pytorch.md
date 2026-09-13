---
title: "PyTorch 图像数据增强方法"
title_en: "PyTorch Image Augmentation Methods"
source: https://sebastianraschka.com/blog/2023/data-augmentation-pytorch.html
crawled: 2026-09-06
translated: 2026-09-06
---

# PyTorch 图像数据增强方法

> 原文：[PyTorch Image Augmentation Methods](https://sebastianraschka.com/blog/2023/data-augmentation-pytorch.html)

减少过拟合的最佳方法之一是收集更多（高质量的）数据。然而，收集更多数据并不总是可行，或者成本可能非常高昂。与之相关的一种技术是数据增强。

数据增强是指从现有数据生成新的数据记录或特征，从而在不额外收集数据的情况下扩充数据集。它通过创建原始输入数据的变体，让模型更难死记硬背训练样本或特征中的无关信息，从而帮助提升模型的泛化能力。数据增强对图像和文本数据很常见，[对表格数据也存在](https://github.com/firmai/deltapy)。

无论是图像还是文本，数据增强都是减少过拟合的关键工具。**本文比较了 PyTorch 中的四种自动图像增强技术：AutoAugment、RandAugment、AugMix 和 TrivialAugment**。

（为什么选 AutoAugment、RandAugment、AugMix 和 TrivialAugment？[我最近分享过自己使用 AutoAugment 的良好体验](https://twitter.com/rasbt/status/1619354379295010816?s=20&t=4oowlqeYaGjvz41zRMJKiw)。作为后续，读者们的建议让我一头扎进了探索 PyTorch/torchvision 库中其他相关方法的兔子洞。）

## 比较 AutoAugment、RandAugment、AugMix 与 TrivialAugment

如上所述，本文比较了针对图像数据的四种相关数据增强技术。这四种方法都在 PyTorch/torchvision 核心库中实现，因此非常易于采用。

在详细讨论这些方法的工作原理之前，让我们开门见山，并排看看它们的性能表现。我在这次性能对比中使用了一个非常朴素、没有任何花哨组件的 ResNet-18。此外，为了保持简单，我省略了其他减少过拟合的技术。（如果你对各种减少过拟合的方法感到好奇，我在新书 [Machine Learning Q and AI](https://leanpub.com/machine-learning-q-and-ai/) 中讨论了十多种方法。）

### 代码

运行该实验的代码相当简单，如果你想运行、调整或修改这些实验，可以在 GitHub 上的[这里](https://github.com/rasbt/comparing-automatic-augmentation-blog)找到。

为避免杂乱，我只展示和总结主要部分。你可以在 [GitHub 上的这里](https://github.com/rasbt/comparing-automatic-augmentation-blog)找到完整自洽、可直接执行的代码：

```python
import torch, torchvision
from torchvision import transforms
import lightning as L

## Dataset
train_transform = torchvision.transforms.Compose(
    [
        transforms.Resize(32),
        # One of the following:
        #   1) Nothing
        #   2) transforms.AutoAugment()
        #   3) transforms.RandAugment()
        #   4) transforms.AugMix()
        #   5) transforms.TrivialAugmentWide()
        transforms.ToTensor(),
        
    ]
)

valid_and_test_transform = transforms.Compose(
    [
        transforms.Resize(32),
        transforms.ToTensor(),
    ]
)

L.seed_everything(123)
dm = Cifar10DataModule(
    batch_size=256, 
    train_transform=train_transform, 
    valid_and_test_transform=valid_and_test_transform,
    num_workers=4
)

## Model
pytorch_model = torchvision.models.resnet18(weights=None)
pytorch_model.fc = torch.nn.Linear(512, 10)
lightning_model = LightningModel(model=pytorch_model, learning_rate=0.05)

## Training
trainer = L.Trainer(
    max_epochs=1000,
    accelerator="gpu",
    devices=[0],
    logger=CSVLogger(save_dir="logs/"),
    deterministic=True,
)
trainer.fit(model=lightning_model, datamodule=dm)

## Model evaluation
trainer.test(model=lightning_model, datamodule=dm)
```

如上所示，我在全部四种训练场景中使用了相同的超参数（batch size 和学习率）。此外，我把 PyTorch/torchvision 提供的 ResNet-18 模型的最后一层替换成了一个有 10 个输出节点的层（因为 CIFAR-10 只有 10 个类别）。

为了让这篇博客文章简洁聚焦，我不会详细解释代码。不过，如你所知，如果有任何问题，我非常乐意多聊聊代码。如有任何疑问或意见，欢迎通过配套的 [GitHub Discussion 论坛](https://github.com/rasbt/comparing-automatic-augmentation-blog/discussions)与我联系。

### 结果

一图胜千言，让我们来看看下面的结果。

![Data augmentation pytorch augmentation results](https://sebastianraschka.com/images/blog/2023/data-augmentation-pytorch/augmentation-results.webp)

可以看到，与不使用增强相比，AutoAugment 将测试集准确率提升了约 12%，这是一个巨大的提升。作为 AutoAugment 后继者的 RandAugment 又提升了 2 个百分点。而更新、简单得多的 TrivialAugment 则比 RandAugment 又好了大约一个百分点。

AugMix 的表现优于不使用增强，但不如 AutoAugment、RandAugment 或 TrivialAugment。这是符合预期的，因为 AugMix 的设计初衷针对的是分布偏移（而非提升验证集准确率）。

如上图所示，我还加入了 [RandomAffine](https://pytorch.org/vision/main/generated/torchvision.transforms.RandomAffine.html) 作为基线。RandomAffine 对图像施加随机仿射变换，包括随机平移、缩放和剪切。它的表现优于不使用增强，但远远比不上其他增强方法（AutoAugment、RandAugment 和 TrivialAugment）。

请注意，由于验证集准确率曲线的正斜率表明更长时间的训练可能进一步提升预测性能，我还将 AutoAugment、RandAugment、AugMix 和 TrivialAugment 跑了 2000 个 epoch（结果未展示）。然而，2000 个 epoch 后的测试集性能与上述 1000 epoch 的实验相比并没有提升。

### 局限性

这里显而易见需要保留意见的是：我只在单一神经网络架构（ResNet-18）和单一数据集（CIFAR-10）上运行了这些实验。根据你的模型架构、数据集以及是否使用其他减少过拟合的技术，结果可能会有所不同。

### 参考文献

以下是三种不同数据增强方法的参考文献和链接。下一节将对它们进行更详细的讨论和总结。

**AutoAugment**

- 论文：Cubuk, Zoph, Mane, Vasudevan, Le (Apr 2019) *AutoAugment: Learning Augmentation Policies from Data*, <https://arxiv.org/abs/1805.09501>。
- 实现：[torchvision.transforms.AutoAugment](https://pytorch.org/vision/main/generated/torchvision.transforms.AutoAugment.html)

**RandAugment**

- 论文：Cubuk, Zoph, Shlens, Le (Nov 2019). *RandAugment: Practical Automated Data Augmentation With A Reduced Search Space*, <https://arxiv.org/abs/1909.13719>
- 实现：[torchvision.transforms.RandAugment](https://pytorch.org/vision/stable/generated/torchvision.transforms.RandAugment.html)

**AugMix**

- 论文：Hendrycks, Mu, Cubuk, Zoph, Gilmer, Lakshminarayanan (2020). *AugMix: A Simple Data Processing Method to Improve Robustness and Uncertainty*, <https://arxiv.org/abs/1912.02781>
- 实现：[torchvision.transforms.AugMix](https://pytorch.org/vision/main/generated/torchvision.transforms.AugMix.html)

**TrivialAugment**

- 论文：Mueller, Hutter (Aug 2021). *TrivialAugment: Tuning-free Yet State-of-the-Art Data Augmentation*, <https://arxiv.org/abs/2103.10158>。
- 实现：[torchvision.transforms.TrivialAugmentWide](https://pytorch.org/vision/main/generated/torchvision.transforms.TrivialAugmentWide.html)

## 方法总结与比较

本节根据上文引用的文献，简要概述各种自动或学习型图像增强的工作原理，并比较它们的异同。

### AutoAugment

在这篇[论文](https://arxiv.org/abs/1805.09501)中，作者学习图像变换的组合，以在给定数据集上优化验证集准确率。变换"鸡尾酒"的候选包括剪切、平移、旋转、对比度、像素反转、直方图均衡化、太阳化、色调分离、色彩、亮度、锐度、[Cutout](https://arxiv.org/abs/1708.04552) 和 [Sample Pairing](https://arxiv.org/abs/1801.02929)。

搜索有效的图像变换技术是一个离散优化问题，可以采用网格搜索、随机搜索、强化学习（RL）或进化算法等方法来求解。

在 AutoAugment 中，研究人员选择了强化学习和一个循环神经网络作为控制器算法。控制器的训练目标是提升验证集准确率，但由于准确率不可微，他们使用策略梯度方法来更新这个 RNN。

![Data augmentation pytorch autoaugment](https://sebastianraschka.com/images/blog/2023/data-augmentation-pytorch/autoaugment.webp)

控制器是一个有 100 个隐藏单元的单层 LSTM（细节见[这里](https://arxiv.org/abs/1707.07012)）。训练使用了 PPO（[近端策略优化](https://arxiv.org/abs/1707.06347)）。

策略本身由两部分组成：（1）应用某个给定图像增强技术的概率，（2）应用所选技术的幅度。研究人员为 CIFAR-10/100、SVHN 和 ImageNet 数据集设计（学习）了策略，但根据论文中的结果，这些策略是可迁移的，在其他新数据集上同样表现良好。

请注意，当我们使用 PyTorch/torchvision 提供的 AutoAugment 时，使用的是针对相应数据集学习到的策略（而不是重新训练这些策略）。例如，对于 CIFAR-10，我们会使用 `torchvision.transforms.AutoAugment(torchvision.transforms.AutoAugmentPolicy.CIFAR10)`。

### RandAugment

[AutoAugment](https://arxiv.org/abs/1909.13719) 通过基于强化学习的策略优化，在代理任务上学习增强方式。

RandAugment 由上一节 AutoAugment 方法的原作者开发，他们提出了一种简单得多的做法。RandAugment 不像 AutoAugment 那样学习增强策略，而是把增强技术的选择转化为一个超参数搜索问题。

换句话说，与 AutoAugment 不同，RandAugment 不需要单独的搜索过程。相反，对于每个 minibatch 中的每张图像，RandAugment 以均匀概率选择一种图像变换策略——每种增强被选中的概率相同。

RandAugment 有两个超参数：（1）对给定图像应用的增强数量，以及（2）这些增强的幅度。根据论文，RandAugment 方法可以用两行 Python 代码实现：

```python
transforms = [
    'Identity', 'AutoContrast', 'Equalize',
    'Rotate', 'Solarize', 'Color', 'Posterize',
    'Contrast', 'Brightness', 'Sharpness',
    'ShearX', 'ShearY', 'TranslateX', 'TranslateY'
]

def randaugment(N, M):
"""Generate a set of distortions.
   Args:
     N: Number of augmentation transformations to
        apply sequentially.
     M: Magnitude for all the transformations.
"""
sampled_ops = np.random.choice(transforms, N)
return [(op, M) for op in sampled_ops]
```

（注意，每个变换的幅度会被转换成 31 个离散的档位。默认情况下，增强数量为 2，幅度的默认档位为 9。）

### AugMix

[AugMix](https://arxiv.org/abs/1912.02781) 专门用于提升对数据偏移的鲁棒性，例如部署阶段经常遇到的情况。在这里，作者混合不同的图像增强技术来提升分类器性能，同时优化一个一致性损失。

AugMix 所选择的图像变换与 AutoAugment 类似，只是去掉了对比度、色彩、亮度、锐度和 Cutout。此外，AugMix 并不是纯粹按顺序应用各变换，而是将增强组合起来。

![Data augmentation pytorch augmix](https://sebastianraschka.com/images/blog/2023/data-augmentation-pytorch/augmix.webp)

注意，在上图中，最终图像 \(x\_{\text{augmix}}\) 是通过对增强图像 \(x\_{\text{aug}}\) 与原始图像 \(x\_{\text{orig}}\) 进行插值（混合）得到的，而 \(x\_{\text{aug}}\) 也是通过施加不同的混合权重（\(w\_1, w\_2, w\_3\)）得到的。

为此，研究人员优化一个由两部分组成的总体损失：

\[\text{Loss}\_{\text{overall}} = \text{Loss}\_{\text{classification}} + \text{Loss}\_{\text{consistency}}.\]

分类损失是标准的交叉熵损失，一致性损失则是将模型应用于原始图像的 softmax 输出与应用于增强图像的 softmax 输出之间的 [Jensen-Shannon 散度](https://en.wikipedia.org/wiki/Jensen%E2%80%93Shannon_divergence)。

（Jensen-Shannon 散度是 [Kullback-Leibler 散度](https://en.wikipedia.org/wiki/Kullback%E2%80%93Leibler_divergence)的对称版本，用于衡量两个概率分布之间的差异。Kullback-Leibler 散度本身等于交叉熵减去自熵项。）

### TrivialAugment

[TrivialAugment](https://arxiv.org/abs/2103.10158) 是一种极简方法，每张图像只应用一种增强。与 AutoAugment 或 AugMix 不同，它不是一个学习出来的过程。

![Data augmentation pytorch trivialaugment](https://sebastianraschka.com/images/blog/2023/data-augmentation-pytorch/trivialaugment.webp)

表面上，TrivialAugment 看起来像是 RandAugment 的特例。然而，RandAugment 可能对每张图像应用不止一种图像变换，而 TrivialAugment 则严格只应用单一增强。此外，RandAugment 对每张图像使用固定的增强强度（该强度是一个超参数，作用于数据集中的每张图像）；与此相反，TrivialAugment 为每张单独的图像随机采样强度。
