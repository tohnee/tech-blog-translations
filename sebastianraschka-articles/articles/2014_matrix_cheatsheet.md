---
title: "Numeric matrix manipulation"
source: https://sebastianraschka.com/Articles/2014_matrix_cheatsheet.html
crawled: 2026-09-06
---

# Numeric matrix manipulation

At its core, this article is about a simple cheat sheet for basic
operations on numeric matrices, which can be very useful if you working
and experimenting with some of the most popular languages that are used
for scientific computing, statistics, and data analysis.

## Sections

## Introduction

Matrices (or multidimensional arrays) are not only presenting the
fundamental elements of many algebraic equations that are used in many
popular fields, such as pattern classification, machine learning, data
mining, and math and engineering in general. But in context of
scientific computing, they also come in very handy for managing and
storing data in an more organized tabular form.  
Such multidimensional data structures are also very powerful
performance-wise thanks to the concept of automatic vectorization:
instead of the individual and sequential processing of operations on
scalars in loop-structures, the whole computation can be parallelized in
order to make optimal use of modern computer architectures.

![Matrix cheatsheet matcheat matrix](https://sebastianraschka.com/images/blog/2014/numeric-matrix/matcheat_matrix.webp)

### Language overview

Before we **[jump to the actual cheat sheet](#cheatsheet)**, I wanted to
give you at least a brief overview of the different languages that we
are dealing with.

All four languages, MATLAB/Octave, Python, R, and Julia are dynamically
typed, have a command line interface for the interpreter, and come with
great number of additional and useful libraries to support scientific
and technical computing. Conveniently, these languages also offer great
solutions for easy plotting and visualizations.

Combined with interactive notebook interfaces or dynamic report
generation engines
([MuPAD](http://www.mathworks.com/discovery/mupad.html) for MATLAB,
[IPython Notebook](https://ipython.readthedocs.io/en/3.x/notebook/notebook.html) for Python,
[knitr](http://yihui.name/knitr/) for R, and
[IJulia](https://github.com/JuliaLang/IJulia.jl) for Julia based on
IPython Notebook) data analysis and documentation has never been easier.

## MATLAB/Octave

[![Matrix cheatsheet matcheat matlab logo](https://sebastianraschka.com/images/blog/2014/numeric-matrix/matcheat_matlab_logo.webp)](http://www.mathworks.com/products/matlab/)

[MATLAB](http://www.mathworks.com/products/matlab/) (stands for MATrix
LABoratory) is the name of an application and language that was
developed by
[MathWorks](http://www.mathworks.com/index.html?s_tid=gn_logo) back in

1. One of its strengths is the variety of different and highly
   optimized “toolboxes” (including very powerful functions for image and
   other signal processing task), which makes suitable for tackling
   basically every possible science and engineering task.  
   Like the other languages, which will be covered in this article, it has
   cross-platform support and is using dynamic types, which allows for a
   convenient interface, but can also be quite “memory hungry” for
   computations on large data sets.

Even today, MATLAB is probably (still) the most popular language for
numeric computation used for engineering tasks in academia as well as in
industry.

### GNU Octave

[![Matrix cheatsheet matcheat octave logo](https://sebastianraschka.com/images/blog/2014/numeric-matrix/matcheat_octave_logo.webp)](http://www.gnu.org/software/octave/)

It is also worth mentioning that MATLAB is the only language in this
cheat sheet which is not free and open-sourced. But since it is so
immensely popular, I want to mention it nonetheless. And as an
alternative there is also the free [GNU Octave
re-implementation](http://www.gnu.org/software/octave/) that follows the
same syntactic rules so that the code is compatible to MATLAB (except
for very specialized libraries).

> This [image](https://commons.wikimedia.org/wiki/File:Matlab_Logo.png)
> is a freely usable media under public domain and represents the first
> eigenfunction of the L-shaped membrane, resembling (but not identical
> to) MATLAB’s logo trademarked by MathWorks Inc.

## Python NumPy

![Matrix cheatsheet matcheat numpy logo](https://sebastianraschka.com/images/blog/2014/numeric-matrix/matcheat_numpy_logo.webp)

Initially, the [NumPy](http://www.numpy.org) project started out under
the name “Numeric” in 1995 (renamed to NumPy in 2006) as a Python
library for numeric computations based on multi-dimensional data
structures, such as arrays and matrices. Since it makes use of
pre-compiled C code for operations on its “`ndarray`” objects, it is
considerably faster than using equivalent approaches in (C)Python.

Python NumPy is my personal favorite since I am a big fan of the Python
programming language. Although similar tools exist for other languages,
I found myself to be most productive doing my research and data analyses
in [IPython notebooks](https://ipython.readthedocs.io/en/3.x/notebook/notebook.html).  
It allows me to easily combine Python code (sometimes optimized by
compiling it via the [Cython](http://cython.org) C-Extension or the
just-in-time (JIT) [Numba](http://numba.pydata.org) compiler if speed is
a concern) with different libraries from the [Scipy
stack](http://www.scipy.org/) including
[matplotlib](http://matplotlib.org) for inline data visualization (you
can find some of my example benchmarks in this [GitHub
repository](https://github.com/rasbt/One-Python-benchmark-per-day)).

## R

![Matrix cheatsheet matcheat R logo](https://sebastianraschka.com/images/blog/2014/numeric-matrix/matcheat_R_logo.webp)

The [R](http://www.r-project.org) programming language was developed in
1993 and is a modern GNU implementation of an older statistical
programming language called [S](http://stat.bell-labs.com/S/), which was
developed in the [Bell Laboratories](http://stat.bell-labs.com) in 1976.
Since its release, it has a fast-growing user base and is particularly
popular among statisticians.

R was also the first language which kindled my fascination for
statistics and computing. I have used it quite extensively a couple of
years ago before I discovered Python as my new favorite language for
data analysis.  
Although R has great in-built functions for performing all sorts
statistics, as well as a plethora of freely available libraries
developed by the large R community, I often hear people complaining
about its rather unintuitive syntax.

## Julia

![Matrix cheatsheet matcheat julia logo](https://sebastianraschka.com/images/blog/2014/numeric-matrix/matcheat_julia_logo.webp)

With its first release in 2012, [Julia](http://julialang.org) is by far
the youngest of the programming languages mentioned in this article. a
While Julia can also be used as an interpreted language with dynamic
types from the command line, it aims for high-performance in scientific
computing that is superior to the other dynamic programming languages
for technical computing thanks to its LLVM-based just-in-time (JIT)
compiler.

Personally, I haven’t used Julia that extensively, yet, but there are
some exciting benchmarks that look very promising:

[![Matrix cheatsheet matcheat julia benchmark](https://sebastianraschka.com/images/blog/2014/numeric-matrix/matcheat_julia_benchmark.webp)](http://julialang.org/benchmarks/)

> C compiled by gcc 4.8.1, taking best timing from all optimization levels
> (-O0 through -O3). C, Fortran and Julia use OpenBLAS v0.2.8. The Python
> implementations of rand\_mat\_stat and rand\_mat\_mul use NumPy (v1.6.1)
> functions; the rest are pure Python implementations.

> Bezanson, J., Karpinski, S., Shah, V.B. and Edelman, A. (2012), “Julia:
> A fast dynamic language for technical computing”.  
> (Source: <http://julialang.org/benchmarks/>, with permission from the
> copyright holder)

## Cheat sheet

[![Matrix cheatsheet matrix cheatsheet](https://sebastianraschka.com/images/blog/2014/numeric-matrix/matrix_cheatsheet.webp)](https://sebastianraschka.com/blog/2014/matrix_cheatsheet_table.html)

### Alternative data structures: NumPy matrices vs. NumPy arrays

Python’s NumPy library also has a dedicated “matrix” type with a syntax
that is a little bit closer to the MATLAB matrix: For example, the
“ `*` ” operator would perform a matrix-matrix multiplication of NumPy
matrices - same operator performs element-wise multiplication on NumPy
arrays.

Vice versa, the “`.dot()`” method is used for element-wise
multiplication of NumPy matrices, wheras the equivalent operation would
for NumPy arrays would be achieved via the “ `*` “-operator.

**Most people recommend the usage of the NumPy array type over NumPy
matrices, since arrays are what most of the NumPy functions return.**
