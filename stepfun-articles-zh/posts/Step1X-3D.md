---
title: "Step1X-3D：迈向高保真、可控的带纹理 3D 资产生成"
title_en: "stepfun-ai/Step1X-3D"
source: https://github.com/stepfun-ai/Step1X-3D/blob/main/README.md
crawled: 2026-09-22
translated: 2026-09-22
---

# Step1X-3D：迈向高保真、可控的带纹理 3D 资产生成

> 原文：[stepfun-ai/Step1X-3D](https://github.com/stepfun-ai/Step1X-3D/blob/main/README.md) · 阶跃星辰 StepFun

<p align="left">
        <a href="README_CN.md">中文</a> &nbsp｜ &nbsp English&nbsp&nbsp 
</p>


<h1 align="center"> Step1X-3D：迈向高保真、可控的带纹理 3D 资产生成</h1>

<div align="center">
  <a href=https://huggingface.co/spaces/stepfun-ai/Step1X-3D  target="_blank"><img src=https://img.shields.io/static/v1?label=Online%20Demo&message=HuggingFace&color=yellow></a>
  <a href=https://huggingface.co/stepfun-ai/Step1X-3D target="_blank"><img src=https://img.shields.io/static/v1?label=Model&message=HuggingFace&color=yellow></a>
  <a href=https://arxiv.org/abs/2505.07747 target="_blank"><img src=https://img.shields.io/static/v1?label=Tech%20Report&message=Arxiv&color=red></a>
  <a href=https://stepfun-ai.github.io/Step1X-3D/ target="_blank"><img src= https://img.shields.io/static/v1?label=Project%20Page&message=Web&color=green></a>
</div>

<p align="center">
  <img src="assets/stepfun_illusions_logo.jpeg" width="100%">
</p>

<div align="center">
  <img src="./assets/step1x-3d-teaser.png" width="100%">
</div>

<div align="left">
<p><b>Step1X-3D 展示了生成具有高保真几何与多样纹理贴图的 3D 资产的能力，同时在表面几何与纹理映射之间保持出色的对齐。从左到右，我们依次展示：基础几何（无纹理），随后是卡通风格、素描风格与照片级写实风格的 3D 资产生成结果。</b></p>
</div>

## 🔥🔥🔥 最新消息！
* 2025 年 6 月 26 日：👋 我们发布了形状 VAE 与扩散模型的数据预处理代码，包括 [CraftsMan3D](https://github.com/wyysf-98/CraftsMan3D) 提出的、基于 depth_test 与 winding_number 的先进水密化方法，位于 "Step1X-3D/data/watertight_and_sampling.py"！
* 2025 年 6 月 9 日：👋 我们发布了用于纹理生成模型训练的多视角渲染代码，位于 "Step1X-3D/data/ig2mv/render"！
* 2025 年 5 月 27 日：👋 我们发布了带纹理同步模块的多视角生成模型！
* 2025 年 5 月 13 日：👋 Step1X-3D 在线演示已在 HuggingFace 上线——尽情享受生成的 3D 资产吧！[Huggingface 在线演示](https://huggingface.co/spaces/stepfun-ai/Step1X-3D)
* 2025 年 5 月 13 日：👋 我们还发布了经严格数据治理流水线筛选得到的 80 万（800K）条高质量 3D 资产 uid（不含自采资产），可用于 3D 几何与合成的训练。[Huggingface 数据集](https://huggingface.co/datasets/stepfun-ai/Step1X-3D-obj-data/tree/main)
* 2025 年 5 月 13 日：👋 我们还发布了 Step1X-3D 几何生成与纹理合成的训练代码。
* 2025 年 5 月 13 日：👋 我们发布了 Step1X-3D 几何与 Step1X-3D 纹理的推理代码与模型权重。
* 2025 年 5 月 13 日：👋 我们开源了 Step1X-3D [技术报告](https://arxiv.org/abs/2505.07747)。

<!-- ## Image Edit Demos -->



## 📑 开源计划
- [x] 技术报告
- [x] 推理代码与模型权重
- [x] 训练代码
- [x] 高质量 3D 资产 uid
- [x] 在线演示（部署在 HuggingFace 的 gradio）
- [x] 网格预处理（包括基于 depth_test 与 winding_number 的水密化、采样）
- [ ] 更多可控模型，例如以多视角、边界框和骨架为条件
- [ ] ComfyUI

## 1. 简介
尽管生成式人工智能在文本、图像、音频和视频领域已取得显著进展，但由于数据稀缺、算法局限与生态碎片化等根本性挑战，3D 生成仍相对落后。
为此，我们提出 Step1X-3D，一个通过以下方式应对这些挑战的开放框架：
(1) 严格的治理流水线，处理超过 500 万（>5M）资产，构建出具有标准化几何与纹理属性的 200 万（2M）高质量数据集；
(2) 两阶段的 3D 原生架构，将混合 VAE-DiT 几何生成器与基于 SD-XL 的纹理合成模块相结合；以及 (3) 模型、训练代码与适配模块的完整开源发布。在几何生成方面，混合 VAE-DiT 组件通过采用基于 Perceiver 的潜空间编码与锐利边缘采样以保留细节，产出水密的 TSDF 表示。基于 SD-XL 的纹理合成模块则通过几何条件与潜空间同步确保跨视角一致性。
基准测试结果表明其性能超过现有开源方法、达到最先进水平，同时与专有方案相比也具备有竞争力的质量。
值得注意的是，该框架独特地打通了 2D 与 3D 生成范式，支持将 2D 控制技术（如 LoRA）直接迁移到 3D 合成。
通过同时推进数据质量、算法保真度与可复现性，Step1X-3D 旨在为可控 3D 资产生成的开放研究树立新标准。
<img width="" alt="framework" src="assets/step1x-3d-framework-overall.jpg">

## 2. 模型下载
| 模型                       | 下载链接                   | 大小       | 更新日期 |                                                                                     
|-----------------------------|-------------------------------|------------|------|
| Step1X-3D-geometry| 🤗 [Huggingface](https://huggingface.co/stepfun-ai/Step1X-3D/tree/main/Step1X-3D-Geometry-1300m)    | 1.3B | 2025-05-13  | 
| Step1X-3D-geometry-label  | 🤗 [Huggingface](https://huggingface.co/stepfun-ai/Step1X-3D/tree/main/Step1X-3D-Geometry-Label-1300m) | 1.3B | 2025-05-13|
| Step1X-3D Texture       | 🤗 [Huggingface](https://huggingface.co/stepfun-ai/Step1X-3D/tree/main/Step1X-3D-Texture)    | 3.5B |2025-05-13|
|ModelScope 上的模型 |🤖 [ModelScope](https://www.modelscope.cn/models/stepfun-ai/Step1X-3D) | 6.1B | 2025-05-14|
## 3. 开放的高质量筛选数据集
| 数据源                       | 下载链接                   | 大小       | 更新日期 |                                                                                    
|-----------------------------|-------------------------------|------------|------|
| Objaverse| 🤗[Huggingface](https://huggingface.co/datasets/stepfun-ai/Step1X-3D-obj-data/blob/main/objaverse_320k.json)    | 320K |2025-05-13|
| Objaverse-XL  | 🤗[Huggingface](https://huggingface.co/datasets/stepfun-ai/Step1X-3D-obj-data/blob/main/objaverse_xl_github_url_480k.json) | 480K |2025-05-13|
| 用于纹理合成的资产 | 🤗[Huggingface](https://huggingface.co/datasets/stepfun-ai/Step1X-3D-obj-data/blob/main/objaverse_texture_30k.json) | 30K |2025-05-13|
| ModelScope 上的资产| 🤖[ModelScope](https://www.modelscope.cn/datasets/stepfun-ai/Step1X-3D-obj-data) | 830K |2025-05-14|

有了上述高质量 3D 资产，你可以参照 [Dora](https://github.com/Seed3D/Dora/tree/main) 的方法为 VAE 与 3D DiT 训练预处理数据，参照 [MV-Adapter](https://github.com/huanngzh/MV-Adapter) 为 ig2mv 训练预处理数据。
## 4. 依赖与安装
按照以下说明配置的依赖可提供兼具训练与推理能力的环境

### 4.1 克隆仓库
```bash
git clone --depth 1 --branch main https://github.com/stepfun-ai/Step1X-3D.git
cd Step1X-3D
```

> 浅克隆更快，且无需拉取 gh-pages 分支。
>
> 使用 `git fetch --unshallow` 命令可将浅克隆转换为完整克隆。
>
> 使用 `git config remote.origin.fetch '+refs/heads/*:refs/remotes/origin/*'` 命令可拉取所有分支。
### 4.2 创建新的 conda 环境
```bash
conda create -n step1x-3d python=3.10
conda activate step1x-3d
```
### 4.3 安装依赖
我们已在 cuda12.4 环境下检查过，你可以按照 [CUDA Toolkit 安装指南](https://developer.nvidia.com/cuda-12-4-0-download-archive) 安装 cuda12.4。

```bash
pip install torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu124
pip install -r requirements.txt
pip install torch-cluster -f https://data.pyg.org/whl/torch-2.5.1+cu124.html
pip install "git+https://github.com/facebookresearch/pytorch3d.git@stable"
pip install kaolin==0.17.0 -f https://nvidia-kaolin.s3.us-east-2.amazonaws.com/torch-2.5.1_cu124.html

cd step1x3d_texture/custom_rasterizer
python setup.py install
cd ../differentiable_renderer
python setup.py install
cd ../../
```
我们在纹理烘焙器中复用了 [Hunyuan3D 2.0](https://github.com/Tencent/Hunyuan3D-2) 的 custom_rasterizer 与 differentiable_renderer 工具，感谢他们的开源贡献。

## 5. 推理脚本

|                                                  | GPU 显存占用 | 50 步耗时 |
| ------------------------------------------------ | ---------------- | ----------------- |
| Step1X-3D-Geometry-1300m+Step1X-3D-Texture       | 27G              | 152 seconds       |
| Step1X-3D-Geometry-Label-1300m+Step1X-3D-Texture | 29G              | 152 seconds       |

我们提供以下示例代码作为教程，按顺序生成几何与纹理。
```python
import torch
# Stage 1: 3D geometry generation
from step1x3d_geometry.models.pipelines.pipeline import Step1X3DGeometryPipeline

# define the pipeline
geometry_pipeline = Step1X3DGeometryPipeline.from_pretrained("stepfun-ai/Step1X-3D", subfolder='Step1X-3D-Geometry-1300m'
).to("cuda")

# input image
input_image_path = "examples/images/000.png"

# run pipeline and obtain the untextured mesh 
generator = torch.Generator(device=geometry_pipeline.device).manual_seed(2025)
out = geometry_pipeline(input_image_path, guidance_scale=7.5, num_inference_steps=50)

# export untextured mesh as .glb format
out.mesh[0].export("untexture_mesh.glb")


# Stage 2: 3D texure synthsis
from step1x3d_texture.pipelines.step1x_3d_texture_synthesis_pipeline import (
    Step1X3DTexturePipeline,
)
from step1x3d_geometry.models.pipelines.pipeline_utils import reduce_face, remove_degenerate_face
import trimesh

# load untextured mesh
untexture_mesh = trimesh.load("untexture_mesh.glb")

# define texture_pipeline
texture_pipeline = Step1X3DTexturePipeline.from_pretrained("stepfun-ai/Step1X-3D", subfolder="Step1X-3D-Texture")

# reduce face
untexture_mesh = remove_degenerate_face(untexture_mesh)
untexture_mesh = reduce_face(untexture_mesh)

# texture mapping
textured_mesh = texture_pipeline(input_image_path, untexture_mesh)

# export textured mesh as .glb format
textured_mesh.export("textured_mesh.glb")
```

你也可以运行以下命令执行完整流程
```bash
python inference.py
```

我们还提供基于 gradio 的本地部署交互式生成
```bash
python app.py
```
 或 [Huggingface 在线演示](https://huggingface.co/spaces/stepfun-ai/Step1X-3D)

## 6. 训练脚本
你可以选择一个配置文件进行训练，并修改脚本以支持多 GPU 训练或更多训练设置。
### 6.1 训练变分自编码器
```bash
# example of VAE config in path: Step1X-3D/configs/train-geometry-autoencoder
CUDA_VISIBLE_DEVICES=0 python train.py --config $config --train --gpu 0
```

### 6.2 从零训练 3D 原生扩散模型

```bash
# example of 3D diffusion config in path: Step1X-3D/configs/train-geometry-diffusiontrain-geometry-autoencoder
CUDA_VISIBLE_DEVICES=0 python train.py --config $config --train --gpu 0
```
### 6.3 使用 LoRA 微调训练 3D 原生扩散模型

```bash
CUDA_VISIBLE_DEVICES=0 python train.py --config $config --train --gpu 0 system.use_lora=True
```
### 6.4 训练基于 SD-XL 的多视角生成

```bash
# example of 3D ig2mv config in Path: Step1X-3D/configs/
train-texture-ig2mv
# We adopt most training code for multi-view generation from MV-Adapter and thank for the nice work.
CUDA_VISIBLE_DEVICES=0 python train_ig2mv.py --config configs/train-texture-ig2mv/step1x3d_ig2mv_sdxl.yaml --train
```

## 7. 致谢
我们感谢以下项目：[FLUX](https://github.com/black-forest-labs/flux)、[DINOv2](https://github.com/facebookresearch/dinov2)、[MV-Adapter](https://github.com/huanngzh/MV-Adapter)、[CLAY](https://arxiv.org/abs/2406.13897)、[Michelango](https://github.com/NeuralCarver/Michelangelo)、[CraftsMan3D](https://github.com/wyysf-98/CraftsMan3D)、[TripoSG](https://github.com/VAST-AI-Research/TripoSG)、[Dora](https://github.com/Seed3D/Dora)、[Hunyuan3D 2.0](https://github.com/Tencent/Hunyuan3D-2)、[FlashVDM](https://github.com/Tencent/FlashVDM)
、[diffusers](https://github.com/huggingface/diffusers) 与 [HuggingFace](https://huggingface.co) 的开放探索与贡献。具体到纹理生成，我们采用了 [MV-Adapter](https://github.com/huanngzh/MV-Adapter) 的部分代码用于多视角生成、[bpy-render](https://github.com/huanngzh/bpy-rendere) 的部分代码用于多视角渲染、[Hunyuan 3D 2.0](https://github.com/Tencent-Hunyuan/Hunyuan3D-2) 的部分代码用于纹理烘焙器。

## 8. 许可证
Step1X-3D 基于 Apache License 2.0 授权。你可以在相应的 GitHub 与 HuggingFace 仓库中找到许可证文件。
## 9. 引用
如果你觉得我们的工作有帮助，请引用我们
```
@article{li2025step1x,
  title={Step1X-3D: Towards High-Fidelity and Controllable Generation of Textured 3D Assets},
  author={Li, Weiyu and Zhang, Xuanyang and Sun, Zheng and Qi, Di and Li, Hao and Cheng, Wei and Cai, Weiwei and Wu, Shihao and Liu, Jiarui and Wang, Zihao and others},
  journal={arXiv preprint arXiv:2505.07747},
  year={2025}
}
```
