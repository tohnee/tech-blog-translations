---
title: "Few-Shot Learning vs. Conventional Supervised Learning"
source: https://sebastianraschka.com/faq/docs/few-shot.html
crawled: 2026-09-06
---

# Few-Shot Learning vs. Conventional Supervised Learning

Few-shot learning is a flavor of supervised learning for small training sets with a very small example-to-class ratio. In regular supervised learning, we train models by iterating over a training set where the model always sees a fixed set of classes. In few-shot learning, we are working on a support set from which we create multiple training tasks to assemble training episodes where each training task consists of different classes.

In supervised learning, we fit a model on a training dataset and evaluate it on a test dataset. Typically, the training set contains a relatively large number of examples per class. For example, in supervised learning context, a tiny dataset is the the Iris dataset with 50 examples per class. For deep learning model, even datasets like MNIST with 5k training examples per class is considered as very small.

In few-shot learning, the number of examples per class is much smaller. We typically use the term *N*-way *K*-shot where *N* stands for the number of classes, and K stands for the number of examples per class. The most common values are *K=1* or *K=5*. For instance, in a 5-way 1-shot problem, we have 5 classes with only 1 example each.

![](https://sebastianraschka.com/images/faq/few-shot/few-shot-1.png)

Rather than fitting the model to the training dataset, we can think of few-shot learning as “learning to learn.” In contrast to supervised learning, we don’t have a training dataset but a so-called support set. From the support set, we sample training tasks that mimic the use-case scenario during prediction. For example, for 3-way 1-shot learning, a training task consists of 3 classes with 1 example each. With each training task comes a query image that is to be classified. The model is trained on several training tasks from the support set; this is called an episode.

Then, during testing, the model receives a new task with classes that are different from those seen during training. Again, the task is to classify the query images. Test tasks are similar to training tasks, except that none of the classes during testing overlap with those encountered during training.

![](https://sebastianraschka.com/images/faq/few-shot/few-shot-2.png)

---

**This is an abbreviated answer and excerpt from my book [Machine Learning Q and AI](https://leanpub.com/machine-learning-q-and-ai/), which contains a more verbose version with additional illustrations.**
