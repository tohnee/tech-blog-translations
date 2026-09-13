---
title: "发布 vime：一个简单、稳定、高效的 LLM 强化学习框架"
title_en: "Announcing vime: A Simple, Stable, and Efficient RL Framework for LLMs"
source: https://vllm.ai/blog/2026-06-09-announcing-vime
crawled: 2026-09-12
translated: 2026-09-13
---

# 发布 vime：一个简单、稳定、高效的 LLM 强化学习框架

> 原文：[Announcing vime: A Simple, Stable, and Efficient RL Framework for LLMs](https://vllm.ai/blog/2026-06-09-announcing-vime) · vLLM 博客

作者：vime 贡献者与 vLLM 团队

[#强化学习](https://vllm.ai/blog/tags/reinforcement-learning)[#生态系统](https://vllm.ai/blog/tags/ecosystem)[#后训练](https://vllm.ai/blog/tags/post-training)

我们很高兴推出 [**vime**](https://github.com/vllm-project/vime)，一个 vLLM 生态内的 LLM 后训练框架。vime 构建在 slime 的训练栈与数据生成设计之上，把 Megatron 与 vLLM 连接成一条完整的强化学习流水线，让分布式训练与推理能够在同一个统一架构下可靠运行。

slime 已经证明自己是 RL 后训练的出色工程范式：开放、轻量、高效。vime 把 vLLM 生态带给 slime，将 slime 的训练栈与 vLLM 的推理优势配成一条简单、稳定、高效的主流水线——提供稳定的训练-推理对齐、灵活的部署模式与全栈 GPU 支持。

## 我们的愿景

兼具实战检验的可信度与开源基因的 RL 框架一直很稀缺。在 GLM 等模型上得到验证的 [slime](https://github.com/THUDM/slime) 是其中的代表：开放、轻量、简洁、高效。但它并没有原生集成 vLLM 后端。与此同时，vLLM 是社区中最活跃的推理引擎，将前沿技术与多平台生态和快速迭代结合在一起。

vime 的使命是把 slime 的训练设计与 vLLM 的推理优势连接成一条简单、稳定、高效的流水线。开发者不应在统一硬件栈、训练稳定性与推理性能之间被迫取舍。

## 定位

vLLM 社区支持广泛的 LLM 后训练框架，包括（按字母顺序）[NeMo RL](https://github.com/NVIDIA-NeMo/RL)、[OpenRLHF](https://github.com/openrlhf/openrlhf)、[verl](https://github.com/verl-project/verl) 等。我们构建 vime，是为了把 slime 经过验证的训练范式无缝引入 vLLM 生态，提供一个生产可用的桥梁，并与两个项目的快速发布节奏保持同步。

我们希望有不同需求的用户都能为各自的工作流找到合适的 vLLM 生态方案。vLLM 社区将继续支持 vLLM 与更广泛后训练生态的集成。

## 架构概览

vime 采用 slime 三阶段的训练-推理解耦设计，关键差异在于 rollout 后端被替换为 vLLM：

- **训练（Megatron）**：主训练循环，负责参数更新并向 rollout 侧同步权重。
- **Rollout（vLLM + Router）**：推理采样，产生带奖励或验证器信号的训练样本。
- **数据缓冲区**：连接训练侧与 rollout 侧，管理提示注入与自定义 rollout 逻辑。

![vime 通过解耦的数据缓冲区把 Megatron 训练与 vLLM 驱动的 rollout 连接起来。](https://vllm.ai/blog-assets/figures/2026-06-09-vime/arch_v1.png)

vime 通过解耦的数据缓冲区把 Megatron 训练与 vLLM 驱动的 rollout 连接起来。

## 核心能力

- **易用**：参数体系继承 slime 与 Megatron 的约定，vLLM 侧参数使用 `--vllm-` 前缀透传。默认 rollout 入口是 `vime.rollout.vllm_rollout`。
- **稳定的训练-推理对齐**：在典型的 Dense 与 MoE 场景中，`train_rollout_logprob_abs_diff` 在长时间运行中保持在可控范围内。对 MoE，**R3**（路由回放）进一步缩小训练-推理失配。
- **算法与模型覆盖**：GRPO、PPO 等 RL 算法，以及 Qwen3 Dense/MoE、GLM-4.5 等模型，均配有端到端示例和经 CI 验证的路径。
- **多硬件支持**：在框架层面，训练资源、rollout 资源与集群拓扑被统一抽象，便于随着 vLLM 生态的发展，把同一条 RL 流水线复用到不同硬件后端。

## 验证与基准测试

对于 Qwen3-30B-A3B、8 卡 GPU 共置（colocate）、dapo-math-17k 与 GRPO 的组合，GB200 的平均 step 时间约为 **147 秒**，而 H200 约为 **252 秒**。在同一框架下，GB200 的端到端 step 速度约为 H200 的 **1.72x**。

![Qwen3-30B-A3B 的 vime step 速度：GB200 对比 H200。](https://vllm.ai/blog-assets/figures/2026-06-09-vime/Qwen3-30B-A3B_GB200_vs_H200_step_bar.png)

Qwen3-30B-A3B 的 vime step 速度：GB200 对比 H200。

我们还在跨硬件的代表性工作负载上验证了训练-推理一致性与端到端功能。

### A100 上的 Qwen3-4B

对于 A100 上的 Qwen3-4B，采用 GRPO、4 卡训练 + 4 卡推理的非共置配置与 gsm8k，vime 的 `train_rollout_logprob_abs_diff` 在整个训练过程中稳定保持在 **0.011** 左右。基线则随着训练推进持续漂移到 **0.77** 左右，而 vime 提供了更稳定的训练-推理对齐。

![Qwen3-4B 的 vime 与基线训练行为对比。](https://vllm.ai/blog-assets/figures/2026-06-09-vime/Qwen3-4B_Training_raw_reward_compare.png)

Qwen3-4B 的 vime 与基线训练行为对比。

### 启用 R3 的 Qwen3-30B-A3B MoE

对于 A100 上的 Qwen3-30B-A3B MoE，采用 4 卡训练 GPU、4 卡推理 GPU、dapo-math-17k 与 EP=4，启用 vime 的 R3 路由回放后，logprob 差异从约 **0.019** 降到约 **0.013**，显著减少了 MoE 的训练-推理失配。

![R3 路由回放减少 Qwen3-30B-A3B MoE 的训练-推理失配。](https://vllm.ai/blog-assets/figures/2026-06-09-vime/Qwen3-30B-A3B_MoE_R3_Comparison.png)

R3 路由回放减少 Qwen3-30B-A3B MoE 的训练-推理失配。

### GB200 上的 Qwen3-30B-A3B MoE

对于 GB200 上的 Qwen3-30B-A3B MoE，采用 8 卡 GPU 共置与 dapo-math-17k，vime 与基线的 `raw_reward` 曲线高度吻合。两者都把 `train_rollout_logprob_abs_diff` 稳定保持在 **0.018** 左右，基线侧没有出现持续漂移。

![GB200 上的 Qwen3-30B-A3B MoE 在共置训练与 rollout 中表现出稳定对齐。](https://vllm.ai/blog-assets/figures/2026-06-09-vime/Qwen3-30B-A3B_GB200_vime_baseline_compare.png)

GB200 上的 Qwen3-30B-A3B MoE 在共置训练与 rollout 中表现出稳定对齐。

### GB200 上的 GLM-4.5-Air

对于 GB200 上的 GLM-4.5-Air，采用 GRPO、8 卡 GPU 共置与 dapo-math-17k，`raw_reward` 在 100 个 step 内持续上升，均值约为 **0.56**。`train_rollout_logprob_abs_diff` 保持在 **0.02-0.03** 区间，均值约为 **0.028**，表明训练-推理对齐扎实。

![GB200 上的 GLM-4.5-Air 在奖励提升的同时保持稳定的 logprob 对齐。](https://vllm.ai/blog-assets/figures/2026-06-09-vime/GLM-4.5-Air_GB200_precision.png)

GB200 上的 GLM-4.5-Air 在奖励提升的同时保持稳定的 logprob 对齐。

## 路线图

vime 仍在快速演进，路线图聚焦三个方向：

- **更深入的 vLLM 集成**：持续采用 Router、PD 分离、FP8 与多模型服务等 vLLM 新能力。
- **多硬件扩展**：沿着 vLLM 的硬件插件体系扩展后端，让 vime 能在更多加速器与集群配置上高效运行。
- **训练效率与算法**：完全异步流水线、训练-推理失配校正、面向多轮工具调用与多智能体场景的 Agentic RL，以及对 MoE、VLM 等新架构的快速跟进。

## 快速开始

上手路径与 slime 类似：配置 Megatron 训练资源与 vLLM rollout 资源，准备好检查点与数据，然后启动 `train.py` 或 `train_async.py`。

- **文档**：[快速开始](https://github.com/vllm-project/vime/tree/main/docs/en/get_started)
- **示例**：`scripts/` 与 `examples/` 目录覆盖 Qwen3-4B、Qwen3-30B-A3B MoE、GLM-4.5-Air 等场景。

## 加入社区

vime 由 vLLM 社区维护，以 Apache 2.0 许可开源，并站在 slime、Megatron-LM 与 vLLM 等项目的肩膀之上。

- **代码与文档**：[github.com/vllm-project/vime](https://github.com/vllm-project/vime)
- **贡献**：欢迎提交 Issue 与 PR。Pre-commit 保证代码风格一致。
- **反馈**：欢迎在 GitHub 上分享使用体验、性能数据与功能建议。

简单的架构、稳定的行为、高效的性能：vime 希望为更多开发者铺就 RL 后训练的主流水线。欢迎加入我们，一起把这条流水线带向更多场景。

## 致谢

**贡献者**：Ao Shen、kaiyuan、princepride、Dakai An、knlnguyen1802、gcanlin、SamitHuang 与 Meihan-chen。

我们感谢 [slime](https://github.com/THUDM/slime)、[Megatron-LM](https://github.com/NVIDIA/Megatron-LM) 与 [vLLM](https://github.com/vllm-project/vllm) 项目维护者所做的开创性工作。同时感谢 Kaichao You、Roger Wang、Hongsheng Liu 与 Xiyuan Wang 对 vime 项目组织工作的支持与贡献。
