---
title: "dropout 技术背后的基本思想是什么？"
title_en: "What is the basic idea behind the dropout technique?"
source: https://sebastianraschka.com/faq/docs/dropout.html
crawled: 2026-09-06
translated: 2026-09-14
---

# dropout 技术背后的基本思想是什么？

> 原文：[What is the basic idea behind the dropout technique?](https://sebastianraschka.com/faq/docs/dropout.html) · Sebastian Raschka's FAQ

Dropout 是一种正则化技术，其目标是降低模型的复杂度，以防止过拟合。

使用「dropout」时，你以服从伯努利分布的某一概率 p（通常为 50%，但这又是一个需要调节的超参数）随机停用一层中的某些单元（神经元）。这样，如果你把一层的激活值的一半置零，神经网络在训练期间的某次前向传播中就无法依赖特定的激活值。其结果是，神经网络会学习到不同的、冗余的表示；网络无法依赖特定的神经元及其组合（或交互作用）必然存在。另一个不错的副作用是训练会更快。

补充技术说明：dropout 只在训练期间施加，并且你需要对保留的神经元激活值进行重新缩放。例如，如果你把某一层 50% 的激活值置零，就需要把剩下的激活值放大 2 倍。最后，训练完成后，测试时应使用完整的网络（换句话说，把 dropout 概率设为 0）。

更多细节，我推荐原始论文：Srivastava, N., Hinton, G., Krizhevsky, A., Sutskever, I., & Salakhutdinov, R. (2014). *Dropout: A simple way to prevent neural networks from overfitting.* The Journal of Machine Learning Research, 15(1), 1929-1958.
(http://www.cs.toronto.edu/~rsalakhu/papers/srivastava14a.pdf)
