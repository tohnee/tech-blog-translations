---
title: "短卷积（ShortConv）"
title_en: "Short Convolution (ShortConv)"
source: https://sebastianraschka.com/llm-architecture-gallery/shortconv/
crawled: 2026-09-06
translated: 2026-09-06
---

# 短卷积（ShortConv）

> 原文：[Short Convolution (ShortConv)](https://sebastianraschka.com/llm-architecture-gallery/shortconv/)

我觉得理解 ShortConv 最容易的方式，是暂时忽略整个模型：取一个隐藏通道，看四个相邻的 token 位置。ShortConv 把这四个值分别乘以四个可学习的权重再相加。本质上就是这么回事。

Kimi Linear 和 Inkling 都使用 4 的核大小。由于卷积是因果的，这四个位置就是当前 token 和之前的三个 token。

该卷积还是逐深度的（depthwise）：每个隐藏通道有自己的权重，跨通道的混合则由外围的线性投影负责。这两个模型在非常不同的位置使用了同一个操作。

[架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
[Kimi Linear 论文](https://arxiv.org/abs/2510.26692)
[Inkling 发布文章](https://thinkingmachines.ai/news/introducing-inkling/)

![四条并行的加权 token 路径汇入核大小为 4 的因果逐深度卷积输出](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/shortconv-kernel4-comparison.webp)

核大小为 4 的逐深度卷积，将当前 token 与之前三个位置分别乘以各自的逐通道权重，
然后把四个加权抽头求和。

局部感受野

核大小为 4 时，当前 token 加上之前三个位置

解码状态

一个大小固定的滚动状态，其大小不随上下文长度增长

示例架构

[Kimi Linear 48B-A3B](https://sebastianraschka.com/llm-architecture-gallery/#card-kimi-linear-48b-a3b) 和
[Inkling](https://sebastianraschka.com/llm-architecture-gallery/#card-inkling)

## 因果逐深度 ShortConv 的工作方式

对于单个通道 `c` 和核大小 `k`，位置 `t` 处的卷积为

```python
y[t, c] = Σᵢ w[c, i] · x[t - i, c]     for i = 0, ..., k - 1
```

"因果"意味着未来的 token 不可触及。在序列开头，缺失的更早取值补零。当 `k = 4` 时，四个输入是 `x[t]`、`x[t-1]`、`x[t-2]` 和 `x[t-3]`。

"逐深度"意味着通道 `c` 在这一步不会读取其他通道。稠密投影仍然可以在卷积之前或之后混合所有通道。

## 一个极简 PyTorch 版本

下面的代码实现了这个操作。激活和残差开关对应后文讨论的两种模型特定变体。

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class ShortConv(nn.Module):
    def __init__(self, d_model, kernel_size=4, activation=None, residual=False):
        super().__init__()
        self.kernel_size = kernel_size
        self.activation = activation
        self.residual = residual
        self.conv = nn.Conv1d(
            in_channels=d_model,
            out_channels=d_model,
            kernel_size=kernel_size,
            groups=d_model,
            bias=False,
            padding=kernel_size - 1,
        )

    def forward(self, x):
        # x has shape (batch, tokens, channels)
        y = self.conv(x.transpose(1, 2))
        y = y[:, :, : x.shape[1]].transpose(1, 2)

        if self.activation == "silu":
            y = F.silu(y)
        if self.residual:
            y = y + x
        return y
```

`Conv1d` 会在序列两侧填充。截断操作去除了依赖右侧填充的输出，从而保证结果是因果的。

## 这个操作为什么便宜

为什么要费心加这么一个小层？一个原因是成本低。对于 `T` 个 token、隐藏宽度 `d`、核大小 `k`，计算量大约是 `O(Tdk)`。当 `k = 4` 时，它随序列长度线性增长。

在推理时，模型用一个小的滚动状态保存最近的激活值。该状态大小为 `O(dk)`，不随上下文增长。ShortConv 负责局部混合，更大范围的检索仍由注意力承担。

## ShortConv 如何与 KDA 互补

卷积只是 Kimi Delta Attention（KDA）的一部分。KDA 是 Gated DeltaNet 的改进版，因此有必要简要看看这一循环注意力家族在做什么，以及为什么需要一个单独的局部混合步骤。

那么，什么是 Gated DeltaNet？Gated DeltaNet（Gated Delta Network 的缩写）是 Qwen3-Next 的线性注意力层，用作标准 softmax 注意力的替代。它取自《[Gated Delta Networks: Improving Mamba2 with Delta Rule](https://arxiv.org/abs/2412.06464)》论文。

Gated DeltaNet 最初作为 Mamba2 的改进版被提出，它把 Mamba2 的门控衰减机制与一个 delta 规则结合起来。delta 规则指的是计算新值与预测值之间的差（delta），用于更新一个作为记忆状态的隐藏状态。

KDA 修改了这一机制的部分内容（包括衰减门），但保留了循环状态更新的思想。在 Kimi Linear 中，ShortConv 就位于该更新之前。

在门控注意力中，模型先在所有 token 之间计算常规注意力（每个 token 都关注其他所有 token），然后在得到注意力输出后，由一个门（sigmoid）决定保留多少输出。关键在于，它仍然是随上下文长度二次增长的常规缩放点积注意力。

简单回顾一下：缩放点积注意力按 `softmax(QKᵀ)V` 计算，其中 Q 和 K 是 *n*×*d* 矩阵，*n* 是输入 token 数，*d* 是嵌入维度。`QKᵀ` 得到一个 *n*×*n* 的注意力矩阵，再与 *n*×*d* 的值矩阵 *V* 相乘。

在 Gated DeltaNet 中没有 *n*×*n* 的注意力矩阵。模型改为逐个处理 token，并维护一个随每个新 token 到来而更新的动态记忆（状态）。

这些门控制记忆如何变化：

- α（alpha）调节旧记忆被遗忘（衰减）多少
- β（beta）调节时间步 *t* 的当前 token 对记忆的更新幅度

最终的输出门与门控注意力类似，控制保留多少输出。

从某种意义上说，Gated DeltaNet 的这种状态更新与循环神经网络（RNN）的工作方式类似。其优势是随上下文长度线性扩展，而非二次扩展。

循环状态更新的缺点是，与常规注意力或门控注意力相比，它牺牲了来自完整成对注意力的全局上下文建模能力。Gated DeltaNet 仍能捕捉上下文，但必须经过记忆瓶颈。这块记忆大小固定因而更高效，但它像 RNN 一样把过去的上下文压缩进单个隐藏状态。

这正是 Kimi Linear 采用混合配置、而不是把每个注意力层都换成 KDA 的原因：它的 20 个 KDA 层负责高效的循环更新，7 个 MLA 层保留完整注意力式的检索。在 KDA 层内部，ShortConv 在循环更新之前增加了一条直接的四 token 混合路径。

在推理端也有类似的区分。ShortConv 只保留每个通道最近 `k - 1` 个激活值；循环注意力机制则保留其固定大小的记忆状态。两者都不随 token 数量增长，但用途不同：ShortConv 保存精确的局部激活值，而循环状态压缩的是跨越更长距离的信息。

除了线性计算复杂度之外，循环机制的另一大优势是节省内存，因为这些层不会让 KV 缓存增长。如前所述，它们维护的是固定大小的循环状态，因此内存不随上下文长度变化。

对于常规的多头注意力（MHA）层，KV 缓存大小可以这样计算：

```python
KV_cache_MHA ≈ batch_size × n_tokens × n_heads × d_head × 2 × bytes
```

系数 2 是因为要同时存储键和值。对于一个简化的 DeltaNet 层，状态大小为

```python
state_DeltaNet = batch_size × n_heads × d_head × d_head × bytes
```

第二个表达式不依赖上下文长度（`n_tokens`），而且只有一个记忆状态，而不是分开的键和值。不过它有一个二次项 `d_head × d_head`。这通常无需担心，因为头维度相对较小，例如 Qwen3-Next 中是 128。

包含卷积混合在内的完整循环机制要更复杂。但这些公式仍然展示了主要趋势：循环状态承载压缩后的长程信息，而 ShortConv 提供一个小得多的滚动缓冲区，用于精确的局部混合。

Kimi Linear 与 Qwen3-Next 在结构上有不少相似之处。两个模型都依赖混合注意力策略：将轻量的线性注意力与更重的完整注意力层结合。两者都使用约 3:1 的比例，即大约三个循环线性注意力块搭配一个完整注意力块。

Gated DeltaNet 是一个受循环神经网络启发的线性注意力变体，其中包括来自 Gated Delta Networks 论文的门控机制。从某种意义上说，Gated DeltaNet 就是加了 Mamba 风格门控的 DeltaNet，而 DeltaNet 是一种线性注意力机制。

Kimi Linear 用 KDA 修改了这一机制。Qwen3-Next 使用标量门（每个注意力头一个值）来控制记忆衰减速率，而 Kimi Linear 将其替换为对每个特征维度的逐通道门控。[Kimi Linear 论文](https://arxiv.org/abs/2510.26692)认为，这样可以更细致地控制记忆，进而改善长上下文推理。

在完整注意力层方面，Kimi Linear 使用多头潜在注意力（MLA）——与 DeepSeek V3 和 R1 使用的总体机制相同，但增加了一个门。MLA 压缩键/值空间以减小 KV 缓存大小。这些 MLA 层在混合架构中提供全局注意力路径，它们不包含 KDA 路径中的那三个 Q/K/V ShortConv 模块。

## Kimi Linear 在 KDA 层中对 Q、K、V 做过滤

Kimi Linear 对 ShortConv 的使用相当具体：在其 27 个解码器层中，20 层使用 Kimi Delta Attention（KDA），7 层使用 [MLA](https://sebastianraschka.com/llm-architecture-gallery/mla/)。

每个 KDA 层有三个 ShortConv 模块，分别位于 Q、K、V 投影之后。这三个卷积使用 4 的核大小和 SiLU 激活，其输出进入循环 KDA 更新。7 个 MLA 层不使用它们。

简而言之，四 token 混合发生在循环状态更新之前。

![Kimi Linear 架构：20 个 KDA 层和 7 个 MLA 层](https://sebastianraschka.com/llm-architecture-gallery/images/architectures/kimi-linear-48b-a3b.webp)

Kimi Linear 使用 KDA 与 MLA 层 3:1 的模式。ShortConv 模块位于 KDA 路径内部，
对其 Q、K、V 投影做预处理（原始出处
[*Kimi Linear*](https://arxiv.org/abs/2510.26692)）。

## Inkling 在每一层使用四个 ShortConv 模块

Inkling 走得更远：它的 66 个解码器层中每层都使用四个 ShortConv 模块：

- 键投影后的 `k_sconv`
- 值投影后的 `v_sconv`
- 注意力输出之后、主残差相加之前的 `attn_sconv`
- MLP 或 MoE 输出之后、主残差相加之前的 `mlp_sconv`

核大小同样是 4。Inkling 把每个模块的输入加回卷积输出，从而形成一个小的残差路径。Hugging Face 实现还把这些卷积保持在 FP32。

K 和 V 模块在注意力内部混合相邻 token；另外两个分别在注意力之后和前馈计算之后做同样的事。

![Inkling 架构：每个解码器层四个短卷积](https://sebastianraschka.com/llm-architecture-gallery/images/architectures/inkling.webp)

Inkling 将 ShortConv 放在 K、V 投影之后以及两个残差分支输出上。因此它的
66 个解码器层每层包含四个 ShortConv 模块（原始出处
[Thinking Machines Lab](https://thinkingmachines.ai/news/introducing-inkling/)）。

## 相同的核，不同的位置

在 Kimi Linear 中，ShortConv 在 KDA 内部为 Q、K、V 做预处理；在 Inkling 中，它作用于 K、V 和两个残差分支输出。核是同一个，主要区别在于放置的位置。

## Kimi Linear 为什么仍保留完整注意力

在那些较早的系统中，编码器 RNN 会逐 token 读取源句子，把它压缩成一列隐藏状态（最简单的版本是压缩成单个最终状态），然后解码器 RNN 必须从这个有限的摘要生成目标句子。这在句子短而简单时行得通，但一旦生成下一个输出词所需的相关信息位于输入句子的其他位置，它就形成了明显的瓶颈。

简而言之，局限在于隐藏状态无法存储无限多的信息或上下文，而有时直接回看完整的输入序列会更有用。

下面的翻译示例展示了这一思路的局限之一。例如，一个句子可以保留许多局部上说得通的选词，但当模型把问题过度当作逐词映射来处理时，作为翻译仍然会失败。（上面板展示了一个夸张的逐词翻译示例；显然，所得句子的语法是错误的。）
实际上，正确的下一个词取决于句子级结构，以及在此步骤中哪些更早的源词是重要的。当然，用 RNN 也能把这句话翻译得不错，但面对更长的序列或知识检索任务时它会很吃力，原因如前所述——隐藏状态能存储的信息有限。

![说明注意力动机的句子翻译示例](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/mha-motivation-translation.webp)

即使许多单独的选词看起来合理，翻译也可能失败，因为句子级结构
仍然重要（原始出处 [*LLMs-from-scratch*](https://github.com/rasbt/LLMs-from-scratch)）。

为了克服标准 RNN 的局限——一切都存进一个隐藏状态，模型在需要时无法访问原始输入——研究者通过
[*Neural Machine Translation by Jointly Learning to Align and Translate*](https://arxiv.org/abs/1409.0473) 引入了注意力机制。
其要点是消除隐藏状态的固定摘要瓶颈：不再强迫解码器只依赖对整个输入的一个压缩
摘要，而是让注意力在每一个输出步骤，通过重新审视更相关的编码器状态，
构建该步骤专属的上下文向量。

在语言中这一点很重要：我们想要的下一个词往往取决于源句子中早得多或晚得多位置上的内容，而不只是紧邻的前一个 token。

Kimi Linear 为这条完整注意力路径保留了七个 MLA 层；其余二十层使用更高效的循环 KDA 路径，并由 ShortConv 提供上文描述的局部四 token 混合。

参考资料

[Kimi Linear 论文](https://arxiv.org/abs/2510.26692)
[Kimi Linear 配置](https://huggingface.co/moonshotai/Kimi-Linear-48B-A3B-Base/blob/main/config.json)
[Kimi Linear 实现](https://huggingface.co/moonshotai/Kimi-Linear-48B-A3B-Instruct/blob/main/modeling_kimi.py)
[Inkling 发布文章](https://thinkingmachines.ai/news/introducing-inkling/)
[Inkling 配置](https://huggingface.co/thinkingmachines/Inkling/blob/main/config.json)
[Inkling Transformers 实现](https://github.com/huggingface/transformers/blob/main/src/transformers/models/inkling/modular_inkling.py)

[返回架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
