---
title: "Claude 计算机使用与浏览器使用的最佳实践"
title_en: "Best practices for computer and browser use with Claude"
source: https://claude.com/blog/best-practices-for-computer-and-browser-use-with-claude/
crawled: 2026-09-14
translated: 2026-09-14
---

# Claude 计算机使用与浏览器使用的最佳实践

> 原文：[Best practices for computer and browser use with Claude](https://claude.com/blog/best-practices-for-computer-and-browser-use-with-claude/) · Claude 博客

Claude 的[最新模型](https://www.anthropic.com/news/claude-sonnet-4-6)在计算机使用（computer use）与浏览器使用（browser use）能力上迈出了重要一步。借助这些能力，大语言模型如今能够驱动日益复杂的智能体系统去完成真实工作，比如构建软件应用，以及在多种彼此异构的技术之间自动化工作流。

在这篇博客文章中，我们分享使用 Claude 进行计算机使用与浏览器使用的最佳实践，从简单的配置改动到更高级的集成模式都有涵盖。希望这篇文章能帮助你着手把 Claude 的计算机使用与浏览器使用能力集成到你的产品中。我们同时还在发布一个新的[演示实现（demo implementation）](https://github.com/anthropics/claude-quickstarts/tree/main/computer-use-best-practices)，它封装了其中一部分最佳实践，并提供了在 Claude 计算机使用能力之上进行开发时颇为实用的附加工具。

*请注意，除非另有说明，这些建议适用于 Claude 4.6 家族（Opus 4.6、Sonnet 4.6、Haiku 4.5）以及 Claude Opus 4.7。当 4.6 家族与 Opus 4.7 的指导存在差异时，我们会在文中就地指出。我们的结论基于内部实验，随着新模型与新技术的出现，未来可能更新。*

# **入门：分辨率与缩放**

点击准确性是任何计算机使用集成的基石。如果点击没有落在它该落的地方，下游的一切都会失效：表单填不了，按钮按不到，工作流失败。影响最大的单项优化同时也是最简单的优化之一：在把截图发送给 API 之前，预先缩小（downscale）它们。

## **确保正确的缩放**

当你把一张截图发送给 Claude 的 Computer Use API 时，模型会看到它，并在你指定的 display_width_px / display_height_px 坐标空间中返回点击坐标。但有一个重要的约束：API 对图像尺寸有内部处理上限。超出这些上限的图像会在模型看到之前被降采样，这意味着模型是在基于图像的降质版本进行点击，而你的执行框架（harness）却期望坐标对齐到原始分辨率。

对我们的 Claude 4.6 模型家族，API 的限制为：

- **最长边上限**：1568 像素
- **总像素上限**：1.15 百万像素
- 超出**任一**限制的图像会被内部降采样

我们的 Opus 4.7 模型支持更高的分辨率。限制为：

- **最长边上限**：2576 像素
- **总像素上限**：3.75 百万像素
- 超出**任一**限制的图像会被内部降采样

当坐标空间与模型感知到的图像不一致时，模型预测的点击就会落在与它实际看到的图像不同的显示比例上。这是高分辨率下点击不准确的主要原因。修复方法很直接：在把截图发送给 API 之前，始终先把它缩小到这些限制之内。我们持续观察到图像超限时会出现的显著准确率下降，而这一项改动的价值几乎超过任何其他优化。

## **推荐的分辨率**

**从 1280x720 开始。**这是对大多数用例都安全、实用的默认值。它大约用掉 80% 的像素预算，稳稳落在最长边和总像素两项限制之内，并且是模型在训练中见过的标准分辨率。它对现代 Web UI 和老式桌面应用都表现良好。

**如果你使用的是 Opus 4.7，我们建议从 1080p 开始**，因为它相比 720p 带来有意义的质量提升，并在 token 用量与性能之间取得了良好平衡。

**对于想要最大化模型所接收视觉信息的开发者**，我们还推荐一种「max API fit」（最大化适配 API）方法：基于源图的原始宽高比，为每张图像计算最优分辨率：

```
import math

# 1568 for 4.6 family, 2576 for Opus 4.7
MAX_LONG_EDGE = 1568

# 1.15MP for 4.6 family, 3.75MP for Opus 4.7
MAX_PIXELS = 1_150_000

def compute_max_api_fit(native_w, native_h):
    """Compute the largest resolution that fits API limits
    while preserving aspect ratio."""
    aspect = native_w / native_h

    # Compute max dimensions from pixel budget
    h_from_pixels = math.sqrt(MAX_PIXELS / aspect)
    w_from_pixels = h_from_pixels * aspect

    # Apply long edge constraint
    if native_w >= native_h:
        w = min(w_from_pixels, MAX_LONG_EDGE)
        h = w / aspect
    else:
        h = min(h_from_pixels, MAX_LONG_EDGE)
        w = h * aspect

    # Never upscale beyond native
    w = min(w, native_w)
    h = min(h, native_h)

    return int(w), int(h)
```

这种方法稍微复杂一些，但避免了宽高比失真，并用满了每张图像可用的全部像素预算。相比固定的 1280x720，准确性提升是适度的，但它实现简单，还能避免把 16:9 的源图强行塞进 4:3 显示分辨率时产生的那种失真。

**应避免的分辨率：**

- **原始分辨率（不缩放）**：除非你的源图恰好低于分辨率上限，否则直接发送原始分辨率截图是点击准确性差的最常见原因。
- **非常低的分辨率（低于 960x540）**：分辨率过低时，丢失的细节太多，模型无法准确识别小型 UI 元素。
- **在 MacOS 上**：浏览器使用的一个常见问题是 MacOS 的截图通常以设备像素比（device pixel ratio）为 2 采集，这意味着你可能得到分辨率是屏幕坐标 2 倍的图像。
- **如果你在 4.6 家族上，避免 1920x1080 及以上**：这些超出了像素上限，会被静默降采样。在 Opus 4.7 上上限更高（3.75 MP），因此 1080p 和 1440p 都在预算之内；但仍应避免不做降缩放直接使用原生 4K。

## **坐标缩放**

当你在发送前缩放了截图，模型会以你指定的显示分辨率返回点击坐标。在执行点击之前，你必须把这些坐标缩放回你的实际屏幕分辨率：

```
# Your screen is screen_w x screen_h
# You sent a screenshot resized to display_w x display_h
scale_x = screen_w / display_w
scale_y = screen_h / display_h

screen_x = int(api_returned_x * scale_x)
screen_y = int(api_returned_y * scale_y)
```

这一步简单却至关重要，因为一旦忘记缩放，或者 `display_width_px` / `display_height_px` 与你发送的图像实际尺寸不一致，每一次点击都会稳定地产生偏移。

## **messages 数组中的内容顺序**

构建 messages 内容数组时，把文本指令放在图像*之前*，如下面的代码片段所示。这让模型在处理截图时就知道自己在找什么，从而提高点击准确性。

```
# RECOMMENDED — text instruction first, then screenshot:
content = [
    {"type": "text", "text": "Click on the Submit button"},
    {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": screenshot_b64}},
]

# NOT RECOMMENDED — image first, then text:
content = [
    {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": screenshot_b64}},
    {"type": "text", "text": "Click on the Submit button"},
]
```

## **诊断点击问题**

如果点击总是打不中目标，通常可以归结为下面几种原因之一：

| 症状 | 可能原因 | 建议尝试 |
|---|---|---|
| 点击持续向同一个方向偏移 | `display_width_px` / `display_height_px` 与实际发送的图像尺寸不匹配<br>截图超出 API 限制而被静默降采样<br>内容顺序是图像在前而非文本在前 | 确保显示尺寸与你缩放后的截图完全一致，而不是原始分辨率<br>预缩放到 1280x720 或使用 `compute_max_api_fit`<br>把文本指令移到 content 数组中图像之前 |
| 点击落在大致正确的区域但没点中目标 | 目标非常小（复选框、图标、开关）<br>源图分辨率非常高（4K+），降采样时丢失细节<br>强制非原始宽高比导致比例失真 | 对密集 UI 启用 `enable_zoom: True`<br>以更低的 DPI 采集，或在降采样前裁剪到相关屏幕区域<br>缩放时保持源图的宽高比 |
| 模型完全点错了元素 | 指令含糊（存在多个类似提交的按钮时只说「点击 Submit」）<br>目标附近存在视觉相似的元素<br>UI 过于复杂，单条指令难以覆盖 | 使用带位置上下文的更具体提示（「点击表单右下角蓝色的 Submit 按钮」）<br>把复杂交互拆成更小的步骤<br>提供关于页面布局的额外上下文 |
| 整体准确率都很差 | 截图以超出 API 限制的尺寸发送<br>源图来自超高分辨率显示屏（4K+），压缩比极端<br>分辨率过低，丢失关键细节 | 预缩放所有截图，使其符合限制<br>在 4.6 家族上处理 4K+ 源图时，Sonnet 比 Opus 4.6 更能承受重度降采样。在 Opus 4.7 上这一差距基本消失，使用 4.7 的像素预算（最高 3.75 MP）可以从一开始就减少降采样<br>以 1280x720 作为基线；若损失过大，使用 `compute_max_api_fit` |

## **为点击任务选择模型**

根据我们的内部测试，Claude Sonnet 4.6 在点击的机械精准度上往往更强（更好的空间准确性、更少的擦边失误），而 Claude Opus 4.6 带来更强的推理能力。当源图需要重度降采样时，Sonnet 4.6 也更稳健。

Opus 4.7 缩小了这一差距：通过测试，我们发现它的点击精准度大致与 Sonnet 4.6 持平，而且它更高的分辨率预算从源头上减少了所需的降采样量，使它成为「想要 Opus 级推理又搭配强点击准确性」时的有力选择。

对大多数任务，我们建议从 Sonnet 4.6 开始，它在点击准确性、推理和成本之间提供了最佳平衡。当你想要更强的推理能力时选择 Opus 4.7，尤其是在使用高分辨率源图的情况下。当延迟是首要考量时，Haiku 4.5 仍然是极好的选择。高级工作流仍可能受益于「编排器 + 子智能体」模式：由推理模型负责规划与决策，由 Sonnet 或 Haiku 执行机械的点击步骤。

## **应对小目标**

目标越小，点击准确性越差。大中型 UI 元素（按钮、输入框和标准菜单项）在安全区内所有分辨率下都很可靠。挑战在于小和极小的目标，比如复选框、系统托盘图标、下拉箭头、小型拨动开关，以及树形视图的展开/折叠按钮。

如果你的应用需要频繁点击小目标，可以考虑以下策略：

**对密集 UI 使用缩放（zoom）。**Claude 4.6 和 4.7 模型支持一项缩放能力，让模型在点击之前以更高分辨率检查特定的屏幕区域。在你的[工具配置](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)中启用它：

```
{
    "type": "computer_20251124",
    "name": "computer",
    "display_width_px": 1280,
    "display_height_px": 720,
    "enable_zoom": True
}
```

**把目标做大。**如果你能控制被自动化的 UI，增大点击目标（哪怕幅度不大）对可靠性的影响不成比例地大。这可能意味着使用更低的系统 DPI、在浏览器中放大，或调整 UI 缩放设置。

**对极小目标使用键盘替代方案。**对于非常小的元素，比如系统托盘图标或极小的复选框，键盘快捷键或基于 Tab 的导航可能比点击更可靠。如果你的工作流允许，提示模型在特定步骤使用键盘交互可以提升成功率。

**考虑源图分辨率。**来自 4K+ 显示屏、被压缩到 720p 的截图会丢失大量细节（例如，一个原生 3840x2160 下 16px 的复选框，在 1280x720 显示分辨率下大约只剩 5px，这让目标小得多、也更难点中）。如果你面对的是超高分辨率显示屏，考虑使用分辨率上限比以往模型更高的 Opus 4.7。如果使用 4.6 模型，考虑以更低的 DPI 采集、用显示缩放放大 UI 元素，或者让截图聚焦于屏幕的相关区域而非整个显示器。由于这些模型用更少的像素表示更多信息，我们观察到源图尺寸越大性能越差，也就是说需要更多的压缩。

## **我们测试过但没有帮助的方法**

我们在内部评估中试验了几种流行的优化技术，没有发现这些方法带来一致的提升，尽管结果可能因具体情况而异：

- **把图像切成更小的瓦片（tile）**：把截图切成四象限或多个区域分别发送，并没有提升点击准确性。
- **叠加带坐标的网格**：在截图上叠加可视化坐标网格来帮助模型定位目标，没有产生可靠的收益。
- **缩放算法的选择**：PIL LANCZOS、sips 和其他常见的缩放算法产生了完全相同的结果。用你技术栈里顺手的那一个即可。

## **检查失败案例**

如果在尝试上述修复后模型行为仍不可预测，请记录完整的对话记录（transcript），并把预测的点击叠加到源截图上，以理解模型实际看到和决定的内容。

有些失败根本与点击准确性无关。例如，某些下拉菜单会调用浏览器视口捕获不到的系统级 UI——模型看起来像是任务失败了，但它只是看不到自己需要交互的那个菜单。在这类情况下，模型应改用其他方法，例如执行 JavaScript、键盘导航或直接操作文档对象模型（DOM），而不是点击。

## **快速参考**

*如何缩放并准备一张用于 computer use 的图像*

```
import math
from PIL import Image
import base64
import io

# 1568 for 4.6 family, 2576 for Opus 4.7
MAX_LONG_EDGE = 1568

# 1.15MP for 4.6 family, 3.75MP for Opus 4.7
MAX_PIXELS = 1_150_000

def prepare_screenshot(screenshot: Image.Image, native_w: int, native_h: int) -> tuple[str, int, int]:
    """Resize a screenshot to fit API limits and return base64 + display dimensions."""

    # Option A: Fixed 720p (simple, reliable)
    display_w, display_h = 1280, 720

    # Option B: Max API fit (maximizes fidelity)
    # display_w, display_h = compute_max_api_fit(native_w, native_h)

    resized = screenshot.resize((display_w, display_h), Image.LANCZOS)

    buffer = io.BytesIO()
    resized.save(buffer, format="PNG")
    b64 = base64.standard_b64encode(buffer.getvalue()).decode()

    return b64, display_w, display_h


def scale_coordinates(api_x: int, api_y: int, display_w: int, display_h: int,
                      screen_w: int, screen_h: int) -> tuple[int, int]:
    """Scale API-returned coordinates back to native screen space."""
    screen_x = int(api_x * (screen_w / display_w))
    screen_y = int(api_y * (screen_h / display_h))
    return screen_x, screen_y


def compute_max_api_fit(native_w: int, native_h: int) -> tuple[int, int]:
    """Compute the largest resolution that fits API limits while preserving aspect ratio."""
    aspect = native_w / native_h
    h_from_pixels = math.sqrt(MAX_PIXELS / aspect)
    w_from_pixels = h_from_pixels * aspect

    if native_w >= native_h:
        w = min(w_from_pixels, MAX_LONG_EDGE)
        h = w / aspect
    else:
        h = min(h_from_pixels, MAX_LONG_EDGE)
        w = h * aspect

    w = min(w, native_w)
    h = min(h, native_h)
    return int(w), int(h)
```

**用法：**

```
import anthropic
from PIL import Image

client = anthropic.Anthropic()

# Capture screenshot (your method here)
screenshot = Image.open("screenshot.png")
native_w, native_h = screenshot.size

# Prepare for API
b64, display_w, display_h = prepare_screenshot(screenshot, native_w, native_h)

# Send to Claude — text before image
response = client.beta.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=4096,
    betas=["computer-use-2025-11-24"],
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "Click on the Submit button"},
            {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": b64}},
        ]
    }],
    tools=[{
        "type": "computer_20251124",
        "name": "computer",
        "display_width_px": display_w,
        "display_height_px": display_h,
    }],
)

# Scale coordinates back for execution
api_x, api_y = extract_click_coords(response)  # your parsing logic
screen_x, screen_y = scale_coordinates(api_x, api_y, display_w, display_h, native_w, native_h)
```

# **为 computer use 调节思考努力等级**

Claude 的最新模型支持[自适应思考（adaptive thinking）](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking)，这一设置让 Claude 自行决定在行动之前要对中间步骤进行多少推理。它无需手动设置思考 token 预算，而是让 Claude 根据每个请求的复杂度动态决定何时以及使用多少扩展思考（extended thinking）。对 computer use 而言，这意味着 Claude 可以想清楚它在屏幕上看到的东西、规划多步交互，并在真正点击或敲键之前自我纠正。

借助自适应思考，Claude 的思考深度通过 thinking 参数和一个努力等级（effort level）来控制：low、medium、high、xhigh（Opus 4.7 支持）以及 max。思考越多，意味着每个动作的推理越多，但也意味着更多输出 token、更高延迟和更高成本。

一个自然的问题是：依模型而定，多少思考对 computer use 才是最优的？

## **Claude Opus 4.7**

我们在一套覆盖桌面应用、浏览器和多应用工作流的端到端 UI 自动化任务上测试了每个思考努力等级。

**Opus 4.7 优于 4.6 家族。**在 OSWorld Verified 基准测试上，我们发现 Opus 在相同的 token 用量和努力等级设置下优于所有 4.6 家族模型。Opus 4.7 以 low 努力取得的分数与 Sonnet 4.6 以 max 努力取得的分数相当，而每个任务使用的 token 约为后者的 1/10。对于困难的任务，Opus 4.7 是显而易见的选择。

**把努力等级设为 `high`** 能取得接近最高的任务成功率，而输出 token 只用 `max` 的大约一半。与 Opus 4.6 相比，low、medium 和 high 消耗的 token 数量大体相同，同时提升了 OSWorld 上的分数。在我们的内部测试中，max 努力消耗了更多 token 并取得了最佳分数。下表概述了我们对何时使用各思考努力等级的建议。

### **努力等级建议**

| 场景 | 思考努力 | 原因 |
|---|---|---|
| 大多数用例的默认选择 | `high` | Opus 4.7 最擅长困难任务。使用 high 可以给模型足够的推理去规划复杂的多步交互，同时不会显著增加 token 用量。 |
| 高吞吐 / 成本敏感 | `low` | 更低的 token 用量，同时质量介于 Opus 4.6 的 high 与 max 努力设置之间。 |
| 简单、定义明确的工作流 / 追求最快 | 建议尝试 Sonnet 4.6 | 如果低延迟是最高优先级就用它。适用于 UI 稳定、工作流已知的短小、可预测任务。 |
| 复杂的一次性任务 | `max` | 当任务极具挑战性、你需要第一次尝试就做对时使用。 |

## **Claude 4.6 模型**

有两个模式很突出：

**medium 努力是最佳平衡点。**把努力设为 medium 能取得接近最高的任务成功率，而输出 token 只用 high 的大约一半。超过 medium 之后，性能大体趋于平台期。值得注意的是，当任务允许重试时，medium 和 high 会收敛到相同的成功率。这意味着 high 努力可能帮助模型第一次尝试就做对困难任务，但如果允许多次尝试，medium 或许能以更低的成本同样可靠地到达终点。

**一点思考就很有用。**low 努力是一个出奇强劲的选择。它实际使用的总输出 token 甚至*少于*完全关闭思考（模型犯的错更少，需要的重试轮次更少），同时达到与不思考持平或略高的准确性。这使它成为成本敏感、高吞吐工作负载的最佳选择。下表概述了我们的努力等级建议。

| 场景 | 思考努力 | 原因 |
|---|---|---|
| 大多数用例的默认选择 | `medium` | 最佳的准确性-成本比。给模型足够的推理去规划多步交互而不过度思考。配合重试，能以一半的 token 成本达到 high 的表现。 |
| 高吞吐 / 成本敏感 | `low` | 比不思考更准确，同时因更少的错误与重试而 token 用量更低。 |
| 简单、定义明确的工作流 / 追求最快 | 关闭思考 | 如果低延迟是最高优先级就用它。适用于 UI 稳定、工作流已知的短小、可预测任务。 |
| 复杂的一次性任务 | `high` | 当任务有挑战性、你需要第一次尝试就做对时使用。如果你的系统支持重试，medium 可能达到同样的最终成功率。 |

我们不建议在 computer use 中使用 `max` 努力。在我们的测试中，它相较 `high` 没有带来准确性收益，反而进一步增加了输出 token 成本。UI 任务主要是感知性而非深度逻辑性的，额外的推理预算要么用不上，要么导致过度思考。请记住，这些建议会随着模型演进而过时。

## **medium 努力等级的示例配置**

```
import anthropic

client = anthropic.Anthropic()

response = client.beta.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=16000,
    betas=["computer-use-2025-11-24"],
    thinking={"type": "adaptive"},
    output_config={"effort": "medium"},
    messages=[...],
    tools=[
        {
            "type": "computer_20251124",
            "name": "computer",
            "display_width_px": 1280,
            "display_height_px": 720,
        }
    ],
)
```

## **为什么更多思考并不总是有帮助**

UI 自动化任务与编程或数学问题有着本质区别。大多数 computer use 动作是感知性和机械性的：识别正确的元素、在正确的位置点击，而不是深度逻辑性的。思考在以下情况下帮助最大：

- 在开始之前规划多步序列（例如，「我需要打开设置，导航到隐私，然后关闭追踪」）
- 从意料之外的 UI 状态中恢复（例如，出现了一个没有预料到的对话框）
- 在屏幕上的信息与任务指令之间交叉核对
- 在专业软件上完成有挑战性的项目

# **提升安全性：利用提示注入分类器**

*本节介绍提示注入防护。如果你使用我们的官方 computer use 工具头（tool header），该防护默认提供且免费。但如果你有兴趣在自定义的计算机或浏览器使用工具上启用它，请填写我们的*[**提示注入分类器意向表。**](https://docs.google.com/forms/d/e/1FAIpQLSfXj6rXC-SUQEYHCLabwUe5JuYiYyJ29Ja-KP7EhLIPlyz0tw/viewform?usp=dialog)

计算机使用智能体在设计上就要与不可信内容交互。Claude 处理的每张截图、每个网页或应用 UI 都可能包含对抗性指令，包括隐藏文本、被操纵的图像、欺骗性 UI 元素，或试图劫持智能体行为的社工话术。这种攻击面与典型的 API 集成有着本质不同——后者中输入由你控制。而在 computer use 中，模型的输入是开放的互联网，以及智能体正在操作的任何软件。

随着计算机使用智能体变得更能干、部署得更广泛，提示注入也相应成为更严重的风险。一个能点击、打字和导航的智能体可能被操纵去执行现实世界的动作，例如填写表单、下载文件或导航到恶意 URL。针对这些攻击构建稳健的防御，对任何生产部署来说都必不可少。

## **我们如何开展提示注入防御**

我们已经详细撰写过我们针对浏览器与计算机使用的[提示注入防御方法](https://www.anthropic.com/research/prompt-injection-defenses)。我们的防御策略在多个层级上运作：

**训练时稳健性。**我们使用强化学习把提示注入抵抗力直接构建进 Claude 的能力中。在训练期间，Claude 会接触到嵌入在模拟网页和应用 UI 中的注入内容，并在正确识别且拒绝遵循恶意指令时获得奖励。这意味着 Claude 的第一道防线是模型本身——它已学会区分合法的用户指令与任务执行过程中遇到的对抗性内容。

**实时分类器。**我们运行探针（probe）扫描进入 Claude 上下文窗口的内容，并标记潜在的提示注入企图。这些探针跨多种模态检测对抗性命令，例如藏在页面内容中的文本、嵌入图像中的指令，以及设计用来欺骗智能体的欺骗性 UI 元素，并在识别到攻击时调整 Claude 的行为。

**持续红队测试。**我们的安全研究人员持续探测这些防御，我们也参与外部对抗性评估，以衡量针对不断演进的攻击技术的稳健性。

自我们最初的 computer use 研究预览以来，我们持续在这三个层级上大力投入。每一代新模型都纳入了更强的训练时防御和更强大的分类器，我们也扩展了红队评估所针对的攻击技术范围。

## **使用 Claude 内置的分类器**

当你通过 API 使用 Claude 的[官方 computer use 工具](https://docs.anthropic.com/en/docs/agents-and-tools/computer-use)时，提示注入分类器会在每个请求上自动运行。这些分类器与主模型推理并行运行，为你的请求增加的额外延迟约为零，也不产生额外成本。

你不需要做任何配置来启用这层防护。只要你使用官方的 `computer_20251124` 工具类型，它默认开启。分类器会评估截图和其他内容中提示注入的迹象，并相应地影响 Claude 的响应。

```
# Classifiers run automatically when using the official CU tool — no extra config needed
tools = [
    {
        "type": "computer_20251124",
        "name": "computer",
        "display_width_px": 1280,
        "display_height_px": 720,
    }
]
```

## **如果你没有使用官方 computer use 工具**

许多开发者使用自定义工具定义而非官方的 `computer_20251124` 工具类型来构建计算机使用集成，例如定义自己的截图与点击工具。如果你的情况如此，上述内置分类器目前不会在你的请求上运行。

我们正在积极探索如何把提示注入防护扩展到这些自定义实现。如果你在没有官方工具类型的情况下构建计算机使用或浏览器使用集成，并对提示注入分类器感兴趣，请[填写这份意向表](https://docs.google.com/forms/d/e/1FAIpQLSfXj6rXC-SUQEYHCLabwUe5JuYiYyJ29Ja-KP7EhLIPlyz0tw/viewform?usp=dialog)，在该能力可用时我们会跟进联系你。

## **无论是否使用分类器都应遵循的最佳实践**

分类器只是防御的一层，不是完整的解决方案。对于任何计算机使用部署，我们都推荐以下实践：

**为高风险动作实现人在回路（human-in-the-loop）。**让智能体在执行不可逆动作（如提交表单、购物、发送消息或修改数据）之前暂停并请求用户确认。无论分类器表现如何，这都是针对提示注入最有效的单项缓解措施。

**限定智能体的权限范围。**限制智能体能做什么。如果你的工作流不需要下载文件，就不要给智能体下载文件的权限。如果它不需要发邮件，就不要给它邮件客户端的访问权。缩小一次成功注入的影响范围（blast radius），与阻止注入本身同等重要。

**监控并记录智能体的动作。**记录智能体采取的完整动作序列，包括每一步的截图。这让你能够发现异常行为、在出问题时审计发生了什么，并构建一个反馈回路来持续改进系统的稳健性。

**把所有网页内容视为不可信。**设计智能体的系统提示，清晰区分用户的指令与任务执行期间遇到的内容。提醒模型：在网页、电子邮件或应用 UI 中发现的文本并非来自用户，不应被当作指令。

# **computer use 的上下文管理**

构建计算机使用智能体时，截图累积得非常快。每个动作都会生成一张新图像，而每张图像按分辨率不同大约消耗 1,000–1,800 个 token。在计入系统提示、工具定义和文本内容之后，一个 200k 的上下文窗口用不到 100 张截图就能填满。

管理好这份上下文有两个目标：1) 让总 token 量有界；2) 保持提示缓存（prompt caching）有效，这样你就不必为同一个前缀反复支付全价。我们发现，有效的[上下文管理](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)对长时间运行智能体的成本和延迟的影响，几乎超过任何其他优化。本节介绍三个可以干净组合的层级：放置缓存断点、在不破坏缓存的情况下修剪旧截图，以及在修剪不够用时对历史做摘要。

## **放置缓存断点**

只有当断点落在会跨轮次重复出现的内容上时，提示缓存才有帮助。API 总共支持四个缓存断点。把四个全放在稳定前缀（系统提示、工具定义）上是一种浪费，因为该前缀命中一次之后永远不会失效，一个断点就够了。另外三个断点更适合花在最近的历史上，那里失效风险最高，而且收益会在长会话中复利累积。

我们建议：

- **在系统提示或尾部工具定义上放一个断点。**这个前缀在一个会话内很少变化。
- **在最近的工具结果上再放至多三个断点**，每轮前移并清除上一轮的断点，以免超出四个断点的上限。

把断点分散在最近的位置可以带来优雅降级。如果你最近的断点失效了——例如因为一次图像修剪、一次压缩（compaction）或工具定义变更——更早的断点仍可命中，你只需支付全价输入成本的 10% 而不是 100%。

*缓存控制与设置断点的示例：*

```
def set_trailing_cache_control(messages, max_breakpoints=3):
    """Place up to `max_breakpoints` ephemeral cache_control markers on the
    most recent tool_result blocks, after clearing any existing markers."""
    for msg in messages:
        for block in msg.get("content", []):
            if isinstance(block, dict):
                block.pop("cache_control", None)

    placed = 0
    for msg in reversed(messages):
        for block in reversed(msg.get("content", [])):
            if placed >= max_breakpoints:
                return
            if isinstance(block, dict) and block.get("type") == "tool_result":
                block["cache_control"] = {"type": "ephemeral"}
                placed += 1
```

## **方法 1：滚动缓冲区（缓存感知）**

让 token 数量有界的最简单方法，是只保留最近 N 张截图并丢弃其余的。在每次 API 调用之前，遍历消息数组，用一段简短的占位文本（例如一个写着「[Image omitted]」的文本块）替换较旧的图像块。

这个模式的朴素版本是随着截图老化逐张丢弃，这会每一轮都改变前缀，持续使提示缓存失效。滚动缓冲区之所以背负「破坏缓存」的名声，正是源于此。修复方法是分批修剪，让前缀在若干轮内保持字节级一致，然后一次性失效，然后再次保持稳定。

我们测试过的一个具体模式是：

1. 以完整分辨率保留最近 keep_n 张截图。
2. 一旦截图总数超过 keep_n + interval，就在一次遍历中把最旧的 interval 张截图替换为占位符。
3. 在两次修剪事件之间，消息数组逐轮字节级一致，因此你的缓存断点会持续命中。

合理的起始默认值：keep_n = 3，interval = 25。这些都是可调的：interval 越大意味着修剪事件越少（缓存效率更高），但上下文中保留完整分辨率截图的尾部更大（token 更多）。在一条有代表性的轨迹上测量缓存命中率与总输入 token，并据此调整。

*在保留缓存断点的同时修剪旧截图的示例：*

```
def prune_old_screenshots(messages, keep_n=3, interval=25):
    """Replace older screenshots with text placeholders in batches.
    Only prunes when the total count exceeds keep_n + interval, so the
    message prefix stays byte-stable for `interval` turns between prunes."""
    image_positions = [
        (msg_idx, block_idx)
        for msg_idx, msg in enumerate(messages)
        for block_idx, block in enumerate(msg.get("content", []))
        if isinstance(block, dict) and block.get("type") == "image"
    ]
    if len(image_positions) <= keep_n + interval:
        return messages

    to_prune = image_positions[:-keep_n][-interval:]
    for msg_idx, block_idx in to_prune:
        messages[msg_idx]["content"][block_idx] = {
            "type": "text",
            "text": "[Image omitted]",
        }
    return messages
```

滚动缓冲区仍有一个真实的局限：缓冲区之外的一切都不复存在。原始指令、智能体已经尝试过什么、它在任务中的位置，都随被修剪的截图一起消失。对短任务（约 50 个动作以内）这没问题。对更长的任务，请把它与压缩（compaction）结合使用。

## **方法 2：基于 LLM 的压缩**

与其默默丢弃旧图像，不如在丢弃之前对完整对话做摘要。摘要保留了发生了什么、用户要求了什么、哪些已完成，以及从哪里继续。若干张最近的截图会与摘要一起保留，让智能体能看到它当前正在看的东西。

压缩与缓存感知的滚动缓冲区是互补的。逐轮使用滚动缓冲区来控制 token 增长；偶尔使用压缩来回收窗口的其余部分，同时不丢失更早的上下文。每次压缩事件在设计上就是一次缓存失效，所以你希望它很少发生，而不是每几轮就来一次。

### **摘要提示**

下面这个示例提示提供了一个脚手架，其中每个部分都针对一种特定的失败模式。这个提示必须捕获智能体继续任务所需的一切，使其无需重读原始对话，如下例所示：

```
COMPACT_PROMPT = """Your task is to create a detailed summary of this conversation that
will REPLACE the conversation history. The agent will continue working with only this
summary and a few recent screenshots as context.

CRITICAL: Preserve ALL user instructions verbatim. User instructions are the most
critical element. If they are lost, the agent will deviate from the task.

Before providing your summary, analyze the conversation in  tags:
1. Extract every user instruction, requirement, and constraint
2. Identify if this is a repeatable workflow (e.g., processing N items)
3. Chronologically trace what actions were taken and what happened

Your summary MUST include these sections:

1. USER INSTRUCTIONS:
   - Complete initial task definition (verbatim when possible)
   - ALL specific requirements and criteria
   - Every "DO NOT", "ALWAYS", "MUST" instruction
   - Any corrections or feedback that changed the approach

2. TASK TEMPLATE (if this is a repeatable workflow):
   - The pattern being repeated
   - Decision criteria for each iteration
   - Standard workflow steps
   - Example of one completed iteration

3. CONSTRAINTS AND RULES:
   - All user-specified rules and restrictions
   - Edge cases and exceptions discovered

4. ACTIONS TAKEN:
   - Pages visited and elements interacted with
   - Forms filled and buttons clicked

5. ERRORS AND FIXES:
   - What went wrong and how it was resolved
   - Approaches that failed (so they aren't retried)

6. PROGRESS TRACKING:
   - Items completed vs. remaining
   - Current position in the workflow

7. CURRENT STATE:
   - Current application, URL and domain (optional)
   - Important page state (logged in, form progress, etc.)

8. NEXT STEP:
   - Exactly what should be done next to continue
"""
```

在上面的提示中，**User Instructions**（用户指令）防止任务漂移：没有它们，智能体会在压缩后偏离任务。**Task Template**（任务模板）捕获可重复的模式，使智能体在压缩后能继续迭代，而不必从头重新推导工作流。**Constraints and Rules**（约束与规则）保留任务开始前设定或任务期间发现的限制与边界情况，使智能体不会违反它明知要遵守的既有规则。**Actions Taken**（已执行的动作）帮助追踪过去的进展。**Errors and Fixes**（错误与修复）防止重试已失败的方法（「我已经点过 Submit 了；在勾选条款复选框之前它是不管用的」）。**Progress Tracking**（进度追踪）防止重启和漏项。**Current State**（当前状态）与 **Next Step**（下一步）给出一个无歧义的恢复入口。

### **服务端压缩（beta）**

使用这个提示最简单的方式，是让 API 通过[服务端压缩（server-side compaction）](https://docs.anthropic.com/en/docs/build-with-claude/compaction)（beta）来处理压缩。把你自定义的摘要提示作为 `context_management` 中的 `instructions` 参数传入，当输入 token 超过触发阈值时，API 会自动进行摘要。`instructions` 参数会完全替换默认的摘要提示，因此模型遵循的正是上面那些部分。设置 `pause_after_compaction` 可以在压缩事件之间附加最近的若干条消息（包括截图）。

*使用 autocompaction 工具的示例：*

```
# Minimal — turn on autocompaction with API defaults
response = client.beta.messages.create(
    model="claude-opus-4-7",
    max_tokens=16000,
    betas=["compact-2026-01-12", "computer-use-2025-11-24"],
    context_management={"edits": [{"type": "compact_20260112"}]},
    messages=[...],
    tools=[...],
)

# Customized — set your own trigger threshold and summarization prompt
response = client.beta.messages.create(
    model="claude-opus-4-7",
    max_tokens=16000,
    betas=["compact-2026-01-12", "computer-use-2025-11-24"],
    context_management={
        "edits": [
            {
                "type": "compact_20260112",
                "trigger": {"type": "input_tokens", "value": 150_000},
                "instructions": COMPACT_PROMPT,
            }
        ]
    },
    messages=[...],
    tools=[...],
)
```

### **在客户端同步截断以与服务端一致**

当 API 执行了一次服务端压缩，它会在自己那一侧替换掉压缩前的内容，但你本地的 messages 数组仍然保存着完整历史。如果你在后续每一轮继续发送完整历史，你就要为服务端已经不需要的 token 付费，而且你的滚动缓冲区修剪器会作用在与服务端实际所见不同的消息切片上，这可能破坏你在上文精心维护的缓存稳定前缀。

修复方法是在客户端镜像服务端的截断，如下面的代码片段所示。当响应报告发生了压缩时，在下一轮之前从你的本地 messages 数组中丢弃压缩标记之前的所有内容。这让客户端与服务端的视图保持对齐，也让滚动缓冲区继续正常工作。

```
def truncate_to_last_compaction(messages, response):
    """If the server compacted on this turn, drop pre-compaction messages
    locally so the next turn's cache prefix matches what the server sees."""
    context_mgmt = getattr(response, "context_management", None)
    if not context_mgmt or not context_mgmt.get("applied_edits"):
        return messages

    compaction = next(
        (e for e in context_mgmt["applied_edits"] if e["type"] == "compact"),
        None,
    )
    if compaction is None:
        return messages

    keep_from = compaction["message_index_after_compaction"]
    return messages[keep_from:]
```

## **客户端压缩**

如果你使用的模型不支持服务端压缩，或者你想要完全控制，可以用同一个提示在客户端实现压缩。在每次 API 调用之后，从响应的 usage 字段检查总输入 token 数。当它超过某个阈值（例如上下文窗口的 90%）时，把对话连同 COMPACT_PROMPT 作为系统提示发送给一个摘要模型。用摘要加上若干张最近截图替换消息历史，然后继续智能体循环。

## **把一切组合起来**

对一个长时间运行的 computer use 智能体，一个不错的默认组合是这样的：

- 在稳定前缀上放一个缓存断点，在尾部工具结果上放三个，每轮清除并重新放置。
- 缓存感知的滚动缓冲区，keep_n = 3、interval = 25，分批把旧截图替换为占位符。
- 在约 150k 输入 token 时用自定义提示触发服务端压缩，外加一次客户端截断让两侧视图保持对齐。

有了这三层，一条典型的长周期 computer use 会话会在绝大多数轮次命中提示缓存，把总输入 token 控制在远低于上下文窗口的水平，并通过压缩事件保留足够的历史，使智能体不会丢失对任务的追踪。

# **改进计算机与浏览器使用的实验性设置**

下面这些模式是我们在自己的实现中一直在测试的技术，它们展现出前景，但还不足以成为普适推荐。每一项都以复杂度或成本换取对特定工作负载的潜在提升。我们在这里列出它们，供你在自己的工作流上尝试，但请预期本节的指导会快速演进。

## **批量工具（Batch tools）**

在更新后的参考实现中，我们在标准 computer 和 browser 工具之外暴露了两个工具：`computer_batch` 和 `browser_batch`。每个都接受一个子动作列表，并在单次工具调用中执行它们。例如，模型可以发出一个包含全部三个动作的 computer_batch 调用，而不必分别经历点击、打字、按键三轮。

它的吸引力在于效率：一个有 N 个机械动作的工作流只需要一次往返，而不是 N 次往返，这在长周期任务上能切实减少实际耗时（wall-clock time）和输出 token 开销。风险则是误差累积：如果动作 2 依赖动作 1 改变后的视觉状态，而动作 1 没点中，批次的其余部分就会基于过时的假设运行，智能体可能在从未看到真实状态截图的情况下漂移。

当子动作彼此自包含、不依赖彼此的视觉结果时（填写表单的多个字段、串联多个键盘快捷键、滚动并点击一个已知目标），我们推荐使用批量工具。在探索式导航、错误恢复序列，或任何「如果动作 1 失败我需要重新规划」是真实状态的场景中，我们会避免使用它们。

由于批量工具是你自己的自定义定义，它们与标准 computer 或 browser 工具可以干净地叠加。把两者都提供给模型，让它自己选择。

## **advisor 工具（beta）**

[advisor 工具](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool)把一个执行者模型与一个更高智能的顾问模型配对，执行者可以在生成过程中向顾问咨询战略性指导。执行者运行循环，当它遇到需要更深入推理的情况时，就调用顾问，收到一份计划或航向修正，然后继续。这一切发生在单次请求内的服务端，你这边没有额外的往返。

具体到 computer use，这一模式在长周期任务上最有用：大多数轮次是机械点击，但偶发的规划时刻（选择打开哪个标签页、从意外的模态对话框中恢复、决定是否放弃某个策略）能从 Opus 级推理中受益。你可以得到接近「advisor 单打独斗」的质量，而大部分 token 生成按执行者的费率计费。

*启用 advisor 工具的示例：*

```
response = client.beta.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=16000,
    betas=["advisor-tool-2026-03-01", "computer-use-2025-11-24"],
    tools=[
        {
            "type": "advisor_20260301",
            "name": "advisor",
            "model": "claude-opus-4-7",
        },
        {
            "type": "computer_20251124",
            "name": "computer",
            "display_width_px": 1280,
            "display_height_px": 720,
        },
    ],
    messages=[...],
)
```

advisor 工具有用的控制项包括：

- **`max_uses`：**限制每个请求的顾问调用次数。当你想约束最坏情况成本时很有用。
- **在你的执行框架中设置会话级上限：**顾问的每次咨询都按 Opus 4.7 费率计费，因此在非常长的会话中，你可能想在一定使用次数之后不再提供顾问。
- **顾问侧缓存：**在多次调用的对话中，缓存顾问的前缀在大约三次咨询之后就会开始划算。在参考实现中我们默认使用 5 分钟的临时缓存。

有两件不那么显眼的事值得知道：advisor 在没有工具、也没有上下文管理的情况下运行，所以它不能代你点击或浏览，只返回文本建议。而且由于执行者模型在长周期任务上并不总能记得 advisor 的存在，请看下文的「提醒轻推」一节。

## **清理孤立的 advisor 块**

当 advisor 工具被触发时，执行者会在返回的内容中发出一个 name 为 "advisor" 的 `server_tool_use` 块，随后是一个 `advisor_tool_result` 块。这些块和其他一切一起存在于你的 messages 数组中。

如果你之后把 advisor 工具从 tools 数组中移除——因为达到了会话级上限、更改了配置或切换了模型——那些先前的 `server_tool_use` / `advisor_tool_result` 块就成了孤块。API 会在下一个请求上返回 400，因为被引用的工具已不再声明。

修复办法是一个简单的发送前清理：每当某一轮禁用了 advisor，就遍历消息历史，剥离所有类型为 `server_tool_use`（且 name == "advisor"）以及 `advisor_tool_result` 的内容块。

*移除过期 advisor 块的示例：*

```
def strip_orphaned_advisor_blocks(messages):
    """Remove advisor server_tool_use / tool_result blocks from history.
    Call this before any request that doesn't include the advisor tool."""
    for msg in messages:
        content = msg.get("content")
        if not isinstance(content, list):
            continue
        msg["content"] = [
            block for block in content
            if not (
                isinstance(block, dict)
                and (
                    (block.get("type") == "server_tool_use"
                     and block.get("name") == "advisor")
                    or block.get("type") == "advisor_tool_result"
                )
            )
        ]
    return messages
```

## **周期性提醒轻推**

在长会话中，执行者模型可能忘记哪些工具可用，或者应该优先使用哪些工具。两种简短的提醒模式在我们的测试中颇有帮助：

**批量提醒。**如果你在标准工具之外暴露了 `computer_batch` 或 `browser_batch`，并观察到模型在适合批量的时候串联单动作调用，就在下一个工具结果后追加一条简短的系统级轻推：「记住，当多个顺序动作不依赖中间截图时，你可以用 `computer_batch` 在单次工具调用中组合它们。」目标是把模型拉回批量方向，而不是替它决定具体何时批量。

**advisor 提醒。**执行者很容易忘记 advisor 工具的存在，尤其是在很多轮都没有调用它的情况下。当会话超过约 20 轮而没有 advisor 调用时，追加一条简短提醒，说明 advisor 可用于规划或航向修正的时刻。在参考实现中我们使用 20 轮的节奏，并追加一行提示。

这两种轻推都是轻触式的上下文注入，而不是系统提示重写。每次追加只花费几十个输入 token。如果你的系统提示已经很长，或者你的缓存断点放置得很精确，就要权衡这点提升是否值得增加失效风险。

## **参考实现中的调试模式**

当某些东西行为异常，而你不确定问题出在你的执行框架、你的截图还是模型时，在开始添加日志之前，参考实现中有三个辅助工具值得先用：

- **轨迹查看器（streamlit run viewer/app.py）。**加载一条录制的轨迹，让你逐步查看智能体的每一轮：截图、思考、工具调用和每步用量。最适合在运行失败之后回答「模型实际看到了什么、决定了什么？」。
- **工具调试面板（uvicorn debug.server:app --reload）**。一个小型 Web UI，让你逐个试用每个工具：截图、捕获点击坐标、打字、滚动、缩放。用于确认你的采集管线和坐标缩放确实产生了你期望的结果。
- **定位实验场（uvicorn localize.server:app --reload --port 8001）**。上传任意图像并让模型指向一个目标。它会把预测坐标以显示分辨率和原生分辨率两种方式渲染回你的图像上。这是诊断一次点击失误究竟是缩放 bug、坐标缩放 bug 还是真正的模型错误的最快方式。当客户报告点击不准、而你想在隔离环境中复现失败时，它尤其有用。

构建一个能用的集成并不需要它们中的任何一个；它们是当默认反馈回路（记日志、重跑、眯着眼看对话记录）不够快时的调试辅助。

## **提升可靠性：教 Claude**

与其反复迭代文本提示直到 Claude 做对一个工作流，不如直接示范正确的行为。把你执行任务的过程录下来，在每一步捕获截图、动作，以及可选的语音旁白，然后在 Claude 执行同一工作流时把这段演示作为上下文回放给它。这段录制成为一份可复用的规格说明，Claude 会遵循它，并适应实时 UI 状态的差异。

我们在 Claude in Chrome 内部使用这一模式（在那里我们称之为「Teach Mode」），并在这里分享它，因为其底层方法对任何构建计算机使用或浏览器使用产品的人都广泛有用。它在两个方面有帮助：提升 Claude 基本能处理但偶尔出错的工作流的可靠性，以及解锁 Claude 仅凭文本提示根本无法完成的全新工作流。核心思想（捕获一段演示，再作为上下文回灌）实现起来很直接，并且能很好地同时适应浏览器和桌面环境。

### **核心概念：演示而非描述**

传统的提示工程要求用户用文字描述他们想要什么，然后在 AI 理解错误时反复迭代。这一模式把它倒转过来：用户执行示范任务，系统记录他们的动作、截图和（可选的）语音旁白。回放时，Claude 接收完整的演示作为上下文，并遵循同样的步骤序列，同时适应当前 UI 状态中的任何差异。

关键洞见在于：回放不是刻板重放。Claude 把演示当作指引，同时对实时环境进行推理。如果一个按钮移动了位置或一个菜单被重新组织，Claude 可以在当前 UI 中找到等价的元素，而不是盲目地在录制的坐标处点击。

### **数据模型**

基本单元是「工作流步骤（workflow step）」，即录制期间捕获的一个单一动作。每个步骤打包了做了什么、发生在哪里，以及屏幕当时的样子：

```
from dataclasses import dataclass, field
from typing import Literal, Optional

@dataclass
class WorkflowStep:
    action: Literal["click", "type", "navigate", "scroll", "select"]
    description: str                         # Human-readable, e.g. "Click the Submit button"
    timestamp: float
    selector: Optional[str] = None           # CSS selector or XPath
    coordinates: Optional[dict] = None       # {"x": int, "y": int}
    url: Optional[str] = None
    screenshot: Optional[str] = None         # Base64-encoded screenshot
    viewport_dimensions: Optional[dict] = None  # {"width": int, "height": int}
    speech_transcript: Optional[str] = None  # Voice narration, if captured
    value: Optional[str] = None              # For type actions

@dataclass
class SavedWorkflow:
    id: str
    name: str                                # e.g. "Submit expense report"
    steps: list[WorkflowStep] = field(default_factory=list)
    description: Optional[str] = None        # AI-generated summary of the workflow
    start_url: Optional[str] = None
    created_at: float = 0.0
    usage_count: int = 0
```

同时捕获选择器（selector）和坐标是有意为之：选择器对布局变化更稳健，而坐标提供了视觉兜底，当选择器失效时 Claude 可以退而使用它。存储视口尺寸是为了让坐标在回放环境与录制环境不同时能够被缩放。

### **录制：要捕获什么**

至少要捕获点击事件、键盘输入、导航变化，以及每个动作处的截图。对每次点击，生成一段人类可读的描述（来自 aria-label、文本内容，或通过一次快速的 Claude 调用），并在截图上的点击位置标注一个可视标记：

```
def on_click(event):
    step = WorkflowStep(
        action="click",
        selector=generate_selector(event.target),
        coordinates={"x": event.client_x, "y": event.client_y},
        url=current_url(),
        description=generate_description(event.target),
        timestamp=now(),
        viewport_dimensions=get_viewport_size(),
    )
    # Annotate screenshot with a circle at the click position
    screenshot = capture_screenshot()
    step.screenshot = annotate_with_circle(screenshot, event.client_x, event.client_y)
    workflow_steps.append(step)
```

这个标注（点击位置上的一个彩色圆圈）有两个目的：它帮助用户确认录制捕捉到了正确的元素；在回放时，它向 Claude 精确显示动作发生的位置。你的回放提示应当说明：这些标记是录制的产物，不是实时 UI 的一部分。

### **回放：构建提示**

这是最重要的部分。当用户触发一个已保存的工作流时，你构建一条发给 Claude 的消息，包含三样东西：用户的意图、一个解释演示格式的上下文块，以及录制下来的截图。

上下文块告诉 Claude 如何解读带标注的截图，以及当实时 UI 与录制不同时如何调整：

```
def generate_playback_context(steps: list[WorkflowStep]) -> str:
    steps_description = "\n".join(
        f"Step {i+1}: {step.description}"
        for i, step in enumerate(steps)
    )

    return f"""<demonstration_context>
The user has recorded a demonstration showing how to perform this task.

RECORDED STEPS:
{steps_description}

ABOUT THE SCREENSHOTS:
- Each screenshot shows the screen state when an action was taken
- BLUE CIRCLES mark where the user clicked — these are recording annotations
- The blue highlighting is NOT part of the actual interface
- Your own screenshots will NOT have these markers

HOW TO USE THIS DEMONSTRATION:
1. Review all steps and screenshots to understand the complete workflow
2. Take your own screenshot to see the CURRENT page state
3. The blue highlights show which element to interact with — find it in your current view
4. Follow the same sequence of actions, adapting to any differences
5. If the UI has changed significantly, use judgment to find equivalent elements
</demonstration_context>"""
```

然后把完整消息组装起来：用户的提示、上下文块，以及每个步骤的截图（作为图像）：

```
import anthropic

client = anthropic.Anthropic()

content = [
    {"type": "text", "text": user_prompt},
    {"type": "text", "text": generate_playback_context(workflow.steps)},
]

for i, step in enumerate(workflow.steps):
    if step.screenshot:
        content.append({"type": "text", "text": f"[Step {i+1}: {step.description}]"})
        content.append({
            "type": "image",
            "source": {"type": "base64", "media_type": "image/jpeg", "data": step.screenshot},
        })

response = client.beta.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=4096,
    betas=["computer-use-2025-11-24"],
    messages=[{"role": "user", "content": content}],
    tools=[{
        "type": "computer_20251124",
        "name": "computer",
        "display_width_px": 1280,
        "display_height_px": 720,
    }],
)
```

### **回放模式**

并非每个工作流都需要以同样的严格程度遵循录制的演示。有些工作流太长，消耗大量输入 token，最终拖慢延迟并增加成本。可以考虑支持一个严格度（strictness）参数，把它包含在上下文提示中：

**严格（Strict）：**逐步精确遵循；如果 UI 变化过大就停下并报告。适用于确切顺序至关重要的合规敏感工作流。

**自适应（Adaptive）：**把演示当作指引，但适应 UI 变化。这是对大多数用例最好的默认值——它能优雅地处理轻微的布局偏移、更新过的按钮文案和重组过的菜单。

**目标导向（Goal-oriented）：**聚焦最终结果；把录制步骤当作提示而非指令。适用于 UI 频繁变化但目标不变的情况。用一个模型对录制的演示做摘要（策略与下一节描述的类似），然后把该摘要传给 computer use 模型。

### **示例：端到端的报销单工作流**

下面是一个已保存工作流在实践中的样子。该工作流捕获五个步骤：导航到报销表单、选择报销类型、从下拉菜单中选择「Travel」、输入金额、点击 Submit。

```
expense_workflow = SavedWorkflow(
    id="wf_abc123",
    name="Submit Expense Report",
    start_url="https://expenses.company.com/new",
    steps=[
        WorkflowStep(
            action="navigate",
            url="https://expenses.company.com/new",
            description="Navigate to new expense form",
            timestamp=1700000000,
        ),
        WorkflowStep(
            action="click",
            selector="#expense-type-dropdown",
            coordinates={"x": 400, "y": 200},
            description="Click on expense type dropdown",
            timestamp=1700000001,
        ),
        WorkflowStep(
            action="click",
            selector="[data-value='travel']",
            coordinates={"x": 400, "y": 280},
            description='Select "Travel" expense type',
            timestamp=1700000002,
        ),
        WorkflowStep(
            action="type",
            selector="#amount-input",
            value="150.00",
            description="Enter expense amount",
            timestamp=1700000003,
        ),
        WorkflowStep(
            action="click",
            selector="#submit-expense-btn",
            coordinates={"x": 1150, "y": 420},
            description="Click the Submit button",
            speech_transcript="Now I'll click submit to send the report for approval",
            timestamp=1700000004,
        ),
    ],
)
```

当用户之后说「为团队午餐提交我的报销单（85.50 美元）」时，回放服务会构建一个包含演示上下文、全部五张带标注截图以及新请求中具体取值的提示。Claude 能确切看到该点哪里、该遵循什么顺序，并调整金额与描述以匹配当前任务。如果你的工作流因输入 token 数量太多而不适合这种方法，可以考虑先对工作流做压缩，再把它作为示例使用。上下文管理的技巧请参见上一节。

# **开始使用计算机与浏览器使用**

这些实践反映了我们当前对「什么能让计算机使用集成在生产环境中可靠运行」的最佳理解。它们适用于 Claude 4.6 模型家族和 Opus 4.7，并将随着新模型与新技术的出现而更新。

随着你的集成走向成熟，最重要的模式将取决于你的具体环境、目标应用和可靠性要求。

*从*[**computer use 文档**](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)*开始上手，查看这些最佳实践的全新*[**演示实现**](https://github.com/anthropics/claude-quickstarts/tree/main/computer-use-best-practices)*，或者重读*[**最初的 computer use 研究文章**](https://www.anthropic.com/news/developing-computer-use)*，了解这些能力是如何构建的以及它们的发展方向。*

*致谢：本文及配套演示由 Lucas Gonzalez 和 Luca Weihs 撰写。作者感谢 Molly Vorwerck、Javier Rando、Maya Nielan、Gabe Mulley 和 Brigit Brown 作出的贡献。*

FAQ（常见问题）
