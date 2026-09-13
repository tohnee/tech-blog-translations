---
title: "Introduction to Deep Learning"
source: https://sebastianraschka.com/blog/2021/dl-course.html
crawled: 2026-09-06
---

# Introduction to Deep Learning

I just sat down this morning and organized all deep learning related videos I recorded in 2021. I am sure this will be a useful reference for my future self, but I am also hoping it might be useful for one or the other person out there.

PS: All code examples are in PyTorch :)

## Part 1: Introduction

### L01: Introduction to deep learning

|  | Videos | Material |
| --- | --- | --- |
| 1 | [🎥 L1.0 Introduction (04:26)](https://www.youtube.com/watch?v=1nqCZqDYPp0) | 📝 [L01-intro\_slides.pdf](https://sebastianraschka.com/pdf/lecture-notes/stat453ss21/L01-intro_slides.pdf) |
| 2 | [🎥 L1.1.1 Course Overview Part 1: Motivation and Topics (16:26)](https://www.youtube.com/watch?v=6VbtJ9nn5ng) |  |
| 3 | [🎥 L1.1.2 Course Overview Part 2: Organization (17:34)](https://www.youtube.com/watch?v=s7ZCbKI5Exw) |  |
| 4 | [🎥 L1.2 What is Machine Learning? (17:42)](https://www.youtube.com/watch?v=d6oQzE4kst0) |  |
| 5 | [🎥 L1.3.1 Broad Categories of ML Part 1: Supervised Learning (10:55)](https://www.youtube.com/watch?v=UadzJLHJB50) |  |
| 6 | [🎥 L1.3.2 Broad Categories of ML Part 2: Unsupervised Learning (7:29)](https://www.youtube.com/watch?v=nHhuuUwd05g) |  |
| 7 | [🎥 L1.3.3 Broad Categories of ML Part 3: Reinforcement Learning (3:48)](https://www.youtube.com/watch?v=EQCZUOxGrOo) |  |
| 8 | [🎥 L1.3.4 Broad Categories of ML Part 4: Special Cases of Supervised Learning (10:46)](https://www.youtube.com/watch?v=B59lK5yo57M) |  |
| 9 | [🎥 L1.4 The Supervised Learning Workflow (17:46)](https://www.youtube.com/watch?v=nd9dhrvtIA0) |  |
| 10 | [🎥 L1.5 Necessary Machine Learning Notation and Jargon (22:02)](https://www.youtube.com/watch?v=o-yHLOvuh2o) |  |
| 11 | [🎥 L1.6 About the Practical Aspects and Tools Used in This Course (11:26)](https://www.youtube.com/watch?v=R16VmI2ZhR0) |  |
| 12 | [🎥 Deep Learning News #1 (15:28)](https://www.youtube.com/watch?v=UAjfVRicYBM) | 📝 [stuff-in-the-news-01.pdf](https://sebastianraschka.com/pdf/lecture-notes/stuff-in-the-news/stuff-in-the-news-01.pdf) |

### L02: The brief history of deep learning

|  | Videos | Material |
| --- | --- | --- |
| 13 | [🎥 L2.0 A Brief History of Deep Learning – Lecture Overview (02:57)](https://www.youtube.com/watch?v=Ezig00nypvU) | 📝 [L02\_dl-history\_slides.pdf](https://sebastianraschka.com/pdf/lecture-notes/stat453ss21/L02_dl-history_slides.pdf) |
| 14 | [🎥 L2.1 Artificial Neurons (16:49)](https://www.youtube.com/watch?v=gbLasjwAGik) |  |
| 15 | [🎥 L2.2 Multilayer Networks (15:11)](https://www.youtube.com/watch?v=G7oqVqU5qsQ) |  |
| 16 | [🎥 L2.3 The Origins of Deep Learning (20:11)](https://www.youtube.com/watch?v=tkUCMtJd43Y) |  |
| 17 | [🎥 L2.4 The Deep Learning Hardware & Software Landscape (7:20)](https://www.youtube.com/watch?v=TMCNkeJGIfg) |  |
| 18 | [🎥 L2.5 Current Trends in Deep Learning (8:21)](https://www.youtube.com/watch?v=FpOpb-BMIH8) |  |

### L03: Single-layer neural networks: The perceptron algorithm

|  | Videos | Material |
| --- | --- | --- |
| 19 | [🎥 L3.0 Perceptron Lecture Overview (05:02)](https://www.youtube.com/watch?v=cm_wv2QpTgc) | 📝 [L03\_perceptron\_slides.pdf](https://sebastianraschka.com/pdf/lecture-notes/stat453ss21/L03_perceptron_slides.pdf) |
| 20 | [🎥 L3.1 About Brains and Neurons (12:50)](https://www.youtube.com/watch?v=AnSDPcvtRLo) |  |
| 21 | [🎥 L3.2 The Perceptron Learning Rule (31:38)](https://www.youtube.com/watch?v=C8Uns9HEVXI) | [🎮 perceptron-animation.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L03/code/perceptron-animation.ipynb) |
| 22 | [🎥 L3.3 Vectorization in Python (14:54)](https://www.youtube.com/watch?v=OnG2NfuC5aY) | [🎮 vectorization-example.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L03/code/vectorization-example.ipynb) |
| 23 | [🎥 L3.4 Perceptron in Python using NumPy and PyTorch (28:42)](https://www.youtube.com/watch?v=TlGpIKMVoOg) | [🎮 perceptron-numpy.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L03/code/perceptron-numpy.ipynb)    [🎮 perceptron-pytorch.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L03/code/perceptron-pytorch.ipynb) |
| 24 | [🎥 L3.5 The Geometric Intuition Behind the Perceptron (18:43)](https://www.youtube.com/watch?v=Fj7BgxI73TA) |  |
| 25 | [🎥 L3.6 Deep Learning News #2 (25:01)](https://www.youtube.com/watch?v=TgbI3LeB1bg) | 📝 [stuff-in-the-news-02.pdf](https://sebastianraschka.com/pdf/lecture-notes/stuff-in-the-news/stuff-in-the-news-02.pdf) |

## Part 2: Mathematical and computational foundations

### L04: Linear algebra and calculus for deep learning

|  | Videos | Material |
| --- | --- | --- |
| 26 | [🎥 L4.0 Linear Algebra for Deep Learning – Lecture Overview (02:11)](https://www.youtube.com/watch?v=3mjJxu3B0zA) | 📝 [L04\_linalg-dl\_slides.pdf](https://sebastianraschka.com/pdf/lecture-notes/stat453ss21/L04_linalg-dl_slides.pdf) |
| 27 | [🎥 L4.1 Tensors in Deep Learning (13:02)](https://www.youtube.com/watch?v=JXfDlgrfOBY) |  |
| 28 | [🎥 L4.2 Tensors in PyTorch (28:32)](https://www.youtube.com/watch?v=zk_asBov8QI) |  |
| 29 | [🎥 L4.3 Vectors, Matrices, and Broadcasting (16:15)](https://www.youtube.com/watch?v=4Ehb_is-MFU) |  |
| 30 | [🎥 L4.4 Notational Conventions for Neural Networks (11:52)](https://www.youtube.com/watch?v=4pnoymfFiYM) |  |
| 31 | [🎥 L4.5 A Fully Connected (Linear) Layer in PyTorch (12:41)](https://www.youtube.com/watch?v=XswEBzNgIYc) |  |

### L05: Parameter optimization with gradient descent

|  | Videos | Material |
| --- | --- | --- |
| 32 | [🎥 L5.0 Gradient Descent – Lecture Overview (06:28)](https://www.youtube.com/watch?v=VBOxg62CwCg) | 📝 [L05\_gradient-descent\_slides.pdf](https://sebastianraschka.com/pdf/lecture-notes/stat453ss21/L05_gradient-descent_slides.pdf) |
| 33 | [🎥 L5.1 Online, Batch, and Minibatch Mode (21:04)](https://www.youtube.com/watch?v=b4DXHd3RwqA) |  |
| 34 | [🎥 L5.2 Relation Between Perceptron and Linear Regression (05:20)](https://www.youtube.com/watch?v=4JB1j8eIGzI) |  |
| 35 | [🎥 L5.3 An Iterative Training Algorithm for Linear Regression (11:10)](https://www.youtube.com/watch?v=1QH2bVuV98A) |  |
| 36 | [🎥 L5.4 (Optional) Calculus Refresher I: Derivatives (17:36)](https://www.youtube.com/watch?v=tL1THESrXgI) |  |
| 37 | [🎥 L5.5 (Optional) Calculus Refresher II: Gradients (17:34)](https://www.youtube.com/watch?v=YPZVGSRmjLk) |  |
| 38 | [🎥 L5.6 Understanding Gradient Descent (26:34)](https://www.youtube.com/watch?v=L4xzybIa-bo) |  |
| 39 | [🎥 L5.7 Training an Adaptive Linear Neuron (Adaline) (06:43)](https://www.youtube.com/watch?v=iLCT0i-lCsw) |  |
| 40 | [🎥 L5.8 Adaline Code Example (33:26)](https://www.youtube.com/watch?v=GGcaqzhKzLc) | [🎮 linear-regr-gd.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L05/code/linear-regr-gd.ipynb)    [🎮 adaline-sgd.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L05/code/adaline-sgd.ipynb) |
| 41 | [🎥 Deep Learning News #3 (20:24)](https://www.youtube.com/watch?v=2I8SqKLt-Nk) | 📝 [stuff-in-the-news-03.pdf](https://sebastianraschka.com/pdf/lecture-notes/stuff-in-the-news/stuff-in-the-news-03.pdf) |

### L06: Automatic differentiation with PyTorch

|  | Videos | Material |
| --- | --- | --- |
| 42 | [🎥 L6.0 Automatic Differentiation in PyTorch – Lecture Overview (04:09)](https://www.youtube.com/watch?v=j1-r1vO2a_o) | 📝 [L06\_pytorch\_slides.pdf](https://sebastianraschka.com/pdf/lecture-notes/stat453ss21/L06_pytorch_slides.pdf) |
| 43 | [🎥 L6.1 Learning More About PyTorch (15:47)](https://www.youtube.com/watch?v=LjdiVPQ45GE) |  |
| 44 | [🎥 L6.2 Understanding Automatic Differentiation via Computation Graphs (22:47)](https://www.youtube.com/watch?v=oY6-i2Ybin4) |  |
| 45 | [🎥 L6.3 Automatic Differentiation in PyTorch (09:02)](https://www.youtube.com/watch?v=VvUz0Q9e09g) | [🎮 pytorch-autograd.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L06/code/pytorch-autograd.ipynb) |
| 46 | [🎥 L6.4 Training ADALINE with PyTorch (23:29)](https://www.youtube.com/watch?v=00KgeJwNaZA) | [🎮 adaline-with-autograd.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L06/code/adaline-with-autograd.ipynb) |
| 47 | [🎥 L6.5 A Closer Look at the PyTorch API (25:02)](https://www.youtube.com/watch?v=klc79sZ1yVc) |  |

### L07: Cluster and cloud computing resources

|  | Videos | Material |
| --- | --- | --- |
| 48 | [🎥 L7.0 GPU resources & Google Colab (19:17)](https://www.youtube.com/watch?v=5pew4YEa1ww) | 📝 [L07\_cloud-computing\_slides.pdf](https://sebastianraschka.com/pdf/lecture-notes/stat453ss21/L07_cloud-computing_slides.pdf)  List of cloud resources: <https://github.com/zszazi/Deep-learning-in-cloud> |
| 49 | [🎥 Deep Learning News #4 (28:09)](https://www.youtube.com/watch?v=mPC14fIO4SY) | 📝 [stuff-in-the-news-04.pdf](https://sebastianraschka.com/pdf/lecture-notes/stuff-in-the-news/stuff-in-the-news-04.pdf) |

## Part 3: Introduction to neural networks

### L08: Multinomial logistic regression / Softmax regression

|  | Videos | Material |
| --- | --- | --- |
| 50 | [🎥 L8.0 Logistic Regression – Lecture Overview (06:28)](https://www.youtube.com/watch?v=10PTpRRpRk0) | 📝 [L08\_logistic\_\_slides.pdf](https://sebastianraschka.com/pdf/lecture-notes/stat453ss21/L08_logistic__slides.pdf) |
| 51 | [🎥 L8.1 Logistic Regression as a Single-Layer Neural Network (09:15)](https://www.youtube.com/watch?v=ncZ5iSZekVQ) |  |
| 52 | [🎥 L8.2 Logistic Regression Loss Function (12:57)](https://www.youtube.com/watch?v=GxJe0DZvydM) |  |
| 53 | [🎥 L8.3 Logistic Regression Loss Derivative and Training (19:57)](https://www.youtube.com/watch?v=7rR1L7t2EnA) |  |
| 54 | [🎥 L8.4 Logits and Cross Entropy (06:47)](https://www.youtube.com/watch?v=icQaFxKa_J0) |  |
| 55 | [🎥 L8.5 Logistic Regression in PyTorch – Code Example (19:02)](https://www.youtube.com/watch?v=6igMArA6k3A) | [🎮 logistic-regression.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L08/code/logistic-regression.ipynb) |
| 56 | [🎥 L8.6 Multinomial Logistic Regression / Softmax Regression (17:31)](https://www.youtube.com/watch?v=L0FU8NFpx4E) |  |
| 57 | [🎥 L8.7.1 OneHot Encoding and Multi-category Cross Entropy (15:34)](https://www.youtube.com/watch?v=4n71-tZ94yk) | [🎮 cross-entropy-pytorch.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L08/code/cross-entropy-pytorch.ipynb) |
| 58 | [🎥 L8.7.2 OneHot Encoding and Multi-category Cross Entropy Code Example (15:04)](https://www.youtube.com/watch?v=5bW0vn4ISqs) |  |
| 59 | [🎥 L8.8 Softmax Regression Derivatives for Gradient Descent (19:38)](https://www.youtube.com/watch?v=aeM-fmcdkXU) |  |
| 60 | [🎥 L8.9 Softmax Regression Code Example Using PyTorch (25:39)](https://www.youtube.com/watch?v=mM6apVBXGEA) | [🎮 softmax-regression\_scratch.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L08/code/softmax-regression_scratch.ipynb)  [🎮 softmax-regression-mnist.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L08/code/softmax-regression-mnist.ipynb) |
| 61 | [🎥 Deep Learning News #5, Feb 27 2021 (30:59)](https://www.youtube.com/watch?v=ZjZ6Yph5c2E) | 📝 [stuff-in-the-news-05.pdf](https://sebastianraschka.com/pdf/lecture-notes/stuff-in-the-news/stuff-in-the-news-05.pdf) |

### L09: Multilayer perceptrons and backpropration

|  | Videos | Material |
| --- | --- | --- |
| 62 | [🎥 L9.0 Multilayer Perceptrons – Lecture Overview (03:54)](https://www.youtube.com/watch?v=jD6IKpqSJM4) | 📝 [L09\_mlp\_\_slides.pdf](https://sebastianraschka.com/pdf/lecture-notes/stat453ss21/L09_mlp__slides.pdf) |
| 63 | [🎥 L9.1 Multilayer Perceptron Architecture (24:24)](https://www.youtube.com/watch?v=IUylp47hNA0) |  |
| 64 | [🎥 L9.2 Nonlinear Activation Functions (22:50)](https://www.youtube.com/watch?v=-_7W0KE8Ykg) | [🎮 xor-problem.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L09/code/xor-problem.ipynb) |
| 65 | [🎥 L9.3.1 Multilayer Perceptron Code Part 1/3 (10:00)](https://www.youtube.com/watch?v=zNyEzACInRg) |  |
| 66 | [🎥 L9.3.2 Multilayer Perceptron in PyTorch Part 2/3 (Jupyter Notebook) (08:31)](https://www.youtube.com/watch?v=Ycp4Si89s5Q) | [🎮 mlp-pytorch\_softmax-crossentr.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L09/code/mlp-pytorch_softmax-crossentr.ipynb) |
| 67 | [🎥 L9.3.3 Multilayer Perceptron in PyTorch Part 3/3 (Script Setup) (13:36)](https://www.youtube.com/watch?v=cDbQgQv_Yz0) | [🎮 mlp-softmax-pyscripts](https://github.com/rasbt/stat453-deep-learning-ss21/tree/main/L09/code/mlp-softmax-pyscripts) |
| 68 | [🎥 L9.4 Overfitting and Underfitting (31:09)](https://www.youtube.com/watch?v=hFGZyDVNgS4) |  |
| 69 | [🎥 L9.5.1 Cats & Dogs and Custom Data Loaders (16:48)](https://www.youtube.com/watch?v=RQIAmvElu1g) |  |
| 70 | [🎥 L9.5.2 Custom DataLoaders in PyTorch (Code Example) (29:29)](https://www.youtube.com/watch?v=hPzJ8H0Jtew) | [🎮 custom-dataloader](https://github.com/rasbt/stat453-deep-learning-ss21/tree/main/L09/code/custom-dataloader) |
| 71 | [🎥 Deep Learning News #6 (36:13)](https://www.youtube.com/watch?v=0J2b31KIIXs) | 📝 [stuff-in-the-news-06.pdf](https://sebastianraschka.com/pdf/lecture-notes/stuff-in-the-news/stuff-in-the-news-06.pdf) |

### L10: Regularization to avoid overfitting

|  | Videos | Material |
| --- | --- | --- |
| 72 | [🎥 L10.0 Regularization Methods for Neural Networks – Lecture Overview (11:09)](https://www.youtube.com/watch?v=Va4K-wYh_p8) | 📝 [L10\_regularization\_\_slides.pdf](https://sebastianraschka.com/pdf/lecture-notes/stat453ss21/L10_regularization__slides.pdf) |
| 73 | [🎥 L10.1 Techniques for Reducing Overfitting (12:17)](https://www.youtube.com/watch?v=KOBmBjlMVAE) |  |
| 74 | [🎥 L10.2 Data Augmentation in PyTorch (14:31)](https://www.youtube.com/watch?v=qLIosWyrh9Q) | [🎮 data-augmentation.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L10/code/data-augmentation.ipynb) |
| 75 | [🎥 L10.3 Early Stopping (04:07)](https://www.youtube.com/watch?v=YA1OdkiHJBY) |  |
| 76 | [🎥 L10.4 L2 Regularization for Neural Nets (15:48)](https://www.youtube.com/watch?v=uu2X47cSLmM) | [🎮 L2-log-reg.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L10/code/L2-log-reg.ipynb) |
| 77 | [🎥 L10.5.1 The Main Concept Behind Dropout (11:07)](https://www.youtube.com/watch?v=IHrZNBsgtwU) |  |
| 78 | [🎥 L10.5.2 Dropout Co-Adaptation Interpretation (03:50)](https://www.youtube.com/watch?v=GAE8dpDWo6E) |  |
| 79 | [🎥 L10.5.3 (Optional) Dropout Ensemble Interpretation (09:10)](https://www.youtube.com/watch?v=4We9G5jgKvI) |  |
| 80 | [🎥 L10.5.4 Dropout in PyTorch (12:04)](https://www.youtube.com/watch?v=kma-4wqp_-k) | [🎮 dropout.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L10/code/dropout.ipynb) |

### L11: Input normalization and weight initialization

|  | Videos | Material |
| --- | --- | --- |
| 81 | [🎥 L11.0 Input Normalization and Weight Initialization – Lecture Overview (02:52)](https://www.youtube.com/watch?v=xk6qb2IePaE) | 📝 [L11\_norm-and-init\_\_slides.pdf](https://sebastianraschka.com/pdf/lecture-notes/stat453ss21/L11_norm-and-init__slides.pdf) |
| 82 | [🎥 L11.1 Input Normalization (08:03)](https://www.youtube.com/watch?v=jzJactQXFDk) |  |
| 83 | [🎥 L11.2 How BatchNorm Works (15:14)](https://www.youtube.com/watch?v=34PDIFvvESc) |  |
| 84 | [🎥 L11.3 BatchNorm in PyTorch (08:44)](https://www.youtube.com/watch?v=8AUDn7iF2DY) | [🎮 batchnorm.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L11/code/batchnorm.ipynb) |
| 85 | [🎥 L11.4 Why BatchNorm Works (23:37)](https://www.youtube.com/watch?v=uI19wIdzh9M) |  |
| 86 | [🎥 L11.5 Weight Initialization – Why Do We Care? (06:00)](https://www.youtube.com/watch?v=RsX01aYbQdI) |  |
| 87 | [🎥 L11.6 Xavier Glorot and Kaiming He Initialization (12:21)](https://www.youtube.com/watch?v=ScWTYHQra5E) |  |
| 88 | [🎥 L11.7 Weight Initialization in PyTorch (07:36)](https://www.youtube.com/watch?v=nA6oEAE9IVc) | [🎮 weight\_normal.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L11/code/weight_normal.ipynb)   [🎮 weight\_kaiming.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L11/code/weight_kaiming.ipynb)   [🎮 weight\_normal-batchnorm.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L11/code/weight_normal-batchnorm.ipynb) |
| 89 | [🎥 Deep Learning News #7 (23:33)](https://www.youtube.com/watch?v=X5cEwDRh0Lk) | 📝 [stuff-in-the-news-07.pdf](https://sebastianraschka.com/pdf/lecture-notes/stuff-in-the-news/stuff-in-the-news-07.pdf) |

### L12: Learning rates and advanced optimization algorithms

|  | Videos | Material |
| --- | --- | --- |
| 90 | [🎥 L12.0: Improving Gradient Descent-based Optimization – Lecture Overview (06:19)](https://www.youtube.com/watch?v=7RhNXYqDBfU) | 📝 [L12\_optim\_\_slides.pdf](https://sebastianraschka.com/pdf/lecture-notes/stat453ss21/L12_optim__slides.pdf) |
| 91 | [🎥 L12.1 Learning Rate Decay (17:07)](https://www.youtube.com/watch?v=Owm1H0ukjS4) |  |
| 92 | [🎥 L12.2 Learning Rate Schedulers in PyTorch (14:38)](https://www.youtube.com/watch?v=tB1rz4L93JA) | [🎮 scheduler.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L12/code/scheduler.ipynb) |
| 93 | [🎥 L12.3 SGD with Momentum (09:05)](https://www.youtube.com/watch?v=gMxvefj0YAM) |  |
| 94 | [🎥 L12.4 Adam: Combining Adaptive Learning Rates and Momentum (15:33)](https://www.youtube.com/watch?v=eUOvUIRPSX8) | [🎮 sgd-scheduler-momentum.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L12/code/sgd-scheduler-momentum.ipynb)  [🎮 adam.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L12/code/adam.ipynb) |
| 95 | [🎥 L12.5 Choosing Different Optimizers in PyTorch (06:01)](https://www.youtube.com/watch?v=c-SRPvK_zzs) |  |
| 96 | [🎥 L12.6 Additional Topics and Research on Optimization Algorithms (12:04)](https://www.youtube.com/watch?v=7yoAocFiUh8) |  |

## Part 4: Deep learning for computer vision and language modeling

### L13: Introduction to convolutional neural networks

|  | Videos | Material |
| --- | --- | --- |
| 97 | [🎥 L13.0 Introduction to Convolutional Networks – Lecture Overview (05:25)](https://www.youtube.com/watch?v=i-Ngb6tn_KM) | 📝 [L13\_intro-cnn\_\_slides.pdf](https://sebastianraschka.com/pdf/lecture-notes/stat453ss21/L13_intro-cnn__slides.pdf) |
| 98 | [🎥 L13.1 Common Applications of CNNs (09:34)](https://www.youtube.com/watch?v=I5B7pgSEMhE) |  |
| 99 | [🎥 L13.2 Challenges of Image Classification (07:44)](https://www.youtube.com/watch?v=0FtJbmuUdFo) |  |
| 100 | [🎥 L13.3 Convolutional Neural Network Basics (18:39)](https://www.youtube.com/watch?v=7fWOE-z8YgY) |  |
| 101 | [🎥 L13.4 Convolutional Filters and Weight-Sharing (20:19)](https://www.youtube.com/watch?v=ryJ6Bna-ZNU) |  |
| 102 | [🎥 L13.5 Cross-correlation vs. Convolution (10:37)](https://www.youtube.com/watch?v=xbO-iIzkBy0) | [🎮 cross-correlation.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L13/code/notes/cross-correlation.ipynb) |
| 103 | [🎥 Deep Learning News #8 (18:02)](https://www.youtube.com/watch?v=AxKPjkBP2t4) | 📝 [stuff-in-the-news-08.pdf](https://sebastianraschka.com/pdf/lecture-notes/stuff-in-the-news/stuff-in-the-news-08.pdf) |
| 104 | [🎥 L13.6 CNNs & Backpropagation (05:54)](https://www.youtube.com/watch?v=-SwKNK9MIUU) |  |
| 105 | [🎥 L13.7 CNN Architectures & AlexNet (20:17)](https://www.youtube.com/watch?v=-IHxe4-09e4) |  |
| 106 | [🎥 L13.8 What a CNN Can See (13:42)](https://www.youtube.com/watch?v=PRFP5YC3u7g) |  |
| 107 | [🎥 L13.9.1 LeNet-5 in PyTorch (13:11)](https://www.youtube.com/watch?v=ye5k82FQC7I) | [🎮 1-lenet5-mnist.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L13/code/1-lenet5-mnist.ipynb) |
| 108 | [🎥 L13.9.2 Saving and Loading Models in PyTorch (05:44)](https://www.youtube.com/watch?v=vB_Y04gsyBI) | [🎮 save-and-load](https://github.com/rasbt/stat453-deep-learning-ss21/tree/main/L13/code/save-and-load) |
| 109 | [🎥 L13.9.3 AlexNet in PyTorch (15:15)](https://www.youtube.com/watch?v=mlXRVuD_HEg) | [🎮 2-alexnet-cifar10.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L13/code/2-alexnet-cifar10.ipynb) |
| 110 | [🎥 Deep Learning News #9 (28:09)](https://www.youtube.com/watch?v=Nm4Y4Pd1mg0) | 📝 [stuff-in-the-news-09.pdf](https://sebastianraschka.com/pdf/lecture-notes/stuff-in-the-news/stuff-in-the-news-09.pdf) |

### L14: Convolutional neural networks architectures

|  | Videos | Material |
| --- | --- | --- |
| 111 | [🎥 L14.0: Convolutional Neural Networks Architectures – Lecture Overview (06:18)](https://www.youtube.com/watch?v=1A6HViSXaqQ) | 📝 [L14\_cnn-architectures\_slides.pdf](https://sebastianraschka.com/pdf/lecture-notes/stat453ss21/L14_cnn-architectures_slides.pdf) |
| 112 | [🎥 L14.1: Convolutions and Padding (11:14)](https://www.youtube.com/watch?v=6v05kAtV1M0) |  |
| 113 | [🎥 L14.2: Spatial Dropout and BatchNorm (06:46)](https://www.youtube.com/watch?v=TGqqTgn4cAg) |  |
| 114 | [🎥 L14.3: Architecture Overview (03:23)](https://www.youtube.com/watch?v=WyXO762G2_A) |  |
| 115 | [🎥 L14.3.1.1 VGG16 Overview (06:05)](https://www.youtube.com/watch?v=YcmNIOyfdZQ) |  |
| 116 | [🎥 L14.3.1.2 VGG16 in PyTorch (15:52)](https://www.youtube.com/watch?v=PlFiRPdBEAo) | [🎮 1.1-vgg16.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L14/1.1-vgg16.ipynb) |
| 117 | [🎥 L14.3.2.1 ResNet Overview (14:41)](https://www.youtube.com/watch?v=q_IlqYlYhlo) |  |
| 118 | [🎥 L14.3.2.2 ResNet-34 in PyTorch (18:47)](https://www.youtube.com/watch?v=JG_ODvnlgjY) | [🎮 2-resnet-example.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L14/2-resnet-example.ipynb)  [🎮 2-resnet34.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L14/2-resnet34.ipynb) |
| 120 | [🎥 L14.4.1 Replacing Max-Pooling with Convolutional Layers (08:19)](https://www.youtube.com/watch?v=Lq83NFkkJCk) |  |
| 121 | [🎥 L14.4.2 All-Convolutional Network in PyTorch (08:17)](https://www.youtube.com/watch?v=A5dC5yuPXwo) | [🎮 3-all-convnet.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L14/3-all-convnet.ipynb) |
| 122 | [🎥 L14.5 Convolutional Instead of Fully Connected Layers (14:33)](https://www.youtube.com/watch?v=rqLjZ8k4va8) |  |
| 123 | [🎥 L14.6.1 Transfer Learning (07:38)](https://www.youtube.com/watch?v=OkQRtm9JY1k) |  |
| 124 | [🎥 L14.6.2 Transfer Learning in PyTorch (11:35)](https://www.youtube.com/watch?v=FaW9JCSJn2s) | [🎮 5-transfer-learning-vgg16\_small.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L14/5-transfer-learning-vgg16_small.ipynb)  [🎮 5-transfer-learning-vgg16\_large.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L14/5-transfer-learning-vgg16_large.ipynb) |
| 119 | [🎥 Deep Learning News #10 (20:55)](https://www.youtube.com/watch?v=sZT4XZkptP8) | 📝 [stuff-in-the-news-10.pdf](https://sebastianraschka.com/pdf/lecture-notes/stuff-in-the-news/stuff-in-the-news-10.pdf) |

### L15: Introduction to recurrent neural networks

|  | Videos | Material |
| --- | --- | --- |
| 125 | [🎥 L15.0: Introduction to Recurrent Neural Networks – Lecture Overview (03:58)](https://www.youtube.com/watch?v=q5YxK17tRm0) | 📝 [L15\_intro-rnn\_\_slides.pdf](https://sebastianraschka.com/pdf/lecture-notes/stat453ss21/L15_intro-rnn__slides.pdf) |
| 126 | [🎥 L15.1: Different Methods for Working With Text Data (15:57)](https://www.youtube.com/watch?v=kwmZtkzB4e0) |  |
| 127 | [🎥 L15.2 Sequence Modeling with RNNs (13:39)](https://www.youtube.com/watch?v=5fdy-hBeWCI) |  |
| 128 | [🎥 L15.3 Different Types of Sequence Modeling Tasks (04:31)](https://www.youtube.com/watch?v=Ed8GTvkzkZE) |  |
| 129 | [🎥 L15.4 Backpropagation Through Time Overview (09:33)](https://www.youtube.com/watch?v=0XdPIqi0qpg) |  |
| 130 | [🎥 L15.5 Long Short-Term Memory (16:58)](https://www.youtube.com/watch?v=k6fSgUaWUF8) |  |
| 131 | [🎥 L15.6 RNNs for Classification: A Many-to-One Word RNN (29:06)](https://www.youtube.com/watch?v=TI4HRR3Hd9A) |  |
| 132 | [🎥 L15.7 An RNN Sentiment Classifier in PyTorch (40:00)](https://www.youtube.com/watch?v=KgrdifrlDxg) | [🎮 1\_lstm.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L15/1_lstm.ipynb)  [🎮 2\_packed-lstm.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L15/2_packed-lstm.ipynb) |

## Part 5: Deep generative models

### L16: Autoencoders

|  | Videos | Material |
| --- | --- | --- |
| 133 | [🎥 L16.0 Introduction to Autoencoders – Lecture Overview (04:45)](https://www.youtube.com/watch?v=9Ujv_IoBtF4) | 📝 [L16\_autoencoder\_\_slides.pdf](https://sebastianraschka.com/pdf/lecture-notes/stat453ss21/L16_autoencoder__slides.pdf) |
| 134 | [🎥 L16.1 Dimensionality Reduction (09:39)](https://www.youtube.com/watch?v=UgOHupaIfcA) |  |
| 135 | [🎥 L16.2 A Fully-Connected Autoencoder (16:34)](https://www.youtube.com/watch?v=8O_FDPIlj1s) |  |
| 136 | [🎥 L16.3 Convolutional Autoencoders & Transposed Convolutions (16:07)](https://www.youtube.com/watch?v=ilkSwsggSNM) |  |
| 137 | [🎥 L16.4 A Convolutional Autoencoder in PyTorch (15:20)](https://www.youtube.com/watch?v=345wRyqKkQ0) | [🎮 conv-autoencoder\_mnist.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L16/conv-autoencoder_mnist.ipynb) |
| 138 | [🎥 L16.5 Other Types of Autoencoders (5:33)](https://www.youtube.com/watch?v=FPZeRM1p1ao) |  |

### L17: Variational autoencoders

|  | Videos | Material |
| --- | --- | --- |
| 139 | [🎥 L17.0 Intro to Variational Autoencoders – Lecture Overview (03:16)](https://www.youtube.com/watch?v=UnImUYOdWgk) | 📝 [L17\_vae\_\_slides.pdf](https://sebastianraschka.com/pdf/lecture-notes/stat453ss21/L17_vae__slides.pdf) |
| 140 | [🎥 L17.1 Variational Autoencoder Overview (05:23)](https://www.youtube.com/watch?v=H2XgdND0DV4) |  |
| 141 | [🎥 L17.2 Sampling from a Variational Autoencoder (09:26)](https://www.youtube.com/watch?v=YgSWrafXI8U) |  |
| 142 | [🎥 L17.3 The Log-Var Trick (07:34)](https://www.youtube.com/watch?v=pmvo0S3-G-I) |  |
| 143 | [🎥 L17.4 Variational Autoencoder Loss Function (12:16)](https://www.youtube.com/watch?v=ywYuZrLENH0) |  |
| 144 | [🎥 L17.5 A Variational Autoencoder for Handwritten Digits in PyTorch (23:12)](https://www.youtube.com/watch?v=afNuE5z2CQ8) | [🎮 1\_VAE\_mnist\_sigmoid\_mse.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L17/1_VAE_mnist_sigmoid_mse.ipynb) |
| 145 | [🎥 L17.6 A Variational Autoencoder for Face Images in PyTorch (10:05)](https://www.youtube.com/watch?v=sul2ExoUrnw) | [🎮 2\_VAE\_celeba-sigmoid\_mse.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L17/2_VAE_celeba-sigmoid_mse.ipynb)  [🎮 3\_VAE\_nearest-neighbor-upsampling.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L17/3_VAE_nearest-neighbor-upsampling.ipynb)  [🎮 5\_VAE\_celeba\_latent-arithmetic.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L17/5_VAE_celeba_latent-arithmetic.ipynb) |
| 146 | [🎥 L17.7 VAE Latent Space Arithmetic in PyTorch – Making People Smile (11:54)](https://www.youtube.com/watch?v=EfFr87ARDF0) | [🎮 5\_VAE\_celeba\_latent-arithmetic.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L17/5_VAE_celeba_latent-arithmetic.ipynb) |

### L18: Introduction to generative adversarial networks

|  | Videos | Material |
| --- | --- | --- |
| 147 | [🎥 L18.0: Introduction to Generative Adversarial Networks – Lecture Overview (05:14)](https://www.youtube.com/watch?v=OnoPaZaKoS8) | 📝 [L18\_gan\_\_slides.pdf](https://sebastianraschka.com/pdf/lecture-notes/stat453ss21/L18_gan__slides.pdf) |
| 148 | [🎥 L18.1: The Main Idea Behind GANs (10:42)](https://www.youtube.com/watch?v=-Zi5SReze6U) |  |
| 149 | [🎥 L18.2: The GAN Objective (26:25)](https://www.youtube.com/watch?v=m_H6viKCTEE) |  |
| 150 | [🎥 L18.3: Modifying the GAN Loss Function for Practical Use (18:45)](https://www.youtube.com/watch?v=ILpC3b-819Q) |  |
| 151 | [🎥 L18.4: A GAN for Generating Handwritten Digits in PyTorch (22:45)](https://www.youtube.com/watch?v=cTlxZ1FO1mY) | [🎮 04\_01\_gan-mnist.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L18/04_01_gan-mnist.ipynb) |
| 152 | [🎥 L18.5: Tips and Tricks to Make GANs Work (17:13)](https://www.youtube.com/watch?v=_cUdjPdbldQ) | [🎮 https://github.com/soumith/ganhacks](https://github.com/soumith/ganhacks) |
| 153 | [🎥 L18.6: A DCGAN for Generating Face Images in PyTorch (12:42)](https://www.youtube.com/watch?v=5fs9PMzrVig) | [🎮 04\_02\_dcgan-celeba.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L18/04_02_dcgan-celeba.ipynb) |

### L19: [Self-attention](https://sebastianraschka.com/glossary/#mha "Multi-Head Attention (MHA)") and transformer networks

|  | Videos | Material |
| --- | --- | --- |
| 154 | [🎥 L19.0 RNNs & Transformers for Sequence-to-Sequence Modeling – Lecture Overview (03:05)](https://www.youtube.com/watch?v=DlWTTrHa8bI) | 📝 [L19\_seq2seq\_rnn-transformers\_\_slides.pdf](https://sebastianraschka.com/pdf/lecture-notes/stat453ss21/L19_seq2seq_rnn-transformers__slides.pdf) |
| 155 | [🎥 L19.1 Sequence Generation with Word and Character RNNs (17:43)](https://www.youtube.com/watch?v=fSBw6TrePPg) |  |
| 156 | [🎥 L19.2.1 Implementing a Character RNN in PyTorch (Concepts) (09:19)](https://www.youtube.com/watch?v=PFcWQkGP4lU) |  |
| 157 | [🎥 L19.2.2 Implementing a Character RNN in PyTorch (Code Example) (25:56)](https://www.youtube.com/watch?v=tL5puCeDr-o) | [🎮 character-rnn](https://github.com/rasbt/stat453-deep-learning-ss21/tree/main/L19/character-rnn) |
| 158 | [🎥 L19.3 RNNs with an Attention Mechanism (22:18)](https://www.youtube.com/watch?v=mDZil99CtSU) |  |
| 159 | [🎥 L19.4.1 Using Attention Without the RNN – A Basic Form of Self-Attention (16:10)](https://www.youtube.com/watch?v=i_pfHD4P_wg) |  |
| 160 | [🎥 L19.4.2 Self-Attention and Scaled Dot-Product Attention (16:08)](https://www.youtube.com/watch?v=0PjHri8tc1c) |  |
| 161 | [🎥 L19.4.3 Multi-Head Attention (07:36)](https://www.youtube.com/watch?v=A1eUVxscNq8) |  |
| 162 | [🎥 L19.5.1 The Transformer Architecture (22:36)](https://www.youtube.com/watch?v=tstbZXNCfLY) |  |
| 163 | [🎥 L19.5.2.1 Some Popular Transformer Models: BERT, GPT, and BART – Overview (08:40)](https://www.youtube.com/watch?v=iFhYwEi03Ew) |  |
| 164 | [🎥 L19.5.2.2 GPT-v1: Generative Pre-Trained Transformer (09:53)](https://www.youtube.com/watch?v=LOCzBgSV4tQ) |  |
| 165 | [🎥 L19.5.2.3 BERT: Bidirectional Encoder Representations from Transformers (18:30)](https://www.youtube.com/watch?v=_BFp4kjSB-I) |  |
| 166 | [🎥 L19.5.2.4 GPT-v2: Language Models are Unsupervised Multitask Learners (09:02)](https://www.youtube.com/watch?v=BXv1m9Asl7I) |  |
| 167 | [🎥 L19.5.2.5 GPT-v3: Language Models are Few-Shot Learners (06:40)](https://www.youtube.com/watch?v=wYdKn-X4MhY) |  |
| 168 | [🎥 L19.5.2.6 BART: Combining Bidirectional and Auto-Regressive Transformers (10:15)](https://www.youtube.com/watch?v=1JBMCG8rW18) |  |
| 169 | [🎥 L19.5.2.7: Closing Words – The Recent Growth of Language Transformers (06:09)](https://www.youtube.com/watch?v=OyqIuxMmLRg) |  |
| 170 | [🎥 L19.6 DistilBert Movie Review Classifier in PyTorch (17:57)](https://www.youtube.com/watch?v=emDmznRlsWw) | [🎮 distilbert-classifier](https://github.com/rasbt/stat453-deep-learning-ss21/tree/main/L19/distilbert-classifier) |
