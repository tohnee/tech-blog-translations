---
title: "多分类任务最好的验证指标是什么？"
title_en: "What is the best validation metric for multi-class classification?"
source: https://sebastianraschka.com/faq/docs/multiclass-metric.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 多分类任务最好的验证指标是什么？

这真的取决于我们的"目标"和数据集。如果类别标签是均匀分布的，分类准确率（或误分类错误率）就是合理的选择。更好的做法是计算 ROC 曲线下面积（即便是多分类系统也可以），例如可以看看那篇很不错的关于 ROC 分析的 [ICML'04 教程](http://www.cs.bris.ac.uk/~flach/ICML04tutorial/)。
类似地，我们可以把精确率（precision）、召回率（recall）和 F1 分数（F1-score）等所有二分类性能指标推广到多分类场景。在二分类情形下，我们有

![](https://sebastianraschka.com/images/faq/multiclass-metric/conf_mat.png)

![](https://sebastianraschka.com/images/faq/multiclass-metric/pre-rec.png)

![](https://sebastianraschka.com/images/faq/multiclass-metric/mcc.png)

（PRE=精确率，REC=召回率，F1=F1 分数，MCC=Matthews 相关系数）
要把它推广到多分类，假设我们有一个一对其余（One-vs-All，OvA）分类器，我们可以采用"微"平均（micro）或"宏"平均（macro）。在"微平均"中，我们用这个 k 类模型的各类真阳性、真阴性、假阳性和假阴性来计算性能，例如精确率：

![](https://sebastianraschka.com/images/faq/multiclass-metric/micro.png)

而在宏平均中，我们对每个单独类别的性能取平均：

![](https://sebastianraschka.com/images/faq/multiclass-metric/macro.png)
