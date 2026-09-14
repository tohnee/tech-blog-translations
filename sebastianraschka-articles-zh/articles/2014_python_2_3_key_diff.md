---
title: "Python 2 与 Python 3 的关键差异"
title_en: "Python 2 vs 3 Key Differences"
source: https://sebastianraschka.com/Articles/2014_python_2_3_key_diff.html
crawled: 2026-09-06
translated: 2026-09-14
---

# Python 2 与 Python 3 的关键差异

> 原文：[Python 2 vs 3 Key Differences](https://sebastianraschka.com/Articles/2014_python_2_3_key_diff.html) · Sebastian Raschka's Articles

许多刚入门的 Python 用户都在纠结应该从哪个版本的 Python 开始学习。对于这个问题，我的回答通常是这样的：「就用你喜欢的教程所用的版本，两者的差异以后再去了解。」

但如果你要启动一个新项目，并且可以自由选择，那该怎么办？我想说，只要 Python 2.7.x 和 Python 3.x 都支持你打算使用的那些库，目前就不存在「正确」或「错误」之分。不过，看一看这两个最流行的 Python 版本之间的主要差异还是值得的：这样可以避免在为其中任何一个版本编写代码时踩到常见的坑，或者在你打算移植项目时有所帮助。

## 章节

## `__future__` 模块

Python 3.x 引入了一些与 Python 2 不兼容的关键字和特性，它们可以通过 Python 2 内置的 `__future__` 模块导入。如果你打算让自己的代码支持 Python 3.x，推荐使用 `__future__` 导入。例如，如果我们想在 Python 2 中获得 Python 3.x 的整数除法行为，可以通过以下方式导入：

```python
from __future__ import division
```

下表列出了可以从 `__future__` 模块导入的更多特性：

| 特性 | 可选引入版本 | 强制生效版本 | 效果 |
| --- | --- | --- | --- |
| nested\_scopes | 2.1.0b1 | 2.2 | [**PEP 227**](https://www.python.org/dev/peps/pep-0227): *Statically Nested Scopes* |
| generators | 2.2.0a1 | 2.3 | [**PEP 255**](https://www.python.org/dev/peps/pep-0255): *Simple Generators* |
| division | 2.2.0a2 | 3.0 | [**PEP 238**](https://www.python.org/dev/peps/pep-0238): *Changing the Division Operator* |
| absolute\_import | 2.5.0a1 | 3.0 | [**PEP 328**](https://www.python.org/dev/peps/pep-0328): *Imports: Multi-Line and Absolute/Relative* |
| with\_statement | 2.5.0a1 | 2.6 | [**PEP 343**](https://www.python.org/dev/peps/pep-0343): *The “with” Statement* |
| print\_function | 2.6.0a2 | 3.0 | [**PEP 3105**](https://www.python.org/dev/peps/pep-3105): *Make print a function* |
| unicode\_literals | 2.6.0a2 | 3.0 | [**PEP 3112**](https://www.python.org/dev/peps/pep-3112): *Bytes literals in Python 3000* |

（来源：[https://docs.python.org/2/library/\_\_future\_\_.html](https://docs.python.org/2/library/\_\_future\_\_.html#module-\_\_future\_\_)）

```python
from platform import python_version
```

## print 函数

非常简单，print 语法的变化大概是流传最广的一个改动，但仍然值得一提：Python 2 的 print 语句已被 `print()` 函数取代，也就是说，我们必须把要打印的对象放进括号里。

Python 2 并不介意多出来的括号；但恰恰相反，如果我们按照 Python 2 的方式、不带括号地调用 print 函数，Python 3 就会抛出 `SyntaxError`。

### Python 2

```python
print 'Python', python_version()
print 'Hello, World!'
print('Hello, World!')
print "text", ; print 'print more text on the same line'
```

```python
Python 2.7.6
Hello, World!
Hello, World!
text print more text on the same line
```

### Python 3

```python
print('Python', python_version())
print('Hello, World!')

print("some text,", end="")
print(' print more text on the same line')
```

```python
Python 3.4.1
Hello, World!
some text, print more text on the same line
```

```python
print 'Hello, World!'
```

```python
  File "<ipython-input-3-139a7c5835bd>", line 1
    print 'Hello, World!'
                        ^
SyntaxError: invalid syntax
```

**注意：**

上面在 Python 2 中打印「Hello, World」看起来相当「正常」。然而，如果括号里有多个对象，我们实际创建的是一个元组，因为在 Python 2 中 `print` 是一个「语句」（statement），而不是函数调用。

```python
print 'Python', python_version()
print('a', 'b')
print 'a', 'b'
```

```python
Python 2.7.7
('a', 'b')
a b
```

## 整数除法

如果你正在移植代码，或者在 Python 2 中执行 Python 3 的代码，这个改动尤其危险，因为整数除法行为的变化往往不易被察觉（它不会抛出 `SyntaxError`）。  
因此，在我的 Python 3 脚本中，我仍然倾向于写 `float(3)/2` 或 `3/2.0`，而不是 `3/2`，好让还在用 Python 2 的人少踩点坑（反过来，我推荐在你的 Python 2 脚本中加上 `from __future__ import division`）。

### Python 2

```python
print 'Python', python_version()
print '3 / 2 =', 3 / 2
print '3 // 2 =', 3 // 2
print '3 / 2.0 =', 3 / 2.0
print '3 // 2.0 =', 3 // 2.0
```

```python
Python 2.7.6
3 / 2 = 1
3 // 2 = 1
3 / 2.0 = 1.5
3 // 2.0 = 1.0
```

### Python 3

```python
print('Python', python_version())
print('3 / 2 =', 3 / 2)
print('3 // 2 =', 3 // 2)
print('3 / 2.0 =', 3 / 2.0)
print('3 // 2.0 =', 3 // 2.0)
```

```python
Python 3.4.1
3 / 2 = 1.5
3 // 2 = 1
3 / 2.0 = 1.5
3 // 2.0 = 1.0
```

## Unicode

Python 2 有 ASCII 的 `str()` 类型、单独的 `unicode()` 类型，但没有 `byte` 类型。

而在 Python 3 中，我们终于有了 Unicode（utf-8）的 `str` 字符串，以及两种字节类：`byte` 和 `bytearray`。

### Python 2

```python
print 'Python', python_version()
```

```python
Python 2.7.6
```

```python
print type(unicode('this is like a python3 str type'))
```

```python
<type 'unicode'>
```

```python
print type(b'byte type does not exist')
```

```python
<type 'str'>
```

```python
print 'they are really' + b' the same'
```

```python
they are really the same
```

```python
print type(bytearray(b'bytearray oddly does exist though'))
```

```python
<type 'bytearray'>
```

### Python 3

```python
print('Python', python_version())
print('strings are now utf-8 \u03BCnico\u0394é!')
```

```python
Python 3.4.1
strings are now utf-8 μnicoΔé!
```

```python
print('Python', python_version(), end="")
print(' has', type(b' bytes for storing data'))
```

```python
Python 3.4.1 has <class 'bytes'>
```

```python
print('and Python', python_version(), end="")
print(' also has', type(bytearray(b'bytearrays')))
```

```python
and Python 3.4.1 also has <class 'bytearray'>
```

```python
'note that we cannot add a string' + b'bytes for data'
```

```python
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)

<ipython-input-13-d3e8942ccf81> in <module>()
----> 1 'note that we cannot add a string' + b'bytes for data'

TypeError: Can't convert 'bytes' object to str implicitly
```

## xrange

在 Python 2.x 中，`xrange()` 的使用非常普遍，用来创建可迭代对象，例如用在 for 循环或列表/集合/字典推导式中。  
它的行为与生成器非常相似（即「惰性求值」），但这里的 xrange 可迭代对象是「耗不尽」的——也就是说，你可以对它无限次地迭代。

得益于这种「惰性求值」，与普通的 `range()` 相比，`xrange()` 的优势在于：如果你只需要迭代一次（例如在 for 循环中），它通常更快。然而，与只需迭代一次的场景相比，如果你要重复迭代多次，就不推荐使用它了，因为每次迭代都要从头开始生成！

在 Python 3 中，`range()` 的实现方式与 `xrange()` 函数相同，因此不再有专门的 `xrange()` 函数（在 Python 3 中调用 `xrange()` 会抛出 `NameError`）。

```python
import timeit

n = 10000
def test_range(n):
    return for i in range(n):
        pass

def test_xrange(n):
    for i in xrange(n):
        pass
```

### Python 2

```python
print 'Python', python_version()

print '\ntiming range()'
%timeit test_range(n)

print '\n\ntiming xrange()'
%timeit test_xrange(n)
```

```python
Python 2.7.6

timing range()
1000 loops, best of 3: 433 µs per loop

timing xrange()
1000 loops, best of 3: 350 µs per loop
```

### Python 3

```python
print('Python', python_version())

print('\ntiming range()')
%timeit test_range(n)
```

```python
Python 3.4.1

timing range()
1000 loops, best of 3: 520 µs per loop
```

```python
print(xrange(10))
```

```python
---------------------------------------------------------------------------
NameError                                 Traceback (most recent call last)

<ipython-input-5-5d8f9b79ea70> in <module>()
----> 1 print(xrange(10))

NameError: name 'xrange' is not defined
```

### Python 3 中 `range` 对象的 `__contains__` 方法

另一件值得一提的事情是，`range` 在 Python 3.x 中得到了一个「新的」`__contains__` 方法（感谢 [Yuchen Ying](https://github.com/yegle) 指出这一点）。对于整数和布尔类型，`__contains__` 方法可以显著加快 Python 3.x 中 `range` 的「查找」速度。

```python
x = 10000000
```

```python
def val_in_range(x, val):
    return val in range(x)
```

```python
def val_in_xrange(x, val):
    return val in xrange(x)
```

```python
print('Python', python_version())
assert(val_in_range(x, x/2) == True)
assert(val_in_range(x, x//2) == True)
%timeit val_in_range(x, x/2)
%timeit val_in_range(x, x//2)
```

```python
Python 3.4.1
1 loops, best of 3: 742 ms per loop
1000000 loops, best of 3: 1.19 µs per loop
```

根据上面的 `timeit` 结果可以看到，当查找的对象是整数类型而不是浮点类型时，「查找」的执行速度大约快了 60,000 倍。然而，由于 Python 2.x 的 `range` 和 `xrange` 都没有 `__contains__` 方法，整数和浮点数的「查找速度」不会有这么大的差别：

```python
print 'Python', python_version()
assert(val_in_xrange(x, x/2.0) == True)
assert(val_in_xrange(x, x/2) == True)
assert(val_in_range(x, x/2) == True)
assert(val_in_range(x, x//2) == True)
%timeit val_in_xrange(x, x/2.0)
%timeit val_in_xrange(x, x/2)
%timeit val_in_range(x, x/2.0)
%timeit val_in_range(x, x/2)
```

```python
Python 2.7.7
1 loops, best of 3: 285 ms per loop
1 loops, best of 3: 179 ms per loop
1 loops, best of 3: 658 ms per loop
1 loops, best of 3: 556 ms per loop
```

下面是 `__contain__` 方法尚未被加入 Python 2.x 的「证据」：

```python
print('Python', python_version())
range.__contains__
```

```python
Python 3.4.1

<slot wrapper '__contains__' of 'range' objects>
```

```python
print 'Python', python_version()
range.__contains__
```

```python
Python 2.7.7

---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)

<ipython-input-7-05327350dafb> in <module>()
      1 print 'Python', python_version()
----> 2 range.__contains__

AttributeError: 'builtin_function_or_method' object has no attribute '__contains__'
```

```python
print 'Python', python_version()
xrange.__contains__
```

```python
Python 2.7.7

---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)

<ipython-input-8-7d1a71bfee8e> in <module>()
      1 print 'Python', python_version()
----> 2 xrange.__contains__

AttributeError: type object 'xrange' has no attribute '__contains__'
```

#### 关于 Python 2 与 Python 3 速度差异的说明

有人指出了 Python 3 的 `range()` 与 Python 2 的 `xrange()` 之间的速度差异。既然两者的实现方式相同，按理说速度也应该一样。然而，这里的差异只是源于一个事实：Python 3 总体上往往比 Python 2 运行得慢。

```python
def test_while():
    i = 0
    while i < 20000:
        i += 1
    return
```

```python
print('Python', python_version())
%timeit test_while()
```

```python
Python 3.4.1
100 loops, best of 3: 2.68 ms per loop
```

```python
print 'Python', python_version()
%timeit test_while()
```

```python
Python 2.7.6
1000 loops, best of 3: 1.72 ms per loop
```

## 抛出异常

Python 2 同时接受「旧」和「新」两种语法，而 Python 3 则不行：如果我们不把异常参数放进括号里，Python 3 就会卡住（并随之抛出一个 `SyntaxError`）：

### Python 2

```python
print 'Python', python_version()
```

```python
Python 2.7.6
```

```python
raise IOError, "file error"
```

```python
---------------------------------------------------------------------------
IOError                                   Traceback (most recent call last)

<ipython-input-8-25f049caebb0> in <module>()
----> 1 raise IOError, "file error"

IOError: file error
```

```python
raise IOError("file error")
```

```python
---------------------------------------------------------------------------
IOError                                   Traceback (most recent call last)

<ipython-input-9-6f1c43f525b2> in <module>()
----> 1 raise IOError("file error")

IOError: file error
```

### Python 3

```python
print('Python', python_version())
```

```python
Python 3.4.1
```

```python
raise IOError, "file error"
```

```python
  File "<ipython-input-10-25f049caebb0>", line 1
    raise IOError, "file error"
                 ^
SyntaxError: invalid syntax
```

在 Python 3 中抛出异常的正确方式：

```python
print('Python', python_version())
raise IOError("file error")
```

```python
Python 3.4.1

---------------------------------------------------------------------------
OSError                                   Traceback (most recent call last)

<ipython-input-11-c350544d15da> in <module>()
      1 print('Python', python_version())
----> 2 raise IOError("file error")

OSError: file error
```

## 处理异常

Python 3 中异常的处理方式也略有变化。在 Python 3 中，我们现在必须使用「`as`」关键字：

### Python 2

```python
print 'Python', python_version()
try:
    let_us_cause_a_NameError
except NameError, err:
    print err, '--> our error message'
```

```python
Python 2.7.6
name 'let_us_cause_a_NameError' is not defined --> our error message
```

### Python 3

```python
print('Python', python_version())
try:
    let_us_cause_a_NameError
except NameError as err:
    print(err, '--> our error message')
```

```python
Python 3.4.1
name 'let_us_cause_a_NameError' is not defined --> our error message
```

## next() 函数与 .next() 方法

由于 `next()`（`.next()`）是非常常用的函数（方法），这是另一个值得提及的语法变化（更确切地说是实现上的变化）：在 Python 2.7.5 中，函数和方法两种语法都可以使用；而在 Python 3 中只剩下 `next()` 函数（调用 `.next()` 方法会抛出 `AttributeError`）。

### Python 2

```python
print 'Python', python_version()

my_generator = (letter for letter in 'abcdefg')

next(my_generator)
my_generator.next()
```

```python
Python 2.7.6

'b'
```

### Python 3

```python
print('Python', python_version())

my_generator = (letter for letter in 'abcdefg')

next(my_generator)
```

```python
Python 3.4.1

'a'
```

```python
my_generator.next()
```

```python
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)

<ipython-input-14-125f388bb61b> in <module>()
----> 1 my_generator.next()

AttributeError: 'generator' object has no attribute 'next'
```

## for 循环变量与全局命名空间泄漏

好消息是：在 Python 3.x 中，for 循环变量不会再泄漏到全局命名空间中了！

这源于 Python 3.x 中做出的一项改动，[What's New In Python 3.0](https://docs.python.org/3/whatsnew/3.0.html) 中是这样描述的：

「列表推导式不再支持 `[... for var in item1, item2, ...]` 这种语法形式。请改用 `[... for var in (item1, item2, ...)]`。另外还要注意，列表推导式的语义有所不同：它们更接近于 `list()` 构造器中包裹一个生成器表达式的语法糖，尤其是循环控制变量不再会泄漏到外围作用域中。」

### Python 2

```python
print 'Python', python_version()

i = 1
print 'before: i =', i

print 'comprehension: ', [i for i in range(5)]

print 'after: i =', i
```

```python
Python 2.7.6
before: i = 1
comprehension:  [0, 1, 2, 3, 4]
after: i = 4
```

### Python 3

```python
print('Python', python_version())

i = 1
print('before: i =', i)

print('comprehension:', [i for i in range(5)])

print('after: i =', i)
```

```python
Python 3.4.1
before: i = 1
comprehension: [0, 1, 2, 3, 4]
after: i = 1
```

## 比较不可排序的类型

Python 3 中另一个很棒的改动是：如果我们试图比较不可排序的类型，会抛出一个 `TypeError` 作为警告。

### Python 2

```python
print 'Python', python_version()
print "[1, 2] > 'foo' = ", [1, 2] > 'foo'
print "(1, 2) > 'foo' = ", (1, 2) > 'foo'
print "[1, 2] > (1, 2) = ", [1, 2] > (1, 2)
```

```python
Python 2.7.6
[1, 2] > 'foo' =  False
(1, 2) > 'foo' =  True
[1, 2] > (1, 2) =  False
```

### Python 3

```python
print('Python', python_version())
print("[1, 2] > 'foo' = ", [1, 2] > 'foo')
print("(1, 2) > 'foo' = ", (1, 2) > 'foo')
print("[1, 2] > (1, 2) = ", [1, 2] > (1, 2))
```

```python
Python 3.4.1

---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)

<ipython-input-16-a9031729f4a0> in <module>()
      1 print('Python', python_version())
----> 2 print("[1, 2] > 'foo' = ", [1, 2] > 'foo')
      3 print("(1, 2) > 'foo' = ", (1, 2) > 'foo')
      4 print("[1, 2] > (1, 2) = ", [1, 2] > (1, 2))

TypeError: unorderable types: list() > str()
```

## 通过 input() 解析用户输入

幸运的是，`input()` 函数在 Python 3 中得到了修复，它现在总是把用户输入存储为 `str` 对象。而为了避免 Python 2 中读取到字符串以外其他类型的危险行为，我们必须改用 `raw_input()`。

### Python 2

```python
Python 2.7.6
[GCC 4.0.1 (Apple Inc. build 5493)] on darwin
Type "help", "copyright", "credits" or "license" for more information.

>>> my_input = input('enter a number: ')

enter a number: 123

>>> type(my_input)
<type 'int'>

>>> my_input = raw_input('enter a number: ')

enter a number: 123

>>> type(my_input)
<type 'str'>
```

### Python 3

```python
Python 3.4.1
[GCC 4.2.1 (Apple Inc. build 5577)] on darwin
Type "help", "copyright", "credits" or "license" for more information.

>>> my_input = input('enter a number: ')

enter a number: 123

>>> type(my_input)
<class 'str'>
```

## 返回可迭代对象而非列表

正如我们在 [`xrange`](#xrange) 一节中已经看到的那样，在 Python 3 中，一些函数和方法现在返回的是可迭代对象——而不是像 Python 2 中那样返回列表。

由于我们通常本来就只对这些对象迭代一次，我认为这个改动对于节省内存来说非常有意义。不过，与生成器不同的是，在需要时我们仍然可以对它们进行多次迭代，只是效率没那么高而已。

而对于那些确实需要 `list` 对象的场景，我们可以直接通过 `list()` 函数把可迭代对象转换成 `list`。

### Python 2

```python
print 'Python', python_version()

print range(3)
print type(range(3))
```

```python
Python 2.7.6
[0, 1, 2]
<type 'list'>
```

### Python 3

```python
print('Python', python_version())

print(range(3))
print(type(range(3)))
print(list(range(3)))
```

```python
Python 3.4.1
range(0, 3)
<class 'range'>
[0, 1, 2]
```

**在 Python 3 中另一些不再返回列表的常用函数和方法：**

- `zip()`
- `map()`
- `filter()`
- 字典的 `.keys()` 方法
- 字典的 `.values()` 方法
- 字典的 `.items()` 方法

## 银行家舍入法

Python 3 采用了如今已成为标准的十进制数舍入方式：当在最后几位有效数字上出现平局（.5）时进行舍入。现在，在 Python 3 中，小数会被舍入到最近的偶数。虽然这给代码可移植性带来了不便，但相比「逢五进一」的舍入方式，这被认为是更好的做法，因为它避免了对较大数字的偏向。更多信息请参阅维基百科上这些出色的文章和段落：

- <https://en.wikipedia.org/wiki/Rounding#Round_half_to_even>
- <https://en.wikipedia.org/wiki/IEEE_floating_point#Roundings_to_nearest>

### Python 2

```python
print 'Python', python_version()
```

```python
Python 2.7.12
```

```python
round(15.5)
```

```python
16.0
```

```python
round(16.5)
```

```python
17.0
```

### Python 3

```python
print('Python', python_version())
```

```python
Python 3.5.1
```

```python
round(15.5)
```

```python
16
```

```python
round(16.5)
```

```python
16
```

## 更多关于 Python 2 与 Python 3 的文章

下面列出一些关于 Python 2 和 Python 3 的好文章，我推荐把它们作为后续阅读。

**// 移植到 Python 3**

- [Should I use Python 2 or Python 3 for my development activity?](https://wiki.python.org/moin/Python2orPython3)
- [What's New In Python 3.0](https://docs.python.org/3.0/whatsnew/3.0.html)
- [Porting to Python 3](http://python3porting.com/differences.html)
- [Porting Python 2 Code to Python 3](https://docs.python.org/3/howto/pyporting.html)
- [How keep Python 3 moving forward](http://nothingbutsnark.svbtle.com/my-view-on-the-current-state-of-python-3)

**// 支持与反对 Python 3**

- [10 awesome features of Python that you can't use because you refuse to upgrade to Python 3](http://asmeurer.github.io/python3-presentation/slides.html#1)
- [Everything you did not want to know about Unicode in Python 3](http://lucumr.pocoo.org/2014/5/12/everything-about-unicode/)
- [Python 3 is killing Python](https://medium.com/@deliciousrobots/5d2ad703365d/)
- [Python 3 can revive Python](https://medium.com/p/2a7af4788b10)
- [Python 3 is fine](https://web.archive.org/web/20140530010014/http://sealedabstract.com:80/rants/python-3-is-fine/)
