---
title: "Google OCS Apollo：数据中心网络领域价值超 30 亿美元的规则改变者"
title_en: "Google OCS Apollo: The >$3 Billion Game-Changer in Datacenter Networking"
subtitle: "定制光交换机削弱 Broadcom 的网络统治地位"
date: 2023-03-17
source: https://newsletter.semianalysis.com/p/google-apollo-the-3-billion-game
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# Google OCS Apollo：数据中心网络领域价值超 30 亿美元的规则改变者

> 原文：[Google OCS Apollo: The >$3 Billion Game-Changer in Datacenter Networking](https://newsletter.semianalysis.com/p/google-apollo-the-3-billion-game) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**定制光交换机削弱 Broadcom 的网络统治地位**

网络是任何数据中心的关键组成部分，随着对网络需求密集的大语言模型兴起，更是如此。因此，它顺理成章地成为 Google 基础设施优化工作的明确目标。过去一年，在 OFC 和 SIGCOMM 等会议上，Google 披露了其定制网络技术栈 Jupiter——从自研交换机一直到可重构的定制软件。

与 Amazon、Microsoft 等竞争对手采用的行业标准方案相比，这套定制网络技术栈为 Google 节省了至少 30 亿美元。除了成本改善之外，Google 还获得了更高的网络性能和更低的延迟！这套定制网络技术栈 5 年多前就开始部署，如今已落地于 Google 的大部分数据中心。Google 的定制网络是其训练包括 PaLM 在内最先进大语言模型不可或缺的一环。

在深入探讨这套定制网络技术栈的工作原理之前，先快速谈谈它能做什么以及对行业的影响。首先，Google 声称其定制网络将吞吐量提升了 30%，功耗降低 40%，资本开支（Capex）减少 30%，流完成时间缩短 10%，网络停机时间减少 50 倍。

最重要的是，他们可以错峰进行数据中心网络升级。Google 的定制交换机还使他们得以不再采购 Broadcom 的网络交换机用于网络的 spine（骨干）层。

[Share](https://newsletter.semianalysis.com/p/google-apollo-the-3-billion-game?utm_source=substack&utm_medium=email&utm_content=share&action=share)

传统网络使用「Clos」拓扑（也称为 spine-leaf 架构），将数据中心内所有服务器及其机柜连接在一起。在 spine-leaf 架构中，有 spine、leaf 和计算节点。计算节点是装满 CPU、GPU、FPGA、存储和/或 ASIC 的服务器机柜。计算节点连接到 leaf 即机柜顶部（ToR）交换机，再经由各层汇聚交换机向上连接到 spine。

![](https://substack-post-media.s3.amazonaws.com/public/images/ea677045-e1ad-4b46-b426-7cdd3df6cfab_624x339.png)

传统上，这一网络的 spine 层使用所谓的电分组交换机（Electronic Packet Switch，EPS）。这就是普通的网络交换机，Broadcom、Cisco、Marvell 和 Nvidia 是其中的领先供应商。然而，这些 EPS 功耗巨大。此外，网络速度每 2 到 3 年翻一番。这种翻倍虽然改善了单位功耗，但也要求升级现有的 spine EPS。因此，每一代 Broadcom Tomahawk 交换机问世，总伴随着一波巨大的资本开支。

![](https://substack-post-media.s3.amazonaws.com/public/images/699f5cbf-e880-4971-9e02-f06569907ce1_624x365.png)

Google 启动了一个名为 Gemini 的项目，目标是去掉数据中心网络的这一 spine 层，从而降低该层交换带来的功耗和资本开支。而且这个项目的目标不止于 spine 层，它还将持续改进，并有望被网络更低的层级所采用。

![](https://substack-post-media.s3.amazonaws.com/public/images/0c540268-0f19-435d-97f1-51efa25f368c_624x277.png)

Apollo 项目专注于用光路交换机（Optical Circuit Switch，OCS）取代使用 EPS 的传统「Clos」架构。第一代光交换机名为 Palomar。这些 OCS 取代了旧「Clos」中的 spine。OCS 不再在 spine 层把信号反复从电转换为光、再转换回电，而是完全基于光的互连：利用镜面重定向入射光束，把从一个源端口编码了数据的光束送到目的端口。

打个比方，OCS 就像铁路道岔。可以有多条路径，但列车一次只能沿某一条特定轨道/路径行进。要改变列车将行驶的路径，你必须手动扳动道岔。

![](https://substack-post-media.s3.amazonaws.com/public/images/1e9caf1d-3e8a-4fcb-aaf2-7401222d2c54_1250x700.png)

以 Google 的网络为例：如果数据中心的某个通过端口 7 连接的区域想与另一个通过端口 4 连接的区域通信，而当前配置的是端口 11，那么光交换机就必须重新配置这些镜面，让端口 7 与端口 4 互通。注意，在传统 EPS 中，无需手动重新配置任何东西，因为所有端口通过电交换机始终处于连通状态。

![](https://substack-post-media.s3.amazonaws.com/public/images/533902f5-37cf-4238-9583-6b33db59cc17_624x307.png)

Google 在直连架构中使用这些光交换机，通过配线架直接连接各 leaf 交换机。这不是分组交换；无论从哪个角度讲，这都是一种光交叉连接（optical cross-connect）。

再用火车类比：这是一座拥有多条进出轨道的巨型火车站。任何进站的列车都可以被转到任何一条出站线路上，但需要在车站进行重新配线。

注意，在典型的网络架构中，每个数据包都带有一个包头。包头被解码后决定电交换机将该包发往何处。而在 Google 的 OCS 中不存在任何包解码。数据包在到达 OCS 之前就已走上预先确定的路径。如果你要更改通信的对端端口，就必须刻画数据包流的特征及其去向。你得在火车进站之前就知道它要去哪里。

总体而言，OCS 是一种「设定后无需理会」（set it and forget it）的方案，因为移动镜面以重新配置流经 OCS 的数据包路由需要数秒时间。与传统的 EPS 相比，这简直是一个世纪。你必须在列车抵达之前就设定好它要走的轨道。

![](https://substack-post-media.s3.amazonaws.com/public/images/6807edcf-c364-41c6-8f5f-9271651ff55b_624x184.png)

Google 的 OCS 并不能直接替换 EPS，网络必须从一开始就针对 OCS 明确设计，以把镜面重配置时间考虑在内。

## **借 Apollo 前进：数据速率无关性、低延迟与功耗节约**

灵活性不足、无法直接替换是 OCS 的重大缺点，但它也有诸多优势。Google 列出了三大优势：与数据速率和波长无关、低延迟，以及显著的功耗节约。

数据速率与波长无关之所以重要，主要有两个原因。第一，你可以与任何交换机和光器件技术互操作，也就是说，如果你需要把一台带 100G 收发器的交换机与一台带 800G 收发器的交换机连接起来，OCS 毫无问题——因为它只是重定向光线，而不是搬运数据包。

![](https://substack-post-media.s3.amazonaws.com/public/images/31f0f736-b45b-40fc-b295-0dba94fd1aa9_624x328.png)

OCS 一旦部署完成，你就可以把交换机和光器件升级到快得多的新一代，而不必换掉网络的「spine」。OCS 的使用寿命可以远长于传统的 EPS。

![](https://substack-post-media.s3.amazonaws.com/public/images/c61846d2-4cfa-4b5a-8095-657491454d71_528x339.png)

传统 EPS 中，光纤从交换机背面接入，经光电探测器和 TIA 转换为电信号，[经 DSP 重驱动和重定时](https://www.semianalysis.com/p/marvells-dsp-dilemma-networkings)，穿越 PCB，进入标准交换芯片，在那里数据包被解码、路径被决定。然后数据包被重新编码，沿着上述整个路径再走一遍。这每一步都会引入额外的延迟。

![](https://substack-post-media.s3.amazonaws.com/public/images/83c02eaf-c4d2-484c-b118-9f2604a4e7d1_1430x741.png)

OCS 之所以低延迟，是因为它不需要解码数据包；它要做的只是把入射光从源端口反射到目的端口。

![](https://substack-post-media.s3.amazonaws.com/public/images/72148e05-433c-4796-b329-ff1122001f21_550x364.png)

这就引出了第三点也是最大的一点优势：功耗。在传统 EPS 中，上述每一个步骤也都要消耗一点功率。

![](https://substack-post-media.s3.amazonaws.com/public/images/004b1162-e4a6-44d1-b04b-d288bfb16eeb_624x364.png)

关于性能与功耗收益的更多内容，见下方补充章节。

## **OCS 的障碍：高昂的前期成本、插入损耗等**

OCS 有四大缺点，而 Google 声称已全部解决。这四大缺点是：前期成本高、插入损耗、重配置时间，以及缺乏直接替换支持。

高昂的前期成本，Google 可以在很长的周期内摊销折旧。由于 OCS 能承载任何带宽，当 Google 的 leaf 交换机升级使用 1.6T 和 3.2T 收发器时，这些 OCS 无需更换，这就抵消了前期成本。Google 估算，由于 OCS 可以跨多个升级周期复用，其整体资本开支约为标准 EPS 的 70%。

![](https://substack-post-media.s3.amazonaws.com/public/images/17435510-2f8e-455e-80a1-6acad2bd9717_1032x552.jpeg)

如果我们假设 Google 预期 OCS 使用 3 个升级周期，那么单台 OCS 的前期成本约为 EPS 的 3.5 倍（EPS 的 ASP 随代际增长）。如果 Google 认为这些 OCS 能用 4 代，那么前期资本开支差距就更接近 6 倍！

插入损耗是 OCS 的下一个重大缺点。插入损耗是指光信号切换传输介质时损失的信号功率，例如从激光器到硅光芯片，或从光纤到光电探测器。它通常以分贝（dB）为单位计量，衡量信号强度的衰减。插入损耗越高，损失的信号功率就越大。例如，若一个器件造成 3 dB 的插入损耗，输出信号功率将只有输入的一半。

![](https://substack-post-media.s3.amazonaws.com/public/images/33508de6-4d28-4bd9-93f6-b88749b8e087_561x563.png)

插入损耗越大，信号就越弱，可能导致数据传输不可靠。插入损耗以分贝计量，损耗的分贝数越少越好。标准光纤的插入损耗约在 6dB 左右，而 Google 已将其降低至最坏情况下

重配置时间是另一个主要问题。为切换到不同路径而重新配置镜面需要数秒时间。Google 通过对其网络流量进行详尽的画像分析（profiling）解决了这个问题。

![](https://substack-post-media.s3.amazonaws.com/public/images/07beb180-4464-44f9-a64f-06b9f2b154a7_1430x765.png)

他们相信，按照流量模式的最坏情况来建设网络是过度设计；通过规划网络流量，镜面较长的重配置时间是可以接受的。

![](https://substack-post-media.s3.amazonaws.com/public/images/6acd7767-dc05-4eb2-a882-3ec2733b148c_1430x733.png)

至于缺乏直接替换支持，Google 的解决办法是重新设计网络以支持 OCS。Google 在 Jupiter 上投入了「十年的演进与生产经验」，而 Apollo 项目是 Google 降低这些大型网络系统 TCO 进程中的重要一步。这属于 Google 不会公开的秘方的一部分，不过在讲完硬件之后，有些细节我们可以分享。

## **Palomar MEMS 镜面封装：揭开 Google 光路交换机的心脏**

Apollo 项目最初在 OCS 上采用的是第三方供应商方案。Huawei 在其不同的网络使用场景中也使用过同一家供应商。

> 由于该方案在大规模部署下难以维持可靠性与质量，我们决定内部开发 OCS 系统。
>
> Google

这个内部开发的 OCS 名为 Palomar。

![](https://substack-post-media.s3.amazonaws.com/public/images/cc04d329-0328-4f41-a866-de210eaa3673_624x491.png)

Palomar OCS 的核心是 Palomar MEMS 镜面封装，包含 176 个可独立控制的微镜。不过，由于良率原因有 40 个被禁用，实际只使用 136 个镜面。

- MEMS 即微机电系统（Micro-Electro-Mechanical Systems）。它们是与电子元件集成、采用微加工技术制造的小型化机械与机电装置。

![](https://substack-post-media.s3.amazonaws.com/public/images/457b78f6-b1a4-4bc6-9387-2fb0e7ac5af4_484x255.png)

各个镜面的工作方式是：入射的 1310nm 信号光（O 波段）通过一个二向色分束器与第二束 850nm 光合并——该分束器让 850nm 光通过，而反射 1310nm 光。二向色分束器本质上就是一面镀了膜的斜置镜面，能让特定波长的光透过，同时反射其他波长的光。

在 Palomar OCS 中，要透射的光波长是 850nm，要反射的是 1310nm。由于无法 100% 反射或透射，分束会造成一些光损耗，但你能让 90% 以上的光到达想去的地方。

![](https://substack-post-media.s3.amazonaws.com/public/images/8eb92f67-add1-4c62-b31a-30f8004b85d7_624x331.png)

随后，合并后的光束经 MEMS 阵列反射到第二个二向色分束器，它把 1310nm 光反射回 MEMS 阵列，同时让 850nm 光进入一台用于监测 MEMS 阵列对准情况的相机。MEMS 阵列的对准非常重要，因为只要阵列出现一点偏移，就会造成数据传输中断。

![](https://substack-post-media.s3.amazonaws.com/public/images/82c971d6-cb3a-4f7a-b5af-2aa3b18e5858_624x351.png)

为了维持 MEMS 阵列对准，系统中有 2 束这样的 850nm 光，因此当 1310nm 光第二次从 MEMS 阵列反射时，仍与 850nm 光合并在一起。然后，当合并光束抵达最后一个二向色分束器时，1310nm 光被分离出来，送往输出端口。

![](https://substack-post-media.s3.amazonaws.com/public/images/102273b2-5076-4ce7-9282-7aec867a406e_532x294.png)

为了把 OCS 端口数和光纤数量减半、控制系统复杂度，Palomar 使用光环行器（optical circulator）实现双向链路。光环行器是一个 3 端口器件：端口 1 的输入被导向端口 2，端口 2 的输入被导向端口 3。这使得标准双工收发器可以转换为双向收发器。

![](https://substack-post-media.s3.amazonaws.com/public/images/ed4bb676-5a56-43ee-a6f5-ce9f6eb5c48a_475x145.png)

这带来了额外的回波损耗和串扰。回波损耗是光缆末端发生的信号损失。光从光纤进入另一种介质（如空气）时折射率的变化会造成信号劣化，而过高的光回波损耗可能导致激光器无法正确发射。

串扰是指两个信道之间的干扰，会造成信号劣化和噪声水平上升。因此，Google 放弃了仅支持 1530nm 至 1565nm 波长范围（C 波段）的掺铒光纤放大器（EDFA），转而采用光学镀膜加上光学重设计，从而能够使用 1310nm 波长范围（O 波段）。这次重设计还降低了系统的回波损耗和串扰。

![](https://substack-post-media.s3.amazonaws.com/public/images/45a8fead-f1b9-42d1-8f0a-1fb8e702c7f0_386x215.png)

Google 为 Apollo 采用了波分复用（WDM）光收发器。WDM 是一种利用不同波长的光将多路光信号通过一根光纤传输的技术。第一代 Apollo 以 40Gb/s 标准为基线。这是全行业采纳的标准（CWDM4 MSA），因此光器件是标准化的大宗商品。该方案中唯一独特的部分是基于 MEMS 的交换机。

![](https://substack-post-media.s3.amazonaws.com/public/images/a05add0c-d4a2-4b43-ac31-7362f3f232a9_624x385.png)

## **结论与未来**

Google 通过 Apollo 项目开发出一款 136x136 端口的无阻塞光路交换机，对 Google 数据中心正在使用或将来会使用的任何带宽、任何波长都向前和向后兼容。据 Google 介绍，这款交换机的功耗仅为 108 瓦。相比之下，一台标准的 136 端口 EPS 交换机的功耗大约在 3,000 瓦量级。

所以，尽管 OCS 存在缺点，Google 打造的这套方案对自身而言利远大于弊。过去 5 年里，「数万台 136x136 端口的 OCS（含 8 个备用端口）被制造并部署」。Google 打造了一套对他们而言运转得极其出色的系统。

未来，Google 正在研究端口数更多的 OCS 以获得更强的横向扩展能力，同时研究更快的切换速度，以便让 OCS 在网络更低层级得到更广泛的采用。这种更广泛的采用对超大规模网络交换机的领导者 Broadcom 将是极大的利空。此外，Google 表示他们还将继续提升可靠性、降低插入/回波损耗。

[Share](https://newsletter.semianalysis.com/p/google-apollo-the-3-billion-game?utm_source=substack&utm_medium=email&utm_content=share&action=share)

Google 还在研究基于压电（piezo）的切换技术，以取代当前基于 MEMS 的系统，因为压电系统在插入损耗和回波损耗上相较 MEMS 系统具有先天优势，切换速度也可能更快。Google 还分享了他们关于 MEMS、Robotic（机械臂）、Piezo（压电）、Guided Wave（导波）和 Wavelength（波长）切换的研究。研究维度包括相对成本、端口数、切换时间、插入损耗、驱动电压和闩锁特性。我们将在下方分享。

## **TPU 应用**

OCS 也用于 Google 全部的 TPUv4 和 TPUv5 系统。这是其卓越性能/TCO 的重要组成部分。

## **未来、支撑数据、软件与性能**

下方我们分享与 OCS 相关的大量文件、图片和论文，包括流量数据以及 Google 对 OCS 的采用情况。其中还有交换机的实物照片，以及 Google 如何对流量画像并部署 OCS。此外，还展示了除成本之外的网络性能收益——成本正是上文的主要焦点。

[团体订阅享 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
