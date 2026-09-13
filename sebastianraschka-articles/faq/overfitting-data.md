---
title: "Reducing Overfitting with Data"
source: https://sebastianraschka.com/faq/docs/overfitting-data.html
crawled: 2026-09-06
---

# Reducing Overfitting with Data

**Collecting more data**

One of the best ways to reduce overfitting is to collect more (good-quality) data. How do we know that more data is beneficial for minimizing overfitting? We can plot learning curves to find out. To construct a learning curve, we train the model to different sizes of the training set (10%, 20%, etc.) and evaluate the trained model on the same fixed-size validation or test set.

**Data augmentation**

Data augmentation refers to generating new data records or features based on existing data. It allows for the expansion of a dataset without additional data collection.

Data augmentation allows us to create different versions of the original input data, which can improve the model’s generalization performance. Why? Augmented data can help the model to generalize better since it makes it harder to memorize spurious information via training examples or features (or exact pixel values for specific pixel locations in the case of image data).

Data augmentation is usually standard for image data and text data, but data augmentation methods for tabular data exist, too [ref1, ref2].

- [ref1] The GReaT method generates synthetic tabular data using an auto-regressive generative large language model. Reference: Borisov, Seßler, Leemann, Pawelczyk, Kasneci, (2022). *Language Models Are Realistic Tabular Data Generators.* <https://arxiv.org/abs/2210.06280>.
- [ref2] TabDDPM is a method for generating synthetic tabular data using a diffusion model. Kotelnikov, Baranchuk, Rubachev, Babenko (2022). *TabDDPM: Modelling Tabular Data with Diffusion Models.* <https://arxiv.org/abs/2209.15421>.

**Pretraining**

Self-supervised learning lets us leverage large, unlabeled datasets to pretrain neural networks. This can help reduce overfitting on the smaller target datasets.

As an alternative to self-supervised learning, traditional transfer learning on large labeled datasets are also an option. Transfer learning is most effective if the labeled dataset is closely related to the target domain. For instance, if we train a model to classify bird species, we can pretrain a network on a large, general animal classification dataset. However, if such a large animal classification dataset is unavailable, we can also pretrain the model on the relatively broad ImageNet dataset.

The dataset may be extremely small and unsuitable for supervised learning, for example, if there are only a handful of labeled examples per class. If our classifier needs to operate in a context where the collection of additional labeled data is not feasible, we may also consider few-shot learning.

**Other methods**

The list above covers the main approaches of using and modifying the dataset to reduce overfitting. However, the list above is not meant to be exhaustive. Other common techniques include

- feature engineering and normalization;
- the inclusion of adversarial examples and label or feature noise;
- label smoothing;
- smaller batch sizes;
- data augmentation techniques such as Mix-Up, Cut-Out, and Cut-Mix.

---

**This is an abbreviated answer and excerpt from my book [Machine Learning Q and AI](https://leanpub.com/machine-learning-q-and-ai/), which contains a more verbose version with additional illustrations.**
