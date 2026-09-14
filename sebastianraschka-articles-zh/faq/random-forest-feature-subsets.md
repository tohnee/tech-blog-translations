---
title: "随机森林在每个树还是每个节点上做特征采样"
title_en: "Random Forest Feature Sampling at Each Tree or Node"
source: https://sebastianraschka.com/faq/docs/random-forest-feature-subsets.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 随机森林在每个树还是每个节点上做特征采样

这是个好问题，因为 Tin Kam Ho 早期的随机决策森林使用的是"随机子空间方法"（random subspace method），即每棵树获得一个随机特征子集。

> "Our method relies on an autonomous, pseudo-random procedure to select a small number of dimensions from a given feature space …"

- Ho, Tin Kam. "The random subspace method for constructing decision forests." IEEE transactions on pattern analysis and machine intelligence 20.8 (1998): 832-844.

然而几年之后，Leo Breiman 描述了为每个节点选择不同特征子集的做法（而每棵树拥有完整的特征集合）——Leo Breiman 的表述已成为如今我们谈论"随机森林"时通常所指的那个"招牌"随机森林算法。

> "… random forest with random features is formed by selecting at random, at each node, a small group of input variables to split on."

- Breiman, Leo. "Random Forests" Machine learning 45.1 (2001): 5-32.

回答你的问题：每棵树都获得完整的特征集合，但在每个节点上，只考虑一个随机的特征子集。
