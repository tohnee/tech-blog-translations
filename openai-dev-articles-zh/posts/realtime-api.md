---
title: "Realtime API 开发者笔记"
title_en: "Developer notes on the Realtime API"
source: https://developers.openai.com/blog/realtime-api/
crawled: 2026-09-14
translated: 2026-09-14
---

# Realtime API 开发者笔记

> 原文：[Developer notes on the Realtime API](https://developers.openai.com/blog/realtime-api/) · OpenAI 开发者博客

我们最近[宣布](https://openai.com/index/introducing-gpt-realtime/)了最新的语音到语音（speech-to-speech）模型 `gpt-realtime`，同时 Realtime API 正式可用，并带来一批新的 API 功能。Realtime API 与语音到语音（s2s）模型正式升级为正式可用（GA）版本，在模型质量、可靠性与开发者体验方面都有重大改进。

新的 API 功能可以在[文档](https://platform.openai.com/docs/guides/realtime)与 [API 参考](https://platform.openai.com/docs/api-reference/realtime)中查到，但我们想在这里重点介绍几个你可能错过的功能，并提供何时使用它们的建议。如果你正在集成 Realtime API，希望这些笔记对你有所启发。

## 模型改进

新模型包含了多项旨在更好地支持生产级语音应用的改进。本文聚焦于 API 层面的变化。要更好地理解与使用模型，我们推荐阅读[发布公告博客](https://openai.com/index/introducing-gpt-realtime/)与 [realtime 提示词指南](https://developers.openai.com/cookbook/examples/realtime_prompting_guide)。不过，我们还是会指出一些具体细节。

关于使用这个模型，几条关键建议：

- 在 [realtime playground](https://platform.openai.com/playground/realtime) 中试验提示词。
- 想要最佳的助手语音质量，请使用 `marin` 或 `cedar` 音色。
- 针对新模型重写提示词。由于指令遵循能力的提升，具体的指令现在威力大得多。例如，「当 Y 时总是说 X」这样的提示词，旧模型可能只当作模糊的指导，而新模型可能会在意料之外的情况下也严格遵守它。请留意你所给出的具体指令。假设指令都会被遵循。

## API 形态变化

随着 GA 发布，我们更新了 Realtime API 的形态，现在同时存在 beta 接口与 GA 接口。我们建议客户端迁移并基于 GA 接口进行集成，因为它提供新功能，而 beta 接口最终将被弃用。

迁移所需变更的完整列表见 [beta 到 GA 迁移文档](https://platform.openai.com/docs/guides/realtime#beta-to-ga-migration)。

你可以通过 beta 接口使用新的 `gpt-realtime` 模型，但某些功能可能不受支持。详见下文。

### 功能可用性

Realtime API 的 GA 版本包含许多新功能。其中一些在旧模型上可用，另一些则不可用。

| 功能 | GA 模型 | Beta 模型 |
|---|---|---|
| 图像输入 | ✅ | ❌ |
| 长上下文 | ✅ | ✅ |
| 异步函数调用 | ✅ | ❌ |
| Prompts（提示词模板） | ✅ | ✅ |
| MCP | ✅ *配合异步 FC 效果最佳* | ✅ *无异步 FC 时功能受限** |
| 音频 token → 文本 | ✅ | ❌ |
| 欧盟数据驻留 | ✅ | ✅ *仅 06-03 版本* |
| SIP | ✅ | ✅ |
| 空闲超时 | ✅ | ✅ |

*由于 beta 模型缺少异步函数调用，模型可能无法很好地处理没有输出的待定 MCP 工具调用。我们建议在 MCP 场景下使用 GA 模型。

### temperature 的变化

GA 接口已移除 `temperature` 这一模型参数，beta 接口则将 temperature 限制在 `0.6 - 1.2` 范围内，默认值为 `0.8`。

你可能会问：「为什么用户不能随意设置 temperature，并用它来让回复更加确定？」答案是：对于这种模型架构，temperature 的行为有所不同，把 temperature 设为推荐的 `0.8` 几乎总是对用户最有利的选择。

根据我们的观察，用低温度无法让这些音频回复变得确定，而更高的温度会导致音频出现失真。我们建议通过提示词试验来控制模型行为的这些维度。

## 新功能

除了 beta 到 GA 的变化之外，我们还为 Realtime API 增加了若干新功能。

所有功能都在[文档](https://platform.openai.com/docs/guides/realtime)与 [API 参考](https://platform.openai.com/docs/api-reference/realtime)中有完整说明，但这里我们会着重讲讲在集成与迁移时如何理解这些新功能。

### 会话空闲超时

对于某些应用来说，用户输入出现长时间的空档是出乎意料的。想象一通电话——如果听不到线路另一端那个人的声音，我们会询问对方是否还在。也许是模型漏听了用户说的话，也许是用户不确定模型是否还在讲话。我们增加了一个功能，可自动触发模型说一句类似「你还在吗？」的话。

要启用此功能，请在轮次检测（turn detection）的 `server_vad` 设置中配置 `idle_timeout_ms`。超时计时从上一条模型回复的音频播放完毕之后开始——即超时时间点 = `response.done` 时刻 + 音频播放时长 + 超时时长。如果 VAD 在这段时间内没有触发，超时即被触发。

超时被触发时，服务器会发送一个 [`input_audio_buffer.timeout_triggered`](https://platform.openai.com/docs/api-reference/realtime-server-events/input_audio_buffer/timeout_triggered) 事件，随后将空音频段提交到会话历史，并触发一次模型响应。提交空音频让模型有机会检查 VAD 是否失效、相关时段内是否存在用户发言。

客户端可以这样启用该功能：

```
{
  "type": "session.update",
  "session": {
    "type": "realtime",
    "instructions": "You are a helpful assistant.",
    "audio": {
      "input": {
        "turn_detection": {
          "type": "server_vad",
          "idle_timeout_ms": 6000
        }
      }
    }
  }
}
```

### 长对话与上下文处理

我们调整了 Realtime API 处理长会话的方式。有几点需要留意：

- Realtime 会话现在最长可持续 60 分钟（此前为 30 分钟）。
- `gpt-realtime` 模型的 token 窗口为 32,768 个 token。回复最多可消耗 4,096 个 token。这意味着模型的最大输入为 28,672 个 token。
- 会话指令加上工具（tools）的最大长度为 16,384 个 token。
- 当会话达到 28,672 个 token 时，服务会自动截断（丢弃）消息，但这是可配置的。
- 当存在转录文本（transcript）时，GA 服务会自动丢弃部分音频 token 以节省 token。

#### 配置截断设置

当对话上下文窗口填满达到 token 上限时会发生什么？一旦达到上限，Realtime API 会自动开始从会话开头截断（丢弃）消息（即最旧的消息）。你可以通过设置 `"truncation": "disabled"` 来禁用这种截断行为，此后当回复的输入 token 过多时会改为抛出错误。不过截断仍然很有用，因为即便输入规模超出模型的承受能力，会话也能继续进行。Realtime API 不会对被丢弃的消息做摘要或压缩（compaction），但你可以自行实现。

截断的一个负面影响是：改变对话开头的消息会使 [token 提示词缓存](https://platform.openai.com/docs/guides/prompt-caching)失效。提示词缓存的原理是识别提示词前缀中完全一致的精确匹配内容。在后续每一轮中，只有未发生变化的 token 会被缓存。当截断改变了对话的开头，可缓存的 token 数量就会减少。

为了缓解这一负面影响，我们实现了一个功能：每次发生截断时，都截断比实际需要更多的内容。将保留比例（retention ratio）设为 `0.8`，就会截断 20% 的上下文窗口，而不是只截断刚好能让输入 token 数低于上限的量。思路是一次性截断*更多*的上下文窗口，而不是每次截断一点点，从而降低缓存失效的频率。这种对缓存友好的做法可以为达到输入上限的长会话节省成本。

```
{
  "type": "session.update",
  "session": {
    "truncation": {
      "type": "retention_ratio",
      "retention_ratio": 0.8
    }
  }
}
```

### 异步函数调用

Responses API 会在函数调用之后立即强制要求函数响应，而 Realtime API 允许客户端在一个函数调用尚未完成时继续会话。这种延续对用户体验很友好，让实时对话得以自然继续，但模型有时会对并不存在的函数响应内容产生幻觉。

为了缓解这一问题，GA 的 Responses API 增加了占位响应（placeholder responses），其内容经过我们在实验中的评估与调优，以确保模型即使在等待函数响应时也能表现得体。如果你向模型询问某个函数调用的结果，它会说类似「我还在等结果」的话。此功能对新模型自动启用——你这边无需任何更改。

### 欧盟数据驻留

欧盟数据驻留现在专门支持 `gpt-realtime-2025-08-28` 与 `gpt-4o-realtime-preview-2025-06-03`。数据驻留必须为组织显式启用，并通过 `https://eu.api.openai.com` 访问。

### 追踪

Realtime API 会将追踪（traces）记录到[开发者控制台](https://platform.openai.com/logs?api=traces)，记录实时会话中的关键事件，这对排查与调试很有帮助。作为 GA 的一部分，我们新增了几种事件类型：

- 会话更新（当 `session.updated` 事件发送给客户端时）
- 输出文本生成（针对模型生成的文本）

### 托管 Prompts（提示词模板）

你现在可以在 Realtime API 中使用 [prompts（提示词模板）](https://platform.openai.com/docs/guides/realtime-models-prompting#update-your-session-to-use-a-prompt)，这是一种便捷方式，让你的应用代码引用一个可以单独编辑的提示词。Prompts 同时包含指令与会话配置，例如轮次检测设置。

你可以在 [realtime playground](https://platform.openai.com/audio/realtime) 中创建 prompt，按需迭代并为它做版本管理，然后客户端可以通过 ID 引用该 prompt，如下所示：

```
{
  "type": "session.update",
  "session": {
    "type": "realtime",
    "prompt": {
      "id": "pmpt_123", // your stored prompt ID
      "version": "89", // optional: pin a specific version
      "variables": {
        "city": "Paris" // example variable used by your prompt
      }
    },
    // You can still set direct session fields; these override prompt fields if they overlap:
    "instructions": "Speak clearly and briefly. Confirm understanding before taking actions."
  }
}
```

如果 prompt 设置与传给会话的其他配置重叠（如上例所示），会话配置优先生效，因此客户端既可以使用 prompt 的配置，也可以在会话时对其进行覆盖调整。

### 旁路连接（sideband connections）

Realtime API 允许客户端通过 WebRTC 或 SIP 直接连接到 API 服务器。不过，你很可能希望把工具使用和其他业务逻辑放在应用服务器上，以保持这些逻辑的私密性，并使之与客户端无关。

通过旁路（sideband）控制通道连接，可以把工具使用、业务逻辑和其他细节安全地保留在服务端。现在 SIP 与 WebRTC 连接都提供旁路选项。

旁路连接意味着同一个 realtime 会话有两条活动连接：一条来自用户的客户端，一条来自你的应用服务器。服务器连接可用于监控会话、更新指令以及响应工具调用。

更多信息请参阅[旁路连接文档](https://platform.openai.com/docs/guides/realtime-server-controls)。

## 开始构建

我们希望这些笔记能帮助你理解正式可用的 Realtime API 与新的 realtime 模型都有哪些变化。

有了这些新的认知框架，就请[查阅 realtime 文档](https://platform.openai.com/docs/guides/realtime)，构建语音智能体、建立连接，或开始为 realtime 模型编写提示词吧。
