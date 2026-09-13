---
title: "用 AutoRound 量化加速 vLLM-Omni 推理"
title_en: "Accelerating vLLM-Omni Inference with AutoRound Quantization"
source: https://vllm.ai/blog/2026-06-02-vllm-omni-autoround
crawled: 2026-09-12
translated: 2026-09-13
---

# 用 AutoRound 量化加速 vLLM-Omni 推理

> 原文：[Accelerating vLLM-Omni Inference with AutoRound Quantization](https://vllm.ai/blog/2026-06-02-vllm-omni-autoround) · vLLM 博客

作者：vLLM-Omni 社区、Intel AutoRound 团队

[#量化](https://vllm.ai/blog/tags/quantization)[#多模态](https://vllm.ai/blog/tags/multimodal)[#vllm-omni](https://vllm.ai/blog/tags/vllm-omni)[#硬件](https://vllm.ai/blog/tags/hardware)

## TL;DR

我们很高兴地宣布：[AutoRound](https://github.com/intel/auto-round)——Intel 最先进的训练后量化（PTQ）算法——现已全面集成到 [vLLM-Omni](https://github.com/vllm-project/vllm-omni) 中，实现了“一次量化、直接服务”的精简工作流。这次合作为多模态 Omni、扩散视频和多阶段图像生成管线带来了 W4A16（4-bit 权重 / 16-bit 激活值）量化。

我们的生产级基准测试套件的关键实证亮点包括：

- **大幅节省显存：** 大型 Omni 模型的检查点总大小最多可减少 62%，把 Qwen3-Omni-30B-A3B 从 66 GB 压到 25 GB。
- **精度保持：** Qwen3-Omni-30B 的 W4A16 量化版本在 OmniBench 上取得了亮眼分数，略好于其 BF16 参考版本。同时，它把文生图质量漂移限制在仅约 1.3%，表明在被评估的工作负载下，4-bit 量化能够保持多模态质量。
- **生产服务收益：** 在 Intel XPU（B60）上解锁高级架构优化，通过 CFG Parallel 执行实现比顺序 BF16 基线服务快 1.55–1.67x 的引导生成。
- **跨后端集成：** 在 Intel XPU 和 NVIDIA GPU 架构上验证了原生执行路径。

## 1. 引言：vLLM-Omni 与 AutoRound 相遇

[vLLM-Omni](https://github.com/vllm-project/vllm-omni) 面向扩散模型、多模态 Omni 模型及相关多阶段生成栈的高性能服务而设计。这种广度让量化显得格外有价值：目标不仅是压缩单个 transformer，而是让一个多样化的运行时组合更容易部署到真实硬件上。

[AutoRound](https://github.com/intel/auto-round) 由 Intel 开发，在 EMNLP 2024 关于通过带符号梯度下降进行权重取整的工作中首次被描述，是一种基于调优的训练后量化算法。其核心思想是对取整与截断进行联合优化，每个被量化张量有三个可学习参数：用于取整偏移的 `V`，以及用于截断范围控制的 `alpha` 和 `beta`。在实践中，这让 AutoRound 的低比特精度强于朴素的最近取整（round-to-nearest）基线，同时仍能产出静态检查点，在推理时不带来任何额外的量化开销。

这三层协作——AutoRound 中的算法工作、vLLM-Omni 中的运行时集成，以及 HuggingFace 上不断增长的 INT4 检查点目录——讲述了一个连贯的故事：AutoRound 不只是一种量化技术，更是一条从研究通往生产级低比特 omni 推理的端到端路径。

运行时路径刻意保持简单。vLLM-Omni 读取检查点元数据，检测 `quantization_config.quant_method = "auto-round"`，把检查点块重映射到运行时模块，并选择匹配的计算后端。这种检查点驱动的流程对生产尤为重要，因为它让服务 API 与普通模型加载完全一致。

## 2. 模型覆盖

经过验证的 AutoRound + vLLM-Omni 生态覆盖三大主要多模态范式。

### 2.1 Omni 多模态模型

这些模型管理统一的文本、视觉与音频处理回路，由于跨模态嵌入对齐而带来独特的量化挑战。

- **Qwen3-Omni-30B-A3B-Instruct**（[Intel/Qwen3-Omni-30B-A3B-Instruct-int4-AutoRound](https://huggingface.co/Intel/Qwen3-Omni-30B-A3B-Instruct-int4-AutoRound)）：大规模旗舰多模态模型。已在 vLLM-Omni 中集成并验证。
- **Qwen2.5-Omni-7B**（[Intel/Qwen2.5-Omni-7B-int4-AutoRound](https://huggingface.co/Intel/Qwen2.5-Omni-7B-int4-AutoRound)）：轻量、低延迟的跨模态引擎。已在 vLLM-Omni 中集成并验证。

### 2.2 扩散与多阶段图像生成

- **GLM-Image**（[Intel/GLM-Image-int4-AutoRound](https://huggingface.co/Intel/GLM-Image-int4-AutoRound)）：多阶段文生图管线。已在 vLLM-Omni 中集成并验证。
- **FLUX.1-dev**（[vllm-project-org/FLUX.1-dev-AutoRound-w4a16](https://huggingface.co/vllm-project-org/FLUX.1-dev-AutoRound-w4a16)）：高保真扩散 transformer（DiT）。已在 vLLM-Omni 中集成并验证。
- **BAGEL-7B-MoT**（[Intel/BAGEL-7B-MoT-int4-AutoRound](https://huggingface.co/Intel/BAGEL-7B-MoT-int4-AutoRound)）：检查点已发布；运行时集成进行中。
- **Ovis-Image-7B**（[Intel/Ovis-Image-7B-int4-AutoRound](https://huggingface.co/Intel/Ovis-Image-7B-int4-AutoRound)）：检查点已发布；运行时集成进行中。

### 2.3 视频扩散

Wan2.2 家族代表最先进的时空视频生成模型，其 AutoRound INT4 检查点已在 vLLM-Omni 中验证：

- **I2V-A14B**（[Intel/Wan2.2-I2V-A14B-Diffusers-int4-AutoRound](https://huggingface.co/Intel/Wan2.2-I2V-A14B-Diffusers-int4-AutoRound)）
- **T2V-A14B**（[Intel/Wan2.2-T2V-A14B-Diffusers-int4-AutoRound](https://huggingface.co/Intel/Wan2.2-T2V-A14B-Diffusers-int4-AutoRound)）
- **TI2V-5B**（[Intel/Wan2.2-TI2V-5B-Diffusers-int4-AutoRound](https://huggingface.co/Intel/Wan2.2-TI2V-5B-Diffusers-int4-AutoRound)）

## 3. 使用方法

通过把所有量化与调优操作都限制在离线管线内，这次集成让生产代码保持精简，并专注于高性能推理。

### 3.1 使用量化模型进行推理

对 FLUX.1-dev 而言，Python API 看起来就像普通的 vLLM-Omni 加载。唯一的区别是检查点路径。

```
from vllm_omni import Omni
from vllm_omni.inputs.data import OmniDiffusionSamplingParams

if __name__ == '__main__':
    omni = Omni(model="vllm-project-org/FLUX.1-dev-AutoRound-w4a16")
    outputs = omni.generate(
        "A cat sitting on a windowsill",
        OmniDiffusionSamplingParams(num_inference_steps=28, guidance_scale=3.5),
    )
    outputs[0].images[0].save("output.png")
```

对 Wan2.2 视频模型而言，服务仍然是一条标准的 vLLM-Omni 命令。服务器运行起来之后，请求走与 BF16 版本相同的视频端点。

```
vllm serve Intel/Wan2.2-T2V-A14B-Diffusers-int4-AutoRound --omni --port 8091
```

```
curl -X POST "http://127.0.0.1:8091/v1/videos/sync" \
  -F 'prompt=Cherry blossoms swaying gently in the breeze, cinematic motion' \
  -F 'width=832' -F 'height=480' -F 'num_frames=48' \
  -F 'num_inference_steps=40' -F 'guidance_scale=5.0' \
  --output t2v_output.mp4
```

对 Qwen2.5-Omni 等 Omni 模型而言，OpenAI 兼容聊天接口同样保持不变。

```
vllm serve Intel/Qwen2.5-Omni-7B-int4-AutoRound --omni --port 8091
```

```
curl -s http://localhost:8091/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Intel/Qwen2.5-Omni-7B-int4-AutoRound",
    "messages": [{"role": "user", "content": "What is 2 + 3?"}],
    "max_tokens": 128
  }'
```

重要的运维细节是：vLLM-Omni 会从检查点自动检测量化元数据。对预量化的 AutoRound 模型，推理时不需要额外添加 `--quantization` 标志。

### 3.2 量化一个新模型

新检查点用 AutoRound 工具离线生成，然后由 vLLM-Omni 直接服务。服务期间不进行任何校准或量化工作。这种分离把量化实验挡在热服务路径之外，确保生产推理始终专注于执行效率。

```
# FLUX.1-dev
auto-round \
  --model black-forest-labs/FLUX.1-dev \
  --scheme W4A16 \
  --batch_size 1 \
  --disable_opt_rtn \
  --dataset coco2014 \
  --iters 0

# Wan2.2-T2V-A14B
auto-round \
  --model_name Wan-AI/Wan2.2-T2V-A14B-Diffusers \
  --format auto_round \
  --scheme W4A16 \
  --iters 100 \
  --nsamples 32 \
  --batch_size 1 \
  --num-inference-steps 3 \
  --guidance-scale 5.0 \
  --dataset coco2014 \
  --output_dir Wan2.2-T2V-A14B-Diffusers-int4-AutoRound

# Qwen3-Omni-30B-A3B-Instruct
auto-round \
  --model Qwen/Qwen3-Omni-30B-A3B-Instruct \
  --bits 4 \
  --group_size 128 \
  --format auto_round \
  --iters 200 \
  --lr 5e-3 \
  --output_dir tmp_qwen3_omni_w4a16 \
  --trust_remote_code
```

生成的检查点在 `config.json` 中包含量化元数据：

```
{
  "quantization_config": {
    "quant_method": "auto-round",
    "bits": 4,
    "group_size": 128,
    "sym": true,
    "packing_format": "auto_round:auto_gptq"
  }
}
```

在实践中，AutoRound 与 vLLM 的指南表明，**128 个校准样本和大约 200 次优化迭代**往往足以让许多工作负载达到稳定收敛，不过更大或更敏感的模型可能受益于更多调优。确切的校准设置取决于模型家族、任务类型和部署约束。

### 3.3 质量验证

对扩散模型而言，vLLM-Omni 还提供了一个比较工具，用于在 BF16 参考与量化候选之间进行同种子回归测试。

```
python -m vllm_omni.quantization.tools.compare_diffusion_trajectory_similarity \
  --task t2i \
  --reference-model black-forest-labs/FLUX.1-dev \
  --candidate-model vllm-project-org/FLUX.1-dev-AutoRound-w4a16 \
  --prompt "a cup of coffee on the table" \
  --height 512 --width 512 \
  --num-inference-steps 20 \
  --seed 142 \
  --output-json /tmp/flux_similarity/result.json
```

## 4. 定量评估：精度与质量

只有保住模型的核心智能，量化才有用。我们使用自动化评估套件，对 AutoRound 集成开展了广泛的多模态回归测试。

### 4.1 Omni 多模态评估（OmniBench）

我们使用 evalscope 在 100 个高度复杂的多模态任务（同时纳入图像与音频模态）上运行了完全相同的评估。W4A16 模型取得了略高于 BF16 基线的 OmniBench 总分。

![Figure 1: OmniBench results comparing BF16 and W4A16 AutoRound quantized variants of Qwen3-Omni-30B-A3B-Instruct.](https://vllm.ai/blog-assets/figures/2026-06-02-vllm-omni-autoround/fig1_omnibench.png)

图 1：对比 Qwen3-Omni-30B-A3B-Instruct 的 BF16 与 W4A16 AutoRound 量化版本的 OmniBench 结果。

### 4.2 多阶段扩散评估（TIIF-Bench）

对多阶段文生图系统，性能在 9 个结构化子属性上被量化，这些子属性评估对齐、构图和保真度。

![Figure 2: TIIF-Bench evaluation across 9 structural sub-attributes for multi-stage text-to-image pipelines.](https://vllm.ai/blog-assets/figures/2026-06-02-vllm-omni-autoround/fig2_tiif_bench.png)

图 2：针对多阶段文生图管线在 9 个结构化子属性上的 TIIF-Bench 评估。

所有维度上的平均精度下降约为 1.3%，稳稳处于生产部署可接受的容差范围内。

### 4.3 视频生成评估（Wan2.2）

由于时间一致性漂移，视频管线在朴素的标量量化下很脆弱。AutoRound 使用跨多个维度的客观指标进行评估：

![Figure 3: Text-to-Video evaluation on Wan2.2 T2V-A14B under W4A16 AutoRound quantization.](https://vllm.ai/blog-assets/figures/2026-06-02-vllm-omni-autoround/fig3_wan22_t2v.png)

图 3：在 W4A16 AutoRound 量化下对 Wan2.2 T2V-A14B 的文生视频评估。

![Figure 4: Image-to-Video evaluation on Wan2.2 I2V-A14B under W4A16 AutoRound quantization.](https://vllm.ai/blog-assets/figures/2026-06-02-vllm-omni-autoround/fig4_wan22_i2v.png)

图 4：在 W4A16 AutoRound 量化下对 Wan2.2 I2V-A14B 的图生视频评估。

在 W4A16 AutoRound 下，文生视频变体（T2V-A14B）在结构一致性指标上反而出现了小幅提升。这一行为与“截断优化可能带来正则化效应”的假设相符。

## 5. 性能、占用与服务基准测试

### 5.1 显存占用优化

W4A16 AutoRound 的一阶收益是检查点大小和执行内存占用的显著缩减。W4A16 把量化权重存储从 BF16 基线缩减到原始权重占用的大约四分之一，这就是为什么一阶收益是内存余量。端到端加速则取决于工作负载此前有多大程度受内存容量或内存带宽瓶颈制约。

![Figure 5: VRAM footprint comparison between BF16 and W4A16 AutoRound across vLLM-Omni model families.](https://vllm.ai/blog-assets/figures/2026-06-02-vllm-omni-autoround/fig5_vram_footprint.png)

图 5：vLLM-Omni 各模型家族上 BF16 与 W4A16 AutoRound 的显存占用对比。

有一个细微之处很重要：并非每个管线的每个阶段都被量化。VAE 解码、辅助阶段以及多阶段系统的一部分可能保持更高精度。这就是为什么权重压缩比通常大于端到端延迟加速比。

### 5.2 用内存余量换取延迟降低

5.1 节确立了 W4A16 的一阶内存收益，而本案例研究展示这些内存余量如何转化为架构优势——启用能够带来真实吞吐增益的 GPU 分配策略，其增益超出了仅凭原始计算节省所能预测的范围。上述所有基准测试均在 Intel XPU B60 上进行。

#### W4A16 把最低硬件需求从 4 张 GPU 降到仅 1 张 GPU

BF16 的 FLUX.1-dev transformer（23 GB）一旦算上运行时激活值就超过了单张 B60 的 24.4 GB 容量——它需要 TP=4（全部四张 GPU）才能服务。W4A16 的 7 GB transformer 则可以轻松放进单张 GPU，还留有 19% 的余量。

#### W4A16 + CFG Parallel = 1.55x - 1.67x 的引导生成加速

无分类器引导（Classifier-Free Guidance, CFG）要求每步运行两次去噪——一次带提示，一次带负向提示。BF16 因张量并行占满全部 4 张 GPU，这两次去噪只能顺序执行（2 倍延迟）。W4A16 放进 TP=2 即可，释放出 2 张 GPU。这就启用了 CFG Parallel——在两个 GPU 组上同时运行两个引导分支：

![Figure 6: Latency and memory tradeoff analysis: W4A16 reduces minimum hardware requirement from 4 GPUs to 1, enabling CFG Parallel execution.](https://vllm.ai/blog-assets/figures/2026-06-02-vllm-omni-autoround/fig6_latency_memory_tradeoff.png)

图 6：延迟与内存的权衡分析：W4A16 把最低硬件需求从 4 张 GPU 降到 1 张，使 CFG Parallel 执行成为可能。

![Figure 7: CFG Parallel execution on Intel XPU B60 achieves 1.55-1.67x speedup over sequential BF16 serving.](https://vllm.ai/blog-assets/figures/2026-06-02-vllm-omni-autoround/fig7_cfg_parallel_latency.png)

图 7：在 Intel XPU B60 上，CFG Parallel 执行相比顺序 BF16 服务实现 1.55-1.67x 加速。

关键洞见：W4A16 在扩散工作负载中的价值超出了内存叙事。内存余量不只是让模型放得下——它让模型能以不同的方式运行，解锁了能产生超出原始反量化开销所能预测的端到端加速的并行策略。

## 6. 结论

AutoRound 与 vLLM-Omni 的契合异常之好，因为这次集成尊重运维人员真正需要的东西：离线检查点生成、自动运行时检测、可预期的内存节省，以及在上线前验证质量的路径。其结果是一套实用的低比特服务工作流，如今已覆盖 vLLM-Omni 生态中相当有意义的一部分：从 FLUX、Wan 到 GLM、BAGEL、Ovis 和 Qwen Omni。

对更广泛的社区来说，真正的要点是：量化不再只是赢得基准测试的聪明把戏——它已经成熟为基础基础设施。随着 AutoRound 在模型家族和硬件架构上拓宽兼容性，它为平衡多模态性能、部署成本和输出质量提供了一条有效路径。

进行中的工作包括更广泛的格式支持，以及在模型家族与硬件目标上的持续扩展。我们正在积极扩展对更多量化格式的支持，例如面向 Linear 与 MoE 模块的 **MXFP4** 和 **MXFP8**，同时也在探索注意力层的低比特技术（例如 SageAttention）。这些改进将在近期进一步扩展多模态服务的效率与灵活性。

## 7. 致谢

特别感谢 vLLM-Omni 团队的 Hongsheng Liu、Shunyang Li 和 WeiQing Chen，以及 Intel 的 Chendi Xue，感谢他们在把 AutoRound 集成进 vLLM-Omni 的过程中给予的巨大支持。我们也深深感谢 vLLM-Omni 社区对 AutoRound 的快速采用！
