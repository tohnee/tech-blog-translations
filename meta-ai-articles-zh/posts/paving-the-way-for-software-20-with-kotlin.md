---
title: "用 Kotlin 为 Software 2.0 铺路"
title_en: "Paving the way for Software 2.0 with Kotlin"
date: 2020-11-17
source: https://ai.facebook.com/blog/paving-the-way-for-software-20-with-kotlin
crawled: 2026-09-22
translated: 2026-09-22
---

# 用 Kotlin 为 Software 2.0 铺路

> 原文：[Paving the way for Software 2.0 with Kotlin](https://ai.facebook.com/blog/paving-the-way-for-software-20-with-kotlin) · Meta AI（Wayback 存档）

我们在可微编程（differentiable programming，让程序自我优化）方面的工作，是 Facebook AI 构建更先进的机器学习（ML）编程工具这一更广泛努力的一部分。正因如此，我们正在扩展 Kotlin 编译器，把可微性变成 Kotlin 语言的一等特性，同时开发一套张量类型系统。我们的工作让开发者能够通过以下方式探索 Software 2.0（软件本质上是自我书写的）：

- 对基元、数据结构和控制流无缝求导
- 张量类型：静态的编译期形状推断与检查
- 可微函数与张量形状的编译期错误报告
- 一个高性能库，提供 Tensor 类和机器学习 API

通过在 Kotlin 中实现直观且高性能的可微编程，我们让开发者能够创建强大、灵活、充分利用问题结构的程序，同时无缝保持类型安全并让调试保持简单。

## 为什么需要可微编程？

今天的大多数代码要么是可学习的（用受限的机器学习库编写），要么是显式编程的（用传统编码范式编写）。实现 Software 2.0 的一个主要障碍在于：这两种方法之间没有真正的兼容性。以 Cartpole 强化学习模型为例。Cartpole 的目标是学会在小车上平衡一根杆。但该模型从零知识开始，不得不通过试错来学习物理定律——尽管已经存在许多用传统代码编写的出色物理模拟器。如果模型能利用这些现成的模拟器，岂不是更高效？

可微编程解决了这个问题。在可微编程中，任意的用户（或库）代码都可以被纳入更全面的模型。可微编程还允许开发者利用梯度，自动优化那些并非用 ML 库编写的参数化程序。我们正在为 Kotlin 语言构建一套自动微分系统。

（学习平衡杆六次迭代后的两个 Cartpole 模型。左边的模型没有把环境的物理规律纳入其中，右边的则纳入了。）

## 自动微分

这种自动微分（AD）发生在编译期，保留了程序结构（如控制流和函数调用），并支持在运行时做 AD 时不可行的编译器优化。我们为 Kotlin 的 float 和 double 提供可微性，并提供一个定义自定义可微数据类型的框架。我们的团队利用该框架还提供了可微的 Tensor 类。这使用户既能对以 Kotlin 表达的传统 ML 模型求导，也能对任意 Kotlin 代码求导。

下面是一个体现我们语言扩展易用性的简单例子：

```kotlin
differentiable fun centripetalAccel(velocity: Float, radius: Float) = (velocity * velocity) / radius

val gradients = grads(::centripetalAccel, 8f, 2f)
```

differentiable 修饰符在语法上类似于 suspend 修饰符，放在函数之前表示该函数是可微的，且只能调用其他可微函数。当可微函数调用不可微函数时，我们会抛出编译期错误，在开发过程中直接显示在 IDE 里。这与当今许多动态框架形成鲜明对比——在那些框架里，你可能错误地调用了不可微函数，直到程序执行到很深的地方才得到报错，甚至根本得不到错误，只留下一个难以追查的错误结果。

函数 grads 接受一个函数引用和一个求导的点。这段代码执行后，gradients.velocity 将是 centripetalAccel 关于 velocity 的导数，即 8f；类似地，gradients.radius 是关于 radius 的导数，即 -16f。

我们的库包含加法、乘法等基元内建操作的导数，因此编译器可以推理并计算这些函数组合（如 centripetalAccel）的导数。我们的系统还允许开发者添加带自定义导数的函数。自定义导数让开发者可以试验自定义数据类型，编写含有不具备内建导数成分的函数。例如：

```kotlin
differentiable fun sigmoid(x: Float): Float = 1f / (1f + math.exp(x))

@PullbackOf(::sigmoid)
fun pullback_sigmoid(x: Float): (Float) -> sigmoid.TangentType = { upstream: Float ->
    sigmoid.TangentType(upstream * sigmoid(x) * (1 - sigmoid(x))
}
```

这个 pullback 函数用于计算 sigmoid 函数的导数。这里 sigmoid 关于 x 的导数是 sigmoid(x) * (1 - sigmoid(x))，该导数按 upstream 缩放。类 sigmoid.TangentType 是自动生成的，让开发者可以按参数名解包梯度。

除了通过自定义 pullback 实现可扩展性，我们还允许开发者创建面向对象的程序。我们支持用户定义的可微类（含可微与不可微的方法和值），以及新的用户自定义可微数据类型。这些系统确保开发者可以对自己自然的面向对象代码求导，而不被限制在我们的库中。

```kotlin
differentiable class Model(includeBias: Boolean) {
    val weight = Tensor.random(Shape(2, 2))
    val bias = if (includeBias) Tensor.random(Shape(2)) else Tensor.zeros(Shape(2))

    differentiable fun forward(input: Tensor) = weight.matmul(input) + bias

    differentiable fun loss(data: Tensor, labels: Tensor): Tensor {
        return crossEntropyLoss(forward(data), labels)
    }

    fun hasBias(): Boolean = includeBias
}

val myModel = Model(true)
val gradients = grads(::Model.loss, myModel).receiver

gradients.weight // gradient of myModel with respect to weight
gradients.bias   // gradient of myModel with respect to bias
// gradients.includeBias is not defined because Booleans are not differentiable
```

编译器能识别类中哪些元素可微、哪些不可微。开发者可以把可微类的任何方法指定为可微。即使是不可微的方法（如返回 Boolean 的 hasBias）也允许出现在可微类中；但如果开发者通过添加修饰符要求 hasBias 可微，就会引发编译期错误。

## 张量类型

深度学习中的许多算子（如卷积）涉及对多维数组（即张量）的复杂操作。没有静态形状信息时，很容易混淆不同形状的张量，导致难以调试的运行时错误。有了张量类型，开发者获得编译期形状推断与检查。张量类型还带来更好的代码文档和清晰度。开发者可以用类型标注作为文档，记录可接受和期望的张量输入类型。类型别名和泛型可用来进一步提升代码的可读性、共享与复用。

下面是一个使用类型别名让文档更清晰的简单例子：

```kotlin
typealias BatchSize = 100
typealias Height = 40
typealias Width = 50

fun getFirst(
    input: Tensor<[BatchSize, Height, Width]>
): Tensor<[Height, Width]> {
    ...
}
```

此外，我们把对 Kotlin 语言的扩展集成到了 IntelliJ IDE，优先保障开发者体验，让开发者通过类型提示和错误红色下划线获得实时反馈。这样，张量形状可以在模型编写时（在构建或运行之前）就被检查。任何训练模型数小时、却因一个形状错误而中断进度的人，都知道这种反馈能在多大程度上节省时间、资源和挫败感。

（这是在 IntelliJ 中编写的一个简单卷积神经网络代码片段。输入数据流经多个层对象，开发者可以检查每一步产生的形状。注意第一维使用了泛型类型参数 N，表示可变的批次大小。）

（我们可以通过删除「maxPool2」层在代码中诱发错误。这会在第一个全连接层 fc1 处产生如下形状错误：fc1 期望形状为 N x 784 的张量，但实际到来的形状是 N x 3136。）

## 下一步

我们对这项工作将激发的生产力和创造力感到兴奋。为进一步推动可微编程的努力，我们还将发布一个充分利用我们 AD 和张量类型系统的用户库，让来自任何 ML 框架的工程师和开发者都能轻松迁移到我们的系统并在其上部署。

感谢可微编程语言团队为这项工作做出贡献的所有成员：Samantha Andow、Arturo Arenas Esparza、Irene Dea、Emilio Arroyo-Fang、Neal Gafter、Johann George、Melissa Grueter、Erik Meijer、Xipeng Shen、Steffi Stumpos、Alanna Tempest、Christy Warden 和 Shannon Yang。

**作者**

- Facebook 可微编程语言团队
