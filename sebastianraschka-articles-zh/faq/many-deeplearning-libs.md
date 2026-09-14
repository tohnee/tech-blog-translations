---
title: "为什么深度学习库这么多？"
title_en: "Why are there so many deep learning libraries?"
source: https://sebastianraschka.com/faq/docs/many-deeplearning-libs.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 为什么深度学习库这么多？

在我看来，主要原因是深度学习领域的一切仍处于高度实验性阶段。这些库通常是某人自己研究的副产品。此外，与其他算法（如随机森林、逻辑回归、SVM 等）相比，深度学习算法并没有那么通用（指编写一份可以套用到许多不同问题上的通用代码）。于是，每个人对于「好的接口应该长什么样」都有自己的独特想法，因此最后可能就会去开发一个新库。而且，他们多半也想把自己的个人研究成果融入相应的库并获得署名——拥有一个可以随心所欲修改的个人库要方便得多。

不过，我也觉得库多可能只是一种错觉，因为深度学习当下确实非常热门，而且我们正生活在一个开源和代码共享（幸运地）非常流行的时代。我猜实现 SVM、逻辑回归等的库其实是深度学习库的 100 倍之多。

总之，如果你有兴趣自己实现神经网络，可以看看 [Theano](http://deeplearning.net/software/theano/)——它常被称作「吃了兴奋剂的 NumPy」。它不仅让你更高效地使用数值表达式，还实现了张量，并让你能够利用 GPU。Theano 实际上正是 Python 中大多数「众多深度学习库」所使用的底层，例如：

- [Lasagne](https://github.com/Lasagne/Lasagne)
- [Keras](http://keras.io)
- [PyLearn 2](https://github.com/lisa-lab/pylearn2)

……
