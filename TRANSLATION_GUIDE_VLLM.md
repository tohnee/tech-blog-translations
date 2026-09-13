# 翻译规范（vLLM 博客中文化）

本文件是 vLLM 官方博客（https://vllm.ai/blog）翻译项目的统一规范，所有翻译批次开始前先读完。通用原则与 [TRANSLATION_GUIDE.md](TRANSLATION_GUIDE.md)（Raschka 项目）一致，本文件补充本项目特有的约定与术语表。

## 项目信息

- 英文存档：`vllm-articles/posts/<slug>.md`（134 篇，2023-06 至 2026-09）
- 输出目录：`vllm-articles-zh/posts/<slug>.md`（与源文件同名镜像）
- 进度索引：`vllm-articles-zh/README.md`（每完成一篇更新）

## 输出文件头格式

```markdown
---
title: "中文标题"
title_en: "Original English Title"
source: <原文件 source URL，保持不变>
crawled: 2026-09-12
translated: <完成日期 YYYY-MM-DD>
---

# 中文标题

> 原文：[Original English Title](source URL) · vLLM 博客

（正文译文……）
```

标题下如有作者名单（多机构合作文章很常见），在引用行下另起一行照译，如：`作者：Woosuk Kwon、Zhuohan Li（UC Berkeley）等（* 共同一作）`。人名保留英文。

## 翻译原则（在通用规范基础上补充）

1. **全文翻译，不得缩写或跳过**：TL;DR、图表说明、引言、结论、附录、致谢全部翻译。文末作者署名/致谢段也要译。
2. **代码块原样保留**：``` 包裹的代码、命令、配置一字不改，代码内英文注释保留。
3. **数学公式一律原样保留**：`$...$` 与 `$$...$$` 中的 LaTeX 一个字符都不改。
4. **图片链接 URL 原样保留**（多为 `https://vllm.ai/blog-assets/...`），图注（图片下一行的说明文字）翻译。部分文章同一图有 light/dark 两张并列，保持原样。
5. **表格**：表头与单元格文字翻译；数字、符号、单位保留。
6. **脚注/参考文献**：`[1]`、`[[1]](#ref-1)` 引用标记位置保持；文末参考文献列表保留条目原文（标题可不译，条目格式不变）。
7. **HTML 保留元素**：源文件中若出现 `<details>`、`<br>` 等 HTML 标签，标签结构保留，标签内文字翻译。
8. **人名**：保留英文（如 Woosuk Kwon、Kwon Woo-suk 不做转写）。中文机构/模型名保留原文。
9. **性能声明以原文为准**：倍数（24x、3.5x）、百分比、延迟数字、硬件型号（A100、H100、MI300X、MI355X、TPU v5e 等）一字不差。
10. **中英混排空格**：中文与英文/数字之间加一个空格。
11. 站内链接 URL 不动，链接文字翻译（如 `[installation guide](...)` → `[安装指南](...)`）。
12. **不要添加原文没有的内容**（译者注如确有必要，用「（译注：……）」且尽量克制）。

## 术语表（全文统一）

### vLLM 核心概念

| English | 中文 |
|---|---|
| vLLM | vLLM（不译） |
| PagedAttention | PagedAttention（不译） |
| KV cache | KV 缓存（KV Cache） |
| continuous batching | 连续批处理（Continuous Batching） |
| chunked prefill | 分块预填充（Chunked Prefill） |
| prefix caching / prefix cache | 前缀缓存 |
| automatic prefix caching (APC) | 自动前缀缓存（APC） |
| block / block table / block size | 块 / 块表 / 块大小 |
| virtual memory / paging | 虚拟内存 / 分页 |
| copy-on-write | 写时复制（Copy-on-Write） |
| KV connector / KV transfer | KV 连接器 / KV 传输 |
| disaggregated / disaggregation | 分离式 / 分离部署 |
| prefill-decode disaggregation (PD disagg) | PD 分离（Prefill-Decode 分离） |
| vLLM v1 engine | vLLM v1 引擎 |
| engine core / engine | 引擎核心 / 引擎 |
| scheduler | 调度器 |
| API server | API 服务器 |
| worker / rank | worker（不译）/ rank（不译） |
| OpenAI-compatible server | OpenAI 兼容服务器 |
| attention backend | 注意力后端 |
| day-0 support | Day-0 支持 |
| memory pool / KV cache pool | 内存池 / KV 缓存池 |
| CPU/GPU offloading | CPU 卸载 / GPU 卸载（offload → 卸载） |
| weight transfer / weight sync | 权重传输 / 权重同步 |

