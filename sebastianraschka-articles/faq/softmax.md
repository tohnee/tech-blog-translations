---
title: "Softmax and Multinomial Logistic Loss Explained"
source: https://sebastianraschka.com/faq/docs/softmax.html
crawled: 2026-09-06
---

# Softmax and Multinomial Logistic Loss Explained

The softmax function is simply a generalization of the logistic function that allows us to compute meaningful class-probabilities in multi-class settings (multinomial logistic regression). In softmax, we compute the probability that a particular sample (with net input z) belongs to the *i*th class using a normalization term in the denominator that is the sum of all *M* linear functions:

![](https://sebastianraschka.com/images/faq/softmax/softmax_1.png)

In contrast, the logistic function:

![](https://sebastianraschka.com/images/faq/softmax/logistic.png)

And for completeness, we define the net input as

![](https://sebastianraschka.com/images/faq/softmax/net_input.png)

where the weight coefficients of your model are stored as vector “w” and “x” is the feature vector of your sample.
