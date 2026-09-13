---
title: "【备忘】Python中断多重循环的几种思路"
date: "2016-12-19"
author: "苏剑林"
category: "信息时代"
tags: ["python", "备忘"]
url: "https://kexue.fm/archives/4159"
blog: "科学空间 | Scientific Spaces"
---

## 跳出单循环
不管是什么编程语言，都有可能会有跳出循环的需求，比如枚举时，找到一个满足条件的数就终止。跳出单循环是很简单的，比如

```
for i in range(10):
    if i > 5:
        print i
        break
```

然而，我们有时候会需要跳出多重循环，而break只能够跳出一层循环，比如

```
for i in range(10):
    for j in range(10):
        if i+j > 5:
            print i,j
            break
```

这样的代码并非说找到一组i+j > 5就停止，而是连续找到10组，因为break只跳出了for j in range(10)这一重循环。那么，怎么才能跳出多重呢？在此记录备忘一下。

## 跳出多重循环
事实上，Python的标准语法是不支持跳出多重循环的，所以只能利用一些技巧，大概的思路有：写成函数、利用笛卡尔积、利用调试。

### 写成函数
在Python中，函数运行到return这一句就会停止，因此可以利用这一特性，将功能写成函数，终止多重循环，例如

```
def work():
    for i in range(10):
        for j in range(10):
            if i+j > 5:
                return i,j

print work()
```

### 利用笛卡尔积
这种方法的思路就是，既然可以跳出单循环，我就将多重循环改写为单循环，这可以利用itertools中的笛卡尔积函数product，例如

```
from itertools import product

for i,j in product(range(10), range(10)):
    if i+j > 5:
        print i,j
        break
```

### 利用调试模式
笛卡尔积的方式很巧妙，也很简洁，但它只能用于每次循环的集合都是独立的情形，假如每层循环都与前一层紧密相关，就不能用这种技巧了。这时候可以用第一种方法，将它写成函数，另外，还可以利用调试模式。这个利用了调试模式中，只要出现报错就退出的原理，它伪装了一个错误出来。

```
class Found(Exception):
    pass

try:
    for i in range(10):
        for j in range(i): #第二重循环跟第一重有关
            if i + j > 5:
                raise Found
except Found:
    print i, j
```
