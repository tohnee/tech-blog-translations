---
title: "彩票假设及其实际用途"
title_en: "The Lottery Ticket Hypothesis and Its Practical Uses"
source: https://sebastianraschka.com/faq/docs/lottery-ticket.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 彩票假设及其实际用途

根据彩票假设（lottery ticket hypothesis）[ref]，一个随机初始化的神经网络中可能包含一个子网络，当这个子网络单独接受训练时，在经过相同步数的训练后，可以在测试集上达到与原始网络相同的准确率。

- [ref] Frankle & Carbin (2018). *The Lottery Ticket Hypothesis: Finding Sparse, Trainable Neural Networks.* <https://arxiv.org/abs/1803.03635>.

下图以更直观的方式展示了彩票假设的训练流程。我们会逐步过一遍各个步骤，帮助厘清这一概念。

![](https://sebastianraschka.com/images/faq/lottery-ticket/lottery-1.png)

我们先从一个大型神经网络（1）开始，把它训练到收敛（2），也就是说，我们尽最大努力让它在目标数据集上表现得尽可能好——例如，最小化训练损失、最大化分类准确率。这个大型神经网络照常用较小的随机权重进行初始化。

接着，我们对神经网络的权重参数做剪枝（3），把它们从网络中移除。具体做法可以是把这些权重置零，从而得到稀疏权重矩阵。那么要剪掉哪些权重呢？原始彩票假设的方法遵循一种叫做*迭代幅度剪枝（iterative magnitude pruning）*的思路，即以迭代的方式移除幅度（绝对值）最小的那些权重。

剪枝步骤之后，我们把权重重置为第 1 步中使用的原始小随机值。值得强调的是，我们并不像迭代幅度剪枝中常见的那样，用任意的小随机权重重新初始化剪枝后的网络，而是复用第 1 步中的那些权重。

然后不断重复第 2-4 步的剪枝流程，直到网络达到期望的规模。例如，在彩票假设的原始论文中，作者成功地把网络缩减到原始规模的 10%，而没有牺牲分类准确率。一个额外的好处是，这个剪枝后的（稀疏）网络——被称为「中奖彩票」（winning ticket）——与原始的（大型稠密）网络相比，甚至表现出了更好的泛化性能。

---

**这是我的书 [Machine Learning Q and AI](https://leanpub.com/machine-learning-q-and-ai/) 中一个答案的精简版与摘录，书中有更详尽的版本和更多插图。**
