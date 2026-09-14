---
title: "Python LEGB 规则与作用域解析"
title_en: "Python LEGB Rule & Scope Resolution"
source: https://sebastianraschka.com/Articles/2014_python_scope_and_namespaces.html
crawled: 2026-09-06
translated: 2026-09-14
---

# Python LEGB 规则与作用域解析

> 原文：[Python LEGB Rule & Scope Resolution](https://sebastianraschka.com/Articles/2014_python_scope_and_namespaces.html) · Sebastian Raschka's Articles

这是一篇关于 Python 命名空间以及如何使用 LEGB 规则对变量名进行作用域解析的简短教程。接下来的各节将给出一些简短的示例代码块来展示问题，并附上简短的说明。你可以只是从头到尾通读本教程，但我更建议你动手执行这些代码片段——你可以复制粘贴它们，或者为了方便起见，直接[下载这个 IPython notebook](https://raw.githubusercontent.com/rasbt/python_reference/master/tutorials/scope_resolution_legb_rule.ipynb)。

## 章节

## 学习目标

- 命名空间与作用域——Python 到哪里查找变量名？
- 我们能否同时为多个对象定义/复用变量名？
- Python 以怎样的顺序在不同的命名空间中查找变量名？

## 命名空间与作用域简介

### 命名空间

粗略地说，命名空间（namespace）只是把名称映射到对象的容器。你可能已经听说过，Python 中的一切——字面量、列表、字典、函数、类等等——都是对象。  
这种「名称到对象」的映射使我们能够通过赋给对象的名称来访问它。例如，当我们通过 `a_string = "Hello string"` 做一个简单的字符串赋值时，就创建了对 `"Hello string"` 对象的一个引用，此后便可以通过变量名 `a_string` 来访问它。

我们可以把命名空间想象成一种 Python 字典结构：字典的键代表名称，字典的值代表对象本身（当前 Python 中的命名空间也正是这样实现的），例如：

```python
a_namespace = {'name_a':object_1, 'name_b':object_2, ...}
```

现在，棘手之处在于：Python 中存在多个彼此独立的命名空间，而名称可以在不同的命名空间中被复用（只有对象本身才是唯一的），例如：

```python
a_namespace = {'name_a':object_1, 'name_b':object_2, ...}
b_namespace = {'name_a':object_3, 'name_b':object_4, ...}
```

例如，每当我们运行一个 `for-loop` 或定义一个函数时，都会创建它自己的命名空间。命名空间还具有不同的层级（即所谓的「作用域」），下一节我们会更详细地讨论。

### 作用域

在上一节中我们了解到，命名空间可以彼此独立地存在，并且按某种层级结构组织，这就引出了「作用域」（scope）的概念。Python 中的「作用域」定义了我们在哪一层级上查找命名空间中特定的「名称到对象」映射。  
例如，来看看下面这段代码：

```python
i = 1

def foo():
    i = 5
    print(i, 'in foo()')

print(i, 'global')

foo()
```

```python
1 global
5 in foo()
```

这里我们只是把变量名 `i` 定义了两次，其中一次是在 `foo` 函数中。

- `foo_namespace = {'i':object_3, ...}`
- `global_namespace = {'i':object_1, 'name_b':object_2, ...}`

那么，当我们想打印变量 `i` 的值时，Python 是如何知道该去查找哪个命名空间的呢？这正是 Python 的 LEGB 规则发挥作用的地方，我们将在下一节讨论。

### 提示：

如果我们想打印出全局变量和局部变量的字典映射，可以使用 `globals()` 和 `locals()` 这两个函数

```python
#print(globals()) # prints global namespace
#print(locals()) # prints local namespace

glob = 1

def foo():
    loc = 5
    print('loc in foo():', 'loc' in locals())

foo()
print('loc in global:', 'loc' in globals())    
print('glob in global:', 'foo' in globals())
```

```python
loc in foo(): True
loc in global: False
glob in global: True
```

### 通过 LEGB 规则解析变量名的作用域。

我们已经看到，多个命名空间可以彼此独立地存在，并且它们可以在不同的层级上包含相同的变量名。「作用域」定义了 Python 在哪一层级上查找某个「变量名」及其关联的对象。接下来的问题是：「在找到『名称到对象』的映射之前，Python 以怎样的顺序查找各个层级的命名空间？」  
答案是：它使用 LEGB 规则，LEGB 代表

**Local -> Enclosed -> Global -> Built-in**（局部 -> 闭包 -> 全局 -> 内置），

其中的箭头表示命名空间层级查找顺序的方向。

- *Local*（局部）例如可以是函数或类方法的内部。
- *Enclosed*（闭包）可以指它的 `enclosing`（外层）函数，例如当一个函数被包裹在另一个函数内部时。
- *Global*（全局）指的是正在执行的脚本本身的最顶层，而
- *Built-in*（内置）则是 Python 为自己保留的特殊名称。

因此，如果在局部命名空间中找不到某个特定的「名称:对象」映射，接下来就会查找闭包作用域的命名空间。如果对闭包作用域的查找也不成功，Python 会继续转向全局命名空间，最后才会查找内置命名空间（顺便一提：如果在任何命名空间中都找不到某个名称，就会抛出 *NameError*）。

**注意**：

命名空间还可以进一步嵌套，例如当我们导入模块或定义新类的时候。在这些情况下，我们必须使用前缀来访问这些嵌套的命名空间。下面用一段代码来说明这个概念：

```python
import numpy
import math
import scipy

print(math.pi, 'from the math module')
print(numpy.pi, 'from the numpy package')
print(scipy.pi, 'from the scipy package')
```

```python
3.141592653589793 from the math module
3.141592653589793 from the numpy package
3.141592653589793 from the scipy package
```

（这也是为什么我们在使用「`from a_module import *`」导入模块时必须小心：它会把变量名加载进全局命名空间，有可能覆盖已经存在的变量名。）

![Scope resolution legb rule scope resolution 1](https://sebastianraschka.com/images/blog/2014/scope_resolution_legb_rule/scope_resolution_1.webp)

## 1. LG——局部与全局作用域

**示例 1.1**  
作为热身练习，让我们先暂时忘掉 LEGB 规则中的闭包（E）和内置（B）作用域，只关注 LG——局部与全局作用域。  
下面的代码会打印出什么？

```python
a_var = 'global variable'

def a_func():
    print(a_var, '[ a_var inside a_func() ]')

a_func()
print(a_var, '[ a_var outside a_func() ]')
```

**a)**

```python
raises an error
```

**b)**

```python
global value [ a_var outside a_func() ]
```

**c)**

