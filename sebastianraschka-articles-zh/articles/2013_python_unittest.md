---
title: "Python 中的单元测试"
title_en: "Unit testing in Python"
source: https://sebastianraschka.com/Articles/2013_python_unittest.html
crawled: 2026-09-06
translated: 2026-09-14
---

# Python 中的单元测试

> 原文：[Unit testing in Python](https://sebastianraschka.com/Articles/2013_python_unittest.html) · Sebastian Raschka's Articles

说实话，代码测试绝不是一件令人愉快的工作。不过，一个好的单元测试框架能让这个过程尽可能顺畅。最终，测试会变成一种常规而持续的过程，并让我们确信：自己的代码会像瑞士钟表一样精确无误、严丝合缝地运行。

## 章节

## 单元测试的优点

按照传统做法，对于我们写下的每一段代码（无论是一个单独的函数还是类方法），我们都会随手喂给它一些输入，以确保它按我们预期的方式工作。如果一切运转正常，而且我们也不打算在「世界末日」之前对代码做任何改动，这听起来倒也算是一种合理的做法。当然，实际情况很少如此。
假设我们想通过重构来修改代码，或者为了提升效率而对它加以调整：我们真的愿意把之前的测试用例（test case）重新手动输入一遍，来确保没有破坏任何功能吗？又假设我们打算把代码移交给同事使用：他们凭什么信任这些代码？我们如何向他们提供「一切都经过了测试、理应正常工作」的证据，从而让他们的工作更轻松？
毫无疑问，没有人愿意花上几个小时甚至几天的时间去枯燥地测试接手来的代码，然后才能问心无愧地把它投入使用。
一定存在一种更聪明的办法，一种自动化的、更系统化的方法……
这正是单元测试（unit test）的用武之地。一旦我们设计好了接口（*这里指*函数和方法的输入与输出），就可以把若干测试用例写下来，并在每次修改代码时让它们自动接受检验——既不必再做重复输入一切的无聊工作，也不会因为偷懒而遗漏任何东西、省略关键的测试。
**这一点在科学研究中尤其重要：你的整个项目都依赖于对任何数据的正确分析与评估——而且，大概再没有比这更便捷的方式，能让你自己和那些理应持怀疑态度的审稿人都相信：你刚刚做出了（又一次）突破性的发现。**

## 典型单元测试的主要组成部分

原则上，单元测试其实不过是一种更系统化的代码测试自动化方式。其中「单元」（unit）一词通常被定义为一个孤立的测试用例，它由以下几个部分组成：

- 一个所谓的「测试夹具」（fixture，例如一个函数、一个类或类方法，甚至一个数据文件）
- 对测试夹具执行的操作（例如以某个特定输入调用一个函数）
- 一个预期结果（例如函数的预期返回值）
- 实际结果（例如一次函数调用后的实际返回值）
- 一条验证消息（例如一份报告，说明实际返回值与预期返回值是否匹配）

## Python 中不同的单元测试框架

在 Python 中，我们有幸可以从各种优秀且功能强大的单元测试框架中进行选择。其中最流行、使用最广泛的可能是：

- [unittest](https://docs.python.org/3.3/library/unittest.html)
  模块——Python 标准库的一部分
- [nose](https://nose.readthedocs.org/en/latest/index.html)
- [py.test](http://pytest.org/latest/index.html)

这几个框架都工作得非常好，对于基础的单元测试而言它们都足够了。有些人可能更喜欢用 *nose*，而不是更「基础」的 *unittest* 模块。还有很多人正在转向较新的 *py.test* 框架，因为它提供了一些不错的扩展，甚至有更多高级而实用的功能。不过，逐一讨论各个单元测试框架的所有细节并对它们相互比较，并不是本教程的重点。下面的截图展示了简单地运行 *py.test* 和 *nose* 时大概的样子。再给你补充一点背景信息：*nose* 和 *py.test* 都会遍历子目录树，寻找以命名前缀「test」开头的 Python 脚本文件。如果这些脚本文件中包含同样以「test」前缀开头的函数、类和类方法，其中包含的代码就会被单元测试框架执行。

![Python unittest pytest 01](https://sebastianraschka.com/images/blog/2013/python-unittest/pytest_01.webp)

---

命令行语法：

- `py.test <file/directory>`——默认单元测试，附带详细报告
- `py.test -q <file/directory>`——默认单元测试，附带汇总报告（静默模式）
- `nosetests`——默认单元测试，附带汇总报告
- `nosetests -v`——默认单元测试，附带详细报告（详细模式）

---

在本教程的后续章节中，我们将使用 *py.test*，不过所有内容同样与 *nose* 框架兼容，而且对于下面的简单示例来说，选哪个框架都无所谓。
然而，两者的默认行为确实存在一个小小的差异，而这个差异或许也能回答这样一个问题：「框架是如何知道到哪里去找要执行的测试代码的？」
默认情况下，*py.test* 会（从当前工作目录或你作为附加参数提供的某个文件夹出发）深入所有子目录，寻找以「test」前缀开头的 Python 脚本。如果这些脚本中包含同样以「test」前缀开头的函数、类或类方法，单元测试框架就会执行它们。*nose* 的基本行为与此非常相似，但与遍历所有子目录不同，它只会考虑那些以「test」前缀开头的目录，并在其中查找相应的 Python 单元测试代码。因此，即便你使用的是 *py.test*，把所有测试代码放在一个以「test」前缀开头的目录下也是一个好习惯——你的 *nose* 同事会感谢你的！
下图展示了 *nose* 和 *py.test* 单元测试框架会如何遍历子目录树，寻找以「test」前缀开头的 Python 脚本文件。

![Python unittest pytest 02](https://sebastianraschka.com/images/blog/2013/python-unittest/pytest_02.webp)

*注：有趣的是，在上面的例子中，nose 似乎比 py.test 快一倍。我很好奇这是不是由 py.test 会搜索所有子目录（nose 只搜索以 "test" 开头的目录）造成的。不过，当我直接指定包含测试代码的文件夹时，两者仍然存在微小的速度差异，nose 依然显得更快。然而，我不知道这种差异在更大规模下会如何变化，针对大得多的项目做一次测试也许会是个有趣的实验。*

![Python unittest pytest 02 2](https://sebastianraschka.com/images/blog/2013/python-unittest/pytest_02_2.webp)

## 安装 py.test

安装 py.test 非常简单。我们可以直接在命令行中通过以下命令安装：

```python
pip install -U pytest
```

或者

```python
easy_install -U pytest
```

如果这些方法对你不起作用，你可以访问 *py.test* 网站（<http://pytest.org/latest/>），下载软件包，并尝试「手动」安装：

```python
~/Desktop/pytest-2.5.0> python3 setup.py install
```

如果安装正确，我们现在就可以在任何目录下通过命令行运行 *py.test*：

```python
py.test <file or directory>
```

或者

```python
python -m pytest <file or directory>
```

## 一个 py.test 示例的完整走查

在下面的例子中，我们将使用 *py.test*；不过 *nose* 的用法与之非常相似，而且正如上一节所说，我在这里只想聚焦于单元测试的要点。请注意，*py.test* 还提供了许多本教程不会触及的高级而实用的功能，例如为调试设置断点等（如果你想了解更多，请查阅完整的 *py.test* 文档：<http://pytest.org/latest/contents.html#toc>）。

### 编写一些我们想要测试的代码

假设我们写了两个非常简单的、想要测试的函数，它们既可以是小脚本，也可以是某个更大软件包的一部分。第一个函数 `multiple_of_three` 用于检查一个数是否是 3 的倍数。我们希望：如果是，函数返回布尔值 True；否则应返回 False。第二个函数 `filter_multiples_of_three` 接受一个列表作为输入参数，应返回输入列表的一个子集，其中只包含那些是 3 的倍数的数。

![Python unittest pytest 03](https://sebastianraschka.com/images/blog/2013/python-unittest/pytest_03.webp)

### 创建「test」文件

接下来，我们编写一个小型单元测试，检查我们的函数在一些简单输入情况下是否正常工作：

![Python unittest pytest 04](https://sebastianraschka.com/images/blog/2013/python-unittest/pytest_04.webp)

太好了，当我们运行 py.test 单元测试框架时，可以看到一切都按预期工作！

![Python unittest pytest 05](https://sebastianraschka.com/images/blog/2013/python-unittest/pytest_05.webp)

那么，边界情况（edge case）又如何呢？

### 测试边界情况并完善代码

为了检查我们的函数是否已经足够健壮、能够处理特殊情况（例如输入为 0），我们扩展单元测试代码。这里，假设我们不希望 0 被判定为 True，因为我们不认为 3 是 0 的因子。

![Python unittest pytest 06](https://sebastianraschka.com/images/blog/2013/python-unittest/pytest_06.webp) ![Python unittest pytest 07](https://sebastianraschka.com/images/blog/2013/python-unittest/pytest_07.webp)

正如 *py.test 报告*所示，我们的测试刚刚失败了。那么，让我们回过头去修改代码，以处理这个特殊情况。

![Python unittest pytest 08](https://sebastianraschka.com/images/blog/2013/python-unittest/pytest_08.webp)

到目前为止一切顺利：当我们再次运行 *py.test*（截图未展示）时，可以看到代码现在已经能正确处理 0 了。让我们再补充一些边界情况：负整数、十进制浮点数，以及大整数。

![Python unittest pytest 09](https://sebastianraschka.com/images/blog/2013/python-unittest/pytest_09.webp) ![Python unittest pytest 10](https://sebastianraschka.com/images/blog/2013/python-unittest/pytest_10.webp)

根据单元测试报告，我们在这里遇到了另一个问题：我们的代码把 3 当成了 –9（负九）的因子。在这个示例中，我们假设并不希望出现这种情况：我们只想把正数视为 3 的倍数。为了覆盖这些情况，我们需要对代码再做一处小小的修改：把 if 语句中的 `!=0` 改为 `>0`。

![Python unittest pytest 11](https://sebastianraschka.com/images/blog/2013/python-unittest/pytest_11.webp)

再次运行 *py.test* 工具后，我们可以确定代码现在也能正确处理负数了。而一旦我们对当前代码的总体行为感到满意，就可以继续测试下一个函数 `filter_multiples_of_three`，它的正确性依赖于 `multiple_of_three`。

![Python unittest pytest 12](https://sebastianraschka.com/images/blog/2013/python-unittest/pytest_12.webp) ![Python unittest pytest 13](https://sebastianraschka.com/images/blog/2013/python-unittest/pytest_13.webp)

这一次，我们的测试看起来已经没有「bug」了，我们确信它能应对目前所能想到的所有场景。如果将来还打算对代码做任何进一步的修改，只需重新运行之前的测试、确保没有破坏任何功能——再没有比这更省心的了。
