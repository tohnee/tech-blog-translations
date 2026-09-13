---
title: "安全优先：用于数据中心自主散热与工业控制的 AI"
title_en: "Safety-first AI for autonomous data centre cooling and industrial control"
source: https://deepmind.google/blog/safety-first-ai-for-autonomous-data-centre-cooling-and-industrial-control/
site: deepmind
date: 2018-08-17
crawled: 2026-09-13
translated: 2026-09-13
---

# 安全优先：用于数据中心自主散热与工业控制的 AI

> 原文：[Safety-first AI for autonomous data centre cooling and industrial control](https://deepmind.google/blog/safety-first-ai-for-autonomous-data-centre-cooling-and-industrial-control/) · Google DeepMind

社会上许多最紧迫的问题正变得日益复杂，寻找解决方案的过程有时令人感到无从下手。在 DeepMind 和 Google，我们相信，如果能把 AI 用作发现新知识的工具，解决方案就会更容易找到。

2016 年，我们共同开发了一个[由 AI 驱动的推荐系统](https://deepmind.com/blog/article/deepmind-ai-reduces-google-data-centre-cooling-bill-40)，用于提升 Google 本已高度优化的数据中心的能源效率。我们的想法很简单：即便是微小的改进，也能带来可观的能源节约并减少二氧化碳排放，帮助应对气候变化。

现在，我们正在把这一系统推向新的高度：我们的 AI 系统不再是由人来执行建议，而是直接控制数据中心散热，同时仍处于我们数据中心运营专家的监督之下。这一开创性的云端控制系统如今已在多个 Google 数据中心安全地实现能源节约。

## 工作原理

每隔五分钟，我们的云端 AI 会从数千个传感器获取数据中心散热系统的快照，并将其输入我们的深度神经网络，由后者预测各种潜在动作组合将如何影响未来的能耗。然后，AI 系统会找出在满足一整套严格安全约束的前提下能够将能耗降到最低的动作。这些动作被发送回数据中心，由本地控制系统验证后执行。

![每隔五分钟，我们的云端 AI 从数千个物理传感器所代表的数据中心散热系统中提取一份快照。](https://lh3.googleusercontent.com/0u87s3Hmu328SX5o5WysUdebSgB7O5VsLslrh4Y-5B7o9XEVRHydVwywUpGxZawCRaJR-0A5CfNADcBjQl8078ui4F4UF_af6YjYnIOiBPBCS8nSqus=w1440)

![这些信息被输入我们的深度神经网络，由其根据候选动作预测未来的能源效率和温度。](https://lh3.googleusercontent.com/pJPaHFVd8tqwC3P04djE-pvBPwsu1YNOYOG_vj13IcNW6FtpDEin1zd3DvEFh3IOi-9cIbEihwf8N6sbUttpiLDWJBwurJCRFZclZ5ndMCRVsR4lcw=w1440)

![AI 会选择既满足安全约束又能将未来能耗降到最低的动作。](https://lh3.googleusercontent.com/g-0Xb_Ky85xmxKNCqTI1YeMNydKIQ1deGvhm3WgDMfiaEcqBblMBXrND0qepkMZNfcKeZlLv_VzPrKTKMQQSoqZbwOhNZZJ8GR2mhicxEK4xDOd7Gg=w1440)

![最优动作被发送回数据中心，本地系统在执行前会根据自身的安全约束对它们进行验证。](https://lh3.googleusercontent.com/iN32ajXdFb8a4Q-Rj7efUkmLL27f0fgKA0xwzJbEQNfzC7zSzWbO4yzITRvEKdBqw6M8W_pSaoHcfDYRFEaakT0_Ss2fI_PfINNIrax1DrfogN8dyuQ=w1440)

这一想法源于一直使用我们 AI 推荐系统的数据中心运营人员的反馈。他们告诉我们，尽管该系统教给他们一些新的最佳实践——例如把散热负载分配到更多而非更少的设备上——但执行这些建议需要运营人员投入过多的精力和监督。他们自然想知道，我们能否在不进行人工执行的情况下取得类似的节能效果。

我们很高兴地告诉大家：答案是肯定的！

## 为安全与可靠性而设计

Google 的数据中心容纳着数千台服务器，为包括 Google 搜索、Gmail 和 YouTube 在内的热门服务提供支持。确保它们可靠、高效地运行是关乎使命的大事。我们从零开始设计 AI 智能体和底层控制基础设施时，就把安全和可靠性放在首位，并采用八种不同的机制来确保系统在所有时刻都按预期运行。

![一座庞大 Google 数据中心的俯视图，里面排列着一排排服务器和顶置散热基础设施。](https://lh3.googleusercontent.com/KnVOqqkDQFl8lhedIsVxOCoxHcA8mSxxwfvvjIeRcs1M5MPFLqDVFDOITFhDatN582sB5_0Iwy0m4eKaPxPSOtVMpBH2TCiOpkaslBhff1heeN65kA=w1440)

我们实现的一种简单方法是估计不确定性。对于每一个潜在动作——数量可达数十亿——我们的 AI 智能体会计算自己对「这是一个好动作」的置信度。置信度低的动作会被排除在考虑范围之外。

另一种方法是双层验证。AI 计算出的最优动作会先对照由我们数据中心运营人员定义的内部安全约束清单进行审核。当指令从云端发送到物理数据中心后，本地控制系统会再根据它自己的一套约束对指令进行验证。这种冗余校验确保系统保持在本地约束之内，同时运营人员始终保持对运行边界的完全控制。

最重要的是，我们的数据中心运营人员始终掌握控制权，可以随时选择退出 AI 控制模式。在这种情况下，控制系统将无缝地从 AI 控制切换到定义当今自动化行业的现场规则与启发式方法。

以下是我们要开发的其他安全机制的介绍：

![持续监控以确保 AI 控制系统不违反安全约束；如果 AI 控制系统确实违反了安全约束，则自动故障切换到中性状态；故障切换期间的平滑过渡，防止系统发生突变；AI 动作在执行前的双层验证；云端 AI 与物理基础设施之间的持续通信；不确定性估计，确保我们只执行高置信度的动作；以及作为退出 AI 控制模式时备用的规则与启发式方法。人工接管始终可用，并将优先于任何 AI 动作。](https://lh3.googleusercontent.com/H64NVqQM9X4R3x3vKz7k8gM-fK98hxJC6MP7zga9jA6dCN3qsS0reapSKxBwS8iIS8TSBYpS9gKjYmJX9ZG0l5isAB9Hpf3d_dWZBYeAydzq1zaRYg=w1440)

## 让节能效果随时间不断提升

我们最初的推荐系统需要运营人员审核并执行动作，而我们的新 AI 控制系统则直接执行动作。我们有意识地将系统的优化边界约束在更窄的运行范围内，以安全和可靠性为先，这意味着在节能幅度上存在风险与收益的权衡。

尽管这套系统投入使用才几个月，它已经实现了平均约 30% 的稳定节能，而且预计还会进一步改善。这是因为这些系统随着数据增多会随时间变得更好，正如下面的图表所示。随着技术成熟，我们的优化边界也将被扩展，以实现更大的节能幅度。

![双轴折线图，绘制 2017 年 9 月至 2018 年 7 月的性能与训练数据指标。左侧纵轴测量「相对于历史表现的改进幅度」，范围为 -35 到 -5；右侧纵轴测量「训练样本数量」，范围为 0 到 9,000 万。代表「滚动十二个月 AI 性能」的绿色线在此期间从约 -12 稳步下降至 -29，并带有浅绿色方差阴影带。相反，代表「训练数据」的蓝色线在同一时期呈稳定线性增长，从约 1,200 万升至超过 8,000 万个训练样本。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622690d2f1f3943175d607a4_DC206.gif)

这张图绘制了 AI 控制开始后相对于此前历史基线的 AI 性能变化。性能采用散热能效的通用行业指标 kW/ton（即每实现一吨制冷量所消耗的能源输入）来衡量。在九个月内，我们的 AI 控制系统性能从 12% 的改进（自主控制刚启动时）提升到约 30% 的改进。

我们的直接 AI 控制系统正在发现更多管理散热的新颖方法，连数据中心运营人员都感到惊讶。Dan Fuenffinger 是 Google 的数据中心运营人员之一，曾长期与该系统并肩工作。他说：「看到 AI 学会利用冬季环境条件、制备出比常温更冷的水，从而降低数据中心内制冷所需的能耗，实在令人惊叹。规则不会随时间变得更好，但 AI 会。」

让我们兴奋的是，我们的直接 AI 控制系统正在安全、可靠地运行，并持续带来能源节约。然而，数据中心只是一个开始。从长远来看，我们认为这项技术有潜力应用于其他工业场景，并在更大的规模上帮助应对气候变化。
