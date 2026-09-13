---
title: "AMD Instinct GPU 上的 EAGLE3 投机解码：用 vLLM 与 AMD Quark 进行训练与服务"
title_en: "EAGLE3 Speculative Decoding on AMD Instinct GPUs: Training and Serving with vLLM and AMD Quark"
source: https://vllm.ai/blog/2026-07-13-eagle-3-amd-instinct
crawled: 2026-09-12
translated: 2026-09-13
---

# AMD Instinct GPU 上的 EAGLE3 投机解码：用 vLLM 与 AMD Quark 进行训练与服务

> 原文：[EAGLE3 Speculative Decoding on AMD Instinct GPUs: Training and Serving with vLLM and AMD Quark](https://vllm.ai/blog/2026-07-13-eagle-3-amd-instinct) · vLLM 博客

作者：Larry Li、Chao Li、Haichen Zhang、Chun Fang、Andy Luo、Spandan Tiwari 和 Ashish Sirasao

[#性能](https://vllm.ai/blog/tags/performance)[#硬件](https://vllm.ai/blog/tags/hardware)

大语言模型（LLM）推理日益受制于自回归解码。即使预填充已被高度优化，解码阶段仍然一次一步地生成 token，而每一步通常都要完整跑一遍目标模型。对于 Kimi-K2.5 和 MiniMax-M2.5 这类大型混合专家、注意力密集的模型，这种串行模式限制了服务吞吐量，并增加了实时应用的延迟。

投机解码是解决这一瓶颈最实用的方法之一。它是一种无损的 LLM 推理加速技术，在保持目标模型精确输出分布的同时提升解码效率。它用一个更小或更轻量的草稿模型提出多个未来 token，再让原目标模型用一次前向验证这些 token。当草稿模型预测出的 token 也是目标模型会产出的时候，这些 token 可以被一并接受，从而减少昂贵的目标模型解码迭代次数。

常见的投机解码方法包括小型草稿模型、多 token 预测（MTP）、Medusa 式多头预测，以及 EAGLE3、DFlash 和最近推出的 DSpark 等特征级草稿方法。在现有投机解码方法中，EAGLE3 尤其有吸引力：草稿质量强、接受率高，推理加速稳定且有竞争力。

本文在 AMD Quark 团队的贡献下，走读 AMD Instinct GPU 上 EAGLE3 工作流的三个部分：(1) 训练 EAGLE3 草稿模型——vLLM 服务目标模型以合成 on-policy 数据、提取训练期隐藏状态，并运行在环的接受率评估；(2) [AMD Quark](https://quark.docs.amd.com/latest/) 量化——为目标模型与草稿模型都提供 Day-0 MXFP4 与 FP8 支持；(3) 在 AMD Instinct™ MI355X GPU 上通过 ROCm/vLLM 对 Kimi-K2.5 和 MiniMax-M2.5 做推理加速，使用 InferenceX 做基准测试。同一条流水线也被用来训练我们的 MiniMax-M3 EAGLE3 草稿，训练章节将以它作为贯穿示例。

## 为什么投机解码与 EAGLE3 重要

标准自回归解码每个目标模型步产出一个 token。如果模型要生成 1,000 个输出 token，服务引擎通常要在预填充后执行约 1,000 次目标模型解码迭代。这很昂贵，因为每次解码迭代都要触及模型权重、注意力状态、调度器和 KV 缓存机制。

投机解码改变了这一过程：

1. 草稿模型提出若干候选的下一个 token。
2. 目标模型用一次前向验证这些候选。
3. 贪心解码下，匹配的草稿 token 被接受；采样解码下，草稿 token 依据目标模型与草稿模型的概率被接受或修正。
4. 在第一次拒绝处，验证器产出一个修正 token 并从它继续草稿；若所有草稿 token 都被接受，验证器额外产出一个奖励 token。

条件接受率衡量在前序位置都被接受的前提下接受某个草稿位置的概率。接受长度衡量每个验证周期产出的 token 数。更高的接受长度可以减少目标模型验证步数，但实际吞吐量还取决于草稿与验证的开销。（图 1）

![贪心投机解码的提案与验证流程](https://vllm.ai/blog-assets/figures/2026-07-13-eagle-3-amd-instinct/figure1.png)

贪心投机解码的提案与验证流程

*图 1：γ=5 的贪心投机解码：目标模型接受 α=3 个 token 的前缀，在第一个不匹配处拒绝，丢弃其后的草稿 token，并产出一个修正 token，共返回 α+1=4 个 token。若所有 γ 个草稿 token 都被接受，多出的那个是目标模型生成的奖励 token。*

[EAGLE](https://github.com/SafeAILab/EAGLE) 在过去几年持续演进：EAGLE 从特征级投机解码起步，EAGLE2 改进了草稿质量和接受率，EAGLE3 则通过利用目标模型的多层特征进一步提升了准确率与加速比。它不依赖一个无关的小语言模型，而是训练一个与目标模型紧密对齐的草稿模块。它使用训练时测试（training-time testing）技术，组合目标模型的低、中、高层语义特征，帮助草稿模型提出验证器更可能接受的候选。

对生产推理来说，要点很简单：EAGLE3 可以提升生成吞吐量，同时通过验证保持目标模型的输出行为。

## AMD Quark MXFP4：面向主流 LLM 的 Day-0 量化

MXFP4 是开放计算项目（OCP）的 Microscaling 4 位浮点格式：4 位元素被分成共享一个缩放因子的小块，显存占用接近 INT4，同时数值行为好得多。AMD Instinct MI350 系列 GPU（MI350X/MI355X）提供原生 FP4 矩阵加速，MXFP4 权重可以直接映射到硬件上，缓解主导大型混合专家解码的显存带宽与容量压力。

AMD Quark 是 AMD 的模型量化工具包，AMD Quark 团队为主流 LLM 提供 Day-0 MXFP4 量化检查点，发布在 Hugging Face 上（例如 [amd/Kimi-K2.5-MXFP4](https://huggingface.co/amd/Kimi-K2.5-MXFP4) 和 [amd/MiniMax-M3-MXFP4](https://huggingface.co/amd/MiniMax-M3-MXFP4)）。Day-0 意味着重大模型发布时，Quark 团队就会交付可直接在硬件上运行、开箱支持 ROCm/vLLM 的 MXFP4（和 FP8）版本，而不必等待第三方量化跟上。这些已发布的检查点可以直接用作 EAGLE3 草稿训练与投机解码推理的目标。

这些检查点通过受支持的 MXFP4 执行路径和 AITER MoE 内核被 ROCm 上的 vLLM 直接消费，用户既得到 MXFP4 的显存节省，也获得生产级吞吐。投机解码是无损的：每个草稿 token 都对照所服务的目标模型验证，因此目标模型的输出分布保持不变。

## 用 vLLM 训练 EAGLE3 草稿模型

高接受率的草稿是投机解码快的原因，而训练这样的草稿既是建模问题，也是系统问题。在我们的流水线中，vLLM 不只是推理引擎——它也处于训练的中心。AMD Quark 团队在 AMD Instinct GPU 上开发并验证了 MiniMax-M3 EAGLE3 训练工作流，我们以它作为贯穿示例。（下文推理结果中的 Kimi-K2.5 与 MiniMax-M2.5 EAGLE3 草稿是来自 Hugging Face 的开源社区草稿，并非由我们训练。）（图 2）

![以 vLLM 为中心的 EAGLE3 训练与服务流水线](https://vllm.ai/blog-assets/figures/2026-07-13-eagle-3-amd-instinct/figure2.png)

以 vLLM 为中心的 EAGLE3 训练与服务流水线

*图 2：以 vLLM 为中心的 EAGLE3 训练流水线。一个 vLLM-on-ROCm 运行时驱动整个循环：它服务 AMD Quark MXFP4/FP8 目标模型以合成 on-policy 数据（Stage 1），把目标模型的低、中、高层隐藏状态流式传给训练器（Stage 2），在 FSDP2 下冷启动单层 EAGLE3 草稿头（Stage 3），运行在环的 serve-eval 按实测接受长度挑选最佳检查点（Stage 4），然后导出草稿并部署用于 EAGLE3 投机解码（Stage 5）。*

1. 由 vLLM 服务的 on-policy 数据合成。EAGLE3 草稿从目标模型自身分布的数据中学得最好。我们把 AMD Quark MXFP4 目标模型搭成 vLLM-ROCm 服务器，通过它生成 on-policy 响应——既包括 chat（`/v1/chat/completions`，使用与服务时完全相同的 chat 模板），也包括原始 `/v1/completions`（绕过模板），用于非对话与分布外鲁棒性。用与后续服务相同的引擎和模板生成数据，让训练与服务保持一致。
2. 由 vLLM 提供的隐藏状态提取。EAGLE3 以目标模型的内部特征——低、中、高层隐藏状态外加一个 `fc_norm`——为草稿提供条件，而不是依赖一个无关的小模型。vLLM 的隐藏状态提取钩子直接从运行中的目标引擎暴露这些辅助层。我们支持三种可互换的模式：在线（目标模型与训练器共置）、离线（隐藏状态转储到磁盘）和流式（隐藏状态从运行中的 vLLM serve 流式传给训练器，不落盘）。流式模式正是让在单节点上训练 420B MXFP4 MoE 目标模型变得可行的关键。
3. FSDP2 冷启动训练。单层 EAGLE3 草稿头从零开始训练，采用训练时测试（TTT）损失和位置衰减加权，运行在 FSDP2 之下。由于验证器就是 AMD Quark MXFP4 目标模型，草稿所学的激活空间与部署时将要面对的完全一致。
4. 在环的 serve-eval，同样在 vLLM 上。训练内损失会高估真实接受率，因此我们定期导出当前检查点，用 vLLM 投机解码来服务它，测量真实接受长度，并按这个服务指标挑选最佳检查点。将来在生产中运行的引擎，正是挑选草稿的同一个引擎。
5. 导出与 vLLM 部署。选出的草稿被导出为 Hugging Face 格式，整理成 vLLM 就绪的草稿目录，并用 vLLM-ROCm EAGLE 投机解码部署——正是下一节测量的那条路径。

### SPEED-Bench 上的草稿质量：11 个领域与长上下文

我们在 SPEED-Bench——一个多领域投机解码基准——上评估训练出的 MiniMax-M3 EAGLE3 草稿，使用接受长度（AL）指标，即每个目标验证步平均产出的 token 数（越高越好；AL = 1 表示每个目标验证步产出一个 token，未计入草稿开销）。

**按领域划分的接受长度（SPEED-Bench 定性）：**

| 领域 | 接受长度（AL） |
| --- | --- |
| 编程 | 3.32 |
| 数学 | 3.14 |
| RAG | 3.12 |
| 多语言 | 3.04 |
| 推理 | 2.89 |
| STEM | 2.86 |
| 摘要 | 2.86 |
| 人文学科 | 2.71 |
| 问答 | 2.55 |
| 写作 | 2.33 |
| 角色扮演 | 2.01 |
| **平均** | **2.80** |

在 11 个领域上，草稿平均 AL 为 2.80——每个目标验证步约产出 2.8 个 token。它在结构化、技术性内容上最强——编程（3.32）、数学（3.14）、RAG（3.12）和多语言（3.04）；在开放性写作和角色扮演上——对任何草稿都最难预测的场景——仍保持 AL 2.01-2.33。同样重要的是，当 prompt 从 1K 增长到 32K token 时，接受长度基本持平（2.69 到 2.65），表明草稿接受率在不同上下文长度下保持稳定。在 3 个投机 token 设置下，第一、二、三个草稿位置的接受比例（累计）分别约为 76%、56% 和 43%。这些结果正是我们以 vLLM 为中心的配方的回报：通过目标模型生成 on-policy 数据、用目标模型自身特征做隐藏状态监督、对照确切的 AMD Quark MXFP4 验证器做冷启动训练，以及按真实服务接受率挑选检查点。（图 3）

![MiniMax-M3 EAGLE3 按输入长度的接受长度](https://vllm.ai/blog-assets/figures/2026-07-13-eagle-3-amd-instinct/figure3.png)

MiniMax-M3 EAGLE3 按输入长度的接受长度

*图 3：在 SPEED-Bench 上，MiniMax-M3 EAGLE3 的接受长度从 1K 到 32K 上下文基本持平（1K 时 2.69 到 32K 时 2.65）。虚线 AL=1 标记每个验证周期产出一个 token。*

训练出的草稿已发布为 [amd/MiniMax-M3-EAGLE3.1](https://huggingface.co/amd/MiniMax-M3-EAGLE3.1)，可配合 vLLM 投机解码，以 [amd/MiniMax-M3-MXFP4](https://huggingface.co/amd/MiniMax-M3-MXFP4) 为目标进行服务：

```
export VLLM_ROCM_USE_AITER=1
vllm serve amd/MiniMax-M3-MXFP4 --trust-remote-code --tensor-parallel-size 8 \
--block-size 128 --attention-backend TRITON_ATTN --moe-backend emulation \
--speculative-config '{"method":"eagle3","model":"amd/MiniMax-M3-EAGLE3.1","num_speculative_tokens":3,"attention_backend":"TRITON_ATTN"}'
```

## 端到端解决方案

AMD Quark 团队端到端地覆盖整个栈：

- 目标模型：Day-0 MXFP4/FP8 量化与 ROCm/vLLM 部署。
- 草稿模型：本工作完成的 EAGLE3 训练、用 AMD Quark 做的 FP8/MXFP4 量化，以及 ROCm/vLLM 部署。
- 端到端集成：on-policy 数据合成、隐藏状态提取、serve-eval、导出与投机服务全部经由 vLLM 串联并一起验证。

这些组件合在一起，为 AMD Instinct GPU 提供了量化目标模型、配套的高接受率草稿，以及经过验证的 vLLM 投机解码部署。

## 加速结果

下面的草稿结果部分只列出 1K/1K 负载，ISL=1024、OSL=1024。加速比按 EAGLE3 吞吐量除以对应的无投机解码基线吞吐量计算。每个草稿结果只与同一 vLLM 构建和 MML 设置下的无投机基线比较。Kimi-K2.5 结果使用 AMD Instinct MI355X、TP=4、随机 prompt、`num_prompts=10 x concurrency`、`num_warmups=2 x concurrency`，每个单元 10 个随机种子。每个绘制值是 10 次不同随机种子运行的算术平均。这些随机 prompt 扫描是吞吐量微基准，不是应用级负载基准。Kimi 图把 BF16 与 FP8 草稿路径画在一起；BF16 的 vLLM v0.19.0 扫描使用 MML=2248，FP8 扫描使用 MML=2304。由于构建与 MML 设置不同，两条路径不是受控的精度对比。这里 MML（`max-model-len`）指最大上下文长度——vLLM 模型在单个请求中可处理的 token 总数（prompt + 生成输出）。

### Kimi K2.5 EAGLE3：BF16 与 AMD Quark FP8 草稿

Docker 镜像：BF16 扫描使用 `vllm/vllm-openai-rocm:v0.19.0`（MML=2248）；FP8 扫描使用 `vllm/vllm-openai-rocm:nightly-fb1ac806c55a6dc96fe92261b80c8550e9c39d2f`（MML=2304）。

目标模型：[amd/Kimi-K2.5-MXFP4](https://huggingface.co/amd/Kimi-K2.5-MXFP4)。BF16 草稿模型：[lightseekorg/kimi-k2.5-eagle3](https://huggingface.co/lightseekorg/kimi-k2.5-eagle3)。FP8 草稿模型：[amd/kimi-k2.5-eagle3-fp8](https://huggingface.co/amd/kimi-k2.5-eagle3-fp8)，由 AMD Quark 团队使用已发布的 AMD Quark FP8 量化工作流和元数据产出；它与目标模型共享 BF16 LM head。在此配置中，FP8 草稿路径经由 vLLM `RowWiseTorchFP8ScaledMMLinearKernel` 分发，即在 hipBLASLt 行级缩放 FP8 GEMM 之上执行 `torch._scaled_mm`，而不是走 AITER 预洗牌（preshuffled）FP8 路径。

![Kimi-K2.5 EAGLE3 在 AMD Instinct MI355X 上的吞吐量](https://vllm.ai/blog-assets/figures/2026-07-13-eagle-3-amd-instinct/figure4.png)

Kimi-K2.5 EAGLE3 在 AMD Instinct MI355X 上的吞吐量

*图 4：AMD Instinct MI355X（TP=4）上 1K/1K 负载的 Kimi-K2.5 EAGLE3 输出吞吐量（tok/s/GPU）。BF16 与 AMD Quark FP8 草稿路径都优于无投机基线（分别为 1.69x-1.90x 和 1.76x-2.00x）；低并发时收益最大。每个加速比都使用与之匹配的无投机基线；BF16 与 FP8 扫描使用不同的 vLLM 构建和 MML 设置。*

### MiniMax M2.5 BF16 EAGLE3

Docker 镜像：`vllm/vllm-openai-rocm:nightly-4eafc729285e459a5fc96efd6f7b313b155cad48`

目标模型：[MiniMaxAI/MiniMax-M2.5](https://huggingface.co/MiniMaxAI/MiniMax-M2.5)。草稿模型：[thoughtworks/MiniMax-M2.5-Eagle3](https://huggingface.co/thoughtworks/MiniMax-M2.5-Eagle3)，BF16 草稿路径，`num_speculative_tokens=3`、`draft_tensor_parallel_size=1`。以下数字使用 1K/1K 随机 prompt、TP=4 且开启专家并行，每个并发 5 个随机种子。每个绘制值是 5 次不同随机种子运行的算术平均，每个 EAGLE3 结果都与同一构建、同一配置下的无投机基线配对。

![MiniMax-M2.5 EAGLE3 在 AMD Instinct 上的吞吐量](https://vllm.ai/blog-assets/figures/2026-07-13-eagle-3-amd-instinct/figure5.png)

MiniMax-M2.5 EAGLE3 在 AMD Instinct 上的吞吐量

*图 5：AMD Instinct MI355X（TP=4）上 1K/1K 负载的 MiniMax-M2.5 EAGLE3 输出吞吐量（tok/s/GPU）。每个 EAGLE3 结果使用与之匹配的无投机基线；相对收益最大出现在低并发时。*

在 1K/1K 扫描中，相对于各自匹配的无投机基线，EAGLE3 为 Kimi-K2.5 带来 1.69x–2.00x 的输出吞吐提升，为 MiniMax-M2.5 带来 1.38x–1.79x 的提升（图 4 和图 5）。

## 总结

在 AMD Instinct GPU 上，采用 EAGLE3 的投机解码在保持目标模型解码语义的同时带来吞吐收益——在我们的 1K/1K 扫描中，Kimi-K2.5 为 1.69x 到 2.00x，MiniMax-M2.5 最高 1.79x。让这一切端到端可行的是三者的结合：(1) 面向目标模型与选定草稿检查点的 AMD Quark MXFP4/FP8 量化；(2) 以 vLLM 为中心的训练流水线——合成 on-policy 数据、提取隐藏状态、按真实服务接受率挑选检查点；(3) ROCm/vLLM 投机服务。已发布的 AMD Quark 工具包提供量化工作流；AMD Instinct GPU 上的 EAGLE3 草稿训练支持计划在下一个 AMD Quark 版本中提供。

## 致谢

我们感谢 AMD Quark 团队、AMD ROCm 与 vLLM 贡献者、InferenceX 维护者与评审者，以及 EAGLE3 研究社区的工作与反馈。特别感谢 Chang Liu、Xinjun Niu、Wei Luo、Lin Zhao。

## 更多资源

- [EAGLE3 项目](https://github.com/SafeAILab/EAGLE)
- [EAGLE3 论文](https://arxiv.org/abs/2503.01840)
- [SPEED-Bench](https://arxiv.org/abs/2604.09557)
- [InferenceX](https://github.com/SemiAnalysisAI/InferenceX)
- [AMD Quark](https://github.com/amd/Quark)
- [vLLM](https://github.com/vllm-project/vllm)
