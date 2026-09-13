---
title: "寻找准确的 AI 信息"
title_en: "Finding Accurate AI Information"
source: https://sebastianraschka.com/blog/2023/chatgpt-dilemma.html
crawled: 2026-09-06
translated: 2026-09-06
---

# 寻找准确的 AI 信息

> 原文：[Finding Accurate AI Information](https://sebastianraschka.com/blog/2023/chatgpt-dilemma.html)

像 ChatGPT 这样的对话式聊天机器人，短期内恐怕还无法取代传统搜索引擎和专家知识。互联网上充斥着海量的错误信息，区分可靠来源与不可靠来源的能力依然既具挑战性又至关重要。

## 大致正确却错误的答案

试想让 [ChatGPT](https://chat.openai.com) 解释*权重衰减（weight decay）*——深度学习中一种流行的正则化技术。遗憾的是，它的回答是错误的——它把权重衰减与相关但略有不同的损失函数 \(L\_2\) 正则化混为一谈：

> “权重衰减最常见的形式是 L2 正则化，它在损失函数中加入一项与权重平方成正比的项。[……]具体做法是在损失函数中加入一项，该项为网络中所有权重平方之和。”

![ChatGPT 困境 截图 1](https://sebastianraschka.com/images/blog/2023/chatgpt-dilemma/chat-gpt-dilemma-1.webp)

接着我试了 [Perplexity AI](https://www.perplexity.ai)，这是一个会为所给信息引用来源的大语言模型。顺着这些来源追查下去，我发现问题并不在于大语言模型（LLM）“凭空想象”出这些事实，而在于训练数据本身就存在事实性错误：

> “权重衰减的实现方式是：在神经网络的代价函数中加入一个惩罚项，其效果是在反向传播过程中使权重收缩。”

![ChatGPT 困境 截图 2](https://sebastianraschka.com/images/blog/2023/chatgpt-dilemma/chat-gpt-dilemma-2.webp)

有人可能会说，只要只提供事实正确的训练数据就能解决这个问题。这当然是可行的，但目前还不具备可操作性。

## 在应对，但尚未解决问题

大语言模型需要海量训练数据，才能学会写出语法正确、读起来通顺的文本。但语法正确并不等于事实正确。为了缓解错误信息带来的问题，InstructGPT 背后的研究者开发了一套三步方法：

1. 使用监督学习，用人类撰写的提示词（prompt）对一个预训练 LLM 进行微调。
2. 让人类对各种提示词的不同回答按 1–5 分进行排序，并用这些数据训练一个[奖励模型](https://sebastianraschka.com/glossary/#rlhf "RLHF (Reinforcement Learning from Human Feedback)")。
3. 用这个奖励模型来微调第 1 步得到的 LLM。

这一三步流程概括在下图（来自 [InstructGPT 论文](https://arxiv.org/abs/2203.02155)）中：

![ChatGPT 困境 截图 3](https://sebastianraschka.com/images/blog/2023/chatgpt-dilemma/chat-gpt-dilemma-3.webp)

OpenAI 雇用了 40 名外包人员为提示词生成回答，通过监督微调和人机协同（human-in-the-loop）的强化学习开发出 InstructLLM，如上图所概括。虽然具体细节尚未公开，但 ChatGPT 遵循的是类似的配方，只是投入的人力资源规模大得多。

## 为了学会正确答案而制造正确答案——一个资源困境

困境在于：当前一代 LLM 需要海量数据，即便雇用数千名人类专家来整理训练数据，最终得到的数据可能仍不足以微调这些模型——因为许多主题上的高质量信息本来就稀缺。

既然事实正确的信息可能过于稀缺，解决办法或许是创造更多事实准确的数据来训练这些 LLM。那么显而易见的问题是：*如果我们本可以直接阅读和引用这些资源，那专门为 ChatGPT 生产多篇关于权重衰减的文章作为训练素材，意义何在？*

## 结论：LLM 有用，但不是万能解药

像 ChatGPT 这样的对话式聊天机器人非常令人惊叹。作为写作工具它们也很趁手，比如用来改写笨拙的句子。然而，批判性地评估这些模型的输出，并用人类的判断来确定它们的用处和适用范围，依然十分重要。

**我们希望在未来看到的一个趋势是：当我们为技术问题寻求事实正确的答案时，重新回归由可信专家精心整理的资源。**

（与此同时，我会持续关注下一代能把参考文献引用整合进回答的 LLM。例如，[DeepMind 计划在 2023 年发布它的 Sparrow 模型](https://time.com/6246119/demis-hassabis-deepmind-interview/)。在那之前，我会把“什么是权重衰减”这个查询先搁置备用。）

## 那么，*权重衰减*到底是什么？

在上面你已经看到了针对*权重衰减*这个查询的各种错误回答。如果你好奇正确的解释是什么——即便使用 Google 这样的传统搜索引擎，也需要花一番功夫才能找到一个给出正确解释的[可信资源](https://paperswithcode.com/method/weight-decay)：

> “权重衰减可以直接并入权重更新规则，而不只是通过目标函数来隐式定义。通常来说，权重衰减指的是直接在权重更新规则中加以指定的实现方式（而 L2 正则化通常指在目标函数中指定的实现方式）。”

![ChatGPT 困境 截图 4](https://sebastianraschka.com/images/blog/2023/chatgpt-dilemma/chat-gpt-dilemma-4.webp)
