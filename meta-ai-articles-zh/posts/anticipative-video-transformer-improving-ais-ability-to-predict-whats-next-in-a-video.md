---
title: "前瞻视频 Transformer：提升 AI 预测视频后续内容的能力"
title_en: "Anticipative Video Transformer: Improving AI's ability to predict what's next in a video"
date: 2021-10-13
source: https://ai.facebook.com/blog/anticipative-video-transformer-improving-ais-ability-to-predict-whats-next-in-a-video
crawled: 2026-09-22
translated: 2026-09-22
---

# 前瞻视频 Transformer：提升 AI 预测视频后续内容的能力

> 原文：[Anticipative Video Transformer: Improving AI's ability to predict what's next in a video](https://ai.facebook.com/blog/anticipative-video-transformer-improving-ais-ability-to-predict-whats-next-in-a-video) · Meta AI（Wayback 存档）

2021 年 10 月 13 日

**研究内容：**从自动驾驶汽车到增强现实，诸多应用都要求 AI 系统能够预判人们未来的行动。当某人在组装宜家梳妆台时，可能会琢磨下一步是装桌腿还是装抽屉。朋友可以根据此前完成的步骤，贴心地提示该装哪个部件。但这种预判对 AI 而言是极具挑战的任务，既需要预测未来活动的多模态分布，又需要建模过去动作的演进。为了应对这一重要挑战，我们借助 Transformer 架构（尤其是在自然语言处理和图像建模方面）的最新进展，构建了前瞻视频 Transformer（Anticipative Video Transformer，AVT）——一个用于视频中动作预判的端到端注意力模型。与以往方法相比，它更擅长理解长程依赖，比如某人过去的烹饪步骤如何预示其下一步动作。

AVT 对「AR 动作教练」或 AI 助手这类应用可能特别有用：提示某人可能在完成任务时即将出错，或者提前一步给出有用的下一步提示。例如，AVT 可以根据此人此前与平底锅的交互，提醒他要拿起的锅是烫的。我们有信心 AVT 能在这些及其他应用中快速提升动作预判性能——我们的模型在四个流行基准（EGTEA Gaze+、50-Salads、EPIC-Kitchens-55）上超越了现有最优架构，并最终赢得 EPIC-Kitchens 2021 竞赛的动作预判（Action Anticipation）挑战赛，就是明证。（Epic-Kitchens-55 数据集采用知识共享署名-非商业性 4.0 国际许可协议授权。）

（原文此处嵌入视频：Something Went Wrong We're having trouble playing this video. Learn more）

**工作原理：**以往大多数动作预判方法难以建模序列化的长程依赖。例如，预测某人做煎蛋卷的下一个动作——切洋葱还是热锅——取决于其已执行的动序列。但 AVT 基于注意力，可以并行处理完整序列；相比之下，基于循环神经网络的方法必须顺序处理，常常「忘记」过去。AVT 还配备了鼓励模型捕捉视频序列特性的损失函数，否则这些特性会被非局部网络（nonlocal networks）这类注意力架构丢失。

AVT 由两部分组成：作用于视频帧的注意力主干（AVT-b），以及作用于主干所提取特征的注意力头部架构（AVT-h）。我们最好的动作预判效果来自端到端训练完整架构，但 AVT-h 也兼容 3D 卷积网络等标准视频主干。这很重要，因为学习更好的视频主干是一个活跃的研究方向，我们希望 AVT 能用上最新最好的视频主干，比如多尺度视觉 Transformer（Multiscale Vision Transformers）。

AVT-b 主干基于 Vision Transformer（ViT）架构：把帧切分为不重叠的图块（patch），用前馈网络嵌入，附加一个特殊的分类 token，并施加多层多头自注意力。然后我们跨帧共享权重，并使用分类 token 对应的特征供头部使用。头部架构接收逐帧特征，再施加另一个带因果注意力的 Transformer 架构。这意味着它只评估当前帧和之前帧的特征，进而使模型在生成任意单帧的表示时只依赖过去的特征——这对预测至关重要。例如，在上面的视频中，模型先编码打开水龙头的视觉特征，接着是清洗每一个西红柿，最后预测下一个动作是关掉水龙头。

我们用三个损失训练模型预测未来动作和特征：第一，对视频片段最后一帧的特征做分类以预测有标签的未来动作；第二，把中间帧特征回归到后续帧的特征，训练模型预测接下来会发生什么；第三，训练模型对中间动作分类。我们已经证明，联合优化这三个损失，模型预测未来动作的能力比仅用双向注意力训练的模型高出 10% 到 30%。这些额外损失为模型提供了额外监督，使 AVT 更适合长程推理，并且其性能随着纳入越来越长的上下文而提升。

**为什么重要：**人们每天都在基于对周围世界的理解做出无数决策——不是把它当作一组静态、固定的输入，而是当作一连串相互关联的事件。AI 模型在与人协作、为人服务的许多任务上前景广阔，但要最大化这种潜力，它们也需要这种预判能力。AVT 是朝这个方向迈出的重要一步。由于建立在因果解码器架构之上，AVT 可以很容易地以自回归方式展开，向更远的未来预测——不仅预判下一个动作，还能预判用户可能执行的多个连续动作。这有朝一日可能对长期规划任务大有用处，例如 AR 眼镜观察到佩戴者正在换爆胎：系统可以预判该任务所需的系列步骤，并提示佩戴者选择需要的具体工具——甚至提前几步，在他们走向工具棚取工具时就给出提示。

展望未来，我们相信 AVT 可以用于预判之外的任务，比如自监督学习、动作模式（action schema）与边界的发现，乃至需要建模动作时序的一般动作识别。这些正是我们期待在未来工作中探索的方向。

（原文此处嵌入视频：Something Went Wrong We're having trouble playing this video. Learn more）

使用自回归展开进行长期预判。

阅读完整论文并试用我们的代码：

**作者**

- Rohit Girdhar，研究科学家
- Kristen Grauman，研究总监
