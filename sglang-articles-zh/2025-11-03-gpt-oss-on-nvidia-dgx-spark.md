---
title: "在 NVIDIA DGX Spark 上优化 GPT-OSS：充分释放你的 Spark 性能"
title_en: "Optimizing GPT-OSS on NVIDIA DGX Spark: Getting the Most Out of Your Spark"
author: "Jerry Zhou"
date: "November 3, 2025"
previewImg: /images/blog/gpt_oss_on_nvidia_dgx_spark/preview.jpg
source: https://lmsys.org/blog/2025-11-03-gpt-oss-on-nvidia-dgx-spark/
translated: 2026-09-12
---

# 在 NVIDIA DGX Spark 上优化 GPT-OSS：充分释放你的 Spark 性能

> 原文：[Optimizing GPT-OSS on NVIDIA DGX Spark: Getting the Most Out of Your Spark](https://lmsys.org/blog/2025-11-03-gpt-oss-on-nvidia-dgx-spark/) · LMSYS Blog · Jerry Zhou

关于 **NVIDIA DGX Spark**，我们有一些激动人心的更新要与大家分享！在 DGX Spark 正式发布后的一周内，我们与 NVIDIA 紧密合作，成功让 DGX Spark 上的 **SGLang** 支持了 **GPT-OSS 20B** 和 **GPT-OSS 120B**。结果令人印象深刻：GPT-OSS 20B 达到约 **70 tokens/s**，GPT-OSS 120B 达到 **50 tokens/s**——这是目前为止的最优水平，也让在 DGX Spark 上运行**本地编程智能体**变得完全可行。

![](/images/blog/gpt_oss_on_nvidia_dgx_spark/demo_1.png)

> 我们已在<a href="https://docs.google.com/spreadsheets/d/1SF1u0J2vJ-ou-R_Ry1JZQ0iscOZL8UKHpdVFr85tNLU/edit?usp=sharing" target="_blank">这里</a>更新了详细的基准测试结果，欢迎观看<a href="https://youtu.be/ApIVoTuWIss" target="_blank">我们的演示视频</a>。

在本文中，你将了解如何：

* 在 DGX Spark 上用 SGLang 运行 GPT-OSS 20B 或 120B  
* 在本地进行性能基准测试  
* 接入 **Open WebUI** 进行聊天  
* 甚至通过 **LMRouter** 完全在本地运行 **Claude Code**

## 1. 准备环境

在启动 SGLang 之前，请确保已准备好 OpenAI Harmony 所需的 **tiktoken encodings**（tiktoken 编码文件）：

```bash
mkdir -p ~/tiktoken_encodings
wget -O ~/tiktoken_encodings/o200k_base.tiktoken "https://openaipublic.blob.core.windows.net/encodings/o200k_base.tiktoken"
wget -O ~/tiktoken_encodings/cl100k_base.tiktoken "https://openaipublic.blob.core.windows.net/encodings/cl100k_base.tiktoken"
```

## 2. 使用 Docker 启动 SGLang

现在，使用以下命令启动 SGLang 服务器：

```bash
docker run --gpus all \
    --shm-size 32g \
    -p 30000:30000 \
    -v ~/.cache/huggingface:/root/.cache/huggingface -v ~/tiktoken_encodings:/tiktoken_encodings \
    --env "HF_TOKEN=<secret>" --env "TIKTOKEN_ENCODINGS_BASE=/tiktoken_encodings" \
    --ipc=host \
    lmsysorg/sglang:spark \
    python3 -m sglang.launch_server --model-path openai/gpt-oss-20b --host 0.0.0.0 --port 30000 --reasoning-parser gpt-oss --tool-call-parser gpt-oss
```

将 `<secret>` 替换为你的 **Hugging Face access token**。如果你想运行 **GPT-OSS 120B**，只需把模型路径改为 `openai/gpt-oss-120b`。该模型的规模约为 20B 版本的 6 倍，因此加载时间会稍长一些。为了获得最佳性能与稳定性，建议在你的 DGX Spark 上启用 **swap memory**（交换内存）。

## 3. 测试服务器

SGLang 运行起来之后，你可以直接发送 OpenAI 兼容格式的请求：

```bash
curl http://localhost:30000/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "How many letters are there in the word SGLang?"
            }
        ]
    }'
```

![](/images/blog/gpt_oss_on_nvidia_dgx_spark/demo_2.jpg)

## 4. 性能基准测试

测试吞吐量有一个简便方法：请求生成一段很长的输出，例如：

```bash
curl http://localhost:30000/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "Generate a long story. The only requirement is long."           
            }
        ]
    }'
```

在典型条件下，GPT-OSS 20B 应该能达到约 **每秒 70 个 token（70 tokens/s）**。

## 5. 运行本地聊天机器人（Open WebUI）

要搭建一个友好的本地聊天界面，你可以在 DGX Spark 上安装 **Open WebUI**，并将其指向正在运行的 SGLang 后端：`http://localhost:30000/v1`。按照 <a href="https://github.com/open-webui/open-webui?tab=readme-ov-file#how-to-install-" target="_blank">Open WebUI 安装说明</a>完成安装和启动。连接成功后，你就可以与本地 GPT-OSS 实例流畅对话了——全程无需联网。

![](/images/blog/gpt_oss_on_nvidia_dgx_spark/demo_3.jpg)

## 6. 完全在本地运行 Claude Code

在本地跑起 GPT-OSS 模型之后，你甚至可以通过 <a href="https://github.com/LMRouter/lmrouter" target="_blank">**LMRouter**</a> 接入 **Claude Code**——它能够把 Anthropic 风格的请求转换为 OpenAI 兼容格式。

### 第 1 步：创建 LMRouter 配置文件

将<a href="https://gist.github.com/yvbbrjdr/0514a32124682f97370dda9c09c3349c" target="_blank">这个文件</a>保存为 `lmrouter-sglang.yaml`。

### 第 2 步：启动 LMRouter

安装 <a href="https://pnpm.io/installation" target="_blank">**pnpm**</a>（如果尚未安装），然后运行：

```bash
pnpx @lmrouter/cli lmrouter-sglang.yaml
```

### 第 3 步：启动 Claude Code

按照 <a href="https://www.claude.com/product/claude-code" target="_blank">安装指南</a>安装 **Claude Code**，然后按如下方式启动：

```bash
ANTHROPIC_BASE_URL=http://localhost:3000/anthropic \
ANTHROPIC_AUTH_TOKEN=sk-sglang claude
```

大功告成！现在你可以**在本地使用 Claude Code** 了，其背后完全由 **DGX Spark 上的 GPT-OSS 20B 或 120B** 驱动。

![](/images/blog/gpt_oss_on_nvidia_dgx_spark/demo_4.jpg)

## 7. 结语

通过以上步骤，你可以充分释放 **DGX Spark** 的潜力，把它打造成一台本地 AI 强机，交互式地运行数百亿参数量级的模型。
