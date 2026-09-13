---
title: "开发可靠的医疗 AI 工具"
title_en: "Developing reliable AI tools for healthcare"
source: https://deepmind.google/blog/codoc-developing-reliable-ai-tools-for-healthcare/
site: deepmind
date: 2023-07-17
crawled: 2026-09-13
translated: 2026-09-13
---

# 开发可靠的医疗 AI 工具

> 原文：[Developing reliable AI tools for healthcare](https://deepmind.google/blog/codoc-developing-reliable-ai-tools-for-healthcare/) · Google DeepMind

新研究提出一个系统，用于在假想的医疗场景中判断预测式 AI 的相对准确性，以及何时该系统应交由人类临床医生处理

人工智能（AI）在提升各行各业人们工作方式方面具有巨大潜力。但要以安全、负责任的方式将 AI 工具整合到工作场所，我们需要开发更健全的方法来理解它们在什么时候最能发挥作用。

那么，什么时候 AI 更准确，什么时候是人类更准确？这个问题在医疗领域尤为重要——预测式 AI 正越来越多地被用于协助临床医生完成高风险任务。

今天，我们在《自然·医学》（Nature Medicine）上发表了与 Google Research 合作的论文，提出了 CoDoC（Complementarity-driven Deferral-to-Clinical Workflow，互补性驱动的临床工作流转交机制）——一个 AI 系统，它学习何时依赖预测式 AI 工具、何时转交给临床医生，以实现对医学影像最准确的判读。

CoDoC 探索了我们如何在假想的医疗场景中利用人机协作来取得最佳结果。在一个示例场景中，对于一个大型去标识化的英国乳腺钼靶数据集，与常用的临床工作流相比，CoDoC 将假阳性数量减少了 25%——同时没有遗漏任何真阳性。

这项工作是与多个医疗组织合作的成果，包括联合国项目事务厅（UNOPS）主持的 Stop TB Partnership（终止结核病伙伴关系）。为帮助研究者在我们工作的基础上改进面向真实世界的 AI 模型的透明度与安全性，我们还在 [GitHub 上开源了 CoDoC 的代码](http://github.com/deepmind/codoc)。

## CoDoC：人机协作的附加工具

构建更可靠的 AI 模型通常需要重新设计预测式 AI 模型复杂的内部机制。然而，对许多医疗服务提供者来说，重新设计预测式 AI 根本不可行。CoDoC 有望帮助用户改进预测式 AI 工具，而无需修改底层 AI 工具本身。

在开发 CoDoC 时，我们有三条标准：

- 非机器学习专家（如医疗服务提供者）应能部署该系统，并在单台计算机上运行。
- 训练只需要相对少量的数据——通常仅需几百个样本。
- 系统可以与任何专有 AI 模型兼容，且无需访问模型的内部机制或其训练数据。

## 判断预测式 AI 与临床医生谁更准确

通过 CoDoC，我们提出了一个简单可用的 AI 系统，通过帮助预测式 AI 系统「知道自己不知道什么」来提升可靠性。我们考察了这样的场景：临床医生可以使用一个帮助判读影像的 AI 工具，例如检查一张胸部 X 光片以判断是否需要进行结核病检测。

对于任何理论上的临床场景，CoDoC 的系统对训练集中的每个病例只需要三个输入。

1. 预测式 AI 输出一个介于 0（确定没有疾病）到 1（确定存在疾病）之间的置信度分数。
2. 临床医生对医学影像的判读。
3. 是否存在疾病的真实情况（ground truth），例如通过活检或其他临床随访确认。

注意：CoDoC 不需要访问任何医学影像。

![流程图展示 CoDoC 的训练过程：医疗病例同时输入预测式 AI 模型和临床工作流，由此得到的预测式 AI 置信度分数与回顾性临床医生意见，连同经活检证实的真实标签一起，用于训练一个转交 AI（Deferral AI）模型。](https://lh3.googleusercontent.com/lSe7Fkpe3zl0CEtsOQsH_v1J7CGMJ8rFW5u7JXb3o7ZO0cmLAloHHvhHh3j8F4Hkorf5B7Rot3aXekftv4la_SjLuoCLmDoLdLlCxx1OhQmFJcKWMB0=w1440)

示意图展示 CoDoC 如何训练。此处，现有的预测式 AI 模型保持不变。

CoDoC 学习建立预测式 AI 模型相对于临床医生判读的准确性对比，以及这一关系如何随预测式 AI 的置信度分数而波动。

训练完成后，CoDoC 可以被嵌入一个假想的、同时涉及 AI 和临床医生的未来临床工作流。当预测式 AI 模型评估一张新的患者影像时，其对应的置信度分数被输入系统。随后，CoDoC 评估接受 AI 的决定还是转交给临床医生，最终能带来最准确的判读。

![流程图展示 CoDoC 系统的工作流：一张新的患者 X 光影像首先由预测式 AI 模型分析并生成置信度分数，这些分数由转交 AI 模型处理，由其决定是直接采用预测式 AI 的输出，还是转交给临床医生做出最终临床诊断。](https://lh3.googleusercontent.com/L0HVLqFdNyL6LjGa-qzF296aqApB5Z50Z-CcblyldbJzrNdiuqDc5n2h0Imihmyiq9R0vcKIvIgSCWeblikysTcInefQIA6UKjmcD_LK3nN9PhycYA=w1440)

示意图展示 CoDoC 如何被嵌入一个假想的临床工作流。

![一张图示，展示 CoDoC 基于预测式 AI 置信度分数的决策策略：当预测式 AI 的置信度非常低（绿色区域）或非常高（红色区域）时，其诊断被采纳；而当分数处于中间区间（灰色区域）时，系统会将该病例转交给临床医生。](https://lh3.googleusercontent.com/nW1tAaGKcQ-JtnE36vQhY6TUnb-3drdY1-GBxfwwP8t_sHpWOE4eRDTIqQr86qAoHGCz_SeD_xFl1VvaUg8uF6R83bAnKZMiKvVwu1gEwwgefVZ1UQ=w1440)

在训练中，我们建立一个「优势函数」来优化 CoDoC 的决策。训练完成后，当模型比临床医生更准确时（绿色和红色区域），它倾向于仅采用 AI 的判读；当人类判断优于 AI 时（灰色区域），它转交给临床医生。

## 更高的准确性与效率

我们用多个真实世界数据集（仅包含历史和去标识化数据）对 CoDoC 进行了全面测试，结果表明，将人类专长与预测式 AI 的优势相结合，比单独使用任何一方都能带来更高的准确性。

除了在乳腺钼靶数据集上实现 25% 的假阳性减少之外，在允许 AI 在特定场合自主行动的假想仿真中，CoDoC 还能将需要临床医生判读的病例数量减少三分之二。我们还展示了 CoDoC 在假想中如何改进胸部 X 光片的分诊，以便后续进行结核病检测。

## 负责任地开发医疗 AI

虽然这项工作是理论性的，但它展示了我们 AI 系统的适应潜力：CoDoC 能够在不同人口群体、临床场景、所使用的医学影像设备以及疾病类型各异的情况下，提升医学影像判读的性能。

CoDoC 是一个有前景的例子，展示了我们如何将 AI 的优势与人类的力量和专长相结合。我们正在与外部合作伙伴一起严谨地评估我们的研究和系统的潜在收益。要把 CoDoC 这样的技术安全地引入真实的医疗场景，医疗服务提供者和厂商还必须理解临床医生与 AI 互动方式的差异，并针对特定的医疗 AI 工具和场景对系统进行验证。

**进一步了解 CoDoC：**

[在 GitHub 下载 CoDoC 的代码](https://github.com/google-deepmind/codoc)[在《自然·医学》上阅读我们的论文](https://www.nature.com/articles/s41591-023-02437-x%20)

**致谢**

我们感谢这一国际项目的众多贡献者，包括由 UNOPS 主持的 Stop TB Partnership；皇家萨里基金会信托（Royal Surrey Foundation Trust）的 OPTIMAM 项目团队和工作人员——他们建设了英国乳腺钼靶 OPTIMAM 影像数据库，其创建由英国癌症研究院（Cancer Research UK）资助；以及我们在西北大学医学院（Northwestern Medicine）和纽约大学格罗斯曼医学院（NYU Grossman School of Medicine）的合作者。

**关于数据的说明**

这项研究纯属理论性质，基于去标识化的历史临床数据。Google DeepMind 和 Google Research 没有访问我们合作伙伴的去标识化医学影像；仅使用了预训练 AI 模型的预测结果，以及每张被检医学影像对应的临床医生意见。研究未在真实世界临床场景中进行。
