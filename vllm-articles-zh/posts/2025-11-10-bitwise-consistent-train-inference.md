---
title: "告别训练-推理不一致：使用 vLLM 与 TorchTitan 实现位级一致的在策略强化学习"
title_en: "No More Train-Inference Mismatch: Bitwise Consistent On-Policy Reinforcement Learning with vLLM and TorchTitan"
source: https://vllm.ai/blog/2025-11-10-bitwise-consistent-train-inference
crawled: 2026-09-12
translated: 2026-09-13
---

# 告别训练-推理不一致：使用 vLLM 与 TorchTitan 实现位级一致的在策略强化学习

> 原文：[No More Train-Inference Mismatch: Bitwise Consistent On-Policy Reinforcement Learning with vLLM and TorchTitan](https://vllm.ai/blog/2025-11-10-bitwise-consistent-train-inference) · vLLM 博客

vLLM 与 TorchTitan 团队

[#性能](https://vllm.ai/blog/tags/performance)

我们演示了一次开源的位级一致（bitwise consistent）在策略强化学习（on-policy RL）运行，以 [TorchTitan](https://github.com/pytorch/torchtitan) 作为训练引擎、[vLLM](https://github.com/vllm-project/vllm) 作为推理引擎。基于 [vLLM 近期在批不变推理（batch-invariant inference）方面的工作](https://docs.vllm.ai/en/latest/features/batch_invariance/)，我们在[开源的说明文档](https://github.com/pytorch/torchtitan/tree/main/torchtitan/experiments/deterministic_vllm_rl)中展示了如何对 Qwen3 1.7B 进行 RL 微调，并使训练与推理的数值在位级上完全一致：

![](https://vllm.ai/blog-assets/figures/2025-11-10-bitwise-exact-rl/rl-script-demo.png)

强化学习已被证明会放大训练器（trainer）与采样器（sampler）之间微小的数值失配，从而导致非确定且不稳定的训练行为（[He 等](https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/)、[Yao, Liu 等](https://fengyao.notion.site/off-policy-rl) 与 [Liu, Li 等](https://yingru.notion.site/When-Speed-Kills-Stability-Demystifying-RL-Collapse-from-the-Training-Inference-Mismatch-271211a558b7808d8b12d403fd15edda)）。我们通过自己的实验结果验证了数值对 RL 结果的影响：让采样器使用与训练器不同的内核（`batch_inv_OFF`）时，奖励在 100 步内出现下降。而启用位级精确训练（`batch_inv_ON`，此时 `kl_div` 始终等于 0.0）后，我们看到模型不仅用更少的步数完成训练，还达到了更高的总奖励。

![](https://vllm.ai/blog-assets/figures/2025-11-10-bitwise-exact-rl/reward-comparison.png)

## 方法

由于工作负载特性不同，训练与推理框架往往使用截然不同的内核。即使在同一个推理框架内，不同场景也会选择不同的内核：高批大小（batch size）场景的内核在批维度上重度并行，而低批大小场景的内核更多在单个实例内部并行，以更好地利用 GPU 上的并行核心。所有这些差异都会在训练与推理框架之间造成数值差异，进而导致更差的 RL 结果。

在这项工作中，我们处理了两个不同框架之间的不变性：TorchTitan 作为训练框架，vLLM 作为推理框架。我们审计了前向传播过程中每一个内核的每一次调用，确保它们在两个框架之间位级等价。我们复用了 vLLM [近期批不变性（batch invariance）工作](https://docs.vllm.ai/en/latest/features/batch_invariance/)中的前向内核，并为这些算子编写了[简单反向传播](https://github.com/pytorch/torchtitan/blob/main/torchtitan/experiments/deterministic_vllm_rl/batch_invariant_backward.py)。

vLLM 有许多深度优化的融合算子，例如 SiLU MLP 和 RMSNorm（带残差相加）。为了保持位级等价，我们为前向传播导入了完全相同的算子。这些算子需要注册自定义的反向传播，而这可以直接用 TorchTitan 所使用的原生 PyTorch 完成。

对于 RL 演示，我们编写了一个使用 GSM8K 和正确性奖励的通用强化学习脚本。我们使用 TorchTitan 的工具实现训练器，并编写了一个自定义生成器。我们的生成器 `VLLMRolloutEngine` 封装了一些简单功能，比如调用 generate 和更新权重。我们以全同步方式运行所有内容，在单台主机上交替执行训练器与生成器。这是严格的在策略（on-policy）执行的示范，但在大规模运行中并不常见。

## 下一步计划

我们将继续推进位级一致的训练与推理。要跟进这项工作，请参阅相关 RFC：[#28326](https://github.com/vllm-project/vllm/issues/28326) 与 [#27433](https://github.com/vllm-project/vllm/issues/27433)。更具体地说，我们将聚焦以下方向：

**统一的模型定义。** 虽然我们已经演示了位级等价的训练与推理结果，但目前仍存在两份模型代码，一份用于训练，一份用于推理。这对我们的首次集成来说容易实现，但对长期维护而言十分脆弱：对任何一份模型代码的细微改动都会破坏训练与推理之间的等价性，导致数值失配。让训练与推理框架共享同一份模型代码，将消除意外人为错误的可能性，并使位级一致这一性质更易维护。

**编译支持。** 目前，我们没有对 TorchTitan 模型使用 `torch.compile`，因此对 vLLM 强制使用 eager 模式。移除这一约束并不困难，但需要构建一个 `torch.compile` 版本的 TorchTitan 模型。vLLM 大量使用 `torch.compile`，并且能够在其中保持批不变性——但要保持跨框架兼容性，需要对训练侧版本的模型进行修改。这将作为后续工作推进！

**RL 性能** 我们目前的结果显示，位级一致的 RL 运行比非位级一致的情况慢 2.4 倍。我们将继续通过更好地调优批不变内核，以及利用编译等技术，来改进 vLLM 的性能。

**更广泛的模型支持** 我们计划把这一位级一致的 RL 框架从 Qwen3 1.7B 扩展到其他开源模型。我们还将推广审计工具与反向传播实现，使其覆盖更广泛的算子类型，让训练-推理位级一致性成为一个可扩展、可复用的特性。

如果你对此感兴趣或想参与贡献，欢迎加入以下 Slack 频道：

- [#sig-post-training](https://vllm-dev.slack.com/archives/C07UUL8E61Z)
- [#sig-batch-invariant](https://vllm-dev.slack.com/archives/C09JVU355CG)

---

*作者：
Bram Wasti, Wentao Ye, Teja Rao, Michael Goin, Paul Zhang, Tianyu Liu, Natalia Gimelshein, Woosuk Kwon, Kaichao You, Zhuohan Li*
