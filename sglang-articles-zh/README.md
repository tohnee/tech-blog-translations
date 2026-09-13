# SGLang 技术博客中文翻译

LMSYS 官方博客（lmsys.org/blog）SGLang 及其生态（slime / Miles / SGLang-Diffusion / SGLang-Jax 等）全部技术文章的中文翻译，共 **96 篇**（2024-01 → 2026-09）。

- 原文存档：[`../sglang-articles/`](../sglang-articles/)（英文 markdown）
- 译文目录：本目录，文件名与原文一一对应
- 翻译规范：[`../TRANSLATION_GUIDE_SGLANG.md`](../TRANSLATION_GUIDE_SGLANG.md)
- 进度记录：[`_PROGRESS.md`](_PROGRESS.md)

语料来源说明：LMSYS 博客是 SGLang 官方文档站（docs.sglang.ai）同步博客内容的权威来源；新官方博客 blog.sglang.io 上线前的全部技术博文均发布于 lmsys.org。

| # | 日期 | 中文标题 | 原文标题 | 文件 |
|---|------|----------|----------|------|
| 1 | Jan 17, 2024 | RadixAttention 与 SGLang：快速且富有表达力的 LLM 推理 | Fast and Expressive LLM Inference with RadixAttention and SGLang | [2024-01-17-sglang.md](2024-01-17-sglang.md) |
| 2 | Feb 5, 2024 | 利用压缩有限状态机为本地 LLM 实现快速 JSON 解码 | Fast JSON Decoding for Local LLMs with Compressed Finite State Machine | [2024-02-05-compressed-fsm.md](2024-02-05-compressed-fsm.md) |
| 3 | Jul 25, 2024 | 用 SGLang Runtime 实现更快的开源 Llama3 推理服务（对比 TensorRT-LLM、vLLM） | Achieving Faster Open-Source Llama3 Serving with SGLang Runtime (vs. TensorRT-LLM, vLLM) | [2024-07-25-sglang-llama3.md](2024-07-25-sglang-llama3.md) |
| 4 | September 4, 2024 | SGLang v0.3 发布：DeepSeek MLA 最高提速 7 倍、torch.compile 最高提速 1.5 倍、LLaVA-OneVision 多图/视频支持 | SGLang v0.3 Release: 7x Faster DeepSeek MLA, 1.5x Faster torch.compile, Multi-Image/Video LLaVA-OneVision | [2024-09-04-sglang-v0-3.md](2024-09-04-sglang-v0-3.md) |
| 5 | December 4, 2024 | SGLang v0.4：零开销批调度器、缓存感知负载均衡器与更快的结构化输出 | SGLang v0.4: Zero-Overhead Batch Scheduler, Cache-Aware Load Balancer, Faster Structured Outputs | [2024-12-04-sglang-v0-4.md](2024-12-04-sglang-v0-4.md) |
| 6 | May 5, 2025 | 在 96 块 H100 GPU 上以 PD 分离与大规模专家并行部署 DeepSeek | Deploying DeepSeek with PD Disaggregation and Large-Scale Expert Parallelism on 96 H100 GPUs | [2025-05-05-large-scale-ep.md](2025-05-05-large-scale-ep.md) |
| 7 | June 16, 2025 | 在 GB200 NVL72 上以 PD 分离与大规模专家并行部署 DeepSeek（第一篇）：解码吞吐提升 2.7 倍 | Deploying DeepSeek on GB200 NVL72 with PD and Large Scale EP (Part I): 2.7x Higher Decoding Throughput | [2025-06-16-gb200-part-1.md](2025-06-16-gb200-part-1.md) |
| 8 | July 8, 2025 | OME：以模型驱动架构革新大模型基础设施 | OME: Revolutionizing LLM Infrastructure with Model-Driven Architecture | [2025-07-08-ome.md](2025-07-08-ome.md) |
| 9 | July 9, 2025 | slime：面向 RL 扩展的 SGLang 原生后训练框架 | slime: An SGLang-Native Post-Training Framework for RL Scaling | [2025-07-09-slime.md](2025-07-09-slime.md) |
| 10 | July 14, 2025 | 使用 Intel® Xeon® 6 CPU 在 SGLang 上高性价比部署 DeepSeek R1 | Cost Effective Deployment of DeepSeek R1 with Intel® Xeon® 6 CPU on SGLang | [2025-07-14-intel-xeon-optimization.md](2025-07-14-intel-xeon-optimization.md) |
| 11 | July 16, 2025 | 如何在 SGLang 中支持新的视觉语言模型（VLM）：以 NVILA 为例 | How to support new VLMs into SGLang: A Case Study with NVILA | [2025-07-16-nvila.md](2025-07-16-nvila.md) |
| 12 | July 17, 2025 | 使用多 token 预测（MTP）加速 SGLang | Accelerating SGLang with Multiple Token Prediction | [2025-07-17-mtp.md](2025-07-17-mtp.md) |
| 13 | July 20, 2025 | 在 128 块 H200 GPU 上以 PD 分离与大规模专家并行部署 Kimi K2 | Deploying Kimi K2 with PD Disaggregation and Large-Scale Expert Parallelism on 128 H200 GPUs | [2025-07-20-k2-large-scale-ep.md](2025-07-20-k2-large-scale-ep.md) |
| 14 | July 25, 2025 | SpecForge：加速 SGLang 的投机解码训练 | SpecForge: Accelerating Speculative Decoding Training for SGLang | [2025-07-25-spec-forge.md](2025-07-25-spec-forge.md) |
| 15 | July 31, 2025 | GLM-4.5 携手 SGLang：推理、编程与智能体能力 | GLM-4.5 Meets SGLang: Reasoning, Coding, and Agentic Abilities | [2025-07-31-glm4-5.md](2025-07-31-glm4-5.md) |
| 16 | August 27, 2025 | SGLang 支持 gpt-oss：从 Day-0 支持到性能全面增强 | SGLang for gpt-oss: From Day 0 Support to Enhanced Performance | [2025-08-27-gpt-oss.md](2025-08-27-gpt-oss.md) |
| 17 | Aug 28, 2025 | 微调并部署 gpt-oss MXFP4：ModelOpt + SGLang | Fine-tune and deploy gpt-oss MXFP4: ModelOpt + SGLang | [2025-08-28-gpt-oss-qat.md](2025-08-28-gpt-oss-qat.md) |
| 18 | September 01, 2025 | LongCat-Flash：使用 SGLang 部署美团的 Agentic 模型 | LongCat-Flash: Deploying Meituan's Agentic Model with SGLang | [2025-09-01-sglang-longcat-flash.md](2025-09-01-sglang-longcat-flash.md) |
| 19 | September 10, 2025 | SGLang HiCache：搭配你喜爱的存储后端，实现高速分层 KV 缓存 | SGLang HiCache: Fast Hierarchical KV Caching with Your Favorite Storage Backends | [2025-09-10-sglang-hicache.md](2025-09-10-sglang-hicache.md) |
| 20 | September 21, 2025 | 在 AMD GPU 上优化 FP4 混合精度推理 | Optimizing FP4 Mixed-Precision Inference on AMD GPUs | [2025-09-21-petit-amdgpu.md](2025-09-21-petit-amdgpu.md) |
| 21 | September 22, 2025 (Updated on September 24) | 迈向 SGLang 确定性推理与可复现 RL 训练 | Towards Deterministic Inference in SGLang and Reproducible RL Training | [2025-09-22-sglang-deterministic.md](2025-09-22-sglang-deterministic.md) |
| 22 | September 25, 2025 | 在 GB200 NVL72 上以 PD 分离与大规模专家并行部署 DeepSeek（第二篇）：预填充吞吐 3.8 倍、解码吞吐 4.8 倍 | Deploying DeepSeek on GB200 NVL72 with PD and Large Scale EP (Part II): 3.8x Prefill, 4.8x Decode Throughput | [2025-09-25-gb200-part-2.md](2025-09-25-gb200-part-2.md) |
| 23 | September 26, 2025 | 携手 SGLang：在 H20-96G 上服务 DeepSeek-R1 的最佳实践 | Together with SGLang: Best Practices for Serving DeepSeek-R1 on H20-96G | [2025-09-26-sglang-ant-group.md](2025-09-26-sglang-ant-group.md) |
| 24 | September 28, 2025 | PD 复用：借助 GreenContext 实现高 goodput 的大模型推理服务 | PD-Multiplexing: Unlocking High-Goodput LLM Serving with GreenContext | [2025-09-28-pdmux.md](2025-09-28-pdmux.md) |
| 25 | September 29, 2025 | SGLang Day-0 支持搭载稀疏注意力的 DeepSeek-V3.2 | SGLang Day 0 Support for DeepSeek-V3.2 with Sparse Attention | [2025-09-29-deepseek-V32.md](2025-09-29-deepseek-V32.md) |
| 26 | October 13, 2025 | NVIDIA DGX Spark 深度评测：本地 AI 推理的新标准 | NVIDIA DGX Spark In-Depth Review: A New Standard for Local AI Inference | [2025-10-13-nvidia-dgx-spark.md](2025-10-13-nvidia-dgx-spark.md) |
| 27 | Oct 14, 2025 | SGLang 与 NVIDIA 携手加速 SemiAnalysis InferenceMAX 与 GB200 | SGLang and NVIDIA Accelerating SemiAnalysis InferenceMAX and GB200 Together | [2025-10-14-sa-inference-max.md](2025-10-14-sa-inference-max.md) |
| 28 | October 22, 2025 | 使用 KTransformers CPU 算子加速 SGLang 混合推理 | Accelerating Hybrid Inference in SGLang with KTransformers CPU Kernels | [2025-10-22-KTransformers.md](2025-10-22-KTransformers.md) |
| 29 | October 29, 2025 | SGLang-Jax：原生 TPU 推理的开源解决方案 | SGLang-Jax: An Open-Source Solution for Native TPU Inference | [2025-10-29-sglang-jax.md](2025-10-29-sglang-jax.md) |
| 30 | November 3, 2025 | 在 NVIDIA DGX Spark 上优化 GPT-OSS：充分释放你的 Spark 性能 | Optimizing GPT-OSS on NVIDIA DGX Spark: Getting the Most Out of Your Spark | [2025-11-03-gpt-oss-on-nvidia-dgx-spark.md](2025-11-03-gpt-oss-on-nvidia-dgx-spark.md) |
| 31 | November 4, 2025 | 「没有免费的午餐」：用 MiniMax M2 解构高效注意力 | "No Free Lunch": Deconstruct Efficient Attention with MiniMax M2 | [2025-11-04-miminmax-m2.md](2025-11-04-miminmax-m2.md) |
| 32 | November 7, 2025 | SGLang Diffusion：加速视频与图像生成 | SGLang Diffusion: Accelerating Video and Image Generation | [2025-11-07-sglang-diffusion.md](2025-11-07-sglang-diffusion.md) |
| 33 | November 14, 2025 | 🚀 AutoRound 携手 SGLang：用 AutoRound 实现量化模型推理 | 🚀 AutoRound Meets SGLang: Enabling Quantized Model Inference with AutoRound | [2025-11-13-AutoRound.md](2025-11-13-AutoRound.md) |
| 34 | November 19, 2025 | Miles 正式发布：点燃大规模 MoE 训练的强化学习框架 | Introducing Miles — RL Framework To Fire Up Large-Scale MoE Training | [2025-11-19-miles.md](2025-11-19-miles.md) |
| 35 | November 25, 2025 | 统一 FP8：超越混合精度，让 MoE 强化学习更稳定、更快速 | Unified FP8: Moving Beyond Mixed Precision for Stable and Accelerated MoE RL | [2025-11-25-fp8-rl.md](2025-11-25-fp8-rl.md) |
| 36 | December 1, 2025 | 从研究到生产：在 Vertex 上用 EAGLE-3 加速开源大语言模型 | From research to production: Accelerate OSS LLM with EAGLE-3 on Vertex | [2025-12-01-eagle3-vertex.md](2025-12-01-eagle3-vertex.md) |
| 37 | Dec 02, 2025 | 提升 SGLang 推理性能：原生集成 NVIDIA Model Optimizer，实现无缝量化与部署 | Boost SGLang Inference: Native NVIDIA Model Optimizer Integration for Seamless Quantization and Deployment | [2025-12-02-modelopt-quantization.md](2025-12-02-modelopt-quantization.md) |
| 38 | December 10, 2025 | 让 Tensor 飞起来——用 R-Fork 加速大模型权重加载 | Let Tensors Fly — Accelerating Large Model Weight Loading with R-Fork | [2025-12-10-rfork.md](2025-12-10-rfork.md) |
| 39 | December 15, 2025 | SGLang 为高效开放的 Nemotron 3 Nano 混合 MoE 模型提供 Day-0 支持 | SGLang Adds Day-0 Support for the Highly Efficient, Open Nemotron 3 Nano Hybrid MoE Model | [2025-12-15-run-nvidia-nemotron-3-nano.md](2025-12-15-run-nvidia-nemotron-3-nano.md) |
| 40 | December 16, 2025 | SGLang Day-0 支持 MiMo-V2-Flash 模型 | SGLang Day-0 Support for MiMo-V2-Flash Model | [2025-12-16-mimo-v2-flash.md](2025-12-16-mimo-v2-flash.md) |
| 41 | December 17, 2025 | Mini-SGLang：小而精的高效推理引擎 | Mini-SGLang: Efficient Inference Engine in a Nutshell | [2025-12-17-minisgl.md](2025-12-17-minisgl.md) |
| 42 | December 19, 2025 | 为扩散 LLM 强力赋能：LLaDA 2.0 的 Day-0 支持 | Power Up Diffusion LLMs: Day‑0 Support for LLaDA 2.0 | [2025-12-19-diffusion-llm.md](2025-12-19-diffusion-llm.md) |
| 43 | December 23, 2025 | SpecBundle 与 SpecForge v0.2：生产级投机解码模型与框架 | SpecBundle & SpecForge v0.2: Production-Ready Speculative Decoding Models and Framework | [2025-12-23-spec-bundle-phase-1.md](2025-12-23-spec-bundle-phase-1.md) |
| 44 | January 12, 2026 | EPD 分离：SGLang 中为视觉语言模型实现编码器弹性伸缩 | EPD Disaggregation: Elastic Encoder Scaling for Vision-Language Models in SGLang | [2026-01-12-epd.md](2026-01-12-epd.md) |
| 45 | January 15, 2026 | SGLang 的流水线并行：扩展至百万 token 上下文及更长 | Pipeline Parallelism in SGLang: Scaling to Million-Token Contexts and Beyond | [2026-01-15-chunked-pipeline.md](2026-01-15-chunked-pipeline.md) |
| 46 | January 16, 2026 | SGLang-Diffusion：两个月进展回顾 | SGLang-Diffusion: Two Months In | [2026-01-16-sglang-diffusion.md](2026-01-16-sglang-diffusion.md) |
| 47 | January 21, 2026 | 面向生产优化 GLM4-MoE：借助 SGLang 将 TTFT 缩短 65% | Optimizing GLM4-MoE for Production: 65% Faster TTFT with SGLang | [2026-01-21-novita-glm4.md](2026-01-21-novita-glm4.md) |
| 48 | January 26, 2026 | 把 1TB 模型的 rollout 塞进单张 H200：INT4 QAT RL 端到端实践 | Squeezing 1TB Model Rollout into a Single H200: INT4 QAT RL End-to-End Practice | [2026-01-26-int4-qat.md](2026-01-26-int4-qat.md) |
| 49 | February 11, 2026 | 释放算力：Qwen3 与 Qwen3-VL 在 AMD MI300X 系列上的极致延迟优化 | Unleashing Computational Power: Ultimate Latency Optimization of Qwen3 and Qwen3-VL on AMD MI300X Series | [2026-02-11-Qwen-latency.md](2026-02-11-Qwen-latency.md) |
| 50 | February 16, 2026 | SGLang-Diffusion：面向生产级视频生成的高级优化 | SGLang-Diffusion: Advanced Optimizations for Production-Ready Video Generation | [2026-02-16-sglang-diffusion-advanced-optimizations.md](2026-02-16-sglang-diffusion-advanced-optimizations.md) |
| 51 | February 19, 2026 | 在 GB300 NVL72 上部署 DeepSeek：长上下文推理的重大收益 | Deploying DeepSeek on GB300 NVL72: Big Wins in Long-Context Inference | [2026-02-19-gb300-longctx.md](2026-02-19-gb300-longctx.md) |
| 52 | February 20, 2026 | SGLang 在 NVIDIA GB300 NVL72 上解锁 25 倍推理性能 | Unlocking 25x Inference Performance with SGLang on NVIDIA GB300 NVL72 | [2026-02-20-gb300-inferencex.md](2026-02-20-gb300-inferencex.md) |
| 53 | March 11, 2026 | SGLang 为 NVIDIA Nemotron 3 Super 提供 Day-0 支持，助力构建高效多智能体系统 | SGLang Adds Day-0 Support for NVIDIA Nemotron 3 Super for building High-Efficiency Multi-Agent Systems | [2026-03-11-run-nvidia-nemotron-3-super.md](2026-03-11-run-nvidia-nemotron-3-super.md) |
| 54 | March 17, 2026 | Miles 的 ROCm 支持：在 AMD Instinct™ GPU 上进行大规模 RL 后训练 | ROCm Support for Miles: Large-Scale RL Post-Training on AMD Instinct™ GPUs | [2026-03-17-rocm-miles-rl-amd.md](2026-03-17-rocm-miles-rl-amd.md) |
| 55 | March 25, 2026 | SGLang 中的弹性专家并行：为 DeepSeek MoE 部署实现部分故障容忍 | Elastic EP in SGLang: Achieving Partial Failure Tolerance for DeepSeek MoE Deployments | [2026-03-25-eep-partial-failure-tolerance.md](2026-03-25-eep-partial-failure-tolerance.md) |
| 56 | March 31, 2026 | SGLang 在 NVIDIA GTC 2026 上的精彩回顾 | Highlights of SGLang at NVIDIA GTC 2026 | [2026-03-25-gtc2026.md](2026-03-25-gtc2026.md) |
| 57 | April 10, 2026 | HiSparse：用分层内存为稀疏注意力全面提速 | HiSparse: Turbocharging Sparse Attention with Hierarchical Memory | [2026-04-10-sglang-hisparse.md](2026-04-10-sglang-hisparse.md) |
| 58 | April 25, 2026 | DeepSeek-V4 Day-0 支持：借助 SGLang 与 Miles，从高速推理到可验证 RL | DeepSeek-V4 on Day 0: From Fast Inference to Verified RL with SGLang and Miles | [2026-04-25-deepseek-v4.md](2026-04-25-deepseek-v4.md) |
| 59 | April 29, 2026 | 数秒内更新 1T 参数——大规模分布式 RL 中的 P2P 权重传输 | Updating 1T parameters in seconds — P2P weight transfer in Large Scale Distributed RL | [2026-04-29-p2p-update.md](2026-04-29-p2p-update.md) |
| 60 | June 5, 2026 | 不让一个 token 掉队：解密 Miles 中的 Token-In-Token-Out（TITO） | No Token Left Behind: Demystifying Token-In-Token-Out in Miles | [2026-05-13-no-token-left-behind.md](2026-05-13-no-token-left-behind.md) |
| 61 | May 28, 2026 | 在 TCO 上取胜：AMD Instinct™ MI355X 如何通过 SGLang 与 MoRI 实现具备成本竞争力的分布式推理 | Win on TCO: How AMD Instinct™ MI355X Achieves Cost-Competitive Distributed Inference Through SGLang with MoRI | [2026-05-28-mori.md](2026-05-28-mori.md) |
| 62 | May 29, 2026 | CPU+GPU 异构 EPD 分离提升 VLM 推理服务性能 | Heterogeneous CPU + GPU EPD Disaggregation to Boost VLM Serving | [2026-06-01-hetero-epd.md](2026-06-01-hetero-epd.md) |
| 63 | June 4, 2026 | SGLang-Omni 上的 Higgs Audio v3 TTS：为语音智能体提供实时、可控的语音生成 | Higgs Audio v3 TTS on SGLang-Omni: Real-Time, Controllable Speech for Voice Agents | [2026-06-04-higgs-audio-v3-tts.md](2026-06-04-higgs-audio-v3-tts.md) |
| 64 | June 4, 2026 | SGLang 与 Miles 为 NVIDIA Nemotron 3 Ultra 提供 Day-0 支持，面向长时运行自主智能体 | SGLang and Miles Add Day-0 Support for NVIDIA Nemotron 3 Ultra for Long-Running Autonomous Agents | [2026-06-04-nvidia-run-nemotron-3-ultra.md](2026-06-04-nvidia-run-nemotron-3-ultra.md) |
| 65 | June 15, 2026 | 下一代投机解码：DFlash 与 Spec V2 | The next generation of speculative decoding: DFlash and Spec V2 | [2026-06-15-next-generation-speculative-decoding-dflash-v2.md](2026-06-15-next-generation-speculative-decoding-dflash-v2.md) |
| 66 | June 17, 2026 | 用 SGLang-JAX 在 TPU 上优化 Ling-2.6-1T：以单个 Pallas kernel 将 MoE 数据搬运隐藏在计算之后 | Optimizing Ling-2.6-1T on TPU with SGLang-JAX: Hiding MoE Data Movement Behind Compute with One Pallas Kernel | [2026-06-17-ling-2-6-tpu.md](2026-06-17-ling-2-6-tpu.md) |
| 67 | June 17, 2026 | SGLang-Omni 上的 MOSS-TTS Local Transformer v1.5：原生流式 48 kHz 语音推理服务 | MOSS-TTS Local Transformer v1.5 on SGLang-Omni: Serving Native-Streaming 48 kHz Speech | [2026-06-17-moss-tts-local-v15.md](2026-06-17-moss-tts-local-v15.md) |
| 68 | June 26, 2026 | 在 SGLang 中使用 Waterfill 与 LPLB 改进 DeepEP MoE 负载均衡 | Improving DeepEP MoE Load Balance in SGLang with Waterfill and LPLB | [2026-06-26-waterfill-lplb.md](2026-06-26-waterfill-lplb.md) |
| 69 | July 8, 2026 | Netpreme X-Mem™ MPU 加速 SGLang HiCache | Accelerating SGLang HiCache with Netpreme X-Mem™ MPU | [2026-06-27-netpreme-xmem.md](2026-06-27-netpreme-xmem.md) |
| 70 | July 2, 2026 | Agent 辅助的 SGLang 开发：一次初步探索 | Agent-Assisted SGLang Development: An Initial Exploration | [2026-07-02-agent-assisted-sglang-development.md](2026-07-02-agent-assisted-sglang-development.md) |
| 71 | July 6, 2026 | SGLang 中的 DSpark：置信度驱动的可变长度验证投机解码 | DSpark in SGLang: Speculative Decoding with Confidence-Driven, Variable-Length Verification | [2026-07-06-dspark-sglang.md](2026-07-06-dspark-sglang.md) |
| 72 | July 10, 2026 | 借助 Miles 在 AMD Instinct MI355X GPU 上实现 DeepSeek-V4 Flash RL 训练 | Bringing DeepSeek-V4 Flash RL Training to AMD Instinct MI355X GPUs with Miles | [2026-07-10-rocm-miles-dsv4.md](2026-07-10-rocm-miles-dsv4.md) |
| 73 | July 14, 2026 | SGLang 服务 GLM5.2 NVFP4 agentic 负载：两周内达到 500 TPS | Serving GLM5.2 NVFP4 Agentic Workload with SGLang: Reaching 500 TPS in 2 Weeks | [2026-07-13-glm52-optimization.md](2026-07-13-glm52-optimization.md) |
| 74 | July 15, 2026 | SGLang 与 Miles 为前沿多模态模型 Inkling 提供 Day-0 支持 | SGLang and Miles Add Day-0 Support for Inkling, a Frontier Multimodal Model | [2026-07-15-inkling-day0-support.md](2026-07-15-inkling-day0-support.md) |
| 75 | July 18, 2026 | Miles 新增 OPD（在线策略蒸馏）支持 | OPD Support in Miles | [2026-07-18-opd-support-in-miles.md](2026-07-18-opd-support-in-miles.md) |
| 76 | July 27, 2026 | SGLang 与 Miles 为 Kimi K3 提供 Day-0 支持 | SGLang and Miles Add Day-0 Support for Kimi K3 | [2026-07-27-kimi-k3-day0-support.md](2026-07-27-kimi-k3-day0-support.md) |
| 77 | July 29, 2026 | 迈向 Blackwell 原生的 8-bit 与 4-bit RL：Miles 中的端到端 MXFP8 与 NVFP4 强化学习 | Towards Blackwell-Native 8-bit and 4-bit RL: End-to-End MXFP8 and NVFP4 RL in Miles | [2026-07-29-mxfp8-nvfp4-rl.md](2026-07-29-mxfp8-nvfp4-rl.md) |
| 78 | July 30, 2026 | RadixArk 携手 Google，将完整的 SGLang 特性带到 TPU | RadixArk Joins Forces with Google to Bring Full SGLang Features to TPUs | [2026-07-30-sglang-google-tpu.md](2026-07-30-sglang-google-tpu.md) |
| 79 | July 28, 2026 | SGLang 迈向更整洁的量化栈 | Toward a Cleaner Quantization Stack in SGLang | [2026-07-31-cleaner-quantization-stack.md](2026-07-31-cleaner-quantization-stack.md) |
| 80 | August 4, 2026 | SpecForge v0.3.0：统一分离式与共置投机解码技术栈，并发布全新开放 SpecBundle 草稿模型 | SpecForge v0.3.0: a Unified Disaggregated and Colocated Speculative Decoding Stack, and New Open SpecBundle Draft Models | [2026-08-04-specforge-v0-3.md](2026-08-04-specforge-v0-3.md) |
| 81 | August 05, 2026 | SGL-Diffusion 中 AR+DiT 的全栈性能优化 | Full-Stack Performance Optimization of AR+DiT in SGL-Diffusion | [2026-08-05-glmImage-optimization.md](2026-08-05-glmImage-optimization.md) |
| 82 | August 7, 2026 | HPC-Ops × SGLang：来自腾讯混元的高性能注意力、Router GEMM 与 MoE 算子 | HPC-Ops × SGLang: High-Performance Attention, Router GEMM, and MoE Kernels from Tencent Hunyuan | [2026-08-07-hpc-ops-sglang.md](2026-08-07-hpc-ops-sglang.md) |
| 83 | August 10, 2026 | SGLang 为 Muse Glimmer 提供 Day-0 支持：一款面向本地智能体工作流的多模态模型 | SGLang Adds Day-0 Support for Muse Glimmer, a Multimodal Model Built for Local Agentic Workflows | [2026-08-10-meta-muse-glimmer.md](2026-08-10-meta-muse-glimmer.md) |
| 84 | August 11, 2026 | SGLang 为 NVIDIA Nemotron 3.5 Lightning 提供 Day-0 支持 | SGLang Adds Day-0 Support for NVIDIA Nemotron 3.5 Lightning | [2026-08-11-nemotron-3-5-lightning.md](2026-08-11-nemotron-3-5-lightning.md) |
| 85 | August 11, 2026 | 统一基数树缓存：用一棵树支撑混合模型的前缀缓存 | Unified Radix Cache: One Tree for Hybrid Model Prefix Caching | [2026-08-11-unified-radix-cache.md](2026-08-11-unified-radix-cache.md) |
| 86 | Aug 12, 2026 | SGLang 与 Miles 为 Qwen3.8 提供 Day-0 支持 | SGLang and Miles Add Day-0 Support for Qwen3.8 | [2026-08-12-qwen3-8-day0-support.md](2026-08-12-qwen3-8-day0-support.md) |
| 87 | August 17, 2026 | SGLang 中的高级 CUDA 图技术 | Advanced CUDA Graph Techniques in SGLang | [2026-08-17-advanced-cuda-graph.md](2026-08-17-advanced-cuda-graph.md) |
| 88 | August 18, 2026 | Miles v0.1：生产级后训练 | Miles v0.1: Production-level Post-training | [2026-08-18-miles-v0-1.md](2026-08-18-miles-v0-1.md) |
| 89 | August 19, 2026 | 将 DeepSeek-V4-Pro 推理服务推向极限 | Pushing the Limits of Serving DeepSeek-V4-Pro | [2026-08-19-deepseek-v4-pro-engine-optimization-h20.md](2026-08-19-deepseek-v4-pro-engine-optimization-h20.md) |
| 90 | August 20, 2026 | Mooncake 赋能 Miles：从碎片化 rollout 数据到高效批量 I/O | Mooncake for Miles: From Fragmented Rollout Data to Efficient Bulk I/O | [2026-08-20-miles-mooncake-rollout-data-transfer.md](2026-08-20-miles-mooncake-rollout-data-transfer.md) |
| 91 | August 21, 2026 | 追逐批量大小 1 的下限：Ling-3.0-flash 在 Blackwell 上的投机解码 | Chasing the Batch-1 Floor: Ling-3.0-flash Speculative Decode on Blackwell | [2026-08-21-ling3-flash-spec-decode-blackwell.md](2026-08-21-ling3-flash-spec-decode-blackwell.md) |
| 92 | August 21, 2026 | 快速引擎恢复：基于权重缓存守护进程的 SGLang 亚秒级引擎重启 | Fast Engine Recovery: Sub-Second Engine Restart for SGLang via Weight Cache Daemon | [2026-08-21-sglang-fast-recovery.md](2026-08-21-sglang-fast-recovery.md) |
| 93 | August 26, 2026 | Qwen3.8-Flash-Next：SGLang 的 Day-0 支持 | Qwen3.8-Flash-Next: Day-0 Support in SGLang | [2026-08-26-qwen-flash-next.md](2026-08-26-qwen-flash-next.md) |
| 94 | August 27, 2026 | 8×H200 上的 MiniMax-H3：无损加速 1.95×，SSIM 0.76–0.91 下最高 6.24× | MiniMax-H3 on 8×H200: 1.95× Lossless, Up to 6.24× at 0.76–0.91 SSIM | [2026-08-27-minimax-h3-h200.md](2026-08-27-minimax-h3-h200.md) |
| 95 | August 28, 2026 | Infer-forge:围绕 SGLang 的执行框架、循环与图工程 | Infer-forge: Harness, Loop, and Graph Engineering Around SGLang | [2026-08-28-infer-forge-loop-engineering.md](2026-08-28-infer-forge-loop-engineering.md) |
| 96 | September 10, 2026 | SGLang 与 Miles 为 DeepSeek-V4.1 提供 Day-0 支持 | SGLang and Miles Add Day-0 Support for DeepSeek-V4.1 | [2026-09-10-deepseek-v41.md](2026-09-10-deepseek-v41.md) |
