---
title: "发现系统中何时存在智能体"
title_en: "Discovering when an agent is present in a system"
source: https://deepmind.google/blog/discovering-when-an-agent-is-present-in-a-system/
site: deepmind
date: 2022-08-18
crawled: 2026-09-13
translated: 2026-09-13
---

# 发现系统中何时存在智能体

> 原文：[Discovering when an agent is present in a system](https://deepmind.google/blog/discovering-when-an-agent-is-present-in-a-system/) · Google DeepMind

智能体性的新形式化定义为 AI 智能体的因果建模及其面临的激励提供了清晰的原则

我们希望构建安全、对齐的通用人工智能（AGI）系统，使其追求设计者预期的目标。[因果影响图](https://deepmindsafetyresearch.medium.com/progress-on-causal-influence-diagrams-a7a32180b0d1#b09d)（Causal influence diagrams，CIDs）是一种对决策情境建模的方式，让我们能够推理[智能体激励](https://ojs.aaai.org/index.php/AAAI/article/view/17368)。例如，下面是一个单步马尔可夫决策过程——决策问题的典型框架——的 CID。

![一幅单步马尔可夫决策过程的因果影响图（CID）：机会节点 S1 通过虚线信息链连接到决策节点 A1，S1 和 A1 又通过实线因果链连接到第二个机会节点 S2，后者进而指向一个黄色菱形效用节点 R2。](https://lh3.googleusercontent.com/9sLgX1JVVqsmVfCGd6hoLuun3F7u8f2wfww-9XW-a0Ik2vkVvXzZbfoHUXpGNyW5PtJgyYkDfApwy6oFQ5aQtEVlJlgbXqKrNKGjClUBQzY4Fg-NuWk=w1440)

S1 表示初始状态，A1 表示智能体的决策（方块），S2 表示下一状态。R2 是智能体的奖励/效用（菱形）。实线链表示因果影响。虚线边表示信息链——即智能体做决策时知道什么。

通过将训练设置与塑造智能体行为的激励联系起来，CIDs 有助于在训练智能体之前阐明潜在风险，并能启发更好的智能体设计。但我们如何知道一个 CID 何时才是对训练设置的准确建模？

我们的新论文 [Discovering Agents](https://arxiv.org/abs/2208.08345) 引入了应对这些问题的新方法，包括：

- 第一个智能体的形式化因果定义：**智能体是那样一些系统——如果其行动以不同的方式影响世界，它们会调整自己的策略**
- 一个从经验数据中发现智能体的算法
- 因果模型与 CIDs 之间的转换方法
- 解决了此前对智能体进行错误因果建模所导致的混淆

综合起来，这些结果额外提供了一层保障，确保没有发生建模错误，这意味着 CIDs 可以被更有把握地用于分析智能体的激励与安全性质。

## 示例：把一只老鼠建模为智能体

为了帮助说明我们的方法，考虑下面这个例子：一个由三个方格组成的世界，一只老鼠从中间方格出发，选择向左或向右走，到达下一个位置，然后可能得到一些奶酪。地面结了冰，所以老鼠可能打滑。奶酪有时在右边，有时在左边。

![一幅插图：三个水平方格组成的网格，左侧方格为空，中间方格里有一只老鼠，右侧方格里有一块奶酪。](https://lh3.googleusercontent.com/dBDVGmGiiliQicECrVvgvB32eDL5CrYoQ09puR61QyuwYVdDThCW0Vnz0TXM-NcN5iH4iCbVUncaZj4XqRQFOguN0qbLKMF65jSpBO2r0sWMkBXwQoQ=w1440)

老鼠与奶酪的环境。

这可以用下面的 CID 表示：

![一幅表示老鼠示例的因果影响图（CID）：标注为「左/右」的粉色方块决策节点 D 指向标注为「新位置」的白色圆形机会节点 X，后者进而指向标注为「得到奶酪」的粉色菱形效用节点 U。](https://lh3.googleusercontent.com/4NkJeGra3AzkhYM01q4ivyFIb-3W6QMmmSBkF6fSeaxen0i7gF-rFci3HV61FTKE92jcxJHf71gV8D0OtmNjKx9Nib8F33jAYCMhJE-avHqIK-l86g=w1440)

老鼠的 CID。D 表示左/右的决策。X 是老鼠执行左/右动作后的新位置（它可能打滑，意外滑到另一侧）。U 表示老鼠是否得到奶酪。

「老鼠会针对不同的环境设置（冰面湿滑程度、奶酪分布）选择不同行为」这一直觉可以用[机械化因果图](https://drive.google.com/file/d/1_OBLw9u29FrqROsLfhO6rIaWGK4xJ3il/view)来刻画，它对每个（对象层）变量都附有一个机制变量，用以刻画该变量如何依赖于其父节点。关键在于，我们允许机制变量之间存在链路。

该图包含额外的黑色机制节点，分别代表老鼠的策略、冰面湿滑程度和奶酪分布。

![一幅老鼠示例的机械化因果图。下方三个白色圆形节点表示对象层变量：D（左/右）指向 X（新位置），X 指向 U（得到奶酪）。上方三个黑色方块机制节点支配着它们：Policy（D-tilde）指向 D，Iciness（X-tilde）指向 X，Cheese distribution（U-tilde）指向 U。机制链路包括一条从 X-tilde 到 D-tilde 的黑色虚线箭头，以及一条从 U-tilde 到 D-tilde 的蓝色点划线箭头（表示末端边）。](https://lh3.googleusercontent.com/le3eeno-1GJCNqurogpt_oTLdxvLTJgOlwZPw2JKDCDRqbgbUmzssNZZZ4aYzvI-yx0sJyBPJt4lTiUSb3E6T3OEqPrJKoYbNTJk4BvBhCqL32hdEg=w1440)

老鼠与奶酪环境的机械化因果图。

机制之间的边代表直接的因果影响。蓝色的边是特殊的末端边——大致而言，即使对象层变量 A 被改变以致不再有任何出边，机制边 A~ → B~ 依然存在。

在上面的例子中，由于 U 没有子节点，它的机制边必然是末端边。但机制边 X~ → D~ 不是末端边，因为如果我们把 X 与其子节点 U 切断，老鼠将不再调整它的决策（因为它的位置不再影响它能否得到奶酪）。

## 智能体的因果发现

因果发现从涉及干预的实验中推断因果图。特别地，可以通过对变量 A 进行实验干预并检查 B 是否响应来发现从 A 到 B 的箭头，即使所有其他变量都保持不变。

我们的第一个算法使用这一技术来发现机械化因果图：

![一幅「算法 1」的插图：将三格网格中试图获取奶酪的老鼠这一物理设置，映射到对应的机械化因果图。](https://lh3.googleusercontent.com/Ij9NGAAMEVJF4j9SnD1FQ85PrEON3_crqniJPAa1IzeOMxs2Jfv5EkJI7gpU-XWxDmu2mIakQzRqu1EWZj3CpIIAL34HpGKSFg_nINM4TC67N99ZNr0=w1440)

算法 1 以来自系统（老鼠与奶酪环境）的干预数据为输入，使用因果发现输出一个机械化因果图。详见论文。

我们的第二个算法将这个机械化因果图转换为博弈图：

![一幅「算法 2」的插图：将左侧的机械化因果图转换为右侧的博弈图。](https://lh3.googleusercontent.com/Oct9eHFPBn5YIgrQsothpBGaiBEJW99PlNkLkgE4w134kcVi9SM_kYcJzkmrQpLpfjseN7qgSIyByHmyevv5FLocCxMgxppo0sXGuOLXONvtnp81yFg=w1440)

算法 2 以机械化因果图为输入，并将其映射为博弈图。入边的末端边表示决策，出边的末端边表示效用。

将算法 1 与算法 2 相结合，我们便能从因果实验中发现智能体，并用 CIDs 来表示它们。

我们的第三个算法将博弈图转换为机械化因果图，从而在某些附加假设下让我们可以在博弈图与机械化因果图两种表示之间转换：

![一幅「算法 3」的插图：将左侧的博弈图转换为右侧的机械化因果图。](https://lh3.googleusercontent.com/l0_pbDgVLJ_TFcp6pwJAcrQugRgqq3kMIc7cz-4eOBNcaiAgZF_qdsopcdp7oKoifuv753pemAv1jBwcxOQJdHOP-pZ54WeskcSyFGZzMl2h_a84=w1440)

算法 3 以博弈图为输入，并将其映射为机械化因果图。决策表示一条入侧末端边，效用表示一条出侧末端边。

## 用于建模 AI 智能体的更好安全工具

我们提出了第一个智能体的形式化因果定义。立足于因果发现，我们的关键洞见是：智能体是那些会针对「其行动影响世界的方式」的变化而调整自身行为的系统。事实上，我们的算法 1 和算法 2 描述了一个精确的实验流程，可以帮助评估一个系统中是否包含智能体。

对 AI 系统因果建模的兴趣正在迅速增长，而我们的研究将这种建模建立在因果发现实验之上。我们的论文通过改进若干示例 AI 系统的安全分析，展示了这一方法的潜力，并表明因果性是发现系统中是否存在智能体的一个有用框架——这是评估 AGI 风险时的一个关键关切。

有兴趣了解更多吗？请查阅我们的[论文](https://arxiv.org/abs/2208.08345)。非常欢迎反馈与评论。
