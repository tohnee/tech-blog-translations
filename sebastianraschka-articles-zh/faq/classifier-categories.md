---
title: "分类器有哪些大的类别？"
title_en: "What are the broad categories of classifiers?"
source: https://sebastianraschka.com/faq/docs/classifier-categories.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 分类器有哪些大的类别？

> 原文：[What are the broad categories of classifiers?](https://sebastianraschka.com/faq/docs/classifier-categories.html) · Sebastian Raschka's FAQ

## 一种（宽泛的）分类方式是「判别式」vs.「生成式」分类器：

判别式（discriminative）算法：

- 从 x 到 y 的直接映射
- 直觉理解：「区分说不同语言的人，但并不真正学会那些语言」
- 例如：逻辑回归、SVM、神经网络、……

生成式（generative）算法：

- 对数据的生成过程进行建模（联合概率分布 p(x, y)）
- 例如：朴素贝叶斯、贝叶斯信念网络、受限玻尔兹曼机

## 或者，我们可以把分类器分为「惰性」vs.「急切」学习器：

惰性（lazy）学习器：

- 不「学习」决策规则（或函数）
- 不涉及学习步骤，但需要保留训练数据
- 例如：K 近邻分类器

## 第三种分法是「参数化」vs.「非参数化」

（这里是在机器学习的语境下；统计学领域对这些术语的用法略有不同。）

非参数化（non-parametric）：

- 表示的规模随训练数据大小而增长
- 例如：决策树、K 近邻

参数化（parametric）：

- 表示是「固定的」
- 例如：大多数线性分类器，如逻辑回归等

## Pedro Domingo 的机器学习五大流派

Pedro Domingo 在他的新书（[The Master Algorithm](https://www.amazon.com/Master-Algorithm-Ultimate-Learning-Machine/dp/0465065708/ref=sr_1_1?ie=UTF8&qid=1447045562&sr=8-1&keywords=pedro+domingos)）中提到了机器学习的五大流派，这是另一种不错的分类方式。以下是对该书内容的概括（第 51-53 页）：

**符号派（Symbolists）**

- 操纵符号（就像数学家用表达式替换表达式一样），或者换句话说，利用已有知识来填补缺失的部分
- 「终极算法」：逆演绎（inverse deduction）

**联结派（Connectionists）**

- 对生物大脑进行逆向工程，即增强神经元之间的连接
- 「终极算法」：反向传播

**进化派（Evolutionaries）**

- 如果说联结主义是对大脑的精调，那么进化就是创造大脑
- 「终极算法」：遗传编程

**贝叶斯派（Bayesians）**

- 基于概率推断，即融入先验知识：某些结果更有可能发生
- 「终极算法」：贝叶斯定理及其衍生

**类推派（Analogizers）**

- 从相似性出发进行泛化，即识别相似之处，或者换句话说：记住经验（训练数据）以及如何组合它们来做出新预测
- 「终极算法」：支持向量机

![](https://sebastianraschka.com/images/faq/classifier_categories/master_chart.jpg)
