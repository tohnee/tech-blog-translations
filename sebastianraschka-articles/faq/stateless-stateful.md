---
title: "What is the difference between stateful and stateless training?"
source: https://sebastianraschka.com/faq/docs/stateless-stateful.html
crawled: 2026-09-06
---

# What is the difference between stateful and stateless training?

Both stateless training and stateful training refer to different ways of training a production model.

**Stateless (re)training**

Stateless training is a conventional, traditional approach where we first train an initial model on the original training set and then retrain it as new data arrives. Hence, stateless training is also commonly referred to as stateless *retraining*

**Stateful training**

In stateful training, we train the model on an initial batch of data and then update it periodically (as opposed to retraining it) when new data arrives.

![](https://sebastianraschka.com/images/faq/stateless-stateful/stateless-stateful.png)
