---
title: "Gemini Robotics 把 AI 带入物理世界"
title_en: "Gemini Robotics brings AI into the physical world"
source: https://deepmind.google/blog/gemini-robotics-brings-ai-into-the-physical-world/
site: deepmind
date: 2025-03-12
crawled: 2026-09-13
translated: 2026-09-13
---

# Gemini Robotics 把 AI 带入物理世界

> 原文：[Gemini Robotics brings AI into the physical world](https://deepmind.google/blog/gemini-robotics-brings-ai-into-the-physical-world/) · Google DeepMind

我们推出 Gemini Robotics，这是我们基于 Gemini 2.0、专为机器人技术设计的模型

在 Google DeepMind，我们一直在推进 Gemini 模型通过跨文本、图像、音频和视频的多模态推理来解决复杂问题的能力。然而迄今为止，这些能力在很大程度上仍局限于数字领域。要让 AI 在物理领域中真正对人有用、有帮助，它们必须展现出"具身"推理——即像人一样理解并对周遭世界做出反应的能力——同时还要能安全地采取行动把事情办成。

今天，我们推出两个基于 Gemini 2.0 的新 AI 模型，它们为新一代有用的机器人奠定了基础。

第一个是 Gemini Robotics，一个先进的视觉-语言-动作（VLA）模型，构建于 Gemini 2.0 之上，并新增物理动作作为新的输出模态，用于直接控制机器人。第二个是 Gemini Robotics-ER，一个具备高级空间理解能力的 Gemini 模型，使机器人专家能够利用 Gemini 的具身推理（ER）能力运行他们自己的程序。

这两个模型都能让各种机器人执行比以往更广泛的真实世界任务。作为这项工作的一部分，我们正与 Apptronik 合作，用 Gemini 2.0 构建下一代人形机器人。我们还与一批经过挑选的可信测试者合作，共同指引 Gemini Robotics-ER 的未来方向。

我们期待探索这些模型的能力，并在通往真实世界应用的道路上继续开发它们。

![](https://lh3.googleusercontent.com/rQvqvsZb5dMgbR9LFKeMlUcaOWY0NTEd2d8-d_xeO6A84MXiluORxTIxLkUZ98O_Tit52oew2lZgbaatVNGrU92gaSMCH1Q7nFuVd_f4LMtLYkgxFg=w1440-h810-n-nu)

我们工作成果的概览

## Gemini Robotics：我们最先进的视觉-语言-动作模型

要对人有用、有帮助，机器人领域的 AI 模型需要具备三项主要素质：它们必须是通用的，即能够适应不同的情况；它们必须是交互式的，即能够快速理解并响应指令或环境变化；它们必须是灵巧的，即能够完成人们通常用手和手指可以做的事情，例如精细地操作物体。

虽然我们此前的工作在这些领域展示了进展，但 Gemini Robotics 在全部三个维度上都实现了显著的性能跃升，让我们更接近真正通用的机器人。

### 通用性

Gemini Robotics 利用 Gemini 对世界的理解来泛化到新情况，开箱即用地解决多种多样的任务，包括它在训练中从未见过的任务。Gemini Robotics 还善于应对新物体、多样化指令和新环境。在[我们的技术报告](https://arxiv.org/abs/2503.20020)中，我们展示了在一个全面的泛化基准测试上，Gemini Robotics 的平均表现是其他最先进视觉-语言-动作模型的两倍以上。

![](https://lh3.googleusercontent.com/n2By6bFHJPOFYCYpbrfUzdO2K09uqSRcamcYJ1qu-lh2S8L8_oYermL5qjOsQBJwATKBkhLyLatmXNgHM4KRhCQeclf2mH-1eBu0t5M_UEXA84zNAw=w1440-h810-n-nu)

Gemini Robotics 世界理解能力的演示。

### 交互性

要在我们这个动态的物理世界中运作，机器人必须能够与人及其周围环境无缝交互，并随机应变地适应变化。

由于建立在 Gemini 2.0 的基础之上，Gemini Robotics 具有直觉式的交互能力。它利用 Gemini 先进的语言理解能力，可以理解并以日常会话语言、以不同语言表述的指令并做出回应。

与之前的模型相比，它能理解并响应更广泛的自然语言指令集合，并根据你的输入调整自身行为。它还会持续监控周围环境，检测环境或指令的变化，并相应调整自己的动作。这种控制能力，或者说"可操控性"，能更好地帮助人们在从家庭到工作场所的各种场景中与机器人助手协作。

![](https://lh3.googleusercontent.com/-TSwa6jvlFbAbtIoHIfDfrXEpZACC-ROkVz0SKXm-Lc4uldO33XbQiWiX_SOwKegzbpZn4IkrFdmCjXZNw1oNtkeRHh4iiqOgfCPki99jJ9bgJ8k7w=w1440-h810-n-nu)

如果物体从它的抓握中滑落，或者有人挪动了物品，Gemini Robotics 会迅速重新规划并继续执行——这是现实世界中的机器人的关键能力，因为在那里意外才是常态。

### 灵巧性

构建有用机器人的第三根支柱是具备[灵巧性](https://deepmind.google/discover/blog/advances-in-robot-dexterity/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=)的行动。人类轻松完成的许多日常任务，其实需要出人意料的精细运动技能，对机器人来说仍然太难。相比之下，Gemini Robotics 能够应对极其复杂、需要精确操作的多步骤任务，例如折纸，或者把零食装进密封保鲜袋。

![](https://lh3.googleusercontent.com/x8ppIjczt6xr0H5ficw-WvO7vEy8O9rn15SgsYNN0-BmZoXBIqn3Mhu8F-BacgdMKsjMbAXtv8p4b9bEhyXHpxflICKPSOc5CGBIvvXqefCV31bbrA=w1440-h810-n-nu)

Gemini Robotics 展现出高水平的灵巧操作

### 多种本体

最后，由于机器人有各种形状和尺寸，Gemini Robotics 也被设计为能够轻松适配不同类型的机器人。我们主要使用双臂机器人平台 [ALOHA 2](https://aloha-2.github.io/) 的数据训练该模型，但我们也证明它可以控制一个基于许多学术实验室使用的 Franka 机械臂的双臂平台。Gemini Robotics 甚至可以针对更复杂的本体进行专门化，例如 Apptronik 开发的人形机器人 Apollo，目标是完成真实世界的任务。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

Gemini Robotics 可以在不同类型的机器人上工作

## 增强 Gemini 的世界理解

与 Gemini Robotics 一起，我们还推出一个名为 Gemini Robotics-ER（"具身推理"的缩写）的先进视觉语言模型。该模型以机器人技术所需的方式增强 Gemini 对世界的理解，尤其聚焦空间推理，并允许机器人专家把它与现有的底层控制器连接起来。

Gemini Robotics-ER 大幅提升了 Gemini 2.0 的既有能力，比如指向和 3D 检测。通过把空间推理与 Gemini 的代码能力相结合，Gemini Robotics-ER 能够即时实例化全新的能力。例如，当看到一个咖啡杯时，该模型可以直觉出一种合适的两指抓取方式——握住杯柄——以及一条接近它的安全轨迹。

Gemini Robotics-ER 开箱即可执行控制机器人所需的全部步骤，包括感知、状态估计、空间理解、规划和代码生成。在这种端到端的设置中，该模型的成功率达到 Gemini 2.0 的 2 到 3 倍。而在代码生成不够用的场合，Gemini Robotics-ER 甚至可以借助上下文学习的力量，仿照少数几个人类示范的模式来提供解决方案。

![Gemini Robotics-ER 擅长多种具身推理能力，包括检测物体、指向物体部件、寻找对应点以及检测 3D 物体。这是一组展示这些能力的可视化拼贴。左上：2D 物体检测，右上：指向，左下：多视角对应，右下：3D 物体检测。](https://lh3.googleusercontent.com/DM4OXpSjM_WxgFGTlzilbnx9iyBvWCEKTh6xza2uZa4MGfwJ38kyoWYRM8HpyZGLZP_czByK-74rYs3h9osaHU-i5JBvzLDHAZd3fvvCH7phDvuB1Q=w1440)

Gemini Robotics-ER 擅长多种具身推理能力，包括检测物体、指向物体部件、寻找对应点以及检测 3D 物体。

## 负责任地推进 AI 与机器人技术

在我们探索 AI 与机器人技术持续潜力的过程中，我们对研究中的安全问题采取一种分层的、[整体性的](https://sites.google.com/corp/view/safe-robots?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=)方法，覆盖从底层运动控制到高层语义理解的各个环节。

机器人及其周围人员的物理安全，是机器人科学中由来已久的根本关切。正因如此，机器人专家拥有一系列经典安全措施，例如避免碰撞、限制接触力的大小，以及确保移动机器人的动态稳定性。Gemini Robotics-ER 可以与这些针对特定本体的"底层"安全关键控制器对接。在 Gemini 核心安全特性之上，我们让 Gemini Robotics-ER 模型能够判断某个潜在动作在给定情境下是否安全，并生成恰当的响应。

为了推动学术界和产业界的机器人安全研究，我们还发布了一个新的数据集，用于评估和改进具身 AI 与机器人技术中的语义安全。在以往的工作中，我们展示了受 Isaac Asimov 机器人三定律启发的[机器人宪章](https://deepmind.google/discover/blog/shaping-the-future-of-advanced-robotics/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=)如何帮助提示一个大语言模型为机器人挑选更安全的任务。此后，我们开发了一个框架，可自动生成数据驱动的宪章——直接以自然语言表达的规则——来引导机器人的行为。这一框架使人们能够创建、修改和应用宪章，开发出更安全、更符合人类价值观的机器人。最后，[新的 ASIMOV 数据集](https://asimov-benchmark.github.io/)将帮助研究者严格测量机器人动作在真实场景中的安全影响。

为了进一步评估我们工作的社会影响，我们与负责任开发与创新团队的专家以及我们的责任与安全委员会——一个致力于确保我们负责任地开发 AI 应用的内部评审小组——展开合作。我们还就具身 AI 在机器人应用中带来的特定挑战与机遇咨询外部专家。

除了与 Apptronik 的合作之外，我们的 Gemini Robotics-ER 模型还向包括 Agile Robots、Agility Robots、Boston Dynamics 和 Enchanted Tools 在内的可信测试者开放。我们期待探索这些模型的能力，继续开发 AI，为下一代更有用的机器人贡献力量。

[阅读我们的论文](https://arxiv.org/abs/2503.20020)

**致谢**

本工作由 Gemini Robotics 团队开发。完整的作者与致谢名单请见[我们的技术报告](https://arxiv.org/abs/2503.20020)。
