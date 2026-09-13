---
title: "用 WaveNet 实现高保真语音合成"
title_en: "High-fidelity speech synthesis with WaveNet"
source: https://deepmind.google/blog/high-fidelity-speech-synthesis-with-wavenet/
site: deepmind
date: 2017-11-22
crawled: 2026-09-13
translated: 2026-09-13
---

# 用 WaveNet 实现高保真语音合成

> 原文：[High-fidelity speech synthesis with WaveNet](https://deepmind.google/blog/high-fidelity-speech-synthesis-with-wavenet/) · Google DeepMind

十月，我们宣布了我们最先进的语音合成模型 [WaveNet](https://deepmind.com/blog/article/wavenet-generative-model-raw-audio) 已被用于在全球范围内为 [Google Assistant](https://deepmind.com/blog/article/wavenet-launches-google-assistant) 生成逼真的日语和美式英语语音。这个生产级模型——称为 Parallel WaveNet——比[原始模型](https://deepmind.com/blog/article/wavenet-generative-model-raw-audio)快 1000 倍以上，同时还能生成更高质量的音频。

我们的[最新论文](https://arxiv.org/abs/1711.10433)介绍了新模型的细节，以及我们为让该系统能在大规模并行计算环境中工作而开发的「概率密度蒸馏（probability density distillation）」技术。

原始 WaveNet 模型使用自回归连接，每次合成一个采样点，每个新采样点都以之前的采样点为条件。虽然这能生成每秒多达 24000 个采样点的高质量音频，但这种顺序生成方式对生产环境来说太慢了。

![示意图，展示神经网络的并行生成：底部输入节点穿过隐藏层直接连接到顶部输出节点。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62227b1d1dd26da452c9e160_unnamed-2.gif)

原始模型每次合成一个采样点，且每个采样点都以之前的采样点为条件

为了绕开这一限制，我们需要一种能够一次性生成长采样序列且不损失质量的解决方案。我们的方案称为概率密度蒸馏：我们用一个训练完毕的 WaveNet 模型去教第二个「学生」网络——它更小、更并行，因而更适合现代计算硬件。这个学生网络是一个更小的扩张卷积[神经网络](https://en.wikipedia.org/wiki/Convolutional_neural_network)，与原始 WaveNet 类似。但关键在于，每个采样点的生成不依赖任何先前生成的采样点，这意味着我们可以同时生成第一个词和最后一个词——以及介于其间的一切，如下面的动画所示。

![一段动画，展示并行神经网络从输入节点同时生成全部输出节点。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622670e8b58caa5fe7d80033_New20Model.gif)

新的 WaveNet 模型以白噪声为输入，并行合成全部输出采样点

在训练期间，学生网络从一个随机状态开始。它接收随机白噪声作为输入，任务是输出一段连续的音频波形。生成的波形随后被送入训练好的 WaveNet 模型，由后者为每个采样点打分，给学生网络一个信号，让它明白自己距离教师网络期望的输出还有多远。随着时间推移，学生网络可以通过反向传播来不断调整，学会自己应当发出什么样的声音。换个说法：教师和学生都为每个音频采样点的取值输出一个概率分布，训练的目标是最小化教师分布与学生分布之间的 [KL 散度](https://en.wikipedia.org/wiki/Kullback%E2%80%93Leibler_divergence)。

这种训练方法与生成对抗网络（GAN）的设置有相似之处：学生扮演生成器的角色，教师扮演判别器。不过与 GAN 不同的是，学生的目标不是「欺骗」教师，而是与教师合作，尽力匹配教师的表现。

尽管这一训练技术效果很好，我们还需要增加几个额外的损失函数来引导学生走向期望的行为。具体来说，我们加入了一个[感知损失](https://arxiv.org/abs/1508.06576)以避免糟糕的发音、一个对比损失以进一步降低噪声，以及一个功率损失以帮助匹配人类语音的能量。举例来说，如果没有后者，训练出的模型发出的将是耳语而非正常说话声。

把这一切加在一起，我们得以训练出与原始 WaveNet 语音质量相当的 Parallel WaveNet，这一点由平均意见得分（mean opinion scores，MOS）体现——这是一个 1 到 5 的量表，根据人类听者的测试衡量语音听上去有多自然。请注意，即便是人类语音，在 MOS 量表上也只得到 4.667 分。

![表格展示平均意见得分（MOS）：当前最佳非 WaveNet（4.19 ± 0.10）、自回归 WaveNet（4.41 ± 0.07）、Parallel WaveNet（4.41 ± 0.08）。](https://lh3.googleusercontent.com/qWug513KsBO4ONSYx8AOkr5P1Mpej02DOBSPuA3VKRYUr8gb1Wx4IU0e2ZPXzzCtbM9v7FnOGg1vu4J2AJfPVlSl9gplVBebh0P29ORCge5ShXxa=w1440)

当然，概率密度蒸馏的开发只是让 WaveNet 满足生产系统速度与质量要求的其中一步。把 Parallel WaveNet 集成进 Google Assistant 的服务管线，同样需要 DeepMind 应用团队与谷歌语音团队付出不亚于此的巨大工程努力。正是通过双方的通力协作，我们才能在 12 个多月的时间里从基础研究走到谷歌规模的产品。

**说明**

阅读[新论文](https://arxiv.org/abs/1711.10433)。

进一步了解 [Google Assistant 中的 WaveNet](https://deepmind.com/blog/article/wavenet-launches-google-assistant)。

阅读[原始 WaveNet 博客文章](https://deepmind.com/blog/article/wavenet-generative-model-raw-audio)。

阅读原始 [WaveNet 论文](https://arxiv.org/pdf/1609.03499.pdf)。

这项工作由 Aaron van den Oord、Yazhe Li、Igor Babuschkin、Karen Simonyan、Oriol Vinyals、Koray Kavukcuoglu、George van den Driessche、Edward Lockhart、Luis C. Cobo、Florian Stimberg、Norman Casagrande、Dominik Grewe、Seb Noury、Sander Dieleman、Erich Elsen、Nal Kalchbrenner、Heiga Zen、Alex Graves、Helen King、Tom Walters、Dan Belov 和 Demis Hassabis 完成。
