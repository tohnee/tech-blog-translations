---
title: "CPU+GPU 异构 EPD 分离提升 VLM 推理服务性能"
title_en: "Heterogeneous CPU + GPU EPD Disaggregation to Boost VLM Serving"
author: "Intel & SGLang Team"
date: "May 29, 2026"
previewImg: /images/blog/hetero-epd/1.png
source: https://lmsys.org/blog/2026-06-01-hetero-epd/
translated: 2026-09-12
---

# CPU+GPU 异构 EPD 分离提升 VLM 推理服务性能

> 原文：[Heterogeneous CPU + GPU EPD Disaggregation to Boost VLM Serving](https://lmsys.org/blog/2026-06-01-hetero-epd/) · LMSYS Blog · Intel & SGLang Team

**TL;DR**

我们通过 Dynamo 和 SGLang 为视觉语言模型（VLM）实现了异构 Encode-Prefill-Decode（EPD）分离。通过将视觉编码任务卸载到 CPU（最容易获取的 CPU 资源就是头节点上的 CPU），我们在多项指标上取得了一致的性能提升：首 token 延迟（TTFT，Time to First Token）、每 token 生成时间（TPOT，Time Per Output Token）以及负载下的整体吞吐量。

## 引言

SGLang 社区已经证明了 EPD 分离对 VLM 推理服务的必要性与收益 ^{[1]}。结果表明，在向服务输入多张图像的图像密集型场景中，EPD 能够显著降低 TTFT。鉴于视觉编码是图像密集型场景中的主要计算瓶颈，我们发现将部分视觉编码工作卸载到头节点 CPU 上有助于提升性能：

- 视觉编码器（CNN/ViT）通常比语言模型部分小，因此配备先进矩阵加速器（如 Intel Xeon CPU 中的 AMX）的现代 CPU 有能力分担这部分工作。
- 视觉编码只发生在预填充（prefill）阶段，因此可以方便地接入异构 worker，而无需持续的跨 worker 状态管理。

## 设备感知加权路由器

通过与 Dynamo 社区合作，我们向 Dynamo 路由器合入了一种新的设备感知加权路由模式，以支持异构分发（PR [#7215](https://github.com/ai-dynamo/dynamo/pull/7215)）。它在设备之间（具体指 CPU 与 GPU 之间）引入了基于预算的限流机制。

在计算能力各异的异构部署环境中（例如 GPU 与 CPU），设备感知加权路由器使用能力比率（Capability Ratio）$R$ 来定义 GPU 相对于 CPU 的吞吐量比例。路由器会计算 CPU 允许的在途请求预算（Allowed CPU In-flight Budget，$B_{cpu}$）。该预算表示 CPU 池应处理的最大请求数，以与 GPU 池当前的压力保持"同步"：

$$B_{cpu} = \frac{I_{gpu}N_{cpu}}{RN_{gpu}}$$

其中，$I_{gpu}$ 是所有 GPU 实例上的在途请求总数，$N_{cpu}$ 和 $N_{gpu}$ 分别是 CPU 实例和 GPU 实例的数量。

路由决策非常简单：当 $I_{cpu}$（所有 CPU 实例上的在途请求总数）小于 $B_{cpu}$ 时，说明 CPU 池相对其归一化容量尚未被充分利用，因此路由到 CPU 池；否则，路由到 GPU 池。

<img src="/images/blog/hetero-epd/1.png"
     style="display: block; margin: 20px auto 0; width: 75%; max-width: 100%; height: auto;">

*图 1：设备感知加权路由器*

## 实验设置

### 用例配置

**环境：**
- Intel(R) Xeon(R) 6747P CPU（2 个插槽，每个插槽 2 个 NUMA 节点，共 4 个 NUMA 节点）$^{[2]}$
- 5 块 L40S CUDA GPU $^{[3]}$

**模型：**
- Qwen3-VL-8B-Instruct

**数据集：**
- ISL/OSL：128/256
- 图像分辨率：1080p
- 图像数量：8
- QPS 范围：1.0、1.2、1.5、2.0

**部署配置：**
- 1E/4PD（编码器：1 个 GPU 编码器，PD：4 个 GPU）
- (4 CPU + 1 GPU) E/4PD（编码器：4 个 CPU + 1 个 GPU，PD：4 个 GPU），能力比率 $R$ 设为 12

### 用例启动脚本

**启动视觉编码器实例：**

```shell
# launch cuda encoder
CUDA_VISIBLE_DEVICES=0 numactl --cpunodebind=0 --membind=0 python -m dynamo.sglang --multimodal-encode-worker --model-path "$MODEL_NAME" --chat-template "$CHAT_TEMPLATE" --embedding-transfer-mode nixl-read &

# launch cpu encoders, DYN_ENCODER_CUDA_TO_CPU_RATIO is 12 in this case
for node in 0 1 2 3; do 12
  case "$node" in
    0) cpus="$(printf "%s\n%s\n" "$(seq 0 2 46)"  "$(seq 96 2 142)" | paste -sd, -)" ;;
    1) cpus="$(printf "%s\n%s\n" "$(seq 48 2 94)" "$(seq 144 2 190)" | paste -sd, -)" ;;
    2) cpus="$(printf "%s\n%s\n" "$(seq 1 2 47)"  "$(seq 97 2 143)" | paste -sd, -)" ;;
    3) cpus="$(printf "%s\n%s\n" "$(seq 49 2 95)" "$(seq 145 2 191)" | paste -sd, -)" ;;
  esac

  CUDA_VISIBLE_DEVICES="" \
  SGLANG_USE_CPU_ENGINE=1 \
  SGLANG_CPU_OMP_THREADS_BIND="$cpus" \
  numactl --cpunodebind="$node" --membind="$node" \
  python -m dynamo.sglang \
      --multimodal-encode-worker \
      --model-path "$MODEL_NAME" \
      --chat-template "$CHAT_TEMPLATE" \
      --embedding-transfer-mode nixl-read & 
done
```

**启动 PD 实例：**

```shell
# launch PD instances
for gpu in 2 3 4 5; do
  if [[ "$gpu" -lt 4 ]]; then
    numa_node=0
  else
    numa_node=1
  fi

  CUDA_VISIBLE_DEVICES="$gpu" \
  numactl --cpunodebind="$numa_node" --membind="$numa_node" \
  python3 -m dynamo.sglang \
    --multimodal-worker \
    --model-path "$MODEL_NAME" \
    --page-size 16 \
    --tp 1 \
    --prefill-max-requests 1 \
    --log-level debug \
    --trust-remote-code \
    --skip-tokenizer-init \
    --disable-radix-cache \
    --embedding-transfer-mode nixl-read \
    --disaggregation-transfer-backend nixl &
done
```

**启动路由器：**

```shell
DYN_ENCODER_CUDA_TO_CPU_RATIO=12 python3 -m dynamo.frontend --router-mode device-aware-weighted
```

## 基准测试

### 基准测试脚本

```shell
python -m sglang.bench_serving.py --model Qwen/Qwen3-VL-8B-Instruct  --num-prompts 32 --dataset-name image --random-input-len 128 --random-output-len 256 --image-count 8  --image-resolution 1080p --host localhost --port 8000 --backend sglang-oai-chat --request-rate $QPS
```

### 基准测试结果

#### P99 TTFT

<img src="/images/blog/hetero-epd/2.png"
     style="display: block; margin: 20px auto 0; width: 75%; max-width: 100%; height: auto;">

#### P99 TPOT

<img src="/images/blog/hetero-epd/3.png"
     style="display: block; margin: 20px auto 0; width: 75%; max-width: 100%; height: auto;">

#### 请求吞吐量

<img src="/images/blog/hetero-epd/4.png"
     style="display: block; margin: 20px auto 0; width: 75%; max-width: 100%; height: auto;">

**关键发现：**

- 在负载条件下（QPS 介于 1 到 2 之间），CPU+GPU 异构 EPD 分离在所有指标（TTFT、TPOT、请求吞吐量）上都持续优于纯 GPU EPD 分离。
- P99 TTFT 和请求吞吐量可获得约 1.2 倍至 1.3 倍的提升，表明在负载下 CPU 帮助分担了 GPU 上视觉编码器的负担。
- 通过缓解视觉编码流量并缩短超过 2 个 token 的生成排队时间，P99 TPOT 实现了约 1.3 倍至 30 倍的大幅降低。

CPU+GPU 异构 EPD 分离在纯 GPU EPD 分离 $^{[1]}$ 带来的投资回报（ROI）之外，几乎零成本地获得了额外更高的回报。这得益于系统级优化——以全局系统视角将 AMX 加持的 CPU 纳入了方案空间。

## 参考文献

1. [EPD 分离：SGLang 中面向视觉语言模型的弹性编码器扩展（EPD Disaggregation: Elastic Encoder Scaling for Vision-Language Models in SGLang）](https://www.lmsys.org/blog/2026-01-12-epd/)
2. [Intel(R) Xeon(R) 6747P CPU](https://www.intel.com/content/www/us/en/products/sku/241825/intel-xeon-6747p-processor-288m-cache-2-70-ghz/specifications.html)
3. [NVIDIA L40S](https://www.nvidia.com/en-us/data-center/l40s/)
