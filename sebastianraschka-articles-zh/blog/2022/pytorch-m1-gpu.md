---
title: "在 M1 GPU 上运行 PyTorch"
title_en: "Running PyTorch on the M1 GPU"
source: https://sebastianraschka.com/blog/2022/pytorch-m1-gpu.html
crawled: 2026-09-06
translated: 2026-09-06
---

# 在 M1 GPU 上运行 PyTorch

> 原文：[Running PyTorch on the M1 GPU](https://sebastianraschka.com/blog/2022/pytorch-m1-gpu.html)

今天，[PyTorch 官方宣布](https://pytorch.org/blog/introducing-accelerated-pytorch-training-on-mac/)为 Apple 的 ARM M1 芯片提供 GPU 支持。对 Mac 用户来说这是激动人心的一天，所以今晚我花了几分钟实际试用了一下。在这篇简短的博客中，我将总结我使用 M1 芯片做深度学习任务的体验和想法。

## 我到目前为止的 M1 使用体验

回想 2021 年初，我愉快地卖掉了又吵又笨重的 15 英寸 Intel MacBook Pro，换了一台便宜得多的 M1 MacBook Air。到目前为止它都是一台极好的机器：安静、轻便、速度超快，续航也很棒。

写新书的时候我注意到，它不仅日常使用感觉快，而且还能给若干计算提速。例如，预处理 IMDb 电影数据集在我的 2019 款 Intel MacBook Pro 上[需要 1 分 51 秒](https://github.com/rasbt/python-machine-learning-book-3rd-edition/blob/master/ch08/ch08.ipynb)，而在 M1 上[只要 21 秒](https://github.com/rasbt/machine-learning-book/blob/main/ch08/ch08.ipynb)。

同样，所有与 scikit-learn 相关的工作流在 M1 MacBook Air 上也快得多！我甚至能在合理的时间内用 PyTorch 跑小型神经网络（教学用的各种多层感知机和卷积神经网络）。我记得还做过一次 LeNet-5 在 M1 与 GeForce 1080Ti 之间的运行时间对比，发现速度不相上下。

尽管 M1 MacBook 是一台了不起的机器，但在它上面训练现代深度神经网络确实不现实。它真的搞不定比 LeNet 更复杂的东西。不过要说明的是，当时作为尝鲜者我自己编译了 PyTorch，而且只能使用 M1 的 CPU。

## PyTorch 的 M1 GPU 支持

今天，PyTorch 团队[终于宣布了 M1 GPU 支持](https://pytorch.org/blog/introducing-accelerated-pytorch-training-on-mac/)，我很兴奋地试了试。公告附带的[基准测试](https://sebastianraschka.com/glossary/#benchmark "Benchmark")显示，训练 VGG16 时 M1 GPU 比 CPU 快约 8 倍，推理（评估）时快约 21 倍。按照细则说明，他们是在配备 M1 Ultra 的 Mac Studio 上测的。我猜这里的 CPU 指的是 M1 Ultra 的 CPU。

如何安装带 M1 GPU 支持的 PyTorch 版本？我预计 M1 GPU 支持会包含在 1.12 版本中，建议关注 [release 列表](https://github.com/pytorch/pytorch/releases)获取更新。不过现在，我们可以从最新的 nightly 版本安装：

![Pytorch m1 gpu m1 support](https://sebastianraschka.com/images/blog/2022/pytorch-m1-gpu/m1-support.webp)

（截图来自 [pytorch.org](https://pytorch.org)）

就我个人而言，我建议在终端中按如下方式安装：

```python
$ conda create -n torch-nightly python=3.8 

$ conda activate torch-nightly

$ pip install --pre torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/nightly/cpu
```

然后，如果你想在 GPU 上运行 PyTorch 代码，使用 `torch.device("mps")`，就像在 Nvidia GPU 上使用 `torch.device("cuda")` 一样。

（一个有趣的小知识：支持 M1 GPU 的 PyTorch 安装包大小约为 45 MB。而支持 CUDA 10.2 的 PyTorch 安装包大小约为 750 MB。）

## 我的基准测试

纯粹出于好奇，我想亲自试一试，于是在各种硬件上各训练一个 epoch 的深度神经网络，包括一台配置强悍的深度学习工作站上的 12 核 Intel 服务器级 CPU，以及一台搭载 M1 Pro 芯片的 MacBook Pro。下面是把 CIFAR-10 图像缩放到 224x224 像素（VGG16 常用的 ImageNet 尺寸）后，VGG16 的结果：

![Pytorch m1 gpu vgg benchmark training](https://sebastianraschka.com/images/blog/2022/pytorch-m1-gpu/vgg-benchmark-training.webp)

---

**关于这些运行的补充细节**

（[M1 Max](https://github.com/rasbt/machine-learning-notes/issues/3) 和 [M1 Ultra](https://github.com/rasbt/machine-learning-notes/issues/12) 的结果由读者热心提供。我还补充了[这里](https://github.com/rasbt/machine-learning-notes/issues/6)和[这里](https://github.com/rasbt/machine-learning-notes/issues/7)热心提供的 RTX 3060 和 RTX 3080 结果。）

除 RTX 3060 外，所有运行的批大小（batch size）均为 32——RTX 3060 只有 6 GB 显存，只能用 8 的批大小。

你可能注意到上图中有某些运行出现了两个版本：5 月 18 日和 5 月 22 日。显然，5 月 18 日的 nightly 版本（torch 1.12.0.dev20220518）存在一个[内存泄漏](https://github.com/pytorch/pytorch/issues/77753#issuecomment-1133875782)，已于 5 月 21 日修复。于是我升级到 5 月 22 日的 nightly 版本（torch-1.13.0.dev20220522）并重跑了实验。

---

与 M1 Pro CPU（从上往下第四行）和 M1 Pro GPU（从下往上第六行）相比，M1 Pro GPU 训练该网络快了 3.5 倍。这至少算是点进步！

接下来看看推理速度。这里的推理指的是在测试集上评估模型：

![Pytorch m1 gpu vgg benchmark inference](https://sebastianraschka.com/images/blog/2022/pytorch-m1-gpu/vgg-benchmark-inference.webp)

在推理时，M1 Pro CPU 与 GPU 之间的速度优势更加明显。例如，M1 Pro GPU（1.69 分钟）比 M1 Pro CPU（8.51 分钟）快 5 倍。

所以，虽然 M1 GPU 支持相比 M1 CPU 带来了明显提升，但它还算不上彻底的改变，进行神经网络训练时我们可能仍要依赖传统 GPU。Mac Studio 的 M1 Ultra 更接近 Nvidia GPU 的性能，但别忘了这是一台昂贵的（约 5000 美元）机器！

关于 M1 GPU 性能的一些补充说明：

- 我注意到，卷积网络在 CPU 或 M1 GPU 上运行时（与 CUDA GPU 相比）需要多得多的内存，而且可能存在换页（swap）问题。不过，我确保了在 MacBook Pro 上训练时[内存占用始终不超过 80%](https://twitter.com/rasbt/status/1527115038720512000?s=20&t=k1374Sdramu2rFp0EQGkxA)。
- 如前所述，M1 GPU 运行时没有把批大小拉满也可能是原因之一。不过为了公平，我所有的训练运行都使用 32 的批大小——2080Ti 和 1080Ti 由于只有 11 GB 显存，也用不了更大的批大小。**更新：** 我用 64 的批大小重跑了 M1 Pro GPU 的运行，结果比 32 的批大小快了约 20%。

另外要记住，这是一个全新功能的早期版本，随着时间推移它可能会改进。不过，它能跑起来并且正处于积极开发之中，这本身就已经足够令人兴奋了！🙌

如果你想自己运行这些代码，[这里是脚本的链接](https://github.com/rasbt/machine-learning-notes/tree/main/benchmark/pytorch-m1-gpu)。

（如果你对如何改进 GPU 性能有任何想法，请[告诉我](https://twitter.com/rasbt/status/1527102613749125120?s=20&t=gerAjN40WmmDglsNDFj5Mg)！）

## 结论

搭载 M1 GPU 的 MacBook 会成为我的深度学习主力吗？绝对不会。我认为我们不该把笔记本当作训练深度神经网络的主力机器。原因在于：

- 它们的单位性能成本很高（与工作站相比）；
- 它们会变得相当烫，这肯定不利于健康；
- 如果满负荷使用，它们在我们通常想让它做的其他任务上就会变得很吃力。

不过，笔记本始终是我的效率主力。我几乎用它做所有事情，包括简单的科学计算，以及在把复杂的神经网络代码放到工作站或云端集群上运行之前的调试。

我从这次基准测试中得到的个人结论是：PyTorch 的 M1 GPU 支持终于可用了，这很令人兴奋！虽然还有一些小问题需要打磨，才能跑得比 CPU 更顺畅、更快，但我预计它会让笔记本（嗯，MacBook）作为深度学习的效率、原型和调试机器的吸引力显著提升。🎉

附言：如果你对如何提升 M1 GPU 性能有什么想法，请[联系我](https://twitter.com/rasbt/status/1527102613749125120?s=20&t=gerAjN40WmmDglsNDFj5Mg) 🙏。
