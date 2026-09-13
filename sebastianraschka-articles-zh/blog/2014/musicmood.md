---
title: "MusicMood"
title_en: "MusicMood"
source: https://sebastianraschka.com/blog/2014/musicmood.html
crawled: 2026-09-06
translated: 2026-09-06
---

# MusicMood

> 原文：[MusicMood](https://sebastianraschka.com/blog/2014/musicmood.html)

在本文中，我想分享我近期一个数据挖掘项目的经验，这大概是我迄今为止最喜欢的业余项目之一。这个项目的核心是构建一个分类模型，能够根据歌曲歌词自动预测音乐的情绪。

## 相关链接

- [试用 MusicMood 网页应用](https://web.archive.org/web/20150118001933/http://rasbt.pythonanywhere.com/)
- [前往 MusicMood GitHub 仓库](https://github.com/rasbt/musicmood)
- [在 SpeakerDeck 上查看项目演示](https://speakerdeck.com/rasbt/musicmood-machine-learning-in-automatic-music-mood-prediction-based-on-song-lyrics)
- [arXiv 上更详细的技术报告](https://arxiv.org/abs/1611.00138)

## 目录

## 关于本项目

这个项目的目标是构建一个分类器，将歌曲划分为*快乐*（happy）和*悲伤*（sad）两类。作为我上一篇文章[《朴素贝叶斯与文本分类（一）——引言与理论》](https://sebastianraschka.com/Articles/2014_naive_bayes_1.html)的后续，我想只基于歌曲歌词来构建这样一个分类模型——更详细的技术报告可以在[这里](https://arxiv.org/abs/1611.00138)找到。

数据收集、预处理和模型训练全部用 Python 完成，使用了 [Pandas](http://pandas.pydata.org)、[scikit-learn](http://scikit-learn.org/stable/)、[h5py](http://www.h5py.org) 和 [Natural Language Toolkit](http://www.nltk.org)（自然语言工具包）——整个过程非常顺畅丝滑，直到我尝试部署由 [Flask](https://flask.palletsprojects.com/en/stable/) 驱动的网页应用时才遇到波折，这个稍后会[谈到](#webapp)。

希望能对他人有所帮助，我把所有数据和代码上传到了一个[公开的 GitHub 仓库](https://github.com/rasbt/musicmood)，并且希望我写的描述性注释足以勾勒出整个工作流程。

### 我为什么对这个项目感兴趣

我一直对"数据科学"领域怀有极大的热情，这也是我最终选择攻读计算生物学博士、研究蛋白质结构建模与分析的原因之一。大约一年前，我有幸修读了一门关于统计模式识别研究的精彩课程，让我深深着迷。由于我非常喜欢音乐（尤其是经典摇滚），而且一直想尝试一下 Python 的 Web 框架，这一切就突然串联了起来。

## 数据收集与探索性分析

在为这个项目头脑风暴时，我并不知道是否有可以免费使用的数据集。我很快找到了一些相关项目的文献，作者们使用了人工标注的数据集来做情绪预测。不过我找不到下载这些数据集的渠道，而且这些数据集的情绪标签数量在我看来也太多了，我担心这会对预测性能产生负面影响。在这个项目中，我只想关注*快乐*和*悲伤*这两个类别，因为我认为仅基于歌词的二分类对文本分析的机器学习算法来说可能已经足够具有挑战性了。

### Million Song Dataset 与歌词

接着，我偶然发现了 [Million Song Dataset](http://labrosa.ee.columbia.edu/millionsong/)，我觉得它相当有意思。还有一个相关的 [musiXmatch](https://www.musixmatch.com) 目录，为 Million Song Dataset 提供歌词。然而，musiXmatch 中的歌词已经过预处理，而我的计划恰恰是要比较不同的预处理技术。另外我也觉得，自己动手构建一个带情绪标签的歌词数据集本身就是一次很好的练习。于是我写了一些简单的脚本，从 [LyricsWiki](http://lyrics.wikia.com/Lyrics_Wiki) 下载歌词，过滤掉没有歌词的歌曲，并使用 Python 的 [Natural Language Toolkit](http://www.nltk.org) 自动剔除了非英文歌曲。

### 情绪标签——从哪里来？

到这一步还比较顺利，我已经收集了一批歌曲及其歌词，下一个任务是获取情绪标签。第一次尝试时，我从 [Last.fm](http://www.last.fm/home) 下载了用户提供的标签，但很快发现，像 *happy* 和 *sad*（以及其他相关形容词）这样的标签只覆盖了很小一部分歌曲，而且由于标签不完整或脱离上下文，彼此之间非常非常矛盾。于是，我决定采用笨办法：手工标注 1200 首歌的子集，其中 1000 首作为训练集，200 首作为验证集。毫无疑问，把音乐与某种特定情绪关联起来本身是一件比较主观的事，如果标签只由一个人提供，更是无可争辩地引入了另一种偏差。不过，我会在后面的 [Webapp](#webapp) 一节中解释我打算如何扩充数据集以及如何处理这种偏差。

### 标注数据其实也可以很有趣

最终，我一边阅读歌词一边听完了这 1200 首歌。当然，这听起来非常枯燥，但我必须说，我也从中获得了乐趣，因为在这个过程中我发现了很多好听又有趣的歌！我使用以下准则来分配*快乐*和*悲伤*的情绪标签：如果歌曲带有比较黑暗的主题，例如暴力、战争、杀戮等（不幸的是符合这些条件的歌还不少），我就把它标为*悲伤*。同样，如果歌手看起来在为某事懊恼或抱怨，或者歌曲是关于"逝去的爱"的，我也会把它标为*悲伤*。其余的基本上都标为*快乐*。

### 满足好奇心的探索性可视化

在完成 1000 首歌训练集的标注后，我实在按捺不住想做些探索性分析，于是绘制了历年快乐歌曲和悲伤歌曲的数量曲线。我发现结果非常有意思：尽管 Million Song Dataset 在发行年代上明显偏向近年的作品，但似乎存在一种趋势：遗憾的是，音乐似乎年复一年地变得越来越悲伤了。

![Musicmood exploratory 1](https://sebastianraschka.com/images/blog/2014/musicmood/exploratory_1.webp)

## 模型选择与训练

### 为什么选择朴素贝叶斯？

正如我在引言中提到的，我在这个项目中聚焦朴素贝叶斯分类的原因之一，是想为之前的[《朴素贝叶斯与文本分类（一）——引言与理论》](https://sebastianraschka.com/Articles/2014_naive_bayes_1.html)一文找一个实际应用场景。此外，由于我还打算做一个小型网页应用，我需要一个计算高效的分类器。朴素贝叶斯模型的优点之一是，它们在批量学习模式下训练起来相当高效，同时也非常适合在线学习（即当新的带标签数据到来时即时更新）。顺便说一句，在文本分类的场景下，朴素贝叶斯分类器的预测性能其实并不差。研究表明，朴素贝叶斯模型在小样本条件下往往表现良好 [1]，并且已被成功用于类似的二分类文本任务，例如电子邮件垃圾邮件检测 [2]。其他实证研究也表明，朴素贝叶斯分类器在文本分类上的性能可与支持向量机相媲美 [3][4]。

[1] P. Domingos and M. Pazzani. [On the optimality of the simple
bayesian classifier under zero-one
loss](http://link.springer.com/article/10.1023%2FA%3A1007413511361).
Machine learning, 29(2-3):103–130, 1997.  
[2] M. Sahami, S. Dumais, D. Heckerman, and E. Horvitz. [A bayesian
approach to filtering junk
e-mail](http://research.microsoft.com/en-us/um/people/horvitz/junkfilter.htm).
In Learning for Text Categorization: Papers from the 1998 workshop,
volume 62, pages 98–105, 1998.  
[3] S. Hassan, M. Rafi, and M. S. Shaikh. [Comparing svm and naive
bayes classifiers for text categorization with wikitology as knowledge
enrichment](https://ieeexplore.ieee.org/document/6151495).
In Multitopic Conference (INMIC), 2011 IEEE 14th International, pages
31–34. IEEE, 2011.  
[4] A. Go, R. Bhayani, and L. Huang. [Twitter sentiment
classification using distant supervision. CS224N Project
Report](http://cs.stanford.edu/people/alecmgo/papers/TwitterDistantSupervision09.pdf),
Stanford, pages 1–12, 2009.

### 网格搜索与最终模型

我要特别称赞 scikit-learn 中出色的 [GridSearch](http://scikit-learn.org/stable/modules/grid_search.html) 实现，它让"预处理步骤与估计器参数"最优组合的搜索变得非常方便。在这里，我重点通过 [F1-score 性能指标](http://arxiv.org/pdf/1410.5330.pdf)来优化精确率和召回率，而不是优化整体准确率——我最感兴趣的是过滤出*悲伤*的歌曲；有人可能会说，这可以成为一个有趣的应用：把音乐库中所有*悲伤*的内容都剔除掉。

我不想在本文中过多展开模型选择的细节（这将是另一份独立报告的内容），所以只对最终模型的选择做一个非常简要的概述：[1-gram](https://sebastianraschka.com/Articles/2014_naive_bayes_1.html#tokenization) 分词、[停用词移除](https://sebastianraschka.com/Articles/2014_naive_bayes_1.html#stop-words)，以及基于词频的特征向量，再结合[多项式朴素贝叶斯模型](https://sebastianraschka.com/Articles/2014_naive_bayes_1.html#multinomial-naive-bayes)，看起来效果最好（以 F1 分数衡量）。不过，除 n-gram 序列长度的选择之外，不同预处理步骤和参数选择之间的差异都相当微小。最终模型的总结见下图。

![Musicmood roc best](https://sebastianraschka.com/images/blog/2014/musicmood/roc_best.webp)
![Musicmood performance table](https://sebastianraschka.com/images/blog/2014/musicmood/performance_table.webp)

## 部署网页应用

我尤其期待把最终分类器做成网页应用这个环节。我此前从未做过这件事，所以非常渴望深入研究 [Django](https://www.djangoproject.com) 或 [Flask](http://flask.pocoo.org)。在浏览了一些入门教程之后，我决定选用 Flask，因为它更加轻量，看起来更适合这个任务。把分类器嵌入 Flask Web 框架实际上比我最初想的要直接得多——Flask 真是一个非常棒、极易上手的库！

### 神秘的 500 错误

然而，真正的难点（也可能是整个项目中最具挑战性的部分）其实是在 Web 服务器上部署应用。问题始于我在 [bluehost](http://www.bluehost.com/shared) 服务器（我买的是"入门级"共享主机套餐）上搭建新的 Python 环境的时候。等我最终把所有 C 扩展"妥当地"编译安装好之后，为了让 *Apache* 服务器能够消化我的代码，还有一道坎要过：[FastCGI](https://en.wikipedia.org/wiki/FastCGI)。幸运的是，有一篇很棒的 [Flask 教程](https://web.archive.org/web/20141220005603/http://flask.pocoo.org/docs/0.10/deploying/fastcgi/)帮我攻克了这个难关。好了，理论上万事俱备——至少我是这么以为的。当我第一次在网上实际使用它时，我记得一切运行正常。不错，我在本地测试完 Flask 应用之后，它在 Web 服务器上似乎也能正常工作！然而遗憾的是，这份工作最初的喜悦并没有持续多久——服务器时不时会抛出 "500 Internal Server Error"（或者更准确地说，80% 的时间都在抛）。我前前后后翻阅了数百篇故障排查指南，也没找到任何原因。在这个特定的案例中，错误日志里什么都没写，这与我故意触发其他 500 错误时的表现不同。

### Pythonanywhere 来救场

最终，我把问题定位到了执行 scikit-learn/scipy/numpy 代码的那部分。于是我的结论是，可能是某个 C 库在这个特定的服务器平台上引发了故障。我也联系了 bluehost 的客服和脚本工程师，但遗憾的是，他们同样说不清这个问题的具体原因。到这一步，我已经相当沮丧了，因为我在一件由于无法解释的原因而无法工作的事情上投入了大量精力。不过出于好奇，我仍然想确认代码本身是否存在普遍性问题，于是就在 [pythonanywhere](https://www.pythonanywhere.com/) 上注册了一个免费账户——结果你猜怎么着：不需要安装任何额外的 Python 库，我的应用就神奇地跑起来了。不过，将来我可能还会在 bluehost 服务器上尝试一些其他方案，因为我不喜欢这种"烂尾"的感觉，也真诚期待任何有助于解决这个问题的技巧和建议。

如你所见，尽管我在模型选择过程中使用了 10 折交叉验证方法，这个模型仍然相当容易过拟合。比较小的训练数据集可能是原因之一，希望未来能够克服。

## 未来计划

### 有更新分类器的计划吗？

有！我最初的计划是以在线学习模式实现朴素贝叶斯分类器，让它在每次用户提供分类反馈时都得到更新。然而，我的直觉是，这样做会逐渐偏向当代最流行歌曲的某个子集。由于我也非常渴望扩充训练数据集以进行其他分析，例如不同机器学习算法之间的比较、以及针对不同训练集规模的性能比较，所以我选择了另一种方案。目前，如果用户对预测结果主动提供反馈，我会把歌曲、歌词和建议的情绪标签存入数据库。我计划每隔一段时间就重新训练和重新评估模型，以期提升预测性能并获得一些有趣的洞见。情绪标签的分配当然具有很强的主观性，因此我会为每首歌向数据库保存多个情绪标签，让"ground truth"标签可以通过多数表决来确定。同时，这也为一些有趣的基于回归的分析打开了大门。

### 声音数据怎么办？

我考虑过把声音数据纳入分类。不过，我认为难点在于声音数据很难获取。当然，Million Song Dataset 里有一些包含预提取声音特征的 HDF5 文件，但对于那些不在训练集中的新歌怎么办？也许从 YouTube 抓取音频流是未来可以探索的一个方向。
