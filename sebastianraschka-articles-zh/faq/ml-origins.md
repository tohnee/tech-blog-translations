---
title: "机器学习的起源是什么？"
title_en: "What are the origins of machine learning?"
source: https://sebastianraschka.com/faq/docs/ml-origins.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 机器学习的起源是什么？

我认为这一切都始于 McCulloch-Pitt（MCP）神经元，这是关于哺乳动物大脑中神经元如何工作的第一个模型：
W. S. McCulloch and W. Pitts. [A logical calculus of the ideas immanent in nervous activity](http://link.springer.com/article/10.1007/BF02459570). The bulletin of mathematical biophysics, 5(4):115–133, 1943.

请注意，线性回归等其他方法在当时早已被发明（F. Galton. [Regression towards mediocrity in hereditary stature](http://www.jstor.org/stable/2841583). Journal of the Anthropological Institute of Great Britain and Ireland, pages 246–263, 1886.）。在这里，我想从机器学习如何演化的角度，对机器学习和统计学做个区分。我把机器学习视为一个从人工智能研究中诞生的领域，因此追溯到 MCP 神经元。

然而，机器学习与统计学深深交织在一起。例如，我会把基于闭式解（正规方程）的线性回归分析主要描述为源自统计学领域的技术，而我会把采用随机梯度下降学习的线性回归归为一种机器学习技术。我认为机器学习早期的目标，是让算法能够自己"学习"出一个函数，而不是通过数学方式求解方程。

所以，我会说第一个真正的机器学习算法是感知机（perceptron）（F. Rosenblatt. The perceptron, a perceiving and recognizing automaton Project Para. Cornell Aeronautical Laboratory, 1957.）。随后出现的是用于自适应线性神经元的梯度下降算法（B. Widrow. Adaptive "Adaline" neuron using chemical "memistors". Number Technical Report 1553-2. Stanford Electron. Labs., Stanford, CA, October 1960.）。这些单一的学习单元随后被连接成多层架构，接着在大约 20 世纪上半叶出现了多层感知机（multi-layer perceptron）。

请注意，比如 Fisher 的线性判别分析（R. A. Fisher. [The use of multiple measurements in taxonomic problems](http://onlinelibrary.wiley.com/store/10.1111/j.1469-1809.1936.tb02137.x/asset/j.1469-1809.1936.tb02137.x.pdf;jsessionid=F0E7EFF219B2C2D94FF2B2981D3533E8.f04t03?v=1&t=igrkwkvk&s=631d3f737becda820356e6862bffc239e9b1f2d6). Annals of eugenics, 7(2):179–188, 1936），我会把它归入统计学界的发展——请注意，这发生在"机器学习"这个词被创造出来之前。
