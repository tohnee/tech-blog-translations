---
title: "服务地理空间、视觉与更多：在 vLLM 中启用多模态输出处理"
title_en: "Serving Geospatial, Vision, and Beyond: Enabling Multimodal Output Processing in vLLM"
source: https://vllm.ai/blog/2025-09-05-beyond-text-generation
crawled: 2026-09-12
translated: 2026-09-13
---

# 服务地理空间、视觉与更多：在 vLLM 中启用多模态输出处理

> 原文：[Serving Geospatial, Vision, and Beyond: Enabling Multimodal Output Processing in vLLM](https://vllm.ai/blog/2025-09-05-beyond-text-generation) · vLLM 博客

作者：Christian Pinto（IBM Research Europe - Dublin）、Michele Gazzetti（IBM Research Europe - Dublin）、Michael Johnston（IBM Research Europe - Dublin）、Maximilien Philippe Marie de Bayser（IBM Research - Brazil）

[#多模态](https://vllm.ai/blog/tags/multimodal)

## 简介

直到最近，生成式 AI 基础设施一直与自回归文本生成模型紧密耦合——这类模型逐 token 产出输出，通常以自然语言的形式。vLLM 一直顺应这一趋势，最初支持文本输入、文本输出的模型，即传统的 LLM。随着 MLLM（多模态大语言模型）的引入——它们能够对文本以及各种模态的数据（例如图像、视频、音频等）进行推理——趋势开始转向多模态数据。vLLM 再次顺应趋势，支持了 LLaVA 风格的 MLLM，对多模态输入数据推理并生成文本。

我们现在正目睹新一轮趋势转变：一类日益壮大的非自回归模型，能够在单次推理中生成多模态输出，让跨多种模态的生成更快、更高效。从推理的角度看，这些模型可以被视作池化（pooling）模型，但它们需要额外的输入和输出处理支持。这类模型的应用可以拓展到文本之外的领域：从图像分类与分割，到音频合成与结构化数据生成。
我们已经在 vLLM 中迈出了下一步，为这一类模型添加了支持。

我们最初的集成聚焦地理空间基础模型——一类卷积或视觉 transformer 模型，它们需要 RGB 通道之外的数据（例如多光谱或雷达）以及元数据（例如地理位置、图像采集日期），用于（但不限于）灾害响应或基于卫星图像的土地利用分类等任务。不过，这些改动是通用的，为服务各种非文本生成模型铺平了道路。

作为一个具体例子，我们通过一个通用后端，把 [TerraTorch](https://github.com/IBM/terratorch) 框架中的所有地理空间模型（其中一些是与 NASA 和 ESA 合作开发的）集成到了 vLLM 中，使它们成为 vLLM 生态中的一等公民。

在接下来的章节中，我们将描述对 vLLM 所做的技术改动，从服务地理空间基础模型的需求与挑战讲起。

## 在 vLLM 中集成地理空间基础模型

与文本模型不同，地理空间基础模型（通常实现为视觉 transformer）不需要 token 解码，即不需要把输出 token 转换成文本。
相反，给定一张输入图像，单次推理即可生成原始模型输出，然后再后处理成输出图像。
此外，有时输入图像需要被切分并批处理成若干子图像，即 patch（图块）。
这些 patch 被送入模型推理，随后把每个 patch 得到的输出图像拼接在一起，构成最终的输出图像。

![](https://vllm.ai/blog-assets/figures/beyond-text/models-diff.png)

鉴于这些需求，显而易见的选择是把地理空间基础模型作为池化（pooling）模型集成到 vLLM 中。池化是深度学习模型中常用的一种技术，用于降低特征图的空间维度。常见类型包括最大池化、平均池化和全局池化，各自采用不同的策略聚合信息。在 vLLM 中，池化可用于[嵌入向量计算与分类等任务](https://docs.vllm.ai/en/latest/models/pooling_models.html?h=pooling)。此外，vLLM 支持恒等池化器（identity pooler），直接返回模型的隐藏状态而不做任何变换——这正是我们需要的。
在输入侧，我们把图像预处理成张量再送入模型推理，利用 vLLM 现有的多模态输入能力。

由于我们希望开箱即用地支持多个地理空间基础模型，我们还按照与 HuggingFace Transformers 库后端相同的模式，为 TerraTorch 模型添加了一个模型实现后端。

不过，让这一切跑通并非易事。
启用这些模型类别需要改动 vLLM 的多个部分，例如：

- 为无注意力（attention free）的模型添加支持
- 改进对不需要分词器的模型的支持
- 支持处理原始输入数据，而不是默认的多模态输入嵌入
- 扩展 vLLM 服务 API。

## 认识 IO Processor：面向任意模型的灵活输入/输出处理

到目前为止一切顺利！不过，这只是让我们走完了一半的路。

通过上述集成，我们确实可以服务地理空间基础模型了——但只能以张量对张量的形式。
用户仍需先把图像预处理成张量格式，再把张量发送给 vLLM 实例。
同样，原始张量输出的后处理也必须在 vLLM 之外完成。
其影响是：不存在这样一个端点——用户把图像发过去，就能拿回一张图像。

这个问题之所以存在，是因为在我们的改动之前，vLLM 对输入数据的预处理和模型输出的后处理只有部分支持。
具体来说，多模态输入数据的预处理只能通过 Transformers 库中提供的处理器完成。
然而 transformers 处理器通常只支持标准数据类型，无法处理更复杂的数据格式，例如 GeoTIFF——一种带有丰富地理空间元数据的图像文件。
而在输出处理方面，vLLM 只支持反分词（de-tokenization）成文本，或对模型隐藏状态应用池化器——无法进行其他输出处理。

这正是我们引入的全新 IO Processor 插件框架的用武之地。
IO Processor 框架允许开发者自定义模型输入与输出的预处理和后处理方式，且全部发生在同一个 vLLM 服务实例内。
无论你的模型返回字符串、JSON 对象、图像张量还是自定义数据结构，IO Processor 都能在返回客户端之前把它转换成所需的格式。

![](https://vllm.ai/blog-assets/figures/beyond-text/io-plugins-flow.png)

IO Processor 框架为 vLLM 用户解锁了新层次的灵活性。
它意味着非文本模型（例如图像生成器、图像到分割掩码、表格到分类等）可以用标准 vLLM 基础设施来服务。
借助 IO Processor，用户可以插入自定义逻辑来转换或丰富输出，例如把模型输出解码成图像，或为下游系统格式化响应。
这保持了统一的服务技术栈，降低运维复杂度并提升可维护性。

### 使用 vLLM IO Processor 插件

每个 IO Processor 插件都实现一个预定义的 [IO Processor 接口](https://github.com/vllm-project/vllm/blob/main/vllm/plugins/io_processors/interface.py)，并位于 vLLM 源代码树之外。
安装时，每个插件会在 `vllm.io_processor_plugins` 组中注册一个或多个 entrypoint。
这使 vLLM 能够在引擎初始化时自动发现并加载插件。

使用 IO Processor 插件非常简单：把它安装到与 vLLM 相同的 Python 环境中，并在启动服务实例时添加 `--io-processor-plugin <plugin_name>` 参数即可。
目前，每个 vLLM 实例可以加载一个 IO Processor 插件。

服务实例启动后，在服务 `/pooling` 端点时，预处理和后处理会自动应用于模型输入和输出。
现阶段 IO Processor 仅可用于池化模型，但未来我们预计会有其他端点接入。

## 一步步实战：在 vLLM 中服务 Prithvi 模型

可以通过 TerraTorch 后端在 vLLM 中服务的一类模型示例是[用于洪水检测的 Prithvi](https://huggingface.co/ibm-nasa-geospatial/Prithvi-EO-2.0-300M-TL-Sen1Floods11)。Prithvi 地理空间基础模型的完整插件示例可在[这里](https://github.com/christian-pinto/prithvi_io_processor_plugin)获取。

### Prithvi IO Processor 插件

为了展示 IO Processor 插件方法的灵活性，下面的伪代码展示了 Prithvi IO Processor 预处理与后处理的主要步骤。我们想强调的是数据相关的变换与模型推理数据之间的解耦。这为理想的任意模型、任意输入/输出数据类型留出了空间，甚至可以让多个插件应用于同一个模型输出，取决于消费数据的下游任务。

```
def pre_process(request_data: dict):
    # Downloads geotiff
    # In this example the input image has 7 bands
    image_url = request_data["url"]
    image_obj = download_image(image_url)

    # Extract image data:
    # - pixel_values([n, 6, 512, 512])
    #   - 6 input bands R, G, B, +3 multispectral wavelengths
    #   - n > 1 if the size of the input image is > [512, 512]
    # - metadata
    #   - GPS coordinates
    #   - date
    pixel_values, metadata = process_image(image_obj)

    # Process the image data into n vLLM prompts
    model_prompts = pixels_to_prompts(pixel_values)

    return model_prompts


def post_process(model_outputs: list[PoolingRequestOutput]):
    # Uses the previously extracted metadata to guarantee the output
    # contains the same georeferences and date.
    return image_object(model_outputs, metadata)
```

### 安装 Python 依赖

在你的 Python 环境中安装 `terratorch`（>=1.1rc3）和 `vllm` 包。
在撰写本文时，复现此示例所需的改动尚未包含在 vLLM 发行版中（当前最新版本为 v0.10.1.1），我们建议用户安装[最新代码](https://docs.vllm.ai/en/latest/getting_started/installation/gpu.html#install-the-latest-code_1)。

下载并安装用于 Prithvi 洪水检测的 IO Processor 插件。

```
git clone git@github.com:christian-pinto/prithvi_io_processor_plugin.git
cd prithvi_io_processor_plugin
pip install .
```

这会安装 `prithvi_to_tiff` 插件。

### 启动 vLLM 服务实例

启动一个加载 `prithvi_to_tiff` 插件与 Prithvi 洪水检测模型的 vLLM 服务实例。

```
vllm serve \
    --model=ibm-nasa-geospatial/Prithvi-EO-2.0-300M-TL-Sen1Floods11 \
    --model-impl terratorch \
    --task embed --trust-remote-code \
    --skip-tokenizer-init --enforce-eager \
    --io-processor-plugin prithvi_to_tiff
```

实例运行起来之后，就可以用选定的插件服务请求了。
下面的日志条目确认你的 vLLM 实例已启动并正在监听 `8000` 端口。

```
INFO: Starting vLLM API server 0 on http://0.0.0.0:8000
...
...
INFO: Started server process [409128]
INFO: Waiting for application startup.
INFO: Application startup complete.
```

### 向模型发送请求

下面的 Python 脚本向 vLLM `/pooling` 端点发送一个请求，其中 JSON 载荷的 `model` 与 `softmax` 参数是预定义的，而 `data` 字段由用户定义并取决于所用的插件。

> \*\*注意：\*\*必须把 `softmax` 字段设为 `False`，以确保插件收到的是原始模型输出。
> 在本例中，我们把输入图像以 URL 的形式发送给 vLLM，并要求响应为 base64 编码的 GeoTIFF 图像。
> 脚本解码图像并将其以 tiff（GeoTIFF）文件写入磁盘。

```
import base64
import os
import requests

def main():
  image_url = "https://huggingface.co/christian-pinto/Prithvi-EO-2.0-300M-TL-VLLM/resolve/main/valencia_example_2024-10-26.tiff"
  server_endpoint = "http://localhost:8000/pooling"

  request_payload = {
      "data": {
          "data": image_url,
          "data_format": "url",
          "image_format": "tiff",
          "out_data_format": "b64_json",
      },
      "model": "ibm-nasa-geospatial/Prithvi-EO-2.0-300M-TL-Sen1Floods11",
      "softmax": False,
  }

  ret = requests.post(server_endpoint, json=request_payload)

  if ret.status_code == 200:
    response = ret.json()

    decoded_image = base64.b64decode(response["data"]["data"])

    out_path = os.path.join(os.getcwd(), "online_prediction.tiff")

    with open(out_path, "wb") as f:
        f.write(decoded_image)
  else:
    print(f"Response status_code: {ret.status_code}")
    print(f"Response reason:{ret.reason}")


if __name__ == "__main__":
    main()
```

下面是输入与预期输出的示例。
输入图像（左）是 2024 年洪水期间西班牙瓦伦西亚的卫星图片。
输出图像（右）显示了 Prithvi 模型预测为被洪水淹没的区域（白色）。

![](https://vllm.ai/blog-assets/figures/beyond-text/prithvi-prediction.png)

## 下一步计划

这只是开始。
我们计划把 IO Processor 插件扩展到更多 TerraTorch 模型与模态乃至更广的范围，并让安装无缝顺畅。
更长远地，我们期待由 IO Processor 驱动的视觉-语言系统、结构化推理智能体以及多模态流水线，全部由同一个 vLLM 技术栈服务。我们也期待看到社区如何使用 IO Processor 推动 vLLM 能力的边界。
我们还计划继续与 vLLM 社区合作并为其做贡献，启用更多的多模态模型与端到端用例。

**随时欢迎贡献、反馈与想法！**

要开始使用 IO Processor 插件，请查阅[文档](https://docs.vllm.ai/en/latest/design/io_processor_plugins.html)并浏览[示例](https://github.com/vllm-project/vllm/tree/main/examples)。
关于 IBM TerraTorch 的更多信息请见[这里](https://github.com/IBM/terratorch)。

## 致谢

我们感谢 vLLM 社区的成员们为改进我们的贡献提供的帮助。特别感谢 [Cyrus Leung](https://github.com/DarkLight1337) 在帮助我们塑造"将 vLLM 拓展到文本生成之外"这一整体概念上的支持。最后，我们感谢 IBM 的 TerraTorch 团队，尤其是 [Paolo Fraccaro](https://github.com/paolo-fraccaro) 与 [Joao Lucas de Sousa Almeida](https://github.com/Joao-L-S-Almeida)，感谢他们在将通用 TerraTorch 后端集成进 vLLM 方面提供的帮助。
