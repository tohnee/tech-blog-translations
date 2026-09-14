---
title: "在 R 中创建热图"
title_en: "Creating Heat Maps in R"
source: https://sebastianraschka.com/Articles/heatmaps_in_r.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 在 R 中创建热图

> 原文：[Creating Heat Maps in R](https://sebastianraschka.com/Articles/heatmaps_in_r.html) · Sebastian Raschka's Articles

我收到过很多人的提问，他们都想通过热图（heat map）快速可视化自己的数据——而且理想情况下越快越好。这正是探索性数据分析的一大痛点：我们往往没有时间去啃完一整本讲各种软件包中特定技术的书，只为把手头的事情做完。不过，一旦我们对初步结果感到满意，再深入研究一下这个主题、进一步定制我们的图形、甚至为了发表而精修它们，或许就值得了。在这篇文章中，我的目标是为一次简单的数据分析简要介绍 R 的多个热图库之一。我选择 R，是因为它是最流行的免费统计软件包之一。当然，还有更多的工具可以产生类似的结果（甚至在 R 里也有许多不同的热图包），不过这个话题就留待日后再谈了。

## 章节

**注意：对于偏爱 Python 的读者，我还有一篇简短教程：[《Heatmaps, Hierarchical Clustering, and Dendrograms in Python"》（Python 中的热图、层次聚类与树状图）](http://nbviewer.ipython.org/github/rasbt/pattern_classification/blob/master/clustering/hierarchical/clust_complete_linkage.ipynb)**

[![Heatmaps in r python heatmap dendrogram](https://sebastianraschka.com/images/blog/2013/heatmaps_in_r/python_heatmap_dendrogram.webp)](http://nbviewer.ipython.org/github/rasbt/pattern_classification/blob/master/clustering/hierarchical/clust_complete_linkage.ipynb)

**我用到的文件可以从这个 GitHub 仓库下载：<https://github.com/rasbt/R_snippets/tree/master/heatmaps>**

![Heatmaps in r heatmaps in r](https://sebastianraschka.com/images/blog/2013/heatmaps_in_r/heatmaps_in_r.webp)

在这段话之后你会看到整套完整的代码，好让你清楚自己面对的是什么：一个使用 R 的 `gplot` 包、通过 `heatmap.2()` 函数创建热图的 R 脚本。考虑到我们「只不过」想创建一个简单的热图，它可能看起来像个庞然大物，但别担心，其中很多参数并不是必需的，我会在后面的章节中讨论细节。

## 脚本总览

```python
#########################################################
### A) Installing and loading required packages
#########################################################

if (!require("gplots")) {
   install.packages("gplots", dependencies = TRUE)
   library(gplots)
   }
if (!require("RColorBrewer")) {
   install.packages("RColorBrewer", dependencies = TRUE)
   library(RColorBrewer)
   }

#########################################################
### B) Reading in data and transform it into matrix format
#########################################################

data <- read.csv("../datasets/heatmaps_in_r.csv", comment.char="#")
rnames <- data[,1]                            # assign labels in column 1 to "rnames"
mat_data <- data.matrix(data[,2:ncol(data)])  # transform column 2-5 into a matrix
rownames(mat_data) <- rnames                  # assign row names

#########################################################
### C) Customizing and plotting the heat map
#########################################################

# creates a own color palette from red to green
my_palette <- colorRampPalette(c("red", "yellow", "green"))(n = 299)

# (optional) defines the color breaks manually for a "skewed" color transition
col_breaks = c(seq(-1,0,length=100),  # for red
  seq(0.01,0.8,length=100),           # for yellow
  seq(0.81,1,length=100))             # for green

# creates a 5 x 5 inch image
png("../images/heatmaps_in_r.png",    # create PNG for the heat map        
  width = 5*300,        # 5 x 300 pixels
  height = 5*300,
  res = 300,            # 300 pixels per inch
  pointsize = 8)        # smaller font size

heatmap.2(mat_data,
  cellnote = mat_data,  # same data set for cell labels
  main = "Correlation", # heat map title
  notecol="black",      # change font color of cell labels to black
  density.info="none",  # turns off density plot inside color legend
  trace="none",         # turns off trace lines inside the heat map
  margins =c(12,9),     # widens margins around plot
  col=my_palette,       # use on color palette defined earlier
  breaks=col_breaks,    # enable color transition at specified limits
  dendrogram="row",     # only draw a row dendrogram
  Colv="NA")            # turn off column clustering

dev.off()               # close the PNG device
```

[（下载该脚本）](https://raw.githubusercontent.com/rasbt/R_snippets/master/heatmaps/h1_simple.R)

## 在 R 中运行脚本

要在 R 中运行脚本，先启动一个新的 R 会话：可以在 shell 终端里输入 R，或者从你的「应用程序」文件夹中运行 R。然后，你可以在 R 中输入以下命令来执行脚本：

```python
source("path/to/the/script/heatmaps_in_R.R")
```

## 脚本参数详解

### A) 安装并加载所需的包

乍一看，这一节似乎比实际需要的复杂了一些，因为如果所需的 R 包已经安装，执行 `library(packagename)` 就足以加载它们了。

```python
if (!require("gplots")) {
 install.packages("gplots", dependencies = TRUE)
 library(gplots)
 }
if (!require("RColorBrewer")) {
 install.packages("RColorBrewer", dependencies = TRUE)
 library(RColorBrewer)
 }
```

### B) 读入数据并转换成矩阵格式

我们可以把多种不同文件格式的数据读入 R，包括 ASCII 格式的文本文件、Excel 电子表格等等。在本教程中，我们假设数据采用逗号分隔值（Comma-Separated Values，CSV）格式——这大概是最常见的数据文件格式之一了。

![Heatmaps in r heatmaps in r 2](https://sebastianraschka.com/images/blog/2013/heatmaps_in_r/heatmaps_in_r_2.webp)

当我们用自己喜欢的纯文本编辑器（而不是 Excel、Numbers 等电子表格程序）打开这个 CSV 文件时，它看起来是这样的：

```python
#heat map example data set,,,,
#12/08/13 sr,,,,
#
,var1,var2,var3,var4
measurement1,0.094,0.668,0.4153,0.4613
measurement2,0.1138,-0.3847,0.2671,0.1529
measurement3,0.1893,0.3303,0.5821,0.2632
measurement4,-0.0102,-0.4259,-0.5967,0.18
measurement5,0.1587,0.2948,0.153,-0.2208
measurement6,-0.4558,0.2244,0.6619,0.0457
measurement7,-0.6241,-0.3119,0.3642,0.2003
measurement8,-0.227,0.499,0.3067,0.3289
measurement9,0.7365,-0.0872,-0.069,-0.4252
measurement10,0.9761,0.4355,0.8663,0.8107
```

[（下载该 CSV 文件）](https://raw.githubusercontent.com/rasbt/R_snippets/master/heatmaps/dataset.csv)

当我们把 CSV 文件中的数据读入 R 并赋给变量 `data` 时，请注意 CSV 文件中位于主数据之前的两行注释，它们以井号（#，octothorpe）字符开头。由于绘制热图并不需要这些行，我们可以通过 `read.csv()` 函数的 `comment.char` 参数来忽略它们。

```python
data <- read.csv("../datasets/heatmaps_in_r.csv", comment.char="#")
```

`heatmap.2()` 函数的一个麻烦之处在于，它要求数据为数值矩阵格式才能绘图。默认情况下，我们用 R 的 `read.table()` 或 `read.csv()` 函数从文件中读取的数据会以 `data table` 格式存储。`matrix` 格式与 `data table` 格式的区别在于：一个 `matrix` 只能容纳一种类型的数据，例如数值、字符串或逻辑值。幸运的是，我们不必为包含列名（var1、var2、var3、var4）的那一行操心，因为 `read.csv()` 函数默认会把第一行数据当作 `table header`（表头）。但如果我们想把行名（measurement1、measurement2 等）也放进数值矩阵里，就会遇到麻烦。为了方便起见，我们把这些行名存到第一列中作为变量 `rnames`，稍后转换完成后，再用它为矩阵指定 `row names`（行名）。

```python
rnames <- data[,1]
```

现在，我们把变量 `data` 中的数值数据（第 2 列到第 5 列）转换成矩阵，并赋给一个新变量 `mat_data`：

```python
mat_data <- data.matrix(data[,2:ncol(data)])
```

与其使用 `ncol(data)]` 这种相当繁琐的表达式（它返回数据表的总列数），我们也可以直接提供整数 5 来指定想要包含的最后一列。不过，对于更大的数据集，`ncol(data)]` 更方便，这样我们就不必为了指定上界而数遍所有列去得到最后一列的索引。接下来，我们通过下面的代码，把之前保存为 `rnames` 的列名赋给矩阵：

```python
rownames(mat_data) <- rnames
```

### C) 定制并绘制热图

最后，我们的数据已经变成了创建热图所需的「正确」格式，不过在正式动手之前，让我们先简单看一些定制选项。

### 可选：选择自定义调色板和颜色分界点

我不想使用 `heatmap.2()` 函数的默认颜色，而是想向你展示如何用 `RColorBrewer` 包来创建我们自己的调色板。这里我们采用热图最流行的配色选择：从绿到黄再到红的颜色范围。

```python
my_palette <- colorRampPalette(c("red", "yellow", "green"))(n = 299)
```

在 R 中有很多种指定颜色的方法。我觉得最方便的是按名称来指定颜色。R 中各种颜色名称的一个不错的概览可以在 [`colors()` 文档](https://search.r-project.org/R/refmans/grDevices/html/colors.html)中找到。

参数 `(n = 299)` 让我们定义调色板中要包含多少种独立的颜色。显然，独立颜色的数量越多，过渡就越平滑；299 这个数字应该足以实现平滑的过渡了。默认情况下，RColorBrewer 会把颜色均匀划分，使调色板中的每种颜色对应的独立颜色区间大小相近。不过，根据所分析数据的不同，有时我们希望颜色范围略有偏斜。假设我们的示例数据集由 –1 到 1 的 Pearson 相关系数（即 R 值）组成，而我们特别关心（相对）高相关的样本：R 值在 0.8 到 1.0 之间。我们希望在热图中突出这些样本，只把 0.8 到 1 之间的值显示为绿色。在这种情况下，我们可以用下面的代码「不均匀地」定义颜色分界点（color breaks）：

```python
col_breaks = c(seq(-1,0,length=100), # for red
seq(0,0.8,length=100),  # for yellow
seq(0.81,1,length=100)) # for green
```

### 可选：将热图保存为 PNG 文件

R 支持多种不同的矢量图形格式，比如 SVG、PostScript 和 PDF，也支持 JPEG、PNG、TIFF、BMP 等光栅图形（位图）。每种格式都各有优缺点，根据具体用途（网站、期刊论文、PowerPoint 演示、归档……），我们会在不同格式之间做选择。在本教程中，我不想详细讨论何时该用哪种文件格式，而是直接为我们的热图选用更常见的 PNG 格式。我选 PNG 而不是 JPEG，是因为 PNG 提供无损压缩（JPEG 是有损图像格式），代价只是文件略微大一点。不过，如果你只想在 R 的交互式屏幕上显示热图，完全可以把脚本中的 `png()` 函数整个省掉。

```python
png("../images/heatmaps_in_r.png",    # create PNG for the heat map        
width = 5*300,        # 5 x 300 pixels
height = 5*300,
res = 300,            # 300 pixels per inch
pointsize = 8)        # smaller font size
```

`png()` 函数的默认参数会生成一个分辨率很低的、相对较小的 PNG 文件，这对热图来说并不实用。因此，我们为图像的 `width`（宽）、`height`（高）和分辨率提供额外的参数。`width` 和 `height` 的单位是像素，而不是英寸。所以，如果我们想创建一张每英寸 300 像素的 5×5 英寸图像，就得在这里做一点数学计算：[1500 像素] / [300 像素/英寸] = 5 英寸。此外，我们选择了稍小的 8 pt 字号。

**注意千万别忘了在脚本末尾通过 `dev.off()` 函数关闭 `png()` 绘图设备，否则你很可能无法打开这个 PNG 文件进行查看。**

### 绘制热图

现在，让我们正式动手，来看一看 `heatmap.2()` 函数：

```python
heatmap.2(mat_data,
  cellnote = mat_data,  # same data set for cell labels
  main = "Correlation", # heat map title
  notecol="black",      # change font color of cell labels to black
  density.info="none",  # turns off density plot inside color legend
  trace="none",         # turns off trace lines inside the heat map
  margins =c(12,9),     # widens margins around plot
  col=my_palette,       # use on color palette defined earlier
  breaks=col_breaks,    # enable color transition at specified limits
  dendrogram="row",     # only draw a row dendrogram
  Colv="NA")            # turn off column clustering
```

### 2014 年 2 月 19 日更新——聚类方法

如果你想更改默认的聚类方法（使用欧氏距离度量的完全链接法 complete linkage），可以这样做：对于方阵，我们可以基于矩阵数据定义距离和聚类：

```python
distance = dist(mat_data, method = "manhattan")
cluster = hclust(distance, method = "ward")
```

然后最终把它插入 `heatmap.2()` 函数：

```python
heatmap.2(mat_data,
  ...
  Rowv = as.dendrogram(cluster), # apply default clustering method
  Colv = as.dendrogram(cluster)) # apply default clustering method
)
```

### 2014 年 3 月 2 日更新——为测量值分类

刚有人问我如何通过添加行或列标签来对输入变量进行分类。例如，如果我们想把「measurement」变量分成 3 个不同的类别：measurement 1-3 = 类别 1，measurement 4-6 = 类别 2，measurement 7-10 = 类别 3。我的解决方案是直接给 `heatmap.2()` 函数提供一个额外参数 `RowSideColors`。例如：

```python
heatmap.2(mat_data,
  ...
  RowSideColors = c(    # grouping row-variables into different
     rep("gray", 3),   # categories, Measurement 1-3: green
     rep("blue", 3),    # Measurement 4-6: blue
     rep("black", 4)),    # Measurement 7-10: red
  ...
)
```

请注意，我们还可以通过 `ColSideColors` 参数为列变量提供类似的标签。另一个有用的补充是为新的类别标签添加颜色图例。这个特定示例的代码如下：

```python
par(lend = 1)           # square line ends for the color legend
legend("topright",      # location of the legend on the heatmap plot
    legend = c("category1", "category2", "category3"), # category labels
    col = c("gray", "blue", "black"),  # color key
    lty= 1,             # line style
    lwd = 10            # line width
)
```

下图展示了我们对行应用分类并添加颜色图例之后，修改过的热图的样子：

![Heatmaps in r heatmaps in r categorizing](https://sebastianraschka.com/images/blog/2013/heatmaps_in_r/heatmaps_in_r_categorizing.webp)

完整的（开箱即用的）脚本可以在这里找到：<https://github.com/rasbt/R_snippets/tree/master/heatmaps>
