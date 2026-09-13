---
title: "使用合成梯度的解耦神经接口"
title_en: "Decoupled Neural Interfaces Using Synthetic Gradients"
source: https://deepmind.google/blog/decoupled-neural-interfaces-using-synthetic-gradients/
site: deepmind
date: 2016-08-29
crawled: 2026-09-13
translated: 2026-09-13
---

# 使用合成梯度的解耦神经接口

> 原文：[Decoupled Neural Interfaces Using Synthetic Gradients](https://deepmind.google/blog/decoupled-neural-interfaces-using-synthetic-gradients/) · Google DeepMind

本文介绍我们推进神经网络能力与训练程序的最新研究之一：[《Decoupled Neural Interfaces using Synthetic Gradients》](https://arxiv.org/abs/1608.05343)。这项工作为我们提供了一种方式，让神经网络能够彼此通信、学习在彼此之间传递消息，而且是以解耦、可扩展的方式进行，为多个神经网络相互通信或改进循环网络的长期时间依赖铺平了道路。其实现方式是用一个模型来近似误差梯度，而不是通过反向传播显式地计算误差梯度。本文的其余部分假定读者对神经网络及其训练方式有一定了解。如果你是这个领域的新手，我们强烈推荐 YouTube 上的 [Nando de Freitas 深度学习与神经网络系列讲座](https://www.youtube.com/watch?v=PlhFWT7vAEw)。

## 神经网络与锁定问题

考虑神经网络中的任意一层或任意模块：只有在网络中所有后续模块都执行完毕、梯度已经反向传播到它之后，它才能被更新。例如，看这个简单的前馈网络：

![简单前馈神经网络的示意图，包含 Layer 1、Layer 2 与 Layer 3。黑色箭头表示激活从输入向损失的前向传播，绿色箭头表示误差梯度反向穿过每一层的反向传播。](https://lh3.googleusercontent.com/gKMZKitakIj90Cl_p9pwClgZGr1TXsfkhcnjszz7v9SHLBP889DLNZ91Ao8sv5aI32CsPD5faULJgNBdEPRSKRO0gHEccS7qIwpsrqJwH1h96fmGKw=w1440)

在这里，Layer 1 处理完输入之后，必须等输出激活（黑线）传播过网络的其余部分、生成一个损失，然后误差梯度（绿线）反向传播穿过每一层直到 Layer 1，它才能被更新。这一操作顺序意味着 Layer 1 必须等待 Layer 2 与 Layer 3 的前向和反向计算完成才能更新。Layer 1 与网络的其余部分被锁定、耦合在一起。

为什么这是个问题？显然，对如图所示的简单前馈网络，我们无需担心这个问题。但请设想一个复杂系统：多个网络在多个环境中运行，时间尺度异步且不规则。

或者设想一个分布在多台机器上的大型分布式网络。有时，要求一个网络中的所有模块都等待所有其他模块执行并反向传播梯度，会过于耗时，甚至完全不可行。如果我们把模块之间的接口——也就是连接——解耦，那么每个模块都可以独立更新，不再被锁定在网络其余部分上。

那么，如何解耦神经接口——即解耦网络模块之间的连接——同时仍让模块学会交互？在本文中，我们移除了对反向传播获取误差梯度的依赖，转而学习一个参数化模型，它仅凭局部信息预测梯度将会是什么。我们把这些预测出的梯度称为合成梯度（synthetic gradients）。

![合成梯度模型的示意图，由一个粉蓝相间的菱形表示。一条标注「Activations」（激活）的虚线箭头从底部指向该菱形，一条蓝色箭头从菱形向上指出，标注「Predicted gradient of the loss with respect to the input activations」（损失对输入激活的预测梯度），标题为「Synthetic Gradient」（合成梯度）。](https://lh3.googleusercontent.com/7SXqEPfXP2m7h9v_yQNxU9tgkCPrpsRw8a6jk_MOLqvQU7nwiwJyRMPV59h7t4xiws91jZ7R2s7tjraro2I09yKv4wsnDOLvKM-7r4_T2h8jtDogSlE=w1440)

合成梯度模型接收来自某个模块的激活，输出它预测的误差梯度——即网络损失对这些激活的梯度。

回到我们简单的前馈网络例子，如果我们拥有一个合成梯度模型，就可以这样做：

![前馈网络示意图，包含 Layer 1、Layer 2 与 Layer 3。输入的激活传入 Layer 1，Layer 1 已变为橙色以表示被更新。一条虚线黑色箭头从 Layer 1 分叉指向 Layer 2 和一个由粉蓝菱形表示的合成梯度模型。代表合成梯度的蓝色箭头从这个菱形指回 Layer 1，在 Layer 2 与 Layer 3 尚未执行之前就更新它。](https://lh3.googleusercontent.com/4AODyPgWTg6IlgFMOPkIYTd5MhwOZKDCtCbW2W835YurHvjK7F2jJqnnDh9mEdUmVt6gui6EET2w46n7c9ed2JiXX7jbvdef-tKrrlijxT809NKY=w1440)

……并利用合成梯度（蓝色）在网络其余部分尚未执行之前就更新 Layer 1。

合成梯度模型本身则被训练来回归目标梯度——这些目标梯度既可以是从损失反向传播回来的真实梯度，也可以是从更下游的合成梯度模型反向传播回来的其他合成梯度。

![前馈网络示意图，包含 Layer 1、Layer 2 与 Layer 3。输入传入已被更新的 Layer 1。虚线黑色箭头从 Layer 2 分叉指向 Layer 3 和一个由粉蓝菱形表示的合成梯度模型。代表合成梯度的蓝色箭头从这个菱形指回 Layer 2。同时，一条代表真实梯度的绿色箭头从 Layer 2 向后指出，与代表合成梯度的蓝色圆点进行对比，并被反向传播至第二个合成梯度模型以更新它。](https://lh3.googleusercontent.com/O8zXOyLBjsgMbL-EYBBAkWBc6eK-H_BrcwYjJzn7sjYkrfkjeBMmbvYwBhnIj4UJTkDKePVOxoGsOlEwYsT_eGXXcRDxC7FtRaW3XJXRY7prVMd87Q=w1440)

这一机制对任意两个模块之间的连接都是通用的，并不限于前馈网络。下方动画展示了该机制的一步步运作过程，其中模块颜色的变化表示该模块的权重被更新。

![动画示意图，展示两个循环神经网络核心之间解耦神经接口（DNI）的逐步执行过程，其中合成梯度（以菱形表示）被用于异步更新前序模块。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622277b1a1bf935c82935454_Decoupled20Neural20Interfaces20Using20Synthetic20.gif)

因此，使用解耦神经接口（DNI）移除了网络中前序模块对后续模块的锁定。在论文的实验中，我们展示了对 [CIFAR-10](https://www.cs.toronto.edu/~kriz/cifar.html) 图像分类任务训练卷积神经网络时，可以让每一层都通过合成梯度解耦，并达到与使用反向传播相同的准确率。需要认识到，DNI 并没有神奇地让网络在缺乏真实梯度信息的情况下完成训练。真实梯度信息确实会向后渗透穿过网络，只是更慢、需要更多的训练迭代，它通过合成梯度模型的损失来传递。合成梯度模型对真实梯度的缺失进行了近似与平滑。

此时一个合理的提问是：这些合成梯度模型会增加多少计算复杂度——也许你会需要一个与网络本身一样复杂的合成梯度模型架构。令人相当惊讶的是，合成梯度模型可以非常简单。对于前馈网络，我们实际上发现哪怕只是一个单线性层，也能很好地充当合成梯度模型。因此它既非常容易训练，又能快速产生合成梯度。

DNI 可以应用于任何通用神经网络架构，而不只是前馈网络。一个有趣的应用是循环神经网络（RNN）。RNN 有一个循环核心，它被展开——即反复施加——以处理序列数据。理想情况下，训练 RNN 时我们应当把核心沿整个序列展开（序列可能无限长），并使用随时间反向传播（BPTT）把误差梯度沿计算图向后传播。

![对理论上的循环神经网络处理序列数据的示意性可视化。](https://lh3.googleusercontent.com/176LUr08t3brnefNEfe2y8AGSxueJzDMR9fD5hXMygWilzynofdFJ2Gu05Jq6fbQXUv_n2B3DWM4FOZ5n4gIW4jerr7zZ9fODnwAIDO2BuXEk1adwQE=w1440)

然而在实践中，由于内存限制以及需要频繁地对核心模型实际计算更新，我们只能负担起展开有限步数。这称为截断的随时间反向传播（truncated BPTT），下图展示了截断为三步的情形：

![循环神经网络处理序列数据的示意性可视化。由于内存限制，每隔若干步它就不进行反向传播。](https://lh3.googleusercontent.com/m6Y_UtdxCXLQoISfhBrLA7zSVmQAZvuuF0RhEXmGTU6jzDwKdK9VVE47UwAmkVZ3SnRi6N291469Ji_RoQ92qdEQsSiWBU087ZvA6YX1SaL6P558-70=w1440)

核心颜色的变化表示核心被更新，即权重已被更新。在这个例子里，截断 BPTT 似乎解决了训练中的一些问题——我们现在每三步就能更新一次核心权重，而且内存中只需保留三个核心。然而，由于误差梯度无法在超过三步的范围内反向传播，对核心的更新将不会直接受到两步之后所犯错误的影响。这限制了 RNN 能够学习建模的时间依赖长度。

那么，如果不在 BPTT 边界处完全放弃反向传播，而是使用 DNI 产生合成梯度——用它来建模未来的误差梯度将会是什么——会怎样？我们可以在核心中内置一个合成梯度模型，使得在每个时间步，RNN 核心不仅产生输出，还产生合成梯度。在这种情形下，合成梯度就是对全部未来损失关于上一个时间步隐状态激活的预测梯度。合成梯度只在截断 BPTT 的边界处使用——也就是原本完全没有梯度的地方。

![使用解耦神经接口的循环神经网络示意图，在截断随时间反向传播的边界处生成合成梯度，以实现高效的长期时间依赖训练。](https://lh3.googleusercontent.com/GXOXL6nSDB5Avf7Lozqg82VAtOHHpFyKewwxUwxPavL1pjZZisFY8ggUD2VQmfIHA7oextLHMDbo6lC6vqf6iDSLyJGJU8cz55RJb6HM4m7vbgrj=w1440)

这可以在训练中非常高效地完成——它只需我们在内存中多保留一个核心，如下图所示。这里，绿色虚线边框表示只计算关于输入状态的梯度，而绿色实线边框则额外计算关于核心参数的梯度。

在 RNN 上使用 DNI 与合成梯度，相当于近似地对一个无限展开的 RNN 做反向传播。在实践中，这使得 RNN 能够建模更长的时间依赖。下面是论文中展示这一点的一个示例结果。

Penn Treebank 训练期间的测试误差（越低越好）：

![折线图，绘制训练期间 Penn Treebank 测试误差（以 BPC，即每字符比特数计）随数据时间的变化。图中比较了分别展开 8、20、40 步的标准截断反向传播模型（分别为蓝色、红色和灰色虚线曲线）与展开 8 步的 DNI 模型（蓝色实线曲线）。DNI T=8.0 模型以明显更快的速度达到更低的测试误差（1.34 BPC）。](https://lh3.googleusercontent.com/kVnUvieA74S1cPmlcEnVIOQo-Zj4rvdy_rwGZdZTrBwUPqPHXueM4FjpQP-UDQazL2zv9a2KmgLEwCnUlIe-kfrZ-ki4zqGqkQVrON12Hreuafxf-Q=w1440)

这张图展示了在 Penn Treebank 上以下一字符预测任务（一个语言建模问题）训练的 RNN 的应用。y 轴是每字符比特数（BPC），数值越小越好。x 轴是模型随训练进行所见过的字符数。蓝色、红色和灰色虚线分别是用截断 BPTT 训练、分别展开 8 步、20 步和 40 步的 RNN——RNN 在执行随时间反向传播之前展开的步数越多，模型就越好，但训练也越慢。当对展开 8 步的 RNN 使用 DNI 时（蓝色实线），该 RNN 能够捕捉到 40 步模型的长期依赖，但训练速度却快一倍（无论按数据量计，还是按在一台配备单块 GPU 的普通台式机上的实际耗时计）。

再强调一遍，加入合成梯度模型使我们能够解耦网络两个部分之间的更新。DNI 还可以应用于层次化 RNN 模型——即以不同时间尺度运行的两个（或更多）RNN 组成的系统。正如我们在[论文](https://arxiv.org/abs/1608.05343)中展示的，DNI 通过提升高层模块的更新速率，显著改善了这些模型的训练速度。

希望通过本文的讲解，以及对我们在[论文](https://arxiv.org/abs/1608.05343)中报告的部分实验的简要浏览，可以明显看出：构建解耦神经接口是可行的。具体做法是创建一个合成梯度模型，它接收局部信息并预测误差梯度将会是什么。从较高的层面上看，这可以被视为两个模块之间的一种通信协议：一个模块发送消息（当前激活），另一个模块接收消息，并使用一个效用模型（即合成梯度模型）来评估它。这个效用模型让接收方能够向发送方提供即时反馈（合成梯度），而不必等待对消息真实效用的评估（经由反向传播）。这一框架也可以从「误差评论家」（error critic）的视角来理解 [[Werbos](http://www.werbos.com/HICChapter13.pdf)]，其风格与在强化学习中使用 critic 相似 [[Baxter](http://www.cis.upenn.edu/~mkearns/finread/BaxterWeaverBartlett.pdf)]。

这些解耦神经接口让网络的分布式训练成为可能，增强了 RNN 学到的时间依赖，并加速了层次化 RNN 系统。我们很期待探索 DNI 的未来，因为我们认为它将成为开启更加模块化、解耦化、异步化的模型架构的重要基础。最后，论文中还有更多细节、技巧与完整实验，请[在此](https://arxiv.org/abs/1608.05343)阅读。

神经网络是 DeepMind 所开发的许多算法的主力。例如，[AlphaGo](https://deepmind.com/research/case-studies/alphago-the-story-so-far) 使用卷积神经网络来评估围棋对局中的棋盘局面，[DQN](https://deepmind.com/research/publications/human-level-control-through-deep-reinforcement-learning/) 与[深度强化学习算法](https://deepmind.com/blog/article/deep-reinforcement-learning)则使用神经网络选择动作，在电子游戏中打出超越人类的水平。
