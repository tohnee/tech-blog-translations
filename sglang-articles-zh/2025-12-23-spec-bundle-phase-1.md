---
title: "SpecBundle 与 SpecForge v0.2：生产级投机解码模型与框架"
title_en: "SpecBundle & SpecForge v0.2: Production-Ready Speculative Decoding Models and Framework"
author: "SpecForge Team, Ant Group AQ Team, Nex-AGI Team, EigenAI Team"
date: "December 23, 2025"
source: https://lmsys.org/blog/2025-12-23-spec-bundle-phase-1/
translated: 2026-09-12
previewImg: /images/blog/specbundle-phase1/preview.png
---

# SpecBundle 与 SpecForge v0.2：生产级投机解码模型与框架

> 原文：[SpecBundle & SpecForge v0.2: Production-Ready Speculative Decoding Models and Framework](https://lmsys.org/blog/2025-12-23-spec-bundle-phase-1/) · LMSYS Blog · SpecForge Team, Ant Group AQ Team, Nex-AGI Team, EigenAI Team

## TL;DR

SpecForge 团队与多家行业伙伴——包括**蚂蚁集团（Ant）、美团（Meituan）、Nex-AGI 和 EigenAI**——合作发布了 [**SpecBundle（第一阶段）**](https://huggingface.co/collections/lmsys/specbundle)，这是一组在大规模数据集上训练得到的生产级 EAGLE-3 模型检查点。**SpecBundle** 旨在提升投机解码的可用性与真实场景表现，第一阶段聚焦指令微调（instruct-tuned）模型。

与本次发布同步，[**SpecForge v0.2**](https://github.com/sgl-project/SpecForge) 带来了重大系统升级，包括为提升易用性而进行的大规模重构以及对多种执行后端的支持，进一步增强了可扩展性与生产可用性。

## 背景

[投机解码（speculative decoding）](https://arxiv.org/abs/2302.01318)于 2023 年首次提出，是一种颇具前景的加速大语言模型（LLM）推理的技术：由轻量级草稿模型（draft model）提出多个 token，再由更强的目标模型（target model）加以验证。原则上，这种方法能够在不牺牲输出质量的前提下大幅降低解码延迟，因此对本地部署和企业部署都颇具吸引力。过去几年里，研究界持续打磨这一范式，提出了日益精巧的方法，最终发展为以 [EAGLE3](https://arxiv.org/abs/2503.01840) 为代表的当前最优（SOTA）方案——它们在 token 接受率与端到端加速两方面都展现出强有力的理论保证和实证收益。

### 现存问题

尽管有这些进展，投机解码——尤其是 EAGLE3 这类 SOTA 方法——尚未在开源社区得到广泛采用。我们将这一差距主要归因于三个因素。

**因素 1：** 缺少易于获取、可直接投入生产的投机解码模型训练工具。现有的大多数实现仍是研究原型，要么缺乏维护，要么适用范围狭窄；另一些则只提供了过于简化的实现，缺乏足够的系统级优化。因此，这些工具难以支撑当今 LLM 生态中常用的多样化模型架构与规模。

**因素 2：** 高质量草稿模型的供给仍是主要瓶颈。有效的投机解码高度依赖草稿模型的强弱，而这类模型在开源社区中相当稀缺，如下表所示。EAGLE3 这类方法需要额外训练草稿模型，而公开可用的 EAGLE3 检查点基本局限于原作者等少数几方的发布。这种受限的供给极大阻碍了投机解码的更广泛采用。

| 模型                                       | 原生 MTP | 社区 EAGLE3 | SpecBundle |
| ----------------------------------------- | ---------- | ---------------- | ---------- |
| meta-llama/Llama-3.1-8B-Instruct          | ❌         | ✅               | ✅         |
| meta-llama/Llama-3.3-70B-Instruct         | ❌         | ✅               | ✅         |
| meta-llama/Llama-4-Scout-17B-16E-Instruct | ❌         | ✅               | ✅         |
| Qwen/Qwen3-30B-A3B-Instruct-2507          | ❌         | ❌               | ✅         |
| Qwen/Qwen3-235B-A22B-Instruct-2507        | ❌         | ✅               | ✅         |
| Qwen/Qwen3-Next-80B-A3B-Instruct-FP8      | ✅         | ❌               | ✅         |
| Qwen/Qwen3-Coder-30B-A3B-Instruct         | ❌         | ❌               | ✅         |
| Qwen/Qwen3-Coder-480B-A35B-Instruct       | ❌         | ❌               | ✅         |
| inclusionAI/Ling-flash-2.0                | ❌         | ❌               | ✅         |
| moonshotai/Kimi-K2-Instruct               | ❌         | ❌               | ✅         |
| nex-agi/Qwen3-30B-A3B-Nex-N1              | ❌         | ❌               | ✅         |
| nex-agi/Qwen3-32B-Nex-N1                  | ❌         | ❌               | ✅         |

**因素 3**：现有大多数草稿模型是在相对较小或经过精心筛选的数据集上训练的，并未扩展到现代 LLM 训练所使用的大规模、多样化语料。因此，这些模型在与强目标模型搭配时，往往泛化能力有限、token 接受率偏低，削弱了投机解码所能带来的实际加速。缺少大规模、生产级的草稿模型，EAGLE3 这类先进方法的全部潜力便在很大程度上无从兑现。

### 动机

上述差距正是我们发布 [**SpecForge v0.2**](https://github.com/sgl-project/SpecForge) 与 [**SpecBundle**](https://huggingface.co/collections/lmsys/specbundle) 的动因。作为一个中立的开源社区，SpecForge 团队希望通过提供生产级训练框架与高性能草稿模型，主动推动投机解码的发展，让这项技术对更广泛的社区而言既实用又触手可及。

这一举措带来以下几项关键收益：

1. 为推进投机解码方法提供更标准化、更可扩展的基线，拓展研究可能性。
2. 借助 [Ollama](https://github.com/ollama/ollama) 等工具支持轻量级部署场景，实现更快的本地推理与模型服务。
3. 借助 [SGLang](https://github.com/sgl-project/sglang) 等推理引擎，在不牺牲输出质量的前提下提升推理吞吐量，降低企业部署成本。
4. 以 EAGLE3 检查点的形式提供强大的初始化起点，可针对特定领域任务高效微调。
5. 通过支持将 [ReSpec](https://arxiv.org/abs/2510.26475) 等技术集成到 [slime](https://github.com/THUDM/slime) 等现有强化学习（RL）框架中，提升强化学习工作流的效率。

## SpecForge v0.2

SpecForge 开源至今已有约五个月，得益于出色社区的支持，系统已演进为一个显著更可靠、更高效、更具可扩展性的解决方案。在过去两个月中，我们为 SpecBundle 训练了大量模型，期间发现了 SpecForge 原始设计中的若干局限。这些洞察推动了框架的全面升级，以同时改进性能与易用性。**SpecForge v0.2** 的主要变更总结如下。

### 易用性改进

在 SpecForge 的早期版本中，一些功能是各自独立开发的，未充分考虑长期可维护性或用户体验，这有时会让用户感到困惑。在过去两个月里，我们将易用性置于优先地位，对框架进行了大幅重构。关键改进包括：

1. 重构了数据处理流水线，消除重复并提升效率。例如，通过数据并行与异步处理，数据再生成速度最高比 v0.1 快 **10 倍**。
2. 将在线与离线训练脚本统一为单一实现。这一整合确保了训练逻辑的一致性，避免在线与离线训练模式之间出现分歧。
3. 改进了文档结构与清晰度，逻辑流程更清晰、可读性更好，帮助用户更高效地上手与迭代。

### 多后端支持

早期版本的 SpecForge 高度依赖目标模型的自研实现，使得模型支持既繁琐又容易出错。为了解决这一局限并更好地利用更广泛的生态，我们为目标模型集成引入了统一接口。

在 **v0.2** 中，我们引入了 `Eagle3TargetModel` 接口，从而无缝支持多种执行后端。目前，SpecForge 已集成 **SGLang** 与 **Hugging Face Transformers** 两种后端。现在新增一个后端只需实现 `Eagle3TargetModel.generate_eagle3_data` 方法，显著降低了扩展门槛并提升了长期可维护性。

```python
target_model = get_eagle3_target_model(
                pretrained_model_name_or_path="meta-llama/Llama-3.1-8B-Instruct",
                backend="sglang",
                torch_dtype=torch.bfloat16,
                device="cuda",
                cache_dir=args.model_download_dir,
                **target_model_kwargs,
            )
```

这些后端不仅减轻了开发者在模型实现与性能优化上的负担，也为用户在不同训练场景中提供了灵活选择。有了多个后端选项，用户可以针对自己的开发与运行时需求选择最合适的后端。

<p align="center">
  <img src="/images/blog/specbundle-phase1/backend.png" alt="Logo preview">
  <br>
</p>

## SpecBundle 计划

如上所述，开源社区在投机解码方案的可用性与性能两方面仍面临显著瓶颈。SpecBundle 正是对这些挑战的直接回应——这是一项由开源社区与行业伙伴共同推动的计划，旨在弥合这些差距。据我们所知，这是首个以普及投机解码为目标的开放行动：通过为主流开源模型配备高性能 EAGLE3 草稿模型权重，让投机解码的采用走向大众化。

<div style="border-left: 4px solid #3b82f6; padding: 10px 12px; margin: 12px 0; background: #eff6ff; border-radius: 8px;">
  <strong>👉 查看 <a href="https://docs.sglang.io/SpecForge/community_resources/specbundle.html">SpecBundle 文档</a>。</strong>
</div>

在本次首期发布中，SpecBundle 路线图仅聚焦指令微调模型，如下图所示。我们相信，将投机解码支持扩展到更广泛的模型范围，将进一步降低本地部署与企业部署的成本，同时使强化学习（RL）训练流水线中的 rollout 更加高效。

<p align="center">
  <img src="/images/blog/specbundle-phase1/roadmap.png" alt="Logo preview">
  <br>
</p>

与此同时，SpecBundle 也是对 SpecForge 的一次大规模验证，展示了其效率、可扩展性与可伸缩性。通过成功为参数量从 8B 到 1T 的目标模型训练草稿模型，我们确认近期的架构与系统改进已使 SpecForge 达到生产可用水平。

我们热忱欢迎社区贡献与产业合作。如果你认同我们加速 LLM 推理与训练的愿景，欢迎加入我们，共同拓展投机解码的能力边界。

### 性能

对于 SpecBundle 发布的所有模型，我们都使用 SGLang 重新生成了模型回复，使训练数据分布与实际模型输出更好地对齐。这种对齐显著提升了投机解码的 token 接受率。

与依赖 ShareGPT 和 UltraChat 数据集（约 32 万条样本）的原始 EAGLE 论文不同，SpecBundle 在 [Perfect-Blend](https://huggingface.co/datasets/mlabonne/open-perfectblend) 数据集上训练，该数据集包含 **140 万条样本**，覆盖的领域范围广泛得多——尤其是代码与数学领域。

因此，SpecBundle 不仅支持众多主流指令微调模型，还在各类基准测试中提供了强劲而一致的加速，相比标准解码基线实现**最高 4 倍的端到端推理加速**。

- **与现有开源权重的对比**

<div style="display:flex; gap:16px;">
  <img src="/images/blog/specbundle-phase1/llama4-perf.png" alt="Llama-4 scout" style="width:50%;">
  <img src="/images/blog/specbundle-phase1/qwen-235b-perf.png" alt="Qwen-235B" style="width:50%;">
</div>

- **SpecBundle 在 100B 以上参数模型上的表现**

<div style="display:flex; gap:16px;">
  <img src="/images/blog/specbundle-phase1/ling-perf.png" alt="ling-flash-v2" style="width:50%;">
  <img src="/images/blog/specbundle-phase1/kimi-perf.png" alt="kimi-k2" style="width:50%;">
</div>

<div style="border-left: 4px solid #3b82f6; padding: 10px 12px; margin: 12px 0; background: #eff6ff; border-radius: 8px;">
  <strong>👉 查看<a href="https://huggingface.co/collections/lmsys/specbundle">完整模型合集</a>。</strong>
</div>

我们已在 [SpecBundle 网站](https://docs.sglang.io/SpecForge/SpecBundle/index.html)上发布了完整的基准测试结果。请访问该网站查看更详细的评测结果。

## 路线图

最后同样重要的是，SpecForge 团队将在整个 2026 年持续构建并扩展 LLM 生态。我们刚刚发布了 2026 年 Q1 路线图，非常期待听到你的反馈，并邀请你加入这段旅程。

我们接下来的工作将主要聚焦于：

- 长上下文训练
- 视觉语言模型（VLM）支持
- 系统级性能优化
- MTP（多 token 预测）微调
- SpecBundle 第二阶段（推理模型）与第三阶段（VLM）

无论你是研究者、实践者还是产业伙伴，我们都热忱欢迎你的想法与贡献，携手共同突破可扩展、高效 LLM 系统的边界。

<div style="border-left: 4px solid #3b82f6; padding: 10px 12px; margin: 12px 0; background: #eff6ff; border-radius: 8px;">
  <strong>👉 查看<a href="https://github.com/sgl-project/SpecForge/issues/374">完整路线图</a>。</strong>
</div>

## 致谢

我们衷心感谢开源社区开发者与产业合作伙伴的共同努力，尤其感谢**蚂蚁集团 AQ 团队（Ant Group AQ Team）**、**美团（Meituan）**、**Nex-AGI (Qiji Zhifeng)** 与 **EigenAI** 对 SpecBundle 与 SpecForge 开发的宝贵贡献。

- SpecForge Team: Shenggui Li, Chao Wang, Yubo Wang, Yefei Chen, Yikai Zhu, Jiaping Wang, Jin Pan, Tao Liu, Fan Yin, Shuai Shi, Yineng Zhang
- Ant Group AQ Team: Ji Li, Yanan Gao, Zhiling Ye
- Meituan Search Team: Laixin Xie
- Nex-AGI (Qiji Zhifeng) Team: Qiaoling Chen, Guoteng Wang, Peng Sun
- EigenAI Team: Xiaomin Dong, Jinglei Cheng
