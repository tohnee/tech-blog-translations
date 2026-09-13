---
title: "RT-2：将视觉与语言转化为动作的新模型"
title_en: "RT-2: New model translates vision and language into action"
source: https://deepmind.google/blog/rt-2-new-model-translates-vision-and-language-into-action/
site: deepmind
date: 2023-07-28
crawled: 2026-09-13
translated: 2026-09-13
---

# RT-2：将视觉与语言转化为动作的新模型

> 原文：[RT-2: New model translates vision and language into action](https://deepmind.google/blog/rt-2-new-model-translates-vision-and-language-into-action/) · Google DeepMind

机器人 Transformer 2（RT-2）是一个新颖的视觉-语言-动作（VLA）模型，它同时从网络数据和机器人数据中学习，并将这些知识转化为机器人控制的通用化指令

大容量视觉-语言模型（VLM）在网络规模的数据集上训练，因此这些系统极其擅长识别视觉或语言模式，并能跨语言运行。但要让机器人达到类似的能力水平，它们就需要在每个物体、每个环境、每个任务和每种情境下亲自收集机器人数据。

在[论文](https://robotics-transformer2.github.io/assets/rt2.pdf)中，我们介绍了机器人 Transformer 2（RT-2）——一个新颖的视觉-语言-动作（VLA）模型，它同时从网络数据和机器人数据中学习，将这些知识转化为机器人控制的通用化指令，同时保留网络规模模型的能力。

![](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/64c28bb04fd16049ea01b833_64c1e428094c3322c3991c90_RT-22520gif_1.gif)

一个在网络规模数据上预训练的视觉-语言模型（VLM），正在从 RT-1 机器人数据中学习，成为 RT-2——一个能够控制机器人的视觉-语言-动作（VLA）模型。

这项工作建立在机器人 Transformer 1 [(RT-1)](https://ai.googleblog.com/2022/12/rt-1-robotics-transformer-for-real.html) 的基础上——后者是一个在多任务演示上训练的模型，可以学习机器人数据中出现过的任务与物体的组合。更具体地说，我们的工作使用了由 13 台机器人在办公室厨房环境中历时 17 个月收集的 RT-1 机器人演示数据。

RT-2 展示出超越其所接触的机器人数据的泛化能力、语义理解与视觉理解。这包括解读新指令，并通过执行初步推理来响应用户指令，例如对物体类别或高层描述进行推理。

我们还证明，引入思维链（chain-of-thought）推理后，RT-2 能够执行多阶段语义推理，例如判断哪个物体可以充当临时锤子（一块石头），或哪种饮料最适合疲惫的人（一罐能量饮料）。

## 让 VLM 适配机器人控制

RT-2 建立在 VLM 之上。这类 VLM 以一张或多张图像作为输入，输出一串通常表示自然语言文本的 token。这样的 VLM 已经[被成功训练](https://ai.googleblog.com/2022/09/pali-scaling-language-image-learning-in.html)在网络规模数据上执行诸如视觉问答、图像描述或物体识别等任务。在我们的工作中，我们改造 Pathways Language and Image 模型（[PaLI-X](https://ai.googleblog.com/2022/09/pali-scaling-language-image-learning-in.html)）和 Pathways Language model Embodied（[PaLM-E](https://ai.googleblog.com/2023/03/palm-e-embodied-multimodal-language.html)）作为 RT-2 的主干。

要控制机器人，必须训练它输出动作。我们通过把动作表示为模型输出中的 token——与语言 token 类似——来解决这一难题，并将动作描述为可以由标准[自然语言分词器](https://github.com/google/sentencepiece)处理的字符串，如下所示：

![示意图展示机器人动作如何表示为一串 token：以「终止或继续」开头，随后是三个表示位置变化（X、Y、Z）的 token，三个表示旋转变化（X、Y、Z）的 token，以及最后一个表示夹爪状态的 token。](https://lh3.googleusercontent.com/_xUzI0LiXRXg-9C6qqFYWt5U-Dn2gUlui_lk9vaJ0lR6zqH9ijCMNfE7mFXXNcsPB85VK-Q0kcV_xylGcFzAdDL4V57jx3kMoXNYTqOO4Le_mrO7pVg=w1440)

RT-2 训练中使用的动作字符串表示。这样的字符串可以是一串机器人动作 token 编号，例如「1 128 91 241 5 101 127 217」。

字符串以一个标志位开始，用于指示是继续还是终止当前回合（终止时不执行后续命令），随后是改变末端执行器位置和旋转的命令，以及夹爪的期望开合程度。

我们使用与 RT-1 相同的机器人动作离散化版本，并证明将其转换为字符串表示，就使得在机器人数据上训练 VLM 模型成为可能——因为这些模型的输入和输出空间无需改变。

![示意图展示 RT-2 模型的训练流程：互联网规模的 VQA 数据与机器人动作数据共同微调，创建用于机器人控制的视觉-语言-动作模型，随后部署到闭环机器人控制任务中，例如「把草莓放进正确的碗里」「拿起快要掉落的袋子」「拿起不同的物体」。](https://lh3.googleusercontent.com/wS51jyqW2T7T_m14tD2kn4pg86isQ1i7kusjlkQC-OktXdDgz-2iG4m_oZB8aFNmulk5ckURCxItJ1yWMVX54uU5k1WshHFKiqbhmNjlQmtgeN-O=w1440)

RT-2 架构与训练：我们在机器人数据和网络数据上共同微调一个预训练的 VLM 模型。所得模型接收机器人相机图像，直接预测机器人要执行的动作。

## 泛化与涌现技能

我们在 RT-2 模型上进行了超过 6000 次机器人试验的一系列定性和定量实验。为探索 RT-2 的涌现能力，我们首先寻找那些需要结合网络规模知识与机器人自身经验的任务，然后定义了三类技能：符号理解、推理和人类识别。

每个任务都需要理解视觉-语义概念，并具备对这些概念进行操作的机器人控制能力。诸如「拿起快要掉下桌子的袋子」或「把香蕉移到二加一的和的位置」之类的指令——要求机器人对其在机器人数据中从未见过的物体或场景执行操作任务——需要从网络数据迁移而来的知识才能完成。

![15 个示例的网格，展示 RT-2 模型的涌现能力。每个示例将机械臂执行任务的照片与包含自然语言指令的文本框配对，例如「拿起快要掉下桌子的袋子」「把香蕉移到德国」「把可乐罐移到 Taylor Swift」「把香蕉移到二加一的和的位置」。](https://lh3.googleusercontent.com/bO4w5oQ6jaC03Mb4IHsBwpbLs6ZIzWE6e26qsBxVxr_C7hH1eWmzXw8XfLsazfZWOxoB_k1wtv7fX9ChE3elaKh0nrIqD-HKu3VxBGB6vcxZo4mt3w=w1440)

机器人数据中不存在、需要从网络预训练迁移知识的涌现机器人技能示例。

在所有类别中，我们都观察到相较此前基线的泛化性能提升（超过 3 倍），这些基线包括以前的 RT-1 模型和在大规模视觉数据集上预训练的 Visual Cortex（[VC-1](https://eai-vc.github.io/)）等模型。

![标题为「涌现技能评估的成功率」的条形图，比较 VC1、RT-1、RT-2（PaLM-E-12B 版本）和 RT-2（PaLI-X-55B 版本）在「符号理解」「推理」「人类识别」三个类别以及「任务平均」上的表现。RT-2 模型显著超越 VC1 和 RT-1 基线，其中 RT-2（PaLI-X-55B）取得最高成功率，符号理解超过 80%，平均接近 60%。](https://lh3.googleusercontent.com/9R8LMhVVNeVXvOJTQTPOAq2DpBtJlruhnq2Hd40iFVdvK2W6aWLvQywhdqN6MDHE3Xc_7UlLa0eXAchDlY6f4aj9hAFWSkKhnn_OKph2DDaP5wJfnQ=w1440)

涌现技能评估的成功率：我们的 RT-2 模型超越了此前的机器人 Transformer（RT-1）基线和视觉预训练（VC-1）基线。

我们还进行了一系列定量评估：从机器人数据中有样本的原始 RT-1 任务开始，随后逐步引入机器人此前未见过的物体、背景和环境（程度各异），这些任务要求机器人从 VLM 预训练中学习泛化。

![三张并排图片展示泛化评估：第一张展示「未见过的物体」（一个汽水罐、一块手表、一条蓝色毛巾和一个粉色工具）；第二张展示「未见过的背景」（一张铺着秋叶图案桌布、上面放着玩具的桌子）；第三张展示「未见过的环境」（金属水槽旁的各种厨房用品）。](https://lh3.googleusercontent.com/bqQlrYAORkOlJ6QTVGTYBSHicJDdX2YcGXlL2mnW-5EvryaZIcBdyBJaoSyiWAs5mrcAdN3mn4E0F5OhxM-hBQhsqyGDpNpRwVDzK3asqxpTNUNt=w1440)

机器人此前未见过的环境示例，RT-2 在这些新情境中实现了泛化。

RT-2 保持在机器人数据中出现过的原始任务上的性能，并将机器人此前未见场景下的性能从 RT-1 的 32% 提升到 62%，展现了大规模预训练的巨大收益。

此外，我们观察到相较仅在视觉任务上预训练的基线（如 VC-1 和面向机器人操作的通用表征 [R3M](https://sites.google.com/corp/view/robot-r3m/)），以及使用 VLM 进行物体识别的算法（如开放世界物体操作 [MOO](https://robot-moo.github.io/)）的显著提升。

![一张条形图，比较各模型在不同评估场景中的表现：「见过的任务」「未见过的物体」「未见过的背景」「未见过的环境」和「未见任务平均」。RT-2（PaLM-E-12B 版本）和 RT-2（PaLI-X-55B 版本）在所有未见类别中持续超越 R3M、VC-1、RT-1 和 MOO 基线。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/64c28bb0a7e46157ca3edb96_64c2566864b91d6bd0590f41_Fig25206.svg)

RT-2 在见过的分布内任务上取得高性能，并在分布外的未见任务上超越多个基线。

在开源的 [Language Table](https://github.com/google-research/language-table) 机器人任务套件上评估我们的模型，我们在仿真中取得了 90% 的成功率，大幅超越此前基线，包括 [BC-Z](https://sites.google.com/corp/view/bc-z/home)（72%）、[RT-1](https://ai.googleblog.com/2022/12/rt-1-robotics-transformer-for-real.html)（74%）和 [LAVA](https://interactive-language.github.io/)（77%）。

随后，我们在真实世界中评估了同一个模型（因为它同时在仿真数据和真实数据上训练），并展示了它对新物体的泛化能力，如下所示——除蓝色立方体之外的所有物体都不在训练数据集中。

![两张并排照片，标题为「把番茄酱推到蓝色立方体」。左图显示机械臂旁边是一块木板，上面放着三瓶不同的调味酱。右图显示机械臂把番茄酱推向蓝色立方体。](https://lh3.googleusercontent.com/TAp7v2jwkWXtS2pfu6SYW8wGL8O7oacILl-G_kRKVhBH-YAa7gOtfQgBGCJSQWy1sAQXd_uPbFCm9BMRS1fp2ax89DnVZbg8-l0Uq4FSLLnPeBM1z7Y=w1440)

RT-2 在真实机器人的 Language Table 任务上表现出色。除蓝色立方体外的所有物体都不在训练数据中。

受 [LLM 中使用的思维链提示方法](https://ai.googleblog.com/2022/05/language-models-perform-reasoning-via.html)启发，我们探索让模型将机器人控制与思维链推理相结合，从而在单一模型内实现长时程规划与底层技能的学习。

具体来说，我们对 RT-2 的一个变体进行了仅几百步梯度的微调，以提升它联合使用语言和动作的能力。然后我们扩充数据，加入一个额外的「规划（Plan）」步骤：先用自然语言描述机器人即将执行的动作的目的，接着是「动作（Action）」和动作 token。这里我们展示这样一个推理示例以及机器人随之产生的行为：

![一张图像，展示机器人执行思维链语义推理。左侧，指令「我需要钉钉子，场景中哪个物体可能有用了？」的预测答案是「石头。动作：1 129 138 122 132 132 106 127」。右侧，三张连拍照片显示机械臂成功识别、伸手并拿起桌上的石头。](https://lh3.googleusercontent.com/AgfKBrhscaCWnmmzUjTpb_4MrH8wS8ITeG-srl3R3U5GVuQHwZOR22Mr5JU4eArTCmz9ijtp4JJHdPIDu9T6HAVJNXrwdSqpyzRVA8vCTTjmBjXb71w=w1440)

思维链推理使得学习一个自包含模型成为可能：它既能规划长时程的技能序列，又能预测机器人动作。

借助这一流程，RT-2 能够执行更复杂的指令——这些指令需要对完成用户指令所需的中间步骤进行推理。得益于其 VLM 主干，RT-2 还能根据图像和文本两种指令进行规划，实现视觉锚定（grounding）的规划；而当前的「先规划后执行」方法（如 [SayCan](https://ai.googleblog.com/2022/08/towards-helpful-robots-grounding.html)）无法看到真实世界，完全依赖语言。

## 推进机器人控制

RT-2 表明，视觉-语言模型（VLM）可以被转化为强大的视觉-语言-动作（VLA）模型：通过将 VLM 预训练与机器人数据相结合，它可以直接控制机器人。

基于 PaLM-E 和 PaLI-X 的两种 VLA 实例化，RT-2 带来了大幅提升的机器人策略，更重要的是，带来了显著更好的泛化性能和从网络规模视觉-语言预训练继承而来的涌现能力。

RT-2 不仅是对现有 VLM 模型的简单而有效的改造，还展示了构建一个通用物理机器人的前景：它能够推理、解决问题、解读信息，从而在真实世界中执行多样化的任务。

[‍阅读我们的论文](https://robotics-transformer2.github.io/assets/rt2.pdf)[在 Keyword 博客上了解更多](https://blog.google/technology/ai/google-deepmind-rt2-robotics-vla-model/)

**致谢**

我们感谢这项工作的共同作者：Anthony Brohan、Noah Brown、Justice Carbajal、Yevgen Chebotar、Xi Chen、Krzysztof Choromanski、Tianli Ding、Danny Driess、Avinava Dubey、Chelsea Finn、Pete Florence、Chuyuan Fu、Montse Gonzalez Arenas、Keerthana Gopalakrishnan、Kehang Han、Karol Hausman、Alexander Herzog、Jasmine Hsu、Brian Ichter、Alex Irpan、Nikhil Joshi、Ryan Julian、Dmitry Kalashnikov、Yuheng Kuang、Isabel Leal、Lisa Lee、Tsang-Wei Edward Lee、Sergey Levine、Yao Lu、Henryk Michalewski、Igor Mordatch、Karl Pertsch、Kanishka Rao、Krista Reymann、Michael Ryoo、Grecia Salazar、Pannag Sanketi、Pierre Sermanet、Jaspiar Singh、Anikait Singh、Radu Soricut、Huong Tran、Vincent Vanhoucke、Quan Vuong、Ayzaan Wahid、Stefan Welker、Paul Wohlhart、Jialin Wu、Fei Xia、Ted Xiao、Peng Xu、Sichun Xu、Tianhe Yu 和 Brianna Zitkovich 感谢他们为本项目做出的贡献；同时感谢 Fred Alcober、Jodi Lynn Andres、Carolina Parada、Joseph Dabis、Rochelle Dela Cruz、Jessica Gomez、Gavin Gonzalez、John Guilyard、Tomas Jackson、Jie Tan、Scott Lehrer、Dee M、Utsav Malla、Sarah Nguyen、Jane Park、Emily Perez、Elio Prado、Jornell Quiambao、Clayton Tan、Jodexty Therlonge、Eleanor Tomlinson、Wenxuan Zhou 以及更广泛的 Google DeepMind 团队的帮助与反馈。
