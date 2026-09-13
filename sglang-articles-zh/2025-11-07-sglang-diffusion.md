---
title: "SGLang Diffusion：加速视频与图像生成"
title_en: "SGLang Diffusion: Accelerating Video and Image Generation"
author: "The SGLang Diffusion Team"
date: "November 7, 2025"
previewImg: /images/blog/sgl-diffusion/sgl-diffusion-banner-16-9.png
source: https://lmsys.org/blog/2025-11-07-sglang-diffusion/
translated: 2026-09-12
---

# SGLang Diffusion：加速视频与图像生成

> 原文：[SGLang Diffusion: Accelerating Video and Image Generation](https://lmsys.org/blog/2025-11-07-sglang-diffusion/) · LMSYS Blog · The SGLang Diffusion Team

我们很高兴地推出 SGLang Diffusion，它将 SGLang 业界领先的性能带入扩散模型的图像与视频生成加速之中。SGLang Diffusion 支持主流开源视频与图像生成模型（Wan、Hunyuan、Qwen-Image、Qwen-Image-Edit、Flux），并通过多种 API 入口（OpenAI 兼容 API、CLI、Python 接口）提供快速的推理速度与良好的易用性。在多种负载下，SGLang Diffusion 可带来 1.2 倍至 5.9 倍的加速。
我们与 FastVideo 团队合作，为扩散模型提供从后训练到生产级推理服务的完整生态。代码见[此处](https://github.com/sgl-project/sglang/tree/main/python/sglang/multimodal_gen)，文档见[此处](https://docs.sglang.io/diffusion/index.html)。

<iframe
width="600"
height="371"
seamless
frameborder="0"
scrolling="no"
src="https://docs.google.com/spreadsheets/d/e/2PACX-1vT3u_F1P6TIUItyXdTctVV4pJVEcBuyPBTqmrdXR3KeQuiN1OdkIhjVNpZyHUDPw_5ZIKe88w2Xz6Dd/pubchart?oid=1360546403&format=interactive"
style="display:block; margin:15px auto 0 auto;">
</iframe>
<p style="color:gray; text-align: center;">SGL Diffusion 在 H100 GPU 上的性能基准测试</p>

<iframe
width="600"
height="371"
seamless
frameborder="0"
scrolling="no"
src="https://docs.google.com/spreadsheets/d/e/2PACX-1vT3u_F1P6TIUItyXdTctVV4pJVEcBuyPBTqmrdXR3KeQuiN1OdkIhjVNpZyHUDPw_5ZIKe88w2Xz6Dd/pubchart?oid=1860768236&format=interactive"
style="display:block; margin:15px auto 0 auto;">
</iframe>
<p style="color:gray; text-align: center;">SGLang Diffusion 在 H200 GPU 上的性能基准测试</p>

## 为什么要在 SGLang 中支持扩散模型？

随着扩散模型成为最先进图像与视频生成的骨干，我们听到社区发出了强烈的呼声：希望把 SGLang 标志性的性能与顺滑的用户体验带给这些新模态。SGLang Diffusion 正是为回应这一需求而生，为语言任务与扩散任务提供一个统一的高性能引擎。

这种统一思路至关重要，因为生成模型的未来在于架构的融合。
先锋模型已经在融合自回归（AR）与扩散两条路线的优势——从使用单一 transformer 同时承担两种任务的 ByteDance [Bagel](https://github.com/ByteDance-Seed/Bagel) 与 Meta [Transfusion](https://arxiv.org/abs/2408.11039)，到让 AR 模型实现并行生成的 NVIDIA [Fast-dLLM v2](https://nvlabs.github.io/Fast-dLLM/v2/)。

SGLang Diffusion 的设计目标就是成为一个面向未来的高性能解决方案，随时为这些创新系统提供支撑。

## 架构

SGLang Diffusion 兼顾性能与灵活性，构建于 SGLang 经过实战检验的推理服务架构之上。它继承了强大的 SGLang 调度器，并复用高度优化的 sgl-kernel 以获得极致效率。

在核心设计上，我们的架构能够容纳现代扩散模型多样化的结构。我们引入了 `ComposedPipelineBase`——一个灵活的抽象，负责编排一系列模块化的 `PipelineStage`。每个阶段封装一个常见的扩散功能——例如 `DenoisingStage` 中的去噪循环，或 `DecodingStage` 中的 VAE 解码——让开发者可以轻松组合与复用这些组件，构建复杂且定制化的 pipeline。

为达到最先进的速度，我们集成了先进的并行技术：针对核心 transformer 块，支持统一序列并行（Unified Sequence Parallelism, USP）——Ulysses-SP 与 Ring-Attention 的结合；同时为其他模型组件提供 CFG 并行与张量并行（TP）。

为加速开发并培育强大的生态，我们的系统构建于 **FastVideo** 的一个增强 fork 之上，并与他们的团队紧密合作。这一合作让 SGLang Diffusion 得以专注于提供最前沿的推理速度，而 **FastVideo** 则为模型蒸馏等训练相关任务提供全面支持。

## 模型支持

我们支持多款主流开源视频与图像生成模型，包括：
  - 视频模型：Wan 系列、FastWan、Hunyuan
  - 图像模型：Qwen-Image、Qwen-Image-Edit、Flux

支持模型的完整列表请参见[此处](https://docs.sglang.io/diffusion/compatibility_matrix.html)。

## 使用方法

为提供顺滑的使用体验，我们提供了一整套熟悉的接口，包括 CLI、Python 引擎 API 与 OpenAI 兼容 API，让用户以最小的成本将扩散生成集成到自己的工作流中。

### 安装

SGLang Diffusion 可通过多种方式安装：

```bash
# with pip or uv
uv pip install 'sglang[diffusion]' --prerelease=allow

# from source
git clone https://github.com/sgl-project/sglang.git
cd sglang
uv pip install -e "python[diffusion]" --prerelease=allow
```
### CLI

启动一个服务器，然后发送请求：
```bash
sglang serve --model-path black-forest-labs/FLUX.1-dev --port 3000

curl http://127.0.0.1:3000/v1/images/generations \
  -o >(jq -r '.data[0].b64_json' | base64 --decode > example.png) \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "black-forest-labs/FLUX.1-dev",
    "prompt": "A cute baby sea otter",
    "n": 1,
    "size": "1024x1024",
    "response_format": "b64_json"
  }'
```

或者，不启动服务器直接生成图像：
```bash
sglang generate --model-path black-forest-labs/FLUX.1-dev \
  --prompt "A Logo With Bold Large Text: SGL Diffusion" \
  --save-output
```

更多安装方式请参考[安装指南](https://docs.sglang.io/diffusion/installation.html)与 [CLI 指南](https://docs.sglang.io/diffusion/api/cli.html)。

### 示例

#### 文生视频：Wan-AI/Wan2.1

```bash
sglang generate --model-path Wan-AI/Wan2.1-T2V-1.3B-Diffusers \
    --prompt "A curious raccoon" \
    --save-output
```

<video width="800" controls poster="https://via.placeholder.com/800x450?text=Video+Preview" style="display:block; margin: auto; width: 80%;">
        <source src="https://github.com/lm-sys/lm-sys.github.io/releases/download/test/T2V.mp4" type="video/mp4">
        你的浏览器不支持 video 标签。
    </video>

备用链接：<a href="https://github.com/lm-sys/lm-sys.github.io/releases/download/test/T2V.mp4">下载视频</a>

#### 图生视频：Wan-AI/Wan2.1-I2V

```bash
sglang generate --model-path=Wan-AI/Wan2.1-I2V-14B-480P-Diffusers \
    --prompt="Summer beach vacation style, a white cat wearing sunglasses sits on a surfboard. The fluffy-furred feline gazes directly at the camera with a relaxed expression. Blurred beach scenery forms the background featuring crystal-clear waters, distant green hills, and a blue sky dotted with white clouds. The cat assumes a naturally relaxed posture, as if savoring the sea breeze and warm sunlight. A close-up shot highlights the feline's intricate details and the refreshing atmosphere of the seaside." \
    --image-path="https://github.com/Wan-Video/Wan2.2/blob/990af50de458c19590c245151197326e208d7191/examples/i2v_input.JPG?raw=true" \
    --num-gpus 2 --enable-cfg-parallel --save-output
```

<video width="800" controls poster="https://via.placeholder.com/800x450?text=Video+Preview" style="display:block; margin: auto; width: 80%;">  
        <source src="https://github.com/lm-sys/lm-sys.github.io/releases/download/test/TI2V.mp4" type="video/mp4">
        你的浏览器不支持 video 标签。
    </video>

备用链接：<a href="https://github.com/lm-sys/lm-sys.github.io/releases/download/test/TI2V.mp4">下载视频</a>

#### 文生图：FLUX

```bash
sglang generate --model-path black-forest-labs/FLUX.1-dev \
    --prompt "A Logo With Bold Large Text: SGL Diffusion" \
    --save-output
```


<img src="https://github.com/lm-sys/lm-sys.github.io/releases/download/test/T2I_FLUX.jpg" alt="Text to Image: FLUX" style="display:block; margin-top: 20px; width: 65%;">


#### 文生图：Qwen-Image

```bash
sglang generate --model-path=Qwen/Qwen-Image \
    --prompt='A curious raccoon' \
    --width=720 --height=720 --save-output
```

<img src="https://github.com/lm-sys/lm-sys.github.io/releases/download/test/T2I_Qwen_Image.jpg" alt="Text to Image: FLUX" style="display:block; margin-top: 20px; width: 65%;">


#### 图生图：Qwen-Image-Edit


```bash
sglang generate --model-path=Qwen/Qwen-Image-Edit \
    --prompt="Convert 2D style to 3D style" --image-path="https://github.com/lm-sys/lm-sys.github.io/releases/download/test/TI2I_Qwen_Image_Edit_Input.jpg" \
    --width=1536 --height=1024 --save-output
```


<div style="display: flex; justify-content: center; gap: 20px;">
  <div style="text-align: center;">
    <img src="https://github.com/lm-sys/lm-sys.github.io/releases/download/test/TI2I_Qwen_Image_Edit_Input.jpg" alt="Input" style="max-width: 100%; height: auto; border: 1px solid #ccc;">
    <div style="margin-top: -25px;">输入</div>
  </div>
  <div style="text-align: center;">
    <img src="https://github.com/lm-sys/lm-sys.github.io/releases/download/test/TI2I_Qwen_Image_Edit_Output.jpg" alt="Output" style="max-width: 100%; height: auto; border: 1px solid #ccc;">
    <div style="margin-top: -25px;">输出</div>
  </div>
</div>


## 性能基准测试

如本文开头的图表所示，我们对 SGLang Diffusion 的性能进行了对比：
  - 与流行的开源基线 Hugging Face Diffusers 对比。SGLang Diffusion 展现出最先进的性能，显著加速了图像与视频生成。
  - 在不同并行配置下。与单 GPU 配置相比，CFG-Parallel 与 USP 均带来显著的加速。


## 路线图与扩散生态

我们的愿景是与 **FastVideo** 团队携手构建一个完整的扩散生态，提供从模型训练到高性能推理的端到端解决方案。

SGLang Diffusion 团队将持续聚焦性能与模型支持上的不断创新：

- 模型支持与优化
  - 优化 Wan、FastWan、Hunyuan、Qwen-Image 系列、FLUX
  - 支持 LongCat-Video
- kernel 支持与融合
  - 量化 kernel
  - 旋转位置嵌入（RoPE）kernel
  - 在 sgl-kernel 中为 Blackwell 集成 Flash Attention 4
- 更多服务器特性
  - 生成文件的可配置云存储上传
  - 批处理支持
  - 更多并行方法
  - 量化
- 通用架构：
  - 降低支持新模型的成本
  - 增强缓存与注意力后端支持

构建这一生态是社区的共同事业，我们欢迎并鼓励各种形式的贡献。加入我们，共同塑造开源扩散生成的未来。


<img src="/images/blog/sgl-diffusion/diffusion_ecosystem.png" style="display:block; margin: auto; width: 85%;"></img>

## 致谢

SGLang Diffusion 团队：[Yuhao Yang](https://github.com/yhyang201)、[Xinyuan Tong](https://github.com/JustinTong0323)、[Yi Zhang](https://github.com/yizhang2077)、[Ke Bao](https://github.com/ispobock)、[Ji Li](https://github.com/GeLee-Q/GeLee-Q)、[Xi Chen](https://github.com/RubiaCx)、[Laixin Xie](https://github.com/laixinn)、[Yikai Zhu](https://github.com/zyksir)、[Mick](https://mickqian.github.io)

FastVideo 团队：[Peiyuan Zhang](https://github.com/jzhang38)、[William Lin](https://github.com/SolitaryThinker)、[Yongqi Chen](https://github.com/BrianChen1129)、[Kevin Lin](https://github.com/kevin314)、[Wenxuan Tan](https://github.com/Edenzzzz)、[Wei Zhou](https://github.com/JerryZhou54)、[Runlong Su](https://github.com/rlsu9)、[Jinzhe Pan](https://github.com/Eigensystem)、[Hangliang Ding](https://github.com/foreverpiano)、[Matthew Noto](https://github.com/RandNMR73)、[You Zhou](https://github.com/PorridgeSwim)、[Jiali Chen](https://github.com/Gary-ChenJL)、[Hao Zhang](https://haozhang.ai/)

特别感谢 NVIDIA 与 Voltage Park 提供的算力支持。

## 了解更多

- 路线图：[Diffusion (2025 Q4)](https://github.com/sgl-project/sglang/issues/12799)
- Slack 频道：[#diffusion](https://sgl-fru7574.slack.com/archives/C09P0HTKE6A)（通过 slack.sglang.io 加入）
