---
title: "深度学习导论"
title_en: "Introduction to Deep Learning"
source: https://sebastianraschka.com/blog/2021/dl-course.html
crawled: 2026-09-06
translated: 2026-09-06
---

# 深度学习导论

> 原文：[Introduction to Deep Learning](https://sebastianraschka.com/blog/2021/dl-course.html)

今天早上我坐下来，把 2021 年录制的所有深度学习相关视频整理了一遍。我确信这对未来的自己会是一份有用的参考资料，也希望它或许能帮到外面的某位读者。

PS：所有代码示例都使用 PyTorch :)

## 第 1 部分：导论

### L01：深度学习导论

|  | 视频 | 资料 |
| --- | --- | --- |
| 1 | [🎥 L1.0 导论 (04:26)](https://www.youtube.com/watch?v=1nqCZqDYPp0) | 📝 [L01-intro\_slides.pdf](https://sebastianraschka.com/pdf/lecture-notes/stat453ss21/L01-intro_slides.pdf) |
| 2 | [🎥 L1.1.1 课程概览 第 1 部分：动机与主题 (16:26)](https://www.youtube.com/watch?v=6VbtJ9nn5ng) |  |
| 3 | [🎥 L1.1.2 课程概览 第 2 部分：课程组织 (17:34)](https://www.youtube.com/watch?v=s7ZCbKI5Exw) |  |
| 4 | [🎥 L1.2 什么是机器学习？ (17:42)](https://www.youtube.com/watch?v=d6oQzE4kst0) |  |
| 5 | [🎥 L1.3.1 机器学习的主要类别 第 1 部分：监督学习 (10:55)](https://www.youtube.com/watch?v=UadzJLHJB50) |  |
| 6 | [🎥 L1.3.2 机器学习的主要类别 第 2 部分：无监督学习 (7:29)](https://www.youtube.com/watch?v=nHhuuUwd05g) |  |
| 7 | [🎥 L1.3.3 机器学习的主要类别 第 3 部分：强化学习 (3:48)](https://www.youtube.com/watch?v=EQCZUOxGrOo) |  |
| 8 | [🎥 L1.3.4 机器学习的主要类别 第 4 部分：监督学习的特殊情况 (10:46)](https://www.youtube.com/watch?v=B59lK5yo57M) |  |
| 9 | [🎥 L1.4 监督学习的工作流程 (17:46)](https://www.youtube.com/watch?v=nd9dhrvtIA0) |  |
| 10 | [🎥 L1.5 必备的机器学习记号与术语 (22:02)](https://www.youtube.com/watch?v=o-yHLOvuh2o) |  |
| 11 | [🎥 L1.6 本课程的实践要点与工具 (11:26)](https://www.youtube.com/watch?v=R16VmI2ZhR0) |  |
| 12 | [🎥 深度学习新闻 #1 (15:28)](https://www.youtube.com/watch?v=UAjfVRicYBM) | 📝 [stuff-in-the-news-01.pdf](https://sebastianraschka.com/pdf/lecture-notes/stuff-in-the-news/stuff-in-the-news-01.pdf) |

### L02：深度学习简史

|  | 视频 | 资料 |
| --- | --- | --- |
| 13 | [🎥 L2.0 深度学习简史——课程概览 (02:57)](https://www.youtube.com/watch?v=Ezig00nypvU) | 📝 [L02\_dl-history\_slides.pdf](https://sebastianraschka.com/pdf/lecture-notes/stat453ss21/L02_dl-history_slides.pdf) |
| 14 | [🎥 L2.1 人工神经元 (16:49)](https://www.youtube.com/watch?v=gbLasjwAGik) |  |
| 15 | [🎥 L2.2 多层网络 (15:11)](https://www.youtube.com/watch?v=G7oqVqU5qsQ) |  |
| 16 | [🎥 L2.3 深度学习的起源 (20:11)](https://www.youtube.com/watch?v=tkUCMtJd43Y) |  |
| 17 | [🎥 L2.4 深度学习的硬件与软件格局 (7:20)](https://www.youtube.com/watch?v=TMCNkeJGIfg) |  |
| 18 | [🎥 L2.5 深度学习的当前趋势 (8:21)](https://www.youtube.com/watch?v=FpOpb-BMIH8) |  |

### L03：单层神经网络：感知机算法

|  | 视频 | 资料 |
| --- | --- | --- |
| 19 | [🎥 L3.0 感知机课程概览 (05:02)](https://www.youtube.com/watch?v=cm_wv2QpTgc) | 📝 [L03\_perceptron\_slides.pdf](https://sebastianraschka.com/pdf/lecture-notes/stat453ss21/L03_perceptron_slides.pdf) |
| 20 | [🎥 L3.1 关于大脑与神经元 (12:50)](https://www.youtube.com/watch?v=AnSDPcvtRLo) |  |
| 21 | [🎥 L3.2 感知机学习规则 (31:38)](https://www.youtube.com/watch?v=C8Uns9HEVXI) | [🎮 perceptron-animation.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L03/code/perceptron-animation.ipynb) |
| 22 | [🎥 L3.3 Python 中的向量化 (14:54)](https://www.youtube.com/watch?v=OnG2NfuC5aY) | [🎮 vectorization-example.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L03/code/vectorization-example.ipynb) |
| 23 | [🎥 L3.4 用 NumPy 和 PyTorch 在 Python 中实现感知机 (28:42)](https://www.youtube.com/watch?v=TlGpIKMVoOg) | [🎮 perceptron-numpy.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L03/code/perceptron-numpy.ipynb)    [🎮 perceptron-pytorch.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L03/code/perceptron-pytorch.ipynb) |
| 24 | [🎥 L3.5 感知机背后的几何直观 (18:43)](https://www.youtube.com/watch?v=Fj7BgxI73TA) |  |
| 25 | [🎥 L3.6 深度学习新闻 #2 (25:01)](https://www.youtube.com/watch?v=TgbI3LeB1bg) | 📝 [stuff-in-the-news-02.pdf](https://sebastianraschka.com/pdf/lecture-notes/stuff-in-the-news/stuff-in-the-news-02.pdf) |

## 第 2 部分：数学与计算基础

### L04：深度学习的线性代数与微积分

|  | 视频 | 资料 |
| --- | --- | --- |
| 26 | [🎥 L4.0 深度学习的线性代数——课程概览 (02:11)](https://www.youtube.com/watch?v=3mjJxu3B0zA) | 📝 [L04\_linalg-dl\_slides.pdf](https://sebastianraschka.com/pdf/lecture-notes/stat453ss21/L04_linalg-dl_slides.pdf) |
| 27 | [🎥 L4.1 深度学习中的张量 (13:02)](https://www.youtube.com/watch?v=JXfDlgrfOBY) |  |
| 28 | [🎥 L4.2 PyTorch 中的张量 (28:32)](https://www.youtube.com/watch?v=zk_asBov8QI) |  |
| 29 | [🎥 L4.3 向量、矩阵与广播 (16:15)](https://www.youtube.com/watch?v=4Ehb_is-MFU) |  |
| 30 | [🎥 L4.4 神经网络的记号约定 (11:52)](https://www.youtube.com/watch?v=4pnoymfFiYM) |  |
| 31 | [🎥 L4.5 PyTorch 中的全连接（线性）层 (12:41)](https://www.youtube.com/watch?v=XswEBzNgIYc) |  |

### L05：基于梯度下降的参数优化

|  | 视频 | 资料 |
| --- | --- | --- |
| 32 | [🎥 L5.0 梯度下降——课程概览 (06:28)](https://www.youtube.com/watch?v=VBOxg62CwCg) | 📝 [L05\_gradient-descent\_slides.pdf](https://sebastianraschka.com/pdf/lecture-notes/stat453ss21/L05_gradient-descent_slides.pdf) |
| 33 | [🎥 L5.1 在线、批量与小批量模式 (21:04)](https://www.youtube.com/watch?v=b4DXHd3RwqA) |  |
| 34 | [🎥 L5.2 感知机与线性回归的关系 (05:20)](https://www.youtube.com/watch?v=4JB1j8eIGzI) |  |
| 35 | [🎥 L5.3 线性回归的迭代训练算法 (11:10)](https://www.youtube.com/watch?v=1QH2bVuV98A) |  |
| 36 | [🎥 L5.4 （选学）微积分温习 I：导数 (17:36)](https://www.youtube.com/watch?v=tL1THESrXgI) |  |
| 37 | [🎥 L5.5 （选学）微积分温习 II：梯度 (17:34)](https://www.youtube.com/watch?v=YPZVGSRmjLk) |  |
| 38 | [🎥 L5.6 理解梯度下降 (26:34)](https://www.youtube.com/watch?v=L4xzybIa-bo) |  |
| 39 | [🎥 L5.7 训练自适应线性神经元（Adaline） (06:43)](https://www.youtube.com/watch?v=iLCT0i-lCsw) |  |
| 40 | [🎥 L5.8 Adaline 代码示例 (33:26)](https://www.youtube.com/watch?v=GGcaqzhKzLc) | [🎮 linear-regr-gd.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L05/code/linear-regr-gd.ipynb)    [🎮 adaline-sgd.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L05/code/adaline-sgd.ipynb) |
| 41 | [🎥 深度学习新闻 #3 (20:24)](https://www.youtube.com/watch?v=2I8SqKLt-Nk) | 📝 [stuff-in-the-news-03.pdf](https://sebastianraschka.com/pdf/lecture-notes/stuff-in-the-news/stuff-in-the-news-03.pdf) |

### L06：使用 PyTorch 进行自动微分

|  | 视频 | 资料 |
| --- | --- | --- |
| 42 | [🎥 L6.0 PyTorch 中的自动微分——课程概览 (04:09)](https://www.youtube.com/watch?v=j1-r1vO2a_o) | 📝 [L06\_pytorch\_slides.pdf](https://sebastianraschka.com/pdf/lecture-notes/stat453ss21/L06_pytorch_slides.pdf) |
| 43 | [🎥 L6.1 进一步了解 PyTorch (15:47)](https://www.youtube.com/watch?v=LjdiVPQ45GE) |  |
| 44 | [🎥 L6.2 通过计算图理解自动微分 (22:47)](https://www.youtube.com/watch?v=oY6-i2Ybin4) |  |
| 45 | [🎥 L6.3 PyTorch 中的自动微分 (09:02)](https://www.youtube.com/watch?v=VvUz0Q9e09g) | [🎮 pytorch-autograd.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L06/code/pytorch-autograd.ipynb) |
| 46 | [🎥 L6.4 用 PyTorch 训练 ADALINE (23:29)](https://www.youtube.com/watch?v=00KgeJwNaZA) | [🎮 adaline-with-autograd.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L06/code/adaline-with-autograd.ipynb) |
| 47 | [🎥 L6.5 深入了解 PyTorch API (25:02)](https://www.youtube.com/watch?v=klc79sZ1yVc) |  |

### L07：集群与云计算资源

|  | 视频 | 资料 |
| --- | --- | --- |
| 48 | [🎥 L7.0 GPU 资源与 Google Colab (19:17)](https://www.youtube.com/watch?v=5pew4YEa1ww) | 📝 [L07\_cloud-computing\_slides.pdf](https://sebastianraschka.com/pdf/lecture-notes/stat453ss21/L07_cloud-computing_slides.pdf)  云资源清单：<https://github.com/zszazi/Deep-learning-in-cloud> |
| 49 | [🎥 深度学习新闻 #4 (28:09)](https://www.youtube.com/watch?v=mPC14fIO4SY) | 📝 [stuff-in-the-news-04.pdf](https://sebastianraschka.com/pdf/lecture-notes/stuff-in-the-news/stuff-in-the-news-04.pdf) |

## 第 3 部分：神经网络导论

### L08：多项逻辑回归 / Softmax 回归

|  | 视频 | 资料 |
| --- | --- | --- |
| 50 | [🎥 L8.0 逻辑回归——课程概览 (06:28)](https://www.youtube.com/watch?v=10PTpRRpRk0) | 📝 [L08\_logistic\_\_slides.pdf](https://sebastianraschka.com/pdf/lecture-notes/stat453ss21/L08_logistic__slides.pdf) |
| 51 | [🎥 L8.1 作为单层神经网络的逻辑回归 (09:15)](https://www.youtube.com/watch?v=ncZ5iSZekVQ) |  |
| 52 | [🎥 L8.2 逻辑回归的损失函数 (12:57)](https://www.youtube.com/watch?v=GxJe0DZvydM) |  |
| 53 | [🎥 L8.3 逻辑回归损失的导数与训练 (19:57)](https://www.youtube.com/watch?v=7rR1L7t2EnA) |  |
| 54 | [🎥 L8.4 logit 与交叉熵 (06:47)](https://www.youtube.com/watch?v=icQaFxKa_J0) |  |
| 55 | [🎥 L8.5 PyTorch 中的逻辑回归——代码示例 (19:02)](https://www.youtube.com/watch?v=6igMArA6k3A) | [🎮 logistic-regression.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L08/code/logistic-regression.ipynb) |
| 56 | [🎥 L8.6 多项逻辑回归 / Softmax 回归 (17:31)](https://www.youtube.com/watch?v=L0FU8NFpx4E) |  |
| 57 | [🎥 L8.7.1 OneHot 编码与多类别交叉熵 (15:34)](https://www.youtube.com/watch?v=4n71-tZ94yk) | [🎮 cross-entropy-pytorch.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L08/code/cross-entropy-pytorch.ipynb) |
| 58 | [🎥 L8.7.2 OneHot 编码与多类别交叉熵代码示例 (15:04)](https://www.youtube.com/watch?v=5bW0vn4ISqs) |  |
| 59 | [🎥 L8.8 用于梯度下降的 Softmax 回归导数 (19:38)](https://www.youtube.com/watch?v=aeM-fmcdkXU) |  |
| 60 | [🎥 L8.9 使用 PyTorch 的 Softmax 回归代码示例 (25:39)](https://www.youtube.com/watch?v=mM6apVBXGEA) | [🎮 softmax-regression\_scratch.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L08/code/softmax-regression_scratch.ipynb)  [🎮 softmax-regression-mnist.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L08/code/softmax-regression-mnist.ipynb) |
| 61 | [🎥 深度学习新闻 #5，2021 年 2 月 27 日 (30:59)](https://www.youtube.com/watch?v=ZjZ6Yph5c2E) | 📝 [stuff-in-the-news-05.pdf](https://sebastianraschka.com/pdf/lecture-notes/stuff-in-the-news/stuff-in-the-news-05.pdf) |

### L09：多层感知机与反向传播

|  | 视频 | 资料 |
| --- | --- | --- |
| 62 | [🎥 L9.0 多层感知机——课程概览 (03:54)](https://www.youtube.com/watch?v=jD6IKpqSJM4) | 📝 [L09\_mlp\_\_slides.pdf](https://sebastianraschka.com/pdf/lecture-notes/stat453ss21/L09_mlp__slides.pdf) |
| 63 | [🎥 L9.1 多层感知机架构 (24:24)](https://www.youtube.com/watch?v=IUylp47hNA0) |  |
| 64 | [🎥 L9.2 非线性激活函数 (22:50)](https://www.youtube.com/watch?v=-_7W0KE8Ykg) | [🎮 xor-problem.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L09/code/xor-problem.ipynb) |
| 65 | [🎥 L9.3.1 多层感知机代码 第 1/3 部分 (10:00)](https://www.youtube.com/watch?v=zNyEzACInRg) |  |
| 66 | [🎥 L9.3.2 PyTorch 中的多层感知机 第 2/3 部分（Jupyter Notebook） (08:31)](https://www.youtube.com/watch?v=Ycp4Si89s5Q) | [🎮 mlp-pytorch\_softmax-crossentr.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L09/code/mlp-pytorch_softmax-crossentr.ipynb) |
| 67 | [🎥 L9.3.3 PyTorch 中的多层感知机 第 3/3 部分（脚本形式） (13:36)](https://www.youtube.com/watch?v=cDbQgQv_Yz0) | [🎮 mlp-softmax-pyscripts](https://github.com/rasbt/stat453-deep-learning-ss21/tree/main/L09/code/mlp-softmax-pyscripts) |
| 68 | [🎥 L9.4 过拟合与欠拟合 (31:09)](https://www.youtube.com/watch?v=hFGZyDVNgS4) |  |
| 69 | [🎥 L9.5.1 猫狗数据集与自定义数据加载器 (16:48)](https://www.youtube.com/watch?v=RQIAmvElu1g) |  |
| 70 | [🎥 L9.5.2 PyTorch 中的自定义 DataLoader（代码示例） (29:29)](https://www.youtube.com/watch?v=hPzJ8H0Jtew) | [🎮 custom-dataloader](https://github.com/rasbt/stat453-deep-learning-ss21/tree/main/L09/code/custom-dataloader) |
| 71 | [🎥 深度学习新闻 #6 (36:13)](https://www.youtube.com/watch?v=0J2b31KIIXs) | 📝 [stuff-in-the-news-06.pdf](https://sebastianraschka.com/pdf/lecture-notes/stuff-in-the-news/stuff-in-the-news-06.pdf) |

### L10：避免过拟合的正则化

|  | 视频 | 资料 |
| --- | --- | --- |
| 72 | [🎥 L10.0 神经网络的正则化方法——课程概览 (11:09)](https://www.youtube.com/watch?v=Va4K-wYh_p8) | 📝 [L10\_regularization\_\_slides.pdf](https://sebastianraschka.com/pdf/lecture-notes/stat453ss21/L10_regularization__slides.pdf) |
| 73 | [🎥 L10.1 减少过拟合的技术 (12:17)](https://www.youtube.com/watch?v=KOBmBjlMVAE) |  |
| 74 | [🎥 L10.2 PyTorch 中的数据增强 (14:31)](https://www.youtube.com/watch?v=qLIosWyrh9Q) | [🎮 data-augmentation.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L10/code/data-augmentation.ipynb) |
| 75 | [🎥 L10.3 早停 (04:07)](https://www.youtube.com/watch?v=YA1OdkiHJBY) |  |
| 76 | [🎥 L10.4 神经网络的 L2 正则化 (15:48)](https://www.youtube.com/watch?v=uu2X47cSLmM) | [🎮 L2-log-reg.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L10/code/L2-log-reg.ipynb) |
| 77 | [🎥 L10.5.1 Dropout 的核心概念 (11:07)](https://www.youtube.com/watch?v=IHrZNBsgtwU) |  |
| 78 | [🎥 L10.5.2 Dropout 的协同适应解释 (03:50)](https://www.youtube.com/watch?v=GAE8dpDWo6E) |  |
| 79 | [🎥 L10.5.3 （选学）Dropout 的集成解释 (09:10)](https://www.youtube.com/watch?v=4We9G5jgKvI) |  |
| 80 | [🎥 L10.5.4 PyTorch 中的 Dropout (12:04)](https://www.youtube.com/watch?v=kma-4wqp_-k) | [🎮 dropout.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L10/code/dropout.ipynb) |

### L11：输入归一化与权重初始化

|  | 视频 | 资料 |
| --- | --- | --- |
| 81 | [🎥 L11.0 输入归一化与权重初始化——课程概览 (02:52)](https://www.youtube.com/watch?v=xk6qb2IePaE) | 📝 [L11\_norm-and-init\_\_slides.pdf](https://sebastianraschka.com/pdf/lecture-notes/stat453ss21/L11_norm-and-init__slides.pdf) |
| 82 | [🎥 L11.1 输入归一化 (08:03)](https://www.youtube.com/watch?v=jzJactQXFDk) |  |
| 83 | [🎥 L11.2 BatchNorm 的工作原理 (15:14)](https://www.youtube.com/watch?v=34PDIFvvESc) |  |
| 84 | [🎥 L11.3 PyTorch 中的 BatchNorm (08:44)](https://www.youtube.com/watch?v=8AUDn7iF2DY) | [🎮 batchnorm.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L11/code/batchnorm.ipynb) |
| 85 | [🎥 L11.4 BatchNorm 为什么有效 (23:37)](https://www.youtube.com/watch?v=uI19wIdzh9M) |  |
| 86 | [🎥 L11.5 权重初始化——我们为什么要关心？ (06:00)](https://www.youtube.com/watch?v=RsX01aYbQdI) |  |
| 87 | [🎥 L11.6 Xavier Glorot 初始化与 Kaiming He 初始化 (12:21)](https://www.youtube.com/watch?v=ScWTYHQra5E) |  |
| 88 | [🎥 L11.7 PyTorch 中的权重初始化 (07:36)](https://www.youtube.com/watch?v=nA6oEAE9IVc) | [🎮 weight\_normal.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L11/code/weight_normal.ipynb)   [🎮 weight\_kaiming.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L11/code/weight_kaiming.ipynb)   [🎮 weight\_normal-batchnorm.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L11/code/weight_normal-batchnorm.ipynb) |
| 89 | [🎥 深度学习新闻 #7 (23:33)](https://www.youtube.com/watch?v=X5cEwDRh0Lk) | 📝 [stuff-in-the-news-07.pdf](https://sebastianraschka.com/pdf/lecture-notes/stuff-in-the-news/stuff-in-the-news-07.pdf) |

### L12：学习率与高级优化算法

|  | 视频 | 资料 |
| --- | --- | --- |
| 90 | [🎥 L12.0: 改进基于梯度的优化——课程概览 (06:19)](https://www.youtube.com/watch?v=7RhNXYqDBfU) | 📝 [L12\_optim\_\_slides.pdf](https://sebastianraschka.com/pdf/lecture-notes/stat453ss21/L12_optim__slides.pdf) |
| 91 | [🎥 L12.1 学习率衰减 (17:07)](https://www.youtube.com/watch?v=Owm1H0ukjS4) |  |
| 92 | [🎥 L12.2 PyTorch 中的学习率调度器 (14:38)](https://www.youtube.com/watch?v=tB1rz4L93JA) | [🎮 scheduler.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L12/code/scheduler.ipynb) |
| 93 | [🎥 L12.3 带动量的 SGD (09:05)](https://www.youtube.com/watch?v=gMxvefj0YAM) |  |
| 94 | [🎥 L12.4 Adam：结合自适应学习率与动量 (15:33)](https://www.youtube.com/watch?v=eUOvUIRPSX8) | [🎮 sgd-scheduler-momentum.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L12/code/sgd-scheduler-momentum.ipynb)  [🎮 adam.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L12/code/adam.ipynb) |
| 95 | [🎥 L12.5 在 PyTorch 中选择不同的优化器 (06:01)](https://www.youtube.com/watch?v=c-SRPvK_zzs) |  |
| 96 | [🎥 L12.6 优化算法的其他主题与研究 (12:04)](https://www.youtube.com/watch?v=7yoAocFiUh8) |  |

## 第 4 部分：面向计算机视觉与语言建模的深度学习

### L13：卷积神经网络导论

|  | 视频 | 资料 |
| --- | --- | --- |
| 97 | [🎥 L13.0 卷积网络导论——课程概览 (05:25)](https://www.youtube.com/watch?v=i-Ngb6tn_KM) | 📝 [L13\_intro-cnn\_\_slides.pdf](https://sebastianraschka.com/pdf/lecture-notes/stat453ss21/L13_intro-cnn__slides.pdf) |
| 98 | [🎥 L13.1 CNN 的常见应用 (09:34)](https://www.youtube.com/watch?v=I5B7pgSEMhE) |  |
| 99 | [🎥 L13.2 图像分类的挑战 (07:44)](https://www.youtube.com/watch?v=0FtJbmuUdFo) |  |
| 100 | [🎥 L13.3 卷积神经网络基础 (18:39)](https://www.youtube.com/watch?v=7fWOE-z8YgY) |  |
| 101 | [🎥 L13.4 卷积滤波器与权重共享 (20:19)](https://www.youtube.com/watch?v=ryJ6Bna-ZNU) |  |
| 102 | [🎥 L13.5 互相关与卷积 (10:37)](https://www.youtube.com/watch?v=xbO-iIzkBy0) | [🎮 cross-correlation.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L13/code/notes/cross-correlation.ipynb) |
| 103 | [🎥 深度学习新闻 #8 (18:02)](https://www.youtube.com/watch?v=AxKPjkBP2t4) | 📝 [stuff-in-the-news-08.pdf](https://sebastianraschka.com/pdf/lecture-notes/stuff-in-the-news/stuff-in-the-news-08.pdf) |
| 104 | [🎥 L13.6 CNN 与反向传播 (05:54)](https://www.youtube.com/watch?v=-SwKNK9MIUU) |  |
| 105 | [🎥 L13.7 CNN 架构与 AlexNet (20:17)](https://www.youtube.com/watch?v=-IHxe4-09e4) |  |
| 106 | [🎥 L13.8 CNN 能"看到"什么 (13:42)](https://www.youtube.com/watch?v=PRFP5YC3u7g) |  |
| 107 | [🎥 L13.9.1 PyTorch 中的 LeNet-5 (13:11)](https://www.youtube.com/watch?v=ye5k82FQC7I) | [🎮 1-lenet5-mnist.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L13/code/1-lenet5-mnist.ipynb) |
| 108 | [🎥 L13.9.2 PyTorch 中模型的保存与加载 (05:44)](https://www.youtube.com/watch?v=vB_Y04gsyBI) | [🎮 save-and-load](https://github.com/rasbt/stat453-deep-learning-ss21/tree/main/L13/code/save-and-load) |
| 109 | [🎥 L13.9.3 PyTorch 中的 AlexNet (15:15)](https://www.youtube.com/watch?v=mlXRVuD_HEg) | [🎮 2-alexnet-cifar10.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L13/code/2-alexnet-cifar10.ipynb) |
| 110 | [🎥 深度学习新闻 #9 (28:09)](https://www.youtube.com/watch?v=Nm4Y4Pd1mg0) | 📝 [stuff-in-the-news-09.pdf](https://sebastianraschka.com/pdf/lecture-notes/stuff-in-the-news/stuff-in-the-news-09.pdf) |

### L14：卷积神经网络架构

|  | 视频 | 资料 |
| --- | --- | --- |
| 111 | [🎥 L14.0: 卷积神经网络架构——课程概览 (06:18)](https://www.youtube.com/watch?v=1A6HViSXaqQ) | 📝 [L14\_cnn-architectures\_slides.pdf](https://sebastianraschka.com/pdf/lecture-notes/stat453ss21/L14_cnn-architectures_slides.pdf) |
| 112 | [🎥 L14.1: 卷积与填充 (11:14)](https://www.youtube.com/watch?v=6v05kAtV1M0) |  |
| 113 | [🎥 L14.2: 空间 Dropout 与 BatchNorm (06:46)](https://www.youtube.com/watch?v=TGqqTgn4cAg) |  |
| 114 | [🎥 L14.3: 架构概览 (03:23)](https://www.youtube.com/watch?v=WyXO762G2_A) |  |
| 115 | [🎥 L14.3.1.1 VGG16 概览 (06:05)](https://www.youtube.com/watch?v=YcmNIOyfdZQ) |  |
| 116 | [🎥 L14.3.1.2 PyTorch 中的 VGG16 (15:52)](https://www.youtube.com/watch?v=PlFiRPdBEAo) | [🎮 1.1-vgg16.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L14/1.1-vgg16.ipynb) |
| 117 | [🎥 L14.3.2.1 ResNet 概览 (14:41)](https://www.youtube.com/watch?v=q_IlqYlYhlo) |  |
| 118 | [🎥 L14.3.2.2 PyTorch 中的 ResNet-34 (18:47)](https://www.youtube.com/watch?v=JG_ODvnlgjY) | [🎮 2-resnet-example.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L14/2-resnet-example.ipynb)  [🎮 2-resnet34.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L14/2-resnet34.ipynb) |
| 120 | [🎥 L14.4.1 用卷积层取代最大池化 (08:19)](https://www.youtube.com/watch?v=Lq83NFkkJCk) |  |
| 121 | [🎥 L14.4.2 PyTorch 中的全卷积网络 (08:17)](https://www.youtube.com/watch?v=A5dC5yuPXwo) | [🎮 3-all-convnet.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L14/3-all-convnet.ipynb) |
| 122 | [🎥 L14.5 用卷积层替代全连接层 (14:33)](https://www.youtube.com/watch?v=rqLjZ8k4va8) |  |
| 123 | [🎥 L14.6.1 迁移学习 (07:38)](https://www.youtube.com/watch?v=OkQRtm9JY1k) |  |
| 124 | [🎥 L14.6.2 PyTorch 中的迁移学习 (11:35)](https://www.youtube.com/watch?v=FaW9JCSJn2s) | [🎮 5-transfer-learning-vgg16\_small.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L14/5-transfer-learning-vgg16_small.ipynb)  [🎮 5-transfer-learning-vgg16\_large.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L14/5-transfer-learning-vgg16_large.ipynb) |
| 119 | [🎥 深度学习新闻 #10 (20:55)](https://www.youtube.com/watch?v=sZT4XZkptP8) | 📝 [stuff-in-the-news-10.pdf](https://sebastianraschka.com/pdf/lecture-notes/stuff-in-the-news/stuff-in-the-news-10.pdf) |

### L15：循环神经网络导论

|  | 视频 | 资料 |
| --- | --- | --- |
| 125 | [🎥 L15.0: 循环神经网络导论——课程概览 (03:58)](https://www.youtube.com/watch?v=q5YxK17tRm0) | 📝 [L15\_intro-rnn\_\_slides.pdf](https://sebastianraschka.com/pdf/lecture-notes/stat453ss21/L15_intro-rnn__slides.pdf) |
| 126 | [🎥 L15.1: 处理文本数据的各种方法 (15:57)](https://www.youtube.com/watch?v=kwmZtkzB4e0) |  |
| 127 | [🎥 L15.2 用 RNN 进行序列建模 (13:39)](https://www.youtube.com/watch?v=5fdy-hBeWCI) |  |
| 128 | [🎥 L15.3 不同类型的序列建模任务 (04:31)](https://www.youtube.com/watch?v=Ed8GTvkzkZE) |  |
| 129 | [🎥 L15.4 随时间反向传播概览 (09:33)](https://www.youtube.com/watch?v=0XdPIqi0qpg) |  |
| 130 | [🎥 L15.5 长短期记忆（LSTM） (16:58)](https://www.youtube.com/watch?v=k6fSgUaWUF8) |  |
| 131 | [🎥 L15.6 用于分类的 RNN：多对一单词 RNN (29:06)](https://www.youtube.com/watch?v=TI4HRR3Hd9A) |  |
| 132 | [🎥 L15.7 PyTorch 中的 RNN 情感分类器 (40:00)](https://www.youtube.com/watch?v=KgrdifrlDxg) | [🎮 1\_lstm.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L15/1_lstm.ipynb)  [🎮 2\_packed-lstm.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L15/2_packed-lstm.ipynb) |

## 第 5 部分：深度生成模型

### L16：自编码器

|  | 视频 | 资料 |
| --- | --- | --- |
| 133 | [🎥 L16.0 自编码器导论——课程概览 (04:45)](https://www.youtube.com/watch?v=9Ujv_IoBtF4) | 📝 [L16\_autoencoder\_\_slides.pdf](https://sebastianraschka.com/pdf/lecture-notes/stat453ss21/L16_autoencoder__slides.pdf) |
| 134 | [🎥 L16.1 降维 (09:39)](https://www.youtube.com/watch?v=UgOHupaIfcA) |  |
| 135 | [🎥 L16.2 全连接自编码器 (16:34)](https://www.youtube.com/watch?v=8O_FDPIlj1s) |  |
| 136 | [🎥 L16.3 卷积自编码器与转置卷积 (16:07)](https://www.youtube.com/watch?v=ilkSwsggSNM) |  |
| 137 | [🎥 L16.4 PyTorch 中的卷积自编码器 (15:20)](https://www.youtube.com/watch?v=345wRyqKkQ0) | [🎮 conv-autoencoder\_mnist.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L16/conv-autoencoder_mnist.ipynb) |
| 138 | [🎥 L16.5 其他类型的自编码器 (5:33)](https://www.youtube.com/watch?v=FPZeRM1p1ao) |  |

### L17：变分自编码器

|  | 视频 | 资料 |
| --- | --- | --- |
| 139 | [🎥 L17.0 变分自编码器导论——课程概览 (03:16)](https://www.youtube.com/watch?v=UnImUYOdWgk) | 📝 [L17\_vae\_\_slides.pdf](https://sebastianraschka.com/pdf/lecture-notes/stat453ss21/L17_vae__slides.pdf) |
| 140 | [🎥 L17.1 变分自编码器概览 (05:23)](https://www.youtube.com/watch?v=H2XgdND0DV4) |  |
| 141 | [🎥 L17.2 从变分自编码器采样 (09:26)](https://www.youtube.com/watch?v=YgSWrafXI8U) |  |
| 142 | [🎥 L17.3 log 方差技巧（Log-Var Trick） (07:34)](https://www.youtube.com/watch?v=pmvo0S3-G-I) |  |
| 143 | [🎥 L17.4 变分自编码器的损失函数 (12:16)](https://www.youtube.com/watch?v=ywYuZrLENH0) |  |
| 144 | [🎥 L17.5 PyTorch 中用于手写数字的变分自编码器 (23:12)](https://www.youtube.com/watch?v=afNuE5z2CQ8) | [🎮 1\_VAE\_mnist\_sigmoid\_mse.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L17/1_VAE_mnist_sigmoid_mse.ipynb) |
| 145 | [🎥 L17.6 PyTorch 中用于人脸图像的变分自编码器 (10:05)](https://www.youtube.com/watch?v=sul2ExoUrnw) | [🎮 2\_VAE\_celeba-sigmoid\_mse.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L17/2_VAE_celeba-sigmoid_mse.ipynb)  [🎮 3\_VAE\_nearest-neighbor-upsampling.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L17/3_VAE_nearest-neighbor-upsampling.ipynb)  [🎮 5\_VAE\_celeba\_latent-arithmetic.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L17/5_VAE_celeba_latent-arithmetic.ipynb) |
| 146 | [🎥 L17.7 PyTorch 中的 VAE 潜在空间运算——让人微笑起来 (11:54)](https://www.youtube.com/watch?v=EfFr87ARDF0) | [🎮 5\_VAE\_celeba\_latent-arithmetic.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L17/5_VAE_celeba_latent-arithmetic.ipynb) |

### L18：生成对抗网络导论

|  | 视频 | 资料 |
| --- | --- | --- |
| 147 | [🎥 L18.0: 生成对抗网络导论——课程概览 (05:14)](https://www.youtube.com/watch?v=OnoPaZaKoS8) | 📝 [L18\_gan\_\_slides.pdf](https://sebastianraschka.com/pdf/lecture-notes/stat453ss21/L18_gan__slides.pdf) |
| 148 | [🎥 L18.1: GAN 背后的核心思想 (10:42)](https://www.youtube.com/watch?v=-Zi5SReze6U) |  |
| 149 | [🎥 L18.2: GAN 的目标函数 (26:25)](https://www.youtube.com/watch?v=m_H6viKCTEE) |  |
| 150 | [🎥 L18.3: 为实际应用改造 GAN 损失函数 (18:45)](https://www.youtube.com/watch?v=ILpC3b-819Q) |  |
| 151 | [🎥 L18.4: PyTorch 中生成手写数字的 GAN (22:45)](https://www.youtube.com/watch?v=cTlxZ1FO1mY) | [🎮 04\_01\_gan-mnist.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L18/04_01_gan-mnist.ipynb) |
| 152 | [🎥 L18.5: 让 GAN 正常工作的技巧与诀窍 (17:13)](https://www.youtube.com/watch?v=_cUdjPdbldQ) | [🎮 https://github.com/soumith/ganhacks](https://github.com/soumith/ganhacks) |
| 153 | [🎥 L18.6: PyTorch 中生成人脸图像的 DCGAN (12:42)](https://www.youtube.com/watch?v=5fs9PMzrVig) | [🎮 04\_02\_dcgan-celeba.ipynb](https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L18/04_02_dcgan-celeba.ipynb) |

### L19：[自注意力](https://sebastianraschka.com/glossary/#mha "Multi-Head Attention (MHA)")与 Transformer 网络

|  | 视频 | 资料 |
| --- | --- | --- |
| 154 | [🎥 L19.0 用于序列到序列建模的 RNN 与 Transformer——课程概览 (03:05)](https://www.youtube.com/watch?v=DlWTTrHa8bI) | 📝 [L19\_seq2seq\_rnn-transformers\_\_slides.pdf](https://sebastianraschka.com/pdf/lecture-notes/stat453ss21/L19_seq2seq_rnn-transformers__slides.pdf) |
| 155 | [🎥 L19.1 用单词级和字符级 RNN 生成序列 (17:43)](https://www.youtube.com/watch?v=fSBw6TrePPg) |  |
| 156 | [🎥 L19.2.1 在 PyTorch 中实现字符级 RNN（概念） (09:19)](https://www.youtube.com/watch?v=PFcWQkGP4lU) |  |
| 157 | [🎥 L19.2.2 在 PyTorch 中实现字符级 RNN（代码示例） (25:56)](https://www.youtube.com/watch?v=tL5puCeDr-o) | [🎮 character-rnn](https://github.com/rasbt/stat453-deep-learning-ss21/tree/main/L19/character-rnn) |
| 158 | [🎥 L19.3 带注意力机制的 RNN (22:18)](https://www.youtube.com/watch?v=mDZil99CtSU) |  |
| 159 | [🎥 L19.4.1 抛开 RNN 使用注意力——自注意力的基本形式 (16:10)](https://www.youtube.com/watch?v=i_pfHD4P_wg) |  |
| 160 | [🎥 L19.4.2 自注意力与缩放点积注意力 (16:08)](https://www.youtube.com/watch?v=0PjHri8tc1c) |  |
| 161 | [🎥 L19.4.3 多头注意力 (07:36)](https://www.youtube.com/watch?v=A1eUVxscNq8) |  |
| 162 | [🎥 L19.5.1 Transformer 架构 (22:36)](https://www.youtube.com/watch?v=tstbZXNCfLY) |  |
| 163 | [🎥 L19.5.2.1 几个流行的 Transformer 模型：BERT、GPT 与 BART——概览 (08:40)](https://www.youtube.com/watch?v=iFhYwEi03Ew) |  |
| 164 | [🎥 L19.5.2.2 GPT-v1：生成式预训练 Transformer (09:53)](https://www.youtube.com/watch?v=LOCzBgSV4tQ) |  |
| 165 | [🎥 L19.5.2.3 BERT：来自 Transformer 的双向编码器表示 (18:30)](https://www.youtube.com/watch?v=_BFp4kjSB-I) |  |
| 166 | [🎥 L19.5.2.4 GPT-v2：语言模型是无监督多任务学习器 (09:02)](https://www.youtube.com/watch?v=BXv1m9Asl7I) |  |
| 167 | [🎥 L19.5.2.5 GPT-v3：语言模型是少样本学习器 (06:40)](https://www.youtube.com/watch?v=wYdKn-X4MhY) |  |
| 168 | [🎥 L19.5.2.6 BART：结合双向与自回归 Transformer (10:15)](https://www.youtube.com/watch?v=1JBMCG8rW18) |  |
| 169 | [🎥 L19.5.2.7: 结语——语言 Transformer 的近期发展 (06:09)](https://www.youtube.com/watch?v=OyqIuxMmLRg) |  |
| 170 | [🎥 L19.6 PyTorch 中的 DistilBERT 影评分类器 (17:57)](https://www.youtube.com/watch?v=emDmznRlsWw) | [🎮 distilbert-classifier](https://github.com/rasbt/stat453-deep-learning-ss21/tree/main/L19/distilbert-classifier) |
