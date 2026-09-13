---
title: "vLLM-Omni 上的 MiniMax H3：从全系统优化到用 FastVideo 的 FastH3 实现实时服务"
title_en: "MiniMax H3 on vLLM-Omni: From System-Wide Optimization to Real-Time Serving with FastVideo's FastH3"
source: https://vllm.ai/blog/2026-09-01-minimax-h3-production-serving
crawled: 2026-09-12
translated: 2026-09-13
---

# vLLM-Omni 上的 MiniMax H3：从全系统优化到用 FastVideo 的 FastH3 实现实时服务

> 原文：[MiniMax H3 on vLLM-Omni: From System-Wide Optimization to Real-Time Serving with FastVideo's FastH3](https://vllm.ai/blog/2026-09-01-minimax-h3-production-serving) · vLLM 博客

作者：vLLM-Omni 团队

[#性能](https://vllm.ai/blog/tags/performance)[#大规模服务](https://vllm.ai/blog/tags/large-scale-serving)[#多模态](https://vllm.ai/blog/tags/multimodal)[#vllm-omni](https://vllm.ai/blog/tags/vllm-omni)[#fastvideo](https://vllm.ai/blog/tags/fastvideo)[#fasth3](https://vllm.ai/blog/tags/fasth3)

> 一个两阶段的优化故事：先降低完整 MiniMax H3 服务栈各处的开销，再集成 FastVideo 的四步 FastH3，让完整 MP4 的生成快于其播放时长。

MiniMax H3 的服务是一个系统性问题。一个请求要跨越庞大的 Qwen3-VL 编码器、长序列音视频 DiT、相互独立的视频与音频 VAE、设备与进程边界，最终还要完成 H.264/AAC 封装。只优化 DiT，其余环节仍会留下可观的延迟。

因此，[vLLM-Omni](https://github.com/vllm-project/vllm-omni) 从完整的常驻流水线入手：注意力与通信、融合 DiT 算子、并行 VAE 解码、紧凑输出传输以及并行 MP4 构建。[FastVideo](https://github.com/hao-ai-lab/FastVideo) 的 [FastH3](https://haoailab.com/blogs/fasth3-preview/) 随后攻克剩下的主导项，把 49 次 DiT 前向减少为 4 次。

在实测的八卡 B300 配置上，FastH3 在 **8.678-8.710 秒**内生成了完整的 10.125 秒 MP4。在本文中，**实时**指完整响应的准备速度快于其播放时长，并不是指流式传输或首帧延迟。

## 1. 为什么 MiniMax H3 服务是一个全系统问题

MiniMax H3 从文本、图像、视频和音频参考出发，联合生成视频与同步音频。其各个组件在计算、内存和部署位置上有着不同的要求：

```
request -> encoder -> joint audio/video DiT -> video + audio VAEs
        -> GPU output preparation -> D2H/IPC -> H.264/AAC MP4
```

![](https://vllm.ai/blog-assets/figures/2026-08-29-minimax-h3-production-serving/h3-model-pipeline.svg)

*图 1：文本使用 H3/Qwen3-VL 编码器；视觉与音频条件也使用各自对应的 VAE。条件信息与带噪目标潜变量组成一个打包序列，用于音视频联合去噪，随后分别进行解码与 MP4 构建。来源：[MiniMax H3 模型卡](https://huggingface.co/MiniMaxAI/MiniMax-H3)、[vLLM-Omni 配方](https://github.com/vllm-project/vllm-omni/blob/main/recipes/MiniMaxAI/MiniMax-H3.md)与 [Diffusers 流水线](https://huggingface.co/docs/diffusers/main/en/api/pipelines/minimax_h3)。*

已发布的检查点覆盖三类服务任务：

| 任务 | 输入 | 典型用途 |
| --- | --- | --- |
| T2VA | 文本 | 创意生成与合成媒体 |
| FL2VA | 文本加首/尾帧图像 | 受控过渡与图像动画 |
| Ref2VA | 混合的图像、视频与音频参考 | 一致性编辑与参考引导生成 |

DiT 在基础调度中占主导，但它并非唯一瓶颈。编码器的常驻影响容量；去噪被缩短之后，VAE 解码开始显眼；而原始帧仍要跨越进程边界并变成 MP4。这就是为什么故事要从全系统优化讲起。

## 2. 基准测试契约与证据边界

本文将两条证据线分开：

| 证据线 | 目的 |
| --- | --- |
| 基础 H3：Diffusers 对比 vLLM-Omni | 在 50 步稠密 BF16 调度下度量全系统运行时优化 |
| FastH3 时长扫描 | 以 4 次 DiT 前向度量绝对低延迟与完整响应的实时表现 |

两条证据线使用的都是有效且冻结的实验，但源 SHA、提示词、种子和产物并不相同。因此我们**不会**推导基础版到 FastH3 的加速比。在可用的匹配 A/B 出现之前，本文只报告 FastH3 的绝对延迟。

### 2.1 冻结的控制变量

| 控制变量 | 基础 H3 系统线 | FastH3 线 |
| --- | --- | --- |
| 硬件 | 8x NVIDIA B300 | 8x NVIDIA B300 |
| 任务 | T2VA 至 FL2VA 分区 | 仅 Dense/Data-Free T2VA |
| 分辨率 / 帧率 | 1344x768 / 24 FPS | 1344x768 / 24 FPS |
| 源码 | vLLM-Omni [`b81aeb7`](https://github.com/vllm-project/vllm-omni/commit/b81aeb7b86837f6fe8956f3aef83798ad26c5a26) | vLLM-Omni [`86b85c07`](https://github.com/vllm-project/vllm-omni/commit/86b85c078bc041e04aee4c4d9167fb10fb1994c7) |
| 模型 | MiniMax H3 [`42ed227e`](https://huggingface.co/MiniMaxAI/MiniMax-H3/tree/42ed227ee7df40d41602854ae760620d6eb651fe) | 相同基础模型加固定的 FastH3 产物 |
| 提示词 / 种子 | 官方 `case-T2VA` 扩展提示词，SHA-256 `98f36b...f06`；种子 0 | 固定 FastH3 提示词；种子 1101 |
| 调度 | 50 个 sigma 点 / 49 次 DiT 前向 | 5 个 sigma 点 / 4 次 DiT 前向 |
| 拓扑 | 编码器 TP8；DiT USP8、Ring1；VAE PP8 tile | 单副本；编码器 TP8；DiT USP8、Ring1；VAE PP8 tile |
| 注意力 | 稠密 BF16 `TRTLLM_ATTN`，Fast Ulysses | 稠密 `TRTLLM_ATTN`，Fast Ulysses |
| 重复 | 排除一次完整形状的预热，然后是计量请求 | 每个形状排除一次可行性请求，随后每个时长进行两次交错运行 |

两条线都从同步提交请求开始计时，直到收到完整 MP4。下载、启动、编译以及被排除的预热都在该区间之外。每个被接受的输出必须能解码为 H.264 视频加立体声 32 kHz AAC，包含预期的帧数与帧率，视频方差和音频 RMS 非零，并通过提示词符合性审查。

对 FastH3，取经过验证的视频与音频流时长，并定义 `T_media = max(T_video, T_audio)`，即有效完整 MP4 播放时长：

`RTF_client = T_client / T_media`

`RTF_client <= 1.0` 是完整响应的实时判据。媒体检查失败、音频缺失、OOM、加速器错误或意外回退都会让该配置在重复测量之前终止。

其他硬件有意作为配方覆盖，而非另一张结果矩阵：[H200 与数据中心 CUDA](https://github.com/vllm-project/vllm-omni/blob/main/recipes/MiniMaxAI/MiniMax-H3.md)、[RTX PRO 5000](https://github.com/vllm-project/vllm-omni/blob/main/recipes/MiniMaxAI/MiniMax-H3-RTX-PRO-5000.md)、[RTX 4090](https://github.com/vllm-project/vllm-omni/blob/main/recipes/MiniMaxAI/MiniMax-H3-4090.md)、[RTX 5090](https://github.com/vllm-project/vllm-omni/blob/main/recipes/MiniMaxAI/MiniMax-H3-5090.md)、[GB10](https://github.com/vllm-project/vllm-omni/blob/main/recipes/MiniMaxAI/MiniMax-H3-Spark-GB10.md) 与 [ROCm](https://github.com/vllm-project/vllm-omni/blob/main/recipes/MiniMaxAI/MiniMax-H3.md#amd-rocm-gfx942--gfx950)。

## 3. 用 vLLM-Omni 做全系统优化

基础 H3 线保留已发布的 BF16 权重、50 个 sigma 点以及稠密注意力覆盖。这些优化沿着执行路径展开，而不是罗列功能清单。

### 3.1 长序列注意力与通信

H3 把文本、音频和视频 token 作为一条长的打包序列去噪。对于典型工作负载，58,758 个有效 token 占用一个 58,816 token 的对齐缓冲区。vLLM-Omni 在三个边界上降低开销：

- [`TRTLLM_ATTN`](https://github.com/vllm-project/vllm-omni/pull/5283) 接收有效序列长度，[打包序列精化](https://github.com/vllm-project/vllm-omni/pull/5779)去除结构性的后缀填充。
- [rank 本地边界](https://github.com/vllm-project/vllm-omni/pull/6173)只构造本地 embedding/RoPE 行，并聚合紧凑的 128 通道投影，而不是 5,376 通道的隐藏状态。
- [Fast Ulysses](https://github.com/vllm-project/vllm-omni/pull/6340) 使用 NCCL SymmetricMemory 以注意力所需的布局交换分片，免去了 all-to-all 周围单独的重排布。

### 3.2 融合 DiT 算子

49 次前向的循环在矩阵乘法周围反复执行小操作。vLLM-Omni 将 Q/K RMSNorm 与 RoPE 融合（[#5990](https://github.com/vllm-project/vllm-omni/pull/5990)），把 FP32 调制、归一化与残差计算合并（[#6281](https://github.com/vllm-project/vllm-omni/pull/6281)、[#6878](https://github.com/vllm-project/vllm-omni/pull/6878)），并用融合 SwiGLU 取代分离的 SiLU 与乘法启动（[#6283](https://github.com/vllm-project/vllm-omni/pull/6283)）。

### 3.3 并行与融合的 VAE 解码

去噪之后，H3 独立解码视频与音频。VAE patch 并行把分块的视频解码器分布到八块 GPU 上。[精确 VAE 算子路径](https://github.com/vllm-project/vllm-omni/pull/6607)加速了解码器块的物化、融合的 Q/K 归一化与 RoPE、融合 SwiGLU 以及带缩放的残差更新，对不支持的布局则回退到 eager 执行。

### 3.4 GPU 输出准备、传输与 MP4

直到数百帧离开 GPU，一个请求才算完成。优化后的路径让每次转换只执行一次：

1. [GPU 输出准备](https://github.com/vllm-project/vllm-omni/pull/6824)把解码后的 FP32 BCTHW 帧转换为连续的 uint8 BTHWC，在传输之前将视频负载减少 75%。
2. 锁页 D2H 与 worker 到引擎的 IPC 传输紧凑负载。
3. [直接平面编码](https://github.com/vllm-project/vllm-omni/pull/6288)、[持久并行转换器](https://github.com/vllm-project/vllm-omni/pull/6499)以及对[传输过来的跨步 RGB 平面](https://github.com/vllm-project/vllm-omni/pull/6776)的支持直接为 H.264 提供输入，无需再构造一份完整的交错 RGB 缓冲区。

`FP32 BCTHW -> uint8 BTHWC -> pinned D2H/IPC -> planar frames -> H.264/AAC MP4`

### 3.5 实测基础 H3 结果

两个运行时都使用八块 B300 GPU、相同的提示词与种子、50 个 sigma 点以及同样的完整 MP4 边界。Diffusers 使用复制权重加原生上下文并行；vLLM-Omni 使用编码器 TP8、带 Fast Ulysses 的 DiT USP8/Ring1、VAE PP8 tile 解码以及 `TRTLLM_ATTN`。

| 运行时 | 模型执行（s） | 提示词（s） | DiT 总计 / 每次前向（s） | 视频 / 音频 VAE（s） | MP4（s） | 客户端 E2E（s） | 每 rank 峰值 HBM（GiB） |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Diffusers | - | - | - | - | - | **82.239** | 151.699 |
| vLLM-Omni | **54.246** | 0.057 | 51.800 / 1.057 | 0.952 / 0.055 | 1.528 | **56.917** | 128.232 |

[视频]()

**MiniMax-H3 模型卡示例** · [打开 MP4](https://huggingface.co/MiniMaxAI/MiniMax-H3/resolve/main/assets/t2va.mp4)

[视频]()

**vLLM-Omni 基线** · [打开 MP4](https://vllm-project.github.io/assets/figures/2026-08-29-minimax-h3-production-serving/evidence/b300/trtllm_dense.mp4)

借助无损优化，vLLM-Omni 相比 Diffusers 将完整响应延迟降低 **30.8%**，即 **1.445x** 加速。这里「无损」指加速不依赖量化、稀疏注意力、缓存复用或更少的去噪步数，但并不意味着输出逐位相同：不同的内核实现与浮点归约顺序仍可能扰动扩散轨迹。

> 这些改进降低的是去噪周围的开销。FastH3 则把去噪循环本身从 49 次前向压缩到 4 次，从而攻击剩下的主导项。

## 4. 扩展通用 H3 服务架构

通用 H3 线组合了两类不同的生产控制。DLO 与分离式编码改变容量与部署位置；可选的量化权重与近似注意力则以数值保真度换取内存或延迟。这些路径说明了如何适配、扩展并加速更广泛的架构。它们**并未**产生第 6 节中的 FastH3 数字。

### 4.1 分布式分层卸载（Distributed Layerwise Offload）

[DLO](https://vllm.ai/blog/2026-08-17-distributed-layerwise-offload) 在 HBM 中保留一个有界的 DiT 层窗口，其余层则从主机内存流式读取。AllGather 模式从主机分片集体重建活跃层；rank 本地模式流式读取每个 rank 常规加载器产生的张量。正确的选择取决于互连、主机带宽、内存、常驻层数量和请求并发。

![](https://vllm.ai/blog-assets/figures/2026-07-30-distributed-layerwise-offload/dlo_pipeline_last_frame.png)

*图 2：DLO 在当前层计算的同时准备下一层。机制与部署权衡见[专门的 DLO 文章](https://vllm.ai/blog/2026-08-17-distributed-layerwise-offload)。*

#### 8× B300 BF16 DLO 帕累托前沿

在官方 BF16 MiniMax-H3 FL2VA 检查点上（5.175 s，1344×768，SP8/Ulysses8/Ring1/DP1/TP1，AllGather，CUDNN 注意力），第一个请求因惰性 CUDA/cuDNN/JIT 工作被排除，其余两个请求取平均。生成的视频与音频具有预期的输出形状。

![](https://vllm.ai/blog-assets/figures/2026-08-29-minimax-h3-production-serving/b300-dlo-pareto.svg)

*图 3：延迟–内存帕累托前沿。*r* 是常驻 DiT 块的数量。实心点为非支配测量值；空心点为被支配测量值。在 *r* = 35 时，DLO 以 5.1% 的延迟代价将报告的 HBM 降低 37.5%；*r* = 0 是最小内存端点。*

### 4.2 分离式编码

H3 以 BF16 保留约 51.5 GB 的 Qwen3-VL 编码器权重。[分离式编码器路径](https://github.com/vllm-project/vllm-omni/pull/5885)把这个一次性编码器移入独立的 vLLM 阶段，拥有自己的部署位置、张量并行、副本、队列、内核和前缀缓存。编排器在 DiT/VAE 阶段之前，将其第 50 层隐藏状态与 token 角色标签同原始媒体组合。

![](https://vllm.ai/blog-assets/figures/2026-08-29-minimax-h3-production-serving/h3-encoder-disaggregation.svg)

*图 4：编码器与扩散的容量独立扩展。合并后的单节点配方通过编排器返回条件信息，并让扩散阶段保持内联；它不配置 OmniConnector。SHM/RDMA 仍是 [RFC #5707](https://github.com/vllm-project/vllm-omni/issues/5707) 中未来的跨节点选项。*

### 4.3 可选的量化与注意力加速

第 3 节刻意使用稠密 BF16 注意力和已发布检查点的精度。通用 H3 部署可以选择以下附加路径，但每一条都是独立的质量-性能配置，而非无损的运行时收益。

#### 权重与激活值量化

- **在线 FP8。** 合并的[全局 FP8 路径](https://github.com/vllm-project/vllm-omni/pull/5910)从 BF16 检查点出发，在加载时对符合条件的 DiT 与 Qwen3-VL 文本解码器线性层进行量化。embedding、归一化、RoPE、视觉塔、两个 VAE 以及对精度敏感的投影保持其声明的精度。
- **SVDQuant NVFP4 W4A4。** 合并的[离线加载器](https://github.com/vllm-project/vllm-omni/pull/6162)将 NVFP4 W4A4 基础 GEMM 与 BF16 低秩校正相结合。当前证据确立了检查点与正确性兼容性；原生的融合残差-GEMM 性能路径仍是未来工作。

![](https://vllm.ai/blog-assets/figures/2026-08-29-minimax-h3-production-serving/h3-quantization-paths.svg)

*图 5：在线 FP8 在加载时创建 FP8 权重与缩放因子，然后在线量化符合条件的激活值。离线 SVDQuant 将 NVFP4 W4A4 基础分支与 BF16 低秩校正结合。来源：vLLM-Omni [#5910](https://github.com/vllm-project/vllm-omni/pull/5910) 与 [#6162](https://github.com/vllm-project/vllm-omni/pull/6162)，以及 cookbook 中的[在线 FP8](https://github.com/hsliuustc0106/vllm-omni-cookbook/blob/main/blog/_posts/2026-08-18-online-quantization-fp8.md) 与 [SVDQuant](https://github.com/hsliuustc0106/vllm-omni-cookbook/blob/main/blog/_posts/2026-08-16-understanding-pr-6162-svdquant-w4a4-blackwell.md) 说明文章。*

量化配置必须报告峰值 HBM、启动主机内存、检查点存储、延迟以及同种子视频/音频质量。容量上的收益并不自动等于延迟收益，加载器的正确性也不是融合内核收益的证据。

#### B300 在线 FP8 的容量与延迟

下面的稠密、常驻结果将在线 FP8 与已发布的 BF16 检查点单独对比。两行都使用 8 块 B300 GPU、带 Fast Ulysses 的 Ulysses8/Ring1、编码器 TP8、VAE PP8 tile 解码、CUDNN 注意力，以及请求 50 个 sigma 点（49 次 DiT 前向）的 10 秒 1344×768 / 24 FPS 请求。排除一次预热；每个数值是三次计量请求的均值。「阶段生成」是原生扩散阶段计时器；E2E 是离线客户端挂钟时间，直到返回视频与音频张量，不含 MP4 封装。

| 权重 | 阶段生成（均值，n=3） | E2E（均值，n=3） | 每 rank 峰值 HBM | 结果 |
| --- | --- | --- | --- | --- |
| BF16 | 52.572 s | 53.118 s | 87.16 GiB | 无损基线 |
| 在线 FP8 | **49.769 s** | **50.331 s** | **53.27 GiB** | 阶段时间降低 5.3%；峰值 HBM 降低 38.9% |

每个计量请求都返回 1344×768 的 243 帧 RGB 与 32 kHz 立体声音频。三次重复使用不同种子，用以确立输出形状与生成成功，而非与 BF16 逐像素等价。

#### `TRTLLM_ATTN` 中的量化与稀疏注意力

`TRTLLM_ATTN` 提供两种可选的有损加速模式：

- **SAGE 量化**将 QK 与 PV 两条路径都量化为 FP8。
- **Skip-Softmax** 利用 QK 结果动态跳过不重要的 Softmax 与 P×V 计算。

![](https://vllm.ai/blog-assets/figures/2026-08-29-minimax-h3-production-serving/trtllm-sage-skip-softmax.jpg)

*图 6：SAGE 将 Q、K、P、V 量化为 FP8 用于 Q×K 与 P×V，而 Skip-Softmax 使用 [BLASST](https://arxiv.org/abs/2512.12087) 的 tile 级决策绕过选定的 Softmax 与 P×V tile。*

下表将视频质量与加速比同稠密、未量化的注意力基线进行对比：

| 注意力策略 | SAGE 配置 | Skip-Softmax 配置 | 模型执行 | 加速比 | 相对基线 LPIPS |
| --- | --- | --- | --- | --- | --- |
| TRTLLM 基线 | 关闭 | 关闭 | 54.246 s | 1.000x | 0 |
| SAGE FP8 | `dtype_qk=fp8_e4m3`、`q_block_size=1`、`k_block_size=16` | 关闭 | 44.787 s | **1.211x** | 0.3697 |
| Skip-Softmax | 关闭 | 阈值 0.05；在 0.97 之前禁用 | 50.029 s | **1.084x** | 0.0917 |
| SAGE + Skip-Softmax | `dtype_qk=fp8_e4m3`、`q_block_size=1`、`k_block_size=16` | 阈值 0.05；在 0.97 之前禁用 | 43.867 s | **1.237x** | 0.3750 |

[视频]()

**TRTLLM 基线**

[视频]()

**SAGE**

[视频]()

**Skip-Softmax**

[视频]()

**SAGE + Skip-Softmax**

实测的 Skip-Softmax 配置在保住视频质量方面是**保守**的。用户可以选择更高的阈值，或在更多去噪步数上启用 Skip-Softmax，用质量换取额外速度。[TRTLLM 注意力指南](https://github.com/vllm-project/vllm-omni/blob/main/docs/user_guide/diffusion/attention_backends/trtllm.md)记录了这些控制项。

#### Cache-DiT

[Cache-DiT](https://github.com/vllm-project/vllm-omni/pull/5853) 是请求级缓存策略而非注意力后端。对 H3，`quality=high` 启用动态的每步复用，`quality=lossless` 则恢复参考路径。其命中/未命中行为依赖部署情况，因此需要独立的延迟与质量验证，未包含在上面的注意力 A/B 中。

### 4.4 兼容性边界

| 组合 | 本文中的状态 |
| --- | --- |
| 基础 H3 + DLO | 通过维护中的 H3 配方支持；在本地对所选拓扑做验证 |
| 基础 H3 + DLO + 在线 FP8 | 支持，包括经 [#6279](https://github.com/vllm-project/vllm-omni/pull/6279) 的 AllGather 路径；性能与质量仍需本地验证 |
| 基础 H3 + 分离式编码器 | 已合并的单节点路径 |
| FastH3 + DLO | **不支持**：FastH3 融合发生在 `load_weights()` 中，而卸载安装的是另一条主机权重路径 |
| FastH3 + VSA | 在 CUDA 上配合匹配的 VSA 产物、`fastvideo-kernel`、`FASTVIDEO_VSA` 以及本地或纯 Ulysses 注意力时受支持；拒绝 Ring 与 AllGather SP |
| FastH3 + 分离式编码器 | **尚未验证**；报告的 FastH3 结果并未使用它 |

> **步骤执行旁注。** H3 可以在去噪步骤之间接纳和中止请求（[#5810](https://github.com/vllm-project/vllm-omni/pull/5810)），但现有的共同批处理测试并未改善延迟。在 [issue #5700](https://github.com/vllm-project/vllm-omni/issues/5700) 调查取消/回收以及小型低利用工作负载期间，仍推荐请求模式。

## 5. 从系统优化到 FastH3

[FastH3](https://haoailab.com/blogs/fasth3-preview/) 是 FastVideo 针对 MiniMax H3 的四步 DMD2 学生模型。它复用 H3 的编码器、视频 VAE、音频 VAE、分词器和调度器，但把去噪循环缩减为五个 sigma 位置上的四次 transformer 前向。vLLM-Omni 同时支持 Dense/Data-Free 产物与推荐的 VSA/Data-Free 产物。

这次集成是跨两个层次的协作：

- **FastVideo** 开发并发布蒸馏后的学生模型与适配器产物。
- **vLLM-Omni** 验证该产物，在检查点流入的同时完成融合，对融合后的权重做分片，并通过优化过的注意力、VAE、传输与 MP4 路径提供服务。

FastH3 并不是普通的可按请求切换的 LoRA。除低秩因子外，其产物还携带满秩增量与替换权重，这是普通 LoRA 层无法表达的。因此 vLLM-Omni 在分片之前先融合该产物，而不是按请求激活它。

![](https://vllm.ai/blog-assets/figures/2026-08-29-minimax-h3-production-serving/h3-few-step-adapters.svg)

*图 7：Turbo 保持基础权重不变，应用按请求选择的 A/B 旁挂文件。FastH3 在分片之前把低秩与满秩更改融合进一个专属学生模型。来源：Turbo [#6476](https://github.com/vllm-project/vllm-omni/pull/6476)、DLO 支持 [#6550](https://github.com/vllm-project/vllm-omni/pull/6550) 与 FastH3 集成 [#6714](https://github.com/vllm-project/vllm-omni/pull/6714)，VSA 与 Ulysses 支持见 [#6909](https://github.com/vllm-project/vllm-omni/pull/6909)。*

| 配置 | 激活模型 | 任务范围 | 何时选择 |
| --- | --- | --- | --- |
| 基础 H3 | 已发布检查点 | T2VA、FL2VA、Ref2VA | 完整任务覆盖，并与通用扩展线兼容 |
| Turbo | 可按请求切换的适配器 | T2VA 与 FL2VA | 同一服务需要请求时切换或 FL2VA |
| FastH3 | 加载时融合的专属学生模型 | Dense/Data-Free 或 VSA/Data-Free 的 T2VA | 专用 T2VA 端点上的最低已验证延迟；VSA 可选择性地稀疏化主 DiT 注意力 |

FastH3 v1 只接受 T2VA，要求其四次前向的调度与检查点 flow shift，拒绝卸载，并且不能接受另一个请求时 LoRA。其 VSA 变体还要求 CUDA、外部的 FastVideo 内核包以及本地或纯 Ulysses 序列并行。这些是服务契约，不是调参建议。

## 6. B300 上的实时 FastH3 服务

本节报告 vLLM-Omni `86b85c07` 上的 FastH3 绝对结果。它不会除以来自不同源/提示词/种子的基础 H3 结果。

### 6.1 固定产物版本

实测的 Dense/Data-Free 产物固定在 Hugging Face revision `bcf40ca6f457ed66f8badf13514943e390205fca`：

```
FASTH3_REV=bcf40ca6f457ed66f8badf13514943e390205fca
FASTH3_DIR=/models/FastH3-LoRA

hf download FastVideo/FastVideo-FastH3-4-step-Preview-v1-LoRA \
  dense-datafree/adapter_model.safetensors \
  --revision "$FASTH3_REV" \
  --local-dir "$FASTH3_DIR"

echo "4ce198c83132251b7fd0de2503823aa49c53983f068318f66cb19eaefb7fcc12  $FASTH3_DIR/dense-datafree/adapter_model.safetensors" \
  | sha256sum -c -
```

该适配器为 1,485,626,152 字节。请同时固定仓库 revision 与文件校验和；仓库名称仍带有 `Preview-v1`，而对应的 vLLM-Omni 集成已合并。

### 6.2 启动服务并发起请求

```
CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 \
VLLM_WORKER_MULTIPROC_METHOD=spawn \
VLLM_OMNI_VIDEO_SYNC_TIMEOUT=1800 \
vllm serve "$H3_MODEL" --omni \
  --host 127.0.0.1 --port 8095 --trust-remote-code \
  --task-type fl2va --served-model-name MiniMaxAI/MiniMax-H3 \
  --num-gpus 8 --usp 8 --ring 1 --ulysses-a2a-permute \
  --text-encoder-tp-size 8 \
  --vae-patch-parallel-size 8 --vae-parallel-mode tile --vae-use-tiling \
  --diffusion-attention-backend TRTLLM_ATTN \
  --lora-path "$FASTH3_DIR/dense-datafree/adapter_model.safetensors"
```

```
curl -sS -X POST http://127.0.0.1:8095/v1/videos/sync \
  -F 'prompt=In a snowy blue-purple forest, Ori carefully walks past a sleeping giant; footsteps crunch in the snow while the creature breathes and softly snorts.' \
  -F 'width=1344' -F 'height=768' -F 'aspect_ratio=16:9' -F 'fps=24' \
  -F 'num_inference_steps=4' -F 'seed=1101' \
  -F 'extra_params={"task":"t2va","duration":10.0,"flow_shift":12.0,"audio_flow_shift":3.0}' \
  -o fasth3_10s.mp4
```

该服务使用一个 FastH3 副本、编码器 TP8、带 Ring1 与 Fast Ulysses 的 DiT DP1 x TP1 x USP8、VAE PP8 tile 解码、`TRTLLM_ATTN`，以及标准的紧凑输出/MP4 路径。

### 6.3 十秒关键路径

性能剖析计时来自单独的插桩运行；干净的 E2E 才承载延迟结论。

> **原始基准测试数据包——等待发布关卡。** 稳定的数据包尚未发布。发布之前，这条[证据移交要求](https://github.com/vllm-project/vllm-project.github.io/pull/315#issuecomment-5459581336)必须替换为一个数据包 URL，其中包含原始的干净/剖析样本、日志、环境清单、媒体元数据与哈希，以及关键路径行和时长扫描两者的拓扑证据。

| 编码器 | DiT 总计 / 4 次 / 每次前向 | 视频 + 音频 VAE | 推导传输 | CPU MP4 | 剖析 E2E | 干净 E2E | 峰值 HBM |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0.052 s | 5.532 s / 4 / 1.383 s | 1.247 s 合计 | 0.881 s | 0.868 s | 8.629 s | **8.678 / 8.710 s** | 94.1 GiB/GPU 保留 |

### 6.4 五秒、十秒与十五秒扫描

扫描保持提示词、种子、分辨率、产物、调度、拓扑、注意力、VAE、输出路径与 CPU 亲和性固定。H3 将请求的时长对齐到 124、243 和 362 帧。

| 请求 / 对齐时长 | 视频 / 音频时长 | DiT 总计 / 每次前向 | VAE 合计 | 传输 + MP4 | 干净 E2E | 客户端 RTF | 实时倍数 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 5 s / 124 | 5.167 / 5.175 s | 2.806 s / 0.702 s | 0.637 s | 0.929 s | 4.602 / 4.396 s | **0.889 / 0.849** | **1.125 / 1.177** |
| 10 s / 243 | 10.125 / 10.125 s | 5.532 s / 1.383 s | 1.247 s | 1.749 s | 8.678 / 8.710 s | 0.857 / 0.860 | 1.167 / 1.163 |
| 15 s / 362 | 15.083 / 15.083 s | 9.517 s / 2.379 s | 1.861 s | 2.484 s | 14.177 / 14.059 s | 0.940 / 0.932 | 1.064 / 1.073 |

全部六个计量请求都满足 `RTF_client <= 1.0`：在所有测试时长下，完整 MP4 的生成都快于播放。

#### FastH3 Dense 与 VSA 对比

[#6909](https://github.com/vllm-project/vllm-omni/pull/6909) 中另一项匹配研究在 8×B300、1344×768、24 FPS 条件下比较 Dense/Data-Free 产物与推荐的 VSA/Data-Free 产物。两者都使用四次 transformer 前向、纯 Ulysses 8，并丢弃一次预热；下表每个结果对应每个后端与时长的一次计量请求。Dense 使用 `TRTLLM_ATTN`；VSA 使用 `FASTVIDEO_VSA`、top-k 64 与 Triton 内核路径。

| 请求 | FastH3 Dense 服务端 E2E（含 MP4） | FastH3 VSA 服务端 E2E（含 MP4） | 加速比 |
| --- | --- | --- | --- |
| 10 s | 9.838 s | **7.278 s** | **1.35×** |
| 15 s | 14.199 s | **10.800 s** | **1.31×** |

这些服务端测量确立了匹配条件下的 VSA 加速比；它们使用的源 revision 与计时边界不同于上面的客户端 E2E 时长扫描。VSA 安装、启动命令与回退检查见维护中的 [MiniMax H3 配方](https://recipes.vllm.ai/MiniMaxAI/MiniMax-H3)。

### 6.5 代表性输出与质量边界

这些提供的 FastH3 输出覆盖同样的 5/10/15 秒时长档。它们是 1280x736 的代表性示例，而非第 6.4 节用于计时的 1344x768 产物。

| 请求 | 帧数 | MP4 时长 | 分辨率 / 帧率 |
| --- | --- | --- | --- |
| 5 s | 124 | 5.184 s | 1280x736 / 24 FPS |
| 10 s | 243 | 10.144 s | 1280x736 / 24 FPS |
| 15 s | 362 | 15.104 s | 1280x736 / 24 FPS |

[视频]()

**5 秒** · [打开 MP4](https://vllm-project.github.io/assets/figures/2026-08-29-minimax-h3-production-serving/fast-h3-5s.mp4)

[视频]()

**10 秒** · [打开 MP4](https://vllm-project.github.io/assets/figures/2026-08-29-minimax-h3-production-serving/fast-h3-10s.mp4)

[视频]()

**15 秒** · [打开 MP4](https://vllm-project.github.io/assets/figures/2026-08-29-minimax-h3-production-serving/fast-h3-15s.mp4)

这些片段是展示示例。发布级的计时与媒体证据仍受第 6.3 节原始数据包关卡约束。

| 质量关卡 | 状态 |
| --- | --- |
| 重复的同种子 FastH3 输出 | 在实测运行中逐字节相同 |
| 媒体结构 | 预期的帧数/帧率、H.264、立体声 AAC、非零视频/音频信号 |
| 匹配的基础版与 FastH3 多种子质量 | **待完成；不做一致性声明** |

缩短去噪暴露了新的尾巴：在 10 秒配置上，VAE 合计、推导传输与 CPU MP4 在插桩路径中合计约占三秒。[RFC #6872](https://github.com/vllm-project/vllm-omni/issues/6872) 提议将 VAE 分块、D2H/IPC 与编码相互重叠，而不是孤立地优化这些阶段。对该 B300 配置而言，其乐观上限约为：传输与编码重叠时 0.87 秒（约 10% E2E）；再叠加增量 VAE 解码重叠时 1.75 秒（约 20% E2E）；对应的 go/no-go 目标分别是至少 5% 与 10% E2E。相关草案 [PR #6885](https://github.com/vllm-project/vllm-omni/pull/6885) 报告了一次四卡 L20X 可行性运行中 0.8847 秒（26.57%）的「从 VAE 到完整 MP4」缩短，且媒体完全一致，但这不是 B300 生产服务结果。

## 7. 生产指引与限制

部署选择现在已经具体化：

| 需求 | 推荐配置 |
| --- | --- |
| 完整的 T2VA、FL2VA 与 Ref2VA 覆盖 | 带全系统栈的基础 H3 |
| 请求时适配器切换，或用四次前向 Turbo 处理 FL2VA | 独立的 Turbo 服务 |
| 最低的已验证 T2VA 完整响应延迟 | 第 6 节的专用 FastH3 服务 |
| 为 FastH3 T2VA 提供匹配的稀疏注意力加速 | 带上述约束的专用 VSA/Data-Free 服务 |
| 由主机内存驱动的适配，或独立扩展的编码器容量 | 基础 H3 的 DLO 或分离式编码器线；在本地验证 |

FastH3 VSA 仅在配合其匹配产物、CUDA 内核包、`FASTVIDEO_VSA` 以及本地或纯 Ulysses 注意力时受支持。未经新的正确性、质量、内存与延迟验证，不要把任一 FastH3 配置与 DLO、量化、缓存策略、Ring/AllGather 稀疏注意力或编码器分离组合使用。持续更新的[功能兼容性追踪器](https://github.com/vllm-project/vllm-omni/issues/5700)记录了跨功能的工作，但可能滞后于已合并的实现。在选择生产组合之前，请核实相关 PR 与维护中的配方。

MiniMax H3 采用 [MiniMax H3 社区许可协议](https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/LICENSE)。商业与托管服务运营者应与法务顾问一起审视其当前的地域、署名、营收、可接受使用与安全保障要求。

在后训练方面，vLLM-Omni 还可以在 [VeRL-Omni](https://github.com/verl-project/verl-omni) 中为 H3 rollout 提供服务；训练属于生态覆盖，不属于本服务基准测试的一部分。

## 8. 结论与聚焦的未来工作

全系统优化让完整的 H3 流水线变得高效。FastVideo 的四次前向学生模型进而把专用 T2VA 配置带入快于播放的完整响应生成，实测于上述 B300 系统。

剩余工作直接顺着这一进程展开：

- 在目标 Blackwell 系统上验证原生 FastVideo SM100a VSA 内核，并集成原生融合 NVFP4 内核；
- 集成并验证 [Sol-Attn](https://github.com/vllm-project/vllm-omni/pull/5851) 即时稀疏注意力后端，覆盖目标 Blackwell 平台与多种子工作负载；
- 完成一次匹配条件下的基础版/FastH3 多种子质量评估；
- 实现[分块的「VAE 到传输到 MP4」流水线](https://github.com/vllm-project/vllm-omni/issues/6872)，并验证 GPU 编码器；
- 增强跨 [VeRL-Omni](https://github.com/verl-project/verl-omni)、[UniRL](https://github.com/Tencent-Hunyuan/UniRL) 与 [RLinf](https://github.com/RLinf/RLinf) 的 MiniMax H3 后训练集成，包括可扩展的 rollout 服务、显式资源放置与端到端训练验证；以及
- 验证 FastH3 与编码器分离或其他扩展特性的组合，而不是推断兼容性。

## 致谢

这项工作建立在 vLLM、vLLM-Omni、VeRL-Omni、MiniMax H3、[FastVideo](https://github.com/hao-ai-lab/FastVideo)、FastH3、Diffusers 与 NVIDIA 各方贡献之上。我们特别感谢 FastVideo 团队[开源 FastH3](https://huggingface.co/FastVideo/FastVideo-FastH3-4-step-Preview-v1-LoRA)，并与 vLLM-Omni 社区在合并的服务集成上协作。

我们感谢 [@Isotr0py](https://github.com/Isotr0py) 对基础 H3 的支持；感谢 [@lishunyang12](https://github.com/lishunyang12)、[@evanchueng](https://github.com/evanchueng)、[@Gaohan123](https://github.com/Gaohan123) 与 [@david6666666](https://github.com/david6666666) 在 DLO、基础集成与在线 FP8 方面的工作；感谢 [@gcanlin](https://github.com/gcanlin) 与 [@yuanwu2017](https://github.com/yuanwu2017) 在编码器分离方面的工作；感谢 [@bobboli](https://github.com/bobboli)、[@fan2956](https://github.com/fan2956)、[@mo-ke-ke](https://github.com/mo-ke-ke)、[@mglyn](https://github.com/mglyn)、[@MosCloud](https://github.com/MosCloud) 与 [@ultism](https://github.com/ultism) 在注意力、融合内核、量化、VAE、传输与媒体路径上的贡献；感谢 [@princepride](https://github.com/princepride) 完成 FastH3 集成、B300 验证与 VSA/Ulysses 支持；感谢 [@NancyFyong](https://github.com/NancyFyong) 与 [@mengchengTang](https://github.com/mengchengTang) 完成 VeRL-Omni 集成。

特别感谢 Hongsheng Liu 与 Roger Wang 提供总体支持并准备本博客。

## 附录 A：可复现性

### A.1 计时层级

vLLM-Omni 的测量是嵌套的；父级与子级数值不能相加：

| 边界 | 范围 |
| --- | --- |
| 客户端 | 从请求提交到收到完整 MP4 |
| 请求 | 编排器跨阶段的生命周期 |
| 阶段 | 一个独立调度的引擎/设备组 |
| 引擎 | 排队、模型执行、等待输出就绪与格式化 |
| 剖析器 | 引擎执行内的提示词、DiT 与 VAE 方法边界 |
| 服务器 | 最后阶段之后的 H.264/AAC 编码与封装 |

每次前向的去噪时间除以实际的 DiT 前向次数，而不是请求的 sigma 位置数。剖析器数值来自单独的诊断请求，不能替代未插桩的客户端延迟。

### A.2 基础 H3 的 vLLM-Omni 复现

```
CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 \
VLLM_WORKER_MULTIPROC_METHOD=spawn \
VLLM_OMNI_VIDEO_SYNC_TIMEOUT=1800 \
vllm serve "$H3_MODEL" --omni \
  --host 127.0.0.1 --port 8093 --trust-remote-code \
  --task-type fl2va --num-gpus 8 --usp 8 --ring 1 \
  --ulysses-a2a-permute --text-encoder-tp-size 8 \
  --vae-patch-parallel-size 8 --vae-parallel-mode tile --vae-use-tiling \
  --diffusion-attention-backend TRTLLM_ATTN
```

标准请求使用第 2 节中的提示词与种子、请求 50 个 sigma 点、flow shift 12、音频 flow shift 3，以及 10 秒目标时长。

## 参考文献

- [vLLM-Omni repository](https://github.com/vllm-project/vllm-omni)
- [FastVideo repository](https://github.com/hao-ai-lab/FastVideo)
- [FastH3 technical overview](https://haoailab.com/blogs/fasth3-preview/)
- [FastH3 four-step adapter](https://huggingface.co/FastVideo/FastVideo-FastH3-4-step-Preview-v1-LoRA)
- [FastH3 VSA and Ulysses integration](https://github.com/vllm-project/vllm-omni/pull/6909)
- [MiniMax H3 model](https://huggingface.co/MiniMaxAI/MiniMax-H3)
- [Diffusers MiniMax H3 pipeline](https://huggingface.co/docs/diffusers/v0.40.0/api/pipelines/minimax_h3)
- [MiniMax H3 serving recipe](https://recipes.vllm.ai/MiniMaxAI/MiniMax-H3)
- [Distributed Layerwise Offload](https://vllm.ai/blog/2026-08-17-distributed-layerwise-offload)
- [Feature compatibility tracker](https://github.com/vllm-project/vllm-omni/issues/5700)
- [Chunkwise output pipeline RFC](https://github.com/vllm-project/vllm-omni/issues/6872)
- [VeRL-Omni repository](https://github.com/verl-project/verl-omni)
- [UniRL repository](https://github.com/Tencent-Hunyuan/UniRL)
- [RLinf repository](https://github.com/RLinf/RLinf)
