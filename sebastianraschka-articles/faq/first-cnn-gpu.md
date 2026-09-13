---
title: "Early Convolutional Neural Networks Trained on GPUs"
source: https://sebastianraschka.com/faq/docs/first-cnn-gpu.html
crawled: 2026-09-06
---

# Early Convolutional Neural Networks Trained on GPUs

The canonical example is [AlexNet (2012)](https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html) by Sutskever and Hinton [1]. However, despite this common belief, Ciresan et al. from Schmidhuber’s lab published the successful training of convolutional neural networks (CNNs) one year before AlexNet in “[Flexible, High Performance Convolutional Neural Networks for Image Classification](https://people.idsia.ch/~juergen/ijcai2011.pdf)” [2].

Note that according to the paper mentioned above, CNN training on GPUs goes even back further to the works by [Chellapilla et al. (2006)](https://hal.inria.fr/inria-00112631/document) [3], [Uetz and Behnke (2009)](https://ieeexplore.ieee.org/abstract/document/5357786/) [4], and [Strigl et al. (2010)](https://ieeexplore.ieee.org/abstract/document/5452452/) [5]. However, these GPU implementations were primarily based on hard-coded code and are less flexible (for example, they don’t support online stochastic gradient descent, that is, updating after each image).

## References

[1] Krizhevsky, Alex, Ilya Sutskever, and Geoffrey E. Hinton. “[Imagenet classification with deep convolutional neural networks](https://proceedings.neurips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html).” Advances in Neural Information Processing Systems 25 (2012).

[2] Ciresan, Dan Claudiu, Ueli Meier, Jonathan Masci, Luca Maria Gambardella, and Jürgen Schmidhuber. “[Flexible, high performance convolutional neural networks for image classification](https://people.idsia.ch/~juergen/ijcai2011.pdf).” In Twenty-second International Joint Conference on Artificial Intelligence. 2011.

[3] Kumar Chellapilla, Sidd Puri, and Patrice Simard. “[High performance convolutional neural networks for document processing](https://hal.inria.fr/inria-00112631/document).” In International Workshop on Frontiers in Handwriting Recognition, 2006.

[4] Uetz, Rafael, and Sven Behnke. “[Large-scale object recognition with CUDA-accelerated hierarchical neural networks](https://ieeexplore.ieee.org/abstract/document/5357786/).” In 2009 IEEE international conference on intelligent computing and intelligent systems, vol. 1, pp. 536-541. IEEE, 2009.

[5] Daniel Strigl, Klaus Kofler, and Stefan Podlipnig. “[Performance and scalability of GPU-based convolutional neural networks](https://ieeexplore.ieee.org/abstract/document/5452452/).” In 18th Euromicro Conference on Parallel, Distributed, and Network-Based Processing, 2010.
