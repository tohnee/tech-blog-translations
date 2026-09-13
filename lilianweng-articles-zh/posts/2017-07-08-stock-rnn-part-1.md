---
title: "使用 RNN 预测股价：第 1 部分"
title_en: "Predict Stock Prices Using RNN: Part 1"
source: https://lilianweng.github.io/posts/2017-07-08-stock-rnn-part-1/
crawled: 2026-09-08
translated: 2026-09-08
---

# 使用 RNN 预测股价：第 1 部分

> 原文：[Predict Stock Prices Using RNN: Part 1](https://lilianweng.github.io/posts/2017-07-08-stock-rnn-part-1/) · Lilian Weng（翁荔）

> 本文是一篇教程，介绍如何使用 Tensorflow 构建循环神经网络来预测股票市场价格。第 1 部分聚焦于标普 500 指数的预测。完整可运行的代码见 [lilianweng/stock-rnn](https://github.com/lilianweng/stock-rnn)。

这是一篇关于如何使用 Tensorflow 构建循环神经网络来预测股票市场价格的教程。完整可运行的代码见 [github.com/lilianweng/stock-rnn](https://github.com/lilianweng/stock-rnn)。如果你不知道什么是循环神经网络或 LSTM 单元，欢迎先阅读[我的上一篇文章](https://lilianweng.github.io/posts/2017-06-21-overview/#recurrent-neural-network)。

*我想强调一点：我写这篇文章的动机更多在于演示如何在 Tensorflow 中构建并训练一个 RNN 模型，而不是解决股票预测问题本身，因此我并没有花大力气去改进预测结果。非常欢迎你把我的[代码](https://github.com/lilianweng/stock-rnn)作为起点，加入更多与股票预测相关的想法来改进它。祝玩得开心！*

## 现有教程概览

互联网上已经有很多教程，比如：
- [A noob's guide to implementing RNN-LSTM using Tensorflow](http://monik.in/a-noobs-guide-to-implementing-rnn-lstm-using-tensorflow/)
- [TensorFlow RNN Tutorial](https://svds.com/tensorflow-rnn-tutorial/)
- [LSTM by Example using Tensorflow](https://medium.com/towards-data-science/lstm-by-example-using-tensorflow-feb0c1968537)
- [How to build a Recurrent Neural Network in TensorFlow](https://medium.com/@erikhallstrm/hello-world-rnn-83cd7105b767)
- [RNNs in Tensorflow, a Practical Guide and Undocumented Features](http://www.wildml.com/2016/08/rnns-in-tensorflow-a-practical-guide-and-undocumented-features/)
- [Sequence prediction using recurrent neural networks(LSTM) with TensorFlow](http://mourafiq.com/2016/05/15/predicting-sequences-using-rnn-in-tensorflow.html)
- [Anyone Can Learn To Code an LSTM-RNN in Python](https://iamtrask.github.io/2015/11/15/anyone-can-code-lstm/)
- [How to do time series prediction using RNNs, TensorFlow and Cloud ML Engine](https://medium.com/google-cloud/how-to-do-time-series-prediction-using-rnns-and-tensorflow-and-cloud-ml-engine-2ad2eeb189e8)

尽管已有这么多教程，我仍想再写一篇，主要出于三个原因：
1. 早期教程已经无法适配新版本，因为 Tensorflow 仍在开发中，API 接口变化很快。
2. 很多教程在示例中使用合成数据。而我更想玩一玩真实世界的数据。
3. 一些教程假设你事先对 Tensorflow API 已有了解，这让阅读变得有点困难。

在读过一堆示例之后，我建议把 Penn Tree Bank（PTB）数据集上的[官方示例](https://github.com/tensorflow/models/tree/master/tutorials/rnn/ptb)作为你的起点。PTB 示例以一种漂亮且模块化的设计模式展示了 RNN 模型，但这反而可能妨碍你轻松理解模型结构。因此，我在这里将以一种非常直白的方式来构建计算图。

## 目标

我将讲解如何构建一个基于 LSTM 单元的 RNN 模型来预测标普 500 指数的价格。数据集可以从 [Yahoo! Finance ^GSPC](https://finance.yahoo.com/quote/%5EGSPC/history?p=%5EGSPC) 下载。在下面的例子中，我使用了 1950 年 1 月 3 日（Yahoo! Finance 能追溯到的最早日期）到 2017 年 6 月 23 日的标普 500 数据。该数据集提供每天多个价格点。为简单起见，我们只用每日**收盘价**来做预测。同时，我会演示如何使用 [TensorBoard](https://www.tensorflow.org/get_started/summaries_and_tensorboard) 来方便地调试和跟踪模型。

快速回顾：循环神经网络（RNN）是一类在隐藏层中带有自循环的人工神经网络，这使得 RNN 能够利用隐藏神经元的先前状态，在给定新输入的情况下学习当前状态。RNN 擅长处理序列数据。长短期记忆（Long short-term memory，LSTM）单元是一种经过特殊设计的工作单元，帮助 RNN 更好地记忆长期上下文。

想了解更多细节，请阅读[我的上一篇文章](https://lilianweng.github.io/posts/2017-06-21-overview/#recurrent-neural-network)或[这篇精彩的文章](http://colah.github.io/posts/2015-08-Understanding-LSTMs/)。

## 数据准备

股价是一个长度为 $$N$$ 的时间序列，定义为 $$p_0, p_1, \dots, p_{N-1}$$，其中 $$p_i$$ 是第 $$i$$ 天的收盘价，$$0 \le i < N$$。设想我们有一个固定大小 $$w$$ 的滑动窗口（后文称之为 `input_size`），每次将窗口向右移动 $$w$$ 的宽度，这样所有滑动窗口中的数据互不重叠。

![时间序列中的滑动窗口](https://lilianweng.github.io/posts/2017-07-08-stock-rnn-part-1/sliding_window_time_series.svg)

*图 1：标普 500 价格随时间的变化。我们用一个滑动窗口中的内容预测下一个窗口，两个相邻窗口之间没有重叠。*

我们将要构建的 RNN 模型以 LSTM 单元作为基本隐藏单元。我们使用从第一个滑动窗口 $$W_0$$ 到时刻 $$t$$ 的窗口 $$W_t$$ 的全部数值：

$$ 
W_0 = (p_0, p_1, \dots, p_{w-1}) \\
W_1 = (p_w, p_{w+1}, \dots, p_{2w-1}) \\
\dots \\
W_t = (p_{tw}, p_{tw+1}, \dots, p_{(t+1)w-1})
$$

来预测紧接着的下一个窗口 $$w_{t+1}$$ 中的价格：

$$ W_{t+1} = (p_{(t+1)w}, p_{(t+1)w+1}, \dots, p_{(t+2)w-1}) $$

本质上，我们试图学习一个近似函数 $$f(W_0, W_1, \dots, W_t) \approx W_{t+1}$$。

![展开的 RNN](https://lilianweng.github.io/posts/2017-07-08-stock-rnn-part-1/unrolled_RNN.png)

*图 2：RNN 的展开版本。*

考虑到[沿时间反向传播（BPTT）](https://en.wikipedia.org/wiki/Backpropagation_through_time)的工作方式，我们通常以"展开（unrolled）"的版本训练 RNN，这样就不必把传播计算回溯得太远，从而省去训练中的复杂性。

以下是 [Tensorflow 教程](tensorflow.org/tutorials/recurrent)中对 `num_steps` 的解释：
> 在设计上，循环神经网络（RNN）的输出依赖于任意远的输入。不幸的是，这让反向传播计算变得困难。为了使学习过程易于处理，常见做法是创建网络的一个"展开"版本，其中包含固定数量（`num_steps`）的 LSTM 输入和输出。然后在这个 RNN 的有限近似上进行训练。实现方式是每次输入长度为 `num_steps` 的数据，并在每个这样的输入块之后执行一次反向传播。

价格序列首先被切分成互不重叠的小窗口。每个窗口包含 `input_size` 个数字，每个窗口被视为一个独立的输入元素。然后，将任意连续的 `num_steps` 个输入元素分为一组，构成一个训练输入，从而形成一个用于在 Tensorflow 上训练的**"展开"**版 RNN。对应的标签是紧随其后的那个输入元素。

<a name="input_format_example"></a>例如，如果 `input_size=3` 且 `num_steps=2`，我最开始的几个训练样本会是这样的：

$$
\text{Input}_1 = [[p_0, p_1, p_2], [p_3, p_4, p_5]], \text{Label}_1 = [p_6, p_7, p_8] \\

\text{Input}_2 = [[p_3, p_4, p_5], [p_6, p_7, p_8]], \text{Label}_2 = [p_9, p_{10}, p_{11}] \\

\text{Input}_3 = [[p_6, p_7, p_8], [p_9, p_{10}, p_{11}]], \text{Label}_3 = [p_{12}, p_{13}, p_{14}] 
$$

下面是数据格式化的关键部分：

```python

seq = [np.array(seq[i * self.input_size: (i + 1) * self.input_size]) 
       for i in range(len(seq) // self.input_size)]

# Split into groups of `num_steps`
X = np.array([seq[i: i + self.num_steps] for i in range(len(seq) - self.num_steps)])
y = np.array([seq[i + self.num_steps] for i in range(len(seq) - self.num_steps)])
```

数据格式化的完整代码在[这里](https://github.com/lilianweng/stock-rnn/blob/master/data_wrapper.py)。

### 训练 / 测试集划分

由于我们总是想预测未来，我们取**最新的 10%** 数据作为测试数据。

### 归一化
标普 500 指数随时间上涨，这带来一个问题：测试集中的大多数数值都超出了训练集的量程，因此模型不得不_预测一些它从未见过的数字_。可悲但不出人意料的是，它的表现惨不忍睹。见图 3。

![惨痛示例](https://lilianweng.github.io/posts/2017-07-08-stock-rnn-part-1/a_sad_example_stock_prediction.png)

图 3：一个十分惨痛的示例——RNN 模型不得不预测超出训练数据量程的数字。

为了解决量程外（out-of-scale）的问题，我对每个滑动窗口内的价格做归一化。任务变成了预测相对变化率，而不是绝对数值。在时刻 $$t$$ 的归一化滑动窗口 $$W'_t$$ 中，所有数值都除以最后一个"未知"价格——即 $$W_{t-1}$$ 中的最后一个价格：

$$ W'_t = (\frac{p_{tw}}{p_{tw-1}}, \frac{p_{tw+1}}{p_{tw-1}}, \dots, \frac{p_{(t+1)w-1}}{p_{tw-1}}) $$

这里有一份我爬取的截至 2017 年 7 月的标普 500 股价数据存档 [stock-data-lilianweng.tar.gz](https://drive.google.com/open?id=1QKVkiwgCNJsdQMEsfoi6KpqoPgc4O6DD)，欢迎取用 :)

## 模型构建

### 定义

- `lstm_size`：一层 LSTM 中的单元数。
- `num_layers`：堆叠的 LSTM 层数。
- `keep_prob`：[dropout](https://www.cs.toronto.edu/~hinton/absps/JMLRdropout.pdf) 操作中保留的单元比例。
- `init_learning_rate`：起始学习率。
- `learning_rate_decay`：后续训练轮次中的衰减比率。
- `init_epoch`：使用恒定 `init_learning_rate` 的轮数。
- `max_epoch`：训练的总轮数。
- `input_size`：滑动窗口的大小 / 一个训练数据点的大小。
- `batch_size`：一个 mini-batch 中使用的数据点数。

该 LSTM 模型有 `num_layers` 层堆叠的 LSTM，每层包含 `lstm_size` 个 LSTM 单元。然后对每个 LSTM 单元的输出应用保留概率为 `keep_prob` 的 [dropout](https://www.cs.toronto.edu/~hinton/absps/JMLRdropout.pdf) 掩码。dropout 的目标是消除对单一维度可能产生的强依赖，从而防止过拟合。

训练总共需要 `max_epoch` 轮（epoch）；一个 [epoch](http://www.fon.hum.uva.nl/praat/manual/epoch.html) 是对所有训练数据点的单次完整遍历。在每一轮中，训练数据点被切分成大小为 `batch_size` 的 mini-batch。我们每次向模型发送一个 mini-batch 进行一次 BPTT 学习。前 `init_epoch` 轮学习率设为 `init_learning_rate`，之后每轮衰减 $$\times$$ `learning_rate_decay`。

```python

# Configuration is wrapped in one object for easy tracking and passing.
class RNNConfig():
    input_size=1
    num_steps=30
    lstm_size=128
    num_layers=1
    keep_prob=0.8
    batch_size = 64
    init_learning_rate = 0.001
    learning_rate_decay = 0.99
    init_epoch = 5
    max_epoch = 50

config = RNNConfig()
```

### 定义计算图

[`tf.Graph`](https://www.tensorflow.org/api_docs/python/tf/Graph) 不附着任何真实数据。它定义了如何处理数据、如何运行计算的流程。之后，可以在 [`tf.session`](https://www.tensorflow.org/api_docs/python/tf/Session) 中向该图喂数据，此时计算才真正发生。

**--- 开始过一遍代码 ---**

(1) 首先初始化一个新图。

```python

import tensorflow as tf
tf.reset_default_graph()
lstm_graph = tf.Graph()
```

(2) 图的工作方式应在其作用域内定义。

```python

with lstm_graph.as_default():
```

(3) 定义计算所需的数据。这里我们需要三个输入变量，全部定义为 [`tf.placeholder`](https://www.tensorflow.org/versions/master/api_docs/python/tf/placeholder)，因为在构图阶段我们还不知道它们的具体取值。
- `inputs`：训练数据 _X_，形状为（数据样本数, `num_steps`, `input_size`）的张量；数据样本数未知，所以是 `None`。在我们的场景中，训练会话里它就是 `batch_size`。如果困惑请查看[输入格式示例](#input_format_example)。
- `targets`：训练标签 _y_，形状为（数据样本数, `input_size`）的张量。
- `learning_rate`：一个简单的浮点数。

```python

    # Dimension = (
    #     number of data examples, 
    #     number of input in one computation step, 
    #     number of numbers in one input
    # )
    # We don't know the number of examples beforehand, so it is None.
    inputs = tf.placeholder(tf.float32, [None, config.num_steps, config.input_size])
    targets = tf.placeholder(tf.float32, [None, config.input_size])
    learning_rate = tf.placeholder(tf.float32, None)
```

(4) 该函数返回一个带或不带 dropout 操作的 [LSTMCell](https://www.tensorflow.org/versions/r1.0/api_docs/python/tf/contrib/rnn/LSTMCell)。

```python

    def _create_one_cell():
        return tf.contrib.rnn.LSTMCell(config.lstm_size, state_is_tuple=True)
        if config.keep_prob < 1.0:
            return tf.contrib.rnn.DropoutWrapper(lstm_cell, output_keep_prob=config.keep_prob)
```

(5) 如果需要，我们把单元堆叠成多层。`MultiRNNCell` 帮助将多个简单单元按顺序连接组合成一个单元。

```python

    cell = tf.contrib.rnn.MultiRNNCell(
        [_create_one_cell() for _ in range(config.num_layers)], 
        state_is_tuple=True
    ) if config.num_layers > 1 else _create_one_cell()
```

(6) [`tf.nn.dynamic_rnn`](https://www.tensorflow.org/api_docs/python/tf/nn/dynamic_rnn) 构建一个由 `cell`（RNNCell）指定的循环神经网络。它返回一对值（模型输出, 状态），其中输出 `val` 默认大小为（`batch_size`, `num_steps`, `lstm_size`）。状态指 LSTM 单元的当前状态，这里不使用。

```python

    val, _ = tf.nn.dynamic_rnn(cell, inputs, dtype=tf.float32)
```

(7) [`tf.transpose`](https://www.tensorflow.org/api_docs/python/tf/transpose) 将输出从维度（`batch_size`, `num_steps`, `lstm_size`）转换为（`num_steps`, `batch_size`, `lstm_size`）。然后取出最后一个输出。

```python

    # Before transpose, val.get_shape() = (batch_size, num_steps, lstm_size)
    # After transpose, val.get_shape() = (num_steps, batch_size, lstm_size)
    val = tf.transpose(val, [1, 0, 2])
    # last.get_shape() = (batch_size, lstm_size)
    last = tf.gather(val, int(val.get_shape()[0]) - 1, name="last_lstm_output")
```

(8) 定义隐藏层与输出层之间的权重和偏置。

```python

    weight = tf.Variable(tf.truncated_normal([config.lstm_size, config.input_size]))
    bias = tf.Variable(tf.constant(0.1, shape=[config.input_size]))
    prediction = tf.matmul(last, weight) + bias
```

(9) 我们使用均方误差作为损失度量，并使用 [RMSPropOptimizer 算法](http://www.cs.toronto.edu/~tijmen/csc321/slides/lecture_slides_lec6.pdf)做梯度下降优化。

```python

    loss = tf.reduce_mean(tf.square(prediction - targets))
    optimizer = tf.train.RMSPropOptimizer(learning_rate)
    minimize = optimizer.minimize(loss)
```

### 开始训练会话

(1) 要用真实数据训练计算图，需要先启动一个 [`tf.session`](https://www.tensorflow.org/api_docs/python/tf/Session)。

```python

with tf.Session(graph=lstm_graph) as sess:
```

(2) 按定义初始化变量。

```python

    tf.global_variables_initializer().run()
```

(0) 各训练轮次的学习率应预先计算好。下标指轮次索引。

```python

learning_rates_to_use = [
    config.init_learning_rate * (
        config.learning_rate_decay ** max(float(i + 1 - config.init_epoch), 0.0)
    ) for i in range(config.max_epoch)]
```

(3) 下面的每个循环完成一轮（epoch）训练。

```python

    for epoch_step in range(config.max_epoch):
        current_lr = learning_rates_to_use[epoch_step]
        
        # Check https://github.com/lilianweng/stock-rnn/blob/master/data_wrapper.py
        # if you are curious to know what is StockDataSet and how generate_one_epoch() 
        # is implemented.
        for batch_X, batch_y in stock_dataset.generate_one_epoch(config.batch_size):
            train_data_feed = {
                inputs: batch_X, 
                targets: batch_y, 
                learning_rate: current_lr
            }
            train_loss, _ = sess.run([loss, minimize], train_data_feed)
```

(4) 别忘了在最后保存你训练好的模型。

```python

    saver = tf.train.Saver()
    saver.save(sess, "your_awesome_model_path_and_name", global_step=max_epoch_step)
```

完整代码见[这里](https://github.com/lilianweng/stock-rnn/blob/master/build_graph.py)。

### 使用 TensorBoard

构建计算图却没有可视化，就像在黑暗中作画——非常晦涩且容易出错。[Tensorboard](https://github.com/tensorflow/tensorboard) 提供了对图结构和学习过程的简便可视化。看看这个[上手教程](https://youtu.be/eBbEDRsCmv4)，只有 20 分钟，但非常实用，还展示了几个现场演示。

**要点总结**
- 使用 `with [tf.name_scope](https://www.tensorflow.org/api_docs/python/tf/name_scope)("your_awesome_module_name"):` 把为相似目标工作的元素包在一起。
- 许多 `tf.*` 方法接受 `name=` 参数。指定自定义名称能让你在读图时轻松许多。
- [`tf.summary.scalar`](https://www.tensorflow.org/api_docs/python/tf/summary/scalar) 和 [`tf.summary.histogram`](https://www.tensorflow.org/api_docs/python/tf/summary/histogram) 等方法帮助在迭代过程中跟踪图中变量的取值。
- 在训练会话中，用 [`tf.summary.FileWriter`](https://www.tensorflow.org/api_docs/python/tf/summary/FileWriter) 定义一个日志文件。

```python

with tf.Session(graph=lstm_graph) as sess:
    merged_summary = tf.summary.merge_all()
    writer = tf.summary.FileWriter("location_for_keeping_your_log_files", sess.graph)
    writer.add_graph(sess.graph)
```

之后，把训练进度和摘要结果写入该文件。

```python

_summary = sess.run([merged_summary], test_data_feed)
writer.add_summary(_summary, global_step=epoch_step)  # epoch_step in range(config.max_epoch)
```

![Tensorboard 截图一](https://lilianweng.github.io/posts/2017-07-08-stock-rnn-part-1/tensorboard1.png)
*图 4a：示例代码构建的 RNN 计算图。"train" 模块已被"从主图中移除"，因为在预测阶段它并不是模型的真实组成部分。*

![Tensorboard 截图二](https://lilianweng.github.io/posts/2017-07-08-stock-rnn-part-1/tensorboard2.png)
*图 4b：点击 "output_layer" 模块将其展开，查看详细结构。*

完整可运行的代码见 [github.com/lilianweng/stock-rnn](https://github.com/lilianweng/stock-rnn)。

## 结果

我在实验中使用了如下配置。

```python

num_layers=1
keep_prob=0.8
batch_size = 64
init_learning_rate = 0.001
learning_rate_decay = 0.99
init_epoch = 5
max_epoch = 100
num_steps=30
```

（感谢 Yury 发现了我在价格归一化中的一个 bug：我原本用的是同一窗口内的最后一个价格，而不是前一个时间窗口的最后一个价格。下列图表已修正。）

总体而言，预测股价不是一件容易的事。尤其是在归一化之后，价格趋势看起来噪声非常大。

![](https://lilianweng.github.io/posts/2017-07-08-stock-rnn-part-1/rnn_input1_lstm32.png)

*图 5a：测试数据最后 200 天的预测结果。模型以 input_size=1 和 lstm_size=32 训练。*

![](https://lilianweng.github.io/posts/2017-07-08-stock-rnn-part-1/rnn_input1_lstm128.png)

*图 5b：测试数据最后 200 天的预测结果。模型以 input_size=1 和 lstm_size=128 训练。*

![](https://lilianweng.github.io/posts/2017-07-08-stock-rnn-part-1/rnn_input5_lstm128.png)

*图 5c：测试数据最后 200 天的预测结果。模型以 input_size=5、lstm_size=128 和 max_epoch=75（而非 50）训练。*

本教程的示例代码见 [github.com/lilianweng/stock-rnn:scripts](https://github.com/lilianweng/stock-rnn/tree/master/scripts)。

<span style="color: red;">（更新于 2017 年 9 月 14 日）</span>
模型代码已更新并封装为类：[LstmRNN](https://github.com/lilianweng/stock-rnn/blob/master/model_rnn.py)。模型训练可以由 [main.py](https://github.com/lilianweng/stock-rnn/blob/master/main.py) 触发，例如：

```
python main.py --stock_symbol=SP500 --train --input_size=1 --lstm_size=128
```

---

*如果你发现本文中的错误，请毫不犹豫地联系我 [lilian dot wengweng at gmail dot com]，我会非常乐意立即修正！*
