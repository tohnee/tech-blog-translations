---
title: "Aroma：用于代码推荐的机器学习"
title_en: "Aroma: ML for code recommendation"
date: 2019-04-04
source: https://ai.meta.com/blog/aroma-ml-for-code-recommendation/
crawled: 2026-09-22
translated: 2026-09-22
---

# Aroma：用于代码推荐的机器学习

> 原文：[Aroma: ML for code recommendation](https://ai.meta.com/blog/aroma-ml-for-code-recommendation/) · Meta AI（Wayback 存档）

数千名工程师编写代码来打造我们的应用，为全球数十亿人服务。这不是一项简单的任务——我们的服务已经变得非常多样和复杂，代码库包含数百万行代码，与从消息传递到图像渲染的各种系统交织在一起。为了让编写会影响如此多系统的代码更简单、更快速，工程师常常希望能找到别人是如何处理类似任务的。为此我们创造了 Aroma——一个使用机器学习（ML）的代码到代码搜索与推荐工具，让从大型代码库获取洞见的过程变得容易得多。

在 Aroma 之前，现有工具都无法完全解决这个问题：文档工具并不总是可得且可能过时；代码搜索工具常常返回海量匹配结果，难以立刻找到惯用的使用模式。有了 Aroma，工程师可以轻松找到常见编码模式，无需手动翻阅几十个代码片段，为日常开发工作流节省时间和精力。除了在内部代码库部署 Aroma，我们还在开源项目上创建了 Aroma 版本。本文所有示例均取自 GitHub 上 5000 个开源 Android 项目的合集。

## 什么是代码推荐？什么时候需要它？

设想一位 Android 工程师想看看别人是怎么写类似代码的。假设这位工程师写了下面这行代码，在 Android 手机上解码一张位图：

```
Bitmap bitmap = BitmapFactory.decodeStream(input);
```

这行代码能工作，但工程师想知道其他人在相关项目中如何实现这一功能，尤其是设置了哪些常见选项、处理了哪些常见错误，以避免应用在生产环境中崩溃。Aroma 让工程师可以直接用代码片段本身发起搜索查询，结果以代码推荐的形式返回。每条代码推荐由代码库中找到的一簇相似代码片段合成，代表一种常见使用模式。以下是 Aroma 针对该示例返回的第一条推荐：

代码示例 1

```
final BitmapFactory.Options options = new BitmapFactory.Options();
options.inSampleSize = 2;
// ...
Bitmap bmp = BitmapFactory.decodeStream(is, null, options);
```

这条代码推荐由代码库中找到的五个相似方法合成交织而成。这里只展示该方法簇中的公共代码，各方法的具体细节在空缺处（即 ... 部分）被移除。

这条代码推荐想说明什么？它说明在五种不同情形下，工程师在解码位图时都设置了额外选项。设置采样率（sample size）有助于降低解码大位图时的内存消耗——事实上，Stack Overflow 上一条热门帖子也建议了同样的模式。Aroma 通过发现一簇都包含这一模式的代码片段，自动创建了这条推荐。

再看另一条推荐。代码示例 2

```
try {
    InputStream is = am.open(fileName);
    image = BitmapFactory.decodeStream(is);
    is.close();
}
catch (IOException e) {
    // ...
}
```

这个代码片段由另外四个方法聚类而来，展示了解码位图时 InputStream 的惯常用法。此外，这条推荐还展示了在打开 InputStream 时捕获潜在 IOException 的良好实践。如果这一异常在运行时发生而未被捕获，应用会立即崩溃。负责任的工程师应基于这条推荐扩展代码，并妥善处理该异常。

编码环境中集成的 Aroma 代码推荐。

与传统代码搜索工具相比，Aroma 的代码推荐能力有若干优势：

- Aroma 在语法树上执行搜索。它不是寻找字符串级或 token 级的匹配，而是能找到与查询代码在语法上相似的实例，并通过剪除无关语法结构来高亮匹配的代码。
- Aroma 自动把相似的搜索结果聚类以生成代码推荐。这些推荐代表惯用的编码模式，比未聚类的搜索匹配更易于消化。
- Aroma 足够快，可以实时使用。实践中，即便对超大型代码库，它也能在数秒内生成推荐，且不需要预先做模式挖掘。
- Aroma 的核心算法与语言无关。我们已在内部 Hack、JavaScript、Python 和 Java 代码库中部署了 Aroma。

## Aroma 如何工作？

Aroma 通过三个主要阶段创建代码推荐：

**1) 基于特征的检索**

