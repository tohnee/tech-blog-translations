---
title: "轻松安装与开发 vLLM"
title_en: "Installing and Developing vLLM with Ease"
source: https://vllm.ai/blog/2025-01-10-dev-experience
crawled: 2026-09-12
translated: 2026-09-12
---

# 轻松安装与开发 vLLM

> 原文：[Installing and Developing vLLM with Ease](https://vllm.ai/blog/2025-01-10-dev-experience) · vLLM 博客

vLLM 团队

[#开发者](https://vllm.ai/blog/tags/developer)

LLM 推理领域正以前所未有的速度前进。新模型和新功能每周都在涌现，传统的软件发布流程常常难以跟上。在 vLLM，我们希望提供的不只是一个软件包。我们正在构建一个系统——一个可信、可追踪、可参与的 LLM 推理生态。本博文重点介绍 vLLM 如何让用户轻松安装与开发，同时始终站在创新的最前沿。

## TL;DR：

- 灵活快速的安装选择，从稳定版本到 nightly 构建。
- 为 Python 与 C++/CUDA 开发者提供精简的开发工作流。
- 为生产部署提供强大的版本追踪能力。

## 无缝安装 vLLM 各个版本

### 安装已发布版本

我们会定期将 vLLM 稳定版本发布到 [Python Package Index](https://pypi.org/project/vllm/)，确保用户可以使用标准 Python 包管理器轻松安装。例如：

```
pip install vllm
```

对于偏好更快包管理器的用户，[**uv**](https://github.com/astral-sh/uv) 在 vLLM 社区中日益流行。在使用 uv 设置好 Python 环境后，安装 vLLM 非常简单：

```
uv pip install vllm
```

关于设置 [**uv**](https://github.com/astral-sh/uv) 的更多细节，请参阅[文档](https://docs.vllm.ai/en/latest/getting_started/installation/gpu.html?device=cuda#create-a-new-python-environment)。在一套简单的服务器级配置（Intel 第 8 代 CPU）上，我们观察到 [**uv**](https://github.com/astral-sh/uv) 比 pip 快 200x：

```
# with cached packages, clean virtual environment
$ time pip install vllm
...
pip install vllm 59.09s user 3.82s system 83% cpu 1:15.68 total

# with cached packages, clean virtual environment
$ time uv pip install vllm
...
uv pip install vllm 0.17s user 0.57s system 193% cpu 0.383 total
```

### 从 Main 分支安装最新 vLLM

为满足社区对前沿特性和模型的需求，我们为 main 分支上的每次提交提供 nightly wheel 包。

**使用 pip**：

```
pip install vllm --pre --extra-index-url https://wheels.vllm.ai/nightly
```

加上 `--pre` 可确保 pip 在搜索时包含预发布版本。

**使用 uv**：

```
uv pip install vllm --extra-index-url https://wheels.vllm.ai/nightly
```

## 让开发变得简单

我们深知，一个活跃、投入的开发者社区是创新的支柱。正因如此，vLLM 为开发者提供了顺畅的工作流——无论他们是在修改 Python 代码还是编写内核。

### Python 开发者

对于需要调整和测试 vLLM Python 代码的 Python 开发者，无需编译内核。这种设置让你可以快速开始开发。

```
git clone https://github.com/vllm-project/vllm.git
cd vllm
VLLM_USE_PRECOMPILED=1 pip install -e .
```

`VLLM_USE_PRECOMPILED=1` 标志会指示安装程序使用预编译的 CUDA 内核，而不是从源码构建，从而大幅缩短安装时间。这对于专注于 Python 层面特性（如 API 改进、模型支持或集成工作）的开发者是理想选择。

这一轻量流程即使在笔记本电脑上也能高效运行。更高级的用法请参阅我们的[文档](https://docs.vllm.ai/en/latest/getting_started/installation/gpu.html?device=cuda#build-wheel-from-source)。

### C++/内核开发者

对于从事 C++ 代码或 CUDA 内核工作的高级贡献者，我们引入了编译缓存以尽量缩短构建时间、简化内核开发。更多细节请查看我们的[文档](https://docs.vllm.ai/en/latest/getting_started/installation/gpu.html?device=cuda#build-wheel-from-source)。

## 轻松追踪变更

LLM 推理快速演进的特性意味着接口和行为仍在稳定过程中。vLLM 已被集成到许多工作流中，包括 [OpenRLHF](https://github.com/OpenRLHF/OpenRLHF)、[veRL](https://github.com/volcengine/verl)、[open\_instruct](https://github.com/allenai/open-instruct)、[LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory) 等。我们与这些项目合作，共同稳定 LLM 推理的接口与行为。为推进这一过程，我们为这些高级用户提供了强大的工具，用于追踪跨版本的变更。

### 安装特定 Commit

为了简化追踪与测试，我们为 main 分支的每次提交提供 wheel 包。用户可以轻松安装任何特定 commit，这在二分定位（bisect）和追踪变更时尤其有用。

我们推荐使用 [**uv**](https://github.com/astral-sh/uv) 安装特定 commit：

```
# use full commit hash from the main branch
export VLLM_COMMIT=72d9c316d3f6ede485146fe5aabd4e61dbc59069
uv pip install vllm --extra-index-url https://wheels.vllm.ai/${VLLM_COMMIT}
```

在 [**uv**](https://github.com/astral-sh/uv) 中，`--extra-index-url` 中的包[优先级高于默认索引](https://docs.astral.sh/uv/pip/compatibility/#packages-that-exist-on-multiple-indexes)，这使得安装早于最新公开发布版本（撰写本文时为 v0.6.6.post1）的开发中版本成为可能。

相比之下，pip 会将 `--extra-index-url` 与默认索引中的包合并，只选择最新版本，这使得安装早于已发布版本的开发中版本变得困难。因此，对于 pip 用户，需要指定一个占位 wheel 名称来安装特定 commit：

```
# use full commit hash from the main branch
export VLLM_COMMIT=33f460b17a54acb3b6cc0b03f4a17876cff5eafd
pip install https://wheels.vllm.ai/${VLLM_COMMIT}/vllm-1.0.0.dev-cp38-abi3-manylinux1_x86_64.whl
```

## 结语

在 vLLM，我们的承诺不止于交付高性能软件。我们正在构建一个赋予信任、支持透明追踪变更、并欢迎积极参与的系统。让我们携手塑造 AI 的未来，在推动创新边界的同时，让创新惠及所有人。

如有合作请求或咨询，请致信 [vllm-questions@lists.berkeley.edu](mailto:vllm-questions@lists.berkeley.edu)。欢迎在 [GitHub](https://github.com/vllm-project/vllm) 上加入我们不断壮大的社区，或在 [vLLM Slack](https://slack.vllm.ai/) 上与我们联系。让我们一起推动 AI 创新向前。

## 致谢

我们感谢 [uv 社区](https://docs.astral.sh/uv/)——特别是 [Charlie Marsh](https://github.com/charliermarsh)——打造了这个快速、创新的包管理器。特别感谢 [Kevin Luu](https://github.com/khluu)（Anyscale）、[Daniele Trifirò](https://github.com/dtrifiro)（Red Hat）和 [Michael Goin](https://github.com/mgoin)（Neural Magic）为精简工作流做出的宝贵贡献。来自 UC Berkeley 团队的 [Kaichao You](https://github.com/youkaichao) 和 [Simon Mo](https://github.com/simon-mo) 领导了这些工作。
