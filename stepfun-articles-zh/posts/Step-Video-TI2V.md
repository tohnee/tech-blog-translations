---
title: "Step-Video-TI2V：文本驱动的图生视频模型"
title_en: "stepfun-ai/Step-Video-TI2V"
source: https://github.com/stepfun-ai/Step-Video-TI2V/blob/main/README.md
crawled: 2026-09-22
translated: 2026-09-22
---

# Step-Video-TI2V：文本驱动的图生视频模型

> 原文：[stepfun-ai/Step-Video-TI2V](https://github.com/stepfun-ai/Step-Video-TI2V/blob/main/README.md) · 阶跃星辰 StepFun

<p align="center">
  <img src="assets/logo.png"  height=100>
</p>
<div align="center">
  <a href="https://yuewen.cn/videos"><img src="https://img.shields.io/static/v1?label=Step-Video&message=Web&color=green"></a> &ensp;
  <a href="https://arxiv.org/abs/2503.11251"><img src="https://img.shields.io/static/v1?label=Tech Report&message=Arxiv&color=red"></a> &ensp;
  <a href="https://x.com/StepFun_ai"><img src="https://img.shields.io/static/v1?label=X.com&message=Web&color=blue"></a> &ensp;
</div>

<div align="center">
  <a href="https://huggingface.co/stepfun-ai/stepvideo-ti2v"><img src="https://img.shields.io/static/v1?label=Step-Video-TI2V&message=HuggingFace&color=yellow"></a> &ensp;
</div>

## 🔥🔥🔥 新闻！
* 2025 年 3 月 17 日：👋 我们发布了 Step-Video-TI2V 的推理代码与模型权重。[下载](https://huggingface.co/stepfun-ai/stepvideo-ti2v)
* 2025 年 3 月 17 日：👋 我们发布了新的 TI2V 基准 [Step-Video-TI2V-Eval](https://github.com/stepfun-ai/Step-Video-TI2V/tree/main/benchmark/Step-Video-TI2V-Eval)
* 2025 年 3 月 17 日：👋 Step-Video-TI2V 已集成进 [ComfyUI-Stepvideo-ti2v](https://github.com/stepfun-ai/ComfyUI-StepVideo)。尽情体验吧！
* 2025 年 3 月 17 日：🎉 我们开源了技术报告。[阅读](https://arxiv.org/abs/2503.11251)





## 运动控制

<table border="0" style="width: 100%; text-align: center; margin-top: 1px;">
  <tr>
    <th style="width: 33%;">战马跳跃</th>
    <th style="width: 33%;">战马蹲下</th>
    <th style="width: 33%;">战马向前奔跑，然后转身</th>
  </tr>
  <tr>
    <td><video src="https://github.com/user-attachments/assets/e664f45c-b8cd-4f89-9858-eaaef54aa0f6" width="30%" controls autoplay loop muted></video></td>
    <td><video src="https://github.com/user-attachments/assets/eb2d09b0-cc37-4f27-85c7-a31b6840fa69" width="30%" controls autoplay loop muted></video></td>
    <td><video src="https://github.com/user-attachments/assets/d17eba41-82f6-4ee2-8a99-3f21af112af0" width="30%" controls autoplay loop muted></video></td>
  </tr>
</table>

## 运动动态强度控制


<table border="0" style="width: 100%; text-align: center; margin-top: 10px;">
  <tr>
    <th style="width: 33%;">两名男子在互相拳击，镜头环绕两人拍摄。(motion_score: 2)</th>
    <th style="width: 33%;">两名男子在互相拳击，镜头环绕两人拍摄。(motion_score: 5)</th>
    <th style="width: 33%;">两名男子在互相拳击，镜头环绕两人拍摄。(motion_score: 20)</th>
  </tr>
  <tr>
    <td><video src="https://github.com/user-attachments/assets/31c48385-fe83-4961-bd42-7bd2b1edeb19" width="33%" controls autoplay loop muted></video></td>
    <td><video src="https://github.com/user-attachments/assets/913a407e-55ca-4a33-bafe-bd5e38eec5f5" width="33%" controls autoplay loop muted></video></td>
    <td><video src="https://github.com/user-attachments/assets/119a3673-014f-4772-b846-718307a4a412" width="33%" controls autoplay loop muted></video></td>
  </tr>
</table>

🎯 小贴士：
默认的 motion_score = 5 适合一般用途。如果需要更高的稳定性，可以将 motion_score 设为 2，不过某些动作可能缺乏动感。若想要更大的运动幅度，可以使用 motion_score = 10 或 motion_score = 20 来实现更激烈的动作。你可以根据创作需求自由定制 motion_score，以适配不同场景。

## 镜头控制

<table border="0" style="width: 100%; text-align: center; margin-top: 1px;">
  <tr>
    <th style="width: 33%;">镜头环绕女孩，女孩在跳舞</th>
    <th style="width: 33%;">镜头缓慢推进，女孩在跳舞</th>
    <th style="width: 33%;">镜头拉远，女孩在跳舞</th>
  </tr>
  <tr>
    <td><video src="https://github.com/user-attachments/assets/257847bc-5967-45ba-a649-505859476aad" height="30%" controls autoplay loop muted></video></td>
    <td><video src="https://github.com/user-attachments/assets/d310502a-4f7e-4a78-882f-95c46b4dfe67" height="30%" controls autoplay loop muted></video></td>
    <td><video src="https://github.com/user-attachments/assets/f6426fc7-2a18-474c-9766-fc8ae8d8d40d" height="30%" controls autoplay loop muted></video></td>
  </tr>
</table>


### 支持的运镜方式

| 运镜方式           |
|--------------------------------|
| **固定镜头（Fixed Camera）**               |
| **镜头上/下/左/右移（Pan Up/Down/Left/Right）**     |
| **镜头上/下/左/右摇（Tilt Up/Down/Left/Right）**    |
| **镜头放大/缩小（Zoom In/Out）**                |
| **镜头推进/拉远（Dolly In/Out）**               |
| **镜头旋转（Camera Rotation）**            |
| **镜头跟随（Tracking Shot）**  |
| **镜头环绕（Orbit Shot）** |
| **焦点转移（Rack Focus）**  |


🔧 motion_score 取值建议：
motion_score = 5 或 10 比 motion_score = 2 带来更平滑、更准确的运动，其中 motion_score = 10 提供最佳的反应灵敏度和镜头跟踪。选择合适的设置可以提升运动精度与流畅度。

## 动漫风格生成

<table border="0" style="width: 100%; text-align: center; margin-top: 1px;">
  <tr>
    <th style="width: 33%;">女生向前行走，背景是虚化模糊的效果</th>
    <th style="width: 33%;">女人眨眼，然后对着镜头做飞吻的动作。</th>
    <th style="width: 10%;">狸猫战士双手缓缓上扬，雷电从手中向四周扩散，<br>身后灵兽影像的双眼闪烁强光，</br>张开巨口发出低吼</th>
  </tr>
  <tr>
    <td><video src="https://github.com/user-attachments/assets/80be13a1-ea65-45c5-b7f4-c2488acbf2a3" height="33%" controls autoplay loop muted></video></td>
    <td><video src="https://github.com/user-attachments/assets/67038b85-19d4-4313-b386-f578b75dcad7" height="33%" controls autoplay loop muted></video></td>
    <td><video src="https://github.com/user-attachments/assets/73ffd269-a5c8-4255-8809-161501273bfd" height="33%" controls autoplay loop muted></video></td>
  </tr>

</table>
Step-Video-TI2V 擅长动漫风格生成，让你可以探索各种动漫风格的图像，并创作符合个人偏好的定制视频。

## 目录

1. [简介](#1-简介)
2. [模型概览](#2-模型概览)
3. [模型下载](#3-模型下载)
4. [模型使用](#4-模型使用)
5. [对比](#5-对比)
6. [在线引擎](#6-在线引擎)
7. [引用](#7-引用)



## 1. 简介
我们提出 Step-Video-TI2V，一个拥有 30B 参数的最先进文本驱动图生视频模型，能够基于文本与图像输入生成最长 102 帧的视频。我们构建了 Step-Video-TI2V-Eval 作为文本驱动图生视频任务的新基准，并使用该数据集将 Step-Video-TI2V 与开源及商用 TI2V 引擎进行对比。实验结果表明，Step-Video-TI2V 在图生视频任务上达到了最先进的性能。

## 2. 模型概览
Step-Video-TI2V 基于 Step-Video-T2V 训练。为了将图像条件作为生成视频的首帧，我们使用 Step-Video-T2V 的 Video-VAE 将其编码为潜空间表示，并沿视频潜空间的通道维度拼接。此外，我们引入了运动分数（motion score）条件，让用户能够控制从图像条件生成视频的动态程度。

<p align="center">
  <img width="80%" src="assets/model.png">
</p>

## 3. 模型下载
| 模型              | 🤗 Huggingface  | 🤖 Modelscope  | 🎛️ ComfyUI  |
|:------------------:|:--------------:|:-------------:|:-----------------:|
| Step-Video-TI2V   | [下载](https://huggingface.co/stepfun-ai/stepvideo-ti2v)  | [下载](https://modelscope.cn/models/stepfun-ai/stepvideo-ti2v) | [链接](https://github.com/stepfun-ai/ComfyUI-StepVideo) |



## 4. 模型使用

### 📜 4.1  依赖与安装

```bash
git clone https://github.com/stepfun-ai/Step-Video-TI2V.git
conda create -n stepvideo python=3.10
conda activate stepvideo

cd Step-Video-TI2V
pip install -e .
```

###  🚀 4.2. 推理脚本
```bash
python api/call_remote_server.py --model_dir where_you_download_dir &  ## We assume you have more than 4 GPUs available. This command will return the URL for both the caption API and the VAE API. Please use the returned URL in the following command.

parallel=1 or 4  # or parallel=8 Single GPU can also predict the results, although it will take longer
url='127.0.0.1'
model_dir=where_you_download_dir

torchrun --nproc_per_node $parallel run_parallel.py --model_dir $model_dir --vae_url $url --caption_url $url  --ulysses_degree  $parallel --prompt "笑起来" --first_image_path ./assets/demo.png --infer_steps 50  --cfg_scale 9.0 --time_shift 13.0 --motion_score 5.0
```

我们还列出了一些便于使用的实用配置：

|        参数        |  默认值  |                描述                |
|:----------------------:|:---------:|:-----------------------------------------:|
|       `--model_dir`       |   None    |   用于视频生成的模型检查点    |
|     `--prompt`     | “笑起来”  |      I2V 生成的文本提示词      |
|    `first_image_path`    |    ./assets/demo.png    |     I2V 任务的参考图像路径。     |
|    `--infer_steps`     |    50     |     采样步数      |
| `--cfg_scale` |    9.0    |    嵌入式无分类器引导（classifier-free guidance）尺度       |
|     `--time_shift`     |    7.0    | Flow Matching 调度器的偏移因子。 |
|     `--motion_score`   |    5.0  | 控制视频运动强度的分数。 |
|        `--seed`        |     None  |   生成视频的随机种子，若为 None，则初始化一个随机种子    |
|  `--use-cpu-offload`   |   False   |    模型加载时使用 CPU offload 以节省更多显存，对高分辨率视频生成是必需的    |
|     `--save-path`      | ./results |     生成视频的保存路径      |



## 5. 对比

为评估 Step-Video-TI2V 的性能，我们利用 [VBench-I2V](https://arxiv.org/html/2411.13503v1) 将 Step-Video-TI2V 与近期发布的主流开源模型进行系统对比。下表展示的详细结果凸显了我们模型相对于这些模型的优越性能。我们给出了 Step-Video-TI2V 的两组结果，运动分数分别设为 5 和 10。正如预期，该机制在生成视频的运动动态与稳定性（或一致性）之间实现了有效平衡。此外，我们将结果提交至 [VBench-I2V 排行榜](https://huggingface.co/spaces/Vchitect/VBench_Leaderboard)，Step-Video-TI2V 取得了榜首位置。
我们还引入了新基准数据集 [Step-Video-TI2V-Eval](https://github.com/stepfun-ai/Step-Video-TI2V/tree/main/benchmark/Step-Video-TI2V-Eval)，专为 TI2V 任务设计，以支持未来的研究与评测。该数据集包含 178 组真实世界与 120 组动漫风格的提示词-图像对，确保对多样用户场景的广泛覆盖。


<table border="0" style="width: 100%; text-align: center; margin-top: 1px;">
  <tr>
    <th style="width: 20%;">分数</th>
    <th style="width: 20%;">Step-Video-TI2V (motion=10)</th>
    <th style="width: 20%;">Step-Video-TI2V (motion=5)</th>
    <th style="width: 20%;">OSTopA</th>
    <th style="width: 20%;">OSTopB</th>
  </tr>
  <tr>
    <td><strong>总分（Total Score）</strong></td>
    <td style="background-color: lightgreen;"><strong>87.98</strong></td>
    <td>87.80</td>
    <td>87.49</td>
    <td>86.77</td>
  </tr>
  <tr>
    <td><strong>I2V 分数（I2V Score）</strong></td>
    <td>95.11</td>
    <td style="background-color: lightgreen;"><strong>95.50</strong></td>
    <td>94.63</td>
    <td>93.25</td>
  </tr>
  <tr>
    <td>视频-文本镜头运动（Video-Text Camera Motion）</td>
    <td>48.15</td>
    <td style="background-color: lightgreen;"><strong>49.22</strong></td>
    <td>29.58</td>
    <td>46.45</td>
  </tr>
  <tr>
    <td>视频-图像主体一致性（Video-Image Subject Consistency）</td>
    <td>97.44</td>
    <td style="background-color: lightgreen;"><strong>97.85</strong></td>
    <td>97.73</td>
    <td>95.88</td>
  </tr>
  <tr>
    <td>视频-图像背景一致性（Video-Image Background Consistency）</td>
    <td>98.45</td>
    <td>98.63</td>
    <td style="background-color: lightgreen;"><strong>98.83</strong></td>
    <td>96.47</td>
  </tr>
  <tr>
    <td><strong>质量分数（Quality Score）</strong></td>
    <td style="background-color: lightgreen;"><strong>80.86</strong></td>
    <td>80.11</td>
    <td>80.36</td>
    <td>80.28</td>
  </tr>
  <tr>
    <td>主体一致性（Subject Consistency）</td>
    <td>95.62</td>
    <td style="background-color: lightgreen;"><strong>96.02</strong></td>
    <td>94.52</td>
    <td style="background-color: lightgreen;"><strong>96.28</strong></td>
  </tr>
  <tr>
    <td>背景一致性（Background Consistency）</td>
    <td>96.92</td>
    <td>97.06</td>
    <td>96.47</td>
    <td style="background-color: lightgreen;"><strong>97.38</strong></td>
  </tr>
  <tr>
    <td>运动平滑度（Motion Smoothness）</td>
    <td>99.08</td>
    <td style="background-color: lightgreen;"><strong>99.24</strong></td>
    <td>98.09</td>
    <td>99.10</td>
  </tr>
  <tr>
    <td>动态程度（Dynamic Degree）</td>
    <td>48.78</td>
    <td>36.58</td>
    <td style="background-color: lightgreen;"><strong>53.41</strong></td>
    <td>38.13</td>
  </tr>
  <tr>
    <td>美学质量（Aesthetic Quality）</td>
    <td>61.74</td>
    <td style="background-color: lightgreen;"><strong>62.29</strong></td>
    <td>61.04</td>
    <td>61.82</td>
  </tr>
  <tr>
    <td>成像质量（Imaging Quality）</td>
    <td>70.17</td>
    <td>70.43</td>
    <td style="background-color: lightgreen;"><strong>71.12</strong></td>
    <td>70.82</td>
  </tr>
</table>


![figure1](assets/vbench.png "figure1")


## 6. 在线引擎
Step-Video-TI2V 的在线版本可在 [跃问视频](https://yuewen.cn/videos) 使用，你还可以在那里探索一些令人惊艳的示例。

## 7. 引用
```
@misc{huang2025step,
      title={Step-Video-TI2V Technical Report: A State-of-the-Art Text-Driven Image-to-Video Generation Model}, 
      author={Haoyang Huang, Guoqing Ma, Nan Duan, Xing Chen, Changyi Wan, Ranchen
  Ming, Tianyu Wang, Bo Wang, Zhiying Lu, Aojie Li, Xianfang Zeng, Xinhao
  Zhang, Gang Yu, Yuhe Yin, Qiling Wu, Wen Sun, Kang An, Xin Han, Deshan Sun,
  Wei Ji, Bizhu Huang, Brian Li, Chenfei Wu, Guanzhe Huang, Huixin Xiong,
  Jiaxin He, Jianchang Wu, Jianlong Yuan, Jie Wu, Jiashuai Liu, Junjing Guo,
  Kaijun Tan, Liangyu Chen, Qiaohui Chen, Ran Sun, Shanshan Yuan, Shengming
  Yin, Sitong Liu, Wei Chen, Yaqi Dai, Yuchu Luo, Zheng Ge, Zhisheng Guan,
  Xiaoniu Song, Yu Zhou, Binxing Jiao, Jiansheng Chen, Jing Li, Shuchang Zhou,
  Xiangyu Zhang, Yi Xiu, Yibo Zhu, Heung-Yeung Shum, Daxin Jiang},
      year={2025},
      eprint={2503.11251},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2503.11251}, 
}
```

```
@misc{ma2025stepvideot2vtechnicalreportpractice,
      title={Step-Video-T2V Technical Report: The Practice, Challenges, and Future of Video Foundation Model}, 
      author={Guoqing Ma and Haoyang Huang and Kun Yan and Liangyu Chen and Nan Duan and Shengming Yin and Changyi Wan and Ranchen Ming and Xiaoniu Song and Xing Chen and Yu Zhou and Deshan Sun and Deyu Zhou and Jian Zhou and Kaijun Tan and Kang An and Mei Chen and Wei Ji and Qiling Wu and Wen Sun and Xin Han and Yanan Wei and Zheng Ge and Aojie Li and Bin Wang and Bizhu Huang and Bo Wang and Brian Li and Changxing Miao and Chen Xu and Chenfei Wu and Chenguang Yu and Dapeng Shi and Dingyuan Hu and Enle Liu and Gang Yu and Ge Yang and Guanzhe Huang and Gulin Yan and Haiyang Feng and Hao Nie and Haonan Jia and Hanpeng Hu and Hanqi Chen and Haolong Yan and Heng Wang and Hongcheng Guo and Huilin Xiong and Huixin Xiong and Jiahao Gong and Jianchang Wu and Jiaoren Wu and Jie Wu and Jie Yang and Jiashuai Liu and Jiashuo Li and Jingyang Zhang and Junjing Guo and Junzhe Lin and Kaixiang Li and Lei Liu and Lei Xia and Liang Zhao and Liguo Tan and Liwen Huang and Liying Shi and Ming Li and Mingliang Li and Muhua Cheng and Na Wang and Qiaohui Chen and Qinglin He and Qiuyan Liang and Quan Sun and Ran Sun and Rui Wang and Shaoliang Pang and Shiliang Yang and Sitong Liu and Siqi Liu and Shuliang Gao and Tiancheng Cao and Tianyu Wang and Weipeng Ming and Wenqing He and Xu Zhao and Xuelin Zhang and Xianfang Zeng and Xiaojia Liu and Xuan Yang and Yaqi Dai and Yanbo Yu and Yang Li and Yineng Deng and Yingming Wang and Yilei Wang and Yuanwei Lu and Yu Chen and Yu Luo and Yuchu Luo and Yuhe Yin and Yuheng Feng and Yuxiang Yang and Zecheng Tang and Zekai Zhang and Zidong Yang and Binxing Jiao and Jiansheng Chen and Jing Li and Shuchang Zhou and Xiangyu Zhang and Xinhao Zhang and Yibo Zhu and Heung-Yeung Shum and Daxin Jiang},
      year={2025},
      eprint={2502.10248},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2502.10248}, 
}
```


