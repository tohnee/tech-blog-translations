---
title: "三次近期事故的复盘"
title_en: "A postmortem of three recent issues"
source: https://www.anthropic.com/engineering/a-postmortem-of-three-recent-issues
published: 2025-09-17
crawled: 2026-09-11
translated: 2026-09-11
---

# 三次近期事故的复盘

> 原文：[A postmortem of three recent issues](https://www.anthropic.com/engineering/a-postmortem-of-three-recent-issues) · Anthropic Engineering Blog

8 月至 9 月初，三个基础设施 bug 间歇性地降低了 Claude 的回答质量。我们现已解决这些问题，并希望解释事情的原委。

8 月初，不少用户开始反馈 Claude 的回答质量下降。这些最初的反馈很难与用户反馈的正常波动区分开。到 8 月下旬，反馈的频率和持续性不断上升，促使我们展开调查，并最终发现了三个彼此独立的基础设施 bug。

直截了当地说：我们从不因需求量、时段或服务器负载而降低模型质量。用户报告的问题完全由基础设施 bug 造成。

我们理解用户期望 Claude 保持稳定的质量，我们也为「基础设施变更不得影响模型输出」设定了极高的标准。在最近这几起事故中，我们没有达到这个标准。下面的复盘将解释出了什么问题、为什么检测和修复比我们希望的要慢，以及我们正在做什么来防止类似事故再次发生。

我们通常不会分享这种程度的基础设施技术细节，但考虑到这些问题的范围与复杂度，我们认为值得给出更完整的解释。

## 我们如何大规模地服务 Claude

我们通过第一方 API、Amazon Bedrock 和 Google Cloud 的 Vertex AI 向数百万用户提供 Claude。我们把 Claude 部署在多个硬件平台上：AWS Trainium、NVIDIA GPU 和 Google TPU。这种做法提供了服务全球用户所需的容量和地域分布。

每个硬件平台特性不同，需要专门的优化。尽管存在这些差异，我们对模型实现有严格的等价性标准：无论哪个平台服务你的请求，都应获得同样质量的回答。这种复杂度意味着，任何基础设施变更都需要在所有平台和配置上仔细验证。

## 事件时间线

![Illustrative timeline of events on the Claude API. Yellow: issue detected, Red: degradation worsened, Green: fix deployed.](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2Fd707dfc2effceba608d04007bc776132a3e57838-3840x1800.png&w=3840&q=75)

**Claude API** 事件的示意时间线。黄色：发现问题；红色：劣化加剧；绿色：修复部署完成。

这些 bug 相互重叠的特性让诊断格外困难。第一个 bug 于 8 月 5 日引入，影响了约 0.8% 的 Sonnet 4 请求。另外两个 bug 由 8 月 25 日和 26 日的部署引发。

虽然最初影响有限，但 8 月 29 日的一次负载均衡变更开始扩大受影响的流量。这让更多用户遇到问题，而其他用户仍看到正常表现，造成了令人困惑、相互矛盾的反馈。

## 三个相互重叠的问题

下面我们描述造成劣化的三个 bug：发生时间以及我们如何解决：

### 1. 上下文窗口路由错误

8 月 5 日，部分 Sonnet 4 请求被错误地路由到为即将推出的 [1M token 上下文窗口](https://docs.claude.com/en/docs/build-with-claude/context-windows#1m-token-context-window)[配置](https://docs.claude.com/en/docs/build-with-claude/context-windows)的服务器。该 bug 最初影响 0.8% 的请求。8 月 29 日，一次例行的负载均衡变更无意中增加了被路由到 1M 上下文服务器的短上下文请求数量。在 8 月 31 日受影响最严重的一小时，16% 的 Sonnet 4 请求受到影响。

在此期间发起请求的 Claude Code 用户中，约 30% 至少有一条消息被路由到错误的服务器类型，导致回答质量下降。在 Amazon Bedrock 上，误路由流量在 8 月 12 日达到峰值，占 Sonnet 4 全部请求的 0.18%。8 月 27 日至 9 月 16 日期间，Google Cloud 的 Vertex AI 上受错误路由影响的请求不足 0.0004%。

不过，部分用户受到的影响更严重，因为我们的路由是「粘性」的：一旦某个请求被错误的服务器服务，后续对话很可能继续被同一个错误的服务器服务。

**解决：** 我们修复了路由逻辑，确保短上下文和长上下文请求被导向正确的服务器池。修复于 9 月 4 日部署，第一方平台和 Google Cloud Vertex AI 的发布于 9 月 16 日完成，AWS Bedrock 于 9 月 18 日完成。

### 2. 输出损坏

8 月 25 日，我们向 Claude API 的 TPU 服务器部署了一项错误配置，导致 token 生成期间出现错误。一个由运行时性能优化引发的问题，偶尔会给那些在当前上下文下本不该出现的高概率 token 赋值——例如对英文提示输出泰文或中文字符，或在代码里产生明显的语法错误。一小部分用英文提问的用户可能在回答中间看到「สวัสดี」这样的内容。

该损坏影响 8 月 25-28 日对 Opus 4.1 和 Opus 4 的请求，以及 8 月 25 日至 9 月 2 日对 Sonnet 4 的请求。第三方平台未受此问题影响。

**解决：** 我们定位了问题并于 9 月 2 日回滚了变更。我们已在部署流程中加入针对异常字符输出的检测测试。

### 3. 近似 top-k 的 XLA:TPU 编译错误

8 月 25 日，我们部署了改进 Claude 文本生成期间 token 选择的代码。这次改动无意中触发了 XLA:TPU[1] 编译器中一个潜伏的 bug，已确认影响对 Claude Haiku 3.5 的请求。

我们也认为它可能影响了 Claude API 上的部分 Sonnet 4 和 Opus 3 请求。第三方平台未受此问题影响。

**解决：** 我们最先观察到该 bug 影响 Haiku 3.5，并于 9 月 4 日回滚。之后我们注意到用户对 Opus 3 的反馈与该 bug 的症状相符，于 9 月 12 日再次回滚。经过大量调查，我们未能在 Sonnet 4 上复现该 bug，但出于审慎决定同样将其回滚。

与此同时，我们 (a) 一直在与 XLA:TPU 团队合作修复编译器 bug，(b) 部署了改用高精度精确 top-k 的修复方案。细节见下文的深入分析。

## 深入剖析 XLA 编译器 bug

为了说明这些问题的复杂度，下面介绍 XLA 编译器 bug 的表现方式，以及为什么它特别难以诊断。

Claude 生成文本时，会为每个可能的下一个词计算概率，然后从这个概率分布中随机采样。我们用「top-p 采样」避免无意义的输出——只考虑累计概率达到阈值（通常为 0.99 或 0.999）的词。在 TPU 上，我们的模型跨多个芯片运行，概率计算发生在不同位置。要对这些概率排序，需要在芯片之间协调数据，这相当复杂。[2]

2024 年 12 月，我们发现当[温度（temperature）](https://docs.claude.com/en/docs/about-claude/glossary#temperature)为零时，我们的 TPU 实现偶尔会丢掉概率最高的 token。我们部署了一个变通方案来修复这种情况。

![Code snippet of a December 2024 patch to work around the unexpected dropped token bug when temperature = 0.](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2Fefee0d3d25f6b03cbfc57e70e0e364dcd8b82fe0-2000x500.png&w=3840&q=75)

2024 年 12 月补丁的代码片段，用于在 temperature = 0 时绕过 token 被意外丢弃的 bug。

根本原因涉及混合精度运算。我们的模型用 [bf16](https://github.com/tensorflow/tensorflow/blob/f41959ccb2d9d4c722fe8fc3351401d53bcf4900/tensorflow/core/framework/bfloat16.h)（16 位浮点）计算下一 token 概率。但向量处理器是 [fp32 原生](https://dl.acm.org/doi/pdf/10.1145/3360307)的，因此 TPU 编译器（XLA）可以通过把部分运算转换为 fp32（32 位）来优化运行时间。这个优化 pass 由 `xla_allow_excess_precision` 标志控制，默认为 true。

这造成了一个不一致：本应对「哪个 token 概率最高」达成一致的运算，却运行在不同的精度级别上。精度不匹配意味着它们对最高概率 token 的判断不一致，导致最高概率的 token 有时干脆从候选中消失。

8 月 26 日，我们部署了采样代码的重写，以修复精度问题并改进对逼近 top-p 阈值的概率的处理。但在修复这些问题的同时，我们暴露出了一个更棘手的问题。

![Code snippet showing minimized reproducer merged as part of the August 11 change that root-caused the “bug” being worked around in December 2024; in reality, it’s expected behavior of the xla_allow_excess_precision flag.](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F6d10e58c0bd5fd7cb03dc0adc716cb1e4f039343-2000x2560.png&w=3840&q=75)

代码片段：随 8 月 11 日变更合并的最小化复现器，它为 2024 年 12 月被绕过的「bug」找到了根因——实际上那是 `xla_allow_excess_precision` 标志的预期行为。

我们的修复移除了 12 月的变通方案，因为我们认为已经解决了根因。结果这暴露了[近似 top-k](https://docs.jax.dev/en/latest/_autosummary/jax.lax.approx_max_k.html) 运算中一个更深的 bug——这是一个快速找出最高概率 token 的性能优化。[3] 这种近似有时会返回完全错误的结果，但只发生在特定的批大小和模型配置下。12 月的变通方案一直在无意中掩盖着这个问题。

![Slack message showing reproducer of the underlying approximate top-k bug shared with the XLA:TPU engineers who developed the algorithm. The code returns correct results when run on CPUs.](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F7e42db934d0e84ea40fc56b416ddb09b2097a5ff-2400x1404.png&w=3840&q=75)

与[开发该算法](https://arxiv.org/pdf/2206.14286)的 XLA:TPU 工程师共享的底层近似 top-k bug 复现器（Slack 消息截图）。这段代码在 CPU 上运行时返回正确结果。

这个 bug 的行为令人抓狂地不稳定：它会随着无关因素改变，比如它前后运行了哪些运算、调试工具是否开启。同一个提示可能这一次请求完美运行、下一次就失败。

调查期间，我们还发现精确 top-k 运算已经不再有当年那种难以承受的性能开销。我们从近似 top-k 切换到精确 top-k，并把另外一些运算统一固定在 fp32 精度上。[4] 模型质量不容妥协，因此我们接受了轻微的效率损失。

## 为什么难以检测

我们的验证流程通常依赖基准测试，辅以安全评估和性能指标。工程团队会做抽查，并先向小规模「金丝雀」群组部署。

这些问题暴露出我们本应更早发现的关键缺口。我们运行的评估根本没有捕捉到用户报告的劣化，部分原因是 Claude 对孤立的错误往往恢复得很好。我们自身的隐私实践也给调查反馈带来了困难：内部的隐私与安全控制限制了工程师访问用户与 Claude 交互内容的方式和时机，尤其是那些没有被作为反馈上报的交互。这保护了用户隐私，但也让工程师无法检查识别或复现 bug 所需的问题交互。

每个 bug 在不同平台上以不同的速率产生不同的症状。这形成了一团令人困惑、不指向任何单一原因的反馈。它看起来像随机、不一致的质量劣化。

更根本地说，我们过度依赖带噪声的评估。虽然我们注意到网上反馈在增加，却缺少把这些反馈与我们近期变更逐一关联的清晰方法。8 月 29 日负面反馈激增时，我们没有立即把它与一次本属常规的负载均衡变更联系起来。

## 我们正在改变什么

在继续改进基础设施的同时，我们也在改进评估和预防 bug 的方式，覆盖我们服务 Claude 的所有平台。以下是我们的改变：

- **更灵敏的评估：** 为了帮助找到任何给定问题的根因，我们开发了能更可靠地区分正常实现与故障实现的评估。我们会持续改进这些评估，更密切地盯住模型质量。
- **在更多地方运行质量评估：** 尽管我们已在系统上运行常规评估，我们将改为在真实生产系统上持续运行，以捕捉诸如上下文窗口负载均衡错误之类的问题。
- **更快的调试工具：** 我们将开发基础设施与工具，在不牺牲用户隐私的前提下更好地调试来自社区的反馈。此外，我们在此次事件中开发的一些定制工具将用于缩短未来类似事故（如果发生）的修复时间。

评估与监控很重要。但这些事故表明，当 Claude 的回答达不到平时水准时，我们同样需要来自用户的持续信号。关于具体变化的反馈、遇到异常行为的实例、以及跨用例的模式，都帮我们隔离了这些问题。

用户继续直接向我们反馈仍然格外有帮助。你可以在 Claude Code 里使用 `/bug` 命令，或在 Claude 应用中点击「踩」按钮。开发者和研究者常常创造出评估模型质量的新颖有趣的方法，与我们的内部测试互补。如果你愿意分享你的方法，请联系 [feedback@anthropic.com](mailto:feedback@anthropic.com)。

我们始终感谢社区的这些贡献。

#### 致谢

作者：Sam McAllister。感谢 Stuart Ritchie、Jonathan Gray、Kashyap Murali、Brennan Saeta、Oliver Rausch、Alex Palcuie 以及许多其他同事。

[1] XLA:TPU 是优化编译器，负责把 [XLA](https://openxla.org/xla/architecture) 高级优化语言（通常用 [JAX](https://docs.jax.dev/en/latest) 编写）翻译为 TPU 机器指令。

[2] 我们的模型太大，单芯片放不下，被切分在数十个甚至更多芯片上，这使得排序操作成为分布式排序。TPU（与 GPU、Trainium 一样）的性能特性也与 CPU 不同，需要使用向量化操作而非串行算法的不同实现技术。

[3] 我们一直使用这个近似运算，因为它带来了可观的性能提升。近似的原理是接受概率最低的 token 上可能出现的不准确——这本不应影响质量，除非像这个 bug 那样把概率最高的 token 也丢掉了。

[4] 注意，如今已修正的 top-k 实现可能导致靠近 top-p 阈值的 token 是否入选出现细微差别，在极少数情况下，用户可能需要重新调整自己的 top-p 取值。
