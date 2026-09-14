---
title: "逻辑回归有解析解吗？"
title_en: "Does Logistic Regression Have an Analytical Solution?"
source: https://sebastianraschka.com/faq/docs/logistic-analytical.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 逻辑回归有解析解吗？

很遗憾，最大化对数似然（或最小化其相反数，即逻辑代价函数）没有闭式解；至少目前还没有找到。

有一个例外情况是你只有 2 个观测值，另外还有这篇论文

*Lipovetsky, Stan. ["Analytical closed-form solution for binary logit regression by categorical predictors."](http://www.tandfonline.com/doi/abs/10.1080/02664763.2014.932760) Journal of Applied Statistics 42.1 (2015): 37-49.（基于类别型预测变量的二项 logit 回归的解析闭式解）*

它"表明对于类别型解释变量，可以用解析闭式公式给出解"。

问题在于逻辑 sigmoid 函数是非线性的——而在线性回归中，你假设的是相互独立的高斯噪声。
