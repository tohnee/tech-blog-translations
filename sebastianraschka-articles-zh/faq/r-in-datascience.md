---
title: "如今 R 在数据科学中还被广泛使用吗？"
title_en: "Is R used extensively today in data science?"
source: https://sebastianraschka.com/faq/docs/r-in-datascience.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 如今 R 在数据科学中还被广泛使用吗？

"广泛"是个相对的说法，所以让我拿它与其他语言比较着来谈。
我想说，大约 5 到 10 年前，R 可能是做统计或"数据科学"工作首选的语言。如今，随着 Python 科学计算体系（sci-stack）迎头赶上并持续壮大，在类似任务上它的使用广泛程度已与 Python 相当。不过，我预计未来会更进一步转向 Python，因为当前在可扩展性和计算效率方向上似乎有更多的进展。例如：

- Blaze，用于大数据集的核外（out-of-core）分析
- Dask，用于多核机器或分布式集群上的并行计算
- Theano 和 Tensorflow，用于涉及多维数组的数学表达式的优化与求值，
借助 GPU 进行计算，
以及许许多多其他项目。虽然 R 用于"小规模"分析完全没问题，但在真实应用中，性能可能成为（或逐渐成为）R 的一大弱点。
不过请记住，Scala 目前也在强势崛起，比如 Spark。
归根结底，我认为这取决于你想要解决的任务和问题。对于"小型"分析和项目，Python 的默认科学计算体系和 R 都很好用。对于大规模分布式计算，你通常会使用 Spark（用 Scala 编写）。对于深度学习，你使用 Theano 或 Tensorflow（通过 Python），或者 Torch（用 Lua 编写）。

（如果你手里只有一把锤子，那一切看起来都像钉子 :).）
