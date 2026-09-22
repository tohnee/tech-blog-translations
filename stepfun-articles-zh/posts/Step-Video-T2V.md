---
title: "Step-Video-T2V：300 亿参数的文生视频预训练模型"
title_en: "stepfun-ai/Step-Video-T2V"
source: https://github.com/stepfun-ai/Step-Video-T2V/blob/main/README.md
crawled: 2026-09-22
translated: 2026-09-22
---

# Step-Video-T2V：300 亿参数的文生视频预训练模型

> 原文：[stepfun-ai/Step-Video-T2V](https://github.com/stepfun-ai/Step-Video-T2V/blob/main/README.md) · 阶跃星辰 StepFun

<p align="center">
  <img src="assets/logo.png"  height=100>
</p>
<div align="center">
  <a href="https://yuewen.cn/videos"><img src="https://img.shields.io/static/v1?label=Step-Video&message=Web&color=green"></a> &ensp;
  <a href="https://arxiv.org/abs/2502.10248"><img src="https://img.shields.io/static/v1?label=Tech Report&message=Arxiv&color=red"></a> &ensp;
  <a href="https://x.com/StepFun_ai"><img src="https://img.shields.io/static/v1?label=X.com&message=Web&color=blue"></a> &ensp;
</div>

<div align="center">
  <a href="https://huggingface.co/stepfun-ai/stepvideo-t2v"><img src="https://img.shields.io/static/v1?label=Step-Video-T2V&message=HuggingFace&color=yellow"></a> &ensp;
  <a href="https://huggingface.co/stepfun-ai/stepvideo-t2v-turbo"><img src="https://img.shields.io/static/v1?label=Step-Video-T2V-Turbo&message=HuggingFace&color=yellow"></a> &ensp;
</div>

## 🔥🔥🔥 新闻！
* 2025 年 3 月 17 日：👋 我们发布了 [Step-Video-TI2V](https://github.com/stepfun-ai/Step-Video-Ti2V)，一个基于 Step-Video-T2V 的图生视频模型。
* 2025 年 2 月 17 日：👋 我们发布了 Step-Video-T2V 的推理代码与模型权重。[下载](https://huggingface.co/stepfun-ai/stepvideo-t2v)
* 2025 年 2 月 17 日：👋 我们发布了 Step-Video-T2V-Turbo 的推理代码与模型权重。[下载](https://huggingface.co/stepfun-ai/stepvideo-t2v-turbo)
* 2025 年 2 月 17 日：🎉 我们开源了技术报告。[阅读](https://arxiv.org/abs/2502.10248)

## 视频演示

<table border="0" style="width: 100%; text-align: center; margin-top: 1px;">
  <tr>
    <td><video src="https://github.com/user-attachments/assets/9274b351-595d-41fb-aba3-f58e6e91603a" width="100%" controls autoplay loop muted></video></td>
    <td><video src="https://github.com/user-attachments/assets/2f6b3ad5-e93b-436b-98bc-4701182d8652" width="100%" controls autoplay loop muted></video></td>
    <td><video src="https://github.com/user-attachments/assets/67d20ee7-ad78-4b8f-80f6-3fdb00fb52d8" width="100%" controls autoplay loop muted></video></td>
  </tr>
  <tr>
    <td><video src="https://github.com/user-attachments/assets/9abce409-105d-4a8a-ad13-104a98cc8a0b" width="100%" controls autoplay loop muted></video></td>
    <td><video src="https://github.com/user-attachments/assets/8d1e1a47-048a-49ce-85f6-9d013f2d8e89" width="100%" controls autoplay loop muted></video></td>
    <td><video src="https://github.com/user-attachments/assets/32cf4bd1-ec1f-4f77-a488-cd0284aa81bb" width="100%" controls autoplay loop muted></video></td>
  </tr>
  <tr>
    <td><video src="https://github.com/user-attachments/assets/f95a7a49-032a-44ea-a10f-553d4e5d21c6" width="100%" controls autoplay loop muted></video></td>
    <td><video src="https://github.com/user-attachments/assets/3534072e-87d9-4128-a87f-28fcb5d951e0" width="100%" controls autoplay loop muted></video></td>
    <td><video src="https://github.com/user-attachments/assets/6d893dad-556d-4527-a882-666cba3d10e9" width="100%" controls autoplay loop muted></video></td>
  </tr>

</table>

## 目录

1. [简介](#1-简介)
2. [模型概览](#2-模型概览)
3. [模型下载](#3-模型下载)
4. [模型使用](#4-模型使用)
5. [基准测试](#5-基准测试)
6. [在线引擎](#6-在线引擎)
7. [引用](#7-引用)
8. [致谢](#8-致谢)

## 1. 简介
我们提出 **Step-Video-T2V**，一个拥有 300 亿参数的最先进（SoTA）文生视频预训练模型，可生成最长 204 帧的视频。为同时提升训练与推理效率，我们提出了一种面向视频的深度压缩 VAE，实现 16x16 空间与 8x 时间压缩比。在最后阶段应用直接偏好优化（DPO）以进一步提升生成视频的视觉质量。Step-Video-T2V 的性能在全新的视频生成基准 **Step-Video-T2V-Eval** 上评测，结果表明其文生视频质量相比开源与商用引擎均达到 SoTA。

## 2. 模型概览
在 Step-Video-T2V 中，视频由高压缩比 Video-VAE 表示，实现 16x16 空间与 8x 时间压缩比。用户提示词使用两个双语预训练文本编码器编码，以同时处理英文和中文。采用 3D 全注意力的 DiT 使用 Flow Matching 训练，用于将输入噪声去噪为潜空间帧，文本嵌入与时间步作为条件因子。为进一步提升生成视频的视觉质量，我们应用了面向视频的 DPO 方法，有效减少伪影，确保输出视频更平滑、更真实。

<p align="center">
  <img width="80%" src="assets/model_architecture.png">
</p>

### 2.1. Video-VAE
为视频生成任务设计了深度压缩变分自编码器（VideoVAE），在保持卓越视频重建质量的同时实现 16x16 空间与 8x 时间压缩比。这种压缩不仅加速了训练与推理，也契合扩散过程对紧凑表示的偏好。

<p align="center">
  <img width="70%" src="assets/dcvae.png">
</p>

### 2.2. 带 3D 全注意力的 DiT
Step-Video-T2V 基于 DiT 架构构建，共 48 层，每层包含 48 个注意力头，每个头的维度设为 128。使用 AdaLN-Single 引入时间步条件，并在自注意力机制中引入 QK-Norm 以确保训练稳定。此外，采用 3D RoPE，在处理不同视频长度与分辨率的序列时发挥关键作用。

<p align="center">
  <img width="80%" src="assets/dit.png">
</p>

### 2.3. Video-DPO
在 Step-Video-T2V 中，我们通过直接偏好优化（DPO）引入人类反馈，进一步提升生成视频的视觉质量。DPO 利用人类偏好数据微调模型，确保生成内容更贴近人类期望。整体 DPO 流水线如下图所示，凸显了其在提升视频生成过程一致性与质量方面的关键作用。

<p align="center">
  <img width="100%" src="assets/dpo_pipeline.png">
</p>



## 3. 模型下载
| 模型   | 🤗Huggingface    |  🤖Modelscope |
|:-------:|:-------:|:-------:|
| Step-Video-T2V | [下载](https://huggingface.co/stepfun-ai/stepvideo-t2v) | [下载](https://www.modelscope.cn/models/stepfun-ai/stepvideo-t2v)
| Step-Video-T2V-Turbo（推理步数蒸馏） | [下载](https://huggingface.co/stepfun-ai/stepvideo-t2v-turbo) | [下载](https://www.modelscope.cn/models/stepfun-ai/stepvideo-t2v-turbo)


## 4. 模型使用
### 📜 4.1  环境要求

下表展示了运行 Step-Video-T2V 模型（batch size = 1，不带 cfg 蒸馏）生成视频的要求：

|     模型    |  高/宽/帧 |  峰值 GPU 显存 | 50 步（带 flash-attn） | 50 步（不带 flash-attn） |
|:------------:|:------------:|:------------:|:------------:|:------------:|
| Step-Video-T2V   |        768px768px204f      |  78.55 GB | 860 s | 1437 s |
| Step-Video-T2V   |        544px992px204f      |  77.64 GB | 743 s | 1232 s |
| Step-Video-T2V   |        544px992px136f      |  72.48 GB | 408 s | 605 s |

* 需要 NVIDIA GPU 且支持 CUDA。
  * 模型已在四张 GPU 上测试。
  * **推荐**：我们推荐使用 80GB 显存的 GPU 以获得更好的生成质量。
* 已测试操作系统：Linux
* 文本编码器（step_llm）中的自注意力仅支持 CUDA 计算能力 sm_80、sm_86 与 sm_90

### 🔧 4.2 依赖与安装
- Python >= 3.10.0（推荐使用 [Anaconda](https://www.anaconda.com/download/#linux) 或 [Miniconda](https://docs.conda.io/en/latest/miniconda.html)）
- [PyTorch >= 2.3-cu121](https://pytorch.org/)
- [CUDA Toolkit](https://developer.nvidia.com/cuda-downloads)
- [FFmpeg](https://www.ffmpeg.org/)
```bash
git clone https://github.com/stepfun-ai/Step-Video-T2V.git
conda create -n stepvideo python=3.10
conda activate stepvideo

cd Step-Video-T2V
pip install -e .
pip install flash-attn --no-build-isolation  ## flash-attn is optional
```

###  🚀 4.3 推理脚本

#### 多 GPU 并行部署

- 我们对文本编码器、VAE 解码与 DiT 采用了解耦策略，以优化 DiT 对 GPU 资源的利用。因此，需要一张专用 GPU 来承载文本编码器嵌入与 VAE 解码的 API 服务。
```bash
python api/call_remote_server.py --model_dir where_you_download_dir &  ## We assume you have more than 4 GPUs available. This command will return the URL for both the caption API and the VAE API. Please use the returned URL in the following command.

parallel=4  # or parallel=8
url='127.0.0.1'
model_dir=where_you_download_dir

tp_degree=2
ulysses_degree=2

# make sure tp_degree x ulysses_degree = parallel
torchrun --nproc_per_node $parallel run_parallel.py --model_dir $model_dir --vae_url $url --caption_url $url  --ulysses_degree $ulysses_degree --tensor_parallel_degree $tp_degree --prompt "一名宇航员在月球上发现一块石碑，上面印有“stepfun”字样，闪闪发光" --infer_steps 50  --cfg_scale 9.0 --time_shift 13.0
```

#### 单 GPU 推理与量化

- ModelScope 的开源项目 DiffSynth-Studio 提供单 GPU 推理与量化支持，可显著降低所需显存。更多信息请参阅 [他们的示例](https://github.com/modelscope/DiffSynth-Studio/tree/main/examples/stepvideo)。

###  🚀 4.4 最佳实践推理设置
Step-Video-T2V 在推理设置上表现稳健，能持续生成高保真、动态的视频。但我们的实验表明，推理超参数的变化会显著影响视频保真度与动态性之间的权衡。为获得最佳效果，我们推荐按以下最佳实践调整推理参数：

| 模型   | infer_steps   | cfg_scale  | time_shift | num_frames |
|:-------:|:-------:|:-------:|:-------:|:-------:|
| Step-Video-T2V | 30-50 | 9.0 |  13.0 | 204
| Step-Video-T2V-Turbo（推理步数蒸馏） | 10-15 | 5.0 | 17.0 | 204 |

更多性能结果请参阅 xDiT 团队的 [基准指标](https://github.com/xdit-project/xDiT/blob/main/docs/performance/stepvideo.md)：

## 5. 基准测试
我们发布 [Step-Video-T2V Eval](https://github.com/stepfun-ai/Step-Video-T2V/blob/main/benchmark/Step-Video-T2V-Eval) 作为新基准，包含 128 条来自真实用户的中文提示词。该基准用于评估生成视频在 11 个类别上的质量：体育、美食、风景、动物、节日、组合概念、超现实、人物、3D 动画、电影摄影与风格。

## 6. 在线引擎
Step-Video-T2V 的在线版本可在 [跃问视频](https://yuewen.cn/videos) 使用，你还可以在那里探索一些令人惊艳的示例。

## 7. 引用
```
@misc{ma2025stepvideot2vtechnicalreportpractice,
      title={Step-Video-T2V Technical Report: The Practice, Challenges, and Future of Video Foundation Model}, 
      author={Guoqing Ma and Haoyang Huang and Kun Yan and Liangyu Chen and Nan Duan and Shengming Yin and Changyi Wan and Ranchen Ming and Xiaoniu Song and Xing Chen and Yu Zhou and Deshan Sun and Deyu Zhou and Jian Zhou and Kaijun Tan and Kang An and Mei Chen and Wei Ji and Qiling Wu and Wen Sun and Xin Han and Yanan Wei and Zheng Ge and Aojie Li and Bin Wang and Bizhu Huang and Bo Wang and Brian Li and Changxing Miao and Chen Xu and Chenfei Wu and Chenguang Yu and Dapeng Shi and Dingyuan Hu and Enle Liu and Gang Yu and Ge Yang and Guanzhe Huang and Gulin Yan and Haiyang Feng and Hao Nie and Haonan Jia and Hanpeng Hu and Hanqi Chen and Haolong Yan and Heng Wang and Hongcheng Guo and Huilin Xiong and Huixin Xiong and Jiahao Gong and Jianchang Wu and Jiaoren Wu and Jie Wu and Jie Yang and Jiashuai Liu and Jiashuo Li and Jingyang Zhang and Junjing Guo and Junzhe Lin and Kaixiang Li and Lei Liu and Lei Xia and Liang Zhao and Liguo Tan and Liwen Huang and Liying Shi and Ming Li and Mingliang Li and Muhua Cheng and Na Wang and Qiaohui Chen and Qinglin He and Qiuyan Liang and Quan Sun and Ran Sun and Rui Wang and Shaoliang Pang and Shiliang Yang and Sitong Liu and Siqi Liu and Shuli Gao and Tiancheng Cao and Tianyu Wang and Weipeng Ming and Wenqing He and Xu Zhao and Xuelin Zhang and Xianfang Zeng and Xiaojia Liu and Xuan Yang and Yaqi Dai and Yanbo Yu and Yang Li and Yineng Deng and Yingming Wang and Yilei Wang and Yuanwei Lu and Yu Chen and Yu Luo and Yuchu Luo and Yuhe Yin and Yuheng Feng and Yuxiang Yang and Zecheng Tang and Zekai Zhang and Zidong Yang and Binxing Jiao and Jiansheng Chen and Jing Li and Shuchang Zhou and Xiangyu Zhang and Xinhao Zhang and Yibo Zhu and Heung-Yeung Shum and Daxin Jiang},
      year={2025},
      eprint={2502.10248},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2502.10248}, 
}
```

## 8. 致谢
- 我们向 [xDiT](https://github.com/xdit-project/xDiT) 团队致以诚挚感谢，感谢他们宝贵的支持与并行化策略。
- 我们的代码将集成进 [Huggingface/Diffusers](https://github.com/huggingface/diffusers) 官方仓库。
- 我们感谢 [FastVideo](https://github.com/hao-ai-lab/FastVideo) 团队的持续合作，期待不久的将来共同推出推理加速方案。
