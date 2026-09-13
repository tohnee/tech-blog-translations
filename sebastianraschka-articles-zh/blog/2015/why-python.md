---
title: "Python、机器学习与语言之战"
title_en: "Python, ML, and Language Wars"
source: https://sebastianraschka.com/blog/2015/why-python.html
crawled: 2026-09-06
translated: 2026-09-06
---

# Python、机器学习与语言之战

> 原文：[Python, ML, and Language Wars](https://sebastianraschka.com/blog/2015/why-python.html)

天哪，又一篇主观到极点、观点鲜明的标题党文章？没错！那我为什么要费劲写这个呢？好吧，先分享一条我从前教授那里听来的、看似琐碎却改变人生的洞见和处世智慧——从那以后它就成了我的座右铭："如果一件事你要做超过 3 次，那就写个脚本把它自动化。"

看到这里，你可能已经开始对这篇博客感到疑惑：我足足半年没写什么东西了！好吧，撇开[在社交平台上发的碎碎念](https://twitter.com/rasbt)不谈，这话并不准确：我其实写了[点东西](https://github.com/rasbt/python-machine-learning-book)——精确地说，大约 400 页。最近这段时间对我而言真是一段不小的旅程。至于那个常被问起的问题"你为什么选择 Python 来做机器学习？"，我想是时候写下*我的脚本*了。

在接下来的段落里，我真的不打算告诉你为什么*你*或者其他任何人应该使用 Python。说实话，我很讨厌这类问题："哪个 \* 最好？"（\* 这里可以填入"编程语言、文本编辑器、IDE、操作系统、电脑厂商"）。这确实是个无聊的问题和讨论。不过有时候它也能带来乐趣，我的建议是把这类问题留到下班后偶尔和同事朋友喝啤酒、喝咖啡的时候聊。

## 复杂问题的简短回答

也许我应该从简短的回答开始。从这一段往下，你可以随时停止阅读，因为它已经切中要害。我是一名科学家，我喜欢把事情做完。我喜欢一个能让我快速做原型、随手记下模型和想法的环境。我需要解决的是非常具体的问题。我分析给定的数据集，从中得出结论。对我而言最重要的是：我怎样才能最高效地完成工作？我说的"高效"是什么意思？我通常只运行一次分析（测试不同想法和调试除外）；我不需要 7×24 小时反复运行某段代码，我不是在为最终用户开发软件应用或 Web 应用。当我*量化*"效率"时，我实际上估算的是三件事的总和：（1）把想法写成代码所需的时间，（2）调试所需的时间，（3）运行所需的时间。对我来说，"最高效"就意味着"拿到结果需要多久？"这些年下来，我发现 Python 适合我。不是永远，但大多数时候是。就像生活中的其他一切一样，Python 不是"银弹"，不是所有问题的"最佳"解决方案。然而，如果把各种编程语言放在从常见到不那么常见的问题任务这个全谱系上来比较，Python 已经相当接近了——它可能是最多才多艺、最有能力的全能选手。

![为什么选择 Python：一般性问题](https://sebastianraschka.com/images/blog/2015/why-python/the_general_problem.png)

（来源：<https://xkcd.com/974/>）

记住："过早的优化是万恶之源"（Donald Knuth）。如果你属于软件工程团队，要为公司的机器学习和数据科学部门优化下一个改变游戏规则的高频交易模型，那 Python 可能不适合你（不过也许数据科学团队选用的正是 Python，所以学会读懂它或许仍然有用）。所以，我的一点小建议是：在选择语言时，评估你日常面对的问题任务和需求。"当你手里只有一把锤子，一切看起来都像钉子"——你足够聪明，不会掉进这个陷阱！不过请记住，凡事讲究平衡。有些场合，即便螺丝刀可能是更"优雅"的方案，锤子也照样是最佳选择。说到底，还是要看效率。[⇧](#table-of-contents)

**让我举一个来自亲身经历的例子。**
我需要开发一批新算法，围绕一个非常具体的问题假设，对 1500 万个小分子化合物进行"筛选"。我是完全做计算的，但我的合作者是做非计算实验的生物学家（我们称之为"湿实验"）。目标是把化合物缩小到一份包含 100 个候选化合物的清单，供他们在实验室测试。麻烦在于，他们急需结果，因为他们可用于实验的时间有限。相信我，时间真的很"有限"：就在必须收集结果的几周前，我们的基金申请才刚获批、研究才刚拿到经费（合作者的实验对象是某种鱼类的幼体，而这种鱼只在春季产卵）。于是我开始思考："我怎样才能尽快把结果交给他们？"我懂 C++ 和 FORTRAN，如果用这些语言实现那些算法，运行"筛选"过程可能确实比 Python 快。但这更多是有依据的猜测，我并不确定是否真的会快多少。不过有一点我很确定：如果用 Python 开发，几天之内就能跑起来——而对应的 C++ 版本可能要一周才能写完。更高效的实现以后再说。当时最重要的是尽快把结果交给合作者——"过早的优化是万恶之源"。顺带一提：同样的思路也适用于数据存储方案。这里我直接选了 SQLite。CSV 不太合理，因为我需要反复标注和检索特定分子。我肯定不想每次查询某个分子或修改其条目时，都从头到尾扫描或重写一遍 CSV——这还没算上内存容量处理方面的麻烦。也许 MySQL 会更好，但出于上述原因，我想尽快把活干完，再额外搭一个 SQL 服务器……没那个时间，SQLite 完全够用了。

![为什么选择 Python：自动化](https://sebastianraschka.com/images/blog/2015/why-python/automation.png)

（来源：<https://xkcd.com/1319/>）

结论：**选择能满足*你*的需求的语言！**
不过这里有一个小提醒！一个初学者在学习一门语言之前，怎么可能了解它的优缺点？又该怎么知道这门语言对自己到底有没有用？我会这样做：直接在 Google 和 [GitHub](https://github.com) 上搜索与你最常见的问题任务相关的应用和解决方案。你不需要读懂代码，只需看看最终成品。另外，别羞于开口问人。不要泛泛地问"哪种编程语言最好"，而要具体一些，描述你的目标以及你想学编程的原因。如果你想为 MacOS X 开发应用，那你大概该去看看 Objective C 和 Swift；如果你想在 Android 上开发，你更感兴趣的可能是学习 Java，诸如此类。[⇧](#table-of-contents)

## 我最喜欢的 Python 工具有哪些？

如果你感兴趣，下面是我最喜欢、使用最频繁的 Python"工具"，其中大多数我每天都在用。

- [NumPy](http://www.numpy.org)：我最喜欢的处理数组结构、利用线性代数将方程向量化的库；由 [SciPy](http://scipy2015.scipy.org/ehome/index.php?eventid=115969&) 补充增强。
- [Theano](https://theano.readthedocs.org/en/latest/)：实现机器学习算法，承担繁重的计算任务，并把计算分发到 GPU 的各个核心上。
- [scikit-learn](http://scikit-learn.org/stable/)：处理日常基础机器学习任务最方便的 API。
- [matplotlib](http://matplotlib.org)：画图时的首选库。有时我也会用 [seaborn](http://stanford.edu/~mwaskom/software/seaborn/index.html) 画特定的图，比如它的热力图就特别棒！

![为什么选择 Python：热力图](https://sebastianraschka.com/images/blog/2015/why-python/heatmap.png)

（来源：<http://stanford.edu/~mwaskom/software/seaborn/examples/structured_heatmap.html>）

- [Flask（Django）](http://flask.pocoo.org)：偶尔我想把一个想法做成 Web 应用，这时 Flask 就非常好用了！
- [SymPy](http://www.sympy.org/en/index.html)：做符号数学，它取代了 WolframAlpha 在我心中的位置。
- [pandas](http://pandas.pydata.org)：处理相对较小的数据集，数据大多来自 CSV 文件。
- [sqlite3](https://docs.python.org/2/library/sqlite3.html)：标注和查询"中等规模"的数据集。
- [IPython notebooks](http://ipython.org)：怎么说呢，我 90% 的研究都是在 IPython notebook 里完成的。它是一个非常棒的环境，所有东西都集中在一处：想法、代码、注释、LaTeX 公式、插图、图示、输出……

![为什么选择 Python：IPython notebook](https://sebastianraschka.com/images/blog/2015/why-python/ipython_notebook.png)

注意，IPython 项目最近演变成了 [Project Jupyter](https://jupyter.org)。现在，Jupyter notebook 环境不仅支持 Python，还支持 R、Julia 以及更多语言。[⇧](#table-of-contents)

## 我怎么看 MATLAB？

几年前我大量使用过 MATLAB（/Octave），大部分计算机科学/数据科学课程都是用 MATLAB 教的。说实话，它真算不上一个糟糕的原型开发环境！由于它从设计之初就面向线性代数（MATLAB 即 MATrix LABoratory 的缩写），在实现机器学习算法时，MATLAB 比 Python/NumPy 感觉更"自然"一些——好吧，公平地说，[从 1 开始索引](https://www.cs.utexas.edu/users/EWD/transcriptions/EWD08xx/EWD831.html)的编程语言在我们程序员眼里确实有点怪。不过要记住，MATLAB 价格不菲，而且我认为它正在学术界和工业界慢慢淡出。再说了，我毕竟是个开源爱好者 ;)。此外，从下面的基准测试来看，与其他"高效率"语言相比，它的性能也不算出众：

![为什么选择 Python：Julia 基准测试](https://sebastianraschka.com/images/blog/2015/why-python/julia_benchmark.png)

（[基准测试](https://sebastianraschka.com/glossary/#benchmark "Benchmark")耗时相对于 C 的倍数——越小越好，C 性能 = 1.0；来源：<http://julialang.org/benchmarks/>）

不过，我们也不应忘记 Python 还有 Theano 这个好用的库。2010 年，Theano 的开发者报告称，代码运行在 CPU 上时，其性能比 NumPy 快 1.8 倍；如果 Theano 以 GPU 为目标，甚至比 NumPy 快 11 倍（J. Bergstra, O. Breuleux, F. Bastien, P. Lamblin, R. Pascanu, G. Desjardins, J. Turian, D. Warde-Farley, and Y. Bengio. Theano: A CPU and GPU math compiler in Python. In Proc. 9th Python in Science Conf, pages 1–7, 2010.）。请注意，这个 Theano 基准测试是 2010 年的数据，这些年 Theano 已有长足进步，现代显卡的能力也一样。

> 我了解到，许多希腊人相信毕达哥拉斯说过"万物皆由数而生"。这一断言本身带来了一个难题：尚不存在的东西，怎么可能被设想为生成万物呢？——克罗顿的 Theano（哲学家，公元前 6 世纪）

PS：如果你不喜欢 NumPy 的 `dot` 方法，那就期待即将到来的 [Python 3.5](https://docs.python.org/3.6/whatsnew/3.5.html) 吧——我们将迎来一个用于矩阵乘法的中缀[运算符](http://legacy.python.org/dev/peps/pep-0465/)，耶！

手工"计算"矩阵乘法（我的意思是，不借助 NumPy 和 BLAS 或 LAPACK）既繁琐又低效。

```python
[[1, 2],     [[5, 6],     [[1 * 5 + 2 * 7, 1 * 6 + 2 * 8],
[3, 4]]  x   [7, 8]]  =   [3 * 5 + 4 * 7, 3 * 6 + 4 * 8]]
```

既然有线性代数和为此专门优化过的库，谁还愿意用嵌套 for 循环来实现这个式子呢！？

```python
>>> X = numpy.array()
>>> W = numpy.array()
>>> X.dot(W)
[[19, 22],
[43, 50]]
```

如果你觉得这个 `dot` 乘积不合胃口，它在 Python 3.5 中是这样写的：

```python
>>> X @ W
[[19, 22],
[43, 50]]
```

老实说，我得承认我对用"@"符号作为矩阵运算符并不算太感冒。不过我为此苦思良久，也没能找到更好且尚未被占用的符号。如果你有更好的想法，请告诉我，我真心好奇！[⇧](#table-of-contents)

## Julia 棒极了……至少在纸面上！

我认为 Julia 是一门伟大的语言，我也很想把它推荐给刚开始学习编程和机器学习的人。但我并不确定是否真的应该这么做。为什么？选择一门编程语言并投入其中，有这样一件令人遗憾、甚至有些悖论的事情。对于 Julia，我们无法判断它未来几年会不会变得足够"流行"。等等，"流行度"和一门编程语言的好坏、实用与否有什么关系？让我告诉你。两难之处在于：最有用的语言未必是设计得最好的，而是流行的那些。为什么？

1. 现成的（大多是免费的）库已经非常丰富，你可以充分利用时间，不必重复造轮子。
2. 在网上更容易找到帮助、教程和示例。
3. 语言本身会不断改进、更新，补丁发布更频繁，让它"更上一层楼"。
4. 更利于协作，团队工作更轻松。
5. 更多人能从你的代码中受益（比如你决定把代码分享到 GitHub 上）。

就我个人而言，我喜欢 Julia 的本色，它完美契合我的兴趣领域。不过我用的是 Python；主要原因是它周围有太多优秀的资源，用起来特别顺手。Python 社区非常棒，我相信它在未来至少 5 到 10 年里仍会蓬勃发展。至于 Julia，我就没那么有把握了。我喜欢它的设计，认为它很出色。然而，如果它不够流行，我就无法判断它是否"经得起未来考验"。万一几年后开发停滞了呢？那我就在一件届时已经"死掉"的东西上做了投资。不过话说回来，如果人人都这么想，任何新语言都永远没有机会。[⇧](#table-of-contents)

## R 其实真的没什么不好

好吧，我猜大家多半知道我曾经是个 R 用户。我甚至为它写过一本书（好吧，准确说是关于[用 R 画热力图](https://www.amazon.com/Instant-Heat-Maps-R-How-/dp/1782165649/ref=sr_1_1?ie=UTF8&qid=1372160113&sr=8-1&keywords=instant+heat+maps+in+r+how-to)的书。注意那是很多年前的事了，`ggplot2` 还没流行起来。实在没什么特别的理由去看它——我指的是那本书。不过如果你实在忍不住，这里有一个免费的、5 分钟就能读完的[精简版](https://sebastianraschka.com/Articles/heatmaps_in_r.html)）。
我承认，这有点跑题了。回到正题：R 有什么问题？我认为它完全没有问题。毕竟，对"数据科学"来说，它相当强大、能干而且"流行"！就在不久前，连 Microsoft 都表现得非常、非常有兴趣：[Microsoft 收购 Revolution Analytics——一家为开源统计计算与预测分析语言 R 提供商业服务的公司](https://www.cio.com/article/246632/microsoft-closes-acquisition-of-r-software-and-services-provider.html)。

那么，我该如何总结对 R 的感受呢？我不太确定下面这句话的出处——很久以前从某个人那里听来的——但它非常恰当地解释了 R 和 Python 的区别："R 是统计学家为统计学家开发的编程语言；Python 则是由计算机科学家开发的，程序员可以用它来应用统计技术。"这句话的部分含义是：R 和 Python 在"数据科学"任务上的能力不相上下，但 Python 的语法让我感觉更自然——这是个人口味问题。

我本来想拿 Theano 和 GPU 计算作为 Python 的一大加分项，但发现 R 在这方面也相当能干：[用 GPU 和 R 做并行编程](http://blog.revolutionanalytics.com/2015/01/parallel-programming-with-gpus-and-r.html)。我知道你接下来想问什么："好吧，那把我的模型变成一个漂亮又 *闪亮*（shiny）的 Web 应用呢？我敢打赌 R 做不到！"抱歉，这赌你输了；看看 [RStudio 的 Shiny——R 的 Web 应用框架](http://www.rstudio.com/shiny/)吧。明白我的意思了吗？这里没有赢家，以后大概也不会有。

借用一句我最喜欢的 Python 名言，跳出它原本的语境："我们都是成年人了"——别把时间浪费在语言战争上。选择那件让你"顺手"的工具。至于就业市场的视角：这里也没有对错之分。我认为，一家想雇你做"数据科学家"的公司，并不会真的在意你偏爱的工具箱——编程语言终究只是"工具"。最重要的技能是像"数据科学家"一样思考，提出正确的问题，有能力解决问题。难的部分是数学和机器学习理论，一门新的编程语言很容易学会。想想看，你已经学会了抡起锤子把钉子砸进去，换一个厂商的锤子又能有多难？
不过，如果你还是感兴趣，可以看看 Tiobe 指数，它是衡量编程语言流行度的*一种*指标：

![为什么选择 Python：TIOBE 指数](https://sebastianraschka.com/images/blog/2015/why-python/tiobe.png)

（来源：<http://www.tiobe.com/index.php/content/paperinfo/tpci/index.html>）

不过，如果我们看看 IEEE Spectrum 的 [2015 年十大编程语言](https://spectrum.ieee.org/the-2015-top-ten-programming-languages)，R 语言正在快速攀升（左栏：2015 年，右栏：2014 年）。

![为什么选择 Python：IEEE Spectrum 排名](https://sebastianraschka.com/images/blog/2015/why-python/spectrum.jpg)

（来源：<https://spectrum.ieee.org/the-2015-top-ten-programming-languages>）

我想你已经明白了。Python 和 R，如今真没什么大差别。而且在两者之间做选择时，你不该为就业机会操心。[⇧](#table-of-contents)

## Perl 怎么了？

Perl 是我职业生涯早期学的第一门语言（当然，高中时学的 Basic、Pascal 和 Delphi 除外）。在德国读本科时，我修过一门 Perl 编程课。那时我真的很喜欢它，不过，当时我也确实没有什么东西可以拿来比较。就我个人所知，身边真正每天用 Perl 写脚本的人寥寥无几。不过我想它在生物信息学领域应该还很常见吧！？总之，这部分就长话短说，让它安息吧：["Perl 死了。Perl 万岁。"](http://archive.oreilly.com/pub/post/perl_is_dead_long_live_perl.html) [⇧](#table-of-contents)

## 其他选择

还有许多其他语言可用于机器学习，例如 [Ruby](https://www.ruby-lang.org)（[Thoughtful Machine Learning: A Test-Driven Approach](https://www.amazon.com/Thoughtful-Machine-Learning-Test-Driven-Approach/dp/1449374069/ref=sr_1_1?ie=UTF8&qid=1440407371&sr=8-1&keywords=machine+learning+ruby)）、[Java](https://www.java.com/en/)（[Java-ML](http://java-ml.sourceforge.net)）、[Scala](http://www.scala-lang.org)（[Breeze](https://github.com/scalanlp/breeze)）、[Lua](http://www.lua.org)（[Torch](http://torch.ch)）等等。不过，除了多年前上过的一门 Java 课，以及 [PySpark](https://spark.apache.org/docs/latest/api/python/index.html)（Spark 的 Python API，Spark 本身用 Scala 编写）之外，我对这些语言实在没什么经验，也说不出什么来。[⇧](#table-of-contents)

## Python 是一门正在消亡的语言吗？

这是个正经问题，最近刚在 Quora 上被提出来，如果你想听听其他精彩观点，可以去看看那个[问题帖](https://www.quora.com/Is-it-true-that-Python-is-a-dying-language)。不过如果你想听我的看法，我的回答是：不，它没有。为什么？好吧，Python 是一门"相对"古老的语言——第一次发布是在 90 年代初（我们可以从 1991 年算起），和每一门编程语言一样，它在设计时不得不做出某些取舍和妥协。每门编程语言都有自己的怪癖，而越新的语言越倾向于吸取过去的教训，这是好事（顺便说一句，R 是在 Python 之后不久发布的：1995 年）。
Python 远非"完美"，和其他语言一样，它也有自己的瑕疵。作为一个核心 Python 用户，我必须说 GIL（全局解释器锁）是最让我恼火的东西——但请注意，Python 有 multiprocessing 和 multithreading 模块，所以这其实算不上真正的限制，只是在某些场景下有点"不方便"。

没有任何指标能够量化一门编程语言"有多好"，这真的取决于你追求什么。你应该问的问题是："我想达成什么目标，哪种工具最能实现它"——"如果你手里只有锤子，一切看起来都像钉子。"
又说回锤子和钉子，Python 用途极其广泛，我日常研究的大部分工作都是通过 Python 完成的：用出色的 scikit-learn 机器学习库，用 pandas 做数据整理，用 matplotlib/seaborn 做可视化，用 IPython notebook 记录所有这些内容。[⇧](#table-of-contents)

## 结论

好吧，对一个看似非常简单的问题，这个回答着实有点长。相信我，这个话题我可以聊上几个小时甚至好几天。但何必把事情搞复杂呢？让我们收个尾：

![为什么选择 Python：Python](https://sebastianraschka.com/images/blog/2015/why-python/python.png)

（来源：<https://xkcd.com/353/>）

感谢阅读。如果你喜欢这些内容，也可以[在 Twitter 上找到我](https://twitter.com/rasbt)，我在那里分享更多有用的内容。

## 反馈与观点

关于这篇文章我收到了很多很棒的反馈，想在这里分享给大家。请记住，"建议"天生就带有偏见；你可能已经注意到，我的偏见几乎完全偏向 Python——抱歉，但我就是这样的人！我相信听听其他人的想法也许会有帮助！尤其当你刚进入"数据科学"、机器学习和编程领域时。话虽如此，请往下看看这些信息量很大的评论吧！[⇧](#table-of-contents)

### Python

- rm999 在 [hackernews](https://news.ycombinator.com/item?id=10113413) 上说：

> 大约一年前，我把主力工具从 R 换成了 Python，用来串联我的整个数据流水线（从数据源一直到生产模型和前端/可视化）。这并没有真正影响我能做的事或我的效率，只是多了一层使用任何新语言头几年都免不了的额外搜索。我选 Python 的主要原因纯粹出于实际考虑：它是一门团队之外的人也会尊重并愿意接手的语言。这让我能以多种方式更轻松地协作：与其他团队共享工具、移交代码所有权、在需要时获得帮助等等。在某些公司，数据科学有个名声，就是"胡乱拼凑个东西，然后甩过墙去让别人收拾"。以我的经验，R 只会加剧这种名声。这挺可惜的，它在自己擅长的领域真的很出色。

- DrNuke 在 [hackernews](https://news.ycombinator.com/item?id=10113413) 上说：

> 我很喜欢这篇文章中这种"黑客式"的态度：工具只是用来做有价值的事情的工具，而不是目的本身。如今，由于数据科学的爆发式发展和快速与非专业人士互动的需求，Python 生态正是合时宜的正确工具。

- zzleeper 在 [hackernews](https://news.ycombinator.com/item?id=10113413) 上说：

> 相当有意思的文章。我觉得很多搞数值计算的 Pythonista 都处在同样的境地：他们对大多数语言都能接受，但觉得 R 的语法有点不自然，Matlab 一旦超出纯矩阵运算就显得不够用，而大家都在观望 Julia 能否崛起（至少在我看来的确如此）

- JanneJM 在 [reddit](https://www.reddit.com/r/MachineLearning/comments/3ibx9j/python_machine_learning_and_language_wars_a/) 上说：

> 关键在于要有足够多高质量的库。我认识的很多人——包括我自己——其实并不是真的对 Python 本身感兴趣。我们用的是 Numpy、Scipy、Matplotlib、Pandas 等等等等，Python 只是搭了个顺风车。如果这些库当年是给 Ruby、Perl 或 Lua 写的，那我们今天用的就是它们了。

### Perl

- leni536 在 [hackernews](https://news.ycombinator.com/item?id=10113413) 上说

> "不过我想 Perl 在生物信息学领域应该还很常见吧！？"这没错——生物信息学的许多日常任务多多少少都是纯文本解析 [1]，而 Perl 擅长解析文本和快速使用正则表达式。我们这一代做数据清洗和分析的生物信息学家（20–30 岁）用 Python，有时是因为画图更好看、语言更容易上手、大学里教得更多，或者其他原因——比我们年长的人通常用 P

### R

- geomark 在 [hackernews](https://news.ycombinator.com/item?id=10113413) 上说

> 我刚完成 Coursera 的数据科学专项课程，从一个彻底的 R 新手变成了至少还算熟练的用户。由于之前用 Python 写过不少 Web 程序，我起初不喜欢 R，只认可它在统计编程方面的强大。但后来我发现了一些非常出色的 R 包，让我在做那些原本会求助于 Python 的事情时也乐在其中。比如我最近发现了用于网页抓取的 rvest 包。R 的数据可视化看起来远胜一筹，除非是我对 Python 了解不够（很可能如此）。而且用 shiny 或 RStudio Presenter 搭一个漂亮的统计应用也很容易。但 R 真的没法扩展到大型生产级应用，对吧？所以我觉得我得继续同时使用 Python 和 R。补充：Lofkin，这份清单很棒，谢谢。另外，文章里说 Python 语法感觉更自然，我也有同感。但后来我开始用 R 里的 magrittr 和 dplyr 包，它们带来了管道这种好东西，那种感觉就开始消退了。

- Adam\_O 在 [hackernews](https://news.ycombinator.com/item?id=10113413) 上说

> 从学生的角度看，大多数优质的在线分析/数据分析/统计课程都用 R，所以在学习这些内容时很难绕开它。一旦掌握了基本概念，切换到 Python 应该不难。不过我想大多数人在可视化方面仍然偏爱 ggplot2。每当我使用 R，我都感觉自己像个统计学家，能感受到这门语言散发出的那种"冷峻的严谨"。但归根结底，我认为同时驾驭两门语言是有优势的。

### MATLAB/Octave

- sampo 在 [hackernews](https://news.ycombinator.com/item?id=10113413) 上说

> Andrew Ng 在 Coursera 机器学习课上说过，根据他的经验，学生用 Octave/Matlab 完成课程作业比用 Python 更快。不过没错，那门课的重点是实现并摆弄小型数值算法，而上面链接的博客讲的是一个主要从 Python 调用现成机器学习库的人。

- misiti3780 在 [hackernews](https://news.ycombinator.com/item?id=10113413) 上说

> Octave/Matlab 很"棒"，但你想把它们集成进生产级 Web 应用？祝你好运。既然确实做不到——那就别用它们，除非你愿意把同一个算法实现两遍。Matlab 的授权要花钱，工具箱还要额外花钱。R 有用是因为它历史悠久、资源丰富，统计社区里有很大一部分人在用。它还有很多尚未被移植到其他语言的有用库（ggmap！！！）。但你仍然会遇到同样的问题：没法把 R 集成进生产级 Web 应用。而且我很确定 Hadoop streaming 也不支持 R、Octave 或 Matlab

- thanatropism 在 [hackernews](https://news.ycombinator.com/item?id=10113413) 上说

> 这里漏了一件事：Matlab 的语法其实和现代 Fortran 非常接近。至少有两次，我都是在改写 Matlab 代码的基础上写出 Fortran 代码的（用于蒙特卡洛模拟；不同场景），只需加上类型、增加一些常规的冗长声明、修正 do 循环的语法等等。

### Julia

- Lofkin 在 [hackernews](https://news.ycombinator.com/item?id=10113413) 上说：

> 就我个人而言，我很想切换到 Julia，但高阶函数速度慢、核心数据基础设施变动频繁、再加上没有 PyMC 3，这些都让我在 pydata 阵营再待一阵子。好在有 numba 帮我过渡。

- Buttons 840 在 [hackernews](https://news.ycombinator.com/item?id=10113413) 上说：

> 我专业使用 Python 已经 8 年，它是我最喜欢的语言。numpy 和 scikit-learn 我也用过一些。话虽如此，我最近真的很享受学习 Julia 的过程。它易于学习，而且性能确实出色（也就是说：很快）。事实上，我觉得学 Julia 的工作量和学 numba 之类的东西差不多，而性能相当（有人说还略好一些？）。

- idunning 在 [hackernews](https://news.ycombinator.com/item?id=10113413) 上说：

> 作为一个日常工作和业余项目几乎全用 Julia 的人，我认为作者关于 Julia 的看法大部分是正确的。我觉得这门语言很棒，使用它让我的生活更美好。在我看来，有一些包确实比其他语言中的任何同类都好。另一方面，我对不完美之处的容忍度也比较高，我能自己摸索解决问题（幸运的是我也有时间这么做），而且如果某样东西还不存在，我也愿意自己写出来（在合理范围内）。当然，大多数人不具备这些条件，这没关系。作者不愿冒 Julia 可能无法"存活"的风险，这合情合理。它确实还不完善，但正在朝那个方向前进。不过我有信心它会存活下来（并且蓬勃发展），继续壮大这个已经相当可观的社区。我有一种预感，作者迟早——大概几年之后——会找到通往 Julia 世界的路。

- niksko 在 [reddit](https://www.reddit.com/r/Python/comments/3i8crj/python_machine_learning_and_language_wars_a/) 上说：

> 关于 Julia 我同意。它的潜力真的很大，而且基本上就是为这类应用量身定做的，但社区和支持还没跟上。我花了一个学期做一个计算进化动力学领域的小型研究项目，其中最繁琐、最困难的部分就是让 Julia 画出我想要的图。而且当时它还不支持 docstring :/。它很快、很炫，但还不够成熟。

- KG7ULQ 在 [reddit](https://www.reddit.com/r/MachineLearning/comments/3ibx9j/python_machine_learning_and_language_wars_a/) 上说：

> 我上完 Coursera 上 Ng 的机器学习课后四处打听，看起来主流选择是用 Python……但包括你提到的那几个在内，有好几个大型库都得学。后来我看了 Julia，心想不如学它，毕竟它内置了所有线性代数和 SIMD 相关的东西，性能也更好。它看上去确实是机器学习的"甜蜜点"语言。

### 其他语言（我忘了提到的）

- leni536 在 [hackernews](https://news.ycombinator.com/item?id=10113413) 上说：

> 还有，C++ 也没什么不好。做线性代数我用 armadillo 库，它是 LAPACK 和 BLAS 的一层很好的封装（而且很快！）。不知为什么，科学家们有点害怕 C++。也不知为什么，大家就"必须"先用一门"更容易"的语言做原型。当然，和解释型语言不同，你不能拿 C++ 当计算器用，但我见过有人被困在原型语言里做计算，最终也没把它搬到更快的平台上。我的意思是：用 C++ 做科学计算并不难。

- WallyMetropolis 在 [reddit](https://www.reddit.com/r/Python/comments/3i8crj/python_machine_learning_and_language_wars_a/) 上说：

> 如果有什么东西能取代 Python，Scala 看起来是最有可能的候选。我认为函数式语言很适合数学味浓的工作，而且它跑在 JVM 上，原型可以不怎么费力地变成能在"任何地方"运行的生产代码。Spark 是 Scala 的杀手级应用。现在我可以从原型直接走到在任意规模的数据集上运行，中间没有太多障碍。

- rpcope1 在 [reddit](https://www.reddit.com/r/Python/comments/3i8crj/python_machine_learning_and_language_wars_a/) 上说：

> [Scala] 编译可能很慢，但它比 CPython 更安全、快得多（撇开不编译成字节码的代码和对 C/Fortran 库的调用不谈），而且它有不少概念是我在 Python 里非常怀念的，比如 Option[T]、implicit 修饰符、像样的 map/reduce/filter、像样的 lambda 等等。
