---
title: "用 Ray symmetric-run 简化多节点服务"
title_en: "Streamlined multi-node serving with Ray symmetric-run"
source: https://vllm.ai/blog/2025-11-22-ray-symmetric-run
crawled: 2026-09-12
translated: 2026-09-13
---

# 用 Ray symmetric-run 简化多节点服务

> 原文：[Streamlined multi-node serving with Ray symmetric-run](https://vllm.ai/blog/2025-11-22-ray-symmetric-run) · vLLM 博客

Richard Liaw（Anyscale/Ray）、Kaichao You（vLLM）

[#大规模服务](https://vllm.ai/blog/tags/large-scale-serving)

Ray 现在有了一个新命令：`ray symmetric-run`。这个命令使得在 Ray 集群的每个节点上启动**同一条入口命令**成为可能，简化了在 HPC 环境或使用 `mpssh` 等并行 SSH 工具时，为多节点模型启动 vLLM 服务器的工作流。

在这篇博客中，我们会谈谈当前用 Ray 启动 vLLM 服务器方式存在的问题；我们会走一遍一个 motivating example（动机示例）；最后我们会讨论 Ray 的新 `symmetric-run` API 将如何改善启动体验。

Ray 近期加入了 PyTorch 基金会。作为这次捐赠的一部分，vLLM 与 Ray 团队正在共同努力建立深度协同，以推进下一代 AI 基础设施。

![](https://vllm.ai/blog-assets/figures/2025-11-25-ray-symmetric-run/symmetric-run.png)
图 1. Ray 的 `symmetric-run` 命令概览。

### 背景

接触 Ray 的 vLLM 用户往往带着来自既有工具与工作流的预期。在裸机集群上做交互式开发的开发者，期望能用 `mpssh` 或 `pssh` 之类的工具快速在多台主机上启动命令，并用以「rank」为参数的单条命令完成。熟悉 SLURM 和 PBS 的 HPC 用户期望*对称执行*——一个同时在所有节点上运行的单一程序入口，类似于 MPI 应用。

然而，Ray 推荐的作业执行模式遵循另一种哲学，为头节点（head node）与工作节点（worker node）设定了不同角色。

程序入口在头节点上执行，由它编排并把工作分派给工作节点。运行时生命周期与作业执行是分离的，需要显式的集群管理。这意味着用户需要两套不同的命令——一套用来以正确的 head/worker 角色搭建集群，另一套用来真正运行工作。

### 动机示例

让我们走一遍在 2 台独立机器上启动分布式作业的例子。我们假设这些机器是「裸」的，即无法使用 Ray 的 cluster launcher 或 KubeRay 等其他方案。

在这种情况下，要在多台机器上运行 Ray 作业，用户需要先在头节点上启动 Ray：

```
ray start --block
```

然后在工作节点上，需要回连头节点：

```
# worker node, terminal 1:
ray start --block --address='ip:6379'
```

节点就绪后，需要在头节点上另开一个终端来运行作业：

```
vllm serve Qwen/Qwen3-32B --tensor-parallel-size 8 --pipeline-parallel-size 2
```

终止时，还需要在每个节点上运行 `ray stop`：

```
ray stop
```

在这种配置下运行 vLLM 通常需要相当多的反复试错。一个常见的失败模式是缺少某些环境变量，比如 `VLLM_HOST_IP`。发生这种情况时，用户需要关闭 Ray 集群，在 `ray start` 上设置好环境变量，然后把上面的步骤重新走一遍。

对于期望对称、单命令执行的用户来说，这给他们的开发和部署工作流带来了显著的摩擦。

Ray 现在提供了一个简单的解决方案：**`ray symmetric-run`**，一种在集群所有节点上运行 Ray 作业的新方式。

### `symmetric-run` 做了什么？

`ray symmetric-run` 让你可以在 Ray 集群的每个节点上启动**同一条入口命令**。该脚本自动处理 Ray 的搭建、作业执行与清理，让用户获得类似 `mpirun` 或 `torchrun` 等工具的体验。

以与上面相同的例子来说，使用 `symmetric-run`，你只需：

```
# in SLURM sbatch script or via mpssh

ray symmetric-run \
  --address <head_node_address>:6379 \
  --min-nodes 2 \
  --num-gpus 8 \
  -- vllm serve Qwen/Qwen3-32B --tensor-parallel-size 8 --pipeline-parallel-size 2
```

每个节点都会执行同一条命令，但底层行为因节点而异。具体而言，工作节点只执行 Ray 集群初始化，而头节点会：

1. 以 `--head` 模式启动 Ray。
2. 等待四个节点注册。
3. 运行你的用户命令（`vllm serve Qwen/Qwen3-32B …`）。
4. 结束后关闭 Ray。

工作节点只需运行 `ray start --address head-node:6379` 并等待作业结束，随后自动退出。无需额外的 SSH 编排或启动脚本。

如果需要提供环境变量，只需把它加在命令前面，`symmetric-run` 会自动把该变量传播到 Ray 运行时：

```
ENV=VAR ray symmetric-run --address 127.0.0.1:6379 -- python test.py
```

### 结论

Ray 的新 symmetric run 工具简化了在 HPC 或并行 SSH 环境中运行 Ray 与 vLLM 程序的过程。今天就试试 Ray Symmetric Run：<https://docs.ray.io/en/latest/cluster/vms/user-guides/community/slurm.html>

如果遇到任何问题，请在 Github 上开一个 issue：<https://github.com/ray-project/ray/>

想与社区其他成员交流，欢迎加入 [vLLM slack](https://communityinviter.com/apps/vllm-dev/join-vllm-developers-slack) 和 [Ray slack](https://www.ray.io/join-slack)！
