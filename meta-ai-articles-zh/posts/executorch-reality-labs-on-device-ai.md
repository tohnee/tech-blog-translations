---
title: "ExecuTorch 在 Reality Labs 的落地：为 Meta 各设备提供设备端 AI 动力"
title_en: "ExecuTorch Adoption in Reality Labs: Powering On-Device AI Across Meta Devices"
date: 2025-11-21
source: https://ai.meta.com/blog/executorch-reality-labs-on-device-ai
crawled: 2026-09-22
translated: 2026-09-22
---

# ExecuTorch 在 Reality Labs 的落地：为 Meta 各设备提供设备端 AI 动力

> 原文：[ExecuTorch Adoption in Reality Labs: Powering On-Device AI Across Meta Devices](https://ai.meta.com/blog/executorch-reality-labs-on-device-ai) · Meta AI（Wayback 存档）

2025 年 11 月 21 日 · 10 分钟阅读

在 Meta，设备端 AI 是为使用我们产品的人们提供快速、私密、智能体验的基石。ExecuTorch——我们的开源、轻量、高效推理引擎——在为我们的多款应用赋能这些能力方面发挥了关键作用。今天，我们很高兴地分享：ExecuTorch 现正在为 Reality Labs 的 VR 头显和 AI 眼镜产品组合提供尖端机器学习体验。ExecuTorch 让开发者轻松部署最先进的机器学习模型，解锁更丰富、更智能、更沉浸的体验。通过打通从研究到应用的路径、让人们把我们的成果握在手中，ExecuTorch 正在为先进的设备端 AI 设立新标准。

## ExecuTorch 在 Reality Labs 各设备上的落地

Reality Labs 的目标是构建下一代计算平台。为此，Reality Labs 的各团队开发下一代硬件，包括 Ray-Ban Meta 和 Oakley Meta 眼镜、Meta Ray-Ban Display 眼镜与 Meta 神经腕带（Neural Band），以及 Meta Quest 头显。这些产品要求 AI 模型在从高性能片上系统（SoC）到超低功耗微控制器的广泛硬件上高效运行。ExecuTorch 的模块化设计及其可移植性、小体积和硬件抽象，使其成为 Reality Labs 多样化产品生态的理想选择。

设备端 AI 部署带来一个根本性挑战：既要支持研究者和工程师在多样硬件目标上快速试验优化流程，又不能牺牲性能和生产力。传统方法需要把 PyTorch 模型转换为其他格式，这会引入数值不匹配和代价高昂的调试周期，打破研究者所需的紧凑迭代闭环。在产品线和 AI 用例多样的场景下，这一挑战尤为尖锐。ExecuTorch 通过消除转换步骤、提供完全 PyTorch 原生的流程来应对。它利用 PyTorch 的导出能力创建模型的可移植表示，既能在设备上执行，也能在 PyTorch 中执行以进行部署前验证。开发者随后可以进一步针对特定硬件编译计算图——例如量化模型以优化内存约束，或应用编译器 pass 来优化目标 SoC 上的延迟。ExecuTorch 的一项重要益处是，大多数优化在部署前仍可在 PyTorch 内验证。这得益于与硬件伙伴的紧密集成——他们通过遵循 ExecuTorch 的 API 和设计原则做出贡献。凭借这一设计及其硬件抽象，ExecuTorch 使 Reality Labs 能够以最少的修改，跨不同产品和芯片组一致地部署模型。

以下是在我们 Reality Labs 硬件上的实际运作情况。

### Meta Quest 3 和 Quest 3S

ExecuTorch 使 Meta Quest 3 和 3S 能够直接在设备上运行高级 AI 工作负载——例如深度估计和场景理解。这种本地处理确保快速、可靠的性能，让 Passthrough 等功能无缝融合物理世界与虚拟内容。其结果是与环境的自然、逼真交互，虚拟与物理空间的边界随之消融。凭借既响应迅速又便捷的高性能 AI 特性，这些头显带来更上一层楼的体验。ExecuTorch 支持的实时 AI 模型还驱动手部追踪和手柄追踪等重要功能。这些能力构成精确 UI 控制、手势识别和虚拟键盘的基础，使交互直观而精准。ExecuTorch 赋能的另一项突出特性是持久房间记忆。得益于高效的设备端推理，Meta Quest 3 和 3S 可以记住多达 15 个不同的房间，每个房间都有独特的布局和边界。这种灵活性节省时间，并确保无论在哪里使用头显，都能获得一致、个性化的体验。

### Meta Ray-Ban Display

ExecuTorch 使复杂模型能够直接在我们的 Ray-Ban Meta 和 Meta Ray-Ban Display 眼镜上运行，交付实时翻译等新功能，以及在眼镜显示屏上实时呈现的字幕。与传统的纯音频翻译不同，这种由快速本地推理实现的视觉方式，让人们可以按自己的节奏滚动查看转录，使外语或嘈杂环境中的对话更易参与。另一项突破是「野外文本」（text-in-the-wild）能力，由设备端 AI 和自我中心 OCR（光学字符识别）实现。由于眼镜所见即你所见，它们可以即时从场景中识别出一个人的感兴趣区域并识别相关文本。这支持对文档、菜单和路牌的翻译、朗读和上下文操作，直接在显示屏上提供即时翻译、听写和上下文操作。佩戴眼镜的人可以走进一家餐厅，瞥一眼外语菜单，几秒钟内获得翻译；或者指向菜单上的特定菜品询问更多信息，而无需掏出手机。Meta Ray-Ban Display 的阅读助手功能更进一步：只需指向物理文本，一个人就能触发即时翻译、释义或听写——这都得益于直接在设备上运行的实时手部追踪和先进 OCR 模型。这些能力使 Meta Ray-Ban Display 眼镜成为探索世界、即时获取信息的得力伙伴。

### Oakley Meta Vanguard

为运动员设计的 Oakley Meta Vanguard 眼镜利用尖端 AI，在连接 Garmin 账户后提供实时表现洞察。无论是跑步、骑行还是徒步，Meta AI 都能通过简单的语音命令，就配速、心率、消耗卡路里等关键表现指标提供即时反馈。例如，你可以说：「Hey Meta，我的心率是多少？」或「Hey Meta，我表现如何？」在放松阶段，运动员还可以收到 Meta AI 的训练总结。

## 拓展 ExecuTorch 的影响力

ExecuTorch 已迅速超越 Meta，成长为一个由开发者、研究者和硬件伙伴组成的活跃社区，大家共享开放、高效、可移植的设备端 AI 愿景。从芯片厂商和设备制造商，到应用开发者和 AI 研究者，生态系统中各方贡献者都在帮助拓展 ExecuTorch 的影响力。项目的开源开发确保了透明与协作，Apple、Arm、Cadence、Intel、MediaTek、NXP Semiconductors、Qualcomm Technologies Inc. 和三星等公司都做出了贡献。这些平台的 ExecuTorch 后端已公开可用。除硬件伙伴外，ExecuTorch 如今也是 AI 生态的重要一环。例如，在最近的正式发布（General Availability）中，ExecuTorch 展示了与 Hugging Face transformers 和 Ultralytics 库的模型导出覆盖、与 Unsloth AI 和 torchao 框架的互操作性，以及与 Liquid AI、NimbleEdge 和 React-Native-Executorch 等 SDK 的集成。更多信息见 Success Stories 页面。

开放性很重要，因为设备端 AI 跨越多个平台、芯片和用例。通过开放协作，ExecuTorch 让整个生态一起创新，确保 PyTorch 模型可以在任何地方高效运行——从手机和 AI 应用，到未来的 AR 眼镜乃至更远。

## 展望

ExecuTorch 是 Meta 设备端 AI 的基础技术，它在 Reality Labs 内的采用正在加速我们在产品中交付智能、私密、响应迅速的体验。我们与芯片伙伴的紧密协作也确保 ExecuTorch 保持在设备端 AI 创新的前沿。我们很高兴继续这段旅程，并在帮助全球人们解锁新能力的同时分享更多进展。我们邀请你为 ExecuTorch 做出贡献，并在我们的 GitHub 页面分享反馈。你也可以加入 ExecuTorch Discord 服务器上日益壮大的社区。
