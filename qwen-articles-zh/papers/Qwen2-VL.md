---
title: "Qwen2-VL：提升视觉语言模型的高分辨率世界感知能力"
title_en: "Qwen2-VL: Enhancing Vision-Language Model's Perception of the World at Any Resolution"
arxiv: 2409.12191
date: 2024-09-18
source: https://arxiv.org/abs/2409.12191
crawled: 2026-09-22
translated: 2026-09-22
---

# Qwen2-VL：提升视觉语言模型的高分辨率世界感知能力

> 原文：[Qwen2-VL](https://arxiv.org/abs/2409.12191) · Qwen 团队 arXiv

Peng Wang* Shuai Bai* Sinan Tan* Shijie Wang* Zhihao Fan*
  
Jinze Bai*
Keqin Chen Xuejing Liu Jialin Wang Wenbin Ge Yang Fan Kai Dang Mengfei Du
Xuancheng Ren Rui Men Dayiheng Liu Chang Zhou Jingren Zhou
  
Junyang Lin
Qwen 团队  阿里巴巴集团

###### 摘要

我们提出 Qwen2-VL 系列——对既有 Qwen-VL 模型的一次先进升级，它重新定义了视觉处理中传统的预定分辨率（predetermined-resolution）方法。Qwen2-VL 引入原生动态分辨率（Naive Dynamic Resolution）机制，使模型能够将不同分辨率的图像动态处理为不同数量的视觉 token。这一方法让模型得以生成更高效、更准确的视觉表示，与人类的感知过程紧密契合。该模型还集成了多模态旋转位置编码（Multimodal Rotary Position Embedding，M-RoPE），促进文本、图像与视频间位置信息的有效融合。我们采用统一范式处理图像与视频，增强了模型的视觉感知能力。为探索大型多模态模型的潜力，Qwen2-VL 研究了大型视觉语言模型（LVLM）的缩放定律。通过同时扩展模型规模——提供 2B、8B 与 72B 参数版本——以及训练数据量，Qwen2-VL 系列取得了极具竞争力的性能。值得注意的是，Qwen2-VL-72B 模型在各种多模态基准上取得了与 GPT-4o 和 Claude3.5-Sonnet 等领先模型相当的结果，胜过其他通用模型。代码可在 <https://github.com/QwenLM/Qwen2-VL> 获取。

††脚注：∗同等核心贡献，†通讯作者

## 引言

在人工智能领域，大型视觉语言模型（LVLM）代表着一次重大飞跃，它们在传统大语言模型强大的文本处理能力之上发展而来。这些先进的模型如今具备了解释与分析更广泛数据的能力，包括图像、音频与视频。这种能力的扩展使 LVLM 成为解决各种现实世界挑战不可或缺的工具。因其将广泛而复杂的知识凝聚为可用表示的独特能力而受到认可，LVLM 正为更全面的认知系统铺平道路。通过整合多样化的数据形式，LVLM 旨在更贴近地模拟人类感知环境并与环境交互的细腻方式。这使这些模型能够更准确地刻画我们与环境互动及感知环境的方式。

大型视觉语言模型（LVLM）的最新进展（[Li et al., 2023c](#bib.bib48)；[Liu et al., 2023b](#bib.bib54)；[Dai et al., 2023](#bib.bib22)；[Zhu et al., 2023](#bib.bib120)；[Huang et al., 2023a](#bib.bib34)；[Bai et al., 2023b](#bib.bib11)；[Liu et al., 2023a](#bib.bib53)；[Wang et al., 2023b](#bib.bib99)；[OpenAI., 2023](#bib.bib71)；[Team et al., 2023](#bib.bib93)）在短时间内带来了显著改进。这些模型（[OpenAI, 2023](#bib.bib70)；[Touvron et al., 2023a](#bib.bib94)；[Touvron et al., 2023b](#bib.bib95)；[Chiang et al., 2023](#bib.bib21)；[Bai et al., 2023a](#bib.bib10)）通常遵循「视觉编码器 → 跨模态连接器 → LLM」的通用方法。这一设置，加上以下一 token 预测作为主要训练方法以及高质量数据集的可得性（[Liu et al., 2023a](#bib.bib53)；[Zhang et al., 2023](#bib.bib118)；[Chen et al., 2023b](#bib.bib14)；[Li et al., 2023b](#bib.bib47)），推动了大部分进展。其他因素也在增强 LVLM 更有效处理复杂视觉与文本信息的能力方面发挥了关键作用，例如更大的模型架构（[Alayrac et al., 2022](#bib.bib1)）、更高分辨率的图像（[Li et al., 2023a](#bib.bib46)；[Li et al., 2023d](#bib.bib51)），以及专家混合模型（MoE）（[Wang et al., 2023b](#bib.bib99)；[Ye et al., 2023b](#bib.bib108)）、模型集成（[Lin et al., 2023](#bib.bib52)）、更精巧的跨模态连接器（[Ye et al., 2023a](#bib.bib107)）等先进技术。

然而，当前的大型视觉语言模型（LVLM）通常受限于固定的图像输入尺寸。标准 LVLM 将输入图像编码为固定分辨率（如 224×224），通常通过对图像下采样或上采样（[Zhu et al., 2023](#bib.bib120)；[Huang et al., 2023a](#bib.bib34)），或采用「先缩放再填充」（scale-then-padding）的方法（[Liu et al., 2023b](#bib.bib54)；[Liu et al., 2023a](#bib.bib53)）。尽管这种一刀切的策略能以一致分辨率处理图像，但也限制了模型捕捉不同尺度信息的能力，尤其会导致高分辨率图像中细节信息的显著丢失。因此，此类模型无法像人类视觉那样以对尺度和细节的同样敏感度来感知视觉信息。

此外，大多数 LVLM 依赖静态、冻结的 CLIP 风格（[Radford et al., 2021](#bib.bib78)）视觉编码器，这引发了此类预训练模型产生的视觉表示是否足够的疑问，尤其是对复杂推理任务以及处理图像中错综复杂的细节而言。近期工作（[Bai et al., 2023b](#bib.bib11)；[Ye et al., 2023a](#bib.bib107)）尝试通过在 LVLM 训练过程中微调视觉 Transformer（ViT）来解决这些局限，并已被证明可产生更好的结果。为进一步增强模型对不同分辨率的适应能力，我们在 LVLM 训练过程中引入动态分辨率训练。具体而言，我们在 ViT 中采用二维旋转位置编码（2D Rotary Position Embedding，RoPE），从而使模型能够更好地捕捉不同空间尺度上的信息。

![Refer to caption](2409.12191v2/images/qwen2_vl_example.jpg)

图 1：Qwen2-VL 的能力：多语言图像文本理解、代码/数学推理、视频分析、实时对话、智能体潜力等。详见附录。

至于视频内容——本质上是帧的序列——许多现有模型仍将其视为一种独立的模态。然而，理解以视频形式呈现的现实世界的动态本质，对于旨在把握现实世界复杂性的模型至关重要。与本质上是一维的文本不同，现实世界环境存在于三个维度之中。当前模型使用一维位置编码，显著限制了它们有效建模三维空间与时间动态的能力。为弥合这一差距，我们开发了多模态旋转位置编码（M-RoPE），它采用相互独立的分量来表示时间与空间信息。这使模型能够自然地理解动态内容（如视频或流式数据），提升其理解世界并与世界交互的能力。

此外，与大语言模型（LLM）的规模化相比，当前 LVLM 在探索训练数据与模型参数规模化的影响方面仍处于早期阶段。LVLM 缩放定律的探索——即模型与数据规模的增长如何影响性能——仍是一个开放且富有前景的研究领域。

在本工作中，我们介绍 Qwen 家族大型视觉语言模型的最新成员：Qwen2-VL 系列，它包含三个开放权重模型，总参数量分别为 20 亿、80 亿与 720 亿。如图 1 所示，Qwen2-VL 的关键进展包括：

- —

  在各种分辨率与宽高比下的最先进理解能力：Qwen2-VL 在视觉基准上取得领先性能，包括 DocVQA、InfoVQA、RealWorldQA、MTVQA、MathVista 等。
- —

  对长时视频（20 分钟以上）的理解：Qwen2-VL 能够理解超过 20 分钟的视频，增强其执行高质量视频问答、对话、内容创作等任务的能力。
- —

  面向设备操作的稳健智能体能力：凭借先进的推理与决策能力，Qwen2-VL 可以与手机、机器人等设备集成，基于视觉输入与文本指令实现自主操作。
- —

  多语言支持：为服务全球用户，除英文与中文外，Qwen2-VL 现在还支持图像内的多语言上下文理解，包括大多数欧洲语言、日语、韩语、阿拉伯语、越南语等。

表 1：Qwen2-VL 的模型描述。

|  |  |  |  |
| --- | --- | --- | --- |
| 模型名称 | 视觉编码器 | LLM | 模型描述 |
| Qwen2-VL-2B | 675M | 1.5B | 最高效的模型，专为端侧运行而设计。在资源有限的情况下，可为大多数场景提供足够的性能。 |
| Qwen2-VL-7B | 675M | 7.6B | 在成本上做了性能优化的模型，在文本识别与视频理解能力上显著升级。它在广泛的视觉任务上均有出色表现。 |
| Qwen2-VL-72B | 675M | 72B | 能力最强的模型，在视觉推理、指令遵循、决策与智能体能力上进一步提升。它在大多数复杂任务上都能带来最佳性能。 |

![Refer to caption](2409.12191v2/images/qwen2_vl_frame.jpg)

图 2：无论图像的清晰度、分辨率或极端宽高比如何，Qwen2-VL 都能准确识别并理解图像中的内容。

## 方法

Qwen2-VL 系列由 3 种规模的模型组成，即 Qwen2-VL-2B、Qwen2-VL-7B 与 Qwen2-VL-72B。表 1 列出了超参数与重要信息。值得注意的是，Qwen2-VL 在不同规模的 LLM 中均采用 675M 参数的 ViT，确保 ViT 的计算负载不随 LLM 的规模而变化。

### 2.1 模型架构

图 2 展示了 Qwen2-VL 的整体结构。我们保留了 Qwen-VL（[Bai et al., 2023b](#bib.bib11)）的框架，它集成了视觉编码器与语言模型。为适配不同规模，我们实现了一个约 6.75 亿参数的视觉 Transformer（ViT）（[Dosovitskiy et al., 2021](#bib.bib26)），擅长处理图像与视频输入。在语言处理方面，我们选择了更强大的 Qwen2（[Yang et al., 2024](#bib.bib104)）系列语言模型。为进一步增强模型有效感知与理解视频中视觉信息的能力，我们引入了若干关键升级：

##### 原生动态分辨率（Naive Dynamic Resolution）

![Refer to caption](2409.12191v2/images/mrope.png)

图 3：M-RoPE 示意图。通过将旋转编码分解为时间、高度与宽度三个分量，M-RoPE 可以在 LLM 中显式建模文本、图像与视频的位置信息。

Qwen2-VL 的一项关键架构改进是引入了原生动态分辨率支持（[Dehghani et al., 2024](#bib.bib25)）。与 Qwen-VL 不同，Qwen2-VL 现在可以处理任意分辨率的图像，并将其动态转换为数量可变的视觉 token。¹
¹ 该技术此前已在内部迭代版本 Qwen-VL Plus 与 Qwen-VL MAX 中实现。我们在 Qwen2-VL 中对其做了进一步升级。
为支持这一特性，我们修改了 ViT：移除原有的绝对位置编码，并引入 2D-RoPE（[Su et al., 2024](#bib.bib91)；[Su, 2021](#bib.bib89)）以捕捉图像的二维位置信息。在推理阶段，不同分辨率的图像被打包进单一序列，并对打包长度加以控制以限制 GPU 显存占用。此外，为减少每张图像的视觉 token 数量，在 ViT 之后采用一个简单的 MLP 层将相邻的 $2\times 2$ 个 token 压缩为单个 token，并在压缩后的视觉 token 首尾分别放置特殊 token ¡—vision_start—¿ 与 ¡—vision_end—¿。因此，一张 $224\times 224$ 分辨率、经 patch_size=14 的 ViT 编码的图像，在进入 LLM 之前会被压缩为 66 个 token。

##### 多模态旋转位置编码（M-RoPE）

另一项关键架构增强是多模态旋转位置编码（M-RoPE）这一创新。与 LLM 中仅能编码一维位置信息的传统 1D-RoPE 不同，M-RoPE 能够有效建模多模态输入的位置信息。其实现方式是将原有的旋转编码解构为三个分量：时间、高度与宽度。对于文本输入，这些分量使用相同的位置 ID，使 M-RoPE 在功能上等价于 1D-RoPE（[Su, 2024](#bib.bib90)）。在处理图像时，每个视觉 token 的时间 ID 保持不变，而高度与宽度分量则根据 token 在图像中的位置被赋予不同的 ID。对于被视为帧序列的视频，时间 ID 逐帧递增，而高度与宽度分量遵循与图像相同的 ID 分配模式。在模型输入包含多种模态的场景下，每种模态的位置编号通过在前一模态的最大位置 ID 上加一来初始化。M-RoPE 的示意图见图 3。M-RoPE 不仅增强了对位置信息的建模，还降低了图像与视频的位置 ID 取值，使模型在推理时能够外推到更长的序列。

##### 统一的图像与视频理解

Qwen2-VL 采用混合训练方案，同时纳入图像与视频数据，以确保图像理解与视频理解两方面的能力。为尽可能完整地保留视频信息，我们以每秒两帧对每个视频采样。此外，我们集成了深度为 2 的三维卷积（[Carreira and Zisserman, 2017](#bib.bib12)）来处理视频输入，使模型能够处理 3D tube 而非 2D patch，从而在不增加序列长度的情况下处理更多视频帧（[Arnab et al., 2021](#bib.bib8)）。为保持一致，每张图像被视为两个相同的帧。为在长视频处理的计算需求与整体训练效率之间取得平衡，我们动态调整每个视频帧的分辨率，将每个视频的总 token 数限制在 16384 以内。这种训练方法在模型理解长视频的能力与训练效率之间取得了平衡。

### 2.2 训练

沿袭 Qwen-VL（[Bai et al., 2023b](#bib.bib11)），我们采用三阶段训练方法。第一阶段，我们仅训练视觉 Transformer（ViT）组件，利用海量图文对语料来增强大语言模型（LLM）内部的语义理解。第二阶段，我们解冻所有参数，使用更广泛的数据进行更全面的学习。最后阶段，我们锁定 ViT 参数，使用指令数据集专门微调 LLM。

模型在多样化的数据集上预训练，包括图文对、光学字符识别（OCR）数据、图文交错的 articles、视觉问答数据集、视频对话与图像知识数据集。我们的数据来源主要包括清洗后的网页、开源数据集与合成数据。我们的数据知识截止日期为 2023 年 6 月。这种多样化的数据构成对于培养稳健的多模态理解能力至关重要。

在初始预训练阶段，Qwen2-VL 使用了约 6000 亿 token 的语料。Qwen2-VL 的 LLM 组件使用 Qwen2（[Yang et al., 2024](#bib.bib104)）的参数初始化，而视觉编码器则使用来自 DFN 的 ViT 初始化。不过，原始 DFN ViT（[Fang et al., 2023](#bib.bib28)）中的固定位置编码被替换为 RoPE-2D。这一预训练阶段主要聚焦于学习图文关系、通过 OCR 识别图像内的文本内容以及图像分类任务。此类基础训练有助于模型建立对核心视觉-文本关联与对齐的稳健理解。

第二预训练阶段标志着一次显著跃进，额外引入 8000 亿图像相关 token。该阶段引入了更多数量的图文混合内容，促进对视觉与文本信息之间交互的更细致理解。视觉问答数据集的纳入提升了模型响应图像相关查询的能力。此外，多任务数据集的引入对培养模型同时应对多样任务的能力至关重要——这一能力在处理复杂的真实世界数据集时尤为重要。与此同时，纯文本数据在保持并提升模型语言能力方面继续发挥关键作用。

在整个预训练阶段，Qwen2-VL 累计处理了 1.4 万亿 token。具体而言，这些 token 不仅涵盖文本 token，还包括图像 token。但在训练过程中，我们仅对文本 token 提供监督。这种对广泛多样的语言与视觉场景的接触，确保模型对视觉与文本信息之间的复杂关系建立起深刻理解，从而为各种多模态任务奠定坚实基础。

在指令微调阶段，我们采用 ChatML（[Openai, 2024](#bib.bib72)）格式构建指令遵循数据。该数据集不仅包含纯文本对话数据，还包含多模态对话数据。多模态部分包括图像问答、文档解析、多图比较、视频理解、视频流对话与基于智能体的交互。我们这种全面的数据构建方法旨在增强模型理解并执行跨多种模态的广泛指令的能力。通过纳入多样数据类型，我们力图打造一个更通用、更稳健的语言模型，除传统文本交互外还能处理复杂的多模态任务。

#### 2.2.1 数据格式。

与 Qwen-VL 一致，Qwen2-VL 也使用特殊 token 来区分视觉与文本输入。token ¡—vision_start—¿ 与 ¡—vision_end—¿ 被插入图像特征序列的首尾，以划定图像内容的边界。

##### 对话数据。

在对话格式方面，我们使用 ChatML 格式构建指令微调数据集，每次交互的发言以两个特殊 token（¡—im_start—¿ 与 ¡—im_end—¿）标记，以便于对话终止。蓝色标注的部分表示被监督的部分。

ChatML 的数据集格式示例

¡—im_start—¿user
¡—vision_start—¿Picture1.jpg¡—vision_end—¿¡—vision_start—¿Picture2.jpg¡—vision_end—¿What do the two pictures have in common?¡—im_end—¿
¡—im_start—¿assistant
Both pictures are of SpongeBob SquarePants. ¡—im_end—¿
¡—im_start—¿user
What is happening in the video?¡—vision_start—¿video.mp4¡—vision_end—¿¡—im_end—¿
¡—im_start—¿assistant
The protagonist in the video is frying an egg.¡—im_end—¿

##### 视觉定位（Visual Grounding）。

为赋予模型视觉定位（visual grounding）能力，边界框坐标在 [0, 1000) 内归一化，并表示为 $(X_{\text{top left}},Y_{\text{top left}}),(X_{\text{bottom right}},Y_{\text{bottom right}})$。token ¡—box_start—¿ 与 ¡—box_end—¿ 用于划定边界框文本的边界。为将边界框与其文本描述准确关联，我们引入 token ¡—object_ref_start—¿ 与 ¡—object_ref_end—¿ 来指示边界框所指代的内容，从而使模型能够有效解释并生成对特定区域的精确描述。

指代定位（Referring Grounding）

¡—vision_start—¿Picture1.jpg¡—vision_end—¿
¡—object_ref_start—¿the eyes on a giraffe¡—object_ref_end—¿¡—box_start—¿(176,106),(232,160) ¡—box_end—¿

##### 视觉智能体。

为将 Qwen2-VL 打造成通用的 VL 智能体（VL-Agent），我们将各类智能体任务——如 UI 操作、机器人控制、游戏与导航——视为序列决策问题，使 Qwen2-VL 能够通过多步动作执行来完成任务。对每项任务，我们首先定义一组允许的动作以及函数调用的关键词模式（下划线）（[Qwen Team, 2024](#bib.bib77)）。随后 Qwen2-VL 分析观察、执行推理与规划、执行所选动作，并与环境交互以获取新的观察。这一循环不断迭代，直到任务成功完成。通过整合各种工具并利用大型视觉语言模型（LVLM）的视觉感知能力，Qwen2-VL 能够迭代执行越来越复杂的、涉及真实世界视觉交互的任务。

视觉智能体（Visual Agent）

¡—im_start—¿system
You are a helpful assistant.
# Actions
## You have the following actions.
### Tap
Tap: A gentle tap that commands, chooses, or navigates through a smartphone’s user interface. Parameters: [{”name”: ”point”, ”description”: ”The specific spot of interest on the monitor, denoted by the coordinates (x, y) where x and y range from 0 to 1000.”, ”required”: True}]
### Home
Home: Go to phone’s home screen. Parameters: []
### Other Actions …
## Continuously take action until the task is completed.
*FUNCTION*: The action to take, should be one of {Actions}.
*ARGS*: The input of the action.
*RESULT*: Action results.
*RETURN*: Reply based on action results. ¡—im_end—¿
¡—im_start—¿user
Find a pizza restaurant nearby in Map. ¡—vision_start—¿Screenshot_1.jpg¡—vision_end—¿ ¡—im_end—¿
¡—im_start—¿assistant
Several e-mails are displaying on the phone screen. To open Map, I need go back to the home screen and find the corresponding app icon.
*FUNCTION*: Home *ARGS*: {}
*RESULT*: ¡—vision_start—¿Screenshot_2.jpg¡—vision_end—¿
*RETURN*: I return to the home screen. Next, I need to find the icon of Map and tap on it.
*FUNCTION*: Tap *ARGS*: {”point”: (348,291)}
*RESULT*: ¡—vision_start—¿Screenshot_3.jpg¡—vision_end—¿
*RETURN*: [Thinking for the next action.]
[Other subsequent actions.] ……
I have found the pizza restaurant nearby in Map. ¡—im_end—¿

### 2.3 多模态模型基础设施

Qwen2-VL 模型在阿里云 PAI-Lingjun 智算服务（[Alibaba-Cloud, 2024c](#bib.bib4)）上训练，利用了其可扩展算力、自动恢复与慢任务检测（straggler detection）能力。

##### 存储。

我们使用阿里云超高速 CPFS（Cloud Parallel File Storage，云并行文件存储）（[Alibaba-Cloud, 2024a](#bib.bib2)）构建 Qwen2-VL 预训练与后训练的存储系统。我们将文本数据与视觉数据的存储解耦。文本数据直接存储在 CPFS 上并使用 mmap 高效访问。对于视觉数据，我们使用阿里云 OSS（Object Storage Service，对象存储服务）（[Alibaba-Cloud, 2024b](#bib.bib3)）进行持久化存储。训练期间，我们通过 OSS 的 python-client 并发访问视觉数据，并调优并发与重试参数以避免触及 QPS（每秒查询数）限制。我们还发现视频数据解码是主要瓶颈，尤其是长视频。在多次尝试开源（[FFmpeg-Developers, 2024](#bib.bib29)）与自研软件均告失败后，我们选择了缓存解码技术。检查点（checkpointing）将每块 GPU 的优化器与模型状态保存到 CPFS。

##### 并行。

我们使用 3D 并行——结合数据并行（DP）（[Li et al., 2020](#bib.bib50)）、张量并行（TP）（[Krizhevsky et al., 2012](#bib.bib44)；[Shoeybi et al., 2019](#bib.bib83)）与流水线并行（PP）（[Huang et al., 2019](#bib.bib36)；[Narayanan et al., 2021](#bib.bib67)；[Lamy-Poirier, 2023](#bib.bib45)）——来扩展 Qwen2-VL 模型训练。我们还利用 deepspeed 的零冗余优化器 zero-1（[Rajbhandari et al., 2020](#bib.bib79)）对状态分片以节省显存。我们利用序列并行（SP）（[Korthikanti et al., 2023](#bib.bib43)）与选择性检查点激活（[Chen et al., 2016](#bib.bib17)）来降低显存占用。启用 TP 训练时，我们始终将视觉编码器与大语言模型一起分片，但不分片视觉合并层（vision merger），因为其参数相对较少。我们发现 TP 训练会因卷积算子的非确定性行为²导致模型共享权重出现不同结果。
² <https://pytorch.org/docs/stable/notes/randomness.html>。
我们通过对共享权重执行离线归约（offline reduction）解决了这一问题，从而避免了额外的 all-reduce 通信步骤。这一方法对性能的影响微乎其微。我们为 Qwen2-VL 72B 训练采用 1F1B PP（[Narayanan et al., 2021](#bib.bib67)）。我们将视觉编码器、视觉适配器与 LLM 的若干解码器层合并为一个 stage，并将剩余解码器层均分。注意，视觉与文本序列长度对每个数据点都是动态的。我们在启动 1F1B 流程之前广播动态序列长度，并使用批次索引访问形状信息。我们还实现了交错式 1F1B PP（[Narayanan et al., 2021](#bib.bib67)），但发现它比标准 1F1B 设置更慢。

##### 软件。

我们使用 PyTorch（[Paszke et al., 2019](#bib.bib74)；[Ansel et al., 2024](#bib.bib6)）2.1.2 版本配合 CUDA 11.8（[Nvidia, 2024b](#bib.bib69)）进行训练。此外，我们在视觉编码器与 LLM 中均利用 flash-attention（[Dao et al., 2022](#bib.bib24)；[Dao, 2024](#bib.bib23)；[Shah et al., 2024](#bib.bib82)）以实现高效训练。我们还使用融合算子（[Nvidia, 2024a](#bib.bib68)），如 LayerNorm（[Ba et al., 2016](#bib.bib9)）、RMSNorm（[Zhang and Sennrich, 2019](#bib.bib115)）与 Adam（[Loshchilov and Hutter, 2019](#bib.bib58)）。除此之外，我们在训练过程中利用了矩阵乘法中通信与计算的重叠。

## 实验

在本节中，我们首先通过在各种视觉基准上的对比分析来评估模型的性能，展示我们方法的优势。随后，我们对特定能力进行深入考察，包括通用视觉感知、文档理解、图像中的多语言识别、视频理解与智能体能力。最后，我们给出消融研究，以考察我们方法中若干关键组件的作用。

表 2：Qwen2-VL 模型与最先进模型的性能比较。

|  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- |
| 基准 | 此前 SoTA | Claude-3.5 Sonnet | GPT-4o | Qwen2-VL-72B | Qwen2-VL-7B | Qwen2-VL-2B |
| MMMUval ([Yue et al., 2023](#bib.bib111)) | 66.1 ([X.AI, 2024b](#bib.bib101)) | 68.3 | 69.1 | 64.5 | 54.1 | 41.1 |
| DocVQAtest ([Mathew et al., 2021](#bib.bib66)) | 94.1 ([Chen et al., 2024c](#bib.bib20)) | 95.2 | 92.8 | 96.5 | 94.5 | 90.1 |
| InfoVQAtest ([Mathew et al., 2021](#bib.bib66)) | 82.0 ([Chen et al., 2024c](#bib.bib20)) | - | - | 84.5 | 76.5 | 65.5 |
| AI2D ([Kembhavi et al., 2016](#bib.bib40)) | 87.6 ([Chen et al., 2024c](#bib.bib20)) | 80.2(94.7) | 84.6(94.2) | 88.1 | 83.0 | 74.7 |
| ChartQAtest ([Masry et al., 2022](#bib.bib65)) | 88.4 ([Chen et al., 2024c](#bib.bib20)) | 90.8 | 85.7 | 88.3 | 83.0 | 73.5 |
| TextVQAval ([Singh et al., 2019](#bib.bib87)) | 84.4 ([Chen et al., 2024c](#bib.bib20)) | - | - | 85.5 | 84.3 | 79.7 |
| OCRBench ([Liu et al., 2023e](#bib.bib57)) | 852 ([Yao et al., 2024](#bib.bib106)) | 788 | 736 | 877 | 866 | 809 |
| MTVQA ([Tang et al., 2024](#bib.bib92)) | 23.2 ([Team et al., 2023](#bib.bib93)) | 25.7 | 27.8 | 30.9 | 25.6 | 18.1 |
| VCRen easy ([Zhang et al., 2024c](#bib.bib119)) | 84.7 ([Chen et al., 2024c](#bib.bib20)) | 63.9 | 91.6 | 91.9 | 89.7 | 81.5 |
| VCRzh easy ([Zhang et al., 2024c](#bib.bib119)) | 22.1 ([Chen et al., 2024c](#bib.bib20)) | 1.0 | 14.9 | 65.4 | 59.9 | 46.2 |
| RealWorldQA ([X.AI, 2024a](#bib.bib100)) | 72.2 ([Chen et al., 2024c](#bib.bib20)) | 60.1 | 75.4 | 77.8 | 70.1 | 62.9 |
| MMEsum ([Fu et al., 2023](#bib.bib30)) | 2414.7 ([Chen et al., 2024c](#bib.bib20)) | 1920.0 | 2328.7 | 2482.7 | 2326.8 | 1872.0 |
| MMBench-ENtest ([Liu et al., 2023d](#bib.bib56)) | 86.5 ([Chen et al., 2024c](#bib.bib20)) | 79.7 | 83.4 | 86.5 | 83.0 | 74.9 |
| MMBench-CNtest ([Liu et al., 2023d](#bib.bib56)) | 86.3 ([Chen et al., 2024c](#bib.bib20)) | 80.7 | 82.1 | 86.6 | 80.5 | 73.5 |
| MMBench-V1.1test ([Liu et al., 2023d](#bib.bib56)) | 85.5 ([Chen et al., 2024c](#bib.bib20)) | 78.5 | 82.2 | 85.9 | 80.7 | 72.2 |
| MMT-Benchtest ([Ying et al., 2024](#bib.bib109)) | 63.4 ([Chen et al., 2024b](#bib.bib19)) | - | 65.5 | 71.7 | 63.7 | 54.5 |
| MMStar ([Chen et al., 2024a](#bib.bib15)) | 67.1 ([Chen et al., 2024c](#bib.bib20)) | 62.2 | 63.9 | 68.3 | 60.7 | 48.0 |
| MMVetGPT-4-Turbo ([Yu et al., 2024](#bib.bib110)) | 67.5 ([OpenAI., 2023](#bib.bib71)) | 66.0 | 69.1 | 74.0 | 62.0 | 49.5 |
| HallBenchavg ([Guan et al., 2023](#bib.bib32)) | 55.2 ([Chen et al., 2024c](#bib.bib20)) | 49.9 | 55.0 | 58.1 | 50.6 | 41.7 |
| MathVistatestmini ([Lu et al., 2024a](#bib.bib61)) | 69.0 ([X.AI, 2024b](#bib.bib101)) | 67.7 | 63.8 | 70.5 | 58.2 | 43.0 |
| MathVision ([Wang et al., 2024](#bib.bib96)) | 30.3 ([OpenAI, 2023](#bib.bib70)) | - | 30.4 | 25.9 | 16.3 | 12.4 |
| MMMU-Pro ([Yue et al., 2024](#bib.bib112)) | 46.9 ([Team et al., 2023](#bib.bib93)) | 51.5 | 51.9 | 46.2 | 43.5 | 37.6 |

表 3：Qwen2-VL 与 GPT-4o 在内部多语言 OCR 基准上的性能。

|  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 语言 | 韩语 | 日语 | 法语 | 德语 | 意大利语 | 俄语 | 越南语 | 阿拉伯语 |
| GPT-4o | 87.8 | 88.3 | 89.7 | 88.3 | 74.1 | 96.8 | 72.0 | 75.9 |
| Qwen2-VL-72B | 94.5 | 93.4 | 94.1 | 91.5 | 89.8 | 97.2 | 73.0 | 70.7 |

表 4：Qwen2-VL 与其他模型在视频基准上的性能。

|  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- |
| 基准 | 此前 SoTA | Gemini 1.5-Pro | GPT-4o | Qwen2-VL-72B | Qwen2-VL-7B | Qwen2-VL-2B |
| MVBench ([Li et al., 2024](#bib.bib49)) | 69.6 | - | - | 73.6 | 67.0 | 63.2 |
| PerceptionTesttest ([Patraucean et al., 2024](#bib.bib75)) | 66.9 | - | - | 68.0 | 62.3 | 53.9 |
| EgoSchematest ([Mangalam et al., 2023](#bib.bib63)) | 62.0 | 63.2 | 72.2 | 77.9 | 66.7 | 54.9 |
| Video-MME(wo/w subs) ([Fu et al., 2024](#bib.bib31)) | 66.3/69.6 | 75.0/81.3 | 71.9/77.2 | 71.2/77.8 | 63.3/69.0 | 55.6/60.4 |

表 5：Qwen2-VL-72B 与 GPT-4o 在各种智能体基准上的性能比较。SR、GC、TM 与 EM 分别是成功率（success rate）、目标条件成功率（goal-condition success）、类型匹配（type match）与精确匹配（exact match）的缩写。ALFRED、R2R 与 REVERIE 为 valid-unseen 划分上的性能。

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  | 基准 | 指标 | 此前 SoTA | GPT-4o | Qwen2-VL-72B |
| 通用 | FnCall | TM | - | 90.2 | 93.1 |
| EM | - | 50.0 | 53.2 |
| UI 操作 | AITZ ([Zhang et al., 2024b](#bib.bib117)) | TM | 83.0 ([Hong et al., 2023](#bib.bib33)) | 70.0 | 89.6 |
| EM | 47.7 ([Zhan and Zhang, 2023](#bib.bib114)) | 35.3 | 72.1 |
| 卡牌游戏 | Number Line ([Zhai et al., 2024](#bib.bib113)) | SR | 89.4 ([Zhai et al., 2024](#bib.bib113)) | 91.5 | 100.0 |
| BlackJack ([Zhai et al., 2024](#bib.bib113)) | SR | 40.2 ([Zhai et al., 2024](#bib.bib113)) | 34.5 | 42.6 |
| EZPoint ([Zhai et al., 2024](#bib.bib113)) | SR | 50.0 ([Zhai et al., 2024](#bib.bib113)) | 85.5 | 100.0 |
| Point24 ([Zhai et al., 2024](#bib.bib113)) | SR | 2.6 ([Liu et al., 2023b](#bib.bib54)) | 3.0 | 4.5 |
| 机器人控制 | ALFRED ([Shridhar et al., 2020a](#bib.bib84)) | SR | 67.7 ([Lu et al., 2023](#bib.bib59)) | - | 67.8 |
| GC | 75.3 ([Lu et al., 2023](#bib.bib59)) | - | 75.8 |
| 导航 | R2R ([Anderson et al., 2018](#bib.bib5)) | SR | 79.0 ([Chen et al., 2022](#bib.bib16)) | 43.7 | 51.7 |
| REVERIE ([Qi et al., 2020](#bib.bib76)) | SR | 61.0 ([Sigurdsson et al., 2023](#bib.bib86)) | 31.6 | 31.0 |

### 3.1 与 SoTA 比较

我们通过各种视觉基准、视频任务与基于智能体的评测来评估模型的视觉能力。Qwen2-VL 在同等规模下展现出极具竞争力的性能，取得新的最先进（SoTA）结果。总体而言，我们的 72B 模型在大多数评测指标上持续交出顶级表现，频繁超越 GPT-4o（[OpenAI, 2024](#bib.bib73)）与 Claude 3.5-Sonnet（[Anthropic, 2024](#bib.bib7)）等闭源模型。值得注意的是，它在文档理解任务中展现出显著优势。然而，在 MMMU（[Yue et al., 2023](#bib.bib111)）基准上，我们的模型在一定程度上仍落后于 GPT-4o，表明 Qwen2-VL-72B 在处理更复杂、更具挑战性的问题集时仍有提升空间。

### 3.2 定量结果

在本节中，我们在一系列数据集上对 Qwen2-VL 系列进行广泛评测，以全面理解模型在各个方面的能力。

#### 3.2.1 通用视觉问答

为严格评估模型在通用视觉问答任务上的能力，我们在多样化的最先进基准上进行了广泛评测：RealWorldQA（[X.AI, 2024a](#bib.bib100)）、MMStar（[Chen et al., 2024a](#bib.bib15)）、MMVet（[Yu et al., 2024](#bib.bib110)）、MMT-Bench（[Ying et al., 2024](#bib.bib109)）、MMBench（[Liu et al., 2023d](#bib.bib56)）、MMbench-1.1（[Liu et al., 2023d](#bib.bib56)）、MME（[Fu et al., 2023](#bib.bib30)）与 HallusionBench（[Guan et al., 2023](#bib.bib32)）。Qwen2-VL 系列在这些基准上表现卓越，72B 模型持续达到或超越最先进结果，7B 与 2B 变体也展现出稳健能力。在评估真实世界空间理解的 RealWorldQA 上，Qwen2-VL-72B 取得 77.7 的分数，超越此前最先进结果（72.2）以及 GPT-4o（75.4）等强大基线，展示了对物理环境的优越理解。在 MMStar——一个通过视觉上不可或缺的样本评估真正多模态能力的基准——上，Qwen2-VL-72B 取得 68.3，优于此前最佳的 67.1，凸显了其整合视觉与文本信息的娴熟能力。在 MMVet——评估 16 项复杂多模态任务中核心视觉-语言能力整合的基准——上，Qwen2-VL-72B 取得 74.0 的出色成绩，显著超越包括 GPT-4V（67.5）在内的强劲对手，展示了其应对多样多模态挑战的全面性。在 MMT-Bench 评测——评估多模态理解中 32 项核心元任务与 162 项子任务上的高级推理与指令遵循——中，Qwen2-VL-72B 取得 71.7，大幅超越此前最佳（63.4），展示了其运用专家知识并执行审慎的视觉识别、定位、推理与规划的能力。在评估 20 个维度上细粒度能力的 MMBench 上，Qwen2-VL-72B 表现强劲，在英文测试集上取得 86.5，与最先进水平持平，在中文测试集上取得 86.6，树立了新的标杆。在衡量 14 个子任务上广泛感知与认知能力的 MME 上，Qwen2-VL-72B 取得 2482.7 的累计分数，显著超越此前最佳（2414.7），凸显了其在视觉感知与高级认知任务上的先进能力。

这些全面的结果凸显了 Qwen2-VL 系列在通用视觉问答任务上的卓越能力。模型在真实世界空间理解、真正的多模态整合、复杂推理、指令遵循以及广泛的感知与认知任务上均展现出先进能力。在多样基准上持续的优越表现，尤其是 72B 模型的杰出结果，使 Qwen2-VL 系列成为视觉问答领域的领先解决方案。我们的模型擅长处理视觉上不可或缺的任务、整合核心视觉-语言能力，并在从基础感知任务到复杂推理与规划的多样多模态场景中展现专业性。这一详尽的评测凸显了 Qwen2-VL 系列在应对最先进多模态基准所提出的多面挑战时的通用性与有效性，从而为大型视觉语言模型树立了新标准。

#### 3.2.2 文档与图表阅读

我们在 DocVQA（[Mathew et al., 2021](#bib.bib66)）、ChartQA（[Masry et al., 2022](#bib.bib65)）、InfoVQA（[Mathew et al., 2021](#bib.bib66)）、TextVQA（[Singh et al., 2019](#bib.bib87)）、AI2D（[Kembhavi et al., 2016](#bib.bib40)）数据集上测试了模型的 OCR 与文档及图表理解能力。DocVQA/InfoVQA/ChartQA 数据集聚焦模型理解文档/高分辨率信息图/图表中文字的能力，而 TextVQA 数据集考察理解自然场景图像中文字的能力。OCRBench 数据集是一个混合任务数据集，除基于文本的 VQA 外还聚焦数学公式解析与信息抽取。AI2D 数据集聚焦于包含文字的科学示意图选择题。此外，我们还在 OCRBench（[Liu et al., 2023e](#bib.bib57)）上测试了模型的 OCR 与公式识别能力，并在 MTVQA（[Tang et al., 2024](#bib.bib92)）数据集上测试了模型的多语言 OCR 能力。

实验结果表明，我们的模型在多个指标上达到 SoTA 水平，包括 DocVQA、InfoVQA、TextVQA 与 OCRBench，表明模型对来自多个领域的图像中的文本内容具有良好的理解能力。

#### 3.2.3 多语言文本识别与理解

尤其突出的是，我们的模型在多语言 OCR 上超越了所有现有多用途 LVLM。我们的模型不仅在公开可得的 MTVQA 数据集上胜过现有 LVLM（包括 GPT-4o、Claude 3.5 Sonnet 等专有模型），在内部基准上也于除阿拉伯语外的所有外语上胜过 GPT-4o（表 3）。

#### 3.2.4 数学推理

我们在 MathVista（[Lu et al., 2024a](#bib.bib61)）与 MathVision（[Wang et al., 2024](#bib.bib96)）数据集上进行了实验，以评估数学推理能力。MathVista 是一个综合基准，包含 6,141 个多样的数学与视觉任务示例。MathVision 数据集包含 3,040 道嵌入在实际数学竞赛视觉情境中的数学题，覆盖 16 个数学学科，难度横跨五个级别。这些挑战凸显了 LVLM 具备强视觉理解、深厚数学理解与扎实逻辑推理技能的必要性。Qwen2-VL 系列在 MathVista 上表现优越，取得 70.5，胜过其他 LVLM。此外，它以 25.9 在 MathVision 上创下新的开源纪录。

#### 3.2.5 指代表达理解

在视觉定位任务方面，我们在 RefCOCO、RefCOCO+ 与 RefCOCOg 数据集（[Kazemzadeh et al., 2014](#bib.bib39)；[Mao et al., 2016](#bib.bib64)）上评测 Qwen2-VL。如表 6 所示，结果表明 Qwen2-VL 在通用模型中取得顶级结果。得益于更合理的结构设计，Qwen2-VL 能够感知高分辨率图像中的细节，相较 Qwen-VL 取得显著提升。这些模型相较通用与专用模型的优越性，凸显了它们推动视觉定位领域发展的潜力，以及在需要精确视觉理解的任务中进行现实实现的能耐。

表 6：指代表达理解任务上的性能比较。

|  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 类型 | 模型 | RefCOCO | | | RefCOCO+ | | | RefCOCOg | |
| val | test-A | test-B | val | test-A | test-B | val | test |
| 通用模型 | OFA-L ([Wang et al., 2022](#bib.bib97)) | 80.0 | 83.7 | 76.4 | 68.3 | 76.0 | 61.8 | 67.6 | 67.6 |
| Shikra ([Chen et al., 2023a](#bib.bib13)) | 87.0 | 90.6 | 80.2 | 81.6 | 87.4 | 72.1 | 82.3 | 82.2 |
| Qwen-VL ([Bai et al., 2023b](#bib.bib11)) | 89.4 | 92.3 | 85.3 | 83.1 | 88.3 | 77.2 | 85.6 | 85.5 |
| Ferretv2 ([Zhang et al., 2024a](#bib.bib116)) | 92.6 | 95.0 | 88.9 | 87.4 | 92.1 | 81.4 | 89.4 | 90.0 |
| CogVLM ([Wang et al., 2023b](#bib.bib99)) | 92.8 | 94.8 | 89.0 | 88.7 | 92.9 | 83.4 | 89.8 | 90.8 |
| InternVL22b ([Chen et al., 2024c](#bib.bib20)) | 82.3 | 88.2 | 75.9 | 73.5 | 82.8 | 63.3 | 77.6 | 78.3 |
| InternVL28b ([Chen et al., 2024c](#bib.bib20)) | 87.1 | 91.1 | 80.7 | 79.8 | 87.9 | 71.4 | 82.7 | 82.7 |
| InternVL276b ([Chen et al., 2024c](#bib.bib20)) | 92.2 | 94.8 | 88.4 | 88.8 | 93.1 | 82.8 | 89.5 | 90.3 |
| Qwen2-VL2b | 87.6 | 90.6 | 82.3 | 79.0 | 84.9 | 71.0 | 81.2 | 80.3 |
| Qwen2-VL7b | 91.7 | 93.6 | 87.3 | 85.8 | 90.5 | 79.5 | 87.3 | 87.8 |
| Qwen2-VL72b | 93.2 | 95.3 | 90.7 | 90.1 | 93.8 | 85.6 | 89.9 | 90.4 |
| 专用模型 | G-DINO-L ([Liu et al., 2023c](#bib.bib55)) | 90.6 | 93.2 | 88.2 | 82.8 | 89.0 | 75.9 | 86.1 | 87.0 |
| UNINEXT-H ([Yan et al., 2023](#bib.bib102)) | 92.6 | 94.3 | 91.5 | 85.2 | 89.6 | 79.8 | 88.7 | 89.4 |
| ONE-PEACE ([Wang et al., 2023a](#bib.bib98)) | 92.6 | 94.2 | 89.3 | 88.8 | 92.2 | 83.2 | 89.2 | 89.3 |

#### 3.2.6 视频理解

我们在各种视频理解任务上评测模型，相关基准覆盖从几秒钟的短视频到长达一小时的长视频。表 4 给出了 Qwen2-VL 与基线模型的性能。总体而言，Qwen2-VL 在 2B、7B 与 72B 规模上都展现出强劲结果，其中 Qwen2-VL-72B 在 MVBench（[Li et al., 2024](#bib.bib49)）、PerceptionTest（[Patraucean et al., 2024](#bib.bib75)）与 EgoSchema（[Mangalam et al., 2023](#bib.bib63)）上取得最佳性能。这展示了 Qwen2-VL 在视频理解任务上的优越能力，且扩大 Qwen2-VL 的规模可带来显著提升。对于包含长达一小时视频的颇具挑战性的 Video-MME 基准（[Fu et al., 2024](#bib.bib31)），值得注意的是，我们在评测期间将每个视频抽取的最大帧数限制为 768，这可能会影响在较长视频上的性能。未来的工作将聚焦于扩展 Qwen2-VL 以支持更长序列，从而容纳更长的视频。

#### 3.2.7 视觉智能体

我们首先评测 Qwen2-VL 通过函数调用与环境交互的能力，然后评测其通过多轮交互完成复杂序列决策任务的能力。实现基于 Qwen-Agent 框架（[Qwen Team, 2024](#bib.bib77)）。

##### 函数调用

与 LLM 中的函数调用（[Yan et al., 2024](#bib.bib103)；[Srinivasan et al., 2023](#bib.bib88)；[Chen et al., 2023c](#bib.bib18)）不同，LVLM 中的函数调用往往涉及从视觉线索中提取信息。由于缺乏评估 LVLM 函数调用能力的公开基准，我们构建了内部评测数据集。

为构建评测数据集，我们执行了以下流程（[Chen et al., 2023c](#bib.bib18)）：场景分类、图像收集、图像内容提取，以及问题/函数/参数生成。首先，我们基于不同的视觉应用将场景划分为若干类别。随后，我们从互联网上为每个类别下载并精心挑选高质量、有代表性的图像。此后，我们利用先进的 LVLM（[Bai et al., 2023b](#bib.bib11)）分析每张图像，提取关键视觉元素与文本信息。最后，基于图像的内容信息，我们使用先进的 LLM（[Yang et al., 2024](#bib.bib104)）生成一系列需要特定函数才能回答的问题，并指定这些函数调用所需的输入参数。

类似于 LLM 中的函数调用评测方法（[Yan et al., 2024](#bib.bib103)），我们设计了两个指标来评估函数选择的准确性与输入参数的正确性。具体而言，类型匹配（Type Match，TM）计算为模型成功调用正确函数的次数占尝试调用总数的比例。精确匹配（Exact Match，EM）：对每次函数调用，我们检查传递给函数的参数是否与图像内容信息中记录的参数完全一致，并计算该正确率。

如表 5 所示，Qwen2-VL 在类型匹配（93.1 对 90.2）与精确匹配（53.2 对 50.0）两项上均胜过 GPT-4o，证实了 Qwen2-VL 在函数调用方面的能力有效性，从而凸显了其通过外部工具集成扩展应用的巨大潜力。

评测结果表明 GPT-4o 表现欠佳主要源于两个因素：在出现不确定性的场景中，GPT-4o 表现出保守倾向，避免使用外部工具；GPT-4o 的光学字符识别（OCR）能力不敌 Qwen2-VL，尤以中文字符场景为甚。

##### UI 操作/游戏/机器人/导航

为评估 Qwen2-VL 通用处理复杂任务的能力，我们在多个 VL 智能体任务上进行了评测，包括移动端操作（[Zhang et al., 2024b](#bib.bib117)；[Rawles et al., 2024b](#bib.bib81)；[Lu et al., 2024b](#bib.bib62)；[Rawles et al., 2024a](#bib.bib80)）、机器人控制（[Kolve et al., 2017](#bib.bib42)；[Shridhar et al., 2020a](#bib.bib84)；[Inoue and Ohashi, 2022](#bib.bib37)；[Lu et al., 2023](#bib.bib59)；[Jiang et al., 2022](#bib.bib38)；[Huang et al., 2023b](#bib.bib35)）、卡牌游戏（[Zhai et al., 2024](#bib.bib113)）与视觉语言导航（[Anderson et al., 2018](#bib.bib5)；[Qi et al., 2020](#bib.bib76)）。由于这些任务需要多个动作才能完成，我们借助 Qwen2-VL 支持的 32K 上下文长度保留（观察，动作）历史，并在每个动作后追加新的观察图像，从而实现对后续步骤的持续推理。

UI 操作：我们使用 AITZ 任务（[Zhang et al., 2024b](#bib.bib117)）评测 Qwen2-VL，该任务基于 AITW（[Rawles et al., 2024b](#bib.bib81)）构建了一个核心的干净测试集。基于手机的常见操作模式，我们定义了点按（tap）、输入（input）与滑动（swipe）等动作（[Rawles et al., 2024b](#bib.bib81)），供 Qwen2-VL 与屏幕上的图标交互以完成任务。例如，当 Qwen2-VL 被要求通过 Google 地图查找附近的披萨餐厅时，它应当在搜索框中输入“pizza”，滑动选择合适的餐厅，并点击相应的链接。按照 AITZ 的设置，我们同时报告类型匹配（点按、输入或滑动的正确性）与精确匹配（点按位置、输入文本或滑动方向的正确性）。凭借在 UI 上的定位能力支持，Qwen2-VL 超越了 GPT-4 与此前 SoTA（[Zhang et al., 2024b](#bib.bib117)；[Zhan and Zhang, 2023](#bib.bib114)）。

机器人控制：我们在 AI2THOR（[Kolve et al., 2017](#bib.bib42)）中的 ALFRED 任务（[Shridhar et al., 2020a](#bib.bib84)）上评测 Qwen2-VL。该任务要求智能体执行复杂的家务任务，例如烤面包片、切苹果以准备一餐。为在虚拟环境中工作，我们定义了高层动作（GotoLocation、Pickup、PutDown、Open、Close、Clean、Heat、Cool、Slice）（[Shridhar et al., 2020b](#bib.bib85)）作为动作集。此外，智能体需要定位物体以便操作（例如，只有识别出苹果才能拿起苹果）。为提高操作的准确性，我们集成了 SAM（[Kirillov et al., 2023](#bib.bib41)）。ALFRED 任务报告任务成功率（SR）（如准备晚餐）与子目标完成率（GC）（如面包是否烤好、苹果是否切开）。Qwen2-VL 在 valid-unseen 集上略胜过此前的专用模型 ThinkBot（[Lu et al., 2023](#bib.bib59)）。

卡牌游戏：我们利用 RL4VLM（[Zhai et al., 2024](#bib.bib113)）的卡牌游戏环境来评估 Qwen2-VL 在一系列卡牌游戏中的表现：Number Line、BlackJack、EZPoint 与 Point24。每个游戏呈现不同挑战：(1) 使用 +1 或 -1 运算达到目标数字；(2) 抽牌或停牌以与庄家竞争；(3) 运用基本算术运算使总数达到 12；(4) 使用算术运算使总数达到 24。我们报告任务的成功率。这些游戏不仅评估智能体能力，还要求强大的 OCR 技能来识别这些卡牌并理解游戏进程。Qwen2-VL 在所有任务上均展现出优越表现。

视觉语言导航：我们使用 R2R（[Anderson et al., 2018](#bib.bib5)）与 REVERIE（[Qi et al., 2020](#bib.bib76)）在视觉语言导航（VLN）任务上评测 Qwen2-VL。在 VLN 中，模型必须基于指令与当前观察自主确定下一个位置。我们报告 VLM 在该任务中到达预定目的地的成功率（SR）。Qwen2-VL 的性能与 GPT-4o 相当，但两个模型都显著落后于当前的专用 VLN 模型（[Chen et al., 2022](#bib.bib16)；[Sigurdsson et al., 2023](#bib.bib86)）。我们将这一差距归因于模型从多张图像生成的地图信息不完整且非结构化。在 3D 环境中精确建模地图与位置仍是多模态模型面临的重大挑战。

### 3.3 消融研究

在本节中，我们给出关于图像动态分辨率、M-RoPE 与模型规模的消融研究。这些实验旨在为这些关键组件对模型性能的影响提供洞见。

#### 3.3.1 动态分辨率

表 7：固定/动态图像 token 下的 Qwen2-VL-7B。调整图像尺寸仅引起性能的小幅扰动，展示了对不同图像尺寸的稳健性。此外，动态分辨率策略以平均更少的 token 消耗取得顶级性能，展示了我们模型的效率。

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| 策略 | 平均图像 token 数 | InfoVQAval | RealWorldQA | OCRBench | MMMU |
| 固定图像 token 数 | 64 | 28.85 | 56.47 | 572 | 53.33 |
| 576 | 65.72 | 65.88 | 828 | 52.78 |
| 1600 | 74.99 | 69.54 | 824 | 52.89 |
| 3136 | 77.27 | 70.59 | 786 | 53.44 |
| 动态图像 token 数 | 1924 | 75.89 | 70.07 | 866 | 53.44 |

![Refer to caption](2409.12191v2/images/qwen2-vl/minpixels_resolution.png)

图 4：采用不同 min_pixels 的 Qwen2-VL-7B。小图像会被上采样以超过指定的 min_pixels 阈值后再输入模型。在合理范围内增大图像尺寸，在 InfoVQA、HallusionBench 与 OCRBench 等感知任务上表现出性能提升。

如表 7 所示，我们比较了动态分辨率与固定分辨率的性能。对于固定分辨率，我们调整图像尺寸以确保输入模型的图像 token 数量恒定，而不是调整为特定的高和宽——因为那样会扭曲原始宽高比。对于动态分辨率，我们仅设置 min_pixels=$100\times 28\times 28$ 与 max_pixels=$16384\times 28\times 28$，使图像 token 数量主要取决于图像的原生分辨率。可以观察到，调整图像尺寸仅引起性能的小幅扰动，展示了模型对不同图像尺寸的稳健性。此外，动态分辨率方法更为高效。我们可以观察到，没有任何单一固定分辨率能在所有基准上都取得最优性能。相比之下，动态分辨率方法以平均更少的 token 消耗持续取得顶级性能。

另外，我们观察到单纯增大图像尺寸并不总能带来性能提升。为不同图像选择合适的分辨率更为重要。如图 4 所详述，我们对小图像进行上采样以超过指定的 min_pixels 阈值。在上采样图像上的评测显示，在 InfoVQA、HallusionBench 与 OCRBench 等感知任务上性能有所增强。我们将这些收益归因于计算负载的增加。然而，对于 OCRBench，过高的 min_pixels 值会导致严重的性能下降。这很可能是因为 OCRBench 包含大量极小图像，过度放大会使这些图像偏离训练数据分布，变成分布外（out-of-distribution）样本。相比之下，增大 min_pixels 对 MMMU 基准的影响可以忽略。我们推测 MMMU 的性能瓶颈更多与模型的推理能力相关，而非图像分辨率。

#### 3.3.2 M-RoPE

表 8：M-RoPE 的消融研究。与 1D-RoPE 相比，使用 M-RoPE 在下游任务中取得更好性能，尤其是在视频基准上。RWQ 指 RealworldQA。

|  |  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | 图像基准 | | | | | | | | 视频基准 | | |
|  | MathVista | MMB | MMStar | RWQ | DocVQA | ChartQA | InfoVQA | TextVQA | PerceptionTest | NextQA | STAR |
| 1D-RoPE | 39.2 | 58.6 | 36.7 | 54.5 | 82.5 | 68.0 | 50.8 | 71.3 | 46.6 | 43.9 | 55.5 |
| M-RoPE | 43.4 | 60.6 | 36.7 | 53.7 | 82.8 | 68.4 | 50.3 | 71.8 | 47.4 | 46.0 | 57.9 |

![Refer to caption](2409.12191v2/peng_fig2.png)

图 5：在 Video-MME 中等时长视频上评估 Qwen2-VL-72B 的长度外推能力。借助 M-RoPE，当推理长度超过 16384 token 的最大训练长度时，模型展现出稳健的性能。

在本小节中，我们论证 M-RoPE 的有效性。首先，我们在各种下游任务上验证其能力。我们采用 Qwen2-1.5B 与 ViT-L 作为骨干，并报告预训练模型的结果。如表 8 所示，与 1D-RoPE 相比，使用 M-RoPE 在下游任务中取得更好性能，尤其是在视频基准上。此外，我们在 Video-MME 中等时长视频上评估 M-RoPE 的长度外推能力。图 5 展示了 Qwen2-VL-72B 在不同推理长度下的性能。借助 M-RoPE，模型在各种推理长度下均展现出稳健结果。值得注意的是，尽管训练期间每个视频的最大 token 数被限制为 16K，模型在 80K token 的最大推理长度下仍表现出卓越性能。

#### 3.3.3 模型规模化

![Refer to caption](2409.12191v2/images/scale.jpg)

图 6：模型性能随能力维度与训练进程的规模化。随着模型规模与训练数据量的增加，性能在一系列能力与基准上持续提升。

我们评估不同规模模型在多个能力维度上的性能。具体而言，我们将这些维度归类为：复杂的大学水平问题求解、数学能力、文档与表格理解、通用场景问答以及视频理解。一个模型的整体能力通过其在与每个维度相关的不同基准上的平均得分来评估。

具体来说，我们使用 MMMU（[Yue et al., 2023](#bib.bib111)）基准代表大学水平的问题求解能力，而 MathVista（[Lu et al., 2024a](#bib.bib61)）与 MathVision（[Wang et al., 2024](#bib.bib96)）的平均分作为数学能力的指标。对于通用场景问答，我们计算 RealWorldQA（[X.AI, 2024a](#bib.bib100)）、MMBench-V1.1（[Liu et al., 2023d](#bib.bib56)）、MMT-Bench（[Ying et al., 2024](#bib.bib109)）、HallBench（[Guan et al., 2023](#bib.bib32)）、MMVet（[Yu et al., 2024](#bib.bib110)）与 MMStar（[Chen et al., 2024a](#bib.bib15)）等基准的平均分。文档与表格理解能力通过 DocVQA（[Mathew et al., 2021](#bib.bib66)）、InfoVQA（[Mathew et al., 2021](#bib.bib66)）、ChartQA（[Masry et al., 2022](#bib.bib65)）、TextVQA（[Singh et al., 2019](#bib.bib87)）、OCRBench（[Liu et al., 2023e](#bib.bib57)）与 MTVQA（[Tang et al., 2024](#bib.bib92)）等基准的平均分反映。最后，视频理解能力通过 MVBench（[Li et al., 2024](#bib.bib49)）、PerceptionTest（[Patraucean et al., 2024](#bib.bib75)）、EgoSchema（[Mangalam et al., 2023](#bib.bib63)）与 Video-MME（[Fu et al., 2024](#bib.bib31)）的平均分衡量。

如图 6(a) 所示，随着模型规模增大，性能持续提升，尤其在数学能力方面，其与模型参数量呈正相关。另一方面，对于光学字符识别（OCR）相关任务，即便是较小规模的模型也表现出相对较强的性能。

如图 6(b) 所示，我们可视化了 Qwen2-VL-7B 在第二阶段预训练期间模型性能与训练 token 数之间的关系。随着训练 token 数增加，模型性能提升；然而，视觉问答（VQA）任务上的性能出现一些波动。相比之下，对于 AI2D（[Kembhavi et al., 2016](#bib.bib40)）与 InfoVQA（[Mathew et al., 2021](#bib.bib66)）等涉及理解图像中文字与图形信息的任务，模型性能随训练数据的增加而稳步提升。

## 结论

我们提出了 Qwen2-VL 系列——多功能的大型视觉语言模型，包括总参数量分别为 20 亿、80 亿与 720 亿的三个开放权重模型。Qwen2-VL 在一系列多模态场景中匹敌 GPT-4o 与 Claude3.5-Sonnet 等顶级模型的性能，超越所有其他开放权重 LVLM 模型。Qwen2-VL 系列引入了原生动态分辨率与多模态旋转位置编码（M-RoPE），以有效融合跨模态信息，并能够理解超过 20 分钟的长视频。凭借先进的推理与决策能力，Qwen2-VL 可以与手机、机器人等设备集成。此外，Qwen2-VL 现在支持理解图像内的多语言文本，包括大多数欧洲语言、日语、韩语、阿拉伯语、越南语等。

我们已公开 Qwen2-VL 模型权重，使研究人员与开发者得以在各类应用与研究项目中充分发挥其潜力。我们致力于通过这些努力推进人工智能技术，并增强其对社会的有益影响。

## 致谢

我们感谢阿里云 PAI 团队（[Alibaba-Cloud, 2024c](#bib.bib4)）的 Juan Zhu、Fan Hong、Jie Zhang、Yong Li 为 Qwen2-VL 训练基础设施提供的支持。本工作还得益于 Qwen LLM 团队（[Yang et al., 2024](#bib.bib104)）的支持，我们特别感谢 Na Ni、Yichang Zhang、Jianxin Ma、Bowen Yu、Zheren Fu 的数据贡献与富有洞见的讨论。

## 参考文献


- Alayrac et al. (2022)

  Jean-Baptiste Alayrac, Jeff Donahue, Pauline Luc, Antoine Miech, Iain Barr, Yana Hasson, Karel Lenc, Arthur Mensch, Katherine Millican, Malcolm Reynolds, et al.
  Flamingo: a visual language model for few-shot learning.
  In *NeurIPS*, 2022.
- Alibaba-Cloud (2024a)

  Alibaba-Cloud.
  Cloud parallel file storage (cpfs), 2024a.
  URL <https://www.alibabacloud.com/en/product/cpfs>.
- Alibaba-Cloud (2024b)

  Alibaba-Cloud.
  Object storage service (oss), 2024b.
  URL <https://www.alibabacloud.com/en/product/object-storage-service>.
- Alibaba-Cloud (2024c)

  Alibaba-Cloud.
  Pai-lingjun intelligent computing service, 2024c.
  URL <https://www.alibabacloud.com/en/product/pai-lingjun>.
- Anderson et al. (2018)

  Peter Anderson, Qi Wu, Damien Teney, Jake Bruce, Mark Johnson, Niko Sünderhauf, Ian Reid, Stephen Gould, and Anton Van Den Hengel.
  Vision-and-language navigation: Interpreting visually-grounded navigation instructions in real environments.
  In *CVPR*, 2018.
- Ansel et al. (2024)

  Jason Ansel, Edward Z. Yang, Horace He, Natalia Gimelshein, Animesh Jain, Michael Voznesensky, Bin Bao, Peter Bell, David Berard, Evgeni Burovski, Geeta Chauhan, Anjali Chourdia, Will Constable, Alban Desmaison, Zachary DeVito, Elias Ellison, Will Feng, Jiong Gong, Michael Gschwind, Brian Hirsh, Sherlock Huang, Kshiteej Kalambarkar, Laurent Kirsch, Michael Lazos, Mario Lezcano, Yanbo Liang, Jason Liang, Yinghai Lu, C. K. Luk, Bert Maher, Yunjie Pan, Christian Puhrsch, Matthias Reso, Mark Saroufim, Marcos Yukio Siraichi, Helen Suk, Shunting Zhang, Michael Suo, Phil Tillet, Xu Zhao, Eikan Wang, Keren Zhou, Richard Zou, Xiaodong Wang, Ajit Mathews, William Wen, Gregory Chanan, Peng Wu, and Soumith Chintala.
  Pytorch 2: Faster machine learning through dynamic python bytecode transformation and graph compilation.
  In *ASPLOS*, 2024.
- Anthropic (2024)

  Anthropic.
  Claude 3.5 sonnet, 2024.
  URL <https://www.anthropic.com/news/claude-3-5-sonnet>.
- Arnab et al. (2021)

  Anurag Arnab, Mostafa Dehghani, Georg Heigold, Chen Sun, Mario Lučić, and Cordelia Schmid.
  Vivit: A video vision transformer.
  In *ICCV*, 2021.
- Ba et al. (2016)

  Lei Jimmy Ba, Jamie Ryan Kiros, and Geoffrey E. Hinton.
  Layer normalization.
  *arXiv:1607.06450*, 2016.
- Bai et al. (2023a)

  Jinze Bai, Shuai Bai, Yunfei Chu, Zeyu Cui, Kai Dang, Xiaodong Deng, Yang Fan, Wenbin Ge, Yu Han, Fei Huang, et al.
  Qwen technical report.
  *arXiv:2309.16609*, 2023a.
- Bai et al. (2023b)

  Jinze Bai, Shuai Bai, Shusheng Yang, Shijie Wang, Sinan Tan, Peng Wang, Junyang Lin, Chang Zhou, and Jingren Zhou.
  Qwen-vl: A frontier large vision-language model with versatile abilities.
  *arXiv:2308.12966*, 2023b.
- Carreira and Zisserman (2017)

  Joao Carreira and Andrew Zisserman.
  Quo vadis, action recognition? a new model and the kinetics dataset.
  In *CVPR*, 2017.
- Chen et al. (2023a)

  Keqin Chen, Zhao Zhang, Weili Zeng, Richong Zhang, Feng Zhu, and Rui Zhao.
  Shikra: Unleashing multimodal llm’s referential dialogue magic.
  *arXiv:2306.15195*, 2023a.
- Chen et al. (2023b)

  Lin Chen, Jisong Li, Xiaoyi Dong, Pan Zhang, Conghui He, Jiaqi Wang, Feng Zhao, and Dahua Lin.
  Sharegpt4v: Improving large multi-modal models with better captions.
  *arXiv:2311.12793*, 2023b.
- Chen et al. (2024a)

  Lin Chen, Jinsong Li, Xiaoyi Dong, Pan Zhang, Yuhang Zang, Zehui Chen, Haodong Duan, Jiaqi Wang, Yu Qiao, Dahua Lin, et al.
  Are we on the right way for evaluating large vision-language models?
  *arXiv:2403.20330*, 2024a.
- Chen et al. (2022)

  Shizhe Chen, Pierre-Louis Guhur, Makarand Tapaswi, Cordelia Schmid, and Ivan Laptev.
  Think global, act local: Dual-scale graph transformer for vision-and-language navigation.
  In *CVPR*, 2022.
- Chen et al. (2016)

  Tianqi Chen, Bing Xu, Chiyuan Zhang, and Carlos Guestrin.
  Training deep nets with sublinear memory cost.
  *arXiv:1604.06174*, 2016.
- Chen et al. (2023c)

  Zehui Chen, Weihua Du, Wenwei Zhang, Kuikun Liu, Jiangning Liu, Miao Zheng, Jingming Zhuo, Songyang Zhang, Dahua Lin, Kai Chen, et al.
  T-eval: Evaluating the tool utilization capability step by step.
  *arXiv:2312.14033*, 2023c.
- Chen et al. (2024b)

  Zhe Chen, Weiyun Wang, Hao Tian, Shenglong Ye, Zhangwei Gao, Erfei Cui, Wenwen Tong, Kongzhi Hu, Jiapeng Luo, Zheng Ma, et al.
  How far are we to gpt-4v? closing the gap to commercial multimodal models with open-source suites.
  *arXiv:2404.16821*, 2024b.
- Chen et al. (2024c)

  Zhe Chen, Weiyun Wang, Hao Tian, Shenglong Ye, Zhangwei Gao, Erfei Cui, Wenwen Tong, Kongzhi Hu, Jiapeng Luo, Zheng Ma, et al.
  Internvl2: Better than the best—expanding performance boundaries of open-source multimodal models with the progressive scaling strategy, 2024c.
  URL <https://internvl.github.io/blog/2024-07-02-InternVL-2.0>.
- Chiang et al. (2023)

  Wei-Lin Chiang, Zhuohan Li, Zi Lin, Ying Sheng, Zhanghao Wu, Hao Zhang, Lianmin Zheng, Siyuan Zhuang, Yonghao Zhuang, Joseph E. Gonzalez, Ion Stoica, and Eric P. Xing.
  Vicuna: An open-source chatbot impressing gpt-4 with 90%* chatgpt quality, 2023.
  URL <https://lmsys.org/blog/2023-03-30-vicuna/>.
- Dai et al. (2023)

  Wenliang Dai, Junnan Li, Dongxu Li, Anthony Meng Huat Tiong, Junqi Zhao, Weisheng Wang, Boyang Li, Pascale Fung, and Steven Hoi.
  Instructblip: Towards general-purpose vision-language models with instruction tuning.
  *arXiv:2305.06500*, 2023.
- Dao (2024)

  Tri Dao.
  Flashattention-2: Faster attention with better parallelism and work partitioning.
  In *ICLR*, 2024.
- Dao et al. (2022)

  Tri Dao, Daniel Y. Fu, Stefano Ermon, Atri Rudra, and Christopher Ré.
  Flashattention: Fast and memory-efficient exact attention with io-awareness.
  In *NeurIPS*, 2022.
- Dehghani et al. (2024)

  Mostafa Dehghani, Basil Mustafa, Josip Djolonga, Jonathan Heek, Matthias Minderer, Mathilde Caron, Andreas Steiner, Joan Puigcerver, Robert Geirhos, Ibrahim M Alabdulmohsin, et al.
  Patch n’pack: Navit, a vision transformer for any aspect ratio and resolution.
  In *NeurIPS*, 2024.
- Dosovitskiy et al. (2021)

  Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov, Dirk Weissenborn, Xiaohua Zhai, Thomas Unterthiner, Mostafa Dehghani, Matthias Minderer, Georg Heigold, Sylvain Gelly, Jakob Uszkoreit, and Neil Houlsby.
  An image is worth 16x16 words: Transformers for image recognition at scale.
  In *ICLR*, 2021.
- Dubey et al. (2024)

  Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad Al-Dahle, Aiesha Letman, Akhil Mathur, Alan Schelten, Amy Yang, Angela Fan, et al.
  The llama 3 herd of models.
  *arXiv:2407.21783*, 2024.
- Fang et al. (2023)

  Alex Fang, Albin Madappally Jose, Amit Jain, Ludwig Schmidt, Alexander Toshev, and Vaishaal Shankar.
  Data filtering networks.
  *arXiv:2309.17425*, 2023.
- FFmpeg-Developers (2024)

  FFmpeg-Developers.
  ffmpeg tool, 2024.
  URL <http://ffmpeg.org/>.
- Fu et al. (2023)

  Chaoyou Fu, Peixian Chen, Yunhang Shen, Yulei Qin, Mengdan Zhang, Xu Lin, Zhenyu Qiu, Wei Lin, Jinrui Yang, Xiawu Zheng, et al.
  Mme: A comprehensive evaluation benchmark for multimodal large language models.
  *arXiv:2306.13394*, 2023.
- Fu et al. (2024)

  Chaoyou Fu, Yuhan Dai, Yondong Luo, Lei Li, Shuhuai Ren, Renrui Zhang, Zihan Wang, Chenyu Zhou, Yunhang Shen, Mengdan Zhang, et al.
  Video-mme: The first-ever comprehensive evaluation benchmark of multi-modal llms in video analysis.
  *arXiv:2405.21075*, 2024.
- Guan et al. (2023)

  Tianrui Guan, Fuxiao Liu, Xiyang Wu, Ruiqi Xian, Zongxia Li, Xiaoyu Liu, Xijun Wang, Lichang Chen, Furong Huang, Yaser Yacoob, Dinesh Manocha, and Tianyi Zhou.
  Hallusionbench: An advanced diagnostic suite for entangled language hallucination & visual illusion in large vision-language models.
  *arXiv:2310.14566*, 2023.
- Hong et al. (2023)

  Wenyi Hong, Weihan Wang, Qingsong Lv, Jiazheng Xu, Wenmeng Yu, Junhui Ji, Yan Wang, Zihan Wang, Yuxiao Dong, Ming Ding, et al.
  Cogagent: A visual language model for gui agents.
  *arXiv:2312.08914*, 2023.
- Huang et al. (2023a)

  Shaohan Huang, Li Dong, Wenhui Wang, Yaru Hao, Saksham Singhal, Shuming Ma, Tengchao Lv, Lei Cui, Owais Khan Mohammed, Qiang Liu, et al.
  Language is not all you need: Aligning perception with language models.
  *arXiv:2302.14045*, 2023a.
- Huang et al. (2023b)

  Siyuan Huang, Zhengkai Jiang, Hao Dong, Yu Qiao, Peng Gao, and Hongsheng Li.
  Instruct2act: Mapping multi-modality instructions to robotic actions with large language model.
  *arXiv:2305.11176*, 2023b.
- Huang et al. (2019)

  Yanping Huang, Youlong Cheng, Ankur Bapna, Orhan Firat, Dehao Chen, Mia Xu Chen, HyoukJoong Lee, Jiquan Ngiam, Quoc V. Le, Yonghui Wu, and Zhifeng Chen.
  Gpipe: Efficient training of giant neural networks using pipeline parallelism.
  In *NeurIPS*, 2019.
- Inoue and Ohashi (2022)

  Yuki Inoue and Hiroki Ohashi.
  Prompter: Utilizing large language model prompting for a data efficient embodied instruction following.
  *arXiv:2211.03267*, 2022.
- Jiang et al. (2022)

  Yunfan Jiang, Agrim Gupta, Zichen Zhang, Guanzhi Wang, Yongqiang Dou, Yanjun Chen, Li Fei-Fei, Anima Anandkumar, Yuke Zhu, and Linxi Fan.
  Vima: General robot manipulation with multimodal prompts.
  *arXiv:2210.03094*, 2022.
- Kazemzadeh et al. (2014)

  Sahar Kazemzadeh, Vicente Ordonez, Mark Matten, and Tamara Berg.
  Referitgame: Referring to objects in photographs of natural scenes.
  In *EMNLP*, 2014.
- Kembhavi et al. (2016)

  Aniruddha Kembhavi, Mike Salvato, Eric Kolve, Minjoon Seo, Hannaneh Hajishirzi, and Ali Farhadi.
  A diagram is worth a dozen images.
  In *ECCV*, 2016.
- Kirillov et al. (2023)

  Alexander Kirillov, Eric Mintun, Nikhila Ravi, Hanzi Mao, Chloe Rolland, Laura Gustafson, Tete Xiao, Spencer Whitehead, Alexander C Berg, Wan-Yen Lo, et al.
  Segment anything.
  In *ICCV*, 2023.
- Kolve et al. (2017)

  Eric Kolve, Roozbeh Mottaghi, Winson Han, Eli VanderBilt, Luca Weihs, Alvaro Herrasti, Matt Deitke, Kiana Ehsani, Daniel Gordon, Yuke Zhu, et al.
  Ai2-thor: An interactive 3d environment for visual ai.
  *arXiv:1712.05474*, 2017.
- Korthikanti et al. (2023)

  Vijay Anand Korthikanti, Jared Casper, Sangkug Lym, Lawrence McAfee, Michael Andersch, Mohammad Shoeybi, and Bryan Catanzaro.
  Reducing activation recomputation in large transformer models.
  In *MLSys*, 2023.
- Krizhevsky et al. (2012)

  Alex Krizhevsky, Ilya Sutskever, and Geoffrey E. Hinton.
  Imagenet classification with deep convolutional neural networks.
  In *NeurIPS*, 2012.
- Lamy-Poirier (2023)

  Joel Lamy-Poirier.
  Breadth-first pipeline parallelism.
  In *MLSys*, 2023.
- Li et al. (2023a)

  Bo Li, Peiyuan Zhang, Jingkang Yang, Yuanhan Zhang, Fanyi Pu, and Ziwei Liu.
  Otterhd: A high-resolution multi-modality model.
  *arXiv:2311.04219*, 2023a.
- Li et al. (2023b)

  Chen Li, Yixiao Ge, Dian Li, and Ying Shan.
  Vision-language instruction tuning: A review and analysis.
  *arXiv:2311.08172*, 2023b.
- Li et al. (2023c)

  Junnan Li, Dongxu Li, Silvio Savarese, and Steven Hoi.
  Blip-2: Bootstrapping language-image pre-training with frozen image encoders and large language models.
  *arXiv:2301.12597*, 2023c.
- Li et al. (2024)

  Kunchang Li, Yali Wang, Yinan He, Yizhuo Li, Yi Wang, Yi Liu, Zun Wang, Jilan Xu, Guo Chen, Ping Luo, et al.
  Mvbench: A comprehensive multi-modal video understanding benchmark.
  In *CVPR*, 2024.
- Li et al. (2020)

  Shen Li, Yanli Zhao, Rohan Varma, Omkar Salpekar, Pieter Noordhuis, Teng Li, Adam Paszke, Jeff Smith, Brian Vaughan, Pritam Damania, et al.
  Pytorch distributed: Experiences on accelerating data parallel training.
  In *VLDB*, 2020.
- Li et al. (2023d)

  Zhang Li, Biao Yang, Qiang Liu, Zhiyin Ma, Shuo Zhang, Jingxu Yang, Yabo Sun, Yuliang Liu, and Xiang Bai.
  Monkey: Image resolution and text label are important things for large multi-modal models.
  *arXiv:2311.06607*, 2023d.
- Lin et al. (2023)

  Ziyi Lin, Chris Liu, Renrui Zhang, Peng Gao, Longtian Qiu, Han Xiao, Han Qiu, Chen Lin, Wenqi Shao, Keqin Chen, Jiaming Han, Siyuan Huang, Yichi Zhang, Xuming He, Hongsheng Li, and Yu Jiao Qiao.
  Sphinx: The joint mixing of weights, tasks, and visual embeddings for multi-modal large language models.
  *arXiv:2311.07575*, 2023.
- Liu et al. (2023a)

  Haotian Liu, Chunyuan Li, Yuheng Li, and Yong Jae Lee.
  Improved baselines with visual instruction tuning.
  *arXiv:2310.03744*, 2023a.
- Liu et al. (2023b)

  Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee.
  Visual instruction tuning.
  *arXiv:2304.08485*, 2023b.
- Liu et al. (2023c)

  Shilong Liu, Zhaoyang Zeng, Tianhe Ren, Feng Li, Hao Zhang, Jie Yang, Chun yue Li, Jianwei Yang, Hang Su, Jun-Juan Zhu, and Lei Zhang.
  Grounding dino: Marrying dino with grounded pre-training for open-set object detection.
  *arXiv:2303.05499*, 2023c.
- Liu et al. (2023d)

  Yuan Liu, Haodong Duan, Bo Li Yuanhan Zhang, Songyang Zhang, Wangbo Zhao, Yike Yuan, Jiaqi Wang, Conghui He, Ziwei Liu, Kai Chen, and Dahua Lin.
  Mmbench: Is your multi-modal model an all-around player?
  *arXiv:2307.06281*, 2023d.
- Liu et al. (2023e)

  Yuliang Liu, Zhang Li, Mingxin Huang, Biao Yang, Wenwen Yu, Chunyuan Li, Xucheng Yin, Cheng lin Liu, Lianwen Jin, and Xiang Bai.
  Ocrbench: On the hidden mystery of ocr in large multimodal models.
  *arXiv:2305.07895*, 2023e.
- Loshchilov and Hutter (2019)

  Ilya Loshchilov and Frank Hutter.
  Decoupled weight decay regularization.
  In *ICLR*, 2019.
- Lu et al. (2023)

  Guanxing Lu, Ziwei Wang, Changliu Liu, Jiwen Lu, and Yansong Tang.
  Thinkbot: Embodied instruction following with thought chain reasoning.
  *arXiv:2312.07062*, 2023.
- Lu et al. (2021)

  Pan Lu, Ran Gong, Shibiao Jiang, Liang Qiu, Siyuan Huang, Xiaodan Liang, and Song-Chun Zhu.
  Inter-gps: Interpretable geometry problem solving with formal language and symbolic reasoning.
  In *ACL*, 2021.
- Lu et al. (2024a)

  Pan Lu, Hritik Bansal, Tony Xia, Jiacheng Liu, Chunyuan Li, Hannaneh Hajishirzi, Hao Cheng, Kai-Wei Chang, Michel Galley, and Jianfeng Gao.
  Mathvista: Evaluating mathematical reasoning of foundation models in visual contexts.
  In *ICLR*, 2024a.
- Lu et al. (2024b)

  Quanfeng Lu, Wenqi Shao, Zitao Liu, Fanqing Meng, Boxuan Li, Botong Chen, Siyuan Huang, Kaipeng Zhang, Yu Qiao, and Ping Luo.
  Gui odyssey: A comprehensive dataset for cross-app gui navigation on mobile devices.
  *arXiv:2406.08451*, 2024b.
- Mangalam et al. (2023)

  Karttikeya Mangalam, Raiymbek Akshulakov, and Jitendra Malik.
  Egoschema: A diagnostic benchmark for very long-form video language understanding.
  In *NeurIPS*, 2023.
- Mao et al. (2016)

  Junhua Mao, Jonathan Huang, Alexander Toshev, Oana Camburu, Alan L Yuille, and Kevin Murphy.
  Generation and comprehension of unambiguous object descriptions.
  In *CVPR*, 2016.
- Masry et al. (2022)

  Ahmed Masry, Do Xuan Long, Jia Qing Tan, Shafiq Joty, and Enamul Hoque.
  Chartqa: A benchmark for question answering about charts with visual and logical reasoning.
  *arXiv:2203.10244*, 2022.
- Mathew et al. (2021)

  Minesh Mathew, Dimosthenis Karatzas, and CV Jawahar.
  Docvqa: A dataset for vqa on document images.
  In *WACV*, 2021.
- Narayanan et al. (2021)

  Deepak Narayanan, Mohammad Shoeybi, Jared Casper, Patrick LeGresley, Mostofa Patwary, Vijay Korthikanti, Dmitri Vainbrand, Prethvi Kashinkunti, Julie Bernauer, Bryan Catanzaro, Amar Phanishayee, and Matei Zaharia.
  Efficient large-scale language model training on GPU clusters using megatron-lm.
  In *SC*, 2021.
- Nvidia (2024a)

  Nvidia.
  Apex, 2024a.
  URL <https://github.com/NVIDIA/apex>.
- Nvidia (2024b)

  Nvidia.
  Cuda, 2024b.
  URL <https://developer.nvidia.com/cuda-toolkit>.
- OpenAI (2023)

  OpenAI.
  Gpt-4 technical report.
  *arXiv:2303.08774*, 2023.
- OpenAI. (2023)

  OpenAI.
  Gpt-4v(ision) system card, 2023.
  URL <https://openai.com/research/gpt-4v-system-card>.
- Openai (2024)

  Openai.
  Chatml documents, 2024.
  URL <https://github.com/openai/openai-python/blob/main/chatml.md>.
- OpenAI (2024)

  OpenAI.
  Hello gpt-4o, 2024.
  URL <https://openai.com/index/hello-gpt-4o>.
- Paszke et al. (2019)

  Adam Paszke, Sam Gross, Francisco Massa, Adam Lerer, James Bradbury, Gregory Chanan, Trevor Killeen, Zeming Lin, Natalia Gimelshein, Luca Antiga, Alban Desmaison, Andreas Köpf, Edward Z. Yang, Zachary DeVito, Martin Raison, Alykhan Tejani, Sasank Chilamkurthy, Benoit Steiner, Lu Fang, Junjie Bai, and Soumith Chintala.
  Pytorch: An imperative style, high-performance deep learning library.
  In *NeurIPS*, 2019.
- Patraucean et al. (2024)

  Viorica Patraucean, Lucas Smaira, Ankush Gupta, Adria Recasens, Larisa Markeeva, Dylan Banarse, Skanda Koppula, Mateusz Malinowski, Yi Yang, Carl Doersch, et al.
  Perception test: A diagnostic benchmark for multimodal video models.
  In *NeurIPS*, 2024.
- Qi et al. (2020)

  Yuankai Qi, Qi Wu, Peter Anderson, Xin Wang, William Yang Wang, Chunhua Shen, and Anton van den Hengel.
  Reverie: Remote embodied visual referring expression in real indoor environments.
  In *CVPR*, 2020.
- Qwen Team (2024)

  Alibaba Group Qwen Team.
  Qwen-agent framework, 2024.
  URL <https://github.com/QwenLM/Qwen-Agent>.
- Radford et al. (2021)

  Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, et al.
  Learning transferable visual models from natural language supervision.
  In *ICML*, 2021.
- Rajbhandari et al. (2020)

  Samyam Rajbhandari, Jeff Rasley, Olatunji Ruwase, and Yuxiong He.
  Zero: memory optimizations toward training trillion parameter models.
  In *SC*, 2020.
- Rawles et al. (2024a)

  Christopher Rawles, Sarah Clinckemaillie, Yifan Chang, Jonathan Waltz, Gabrielle Lau, Marybeth Fair, Alice Li, William Bishop, Wei Li, Folawiyo Campbell-Ajala, et al.
  Androidworld: A dynamic benchmarking environment for autonomous agents.
  *arXiv:2405.14573*, 2024a.
- Rawles et al. (2024b)

  Christopher Rawles, Alice Li, Daniel Rodriguez, Oriana Riva, and Timothy Lillicrap.
  Androidinthewild: A large-scale dataset for android device control.
  In *NeurIPS*, 2024b.
- Shah et al. (2024)

  Jay Shah, Ganesh Bikshandi, Ying Zhang, Vijay Thakkar, Pradeep Ramani, and Tri Dao.
  Flashattention-3: Fast and accurate attention with asynchrony and low-precision.
  *arXiv:2407.08608*, 2024.
- Shoeybi et al. (2019)

  Mohammad Shoeybi, Mostofa Patwary, Raul Puri, Patrick LeGresley, Jared Casper, and Bryan Catanzaro.
  Megatron-lm: Training multi-billion parameter language models using model parallelism.
  *arXiv:1909.08053*, 2019.
- Shridhar et al. (2020a)

  Mohit Shridhar, Jesse Thomason, Daniel Gordon, Yonatan Bisk, Winson Han, Roozbeh Mottaghi, Luke Zettlemoyer, and Dieter Fox.
  Alfred: A benchmark for interpreting grounded instructions for everyday tasks.
  In *CVPR*, 2020a.
- Shridhar et al. (2020b)

  Mohit Shridhar, Xingdi Yuan, Marc-Alexandre Côté, Yonatan Bisk, Adam Trischler, and Matthew Hausknecht.
  Alfworld: Aligning text and embodied environments for interactive learning.
  *arXiv:2010.03768*, 2020b.
- Sigurdsson et al. (2023)

  Gunnar A Sigurdsson, Jesse Thomason, Gaurav S Sukhatme, and Robinson Piramuthu.
  Rrex-bot: Remote referring expressions with a bag of tricks.
  In *IROS*, 2023.
- Singh et al. (2019)

  Amanpreet Singh, Vivek Natarajan, Meet Shah, Yu Jiang, Xinlei Chen, Dhruv Batra, Devi Parikh, and Marcus Rohrbach.
  Towards vqa models that can read.
  In *CVPR*, 2019.
- Srinivasan et al. (2023)

  Venkat Krishna Srinivasan, Zhen Dong, Banghua Zhu, Brian Yu, Damon Mosk-Aoyama, Kurt Keutzer, Jiantao Jiao, and Jian Zhang.
  Nexusraven: a commercially-permissive language model for function calling.
  In *NeurIPS Workshop*, 2023.
- Su (2021)

  Jianlin Su.
  Transformer upgrade path: 4. rotary position encoding for two-dimensional positions, 2021.
  URL <https://www.spaces.ac.cn/archives/8397>.
- Su (2024)

  Jianlin Su.
  Transformer upgrade path: 17. insights into multimodal positional encoding, 2024.
  URL <https://spaces.ac.cn/archives/10040>.
- Su et al. (2024)

  Jianlin Su, Murtadha Ahmed, Yu Lu, Shengfeng Pan, Wen Bo, and Yunfeng Liu.
  Roformer: Enhanced transformer with rotary position embedding.
  In *Neurocomputing*, 2024.
- Tang et al. (2024)

  Jingqun Tang, Qi Liu, Yongjie Ye, Jinghui Lu, Shu Wei, Chunhui Lin, Wanqing Li, Mohamad Fitri Faiz Bin Mahmood, Hao Feng, Zhen Zhao, Yanjie Wang, Yuliang Liu, Hao Liu, Xiang Bai, and Can Huang.
  Mtvqa: Benchmarking multilingual text-centric visual question answering.
  *arXiv:2405.11985*, 2024.
- Team et al. (2023)

  Gemini Team, Rohan Anil, Sebastian Borgeaud, Yonghui Wu, Jean-Baptiste Alayrac, Jiahui Yu, Radu Soricut, Johan Schalkwyk, Andrew M Dai, Anja Hauth, et al.
  Gemini: A family of highly capable multimodal models.
  *arXiv:2312.11805*, 2023.
- Touvron et al. (2023a)

  Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timothée Lacroix, Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal Azhar, et al.
  Llama: Open and efficient foundation language models.
  *arXiv:2302.13971*, 2023a.
- Touvron et al. (2023b)

  Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, et al.
  Llama 2: Open foundation and fine-tuned chat models.
  *arXiv:2307.09288*, 2023b.
- Wang et al. (2024)

  Ke Wang, Junting Pan, Weikang Shi, Zimu Lu, Mingjie Zhan, and Hongsheng Li.
  Measuring multimodal mathematical reasoning with math-vision dataset.
  *arXiv:2402.14804*, 2024.
- Wang et al. (2022)

  Peng Wang, An Yang, Rui Men, Junyang Lin, Shuai Bai, Zhikang Li, Jianxin Ma, Chang Zhou, Jingren Zhou, and Hongxia Yang.
  Ofa: Unifying architectures, tasks, and modalities through a simple sequence-to-sequence learning framework.
  In *ICML*, 2022.
- Wang et al. (2023a)

  Peng Wang, Shijie Wang, Junyang Lin, Shuai Bai, Xiaohuan Zhou, Jingren Zhou, Xinggang Wang, and Chang Zhou.
  One-peace: Exploring one general representation model toward unlimited modalities.
  *arXiv:2305.11172*, 2023a.
- Wang et al. (2023b)

  Weihan Wang, Qingsong Lv, Wenmeng Yu, Wenyi Hong, Ji Qi, Yan Wang, Junhui Ji, Zhuoyi Yang, Lei Zhao, Xixuan Song, et al.
  Cogvlm: Visual expert for pretrained language models.
  *arXiv:2311.03079*, 2023b.
- X.AI (2024a)

  X.AI.
  Grok-1.5 vision preview.
  <https://x.ai/blog/grok-1.5v>, 2024a.
- X.AI (2024b)

  X.AI.
  Grok-2 beta release.
  <https://x.ai/blog/grok-2>, 2024b.
- Yan et al. (2023)

  B. Yan, Yi Jiang, Jiannan Wu, D. Wang, Ping Luo, Zehuan Yuan, and Huchuan Lu.
  Universal instance perception as object discovery and retrieval.
  In *CVPR*, 2023.
- Yan et al. (2024)

  Fanjia Yan, Huanzhi Mao, Charlie Cheng-Jie Ji, Tianjun Zhang, Shishir G. Patil, Ion Stoica, and Joseph E. Gonzalez.
  Berkeley function calling leaderboard, 2024.
  URL <https://gorilla.cs.berkeley.edu/blogs/8_berkeley_function_calling_leaderboard.html>.
- Yang et al. (2024)

  An Yang, Baosong Yang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang Zhou, Chengpeng Li, Chengyuan Li, Dayiheng Liu, Fei Huang, et al.
  Qwen2 technical report.
  *arXiv:2407.10671*, 2024.
- Yang et al. (2023)

  Zhengyuan Yang, Linjie Li, Kevin Lin, Jianfeng Wang, Chung-Ching Lin, Zicheng Liu, and Lijuan Wang.
  The dawn of lmms: Preliminary explorations with gpt-4v (ision).
  *arXiv:2309.17421*, 2023.
- Yao et al. (2024)

  Yuan Yao, Tianyu Yu, Ao Zhang, Chongyi Wang, Junbo Cui, Hongji Zhu, Tianchi Cai, Haoyu Li, Weilin Zhao, Zhihui He, et al.
  Minicpm-v: A gpt-4v level mllm on your phone.
  *arXiv:2408.01800*, 2024.
- Ye et al. (2023a)

  Qinghao Ye, Haiyang Xu, Guohai Xu, Jiabo Ye, Ming Yan, Yiyang Zhou, Junyang Wang, Anwen Hu, Pengcheng Shi, Yaya Shi, et al.
  mplug-owl: Modularization empowers large language models with multimodality.
  *arXiv:2304.14178*, 2023a.
- Ye et al. (2023b)

  Qinghao Ye, Haiyang Xu, Jiabo Ye, Ming Yan, Haowei Liu, Qi Qian, Ji Zhang, Fei Huang, and Jingren Zhou.
  mplug-owl2: Revolutionizing multi-modal large language model with modality collaboration.
  *arXiv:2311.04257*, 2023b.
- Ying et al. (2024)

  Kaining Ying, Fanqing Meng, Jin Wang, Zhiqian Li, Han Lin, Yue Yang, Hao Zhang, Wenbo Zhang, Yuqi Lin, Shuo Liu, Jiayi Lei, Quanfeng Lu, Runjian Chen, Peng Xu, Renrui Zhang, Haozhe Zhang, Peng Gao, Yali Wang, Yu Qiao, Ping Luo, Kaipeng Zhang, and Wenqi Shao.
  Mmt-bench: A comprehensive multimodal benchmark for evaluating large vision-language models towards multitask agi.
  *arXiv:2404.16006*, 2024.
- Yu et al. (2024)

  Weihao Yu, Zhengyuan Yang, Linjie Li, Jianfeng Wang, Kevin Lin, Zicheng Liu, Xinchao Wang, and Lijuan Wang.
  Mm-vet: Evaluating large multimodal models for integrated capabilities.
  In *ICML*, 2024.
- Yue et al. (2023)

  Xiang Yue, Yuansheng Ni, Kai Zhang, Tianyu Zheng, Ruoqi Liu, Ge Zhang, Samuel Stevens, Dongfu Jiang, Weiming Ren, Yuxuan Sun, et al.
  Mmmu: A massive multi-discipline multimodal understanding and reasoning benchmark for expert agi.
  *arXiv:2311.16502*, 2023.
- Yue et al. (2024)

  Xiang Yue, Tianyu Zheng, Yuansheng Ni, Yubo Wang, Kai Zhang, Shengbang Tong, Yuxuan Sun, Ming Yin, Botao Yu, Ge Zhang, et al.
  Mmmu-pro: A more robust multi-discipline multimodal understanding benchmark.
  *arXiv preprint arXiv:2409.02813*, 2024.
- Zhai et al. (2024)

  Yuexiang Zhai, Hao Bai, Zipeng Lin, Jiayi Pan, Shengbang Tong, Yifei Zhou, Alane Suhr, Saining Xie, Yann LeCun, Yi Ma, et al.
  Fine-tuning large vision-language models as decision-making agents via reinforcement learning.
  *arXiv:2405.10292*, 2024.
- Zhan and Zhang (2023)

  Zhuosheng Zhan and Aston Zhang.
  You only look at screens: Multimodal chain-of-action agents.
  *arXiv:2309.11436*, 2023.
- Zhang and Sennrich (2019)

  Biao Zhang and Rico Sennrich.
  Root mean square layer normalization.
  In *NeurIPS*, 2019.
- Zhang et al. (2024a)

  Haotian Zhang, Haoxuan You, Philipp Dufter, Bowen Zhang, Chen Chen, Hong-You Chen, Tsu-Jui Fu, William Yang Wang, Shih-Fu Chang, Zhe Gan, and Yinfei Yang.
  Ferret-v2: An improved baseline for referring and grounding with large language models.
  *arXiv:2404.07973*, 2024a.
- Zhang et al. (2024b)

  Jiwen Zhang, Jihao Wu, Yihua Teng, Minghui Liao, Nuo Xu, Xiao Xiao, Zhongyu Wei, and Duyu Tang.
  Android in the zoo: Chain-of-action-thought for gui agents.
  *arXiv:2403.02713*, 2024b.
- Zhang et al. (2023)

  Pan Zhang, Xiaoyi Dong Bin Wang, Yuhang Cao, Chao Xu, Linke Ouyang, Zhiyuan Zhao, Shuangrui Ding, Songyang Zhang, Haodong Duan, Hang Yan, et al.
  Internlm-xcomposer: A vision-language large model for advanced text-image comprehension and composition.
  *arXiv:2309.15112*, 2023.
- Zhang et al. (2024c)

  Tianyu Zhang, Suyuchen Wang, Lu Li, Ge Zhang, Perouz Taslakian, Sai Rajeswar, Jie Fu, Bang Liu, and Yoshua Bengio.
  Vcr: Visual caption restoration.
  *arXiv:2406.06462*, 2024c.
- Zhu et al. (2023)

  Deyao Zhu, Jun Chen, Xiaoqian Shen, Xiang Li, and Mohamed Elhoseiny.
  Minigpt-4: Enhancing vision-language understanding with advanced large language models.
  *arXiv:2304.10592*, 2023.

## 附录 A 模型能力与定性示例

在本节中，我们展示 Qwen2-VL 的一些实际示例。

### A.1 通用对话与 OCR

Qwen2-VL 模型如今更擅长准确描述与识别图像中的复杂信息，并能提供详细的背景说明并回答相关问题。此外，Qwen2-VL 模型的文本处理能力也得到显著提升，尤其是在识别图像中的中文与英文文本方面。

多目标识别
![Refer to caption](2409.12191v2/images/qwen2-vl/boxes.png)
Output the color and number of each box.

模型回复

The image shows a stack of colorful blocks with numbers on them. Here is the color and number of each block from top to bottom:
- Top row (single block): Blue with the number 9
- Second row (two blocks): Light blue with the number 7, and green with the number 8
- Third row (three blocks): Purple with the number 4, pink with the number 5, and light green with the number 6
- Bottom row (four blocks): Red with the number 0, orange with the number 1, yellow with the number 2, and light green with the number 3

图 7：当呈现一张不同颜色立方体的图像时，模型识别出它们的布局以及每个立方体的颜色。

植物识别
![Refer to caption](2409.12191v2/images/qwen2-vl/flowers.jpg)
What kind of flower is this?

模型回复

The flowers in the picture are forget-me-nots (Myosotis). These small, delicate flowers are known for their vibrant colors, typically blue, pink, or white, and are often used in bouquets and gardens for their charming appearance.

图 8：模型展示了识别照片中花卉的高超能力。

含密集公式的文档解析
![Refer to caption](2409.12191v2/images/qwen2-vl/arxiv_sample.png)
Convert the content in the image to Markdown

模型回复

1. If i>0i>0, let d¯′′:=(i−1,d−i−l+1,l)\underline{d}^{\prime\prime}:=(i-1,d-i-l+1,l). Let Vd¯V_{\underline{d}} and Vd¯′′V_{\underline{d}^{\prime\prime}} be r+1r+1-dimensional subspaces of H0​(ℒd¯)H^{0}(\mathcal{L}_{\underline{d}}) and H0​(ℒd¯′′)H^{0}(\mathcal{L}_{\underline{d}^{\prime\prime}}), respectively, such that φd¯,d¯′′​(Vd¯)=Vd¯′′X1,0\varphi_{\underline{d},\underline{d}^{\prime\prime}}(V_{\underline{d}})=V_{\underline{d}^{\prime\prime}}^{X_{1},0}. Then the distributivity holds in Vd¯′′V_{\underline{d}^{\prime\prime}} if and only if

dim(Vd¯X2,0+Vd¯X3,0)−dim(Vd¯′′X2,0+Vd¯′′X3,0)=r+1−dim(Vd¯′′X1,0+Vd¯′′X2,0+Vd¯′′X3,0)\dim(V_{\underline{d}}^{X_{2},0}+V_{\underline{d}}^{X_{3},0})-\dim(V_{\underline{d}^{\prime\prime}}^{X_{2},0}+V_{\underline{d}^{\prime\prime}}^{X_{3},0})=r+1-\dim(V_{\underline{d}^{\prime\prime}}^{X_{1},0}+V_{\underline{d}^{\prime\prime}}^{X_{2},0}+V_{\underline{d}^{\prime\prime}}^{X_{3},0})
2. If i+l≤d−1i+l\leq d-1, let d¯′′′:=(i,d−i−l−1,l+1)\underline{d}^{\prime\prime\prime}:=(i,d-i-l-1,l+1). Let Vd¯V_{\underline{d}} and Vd¯′′′V_{\underline{d}^{\prime\prime\prime}} be r+1r+1-dimensional subspaces of H0​(ℒd¯)H^{0}(\mathcal{L}_{\underline{d}}) and H0​(ℒd¯′′′)H^{0}(\mathcal{L}_{\underline{d}^{\prime\prime\prime}}), respectively, such that φd¯′′′,d¯​(Vd¯′′′)=Vd¯X3,0\varphi_{\underline{d}^{\prime\prime\prime},\underline{d}}(V_{\underline{d}^{\prime\prime\prime}})=V_{\underline{d}}^{X_{3},0}. Then the distributivity holds in Vd¯V_{\underline{d}} if and only if

dim(Vd¯′′′X1,0+Vd¯′′′X2,0)−dim(Vd¯X1,0+Vd¯X2,0)=r+1−dim(Vd¯X1,0+Vd¯X2,0+Vd¯X3,0),\dim(V_{\underline{d}^{\prime\prime\prime}}^{X_{1},0}+V_{\underline{d}^{\prime\prime\prime}}^{X_{2},0})-\dim(V_{\underline{d}}^{X_{1},0}+V_{\underline{d}}^{X_{2},0})=r+1-\dim(V_{\underline{d}}^{X_{1},0}+V_{\underline{d}}^{X_{2},0}+V_{\underline{d}}^{X_{3},0}),
where the maps φd¯,d¯′′\varphi_{\underline{d},\underline{d}^{\prime\prime}} and φd¯′′′,d¯\varphi_{\underline{d}^{\prime\prime\prime},\underline{d}} in Proposition 3.14 are the maps linking the corresponding sheaves. Another important result is Proposition 3.16, which establishes an inequality for any exact limit linear series. Specifically, our Proposition 3.16 says:
Let {(ℒd¯,Vd¯)}d¯\{(\mathcal{L}_{\underline{d}},V_{\underline{d}})\}_{\underline{d}} be an exact limit linear series of degree dd and dimension rr. Then

∑d¯dim(Vd¯Vd¯X1,0+Vd¯X2,0+Vd¯X3,0)≥r+1.\sum_{\underline{d}}\dim\left(\frac{V_{\underline{d}}}{V_{\underline{d}}^{X_{1},0}+V_{\underline{d}}^{X_{2},0}+V_{\underline{d}}^{X_{3},0}}\right)\geq r+1.
As a consequence of Proposition 3.14 and Proposition 3.16, in Corollary 3.17, we get the following characterization of exact limit linear series satisfying the distributivity at each multidegree:
Let {(ℒd¯,Vd¯)}d¯\{(\mathcal{L}_{\underline{d}},V_{\underline{d}})\}_{\underline{d}} be an exact limit linear series of degree dd and dimension rr. Then

∑d¯dim(Vd¯Vd¯X1,0+Vd¯X2,0+Vd¯X3,0)=r+1\sum_{\underline{d}}\dim\left(\frac{V_{\underline{d}}}{V_{\underline{d}}^{X_{1},0}+V_{\underline{d}}^{X_{2},0}+V_{\underline{d}}^{X_{3},0}}\right)=r+1
if and only if the distributivity holds in Vd¯V_{\underline{d}} for any d¯\underline{d}.
In Section 3, we also study simple limit linear series. In Proposition 3.18, we characterize the multidegrees which determine all simple bases. In Proposition 3.20, following the construction in Muñoz [5], Proposition 4.4, we present a certain structure of linearly independent sections for any exact limit linear series satisfying the distributivity property. In propositions 3.21 and 3.22, we obtain some properties of that structure. These properties imply the existence of a simple basis (we give a proof of that in Proposition 3.23).
We conclude Section 3 with a characterization of simple limit linear series among the exact limit linear series. Specifically, our Corollary 3.24 says:
Let {(ℒd¯,Vd¯)}d¯\{(\mathcal{L}_{\underline{d}},V_{\underline{d}})\}_{\underline{d}} be an exact limit linear series of degree dd and dimension rr. Then the following statements are equivalent:
1. {(ℒd¯,Vd¯)}d¯\{(\mathcal{L}_{\underline{d}},V_{\underline{d}})\}_{\underline{d}} is simple.
2. ∑d¯dim(Vd¯Vd¯X1,0+Vd¯X2,0+Vd¯X3,0)=r+1\sum_{\underline{d}}\dim\left(\frac{V_{\underline{d}}}{V_{\underline{d}}^{X_{1},0}+V_{\underline{d}}^{X_{2},0}+V_{\underline{d}}^{X_{3},0}}\right)=r+1.
3. The distributivity holds in Vd¯V_{\underline{d}} for any d¯\underline{d}.
In a subsequent work, given a refined limit linear series, we will construct all simple extensions by combining our Proposition 3.14 and the method of Muñoz [6] for the construction of all exact extensions.

图 9：基于视觉刺激的多语言文学写作。

多语言文本识别
![Refer to caption](2409.12191v2/images/qwen2-vl/screenshot_multilingual4.png)
转录图中内容，并识别图中每段内容的语言。
(Translation: Transcribe the picture and identify the language of each paragraph in it.)

模型回复

1. 汉语，也称为“华语”。是中国使用人数最多的语言，也是世界上作为第一语言使用人数最多的语言。是中华优秀传统文化的重要载体。繁体字，又稱為“繁體中文”，與“簡化字”/“簡體字”相對。一般是指漢字簡化運動被簡化字所代替的漢字。
- 语言：中文
2. 日本語は地方ごとに多様な方言があり、とりわけ琉球諸島で方言差が著しい。
- 语言：日语
3. 한국어(韓國語), 조선말(朝鮮말)는 대한민국과 조선민주주의인민공화국의 공용어이다. 둘은 표기나 문법에서는 차이가 없지만 동사 어미나 표현에서 차이가 있다.
- 语言：韩语
4. Le français est une langue indo-européenne de la famille des langues romanes dont les locuteurs sont appelés « francophones ».
- 语言：法语
5. El español o castellano es una lengua romance procedente del latín hablado, perteneciente a la familia de lenguas indoeuropeas.
- 语言：西班牙语
6. A língua portuguesa, também designada português, é uma língua indo-europeia românica flexiva ocidental originada no galego-português falado no Reino da Galiza e no norte de Portugal.
- 语言：葡萄牙语
7. Is ceann de na teangacha Ceilteacha í an Ghaeilge (nó Gaeilge na hÉireann mar a thugtar uirthi corruair), agus ceann de na trí cinn de theangacha Ceilteacha ar a dtugtar na teangacha Gaelacha (Gaeilge, Gaeilge Mhanann agus Gaeilge na hAlban) go háirithe.
- 语言：爱尔兰语
8. English is a West Germanic language in the Indo-European language family, whose speakers, called Anglophones, originated in early medieval England on the island of Great Britain.
- 语言：英语
9. Die deutsche Sprache bzw. Deutsch ist eine westgermanische Sprache, die weltweit etwa 90 bis 105 Millionen Menschen als Muttersprache und weiteren rund 80 Millionen als Zweit- oder Fremdsprache dient.
- 语言：德语
10. Język polski, polszczyzna — język z grupy zachodniosłowiańskiej (do której należą również czeski, kaszubski, słowacki, języki łużyckie czy wymarły język drzewiański), stanowiącej część rodziny indoeuropejskiej.
- 语言：波兰语
11. \acctonos \acctonosςς \acctonos ς \accdialytika\acctonos \acctonos \acctonos µ\acctonos µ\acctonos \acctonos \acctonos.
- 语言：希腊语
12. Tiếng Việt hay Việt ngữ là một ngôn ngữ thuộc ngữ hệ Nam Á, được công nhận là ngôn ngữ chính thức tại Việt Nam.
- 语言：越南语
13. .
- 语言：蒙古语
- 语言：俄语
16. Kiswahili ni lugha ya Kibantu yenye misamiati mingi ya Kiarabu (35%), lakini sasa ya Kiingereza pia (10%), inayozungumzwa katika eneo kubwa la Afrika ya Mashariki.
- 语言：斯瓦希里语

图 10：模型展示了识别图像中多语言文本的高超能力。

文本信息识别与处理
![Refer to caption](2409.12191v2/images/4_text_information_1.jpeg)
Translate all the text in the picture into English and standardize the format

模型回复

The text in the image reads:
Learning Prompt
Guo Moruo’s collection of poems, ”The Goddess”, is a representative work of modern Chinese poetry. It expresses new content and forms, embodying the spirit of the May Fourth Movement. ”Standing on the Edge of the Earth” is a representative poem from ”The Goddess”. The poet imagines standing on the edge of the earth to observe it from all angles, shouting and singing, imagining the surging clouds, magnificent Arctic ice, and violent Pacific Ocean, praising the power to destroy the old world and create a new life. This poem embodies the free, and bold spirit of the May Fourth Movement. When reading, pay attention to connecting with the specific context of the May Fourth Movement to understand the content and form of this poem.

Wen Yiduo’s ”Red Candle” uses the classical image of ”candle” to give it a new meaning, praising the red candle for its dedication to lighting up the world. Pay attention to how the poet uses the dialogue between ”red candle” and ”red candle” to express the confusion and hope of youth, as well as the firm pursuit of ideals. The use of fantasy and emotional rhetoric, the use of rhetorical devices such as alliteration and assonance, and the formation of rhythmic beauty through the arrangement of long and short sentences in the poem are also important aspects to appreciate.

Chang Yao’s ”Snow Capped Peak on the Side of the Sun” is rich in content. When reading, pay attention to the development of imagination and taste the heavy and majestic atmosphere created by the images of ”snow-capped peak”, ”sun”, and ”spider”. Feel the powerful contained in it.

Shelley’s ”To a Skylark” has profound implications and novel imagery. Pay attention to the poet’s emotions and understand the symbolic meaning of the skylark. Grasp the characteristics of the interlocking between sections of the work and appreciate the poet’s use of bold and flexible imagery.

When learning this group of poems, rely more on reading aloud to clarify the emotional context of the poem and grasp the connotation of the image. Feel the emotions expressed by the poet and understand the use of symbolism.

图 11：密集中文文本的识别。模型能够将冗长、紧密排列的汉字准确而流畅地直接转换为标准英文。

多语言文本识别
![Refer to caption](2409.12191v2/images/qwen2-vl/multilingual_2.png)
What is the text?

模型回复

The text on the wall is in Portuguese and reads: “não é normal ter medo de andar sozinha na rua!!!” This translates to: “It is not normal to be afraid to walk alone on the street!!!”

图 12：模型展示了识别图像中多语言文本的高超能力。图像来源：([Yang et al., 2023](#bib.bib105))

多语言文本识别
![Refer to caption](2409.12191v2/images/qwen2-vl/Handwritten_chinese.jpeg)
识别图中所有文字，无需添加标点。
(Translation: Recognize all the text in the image without adding punctuation.)

模型回复

尊敬的老师
展信舒颜
气温骤降
树叶无声无息的掉落
教诲如春风
师恩深似海
愿温馨、喜悦与幸福
如同吐露芬芳的花朵
永远洋溢在您幸福的时光里

图 13：模型展示了识别图像中多语言文本的高超能力。

### A.2 信息抽取与视觉推理

Qwen2-VL 模型的一项显著进步是其增强的视觉推理能力。这一进步使模型能够解释并理解诸如流程图、示意图等复杂表示以及其他符号系统。

数学问题求解
![Refer to caption](2409.12191v2/images/2-1-triangle.jpg)
Find the length of A​CAC in the isosceles triangle A​B​CABC.

模型回复

Since triangle A​B​CABC is isosceles, we know that A​C=B​CAC=BC. Therefore, we can set the expressions for A​CAC and B​CBC equal to each other and solve for xx
4​x+1=5​x−0.54x+1=5x-0.5
Subtracting 4​x4x from both sides, we get:
1=x−0.51=x-0.5
Adding 0.50.5 to both sides, we get:
1.5=x1.5=x
Now that we know the value of xx, we can substitute it back into the expression for A​CAC to find its length:
A​C=4​x+1AC=4x+1
A​C=4​(1.5)+1AC=4(1.5)+1
A​C=6+1AC=6+1
A​C=7AC=7
Therefore, the length of A​CAC is 77.

图 14：模型展示了求解数学问题的高超能力。图像来源：[Lu et al. (2021)](#bib.bib60)

数学问题求解
![Refer to caption](2409.12191v2/images/3_1_math_cube_2x.jpg)
Read the image and solve it step by step.

模型回复

The image shows two geometric figures, a rectangular prism and a cube, with their dimensions labeled. The problem asks to calculate the surface area and volume of these figures.

1.For the rectangular prism:
Length (l) = 4 cm
Width (w) = 2 cm
Height (h) = 3 cm
Surface Area (SA) of a rectangular prism = 2lw + 2lh + 2wh
Volume (V) of a rectangular prism = lwh
Substituting the given values:
SA = 2(4cm)(2cm) + 2(4cm)(3cm) + 2(2cm)(3cm)
SA = 16cm² + 24cm² + 12cm² SA = 52cm²
V = (4cm)(2cm)(3cm) V = 24cm³

2.For the cube:
Side length (a) = 3 dm
Surface Area (SA) of a cube = 6a² Volume (V) of a cube = a³
Substituting the given value:
SA = 6(3dm)² SA = 6(9dm²) SA = 54dm²
V = (3dm)³ V = 27dm³

So, the surface area and volume for each figure are as follows:
For the rectangular prism:
Surface Area = 52 cm²
Volume = 24 cm³

For the cube:
Surface Area = 54 dm²
Volume = 27 dm³

图 15：求解数学问题。模型以逐步讲解的方式计算出这些图形的表面积与体积。

算法问题求解
![[Uncaptioned image]](2409.12191v2/images/2-2-Code.jpeg)
Solve the algorithmic problem in the web page.

模型回复

To solve the “Snake in Matrix” problem, we need to implement a function that takes the size of the matrix nn and a list of commands, and returns the final position of the snake after executing all the commands. Here’s a step-by-step approach to solve this problem:

1.

Initialize Variables:

—

Initialize the current position of the snake as 00.
—

Initialize the direction of the snake as RIGHT (initially, the snake moves to the right).
2.

Define Movement Functions:

—

Create a function to move the snake based on the current direction and the size of the matrix nn.
—

Update the position of the snake accordingly.
3.

Process Commands:

—

Iterate through each command in the list of commands.
—

For each command, update the direction and position of the snake.
4.

Return Final Position:

—

After processing all commands, return the final position of the snake.
Here’s the Python code to implement the solution:
[⬇](data:text/plain;base64,Y2xhc3MgU29sdXRpb246CiAgICBkZWYgZmluYWxQb3NpdGlvbk9mU25ha2Uoc2VsZiwgbjogaW50LCBjb21tYW5kczogTGlzdFtzdHJdKSAtPiBpbnQ6CiAgICAgICAgIyBJbml0aWFsaXplIHZhcmlhYmxlcwogICAgICAgIHBvc2l0aW9uID0gMAogICAgICAgIGRpcmVjdGlvbiA9ICJSSUdIVCIKICAgICAgICAjIERlZmluZSBtb3ZlbWVudCBmdW5jdGlvbnMKICAgICAgICBkZWYgbW92ZV9yaWdodCgpOgogICAgICAgICAgICBub25sb2NhbCBwb3NpdGlvbgogICAgICAgICAgICBwb3NpdGlvbiArPSAxCiAgICAgICAgZGVmIG1vdmVfZG93bigpOgogICAgICAgICAgICBub25sb2NhbCBwb3NpdGlvbgogICAgICAgICAgICBwb3NpdGlvbiArPSBuCiAgICAgICAgZGVmIG1vdmVfbGVmdCgpOgogICAgICAgICAgICBub25sb2NhbCBwb3NpdGlvbgogICAgICAgICAgICBwb3NpdGlvbiAtPSAxCiAgICAgICAgZGVmIG1vdmVfdXAoKToKICAgICAgICAgICAgbm9ubG9jYWwgcG9zaXRpb24KICAgICAgICAgICAgcG9zaXRpb24gLT0gbgogICAgICAgICMgUHJvY2VzcyBjb21tYW5kcwogICAgICAgIGZvciBjb21tYW5kIGluIGNvbW1hbmRzOgogICAgICAgICAgICBpZiBjb21tYW5kID09ICJSSUdIVCI6CiAgICAgICAgICAgICAgICBtb3ZlX3JpZ2h0KCkKICAgICAgICAgICAgZWxpZiBjb21tYW5kID09ICJET1dOIjoKICAgICAgICAgICAgICAgIG1vdmVfZG93bigpCiAgICAgICAgICAgIGVsaWYgY29tbWFuZCA9PSAiTEVGVCI6CiAgICAgICAgICAgICAgICBtb3ZlX2xlZnQoKQogICAgICAgICAgICBlbGlmIGNvbW1hbmQgPT0gIlVQIjoKICAgICAgICAgICAgICAgIG1vdmVfdXAoKQogICAgICAgICMgUmV0dXJuIGZpbmFsIHBvc2l0aW9uCiAgICAgICAgcmV0dXJuIHBvc2l0aW9u)
class Solution:
 def finalPositionOfSnake(self, n: int, commands: List[str]) -> int:
 # Initialize variables
 position = 0
 direction = "RIGHT"
 # Define movement functions
 def move_right():
 nonlocal position
 position += 1
 def move_down():
 nonlocal position
 position += n
 def move_left():
 nonlocal position
 position -= 1
 def move_up():
 nonlocal position
 position -= n
 # Process commands
 for command in commands:
 if command == "RIGHT":
 move_right()
 elif command == "DOWN":
 move_down()
 elif command == "LEFT":
 move_left()
 elif command == "UP":
 move_up()
 # Return final position
 return position
This code defines a class Solution with a method finalPositionOfSnake that takes the size of the matrix nn and a list of commands, and returns the final position of the snake after executing all the commands. The movement functions (move_right, move_down, move_left, move_up) are used to update the position of the snake based on the current direction.

图 16：模型展示了求解算法问题的高超能力。

网页内容识别
![Refer to caption](2409.12191v2/images/2-3-screenshot1.png)
Extract all page titles in the screenshot of search result.

模型回复

The page titles in the screenshot of the search result are:

1.

你好，Qwen2
2.

QwenLM/Qwen2
3.

Qwen2 - a Qwen Collection
4.

快速开始
5.

Qwen2-7B
6.

Qwen2-Math，新一代数学模型
7.

Qwen
8.

Qwen/Qwen2-7B-Instruct
9.

[2407.10671] Qwen2 Technical Report
10.

qwen2

图 17：模型展示了识别网页内容的高超能力。

OCR 与数学问题求解
![Refer to caption](2409.12191v2/images/2-4-math1.jpg)
Please tell me how many days are between Ruka’s birthday and Yuki’s birthday? Think carefully step by step.

模型回复

To determine the number of days between Ruka’s and Yuki’s birthdays, we need to calculate the difference between their respective birth dates.

1.

Ruka’s birthday is on June 24.
2.

Yuki’s birthday is on September 17.
Let’s break it down step by step:

1.

From June 24 to June 30:

—

June 24 to June 30 is 6 days.
2.

From July 1 to August 31:

—

July has 31 days.
—

August has 31 days.
—

Total days in July and August: 31 + 31 = 62 days.
3.

From September 1 to September 17:

—

September 1 to September 17 is 17 days.
Now, we add all these days together:

—

June 24 to June 30: 6 days
—

July 1 to August 31: 62 days
—

September 1 to September 17: 17 days
Total days = 6 + 62 + 17 = 85 days
Therefore, there are 85 days between Ruka’s and Yuki’s birthdays.

图 18：模型展示了 OCR 与数学推理的高超能力。

OCR 与格式遵循
![Refer to caption](2409.12191v2/images/2-5-information_extraction.jpg)
What are the Linux versions and their release dates in the picture? Return results as a JSON list.

模型回复

[⬇](data:text/plain;base64,WwogIHsKICAgICJ2ZXJzaW9uIjogIjYuMTEtcmMzIiwgInJlbGVhc2VfZGF0ZSI6ICIyMDI0LTA4LTExIgogIH0sCiAgewogICAgInZlcnNpb24iOiAiNi4xMC40IiwgInJlbGVhc2VfZGF0ZSI6ICIyMDI0LTA4LTExIgogIH0sCiAgewogICAgInZlcnNpb24iOiAiNi45LjEyIFtFT0xdIiwgInJlbGVhc2VfZGF0ZSI6ICIyMDI0LTA3LTI3IgogIH0sCiAgewogICAgInZlcnNpb24iOiAiNi42LjQ1IiwgInJlbGVhc2VfZGF0ZSI6ICIyMDI0LTA4LTExIgogIH0sCiAgewogICAgInZlcnNpb24iOiAiNi4xLjEwNCIsICJyZWxlYXNlX2RhdGUiOiAiMjAyNC0wOC0xMSIKICB9LAogIHsKICAgICJ2ZXJzaW9uIjogIjUuMTUuMTY0IiwgInJlbGVhc2VfZGF0ZSI6ICIyMDI0LTA3LTI3IgogIH0sCiAgewogICAgInZlcnNpb24iOiAiNS4xMC4yMjMiLCAicmVsZWFzZV9kYXRlIjogIjIwMjQtMDctMjciCiAgfSwKICB7CiAgICAidmVyc2lvbiI6ICI1LjQuMjgxIiwgInJlbGVhc2VfZGF0ZSI6ICIyMDI0LTA3LTI3IgogIH0sCiAgewogICAgInZlcnNpb24iOiAiNC4xOS4zMTkiLCAicmVsZWFzZV9kYXRlIjogIjIwMjQtMDctMjciCiAgfSwKICB7CiAgICAidmVyc2lvbiI6ICJuZXh0LTIwMjQwODEyIiwgInJlbGVhc2VfZGF0ZSI6ICIyMDI0LTA4LTEyIgogIH0KXQ==)
[
 {
 "version": "6.11-rc3", "release_date": "2024-08-11"
 },
 {
 "version": "6.10.4", "release_date": "2024-08-11"
 },
 {
 "version": "6.9.12 [EOL]", "release_date": "2024-07-27"
 },
 {
 "version": "6.6.45", "release_date": "2024-08-11"
 },
 {
 "version": "6.1.104", "release_date": "2024-08-11"
 },
 {
 "version": "5.15.164", "release_date": "2024-07-27"
 },
 {
 "version": "5.10.223", "release_date": "2024-07-27"
 },
 {
 "version": "5.4.281", "release_date": "2024-07-27"
 },
 {
 "version": "4.19.319", "release_date": "2024-07-27"
 },
 {
 "version": "next-20240812", "release_date": "2024-08-12"
 }
]

图 19：模型展示了 OCR 与格式遵循的高超能力。

OCR 与格式遵循
![Refer to caption](2409.12191v2/images/2-6-table_weather.jpg)
将图中的每日的最高气温和最低气温整理成表格。
(Translation: Organize the daily highest and lowest temperatures from the image into a table.)

模型回复

以下是图中每日的最高气温和最低气温整理成的表格：

日期
最高气温
最低气温

08/12
31°C
23°C

08/13
30°C
22°C

08/14
30°C
23°C

08/15
31°C
24°C

08/16
31°C
24°C

08/17
30°C
24°C

08/18
30°C
23°C

08/19
30°C
22°C
希望这对你有帮助！

图 20：模型展示了 OCR 与格式遵循的高超能力。

大图 OCR
![Refer to caption](2409.12191v2/images/2-7-screenshot2.png)![Refer to caption](2409.12191v2/images/screenshot_with_crop.jpg)
qwen-vl-max-0809对视频内容的理解功能存在哪些限制？
(Translation: What limitations exist in qwen-vl-max-0809’s ability to understand video content?)

模型回复

qwen-vl-max-0809对视频内容的理解功能存在以下限制：视频文件大小最大为150MB，视频文件格式支持MP4、AVI、MKV、MOV、FLV、WMV等，视频尺寸无限制，但视频文件会被调整到约600K像素数，更大尺寸的视频文件不会有更好的理解效果。
(Translation: qwen-vl-max-0809 has the following limitations on the video content understanding: the maximum video file size is 150MB, the video file formats supported are MP4, AVI, MKV, MOV, FLV, WMV, etc. There is no limitation on the video size, but the video file will be resized to about 600K pixels, and video files of larger sizes won’t have better video understanding results.)

图 21：模型展示了大图 OCR 的高超能力。

### A.3 视频理解

多轮视频对话
![Refer to caption](2409.12191v2/images/qwen2-vl/video_space_frames.png)
Please describe the video in detail.

模型回复

The video begins with a man speaking to the camera, followed by a group of people sitting in a control room. The camera then cuts to two men floating inside a space station, where they are seen speaking to the camera. The men appear to be astronauts, and they are wearing space suits. The space station is filled with various equipment and machinery, and the camera pans around to show the different areas of the station. The men continue to speak to the camera, and they appear to be discussing their mission and the various tasks they are performing. Overall, the video provides a fascinating glimpse into the world of space exploration and the daily lives of astronauts.

用户查询

What is the color of the clothes the two astronauts wearing?

模型回复

The two astronauts are wearing blue and black clothes.

图 22：模型展示了多轮视频对话的高超能力。

多视频理解
![Refer to caption](2409.12191v2/images/qwen2-vl/video_part1_frames.png)
视频中的人在做什么？
(Translation: What are the people in the video doing?)

模型回复

视频中的人正在使用吸尘器清理地板。
(Translation: The man in the video is using a vacuum cleaner to clean the floor.)

用户查询

如果要进一步清洁地面的话，接下来该怎么做？
(Translation: What should I do next if I want to clean the floor further?)

模型回复

如果要进一步清洁地面，可以使用拖把或湿布擦拭地面，以去除吸尘器无法清除的污渍和灰尘。
(Translation: For further cleaning of the floor, wipe the floor with a mop or damp cloth to remove stains and dirt that the vacuum cleaner cannot remove.)

用户查询
![Refer to caption](2409.12191v2/images/qwen2-vl/video_part2_frames.png)
已经用拖把清洁了地面，评价一下清洁工作？
(Translation: Already cleaned the floor with a mop and please comment on the cleaning?)

模型回复

从视频中可以看出，清洁工作已经完成，地面已经变得干净整洁。
(Translation: As you can see from the video, the cleaning has been completed and the floor has been made clean and tidy.)

用户查询

通过你看到的，接下来还能做些什么？
(Translation: By what you see, what else can you do next?)

模型回复

接下来可以将拖把清洗干净，晾干备用。
(Translation: Next you can clean the mop, dry it and set it aside.)

图 23：模型展示了多视频理解的高超能力。

### A.4 视觉智能体能力

Qwen2-VL 在定位与智能体任务上同样表现出色。

随心所欲定位
![Refer to caption](2409.12191v2/images/2_car_input.jpeg)
Detect the bounding box of ’the red car’

模型回复

¡—object_ref_start—¿the red car¡—object_ref_end—¿¡—box_start—¿(701,531),(869,675)¡—box_end—¿![Refer to caption](2409.12191v2/images/2_car_output.png)

图 24：我们的模型能够在图像中定位特定元素，例如准确识别出红色汽车。

视觉指代提示（Visual Referring Prompting）
![Refer to caption](2409.12191v2/images/2_news.jpeg)
What does the pointed news talk about?

模型回复

The pointed news with a green logo of OpenAI and a title ”Le chatbot ChatGPT d’OpenAI dispose désormais d’instructions personnalisées pour stocker vos préférences” is talking about the new feature of ChatGPT that can now store personalized instructions to better serve users.

图 25：我们的模型能够对网页截图中的内容进行标注并提出问题，展示了其作为视觉智能体的潜力。图像来源：([Yang et al., 2023](#bib.bib105))

函数调用——基础
![Refer to caption](2409.12191v2/images/func_call_basic.jpg)
几点到达，到的时候目的地天气怎么样
(Translation: What time does this flight arrive? What is the weather like at the destination when it arrives?)

函数输入

北京

函数结果

时间: 2024-07-30 14:00, 风向: 西南风, 风力: 0-3级 微风 ¡5.4m/s, 温度: 29°C, 天气: 小雨
时间: 2024-07-30 15:00, 风向: 西南风, 风力: 0-3级 微风 ¡5.4m/s, 温度: 28°C, 天气: 小雨
时间: 2024-07-30 16:00, 风向: 西南风, 风力: 0-3级 微风 ¡5.4m/s, 温度: 28°C, 天气: 小雨
时间: 2024-07-30 17:00, 风向: 西南风, 风力: 0-3级 微风 ¡5.4m/s, 温度: 28°C, 天气: 小雨
时间: 2024-07-30 18:00, 风向: 西南风, 风力: 0-3级 微风 ¡5.4m/s, 温度: 27°C, 天气: 中雨
时间: 2024-07-30 19:00, 风向: 南风, 风力: 0-3级 微风 ¡5.4m/s, 温度: 27°C, 天气: 中雨
时间: 2024-07-30 20:00, 风向: 南风, 风力: 0-3级 微风 ¡5.4m/s, 温度: 27°C, 天气: 中雨
时间: 2024-07-30 21:00, 风向: 南风, 风力: 0-3级 微风 ¡5.4m/s, 温度: 26°C, 天气: 小雨
时间: 2024-07-30 22:00, 风向: 南风, 风力: 0-3级 微风 ¡5.4m/s, 温度: 26°C, 天气: 小雨
时间: 2024-07-30 23:00, 风向: 南风, 风力: 0-3级 微风 ¡5.4m/s, 温度: 26°C, 天气: 小雨
（避免显示过长，省略部分信息。）

模型回复

根据航班信息，您乘坐的中国国航CA1723航班预计将于2024年7月30日20:30抵达北京首都机场T3航站楼。
在您到达时，北京的天气预报显示会有中雨，并且温度约为27℃。请注意携带雨具并做好防雨措施。祝您旅途愉快！
(Translation: According to flight information, your Air China flight CA1723 is expected to arrive at Beijing Capital Airport T3 Terminal at 20:30 on July 30, 2024. When you arrive, the weather forecast in Beijing shows moderate rain and the temperature is about 27℃. Please remember to bring rain gear and take rain protection measures. Have a pleasant journey!)

图 26：模型在图像中识别出目的地与到达时间，调用了 24 小时天气查询函数，正确输入目的地，并从查询结果中提取到达时刻的天气，从而能够回答用户的问题。

函数调用——代码解释器
![Refer to caption](2409.12191v2/images/func_call_flowchart.png)
Implement the flowchart, representing modules as functions without implementation details. Write the code and validate it using the code interpreter.

函数输入

[⬇](data:text/plain;base64,IyBQbGFjZWhvbGRlciBmdW5jdGlvbnMgZm9yIHRoZSBtb2R1bGVzCmRlZiBzcGVlY2hfYWRhcHRlcihpbnB1dF9hdWRpbyk6CiAgICAjIFBsYWNlaG9sZGVyIGZvciBzcGVlY2ggYWRhcHRlciBpbXBsZW1lbnRhdGlvbgogICAgcGFzcwoKIyBUbyBhdm9pZCBleGNlc3NpdmUgbGVuZ3RoLAojIHRoZSByZW1haW5pbmcgZnVuY3Rpb25zIHdpdGhvdXQgaW1wbGVtZW50YXRpb24gZGV0YWlscyBhcmUgb21pdHRlZCBoZXJlLgoKIyBFeGFtcGxlIHVzYWdlCmlucHV0X2F1ZGlvID0gInRhbGsgYWJvdXQgdGhlIHdlYXRoZXIgaW4gU2FuIEZyYW5jaXNjby4iCnNwZWVjaF9hZGFwdGVyX291dHB1dCA9IHNwZWVjaF9hZGFwdGVyKGlucHV0X2F1ZGlvKQpzcGVlY2hfZW5jb2Rlcl9vdXRwdXQgPSBzcGVlY2hfZW5jb2RlcihzcGVlY2hfYWRhcHRlcl9vdXRwdXQpCnN5c3RlbV9wcm9tcHRfb3V0cHV0ID0gc3lzdGVtX3Byb21wdCgpCmRpYWxvZ3VlX2hpc3Rvcnlfb3V0cHV0ID0gZGlhbG9ndWVfaGlzdG9yeSgpCmxsYW1hXzNfb3V0cHV0ID0gbGxhbWFfMyhzcGVlY2hfZW5jb2Rlcl9vdXRwdXQsIHN5c3RlbV9wcm9tcHRfb3V0cHV0LCBcCmRpYWxvZ3VlX2hpc3Rvcnlfb3V0cHV0KQp0ZXh0X25vcm1hbGl6YXRpb25fb3V0cHV0ID0gdGV4dF9ub3JtYWxpemF0aW9uKGxsYW1hXzNfb3V0cHV0KQpwcm9zb2R5X21vZGVsX291dHB1dCA9IHByb3NvZHlfbW9kZWwodGV4dF9ub3JtYWxpemF0aW9uX291dHB1dCkKb3V0cHV0X2F1ZGlvID0gc3ludGhlc2l6ZXIocHJvc29keV9tb2RlbF9vdXRwdXQp)
# Placeholder functions for the modules
def speech_adapter(input_audio):
 # Placeholder for speech adapter implementation
 pass

# To avoid excessive length,
# the remaining functions without implementation details are omitted here.

# Example usage
input_audio = "talk about the weather in San Francisco."
speech_adapter_output = speech_adapter(input_audio)
speech_encoder_output = speech_encoder(speech_adapter_output)
system_prompt_output = system_prompt()
dialogue_history_output = dialogue_history()
llama_3_output = llama_3(speech_encoder_output, system_prompt_output, \
dialogue_history_output)
text_normalization_output = text_normalization(llama_3_output)
prosody_model_output = prosody_model(text_normalization_output)
output_audio = synthesizer(prosody_model_output)

函数结果

Finished execution.

模型回复

The code has been executed without any errors, which means that the structure of the code matches the flowchart and there are no syntax issues. However, since the functions are placeholders and do not perform any actual operations, we cannot validate the correctness of the implementation. The code simply represents the flowchart by defining each module as a function and demonstrating how the functions could be called in sequence to process input audio and produce output audio.

图 27：模型识别出流程图中的步骤，按要求起草了省略细节的模拟代码，随后通过代码解释器成功执行。图像来源：([Dubey et al., 2024](#bib.bib27))

函数调用——代码解释器
![[Uncaptioned image]](2409.12191v2/images/func_call_table.png)
Count the average value of each row in this chart and draw a bar chart to show it. Write the code and verify it using the code interpreter.

函数输入

[⬇](data:text/plain;base64,aW1wb3J0IHBhbmRhcyBhcyBwZAppbXBvcnQgbnVtcHkgYXMgbnAKaW1wb3J0IG1hdHBsb3RsaWIucHlwbG90IGFzIHBsdAoKIyBFeHRyYWN0aW5nIHRoZSBudW1lcmljYWwgdmFsdWVzIGZyb20gdGhlIHRhYmxlCmRhdGEgPSB7CiAgICAiTW9kZWwiOiBbIkxsYW1hIDMgOEIiLCAiR2VtbWEgMiA5QiIsICJNaXN0cmFsIDdCIiwgIkxsYW1hIDMgNzBCIiwgXAogICAgICAgICJNaXh0cmFsIDh4MjJCIiwgIkdQVC0zLjUgVHVyYm8iLCAiTGxhbWEgMyA0MDVCIiwgIkdQVC00IiwgXAogICAgICAgICJHUFQtNG8iLCAiQ2xhdWRlIDMuNSBTb25uZXQiLCAiTmVtb3Ryb24gNCAzNDBCIl0sCiAgICAiSHVtYW5FdmFsIjogWzcyLjYsIDU0LjMsIDQwLjIsIDgwLjUsIDc1LjYsIDY4LjAsIDg5LjAsIDg2LjYsIDkwLjIsIFwKICAgICAgICA5Mi4wLCA3My4yXSwKICAgICJIdW1hbkV2YWwrIjogWzY3LjEsIDQ4LjgsIDMyLjMsIDc0LjQsIDY4LjMsIDYyLjgsIDgyLjMsIDc3LjQsIDg2LjAsIFwKICAgICAgICA4Mi4zLCA2NC4wXSwKICAgICJNQlBQIjogWzYwLjgsIDU5LjIsIDQyLjYsIDc1LjQsIDY2LjIsIDcxLjIsIDc4LjgsIDgwLjIsIDgxLjQsIDc2LjYsIFwKICAgICAgICA3NS40XSwKICAgICJNQlBQIEV2YWxQbHVzIChiYXNlKSI6IFs3Mi44LCA3MS43LCA0OS41LCA4Ni4wLCA3OC42LCA4Mi4wLCA4OC42LCBcCiAgICAgICAgODMuNiwgODcuOCwgOTAuNSwgNzIuOF0KfQoKIyBDcmVhdGUgYSBEYXRhRnJhbWUKZGYgPSBwZC5EYXRhRnJhbWUoZGF0YSkKCiMgQ2FsY3VsYXRlIHRoZSBhdmVyYWdlIGZvciBlYWNoIHJvdwpkZlsiQXZlcmFnZSJdID0gZGYubWVhbihheGlzPTEpCgojIFBsb3R0aW5nIHRoZSBiYXIgY2hhcnQKcGx0LmZpZ3VyZShmaWdzaXplPSgxMiwgNikpCnBsdC5iYXIoZGZbIk1vZGVsIl0sIGRmWyJBdmVyYWdlIl0sIGNvbG9yPSJza3libHVlIikKcGx0LnhsYWJlbCgiTW9kZWwiKQpwbHQueWxhYmVsKCJBdmVyYWdlIFNjb3JlIikKcGx0LnRpdGxlKCJBdmVyYWdlIFBhc3NAMSBTY29yZXMgb24gQ29kZSBHZW5lcmF0aW9uIEJlbmNobWFya3MiKQpwbHQueHRpY2tzKHJvdGF0aW9uPTQ1LCBoYT0icmlnaHQiKQpwbHQudGlnaHRfbGF5b3V0KCkKcGx0LnNob3coKQ==)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Extracting the numerical values from the table
data = {
 "Model": ["Llama 3 8B", "Gemma 2 9B", "Mistral 7B", "Llama 3 70B", \
 "Mixtral 8x22B", "GPT-3.5 Turbo", "Llama 3 405B", "GPT-4", \
 "GPT-4o", "Claude 3.5 Sonnet", "Nemotron 4 340B"],
 "HumanEval": [72.6, 54.3, 40.2, 80.5, 75.6, 68.0, 89.0, 86.6, 90.2, \
 92.0, 73.2],
 "HumanEval+": [67.1, 48.8, 32.3, 74.4, 68.3, 62.8, 82.3, 77.4, 86.0, \
 82.3, 64.0],
 "MBPP": [60.8, 59.2, 42.6, 75.4, 66.2, 71.2, 78.8, 80.2, 81.4, 76.6, \
 75.4],
 "MBPP EvalPlus (base)": [72.8, 71.7, 49.5, 86.0, 78.6, 82.0, 88.6, \
 83.6, 87.8, 90.5, 72.8]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Calculate the average for each row
df["Average"] = df.mean(axis=1)

# Plotting the bar chart
plt.figure(figsize=(12, 6))
plt.bar(df["Model"], df["Average"], color="skyblue")
plt.xlabel("Model")
plt.ylabel("Average Score")
plt.title("Average Pass@1 Scores on Code Generation Benchmarks")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

函数结果
![Refer to caption](2409.12191v2/images/func_call_table_result.png)

模型回复

The average Pass@1 scores on code generation benchmarks for each model have been calculated and are displayed in the table above. The bar chart shows the average scores for each model, providing a visual comparison of their performance across the different benchmarks.

图 28：模型分析了表格，编写代码计算表格每行的平均值并将结果绘制为条形图，该代码由代码解释器成功执行并可视化。图像来源：([Dubey et al., 2024](#bib.bib27))

函数调用——代码解释器
![[Uncaptioned image]](2409.12191v2/images/func_call_formula.png)
Implement the formula, write the code and verify it using the code interpreter.

函数输入

[⬇](data:text/plain;base64,aW1wb3J0IG51bXB5IGFzIG5wCgpkZWYgc29mdG1heCh4KToKICAgICIiIkNvbXB1dGUgc29mdG1heCB2YWx1ZXMgZm9yIGVhY2ggc2V0cyBvZiBzY29yZXMgaW4geC4iIiIKICAgIGVfeCA9IG5wLmV4cCh4IC0gbnAubWF4KHgpKQogICAgcmV0dXJuIGVfeCAvIGVfeC5zdW0oYXhpcz0wKQoKZGVmIHRvcF9rKHAsIGspOgogICAgIiIiUmV0dXJuIHRoZSBpbmRpY2VzIG9mIHRoZSB0b3AgayBlbGVtZW50cyBpbiB0aGUgcHJvYmFiaWxpdHkgdmVjdG9yIHAuIiIiCiAgICByZXR1cm4gbnAuYXJnc29ydChwKVstazpdWzo6LTFdCgojIEV4YW1wbGUgaW5wdXQKeCA9IG5wLmFycmF5KFsxLCAyLCAzLCA0LCA1XSkgICMgRXhhbXBsZSBpbnB1dCB2ZWN0b3IKRyA9IGxhbWJkYSB4OiB4ICAjIFNpbXBsZSBnYXRpbmcgbmV0d29yayAoaWRlbnRpdHkgZnVuY3Rpb24gZm9yIGRlbW9uc3RyYXRpb24pCkUgPSBsYW1iZGEgeCwgaTogeCArIGkgICMgU2ltcGxlIGV4cGVydCBmdW5jdGlvbnMgKGFkZCB0aGUgZXhwZXJ0IGluZGV4IHRvIHRoZSBpbnB1dCkKIyBDb21wdXRlIHByb2JhYmlsaXRpZXMKcCA9IHNvZnRtYXgoRyh4KSkKIyBTZWxlY3QgdG9wIGsgZXhwZXJ0cwprID0gMwp0b3BfZXhwZXJ0cyA9IHRvcF9rKHAsIGspCiMgQ29tcHV0ZSBvdXRwdXQKeSA9IG5wLnN1bShbcFtpXSAqIEUoeCwgaSkgZm9yIGkgaW4gdG9wX2V4cGVydHNdKQpwLCB0b3BfZXhwZXJ0cywgeQ==::LTFdCgojIEV4YW1wbGUgaW5wdXQKeCA9IG5wLmFycmF5KFsxLCAyLCAzLCA0LCA1XSkgICMgRXhhbXBsZSBpbnB1dCB2ZWN0b3IKRyA9IGxhbWJkYSB4OiB4ICAjIFNpbXBsZSBnYXR0aW5nIG5ldHdvcmsgKGlkZW50aXR5IGZ1bmN0aW9uIGZvciBkZW1vbnN0cmF0aW9uKQpFID0gbGFtYmRhIHgsIGk6IHggKyBpICAgIyBTaW1wbGUgZXhwZXJ0IGZ1bmN0aW9ucyAoYWRkIHRoZSBleHBlcnQgaW5kZXggdG8gdGhlIGlucHV0KQojIENvbXB1dGUgcHJvYmFiaWxpdGllcwpwID0gc29mdG1heChHKHgpKQojIFNlbGVjdCB0b3AgayBleHBlcnRzCmsgPSAzCnRvcF9leHBlcnRzID0gdG9wX2socCwgaykKIyBDb21wdXRlIG91dHB1dAp5ID0gbnAuc3VtKFtwW2ldICogRSh4LCBpKSBmb3IgaSBpbiB0b3BfZXhwZXJ0c10pCnAsIHRvcF9leHBlcnRzLCB5)
import numpy as np

def softmax(x):
 """Compute softmax values for each sets of scores in x."""
 e_x = np.exp(x - np.max(x))
 return e_x / e_x.sum(axis=0)

def top_k(p, k):
 """Return the indices of the top k elements in the probability vector p."""
 return np.argsort(p)[-k:][::-1]

# Example input
x = np.array([1, 2, 3, 4, 5]) # Example input vector
G = lambda x: x # Simple gating network (identity function for demonstration)
E = lambda x, i: x + i # Simple expert functions (add the expert index to the input)
# Compute probabilities
p = softmax(G(x))
# Select top k experts
k = 3
top_experts = top_k(p, k)
# Compute output
y = np.sum([p[i] * E(x, i) for i in top_experts])
p, top_experts, y

函数结果

(array([0.01165623, 0.03168492, 0.08612854, 0.23412166, 0.63640865]),
array([4, 3, 2]),
31.451165958047895)

模型回复

The probabilities assigned to each expert based on the input vector (x) are: (p = [0.01165623, 0.03168492, 0.08612854, 0.23412166, 0.63640865]).
The top (k = 3) experts selected based on these probabilities are the experts with indices 4, 3, and 2 (in descending order of probability).
The output (y) computed as a weighted sum of the outputs of these top experts is approximately 31.4512.
This example demonstrates a simple implementation of the MoE model’s operation. In a real-world scenario, the gating network (GG) and the experts (EiE_{i}) would be more complex, involving neural network layers and potentially non-linear transformations.

图 29：模型理解了公式，按要求实现了代码，并在代码解释器中成功执行以获得结果。图像来源：([Dubey et al., 2024](#bib.bib27))

VL 智能体——UI 操作
![[Uncaptioned image]](2409.12191v2/images/agent/ui/ui_operation.png)

系统消息

You are a helpful assistant.

# Actions

## You have the following actions.

### Click

Click: A quick, light fingertip press that commands, selects, or navigates through a phone’s user interface. Parameters: [{”name”: ”point”, ”description”: ”The specific point of interest on the screen, marked by the coordinate (x, y).” ”required”: true, ”schema”: ”string”}]

### Type

Type: Engaging with a smartphone’s interface by entering text for various purposes like messaging, searching, or command execution. Parameters: [{ ”name”: ”text”, ”description”: ”The text to be typed on a smartphone.”, ”required”: true, ”schema”: ”string”}]

### Swipe

Swipe: Touch the screen and move your finger to a new location for new content. Parameters: [”name”: ”direction”, ”description”: ”Determine the swipe route from the cardinal directions: up, down, left, or right.” ”required”: true, ”schema”: ”string”, ”choices”: [”up”, ”down”, ”left”, ”right”]]

### Back

Back: Go in reverse to the prior interface or exiting the current context Parameters: []

### Home

Home: Return to the device’s home screen from any application or task. Parameters: []

### Enter

Enter: Execute a command to confirm inputs or selections. Parameters: []

### Done

Done: Indicate the completion of a task. Parameters: []

VL 智能体——UI 操作

## Continuously take action until the task is completed.

*FUNCTION*: The action to take, should be one of {Click,Type,Swipe,Back,Home,Enter,Done}

*ARGS*: The input of the action.

*RESULT*: Action results.

*RETURN*: Reply based on action results.

用户

Your task is: What’s a good restaurant in San Diego?

![](Screenshot_1)

助手

The screen shows the email setup page, which is not relevant to finding a restaurant. Possible actions are to exit the em ail setup and navigate to a search engine or map application where I can look up restaurants in San Diego.
*FUNCTION*: Home *ARGS*: {}

*RESULT*: ![](Screenshot_2)

*RETURN*: The screen shows the home screen with various apps, including Google Chrome and Maps which could be used to search for a restaurant in San Diego. Possible actions are to tap on the Google Chrome app to open it and then use it to search for a good restaurant in San Diego.

*FUNCTION*: Click *ARGS*: {”point”: ”(687, 792)”}

*RESULT*: ![](Screenshot_4)

*RETURN*: The current screen shows search results for skateboards, which is not related to the query about finding a good restaurant in San Diego. Possible actions are to click on the Google search bar at the top of the screen and enter the correct search term ”good restaurant in San Diego” to find relevant information.

*FUNCTION*: Click *ARGS*: {”point”: ” (596, 213)”}

*RESULT*: ![](Screenshot_6)

*RETURN*: The current screen shows search suggestions related to skateboard speeds, which is not relevant to the query about finding a good restaurant in San Diego. Possible actions are to click on the ”X” button to he correct query for finding a good restaurant in San Diego.

*FUNCTION*: Click *ARGS*: {”point”: ”(927, 135)”}

*RESULT*: ![](Screenshot_8)

*RETURN*: The screen shows the Google search bar with a list of previous searches, none of which are related to finding a restauran t in San Diego. Possible actions are to type ”good restaurant in San Diego” into the search bar and then press enter to perform the search.

*FUNCTION*: Type *ARGS*: {”text”: ”What’s a good restaurant in San Diego?”}

*RESULT*: ![](Screenshot_9)

*RETURN*: The screen shows a list of search suggestions related to finding good restaurants in San Diego, indicating that the user has typed in a query but not yet executed it. Possible actions are to select one of the suggested searches or press enter on the keyboard to execute the current search and view the results.

*FUNCTION*: Enter *ARGS*: {}

*RESULT*: ![](Screenshot_10)

*RETURN*: The screen shows a list of top-rated restaurants in San Diego with details such as ratings, price range, and opening hours. Possible actions are to stop and set the query as completed.

*FUNCTION*: Done *ARGS*: {}

图 30：Qwen2-VL 作为智能体理解与 UI 操作相关的查询，利用系统消息中预定义的动作，逐步完成任务。

VL 智能体——卡牌游戏
![[Uncaptioned image]](2409.12191v2/images/agent/game/blackjack.png)

系统消息

You are a helpful assistant.

# Actions

## You have the following actions.

### Hit

Hit: Get a new card. Parameters: []

### Stand

Stand: Stop to get a new card. Parameters: []

## Continuously take action until the task is completed.

*FUNCTION*: The action to take, should be one of {Hit,Stand}

*ARGS*: The input of the action.

*RESULT*: Action results.

*RETURN*: Reply based on action results.

用户

You are a blackjack player. You are observing the current game state in the image. With the given functions, your goal is to dealer by getting as close to 21 points as possible without exceeding it.

![](Screenshot_1)

助手

I have 8 points, and the dealer has 10 points. I should hit.

*FUNCTION*: Hit *ARGS*: {}

*RESULT*:

![](Screenshot_2)

*RETURN*: I have 15 points, and the dealer has 10 points. I should hit.

*FUNCTION*: Hit *ARGS*: {}

*RESULT*:

![](Screenshot_3)

*RETURN*: I have 17 points, and the dealer has 10 points. I should stand.

*FUNCTION*: Stand *ARGS*: {}

*RESULT*: Dealer Card: Q, 5, Q. The total point of dealer is 25 ¿ 21.

Player Card: 4, 4, 7, 2. The total point of player is 17.

Player win!

图 31：Qwen2-VL 识别这些卡牌，并利用 Hit 与 Stand 动作玩二十一点（Blackjack）。
