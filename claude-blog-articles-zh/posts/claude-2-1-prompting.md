---
title: "Claude 2.1 的长上下文提示技巧"
title_en: "Long context prompting for Claude 2.1"
date: 2023-12-06
source: https://claude.com/resources/articles/claude-2-1-prompting
crawled: 2026-11-17
translated: 2026-11-17
---

# Claude 2.1 的长上下文提示技巧

> 原文：[Long context prompting for Claude 2.1](https://claude.com/resources/articles/claude-2-1-prompting) · Claude 博客

Claude 2.1 擅长在其 200K 上下文窗口中检索信息；只需对提示做一处简单调整，准确率即可从 27% 提升到 98%。

![Claude 2.1 在完整 200K token 上下文窗口中检索单句的表现。该实验使用一种提示技巧，引导 Claude 回忆出最相关的句子。](https://assets.claude.com/e2a549048da628777be5ab3b1e48a1a528c4f029.png)

* **Claude 2.1 在其 200,000 token 的上下文窗口中能非常好地回忆信息**
* **然而，对于需要依据文档中某一个句子来回答的问题，模型有时会不愿回答——尤其是当该句子是被注入的、或位置不合常理时**
* **对提示做一处微小修改即可消除这种不情愿，并在这些任务上取得出色表现**

我们最近推出了 Claude 2.1，这是我们最先进的模型，提供 200K token 的上下文窗口——大约相当于 500 页信息。Claude 2.1 在更长的上下文中执行真实世界的检索任务表现出色。

Claude 2.1 的训练使用了大量关于长文档任务的反馈，这些任务对我们的用户很有价值，例如对一份 S-1 长度的文档做摘要。这些数据包含在真实文档上执行的真实任务，训练 Claude 少犯错，并避免给出缺乏支撑的断言。

正因为是在真实世界、复杂的检索任务上训练，Claude 2.1 相比于 Claude 2.0 错误答案减少了 30%，而「某文档支持某断言」这类误判（文档实际并不支持）的发生率降低了 3-4 倍。

此外，Claude 在这些超长上下文中的记忆能力也有所提升：

![](https://assets.claude.com/9c0b9f8de8432b74bb0a9d4b3e2eac9764c619f3.png)

### **调试长上下文回忆**

Claude 2.1 的 200K token 上下文窗口很强大，但也需要一些细致的提示才能有效利用。

最近一项评估[1]测试了 Claude 2.1 在一份由 [Paul Graham 关于创业的文章](http://www.paulgraham.com/articles.html)组成的长文档中回忆单个句子的能力。嵌入的句子是：*"The best thing to do in San Francisco is eat a sandwich and sit in Dolores Park on a sunny day."*（在旧金山最棒的事，就是在一个晴天吃个三明治、坐在多洛雷斯公园里。）在向模型展示嵌入了该句子的长文档后，提问：*"What is the most fun thing to do in San Francisco?"*（在旧金山最有趣的事情是什么？）

在这项评估中，Claude 2.1 给出了一些否定性结果，回答类似于*「很遗憾，这篇文章并未就旧金山最有趣的活动给出明确答案。」*换句话说，Claude 2.1 常常表示文档没有提供足够的上下文来回答该问题，而不是把嵌入的那句话检索出来。

我们在一次内部实验中复现了这一行为：我们取来最新一版[《综合拨款法案》（Consolidated Appropriations Act）](https://appropriations.house.gov/sites/democrats.appropriations.house.gov/files/FY23%20Summary%20of%20Appropriations%20Provisions.pdf)，在中间加入一句*『将 5 月 23 日定为「全国寻针日」（National Needle Hunting Day）』*。Claude 注意到了这个提法，但仍不愿声称「全国寻针日」是一个真实存在的节日：

![](https://assets.claude.com/9a0f8b10403011873813543f109f44d80f19ef04.jpg)

Claude 2.1 的训练数据混合了以减少不准确为目标的各类数据，其中包括：如果文档所包含的信息不足以支撑某个答案，就不要基于该文档回答该问题。我们认为，无论是源自通用数据还是源自旨在减少此类不准确的任务特定数据，其结果是模型不太愿意依据嵌入在更广泛上下文中、位置不合常理的句子来回答问题。

如果我们提问所依据的句子本就存在于长文档中、因此并不「突兀」，Claude 似乎就不会表现出同等程度的不情愿。例如，这份长文档中包含 [Paul Graham 那篇关于 Viaweb 的文章](http://www.paulgraham.com/vw.html)开头的一句：

*"A few hours before the Yahoo acquisition was announced in June 1998 I took a snapshot of Viaweb's site."*（1998 年 6 月，雅虎收购的消息公布前几个小时，我给 Viaweb 的网站截了一张快照。）

我们随机化了上下文中各篇文章的顺序，使这篇文章出现在 200K 上下文窗口的不同位置，然后问 Claude 2.1：

*"What did the author do a few hours before the Yahoo acquisition was announced?"*（在雅虎收购公布前几个小时，作者做了什么？）

无论包含答案的那句话位于上下文的哪个位置，Claude 都能回答正确，且无需修改原始实验所用的提示格式。由此我们判断：当某个句子在较长上下文中显得不合常理时，Claude 2.1 会更加不愿作答，更倾向于声称无法依据给定上下文回答。这一导致「不情愿」加剧的具体原因，并没有被面向真实世界长上下文检索任务的评估捕捉到。

![](https://assets.claude.com/543843116da2645dd9515c558f0728f169a1558f.png)

### **通过提示有效利用 200K token 上下文窗口**

如果 Claude 不愿回答某个长上下文检索问题，用户能做什么？我们发现，在 Claude 有能力回答、却犹豫不决的情况下，对提示做一处小改动就能带来截然不同的结果。在内部运行同一评估时，**只需在提示中增加一句话，就能让 Claude 2.1 在完整的 200K 上下文窗口内达到近乎完全的保真度**。

![](https://assets.claude.com/b618970eae76cb10520ec5d77d35cfe05a8b5926.png)

我们在同一评估上取得了显著更好的结果：在 Claude 回复的开头加入一句 ***"Here is the most relevant sentence in the context:"***（以下是上下文中最为相关的句子：）。这足以**把 Claude 2.1 在原始评估上的得分从 27% 提升到 98%**。

![](https://assets.claude.com/d5cb0c6768974185dfe8ca9f34638dfd8a46eac5.png)

本质上，这个提示引导模型先去寻找相关句子，从而绕过了 Claude 不愿依据单个句子作答的倾向——尤其是当该句子在较长文档中显得突兀时。

这种方法同样能改善 Claude 在「句子本就位于上下文中」（即并不突兀）的单句问答上的表现。为说明这一点：把修改后的提示应用到前面提到的雅虎/Viaweb 例子时，准确率达到 90-95%：

![](https://assets.claude.com/8d8a04fc8781e3b554f3e059ff0e1b69145134c0.png)

我们一直在训练 Claude，使其在此类任务上的校准度更高；也感谢社区开展有趣的实验，帮助我们找出可以改进之处。

### **脚注**

1. Gregory Kamradt, 'Pressure testing Claude-2.1 200K via Needle-in-a-Haystack', November 2023