```python
global value [ a_var inside a_func() ]  
global value [ a_var outside a_func() ]
```

### 原因解析：

我们先调用 `a_func()`，它要打印 `a_var` 的值。按照 LEGB 规则，函数会先在自己的局部作用域（L）中查找 `a_var` 是否有定义。由于 `a_func()` 并没有定义自己的 `a_var`，它会向上一层到全局作用域（G）中查找，而 `a_var` 恰好之前就定义在那里。

**示例 1.2**  
现在，让我们在全局作用域和局部作用域中都定义变量 `a_var`。  
你能猜到下面的代码会输出什么吗？

```python
a_var = 'global value'

def a_func():
    a_var = 'local value'
    print(a_var, '[ a_var inside a_func() ]')

a_func()
print(a_var, '[ a_var outside a_func() ]')
```

**a)**

```python
raises an error
```

**b)**

```python
local value [ a_var inside a_func() ]
global value [ a_var outside a_func() ]
```

**c)**

```python
global value [ a_var inside a_func() ]  
global value [ a_var outside a_func() ]
```

### 原因解析：

当我们调用 `a_func()` 时，它会先在局部作用域（L）中查找 `a_var`；由于 `a_var` 在 `a_func` 的局部作用域中有定义，所以打印出来的是赋给它的值 `local variable`。注意，这并不会影响全局变量，因为全局变量位于另一个不同的作用域。

不过，如果使用 global 关键字，我们也可以修改全局变量，例如为它重新赋一个新值，正如下面的例子所示：

```python
a_var = 'global value'

def a_func():
    global a_var
    a_var = 'local value'
    print(a_var, '[ a_var inside a_func() ]')

print(a_var, '[ a_var outside a_func() ]')
a_func()
print(a_var, '[ a_var outside a_func() ]')
```

