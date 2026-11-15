---
title: "FastH3 登陆消费级硬件：RTX GPU、DGX Spark 与 Mac，外加 FastH3 Trim"
title_en: "FastH3 on Consumer Hardware: RTX GPUs, DGX Spark and Macs, Plus FastH3 Trim"
date: 2026-10-06
source: https://haoailab.com/blogs/fasth3-rtx/
crawled: 2026-11-16
translated: 2026-11-16
---

# FastH3 登陆消费级硬件：RTX GPU、DGX Spark 与 Mac，外加 FastH3 Trim

> 原文：[FastH3 on Consumer Hardware: RTX GPUs, DGX Spark and Macs, Plus FastH3 Trim](https://haoailab.com/blogs/fasth3-rtx/) · Hao AI Lab @ UCSD

2026 年 10 月 6 日 · 12 分钟 · Aryan Kumar、Will Lin、Hao Zhang

![DGX Spark、Mac Studio、RTX 4090 与 RTX 5090 的蓝图式线稿](img/cover.jpg)

[![](https://img.shields.io/github/stars/hao-ai-lab/FastVideo?style=social)](https://github.com/hao-ai-lab/FastVideo)[![](https://img.shields.io/badge/🤗%20huggingface--green.svg?style=social)](https://huggingface.co/collections/FastVideo/fastvideo-fasth3)[![Slack](https://img.shields.io/badge/Slack--4A154B?style=social&logo=slack&logoColor=blue)](https://join.slack.com/t/fastvideo/shared_invite/zt-3f4lao1uq-u~Ipx6Lt4J27AlD2y~IdLQ)

FastH3 V2 用八步生成带同步音频的视频，而在这八步上，它已经在质量上超过了基础 H3。此前它需要数据中心 GPU：权重占 138 GiB。今天，FastH3 V2 可以运行在单台消费级机器上：一块 RTX 5090、RTX 4090 或 RTX PRO 6000，一台 DGX Spark，或一台 Apple Silicon Mac。我们还发布 **FastH3 Trim**，一个实验性的更小版本，从 50 个 transformer 块中去掉 8 个，以便跑得更快。

本文是 [FastH3 落地本地](/blogs/fasth3-local/) 的续篇——那篇把 FastH3 带到 DGX Spark 与 Mac 上，并把 RTX 系列列为下一个目标。

## TL;DR[#](#tldr)

* **FastH3 V2 现在可以运行在单块消费级 GPU、一台 DGX Spark 或一台 Mac 上。** 我们为 Blackwell GPU 与 DGX Spark 提供 NVFP4，为 RTX 4090 及显存更少的 GPU 提供 FP8，为 Apple Silicon 提供 INT6。
* **量化不牺牲质量。** 每个 FP4 层使用的激活缩放都在 1,000 条提示词上校准，因此大幅值激活不会被截断。
* **FastH3 Trim 是一次把模型做小的实验。** 它比基础 H3 小 4.2 倍，在每台设备上都比 V2 更快，最低可在 8 GB 显存内运行，质量代价很小。
* **仍有改进空间，我们会继续推进。** 两个模型都是八步蒸馏；我们预计后续版本会有更好的质量和更小的模型。

## 相同提示词，每台机器[#](#same-prompt-every-machine)

每行是一台机器。左侧片段是 FastH3 V2，右侧是 FastH3 Trim，二者来自同一提示词与随机种子，832×480、5 秒、含音频。请打开声音。另外三条提示词见[更多样例](#more-samples)。

FastH3 V2

FastH3 Trim

**RTX 5090**32 GB · NVFP4

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-rtx--img--videos--rtx5090--v2-nvfp4-corgi-weather.mp4#t=0.1)

**V2 · NVFP4**14.8 秒

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-rtx--img--videos--rtx5090--trim-nvfp4-corgi-weather.mp4#t=0.1)

**Trim · NVFP4**13.4 秒

**RTX PRO 6000**96 GB · NVFP4

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-rtx--img--videos--rtx-pro-6000--v2-nvfp4-corgi-weather.mp4#t=0.1)

**V2 · NVFP4**13.5 秒

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-rtx--img--videos--rtx-pro-6000--trim-nvfp4-corgi-weather.mp4#t=0.1)

**Trim · NVFP4**12.0 秒

**RTX 4090**24 GB · FP8

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-rtx--img--videos--rtx4090-24gb--v2-fp8-corgi-weather.mp4#t=0.1)

**V2 · FP8**54.6 秒

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-rtx--img--videos--rtx4090-24gb--trim-fp8-corgi-weather.mp4#t=0.1)

**Trim · FP8**43.9 秒

**DGX Spark**128 GB 统一内存 · NVFP4

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-rtx--img--videos--spark-1x--v2-nvfp4-corgi-weather.mp4#t=0.1)

**V2 · NVFP4**141.4 秒

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-rtx--img--videos--spark-1x--trim-nvfp4-corgi-weather.mp4#t=0.1)

**Trim · NVFP4**125.8 秒

**Mac（M4 Max）**36 GB 统一内存 · INT6

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-rtx--img--videos--m4max--v2-int6-corgi-weather.mp4#t=0.1)

**V2 · INT6**

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-rtx--img--videos--m4max--trim-int6-corgi-weather.mp4#t=0.1)

**Trim · INT6**925.2 秒

## 跑得多快[#](#how-fast-it-runs)

我们为每台机器报告两个数字：832×480 的 5 秒片段，以及 1344×768 的 5 秒片段，均含音频。时间是热启动服务器上从提示词到成品 MP4 的端到端耗时：文本编码、八步去噪、视频与音频解码，以及导出。每个数字是两条提示词各跑两次的中位数。

![每台机器成对细柱，FastH3 V2 与 FastH3 Trim，5 秒、832×480 片段的端到端秒数，对数刻度。](img/fig_e2e.svg)

图 1. 5 秒、832×480、含音频片段的端到端时间。每行是一台机器。

| 机器 | 显存 | V2, 480p | Trim, 480p | V2, 768p | Trim, 768p |
| --- | --- | --- | --- | --- | --- |
| RTX PRO 6000 | 96 GB | 13.5 秒 | 12.0 秒 | 36.5 秒 | 32.5 秒 |
| RTX 5090 | 32 GB | 14.8 秒 | 13.4 秒 | 38.6 秒 | 35.4 秒 |
| RTX 4090 | 24 GB | 54.6 秒 | 43.9 秒 | 154.6 秒 | 132.8 秒 |
| RTX 4090，限制 16 GB | 16 GB | 79.9 秒 | 72.1 秒 | 153.7 秒 | 139.9 秒 |
| RTX 4090，限制 12 GB | 12 GB | 91.2 秒 | 74.1 秒 | 170.7 秒 | 147.1 秒 |
| RTX 4090，限制 8 GB | 8 GB | — | 82.0 秒 | — | — |
| DGX Spark | 128 GB 统一内存 | 141.4 秒 | 125.8 秒 | — | 340.1 秒 |
| 2× DGX Spark | 各 128 GB | 87.2 秒 | 78.3 秒 | — | — |
| Mac，M4 Max | 36 GB 统一内存 | — | 925.2 秒 | — | — |

## 把 H3 装进一台机器[#](#fitting-h3-on-one-machine)

H3 是三个网络。一个 Qwen3-VL 文本编码器读取提示词，一个 50 块的扩散 transformer（DiT）同时去噪视频与音频隐变量，两个 VAE 把隐变量解码成画面与声音。BF16 下这些权重合计 137.7 GiB，一块 32 GB 的 RTX 5090 连 DiT 都装不下。我们逐个压缩这三个网络。

![堆叠柱状图。BF16 H3：文本编码器 62.1 GiB、DiT 65.3 GiB、VAE 10.3 GiB，合计 137.7 GiB。FastH3 Trim 使用 NVFP4：文本编码器 15.3、DiT 11.1、VAE 6.5，合计 33.0 GiB。](img/fig_memory_stack.svg)

图 2. 各组件检查点大小。FastH3 Trim 的 NVFP4 版本比 BF16 H3 小 4.2 倍。

* **文本编码器：62.1 → 15.3 GiB。** H3 读取 64 层 Qwen3-VL 的第 50 层隐藏状态，且从不生成文本，因此我们去掉最后 14 层和语言模型头，而不改变 H3 使用的特征。其余线性层以 NVFP4 存储。
* **Transformer：BF16 下 65.3 GiB。** 对 FastH3 V2，我们以 NVFP4 存储注意力、MLP 与稀疏注意力门控权重（在不支持 FP4 的 GPU 上用 FP8）。FastH3 Trim 还去掉 50 个块中的 8 个，并把每个块的 timestep 投影替换为 rank-16 分解，在 NVFP4 下降到 11.1 GiB。
* **VAE：10.3 → 6.5 GiB。** 我们用 [LynnReal 轻量视频 VAE](https://huggingface.co/stdstu123/LynnReal-Onmi-light-vae) 解码视频，这是一个蒸馏的 26 块解码器，隐变量接口与 H3 VAE 相同，加载 [Kijai 的 INT8 权重](https://huggingface.co/Kijai/MiniMax-H3-experimental)。它占用 2.3 GiB 显存，本文所有设备都使用同一个。

体积直接影响速度。在 32 GB 的 GPU 上，问题在于 DiT 能否在两次请求之间留在显存里。如果能，每个请求就只需要把文本编码器换进换出。

### RTX 5090[#](#rtx-5090)

我们最初的 FP4 导出只量化 MLP，这是我们在数据中心 GPU 上用的设置。在 5090 上，这留下了 20 GB 的 DiT——仅 BF16 注意力投影就占 9.7 GB——文本编码器再也装不到它旁边。每个请求都要把 DiT 搬到主机内存再搬回来：480p 片段耗时 26.4 秒，768p 片段根本装不下。

把注意力与门控也放进 NVFP4 后，DiT 为 11.1 GiB 并能常驻 GPU，文本编码器则逐层流式加载。同样的 480p 片段现在只需 13.4 秒，768p 也装得下了。

PyTorch 的锁页内存分配器会把每个块向上取整到 2 的幂，于是 2.87 GiB 的 FP4 权重占用了 5.06 GiB 主机内存，足以在 60 GB 的云容器里把进程 OOM 掉。我们改用 `cudaHostRegister` 为每个模块锁定一个精确大小的缓冲区，占用 2.90 GiB。

### RTX 4090 与更小显存[#](#rtx-4090-and-smaller-memory)

RTX 4090 没有 FP4 tensor core，因此使用 FP8：8-bit 权重，每个输出通道一个缩放；8-bit 激活，每个 token 一个缩放。PyTorch 在这套缩放下的 FP8 矩阵乘法在 4090 上约为 70 TFLOPS，比 BF16 的约 160 TFLOPS 更慢。逐张量 FP8 kernel 能跑到 220–305 TFLOPS，所以我们用单位缩放调用它，并在一次融合 pass 中把两个缩放向量作用到输出上。结果与逐 token、逐通道缩放一致，成本比逐张量缩放高 5–10%。

再有三处改动，把 4090 上的 5 秒片段压到 43.9 秒：

* **稀疏注意力：** query 与 key 在分数计算时量化为 INT8，value 保持 BF16。细粒度注意力 kernel 快 1.6 倍，相对误差约 0.6%。
* **文本编码器：** 通过精确大小的锁页缓冲区逐层流式传到 GPU，并用一个融合 kernel 展开其 NVFP4 权重。
* **VAE：** 与其他设备相同的 INT8 轻量 VAE，带融合反量化步骤，Q、K、V 投影共享同一个量化输入。解码帧与未优化路径逐比特一致。

16 GB、12 GB 与 8 GB 那几行，是在同一块 4090 上限制显存得到的。两个模型都能装进 12 GB，FastH3 Trim 能装进 8 GB；真实显存更小的卡会更慢。

### DGX Spark 与 Apple Silicon[#](#dgx-spark-and-apple-silicon)

DGX Spark 把文本编码器、transformer 和两个 VAE 都常驻在其 128 GB 统一内存里，因此请求之间没有数据搬移。它使用与 5090 相同的 NVFP4 检查点和轻量 VAE，两台 Spark 则用序列并行切分每个请求。在 [FastH3 落地本地](/blogs/fasth3-local/) 中，使用四步 preview 模型时，单台 Spark 上 5 秒片段耗时 243 秒；现在的八步模型做了两倍的去噪步数，完成得却更快。

在 Apple Silicon 上，两个模型都以 MLX 运行，使用 INT6 权重、NVFP4 文本编码器和轻量 VAE。

## 不截断的四位权重[#](#four-bit-weights-without-clipping)

NVFP4 把每 16 个值存为一组 4-bit 浮点，共享一个 8-bit 缩放，另有一个逐张量缩放决定整体范围。对权重，我们直接从权重本身计算这个逐张量缩放。对激活，它必须在数据到达之前就固定下来。最简单的选择是单位缩放，可覆盖到 6 × 448 = 2,688 的幅值，而 H3 的激活远大于此。

![柱状图：42 个块中各块 MLP 输出投影的最大输入，对数刻度。42 根柱子中有 40 根超过 2,688 这条线；第 37 块达到 368,640。](img/fig_fc_out_amax.svg)

图 3. 每块 MLP 输出投影的最大输入，统计自 1,000 条校准提示词的全部八步。使用单位缩放时，虚线以上的数值全都会被截断。

在 42 个块中有 40 个，MLP 输出投影的输入超过 2,688。第 37 块达到 368,640，是上限的 137 倍，单位缩放下每次前向都会截断这些值。所以我们要校准：把 1,000 条提示词跑过完整的八步采样器，记录每个线性层的最大输入，并把每层一个静态缩放存入检查点。FastH3 Trim 有 294 个校准层，覆盖注意力投影、MLP 与稀疏注意力门控。这把 FastH3 V2 的 NVFP4 配方从 MLP 扩展到了每一个量化层。

## FastH3 Trim：一次剪枝实验[#](#fasth3-trim-an-experiment-in-pruning)

剪枝是我们通往更小模型的路径。我们移除实测最不重要的块，这让模型更小更快，但也带走了它们学到的一部分能力。FastH3 Trim 是我们的第一步。

![按比例绘制的方块，面积等于 transformer 检查点大小。H3 BF16 为 65.3 GiB，用 0 到 49 号块铺满；第 6、7、9、13、15、16、22、23 号块为红色（已移除），第 0、1、5、47、48、49 号块加描边表示最敏感。箭头指向更小的方块，用同样的 42 个保留块铺成：Trim BF16 34.8 GiB（小 1.9 倍）、FP8 19.9（3.3 倍）、INT6 14.3（4.6 倍）、NVFP4 11.1（5.9 倍）。](img/fig_squares.svg)

图 4. 我们发布的各格式 FastH3 Trim transformer，按比例绘制：面积即检查点大小。

### 如何挑选块[#](#choosing-the-blocks)

我们第一个剪枝模型按激活选择块，效果明显好于等间隔移除块。我们用教师引导恢复了那个模型，再用 DMD 减少其采样步数。运动连贯性、细节和提示词遵循度始终偏弱。在我们的并排比较中，量化感知蒸馏（QAD）并未胜过训练后量化。

对 FastH3 Trim，我们直接测量每个块。从基础 H3 出发，一次跳过一个块，记录视频与音频预测变化了多少。我们在三种噪声水平下测试了四个样例（运动、语音、音乐与音效），共 600 次测量。每个块按它在任何条件下造成的最大变化排序，因此只要对视频或音频之一重要，该块就会被保留。首尾两个块对输出的影响最大。我们移除的 8 个块全部位于网络前半部分。

### 压缩 timestep 条件[#](#compressing-the-timestep-conditioning)

H3 通过 AdaLN 投影把扩散 timestep 作为每个块的条件，该投影把一个 2,688 维时间嵌入映射为六个调制向量。50 个块的这些投影在 BF16 下占用 24 GiB。然而它们的输入只是单个数字（timestep）的平滑函数，因此只用到 2,688 维中的很少几维。FastH3 Trim 把投影替换为一个共享的 2,688→16 基，加上每个块一个小投影。分解后的权重以 FP16 存储，因为 BF16 的重建误差大约高 1.7 倍。

### 训练[#](#training)

我们直接用八步 DMD2、沿用 FastH3 V2 的目标函数训练这个新的 42 块模型。基础 H3 同时初始化冻结的教师和可训练的 critic，注意力为 80% 稀疏。模型在 timestep 999、874、749、624、500、375、250 和 125 上采样。

## 时间花在哪里[#](#where-the-time-goes)

![100% 堆叠柱状图。RTX PRO 6000 Trim NVFP4，480p、5 秒、12.0 秒：去噪 78%、解码 17%、其余 5%。RTX 5090 Trim NVFP4，480p、5 秒、13.4 秒：去噪 68%、解码 16%、其余 16%。RTX 4090 Trim FP8，480p、5 秒、43.9 秒：去噪 75%、解码 17%、其余 7%。DGX Spark Trim NVFP4，480p、5 秒、125.8 秒：去噪 65%、解码 34%、其余 1%。Mac，M4 Max Trim MLX INT6，480p、5 秒、925.2 秒：去噪 91%、解码 8%、其余 2%。](img/fig_stages.svg)

图 5. 各阶段占端到端时间的比例。

图 5 把一段 5 秒、480p 的 FastH3 Trim 片段按阶段拆分到各机器上。在 RTX PRO 6000 上，所有模型都常驻显存，去噪占 12.0 秒中的 78%。RTX 5090 的去噪同样快（9.1 秒），总耗时 13.4 秒，因为只有文本编码器和解码器在主机与 GPU 之间搬移。RTX 4090 没有 FP4 tensor core，因此跑 FP8，并且每步都要从主机内存流式加载部分 transformer；43.9 秒中有 33.1 秒是去噪。在 DGX Spark 上，视频解码占了三分之一时间（42.6 秒），这是我们下一个要优化的阶段。在 Mac 上，去噪占 91%，因为注意力仍跑在参考路径上，而不是调优过的 Metal kernel。

## 局限与后续[#](#limitations-and-what-comes-next)

* **FastH3 Trim 是实验性的。** 复杂场景的细节可能不如 V2；质量优先时请用 V2。
* **显存档位是模拟的。** 16 GB、12 GB 和 8 GB 的数字是在一块 4090 上限制显存得到的；真实同等显存的卡会更慢。

## 获取模型[#](#get-the-models)

| 硬件 / 运行时 | FastH3 V2 | FastH3 Trim |
| --- | --- | --- |
| RTX 5090、RTX PRO 6000、DGX Spark（NVFP4） | [`FastVideo-FastH3-8-Step-V2-NVFP4-Consumer`](https://huggingface.co/FastVideo/FastVideo-FastH3-8-Step-V2-NVFP4-Consumer) | [`FastVideo-FastH3-Trim-8-Step-NVFP4`](https://huggingface.co/FastVideo/FastVideo-FastH3-Trim-8-Step-NVFP4) |
| RTX 4090 及低至 8 GB 的 GPU（FP8） | [`FastVideo-FastH3-8-Step-V2-FP8`](https://huggingface.co/FastVideo/FastVideo-FastH3-8-Step-V2-FP8) | [`FastVideo-FastH3-Trim-8-Step-FP8`](https://huggingface.co/FastVideo/FastVideo-FastH3-Trim-8-Step-FP8) |
| Apple Silicon（MLX INT6） | [`FastVideo-FastH3-8-Step-V2-MLX-INT6`](https://huggingface.co/FastVideo/FastVideo-FastH3-8-Step-V2-MLX-INT6) | [`FastVideo-FastH3-Trim-8-Step-MLX-INT6`](https://huggingface.co/FastVideo/FastVideo-FastH3-Trim-8-Step-MLX-INT6) |
| ComfyUI 检查点 | [`FastVideo-FastH3-8-Step-V2-NVFP4-Comfy`](https://huggingface.co/FastVideo/FastVideo-FastH3-8-Step-V2-NVFP4-Comfy) | [`FastVideo-FastH3-Trim-Comfy`](https://huggingface.co/FastVideo/FastVideo-FastH3-Trim-Comfy) |
| 源权重（BF16） | [`FastVideo-FastH3-8-Step-V2`](https://huggingface.co/FastVideo/FastVideo-FastH3-8-Step-V2) | [`FastVideo-FastH3-Trim-8-Step`](https://huggingface.co/FastVideo/FastVideo-FastH3-Trim-8-Step) |

所有仓库都在 [FastVideo](https://huggingface.co/FastVideo) 组织下。多 GPU 的数据中心服务继续使用 [`FastVideo-FastH3-8-Step-V2-NVFP4`](https://huggingface.co/FastVideo/FastVideo-FastH3-8-Step-V2-NVFP4)。每个 FastVideo 格式的消费级仓库都包含 NVFP4 文本编码器、轻量 VAE，以及一个含采样调度的 `fastvideo_inference.json` 文件，FastVideo 会自动读取。在单块 RTX 5090 上：

```
import os

from huggingface_hub import hf_hub_download

repo = "FastVideo/FastVideo-FastH3-8-Step-V2-NVFP4-Consumer"
os.environ["FASTVIDEO_H3_PARK_MODULES"] = "vae,audio_vae"  # keep the transformer on the GPU during text encoding
os.environ["FASTVIDEO_H3_ENCODER_LAYERWISE"] = "1"  # stream the text encoder layer by layer
os.environ["FASTVIDEO_H3_ADALN_TABLE"] = hf_hub_download(repo, "transformer/adaln_tables.pt")  # skip 26 GB of AdaLN weights

from fastvideo import VideoGenerator

generator = VideoGenerator.from_config({
    "model_path": repo,
    "engine": {
        "num_gpus": 1,
        "quantization": {"transformer_quant": "NVFP4", "layer_profile": "h3_dit_vsa"},
        "offload": {"text_encoder": True, "pin_cpu_memory": True},
    },
    "pipeline": {"experimental": {"attention_backend": "VIDEO_SPARSE_ATTN_H3", "h3_sequential_load": True}},
})
generator.generate_video(
    prompt="A red fox leaps into deep snow at sunrise and pops back up with snow on its face.",
    height=480, width=832, num_frames=124, guidance_scale=1.0, output_path="out.mp4",
)
```

把仓库换成 `FastVideo/FastVideo-FastH3-Trim-8-Step-NVFP4` 即可使用更快的实验模型，同时去掉 AdaLN 表那一行。

## 致谢[#](#acknowledgements)

FastH3 构建于 [MiniMax H3](https://huggingface.co/MiniMaxAI/MiniMax-H3)，感谢 MiniMax 团队发布其权重与代码。

轻量解码器是 [LynnReal Lightweight Video VAE](https://huggingface.co/stdstu123/LynnReal-Onmi-light-vae)（[论文](https://arxiv.org/abs/2609.15863)、[代码](https://github.com/LynnReal-AI/LynnReal-Omni)），加载 [Kijai](https://huggingface.co/Kijai) 在 [MiniMax-H3-experimental](https://huggingface.co/Kijai/MiniMax-H3-experimental) 中提供的 INT8 权重。感谢二者。

感谢 NVIDIA Enterprise Products 团队（Pengcheng Li 与 Cliff Woolley）提供 Video Sparse Attention kernel，感谢 FlashInfer 与 NVIDIA Model Optimizer 团队提供 FP4 kernel 与校准工具。RTX GPU 上的 FP4 稀疏注意力构建于 [SageAttention](https://github.com/thu-ml/SageAttention) 之上。

FastVideo 团队与 [Nuva Lab](https://nuvalab.ai/)、[NVIDIA FastGen](https://github.com/NVlabs/FastGen)（Julius Berner、Chao Liu、Arash Vahdat）以及 NVIDIA Enterprise Products 团队在 [FastH3](/blogs/fasth3-preview/) 上紧密合作。我们还要感谢 [vLLM 项目](https://vllm.ai/)、[NVIDIA](https://www.nvidia.com/en-us/) 与 [MBZUAI](https://mbzuai.ac.ae/) 对 FastVideo 的持续赞助与支持。

## FastVideo 团队[#](#fastvideo-team)

**贡献者：** [Aryan Kumar](https://github.com/aryan5v)

  
**技术负责人：** [Will Lin](https://github.com/SolitaryThinker)

  
**指导：** [Hao Zhang](https://github.com/zhisbug)

## 更多样例[#](#more-samples)

FastH3 V2（上）与 FastH3 Trim（下），单块 RTX 5090，832×480、5 秒含音频。

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-rtx--img--videos--rtx5090--v2-nvfp4-street-food-jingle.mp4#t=0.1)

V2 · 街头小吃广告曲

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-rtx--img--videos--rtx5090--v2-nvfp4-parrot-pirate.mp4#t=0.1)

V2 · 海盗与鹦鹉

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-rtx--img--videos--rtx5090--v2-nvfp4-grandma-dj.mp4#t=0.1)

V2 · DJ 奶奶

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-rtx--img--videos--rtx5090--trim-nvfp4-street-food-jingle.mp4#t=0.1)

Trim · 街头小吃广告曲

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-rtx--img--videos--rtx5090--trim-nvfp4-parrot-pirate.mp4#t=0.1)

Trim · 海盗与鹦鹉

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-rtx--img--videos--rtx5090--trim-nvfp4-grandma-dj.mp4#t=0.1)

Trim · DJ 奶奶
