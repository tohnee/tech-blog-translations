---
title: "Unlocking High-Accuracy Differentially Private Image Classification through Scale"
source: https://deepmind.google/blog/unlocking-high-accuracy-differentially-private-image-classification-through-scale/
site: deepmind
date: 2022-06-17
authors: Soham De, Leonard Berrada, Jamie Hayes, Samuel L. Smith, Borja Balle
crawled: 2026-09-13
---

A recent [DeepMind paper](https://arxiv.org/abs/2112.04359) on the ethical and social risks of language models identified large language models [leaking sensitive information](https://www.usenix.org/conference/usenixsecurity21/presentation/carlini-extracting) about their training data as a potential risk that organisations working on these models have the responsibility to address. Another [recent paper](https://arxiv.org/abs/2201.04845) shows that similar privacy risks can also arise in standard image classification models: a fingerprint of each individual training image can be found embedded in the model parameters, and malicious parties could exploit such fingerprints to reconstruct the training data from the model.

Privacy-enhancing technologies like differential privacy (DP) can be deployed at training time to mitigate these risks, but they often incur significant reduction in model performance. In this work, we make substantial progress towards unlocking high-accuracy training of image classification models under differential privacy.

![Diagram illustrating privacy risks in machine learning models, showing text memorization in GPT-2 on the left and successful training image reconstructions from standard image classification models on the right.](https://lh3.googleusercontent.com/EE-e4w3q5sqP90b5wMttB0k5SW6fiJ-9xEp6lBcGYglzX-7gIyhq5x3GOXEOHf9derEkSjSQY4TrF_lPmCnBat79uetL5p7ta5KZFJQF9j840EdN2dg=w1440)

Figure 1: (left) Illustration of training data leakage in GPT-2 [credit: Carlini et al. "Extracting Training Data from Large Language Models", 2021]. (right) CIFAR-10 training examples reconstructed from a 100K parameter convolutional neural network [credit: Balle et al. "Reconstructing Training Data with Informed Adversaries", 2022]

Differential privacy was [proposed](https://link.springer.com/content/pdf/10.1007/11681878_14.pdf) as a mathematical framework to capture the requirement of protecting individual records in the course of statistical data analysis (including the training of machine learning models). DP algorithms protect individuals from any inferences about the features that make them unique (including complete or partial reconstruction) by injecting carefully calibrated noise during the computation of the desired statistic or model. Using DP algorithms provides robust and rigorous privacy guarantees both in theory and in practice, and has become a de-facto gold standard adopted by a number of [public](https://dl.acm.org/doi/10.1145/3219819.3226070) and [private](https://ai.googleblog.com/2022/02/federated-learning-with-formal.html) organisations.

The most popular DP algorithm for deep learning is differentially private stochastic gradient descent (DP-SGD), a modification of standard SGD obtained by clipping gradients of individual examples and adding enough noise to mask the contribution of any individual to each model update:

![Diagram illustrating the Differentially Private Stochastic Gradient Descent (DP-SGD) training loop: training data is passed to a model to compute gradients for each example, which are clipped, averaged, combined with added noise to create a privatised gradient, and then used to update model parameters.](https://lh3.googleusercontent.com/jPzWgyDsXg_xXncwyZZhqKWrH39Seck6BVmdLyT6nbIMKjdBiFwpkXXHFh8b_rtvPpISyzu7smCRg_-5gtG21Ax_Uzaabf-Xx6JXcFtw60zKGbwpRQ=w1440)

Figure 2: Illustration of how DP-SGD processes gradients of individual examples and adds noise to produce model updates with privatised gradients.

Unfortunately, prior works have found that in practice, the privacy protection provided by DP-SGD often comes at the cost of significantly less accurate models, which presents a major obstacle to the widespread adoption of differential privacy in the machine learning community. According to empirical evidence from prior works, this utility degradation in DP-SGD becomes more severe on larger neural network models – including the ones regularly used to achieve the best performance on challenging image classification benchmarks.

Our work investigates this phenomenon and proposes a series of simple modifications to both the training procedure and model architecture, yielding a significant improvement on the accuracy of DP training on standard image classification benchmarks. The most striking observation coming out of our research is that DP-SGD can be used to efficiently train much deeper models than previously thought, as long as one ensures the model's gradients are well-behaved. We believe the substantial jump in performance achieved by our research has the potential to unlock practical applications of image classification models trained with formal privacy guarantees.

The figure below summarises two of our main results: an ~10% improvement on CIFAR-10 compared to previous work when privately training without additional data, and a top-1 accuracy of 86.7% on ImageNet when privately fine-tuning a model pre-trained on a different dataset, almost closing the gap with the best non-private performance.

![Two bar charts showing the paper's results at ε=8. On CIFAR-10 without extra data, "Ours" achieves 81.4% top-1 accuracy compared to the "Previous Best Result" of 71.7%. On ImageNet fine-tuning, "Ours" achieves 86.7% top-1 accuracy, nearing the non-private State-Of-The-Art (SOTA) level of 91%.](https://lh3.googleusercontent.com/lsVsbIezoFPBKTvpRzIFU3sxI8g_ajbrzqaR2WbpBukTBuYkFS0_pC6mBC3OOTM4E55R7M4pg_s7NZTUO7seK-x5-54axMx8MqW9oCxzyhzCcWLeCQ=w1440)

Figure 3: (left) Our best results on training WideResNet models on CIFAR-10 without additional data. (right) Our best results on fine-tuning NFNet models on ImageNet. The best performing model was pre-trained on an internal dataset disjoint from ImageNet.

These results are achieved at ε=8, a standard setting for calibrating the strength of the protection offered by differential privacy in machine learning applications. We refer to the paper for a discussion of this parameter, as well as additional experimental results at other values of ε and also on other datasets. Together with the paper, we are also open-sourcing our implementation to enable other researchers to verify our findings and build on them. We hope this contribution will help others interested in making practical DP training a reality.

Download our JAX implementation [on GitHub](https://github.com/deepmind/jax_privacy).
