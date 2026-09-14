---
title: "我该如何选择 SVM 核函数？"
title_en: "How do I select SVM kernels?"
source: https://sebastianraschka.com/faq/docs/select_svm_kernels.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 我该如何选择 SVM 核函数？

面对一个任意的数据集，通常你并不知道哪个核函数效果最好。我的建议是：既然你对数据了解不多，就从最简单的假设空间开始，然后逐步向更复杂的假设空间推进。

因此，如果你的数据集是线性可分的，线性核就足够好；反之，如果数据集不是线性可分的，线性核就无能为力了（几乎是从字面意义上无能为力 ;））。

为简单起见（也为了便于可视化），我们假设数据集只有 2 个维度。下面是线性 SVM 在鸢尾花（iris）数据集 2 个特征上的决策区域图：

![](https://sebastianraschka.com/images/faq/select_svm_kernels/1.png)

效果非常好。接下来看 RBF 核 SVM：

![](https://sebastianraschka.com/images/faq/select_svm_kernels/2.png)

看起来线性核和 RBF 核 SVM 在这个数据集上的表现不相上下。那么，为什么要偏好更简单的线性假设呢？在这个特定情形下不妨想想奥卡姆剃刀。线性 SVM 是参数化模型，而 RBF 核 SVM 不是，后者的复杂度会随训练集规模的增长而增长。训练 RBF 核 SVM 不仅更昂贵，你还必须保留核矩阵，而且在预测阶段，把数据投影到那个数据变得线性可分的「无限」高维空间中的开销也更大。此外，需要调节的超参数更多，模型选择也因此更昂贵！最后，复杂模型也更容易过拟合！

好了，上面这些听起来对核方法都非常负面，但这真的取决于数据集。例如，如果你的数据不是线性可分的，使用线性分类器就没有意义：

![](https://sebastianraschka.com/images/faq/select_svm_kernels/3.png)

在这种情况下，RBF 核就要合理得多：

![](https://sebastianraschka.com/images/faq/select_svm_kernels/4.png)

无论如何，我不会在多项式核上花太多心思。实践中，出于（计算性能和预测性能方面的）效率原因，它用处不大。所以经验法则是：线性问题用线性 SVM（或逻辑回归），非线性问题用径向基函数（RBF）核等非线性核。

RBF 核 SVM 的决策区域其实也是一个线性决策区域。RBF 核 SVM 实际所做的是构造特征的非线性组合，把样本提升到一个更高维的特征空间，在那里你可以用线性决策边界把类别分开：

![](https://sebastianraschka.com/images/faq/select_svm_kernels/5.png)

好，上面我用一个可以把数据可视化在 2 维空间中的直观例子带你走了一遍……但在真实世界的问题中，即数据集超过 2 个维度时，我们该怎么办？这时，我们要盯住我们的目标函数：最小化 hinge 损失。我们会设置一个超参数搜索（例如网格搜索），把不同的核函数相互比较。基于损失函数（或某个性能指标，如准确率、F1、MCC、ROC AUC 等），我们就可以确定哪个核函数对给定任务是「合适」的。
