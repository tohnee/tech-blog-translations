---
title: "最早在 GPU 上训练的卷积神经网络"
title_en: "Early Convolutional Neural Networks Trained on GPUs"
source: https://sebastianraschka.com/faq/docs/first-cnn-gpu.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 最早在 GPU 上训练的卷积神经网络

> 原文：[Early Convolutional Neural Networks Trained on GPUs](https://sebastianraschka.com/faq/docs/first-cnn-gpu.html) · Sebastian Raschka's FAQ

最经典的例子是 Sutskever 和 Hinton 等人的 [AlexNet（2012）](https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html) [1]。然而，尽管这是人们的普遍认知，来自 Schmidhuber 实验室的 Ciresan 等人早在 AlexNet 发表一年之前，就在《[Flexible, High Performance Convolutional Neural Networks for Image Classification](https://people.idsia.ch/~juergen/ijcai2011.pdf)》[2] 一文中公布了卷积神经网络（CNN）的成功训练。

值得注意的是，根据上面提到的论文，在 GPU 上训练 CNN 的历史还可以追溯到更早的工作：[Chellapilla et al.（2006）](https://hal.inria.fr/inria-00112631/document) [3]、[Uetz and Behnke（2009）](https://ieeexplore.ieee.org/abstract/document/5357786/) [4] 以及 [Strigl et al.（2010）](https://ieeexplore.ieee.org/abstract/document/5452452/) [5]。不过，这些 GPU 实现主要以硬编码代码为基础，灵活性较差（例如，它们不支持在线随机梯度下降，也就是逐张图像进行更新）。

## 参考文献

[1] Krizhevsky, Alex, Ilya Sutskever, and Geoffrey E. Hinton. “[Imagenet classification with deep convolutional neural networks](https://proceedings.neurips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html).” Advances in Neural Information Processing Systems 25 (2012).

[2] Ciresan, Dan Claudiu, Ueli Meier, Jonathan Masci, Luca Maria Gambardella, and Jürgen Schmidhuber. “[Flexible, high performance convolutional neural networks for image classification](https://people.idsia.ch/~juergen/ijcai2011.pdf).” In Twenty-second International Joint Conference on Artificial Intelligence. 2011.

[3] Kumar Chellapilla, Sidd Puri, and Patrice Simard. “[High performance convolutional neural networks for document processing](https://hal.inria.fr/inria-00112631/document).” In International Workshop on Frontiers in Handwriting Recognition, 2006.

[4] Uetz, Rafael, and Sven Behnke. “[Large-scale object recognition with CUDA-accelerated hierarchical neural networks](https://ieeexplore.ieee.org/abstract/document/5357786/).” In 2009 IEEE international conference on intelligent computing and intelligent systems, vol. 1, pp. 536-541. IEEE, 2009.

[5] Daniel Strigl, Klaus Kofler, and Stefan Podlipnig. “[Performance and scalability of GPU-based convolutional neural networks](https://ieeexplore.ieee.org/abstract/document/5452452/).” In 18th Euromicro Conference on Parallel, Distributed, and Network-Based Processing, 2010.
