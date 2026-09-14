---
title: "作为学习机器的分类是如何发展起来的？"
title_en: "How was classification, as a learning machine, developed?"
source: https://sebastianraschka.com/faq/docs/classifier-history.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 作为学习机器的分类是如何发展起来的？

> 原文：[How was classification, as a learning machine, developed?](https://sebastianraschka.com/faq/docs/classifier-history.html) · Sebastian Raschka's FAQ

我认为有两个里程碑式的奠基性工作。

第一个是 Fisher 的线性判别式（Linear Discriminant）[1]，后来由 Rao [2] 推广为我们今天所熟知的线性判别分析（Linear Discriminant Analysis，LDA）。本质上，LDA 是一种线性变换（或投影）技术，主要用于降维（也就是说，其目标是找到能在线性意义下最好地区分不同类别样本的 k 维特征子空间）。
以最大化类别可分性为目标，对于下面的二维数据集，把它投影到"x 轴分量"上就比投影到"y 轴分量"上更好。

![](https://sebastianraschka.com/images/faq/classifier-history/lda.png)

不过请记住，LDA 是一种投影技术；新特征子空间的特征轴（几乎可以肯定）与你原始的特征轴并不相同。
换句话说，LDA 旨在找到一个能保留大部分类别判别信息的新特征子空间。我想说明什么问题呢？直观上，我们可以构造一个准则函数，来最小化（类别）样本均值之间的距离与类内散度之比。而最大化我们的准则函数，再代入一个阈值函数，就得到了一个线性分类器。
总之，从主观上讲，我会把拥有闭式解的 LDA 归入更经典的统计学领域（或者，鉴于它与 ANOVA 和贝叶斯定理的关联，你也可以称之为概率学习）。

分类的另一个应时的思路是感知机（perceptron）算法，它建立在 McCulloch-Pitt（MCP）神经元概念之上——这是对哺乳动物大脑中神经元如何工作的一个早期（也许是第一个？）建模 [3]。与 LDA 分类器不同，Rosenblatt 的感知机 [4] 是一种增量式学习器。对每个训练样本，它都会将预测的类别标签与真实类别标签进行比较，并相应地调整模型权重。
Rosenblatt 最初的感知机规则相当简单，可以概括为以下几个步骤：

1. 将权重初始化为 0 或很小的随机数。
2. 对每个训练样本 x(i)：
   - 计算输出值。
   - 更新权重。
     每次增量更新权重所用的值由如下学习规则计算：

![](https://sebastianraschka.com/images/faq/classifier-history/perceptron-rule.png)

![](https://sebastianraschka.com/images/faq/classifier-history/perceptron-figure.png)

这种方法存在一些问题：如果数据无法被一条直线或超平面完美分开，算法就永远不会收敛。
对感知机的一个改进是自适应线性神经元（adaptive linear neuron，Adaline）[5]。它与线性回归密切相关（前提是你使用梯度下降这类优化算法而非闭式解）；我们通过比较实值输出与真实类别标签来更新权重。（记住，感知机算法比较的是二值的类别标签，即预测的类别标签与真实的类别标签。）训练好模型之后，我们再用一个阈值函数把实值输出转成类别标签：

![](https://sebastianraschka.com/images/faq/classifier-history/adaline.png)

一个非常相近的概念是逻辑回归（Logistic Regression），只不过我们最小化的是一个 logistic 函数而非线性函数 [6]。再者，我不会说逻辑回归早期的形态就一定是"机器学习"式的做法，直到增量学习（梯度下降、随机梯度下降以及其他优化算法）被用来学习模型权重，它才成为机器学习方法。无论如何，此后科学家们提出了许多其他的代价函数，我想它们多半是受了感知机、Adaline 和逻辑回归的启发。
![](https://sebastianraschka.com/images/faq/classifier-history/activation-functions.png)

例如 SVM 使用的铰链损失（hinge loss）。与类比推理者（analogizer）的 SVM 思路不同的另一个方向是"连接主义"（connectionism），即把神经元单元组合成多层神经网络。虽然科学家们曾把多个 Adaline 单元组合成 Madaline，但 Adaline 的问题在于：线性单元的组合……好吧，它仍然是线性的。总之，这里还有太多东西可写，不过希望这些内容能在一定程度上满足你对早期发展史的好奇心。

[1] Fisher, R. A. (1936). “The Use of Multiple Measurements in Taxonomic Problems”. Annals of Eugenics 7 (2): 179–188. doi:10.1111/j.1469-1809.1936.tb02137.x  
[2] Rao, R. C. (1948). “The utilization of multiple measurements in problems of biological classification”. Journal of the Royal Statistical Society, Series B 10 (2): 159–203.  
[3] McCulloch, W. and Pitts, W. (1943). A logical calculus of the ideas immanent in nervous activity. Bulletin of Mathematical Biophysics, 5:115–133.  
[4] F. Rosenblatt. The perceptron, a perceiving and recognizing automaton Project Para. Cornell Aeronautical Laboratory, 1957.  
[5] B. Widrow et al. Adaptive ”Adaline” neuron using chemical ”memistors”. Number Technical Report 1553-2. Stanford Electron. Labs., Stanford, CA, October 1960.  
[6] Berkson, Joseph. “Application of the logistic function to bio-assay.” Journal of the American Statistical Association 39.227 (1944): 357-365.
