---
title: "门控残差（GR）"
title_en: "Gated Residuals (GR)"
source: https://sebastianraschka.com/llm-architecture-gallery/gated-residuals/
crawled: 2026-09-06
translated: 2026-09-06
---

# 门控残差（GR）

> 原文：[Gated Residuals (GR)](https://sebastianraschka.com/llm-architecture-gallery/gated-residuals/)

门控残差（Gated Residuals，GR）机制在思路上与 [mHC](https://sebastianraschka.com/llm-architecture-gallery/mhc/) 相关，两者都用四条并行的残差连接替换 transformer 块中的单一残差连接。就 GR 而言，它包含两个单元或模块：GR Read 和 GR Write。例如，在每个 MoE 子层之前，GR Read 模块把 4 条流压缩成一个常规宽度的输入；随后，GR Write 模块把该子层的输出加回全部四条流（这里为每条流使用一个可学习的标量门）。

它与 mHC 的相似之处在于，每个子层仍然使用常规的隐藏宽度。不过，引入这一概念的 Qwen 3.8-Flash-Next 并没有使用 mHC 那个用于混合残差流的独立受约束矩阵。

[架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
[mHC 解释](https://sebastianraschka.com/llm-architecture-gallery/mhc/)
[模型卡](https://huggingface.co/Qwen/Qwen3.8-Flash-Next)

![Qwen3.8-Flash-Next 架构：GR Read 与 GR Write 环绕序列子层和 MoE 子层](https://sebastianraschka.com/llm-architecture-gallery/images/architectures/qwen3-8-flash-next.webp)

图 1. Qwen3.8-Flash-Next 在每个 transformer 块中把 GR Read 和 GR Write 同时置于序列子层与 MoE 子层周围。架构细节来自
[模型卡](https://huggingface.co/Qwen/Qwen3.8-Flash-Next)、
[发布配置](https://huggingface.co/Qwen/Qwen3.8-Flash-Next/blob/main/config.json)以及
[实现代码](https://github.com/huggingface/transformers/blob/main/src/transformers/models/qwen4_exp/modeling_qwen4_exp.py#L920-L947)。

残差宽度

四条并行流

读门与写门

逐元素的读门，以及每条流一个标量写门

示例架构

[Qwen3.8-Flash-Next 125B-A6B](https://sebastianraschka.com/llm-architecture-gallery/#card-qwen3-8-flash-next-125b-a6b)

## GR Read

设 \(R\_1, \ldots, R\_4\) 表示四条独立的残差流。GR Read 对每条残差流分别独立地做归一化，然后为每条流预测一个逐元素的门 \(g\_i\)。接着，它对这些经过门控的流取平均，得到常规宽度的子层输入：

\[x = \frac{1}{4}\sum\_{i=1}^{4} g\_i \odot \operatorname{RMSNorm}(R\_i).\]

这里，门控网络读取（拼接后的）四流状态。在 Qwen3.8-Flash-Next 中，它把 10,240 维状态先投影降到一个 320 维表示，再投影回升为 10,240 个逐元素门。sigmoid 函数（"门"）保证每个 Read 门落在 0 到 1 的范围内。

## GR Write

在某个模块（注意力模块、Gated DeltaNet 或 MoE 子层）产生输出 \(y\) 之后，GR Write 模块为每条流预测一个标量门 \(s\_i\)，并分别施加常规的残差相加：

\[R\_i' = R\_i + s\_i y.\]

GR Write 模块以 \(2\,\sigma(\cdot)\) 的形式计算写门，因此每个取值都落在 0 到 2 之间。原始残差流保持不变，每条流接收的是同一个子层输出的不同缩放副本。

Qwen 在每个 transformer 块中把这种"读—子层—写"的序列应用两次。第一次包裹 Gated DeltaNet 或 [Qwen Sparse Attention](https://sebastianraschka.com/llm-architecture-gallery/qwen-sparse-attention/)，第二次包裹 MoE 子层。在最后一层之后，还有一个最终的 GR Read 把四条流收敛回单一模型输出。

## GR 与 mHC 的区别

两种方法都在保持注意力和 MoE 子层为常规隐藏宽度的同时拓宽了残差路径。区别在于流更新的方式。

- [mHC](https://sebastianraschka.com/llm-architecture-gallery/mhc/) 包含一个残差流混合矩阵。流形约束使该矩阵成为双随机矩阵。
- GR 直接把每条残差流向前传递。各条流在 GR Read 形成子层输入时汇合，GR Write 再以每条流一个标量门的方式把子层输出加回去。
- GR 使用以 sigmoid 限界的读门和写门，不采用 mHC 那种双随机投影。

参考资料

[Qwen3.8-Flash-Next 模型卡](https://huggingface.co/Qwen/Qwen3.8-Flash-Next)
[Qwen3.8-Flash-Next 配置](https://huggingface.co/Qwen/Qwen3.8-Flash-Next/blob/main/config.json)
[Qwen3.8-Flash-Next 技术报告](https://github.com/QwenLM/Qwen3.8-Flash-Next/blob/main/tech_report.pdf)
[Transformers 中的 GR 实现](https://github.com/huggingface/transformers/blob/main/src/transformers/models/qwen4_exp/modeling_qwen4_exp.py#L920-L947)
[mHC 论文](https://arxiv.org/abs/2512.24880)

[返回架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
