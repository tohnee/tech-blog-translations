---
title: "在 Amazon SageMaker AI 与 Amazon Bedrock 上用 vLLM 高效服务数十个微调模型"
title_en: "Efficiently serve dozens of fine-tuned models with vLLM on Amazon SageMaker AI and Amazon Bedrock"
source: https://vllm.ai/blog/2026-02-26-multi-lora
crawled: 2026-09-12
translated: 2026-09-13
---

# 在 Amazon SageMaker AI 与 Amazon Bedrock 上用 vLLM 高效服务数十个微调模型

> 原文：[Efficiently serve dozens of fine-tuned models with vLLM on Amazon SageMaker AI and Amazon Bedrock](https://vllm.ai/blog/2026-02-26-multi-lora) · vLLM 博客

作者：Danielle Maddix Robinson、Florian Saupe、George Novack、Haipeng Li、Mani Kumar Adari、Xiang Song、Yu Gong（AWS AI 团队）

[#性能](https://vllm.ai/blog/tags/performance)

运行多个自定义 AI 模型的组织和个人——尤其是近期的混合专家（MoE）模型家族——可能面临这样的挑战：当单个模型获得的流量不足以填满专用计算端点时，却仍要为闲置的 GPU 容量付费。为解决这一问题，我们与 vLLM 社区合作，为 GPT-OSS、Qwen 等流行开源 MoE 模型开发了一套高效的多低秩适应（Multi-LoRA）服务方案。Multi-LoRA 是一种流行的模型微调方法。它不重新训练整个模型权重，而是保持原始权重冻结，并在模型层中注入小的可训练适配器。采用 multi-LoRA 时，推理阶段多个自定义模型共享同一 GPU，每个请求只换入换出适配器。例如，五个各自只用了专用 GPU 10% 容量的客户，可以通过 multi-LoRA 由一块 GPU 服务，把五块利用率不足的 GPU 变成一块高效共享的 GPU。

在本文中，我们介绍如何在 vLLM 中为混合专家（MoE）模型实现 multi-LoRA 推理，描述我们所做的内核级优化，并展示你如何从这项工作中受益。全文以 GPT-OSS 20B 为主要示例。

你现在就可以在本地 vLLM 部署中使用这些改进，要求版本为 0.15.0 或更高。Multi-LoRA 服务现已支持 GPT-OSS、Qwen3-MoE、DeepSeek 与 Llama MoE 等 MoE 模型家族。我们的优化还有助于改进稠密模型的多 LoRA 托管，例如 Llama3.3 70B 或 Qwen3 32B。相比 vLLM 0.15.0，Amazon 专属优化还能进一步降低延迟：对 GPT-OSS 20B，每秒输出 token 数（OTPS）提高 19%（即模型生成输出的速度），首 token 延迟（TTFT）降低 8%（即模型开始生成输出前需要等待的时间）。要从这些优化中受益，请把你的 LoRA 定制模型托管在 [Amazon SageMaker AI](https://aws.amazon.com/sagemaker/ai/) 或 [Amazon Bedrock](https://aws.amazon.com/bedrock/) 上。

# 在 vLLM 中为 MoE 模型实现 multi-LoRA 推理

在深入 vLLM 中 MoE 模型 multi-LoRA 推理的最初实现之前，我们先提供一些关于 MoE 模型与 LoRA 微调的背景信息，这对理解我们优化背后的原理十分重要。MoE 模型包含多个被称为专家（expert）的专用神经网络。路由器把每个输入 token 引导到最相关的专家，再对它们的输出进行聚合。这种稀疏架构能以更少的计算资源处理更大的模型，因为每个 token 只激活模型总参数的一小部分，可视化见图 1。

每个专家都是一个小的前馈网络，分两个阶段处理 token 的隐藏状态。第一步，`gate_up` 投影把紧凑的隐藏状态（如 4096 维）扩展到更大的中间空间（如 11008 维）。这一扩展是必要的，因为紧凑空间中的特征彼此高度纠缠——更大的空间给了网络把特征拉开、变换它们、并选择性地门控哪些特征重要的余地。第二步，`down` 投影把结果压缩回原始维度。这有助于保持输出与模型其余部分的兼容，并充当瓶颈，迫使网络只保留最有用的特征。两者结合，这种“先扩展再压缩”的模式让每个专家在保持输出大小一致的同时施加丰富的变换。vLLM 使用 `fused_moe` 内核以分组通用矩阵乘法（Group GEMM）的方式执行这些投影——每个被分配给给定 token 的专家对应一次 GEMM。Multi-LoRA 微调保持基础模型权重 `W`（例如 gate\_up 投影的 `W_gate_up`）冻结，训练两个小矩阵 `A` 与 `B`，二者共同构成一个适配器。对于基础权重 `W` 形状为 `h_in × h_out` 的投影，LoRA 训练形状为 `h_in × r` 的 `A` 与形状为 `r × h_out` 的 `B`，其中 `r` 是 LoRA 秩（通常为 16-64）。微调后的输出变为 `y = xW + xAB`。每个 LoRA 适配器为一次投影增加两个操作。收缩（shrink）操作计算 `z=xA`，把输入从 h\_in 维降到 `r` 维。扩展（expand）操作取该 r 维结果，通过 `z` 与 `B` 相乘投影回 `h_out` 维。见图 1 右侧的示意。

![](https://vllm.ai/blog-assets/figures/2026-multilora/moe_schematic.png)

*图 1：MoE-LoRA 模型工作原理示意，示例中隐藏状态维度为 4096，中间表示维度为 11008，LoRA 秩 r = 32。*

每个专家有两个权重投影：`gate_up` 与 `down`。应用 LoRA 适配器时，会为每个投影增加两个低秩操作，即收缩与扩展。这意味着每个专家总共需要四个 LoRA 内核操作：`gate_up` 的收缩与扩展，以及 `down` 的收缩与扩展。在多 LoRA 服务场景中，多个 LoRA 适配器同时为不同用户或任务服务，系统必须针对每个专家、每个适配器、每个请求高效管理这四个操作。这使其成为 MoE 模型的关键性能瓶颈。这四个操作涉及的矩阵中，一个维度（LoRA 秩 `r`）比另一维度（如隐藏状态与中间表示维度）小 100-300×。标准 GEMM 内核是为近似方阵设计的，在瘦长矩阵上表现不佳，这正是本文稍后描述的内核优化之所以必要的原因。除了要针对瘦长矩阵优化之外，为 MoE 模型添加 multi-LoRA 支持还面临两个技术挑战。其一，vLLM 此前缺少能在 MoE 层上执行 LoRA 的内核，因为现有的稠密 multi-LoRA 内核不处理专家路由。其二，MoE LoRA 结合了两个稀疏性来源：专家路由（token 被分配给不同专家）与适配器选择（请求使用不同 LoRA 适配器）。这种复合稀疏性需要专门的内核设计。为应对这些挑战，我们创建了 `fused_moe_lora` 内核，将 LoRA 操作集成到 `fused_moe` 内核中。这一新内核为 `gate_up` 与 `down` 投影执行 LoRA 收缩与扩展 GEMM。`fused_moe_lora` 内核遵循与 `fused_moe` 内核相同的逻辑，并在网格上为相应激活的 LoRA 适配器增加了一个额外维度。

# 改进 vLLM 中的 multi-LoRA 推理性能

在完成初始实现后，我们使用 NVIDIA Nsight Systems（Nsys）识别瓶颈，发现 `fused_moe_lora` 内核是延迟最高的组件。随后我们使用 NVIDIA Nsight Compute（NCU）对四个内核操作 `gate_up_shrink`、`gate_up_expand`、`down_shrink` 与 `down_expand` 的计算与内存吞吐进行了剖析。基于这些发现，我们为这四个内核开发了执行优化、内核级优化与调优后的配置。

## 执行优化

在初始实现中，multi-LoRA 的 TTFT 比基础模型的 TTFT（即 GPT-OSS 20B 的公开发布版本）高出 10 倍（更差）。我们的剖析发现，Triton 编译器把与输入长度相关的变量当作编译期常量，导致 `fused_moe_lora` 内核每遇到新的上下文长度都要从头重新编译，而不是复用。这在图 2 中清晰可见：每次 `fused_moe_lora` 内核执行前出现的 `cuModuleLoadData` 调用表明 GPU 正在加载新编译的内核二进制而非复用缓存，内核启动时间之间的大段空隙则表明 GPU 在重新编译期间处于空闲。这一开销造成了相比基础模型 10× 的 TTFT 回退。我们通过为这些变量添加 `do_not_specialize` 编译器提示解决了这一问题，指示 Triton 只编译一次内核并在所有上下文长度间复用。

![](https://vllm.ai/blog-assets/figures/2026-multilora/exec_opt.png)

*图 2：执行优化前 `fused_moe_lora` 内核的剖析结果。*

## 内核优化

Split-K 是一种工作分解策略，有助于改善瘦长矩阵的负载均衡。LoRA 收缩计算 `xA`，其中 `x` 的维度为 `1×h_in`，`A` 的维度为 `h_in×r`。`r` 个输出元素中的每一个都需要对 `h_in` 次乘法求和。标准 GEMM 内核把不同的线程组——共享高速片上内存的一批 GPU 线程——分配给不同的输出元素，但每个线程组按顺序计算自己的 `h_in` 求和。当 `r` 只有几十而 `h_in` 有数千时，可并行化的输出元素很少，而每个又需要很长的串行求和。Split-K 通过把 GEMM 内维 `K`（本例中 `K=h_in`）上的求和拆分到多个线程组来解决这一问题：各线程组并行计算部分和，再合并结果。这些部分结果需要一次原子加法才能得到最终的和。由于我们执行的是不带额外逻辑的纯原子加法，我们利用 Triton 编译器的优化自由度，为原子加法操作设置参数 `sem="relaxed"`。

GPU 调度器会把多个线程组分配给同一个输出元素，并同时运行不同输出元素的线程组。对于 `lora_shrink`，每个输出元素需要读取 `A` 的一列，该列跨越 `h_in` 行。当 `h_in` 达到数千时，每一列触及的缓存行分布在很大的内存区域上。相邻的列共享相同的行并在缓存中重叠，因此处理相邻列的线程组可以通过复用彼此已加载的数据而受益。协作线程数组（CTA）swizzling 会重排调度，让处理相邻列的线程组同时运行，从而提高 L2 缓存复用。我们对 `lora_shrink` 操作应用了 CTA swizzling。

我们还从收缩与扩展 LoRA 内核中移除了不必要的掩码与点积操作。Triton 内核以固定大小的块加载数据，但矩阵维度未必能被这些块大小整除。例如，如果 `BLOCK_SIZE_K` 为 64 而矩阵维度 K 为 100，第二个块会尝试读取 28 个无效内存位置。掩码通过在加载前检查每个索引是否越界来防止这些非法内存访问。然而，这些条件检查会在每次加载操作时执行，即使元素有效也会带来开销。我们引入了 `EVEN_K` 参数来检查 K 是否能被 `BLOCK_SIZE_K` 整除。当为真时，所有加载都是有效的，可以完全跳过掩码，这有助于同时降低掩码开销与不必要的点积计算。

最后，我们把 LoRA 权重与基础模型权重的相加融合进 LoRA 扩展内核。这一优化有助于减少内核启动开销。这些内核优化帮助我们在 GPT-OSS 20B 上达到 144 OTPS 与 135 ms TTFT。

## 为 Amazon SageMaker AI 与 Amazon Bedrock 调优内核配置

Triton 内核需要对块大小（`BLOCK_SIZE_M`、`BLOCK_SIZE_N`、`BLOCK_SIZE_K`）等参数进行调优，它们控制矩阵计算在线程组之间的划分方式。高级参数包括控制线程组排序以提升缓存局部性的 `GROUP_SIZE_M`，以及在矩阵内维上并行化求和的 `SPLIT_K`。

我们发现，使用为标准 fused MoE 优化的默认配置的 MoE LoRA 内核，在 multi-LoRA 服务中表现不佳。这些默认值没有考虑与 LoRA 索引对应的额外网格维度，也没有考虑多个适配器带来的复合稀疏性。为解决这一瓶颈，我们增加了让用户通过提供文件夹路径来加载自定义调优配置的支持。更多信息请参见 vLLM LoRA Tuning 文档。我们对四个 `fused_moe_lora` 操作（`gate_up_shrink`、`gate_up_expand`、`down_shrink`、`down_expand`）同时进行调优，因为它们共享同一个 `BLOCK_SIZE_M` 参数。Amazon SageMaker AI 与 Bedrock 客户现在可以使用这些调优后的配置，它们会被自动加载，在 GPT-OSS 20B 上达到 171 OTPS 与 124 ms TTFT。

# 结果与结论

通过与 vLLM 社区的合作，我们为 GPT-OSS、Qwen3 MoE、DeepSeek 与 Llama MoE 等 MoE 模型实现并开源了 multi-LoRA 服务。随后我们应用了各项优化，例如在 vLLM 0.15.0 相比 vLLM 0.11.1rc3 时，GPT-OSS 20B 的 OTPS 提升 454%、TTFT 降低 87%。部分优化——尤其是内核调优与 CTA swizzling——也改善了稠密模型的性能，例如 Qwen3 32B 的 OTPS 提升了 99%。要在本地部署中利用这项工作，请使用 vLLM 0.15.0 或更高版本。可在 Amazon Bedrock 与 Amazon SageMaker AI 中使用的 Amazon 专属优化，为各模型带来额外的延迟改进，例如对 GPT-OSS 20B 而言，相比 vLLM 0.15.0 OTPS 快 19%、TTFT 改善 8%。要开始在 Amazon 上托管自定义模型，请参阅 [Amazon SageMaker AI 托管](https://docs.aws.amazon.com/sagemaker/latest/dg/deploy-model.html)与 [Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/fine-tuning-openai-apis.html) 文档。

![](https://vllm.ai/blog-assets/figures/2026-multilora/otps.png)

*图 3：GPT-OSS 20B multi-LoRA 推理的每秒输出 token 数（OTPS）与首 token 延迟（TTFT）：1/ vLLM 0.11.1rc3 中的初始实现；2/ 使用 vLLM 0.15.0；3/ 使用 vLLM 0.15.0 加 AWS 自定义内核调优。实验使用 1600 个输入 token 与 600 个输出 token，LoRA 秩为 32，并行加载 8 个适配器。*

### 致谢

我们感谢来自 vLLM 社区的贡献者与合作者：Jie Li、Chen Wu、Varun Sundar Rabindranath、Simon Mo 与 Robert Shaw，以及我们的团队成员：Xin Yang、Sadaf Fardeen、Ashish Khetan 与 George Karypis。

本文同时发表于 [AWS Blogs](https://aws.amazon.com/blogs/machine-learning/efficiently-serve-dozens-of-fine-tuned-models-with-vllm-on-amazon-sagemaker-ai-and-amazon-bedrock/)。
