# 翻译规范（SGLang 技术博客中文化）

本文件是 SGLang 技术博客翻译项目的统一规范，所有翻译批次开始前先读完。通用原则与 [TRANSLATION_GUIDE.md](TRANSLATION_GUIDE.md)（Raschka 项目）一致，本文件补充本项目特有的约定与术语表。

## 项目信息

- 语料来源：LMSYS 官方博客（`lmsys.org/blog`），markdown 源文件托管于 GitHub `lm-sys/lm-sys.github.io/blog/`——这也是 SGLang 官方文档站（docs.sglang.ai）同步博客的权威来源（见 `sgl-docs/scripts/update_lmsys_sglang_blogs.py`）。
- 范围：2024-01 至 2026-09 全部 SGLang 及其生态（slime、Miles、SGLang-Diffusion、SGLang-Jax 等）相关文章，共 **96 篇**。不含 LMSYS 非技术内容（Chatbot Arena 新闻、排行榜等）。
- 英文存档：`sglang-articles/<slug>.md`（96 篇）
- 输出目录：`sglang-articles-zh/<slug>.md`（与源文件同名镜像）
- 进度索引：`sglang-articles-zh/README.md` + `_PROGRESS.md`（每完成一篇更新）

## 输出文件头格式

```markdown
---
title: "中文标题"
title_en: "Original English Title"
author: <原文件 author 字段，保持不变>
date: <原文件 date 字段，保持不变>
source: https://lmsys.org/blog/<slug 去掉 .md>/
translated: <完成日期 YYYY-MM-DD>
---

# 中文标题

> 原文：[Original English Title](https://lmsys.org/blog/<slug>/) · LMSYS Blog · <作者>

（正文译文……）
```

- 原 frontmatter 中 `previewImg` 等字段保留（值不动）。`title` 换中文并新增 `title_en`、`source`、`translated`。
- 正文首行 `# 中文标题`，下一行引用块给出原文链接与作者。

## 翻译原则（在通用规范基础上补充）

1. **全文翻译，不得缩写或跳过**：包括 TL;DR、开篇引言、所有章节、Conclusion、参考文献引言行。文末 "Cite this article" / BibTeX 代码块原样保留。
2. **代码块、shell 命令、配置片段原样保留**（含代码内英文注释）。
3. **数字、基准数据、表格数据一字不差**：吞吐量、延迟、倍数（如 1.95×）、GPU 型号与数量。表格表头与文字单元格翻译，数字与符号单元格保留。
4. **图片 URL 原样保留**（`/images/blog/...` 为 LMSYS 站内路径，保持原样即可），caption/图注翻译。无法查看的图片内容按上下文翻译其说明文字。
5. **链接 URL 原样保留**，链接文字翻译。GitHub PR/Issue 链接文字可保留原编号描述。
6. **人名**：正文人名保留英文（如 Banghua Zhu、Lianmin Zheng），不音译。
7. **模型/系统/框架/公司名不翻译**：SGLang、vLLM、TensorRT-LLM、DeepSeek、Qwen、GLM、Kimi、Llama、FlashInfer、FlashAttention、DeepGEMM、DeepEP、slime、Miles、SpecForge、KTransformers、Mooncake、NVIDIA、AMD、Intel、Google TPU 等。
8. **硬件与 GPU 型号不翻译**：H100、H200、H20、GB200 NVL72、GB300、MI300X、MI355X、DGX Spark、B200、TPU 等。
9. **首次出现的重要术语**采用「中文（English/缩写）」标注，之后直接用中文或缩写。
10. **命令行 flag / 环境变量 / 配置项**（如 `--enable-torch-compile`、`SGLANG_ENABLE_JIT_DEEPGEMM=1`）原样保留。
11. 脚注 `[^1]` 标记保持，定义行翻译。

## 术语表（全文统一）

### 推理服务核心

| English | 中文 |
|---|---|
| inference | 推理 |
| serving | 推理服务（动词：服务/部署，视语境） |
| throughput | 吞吐量 |
| latency | 延迟 |
| goodput | goodput（不译） |
| TTFT (time to first token) | 首 token 延迟（TTFT） |
| TPOT / ITL (inter-token latency) | 每 token 生成时间（TPOT/ITL） |
| prefill | 预填充（prefill） |
| decode / decoding | 解码 |
| prefill-decode disaggregation / PD disaggregation | PD 分离（预填充-解码分离） |
| PD-Multiplexing | PD 复用 |
| batch / batching | 批 / 批处理 |
| continuous batching | 连续批处理 |
| chunked prefill | 分块预填充 |
| scheduler | 调度器 |
| batch scheduler | 批调度器 |
| overlap scheduling | 重叠调度 |
| request | 请求 |
| workload | 负载/工作负载 |
| concurrency | 并发 |
| QPS / RPS | QPS / RPS（不译） |

### 并行与集群

