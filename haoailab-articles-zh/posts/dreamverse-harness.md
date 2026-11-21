---
title: "FastVideo Dreamverse Harness：本地优先的 AI 电影制作，就在你自己的 GPU 上"
title_en: "FastVideo Dreamverse Harness: Local-First AI Filmmaking on Your Own GPUs"
date: 2026-11-19
source: https://haoailab.com/blogs/dreamverse-harness/
crawled: 2026-11-21
translated: 2026-11-21
---

# FastVideo Dreamverse Harness：本地优先的 AI 电影制作，就在你自己的 GPU 上

> 原文：[FastVideo Dreamverse Harness: Local-First AI Filmmaking on Your Own GPUs](https://haoailab.com/blogs/dreamverse-harness/) · Hao AI Lab @ UCSD

2026 年 11 月 19 日 · 14 分钟 · FastVideo 团队

今天我们正式开源 **Dreamverse Harness**——一个构建于 [FastVideo](https://github.com/hao-ai-lab/FastVideo) 之上的智能体 harness（执行框架），它把本地视频生成从单个片段推进到完整影片。

**上手体验：**[GitHub](https://github.com/fastvideo-project/dreamverse-harness) · [Slack](https://join.slack.com/t/fastvideo/shared_invite/zt-4heayzk81-lOkgpvJRoceuZjNP7pXxJA) · [Discord](https://discord.gg/dqc2J2yNQ)

[![
你的浏览器不支持带音频的 MP4 视频。](media/intro-poster.jpg)](media/intro.mp4)

## **从单个片段生成到电影制作**[#](#from-single-clip-generation-to-film-production)

有了 [FastVideo](https://github.com/hao-ai-lab/FastVideo) 与 [FastH3](https://huggingface.co/FastVideo/FastH3-Omni-NVFP4-QAD)，在你自己的 GPU 上生成单个视频片段比以往任何时候都快。然而，一部影片远不止一个片段。它需要剧本、跨镜头保持一致的角色，以及最终的成片——这些事情视频模型无法独立完成。

如今，Higgsfield⁹、Runway¹⁰、TapNow¹¹ 这样的云端 AIGC 工作室可以制作完整影片，但整套技术栈都由它们托管，因此每次生成都要支付点数加价，而不是跑在你自己的硬件上。自定义也止步于界面：你可以调整预设、从它们托管的模型中选择，却无法修改智能体的逻辑，也无法接入自己的模型。

开源项目已经开始着手这个问题，但每一个都只覆盖了一半。一些项目只能跑在你自己的 GPU 上，模型是一组固定的本地模型¹˒²；另一些可以执导整部影片，却只能通过付费的云端 API 实现³˒⁴。我们构建 FastVideo Dreamverse Harness 正是为了填补这一空白：一个完全开源的 harness，构建于 FastVideo 之上，并对你接入的任何模型开放。

## **FastVideo Dreamverse Harness 能做什么**[#](#what-fastvideo-dreamverse-harness-does)

Dreamverse Harness 是一个由你和智能体共同搭建影片的工作空间。它不把生成过程藏在单一聊天框之后，而是把智能体连接到承载素材的可视化画布和承载最终成片的时间线上——让你在影片逐步成形的过程中，能看到并编辑每一个组成部分。

**把任何模型接入你的工作流。**Dreamverse Harness 自带一个运行 [FastH3](https://huggingface.co/collections/FastVideo/fastvideo-fasth3) 的 FastVideo 服务器，既可以部署在远程集群上，也可以本地跑在 [DGX Spark](https://haoailab.com/blogs/fasth3-omni-local/) 上。要接入另一个本地模型或 API，你只需编写一个 provider 插件，或者让编程智能体用内置的 dv-add-model-provider 技能替你写好。

**一个具备执导能力的智能体。**Dreamverse Harness 为智能体配备了结构化的导演技能、领域专属提示词，以及一套让它掌控整部影片的专用工具集——从拆解剧本、锁定角色参考，到跨模型调度镜头。

![画布上打开的分镜（Storyboard）笔记，旁边是聊天中智能体的第一版镜头计划](img/plan-storyboard.png)

**交互式执导。**输入一句话然后期待成品电影自动产出，对真实项目从来行不通；而缓慢、昂贵的视频模型过去也让来回迭代变得不现实。Dreamverse Harness 同时解决了这个循环的两端。其一，FastH3 以低成本在数秒内完成渲染，你可以立刻观看一个镜头并顺势调整下一个；其二，每个角色、场景资产和每条镜头片段（take）都存放在共享画布与时间线上——你与智能体可以一起调整机位、重新生成单个镜头，或者重新剪辑整个序列，而不必从头重新生成。

![聊天中的请求，两张 Nailong 图片是唯一的参考](img/chat-request.png)![画布，从左到右：笔记、两张图片、Nailong 角色与六个已渲染镜头](img/canvas-nodes.png)![时间线停在六个镜头中的第 3 个镜头](img/timeline.png)

**一切都是插件。**Dreamverse Harness 构建在 [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness)⁵ 之上，把技术栈的每一部分都当作模块化插件。你可以移除不需要的功能，直接调整喂给智能体的技能与上下文，也可以构建并分发你自己的自定义画布节点和 UI 可视化。

**运行于 DGX Spark：本地或云端皆可。**Dreamverse Harness 运行在 NVIDIA DGX Spark——配备 128 GB 统一内存的 GB10 Grace Blackwell 桌面级设备——之上。在单台 DGX Spark 上，整套技术栈完全本地运行：NVFP4 版 Qwen 3.8 27B 充当智能体的 LLM，FastH3 渲染视频，剧本、参考素材和镜头片段都不会离开这台机器。本地是默认选项，而非硬性要求。云端 LLM 或远程 FastVideo 服务器只是同一个目录中的又一条条目：你可以用更大的云端模型执导、而视频留在你的 Spark 上，可以在本地服务器旁添加远程渲染服务器，也可以从一台 DGX Spark 扩展到两台、三台乃至四台。最多四台可以通过 QSFP 线缆直连而无需交换机，harness 对所有这些组合一视同仁。

1 台 Spark
2 台 Spark
3 台 Spark
4 台 Spark

[![
你的浏览器不支持 MP4 视频。](media/spark-1-spark-poster.jpg)](media/spark-1-spark.mp4)

1 台 DGX Spark，完全本地：Qwen 3.8 27B 与 FastH3 共用一台机器

**内置 FastVideo，为 DGX Spark 深度调优。**Dreamverse Harness 把 FastVideo 作为原生视频后端一并交付，而 FastVideo 对 GB10 的调优深入到 kernel 层面。每个 FastH3 模型（V1、V2、Trim 与 Omni）以及 Pika H3 Flex⁶ 都提供面向 Blackwell 的 NVFP4 构建，并运行在 GB10 kernel 上：融合的 NVFP4 矩阵乘法、稀疏视频注意力以及 NVFP4 视频解码器。收益层层叠加。FastH3 首次跑在 DGX Spark 上时，一段五秒的片段需要 243 秒；如今，五秒 480p 带音频视频在单台 Spark 上约 33 秒完成渲染，两台则约 19 秒。这样一来，一台 DGX Spark 既可以同时容纳智能体的 LLM 和一个 FastH3 模型，也可以并排放两个 FastH3 模型，智能体会根据影片需要在各模型之间切换。

**经由智能体实现硬件感知的控制。**在新的 Hardware 设置页上添加每台 Spark，智能体就能看到每一台设备：是否可达、是否忙碌、装载了哪些模型。它会把每个片段放到一台装有对应模型的空闲 Spark 上，优先选择模型已加载的那台，并并行渲染相互独立的片段。它会自行在各设备上加载和卸载模型，而你在 Generation models 页面上也保有同样的控制权。

[![
你的浏览器不支持 MP4 视频。](media/spark-4-sparks-switch-poster.jpg)](media/spark-4-sparks-switch.mp4)

200G 交换机上的 4 台 DGX Spark：智能体并行渲染四个镜头，随后四台 Spark 共同拆分每一次 2K 超分

**将视频超分至 2K。**我们把 NVlabs 的 Open-H3-Regenerate-2K⁷——它以 2560×1440 分辨率重新生成初稿——适配到了 DGX Spark。它在 GB10 上以稀疏注意力、MXFP8 矩阵乘法和更轻量的 24 层解码器运行，并把每个片段拆分到两台通过线缆连接的 Spark 上。这些优化合在一起，把双 DGX Spark 上的 2K 重新生成从 454 秒缩短到 158 秒。智能体会把你保留的镜头片段作为 V2V 任务发送给超分器；在三台或更多 Spark 时，其余 Spark 继续用 FastH3 生成初稿，而其中一对负责以 2K 重新生成保留片段。

## **Harness 的工作原理**[#](#how-the-harness-works)

Dreamverse Harness 构建在 [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) 之上，运行于其插件系统与智能体循环。Dreamverse Harness 添加的一切都是插件，且插件之间只存在单向依赖。图 1 自下而上展示了由此形成的各层。项目层记录一个项目的完整生命周期；其上的模型生成层保存模型目录与为模型提供服务的 provider；特性层则保存影片的各个组成部分，例如角色、场景、镜头渲染与时间线；在顶层，诸如 story 工作流这样的工作流把这些特性组合成一条生产流程。此外，每个插件都随附技能，告诉智能体如何使用它。

智能体并不是多出来的一层：它贯穿所有层，从工作流到特性与模型。它遵循视频执导技能（video-directing skill）来规划一部影片，并通过插件提供的工具来执行操作。例如，当一个镜头需要渲染时，智能体会从目录中挑选模型，并遵循该模型的提示词技能（prompting skill）。在做任何改动之前，它都会先读取项目历史，了解已经做过什么。

![图 1 · Dreamverse 插件分层；右侧虚线框是插件随附的技能示例](img/fig1-plugin-layers-v2.png)

图 1 · Dreamverse 插件分层；右侧虚线框是插件随附的技能示例

### **1. 项目层：一部影片的版本控制**[#](#1-the-project-layer-version-control-for-a-film)

与智能体一起制作影片是迭代式的。你试一条镜头片段，与上一条对比，更换一张参考照片，有时还会回退两步。一个只保存当前状态的项目，恰恰会丢失这项工作所依赖的信息。因此我们把项目层设计成影片的版本控制（图 2）。

![图 2 · 项目层：记录历史与带版本的参考](img/fig2-project-layer.png)

图 2 · 项目层：记录历史与带版本的参考

每一次改动——无论你在画布上操作，还是智能体从聊天中执行——都是项目只追加（append-only）日志 records.jsonl 中的一条记录。一条记录会保存是谁做的改动、来自哪个视图、用了哪些输入、产出了什么。项目状态由这些记录计算得出，因此三个视图始终呈现同一个项目。撤销与重做只是沿着历史移动项目的当前位置，不删除任何东西。于是，被撤销的镜头片段仍保留在日志中，你可以回到它，或把它与新的一条对比。

参考素材同样有版本。像 c1 这样的角色从版本 c1@1 开始，当你更换它的照片后变为 c1@2；镜头计划每次修订都会产生新版本。每次渲染都会精确记录它读取了哪些版本。因此，每条镜头片段都能回答它是基于哪张照片、哪个计划生成的。当一条镜头片段读取过的版本被更新版本取代时，该片段会被标记出来，以便你或智能体决定是否重新渲染。

### **2. 生来可组合**[#](#2-composable-by-design)

用于电影制作的 harness 必须能生长。新模型每隔几周就会出现，新的影片类型也会带来需要追踪的新事物。

因此我们把 Dreamverse Harness 围绕注册表（registry）来构建。核心只提供注册表，不点名任何插件；插件通过向注册表注册来加入。在宿主端，项目内核接收组件及其操作，模型注册表接收模型条目；在浏览器端，画布接收节点类型，历史面板与聊天输入框接收各自的行条目与 @ 提及类型。每一次注册都与创建它的插件的生命周期绑定，因此卸载一个插件会移除它添加的一切。

画布是浏览器端最清晰的例子（图 3）。ui-canvas 提供一个节点类型注册表，并绘制其中注册的任何内容。ui-character、ui-shot-plan 这类 UI 插件注册自己的节点类型与编辑器。因此，新增一种节点就是一个新插件，卸载该插件就会把它的节点从画布上移除。

![图 3 · 画布注册表：UI 插件注册节点类型，画布负责绘制它们](img/fig3-canvas-registry.png)

图 3 · 画布注册表：UI 插件注册节点类型，画布负责绘制它们

模型目录在宿主端以同样的方式运作（图 4）。每个 provider 插件为每个模型和任务注册一个条目，镜头渲染插件则按智能体指定的键查找条目。于是，目录与渲染代码都不点名任何 provider，接入一个模型只需新增一个 provider 插件。

![图 4 · 模型目录：provider 注册模型条目，镜头渲染按键查找](img/fig4-model-catalog-v2.png)

图 4 · 模型目录：provider 注册模型条目，镜头渲染按键查找

### **3. 工作流组合组件**[#](#3-workflows-compose-components)

影片的每一个元素——例如角色、场景、风格、镜头计划或时间线——都是一个组件，拥有自己的状态切片与操作，且组件之间互不导入。生产的先后次序放在别处：放在工作流里。Dreamverse Harness 随附的 story 工作流拥有两个操作（图 5）。story.preview 是只读的：它报告哪些镜头会被渲染、GPU 用量估算，以及每一次渲染会被拒绝的原因。story.approve 总是先请求你的确认，然后写入整条链：为每个新增或改动的镜头各写入一次渲染，再写入一次时间线布局。链中的每条记录都带有 started\_by，指向那次确认，因此画布可以把同一次确认产生的镜头片段归为一组，后续的重拍也会留在同一条链里。

![图 5 · story 工作流：先预览，再确认，然后写入一条记录链](img/fig5-story-workflow.png)

图 5 · story 工作流：先预览，再确认，然后写入一条记录链

我们把流程留在组件之外，因为流程各不相同，而元素始终如一。例如，一个以两种画幅比例渲染同一份计划的广告剪辑，需要不同的确认逻辑，但用的是同一个镜头计划与同一个渲染操作。于是，第二个工作流就是一个新软件包，任何组件都不需要改动。

## **上手指南**[#](#getting-started)

Dreamverse Harness 需要两个服务器：一个渲染视频的 FastVideo 服务器，和一个运行智能体的 LLM 端点。

**依赖**

* Node.js ^22.19.0 || >=24.0.0 与 pnpm 11.7.0
* ffmpeg 与 ffprobe
* 一块或多块 NVIDIA GPU，供 FastVideo 服务器使用（默认的 FastH3 8 步配置需要 4 块）
* 一个 OpenAI 兼容的 LLM 端点，供智能体使用（默认模型 id 为 deepseek-v4.1）

**步骤**

1. 启动一个提供 FastH3 的 FastVideo 服务器：

   ```
   uv venv --python 3.12 --seed && source .venv/bin/activate
   git clone https://github.com/hao-ai-lab/FastVideo.git && cd FastVideo
   UV_TORCH_BACKEND=cu130 uv pip install -e ".[fasth3]"
   fastvideo serve --config examples/serving/openai_fasth3_8step.yaml \
     --server.host 127.0.0.1   # port 8000
   ```
2. 获取 Dreamverse Harness 并创建其 profile：

   ```
   git clone https://github.com/fastvideo-project/dreamverse-harness.git dreamverse && cd dreamverse
   pnpm install && pnpm run build
   export DSH_HOME="$HOME/.local/state/dsh-video-harness"
   scripts/video-harness/setup-profile.sh
   ```
3. 将 Dreamverse Harness 指向你的服务器。把下面几行添加到 $DSH\_HOME/profiles/video-harness/cordis.patch.yml：

   ```
   - id: dv-fastvideo
     disabled: false
     config:
       models:
         fasth3:
           t2v:
             baseUrl: http://127.0.0.1:8000
   - id: dv-uniserve
     disabled: true
   ```

   然后导出这些变量：

   ```
   export DV_DEEPSEEK_BASE_URL=[your OpenAI-compatible endpoint, ending in /v1]
   export DV_DEEPSEEK_API_KEY=[your key, or leave unset for a keyless server]
   export DV_FFMPEG="$(command -v ffmpeg)"
   ```
4. 用 scripts/video-harness/launch.sh web 启动 Web UI。它监听 8092 端口；可通过设置 DV\_PORT 更改端口。
5. 打开启动器打印出的 URL，例如 http://127.0.0.1:8092，然后在聊天里描述你的第一个视频。
6. 可选：要接入 OpenRouter 托管的图像与语音模型，请在 Web UI 中打开 Settings → Video, image & audio APIs，保存你的 OpenRouter API key，加载模型目录，并在想要的模型上选择 Add to chat。它们随后会出现在聊天里的模型选择器中。

### **在 DGX Spark 上部署**[#](#set-up-on-dgx-spark)

最快的路径是让编程智能体代劳。在 Codex 或 Claude Code 中安装我们的部署技能，并让它把 Dreamverse 部署到你的 DGX Spark 上：

```
npx skills add fastvideo-project/dreamverse-harness --skill dreamverse-dgx-spark-setup
```

智能体会检查每一台机器，根据你手头的硬件选择模型布局，安装 FastVideo、LLM 与 Dreamverse Harness，并用一次测试渲染逐一验证。想自己动手？仓库中的 DGX Spark 指南列出了每一步，且每步之后都有一次检查。下面的配方就是我们实际运行的部署组合，欢迎自由混搭与扩展。

**单台 DGX Spark，完全本地。**Qwen 3.8 27B（vLLM 下约 39 GB）与 FastH3 Trim（渲染时约 45 GB）共用一台机器：

1. 准备好机器：搭载 CUDA 13 的 DGX OS、至少 120 GB 空闲磁盘、一个 Hugging Face 登录，以及一个内存看门狗——因为内存耗尽可能导致 GB10 冻结。
2. 下载权重：

   ```
   hf download nvidia/Qwen3.8-27B-NVFP4 --local-dir ~/models/Qwen3.8-27B-NVFP4
   hf download FastVideo/FastVideo-FastH3-Trim-8-Step-NVFP4 --local-dir ~/models/FastH3-Trim-8-Step-NVFP4
   ```
3. 用 vLLM 的 nightly CUDA 13 wheel 在 8000 端口提供 Qwen 服务，并用 `--gpu-memory-utilization 0.32` 限制显存占用，以便 FastH3 能与之并存。先启动它，因为首次启动需要编译 kernel。
4. 按照其 [DGX Spark 指南](https://github.com/hao-ai-lab/FastVideo/blob/main/docs/getting_started/installation/spark_performance.md)安装 FastVideo，并使用本地权重从 `examples/serving/openai_fasth3_trim_spark.yaml` 在 18000 端口提供 FastH3 Trim 服务。
5. 构建 Dreamverse Harness，创建其 profile，并编写一个 profile 补丁，把智能体指向 Qwen、把 `dv-fastvideo` 指向 FastH3 Trim。然后用 `scripts/video-harness/launch.sh web` 启动 Web UI，并在 DGX Spark 的浏览器中打开打印出的 URL。

**多台 DGX Spark。**每台 DGX Spark 各自运行一个 FastVideo 服务器，绑定到它的线缆或局域网地址，并带有模型目录（`server.model_catalog`），让智能体可以在其上加载与卸载模型。在 profile 补丁中，为每个模型填上其服务器的 `baseUrl`，并设置 `managed: true`。一个 FastH3 NVFP4 模型占用 40 至 55 GB，因此一台 DGX Spark 能装下两个，或一个与 Qwen 并存。

**2K 跨两台 DGX Spark。**两台通过线缆连接的 DGX Spark 共同运行一个 Open-H3-Regenerate-2K 服务器，通过 Ray 做序列并行（`sp_size: 2`），每台机器负责精修每个片段的一半。

Dreamverse Harness 仓库中的 [DGX Spark 指南](https://github.com/fastvideo-project/dreamverse-harness/blob/main/scripts/video-harness/dgx-spark.md)包含完整命令，且每一步之后都有一次检查。

## **更多用 Dreamverse Harness 制作的示例视频**[#](#more-example-videos-built-with-dreamverse-harness)

一段发生在星舰上的科幻场景。

[![
你的浏览器不支持带音频的 MP4 视频。](media/example-scifi-poster-v2.jpg)](media/example-scifi-v2.mp4)

一段呈现精卫神话的中国水墨动画。

[![
你的浏览器不支持带音频的 MP4 视频。](media/example-jingwei-poster.jpg)](media/example-jingwei.mp4)

一支 NVIDIA DGX Spark 产品广告。

[![
你的浏览器不支持带音频的 MP4 视频。](media/example-spark-ad-poster-v2.jpg)](media/example-spark-ad-v2.mp4)

一部关于真菌的自然纪录片。

[![
你的浏览器不支持带音频的 MP4 视频。](media/example-fungi-poster.jpg)](media/example-fungi.mp4)

把粗糙的 Blender 场景渲染成动作镜头。

[![
你的浏览器不支持带音频的 MP4 视频。](media/example-david-poster.jpg)](media/example-david.mp4)

欢迎在 [Slack](https://join.slack.com/t/fastvideo/shared_invite/zt-4heayzk81-lOkgpvJRoceuZjNP7pXxJA) 或 [Discord](https://discord.gg/dqc2J2yNQ) 上加入我们，或在 [GitHub](https://github.com/fastvideo-project/dreamverse-harness) 上提交 issue。

## **参考文献**[#](#references)

1. WanGP. [github.com/deepbeepmeep/WanGP](https://github.com/deepbeepmeep/WanGP)
2. LTX Desktop. [github.com/Lightricks/LTX-Desktop](https://github.com/Lightricks/LTX-Desktop)
3. OpenMontage. [github.com/calesthio/OpenMontage](https://github.com/calesthio/OpenMontage)
4. ViMax. [github.com/HKUDS/ViMax](https://github.com/HKUDS/ViMax)
5. DeepSeek Harness. [github.com/deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness)
6. Pika H3 Flex. [huggingface.co/Pika-Labs/Pika-H3-Flex](https://huggingface.co/Pika-Labs/Pika-H3-Flex)
7. Open-H3-Regenerate-2K. [huggingface.co/Efficient-Large-Model/Open-H3-Regenerate-2K](https://huggingface.co/Efficient-Large-Model/Open-H3-Regenerate-2K)
8. vLLM-Omni. [github.com/vllm-project/vllm-omni](https://github.com/vllm-project/vllm-omni)
9. Higgsfield. [higgsfield.ai](https://higgsfield.ai)
10. Runway. [runwayml.com](https://runwayml.com)
11. TapNow. [tapnow.ai](https://tapnow.ai)

## **致谢**[#](#acknowledgement)

我们感谢 NVIDIA 提供的算力支持与协作。

## **FastVideo 团队**[#](#fastvideo-team)

**贡献者：** [Aryan Kumar](https://github.com/aryan5v), [Kun Lin](https://github.com/klhhhhh), [Kyle Hu](https://github.com/KyleNeverGivesUp), [Kevin Lin](https://github.com/kevin314), [Loay Rashid](https://github.com/loaydatrain), [Junda Chen](https://github.com/GindaChen), [Ishan Vaish](https://github.com/ivaish)  
**技术负责人：** [Junda Su](https://davids048.github.io/), [Will Lin](https://solitarythinker.github.io/)  
**顾问：** [Hao Zhang](https://haozhang.ai/)
