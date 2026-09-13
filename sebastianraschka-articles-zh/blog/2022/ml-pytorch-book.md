---
title: "PyTorch 与 Scikit-Learn 新书发布"
title_en: "PyTorch and Scikit-Learn Book Release"
source: https://sebastianraschka.com/blog/2022/ml-pytorch-book.html
crawled: 2026-09-06
translated: 2026-09-06
---

# PyTorch 与 Scikit-Learn 新书发布

> 原文：[PyTorch and Scikit-Learn Book Release](https://sebastianraschka.com/blog/2022/ml-pytorch-book.html)

《Machine Learning with PyTorch and Scikit-Learn》的写作历经多年，如今终于可以聊聊这本新书的发布了，我很兴奋。这个项目最初是作为《Python Machine Learning》第 4 版启动的。但我们对这本书做了太多改动，以至于我们认为它值得一个新书名来体现这一点。那么，新增了什么内容呢？在这篇文章里，我想把这一切讲给你听。

[![Ml pytorch book cover 1](https://sebastianraschka.com/images/blog/2022/ml-pytorch-book/cover_1.webp)](https://www.amazon.com/Machine-Learning-PyTorch-Scikit-Learn-scikit-learn-ebook-dp-B09NW48MR1/dp/B09NW48MR1/)

## 本书的结构

在深入讲那些令人兴奋的内容之前，先让我快速介绍一下这本书的结构。总体而言，本书是对机器学习的全面介绍，既包括"传统"机器学习——即不使用神经网络的机器学习——也包括深度学习。

前十章介绍基于 [scikit-learn](https://scikit-learn.org/stable/) 的机器学习，它可能是当今使用最广泛的机器学习库。本书第一部分教授机器学习的所有基础概念，包括数据预处理、模型评估和超参数调优。

![Ml pytorch book TOC](https://sebastianraschka.com/images/blog/2022/ml-pytorch-book/TOC.webp)

第 11 章是全书的转折点。在这一章，我展示了如何用 NumPy 从零实现一个多层神经网络，并一步步带你走一遍反向传播——一种广泛用于神经网络训练的流行算法。

![Ml pytorch book backprop](https://sebastianraschka.com/images/blog/2022/ml-pytorch-book/backprop.webp)

本书的后半部分聚焦深度学习，涵盖图像与文本的分类和生成等主题。还有一章讨论图结构数据，这是一个令人兴奋的方向，拓展了深度学习的应用范围。最后，本书以强化学习收尾——它基本上是一个独立的子领域（不过其中也有一节使用深度学习来做强化学习）。

现在要说明的是，这反映的是 [*Python Machine Learning, 3rd edition*](https://www.amazon.com/Python-Machine-Learning-scikit-learn-TensorFlow/dp/1789955750/ref=sr_1_1_sspa) 的总体结构。不过，我会在下面几节里讲到多处重写、扩充的章节，以及两个全新的章节。全书超过 770 页，我们也已经到了内容量的极限——再多一些，可能就做不出纸质版了 😅。

## 使用 PyTorch

从书名你就能注意到，一大变化是我们把深度学习章节的代码示例从 TensorFlow 迁移到了 PyTorch。这是一项大工程，我非常感谢 [Yuxi (Hayden) Liu](https://www.linkedin.com/in/hayden-liu-80445056/) 主导了这次迁移并给予我帮助。

PyTorch 于 2016 年发布，而我全面采用它用于科研和[教学](https://sebastianraschka.com/blog/2021/dl-course.html)也已经四年了。我喜欢 PyTorch 的地方在于：它设计良好、使用便捷，同时又足够灵活，让我可以在自己的[研究项目](https://raschka-research-group.github.io/coral-pytorch/)中随手定制。

而且喜欢用 PyTorch 的不只是我。[根据最新趋势](https://paperswithcode.com/trends)，在近期的深度学习论文中，大约 60% 的代码实现使用 PyTorch。

![Ml pytorch book papers with code](https://sebastianraschka.com/images/blog/2022/ml-pytorch-book/papers-with-code.webp)

（来源：[Papers with Code](https://paperswithcode.com/trends)）

作为一个小福利，我还增加了一节关于 [PyTorch Lightning](https://www.pytorchlightning.ai/) 的内容，这是一个帮助组织代码和项目的库，也让多 GPU 训练这类复杂的事情容易得多。由于我现在与 PyTorch Lightning 团队合作更紧密，请期待未来更多 PyTorch Lightning 相关的后续内容。

无论你是完全的深度学习新手，还是已经用其他深度学习框架开启了自己的深度学习之旅，我相信你都会喜欢使用 PyTorch。

## 面向自然语言处理的 Transformer

你可能已经听说，Transformer 如今是自然语言处理最先进成果背后的主流深度学习架构。在这一章，你将了解 Transformer 如何从循环神经网络演化而来。我们会一步步讲解[自注意力](https://sebastianraschka.com/glossary/#mha "Multi-Head Attention (MHA)")机制，一直讲到[最初的 Transformer 架构](https://arxiv.org/abs/1706.03762)。不过，这一章并不止步于此。

我们还介绍了各种 [GPT](https://en.wikipedia.org/wiki/GPT-2) 架构（专注于文本生成的解码器型 Transformer）和 [BERT](https://en.wikipedia.org/wiki/BERT_(language_model))（专注于文本分类的编码器型 Transformer），并向你展示如何在实践中使用这些架构。别担心，你不需要超级计算机——我们展示了如何采用免费开放的预训练模型，并在新任务上对它们进行微调。

![Ml pytorch book adapting transformers](https://sebastianraschka.com/images/blog/2022/ml-pytorch-book/adapting-transformers.webp)

去年讲完一堂很[长的 Transformer 课](https://sebastianraschka.com/blog/2021/dl-course.html#l19-self-attention-and-transformer-networks)之后，我就非常期待写这个新章节。在 [Jitian Zhao](https://jzhao326.github.io/) 的大力帮助下，我们重新组织了这些内容，使其更易上手。我尤其为改进后的行文脉络和新配的插图感到骄傲，它们能更好地阐释这些概念。

![Ml pytorch book self attention](https://sebastianraschka.com/images/blog/2022/ml-pytorch-book/self-attention.webp)

## 图神经网络

看了上一节，你可能会觉得 Transformer 独占了风头。不过，我对第二个新章节——图神经网络——同样非常兴奋。这个主题与我的研究兴趣密切相关，也是深度学习中一个激动人心的新方向。

图神经网络真正酷的地方在于，它让我们能够处理图结构数据（而不是表格、图像或文本）。例如，不少现实世界的问题本身就以图的形式呈现，包括社交网络图和分子（化学物质）图。

![Ml pytorch book graphs](https://sebastianraschka.com/images/blog/2022/ml-pytorch-book/graphs.webp)

在这一章，我们一步一步解释图神经网络的工作原理。本章首先说明如何把图组织成深度神经网络的输入，然后讲使用图卷积的动机，从零实现一个图神经网络，最后用 PyTorch Geometric 完成一个分子性质预测任务。

这一章我有幸与 [Ben Kaufman](https://www.linkedin.com/in/benjamin-kaufman-26b1a994/) 合作，他是我目前共同指导的博士生。我正和 Ben 一起做几个令人兴奋的研究项目，也很感谢他热情地承担了本章的主要写作工作。

本章源于我们共同的一个兴趣：在虚拟筛选背景下使用图神经网络——虚拟筛选是生物活性分子与（药物）发现中常用的一种计算流程。（如果你对这个话题的更多细节感兴趣，我们的综述文章 [*Machine Learning and AI-based Approaches for Bioactive Ligand Discovery and GPCR-ligand Recognition*](https://www.sciencedirect.com/science/article/pii/S1046202319302762) 可能也合你的口味。）

## 焕然一新的排版

这是我与 Packt 合作的第五本书（我常常忘记自己很久很久以前还写过一本关于 [R 语言热力图](https://sebastianraschka.com/all-books/#heat-maps-in-r-how-to)的书），而这次全新的排版让我兴奋不已！新排版采用了更窄的页边距（这是在页数限制内装下全部内容的唯一办法），并加上了图注——在上面几张书中插图的截图里可以看到。

不过最重要的是，新排版对书中的数学部分更友好：数学符号的字号终于统一了。

![Ml pytorch book mathy stuff](https://sebastianraschka.com/images/blog/2022/ml-pytorch-book/mathy-stuff.webp)

此外还有一个加分项：本书现在支持代码语法高亮。我发现这能让某些代码容易读得多。

![Ml pytorch book new look](https://sebastianraschka.com/images/blog/2022/ml-pytorch-book/new-look.webp)

一个小瑕疵是行内代码带有深色背景，打印时可能有点麻烦，但对那些在代码编辑器或命令行终端里就偏好深色背景的众多程序员来说，可能反而更亲切。

![Ml pytorch book graph conv](https://sebastianraschka.com/images/blog/2022/ml-pytorch-book/graph-conv.webp)

最后要说明的是，为了让书价保持在合理水平，纸质版只有灰度印刷。我还没收到纸质书，所以没法附上它的实拍图。不过我一直在[我的黑白电子墨水阅读器](https://twitter.com/rasbt/status/1493074934230355972?s=20&t=d5tv9xLkPrdq7oacFTTuZw)上读这本书，看起来效果相当不错 😊。

![Ml pytorch book ereader](https://sebastianraschka.com/images/blog/2022/ml-pytorch-book/ereader.webp)

事实上，由于可以毫无顾忌地随手涂写，电子阅读器近来已成为我读书的首选。当然，如果你更喜欢彩色，可以考虑非墨水屏的平板，或者去翻翻本书的 [GitHub 仓库](https://github.com/rasbt/machine-learning-book)——我把所有插图都以彩色上传，并嵌入到了 Jupyter notebook 里，方便查阅。

## 其他改动

除了两个新章节，以及把所有基于 TensorFlow 的章节迁移到 PyTorch 之外，本书第一部分也有若干改动。

例如，我几乎是从零重写了第 11 章——从零实现神经网络——以便更好地讲解反向传播。逻辑回归等其他章节也做了翻新。虽然我不想逐一罗列所有小改动，但我也修订了一些插图，如下所示。

![Ml pytorch book concept overhaul](https://sebastianraschka.com/images/blog/2022/ml-pytorch-book/concept-overhaul.webp)

总体而言，全书散布着许多小的增补。像 PCA 因子载荷或随机搜索这样的小内容——单拎出来似乎不值一提——但在实际应用中可能产生很大影响。

![Ml pytorch book randomized search](https://sebastianraschka.com/images/blog/2022/ml-pytorch-book/randomized-search.webp)

最值得注意的新增小节是讲解用于分类的梯度提升。在课堂上我通常[用回归的例子](https://youtu.be/zblsrxc7XpM)讲梯度提升，因为它比分类更简单方便。但有学生问我它在分类任务上如何工作，我也乐于接受把这个内容写下来的挑战。（而且，既然你问了——是的，书里也有一个非常简明的 XGBoost 介绍。）

![Ml pytorch book gradient boosting](https://sebastianraschka.com/images/blog/2022/ml-pytorch-book/gradient-boosting.webp)

## （乐）在其中

总的来说，我对这本书非常兴奋。自从第一版以来，我从没有在一本书的项目里获得过这么多乐趣。我很高兴我们终于切换到了 PyTorch——一个我每天在科研和业余项目中使用的工具。撰写 Transformer 和图神经网络两章的过程也非常愉快。

从零创建所有这些新内容工作量很大。你记笔记、搭结构、画图，然后最终一段一段地把文字填进去。工作量不小，但这正是我所热爱的 🤗。

如果你有任何问题或反馈，我很乐意听到，请随时联系我！最好的去处是 [GitHub 上的讨论区](https://github.com/rasbt/machine-learning-book/discussions)。

希望你会喜欢这本书！

### 链接

- [GitHub 仓库](https://github.com/rasbt/machine-learning-book)
- [Amazon.com 页面](https://www.amazon.com/Machine-Learning-PyTorch-Scikit-Learn-scikit-learn-ebook-dp-B09NW48MR1/dp/B09NW48MR1/)
- [Packt 图书页面](https://www.packtpub.com/product/machine-learning-with-pytorch-and-scikit-learn/9781801819312)
