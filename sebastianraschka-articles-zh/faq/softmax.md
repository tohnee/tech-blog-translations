---
title: "softmax 与多项 logistic 损失详解"
title_en: "Softmax and Multinomial Logistic Loss Explained"
source: https://sebastianraschka.com/faq/docs/softmax.html
crawled: 2026-09-06
translated: 2026-09-14
---

# softmax 与多项 logistic 损失详解

softmax 函数其实就是 logistic 函数的一种推广，使我们在多分类场景（多项 logistic 回归）中也能计算出有意义的类别概率。在 softmax 中，我们用一个归一化项——即所有 *M* 个线性函数之和——作为分母，来计算某个特定样本（净输入为 z）属于第 *i* 类的概率：

![](https://sebastianraschka.com/images/faq/softmax/softmax_1.png)

作为对比，logistic 函数为：

![](https://sebastianraschka.com/images/faq/softmax/logistic.png)

为完整起见，我们将净输入定义为

![](https://sebastianraschka.com/images/faq/softmax/net_input.png)

其中模型的权重系数存储为向量 "w"，而 "x" 是样本的特征向量。
