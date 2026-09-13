---
title: "vLLM Playground 发布：管理与交互 vLLM 服务器的现代化 Web 界面"
title_en: "Introducing vLLM Playground: A Modern Web Interface for Managing and Interacting with vLLM Servers"
source: https://vllm.ai/blog/2026-01-02-introducing-vllm-playground
crawled: 2026-09-12
translated: 2026-09-13
---

# vLLM Playground 发布：管理与交互 vLLM 服务器的现代化 Web 界面

> 原文：[Introducing vLLM Playground: A Modern Web Interface for Managing and Interacting with vLLM Servers](https://vllm.ai/blog/2026-01-02-introducing-vllm-playground) · vLLM 博客

micytao

[#前端](https://vllm.ai/blog/tags/frontend)[#生态](https://vllm.ai/blog/tags/ecosystem)

作为一名希望看到 vLLM 蓬勃发展、触达更多开发者的 vLLM 社区热心成员，我很高兴地宣布 **[vLLM Playground](https://github.com/micytao/vllm-playground)** 发布——这是一个功能丰富的现代化 Web 界面，用于管理和交互 vLLM 服务器。无论你是在 macOS 上本地开发、在带 GPU 的 Linux 上测试，还是部署到企业级 Kubernetes/OpenShift 集群，vLLM Playground 都能为你提供统一、直观的 vLLM 使用体验。

![](https://vllm.ai/blog-assets/figures/vllm-playground/vllm-playground-newUI.png)

## 为什么选择 vLLM Playground？

搭建和管理 vLLM 服务器通常需要命令行技能、容器编排知识，以及对各种配置选项的熟悉。vLLM Playground 通过以下方式消除了这些门槛：

- **零配置上手**：无需手动安装 vLLM——容器自动处理一切
- **一键操作**：通过直观的 UI 启动/停止服务器、切换模型、调整配置
- **跨平台支持**：支持 macOS（Apple Silicon）、Linux（CPU/GPU）以及企业级 Kubernetes 环境
- **处处一致的 UI**：从本地开发到云端部署，体验完全一致

## 愿景与路线图

vLLM Playground 的目标很简单：**紧跟 vLLM 官方项目的步伐，让每一个新功能都易于获取、易于试用**。

vLLM 正在快速演进，能力日益强大——结构化输出、工具调用、投机解码、多模态支持等等。然而，探索这些功能往往需要翻阅文档、编写脚本、管理配置。vLLM Playground 弥合了这一鸿沟：它提供可视化、可交互的界面，让你在新功能发布的那一刻就能上手实验。

**路线图上的下一步：**

- **🔗 MCP 服务器集成**：通过模型上下文协议（Model Context Protocol）增强工具能力
- **➕ RAG 支持**：检索增强生成，实现有知识依据的回答
- **🎯 功能对齐**：随着 vLLM 新能力落地，持续为其添加 UI 支持

## 快速开始

上手非常简单：

```
# Install from PyPI
pip install vllm-playground

# Pre-download container image (optional, ~10GB for GPU)
vllm-playground pull

# Start the playground
vllm-playground
```

打开 <http://localhost:7860>，点击「Start Server」，vLLM 就跑起来了！容器编排器会自动为你的平台拉取合适的镜像，并管理 vLLM 的生命周期。

## 核心特性

### 🎨 现代深色主题 UI

新界面采用简洁专业的设计，具备：

- **精简的聊天界面**：干净、无干扰的聊天 UI，带内联可展开面板
- **图标工具栏**：快速访问设置、系统提示、结构化输出和工具调用等高级功能
- **实时指标**：为每次响应显示 token 计数与生成速度
- **可调整面板**：自定义布局，打造最顺手的工作流

### 🏗️ 结构化输出

通过四种强大的模式约束模型响应格式：

| 模式 | 描述 | 示例用例 |
| --- | --- | --- |
| **Choice** | 强制输出为特定值 | 情感分析（正面/负面/中性） |
| **Regex** | 让输出匹配正则模式 | 邮箱、电话、日期格式校验 |
| **JSON Schema** | 生成符合你 schema 的有效 JSON | API 响应、结构化数据抽取 |
| **Grammar (EBNF)** | 定义复杂的输出结构 | 自定义 DSL、形式语言 |

![](https://vllm.ai/blog-assets/figures/vllm-playground/vllm-playground-structured-outputs.png)

### 🔧 工具调用 / 函数调用

让模型使用你定义的自定义工具和函数：

- **服务端配置**：启动前在 Server Configuration 面板中启用
- **自动识别解析器**：为 Llama 3.x、Mistral、Hermes、Qwen、Granite 和 InternLM 自动选择解析器
- **预设工具**：内置天气、计算器和搜索工具
- **自定义工具创建**：通过名称、描述和 JSON Schema 参数定义工具
- **并行工具调用**：支持同时调用多个工具

### 🐳 容器编排

vLLM Playground 在隔离的容器中管理 vLLM，提供：

- **自动生命周期管理**：启动、停止、健康检查和日志流式输出
- **智能容器复用**：配置未变时快速重启
- **跨平台镜像**：
  - GPU：`vllm/vllm-openai:v0.11.0`（官方）
  - CPU x86：`quay.io/rh_ee_micyang/vllm-cpu:v0.11.0`
  - macOS ARM64：`quay.io/rh_ee_micyang/vllm-mac:v0.11.0`

### 📊 GuideLLM 基准测试集成

由 [GuideLLM](https://github.com/neuralmagic/guidellm) 驱动的全面性能测试：

- 请求统计（成功率、耗时、平均时间）
- token 吞吐量分析（平均/中位 tokens per second）
- 延迟百分位（P50、P75、P90、P95、P99）
- 可配置的负载模式与请求速率
- 支持 JSON 导出以便深入分析

![](https://vllm.ai/blog-assets/figures/vllm-playground/guidellm.png)

### 📚 vLLM 社区配方（Recipes）

来自官方 [vLLM Recipes 仓库](https://github.com/vllm-project/recipes)的一键模型配置：

- **17+ 个模型类别**：DeepSeek、Qwen、Llama、Mistral、InternVL、GLM、NVIDIA Nemotron 等
- **可搜索的目录**：按模型名称、类别或标签筛选
- **一键加载**：即刻自动填入优化好的 vLLM 设置
- **硬件指导**：查看每个模型推荐的 GPU 配置

![](https://vllm.ai/blog-assets/figures/vllm-playground/vllm-recipes-1.png)

### ☸️ OpenShift/Kubernetes 部署

面向企业的云部署，具备：

- 通过 Kubernetes API 动态创建 vLLM pod
- 支持 GPU 与 CPU 模式，自动检测
- 基于 RBAC 的安全模型
- 自动化部署脚本
- 与本地部署相同的 UI 和工作流

```
cd openshift/
./deploy.sh --gpu    # For GPU clusters
./deploy.sh --cpu    # For CPU-only clusters
```

## 架构概览

vLLM Playground 采用混合架构，可在本地与云环境中无缝工作：

```
┌─────────────────────────────────────────────────────────────┐
│                     Web UI (FastAPI)                        │
│              app.py + index.html + static/                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ├─→ container_manager.py (Local)
                         │   └─→ Podman CLI
                         │       └─→ vLLM Container
                         │
                         └─→ kubernetes_container_manager.py (Cloud)
                             └─→ Kubernetes API
                                 └─→ vLLM Pods

```

容器管理器在构建时切换（Podman → Kubernetes），确保本地与云端的用户体验完全一致。

## macOS Apple Silicon 支持

对 macOS ARM64 的完整支持：

- 专为 Apple Silicon 构建的 CPU 优化容器镜像
- 自动平台检测
- 通过 Podman 实现无 root 容器执行
- 预配置的 CPU 设置以获得最佳性能

```
# Just start the Web UI - it handles containers automatically
python run.py
# Or use the CLI
vllm-playground
```

## CLI 命令

```
vllm-playground                    # Start with defaults
vllm-playground --port 8080        # Custom port
vllm-playground pull               # Pre-download GPU image (~10GB)
vllm-playground pull --cpu         # Pre-download CPU image
vllm-playground pull --all         # Pre-download all images
vllm-playground stop               # Stop running instance
vllm-playground status             # Check if running
```

## 参与贡献

vLLM Playground 是开源项目（Apache-2.0 许可证），欢迎贡献！

- **GitHub**：<https://github.com/micytao/vllm-playground>
- **PyPI**：<https://pypi.org/project/vllm-playground/>
- **Issue 与 PR**：欢迎提交 bug 报告、功能请求和 pull request

今天就试试：

```
pip install vllm-playground
vllm-playground
```

希望 vLLM Playground 能让你的 vLLM 开发与部署体验更顺畅、更愉快。祝服务顺利！🚀