```python
global value [ a_var outside a_func() ]
local value [ a_var inside a_func() ]
local value [ a_var outside a_func() ]
```

但我们必须注意顺序：如果没有明确告诉 Python 我们要使用全局作用域就试图修改变量的值，很容易引发 `UnboundLocalError`（记住，赋值操作的右侧会先执行）：

```python
a_var = 1

def a_func():
    a_var = a_var + 1
    print(a_var, '[ a_var inside a_func() ]')

print(a_var, '[ a_var outside a_func() ]')
a_func()
```

```python
---------------------------------------------------------------------------
UnboundLocalError                         Traceback (most recent call last)

<ipython-input-4-a6cdd0ee9a55> in <module>()
      6
      7 print(a_var, '[ a_var outside a_func() ]')
----> 8 a_func()

<ipython-input-4-a6cdd0ee9a55> in a_func()
      2
      3 def a_func():
----> 4     a_var = a_var + 1
      5     print(a_var, '[ a_var inside a_func() ]')
      6

UnboundLocalError: local variable 'a_var' referenced before assignment

1 [ a_var outside a_func() ]
```

## 2. LEG——局部、闭包与全局作用域

现在，让我们引入闭包（E）作用域的概念。按照「Local -> Enclosed -> Global」的顺序，你能猜到下面的代码会打印什么吗？

**示例 2.1**

```python
a_var = 'global value'

def outer():
    a_var = 'enclosed value'

    def inner():
        a_var = 'local value'
        print(a_var)

    inner()

outer()
```

**a)**

```python
global value
```

**b)**

```python
enclosed value
```

**c)**

```python
local value
```

### 原因解析：

让我们快速回顾一下刚才做了什么：我们调用了 `outer()`，它在局部定义了变量 `a_var`（与全局作用域中已存在的 `a_var` 并存）。接着，`outer()` 函数调用了 `inner()`，后者同样定义了一个名为 `a_var` 的变量。`inner()` 中的 `print()` 函数先在局部作用域中查找（L->E），然后才沿作用域层级向上搜索，因此它打印的是局部作用域中所赋的值。

与上一节看到的 `global` 关键字的概念类似，我们可以在内层函数中使用 `nonlocal` 关键字，显式地访问外层（闭包）作用域中的变量并修改其值。  
注意，`nonlocal` 关键字是 Python 3.x 中新增的，（目前）尚未在 Python 2.x 中实现。

```python
a_var = 'global value'

def outer():
       a_var = 'local value'
       print('outer before:', a_var)
       def inner():
           nonlocal a_var
           a_var = 'inner value'
           print('in inner():', a_var)
       inner()
       print("outer after:", a_var)
outer()
```

```python
outer before: local value
in inner(): inner value
outer after: inner value
```

## 3. LEGB——局部、闭包、全局、内置

最后，为了把 LEGB 规则讲完整，我们来看内置作用域。这里，我们将定义一个「自己的」求长度函数，它的名字恰好与内置的 `len()` 函数相同。如果执行下面的代码，你预期会得到什么结果？

**示例 3**

```python
a_var = 'global variable'

def len(in_var):
    print('called my len() function')
    l = 0
    for i in in_var:
        l += 1
    return l

def a_func(in_var):
    len_in_var = len(in_var)
    print('Input variable is of length', len_in_var)

a_func('Hello, World!')
```

**a)**

```python
raises an error (conflict with in-built `len()` function)
```

**b)**

```python
called my len() function
Input variable is of length 13
```

**c)**

```python
Input variable is of length 13
```

### 原因解析：

由于完全相同的名称可以映射到不同的对象——只要这些名称位于不同的命名空间中——那么复用 `len` 这个名字来定义我们自己的求长度函数就没有任何问题（这只是为了演示，并不推荐这样做）。当 `a_func()` 沿着 Python 的 L -> E -> G -> B 层级向上查找时，它先在全局作用域（G）中就找到了 `len()`，根本轮不到去查找内置（B）命名空间。

## 自测练习

现在，已经做完了几道练习，让我们快速检验一下学习成果。再来一次：下面的代码会打印出什么？