首先，Aroma 把代码语料索引为稀疏矩阵。它解析语料中的每个方法并创建其语法树，然后从每个方法的语法树中抽取一组结构特征。这些特征经过精心挑选，用以捕捉变量使用、方法调用和控制结构的信息。最后，它根据特征为每个方法创建一个稀疏向量。所有方法体的特征向量构成索引矩阵，用于搜索检索。

当工程师写下一个新的代码片段时，Aroma 按上述方式创建一个稀疏向量，并计算该向量与包含所有现有方法特征向量的矩阵的点积。点积最高的前 1000 个方法体被检索出来，作为推荐的候选集。即使代码语料可能包含数百万个方法，得益于稀疏向量与矩阵点积的高效实现，这一检索也很快。

**2) 重排序与聚类**

Aroma 检索出外观相似的方法候选集后，下一阶段是对它们聚类。为此，Aroma 首先需要按候选方法与查询代码片段的相似度重新排序。由于稀疏向量只包含「存在哪些特征」的抽象信息，点积分数低估了代码片段与查询的实际相似度。因此，Aroma 对方法语法树施加剪枝，丢弃方法体中无关的部分、只保留与查询片段最匹配的部分，从而按候选代码片段与查询的实际相似度对其重排序。

在得到按与查询相似度降序排列的候选代码片段列表后，Aroma 运行迭代聚类算法，找出彼此相似且包含可用于创建代码推荐的额外语句的代码片段簇。

**3) 交织（Intersecting）：创建代码推荐的过程**

代码片段 1（改编自该项目）：

```
InputStream is = ...;
final BitmapFactory.Options options = new BitmapFactory.Options();
options.inSampleSize = 2;
Bitmap bmp = BitmapFactory.decodeStream(is, null, options);
ImageView imageView = ...;
imageView.setImageBitmap(bmp);
// some more code
```

代码片段 2（改编自该项目）：

```
BitmapFactory.Options options = new BitmapFactory.Options();
while (...) {
    in = ...;
    options.inSampleSize = 2;
    options.inJustDecodeBounds = false;
    bitmap = BitmapFactory.decodeStream(in, null, options);
}
```

代码片段 3（改编自该项目）：

```
BitmapFactory.Options bmpFactoryOptions = new BitmapFactory.Options();
// some setup code
try {
    options.inSampleSize = 2;
    loadedBitmap = BitmapFactory.decodeStream(inputStream, null, bmpFactoryOptions);
    // some code...
}
catch (OutOfMemoryError oom) {
}
```

交织算法把第一个代码片段当作「基底」代码，然后针对簇中其余每个方法对其迭代施加剪枝。剪枝过程后剩下的代码就是所有方法的公共代码，它成为代码推荐。更多细节见我们关于该主题的论文。

在这个例子中，每个代码片段都包含其项目特有的代码，但它们都包含同样的设置位图解码选项的代码。如前所述，Aroma 首先剪掉第一个代码片段中没有出现在第二个片段中的行，找出公共代码。中间结果会是这样：

```
InputStream is = ...;
final BitmapFactory.Options options = new BitmapFactory.Options();
options.inSampleSize = 2;
Bitmap bmp = BitmapFactory.decodeStream(is, null, options);
```

代码片段 1 中关于 ImageView 的代码没有出现在代码片段 2 中，因此被移除。现在 Aroma 拿这个中间片段，继续剪掉未出现在代码片段 3、代码片段 4 等中的行。最终得到的代码作为代码推荐返回。如代码示例 1 所示，从这一簇创建的代码推荐恰好包含所有方法体公共的那三行代码。其他代码推荐以同样方式从其他簇创建，Aroma 的算法确保这些推荐彼此差异明显，因此工程师只需看少数几个代码片段就能学到多样的编码模式。例如，代码示例 2 就是从另一个簇计算出的推荐。

这正是使用 Aroma 的真正优势：不用手动翻阅几十条代码搜索结果、人工归纳惯用模式，Aroma 可以自动完成，而且只需几秒钟！

## 更大的图景

鉴于已经存在海量代码，我们相信工程师应当能够轻松发现大型代码库中反复出现的编码模式并从中学习。这正是 Aroma 所促成的能力。Aroma 和 Getafix 只是我们正在进行的多个利用 ML 改进软件工程的大型代码项目中的两个。随着这一领域的进展，我们相信编程应该成为一种半自动化任务：人类表达更高层的想法，而具体实现由计算机自己完成。

我们要感谢 Koushik Sen 和 Di Yang 在本项目上的工作。

**作者**

- Celeste Barnaby，Facebook 软件工程师
- Satish Chandra，Facebook 软件工程经理
- Frank Luan，Facebook 软件工程师
