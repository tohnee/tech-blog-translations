---
title: "vLLM 硬件插件正式推出：来自 Ascend NPU 的最佳实践"
title_en: "Introducing vLLM Hardware Plugin, Best Practice from Ascend NPU"
source: https://vllm.ai/blog/2025-05-12-hardware-plugin
crawled: 2026-09-12
translated: 2026-09-13
---

# vLLM 硬件插件正式推出：来自 Ascend NPU 的最佳实践

> 原文：[Introducing vLLM Hardware Plugin, Best Practice from Ascend NPU](https://vllm.ai/blog/2025-05-12-hardware-plugin) · vLLM 博客

作者：vLLM 上的 Ascend 团队

[#硬件](https://vllm.ai/blog/tags/hardware)

自 2024 年 12 月以来，通过 vLLM 社区与 vLLM 上的 Ascend 团队的共同努力，我们完成了[硬件可插拔 RFC（Hardware Pluggable RFC）](https://github.com/vllm-project/vllm/issues/11162)。该提案允许以解耦的方式将硬件集成到 vLLM 中，从而实现对不同硬件平台的快速、模块化支持。

---

## 为什么需要 vLLM 硬件插件？

目前，vLLM 已经支持多个后端。然而，随着 vLLM 后端数量的持续增长，一些挑战逐渐浮现：

- **代码复杂度上升**：每个硬件后端都有自己的 `Executor`、`Worker`、`Runner` 和 `Attention` 组件。这增加了 vLLM 代码库的复杂度，非通用的后端特定代码散落在整个项目中。
- **维护成本高**：维护后端的成本很高，不仅对后端开发者如此，对 vLLM 社区也是如此。社区贡献者资源稀缺，当后端维护者不在场时，高效添加新特性变得困难。
- **缺乏可扩展性**：虽然 vLLM 通过 `Executor`、`Worker`、`Runner` 和 `Attention` 实现后端，遵循了结构良好的分层设计，但支持新硬件往往需要侵入式修改或打补丁，而非动态注册。这使得添加新后端十分繁琐。

认识到需要一种灵活、模块化的硬件后端集成方式，我们提出了硬件插件作为可行的解决方案：

- **解耦的代码库**：硬件后端插件代码保持独立，使 vLLM 核心代码更加整洁。
- **降低维护负担**：vLLM 开发者可以专注于通用特性，而不会被后端特定实现带来的差异所困扰。
- **更快的集成与更强的独立性**：新后端可以用更少的工作快速集成，并能独立演进。

---

## 什么是 vLLM 硬件插件？

在介绍 vLLM 硬件插件之前，我们先来看两个前置 RFC：

- [[RFC] vLLM 插件系统](https://github.com/vllm-project/vllm/issues/7131)：该 RFC 引入了基于插件的方法来支持各种定制需求，允许用户定义自定义模型、执行器、调度器等。
- [[RFC] 让 vLLM 设备无关以支持多样硬件](https://github.com/vllm-project/vllm/issues/9268)及（[vllm-project/vllm#6080](https://github.com/vllm-project/vllm/pull/6080)）：该 RFC 引入了 **platform** 子模块，将硬件相关的实现集中起来，以减少主代码库中的条件逻辑，并为模块化奠定基础。

基于这些 RFC，我们提出了 [[RFC] 硬件可插拔](https://github.com/vllm-project/vllm/issues/11162)，将 `Platform` 模块作为插件集成进 vLLM。此外，我们重构了 `Executor`、`Worker`、`ModelRunner`、`AttentionBackend` 和 `Communicator`，以更灵活地支持硬件插件。

目前，vLLM 社区已成功实现了该 RFC 中引入的 Platform 模块。其功能已通过 [vllm-project/vllm-ascend](https://github.com/vllm-project/vllm-ascend) 和 [vllm-project/vllm-spyre](https://github.com/vllm-project/vllm-spyre) 项目得到验证。借助这一插件机制，我们成功地将 vLLM 与 Ascend NPU 和 IBM Spyre 后端集成。

---

## 如何通过 vLLM 硬件插件机制集成新后端

本节将从开发者和用户两个视角，深入介绍如何通过硬件插件集成新后端。

### 开发者视角

要使用硬件插件将新后端集成到 vLLM，请遵循以下步骤：

#### 步骤 1：创建新项目并初始化 Platform

首先为新后端创建一个 Python 项目，并添加一个 `platform.py` 文件。然后，从 `vllm.platforms` 导入 `Platform` 类，并实现所需的属性和方法。

你可以参考 vLLM Ascend 项目中的 [`platform.py`](https://github.com/vllm-project/vllm-ascend/blob/72a43a61d8d2193dddbfcc60578fd642008225a5/vllm_ascend/platform.py#L52) 作为示例。

#### 步骤 2：实现自定义的 Worker、Model Runner、Attention 后端和 Communicator 模块

根据新后端的需求，实现以下模块：

```
from vllm.worker.worker_base import WorkerBase
from vllm.worker.model_runner_base import ModelRunnerBase
from vllm.attention.backends.abstract import AttentionBackend
from vllm.distributed.device_communicators.base_communicator import CommunicatorBase
```

这些类在 vLLM 中都有对应的基类。同样，你可以参考 [vLLM Ascend 的实现](https://github.com/vllm-project/vllm-ascend/tree/main/vllm_ascend)作为示例。

#### 步骤 3：注册插件

使用 Python 的 entrypoint 机制在 `setup.py` 中注册插件：

```
setup(
    entry_points={'vllm.platform_plugins': ["{your_platform_name} = {code_path}:{register_function}"]}
)
```

- `{your_platform_name}`：新后端的名称（可以任意）。
- `{code_path}`：主 Python 模块的路径。
- `{register_function}`：注册函数，返回步骤 1 中定义的 `Platform` 类的路径。

参考 vLLM Ascend 中的 [`setup.py`](https://github.com/vllm-project/vllm-ascend/blob/72a43a61d8d2193dddbfcc60578fd642008225a5/setup.py#L102) 查看实际示例。

---

### 用户视角

用户只需在运行前安装 vllm 和你的插件，以 [vllm-ascend](https://github.com/vllm-project/vllm-ascend) 为例：

```
pip install vllm vllm-ascend
```

启动时，你会看到如下日志，这表明后端插件工作正常：

```
INFO 02-06 15:49:01 __init__.py:30] Available plugins for group vllm.platform_plugins:
INFO 02-06 15:49:01 __init__.py:32] name=ascend, value=vllm_ascend:register
… …
INFO 02-06 15:49:01 __init__.py:44] plugin ascend loaded.
INFO 02-06 15:49:01 __init__.py:181] Platform plugin ascend is activated
```

---

## 接下来做什么？

接下来，我们将继续与 vLLM 社区的开发者合作，在以下方面进行增强：

1. 持续增强 V1 引擎和 VLM。
2. 扩展插件对更多模块和特性的支持，例如调度器、图模式和自定义算子。
3. 更好的用户体验和更高的性能。
4. 为合适的硬件平台维护和增强稳定的插件架构

我们鼓励大家试用这一新特性！如果你有任何问题，请加入 [vLLM Slack](https://slack.vllm.ai) 并参与 **#sig-extensible-hardware** 频道的讨论。 🚀

## 致谢

如果没有众多 vLLM 贡献者的努力，这一灵活的硬件后端插件机制将无从谈起。因此，我们深深感谢 vLLM 维护者 [Kaichao You](https://github.com/youkaichao)、[Simon Mo](https://github.com/simon-mo)、[Cyrus Leung](https://github.com/DarkLight1337)、[Robert Shaw](https://github.com/robertgshaw2-redhat)、[Michael Goin](https://github.com/mgoin) 和 [Jie Li](https://github.com/jeejeelee) 的相关重构、深入讨论和快速审查；感谢 vLLM 上的 Ascend 团队的 [Xiyuan Wang](https://github.com/wangxiyuan)、[Shanshan Shen](https://github.com/shen-shanshan)、[Chenguang Li](https://github.com/noemotiovon) 和 [Mengqing Cao](https://github.com/MengqingCao) 进行机制设计与实现；感谢 vLLM 上的 Spyre 团队的 [Joe Runde](https://github.com/joerunde) 和 [Yannick Schnider](https://github.com/yannicks1) 设计并实现可插拔调度器；也感谢其他贡献者，包括为可扩展量化方法的设计与实现做出贡献的 [yancong](https://github.com/ice-tong)，以及为可扩展 `SamplingParams` 做出贡献的 [Aviv Keshet](https://github.com/akeshet)。
