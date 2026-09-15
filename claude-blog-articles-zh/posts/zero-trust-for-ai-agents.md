---
title: "面向 AI 智能体的零信任"
title_en: "Zero Trust for AI agents"
source: https://claude.com/blog/zero-trust-for-ai-agents/
crawled: 2026-09-14
translated: 2026-09-14
---

# 面向 AI 智能体的零信任

> 原文：[Zero Trust for AI agents](https://claude.com/blog/zero-trust-for-ai-agents/) · Claude 博客

前沿 AI 模型正在把从漏洞出现到被利用的时间线从数月压缩到数小时。采用这些工具的防御者能更快地发现并修复缺陷；而采用这些工具的攻击者，或者只是按兵不动、等防御者发布补丁后再逆向工程出攻击利用代码的攻击者，同样在提速。这并非未来的隐忧：模型已经能够找出传统工具和人工审查者多年未能发现的严重漏洞。

对于任何部署智能体的组织，这种加速都构成双重影响。你的智能体赖以运行的基础设施，与技术版图中的其他部分一样暴露在 AI 加速的攻势之下；而智能体本身又引入了自主性——解读目标、选择工具、执行多步骤操作。传统的访问控制无法阻止智能体滥用其合法权限，监控也需要把那些靠持续驻留而非漏洞利用来达成目的的攻击纳入考量。

[零信任（zero trust）](https://en.wikipedia.org/wiki/Zero_trust_architecture)——不信任任何事物、验证一切，并假定入侵（assume breach）已经发生——为安全负责人提供了应对这一局面的成熟基础。但这些原则在智能体系统中需要新的形态：以密码学方式扎根的身份、按任务划定范围的权限、防范投毒的记忆，以及能以自主攻击者的速度运转的防御行动。

为了帮助安全与风险负责人为这一转变做好准备，我们整理了一套在企业中部署自主 AI 智能体的实用框架。

在这份指南中，我们分享了：

- 智能体系统独有的安全考量，包括工具访问、自主决策、上下文持久化和多智能体协同
- 智能体当前面临的威胁图景，包括提示注入（prompt injection）、工具投毒（tool poisoning）、身份与权限滥用、记忆投毒（memory poisoning）以及供应链攻击
- 一个与组织成熟度和风险容忍度相匹配的三级零信任框架（基础级 Foundation、进阶级 Advanced、优化级 Optimized）
- 一套八阶段实施工作流，覆盖身份、访问范围划定、沙箱机制、输入与输出控制以及记忆保障
- 如何以足够快的速度运行智能体安全运营（Agentic SOAR），从而与 AI 加速的攻击者抗衡
- 面向医疗、金融、政府等受监管行业的合规对齐

在这场转变中占据最有利位置的组织，将是那些基础足够扎实、以致 AI 辅助扫描从一开始就找不到多少缺陷的组织，以及那些从第一天起就按「已被入侵」来架构其智能体部署的组织。

欢迎前往[这里](https://cdn.prod.website-files.com/6889473510b50328dbb70ae6/6a1611a04085d7cd3dadc924_Claude-eBook-Zero-Trust-for-AI-Agents-05182026.pdf)阅读。

立即开始使用 [Claude Security](https://www.anthropic.com/product/security)。

FAQ（常见问题）
