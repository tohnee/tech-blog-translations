---
title: "逻辑回归——为什么用 sigmoid 函数？"
title_en: "Logistic Regression -- Why sigmoid function?"
source: https://sebastianraschka.com/faq/docs/logistic-why-sigmoid.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 逻辑回归——为什么用 sigmoid 函数？

逻辑回归的一个很好的性质在于：sigmoid 函数输出的是预测的条件概率，即类别概率。这是怎么做到的呢？
我们先从所谓的「几率」（odds ratio）*p / (1 - p)* 说起，它描述的是某个我们关心的正事件发生的概率与它不发生的概率之比——这里的「正」指的是「我们想要预测的事件」，即 *p(y=1 | x)*。

（注意，逻辑回归使用的是 sigmoid 函数中的一个特例——逻辑 sigmoid；其他 sigmoid 函数也是存在的，比如双曲正切函数。）

![](https://sebastianraschka.com/images/faq/logistic-why-sigmoid/1.png)

于是，正事件发生的可能性越大，几率也就越大。
现在，如果我们对这个几率取自然对数，也就是所谓的对数几率（log-odds）或 logit 函数，就会得到下式

![](https://sebastianraschka.com/images/faq/logistic-why-sigmoid/2.png)

![](https://sebastianraschka.com/images/faq/logistic-why-sigmoid/3.png)

接下来，我们用这个*对数变换*来建模解释变量与目标变量之间的关系：

![](https://sebastianraschka.com/images/faq/logistic-why-sigmoid/4.png)

|  |  |
| --- | --- |
| 现在，请记住我们并不是想预测上面等式的右边部分，因为我们真正感兴趣的是 \*p(y=1 | x)\*。所以，让我们对这个 logit 函数取逆……瞧，我们就得到了逻辑 sigmoid： |

![](https://sebastianraschka.com/images/faq/logistic-why-sigmoid/5.png)

|  |  |
| --- | --- |
| 它可以从输入中返回类别概率 \*p(y=1 | x)\* |

![](https://sebastianraschka.com/images/faq/logistic-why-sigmoid/6.png)

![](https://sebastianraschka.com/images/faq/logistic-why-sigmoid/7.png)
