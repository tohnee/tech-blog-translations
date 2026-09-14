---
title: "如何将 SVM 应用于类别型数据？"
title_en: "How can I apply an SVM to categorical data?"
source: https://sebastianraschka.com/faq/docs/svm_for_categorical_data.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 如何将 SVM 应用于类别型数据？

我假设你问的是类别型特征，而不是目标变量——在 SVM 分类器中，目标变量本来就默认是类别型的（二分类）。

首先，类别型特征有两个子类型：序数（ordinal）特征和名义（nominal）特征。

序数意味着隐含一种「顺序」。例如，客户满意度指标 {'satisfied'（满意）、'neutral'（中性）、'dissatisfied'（不满意）} 就是一个序数变量，因为我们可以对其排序：'satisfied' > 'neutral' > 'dissatisfied'。这时，我们可以直接把「字符串」表示映射为整数表示，例如 'satisfied'=1、'neutral'=0、'dissatisfied'=-1。

如果变量是*名义*变量，那么「顺序」就没有意义了。例如「颜色」；在图像处理的某些场景下对颜色值排序是有意义的，但简单起见，我们无法说 'red > blue > yellow' 之类的话。要在 SVM 分类中处理这类变量，我们通常做「one-hot」编码。也就是创建所谓的哑变量（dummy variable），其取值为二值——我们为该名义特征变量的每一个可能取值创建一个哑变量。假设我们的颜色变量可以取 'red'、'blue'、'yellow' 三个值之一。再假设我们有如下由 4 个训练样本组成的数据集：

- sample 1: 'blue'
- sample 2: 'yellow'
- sample 3: 'red'
- sample 4: 'yellow'

那么 one-hot 编码的结果如下：

![](https://sebastianraschka.com/images/faq/svm_for_categorical_data/onehot-color.png)

注意每一行中只有一个「真」值（整数 1），它标明了该样本在训练集中对应的列。样本 1 是蓝色；样本 2 是黄色，依此类推。
