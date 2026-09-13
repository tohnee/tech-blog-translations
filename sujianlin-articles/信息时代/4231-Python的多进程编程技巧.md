---
title: "Python的多进程编程技巧"
date: "2017-02-19"
author: "苏剑林"
category: "信息时代"
tags: ["编程", "python"]
url: "https://kexue.fm/archives/4231"
blog: "科学空间 | Scientific Spaces"
---

## 过程
在Python中，如果要多进程运算，一般是通过multiprocessing来实现的，常用的是multiprocessing中的进程池，比如：

```
from multiprocessing import Pool
import time

def f(x):
    time.sleep(1)
    print x+1
    return x+1

a = range(10)
pool = Pool(4)
b = pool.map(f, a)
pool.close()
pool.join()

print b

```

这样写简明清晰，确实方便，有趣的是，只需要将multiprocessing换成multiprocessing.dummy，就可以将程序从多进程改为多线程了。

## 对象
Python是一个面向对象的编程语言，很多时候我们会将一些程序封装为一个类。但是在类中，以上方法就不好使了。比如

```
from multiprocessing import Pool
import time

class test:
    def __init__(self):
        self.a = range(10)
    def run(self):
        def f(x):
            time.sleep(1)
            print x+1
            return x+1
        pool = Pool(4)
        self.b = pool.map(f, self.a)
        pool.close()
        pool.join()

t = test()
t.run()
print t.b

```

看上去很自然的代码，运行报错：

> cPickle.PicklingError: Can't pickle : attribute lookup __builtin__.function failed

但如果将multiprocessing换成multiprocessing.dummy，就不会报错。说白了，这还是因为多进程之前变量无法共享的问题，而多线程之间同处于一个进程，自然不会有这个问题。

## 临摹
为了研究对象中的多进程编程，笔者做了不少尝试。后来想到，gensim中的不少模块都是支持并行的，可以模仿一下。果不其然，我找到了[ldamulticore.py](https://github.com/RaRe-Technologies/gensim/blob/develop/gensim/models/ldamulticore.py)，经过与网上资料反复对比学习之后，总结出一种比较简明、方便而又通用的写法。

同大多数多进程编程一样，为了在进程之间通信，需要建立Queue对象，不同的是，网上一般的教程是通过multiprocessing的Process函数结合循环语句，来启动多进程，而用Pool是失败的（除非用multiprocessing.Manager.Queue，参考[这篇文章](https://my.oschina.net/yangyanxing/blog/296052)），而gensim使用了Pool的一个技巧，还是可以通过Pool来直接启动多进程，果然高手的作品就是不一样。参考代码如下

```
from multiprocessing import Pool,Queue
import time

class test:
    def __init__(self):
        self.a = range(10)
    def run(self):
        in_queue, out_queue = Queue(), Queue()
        for i in self.a:
            in_queue.put(i)
        def f(in_queue, out_queue):
            while not in_queue.empty():
                time.sleep(1)
                out_queue.put(in_queue.get()+1)
        pool = Pool(4, f, (in_queue, out_queue))
        self.b = []
        while len(self.b) < len(self.a):
            if not out_queue.empty():
                t = out_queue.get()
                print t
                self.b.append(t)
        pool.terminate()

t = test()
t.run()
print t.b
```

总的来说，就是建立两个Queue，一个负责队列任务，一个负责取出结果。比较神奇的是，Pool居然还有第二、第三个参数！具体说明请看[官方文档](https://docs.python.org/2/library/multiprocessing.html#module-multiprocessing.pool)，即Pool的初始化函数，它也是自动并行运行的。

注意运行pool = Pool(4, f, (in_queue, out_queue))这句之后，多进程启动，但不会等待进程运行完，而是立马就运行下面的语句，这时可以像前面那样，用pool.close()和pool.join()让进程完成后再运行后面的语句，而这里使用的方案是直接执行取结果的语句，然后通过这个过程判断进程是否执行完，执行完就通过pool.terminate()关闭进程池。这种写法基本是通用的。
