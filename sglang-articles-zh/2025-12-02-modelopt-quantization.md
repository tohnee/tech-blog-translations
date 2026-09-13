---
title: "提升 SGLang 推理性能：原生集成 NVIDIA Model Optimizer，实现无缝量化与部署"
title_en: "Boost SGLang Inference: Native NVIDIA Model Optimizer Integration for Seamless Quantization and Deployment"
author: "NVIDIA ModelOpt Team"
date: "Dec 02, 2025"
previewImg: /images/blog/nvidia-modelopt-quantization/Preview-modelopt-integration.png
source: https://lmsys.org/blog/2025-12-02-modelopt-quantization/
translated: 2026-09-12
---

# 提升 SGLang 推理性能：原生集成 NVIDIA Model Optimizer，实现无缝量化与部署

> 原文：[Boost SGLang Inference: Native NVIDIA Model Optimizer Integration for Seamless Quantization and Deployment](https://lmsys.org/blog/2025-12-02-modelopt-quantization/) · LMSYS Blog · NVIDIA ModelOpt Team

（12 月 2 日更新）

我们非常高兴地宣布 SGLang 迎来一项重要的新特性：原生支持 [NVIDIA Model Optimizer](https://github.com/NVIDIA/TensorRT-Model-Optimizer) 量化！这一集成简化了模型优化与部署的整个流程，让你可以在 SGLang 生态内完成从全精度模型到高性能量化端点的全过程。

在生产环境中高效地服务大语言模型是最大的挑战之一。模型量化是降低模型内存占用、提升推理速度的关键技术。在该特性推出之前，这一流程需要多步骤的工作流，且模型优化与部署要使用各自独立的工具。

通过我们最近的更新（PR [#7149](https://github.com/sgl-project/sglang/pull/7149)、[#9991](https://github.com/sgl-project/sglang/pull/9991) 和 [#10154](https://github.com/sgl-project/sglang/pull/10154)），我们消除了这种复杂性。

Model Optimizer 与 SGLang 带来的优化，可使 NVFP4 和 FP8 推理的单 GPU 吞吐量最高提升 2 倍。

### 新特性：SGLang 中的 ModelOpt 直接 API

SGLang 现在直接集成了 NVIDIA 的 Model Optimizer，你可以在 SGLang 代码中直接调用其强大的量化 API。

这一新能力带来了简洁的三步工作流：

1. **量化**：使用全新的 SGLang-ModelOpt 接口，应用最先进的量化技术，实现 NVFP4、MXFP4、FP8 等格式的低精度推理加速。

2. **导出**：保存优化后的模型产物，现在与 SGLang 运行时完全兼容。

3. **部署**：将量化后的模型直接加载到 SGLang 运行时，在 NVIDIA 平台上提供服务，即刻享受更低延迟和更少内存占用的收益。

#### 性能表现

通过这一新 API 优化后的模型能带来显著的性能提升。更棒的是，这些优化可以与 NVIDIA 软硬件栈中的其他软件组件叠加使用，并覆盖最新 Blackwell 架构的各类形态，从 DGX Spark 到 GB300 NVL72。

![DSR1-nvfp4-perf.jpg](/images/blog/nvidia-modelopt-quantization/DSR1-nvfp4-perf.jpg)

上图展示了使用 Model Optimizer NVFP4 量化模型的 DeepSeek-R1-0528 在多种配置下 NVIDIA B200 单 GPU 吞吐量与端到端延迟的关系，对比了原始 FP8 与 NVFP4。在本次初始 API 版本中，DeepSeek-R1-0528 尚未得到支持。

根据 [InferenceMAX 最新结果](https://lmsys.org/blog/2025-10-14-sa-inference-max/)的测量，Model Optimizer 与 SGLang 的优化相比原始 FP8 基线可带来最高 2 倍的单 GPU 吞吐量提升。这些性能收益即将通过本博客讨论的原生集成提供。

### 如何上手

SGLang 提供了一个[示例脚本](https://github.com/sgl-project/sglang/blob/main/examples/usage/modelopt_quantize_and_export.py)，演示了完整的 Model Optimizer 量化与导出工作流。你也可以参照下面的代码片段对模型运行量化和导出。请确保已在 SGLang 环境中安装 `nvidia-modelopt` 和 `accelerate`。

```
import sglang as sgl
from sglang.srt.configs.device_config import DeviceConfig
from sglang.srt.configs.load_config import LoadConfig
from sglang.srt.configs.model_config import ModelConfig
from sglang.srt.model_loader.loader import get_model_loader

# Configure model with ModelOpt quantization and export
model_config = ModelConfig(
	model_path="Qwen/Qwen3-8B",
	quantization="modelopt_fp8",  # or "modelopt_fp4"
	trust_remote_code=True,
)

load_config = LoadConfig(
	modelopt_export_path="./quantized_qwen3_8b_fp8",
	modelopt_checkpoint_save_path="./checkpoint.pth",  # optional, fake quantized checkpoint
)
device_config = DeviceConfig(device="cuda")

# Load and quantize the model (export happens automatically)
model_loader = get_model_loader(load_config, model_config)
quantized_model = model_loader.load_model(
	model_config=model_config,
	device_config=device_config,
)
```

量化和导出完成后，即可使用 SGLang 部署该模型：

```
# Deploy the exported quantized model
python -m sglang.launch_server \
   --model-path ./quantized_qwen3_8b_fp8 \
   --quantization modelopt \
   --port 30000 --host 0.0.0.0
```

或者使用 Python API：

```
import sglang as sgl
from transformers import AutoTokenizer

def main():
   # Deploy exported ModelOpt quantized model
   llm = sgl.Engine(
      model_path="./quantized_qwen3_8b_fp8",
      quantization="modelopt"
   )

   # Use chat template to format prompts for Qwen3-8B
   tokenizer = AutoTokenizer.from_pretrained("./quantized_qwen3_8b_fp8")

   messages = [
       [{"role": "user", "content": "Hello, how are you?"}],
       [{"role": "user", "content": "What is the capital of France?"}]
   ]

   prompts = [
       tokenizer.apply_chat_template(m, tokenize=False, add_generation_prompt=True)
       for m in messages
   ]

   # Run inference
   sampling_params = {"temperature": 0.8, "top_p": 0.95, "max_new_tokens": 512}
   outputs = llm.generate(prompts, sampling_params)

   for i, output in enumerate(outputs):
      print(f"Prompt: {prompts[i]}")
      print(f"Output: {output['text']}")

if __name__ == "__main__":
    main()
```

### 结语

这次的 Model Optimizer 原生集成进一步体现了 SGLang 致力于为 LLM 推理提供简单而强大平台的承诺。我们将继续缩小高性能模型优化与部署之间的差距。

我们迫不及待想看到你用这一新特性取得的性能提升。欢迎前往我们的 [GitHub 仓库](https://github.com/sgl-project/sglang)拉取最新版本并动手试试！

另外，欢迎加入我们专门的 Slack 频道 [#modelopt](https://sgl-fru7574.slack.com/archives/C09NPJSBR32)，一起讨论 modelopt、量化、低精度数值等相关话题！如果你还没有加入我们的 workspace，可以先[在这里](https://slack.sglang.io)加入。

### 致谢

NVIDIA 团队：Zhiyu Cheng、Jingyu Xin、Huizi Mao、Eduardo Alvarez、Pen Chung Li、Omri Almog

SGLang 团队与社区：Qiaolin Yu、Xinyuan Tong
