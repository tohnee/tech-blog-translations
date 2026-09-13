---
title: "使用 RNN 预测股票价格：第二部分"
title_en: "Predict Stock Prices Using RNN: Part 2"
source: https://lilianweng.github.io/posts/2017-07-22-stock-rnn-part-2/
crawled: 2026-09-08
translated: 2026-09-08
---

# 使用 RNN 预测股票价格：第二部分

> 原文：[Predict Stock Prices Using RNN: Part 2](https://lilianweng.github.io/posts/2017-07-22-stock-rnn-part-2/) · Lilian Weng（翁荔）

> 本文是「如何使用 Tensorflow 构建循环神经网络来预测股票市场价格」系列教程的续篇。第二部分尝试使用嵌入来预测多只股票的价格。完整可运行的代码见 [lilianweng/stock-rnn](https://github.com/lilianweng/stock-rnn)。

在第二部分教程中，我想继续股价预测这一话题，并为我[第一部分](https://lilianweng.github.io/posts/2017-07-08-stock-rnn-part-1/)中构建的循环神经网络（Recurrent Neural Network，RNN）赋予同时应对多只股票的能力。为了区分与不同价格序列相关联的模式，我将股票代码的嵌入向量作为输入的一部分。

---

## 数据集

在查找过程中，我发现了[这个库](https://github.com/lukaszbanasiak/yahoo-finance)，用于查询 Yahoo! Finance API。如果 Yahoo 没有关闭历史数据抓取 API，它本会非常好用；不过查询其他信息时，它或许仍能派上用场。在若干可以免费下载历史股价的[数据源](https://www.quantshare.com/sa-43-10-ways-to-download-historical-stock-quotes-data-for-free)中，我这里选择了 Google Finance 的链接。

数据抓取代码可以写得非常简单：

```python

import urllib2
from datetime import datetime
BASE_URL = "https://www.google.com/finance/historical?"
           "output=csv&q={0}&startdate=Jan+1%2C+1980&enddate={1}"
symbol_url = BASE_URL.format(
    urllib2.quote('GOOG'), # Replace with any stock you are interested.
    urllib2.quote(datetime.now().strftime("%b+%d,+%Y"), '+')
)
```

抓取内容时，记得加上 try-catch 包装，以防链接失效或所提供的股票代码无效。

```python

try:
    f = urllib2.urlopen(symbol_url)
    with open("GOOG.csv", 'w') as fin:
        print >> fin, f.read()
except urllib2.HTTPError:
    print "Fetching Failed: {}".format(symbol_url)
```

完整可运行的数据抓取器代码可在[这里](https://github.com/lilianweng/stock-rnn/blob/master/data_fetcher.py)查看。

## 模型构建

我们希望模型按时间学习不同股票的价格序列。由于不同股票背后的模式各不相同，我想明确地告诉模型它正在处理的是哪只股票。[嵌入](https://en.wikipedia.org/wiki/Embedding)比 one-hot 编码（独热编码）更受青睐，原因如下：
1. 假设训练集包含 $$N$$ 只股票，one-hot 编码会引入 $$N$$（或 $$N-1$$）个额外的稀疏特征维度。而当每个股票代码都被映射到一个长度为 $$k$$（$$k \ll N$$）、小得多的嵌入向量之后，我们得到的就是一种压缩得多的表示，需要处理的数据集也更小。
2. 嵌入向量本身是待学习的变量。相似的股票可能会学到相似的嵌入，从而互相帮助预测，比如 "GOOG" 和 "GOOGL"，你会在后文图 5 中看到。

在循环神经网络中，在某个时间步 $$t$$，输入向量包含第 $$i$$ 只股票的 `input_size`（记为 $$w$$）个每日价格值，即 $$(p_{i, tw}, p_{i, tw+1}, \dots, p_{i, (t+1)w-1})$$。股票代码被唯一地映射到一个长度为 `embedding_size`（记为 $$k$$）的向量，即 $$(e_{i,0}, e_{i,1}, \dots, e_{i,k})$$。如图 1 所示，价格向量与嵌入向量拼接后，一起送入 LSTM 单元。

另一种备选方案是把嵌入向量与 LSTM 单元的最后状态拼接，并在输出层学习新的权重 $$W$$ 和偏置 $$b$$。然而这样一来，LSTM 单元就无法区分一只股票与另一只股票的价格，其能力会受到很大限制。因此我决定采用前一种方案。

![带嵌入的 RNN](https://lilianweng.github.io/posts/2017-07-22-stock-rnn-part-2/rnn_with_embedding.png)

*图 1：带股票代码嵌入的股价预测 RNN 模型架构。*

`RNNConfig` 中新增了两个配置项：
- `embedding_size` 控制每个嵌入向量的大小；
- `stock_count` 指数据集中不同股票的数量。

二者共同定义了嵌入矩阵的大小：与[第一部分](https://lilianweng.github.io/posts/2017-07-08-stock-rnn-part-1/)的模型相比，模型需要多学习 `embedding_size` $$\times$$ `stock_count` 个变量。

```python

class RNNConfig():
   # ... old ones
   embedding_size = 3
   stock_count = 50
```

### 定义计算图

**--- 我们开始过一遍代码吧 ---**

（1）如教程[第一部分：定义计算图](https://lilianweng.github.io/posts/2017-07-08-stock-rnn-part-1/#define-graph)所示，我们以同样的方式定义一个名为 `lstm_graph` 的 `tf.Graph()`，以及一组用于承载输入数据的张量：`inputs`、`targets` 和 `learning_rate`。还需要多定义一个占位符，用于存放与输入价格相关联的股票代码列表。股票代码事先已通过[标签编码](http://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.LabelEncoder.html)映射为唯一的整数。

```python

# Mapped to an integer. one label refers to one stock symbol.
stock_labels = tf.placeholder(tf.int32, [None, 1])
```

（2）接下来，我们需要建立一个嵌入矩阵，作为查找表使用，其中存放所有股票的嵌入向量。该矩阵以 [-1, 1] 区间内的随机数初始化，并会在训练过程中不断更新。

```python

# NOTE: config = RNNConfig() and it defines hyperparameters.
# Convert the integer labels to numeric embedding vectors.
embedding_matrix = tf.Variable(
    tf.random_uniform([config.stock_count, config.embedding_size], -1.0, 1.0)
)
```

（3）然后将股票标签重复 `num_steps` 次，以匹配 RNN 按时间展开后的版本以及训练期间 `inputs` 张量的形状。
变换操作 [tf.tile](https://www.tensorflow.org/api_docs/python/tf/tile) 接收一个基础张量，并通过将其某些维度复制多倍来创建新张量；确切地说，输入张量的第 $$i$$ 个维度会被复制 `multiples[i]` 倍。例如，若 `stock_labels` 为 `[[0], [0], [2], [1]]`
将它按 `[1, 5]` 平铺后得到 `[[0 0 0 0 0], [0 0 0 0 0], [2 2 2 2 2], [1 1 1 1 1]]`。

```python

stacked_stock_labels = tf.tile(stock_labels, multiples=[1, config.num_steps])
```

（4）然后根据查找表 `embedding_matrix`，把股票代码映射为嵌入向量。

```python

# stock_label_embeds.get_shape() = (?, num_steps, embedding_size).
stock_label_embeds = tf.nn.embedding_lookup(embedding_matrix, stacked_stock_labels)
```

（5）最后，把价格数值与嵌入向量组合起来。操作 [tf.concat](https://www.tensorflow.org/api_docs/python/tf/concat) 沿 `axis` 指定的维度拼接一组张量。在我们的场景中，批大小和步数保持不变，只需把长度为 `input_size` 的输入向量扩展为包含嵌入特征即可。

```python

# inputs.get_shape() = (?, num_steps, input_size)
# stock_label_embeds.get_shape() = (?, num_steps, embedding_size)
# inputs_with_embeds.get_shape() = (?, num_steps, input_size + embedding_size)
inputs_with_embeds = tf.concat([inputs, stock_label_embeds], axis=2)
```

其余代码运行动态 RNN、提取 LSTM 单元的最后状态，并处理输出层的权重和偏置。详情参见[第一部分：定义计算图](https://lilianweng.github.io/posts/2017-07-08-stock-rnn-part-1/#define-graph)。

### 训练会话

如果你还没有读过[第一部分：启动训练会话](https://lilianweng.github.io/posts/2017-07-08-stock-rnn-part-1/#start-training-session)，请先阅读，了解如何在 Tensorflow 中运行训练会话。

在把数据喂给计算图之前，需要先用[标签编码](http://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.LabelEncoder.html)将股票代码转换为唯一的整数。

```python

from sklearn.preprocessing import LabelEncoder
label_encoder = LabelEncoder()
label_encoder.fit(list_of_symbols)
```

对每只股票，训练/测试划分比例保持不变：90% 用于训练，10% 用于测试。

### 可视化计算图

在代码中定义好计算图之后，我们来查看 Tensorboard 中的可视化，确认各组件都构建正确。它看起来与图 1 中的架构示意图基本一致。

![带嵌入的 RNN 可视化](https://lilianweng.github.io/posts/2017-07-22-stock-rnn-part-2/rnn_with_embedding_tensorboard.png)

*图 2：上述定义的计算图在 Tensorboard 中的可视化。两个模块（"train" 和 "save"）已从主图中移除。*

除了展示计算图结构或随时间跟踪变量之外，Tensorboard 还支持[**嵌入可视化**](https://www.tensorflow.org/get_started/embedding_viz)。为了把嵌入值传递给 Tensorboard，我们需要在训练日志中添加适当的跟踪。

（0）在我的嵌入可视化中，我想按行业板块为每只股票着色。这些元数据应存储在一个 csv 文件中。该文件包含两列：股票代码和行业板块。csv 文件是否带表头无关紧要，但所列股票的顺序必须与 `label_encoder.classes_` 保持一致。

```python

import csv
embedding_metadata_path = os.path.join(your_log_file_folder, 'metadata.csv')
with open(embedding_metadata_path, 'w') as fout:
    csv_writer = csv.writer(fout)
    # write the content into the csv file.
    # for example, csv_writer.writerows(["GOOG", "information_technology"])
```

（1）先在训练用的 `tf.Session` 中设置好 summary writer（摘要写入器）。

```python

from tensorflow.contrib.tensorboard.plugins import projector
with tf.Session(graph=lstm_graph) as sess:
    summary_writer = tf.summary.FileWriter(your_log_file_folder)
    summary_writer.add_graph(sess.graph)
```

（2）把计算图 `lstm_graph` 中定义的张量 `embedding_matrix` 添加到 projector 配置变量中，并附上元数据 csv 文件。

```python

    projector_config = projector.ProjectorConfig()
    # You can add multiple embeddings. Here we add only one.
    added_embedding = projector_config.embeddings.add()
    added_embedding.tensor_name = embedding_matrix.name
    # Link this tensor to its metadata file.
    added_embedding.metadata_path = embedding_metadata_path
```

（3）这行代码会在文件夹 `your_log_file_folder` 中创建一个 `projector_config.pbtxt` 文件。TensorBoard 启动时会读取该文件。

```python

    projector.visualize_embeddings(summary_writer, projector_config)
```

## 结果

模型使用 S&P 500 指数中市值最大的前 50 只股票进行训练。

（在 [github.com/lilianweng/stock-rnn](https://github.com/lilianweng/stock-rnn) 中运行以下命令）
```bash
python main.py --stock_count=50 --embed_size=3 --input_size=3 --max_epoch=50 --train
```

所用配置如下：
```
stock_count = 100
input_size = 3
embed_size = 3
num_steps = 30
lstm_size = 256
num_layers = 1
max_epoch = 50
keep_prob = 0.8
batch_size = 64
init_learning_rate = 0.05
learning_rate_decay = 0.99
init_epoch = 5
```

### 价格预测

作为对预测质量的简要概览，图 3 绘制了 "KO"、"AAPL"、"GOOG" 和 "NFLX" 测试数据的预测结果。真实值与预测值之间的整体趋势是吻合的。考虑到预测任务的设计方式，模型依赖全部历史数据点，只预测接下来的 5（`input_size`）天。`input_size` 较小时，模型不必操心长期增长曲线；一旦增大 `input_size`，预测就会变得困难得多。

![结果 AAPL](https://lilianweng.github.io/posts/2017-07-22-stock-rnn-part-2/rnn_embedding_AAPL.png)
![结果 MSFT](https://lilianweng.github.io/posts/2017-07-22-stock-rnn-part-2/rnn_embedding_MSFT.png)
![结果 GOOG](https://lilianweng.github.io/posts/2017-07-22-stock-rnn-part-2/rnn_embedding_GOOG.png)
*图 3：测试集中 AAPL、MSFT 和 GOOG 的真实股价与预测股价。价格在连续的预测滑动窗口内做了归一化（见[第一部分：归一化](https://lilianweng.github.io/posts/2017-07-08-stock-rnn-part-1/#normalization)）。为了更好地比较真实趋势与预测趋势，y 轴数值乘以了 5。*

### 嵌入可视化

可视化嵌入空间中聚类的一种常用技术是 [t-SNE](https://en.wikipedia.org/wiki/T-distributed_stochastic_neighbor_embedding)（[Maaten and Hinton, 2008](http://www.jmlr.org/papers/volume9/vandermaaten08a/vandermaaten08a.pdf)），Tensorboard 对它有很好的支持。t-SNE 是 "t-Distributed Stochastic Neighbor Embedding"（t 分布随机邻域嵌入）的缩写，是随机邻域嵌入（Stochastic Neighbor Embedding，[Hinton and Roweis, 2002](http://www.cs.toronto.edu/~fritz/absps/sne.pdf)）的一种变体，但采用了一个更容易优化的修改版代价函数。

1. 与 SNE 类似，t-SNE 首先把高维空间中数据点之间的欧氏距离转换为表示相似度的条件概率。
2. t-SNE 在低维空间的数据点上定义一个类似的概率分布，并针对点在映射图上的位置，最小化这两个分布之间的 [Kullback–Leibler 散度](https://en.wikipedia.org/wiki/Kullback%E2%80%93Leibler_divergence)。

关于如何在 t-SNE 可视化中调整困惑度（Perplexity）和学习率（epsilon）这两个参数，请参阅[这篇文章](http://distill.pub/2016/misread-tsne/)。

![嵌入可视化](https://lilianweng.github.io/posts/2017-07-22-stock-rnn-part-2/embedding_clusters.png)

*图 4：使用 t-SNE 对股票嵌入的可视化。每个标签按股票所属行业板块着色。共有 5 个聚类。有趣的是，GOOG、GOOGL 和 FB 属于同一个聚类，而 AMZN 和 AAPL 则位于另一个聚类。*

在嵌入空间中，我们可以通过考察两只股票嵌入向量之间的相似度来衡量这两只股票的相似性。例如，在学到的嵌入中，与 GOOG 最相似的是 GOOGL（见图 5）。

![嵌入可视化：GOOG](https://lilianweng.github.io/posts/2017-07-22-stock-rnn-part-2/embedding_clusters_2.png)

*图 5：在嵌入可视化图中点击 "GOOG"，最相似的 20 个邻居被高亮显示，颜色随相似度降低由深变浅。*

### 已知问题

- 随着训练的进行，预测值会大幅缩小并变得非常平缓。这就是为什么我在图 3 中把绝对值乘了一个常数，让趋势更明显——因为我更关心涨跌方向的预测是否正确。不过，预测值缩小的问题一定有其原因。或许可以不使用简单的 MSE 作为损失，而是采用另一种形式的损失函数，在方向预测错误时施加更大的惩罚。
- 损失函数在开始阶段下降很快，但偶尔会出现数值爆炸（突然冒出一个峰值，随后又立刻回落）。我怀疑这也与损失函数的形式有关。一个改进的、更聪明的损失函数或许能够解决这个问题。

<br />
本教程的完整代码可在 [github.com/lilianweng/stock-rnn](https://github.com/lilianweng/stock-rnn) 获取。

---

*如果你发现本文中存在错误或问题，请随时通过 [lilian dot wengweng at gmail dot com] 联系我，我会非常乐意立即修正！*

谢谢！:)
