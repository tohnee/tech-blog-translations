---
title: "FastH3-QAD-v2 与 NVFP4 VAE 解码器：更好的质量、更快的解码，以及社区 LoRA"
title_en: "FastH3-QAD-v2 and NVFP4 VAE Decoders: Better Quality, Faster Decoding, and Community LoRAs"
date: 2026-10-19
source: https://haoailab.com/blogs/fasth3-v21/
crawled: 2026-11-16
translated: 2026-11-16
---

# FastH3-QAD-v2 与 NVFP4 VAE 解码器：更好的质量、更快的解码，以及社区 LoRA

> 原文：[FastH3-QAD-v2 and NVFP4 VAE Decoders: Better Quality, Faster Decoding, and Community LoRAs](https://haoailab.com/blogs/fasth3-v21/) · Hao AI Lab @ UCSD

2026 年 10 月 19 日 · 9 分钟 · Aryan Kumar、Will Lin、Hao Zhang

![FastH3-QAD-v2](https://haoailab.com/blogs/fasth3-v21/img/cover.png)

[![](https://img.shields.io/github/stars/hao-ai-lab/FastVideo?style=social)](https://github.com/hao-ai-lab/FastVideo)[![](https://img.shields.io/badge/🤗%20huggingface--green.svg?style=social)](https://huggingface.co/collections/FastVideo/fastvideo-fasth3)[![Slack](https://img.shields.io/badge/Slack--4A154B?style=social&logo=slack&logoColor=blue)](https://join.slack.com/t/fastvideo/shared_invite/zt-3f4lao1uq-u~Ipx6Lt4J27AlD2y~IdLQ)

FastH3 V2 在消费级 GPU 上以 NVFP4 运行一个八步的视频与音频模型。FastH3-QAD-v2 在不改变架构、显存占用或文件布局的前提下提升了质量——做法是训练这个 4-bit 模型，而不只是校准它。

我们发布三样东西：

* **FastH3-QAD-v2**，FastH3 V2 的量化感知蒸馏（QAD）检查点。它保持 V2 的显存占用与文件布局，并且在 FP4 注意力下端到端追平或超过 V2。
* **两个 NVFP4 VAE 解码器**，在 FastH3 自己的输出上训练。36 层解码器与原版 H3 解码器相当。8 层解码器快 15 倍。两者在 LightVAE 自己的基准上都胜出。
* **FastVideo 中的社区 LoRA。** 为 MiniMax H3 在 ComfyUI 及其他常见格式中训练的 LoRA 现在可以直接加载，在 NVFP4 模型上也可以。

三者共同构成了明天发布的 **FastH3 Omni** 的基础——它会同时用到这三项。更多内容见[文末](#tomorrow-fasth3-omni)。

[![
](img/cover.png)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-v21--img--videos--world-tour.mp4#t=0.1)

用 FastH3-QAD-v2 与两个 NVFP4 解码器在两台 DGX Spark 上生成的六个 10 秒片段。请打开声音。

## FastH3-QAD-v2：QAD 弥合 PTQ 的质量差距[#](#fasth3-qad-v2-qad-closes-the-ptq-quality-gap)

FastH3-QAD-v2 是 FastH3 V2 的量化感知蒸馏（QAD）检查点。V2 交付时用的是训练后量化（PTQ）：在 1,000 条提示词上校准激活缩放，然后把每个权重舍入到 4 bit。QAD 更进一步。教师是全精度的 V2。学生在全部 350 个线性层上运行部署时的 4-bit 权重与激活，并透过舍入进行训练，于是权重去适配量化后的前向计算，而不是把误差带进输出。

* **对齐每一步。** 在八个采样步的每一步，学生看到教师的输入，学习教师的输出。四分之一的样本跑在学生自己的轨迹上，因此它也学会从自身的小误差中恢复。
* **纯文本训练。** 该配方使用 3,000 条文本提示词，在两个 GB200 节点上训练 300 步，约五小时。
* **共享配方。** 同一套 QAD 方法也是后续 FastH3 模型（包括 FastH3 Omni）的训练路径。

结果以 30 条留出提示词上相对全精度 V2 的误差衡量（越低越好）：

| 相对全精度 V2 的误差 | V2 NVFP4 | FastH3-QAD-v2 NVFP4 | 变化 |
| --- | --- | --- | --- |
| 每个采样步，视频 + 音频 | 0.431 | 0.351 | −19% |
| 视频 | 0.471 | 0.382 | −19% |
| 音频 | 0.391 | 0.319 | −18% |
| 八步后的最终视频 | 0.817 | 0.713 | −13% |
| 显存、文件布局 | 不变 | | |

### 为什么 VSA 门控保持 BF16[#](#why-the-vsa-gates-stay-in-bf16)

Video Sparse Attention 用小型的门控投影来决定每个 token 关注哪些视频瓦片。量化这些线性层会改变算术结果；改变门控则会改变选择本身，于是注意力模式不再与模型训练时的一致。FastH3-QAD-v2 把门控与归一化层保持在 BF16，只训练 q/k/v/out 与 FFN 投影——这正是 NVFP4 导出所量化的同一批层。

结果在保留瓦片选择的同时，让每个量化投影都能适配 4-bit 算术。在正式推广每个 QAD 检查点之前，我们除了看教师强制指标，还会用部署流水线在渲染片段上做评估。

## NVFP4 VAE 解码器[#](#nvfp4-vae-decoders)

每个 FastH3 片段都以 VAE 解码器收尾，它把隐变量变成像素。在 transformer 与文本编码器迁移到 NVFP4 之后，解码器是 FastH3 中最后一块非 4-bit 的部分，而在 DGX Spark 上它已占总时间的三分之一：INT8 轻量 VAE 解码一个 5 秒、480p 片段需要 **43 秒**，而去噪是 68 秒。

![单台 DGX Spark 上 5 秒 832×480 片段的视频解码时间：INT8 轻量 VAE 42.8 秒、稠密轻量 VAE 9.6 秒、我们的 8 层 NVFP4 解码器 1.6 秒。](img/fig_spark_decode.svg)

图 1. 单台 DGX Spark 上 5 秒、832×480 片段的视频解码时间。

我们训练了两个 NVFP4 解码器，二者都从原始的 36 层 H3 解码器蒸馏而来：

* **质量版，36 层。** 完整解码器，每个块都是 NVFP4。1.29 GiB 而非 4.5 GiB，与原版差距在 0.1 dB 以内。
* **快速版，8 层。** 36 个块中的 8 个，经蒸馏与量化。0.31 GiB，比原版快 15 倍。

### 在 FastH3 自己的输出上训练[#](#trained-on-fasth3s-own-outputs)

解码器只需在它拿到的隐变量上表现良好。我们在 **FastH3 自己生成的隐变量**上训练，并混入编码后的真实视频，使解码器在训练与推理时看到相同的分布：

* **教师：** 全精度的原始 H3 解码器。**损失：** 在随机隐变量瓦片上，对教师输出的像素 L1 加 LPIPS。
* **学生：** 每个 transformer 块中使用 NVFP4 权重与激活；输入/输出投影与归一化保持更高精度。
* **误差从何而来：** 仅用 4-bit 权重时解码器几乎无损。剩余误差来自 4-bit 激活，且均匀分布在各个块中。

### 融合的 FP4 kernel[#](#fused-fp4-kernels)

一个 4-bit GEMM 只有在它周围的一切也够快时才快。解码器的块运行在融合的 Triton 与 CUTLASS FP4 kernel 上，这些 kernel 完成激活量化、应用缩放并执行 GEMM，无需往返内存。CUDA graphs 消除了启动开销，权重在 GPU 上保持 4-bit 打包。融合路径与未融合的 NVFP4 参考逐比特一致，并把 36 层解码器在 480p 下从 1.88 秒降到 0.53 秒。

### 与 LightVAE 正面对比[#](#head-to-head-with-lightvae)

[LightVAE](https://huggingface.co/lightx2v/LightVAE) 是 H3 上广泛使用的公开轻量解码器。LightVAE-Lite 保留 36 个解码器层中的 12 个，声称约为原版速度的 3 倍。我们**在 LightVAE 自己的协议上**对比：1344×768、124 帧、bf16、eager 模式，一次预热、三次运行取中位数，单台 GB200。LightVAE 使用它自己的代码与权重，每个解码器接收到来自原版 H3 编码器的相同隐变量。20 个测试片段由 10 段 H3 生成视频和 10 段真实影像组成，后者任何解码器都没见过。我们的测试框架精确复现了 LightVAE 的 PSNR，他们的速度声明也成立（2.85 倍，他们声称 2.96 倍）。

| 解码器 | 解码 FPS，eager | 解码 FPS，最佳配置 | PSNR (dB) | LPIPS | 大小 |
| --- | --- | --- | --- | --- | --- |
| 原版 H3 | 17.9 | 62.1 | 33.73 | 0.071 | 4.5 GiB |
| LightVAE-Lite（解码器） | 51.0（2.86×） | 183.7 | 31.74（−2.0） | 0.109 | 1.5 GiB |
| LightVAE-Lite（编码器 + 解码器） | 49.3 | 183.1 | 30.57（−3.2） | 0.140 | 1.5 GiB |
| 我们的，36 层 NVFP4 | 70.0（3.9×） | 104.3 | 33.63（−0.10） | 0.073 | 1.29 GiB |
| 我们的，8 层 NVFP4 | 274.6（15.4×） | 418 | 31.73（= Lite） | 0.096 | 0.31 GiB |

列内最优为我们的结果，优于 LightVAE-Lite。「最佳配置（Best config）」把所有空间瓦片放在一次调用中，并加上 `torch.compile`，对所有模型同等应用。

![原版 H3 解码器、LightVAE-Lite、TAEH3 与我们两个 NVFP4 解码器的解码延迟对 PSNR。](img/fig_vae_pareto.svg)

图 2. LightVAE 协议（1344×768，单台 GB200）下 H3 VAE 解码器的质量与解码延迟。延迟越低、PSNR 越高越好。

* **36 层 vs LightVAE-Lite：** 高 1.9 dB，基本无损（相对原版 −0.10 dB，而 Lite 损失 2.0），在他们的协议上更快（70 vs 51 FPS），体积也更小。唯一落后之处：在最佳配置下，Lite 的解码器更快（184 vs 104 FPS），但质量低 1.9 dB。
* **8 层 vs LightVAE-Lite：** PSNR 相同（31.73 vs 31.74 dB），LPIPS 更好（0.096 vs 0.109），在他们的协议上快 5.4 倍，最佳配置下快 2.3 倍，体积小 5 倍。
* **在真实影像与生成视频上，480p、720p 与 768p 下，** 排名都一致。
* **在我们的 20 片段协议上，Lite 损失 2.0 dB；其 README 报告的是 1.25 dB。** 其论文在真实数据集上的结果（UCF-101 与 DAVIS 上约 −3 dB）与我们的测量一致。

## 全栈 NVFP4[#](#the-whole-stack-in-nvfp4)

解码器完成后，FastH3 文生视频的每一个大组件都以 NVFP4 运行：文本编码器、transformer 与 VAE 解码器。下面是相比同一模型保持 BF16 的收益。

![FastH3 文生视频所加载权重的堆叠柱状图：同一模型 BF16 为 118.3 GiB，FastH3-QAD-v2 NVFP4 栈为 30.0 GiB。](img/fig_stack_size.svg)

图 3. 文生视频加载的权重，按组件划分。

| 组件 | 同一模型 BF16 | FastH3-QAD-v2 栈 | 缩小倍数 |
| --- | --- | --- | --- |
| Transformer 线性层（21.2B 参数） | 39.5 GiB | 11.1 GiB，NVFP4 | 3.6× |
| Timestep（AdaLN）投影（13.0B） | 24.2 GiB | 0.14 GiB，预计算表 | 170× |
| 其他 transformer 权重（0.8B） | 1.6 GiB | 1.6 GiB，BF16 | — |
| 文本编码器，Qwen3-VL，50 层（25.8B） | 48.0 GiB | 15.3 GiB，NVFP4 | 3.1× |
| VAE 解码器（2.4B） | 4.5 GiB | 1.29 GiB（36 层）/ 0.31 GiB（8 层） | 3.5× / 15× |
| 音频 VAE | 0.6 GiB | 0.6 GiB | — |
| 合计 | 118.3 GiB | 30.0 GiB / 29.0 GiB | 3.9× / 4.1× |

* **NVFP4 把一个权重存成约 4.5 bit**（4-bit 数值，加上每 16 个值共享一个 FP8 缩放），因此 4-bit 层比 BF16 小约 3.6 倍。
* **timestep 投影根本没有量化。** FastH3 在固定的八步调度上采样，因此它们的输出被一次性预计算成一张 155 MB 的表，24 GiB 的权重从不加载。
* **保持 BF16 的部分**都很小且敏感：归一化、嵌入、输入与输出投影、文本编码器的视觉塔，以及音频 VAE。
* **BF16 那一列是 FastH3 实际运行的同一批层。** H3 读取其 64 层 Qwen3-VL 文本编码器的第 50 层，所以我们只保留这 50 层。BF16 H3 检查点发布时为 137.7 GiB，因为它还带着最后 14 层编码器、语言模型头，以及 FP32 的 VAE 编码器与解码器。
* **并非所有内容都同时驻留 GPU。** 在 32 GB 的 RTX 5090 上，transformer（12.7 GiB）与解码器常驻 GPU，文本编码器从主机内存逐层流式加载，timestep 投影从不加载。DGX Spark 把所有内容都放在 128 GB 统一内存里。

### 端到端延迟[#](#end-to-end-latency)

协议与上一篇相同：热启动服务器上从提示词到成品 MP4 的端到端时间，四次运行的中位数，不含模型加载。图中使用 FP4 VSA 注意力路径。

![双面板分组柱状图。上：V2、带 36 层解码器的 FastH3-QAD-v2、带 8 层解码器的 FastH3-QAD-v2 的 5 秒 832×480 片段。下：两个 FastH3-QAD-v2 解码器配置下的 10 秒 1344×768 片段。对数刻度。](img/fig_e2e.svg)

图 4. 含音频的端到端时间。上：5 秒、832×480 片段。下：10 秒、1344×768 片段。每行是一台机器；所有时间都使用 FP4 VSA。

## 社区 LoRA[#](#community-loras)

H3 社区已经发布了许多 LoRA，从运镜到胶片质感都有。它们大多使用 ComfyUI 或训练器布局。FastVideo 可以直接加载，在 NVFP4 模型上也可以：

```
from fastvideo import VideoGenerator
from fastvideo.api import ComponentConfig, GeneratorConfig, PipelineSelection

generator = VideoGenerator.from_config(
    GeneratorConfig(
        model_path="FastVideo/FastH3-QAD-v2",
        pipeline=PipelineSelection(
            components=ComponentConfig(lora_path="pablodawson/MiniMax-H3-360-Orbit-LoRA", lora_strength=0.8),
        ),
    ))
```

* **格式：** ComfyUI、fal、ai-toolkit 与 musubi-tuner 布局，支持 `lora_A/lora_B` 或 `lora_down/lora_up` 因子以及逐层 alpha。
* **在 4-bit 模型上：** NVFP4 与 FP8 权重保持打包、不被改动；每个 LoRA 作为其所在层旁边的一个 bf16 小分支运行。强度 0 精确复现基础模型，强度可在运行时调整。
* **清晰的加载错误：** 若某个 LoRA 没有匹配任何层、或匹配得过少，会报错并列出未匹配项，而不是静默返回基础模型。

大多数社区 LoRA 针对基础 H3 的 50 步调度。FastH3 以八步采样，因此风格与运动类 LoRA 通常能沿用，但最佳强度可能不同。Turbo LoRA 没有必要。

## 明天：FastH3 Omni[#](#tomorrow-fasth3-omni)

明天我们将发布 **FastH3 Omni**：通用模型及其训练代码（BF16），外加一个消费级硬件版本。消费级版本使用上述 QAD 配方（扩展到 4-bit 注意力）与 NVFP4 解码器。

## 已知局限[#](#known-limitations)

* **8 层解码器用质量换速度。** 细节重要时请使用 36 层解码器。
* **NVFP4 解码器需要 Blackwell GPU：** RTX 50 系列、RTX PRO 6000、DGX Spark，或 B200/GB200。
* **FastH3 Trim 上的 LoRA 暂不支持。** Trim 移除了 transformer 块，因此基于完整 H3 训练的 LoRA 与其层对不上。

## 获取模型[#](#get-the-models)

|  |  |
| --- | --- |
| FastH3-QAD-v2, NVFP4（RTX 5090、RTX PRO 6000、DGX Spark） | [`FastH3-QAD-v2`](https://huggingface.co/FastVideo/FastH3-QAD-v2) |
| NVFP4 VAE 解码器：`quality-36L/` 与 `fast-8L/` | [`FastH3-NVFP4-VAE-Decoder`](https://huggingface.co/FastVideo/FastH3-NVFP4-VAE-Decoder) |

## 致谢[#](#acknowledgements)

FastH3 构建于 [MiniMax H3](https://huggingface.co/MiniMaxAI/MiniMax-H3) 之上；感谢 MiniMax 团队发布其权重与代码。感谢 [LightX2V](https://github.com/ModelTC/LightX2V) 团队发布 LightVAE 及其基准代码，使公平比较成为可能；也感谢 H3 社区提供的 LoRA。

感谢 NVIDIA Enterprise Products 团队（Pengcheng Li 与 Cliff Woolley）提供 Video Sparse Attention kernel，感谢 FlashInfer 与 NVIDIA Model Optimizer 团队提供 FP4 kernel 与校准工具。我们还要感谢 [Nuva Lab](https://nuvalab.ai/)、[NVIDIA FastGen](https://github.com/NVlabs/FastGen)、[vLLM 项目](https://vllm.ai/)、[NVIDIA](https://www.nvidia.com/en-us/) 与 [MBZUAI](https://mbzuai.ac.ae/) 的合作与支持。

## FastVideo 团队[#](#fastvideo-team)

**贡献者：** [Aryan Kumar](https://github.com/aryan5v)

  
**技术负责人：** [Will Lin](https://github.com/SolitaryThinker)

  
**指导：** [Hao Zhang](https://github.com/zhisbug)
