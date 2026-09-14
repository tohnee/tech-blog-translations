---
title: "数值矩阵操作"
title_en: "Numeric matrix manipulation"
source: https://sebastianraschka.com/Articles/2014_matrix_cheatsheet.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 数值矩阵操作

> 原文：[Numeric matrix manipulation](https://sebastianraschka.com/Articles/2014_matrix_cheatsheet.html) · Sebastian Raschka's Articles

这篇文章的核心内容是一份关于数值矩阵基本操作的简易速查表（cheat sheet）。如果你正在使用并试验一些最流行的用于科学计算、统计学和数据分析的编程语言，它可能会非常有用。

## 章节

## 引言

矩阵（或多维数组）不仅是许多代数方程的基本要素——这些方程被广泛应用于模式分类、机器学习、数据挖掘，以及整个数学与工程领域；在科学计算的语境下，它们还能以更有组织的表格形式来管理和存储数据，用起来非常顺手。
得益于自动向量化（automatic vectorization）的概念，这类多维数据结构在性能方面也非常强大：不必再在循环结构中对标量逐个、顺序地执行操作，整个计算都可以被并行化，从而充分利用现代计算机体系结构。

![Matrix cheatsheet matcheat matrix](https://sebastianraschka.com/images/blog/2014/numeric-matrix/matcheat_matrix.webp)

### 语言概览

在我们**[跳转到真正的速查表](#cheatsheet)**之前，我想至少先简要介绍一下我们将要涉及的几种不同的语言。

MATLAB/Octave、Python、R 和 Julia 这四种语言都是动态类型的，都带有解释器的命令行界面，并且都附带了数量可观的额外实用程序库，以支持科学与技术计算。方便的是，这些语言还为轻松绘图和可视化提供了出色的解决方案。

再结合交互式 notebook 界面或动态报告生成引擎（MATLAB 的 [MuPAD](http://www.mathworks.com/discovery/mupad.html)、Python 的 [IPython Notebook](https://ipython.readthedocs.io/en/3.x/notebook/notebook.html)、R 的 [knitr](http://yihui.name/knitr/)，以及基于 IPython Notebook 的 Julia 的 [IJulia](https://github.com/JuliaLang/IJulia.jl)），数据分析和文档编写从未如此轻松。

## MATLAB/Octave

[![Matrix cheatsheet matcheat matlab logo](https://sebastianraschka.com/images/blog/2014/numeric-matrix/matcheat_matlab_logo.webp)](http://www.mathworks.com/products/matlab/)

[MATLAB](http://www.mathworks.com/products/matlab/)（代表 MATrix LABoratory，即「矩阵实验室」）是一款应用程序兼编程语言的名字，由 [MathWorks](http://www.mathworks.com/index.html?s_tid=gn_logo) 公司早在

1. 它的一大优势在于拥有各种各样高度优化的「工具箱」（包括用于图像及其他信号处理任务的非常强大的函数），这使它几乎适合解决所有可能的科学与工程任务。
   与本文将要介绍的其他语言一样，它支持跨平台并使用动态类型，这带来了便利的接口，但在对大型数据集进行计算时也可能会相当「吃内存」。

即使在今天，MATLAB 可能（仍然）是学术界和工业界的工程任务中最流行的数值计算语言。

### GNU Octave

[![Matrix cheatsheet matcheat octave logo](https://sebastianraschka.com/images/blog/2014/numeric-matrix/matcheat_octave_logo.webp)](http://www.gnu.org/software/octave/)

值得一提的是，MATLAB 是这份速查表中唯一一款非免费、非开源的语言。但由于它实在太流行了，我还是想把它列进来。作为替代方案，还有免费的 [GNU Octave 重新实现](http://www.gnu.org/software/octave/)，它遵循相同的语法规则，因此代码与 MATLAB 兼容（非常专门化的程序库除外）。

> 这张[图片](https://commons.wikimedia.org/wiki/File:Matlab_Logo.png)是一张处于公有领域、可自由使用的媒体素材，描绘的是 L 形薄膜的第一本征函数，与 MathWorks Inc. 注册了商标的 MATLAB logo 相似（但并不相同）。

## Python NumPy

![Matrix cheatsheet matcheat numpy logo](https://sebastianraschka.com/images/blog/2014/numeric-matrix/matcheat_numpy_logo.webp)

最初，[NumPy](http://www.numpy.org) 项目于 1995 年以「Numeric」之名起步（2006 年更名为 NumPy），是一个基于数组、矩阵等多维数据结构进行数值计算的 Python 程序库。由于它在对「`ndarray`」对象执行操作时使用了预编译的 C 代码，因此比在 (C)Python 中使用等价的做法要快得多。

Python NumPy 是我的个人最爱，因为我是 Python 编程语言的铁杆粉丝。尽管其他语言也存在类似的工具，但我发现在 [IPython notebook](https://ipython.readthedocs.io/en/3.x/notebook/notebook.html) 中做研究和数据分析时我的效率最高。
它让我可以轻松地把 Python 代码（如果在意速度，有时会通过 [Cython](http://cython.org) C 扩展或即时（JIT）编译器 [Numba](http://numba.pydata.org) 编译来优化）与 [Scipy 技术栈](http://www.scipy.org/)中的各种程序库结合起来，其中包括用于内联数据可视化的 [matplotlib](http://matplotlib.org)（你可以在这个 [GitHub 仓库](https://github.com/rasbt/One-Python-benchmark-per-day)中找到我的一些示例基准测试）。

## R

![Matrix cheatsheet matcheat R logo](https://sebastianraschka.com/images/blog/2014/numeric-matrix/matcheat_R_logo.webp)

[R](http://www.r-project.org) 编程语言开发于 1993 年，是一门更早的统计编程语言——[S 语言](http://stat.bell-labs.com/S/)（1976 年在[贝尔实验室](http://stat.bell-labs.com)开发）——的现代 GNU 实现。自发布以来，R 的用户群体快速增长，尤其在统计学家当中特别受欢迎。

R 也是第一门点燃我对统计学和计算之热情的语言。几年前，在发现 Python 成为我做数据分析的新宠语言之前，我曾相当广泛地使用过它。
尽管 R 内置了用于执行各种统计的出色函数，而且庞大的 R 社区还贡献了海量免费可用的程序库，我还是经常听到有人抱怨它那相当不直观的语法。

## Julia

![Matrix cheatsheet matcheat julia logo](https://sebastianraschka.com/images/blog/2014/numeric-matrix/matcheat_julia_logo.webp)

[Julia](http://julialang.org) 于 2012 年首次发布，是本文提到的编程语言中远为最年轻的一门。虽然 Julia 也可以像解释型语言一样在命令行中以动态类型使用，但它的目标是在科学计算中实现高性能——得益于其基于 LLVM 的即时（JIT）编译器，它的性能优于其他用于技术计算的动态编程语言。

就我个人而言，我还没有太深入地使用过 Julia，不过已经有一些看起来非常有前景、令人兴奋的基准测试：

[![Matrix cheatsheet matcheat julia benchmark](https://sebastianraschka.com/images/blog/2014/numeric-matrix/matcheat_julia_benchmark.webp)](http://julialang.org/benchmarks/)

> C 由 gcc 4.8.1 编译，取所有优化级别（-O0 到 -O3）中的最佳计时。C、Fortran 和 Julia 使用 OpenBLAS v0.2.8。rand\_mat\_stat 和 rand\_mat\_mul 的 Python 实现使用 NumPy（v1.6.1）函数；其余均为纯 Python 实现。

> Bezanson, J., Karpinski, S., Shah, V.B. and Edelman, A. (2012), “Julia:
> A fast dynamic language for technical computing”.
> （来源：<http://julialang.org/benchmarks/>，已获版权持有者许可）

## 速查表

[![Matrix cheatsheet matrix cheatsheet](https://sebastianraschka.com/images/blog/2014/numeric-matrix/matrix_cheatsheet.webp)](https://sebastianraschka.com/blog/2014/matrix_cheatsheet_table.html)

### 备选数据结构：NumPy 矩阵 vs. NumPy 数组

Python 的 NumPy 库还有一个专门的「matrix（矩阵）」类型，其语法与 MATLAB 矩阵稍微更接近一些：例如，「 `*` 」运算符对 NumPy 矩阵执行的是矩阵-矩阵乘法，而同一个运算符对 NumPy 数组执行的是逐元素乘法。

反过来，「`.dot()`」方法用于 NumPy 矩阵的逐元素乘法；而对 NumPy 数组而言，等价的操作则要通过「 `*` 」运算符来实现。

**大多数人推荐使用 NumPy 数组（array）类型而非 NumPy 矩阵（matrix），因为 NumPy 的大多数函数返回的都是数组。**
