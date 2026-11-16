---
title: "铁（木）王座：Google 的 TPU 在推理领域宣示主权"
title_en: "The Iron(wood) Throne: Google's TPU Stakes Its Claim on Inference"
subtitle: "CUDA 护城河的可行替代、NVIDIA 夜以继日（含周末）赶工、黄仁勋的反击提交、Kimi K3、Meta Muse Spark Open、GLM5.3、TorchTPU、SGLang、vLLM、llm-d、Ray"
date: 2026-11-05
source: https://newsletter.semianalysis.com/p/tpu-strikes-the-king
crawled: 2026-11-16
authors: ["Bryan Shan", "Alec Ibarra", "Cam Quilici", "Kimbo Chen", "Wenyao Gao", "Dylan Patel", "Myron Xie"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-11-16
---

# 铁（木）王座：Google 的 TPU 在推理领域宣示主权

> 原文：[The Iron(wood) Throne: Google's TPU Stakes Its Claim on Inference](https://newsletter.semianalysis.com/p/tpu-strikes-the-king) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**CUDA 护城河的可行替代、NVIDIA 夜以继日（含周末）赶工、黄仁勋的反击提交、Kimi K3、Meta Muse Spark Open、GLM5.3、TorchTPU、SGLang、vLLM、llm-d、Ray**

2025 年 11 月，我们[发文](https://newsletter.semianalysis.com/p/tpuv7-google-takes-a-swing-at-the)指出 Google 正在向外部客户出售 TPU。此后，Oracle、[OpenAI](https://openai.com/careers/software-engineer-tpu-compilers-san-francisco/)、Anthropic 和 Meta 相继成为 TPU 客户，正如我们的[加速器模型](https://semianalysis.com/accelerator-hbm-model/)所报告的那样，我们被一次又一次证明是对的。

硬件需求只是故事的一半，因为 NVIDIA 的护城河历来在于其软件和庞大的开发者生态。TPU 也正在这一领域取得进展：它与整个生态的上游维护者合作，包括 Meta 的 PyTorch 团队、vLLM（Inferact、RedHat）、SGLang（RadixArk）、llm-d、Ray 等。[对读过我们 2026 年 9 月那篇阐述 Google TPU 外部化战略文章的人来说，这并不意外](https://newsletter.semianalysis.com/p/tpu-inferencex-full-steam)。

在 9 月那篇文章中，我们在 InferenceX 上发布了 TPUv7 在单轮工作负载上的首批第三方结果，显示在 Qwen 3.5 397B 上做同口径 FP8 对比时，TPUv7（Ironwood）的每美元性能最高比 B200 和 B300 好 50%。

我们还报告称，许多 Google TPU 客户在询问 AgentX 结果，因为长上下文、多轮的智能体服务正是推理支出正在流向的方向。

此前，黄仁勋做客 [Dwarkesh 播客](https://www.youtube.com/watch?v=Hrbq66XqtCo)，评论说没有其他芯片利用这个机会在 InferenceX 上展示性能。

![](https://substack-post-media.s3.amazonaws.com/public/images/2155d462-261a-4ab4-95f9-9231e9380d34_3840x2160.png)
*来源：Dwarkesh（Dylan 的表亲）播客*

六个月后，Google 确实在充分利用这个机会。

今天我们发布 TPUv7 在四个模型上的首批官方长上下文、多轮、真实智能体推理基准结果，显示 TPUv7 在外部客户的每美元性能上要么具备竞争力，要么交付最佳 SOTA 结果：

- **Muse Spark Open SGLang AgentX（NVFP4 权重）：** 尽管该架构是为 GPU 协同设计的，TPU 的每美元性能仍具竞争力。由开源生态开发者 RadixArk（SGLang 的开发者）提交。

- **GLM-5.2 vLLM AgentX（FP8）：** TPUv7 是最便宜的 FP8 选项，在 60 至 300 tok/s/user 区间内，每美元 token 数达到 B200、B300 和 MI355X 的 1.2 倍至 2.7 倍。NVIDIA NVFP4 仍可击败 TPUv7 FP8，但伴随精度/质量损失。
- **Qwen3.5 vLLM AgentX（FP8）：** 借助 llm-d 分离式服务，TPUv7 在每个交互性水平上都击败 GB300 FP8，并以更高的质量/精度在与 GB300 FP4 的对比中恢复平价。
- **Kimi K3 vLLM AgentX（MXFP4 权重）：** 发布时与 GB300 NVL72 具竞争力；TPUv7 的每美元 token 数达到 GB200、B200、B300 和 MI355X 的 1.15 倍至 2.5 倍。由 vLLM 开源生态开发者 Inferact 提交。

该基准在 InferenceX/AgentX 上完成，这是行业标准的推理基准，几乎得到所有主要算力买家的支持——从 Microsoft Azure 到 Oracle 再到 Meta 以及更多。此外，它还获得 ML 社区的支持，包括 vLLM、LMCache、SGLang、PyTorch 和 Huggingface，以及 OpenAI、MiniMax、ZAI、Qwen、Moonshot Kimi 等主要实验室的支持。

Google 的潜在 TPU 客户和现有 TPU 客户都在向 Google 索要 AgentX 结果，因为 AgentX 基准非常贴近现实，与他们真实的推理负载高度相似。[关于我们对 TPUv8i、TPUv8t、TPUv9、TPUv10 的 SemiAnalysis 供应链出货量估算，请查看我们的加速器模型，获取逐季度出货量的完整拆解。](https://semianalysis.com/accelerator-hbm-model/)

![](https://substack-post-media.s3.amazonaws.com/public/images/5810db06-2805-45bf-bfa0-8b3a3e47684c_1080x731.png)
*来源：InferenceX*

[如果你觉得这个开源基准与数据有用，请给 InferenceX 的 GitHub 仓库点个 Star！](https://github.com/SemiAnalysisAI/InferenceX) InferenceX 是全球唯一同时收录 TPUv7、OpenAI Jalapeño、Nvidia Rubin NVL72、AMD，以及即将收录 SambaNova 和 Trainium2/3 的推理基准。

![](https://substack-post-media.s3.amazonaws.com/public/images/d65268ce-9719-4232-94b5-d1f47289d2bc_1496x633.png)
*来源：InferenceX*

# 给黄仁勋的建议

NVIDIA 只是[偶尔在某些模型/场景上输给 AMD](https://x.com/SemiAnalysis_/status/2116606900271788210)，但 TPU 交付更好的每美元性能、或与之相当的每美元性能，是一种 NVIDIA 高层不愿接受的新体验。TPU 刚在 Qwen3.5 397B FP8 上发布首个 AgentX 结果、显示即便 TPUv7 FP8 也能击败 GB300 NVL72 FP4，NVIDIA 便派出由人类工程师和智能体集群（agent swarms）组成的突击队，横跨美国和中国大陆，以「997」节奏工作——熬到当地时间凌晨两点，周末也不停。[不幸的是，对 NVIDIA 而言，他们的首次 GB300 FP4 反击提交在外部客户的大部分曲线上，每美元性能仍比 TPUv7 FP8 差 1.64 倍。](https://x.com/SemiAnalysis_/status/2112258243372146742) 我们确实认为，只要有足够多的智能体集群，NVIDIA 在 GB300 NVL72 FP4 对 TPUv7 FP8 上或可重新夺回微弱领先；但在 NVIDIA FP8 对 TPUv7 FP8 上，我们认为 NVIDIA 不可能在某些模型上重夺 SOTA。

我们从 PyTorch 开源维护者和 NVIDIA 客户那里经常听到的一点是：官僚主义严重。一些简单的事情——比如给 NVIDIA 驱动加一项新功能，以支持 PyTorch CUDA Graph 捕获的某个特性——卡在「NVIDIA 内部法务审查」三个月。让律师成为技术驱动功能的阻碍者，这毫无道理。我们在试图让 NVIDIA 添加改进 ConnectX、NVSwitch、HGX 板（Vulcan、Umbriel）DCGM 功耗遥测等功能时，也遇到过类似的挑战——光是拿到时间表的时间表就要等很久。相比之下，像 [AMD 这样具备创业公司心态的公司（在 Anush、Ramine、Vamsi、Lisa 的领导下）](https://github.com/ROCm/rocm-systems/pull/12724)能够快速开发这些功能。

NVIDIA 需要一场文化转变，大幅削减官僚主义。这是黄仁勋必须应对的 NVIDIA 护城河最大风险之一。根据我们的经验以及许多客户的经验，Nvidia 现在对外部建议、git 提交和反馈的响应速度已慢于 AMD、Google 和 Amazon。

话虽如此，NVIDIA 的某些团队正在打破官僚主义，例如 [NVIDIA 前 CentML 的 vLLM 团队](https://x.com/SemiAnalysis_/status/2111627094878790023)。AMD 和 [TPU](https://github.com/Inferact/tpu-megakernels) [为流行的开源生产级推理引擎添加了创新的超大内核（Megakernel）解码支持](https://x.com/SemiAnalysis_/status/2109841575547211955)。一周之内，他们就成功为 NVIDIA 守住阵地——[同样快速添加并合入了超大内核支持（PR 由 AMD 的 vLLM 维护者批准）](https://github.com/vllm-project/vllm/pull/61867)。

TPU 正在生态中取得重大进展，多个模型——如 Day 0 Meta 的 Muse Spark Open 支持——以及 [Kimi K3.1 Pro 已具备首日 TPU 支持](https://llm-d.ai/blog/deploy-kimi-k3-1-pro-with-llm-d)；它沿用了 NVIDIA 的剧本：给开源维护者大量芯片。**相比之下，NVIDIA 向社区维护者提供集群贡献，越来越多地被裹上「车管所式」的官僚程序，充其量也只能说是吝啬。对一家市值 $5 万亿的公司，人们本应期待 NVIDIA 更慷慨地向那些免费为改进 NVIDIA 软件栈工作的开源开发者提供资源。我们希望黄仁勋能想办法消除拖慢进展的官僚主义。**

相比之下，AMD 越来越不吝啬，向 vLLM、TileRT、SGLang、Tokenspeed 等上游维护者开放集群访问，并快速扩充 CI 机群，几乎没有任何官僚程序。

![](https://substack-post-media.s3.amazonaws.com/public/images/78c1bfee-bc21-46e5-bb7f-1abfe8ac31fe_2048x1065.png)
*来源：vLLM Dashboard*

# Meta 的 Muse Spark Open FP4 816B 在 SGLang TorchTPU 上的智能体推理性能

Meta 是 TPU 的早期采用者之一，已在使用 SGLang-TorchTPU 将 TPUv7 部署到生产环境。

![](https://substack-post-media.s3.amazonaws.com/public/images/c660c650-cffd-48cd-84b4-1572debb9545_946x676.png)
*来源：Meta*

Muse Spark Open 是 Meta 最新的 816B 参数开放模型，也是 SGLang-TorchTPU 的首发模型之一。在 InferenceX 的智能体推理负载上，来自 RadixArk（社区开发者、SGLang 主要维护者）的提交显示：即便按 Meta 购买 TPU 的实际成本基数计算，TPUv7 的解码每美元性能仍具竞争力。在生产推理中，Meta 用 SGLang 做 LLM 推理，用 vLLM 做 RL 训练 rollout。看端到端延迟，TPUv7 仍需改进才能具备竞争力，例如继续优化其预填充内核。在解码内核方面，TPUv7 SGLang 使用完全融合的超大内核，消除了内核启动延迟。此外，该提交在高并发下使用 SGLang HiCache 的 CPU DRAM 卸载，借助 Google 开源、TPU 原生的 [TPU-Sync](https://github.com/google/tpu-sync) 库，以提高前缀缓存命中率。

![](https://substack-post-media.s3.amazonaws.com/public/images/3b56ac59-ae8d-4abf-8db0-b0c5bb376c0a_918x731.png)
*来源：SemiAnalysis 与 RadixArk*

请注意，Muse Spark Open 是一个极度针对 GPU 优化的模型，理论上对 TPU 完全不友好。原因在于 Muse Spark Open 的 head dim 为 64，这意味着在长上下文注意力中，脉动阵列有 25% 被填充（padding）浪费。

相比之下，GPU 的矩阵核心消费小图块（tile），因此各种 head 维度、专家宽度以及分片后的 KV head 数量都能接近峰值。在 H100 或 B200 上，用 64 而非 128 的维度几乎不付代价，还换来更便宜的注意力层。GPU 架构让研究者可以在优先提升评估性能的同时不损失推理性能。

这相当有意思：TPU 在一个对 TPU 极不友好的模型上，仍能取得颇具竞争力的性能。请注意，拥有大量 TPU 容量的 AI 实验室——如 Anthropic、Google DeepMind，以及即将加入的 OpenAI——通常会协同设计模型，让注意力形状刚好适配 TPU，以避免这个问题。

![](https://substack-post-media.s3.amazonaws.com/public/images/523e5780-f129-497f-91b3-5c740d895932_1876x976.png)
*来源：SemiAnalysis*

当 TPU 遇到 attention head_dim=256 的模型架构时，便进入全力狂飙的「兰博基尼模式」。

![](https://substack-post-media.s3.amazonaws.com/public/images/9b869a08-8df1-47f8-975f-8e411c754af9_848x473.png)
*来源：《马力欧卡丁车》*

RadixArk 团队取得这一惊人成就，干得漂亮！他们正积极更新文档，让所有人都能获得这套优化后的 SGLang Muse Spark Open TPU 配置。我们预计 RadixArk 很快会带来更多 AgentX 结果，证明其 SGLang-TorchTPU 软件栈已可用于生产。

# GLM5.2 / 5.3 vLLM AgentX FP8 智能体推理性能

GLM-5.2/5.3 是一个前沿开放模型。它是混合专家（MoE）Transformer，744B 参数，每 token 约激活 39B。该模型通过 DeepSeek 稀疏注意力（DSA）支持 1M token 上下文：一个轻量级索引器对先前的 token 打分，每次查询只在选出的 2,048 个 token 上运行完整注意力。

在 FP8 下，TPUv7 是服务 GLM-5.2 AgentX 最便宜的方式。在 60 至 300 tok/s/user 区间，其**每美元 token 数达到 FP8 下 B200、B300 和 MI355X 的 1.2 倍至 2.7 倍**，在 150 tok/s/user 时达到 H200 的 4.4 倍。

![](https://substack-post-media.s3.amazonaws.com/public/images/e15bad2d-730d-4116-89f8-3a16fc0e14da_981x737.png)
*来源：SemiAnalysis*

## FP4 GPU 在每美元性能上仍然领先

由于 GLM-5.3 并非原生采用块缩放 FP4 的 QAT（量化感知训练），FP4 相比 FP8 有轻微精度下降。在大多数速度下，FP4 GPU 仍能提供更多每美元 token 数，因为 TPUv7 没有原生 FP4 支持，我们需要等到 2027 年第一季度才有支持 FP4 的 TPUv8——这一点在我们的[加速器与 HBM 模型](https://semianalysis.com/accelerator-hbm-model/)中有追踪。在 100 tok/s/user 时，GB300 和 GB200 FP4 的每美元 token 数分别是 TPUv7 的 3.6 倍和 3.5 倍。FP4 将每个权重的字节数减半，而小批量解码受限于内存带宽。

![](https://substack-post-media.s3.amazonaws.com/public/images/3831cb69-f06e-4ce5-872b-cf533cc951bf_875x733.png)
*来源：SemiAnalysis*

[SemiAnalysis AI 云与 TCO 模型提供 InferenceX 上所有当前加速器的全面定价拆解](https://semianalysis.com/ai-cloud-tco-model/)，以及更多产品——包括 Nvidia Rubin Ultra 和 Feynman、AMD MI400 至 MI700、Google TPU v8 至 v12、AWS Trainium3 至 Trainium6 等未来 SKU。

[获取访问权限](https://semianalysis.com/ai-cloud-tco-model/#contact)

## GLM-5.3 优化

GLM-5.3 AgentX 的上下文长达 1M token，且每个请求中超过 90% 已被缓存，因此 KV 缓存容量决定了能容纳多少用户。共有四项主要改动：

1. GLM-5.3 的注意力对每个 token 只读取一条共享的压缩 KV 条目，因此若按设备切分注意力头，就会把整份缓存复制到每台设备。解码上下文并行（DCP）改为按序列位置切分，并在每一层合并部分注意力结果。

![](https://substack-post-media.s3.amazonaws.com/public/images/8f037375-fc9a-4f62-8084-dedc4b6cfc52_1720x766.png)
*来源：SemiAnalysis 与 Google*

2. 每次查询只读取索引器选出的 2,048 条缓存条目。TPUv7 的 SparseCore 专为分散内存访问而设计，负责挑出并聚集这些条目，同时 TensorCore 运行注意力计算。
3. TPUv7 的寄存器为 8 行 × 128 通道。数据必须打包进这些寄存器，可能产生碎片。128 字节的索引器 key 加上 1 字节的 scale 共 129 字节，比 128 宽的一行多出 1 字节，因此旧布局会向上取整到 256。新布局将其横置：token 沿每行排布，每个 token 的 key 纵贯 32 行、每行 4 字节，再加一行存放 scale。合计 132 字节，仅浪费 3 字节。

![](https://substack-post-media.s3.amazonaws.com/public/images/1ae04378-b44c-451e-88ac-5e6f771932ff_1606x1332.png)
*来源：SemiAnalysis 与 Google*

4. 一个融合内核完成路由；专家计算、all-reduce 与注意力合并成为单次集合通信。TPU 程序针对固定形状编译，因此 Google 为小解码步新增了 4 token 和 8 token 的形状——此前这些会被填充到 16。

# Qwen3.5 397B AgentX

两周前，Qwen3.5 397B 成为 Google 向 AgentX 提交的第一个模型。其 TPUv7 FP8 vLLM 在我们的智能体推理基准上的结果显示，它的每美元性能甚至比 FP4 的 GB300 NVL72 好 1.67 倍。

![](https://substack-post-media.s3.amazonaws.com/public/images/25ecc219-b095-4274-9ff8-11ac2b752949_1412x1278.png)
*来源：SemiAnalysis*

NVIDIA 可能会声称自己不在乎 Qwen3.5 397B 模型，但通过分析我们上游 InferenceX 提交分析数据湖，现实是：对某些 NVIDIA GPU SKU 而言，NVIDIA 已把超过 20% 的扫描 GPU 小时花在 Qwen3.5 上，所以 NVIDIA 很难这么说。此外，看看被分配到 Qwen3.5 的 NVIDIA 工程师，其中有些是 NVIDIA 在**中国大陆**和美国最顶尖的 10 倍效率推理性能工程师，所以显然，NVIDIA 很在意优化这个模型。

**此外，某些主要超大规模云厂商/AI 实验室在做硬件采购和产能规划决策时，会把 Qwen3.5 397B 以及基于 Qwen3.5 397B 架构扩展出的数万亿参数版本当作代理模型（proxy models）。** 所以，对某些「token 工厂」来说，这是一个非常重要的模型。

对做采购决策的读者，我们的 [AI 云与 TCO 模型](https://semianalysis.com/ai-cloud-tco-model)将分析延伸至集群经济性，包括现金流、投资回报和加速器残值。

[获取访问权限](https://semianalysis.com/ai-cloud-tco-model/#contact)

AgentX 捕捉智能体负载的四个要素：

- 多轮：一个会话包含大量用户/助手交互（数十甚至数百次），而聊天机器人场景只有几次。
- 长上下文：系统提示词、工具定义以及大量轮次使上下文快速累积。
- 高前缀复用：因为对话线性推进，第 n-1 轮的输出会拼接到第 n 轮。
- 子智能体突发：一个会话会启动多个生命周期短暂、上下文全新的子智能体，形成突发式的 KVCache 访问模式。

TPU 证明了其即将推出的 TorchTPU vLLM 软件栈能够成功处理智能体负载。

![](https://substack-post-media.s3.amazonaws.com/public/images/ccdfce66-ca13-4572-b74d-41e5a85d1380_1978x1320.png)
*来源：SemiAnalysis*

## NVIDIA 的首次反击提交

NVIDIA 工程师加班加点发布了反击提交 FP4，在解码性能上击败 TPUv7 FP8，但有个小问题：他们把解码调得过头，牺牲了预填充，损害了整体端到端性能。因此，在端到端性能上，TPU FP8 目前仍胜过 GB300 NVL72 FP4。

![](https://substack-post-media.s3.amazonaws.com/public/images/c48e3dfd-b06c-46fb-92ab-e9667bcd79d8_814x700.png)
*来源：SemiAnalysis*

![](https://substack-post-media.s3.amazonaws.com/public/images/90e4b8ad-367a-4071-9d38-43fb1ba89851_822x673.png)

## 开源 Kubernetes 方案 llm-d 让 TPUv7 的解码交互性远超 GB300 FP8

分离式服务把预填充和解码放在不同主机上运行，这样长预填充不会阻塞生成。llm-d 是协调二者的开源 K8s 路由器，每台主机配 4 颗 TPUv7，每个结果使用 24–32 颗芯片。

![](https://substack-post-media.s3.amazonaws.com/public/images/18790491-f0db-438c-8c9e-745221abf5f6_1600x642.png)
*来源：SemiAnalysis*

速度来自于限制每台解码主机同时运行多少请求——从低延迟端的 1 个，到高吞吐端的 112 个。超出上限的请求等待空闲主机，这增加了它们的 TTFT。即便如此，最快点位的 p90 首 token 时间为 8.6 秒，而 GB300 FP4 最快点位为 11.1 秒。

这里使用的是 llm-d——最大的基于生态的生产级推理 Kubernetes 编排器之一。在最近的 Kimi K3.1 Pro 发布中，[它在 llm-d 上实现了 TPUv7 的首日支持](https://llm-d.ai/blog/deploy-kimi-k3-1-pro-with-llm-d)。

![](https://substack-post-media.s3.amazonaws.com/public/images/d87cb8ff-a121-4daa-a8ae-72239abcde9c_1173x717.png)
*来源：InferenceX*

在 FP8 下，搭配 llm-d 的 TPUv7 在每个交互性水平上都击败 GB300——从高吞吐端的 2 倍以上，到超快区间实现超过 1000 tok/s/user。

遗憾的是，对这种基于轮次的路由算法而言，TPU 的端到端性能确实不如 GB300 TRTLLM FP4。但相比 FP8 和 FP4 的 GB300 NVL72 SGLang，它仍然好得多。

![](https://substack-post-media.s3.amazonaws.com/public/images/544a77c4-b86b-46d6-b9a3-321e1c6af525_1176x757.png)
*来源：SemiAnalysis*

## Qwen3.5 的 TPU 优化

Qwen3.5-397B 混合了 45 层线性注意力（每个请求保持固定大小的状态）与 15 层完整注意力。Google 描述了三项主要改动：

- **解码超大内核。** 一个内核运行整个解码步骤，并在当前层计算时预取下一层权重。
- **主机 DRAM 卸载。** KV 缓存与线性注意力状态通过 TPU Sync（Google 新开源的卸载框架）溢出到主机 DRAM。
- **缓存感知路由。** llm-d 把每一轮发送到持有其前缀的预填充主机，并让每个会话留在其解码主机上，除非该主机已满。Google 表示，路由到精确的数据并行 rank 后，解码缓存命中率从 56% 提升到 76%。

# Kimi K3 AgentX

[来自 Inferact 的 TPU 方案和 AMD 率先在开源引擎中为前沿 MoE 模型交付了超大内核。](https://inferact.ai/blog/tpu-megakernels) NVIDIA 在一周内迅速跟进，推出了自己的超大内核。

常规解码步骤会启动数百到数千个内核，芯片在它们之间空转。超大内核在一个长时间运行的内核中执行多层，同时在当前层计算时预取下一层权重。AMD 将其版本称为 MonoKernel。在八颗 MI350X GPU 上运行 GLM-5.2 时，AMD 报告其将单次解码步骤从约 2,459 次启动减少到 210 次，在 batch 1 下运行速度快 2.31 倍。

![](https://substack-post-media.s3.amazonaws.com/public/images/3c217042-892b-4bcd-a0eb-1eb31f185823_1700x604.png)
*来源：SemiAnalysis*

超大内核消除了内核启动之间的空闲间隙。关于超大内核的更多内容，请阅读我们的 TileRT 文章：

在这套配置中，预填充使用了 DCP。上下文并行的预填充与解码两种变体，描述的是各类技术*通常*在何处有益，而非只能在何处运行。K3 使用 MLA，它把 KV 存储为一个跨头共享的潜向量（latent），因此 TP 无法切分它，每个 TP rank 都持有完整副本。DCP 通过给每个 TP rank 分配不同的 token 切片来解决这个问题。若在预填充使用上下文并行，则需要更低的 TP 度数，这会把权重复制到更多芯片上，为 KV 缓存留下更少的 HBM——而 KV 缓存在这里已经是稀缺资源。

![](https://substack-post-media.s3.amazonaws.com/public/images/91dc8bc4-7646-464f-b8dc-80a7e3a5dbbe_2048x1013.png)
*来源：Inferact*

## 发布时与 GB300 FP4 具竞争力

在 10 月 17 日发布时，TPUv7 的每美元 token 数在 50 至 200 tok/s/user 区间为 GB300 的 0.77 倍至 0.91 倍，单用户速度则快 1.6 倍——391 tok/s/user 对 251。按 Google 的内部成本计算，它在 100 和 200 tok/s/user 时击败了 GB300。

![](https://substack-post-media.s3.amazonaws.com/public/images/8bd18ac8-2336-435b-84e6-5b2054f098ee_2038x1349.png)
*来源：InferenceX*

在 NVIDIA 四次刷新之后，GB300 FP4 现在领先 1.5 倍至 2.6 倍。TPUv7 的每美元 token 数仍具竞争力，是 GB200、B200 和 B300 的 1.15 倍至 2.5 倍；而 VR200 是 TPUv7 的 4.3 倍至 5.6 倍。

![](https://substack-post-media.s3.amazonaws.com/public/images/6c33f9a0-4ffb-40d2-b82b-1c7e94632921_1030x704.png)
*来源：InferenceX*

在 TPUv7 与 Rubin NVL72 之间「苹果对香蕉」式的比较中，Rubin 的每美元性能最高好 6 倍。但请注意，这是不公平的比较，因为 Rubin 应当与 TPUv8i 对比——我们很快就会对后者做基准测试。

![](https://substack-post-media.s3.amazonaws.com/public/images/4597cafb-fdb4-4046-831c-d3e8eda53c49_1040x705.png)
*来源：SemiAnalysis*

需要指出的是，**Rubin 的结果仍是预览提交**。我们期待 NVIDIA 提供 Rubin 的直接访问权限，以便我们独立复现这些结果并运行完整的 InferenceX/AgentX 套件。

## 由生态共同构建

这个结果来自 vLLM 生态，而不只是 Google。由 vLLM 的创建者与维护者创立的 Inferact 与 Google 共同构建了 K3 超大内核，双方联合提交了这一结果。该超大内核作为 model runner 插入 vLLM，只替换前向计算，因此 vLLM 的调度、前缀缓存和 KV 传输保持不变。该软件栈在 vLLM TorchTPU 上开源，Inferact 的复现指南可从 Docker 镜像运行。这样的生态开发过去大多发生在 CUDA 上。

![](https://substack-post-media.s3.amazonaws.com/public/images/a7b6ad41-a35c-472d-9f02-b33d7c994c37_2048x927.png)
*来源：Inferact*