```python
a = 'global'

def outer():

    def len(in_var):
        print('called my len() function: ', end="")
        l = 0
        for i in in_var:
            l += 1
        return l

    a = 'local'

    def inner():
        global len
        nonlocal a
        a += ' variable'
    inner()
    print('a is', a)
    print(len(a))

outer()

print(len(a))
print('a is', a)
```

## 结论

希望这篇简短的教程有助于你理解使用 LEGB 规则的 Python 作用域解析顺序这一基本概念。我建议你（作为一个小小的自测练习）明天再回来看这些代码片段，检验自己能否正确预测它们所有的输出结果。

### 一条经验法则

在实践中，**在函数作用域内修改全局变量通常是个坏主意**，因为这常常是造成混乱和难以调试的奇怪错误的根源。  
如果你想通过函数修改一个全局变量，推荐的做法是把它作为参数传入，再用返回值重新赋值。  
例如：

```python
a_var = 2

def a_func(some_var):
    return 2**3

a_var = a_func(a_var)
print(a_var)
```

```python
8
```

### 参考答案

为了避免你不小心看到剧透，我把答案写成了二进制格式。要显示其字符表示，你只需执行下面这几行代码：

```python
print('Example 1.1:', chr(int('01100011',2)))
```

```python
print('Example 1.2:', chr(int('01100010',2)))
```

```python
print('Example 2.1:', chr(int('01100011',2)))
```

```python
print('Example 3.1:', chr(int('01100010',2)))
```

```python
# Execute to run the self-assessment solution

sol = "000010100110111101110101011101000110010101110010001010"\
"0000101001001110100000101000001010011000010010000001101001011100110"\
"0100000011011000110111101100011011000010110110000100000011101100110"\
"0001011100100110100101100001011000100110110001100101000010100110001"\
"1011000010110110001101100011001010110010000100000011011010111100100"\
"1000000110110001100101011011100010100000101001001000000110011001110"\
"1010110111001100011011101000110100101101111011011100011101000100000"\
"0011000100110100000010100000101001100111011011000110111101100010011"\
"0000101101100001110100000101000001010001101100000101001100001001000"\
"0001101001011100110010000001100111011011000110111101100010011000010"\
"1101100"

sol_str =''.join(chr(int(sol[i:i+8], 2)) for i in range(0, len(sol), 8))
for line in sol_str.split('\n'):
    print(line)
```

### 警告：for 循环变量「泄漏」到全局命名空间

与某些其他编程语言不同，`for-loops` 会使用其所在的作用域，并把定义的循环变量留在该作用域中。

```python
for a in range(5):
    if a == 4:
        print(a, '-> a in for-loop')
print(a, '-> a in global')
```

```python
4 -> a in for-loop
4 -> a in global
```

**即使我们之前已经在全局命名空间中显式定义过 `for-loop` 变量，情况也一样！**此时它会重新绑定（rebind）已有的变量：

```python
b = 1
for b in range(5):
    if b == 4:
        print(b, '-> b in for-loop')
print(b, '-> b in global')
```

```python
4 -> b in for-loop
4 -> b in global
```

不过在 **Python 3.x** 中，我们可以借助闭包（closure）来防止 for 循环变量侵入全局命名空间。下面是一个例子（在 Python 3.4 中执行）：

```python
i = 1
print([i for i in range(5)])
print(i, '-> i in global')
```

```python
[0, 1, 2, 3, 4]
1 -> i in global
```

为什么我要特意提「Python 3.x」呢？呃，碰巧的是，同一段代码在 Python 2.x 中执行会打印出：

```python
4 -> i in global
```

这源于 Python 3.x 中做出的一项改动，在 [What's New In Python 3.0](https://docs.python.org/3/whatsnew/3.0.html) 中是这样描述的：

「列表推导式不再支持 `[... for var in item1, item2, ...]` 这样的语法形式。请改用 `[... for var in (item1, item2, ...)]`。另外要注意，列表推导式的语义有所不同：它们更接近于在 `list()` 构造器内包裹一个生成器表达式的语法糖，尤其是循环控制变量不再泄漏到外围作用域中。」
