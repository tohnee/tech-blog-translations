---
title: "ORA：开放机器人使用智能体"
title_en: "ORA: Open Robot-Use Agents"
date: 2026-10-15
source: https://haoailab.com/blogs/ora/
crawled: 2026-11-16
translated: 2026-11-16
---

# ORA：开放机器人使用智能体

> 原文：[ORA: Open Robot-Use Agents](https://haoailab.com/blogs/ora/) · Hao AI Lab @ UCSD

# ORA：开放机器人使用智能体

一套开放的机器人使用 harness（ORA，开放机器人使用智能体），把开放权重语言模型接到机器人上。

2026 年 10 月 15 日 · ORA Team

目录

* [引言](#intro)
  + [为什么需要机器人使用智能体](#why)
  + [ORA 的位置](#landscape)
* [ORA 如何工作](#method)

  * [提示词包](#)
  * [本次运行中的 20 个工具](#)
  * [上下文管理](#)+ [环境与观测](#sub-env)
  + [提示词包](#sub-prompt)
  + [工具套件](#sub-tools)
  + [上下文管理](#sub-context)
* [结果](#results)
  + [RoboTwin](#res-robotwin)
  + [LIBERO](#res-libero)
  + [LIBERO-Pro](#res-pro)
  + [RoboDojo：初次扫描](#res-robodojo)
  + [真机上的初步结果](#real)
  + [成本](#cost)
* [分析：harness 贡献了什么](#analysis)
  + [从经验中学习](#an-learn)
  + [精确的任务指令与成功判据很重要](#cs-task)
  + [感知工具有助于发现和定位物体](#cs-perception)
  + [精确的常量与测量](#cs-measure)
  + [解释被拒绝的动作有助于恢复](#cs-feedback)
* [局限](#limitations)
* [致谢](#ack)
* [引用](#citation-sec)
* [参考文献](#references)

[代码](https://github.com/hao-ai-lab/ORA)[附录](https://freemty.github.io/ora/appendix/)[图集 · 153 个回合](https://freemty.github.io/ora/gallery/)

**TL;DR：** ORA 是一套开放的机器人使用智能体 harness，让开放权重语言模型**完全零样本地操作机器人：不用 VLA、不做机器人训练、不用任务专用记忆**，在 RoboTwin 与 LIBERO-Pro 上的成绩（按官方成功判据为 69.2% 与 81.4%）足以与基于前沿模型构建的智能体相比。它靠的是一套为物理世界机器人任务设计的 harness：精确的任务与环境上下文、用于感知和运动的工具，以及上下文管理。

[![](img/i-aa2245c958ee.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/ora--img--videos--ora-teaser.mp4)

**图 1.** 开放权重模型 DeepSeek-V4.1-Flash 通过 ORA 零样本操作机器人。按 DeepSeek 的 API 非高峰价格、使用估算的缓存命中率估算的模型 token 成本：此处所示 40 个任务平均每个已解决任务 $0.13，含失败尝试在内每个已解决基准用例 $0.30–$0.35。这些是按 API 价格折算的估计值，不是我们实际的自托管成本；GPU 与模拟器成本未计入（见[成本](#cost)）。

(a) RoboTwin C2R

50 个任务 · 250 个用例

成功率（%）

0255075100

1. *69.2*ORADeepSeek**ORA + DeepSeek-V4.1-Flash · 69.2%**我们的 harness + 开放权重模型 · 无 VLA、无机器人训练、无任务记忆173/250 个用例成功；没有有效结果的计为失败。
2. *62.4*GPT-5.5RPent**RPent + GPT-5.5 · 62.4%**RPent harness + 语言模型 + VLA + 任务专用记忆按 RPent 发布；156/250 个结果有报告。
3. *58.4*Opus-4.7RPent**RPent + Opus-4.7 · 58.4%**RPent harness + 语言模型 + VLA + 任务专用记忆按 RPent 发布；报告 250 个用例。
4. *50.4*LingBotVLA**LingBot-VLA · 50.4%**VLA，在机器人演示上训练按 RPent 发布；未报告计数。
5. *47.9*π0.5**π0.5 · 47.9%**VLA，在机器人演示上训练按 RPent 发布；未报告计数。
6. *20.7*GR00TN1.7**GR00T-N1.7 · 20.7%**VLA，在机器人演示上训练按 RPent 发布；未报告计数。

(b) LIBERO-Pro

8 个 Task 与 Swap 套件 · 800 个用例

成功率（%）

0255075100

1. *81.4*ORADeepSeek**ORA + DeepSeek-V4.1-Flash · 81.4%**我们的 harness + 开放权重模型 · 无 VLA、无机器人训练、无任务记忆651/800 个用例成功；没有有效结果的计为失败。
2. *92.63*AstraRPent [a]**RPent + GPT-6 Astra [a] · 92.63%**RPent harness + 语言模型 + VLA + 任务专用记忆按 RPent 发布；741/800 个结果有报告。
3. *82.4*Opus-4.7RPent**RPent + Opus-4.7 · 82.4%**RPent harness + 语言模型 + VLA + 任务专用记忆按 RPent 发布；报告 800 个用例。
4. *75.13*GPT-5.5RPent**RPent + GPT-5.5 · 75.13%**RPent harness + 语言模型 + VLA + 任务专用记忆按 RPent 发布；报告 800 个用例。
5. *72.63*FlashRPent [b]**RPent Flash Mode [b] · 72.63%**RPent harness + Molmo2-8B + VLA + 已发布的任务专用记忆按 RPent 发布；581/800 个结果有报告。
6. *70.63*QwenRPent**RPent + Qwen3.6 27B · 70.63%**RPent harness + 开放权重模型 + VLA + 任务专用记忆按 RPent 发布；565/800 个结果有报告。
7. *50.0*πRLinf**π\_RLinf · 50.0%**VLA，机器人演示 + 强化学习按 RPent 发布；未报告计数。
8. *11.0*π0.5**π0.5 · 11.0%**VLA，在机器人演示上训练按 RPent 发布；未报告计数。
9. *6.3*AtomVLA**AtomVLA · 6.3%**VLA，在机器人演示上训练按 RPent 发布；未报告计数。

ORA harness（我们的）+ 开放权重模型，零样本RPent 智能体 harness + 语言模型 + VLA + 任务专用记忆VLA 策略与其它方法

**图 2.** 在 (a) RoboTwin C2R（250 个用例）与 (b) LIBERO-Pro（800 个用例）上的成功率，使用与 RPent 相同的用例列表[[1]](#ref-rpent)。ORA 对每个用例都是零样本运行，不使用演示或任务专用记忆。基线成绩来自 RPent 的排行榜。[a] Astra 使用冻结的记忆批次。[b] Flash Mode 使用已发布的记忆并报告十个 seed 中的最佳。完整协议与数值见[附录](https://freemty.github.io/ora/appendix/)。

评测用例与基线模型

RoboTwin C2R（clean-to-randomized）覆盖 50 个任务，每个在随机化场景中跑 5 个 seed。LIBERO-Pro 覆盖八个 Task 与 Swap 套件，每个含 10 个任务、10 个 seed。ORA 的成功率统计每一个用例。

RPent 把一个语言模型、一个 VLA 和在一轮早期探索中收集的任务专用记忆组合起来。模型包括 GPT-5.5、Opus-4.7、GPT-6 Astra 与开放权重的 Qwen3.6-27B[[2]](#ref-qwen36)。端到端 VLA 基线为 π0.5[[3]](#ref-openpi)、π\_RLinf[[4]](#ref-pirl)、GR00T-N1.7[[5]](#ref-gr00t)、LingBot-VLA[[6]](#ref-lingbot) 与 AtomVLA[[7]](#ref-atomvla)。RPent Flash Mode 使用 Molmo2-8B[[8]](#ref-molmo2) 与已发布的记忆。

这些比较的是完整系统，它们的工具、记忆与协议各不相同。成功率采用官方成功判据，而该判据可能高估任务完成度；见[局限](#limitations)。

## 引言[#](#intro)

**ORA** 是一套开放的机器人使用智能体 harness，使 DeepSeek-V4.1-Flash[[9]](#ref-deepseek) 这样的开放权重模型能够解决机器人任务（[图 3](#fig-tui)）。它在 RoboTwin 上领先于基于闭源前沿模型构建的智能体，在 LIBERO-Pro 上也很接近（[图 2](#fig-main)）。下面我们说明为什么机器人使用需要由开放模型驱动的智能体，以及 **ORA** 在现有方法中的位置。

[![](img/i-cfeb6932ec6e.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/ora--img--videos--ora-tui-C2.mp4)

**图 3.** ORA 在一个 RoboDojo[[10]](#ref-robodojo) 任务上工作。左：智能体的终端，模型在这里观察、推理并调用工具。右：机器人的相机。任务要求把方块按蓝、黄、橙自下而上叠起；模型在第 1 轮失败后于第 2 轮成功。画面由该次运行的记录重放，动作已加速。

### 为什么需要机器人使用智能体[#](#why)

LLM 智能体现在承担了大量数字化工作，包括编程[[11]](#ref-sweagent)与计算机操作——即计算机使用智能体（CUA）[[12]](#ref-cua)[[13]](#ref-opencua)。然而，现有大多数机器人策略——例如视觉-语言-动作模型（VLA）[[14]](#ref-rt2)[[15]](#ref-openvla)与世界动作模型（WAM）[[16]](#ref-dreamzero)——仍依赖机器人专用训练数据，这些数据通过遥操作[[17]](#ref-aloha)、UMI[[18]](#ref-umi) 这类手持夹爪，或从第一人称视频[[19]](#ref-egomimic)中采集。另一条路是建立在现有 LLM 智能体的推理与工具调用之上。正如近期一场演讲所问：一个足够强的智能体，能否只凭机器人的说明书就操作它（[图 4](#fig-slide)）[[20]](#ref-jwang)？

![幻灯片：通用机器人？假设 GPT-9.8 + 智能体控制 + 任意机器人 + 它的说明书。](img/i-a0a702f44835.jpg)

**图 4.** 来自 Jianyuan Wang 在 IMW 2026 关于通用机器人的演讲；图片来源[[20]](#ref-jwang)。

![GPT-6 Astra 对比 Fable 5.1 在直接机器人控制上的表现：完成率与 API 成本的关系，含机器人相机视角。](img/i-951ff4bc9b55.jpg)

**图 5.** 用 GPT-6 Astra 零样本直接控制机器人；图片来源[[21]](#ref-chooi)。

这提示我们把智能体循环带入物理世界，正如近期的机器人使用智能体[[22]](#ref-isola)所做：一次工具调用让机器人移动，模型对所见进行推理，下一帧相机画面开启下一轮。与此同时，GPT-6 Astra 这类前沿模型已展示出很强的零样本直接机器人控制能力（[图 5](#fig-astra)）[[21]](#ref-chooi)，近期也有多个用这种方式操作机器人的演示[[23]](#ref-cpr)[[24]](#ref-robocurve)[[25]](#ref-waddle)。

但开放权重模型在这方面几乎还没被测试过；而机器人使用需要它们，原因有二。第一，要理解语言模型在物体操作上能做到多好、以及如何改进，我们需要大量可复现的数据，这意味着我们要能自己服务、以可接受的成本做实验的模型，而不是支付前沿模型的 API 价格。第二，一个基于 LLM 的已部署机器人系统必须足够快、足够高效，能在本地硬件上运行。这需要一个小到可以部署的开放模型，以及只有开放模型才负担得起采集的任务数据。

### **ORA** 的位置[#](#landscape)

用学习模型控制机器人的方法可分为四类。它们的区别在于语言模型扮演的角色，以及它多久做一次决策（[表 1](#tab-taxo)）。

视觉-语言-动作（VLA）模型[[14]](#ref-rt2)[[3]](#ref-openpi)[[15]](#ref-openvla)，以及更近期、还会预测未来视频的世界动作模型[[16]](#ref-dreamzero)[[26]](#ref-gigaworld)，在每个控制步把相机图像与指令映射为动作，并在最大的机器人数据集上训练。由于视觉-语言骨干被微调成了输出动作的视觉运动策略，这些系统几乎没用上它作为智能体推理与行动的能力——例如在移动前先测量、提前规划数步，或在失败后改变做法。

一个常见的应对是在学习策略之上加一个语言模型作为规划器，即 System 2 / System 1 设计[[27]](#ref-saycan)[[28]](#ref-hirobot)[[29]](#ref-helix)[[5]](#ref-gr00t)。语言模型把任务拆成步骤，策略负责执行。在 RPent[[1]](#ref-rpent) 中，语言模型借助任务专用记忆指挥一个 VLA 策略。模型自己也能下达某些动作指令，但大部分操作仍由在机器人演示上训练的 VLA 完成。

第三类让语言模型把策略写成代码。Code as Policies[[30]](#ref-cap) 把场景与任务变成调用感知与控制原语的程序。CaP-Agent0[[31]](#ref-capx)、ASPIRE[[32]](#ref-aspire) 与 RATs[[33]](#ref-rats) 增加了一个运行程序、读取结果并修改程序的智能体；ASPIRE 与 RATs 还会保留有效的技能。这些方法不需要机器人演示，运行也很经济：每个任务只调用模型一次或几次，之后程序自行运行。代价是程序以一个或少数几个开环片段执行。要写对往往需要试跑（例如 ASPIRE 会在单独的 seed 上学习技能再接受测试），而且在两次修改之间没有模型观察场景：程序只通过写进去的检查做反应，这限制了它向新场景的迁移能力。

第四类直接运行智能体循环，采用 ReAct 风格[[34]](#ref-react)：模型推理、调用工具、读取结果，再次决策。前沿模型已经用这种方式控制机器人[[21]](#ref-chooi)[[23]](#ref-cpr)，Guava[[35]](#ref-guava)、OpenRUA[[36]](#ref-openrua)、Agent as Policy[[37]](#ref-agp) 与 Robo-Harness K1[[38]](#ref-k1) 是为这类智能体打造的 harness。当模型自己下达每一条底层指令时，某项研究中最好的模型在 LIBERO 上只达到 5.5%[[23]](#ref-cpr)。**ORA** 属于这一类。每次工具调用覆盖一段有界的运动，由控制器执行，模型在下一次决策前看到结果。它在每一步都要调用模型，因此在今天的延迟与价格下，这一类比一次写好的程序更慢、更贵（见成本与局限）。

| 类别 | 语言模型做什么 | 多久决策一次 | 是否需要机器人数据 | 例子 |
| --- | --- | --- | --- | --- |
| VLA 与世界动作模型 | 被训练进运动策略 | 每个控制步 | 大规模机器人数据集 | RT-2[[14]](#ref-rt2)、π0、π0.5[[3]](#ref-openpi)、OpenVLA[[15]](#ref-openvla)、DreamZero[[16]](#ref-dreamzero) |
| 规划器 + 学习策略（System 2 / System 1） | 逐步指挥一个学习策略 | 策略完成一步时 | 训练策略所需的演示 | SayCan[[27]](#ref-saycan)、Hi Robot[[28]](#ref-hirobot)、Helix[[29]](#ref-helix)、GR00T N1[[5]](#ref-gr00t)、RPent[[1]](#ref-rpent) |
| 代码即策略 | 在感知与控制原语之上写程序，运行并修改 | 每个任务一次或几次 | 无 | Code as Policies[[30]](#ref-cap)、CaP-Agent0[[31]](#ref-capx)、ASPIRE[[32]](#ref-aspire)、RATs[[33]](#ref-rats) |
| 机器人使用智能体（ReAct 循环） | 调用工具、读取结果、再次决策 | 每次工具调用一次 | 无 | Guava[[35]](#ref-guava)、OpenRUA[[36]](#ref-openrua)、Agent as Policy[[37]](#ref-agp)、Robo-Harness K1[[38]](#ref-k1)、ORA |

**表 1.** 用学习模型控制机器人的四类方法，按语言模型的角色与决策频率划分。有些系统会组合多类方法。

## **ORA** 如何工作[#](#method)

**ORA** 沿用 Claude Code[[39]](#ref-claudecode) 与 Pi[[40]](#ref-pi) 这类编程智能体的做法：任务以 ReAct 循环[[34]](#ref-react)运行，每一轮模型读取输入、思考并做一次工具调用；动作改变世界的状态，返回的内容成为下一轮的输入（[图 6](#fig-system)）。与那些智能体一样，它有提示词包、工具与上下文管理，但对机器人来说，每一样都要做更多事。

第一，**提示词包**必须描述每个本体（embodiment）的身体与任务：机器人的坐标系、每条指令移动的点、夹爪的常量，以及详细写出的任务成功判据。第二，**工具套件**必须帮助模型在物理环境中感知和行动。这里没有 shell，也没有文件读写；模型只能通过相机与机器人传感器看世界，因此它需要测量真实场景的感知工具，以及作用于环境、并在每次动作后准确回报发生了什么的动作工具。第三，与编程智能体相比，机器人使用智能体会收到大量冗余的视觉观测与环境数据，所以**上下文管理**必须承载重得多的输入：每一轮都加入相机图像，而模型又会反复回到早先的结果。输入必须保持小，同时不能丢掉那些结果，也不能打断 prompt cache。

另一侧是环境：一个 supervisor 会对照机器人的限位检查每个动作，执行它并返回一份实测回执。自始至终，模型只通过 RGB 与深度图像感知场景，从不见模拟器的特权信息：成功判据的代码、物体的 ground truth 或模拟器接触信息。

**DeepSeek-V4.1-Flash**开放权重

ORAharness

##### 提示词包

系统策略证据规则基准边界机器人卡片任务工具 schema本轮事实

##### 工具套件*本次运行 20 个*

lookvision\_ground按名称查找vision\_segment在点上取 maskmark\_point像素 → 世界

measuregeometry\_query相机 ↔ 世界compute向量运算grasp\_plan抓取提案

actmove\_pose移动到某个位姿set\_gripper开或合grasp\_execute执行一次抓取

还有

observealign\_planmove\_torotate\_wristrotate\_pitchrecover\_posewait\_tickscheck\_taskfinish\_episodereport\_issueartifact\_read

##### 上下文管理

本轮观测与回执，完整最近若干轮逐字保留更早的轮次图像 → 引用历史摘要已完成的轮 → 检查点

action

每一轮

observation

信任边界

环境

多种本体

![](img/i-92d8ba334676.jpg)ARX X5RoboDojo · 双臂![](img/i-5346794e6840.jpg)ALOHARoboTwin · 双臂![](img/i-f5475c341b45.jpg)FrankaLIBERO · 单臂

![](img/i-6f0c8af3c62f.jpg)![](img/i-1935b668ab81.jpg)**观测**RGB-D、机器人状态、回执成功判据

**图 6.** LLM、ORA 与环境之间的交互循环。每一轮，模型读取提示词包与上下文、思考并调用一个工具；动作改变世界，返回的观测——如同每个工具结果一样——加入上下文供下一轮使用。提示词包与上下文每轮重建、最新的材料在前，构成模型收到的全部内容；另一侧的环境持有机器人、每轮返回观测，并保留成功判据。点击任意部分可查看细节。

### 环境与观测[#](#sub-env)

我们在三个仿真基准上运行 **ORA**，每个都有自己的机器人（[图 7](#fig-cards)）。它们在模拟器及其世界坐标系、机械臂、每条指令移动的点、夹爪几何、相机以及成功判定方式上都不同。RoboDojo[[10]](#ref-robodojo) 运行在 Isaac Sim[[41]](#ref-isaacsim) 上，使用双臂 ARX X5；RoboTwin[[42]](#ref-robotwin) 运行在 SAPIEN[[43]](#ref-sapien) 上，使用双臂 ALOHA；LIBERO[[44]](#ref-libero) 与 LIBERO-Pro[[45]](#ref-liberopro) 通过 robosuite[[47]](#ref-robosuite) 运行在 MuJoCo[[46]](#ref-mujoco) 上，使用单臂 Franka。

循环、工具种类与模型是共享的；只有控制器按各机器人适配。差异通过一个基准边界与一张机器人卡片以文本形式到达模型。有了它们，一个模型就能跑三种机器人。卡片与边界把智能体推理所需的身体与场景细节交给它，例如每条指令移动的点、手指在哪里接触、钳口开多宽；点开下面的卡片即可看到。

![](img/i-92d8ba334676.jpg)ARX X5RoboDojo固定底座 ARX X5：左 6-DoF 臂，右 6-DoF 臂；平行钳口夹爪。相机：`head` 为固定 RGB-D；`left_wrist`、`right_wrist` 为随臂移动的 RGB-D。

|  |  |
| --- | --- |
| 模拟器 | Isaac Sim[[41]](#ref-isaacsim) |
| 我们运行的任务 | 42 个多阶段桌面任务，初次扫描 |
| 机器人 | ARX X5，两条 6-DoF 臂 |
| 指令移动的点 | 腕部法兰；不加偏移 |
| 接近轴 / 钳口闭合轴 | [1, 0, 0] / [0, 1, 0] |
| 手指接触位置 | 沿接近轴 0.150 m 处的钳口接触中心 |
| 钳口全开 | 88.8 mm |
| 相机 | 一台固定，每腕各一台；640 × 480 |
| 官方成功判据 | 基准的 reward manager |

![](img/i-5346794e6840.jpg)ALOHARoboTwin固定底座 ALOHA-AgileX：左 6-DoF 臂，右 6-DoF 臂；平行钳口夹爪。`right_tcp` 是被控参考点，距法兰 0.12 m；指令已直接以它为目标。

|  |  |
| --- | --- |
| 模拟器 | SAPIEN[[43]](#ref-sapien) |
| 我们运行的任务 | 50 个任务，各 5 个随机化场景 |
| 机器人 | ALOHA-AgileX，两条 6-DoF 臂 |
| 指令移动的点 | 法兰之外 0.12 m 的工具点 |
| 接近轴 / 钳口闭合轴 | [1, 0, 0] / [0, 1, 0] |
| 手指接触位置 | 工具点周围 −50 到 36 mm 的手指范围 |
| 钳口全开 | 94.9 mm，见 `grasp_plan` 的帮助 |
| 相机 | 两台固定，每腕各一台；320 × 240 |
| 官方成功判据 | 任务的 `check_success` |

![](img/i-f5475c341b45.jpg)FrankaLIBERO / LIBERO-Pro固定底座 Franka Panda：右 7-DoF 臂；平行钳口夹爪。`right_grip_site` 是被控参考点，距末端执行器根部 0.097 m；指令已直接以它为目标。

|  |  |
| --- | --- |
| 模拟器 | MuJoCo[[46]](#ref-mujoco)（robosuite[[47]](#ref-robosuite)） |
| 我们运行的任务 | 40 个任务 × 10 个 seed；LIBERO-Pro 8 个套件 × 100 |
| 机器人 | Franka Panda，一条 7-DoF 臂 |
| 指令移动的点 | 末端执行器根部之外 0.097 m 的抓取点 |
| 接近轴 / 钳口闭合轴 | [0, 0, 1] / [1, 0, 0] |
| 手指接触位置 | 抓取点周围 −44 到 9 mm 的手指范围 |
| 钳口全开 | 80 mm |
| 相机 | 一台固定，一台在腕部；256 × 256 |
| 官方成功判据 | 环境的终止信号 |

**图 7.** 三种本体与各自机器人卡片的开头，逐字呈现。点开卡片可看它和基准边界告诉了模型什么；模型从不见成功判据的代码，只见它的是或否。

每次动作之后，环境返回一份观测（[图 8](#fig-obs)）。它包含每台相机的一张 RGB 图像及其标定、每条臂的实测位姿与夹爪状态、上一条动作的回执与剩余预算，并与该动作被选择时所依据的观测配对，因此模型可以比较前后。每台相机的深度图随观测一起存储，look 类工具在模型测量时读取它。

![头部相机，RGB](img/i-6f0c8af3c62f.jpg)

头部相机，RGB

![左腕，RGB](img/i-5fd3ef09ae94.jpg)

左腕，RGB

![右腕，RGB](img/i-9147403366f2.jpg)

右腕，RGB

![头部相机，深度](img/i-1935b668ab81.jpg)

头部相机，深度

模型收到的数据包（已删节）

* comparison
  + action\_input\_actual\_sequence 7
  + action\_result\_actual\_sequence 8
  + available true
  + instruction "Compare the retained ACTION INPUT ACTUAL with this ACTION RESULT ACTUAL before choosing the next tool."
* current\_actual
  + observation\_step 8
  + camera\_geometry
    - left\_wrist…
    - right\_wrist…
  + public\_robot\_facts
    - end\_effectors
      * right
        + pose\_xyz\_xyzw [0.001, -0.141, 0.934, -0.348, 0.619, 0.328, 0.623]
        + axes
          - approach\_world [0.018, -0.023, -1.0]
          - closing\_world [-0.84, 0.542, -0.028]
        + gripper
          - command\_target "close"
          - measured\_opening\_normalized 0.51
      * left
        + pose\_xyz\_xyzw [-0.358, -0.131, 1.09, -0.402, 0.581, 0.403, 0.582]
        + axes…
        + gripper…
    - cameras…
* last\_action\_effect
  + action "move\_pose"
  + action\_summary "right arm 1.6 mm / 0.6° from target, reached, TCP moved 163 mm"
  + detail…
* remaining\_budget
  + native\_actions\_remaining 352
  + native\_actions\_limit 400
  + robot\_decisions 75
  + model\_calls 185
* images
  + "ACTION RESULT ACTUAL · sequence 8 · head"
  + "ACTION RESULT ACTUAL · sequence 8 · left\_wrist"
  + "ACTION RESULT ACTUAL · sequence 8 · right\_wrist"

**图 8.** RoboDojo 上的一次观测，取自[图 3](#fig-tui) 那次运行的第 1 轮、第 8 步：模型收到的三张相机图像、look 类工具读取的头部相机深度图，以及随它们一起的数据包。

### 提示词包[#](#sub-prompt)

编程智能体在动手编辑之前会先读仓库与其中的说明；机器人使用智能体同样要在移动之前被告知足够多的环境信息。因此我们给它一个七层的提示词包（[图 6](#fig-system)）。于是新的本体无需训练：只需替换本体上下文。展开任意一层，即可读到模型在[图 3](#fig-tui) 那次运行中读到的内容。

1. **系统策略**，对每个机器人、每个任务都相同：轮次协议（只读调用可以批量执行；改变世界的调用必须单独一次）、每个推导出的数字都要交给 `compute`、较早的证据如何被替换为引用，以及各预算的含义。

   系统消息，Native Robot Policy v4，节选

   ```
   Turn protocol

   Read-only tools may be called sequentially or in one independent batch. A
   world-mutating tool must be the only tool call in its assistant response. Each
   accepted mutation ends the current turn; wait for the next actual observation
   before choosing another mutation.

   Arithmetic belongs in the advertised calculation capability, not in your own
   working. Whenever a number would be derived -- a residual, an offset along a
   direction, a quaternion unpacked, a sum of extents, a dot or cross product, a
   projection between image and world, a trigonometric value -- that derivation is
   part of how the action was chosen […]

   How this context reaches you

   Current actual evidence arrives complete on every turn. Earlier evidence is not
   guaranteed to stay in the form you first received it.

   A result that exceeds its inline budget is replaced by a status record carrying
   an exact reference to the complete original. […] Open the reference when you
   need what a past result said; call again when you need what is true now.

   What the reported allowances mean

   Every turn reports what remains of the current session round […]: accepted world
   mutations, model turns including read-only ones, and elapsed wall-clock seconds.
   […] keep enough in hand to witness the effect of your final mutation and to take
   the advertised closing step: an unverified last action and an unclosed episode
   are both worse than one attempt fewer.
   ```

   逐字摘自提示词；[…] 表示删节。
2. **证据规则**，也是共享的：把直接证据、推断、候选、已执行命令与已验证效果区分开；失败之后，改变下一次尝试所依赖的东西。

   Evidence-to-Action Invariants v5，节选

   ```
   Keep these states distinct:

   - **Direct evidence:** present in a current image, measurement or tool result.
   - **Inferred:** a task-relevant interpretation supported by observations.
   - **Candidate:** a proposed point, pose or action that has not executed.
   - **Executed:** a command the Runtime accepted and attempted.
   - **Verified:** a physical effect confirmed by a later observation.
   […]
   When something fails

   A refusal, an error or an unchanged world is evidence about the approach, not
   only about the tool. Before repeating anything, change what the attempt rests
   on: refresh the evidence its arguments came from, or take a different route to
   the same effect. An identical call against an unchanged premise is not a
   recovery, and when two attempts fail the same way the premise is what to test.
   ```

   逐字摘自提示词；[…] 表示删节。
3. **基准边界**，每个基准一份：世界坐标系与单位、桌面、相机、哪些信息保密，以及官方判定来自哪里。

   RoboDojo 环境边界，节选

   ```
   The scene is a simulated Isaac Sim tabletop in an episode-local world frame:
   `+X` (red), `+Y` (green) and `+Z` (blue), `+Z` upward, positions in metres.
   One 1.4 m by 1.1 m table stands with its top near z = 0.76 m (table body
   centred at z = 0.74 m). The robot is mounted on the table's `-Y` side, so
   `+Y` runs from the robot toward the far edge. […]

   Simulator object and actor state, ground-truth poses, segmentation, contacts,
   evaluator objects, reward internals, the success-predicate implementation,
   task source and the teleoperated source demonstrations are private and
   unavailable.

   Only RoboDojo's reward manager supplies the official Boolean verdict,
   read through the advertised verdict query at a valid state boundary […]
   Every robot command reserves up to a fixed number of native actions (20) from
   that allowance; the receipt reports how many were consumed, and a refused
   command consumes none.
   ```

   逐字摘自提示词；[…] 表示删节。
4. **机器人卡片**，每个机器人一份：机械臂、每条指令移动的点、夹爪的轴与常量，以及相机（[图 7](#fig-cards)）。

   ARX X5 机器人卡片，节选

   ```
   Identity and topology
   Fixed-base ARX X5: left 6-DoF arm, right 6-DoF arm; parallel-jaw grippers.

   Controlled points
   `left_link6` is the left arm's controlled point, its wrist flange, not a fingertip;
   commands and measured poses already refer to it, so add no offset. […]

   End-effector axes
   `left_link6` local approach [1, 0, 0]; jaw-closing line [0, 1, 0]. Local Z is
   perpendicular to both. Current world directions are supplied with measured state.

   Gripper semantics
   […] The jaw contact centre is +0.1501 m along the approach axis from `left_link6`. […]
   Nominal full-open pad separation is 88.8 mm. Physical pad aperture remains
   uncalibrated. The public encoder reading is the mean of both finger joints on the
   normalized command scale (empty-close reference about 0.185, full-open 1); it is
   not measured pad separation […]

   Sensors and cameras
   `head`: fixed RGB-D; use calibration from the same observation.
   `left_wrist`: arm-mounted moving RGB-D; use calibration from the same observation.
   `right_wrist`: arm-mounted moving RGB-D; use calibration from the same observation.
   ```

   逐字摘自提示词；[…] 表示删节。
5. **任务与完成契约**，每个任务一份：基准自己的指令（原样复制），以及一份用平实语言重述官方成功判据的契约。

   任务消息，RoboDojo stack\_blocks\_by\_language，节选

   ```
   stack the blocks from bottom to top in the order ofblue, yellow, and orange, then reset the robot arm.

   That sentence is the objective, in its exact words. […]

   Public completion contract for this task:

   - The three blocks must end up in one stack in the colour order the instruction
     gives, read from the bottom up: the first colour named at the bottom, the
     second in the middle and the third on top.
   - Each block must sit on top of the block below it, centred over it rather than
     set off toward one side or placed beside it.
   - Both arms must be back at the poses they held when the episode reset, at the
     same instant that everything else in this contract is true.
   ```

   逐字摘自提示词；[…] 表示删节。
6. **工具 schema**，每个工具一份：何时使用、它会改变并返回什么、它不做什么，以及它如何拒绝。

   20 个 schema 之一：vision\_ground，已删节

   ```
   {"name": "vision_ground",
    "description": "Retrieve up to three inspectable text-grounded target proposals from one selected
     current RGB-D camera. Use when: task language names an object or part and the scene-level search
     space should be reduced before the policy makes its own identity decision […] Treat the returned
     set as recall-oriented proposals: top rank and backend score are within-call ordering signals, not
     an oracle. […] Does not: choose the correct candidate, guarantee that rank 0 is foreground, combine
     cameras, expose object ground truth […] On error: Refused: max_candidates outside 1 to 3 […]",
    "parameters": {"camera": {"enum": ["head", "left_wrist", "right_wrist"]},
                   "text": {"type": "string", "maxLength": 120,
                            "description": "Short visible object or part description, never a simulator identifier."},
                   "max_candidates": {"minimum": 1, "maximum": 3, "default": 3}}}
   ```

   逐字摘自提示词；[…] 表示删节。
7. **本轮事实**，每轮一份：预算、最初的相机图像，以及本轮内保持不变的内容，例如固定相机的标定。

   第一次观测与本轮静态事实，第 1 轮，已删节

   ```
   {"session_round": {"kind": "session_round_start", "round": 1, "total_rounds": 3, "budget_scope": "per_round",
      "instruction": "This is a new independent environment round in the same AgentSession. […] Prior scene state
      and coordinates are stale. Re-ground from the current observation and retain useful experience."},
    "remaining_budget": {"model_calls": 200, "robot_decisions": 80, "native_actions_remaining": 400,
      "native_actions_limit": 400, "wall_time_s": 21091.7}, …}
   INITIAL ACTUAL · sequence 0 · head / left_wrist / right_wrist          [three images, 640×480]

   {"round_static_facts": {"current_actual": {
      "camera_geometry": {"head": {"intrinsic_cv": [[288.13, 0.0, 320.0], [0.0, 288.13, 240.0], [0.0, 0.0, 1.0]],
          "camera_origin_world_m": [0.0, -0.41, 1.308], "extrinsic_cv": […]}, "left_wrist": {…}, "right_wrist": {…}},
      "conventions": {"camera_coordinates": "OpenCV: x right, y down, z forward", "depth_unit": "metres", …},
      "view_dimensions": {"head": {"width": 640, "height": 480}, …}, "depth_delivery": "on_demand", …},
    "rule": "An observation in this round leaves out each current_actual field whose current value is
      byte-identical to its value here. […]"}}
   ```

   逐字摘自提示词；[…] 表示删节。

这个包说明如何看、如何动。它从不包含解法、物体坐标或成功测试。其中三层是机器人任务特有的：机器人卡片、从基准原样复制的任务指令，以及完成契约。这些组件的作用见[分析](#analysis)。

### 工具套件[#](#sub-tools)

每个工具覆盖模型无法独自可靠完成的事情（[图 9](#fig-toolbox)）。模型只看到工具测得的东西。

look`vision_ground`按名称查找`vision_segment`在点上取 mask`mark_point`像素 → 世界`observe`重开或叠加图像

measure`geometry_query`相机 ↔ 世界`compute`向量运算`grasp_plan`抓取提案`align_plan`可达的站位位姿

act`move_pose`移动到某个位姿`set_gripper`开或合`grasp_execute`执行一次抓取`move_to`移动并保持姿态`rotate_wrist`转动钳口线`rotate_pitch`倾斜接近方向`recover_pose`回到命名位姿`wait_ticks`让时间流逝

episode`check_task`询问官方判定`finish_episode`带理由结束本轮`report_issue`报告接口缺陷`artifact_read`重开已存结果

**图 9.** [图 3](#fig-tui) 那次运行的 20 个工具，按功能分组。点击工具可查看其 schema、一次真实调用与返回内容。

语言模型能说出它看到了什么，却无法精确指出来，这就是 DeepSeek 所说的引用鸿沟[[48]](#ref-dsvp)。look 类工具缩小这个鸿沟：`vision_ground` 与 `vision_segment` 为一个命名物体或几个点出的像素返回 SAM 3[[49]](#ref-sam3) 的 mask，`mark_point` 测量单个像素，每个结果都在深度图上查值，于是模型得到以米为单位的位置（[图 10](#fig-tools)）。

`vision_ground`按名称找物体 · LIBERO-Pro

![LIBERO-Pro 场景中框出的三个候选瓶子](img/i-37ff636e06eb.jpg)

`vision_ground(camera="agentview", text="ketchup bottle")`

三个候选瓶子，各有 mask 与由深度测得的中心。前两个分数很接近（0.69 与 0.67），所以仅凭排序无法确定哪瓶是番茄酱；模型在抓取前比较了特写。

`vision_segment`对模型指出的位置取 mask · RoboDojo

![腕部视图上一个点出的像素与黄色方块的 mask](img/i-e2a03f31930e.jpg)

`vision_segment(camera="left_wrist", points_uv=[[215, 412]])`

一个覆盖黄色方块的 mask：中心 (−0.355, −0.142, 0.800) m，36 × 37 mm，高出 0.765 m 处的表面 35 mm。而模型上一轮在头部视图上选的那个点落在了桌面上。

`mark_point`测量单个像素 · RoboTwin

![在 RoboTwin 头部相机上沿鞋子标记的八个命名点](img/i-6d2332ebe320.jpg)

`mark_point(view="head_camera", point_ids=["shoe_a", …, "shoe_h"], …)`

沿鞋子八个点的世界坐标，全部由深度解算，在规划抓取之前给出它在桌面上的长度与朝向。

`grasp_plan`提出机械臂可达的抓取 · LIBERO-Pro

![在选定的瓶子上画出三个抓取候选](img/i-38557051eb8c.jpg)

`grasp_plan(target_ref="target-dade139…", max_candidates=3)`

由 Contact-GraspNet 在选定瓶子上给出的三个抓取，每个都按 Franka 夹爪给出 40.7 mm 的钳口开度，且全部可达。

**图 10.** LIBERO-Pro、RoboDojo 与 RoboTwin 上的四次工具调用，各附它返回给模型的图像与返回的数值。在[图 6](#fig-system) 中点击某个工具，可看[图 3](#fig-tui) 那次运行中的更多调用。

模型在推理中也会做几何运算，有时会错：35,270 条响应中有 12.2% 手工推导向量或旋转，还有三次运行在想从上方接近时把夹爪朝上指。`compute` 接管这类算术，而位姿可以按方向给出，例如竖直向下接近。

运动工具接受被控点的目标，从不接受关节目标。环境用 cuRobo[[50]](#ref-curobo) 解逆运动学并规划路径、执行它并返回回执；拒绝时会说明原因，例如直线路径只有 75% 可达。`grasp_plan` 用 Contact-GraspNet[[51]](#ref-cgn) 提出抓取，`grasp_execute` 把其中一次作为单个受监督序列执行。

`check_task` 返回官方的是或否，`finish_episode` 在错误无法挽回时提前结束一轮，`report_issue` 让模型指出 harness 的缺陷而不是归咎于自己的尝试。

这些组件的作用见[分析](#analysis)。

### 上下文管理[#](#sub-context)

编程智能体的一轮只增加几行文本；机器人的一轮增加三张相机图像、实测位姿和一份回执。上下文管理必须平衡三个彼此拉扯的目标。输入要短。每一个早先结果都必须能被精确恢复，因为模型常常需要很多轮之前的一个数字：当我们把每份观测截到约一半长度、对数字取整并丢掉限值时，RoboDojo 的成功从 27 轮中的 17 轮降到 10 轮。而输入的开头必须保持稳定，好让服务器的 prompt cache 持续命中，但每一次压缩都会打断它。

**ORA** 把输入分成四层，最新的在前（[图 6](#fig-system)）。展开任意一层，即可看到模型当时收到的内容。

1. **本轮**完整到达：上一条动作的回执、全部三张相机图像、实测位姿与夹爪状态、剩余预算，并与该动作被选择时所依据的观测配对。

   第 1 轮的一份观测，已删节

   * comparison
     + action\_input\_actual\_sequence 7
     + action\_result\_actual\_sequence 8
     + available true
     + instruction "Compare the retained ACTION INPUT ACTUAL with this ACTION RESULT ACTUAL before choosing the next tool."
   * current\_actual
     + observation\_step 8
     + camera\_geometry
       - left\_wrist…
       - right\_wrist…
     + public\_robot\_facts
       - end\_effectors
         * right
           + pose\_xyz\_xyzw [0.001, -0.141, 0.934, -0.348, 0.619, 0.328, 0.623]
           + axes
             - approach\_world [0.018, -0.023, -1.0]
             - closing\_world [-0.84, 0.542, -0.028]
           + gripper
             - command\_target "close"
             - measured\_opening\_normalized 0.51
         * left
           + pose\_xyz\_xyzw [-0.358, -0.131, 1.09, -0.402, 0.581, 0.403, 0.582]
           + axes…
           + gripper…
       - cameras…
   * last\_action\_effect
     + action "move\_pose"
     + action\_summary "right arm 1.6 mm / 0.6° from target, reached, TCP moved 163 mm"
     + detail…
   * remaining\_budget
     + native\_actions\_remaining 352
     + native\_actions\_limit 400
     + robot\_decisions 75
     + model\_calls 185
   * images
     + "ACTION RESULT ACTUAL · sequence 8 · head"
     + "ACTION RESULT ACTUAL · sequence 8 · left\_wrist"
     + "ACTION RESULT ACTUAL · sequence 8 · right\_wrist"

   取自该次运行自己的记录；… 表示删节。
2. **最近若干轮**逐字保留：最近两个动作步的图像保持内联，最近三个结果保持原样。

   第 2 轮的第一次交换，到第 30 轮时仍逐字保留，已删节

   ```
   assistant: Round 2. Key lesson from round 1: after releasing a block, retract straight up before any lateral motion, and verify build-spot reachability both arms can satisfy. The layout is the same. Let me re-localize the blue block.

   tool (vision_segment): {"camera": "head", "candidate_previews": [{"crop_xyxy": [316, 209, 400, 293], "image_index": 1, "position": 0, …}], "candidates": [{"backend_score": 0.973, "candidate_id": "T0", "localization": {"center_xyz_m": [0.075, -0.140, 0.800], "extent_xyz_m": [0.039, 0.040, 0.033], …}}]}

   [two returned images, as references]
   ```

   取自该次运行自己的记录；… 表示删节。
3. **更早的轮次**保留文本，但每四个动作步，它们的图像以及任何超过 50 KB 的结果都会被替换成精确引用；`observe` 或 `artifact_read` 可重开原始字节，而大结果会保留 2 KB 预览。

   第 1 轮最初的相机图像，到第 14 轮时已变成引用

   ```
   INITIAL ACTUAL · sequence 0 · head · latest at this message <recoverable_artifact>{"at":[1,0],"bytes":409641,"mime":"image/png","open":"observe","ref":"artifact://…/d663528e…","v":1}</recoverable_artifact>
   INITIAL ACTUAL · sequence 0 · left_wrist · latest at this message <recoverable_artifact>{"at":[1,0],"bytes":353088,"mime":"image/png","open":"observe","ref":"artifact://…/6fc7c0b4…","v":1}</recoverable_artifact>
   …
   ```

   取自该次运行自己的记录；… 表示删节。
4. **历史摘要**在输入超过约 150,000 token 后接管：同一个模型把一个已完成的轮折叠成一条记录，目标约 1,200 token，含官方结果、学到的东西，以及指向原始对话记录的引用。如果输入仍达到模型窗口的 80%，最旧的材料会被压缩到 65%，与 Claude Code[[39]](#ref-claudecode) 的做法相同。

   第 1 轮的检查点，从第 31 轮起读取，已删节

   * coverage
     + action\_step\_count 13
     + from\_action\_step\_index 0
     + through\_action\_step\_index 12
   * official\_verdict
     + round 1
     + passed false
     + instruction "This completed-round result is exact. Reflect on durable task-local lessons."
   * summary
     + confirmed\_facts
       - "Right-wrist measurement of the stranded block, re-projected into the head view, was self-consistent and placed it well beyond the table's far edge …"
     + current\_constraints
       - "The stranded block is beyond the table's far edge and outside the commanded workspace, so neither arm can retrieve it; …"
     + failed\_attempts
       - * failure "Right-arm retraction after releasing the block displaced the block instead of leaving it in place."
         * evidence "After the clearing move the block was absent from the drop point and later measured beyond the far table edge."
         * correction "Clear with a short upward move first and re-observe, rather than a long diagonal retraction past the release point."
       - …
     + do\_not\_repeat
       - "Do not resubmit world targets that already returned planner\_failed for the same arm without changing standoff, height or arm."
       - …
     + invalidated\_beliefs…
     + re\_ground\_next…
   * exact\_transcript
     + bytes 228007
     + open
       - tool "artifact\_read"
       - arguments
         * ref "artifact://…/26c825a2…"

   取自该次运行自己的记录；… 表示删节。

要看这三个目标如何共同起作用，[图 11](#fig-loop) 跟踪一次长会话：即[图 3](#fig-tui) 的 RoboDojo 叠方块任务，在同一场景上连续打三次，共 123 轮。

输入保持短。第 1 轮输入从 33k 增长到 162k token，在第 14、18 轮时，较早步骤的图像变成了引用。第 2 轮开始时第 1 轮仍是逐字的；到 180k token、第 31 轮之前，模型把第 1 轮折叠成一个检查点，含官方结果、事实与约束摘要、失败尝试与不要重复的事项，以及指向 228 KB 对话记录的引用。输入降到 59k。只有已完成的轮才被折叠，因此跑了 65 轮的第 2 轮增长到 253k token，其间较早的图像九次变成引用；它在第 96 轮之前以同样方式被折叠，从 261k 降到 58k，而第 3 轮 33 轮就完成了。

没有东西丢失。每个离开输入的图像或结果都变成指向精确存储字节的引用，由 `observe` 或 `artifact_read` 重开。在 250 个 RoboTwin 用例中，模型有 30 个用例里共 65 次重开了较早的证据。其中一个，它的左夹爪刚夹住锅的一个把手；为了规划右把手，它把内联预览被截断的完整 `grasp_plan` 结果——7,965 字节的 JSON——逐页读了回来。

前缀保持稳定。两次压缩之间，每个请求都逐字节扩展前一个请求，于是服务器可以复用缓存。这次会话中，122 个后续请求里有 104 个扩展了前一个；另外 18 个跟在一次压缩之后或开启新的一轮，它们占了 82% 的未缓存输入。整个会话估计的缓存命中率为 86%，与评测运行一致（见成本）。

第 1 轮25 轮 · 失败

第 2 轮65 轮 · 成功

第 3 轮33 轮 · 成功

检查点，已完成轮被折叠（第 31、96 轮）较早图像被替换为引用（第 14、18、32、39、48、55、65、71、75、81、85、101、107、111、117、122 轮）

每根柱是一轮，高度是提供方报告的输入 token 数。任选一轮，或选这些：

**1**分割方块**3**抓住黄色**6**移动被拒绝**7**换臂**17**侧向回撤**24**找回丢失的方块**25**放弃**26**第 1 轮的教训**31**检查点**89**判定**91**第 3 轮复用第 2 轮**96**第二个检查点**122**第 3 轮判定

**1**读取

提示词 18k 字符本轮事实 11k 字符较早轮次 33k 字符本轮新增 8.0k 字符

64k 输入 token · 17 张图像内联

抬起动作的回执（距目标 4.8 mm，已到达，移动 126 mm）与三张新的相机图像。

**2**思考

> “抬起成功；方块仍在手上。现在在蓝色方块上方水平平移。”

**3**行动

`move_pose(`

|  |  |
| --- | --- |
| targets | * left   + interaction "free\_space"   + orientation\_mode "hold\_current"   + position\_m [0.075, -0.14, 1.09]   + position\_mode "absolute" |

`)`

**4**结果

被规划器拒绝，没有任何移动：蓝色方块上方的目标距离 434 mm，直线路径只有 75% 可达，最近的可达姿态使夹爪偏离竖直向下 15°。

*下一轮*

**第 6 轮**

**图 11.** 在图 3 那次运行上每轮都跑的循环：模型读取输入、推理、发起调用，结果成为下一轮输入的一部分。可在时间线上任选 123 轮中的一轮。深色柱标记两个检查点，已完成的轮在此被折叠成一条记录；圆点标记较早图像刚被替换为引用的轮次。读取显示该轮之前发生了什么。其堆叠柱以共享的 400k 字符刻度度量文本字符数（不含图像内容）：提示词、本轮事实、较早轮次与新增证据。时间线与输入 token 总数使用提供方报告的 token。字符数与 token 数是不同单位。

## 结果[#](#results)

[表 2](#tab-summary) 重述主要对比。每次 **ORA** 运行都使用 DeepSeek-V4.1-Flash 零样本、每个用例一次尝试（一个任务配一个 seed），在 RPent[[1]](#ref-rpent) 的用例列表上运行；每个成功率统计全部计划用例。**ORA** 的模型可以调用成功判据，我们尚未确认 RPent 的智能体是否如此，因此这些比较的是完整系统而非模型。

| 成功率 % | RoboTwin | LIBERO-Pro | LIBERO |
| --- | --- | --- | --- |
| ORA + DeepSeek-V4.1-Flash开放权重模型，零样本，无 VLA | **69.2** | **81.4** | **83.5** |
| RPent + GPT-6 Astra语言模型 + VLA + 任务专用记忆 | — | 92.6 | — |
| RPent + Opus-4.7语言模型 + VLA + 任务专用记忆 | 58.4 | 82.4 | 96.0 |
| RPent + GPT-5.5语言模型 + VLA + 任务专用记忆 | 62.4 | 75.1 | — |
| 最佳端到端 VLALingBot-VLA · π\_RLinf · AtomVLA | 50.4 | 50.0 | 97.0 |

**表 2.** [图 2](#fig-main) 在三个基准上的对比。其它行来自 RPent 排行榜[[1]](#ref-rpent)；— 表示未报告。最佳 VLA 在每个基准上都是不同策略：LingBot-VLA[[6]](#ref-lingbot)、π\_RLinf[[4]](#ref-pirl) 与 AtomVLA[[7]](#ref-atomvla)。

### RoboTwin[#](#res-robotwin)

**ORA** 在 RoboTwin[[42]](#ref-robotwin) 上领先，其 250 个用例全部使用随机化场景，我们没有在干净场景上跑任何一次；而 RPent 的智能体先在干净场景上探索以收集任务记忆。它的失败是聚集的（[表 3](#tab-rtspread)）：50 个任务中有 31 个在五个 seed 里至少成功四个，而最多只成功一次的那八个任务贡献了 77 次失败中的 36 次。这些大多需要双臂协作或依次移动多个物体。

| 成功的 seed 数 | 任务数 | RoboTwin 任务 |
| --- | --- | --- |
| 5 / 5 | 16 | blocks ranking rgb、click alarmclock、click bell、grab roller、move playingcard away、move stapler pad、open microwave、place a2b left、place a2b right、place burger fries、place mouse pad、place object stand、press stapler、shake bottle、shake bottle horizontally、stack bowls two |
| 4 / 5 | 15 | adjust bottle、beat block hammer、blocks ranking size、handover mic、lift pot、move pillbottle pad、open laptop、place container plate、place empty cup、place object basket、place object scale、put object cabinet、rotate qrcode、stack blocks two、turn switch |
| 3 / 5 | 7 | pick dual bottles、place bread basket、place cans plasticbox、place fan、place shoe、stack blocks three、stamp seal |
| 2 / 5 | 4 | pick diverse bottles、place bread skillet、place phone stand、stack bowls three |
| 1 / 5 | 4 | dump bin bigbin、handover block、move can pot、place can basket |
| 0 / 5 | 4 | hanging mug、place dual shoes、put bottles dustbin、scan object |

**表 3.** 按 ORA 在五个 seed 中成功的数量分组的 RoboTwin 任务，共 250 个用例。

### LIBERO[#](#res-libero)

在标准 LIBERO[[44]](#ref-libero) 上，**ORA** 低于在 LIBERO 自身演示上训练的 VLA 策略。它在 Spatial 与 Object 上接近（95% 与 92%），但在 Goal（84%）与 Long（63%）上落后，后两者的任务大多串联两个子任务（[表 4](#tab-libero)）。

| LIBERO，成功率 % | Spatial | Object | Goal | Long | 总体 |
| --- | --- | --- | --- | --- | --- |
| ORA + DeepSeek-V4.1-Flash我们的 harness + 开放权重模型 · 无 VLA、机器人训练或任务记忆 | 95.0 | 92.0 | 84.0 | 63.0 | **83.5** |
| AtomVLA[[7]](#ref-atomvla)VLA，在机器人演示上训练 | 96.4 | 99.6 | 97.6 | 94.4 | **97.0** |
| RPent + Opus-4.7[[1]](#ref-rpent)RPent harness + 语言模型 + VLA + 任务专用记忆 | 97.0 | 100.0 | 94.0 | 93.0 | **96.0** |
| π\_RLinf[[4]](#ref-pirl)VLA，机器人演示 + 强化学习 | 99.0 | 96.0 | 97.0 | 89.0 | **95.3** |
| π0[[3]](#ref-openpi)VLA，在机器人演示上训练 | 96.8 | 98.8 | 95.8 | 85.2 | **94.2** |
| NORA[[52]](#ref-nora)VLA，在机器人演示上训练 | 85.6 | 89.4 | 80.0 | 63.0 | **79.5** |
| OpenVLA[[15]](#ref-openvla)VLA，在机器人演示上训练 | 84.7 | 88.4 | 79.2 | 53.7 | **76.5** |

**表 4.** 标准 LIBERO 上按套件的成功率（%）：4 个套件，每个 10 个任务，每个任务 10 个 seed。RPent 与 VLA 行取自 RPent 排行榜。版本、基础设施替换与协议差异见[附录](https://freemty.github.io/ora/appendix/)。

### LIBERO-Pro[#](#res-pro)

LIBERO-Pro[[45]](#ref-liberopro) 改变任务（Task 套件）或移动物体（Swap 套件）。**ORA** 相对 LIBERO 只掉了两分，Swap 用例与 Task 用例解决得差不多（400 个中分别为 331 与 320），而在 LIBERO 上训练的 VLA 策略急剧下降：π\_RLinf 从 95.3% 降到 50.0%，AtomVLA 从 97.0% 降到 6.3%（[表 5](#tab-pro)）。在写机器人代码的智能体报告过的六个套件上，**ORA** 平均 89.2%，而 ASPIRE[[32]](#ref-aspire) 为 71.7%、RATs[[33]](#ref-rats) 为 43.8%、CaP-Agent0[[31]](#ref-capx) 为 18.2%，协议各不相同。OpenRUA[[36]](#ref-openrua) 报告用 Claude Opus 5 达到 87.0%；我们尚未比较其协议与我们的。

| LIBERO-Pro，成功率 % | Spatial | | Object | | Goal | | Long | | 总体 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Task | Swap | Task | Swap | Task | Swap | Task | Swap |
| ORA + DeepSeek-V4.1-Flash我们的 harness + 开放权重模型 · 无 VLA、机器人训练或任务记忆 | 98 | 91 | 93 | 98 | 77 | 78 | 52 | 64 | **81.4** |
| RPent + GPT-6 Astra [a]RPent harness + 语言模型 + VLA + 任务专用记忆 | 100 | 98 | 100 | 99 | 88 | 99 | 85 | 72 | **92.6** |
| RPent + Opus-4.7[[1]](#ref-rpent)RPent harness + 语言模型 + VLA + 任务专用记忆 | — | — | — | — | — | — | — | — | **82.4** |
| RPent + GPT-5.5RPent harness + 语言模型 + VLA + 任务专用记忆 | 81 | 69 | 94 | 91 | 75 | 66 | 70 | 55 | **75.1** |
| RPent Flash Mode [b][[8]](#ref-molmo2)RPent harness + Molmo2-8B + VLA + 已发布的任务专用记忆 | 79 | 70 | 86 | 93 | 74 | 65 | 60 | 54 | **72.6** |
| RPent + Qwen3.6 27B[[2]](#ref-qwen36)RPent harness + 开放权重模型 + VLA + 任务专用记忆 | 82 | 78 | 83 | 84 | 68 | 68 | 61 | 41 | **70.6** |
| ASPIRE [c][[32]](#ref-aspire)LLM 写代码 + 技能库 | 60 | 51 | 95 | 98 | 45 | 81 | 38 | 23 | — |
| RATs[[33]](#ref-rats)LLM 写代码 + 技能库 | 31 | 29 | 63 | 61 | 36 | 43 | — | — | — |
| CaP-Agent0[[31]](#ref-capx)LLM 写代码 | 14 | 12 | 18 | 22 | 17 | 26 | — | — | — |
| π\_RLinf[[4]](#ref-pirl)VLA，机器人演示 + 强化学习 | 42 | 59 | 71 | 78 | 45 | 42 | 49 | 14 | **50.0** |
| π0.5[[3]](#ref-openpi)VLA，在机器人演示上训练 | 1 | 20 | 1 | 17 | 2 | 38 | 1 | 8 | **11.0** |

**表 5.** 八个 LIBERO-Pro 套件上的成功率（%），每个 10 个任务、10 个 seed。Swap 是排行榜对位置扰动的叫法。RPent 与 VLA 行来自 RPent 排行榜；— 表示未报告。[a] GPT-6 Astra 使用各自冻结的记忆快照。[b] Flash Mode 用 Molmo2-8B 与已发布记忆运行，报告十个 seed 中的最佳。[c] ASPIRE 在 seed 51–65 上学习技能，并用 Claude Opus 4.6 在留出 seed 上测试，其 Long 结果迁移了一个 LIBERO-90 技能库，因此我们不给它的总体成功率。CaP-Agent0 按每种条件 50 次试验报告。精确计数见[附录](https://freemty.github.io/ora/appendix/)。

### RoboDojo：初次扫描[#](#res-robodojo)

RoboDojo[[10]](#ref-robodojo) 是最难的：在双臂 ARX X5 上的 42 个多阶段任务。用较早版本 **ORA** 做的首次运行，每个任务三轮，解决了 126 轮中的 18 轮、42 个任务中的 9 个至少一次。108 个失败轮中大多数败在运动：目标合理，但运动没有达成它（[表 6](#tab-rdj)）。这不是一次评测，我们也不知道该任务集有已发表的结果。

| 失败轮的主要原因 | 轮数 |
| --- | --- |
| 运动未达成合理目标 | 64 |
| 策略、顺序或工具使用 | 29 |
| 感知或定位 | 7 |
| 模拟器异常 | 3 |
| 在仍可恢复时放弃 | 3 |
| 无法判定 | 2 |

**表 6.** 42 任务 RoboDojo 扫描中 108 个失败轮各自的主要原因，每轮一位审核人判断；64 个运动案例中有 27 个置信度较低。

### 真机上的初步结果[#](#real)

以上全部在仿真中运行。我们还将 **ORA** 接到桌上的一个低成本机械臂上，配一台固定 RGB-D 相机和一台腕部相机，并给 DeepSeek-V4.1-Flash 两个家务任务：把一个小抽屉的把手拉开（[图 12](#fig-realdrawer)），以及把一根糖果棒放进一个小开口盒（[图 13](#fig-realbar)）。循环与仿真中相同：模型读取相机视图与深度，规划每个动作并读取返回内容。每次动作执行前都有操作员审阅。这两次运行中两个任务都完成了。我们尚未测量成功率。

[![](img/i-03e98ec0d5ee.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/ora--img--videos--ora-real-drawer.mp4)

**图 12.** **拉开抽屉**（真机）。模型以 50° 接近把手，双钳口合上，然后两次各拉 4.5 cm，抽屉出来 9 cm。左：外部相机；中：模型收到的深度图；右：腕部相机。时间已加速，模型规划期间的停顿以静帧呈现。

[![](img/i-c4e443aa6334.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/ora--img--videos--ora-real-bar.mp4)

**图 13.** **把糖果棒放进盒子**（真机）。腕部修正 9 mm 后，夹爪合上夹住糖果棒，抬升 13 cm，滑到开口上方并松开，机械臂回到折叠位。左：外部相机；右：腕部相机。时间已加速，模型规划期间的停顿以静帧呈现。

### 成本[#](#cost)

我们按 DeepSeek 为 DeepSeek-V4.1-Flash 公布的 API 非高峰价格[[53]](#ref-dsprice)为每次模型调用计价：每百万缓存输入 token $0.003，每百万未缓存输入 token $0.15，每百万输出 token $0.60。非高峰价格是高峰的一半，因此在高峰价格下下面每个数字都翻倍。模型由我们自己服务，所以这些是按 API 价格折算的成本，而非我们实际支付的费用。每次尝试都计入，含失败；模拟器与 GPU 成本未计入。

| 基准 | 尝试 | 解决 | 模型调用中位数 | 输入 token 中位数 | 缓存命中（估计） | 每次尝试均值 / 中位数 | 合计 | 每个已解决用例 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RoboTwin | 250 | 173 | 28 | 3.7M | 86% | $0.24 / $0.12 | $60.2 | **$0.35** |
| LIBERO-Pro | 800 | 651 | 27 | 3.1M | 84% | $0.28 / $0.10 | $227.4 | **$0.35** |
| LIBERO | 405 | 334 | 26 | 2.9M | 84% | $0.25 / $0.09 | $100.2 | **$0.30** |
| RoboDojo | 126 | 18 | 55.5 | 11.0M | 86% | $0.39 / $0.35 | $49.2 | $2.74 |

**表 7.** 上述评测运行按 API 折算的模型成本，按 DeepSeek-V4.1-Flash 在 DeepSeek 非高峰美元价计算。LIBERO 统计 400 个计分用例，另有 5 次因基础设施故障结束并重跑的尝试。RoboDojo 行统计结果一节中首次 RoboDojo 运行的 126 轮（42 个任务、每个三轮，较早版本的 harness），它不是一次评测。

大部分成本是未缓存输入：在 LIBERO-Pro 上，$227 中有 $157 是它，输出为 $54，缓存输入为 $17。成本也高度偏斜。中位尝试的成本远低于均值的一半，因为长时间失败的尝试会不断追加输入；一次已解决的尝试平均花费 $0.11 至 $0.14，而[图 1](#fig-hero) 中 40 个已解决的轮各花 $0.13。一次尝试产生约 100k 输出 token。

我们的服务器不报告 prompt cache 命中，因此我们从 token 数重建：一次调用的输入若包含上一个请求与响应的全部内容，它就是在扩展，该前缀计为命中；其它调用打断前缀，只计其开头固定的提示词。86–89% 的调用扩展了前一个，由此得到表中 84–86% 的估计命中率。其余调用跟在一次上下文压缩之后或开启新一轮，它们产生了全部未缓存 token 的 83–89%。既然未缓存输入是最大成本，降低成本的主要办法就是更少地打断前缀。

## 分析：harness 贡献了什么[#](#analysis)

前面我们论证过，机器人对 harness 的要求比编程智能体更高。每一部分都来自对失败运行的审计；这里我们比较各运行版本并考察个别案例。大多数比较没有隔离单一组件。每段视频的所有画面都以相同的仿真时间速度播放，每条结论都说明其证据与局限。

### 从经验中学习[#](#an-learn)

上下文管理把已完成的轮保留在输入里，先逐字、之后作为检查点。**ORA** 不跨任务保留记忆，上面的基准运行每个用例只用一轮，但在一次会话内，模型可以利用它早先的轮次。在[图 14](#fig-rounds) 中，每次第 2 轮开场都先说明第 1 轮哪里错了，然后避开它；在上排——即[图 3](#fig-tui) 那次运行——第 1 轮在放下蓝色方块后手臂侧移，把方块弄丢了，第 2 轮一开场就陈述“先竖直抬起”的规则。

[![](img/i-7975d47a86e2.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/ora--img--videos--ora-rounds.mp4)

**图 14.** 两次会话，每排一次：失败的第 1 轮（左）、模型在第 2 轮开头陈述的教训（黄色），以及同一场景上成功的第 2 轮（右）。上：RoboDojo 叠方块；第 1 轮在回撤时把蓝色方块拖下了桌。下：RoboTwin 开笔记本；第 1 轮从上方把半开的盖子推合上了。两次会话都是在看到结果之后挑选的，其中 RoboTwin 那次不在报告的评测范围内。

**结论：在上述例子中，模型利用保留的上下文修正了做法。在 148 次两轮开发会话中，第 2 轮成功 72 次，第 1 轮成功 63 次。这一比较没有把保留上下文的效果与“多一次尝试”的收益分离开。**

### 精确的任务指令与成功判据很重要[#](#cs-task)

提示词包分两部分陈述任务：基准的指令（不变）和一份用平实语言重述官方成功测试的完成契约。在一次早期运行中，释义改写了某个 LIBERO-Spatial 任务，把“最上层抽屉”写成“木柜的顶层”，模型就拿走了立在柜子上的碗，而不是抽屉里的碗（[图 15](#fig-pairtask)）。指令也可能漏掉测试的一部分：RoboTwin 的“把瓶子头朝上立住”还要求把瓶子朝其底部所指的一侧搬运，而“把扑克牌移开近边”要求牌最终落在很靠左或靠右的位置。没有契约时，模型满足了字面要求却未通过检查（[图 16](#fig-paircontract)）。

[![](img/i-0fb64b759773.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/ora--img--videos--ora-cs-task.mp4)

**图 15.** LIBERO-Spatial，两个 seed。左：释义后的指令，以及拿错的碗。右：基准原话，以及从抽屉取出并放到盘子上的碗。

[![](img/i-5c3be6d61385.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/ora--img--videos--ora-cs-contract.mp4)

**图 16.** RoboTwin，每排同一 seed，无契约（左）与有契约（右）。上：瓶子只是立住、从未被搬运；有契约时它被朝底部所指的一侧搬运。下：牌盒在一个个位置之间被挪动、经历十次失败的检查；有契约时它被搬到左边缘并放下。

**结论：使用基准原话的运行版本在 10 个 seed 中成功 10 个，使用释义的版本为 10 个中成功 2 个。在 206 个配对的 RoboTwin 用例上，带完成契约的版本成功率为 64.1%，不带为 53.4%。其它 harness 组件也同时变了，所以这两个比较都没有隔离措辞或契约本身的效果。**

### 感知工具有助于发现和定位物体[#](#cs-perception)

look 类工具把模型的命名与指向变成带实测位置和尺寸的 mask（[图 10](#fig-tools)）。早期运行说明了模型为什么需要它们。它自己点的位置不够准：在一次 LIBERO 运行中，在倾斜相机上选的点落在了支撑面上而不是物体上，而把点移动 7 到 14 像素就让 mask 里的罐子与桌面连成一片；返回 mask 的尺寸让这个错误变得可见。它在相似物体间的选择也不可靠：当文本 grounding 把错误的罐子排在第一位时，把每个候选放大成特写让模型选出了正确的那一个。后来的运行重复了第二种模式（[图 17](#fig-csperception)）。

[![](img/i-6f48175ec12d.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/ora--img--videos--ora-cs-perception.mp4)

**图 17.** 两次已解决的运行，其中文本 grounding 给相似物体的打分很接近，而在 LIBERO-Pro 上把错误的瓶子排在第一位：工具返回的内容（左）与模型据此所做的（右）。

**结论：依据早期单次运行、且尚无配对消融，这些工具让指向与身份错误变得可见，而选对物体仍是最难的一步。**

### 精确的常量与测量[#](#cs-measure)

工具套件把测量值交给模型，而不是让它自己估计，而且这个测量必须是动作所需要的那一个。对放置而言，工具最初返回目标 mask 的中心按其 LIBERO 倾斜相机的视角所见，落在桌面上物体中心之外 2–3 cm，差不多等于整个放置容差。现在它们返回俯视所见到的中心（[图 18](#fig-csmeasure)）。更一般地说，把精确坐标与环境的常量交给模型——在工具结果与系统提示词里——对其推理影响很大。Astranomy 在 GPT-6 Astra 上也发现同样的事：作为直接机器人策略，当提示词中加入相机与夹爪几何后，其成功率从 19.3% 升到 72.7%[[54]](#ref-astranomy)。

[![](img/i-4a5bff6b6417.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/ora--img--videos--ora-cs-measure.mp4)

**图 18.** 两个较长的 LIBERO 任务，每排初始状态相同：用相机视角的中心时放置失准（左）；用俯视中心时放到位（右）。

**结论：返回俯视中心使两个受影响任务族在 59 个测试状态上的成功数从 29 升到 42。**

### 解释被拒绝的动作有助于恢复[#](#cs-feedback)

运动工具在每次动作后回报，而拒绝会说明原因。早期，当规划器找不到逆运动学解、拒绝又不给理由时，RoboDojo 的运行就把目标当作不可达而放弃，尽管这类目标大多在夹爪倾斜后可达；一条光秃秃的错误信息曾让一次 GPT-6 Astra 运行在五分钟内重复同一调用 14 次。现在拒绝会报告机械臂沿直线路径能到达多远，以及最近的可达姿态。在[图 3](#fig-tui) 那次运行中，第 6 轮就是这样被拒绝的：75% 的路径可达，最近可达姿态是倾斜 15°；模型把搭建点移到两臂都能到达的位置，在左臂又一次移动被拒之后，用右臂抓住了蓝色方块（[图 11](#fig-loop)）。[图 19](#fig-csfeedback) 展示了另外两次运行：在 RoboTwin 中，报告的可达范围让模型把方块放下并用另一条臂接力；在 LIBERO-Pro 中，模型采用了拒绝信息给出的可达姿态。

[![](img/i-0c107fb5c767.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/ora--img--videos--ora-cs-feedback.mp4)

**图 19.** 两次含被拒绝动作的已解决运行：拒绝信息与模型的解读（左），以及它接下来做了什么（右）。

**结论：对 77 次被拒绝的动作做离线重放，指出最近可达姿态的拒绝信息能解决其中 69 次。**

[图集](https://freemty.github.io/ora/gallery/)展示了 153 个已解决的回合，每个任务一个，都经人工目检。

## 局限[#](#limitations)

**ORA** 表明开放权重模型可以零样本操作机器人，但它有明确的局限。第一，它很慢：一个回合的中位耗时是 14 到 25 分钟，大部分时间在等模型，而模拟器在模型思考时暂停，因此这些结果不能说明实时控制能力。长时程任务仍然困难：Long 套件成功率 52–64%，首次 RoboDojo 扫描在 126 轮中解决 18 轮。第二，工具套件是手写的，**ORA** 还不能自动迭代或修改自己的工具。我们几乎所有结果都来自仿真和一个模型 DeepSeek-V4.1-Flash；在真机上我们只有两个演示，且每次动作都由操作员批准。我们的成功率使用各基准的官方检查，它在条件一满足时就结束回合，而有些条件比指令更宽松：RoboTwin 的摇晃任务只检查瓶子被抬起。当我们对每个任务观看一个已解决的 RoboTwin 回合时，46 个中有 7 个没有做指令要求的事，因此报告的成功率高估了真实任务完成度。这个按任务挑选的样本无法建立修正后的总体成功率。我们的大部分发现来自阅读失败运行，而非受控消融。接下来，我们会把 **ORA** 跑在更多真机上，并把已验证的回合变成训练数据，用于一个能在机器人上运行的小模型。

## 致谢[#](#ack)

感谢 RPent 团队发布其评测用例、排行榜与代码，本文的比较依赖它们[[1]](#ref-rpent)；感谢 CaP-X[[31]](#ref-capx) 与 ASPIRE[[32]](#ref-aspire) 的作者，他们的工作启发了我们的工具；感谢 DeepSeek 以开放权重发布 DeepSeek-V4.1-Flash[[9]](#ref-deepseek)。感谢 [Zhaoning Wang](https://www.zhaoningwang.com/) 在真机上部署 **ORA**，感谢 [Junda Chen](https://github.com/GindaChen/)、[Runyu Lu](https://runyulu.com/) 与 [Nan Xue](https://xuenan.net/) 的有益讨论。

## 引用[#](#citation-sec)

复制

```
@misc{ora2026,
  title        = {{ORA}: Open Robot-Use Agents},
  author       = {Yang, Yuanbo and Chen, Siyi and Gao, Jun and Zhang, Hao},
  year         = {2026},
  month        = oct,
  howpublished = {Hao AI Lab blog},
  url          = {https://haoailab.com/blogs/ora/}
}
```

## 参考文献[#](#references)

1. Yixian Zhang et al. Harness VLA: Steering Frozen VLAs into Reliable Manipulation Primitives via Memory-Guided Agents. arXiv:2607.08448, 2026. Code and leaderboard: RPent (RLinf). [arxiv.org/abs/2607.08448](https://arxiv.org/abs/2607.08448) [↩](#cite-rpent)
2. Qwen Team. Qwen3.6-27B. Model card, 2026. [huggingface.co/Qwen/Qwen3.6-27B](https://huggingface.co/Qwen/Qwen3.6-27B) [↩](#cite-qwen36)
3. Physical Intelligence. openpi. Software, 2025. [github.com/Physical-Intelligence/openpi](https://github.com/Physical-Intelligence/openpi) [↩](#cite-openpi)
4. Kang Chen et al. πRL: Online RL Fine-tuning for Flow-based Vision-Language-Action Models. arXiv:2510.25889, 2025. [arxiv.org/abs/2510.25889](https://arxiv.org/abs/2510.25889) [↩](#cite-pirl)
5. NVIDIA. GR00T N1: An Open Foundation Model for Generalist Humanoid Robots. arXiv:2503.14734, 2025. [arxiv.org/abs/2503.14734](https://arxiv.org/abs/2503.14734) [↩](#cite-gr00t)
6. Wei Wu et al. A Pragmatic VLA Foundation Model. arXiv:2601.18692, 2026. [arxiv.org/abs/2601.18692](https://arxiv.org/abs/2601.18692) [↩](#cite-lingbot)
7. Xiaoquan Sun et al. AtomVLA: Scalable Post-Training for Robotic Manipulation via Predictive Latent World Models. arXiv:2603.08519, 2026. [arxiv.org/abs/2603.08519](https://arxiv.org/abs/2603.08519) [↩](#cite-atomvla)
8. Christopher Clark et al. Molmo2: Open Weights and Data for Vision-Language Models with Video Understanding and Grounding. arXiv:2601.10611, 2026. [arxiv.org/abs/2601.10611](https://arxiv.org/abs/2601.10611) [↩](#cite-molmo2)
9. DeepSeek-AI. DeepSeek-V4.1-Flash. Model card, 2026. [huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash) [↩](#cite-deepseek)
10. Tianxing Chen et al. RoboDojo: A Unified Sim-and-Real Benchmark for Comprehensive Evaluation of Generalist Robot Manipulation Policies. arXiv:2607.04434, 2026. [arxiv.org/abs/2607.04434](https://arxiv.org/abs/2607.04434) [↩](#cite-robodojo)
11. John Yang et al. SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering. NeurIPS, 2024. [arxiv.org/abs/2405.15793](https://arxiv.org/abs/2405.15793) [↩](#cite-sweagent)
12. OpenAI. Computer-Using Agent. Blog post, 2025. [openai.com/index/computer-using-agent/](https://openai.com/index/computer-using-agent/) [↩](#cite-cua)
13. Xinyuan Wang et al. OpenCUA: Open Foundations for Computer-Use Agents. NeurIPS, 2025. [arxiv.org/abs/2508.09123](https://arxiv.org/abs/2508.09123) [↩](#cite-opencua)
14. Brianna Zitkovich et al. RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control. CoRL, 2023. [arxiv.org/abs/2307.15818](https://arxiv.org/abs/2307.15818) [↩](#cite-rt2)
15. Moo Jin Kim et al. OpenVLA: An Open-Source Vision-Language-Action Model. CoRL, 2024. [arxiv.org/abs/2406.09246](https://arxiv.org/abs/2406.09246) [↩](#cite-openvla)
16. Seonghyeon Ye et al. World Action Models are Zero-shot Policies. ICLR 2026 Workshop on World Models, 2026. [arxiv.org/abs/2602.15922](https://arxiv.org/abs/2602.15922) [↩](#cite-dreamzero)
17. Tony Z. Zhao et al. Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware. RSS, 2023. [arxiv.org/abs/2304.13705](https://arxiv.org/abs/2304.13705) [↩](#cite-aloha)
18. Cheng Chi et al. Universal Manipulation Interface: In-The-Wild Robot Teaching Without In-The-Wild Robots. RSS, 2024. [arxiv.org/abs/2402.10329](https://arxiv.org/abs/2402.10329) [↩](#cite-umi)
19. Simar Kareer et al. EgoMimic: Scaling Imitation Learning via Egocentric Video. ICRA, 2025. [arxiv.org/abs/2410.24221](https://arxiv.org/abs/2410.24221) [↩](#cite-egomimic)
20. Jianyuan Wang. Slide at the Eighth Workshop on Image Matching: Local Features and Beyond (CVPR 2026), photo shared on X. Social post, 2026. [x.com/ducha\_aiki/status/2062653228802515047](https://x.com/ducha_aiki/status/2062653228802515047) [↩](#cite-jwang)
21. Jay Chooi. GPT-6 Astra on a robot control task. Thread on X, 2026. [x.com/chooi\_jeq/status/2096064315115839904](https://x.com/chooi_jeq/status/2096064315115839904) [↩](#cite-chooi)
22. Phillip Isola. Robot-Use Agents. Essay, 2026. [web.mit.edu/phillipi/www/writing/robot-use-agents.html](https://web.mit.edu/phillipi/www/writing/robot-use-agents.html) [↩](#cite-isola)
23. Shmuel Berman et al. Claude plays robotics. Anthropic blog post, 2026. [www.anthropic.com/research/claude-plays-robotics](https://www.anthropic.com/research/claude-plays-robotics) [↩](#cite-cpr)
24. Achu Menon et al. GPT-6 Astra on robotic manipulation. Robocurve blog post, 2026. [openai.robocurve.org/gpt-6-astra/](https://openai.robocurve.org/gpt-6-astra/) [↩](#cite-robocurve)
25. Hanming Ye and Yiding Song. Introducing Waddle: agents that control robots. Waddle Labs blog post, 2026. [www.waddlelabs.ai/research/introducing-waddle](https://www.waddlelabs.ai/research/introducing-waddle) [↩](#cite-waddle)
26. Angen Ye et al. GigaWorld-Policy: An Efficient Action-Centered World–Action Model. arXiv:2603.17240, 2026. [arxiv.org/abs/2603.17240](https://arxiv.org/abs/2603.17240) [↩](#cite-gigaworld)
27. Michael Ahn et al. Do As I Can, Not As I Say: Grounding Language in Robotic Affordances. CoRL, 2022. [arxiv.org/abs/2204.01691](https://arxiv.org/abs/2204.01691) [↩](#cite-saycan)
28. Lucy Xiaoyang Shi et al. Hi Robot: Open-Ended Instruction Following with Hierarchical Vision-Language-Action Models. ICML, 2025. [arxiv.org/abs/2502.19417](https://arxiv.org/abs/2502.19417) [↩](#cite-hirobot)
29. Figure. Helix: A Vision-Language-Action Model for Generalist Humanoid Control. Blog post, 2025. [www.figure.ai/news/helix](https://www.figure.ai/news/helix) [↩](#cite-helix)
30. Jacky Liang et al. Code as Policies: Language Model Programs for Embodied Control. ICRA, 2023. [arxiv.org/abs/2209.07753](https://arxiv.org/abs/2209.07753) [↩](#cite-cap)
31. Letian Fu et al. CaP-X: A Framework for Benchmarking and Improving Coding Agents for Robot Manipulation. ICML, 2026. [arxiv.org/abs/2603.22435](https://arxiv.org/abs/2603.22435) [↩](#cite-capx)
32. Runyu Lu et al. ASPIRE: Agentic Skills Discovery for Robotics. arXiv:2607.00272, 2026. [arxiv.org/abs/2607.00272](https://arxiv.org/abs/2607.00272) [↩](#cite-aspire)
33. Junyi Zhang et al. Playful Agentic Robot Learning. arXiv:2606.19419, 2026. [arxiv.org/abs/2606.19419](https://arxiv.org/abs/2606.19419) [↩](#cite-rats)
34. Shunyu Yao et al. ReAct: Synergizing Reasoning and Acting in Language Models. ICLR, 2023. [arxiv.org/abs/2210.03629](https://arxiv.org/abs/2210.03629) [↩](#cite-react)
35. Haowen Liu et al. Guava: Distilling Frontier VLMs into a Compact Agent through a Robotic Manipulation Harness. arXiv:2606.18363, 2026. [arxiv.org/abs/2606.18363](https://arxiv.org/abs/2606.18363) [↩](#cite-guava)
36. Zhaoyang Chu et al. OpenRUA: Robot-Use Agents Are Zero-Shot Visuomotor Policies. arXiv:2610.02459, 2026. [arxiv.org/abs/2610.02459](https://arxiv.org/abs/2610.02459) [↩](#cite-openrua)
37. Mengzhao Jia et al. Agent as Policy for Robotic Manipulation. arXiv:2609.12541, 2026. [arxiv.org/abs/2609.12541](https://arxiv.org/abs/2609.12541) [↩](#cite-agp)
38. Zexi Li et al. Robo-Harness K1: Harnessing Robot-Use Agents via Perception Augmentation. arXiv:2609.29389, 2026. [arxiv.org/abs/2609.29389](https://arxiv.org/abs/2609.29389) [↩](#cite-k1)
39. Anthropic. Claude Code. Software, 2025. [github.com/anthropics/claude-code](https://github.com/anthropics/claude-code) [↩](#cite-claudecode)
40. Mario Zechner. Pi: a minimal, extensible agent harness (pi-mono). Software, 2025. [github.com/earendil-works/pi](https://github.com/earendil-works/pi) [↩](#cite-pi)
41. NVIDIA. Isaac Sim. Software, 2026. [developer.nvidia.com/isaac/sim](https://developer.nvidia.com/isaac/sim) [↩](#cite-isaacsim)
42. Tianxing Chen et al. RoboTwin 2.0: A Scalable Data Generator and Benchmark with Strong Domain Randomization for Robust Bimanual Robotic Manipulation. ICML, 2026. [arxiv.org/abs/2506.18088](https://arxiv.org/abs/2506.18088) [↩](#cite-robotwin)
43. Fanbo Xiang et al. SAPIEN: A SimulAted Part-based Interactive ENvironment. CVPR, 2020. [arxiv.org/abs/2003.08515](https://arxiv.org/abs/2003.08515) [↩](#cite-sapien)
44. Bo Liu et al. LIBERO: Benchmarking Knowledge Transfer for Lifelong Robot Learning. NeurIPS Datasets and Benchmarks Track, 2023. [arxiv.org/abs/2306.03310](https://arxiv.org/abs/2306.03310) [↩](#cite-libero)
45. Xueyang Zhou et al. LIBERO-PRO: Towards Robust and Fair Evaluation of Vision-Language-Action Models Beyond Memorization. arXiv:2510.03827, 2025. [arxiv.org/abs/2510.03827](https://arxiv.org/abs/2510.03827) [↩](#cite-liberopro)
46. Emanuel Todorov, Tom Erez and Yuval Tassa. MuJoCo: A physics engine for model-based control. IROS, 2012. [ieeexplore.ieee.org/document/6386109](https://ieeexplore.ieee.org/document/6386109) [↩](#cite-mujoco)
47. Yuke Zhu et al. robosuite: A Modular Simulation Framework and Benchmark for Robot Learning. arXiv:2009.12293, 2020. [arxiv.org/abs/2009.12293](https://arxiv.org/abs/2009.12293) [↩](#cite-robosuite)
48. Ruijie Lu et al. Thinking with Visual Primitives. DeepSeek-AI technical report, 2026. [github.com/deepseek-ai/Thinking-with-Visual-Primitives](https://github.com/deepseek-ai/Thinking-with-Visual-Primitives) [↩](#cite-dsvp)
49. Nicolas Carion et al. SAM 3: Segment Anything with Concepts. ICLR, 2026. [arxiv.org/abs/2511.16719](https://arxiv.org/abs/2511.16719) [↩](#cite-sam3)
50. Balakumar Sundaralingam et al. cuRobo: Parallelized Collision-Free Minimum-Jerk Robot Motion Generation. arXiv:2310.17274, 2023. [arxiv.org/abs/2310.17274](https://arxiv.org/abs/2310.17274) [↩](#cite-curobo)
51. Martin Sundermeyer et al. Contact-GraspNet: Efficient 6-DoF Grasp Generation in Cluttered Scenes. ICRA, 2021. [arxiv.org/abs/2103.14127](https://arxiv.org/abs/2103.14127) [↩](#cite-cgn)
52. Chia-Yu Hung et al. NORA: A Small Open-Sourced Generalist Vision Language Action Model for Embodied Tasks. arXiv:2504.19854, 2025. [arxiv.org/abs/2504.19854](https://arxiv.org/abs/2504.19854) [↩](#cite-nora)
53. DeepSeek. Models & Pricing. Documentation. [api-docs.deepseek.com/quick\_start/pricing](https://api-docs.deepseek.com/quick_start/pricing) [↩](#cite-dsprice)
54. Jenai Xuning Yang, Ashna Khetan and Shun Zhang. Astranomy: An empirical study of GPT-6 Astra as a native robot policy. NVIDIA Seattle Robotics Lab, 2026. [research.nvidia.com/labs/srl/projects/astranomy/](https://research.nvidia.com/labs/srl/projects/astranomy/) [↩](#cite-astranomy)

