---
title: "2021 年度回顾：Google Quantum AI"
title_en: "2021 Year in Review: Google Quantum AI"
source: https://blog.google/innovation-and-ai/technology/research/2021-year-review-google-quantum-ai/
site: google-blog
date: 2021-12-30
crawled: 2026-09-13
translated: 2026-09-13
---

# 2021 年度回顾：Google Quantum AI

> 原文：[2021 Year in Review: Google Quantum AI](https://blog.google/innovation-and-ai/technology/research/2021-year-review-google-quantum-ai/) · Google

Google 的 Quantum AI 团队度过了成果丰硕的 2021 年。尽管全球性挑战仍在持续，我们在构建全容错量子计算机的道路上取得了显著进展，向着下一个硬件里程碑——构建容错量子比特（qubit）原型——稳步迈进。与此同时，我们继续致力于发掘量子计算机在各类应用中的潜力。为此，我们在顶级期刊上[发表了研究成果](https://quantumai.google/research)，与学术界和产业界的研究者开展合作，并扩充了[团队](https://quantumai.google/team)，引入了新的专业人才。

### 硬件进展

Quantum AI 团队决心在未来十年内造出容错量子计算机，同时把一路学到的知识用于交付有用的、甚至变革性的量子计算应用。这一[长期承诺](https://www.wsj.com/articles/google-aims-for-commercial-grade-quantum-computer-by-2029-11621359156)具体展开为我们量子硬件的三个关键问题：

1. 我们能否证明量子计算机在特定任务上能胜过当今的经典超级计算机？我们已于 2019 年[演示了超经典计算](https://www.nature.com/articles/s41586-019-1666-5)。
2. 我们能否造出容错量子比特的原型？要充分发挥量子计算机的潜力，我们需要实现量子纠错，以克服计算过程中存在的噪声。作为朝这个方向迈进的关键一步，我们的目标是通过把量子信息冗余地编码到多个物理量子比特上来实现量子纠错的基本要素，并证明这种冗余编码能带来优于单个物理量子比特的效果。这就是我们当前的目标。
3. 我们能否造出能长时间任意无错误运行的逻辑量子比特？逻辑量子比特把信息冗余地编码到多个物理量子比特上，能够降低噪声对整体量子计算的影响。集成数千个逻辑量子比特，将使我们能够充分发挥量子计算机在各类应用中的潜力。

一张[我们构建容错量子计算机历程的交互式地图](https://quantumai.google/learn/map)

![我们构建容错量子计算机历程的交互式地图。](https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/Scroll_Journey_02.gif)

### 迈向容错量子比特原型的进展

当今含噪声的量子计算机与未来全容错量子计算机之间的距离还很遥远。2021 年，我们在缩小这一差距方面取得了重大进展——朝着构建逻辑量子比特原型努力，使其错误率低于我们芯片上的物理量子比特。

这项工作需要改进量子计算技术栈的方方面面。我们制造了量子比特性能更好的芯片，改进了芯片封装方法以便更好地与控制电子设备连接，并开发了[同时校准数十个量子比特的大型芯片的技术](https://quantumai.google/cirq/tutorials/google/floquet_calibration_example)。

这些改进最终结出了两项关键成果。第一，我们现在能够[高保真度地重置量子比特](https://www.nature.com/articles/s41467-021-21982-y)，从而在量子计算中复用量子比特。第二，我们实现了电路中途测量，能够在量子线路中持续追踪计算状态。高保真重置与电路中途测量相结合，被用于我们近期利用重复码演示的[比特翻转错误与相位翻转错误的指数级抑制](https://www.nature.com/articles/s41586-021-03588-y)：当码距从 5 个量子比特增长到 21 个量子比特时，错误被抑制了 100 倍。

[随着重复码中量子比特数量增加，逻辑错误被抑制](https://www.nature.com/articles/s41586-021-03588-y)。当码规模从 5 个量子比特增加到 21 个时，逻辑错误降低 100 倍。图片致谢：Kevin Satzinger/Google Quantum AI

![记录重复码的图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Fig_Abe_EOY_blog_2021.width-1200.format-webp.webp)

重复码是一种纠错工具，让我们能够在资源（更多量子比特）与性能（更低错误率）之间进行权衡，这将成为指导我们未来硬件研发的核心。今年我们展示了[一维编码中错误率如何随所含量子比特数量的增加而下降](https://www.nature.com/articles/s41586-021-03588-y)。我们目前正在开展实验，将这些结果扩展到能更全面纠错的二维表面码。

### 量子计算的应用

除了构建量子硬件，我们的团队还在现实世界应用中寻找明确的量子优势空间。与学术界和产业界的合作者一道，我们正在探索量子计算机能够带来显著加速的领域，并对[容错量子计算机可能需要优于二次方的加速才能带来有意义的改进](https://journals.aps.org/prxquantum/abstract/10.1103/PRXQuantum.2.010103)抱有现实的预期。

一如既往，2021 年我们与学术和产业伙伴的合作弥足珍贵。与加州理工学院的一项著名合作表明，在某些条件下，[量子机器可以用指数级更少的实验来学习物理系统](https://scirate.com/arxiv/2112.00778)，远少于传统方法所需。这一新颖方法通过 40 个量子比特和 1300 次量子操作得到了实验验证，即便使用当今含噪声的量子处理器也展现出了实质性的量子优势。这为量子机器学习和量子传感领域的更多创新铺平了道路，并具有潜在的近期用例。

与哥伦比亚大学的研究者合作，我们将化学模拟中最强大的技术之一——量子蒙特卡洛方法——与量子计算[相结合](https://arxiv.org/abs/2106.16235)。这种方法作为基态多电子计算的量子路线，超越了以往的方法，而基态多电子计算对创造新材料和理解其化学性质至关重要。当我们在真实的量子计算机上运行该技术的一个组件时，我们能够把此前计算的规模扩大一倍，而不牺牲测量精度——即便在多达 16 个量子比特的设备存在噪声的情况下也是如此。这种方法对噪声的韧性表明，即使在当今的量子计算机上，它也具备可扩展的潜力。

我们继续研究如何利用量子计算机模拟量子物理现象——最近的一个体现是我们在量子处理器上实验[观测到时间晶体](https://www.nature.com/articles/s41586-021-04257-w)（[问问专家：时间晶体究竟是什么？](https://blog.google/inside-google/googlers/ask-techspert-what-exactly-time-crystal/)）。对思考时间晶体可能性近百年的理论学家来说，这是一个伟大的时刻。在其他工作中，我们还与 NASA 艾姆斯研究中心的合作者共同实验[测量了量子计算机上的时序关联](https://www.science.org/doi/10.1126/science.abg5029)，以探索量子混沌动力学的涌现；并与慕尼黑工业大学合作，通过浅层量子线路构造本征态，实验[测量了环面码哈密顿量基态的纠缠熵](https://www.science.org/doi/10.1126/science.abi8378)。

我们的合作者参与并启发了我们 2021 年一些最有影响力的研究。Quantum AI 仍将继续专注于机器学习、化学和多体量子物理，在 2022 年及以后与世界各地的科学家和研究者合作，发现并实现有意义的量子应用。

我们的全部论文列表可以在[这里](https://quantumai.google/research/publications)找到。

### 持续投资量子计算生态

今年，在 Google 年度开发者大会 Google I/O 上，我们[重申](https://blog.google/technology/ai/unveiling-our-new-quantum-ai-campus/)了在十年内造出实用量子计算机所需的路线图与投入承诺。在圣巴巴拉扩张的同时，我们也继续通过开源软件支持量子社区的研究者。我们的量子编程框架 [Cirq](https://github.com/quantumlib/cirq) 在社区贡献下不断改进。2021 年，我们还与生态伙伴合作发布了专门的工具。其中两个例子是：

- 与 QSimulate 合作，面向量子化学应用发布了[新的费米子量子模拟器](https://opensource.googleblog.com/2021/11/Efficient%20emulation%20of%20quantum%20circuits%20for%20chemistry.html)，利用量子化学问题中的对称性提供高效模拟。
- 对 [qsim 的重大升级](https://opensource.googleblog.com/2021/11/Upgrading%20qsim%20Google%20Quantum%20AIs%20Open%20Source%20Quantum%20Simulator%20.html)，使其能够通过 Google Cloud 在 GPU 等高性能处理器上模拟含噪声量子线路；以及 [qsim 与 NVIDIA cuQuantum SDK 的集成](https://opensource.googleblog.com/2021/11/qsim%20integrates%20with%20NVIDIA%20cuQuantum%20SDK%20to%20accelerate%20quantum%20circuit%20simulations%20on%20NVIDIA%20GPUs.html)，让 qsim 用户在开发量子算法和应用时充分利用 NVIDIA GPU。

我们还发布了一个名为 [stim](https://github.com/quantumlib/stim) 的开源工具，它[在模拟纠错线路时提供 10000 倍加速](https://quantum-journal.org/papers/q-2021-07-06-497/)。

我们的开源软件合集可以在[这里](https://quantumai.google/software)获取。

### 展望 2022

驻地量子科学家[小狗 Qubit](https://blog.google/technology/ai/qubit-dog-big-questions-quantum-computing/) 参加了由团队成员 Jimmy Chen 和 Ofer Naaman 主持的节日歌会。

![驻地量子科学家小狗 Qubit 参加节日歌会。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/IMG-1324.width-1200.format-webp.webp)

凭借团队合作、协作与一些创新的科学，我们对 2021 年取得的进展感到兴奋。随着我们专注于推进硬件里程碑、发现新的量子算法，以及在当今量子处理器上实现量子应用，我们对 2022 年充满期待。为了完成艰巨的使命，我们正在[扩充团队](https://quantumai.google/team/careers)、拓展既有的[合作者网络](https://quantumai.google/research/outreach)，并扩建我们的[圣巴巴拉园区](https://quantumai.google/hardware/our-lab)。与更广泛的量子社区一起，我们期待看到量子计算在 2022 年及以后取得的进展。
