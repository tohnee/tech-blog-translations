---
title: "在 macOS 上安装 Python 科学计算包"
title_en: "Python Scientific Packages on macOS"
source: https://sebastianraschka.com/Articles/2014_install_python_sci_pkgs.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 在 macOS 上安装 Python 科学计算包

> 原文：[Python Scientific Packages on macOS](https://sebastianraschka.com/Articles/2014_install_python_sci_pkgs.html) · Sebastian Raschka's Articles

当我想在自己的第二台 Mac 上安装一些 Python 科学计算库时，又（一次）经历了一番折腾。我把整个配置和安装过程总结下来，以备日后参考。
如果你遇到了任何不同或额外的障碍，请告诉我；也欢迎提出任何改进这篇简短指南的建议。

![Install python sci pkgs python sci pack ing](https://sebastianraschka.com/images/blog/2014/install_python_sci_pkgs/python_sci_pack_ing.webp)

---

## 章节

---

\

## Anaconda 与 Miniconda

作为替代方案，如果不打算走下面几节列出的那些手动步骤，还可以选择面向科学计算的 [Anaconda Python
发行版](https://store.continuum.io/cshop/anaconda/)。虽然 Anaconda 由 Continuum Analytics 发行，但它完全免费，并且包含了 125 个以上用于科学与数据分析的包。\\安装流程在这里总结得很清楚：
<http://docs.continuum.io/anaconda/install.html>

如果觉得这有些太重了，那么 [Miniconda](http://repo.continuum.io/miniconda/) 或许更适合你。
Miniconda 本质上就是一个自带 Conda 包管理器的 Python 发行版，借助它我们可以把一组 Python 包安装到指定的 conda 环境中。

```python
$[bash]> conda create -n myenv python=3
$[bash]> conda install -n myenv numpy scipy matplotlib ipython
```

注意：环境默认会创建在 `ROOT_DIR/envs` 下；你也可以在上面的 conda 命令中使用 `-p` 标志代替 `-n` 标志，以指定自定义路径。

如果我们决定选用 Anaconda 或 Miniconda，那么到这里基本上就大功告成了。接下来几节介绍的是一种更（半）手动的方式：使用 `pip` 逐个安装这些包。

## 考虑使用虚拟环境

为了避免把系统自带的包搞得一团糟，在安装这些额外的科学计算包时，我们应当考虑搭建一个虚拟环境。
要创建一个新的虚拟环境，我们可以使用以下命令

```python
$[bash]> python3 -m venv /path_to/my_virtual_env
```

然后通过以下命令激活它

```python
$[bash]> source /path_to/my_virtual_env/bin/activate
```

## 安装 pip

`pip` 是一个用于安装和管理 Python 包的工具。它让 Python 包的安装过程轻松了许多，因为我们不必再手动下载这些包。
如果你还没有为自己的 Python 版本安装 `pip` 包，我建议从 <https://pypi.python.org/pypi/pip> 下载它，解压后进入解压目录，然后通过以下命令安装

```python
$[bash]> python3 setup.py install
```

## 安装 NumPy

现在使用 `pip` 安装 NumPy 应该很顺利

```python
$[bash]> python3 -m pip install numpy
```

由于需要为你的机器编译源代码文件，安装过程可能要花上几分钟。安装完成后，在 Python 中应该可以通过以下方式使用 `NumPy`

```python
>> import numpy
```

如果你想看一些操作 NumPy 数组的例子，可以看看我写的这篇 [Matrix Cheatsheet for Moving from MATLAB matrices
to NumPy arrays（从 MATLAB 矩阵迁移到 NumPy 数组的速查表）](https://sebastianraschka.com/Articles/2014_matrix_cheatsheet.html)

安装 SciPy
—————-

虽然 `clang` 编译器编译 `numpy` 的 C 源代码毫无问题，但为了安装 `scipy`，我们现在还需要一个额外的 Fortran 编译器。

### 安装 Fortran 编译器

遗憾的是，MacOS 10.9 Mavericks 并没有自带 Fortran 编译器，不过下载并安装一个也相当容易。
例如，适用于 MacOS 10.9 的 `gfortran` 可以从
<https://www.coudert.name/software.html> 下载

只需双击下载下来的 .DMG 镜像，按照熟悉的 MacOS X 安装流程操作即可。安装完成后，就应该可以在命令行中使用 `gfortran` 编译器了。我们可以输入以下命令来测试

```python
$[bash]> gfortran -v
```

在输出的各种信息中，我们会看到当前版本号，例如

```python
gcc version 4.8.2 (GCC)
```

### 安装 SciPy

现在，我们应该可以顺利地使用 `pip` 安装 `SciPy` 了。

```python
$[bash]> python3 -m pip install scipy
```

成功安装之后（由于需要编译源代码，同样可能需要几分钟），在 Python 中应该可以通过以下方式使用它

```python
>> import scipy
```

## 安装 matplotlib

使用 `pip` 安装 matplotlib 的过程应该非常顺畅，我在这一步没有遇到任何障碍。

```python
$[bash]> python3 -m pip install matplotlib
```

安装成功后，可以在 Python 中通过以下方式导入

```python
>> import matplotlib
```

`matplotlib` 库最近已经成了我最喜欢的数据绘图工具，你可以在 GitHub 上我的小型 matplotlib 作品集里看一些例子：
<https://github.com/rasbt/matplotlib_gallery>

## 安装 IPython

### 安装 pyzmq

IPython 内核的运行需要 `pyzmq` 包，`pyzmq` 包含了 ØMQ 的 Python 绑定，而 ØMQ 是一个轻量、快速的消息传递实现。它可以通过 `pip` 安装。

```python
$[bash]> python3 -m pip install pyzmq
```

### 安装 pyside

在我尝试安装 `pyside` 包时，它抱怨缺少 `cmake`。`cmake` 可以从下面这个地址下载：

<http://www.cmake.org/files/v2.8/cmake-2.8.12.2-Darwin64-universal.dmg>

就像我们在[安装 SciPy 一节](#scipy)中处理 `gfortran` 那样，双击下载下来的 .DMG 镜像，按照熟悉的 MacOS X 安装流程操作即可。\我们可以通过在命令行中输入以下命令来确认安装成功

```python
$[bash]> cmake --version
```

它会打印出类似这样的信息

```python
cmake version 2.8.12.2
```

### 安装 IPython

现在，我们终于应该可以通过以下命令，连同其余所有依赖（pygments、Sphinx、jinja2、docutils、markupsafe）一起安装 IPython 了

```python
$[bash]> python3 -m pip install ipython[all]
```

这样一来，我们会把 IPython 安装到一个自定义位置，例如
`/Library/Frameworks/Python.framework/Versions/3.3/lib/python3.3/site-packages/IPython`。

你可以先在 Python 中导入 IPython，然后打印它的路径，以此找到这个位置的路径：

```python
>> import IPython
>> IPython.__path__
```

最后，我们可以在 `.bash_profile` 或 `.bash_rc` 文件里设置一个 `alias`，以便在控制台中方便地运行 IPython。例如

```python
alias ipython3="python3 /Library/Frameworks/Python.framework/Versions/3.3/lib/python3.3/site-packages/IPython/terminal/ipapp.py"
```

（之后别忘了 `source` 一下 `.bash_rc` 或 `.bash_profile` 文件）

现在我们可以在 shell 终端里运行

```python
$[bash]> ipython3
```

来启动交互式 IPython shell，以及运行

```python
$[bash]> ipython3 notebook
```

在浏览器中打开超棒的 IPython notebook。

## 更新已安装的包

最后，如果想让我们刚装好的这些包保持最新，我们可以在运行 `pip` 时加上 `--upgrade` 标志，例如

```python
$[bash]> python3 -m pip install numpy --upgrade
```
