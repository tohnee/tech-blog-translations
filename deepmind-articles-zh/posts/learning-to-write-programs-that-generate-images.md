---
title: "学习编写生成图像的程序"
title_en: "Learning to write programs that generate images"
source: https://deepmind.google/blog/learning-to-write-programs-that-generate-images/
site: deepmind
date: 2018-03-27
crawled: 2026-09-13
translated: 2026-09-13
---

# 学习编写生成图像的程序

> 原文：[Learning to write programs that generate images](https://deepmind.google/blog/learning-to-write-programs-that-generate-images/) · Google DeepMind

在人类眼中，世界远不止是映入角膜的图像。例如，当我们端详一座建筑并赞叹其设计的精妙时，我们能体会到它所需的匠心。这种借助创造事物所用工具来解读事物的能力，让我们对世界有更丰富的理解，也是我们智能的一个重要方面。

我们希望自己的系统能够构建同样丰富的世界表征。例如，在观察一幅画作的图像时，我们希望它们能理解创作它时所用的笔触，而不只是屏幕上代表它的像素。

在[这项工作](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/learning-to-write-programs-that-generate-images/SPIRAL.pdf)中，我们为人工智能体配备了与我们生成图像时相同的工具，并证明它们能够推理数字、字符和肖像的构成方式。关键在于，它们靠自己学会了这一点，无需人工标注的数据集。这与[近期研究](https://arxiv.org/pdf/1704.03477.pdf)形成对比——后者迄今依赖从人类示范中学习，而那可能是一个费时的过程。

![左侧是一个人用毛笔书写字母；右侧是绘有古代画作和手印的洞穴岩壁。](https://lh3.googleusercontent.com/xvuBowQ7eb2bVc4zds8fwwp_PKR0kkH1wMmxRILCw1NSqjLlgxhfQGO6x1H4-OZcAQrcy8e3nFF7bOetCBu5fvyyRtiOJ9TjwsovL3uiNRurcX4XvJU=w1440)

图片来源：Shutterstock

我们设计了一个与计算机[画图程序](http://mypaint.org/)交互的深度强化学习智能体：它在数字画布上落笔作画，并可以改变笔刷的大小、压力和颜色。未经训练的智能体一开始只会画一些看不出意图或结构的随机笔画。为解决这个问题，我们必须设计一种奖励机制，鼓励它画出有意义的图像。

为此，我们训练了第二个神经网络——判别器（discriminator），它唯一的任务是判断某幅画是智能体画的，还是从真实照片数据集中采样的。绘画智能体获得的奖励取决于它在多大程度上成功「骗过」判别器、让其相信自己的画是真迹。换句话说，智能体的奖励信号本身就是学出来的。这与生成对抗网络（GAN）中使用的方法相似，但有所不同：GAN 中的生成器通常是直接输出像素的神经网络，而我们的智能体是通过编写图形程序与画图环境交互来生成图像。

![AI 尝试控制数字画笔工具来重现字符和数字的动画](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62268128f70ee1eb07d75761_L2W2002.gif)

在第一组实验中，智能体被训练生成类似 [MNIST](http://yann.lecun.com/exdb/mnist/) 数字的图像：它看到了数字长什么样，但没有看到数字是怎么写出来的。通过尝试生成能骗过判别器的图像，智能体学会了控制画笔并操纵它以契合不同数字的风格，这项技术被称为视觉[程序合成（program synthesis）](https://en.wikipedia.org/wiki/Program_synthesis)。

我们还训练它复现特定的图像。在这里，判别器的目标是判断复现的图像究竟是目标图像的复制，还是智能体的创作。这一区分对判别器越困难，智能体获得的奖励就越多。

至关重要的是，该框架还是可解释的，因为它产生的是控制模拟画笔的一系列动作。这意味着模型可以把在模拟画图程序中学到的内容应用到其他类似环境中重新创作字符，例如在模拟或真实的机械臂上。相关视频可在[此处](https://youtu.be/XXM3PdIdLJQ)观看。

![智能体收到一幅二维输入图像，尝试自己动手绘制以复现该图像。它在数字环境中的绘制结果接近但不完美。下一步是让智能体控制机械臂，尝试在现实世界中画出这幅图像。图中也展示了这一点——结果同样接近但不完美。](https://lh3.googleusercontent.com/E1NV89M6PctVsgZ0wEMnBR__FYy2mmQYd5uwdMoGNHJYInhZorZksW2j0Rv5DpNyl3WCOg0t7L6ujVWEXsUJ6BpJxrvgr12B41oyBpLERWcxMqDHPYU=w1440)

这一框架也有潜力扩展到真实数据集。在训练绘制[名人面孔](http://mmlab.ie.cuhk.edu.hk/projects/CelebA.html)时，智能体能捕捉面部的整体特征，如形状、色调和发型，就像街头画师用有限的笔触画肖像那样：

![AI 复现了20张名人面孔的色调、大致轮廓和关键特征。细节不多，但明显在一定程度上重现了原图。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62268149c481fcf0a1269b88_L2W2004.gif)

从原始感觉中恢复结构化表征，是人类轻易具备并频繁使用的能力。在这项工作中，我们证明可以为人工智能体提供与我们重现周遭世界相同的工具，引导它们生成类似的表征。由此，它们学会生成简洁表达因果关系的视觉程序，而这些因果关系正是产生其观测的原因。

尽管我们的工作只是迈向灵活程序合成的一小步，我们预计要让人工智能体具备类人的认知、泛化和交流能力，类似的技术可能是必需的。

**注**

视频可在[此处](https://www.youtube.com/watch?v=iSyvwAwa7vk&feature=youtu.be)观看；方法的更多细节请阅读[论文](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/learning-to-write-programs-that-generate-images/SPIRAL.pdf)。

本工作由 Yaroslav Ganin、Tejas Kulkarni、Igor Babuschkin、S. M. Ali Eslami 和 Oriol Vinyals 完成，并感谢 Oleg Sushkov、David Barker、Matej Vecerik 和 Jon Scholz 在机器人方面的帮助。
