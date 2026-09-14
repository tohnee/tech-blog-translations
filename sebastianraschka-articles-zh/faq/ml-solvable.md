---
title: "如何判断一个问题能否用机器学习解决？"
title_en: "How do I know if the problem is solvable through machine learning?"
source: https://sebastianraschka.com/faq/docs/ml-solvable.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 如何判断一个问题能否用机器学习解决？

一般来说，大多数机器学习算法都假设我们的训练样本是独立同分布（i.i.d.）的。由于我们希望训练集能代表总体，需要将其随机划分为训练集和测试集。

另外，测试集我们只想用一次；我们不希望反复地在随机测试集上重新训练并评估模型，否则我们的估计会极度乐观。我们应当改用 k 折交叉验证或嵌套交叉验证。

性能不令人满意可能有许多不同的原因：

- 我们的数据是有偏的（skewed）
- 噪声太多
- 离群点太多
- 我们的特征信息量不够
- 训练样本不足

简而言之：我们的算法要么受高方差（过拟合）困扰，要么受高偏差（欠拟合）困扰。

![](https://sebastianraschka.com/images/faq/ml-solvable/bias-variance.png)

通过绘制"学习曲线"（learning curves）来更好地把握我们的问题，可能会有所帮助。

例如，这里我绘制了一个模型的平均准确率（使用 10 折交叉验证）。蓝线（训练准确率）表示在各训练折上的平均准确率，绿线表示在不同初始训练集规模下测试折上的平均准确率。

![](https://sebastianraschka.com/images/faq/ml-solvable/learning_curve.png)

类似地，我们还可以评估模型在特定调优参数下的性能（这里我绘制了 C 的不同取值，即 SVM 的正则化强度倒数参数）。

![](https://sebastianraschka.com/images/faq/ml-solvable/param_curve.png)
