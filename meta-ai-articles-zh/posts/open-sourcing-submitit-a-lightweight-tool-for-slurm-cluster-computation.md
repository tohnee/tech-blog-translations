---
title: "开源 Submitit：面向 Slurm 集群计算的轻量工具"
title_en: "Open-sourcing Submitit: A lightweight tool for Slurm cluster computation"
date: 2020-08-25
source: https://ai.facebook.com/blog/open-sourcing-submitit-a-lightweight-tool-for-slurm-cluster-computation
crawled: 2026-09-22
translated: 2026-09-22
---

# 开源 Submitit：面向 Slurm 集群计算的轻量工具

> 原文：[Open-sourcing Submitit: A lightweight tool for Slurm cluster computation](https://ai.facebook.com/blog/open-sourcing-submitit-a-lightweight-tool-for-slurm-cluster-computation) · Meta AI（Wayback 存档）

**它是什么：**Submitit 是一个轻量工具，用于提交 Python 函数到 Slurm 集群中计算。Slurm 是一个开源、高度可扩展的集群作业调度系统，在工业界和学术界都被广泛使用。在 Facebook AI Research（FAIR），我们使用一个由 Slurm 管理的、拥有数千块 GPU 的集群，研究人员在其上训练神经网络。Submitit 简化了在集群上调度实验并收集结果、日志等工作。我们发布 Submitit，以帮助其他研究人员在 Slurm 集群上运行他们的实验。

**它做了什么：**Submitit 与标准库 concurrent.futures 共享相同的基础 Executor API，还附带一些其他特性。

```python
import submitit

def add(a, b):
    return a + b

# ask for resources
executor = submitit.AutoExecutor(folder="my_shared_folder")
executor.update_parameters(gpus_per_node=2)

# submit to the cluster
job = executor.submit(add, 5, 7)  # will compute add(5, 7)

# waits for completion and returns output
output = job.result()  # 5 + 7 = 12... your addition was computed in the cluster
assert output == 12
```

这个 Executor 接口与 dask.distributed 包的类似，只是层级更低，可以直接访问日志、错误，以及抢占或超时情况下的检查点处理（一项高级特性）。得益于共享的 API，代码可以在「用 submitit.AutoExecutor 在 Slurm 集群上运行」与「在本地用多进程（concurrent.futures.ProcessPoolExecutor）或多线程（concurrent.futures.ThreadPoolExecutor）运行」之间直截了当地转换。Submitit 还可以配置为在本地运行以便测试，其插件系统也为未来支持新的集群留出了空间。

**为什么重要：**Submitit 让研究人员能够轻松地从本机上的小规模实验切换到集群上的大规模实验。他们可以用自己熟悉的语言（Python）工作，更轻松地分析结果、调度更多实验。Submitit 的开源版本将让我们的研究人员更容易发布和共享开源代码。如果找不到集群，Submitit 会自动回退到本地运行实验，这使得第三方可以克隆 FAIR 论文的开源代码并立即开始运行小规模实验。

Submitit 已直接集成到我们的多个开源 Python 项目中，包括：

- **Nevergrad**：一个无导数优化平台，可用于优化神经网络训练的超参数。Nevergrad 优化的主方法可以接受可选的 Executor 参数，因此优化既可以在本地并行运行，也可以用 concurrent.futures、submitit 或 dask.distributed 在集群上运行。
- **Hydra**：一个用于优雅配置复杂应用的框架。该框架支持在应用参数上进行扫描（包括 Nevergrad 超参数调优），而借助 Hydra 的 submitit 插件，这些扫描现在可以在 Slurm 上运行。

**GitHub 获取地址：**https://github.com/facebookincubator/submitit

**作者**

- Guillaume Wenzek，研究工程师
- Jérémy Rapin，研究工程师
