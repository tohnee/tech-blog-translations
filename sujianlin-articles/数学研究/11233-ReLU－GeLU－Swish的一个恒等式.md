---
title: "ReLU/GeLU/Swish的一个恒等式"
date: "2025-08-16"
author: "苏剑林"
category: "数学研究"
tags: ["分析", "神经网络", "恒等式"]
url: "https://kexue.fm/archives/11233"
blog: "科学空间 | Scientific Spaces"
---

今天水一点轻松的内容，它基于笔者这两天意识到的一个恒等式。这个恒等式实际上很简单，但初看之下会有点意料之外的感觉，所以来记录一下。

## 基本结果
我们知道$\newcommand{relu}{\mathop{\text{relu}}}\relu(x) = \max(x, 0)$，容易证明如下恒等式
\begin{equation}x = \relu(x) - \relu(-x)\end{equation}
如果$x$是一个向量，那么上式就更直观了，$\relu(x)$是提取出$x$的正分量，$- \relu(-x)$是提取出$x$的负分量，两者相加就得到原本的向量。

## 一般结论
接下来的问题是[GeLU](https://kexue.fm/archives/7309)、[Swish](https://papers.cool/arxiv/1710.05941)等激活函数成立类似的恒等式吗？初看之下并不成立，然而事实上是成立的！我们甚至还有更一般的结论：

> 设$\phi(x)$是任意奇函数，$f(x)=\frac{1}{2}(\phi(x) + 1)x$，那么恒成立
> \begin{equation}x = f(x) - f(-x)\end{equation}

证明该结论也是一件很轻松的事，这里就不展开了。对于Swish来说我们有$\phi(x) = \tanh(\frac{x}{2})$，对于GeLU来说则有$\phi(x)=\mathop{\text{erf}}(\frac{x}{\sqrt{2}})$，它们都是奇函数，所以成立同样的恒等式。

## 意义思考
上述恒等式写成矩阵形式是
\begin{equation}x = f(x) - f(-x) = f(x[1, -1])\begin{bmatrix}1 \\ -1\end{bmatrix}\end{equation}
这表明以ReLU、GeLU、Swish等为激活函数时，两层神经网络有退化为一层的能力，这意味着它们可以自适应地调节模型的实际深度，这与ResNet的工作原理异曲同工，这也许是这些激活函数为什么比传统的Tanh、Sigmoid等更好的原因之一。
