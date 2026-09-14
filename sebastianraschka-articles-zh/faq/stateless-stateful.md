---
title: "有状态训练与无状态训练有什么区别？"
title_en: "What is the difference between stateful and stateless training?"
source: https://sebastianraschka.com/faq/docs/stateless-stateful.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 有状态训练与无状态训练有什么区别？

无状态训练与有状态训练指的是训练生产模型的两种不同方式。

**无状态（重新）训练**

无状态训练是一种常规的、传统的方法：我们首先在原始训练集上训练一个初始模型，然后随着新数据的到来对它重新训练。因此，无状态训练通常也被称为无状态*重新训练*（retraining）。

**有状态训练**

在有状态训练中，我们在初始的一批数据上训练模型，然后在新数据到来时定期更新它（而不是重新训练它）。

![](https://sebastianraschka.com/images/faq/stateless-stateful/stateless-stateful.png)
