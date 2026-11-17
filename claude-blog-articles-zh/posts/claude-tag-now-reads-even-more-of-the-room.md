---
title: "Claude Tag 现在更会察言观色了"
title_en: "Claude Tag now reads even more of the room"
date: 2026-08-13
source: https://claude.com/resources/articles/claude-tag-now-reads-even-more-of-the-room
crawled: 2026-11-17
translated: 2026-11-17
---

# Claude Tag 现在更会察言观色了

> 原文：[Claude Tag now reads even more of the room](https://claude.com/resources/articles/claude-tag-now-reads-even-more-of-the-room) · Claude 博客

Claude 掌握了更多上下文，能更好地判断何时在 Slack 中主动协作（以及何时不该）

Claude Tag 让你把 Claude 加入 Slack 频道，与你的团队并肩工作。当你 @ 提及时 Claude 会回应，当它认为有帮助时也会主动回应。

以前，Claude 一次只能看到**一条消息**，因此它做出主动行动的决定时，依据的是眼前这一条消息，而不是周围更广泛的上下文。

现在，Claude 会利用**整个频道的上下文**，以及它的记忆和你给它的常设指令，来判断何时参与对话。

结果是，Claude 现在判断何时该主动回应、何时不该的能力提升了约 30%。

本次更新目前不额外收费。虽然持有更多上下文确实会增加 Claude Tag 的用量，但 Claude Tag 所持有的额外上下文不计入任何套餐的用量或支出限额。

## 从被动应答者到主动参与者

以前，由一个轻量级分类器决定 Claude 是否应当行动。它逐条单独查看每条新消息，做出一个是或否的判断。

例如，下面是两位工程师从相反的方向追同一个 bug。两人都抽不出一小时把它查到底，而且两条消息都没有提出任何请求。

![](https://assets.claude.com/accdcc7ea246bffe057f3186ee58ee7c906872fb.png)

Priya 有一个猜想，Devon 手上有证据。两条消息都不是发给 Claude 的，也都没有提出任何请求。

逐条来看，两条消息都不是给 Claude 的，因此分类器正确地什么都不做——而且是两次正确地什么都不做。合起来看，这里明显摆着一件该做的事：一位工程师有猜想，另一位有支持它的证据，而谁都没时间去核实。

移除分类器后，Claude 利用整个频道的上下文，从四种动作中选择一种：

* **就地回复**，当答案是简短的、可验证的，并且是频道中尚不知道的内容时。
* **在话题串（thread）中开始更深入的工作**，当某条消息值得投入真正的时间时。
* **把消息转到它正在进行的工作中**，当这条消息能为 Claude 已经开启的工作流补充内容时。
* **什么都不说**，当没有需要它做的事时。

下面是同一段对话在 Claude Tag 使用额外上下文后的表现。即使没有被 @ 提及，Claude 也选择了第二种动作。它看到 Priya 的假设和 Devon 的证据，开启一个话题串并让调查随之展开，把两位工程师都拉了进来。它的行动始终在你配置的权限、工具和范围内。

![](https://assets.claude.com/1be7311c2a5a8aa622ef0bd9979c41b4c80dd743.png)

同一话题串，两分钟后。Claude 把两条消息合起来读，开始动手。没有被 @ 提及。

对话之间并非彼此隔绝。所以当 Devon 发布更新时，它会落到正确的工作流中；当两项调查最终发现是同一个 bug 时，这层联系也会被建立起来。

![](https://assets.claude.com/7c5006eaeb8866edbc525ceffd925a2b9b60d9de.png)

Claude 现在会查看所有消息，以理解频道的完整上下文，从而更准确地判断是否应当在无人提示的情况下参与对话。

## Claude 如何决定何时不说话

一个烦人的智能体比一个帮不上忙的智能体更糟。我们构建 Claude Tag 的原则是只在有用时才出声，而在大多数频道、对大多数消息而言，这意味着什么都不说。

我们的做法是，用一套评分准则（rubric）来给 Claude 在每个频道中的选择打分，准则基于这些原则：这条评论有多大用处、Claude 对回答有多大把握，以及是否有更适合回应的人。

Claude 也知道何时该停止关注，类似于人们使用 Slack 的方式。它会密切关注少数几个频道，对其他频道关注较少，直到有人把它 @ 进来。在某个频道里，如果一条又一条消息之后 Claude 都得出「自己没什么可补充」的结论，它就会进入休眠；一次 @ 提及会立刻把它唤醒。

你也可以用大白话引导它的回应行为：「除非有人 @ 你，否则永远不要在这里回应」，或者「凡是和部署流水线相关的内容，都可以随时插话」。

如果你希望 Claude 只在有人 @ 它时才在某个频道说话，[任何成员都可以关闭「**自动回应**」（Respond automatically）](https://claude.com/docs/claude-tag/users/when-claude-responds#turn-automatic-replies-on-or-off)。

## 第一条回复更快了

额外的上下文也让 Claude 能更快回应。它会在几秒内先回应你，而不是在启动时默默工作。工作本身所需的时间和以前一样；消失的是那沉默的第一分钟——那时你无法判断它到底有没有听到你。

## 现已上线

本次更新现已覆盖 Claude Tag，面向 Claude Teams 和 Enterprise 客户提供。你可以从[这里](https://claude.ai/admin-settings/claude-tag)开始使用。Claude 现在是一个更高效的协作者：能跟上对话，自行决定何时行动、何时不挡路。

把 Claude 加入一个频道，看看它能为你的对话增添什么。进一步了解 [Claude Tag](https://claude.com/product/tag)。
