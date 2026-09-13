---
title: "Batch Size 取 2 的幂的迷思"
title_en: "Batch Size Powers-of-2 Myth"
source: https://sebastianraschka.com/blog/2022/batch-size-2.html
crawled: 2026-09-06
translated: 2026-09-06
---

# Batch Size 取 2 的幂的迷思

> 原文：[Batch Size Powers-of-2 Myth](https://sebastianraschka.com/blog/2022/batch-size-2.html)

在神经网络训练这件事上，我想我们都有过这样的习惯：把 batch size 选成 2 的幂，也就是 64、128、256、512、1024 等等。（这里的 batch size 指的是当我们基于随机梯度下降类优化算法、通过反向传播训练神经网络时，每个 minibatch 中训练样本的数量。）

据说是出于习惯，也因为这是约定俗成的标准惯例。理由是我们曾被教导：把 batch size 选成 2 的幂有助于从计算角度提升训练效率。

这个说法有一些有效的理论依据，但在实践中效果究竟如何？前几天我们围绕这个问题进行了一些[讨论](https://twitter.com/rasbt/status/1542882893181108227?s=20&t=EhZ1RY7qN2w3xO6w-M28MA)，在这里我想把一些要点记录下来，以便日后引用。希望这对你也有帮助！

## 背后的主要想法与理论

在查看动手[基准测试](https://sebastianraschka.com/glossary/#benchmark "Benchmark")结果之前，我们先简要过一遍"把 batch size 选成 2 的幂"背后的主要想法。下面两个小节将简要介绍两个主要论点：内存对齐与浮点运算效率。

### 内存对齐

支持把 batch size 选成 2 的幂的一个主要论据是：CPU 和 GPU 的内存架构本身就是按 2 的幂组织的。或者更准确地说，存在[*内存页*](https://en.wikipedia.org/wiki/Page_(computer_memory))的概念，它本质上是一块连续的内存。如果你用的是 macOS 或 Linux，可以在终端执行 `getconf PAGESIZE` 查看页大小，返回的数字应该就是 2 的幂。

![Batch size 2 pagesize](https://sebastianraschka.com/images/blog/2022/batch-size-power-2/pagesize.webp)

这个想法是让一个或多个 batch 恰好装进一页内存，以帮助 GPU 进行并行处理。换句话说，我们把 batch size 选成 2 的幂是为了更好的内存对齐。这类似于（并且很可能受到了启发于）在游戏开发和图形设计中使用 OpenGL 和 DirectX 时[选择 2 的幂大小的纹理](https://gamedev.stackexchange.com/questions/7927/should-i-use-textures-not-sized-to-a-power-of-2)。

### 矩阵乘法与 Tensor Core

再深入一点，Nvidia 有一份[《矩阵乘法背景用户指南》](https://docs.nvidia.com/deeplearning/performance/dl-performance-matrix-multiplication/index.html#gpu-imple)，解释了矩阵维度与图形处理器（GPU）计算效率之间的关系。这篇文章的建议并不是把矩阵维度选成 2 的幂，而是在配备 [Tensor Core](https://en.wikipedia.org/wiki/Deep_learning_super_sampling#Architecture) 的 GPU 上做混合精度训练时，把矩阵维度选成 8 的倍数。当然，这两种选择之间存在重叠：

![Batch size 2 intersect](https://sebastianraschka.com/images/blog/2022/batch-size-power-2/intersect.webp)

为什么是 8 的倍数？这与矩阵乘法有关。假设我们有矩阵 \(A\) 和 \(B\) 之间的如下矩阵乘法：

![Batch size 2 matmul1](https://sebastianraschka.com/images/blog/2022/batch-size-power-2/matmul1.webp)

计算矩阵 \(A\) 和 \(B\) 乘积的一种方式，是计算矩阵 \(A\) 的行向量与矩阵 \(B\) 的列向量之间的点积。如下图所示，这些是 \(k\) 元素向量两两之间的点积：

![Batch size 2 matmul2](https://sebastianraschka.com/images/blog/2022/batch-size-power-2/matmul2.webp)

每个点积由一次"加法"和一次"乘法"操作组成，而我们一共有 \(M \times N\) 个这样的点积。所以总共有 \(2 \times M \times N \times K\) 次浮点运算（FLOPS）。

（当然，这并不是 GPU 上矩阵乘法的真实实现方式；GPU 上的矩阵乘法涉及[分块（tiling）](https://docs.nvidia.com/deeplearning/performance/dl-performance-matrix-multiplication/index.html#gpu-imple)。）

现在，如果我们使用配备 [Tensor Core](https://en.wikipedia.org/wiki/Deep_learning_super_sampling#Architecture) 的 GPU（例如 V100），当矩阵维度（\(M\)、\(N\) 和 \(K\)）对齐到 16 字节的倍数时，计算效率更高（依据 Nvidia 的[这份指南](https://docs.nvidia.com/deeplearning/performance/dl-performance-matrix-multiplication/index.html#gpu-imple)）。而在 [FP16 混合精度训练](https://docs.nvidia.com/deeplearning/performance/mixed-precision-training/index.html)的情况下，8 的倍数是效率最优的。

通常，维度 \(K\) 和 \(N\) 由神经网络架构决定（如果我们自己设计架构，则有一定的回旋余地）。不过，batch size（这里的 \(M\)）通常是我们完全可以控制的。

那么，假设 8 的倍数的 batch size 在配备 Tensor Core 的 GPU 和 FP16 [混合精度](https://sebastianraschka.com/glossary/#mixed-precision "Mixed Precision")训练下理论上最高效，让我们来考察一下在实践中差异到底有多大。

## 一个简单的基准测试

为了观察不同 batch size 在实践中对训练的影响，我运行了一个简单的基准测试：在 [CIFAR-10](https://www.cs.toronto.edu/~kriz/cifar.html) 上训练 [MobileNetV3](https://arxiv.org/abs/1905.02244v5)（large）10 个 epoch——图像被调整为 \(224 \times 224\) 以达到合理的 GPU 利用率。训练在 [V100](https://www.nvidia.com/en-us/data-center/v100/) 卡上进行，使用 16 位原生自动混合精度训练，这能更高效地利用 GPU 的 Tensor Core。

如果你想自己跑一遍，代码在这个 GitHub 仓库里：https://github.com/rasbt/b3-basic-batchsize-benchmark。

### 小 Batch Size 基准测试

我从 batch size 128 附近的小规模基准开始。"Train Time"对应在 CIFAR-10 上训练 MobileNetV3 共 10 个 epoch 的时间。推理时间指在测试集的 1 万张图像上评估模型的时间。

| Batch Size | Train Time | Inference Time | Epochs | GPU | Mixed Precision |
| --- | --- | --- | --- | --- | --- |
| 100 | 10.50 min | 0.15 min | 10 | V100 | Yes |
| 127 | 9.80 min | 0.15 min | 10 | V100 | Yes |
| 128 | 9.78 min | 0.15 min | 10 | V100 | Yes |
| 129 | 9.92 min | 0.15 min | 10 | V100 | Yes |
| 156 | 9.38 min | 0.16 min | 10 | V100 | Yes |

```python
      |
```

看上表，我们以 batch size 128 作为参考点。看起来，把 batch size 减一（127）或加一（129）确实会让训练性能略微变慢。不过这里的差异几乎察觉不到，我认为可以忽略不计。

把 batch size 减 28（100）带来的性能下降则明显一些。这很可能是因为模型现在需要处理比之前更多的 batch（50,000 / 100 = 500 vs. 50,000 / 128 = 390）。出于类似的原因，我们可以观察到把 batch size 加 28（156）时训练时间反而更短。

### 最大 Batch Size 基准测试

考虑到 MobileNetV3 的架构和输入图像尺寸，上一节的 batch size 相对较小，GPU 利用率在 70% 左右。为了考察 GPU 满负载时的训练时间差异，我把 batch size 增加到 512，让 GPU 显示接近 100% 的计算利用率：

| Batch Size | Train Time | Inference Time | Epochs | GPU | Mixed Precision |
| --- | --- | --- | --- | --- | --- |
| 511 | 8.74 min | 0.17 min | 10 | V100 | Yes |
| 512 | 8.71 min | 0.17 min | 10 | V100 | Yes |
| 513 | 8.72 min | 0.17 min | 10 | V100 | Yes |

（由于 GPU 显存限制，无法使用大于 515 的 batch size。）

同样，正如我们之前看到的，2 的幂（或 8 的倍数）的 batch size 确实有一点差异，但几乎察觉不到。

### 多 GPU 训练

前面的基准测试评估的是单 GPU 上的训练性能。然而，如今更常见的做法是在多个 GPU 上训练深度神经网络。那么，让我们看看多 GPU 训练时的数字对比。

| Batch Size | Train Time | Epochs | GPU | Mixed Precision |
| --- | --- | --- | --- | --- |
| 255 | 2.95 min | 10 | 4xV100 | Yes |
| 256 | 2.87 min | 10 | 4xV100 | Yes |
| 257 | 2.86 min | 10 | 4xV100 | Yes |

（注意，推理速度被省略了，因为实践中我们通常仍然只用单个 GPU 做推理。另外，由于 GPU 显存限制，我无法以 batch size 512 运行基准测试，所以把它降到了 256。）

可以看到，这一次，2 的幂且为 8 的倍数的 batch size（256）并不比 257 更快。

这里我使用 [DistributedDataParallel](https://pytorch.org/tutorials/intermediate/ddp_tutorial.html)（DDP）作为默认的多 GPU 训练策略。不过，欢迎读者用其他多 GPU 训练策略重复这些实验。[GitHub](https://github.com/rasbt/b3-basic-batchsize-benchmark) 上的代码支持 `--strategy ddp_sharded`（fairscale）、`ddp_spawn`、`deepspeed` 等。

### 基准测试的注意事项：真实世界 vs. 实验室

需要强调的是，上面所有基准测试都存在一些注意事项。例如，每个设置我只跑了一次。理想情况下，我们应该把每次运行重复多次，并报告平均值和标准差。（不过，这大概率不会影响"性能上没有实质差异"这一结论。）

另外，虽然我是在同一台机器上运行所有基准测试的（这是好事），但我是按先后顺序连续运行的，各次运行之间没有长时间间隔。这意味着每次运行时的 GPU 基础[温度](https://sebastianraschka.com/glossary/#temperature "Temperature")可能不同，可能会轻微影响计时结果。

我运行这些基准测试是为了模拟一个真实世界的用例，即在 PyTorch 中用相对常见的设置训练一个现成的架构。不过，正如 [Piotr Bialecki 正确指出的](https://twitter.com/ptrblck_de/status/1543037414121213952?s=20&t=UWSJsx3g-ulVM51Obp3LTQ)，设置 `torch.backends.cudnn.benchmark = True` 可以略微提升训练速度。

## 更多资源与讨论

[正如 Ross Wightman 提到的](https://twitter.com/wightmanr/status/1542917523556904960?s=20&t=owhg9v-fyN58ICd1lTF0FA)，他同样不认为把 batch size 选成 2 的幂会带来可感知的差异。不过，对于某些矩阵维度来说，选择 8 的倍数可能很重要。此外，[Ross Wightman 指出](https://twitter.com/wightmanr/status/1542917667715108864?s=20&t=owhg9v-fyN58ICd1lTF0FA)，在使用 TPU 时 batch size 非常关键。（遗憾的是，我不方便使用 TPU，也就没有相关的基准测试对比。）

如果你对更多的 GPU 基准测试感兴趣，请参阅 Thomas Bierhance 的精彩文章[这里](https://wandb.ai/datenzauberai/Batch-Size-Testing/reports/Do-Batch-Sizes-Actually-Need-to-be-Powers-of-2---VmlldzoyMDkwNDQx)。如果你正在寻找以下场景的对比，这篇文章尤其有价值：

- 在没有 Tensor Core 的显卡上；
- 不使用混合精度训练；
- 在 [DeiT](https://arxiv.org/abs/2012.12877) 这类无卷积的视觉 Transformer 上。

Rémi Coulom-Kayufu 的一个有趣的[实验](https://twitter.com/Remi_Coulom/status/1259188988646129665?s=20&t=UTsX1zhhmVhkgvMHzJmY3w)表明，2 的幂的 batch size 实际上反而不好。看起来，对于卷积神经网络，可以通过 \(\text{batch size}=int((n \times (1<<14)\times SM)/(H\times W\times C))\) 计算出合适的 batch size。其中 \(n\) 是整数，\(SM\) 是 GPU 核心数（例如 V100 为 80，RTX 2080 Ti 为 68）。

## 结论

基于本文分享的基准测试结果，我不认为把 batch size 选成 2 的幂或 8 的倍数会在实践中带来可感知的差异。

不过，在任何给定的项目中，无论是研究基准还是真实世界的机器学习应用，需要调的旋钮已经够多了。所以，把 batch size 选成 2 的幂（即 64、128、256、512、1024 等）有助于让事情更简单、更易管理。此外，如果你打算发表学术论文，把 batch size 选成 2 的幂会让你的结果看起来不那么像是刻意挑选的。

虽然坚持使用 2 的幂的 batch size 有助于约束超参数搜索空间，但需要强调的是，batch size 仍然是一个超参数。[有人认为更小的 batch size 有助于泛化性能](https://arxiv.org/abs/1804.07612)，也有人[建议尽可能增大 batch size](https://arxiv.org/abs/1711.00489)。

就个人而言，我发现最优 batch size 高度依赖于神经网络架构和损失函数。例如，在最近一个使用相同 ResNet 架构的研究项目中，[我发现最优 batch size 会随损失函数的不同而在 16 到 256 之间变化](https://arxiv.org/abs/2111.08851)。所以，我建议始终把调整 batch size 纳入你的超参数优化搜索。不过，如果由于显存限制你无法使用 512 的 batch size，也不必直接退到 256。先考虑 500 这样的 batch size 完全没问题。
