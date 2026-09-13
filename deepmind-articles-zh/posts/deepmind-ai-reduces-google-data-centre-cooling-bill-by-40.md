---
title: "DeepMind AI 为谷歌数据中心节省 40% 散热电费"
title_en: "DeepMind AI Reduces Google Data Centre Cooling Bill by 40%"
source: https://deepmind.google/blog/deepmind-ai-reduces-google-data-centre-cooling-bill-by-40/
site: deepmind
date: 2016-07-20
crawled: 2026-09-13
translated: 2026-09-13
---

# DeepMind AI 为谷歌数据中心节省 40% 散热电费

> 原文：[DeepMind AI Reduces Google Data Centre Cooling Bill by 40%](https://deepmind.google/blog/deepmind-ai-reduces-google-data-centre-cooling-bill-by-40/) · Google DeepMind

从智能手机助手到图像识别与翻译，机器学习已经在我们的日常生活中发挥作用。但它也能帮助我们应对世界上一些最具挑战性的物理问题——例如能源消耗。数据中心这类大规模商业与工业系统消耗大量能源，尽管我们已经为[遏制能耗增长](https://blog.google/outreach-initiatives/environment/data-centers-get-fit-on-efficiency/)做了很多，但鉴于世界对计算能力的需求与日俱增，仍有大量工作要做。

降低能耗是我们过去 10 年的一大重点：我们在 Google 打造了自己的[超高效服务器](http://www.google.com/about/datacenters/efficiency/internal/#servers)，发明了[为数据中心散热更高效的方法](http://www.google.com/about/datacenters/efficiency/internal/#water-and-cooling)，并大力投资[绿色能源](https://googleblog.blogspot.com/2015/12/powering-internet-with-renewable-energy.html)，目标是实现 100% 由可再生能源供电。与五年前相比，我们现在用同样多的能源获得了约 3.5 倍的计算能力，而且每年都在持续做出许多改进。

然而，重大突破总是可遇不可求——这正是我们兴奋地想要分享的原因：通过把 DeepMind 的机器学习应用于我们自己的 Google 数据中心，我们成功把散热所用的能源最多降低了 40%。在任何大规模耗能环境中，这都会是巨大的改进；而考虑到 Google 的数据中心本就已高度精密，这是一个了不起的进步。

这对 Google 的数据中心意义重大，因为它有潜力大幅提升能源效率并从整体上减少排放。这还将帮助运行在 Google 云上的其他公司[提升自身的能源效率](https://blog.google/outreach-initiatives/environment/data-centers-get-fit-on-efficiency/)。虽然 Google 只是世界上众多数据中心运营商之一，但许多运营商并不像我们这样使用可再生能源供电。数据中心效率的每一次提升都会减少排入环境的总排放量；借助 DeepMind 的这类技术，我们可以用机器学习消耗更少的能源，帮助应对所有挑战中最严峻的一个——气候变化。

数据中心环境中能源消耗的主要来源之一就是散热。正如你的笔记本电脑会产生大量热量，我们的数据中心——其中运行着支撑 Google 搜索、Gmail、YouTube 等服务的服务器——也会产生大量必须排出的热量，才能让服务器持续运转。散热通常依靠大型工业设备完成，例如泵、冷水机组和冷却塔。然而，像数据中心这样的动态环境，由于以下几个原因，很难做到最优运行：

1. 设备本身、我们对设备的操作方式与环境之间，以复杂的非线性方式相互作用。传统的基于公式的工程方法和人类直觉往往无法捕捉这些相互作用。
2. 系统无法快速适应内部或外部的变化（例如天气）。这是因为我们无法为每一种运行场景都制定规则与启发式方法。
3. 每个数据中心都有独特的架构和环境。为某个系统定制的模型未必适用于另一个系统。因此，需要一个通用的智能框架来理解数据中心的相互作用。

为解决这个问题，我们在两年前就开始应用[机器学习](https://googleblog.blogspot.com/2014/05/better-data-centers-through-machine.html)来更高效地运营数据中心。在过去几个月里，DeepMind 的研究人员开始与 Google 的数据中心团队合作，显著提升系统的效用。我们利用一组神经网络——它们在我们的数据中心内不同运行场景和参数上训练而成——创建了一个更高效、更具适应性的框架，以理解数据中心动态并优化效率。

我们的做法是：利用数据中心内数千个传感器已经采集的历史数据——例如温度、电力、泵速、设定值等——训练一个深度神经网络集成。由于我们的目标是提升数据中心能源效率，我们以未来的平均 PUE（电源使用效率，Power Usage Effectiveness）为目标训练神经网络。PUE 定义为建筑总能耗与 IT 能耗之比。随后，我们又训练了两个额外的深度神经网络集成，用来预测数据中心未来一小时内的温度与压力。这些预测的目的是对 PUE 模型推荐的措施进行模拟验证，确保我们不会越过任何运行约束。

我们把模型部署到一个实际运行的数据中心上进行了测试。下图展示了典型一天的测试情况，包括我们开启机器学习建议的时刻和关闭的时刻。

![折线图，展示电源使用效率（PUE）随时间的变化。当「ML Control」（机器学习控制）开启时，PUE 水平急剧下降并持续保持低位；一旦「ML Control」关闭，PUE 立即反弹回更高、波动更大的水平。](https://lh3.googleusercontent.com/u6MGmmxkUoxkeZpkYKVssormqoxu4Birec6GFL39HbTa1rCGnrr5HRKye6bIbVxRkP-m9TKR1LLf0E-axsloDl5NKd5BN0TpewAN7ZOixLT4CuYHjQ=w1440)

我们的机器学习系统能够持续实现散热能耗降低 40%——在计入电力损耗及其他非散热低效因素之后，相当于整体 PUE 开销降低 15%。它还创下了该站点有史以来最低的 PUE。

由于该算法是一个理解复杂动力学的通用框架，我们计划在接下来的几个月里把它应用于数据中心环境中乃至更广泛领域的其他挑战。这项技术可能的应用包括：提高电厂转换效率（从同样单位的输入中获得更多能源）、降低半导体制造的能源与水耗，或帮助制造设施提高产量。

我们计划把这套系统推广得更广，并将在即将发表的一篇文章中分享我们的具体做法，让其他数据中心和工业系统运营商——并最终让环境——都能从这一重大进步中受益。
