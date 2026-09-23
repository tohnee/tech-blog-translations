---
title: "开源 mvfst-rl：用强化学习管理网络拥塞的研究平台"
title_en: "Open-sourcing mvfst-rl, a research platform for managing network congestion with reinforcement learning"
date: 2019-03-15
source: https://ai.facebook.com/blog/open-sourcing-mvfst-rl-a-research-platform-for-managing-network-congestion-with-reinforcement-learning
crawled: 2026-09-22
translated: 2026-09-22
---

# 开源 mvfst-rl：用强化学习管理网络拥塞的研究平台

> 原文：[Open-sourcing mvfst-rl, a research platform for managing network congestion with reinforcement learning](https://ai.facebook.com/blog/open-sourcing-mvfst-rl-a-research-platform-for-managing-network-congestion-with-reinforcement-learning) · Meta AI（Wayback 存档）

**它是什么：**mvfst-rl 是一个用于训练和部署强化学习（RL）策略的平台，旨在实现更有效的网络拥塞控制，并能主动适应不断变化的流量模式。mvfst-rl 使用 PyTorch 进行 RL 训练，构建在我们的 QUIC 传输协议开源实现 mvfst 之上（QUIC 来自互联网工程任务组 IETF）。mvfst-rl 用异步 RL 智能体实现拥塞控制，使训练环境对真实世界部署更加逼真。它与 mvfst 的紧密集成，使训练好的 RL 策略能够从研究无缝、高效地迁移到部署。

**它做了什么：**现有的拥塞控制研究 RL 环境与真实世界用例并不兼容，因为它们使用的 RL 接口中，智能体会阻塞网络发送方。这在很大程度上是在为游戏研究使用 RL 而设计的框架上构建的产物——在游戏中，资源约束不会像大规模生产环境那样构成挑战，而在生产环境中，哪怕几毫秒的延迟也会损害性能。mvfst-rl 向前迈出一大步，采用能够处理延迟动作的异步 RL 智能体来做拥塞控制。系统累积网络统计信息，并异步地把状态更新发送给运行在单独线程中的 RL 智能体。智能体完成策略查询后，更新再被应用。这样，网络环境就能基于 RL 策略采取拥塞控制动作，而不引入延迟。

**为什么重要：**业界估计显示，2018 年每月通过互联网发送的数据超过 150 EB，预计到 2021 年将几乎翻倍。有效的网络拥塞控制策略是让互联网在这种 massive 规模下保持运转的关键。几十年来，这些系统一直由手工设计的启发式规则主导，它们能对动态流量模式做出反应，却无法学习预判这些模式的新方法。基于 RL 的系统有望主动采取措施减少网络拥塞并适应多变的网络场景，但据我们所知，尚无此类系统被迁移到真实生产系统中。我们用 mvfst-rl 做的初步结果显示出应用于拥塞控制的前景，我们希望未来在生产环境中测试训练好的网络控制智能体。此外，在大规模实时系统中部署强化学习，会带来研究社区流行的高度受控、可预测 RL 环境中见不到的挑战。我们希望 mvfst-rl 提供一个新平台和一组新颖的挑战，以推进 RL 研究，并发展在真实用例中使用 RL 的新方式。

更多细节见我们的论文。

**GitHub 获取地址：**https://github.com/facebookresearch/mvfst-rl

**作者**

- Viswanath Sivakumar，软件工程师
