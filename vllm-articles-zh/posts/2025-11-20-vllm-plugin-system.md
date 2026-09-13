---
title: "使用 vLLM 插件系统构建整洁、可维护的 vLLM 定制修改"
title_en: "Building Clean, Maintainable vLLM Modifications Using the Plugin System"
source: https://vllm.ai/blog/2025-11-20-vllm-plugin-system
crawled: 2026-09-12
translated: 2026-09-13
---

# 使用 vLLM 插件系统构建整洁、可维护的 vLLM 定制修改

> 原文：[Building Clean, Maintainable vLLM Modifications Using the Plugin System](https://vllm.ai/blog/2025-11-20-vllm-plugin-system) · vLLM 博客

Dhruvil Bhatt（AWS SageMaker）

[#开发者](https://vllm.ai/blog/tags/developer)

> **注意：** 本文最初发表于这篇 [Medium 文章](https://medium.com/@dhruvilbhattlm10/building-clean-maintainable-vllm-modifications-using-the-plugin-system-e80df0f62861)。

![](https://vllm.ai/blog-assets/figures/2025-11-20-vllm-plugin-system/vllm-plugin-system-arch.png)
*图片来源：<https://github.com/vllm-project/vllm-ascend>*

---

## 概述

大语言模型推理一直在快速演进，[vLLM](https://github.com/vllm-project/vllm/) 已成为高吞吐、低延迟模型服务最强大的引擎之一。它提供连续批处理、高效调度、分页注意力（paged attention）和生产就绪的 API 层——使其成为从小型语言模型到庞大前沿系统的理想服务选择。

但正如任何快速演进的系统一样，总会出现团队或个人想要修改 vLLM 内部行为的时刻。也许你想试验自定义调度逻辑、改变 KV 缓存处理方式、注入专有优化，或者给模型执行流程的某一部分打补丁。

而真正的挑战正是从这里开始。

---

## 问题：「我需要修改 vLLM……然后怎么办？」

如果改动很简单，或者它对整个社区都有益，答案很直接：

### 方案 A - 将你的贡献上游合入 vLLM

这始终是最整洁的方式。你的改动存在于开源之中，接受社区评审，并与 vLLM 的演进保持同步。

然而，现实并不总是这么配合。许多修改是：

- **专有的**
- **领域特定的**
- **过于实验性的**
- **泛化程度不足以被上游接受**
- 或者**受内部时间表限制**，与开源评审周期不同步

当无法上游合入时，你必须另寻他路。

---

### 方案 B - 维护自己的 vLLM fork

这通常是第一反应：

> 「我们直接 fork vLLM，把改动加进去吧。」

这对微小、变动缓慢的项目可行，但 **vLLM 绝不属于这一类**。

vLLM 是一个极其活跃的仓库，新版本发布的频率快到**每两周一次**，每周合并**数百个 PR**。

维护一个长期存在的 fork 意味着：

- ❌ 不断地 rebase 或合并上游变更
- ❌ 在快速变动的区域解决冲突
- ❌ 手动重新套用你的补丁
- ❌ 执行繁重的兼容性测试
- ❌ 围绕一个自定义 vLLM 产物管理内部开发者工作流

用不了多久，这个 fork 就会变成一项**全职工作**。

对许多团队来说，这种运维负担根本不可持续。

---

### 方案 C - 使用 monkey patching（猴子补丁）

另一条路是构建一个小 Python 包，在构建时对原生 vLLM 应用猴子补丁。

乍一看，这很吸引人：

- ✅ 不需要 fork
- ✅ 不与原生 vLLM 分叉
- ✅ 补丁动态应用
- ✅ 代码占用小

……但现实远非理想。

猴子补丁通常需要替换整个类或模块，哪怕你只想改十行代码。这意味着：

- ❌ **你复制了 vLLM 源码的大块内容**——甚至包括你没有修改的部分
- ❌ **每次 vLLM 升级都会破坏你的补丁**——因为你替换的是完整文件，而不是你真正关心的那几行
- ❌ **调试变得痛苦**——bug 在你的补丁里？在未改动的原生代码里？还是因为猴子补丁意外重接了行为？
- ❌ **运维复杂度随时间增长**——每次 vLLM 发布都迫使你 diff 并重新同步你复制的文件——这和维护 fork 是完全相同的问题，只是藏在你的 Python 包里
- ❌ 对某些模块（如 `Scheduler`）打猴子补丁常常**行不通**，因为它们在独立进程中的 `EngineCore` 里运行。这可能导致进程同步问题：`EngineCore` 继续调用你本想修改的模块的旧实现。

猴子补丁解决了表面问题，却引入了可能失控的长期维护难题。

---

## 更整洁的替代方案：利用 vLLM 插件系统

为了克服 fork 与猴子补丁两者的局限，我研究了 vLLM 不断演进的 [general\_plugin 架构](https://docs.vllm.ai/en/stable/design/plugin_system.html)，它允许开发者在不改动上游代码的前提下，向引擎注入针对性的修改。

这一架构支持：

- ✅ 结构化、模块化的补丁
- ✅ 运行时激活
- ✅ 外科手术式的代码覆盖
- ✅ 兼容性保护
- ✅ 无需复制完整文件
- ✅ 无需猴子补丁式的花招
- ✅ 无需维护 fork

它在「全部上游合入」与「替换整个文件」之间提供了一个折中地带。

---

> **注意：** vLLM 提供了*四类*插件组/机制——平台插件（platform plugins）、引擎插件（engine plugins）、模型插件（model plugins）和**通用插件（general plugins）**。本文专门聚焦**通用插件系统**，它会在所有 vLLM 进程中加载，因此非常适合本文所述的整洁 vLLM 修改方式。关于不同插件组的更多细节，请参阅 vLLM 文档：[支持的插件类型](https://docs.vllm.ai/en/latest/design/plugin_system/#types-of-supported-plugins)。

---

## 使用 vLLM 插件构建整洁的扩展框架

利用插件系统，我创建了一个小型扩展包，作为所有自定义修改的容器。它不替换整个模块，也不 fork 整个仓库，每个补丁：

- 只包含**恰好需要改动的代码片段或类**
- 可以**在运行时启用或禁用**
- 可以声明**最低支持的 vLLM 版本**
- 可以保持**休眠状态，除非某个特定模型配置请求它**

由于插件在运行时应用，我们可以维护**一个统一的容器镜像**来服务多个模型，同时按模型选择性地启用不同补丁。

这一方法受 [ArcticInference](https://github.com/snowflakedb/ArcticInference) 等基于插件的设计启发，在运行时以整洁且可选择的方式注入补丁。

---

## 实现：创建你的第一个 vLLM 插件包

让我们一步步构建一个基于 vLLM `general_plugins` 入口点的插件式扩展系统。

### 项目结构

```
vllm_custom_patches/
├── setup.py
├── vllm_custom_patches/
│   ├── __init__.py
│   ├── core.py              # Base patching infrastructure
│   └── patches/
│       ├── __init__.py
│       └── priority_scheduler.py
└── README.md

```

---

### 核心补丁基础设施

基础是一个允许外科手术式修改的整洁补丁机制：

```
# vllm_custom_patches/core.py
import logging
from types import MethodType, ModuleType
from typing import Type, Union
from packaging import version
import vllm

logger = logging.getLogger(__name__)

PatchTarget = Union[Type, ModuleType]

class VLLMPatch:
    """
    Base class for creating clean, surgical patches to vLLM classes.

    Usage:
        class MyPatch(VLLMPatch[TargetClass]):
            def new_method(self):
                return "patched behavior"

        MyPatch.apply()
    """

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, '_patch_target'):
            raise TypeError(
                f"{cls.__name__} must be defined as VLLMPatch[Target]"
            )

    @classmethod
    def __class_getitem__(cls, target: PatchTarget) -> Type:
        if not isinstance(target, (type, ModuleType)):
            raise TypeError(f"Can only patch classes or modules, not {type(target)}")

        return type(
            f"{cls.__name__}[{target.__name__}]",
            (cls,),
            {'_patch_target': target}
        )

    @classmethod
    def apply(cls):
        """Apply this patch to the target class/module."""
        if cls is VLLMPatch:
            raise TypeError("Cannot apply base VLLMPatch class directly")

        target = cls._patch_target

        # Track which patches have been applied
        if not hasattr(target, '_applied_patches'):
            target._applied_patches = {}

        for name, attr in cls.__dict__.items():
            if name.startswith('_') or name in ('apply',):
                continue

            if name in target._applied_patches:
                existing = target._applied_patches[name]
                raise ValueError(
                    f"{target.__name__}.{name} already patched by {existing}"
                )

            target._applied_patches[name] = cls.__name__

            # Handle classmethods
            if isinstance(attr, MethodType):
                attr = MethodType(attr.__func__, target)

            setattr(target, name, attr)
            action = "replaced" if hasattr(target, name) else "added"
            logger.info(f"✓ {cls.__name__} {action} {target.__name__}.{name}")

def min_vllm_version(version_str: str):
    """
    Decorator to specify minimum vLLM version required for a patch.

    Usage:
        @min_vllm_version("0.9.1")
        class MyPatch(VLLMPatch[SomeClass]):
            pass
    """
    def decorator(cls):
        original_apply = cls.apply

        @classmethod
        def checked_apply(cls):
            current = version.parse(vllm.__version__)
            minimum = version.parse(version_str)

            if current < minimum:
                logger.warning(
                    f"Skipping {cls.__name__}: requires vLLM >= {version_str}, "
                    f"but found {vllm.__version__}"
                )
                return

            original_apply()

        cls.apply = checked_apply
        cls._min_version = version_str
        return cls

    return decorator
```

---

### 补丁示例：基于优先级的调度

现在让我们创建一个具体的补丁，为 vLLM 添加优先级调度：

```
# vllm_custom_patches/patches/priority_scheduler.py
import logging
from vllm.core.scheduler import Scheduler
from vllm_custom_patches.core import VLLMPatch, min_vllm_version

logger = logging.getLogger(__name__)

@min_vllm_version("0.9.1")
class PrioritySchedulerPatch(VLLMPatch[Scheduler]):
    """
    Adds priority-based scheduling to vLLM's scheduler.

    Requests can include a 'priority' field in their metadata.
    Higher priority requests are scheduled first.

    Compatible with vLLM 0.9.1+
    """

    def schedule_with_priority(self):
        """
        Enhanced scheduling that respects request priority.

        This method can be called instead of the standard schedule()
        to enable priority-aware scheduling.
        """
        # Get the standard scheduler output
        output = self._schedule()

        # Sort by priority if metadata contains priority field
        if hasattr(output, 'scheduled_seq_groups'):
            output.scheduled_seq_groups.sort(
                key=lambda seq: getattr(seq, 'priority', 0),
                reverse=True
            )

            logger.debug(
                f"Scheduled {len(output.scheduled_seq_groups)} sequences "
                f"with priority ordering"
            )

        return output
```

---

### 插件入口点与注册表

插件系统把一切串联起来：

```
# vllm_custom_patches/__init__.py
import os
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

class PatchManager:
    """Manages registration and application of vLLM patches."""

    def __init__(self):
        self.available_patches: Dict[str, type] = {}
        self.applied_patches: List[str] = []

    def register(self, name: str, patch_class: type):
        """Register a patch for later application."""
        self.available_patches[name] = patch_class
        logger.info(f"Registered patch: {name}")

    def apply_patch(self, name: str) -> bool:
        """Apply a single patch by name."""
        if name not in self.available_patches:
            logger.error(f"Unknown patch: {name}")
            return False

        try:
            self.available_patches[name].apply()
            self.applied_patches.append(name)
            return True
        except Exception as e:
            logger.error(f"Failed to apply {name}: {e}")
            return False

    def apply_from_env(self):
        """
        Apply patches specified in VLLM_CUSTOM_PATCHES environment variable.

        Format: VLLM_CUSTOM_PATCHES="PatchOne,PatchTwo"
        """
        env_patches = os.environ.get('VLLM_CUSTOM_PATCHES', '').strip()

        if not env_patches:
            logger.info("No custom patches specified (VLLM_CUSTOM_PATCHES not set)")
            return

        patch_names = [p.strip() for p in env_patches.split(',') if p.strip()]
        logger.info(f"Applying patches: {patch_names}")

        for name in patch_names:
            self.apply_patch(name)

        logger.info(f"Successfully applied: {self.applied_patches}")

# Global manager instance
manager = PatchManager()

def register_patches():
    """
    Main entry point called by vLLM's plugin system.
    This function is invoked automatically when vLLM starts.
    """
    logger.info("=" * 60)
    logger.info("Initializing vLLM Custom Patches Plugin")
    logger.info("=" * 60)

    # Import and register all available patches
    from vllm_custom_patches.patches.priority_scheduler import PrioritySchedulerPatch

    manager.register('PriorityScheduler', PrioritySchedulerPatch)

    # Apply patches based on environment configuration
    manager.apply_from_env()

    logger.info("=" * 60)
```

---

### setup 配置

`setup.py` 文件将插件注册到 vLLM：

```
# setup.py
from setuptools import setup, find_packages

setup(
    name='vllm-custom-patches',
    version='0.1.0',
    description='Clean vLLM modifications via the plugin system',
    packages=find_packages(),
    install_requires=[
        'vllm>=0.9.1',
        'packaging>=20.0',
    ],
    # Register with vLLM's plugin system
    entry_points={
        'vllm.general_plugins': [
            'custom_patches = vllm_custom_patches:register_patches'
        ]
    },
    python_requires='>=3.11',
)
```

---

## 使用示例

### 安装

```
# Install the plugin package
pip install -e .
```

### 以不同配置运行

```
# Vanilla vLLM (no patches)
VLLM_CUSTOM_PATCHES="" python -m vllm.entrypoints.openai.api_server \
    --model mistralai/Mistral-7B-Instruct-v0.2

# With priority scheduling patch
VLLM_CUSTOM_PATCHES="PriorityScheduler" python -m vllm.entrypoints.openai.api_server \
    --model meta-llama/Meta-Llama-3-70B-Instruct
```

### Docker 集成

```
# Dockerfile
FROM vllm/vllm-openai:latest

COPY . /workspace/vllm-custom-patches/
RUN pip install -e /workspace/vllm-custom-patches/

ENV VLLM_CUSTOM_PATCHES=""

CMD python -m vllm.entrypoints.openai.api_server \
    --model ${MODEL_NAME} \
    --host 0.0.0.0 \
    --port 8000
```

```
# Run with patches
docker run \
    -e MODEL_NAME=meta-llama/Meta-Llama-3-70B-Instruct \
    -e VLLM_CUSTOM_PATCHES="PriorityScheduler" \
    -p 8000:8000 \
    vllm-with-patches

# Run vanilla vLLM
docker run \
    -e MODEL_NAME=mistralai/Mistral-7B-Instruct-v0.2 \
    -e VLLM_CUSTOM_PATCHES="" \
    -p 8000:8000 \
    vllm-with-patches
```

---

## 工作原理：vLLM 插件生命周期

理解补丁在何时以及如何被应用至关重要。以下是完整的生命周期：

### vLLM 自动加载插件

**关键洞察：** vLLM 的架构涉及多个进程，尤其是在使用张量并行、流水线并行或其他并行技术进行分布式推理时。为确保一致性，vLLM 会在它创建的**每一个进程**中、在该进程开始任何实际工作之前，自动调用 `load_general_plugins()`。

这意味着：

- ✅ 你的补丁会被加载到**主进程**
- ✅ 你的补丁会被加载到**所有 worker 进程**
- ✅ 你的补丁会被加载到 **GPU worker、CPU worker 以及任何辅助进程**
- ✅ 加载发生在**模型初始化之前**、调度器创建之前、任何推理开始之前

### 完整的启动序列

当 vLLM 启动时，每个进程中会发生：

1. **进程创建：** vLLM 生成一个新进程（主进程、worker 等）
2. **插件系统激活：** vLLM 在任何其他 vLLM 工作之前内部调用 `load_general_plugins()`
3. **入口点发现：** Python 的入口点系统找到所有已注册的 `vllm.general_plugins`
4. **插件函数执行：** 我们的 `register_patches()` 函数被调用
5. **补丁注册：** 可用补丁被注册到管理器
6. **环境检查：** 读取 `VLLM_CUSTOM_PATCHES` 变量
7. **选择性应用：** 只应用通过 `VLLMPatch.apply()` 指定的补丁
8. **版本校验：** 每个补丁通过 `@min_vllm_version` 检查 vLLM 版本兼容性
9. **外科手术式修改：** 特定方法被添加/替换到目标类上
10. **vLLM 正常启动：** 直到此时，vLLM 才继续进行模型加载、调度器初始化等

这保证了你的补丁始终**在 vLLM 做任何事之前**就已生效，确保所有进程行为一致，并防止竞态条件。

---

## 基于插件的扩展方式的优势

### 1. 极小、外科手术式的补丁定义

没有重复的文件。没有冗余的代码。只有修改本身。`VLLMPatch` 系统让你可以只添加单个方法，而不必复制整个类。

### 2. 同一 vLLM 构建支持多个模型

不同的模型可以通过 `VLLM_CUSTOM_PATCHES` 环境变量启用不同的补丁。

### 3. 版本感知的安全检查

每个补丁都可以声明其最低要求的版本：

```
@min_vllm_version("0.9.1")
class MyPatch(VLLMPatch[TargetClass]):
    pass
```

这可以避免升级过程中出现意外行为。

### 4. 告别 fork、同步与 rebase

升级 vLLM 就像 `pip install --upgrade vllm` 然后测试你的补丁一样简单。

### 5. 消除了猴子补丁的复杂性

干净、可追踪的修改，不再有传统猴子补丁式的静默破坏。

### 6. vLLM 官方支持

使用 vLLM 官方的 `general_plugins` 入口点系统，也就是说这是一个受支持的扩展机制。

---

## 为什么这一模式重要

当推理引擎高速演进时，团队常常被迫在以下两者之间二选一：

- 修改内部行为
- **或者**保持与上游版本的兼容性

基于插件的扩展模式**消除了这种取舍**。它让你既能快速创新，又能与快速成长的 vLLM 生态保持同步。

这种方式把运维开销降到最低，同时保持了长期灵活性——无论小团队还是大型平台团队都会受益。

---

## 结语

如果你正在试验或部署 vLLM，并且发现需要自定义行为，请在选择 fork 或猴子补丁策略之前，先考虑利用通用插件系统。

它在**控制力**、**可维护性**与**心智健全**之间取得了恰当的平衡——并让你的代码库保持整洁、模块化和面向未来。

### 要点回顾：

- ✅ 使用 `VLLMPatch[TargetClass]` 进行外科手术式的类级修改
- ✅ 在 `setup.py` 中通过 `vllm.general_plugins` 入口点注册
- ✅ 用 `VLLM_CUSTOM_PATCHES` 环境变量控制补丁。
  - 注意：`VLLM_CUSTOM_PATCHES` **不是** vLLM 官方的环境变量——它只是本文使用的一个示例。你可以在自己的插件包中选择任意环境变量名。
- ✅ 用 `@min_vllm_version` 装饰器为补丁加上版本保护
- ✅ 一个 Docker 镜像，多种配置

这一模式已在生产环境中被证明有效，并可以从实验性原型一直扩展到多模型生产部署。

---

### 联系我

如果你对推理系统的插件式架构感兴趣，或者想探讨如何以整洁的方式组织运行时补丁，欢迎联系我。我一直乐于聊可扩展 LLM 部署与设计模式😊 你可以通过以下方式找到我：

- **LinkedIn:** <https://www.linkedin.com/in/dhruvil-bhatt-uci/>
- **个人网站** - <https://www.dhruvilbhatt.com/>
- **邮箱：** [dhruvilbhattlm10@gmail.com](mailto:dhruvilbhattlm10@gmail.com)
