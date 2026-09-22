---
title: "Ling：InclusionAI 开源的 MoE 大语言模型"
title_en: "inclusionAI/Ling"
source: https://github.com/inclusionAI/Ling/blob/master/README.md
crawled: 2026-09-22
translated: 2026-09-22
---

# Ling：InclusionAI 开源的 MoE 大语言模型

> 原文：[inclusionAI/Ling](https://github.com/inclusionAI/Ling/blob/master/README.md) · 蚂蚁集团 InclusionAI

# Ling
<p align="center"><img src="./figures/ant-bailing.png" width="100"/></p>

<p align="center">🤗 <a href="https://huggingface.co/inclusionAI">Hugging Face</a>&nbsp&nbsp | &nbsp&nbsp🤖 <a href="https://modelscope.cn/organization/inclusionAI">ModelScope</a></p>


## 简介

Ling 是由 InclusionAI 提供并开源的 MoE 大语言模型。我们介绍了两种不同规模：Ling-lite 与 Ling-plus。Ling-lite 拥有 168 亿总参数、27.5 亿激活参数；Ling-plus 拥有 2900 亿总参数、288 亿激活参数。与业界现有模型相比，两个模型都展现出令人瞩目的性能。

它们的结构便于向上或向下扩展并适配不同任务，因此用户可以将其用于从自然语言处理到复杂问题求解的广泛任务。此外，Ling 的开源属性促进了 AI 社区内的协作与创新，催生多样的用例与增强。

随着越来越多的开发者和研究者加入该平台，我们可以预期快速的进步与改进，带来更复杂的应用。这种协作方式加速了发展，并确保模型始终处于技术前沿，应对各个领域不断涌现的挑战。

## 更新

- [2025-5-10] Ling-lite-1.5 已发布！与之前的 Ling-lite 相比，其推理能力取得显著进步。
- [2025-4-15] Ling-lite 升级为 Ling-lite-0415。新模型相比前代 Ling-lite-0220 有明显提升，尤其是在代码和数学方面。

## 模型下载

你可以在下表中查看适合你用例的各种参数版本。如果你位于中国大陆，我们还在 ModelScope.cn 上提供模型以加速下载。


|      **模型**       | **总参数量** | **激活参数量** | **上下文长度** |                                                                        **下载**                                                                        |
| :------------------: | :---------------: | :-------------------: | :----------------: | :--------------------------------------------------------------------------------------------------------------------------------------------------------: |
|    Ling-lite-base-1.5    |       16.8B       |         2.75B         |        128K         |     [🤗 HuggingFace](https://huggingface.co/inclusionAI/Ling-lite-base-1.5) <br>[🤖 ModelScope](https://www.modelscope.cn/models/inclusionAI/Ling-lite-base-1.5)     |
|      Ling-lite-1.5       |       16.8B       |         2.75B         |        128K         |          [🤗 HuggingFace](https://huggingface.co/inclusionAI/Ling-lite-1.5) <br>[🤖 ModelScope](https://www.modelscope.cn/models/inclusionAI/Ling-lite-1.5)          |
|    Ling-plus-base    |       290B        |         28.8B         |        64K         |     [🤗 HuggingFace](https://huggingface.co/inclusionAI/Ling-plus-base) <br>[🤖 ModelScope](https://www.modelscope.cn/models/inclusionAI/Ling-plus-base)     |
|      Ling-plus       |       290B        |         28.8B         |        64K         |          [🤗 HuggingFace](https://huggingface.co/inclusionAI/Ling-plus) <br>[🤖 ModelScope](https://www.modelscope.cn/models/inclusionAI/Ling-plus)          |
| Ling-coder-lite-base |       16.8B       |         2.75B         |        16K         | [🤗 HuggingFace](https://huggingface.co/inclusionAI/Ling-Coder-lite-base) <br>[🤖 ModelScope](https://modelscope.cn/models/inclusionAI/Ling-Coder-lite-base) |
|   Ling-coder-lite    |       16.8B       |         2.75B         |        16K         |      [🤗 HuggingFace](https://huggingface.co/inclusionAI/Ling-Coder-lite) <br>[🤖 ModelScope](https://modelscope.cn/models/inclusionAI/Ling-Coder-lite)      |


注：如果你对旧版本感兴趣，请访问 [Huggingface](https://huggingface.co/inclusionAI) 或 [ModelScope](https://modelscope.cn/organization/inclusionAI) 上的历史模型合集。

## 评测

### Ling-lite

#### 标准基准

| **基准**             | **#shots** | **Ling-lite-1.5** | **Ling-lite** | **Qwen3-4B-Instruct** | **Qwen3-8B-Instruct** | **Moonlight-16B-A3B-Instruct** | **LLaMA3.1-8B** |
| :--------------------------------------------: | :--------: | :---------------: | :-----------: | :-------------------: | :-------------------: | :-----------: | :-------------: |
| MMLU(EM)              | 5      | **74.33**         | 71.27     | 70.09             | 75.97             | 70.74     | 68.67       |
| GPQA(Pass@1)          | 0      | **36.55**         | 29.73     | 40.4              | 47.10             | 19.51     | 27.59       |
| HumanEval(Pass@1)     | 0      | **87.27**         | 84.38     | 81.94             | 85.29             | 72.94     | 67.23       |
| LiveCodeBench 2408-2502 (Pass@1) | 0      | **22.7**          | 18.94     | 21.8              | 26.88             | 14.76     | 18.41       |
| LCBench(pass@1)       | 0      | **60.37**         | 46.57     | 48.61             | 60.03             | 28.39     | 23.13       |
| Math(EM)              | 0      | **82.62**         | 72.80     | 81.46             | 82.70             | 67.1      | 52.42       |
| AIME2024(pass@1)      | 0      | **21.88**         | 10.21     | 20.62             | 26.25             | 6.88      | 7.29        |
| OlympiadBench(pass@1) | 0      | **52.30**         | 36.44     | 54.33             | 56.11             | 32.85     | 17.04       |
| BBH(EM)               | 0      | **75.75**         | 66.38     | 78.21             | 79.33             | 63.45     | 68.05       |
| IFEval(Prompt Strict) | 0      | **77.70**         | 77.99     | 81.06             | 83.55             | 49.01     | 73.01       |
| BFCL_live | 0 | **72.15** | 67.93 | 65.35 | 69.83 | 47.14 | 49.98 |

#### 上下文窗口
![](./figures/needle_testing.png)

在「大海捞针」（Needle In A Haystack，NIAH）测试上的评测结果。Ling-lite-1.5 的长文本生成能力有所提升，在最长 **128K** 的大多数上下文窗口长度下均表现良好。

## 快速开始

### 🤗 Hugging Face Transformers

以下代码片段展示如何使用 `transformers` 运行对话模型：

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "inclusionAI/Ling-lite-1.5"

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

prompt = "Give me a short introduction to large language models."
messages = [
    {"role": "system", "content": "You are Ling, an assistant created by inclusionAI"},
    {"role": "user", "content": prompt}
]
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)
model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

generated_ids = model.generate(
    **model_inputs,
    max_new_tokens=512
)
generated_ids = [
    output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
]

response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
```

### 🤖 ModelScope

如果你位于中国大陆，我们强烈建议你从 🤖 <a href="https://modelscope.cn/organization/inclusionAI">ModelScope</a> 使用我们的模型。

## 部署

### vLLM

vLLM 支持离线批量推理，或启动 OpenAI 兼容的 API 服务进行在线推理。

#### 环境准备

由于该 Pull Request（PR）尚未提交到 vLLM 社区，请按以下步骤准备环境：

```bash
git clone -b  v0.7.3 https://github.com/vllm-project/vllm.git
cd vllm
git apply Ling/inference/vllm/bailing_moe.patch
pip install -e .
```

#### 离线推理：

```bash
from transformers import AutoTokenizer
from vllm import LLM, SamplingParams

tokenizer = AutoTokenizer.from_pretrained("inclusionAI/Ling-lite-1.5")

sampling_params = SamplingParams(temperature=0.7, top_p=0.8, repetition_penalty=1.05, max_tokens=16384)

llm = LLM(model="inclusionAI/Ling-lite", dtype='bfloat16')
prompt = "Give me a short introduction to large language models."
messages = [
    {"role": "system", "content": "You are Ling, an assistant created by inclusionAI"},
    {"role": "user", "content": prompt}
]

text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)
outputs = llm.generate([text], sampling_params)

```

#### 在线推理：

```bash
vllm serve inclusionAI/Ling-lite \
              --tensor-parallel-size 2 \
              --pipeline-parallel-size 1 \
              --use-v2-block-manager \
              --gpu-memory-utilization 0.90
```

要在 vLLM 中使用 YaRN 处理长上下文，我们需要遵循以下两步：
1. 在模型的 `config.json` 文件中添加 `rope_scaling` 字段，例如：
```json
{
  ...,
  "rope_scaling": {
    "factor": 4.0,
    "original_max_position_embeddings": 32768,
    "type": "yarn"
  }
}
```
2. 启动 vLLM 服务时，使用附加参数 `--max-model-len` 指定期望的最大上下文长度。

详细指引请参阅 vLLM [`说明文档`](https://docs.vllm.ai/en/latest/)。

### MindIE

本主题概述在指定硬件与 MindIE 推理框架上运行 Ling MoE 模型的主要流程。

#### 配置准备

在主机上创建用于下载的模型目录，目录示例为：/root/models'，稍后用于挂载 docker 容器。

从 github 下载 mindie 相关配置：

```bash
cd /root/models
git clone git@github.com:inclusionAI/Ling.git
```

#### 机器网络环境检查

```bash
# Check the physical link
for i in {0..7}; do hccn_tool -i $i -lldp -g | grep Ifname; done
# Check the links
for i in {0..7}; do hccn_tool -i $i -link -g ; done
# Check your network health
for i in {0..7}; do hccn_tool -i $i -net_health -g ; done
# Check whether the detected IP address is correctly configured
for i in {0..7}; do hccn_tool -i $i -netdetect -g ; done
# Check whether the gateway is configured correctly
for i in {0..7}; do hccn_tool -i $i -gateway -g ; done
# Check the consistency of the underlying TLS verification behavior of the NPU, recommend that all 0 be
for i in {0..7}; do hccn_tool -i $i -tls -g ; done | grep switch
# The underlying TLS check line of the NPU is set to 0
for i in {0..7}; do hccn_tool -i $i -tls -s enable 0; done
```

#### 拉取镜像

前往 [昇腾社区/开发资源](https://www.hiascend.com/developer/ascendhub) 拉取 mindie 镜像

镜像版本：1.0.0-800I-A2-py311-openeuler24.03-lts

各组件版本如下：
| 组件 | 版本     |
| --------- | ----------- |
| MindIE    | 1.0.0       |
| CANN      | 8.0.0       |
| PTA       | 6.0.0.beta1 |
| HDK       | 24.1.0      |

#### 容器启动与配置修改

##### 启动容器

执行以下启动命令（参考）：

```bash
docker run -itd --privileged --name=container name --net=host \
--shm-size 500g \
--device=/dev/davinci0 \
--device=/dev/davinci1 \
--device=/dev/davinci2 \
--device=/dev/davinci3 \
--device=/dev/davinci4 \
--device=/dev/davinci5 \
--device=/dev/davinci6 \
--device=/dev/davinci7 \
--device=/dev/davinci_manager \
--device=/dev/hisi_hdc \
--device /dev/devmm_svm \
-v /usr/local/Ascend/driver:/usr/local/Ascend/driver \
-v /usr/local/Ascend/firmware:/usr/local/Ascend/firmware \
-v /usr/local/sbin/npu-smi:/usr/local/sbin/npu-smi \
-v /usr/local/sbin:/usr/local/sbin \
-v /etc/hccn.conf:/etc/hccn.conf \
-v /root/models:/home/HwHiAiUser/Ascend \
mindie: 1.0.0-XXX-800I-A2-arm64-py3.11 (modified according to the name of the loaded image) \
bash
```

##### 下载模型

本例中，我们使用 ModelScope 下载模型，请先安装 ModelScope：

```bash
pip install modelscope
```

下载模型：

```bash
# The model takes a long time to download and can be executed in the background
nohup modelscope download --model inclusionAI/Ling-plus --local_dir /home/HwHiAiUser/Ascend/Ling_plus 2>&1 > /tmp/ling_plus.log &

nohup modelscope download --model inclusionAI/Ling-plus-base --local_dir /home/HwHiAiUser/Ascend/Ling_plus_base 2>&1 > /tmp/ling_plus_base.log &

nohup modelscope download --model inclusionAI/Ling-lite --local_dir /home/HwHiAiUser/Ascend/Ling_lite 2>&1 > /tmp/ling_lite.log &

nohup modelscope download --model inclusionAI/Ling-lite-base --local_dir /home/HwHiAiUser/Ascend/Ling_lite_base 2>&1 > /tmp/ling_lite_base.log &
```

下载完成后，需要修改文件权限，否则启动 MindIE-Service 时会报错：

```bash
chmod -R 750 *.json *.py
```

##### 模型权重格式转换

> 本节适用于 Ling Lite 模型，Ling Plus 模型无需关注本章内容

mindie 支持 safetensors 格式权重，如果下载的权重不是 safetensors 格式，则需要转换权重。以 Ling Lite 为例，转换命令如下：

```bash
# Convert Ling lite
python /home/HwHiAiUser/Ascend/Ling/inference/mindie/convert_bin_to_safetensor.py

cd /home/HwHiAiUser/Ascend/Ling_lite
cp README.md configuration.json config.json special_tokens_map.json modeling_bailing_moe.py tokenizer.json tokenizer_config.json ../Ling_lite_safetensor/

# Convert Ling lite base
python /home/HwHiAiUser/Ascend/Ling/inference/mindie/convert_bin_to_safetensor_base.py

cd /home/HwHiAiUser/Ascend/Ling_lite_base
cp README.md configuration.json config.json special_tokens_map.json modeling_bailing_moe.py tokenizer.json tokenizer_config.json ../Ling_lite_base_safetensor/
```

Ling Lite 模型的加载路径改为 '/home/HwHiAiUser/Ascend/Ling_lite_safetensor'，Ling Lite Base 模型的路径改为 '/home/HwHiAiUser/Ascend/Ling_lite_base_safetensor'

##### 修改模型配置

mindie 无法直接加载默认的模型配置文件（config.json），需要修改：

```bash
# Adapt to mindie's Ling lite model configuration
cp /home/HwHiAiUser/Ascend/Ling_lite_safetensor/config.json /home/HwHiAiUser/Ascend/Ling_lite_safetensor/config.json.bak
cp /home/HwHiAiUser/Ascend/Ling/inference/mindie/lite/model_chat_config.json /home/HwHiAiUser/Ascend/Ling_lite_safetensor/config.json
chmod 750 /home/HwHiAiUser/Ascend/Ling_lite_safetensor/config.json

# Adapt to mindie's Ling lite base model configuration
cp /home/HwHiAiUser/Ascend/Ling_lite_base_safetensor/config.json /home/HwHiAiUser/Ascend/Ling_lite_base_safetensor/config.json.bak
cp /home/HwHiAiUser/Ascend/Ling/inference/mindie/lite/model_base_config.json /home/HwHiAiUser/Ascend/Ling_lite_base_safetensor/config.json
chmod 750 /home/HwHiAiUser/Ascend/Ling_lite_base_safetensor/config.json

# Adapt to mindie's Ling plus model configuration
cp /home/HwHiAiUser/Ascend/Ling_plus/config.json /home/HwHiAiUser/Ascend/Ling_plus/config.json.bak
cp /home/HwHiAiUser/Ascend/Ling/inference/mindie/plus/model_chat_config.json /home/HwHiAiUser/Ascend/Ling_plus/config.json
chmod 750 /home/HwHiAiUser/Ascend/Ling_plus/config.json

# Adapt to mindie's Ling plus base model configuration
cp /home/HwHiAiUser/Ascend/Ling_plus_base/config.json /home/HwHiAiUser/Ascend/Ling_plus_base/config.json.bak
cp /home/HwHiAiUser/Ascend/Ling/inference/mindie/plus/model_base_config.json /home/HwHiAiUser/Ascend/Ling_plus_base/config.json
chmod 750 /home/HwHiAiUser/Ascend/Ling_plus_base/config.json
```

执行 mindie 适配 Ling 模型的 shell 脚本：

```bash
bash /home/HwHiAiUser/Ascend/Ling/inference/mindie/patch_atb_llm.sh
```

#### 单机服务化推理（Ling lite）

设置底层环境变量：

```bash
source /usr/local/Ascend/atb-models/set_env.sh
```

根据模型类型设置不同的 mindie 配置：

```bash
# Ling Lite
cp /home/HwHiAiUser/Ascend/Ling/inference/mindie/lite/config.json /usr/local/Ascend/mindie/latest/mindie-service/conf/config.json

# Ling Lite base
cp /home/HwHiAiUser/Ascend/Ling/inference/mindie/lite/config.base.json /usr/local/Ascend/mindie/latest/mindie-service/conf/config.json
```

启动 mindie 服务：

```bash
chmod 640 /usr/local/Ascend/mindie/latest/mindie-service/conf/config.json

cd $MIES_INSTALL_PATH
nohup ./bin/mindieservice_daemon > /tmp/service.log 2>&1 &
```

检查 /tmp/service.log，查看输出是否为 Daemon start success!，如果是，则说明 MindIE-Service 已启动成功。

测试请求是否正确：

```bash
# Chat model
wget -O- --post-data="{\"messages\":[{\"role\": \"system\", \"content\": \"You are a helpful assistant.\"}, {\"role\": \"user\", \"content\": \"Who are you?\"}], \"stream\": false, \"max_tokens\":100, \"model\": \"bailing_moe\", \"temperature\":0}" \
--header='Content-Type:application/json' \
'http://127.0.0.1:1025/v1/chat/completions'

# base model

wget -O- --post-data='{"inputs":"My name is Olivier and I","stream":false,"parameters":{"temperature":1,"max_new_tokens":100,"do_sample":false}}' \
--header='Content-Type:application/json' \
'http://127.0.0.1:1025/infer'
```

#### 多机服务化推理（Ling plus）

以下所有命令都需要在所有机器上同时执行。

要启用多机服务化推理，需要配置多机 ranktable 文件。

- 获取每张卡的 IP 地址（在主机上）

```bash
for i in {0..7}; do hccn_tool -i $i -ip -g; done
```

- 按以下格式配置 'rank_table.json'，并放入 '/root/models'，以便挂载到容器

```json
{
"server_count": "...", # Total number of nodes
# The first server in the server_list is the primary node
"server_list": [
{
"device": [
{
"device_id": "...", # The number of the current card, the value range is [0, the number of cards in the machine)
"device_ip": "...", # The IP address of the current card, which can be obtained by hccn_tool command
"rank_id": "..." # The global number of the current card, the value range is [0, total number of cards)
},
...
],
"server_id": "...", # IP address of the current node
"container_ip": "..." # The IP address of the container (required for service-based deployment) is the same as that of the server_id unless otherwise configured
},
...
],
"status": "completed",
"version": "1.0"
}
```

进入容器并运行以下命令：

```bash
# Set the basic environment variables:
source /home/HwHiAiUser/Ascend/Ling/inference/mindie/set_env.sh
# Enable communication environment variables
export ATB_LLM_HCCL_ENABLE=1
export ATB_LLM_COMM_BACKEND="hccl"
export HCCL_CONNECT_TIMEOUT=7200
export WORLD_SIZE=16
export HCCL_EXEC_TIMEOUT=0

# Configure virtual memory environment variables
export PYTORCH_NPU_ALLOC_CONF=expandable_segments:True #开启
# Fixed the issue of slow weight loading

export OMP_NUM_THREADS=1


export RANKTABLEFILE=/home/HwHiAiUser/Ascend/rank_table.json
chmod 640 /home/HwHiAiUser/Ascend/rank_table.json

# To serve, you need to configure the 'container_ip' field in 'ranktable.json', and the configuration of all machines should be consistent, except for the MIES_CONTAINER_IP of the environment variable is the local IP address.
export MIES_CONTAINER_IP=IP address of the container

```

根据模型类型设置不同的 mindie 配置：

```bash
# Ling plus
cp /home/HwHiAiUser/Ascend/Ling/inference/mindie/plus/config.json /usr/local/Ascend/mindie/latest/mindie-service/conf/config.json

# Ling plus base
cp /home/HwHiAiUser/Ascend/Ling/inference/mindie/plus/config.base.json /usr/local/Ascend/mindie/latest/mindie-service/conf/config.json
```

修改服务化参数：

```bash
cd /usr/local/Ascend/mindie/latest/mindie-service/
vim conf/config.json
# The following configurations need to be changed

# "ipAddress" : "Change to primary node IP",
# "managementIpAddress" : "Change to primary node IP",
```

设置内存使用比例：

```bash
export NPU_MEMORY_FRACTION=0.95
```

拉起服务化：

```bash
cd $MIES_INSTALL_PATH
nohup ./bin/mindieservice_daemon > /tmp/service.log 2>&1 &
```

命令执行时会先打印本次启动使用的所有参数，然后直到出现以下输出：

`Daemon start success!`

即认为服务启动成功。

测试请求是否正确：

```
# Chat model
wget -O- --post-data="{\"messages\":[{\"role\": \"system\", \"content\": \"You are a helpful assistant.\"}, {\"role\": \"user\", \"content\": \"Who are you?\"}], \"stream\": false, \"max_tokens\":100, \"model\": \"bailing_moe\", \"temperature\":0}" \
--header='Content-Type:application/json' \
'http://<Change to primary node IP>:1025/v1/chat/completions'

# base model

wget -O- --post-data='{"inputs":"My name is Olivier and I","stream":false,"parameters":{"temperature":1,"max_new_tokens":100,"do_sample":false}}' \
--header='Content-Type:application/json' \
'http://<Change to primary node IP>:1025/infer'
```

## 微调

我们推荐使用 [Llama-Factory](https://github.com/hiyouga/LLaMA-Factory) 对 Ling 进行 SFT、DPO 等微调。

我们使用 [`identity`](https://github.com/hiyouga/LLaMA-Factory/blob/main/data/identity.json) 演示如何微调 Ling 模型：将 `name` 替换为 `Ling`，`author` 替换为 `inclusionAI`。

```json
{
  "instruction": "hi",
  "input": "",
  "output": "Hello! I am Ling, an AI assistant developed by inclusionAI. How can I assist you today?"
}
```

我们提供如下 `Llama-Factory` 的 SFT Ling 模型示例配置：

```bash
llamafactory-cli train examples/sft/ling_full_sft.yaml
```

## 许可证

本代码仓库基于 [MIT License](https://github.com/inclusionAI/Ling/blob/master/LICENCE) 授权。

## 引用

如果你觉得我们的工作有帮助，欢迎引用我们。

```
@article{ling,
    title   = {Every FLOP Counts: Scaling a 300B Mixture-of-Experts LING LLM without Premium GPUs}, 
    author  = {Ling Team},
    journal = {arXiv preprint arXiv:2503.05139},
    year    = {2025}
}
```
