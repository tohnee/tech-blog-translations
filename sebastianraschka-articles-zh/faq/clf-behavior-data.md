---
title: "用于可视化分类器行为的玩具数据集"
title_en: "Toy Datasets for Visualizing Classifier Behavior"
source: https://sebastianraschka.com/faq/docs/clf-behavior-data.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 用于可视化分类器行为的玩具数据集

> 原文：[Toy Datasets for Visualizing Classifier Behavior](https://sebastianraschka.com/faq/docs/clf-behavior-data.html) · Sebastian Raschka's FAQ

可视化这部分有点棘手，因为我们人类只能看一维到三维的图形。不过，我仍然要说 Iris 是观察分类器行为最有用的玩具数据集之一（见下图）。

![](https://sebastianraschka.com/images/faq/clf-behavior-data/iris.png)

（如果你有兴趣，我在这里实现过这个简单的函数：[mlxtend plot\_decision\_regions](https://rasbt.github.io/mlxtend/user_guide/plotting/plot_decision_regions/)。）
除此之外，我认为像"XOR"、"半月形"（half-moons）或同心圆这样的合成数据集，是在非线性问题上评估分类器的不错候选：

---

![](https://sebastianraschka.com/images/faq/clf-behavior-data/xor.png)

---

![](https://sebastianraschka.com/images/faq/clf-behavior-data/moons.png)

---

![](https://sebastianraschka.com/images/faq/clf-behavior-data/circles.png)
