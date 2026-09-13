---
title: "Gemini Robotics 2 为机器人带来全身智能"
title_en: "Gemini Robotics 2 brings whole body intelligence to robots"
source: https://deepmind.google/blog/gemini-robotics-2-brings-whole-body-intelligence-to-robots/
site: deepmind
date: 2026-07-30
crawled: 2026-09-13
translated: 2026-09-13
---

# Gemini Robotics 2 为机器人带来全身智能

> 原文：[Gemini Robotics 2 brings whole body intelligence to robots](https://deepmind.google/blog/gemini-robotics-2-brings-whole-body-intelligence-to-robots/) · Google DeepMind

从脚到指尖——我们正在教机器人实现智能化的全身控制、精细灵巧操作与团队协作，以完成各种复杂任务

几十年来，我们一直梦想着机器人能够无缝走进我们的世界、助我们一臂之力。如今，这一愿景迈出了重要一步。

大多数机器人都是预先编程或由人遥控来完成狭窄、重复的任务序列。它们缺乏真正自主学习的能力，也无法适应不可预测的环境。此外，把学到的技能从一台机器人身上迁移到另一台仍然极其困难。要在大规模上解决最难的问题，各种形态与尺寸的机器人都需要 AI 模型赋予它们智能地思考、行动和交互的能力，以安全地完成任务。

我们曾通过 [Gemini Robotics](https://deepmind.google/models/gemini-robotics/) 展示了 Gemini 的多模态理解能力如何驱动真实世界的行动。今天，我们推出 Gemini Robotics 2——驱动下一代真正自适应机器人的智能层。随着它迈出字面意义上的第一步，这一重大进展解锁了智能全身控制、高级灵巧操作和多机器人协作。

Gemini Robotics 2 让机器人能够对每一个动作进行推理，解锁了广泛的任务。例如，它可以让一台人形机器人行走、下蹲、伸展并操作物体来收拾凌乱的房间。它甚至可以与其他机器人组队，更快地完成任务。而这种深度的智能还可以在设备本地运行，同时只需几小时就能无缝适配全新的机器人本体。

我们通过三个能力强大的模型来实现这一切：

- [Gemini Robotics 2](https://deepmind.google/models/gemini-robotics/vla/)：我们最先进的视觉-语言-动作模型（VLA），可将视觉和语言输入转化为运动控制，使机器人得以采取行动。该模型能够控制完整的人形机器人——从脚到指尖——以及其他双臂机器人。它还为双手和夹爪带来了新水平的灵巧操作能力。
- [Gemini Robotics ER 2](https://deepmind.google/models/gemini-robotics/embodied-reasoning/)：我们能力最强的具身推理（ER）模型。它是一个视觉语言模型（VLM），充当我们的智能体，使机器人能够与人类沟通、理解物理世界，并规划持续数分钟的多步骤任务。我们还在其中引入了让机器人作为一个团队协同工作的能力。
- [Gemini Robotics On-Device 2](https://deepmind.google/models/gemini-robotics/on-device/)：我们最高效的视觉-语言-动作模型（VLA），经过优化可在机器人设备本地运行。该模型现在只需几小时的数据即可快速适配全新的机器人本体。

第 1 页，共 3 页

![一张标题为“General whole body manipulation（全身通用操作）”、副标题为“Apollo with Inspire hands（搭载 Inspire 手的 Apollo）”的柱状图，在三项任务上显示了带误差线的准确率百分比：“从桌面拾取”为 68.4%、“从地面拾取”为 45.7%、“从货架拾取”为 76.3%。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/MVCfTE-4h3AwDVPZ/gemini-robotics-2__general-whole-body-manipulation__light.svg)![一张标题为“General whole body manipulation（全身通用操作）”、副标题为“Apollo with Inspire hands（搭载 Inspire 手的 Apollo）”的柱状图，在三项任务上显示了带误差线的准确率百分比：“从桌面拾取”为 68.4%、“从地面拾取”为 45.7%、“从货架拾取”为 76.3%。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/MVCfTE-4h3AwDVPZ/gemini-robotics-2__general-whole-body-manipulation__dark.svg)

Gemini Robotics 2 使用同一个模型检查点控制三种不同的本体——搭载 SharpaWave 手的 Apptronik Apollo 2 机器人、搭载 Inspire 手的 Apollo 2 机器人，以及搭载 Robotiq 夹爪的 Franka Duo——涵盖各种全身任务和灵巧操作任务。每根柱线代表同一技能类别内多个任务的平均成功率。对于多指任务，我们展示单个任务的表现。虽然 Gemini Robotics 2 在全身任务和基于夹爪的灵巧任务上达到了中等到较高的成功率，但多指灵巧操作仍然具有挑战性。

![一张标题为“Multi-finger dexterity（多指灵巧性）”、副标题为“Apollo with Sharpa hands（搭载 Sharpa 手的 Apollo）”的柱状图，在五项任务上显示了带误差线的准确率百分比：“拧灯泡”为 36%、“拧下灯泡”为 92%、“系垃圾袋”为 44%、“簸箕”为 32%、“密封袋”为 40%。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/MVCfTE-4h3AwDVPZ/gemini-robotics-2__multi-finger-dexterity__light.svg)![一张标题为“Multi-finger dexterity（多指灵巧性）”、副标题为“Apollo with Sharpa hands（搭载 Sharpa 手的 Apollo）”的柱状图，在五项任务上显示了带误差线的准确率百分比：“拧灯泡”为 36%、“拧下灯泡”为 92%、“系垃圾袋”为 44%、“簸箕”为 32%、“密封袋”为 40%。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/MVCfTE-4h3AwDVPZ/gemini-robotics-2__multi-finger-dexterity__dark.svg)

![一张标题为“Gripper dexterity（夹爪灵巧性）”、副标题为“Franka Duo”的柱状图，在三项任务上显示了带误差线的准确率百分比：“通用拾取与放置”为 74.2%、“多样化工具套件整理”为 78.9%、“精准插入任务”为 89.6%。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/MVCfTE-4h3AwDVPZ/gemini-robotics-2__gripper-dexterity__light.svg)![一张标题为“Gripper dexterity（夹爪灵巧性）”、副标题为“Franka Duo”的柱状图，在三项任务上显示了带误差线的准确率百分比：“通用拾取与放置”为 74.2%、“多样化工具套件整理”为 78.9%、“精准插入任务”为 89.6%。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/MVCfTE-4h3AwDVPZ/gemini-robotics-2__gripper-dexterity__dark.svg)

Gemini Robotics ER 2，我们的推理模型，现已在 [Google AI Studio](https://ai.dev/prompts/new_chat?model=gemini-robotics-er-2-preview) 上可用，并在 [Gemini Enterprise Agent Platform](https://console.cloud.google.com/agent-platform/publishers/google/model-garden/gemini-robotics-er-2-preview-info) 上提供私密预览。我们的 VLA 模型和 On-Device 模型面向[早期访问合作伙伴](https://docs.google.com/forms/d/1sM5GqcVMWv-KmKY3TOMpVtQ-lDFeAftQ-d9xQn92jCE/viewform?ts=67cef986&edit_requested=true)开放。请阅读我们的[开发者博客](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-robotics-er-2/)，了解如何将这些模型带到你的硬件上。

## 行动中的人形机器人：管理全身任务

这个世界是为人类的运动方式而建造的；它要求我们在狭窄、杂乱的空间中伸展、弯腰并保持平衡。虽然我们之前的模型控制人形机器人的上半身来完成桌面任务，但 Gemini Robotics 2 将物理 AI 扩展到了全身运动。

我们的模型首次可以控制整个人形机器人，将意图转化为智能的全身控制。例如，在控制 [Apptronik 的 Apollo 2](https://apptronik.com/apollo/apollo-2) 人形机器人时，我们可以让它“把浇水壶放进最下层货架的绿色收纳箱里”。Apollo 会处理这一指令，走到桌边，拿起浇水壶，再走几步到货架前，然后精准地把它放到目的地。虽然我们的机器人在移动速度方面仍有待提升，但这是朝着完成更复杂的真实世界任务所需的全身协调能力迈出的重要一步。

[ 您的浏览器不支持 video 标签。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/MVCfTE-4h3AwDVPZ/GR2_Wholebody_posterframe_v01.webm)

## 为手和夹爪带来高级灵巧能力

要真正在我们的家庭和工作场所派上用场，机器人需要精细的操作能力。Gemini Robotics 2 在不同的末端执行器上——无论机器人使用的是手还是夹爪——解锁了新水平的物理灵巧性，让机器人比以往任何时候都更有用。

该模型现在可以控制 Apollo 2 机器人上五指、22 自由度的 SharpaWave 手，完成系绳结或密封密封袋等精细动作。它还可以操作 [Franka Duo 平台](https://franka.de/fr3-duo)上的标准两指平行夹爪来执行复杂的灵巧任务（例如紧凑装箱）。我们将继续提升精度和速度水平，以实现人类水平的灵巧操作。

[ 您的浏览器不支持 video 标签。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/MVCfTE-4h3AwDVPZ/GR2_Dexterity_posterframe_v01.webm)

## 以智能体化推理和多机器人协作解锁高级任务

大多数真实世界任务需要在较长时间内完成多个步骤。为了管理这种复杂性，我们的具身推理（ER）模型 Gemini Robotics ER 2 充当机器人的高层大脑，处理用户指令并与人类沟通。它观察房间、推理完成任务所需的步骤、与 VLA 协调以执行动作，并跟踪进度直到任务完成。这种配置使机器人能够执行复杂的多步骤任务，在某一步失败时自我纠正，并泛化到新情况和目标。

在本次更新中，我们让机器人能够更可靠地执行更长的任务序列——持续数分钟并涉及数百个决策。Gemini Robotics ER 2 现在能理解任务的开始与结束，并能准确定位关键事件发生的时刻，这标志着进度理解能力的重大跃升。

此外，我们还在推出多机器人协作。这使不同类型的机器人能够沟通并协同工作，以解决单个机器人无法独立完成的复杂工作流。

[ 您的浏览器不支持 video 标签。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/MVCfTE-4h3AwDVPZ/GR2_MultiRobot_posterframe_v04.webm)

## 让设备本地模型快速适配任何机器人

许多机器人应用需要在没有网络延迟或没有互联网连接的情况下运行。Gemini Robotics On-Device 2 正是专门为应对这些限制而构建的——它是我们最高效的视觉-语言-动作模型（VLA），经过优化可在机器人设备上本地运行。

该模型原生支持多本体，并继承了来自 [Gemini Robotics 1.5](https://deepmind.google/blog/gemini-robotics-15-brings-ai-agents-into-the-physical-world/) 的先进“运动迁移”技术。现在，我们只需几小时的适配时间、通常少于 200 个样本，就能适配新的双臂机器人本体。即使面对形状、传感器和自由度差异巨大的全新本体也同样有效，如下方 Dexmate、SO101 和 Trossen 平台执行的一组多样化任务所示。

![](https://lh3.googleusercontent.com/-CSJxggUnu5m5TfompiXP2z7YLThhUvDn2-kBueCZv6HCEWWefUt_WLzM6wxnTV1sTGqBbvmXDnOTB12W18NDr2NgFVXvHKCiTtjfXpyzuOYPJZXlg=w1440-h810-n-nu)

![ 您的浏览器不支持 video 标签。](https://lh3.googleusercontent.com/-CSJxggUnu5m5TfompiXP2z7YLThhUvDn2-kBueCZv6HCEWWefUt_WLzM6wxnTV1sTGqBbvmXDnOTB12W18NDr2NgFVXvHKCiTtjfXpyzuOYPJZXlg)

## 践行我们对安全、负责任机器人技术的承诺

安全是我们机器人研究的基石。随着机器人获得更多的物理能力，我们致力于确保端到端的安全与对齐。在每次发布中，我们都采取了多层次的方法，将传统的物理安全措施与稳健的 AI 安全框架相结合。

Gemini Robotics 2 特别在应对真实世界的不确定性以及与人类协作方面推进了机器人安全。

我们推出了 [ASIMOV-Agentic](https://huggingface.co/datasets/google/asimov_agentic/blob/main/README.md)，这是一个针对智能体安全编排与不确定性裁决的新基准测试。例如，它衡量具身推理智能体拒绝来自 VLA 的不安全工具调用的能力；它还衡量智能体预测任务是否可行，以及在不确定时主动请求人类介入的能力。

此外，凭借增强的具身推理能力，Gemini Robotics ER 2 是我们在安全约束遵循和人类接近度基准测试中迄今最安全的机器人模型。它能更好地检测是否有人在附近，触发安全工具调用，并在有人靠得太近时让机器人安全停止。这是协作安全标准中的一项关键要求。更多细节请阅读我们的 [Gemini Robotics 2：安全技术报告](https://storage.googleapis.com/deepmind-media/gemini-robotics/Gemini-Robotics-2-Safety.pdf)。

## 迈向通用物理 AI

Gemini Robotics 2 标志着在物理世界中求解 AGI 道路上的一个重要里程碑。释放机器人技术的真正潜力，需要超越单一任务的自动化，走向通用智能。通过构建这一核心智能，我们的目标是让物理世界中的 AI 能够与人类并肩解决复杂挑战。

**探索 Gemini Robotics 2**

[在 Google AI Studio 中试用](https://ai.dev/prompts/new_chat?model=gemini-robotics-er-2-preview)[查看 Gemini Robotics ER 2 模型卡](https://deepmind.google/models/model-cards/gemini-robotics-er-2/)[查看 Gemini Robotics On-Device 2 模型卡](https://deepmind.google/models/model-cards/gemini-robotics-on-device-2/)[在开发者博客上了解更多](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-robotics-er-2/)[注册我们的可信测试者计划](https://docs.google.com/forms/d/1sM5GqcVMWv-KmKY3TOMpVtQ-lDFeAftQ-d9xQn92jCE/viewform?ts=67cef986&edit_requested=true)[在 Gemini Enterprise Agent Platform 上试用（私密预览）](https://console.cloud.google.com/agent-platform/publishers/google/model-garden/gemini-robotics-er-2-preview-info)

**致谢**
本工作由 Gemini Robotics 团队开发：Abhijit Ogale, Abhishek Jindal, Adil Dostmohamed, Adrian Collister, Alan Thompson, Alessio Quaglino, Alex Bewley, Alex Hofer, Alex Taeho Kim, Alex X. Lee, Alex Zihao Zhu, Allen Chai, Amaris Paryag, Amit Hampaul, Amy Nommeots-Nomm, Amy Shen, Andre Araujo, Andrew Gallagher, Anirudha Majumdar, Anna Volosina, Annie S. Chen, Annie Xie, Anthony Brohan, Antoine Laurens, Arunkumar Byravan, Asaf Revach, Assaf Hurwitz Michaely, Baruch Tabanpour, Ben Moran, Benoit Landry, Bingyi Cao, Bogdan Mazoure, Brandon Hernaez, Brijen Thananjeyan, Bryan Anenberg, Caden Lu, Carl Doersch, Carolina Parada, Caroline Pantofaru, Charles Shu, Chengda Wu, Christine Chan, Christy Koh, Chuyuan Fu, Claire Cui, Clare Lee, Claudio Fantacci, Connor Schenck, David Rendleman, Deepali Jain, Demetra Brady, Dennis Li, Dhruv Shah, Dimple Vijaykumar, Dirk Ehrlich, Divya Garikapati, Dmitry Kalashnikov, Dre Mahaarachchi, Dushyant Rao, Erik Frey, Fangchen Liu, Federico Casarini, Francesco Nori, Francesco Romano, Frankie Garcia, Gabor Simko, Gautam Salhotra, Giulia Vezzani, Grace Popple, Grace Vesom, Graziano Misuraca, Guangyao Zhou, Hagen Soltau, Hanzi Mao, Hao-Tien Lewis Chiang, Harris Chan, Hila Noga, Howard Zhou, Ian Storz, Idan Lev-Yehudi, Ignacio Rocco, Inessa Konstanz, Isaac Reid, Ishita Prasad, Ivan Kapelyukh, J. Chase Kew, Jacky Liang, Jake Varley, James Susilo, Jasmine Hsu, Jerad Kirkland, Jeremy Plassmann, Jessica Lo, Jie Tan, Jimmy Yan, Jingwei Zhang, Jinyu Xie, Jose Enrique Chen, Joshua Ainslie, Joss Moore, Juanita Bawagan, Junkyung Kim, Justin Lidard, Kanishka Rao, Kathryn Quinn Shea, Kaustubh Sridhar, Keerthana Gopalakrishnan, Ken Caluwaerts, Kenneth Oslund, Khimya Khetarpal, Konstantinos Bousmalis, Krista Reymann, Krzysztof Choromanski, Ksenia Konyushkova, Kun Zhang, Kunal Aneja, Laura Graesser, Leen Verburgh, Leonard Hasenclever, Li-Heng Lin, London Chappellet-Volpini, Lucie Kerley, Maria Attarian, Maria Bauza Villalonga, Marissa Giustina, Max McCabe, Meet Kirankumar Dave, Mehdi S. M. Sajjadi, Metin Tokosz-Exley, Michael Neunert, Michael Noseworthy, Michiel Blokzijl, Miguel Rivas, Mithun George Jacob, Mitsuhiko Nakamoto, Mo Dawoud, Mohan Kumar Srirama, Mohit Sharma, Mohit Shridhar, Muinat Abdul, Murilo F. Martins, Nadav Olmert, Nathan Batchelor, Nicolas Heess, Niko Milonopoulos, Norman Di Palo, Oliver Groth, Ouais Alsharif, Padmini Copparapu, Parth Parekh, Paul Ruiz, Paul Wohlhart, Peide Huang, Peng Xu, Pengfei Xing, Peter Pastor, Petko Yotov, Phil Duffy, Philemon Brakel, Rachel Sterneck, Rajkumar Vasudeva Raju, Ravin Kumar, Razvan Surdulescu, René Wagner, Reza Sanatinia, Robert Baruch, Robert McDonald, Robert Moreno, Rohan Thakker, Roland Hafner, Ryan Doss, Sajjad Zafar, Sally Jesmonth, Sam Haves, Saminda Abeyruwan, Sandy Han Huang, Scott Crowell, Seliem El-Sayed, Sergey Yaroshenko, Sergio Martinez Abad, Serkan Cabi, Sharath Maddineni, Shuang Li, Sichun Xu, Silvia Cruciani, Skanda Koppula, Skye Yang, Soo Sung, Stefan Welker, Stefani Karp, Stefano Saliceti, Steven Hansen, Stuart Bowers, Sumeet Singh, Svetlana Grant, Takahiro Miki, Takuma Yoneda, Thomas Buschmann, Thomas Lampe, Thomas Power, Thor Schaeff, Tim Hertweck, Tingnan Zhang, Todd McInally, Todor Davchev, Tong Zhao, Travers Rhodes, Tsang-Wei Edward Lee, Vika Koriakin, Vikas Sindhwani, Wenhao Yu, Wentao Yuan, Xiaolin Fang, Yahav Nussbaum, Ying Sheng, Ying Xu, Yuheng Kuang, Yuxiang Yang, Yuxiang Zhou

感谢 Jean-Baptiste Alayrac、Zoubin Ghahramani、Koray Kavukcuoglu 和 Demis Hassabis（德米斯·哈萨比斯）对这项工作的领导与支持。我们还要感谢 Google 和 Google DeepMind 中为这项工作做出贡献的众多团队，包括法务、市场、传播、责任与安全委员会、负责任开发与创新、政策、战略与运营，以及我们的业务和企业发展团队。感谢机器人团队中所有上文未一一提及的同事一直以来的支持与指导。最后，感谢我们的合作伙伴 Apptronik、Boston Dynamics 和 Agile Robots 团队的支持。
