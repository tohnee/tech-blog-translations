---
title: "《Deep Learning with PyTorch》书评"
title_en: "Deep Learning with PyTorch Review"
source: https://sebastianraschka.com/blog/2021/pytorch-deeplearning-review.html
crawled: 2026-09-06
translated: 2026-09-06
---

# 《Deep Learning with PyTorch》书评

> 原文：[Deep Learning with PyTorch Review](https://sebastianraschka.com/blog/2021/pytorch-deeplearning-review.html)

《Deep Learning with PyTorch》自 2020 年 8 月出版以来就一直放在我的书架上，直到这个寒假我才终于有机会读完它。事实证明，在轻松的假期之后，它是一本非常适合用来找回一点工作状态的轻松读物。正如我[上周](https://twitter.com/rasbt/status/1348680806487760897?s=20)承诺的那样，以下是我的想法。

![Drawing](https://sebastianraschka.com/images/blog/2021/pytorch-deeplearning-review/IMG_5363.webp)

**免责声明**
我想说明的是，我与本书作者没有任何关联，也没有收到过这本书的赠阅版。下面写下的一切都是我诚实、无偏向的意见。

这本书引起我兴趣的主要原因在于我喜欢读书，而且作为一名长期的 PyTorch 用户，我觉得或许能从这本书里发现一些有用的技巧。此外，我也在为我的深度学习课程（STAT 453: Introduction to Deep Learning and Generative Models）寻找一份对学生有帮助的资源。在过去几个学期里，我一直向学生推荐在线教程作为"延伸阅读资源"。不过我认为，拥有更多选择，以及一份可能更加一致、更有结构的资源，应该会受到欢迎。

## 全书的组织方式

全书分为三个部分，总计约 470 页内容。听起来不少，但由于其轻松的风格和语调，整体读起来相当快。不出所料，书中包含了相当数量的代码。不过，鉴于深度学习代码出了名的冗长（例如与使用 scikit-learn 的机器学习相比），作者做出了正确的决定：精简部分代码段落，并链接到其 [GitHub 仓库](https://github.com/deep-learning-with-pytorch/dlwpt-code)中的相关部分。我认为这是个好决定，因为它让本书的可读性大大提高。接下来，让我再多谈谈这三个部分。

第 1 部分（第 1–9 章）介绍 PyTorch 和深度学习背后的宏观概念。值得注意的是，它采用自顶向下的方式切入，也就是说，先使用一个预训练模型。然后，它更详细地讲解 PyTorch，并在基础层面上解释多层感知机和用于图像分类的卷积神经网络。我特别喜欢其中对 PyTorch 的介绍，这大概是我迄今为止在这个主题上见过的组织得最好的资源。不过总体而言，它仍停留在初学者水平——更适合新手，而非高级实践者。

第 2 部分（第 9–14 章）提供了一个特别有趣、耳目一新的思路。这五章带领读者从头到尾完成一个动手的计算机视觉项目。该项目围绕检测肺部 CT 扫描（3D 数据）中的癌性结节展开。各章环环相扣，读起来像一个故事，引导读者走过各个组成部分：数据加载、分割、分组、分类、分析和诊断。同样值得称道的是，第一章着重强调了对底层数据的理解——这是真实项目中至关重要却常被忽视的一环。

![Drawing](https://sebastianraschka.com/images/blog/2021/pytorch-deeplearning-review/ch9-scan.webp)

（*第 9 章一张插图的翻拍，概述了第 2 部分涵盖的主题。*）

最后，第 3 部分（第 15 章）讨论 PyTorch 的生产与部署。它更接近第 1 部分的风格：各小节是自成一体的示例和讲解（区别于第 2 部分的连续项目）。第 3 部分只有一章，因此相对简短。不过，这种简短也许是个好兆头，说明 PyTorch 的部署工具并没有那么复杂。它具体涵盖了通过 Flask 和 Sanic 进行基础的服务器部署、通过 ONNX 导出 PyTorch 模型、PyTorch JIT 的 tracing 与 scripting 两种模式，以及在移动端运行 PyTorch 模型。虽然这与我的研究需求无关，但我真的很喜欢这一部分，因为它结构清晰、简洁明了，而且其中大部分内容对我来说都很新鲜。例如，我觉得书中对 PyTorch JIT 的 tracing 与 scripting 之间区别的讲解非常有帮助。既然你可能也对两者的区别感到好奇，请允许我在下面稍微跑题一下。

## 题外话：关于 TorchScript

你可能知道，出于性能考虑，PyTorch（与大多数其他科学计算库类似，例如 NumPy）在底层使用了优化过的 C++ 代码。Python 只是充当一个 API"胶水层"，让这些函数更易于使用。大多数人（包括我在内）都是通过 Python API 使用 PyTorch 的。不过，[它也提供 C++ API](https://pytorch.org/cppdocs/installing.html)（其发行版称为 *LibTorch*）。这在部署和生产场景中会派上用场：你可能无法访问 Python 运行时，或者希望避免使用它。

既然 PyTorch API 本来就依赖 C++ 代码，我们就可以通过 TorchScript 计算图或中间表示（也称 TorchScript IR）把 Python-PyTorch 代码转换回 C++ 代码。通过 Torch JIT 的 *tracing*（追踪）和 *scripting*（脚本化）都可以做到这一点。下面我草绘了我对这些概念之间关系的理解。

![Drawing](https://sebastianraschka.com/images/blog/2021/pytorch-deeplearning-review/pytorch-ir-sketch.webp)

（*我对底层各组件如何连接与工作的理解草图*）

Torch 的 C++ autograd 接口随后可以使用 TorchScript IR 计算图进行部署，从而把 Python 从（计算）等式中去掉。如上所述，如果目标环境没有 Python 运行时，或者你想提升深度学习模型的性能，这尤其有吸引力。顺便一提，事实证明 PyTorch 中大多数与深度学习相关的代码已经通过调用 C++ 和 CUDA 代码得到了高度优化。因此，Python 很可能并不是性能上的大瓶颈（这也是为什么我认为 Python 在深度学习领域还会长期保持其地位）。引用作者的话：

> 人们常说 Python 缺乏速度。这有一定道理，但我们在 PyTorch 中使用的张量运算本身通常已经足够庞大，Python 在运算之间的缓慢并不是一个大问题。对于智能手机这类小型设备来说，Python 带来的内存开销可能更为重要。所以请记住，多数情况下，把 Python 从计算中剔除所换来的加速只有 10% 或更少。

现在，通过 torch.jit.trace 进行的 *tracing* 会借助样例输入来追踪计算。如果我们有一个迭代五次的 for 循环（如下所示），这个 for 循环会被展开成 5 个独立的步骤：

![Drawing](https://sebastianraschka.com/images/blog/2021/pytorch-deeplearning-review/trace.webp)

上述 tracing 方式的一个缺点是：一旦我们把函数追踪成中间表示（它可以作为编译器的输入），编译后的函数就只适用于大小为 5 的输入，正如上方的 `TracerWarning` 所示。

JIT 的 `script` 方式比 tracing 更灵活，因为它可以在不依赖输入的情况下转换函数：

![Drawing](https://sebastianraschka.com/images/blog/2021/pytorch-deeplearning-review/script.webp)

在实践中，更常见的做法是使用方便的 `@torch.jit.script` 函数装饰器。无论如何，在这段小插曲之后，下一节继续回到对本书的讨论。

## 阅读预期：广度与深度

总体来说，这本书写得很简单、易于上手。它涵盖了深度学习和 PyTorch 的基础知识，除要求读者熟悉 Python 之外不假设任何先验知识。全书也完全不出现公式（好吧，除了一幅演示 softmax 函数的插图）。引用作者的话：

> "我们宁可把事情保持简单，以便专注于基本概念；等你掌握了基础，那些聪明的花活可以以后再来。"

从这个角度看，它与 Goodfellow 等人的 [Deep Learning](https://www.deeplearningbook.org/) 一书正好相反——后者不含代码，更适合已有一定深度学习基础的读者。实际上，两本书是互补的（例如，初学者可以先读这本 PyTorch 书建立基本理解，再通过 Goodfellow 等人的书深入细节）。

读者需要注意的一点是，这本书高度聚焦于计算机视觉，所有神经网络示例都是在图像数据的语境下给出的。文本等其他数据模态并未涉及。本书也仅限于多层感知机和卷积架构（U-Net 与 ResNet）；其他类型的神经网络架构，例如循环神经网络、图神经网络、自编码器、生成对抗网络和 Transformer，都不在本书的范围之内。

## 令人印象深刻的亮点

除了整体上有趣的结构（例如读起来像一个故事的、以项目为主线的第 2 部分），我还喜欢这本书通过预训练模型做图像分类的自顶向下开局。考虑到深度学习代码可能非常冗长，我可以想象这会降低入门门槛，让深度学习对新手来说不那么吓人。此外，口语化的语言和偶尔的幽默也让这本书读起来相对轻松。
很多代码片段都带有直接的行内标注。这是我在课程幻灯片里常做、但之前从未在书里见过的事情。非常有效。

![Drawing](https://sebastianraschka.com/images/blog/2021/pytorch-deeplearning-review/code-annotation.webp)

（*书中代码片段行内标注的示例。*）

## 总体评价

总体而言，我认为对于完全零基础的深度学习初学者来说，这是一本很棒的书。那些已经是深度学习专家、又特别关注 PyTorch 的读者可能会觉得这本书偏入门，但我认为第 3 章仍然值得一读。它是一份精美、自成体系的 PyTorch 基础入门，比我在网上见过的其他资源都更赏心悦目、更有条理。

![Drawing](https://sebastianraschka.com/images/blog/2021/pytorch-deeplearning-review/chapter-3.webp)

（*第 3 章涵盖内容的概览。*）

我确实认为这本书很适合作为涉及编程环节和课程项目的深度学习课程的配套读物。尤其是第 2 部分的完整项目走读，可以帮助学生规划自己课程项目的结构。

---

## 附赠：Leviathan Wakes

作为一个小小的附赠，我想谈谈我在最初那条推文中提到的另一本书，因为也有一些人（更）感兴趣想听听它的消息。

![Drawing](https://sebastianraschka.com/images/blog/2021/pytorch-deeplearning-review/both-books.webp)

（来源：<https://twitter.com/rasbt/status/1348680806487760897?s=20>）

James S. A. Corey（Daniel Abraham 和 Ty Franck 的合用笔名）所著的《Leviathan Wakes》（《巨兽苏醒》）是一部老派而纯正的太空歌剧——同样是一本轻松愉快的读物。故事设定在一个不算太遥远的近未来（也许是 22 世纪？），人类已经殖民了火星以及火星与木星之间的小行星带。虽然它不是硬科幻，但背景设定显得可信而合理，同时始终把重点放在讲好一个有趣的故事上。《Leviathan Wakes》是"The Expanse"（苍穹浩瀚）系列的第一部。顺便一提，这个系列最近也被改编成了电视剧。不过我没有看过，所以无法多加评论。

大多数科幻书籍都会聚焦于太空的某个特定侧面，以此形成自己的独特之处。《Leviathan Wakes》聚焦的是重力与辐射。例如，加速中的飞船会改变重力的方向，角色们配备了在需要时才使用的磁力靴。这一切都以细致入微的笔触加以描绘，让这个世界（或者说这些行星与太空）显得非常可信。

主线故事围绕两位主角展开。其中一个是典型的正义英雄形象，另一个则是反英雄。后者让我想起《银翼杀手》里的 Deckard，而"带环带"（Belt）的场景则带有浓厚的黑色侦探小说气息，营造出一种扣人心弦的氛围。

这本书有个有趣之处：各章节从两位主角的视角交替书写，每一章切换一次视角。这种视角切换让我想起《冰与火之歌》系列，但由于只聚焦于两个人的视角，跟踪这条相对直白却引人入胜的故事线（它讲述的是一个缓缓揭开的谜团）要容易得多。

总的来说，我很享受这本书。它没有我喜欢的 Joe Abercrombie 作品中那种挖苦式的幽默，也不像《辅助正义》（Ancillary Justice）那样不走寻常路。不过，它是一部动作场面密集的轻松读物，有着一些有趣的故事元素和绝妙的黑色氛围，正好适合辛苦一天之后在夜晚轻松一读。我非常喜欢它，所以一定会去找这个系列的其他几本来看。
