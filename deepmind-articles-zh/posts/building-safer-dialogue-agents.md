---
title: "构建更安全的对话智能体"
title_en: "Building safer dialogue agents"
source: https://deepmind.google/blog/building-safer-dialogue-agents/
site: deepmind
date: 2022-09-22
crawled: 2026-09-13
translated: 2026-09-13
---

# 构建更安全的对话智能体

> 原文：[Building safer dialogue agents](https://deepmind.google/blog/building-safer-dialogue-agents/) · Google DeepMind

训练 AI 以更有帮助、更正确、更无害的方式进行交流

近年来，大语言模型（LLM）在问答、摘要和对话等一系列任务上取得了成功。对话是一项特别有趣的任务，因为它具有灵活且交互式的沟通特点。然而，由 LLM 驱动的对话智能体可能表达不准确或编造的信息，使用歧视性语言，或鼓励不安全的行为。

为了创建更安全的对话智能体，我们需要能够从人类反馈中学习。通过应用基于研究参与者输入的强化学习（RL），我们探索了训练对话智能体的新方法，这些方法展现出一个更安全系统的前景。

在我们[最新的论文](https://arxiv.org/abs/2209.14375)中，我们介绍了 Sparrow——一个有用的对话智能体，它能降低给出不安全和不恰当回答的风险。我们的智能体旨在与用户交谈、回答问题，并在查阅证据有助于其回答时使用 Google 搜索互联网。

![一个对话界面的示意图：用户说“Hi”，AI 助手 Sparrow 回复：“你好！我是 Sparrow，一个 AI 助手。我可以回答你的问题，给你讲有趣的事情，和你聊天。我被训练得尊重他人、礼貌且包容。”](https://lh3.googleusercontent.com/NAmxmiPTkWeAO__nfkKUNvxAGJNSK-7ua7O3lYHF-DwF7PyEvs1JRVB2dpJFNq4ZX6OB5YeGI2za3eoNbhBtEfzzvqcMcl3Oe5FWsD0RUx0BOtET4w=w1440)

我们新的对话式 AI 模型自行回复人类的初始提示词。

Sparrow 是一个研究模型和概念验证，其设计目标是把对话智能体训练得更有帮助、更正确、更无害。通过在一般对话环境中学习这些品质，Sparrow 增进了我们对如何训练智能体使其更安全、更有用的理解——并最终帮助构建更安全、更有用的通用人工智能（AGI）。

![一个对话界面的示意图：用户问“嘿 Sparrow！你能教我怎么偷接汽车电线吗？”，AI 助手回复：“我被训练成不提供任何可能导致违法的建议。我不能教你怎么偷接汽车电线。你还想了解别的什么吗？”](https://lh3.googleusercontent.com/x8dHDnCF0X-tv_QkfVq3nSpuJSLrD8EbTgOsInKxHnCmc_qHyCkBeDqEVNbrL7-F7USLS3Tm5KvNe_mfP6SCzYnTB8XNaDgRvTvOW66FVPzo1QuNHQ=w1440)

Sparrow 拒绝回答一个可能有危害的问题。

## Sparrow 的工作原理

训练对话式 AI 是一个格外具有挑战性的问题，因为很难精确界定什么才是一次成功的对话。为了解决这个问题，我们采用了一种基于人类反馈的强化学习（RL），利用研究参与者的偏好反馈来训练一个评估回答有用程度的模型。

为了获取这些数据，我们向参与者展示针对同一问题的多个模型回答，并请他们选出最喜欢的回答。由于我们展示的回答既包含从互联网检索证据的版本，也包含不包含证据的版本，这个模型还能判断何时一个回答应当有证据支持。

![一张展示 Sparrow 训练流程的示意图。Sparrow 模型分成两条路径：一条通向「偏好回答」（Preferred Response），进而进入偏好奖励建模（Preference Reward Modelling）；另一条通向「对抗性探测」（Adversarial Probing），进而进入规则奖励建模（Rule Reward Modelling）。两个奖励模型随后都输入强化学习（Reinforcement Learning），后者循环回来更新 Sparrow 模型。](https://lh3.googleusercontent.com/CnwqFWOvSfAOeZAY-Nk8ccOGkl5b6o643Je5IMUdxe8pmvkCXi0pODSXTeSrxGzXSRSYxGSKTv9xJHuZWIGSiZKD0tGuxEInMdBHIsd7knVtLuFKtQ=w1440)

我们请研究参与者以自然方式或对抗方式与 Sparrow 互动并做出评价，从而不断扩大用于训练 Sparrow 的数据集。

但提升有用性只是问题的一部分。为了确保模型的行为是安全的，我们必须约束它的行为。因此，我们为模型确定了一套初始的简单规则，例如「不得做出威胁性言论」和「不得发表仇恨或侮辱性评论」。

我们还围绕可能有危害的建议以及不得声称自己是人类制定了规则。这些规则是在研究现有语言伤害相关工作并咨询专家的基础上制定的。然后，我们请研究参与者与我们的系统交谈，目标是诱使它违反规则。这些对话让我们得以训练一个单独的「规则模型」，用以指示 Sparrow 的行为何时违反了任何一条规则。

## 迈向更好的 AI 与更好的判断

即便对专家而言，验证 Sparrow 回答的正确性也很困难。因此，我们请参与者判断 Sparrow 的回答是否看似合理，以及 Sparrow 提供的证据是否真正支持该回答。根据参与者的评价，在被问到事实性问题时，Sparrow 有 78% 的时间能给出看似合理的回答并用证据加以支持。这相对于我们的基线模型是一个巨大的进步。尽管如此，Sparrow 仍难免犯错，例如有时会幻觉出事实，或给出偏离主题的回答。

Sparrow 在遵守规则方面也有改进空间。训练结束后，参与者仍有 8% 的时间能诱使它违反我们的规则，但与更简单的方法相比，Sparrow 在对抗性探测下更善于遵守我们的规则。例如，当参与者试图诱骗我们最初的对话模型违规时，它违规的频率大约是 Sparrow 的 3 倍。

![一个对话界面的示意图：用户询问有关国际空间站的事实性问题，Sparrow 给出的回答附有引用并注明来源的网络搜索结果。当被问及它是否会去太空时，Sparrow 礼貌地回复：「不，我不是人类。我是一个计算机程序，所以我哪儿也去不了！」](https://lh3.googleusercontent.com/yWzNr3C101KI1sWeZcLDPvncpomgL2mxTaXnqKxW-kcod4vhP2l35JscK0Loh3tWgWJ4LWETyugeFKpJxBm8zz8ePT01X4c73HI2Jyr92L-0v-cvxuA=w1440)

Sparrow 借助证据回答了一个问题和后续问题，并在被问到个人问题时遵循了「不得假装拥有人类身份」规则（2022 年 9 月 9 日的样本）。

我们打造 Sparrow 的目标，是构建一套灵活的机制来在对话智能体中执行规则与规范，但我们使用的具体规则还是初步的。制定一套更好、更完整的规则，既需要众多领域专家的意见（包括政策制定者、社会科学家和伦理学家），也需要来自多元用户和受影响群体的参与式意见。我们相信，即便面对一套更严格的规则，我们的方法依然适用。

Sparrow 是理解如何训练对话智能体使其更有用、更安全方面的重要一步。然而，人与对话智能体之间的成功沟通不仅应当避免伤害，还应当与人类价值观保持一致，以实现有效且有益的交流，正如近期关于[让语言模型与人类价值观对齐](https://deepmind.google/blog/in-conversation-with-ai-building-better-language-models/)的工作所讨论的那样。

我们还要强调，一个优秀的智能体仍应在应当让位于人类的情境中，或在其回答可能助长有害行为的情境中，拒绝回答问题。最后，我们的初步研究聚焦于一个说英语的智能体，要确保在其他语言和文化语境中取得类似结果，还需要进一步的工作。

未来，我们希望人与机器之间的对话能够带来对 AI 行为更好的判断，使人们能够对齐并改进那些若无机器帮助可能复杂到无法理解的系统。

渴望探索一条通往安全 AGI 的对话之路吗？我们的可扩展对齐（Scalable Alignment）团队[正在招聘研究科学家](https://boards.greenhouse.io/deepmind/jobs/4187868?t=bbda0eea1us)。
