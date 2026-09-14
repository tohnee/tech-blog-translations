---
title: "为什么决策树使用熵而不是分类误差"
title_en: "Why Decision Trees Use Entropy Instead of Classification Error"
source: https://sebastianraschka.com/faq/docs/decisiontree-error-vs-entropy.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 为什么决策树使用熵而不是分类误差

> 原文：[Why Decision Trees Use Entropy Instead of Classification Error](https://sebastianraschka.com/faq/docs/decisiontree-error-vs-entropy.html) · Sebastian Raschka's FAQ

在进入正题——也就是真正有趣的部分——之前，我们先来看一些（分类）决策树的基础知识，确保我们的理解一致。

## 基本算法

1. 从根节点开始，将其作为父节点
2. 在特征 *xi* 上划分父节点，以使子节点不纯度之和最小（即最大化信息增益）
3. 将训练样本分配到新的子节点
4. 若叶节点已纯净或满足早停准则则停止；否则对每个新的子节点重复步骤 1 和 2

## 停止规则

1. 叶节点已纯净
2. 达到最大节点深度
3. 划分某个节点不再带来信息增益\*

\* 这正是后文将要看到的关键之处。

## 不纯度度量与信息增益

形式上，我们可以把「信息增益」写成

![](https://sebastianraschka.com/images/faq/decisiontree-error-vs-entropy/ig.png)

![](https://sebastianraschka.com/images/faq/decisiontree-error-vs-entropy/ig_xp.png)

（注意，由于父节点的不纯度是一个常数，我们也可以直接计算子节点不纯度的平均值，效果相同。）
为简单起见，我们只将「熵」准则与分类误差进行比较；不过，同样的概念也适用于基尼指数（Gini index）。

我们将熵的公式写作

![](https://sebastianraschka.com/images/faq/decisiontree-error-vs-entropy/entropy_eq.png)

它对所有非空类别 *p(i* ❘ *t)* ≠ 0 成立，其中 *p(i* ❘ *t)* 是属于特定节点 *t* 上类别 *i* 的样本所占的比例（或频率、概率）；*C* 是唯一类别标签的数量。

![](https://sebastianraschka.com/images/faq/decisiontree-error-vs-entropy/entropy_plot.png)

尽管大家对分类误差都非常熟悉，出于完整性考虑，我们还是把它写出来：

![](https://sebastianraschka.com/images/faq/decisiontree-error-vs-entropy/error_eq.png)

![](https://sebastianraschka.com/images/faq/decisiontree-error-vs-entropy/error_plot.png)

## 分类误差 vs. 熵

正如承诺的那样，接下来是更有趣的部分。我们考虑下面这棵二叉树，其训练集包含 40 个「正」类训练样本（y=1）和 80 个「负」类训练样本（y=0）。此外，假设可以构造出 3 个划分准则（基于 3 个二值特征 x1、x2 和 x3），它们都能完美地把训练样本分开：

![](https://sebastianraschka.com/images/faq/decisiontree-error-vs-entropy/Slide1.png)

那么，以最小化分类误差作为准则函数，能学出这个假设（即树模型）吗？我们来算一算：

![](https://sebastianraschka.com/images/faq/decisiontree-error-vs-entropy/Slide2.png)

可以看到，第一次划分之后的信息增益恰好为 0，因为两个子节点的平均分类误差与父节点的分类误差完全相同（40/120 = 0.3333333）。在这种情况下，划分初始训练集在分类误差这一准则下不会带来任何改进，因此树算法会在这一步就停止（要使这一论断成立，我们还得假设在特征 x2 或 x3 上划分同样不会带来信息增益）。

接下来，看看使用熵作为不纯度度量会发生什么：

![](https://sebastianraschka.com/images/faq/decisiontree-error-vs-entropy/Slide3.png)

与平均分类误差不同，子节点的平均熵**不**等于父节点的熵。因此，划分规则会继续进行，直到子节点变纯（再划分两次之后）。那么，为什么会这样？为了给出直观的解释，我们把熵的曲线图放大来看：

![](https://sebastianraschka.com/images/faq/decisiontree-error-vs-entropy/entropy_annotated.png)

绿色方块是上面决策树模型中前两个子节点在 p(28/70) 和 (12/50) 处的熵值，二者由一条绿色（虚）线相连。回顾一下：决策树算法的目标是找到那样的特征和划分值，使得子节点的平均不纯度相对于父节点下降最大。
于是，如果我们有 2 个熵值（左子节点和右子节点），它们的平均值会落在这条连接直线上。
然而**——这才是关键所在——**我们可以看到，由于熵的「钟形」形状，该平均值处的熵总是大于平均熵，这就是为什么与分类误差不同，我们会继续不断地划分节点。
