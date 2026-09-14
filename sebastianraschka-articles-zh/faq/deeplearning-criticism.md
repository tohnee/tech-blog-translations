---
title: "为什么有些人讨厌神经网络/深度学习？"
title_en: "Why do some people hate neural networks/deep learning?"
source: https://sebastianraschka.com/faq/docs/deeplearning-criticism.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 为什么有些人讨厌神经网络/深度学习？

> 原文：[Why do some people hate neural networks/deep learning?](https://sebastianraschka.com/faq/docs/deeplearning-criticism.html) · Sebastian Raschka's FAQ

我也认识很多对神经网络总体上出言不逊的人。就我个人而言，我觉得循环神经网络和卷积神经网络真的很美。不过，有句流行的话说得好：「如果你手里只有一把锤子，那么所有东西看起来都像钉子。」

神经网络背后的数学可能稍微难懂一些，但我不认为它们真的是黑箱。我认为神经网络并不比核 SVM 或随机森林这类标准技术更像黑箱。事实上，我觉得解释反向传播比解释核方法更容易。

不过，我想生物科学领域的人更偏爱「可解释」的结果，比如决策树，他们可以一步一步地跟踪其「推理」过程。无可否认，随机森林更擅长解决预测任务，因为你不必那么担心过拟合或剪枝；但与此同时，我们也损失了一部分这种「可解释性」。尽管如此，我认为这并不完全成立。比如从极端随机树（extremely randomized trees）中计算出的特征重要性，可能比看一棵单独的决策树更有用。

请注意，我并不是在责怪生物研究领域有这种想法，他们要解决的问题确实不同。
假设生物学家想知道配体的哪些官能团在与蛋白质结合位点中的残基发生「相互作用」。当然，首要目标往往是在百万级化合物库中找到一个好的激动剂或拮抗剂（抑制剂或药物）来解决特定问题；除此之外，他们也在努力「理解」和「解释」这些结果。
