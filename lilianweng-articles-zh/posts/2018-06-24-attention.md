---
title: "注意力？注意力！"
title_en: "Attention? Attention!"
source: https://lilianweng.github.io/posts/2018-06-24-attention/
crawled: 2026-09-08
translated: 2026-09-08
---

# 注意力？注意力！

> 原文：[Attention? Attention!](https://lilianweng.github.io/posts/2018-06-24-attention/) · Lilian Weng（翁荔）

> 近年来，注意力（attention）已成为深度学习社区中相当流行的概念和有用的工具。本文将探究注意力是如何被发明的，以及各种注意力机制与模型，例如 Transformer 和 SNAIL。

<span style="color: #286ee0;">[更新于 2018-10-28：新增[指针网络（Pointer Network）](#pointer-network)以及我的 Transformer 实现[链接](https://github.com/lilianweng/transformer-tensorflow)。]</span><br/>
<span style="color: #286ee0;">[更新于 2018-11-06：新增 Transformer 模型实现的[链接](https://github.com/lilianweng/transformer-tensorflow)。]</span><br/>
<span style="color: #286ee0;">[更新于 2018-11-18：新增[神经图灵机（Neural Turing Machines）](#neural-turing-machines)。]</span><br/>
<span style="color: #286ee0;">[更新于 2019-07-18：修正了介绍 [show-attention-tell](https://arxiv.org/abs/1502.03044) 论文时误用"self-attention"一词的错误；已移至[自注意力](#self-attention)一节。]</span><br/>
<span style="color: #286ee0;">[更新于 2020-04-07：关于改进 Transformer 模型的后续文章在[这里](https://lilianweng.github.io/posts/2020-04-07-the-transformer-family/)。]</span>

注意力在某种程度上受启发于我们如何对图像的不同区域投入视觉注意力，或如何关联一句话中的词。以图 1 中的柴犬照片为例。

![shiba](https://lilianweng.github.io/posts/2018-06-24-attention/shiba-example-attention.png)

*图 1：一只穿着男装的柴犬。原始照片归功于 Instagram [@mensweardog](https://www.instagram.com/mensweardog/?hl=en)。*

人类的视觉注意力让我们能够以"高分辨率"聚焦某个区域（即看黄色框里的尖耳朵），同时以"低分辨率"感知周围的图像（即现在那雪景背景和这套行头又如何？），然后据此调整焦点或做出推断。给定图像的一小块区域，其余的像素为那里应该显示什么提供了线索。我们预期黄色框里有一只尖耳朵，因为我们已经看到了狗鼻子、右边另一只尖耳朵和柴犬谜之双眼（红框里的东西）。相比之下，底部的毛衣和毯子就不如那些狗狗特征有用了。

类似地，我们可以解释一句话或相近上下文中词与词之间的关系。当我们看到 "eating"，我们预期很快遇到一个食物词。颜色词描述的是食物，但与 "eating" 本身大概没有太多直接关系。

![sentence](https://lilianweng.github.io/posts/2018-06-24-attention/sentence-example-attention.png)

*图 2：一个词以不同的方式"关注"同一句子中的其他词。*

简而言之，深度学习中的注意力可以宽泛地解释为一个重要性权重向量：为了预测或推断一个元素（如图像中的一个像素或句子中的一个词），我们用注意力向量估计它与其他元素的相关性（或如你在许多论文中读到的"*attends to*"，即"关注"）有多强，然后以注意力向量加权的元素值之和作为目标的近似。

## Seq2Seq 模型有什么问题？

**seq2seq** 模型诞生于语言建模领域（[Sutskever, et al. 2014](https://arxiv.org/abs/1409.3215)）。宽泛地说，它旨在把一个输入序列（源）变换为一个新的序列（目标），且两个序列的长度都可以是任意的。变换任务的例子包括多种语言之间文本或语音的机器翻译、问答对话生成，甚至把句子解析为语法树。

seq2seq 模型通常采用编码器-解码器（encoder-decoder）架构，由以下部分组成：
- **编码器（encoder）**处理输入序列，把信息压缩成一个*固定长度*的上下文向量（也称句子嵌入或"思维"向量）。期望该表示是对*整个*源序列含义的良好概括。
- **解码器（decoder）**以上下文向量初始化，发出变换后的输出。早期工作只用编码器网络的最后状态作为解码器初始状态。

编码器和解码器都是循环神经网络，即使用 [LSTM 或 GRU](http://colah.github.io/posts/2015-08-Understanding-LSTMs/) 单元。

![带加性注意力层的编码器-解码器模型](https://lilianweng.github.io/posts/2018-06-24-attention/encoder-decoder-example.png)

*图 3：编码器-解码器模型，把句子 "she is eating a green apple" 翻译成中文。编码器与解码器的可视化都按时间展开。*

这种固定长度上下文向量设计的一个关键且明显的缺点是无法记住长句子。常常是处理完整个输入后，它已经忘了开头的部分。注意力机制的诞生（[Bahdanau et al., 2015](https://arxiv.org/pdf/1409.0473.pdf)）正是为了解决这个问题。

## 为翻译而生

注意力机制诞生是为了在神经机器翻译（[NMT](https://arxiv.org/pdf/1409.0473.pdf)）中帮助记忆长的源句子。注意力发明的秘诀不在于从编码器最后的隐藏状态构建单个上下文向量，而是在上下文向量与整个源输入之间创建捷径。这些捷径连接的权重可以为每个输出元素定制。

由于上下文向量可以访问整个输入序列，我们无须担心遗忘。源与目标之间的对齐由上下文向量学习并控制。本质上，上下文向量消费三条信息：
- 编码器隐藏状态；
- 解码器隐藏状态；
- 源与目标之间的对齐。

![带加性注意力层的编码器-解码器模型](https://lilianweng.github.io/posts/2018-06-24-attention/encoder-decoder-attention.png)

*图 4：[Bahdanau et al., 2015](https://arxiv.org/pdf/1409.0473.pdf) 中带加性注意力机制的编码器-解码器模型。*

### 定义

现在让我们以科学的方式定义 NMT 中引入的注意力机制。设我们有一个长度为 $$n$$ 的源序列 $$\mathbf{x}$$，试图输出一个长度为 $$m$$ 的目标序列 $$\mathbf{y}$$：

$$
\begin{aligned}
\mathbf{x} &= [x_1, x_2, \dots, x_n] \\
\mathbf{y} &= [y_1, y_2, \dots, y_m]
\end{aligned}
$$

（粗体变量表示向量；本文其余部分同。）

编码器是一个[双向 RNN](https://www.coursera.org/lecture/nlp-sequence-models/bidirectional-rnn-fyXnn)（或你选的其他循环网络设定），有前向隐藏状态 $$\overrightarrow{\boldsymbol{h}}_i$$ 和后向隐藏状态 $$\overleftarrow{\boldsymbol{h}}_i$$。二者的简单拼接表示编码器状态。动机是在一个词的标注中同时包含其前文和后文。

$$
\boldsymbol{h}_i = [\overrightarrow{\boldsymbol{h}}_i^\top; \overleftarrow{\boldsymbol{h}}_i^\top]^\top, i=1,\dots,n
$$

解码器网络对位置 t 的输出词有隐藏状态 $$\boldsymbol{s}_t=f(\boldsymbol{s}_{t-1}, y_{t-1}, \mathbf{c}_t)$$，$$t=1,\dots,m$$，其中上下文向量 $$\mathbf{c}_t$$ 是输入序列隐藏状态以对齐分数加权的和：

$$
\begin{aligned}
\mathbf{c}_t &= \sum_{i=1}^n \alpha_{t,i} \boldsymbol{h}_i & \small{\text{; Context vector for output }y_t}\\
\alpha_{t,i} &= \text{align}(y_t, x_i) & \small{\text{; How well two words }y_t\text{ and }x_i\text{ are aligned.}}\\
&= \frac{\exp(\text{score}(\boldsymbol{s}_{t-1}, \boldsymbol{h}_i))}{\sum_{i'=1}^n \exp(\text{score}(\boldsymbol{s}_{t-1}, \boldsymbol{h}_{i'}))} & \small{\text{; Softmax of some predefined alignment score.}}.
\end{aligned}
$$

对齐模型基于匹配程度为位置 i 的输入与位置 t 的输出对 $$(y_t, x_i)$$ 打出分数 $$\alpha_{t,i}$$。集合 $$\{\alpha_{t, i}\}$$ 是定义每个输出应考虑多少各源隐藏状态的权重。在 Bahdanau 的论文中，对齐分数 $$\alpha$$ 由一个带单个隐藏层的**前馈网络**参数化，该网络与模型的其他部分联合训练。因此，在以 tanh 为非线性激活函数的情况下，分数函数具有如下形式：

$$
\text{score}(\boldsymbol{s}_t, \boldsymbol{h}_i) = \mathbf{v}_a^\top \tanh(\mathbf{W}_a[\boldsymbol{s}_t; \boldsymbol{h}_i])
$$

其中 $$\mathbf{v}_a$$ 和 $$\mathbf{W}_a$$ 都是对齐模型中要学习的权重矩阵。

对齐分数矩阵是一个漂亮的副产品，可以显式展示源词与目标词之间的相关性。

![对齐矩阵](https://lilianweng.github.io/posts/2018-06-24-attention/bahdanau-fig3.png)

*图 5："L'accord sur l'Espace économique européen a été signé en août 1992"（法语）与其英语翻译 "The agreement on the European Economic Area was signed in August 1992" 的对齐矩阵。（图片来源：[Bahdanau et al., 2015](https://arxiv.org/pdf/1409.0473.pdf) 图 3）*

更多实现说明请看 Tensorflow 团队的这个优质[教程](https://www.tensorflow.org/versions/master/tutorials/seq2seq)。

## 注意力机制家族

借助注意力，源序列与目标序列之间的依赖不再受中间距离的限制！鉴于注意力在机器翻译上的巨大改进，它很快被扩展到计算机视觉领域（[Xu et al. 2015](http://proceedings.mlr.press/v37/xuc15.pdf)），人们也开始探索各种其他形式的注意力机制（[Luong, et al., 2015](https://arxiv.org/pdf/1508.04025.pdf)；[Britz et al., 2017](https://arxiv.org/abs/1703.03906)；[Vaswani, et al., 2017](http://papers.nips.cc/paper/7181-attention-is-all-you-need.pdf)）。

### 总结

下面是几种流行的注意力机制及相应对齐分数函数的总结表：

| 名称 | 对齐分数函数 | 引用 |
| -------------------------- | ------------- | ------------- |
| 基于内容的注意力 | $$\text{score}(\boldsymbol{s}_t, \boldsymbol{h}_i) = \text{cosine}[\boldsymbol{s}_t, \boldsymbol{h}_i]$$ | [Graves2014](https://arxiv.org/abs/1410.5401) |
| 加性（*） | $$\text{score}(\boldsymbol{s}_t, \boldsymbol{h}_i) = \mathbf{v}_a^\top \tanh(\mathbf{W}_a[\boldsymbol{s}_t; \boldsymbol{h}_i])$$ | [Bahdanau2015](https://arxiv.org/pdf/1409.0473.pdf) |
| 基于位置 | $$\alpha_{t,i} = \text{softmax}(\mathbf{W}_a \boldsymbol{s}_t)$$<br/>注：这将 softmax 对齐简化为只依赖目标位置。 | [Luong2015](https://arxiv.org/pdf/1508.04025.pdf) |
| General | $$\text{score}(\boldsymbol{s}_t, \boldsymbol{h}_i) = \boldsymbol{s}_t^\top\mathbf{W}_a\boldsymbol{h}_i$$<br/>其中 $$\mathbf{W}_a$$ 是注意力层中可训练的权重矩阵。 | [Luong2015](https://arxiv.org/pdf/1508.04025.pdf) |
| 点积 | $$\text{score}(\boldsymbol{s}_t, \boldsymbol{h}_i) = \boldsymbol{s}_t^\top\boldsymbol{h}_i$$ | [Luong2015](https://arxiv.org/pdf/1508.4025.pdf) |
| 缩放点积（^） | $$\text{score}(\boldsymbol{s}_t, \boldsymbol{h}_i) = \frac{\boldsymbol{s}_t^\top\boldsymbol{h}_i}{\sqrt{n}}$$<br/>注：与点积注意力非常相似，只差一个缩放因子；n 是源隐藏状态的维度。 | [Vaswani2017](http://papers.nips.cc/paper/7181-attention-is-all-you-need.pdf) |

（*）在 Luong, et al., 2015 中称为 "concat"，在 Vaswani, et al., 2017 中称为 "加性注意力（additive attention）"。<br/>
（^）它添加了缩放因子 $$1/\sqrt{n}$$，动机是担心当输入很大时 softmax 函数的梯度可能极小，不利于高效学习。<br/>

下面是更宽泛类别的注意力机制总结：

| 名称 | 定义 | 引用 |
| -------------------------- | ------------- | ------------- |
| 自注意力（&） | 关联同一输入序列的不同位置。理论上自注意力可以采用上面任何分数函数，只需把目标序列换成同一输入序列。 | [Cheng2016](https://arxiv.org/pdf/1601.06733.pdf) |
| 全局/软 | 关注整个输入状态空间。 | [Xu2015](http://proceedings.mlr.press/v37/xuc15.pdf) |
| 局部/硬 | 关注输入状态空间的一部分；即输入图像的一块。 | [Xu2015](http://proceedings.mlr.press/v37/xuc15.pdf)；[Luong2015](https://arxiv.org/pdf/1508.04025.pdf) |

（&）在 Cheng et al., 2016 及其他一些论文中也称为 "intra-attention"。

### 自注意力

**自注意力（self-attention）**也称**内部注意力（intra-attention）**，是一种关联单个序列不同位置以计算该序列自身表示的注意力机制。它已被证明在机器阅读、抽象摘要或图像描述生成中非常有用。

[长短期记忆网络](https://arxiv.org/pdf/1601.06733.pdf)论文使用自注意力做机器阅读。在下面的例子中，自注意力机制使我们能学习当前词与句子前文之间的相关性。

![intra-attention](https://lilianweng.github.io/posts/2018-06-24-attention/cheng2016-fig1.png)

*图 6：当前词为红色，蓝色阴影的大小表示激活程度。（图片来源：[Cheng et al., 2016](https://arxiv.org/pdf/1601.06733.pdf)）*

### 软注意力与硬注意力

在 [show, attend and tell](http://proceedings.mlr.press/v37/xuc15.pdf) 论文中，注意力机制被应用于图像以生成描述。图像先由 CNN 编码以提取特征。然后 LSTM 解码器消费卷积特征逐个生成描述词，其中权重通过注意力学习。注意力权重的可视化清晰地展示了模型为输出某个词正在关注图像的哪些区域。

![show-attend-and-tell](https://lilianweng.github.io/posts/2018-06-24-attention/xu2015-fig6b.png)

*图 7："A woman is throwing a frisbee in a park."（一位女人在公园里扔飞盘。）（图片来源：[Xu et al. 2015](http://proceedings.mlr.press/v37/xuc15.pdf) 图 6(b)）*

该论文首次基于"注意力能访问整幅图像还是仅一小块"提出了"软"与"硬"注意力的区分：

- **软（Soft）**注意力：对齐权重被学习并"软性"地放置在源图像的所有图块上；本质上与 [Bahdanau et al., 2015](https://arxiv.org/abs/1409.0473) 中的注意力同型。
    - *优点*：模型平滑且可微。
    - *缺点*：源输入很大时代价高昂。
- **硬（Hard）**注意力：一次只选择图像的一个图块去关注。
    - *优点*：推理时计算量更少。
    - *缺点*：模型不可微，需要更复杂的技术如方差缩减或强化学习来训练。（[Luong, et al., 2015](https://arxiv.org/abs/1508.04025)）

### 全局与局部注意力

[Luong, et al., 2015](https://arxiv.org/pdf/1508.04025.pdf) 提出了"全局（global）"和"局部（local）"注意力。全局注意力类似于软注意力，而局部注意力是[硬与软注意力](#soft-vs-hard-attention)的有趣混合，是对硬注意力的改进使其可微：模型先为当前目标词预测单个对齐位置，然后以源位置为中心的窗口被用于计算上下文向量。

![global-local-attention](https://lilianweng.github.io/posts/2018-06-24-attention/luong2015-fig2-3.png)

*图 8：全局与局部注意力（图片来源：[Luong, et al., 2015](https://arxiv.org/pdf/1508.04025.pdf) 图 2 与图 3）*

## 神经图灵机

Alan Turing 在 [1936 年](https://en.wikipedia.org/wiki/Turing_machine)提出了一个极简的计算模型。它由一条无限长的纸带和一个与纸带交互的读写头组成。纸带上有数不清的单元格，每个单元格填有一个符号：0、1 或空白（" "）。操作头可以读符号、改符号并在纸带上左右移动。理论上，无论算法多复杂、代价多高，图灵机都能模拟任何计算机算法。无限内存使图灵机在数学上无远弗届。然而无限内存在现代真实计算机中不可行，因此我们只把图灵机当作计算的数学模型。

![turing-machine](https://lilianweng.github.io/posts/2018-06-24-attention/turing-machine.jpg)

*图 9：图灵机的样子：一条纸带 + 一个处理纸带的读写头。（图片来源：http://aturingmachine.com/）*

**神经图灵机（Neural Turing Machine，NTM**，[Graves, Wayne & Danihelka, 2014](https://arxiv.org/abs/1410.5401)）是把神经网络与外部存储器耦合的模型架构。存储器模拟图灵机的纸带，神经网络控制操作头从纸带读取或写入。然而，NTM 中的存储器是有限的，因此它看起来可能更像一台"神经[冯·诺依曼](https://en.wikipedia.org/wiki/Von_Neumann_architecture)机"。

NTM 包含两个主要组件：*控制器*神经网络和*存储器*库。
控制器（Controller）：负责对存储器执行操作。它可以是任何类型的神经网络，前馈或循环皆可。
存储器（Memory）：存储处理过的信息。它是一个大小为 $$N \times M$$ 的矩阵，包含 N 个向量行，每个有 $$M$$ 维。

在一次更新迭代中，控制器处理输入并相应地与存储器库交互以生成输出。交互由一组并行的*读*头和*写*头处理。读和写操作都是"模糊"的——通过软性关注所有存储地址来实现。

![turing-machine](https://lilianweng.github.io/posts/2018-06-24-attention/NTM.png)

*图 10：神经图灵机架构。*

### 读写

在时间 t 从存储器读取时，一个大小为 $$N$$ 的注意力向量 $$\mathbf{w}_t$$ 控制对不同存储位置（矩阵行）分配多少注意力。读向量 $$\mathbf{r}_t$$ 是以注意力强度加权的和：

$$
\mathbf{r}_t = \sum_{i=1}^N w_t(i)\mathbf{M}_t(i)\text{, where }\sum_{i=1}^N w_t(i)=1, \forall i: 0 \leq w_t(i) \leq 1
$$

其中 $$w_t(i)$$ 是 $$\mathbf{w}_t$$ 的第 $$i$$ 个元素，$$\mathbf{M}_t(i)$$ 是存储器中的第 $$i$$ 个行向量。

在时间 t 向存储器写入时，受 LSTM 中输入门和遗忘门的启发，写头先按擦除向量 $$\mathbf{e}_t$$ 抹去一些旧内容，再通过添加向量 $$\mathbf{a}_t$$ 加入新信息。

$$
\begin{aligned}
\tilde{\mathbf{M}}_t(i) &= \mathbf{M}_{t-1}(i) [\mathbf{1} - w_t(i)\mathbf{e}_t] &\scriptstyle{\text{; erase}}\\
\mathbf{M}_t(i) &= \tilde{\mathbf{M}}_t(i) + w_t(i) \mathbf{a}_t &\scriptstyle{\text{; add}}
\end{aligned}
$$

### 注意力机制

在神经图灵机中，如何生成注意力分布 $$\mathbf{w}_t$$ 取决于寻址机制：NTM 使用基于内容与基于位置的混合寻址。

**基于内容的寻址**

内容寻址基于控制器从输入中提取的键向量 $$\mathbf{k}_t$$ 与存储器各行之间的相似性创建注意力向量。基于内容的注意力分数按余弦相似度计算，再由 softmax 归一化。此外，NTM 加入强度乘子 $$\beta_t$$ 来放大或收缩分布的焦点。

$$
w_t^c(i) 
= \text{softmax}(\beta_t \cdot \text{cosine}[\mathbf{k}_t, \mathbf{M}_t(i)])
= \frac{\exp(\beta_t \frac{\mathbf{k}_t \cdot \mathbf{M}_t(i)}{\|\mathbf{k}_t\| \cdot \|\mathbf{M}_t(i)\|})}{\sum_{j=1}^N \exp(\beta_t \frac{\mathbf{k}_t \cdot \mathbf{M}_t(j)}{\|\mathbf{k}_t\| \cdot \|\mathbf{M}_t(j)\|})}
$$

**插值**

然后使用插值门标量 $$g_t$$ 把新生成的基于内容的注意力向量与上一时间步的注意力权重混合：

$$
\mathbf{w}_t^g = g_t \mathbf{w}_t^c + (1 - g_t) \mathbf{w}_{t-1} 
$$

**基于位置的寻址**

基于位置的寻址把注意力向量中不同位置的值加总，权重是一个在允许的整数位移上的加权分布。它等价于与核 $$\mathbf{s}_t(.)$$（位置偏移的函数）做一维卷积。定义这个分布有多种方式，见图 11 以获取灵感。

![shift-weighting](https://lilianweng.github.io/posts/2018-06-24-attention/shift-weighting.png)

*图 11. 表示位移权重分布 $$\mathbf{s}_t$$ 的两种方式。*

最后，注意力分布被锐化标量 $$\gamma_t \geq 1$$ 增强。

$$
\begin{aligned}
\tilde{w}_t(i) &= \sum_{j=1}^N w_t^g(j) s_t(i-j) & \scriptstyle{\text{; circular convolution}}\\
w_t(i) &= \frac{\tilde{w}_t(i)^{\gamma_t}}{\sum_{j=1}^N \tilde{w}_t(j)^{\gamma_t}} & \scriptstyle{\text{; sharpen}}
\end{aligned}
$$

时间步 t 生成注意力向量 $$\mathbf{w}_t$$ 的完整流程见图 12。控制器产生的所有参数对每个头都是独立的。若有多个并行的读写头，控制器会输出多组参数。

![NTM-flow-addressing](https://lilianweng.github.io/posts/2018-06-24-attention/NTM-flow-addressing.png)

*图 12：神经图灵机寻址机制的流程图。（图片来源：[Graves, Wayne & Danihelka, 2014](https://arxiv.org/abs/1410.5401)）*

## 指针网络

在排序或旅行商这类问题中，输入和输出都是序列数据。遗憾的是，它们无法被经典 seq2seq 或 NMT 模型轻易解决，因为输出元素的离散类别并非预先确定，而是取决于可变的输入大小。**指针网络（Pointer Net，Ptr-Net**；[Vinyals, et al. 2015](https://arxiv.org/abs/1506.03134)）被提出来解决这类问题：当输出元素对应输入序列中的*位置*时。指针网络不用注意力把编码器的隐藏单元混合成上下文向量（见图 8），而是在每个解码器步骤对输入元素施加注意力、从中挑选一个作为输出。

![pointer network](https://lilianweng.github.io/posts/2018-06-24-attention/ptr-net.png)

*图 13：指针网络模型的架构。（图片来源：[Vinyals, et al. 2015](https://arxiv.org/abs/1506.03134)）*

Ptr-Net 给定输入向量序列 $$\boldsymbol{x} = (x_1, \dots, x_n)$$ 时输出一列整数索引 $$\boldsymbol{c} = (c_1, \dots, c_m)$$，且 $$1 \leq c_i \leq n$$。模型仍采用编码器-解码器框架。编码器和解码器的隐藏状态分别记作 $$(\boldsymbol{h}_1, \dots, \boldsymbol{h}_n)$$ 和 $$(\boldsymbol{s}_1, \dots, \boldsymbol{s}_m)$$。注意 $$\mathbf{s}_i$$ 是解码器中单元激活后的输出门。Ptr-Net 在状态之间应用加性注意力，然后用 softmax 归一化以建模输出的条件概率：

$$
\begin{aligned}
y_i &= p(c_i \vert c_1, \dots, c_{i-1}, \boldsymbol{x}) \\
    &= \text{softmax}(\text{score}(\boldsymbol{s}_t; \boldsymbol{h}_i)) = \text{softmax}(\mathbf{v}_a^\top \tanh(\mathbf{W}_a[\boldsymbol{s}_t; \boldsymbol{h}_i]))
\end{aligned}
$$

注意力机制被简化了，因为 Ptr-Net 不用注意力权重把编码器状态混合进输出。这样，输出只响应位置而不响应输入内容。

## Transformer

["Attention is All you Need"](http://papers.nips.cc/paper/7181-attention-is-all-you-need.pdf)（Vaswani, et al., 2017）无疑是 2017 年最有影响力和最有趣的论文之一。它对软注意力提出了许多改进，使*不使用*循环网络单元做 seq2seq 建模成为可能。所提出的 "**transformer**" 模型完全建立在自注意力机制之上，不使用序列对齐的循环架构。

秘诀就在其模型架构中。

### 键、值与查询

Transformer 的主要组件是*多头自注意力机制*单元。Transformer 把输入的编码表示视为一组**键（key）**-**值（value）**对 $$(\mathbf{K}, \mathbf{V})$$，二者的维度均为 $$n$$（输入序列长度）；在 NMT 语境中，键和值都是编码器隐藏状态。在解码器中，先前的输出被压缩成一个**查询（query）**（维度为 $$m$$ 的 $$\mathbf{Q}$$），通过映射该查询与键值集合来产生下一个输出。

Transformer 采用[缩放点积注意力](#summary)：输出是值的加权和，其中分配给每个值的权重由查询与所有键的点积确定：

$$
\text{Attention}(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = \text{softmax}(\frac{\mathbf{Q}\mathbf{K}^\top}{\sqrt{n}})\mathbf{V}
$$

### 多头自注意力

![multi-head scaled dot-product attention](https://lilianweng.github.io/posts/2018-06-24-attention/multi-head-attention.png)

*图 14：多头缩放点积注意力机制。（图片来源：[Vaswani, et al., 2017](http://papers.nips.cc/paper/7181-attention-is-all-you-need.pdf) 图 2）*

多头机制不是只计算一次注意力，而是并行地多次运行缩放点积注意力。各独立的注意力输出被简单地拼接并线性变换到期望的维度。我猜测其动机是集成总是有帮助的？;) 用论文的话说：*"多头注意力允许模型联合关注不同位置上不同表示**子空间**的信息。单个注意力头做平均会抑制这一点。"*

$$
\begin{aligned}
\text{MultiHead}(\mathbf{Q}, \mathbf{K}, \mathbf{V}) &= [\text{head}_1; \dots; \text{head}_h]\mathbf{W}^O \\
\text{where head}_i &= \text{Attention}(\mathbf{Q}\mathbf{W}^Q_i, \mathbf{K}\mathbf{W}^K_i, \mathbf{V}\mathbf{W}^V_i)
\end{aligned}
$$

其中 $$\mathbf{W}^Q_i$$、$$\mathbf{W}^K_i$$、$$\mathbf{W}^V_i$$ 和 $$\mathbf{W}^O$$ 是待学习的参数矩阵。

### 编码器

![Transformer encoder](https://lilianweng.github.io/posts/2018-06-24-attention/transformer-encoder.png)

*图 15：Transformer 的编码器。（图片来源：[Vaswani, et al., 2017](http://papers.nips.cc/paper/7181-attention-is-all-you-need.pdf)）*

编码器生成基于注意力的表示，能够从潜在无限大的上下文中定位特定信息。
- 一叠 N=6 个相同的层。
- 每层有一个**多头自注意力层**和一个简单的逐位置**全连接前馈网络**。
- 每个子层采用[**残差**](https://arxiv.org/pdf/1512.03385.pdf)连接和层**归一化**。
所有子层输出的数据维度相同，$$d_\text{model} = 512$$。

### 解码器

![Transformer decoder](https://lilianweng.github.io/posts/2018-06-24-attention/transformer-decoder.png)

*图 16：Transformer 的解码器。（图片来源：[Vaswani, et al., 2017](http://papers.nips.cc/paper/7181-attention-is-all-you-need.pdf)）*

解码器能够从编码表示中检索。
- 一叠 N = 6 个相同的层
- 每层有两个多头注意力子层和一个全连接前馈网络子层。
- 与编码器类似，每个子层采用残差连接和层归一化。
- 第一个多头注意力子层被**修改**以防止位置关注后续位置，因为在预测当前位置时我们不想偷看目标序列的未来。

### 完整架构

最后是 Transformer 架构的完整视图：
- 源序列和目标序列都先经过嵌入层，产生维度相同（$$d_\text{model} =512$$）的数据。
- 为保留位置信息，应用基于正弦波的位置编码并与嵌入输出相加。
- 最终解码器输出后接 softmax 和线性层。

![Transformer model](https://lilianweng.github.io/posts/2018-06-24-attention/transformer.png)

*图 17：Transformer 的完整模型架构。（图片来源：[Vaswani, et al., 2017](http://papers.nips.cc/paper/7181-attention-is-all-you-need.pdf) 图 1 与图 2。）*

实现 Transformer 模型是一次有趣的经历，这是我的实现：[lilianweng/transformer-tensorflow](https://github.com/lilianweng/transformer-tensorflow)。感兴趣的话请阅读代码中的注释。

## SNAIL

Transformer 没有循环或卷积结构，即使在嵌入向量上加了位置编码，序列顺序也只被弱性地纳入。对于像[强化学习](https://lilianweng.github.io/posts/2018-02-19-rl-overview/)这样对位置依赖敏感的问题，这可能是个大问题。

**简单神经注意力[元学习器](http://bair.berkeley.edu/blog/2017/07/18/learning-to-learn/)（Simple Neural Attention Meta-Learner，SNAIL）**（[Mishra et al., 2017](http://metalearning.ml/papers/metalearn17_mishra.pdf)）的提出部分就是为了解决 Transformer 模型中的[定位](#full-architecture)问题，做法是把 Transformer 中的自注意力机制与[时间卷积](https://deepmind.com/blog/wavenet-generative-model-raw-audio/)相结合。它已被证明在监督学习和强化学习任务上都表现出色。

![SNAIL](https://lilianweng.github.io/posts/2018-06-24-attention/snail.png)

*图 18：SNAIL 模型架构（图片来源：[Mishra et al., 2017](http://metalearning.ml/papers/metalearn17_mishra.pdf)）*

SNAIL 诞生于元学习领域——那是另一个值得单独成文的大话题。但简单说，元学习模型被期望能泛化到相似分布中新颖、未见过的任务。感兴趣可以读[这篇](http://bair.berkeley.edu/blog/2017/07/18/learning-to-learn/)不错的介绍。

## 自注意力 GAN

*Self-Attention GAN*（**SAGAN**；[Zhang et al., 2018](https://arxiv.org/pdf/1805.08318.pdf)）把自注意力层加入 [GAN](https://lilianweng.github.io/posts/2017-08-20-gan/)，使生成器和判别器都能更好地建模空间区域之间的关系。

经典的 [DCGAN](https://arxiv.org/abs/1511.06434)（Deep Convolutional GAN）把判别器和生成器都表示为多层卷积网络。然而，网络的表示能力受限于滤波器大小，因为单个像素的特征被限制在一个小的局部区域内。为了连接相距很远的区域，特征必须经过多层卷积操作稀释传递，且依赖关系不保证得以保持。

由于视觉语境中的（软）自注意力被设计为显式学习一个像素与所有其他位置（哪怕是相距很远的区域）之间的关系，它能轻松捕捉全局依赖。因此装备了自注意力的 GAN 被*期待能更好地处理细节*，太棒了！

![Conv vs self-attention on images](https://lilianweng.github.io/posts/2018-06-24-attention/conv-vs-self-attention.png)

*图 19：卷积操作与自注意力能访问的区域大小差异悬殊。*

SAGAN 采用[非局部神经网络](https://arxiv.org/pdf/1711.07971.pdf)来应用注意力计算。卷积图像特征图 $$\mathbf{x}$$ 分出三份拷贝，对应 Transformer 中[键、值、查询](#key-value-and-query)的概念：
- Key: $$f(\mathbf{x}) = \mathbf{W}_f \mathbf{x}$$
- Query: $$g(\mathbf{x}) = \mathbf{W}_g \mathbf{x}$$
- Value: $$h(\mathbf{x}) = \mathbf{W}_h \mathbf{x}$$

然后应用点积注意力输出自注意力特征图：

$$
\begin{aligned}
\alpha_{i,j} &= \text{softmax}(f(\mathbf{x}_i)^\top g(\mathbf{x}_j)) \\
\mathbf{o}_j &= \mathbf{W}_v \Big( \sum_{i=1}^N \alpha_{i,j} h(\mathbf{x}_i) \Big)
\end{aligned}
$$

![SAGAN](https://lilianweng.github.io/posts/2018-06-24-attention/SAGAN.png)

*图 20：SAGAN 中的自注意力机制。（图片来源：[Zhang et al., 2018](https://arxiv.org/abs/1805.08318) 图 2）*

注意 $$\alpha_{i,j}$$ 是注意力图中的一个条目，指示模型在合成第 $$j$$ 个位置时应给予第 $$i$$ 个位置多少注意力。$$\mathbf{W}_f$$、$$\mathbf{W}_g$$ 和 $$\mathbf{W}_h$$ 都是 1x1 卷积滤波器。如果你觉得 1x1 卷积听起来是个奇怪的概念（即，这不就是把整个特征图乘一个数吗？），请看 Andrew Ng 的这个短[教程](https://www.coursera.org/lecture/convolutional-neural-networks/networks-in-networks-and-1x1-convolutions-ZTb8x)。输出 $$\mathbf{o}_j$$ 是最终输出 $$\mathbf{o}= (\mathbf{o}_1, \mathbf{o}_2, \dots, \mathbf{o}_j, \dots, \mathbf{o}_N)$$ 的一个列向量。

此外，注意力层的输出乘以一个尺度参数并加回原始输入特征图：

$$
\mathbf{y} = \mathbf{x}_i + \gamma \mathbf{o}_i
$$

在训练期间，尺度参数 $$\gamma$$ 从 0 逐渐增大，网络被配置为先依赖局部区域的线索，然后逐渐学会把更多权重分配给更远的区域。

![SAGAN examples](https://lilianweng.github.io/posts/2018-06-24-attention/SAGAN-examples.png)

*图 21：SAGAN 为不同类别生成的 128×128 示例图像。（图片来源：[Zhang et al., 2018](https://arxiv.org/pdf/1805.08318.pdf) 图 6 局部）*

---

引用格式：
```
@article{weng2018attention,
  title   = "Attention? Attention!",
  author  = "Weng, Lilian",
  journal = "lilianweng.github.io/lil-log",
  year    = "2018",
  url     = "http://lilianweng.github.io/lil-log/2018/06/24/attention-attention.html"
}
```
*如果你发现本文中的错误，请毫不犹豫地联系我 [lilian dot wengweng at gmail dot com]，我会非常乐意立即修正！*

下一篇文章见 :D

## 参考文献

[1] ["Attention and Memory in Deep Learning and NLP."](http://www.wildml.com/2016/01/attention-and-memory-in-deep-learning-and-nlp/) - Jan 3, 2016 by Denny Britz

[2] ["Neural Machine Translation (seq2seq) Tutorial"](https://github.com/tensorflow/nmt)

[3] Dzmitry Bahdanau, Kyunghyun Cho, and Yoshua Bengio. ["Neural machine translation by jointly learning to align and translate."](https://arxiv.org/pdf/1409.0473.pdf) ICLR 2015.

[4] Kelvin Xu, Jimmy Ba, Ryan Kiros, Kyunghyun Cho, Aaron Courville, Ruslan Salakhudinov, Rich Zemel, and Yoshua Bengio. ["Show, attend and tell: Neural image caption generation with visual attention."](http://proceedings.mlr.press/v37/xuc15.pdf) ICML, 2015.

[5] Ilya Sutskever, Oriol Vinyals, and Quoc V. Le. ["Sequence to sequence learning with neural networks."](https://papers.nips.cc/paper/5346-sequence-to-sequence-learning-with-neural-networks.pdf) NIPS 2014. 

[6] Thang Luong, Hieu Pham, Christopher D. Manning. ["Effective Approaches to Attention-based Neural Machine Translation."](https://arxiv.org/pdf/1508.04025.pdf) EMNLP 2015.

[7] Denny Britz, Anna Goldie, Thang Luong, and Quoc Le. ["Massive exploration of neural machine translation architectures."](https://arxiv.org/abs/1703.03906) ACL 2017.

[8] Ashish Vaswani, et al. ["Attention is all you need."](http://papers.nips.cc/paper/7181-attention-is-all-you-need.pdf) NIPS 2017.

[9] Jianpeng Cheng, Li Dong, and Mirella Lapata. ["Long short-term memory-networks for machine reading."](https://arxiv.org/pdf/1601.06733.pdf) EMNLP 2016.

[10] Xiaolong Wang, et al. ["Non-local Neural Networks."](https://arxiv.org/pdf/1711.07971.pdf) CVPR 2018

[11] Han Zhang, Ian Goodfellow, Dimitris Metaxas, and Augustus Odena. ["Self-Attention Generative Adversarial Networks."](https://arxiv.org/pdf/1805.08318.pdf) arXiv preprint arXiv:1805.08318 (2018). 

[12] Nikhil Mishra, Mostafa Rohaninejad, Xi Chen, and Pieter Abbeel. ["A simple neural attentive meta-learner."](https://arxiv.org/abs/1707.03141) ICLR 2018.

[13] ["WaveNet: A Generative Model for Raw Audio"](https://deepmind.com/blog/wavenet-generative-model-raw-audio/) - Sep 8, 2016 by DeepMind.

[14]  Oriol Vinyals, Meire Fortunato, and Navdeep Jaitly. ["Pointer networks."](https://arxiv.org/abs/1506.03134) NIPS 2015.

[15] Alex Graves, Greg Wayne, and Ivo Danihelka. ["Neural turing machines."](https://arxiv.org/abs/1410.5401) arXiv preprint arXiv:1410.5401 (2014).
