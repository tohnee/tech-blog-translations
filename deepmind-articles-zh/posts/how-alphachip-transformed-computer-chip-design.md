---
title: "AlphaChip 如何变革计算机芯片设计"
title_en: "How AlphaChip transformed computer chip design"
source: https://deepmind.google/blog/how-alphachip-transformed-computer-chip-design/
site: deepmind
date: 2024-09-26
crawled: 2026-09-13
translated: 2026-09-13
---

# AlphaChip 如何变革计算机芯片设计

> 原文：[How AlphaChip transformed computer chip design](https://deepmind.google/blog/how-alphachip-transformed-computer-chip-design/) · Google DeepMind

我们的 AI 方法加速并优化了芯片设计，其超越人类的芯片布局已被全球硬件所采用

2020 年，我们发布了一篇[预印本](https://arxiv.org/pdf/2004.10746)，介绍了我们用于设计芯片布局的新型强化学习方法，随后我们[将其发表于《自然》（Nature）](https://www.nature.com/articles/s41586-021-03544-w)并[开放了源代码](https://github.com/google-research/circuit_training)。

今天，我们[发表一篇 Nature 增补文件](https://www.nature.com/articles/s41586-024-08032-5)，更详细地描述我们的方法及其对芯片设计领域的影响。我们还在发布一个[预训练检查点](https://github.com/google-research/circuit_training/?tab=readme-ov-file#PreTrainedModelCheckpoint)，共享模型权重，并公布它的名字：AlphaChip。

计算机芯片推动了人工智能（AI）的卓越进步，而 AlphaChip 则投桃报李，用 AI 加速并优化芯片设计。该方法已被用于为 Google 定制 AI 加速器[张量处理单元](https://cloud.google.com/tpu?hl=en)（TPU）最近三代产品设计超越人类的芯片布局。

AlphaChip 是最早用于解决现实世界工程问题的强化学习方法之一。它能在数小时内生成超越人类或与之相当的芯片布局，而人工设计则需要数周或数月的努力；它的布局被应用于世界各地的芯片，从数据中心到手机。

> AlphaChip 开创性的 AI 方法革新了芯片设计的一个关键阶段。

SR Tsai

联发科（MediaTek）高级副总裁

## AlphaChip 的工作原理

设计芯片布局并非简单的任务。计算机芯片由许多互连的模块组成，模块中有多层电路元件，全部由极细的导线连接。此外还有大量复杂且相互交织的设计约束，必须同时满足。由于其复杂性极高，芯片设计师在六十多年来一直难以将芯片布局规划（floorplanning）过程自动化。

类似于学会了围棋、国际象棋和将棋的 [AlphaGo](https://deepmind.google/technologies/alphago/) 与 [AlphaZero](https://deepmind.google/technologies/alphazero-and-muzero/)，我们把 AlphaChip 打造成将芯片布局规划视为一种游戏的方法。

从一张空白网格开始，AlphaChip 逐一放置电路元件，直到完成所有元件的放置。然后，它根据最终布局的质量获得奖励。一种新颖的"基于边"的图神经网络让 AlphaChip 能够学习互连芯片元件之间的关系并在不同芯片间泛化，使 AlphaChip 随着每一次布局设计不断进步。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

左：动画展示 AlphaChip 在没有任何先验经验的情况下放置开源的 Ariane RISC-V CPU。右：动画展示 AlphaChip 在 20 个 TPU 相关设计上练习后放置同一模块。

## 用 AI 设计 Google 的 AI 加速器芯片

自 2020 年发表以来，AlphaChip 生成的超越人类的芯片布局已被用于 Google TPU 的每一代产品。这些芯片让基于 Google [Transformer](https://research.google/blog/transformer-a-novel-neural-network-architecture-for-language-understanding/) 架构的 AI 模型得以大规模扩展。

TPU 位于我们强大的生成式 AI 系统的核心，从 [Gemini](https://gemini.google.com/) 这样的大语言模型，到图像和视频生成器 [Imagen](https://deepmind.google/technologies/imagen-3/) 与 [Veo](https://deepmind.google/technologies/veo/)。这些 AI 加速器同样位于 Google AI 服务的核心，并可通过 Google Cloud [供外部用户使用](https://cloud.google.com/tpu)。

![Google 数据中心内一排 Cloud TPU v5p AI 加速器超级计算机的照片](https://lh3.googleusercontent.com/tsPiQ_Sw2dnUDFsKuKa1SkyezcLczPkIEa44V3785ov_3YqDKm7HD1AL5MSjk9-SZ87kbAG-mKC-BMq4HoAVAOLxvJ62Zhguuu_RMn_0VfxOI6Pu4A=w1440)

Google 数据中心内一排 Cloud TPU v5p AI 加速器超级计算机。

为了设计 TPU 布局，AlphaChip 先在来自前代产品的各种芯片模块上进行练习，例如[片上与片间网络模块](https://en.wikipedia.org/wiki/Network_on_a_chip)、[内存控制器](https://en.wikipedia.org/wiki/Memory_controller)和[数据传输缓冲器](https://en.wikipedia.org/wiki/Data_buffer)。这一过程称为预训练。然后，我们在当前的 TPU 模块上运行 AlphaChip 以生成高质量布局。与以往方法不同，AlphaChip 在解决更多芯片放置任务实例的过程中变得更强、更快，就像人类专家一样。

随着 TPU 每一代的更新——包括我们最新的 [Trillium](https://cloud.google.com/blog/products/compute/introducing-trillium-6th-gen-tpus)（第 6 代）——AlphaChip 设计出了更好的芯片布局，并承担了更大比例的整体布局规划，加速了设计周期，产出了性能更高的芯片。

![柱状图显示 AlphaChip 设计的芯片模块数量在 Google 三代张量处理单元（TPU）中的变化，包括 v5e、v5p 和 Trillium。](https://lh3.googleusercontent.com/uvA--nI76IjsOKgvkv3eVi3MICc9-zRB8eLVhizsrJOneYBvaT-Ub65q-FwyUw_HXWyc-7z0J7_W3WlNJogdIXoAeeA8zkUKYiok8YM1ey44e3bFt9o=w1440)

柱状图显示 AlphaChip 设计的芯片模块数量在 Google 三代张量处理单元（TPU）中的变化，包括 v5e、v5p 和 Trillium。

![柱状图显示在 Google 三代张量处理单元（TPU）上，与 TPU 物理设计团队生成的布局相比，AlphaChip 的平均线长缩减。](https://lh3.googleusercontent.com/HCymxHdoYn-g1paupQodU33pZqnEpJrqLn86Ji4KrX6PtyhoIVSOuSKGjLRVKUg3gj1aPtrEx8ppSa7EOA5wQY1DjWzQMDW4GJvu82qhlS6zPWGFHQ=w1440)

柱状图显示在 Google 三代张量处理单元（TPU）上，与 TPU 物理设计团队生成的布局相比，AlphaChip 的平均线长缩减。

## AlphaChip 的更广泛影响

AlphaChip 的影响体现在它在 Alphabet 内部、研究界和芯片设计行业的应用中。除了设计 TPU 这类专用 AI 加速器之外，AlphaChip 还为 Alphabet 内部的其他芯片生成了布局，例如 [Google Axion 处理器](https://cloud.google.com/blog/products/compute/introducing-googles-new-arm-based-cpu)——我们首款基于 Arm 的通用数据中心 CPU。

外部机构也在采用并拓展 AlphaChip。例如，全球顶尖芯片设计公司之一联发科（MediaTek）扩展了 AlphaChip，以加速其最先进芯片的开发，同时改善功耗、性能与芯片面积。

AlphaChip 引发了 AI 芯片设计工作的爆发，并被拓展到芯片设计的其他关键阶段，例如[逻辑综合](https://openreview.net/forum?id=0t1O8ziRZp)和[宏单元选择](https://ieeexplore.ieee.org/document/9980637)。

> AlphaChip 激发了芯片设计强化学习领域一条全新的研究路线，横跨从逻辑综合到布局规划、时序优化等整个设计流程。

Siddharth Garg 教授

纽约大学坦登工程学院

## 创造未来的芯片

我们相信，AlphaChip 有潜力优化芯片设计周期的每一个阶段——从计算机架构到制造——并变革智能手机、医疗设备、农业传感器等日常设备中定制硬件的芯片设计。

AlphaChip 的未来版本目前正在开发中，我们期待与社区合作，继续革新这一领域，迎来芯片更快、更便宜、更节能的未来。

[阅读我们 2024 年的增补文件](https://www.nature.com/articles/s41586-024-08032-5)[阅读我们 2021 年的论文](https://www.nature.com/articles/s41586-021-03544-w)[阅读我们 2020 年的预印本](https://arxiv.org/pdf/2004.10746)[查看我们的预训练教程](https://github.com/google-research/circuit_training/blob/main/docs/PRETRAINING.md)

第 1 页，共 5 页

> AlphaChip 开创性的 AI 方法革新了芯片设计的一个关键阶段。在联发科，我们一直在拓展这项技术并结合行业最佳实践，率先推进芯片设计的布局规划与宏单元摆放。这一范式转变不仅提升了设计效率，也为有效性设立了新的基准，推动行业迈向未来的突破。

SR Tsai，高级副总裁

联发科（MediaTek）

> AlphaChip 展示了强化学习在应对最复杂的硬件优化挑战之一——芯片布局规划——时非凡的变革潜力。这项研究不仅将强化学习的应用从其在博弈场景中的既定成功拓展到具有实际影响力的高价值工业挑战，还为在 AI 与全栈芯片设计交汇处对未来进展进行基准测试建立了一个稳健的基线环境。这项工作的长期影响深远，展示了困难的工程任务如何能被重构为半导体技术中 AI 驱动优化的新途径。

Vijay Janapa Reddi 教授

哈佛大学

> AlphaChip 激发了芯片设计强化学习领域一条全新的研究路线，横跨从逻辑综合到布局规划、时序优化等整个设计流程。虽然细节各有不同，但论文中的关键思想——包括帮助引导在线搜索的预训练智能体，以及基于图网络的电路表示——持续影响着这一领域，包括我自己关于逻辑综合强化学习的工作。这项工作即便尚未成为，也注定将成为机器学习用于硬件设计的里程碑论文之一。

Siddharth Garg 教授

纽约大学坦登工程学院

> 强化学习已深刻影响了电子设计自动化（EDA），尤其是通过解决 AI 驱动方法中数据稀缺的挑战。尽管存在延迟奖励和泛化能力有限等障碍，研究已经证明强化学习在布局规划等复杂电子设计自动化任务中的能力。这篇开创性论文已成为强化学习-电子设计自动化研究的基石，被频繁引用，包括在我自己获得 2023 年 ACM 设计自动化会议最佳论文奖的工作中。

Sung-Kyu Lim 教授

佐治亚理工学院

> 当今时代有两股举足轻重的力量：半导体芯片设计与 AI。这项研究开辟了一条新路径，展示了一些想法，让电子设计自动化（EDA）社区看到了 AI 和强化学习在集成电路设计中的力量。它在 AI 芯片设计领域产生了开创性影响，对于我们围绕建立 IEEE LLM-Aided Design（LAD）这样一个重大研究会议、以讨论此类具有影响力想法的思考与努力起到了关键作用。

Ruchir Puri

IBM Research 首席科学家；IBM Fellow

**致谢**

我们非常感谢了不起的共同作者：Mustafa Yazgan、Joe Wenjie Jiang、Ebrahim Songhori、Shen Wang、Young-Joon Lee、Eric Johnson、Omkar Pathak、Azade Nazi、Jiwoo Pak、Andy Tong、Kavya Srinivasa、William Hang、Emre Tuncer、Quoc V. Le、James Laudon、Richard Ho、Roger Carpenter 和 Jeff Dean（杰夫·迪恩）。

我们特别感谢 Joe Wenjie Jiang、Ebrahim Songhori、Young-Joon Lee、Roger Carpenter 和 Sergio Guadarrama 为落地这一生产影响所做的持续努力，感谢 Quoc V. Le 的研究建议与指导，感谢我们的资深作者 Jeff Dean 的支持与深入的技术讨论。

我们还要感谢 Ed Chi、Zoubin Ghahramani、Koray Kavukcuoglu、Dave Patterson 和 Chris Manning 的建议与支持。
