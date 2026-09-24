---
title: "inclusionAI/Ming-Image"
title_en: "inclusionAI/Ming-Image"
source: https://github.com/inclusionAI/Ming-Image/blob/main/README.md
crawled: 2026-09-23
translated: 2026-09-23
---

# Ming Image 0.1 Design

| 模型 | 链接 |
| --- | --- |
| **Design** | [🧩 ModelScope](https://www.modelscope.cn/models/inclusionAI/Ming-Image-0.1-Design) · [🤗 Hugging Face](https://huggingface.co/inclusionAI/Ming-Image-0.1-Design) · [🖥️ 演示](https://huggingface.co/spaces/hugging-apps/ming-image-0-1-design-demo) |
| **Layer** | [🧩 ModelScope](https://www.modelscope.cn/models/inclusionAI/Ming-Image-0.1-Design-Layer) · [🤗 Hugging Face](https://huggingface.co/inclusionAI/Ming-Image-0.1-Design-Layer) · [🖥️ 演示](https://huggingface.co/spaces/Xiaolong-Wang/Ming-Image-0.1-Design-Layer) |

[📄 博客](https://mp.weixin.qq.com/s/VGdtxfM8kbHIQJw50VD_Sw) · [🎨 设计技能](https://github.com/inclusionAI/ling-cookbook/tree/main/resources/recommended-skills/ling-ui-design) · [📊 PPT 技能](https://github.com/inclusionAI/ling-cookbook/tree/main/resources/recommended-skills/image-to-editable-ppt)

Ming-Image-0.1-Design 是一个面向视觉设计生成与可编辑图层分解的开源系列。

该系列包含两个 6B 参数模型：

- [Ming-Image-0.1-Design](https://huggingface.co/inclusionAI/Ming-Image-0.1-Design)
  可为 UI、信息图、海报以及富文本构图生成完整的视觉设计。
- [Ming-Image-0.1-Design-Layer](https://huggingface.co/inclusionAI/Ming-Image-0.1-Design-Layer)
  可将扁平化的设计图像分解为可独立编辑的透明图层。

![Ming-Image-0.1-Design on the Artificial Analysis UI/UX Design leaderboard](assets/ming-image-design-ui-ux-leaderboard.webp)

## 效果展示

### 文生图

![Text-to-image showcase](assets/model_cards/design_showcase.webp)

### 透明背景文生图

![Transparent-background text-to-image showcase](assets/model_cards/design_transparency_showcase.webp)

### 图层分解

![Six-layer card decomposition showcase](assets/model_cards/layer_showcase.webp)

![Layer-decomposition gallery](assets/model_cards/layer_gallery.webp)

![Layer-decomposition results on the Crello test set](assets/model_cards/layer_performance.webp)

## 配合技能使用

- [Ling UI Design](https://github.com/inclusionAI/ling-cookbook/blob/main/resources/recommended-skills/ling-ui-design/README.md) 利用生成的视觉参考和图层分解，帮助智能体根据提示词或截图构建 UI 代码并进行视觉检查。
- [Image to Editable PPT](https://github.com/inclusionAI/ling-cookbook/blob/main/resources/recommended-skills/image-to-editable-ppt/README.md) 帮助智能体把一张生成的页面或幻灯片图像重制为可编辑的 PowerPoint 幻灯片，文字和简单形状都会转换为原生元素。

这些是相互独立的智能体工作流；请按照各技能自身的安装说明配置其依赖项和兼容的模型服务。

## 环境要求

- Python 3.10 或更新版本；
- 支持 CUDA 的 PyTorch，用于完整的模型推理；
- 一个本地检查点目录，或一个 Hugging Face Hub 仓库 ID。

在干净的环境中安装运行时依赖：

```bash
pip install -r requirements.txt
```

`flash_attention_2` 为可选项。CLI 默认使用 `eager` 注意力，因为 LLM 仅实现了
eager 和 FlashAttention 2 两类注意力；扩散 transformer 内部则始终使用 PyTorch
SDPA。选择 `--attn-implementation sdpa` 会在加载时直接报错拒绝（fails
closed）。

## 推理

`--model` 参数接受本地目录或 HF Hub 仓库 ID。Hub 模型会在加载任何组件之前
被解析为一个不可变的本地快照。使用 `--revision` 可固定到某个分支、标签或
提交。示例中使用的是已发布的 Hub ID；离线推理时请将其替换为本地检查点
目录。

采样默认值和公开的分辨率档位因任务而异：

| 任务 | 步数 | CFG | 分辨率档位 | 默认 / 推荐 |
| --- | ---: | ---: | --- | ---: |
| 文生图 | 12 | 1.0 | 1024, 2048 | 2048 |
| 图层分解 | 12 | 2.0 | 512, 1024 | 1024 |

传入 `--steps` 或 `--cfg` 可显式覆盖对应数值。`--resolution` 为可选。所给
的正整数会吸附到所选任务支持的最近档位；距离相同时取较小的档位。想要更快
的图层分解，可显式传入 `--resolution 512`；使用 1024 可获得推荐的输出
质量。文生图输出为所选档位下的正方形图像。图层分解在保留参考图像纵横比的
同时，从实际生效的 1024 或 512 档位中选择一个预定义的工作尺寸。

默认且经过验证的最低部署配置为**一块显存至少 80 GiB 的 GPU**，以 BF16
运行。该配置可端到端跑通两个模型系列，下文所有演示默认使用该配置。

```bash
export CUDA_VISIBLE_DEVICES=0
```

安装了 FlashAttention 2 时，可选择 `--attn-implementation
flash_attention_2`；可移植 CLI 的默认值仍为 `eager`。

对这两种任务，`--prompt` 均接受原始文本或提示词文件路径。使用
`--validate-only` 可在不加载模型权重的情况下检查检查点契约与任务组合：

```bash
python infer.py --model inclusionAI/Ming-Image-0.1-Design --task text-to-image \
  --prompt "A red circle on a white background" --validate-only
```

### 文生图演示

这个演示会渲染同一座固定的小屋在春、夏、秋、冬四季中的样子。它使用的是
[这份结构化 JSON 提示词](assets/t2i_four_seasons_cabin_prompt.json)，而不在
README 中重复这段很长的输入。

```bash
python infer.py \
  --model inclusionAI/Ming-Image-0.1-Design \
  --task text-to-image \
  --prompt assets/t2i_four_seasons_cabin_prompt.json \
  --attn-implementation flash_attention_2 \
  --resolution 2048 \
  --output-dir outputs/t2i
```

### 文生图提示词改写

一个遵循指令的 VLM 可以把简短的说明转化为精确、按布局结构组织的 JSON
描述：Figma 风格的图层按从后到前的顺序排列，带有精确坐标、层级关系和颜色
规范，并且每个渲染出的字符串都逐字加引号、恰好只归属一次。与图层分解不
同，文生图改写器描述的是完整的 1:1 画布。

这一改写是 `infer.py` *之外*的预处理步骤。提示词增强（PE）可以使用
`Ling-3.0-flash-VL` 或 `qwen3.8-27B`；先运行它，再将其输出以原始文本或
资源文件的形式传给 `--prompt`。

已发布的系统提示词存放在
[`assets/t2i_rewriter_system_prompt.txt`](assets/t2i_rewriter_system_prompt.txt)
中，全文复现如下：

```text
You are a senior visual designer and image-prompt engineer. Expand the user's request into one precise, high-resolution Figma-style caption. Return only one JSON object.

Use exactly two top-level keys. `canvas_settings` contains exactly `aspect_ratio`, `ambient_lighting`, and `image_style`. `layers` lists visible groups from background to topmost overlay. Every layer contains exactly `description`, `coordinates`, `hierarchy_and_relation`, and `color_specs`; `color_specs` is an array of hex colors.

`coordinates` MUST be one string, never an object or array, in exactly this form: `"cx: 0.500, cy: 0.500, w: 1.000, h: 1.000"`. Values are normalized; each bbox encloses its complete owned object and stays inside the canvas.

A layer is one selectable visible semantic group: background, full person, coherent object, panel, card, row, or text block. Prefer the fewest groups that preserve the layout. Keep people and objects intact. Never create invisible parents, guides, placeholders, empty layers, duplicate summaries, or multiple owners for one element.

Preserve every user-supplied rendered string character-for-character and as one contiguous string. Unless multiple visible copies are requested, it must occur exactly once across all `description` fields and zero times in `hierarchy_and_relation`. Quote it only where describing its visible rendering; refer to the related subject elsewhere with unquoted semantic wording. Enumerate intended copy, invent extra copy sparingly, and never hide content behind "other text", "remaining labels", or "etc."

Describe concrete composition, typography, materials, texture, lighting, pose, and camera treatment without literary filler. Use `hierarchy_and_relation` only for ownership, alignment, containment, stacking, and occlusion.

Infer structured layouts first. Use one complete layer per card and state its row and column. A compact secondary table may be one layer only if every header and cell is listed; otherwise use a visible shared frame when present, one complete header, and one complete layer per body row, binding values to columns and stating blanks. Enumerate sequences, schedules, spans, gaps, and vacant tracks in visual order. Do not mistake ordinary alignment for a table.

Silently verify schema, string coordinates, Z-order, exact-text counts, geometry, bbox validity, and completeness.
```

### 透明背景生成技巧

要生成带 alpha 通道的图像，请从下列固定短语中恰好选择一条，并将其放在
提示词的开头。不要组合多个前缀。

- `带透明通道，4通道RGBA图像`
- `透明背景，alpha通道，无底图`
- `抠图素材，背景alpha=0`
- `孤立主体，透明PNG图层`
- `不要白底，不要棋盘格，只要透明通道`
- `RGBA, 4-channel, transparent background`
- `isolated subject, alpha matte, no background`
- `cutout PNG, alpha=0 outside the object`
- `transparent canvas, not white, not checkerboard`
- `production RGBA layer for compositing`

### 图层分解演示

这个示例会把扁平化的卡片设计拆分为六个透明 RGBA 图层。参见
[源输入图像](assets/layer_samples/card_making_input.png)和
[确切的六层规格说明](assets/layer_samples/card_making_prompt.txt)。

```bash
python infer.py \
  --model inclusionAI/Ming-Image-0.1-Design-Layer \
  --task layer-decompose \
  --input-image assets/layer_samples/card_making_input.png \
  --prompt assets/layer_samples/card_making_prompt.txt \
  --attn-implementation flash_attention_2 \
  --resolution 1024 \
  --output-dir outputs/layers
```

图层数量从提示词中的 “Decompose this image into N layers” 或 “Number of
layers: N” 规格说明解析得到。当省略 `--prompt` 时，`--num-layers N` 会生成
默认请求 `Decompose this image into N layers.`

图层模型会返回所请求的各个图层，外加一张位于最前面的合成/全画布图像。
CLI 会跳过这第一张图像，并将各独立图层保存为 `layer_01.png`、
`layer_02.png` 等。

### 图层分解提示词改写

图层分解由显式的逐层规格说明驱动，而不是自由格式的描述。参考流水线会先
运行一个提示词增强器：一个遵循指令的 VLM 把用户粗糙的图层方案改写为精确
的分解——每层给出具体的颜色/位置/形状，真实文字逐字引用并置于自己的前置
图层，承载文字的卡片/面板/徽章/横幅作为紧随文字之后的独立图层，主体作为
独立图层，背景放在最后并吸收其余的衬托物与表面。

这一改写同样是 `infer.py` *之外的*预处理步骤：先运行增强器，再将其输出
传给 `--prompt`（以原始文本或资源文件的形式）。增强器的输出正是本 CLI 所
解析的格式——它会重新生成 “Decompose this image into N layers” /
“Number of layers: N” 规格说明，因此图层数量会经由上文所述的同一条
`--prompt` 解析路径传入。

提示词增强（PE）可使用 `Ling-3.0-flash-VL` 或 `qwen3.8-27B` 作为遵循指令
的 VLM。下面的引导提示词是已发布流水线的一部分，此处保留以便复现：

```text
GUIDED_PROMPT = """You are a graphic-design layer-decomposition expert. You are given ONE flattened design image and a ROUGH layer plan from the user. Rewrite the rough plan into a precise layer decomposition that matches the image.

User's rough layer plan:
{spec}

Guidelines:
- Follow the user's plan EXACTLY: use the same number of layers and the same per-layer role/meaning, in the same order. Layer 1 is the FRONT-most (topmost); the last layer is the background/environment. Stacking the layers back-to-front must reproduce the image.
- For each layer, write a concrete one-or-two-sentence description grounded in the image: real colors, positions and shapes.
- TEXT goes in the front layer(s); quote any real text VERBATIM in double quotes and keep its original language (do not translate).
- A text-supporting CARD / PANEL / BADGE / BANNER is its OWN layer directly behind the text — do not merge it into the text layer or into the background.
- The MAIN SUBJECT (hero product/photo/illustration) is its own layer.
- The BACKGROUND/ENVIRONMENT is the LAST layer and ABSORBS supporting props and surfaces under the subject (tables, boards, plates, floors, shadows, gradients, patterns) — these are NOT separate layers.

Write the description DIRECTLY about the content; do NOT mention "image" or narrate your reasoning. Output EXACTLY in this format and NOTHING else (N = the number of layers in the user's plan):

Decompose this image into N layers with the following specifications:

Number of layers: N
Layer 1: <front-most layer>
Layer 2: <...>
Layer N: <background/environment layer>"""
```

## 部署

我们推荐使用以下推理框架来提供模型服务：

- vLLM-Omni：参见[配方](https://github.com/vllm-project/vllm-omni/blob/main/recipes/inclusionAI/Ming-Image.md)
  和[安装指南](https://docs.vllm.ai/projects/vllm-omni/en/latest/getting_started/quickstart/)。

## 验证

快速契约测试不需要模型权重：

```bash
python -m unittest -v tests.test_inference_profile
python -m unittest -v tests.test_padding
```

完整推理是一项 GPU 冒烟测试，需要两个检查点系列。至少应使用固定随机种子
验证四季小屋文生图用例和六层卡片制作分解用例。冒烟测试默认采用上文所示的
单 GPU 部署与 FlashAttention 2 配置：

```bash
export CUDA_VISIBLE_DEVICES=0
export MING_GENERATION_MODEL=inclusionAI/Ming-Image-0.1-Design
export MING_LAYER_MODEL=inclusionAI/Ming-Image-0.1-Design-Layer
export MING_SMOKE_OUTPUT_DIR=/path/to/persistent/results
python -m unittest -v tests.test_inference_smoke.InferenceSmokeTest.test_two_step_showcase_smoke
```

## 检查点契约

每个检查点都在 `transformer/config.json` 中声明其运行时能力：

| 系列 | `alignment_padding_mode` | `multi_frame_output` |
| --- | --- | ---: |
| 文生图 | `"zero_masked"` | `false` |
| 图层分解 | `"learned"` | `true` |

这两个字段必须同时存在，且 VAE 组件必须是 4 通道的
`AutoencoderKLQwenImage`（argmax 参考编码）。缺失、不完整或未知的取值都会
被视为错误；加载器绝不会从目录名推断填充行为，也不会静默回退到其他模式。

早于组件元数据出现的旧版软件包，在兼容期内严格从根目录的
`inference_profile.json` 加载；当两者同时存在时，以组件配置为准，与旧文件
的任何不一致都会被视为错误。
