---
title: "Data-Centric AI vs. Model-Centric Machine Learning"
source: https://sebastianraschka.com/faq/docs/data-centric-ai.html
crawled: 2026-09-06
---

# Data-Centric AI vs. Model-Centric Machine Learning

Data-centric AI is a paradigm or workflow where we keep the model training procedure fixed and iterate over the dataset to improve the predictive performance of a model.

In the context of data-centric AI, we can think of the conventional workflow, which is often part of academic publishing, as model-centric AI. However, in an academic research setting, we are typically interested in developing new methods (for example, neural network architectures or loss functions). Here, we consider existing benchmark datasets to compare the new method to previous approaches to determine whether it is an improvement over the status quo.

**Why can’t we have both?**

In short, data-centric AI focuses on changing the data to improve performance. Model-centric approaches focus on modifying the model to improve performance. Ideally, we can do both in an applied setting where we want to get the best possible predictive performance. However, if we are in a research setting or an exploratory stage of an applied project, varying too many variables simultaneously is messy. If we change both model and data simultaneously, it is hard to pinpoint which change is responsible for the improvement.

**How do we decide if data-centric AI is the right fit?**

Taking a data-centric approach is often a good idea in an applied project where we want to improve the predictive performance to solve a particular problem. It makes sense to start with a modeling baseline and improve the dataset since it can often be more worthwhile than trying out bigger, more expensive models.

If our task is to develop a new or better methodology, such as a new neural network architecture or loss function, then a model-centric approach might be a better choice. Using an established benchmark dataset, and not changing it, will make it easier to compare the new modeling approach to previous work.

In a real-world project, alternating between data-centric and model-centric modes makes a lot of sense. Early on, investing more in data quality makes sense because it will benefit all models. Then, once a good dataset is available, it makes sense to hone in on the model tuning part, to improve performance.

---

**This is an abbreviated answer and excerpt from my book [Machine Learning Q and AI](https://leanpub.com/machine-learning-q-and-ai/), which contains a more verbose version with additional illustrations.**
