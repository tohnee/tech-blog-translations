---
title: "如何在多块 GPU 上训练超大的深度模型？"
title_en: "How to Train Really Large Models on Many GPUs?"
source: https://lilianweng.github.io/posts/2021-09-25-train-large/
crawled: 2026-09-08
translated: 2026-09-08
---

# 如何在多块 GPU 上训练超大的深度模型？

> 原文：[How to Train Really Large Models on Many GPUs?](https://lilianweng.github.io/posts/2021-09-25-train-large/) · Lilian Weng（翁荔）

> 如何训练大而深的神经网络颇具挑战，因为它需要大量 GPU 内存和漫长的训练时间。本文回顾几种流行的训练并行范式，以及多种模型架构与省内存设计，使跨大量 GPU 训练超大神经网络成为可能。

近年来，更大的预训练[语言模型](https://lilianweng.github.io/posts/2019-01-31-lm/)在许多 NLP 基准任务上带来更好的结果。如何训练大而深的神经网络颇具挑战，因为它需要大量 GPU 内存和漫长的训练时间。

然而单块 GPU worker 的内存有限，许多大模型的规模已超出单块 GPU。有几种并行范式可实现跨多块 GPU 的模型训练，还有多种模型架构与省内存设计，帮助使训练*超大*神经网络成为可能。

## 训练并行

训练超大神经网络模型的主要瓶颈是对大量 GPU 内存的强烈需求，远超单台 GPU 机器所能容纳。除模型权重（如数百亿个浮点数）外，存储中间计算输出（如梯度和优化器状态，如 Adam 的动量与方差）通常甚至更昂贵。此外，训练大模型往往伴随大训练语料，单进程可能要跑到天荒地老。

因此，并行是必需的。并行可以发生在不同维度上，包括数据、模型架构和张量运算。

### 数据并行

**数据并行（Data parallelism，DP）**最朴素的方式是把相同模型权重复制到多个 worker，给每个 worker 分配一小份数据同时处理。

若模型大小超过单个 GPU 节点的内存，朴素 DP 无法很好工作。像 *GeePS*（[Cui et al. 2016](https://www.pdl.cmu.edu/PDL-FTP/CloudComputing/GeePS-cui-eurosys16.pdf)）这样的方法把暂时不用的参数卸载回 CPU，以便模型大到装不进一台机器时在有限 GPU 内存下工作。数据换入换出的传输应在后台发生，不干扰训练计算。

每个 minibatch 结束时，worker 需要同步梯度或权重以避免陈旧。有两种主要同步方式，各有明显优缺点。
1. *批量同步并行（Bulk synchronous parallels，BSP）*：worker 在每个 minibatch 结束时同步数据。它防止模型权重陈旧、学习效率好，但每台机器必须停下等待其他机器发送梯度。
2. *异步并行（Asynchronous parallel，ASP）*：每个 GPU worker 异步处理数据，无等待无停顿。然而它容易导致使用陈旧权重，从而降低统计学习效率。尽管它增加了计算时间，可能并未加速收敛所需的训练时间。

折中方案是每 $$x$$ 次迭代（$$x > 1$$）全局同步一次梯度。这一特性在 Pytorch v1.5 起的 Distributed Data Parallel（[DDP](https://pytorch.org/tutorials/intermediate/ddp_tutorial.html)）中称为"梯度累积"（[Li et al. 2021](https://arxiv.org/abs/2006.15704)）。梯度分桶避免立即执行 `AllReduce` 操作，而是把多个梯度装进一个桶做一次 `AllReduce` 以提高吞吐。可以基于计算图做计算与通信的调度优化。

![Pytorch DDP](https://lilianweng.github.io/posts/2021-09-25-train-large/pytorch-ddp.png)

*图 1：Pytorch DDP 的伪代码。（图片来源：[Li et al. 2021](https://arxiv.org/abs/2006.15704)）*

### 模型并行

**模型并行（Model parallelism，MP）**旨在解决模型权重装不进单节点的情况。计算与模型参数被分区到多台机器。与每个 worker 持有整个模型完整副本的数据并行不同，MP 只在一个 worker 上分配一小部分模型参数，因此内存使用和计算都减少了。

由于深度神经网络通常包含垂直层堆叠，按层切分大模型（把一小段连续层归入一个 worker 上的一个分区）看起来很直接。然而，让每个数据批次穿过多个这样顺序依赖的 worker 的朴素实现，会导致巨大的等待时间"气泡"和计算资源的严重利用不足。

![Naive DP](https://lilianweng.github.io/posts/2021-09-25-train-large/naive-data-parallelism.png)

*图 2：朴素的模型并行设定，模型被垂直切成 4 个分区。由于顺序依赖，数据一次只被一个 worker 处理，导致大片空闲时间"气泡"。（图片来源：[Huang et al. 2019](https://arxiv.org/abs/1811.06965)）*

### 流水线并行

**流水线并行（Pipeline parallelism，PP）**结合模型并行与数据并行以减少低效的时间"气泡"。主要思想是把一个 minibatch 拆成多个 microbatch，使每个阶段的 worker 能同时处理一个 microbatch。注意每个 microbatch 需要两趟：一趟前向、一趟反向。worker 间通信只传输激活（前向）和梯度（反向）。这些趟如何调度、梯度如何聚合在不同方法中各不相同。分区（worker）数也称*流水线深度*。

在 *GPipe*（[Huang et al. 2019](https://arxiv.org/abs/1811.06965)）中，多个 microbatch 的梯度被聚合并在结束时同步应用。同步梯度下降保证了学习的一致性与效率，与 worker 数量无关。如图 3 所示，气泡仍存在但比图 2 小得多。给定 $$m$$ 个均分的 microbatch 和 $$d$$ 个分区，假设每个 microbatch 的前向和反向各占一个单位时间，气泡占比为：

$$
1 - \frac{2md}{(2m + 2(d-1))d} = \frac{d-1}{m+d-1}
$$

GPipe 论文观察到，若 microbatch 数超过分区数的 4 倍（$$m > 4d$$，当应用[激活重计算](#activation-recomputation)时），气泡开销几乎可以忽略。

![GPipe](https://lilianweng.github.io/posts/2021-09-25-train-large/gpipe.png)

*图 3：GPipe 流水线并行示意（4 个 microbatch、4 个分区）。GPipe 在每批次结束时跨设备同步地聚合并更新梯度。（图片来源：[Huang et al. 2019](https://arxiv.org/abs/1811.06965)）*

尽管不总是有保证（若模型参数未在 worker 间均匀分布），GPipe 在吞吐上随设备数接近线性加速。

*PipeDream*（[Narayanan et al. 2019](https://cs.stanford.edu/~matei/papers/2019/sosp_pipedream.pdf)）调度每个 worker 交替处理前向和反向趟（`1F1B`）。
PipeDream 把每个模型分区命名为"阶段（stage）"，每个阶段 worker 可以有多个副本以运行数据并行。此过程中，PipeDream 使用确定性的轮询负载均衡策略在阶段的多个副本间分配工作，确保同一 minibatch 的前向与反向趟发生在同一副本上。

![PipeDream](https://lilianweng.github.io/posts/2021-09-25-train-large/pipedream.png)

*图 4：PipeDream 中 `1F1B` microbatch 调度示意。（图片来源：[Harlap et al. 2018](https://arxiv.org/abs/1806.03377)）*

由于 PipeDream 没有跨所有 worker 的批次结束全局梯度同步，1F1B 的朴素实现容易导致一个 microbatch 的前向与反向趟使用不同版本的模型权重，从而降低学习效率。PipeDream 提出了几个设计来解决该问题：
- *权重储藏（Weight stashing）*：每个 worker 跟踪多个模型版本，确保同一数据批次的前向与反向趟使用同一版本权重。
- *垂直同步（Vertical sync）*（可选）：模型权重版本随激活和梯度在阶段 worker 间流动。然后计算采用从上一 worker 传播来的相应储藏版本。该过程保持跨 worker 的版本一致性。注意它与 GPipe 不同，是异步的。

训练运行开始时，PipeDream 先剖析模型中每层的计算内存成本与时间，然后优化一个把层分区到各阶段的解——这是一个动态规划问题。

![PipeDream experiments](https://lilianweng.github.io/posts/2021-09-25-train-large/pipedream-results.png)

*图 5：VGG16 在 ILSVRC12 上的结果。（上）准确率 vs 时间。整数标记阶段 worker 数。ASP = 异步并行，BSP = 批量同步并行。（下）不同并行配置的训练时间加速比。Straight pipeline 指不带数据并行的流水线并行。（图片来源：[Harlap et al. 2018](https://arxiv.org/abs/1806.03377)）*

后来提出了 PipeDream 的两个变体，以减少储藏模型版本的内存占用（[Narayanan et al. 2021](https://arxiv.org/abs/2006.09503)）。

*PipeDream-flush* 周期性地加入全局同步的流水线冲刷（flush），就像 GPipe。这样，它以牺牲一点吞吐为代价大幅减少了内存占用（即只维护单一版本的模型权重）。

![PipeDream-flush](https://lilianweng.github.io/posts/2021-09-25-train-large/pipedream-flush.png)

*图 6：PipeDream-flush 中流水线调度示意。（图片来源：[Narayanan et al. 2021](https://arxiv.org/abs/2006.09503)）*

*PipeDream-2BW* 只维护两个版本的模型权重，"2BW" 是 "double-buffered weights" 的缩写。它每 $$k$$ 个 microbatch 生成一个新模型版本，$$k$$ 应大于流水线深度 $$d$$，即 $$k > d$$。新更新的模型版本不能立即完全替换旧版本，因为一些遗留的反向趟仍依赖旧版本。总共只需保存两个版本，内存开销大幅降低。

![PipeDream-2BW](https://lilianweng.github.io/posts/2021-09-25-train-large/pipedream-2bw.png)

*图 7：PipeDream-2BW 中流水线调度示意。（图片来源：[Narayanan et al. 2021](https://arxiv.org/abs/2006.09503)）*

### 张量并行

模型并行与流水线并行都垂直切分模型。另一方面，我们可以把单个张量运算的计算水平分区到多个设备，称为**张量并行（Tensor parallelism，TP）**。

鉴于 Transformer 的流行，以它为例。Transformer 模型主要由多层 MLP 与自注意力块组成。*Megatron-LM*（[Shoeybi et al. 2020](https://arxiv.org/abs/1909.08053)）采用简单的方式对 MLP 与自注意力做层内计算并行。

Transformer 中的 MLP 层包含一个 GEMM（通用矩阵乘）后接非线性 GeLU 变换。按列拆分权重矩阵 $$A$$：

$$
\begin{aligned}
\text{Split }A &= [A_1, A_2] \\
Y &=\text{GeLU}(XA) \\
[Y_1, Y_2] &= [\text{GeLU}(XA_1), \text{GeLU}(XA_2)]
\end{aligned}
$$

注意力块按上述分区并行地对查询（$$Q$$）、键（$$K$$）、值权重（$$V$$）运行 GEMM，然后用另一个 GEMM 组合它们产生注意力头结果。

$$
\text{Attention}(X, Q, K, V) = \text{softmax}(\frac{(XQ) (XK)^\top}{\sqrt{d_k}}) XV
$$

![Megatron LM](https://lilianweng.github.io/posts/2021-09-25-train-large/Megatron-LM.png)

*图 8：Megatron-LM 提出的 Transformer 关键组件张量并行示意。（图片来源：[Shoeybi et al. 2020](https://arxiv.org/abs/1909.08053)）*

[Narayanan et al. (2021)](https://arxiv.org/abs/2104.04473) 把流水线、张量与数据并行与一种新的流水线调度策略相结合，命名为 *PTD-P*。不同于只把一段连续层（"模型块"）放在一个设备上，每个 worker 可被分配多个更小的连续层子集块（如设备 1 有层 1、2、9、10；设备 2 有层 3、4、11、12；各有两个模型块）。一个批次中的 microbatch 数应能被 worker 数整除（$$m % d = 0$$）。若每个 worker 有 $$v$$ 个模型块，相比 GPipe 调度，流水线气泡时间可缩减 $$v$$ 倍。

![PTD-P](https://lilianweng.github.io/posts/2021-09-25-train-large/PTD-P-interleaved.png)

*图 9：（上）PipeDream-flush 中的默认 `1F1B` 流水线调度。（下）交错式 1F1B 流水线调度。第一组模型块为深色，第二组为浅色。（图片来源：[Narayanan et al. 202](https://arxiv.org/abs/2104.04473)）*

## 专家混合（MoE）

**专家混合（Mixture-of-Experts，MoE）**方法近来备受关注，因为研究者（主要来自 Google）试图推动模型尺寸的极限。思想的核心是[集成学习](https://en.wikipedia.org/wiki/Ensemble_learning)：*多个弱学习器的组合给你一个强学习器！*

在一个深度神经网络内，集成可以用连接多个专家的门控机制实现（[Shazeer et al., 2017](https://arxiv.org/abs/1701.06538)）。门控机制控制网络的哪个子集（如哪些专家）应被激活以产生输出。论文称之为"稀疏门控专家混合（sparsely gated mixture-of-experts，MoE）"层。

确切地说，一个 MoE 层包含
- $$n$$ 个作为专家的前馈网络 $$\{E_i\}^n_{i=1}$$
- 一个可训练的门控网络 $$G$$，学习 $$n$$ 个专家上的概率分布，以便把流量路由到少数被选中的专家。

取决于门控输出，并非每个专家都必须被评估。当专家数量太大时，可以考虑使用两层层级 MoE。

![MoE](https://lilianweng.github.io/posts/2021-09-25-train-large/moe.png)

*图 10：专家混合（MoE）层示意。$$n$$ 个专家中只有 2 个被门控网络选中并激活。（图片来源：[Shazeer et al., 2017](https://arxiv.org/abs/1701.06538)）*

$$G$$ 的一个简单选择是把输入乘以可训练权重矩阵 $$G_g$$ 再做 softmax：$$G_\sigma (x) = \text{softmax}(x W_g)$$。然而这产生稠密的门控控制向量，无助于节省计算资源，因为只有当 $$G^{(i)}(x)=0$$ 时我们才无须评估某专家。因此 MoE 层只保留前 $$k$$ 个值。它还向 $$G$$ 加入可调高斯噪声以改善负载均衡。该机制称为*噪声 top-k 门控（noisy top-k gating）*。

$$
\begin{aligned} 
G(x) &= \text{softmax}( \text{topk}(H(x), k)) \\
H^{(i)}(x) &= (xW_g)^{(i)} + \epsilon \cdot \text{softplus}((xW_\text{noise})^{(i)} ); \quad \epsilon \sim \mathcal{N}(0, \mathbf{1}) \\
\text{topk}^{(i)}(v, k) &= \begin{cases} v^{(i)} & \text{if }v^{(i)}\text{ is in the top }k\text{ elements of }v \\ -\infty & \text{otherwise} 
\end{cases} 
\end{aligned}
$$

其中上标 $$v^{(i)}$$ 表示向量 $$v$$ 的第 i 维。函数 $$\text{topk}(., k)$$ 把其他维设为 $$-\infty$$，选出值最高的前 $$k$$ 维。

为避免门控网络一直偏爱少数强专家的自增强效应，[Shazeer et al. (2017)](https://arxiv.org/abs/1701.06538) 通过额外的重要性损失提出一个软约束，鼓励所有专家拥有相同权重。它等价于每专家批平均值[变异系数](https://en.wikipedia.org/wiki/Coefficient_of_variation)的平方。

$$
L_\text{aux} = w_\text{aux} \cdot \text{CV}(\sum_{x \in X} G(x))^2
$$

其中 $$\text{CV}$$ 是变异系数，损失权重 $$w_\text{aux}$$ 是待调超参数。

由于每个专家网络只得到一部分训练样本（"缩批问题"），我们在 MoE 中应尽量用大的 batch size。但它受 GPU 内存限制。可以应用数据并行与模型并行来提升吞吐。

![MoE experiments](https://lilianweng.github.io/posts/2021-09-25-train-large/moe-experiments.png)

*图 11：1-Billion-Word 语言建模基准上的测试困惑度。（左）模型容量从左到右递增，含 4、32、256、256、1024、4096 个专家。（右）左图中最大的 40 亿参数 MoE 模型在不同计算预算下的性能。（图片来源：[Shazeer et al., 2017](https://arxiv.org/abs/1701.06538)）*

**GShard**（[Lepikhin et al., 2020](https://arxiv.org/abs/2006.16668)）用分片把 MoE transformer 模型扩展到 6000 亿参数。MoE transformer 把每隔一个的前馈层替换为 MoE 层。*分片 MoE transformer* 只把 MoE 层分片到多台机器，其他层简单复制。

GShard 中门控函数 $$G$$ 有若干改进设计：
- *专家容量（Expert capacity）*：流经一个专家的 token 数不应超过阈值，称为"专家容量"。若一个 token 被路由到已达容量的专家，该 token 被标记为"溢出"，门控输出改为零向量。
- *局部组分发（Local group dispatching）*：token 被均分到多个局部组，专家容量按组施加。
- *辅助损失*：动机类似原始 MoE 辅助损失。他们添加辅助损失以最小化路由到每个专家的数据比例的均方。
- *随机路由*：第 2 好的专家以与其权重成正比的概率被选中；否则 GShard 按随机路由，以加入一些随机性。

![GShard algorithm](https://lilianweng.github.io/posts/2021-09-25-train-large/gshard-algo.png)

*图 12：GShard 中带辅助损失的组级 top-2 门控机制伪代码。（图片来源：[Lepikhin et al., 2020](https://arxiv.org/abs/2006.16668)）*

**Switch Transformer**（[Fedus et al. 2021](https://arxiv.org/abs/2101.03961)）把稠密前馈层替换为*稀疏 switch FFN 层*（每个输入只路由到*一个*专家网络），把模型规模扩展到万亿参数（！！）。负载均衡的辅助损失为 $$\text{loss}_\text{aux} = w_\text{aux} \sum_{i=1}^n f_i p_i$$（给定 $$n$$ 个专家），其中 $$f_i$$ 是路由到第 $$i$$ 个专家的 token 比例，$$p_i$$ 是门控网络预测的专家 $$i$$ 的路由概率。

![Switch transformer](https://lilianweng.github.io/posts/2021-09-25-train-large/switch-transformer.png)

*图 13：Switch transformer。稀疏 switch FFN 层在蓝色框中。（图片来源：[Fedus et al. 2021](https://arxiv.org/abs/2101.03961)）*

为提升训练稳定性，Switch Transformer 融入了以下设计：
- *选择性精度*。他们表明，只把模型的一小部分局部地转为 FP32 精度能提升稳定性，同时避免 FP32 张量昂贵的通信开销。FP32 精度只在路由器函数体内部使用，结果再转回 FP16。
- *更小的初始化*。权重矩阵的初始化从截断正态分布采样，均值 $$\mu=0$$、标准差 $$\sigma = \sqrt{s/n}$$。他们还建议把 transformer 初始化尺度参数从 $$s=1$$ 降到 $$s=0.1$$。
- *更高的专家 dropout*。微调常在小数据集上进行。为避免过拟合，每个专家内的 dropout 率大幅提高。有趣的是，他们发现提高所有层的 dropout 导致差性能。论文中非专家层用 0.1 的 dropout 率，而专家 FF 层内用 0.4。

Switch Transformer 论文用一张漂亮的图总结了训练大模型的不同数据与模型并行策略：

![Parallelism strategies](https://lilianweng.github.io/posts/2021-09-25-train-large/switch-transformer-parallelism.png)

*图 14：各种并行策略如何把（上）模型权重与（下）数据切分到多个 GPU 核的示意。上排中每种颜色表示一个唯一的权重矩阵；下排中不同颜色表示不同的 token 集。（图片来源：[Fedus et al. 2021](https://arxiv.org/abs/2101.03961)）*

## 其他省内存设计

### CPU 卸载

当 GPU 内存满时，一个选择是把暂时不用的数据卸载到 CPU，稍后需要时再读回（[Rhu et al. 2016](https://arxiv.org/abs/1602.08124)）。**CPU 卸载（CPU offloading）**的想法直接，但近年不太流行，因为它拖慢训练时间。

### 激活重计算

**激活重计算（Activation recomputation**，也称"激活检查点"或"梯度检查点"；[Chen et al. 2016](https://arvix.org/abs/1604.06174)）是一个聪明而简单的想法：以计算时间为代价减少内存占用。它把训练一个 $$\ell$$ 层深度神经网络的内存开销降到 $$O(\sqrt{\ell})$$，每批次只额外消耗一次额外的前向计算。

设我们把 $$\ell$$ 层网络均分为 $$d$$ 个分区。只保存分区边界处的激活并在 worker 间通信。分区内各层的中间激活在计算梯度时仍然需要，因此在反向趟中重算。用激活重计算，训练的内存开销 $$M(\ell)$$ 为：

$$
M(\ell) 
=\max_{i=1,\dots,k} \underbrace{\text{cost-of-one-partition}(i)}_\text{cost of back-propagation on the i-th partition} + \underbrace{O(d)}_\text{store intermediate outputs} 
= O(\frac{\ell}{d}) + O(d)
$$

在 $$d=\sqrt{\ell}$$ 时取得最小开销 $$O(\sqrt{\ell})$$。

激活重计算技巧可以做到内存开销相对模型规模是次线性的。

![Activation checkpointing experiments](https://lilianweng.github.io/posts/2021-09-25-train-large/activation-checkpointing.png)

*图 15：不同省内存算法的内存开销。<u>Sharing</u>：不再需要时回收中间结果占用的内存。<u>Inplace</u>：把输出直接存进某输入值的内存。（图片来源：[Chen et al. 2016](https://arvix.org/abs/1604.06174)）*

### 混合精度训练

[Narang & Micikevicius et al. (2018)](https://arxiv.org/abs/1710.03740) 介绍了一种用半精度浮点（FP16）数训练模型而不损失模型精度的方法。

![Mixed-precision training](https://lilianweng.github.io/posts/2021-09-25-train-large/mixed-precision-training.png)

*图 16：一层上混合精度训练的流程。（图片来源：[Narang & Micikevicius, et al. 2018](https://arxiv.org/abs/1710.03740)）*

避免半精度下丢失关键信息的三项技术：
- *权重的全精度主副本*。维护累积梯度的全精度（FP32）模型权重副本。数值舍入到半精度用于前向与反向趟。动机是每次梯度更新（梯度乘学习率）可能太小而无法完全容纳于 FP16 范围（即 $$2^{-24}$$ 在 FP16 中变为零）。
- *损失缩放*。放大损失以更好地处理小幅度梯度（见图 16）。放大梯度帮助把它们移到可表示范围中靠右（含更大值）的更大区段，保住否则会丢失的值。
- *算术精度*。对常见网络算术（如向量点积、向量元素求和归约），我们可以在 FP32 中累积部分结果，然后在存入内存前把最终输出存为 FP16。逐点操作可以在 FP16 或 FP32 中执行。

![Gradient histogram](https://lilianweng.github.io/posts/2021-09-25-train-large/gradient-histogram.png)

*图 17：全精度梯度的直方图。模型切换到 FP16 后，左侧直到 $$2^{-24}$$ 的部分将被清零。（图片来源：[Narang & Micikevicius, et al. 2018](https://arxiv.org/abs/1710.03740)）*

他们的实验中，一些网络（如图像分类、Faster R-CNN）不需要损失缩放，但另一些（如 Multibox SSD、大 LSTM 语言模型）必需。

### 压缩

中间结果常常消耗大量内存，尽管它们只在一趟前向和一趟反向中需要。这两次使用之间有明显的时间间隔。因此 [Jain et al. (2018)](https://www.microsoft.com/en-us/research/uploads/prod/2018/04/fiddle-gist-isca18.pdf) 提出数据编码策略：第一趟首次使用后压缩中间结果，稍后为反向传播再解码回来。

他们的系统 *Gist* 融入两种编码方案：
*层特定的无损编码*；聚焦 ReLU-Pool（"二值化"）与 ReLU-Conv（"稀疏存储、稠密计算"）模式。
*激进的有损编码*；使用延迟精度降低（DPR）。他们观察到特征图的第一次即时使用应保持高精度，但第二次使用可容忍较低精度。

实验表明，Gist 在 5 个 SOTA 图像分类 DNN 上能把内存开销降低 2 倍，平均 1.8 倍，性能开销仅 4%。

### 内存高效优化器

优化器对内存的消耗很可观。以流行的 Adam 优化器为例，它内部需要维护动量和方差，二者都与梯度和模型参数同规模。一转眼，我们就需要保存 4 倍于模型权重的内存。

已有若干优化器被提出以减少内存占用。
例如，*Adafactor*（[Shazeer et al. 2018](https://arxiv.org/abs/1804.04235)）不像 Adam 那样存储完整的动量与方差，只跟踪滑动平均的行和与列和，然后基于这些和估计二阶矩。*SM3*（[Anil et al. 2019](https://arxiv.org/abs/1901.11150)）描述了另一种自适应优化方法，同样大幅减少内存。

*ZeRO*（*Zero Redundancy Optimizer*；[Rajbhandari et al. 2019](https://arxiv.org/abs/1910.02054)）基于对大模型训练两大内存消耗的观察，优化训练大模型的内存使用：
1. 大头被*模型状态*占据，包括优化器状态（如 Adam 动量与方差）、梯度和参数。混合精度训练需要大量内存，因为优化器除 FP16 版本外还需保存 FP32 参数副本和其他优化器状态。
2. 其余被激活、临时缓冲和不可用的碎片内存（论文中称*残余状态*）消耗。

ZeRO 结合两种方法：*ZeRO-DP* 与 *ZeRO-R*。
ZeRO-DP 是一种增强的数据并行，避免模型状态上的简单冗余。它把优化器状态、梯度和参数分区到多个数据并行进程，并通过动态通信调度最小化通信量。
ZeRO-R 优化残余状态的内存消耗，使用分区激活重计算、恒定缓冲区和即时内存碎片整理。

---
引用格式：
```
@article{weng2021large,
  title   = "How to Train Really Large Models on Many GPUs?",
  author  = "Weng, Lilian",
  journal = "lilianweng.github.io/lil-log",
  year    = "2021",
  url     = "https://lilianweng.github.io/lil-log/2021/09/24/train-large-neural-networks.html"
}
```

## 参考文献

[1] Li et al. ["PyTorch Distributed: Experiences on Accelerating Data Parallel Training"](https://arxiv.org/abs/2006.15704) VLDB 2020.

[2] Cui et al. ["GeePS: Scalable deep learning on distributed GPUs with a GPU-specialized parameter server"](https://www.pdl.cmu.edu/PDL-FTP/CloudComputing/GeePS-cui-eurosys16.pdf) EuroSys 2016 

[3] Shoeybi et al. ["Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism."](https://arxiv.org/abs/1909.08053) arXiv preprint arXiv:1909.08053 (2019).

[4] Narayanan et al. ["Efficient Large-Scale Language Model Training on GPU Clusters Using Megatron-LM."](https://arxiv.org/abs/2104.04473) arXiv preprint arXiv:2104.04473 (2021).

[5] Huang et al. ["GPipe: Efficient Training of Giant Neural Networks using Pipeline Parallelism."](https://arxiv.org/abs/1811.06965) arXiv preprint arXiv:1811.06965 (2018).

[6] Narayanan et al. ["PipeDream: Generalized Pipeline Parallelism for DNN Training."](https://cs.stanford.edu/~matei/papers/2019/sosp_pipedream.pdf) SOSP 2019.

[7] Narayanan et al.  ["Memory-Efficient Pipeline-Parallel DNN Training."](https://arxiv.org/abs/2006.09503) ICML 2021.

[8] Shazeer et al. ["The Sparsely-Gated Mixture-of-Experts Layer Noam."](https://arxiv.org/abs/1701.06538) arXiv preprint arXiv:1701.06538 (2017).

[9] Lepikhin et al. ["GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding."](https://arxiv.org/abs/2006.16668) arXiv preprint arXiv:2006.16668 (2020).

[10] Fedus et al. ["Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity."](https://arxiv.org/abs/2101.03961) arXiv preprint arXiv:2101.03961 (2021).

[11] Narang & Micikevicius, et al.  ["Mixed precision training."](https://arxiv.org/abs/1710.03740) ICLR 2018.

[12] Chen et al. 2016 ["Training Deep Nets with Sublinear Memory Cost."](https://arxiv.org/abs/1604.06174) arXiv preprint arXiv:1604.06174 (2016).

[13] Jain et al. ["Gist: Efficient data encoding for deep neural network training."](https://www.microsoft.com/en-us/research/uploads/prod/2018/04/fiddle-gist-isca18.pdf) ISCA 2018.

[14] Shazeer & Stern. ["Adafactor: Adaptive learning rates with sublinear memory cost."](https://arxiv.org/abs/1804.04235) arXiv preprint arXiv:1804.04235 (2018).

[15] Anil et al. ["Memory-Efficient Adaptive Optimization."](https://arxiv.org/abs/1901.11150) arXiv preprint arXiv:1901.11150 (2019).

[16] Rajbhandari et al. ["ZeRO: Memory Optimization Towards Training A Trillion Parameter Models Samyam."](https://arxiv.org/abs/1910.02054) arXiv preprint arXiv:1910.02054 (2019).
