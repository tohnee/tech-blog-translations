---
title: "编码会话更长、上下文更多。Claude Opus 5.5 正是为此而设计。"
title_en: "Coding sessions are longer and use more context. Claude Opus 5.5 is built with that in mind."
date: 2026-09-24
source: https://claude.com/blog/claude-opus-5-5-built-for-coding-sessions-that-use-more-context/
crawled: 2026-09-26
translated: 2026-09-26
---

# 编码会话更长、上下文更多。Claude Opus 5.5 正是为此而设计。

> 原文：[Coding sessions are longer and use more context. Claude Opus 5.5 is built with that in mind.](https://claude.com/blog/claude-opus-5-5-built-for-coding-sessions-that-use-more-context/) · Claude 博客

我们估算，对于按 token 计费的典型工作负载，Claude Opus 5.5 的运行成本比 Opus 5 [低约 40%](https://www.anthropic.com/claude-opus-5-5)。对开发者而言，这些节省究竟*如何*累积起来，非常重要。

如果你按 token 付费，那么在长时运行、高上下文的会话中，你会看到最大的成本差异——而这恰恰是过去六个月里变得越来越普遍的那类 Claude Code 会话。

本文将深入剖析其中的机制：是什么让 Opus 5.5 在开发者今天（以及很可能明天）的编码方式下依然划算。

## **Claude Code 趋势**

我们调取了 2026 年 3 月至 9 月开发者使用 Claude Code 的汇总数据。随着模型能力的提升，开发者部署智能体的方式越来越精深。每个会话的提示数量保持平稳，但我们发现了一些有趣的行为：

- Claude 在每个提示上工作的时间延长至 3.3 倍，每个提示的模型调用次数增加超过 40%。中断次数减少了 68%。
- 开发者连接工具服务器或使用技能（skill）的可能性大约翻倍，而向提示中粘贴文本的可能性降低了约三分之一。
- 每个请求的上下文增长了 2.6 倍。输入与输出 token 之比从 189:1 变为 324:1。

这一切都表明，开发者正在把工作更卖力、信息更充分的 Claude 指向更大、更开放式的任务。对于这类会话，上下文工程的经济影响会复利叠加。

简而言之，Claude 读取的 token 更多了。你需要确保[你提供的所有上下文都是必要的](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models)，并确保[尽可能多的上下文是从缓存中读取的](https://claude.com/blog/maximizing-the-value-of-your-claude-code-sessions)。

## **是什么让 Opus 5.5 在长时、重上下文的会话中划算**

有三项变化让长时运行、重上下文的会话更具成本效益：定价、模型行为以及 Claude Code 执行框架（harness）方面的变化。我们逐一来看。

### **缓存很便宜**

对于按 token 计费的用量，我们将输入和输出 token 的价格降低了 20%，而*缓存 token 的读取价格直降了 60%*。后一项降价意义重大，因为缓存读取占据了智能体与编码工作成本的大部分。

而且正如我们刚刚讨论的，六个月内每个请求的上下文增长了约 2.6 倍，这意味着节省正朝着正确的方向发展。对按 token 计费的用户来说，同样的降价放在今天的 Claude Code 流量上，比六个月前能省下更多，因为如今账单中更大的一部分是重复读取的上下文。

截至本文发布之日，Opus 5.5 的缓存 token 价格仅为竞争模型的五分之一，同时性能还更胜一筹。

### **Claude Code 更善于利用缓存**

这一点对 Opus 5.5 的针对性较弱，更多是过去六个月我们为 Claude Code 添加的众多功能的成果。考虑到刚才讨论的编码会话趋势，你会预期缓存未命中率更高，但事实恰恰相反。**未命中缓存的输入减少了超过 50%。**

例如，我们让刷新登录之类的小麻烦（papercut）更难无意中破坏你的缓存。对于在对话中途添加指令或按需加载工具这类更大的动作，我们也让它更难破坏缓存。对于 Opus 5.5 和 Fable 5.1 等较新的模型，你现在可以在会话中途更改努力等级（effort level），而无需重置缓存。

我们还让缓存在长时运行和委派会话中更加有用。使用 API 密钥和云厂商的开发者现在可以设置一小时的缓存生存时间（订阅用户此前已享有），而分叉出的子智能体会从父会话的缓存起步，不必为同样的上下文再次付费。

### **同样的任务，更少的轮次**

完成同样的任务，Opus 5.5 所需的轮次可以比其他模型更少。Zeta Labs 看到，与 Opus 5 相比，每个任务的轮次和工具调用更少，成本却几乎只有一半，而且他们最难的任务完成量翻倍。

这并非对每个任务都成立。在[Opus 5.5 上一个任务的成本](https://claude.com/blog/what-a-task-costs-on-opus-5-5)一文中，Addy 写道："在一个范围明确的任务上，两个模型完成所需的轮次大致相同，你得到的只有降价本身。差距在开放式任务上应该最大，因为模型可能把很多轮次浪费在错误的方向上。没有任何单一数字适用于所有代码库，所以要自己去测量。"

换句话说，简单、短小、机械的任务所需的轮次不会有什么变化，而更长、更难的任务则有更多机会让 Opus 5.5 避免把 token 浪费在错误的方案上。省掉一个轮次的成本效益甚至比缓存 token 还要高。

同样值得一提的是，尤其是当 Claude 无人值守或不间断工作的时间更长时——Opus 5.5 的输出速度比 Opus 5 快 30% 以上。这虽然不会提高缓存命中率，也不会减少 token 用量，但意味着长任务中的等待时间更短。

## **保护好你的缓存读取**

随着智能体编码走向成熟，组织已经从要求开发者不计代价地扩张，转向要求开发者高效地扩张。在 Claude Code 中运行 /usage，看看你的用量中有多少是缓存读取。然后保护好这个数字：

- 在会话开始时就选好模型，而不是中途切换；
- 在离开之前就执行上下文压缩（compact），而不是离开之后；
- 如果你使用的是 API 密钥或云厂商，请为长会话设置[一小时缓存生存时间](https://code.claude.com/docs/en/prompt-caching#choose-the-ttl-yourself)。

把 Opus 5.5 用在开放式、重上下文的工作上，让这些习惯复利累积；具体的实测数字请参见[Opus 5.5 上一个任务的成本](https://claude.com/blog/what-a-task-costs-on-opus-5-5)。