| English | 中文 |
|---|---|
| tensor parallelism (TP) | 张量并行（TP） |
| pipeline parallelism (PP) | 流水线并行（PP） |
| data parallelism (DP) | 数据并行（DP） |
| expert parallelism (EP) | 专家并行（EP） |
| large-scale expert parallelism | 大规模专家并行 |
| sequence parallelism | 序列并行 |
| context parallelism | 上下文并行 |
| Elastic EP | 弹性专家并行（Elastic EP） |
| attention / DP attention | 注意力 / DP 注意力 |
| disaggregation | 分离部署 |
| load balancer / load balancing | 负载均衡器 / 负载均衡 |
| cache-aware load balancing | 缓存感知负载均衡 |
| fault tolerance | 容错 |
| failure tolerance | 故障容忍 |
| failover | 故障切换 |
| NIC / NVLink / NVSwitch / InfiniBand / RDMA | 不译 |
| node / GPU / xPU | 节点 / GPU / xPU |

### 缓存与内存

| English | 中文 |
|---|---|
| KV cache | KV 缓存 |
| radix cache / RadixAttention | 基数树缓存 / RadixAttention（不译） |
| prefix caching | 前缀缓存 |
| hierarchical KV cache (HiCache) | 分层 KV 缓存（HiCache） |
| hit rate | 命中率 |
| eviction | 逐出 |
| memory pool | 内存池 |
| paged attention | 分页注意力（PagedAttention） |
| VRAM / HBM | VRAM / HBM（不译） |
| offloading | 卸载（到主机内存/SSD） |

### 加速技术

| English | 中文 |
|---|---|
| speculative decoding | 投机解码 |
| draft model / target model | 草稿模型 / 目标模型 |
| Multi-Token Prediction (MTP) | 多 token 预测（MTP） |
| EAGLE / DFlash / DSpark | 不译 |
| CUDA graph | CUDA 图（CUDA Graph） |
| kernel fusion | 算子融合 |
| kernel | 算子/内核（kernel，视语境，CUDA kernel → CUDA 内核） |
| attention backend | 注意力后端 |
| torch.compile | 不译 |
| JIT compilation | JIT 编译 |
| overlap event / overlap scheduler | 重叠调度 |
| weight loading | 权重加载 |
| engine recovery / restart | 引擎恢复 / 重启 |
| deterministic inference | 确定性推理 |
| reproducible | 可复现 |
| structured output | 结构化输出 |
| finite state machine (FSM) | 有限状态机（FSM） |
| JSON mode | JSON 模式 |
| constrained decoding | 受限解码 |

### 量化与数值格式

| English | 中文 |
|---|---|
| quantization | 量化 |
| FP8 / INT4 / INT8 / FP4 / MXFP8 / NVFP4 / FP4 | 不译 |
| mixed precision | 混合精度 |
| weight-only quantization | 仅权重量化 |
| QAT (quantization-aware training) | 量化感知训练（QAT） |
| calibration | 校准 |
| accuracy loss | 精度损失 |
| lossless | 无损 |
| SSIM / KL divergence | SSIM / KL 散度 |

### RL 与后训练（Miles/slime 语境）

| English | 中文 |
|---|---|
| post-training | 后训练 |
| reinforcement learning (RL) | 强化学习（RL） |
| RLHF / RLVR | 不译 |
| rollout | rollout（不译；首次可注「采样生成」） |
| rollout generation | rollout 生成 |
| reward | 奖励 |
| policy model / reference model | 策略模型 / 参考模型 |
| training / inference engine | 训练引擎 / 推理引擎 |
| colocated / disaggregated | 共置（colocated）/ 分离式 |
| asynchronous RL | 异步强化学习 |
| weight sync / weight transfer | 权重同步 / 权重传输 |
| KL divergence / zero-KL | KL 散度 / zero-KL（不译） |
| agentic RL | 智能体强化学习（agentic RL） |
| multi-turn / tool call | 多轮 / 工具调用 |
| loss mask | 损失掩码 |
| logprob | logprob（不译） |
| harness | 执行框架（harness） |
| verifier | 验证器 |
| GRPO / PPO / FSDP2 / Megatron-LM | 不译 |

### 多模态与扩散

| English | 中文 |
|---|---|
| VLM (vision-language model) | 视觉语言模型（VLM） |
| multimodal | 多模态 |
| image / video generation | 图像 / 视频生成 |
| diffusion model / diffusion LLM | 扩散模型 / 扩散 LLM |
| DiT (Diffusion Transformer) | DiT（不译） |
| AR (autoregressive) | 自回归（AR） |
| encoder-decoder | 编码器-解码器 |
| embedding / Embedding model | 嵌入 / 嵌入模型 |
| TTS / ASR | TTS / ASR（不译） |
| streaming | 流式 |

### 模型架构

| English | 中文 |
|---|---|
| MoE (mixture-of-experts) | 专家混合（MoE） |
| dense model | 稠密模型 |
| MLA (multi-head latent attention) | MLA（不译） |
| GQA / MHA / sliding window attention | GQA / MHA / 滑窗注意力 |
| sparse attention | 稀疏注意力 |
| long context | 长上下文 |
| context length | 上下文长度 |
| vocabulary / vocab | 词表 |
| Day-0 support | Day-0 支持（首发日支持） |
| benchmark | 基准测试 |
| baseline | 基线 |
| ablation | 消融（实验） |

其余术语以 [TRANSLATION_GUIDE.md](TRANSLATION_GUIDE.md) 总表为准；两表冲突时以本文件为准。
