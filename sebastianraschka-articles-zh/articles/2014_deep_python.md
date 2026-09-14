---
title: "深入 Python 底层"
title_en: "Diving deep into Python"
source: https://sebastianraschka.com/Articles/2014_deep_python.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 深入 Python 底层

> 原文：[Diving deep into Python](https://sebastianraschka.com/Articles/2014_deep_python.html) · Sebastian Raschka's Articles

## 章节

### 多重继承的 C3 类解析算法

当我们处理多重继承时，按照较新的 C3 类解析算法，规则如下：  
假设子类 C 同时继承自两个父类 A 和 B，那么「应先检查类 A，再检查类 B」。

如果你想了解更多，请阅读 Guido van Rossum 的[原博客文章](http://python-history.blogspot.ru/2010/06/method-resolution-order.html)。

（原始来源：<http://gistroll.com/rolls/21/horizontal_assessments/new>）

```python
class A(object):
    def foo(self):
        print("class A")

class B(object):
    def foo(self):
        print("class B")

class C(A, B):
    pass

C().foo()
```

```python
class A
```

上面实际发生的事情是：类 `C` 先在父类 `A` 的作用域中查找方法 `.foo()`（而且找到了）！

我收到一封邮件，对方建议用一个嵌套层次更多的例子来更好地阐明 Guido van Rossum 的观点：

```python
class A(object):
   def foo(self):
      print("class A")

class B(A):
   pass

class C(A):
   def foo(self):
      print("class C")

class D(B,C):
   pass

D().foo()
```

```python
class C
```

这里，类 `D` 先在 `B` 中查找，而 `B` 又继承自 `A`（注意类 `C` 同样继承自 `A`，但它有自己的 `.foo()` 方法），由此我们得到的搜索顺序是：`D, B, C, A`。

### 赋值运算符与列表——「简单相加」与「相加并赋值」运算符

众所周知，Python 的 `list`（列表）是可变对象。因此，如果我们对列表使用 `+=` 运算符，实际上是通过直接修改对象本身来扩展列表。

然而，如果我们通过 `my_list = my_list + ...` 的方式赋值，则会创建一个全新的列表对象，下面的代码可以证明这一点：

```python
a_list = []
print('ID:', id(a_list))

a_list += [1]
print('ID (+=):', id(a_list))

a_list = a_list + [2]
print('ID (list = list + ...):', id(a_list))
```

```python
ID: 4366496544
ID (+=): 4366496544
ID (list = list + ...): 4366495472
```

顺便一提，`.append()` 和 `.extends()` 方法正如预期那样，是在原处修改列表对象的。

```python
a_list = []
print(a_list, '\nID (initial):',id(a_list), '\n')

a_list.append(1)
print(a_list, '\nID (append):',id(a_list), '\n')

a_list.extend([2])
print(a_list, '\nID (extend):',id(a_list))
```

```python
[]
ID (initial): 140704077653128

[1]
ID (append): 140704077653128

[1, 2]
ID (extend): 140704077653128
```

### datetime 模块中的 `True` 与 `False`

「程序员们常常会大跌眼镜地发现（有时是通过一个难以复现的 bug）：午夜（即 `datetime.time(0,0,0)`）与其他任何时间值都不同，它的布尔值是 False。python-ideas 邮件列表上的一场长篇讨论表明，尽管令人意外，这种行为是符合期望的——至少在某些圈子里是如此。」

（原始来源：<http://lwn.net/SubscriberLink/590299/bf73fe823974acea/>）

```python
import datetime

print('"datetime.time(0,0,0)" (Midnight) ->', bool(datetime.time(0,0,0)))

print('"datetime.time(1,0,0)" (1 am) ->', bool(datetime.time(1,0,0)))
```

```python
"datetime.time(0,0,0)" (Midnight) -> False
"datetime.time(1,0,0)" (1 am) -> True
```

### Python 会为小整数复用对象——判相等用 `==`，判同一用 `is`

之所以出现这种怪现象，是因为 Python 会维护一个小整数对象数组（即 -5 到 256 之间的整数，[参见文档](https://docs.python.org/2/c-api/int.html#PyInt_FromLong)）。

```python
a = 1
b = 1
print('a is b', bool(a is b))
True

c = 999
d = 999
print('c is d', bool(c is d))
```

```python
a is b True
c is d False
```

（*我收到一条评论指出，这实际上是 CPython 的实现产物，在 Python 的所有实现中**未必都成立**！*）

所以要点是：判断相等性永远用 `==`，判断同一性用 `is`！

这里有一篇[不错的文章](http://python.net/%7Egoodger/projects/pycon/2007/idiomatic/handout.html#other-languages-have-variables)，通过比较「盒子」（C 语言）与「名字标签」（Python）来解释这一概念。

下面的例子表明，这一规律确实适用于 -5 到 256 范围内的整数：

```python
print('256 is 257-1', 256 is 257-1)
print('257 is 258-1', 257 is 258 - 1)
print('-5 is -6+1', -5 is -6+1)
print('-7 is -6-1', -7 is -6-1)
```

```python
256 is 257-1 True
257 is 258-1 False
-5 is -6+1 True
-7 is -6-1 False
```

#### 再来演示相等性测试（`==`）与同一性测试（`is`）的对比：

```python
a = 'hello world!'
b = 'hello world!'
print('a is b,', a is b)
print('a == b,', a == b)
```

```python
a is b, False
a == b, True
```

我们可能会以为同一性必然蕴含相等性，但事实并非总是如此，下一个例子就能说明这一点：

```python
a = float('nan')
print('a is a,', a is a)
print('a == a,', a == a)
```

```python
a is a, True
a == a, False
```

### 当列表包含其他结构与对象时的浅拷贝与深拷贝

**浅拷贝（shallow copy）**：  
如果我们用赋值运算符把一个列表赋给另一个列表，仅仅是创建了一个指向原列表的新名字引用。如果想创建新的列表对象，就必须对原列表进行拷贝，这可以通过 `a_list[:]` 或 `a_list.copy()` 来完成。

```python
list1 = [1,2]
list2 = list1        # reference
list3 = list1[:]     # shallow copy
list4 = list1.copy() # shallow copy

print('IDs:\nlist1: {}\nlist2: {}\nlist3: {}\nlist4: {}\n'
      .format(id(list1), id(list2), id(list3), id(list4)))

list2[0] = 3
print('list1:', list1)

list3[0] = 4
list4[1] = 4
print('list1:', list1)
```

```python
IDs:
list1: 4346366472
list2: 4346366472
list3: 4346366408
list4: 4346366536

list1: [3, 2]
list1: [3, 2]
```

**深拷贝（deep copy）**  
正如上面所见，如果我们想创建一个包含原列表内容、且可以独立修改的新列表，浅拷贝就已经够用了。

然而，如果要处理的是复合对象（例如包含其他列表的列表，更多信息请[阅读这里](https://docs.python.org/2/library/copy.html)），事情就变得有些棘手了。

对于复合对象，浅拷贝会创建一个新的复合对象，但它只是把指向被包含对象的引用插入到这个新复合对象中。相比之下，深拷贝会走得更「深」，还会为原复合对象中所包含的对象创建新对象。  
跟着代码走一遍，这个概念应该会更清晰：

```python
from copy import deepcopy

list1 = [[1],[2]]
list2 = list1.copy()    # shallow copy
list3 = deepcopy(list1) # deep copy

print('IDs:\nlist1: {}\nlist2: {}\nlist3: {}\n'
      .format(id(list1), id(list2), id(list3)))

list2[0][0] = 3
print('list1:', list1)

list3[0][0] = 5
print('list1:', list1)
```

```python
IDs:
list1: 4377956296
list2: 4377961752
list3: 4377954928

list1: [[3], [2]]
list1: [[3], [2]]
```

### 从逻辑 `and` 与 `or` 中挑出的 `True` 值

**逻辑 `or`：**

`a or b == a if a else b`

- 在 `or` 表达式中，如果两个值都为 `True`，Python 会选择第一个值（例如在 `"a" or "b"` 中选择 `"a"`）；而在 `and` 表达式中则会选择第二个值。  
  这也被称为**短路求值（short-circuiting）**——我们已经知道，只要第一个值为 `True`，逻辑 `or` 的结果就必然为 `True`，因此可以省略对第二个值的求值。

**逻辑 `and`：**

`a and b == b if a else a`

- 在 `and` 表达式中，如果两个值都为 `True`，Python 会选择第二个值，因为对逻辑 `and` 而言，两个值都必须为真。

```python
result = (2 or 3) * (5 and 7)
print('2 * 7 =', result)
```

```python
2 * 7 = 14
```

### 不要把可变对象用作函数的默认参数！

不要把可变对象（例如字典、列表、集合等）用作函数的默认参数！你可能以为，每当我们不提供默认参数对应的实参而调用函数时，都会新建一个列表，但事实并非如此：**Python 会在函数第一次被定义时创建这个可变对象（默认参数）——而不是在函数被调用时**，请看下面的代码：

（原始来源：<http://docs.python-guide.org/en/latest/writing/gotchas/>

```python
def append_to_list(value, def_list=[]):
    def_list.append(value)
    return def_list

my_list = append_to_list(1)
print(my_list)

my_other_list = append_to_list(2)
print(my_other_list)
```

```python
[1]
[1, 2]
```

另一个很好的例子同样说明，默认参数是在函数被创建时（**而不是被调用时！**）生成的：

```python
import time
def report_arg(my_default=time.time()):
    print(my_default)

report_arg()

time.sleep(5)

report_arg()
```

```python
1397764090.456688
1397764090.456688
```

### 小心生成器会被「消耗」

要注意把 «`in`» 检查与生成器结合使用时会发生什么，因为一旦某个位置被「消耗」掉，生成器就不会再从头开始求值。

```python
gen = (i for i in range(5))
print('2 in gen,', 2 in gen)
print('3 in gen,', 3 in gen)
print('1 in gen,', 1 in gen)
```

```python
2 in gen, True
3 in gen, True
1 in gen, False
```

尽管这样做（在大多数情况下）违背了使用生成器的初衷，但我们可以把生成器转换成列表来绕过这个问题。

```python
gen = (i for i in range(5))
a_list = list(gen)
print('2 in l,', 2 in a_list)
print('3 in l,', 3 in a_list)
print('1 in l,', 1 in a_list)
```

```python
2 in l, True
3 in l, True
1 in l, True
```

### `bool` 是 `int` 的子类

先有鸡还是先有蛋？在 Python 的历史上（确切地说是 Python 2.2），真值是通过 1 和 0 来实现的（与早期的 C 语言类似）。为了避免旧的（但完全能正常工作的）Python 代码出现语法错误，Python 2.3 中把 `bool` 作为 `int` 的子类加了进来。

原始来源：<http://www.peterbe.com/plog/bool-is-int>

```python
print('isinstance(True, int):', isinstance(True, int))
print('True + True:', True + True)
print('3*True + True:', 3*True + True)
print('3*True - False:', 3*True - False)
```

```python
isinstance(True, int): True
True + True: 2
3*True + True: 4
3*True - False: 3
```

### 关于「闭包与循环中的 lambda」陷阱

还记得关于[「生成器会被消耗」](#be-aware-of-the-consuming-generator)的那一节吗？这个例子与它有些关联，但结果可能依然出人意料。

（原始来源：<http://openhome.cc/eGossip/Blog/UnderstandingLambdaClosure3.html>）

在下面的第一个例子中，我们在列表推导式里调用 `lambda` 函数，而每次调用 `lambda` 时都会对值 `i` 解引用。由于当我们 for 循环遍历列表时，列表推导式早已构建并求值完毕，闭包变量会被设为最后一个值 4。

```python
my_list = [lambda: i for i in range(5)]
for l in my_list:
    print(l())
```

```python
4
4
4
4
4
```

不过，通过使用生成器表达式，我们可以利用它逐步求值的特性（注意，返回的变量仍然来自同一个闭包，但其值会随着我们对生成器的迭代而变化）。

```python
my_gen = (lambda: n for n in range(5))
for l in my_gen:
    print(l())
```

```python
0
1
2
3
4
```

如果你确实偏爱使用列表，也有一个巧妙的办法可以绕过这个问题，正如一位读者在评论中友好指出的：我们可以直接把循环变量 `i` 作为默认参数传给各个 lambda。

```python
my_list = [lambda x=i: x for i in range(5)]
for l in my_list:
    print(l())
```

```python
0
1
2
3
4
```

### Python 的 LEGB 作用域解析与 `global`、`nonlocal` 关键字

Python 的 LEGB 作用域解析（Local（局部） -> Enclosed（嵌套） -> Global（全局） -> Built-in（内置））并没有什么特别出人意料的地方，但看一些例子仍然很有帮助！

#### `global` 与 `local`

根据 LEGB 规则，Python 会首先在局部作用域中查找变量。因此，如果我们在函数作用域内以 `local`（局部）方式设置变量 `x = 1`，它不会对 `global`（全局）的 `x` 产生任何影响。

```python
x = 0
def in_func():
    x = 1
    print('in_func:', x)

in_func()
print('global:', x)
```

```python
in_func: 1
global: 0
```

如果我们想通过函数修改 `global` 的 x，只需使用 `global` 关键字把该变量引入函数的作用域即可：

```python
x = 0
def in_func():
    global x
    x = 1
    print('in_func:', x)

in_func()
print('global:', x)
```

```python
in_func: 1
global: 1
```

#### `local` 与 `enclosed`

现在来看看 `local` 与 `enclosed` 的对比。这里，我们在 `outer` 函数中设置变量 `x = 1`，并在被嵌套的函数 `inner` 中设置 `x = 1`。由于 `inner` 会先在局部作用域中查找，它不会修改 `outer` 的 `x`。

```python
def outer():
       x = 1
       print('outer before:', x)
       def inner():
           x = 2
           print("inner:", x)
       inner()
       print("outer after:", x)
outer()
```

```python
outer before: 1
inner: 2
outer after: 1
```

这时 `nonlocal` 关键字就派上用场了——它允许我们修改 `enclosed`（外层嵌套）作用域中的变量 `x`：

```python
def outer():
       x = 1
       print('outer before:', x)
       def inner():
           nonlocal x
           x = 2
           print("inner:", x)
       inner()
       print("outer after:", x)
outer()
```

```python
outer before: 1
inner: 2
outer after: 2
```

### 当不可变元组中的可变内容不再那么「不可变」

众所周知，元组在 Python 中是不可变对象，对吧！？可如果它们包含的是可变对象，会发生什么呢？

首先看看符合预期的行为：如果我们试图修改元组中的不可变类型，会抛出 `TypeError`：

```python
tup = (1,)
tup[0] += 1
```

```python
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)

<ipython-input-41-c3bec6c3fe6f> in <module>()
      1 tup = (1,)
----> 2 tup[0] += 1

TypeError: 'tuple' object does not support item assignment
```

#### 可要是我们把一个可变对象放进不可变的元组呢？嗯，修改确实生效了，但**同时**我们也会得到一个 `TypeError`。

```python
tup = ([],)
print('tup before: ', tup)
tup[0] += [1]
```

```python
tup before:  ([],)

---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)

<ipython-input-42-aebe9a31dbeb> in <module>()
      1 tup = ([],)
      2 print('tup before: ', tup)
----> 3 tup[0] += [1]

TypeError: 'tuple' object does not support item assignment
```

```python
print('tup after: ', tup)
```

```python
tup after:  ([1],)
```

不过，**还是有办法**在不触发 `TypeError` 的情况下修改元组中的可变内容的——解决方案是 `.extend()` 方法，或者（对列表而言）`.append()`：

```python
tup = ([],)
print('tup before: ', tup)
tup[0].extend([1])
print('tup after: ', tup)
```

```python
tup before:  ([],)
tup after:  ([1],)
```

```python
tup = ([],)
print('tup before: ', tup)
tup[0].append(1)
print('tup after: ', tup)
```

```python
tup before:  ([],)
tup after:  ([1],)
```

#### 解释

**A. Jesse Jiryu Davis** 对这一现象有一段精彩的解释（原始来源：<http://emptysqua.re/blog/python-increment-is-weird-part-ii/>）

如果我们试图通过 `+=` 来扩展列表，*「那么该语句会执行 `STORE_SUBSCR`，后者调用 C 函数 `PyObject_SetItem`，由它检查该对象是否支持条目赋值（item assignment）。在我们的例子中，对象是一个元组，所以 `PyObject_SetItem` 抛出了 `TypeError`。谜底揭晓。」*

##### 关于元组 `immutable` 身份的补充说明。元组以不可变著称，可为什么下面这段代码却能正常工作？

```python
my_tup = (1,)
my_tup += (4,)
my_tup = my_tup + (5,)
print(my_tup)
```

```python
(1, 4, 5)
```

幕后实际发生的事情是：元组并没有被修改，而是每次都生成了一个新对象，并继承了旧的「名字标签」：

```python
my_tup = (1,)
print(id(my_tup))
my_tup += (4,)
print(id(my_tup))
my_tup = my_tup + (5,)
print(id(my_tup))
```

```python
4337381840
4357415496
4357289952
```

### 列表推导式很快，但生成器更快！？

「列表推导式很快，但生成器更快！？」——不，并非如此（或者说并没有显著差距，见下面的基准测试）。那么，到底该依据什么在两者之间做选择呢？

- 如果你想使用丰富的列表方法，就使用列表
- 当处理超大集合时，使用生成器以避免内存问题

```python
import timeit

def plainlist(n=100000):
    my_list = []
    for i in range(n):
        if i % 5 == 0:
            my_list.append(i)
    return my_list

def listcompr(n=100000):
    my_list = [i for i in range(n) if i % 5 == 0]
    return my_list

def generator(n=100000):
    my_gen = (i for i in range(n) if i % 5 == 0)
    return my_gen

def generator_yield(n=100000):
    for i in range(n):
        if i % 5 == 0:
            yield i
```

#### 为了对列表公平起见，让我们把生成器耗尽：

```python
def test_plainlist(plain_list):
    for i in plain_list():
        pass

def test_listcompr(listcompr):
    for i in listcompr():
        pass

def test_generator(generator):
    for i in generator():
        pass

def test_generator_yield(generator_yield):
    for i in generator_yield():
        pass

print('plain_list:     ', end = '')
%timeit test_plainlist(plainlist)
print('\nlistcompr:     ', end = '')
%timeit test_listcompr(listcompr)
print('\ngenerator:     ', end = '')
%timeit test_generator(generator)
print('\ngenerator_yield:     ', end = '')
%timeit test_generator_yield(generator_yield)
```

```python
plain_list:     10 loops, best of 3: 22.4 ms per loop

listcompr:     10 loops, best of 3: 20.8 ms per loop

generator:     10 loops, best of 3: 22 ms per loop

generator_yield:     10 loops, best of 3: 21.9 ms per loop
```

### 公有与私有类方法及名称改写（name mangling）

在 Python 社区里，谁还没有偶尔撞见「我们都是自愿的成年人」（we are all consenting adults here）这句话呢？与 C++ 等其他语言不同（抱歉，还有很多别的语言，但 C++ 是我最熟悉的一种），我们无法真正保护类方法不被类外部（也就是 API 使用者）使用。  
我们所能做的，只是把方法标记为私有，以表明它们不应在类外部使用，但最终仍然取决于类的使用者，因为「我们都是自愿的成年人」！  
所以，当我们想把一个类方法标记为私有时，可以在它前面加上一个下划线。  
如果还想避免与其他可能使用相同方法名的类发生命名冲突，可以在名称前加上双下划线来触发名称改写（name mangling）。

不过，这并不能阻止类的使用者访问这个类成员，只是他们必须知道这个窍门，并且明白风险自负……

让下面的例子来说明我的意思：

```python
class my_class():
    def public_method(self):
        print('Hello public world!')
    def __private_method(self):
        print('Hello private world!')
    def call_private_method_in_class(self):
        self.__private_method()

my_instance = my_class()

my_instance.public_method()
my_instance._my_class__private_method()
my_instance.call_private_method_in_class()
```

```python
Hello public world!
Hello private world!
Hello private world!
```

### 遍历列表的同时修改列表的后果

在迭代列表的同时修改它可能非常危险——这是一个极为常见的陷阱，会导致非预期的行为！  
看看下面的例子，做个趣味小练习：在跳去看答案之前，先自己弄清楚发生了什么！

```python
a = [1, 2, 3, 4, 5]
for i in a:
    if not i % 2:
        a.remove(i)
print(a)
```

```python
[1, 3, 5]
```

```python
b = [2, 4, 5, 6]
for i in b:
     if not i % 2:
         b.remove(i)
print(b)
```

```python
[4, 5]
```

**答案**在于：我们是逐个索引地遍历列表的，一旦中途删除了某个元素，就不可避免地打乱了索引。看看下面的例子，一切就一目了然了：

```python
b = [2, 4, 5, 6]
for index, item in enumerate(b):
    print(index, item)
    if not item % 2:
        b.remove(item)
print(b)
```

```python
0 2
1 5
2 6
[4, 5]
```

### 动态绑定与变量名中的笔误

小心：动态绑定很方便，但也可能很快变得危险！

```python
print('first list:')
for i in range(3):
    print(i)

print('\nsecond list:')
for j in range(3):
    print(i) # I (intentionally) made typo here!
```

```python
first list:
0
1
2

second list:
2
2
2
```

### 使用「越界」索引进行列表切片

我们每个人一生中都遇到过 1（乘以 10000）次的、臭名昭著的 `IndexError`：

```python
my_list = [1, 2, 3, 4, 5]
print(my_list[5])
```

```python
---------------------------------------------------------------------------
IndexError                                Traceback (most recent call last)

<ipython-input-15-eb273dc36fdc> in <module>()
      1 my_list = [1, 2, 3, 4, 5]
----> 2 print(my_list[5])

IndexError: list index out of range
```

但令人意外的是，做列表切片时它却不会被抛出——这在调试时可能让人相当头疼：

```python
my_list = [1, 2, 3, 4, 5]
print(my_list[5:])
```

```python
[]
```

### 复用全局变量名与 `UnboundLocalError`

通常，在函数的局部作用域中访问全局变量是没有问题的：

```python
def my_func():
    print(var)

var = 'global'
my_func()
```

```python
global
```

同样，在局部作用域中使用相同的变量名而不影响其对应的那一个，也没有问题：

```python
def my_func():
    var = 'locally changed'

var = 'global'
my_func()
print(var)
```

```python
global
```

但如果某个变量名已经出现在全局作用域中，我们又想在局部函数作用域中访问并复用这个名字，就必须小心了：

```python
def my_func():
    print(var) # want to access global variable
    var = 'locally changed' # but Python thinks we forgot to define the local variable!

var = 'global'
my_func()
```

```python
---------------------------------------------------------------------------
UnboundLocalError                         Traceback (most recent call last)

<ipython-input-40-3afd870b7c35> in <module>()
      4
      5 var = 'global'
----> 6 my_func()

<ipython-input-40-3afd870b7c35> in my_func()
      1 def my_func():
----> 2     print(var) # want to access global variable
      3     var = 'locally changed'
      4
      5 var = 'global'

UnboundLocalError: local variable 'var' referenced before assignment
```

这种情况下，我们就必须使用 `global` 关键字了！

```python
def my_func():
    global var
    print(var) # want to access global variable
    var = 'locally changed' # changes the gobal variable

var = 'global'

my_func()
print(var)
```

```python
global
locally changed
```

### 创建可变对象的副本

假设这样一个场景：我们想复制存储在另一个列表中的子列表（sub`list`）。如果我们想创建独立的子列表对象，使用算术乘法运算符可能会带来相当出乎意料（或不尽如人意）的结果：

```python
my_list1 = [[1, 2, 3]] * 2

print('initially ---> ', my_list1)

# modify the 1st element of the 2nd sublist
my_list1[1][0] = 'a'
print("after my_list1[1][0] = 'a' ---> ", my_list1)
```

```python
initially --->  [[1, 2, 3], [1, 2, 3]]
after my_list1[1][0] = 'a' --->  [['a', 2, 3], ['a', 2, 3]]
```

在这种情况下，我们最好创建「新」对象：

```python
my_list2 = [[1, 2, 3] for i in range(2)]

print('initially:  ---> ', my_list2)

# modify the 1st element of the 2nd sublist
my_list2[1][0] = 'a'
print("after my_list2[1][0] = 'a':  ---> ", my_list2)
```

```python
initially:  --->  [[1, 2, 3], [1, 2, 3]]
after my_list2[1][0] = 'a':  --->  [[1, 2, 3], ['a', 2, 3]]
```

证据如下：

```python
for a,b in zip(my_list1, my_list2):
    print('id my_list1: {}, id my_list2: {}'.format(id(a), id(b)))
```

```python
id my_list1: 4350764680, id my_list2: 4350766472
id my_list1: 4350764680, id my_list2: 4350766664
```

### Python 2 与 3 的关键差异

已经有一些不错的文章总结了 Python 2 与 3 之间的差异，例如：

- <https://wiki.python.org/moin/Python2orPython3>
- <https://docs.python.org/3.0/whatsnew/3.0.html>
- <http://python3porting.com/differences.html>
- <https://docs.python.org/3/howto/pyporting.html>  
  等等。

但看看其中的一些内容——尤其是对 Python 新手而言——可能仍然值得！
（注：这些代码分别在 Python 3.4.0 和 Python 2.7.5 中执行，并复制自交互式 shell 会话。）

#### 概览——Python 2 与 3 的关键差异

- [Unicode](#unicode)
- [print 语句](#print)
- [整数除法](#integer_div)
- [xrange()](#xrange)
- [抛出异常](#raising_exceptions)
- [处理异常](#handling_exceptions)
- [next() 函数与 .next() 方法](#next_next)
- [循环变量泄漏到全局作用域](#loop_leak)
- [比较不可排序的类型](#compare_unorder)

#### Unicode……

[[回到 Python 2.x 与 3.x 概览](#py23_overview)]

##### - Python 2：

我们只有 ASCII 的 `str()` 类型、单独的 `unicode()`，而没有 `byte` 类型

##### - Python 3：

现在，我们终于有了 Unicode（utf-8）的 `str` 字符串，以及两个字节类：`byte` 和 `bytearray`

```python
#############
# Python 2
#############

>>> type(unicode('is like a python3 str()'))
<type 'unicode'>

>>> type(b'byte type does not exist')
<type 'str'>

>>> 'they are really' + b' the same'
'they are really the same'

>>> type(bytearray(b'bytearray oddly does exist though'))
<type 'bytearray'>

#############
# Python 3
#############

>>> print('strings are now utf-8 \u03BCnico\u0394é!')
strings are now utf-8 μnicoΔé!

>>> type(b' and we have byte types for storing data')
<class 'bytes'>

>>> type(bytearray(b'but also bytearrays for those who prefer them over strings'))
<class 'bytearray'>

>>> 'string' + b'bytes for data'
Traceback (most recent call last):s
  File "<stdin>", line 1, in <module>
TypeError: Can't convert 'bytes' object to str implicitly
```

#### print 语句

非常琐碎的一个改动，但很有道理：Python 3 现在只接受带规范括号的 `print`——就像其他函数调用一样……

```python
# Python 2
>>> print 'Hello, World!'
Hello, World!
>>> print('Hello, World!')
Hello, World!

# Python 3
>>> print('Hello, World!')
Hello, World!
>>> print 'Hello, World!'
  File "<stdin>", line 1
    print 'Hello, World!'
                        ^
SyntaxError: invalid syntax
```

如果我们想把两个连续 print 函数的输出打印在同一行上，在 Python 2 中你会用逗号，而在 Python 3 中则要用 `end=""`：

```python
# Python 2
>>> print "line 1", ; print 'same line'
line 1 same line

# Python 3
>>> print("line 1", end="") ; print (" same line")
line 1 same line
```

#### 整数除法

如果你正在移植代码，或在 Python 2 中执行 Python 3 的代码，这件事相当危险，因为整数除法行为的变化往往不会被察觉。  
所以，我在自己的 Python 3 脚本里仍然倾向于写 `float(3)/2` 或 `3/2.0` 而不是 `3/2`，好替还在用 Python 2 的朋友们省去一些麻烦……（附注：反过来，你也可以在 Python 2 脚本中 `from __future__ import division`）。

```python
# Python 2
>>> 3 / 2
1
>>> 3 // 2
1
>>> 3 / 2.0
1.5
>>> 3 // 2.0
1.0

# Python 3
>>> 3 / 2
1.5
>>> 3 // 2
1
>>> 3 / 2.0
1.5
>>> 3 // 2.0
1.0
```

###`xrange()`

在 Python 2.x 中，如果你想创建一个可迭代对象，`xrange()` 相当流行。它的行为与生成器十分相似（「惰性求值」），但你可以对它无限次迭代。它的优点是通常比 `range()` 更快（例如在 for 循环中）——但如果你需要多次遍历该列表就不然了，因为每次都要从头重新生成！  
在 Python 3 中，`range()` 已经按照 `xrange()` 函数的方式来实现，因此专门的 `xrange()` 函数已不复存在。

```python
# Python 2
> python -m timeit 'for i in range(1000000):' ' pass'
10 loops, best of 3: 66 msec per loop

    > python -m timeit 'for i in xrange(1000000):' ' pass'
10 loops, best of 3: 27.8 msec per loop

# Python 3
> python3 -m timeit 'for i in range(1000000):' ' pass'
10 loops, best of 3: 51.1 msec per loop

> python3 -m timeit 'for i in xrange(1000000):' ' pass'
Traceback (most recent call last):
  File "/Library/Frameworks/Python.framework/Versions/3.4/lib/python3.4/timeit.py", line 292, in main
    x = t.timeit(number)
  File "/Library/Frameworks/Python.framework/Versions/3.4/lib/python3.4/timeit.py", line 178, in timeit
    timing = self.inner(it, self.timer)
  File "<timeit-src>", line 6, in inner
    for i in xrange(1000000):
NameError: name 'xrange' is not defined
```

#### 抛出异常

Python 2 既接受「旧」写法也接受「新」写法，而 Python 3 则不然：如果我们不用括号把异常参数括起来，它就会噎住（并转而抛出 `SyntaxError`）：

```python
# Python 2
>>> raise IOError, "file error"
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IOError: file error
>>> raise IOError("file error")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IOError: file error

# Python 3    
>>> raise IOError, "file error"
  File "<stdin>", line 1
    raise IOError, "file error"
                 ^
SyntaxError: invalid syntax
>>> raise IOError("file error")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
OSError: file error
```

#### 处理异常

Python 3 中异常的处理方式也略有变化。现在，我们必须使用 `as` 关键字！

```python
# Python 2
>>> try:
...     blabla
... except NameError, err:
...     print err, '--> our error msg'
...
name 'blabla' is not defined --> our error msg

# Python 3
>>> try:
...     blabla
... except NameError as err:
...     print(err, '--> our error msg')
...
name 'blabla' is not defined --> our error msg
```

#### `next()` 函数与 `.next()` 方法

在 Python 2.7.5 中，函数和方法两种用法都可以，而在 Python 3 中就只剩下 `next()` 函数了！

```python
# Python 2
>>> my_generator = (letter for letter in 'abcdefg')
>>> my_generator.next()
'a'
>>> next(my_generator)
'b'

# Python 3
>>> my_generator = (letter for letter in 'abcdefg')
>>> next(my_generator)
'a'
>>> my_generator.next()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'generator' object has no attribute 'next'
```

#### 在 Python 3.x 中，for 循环变量不再泄漏到全局命名空间

这要归结于 Python 3.x 中做出的一项改动，[What's New In Python 3.0](https://docs.python.org/3/whatsnew/3.0.html) 中是这样描述的：

「列表推导式不再支持 `[... for var in item1, item2, ...]` 这种语法形式，请改用 `[... for var in (item1, item2, ...)]`。另请注意，列表推导式的语义有所不同：它们更接近于在 `list()` 构造器内包裹一个生成器表达式的语法糖，尤其是，循环控制变量不再泄漏到外围作用域。」

```python
from platform import python_version
print('This code cell was executed in Python', python_version())

i = 1
print([i for i in range(5)])
print(i, '-> i in global')
```

```python
This code cell was executed in Python 3.3.5
[0, 1, 2, 3, 4]
1 -> i in global
```

```python
from platform import python_version
print 'This code cell was executed in Python', python_version()

i = 1
print [i for i in range(5)]
print i, '-> i in global'
```

```python
This code cell was executed in Python 2.7.6
[0, 1, 2, 3, 4]
4 -> i in global
```

##### Python 3.x 阻止我们比较不可排序的类型

```python
from platform import python_version
print 'This code cell was executed in Python', python_version()

print [1, 2] > 'foo'
print (1, 2) > 'foo'
print [1, 2] > (1, 2)
```

```python
This code cell was executed in Python 2.7.6
False
True
False
```

```python
from platform import python_version
print('This code cell was executed in Python', python_version())

print([1, 2] > 'foo')
print((1, 2) > 'foo')
print([1, 2] > (1, 2))
```

```python
This code cell was executed in Python 3.3.5

---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)

<ipython-input-3-1d774c677f73> in <module>()
      2 print('This code cell was executed in Python', python_version())
      3
----> 4 [1, 2] > 'foo'
      5 (1, 2) > 'foo'
      6 [1, 2] > (1, 2)

TypeError: unorderable types: list() > str()
```

### 函数注解——我的 Python 代码里那些 `->` 是什么？

你有没有见过在函数定义的括号里使用冒号的 Python 代码？

```python
def foo1(x: 'insert x here', y: 'insert x^2 here'):
    print('Hello, World')
    return
```

那这里这个花哨的箭头又是怎么回事？

```python
def foo2(x, y) -> 'Hi!':
    print('Hello, World')
    return
```

问：这是合法的 Python 语法吗？  
答：合法！

问：那么，如果我只是*调用*这个函数，会发生什么？  
答：什么也不会发生！

证据如下！

```python
foo1(1,2)
```

```python
Hello, World
```

```python
foo2(1,2)
```

```python
Hello, World
```

\*\*所以，这些就是函数注解……\*\*

- 冒号用于函数参数
- 箭头用于返回值

你可能永远也用不到它们（或者至少极少用到）。通常，我们会把优秀的函数文档以 docstring 的形式写在函数下方——至少我是这么做的（好吧，我承认这个例子是有点极端）：

```python
def is_palindrome(a):
    """
    Case-and punctuation insensitive check if a string is a palindrom.

    Keyword arguments:
        a (str): The string to be checked if it is a palindrome.

    Returns `True` if input string is a palindrome, else False.

    """
    stripped_str = [l for l in my_str.lower() if l.isalpha()]
    return stripped_str == stripped_str[::-1]
```

不过，在某些情况下，函数注解可以用来表明工作仍在进行中。但它们是可选的，而且我极少极少见到它们。

正如 [PEP3107](http://legacy.python.org/dev/peps/pep-3107/#fundamentals-of-function-annotations) 所述：

1. 函数注解，无论用于参数还是返回值，都完全是可选的。
2. 函数注解不过是一种在编译时将任意 Python 表达式与函数各个部分关联起来的方式。

函数注解的一个妙处在于它的 `__annotations__` 属性，它是一个字典，收录了你注解过的所有参数和/或 `return` 返回值。

```python
foo1.__annotations__
```

```python
{'y': 'insert x^2 here', 'x': 'insert x here'}
```

```python
foo2.__annotations__
```

```python
{'return': 'Hi!'}
```

**它们什么时候有用？**

函数注解在以下几个方面可能有用：

- 一般性的文档说明
- 前置条件测试
- [类型检查](http://legacy.python.org/dev/peps/pep-0362/#annotation-checker)

……

### `finally` 块中的中止性语句

Python 的 `try-except-finally` 块非常适合用来捕获和处理错误。无论是否抛出了 `exception`（异常），`finally` 块总会被执行，下面的例子说明了这一点。

```python
def try_finally1():
    try:
        print('in try:')
        print('do some stuff')
        float('abc')
    except ValueError:
        print('an error occurred')
    else:
        print('no error occurred')
    finally:
        print('always execute finally')

try_finally1()
```

```python
in try:
do some stuff
an error occurred
always execute finally
```

但你也能猜出下一个代码单元会打印出什么吗？

```python
def try_finally2():
    try:
        print("do some stuff in try block")
        return "return from try block"
    finally:
        print("do some stuff in finally block")
        return "always execute finally"

print(try_finally2())
```

```python
do some stuff in try block
do some stuff in finally block
always execute finally
```

在这里，`finally` 块中那个中止性的 `return` 语句直接压过了 `try` 块中的 `return`，因为**`finally` 保证一定会被执行**。所以，在 `finally` 块中使用中止性语句时一定要小心！

## 把类型作为值赋给变量

我还不确定这能在什么场景下派上用场，但「可以把类型当作值赋给变量」这一点是个不错的冷知识。

```python
a_var = str
a_var(123)
```

```python
'123'
```

```python
from random import choice

a, b, c = float, int, str
for i in range(5):
    j = choice([a,b,c])(i)
    print(j, type(j))
```

```python
0 <class 'int'>
1 <class 'int'>
2.0 <class 'float'>
3 <class 'str'>
4 <class 'int'>
```

## 只有生成器的第一个子句会被立即求值

在某些情况下（也就是需要处理大量计算时），我们喜欢使用生成器的主要原因在于：它只在需要时才计算下一个值，这也就是所谓的「惰性」求值。
然而，生成器的第一个子句在创建时就已被检查，如下面的例子所示：

```python
gen_fails = (i for i in 1/0)
```

```python
---------------------------------------------------------------------------
ZeroDivisionError                         Traceback (most recent call last)

<ipython-input-18-29312e1ece8d> in <module>()
----> 1 gen_fails = (i for i in 1/0)

ZeroDivisionError: division by zero
```

当然，这是个不错的特性，因为它能让我们立即发现语法错误。然而（遗憾的是），如果生成器里有多个子句，情况就不是这样了。

```python
gen_succeeds = (i for i in range(5) for j in 1/0)
```

```python
print('But obviously fails when we iterate ...')
for i in gen_succeeds:
    print(i)
```

```python
---------------------------------------------------------------------------
ZeroDivisionError                         Traceback (most recent call last)

<ipython-input-20-8a83a1022971> in <module>()
      1 print('But obviously fails when we iterate ...')
----> 2 for i in gen_succeeds:
      3     print(i)

<ipython-input-19-c54c53f2218a> in <genexpr>(.0)
----> 1 gen_succeeds = (i for i in range(5) for j in 1/0)

ZeroDivisionError: division by zero

But obviously fails when we iterate ...
```

##关键字参数解包语法——`*args` 与 `**kwargs`

Python 有一套非常方便的「关键字参数解包语法」（常被称为「splat」运算符）。如果我们想定义一个能接受任意数量输入参数的函数，它尤其有用。

### 单星号（\*args）

```python
def a_func(*args):
    print('type of args:', type(args))
    print('args contents:', args)
    print('1st argument:', args[0])

a_func(0, 1, 'a', 'b', 'c')
```

```python
type of args: <class 'tuple'>
args contents: (0, 1, 'a', 'b', 'c')
1st argument: 0
```

### 双星号（\*\*kwargs）

```python
def b_func(**kwargs):
    print('type of kwargs:', type(kwargs))
    print('kwargs contents: ', kwargs)
    print('value of argument a:', kwargs['a'])

b_func(a=1, b=2, c=3, d=4)
```

```python
type of kwargs: <class 'dict'>
kwargs contents:  {'d': 4, 'a': 1, 'c': 3, 'b': 2}
value of argument a: 1
```

### （部分）解包可迭代对象

「解包」运算符另一个有用的应用，是对列表及其他可迭代对象进行解包。

```python
val1, *vals = [1, 2, 3, 4, 5]
print('val1:', val1)
print('vals:', vals)
```

```python
val1: 1
vals: [2, 3, 4, 5]
```

### 元类——是什么创建了一个类的新实例？

提到从类实例化一个新对象时，我们通常想到的是 `__init__` 方法。然而，真正在 `__init__()` 被调用之前创建并返回新实例的，是静态方法 `__new__`（它不是类方法！）。
更具体地说，它返回的是这个：  
`return super(<currentclass>, cls).__new__(subcls, *args, **kwargs)`

关于 `__new__` 方法的更多信息，请参阅[文档](https://www.python.org/download/releases/2.2/descrintro/#__new__))。

做个小实验：让我们动点手脚，让 `__new__` 返回 `None`，看看 `__init__` 还会不会被执行：

```python
class a_class(object):
    def __new__(clss, *args, **kwargs):
        print('excecuted __new__')
        return None
    def __init__(self, an_arg):
        print('excecuted __init__')
        self.an_arg = an_arg

a_object = a_class(1)
print('Type of a_object:', type(a_object))
```

```python
excecuted __new__
Type of a_object: <class 'NoneType'>
```

正如上面的代码所示，`__init__` 需要 `__new__` 返回的实例才能被调用。所以，我们这里只是创建了一个 `NoneType` 对象。  
现在让我们重写 `__new__`，确认这次 `__init__` 会被调用来实例化新对象"：

```python
class a_class(object):
    def __new__(cls, *args, **kwargs):
        print('excecuted __new__')
        inst = super(a_class, cls).__new__(cls)
        return inst
    def __init__(self, an_arg):
        print('excecuted __init__')
        self.an_arg = an_arg

a_object = a_class(1)
print('Type of a_object:', type(a_object))
print('a_object.an_arg: ', a_object.an_arg)
```

```python
excecuted __new__
excecuted __init__
Type of a_object: <class '__main__.a_class'>
a_object.an_arg:  1
```

```python
for i in range(5):
    if i == 1:
        print('in for')
else:
    print('in else')
print('after for-loop')
```

```python
in for
in else
after for-loop
```

```python
for i in range(5):
    if i == 1:
        break
else:
    print('in else')
print('after for-loop')
```

```python
after for-loop
```

### else 子句：「条件型 else」与「完成型 else」

我敢说，条件型的「else」是每个程序员的日常必修课。然而，Python 中还有第二种风味的「else」子句，我把它称作「完成型 else（completion else）」（原因稍后自明）。  
不过首先，让我们来看看大家都熟悉的那个「传统」条件型 else。

#### 条件型 else：

```python
# conditional else

a_list = [1,2]
if a_list[0] == 1:
    print('Hello, World!')
else:
    print('Bye, World!')
```

```python
Hello, World!
```

```python
# conditional else

a_list = [1,2]
if a_list[0] == 2:
    print('Hello, World!')
else:
    print('Bye, World!')
```

```python
Bye, World!
```

为什么我要展示这些简单的例子？我认为它们很适合凸显几个关键点：执行的**要么**是 `if` 子句下的代码，**要么**是 `else` 块下的代码，二者不可兼得。  
如果 `if` 子句的条件求值为 `True`，就执行 `if` 块；如果求值为 `False`，执行的就是 `else` 块。

#### 完成型 else

与我们在条件型 `else` 中熟悉的**非此即彼**\*情形**不同**，完成型 `else` 是在一个代码块执行完毕之后才执行的。  
为了给大家举个例子，让我们把 `else` 用于错误处理：

##### 完成型 else（try-except）

```python
try:
    print('first element:', a_list[0])
except IndexError:
    print('raised IndexError')
else:
    print('no error in try-block')
```

```python
first element: 1
no error in try-block
```

```python
try:
    print('third element:', a_list[2])
except IndexError:
    print('raised IndexError')
else:
    print('no error in try-block')
```

```python
raised IndexError
```

在上面的代码中可以看到，**`else` 子句下的代码只有在 `try` 块执行过程中没有遇到任何错误时才会被执行，也就是说，只有 `try` 块被「完整」执行时才行。**  
同样的规则也适用于 while 循环和 for 循环中的「完成型」 `else`，你可以在下面的示例中验证。

##### 完成型 else（while 循环）

```python
i = 0
while i < 2:
    print(i)
    i += 1
else:
    print('in else')
```

```python
0
1
in else
```

```python
i = 0
while i < 2:
    print(i)
    i += 1
    break
else:
    print('completed while-loop')
```

```python
0
```

##### 完成型 else（for 循环）

```python
for i in range(2):
    print(i)
else:
    print('completed for-loop')
```

```python
0
1
completed for-loop
```

```python
for i in range(2):
    print(i)
    break
else:
    print('completed for-loop')
```

```python
0
```

### 编译时常量与运行时表达式的驻留（interning）

这可能没什么特别的用处，但仍然很有意思：Python 解释器会对编译时常量做驻留（interning），但不会对运行时表达式这么做（注意，这是与具体实现相关的）。

（原始来源：[Stackoverflow](http://stackoverflow.com/questions/15541404/python-string-interning)）

来看看下面这个简单的例子。我们创建 3 个变量，以不同的方式给它们赋值 "Hello"，然后测试它们的同一性。

```python
hello1 = 'Hello'

hello2 = 'Hell' + 'o'

hello3 = 'Hell'
hello3 = hello3 + 'o'

print('hello1 is hello2:', hello1 is hello2)
print('hello1 is hello3:', hello1 is hello3)
```

```python
hello1 is hello2: True
hello1 is hello3: False
```

那么，为什么第一个表达式求值为真，第二个却不是呢？要回答这个问题，我们需要仔细看看底层的字节码：

```python
import dis
def hello1_func():
    s = 'Hello'
    return s
dis.dis(hello1_func)
```

```python
  3           0 LOAD_CONST               1 ('Hello')
              3 STORE_FAST               0 (s)

  4           6 LOAD_FAST                0 (s)
              9 RETURN_VALUE
```

```python
def hello2_func():
    s = 'Hell' + 'o'
    return s
dis.dis(hello2_func)
```

```python
  2           0 LOAD_CONST               3 ('Hello')
              3 STORE_FAST               0 (s)

  3           6 LOAD_FAST                0 (s)
              9 RETURN_VALUE
```

```python
def hello3_func():
    s = 'Hell'
    s = s + 'o'
    return s
dis.dis(hello3_func)
```

```python
  2           0 LOAD_CONST               1 ('Hell')
              3 STORE_FAST               0 (s)

  3           6 LOAD_FAST                0 (s)
              9 LOAD_CONST               2 ('o')
             12 BINARY_ADD
             13 STORE_FAST               0 (s)

  4          16 LOAD_FAST                0 (s)
             19 RETURN_VALUE
```

看起来 `'Hello'` 和 `'Hell'` + `'o'` 都在编译时被求值并以 `'Hello'` 的形式存储了，而第三种写法   
`s = 'Hell'`  
`s = s + 'o'` 似乎没有被驻留。让我们用下面的代码快速确认这一行为：

```python
print(hello1_func() is hello2_func())
print(hello1_func() is hello3_func())
```

```python
True
False
```

最后，为了证明这个假说正是这个相当出人意料的观察结果背后的答案，让我们手动对该值做 `intern`：

```python
import sys

print(hello1_func() is sys.intern(hello3_func()))
```

```python
True
```