### 推理与解码

| English | 中文 |
|---|---|
| inference | 推理 |
| serving | 服务（推理服务） |
| throughput | 吞吐量 |
| latency | 延迟 |
| TTFT (time to first token) | TTFT（首 token 延迟） |
| TPOT / inter-token latency | TPOT / 逐 token 延迟 |
| prefill | 预填充（Prefill） |
| decode | 解码（Decode） |
| speculative decoding | 投机解码 |
| draft model / draft tokens | 草稿模型 / 草稿 token |
| target model / verify | 目标模型 / 验证 |
| acceptance rate / acceptance length | 接受率 / 接受长度 |
| EAGLE / MTP / Medusa / n-gram | 保留原名 |
| beam search | 束搜索 |
| parallel sampling | 并行采样 |
| greedy decoding | 贪心解码 |
| sampling params | 采样参数 |
| logprobs | logprobs（不译） |
| guided decoding / structured output | 引导解码 / 结构化输出 |
| tool calling / function calling | 工具调用 / 函数调用 |
| multi-LoRA | 多 LoRA |
| batching / batch size | 批处理 / 批大小 |
| request / sequence / token | 请求 / 序列 / token（不译） |

### 并行与硬件

| English | 中文 |
|---|---|
| tensor parallelism (TP) | 张量并行（TP） |
| pipeline parallelism (PP) | 流水线并行（PP） |
| expert parallelism (EP) | 专家并行（EP） |
| data parallelism (DP) | 数据并行（DP） |
| context parallelism (CP) | 上下文并行（CP） |
| sequence parallelism | 序列并行 |
| elastic expert parallelism | 弹性专家并行 |
| MoE (Mixture of Experts) / expert | 混合专家（MoE）/ 专家 |
| collective communication | 集合通信 |
| NCCL / RCCL / MSCCL++ | 保留原名 |
| CUDA graphs | CUDA Graph |
| kernel / fused kernel | 内核 / 融合内核 |
| FlashAttention / FlashInfer / FlashMLA | 保留原名 |
| HBM / GPU memory | HBM / 显存 |
| SM (streaming multiprocessor) | SM |
| quantization | 量化 |
| FP8 / FP4 / INT8 / INT4 / NVFP4 / AWQ / GPTQ / W4A16 | 保留原名 |
| activation | 激活值 |
| calibration | 校准 |
| weight-only quantization | 仅权重量化 |
| GPU utilization (GPU-Util) | GPU 利用率 |
| NUMA | NUMA（不译） |
| ROCm / CUDA / XPU / NPU / TPU | 保留原名 |

### 训练后服务与生态

| English | 中文 |
|---|---|
| RLHF / RL / rollout | RLHF / 强化学习 / rollout（不译） |
| reward model | 奖励模型 |
| verl / vLLM-Omni / vLLM-SR / SigMA | 保留原名 |
| load balancing / router | 负载均衡 / 路由器 |
| endpoint | 端点 |
| health check | 健康检查 |
| checkpoint | 检查点 |
| fine-tuning | 微调 |
| benchmark / benchmark suite | 基准测试 / 基准测试套件 |
| open source | 开源 |
| community meetup | 社区聚会（Meetup 保留亦可，全文统一即可） |
| production | 生产环境 |
| scaling / scale-out | 扩展 / 横向扩展 |
| cost efficiency | 成本效益 |
| state of the art (SOTA) | 最先进水平（SOTA） |
| LLM / VLM / MLLM | LLM / VLM / 多模态大模型（MLLM） |
| multimodal | 多模态 |
| embedding | 嵌入 |
| long context / context length | 长上下文 / 上下文长度 |
| agentic | 智能体（agentic serving → 智能体服务） |
| hallucination | 幻觉 |
| guard / guardrail | 守护模型 / 安全护栏 |

## 模型名处理

模型名一律保留官方写法：LLaMA / Llama 2 / Llama 3.1、Qwen3 / Qwen3.8、DeepSeek-R1 / DeepSeek-V3.2、GLM-5 / GLM-4.5、Kimi K2 / K3、MiniMax-M2 / M3、GPT-OSS、Gemma、Nemotron、Vicuna、ShareGPT 等。个别官方有中文名的（如通义千问 Qwen）在首次出现时可注一次，后文用官方写法。
