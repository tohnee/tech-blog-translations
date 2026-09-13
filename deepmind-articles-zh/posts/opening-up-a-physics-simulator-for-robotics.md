---
title: "开放一款面向机器人学的物理模拟器"
title_en: "Opening up a physics simulator for robotics"
source: https://deepmind.google/blog/opening-up-a-physics-simulator-for-robotics/
site: deepmind
date: 2021-10-18
crawled: 2026-09-13
translated: 2026-09-13
---

# 开放一款面向机器人学的物理模拟器

> 原文：[Opening up a physics simulator for robotics](https://deepmind.google/blog/opening-up-a-physics-simulator-for-robotics/) · Google DeepMind

通过收购 MuJoCo 推进各地的研究

当你走路时，你的双脚与地面接触。当你写字时，你的手指与笔接触。物理接触是让我们能够与世界互动的关键。然而，尽管如此常见，接触却是一种出奇复杂的现象。接触发生在两个物体界面的微观尺度上，可以是柔软或坚硬的、有弹性或如海绵般的、光滑或黏滞的。难怪我们的指尖拥有[四种不同类型](https://courses.lumenlearning.com/boundless-biology/chapter/somatosensation/)的触觉传感器。这种微妙的复杂性使得模拟物理接触——机器人学研究中至关重要的一环——成为一项棘手的任务。

[MuJoCo 物理模拟器](https://mujoco.org/)丰富而高效的接触模型使它成为机器人学研究者的首选之一。今天，我们自豪地宣布，作为 [DeepMind 推进科学之使命](https://deepmind.com/about)的一部分，我们收购了 MuJoCo，并将[免费开放](https://mujoco.org/download)给所有人使用，以支持世界各地的研究。MuJoCo 已经在机器人学社区被广泛使用，包括作为 DeepMind 机器人团队的首选物理模拟器，它拥有丰富的接触模型、强大的场景描述语言和精心设计的 API。我们将与社区一起，在宽松许可证下继续把 MuJoCo 作为开源软件加以改进。在我们准备代码库的同时，我们正以预编译库的形式[免费提供](https://mujoco.org/download) MuJoCo。

均衡的接触模型。MuJoCo 是 **Mu**lti-**Jo**int Dynamics with **Co**ntact（带接触的多关节动力学）的缩写，它的接触模型恰到好处，能够准确而高效地捕捉相互接触物体的显著特征。与其他刚体模拟器一样，它避免刻画接触点形变的精细细节，而且常常以远快于实时的速度运行。与其他模拟器不同的是，MuJoCo 使用凸的[高斯原理](https://en.wikipedia.org/wiki/Gauss%27s_principle_of_least_constraint)来求解接触力。凸性保证了唯一解和定义良好的逆动力学。该模型还很灵活，提供了多个可调参数，能够近似范围广泛的接触现象。

**真实：**

像翻转陀螺（Tippe top）翻转这类复杂的接触相关现象，在 MuJoCo 中因其对接触的准确描述而自然涌现。

**MuJoCo：**

像翻转陀螺（Tippe top）翻转这类复杂的接触相关现象，在 MuJoCo 中因其对接触的准确描述而自然涌现。

一篇近期发表在 PNAS 上的[观点文章](https://www.pnas.org/content/118/1/e1907856118)探讨了机器人学模拟的现状，指出开源工具是推进研究的关键。作者的建议是开发和验证开源模拟平台，并建立开放、由社区维护的经过验证的模型库。基于这些目标，我们致力于把 MuJoCo 开发和维护为一个免费、开源、社区驱动且具备一流能力的项目。我们目前正在全力准备 MuJoCo 的完全开源，鼓励你从[新主页](http://mujoco.org/)下载该软件；如果你愿意贡献，请访问 [GitHub 仓库](https://github.com/deepmind/mujoco)。如有任何问题或建议，请[发邮件给我们](mailto:mujoco@deepmind.com)；如果你也热衷于推动逼真物理模拟的边界，[我们正在招聘](https://deepmind.com/careers/jobs/3242004)。我们无法承诺立刻解决所有问题，但我们渴望与大家一起，把 MuJoCo 打造成我们一直在等待的那款物理模拟器。

**DeepMind 中的 MuJoCo。** 我们的机器人团队一直在多个项目中使用 MuJoCo 作为模拟平台，主要通过我们的 [dm\_control](https://github.com/deepmind/dm_control) Python 工具栈。在下方的轮播中，我们精选了几个示例，展示 MuJoCo 可以模拟什么。当然，这些片段只代表研究者使用该模拟器的巨大可能性中的一小部分。更高清晰度的版本请点击[这里](https://www.youtube.com/playlist?list=PLstWnsTbb45eqXgVY2RhsFV6VeNsMFLS9)。

**真实的物理，没有捷径。** 由于许多模拟器最初是为游戏和电影等目的设计的，它们有时会走捷径，把稳定性置于准确性之上。例如，它们可能忽略陀螺力，或直接修改速度。这在优化场景中尤其有害：正如艺术家兼研究者 Karl Sims [最早观察到的](https://doi.org/10.1145/192161.192167)，进行优化的智能体可以迅速发现并利用这些对现实的偏离。与之相反，MuJoCo 是一个二阶连续时间模拟器，完整实现了运动方程。[牛顿摆](https://en.wikipedia.org/wiki/Newton%27s_cradle)这类熟悉却不平凡的现象，以及[贾尼别科夫效应](https://en.wikipedia.org/wiki/Tennis_racket_theorem)这类反直觉的现象，都会自然涌现。归根结底，MuJoCo 严格遵循支配我们世界的方程。

**真实：**

MuJoCo 能够准确捕捉牛顿摆中的冲量传播。

**MuJoCo：**

MuJoCo 能够准确捕捉牛顿摆中的冲量传播。

**真实（来源：NASA）：**

由角动量守恒引起的陀螺力造成了这个有趣的效应，此处展示于零重力环境中。

**MuJoCo：**

由角动量守恒引起的陀螺力造成了这个有趣的效应，此处展示于零重力环境中。

**可移植的代码，干净的 API。** MuJoCo 的核心引擎用纯 C 语言编写，这使它可以轻松移植到各种架构。该库产生确定性的结果，场景描述和模拟状态完全封装在两个数据结构中。它们构成了重建一次模拟所需的全部信息，包括中间阶段的结果，从而便于访问其内部。该库还提供了对常用量的快速便捷计算，如运动学雅可比矩阵和惯性矩阵。

**强大的场景描述。** MJCF 场景描述格式使用级联默认值——避免大量重复取值——并包含现实世界机器人部件对应的元素，如等式约束、动作捕捉标记、肌腱、执行器和传感器。我们的长期路线图包括将 MJCF 标准化为开放格式，把它的用途扩展到 MuJoCo 生态系统之外。

**生物力学模拟。** MuJoCo 包含两个强大功能，支持人类和动物的肌肉骨骼模型。空间肌腱布线（包括绕骨骼缠绕）意味着施加的力可以被正确分配到各个关节，描述复杂效应，例如[胫骨](https://www.youtube.com/watch?v=wyiJw034ssA)实现的[膝关节](https://www.oxfordreference.com/view/10.1093/acref/9780198568506.001.0001/acref-9780198568506-e-4405)可变[力臂](https://www.oxfordreference.com/view/10.1093/acref/9780198568506.001.0001/acref-9780198568506-e-4405)。MuJoCo 的肌肉模型捕捉了生物肌肉的复杂性，包括激活状态和力-长度-速度曲线。

一条被肌腱上施加的力驱动而摆动的模拟人腿。注意胫骨如何沿股骨滑动。基于 Lai, Arnold & Wakeling (2017)。

一篇近期发表在 PNAS 上的[观点文章](https://www.pnas.org/content/118/1/e1907856118)探讨了机器人学模拟的现状，指出开源工具是推进研究的关键。作者的建议是开发和验证开源模拟平台，并建立开放、由社区维护的经过验证的模型库。基于这些目标，我们致力于把 MuJoCo 开发和维护为一个免费、开源、社区驱动且具备一流能力的项目。我们目前正在全力准备 MuJoCo 的完全开源，鼓励你从[新主页](http://mujoco.org/)下载该软件；如果你愿意贡献，请访问 [GitHub 仓库](https://github.com/deepmind/mujoco)。如有任何问题或建议，请发邮件给我们；如果你也热衷于推动逼真物理模拟的边界，[我们正在招聘](https://deepmind.com/careers/jobs/3242004)。我们无法承诺立刻解决所有问题，但我们渴望与大家一起，把 MuJoCo 打造成我们一直在等待的那款物理模拟器。

**DeepMind 中的 MuJoCo。** 我们的机器人团队一直在多个项目中使用 MuJoCo 作为模拟平台，主要通过我们的 [dm\_control](https://github.com/deepmind/dm_control) Python 工具栈。在下方的轮播中，我们精选了几个示例，展示 MuJoCo 可以模拟什么。当然，这些片段只代表研究者使用该模拟器的巨大可能性中的一小部分。更高清晰度的版本请点击[这里](https://www.youtube.com/playlist?list=PLstWnsTbb45eqXgVY2RhsFV6VeNsMFLS9)。

![模拟的人形机器人踢足球，每队两名球员，一队为红色，一队为蓝色。红队成功防守了蓝队的进攻，并最终攻入一球。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/mujoco_01.gif)

![一个模拟的类犬形体在平面上奔跑。奔跑时我们可以瞥见其动画骨骼的 X 光视角，骨骼刻画得非常精细。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/mujoco_03.gif)

![一个模拟的人形机器人保持倒立。它明显在努力维持姿势，但不断调整姿态以免摔倒。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/mujoco_04.gif)

![一个模拟的人形机器人接住以各种角度和速度抛来的球。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/mujoco_05.gif)

与社区中的其他人一样，我们的机器人团队已经在多个项目中把 MuJoCo 用作模拟平台。在上面的合集中，我们精选了几个示例，展示这一工具在实际使用中的样子。当然，这些视频片段只代表机器人学家使用该模拟器推进研究的巨大可能性中的一小部分。
