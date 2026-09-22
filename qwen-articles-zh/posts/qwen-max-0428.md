---
title: "Qwen-Max-0428模型介绍"
date: 2024-05-11
source: https://qwenlm.github.io/blog/qwen-max-0428/
crawled: 2026-09-22
zh_source: official（官方中文版，非翻译）
---
{{< button href="https://dashscope.aliyun.com" label="API" external=true >}}
{{< button href="https://huggingface.co/spaces/Qwen/Qwen-Max-0428" label="DEMO" external=true >}}
{{< button href="https://discord.gg/yPEP2vHTu4" label="DISCORD" external=true >}}

此前，我们开源了Qwen1.5系列的模型，参数规模最小至5亿，最大至1100亿。这一次，我们推出更大规模模型Qwen-Max-0428（通义千问网页端及APP产品版本从2.1升级至2.5）。Qwen-Max-0428是经过指令微调的Chat模型。近期该模型登陆了[Chatbot Arena](https://chat.lmsys.org/)，并登榜前十。此外，我们在MT-Bench的评测上也观察到该模型的表现显著优于Qwen1.5-110B-Chat。

{{< figure src="https://qianwen-res.oss-cn-beijing.aliyuncs.com/arena_leaderboard.jpg#center" width="100%">}}

<table>
    <tr>
        <th rowspan="1" align="center">Models</th>
        <th colspan="1" align="center">MT-Bench</th>
        <th colspan="1" align="center">Arena</th>
    </tr>
    <tr>
        <td>Qwen1.5-110B-Chat</td>
        <td align="center">8.88</td>
        <td align="center">1172</td>
    </tr>
    <tr>
        <td>Qwen-Max-0428</td>
        <td align="center">8.96</td>
        <td align="center">1186</td>
    </tr>
</table>

我们也在Hugging Face上提供了Demo服务（[链接](https://huggingface.co/spaces/Qwen/Qwen-Max-0428)）：

<iframe
	src="https://qwen-qwen-max-0428.hf.space"
	frameborder="0"
	width="850"
	height="1000"
></iframe>

同时我们也提供了DashScope API服务（[链接](https://dashscope.aliyun.com)）。目前API服务已经支持OpenAI API格式，示例如下所示：

```python
from openai import OpenAI

client = OpenAI(
    api_key="$your-dashscope-api-key",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

completion = client.chat.completions.create(
    model="qwen-max",
    messages=[{'role': 'system', 'content': 'You are a helpful assistant.'},
              {'role': 'user', 'content': 'Tell me something about large language models.'}]
)
print(completion.choices[0].message)
```

此外，Qwen-Max-0428已上线通义千问网页端及APP。欢迎体验！

# 引用

```
@misc{qwen1.5,
    title = {Introducing Qwen1.5},
    url = {https://qwenlm.github.io/blog/qwen1.5/},
    author = {Qwen Team},
    month = {February},
    year = {2024}
}
```
